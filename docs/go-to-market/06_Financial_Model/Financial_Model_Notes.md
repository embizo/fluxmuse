# FluxMuse Financial Model v3: notes

**Files:** `FluxMuse_Financial_Model.xlsx` (live formulas, Base selected), `model_summary.json` (the outputs other documents quote), charts in `../assets/charts/`.
**Rebuild:** `python3 docs/go-to-market/_build/financial_model.py` from the repo root. This regenerates the workbook, the JSON and all 48 chart PNGs (12 charts, 4 variants each).
**Status:** forward-looking projections, model date 5 Oct 2026, version v3. It replaces v2 (11 Sep 2026) and follows the current offer in `08_Prospects/CURRENT_OFFER.md` and the live product tables. FluxMuse has no paying customers yet, so every volume and rate below is an assumption. Inputs flagged `[[CONFIRM]]` show in red on the Assumptions sheet and need founder sign-off.

**The short version.** On the current offer, the Base case does **not** reach EBITDA break-even on the R25M seed alone. Cash falls below the R3.0M buffer in Jan 2029, runs out in Mar 2029 and bottoms at **-R17.0M in Nov 2030**. EBITDA turns positive in **Jan 2031** and stays positive. Closing the gap needs about **R20.0M** more funding, or one of the levers in §3. No input was tuned to change this result.

**Integrity:**
- **Mirror check.** The Python build mirrors the workbook independently. It evaluates all 43,529 formulas with its own Excel evaluator and compares 43,327 cells against the mirror: every monthly, annual and key-output cell plus the Use_of_Funds reconciliation. The build stops on any mismatch. Current build: **0 mismatches, 0 evaluation errors.**
- **Hand checks.** Four cells are also checked by hand: a South African Solo Nano cohort balance (month 13), Nigeria's partner-wholesale Agency revenue (month 40), the active Free-user balance in South Africa (month 7) and the FY2 revenue roll-up. All match.
- **Recalculation.** The saved file was recalculated separately with the open-source `formulas` engine: 48,886 cells, **0 `#REF`, `#DIV/0` or `#N/A` errors**. FY1-FY5 revenue, EBITDA, closing cash and paying workspaces (20 values) all matched the JSON, as did the break-even month (Jan 2031) and the profitability flag ("No").

---

## 1. Headline: Base case

| | FY1 | FY2 | FY3 | FY4 | FY5 |
|---|---|---|---|---|---|
| Revenue (R m, net of Founding Member discount, no VAT) | 1.9 | 9.5 | 25.5 | 54.1 | 93.5 |
| Revenue (US$ m) | 0.10 | 0.51 | 1.38 | 2.92 | 5.06 |
| EBITDA (R m) | -7.0 | -11.7 | -16.9 | -10.6 | 4.5 |
| EBITDA margin | n/m | -124% | -66% | -20% | 5% |
| Gross margin / software GM | 22% / 23% | 55% / 59% | 62% / 67% | 67% / 71% | 71% / 76% |
| Paying workspaces (Sep) | 238 | 728 | 1,734 | 3,147 | 4,627 |
| of which Solo / SMEs / Agencies / Corporate / Enterprise | 116 / 104 / 17 / 1 / 0 | 348 / 336 / 40 / 4 / 1 | 817 / 821 / 85 / 8 / 3 | 1,448 / 1,532 / 146 / 15 / 5 | 2,071 / 2,322 / 203 / 24 / 8 |
| of which ZA / NG / KE / GH / Rest (USD) | 238 / 0 / 0 / 0 / 0 | 727 / 1 / 0 / 0 / 0 | 1,389 / 196 / 101 / 48 / 0 | 2,233 / 417 / 254 / 155 / 88 | 3,154 / 634 / 404 / 257 / 179 |
| Active Free users (Sep) | 2,275 | 5,490 | 12,484 | 20,478 | 27,061 |
| Free users upgrading to paid in the year | 54 | 224 | 511 | 969 | 1,419 |
| Subscription ARR (R m) | 3.9 | 12.7 | 32.0 | 63.0 | 99.9 |
| Net subscription ARPA (R / month) | 1,355 | 1,441 | 1,546 | 1,640 | 1,784 |
| Founding Member discount cost (R) | 32,143 | 0 | 0 | 0 | 0 |
| Closing cash (R m) / headcount | 18.7 / 13 | 7.5 / 23 | -8.2 / 41 | -16.8 / 67 | -9.7 / 70 |

Paying workspaces by tier, Sep 2031: Nano 763, Micro 886, Starter 1,142, Growth 1,222, Scale 380, Corporate 24, Agency 203, Custom 8.

**Cash (Base)**

