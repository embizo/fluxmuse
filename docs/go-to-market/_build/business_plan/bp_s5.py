"""Sections 14-16 and appendices A-F."""
from bp_doc import ANN, D, DEEP, M, TINT, pct, rand, rk, rm

CASH = M["cash"]
UE = M["unit_economics_fy3"]
MKL = M["markets"]["launch_months"]["Base"]

COUNTRIES = [
    (1, "South Africa", "ZA", "ZAR", "Yoco, Ozow, Paystack, Fincra"),
    (2, "Nigeria", "NG", "NGN", "Paystack, pawaPay, Fincra"),
    (3, "Ghana", "GH", "GHS", "Paystack, pawaPay, Fincra"),
    (4, "Kenya", "KE", "KES", "Paystack, pawaPay, Fincra"),
    (5, "Côte d'Ivoire", "CI", "XOF", "Paystack, pawaPay, Fincra"),
    (6, "Rwanda", "RW", "RWF", "Paystack, pawaPay, Fincra"),
    (7, "Uganda", "UG", "UGX", "pawaPay, Fincra"),
    (8, "Tanzania", "TZ", "TZS", "pawaPay, Fincra"),
    (9, "Zambia", "ZM", "ZMW", "pawaPay, Fincra"),
    (10, "Cameroon", "CM", "XAF", "pawaPay, Fincra"),
    (11, "Senegal", "SN", "XOF", "pawaPay, Fincra"),
    (12, "Benin", "BJ", "XOF", "pawaPay, Fincra"),
    (13, "Burkina Faso", "BF", "XOF", "pawaPay, Fincra"),
    (14, "Republic of the Congo", "CG", "XAF", "pawaPay, Fincra"),
    (15, "Gabon", "GA", "XAF", "pawaPay, Fincra"),
    (16, "DR Congo", "CD", "CDF/USD", "pawaPay, Fincra"),
    (17, "Malawi", "MW", "MWK", "pawaPay"),
    (18, "Mozambique", "MZ", "MZN", "pawaPay"),
    (19, "Sierra Leone", "SL", "SLE", "pawaPay"),
    (20, "Ethiopia", "ET", "ETB", "pawaPay"),
    (21, "Lesotho", "LS", "LSL", "pawaPay"),
    (22, "South Sudan", "SS", "SSP", "Fincra (payouts only)"),
    (23, "Zimbabwe", "ZW", "USD", "Fincra (payouts only)"),
]


