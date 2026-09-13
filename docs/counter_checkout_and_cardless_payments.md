# In-person checkout + cardless payment (QR / WhatsApp / M-Pesa)

## What this is for

`Ecommerce.php` only supported customer-initiated checkout through a chat storefront.
This change adds:

1. A merchant-facing counter-checkout flow — finalize an existing pickup order, or ring
   up a walk-in sale with no prior online order.
2. A per-order, per-amount hosted checkout QR/pay-link, so a merchant without a card
   machine can let the customer pay on their own phone, auto-confirmed via webhook.
3. A verified-vs-declared payment-status distinction, so `manual_payment()`/
   `cod_payment()` (pure self-declaration) are visibly distinct from a gateway-confirmed
   payment.
4. An M-Pesa gateway for Kenya, wired into the same QR/pay-link flow (as an STK push
   prompt instead of a scan, since M-Pesa doesn't have a scan-based hosted checkout).
5. Pushing the generated pay link directly into the buyer's Messenger thread, and a
   scoped WhatsApp Business (Cloud API) sender for the same purpose — see "Social
   checkout channels" below for what was and wasn't extended here, and why.

## Architecture decision: M-Pesa via direct Daraja integration, not extending Paystack

Two options were considered, per the task brief:

1. **Extend the existing Paystack integration** (`Paystack_class_ecommerce.php`) to
   cover M-Pesa/mobile money for Kenya.
2. **Direct integration with Safaricom's Daraja API** (STK Push), as a new
   self-contained gateway library matching the existing pattern.

**Decision: option 2.** Confirmed by reading the actual code, not assumed:

- `Paystack_class_ecommerce.php` (before this change) only did two things: build an
  inline-JS "Pay with Paystack" popup button, and verify a transaction reference
  server-side (`GET /transaction/verify/{reference}`). It never called Paystack's
  hosted-checkout **Initialize Transaction** endpoint, and grepping the file for
  `mobile_money`, `mpesa`, `channels`, or `KES` returns zero matches anywhere in this
  repository's Paystack code.
- Because this integration never uses Paystack's `channels` parameter (the mechanism
  Paystack uses to opt a transaction into mobile-money rails in supported markets) at
  all, making Paystack handle M-Pesa here would mean building the missing
  hosted-checkout + channels + Kenya-market support essentially from scratch — no less
  work than a self-contained Daraja library, while also resting on assumptions about
  Paystack's current API surface for Kenya that can't be verified from this
  environment (no network access to Paystack's live docs/dashboard, no sandbox
  credentials).
- Daraja's STK Push flow (OAuth token → STK push request → async callback) maps
  directly onto the same self-contained gateway-library shape already used by
  `Paystack_class_ecommerce.php`, so it was no extra architectural cost to add
  `Mpesa_class_ecommerce.php` alongside it.