| Output | Value |
|---|---|
| Seed | R25.0M (≈US$1.35M), lands Feb 2027 `[[CONFIRM]]` |
| Series A | none (input kept at R0) |
| Pre-seed bridge required | **R66,279**: cash dips to -R66k in Jan 2027 on R500k opening cash `[[CONFIRM]]` |
| First month below the R3.0M buffer | **Jan 2029** |
| Cash runs out (below zero) | **Mar 2029**, 25 months after the seed |
| Minimum cash | **-R17.00M in Nov 2030** |
| Funding gap | **R20.0M** to hold the R3.0M buffer; R17.0M to stay above zero |
| EBITDA break-even | first **Jan 2031**, sustained from Jan 2031 |
| Operating cash flow positive | first **Dec 2030**, sustained from Dec 2030 |
| Market launches | Nigeria **Oct 2028**, Kenya **Jan 2029**, Ghana **Apr 2029**, Rest of Africa (USD) **Nov 2029**, Botswana & Namibia off |
| Profitable on the R25M seed alone | **No** |

## 2. Scenarios

| | Conservative | Base | Upside |
|---|---|---|---|
| Revenue FY1 / FY3 / FY5 (R m) | 1.6 / 14.5 / 43.4 | 1.9 / 25.5 / 93.5 | 2.2 / 44.8 / 179.6 |
| EBITDA FY3 / FY5 (R m) | -9.7 / -9.2 | -16.9 / 4.5 | -15.2 / 19.4 |
| FY5 EBITDA margin | -21% | 5% | 11% |
| Paying workspaces FY5 | 1,906 | 4,627 | 9,847 |
| Headcount FY1 / FY3 / FY5 | 13 / 23 / 48 | 13 / 41 / 70 | 17 / 67 / 135 |
| EBITDA ≥ 0 sustained from | not by Sep 2031 | Jan 2031 | Jul 2030 |
| Operating cash flow ≥ 0 sustained from | not by Sep 2031 | Dec 2030 | Jan 2030 |
| Minimum post-seed cash | -R20.47M (Sep 2031) | -R17.00M (Nov 2030) | -R10.84M (Dec 2029) |
| First month below the buffer | Jun 2029 | Jan 2029 | Sep 2028 |
| Pre-seed bridge | R74.9k | R66.3k | R54.9k |
| Launches NG / KE / GH / Rest | Nov 2029 / Apr 2030 / Sep 2030 / Sep 2031 | Oct 2028 / Jan 2029 / Apr 2029 / Nov 2029 | Apr 2028 / Jul 2028 / Sep 2028 / Mar 2029 |
| Profitable on R25M alone | **No** | **No** | **No** |

Upside fails too: it hires faster (0.80x gates, to the 135-FTE ceiling) and the trough comes in Dec 2029, before revenue catches up.

**Scenario drivers** (columns D:F on Assumptions, switched by the selector in B6; unchanged from v2 except where noted)

