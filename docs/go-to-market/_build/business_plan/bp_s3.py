"""Sections 9-11: pricing, operations, management and organisation."""
from bp_doc import ANN, D, M, TINT, pct, rand, rk, rm

PT = M["price_tables"]
PW = PT["partner_wholesale_monthly"]
MK = M["markets"]
DEPTS = list(D["headcount_by_dept_fy_end"].keys())


def s9_pricing(d):
    d.h1("9. Pricing strategy", new_page=True)
    d.para("Base currency is the South African rand. Annual plans cost 10× the monthly price, so two months "
           "are free. A 14-day free trial with no card comes before any plan.")

    d.h2("Plans")
    d.table(["Plan", "Monthly (ZAR)", "Annual (ZAR)", "Brands", "Channels", "AI credits/mo", "For"], [
        ("Starter", "R499", "R4,990", "1", "3", "5,000", "Solo founders; community support"),
        ("Growth", "R1,999", "R19,990", "3", "15", "25,000",
         "E-commerce and WhatsApp commerce, USSD, integrations; email support"),
        ("Scale", "R4,999", "R49,990", "10", "40", "100,000",
         "API access, white-label reports, priority support"),
        ("Agency", "R7,999", "R79,990", "Unlimited", "80", "500,000",
         "Full white-label, 50 sub-accounts, reseller billing"),
        ("Enterprise", "from R19,999", "Custom", "Unlimited", "Unlimited", "Unlimited",
         "SSO, SLA, dedicated AI, 24×7; inbound only"),
    ], [2.1, 2.3, 2.2, 1.7, 1.7, 2.2, 4.8], "Plans and list prices (ZAR)", size=8.5,
        aligns=[None, "right", "right", "right", "right", "right", None])

    d.h2("Local pricing")
    d.para("Nigeria, Kenya and Ghana are billed in **fixed local price points**, set at parity with the ZAR "
           "price at early-September 2026 rates (1 ZAR = ₦82.83 = KSh 8.07 = GH₵ 0.68), not at the day's "
           "exchange rate. The other 19 rail-covered countries are billed in **US dollars** at R18.50 = US$1.")
    d.figure("infographics/pricing-regional.png",
             "One set of plans, priced for each market.",
             "Monthly prices per plan: Starter R499, ₦41,000, KSh 3,999, GH₵ 339, $27; Growth R1,999, "
             "₦165,000, KSh 15,999, GH₵ 1,359, $109; Scale R4,999, ₦413,000, KSh 39,999, GH₵ 3,399, $269; "
             "Agency R7,999, ₦662,000, KSh 64,499, GH₵ 5,439, $429. Annual is ten times monthly, USD applies "
             "in 19 other rail-covered countries, other countries join the waitlist, prices reviewed quarterly.")

    d.h2("Repricing policy")
    d.bullets([
        "Local prices are **reviewed quarterly**. If the rand value of a local price has drifted more than "
        "**10%**, the price is reset to parity, using the rate observed a quarter earlier.",
        "A **6% list-price escalator** applies each October in all markets.",
        "The model assumes annual depreciation against the rand of NGN −10%, GHS −8%, KES −3% and USD 0% "
        "(**[[CONFIRM FX ASSUMPTIONS]]**).",
        "Section 12 shows why this discipline matters: in a 15% rand-strengthening shock, repricing is the "
        "difference between a one-quarter dip and a R9.9m hit to FY5 EBITDA.",
    ])

    d.h2("Partner wholesale")
    d.table(["", "ZAR", "NGN", "KES", "GHS", "USD"], [
        ("Agency list, monthly", "R7,999", "₦662,000", "KSh 64,499", "GH₵ 5,439", "$429"),
        (f"Partner wholesale, monthly (−{PW['discount_vs_agency_list_pct']}%)", rand(PW["ZAR"]),
         f"₦{PW['NGN']:,}", f"KSh {PW['KES']:,}", f"GH₵ {PW['GHS']:,}", f"${PW['USD']}"),
        ("Partner wholesale, annual", "R55,990", "₦4,630,000", "KSh 449,990", "GH₵ 37,990", "$2,990"),
    ], [5.0, 2.4, 2.7, 2.5, 2.4, 2.0], "Partner wholesale pricing", size=9,
        aligns=[None, "right", "right", "right", "right", "right"])
    d.note("The partner price is a permanent wholesale price for the Agency tier, not a launch discount. The "
           "model assumes 100% of agency-segment customers buy at it (**[[CONFIRM]]**). Whether partners earn "
           "a commission on clients they refer onto their own Starter, Growth or Scale plans is "
           "**[[FOUNDER DECISION: REFERRAL COMMISSION %]]** and is not modelled.")

    d.h2("Discounts")
    d.bullets([
        "**One launch offer only**: Founding Member, 60 days per market, on Starter, Growth and Scale.",
        "**Pilot brands** get deepened terms (50% off the first two monthly bills from 1 December 2026) in "
        "exchange for a case study and logo permission. This is not a public offer.",
        "**No stacking.** Founding Member does not combine with partner wholesale pricing, and is never "
        "offered on the Agency tier.",
        "**Perks duration** (badge and priority support) is **[[FOUNDER DECISION: PERKS DURATION]]**. Until it "
        "is decided, materials state the perks with no duration.",
    ])

    d.h2("Market gating")
    d.para("Prices and checkout are shown **only** in the 23 countries where a secured rail can collect. "
           "Botswana and Namibia appear as coming soon; South Sudan and Zimbabwe are payouts-only through "
           "Fincra and stay gated until subscription collection is confirmed "
           "(**[[CONFIRM FINCRA COLLECTION FOR SOUTH SUDAN AND ZIMBABWE]]**). Everywhere else, including all "
           "countries outside Africa, visitors may join a waitlist but cannot buy.")

    d.h2("A fee that is not in pricing today")
    d.para("A **0.75% commerce fee** on WhatsApp-checkout GMV is modelled in the Upside scenario only. It is "
           "**not part of current pricing**, is not assumed in the Base or Conservative cases, and would need "
           "both a product change and evidence that merchants accept it.")


