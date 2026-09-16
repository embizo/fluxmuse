# FluxMuse asset library

Shared visuals for the go-to-market pack. Every fact on an infographic comes from `../00_FACTS_AND_ASSUMPTIONS.md`.
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
| `brand/social-cover-1500x500.png` | 1500×500 | dark | X / LinkedIn-style cover: logo, "AI Marketing & WhatsApp Commerce for Africa", trial chip. | social profiles |
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
| `screenshots/demo-step-04-checkout-details.png` | 2880×1800 | dark (site) | WhatsApp checkout step (desktop 1440×900 @2x or mobile 390×844 @3x). The payment list includes SnapScan, which is not one of the 5 secured rails. | brand deck, proposal, investor deck |
| `screenshots/demo-step-04-checkout-details_mobile.png` | 1170×2532 | dark (site) | WhatsApp checkout step (desktop 1440×900 @2x or mobile 390×844 @3x). The payment list includes SnapScan, which is not one of the 5 secured rails. | brand deck, proposal, investor deck |
| `screenshots/demo-step-05-payment-method.png` | 2880×1800 | dark (site) | WhatsApp checkout step (desktop 1440×900 @2x or mobile 390×844 @3x). The payment list includes SnapScan, which is not one of the 5 secured rails. | brand deck, proposal, investor deck |
| `screenshots/demo-step-05-payment-method_mobile.png` | 1170×2532 | dark (site) | WhatsApp checkout step (desktop 1440×900 @2x or mobile 390×844 @3x). The payment list includes SnapScan, which is not one of the 5 secured rails. | brand deck, proposal, investor deck |
| `screenshots/demo-step-06-processing.png` | 2880×1800 | dark (site) | WhatsApp checkout demo step, desktop 1440×900 @2x (side cards mention SnapScan). | brand deck, proposal, investor deck |
| `screenshots/demo-step-06-processing_mobile.png` | 1170×2532 | dark (site) | WhatsApp checkout demo step, mobile 390×844 @3x. | brand deck, proposal, investor deck |
| `screenshots/demo-step-07-confirmation.png` | 2880×1800 | dark (site) | WhatsApp checkout demo step, desktop 1440×900 @2x (side cards mention SnapScan). | brand deck, proposal, investor deck |
| `screenshots/demo-step-07-confirmation_mobile.png` | 1170×2532 | dark (site) | WhatsApp checkout demo step, mobile 390×844 @3x. | brand deck, proposal, investor deck |
| `screenshots/demo.png` | 2880×1800 | dark (site) | /demo landing view: WhatsApp demo store catalog plus side cards (mention SnapScan and "within 30 min"). | brand deck, proposal |
| `screenshots/demo_mobile.png` | 1170×2532 | dark (site) | /demo on mobile 390×844 @3x: page heading and demo store catalog. | brand deck, proposal |
| `screenshots/features-full.png` | 2880×6796 | dark (site) | /features full page: 4 agents, feature grid, a "How we compare" table. | internal reference |
| `screenshots/features-hero.png` | 2880×1800 | dark (site) | /features hero ("replaces six tools and a marketing agency" claim). | brand deck (after claim check) |
| `screenshots/for-agencies-full.png` | 2880×4694 | dark (site) | /for-agencies. SHOWS AN UNVERIFIED TESTIMONIAL ("Lerato's Agency", 37 clients, 9x, R2.1M MRR, 52% margin); the full page also shows "Partner pricing" (Studio R4,999 / Agency R14,999) that conflicts with the R7,999 Agency tier. | internal reference only |
| `screenshots/for-agencies-hero.png` | 2880×1800 | dark (site) | /for-agencies. SHOWS AN UNVERIFIED TESTIMONIAL ("Lerato's Agency", 37 clients, 9x, R2.1M MRR, 52% margin); the full page also shows "Partner pricing" (Studio R4,999 / Agency R14,999) that conflicts with the R7,999 Agency tier. | internal reference only |
| `screenshots/home-full.png` | 2880×13520 | dark (site) | Home, full page. SHOWS UNVERIFIED CLAIMS, a reviews section, and a pricing block whose figures (R399 / R1,439 / R3,199 / R6,399) differ from the facts-file pricing. | internal reference only |
| `screenshots/home-hero.png` | 2880×1800 | dark (site) | Home hero as live. SHOWS UNVERIFIED CLAIMS (200+ businesses, 4.9 rating, Stitch ready, purchase toast). | internal reference only |
| `screenshots/home-hero_clean.png` | 2880×1800 | dark (site) | Home hero, 1440×900 @2x, with the unverified "200+ businesses · 4.9 rating", "Stitch ready" line and purchase toast hidden in the DOM. Still shows a "Trusted by independent brands…" strip at the bottom. | brand deck, investor deck |
| `screenshots/home_clean_mobile.png` | 1170×2532 | dark (site) | Home, mobile 390×844 @3x, same claims hidden. | brand deck, investor deck |
| `screenshots/home_mobile.png` | 1170×2532 | dark (site) | Home, mobile, as live. SHOWS the same UNVERIFIED CLAIMS. | internal reference only |
| `screenshots/pricing-ke.png` | 2880×1800 | dark (site) | /pricing with region KE: Kenyan shilling prices at live FX. Shows FX-converted amounts, NOT the fixed local price points (use `infographics/pricing-regional*`). | internal only: shows FX-converted amounts, not the fixed local price points |
| `screenshots/pricing-ng.png` | 2880×1800 | dark (site) | /pricing with region NG: Naira prices at live FX, Pidgin headline. Shows FX-converted amounts, NOT the fixed local price points (use `infographics/pricing-regional*`). | internal only: shows FX-converted amounts, not the fixed local price points |
| `screenshots/pricing-za-full.png` | 2880×3238 | dark (site) | /pricing full page incl. an ROI estimator with example output figures. | internal reference |
| `screenshots/pricing-za.png` | 2880×1800 | dark (site) | /pricing in ZAR (R499 / R1,999 / R4,999 / R7,999 / Custom). | brand deck, proposal, investor deck |

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
| `screenshots/composites/browser-demo.png` | 3200×2080 | transparent | Screenshot in a browser window frame (home = clean hero). | brand deck, proposal, investor deck |
| `screenshots/composites/browser-home.png` | 3200×2080 | transparent | Screenshot in a browser window frame (home = clean hero). | brand deck, proposal, investor deck |
| `screenshots/composites/browser-pricing.png` | 3200×2080 | transparent | Screenshot in a browser window frame (home = clean hero). | brand deck, proposal, investor deck |
| `screenshots/composites/checkout-in-chat-3-phones.png` | 3840×2160 | light (Mist) | 3-phone strip: catalog, cart, confirmation, "Checkout inside the chat". | brand deck, proposal, investor deck, business plan |
| `screenshots/composites/checkout-in-chat-3-phones_dark.png` | 3840×2160 | dark | 3-phone strip: catalog, cart, confirmation, "Checkout inside the chat". | brand deck, investor deck |
| `screenshots/composites/hero-laptop-phone_night.png` | 3840×2160 | dark | Hero composite: laptop (clean home hero) + phone (order confirmed). | brand deck, investor deck cover |
| `screenshots/composites/hero-laptop-phone_white.png` | 3840×2160 | light | Hero composite on white. | proposal, business plan cover |
| `screenshots/composites/laptop-demo.png` | 3600×2360 | transparent | Screenshot on a laptop (home = clean hero, footer strip painted out). | brand deck, proposal, investor deck |
| `screenshots/composites/laptop-home.png` | 3600×2360 | transparent | Screenshot on a laptop (home = clean hero, footer strip painted out). | brand deck, proposal, investor deck |
| `screenshots/composites/laptop-pricing.png` | 3600×2360 | transparent | Screenshot on a laptop (home = clean hero, footer strip painted out). | brand deck, proposal, investor deck |
| `screenshots/composites/phone-demo-step-01-catalog.png` | 1120×2120 | transparent | Demo step in a phone frame. | brand deck, proposal, investor deck |
| `screenshots/composites/phone-demo-step-02-added-to-cart.png` | 1120×2120 | transparent | Demo step in a phone frame. | brand deck, proposal, investor deck |
| `screenshots/composites/phone-demo-step-03-cart.png` | 1120×2120 | transparent | Demo step in a phone frame. | brand deck, proposal, investor deck |
| `screenshots/composites/phone-demo-step-04-checkout-details.png` | 1120×2120 | transparent | Demo step in a phone frame. SnapScan visible in the payment list. | brand deck, proposal |
| `screenshots/composites/phone-demo-step-05-payment-method.png` | 1120×2120 | transparent | Demo step in a phone frame. SnapScan visible in the payment list. | brand deck, proposal |
| `screenshots/composites/phone-demo-step-06-processing.png` | 1120×2120 | transparent | Demo step in a phone frame. | brand deck, proposal, investor deck |
| `screenshots/composites/phone-demo-step-07-confirmation.png` | 1120×2120 | transparent | Demo step in a phone frame. | brand deck, proposal, investor deck |

