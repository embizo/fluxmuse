"""Sections 14-16 and appendices A-F."""
from bp_doc import ANN, D, DEEP, M, MV, SEED_M, TINT, pct, rand, rk, rm

CASH = M["cash"]
UE = M["unit_economics_fy3"]
MKL = M["markets"]["launch_months"]["Base"]
MKP = M["markets"]["planned_earliest_launch_month"]
GATES = M["markets"]["launch_mrr_gate_zar"]
PT = M["price_tables"]
ZAR = PT["zar_list_monthly"]
LM = PT["local_monthly"]
PW = PT["partner_wholesale_monthly"]
FMB = PT["founding_member_first_2_bills_zar"]
FP = M["free_plan"]
FG = M["first_group"]
FCS = M["free_conversion_sensitivity"]
FX = M["fx_shock"]["results"]
SC = M["scenarios"]
SENS = M["sensitivity_base"]["min_post_seed_cash_zar_m"]

# Status by country, as shown in assets/infographics/payment-rails-matrix.png (Oct 2026).
COUNTRIES = [
    ("South Africa", "ZA", "ZAR", "Open: Paystack live; Yoco and Ozow for FluxMuse billing"),
    ("Nigeria", "NG", "NGN", "Priced, not on sale: Paystack, pawaPay, Fincra pending"),
    ("Kenya", "KE", "KES", "Priced, not on sale: Paystack, pawaPay, Fincra pending"),
    ("Ghana", "GH", "GHS", "Priced, not on sale: Paystack, pawaPay, Fincra pending"),
    ("Côte d'Ivoire", "CI", "XOF", "Closed: Paystack, pawaPay, Fincra pending"),
    ("Rwanda", "RW", "RWF", "Closed: Paystack, pawaPay, Fincra pending"),
    ("Uganda, Tanzania, Zambia, Cameroon, Senegal, Benin, Burkina Faso, Republic of the Congo, Gabon, DR Congo",
     "—", "local / USD", "Closed: pawaPay and Fincra pending"),
    ("Malawi, Mozambique, Sierra Leone, Ethiopia, Lesotho", "—", "local / USD", "Closed: pawaPay pending"),
    ("South Sudan, Zimbabwe", "SS, ZW", "SSP / USD", "Closed: Fincra pending"),
    ("Botswana, Namibia", "BW, NA", "BWP / NAD", "Coming soon: no provider yet; waitlist"),
]


