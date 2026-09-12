# FluxMuse Financial Model v2: notes

**Files:** `FluxMuse_Financial_Model.xlsx` (live formulas, Base selected), `model_summary.json` (the outputs other documents quote), charts in `../assets/charts/`.
**Rebuild:** `venv/bin/python docs/go-to-market/_build/financial_model.py`. This regenerates the workbook, the JSON and all 48 chart PNGs (12 charts, 4 variants each).
**Status:** forward-looking projections, model date 11 Sep 2026, version v2. It replaces the R18.5M v1 model and follows the founder decisions of 11 Sep 2026 in `00_FACTS_AND_ASSUMPTIONS.md`. Inputs flagged `[[CONFIRM]]` in red on the Assumptions sheet still need founder sign-off.

**Integrity:**
- **Mirror check.** The Python build script mirrors the workbook independently. It evaluates all 36,977 formulas with its own Excel evaluator and compares 36,801 cells against the mirror, covering every monthly, annual and key-output cell plus the Use_of_Funds reconciliation. The build stops on any mismatch. The current build has 0 mismatches and 0 evaluation errors.
- **Hand checks.** Three cells are also checked by hand: a Solo Starter cohort balance, Nigeria's partner-wholesale Agency revenue, and the FY2 revenue roll-up.
- **Recalculation.** Separately, the saved file was recalculated with the open-source `formulas` engine. All 46 key outputs matched: revenue, EBITDA, margin, workspaces, ARR, cash, segment and market counts, Founding Member cost, LTV:CAC, break-even, cash-flow months, minimum cash, bridge, launch months and the profitability flag.
- **Errors.** The recalculation found no `#REF`, `#DIV/0` or `#N/A` values.

---

## 1. Headline: Base case

| | FY1 | FY2 | FY3 | FY4 | FY5 |
|---|---|---|---|---|---|
| Revenue (R m, net of launch discounts) | 3.4 | 24.9 | 73.1 | 144.9 | 238.0 |
| Revenue (US$ m) | 0.19 | 1.34 | 3.95 | 7.83 | 12.86 |
| EBITDA (R m) | -7.1 | -13.7 | 0.5 | 31.5 | 66.3 |
| EBITDA margin | n/m | -55% | 1% | 22% | 28% |
| Gross margin / software GM | 47% / 50% | 67% / 72% | 72% / 77% | 75% / 80% | 76% / 81% |
| Paying workspaces (Sep) | 421 | 1,759 | 3,820 | 6,261 | 8,816 |
| of which Solo / SMEs / Agencies / Enterprise | 229 / 175 / 17 / 1 | 926 / 768 / 62 / 3 | 1,933 / 1,749 / 133 / 6 | 3,062 / 2,970 / 218 / 11 | 4,173 / 4,305 / 321 / 17 |
| of which ZA / NG / KE / GH / Rest (USD) | 421 / 0 / 0 / 0 / 0 | 1,360 / 221 / 118 / 60 / 0 | 2,574 / 544 / 340 / 216 / 146 | 4,091 / 907 / 586 / 383 / 294 | 5,724 / 1,275 / 837 / 548 / 433 |
| Subscription ARR (R m) | 8.1 | 36.9 | 89.1 | 162.6 | 249.3 |
| Net subscription ARPA (R / month) | 1,612 | 1,739 | 1,900 | 2,112 | 2,327 |
| Founding Member discount cost (R) | 26,444 | 118,887 | 45,283 | 0 | 0 |
| Closing cash (R m) / headcount | 19.1 / 18 | 8.0 / 41 | 13.2 / 68 | 48.4 / 92 | 104.4 / 135 |

**Cash (Base)**

| Output | Value |
|---|---|
| Seed | R25.0M (≈US$1.35M), lands Feb 2027 |
| Series A | none (input kept at R0) |
| Pre-seed bridge required | **R57,528**: cash dips to -R57.5k in Jan 2027 on R500k opening cash `[[CONFIRM]]` |
| Minimum cash from the seed month on | **R7.96M in Sep 2028**, R4.96M above the R3.0M buffer |
| EBITDA break-even | first **Mar 2029**; EBITDA ≥ 0 every month from **Jun 2029** |
| Operating cash flow positive | first **Oct 2028**; ≥ 0 every month from **May 2029** |
| Market launches | Nigeria **Feb 2028**, Kenya **Apr 2028**, Ghana **Jun 2028**, Rest of Africa (USD) **Nov 2028**, Botswana & Namibia off |
| Profitable on the R25M seed alone | **Yes** |

