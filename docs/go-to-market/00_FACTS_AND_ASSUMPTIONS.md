# FluxMuse go-to-market pack: facts and assumptions

This is the single source of truth for every document in `docs/go-to-market/`.
Anything labelled **FACT** was checked against the live product code
(`embizo/foundation-zero-point`) or the provider's public docs on 2026-09-11.
Anything labelled **ASSUMPTION** is a planning input the founder must confirm
before a document goes to an external party. Placeholders look like `[[LIKE THIS]]`.

---

## 1. Company and product (FACT)

- Legal entity: **Fluxmuse Pty Ltd** (South Africa). Meta Business Verification: *Verified*. Meta Access Verification: *Verified (Tech Provider)*.
- Product: **FluxMuse**, "AI marketing team and WhatsApp commerce platform built for African SMBs".
- Domain: **fluxmuse.ai** (app and marketing site).
- Positioning line in product: *AI Marketing & WhatsApp Commerce for Africa*.
- Trial: **14-day free trial, no card required**.
- Stack: React/Vite + Supabase (Postgres, Auth, 140+ Edge Functions) on Vercel.

### Meta approvals held (FACT)
pages_show_list, pages_manage_metadata, pages_messaging, whatsapp_business_messaging,
whatsapp_business_management, public_profile.
In App Review pipeline (not yet approved; do **not** claim as live): pages_manage_posts,
pages_read_engagement, instagram_basic, instagram_content_publish,
instagram_manage_comments, instagram_manage_messages, business_management.

### Shipped capability (FACT, from the app's navigation and edge functions)
- **The AI marketing team** (4 core agents): *Strategist* (goal decomposition, budget allocation, ROI forecasting), *Creator* (multilingual copy in Zulu, Pidgin, Swahili, Afrikaans, English and more; image generation), *Publisher* (scheduling, WhatsApp catalog + checkout flows), *Analyst* (RAG memory, cohort analysis, auto-optimisation).
- **Flux agent family** (specialist agents): Flux Content, Create, Design, Ads, Growth, Nurture, Sales, Support, Commerce, Community, Insights, Advisor, Finance, Compliance, Ops, DevOps, Integrate, Onboarding, Partner, Product, Discover, Personal, Agentic. Plus an AI Agent Marketplace.
- **WhatsApp commerce**: WhatsApp Cloud API accounts (Embedded Signup), contacts, templates, WhatsApp Flows, chatbots, short links (wa.me), website chat widget, catalog, cart checkout in chat, orders with status notifications, abandoned-cart recovery.
- **Social**: in-house publisher (Facebook Pages live; Instagram via Facebook Login in review), content library, templates, calendar, bulk upload, Instagram automation, Messenger bot, social metrics.
- **Campaigns & channels**: campaigns with approvals, email marketing (domains, sequences, suppression), SMS broadcasts, USSD handler, A/B testing, landing page builder, link-in-bio.
- **Growth & CRM**: lead scoring, CRM deals, customer segmentation, loyalty programmes, churn-risk scoring, sentiment analysis with escalation, competitor tracking, custom reports.
- **Automation**: workflow builder (Flux Automate), Zapier, public API + API keys.
- **Integrations**: Shopify, WooCommerce, Takealot, HubSpot/CRM sync, accounting sync, Slack.
- **Finance**: campaign credit facilities / instalment plans (Campaign Financing), AI ad procurement.
- **Trust**: POPIA, NDPR and GDPR ready; row-level security on every table; encrypted tokens; audit export; account deletion and data export.
- **Agencies**: white-label, sub-accounts, reseller billing, partner directory; "40–60% reseller margins" (claim on /for-agencies page).

### Roadmap (FACT: founder's agreed order, Sept 2026)
1. Meta permissions (Instagram, Pages posting, business_management, ads).
2. Social adapters: Instagram Login, Threads, LinkedIn, X, TikTok, YouTube, Pinterest.
3. Business app integrations: commerce, CRM, accounting, email/SMS providers.
4. Flux_Partner programme: referral tracking, white-label, partner-managed workspaces.

---

## 2. Pricing (FACT: `supabase/functions/_shared/pricing.ts`, `subscription_tiers`)

Base currency ZAR; other currencies converted at live FX. Annual = 10× monthly (2 months free).