def s14_risks(d):
    d.h1("14. Risk analysis", new_page=True)
    d.para("Likelihood and impact are assessed on the plan as it stands, after the mitigations built into the "
           f"model (MRR-gated hiring and launches, capped paid acquisition and the "
           f"{rm(CASH['min_cash_buffer_zar'], 1)} minimum-cash buffer). Owners are to be assigned before this "
           "plan is issued.")
    f25 = FCS["0.25% a month"]
    nr = FX["ZAR 15% stronger (no repricing)"]
    d.table(["#", "Risk", "Likelihood", "Impact", "Mitigation", "Owner"], [
        ("R1", "**Demand is unproven.** There are no paying customers; sign-ups and conversion may fall short",
         "High", "High",
         f"The model quantifies it: sign-ups 15% below plan take minimum cash to R{SENS[2][1]:.2f}m, below the "
         "buffer. Measure from month 1; raise hiring and launch gates early if early data lags", "[[OWNER]]"),
        ("R2", "**Thin headroom on the seed.** The Base case passes by about "
               f"{rm(CASH['headroom_over_buffer_zar'], 1)}; Conservative fails", "Medium", "High",
         f"Free upgrades at 0.25% a month take minimum cash to {rm(f25['min_post_seed_cash_zar'], 2)}. "
         "Pre-agreed response: slow hiring, delay launches. If that is not enough, raise more or cut cost early "
         "**[[FOUNDER: CONTINGENCY]]**", "[[OWNER]]"),
        ("R3", "**Meta dependency.** Publishing permissions refused or delayed, or policy and pricing change",
         "Medium", "High",
         "Verified Tech Provider; WhatsApp Business is live. Nothing waiting on Meta is sold as live; WhatsApp "
         "Status and TikTok work today", "[[OWNER]]"),
        ("R4", "**Payment accounts.** Only South Africa has live checkout; FluxMuse checkout is untested with "
               "real money", "Medium", "High",
         "Test checkout end to end before offering it. pawaPay and Fincra are contracted; no expansion market "
         "opens until its accounts are live", "[[OWNER]]"),
        ("R5", "**FX.** The rand strengthens against NGN, KES, GHS or USD", "Medium", "Medium",
         f"Quarterly repricing at more than 10% drift. Without it, a 15% shock takes minimum cash to "
         f"{rm(nr['min_post_seed_cash_zar'], 2)} and the plan fails", "[[OWNER]]"),
        ("R6", "**AI cost.** Credit usage runs ahead of assumptions", "Medium", "Medium",
         "Credits priced at R0.15 of provider cost with 40% utilisation assumed; allowances per plan, packs for "
         "more; Corporate and above use their own keys. Cost per credit is a monthly KPI", "[[OWNER]]"),
        ("R7", "**Competition.** A global platform adds WhatsApp selling and rand pricing", "Medium", "Medium",
         "WhatsApp-first product, rand pricing and the partner channel (section 7)", "[[OWNER]]"),
        ("R8", "**Hiring and execution**", "Medium", "Medium",
         "Every non-founder role waits for an MRR gate, so payroll cannot outrun revenue by design", "[[OWNER]]"),
        ("R9", "**Regulatory.** POPIA, VAT registration, data-protection registrations in new markets", "Medium",
         "Medium", "Consent-only broadcasts and human-sent outreach; VAT plan before the threshold; "
         "registrations funded from the expansion budget", "[[OWNER]]"),
        ("R10", "**Key person.** The business depends on two founders", "Medium", "High",
         "Senior hires as MRR allows. **[[KEY-PERSON COVER AND INSURANCE]]**", "[[OWNER]]"),
    ], [0.9, 3.9, 1.6, 1.4, 6.6, 1.6], "Risk register", size=8, first_col_bold=False)
    d.note("The model's own limitations are listed in Appendix E: fractional customers, one-way launch and "
           "hiring decisions, deterministic FX, no downgrades, and simplified tax and working capital.")


