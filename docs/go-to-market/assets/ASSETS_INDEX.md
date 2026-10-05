# FluxMuse asset library

Shared visuals for the go-to-market pack. Every fact on an infographic comes from `../08_Prospects/CURRENT_OFFER.md` and `../00_FACTS_AND_ASSUMPTIONS.md` (refreshed 2026-10-05).
Infographics are 1920×1080 CSS px rendered at 2× (3840×2160 files); `_square` = 1080×1080 @2x, `_portrait` = 1080×1350 @2x, `_dark` = Night #0F1419 ground.
Rebuild everything from `../_build/` (see "Rebuilding" below).

## Brand (`brand/`, 23 files)

| File | Pixels | Ground | What it shows | Suggested use |
|---|---|---|---|---|
| `brand/apple-touch-icon.png` | 512×512 | transparent | Apple touch icon, original file. | web / app |
| `brand/colour-accessibility-pairings.png` | 3840×2160 | light | WCAG contrast of 12 text/background pairs with AAA/AA/large-only/fail labels (computed). | brand kit |
| `brand/colour-palette.png` | 3840×2160 | light | Palette swatches with names, HEX, RGB, HSL (facts-file tokens) and proportion guide. | brand kit |
| `brand/email-signature-banner-600x150.png` | 600×150 | light | Email signature banner at 1x. | email |
| `brand/email-signature-banner-600x150@2x.png` | 1200×300 | light | Email signature banner, retina version; display at 600×150. | email |
| `brand/fluxmuse-icon-512.png` | 512×512 | transparent | The "Muse" icon, 512 px (public/icon-512.png). | brand kit, brand deck, proposal, investor deck, business plan |
| `brand/fluxmuse-icon-on-night-1024.png` | 1024×1024 | dark (Night) | Icon centred on Night #0F1419 square. | brand kit, app stores, social |
| `brand/fluxmuse-icon-on-orange-1024.png` | 1024×1024 | Flux Orange | Icon on Flux Orange square. The icon's warm facets blend into the ground; use sparingly. | brand kit |
| `brand/fluxmuse-icon-on-white-1024.png` | 1024×1024 | light (white) | Icon centred on white square. | brand kit, documents |
| `brand/fluxmuse-icon.png` | 256×256 | transparent | The "Muse" icon, original 256 px file. | brand kit, brand deck, proposal, investor deck, business plan |
| `brand/fluxmuse-logo-dark.png` | 497×165 | transparent (for dark grounds) | Official logo for dark grounds, original file. | brand kit, brand deck, proposal, investor deck, business plan |
| `brand/fluxmuse-logo-light.png` | 640×244 | transparent (for light grounds) | Official logo, original file from the product repo. Note: the "F" stem is clipped at the left edge in this source raster. | brand kit, brand deck, proposal, investor deck, business plan |
| `brand/fluxmuse-logo-lockup-dark-1600x600.png` | 1600×600 | dark (Night) | Logo lockup on Night canvas (upscaled from 497 px source). | brand kit, brand deck, investor deck |
| `brand/fluxmuse-logo-lockup-light-1600x600.png` | 1600×600 | light (white) | Logo lockup on white canvas (upscaled from 640 px source). | brand kit, brand deck, proposal |
| `brand/logo-clear-space-minimum-size.png` | 3840×2160 | light | Clear-space rule (x = wordmark cap height) and minimum sizes (recommendations). | brand kit |
| `brand/logo-misuse-donts.png` | 3840×2160 | light | Logo do's and don'ts: stretch, recolour, low contrast, busy background, rotate, outline. | brand kit |
| `brand/social-avatar-1080.png` | 1080×1080 | dark | Social profile avatar (circle-safe). | social profiles |
| `brand/social-cover-1500x500.png` | 1500×500 | dark | X / LinkedIn-style cover: logo, "AI Marketing & WhatsApp Commerce for Africa", "Paid plans from R149 a month" chip. | social profiles |
| `brand/social-cover-1500x500_guides.png` | 1500×500 | dark | Cover with approximate crop / profile-photo zones overlaid. Planning only; do not upload. | brand kit |
| `brand/social-cover-1640x624.png` | 1640×624 | dark | Facebook page cover, same content. | social profiles |
| `brand/social-cover-1640x624_guides.png` | 1640×624 | dark | Cover with approximate crop / profile-photo zones overlaid. Planning only; do not upload. | brand kit |
| `brand/typography-specimen.png` | 3840×2160 | light | Poppins + Inter specimen and slide type scale. | brand kit |
| `brand/whatsapp-business-profile-640.png` | 640×640 | light | WhatsApp Business profile image (icon inside the circular crop). | WhatsApp Business |

## Product screenshots (`screenshots/`, 30 files)

