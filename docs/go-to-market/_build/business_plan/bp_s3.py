"""Sections 9-11: pricing, operations, management and organisation."""
from bp_doc import ANN, D, M, MV, TINT, pct, rand, rk, rm

PT = M["price_tables"]
PW = PT["partner_wholesale_monthly"]
ZAR = PT["zar_list_monthly"]
LM = PT["local_monthly"]
FMB = PT["founding_member_first_2_bills_zar"]
MK = M["markets"]
DEPTS = list(D["headcount_by_dept_fy_end"].keys())
PAID = ["Nano", "Micro", "Starter", "Growth", "Scale", "Corporate", "Agency"]
SPEC = {"Free": ("1", "1", "Permanent plan, not a trial; no card"),
        "Nano": ("1", "3", "Entry paid plan for side hustles"),
        "Micro": ("1", "4", "1 WhatsApp number"),
        "Starter": ("1", "3", ""),
        "Growth": ("3", "15", "+ inbound AI Voice (beta)"),
        "Scale": ("10", "40", "+ inbound and outbound AI Voice (beta)"),
        "Corporate": ("25", "60", "Bring your own cloud"),
        "Agency": ("Unlimited", "80", "Bring your own cloud, white-label, multi-client"),
        "Custom": ("—", "—", "Sold by consultation")}