def s15_milestones(d):
    d.h1("15. Milestones and KPIs", new_page=True)
    d.h2("Timeline")
    d.para("Dates to October 2026 are facts. Later dates are model inputs or are **gated on payment accounts and "
           "revenue, not on the calendar**.")
    d.table(["When", "Milestone", "Gate or condition"], [
        ("Sept 2026", "Verified Meta Tech Provider", "Done"),
        ("Oct 2026", "Selling in South Africa; Founding Member live (1 Oct)", "Done"),
        (FG["months"].replace(" - ", " to "), "First group of businesses set up by hand (model input)",
         "[[CONFIRM]]"),
        ("[[TARGET DATE]]", "Checkout through FluxMuse tested with real money; Meta publishing approved",
         "Real-money test; Meta approval"),
        (CASH["seed_month"], f"{SEED_M} seed closes; hiring and capped paid acquisition begin",
         "Round closed (model input)"),
        ("Pending", "Fincra and pawaPay accounts live", "Provider onboarding"),
        (f"{MKL['Nigeria']} to {MKL['Ghana']}", f"Nigeria {MKL['Nigeria']}, Kenya {MKL['Kenya']}, Ghana {MKL['Ghana']}",
         f"Accounts live, then net MRR gates of {rm(GATES['Nigeria'], 1)}, {rm(GATES['Kenya'], 1)} and "
         f"{rm(GATES['Ghana'], 1)}"),
        (MKL["Rest of Africa (USD)"], "Other covered markets, self-serve in US dollars",
         f"{rm(GATES['Rest of Africa (USD)'], 1)} net MRR gate"),
        (CASH["cash_flow_positive_month"], "Operating cash flow turns positive", "—"),
        (CASH["break_even_month"], "EBITDA break-even, sustained", "—"),
        ("FY5 (Oct 2030 – Sep 2031)",
         f"{ANN[4]['ending_paying_workspaces']:,} paying workspaces, "
         f"{rm(ANN[4]['subscription_arr_zar'], 0)} subscription ARR", "—"),
        ("Not scheduled", "Botswana and Namibia", "A payment provider must cover them first"),
    ], [3.4, 7.6, 6.0], "Milestones (Base case)", size=9)
    d.source()

    d.h2("The KPI dashboard")
    d.para("Reported to investors **monthly**, within [[N]] working days of month end, against the model.")
    d.table(["KPI", "Why it matters", "Base case reference point"], [
        ("Sign-ups, by market and segment", "The leading indicator", "150 a month in South Africa at launch"),
        ("Pay-at-sign-up rate", "Sets early revenue",
         f"Solo {pct(FP['direct_paid_share_of_signups_pct']['Solo'])}, SME "
         f"{pct(FP['direct_paid_share_of_signups_pct']['SMEs'])}"),
        ("Free-to-paid upgrade rate", "The input that most decides whether the seed is enough",
         f"{FP['monthly_upgrade_pct']}% a month"),
        ("New and total paying workspaces", "The headline growth number",
         f"{ANN[0]['ending_paying_workspaces']} at the end of FY1"),
        ("Net subscription MRR", "Drives every hiring and launch gate",
         f"{rand(ANN[0]['subscription_mrr_sept_zar'])} in September 2027"),
        ("Monthly churn by tier", "Nano and Micro churn set Solo economics", "Nano 8.0%, Micro 7.0%"),
        ("CAC and payback by segment", "The paid-spend switch is set on payback",
         f"FY3 blended CAC {rand(UE['blended']['cac_zar'])}, payback {UE['blended']['cac_payback_months']} months"),
        ("AI credits used per workspace, Free and paid", "AI is the largest variable cost",
         "40% of allowance; R0.15 a credit"),
        ("Gross margin and software gross margin", "AI and messaging cost control",
         f"FY1 {pct(ANN[0]['gross_margin_pct'])} / {pct(ANN[0]['software_gross_margin_pct'])}"),
        ("Closing cash against the buffer", "The constraint the plan is built around",
         f"Low of {rm(CASH['min_post_seed_cash_zar'], 2)} in {CASH['min_post_seed_cash_month']}"),
        ("Qualified leads per merchant in 30 days", "The lead guarantee", "3 in 30 days of go-live"),
        ("Agency partners signed", "Channel health",
         f"{ANN[0]['ending_customers_by_segment']['Agencies']} agencies by the end of FY1"),
        ("Meta permissions and payment accounts", "The platform and rail dependencies", "Being switched on"),
    ], [4.4, 5.0, 7.6], "Monthly KPI dashboard", size=8.5)


