# FluxMuse go-to-market pack: facts and assumptions

**Refreshed 2026-10-05.** This is the source of truth for every document in `docs/go-to-market/`,
rewritten to match `08_Prospects/CURRENT_OFFER.md` (prices, policy and capability status as of 1 Oct 2026).
**If this file and `CURRENT_OFFER.md` ever disagree, `CURRENT_OFFER.md` wins.** For voice, allowed claims and the
never-write list, see `08_Flux_Loop/FluxMuse_Taste_Profile.md`.

Anything labelled **FACT** was checked against the live product code (`embizo/foundation-zero-point`), the founder's
confirmed decisions, or the provider's public docs. Anything labelled **ASSUMPTION** is a planning input the founder must
confirm before a document goes to an external party. Placeholders look like `[[LIKE THIS]]`.

What changed since the 11 Sept version: nine tiers in three bands (Agency now R9,999, partner wholesale R6,999); no free
trials; no pilot and no customers; Founding Member live now with no end date; a lead guarantee instead of any refund;
payment rails described as they really are (South Africa live, the rest pending); every capability labelled live, in
setup or not available.

---

## 1. Company and product (FACT)

- Legal entity: **Fluxmuse (Pty) Ltd**, South Africa. A **verified Meta Tech Provider** (business verification and access
  verification, as of Sept 2026).
- **Not VAT-registered.** Prices are the amount charged. No VAT is added and VAT is not mentioned in any copy.
- Product: **FluxMuse**, an AI marketing team and WhatsApp shop for African small businesses. WhatsApp-first, priced in
  rands, multilingual.
- Domain: **fluxmuse.ai** (app and marketing site). Mail: **thabo@fluxmuse.com** is the only address that receives mail.
- Contact: **Thabo Malebadi**, founder, thabo@fluxmuse.com.
- Stack: React/Vite + Supabase (Postgres, Auth, Edge Functions) on Vercel.
- **No free trials.** Every paid plan starts with payment. The Free plan is a permanent plan (free forever, no card), not a
  trial; don't lead with it.

### Meta and platform approvals (FACT)
- Held: pages_show_list, pages_manage_metadata, pages_messaging, whatsapp_business_messaging,
  whatsapp_business_management, public_profile. TikTok video posting is approved.
- **Not approved yet** (never claim as live): pages_manage_posts, pages_read_engagement, instagram_basic,
  instagram_content_publish, instagram_manage_comments, instagram_manage_messages, business_management.

### What is real today (FACT, from CURRENT_OFFER.md §3)

Label every capability with one of these three. Nothing has been run end to end by a real merchant yet, so live features
are "newly launched", never "proven", and no results are quoted.

**Live, newly launched**
- **WhatsApp Concierge:** the business sends product photos on WhatsApp; AI drafts the catalogue entry (name, description,
  price guess); the owner replies YES, NO or an edit.
- **Hosted shop link** (`fluxmuse.ai/s/<name>`): orders arrive as a pre-typed WhatsApp message to the owner's own number.
- **Order alerts and SOLD:** a WhatsApp alert per order; the owner replies SOLD to mark it sold.
- **AI captions and images for posts** (the POST keyword), ready to forward to WhatsApp Status.
- **Short AI video clips** (720p by default) and **voice-note transcription** on WhatsApp.
- **WhatsApp Business setup:** number connection, profile, templates, quick replies, broadcast to **consented** contacts.
- **Answers in the customer's language.**
- **TikTok posting** (video only).

**In setup ("being switched on", never "available")**
- Auto-publishing to Facebook Pages and Instagram (Meta permissions not approved). Until then the value is forwarding to
  WhatsApp Status.