After break-even in Mar 2029, EBITDA dips again in Apr–May 2029. Net MRR clears the R5M hiring gate, so 10 FTE join in one month: engineers scale-up I ×3, marketing expansion I ×3, the Head of Sales & Partnerships, a finance analyst, and Kenya's 12-month team expansion ×2. EBITDA stays positive from Jun 2029.

## 2. Scenarios

| | Conservative | Base | Upside |
|---|---|---|---|
| Revenue FY1 / FY3 / FY5 (R m) | 2.7 / 39.0 / 116.0 | 3.4 / 73.1 / 238.0 | 4.6 / 121.8 / 450.9 |
| EBITDA FY3 / FY5 (R m) | -8.4 / 24.7 | 0.5 / 66.3 | 34.6 / 223.4 |
| FY5 EBITDA margin | 21% | 28% | 50% |
| Paying workspaces FY5 | 3,974 | 8,816 | 17,793 |
| Headcount FY1 / FY3 / FY5 | 13 / 44 / 67 | 18 / 68 / 135 | 21 / 70 / 135 |
| EBITDA ≥ 0 sustained from | Mar 2030 | Jun 2029 | Jun 2028 |
| Operating cash flow ≥ 0 sustained from | Oct 2029 | May 2029 | Apr 2028 |
| Minimum post-seed cash | R4.27M (Sep 2029) | R7.96M (Sep 2028) | R15.08M (Mar 2028) |
| Pre-seed bridge | R69.7k | R57.5k | R39.8k |
| Launches NG / KE / GH / Rest | Sep 2028 / Jan 2029 / Mar 2029 / Oct 2029 | Feb 2028 / Apr 2028 / Jun 2028 / Nov 2028 | Nov 2027 / Jan 2028 / Mar 2028 / Sep 2028 |
| Profitable on R25M alone | **Yes** | **Yes** | **Yes** |

**Scenario drivers** (columns D:F on Assumptions, switched by the selector in B6)

