"""Sections 12-13: financial plan, funding request and use of funds."""
from bp_doc import ANN, BASE, D, M, MODEL_LINE, MV, SEED_M, SEED_WORDS, TINT, ann, pct, rand, rk, rm, usd

CASH = M["cash"]
UOF = M["use_of_funds"]
REC = UOF["reconciliation"]
UE = M["unit_economics_fy3"]
SC = M["scenarios"]
SENS = M["sensitivity_base"]
FX = M["fx_shock"]["results"]
CD = M["conservative_diagnostics"]
FM = M["founding_member"]
FP = M["free_plan"]
FCS = M["free_conversion_sensitivity"]
PASS = M["profitable_on_seed_alone"]
CC = M["constraint_checks"]
SS = M["seed_sizing"]
NAMES = ("Conservative", "Base", "Upside")


def yn(b):
    return "Yes" if b else "No"


def s12_financials(d):
    d.h1("12. Financial plan", new_page=True)
    d.para(f"Every figure in this section comes from the **{MODEL_LINE}**, Base case unless stated. The "
           "workbook carries the monthly build; this section summarises it. **These are forward-looking "
           "projections, not results.** FluxMuse has no paying customers yet, so every volume and rate is an "
           "assumption, and many are still marked [[CONFIRM]] (Appendix E).")

    d.h2("Key assumptions")
    d.bullets([
        f"**Timing.** Month 1 is October 2026; the fiscal year runs October to September. The {SEED_M} seed is "
        f"modelled to land in **{CASH['seed_month']}** **[[CONFIRM]]**. Until then the business runs lean: two "
        "founders on reduced salaries, lean hosting and overheads, the first-group set-up cost, and no paid "
        "marketing or hiring.",
        "**No trials, no pilot.** South Africa sells from October 2026. A first group of businesses is set up "
        "by hand from October 2026 to January 2027 **[[CONFIRM]]**.",
        f"**Sign-ups.** 150 self-serve sign-ups in South Africa in October 2026, growing 12% a month in FY1 "
        f"**[[CONFIRM]]**. {pct(FP['direct_paid_share_of_signups_pct']['Solo'])} of Solo and "
        f"{pct(FP['direct_paid_share_of_signups_pct']['SMEs'])} of SME sign-ups pay at once; the rest join Free, "
        f"which upgrades at {FP['monthly_upgrade_pct']}% a month **[[CONFIRM]]**.",
        "**Pricing.** The nine live plans; Solo buyers mostly on Nano and Micro, SMEs on Starter, Growth and "
        "Scale. Annual plans are 10× monthly and 25% of subscriptions. No VAT.",
        "**AI cost.** R0.15 of provider cost per credit, the product's own figure.",
        "**Markets.** South Africa only until Nigeria, Kenya and Ghana checkout is live; each then waits for an "
        "MRR gate.",
        "**Cost discipline.** Hiring and launches wait for net MRR gates; paid acquisition is capped at R40,000 "
        "plus 35% of last month's net MRR and switched off where CAC payback would exceed 12 months.",
        f"**Funding.** The {SEED_M} seed only; the Series A input is zero. Tax at 27% only once cumulative "
        "EBITDA is positive.",
    ])

    d.h2("Revenue build")
    d.para("Revenue is mostly recurring subscriptions, plus AI-credit packs, WhatsApp messaging resold at Meta "
           "cost plus a margin, and Custom setup fees. There is no FluxMuse checkout fee.")
    st = [a["revenue_by_stream_zar"] for a in ANN]
    d.figure("charts/revenue_by_stream_fy1_fy5.png",
             "Revenue by stream, FY1–FY5 (Base case), net of the Founding Member discount.",
             f"Stacked bar chart of revenue by stream rising from {rm(ANN[0]['total_revenue_zar'])} in FY1 to "
             f"{rm(ANN[4]['total_revenue_zar'])} in FY5, mostly subscriptions, with smaller AI-credit pack, "
             "WhatsApp messaging and setup-fee layers.")
    d.fy_table("Revenue by stream (R million, Base case)", [
        ["Subscriptions (net)"] + [rm(s["subscriptions"]) for s in st],
        ["AI-credit packs"] + [rm(s["ai_credit_topups"], 2) for s in st],
        ["WhatsApp messaging"] + [rm(s["whatsapp_messaging"], 2) for s in st],
        ["Custom setup fees"] + [rm(s["enterprise_setup_fees"] + s["agency_setup_fees"], 2) for s in st],
        ["**Total revenue**"] + [rm(a["total_revenue_zar"]) for a in ANN],
        ["Total revenue (US$ m)"] + [f"US${a['total_revenue_usd'] / 1e6:,.2f}m" for a in ANN],
        ["Growth on prior year"] + ["n/a"] + [pct(a["revenue_growth_pct"]) for a in ANN[1:]],
    ], total_rows=(4,))
    d.source()
    d.figure("charts/arr_and_customers.png",
             "Subscription ARR and paying workspaces at each year end (Base case).",
             f"Two bar charts: subscription ARR rising from {rm(ANN[0]['subscription_arr_zar'])} in FY1 to "
             f"{rm(ANN[4]['subscription_arr_zar'])} in FY5, and paying workspaces rising from "
             f"{ANN[0]['ending_paying_workspaces']:,} to {ANN[4]['ending_paying_workspaces']:,}.")
    seg = ANN[4]["ending_customers_by_segment"]
    d.figure("charts/customers_by_segment.png",
             "Paying workspaces by segment (Base case).",
             f"Stacked bars of paying workspaces by segment to {ANN[4]['ending_paying_workspaces']:,} in FY5: "
             f"Solo {seg['Solo']:,}, SMEs {seg['SMEs']:,}, Agencies {seg['Agencies']}, Corporate "
             f"{seg['Corporate']} and Custom {seg['Enterprise']}.")
    mk = ANN[4]["ending_customers_by_market"]
    d.figure("charts/customers_by_region.png",
             "Paying workspaces by market (Base case). Markets outside South Africa wait for payment accounts.",
             f"Area chart of paying workspaces by market to September 2031: South Africa {mk['South Africa']:,}, "
             f"Nigeria {mk['Nigeria']}, Kenya {mk['Kenya']}, Ghana {mk['Ghana']} and other markets in US dollars "
             f"{mk['Rest of Africa (USD)']}.")
    d.fy_table("The Free plan (Base case)", [
        ["Active Free users (Sept)"] + [f"{v:,}" for v in FP["active_free_users_fy1_fy5"]],
        ["Free users upgrading to paid in the year"] + [f"{v:,}" for v in FP["free_to_paid_upgrades_fy1_fy5"]],
        ["Cost of the Free plan (R)"] + [rand(v) for v in FP["free_plan_cost_zar_fy1_fy5"]],
    ], first_header="Free plan", size=9)
    d.source()

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
    d.note("Gross margin is low in FY1 and FY2 because AI cost (R0.15 a credit) and the Free plan weigh on a "
           "small revenue base. WhatsApp messaging is booked gross, so the software gross margin line shows the "
           "platform margin.")

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
             f"Monthly closing cash on the {SEED_M} seed against the {rm(CASH['min_cash_buffer_zar'], 1)} buffer "
             "(Base case). No Series A.",
             f"Line chart of monthly closing cash: a small pre-seed dip, the {SEED_M} seed landing in "
             f"{CASH['seed_month']}, a long decline to a post-seed low of {rm(CASH['min_post_seed_cash_zar'], 2)} in "
             f"{CASH['min_post_seed_cash_month']}, {rm(CASH['headroom_over_buffer_zar'], 2)} above the buffer, then "
             f"recovery after EBITDA break-even in {CASH['break_even_month']}.")
    d.bullets([
        f"**Pre-seed bridge: {rand(CASH['pre_seed_bridge_required_zar'])}.** On opening cash of "
        f"{rand(CASH['opening_cash_zar'])} (**[[CONFIRM OPENING CASH]]**), cash dips to "
        f"−{rk(abs(CASH['min_cash_zar']))} in {CASH['min_cash_month']}, one month before the seed lands.",
        f"**Minimum cash after the seed: {rm(CASH['min_post_seed_cash_zar'], 2)} in "
        f"{CASH['min_post_seed_cash_month']}**, only {rm(CASH['headroom_over_buffer_zar'], 2)} above the "
        f"{rm(CASH['min_cash_buffer_zar'], 1)} buffer, {CASH['months_from_seed_to_cash_trough']} months after "
        "the seed.",
        f"**Runway at the seed close: about {CASH['runway_at_seed_close_months']:.0f} months** at the average "
        f"net burn of the following year ({rand(CASH['avg_monthly_net_burn_12m_after_seed_zar'])} a month).",
    ])

    d.h2("Break-even")
    d.figure("charts/ebitda_and_cash.png",
             "Monthly EBITDA and closing cash (Base case).",
             f"Two panels: monthly EBITDA turning positive in {CASH['break_even_month']}, and closing cash "
             f"falling to {rm(CASH['min_post_seed_cash_zar'], 2)} in {CASH['min_post_seed_cash_month']} before "
             "recovering.")
    d.table(["Milestone", "Base case"], [
        ("First month of positive EBITDA", CASH["break_even_month"]),
        ("EBITDA positive every month from", CASH["break_even_month_sustained"]),
        ("First month of positive operating cash flow", CASH["cash_flow_positive_month"]),
        ("Operating cash flow positive every month from", CASH["cash_flow_positive_month_sustained"]),
        (f"Profitable on the {SEED_M} seed alone",
         f"Base {yn(PASS['Base'])}; Upside {yn(PASS['Upside'])}; Conservative {yn(PASS['Conservative'])}"),
    ], [9.0, 8.0], "Break-even milestones", size=9.5)

    d.h2("Unit economics")
    d.figure("charts/unit_economics.png",
             "Lifetime value against acquisition cost by segment, FY3 (Base case).",
             f"Panels comparing LTV and CAC per customer in FY3 by segment; Solo at "
             f"{UE['by_segment']['Solo']['ltv_to_cac']} times does not pay back; blended "
             f"{UE['blended']['ltv_to_cac']} times with a {UE['blended']['cac_payback_months']}-month payback.")
    segname = {"Enterprise": "Custom"}
    d.table(["Segment, FY3", "ARPA (R/month)", "Monthly churn", "LTV", "CAC", "LTV:CAC", "Payback"], [
        (segname.get(name, name), rand(s["arpa_zar_per_month"]), pct(s["monthly_churn_pct"], 1), rand(s["ltv_zar"]),
         rand(s["cac_zar"]), f"{s['ltv_to_cac']}x", f"{s['cac_payback_months']} months")
        for name, s in UE["by_segment"].items()
    ] + [("**Blended**", rand(UE["blended"]["arpa_zar_per_month"]), "—", rand(UE["blended"]["ltv_zar"]),
          rand(UE["blended"]["cac_zar"]), f"{UE['blended']['ltv_to_cac']}x",
          f"{UE['blended']['cac_payback_months']} months")],
            [3.0, 2.7, 2.3, 2.8, 2.3, 1.7, 2.2], "Unit economics by segment, FY3", size=9,
            aligns=[None, "right", "right", "right", "right", "right", "right"],
            total_rows=(len(UE["by_segment"]),))
    d.source()
    d.bullets([
        "LTV is ARPA × software gross margin ÷ monthly logo churn. Solo and SME CAC includes paid spend plus a "
        "share of brand, launch and marketing payroll.",
        f"**Solo does not pay back on fully loaded CAC ({UE['by_segment']['Solo']['ltv_to_cac']}×).** Nano and "
        "Micro are cheap and churn fast. Solo customers earn their place through the Free plan and upgrades, not "
        "paid acquisition at scale.",
        f"**SMEs and agencies carry the economics** ({UE['by_segment']['SMEs']['ltv_to_cac']}× and "
        f"{UE['by_segment']['Agencies']['ltv_to_cac']}×).",
    ])

    d.h2("Scenarios")
    d.figure("charts/scenarios.png",
             f"FY5 revenue and EBITDA in all three scenarios, on the {SEED_M} seed. Conservative fails the test.",
             "Bar chart of FY5 revenue and EBITDA for Conservative, Base and Upside, with workspaces, break-even "
             "and minimum cash under each; Conservative is short of the buffer, Base and Upside pass.")
    S = [SC[n] for n in NAMES]
    d.table(["", "Conservative", "Base", "Upside"], [
        ("Revenue FY1 / FY3 / FY5 (R m)",) + tuple(
            f"{s['revenue_zar_fy1_fy5'][0] / 1e6:.1f} / {s['fy3_revenue_zar'] / 1e6:.1f} / "
            f"{s['fy5_revenue_zar'] / 1e6:.1f}" for s in S),
        ("EBITDA FY3 / FY5 (R m)",) + tuple(
            f"{s['fy3_ebitda_zar'] / 1e6:.1f} / {s['fy5_ebitda_zar'] / 1e6:.1f}" for s in S),
        ("FY5 EBITDA margin",) + tuple(pct(s["fy5_ebitda_margin_pct"]) for s in S),
        ("Paying workspaces FY5",) + tuple(f"{s['fy5_paying_workspaces']:,}" for s in S),
        ("Headcount FY5",) + tuple(str(s["headcount_fy1_fy5"][4]) for s in S),
        ("EBITDA positive every month from",) + tuple(s["breakeven_month_sustained"] for s in S),
        ("Minimum cash after the seed",) + tuple(
            f"{rm(s['min_post_seed_cash_zar'], 2)} ({s['min_post_seed_cash_month']})" for s in S),
        ("First month below the buffer",) + tuple(s["first_month_below_buffer"] for s in S),
        ("Nigeria / Kenya / Ghana launch",) + tuple(
            f"{s['market_launch_months']['Nigeria']} / {s['market_launch_months']['Kenya']} / "
            f"{s['market_launch_months']['Ghana']}" for s in S),
        (f"**Profitable on {SEED_M} alone**",) + tuple(f"**{yn(PASS[n])}**" for n in NAMES),
    ], [5.0, 4.0, 4.0, 4.0], "Scenario comparison", size=9,
        aligns=[None, "right", "right", "right"], total_rows=(9,))
    d.source()
    d.callout(f"The Conservative case fails on {SEED_M}, and we say so", [
        f"Cash stays above zero but falls below the {rm(CASH['min_cash_buffer_zar'], 1)} buffer from "
        f"{SC['Conservative']['first_month_below_buffer']} (low {rm(CD['as_modelled']['min_post_seed_cash_zar'], 2)}, "
        f"short {rm(CD['as_modelled']['shortfall_vs_buffer_zar'], 2)}), and EBITDA does not turn positive by "
        "Sep 2031.",
        f"- The smallest single fixes would be a {CD['smallest_gate_multiplier_that_passes']}× hiring and launch "
        f"gate multiplier, or a {CD['smallest_uniform_non_founder_salary_cut_pct_that_passes']}% cut to every "
        "non-founder salary. Neither is adopted.",
        "- If early data looks like Conservative, the response is to slow hiring and launches early, before the "
        "cash is spent.",
    ], fill=TINT, caption="Layout: conservative case callout")

    d.h2("Sensitivities: the headroom is thin")
    d.para(f"The {SEED_M} buys about {rm(CASH['headroom_over_buffer_zar'], 1)} of headroom, not a margin of "
           "safety. The grid shows minimum post-seed cash on Base gates as new-customer volume and churn move.")
    vol = SENS["cols_new_customer_volume_multiplier"]
    grid = SENS["min_post_seed_cash_zar_m"]
    d.table(["Churn ×  /  Volume →"] + [f"{v:.0%}" for v in vol],
            [[f"{SENS['rows_churn_multiplier'][i]:.2f}×"] + [f"R{val:.2f}m" for val in row]
             for i, row in enumerate(grid)],
            [4.2] + [2.56] * 5, "Minimum post-seed cash (R m), Base gates", size=9,
            aligns=[None] + ["right"] * 5, highlight_rows=(2,))
    d.source()
    d.table(["Free-to-paid upgrade rate", "FY3 revenue", "FY5 EBITDA", "Minimum post-seed cash", "Passes"], [
        (k, rm(v["fy3_revenue_zar"]), rm(v["fy5_ebitda_zar"]), rm(v["min_post_seed_cash_zar"], 2),
         yn(v["profitable_on_seed_alone"])) for k, v in FCS.items()
    ], [4.6, 3.0, 3.0, 3.8, 2.6], "Free-plan conversion sensitivity (Base case)", size=9,
        aligns=[None, "right", "right", "right", "right"])
    d.source()
    d.bullets([
        f"**Sign-ups 15% below plan** take minimum cash to R{grid[2][1]:.2f}m, below the buffer; churn 15% worse "
        f"takes it to R{grid[3][2]:.2f}m.",
        f"**Free upgrades at 0.25% a month** take it to {rm(FCS['0.25% a month']['min_post_seed_cash_zar'], 2)}: "
        "the plan fails.",
        "**The response is pre-agreed**: measure pay-at-sign-up and Free upgrades from the first month, and "
        "raise the hiring gates early if they lag.",
    ])
    d.h3("FX shock: the rand 15% stronger")
    d.figure("charts/fx_shock_sensitivity.png",
             "A 15% stronger rand against NGN, KES, GHS and USD from April 2029, with and without quarterly "
             "repricing.",
             "Grouped bars comparing base, shock with repricing and shock without repricing for FY3 and FY5 "
             "revenue and EBITDA and minimum post-seed cash. Without repricing the plan fails the cash test.")
    keys = ["Base", "ZAR 15% stronger (repricing on)", "ZAR 15% stronger (no repricing)"]
    d.table(["Outcome", "Base", "Rand +15%, repricing on", "Rand +15%, no repricing"], [
        ("FY3 revenue",) + tuple(rm(FX[k]["fy3_revenue_zar"], 2) for k in keys),
        ("FY5 revenue",) + tuple(rm(FX[k]["fy5_revenue_zar"], 2) for k in keys),
        ("FY5 EBITDA",) + tuple(rm(FX[k]["fy5_ebitda_zar"], 2) for k in keys),
        ("Minimum post-seed cash",) + tuple(rm(FX[k]["min_post_seed_cash_zar"], 2) for k in keys),
        (f"Profitable on {SEED_M} alone",) + tuple(yn(FX[k]["profitable_on_seed_alone"]) for k in keys),
    ], [4.4, 4.2, 4.2, 4.2], "FX shock, Base case", size=9,
        aligns=[None, "right", "right", "right"])
    d.source()
    d.note("Quarterly repricing is the main FX control. Without it, the shock breaks the buffer.")

    d.h3("What the launch offer costs")
    oc = FM["option_comparison"]
    d.table(["Launch offer (Base case)", "FY1–FY3 discount cost", "Minimum post-seed cash",
             f"Profitable on {SEED_M}"], [
        ("Founding Member (live)", rk(oc["Founding Member (default)"]["discount_cost_fy1_fy3_zar"]),
         rm(oc["Founding Member (default)"]["min_post_seed_cash_zar"], 2),
         yn(oc["Founding Member (default)"]["profitable_on_seed_alone"])),
        ("No launch offer", "R0", rm(oc["None"]["min_post_seed_cash_zar"], 2),
         yn(oc["None"]["profitable_on_seed_alone"])),
    ], [6.0, 3.8, 3.8, 3.4], "Cost of the launch offer", size=9,
        aligns=[None, "right", "right", "right"])
    d.note(f"Because sign-ups are assumed to rise {FM['window_signup_uplift_pct']}% while the offer runs, it "
           "leaves marginally more cash than no offer. That uplift is unproven.")