def s9_pricing(d):
    d.h1("9. Pricing strategy", new_page=True)
    d.para("Base currency is the South African rand. Annual plans cost 10× the monthly price. **There are no "
           "free trials**: every paid plan starts with payment. Free is a permanent plan with no card, and we "
           "don't lead with it. Prices are the amounts charged: FluxMuse is not VAT-registered, so no VAT is "
           "added.")

    d.h2("Nine plans in three bands")
    rows = []
    for band, tiers in PT["bands"].items():
        for t in tiers:
            b, c, note = SPEC[t]
            mo = "On request" if t == "Custom" else rand(ZAR[t])
            an = "—" if t == "Custom" else rand(ZAR[t] * 10)
            rows.append((band if t == tiers[0] else "", t, mo, an, b, c, note))
    d.table(["Band", "Plan", "Monthly", "Annual", "Brands", "Channels", "Notes"], rows,
            [2.1, 2.0, 2.0, 2.1, 1.8, 1.7, 5.3], "Plans and list prices (ZAR)", size=8.5,
            aligns=[None, None, "right", "right", "right", "right", None])
    d.note("AI credit allowances changed on 24 September and are set on the pricing page; this plan never "
           f"quotes per-plan credit numbers. Custom is modelled from {rand(ZAR['Custom'])} a month "
           "**[[CONFIRM]]**.")
    d.figure("infographics/pricing-tiers.png",
             "Nine plans in three bands, priced in rands.",
             "Pricing page: a Founding Member banner, 30% off the first two monthly bills for South African "
             "sign-ups; Small (Free R0, Nano R149, Micro R289), Medium (Starter R499, Growth R1,999, Scale "
             "R4,999) and Enterprise (Corporate R6,999, Agency R9,999, Custom on request), with brands, channels "
             "and annual prices.")

    d.h2("Local pricing: priced, not yet on sale")
    d.para("Nigeria, Kenya and Ghana have **fixed local price points** in the product, set at parity with the "
           "rand (1 ZAR = ₦82.83 = KSh 8.07 = GH₵ 0.68), and other markets have US dollar prices at R18.50 = "
           "US$1. **None of these is on sale**: checkout outside South Africa waits for the Fincra and pawaPay "
           "accounts and a real-money test.")
    d.figure("infographics/pricing-regional.png",
             "One set of plans, priced for each market. Only South Africa is on sale.",
             "Table of monthly prices for Nano to Agency in ZAR (on sale), and NGN, KES, GHS and USD (not yet on "
             "sale): for example Nano R149, ₦12,000, KSh 1,199, GH₵ 99, $8; Agency R9,999, ₦829,000, KSh 80,999, "
             "GH₵ 6,799, $539.")

    d.h2("Repricing policy")
    d.bullets([
        "Local prices are **reviewed quarterly**. If the rand value of a local price has drifted more than "
        "**10%**, the price is reset to parity.",
        "A **6% list-price escalator** applies each October in the model **[[CONFIRM]]**.",
        "The model assumes annual depreciation against the rand of NGN −10%, GHS −8%, KES −3% and USD 0% "
        "(**[[CONFIRM FX ASSUMPTIONS]]**).",
        "Section 12 shows why this matters: in a 15% rand-strengthening shock without repricing, the Base case "
        "fails the cash test.",
    ])

    d.h2("Partner wholesale")
    d.table(["", "ZAR", "NGN", "KES", "GHS", "USD"], [
        ("Agency list, monthly", rand(ZAR["Agency"]), f"₦{LM['NGN']['Agency']:,}", f"KSh {LM['KES']['Agency']:,}",
         f"GH₵ {LM['GHS']['Agency']:,}", f"${LM['USD']['Agency']:,}"),
        (f"Partner wholesale, monthly (−{PW['discount_vs_agency_list_pct']}%)", rand(PW["ZAR"]),
         f"₦{PW['NGN']:,}", f"KSh {PW['KES']:,}", f"GH₵ {PW['GHS']:,}", f"${PW['USD']}"),
        ("Partner wholesale, annual (10×)", rand(PW["ZAR"] * 10), f"₦{PW['NGN'] * 10:,}", f"KSh {PW['KES'] * 10:,}",
         f"GH₵ {PW['GHS'] * 10:,}", f"${PW['USD'] * 10:,}"),
    ], [5.0, 2.4, 2.7, 2.5, 2.4, 2.0], "Partner wholesale pricing", size=9,
        aligns=[None, "right", "right", "right", "right", "right"])
    d.note("The partner price is a permanent wholesale price, not a launch discount. The product has no regional "
           "wholesale rows, so local wholesale uses the Corporate local prices **[[CONFIRM]]**. The model "
           "assumes 100% of agency-segment customers buy at wholesale. A referral commission is "
           "**[[FOUNDER DECISION: REFERRAL COMMISSION %]]** and is not modelled.")

    d.h2("Discounts")
    d.bullets([
        "**One launch offer only**: Founding Member, 30% off the first two monthly bills for South African "
        f"sign-ups (Nano {rand(FMB['Nano'])} to Scale {rand(FMB['Scale'])}). Live now; no end date set.",
        "**No stacking.** Founding Member does not combine with partner wholesale.",
        "**Every paid plan starts with payment.** The offer is backed by the lead guarantee "
        "(section 4), paid in support, not cash.",
    ])

    d.h2("Checkout fees")
    d.para("When checkout through FluxMuse is switched on, card payments carry Paystack's standard fee (2.9% + "
           "R1), deducted before payout, and EFT is 2%. FluxMuse adds **no fee on checkout** in any scenario of "
           "the model.")