STK Push also changes the UX slightly from the other gateways: instead of a QR to scan,
the customer's phone receives a native M-Pesa payment prompt directly. `counter_generate_pay_link()`
routes to M-Pesa STK push automatically when a store's currency is `KES` and M-Pesa is
enabled, so the merchant-facing flow ("generate pay link, customer's phone gets a way
to pay, order auto-confirms") is the same shape either way.

## What was built

- `application/libraries/Paystack_class_ecommerce.php` — added `initialize_transaction()`
  (Paystack hosted-checkout, additive) and `verify_webhook_signature()`. Existing
  `set_button()`/`paystack_payment_action()` are unchanged.
- `application/libraries/Mpesa_class_ecommerce.php` — new self-contained Daraja STK
  Push library (`get_access_token()`, `stk_push()`, `query_stk_status()`).
- `application/controllers/Ecommerce.php`:
  - New: `counter_checkout()`, `counter_search_order()`, `counter_start_sale()` (Piece 1
    — counter/walk-in checkout, reusing `update_cart_item()`/`proceed_checkout()`
    unmodified for cart mutation and payment-option resolution).
  - New: `counter_generate_pay_link()`, `paystack_webhook()`, `mpesa_action()`,
    `mpesa_webhook()`, and private helpers `mark_paystack_cart_paid()` and
    `trigger_mpesa_stk_push()` (Piece 2/4 — QR/pay-link + auto-confirm).
  - Modified: `paystack_action()` — its field-write logic was extracted into
    `mark_paystack_cart_paid()` so the existing browser-redirect callback and the new
    server-to-server webhook don't duplicate the "mark cart paid" logic. The fields
    written and their values are unchanged from before.
  - Modified: `manual_payment()`, `cod_payment()` — now set the new
    `payment_verification_method` column to `'merchant_declared'`. No other behavior
    changed.
  - Modified: the manual-payment checkout button's label (adds "(cash / other,
    unverified)"), and `order_list_data()`'s payment-method column (adds a
    "Verified"/"Declared" badge from the new column).
  - Modified: the store settings-save action and `payment_accounts.php` view — new
    M-Pesa credential fields (`ecommerce_config`) and enabled-flag (`ecommerce_store`),
    following the exact field-by-field pattern already used for Paystack/Razorpay/etc.
- `application/views/ecommerce/counter_checkout.php` — new merchant-facing view.
- `application/libraries/Whatsapp_cloud_api.php` — new, scoped WhatsApp Business
  (Cloud API) sender (see "Social checkout channels" below).
- `application/controllers/Home.php` — `central_webhook_callback()` gets one explicit
  branch acknowledging WhatsApp Cloud API payloads (see below).
- `assets/backup_db/counter_checkout_payments.sql` — additive schema migration (see
  below).

## Social checkout channels: what's real, what's scoped, what's not feasible

Before wiring anything, the actual state of each channel was checked in code (not
assumed), since the platform's marketing covers Messenger/Instagram/WhatsApp broadly
but the underlying integrations are at very different levels of completeness:

- **Messenger — mostly real, one gap closed here.** `confirmation_message_sender()`
  already pushes a receipt/button-template message back into the buyer's Messenger
  thread via the existing `send_messenger_reminder()` (skipped automatically for
  non-chat/"sys" subscribers) once an order is marked paid. The gap this PR closes:
  `counter_generate_pay_link()` now also proactively pushes the pay link itself into
  the thread the moment it's generated (`push_pay_link_to_messenger()`, a button
  template identical in shape to the existing post-checkout "My Orders" button
  message), and pushes a plain-text STK-push notice for the M-Pesa branch
  (`push_text_to_messenger()`). Both are best-effort — a send failure never blocks the
  pay link from being returned to the merchant's screen.
