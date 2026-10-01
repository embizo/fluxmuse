# Verification report, prospects 05-08 (2026-09-26)

Method: raw curl + text extraction for websites (raw). Instagram returns no text to curl, so Instagram facts are "summariser-only" (weaker). Verdicts: V verified, R reworded, U unverified (moved to gaps), C contradicted.

## 05 Giftedhands Salon SA
| Fact (original) | Verdict | Check | Change |
|---|---|---|---|
| IG bio 'Luxury Knotless Braids...' Centurion, Fourways, Housecalls | V | summariser-only | kept |
| IG bio links take.app booking page | V | summariser-only; take.app links back to IG (raw) | kept |
| Booking page 'Home of No Pain Braiding', lists braiding, kids, hair wash, scalp detox, nails | R | raw | now lists actual sections (Hair Wash, Braids, Kids Braids, Nails Pricelist, Memberships) |
| Prices R140 to R2,400, braids R450-R2,400 | R | raw | R140 is a nail item; braids R450-R2,400 stated separately |
| Zwartkop (0157) address and "booking through Take App" | R | raw (address in page description) | address kept as Zwartkop only; Take App clause dropped |
| Directory: mobile stylists Pretoria, Centurion, Midrand; call/WhatsApp to book | R | raw | description says Pretoria and Centurion; Midrand is in its areas list |
| Directory review system: communication, quality, punctuality, pricing | V | raw | "time (was the person on time)" |
| Facebook page and Threads account | U | Facebook not linked anywhere raw; Threads only via IG summariser | removed to gaps; replaced by IG posts dated 22-26 Sept 2026 (summariser-only) |
Other: currently trading (IG posts Sept 2026, summariser-only). Route = IG DM; account exists. Take App page description also carries a phone number and address (not used). No owner name used. Blog slug exists. Pains: 2 observed pains still supported.

## 06 The Barbers Chop Shop
| Fact | Verdict | Check | Change |
|---|---|---|---|
| Two shops, Maraisburg and Melville addresses | V | raw | kept |
| About: started with two barbers, now approx. ten staff across both shops | R | raw | page says two barbers, first shop with four barbers, second branch "now employ a passionate team of ten People"; ambiguous whether ten is total, and undated (footer 2024). Reworded literally; opening message no longer quotes growth or headcount |
| Online booking through Fresha | R | raw | Fresha link on homepage/price list plus "Proceed to booking"; wording softened |
| Card payments through Yoco | R | raw | page says "Card payments accepted" and shows a Yoco logo |
| Online shop for perfume + "OG Barber Guide" | C/U | raw | "Shop Perfume" link redirects to scentsperfume.co.za, a separate store; ownership unconfirmed. OG Barber Guide appears nowhere: removed |
| Contact page phone and email | V | raw | kept |
| TikTok/Instagram/Facebook links | V | raw | kept |
| Growth from hard work and faith | dropped | raw | faith/religious framing removed as unnecessary personal content; replaced with verified operating hours |
Other: legal name is from the site footer, not the contact page (fixed). Trading now: IG posts to 26 Sept 2026 (summariser-only), bio "book online". Owners and owner-run status still unconfirmed (gaps). Pain 4 downgraded observed to inferred. Blog slug exists and is relevant.

## 07 The Nail Studio & Beauty Salon
| Fact | Verdict | Check | Change |
|---|---|---|---|
| Address FF 4, Bassonia Shopping Centre | V | raw | kept |
| Services list | V | raw | kept |
| Book by phone/WhatsApp, form, or in person | R | raw | "in person" not on site; now: call or WhatsApp invite, contact form, "book now" button |
| Email published | V | raw | kept |
| Girls Day Out packages | V | raw | kept |
| Facebook and Instagram accounts | V | raw hrefs | Facebook URL now given |
| IG shows phone, website, specials with prices | V | summariser-only | dated Sept 2026; pedicure and gel-toe combo R410 |
| IG laser packages and facials "under RegimA" | R | website raw, IG summariser | RegimA is on the website, not confirmed on IG; reworded |
Other: opening message said Girls Day Out is "on Instagram"; it is on the website; fixed. Trading now: IG posts 15-24 Sept 2026 (summariser-only). Email is Gmail from own site. Blog slug exists.

## 08 LOWKAL SA
| Fact | Verdict | Check | Change |
|---|---|---|---|
| "South African streetwear retailer", tagline | R | raw | About page: "independent menswear and lifestyle boutique"; tagline verified |
| Store 256 Sisulu St, hours | V | raw | kept; hours conflict noted (9-6 vs 9-5) |
| Email and phone | V | raw | phone matches footer and Contact page WhatsApp; a second number looks like a placeholder |
| Tops, bottoms, headwear, accessories; nationwide 2-3 days | R | raw | Contact page says 2 to 4 business days; both stated |
| Jeans page R250-R550, availability filter, multiple payment methods | R | raw | prices seen R180-R550, states "up to R550"; filter 87 in stock / 44 out; payment methods not readable, dropped |
| Newsletter signup | V | raw | kept |
| IG bio, Pretoria, shop link, posts through Sept 2026 | V | summariser-only | dated 20-22 Sept |
| Reviews mention quality, fit, delivery | V | raw | kept |
New verified fact (raw): Contact page lists a WhatsApp number (same as footer) and tells customers to WhatsApp for order tracking, sizing, returns, availability. This is stronger fit than earlier believed: attainability raised 3 to 4, opening message updated, contact_source changed to /pages/contact-us. LOWKAL is real, current (2026 footer, Sept posts), independent (per About page), Gauteng. Pain 2 upgraded to observed. Blog slug exists and is relevant. Dipstreet: dipstreet.co.za does not connect (HTTP 000) and WebFetch returned nothing; still unverified, not swapped.

## Validation
All four files pass json.tool; build_prospects.py --check shows no FAIL (only warnings on Instagram wording and contact details, checked above).