| Tier | Monthly (ZAR) | Annual (ZAR) | ≈ USD/mo* | Brands | Channels | AI credits/mo | Highlights |
|---|---|---|---|---|---|---|---|
| Starter | R499 | R4,990 | $27 | 1 | 3 | 5,000 | Solo founders; community support |
| Growth (most popular) | R1,999 | R19,990 | $108 | 3 | 15 | 25,000 | E-commerce, WhatsApp commerce, USSD, integrations; email support |
| Scale | R4,999 | R49,990 | $270 | 10 | 40 | 100,000 | API access, white-label reports, priority support |
| Agency | R7,999 | R79,990 | $432 | Unlimited | 80 | 500,000 | Full white-label, 50 sub-accounts, reseller billing, dedicated support |
| Enterprise | from R19,999 | custom | from $1,081 | Unlimited | Unlimited | Unlimited | SSO, SLA, dedicated AI, 24×7 |

\*USD at **R18.50 = US$1** (ASSUMPTION for all USD conversions in this pack).

### Local pricing for the first expansion wave (founder decision, 2026-09-11)

Nigeria, Kenya and Ghana are priced in **NGN, KES and GHS** at fixed, rounded price points, set at FX parity with the ZAR price. Mid-market rates in early September 2026: 1 ZAR = ₦82.83 = KSh 8.07 = GH₵ 0.68. Annual = 10× monthly. Review quarterly, and reprice if FX moves more than ±10%.

| Tier | ZAR / mo | NGN / mo | KES / mo | GHS / mo | NGN / yr | KES / yr | GHS / yr |
|---|---|---|---|---|---|---|---|
| Starter | R499 | ₦41,000 | KSh 3,999 | GH₵ 339 | ₦410,000 | KSh 39,990 | GH₵ 3,390 |
| Growth | R1,999 | ₦165,000 | KSh 15,999 | GH₵ 1,359 | ₦1,650,000 | KSh 159,990 | GH₵ 13,590 |
| Scale | R4,999 | ₦413,000 | KSh 39,999 | GH₵ 3,399 | ₦4,130,000 | KSh 399,990 | GH₵ 33,990 |
| Agency | R7,999 | ₦662,000 | KSh 64,499 | GH₵ 5,439 | ₦6,620,000 | KSh 644,990 | GH₵ 54,390 |
| Enterprise | from R19,999 | from ₦1,650,000 | from KSh 161,000 | from GH₵ 13,600 | custom | custom | custom |

### USD pricing for all other rail-covered countries (founder decision, 2026-09-11)

The other **19 rail-covered countries**, i.e. §3's 23 minus ZA/NG/KE/GH (CI, RW, UG, TZ, ZM, CM, SN, BJ, BF, CG, GA, CD, MW, MZ, SL, ET, LS, SS, ZW), are billed in **USD** at parity with ZAR (R18.50 = US$1), rounded. This includes Zambia and Mozambique, which the app currently prices in ZMW/MZN.

| Tier | ZAR / mo | USD / mo | USD / yr |
|---|---|---|---|
| Starter | R499 | $27 | $270 |
| Growth | R1,999 | $109 | $1,090 |
| Scale | R4,999 | $269 | $2,690 |
| Agency | R7,999 | $429 | $4,290 |
| Enterprise | from R19,999 | from $1,099 | custom |

### Partner wholesale pricing (founder decision, 2026-09-11)

**Partners (agencies and resellers in the Flux_Partner programme) buy the Agency tier at 30% off list**, then set their own retail price for their clients and keep the difference. Same inclusions as Agency: full white-label, 50 client sub-accounts, reseller billing, 80 channels, 500,000 AI credits, dedicated support. Annual = 10× monthly. Founding Member discounts don't stack with wholesale pricing.

| | ZAR | NGN | KES | GHS | USD |
|---|---|---|---|---|---|
| Agency list / mo | R7,999 | ₦662,000 | KSh 64,499 | GH₵ 5,439 | $429 |
| **Partner wholesale / mo (−30%)** | **R5,599** | **₦463,000** | **KSh 44,999** | **GH₵ 3,799** | **$299** |
| Partner wholesale / yr | R55,990 | ₦4,630,000 | KSh 449,990 | GH₵ 37,990 | $2,990 |

**Illustrative partner economics** (always label "illustrative"): a partner serving 20 clients at a retail price they set of R1,500/mo bills R30,000/mo, pays FluxMuse R5,599/mo, and keeps a **R24,401/mo gross spread** before their own service costs. Don't quote a fixed "40–60% margin": margin depends on the partner's retail price and costs.

