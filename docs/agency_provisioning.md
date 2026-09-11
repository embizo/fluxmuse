# Agency ($346/mo) tier — provisioning pipeline

## What this is for

The Agency package is the highest Fluxmuse pricing tier. A customer who buys it should
end up owning their own white-labeled Fluxmuse instance — reachable at either a
Fluxmuse-issued subdomain (`clientname.fluxmuse.app`) or a domain/subdomain they point
at Fluxmuse themselves via CNAME — where they are the `Admin` of that instance.

This document is the design write-up requested alongside the code in this change. It
covers the architecture decision, what was actually built, and exactly what remains
manual/unwired because it needs real infrastructure credentials this environment
doesn't have.

## Architecture decision: clone-per-client, not shared multi-tenancy

Two models were considered:

1. **Clone-per-client** — each Agency client gets a real, separate deployment (own
   codebase copy/container, own database, own config files). Subdomain/custom-domain
   routing just points DNS at that instance's own server.
2. **Shared-app, host-routed multi-tenancy** — one running app resolves the tenant from
   the `Host` header per request, with a tenant-scoping column added across most
   tables.

**Decision: clone-per-client.** Confirmed, not just assumed, by checking the codebase:

- There is no `tenant_id`/`account_id`/`white_label`/`multi_tenant` concept anywhere in
  `application/` (grepped controllers, models, modules, config). Every `Admin`-gated
  controller (`Custom_theme_manager.php`, `Update_system.php`, `Admin.php`, and now
  `Agency_provisioning.php`) assumes it is the only tenant on the install.
- Branding (`application/config/my_config.php` — `product_name`, `slogan`, etc.) and
  theming (`application/views/admin/theme/style_theme.php`'s `$PRIMARY_COLOR`, sourced
  from `ecommerce_config`/install-level settings) are install-level PHP config files and
  DB rows, not columns scoped to a tenant.
- Payment gateway credentials (`Payment.php`) are configured once per install, with no
  per-tenant credential storage.
- `Update_system.php` updates exactly the one running install it's called on.

Retrofitting option 2 onto this codebase would mean adding tenant-scoping to most of the
~50+ tables in `assets/backup_db/initial_db.sql`, rewriting every `Admin`-gate to also
check tenant ownership, and turning every config file into a per-tenant DB lookup — a
rewrite an order of magnitude larger than what a first Agency-tier pass justifies, and
one that fights the framework's existing single-tenant assumptions at every turn.
Clone-per-client requires real infra automation, but zero app-level rewrite — each
clone runs the existing single-tenant codebase completely unmodified.

## What was built (this change)

All of it lives on the **control-plane install** — the one Fluxmuse itself runs that
sells the Agency package and tracks provisioning requests. It does not modify how a
provisioned clone behaves; clones run the stock single-tenant app.

- **`assets/backup_db/agency_provisioning.sql`** — additive migration (same
  `CREATE TABLE IF NOT EXISTS` style as `initial_db.sql`):
  - `agency_instances` — one row per requested/provisioned client instance: company
    name, domain mode + subdomain/custom domain, admin name/email, branding
    (product name, primary color, logo path), a self-issued `license_key`, a
    `suggested_db_name`, the path the generated config export was written to, and two
    status columns (`dns_status`, `instance_status`) tracked through the pipeline.
  - `agency_provisioning_config` — single settings row (same pattern as
    `ecommerce_config`/`sms_api_config`) for the *Fluxmuse-owned* DNS/hosting
    provider settings (`base_domain`, `dns_provider` + credentials, `hosting_provider`
    + credentials, ACME contact email). Ships with safe empty/`manual` defaults.
  - An `INSERT` into `menu_child_1` wiring an "Agency Instances" sidebar link under the
    existing DB-driven "System" menu (see `application/modules/menu_manager`), the same
    way `Update_system`/`Menu_manager`/etc. are already wired.