| File | Pixels | Ground | What it shows | Suggested use |
|---|---|---|---|---|
| `screenshots/demo-full.png` | 2880×3082 | dark (site) | /demo full page. | internal reference |
| `screenshots/demo-step-01-catalog.png` | 2880×1800 | dark (site) | WhatsApp checkout demo step, desktop 1440×900 @2x (side cards mention SnapScan). | brand deck, proposal, investor deck |
| `screenshots/demo-step-01-catalog_mobile.png` | 1170×2532 | dark (site) | WhatsApp checkout demo step, mobile 390×844 @3x. | brand deck, proposal, investor deck |
| `screenshots/demo-step-02-added-to-cart.png` | 2880×1800 | dark (site) | WhatsApp checkout demo step, desktop 1440×900 @2x (side cards mention SnapScan). | brand deck, proposal, investor deck |
| `screenshots/demo-step-02-added-to-cart_mobile.png` | 1170×2532 | dark (site) | WhatsApp checkout demo step, mobile 390×844 @3x. | brand deck, proposal, investor deck |
| `screenshots/demo-step-03-cart.png` | 2880×1800 | dark (site) | WhatsApp checkout demo step, desktop 1440×900 @2x (side cards mention SnapScan). | brand deck, proposal, investor deck |
| `screenshots/demo-step-03-cart_mobile.png` | 1170×2532 | dark (site) | WhatsApp checkout demo step, mobile 390×844 @3x. | brand deck, proposal, investor deck |
| `screenshots/demo-step-04-checkout-details.png` | 2880×1800 | dark (site) | WhatsApp checkout step (desktop 1440×900 @2x or mobile 390×844 @3x). The payment list includes SnapScan, which must never be shown. | brand deck, proposal, investor deck |
| `screenshots/demo-step-04-checkout-details_mobile.png` | 1170×2532 | dark (site) | WhatsApp checkout step (desktop 1440×900 @2x or mobile 390×844 @3x). The payment list includes SnapScan, which must never be shown. | brand deck, proposal, investor deck |
| `screenshots/demo-step-05-payment-method.png` | 2880×1800 | dark (site) | WhatsApp checkout step (desktop 1440×900 @2x or mobile 390×844 @3x). The payment list includes SnapScan, which must never be shown. | brand deck, proposal, investor deck |
| `screenshots/demo-step-05-payment-method_mobile.png` | 1170×2532 | dark (site) | WhatsApp checkout step (desktop 1440×900 @2x or mobile 390×844 @3x). The payment list includes SnapScan, which must never be shown. | brand deck, proposal, investor deck |
| `screenshots/demo-step-06-processing.png` | 2880×1800 | dark (site) | WhatsApp checkout demo step, desktop 1440×900 @2x (side cards mention SnapScan). | brand deck, proposal, investor deck |
| `screenshots/demo-step-06-processing_mobile.png` | 1170×2532 | dark (site) | WhatsApp checkout demo step, mobile 390×844 @3x. | brand deck, proposal, investor deck |
| `screenshots/demo-step-07-confirmation.png` | 2880×1800 | dark (site) | WhatsApp checkout demo step, desktop 1440×900 @2x (side cards mention SnapScan). | brand deck, proposal, investor deck |
| `screenshots/demo-step-07-confirmation_mobile.png` | 1170×2532 | dark (site) | WhatsApp checkout demo step, mobile 390×844 @3x. | brand deck, proposal, investor deck |
| `screenshots/demo.png` | 2880×1800 | dark (site) | /demo landing view: WhatsApp demo store catalog plus side cards (mention SnapScan and "within 30 min"). | brand deck, proposal |
| `screenshots/demo_mobile.png` | 1170×2532 | dark (site) | /demo on mobile 390×844 @3x: page heading and demo store catalog. | brand deck, proposal |
| `screenshots/features-full.png` | 2880×6796 | dark (site) | /features full page: 4 agents, feature grid, a "How we compare" table. | internal reference |
| `screenshots/features-hero.png` | 2880×1800 | dark (site) | /features hero ("replaces six tools and a marketing agency" claim). | brand deck (after claim check) |
| `screenshots/for-agencies-full.png` | 2880×4694 | dark (site) | /for-agencies. SHOWS AN UNVERIFIED TESTIMONIAL ("Lerato's Agency", 37 clients, 9x, R2.1M MRR, 52% margin); the full page also shows "Partner pricing" (Studio R4,999 / Agency R14,999) that conflicts with the current R9,999 Agency tier and R6,999 partner price. | internal reference only |
| `screenshots/for-agencies-hero.png` | 2880×1800 | dark (site) | /for-agencies. SHOWS AN UNVERIFIED TESTIMONIAL ("Lerato's Agency", 37 clients, 9x, R2.1M MRR, 52% margin); the full page also shows "Partner pricing" (Studio R4,999 / Agency R14,999) that conflicts with the current R9,999 Agency tier and R6,999 partner price. | internal reference only |
| `screenshots/home-full.png` | 2880×13520 | dark (site) | Home, full page. SHOWS UNVERIFIED CLAIMS, a reviews section, and a pricing block whose figures (R399 / R1,439 / R3,199 / R6,399) differ from the facts-file pricing. | internal reference only |
| `screenshots/home-hero.png` | 2880×1800 | dark (site) | Home hero as live. SHOWS UNVERIFIED CLAIMS (200+ businesses, 4.9 rating, Stitch ready, purchase toast). | internal reference only |
| `screenshots/home-hero_clean.png` | 2880×1800 | dark (site) | Home hero, 1440×900 @2x, with the unverified "200+ businesses · 4.9 rating", "Stitch ready" line and purchase toast hidden in the DOM. Still shows a "Trusted by independent brands…" strip at the bottom. | brand deck, investor deck |
| `screenshots/home_clean_mobile.png` | 1170×2532 | dark (site) | Home, mobile 390×844 @3x, same claims hidden. | brand deck, investor deck |
| `screenshots/home_mobile.png` | 1170×2532 | dark (site) | Home, mobile, as live. SHOWS the same UNVERIFIED CLAIMS. | internal reference only |
| `screenshots/pricing-ke.png` | 2880×1800 | dark (site) | /pricing with region KE: Kenyan shilling prices at live FX. Shows FX-converted amounts, NOT the fixed local price points (use `infographics/pricing-regional*`). | internal only: shows FX-converted amounts, not the fixed local price points |
| `screenshots/pricing-ng.png` | 2880×1800 | dark (site) | /pricing with region NG: Naira prices at live FX, Pidgin headline. Shows FX-converted amounts, NOT the fixed local price points (use `infographics/pricing-regional*`). | internal only: shows FX-converted amounts, not the fixed local price points |
| `screenshots/pricing-za-full.png` | 2880×3238 | dark (site) | /pricing full page incl. an ROI estimator with example output figures. | internal reference |
| `screenshots/pricing-za.png` | 2880×1800 | dark (site) | /pricing in ZAR as captured 2026-09-11 (old five-tier ladder incl. Agency R7,999). STALE: internal only; use `infographics/pricing-tiers.png`. | brand deck, proposal, investor deck |