| Driver | Conservative | Base | Upside |
|---|---|---|---|
| Sign-up growth m/m, FY1 → FY5 | 10% → 1.0% | 12% → 1.5% | 14% → 2.0% |
| Conversion multiplier (direct paid and Free upgrades) | 0.85x | 1.00x | 1.20x |
| Churn multiplier / paid CAC multiplier | 1.20x / 1.20x | 1.00x / 1.00x | 0.85x / 0.85x |
| Expansion plan shift | +3 months | 0 | -2 months |
| Inbound Corporate & Custom multiplier | 0.5x | 1.0x | 1.5x |
| Paid-acquisition cap (% of last month's net MRR, plus floor) | 30% | 35% | 50% |
| Hiring & launch MRR-gate multiplier | 1.40x | 1.00x | 0.80x |
| FluxMuse fee on checkout GMV | 0% | 0% | **0%** (was 0.75% in v2) |

## 3. Constraint check: does the R25M seed still reach break-even?

The constraint is unchanged: no Series A; closing cash ≥ R3.0M every month from Feb 2027; EBITDA and operating cash flow reach break-even and stay there. The Cash_Flow sheet evaluates it live (`PROFITABLE ON THE SEED ALONE?`) and the Cover repeats it.

| Test | Conservative | Base | Upside |
|---|---|---|---|
| No Series A | Yes | Yes | Yes |
| Cash ≥ R3.0M every month from the seed | No: low -R20.47M, Sep 2031 | No: low -R17.00M, Nov 2030 | No: low -R10.84M, Dec 2029 |
| EBITDA break-even reached and sustained | No | Yes, from Jan 2031 | Yes, from Jul 2030 |
| Operating cash flow positive and sustained | No | Yes, from Dec 2030 | Yes, from Jan 2030 |
| **Result** | **Fail** | **Fail** | **Fail** |

**Honest answer: no.** The base case reaches EBITDA break-even only in Jan 2031, after spending about R20M more than the seed provides (to hold the buffer). It does not reach break-even without a Series A or another source of cash.

**Why v2 passed and v3 does not.** Four changes, all from the current offer, not from tuning:
- **Lower revenue per customer.** Solo buyers now land mostly on Nano (R149) and Micro (R289), not Starter (R499). Solo ARPA falls from about R809 to R291 a month (FY3), and SMEs from R2,769 to R2,024 as Starter joins their mix.
- **Fewer and slower paying customers.** No trial: 5% of Solo and 8% of SME sign-ups pay at once (v2 assumed 11% and 14% trial conversion). Most sign-ups join Free and upgrade slowly (0.5% a month). FY5 paying workspaces: 4,627 against 8,816.
- **Higher AI cost.** The product prices a credit at R0.15 of provider cost. v2 assumed R0.012. FY1-FY2 gross margin is much lower, and the Free plan adds R0.1M-R1.6M a year of cost.
- **The cost base did not change.** The hiring plan, MRR gates, office, G&A and legal base are as in v2. Fixed costs that v2 covered with R73M of FY3 revenue now face R25M.

Partner wholesale at R6,999 (was R5,599) and the new Corporate line help, but agencies and corporates are small in number.

**Levers that would fix it (each moved alone; none adopted).** The build searches for the smallest single change that passes the test:

| Lever | Value that passes | What it means |
|---|---|---|
| Hiring & launch MRR-gate multiplier | **2.05x** (Base is 1.00x) | Hire each role at about twice the MRR. Break-even Sep 2030, low cash R3.08M (Jul 2030), FY5 revenue R74.7M, FY5 EBITDA R10.3M, FY5 headcount 48, Nigeria Oct 2029 |
| Uniform non-founder salary cut | **32%** | Break-even May 2030, low cash R3.08M (Mar 2030) |
| Sign-up volume | **3.25x** plan | About 490 South African sign-ups in Oct 2026 instead of 150 |
| Conversion (direct paid and Free upgrades) | **3.05x** | e.g. Solo 15% and SME 24% paying at sign-up |
| Free-to-paid upgrades | **3.5% a month** (plan 0.5%) | Well above freemium norms |
| Seed size | **R46M** instead of R25M | |
| Extra funding | **R20.0M** | To hold the buffer (R17.0M to stay above zero) |

The most realistic route is a mix: hire on slower gates (the 2.05x result shows hiring pace is the biggest lever), steer Solo sign-ups toward Micro and Starter, and prove that SMEs convert better than assumed before the seed is spent. Volume alone would need more than three times the planned sign-ups.

**Conservative.** As modelled (1.40x gates) cash falls to -R20.47M by Sep 2031. Smallest single fixes: a 2.75x gate multiplier, or a 35% cut to every non-founder salary.

**Pre-seed bridge.** Every scenario needs R55k-R75k before the seed lands (lowest cash Jan 2027). Opening cash above about R570k, a founder loan or an earlier close would cover it.

## 4. How v3 works

**Timing and lean mode.** Month 1 is Oct 2026. South Africa sells from Oct 2026. Until the seed lands (month 5 = Feb 2027) the model runs the two founders at reduced salaries (R45k and R55k CTC), lean hosting (R15k a month), lean overheads (R15k a month), software tools and the first-group set-up (R10k a month, Oct 2026-Jan 2027). There is no paid marketing, hiring, office, travel or legal retainer before the seed.

**First group set up by hand.** There is no pilot and no free period. The founders set up a small first group of South African businesses by hand: 4 a month from Oct 2026 to Jan 2027 (16 in total), half Solo and half SMEs, each taking its segment's tier mix `[[CONFIRM]]`. They pay list price less Founding Member from the first bill.

**Self-serve funnel: sign-ups, direct paid, Free plan.**
- **Sign-ups.** South Africa starts with 150 self-serve sign-ups (Free and paid accounts) in Oct 2026 `[[CONFIRM]]`, growing 12% a month in FY1 (Base). Before the seed these are organic only.
- **Pay at sign-up.** 5% of Solo and 8% of SME sign-ups pay at once `[[CONFIRM]]`. Paid acquisition, the cap and the payback test apply to these.
- **Free plan.** Everyone else joins Free (permanent plan, no card). Active Free users upgrade at 0.5% a month and go dormant at 10% a month `[[CONFIRM]]`, which is about 5% lifetime conversion. Upgrades split Solo/SME like sign-ups and need no paid acquisition.
- **Free cost.** Each active Free user uses 60 AI credits a month at 40% utilisation (R3.60 at R0.15 a credit) plus R3 of hosting and messaging `[[CONFIRM]]`. Dormant users cost nothing.

**AI credit cost: which number is right.** CURRENT_OFFER §1 says "1 credit is about R1 of real provider cost"; the platform guide says R0.15. The product code settles it: `supabase/functions/_shared/ai-credit-math.ts` sets `DEFAULT_ZAR_PER_CREDIT = 0.15` ("1 credit = R0.15 of real provider cost, founder decision 2026-09-25"), and migration `20260926110000_ai_credit_metering.sql` seeds `platform_billing_config ai.zar_per_credit = 0.15`. **The model uses R0.15.** The "about R1" line in CURRENT_OFFER is out of date and should be corrected there. The Free allowance is **60 credits**, not 100: `20260926100000_credit_allowances_and_voice_plans.sql` cut it from the 100 set on 18 Sep. Paid allowances used for cost only (never quoted): Nano 450, Micro 900, Starter 1,500, Growth 6,500 (incl. the 500 bonus), Scale 15,500 (incl. the 2,000 bonus, which the migration describes as cost-equivalent to the outbound voice minutes). Corporate, Agency and Custom run AI on the customer's own keys, so they carry no AI credit cost. Credit packs: R300 for 1,000 credits, no overage on paid plans.

**Segments and tiers.**

| | Solo | SMEs | Agencies | Corporate | Enterprise (Custom) |
|---|---|---|---|---|---|
| Acquisition | pay at sign-up 5% + Free upgrades | pay at sign-up 8% + Free upgrades | 0.5 inbound a month in SA + 1.5 per partnerships manager; 0.4 per NG/KE/GH country lead + inbound | inbound only, SA: 1 / 3 / 6 / 9 / 12 deals a year | inbound only, SA: 0 / 1 / 2 / 3 / 4 a year |
| Tier mix | 45% Nano / 40% Micro / 15% Starter | 40% Starter / 50% Growth / 10% Scale | Agency at partner wholesale R6,999 | Corporate R6,999 | Custom, modelled at R19,999 |
| Upgrades a month | Nano → Micro 1.5%; Micro → Starter 0.8% | Starter → Growth 1.0%; Growth → Scale 0.6% | none | none | none |
| Monthly churn | Nano 8.0% / Micro 7.0% / Starter 6.0% | Starter 4.5% / Growth 3.0% / Scale 2.2% | 2.0% | 1.5% | 1.0% |
| Paid CAC | R1,500 | R6,500 | partner programme + team | R10k handling per deal | R25k handling per deal |

**Founding Member.** 30% off the first 2 monthly bills for South African Solo and SME sign-ups (Nano to Scale), including the first group and Free users who upgrade while it runs. It has been live since 1 Oct 2026 with no end date; the model ends it on **31 Mar 2027** `[[CONFIRM]]`, a month after the seed lands. It is not modelled on Agency (it doesn't stack with wholesale), Corporate, Custom or annual plans `[[CONFIRM]]`. 8% of new sign-ups churn before the second discounted bill. Sign-ups rise **+20%** while it runs `[[CONFIRM]]` (unchanged from v2, unproven). Total cost: **R32,143**, all in FY1 (1.9% of FY1 gross subscriptions). With no offer, minimum cash is R49k lower, because the assumed uplift slightly outweighs the discount. Nigeria, Kenya and Ghana get no launch window: the live promotion is South Africa only, and an NG/KE/GH offer is undecided and not modelled.

**Markets.** South Africa only until NG/KE/GH checkout is live (Fincra and pawaPay accounts pending). New planned earliest months `[[CONFIRM]]`: Nigeria **Apr 2028**, Kenya **Jul 2028**, Ghana **Oct 2028** (v2: Nov 2027 / Feb 2028 / May 2028), Rest of rail-covered Africa (19 USD countries, self-serve) **May 2029** (v2: Nov 2028). Each also waits for its MRR gate (R0.9M / R1.2M / R1.5M / R2.5M x the scenario multiplier), and the launch follows the decision by 2 months. In Base the gates bind, so the actual launches are later: Oct 2028 / Jan 2029 / Apr 2029 / Nov 2029. Country costs are unchanged from v2: country lead 2 months before launch; local sales and CS at launch; launch marketing NG R350k, KE R300k, GH R250k over 3 months; one-off compliance R300k / R250k / R200k; monthly compliance R12k / R12k / R10k. Rest of Africa: R150k of tax registrations, R20k a month compliance and R20k a month marketing. Botswana & Namibia stay off (coming soon).

**Prices outside South Africa.** NG/KE/GH and the 19 USD markets book the live `tier_regional_prices` (migrations `20260911190000` and `20260918010100`) converted at 1 ZAR = ₦82.83 / KSh 8.07 / GH₵ 0.68 and R18.50 = US$1:

| Tier | ZAR | NGN | KES | GHS | USD |
|---|---|---|---|---|---|
| Nano | 149 | 12,000 | 1,199 | 99 | 8 |
| Micro | 289 | 24,000 | 2,299 | 199 | 16 |
| Starter | 499 | 41,000 | 3,999 | 339 | 27 |
| Growth | 1,999 | 165,000 | 15,999 | 1,359 | 109 |
| Scale | 4,999 | 413,000 | 39,999 | 3,399 | 269 |
| Corporate | 6,999 | 579,000 | 56,999 | 4,799 | 379 |
| Agency | 9,999 | 829,000 | 80,999 | 6,799 | 539 |
| Custom (from) | 19,999 | 1,650,000 | 161,000 | 13,600 | 1,099 |
| Partner wholesale | 6,999 | 579,000 | 56,999 | 4,799 | 379 |

There are no regional wholesale prices in the product. The model uses the Corporate local prices, which are the same 70% of Agency list `[[CONFIRM]]`. FX drift (NGN -10%, GHS -8%, KES -3%, USD 0% a year vs ZAR `[[CONFIRM]]`), quarterly repricing at >10% drift and the 6% October escalator are unchanged. Annual billing is 10x monthly; 25% of subscriptions are annual.

**No VAT.** Fluxmuse (Pty) Ltd is not VAT-registered. List prices are the amounts charged and revenue is booked as charged: no VAT is added, grossed up or deducted anywhere. (v2 also had no VAT gross-up; v3 says so on the Assumptions sheet and in the P&L labels.)

**Commerce.** CURRENT_OFFER §2: checkout fees are pass-through (Paystack 2.9% + R1 on cards, 2% EFT), deducted before payout, with no FluxMuse service fee. The FluxMuse fee is **0% in every scenario** `[[CONFIRM]]` (v2 had 0.75% in Upside). Checkout GMV stays as a memo row. Payment processing on FluxMuse's own subscriptions is 3.0% (Paystack 2.9% + R1 at FluxMuse's ARPA) `[[CONFIRM]]`.

**Other revenue.** AI-credit packs: 5% of metered workspaces (Nano to Scale) buy one R300 pack a month `[[CONFIRM]]` (v2: 10% buying R350). WhatsApp template messages resold at Meta cost +25% (Micro 50 and Corporate 1,500 messages a month added `[[CONFIRM]]`). Custom setup fee R25,000 a deal `[[CONFIRM]]`. The R4,999 agency setup fee is removed because it is not in the live price list `[[CONFIRM]]`. Campaign Financing excluded.

**Cost discipline.** Unchanged from v2. Every non-founder hire waits for its earliest month, the seed, and last month's net MRR ≥ gate x scenario multiplier. Paid spend = MIN(desired, R40k floor + 35% of last month's MRR in Base), switched off where CAC payback exceeds 12 months `[[CONFIRM]]`. Brand = MIN(ceiling, R25k + 4% of MRR).

