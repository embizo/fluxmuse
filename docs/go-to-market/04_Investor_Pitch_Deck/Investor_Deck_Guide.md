# FluxMuse investor pitch deck: how to use it

**Deck:** `FluxMuse_Investor_Pitch_Deck.pptx` (30 slides: 19 core + appendix divider + A1–A7).
**Round:** Seed, **R46M** (≈US$2.49M), Fluxmuse (Pty) Ltd, South Africa. Founder decision 2026-10-05: the seed
is sized to the model (R45.1M is the smallest seed at which the Base case passes, rounded up). `[[CONFIRM]]`
**Numbers:** every financial figure is read at build time from `../06_Financial_Model/model_summary.json`
(model **v3**, dated 5 Oct 2026, Base case). Product, pricing and status facts come from
`../08_Prospects/CURRENT_OFFER.md` and `../00_FACTS_AND_ASSUMPTIONS.md`; the model's reasoning is in
`../06_Financial_Model/Financial_Model_Notes.md`. Nothing in the deck is typed by hand.
**Build & QA:** `../_build/investor_deck/build_investor_deck.py` and `qa_investor_deck.py`.

**The one thing to get right in the room:** the R46M carries FluxMuse to profitability with no Series A in
the **Base and Upside** cases. **The Conservative case fails on R46M**, and the Base headroom is thin (about
R1.0M above the R3.0M buffer at the Nov 2030 low). The deck says this on slides 13–15; never drop it.

---

## 1. Slide map

| # | Slide | Source |
|---|---|---|
| 1 | Title: AI marketing team and a WhatsApp shop · Seed round R46M · `[[DATE]]` | `seed_zar` |
| 2 | Problem: sales happen in chat, the tools don't | segment work (no stats by design) |
| 3 | Solution: one loop, run from WhatsApp (newly launched; Meta publishing and checkout being switched on) | CURRENT_OFFER §3 |
| 4 | Product: live / in setup / not available status table, platform-stack infographic | CURRENT_OFFER §3 |
| 5 | Why Africa, why now + TAM/SAM/SOM (all **est.**) | facts §5, `market_sizing` |
| 6 | Business model: nine plans in three bands (ZAR), Founding Member, partner wholesale R6,999, FY5 streams | `price_tables`, `annual[4]` |
| 7 | Go-to-market: three segments, first group set up by hand, SA now → NG/KE/GH pending → USD later | `first_group`, `markets` |
| 8 | Payments: live in South Africa, the rest pending | CURRENT_OFFER §2–§4 |
| 9 | Where we are · no customers yet: Meta Tech Provider, live in SA, Paystack, TikTok; first group; lead guarantee | CURRENT_OFFER §2–§4 |
| 10 | Competition & positioning (qualitative, categories only) | facts |
| 11 | Unit economics FY3 (Solo does not pay back on loaded CAC) | `unit_economics_fy3` |
| 12 | Financial projections FY1–FY5 | `annual[0–4]` |
| 13 | Path to profitability: Base case on R46M, thin headroom | `cash`, `seed_sizing` |
| 14 | Scenarios: Base and Upside pass, Conservative fails; FX and headroom sensitivities | `scenarios`, `fx_shock`, `free_conversion_sensitivity`, `sensitivity_base` |
| 15 | Key risks (demand unproven, thin headroom, Meta, payment accounts, FX, execution) | Notes §6, §10 |
| 16 | The ask: R46M, why this size, use of funds 40/30/15/15 | `use_of_funds`, `seed_sizing` |
| 17 | Milestones: facts to Oct 2026, then model dates; `[[TARGET]]` for switch-on | CURRENT_OFFER §3, `markets`, `cash` |
| 18 | Team + the hires the seed buys (MRR-gated) | `fm_inputs.py` ROLES × `monthly_base` |
| 19 | Close: contact (thabo@fluxmuse.com) and data room | — |
| 20 | Appendix divider | — |
| 21–23 | **A1** key assumptions, verbatim | `key_assumptions` |
| 24 | **A2** paying workspaces by segment and market | `annual[].ending_customers_*` |
| 25 | **A3** pricing (1): nine plans in rands (pricing-tiers infographic) | CURRENT_OFFER §1 |
| 26 | **A3** pricing (2): local and USD prices, priced but not on sale | `price_tables` |
| 27 | **A4** payment rails by country: live and pending | payment-rails-matrix |
| 28 | **A5** FX shock (no repricing fails) | `fx_shock` |
| 29 | **A6** Founding Member discount cost | `founding_member` |
| 30 | **A7** founder confirmations — **INTERNAL** | `founder_confirmations_needed` |

(A1 paginates automatically; if it changes length, later slide numbers shift.) Speaker notes are on
every slide (80–150 words) and point at 00_FACTS, CURRENT_OFFER.md or Financial_Model_Notes.md.