- Daily digest message (needs a Meta-approved template).
- Checkout through FluxMuse (Paystack, South African bank accounts; FluxMuse doesn't hold the money): built, **not yet
  tested end to end with real money**.
- AI Voice (inbound on Growth; inbound and outbound on Scale and above): beta, evaluated together, not a receptionist
  replacement.
- Click-to-WhatsApp ads (FluxLoop): run on FluxMuse's own account first, not offered to businesses yet.
- Sync from Shopify, WooCommerce and Takealot: partly built; don't promise it.

**Not available**
- Instagram DMs and comments, X posting, Nigeria/Kenya/Ghana checkout, and any paid checkout outside South Africa.

### Wider platform (FACT that the code exists; not a sales claim)
The codebase also holds an agent family (Strategist, Creator, Publisher, Analyst and specialist Flux agents), email/SMS
campaign tools, CRM and segmentation features, a workflow builder and integrations. These exist in code but have not been
used by a real business. In external materials, describe only the live list above; mention the rest as roadmap, if at all.

### Roadmap (FACT: founder's agreed order)
1. Meta permissions (Instagram, Pages posting, business_management, ads).
2. Social adapters: Instagram Login, Threads, LinkedIn, X, TikTok (video posting already approved), YouTube, Pinterest.
3. Business app integrations: commerce, CRM, accounting, email/SMS providers.
4. Flux_Partner programme: referral tracking, white-label, partner-managed workspaces.

---

## 2. Pricing (FACT: live `subscription_tiers`, read 2026-09-26; see CURRENT_OFFER.md §1)

ZAR per month. **Annual = 10× monthly** (12 months for the price of 10). No VAT is added.

| Band | Tier | Monthly | Annual | Brands | Channels | Notes |
|---|---|---|---|---|---|---|
| Small | Free | R0 | R0 | 1 | 1 | Permanent plan, not a trial. Don't lead with it. |
| Small | **Nano** | R149 | R1,490 | 1 | 3 | Entry paid plan for side-hustles |
| Small | **Micro** | R289 | R2,890 | 1 | 4 | 1 WhatsApp number |
| Medium | **Starter** | R499 | R4,990 | 1 | 3 | |
| Medium | **Growth** | R1,999 | R19,990 | 3 | 15 | + inbound AI Voice (beta) |
| Medium | **Scale** | R4,999 | R49,990 | 10 | 40 | + inbound and outbound AI Voice (beta) |
| Enterprise | **Corporate** | R6,999 | R69,990 | 25 | 60 | Bring your own cloud (BYOC) |
| Enterprise | **Agency** | R9,999 | R99,990 | unlimited | 80 | BYOC, white-label, multi-client |
| Enterprise | Custom | on request | | | | Sold by consultation |

- **AI credits:** 1 credit is about R1 of real provider cost (chat 1, image 2, 8-second 720p video 7). Allowances changed
  on 24 Sept: **never quote per-tier credit numbers**; point to the pricing page.
- "From R149" (Nano) is the honest entry price for paid plans. Old "from R499" headlines are stale.
- Old prices that must not appear anywhere: Agency R7,999, partner R5,599, Enterprise "from R19,999".

### Local prices for Nigeria, Kenya and Ghana, and USD (priced, not yet on sale)

FACT: these rows exist in `tier_regional_prices` (migrations `20260911190000_market_gate_and_usd_prices.sql` and
`20260918010100_pricing_small_medium_enterprise_bands.sql`), fixed per currency, annual = 10× monthly.
**They are not on sale.** Nigeria, Kenya and Ghana checkout is not available (Fincra and pawaPay accounts pending), and
there is no paid checkout outside South Africa. Use these tables for planning and investor material only, labelled
"priced, not yet on sale". Never put them in a prospect proposal or ad.

| Tier | ZAR / mo | NGN / mo | KES / mo | GHS / mo | USD / mo |
|---|---|---|---|---|---|
| Free | R0 | ₦0 | KSh 0 | GH₵ 0 | $0 |
| Nano | R149 | ₦12,000 | KSh 1,199 | GH₵ 99 | $8 |
| Micro | R289 | ₦24,000 | KSh 2,299 | GH₵ 199 | $16 |
| Starter | R499 | ₦41,000 | KSh 3,999 | GH₵ 339 | $27 |
| Growth | R1,999 | ₦165,000 | KSh 15,999 | GH₵ 1,359 | $109 |
| Scale | R4,999 | ₦413,000 | KSh 39,999 | GH₵ 3,399 | $269 |
| Corporate | R6,999 | ₦579,000 | KSh 56,999 | GH₵ 4,799 | $379 |
| Agency | R9,999 | ₦829,000 | KSh 80,999 | GH₵ 6,799 | $539 |
| Custom | on request | on request | on request | on request | on request |

Review local prices quarterly once sales open, and reprice if FX moves more than ±10%.

### Partner wholesale (FACT, confirmed 2026-10-01)

Partners (agencies and resellers) buy the **Agency tier at 30% off list: R6,999/mo** (list R9,999), then set their own
retail price for their clients and keep the difference. Annual = 10× monthly (R69,990). Founding Member does not stack
with wholesale. Local-currency partner prices: `[[FOUNDER TO CONFIRM]]` (not needed until checkout opens outside SA).

**Illustrative partner economics** (always label "illustrative, not a forecast"): a partner serving 20 clients at a retail
price they set of R1,500/mo bills R30,000/mo, pays FluxMuse R6,999/mo, and keeps a **R23,001/mo gross spread** before their
own costs. Don't quote a fixed margin: it depends on the partner's retail price and costs.

Referral commission for clients a partner sends onto their own plans: `[[FOUNDER DECISION: referral commission %]]`.

### Launch offer: Founding Member (FACT, confirmed 2026-10-01, live now)

- **30% off the first two monthly bills, for South African sign-ups.** A discount, not a free period.
- **No end date is set.** Say "while it lasts" if anything. Never print the old 1 Dec 2026 to 31 Jan 2027 window.
- Example prices for the first two bills (30% off, rounded down to whole rands): Nano R104 · Micro R202 · Starter R349 ·
  Growth R1,399 · Scale R3,499. `[[FOUNDER TO CONFIRM: rounding matches what checkout charges]]`
- Agencies are pointed to the partner wholesale price instead; don't show R6,999 as a launch discount.
- Annual-plan bonus months: not part of the live promotion. Don't offer them.
- Founding Member perks beyond the discount (badge, priority support): `[[FOUNDER TO CONFIRM]]`. Until confirmed, mention
  only the discount.

### Lead guarantee (FACT, confirmed 2026-10-01)

**3 qualified leads in 30 days of go-live.** A qualified lead is a unique WhatsApp number that starts a conversation
through a FluxMuse-tracked entry point (`08_Prospects/Outreach_Playbook.md`). If fewer than 3 arrive in 30 days and the
business held up its side (shared the link, posted at least weekly), FluxMuse extends support at no extra charge until 3
are reached. **Not a refund. There is no money-back guarantee.** Always state the guarantee with its conditions.

### Checkout fees (FACT, confirmed 2026-10-01; use only once checkout is tested)

"Card payments carry Paystack's standard fee (2.9% + R1), deducted before payout; EFT is 2%." No FluxMuse service fee on
top. Don't quote this until FluxMuse checkout has been tested end to end with real money.

### Market gating (FACT)

- **Open for paid sign-up:** South Africa only.
- **Priced but closed:** Nigeria, Kenya, Ghana and the USD markets, until Fincra/pawaPay accounts are live and checkout is
  tested. Visitors there can join a waitlist.
- Botswana and Namibia stay "coming soon". Materials must never offer prices or checkout to closed markets.

---

## 3. Payment rails (FACT, status 2026-10-05)

| Rail | Use | Status |
|---|---|---|
| **Paystack** | Card and EFT in South Africa; the rail behind FluxMuse checkout | **Live in South Africa.** In-chat checkout through FluxMuse is built, not yet tested end to end with real money |
| **Yoco** | Card, for FluxMuse's own subscription billing | Integrated (South Africa) |
| **Ozow** | Instant EFT, for FluxMuse's own subscription billing | Integrated (South Africa) |
| **pawaPay** | Mobile money, for expansion | Contracted, **account pending**; not live |
| **Fincra** | Collections and payouts, for expansion (NG, KE, GH first) | Contracted, **account pending**; not live |

- **Do not present "five rails live" or a country count as live coverage.** Paid checkout works in South Africa only.
- The provider coverage lists (pawaPay's mobile-money markets, Fincra's collection hubs and payout corridors) are the
  expansion opportunity once those accounts go live. Present them as "contracted, pending", clearly labelled.
- Also present in code but **not** part of the payments story: Flutterwave, M-Pesa direct, PayFast, SnapScan, Stitch.
  Never name them.

### Market entry sequence (FACT, founder; timing not fixed)
1. **South Africa:** home market. Opening with a small first group of businesses, set up by hand, then national.
2. **Nigeria, Kenya, Ghana:** first expansion wave, priced in local currency, opening once Fincra/pawaPay accounts are live
   and checkout is tested.
3. **Other markets those providers cover:** self-serve, billed in USD, later.
4. **Botswana and Namibia:** coming soon.

No launch dates are set for 2 to 4. Don't print them; the financial model is being rebuilt and will set its own
milestone-gated assumptions.

---

## 4. Brand system (FACT from product; usage rules are recommendations)

- Logo files: `assets/brand/fluxmuse-logo-light.png` (for light backgrounds), `fluxmuse-logo-dark.png` (for dark
  backgrounds), `fluxmuse-icon.png` (the "Muse": a rainbow low-poly head over a node network).
- Wordmark: "FLUX" in orange, "MUSE" in slate, wide geometric sans, all caps.
- **Primary: Flux Orange `#FF6A00`** (HSL 24 100% 50%), used as `theme_color` and `--primary`.
- **Orange glow `#FF8533`** (HSL 24 100% 60%). **Orange tint `#FFF4EB`** (HSL 24 100% 96%).
- **Slate (wordmark "MUSE") `#37474F`**. **Ink `#20242B`** (HSL 220 15% 15%, light-mode text).
- **Night `#0F1419`** (dark surface / PWA background). **Paper `#FFFFFF`**. **Mist `#F3F4F6`** (HSL 220 15% 96%).
- **Muse spectrum** (from the icon, accent use only, never for body text): Violet `#6A2DC8`, Blue `#1E88E5`, Teal
  `#00A6A6`, Green `#43A047`, Yellow `#FDD835`, Amber `#FFA000`, Red `#E53935`, Magenta `#D81B60`.
- **Accessibility (measured):** white on Flux Orange is only **2.9:1**, which fails WCAG AA even for large text. Use
  **Ink `#20242B` or Night text on Flux Orange**; use **Deep Orange `#C24E00`** for orange text or links on white.
- **Logo files:** the source `fluxmuse-logo-light.png` has the left stroke of the "F" clipped, and the logos are small
  rasters. Vector masters are needed before any print work: `[[COMMISSION VECTOR LOGO]]`.
- **Claims rules for all materials:** FluxMuse has **no paying customers, no pilot cohort, no results, ratings or
  testimonials**. Don't imply any. The honest angle: "we're opening with a small first group of businesses, and we set
  you up by hand." Never write the phrases on the never-write list in `CURRENT_OFFER.md` §5. If the live website still
  shows unverified claims ("200+ businesses", "4.9 rating", a testimonial), don't copy them or use screenshots that show
  them.
- Typography: **Poppins** (headlines) + **Inter** (body/UI). Fallback: Arial.
- Voice: warm, direct, African-first, zero jargon, short sentences. See the Taste Profile.

---

## 4b. Target customers: South Africa first (FACT, founder)

Three launch segments, all in **South Africa first**. Corporate and Custom are taken inbound; no FY1 sales motion for them.

| | **1. Solo and side-hustle** | **2. Small and medium businesses** | **3. Agencies** |
|---|---|---|---|
| Who | Founder-run businesses of 1 to 5 people: beauty and braiding, fashion resellers, home bakers, coaches, informal retailers selling on WhatsApp and social | 5 to 200 staff: retail, restaurants, e-commerce brands, clinics, property, auto, education, professional services | Marketing, digital and social agencies and freelancers managing 5 to 50 small-business clients |
| Main tiers | **Nano R149 / Micro R289**, then Starter R499 | **Starter R499 / Growth R1,999**, then Scale R4,999 | **Agency R9,999** list; **partner wholesale R6,999** |
| Pain | No time or budget for a marketer; DMs answered late; no shop page | Disconnected tools; WhatsApp handled by hand; no clear view of what sells | Margin squeeze; manual reporting; clients asking for WhatsApp selling and AI |
| Promise | "Send photos, get a shop link. Your marketing team lives in WhatsApp." | "Answer every customer, post every week, and see every order on WhatsApp." | "Serve more clients under your own brand, at a partner price, and set your own retail price." |
| Buying motion | Founder-led: demo on their own public catalogue, then a paid plan with Founding Member pricing | Discovery call, demo, proposal; set up by hand | Partner conversation, demo, partner wholesale plan |
| Proof we can show | Verified Meta Tech Provider; a live demo on their own products; the founder sets them up | Same, plus the lead guarantee with its conditions | White-label demo; illustrative spread calculator |

Case studies come later, only from real businesses who give written consent. See `07_Case_Studies/First_Group_Case_Studies.md`.

## 5. Market (ASSUMPTION: cite and verify before external use)

Directional figures for sizing; present them as "est." with the source noted.
- ~44 million MSMEs in Sub-Saharan Africa (IFC/World Bank est.); South Africa ~2.5 to 3 million SMMEs (SEDA/Stats SA);
  Nigeria ~39 million MSMEs (SMEDAN); Kenya ~7.4 million MSMEs (KNBS).
- WhatsApp is the dominant messaging app in SA, NG, KE and GH (>90% of internet users in SA and NG; DataReportal 2025).
- Sub-Saharan Africa accounts for ~70% of global mobile money value (GSMA State of the Industry 2025).

Serviceable market (ASSUMPTION, from the 11 Sept model; the rebuilt model may change these):
- **TAM**: 44M SSA MSMEs.
- **SAM**: ~3.5M digitally active SMBs in the markets the contracted rails are expected to cover, that sell via
  social/WhatsApp and can pay ≥US$25/mo.
- **SOM (5-yr)**: ~0.5% of SAM ≈ 17,500 paying workspaces.

---

## 6. Traction (FACT: none yet)

- **No paying customers, no pilot cohort, no case studies, no results.** There is no "Gauteng pilot".
- What exists: a live, newly launched product (§1), Meta Tech Provider verification, live pricing, Paystack live in South
  Africa, and a first list of 20 South African prospects (`08_Prospects/`).
- Plan: open with a small first group of South African businesses, set up by hand by the founder. Record what happens
  with consent, using `07_Case_Studies/First_Group_Case_Studies.md`. Never present targets as results.
- Team and advisors: `[[TEAM]]`, `[[ADVISORS]]`.

---

## 7. Fundraise

- Round: **Seed, R25M (≈ US$1.35M)** (FACT, founder). Instrument (SAFE vs priced equity) `[[TBC]]`.
- **The R25M must carry FluxMuse to profitability** (founder): the base case reaches EBITDA break-even and positive cash
  flow on this round alone, with no Series A.
- Use of funds (ASSUMPTION, 11 Sept split): Product & engineering 40% (R10.0M), Sales & marketing / partner programme 30%
  (R7.5M), Market expansion (NG, KE, GH) & payments compliance 15% (R3.75M), Operations & working capital 15% (R3.75M).
- **The financial model is being rebuilt** against the nine tiers and the no-pilot, no-trial facts. Decks and the business
  plan must quote the rebuilt `06_Financial_Model/` outputs once they land, not figures from this file or the old model.