| Driver | Conservative | Base | Upside |
|---|---|---|---|
| Trial growth m/m, FY1 → FY5 | 10% → 1.0% | 12% → 1.5% | 14% → 2.0% |
| Conversion multiplier (Solo 11%, SME 14% base) | 0.85x | 1.00x | 1.20x |
| Churn multiplier / paid CAC multiplier | 1.20x / 1.20x | 1.00x / 1.00x | 0.85x / 0.85x |
| Expansion plan shift | +3 months | 0 | -2 months |
| Inbound enterprise multiplier | 0.5x | 1.0x | 1.5x |
| **Paid-acquisition cap (% of last month's net MRR, plus floor)** | 30% | 35% | 50% |
| **Hiring & launch MRR-gate multiplier** | **1.40x** | 1.00x | 0.80x |
| Commerce fee on WhatsApp-checkout GMV | 0% | 0% | 0.75% (not in current pricing) |

Hiring is no longer the same in every scenario. Each role and each launch waits for its MRR milestone times the gate multiplier, so Conservative hires later and Upside earlier. Upside reaches the same 135 FTE ceiling as Base because the role list ends there. That is why its FY5 margin (50%) is high.

## 3. Constraint check

The constraint is:
- no Series A;
- closing cash ≥ R3.0M every month from Feb 2027;
- EBITDA and operating cash flow reach break-even and stay there.

The Cash_Flow sheet evaluates it live (`PROFITABLE ON THE SEED ALONE?`), and the Cover repeats it.

| Test | Conservative | Base | Upside |
|---|---|---|---|
| No Series A | Yes | Yes | Yes |
| Cash ≥ R3.0M every month from the seed | Yes: low R4.27M, Sep 2029; 0 months below | Yes: low R7.96M, Sep 2028; 0 months below | Yes: low R15.08M, Mar 2028; 0 months below |
| EBITDA break-even reached and sustained | first Nov 2029; ≥ 0 from Mar 2030 | first Mar 2029; ≥ 0 from Jun 2029 | Jun 2028 onward |
| Operating cash flow positive and sustained | first Jul 2029; ≥ 0 from Oct 2029 | first Oct 2028; ≥ 0 from May 2029 | Apr 2028 onward |
| **Result** | **Pass** | **Pass** | **Pass** |

**Conservative needed a cost cut, and the model reports it.**
- **Base hiring gates (1.00x).** Cash falls to **-R2.76M in Jan 2030**, a **R5.76M shortfall** against the buffer, and the constraint fails.
- **Smallest fixes.** The model searches for the smallest change that passes. The options are:
  - raise the hiring and launch gate multiplier to **1.35x**;
  - or, keeping Base gates, cut every non-founder salary by **13%**.
- **What's adopted.** Conservative uses **1.40x**, which leaves R1.27M of headroom rather than R0.5M.
- **What it costs.** Wave-1 launches move to Sep 2028 to Mar 2029, and FY5 headcount falls to 67.

**Pre-seed bridge.** Every scenario needs R40k–R70k before the seed lands. Pilot conversion barely changes this: R63k at 50% conversion and R52k at 100%. Opening cash above ~R560k, a founder loan, or pilot prepayments would cover it.

## 4. How v2 works

**Timing and lean mode.** Month 1 is Oct 2026. Until the seed lands (input month 5 = Feb 2027), the model runs:
- the two founders at reduced salaries (R45k and R55k CTC);
- lean hosting at R15k a month and overheads at R15k a month;
- software tools;
- the pilot programme at R15k a month in Oct–Nov.

Before the seed there is no paid marketing, no hiring, no office, no travel and no legal retainer.

**Pilot.** The 12 Gauteng brands pay nothing in Oct–Nov 2026. On 1 Dec 2026, 75% of them (9 brands) convert. The mix is 40% Solo, 45% SME and 15% Agency. They pay the pilot prices for 2 bills (R249 / R999 / R2,499 / R3,999), then list price, or partner wholesale for agencies. The discount costs R13.6k in FY1. It is measured against the price actually booked, so a pilot agency's discount is R5,599 − R3,999. South Africa launches commercially on 1 Dec 2026, and no other customer pays before December.

**Founding Member (option B).**
- **Who and when.** Solo and SME sign-ups inside a launch window get 30% off their first 2 monthly bills: South Africa from Dec 2026 to Jan 2027, and Nigeria, Kenya and Ghana for their first 60 days. USD markets have no window.
- **Agencies.** The offer isn't available on Agency and doesn't stack with partner wholesale.
- **Retention.** 8% of new sign-ups are assumed to churn before the second discounted bill.
- **Annual plans.** Annual plans (25% of subscriptions) get **2 bonus months**. The model recognises each window cohort's annual fee (10 × monthly) over 14 months instead of 12, and books the difference as discount until the cohort's term ends.
- **Uplift.** Sign-ups rise **+20%** inside each window `[[CONFIRM]]`.

The total discount cost is R26k in FY1, R119k in FY2 and R45k in FY3. It never exceeds 1.3% of gross subscriptions. The Sensitivity sheet compares options A, B and None:

| Launch offer (Base) | FY1–FY3 discount cost | Minimum post-seed cash | Profitable on R25M |
|---|---|---|---|
| B Founding Member (default) | R190.6k | R7.96M | Yes |
| A Launch Sprint | R63.1k | R7.94M | Yes |
| None | R0 | R7.82M | Yes |

Because of the assumed uplift, B leaves slightly *more* cash than no offer, so it doesn't threaten the R25M constraint. The uplift is unproven, so treat this as a hypothesis for the ZA Dec–Jan window to test.

**Markets.** ZA → Nigeria, Kenya, Ghana → Rest of rail-covered Africa → Botswana & Namibia. Gated countries are zero. Each wave-1 country has its own inputs:
- earliest launch month;
- MRR gate;
- country-lead hire (2 months before launch);
- local sales and CS (hired at launch; team expansion after 12 months);
- launch marketing: NG R350k, KE R300k, GH R250k, spread over 3 months;
- one-off compliance: R300k / R250k / R200k;
- monthly compliance: R12k / R12k / R10k;
- CAC and churn indices.

The Rest-of-Africa row (19 countries, USD, self-serve, no team) has R150k of VAT-registration cost, R20k a month of compliance and R20k a month of marketing. Botswana & Namibia is switched off.

*Why these launch defaults.* The planned earliest months are staggered three months apart (Nov 2027 / Feb 2028 / May 2028, Rest Nov 2028). Each launch also waits until last month's net MRR clears a rising gate: R0.9M / R1.2M / R1.5M / R2.5M. Staggering spreads the fixed country costs across the cash trough in Sep 2028, and the gates stop a launch until South Africa can carry it. In Base the gates, not the plan months, set the dates. The launch decision needs MRR ≥ gate, and the launch follows 2 months later.

**Pricing at parity, FX and repricing.**
- **Price points.** ZA uses ZAR list prices. Nigeria, Kenya and Ghana book the fixed local price points from facts §2, converted at 1 ZAR = ₦82.83 / KSh 8.07 / GH₵ 0.68. The 19 USD markets book $27 / $109 / $269 / $429 / $1,099 at R18.50. v1's 75–85% regional price index is gone.
- **Drift.** Each month, local prices are multiplied by an FX value factor, driven by depreciation vs ZAR of NGN -10%, GHS -8%, KES -3% and USD 0% a year `[[CONFIRM]]`.
- **Repricing.** Every quarter, if the ZAR value of local prices has drifted more than 10%, prices are reset to parity using the rate observed one quarter earlier.
- **Escalator.** A 6% list-price escalator applies each October in all markets.

**Segments.** Self-serve trials in each market split 65% Solo and 35% SME.

| | Solo | SME | Agencies | Enterprise |
|---|---|---|---|---|
| Acquisition | trials × 11% conversion | trials × 14% conversion | 0.5 inbound a month in SA + 1.5 per partnerships manager; 0.4 per NG/KE/GH country lead + inbound | inbound only: FY1 1 deal, then 2 / 4 / 6 / 8 a year |
| Tier mix | 90% Starter / 10% Growth | 85% Growth / 15% Scale | Agency tier at partner wholesale | Enterprise |
| Upgrades | Starter → Growth 1.0% a month | Growth → Scale 0.8% a month | none | none |
| Monthly churn | 6.5% Starter / 4.0% Growth | 3.0% Growth / 2.2% Scale | 2.0% | 1.0% |
| Paid CAC | R2,200 | R6,500 | partner programme + team | R25k handling per deal |

**Partner wholesale.**
- **Price.** Every agency-segment customer (input: 100%) pays **R5,599 / ₦463,000 / KSh 44,999 / GH₵ 3,799 / $299** a month.
- **Sub-accounts.** Client sub-accounts are part of the partner's Agency subscription. v1's separate sub-account stocks at a 40% wholesale discount are removed, because that discount doesn't map onto the decided scheme.
- **Referral commission.** Commission on clients a partner refers to their own plans is undecided and **not modelled**.

**Cost discipline.**
- **Hiring gates.** Every non-founder role has an earliest month and an MRR gate. It is hired only after the seed, once last month's net MRR ≥ gate × scenario multiplier.
- **Paid acquisition.** Paid spend = MIN(desired spend, R40k floor + cap % × last month's net MRR). Wanted sign-ups the cap can't fund are simply not acquired.
- **Payback test.** Paid acquisition is switched off in any segment and market where CAC payback (CAC ÷ ARPA × 70% GM) exceeds 12 months `[[CONFIRM]]`. It doesn't bind at current inputs: the worst payback in any live market is 6.1 months (Solo, ZA, Conservative, Dec 2026).
- **Brand budget.** Brand spend = MIN(annual ceiling, floor + 4% of MRR).
- **FY1 effect.** In FY1 the cap funds 77% of the paid acquisition the funnel wants, and 100% from FY2.

**Commerce fee:** 0% in Base and Conservative, 0.75% in Upside only (flagged: not in current pricing). **Campaign Financing:** excluded.

## 5. Use of funds (R25M) against modelled spend

The allocation is 40 / 30 / 15 / 15: R10.0M / R7.5M / R3.75M / R3.75M. The seed funds net burn, not gross spend, so each category's share of modelled gross spend is compared with its allocation share.

| Category | Allocation | Spend, 18 months (Feb 2027–Jul 2028) | Share of spend, 18 months | Spend, 24 months (Feb 2027–Jan 2029) | Share of spend, 24 months | Gap at 24 months |
|---|---|---|---|---|---|---|
| Product & engineering | 40% | R14.83M | 39.4% | R24.30M | 38.4% | -1.6 pp |
| Sales & marketing / partner programme | 30% | R11.59M | 30.8% | R19.18M | 30.3% | +0.3 pp |
| NG/KE/GH expansion & payments compliance | 15% | R3.64M | 9.7% | R6.14M | 9.7% | **-5.3 pp** |
| Operations & working capital | 15% | R7.57M | 20.1% | R13.66M | 21.6% | **+6.6 pp** |
| Total gross spend | | R37.63M | | R63.28M | | |
| less revenue collected | | R21.53M | | R46.34M | | |
| **Net cash consumed from the seed** | | **R16.10M** | | **R16.93M** | | |
| Seed remaining at the end of the window | | R8.90M | | R8.07M | | |

**Gaps to note:**
- **Expansion is under-spent against 15%.** The MRR gates start the wave-1 launches 12–16 months after close, and country teams are small.
- **Operations & working capital is over 15%.** Customer success, processing, WhatsApp pass-through and support scale with revenue, and revenue funds them.

Either relabel the split as "share of spend", or move about 5 points from expansion to operations in the deck. About R8M of the seed is still unspent after 24 months. That is the buffer and the reserve that carry the business through the Sep 2028 trough.

## 6. FX shock: ZAR 15% stronger (Base)

The shock applies from Oct 2028 (month 25), once Nigeria, Kenya and Ghana are live.

| Output | Base | ZAR +15%, repricing on | ZAR +15%, no repricing |
|---|---|---|---|
| FY3 revenue | R73.06M | R73.25M (+R0.19M) | R69.46M (-R3.60M) |
| FY5 revenue | R237.98M | R238.05M (+R0.07M) | R216.97M (-R21.01M) |
| FY3 EBITDA | R0.54M | R0.73M (+R0.19M) | -R2.10M (-R2.64M) |
| FY5 EBITDA | R66.29M | R66.77M (+R0.48M) | R56.40M (-R9.89M) |
| Minimum post-seed cash | R7.96M (Sep 2028) | R7.55M (Dec 2028) | R6.79M (Feb 2029) |
| Profitable on R25M alone | Yes | Yes | Yes |

With the quarterly repricing policy, the shock costs one quarter of revenue and then triggers a reset. The reset also clears the depreciation that had built up below the 10% trigger, so later years end slightly *above* Base. Without repricing, FY5 EBITDA falls by R9.9M, but the R3.0M buffer still holds. **Repricing discipline is the main FX control.**

## 7. Unit economics, FY3 (Base)

| Segment | ARPA (R / month, gross) | Monthly churn | LTV | CAC | LTV:CAC | Payback |
|---|---|---|---|---|---|---|
| Solo | 809 | 6.3% | R9,900 | R3,307 | 3.0x | 5.3 months |
| SMEs | 2,769 | 2.9% | R72,544 | R5,667 | 12.8x | 2.7 months |
| Agencies (partner wholesale) | 5,919 | 2.0% | R222,419 | R36,973 | 6.0x | 8.1 months |
| Enterprise (4 inbound deals) | 21,535 | 1.0% | R1.65M | R25,000 | 66x | 1.5 months |
| **Blended** | 1,900 (net) | | R31,572 | R5,604 | **5.6x** | **3.8 months** |

- LTV = ARPA × software gross margin (76.8%) ÷ monthly logo churn.
- Solo/SME CAC includes the paid spend plus a share of brand, launch and marketing payroll, split by new-customer mix.
- Agency CAC = partner programme cost + partnerships-manager payroll per new agency.

## 8. Changes from v1, and why

| Area | v1 | v2 | Why |
|---|---|---|---|
| Raise | R18.5M, Dec 2026; Series A needed in Conservative | R25M, Feb 2027 (input); Series A input R0 | Founder decision: R25M must reach profitability alone |
| Constraint | cash ≥ 0 | cash ≥ R3.0M from the seed; sustained EBITDA and operating-cash-flow break-even; live pass/fail output | Founder constraint |
| Pre-seed | spend from month 1 | lean mode until the seed; new "pre-seed bridge required" output | Seed now lands in Feb 2027 |
| Pilot | 25 paying workspaces in Oct–Nov 2026 | 12 brands free; 75% convert 1 Dec at 50% off 2 bills | Facts §6 |
| Launch offer | none | Founding Member B (A and None as sensitivities), gross → discounts → net, +20% uplift | Facts §2 decision |
| Markets | SA + NG/KE/GH + "francophone/other" regions allocated by trial share | own row per market with launch-month input, lead hire, launch marketing and compliance; Rest (19 USD countries); BW/NA off; gated = 0 | Facts §3 sequence and gating |
| Pricing outside SA | 75–85% of ZAR list | fixed local/USD price points at parity; FX drift, quarterly repricing; FX-shock sensitivity | Facts §2 |
| Acquisition | channels: self-serve, agency, direct AEs | segments: Solo, SMEs, Agencies, Enterprise inbound (no AEs) | Facts §4b |
| Agency revenue | Agency at list + client sub-accounts at 40% wholesale | Agency tier at partner wholesale R5,599 (local/USD equivalents); no sub-account revenue; referral commission not modelled | Partner wholesale decision |
| Cost discipline | same hiring plan in all scenarios | MRR-gated hires and launches, scenario gate multiplier, paid-acquisition cap and payback test, brand budget scaled to MRR | Profit on R25M; Conservative must survive |
| Commerce fee | 0.75% in every scenario | Upside only | Not in current pricing |
| Use of funds | R18.5M, 18-month cross-check | R25M; 18- and 24-month reconciliation with gaps | Facts §7 |
| Base result | FY5 R335.0M revenue, 40% EBITDA margin, break-even Oct 2028 | FY5 R238.0M, 28%, break-even Mar 2029 (sustained Jun 2029) | Wholesale agency pricing, lower non-SA volumes, later seed and launches, scale-up hires |

## 9. Calibration log

The raise was never changed. Every iteration used hiring pace, gates, marketing caps or launch timing.

1. **Previous agent's draft.** It had the R25M seed in Feb 2027, MRR-gated hires and launches, and a paid cap, but still used v1 agency sub-accounts. The partner wholesale decision superseded it.
2. **Partner wholesale, Founding Member excluded from Agency, payback guard added; gates 1.00x in Base and Conservative.**
   - Base passed with R7.96M minimum cash, but its FY5 EBITDA margin was **36.7%**, above the 15–30% target.
   - Conservative **failed**: cash reached -R2.56M in Sep 2029 and first fell below the buffer in Dec 2028.
3. **Base margin: added FY4–FY5 scale-up roles gated at R14–19M net MRR:**
   - engineers IV ×5 and data & AI II ×3;
   - marketing III ×4 and partnerships III ×2;
   - SME account managers II ×4 and CS agents VI ×10;
   - finance/legal/people ×3 and Ghana expansion ×2.

   Base FY5 margin fell to **27.9%**, and minimum cash was unchanged at R7.96M because these hires come after the trough.
4. **Conservative: tested three levers.**
   - **Gate multiplier (1.0–1.75x):** 1.35x is the first value that passes.
   - **Paid cap (20–30% of MRR):** lower caps made cash *worse*, because the business acquires fewer customers.
   - **Launch delay (+3/+6/+9 months):** no effect once the MRR gates bind.

   Adopted **1.40x**: minimum cash R4.27M, profitable on the seed alone.

## 10. Known limitations

- **Volume is the biggest risk to the buffer.** Base Sensitivity grid (gates at 1.00x):
  - trial volume 30% below plan at base churn: minimum post-seed cash **R0.98M** (below the buffer);
  - with churn also +15%: **-R0.07M**;
  - volume -15%: R4.15M (passes);
  - churn +30% with volume -15%: R3.10M (just passes).

  If early trials run more than ~20% below plan, raise the gate multiplier as in Conservative.
- **Simplified dynamics.**
  - Customers are fractional, and launch and hiring decisions are one-way (never reversed).
  - Gates use last month's MRR, with no look-ahead.
  - There are no downgrades. Upgrades only run Solo Starter → Growth and SME Growth → Scale.
  - Agency client growth adds no revenue beyond the partner's Agency subscription and its usage.
- **FX paths are deterministic.** The model assumes repricing causes no extra churn. USD markets are assumed flat against ZAR.
- **Founding Member.** The uplift (+20%) and the 8% churn between bills are assumptions. The annual-plan bonus is an approximation, recognised over 14 months.
- **Upside margins are high (42–50% in FY4–FY5)** because the hiring plan tops out at 135 FTE. A real Upside plan would reinvest more.
- **Accounting simplifications.**
  - Tax ignores SA's 80% cap on using assessed losses.
  - D&A, interest, VAT and payables are ignored.
  - Receivables and deferred revenue are simplified.
- **WhatsApp pass-through is booked as gross revenue**, which lowers blended gross margin; software GM is shown separately.
- **Static windows and values.** The Use_of_Funds reconciliation windows are fixed at build time from the seed month. Sensitivity values are computed at build time, so rerun the build after changing inputs.

## 11. Replace with pilot data first (in order)

1. **Trial-to-paid conversion by segment (Solo 11%, SME 14%), the Solo/SME split, and pilot conversion (75%).** These drive both revenue and the buffer.
2. **Trial volume at launch (250 a month in ZA) and early growth (12% m/m).** The Sensitivity grid shows this is the variable most likely to breach R3.0M.
3. **Month-1 to month-3 churn by segment.** Solo Starter at 6.5% sets Solo's 3.0x LTV:CAC.
4. **Paid CAC by segment, and the Founding Member uplift**, measured in the ZA Dec 2026–Jan 2027 window.
5. **Agency behaviour:** agencies signed per partnerships manager, and uptake of partner wholesale.
6. **Usage costs:** billable WhatsApp messages, AI-credit utilisation, and support contacts per workspace.
7. **NG/KE/GH inputs:** trials at launch, CAC and churn indices, and actual FX drift against the repricing trigger.
8. **Merchant GMV and acceptance of a commerce fee** (Upside only).

## 12. Founder confirmations needed

- **Cash and seed timing.**
  - Opening cash at 1 Oct 2026 (default R500k), and how to cover the **R57.5k pre-seed bridge**: founder loan, pilot prepayment or an earlier close.
  - Seed close month (Feb 2027) and instrument (SAFE vs priced equity).
- **Pilot and launch offer.**
  - Pilot conversion rate (75%) and pilot segment mix (40% Solo / 45% SME / 15% Agency).
  - Founding Member sign-up uplift (+20%) and perks duration.
- **Pricing and FX.**
  - FX depreciation assumptions (NGN -10%, GHS -8%, KES -3%, USD 0% a year) and the repricing policy (>10% drift, one-quarter lag).
  - Partner referral commission %, and whether 100% of agency customers buy at wholesale.
  - Commerce fee (0.75%, Upside only; not in current pricing).
- **Cost discipline and hiring.**
  - The rules: MRR gates, scenario gate multipliers (1.40x / 1.00x / 0.80x), paid cap (30% / 35% / 50% of MRR) and the 12-month CAC payback limit.
  - Salary levels and the hiring plan, including founders' reduced salaries.
- **Markets.**
  - Wave-1 plan months, launch marketing and compliance budgets; the Rest-of-Africa gate.
  - Whether South Sudan and Zimbabwe can collect subscriptions via Fincra (both sit inside the USD row).
- **Other estimates.** Inbound enterprise deal volume, and the TAM/SAM/SOM estimates before external use.