## 5. Use of funds (R25M) against modelled spend

The allocation is unchanged: 40 / 30 / 15 / 15 = R10.0M / R7.5M / R3.75M / R3.75M.

| Category | Allocation | Spend, 18 months (Feb 2027-Jul 2028) | Share, 18 months | Spend, 24 months (Feb 2027-Jan 2029) | Share, 24 months | Gap at 24 months |
|---|---|---|---|---|---|---|
| Product & engineering | 40% | R11.17M | 45.7% | R17.60M | 43.1% | +3.1 pp |
| Sales & marketing / partner programme | 30% | R6.91M | 28.3% | R10.90M | 26.7% | -3.3 pp |
| NG/KE/GH expansion & payments compliance | 15% | R0.36M | 1.5% | R2.38M | 5.8% | **-9.2 pp** |
| Operations & working capital | 15% | R6.00M | 24.6% | R9.91M | 24.3% | **+9.3 pp** |
| Total gross spend | | R24.43M | | R40.79M | | |
| less revenue collected | | R8.93M | | R17.43M | | |
| **Net cash consumed from the seed** | | **R15.51M** | | **R23.36M** | | |
| Seed remaining at the end of the window | | R9.49M | | R1.64M | | |

Expansion spend is low because NG/KE/GH now start late in the 24-month window. Operations runs over 15% because customer success, hosting, AI and support scale with customers. After 24 months only R1.6M of the seed is left, which is why cash breaks the buffer in Jan 2029.