def s10_operations(d):
    d.h1("10. Operations", new_page=True)
    d.h2("Technology and architecture")
    d.bullets([
        "**Front end**: React with Vite, deployed on Vercel; installable as a progressive web app.",
        "**Back end**: Supabase, providing Postgres, authentication and more than 140 edge functions.",
        "**Security**: row-level security on every table, encrypted third-party access tokens, audit export.",
        "**Integrations**: WhatsApp Cloud API, Meta Graph API, five payment providers, Shopify, WooCommerce, "
        "Takealot, HubSpot, accounting sync, Slack, Zapier and a public API.",
        "**Why it scales cheaply**: managed infrastructure with per-workspace costs, so hosting grows with "
        "customers instead of ahead of them. Hosting is modelled at R30,000 a month plus R35 per workspace "
        "after the seed.",
    ])

    d.h2("Meta platform dependency and the App Review plan")
    d.para("FluxMuse depends on Meta for WhatsApp and for Facebook and Instagram publishing. Business and "
           "Access Verification (Tech Provider) are already held, and WhatsApp messaging and management "
           "permissions are approved. The permissions still in App Review are the first item on the product "
           "roadmap. Until each is approved it stays switched off, and no customer is sold it.")
    d.table(["Stage", "Scope"], [
        ("1. Meta permissions (Q4 2026)",
         "Instagram publishing, comments and DMs; Pages posting and engagement insights; business management; "
         "ads"),
        ("2. Social adapters", "Instagram Login, Threads, LinkedIn, X, TikTok, YouTube, Pinterest"),
        ("3. Business app integrations", "Commerce, CRM, accounting, email and SMS providers"),
        ("4. Flux_Partner programme", "Referral tracking, white-label, partner-managed workspaces"),
    ], [5.4, 11.6], "Product roadmap, in the founder's agreed order", size=9.5)
    d.note("Timing beyond Q4 2026 is indicative and depends on Meta approvals and team capacity.")

    d.h2("Payment rails and settlement")
    d.table(["Rail", "Type", "Countries"], [
        ("Yoco", "Card acquiring, tap-to-pay", "South Africa"),
        ("Ozow", "Instant EFT / pay-by-bank", "South Africa"),
        ("Paystack", "Cards, bank transfer, USSD, mobile money",
         "Nigeria, Ghana, South Africa, Kenya, Côte d'Ivoire, Rwanda"),
        ("pawaPay", "Mobile money collections and payouts, 40+ mobile network operators", "20 countries"),
        ("Fincra", "Collections (virtual accounts, cards, bank, mobile money) and payouts",
         "Collections hubs: Nigeria, Ghana, Kenya, Uganda, South Africa. African payouts across West, Central "
         "and East Africa, plus South Sudan and Zimbabwe"),
    ], [2.4, 6.0, 8.6], "The five secured payment rails", size=9)
    d.figure("infographics/payment-coverage-map.png",
             "Coverage: 23 countries, with Botswana and Namibia coming soon.",
             "Tile map of 23 African countries coloured by how many of the five rails cover them, with South "
             "Africa the only four-rail country, Botswana and Namibia shown as dashed coming-soon tiles, and "
             "stat cards for five live payment rails, 23 countries covered, plus two coming soon and 40-plus "
             "mobile money operators.")
    d.bullets([
        "**All five rails are live in September 2026** (pawaPay and Fincra from the week of 14 September), so "
        "market expansion depends on sales capacity, not payments.",
        "**Settlement** runs through each provider to the company's bank accounts; FluxMuse does not hold "
        "customer funds. Settlement timing and reconciliation by rail: "
        "**[[SETTLEMENT TERMS AND RECONCILIATION PROCESS PER RAIL]]**.",
        "**Processing cost** is modelled at 2.9%, plus 1.5% for mobile money and FX on non-South African "
        "revenue.",
        "Appendix B lists all 23 countries, their currencies and their rails.",
    ])

    d.h2("Customer onboarding and support")
    d.bullets([
        "**Solo**: self-serve 14-day trial, in-product onboarding, community support.",
        "**SME**: trial plus a guided onboarding call; email support, priority on Scale.",
        "**Agency**: demo, a pilot client, then white-label setup with dedicated support.",
        "A customer success team is hired from the seed month and sits in cost of revenue, not operating "
        f"expenses: {D['headcount_by_dept_fy_end']['Customer success'][0]} people at the end of FY1 rising to "
        f"{D['headcount_by_dept_fy_end']['Customer success'][4]} by FY5.",
        "Support cost is modelled at R50 per workspace per month on top of that team.",
    ])

    d.h2("Data protection and security")
    d.bullets([
        "Built to be POPIA, NDPR and GDPR ready; row-level security on every table; encrypted tokens; audit "
        "export; data export and account deletion on request.",
        "Marketing messages go only to contacts who opted in, using Meta-approved templates, with an opt-out "
        "in every broadcast and suppression lists kept in the platform.",
        "Screenshots and case studies blur customer names and phone numbers.",
        "A security and compliance engineer is hired in the plan once net MRR passes R2.5m, and legal and "
        "data-protection counsel once it passes R2.0m.",
        "**[[SECURITY POLICY, BREACH-RESPONSE PLAN, PENETRATION TEST AND HOSTING REGIONS: TO CONFIRM]]**",
    ])

    d.h2("Suppliers and key partners")
    d.table(["Partner", "Role", "Dependency"], [
        ("Meta", "WhatsApp Cloud API, Facebook and Instagram", "High: see section 14"),
        ("Supabase and Vercel", "Database, authentication, edge functions, hosting", "Medium: replaceable, "
                                                                                     "with effort"),
        ("AI model providers", "Inference behind the agents", "Medium: cost and availability; multi-provider "
                                                              "by design"),
        ("Yoco, Ozow, Paystack, pawaPay, Fincra", "Collections and payouts",
         "Medium: overlapping coverage in the larger markets"),
        ("Agency partners", "White-label distribution", "Builds over time"),
    ], [4.4, 7.0, 5.6], "Key suppliers and partners", size=9)