What changed from the 11 Sept deck: R25M → R46M everywhere; the pilot and traction slides are replaced by
what is real (no customers, no pilot); "5 rails · 23 countries" is replaced by live-in-SA / pending; nine
tiers replace four; no trials; partner wholesale R6,999; the Conservative failure and thin headroom are
disclosed; stale screenshots (hero laptop/phone, checkout phones) are replaced by refreshed infographics.

---

## 2. What to fill in before sending

| Placeholder | Slide | Notes |
|---|---|---|
| `[[DATE]]` | 1 | Date of the meeting or send. |
| `[[TBC]]` × 2 | 16 | Instrument and valuation. |
| `[[TARGET]]` | 17 | Target date for switching on FluxMuse checkout and Meta publishing. |
| `[[FOUNDER NAME, TITLE, BIO]]`, `[[CO-FOUNDER]]`, `[[ADVISORS]]` | 18 | One line each, or delete the card. |
| `[[PHONE]]`, `[[LINK]]` | 19 | Phone and data-room link. |

A1 carries `[[CONFIRM]]` markers inside the quoted model assumptions. Leave them: this is an internal-review
deck and they show which inputs are not signed off. **Hide A7 before sending** (right-click → Hide Slide).

---

## 3. Data-room checklist

| Item | Where | Status |
|---|---|---|
| Financial model workbook, notes, summary | `../06_Financial_Model/` | Ready (v3) |
| Business plan | `../05_Business_Plan/` | Ready (v2.0, model v3) |
| Facts sourcebook, current offer | `../00_FACTS_AND_ASSUMPTIONS.md`, `../08_Prospects/CURRENT_OFFER.md` | Internal — do not share as-is |
| Cap table, company documents | `[[ ]]` | Founder to supply |
| Meta Tech Provider verification evidence | `[[ ]]` | Founder to export |
| Payment agreements: Paystack (live); pawaPay, Fincra (contracted, accounts pending) | `[[ ]]` | Founder to supply |
| Case studies | `../07_Case_Studies/First_Group_Case_Studies.md` (template) | None yet; consent and measured data only |

---

## 4. Claims rules (enforced by `qa_investor_deck.py`)

- **No customers, no pilot, no results.** The honest line: "we are opening with a small first group of
  businesses, and we set you up by hand."
- **Status labels** from CURRENT_OFFER §3: live (say "newly launched"), being switched on, not available.
  Facebook/Instagram auto-publishing and FluxMuse checkout are never shown as live.
- **Payments:** Paystack live in South Africa; pawaPay and Fincra contracted, accounts pending; no paid
  checkout outside South Africa.
- **Never write** (CURRENT_OFFER §5): free trial, free month, 14 days free, try it free, risk-free, pilot (as a
  cohort), our customers, trusted by, proven, guaranteed results/sales/ROI, 10x, uplift numbers, money-back or
  refund, SnapScan, Stitch, Flutterwave, PayFast, M-Pesa direct. The lead guarantee (3 qualified leads in 30
  days, or extended support) is allowed, with its conditions.
- **Never quote the v2 numbers** (R25M ask, R238M FY5, break-even Mar 2029). QA fails if they appear, and
  asserts the R46M ask appears on the title, ask and close slides.
- **Label every projection** "Projection (model v3, base case)" and every market figure "est.".
- Don't embed `screenshots/composites/hero-laptop-phone_*`, `laptop-home*`, `browser-*` or the checkout-phone
  composites (stale pricing, "Start free trial", Yoco payment demo).

---

## 5. Rebuilding after the model changes

```bash
cd docs/go-to-market/_build
python3 financial_model.py
cd investor_deck
python3 build_investor_deck.py
CHROME_PATH=/opt/pw-browsers/chromium-1194/chrome-linux/chrome python3 qa_investor_deck.py
```

QA renders every slide in headless Chrome (random debug port, locally installed Poppins/Inter) and checks
notes, font sizes, overlaps, margins, forbidden claims, overflow and a number trace against
`model_summary.json`, the facts file, CURRENT_OFFER.md and the model notes. The only accepted residual
findings are a few hundredths of an inch of table-row growth on A7 (internal slide). The chart file
`cash_runway_r25m*.png` keeps its old name but plots the R46M seed.

---

## 6. Talk track in one minute

Small businesses in South Africa already sell in chat, but have no marketing capacity and no simple shop.
FluxMuse gives them an AI marketing team and a shop that runs on WhatsApp. It is newly launched in South
Africa; we are a verified Meta Tech Provider, Paystack is live, and we are opening with a small first group of
businesses we set up by hand. We have no customers yet. We are raising R46M. In our base case that carries us
to profitability with no Series A; upside passes too, but the conservative case falls short and the base-case
headroom is thin, so we will measure conversion from the first month and slow hiring if it lags.