Scope: the 30% applies to the partner's Agency-tier subscription only. Whether clients a partner refers onto their *own* Starter/Growth/Scale subscriptions earn the partner a referral commission is `[[FOUNDER DECISION: referral commission %]]`, and it isn't modelled as a wholesale discount.

### Market gating (founder decision, 2026-09-11)

- **Open for sale:** only the 23 countries where a secured rail can both collect and pay out. Where coverage is payout-only (South Sudan and Zimbabwe via Fincra), confirm with Fincra that subscription collection works before opening sales. Until then, treat them as gated.
- **Gated (waitlist only, no checkout):** every country without a payment or payout rail. That includes **Botswana and Namibia (shown as "coming soon")** and all countries outside Africa. Visitors from gated countries can join a waitlist but can't buy.
- Materials must never offer prices or checkout to gated countries.

### Launch discount: **Founding Member, 60 days** (founder decision, 2026-09-11)

**Decision: Option B, "Founding Member" (60 days).** This is the only launch offer in all materials. Option A is kept below for the record only: don't present it externally. The financial model's discount toggle defaults to B, and A remains as a sensitivity.

| | **Option A: "Launch Sprint" (30 days)** | **Option B: "Founding Member" (60 days), recommended** |
|---|---|---|
| Who qualifies | Sign-ups in the first 30 days of a market launch | Sign-ups in the first 60 days of a market launch |
| Monthly plans | 50% off the first billing month | 30% off the first 2 billing months |
| Annual plans | 1 extra month free (13 for the price of 12) | 2 extra months free (14 for the price of 12) |
| Price after | List price | List price, plus a "Founding Member" badge and priority support |
| Example, Growth | R999.50 for month 1, then R1,999 | R1,399 for months 1–2, then R1,999 |
| Why | Cheap and fast, creates urgency | Gets businesses past month 2, where SMB churn peaks; smaller per-month cut; builds a founding community for referrals and case studies |

**Founding Member price points (30% off, rounded down to whole rands), for the first 2 monthly bills:** Starter R349 · Growth R1,399 · Scale R3,499. **Agency tier:** Founding Member is **not** promoted for Agency. Agencies are pointed to the permanent **partner wholesale price R5,599/mo** instead (see Partner wholesale pricing). Never show R5,599 as a 2-month launch discount.

**Perks duration: `[[FOUNDER DECISION]]`.** Until decided, say "Founding Member badge and priority support" with **no** duration. Never say "for life" or "for the life of your account".

**Pilot price points (50% off, rounded down to whole rands), for the first 2 monthly bills from 1 Dec 2026:** Starter R249 · Growth R999 · Scale R2,499 · Agency R3,999. No cents in any material.

**Pilot brands (12, Gauteng):** Founding Member terms, deepened to 50% off for 60 days, in exchange for a case study and logo permission. The offer converts them in December 2026 when the pilot ends.

**Launch windows:** South Africa, 1 December 2026 to 31 January 2027 (the pilot ends 30 November). Nigeria, Kenya and Ghana: the first 60 days after each country's launch date in the model. USD markets: no dedicated launch window, since they're self-serve. Offer the discount only if the model shows it doesn't break R25M profitability.

Product gap: the live app charges ZAR × the day's FX rate (unrounded) and has **no Ghana/GHS region** yet; Ghanaian visitors currently see USD. Until the app adds fixed local prices, proposals and decks should quote this table and say "billed in local currency".

In the financial model, NG/KE/GH revenue is booked at these local prices converted back to ZAR at the rates above. Also run a downside sensitivity with ZAR 15% stronger than NGN/KES/GHS, since that's the main currency risk for these markets.

Note for founder: the ChatPion-era `docs/agency_provisioning.md` refers to an Agency tier at **$346/mo**; the live checkout charges **R7,999**. This pack uses the live checkout price. Enterprise shows "custom" on the pricing page but checkout charges R19,999; this pack says "from R19,999".

---

## 3. Payment rails secured (FACT: provider docs, 2026-09-11)

Five rails secured: **Yoco, Ozow, Paystack** (live in product) + **pawaPay, Fincra** (contracted; **go-live week of 14 September 2026**, founder). In materials dated after go-live, present all five as live. Until go-live is confirmed, say "live September 2026".