def s16_impact(d):
    d.h1("16. Social and economic impact", new_page=True)
    d.para("This section is written for development-finance funders. **Every claim below is either a modelled "
           "figure or a measurement commitment.** Where we cannot yet measure something, the plan says so.")

    d.h2("SMME enablement")
    d.bullets([
        f"The Base case puts **{ANN[4]['ending_paying_workspaces']:,} small and medium businesses** on paid "
        f"plans by FY5, of which {ANN[4]['ending_customers_by_segment']['Solo']:,} are solo sellers, plus "
        f"about {FP['active_free_users_fy1_fy5'][4]:,} active users of the permanent Free plan.",
        f"Paid plans start at **{rand(ZAR['Nano'])} a month**, which puts a marketing capability within reach of "
        "a business that could never fund an agency retainer.",
        "Customer outcomes (leads, orders, hours saved) are measured per workspace. **[[BASELINE AND TARGETS: TO "
        "BE MEASURED WITH THE FIRST GROUP]]**",
    ])

    d.h2("Digital inclusion")
    d.bullets([
        "Owners run their marketing and shop from **WhatsApp**, on the phone they already own, without a "
        "website or a card machine.",
        "**Answers in the customer's language**, and voice notes are transcribed, so owners can work the way "
        "they already talk.",
        "Paid checkout opens only where a payment provider is live, so no business is sold a service it cannot "
        "pay for.",
    ])

    d.h2("Jobs created")
    d.fy_table("Direct jobs in the plan, at each year end (Base case)",
               [[dep] + [str(v) for v in D["headcount_by_dept_fy_end"][dep]]
                for dep in D["headcount_by_dept_fy_end"]] +
               [["**Total direct jobs**"] + [str(v) for v in D["headcount_total_fy_end"]]],
               first_header="Department", total_rows=(len(D["headcount_by_dept_fy_end"]),))
    d.source()
    d.bullets([
        f"**{D['headcount_total_fy_end'][0]} jobs by the end of FY1** and "
        f"**{D['headcount_total_fy_end'][4]} by FY5**, from a base of two founders.",
        f"**{D['headcount_by_dept_fy_end']['Customer success'][4]} customer-success roles** by FY5: the most "
        "accessible entry-level positions in the plan.",
        f"**{D['headcount_by_dept_fy_end']['Country teams'][4]} country-team roles** in Nigeria, Kenya and "
        "Ghana, hired locally once those markets open.",
        "**Indirect employment** through agency partners is not counted. **[[MEASUREMENT PLAN]]**",
    ])

    d.h2("Women- and youth-owned businesses")
    d.para("The launch segments lean towards categories where women- and youth-owned businesses are strongly "
           "represented in South Africa: beauty and braiding, fashion resale, home baking and personal services.")
    d.para("**We do not yet have data, and will not claim any.** From the first group onward we will measure "
           "reach with a voluntary, POPIA-compliant question at onboarding, and report: "
           "**[[MEASURE: % OF WORKSPACES THAT ARE WOMEN-OWNED]]**, "
           "**[[MEASURE: % YOUTH-OWNED (OWNER UNDER 35)]]**, "
           "**[[MEASURE: % IN TOWNSHIP OR RURAL AREAS]]**, and "
           "**[[TARGETS AGREED WITH THE FUNDER]]**.")

    d.h2("Transformation and B-BBEE")
    d.kv_table([
        ("B-BBEE level", "[[B-BBEE LEVEL AND VERIFICATION DATE]]"),
        ("Ownership", "[[BLACK OWNERSHIP %, BLACK WOMEN OWNERSHIP %]]"),
        ("Employment equity", "[[EMPLOYMENT EQUITY PROFILE AND TARGETS FOR THE HIRING PLAN]]"),
        ("Skills development", "[[SKILLS DEVELOPMENT / LEARNERSHIP PLAN, IF ANY]]"),
        ("Enterprise and supplier development",
         "[[WHETHER THE PLATFORM QUALIFIES AS AN ESD CONTRIBUTION FOR CORPORATE PARTNERS]]"),
    ], widths=(5.4, 11.6), caption="Layout: transformation details")
    d.note("These fields must be completed from verified records. Do not estimate a B-BBEE level.")

    d.h2("How impact will be reported")
    d.bullets([
        "Impact metrics reported **quarterly** alongside the monthly KPI dashboard.",
        "Customer-level figures aggregated and anonymised; no business named without written consent; customer "
        "names and phone numbers blurred in any screenshot (POPIA).",
        "**[[IMPACT REPORTING FORMAT AND FREQUENCY AGREED WITH THE FUNDER]]**",
    ])