## 6. FX shock: ZAR 15% stronger (Base)

The shock now applies from Apr 2029 (month 31), after the later NG/KE/GH plan months.

| Output | Base | ZAR +15%, repricing on | ZAR +15%, no repricing |
|---|---|---|---|
| FY3 revenue | R25.49M | R25.44M (-R0.05M) | R24.98M (-R0.51M) |
| FY5 revenue | R93.52M | R93.66M (+R0.14M) | R86.12M (-R7.40M) |
| FY5 EBITDA | R4.50M | R4.47M (-R0.03M) | -R0.88M (-R5.38M) |
| Minimum post-seed cash | -R17.00M (Nov 2030) | -R16.47M (Nov 2030) | -R20.08M (Mar 2031) |

Repricing discipline is still the main FX control: without it, FY5 EBITDA turns negative and the funding gap grows by about R3.1M.

## 7. Unit economics, FY3 (Base)

| Segment | ARPA (R / month, gross) | Monthly churn | LTV | CAC | LTV:CAC | Payback |
|---|---|---|---|---|---|---|
| Solo | 291 | 7.3% | R2,659 | R3,760 | **0.7x** | 19.3 months |
| SMEs | 2,024 | 3.5% | R39,214 | R5,957 | 6.6x | 4.4 months |
| Agencies (partner wholesale) | 7,453 | 2.0% | R245,679 | R33,673 | 7.3x | 6.8 months |
| Corporate (inbound) | 7,536 | 1.5% | R335,754 | R10,000 | 33.6x | 2.0 months |
| Enterprise / Custom (inbound) | 21,535 | 1.0% | R1.44M | R25,000 | 57.6x | 1.7 months |
| **Blended** | 1,546 (net) | | R19,908 | R6,272 | **3.2x** | **6.1 months** |

