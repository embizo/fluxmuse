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

- **Secrets are committed.** `application/config/database.php` and other config files
  containing credentials/API keys are tracked in git. Treat them as sensitive; avoid
  printing secret values. See "Security follow-up" below.
- `vendor/` and `system/` are vendored — don't hand-edit; update via Composer / upstream.
- This is a large white-label product; a lot of features are toggled by config and admin
  settings rather than code paths, so behavior can depend on DB/admin state.

## Security follow-up (not yet done)

- No `.gitignore` exists and live-looking DB credentials + API keys are committed. Before
  any public push, consider moving secrets to environment/untracked config and rotating
  anything already exposed on GitHub (`origin` = github.com/embizo/fluxmuse).
