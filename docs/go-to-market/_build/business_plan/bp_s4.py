"""Sections 12-13: financial plan, funding request and use of funds."""
from bp_doc import ANN, BASE, D, M, TINT, ann, pct, rand, rk, rm, usd

CASH = M["cash"]
UOF = M["use_of_funds"]
REC = UOF["reconciliation"]
UE = M["unit_economics_fy3"]
SC = M["scenarios"]
SENS = M["sensitivity_base"]
FX = M["fx_shock"]["results"]
CD = M["conservative_diagnostics"]
FM = M["founding_member"]


def s12_financials(d):
    d.h1("12. Financial plan", new_page=True)
    d.para("Every figure in this section comes from the **FluxMuse Financial Model v2** (model date "
           "11 September 2026), Base case unless stated. The workbook carries the monthly build; this section "
           "summarises it. **These are forward-looking projections, not results**, and the assumptions most "
           "likely to move are listed in Appendix E.")

    d.h2("Key assumptions")
    d.bullets([
        "**Timing.** Month 1 is October 2026; the fiscal year runs October to September. The R25m seed is "
        "modelled to land in **February 2027**. Until then the business runs lean: two founders on reduced "
        "salaries, lean hosting and overheads, pilot costs, and no paid marketing or hiring.",
        "**Pilot.** 12 Gauteng brands pay nothing in October and November 2026; 75% convert on 1 December 2026 "
        "at pilot prices for two bills. South Africa launches commercially on 1 December 2026.",
        "**Pricing.** ZAR list prices; fixed local price points in Nigeria, Kenya and Ghana; US dollars in the "
        "other 19 rail-covered countries. Annual plans are 10× monthly and are 25% of subscriptions. A 6% list "
        "escalator applies each October.",
        "**Segments.** Self-serve trials split 65% solo and 35% SME, converting at 11% and 14%. Agencies come "
        "through the partner programme and country leads. Enterprise is inbound only.",
        "**Cost discipline.** Hiring and market launches wait for net MRR gates; paid acquisition is capped at "
        "R40,000 plus 35% of last month's net MRR; paid spend switches off where CAC payback would exceed "
        "12 months.",
        "**Funding.** The R25m seed only. The Series A input is kept at zero in every scenario.",
        "**Tax** at 27%, and only once cumulative EBITDA turns positive. Depreciation, amortisation and "
        "interest are ignored.",
    ])

    d.h2("Revenue build")
    d.para("Revenue is mostly recurring subscriptions, plus AI-credit top-ups, WhatsApp messaging resold at "
           "Meta cost plus a margin, and setup fees. There is no commerce fee in the Base case.")
    d.figure("charts/revenue_by_stream_fy1_fy5.png",
             "Revenue by stream, FY1–FY5 (Base case), net of launch discounts.",
             "Stacked bar chart of revenue by stream rising from R3.4 million in FY1 to R238.0 million in FY5, "
             "dominated by subscriptions, with smaller AI-credit top-up, WhatsApp messaging and setup-fee "
             "layers.")
    d.fy_table("Revenue by stream (R million, Base case)", [
        ["Subscriptions (net)"] + [rm(a["revenue_by_stream_zar"]["subscriptions"]) for a in ANN],
        ["AI-credit top-ups"] + [rm(a["revenue_by_stream_zar"]["ai_credit_topups"], 2) for a in ANN],
        ["WhatsApp messaging"] + [rm(a["revenue_by_stream_zar"]["whatsapp_messaging"], 2) for a in ANN],
        ["Setup fees (enterprise and agency)"] +
        [rm(a["revenue_by_stream_zar"]["enterprise_setup_fees"] + a["revenue_by_stream_zar"]["agency_setup_fees"], 2)
         for a in ANN],
        ["**Total revenue**"] + [rm(a["total_revenue_zar"]) for a in ANN],
        ["Total revenue (US$ m)"] + [f"US${a['total_revenue_usd'] / 1e6:,.2f}m" for a in ANN],
        ["Growth on prior year"] + ["n/a"] + [pct(a["revenue_growth_pct"]) for a in ANN[1:]],
    ], total_rows=(4,))
    d.source()
    d.figure("charts/arr_and_customers.png",
             "Subscription ARR and paying workspaces at each year end (Base case).",
             "Two bar charts: subscription ARR rising from R8.1 million in FY1 to R249 million in FY5, and "
             "paying workspaces rising from 421 to 8,816.")
    d.figure("charts/customers_by_segment.png",
             "Paying workspaces by segment (Base case).",
             "Stacked bars of paying workspaces by segment from 422 in FY1 to 8,816 in FY5, with solo at 4,173 "
             "and SMEs at 4,305 by FY5, agencies 321 and enterprise 17.")
    d.figure("charts/customers_by_region.png",
             "Paying workspaces by market (Base case). Gated countries are zero throughout.",
             "Area chart of paying workspaces by market to September 2031: South Africa 5,724, Nigeria 1,275, "
             "Kenya 837, Ghana 548 and Rest of Africa in US dollars 433, about 35% outside South Africa.")

    d.h2("Profit and loss summary")
    d.fy_table("P&L summary (R million, Base case)", [
        ["Revenue"] + [rm(a["total_revenue_zar"]) for a in ANN],
        ["Cost of revenue"] + [rm(v) for v in D["annual"]["a_cogs"]],
        ["**Gross profit**"] + [rm(a["gross_profit_zar"]) for a in ANN],
        ["Gross margin"] + [pct(a["gross_margin_pct"]) for a in ANN],
        ["Software gross margin"] + [pct(a["software_gross_margin_pct"]) for a in ANN],
        ["Operating expenses"] + [rm(a["opex_zar"]["total"]) for a in ANN],
        ["**EBITDA**"] + [rm(a["ebitda_zar"]) for a in ANN],
        ["EBITDA margin"] + ["n/m"] + [pct(a["ebitda_margin_pct"]) for a in ANN[1:]],
        ["Tax"] + [rm(a["tax_zar"], 2) for a in ANN],
        ["**Net income**"] + [rm(a["net_income_zar"]) for a in ANN],
    ], total_rows=(2, 6, 9))
    d.source()
    d.note("Blended gross margin is held down by WhatsApp messaging, which is booked gross as revenue and "
           "cost; the software gross margin line shows the underlying platform margin.")

    d.h2("Cash flow and funding")
    d.fy_table("Cash flow summary (R million, Base case)", [
        ["Opening cash"] + [rm(v) for v in D["opening_cash_fy"]],
        ["EBITDA"] + [rm(a["ebitda_zar"]) for a in ANN],
        ["Tax paid"] + [rm(v) for v in D["cash_flow_rows_fy_sum"]["cf_tax"]],
        ["Working capital movement"] +
        [rm(dr - ar, 2) for dr, ar in zip(D["cash_flow_rows_fy_sum"]["d_dr"], D["cash_flow_rows_fy_sum"]["d_ar"])],
        ["**Operating cash flow**"] + [rm(a["operating_cash_flow_zar"]) for a in ANN],
        ["Equity funding (seed)"] + [rm(a["equity_funding_zar"]) for a in ANN],
        ["**Closing cash**"] + [rm(a["closing_cash_zar"]) for a in ANN],
        ["Lowest month-end cash in year"] + [rm(a["min_month_end_cash_zar"], 2) for a in ANN],
    ], total_rows=(4, 6))
    d.source()
    d.figure("charts/cash_runway_r25m.png",
             "Monthly closing cash against the R3.0m minimum-cash buffer (Base case). No Series A.",
             "Line chart of monthly closing cash from October 2026 to September 2030: a small pre-seed dip, the "
             "R25 million seed landing in February 2027, a decline through the Nigeria, Kenya and Ghana "
             "launches to a post-seed low of R7.96 million in September 2028, R4.96 million above the R3.0 "
             "million buffer, then recovery past EBITDA break-even in March 2029.")
    d.bullets([
        f"**Pre-seed bridge: {rand(CASH['pre_seed_bridge_required_zar'])}.** On opening cash of "
        f"{rand(CASH['opening_cash_zar'])} (**[[CONFIRM OPENING CASH]]**), cash dips to "
        f"−{rk(abs(CASH['min_cash_zar']))} in {CASH['min_cash_month']}, one month before the seed lands.",
        f"**Minimum cash after the seed: {rm(CASH['min_post_seed_cash_zar'], 2)} in "
        f"{CASH['min_post_seed_cash_month']}**, which is {rm(CASH['headroom_over_buffer_zar'], 2)} above the "
        f"{rm(CASH['min_cash_buffer_zar'], 1)} buffer. The plan never goes below the buffer.",
        f"**Runway at the seed close: about {CASH['runway_at_seed_close_months']:.0f} months** at the average "
        f"net burn of the following year ({rand(CASH['avg_monthly_net_burn_12m_after_seed_zar'])} a month). "
        "Cash is not exhausted within the 60-month horizon.",
    ])

    d.h2("Break-even")
    d.figure("charts/ebitda_and_cash.png",
             "Monthly EBITDA and closing cash (Base case).",
             "Two panels: monthly EBITDA turning positive at break-even in March 2029 and rising through FY5, "
             "and closing cash dipping to a post-seed low of R7.96 million in September 2028 before rising to "
             "about R104 million by the end of FY5, always above the R3.0 million buffer.")
    d.table(["Milestone", "Base case"], [
        ("First month of positive EBITDA", CASH["break_even_month"]),
        ("EBITDA positive every month from", CASH["break_even_month_sustained"]),
        ("First month of positive operating cash flow", CASH["cash_flow_positive_month"]),
        ("Operating cash flow positive every month from", CASH["cash_flow_positive_month_sustained"]),
        ("Profitable on the R25m seed alone", "Yes, in all three scenarios"),
    ], [9.0, 8.0], "Break-even milestones", size=9.5)
    d.note("EBITDA dips again in April and May 2029: net MRR clears the R5m gate and ten people join in one "
           "month, including three scale-up engineers, three marketers, the Head of Sales & Partnerships, a "
           "finance analyst and Kenya's team expansion. It is positive every month from June 2029.")

    d.h2("Unit economics")
    d.figure("charts/unit_economics.png",
             "Lifetime value against acquisition cost by segment, FY3 (Base case).",
             "Four panels comparing LTV and CAC per customer in FY3: solo R9.9k against R3.3k at 3.0 times, "
             "SMEs R73k against R5.7k at 12.8 times, agencies R222k against R37k at 6.0 times, enterprise "
             "R1,655k against R25k; blended LTV R32k, CAC R5.6k, 5.6 times, payback 3.8 months.")
    d.table(["Segment, FY3", "ARPA (R/month)", "Monthly churn", "LTV", "CAC", "LTV:CAC", "Payback"], [
        (name, rand(s["arpa_zar_per_month"]), pct(s["monthly_churn_pct"], 1), rand(s["ltv_zar"]),
         rand(s["cac_zar"]), f"{s['ltv_to_cac']}x", f"{s['cac_payback_months']} months")
        for name, s in UE["by_segment"].items()
    ] + [("**Blended**", rand(UE["blended"]["arpa_zar_per_month"]), "—", rand(UE["blended"]["ltv_zar"]),
          rand(UE["blended"]["cac_zar"]), f"{UE['blended']['ltv_to_cac']}x",
          f"{UE['blended']['cac_payback_months']} months")],
            [3.0, 2.7, 2.3, 2.8, 2.3, 1.7, 2.2], "Unit economics by segment, FY3", size=9,
            aligns=[None, "right", "right", "right", "right", "right", "right"], total_rows=(4,))
    d.source()
    d.bullets([
        "LTV is ARPA × software gross margin ÷ monthly logo churn. Solo and SME CAC includes paid spend plus a "
        "share of brand, launch and marketing payroll; agency CAC is the partner programme plus the "
        "partnerships team.",
        "**Solo is the thin one at 3.0×**, because Starter churn is assumed at 6.5% a month. It is the first "
        "number the pilot must test.",
        "**SMEs carry the economics** at 12.8× with a 2.7-month payback, which is why SME conversion and "
        "retention are the priority metrics in section 15.",
    ])

    d.h2("Scenarios")
    d.figure("charts/scenarios.png",
             "FY5 revenue and EBITDA in all three scenarios, on the R25m seed alone.",
             "Bar chart: Conservative R116 million revenue and R25 million EBITDA at 21%, with 3,974 "
             "workspaces and break-even March 2030; Base R238 million and R66 million at 28%, 8,816 workspaces, "
             "break-even June 2029; Upside R451 million and R223 million at 50%, 17,793 workspaces, break-even "
             "June 2028. All three profitable on the seed alone.")
    d.table(["", "Conservative", "Base", "Upside"], [
        ("Revenue FY1 / FY3 / FY5 (R m)",) + tuple(
            f"{s['revenue_zar_fy1_fy5'][0] / 1e6:.1f} / {s['fy3_revenue_zar'] / 1e6:.1f} / "
            f"{s['fy5_revenue_zar'] / 1e6:.1f}" for s in (SC["Conservative"], SC["Base"], SC["Upside"])),
        ("EBITDA FY3 / FY5 (R m)",) + tuple(
            f"{s['fy3_ebitda_zar'] / 1e6:.1f} / {s['fy5_ebitda_zar'] / 1e6:.1f}"
            for s in (SC["Conservative"], SC["Base"], SC["Upside"])),
        ("FY5 EBITDA margin",) + tuple(pct(s["fy5_ebitda_margin_pct"])
                                       for s in (SC["Conservative"], SC["Base"], SC["Upside"])),
        ("Paying workspaces FY5",) + tuple(f"{s['fy5_paying_workspaces']:,}"
                                           for s in (SC["Conservative"], SC["Base"], SC["Upside"])),
        ("Headcount FY5",) + tuple(str(s["headcount_fy1_fy5"][4])
                                   for s in (SC["Conservative"], SC["Base"], SC["Upside"])),
        ("EBITDA positive every month from",) + tuple(s["breakeven_month_sustained"]
                                                      for s in (SC["Conservative"], SC["Base"], SC["Upside"])),
        ("Minimum cash after the seed",) + tuple(rm(s["min_post_seed_cash_zar"], 2)
                                                 for s in (SC["Conservative"], SC["Base"], SC["Upside"])),
        ("Nigeria / Kenya / Ghana launch",) + tuple(
            f"{s['market_launch_months']['Nigeria']} / {s['market_launch_months']['Kenya']} / "
            f"{s['market_launch_months']['Ghana']}" for s in (SC["Conservative"], SC["Base"], SC["Upside"])),
        ("**Profitable on R25m alone**", "**Yes**", "**Yes**", "**Yes**"),
    ], [5.0, 4.0, 4.0, 4.0], "Scenario comparison", size=9,
        aligns=[None, "right", "right", "right"], total_rows=(8,))
    d.source()
    d.callout("The Conservative case needs cost discipline, and the model says so plainly", [
        "On Base hiring gates, the Conservative case **fails**: cash falls to "
        f"−{rm(abs(CD['with_base_gates_1_00x']['min_post_seed_cash_zar']), 2)} in "
        f"{CD['with_base_gates_1_00x']['min_post_seed_cash_month']}, a "
        f"{rm(CD['with_base_gates_1_00x']['shortfall_vs_buffer_zar'], 2)} shortfall against the buffer.",
        f"- The smallest fixes are to raise the hiring and launch gate multiplier to "
        f"{CD['smallest_gate_multiplier_that_passes']}×, or to cut every non-founder salary by "
        f"{CD['smallest_uniform_non_founder_salary_cut_pct_that_passes']}%.",
        "- The plan adopts **1.40×**, which leaves more headroom. The cost is real: wave-1 launches move to "
        "September 2028 to March 2029 and FY5 headcount falls to 67.",
        "- In other words, a slower market is survived by hiring and launching later, not by raising more.",
    ], fill=TINT, caption="Layout: conservative case callout")

    d.h2("Sensitivities")
    d.para("**Volume is the biggest risk to the cash buffer.** The grid below shows minimum post-seed cash on "
           "Base hiring gates as new-customer volume and churn move.")
    vol = SENS["cols_new_customer_volume_multiplier"]
    grid = SENS["min_post_seed_cash_zar_m"]
    d.table(["Churn ×  /  Volume →"] + [f"{v:.0%}" for v in vol],
            [[f"{SENS['rows_churn_multiplier'][i]:.2f}×"] + [f"R{val:.2f}m" for val in row]
             for i, row in enumerate(grid)],
            [4.2] + [2.56] * 5, "Minimum post-seed cash (R m), Base gates", size=9,
            aligns=[None] + ["right"] * 5, highlight_rows=(2,))
    d.source()
    d.bullets([
        "**Trial volume 30% below plan** takes minimum post-seed cash to **R0.98m**, below the R3.0m buffer. "
        "With churn 15% worse as well it goes slightly negative (−R0.07m).",
        "Volume 15% below plan still passes at R4.15m, and churn 30% worse with volume 15% down just passes at "
        "R3.10m.",
        "**The response is pre-agreed**: if early trials run more than about 20% below plan, the gate "
        "multiplier is raised as in the Conservative case, which delays hiring and launches and protects cash. "
        "This is also why roughly R8m of the seed is deliberately left unspent (section 13).",
    ])
    d.h3("FX shock: the rand 15% stronger")
    d.figure("charts/fx_shock_sensitivity.png",
             "A 15% stronger rand against NGN, KES, GHS and USD from October 2028, with and without the "
             "quarterly repricing policy.",
             "Grouped bars comparing base, shock with repricing and shock without repricing for FY3 revenue, "
             "FY5 revenue, FY3 EBITDA, FY5 EBITDA and minimum post-seed cash. Without repricing FY5 revenue "
             "falls R21.0 million and FY5 EBITDA R9.9 million; with repricing the effect is negligible. "
             "Profitable on the R25 million seed alone in all three cases.")
    d.table(["Outcome", "Base", "Rand +15%, repricing on", "Rand +15%, no repricing"], [
        ("FY3 revenue", rm(FX["Base"]["fy3_revenue_zar"], 2),
         rm(FX["ZAR 15% stronger (repricing on)"]["fy3_revenue_zar"], 2),
         rm(FX["ZAR 15% stronger (no repricing)"]["fy3_revenue_zar"], 2)),
        ("FY5 revenue", rm(FX["Base"]["fy5_revenue_zar"], 2),
         rm(FX["ZAR 15% stronger (repricing on)"]["fy5_revenue_zar"], 2),
         rm(FX["ZAR 15% stronger (no repricing)"]["fy5_revenue_zar"], 2)),
        ("FY5 EBITDA", rm(FX["Base"]["fy5_ebitda_zar"], 2),
         rm(FX["ZAR 15% stronger (repricing on)"]["fy5_ebitda_zar"], 2),
         rm(FX["ZAR 15% stronger (no repricing)"]["fy5_ebitda_zar"], 2)),
        ("Minimum post-seed cash", rm(FX["Base"]["min_post_seed_cash_zar"], 2),
         rm(FX["ZAR 15% stronger (repricing on)"]["min_post_seed_cash_zar"], 2),
         rm(FX["ZAR 15% stronger (no repricing)"]["min_post_seed_cash_zar"], 2)),
        ("Profitable on R25m alone", "Yes", "Yes", "Yes"),
    ], [4.4, 4.2, 4.2, 4.2], "FX shock, Base case", size=9,
        aligns=[None, "right", "right", "right"])
    d.source()
    d.note("Quarterly repricing is the main FX control. Without it, FY5 EBITDA falls by R9.9m; with it, the "
           "shock costs about one quarter of revenue and then resets.")

    d.h3("What the launch and pilot discounts cost")
    d.table(["Launch offer (Base case)", "FY1–FY3 discount cost", "Minimum post-seed cash",
             "Profitable on R25m"], [
        ("Founding Member (the decided offer)",
         rk(FM["option_comparison"]["B Founding Member (default)"]["discount_cost_fy1_fy3_zar"]),
         rm(FM["option_comparison"]["B Founding Member (default)"]["min_post_seed_cash_zar"], 2), "Yes"),
        ("A shorter 30-day alternative (not offered)",
         rk(FM["option_comparison"]["A Launch Sprint"]["discount_cost_fy1_fy3_zar"]),
         rm(FM["option_comparison"]["A Launch Sprint"]["min_post_seed_cash_zar"], 2), "Yes"),
        ("No launch offer", "R0",
         rm(FM["option_comparison"]["None"]["min_post_seed_cash_zar"], 2), "Yes"),
    ], [6.0, 3.8, 3.8, 3.4], "Cost of the launch offer", size=9,
        aligns=[None, "right", "right", "right"])
    d.note("The pilot discount costs a further "
           f"{rand(M['pilot']['pilot_discount_cost_fy1_zar'])} in FY1. Because sign-ups are assumed to rise 20% "
           "inside a window, the Founding Member offer leaves marginally more cash than no offer; that uplift "
           "is the assumption the South African window is there to test.")