- LTV = ARPA x software gross margin (66.8% in FY3) ÷ monthly logo churn.
- Solo/SME CAC = paid spend plus a share of brand, launch and marketing payroll, split by new-customer mix (Free upgrades and the first group count as new customers).
- **Solo does not pay back on fully loaded CAC.** Its paid CAC (R1,500) passes the 12-month payback test, but with shared marketing cost Solo LTV:CAC is 0.7x. Solo customers are worth having through the Free plan and upgrades, not through paid acquisition at scale.

## 8. Changes from v2, and why

| Area | v2 (11 Sep 2026) | v3 (5 Oct 2026) | Why |
|---|---|---|---|
| Tiers | 5: Starter, Growth, Scale, Agency R7,999, Enterprise from R19,999 | 9: Free, Nano R149, Micro R289, Starter R499, Growth R1,999, Scale R4,999, Corporate R6,999, Agency R9,999, Custom (from R19,999) | Live `subscription_tiers` (18 Sep bands) |
| Local prices | 5 tiers | all 8 paid tiers from `tier_regional_prices` | Live product |
| Trials & pilot | 14-day trials (Solo 11%, SME 14%); 12-brand pilot free Oct-Nov, 75% convert 1 Dec at 50% off | no trials, no pilot; pay at sign-up (5% / 8%); first group of 4 a month set up by hand Oct 2026-Jan 2027 | 25 Sep "pay first"; no pilot exists |
| Free plan | not modelled | funnel stage: 0.5% a month upgrade, 10% dormancy, AI and hosting cost | Live permanent Free plan |
| SA launch | 1 Dec 2026 | Oct 2026 (month 1) | Paid plans live now |
| Segments | Solo 90% Starter / 10% Growth; SME 85% Growth / 15% Scale; Enterprise | Solo Nano/Micro/Starter; SME Starter/Growth/Scale; new Corporate line; Custom | New bands |
| Founding Member | ZA 1 Dec 2026-31 Jan 2027 + NG/KE/GH 60-day windows; annual +2 months; option A as sensitivity | ZA only, Oct 2026-Mar 2027 (proposed end); monthly plans only; A removed | Live promotion (1 Oct) |
| Partner wholesale | R5,599 | R6,999 | Confirmed 1 Oct |
| Markets | NG Nov 2027, KE Feb 2028, GH May 2028, Rest Nov 2028 (plan) | NG Apr 2028, KE Jul 2028, GH Oct 2028, Rest May 2029 (plan) | NG/KE/GH checkout not live |
| AI cost | R12 per 1,000 credits; large allowances | R150 per 1,000 (R0.15 a credit); live allowances; own keys on Corporate/Agency/Custom | `ai-credit-math.ts`, platform_billing_config |
| Top-ups | 10% buy R350 (14,000 credits) | 5% of metered plans buy R300 (1,000 credits) | Live packs, no overage |
| Commerce fee | 0.75% in Upside | 0% everywhere | Pass-through fees, no FluxMuse fee |
| Setup fees | Enterprise R25k, Agency R4,999 | Custom R25k, Agency 0 | Not in the live price list |
| Solo paid CAC | R2,200 | R1,500 | Cheaper entry-tier buyers |
| Processing | 2.9% | 3.0% | Paystack 2.9% + R1 |
| FX shock month | Oct 2028 | Apr 2029 | Later launches |
| Hiring, gates, cap, seed, buffer, use of funds | | unchanged | Not tuned |
| Base result | FY5 R238.0M, EBITDA 28%, break-even Mar 2029, low cash R7.96M; passes | FY5 R93.5M, EBITDA 5%, break-even Jan 2031, low cash -R17.0M; **fails** | Lower ARPA, no trial, higher AI cost, same cost base |