## Screenshot crops (`screenshots/crops/`, 14 files)

| File | Pixels | Ground | What it shows | Suggested use |
|---|---|---|---|---|
| `screenshots/crops/demo-step-01-catalog_chat-desktop.png` | 768×1200 | dark | Chat-screen-only crop of the demo step (source for phone composites). | composites / decks |
| `screenshots/crops/demo-step-01-catalog_chat-mobile.png` | 1038×1800 | dark | Chat-screen-only crop of the demo step (source for phone composites). | composites / decks |
| `screenshots/crops/demo-step-02-added-to-cart_chat-desktop.png` | 768×1200 | dark | Chat-screen-only crop of the demo step (source for phone composites). | composites / decks |
| `screenshots/crops/demo-step-02-added-to-cart_chat-mobile.png` | 1038×1800 | dark | Chat-screen-only crop of the demo step (source for phone composites). | composites / decks |
| `screenshots/crops/demo-step-03-cart_chat-desktop.png` | 768×1200 | dark | Chat-screen-only crop of the demo step (source for phone composites). | composites / decks |
| `screenshots/crops/demo-step-03-cart_chat-mobile.png` | 1068×1800 | dark | Chat-screen-only crop of the demo step (source for phone composites). | composites / decks |
| `screenshots/crops/demo-step-04-checkout-details_chat-desktop.png` | 768×1200 | dark | Chat-screen-only crop of the demo step (source for phone composites). Shows SnapScan in the payment list. | composites / decks |
| `screenshots/crops/demo-step-04-checkout-details_chat-mobile.png` | 1026×1800 | dark | Chat-screen-only crop of the demo step (source for phone composites). Shows SnapScan in the payment list. | composites / decks |
| `screenshots/crops/demo-step-05-payment-method_chat-desktop.png` | 768×1200 | dark | Chat-screen-only crop of the demo step (source for phone composites). Shows SnapScan in the payment list. | composites / decks |
| `screenshots/crops/demo-step-05-payment-method_chat-mobile.png` | 1026×1800 | dark | Chat-screen-only crop of the demo step (source for phone composites). Shows SnapScan in the payment list. | composites / decks |
| `screenshots/crops/demo-step-06-processing_chat-desktop.png` | 768×1200 | dark | Chat-screen-only crop of the demo step (source for phone composites). | composites / decks |
| `screenshots/crops/demo-step-06-processing_chat-mobile.png` | 1026×1800 | dark | Chat-screen-only crop of the demo step (source for phone composites). | composites / decks |
| `screenshots/crops/demo-step-07-confirmation_chat-desktop.png` | 768×1200 | dark | Chat-screen-only crop of the demo step (source for phone composites). | composites / decks |
| `screenshots/crops/demo-step-07-confirmation_chat-mobile.png` | 1026×1800 | dark | Chat-screen-only crop of the demo step (source for phone composites). | composites / decks |

## Device composites (`screenshots/composites/`, 17 files)