- **WhatsApp Business API (WABA) — genuinely a stub before this PR, now has a scoped
  sender.** OAuth scopes (`whatsapp_business_messaging`/`whatsapp_business_management`)
  were requested in an earlier commit, but `Livechat.php::get_bot_whatsapp_by_phone_number_id()`
  is dead code (`return [];`, the real query is commented out) and no `whatsapp_bots`
  table exists — there was no working Cloud API send path anywhere. Building a full
  WhatsApp inbox (embedded signup, multi-bot management, inbound conversation
  threading in Livechat) is a large, separate feature and stays out of scope here.
  What was built instead is deliberately narrow: `Whatsapp_cloud_api::send_text_message()`
  posts a plain text message to `graph.facebook.com/v19.0/{phone_number_id}/messages`
  using per-store credentials (`whatsapp_business_enabled`/`_phone_number_id`/
  `_access_token` on `ecommerce_config`, entered directly in Appearance Settings next
  to the existing WhatsApp order-notification fields — there's no existing
  manual-token-entry UI pattern to reuse, so this is a small new form section
  following that screen's existing layout). `counter_generate_pay_link()` tries this
  first for the payment link and falls back to the existing `wa.me` click-to-chat link
  if it's not configured or the send fails.
  - **Known limitation, not fixed here**: WhatsApp requires a pre-approved message
    template for business-initiated messages sent outside a 24-hour customer-service
    session window. A plain text send works when the customer messaged the business
    first (or paid via the storefront chat) within that window; a cold outbound send
    (e.g. purely from a counter walk-in phone number with no prior conversation) would
    be rejected by Meta without an approved template — building and submitting a
    template requires a live, verified Meta Business Manager app this environment
    doesn't have, so it's left as a follow-up.
  - `Home::central_webhook_callback()`'s existing GET handshake already answers Meta's
    verify-token challenge for any product, so it needed no change. Its POST dispatcher
    gets one explicit branch: a WhatsApp Cloud API payload (`value.messaging_product
    == 'whatsapp'`) is acknowledged and dropped, matching what the existing
    unmatched-payload fallthrough already did (a plain 200 response) — added mainly for
    clarity that this is a deliberate no-op, not an oversight, since this PR doesn't
    process inbound WhatsApp conversations.
- **Instagram — not feasible for DM-driven checkout, so nothing was built.** Instagram's
  Graph API only exposes `send_private_reply()` (a one-shot reply seeded from a
  specific comment/mention), not a general bidirectional DM send the way Messenger's
  `/me/messages` works. There's no way to push an unprompted "here's your pay link"
  message into an Instagram DM thread with the API this platform has access to.
- **Other social channels** (Telegram, Twitter/X, etc.) don't exist anywhere in this
  codebase — adding them would mean building entirely new platform integrations, well
  beyond a checkout feature.

## Cross-border payment: already works, no code needed

Checked whether "cross-border cash send" meant accepting a foreign customer's payment
(already covered) or real P2P money transfer/remittance (a licensing and compliance
question, out of scope per the user). For the former: every gateway library already in
this codebase (`Stripe_class_ecommerce.php`, `Paystack_class_ecommerce.php`,
`Razorpay_class_ecommerce.php`, `Mollie_class_ecommerce.php`, `Paypal_class_ecommerce.php`)
passes the store's configured `currency` straight through with no whitelist or
restriction, and there is no buyer-vs-merchant currency separation anywhere in
`Ecommerce.php` — a merchant already accepts a foreign customer's card/payment in
their own configured currency, with FX conversion handled entirely on the card
network/gateway side, exactly like ordinary multi-currency card acceptance. Nothing in
this codebase blocks that today, so no change was made here.

## Schema changes (`assets/backup_db/counter_checkout_payments.sql`)

All additive; every new column is `DEFAULT`-backed so existing rows and behavior are
unaffected until the new flows are used:

- `ecommerce_cart.sale_channel` (`online`/`counter`) — set by `counter_start_sale()`.
- `ecommerce_cart.payment_verification_method` (`gateway_verified`/`merchant_declared`)
  — defaults to `gateway_verified` so every existing gateway `_action` method needed
  zero code changes to be correct; only `manual_payment()`/`cod_payment()` explicitly
  override it.
- `ecommerce_cart.mpesa_checkout_request_id` — a dedicated column, not reused from
  `transaction_id`: Safaricom's `CheckoutRequestID` (~24-27 chars) doesn't reliably fit
  `transaction_id`'s `varchar(25)`. `mpesa_webhook()` resolves the cart by this column,
  then writes the short, final `MpesaReceiptNumber` into `transaction_id`.
- `ecommerce_store.mpesa_enabled` — placed on `ecommerce_store`, matching where every
  other gateway's `_enabled` flag already lives (not `ecommerce_config`, which holds
  credentials only).
- `ecommerce_config.mpesa_consumer_key` / `mpesa_consumer_secret` / `mpesa_shortcode` /
  `mpesa_passkey` / `mpesa_environment` — Daraja credentials, alongside the existing
  per-gateway credential columns on that table.