## Infographics & workflows (`infographics/`, 53 files)

| File | Pixels | Ground | What it shows | Suggested use |
|---|---|---|---|---|
| `infographics/agency-partner-model.png` | 3840×2160 | light | FluxMuse → agency at the partner wholesale price R5,599/mo (30% off the R7,999 Agency tier; 50 client sub-accounts, full white-label, reseller billing) → clients at a retail price the partner sets; "set your own retail price and keep the spread"; illustrative 20 × R1,500 = R30,000 − R5,599 = R24,401/mo gross spread. [v3] | proposal (agencies), brand deck, business plan |
| `infographics/agency-partner-model_dark.png` | 3840×2160 | dark (Night) | FluxMuse → agency at the partner wholesale price R5,599/mo (30% off the R7,999 Agency tier; 50 client sub-accounts, full white-label, reseller billing) → clients at a retail price the partner sets; "set your own retail price and keep the spread"; illustrative 20 × R1,500 = R30,000 − R5,599 = R24,401/mo gross spread. [v3] (dark) | proposal (agencies), brand deck, business plan |
| `infographics/ai-agent-roster.png` | 3840×2160 | light | 4 core agents with roles + 23 specialist Flux agents grouped by name + AI Agent Marketplace. | brand deck, investor deck, business plan |
| `infographics/brand-engagement-journey.png` | 3840×2160 | light | Discovery call → audit & strategy → setup → pilot campaign (up to 90 days) → report & optimise → convert to a plan on Founding Member terms; KPI chips from the facts-file pilot KPIs; targets labelled as goals; Gauteng pilot to 30 Nov 2026. [v2] | proposal, brand deck |
| `infographics/brand-engagement-journey_square.png` | 2160×2160 | light | Discovery call → audit & strategy → setup → pilot campaign (up to 90 days) → report & optimise → convert to a plan on Founding Member terms; KPI chips from the facts-file pilot KPIs; targets labelled as goals; Gauteng pilot to 30 Nov 2026. [v2] (square) | proposal, brand deck |
| `infographics/case-study-template.png` | 3840×2160 | light | Designed case-study slide for the lead case (Gauteng braiding & hair studio) with visible [[PLACEHOLDER]] fields (brand, area, challenge, set-up, 3 metrics as [[ ]] with "Target (goal)" sub-labels, quote) and a "Pilot data pending, December 2026" stamp. Template only: fill with consented pilot data. [new v2] | brand deck, proposal, investor deck, business plan |
| `infographics/case-study-template_dark.png` | 3840×2160 | dark (Night) | Designed case-study slide for the lead case (Gauteng braiding & hair studio) with visible [[PLACEHOLDER]] fields (brand, area, challenge, set-up, 3 metrics as [[ ]] with "Target (goal)" sub-labels, quote) and a "Pilot data pending, December 2026" stamp. Template only: fill with consented pilot data. [new v2] (dark) | brand deck, proposal, investor deck, business plan |
| `infographics/case-study-template_square.png` | 2160×2160 | light | Designed case-study slide for the lead case (Gauteng braiding & hair studio) with visible [[PLACEHOLDER]] fields (brand, area, challenge, set-up, 3 metrics as [[ ]] with "Target (goal)" sub-labels, quote) and a "Pilot data pending, December 2026" stamp. Template only: fill with consented pilot data. [new v2] (square) | brand deck, proposal, investor deck, business plan |
| `infographics/founding-member-offer.png` | 3840×2160 | light | Founding Member launch offer: 30% off first 2 monthly bills or +2 months free on annual; Founding Member badge + priority support (no duration) on Starter, Growth and Scale, "Agencies: see partner pricing"; Growth example R1,399 × 2 then R1,999; South Africa window 1 Dec 2026 – 31 Jan 2027; on top of the 14-day free trial. Square works as a social post. [v3] | brand deck, proposal, social |
| `infographics/founding-member-offer_dark.png` | 3840×2160 | dark (Night) | Founding Member launch offer: 30% off first 2 monthly bills or +2 months free on annual; Founding Member badge + priority support (no duration) on Starter, Growth and Scale, "Agencies: see partner pricing"; Growth example R1,399 × 2 then R1,999; South Africa window 1 Dec 2026 – 31 Jan 2027; on top of the 14-day free trial. Square works as a social post. [v3] (dark) | brand deck, proposal, social |
| `infographics/founding-member-offer_pilot.png` | 3840×2160 | light | Pilot-brand edition of the Founding Member offer: 50% off for 60 days from 1 Dec 2026 in exchange for a case study and logo permission; badge + priority support (no duration); whole-rand pilot prices for the first 2 monthly bills: Starter R249 · Growth R999 · Scale R2,499 · Agency R3,999; pilot timeline Sept → 30 Nov → 1 Dec 2026 → list price from bill 3. For the 12 Gauteng pilot brands only. [v3] | proposal (pilot brands) |
| `infographics/founding-member-offer_pilot_dark.png` | 3840×2160 | dark (Night) | Pilot-brand edition of the Founding Member offer: 50% off for 60 days from 1 Dec 2026 in exchange for a case study and logo permission; badge + priority support (no duration); whole-rand pilot prices for the first 2 monthly bills: Starter R249 · Growth R999 · Scale R2,499 · Agency R3,999; pilot timeline Sept → 30 Nov → 1 Dec 2026 → list price from bill 3. For the 12 Gauteng pilot brands only. [v3] (dark) | proposal (pilot brands) |
| `infographics/founding-member-offer_square.png` | 2160×2160 | light | Founding Member launch offer: 30% off first 2 monthly bills or +2 months free on annual; Founding Member badge + priority support (no duration) on Starter, Growth and Scale, "Agencies: see partner pricing"; Growth example R1,399 × 2 then R1,999; South Africa window 1 Dec 2026 – 31 Jan 2027; on top of the 14-day free trial. Square works as a social post. [v3] (square) | brand deck, proposal, social |
| `infographics/gauteng-pilot.png` | 3840×2160 | light | Gauteng pilot overview: 12 brands, Sept → 30 Nov 2026; suggested mix 5 solo / 5 SME / 2 agency (archetypes, no brand names); KPI names tracked (no numbers); lead case study braiding & hair studio; results December 2026. [new v2] | investor deck, brand deck, business plan |
| `infographics/gauteng-pilot_dark.png` | 3840×2160 | dark (Night) | Gauteng pilot overview: 12 brands, Sept → 30 Nov 2026; suggested mix 5 solo / 5 SME / 2 agency (archetypes, no brand names); KPI names tracked (no numbers); lead case study braiding & hair studio; results December 2026. [new v2] (dark) | investor deck, brand deck, business plan |
| `infographics/how-fluxmuse-works.png` | 3840×2160 | light | Loop: Plan (Strategist) → Create (Creator) → Publish (Publisher) → Sell (WhatsApp commerce) → Learn (Analyst), labelled hand-offs. | brand kit, brand deck, proposal, investor deck, business plan |
| `infographics/how-fluxmuse-works_dark.png` | 3840×2160 | dark (Night) | Loop: Plan (Strategist) → Create (Creator) → Publish (Publisher) → Sell (WhatsApp commerce) → Learn (Analyst), labelled hand-offs. (dark) | brand kit, brand deck, proposal, investor deck, business plan |
| `infographics/how-fluxmuse-works_square.png` | 2160×2160 | light | Loop: Plan (Strategist) → Create (Creator) → Publish (Publisher) → Sell (WhatsApp commerce) → Learn (Analyst), labelled hand-offs. (square) | brand kit, brand deck, proposal, investor deck, business plan |
| `infographics/how-fluxmuse-works_square_dark.png` | 2160×2160 | dark (Night) | Loop: Plan (Strategist) → Create (Creator) → Publish (Publisher) → Sell (WhatsApp commerce) → Learn (Analyst), labelled hand-offs. (square, dark) | brand kit, brand deck, proposal, investor deck, business plan |
| `infographics/market-entry-sequence.png` | 3840×2160 | light | Market entry order with mini tile maps: 1 South Africa (Gauteng pilot → national, ZAR) → 2 Nigeria, Kenya, Ghana (local currency) → 3 19 other rail-covered countries (USD, self-serve) → 4 Botswana & Namibia coming soon; everywhere else waitlist only (gated). [new v2] | investor deck, business plan, brand deck |
| `infographics/market-entry-sequence_dark.png` | 3840×2160 | dark (Night) | Market entry order with mini tile maps: 1 South Africa (Gauteng pilot → national, ZAR) → 2 Nigeria, Kenya, Ghana (local currency) → 3 19 other rail-covered countries (USD, self-serve) → 4 Botswana & Namibia coming soon; everywhere else waitlist only (gated). [new v2] (dark) | investor deck, business plan, brand deck |
| `infographics/omnichannel-hub.png` | 3840×2160 | light | Hub-and-spoke: FluxMuse AI team with 10 channel nodes; Instagram dashed as in Meta review. | brand deck, proposal, investor deck |
| `infographics/payment-coverage-map.png` | 3840×2160 | light | Africa tile-grid cartogram of the 23 countries coloured by rail count (1–4; ZA the only 4-rail tile) plus Botswana (BW) and Namibia (NA) as dashed "Coming soon" tiles; stat cards 5 live payment rails / 23 countries covered / +2 coming soon / 40+ MNOs; footnote on all rails live Sept 2026 and SS/ZW payouts-only. [v2] | investor deck, business plan, brand deck |
| `infographics/payment-coverage-map_dark.png` | 3840×2160 | dark (Night) | Africa tile-grid cartogram of the 23 countries coloured by rail count (1–4; ZA the only 4-rail tile) plus Botswana (BW) and Namibia (NA) as dashed "Coming soon" tiles; stat cards 5 live payment rails / 23 countries covered / +2 coming soon / 40+ MNOs; footnote on all rails live Sept 2026 and SS/ZW payouts-only. [v2] (dark) | investor deck, business plan, brand deck |
| `infographics/payment-coverage-map_square.png` | 2160×2160 | light | Africa tile-grid cartogram of the 23 countries coloured by rail count (1–4; ZA the only 4-rail tile) plus Botswana (BW) and Namibia (NA) as dashed "Coming soon" tiles; stat cards 5 live payment rails / 23 countries covered / +2 coming soon / 40+ MNOs; footnote on all rails live Sept 2026 and SS/ZW payouts-only. [v2] (square) | investor deck, business plan, brand deck |
| `infographics/payment-coverage-map_square_dark.png` | 2160×2160 | dark (Night) | Africa tile-grid cartogram of the 23 countries coloured by rail count (1–4; ZA the only 4-rail tile) plus Botswana (BW) and Namibia (NA) as dashed "Coming soon" tiles; stat cards 5 live payment rails / 23 countries covered / +2 coming soon / 40+ MNOs; footnote on all rails live Sept 2026 and SS/ZW payouts-only. [v2] (square, dark) | investor deck, business plan, brand deck |
| `infographics/payment-rails-matrix.png` | 3840×2160 | light | 23 countries × 5 rails matrix by region with currency and Billing currency column (ZAR; NGN/KES/GHS; USD for the other 19); all rails live; BW/NA rows "Coming soon · no rail yet" (waitlist); SS/ZW marked payouts only. [v2] | investor deck, business plan, proposal |
| `infographics/payment-rails-matrix_dark.png` | 3840×2160 | dark (Night) | 23 countries × 5 rails matrix by region with currency and Billing currency column (ZAR; NGN/KES/GHS; USD for the other 19); all rails live; BW/NA rows "Coming soon · no rail yet" (waitlist); SS/ZW marked payouts only. [v2] (dark) | investor deck, business plan, proposal |
| `infographics/payment-rails-matrix_portrait.png` | 2160×2700 | light | 23 countries × 5 rails matrix by region with currency and Billing currency column (ZAR; NGN/KES/GHS; USD for the other 19); all rails live; BW/NA rows "Coming soon · no rail yet" (waitlist); SS/ZW marked payouts only. [v2] (portrait) | investor deck, business plan, proposal |
| `infographics/payment-rails-matrix_portrait_dark.png` | 2160×2700 | dark (Night) | 23 countries × 5 rails matrix by region with currency and Billing currency column (ZAR; NGN/KES/GHS; USD for the other 19); all rails live; BW/NA rows "Coming soon · no rail yet" (waitlist); SS/ZW marked payouts only. [v2] (portrait, dark) | investor deck, business plan, proposal |
| `infographics/pilot-campaign-framework.png` | 3840×2160 | light | 30/60/90-day pilot (Gauteng, 12 brands, Sept to 30 Nov 2026): objectives, deliverables, metrics tracked per phase; targets labelled as goals; conversion on Founding Member pilot terms from 1 Dec 2026; results December 2026. [v2] | proposal, brand deck |
| `infographics/platform-stack.png` | 3840×2160 | light | Six-layer platform stack: Channels (Instagram marked in Meta review), AI workforce, Commerce & payments ("5 live rails"), Growth & CRM, Integrations, Trust. [v2] | investor deck, business plan, brand deck |
| `infographics/platform-stack_dark.png` | 3840×2160 | dark (Night) | Six-layer platform stack: Channels (Instagram marked in Meta review), AI workforce, Commerce & payments ("5 live rails"), Growth & CRM, Integrations, Trust. [v2] (dark) | investor deck, business plan, brand deck |
| `infographics/pricing-regional.png` | 3840×2160 | light | Starter/Growth/Scale/Agency monthly prices in ZAR, NGN, KES, GHS and USD (facts §2 fixed price points); notes: annual = 10× monthly, USD in 19 other rail-covered countries, other countries join the waitlist, prices reviewed quarterly. [new v2] | brand deck, proposal, investor deck, business plan |
| `infographics/pricing-regional_dark.png` | 3840×2160 | dark (Night) | Starter/Growth/Scale/Agency monthly prices in ZAR, NGN, KES, GHS and USD (facts §2 fixed price points); notes: annual = 10× monthly, USD in 19 other rail-covered countries, other countries join the waitlist, prices reviewed quarterly. [new v2] (dark) | brand deck, proposal, investor deck, business plan |
| `infographics/pricing-regional_square.png` | 2160×2160 | light | Starter/Growth/Scale/Agency monthly prices in ZAR, NGN, KES, GHS and USD (facts §2 fixed price points); notes: annual = 10× monthly, USD in 19 other rail-covered countries, other countries join the waitlist, prices reviewed quarterly. [new v2] (square) | brand deck, proposal, investor deck, business plan |
| `infographics/pricing-tiers.png` | 3840×2160 | light | Four ZAR tiers (Starter, Growth, Scale, Agency) with monthly/annual price, brands/channels/AI credits, highlights; Founding Member ribbon (30% off first 2 months on Starter, Growth & Scale · annual +2 months free · 60-day window); 14-day free trial, no card; footer "Enterprise: talk to us. Agency partners: R5,599/mo wholesale." [v3] | brand deck, proposal, investor deck, business plan |
| `infographics/problem-solution.png` | 3840×2160 | light | Today (patchwork tools, retainers, payment-link drop-off, no local payment options) vs With FluxMuse ("Plans from R499/mo, 14-day free trial, no card required"). [v2] | brand deck, investor deck, business plan |
| `infographics/roadmap-2026-2027.png` | 3840×2160 | light | Indicative timeline in two lanes, horizon 2026–2028 (file name unchanged). Markets & payments: Sept 2026 pawaPay & Fincra live (all 5 rails) · Gauteng pilot 12 brands Sept–30 Nov 2026 · South Africa launch with the Founding Member window 1 Dec 2026–31 Jan 2027 · 2027 scale South Africa, no new launches · wave 1 in local currency Nigeria Feb 2028, Kenya Apr 2028, Ghana Jun 2028 · rest of rail-covered Africa (19 countries, USD, self-serve) Nov 2028 · Botswana & Namibia coming soon. Product (founder order, facts §1): 1 Meta permissions Q4 2026 → 2 Social adapters → 3 Business app integrations → 4 Flux_Partner programme. Footnote: launch months are milestone-gated in the financial model (v2, base case); dates move with actual revenue. [v4] | investor deck, business plan, brand deck |
| `infographics/roadmap-2026-2027_dark.png` | 3840×2160 | dark (Night) | Indicative timeline in two lanes, horizon 2026–2028 (file name unchanged). Markets & payments: Sept 2026 pawaPay & Fincra live (all 5 rails) · Gauteng pilot 12 brands Sept–30 Nov 2026 · South Africa launch with the Founding Member window 1 Dec 2026–31 Jan 2027 · 2027 scale South Africa, no new launches · wave 1 in local currency Nigeria Feb 2028, Kenya Apr 2028, Ghana Jun 2028 · rest of rail-covered Africa (19 countries, USD, self-serve) Nov 2028 · Botswana & Namibia coming soon. Product (founder order, facts §1): 1 Meta permissions Q4 2026 → 2 Social adapters → 3 Business app integrations → 4 Flux_Partner programme. Footnote: launch months are milestone-gated in the financial model (v2, base case); dates move with actual revenue. [v4] (dark) | investor deck, business plan, brand deck |
| `infographics/segment-agency.png` | 3840×2160 | light | Segment hero card: segment name, promise line, 3 pains → 3 FluxMuse answers, main tier price and, for solo/SME, the Founding Member price for the first 2 monthly bills (R349 / R1,399; SME card also notes Scale R3,499); the agency card shows the ongoing partner price R5,599/mo (30% off the Agency tier) instead. For segment-specific decks and proposals. [v3] | brand deck, proposal |
| `infographics/segment-agency_dark.png` | 3840×2160 | dark (Night) | Segment hero card: segment name, promise line, 3 pains → 3 FluxMuse answers, main tier price and, for solo/SME, the Founding Member price for the first 2 monthly bills (R349 / R1,399; SME card also notes Scale R3,499); the agency card shows the ongoing partner price R5,599/mo (30% off the Agency tier) instead. For segment-specific decks and proposals. [v3] (dark) | brand deck, proposal |
| `infographics/segment-sme.png` | 3840×2160 | light | Segment hero card: segment name, promise line, 3 pains → 3 FluxMuse answers, main tier price and, for solo/SME, the Founding Member price for the first 2 monthly bills (R349 / R1,399; SME card also notes Scale R3,499); the agency card shows the ongoing partner price R5,599/mo (30% off the Agency tier) instead. For segment-specific decks and proposals. [v3] | brand deck, proposal |
| `infographics/segment-sme_dark.png` | 3840×2160 | dark (Night) | Segment hero card: segment name, promise line, 3 pains → 3 FluxMuse answers, main tier price and, for solo/SME, the Founding Member price for the first 2 monthly bills (R349 / R1,399; SME card also notes Scale R3,499); the agency card shows the ongoing partner price R5,599/mo (30% off the Agency tier) instead. For segment-specific decks and proposals. [v3] (dark) | brand deck, proposal |
| `infographics/segment-solo.png` | 3840×2160 | light | Segment hero card: segment name, promise line, 3 pains → 3 FluxMuse answers, main tier price and, for solo/SME, the Founding Member price for the first 2 monthly bills (R349 / R1,399; SME card also notes Scale R3,499); the agency card shows the ongoing partner price R5,599/mo (30% off the Agency tier) instead. For segment-specific decks and proposals. [v3] | brand deck, proposal |
| `infographics/segment-solo_dark.png` | 3840×2160 | dark (Night) | Segment hero card: segment name, promise line, 3 pains → 3 FluxMuse answers, main tier price and, for solo/SME, the Founding Member price for the first 2 monthly bills (R349 / R1,399; SME card also notes Scale R3,499); the agency card shows the ongoing partner price R5,599/mo (30% off the Agency tier) instead. For segment-specific decks and proposals. [v3] (dark) | brand deck, proposal |
| `infographics/target-segments.png` | 3840×2160 | light | Three launch segments (Solo entrepreneurs, SMEs, Agencies) with who, main tier, pain, promise, buying motion (facts §4b); Agencies on the R5,599/mo partner price; South Africa first; Enterprise inbound only. [v3] | brand deck, investor deck, business plan |
| `infographics/target-segments_dark.png` | 3840×2160 | dark (Night) | Three launch segments (Solo entrepreneurs, SMEs, Agencies) with who, main tier, pain, promise, buying motion (facts §4b); Agencies on the R5,599/mo partner price; South Africa first; Enterprise inbound only. [v3] (dark) | brand deck, investor deck, business plan |
| `infographics/whatsapp-commerce-flow.png` | 3840×2160 | light | Discover → Chat → Catalog → Cart → Pay (5 rails) → Confirmed → Loyalty, with abandoned-cart recovery and retargeting loops. Footnote: all five rails live September 2026 (pawaPay & Fincra from 14 Sept). [v2] | brand deck, proposal, investor deck |
| `infographics/whatsapp-commerce-flow_dark.png` | 3840×2160 | dark (Night) | Discover → Chat → Catalog → Cart → Pay (5 rails) → Confirmed → Loyalty, with abandoned-cart recovery and retargeting loops. Footnote: all five rails live September 2026 (pawaPay & Fincra from 14 Sept). [v2] (dark) | brand deck, proposal, investor deck |
| `infographics/whatsapp-commerce-flow_square.png` | 2160×2160 | light | Discover → Chat → Catalog → Cart → Pay (5 rails) → Confirmed → Loyalty, with abandoned-cart recovery and retargeting loops. Footnote: all five rails live September 2026 (pawaPay & Fincra from 14 Sept). [v2] (square) | brand deck, proposal, investor deck |
| `infographics/whatsapp-commerce-flow_square_dark.png` | 2160×2160 | dark (Night) | Discover → Chat → Catalog → Cart → Pay (5 rails) → Confirmed → Loyalty, with abandoned-cart recovery and retargeting loops. Footnote: all five rails live September 2026 (pawaPay & Fincra from 14 Sept). [v2] (square, dark) | brand deck, proposal, investor deck |
| `infographics/why-africa-why-now.png` | 3840×2160 | light | Market stat cards from facts §5 with sources and "est.", plus TAM/SAM/SOM planning assumption. | investor deck, business plan |