def s13_funding(d):
    d.h1("13. Funding request and use of funds", new_page=True)
    d.h2("The ask")
    d.kv_table([
        ("Amount", f"R25,000,000 (about {usd(M['seed_usd'])})"),
        ("Round", "Seed"),
        ("Instrument", "[[INSTRUMENT: SAFE OR PRICED EQUITY]]"),
        ("Valuation", "[[PRE-MONEY VALUATION: TBC]]"),
        ("Modelled close", "February 2027 (model input; an earlier close removes the pre-seed bridge)"),
        ("Follow-on funding", "None required: the Series A input is zero in every scenario"),
        ("Minimum-cash policy", "Closing cash stays at or above R3.0m every month from the seed"),
    ], widths=(4.6, 12.4), caption="Layout: the ask")

    d.h2("Allocation")
    d.table(["Category", "Share", "R", "What it buys and when"], [
        (a["category"], pct(a["share_pct"]), rm(a["amount_zar"], 2), a["what_it_buys"])
        for a in UOF["allocation"]
    ], [3.6, 1.3, 1.8, 10.3], "Use of the R25m seed", size=8.5,
        aligns=[None, "right", "right", None])
    d.figure("charts/use_of_funds.png",
             "The R25m seed by category.",
             "Chart of the use of funds: product and engineering R10.0 million at 40%, sales and marketing "
             "including the partner programme R7.5 million at 30%, market expansion and payments compliance "
             "R3.75 million at 15%, and operations and working capital R3.75 million at 15%.")
    d.para("**Timing.** Product and engineering hires begin in the seed month; growth and partnerships hires "
           "follow immediately; country leads are hired two months before each market launch, and local sales "
           "and customer success at launch. Launch marketing is R350,000 for Nigeria, R300,000 for Kenya and "
           "R250,000 for Ghana, spread over three months each, with one-off compliance of R300,000, R250,000 "
           "and R200,000.")

    d.h2("How the allocation compares with modelled spend")
    d.para("The seed funds **net** burn, not gross spend, because revenue pays for a growing share of costs as "
           "it arrives. The honest way to read the allocation is as a share of what the plan actually spends. "
           f"Over the 24 months from the seed ({REC['24']['window']}):")
    d.table(["Category", "Allocation", "Modelled spend, 24 months", "Share of spend", "Gap"], [
        (c["category"], pct(c["allocation_pct"]), rm(c["modelled_spend_zar"], 2),
         pct(c["share_of_spend_pct"], 1), f"{c['gap_pp']:+.1f} pp")
        for c in REC["24"]["categories"]
    ] + [
        ("**Total gross spend**", "", rm(REC["24"]["total_gross_spend_zar"], 2), "", ""),
        ("less revenue collected", "", rm(REC["24"]["revenue_collected_zar"], 2), "", ""),
        ("**Net cash consumed from the seed**", "", rm(REC["24"]["net_cash_consumed_zar"], 2), "", ""),
        ("**Seed remaining after 24 months**", "", rm(REC["24"]["seed_remaining_zar"], 2), "", ""),
    ], [5.6, 2.2, 3.6, 2.6, 3.0], "Allocation against modelled spend, 24 months", size=9,
        aligns=[None, "right", "right", "right", "right"], total_rows=(4, 6, 7))
    d.source()
    d.para("**Two gaps, stated plainly:**")
    d.bullets([
        "**Expansion is under-spent against its 15% share (9.7% of spend, −5.3 points).** The MRR gates start "
        "the Nigeria, Kenya and Ghana launches 12 to 16 months after close, and country teams are deliberately "
        "small. This is the cost discipline working, not an under-investment we intend to fix by spending "
        "earlier.",
        "**Operations and working capital is over its 15% share (21.6% of spend, +6.6 points).** Customer "
        "success, payment processing, WhatsApp pass-through and support scale with revenue, and revenue funds "
        "them.",
        "The straightforward reading is to treat the split as a **share of spend**, or to move about five "
        "points from expansion to operations. We have not restated the headline split, so that this plan and "
        "the model can be compared line for line.",
    ])

    d.h2("The unspent reserve")
    d.para(f"About **{rm(REC['24']['seed_remaining_zar'], 1)} of the seed is still unspent 24 months after "
           f"close** ({rm(REC['18']['seed_remaining_zar'], 1)} at 18 months). That is deliberate. It is the "
           "downside reserve that keeps the plan self-funded if the market is slower than assumed: in the "
           "−30% trial-volume case, minimum post-seed cash falls from "
           f"{rm(CASH['min_post_seed_cash_zar'], 2)} to about **R0.98m**, and this reserve, together with "
           "raising the hiring and launch gates, is what absorbs that. It is not idle capital looking for a "
           "use; it is the reason no Series A is needed.")

    d.h2("The pre-seed bridge")
    d.para(f"On the modelled February 2027 close and opening cash of {rand(CASH['opening_cash_zar'])}, the "
           f"business needs a bridge of **{rand(CASH['pre_seed_bridge_required_zar'])}** in "
           f"{CASH['min_cash_month']}. It is small and it is not optional. Options are a founder loan, pilot "
           "prepayments, or closing the round earlier. **[[HOW THE PRE-SEED BRIDGE WILL BE COVERED]]**")
    d.note(f"Pilot conversion barely moves it: {rand(M['pilot_conversion_sensitivity']['50% convert']['pre_seed_bridge_required_zar'])} "
           f"at 50% conversion and {rand(M['pilot_conversion_sensitivity']['100% convert']['pre_seed_bridge_required_zar'])} "
           "at 100%. Opening cash above about R560k removes it.")

    d.h2("Investor return considerations")
    d.para("This plan does not propose a valuation or model a return: those are matters for negotiation, and "
           "inventing them here would be false precision. What the plan does say:")
    d.bullets([
        "**The round is sized to reach profitability, not to reach the next round.** All three scenarios reach "
        "sustained EBITDA and operating-cash-flow break-even on this R25m with no Series A, so an investor is "
        "not underwriting a financing risk on top of an execution risk.",
        "**Cash generation starts inside the horizon**: operating cash flow turns positive in "
        f"{CASH['cash_flow_positive_month']} and closing cash reaches {rm(ANN[4]['closing_cash_zar'], 0)} by "
        "the end of FY5 in the Base case.",
        "**Recurring revenue with sound unit economics**: FY3 blended LTV:CAC of "
        f"{UE['blended']['ltv_to_cac']}× with a {UE['blended']['cac_payback_months']}-month payback, and "
        f"subscription ARR of {rm(ANN[4]['subscription_arr_zar'], 0)} by FY5.",
        "**Optionality that is not in the Base case**: the commerce fee, Campaign Financing, Botswana and "
        "Namibia, and any market outside the current 23 are all excluded from these projections.",
        "**Exit routes** are **[[EXIT CONSIDERATIONS: TO BE DISCUSSED WITH INVESTORS]]**. Any Series A would "
        "be optional acceleration rather than survival.",
    ])