| Rail | Type | Countries |
|---|---|---|
| **Yoco** | Card acquiring, tap-to-pay | South Africa |
| **Ozow** | Instant EFT / pay-by-bank | South Africa |
| **Paystack** | Cards, bank transfer, USSD, mobile money | Nigeria, Ghana, South Africa, Kenya, Côte d'Ivoire, Rwanda |
| **pawaPay** | Mobile money collections + payouts, 40+ MNOs | Benin, Burkina Faso, Cameroon, Côte d'Ivoire, DR Congo, Ethiopia, Gabon, Ghana, Kenya, Lesotho, Malawi, Mozambique, Nigeria, Republic of the Congo, Rwanda, Senegal, Sierra Leone, Tanzania, Uganda, Zambia (20) |
| **Fincra** | Collections (virtual accounts, cards, bank, mobile money) + payouts; global corridors | Collections hubs: Nigeria, Ghana, Kenya, Uganda, South Africa (+ UK, Canada, EU/US virtual accounts). African payouts: Benin, Burkina Faso, Côte d'Ivoire, Senegal (XOF); Cameroon, Gabon, Rep. of Congo (XAF); Ghana; Kenya; Rwanda; Uganda; Tanzania; Zambia; South Sudan; DR Congo, Nigeria, Zimbabwe (USD). Payouts to 100+ countries globally. |

### Combined African coverage: 23 countries

| # | Country | ISO | Currency | Rails |
|---|---|---|---|---|
| 1 | South Africa | ZA | ZAR | Yoco, Ozow, Paystack, Fincra |
| 2 | Nigeria | NG | NGN | Paystack, pawaPay, Fincra |
| 3 | Ghana | GH | GHS | Paystack, pawaPay, Fincra |
| 4 | Kenya | KE | KES | Paystack, pawaPay, Fincra |
| 5 | Côte d'Ivoire | CI | XOF | Paystack, pawaPay, Fincra |
| 6 | Rwanda | RW | RWF | Paystack, pawaPay, Fincra |
| 7 | Uganda | UG | UGX | pawaPay, Fincra |
| 8 | Tanzania | TZ | TZS | pawaPay, Fincra |
| 9 | Zambia | ZM | ZMW | pawaPay, Fincra |
| 10 | Cameroon | CM | XAF | pawaPay, Fincra |
| 11 | Senegal | SN | XOF | pawaPay, Fincra |
| 12 | Benin | BJ | XOF | pawaPay, Fincra |
| 13 | Burkina Faso | BF | XOF | pawaPay, Fincra |
| 14 | Republic of the Congo | CG | XAF | pawaPay, Fincra |
| 15 | Gabon | GA | XAF | pawaPay, Fincra |
| 16 | DR Congo | CD | CDF/USD | pawaPay, Fincra |
| 17 | Malawi | MW | MWK | pawaPay |
| 18 | Mozambique | MZ | MZN | pawaPay |
| 19 | Sierra Leone | SL | SLE | pawaPay |
| 20 | Ethiopia | ET | ETB | pawaPay |
| 21 | Lesotho | LS | LSL | pawaPay |
| 22 | South Sudan | SS | SSP | Fincra (payouts) |
| 23 | Zimbabwe | ZW | USD | Fincra (payouts) |

### Market entry sequence (FACT, founder, 2026-09-11)
1. **South Africa**: home market; Gauteng pilot, then national.
2. **Nigeria, Kenya, Ghana**: the first expansion wave, all three covered by Paystack, pawaPay and Fincra.
3. **Rest of the rail-covered countries**: Côte d'Ivoire, Rwanda, Uganda, Tanzania, Zambia, francophone West and Central Africa, and the remaining pawaPay markets. These are served self-serve first, and there's no local team until traction justifies one.
4. **Botswana and Namibia**: coming soon, once a rail covers them.

Every deck, plan and model must use this order. Payment rails are live everywhere, so a sales push in the rest of the countries is opportunistic self-serve, not a planned launch.

Regional roll-up: **Southern Africa** ZA, ZM, MW, MZ, LS, ZW · **East Africa** KE, UG, TZ, RW, ET, SS · **West Africa** NG, GH, CI, SN, BJ, BF, SL · **Central Africa** CM, CG, GA, CD.

**Coming soon: Botswana (BW, BWP) and Namibia (NA, NAD).** They're in the app's region picker and stay in all materials, labelled **"coming soon"** (founder, 2026-09-11). None of the five secured rails covers them yet, so never show them as live payment markets. Headline counts stay "5 rails · 23 countries live", with "+2 coming soon (Botswana, Namibia)".

Also present in code but **not** part of the "secured rails" story: Flutterwave, M-Pesa direct (Daraja), PayFast. Mention only if the founder confirms they're contracted.

---