Total: 137 PNG files.

## Screenshot notes and limitations

- Captured logged out from https://fluxmuse.ai on 2026-09-11 with Chrome over DevTools; cookie consent set to `rejected` (`fluxmuse.cookie.consent`), geo prompt declined (`fm_geo_consent`, `fluxmuse:geo-consent`), region via `fluxmuse:region` / `fm_region`. Desktop 1440×900 @2x, mobile 390×844 @3x.
- **Unverified live-site claims.** Do not use these in brand or investor decks until the claims are verified: `home-hero.png`, `home_mobile.png`, `home-full.png` (200+ businesses, 4.9 rating, "Stitch ready", purchase toast, reviews section, off-facts pricing block), `for-agencies-hero.png`, `for-agencies-full.png` (named-agency testimonial with 9x / R2.1M / 52%, "Partner pricing" R4,999 / R14,999), `features-hero.png` and `features-full.png` ("replaces six tools", comparison table), `pricing-za-full.png` (ROI estimator example figures).
- **Deck-safe home imagery:** `home-hero_clean.png`, `home_clean_mobile.png` and every composite built from them (`browser-home`, `laptop-home`, `hero-laptop-phone_*`). The claims were hidden in the DOM (layout kept), not retouched. `home-hero_clean.png` still has the vague "Trusted by independent brands…" strip at the bottom; the laptop/hero composites paint it out.
- **SnapScan.** The /demo payment step lists "Yoco card, Ozow EFT, SnapScan", and the /demo side cards say "Yoco card, Ozow EFT, SnapScan" and promise recovery "within 30 min". SnapScan is not one of the 5 secured rails. Affected: `demo.png`, `demo-full.png`, all desktop `demo-step-*.png` (side cards), steps 04–05 (all sizes, crops and phone composites), `browser-demo.png`, `laptop-demo.png`. `checkout-in-chat-3-phones*` uses steps 01/03/07 and avoids it.
- The demo checkout is fully simulated in the browser (no payment is made). Fictional buyer "Thandi M." and the form's own placeholder number were entered. Order numbers (FLX-ZA-…) are random per run.
- `home-full_mobile.png` was not kept: headless Chrome repeats tiles on very tall mobile pages.
- **NG/KE pricing screenshots are internal only.** `pricing-ng*.png` and `pricing-ke*.png` show the site's live FX-converted amounts at capture time, not the fixed local price points (₦/KSh) in facts §2, and will drift. Use `infographics/pricing-regional*` for external NGN/KES/GHS/USD prices.