def s10_operations(d):
    d.h1("10. Operations", new_page=True)
    d.h2("Technology and architecture")
    d.bullets([
        "**Front end**: React with Vite, deployed on Vercel.",
        "**Back end**: Supabase, providing Postgres, authentication and edge functions.",
        "**Security**: row-level security on every table, encrypted third-party access tokens.",
        "**Integrations**: WhatsApp Cloud API, Meta Graph API, TikTok, Paystack; Shopify, WooCommerce and "
        "Takealot sync in part.",
        "**Why it scales cheaply**: managed infrastructure with per-workspace costs. Hosting is modelled at "
        "R30,000 a month plus R35 per workspace after the seed.",
        "**AI cost**: one AI credit is R0.15 of real provider cost (the product's own figure). Corporate, Agency "
        "and Custom run AI on the customer's own keys.",
    ])

    d.h2("Meta platform dependency")
    d.para("FluxMuse depends on Meta for WhatsApp and for Facebook and Instagram publishing. Fluxmuse (Pty) Ltd "
           "is a verified Meta Tech Provider and WhatsApp Business is live. Facebook and Instagram "
           "auto-publishing wait on Meta permissions; until approved they stay switched off and the real value "
           "is forwarding to WhatsApp Status. Instagram DMs and comments are not available.")
    d.table(["Stage", "Scope"], [
        ("1. Switch on what is built", "Checkout through FluxMuse (real-money test), Meta publishing permissions, "
                                       "daily digest template, AI Voice beta"),
        ("2. Expansion rails", "Fincra and pawaPay accounts live; Nigeria, Kenya and Ghana checkout tested"),
        ("3. Integrations", "Tenant catalogue sync from Shopify, WooCommerce and Takealot"),
        ("4. Partner programme", "Referral tracking and partner-managed workspaces"),
    ], [5.4, 11.6], "Product roadmap, in order", size=9.5)
    d.note("No dates are set for these stages. **[[FOUNDER: TARGET DATES]]**")

    d.h2("Payment rails and settlement")
    d.table(["Provider", "Role", "Status"], [
        ("Paystack", "Cards and EFT in South Africa; FluxMuse checkout for merchants",
         "Live in South Africa; merchant checkout being switched on"),
        ("Yoco, Ozow", "FluxMuse's own subscription billing", "Integrated"),
        ("pawaPay", "Mobile money for expansion markets", "Contracted, account pending"),
        ("Fincra", "Collections and payouts for expansion markets", "Contracted, account pending"),
    ], [2.6, 7.4, 7.0], "Payment providers", size=9)
    d.figure("infographics/payment-coverage-map.png",
             "Live in South Africa. The rest is pending.",
             "Tile map: paid checkout live in South Africa only (Paystack); Nigeria, Kenya and Ghana priced, not "
             "yet on sale; 19 countries where pawaPay or Fincra are contracted, accounts pending; Botswana and "
             "Namibia coming soon.")
    d.bullets([
        "**Settlement** runs through each provider to the merchant's own South African bank account; FluxMuse "
        "does not hold the money. **[[SETTLEMENT TERMS AND RECONCILIATION PROCESS]]**.",
        "**Processing cost** on FluxMuse's own subscriptions is modelled at 3.0% (Paystack 2.9% + R1), plus "
        "1.5% for mobile money and FX on non-South African revenue.",
        "Appendix B shows status by country.",
    ])

    d.h2("Customer onboarding and support")
    d.bullets([
        "**First group**: set up by hand by the founders, one business at a time.",
        "**Solo**: self-serve or a short demo on their own products.",
        "**SME**: a discovery call, a demo and set-up by hand.",
        "**Agency**: a live demo on a client's public catalogue, then white-label set-up.",
        "A customer success team is hired from the seed month and sits in cost of revenue: "
        f"{D['headcount_by_dept_fy_end']['Customer success'][0]} people at the end of FY1 rising to "
        f"{D['headcount_by_dept_fy_end']['Customer success'][4]} by FY5.",
    ])

    d.h2("Data protection and security")
    d.bullets([
        "Built to be POPIA ready; row-level security on every table; encrypted tokens; data export and account "
        "deletion on request.",
        "Broadcasts go only to consented contacts, using Meta-approved templates, with an opt-out.",
        "Screenshots and case studies blur customer names and phone numbers.",
        "**[[SECURITY POLICY, BREACH-RESPONSE PLAN, PENETRATION TEST AND HOSTING REGIONS: TO CONFIRM]]**",
    ])

    d.h2("Suppliers and key partners")
    d.table(["Partner", "Role", "Dependency"], [
        ("Meta", "WhatsApp Cloud API, Facebook and Instagram", "High: see section 14"),
        ("Supabase and Vercel", "Database, authentication, edge functions, hosting", "Medium: replaceable, "
                                                                                     "with effort"),
        ("AI model providers", "Inference behind the assistant", "Medium: cost and availability"),
        ("Paystack; pawaPay and Fincra (pending)", "Collections and payouts", "High until expansion rails are live"),
        ("Agency partners", "White-label distribution", "Builds over time"),
    ], [4.4, 7.0, 5.6], "Key suppliers and partners", size=9)