## 4. Brand system (FACT from product; usage rules are recommendations)

- Logo files: `assets/brand/fluxmuse-logo-light.png` (for light backgrounds), `fluxmuse-logo-dark.png` (for dark backgrounds), `fluxmuse-icon.png` (the "Muse": a rainbow low-poly head over a node network).
- Wordmark: "FLUX" in orange, "MUSE" in slate, wide geometric sans, all caps.
- **Primary: Flux Orange `#FF6A00`** (HSL 24 100% 50%), used as `theme_color` and `--primary`.
- **Orange glow `#FF8533`** (HSL 24 100% 60%). **Orange tint `#FFF4EB`** (HSL 24 100% 96%).
- **Slate (wordmark "MUSE") `#37474F`**. **Ink `#20242B`** (HSL 220 15% 15%, light-mode text).
- **Night `#0F1419`** (dark surface / PWA background). **Paper `#FFFFFF`**. **Mist `#F3F4F6`** (HSL 220 15% 96%).
- **Muse spectrum** (from the icon, accent use only, never for body text): Violet `#6A2DC8`, Blue `#1E88E5`, Teal `#00A6A6`, Green `#43A047`, Yellow `#FDD835`, Amber `#FFA000`, Red `#E53935`, Magenta `#D81B60`.
- **Accessibility (measured):** white on Flux Orange is only **2.9:1**, which fails WCAG AA even for large text. Rules: use **Ink `#20242B` or Night text on Flux Orange** buttons and fills; use **Deep Orange `#C24E00`** for orange text or links on white (passes AA); keep Flux Orange for fills, accents, icons and large display type on Night.
- **Logo files:** the source `fluxmuse-logo-light.png` has the left stroke of the "F" clipped, and the logos are small rasters (640 px / 497 px). Vector (SVG/EPS) master files are needed before any print work: `[[COMMISSION VECTOR LOGO]]`.
- **Claims rules for all materials:** no customer counts, ratings, testimonials or results until pilot data exists with consent. No SnapScan, Stitch, Flutterwave, PayFast or M-Pesa-direct in the rails story. The live website currently shows unverified claims ("200+ businesses", "4.9 rating", an agency testimonial) and mismatched home/agency prices; don't copy them, and don't use screenshots that show them.
- Typography: product uses the system UI stack. Recommended brand pair: **Poppins** (headlines, echoes the geometric wordmark) + **Inter** (body/UI). Fallback: Arial.
- Voice: warm, direct, African-first, zero jargon. "Receipts and revenue, not jargon." Multilingual by default.

---

## 4b. Target customers: South Africa first (founder decision, 2026-09-11)

Three launch segments, all in **South Africa first** (Gauteng pilot, then national), before the Nigeria/Kenya/Ghana wave. **Enterprise is not a launch target**: take inbound enterprise deals, but don't build sales motions, decks or hires for enterprise in FY1.

| | **1. Solo entrepreneurs** | **2. SMEs (small to medium-sized enterprises)** | **3. Agencies** |
|---|---|---|---|
| Who | Founder-run businesses of 1–5 people: side hustles, beauty and braiding, fashion resellers, home bakers, coaches, informal retailers selling on Instagram/Facebook/WhatsApp | 5–200 staff: retail, restaurants and franchises, e-commerce brands, clinics, property, auto dealers, education, professional services | Marketing, digital and social media agencies and freelancers managing 5–50 SMB clients |
| Main tier | **Starter R499** → Growth | **Growth R1,999** → Scale R4,999 | **Agency R7,999** (white-label, 50 sub-accounts) |
| Pain | No time or budget for a marketer; posts inconsistently; loses sales in WhatsApp DMs; payment links drop off | 6+ disconnected tools; agency retainers of R15k+/mo; no attribution from social to sales; WhatsApp handled manually by staff | Margin squeeze; manual reporting; too many tools per client; clients want WhatsApp commerce and AI |
| Promise | "Your AI marketing team for R499/mo, and you sell right inside WhatsApp" | "Replace the tool stack, sell and get paid in chat, see what drives revenue" | "Serve more clients with the same team, under your brand, at a partner price of R5,599/mo, and set your own retail price" |
| Buying motion | Self-serve: 14-day trial → Founding Member offer | Trial + guided onboarding call; proposal for multi-brand/Scale | Partner programme: demo → pilot client → Agency tier, reseller billing |
| Acquisition channels | Meta/TikTok ads, WhatsApp short links, creators and influencers, community markets, Link-in-bio | Content/SEO, webinars, chamber and business networks (e.g. Gauteng SMME hubs), bank/fintech partnerships, referrals from pilot brands | Direct outreach, agency communities, partner directory, co-marketing, referral fees |
| Key proof | Pilot case studies from solo-run brands | Pilot KPIs: conversations, orders, GMV, hours saved | White-label demo; margin calculator |