## Brand notes

- Source logos are small rasters (light 640×244, dark 497×165, icon 512×512). Lockups upscale them. Ask for vector (SVG/AI) masters before print work.
- `fluxmuse-logo-light.png` has the left stem of the "F" clipped in the source file. Fix upstream in `foundation-zero-point/src/assets/`.
- Contrast (computed): white on Flux Orange is **2.9:1**, below AA even for large text, so use Night/Ink text on orange buttons (6.5:1 / 5.4:1). Flux Orange text on white is also 2.9:1; for orange text on white use the derived deep orange `#C24E00` (4.8:1). Muse spectrum colours are accents only.
- Clear-space and minimum sizes are design recommendations, not existing brand rules.

## Content decisions on infographics

- Instagram, TikTok and LinkedIn publishing are never shown as live; Instagram is marked "in Meta review".
- All five rails are shown as live: "All five rails live September 2026 (pawaPay & Fincra from 14 Sept)" (facts §3, §6).
- Botswana and Namibia appear as dashed "Coming soon" tiles/rows, never as live payment markets; headline counts stay 5 rails · 23 countries, "+2 coming soon".
- South Sudan and Zimbabwe are marked Fincra payouts only; sales open once subscription collection is confirmed (gated until then).
- Billing currency: ZAR (South Africa), fixed local NGN/KES/GHS (Nigeria, Kenya, Ghana), USD for the other 19 rail-covered countries. Other countries: waitlist only, never prices or checkout.
- Founding Member (60 days) is the only launch offer shown. Pilot brands get the deepened 50% for 60 days only on `founding-member-offer_pilot*`. Founding Member prices are 30% off list, rounded down to the rand (Starter R349 / Growth R1,399 / Scale R3,499), for the first 2 monthly bills. Founding Member is not shown for Agency: agencies see the permanent partner wholesale price R5,599/mo (30% off R7,999), never presented as a 2-month discount.
- Pilot and case-study graphics carry no results, brand names or logos; KPI targets appear only as "Target (goal)"; "Results: December 2026".
- Enterprise is not a launch target: `pricing-tiers` shows only a small "Enterprise: talk to us" line.
- Accessibility: orange fills carry Night/Ink text (never white); orange text on white uses Deep Orange #C24E00. The rails-matrix check marks are Night on orange.
- Founding Member perks are shown as "Founding Member badge + priority support" with no duration (facts §2: perks duration is a founder decision). Pilot prices are whole rands, no cents.
- The specialist agent count is 23 (the facts-file list), shown as "+ 23 specialist Flux agents". Grouping them into 3 families is for readability only.
- `problem-solution.png` avoids "6 tools" and "R15k+/mo agencies" because neither figure is in the facts file.
- `agency-partner-model` example: 20 × R1,500 = R30,000; minus the R5,599 partner wholesale price = R24,401/mo gross spread (81%), labelled illustrative, before the partner's own costs. No fixed "40–60% margin" is quoted anywhere.
- Roadmap: the Sept 2026 rails go-live, the pilot dates, the SA launch window and "Q4 2026" for Meta permissions are firm dates; the 2028 market launch months (Nigeria Feb, Kenya Apr, Ghana Jun, rest of rail-covered Africa Nov) come straight from the financial model v2 base case and are milestone-gated, so the graphic labels them indicative and says dates move with actual revenue. Product stages 2–4 stay undated.

