"""Regenerate docs/go-to-market/assets/ASSETS_INDEX.md from the PNGs on disk.
Run with any Python that has Pillow:  python write_assets_index.py
"""
import fnmatch
from pathlib import Path
from PIL import Image

ASSETS = Path(__file__).resolve().parent.parent / 'assets'
BK, BD, PR, INV, BP = 'brand kit', 'brand deck', 'proposal', 'investor deck', 'business plan'
ALL = f'{BK}, {BD}, {PR}, {INV}, {BP}'

# (glob, ground, what it shows, suggested use) — first match wins
RULES = [
    ('brand/fluxmuse-logo-light.png', 'transparent (for light grounds)', 'Official logo, original file from the product repo. Note: the "F" stem is clipped at the left edge in this source raster.', ALL),
    ('brand/fluxmuse-logo-dark.png', 'transparent (for dark grounds)', 'Official logo for dark grounds, original file.', ALL),
    ('brand/fluxmuse-icon.png', 'transparent', 'The "Muse" icon, original 256 px file.', ALL),
    ('brand/fluxmuse-icon-512.png', 'transparent', 'The "Muse" icon, 512 px (public/icon-512.png).', ALL),
    ('brand/apple-touch-icon.png', 'transparent', 'Apple touch icon, original file.', 'web / app'),
    ('brand/fluxmuse-icon-on-night-1024.png', 'dark (Night)', 'Icon centred on Night #0F1419 square.', f'{BK}, app stores, social'),
    ('brand/fluxmuse-icon-on-white-1024.png', 'light (white)', 'Icon centred on white square.', f'{BK}, documents'),
    ('brand/fluxmuse-icon-on-orange-1024.png', 'Flux Orange', 'Icon on Flux Orange square. The icon\'s warm facets blend into the ground; use sparingly.', BK),
    ('brand/fluxmuse-logo-lockup-light-*.png', 'light (white)', 'Logo lockup on white canvas (upscaled from 640 px source).', f'{BK}, {BD}, {PR}'),
    ('brand/fluxmuse-logo-lockup-dark-*.png', 'dark (Night)', 'Logo lockup on Night canvas (upscaled from 497 px source).', f'{BK}, {BD}, {INV}'),
    ('brand/logo-clear-space-minimum-size.png', 'light', 'Clear-space rule (x = wordmark cap height) and minimum sizes (recommendations).', BK),
    ('brand/logo-misuse-donts.png', 'light', 'Logo do\'s and don\'ts: stretch, recolour, low contrast, busy background, rotate, outline.', BK),
    ('brand/colour-palette.png', 'light', 'Palette swatches with names, HEX, RGB, HSL (facts-file tokens) and proportion guide.', BK),
    ('brand/colour-accessibility-pairings.png', 'light', 'WCAG contrast of 12 text/background pairs with AAA/AA/large-only/fail labels (computed).', BK),
    ('brand/typography-specimen.png', 'light', 'Poppins + Inter specimen and slide type scale.', BK),
    ('brand/social-avatar-1080.png', 'dark', 'Social profile avatar (circle-safe).', 'social profiles'),
    ('brand/social-cover-*_guides.png', 'dark', 'Cover with approximate crop / profile-photo zones overlaid. Planning only; do not upload.', BK),
    ('brand/social-cover-1500x500.png', 'dark', 'X / LinkedIn-style cover: logo, "AI Marketing & WhatsApp Commerce for Africa", "Paid plans from R149 a month" chip.', 'social profiles'),
    ('brand/social-cover-1640x624.png', 'dark', 'Facebook page cover, same content.', 'social profiles'),
    ('brand/whatsapp-business-profile-640.png', 'light', 'WhatsApp Business profile image (icon inside the circular crop).', 'WhatsApp Business'),
    ('brand/email-signature-banner-600x150@2x.png', 'light', 'Email signature banner, retina version; display at 600×150.', 'email'),
    ('brand/email-signature-banner-600x150.png', 'light', 'Email signature banner at 1x.', 'email'),

    ('screenshots/home-hero_clean.png', 'dark (site)', 'Home hero, 1440×900 @2x, with the unverified "200+ businesses · 4.9 rating", "Stitch ready" line and purchase toast hidden in the DOM. Still shows a "Trusted by independent brands…" strip at the bottom.', f'{BD}, {INV}'),
    ('screenshots/home_clean_mobile.png', 'dark (site)', 'Home, mobile 390×844 @3x, same claims hidden.', f'{BD}, {INV}'),
    ('screenshots/home-hero.png', 'dark (site)', 'Home hero as live. SHOWS UNVERIFIED CLAIMS (200+ businesses, 4.9 rating, Stitch ready, purchase toast).', 'internal reference only'),
    ('screenshots/home_mobile.png', 'dark (site)', 'Home, mobile, as live. SHOWS the same UNVERIFIED CLAIMS.', 'internal reference only'),
    ('screenshots/home-full.png', 'dark (site)', 'Home, full page. SHOWS UNVERIFIED CLAIMS, a reviews section, and a pricing block whose figures (R399 / R1,439 / R3,199 / R6,399) differ from the facts-file pricing.', 'internal reference only'),
    ('screenshots/features-hero.png', 'dark (site)', '/features hero ("replaces six tools and a marketing agency" claim).', f'{BD} (after claim check)'),
    ('screenshots/features-full.png', 'dark (site)', '/features full page: 4 agents, feature grid, a "How we compare" table.', 'internal reference'),
    ('screenshots/pricing-za.png', 'dark (site)', '/pricing in ZAR as captured 2026-09-11 (old five-tier ladder incl. Agency R7,999). STALE: internal only; use `infographics/pricing-tiers.png`.', f'{BD}, {PR}, {INV}'),
    ('screenshots/pricing-za-full.png', 'dark (site)', '/pricing full page incl. an ROI estimator with example output figures.', 'internal reference'),
    ('screenshots/pricing-ng*.png', 'dark (site)', '/pricing with region NG: Naira prices at live FX, Pidgin headline. Shows FX-converted amounts, NOT the fixed local price points (use `infographics/pricing-regional*`).', 'internal only: shows FX-converted amounts, not the fixed local price points'),
    ('screenshots/pricing-ke*.png', 'dark (site)', '/pricing with region KE: Kenyan shilling prices at live FX. Shows FX-converted amounts, NOT the fixed local price points (use `infographics/pricing-regional*`).', 'internal only: shows FX-converted amounts, not the fixed local price points'),
    ('screenshots/for-agencies-*.png', 'dark (site)', '/for-agencies. SHOWS AN UNVERIFIED TESTIMONIAL ("Lerato\'s Agency", 37 clients, 9x, R2.1M MRR, 52% margin); the full page also shows "Partner pricing" (Studio R4,999 / Agency R14,999) that conflicts with the current R9,999 Agency tier and R6,999 partner price.', 'internal reference only'),
    ('screenshots/demo.png', 'dark (site)', '/demo landing view: WhatsApp demo store catalog plus side cards (mention SnapScan and "within 30 min").', f'{BD}, {PR}'),
    ('screenshots/demo_mobile.png', 'dark (site)', '/demo on mobile 390×844 @3x: page heading and demo store catalog.', f'{BD}, {PR}'),
    ('screenshots/demo-full.png', 'dark (site)', '/demo full page.', 'internal reference'),
    ('screenshots/demo-step-0[45]-*', 'dark (site)', 'WhatsApp checkout step (desktop 1440×900 @2x or mobile 390×844 @3x). The payment list includes SnapScan, which must never be shown.', f'{BD}, {PR}, {INV}'),
    ('screenshots/demo-step-*_mobile.png', 'dark (site)', 'WhatsApp checkout demo step, mobile 390×844 @3x.', f'{BD}, {PR}, {INV}'),
    ('screenshots/demo-step-*.png', 'dark (site)', 'WhatsApp checkout demo step, desktop 1440×900 @2x (side cards mention SnapScan).', f'{BD}, {PR}, {INV}'),
    ('screenshots/crops/demo-step-0[45]-*', 'dark', 'Chat-screen-only crop of the demo step (source for phone composites). Shows SnapScan in the payment list.', 'composites / decks'),
    ('screenshots/crops/*', 'dark', 'Chat-screen-only crop of the demo step (source for phone composites).', 'composites / decks'),

    ('screenshots/composites/browser-*.png', 'transparent', 'Screenshot in a browser window frame (home = clean hero). RECAPTURE BEFORE USE (5 Oct): home page shows "Start free trial"; demo checkout ends on "Payment received · Yoco card".', f'{BD}, {PR}, {INV}'),
    ('screenshots/composites/laptop-*.png', 'transparent', 'Screenshot on a laptop (home = clean hero, footer strip painted out). RECAPTURE BEFORE USE (5 Oct): home page shows "Start free trial"; demo checkout ends on "Payment received · Yoco card".', f'{BD}, {PR}, {INV}'),
    ('screenshots/composites/phone-demo-step-0[45]-*', 'transparent', 'Demo step in a phone frame. SnapScan visible in the payment list. RECAPTURE BEFORE USE (5 Oct): home page shows "Start free trial"; demo checkout ends on "Payment received · Yoco card".', f'{BD}, {PR}'),
    ('screenshots/composites/phone-demo-step-*', 'transparent', 'Demo step in a phone frame. RECAPTURE BEFORE USE (5 Oct): home page shows "Start free trial"; demo checkout ends on "Payment received · Yoco card".', f'{BD}, {PR}, {INV}'),
    ('screenshots/composites/checkout-in-chat-3-phones_dark.png', 'dark', '3-phone strip: catalog, cart, confirmation, "Checkout inside the chat". RECAPTURE BEFORE USE (5 Oct): home page shows "Start free trial"; demo checkout ends on "Payment received · Yoco card".', f'{BD}, {INV}'),
    ('screenshots/composites/checkout-in-chat-3-phones.png', 'light (Mist)', '3-phone strip: catalog, cart, confirmation, "Checkout inside the chat". RECAPTURE BEFORE USE (5 Oct): home page shows "Start free trial"; demo checkout ends on "Payment received · Yoco card".', f'{BD}, {PR}, {INV}, {BP}'),
    ('screenshots/composites/hero-laptop-phone_night.png', 'dark', 'Hero composite: laptop (clean home hero) + phone (order confirmed). RECAPTURE BEFORE USE (5 Oct): home page shows "Start free trial"; demo checkout ends on "Payment received · Yoco card".', f'{BD}, {INV} cover'),
    ('screenshots/composites/hero-laptop-phone_white.png', 'light', 'Hero composite on white. RECAPTURE BEFORE USE (5 Oct): home page shows "Start free trial"; demo checkout ends on "Payment received · Yoco card".', f'{PR}, {BP} cover'),

    ('infographics/how-fluxmuse-works*', None, 'Loop: Plan → Create (captions, images, short clips) → Publish (WhatsApp Status, consented broadcasts, TikTok) → Sell (shop link from photos, every order on WhatsApp) → Learn. [v5]', ALL),
    ('infographics/whatsapp-commerce-flow*', None, 'Discover → Chat (assistant replies in the buyer\'s language) → Catalog (built from photos) → Cart → Pay (Paystack, South Africa, "being switched on") → Order alert (reply SOLD) → Come back (consented broadcasts). Footnote: checkout through FluxMuse not yet tested with real money. [v5]', f'{BD}, {PR}, {INV}'),
    ('infographics/payment-coverage-map*', None, 'Tile-grid cartogram coloured by status: South Africa live (Paystack); Nigeria, Kenya, Ghana priced, not yet on sale; other countries "provider contracted, account pending" (pawaPay / Fincra); Botswana, Namibia coming soon. Stats 1 / 3 / 2. [v5]', f'{INV}, {BP}, {BD}'),
    ('infographics/payment-rails-matrix*', None, 'Countries × providers matrix: Paystack live in SA, Yoco/Ozow for FluxMuse subscription billing (SA), pawaPay/Fincra coverage shown as "contracted, account pending"; billing status column (ZAR live; NGN/KES/GHS priced; others closed); BW/NA coming soon. [v5]', f'{INV}, {BP}, {PR}'),
    ('infographics/platform-stack*', None, 'Six layers with every chip labelled: live (solid), being switched on (dashed: Facebook/Instagram posting, AI Voice beta, Paystack checkout, daily digest, click-to-WhatsApp ads, Shopify/WooCommerce/Takealot sync) or not available (struck: Instagram DMs, X posting). [v5]', f'{INV}, {BP}, {BD}'),
    ('infographics/agency-partner-model*', None, 'FluxMuse → agency at the partner wholesale price R6,999/mo (30% off the R9,999 Agency tier; white-label, multi-client, 80 channels, bring your own cloud) → clients at a retail price the partner sets; illustrative 20 × R1,500 = R30,000 − R6,999 = R23,001/mo gross spread. [v5]', f'{PR} (agencies), {BD}, {BP}'),
    ('infographics/brand-engagement-journey*', 'light', 'Discovery call → demo on your products → set up by hand → go live (lead guarantee starts) → weekly check-ins → keep growing; measures: qualified leads, orders via link, posts made, time saved; lead guarantee stated with its conditions. [v5]', f'{PR}, {BD}'),
    ('infographics/pricing-tiers.png', 'light', 'Nine ZAR tiers in three bands (Small: Free, Nano R149, Micro R289; Medium: Starter R499, Growth R1,999, Scale R4,999; Enterprise: Corporate R6,999, Agency R9,999, Custom) with annual price and brands/channels; Founding Member ribbon (30% off first two monthly bills, SA sign-ups, while it lasts); footer: no trials, Free is permanent, partners R6,999 wholesale; no AI credit numbers. [v5]', f'{BD}, {PR}, {INV}, {BP}'),
    ('infographics/pricing-regional*', None, 'Nano → Agency monthly prices in ZAR (on sale) and NGN, KES, GHS, USD (from tier_regional_prices, labelled "not yet on sale"). Internal / investor use only, never in prospect copy. [v5]', f'{INV}, {BP}'),
    ('infographics/founding-member-offer*', None, 'Founding Member: 30% off the first two monthly bills, South African sign-ups, live now, while it lasts (no dates); first-two-bill prices Nano R104 · Micro R202 · Starter R349 · Growth R1,399 · Scale R3,499; Growth bar example; "a discount, not a free period"; agencies see partner pricing. Square works as a social post. [v5]', f'{BD}, {PR}, social'),
    ('infographics/target-segments*', None, 'Three launch segments (Solo: Nano R149; SMEs: Growth R1,999; Agencies: partner R6,999) with who, pain, promise, buying motion; South Africa first, a small first group set up by hand; Corporate/Custom inbound only. [v5]', f'{BD}, {INV}, {BP}'),
    ('infographics/market-entry-sequence*', None, 'Market order with mini tile maps: 1 South Africa (open now, Paystack live) → 2 Nigeria, Kenya, Ghana (priced, not yet on sale, no date) → 3 other covered markets (USD, later) → 4 Botswana & Namibia coming soon; everywhere else waitlist only. [v5]', f'{INV}, {BP}, {BD}'),
    ('infographics/case-study-template*', None, 'Empty case-study template for the first group of businesses, stamped "Template · no data yet / Consent first": [[PLACEHOLDER]] fields, three measures with "Goal, not a result" sub-labels (qualified leads 3 in 30 days; others agreed at kickoff), live features only. [v5]', f'{BD}, {PR}, {INV}, {BP}'),
    ('infographics/segment-*', None, 'Segment hero card: promise, 3 pains → 3 live-feature answers, main plan (Nano R149 / Growth R1,999 / Agency R9,999) and Founding Member price for the first 2 bills (R104 / R1,399) or, for agencies, the partner price R6,999/mo. [v5]', f'{BD}, {PR}'),
    ('infographics/roadmap-2026-2027*', None, 'Indicative roadmap in order, no dates (file name kept). Markets: Now SA open → Next checkout through FluxMuse → Then NG/KE/GH once provider accounts are live → Later other markets (USD) → BW/NA coming soon. Product: live today → Meta permissions → social adapters → business apps → partner programme. [v5]', f'{INV}, {BP}, {BD}'),
    ('infographics/omnichannel-hub.png', 'light', 'Hub-and-spoke of 10 nodes: live (WhatsApp Business, Status, shop link, TikTok video, consented broadcasts), being switched on (Facebook Pages, Instagram posts, WhatsApp ads), not available (Instagram DMs, X posting). [v5]', f'{BD}, {PR}, {INV}'),
    ('infographics/problem-solution.png', 'light', 'Today (patchwork tools, retainers, lost orders in chats, unanswered after-hours messages) vs With FluxMuse (AI marketing team in WhatsApp; paid plans from R149; photos → catalogue and shop link; answers in the customer\'s language). [v5]', f'{BD}, {INV}, {BP}'),
    ('infographics/why-africa-why-now.png', 'light', 'Market stat cards from facts §5 with sources and "est.", plus TAM/SAM/SOM planning assumption.', f'{INV}, {BP}'),
    ('infographics/ai-agent-roster.png', 'light', '4 core agents with roles + 23 specialist Flux agents grouped by name + AI Agent Marketplace. Exists in code; not a live-feature claim (facts §1).', f'{BD}, {INV}, {BP}'),
]