def s14_risks(d):
    d.h1("14. Risk analysis", new_page=True)
    d.para("Likelihood and impact are assessed on the plan as it stands, after the mitigations already built "
           "into the model (MRR-gated hiring and launches, the capped paid-acquisition budget and the R3.0m "
           "minimum-cash buffer). Owners are to be assigned before this plan is issued.")
    d.table(["#", "Risk", "Likelihood", "Impact", "Mitigation", "Owner"], [
        ("R1", "**Trial volume below plan.** Demand at launch is weaker than the funnel assumes",
         "Medium", "High",
         "The model quantifies it: 30% below plan takes minimum cash to R0.98m. Pre-agreed response: raise the "
         "hiring and launch gate multiplier to 1.40× as in the Conservative case, which delays cost rather "
         "than requiring capital. About R8m of the seed is held as reserve", "[[OWNER]]"),
        ("R2", "**FX: the rand strengthens** against NGN, KES, GHS or USD", "Medium", "Medium",
         "Quarterly repricing at more than 10% drift restores parity. With repricing a 15% shock is "
         "immaterial; without it FY5 EBITDA falls R9.9m. Repricing discipline is a standing policy, not a "
         "decision taken under pressure", "[[OWNER]]"),
        ("R3", "**Meta dependency.** App Review is refused or delayed, or platform policy or pricing changes",
         "Medium", "High",
         "WhatsApp permissions, the commercial core, are already approved and Tech Provider verification is "
         "held. Nothing in review is sold as live, so no revenue in the plan depends on it. Channel mix "
         "(WhatsApp, Facebook, email, SMS, USSD, link-in-bio) reduces single-channel exposure, and stage 2 of "
         "the roadmap adds non-Meta networks", "[[OWNER]]"),
        ("R4", "**Payment rail concentration or settlement failure**", "Low", "High",
         "Five rails with overlapping coverage in the largest markets; South Africa has four. Settlement "
         "monitoring and reconciliation per rail, and no customer funds are held by FluxMuse. South Sudan and "
         "Zimbabwe stay gated until collection is confirmed", "[[OWNER]]"),
        ("R5", "**Competition.** A global platform adds WhatsApp commerce and local payments, or a local "
               "entrant undercuts", "Medium", "Medium",
         "Defensibility rests on verification, rail contracts, local pricing, multilingual AI and the partner "
         "channel (section 7). Price position at R499 is difficult to attack from above", "[[OWNER]]"),
        ("R6", "**Hiring and execution.** Key roles are not filled, or scale-up hiring outruns revenue",
         "Medium", "Medium",
         "Every non-founder role waits for an MRR gate, so payroll cannot outrun revenue by design. Country "
         "roles are hired locally around each launch", "[[OWNER]]"),
        ("R7", "**Regulatory and data protection.** POPIA, NDPR/NDPA, Kenya DPA or Ghana DPA breach, or a "
               "registration missed", "Low", "High",
         "Platform built POPIA, NDPR and GDPR ready; opt-in marketing with approved templates; registrations "
         "and local counsel funded from the expansion budget; legal and data-protection counsel hired at R2.0m "
         "net MRR; Information Officer appointed", "[[OWNER]]"),
        ("R8", "**AI cost.** Inference prices rise, or credit usage runs ahead of assumptions", "Medium",
         "Medium",
         "AI inference is modelled at R12 per 1,000 credits falling 10% a year at 40% utilisation, and credits "
         "are capped per tier with paid top-ups. Multi-provider architecture allows switching. Cost per credit "
         "is a monthly KPI", "[[OWNER]]"),
        ("R9", "**Key person.** The business depends on two founders",
         "Medium", "High",
         "Senior hires from the seed month (VP Engineering, Head of Growth, Head of Sales & Partnerships, CFO) "
         "spread the load. Documentation, access control and continuity: "
         "**[[KEY-PERSON COVER AND INSURANCE]]**", "[[OWNER]]"),
        ("R10", "**Pilot outcome.** Pilot brands do not convert or produce usable case studies", "Medium",
         "Medium",
         "Conversion is modelled at 75%, and the sensitivity shows the pre-seed bridge moves only from R63k to "
         "R52k across the 50% to 100% range. Case-study consent is agreed up front in exchange for pilot "
         "pricing", "[[OWNER]]"),
    ], [0.9, 3.9, 1.6, 1.4, 6.6, 1.6], "Risk register", size=8, first_col_bold=False)
    d.note("The model's own limitations are listed in Appendix E: fractional customers, one-way launch and "
           "hiring decisions, deterministic FX, no downgrades, and simplified tax and working capital.")