## 9. Every new or changed assumption (`[[CONFIRM]]` on the Assumptions sheet)

| Assumption | Value | Why this value |
|---|---|---|
| Seed month | Feb 2027 (unchanged) | No pilot results gate it now; kept for comparability |
| First group | 4 a month, Oct 2026-Jan 2027, 50% Solo, R10k a month set-up | Founders can onboard about one business a week by hand alongside the build |
| SA sign-ups at launch | 150 a month | Organic only before the seed; below v2's 250 trials |
| Pay at sign-up | Solo 5%, SME 8% | Below v2's trial conversion; pay-first plans convert less up front |
| Free upgrade / dormancy | 0.5% / 10% a month | About 5% lifetime, the top of the 2-5% freemium range |
| Free hosting | R3 per active Free user a month | Small: one channel, few posts |
| Solo mix | 45% Nano, 40% Micro, 15% Starter | "Mostly Nano/Micro with some Starter" |
| SME mix | 40% Starter, 50% Growth, 10% Scale | Starter is now the SME entry; Scale is a step up |
| Upgrades | Nano → Micro 1.5%, Micro → Starter 0.8%, Starter → Growth 1.0%, Growth → Scale 0.6% a month | Small price steps upgrade faster |
| Churn | Nano 8.0%, Micro 7.0%, Solo Starter 6.0%, SME Starter 4.5%, Corporate 1.5% | Cheaper plans churn more; Corporate between Agency and Custom |
| Corporate deals | 1 / 3 / 6 / 9 / 12 a year | New BYOC tier for multi-brand groups, inbound only |
| Custom deals | 0 / 1 / 2 / 3 / 4 a year (was 1 / 2 / 4 / 6 / 8) | Corporate now takes the smaller enterprise deals |
| Custom price | R19,999 (from) | As before; Custom is by consultation |
| Custom setup fee | R25,000 | As before; not in the public list |
| Corporate handling | R10,000 a deal | Lighter than Custom |
| Founding Member end | 31 Mar 2027 | No end date set; six months covers the seed close |
| Founding Member scope | Solo & SME monthly plans only | Agency is excluded by rule; Corporate and annual unclear |
| Founding Member uplift | +20% | Unchanged, unproven |
| NG / KE / GH / Rest plan months | Apr 2028 / Jul 2028 / Oct 2028 / May 2029 | About five months later than v2; needs Fincra/pawaPay live and SA MRR |
| NG/KE/GH launch offer | none | Live promotion is SA only |
| Local wholesale prices | Corporate local prices | No regional wholesale rows in the product |
| FluxMuse checkout fee | 0% | Pass-through only |
| Agency setup fee | 0 | Not in the live list |
| Pack attach | 5% of metered workspaces | Allowances are now sized for normal use |
| WhatsApp messages | Micro 50, Corporate 1,500 a month | Micro has one WhatsApp number; Corporate like Agency |
| Solo paid CAC | R1,500 | Entry-tier buyers on Meta/TikTok/WhatsApp |
| Processing | 3.0% | Paystack 2.9% + R1 |
| FX shock month | Apr 2029 | After the new plan months |
| Opening cash, FX depreciation, payback limit | unchanged | Still need confirmation |

## 10. Known limitations

- **Volume and conversion are guesses.** There are no paying customers. The Base Sensitivity grid shows no churn x volume cell that passes: even at 0.7x churn and 1.3x volume, minimum cash is -R8.75M.
- **Free conversion matters.** At 0.25% a month minimum cash is -R21.7M and FY5 EBITDA -R2.3M; at 1.0% it is -R10.2M and +R15.2M. Measure it from the first month.
- **Simplified dynamics.** Customers are fractional; launch and hiring decisions are one-way; gates use last month's MRR. No downgrades. Free users who go dormant never come back. Sign-ups that pay at once and Free users split Solo/SME by the same share.
- **AI cost.** Utilisation (40%) is assumed; the R0.15 peg is the platform's own figure, not a measured average. AI Voice minutes on Corporate/Agency prepaid balances are neither revenue nor cost here.
- **Founding Member.** The +20% uplift and 8% churn between bills are assumptions; annual-plan treatment is unconfirmed.
- **Accounting simplifications.** Tax ignores SA's 80% assessed-loss cap; D&A, interest and payables are ignored; receivables and deferred revenue are simplified. No VAT because FluxMuse is not registered; registration (compulsory above R1M taxable supplies in 12 months, which Base passes late in FY1) would change pricing or margin. Flag for the founder.
- **WhatsApp pass-through is booked as gross revenue**, which lowers blended gross margin; software GM is shown separately.
- **Static windows.** Use_of_Funds windows and Sensitivity values are fixed at build time; rerun the build after changing inputs.