## Revision v2 (2026-09-11): founder decisions applied

Changed (same filenames): `payment-coverage-map` (+ `_dark`, `_square`, `_square_dark`), `payment-rails-matrix` (+ `_dark`, `_portrait`, `_portrait_dark`), `whatsapp-commerce-flow` (+ `_dark`, `_square`, `_square_dark`), `platform-stack` (+ `_dark`), `roadmap-2026-2027`, `pricing-tiers`, `pilot-campaign-framework`, `brand-engagement-journey` (+ `_square`), `problem-solution`.

Added: `pricing-regional` (+ `_dark`, `_square`), `founding-member-offer` (+ `_dark`, `_square`), `founding-member-offer_pilot` (+ `_dark`), `target-segments` (+ `_dark`), `market-entry-sequence` (+ `_dark`), `gauteng-pilot` (+ `_dark`), `case-study-template` (+ `_dark`, `_square`), `segment-solo`, `segment-sme`, `segment-agency` (each + `_dark`).

Checked, no change needed: `why-africa-why-now`, `agency-partner-model` (+ `_dark`) (claims already labelled est. / illustrative / attributed).

## Revision v3 (2026-09-11): partner wholesale and whole-rand prices

Changed (same filenames): `agency-partner-model` (+ `_dark`): partner wholesale R5,599/mo (30% off R7,999), illustrative 20 × R1,500 = R30,000 − R5,599 = R24,401/mo gross spread, "set your own retail price and keep the spread", 40–60% margin wording removed. `segment-agency` (+ `_dark`): Founding Member band replaced by "Partner price R5,599/mo: 30% off the Agency tier, ongoing"; 40–60% margin promise removed. `segment-solo`, `segment-sme` (each + `_dark`): Founding Member R349 / R1,399 (Scale R3,499) for the first 2 monthly bills. `founding-member-offer` (+ `_dark`, `_square`): "kept for the life of your account" removed; Starter, Growth and Scale only, "Agencies: see partner pricing". `founding-member-offer_pilot` (+ `_dark`): whole-rand pilot prices R249 / R999 / R2,499 / R3,999 (no cents), no perks duration. `target-segments` (+ `_dark`): agency tier shown as partner R5,599/mo, 40–60% margin removed. `pricing-tiers`: Founding Member ribbon limited to Starter, Growth & Scale; footer adds "Agency partners: R5,599/mo wholesale".

## Revision v4 (2026-09-12): roadmap aligned to financial model v2

Changed (same filenames): `roadmap-2026-2027` — horizon extended to 2028 and the expansion wave moved off 2027 onto the milestone-gated launch months in `06_Financial_Model/model_summary.json` (base case): Nigeria Feb 2028, Kenya Apr 2028, Ghana Jun 2028, rest of rail-covered Africa (19 countries, USD, self-serve) Nov 2028. 2027 now shows "Scale South Africa — no new market launches". Footnote added: "Market launch months are milestone-gated in the financial model (v2, base case); dates move with actual revenue." Title reads Roadmap 2026–2028; the file name is kept so embeds do not break.

Added: `roadmap-2026-2027_dark` (dark variant, same content).

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
