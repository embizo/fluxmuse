# FluxMuse investor pitch deck: how to use it

**Deck:** `FluxMuse_Investor_Pitch_Deck.pptx` (30 slides: 19 core + appendix divider + A1–A7).
**Round:** Seed, **R25M** (≈US$1.35M), Fluxmuse Pty Ltd, South Africa.
**Numbers:** every financial figure is read at build time from `../06_Financial_Model/model_summary.json`
(model **v2**, dated 11 Sep 2026, Base case). Product, pricing, rails and market facts come from
`../00_FACTS_AND_ASSUMPTIONS.md`. Nothing in the deck is typed by hand.
**Build & QA:** `../_build/investor_deck/build_investor_deck.py` and `qa_investor_deck.py`
(house style, helpers and icons copied from the brand deck, so both decks look like one family).

---

## 1. Slide map

| # | Slide | Source of the numbers |
|---|---|---|
| 1 | Title: AI marketing team + WhatsApp commerce · Seed round R25M · `[[DATE]]` · Confidential | `seed_zar` |
| 2 | Problem: sales happen in chat, the tools don't | facts §4b (no stats by design) |
| 3 | Solution: one AI team that markets and sells in chat | facts §1 |
| 4 | Product: live today, and what's in review (3-phone checkout strip + platform stack) | facts §1, §3 |
| 5 | Why Africa, why now + TAM/SAM/SOM (all **est.**, sourced) | facts §5, `market_sizing` |
| 6 | Business model: ZAR / NGN / KES / GHS / USD prices, partner wholesale, Founding Member, FY5 streams | `price_tables`, `annual[4].revenue_by_stream_zar` |
| 7 | Go-to-market: three SA segments, partner channel, launch window, market entry sequence | facts §3, §4b, `markets.launch_months.Base` |
| 8 | Payments moat: 5 rails, 23 countries, 40+ operators (dark) | facts §3 |
| 9 | Traction & proof: Meta verification, WhatsApp approvals, publisher, rails, Gauteng pilot | facts §1, §6, case-study file |
| 10 | Competition & positioning (qualitative, categories only) | facts §1–§3 |
| 11 | Unit economics FY3 (LTV, CAC, LTV:CAC, payback) | `unit_economics_fy3`, `annual[].unit_economics` |
| 12 | Financial projections FY1–FY5 (chart + table) | `annual[0–4]` |
| 13 | Path to profitability on R25M (cash runway, break-even, buffer, gating) | `cash`, `markets.launch_mrr_gate_zar` |
| 14 | Scenarios & sensitivities (FX shock, trials −30%) | `scenarios`, `fx_shock`, `sensitivity_base` |
| 15 | Key risks and mitigations | `Financial_Model_Notes.md` §6, §10 |
| 16 | The ask: R25M, use of funds, reconciliation and downside reserve | `use_of_funds` |
| 17 | Milestones this round buys (timeline) | facts roadmap + `cash`, `markets` |
| 18 | Team + the hires the seed buys (MRR-gated) | `_build/fm_inputs.py` ROLES × `monthly_base` |
| 19 | Close: contact and data room | — |
| 20 | Appendix divider | — |
| 21–23 | **A1** key assumptions, verbatim | `key_assumptions` |
| 24 | **A2** paying workspaces by segment and by market | `annual[].ending_customers_*` |
| 25–26 | **A3** pricing: ZAR / local & USD / partner wholesale | facts §2, `price_tables` |
| 27 | **A4** payment rails by country | facts §3 |
| 28 | **A5** FX shock sensitivity | `fx_shock` |
| 29 | **A6** Founding Member discount cost vs alternatives | `founding_member` |
| 30 | **A7** founder confirmations still open — **INTERNAL** | `founder_confirmations_needed` |

Speaker notes are on **every** slide (80–150 words) and name the source of each number.

---

## 2. What to fill in before sending