How this applies to the documents:
- **Brand pitch deck**: one core deck with a segment slide for each of the three. Speaker notes explain which slides to swap for each audience.
- **Proposal templates**: one template per segment (Solo, SME, Agency partner), plus a brand/campaign proposal for SMEs running a specific campaign.
- **Financial model**: FY1 acquisition is 100% South Africa across these three segments, with the channel split self-serve (solo + SME) vs agency partner channel. Enterprise revenue in FY1 is inbound only and minimal.
- **Investor deck and business plan**: the go-to-market section leads with these three segments in South Africa, then Nigeria/Kenya/Ghana.

## 5. Market (ASSUMPTION: cite and verify before external use)

Directional figures for sizing; each document should present them as "est." with the source noted.
- Formal and informal SMBs in Sub-Saharan Africa: ~44 million MSMEs (IFC/World Bank est.); South Africa ~2.5–3 million SMMEs (SEDA/Stats SA); Nigeria ~39 million MSMEs (SMEDAN); Kenya ~7.4 million MSMEs (KNBS).
- WhatsApp is the dominant messaging app in SA, NG, KE, GH (>90% of internet users in SA and NG use it; DataReportal 2025).
- Mobile money: Sub-Saharan Africa accounts for ~70% of global mobile money value (GSMA State of the Industry 2025, >US$1 trillion processed/yr).

Serviceable market used in the model (ASSUMPTION):
- **TAM**: 44M SSA MSMEs.
- **SAM**: ~3.5M digitally active SMBs in the 23 rail-covered countries that sell via social/WhatsApp and can pay ≥US$25/mo.
- **SOM (5-yr)**: ~0.5% of SAM ≈ 17,500 paying workspaces.

---

## 6. Traction and pilot (placeholders; founder to fill)

- **Pilot campaign in progress: 12 brands in Gauteng, South Africa, running Sept 2026 to 30 November 2026** (FACT, founder). Name: `[[PILOT NAME]]`.
- Model implication: pilot brands aren't paying during the pilot. First paid conversions are **December 2026**, and pilot results (case studies, KPIs) are available for the investor raise from **December 2026**.
- **Case study placeholders:** `07_Case_Studies/Gauteng_Pilot_Case_Studies.md`. The lead case study is a **Gauteng braiding & hair studio** (solo entrepreneur, Starter tier), picked as the most attainable, lowest-barrier proof point. It has 11 more archetype slots across solo, SME and agency. Decks, proposals and the business plan should include a case-study slide/section using the lead's structure, with all metrics as `[[placeholders]]` and target KPIs clearly labelled as goals.
- Pilot KPIs to report: brands onboarded `[[ ]]`, WhatsApp conversations `[[ ]]`, orders/GMV `[[ ]]`, content pieces published `[[ ]]`, time saved/week `[[ ]]`, conversion uplift `[[ ]]`, NPS `[[ ]]`.
- pawaPay and Fincra go-live: **week of 14 September 2026** (FACT, founder). Model implication: payments are in place for all 23 countries from October 2026, so market expansion timing depends on sales and marketing capacity, not on payment rails.
- Founder/team: `[[FOUNDER NAME, TITLE]]`, `[[TEAM]]`, `[[ADVISORS]]`.
- Contact: `[[EMAIL]]`, `[[PHONE / WHATSAPP]]`.

---

## 7. Fundraise

- Round: **Seed, R25M (≈ US$1.35M)** (FACT, founder). Instrument (SAFE vs priced equity) `[[TBC]]`.
- **The R25M must carry FluxMuse to profitability** (founder, 2026-09-11): the base case reaches EBITDA break-even and positive cash flow on this round alone, with no Series A. A later round is optional acceleration, not survival.
- Use of funds (ASSUMPTION): Product & engineering 40% (R10.0M), Sales & marketing / partner programme 30% (R7.5M), Market expansion (NG, KE, GH) & payments compliance 15% (R3.75M), Operations & working capital 15% (R3.75M).
- Detailed figures live in `FluxMuse_Financial_Model.xlsx`; decks and the business plan must quote that model, not invent numbers.