def describe(rel):
    for pat, ground, what, use in RULES:
        if fnmatch.fnmatch(rel, pat):
            if ground is None:
                ground = 'dark (Night)' if '_dark' in rel else 'light'
            return ground, what, use
    return '?', '(undocumented)', '?'


def variant(rel):
    tags = [t for t in ('square', 'portrait', 'dark', 'mobile') if f'_{t}' in rel]
    return f" ({', '.join(tags)})" if tags and rel.startswith('infographics/') else ''


sections = [('Brand', 'brand'), ('Product screenshots', 'screenshots'), ('Screenshot crops', 'screenshots/crops'),
            ('Device composites', 'screenshots/composites'), ('Infographics & workflows', 'infographics')]
out = ['# FluxMuse asset library', '',
       'Shared visuals for the go-to-market pack. Every fact on an infographic comes from `../08_Prospects/CURRENT_OFFER.md` and `../00_FACTS_AND_ASSUMPTIONS.md` (refreshed 2026-10-05).',
       'Infographics are 1920×1080 CSS px rendered at 2× (3840×2160 files); `_square` = 1080×1080 @2x, `_portrait` = 1080×1350 @2x, `_dark` = Night #0F1419 ground.',
       'Rebuild everything from `../_build/` (see "Rebuilding" below).', '']