| File | Pixels | Ground | What it shows | Suggested use |
|---|---|---|---|---|
| `screenshots/composites/browser-demo.png` | 3200×2080 | transparent | Screenshot in a browser window frame (home = clean hero). RECAPTURE BEFORE USE (5 Oct): home page shows "Start free trial"; demo checkout ends on "Payment received · Yoco card". | brand deck, proposal, investor deck |
| `screenshots/composites/browser-home.png` | 3200×2080 | transparent | Screenshot in a browser window frame (home = clean hero). RECAPTURE BEFORE USE (5 Oct): home page shows "Start free trial"; demo checkout ends on "Payment received · Yoco card". | brand deck, proposal, investor deck |
| `screenshots/composites/browser-pricing.png` | 3200×2080 | transparent | Screenshot in a browser window frame (home = clean hero). RECAPTURE BEFORE USE (5 Oct): home page shows "Start free trial"; demo checkout ends on "Payment received · Yoco card". | brand deck, proposal, investor deck |
| `screenshots/composites/checkout-in-chat-3-phones.png` | 3840×2160 | light (Mist) | 3-phone strip: catalog, cart, confirmation, "Checkout inside the chat". RECAPTURE BEFORE USE (5 Oct): home page shows "Start free trial"; demo checkout ends on "Payment received · Yoco card". | brand deck, proposal, investor deck, business plan |
| `screenshots/composites/checkout-in-chat-3-phones_dark.png` | 3840×2160 | dark | 3-phone strip: catalog, cart, confirmation, "Checkout inside the chat". RECAPTURE BEFORE USE (5 Oct): home page shows "Start free trial"; demo checkout ends on "Payment received · Yoco card". | brand deck, investor deck |
| `screenshots/composites/hero-laptop-phone_night.png` | 3840×2160 | dark | Hero composite: laptop (clean home hero) + phone (order confirmed). RECAPTURE BEFORE USE (5 Oct): home page shows "Start free trial"; demo checkout ends on "Payment received · Yoco card". | brand deck, investor deck cover |
| `screenshots/composites/hero-laptop-phone_white.png` | 3840×2160 | light | Hero composite on white. RECAPTURE BEFORE USE (5 Oct): home page shows "Start free trial"; demo checkout ends on "Payment received · Yoco card". | proposal, business plan cover |
| `screenshots/composites/laptop-demo.png` | 3600×2360 | transparent | Screenshot on a laptop (home = clean hero, footer strip painted out). RECAPTURE BEFORE USE (5 Oct): home page shows "Start free trial"; demo checkout ends on "Payment received · Yoco card". | brand deck, proposal, investor deck |
| `screenshots/composites/laptop-home.png` | 3600×2360 | transparent | Screenshot on a laptop (home = clean hero, footer strip painted out). RECAPTURE BEFORE USE (5 Oct): home page shows "Start free trial"; demo checkout ends on "Payment received · Yoco card". | brand deck, proposal, investor deck |
| `screenshots/composites/laptop-pricing.png` | 3600×2360 | transparent | Screenshot on a laptop (home = clean hero, footer strip painted out). RECAPTURE BEFORE USE (5 Oct): home page shows "Start free trial"; demo checkout ends on "Payment received · Yoco card". | brand deck, proposal, investor deck |
| `screenshots/composites/phone-demo-step-01-catalog.png` | 1120×2120 | transparent | Demo step in a phone frame. RECAPTURE BEFORE USE (5 Oct): home page shows "Start free trial"; demo checkout ends on "Payment received · Yoco card". | brand deck, proposal, investor deck |
| `screenshots/composites/phone-demo-step-02-added-to-cart.png` | 1120×2120 | transparent | Demo step in a phone frame. RECAPTURE BEFORE USE (5 Oct): home page shows "Start free trial"; demo checkout ends on "Payment received · Yoco card". | brand deck, proposal, investor deck |
| `screenshots/composites/phone-demo-step-03-cart.png` | 1120×2120 | transparent | Demo step in a phone frame. RECAPTURE BEFORE USE (5 Oct): home page shows "Start free trial"; demo checkout ends on "Payment received · Yoco card". | brand deck, proposal, investor deck |
| `screenshots/composites/phone-demo-step-04-checkout-details.png` | 1120×2120 | transparent | Demo step in a phone frame. SnapScan visible in the payment list. RECAPTURE BEFORE USE (5 Oct): home page shows "Start free trial"; demo checkout ends on "Payment received · Yoco card". | brand deck, proposal |
| `screenshots/composites/phone-demo-step-05-payment-method.png` | 1120×2120 | transparent | Demo step in a phone frame. SnapScan visible in the payment list. RECAPTURE BEFORE USE (5 Oct): home page shows "Start free trial"; demo checkout ends on "Payment received · Yoco card". | brand deck, proposal |
| `screenshots/composites/phone-demo-step-06-processing.png` | 1120×2120 | transparent | Demo step in a phone frame. RECAPTURE BEFORE USE (5 Oct): home page shows "Start free trial"; demo checkout ends on "Payment received · Yoco card". | brand deck, proposal, investor deck |
| `screenshots/composites/phone-demo-step-07-confirmation.png` | 1120×2120 | transparent | Demo step in a phone frame. RECAPTURE BEFORE USE (5 Oct): home page shows "Start free trial"; demo checkout ends on "Payment received · Yoco card". | brand deck, proposal, investor deck |

## Infographics & workflows (`infographics/`, 48 files)