def s15_milestones(d):
    d.h1("15. Milestones and KPIs", new_page=True)
    d.h2("Timeline")
    d.para("Dates before 2027 are committed; later dates are **gated on revenue, not on the calendar**. Each "
           "market launch waits for last month's net MRR to clear its gate, and the launch follows two months "
           "later.")
    d.table(["When", "Milestone", "Gate or condition"], [
        ("Sept 2026", "All five payment rails live (pawaPay and Fincra from the week of 14 September)", "—"),
        ("Sept–30 Nov 2026", "Gauteng pilot: 12 brands", "—"),
        ("Q4 2026", "Meta App Review: Instagram, Pages posting, business management, ads", "Meta approval"),
        ("1 Dec 2026", "South Africa commercial launch; pilot brands convert; first case studies",
         "Pilot complete"),
        ("1 Dec 2026 – 31 Jan 2027", "Founding Member window, South Africa", "—"),
        ("Feb 2027", "R25m seed closes; hiring and paid acquisition begin", "Round closed"),
        ("FY2 (Oct 2027 – Sep 2028)",
         f"Nigeria {MKL['Nigeria']}, Kenya {MKL['Kenya']}, Ghana {MKL['Ghana']}",
         "Net MRR gates of R0.9m, R1.2m and R1.5m; country lead hired two months before each launch"),
        ("Nov 2028", "Rest of Africa: 19 countries, self-serve in US dollars", "R2.5m net MRR gate"),
        ("Oct 2028", "Operating cash flow turns positive", "—"),
        ("Mar 2029", "EBITDA break-even; positive every month from June 2029", "—"),
        ("FY5 (Oct 2030 – Sep 2031)",
         f"{ANN[4]['ending_paying_workspaces']:,} paying workspaces, "
         f"{rm(ANN[4]['subscription_arr_zar'], 0)} subscription ARR", "—"),
        ("Not scheduled", "Botswana and Namibia", "A payment rail must cover them first"),
    ], [3.4, 7.6, 6.0], "Milestones, Q4 2026 to FY5 (Base case)", size=9)
    d.source()

    d.h2("The KPI dashboard")
    d.para("Reported to investors **monthly**, within [[N]] working days of month end, against the model.")
    d.table(["KPI", "Why it matters", "Base case reference point"], [
        ("Trials started, by market and segment", "The leading indicator; the model's most sensitive input",
         "250 a month in South Africa at launch, growing 12% a month in FY1"),
        ("Trial-to-paid conversion", "Sets revenue and the cash buffer", "Solo 11%, SME 14%"),
        ("New paying workspaces and total paying workspaces", "The headline growth number",
         f"{ANN[0]['ending_paying_workspaces']} at the end of FY1"),
        ("Net subscription MRR", "Drives every hiring and launch gate",
         f"{rand(ANN[0]['subscription_mrr_sept_zar'])} in September 2027"),
        ("Monthly logo churn by segment and tier", "Solo Starter churn sets solo LTV:CAC",
         "Solo Starter 6.5%, SME Growth 3.0%, agency 2.0%"),
        ("CAC and CAC payback by segment", "The paid-spend switch is set on payback",
         f"FY3 blended CAC {rand(UE['blended']['cac_zar'])}, payback "
         f"{UE['blended']['cac_payback_months']} months"),
        ("LTV:CAC by segment", "Where to put the next rand", f"FY3 blended {UE['blended']['ltv_to_cac']}×"),
        ("Paid acquisition spend against the cap", "Shows growth is still self-financing",
         f"{pct(ANN[0]['paid_acquisition_funded_by_cap_pct'])} of desired spend funded in FY1"),
        ("Gross margin and software gross margin", "AI and messaging cost control",
         f"FY1 {pct(ANN[0]['gross_margin_pct'])} / {pct(ANN[0]['software_gross_margin_pct'])}"),
        ("EBITDA and operating cash flow", "Progress to break-even", "Break-even March 2029"),
        ("Closing cash against the R3.0m buffer", "The constraint the whole plan is built around",
         f"Low of {rm(CASH['min_post_seed_cash_zar'], 2)} in {CASH['min_post_seed_cash_month']}"),
        ("Headcount against the MRR gates", "Confirms cost discipline is holding",
         f"{D['headcount_total_fy_end'][0]} at the end of FY1"),
        ("Agency partners signed and their client sub-accounts", "Channel health",
         f"{ANN[0]['ending_customers_by_segment']['Agencies']} agencies by the end of FY1"),
        ("WhatsApp conversations, orders and GMV on the platform", "Proves the commerce claim",
         "Pilot KPIs from December 2026"),
        ("Meta App Review status", "The largest platform dependency", "Stage 1 of the roadmap"),
    ], [4.4, 5.0, 7.6], "Monthly KPI dashboard", size=8.5)