## 11. Replace with live data first (in order)

1. **Pay-at-sign-up rates and Free upgrade rate** (5% / 8% / 0.5% a month). These decide whether the seed is enough.
2. **Sign-up volume** (150 a month in SA at launch) and its growth.
3. **Tier mix of new paying customers**, especially the Nano share, and early churn by tier.
4. **Founding Member effect** on sign-ups, measured Oct 2026-Mar 2027.
5. **AI-credit utilisation** by tier and on Free, against the R0.15 peg.
6. **Agency and Corporate demand**: agencies per partnerships manager, Corporate inbound deals.
7. **NG/KE/GH**: Fincra/pawaPay go-live dates, then sign-ups, CAC and churn after launch.

## 12. Founder confirmations needed

- **Cash and seed.** Opening cash at 1 Oct 2026 (R500k) and how to cover the R66k pre-seed bridge; seed month (Feb 2027) and instrument.
- **The seed test.** The Base case needs about R20M more, or a lever from §3. Decide which: slower hiring gates (2.05x), a smaller cost base, a larger raise (about R46M), or a planned Series A or bridge.
- **First group** size, mix and set-up cost.
- **Funnel**: sign-ups at launch, pay-at-sign-up rates, Free upgrade and dormancy rates, Free hosting cost.
- **Mixes, upgrades and churn** for the new tiers, and the Corporate and Custom deal volumes.
- **Founding Member**: end date (proposed 31 Mar 2027), Corporate and annual-plan eligibility, the +20% uplift, and whether NG/KE/GH get a launch offer.
- **Markets**: the new NG/KE/GH/Rest plan months and their dependence on Fincra/pawaPay.
- **Pricing**: Custom at R19,999, Custom setup fee, local partner wholesale prices, no agency setup fee, 0% checkout fee, 5% pack attach.
- **CURRENT_OFFER §1 correction**: the product prices a credit at R0.15 of provider cost, not about R1, and the Free allowance is 60 credits.
- **Unchanged items still open**: FX depreciation and repricing policy; MRR gates, multipliers, paid cap and 12-month payback limit; salaries and hiring plan; TAM/SAM/SOM before external use.

## 13. `model_summary.json`: keys changed or removed in v3

Readers of the JSON (business plan, investor deck, `_build/business_plan/derive_model_tables.py`) should note:

- **Removed:** `pilot` (whole block); `pilot_conversion_sensitivity` (replaced by `free_conversion_sensitivity`); `annual[].pilot_discount_zar`; `founding_member.breaks_r25m_profitability`; `price_tables.pilot_first_2_bills_zar`; `monthly_base.markers.pilot_last_month_index` and `pilot_conversion_month_index` (replaced by `first_group_last_month_index`).
- **Renamed:** tier `Enterprise` → `Custom` in every tier-keyed map (`annual[].ending_customers_by_tier`, `price_tables.zar_list_monthly`, `price_tables.local_monthly.*`, `price_tables.zar_value_at_parity.*`, `unit_economics_fy3.by_tier`). The **segment** is still called `Enterprise`.
- **Narrowed:** `founding_member.windows`, `founding_member.discount_cost_by_market_fy_zar`, `annual[].founding_member_discount_by_market_zar` and `monthly_base.markers.founding_member_window_indices` now hold South Africa only (Nigeria, Kenya, Ghana removed). `founding_member.option_comparison` keys are now `Founding Member (default)` and `None` (was `B Founding Member (default)`, `A Launch Sprint`, `None`).
- **Added:** segment `Corporate` in every segment-keyed map; tiers `Nano`, `Micro`, `Corporate`, `Custom`; `Free` in `price_tables.zar_list_monthly`; `annual[].free_plan`; top-level `free_plan`, `first_group`, `base_levers_to_pass_r25m_test`, `free_conversion_sensitivity`; `monthly_base.active_free_users`; `price_tables.bands`, `custom_modelled_as`, `vat`, `partner_wholesale_monthly.local_basis`.
- **Meaning changed, same key:** `profitable_on_seed_alone` is now `false` in every scenario; `annual[].revenue_by_stream_zar.ai_credit_topups` is now credit-pack revenue; `commerce_platform_fees` is 0 in every scenario; `markets.launch_months.*.South Africa` is `Oct 2026`.