total = 0
for title, folder in sections:
    files = sorted(p for p in (ASSETS / folder).glob('*.png'))
    total += len(files)
    out += [f'## {title} (`{folder}/`, {len(files)} files)', '', '| File | Pixels | Ground | What it shows | Suggested use |', '|---|---|---|---|---|']
    for p in files:
        rel = str(p.relative_to(ASSETS))
        w, h = Image.open(p).size
        ground, what, use = describe(rel)
        out.append(f'| `{rel}` | {w}×{h} | {ground} | {what}{variant(rel)} | {use} |')
    out.append('')

out += [f'Total: {total} PNG files.', '',
'## Screenshot notes and limitations', '',
'- Captured logged out from https://fluxmuse.ai on 2026-09-11 with Chrome over DevTools; cookie consent set to `rejected` (`fluxmuse.cookie.consent`), geo prompt declined (`fm_geo_consent`, `fluxmuse:geo-consent`), region via `fluxmuse:region` / `fm_region`. Desktop 1440×900 @2x, mobile 390×844 @3x.',
'- **Unverified live-site claims.** Do not use these in brand or investor decks until the claims are verified: `home-hero.png`, `home_mobile.png`, `home-full.png` (200+ businesses, 4.9 rating, "Stitch ready", purchase toast, reviews section, off-facts pricing block), `for-agencies-hero.png`, `for-agencies-full.png` (named-agency testimonial with 9x / R2.1M / 52%, "Partner pricing" R4,999 / R14,999), `features-hero.png` and `features-full.png` ("replaces six tools", comparison table), `pricing-za-full.png` (ROI estimator example figures).',
'- **Recapture before use (5 Oct 2026):** every product screenshot and composite predates the current offer (trial button, demo Yoco payment, old pricing on `browser-pricing`). Use infographics until they are recaptured with `capture_screenshots.mjs`.',
'- **Formerly deck-safe home imagery:** `home-hero_clean.png`, `home_clean_mobile.png` and every composite built from them (`browser-home`, `laptop-home`, `hero-laptop-phone_*`). The claims were hidden in the DOM (layout kept), not retouched. `home-hero_clean.png` still has the vague "Trusted by independent brands…" strip at the bottom; the laptop/hero composites paint it out.',
'- **SnapScan.** The /demo payment step lists "Yoco card, Ozow EFT, SnapScan", and the /demo side cards say "Yoco card, Ozow EFT, SnapScan" and promise recovery "within 30 min". SnapScan must never be shown. Affected: `demo.png`, `demo-full.png`, all desktop `demo-step-*.png` (side cards), steps 04–05 (all sizes, crops and phone composites), `browser-demo.png`, `laptop-demo.png`. `checkout-in-chat-3-phones*` uses steps 01/03/07 and avoids it.',
'- The demo checkout is fully simulated in the browser (no payment is made). Fictional buyer "Thandi M." and the form\'s own placeholder number were entered. Order numbers (FLX-ZA-…) are random per run.',
'- `home-full_mobile.png` was not kept: headless Chrome repeats tiles on very tall mobile pages.',
'- **NG/KE pricing screenshots are internal only.** `pricing-ng*.png` and `pricing-ke*.png` show the site\'s live FX-converted amounts at capture time, not the fixed local price points in facts §2. NG/KE/GH are not on sale; `infographics/pricing-regional*` is for internal / investor use only.',
'',
'## Brand notes', '',
'- Source logos are small rasters (light 640×244, dark 497×165, icon 512×512). Lockups upscale them. Ask for vector (SVG/AI) masters before print work.',
'- `fluxmuse-logo-light.png` has the left stem of the "F" clipped in the source file. Fix upstream in `foundation-zero-point/src/assets/`.',
'- Contrast (computed): white on Flux Orange is **2.9:1**, below AA even for large text, so use Night/Ink text on orange buttons (6.5:1 / 5.4:1). Flux Orange text on white is also 2.9:1; for orange text on white use the derived deep orange `#C24E00` (4.8:1). Muse spectrum colours are accents only.',
'- Clear-space and minimum sizes are design recommendations, not existing brand rules.',
'',
'## Content decisions on infographics (v5, 2026-10-05)', '',
'- Source of truth: `08_Prospects/CURRENT_OFFER.md`. Every capability is labelled live (newly launched), being switched on, or not available. Facebook/Instagram auto-posting is never shown as live.',
'- Payments: Paystack live in South Africa only. pawaPay and Fincra are "contracted, account pending". No graphic says "five rails live" or shows a country count as live coverage. Checkout through FluxMuse is "being switched on".',
'- Pricing: nine tiers in three bands. Agency R9,999; partner wholesale R6,999. No per-tier AI credit numbers. NGN/KES/GHS/USD prices appear only on `pricing-regional*`, labelled "not yet on sale".',
'- No free trials anywhere. Free is shown only as a permanent plan, not a trial.',
'- Founding Member: 30% off the first two monthly bills, SA sign-ups, no dates. Badge and priority support are not claimed until the founder confirms them.',
'- No pilot, customers or results. The case-study template is empty and stamped as a template; goals are labelled "Goal, not a result". The lead guarantee always appears with its conditions.',
'- Botswana and Namibia stay dashed "Coming soon".',
'- Accessibility: orange fills carry Night/Ink text (never white); orange text on white uses Deep Orange #C24E00.',
'- `agency-partner-model` example: 20 × R1,500 = R30,000; minus R6,999 = R23,001/mo gross spread, labelled illustrative. No fixed margin is quoted.',
'',
'## Revision v5 (2026-10-05): aligned to CURRENT_OFFER.md', '',
'Changed (same filenames): `how-fluxmuse-works` (+ variants), `whatsapp-commerce-flow` (+ variants), `payment-coverage-map` (+ variants), `payment-rails-matrix` (+ variants), `platform-stack` (+ `_dark`), `agency-partner-model` (+ `_dark`), `brand-engagement-journey` (+ `_square`), `pricing-tiers`, `roadmap-2026-2027` (+ `_dark`), `omnichannel-hub`, `problem-solution`, `why-africa-why-now` (SAM wording), `pricing-regional` (+ `_dark`, `_square`), `founding-member-offer` (+ `_dark`, `_square`), `target-segments` (+ `_dark`), `market-entry-sequence` (+ `_dark`), `case-study-template` (+ `_dark`, `_square`), `segment-solo`, `segment-sme`, `segment-agency` (each + `_dark`). Brand: `typography-specimen`, `social-cover-*` (+ `_guides`), `email-signature-banner-*` (trial wording replaced with "Paid plans from R149 a month").',
'',
'Removed (no pilot exists): `pilot-campaign-framework.png`, `gauteng-pilot.png`, `gauteng-pilot_dark.png`, `founding-member-offer_pilot.png`, `founding-member-offer_pilot_dark.png`.',
'',
'Earlier revisions v2 to v4 (11 and 12 Sept 2026) are superseded; see git history.',
'',
'## Rebuilding', '',
'```bash',
'cd docs/go-to-market/_build',
'node capture_screenshots.mjs                 # live-site screenshots (ONLY=demo | ONLY=clean for subsets)',
'python composites/prep_screens.py            # needs Pillow',
'node build_brand.mjs && node build_composites.mjs',
'node build_infographics.mjs && node build_infographics2.mjs && node build_infographics3.mjs',
'python write_assets_index.py',
'```',
'Each script launches its own headless Chrome (set `CDP_UDD` to a scratch profile dir) and closes it when done. HTML sources are written next to each script (`brand/`, `composites/`, `infographics/`).', '']
(ASSETS / 'ASSETS_INDEX.md').write_text('\n'.join(out))
print('wrote', total, 'rows')