# ---------------------------------------------------------------- appendices
def appendices(d):
    d.h1("Appendix A. Pricing tables", new_page=True)
    d.h2("South Africa (on sale)")
    rows = []
    for band, tiers in PT["bands"].items():
        for t in tiers:
            if t == "Custom":
                rows.append((band if t == tiers[0] else "", t, "On request", "—", "—"))
                continue
            fm = rand(FMB[t]) if t in FMB else "—"
            rows.append((band if t == tiers[0] else "", t, rand(ZAR[t]), rand(ZAR[t] * 10), fm))
    rows.append(("", "Partner wholesale (Agency tier)", rand(PW["ZAR"]), rand(PW["ZAR"] * 10), "Does not stack"))
    d.table(["Band", "Plan", "Monthly", "Annual (10×)", "Founding Member, first 2 monthly bills"], rows,
            [2.4, 4.6, 2.8, 3.0, 4.2], "South African prices (ZAR)", size=9,
            aligns=[None, None, "right", "right", "right"])
    d.h2("Local currency and US dollars (priced, not yet on sale)")
    hdr = ["Plan, monthly", "Nigeria (NGN)", "Kenya (KES)", "Ghana (GHS)", "USD markets"]
    paid = ["Nano", "Micro", "Starter", "Growth", "Scale", "Corporate", "Agency"]
    d.table(hdr, [(t, f"₦{LM['NGN'][t]:,}", f"KSh {LM['KES'][t]:,}", f"GH₵ {LM['GHS'][t]:,}", f"${LM['USD'][t]:,}")
                  for t in paid] +
            [("Custom (from)", f"₦{LM['NGN']['Custom']:,}", f"KSh {LM['KES']['Custom']:,}",
              f"GH₵ {LM['GHS']['Custom']:,}", f"${LM['USD']['Custom']:,}"),
             ("Partner wholesale", f"₦{PW['NGN']:,}", f"KSh {PW['KES']:,}", f"GH₵ {PW['GHS']:,}", f"${PW['USD']:,}")],
            [4.0, 3.3, 3.3, 3.3, 3.1], "Local-currency and USD prices", size=9,
            aligns=[None, "right", "right", "right", "right"])
    d.bullets([
        "Free is R0 everywhere. Annual is 10× monthly in every currency.",
        "Local prices are set at parity with the rand and reviewed quarterly. None is on sale until the "
        "relevant payment accounts are live and checkout is tested.",
        "Founding Member applies to South African sign-ups only. No offer is set for other markets.",
        "Custom is sold by consultation; the model books it from the figures above **[[CONFIRM]]**.",
    ])

    d.h1("Appendix B. Payment rails and country coverage", new_page=True)
    d.table(["Country", "ISO", "Currency", "Status (October 2026)"],
            [(n, iso, cur, st) for n, iso, cur, st in COUNTRIES],
            [6.6, 1.6, 2.4, 6.4], "Payment status by country", size=8.5, first_col_bold=False)
    d.figure("infographics/payment-rails-matrix.png",
             "What is live, and what is still pending.",
             "Matrix of countries against Yoco, Ozow, Paystack, pawaPay and Fincra: South Africa live with "
             "Paystack, Yoco and Ozow; Nigeria, Kenya and Ghana priced; other countries closed with providers "
             "contracted and accounts pending; Botswana and Namibia coming soon with no provider yet.")
    d.bullets([
        "**Only South Africa is open for paid sign-up.** Paystack is live there; Yoco and Ozow run FluxMuse's own "
        "subscription billing.",
        "**pawaPay and Fincra are contracted for expansion; accounts are pending.** No country they cover is "
        "described as live.",
        "Every other country is **waitlist only**: no prices, no checkout.",
    ])

    d.h1("Appendix C. First group and case-study template", new_page=True)
    d.h2("The first group")
    d.table(["Item", "Detail"], [
        ("What it is", "A small first group of South African businesses, set up by hand by the founders. Not a "
                       "pilot, not free"),
        ("Pace (model input)", f"{FG['per_month']} a month, {FG['months'].replace(' - ', ' to ')}, "
                               f"{FG['total_workspaces']} in total, {FG['solo_share_pct']}% solo **[[CONFIRM]]**"),
        ("Price", "List price less Founding Member from the first bill"),
        ("Set-up cost (model)", f"{rand(FG['setup_cost_zar_per_month'])} a month"),
        ("Case studies", "Only with measured data and signed consent. None exists yet"),
        ("Working notes", "07_Case_Studies/First_Group_Case_Studies.md"),
    ], [4.0, 13.0], "First group", size=9)
    d.h2("Case-study template")
    d.para("Each case study follows this structure. **Every metric is a placeholder until measured, and target "
           "columns are labelled as goals, never as results.**")
    d.table(["KPI", "Baseline", "Target (goal)", "Actual"], [
        ("Qualified leads in 30 days of go-live", "[[ ]]", "3 (lead guarantee)", "[[ ]]"),
        ("Orders via the shop link", "[[ ]]", "[[ ]]", "[[ ]]"),
        ("Catalogue items built from photos", "[[ ]]", "[[ ]]", "[[ ]]"),
        ("Posts made per month", "[[ ]]", "[[ ]]", "[[ ]]"),
        ("Median first-reply time", "[[ ]]", "[[ ]]", "[[ ]]"),
        ("Owner hours saved per week", "[[ ]]", "[[ ]]", "[[ ]]"),
    ], [7.4, 3.2, 3.2, 3.2], "Case-study KPI template", size=9,
        aligns=[None, "center", "center", "center"])
    d.figure("infographics/case-study-template.png",
             "The case-study layout, with placeholder fields. Template only; no data yet.",
             "Case-study template for the first group of businesses: placeholders for business name, what "
             "changed, archetype, area, plan and period; the challenge in the owner's words; what was set up in "
             "week 1; three measured metrics labelled as goals, not results; an owner-quote placeholder; and a "
             "stamp reading template, no data yet, consent first.")
    d.bullets([
        "No business name, logo or photograph is used without signed consent; customer names and phone numbers "
        "are blurred in every screenshot.",
        "Every published figure states the period and how it was measured. Goals are never shown as results.",
    ])

    d.h1("Appendix D. Detailed financial tables", new_page=True)
    d.h2("Annual profit and loss")
    d.fy_table("Annual P&L (R, Base case)", [
        ["Subscriptions (gross)"] + [rand(a["subscriptions_gross_zar"]) for a in ANN],
        ["less Founding Member discount"] + [f"({rand(a['founding_member_discount_zar'])})" for a in ANN],
        ["Subscriptions (net)"] + [rand(a["revenue_by_stream_zar"]["subscriptions"]) for a in ANN],
        ["AI-credit packs"] + [rand(a["revenue_by_stream_zar"]["ai_credit_topups"]) for a in ANN],
        ["WhatsApp messaging"] + [rand(a["revenue_by_stream_zar"]["whatsapp_messaging"]) for a in ANN],
        ["Custom setup fees"] + [rand(a["revenue_by_stream_zar"]["enterprise_setup_fees"]) for a in ANN],
        ["**Total revenue**"] + [rand(a["total_revenue_zar"]) for a in ANN],
        ["Cost of revenue"] + [f"({rand(v)})" for v in D["annual"]["a_cogs"]],
        ["**Gross profit**"] + [rand(a["gross_profit_zar"]) for a in ANN],
        ["Payroll (excluding customer success)"] + [f"({rand(a['opex_zar']['payroll_excl_cs'])})" for a in ANN],
        ["Marketing and sales programmes"] +
        [f"({rand(a['opex_zar']['marketing_sales_programmes'])})" for a in ANN],
        ["G&A (non-payroll)"] + [f"({rand(a['opex_zar']['g_and_a'])})" for a in ANN],
        ["Meta, legal and compliance"] + [f"({rand(a['opex_zar']['legal_compliance'])})" for a in ANN],
        ["Software and tools"] + [f"({rand(a['opex_zar']['tools'])})" for a in ANN],
        ["Travel"] + [f"({rand(a['opex_zar']['travel'])})" for a in ANN],
        ["**Total operating expenses**"] + [f"({rand(a['opex_zar']['total'])})" for a in ANN],
        ["**EBITDA**"] + [rand(a["ebitda_zar"]) for a in ANN],
        ["Tax"] + [f"({rand(a['tax_zar'])})" for a in ANN],
        ["**Net income**"] + [rand(a["net_income_zar"]) for a in ANN],
    ], first_header="R", size=7.5, total_rows=(6, 8, 15, 16, 18), widths=[5.0] + [2.4] * 5)
    d.source()
    d.h2("Cost of revenue detail")
    cf = D["cash_flow_rows_fy_sum"]
    d.fy_table("Cost of revenue (R, Base case)", [
        ["AI inference, paid plans"] + [rand(v) for v in cf["cogs_ai_paid"]],
        ["AI and hosting, Free plan"] + [rand(v) for v in cf["cogs_free"]],
        ["Hosting"] + [rand(v) for v in cf["cogs_hosting"]],
        ["WhatsApp Meta fees (pass-through)"] + [rand(v) for v in cf["cogs_wa"]],
        ["Payment processing"] + [rand(v) for v in cf["cogs_proc"]],
        ["Variable support"] + [rand(v) for v in cf["cogs_support"]],
        ["Customer success team"] + [rand(v) for v in cf["cogs_cs_team"]],
        ["**Total cost of revenue**"] + [rand(v) for v in cf["cogs_total"]],
    ], first_header="R", size=8, total_rows=(7,), widths=[5.0] + [2.4] * 5)
    d.source()
    d.note("The Free-plan line is the AI and hosting cost of active Free users, shown separately from paid AI "
           "inference.")
    d.h2("Annual cash flow")
    d.fy_table("Annual cash flow (R, Base case)", [
        ["Opening cash"] + [rand(v) for v in D["opening_cash_fy"]],
        ["EBITDA"] + [rand(v) for v in cf["cf_ebitda"]],
        ["Tax paid"] + [rand(v) for v in cf["cf_tax"]],
        ["Increase in deferred revenue"] + [rand(v) for v in cf["d_dr"]],
        ["Increase in receivables"] + [f"({rand(v)})" for v in cf["d_ar"]],
        ["**Operating cash flow**"] + [rand(v) for v in cf["op_cf"]],
        ["Seed equity"] + [rand(v) for v in cf["seed_in"]],
        ["**Net cash flow**"] + [rand(v) for v in cf["net_cf"]],
        ["**Closing cash**"] + [rand(a["closing_cash_zar"]) for a in ANN],
        ["Lowest month-end cash in year"] + [rand(a["min_month_end_cash_zar"]) for a in ANN],
    ], first_header="R", size=8, total_rows=(5, 7, 8), widths=[5.0] + [2.4] * 5)
    d.source()
    d.h2("Payroll by department")
    d.fy_table("Payroll by department (R, Base case)",
               [[dep] + [rand(v) for v in D["payroll_by_dept_zar_fy"][dep]]
                for dep in D["payroll_by_dept_zar_fy"]],
               first_header="R", size=8, widths=[5.0] + [2.4] * 5)
    d.source()
    d.note("Customer-success payroll sits in cost of revenue, not operating expenses.")
    d.h2("Workspaces by segment, market and tier")
    segs = list(ANN[0]["ending_customers_by_segment"])
    mkts = [k for k in ANN[0]["ending_customers_by_market"] if k != "Botswana & Namibia"]
    tiers = list(ANN[0]["ending_customers_by_tier"])
    lab = {"Enterprise": "Enterprise (Custom)"}
    d.fy_table("Paying workspaces at year end (Base case)",
               [[f"Segment: {lab.get(k, k)}"] + [f"{a['ending_customers_by_segment'][k]:,}" for a in ANN] for k in segs] +
               [[f"Market: {k}"] + [f"{a['ending_customers_by_market'][k]:,}" for a in ANN] for k in mkts] +
               [[f"Tier: {k}"] + [f"{a['ending_customers_by_tier'][k]:,}" for a in ANN] for k in tiers] +
               [["**Total paying workspaces**"] + [f"{a['ending_paying_workspaces']:,}" for a in ANN]],
               first_header="Workspaces", size=8, total_rows=(len(segs) + len(mkts) + len(tiers),),
               widths=[5.0] + [2.4] * 5)
    d.source()
    d.note("Each breakdown sums to the total, subject to rounding. Botswana, Namibia and every gated country are "
           "zero in all five years.")

    d.h1("Appendix E. Model assumptions and open confirmations", new_page=True)
    d.callout("Internal section: remove before sending to an external party", [
        "Appendix E lists assumptions that still need founder sign-off. Delete this appendix, or the "
        "open-confirmations table below, before the plan goes to an investor or funder.",
    ], fill="FFF1A8", accent=DEEP, caption="Layout: internal-only banner")
    d.h2("Key assumptions")
    d.numbered(M["key_assumptions"])
    d.h2("Not modelled")
    d.bullets(M["not_modelled"])
    d.h2("Known limitations of the model")
    d.bullets([
        "Customers are fractional, and launch and hiring decisions are one-way.",
        "Gates use last month's MRR, with no look-ahead.",
        "There are no downgrades. Free users who go dormant never come back.",
        "Sign-ups that pay at once and Free users split Solo/SME by the same share.",
        "AI utilisation (40%) is assumed; R0.15 a credit is the platform's own figure, not a measured average.",
        "FX paths are deterministic, and repricing is assumed to cause no extra churn.",
        "WhatsApp pass-through is booked as gross revenue, which lowers blended gross margin.",
        "Tax ignores South Africa's 80% cap on assessed losses; depreciation, amortisation, interest and "
        "payables are ignored. VAT is not modelled because FluxMuse is not registered; registration would "
        "change pricing or margin.",
    ])
    d.h2("Open confirmations (founder)")
    d.table(["#", "To confirm"], [(str(i + 1), t) for i, t in enumerate(M["founder_confirmations_needed"])],
            [0.9, 16.1], "Founder confirmations still open", size=8.5, first_col_bold=False)
    d.h2("What live data replaces first")
    d.numbered([
        f"Pay-at-sign-up rates (Solo {pct(FP['direct_paid_share_of_signups_pct']['Solo'])}, SME "
        f"{pct(FP['direct_paid_share_of_signups_pct']['SMEs'])}) and the Free upgrade rate "
        f"({FP['monthly_upgrade_pct']}% a month). These decide whether the seed is enough.",
        "Sign-up volume (150 a month in South Africa at launch) and its growth.",
        "Tier mix of new paying customers, especially the Nano share, and early churn by tier.",
        "The Founding Member effect on sign-ups.",
        "AI-credit utilisation by plan and on Free.",
        "Agency and Corporate demand.",
        "Fincra and pawaPay go-live dates, then Nigeria, Kenya and Ghana sign-ups, CAC and churn.",
    ])

    d.h1("Appendix F. Glossary", new_page=True)
    d.table(["Term", "Meaning"], [
        ("ARPA", "Average revenue per account, per month"),
        ("ARR", "Annual recurring revenue: September net subscription MRR × 12"),
        ("B-BBEE", "Broad-Based Black Economic Empowerment (South Africa)"),
        ("Being switched on", "Built, but waiting on an approval, a real-money test or a beta"),
        ("CAC", "Customer acquisition cost"),
        ("CAC payback", "Months of gross profit needed to recover the CAC"),
        ("Cloud API", "Meta's hosted WhatsApp Business API"),
        ("EBITDA", "Earnings before interest, tax, depreciation and amortisation"),
        ("First group", "The small first set of South African businesses the founders set up by hand"),
        ("Founding Member", "30% off the first two monthly bills for South African sign-ups"),
        ("Free plan", "A permanent R0 plan with 1 brand and 1 channel. Not a trial"),
        ("FY", "Fiscal year, October to September. FY1 is October 2026 to September 2027"),
        ("Lead guarantee", "3 qualified leads in 30 days of go-live, or extended support at no extra charge"),
        ("LTV", "Lifetime value: ARPA × software gross margin ÷ monthly churn"),
        ("MRR", "Monthly recurring revenue"),
        ("MRR gate", "The net MRR a hire or a market launch must wait for"),
        ("MSME / SMME", "Micro, small and medium enterprise. SMME is the South African usage"),
        ("Partner wholesale", f"The permanent Agency-tier price for partners: {rand(PW['ZAR'])} a month"),
        ("POPIA", "Protection of Personal Information Act, 2013 (South Africa)"),
        ("SAM / SOM / TAM", "Serviceable addressable, serviceable obtainable and total addressable market"),
        ("Tech Provider", "Meta's verified status for a platform acting for other businesses"),
        ("Workspace", "One paying customer account on FluxMuse"),
    ], [4.0, 13.0], "Glossary", size=9)