def s11_management(d):
    d.h1("11. Management and organisation", new_page=True)
    d.h2("Founders and team")
    d.table(["Role", "Name", "Background and responsibility"], [
        ("Founder & CEO", "[[FOUNDER NAME]]", "[[BACKGROUND, YEARS OF EXPERIENCE, RESPONSIBILITY]]"),
        ("CTO / founding engineer", "[[CTO NAME]]", "[[BACKGROUND, RESPONSIBILITY]]"),
        ("[[ROLE]]", "[[NAME]]", "[[BACKGROUND, RESPONSIBILITY]]"),
    ], [4.0, 4.0, 9.0], "Founders and senior team", size=9.5)
    d.para("Both founders are on reduced salaries until the seed lands (R45,000 and R55,000 cost to company a "
           "month), which is what keeps the pre-seed burn small.")
    d.para("**Advisors.** [[ADVISORS: NAMES, AREAS AND WHAT THEY CONTRIBUTE]]")

    d.h2("Governance")
    d.bullets([
        "Board composition after the round: **[[BOARD COMPOSITION AND INVESTOR RIGHTS]]**.",
        "Reporting: monthly management accounts and the KPI dashboard in section 15; quarterly board meetings "
        "(**[[CONFIRM REPORTING CADENCE WITH INVESTORS]]**).",
        "Financial controls: **[[SIGNING AUTHORITY, APPROVAL LIMITS, PAYROLL AND PAYMENT CONTROLS]]**.",
        "A finance and compliance manager is hired early (from R150,000 net MRR), a finance analyst and people "
        "partner later, and a CFO at R8m net MRR.",
    ])

    d.h2("The hiring plan")
    d.para("**Nobody is hired on a calendar date alone.** Every non-founder role waits for three things: its "
           "earliest month, the seed, and last month's net MRR clearing that role's gate. In the Conservative "
           "scenario every gate rises by 40%, which is how the plan survives a slower market without extra "
           "funding.")
    d.fy_table("Headcount by department at each year end (Base case)",
               [[dep] + [str(v) for v in D["headcount_by_dept_fy_end"][dep]] for dep in DEPTS] +
               [["Total headcount"] + [str(v) for v in D["headcount_total_fy_end"]]],
               first_header="Department", total_rows=(len(DEPTS),))
    d.source("FluxMuse Financial Model v2 (Base case), derived from the model's headcount rows.")
    d.para(f"**Jobs created.** The plan grows from 2 founders to **{D['headcount_total_fy_end'][0]} people by "
           f"the end of FY1** and **{D['headcount_total_fy_end'][4]} by FY5**, of which "
           f"{D['headcount_by_dept_fy_end']['Country teams'][4]} are country-team roles in Nigeria, Kenya and "
           f"Ghana and {D['headcount_by_dept_fy_end']['Customer success'][4]} are customer-success roles, "
           "which are the most accessible entry-level positions in the plan. Section 16 sets out the "
           "development-impact view.")

    d.h2("When each role is hired")
    d.para("The table shows the first month each role group is hired in the Base case, and the net MRR gate it "
           "waits for. Country-team roles are tied to their market's launch decision rather than to an MRR "
           "gate of their own.")
    rows = []
    for r in sorted(D["roles"], key=lambda r: (r["fy"], r["role"])):
        if r["dept"] == "Leadership":
            continue
        gate = rand(r["mrr_gate_zar"]) if r["mrr_gate_zar"] else "Tied to market launch"
        rows.append((r["fy"], r["first_month"], str(r["count"]), r["role"], gate))
    d.table(["FY", "First hired", "FTE", "Role", "Net MRR gate"], rows,
            [1.2, 2.3, 1.0, 9.5, 3.0], "Hiring plan: first hire month and MRR gate (Base case)", size=8,
            first_col_bold=False, aligns=[None, None, "right", None, "right"])
    d.source()