def s13_funding(d):
    d.h1("13. Funding request and use of funds", new_page=True)
    d.h2("The ask")
    d.kv_table([
        ("Amount", f"R{M['seed_zar']:,} (about {usd(M['seed_usd'])})"),
        ("Round", "Seed"),
        ("Instrument", "[[INSTRUMENT: SAFE OR PRICED EQUITY]]"),
        ("Valuation", "[[PRE-MONEY VALUATION: TBC]]"),
        ("Modelled close", f"{CASH['seed_month']} (model input; an earlier close removes the pre-seed bridge)"),
        ("Why this size", f"{rm(SS['smallest_passing_seed_zar_base'], 1)} is the smallest seed at which the Base "
                          f"case passes on the current offer, rounded up to {SEED_M} **[[CONFIRM]]**"),
        ("Follow-on funding", "None in the Base and Upside cases. The Conservative case falls short"),
        ("Minimum-cash policy", f"Closing cash at or above {rm(CASH['min_cash_buffer_zar'], 1)} every month from "
                                "the seed"),
    ], widths=(4.6, 12.4), caption="Layout: the ask")

    d.h2("Allocation")
    d.table(["Category", "Share", "R", "What it buys and when"], [
        (a["category"], pct(a["share_pct"]), rm(a["amount_zar"], 2), a["what_it_buys"])
        for a in UOF["allocation"]
    ], [3.6, 1.3, 1.8, 10.3], f"Use of the {SEED_M} seed", size=8.5,
        aligns=[None, "right", "right", None])
    al = UOF["allocation"]
    d.figure("charts/use_of_funds.png",
             f"The {SEED_M} seed by category.",
             "Chart of the use of funds: " + "; ".join(
                 f"{a['category']} {rm(a['amount_zar'], 1)} at {a['share_pct']}%" for a in al) + ".")
    d.para("**Timing.** Product and engineering hires begin in the seed month; growth and partnerships hires "
           "follow; country leads are hired two months before each market launch, which waits for the payment "
           "accounts and an MRR gate.")

    d.h2("How the allocation compares with modelled spend")
    d.para("The seed funds **net** burn, not gross spend, because revenue pays a growing share of costs. "
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
    cats = {c["category"]: c for c in REC["24"]["categories"]}
    ex = cats["Market expansion (NG, KE, GH) & payments compliance"]
    op = cats["Operations & working capital"]
    d.bullets([
        f"**Expansion is under-spent against its 15% share ({pct(ex['share_of_spend_pct'], 1)} of spend, "
        f"{ex['gap_pp']:+.1f} points)** because Nigeria, Kenya and Ghana open late in the window.",
        f"**Operations runs over its 15% share ({pct(op['share_of_spend_pct'], 1)}, {op['gap_pp']:+.1f} points)** "
        "because customer success, hosting, AI and support scale with customers.",
    ])

    d.h2("Why most of the seed is still there after two years")
    d.para(f"About **{rm(REC['24']['seed_remaining_zar'], 1)} is unspent 24 months after close**. It is not a "
           "reserve on top of the plan: the Base case needs it to carry the business through the long "
           f"loss-making stretch to the {CASH['min_post_seed_cash_month']} low, "
           f"{CASH['months_from_seed_to_cash_trough']} months after the seed.")

    d.h2("The pre-seed bridge")
    d.para(f"On the modelled {CASH['seed_month']} close and opening cash of {rand(CASH['opening_cash_zar'])}, "
           f"the business needs a bridge of **{rand(CASH['pre_seed_bridge_required_zar'])}** in "
           f"{CASH['min_cash_month']}. Options are a founder loan or closing the round earlier. "
           "**[[HOW THE PRE-SEED BRIDGE WILL BE COVERED]]**")

    d.h2("Investor return considerations")
    d.para("This plan does not propose a valuation or model a return. What it does say:")
    d.bullets([
        "**The round is sized to reach profitability in the Base case**, with no Series A. It is not sized for "
        "the Conservative case, which falls short, and the Base headroom is thin.",
        f"**Cash generation starts inside the horizon** in the Base case: operating cash flow turns positive in "
        f"{CASH['cash_flow_positive_month']}.",
        f"**Recurring revenue**: subscription ARR of {rm(ANN[4]['subscription_arr_zar'], 0)} by FY5, FY3 blended "
        f"LTV:CAC of {UE['blended']['ltv_to_cac']}×.",
        "**Not in the projections**: " + ", ".join(M["not_modelled"][:3]).lower() + ".",
        "**Exit routes**: **[[EXIT CONSIDERATIONS: TO BE DISCUSSED WITH INVESTORS]]**.",
    ])