def s11_management(d):
    d.h1("11. Management and organisation", new_page=True)
    d.h2("Founders and team")
    d.table(["Role", "Name", "Background and responsibility"], [
        ("Founder", "Thabo Malebadi", "[[TITLE, BACKGROUND, YEARS OF EXPERIENCE, RESPONSIBILITY]]"),
        ("CTO / founding engineer", "[[CTO NAME]]", "[[BACKGROUND, RESPONSIBILITY]]"),
        ("[[ROLE]]", "[[NAME]]", "[[BACKGROUND, RESPONSIBILITY]]"),
    ], [4.0, 4.0, 9.0], "Founders and senior team", size=9.5)
    d.para("Both founders are on reduced salaries until the seed lands (R45,000 and R55,000 cost to company a "
           "month) **[[CONFIRM]]**, which keeps the pre-seed burn small.")
    d.para("**Advisors.** [[ADVISORS: NAMES, AREAS AND WHAT THEY CONTRIBUTE]]")

    d.h2("Governance")
    d.bullets([
        "Board composition after the round: **[[BOARD COMPOSITION AND INVESTOR RIGHTS]]**.",
        "Reporting: monthly management accounts and the KPI dashboard in section 15; quarterly board meetings "
        "(**[[CONFIRM REPORTING CADENCE WITH INVESTORS]]**).",
        "Financial controls: **[[SIGNING AUTHORITY, APPROVAL LIMITS, PAYROLL AND PAYMENT CONTROLS]]**.",
    ])

    d.h2("The hiring plan")
    d.para("**Nobody is hired on a calendar date alone.** Every non-founder role waits for its earliest month, "
           "the seed, and last month's net MRR clearing that role's gate. The hiring plan is unchanged from the "
           "previous model; the seed was sized to it rather than the other way round.")
    d.fy_table("Headcount by department at each year end (Base case)",
               [[dep] + [str(v) for v in D["headcount_by_dept_fy_end"][dep]] for dep in DEPTS] +
               [["Total headcount"] + [str(v) for v in D["headcount_total_fy_end"]]],
               first_header="Department", total_rows=(len(DEPTS),))
    d.source(f"FluxMuse Financial Model {MV} (Base case), derived from the model's headcount rows.")
    d.para(f"**Jobs created.** The plan grows from 2 founders to **{D['headcount_total_fy_end'][0]} people by "
           f"the end of FY1** and **{D['headcount_total_fy_end'][4]} by FY5**, of which "
           f"{D['headcount_by_dept_fy_end']['Country teams'][4]} are country-team roles in Nigeria, Kenya and "
           f"Ghana and {D['headcount_by_dept_fy_end']['Customer success'][4]} are customer-success roles.")

    d.h2("When each role is hired")
    d.para("The first month each role group is hired in the Base case, and the net MRR gate it waits for. "
           "Country-team roles are tied to their market's launch. Roles whose gate is not reached within FY5 are "
           "left out.")
    rows = []
    for r in sorted(D["roles"], key=lambda r: (r["fy"], r["role"])):
        if r["dept"] == "Leadership" or r["fy"] == "-":
            continue
        gate = rand(r["mrr_gate_zar"]) if r["mrr_gate_zar"] else (
            "Tied to market launch" if r["dept"] == "Country teams" else "At the seed")
        rows.append((r["fy"], r["first_month"], str(r["count"]), r["role"], gate))
    d.table(["FY", "First hired", "FTE", "Role", "Net MRR gate"], rows,
            [1.2, 2.3, 1.0, 9.5, 3.0], "Hiring plan: first hire month and MRR gate (Base case)", size=8,
            first_col_bold=False, aligns=[None, None, "right", None, "right"])
    d.source()