- **`application/controllers/Agency_provisioning.php`** — `Admin`-gated controller,
  same conventions as `Custom_theme_manager.php`/`Announcement.php`:
  - `new_instance` / `create_action` — captures company name, desired subdomain
    (always collected — it doubles as the internal instance slug even in custom-domain
    mode), domain mode (Fluxmuse subdomain vs. client CNAME) + custom domain, instance
    admin name/email, the purchasing `users` row and `package_id`.
  - Generates a Fluxmuse-owned `license_key` — deliberately **not** the legacy Envato
    `purchase_code` flow already in `Home.php`/`Update_system.php` (that mechanism
    activates against a third-party `xeroneit.net`/`mostofa.club` endpoint Fluxmuse
    doesn't control, and is scoped to one Envato purchase). Instead it's a locally
    signed token (`hash_hmac` keyed on `config['encryption_key']`), verifiable offline
    by anything holding the same key — good enough for a first pass; a real
    online-verifiable licensing service is future work if piracy resistance matters.
  - `show` / `update_status` — view one instance and manually advance
    `instance_status` (`pending → config_generated → dns_configured → active`, or
    `suspended`/`failed`) as an operator actually completes each real-world step.
  - `regenerate_config` — re-render the branding export without re-issuing the license.

- **`application/libraries/Agency_branding_generator.php`** — the branding templating
  layer replacing the old hand-edit-`my_config.php` process. Given an `agency_instances`
  row, it writes to `upload/agency_instances/{subdomain}/`:
  - `config/my_config.php` and `config/frontend_config.php` — ready to overlay onto a
    fresh clone's `application/config/`, pre-filled with the client's product name,
    slogan, and contact email.
  - `manifest.json` — a structured provisioning manifest: the resolved host, DNS record
    type/name/target, ACME/TLS method, the suggested DB name, the admin to seed, and a
    plain-English `action_needed` string for whoever (or whatever automation) finishes
    the clone.

- **Views** under `application/views/admin/agency_provisioning/` (`list`, `create`,
  `show`) matching the existing Bootstrap admin theme.

## What is explicitly NOT wired up (needs real credentials/access)

Nothing here calls a real DNS or hosting API — there are no such credentials in this
sandboxed environment, and the task explicitly scoped that out. What's needed from
Fluxmuse's team to close the loop, one piece at a time:

1. **DNS automation for `*.fluxmuse.app`.** Needs: which registrar/DNS provider
   Fluxmuse actually uses (Cloudflare, Route53, etc.), an API token scoped to creating
   records in that zone, and the zone ID. `agency_provisioning_config` already has
   columns for this (`dns_provider`, `dns_zone_id`, `dns_api_token`) — wiring it up is
   adding a provider-specific client call inside a new
   `_create_dns_record($instance, $provisioning_config)` step, called once
   `instance_status` reaches `config_generated`.
2. **Custom-domain flow for clients' own CNAMEs.** The manifest already tells the
   operator/automation what CNAME target to tell the client to create; verifying it
   resolved (a DNS lookup) and then issuing TLS for it is unbuilt. Needs: an ACME
   client (e.g. Certbot or a Go ACME lib) with DNS-01 or HTTP-01 access to the
   clone's web server, and the `acme_email` already collected in
   `agency_provisioning_config`.
3. **Instance spin-up automation.** Needs: either a Docker host/orchestrator API
   (if clones run as containers) or a hosting-panel API (e.g. cPanel/Plesk/a custom
   panel) that can create a new vhost + MySQL database + import
   `assets/backup_db/initial_db.sql` + overlay the generated `config/` files + set the
   `license_key` + create the `Admin` user from `admin_name`/`admin_email`. The
   `manifest.json` this change generates is designed to be the input to that
   automation once it exists (`hosting_provider` + `hosting_api_endpoint` +
   `hosting_api_token` columns are already reserved in `agency_provisioning_config`).
4. **Fleet updates.** `Update_system.php` still only updates the one install it runs
   on — that's unchanged and correct for a single clone. Once clones exist, rolling out
   a version bump across all Agency clients needs a separate fleet script that iterates
   `agency_instances` where `instance_status = 'active'` and triggers
   `update_system`'s existing per-install update endpoint on each one (e.g. over SSH or
   an authenticated HTTP call) — that iteration script doesn't exist yet.
5. **Billing → provisioning trigger.** This change assumes an operator manually opens
   `agency_provisioning/new_instance` after a Member's Agency purchase clears (the
   `package`/`transaction_history` tables already record that). Auto-triggering
   `create_action` from `Payment.php`'s post-purchase callback once the Agency package
   specifically is bought is straightforward follow-up, deliberately left out here to
   keep this change reviewable as "provisioning pipeline exists" rather than "silently
   changes checkout behavior."

## Explicitly out of scope for this change

- Any live DNS record creation, TLS issuance, or container/hosting spin-up (per above).
- Per-tenant data isolation inside a single running app (rejected architecture, see
  above) — every clone is a fully separate app+DB.
- Rewriting the legacy Envato `purchase_code` activation flow in `Home.php` — left
  untouched; the new `license_key` is a parallel, Fluxmuse-owned mechanism for Agency
  clones only.
- A fleet-update iterator for `Update_system.php` (see point 4 above).
- Auto-triggering provisioning from `Payment.php` checkout (see point 5 above).