| File | Pixels | Ground | What it shows | Suggested use |
|---|---|---|---|---|
| `infographics/agency-partner-model.png` | 3840×2160 | light | FluxMuse → agency at the partner wholesale price R6,999/mo (30% off the R9,999 Agency tier; white-label, multi-client, 80 channels, bring your own cloud) → clients at a retail price the partner sets; illustrative 20 × R1,500 = R30,000 − R6,999 = R23,001/mo gross spread. [v5] | proposal (agencies), brand deck, business plan |
| `infographics/agency-partner-model_dark.png` | 3840×2160 | dark (Night) | FluxMuse → agency at the partner wholesale price R6,999/mo (30% off the R9,999 Agency tier; white-label, multi-client, 80 channels, bring your own cloud) → clients at a retail price the partner sets; illustrative 20 × R1,500 = R30,000 − R6,999 = R23,001/mo gross spread. [v5] (dark) | proposal (agencies), brand deck, business plan |
| `infographics/ai-agent-roster.png` | 3840×2160 | light | 4 core agents with roles + 23 specialist Flux agents grouped by name + AI Agent Marketplace. Exists in code; not a live-feature claim (facts §1). | brand deck, investor deck, business plan |
| `infographics/brand-engagement-journey.png` | 3840×2160 | light | Discovery call → demo on your products → set up by hand → go live (lead guarantee starts) → weekly check-ins → keep growing; measures: qualified leads, orders via link, posts made, time saved; lead guarantee stated with its conditions. [v5] | proposal, brand deck |
| `infographics/brand-engagement-journey_square.png` | 2160×2160 | light | Discovery call → demo on your products → set up by hand → go live (lead guarantee starts) → weekly check-ins → keep growing; measures: qualified leads, orders via link, posts made, time saved; lead guarantee stated with its conditions. [v5] (square) | proposal, brand deck |
| `infographics/case-study-template.png` | 3840×2160 | light | Empty case-study template for the first group of businesses, stamped "Template · no data yet / Consent first": [[PLACEHOLDER]] fields, three measures with "Goal, not a result" sub-labels (qualified leads 3 in 30 days; others agreed at kickoff), live features only. [v5] | brand deck, proposal, investor deck, business plan |
| `infographics/case-study-template_dark.png` | 3840×2160 | dark (Night) | Empty case-study template for the first group of businesses, stamped "Template · no data yet / Consent first": [[PLACEHOLDER]] fields, three measures with "Goal, not a result" sub-labels (qualified leads 3 in 30 days; others agreed at kickoff), live features only. [v5] (dark) | brand deck, proposal, investor deck, business plan |
| `infographics/case-study-template_square.png` | 2160×2160 | light | Empty case-study template for the first group of businesses, stamped "Template · no data yet / Consent first": [[PLACEHOLDER]] fields, three measures with "Goal, not a result" sub-labels (qualified leads 3 in 30 days; others agreed at kickoff), live features only. [v5] (square) | brand deck, proposal, investor deck, business plan |
| `infographics/founding-member-offer.png` | 3840×2160 | light | Founding Member: 30% off the first two monthly bills, South African sign-ups, live now, while it lasts (no dates); first-two-bill prices Nano R104 · Micro R202 · Starter R349 · Growth R1,399 · Scale R3,499; Growth bar example; "a discount, not a free period"; agencies see partner pricing. Square works as a social post. [v5] | brand deck, proposal, social |
| `infographics/founding-member-offer_dark.png` | 3840×2160 | dark (Night) | Founding Member: 30% off the first two monthly bills, South African sign-ups, live now, while it lasts (no dates); first-two-bill prices Nano R104 · Micro R202 · Starter R349 · Growth R1,399 · Scale R3,499; Growth bar example; "a discount, not a free period"; agencies see partner pricing. Square works as a social post. [v5] (dark) | brand deck, proposal, social |
| `infographics/founding-member-offer_square.png` | 2160×2160 | light | Founding Member: 30% off the first two monthly bills, South African sign-ups, live now, while it lasts (no dates); first-two-bill prices Nano R104 · Micro R202 · Starter R349 · Growth R1,399 · Scale R3,499; Growth bar example; "a discount, not a free period"; agencies see partner pricing. Square works as a social post. [v5] (square) | brand deck, proposal, social |
| `infographics/how-fluxmuse-works.png` | 3840×2160 | light | Loop: Plan → Create (captions, images, short clips) → Publish (WhatsApp Status, consented broadcasts, TikTok) → Sell (shop link from photos, every order on WhatsApp) → Learn. [v5] | brand kit, brand deck, proposal, investor deck, business plan |
| `infographics/how-fluxmuse-works_dark.png` | 3840×2160 | dark (Night) | Loop: Plan → Create (captions, images, short clips) → Publish (WhatsApp Status, consented broadcasts, TikTok) → Sell (shop link from photos, every order on WhatsApp) → Learn. [v5] (dark) | brand kit, brand deck, proposal, investor deck, business plan |
| `infographics/how-fluxmuse-works_square.png` | 2160×2160 | light | Loop: Plan → Create (captions, images, short clips) → Publish (WhatsApp Status, consented broadcasts, TikTok) → Sell (shop link from photos, every order on WhatsApp) → Learn. [v5] (square) | brand kit, brand deck, proposal, investor deck, business plan |
| `infographics/how-fluxmuse-works_square_dark.png` | 2160×2160 | dark (Night) | Loop: Plan → Create (captions, images, short clips) → Publish (WhatsApp Status, consented broadcasts, TikTok) → Sell (shop link from photos, every order on WhatsApp) → Learn. [v5] (square, dark) | brand kit, brand deck, proposal, investor deck, business plan |
| `infographics/market-entry-sequence.png` | 3840×2160 | light | Market order with mini tile maps: 1 South Africa (open now, Paystack live) → 2 Nigeria, Kenya, Ghana (priced, not yet on sale, no date) → 3 other covered markets (USD, later) → 4 Botswana & Namibia coming soon; everywhere else waitlist only. [v5] | investor deck, business plan, brand deck |
| `infographics/market-entry-sequence_dark.png` | 3840×2160 | dark (Night) | Market order with mini tile maps: 1 South Africa (open now, Paystack live) → 2 Nigeria, Kenya, Ghana (priced, not yet on sale, no date) → 3 other covered markets (USD, later) → 4 Botswana & Namibia coming soon; everywhere else waitlist only. [v5] (dark) | investor deck, business plan, brand deck |
| `infographics/omnichannel-hub.png` | 3840×2160 | light | Hub-and-spoke of 10 nodes: live (WhatsApp Business, Status, shop link, TikTok video, consented broadcasts), being switched on (Facebook Pages, Instagram posts, WhatsApp ads), not available (Instagram DMs, X posting). [v5] | brand deck, proposal, investor deck |
| `infographics/payment-coverage-map.png` | 3840×2160 | light | Tile-grid cartogram coloured by status: South Africa live (Paystack); Nigeria, Kenya, Ghana priced, not yet on sale; other countries "provider contracted, account pending" (pawaPay / Fincra); Botswana, Namibia coming soon. Stats 1 / 3 / 2. [v5] | investor deck, business plan, brand deck |
| `infographics/payment-coverage-map_dark.png` | 3840×2160 | dark (Night) | Tile-grid cartogram coloured by status: South Africa live (Paystack); Nigeria, Kenya, Ghana priced, not yet on sale; other countries "provider contracted, account pending" (pawaPay / Fincra); Botswana, Namibia coming soon. Stats 1 / 3 / 2. [v5] (dark) | investor deck, business plan, brand deck |
| `infographics/payment-coverage-map_square.png` | 2160×2160 | light | Tile-grid cartogram coloured by status: South Africa live (Paystack); Nigeria, Kenya, Ghana priced, not yet on sale; other countries "provider contracted, account pending" (pawaPay / Fincra); Botswana, Namibia coming soon. Stats 1 / 3 / 2. [v5] (square) | investor deck, business plan, brand deck |
| `infographics/payment-coverage-map_square_dark.png` | 2160×2160 | dark (Night) | Tile-grid cartogram coloured by status: South Africa live (Paystack); Nigeria, Kenya, Ghana priced, not yet on sale; other countries "provider contracted, account pending" (pawaPay / Fincra); Botswana, Namibia coming soon. Stats 1 / 3 / 2. [v5] (square, dark) | investor deck, business plan, brand deck |
| `infographics/payment-rails-matrix.png` | 3840×2160 | light | Countries × providers matrix: Paystack live in SA, Yoco/Ozow for FluxMuse subscription billing (SA), pawaPay/Fincra coverage shown as "contracted, account pending"; billing status column (ZAR live; NGN/KES/GHS priced; others closed); BW/NA coming soon. [v5] | investor deck, business plan, proposal |
| `infographics/payment-rails-matrix_dark.png` | 3840×2160 | dark (Night) | Countries × providers matrix: Paystack live in SA, Yoco/Ozow for FluxMuse subscription billing (SA), pawaPay/Fincra coverage shown as "contracted, account pending"; billing status column (ZAR live; NGN/KES/GHS priced; others closed); BW/NA coming soon. [v5] (dark) | investor deck, business plan, proposal |
| `infographics/payment-rails-matrix_portrait.png` | 2160×2700 | light | Countries × providers matrix: Paystack live in SA, Yoco/Ozow for FluxMuse subscription billing (SA), pawaPay/Fincra coverage shown as "contracted, account pending"; billing status column (ZAR live; NGN/KES/GHS priced; others closed); BW/NA coming soon. [v5] (portrait) | investor deck, business plan, proposal |
| `infographics/payment-rails-matrix_portrait_dark.png` | 2160×2700 | dark (Night) | Countries × providers matrix: Paystack live in SA, Yoco/Ozow for FluxMuse subscription billing (SA), pawaPay/Fincra coverage shown as "contracted, account pending"; billing status column (ZAR live; NGN/KES/GHS priced; others closed); BW/NA coming soon. [v5] (portrait, dark) | investor deck, business plan, proposal |
| `infographics/platform-stack.png` | 3840×2160 | light | Six layers with every chip labelled: live (solid), being switched on (dashed: Facebook/Instagram posting, AI Voice beta, Paystack checkout, daily digest, click-to-WhatsApp ads, Shopify/WooCommerce/Takealot sync) or not available (struck: Instagram DMs, X posting). [v5] | investor deck, business plan, brand deck |
| `infographics/platform-stack_dark.png` | 3840×2160 | dark (Night) | Six layers with every chip labelled: live (solid), being switched on (dashed: Facebook/Instagram posting, AI Voice beta, Paystack checkout, daily digest, click-to-WhatsApp ads, Shopify/WooCommerce/Takealot sync) or not available (struck: Instagram DMs, X posting). [v5] (dark) | investor deck, business plan, brand deck |
| `infographics/pricing-regional.png` | 3840×2160 | light | Nano → Agency monthly prices in ZAR (on sale) and NGN, KES, GHS, USD (from tier_regional_prices, labelled "not yet on sale"). Internal / investor use only, never in prospect copy. [v5] | investor deck, business plan |
| `infographics/pricing-regional_dark.png` | 3840×2160 | dark (Night) | Nano → Agency monthly prices in ZAR (on sale) and NGN, KES, GHS, USD (from tier_regional_prices, labelled "not yet on sale"). Internal / investor use only, never in prospect copy. [v5] (dark) | investor deck, business plan |
| `infographics/pricing-regional_square.png` | 2160×2160 | light | Nano → Agency monthly prices in ZAR (on sale) and NGN, KES, GHS, USD (from tier_regional_prices, labelled "not yet on sale"). Internal / investor use only, never in prospect copy. [v5] (square) | investor deck, business plan |
| `infographics/pricing-tiers.png` | 3840×2160 | light | Nine ZAR tiers in three bands (Small: Free, Nano R149, Micro R289; Medium: Starter R499, Growth R1,999, Scale R4,999; Enterprise: Corporate R6,999, Agency R9,999, Custom) with annual price and brands/channels; Founding Member ribbon (30% off first two monthly bills, SA sign-ups, while it lasts); footer: no trials, Free is permanent, partners R6,999 wholesale; no AI credit numbers. [v5] | brand deck, proposal, investor deck, business plan |
| `infographics/problem-solution.png` | 3840×2160 | light | Today (patchwork tools, retainers, lost orders in chats, unanswered after-hours messages) vs With FluxMuse (AI marketing team in WhatsApp; paid plans from R149; photos → catalogue and shop link; answers in the customer's language). [v5] | brand deck, investor deck, business plan |
| `infographics/roadmap-2026-2027.png` | 3840×2160 | light | Indicative roadmap in order, no dates (file name kept). Markets: Now SA open → Next checkout through FluxMuse → Then NG/KE/GH once provider accounts are live → Later other markets (USD) → BW/NA coming soon. Product: live today → Meta permissions → social adapters → business apps → partner programme. [v5] | investor deck, business plan, brand deck |
| `infographics/roadmap-2026-2027_dark.png` | 3840×2160 | dark (Night) | Indicative roadmap in order, no dates (file name kept). Markets: Now SA open → Next checkout through FluxMuse → Then NG/KE/GH once provider accounts are live → Later other markets (USD) → BW/NA coming soon. Product: live today → Meta permissions → social adapters → business apps → partner programme. [v5] (dark) | investor deck, business plan, brand deck |
| `infographics/segment-agency.png` | 3840×2160 | light | Segment hero card: promise, 3 pains → 3 live-feature answers, main plan (Nano R149 / Growth R1,999 / Agency R9,999) and Founding Member price for the first 2 bills (R104 / R1,399) or, for agencies, the partner price R6,999/mo. [v5] | brand deck, proposal |
| `infographics/segment-agency_dark.png` | 3840×2160 | dark (Night) | Segment hero card: promise, 3 pains → 3 live-feature answers, main plan (Nano R149 / Growth R1,999 / Agency R9,999) and Founding Member price for the first 2 bills (R104 / R1,399) or, for agencies, the partner price R6,999/mo. [v5] (dark) | brand deck, proposal |
| `infographics/segment-sme.png` | 3840×2160 | light | Segment hero card: promise, 3 pains → 3 live-feature answers, main plan (Nano R149 / Growth R1,999 / Agency R9,999) and Founding Member price for the first 2 bills (R104 / R1,399) or, for agencies, the partner price R6,999/mo. [v5] | brand deck, proposal |
| `infographics/segment-sme_dark.png` | 3840×2160 | dark (Night) | Segment hero card: promise, 3 pains → 3 live-feature answers, main plan (Nano R149 / Growth R1,999 / Agency R9,999) and Founding Member price for the first 2 bills (R104 / R1,399) or, for agencies, the partner price R6,999/mo. [v5] (dark) | brand deck, proposal |
| `infographics/segment-solo.png` | 3840×2160 | light | Segment hero card: promise, 3 pains → 3 live-feature answers, main plan (Nano R149 / Growth R1,999 / Agency R9,999) and Founding Member price for the first 2 bills (R104 / R1,399) or, for agencies, the partner price R6,999/mo. [v5] | brand deck, proposal |
| `infographics/segment-solo_dark.png` | 3840×2160 | dark (Night) | Segment hero card: promise, 3 pains → 3 live-feature answers, main plan (Nano R149 / Growth R1,999 / Agency R9,999) and Founding Member price for the first 2 bills (R104 / R1,399) or, for agencies, the partner price R6,999/mo. [v5] (dark) | brand deck, proposal |
| `infographics/target-segments.png` | 3840×2160 | light | Three launch segments (Solo: Nano R149; SMEs: Growth R1,999; Agencies: partner R6,999) with who, pain, promise, buying motion; South Africa first, a small first group set up by hand; Corporate/Custom inbound only. [v5] | brand deck, investor deck, business plan |
| `infographics/target-segments_dark.png` | 3840×2160 | dark (Night) | Three launch segments (Solo: Nano R149; SMEs: Growth R1,999; Agencies: partner R6,999) with who, pain, promise, buying motion; South Africa first, a small first group set up by hand; Corporate/Custom inbound only. [v5] (dark) | brand deck, investor deck, business plan |
| `infographics/whatsapp-commerce-flow.png` | 3840×2160 | light | Discover → Chat (assistant replies in the buyer's language) → Catalog (built from photos) → Cart → Pay (Paystack, South Africa, "being switched on") → Order alert (reply SOLD) → Come back (consented broadcasts). Footnote: checkout through FluxMuse not yet tested with real money. [v5] | brand deck, proposal, investor deck |
| `infographics/whatsapp-commerce-flow_dark.png` | 3840×2160 | dark (Night) | Discover → Chat (assistant replies in the buyer's language) → Catalog (built from photos) → Cart → Pay (Paystack, South Africa, "being switched on") → Order alert (reply SOLD) → Come back (consented broadcasts). Footnote: checkout through FluxMuse not yet tested with real money. [v5] (dark) | brand deck, proposal, investor deck |
| `infographics/whatsapp-commerce-flow_square.png` | 2160×2160 | light | Discover → Chat (assistant replies in the buyer's language) → Catalog (built from photos) → Cart → Pay (Paystack, South Africa, "being switched on") → Order alert (reply SOLD) → Come back (consented broadcasts). Footnote: checkout through FluxMuse not yet tested with real money. [v5] (square) | brand deck, proposal, investor deck |
| `infographics/whatsapp-commerce-flow_square_dark.png` | 2160×2160 | dark (Night) | Discover → Chat (assistant replies in the buyer's language) → Catalog (built from photos) → Cart → Pay (Paystack, South Africa, "being switched on") → Order alert (reply SOLD) → Come back (consented broadcasts). Footnote: checkout through FluxMuse not yet tested with real money. [v5] (square, dark) | brand deck, proposal, investor deck |
| `infographics/why-africa-why-now.png` | 3840×2160 | light | Market stat cards from facts §5 with sources and "est.", plus TAM/SAM/SOM planning assumption. | investor deck, business plan |

Total: 132 PNG files.

## Screenshot notes and limitations

- Captured logged out from https://fluxmuse.ai on 2026-09-11 with Chrome over DevTools; cookie consent set to `rejected` (`fluxmuse.cookie.consent`), geo prompt declined (`fm_geo_consent`, `fluxmuse:geo-consent`), region via `fluxmuse:region` / `fm_region`. Desktop 1440×900 @2x, mobile 390×844 @3x.
- **Unverified live-site claims.** Do not use these in brand or investor decks until the claims are verified: `home-hero.png`, `home_mobile.png`, `home-full.png` (200+ businesses, 4.9 rating, "Stitch ready", purchase toast, reviews section, off-facts pricing block), `for-agencies-hero.png`, `for-agencies-full.png` (named-agency testimonial with 9x / R2.1M / 52%, "Partner pricing" R4,999 / R14,999), `features-hero.png` and `features-full.png` ("replaces six tools", comparison table), `pricing-za-full.png` (ROI estimator example figures).
- **Recapture before use (5 Oct 2026):** every product screenshot and composite predates the current offer (trial button, demo Yoco payment, old pricing on `browser-pricing`). Use infographics until they are recaptured with `capture_screenshots.mjs`.
- **Formerly deck-safe home imagery:** `home-hero_clean.png`, `home_clean_mobile.png` and every composite built from them (`browser-home`, `laptop-home`, `hero-laptop-phone_*`). The claims were hidden in the DOM (layout kept), not retouched. `home-hero_clean.png` still has the vague "Trusted by independent brands…" strip at the bottom; the laptop/hero composites paint it out.
- **SnapScan.** The /demo payment step lists "Yoco card, Ozow EFT, SnapScan", and the /demo side cards say "Yoco card, Ozow EFT, SnapScan" and promise recovery "within 30 min". SnapScan must never be shown. Affected: `demo.png`, `demo-full.png`, all desktop `demo-step-*.png` (side cards), steps 04–05 (all sizes, crops and phone composites), `browser-demo.png`, `laptop-demo.png`. `checkout-in-chat-3-phones*` uses steps 01/03/07 and avoids it.
- The demo checkout is fully simulated in the browser (no payment is made). Fictional buyer "Thandi M." and the form's own placeholder number were entered. Order numbers (FLX-ZA-…) are random per run.
- `home-full_mobile.png` was not kept: headless Chrome repeats tiles on very tall mobile pages.
- **NG/KE pricing screenshots are internal only.** `pricing-ng*.png` and `pricing-ke*.png` show the site's live FX-converted amounts at capture time, not the fixed local price points in facts §2. NG/KE/GH are not on sale; `infographics/pricing-regional*` is for internal / investor use only.

## Brand notes

- Source logos are small rasters (light 640×244, dark 497×165, icon 512×512). Lockups upscale them. Ask for vector (SVG/AI) masters before print work.
- `fluxmuse-logo-light.png` has the left stem of the "F" clipped in the source file. Fix upstream in `foundation-zero-point/src/assets/`.
- Contrast (computed): white on Flux Orange is **2.9:1**, below AA even for large text, so use Night/Ink text on orange buttons (6.5:1 / 5.4:1). Flux Orange text on white is also 2.9:1; for orange text on white use the derived deep orange `#C24E00` (4.8:1). Muse spectrum colours are accents only.
- Clear-space and minimum sizes are design recommendations, not existing brand rules.

## Content decisions on infographics (v5, 2026-10-05)

- Source of truth: `08_Prospects/CURRENT_OFFER.md`. Every capability is labelled live (newly launched), being switched on, or not available. Facebook/Instagram auto-posting is never shown as live.
- Payments: Paystack live in South Africa only. pawaPay and Fincra are "contracted, account pending". No graphic says "five rails live" or shows a country count as live coverage. Checkout through FluxMuse is "being switched on".
- Pricing: nine tiers in three bands. Agency R9,999; partner wholesale R6,999. No per-tier AI credit numbers. NGN/KES/GHS/USD prices appear only on `pricing-regional*`, labelled "not yet on sale".
- No free trials anywhere. Free is shown only as a permanent plan, not a trial.
- Founding Member: 30% off the first two monthly bills, SA sign-ups, no dates. Badge and priority support are not claimed until the founder confirms them.
- No pilot, customers or results. The case-study template is empty and stamped as a template; goals are labelled "Goal, not a result". The lead guarantee always appears with its conditions.
- Botswana and Namibia stay dashed "Coming soon".
- Accessibility: orange fills carry Night/Ink text (never white); orange text on white uses Deep Orange #C24E00.
- `agency-partner-model` example: 20 × R1,500 = R30,000; minus R6,999 = R23,001/mo gross spread, labelled illustrative. No fixed margin is quoted.

## Revision v5 (2026-10-05): aligned to CURRENT_OFFER.md

Changed (same filenames): `how-fluxmuse-works` (+ variants), `whatsapp-commerce-flow` (+ variants), `payment-coverage-map` (+ variants), `payment-rails-matrix` (+ variants), `platform-stack` (+ `_dark`), `agency-partner-model` (+ `_dark`), `brand-engagement-journey` (+ `_square`), `pricing-tiers`, `roadmap-2026-2027` (+ `_dark`), `omnichannel-hub`, `problem-solution`, `why-africa-why-now` (SAM wording), `pricing-regional` (+ `_dark`, `_square`), `founding-member-offer` (+ `_dark`, `_square`), `target-segments` (+ `_dark`), `market-entry-sequence` (+ `_dark`), `case-study-template` (+ `_dark`, `_square`), `segment-solo`, `segment-sme`, `segment-agency` (each + `_dark`). Brand: `typography-specimen`, `social-cover-*` (+ `_guides`), `email-signature-banner-*` (trial wording replaced with "Paid plans from R149 a month").

Removed (no pilot exists): `pilot-campaign-framework.png`, `gauteng-pilot.png`, `gauteng-pilot_dark.png`, `founding-member-offer_pilot.png`, `founding-member-offer_pilot_dark.png`.

Earlier revisions v2 to v4 (11 and 12 Sept 2026) are superseded; see git history.

## Rebuilding

```bash
cd docs/go-to-market/_build
node capture_screenshots.mjs                 # live-site screenshots (ONLY=demo | ONLY=clean for subsets)
python composites/prep_screens.py            # needs Pillow
node build_brand.mjs && node build_composites.mjs
node build_infographics.mjs && node build_infographics2.mjs && node build_infographics3.mjs
python write_assets_index.py
```
Each script launches its own headless Chrome (set `CDP_UDD` to a scratch profile dir) and closes it when done. HTML sources are written next to each script (`brand/`, `composites/`, `infographics/`).
