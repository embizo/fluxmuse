# CLAUDE.md

Guidance for Claude Code when working in this repository.

## What this is

**Fluxmuse AI** is a self-hosted social-media marketing & chatbot automation platform.
The codebase is a **ChatPion** application (product_name `ChatPion`, version `9.4.3` in
`application/config/my_config.php`) that has been rebranded to Fluxmuse. It covers
Facebook/Instagram/Messenger bots, autoposting & scheduling, e-commerce, SMS/email
marketing, live chat, comment automation, and AI reply features.

## Tech stack

- **PHP** ≥ 7.4 (see `composer.json`)
- **CodeIgniter 3.1.5** (`system/`) with **HMVC** (Modular Extensions) — modules live in
  `application/modules/`
- **MySQL** via CI's `mysqli` driver
- **Pusher** for realtime (live chat, notifications)
- **Composer** deps: `pusher/pusher-php-server`, `google/apiclient`, `symfony/var-dumper`
  (`vendor/` is committed to the repo)
- Front-end: jQuery + Bootstrap + a large set of vendored `plugins/` (summernote,
  select2, fullcalendar, apexcharts, formbuilder, flow_builder, etc.)

## Layout

- `application/controllers/` — 35 top-level controllers (`Home`, `Dashboard`, `Admin`,
  `Autoposting`, `Messenger_bot*`, `Payment`, `Stripe_action`, `Ecommerce`, …)
- `application/modules/` — HMVC feature modules: `ai_reply`, `visual_flow_builder`,
  `ultrapost`, `instagram_bot`, `instagram_poster`, `instagram_poster`, `blog`,
  `menu_manager`, `simplesupport`
- `application/models/` — only a few shared models here (`Basic.php`,
  `Grocery_CRUD_Model.php`); most data logic lives inside modules and controllers
- `application/libraries/` — 46 libraries (payment gateways, Google API, Pusher wrapper,
  grocery CRUD, etc.)
- `application/config/` — CI config. Routing in `routes.php`
  (`default_controller = home`, `404_override = home/error_404`)
- `application/views/` — top-level views; module views live under each module
- `assets/`, `js/`, `plugins/` — front-end assets
- `upload/`, `upload_caster/`, `download/` — user-generated / runtime content
- `ci/` — CI-related scripts
- `system/`, `vendor/` — framework & Composer deps (do not edit)

## Conventions

- CodeIgniter naming: controller/model/library **class files are `Ucfirst.php`**;
  methods map to URL segments (`Controller/method`).
- Routes are defined in `application/config/routes.php` — check there before assuming a
  URL maps 1:1 to a controller method.
- HMVC: cross-module calls use `Modules::run()` / `$this->load->module()`.
- Keep changes idiomatic to CI3 — this is a legacy framework; match surrounding style.

## Running locally

Requires a PHP + MySQL environment (e.g. LAMP/MAMP/Docker) with the web root pointed at
the project root; `index.php` is the front controller and `.htaccess` handles rewriting.
Configure:
- `application/config/database.php` — DB connection
- `application/config/config.php` — `base_url`
- `application/config/my_config.php`, `frontend_config.php` — product/app config

There is currently no PHP toolchain on PATH in this environment, so the app cannot be
booted from here without one installed.

## Important notes / gotchas

- `vendor/` and `system/` are vendored — don't hand-edit; update via Composer / upstream.
- This is a large white-label product; a lot of features are toggled by config and admin
  settings rather than code paths, so behavior can depend on DB/admin state.

## Security follow-up (resolved)

Config files (`database.php`, `config.php`, `pusher.php`, `my_config.php`,
`package_config.php`, `frontend_config.php`) are `.gitignore`d and untracked
(`.example` templates are tracked instead) as of commits `cd564cca` and `f69a99da`.

Audited the full git history of every one of those files (each only ever existed in
one commit, `b8caae1c`, before being untracked) to check whether real secrets had been
exposed on the public `embizo/fluxmuse` repo. Result: no real credentials were ever
committed — `database.php`'s hostname/username/password/database and `pusher.php`'s
app_id/key/secret were all empty-string placeholders; no other file had a non-empty
key/secret/token. The one non-empty value, `config.php`'s `encryption_key = '12345'`,
is an obvious default placeholder, not a production secret. Nothing needs rotating.

Checked the untracked `application/config/config.php` present in this working copy:
its `encryption_key` is a 64-character hex string (32 random bytes) — a properly
strong key, not the `'12345'` placeholder. Note this environment has no PHP toolchain
and isn't the deployed server (see "Running locally" above), so this only confirms
the key in *this local file*; it doesn't confirm what's actually configured on the
live production host. If the production server's `config.php` was ever seeded from
the same placeholder-containing `b8caae1c` commit and not since regenerated, rotate
its `encryption_key` there directly (changing it invalidates existing sessions/cookies
but rotating a weak key outweighs that).