| Placeholder | Slide | Notes |
|---|---|---|
| `[[DATE]]` | 1 | Date of the meeting or of the send. |
| `[[TBC]]` × 2 | 16 | Instrument (SAFE vs priced equity) and valuation. Both are still founder decisions (A7 #2). |
| `[[FOUNDER NAME, TITLE, BIO]]` | 18 | One line of bio; the card also shows the model role "Founder & CEO". |
| `[[CO-FOUNDER]]` | 18 | Model role "CTO / founding engineer". |
| `[[ADVISORS]]` | 18 | Names and one-line relevance, or delete the card if there are none yet. |
| `[[EMAIL]]`, `[[PHONE]]` | 19 | Contact details. |
| `[[LINK]]` | 19 | Data-room link (see §3). |

A1 also carries `[[CONFIRM]]` markers **inside quoted model assumptions** — leave them: they show an
investor exactly which inputs are not yet signed off. They are listed again on A7.

**Hide before sending:** slide **30 (A7)** is internal. In PowerPoint: right-click the thumbnail →
*Hide Slide*, or delete it. Also consider hiding the appendix divider and any appendix slide the
audience does not need (A3 pricing is usually kept; A5/A6 are diligence follow-ups).

---

## 3. Data-room checklist

| Item | Where it is today | Status |
|---|---|---|
| Financial model workbook | `../06_Financial_Model/FluxMuse_Financial_Model.xlsx` | Ready (v2, live formulas, Base selected) |
| Model notes (assumptions, scenarios, integrity checks) | `../06_Financial_Model/Financial_Model_Notes.md` | Ready |
| Model summary (the JSON this deck quotes) | `../06_Financial_Model/model_summary.json` | Ready |
| Business plan | `../05_Business_Plan/` | Check it is on model v2 before sharing |
| Facts and assumptions (internal sourcebook) | `../00_FACTS_AND_ASSUMPTIONS.md` | Internal — do not share as-is |
| Cap table (pre-round, fully diluted) | `[[ ]]` | Founder to supply |
| Company documents: CIPC registration, MOI, director IDs, tax clearance, B-BBEE affidavit | `[[ ]]` | Founder to supply |
| Meta verification evidence: Business Verification, Access Verification (Tech Provider), approved permissions screenshot | `[[ ]]` | Founder to export from Meta Business Suite |
| Payment-rail contracts / agreements: Yoco, Ozow, Paystack, pawaPay, Fincra | `[[ ]]` | Founder to supply; pawaPay and Fincra go live week of 14 Sept 2026 |
| Pilot data and consented case studies (12 Gauteng brands) | `../07_Case_Studies/Gauteng_Pilot_Case_Studies.md` (template) | **After December 2026 only**, with written consent |
| Product: architecture note, security and POPIA/NDPR/GDPR summary, RLS and audit-export evidence | `[[ ]]` | Founder to supply |
| Team: founder CVs, org chart, hiring plan | `[[ ]]` | Hiring plan is in the model (slide 18) |
| IP and domains: fluxmuse.ai, trademarks, repo ownership | `[[ ]]` | Founder to supply |
| Insurance, key contracts, any debt | `[[ ]]` | Founder to supply |

---

## 4. Claims rules (do not break these)

- **No customer counts, revenue, ratings, testimonials or results** until pilot data exists *with written
  consent*. Until 30 Nov 2026 the line is "pilot underway, results December 2026" — never projected results.
- **Label every projection** "Projection (model v2, base case)" and every market figure "est." with its source.
  The deck already does this; keep it if you edit.
- **Never** use these, in any material: "200+ businesses", "4.9 rating", SnapScan, Stitch, Flutterwave,
  PayFast or M-Pesa-direct in the rails story, "40–60% margins", "lifetime"/"for life" perks, or any
  guarantee. The QA script greps for all of them (plus the retired R18.5M raise figure).
- **Rails:** five secured rails, 23 countries live September 2026 (pawaPay and Fincra from 14 Sept),
  +2 coming soon (Botswana and Namibia). South Sudan and Zimbabwe are payouts-only and stay gated.
- **Instagram** is in Meta App Review — never shown as live. Other social networks are "coming soon".
- **Founding Member** is the only launch offer shown externally, and it is **not** offered on Agency;
  agencies see the permanent partner wholesale price R5,599/mo. Never present R5,599 as a 2-month discount.
- **Pricing** only for the 23 rail-covered countries. Gated countries get the waitlist, never prices.
- Screenshots: use only the deck-safe assets listed in `../assets/ASSETS_INDEX.md`. Anything marked
  "internal reference only" (live-site claims, FX-converted NG/KE pricing pages, payment steps that show a
  provider outside the five rails) must not appear in this deck.

---

## 5. Rebuilding after the model changes

```bash
cd docs/go-to-market/_build
python financial_model.py                     # regenerates the workbook, model_summary.json and all charts
cd investor_deck
python build_investor_deck.py                 # rebuilds 04_Investor_Pitch_Deck/FluxMuse_Investor_Pitch_Deck.pptx
python qa_investor_deck.py                    # structural QA + number trace + headless-Chrome previews
```

- Needs `python-pptx`, `Pillow`, `lxml` and Node (for the preview renderer). No LibreOffice.
- The build reads the JSON, so **no number is edited by hand**. If a figure on a slide looks wrong, fix the
  model, not the deck.
- `build_investor_deck.py` also reconstructs the hiring months for slide 18 from `fm_inputs.py` ROLES and the
  monthly MRR series, and asserts that the reconstruction matches `monthly_base.headcount`. If the hiring plan
  changes and that assertion fires, the slide (not the model) is out of date.
- QA must end with **Total findings: 0**. It checks: notes on every slide (80–150 words), body text ≥ 14pt
  (appendix tables may go to 12pt), no off-slide or overlapping shapes, edge margins, forbidden claims,
  placeholders only in `[[ ]]` form, text overflow and table growth measured in headless Chrome with the real
  Poppins/Inter fonts, and a **number trace**: every `R…` and `…%` token on a slide must match
  `model_summary.json`, the facts file or the model notes.
- Previews and contact sheets land in `_build/investor_deck/preview/FluxMuse_Investor_Pitch_Deck/`.

### Known cosmetic note

The chart `customers_by_segment` rounds each segment before stacking, so its FY1 and FY3 bar labels read
**422** and **3,821** while the model totals are **421** and **3,820**. Appendix A2 states this on the slide;
always quote the model totals.

---

## 6. Talk track in one minute

African SMBs already sell in chat but have no marketing capacity and no local checkout. FluxMuse gives them
an AI marketing team and WhatsApp commerce on five local payment rails across 23 countries. We are a verified
Meta Tech Provider with WhatsApp Business permissions approved, all five rails live from September 2026, and
a 12-brand Gauteng pilot reporting in December 2026. The R25M seed funds product, the South African launch and
the Nigeria/Kenya/Ghana wave; the base case reaches R238.0M of revenue and a 27.9% EBITDA margin in FY5, breaks
even on EBITDA in March 2029, turns cash-flow positive in October 2028, never drops below R7.96M of cash against
a R3.0M buffer, and needs no Series A — in Conservative, Base and Upside alike.