def s16_impact(d):
    d.h1("16. Social and economic impact", new_page=True)
    d.para("This section is written for development-finance funders. **Every claim below is either a modelled "
           "figure or a measurement commitment.** Where we cannot yet measure something, the plan says so and "
           "states how it will be measured, rather than asserting an outcome.")

    d.h2("SMME enablement")
    d.bullets([
        f"The Base case puts **{ANN[4]['ending_paying_workspaces']:,} small and medium businesses** on the "
        f"platform by FY5, of which {ANN[4]['ending_customers_by_segment']['Solo']:,} are solo entrepreneurs "
        "on the entry tier.",
        "The entry price is **R499 a month**, with a 14-day free trial and no card required, which puts a "
        "marketing capability inside the reach of a business that could never fund an agency retainer.",
        "The measurable outcomes for a customer are orders, GMV and hours saved, tracked per workspace in the "
        "product. **[[BASELINE AND TARGET FOR AVERAGE REVENUE UPLIFT PER CUSTOMER: TO BE MEASURED FROM PILOT "
        "DATA, DECEMBER 2026]]**",
    ])

    d.h2("Digital and financial inclusion")
    d.bullets([
        "Customers sell and get paid inside **WhatsApp**, on the phone they already own, without needing a "
        "website, a card machine or a storefront.",
        "**Five payment rails across 23 countries**, including mobile money in 20 of them, bring instant EFT, "
        "cards, bank transfer, USSD and mobile money into reach for informal and semi-formal traders.",
        "**USSD and SMS** channels reach customers who are not on smartphones.",
        "Coverage deliberately follows what a rail can actually collect, so no business is sold a service it "
        "cannot pay for.",
    ])

    d.h2("Local languages")
    d.para("The Creator agent produces content in **isiZulu, Pidgin, Swahili, Afrikaans and English, among "
           "others**. For a township or market business, marketing in the language its customers speak is the "
           "difference between a post that works and one that does not. This is a product capability today, "
           "not a roadmap item.")

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
        "accessible entry-level positions in the plan, and the natural route into the technology sector for "
        "young people without a degree.",
        f"**{D['headcount_by_dept_fy_end']['Country teams'][4]} country-team roles** in Nigeria, Kenya and "
        "Ghana, all hired locally.",
        "**Indirect employment** through agency partners, who serve more clients with the same team, is not "
        "counted here. **[[MEASUREMENT PLAN FOR INDIRECT JOBS THROUGH PARTNERS]]**",
    ])

    d.h2("Women- and youth-owned businesses")
    d.para("The launch segments are weighted towards categories in which women- and youth-owned businesses are "
           "strongly represented in South Africa: beauty and braiding, fashion resale, home baking, nails and "
           "lashes, and personal training. The lead pilot case study is a braiding and hair studio.")
    d.para("**We do not yet have data, and will not claim any.** From the pilot onward we will measure reach "
           "with a voluntary, POPIA-compliant question at onboarding, and report: "
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
        "Customer-level figures aggregated and anonymised; no brand named without written consent; customer "
        "names and phone numbers blurred in any screenshot (POPIA).",
        "Aggregate pilot results reported only where at least 8 of the 12 brands provide data, stating the "
        "period and how each figure was measured.",
        "**[[IMPACT REPORTING FORMAT AND FREQUENCY AGREED WITH THE FUNDER]]**",
    ])