- `ecommerce_config.whatsapp_business_enabled` / `_phone_number_id` / `_access_token` —
  WhatsApp Business (Cloud API) credentials for the scoped checkout-link sender, kept
  alongside the existing `whatsapp_send_order_button`/`whatsapp_phone_number` cosmetic
  click-to-chat fields already on this table (different mechanism, same table).

## Idempotency: the one pre-existing gap this change touches carefully

`confirmation_message_sender()` (the shared "mark order done" hook every gateway calls)
decrements `ecommerce_product.stock_item` with **no idempotency guard of its own** — it
only checks `action_type=='checkout'`. That was a tolerable gap when the only trigger
was a one-shot browser redirect. It stops being tolerable once webhooks are in the
picture, since gateways legitimately retry undelivered/unacknowledged webhooks.

Both new webhook handlers (`paystack_webhook()`, `mpesa_webhook()`) guard against this
explicitly and locally: they only proceed to write the cart / call
`confirmation_message_sender()` if the cart's `status` is not already
`approved`/`completed`. This guard is scoped to the new webhook code paths — the
existing gateway `_action` methods (browser redirects) are untouched, since they were
out of scope and already effectively single-shot in practice.

## Deliberately deferred (not silently skipped)

- **Live testing against Paystack and Safaricom Daraja sandboxes** — no credentials
  available in this environment, and no PHP toolchain to boot the app at all (per
  `CLAUDE.md`). Everything above is written defensively but unboot-tested.
- **Hosted checkout for other gateways** (Mollie also supports one) — Paystack + M-Pesa
  cover the brief; adding more is a natural, independent fast-follow.
- **Nav-menu entry for `counter_checkout`** — reachable today at
  `ecommerce/counter_checkout/{store_id}`; wiring a menu link in is minor UI polish, not
  functional.
- **General WhatsApp livechat/inbox support** — `Livechat.php`'s `whatsapp_bots` stub,
  embedded signup, multi-bot management, inbound conversation threading. Pre-existing,
  separate, and much larger than a checkout PR should take on; only a scoped outbound
  sender for payment links was built here (see "Social checkout channels" above).
- **WhatsApp message template approval** — needed for a cold outbound send outside a
  24-hour session window; requires a live, verified Meta Business Manager app this
  environment doesn't have.
- **Instagram DM checkout / other social channels (Telegram, Twitter, etc.)** — not
  feasible with Meta's current API for Instagram, and don't exist at all for the
  others; see "Social checkout channels" above for why.

## Manual test plan for a real environment

1. Run `assets/backup_db/counter_checkout_payments.sql` against the target database.
2. In the store's payment settings (`ecommerce/payment_accounts`), fill in Paystack
   test keys and/or M-Pesa Daraja sandbox credentials (consumer key/secret, shortcode,
   passkey, environment=sandbox), and enable the relevant gateway flag.
3. Visit `ecommerce/counter_checkout/{store_id}` as the store's admin:
   - Start a walk-in sale, add products, generate a pay link/QR, and pay it in the
     Paystack sandbox (or trigger the M-Pesa sandbox STK push) — confirm the webhook
     flips `ecommerce_cart.status` to `approved` and decrements `stock_item` exactly
     once (not twice, even if you deliver the webhook payload a second time).
   - Search for and resume an existing pickup order (`store_pickup=1`) by cart ID and
     by phone number.
4. Exercise `manual_payment()` end-to-end and confirm the order list shows a "Declared"
   badge, versus "Verified" for a gateway-confirmed order.
5. In Appearance Settings, configure a WABA test number's `phone_number_id`/access
   token (from Meta's WhatsApp test number in Business Manager) and enable it; generate
   a pay link from counter-checkout with a `buyer_mobile` set and confirm a real
   WhatsApp message arrives (`whatsapp_sent` in the response should be `true`) — and
   confirm the `wa.me` fallback link still works when WABA isn't configured.
6. Confirm a genuine (non-counter) Messenger subscriber's thread receives a "Pay Now"
   button message when a pay link is generated for their cart, and a plain-text STK-push
   notice when M-Pesa is used instead.