# ---------------------------------------------------------------- appendices
def appendices(d):
    d.h1("Appendix A. Pricing tables", new_page=True)
    d.h2("Monthly prices by market")
    hdr = ["Plan", "South Africa (ZAR)", "Nigeria (NGN)", "Kenya (KES)", "Ghana (GHS)", "USD markets"]
    w = [2.6, 2.9, 2.9, 2.9, 2.9, 2.8]
    al = [None, "right", "right", "right", "right", "right"]
    d.table(hdr, [
        ("Starter", "R499", "₦41,000", "KSh 3,999", "GH₵ 339", "$27"),
        ("Growth", "R1,999", "₦165,000", "KSh 15,999", "GH₵ 1,359", "$109"),
        ("Scale", "R4,999", "₦413,000", "KSh 39,999", "GH₵ 3,399", "$269"),
        ("Agency", "R7,999", "₦662,000", "KSh 64,499", "GH₵ 5,439", "$429"),
        ("Enterprise (from)", "R19,999", "₦1,650,000", "KSh 161,000", "GH₵ 13,600", "$1,099"),
    ], w, "Monthly prices by market", size=9, aligns=al)
    d.h2("Annual prices (10× monthly)")
    d.table(hdr, [
        ("Starter", "R4,990", "₦410,000", "KSh 39,990", "GH₵ 3,390", "$270"),
        ("Growth", "R19,990", "₦1,650,000", "KSh 159,990", "GH₵ 13,590", "$1,090"),
        ("Scale", "R49,990", "₦4,130,000", "KSh 399,990", "GH₵ 33,990", "$2,690"),
        ("Agency", "R79,990", "₦6,620,000", "KSh 644,990", "GH₵ 54,390", "$4,290"),
        ("Enterprise", "Custom", "Custom", "Custom", "Custom", "Custom"),
    ], w, "Annual prices by market", size=9, aligns=al)
    d.h2("Partner wholesale, Founding Member and pilot prices")
    d.table(["Item", "ZAR", "NGN", "KES", "GHS", "USD"], [
        ("Partner wholesale, Agency tier, monthly", "R5,599", "₦463,000", "KSh 44,999", "GH₵ 3,799", "$299"),
        ("Partner wholesale, annual", "R55,990", "₦4,630,000", "KSh 449,990", "GH₵ 37,990", "$2,990"),
        ("Founding Member: Starter, first 2 monthly bills", "R349", "—", "—", "—", "—"),
        ("Founding Member: Growth, first 2 monthly bills", "R1,399", "—", "—", "—", "—"),
        ("Founding Member: Scale, first 2 monthly bills", "R3,499", "—", "—", "—", "—"),
        ("Pilot brands: Starter, first 2 monthly bills", "R249", "—", "—", "—", "—"),
        ("Pilot brands: Growth, first 2 monthly bills", "R999", "—", "—", "—", "—"),
        ("Pilot brands: Scale, first 2 monthly bills", "R2,499", "—", "—", "—", "—"),
        ("Pilot brands: Agency, first 2 monthly bills", "R3,999", "—", "—", "—", "—"),
    ], [6.2, 2.4, 2.6, 2.4, 2.0, 1.4], "Partner, Founding Member and pilot prices", size=8.5,
        aligns=[None, "right", "right", "right", "right", "right"])
    d.bullets([
        "Founding Member applies in local currency at the same 30% off the first two monthly bills in Nigeria, "
        "Kenya and Ghana, inside each country's 60-day window. It is never offered on the Agency tier.",
        "Local price points are set at parity with ZAR at early-September 2026 rates and reviewed quarterly.",
        "USD markets are the 19 rail-covered countries other than South Africa, Nigeria, Kenya and Ghana.",
        "The live app currently converts ZAR at the day's rate and has no Ghana region yet; fixed local pricing "
        "is a roadmap item. Quote this table, and say “billed in local currency”.",
    ])

    d.h1("Appendix B. Payment rails and country coverage", new_page=True)
    d.table(["#", "Country", "ISO", "Currency", "Rails", "Billing currency"],
            [(str(n), name, iso, cur, rails,
              {"ZA": "ZAR", "NG": "NGN", "KE": "KES", "GH": "GHS"}.get(iso, "USD"))
             for n, name, iso, cur, rails in COUNTRIES],
            [0.9, 4.2, 1.1, 1.9, 5.9, 3.0], "The 23 rail-covered countries", size=8.5,
            first_col_bold=False)
    d.bullets([
        "**All five rails are live in September 2026** (pawaPay and Fincra from the week of 14 September).",
        "**South Sudan and Zimbabwe are payouts-only** through Fincra. They stay gated for sales until "
        "subscription collection is confirmed. **[[CONFIRM WITH FINCRA]]**",
        "**Botswana (BWP) and Namibia (NAD) are coming soon**: they appear in the app's region picker and in "
        "materials, but no secured rail covers them yet, so they are never shown as live payment markets. "
        "Headline counts stay 5 rails · 23 countries, plus 2 coming soon.",
        "Every other country, including all countries outside Africa, is **waitlist only**: no prices, no "
        "checkout.",
    ])

    d.h1("Appendix C. Gauteng pilot and case-study template", new_page=True)
    d.h2("The pilot")
    d.table(["Item", "Detail"], [
        ("Brands", "12, in Gauteng"),
        ("Period", "September to 30 November 2026"),
        ("Cost to brands", "Nothing during the pilot"),
        ("Suggested mix", "5 solo entrepreneurs, 5 SMEs, 2 agencies (archetypes; the real roster replaces this)"),
        ("Lead case study", "A braiding and hair studio: solo entrepreneur on Starter, short booking cycles, "
                            "decisions made by one owner"),
        ("Conversion", "From 1 December 2026 on pilot terms (50% off the first two monthly bills) in exchange "
                       "for a case study and logo permission"),
        ("Modelled conversion", f"{M['pilot']['conversion_pct']}% "
                                f"({M['pilot']['converting_brands']:.0f} brands) **[[CONFIRM]]**"),
        ("Results available", "December 2026"),
        ("Pilot name", "[[PILOT NAME]]"),
    ], [4.0, 13.0], "Gauteng pilot plan", size=9)
    d.h2("Case-study template")
    d.para("Each case study follows this structure. **Every metric is a placeholder until measured, and target "
           "columns are labelled as goals, never as results.**")
    d.table(["KPI", "Baseline", "Target (goal)", "Actual"], [
        ("WhatsApp conversations handled", "[[ ]]", "[[ ]]", "[[ ]]"),
        ("Median first-reply time", "[[ ]]", "[[ ]]", "[[ ]]"),
        ("Bookings or orders via WhatsApp", "[[ ]]", "[[ ]]", "[[ ]]"),
        ("Deposits or payments collected in chat (R)", "[[ ]]", "[[ ]]", "[[ ]]"),
        ("Posts published per month", "[[ ]]", "[[ ]]", "[[ ]]"),
        ("Owner or staff hours saved per week", "[[ ]]", "[[ ]]", "[[ ]]"),
        ("Repeat-customer rate", "[[ ]]", "[[ ]]", "[[ ]]"),
        ("NPS", "[[ ]]", "[[ ]]", "[[ ]]"),
    ], [7.4, 3.2, 3.2, 3.2], "Case-study KPI template", size=9,
        aligns=[None, "center", "center", "center"])
    d.figure("infographics/case-study-template.png",
             "The case-study layout, with placeholder fields and a pilot-data-pending stamp.",
             "Designed case-study page for the Gauteng braiding and hair studio with placeholder fields for "
             "brand, area, challenge, set-up and three metrics labelled Target (goal), an owner quote "
             "placeholder, and a stamp reading pilot data pending, December 2026.")
    d.bullets([
        "Aggregate pilot figures need data from at least 8 of the 12 brands, and must state the period and how "
        "each figure was measured.",
        "No brand name, logo or photograph is used without signed consent; customer names and phone numbers "
        "are blurred in every screenshot.",
        "Until 30 November 2026 all materials say “pilot underway, results December 2026”.",
    ])

    d.h1("Appendix D. Detailed financial tables", new_page=True)
    d.h2("Annual profit and loss")
    d.fy_table("Annual P&L (R, Base case)", [
        ["Subscriptions (gross)"] + [rand(a["subscriptions_gross_zar"]) for a in ANN],
        ["less Founding Member discount"] + [f"({rand(a['founding_member_discount_zar'])})" for a in ANN],
        ["less pilot discount"] + [f"({rand(a['pilot_discount_zar'])})" for a in ANN],
        ["Subscriptions (net)"] + [rand(a["revenue_by_stream_zar"]["subscriptions"]) for a in ANN],
        ["AI-credit top-ups"] + [rand(a["revenue_by_stream_zar"]["ai_credit_topups"]) for a in ANN],
        ["WhatsApp messaging"] + [rand(a["revenue_by_stream_zar"]["whatsapp_messaging"]) for a in ANN],
        ["Enterprise setup fees"] + [rand(a["revenue_by_stream_zar"]["enterprise_setup_fees"]) for a in ANN],
        ["Agency setup fees"] + [rand(a["revenue_by_stream_zar"]["agency_setup_fees"]) for a in ANN],
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
    ], first_header="R", size=7.5, total_rows=(8, 10, 17, 18, 20), widths=[5.0] + [2.4] * 5)
    d.source()
    d.h2("Cost of revenue detail")
    cf = D["cash_flow_rows_fy_sum"]
    d.fy_table("Cost of revenue (R, Base case)", [
        ["AI inference"] + [rand(v) for v in cf["cogs_ai"]],
        ["Hosting"] + [rand(v) for v in cf["cogs_hosting"]],
        ["WhatsApp Meta fees (pass-through)"] + [rand(v) for v in cf["cogs_wa"]],
        ["Payment processing"] + [rand(v) for v in cf["cogs_proc"]],
        ["Variable support"] + [rand(v) for v in cf["cogs_support"]],
        ["Customer success team"] + [rand(v) for v in cf["cogs_cs_team"]],
        ["**Total cost of revenue**"] + [rand(v) for v in cf["cogs_total"]],
    ], first_header="R", size=8, total_rows=(6,), widths=[5.0] + [2.4] * 5)
    d.source()
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
    d.h2("Headcount and payroll by department")
    d.fy_table("Payroll by department (R, Base case)",
               [[dep] + [rand(v) for v in D["payroll_by_dept_zar_fy"][dep]]
                for dep in D["payroll_by_dept_zar_fy"]],
               first_header="R", size=8, widths=[5.0] + [2.4] * 5)
    d.source()
    d.note("Customer-success payroll sits in cost of revenue, not operating expenses, so it appears in the "
           "cost-of-revenue table above as well.")
    d.h2("Workspaces by segment, market and tier")
    d.fy_table("Paying workspaces at year end (Base case)",
               [[f"{k}"] + [f"{a['ending_customers_by_segment'][k]:,}" for a in ANN]
                for k in ANN[0]["ending_customers_by_segment"]] +
               [[f"{k}"] + [f"{a['ending_customers_by_market'][k]:,}" for a in ANN]
                for k in ANN[0]["ending_customers_by_market"] if k != "Botswana & Namibia"] +
               [["**Total paying workspaces**"] + [f"{a['ending_paying_workspaces']:,}" for a in ANN]],
               first_header="Workspaces", size=8.5, total_rows=(9,), widths=[5.0] + [2.4] * 5)
    d.source()
    d.note("Botswana, Namibia and every gated country are zero in all five years.")

    d.h1("Appendix E. Model assumptions and open confirmations", new_page=True)
    d.callout("Internal section: remove before sending to an external party", [
        "Appendix E lists assumptions that still need founder sign-off. Delete this appendix, or delete the "
        "open-confirmations table below, before the plan goes to an investor or funder.",
    ], fill="FFF1A8", accent=DEEP, caption="Layout: internal-only banner")
    d.h2("Key assumptions")
    d.numbered(M["key_assumptions"])
    d.h2("Not modelled")
    d.bullets(M["not_modelled"])
    d.h2("Known limitations of the model")
    d.bullets([
        "Customers are fractional, and launch and hiring decisions are one-way: once taken they are never "
        "reversed.",
        "Gates use last month's MRR, with no look-ahead.",
        "There are no downgrades; upgrades run only Starter → Growth and Growth → Scale.",
        "Agency client growth adds no revenue beyond the partner's own subscription and usage.",
        "FX paths are deterministic, and repricing is assumed to cause no extra churn.",
        "WhatsApp pass-through is booked as gross revenue, which lowers blended gross margin.",
        "Tax ignores South Africa's 80% cap on the use of assessed losses; depreciation, amortisation, "
        "interest, VAT and payables are ignored; receivables and deferred revenue are simplified.",
    ])
    d.h2("Open confirmations (founder)")
    d.table(["#", "To confirm"], [(str(i + 1), t) for i, t in enumerate(M["founder_confirmations_needed"])],
            [0.9, 16.1], "Founder confirmations still open", size=8.5, first_col_bold=False)
    d.h2("What the pilot replaces first")
    d.numbered([
        "Trial-to-paid conversion by segment (solo 11%, SME 14%), the solo/SME split, and pilot conversion "
        "(75%).",
        "Trial volume at launch (250 a month in South Africa) and early growth (12% a month).",
        "Month-1 to month-3 churn by segment; solo Starter at 6.5% sets solo's 3.0× LTV:CAC.",
        "Paid CAC by segment, and the Founding Member sign-up uplift, measured in the South African window.",
        "Agency behaviour: agencies signed per partnerships manager, and uptake of partner wholesale.",
        "Usage costs: billable WhatsApp messages, AI-credit utilisation and support contacts per workspace.",
        "Nigeria, Kenya and Ghana inputs: trials at launch, CAC and churn indices, and actual FX drift.",
        "Merchant GMV and whether merchants accept a commerce fee (Upside only).",
    ])

    d.h1("Appendix F. Glossary", new_page=True)
    d.table(["Term", "Meaning"], [
        ("ARPA", "Average revenue per account, per month"),
        ("ARR", "Annual recurring revenue: September net subscription MRR × 12"),
        ("B-BBEE", "Broad-Based Black Economic Empowerment (South Africa)"),
        ("CAC", "Customer acquisition cost"),
        ("CAC payback", "Months of gross profit needed to recover the CAC"),
        ("Cloud API", "Meta's hosted WhatsApp Business API"),
        ("EBITDA", "Earnings before interest, tax, depreciation and amortisation"),
        ("Edge function", "Server-side function running close to the user, here on Supabase"),
        ("Founding Member", "The 60-day launch offer: 30% off the first two monthly bills, or two extra months "
                            "on annual plans"),
        ("FY", "Fiscal year, October to September. FY1 is October 2026 to September 2027"),
        ("Gated country", "A country with no rail that can collect: waitlist only, no prices, no checkout"),
        ("GMV", "Gross merchandise value: the value of orders transacted by customers"),
        ("Instant EFT", "Pay-by-bank transfer confirmed in real time"),
        ("LTV", "Lifetime value: ARPA × software gross margin ÷ monthly churn"),
        ("Mobile money", "Payment from a mobile-network wallet, dominant across much of Africa"),
        ("MRR", "Monthly recurring revenue"),
        ("MRR gate", "The net MRR a hire or a market launch must wait for before it happens"),
        ("MSME / SMME", "Micro, small and medium enterprise. SMME is the South African usage"),
        ("NDPR / NDPA", "Nigeria's data-protection regulation and act"),
        ("Partner wholesale", "The permanent Agency-tier price for programme partners: R5,599 a month"),
        ("POPIA", "Protection of Personal Information Act, 2013 (South Africa)"),
        ("RAG", "Retrieval-augmented generation: the Analyst agent's memory of past campaigns"),
        ("RLS", "Row-level security: database access rules enforced per row"),
        ("SAM", "Serviceable addressable market"),
        ("SOM", "Serviceable obtainable market"),
        ("TAM", "Total addressable market"),
        ("Tech Provider", "Meta's verified status for a platform acting for other businesses"),
        ("USSD", "Menu-based mobile service that works on any phone, without internet"),
        ("Workspace", "One paying customer account on FluxMuse"),
    ], [4.0, 13.0], "Glossary", size=9)
