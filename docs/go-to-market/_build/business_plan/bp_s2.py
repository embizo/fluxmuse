"""Sections 5-8: market analysis, target customers, competition, marketing & sales."""
from bp_doc import ANN, BASE, D, M, MV, SEED_M, TINT, ann, pct, rand, rk, rm

MS = M["market_sizing"]
UE = M["unit_economics_fy3"]
FM = M["founding_member"]
FG = M["first_group"]
FP = M["free_plan"]
PT = M["price_tables"]
ZAR = PT["zar_list_monthly"]
PW = PT["partner_wholesale_monthly"]
FMB = PT["founding_member_first_2_bills_zar"]
MKL = M["markets"]["launch_months"]["Base"]
MKP = M["markets"]["planned_earliest_launch_month"]
SEG = ANN[4]["ending_customers_by_segment"]


def s5_market(d):
    d.h1("5. Market analysis", new_page=True)
    d.para("All market figures below are **estimates** and are labelled with their source. They are planning "
           "inputs, not measured results, and should be re-verified before any external commitment "
           "(**[[VERIFY MARKET SIZING WITH A CURRENT SOURCE]]**).")

    d.h2("Market size")
    d.table(["Measure", "Estimate", "Basis"], [
        ("TAM: MSMEs in Sub-Saharan Africa", f"{MS['tam_msmes'] / 1e6:.0f} million businesses",
         "IFC / World Bank est."),
        ("SAM: digitally active small businesses in the African markets FluxMuse's contracted payment "
         "partners can reach, selling via social or WhatsApp and able to pay US$25 a month or more",
         f"about {MS['sam_smbs'] / 1e6:.1f} million businesses", "Planning estimate"),
        ("SAM value at US$25 a month", f"about R{MS['sam_value_zar_per_year_at_usd25'] / 1e9:.1f} billion a year",
         "SAM × US$25 × 12 at R18.50 = US$1"),
        ("SOM over 5 years", f"about {MS['som_paying_workspaces']:,} paying workspaces "
                             f"({pct(MS['som_share_of_sam_pct'], 1)} of SAM)", "Planning estimate"),
        ("Base case FY5 in this plan", f"{ANN[4]['ending_paying_workspaces']:,} paying workspaces "
                                       f"({pct(MS['model_fy5_workspaces_pct_of_som'], 1)} of the SOM)",
         f"FluxMuse Financial Model {MV}, Base case"),
    ], [5.8, 5.2, 6.0], "TAM, SAM and SOM (estimates)", size=9)
    d.note("Today only South Africa is on sale. The SAM counts markets FluxMuse can reach once its pending "
           "payment accounts are live; it is not a statement of current coverage.")

    d.h2("South Africa: the home market")
    d.para("South Africa has an estimated 2.5–3 million SMMEs (SEDA/Stats SA est.). It is the right first "
           "market: Paystack is live there, WhatsApp is near-universal, SMME support structures are well "
           "developed, and the company and team are here. Base case FY1 revenue is entirely South African.")

    d.h2("Nigeria, Kenya and Ghana: the first expansion wave")
    d.bullets([
        "**Nigeria**: about 39 million MSMEs (SMEDAN est.).",
        "**Kenya**: about 7.4 million MSMEs (KNBS est.); deep mobile-money usage.",
        "**Ghana**: strong mobile money and a large informal trading sector.",
        "All three are **priced in local currency but not yet on sale**. Checkout there waits for the Fincra "
        "and pawaPay accounts, then for a revenue gate (section 15). The model's planned earliest months are "
        f"Nigeria {MKP['Nigeria']}, Kenya {MKP['Kenya']} and Ghana {MKP['Ghana']} **[[CONFIRM]]**; in the Base "
        f"case the gates bind, so they open in {MKL['Nigeria']}, {MKL['Kenya']} and {MKL['Ghana']}.",
    ])

    d.h2("Trends")
    d.bullets([
        "**Chat commerce is becoming the default** for small-business selling in these markets.",
        "**Mobile money keeps widening**: Sub-Saharan Africa accounts for about 70% of global mobile money "
        "value (GSMA 2025 est.).",
        "**AI lowers the price floor** of marketing services, which opens a segment agencies cannot serve "
        "profitably.",
        "**Data-protection regimes are maturing**, which favours platforms built for consent from the start.",
    ])

    d.h2("Regulatory environment")
    d.table(["Market", "Regime", "What it means for FluxMuse"], [
        ("South Africa", "Protection of Personal Information Act (POPIA)",
         "Information Officer registered, operator agreements, opt-in marketing, breach notification. "
         "Outreach is human-sent and one-to-one (POPIA s69). [[INFORMATION OFFICER REGISTRATION CONFIRMED]]"),
        ("South Africa", "VAT",
         "Not VAT-registered today. Registration becomes compulsory above R1m of taxable supplies in 12 "
         "months, which the Base case passes late in FY1 **[[FOUNDER: VAT PLAN]]**"),
        ("Nigeria", "NDPR / Nigeria Data Protection Act",
         "Data-controller registration and local counsel, funded from the expansion budget"),
        ("Kenya", "Kenya Data Protection Act",
         "Registration with the Office of the Data Protection Commissioner"),
        ("Ghana", "Ghana Data Protection Act", "Registration with the Data Protection Commission"),
        ("All markets", "Payments regulation",
         "Handled by licensed providers. FluxMuse does not take deposits or hold merchants' money"),
        ("All markets", "Meta platform policy",
         "WhatsApp Business messaging policy, template approval and opt-in rules govern what may be sent"),
    ], [2.8, 4.4, 9.8], "Regulatory environment", size=9)


def s6_customers(d):
    d.h1("6. Target customers", new_page=True)
    d.para("Three launch segments, all in South Africa first. **Corporate and Custom are taken inbound "
           "only**: no sales motion or hire is built for them in FY1.")
    d.figure("infographics/target-segments.png",
             "The three launch segments, South Africa first.",
             "Three segment cards: solo entrepreneurs on Nano R149 moving to Micro R289 and Starter R499; SMEs "
             "on Growth R1,999 moving to Scale R4,999; agencies on the partner price of R6,999 a month, 30% off "
             "Agency; each with who they are, their pain, the promise and the buying motion.")
    d.table(["", "Solo sellers", "SMEs", "Agencies"], [
        ("Who", "Founder-run businesses of 1–5 people: side hustles, beauty and braiding, fashion resellers, "
                "home bakers, informal retailers selling on WhatsApp and social",
         "5–200 staff: retail, restaurants, e-commerce brands, clinics, property, education, professional "
         "services",
         "Marketing, digital and social agencies and freelancers managing many small-business clients"),
        ("Main tier", f"Nano {rand(ZAR['Nano'])} → Micro {rand(ZAR['Micro'])} → Starter {rand(ZAR['Starter'])}",
         f"Starter {rand(ZAR['Starter'])} → Growth {rand(ZAR['Growth'])} → Scale {rand(ZAR['Scale'])}",
         f"Agency tier at partner wholesale {rand(PW['ZAR'])}"),
        ("Pain", "No time or budget for a marketer; DMs answered late; no shop page, so orders get lost",
         "Disconnected tools; agency retainers; WhatsApp handled by hand; no clear view of what sells",
         "Margin squeeze; manual reporting; too many tools per client; clients asking for WhatsApp selling"),
        ("Promise", "“Send photos, get a shop link. Your marketing team lives in WhatsApp”",
         "“Answer every customer, post every week, and see every order on WhatsApp”",
         "“Serve more clients under your brand: set your own retail price and keep the spread”"),
        ("Buying motion", "Self-serve, or a demo on their own products; Free plan as an on-ramp, not a trial",
         "Discovery call, demo on their products, proposal; set up by hand",
         "Partner conversation and a live demo on a client's public catalogue, then the wholesale plan"),
        ("Base case FY5 workspaces", f"{SEG['Solo']:,}", f"{SEG['SMEs']:,}", f"{SEG['Agencies']:,}"),
    ], [2.5, 4.9, 4.9, 4.7], "The three launch segments", size=9)
    d.note(f"Corporate and Custom are inbound only: {SEG['Corporate']} Corporate and {SEG['Enterprise']} Custom "
           "workspaces by FY5 in the Base case.")

    d.h2("Personas")
    d.callout("Persona 1: the braiding studio owner (solo seller)", [
        "Runs a braiding and hair studio. Decides alone. Already books clients and posts work on WhatsApp, "
        "Instagram and Facebook.",
        "- **Needs**: bookings that don't get lost in DMs, consistent posts in isiZulu, Sesotho and English, "
        "and a simple page that shows what she offers.",
        f"- **Buys**: Nano or Micro, usually on a phone, often on a peer's recommendation. Founding Member "
        f"brings Nano to {rand(FMB['Nano'])} for the first two monthly bills.",
    ], caption="Layout: persona solo")
    d.callout("Persona 2: the multi-branch SME marketing lead", [
        "Runs marketing for a business with several branches or an online store, and is asked every month what "
        "the marketing earned.",
        "- **Needs**: one product instead of several, WhatsApp handled properly rather than on staff phones, "
        "and every order visible.",
        "- **Buys**: after a call and a demo on their own products; Starter or Growth, moving to Scale for more "
        "brands.",
    ], caption="Layout: persona SME")
    d.callout("Persona 3: the agency owner", [
        "Runs a social or digital agency. Margin is squeezed by delivery time and tool costs, and clients are "
        "asking for WhatsApp selling and AI.",
        "- **Needs**: white-label delivery, client sub-accounts and less time on reporting.",
        f"- **Buys**: through the partner programme at {rand(PW['ZAR'])} a month, and sets its own retail price.",
    ], caption="Layout: persona agency")


def s7_competition(d):
    d.h1("7. Competitive landscape", new_page=True)
    d.para("FluxMuse competes with four categories at once, and with none of them completely. The comparison "
           "below is **qualitative and about categories, not named competitors**.")
    d.table(["Category", "What they do well", "Where they leave the customer", "FluxMuse"], [
        ("Global social media management tools",
         "Scheduling, publishing and analytics across many networks",
         "Stop at the post: no shop, priced in hard currency, little local-language support",
         "Runs from WhatsApp, builds the shop, priced in rands"),
        ("WhatsApp business solution providers and chatbot vendors",
         "Reliable messaging infrastructure and chatbot building",
         "No marketing team or content creation; often aimed at larger businesses",
         f"Messaging inside a marketing product, on flat plans from {rand(ZAR['Nano'])}"),
        ("E-commerce platforms",
         "Storefronts, catalogues and payment integrations",
         "Sell on a website; building the catalogue is the owner's job",
         "The catalogue is built from photos sent on WhatsApp"),
        ("Local agencies and freelancers",
         "Local knowledge, relationships and creative judgement",
         "Retainer pricing this market mostly cannot afford",
         f"Sold to agencies, not against them: white-label at {rand(PW['ZAR'])} so they serve more clients"),
    ], [3.3, 4.4, 4.9, 4.4], "Competitive categories (qualitative)", size=9)

    d.h2("Our differentiation")
    d.bullets([
        "**WhatsApp-first**: the owner runs the business from WhatsApp, where they already work.",
        "**Priced in rands**, from a permanent Free plan to Custom, with paid plans from "
        f"{rand(ZAR['Nano'])} a month.",
        "**Answers in the customer's language**, a product feature rather than an afterthought.",
        "**Verified Meta Tech Provider**, already held.",
        "**A partner channel** that turns the most obvious local competitor into a distribution route.",
    ])

    d.h2("Defensibility")
    d.bullets([
        "**Verification takes time.** Meta Tech Provider verification is months of work a new entrant must "
        "repeat. Payment contracts for expansion are signed; accounts are pending.",
        "**Switching costs.** The WhatsApp number, catalogue, templates, contacts and shop link all live in the "
        "workspace.",
        "**Channel lock-in through partners.** An agency that rebuilds its delivery on a white-label platform "
        "does not move lightly.",
        f"**Price position.** A product built for {rand(ZAR['Nano'])}-a-month customers is hard to attack from "
        "above.",
    ])
    d.note("This position has not yet been tested in the market. Risks, including Meta dependency and pending "
           "payment accounts, are set out in section 14.")


def s8_gtm(d):
    d.h1("8. Marketing and sales strategy", new_page=True)
    d.h2("Sequence")
    d.para("The order is fixed: **South Africa now; Nigeria, Kenya and Ghana once their payment accounts are "
           "live and checkout is tested; then other covered markets self-serve in US dollars.** Botswana and "
           "Namibia are coming soon. Everywhere else is waitlist only.")
    d.figure("infographics/market-entry-sequence.png",
             "Where we sell, in order. Launch dates in this plan are set by payment accounts and revenue gates.",
             "Four stages: South Africa, billed in ZAR, open now with Paystack live, a first group set up by hand "
             "and Founding Member; Nigeria, Kenya and Ghana, priced in NGN, KES and GHS, not yet on sale, no "
             "date set; other covered markets in USD once open; Botswana and Namibia coming soon, waitlist only.")

    d.h2("Opening with a small first group")
    d.para(f"There is no pilot and no free period. We are opening with a **small first group of businesses and "
           f"setting each one up by hand**. The model assumes {FG['per_month']} a month from "
           f"{FG['months'].replace(' - ', ' to ')} ({FG['total_workspaces']} in total, half solo sellers), at "
           f"{rand(FG['setup_cost_zar_per_month'])} a month of set-up cost **[[CONFIRM]]**. They pay list price "
           "less Founding Member from the first bill. Each may become a case study, only with measured data and "
           "signed consent (Appendix C).")

    d.h2("Channels by segment")
    d.table(["Segment", "Acquisition channels", "What we measure first"], [
        ("Solo sellers",
         "Founder-led demos, WhatsApp short links, creators, community markets, Meta and TikTok ads after the "
         "seed (capped)", "Pay-at-sign-up rate and Free-to-paid upgrades"),
        ("SMEs",
         "Discovery calls and demos on the prospect's own products, business networks, referrals",
         "Conversion after a demo; early churn"),
        ("Agencies",
         "Direct outreach, agency communities, a live demo on a client's public catalogue",
         "Agencies signed per partnerships manager"),
    ], [3.4, 8.6, 5.0], "Channels by segment", size=9)
    d.note("Outreach is human-sent and one-to-one, through channels the business publishes, with a clear "
           "opt-out (CURRENT_OFFER.md §6). No bulk automation and no AI cold calls.")

    d.h2("Founding Member")
    d.para(f"One launch offer, live since 1 October 2026: **30% off the first two monthly bills** for South "
           f"African sign-ups (for example Nano {rand(FMB['Nano'])}, Micro {rand(FMB['Micro'])}, Starter "
           f"{rand(FMB['Starter'])}, Growth {rand(FMB['Growth'])}, Scale {rand(FMB['Scale'])}). It is a discount, "
           "not a free period. **No end date is set**; the model ends it in March 2027 **[[CONFIRM]]**. It does "
           "not stack with partner wholesale, and no offer is modelled for Nigeria, Kenya or Ghana.")
    d.para(f"**The offer is cheap and it is modelled.** It costs {rand(FM['discount_cost_by_fy_zar']['FY1'])} "
           f"in FY1 and nothing after. Because sign-ups are assumed to rise "
           f"{FM['window_signup_uplift_pct']}% while it runs (unproven, to be measured), it leaves slightly more "
           "cash than no offer at all.")
    d.figure("charts/founding_member_discount_cost.png",
             "Founding Member discount cost by month (Base case).",
             "Bar chart of the monthly Founding Member discount cost in South Africa from October 2026 to April "
             "2027, all within FY1.")

    d.h2("The lead guarantee")
    d.para("3 qualified leads in 30 days of go-live; if fewer arrive and the merchant shared the link and posted "
           "at least weekly, FluxMuse extends support at no extra charge until 3 are reached. It is never a cash "
           "payment and never a promise of sales.")

    d.h2("The partner programme")
    d.para(f"Agencies are a channel, not only a segment. Partners buy the Agency tier at **{rand(PW['ZAR'])} a "
           "month** and set their own retail price. In the Base case the partner channel grows from "
           f"{ANN[0]['ending_customers_by_segment']['Agencies']} agency workspaces in FY1 to {SEG['Agencies']} in "
           "FY5, through a partnerships team rather than paid advertising. A referral commission is undecided "
           "and not modelled.")

    d.h2("Brand positioning and messaging")
    d.para("**Positioning.** For solo sellers, SMEs and agencies in South Africa who sell on social media and "
           "WhatsApp but have no time, budget or tools for a marketing team, FluxMuse is the AI marketing team "
           "and WhatsApp shop that turns photos into a catalogue, posts and orders, in their language and priced "
           "in rands.")
    d.para("**Voice.** Plain, warm and direct. Newly launched, and said plainly. No results quoted until they are "
           "measured.")

    d.h2("Sales process and funnel")
    d.para("There are no free trials. Sign-ups either pay at once or join the permanent Free plan, from which "
           "some upgrade over time. The funnel assumptions that drive the model are:")
    sg = UE["by_segment"]
    d.table(["Funnel assumption", "Solo", "SMEs", "Agencies", "Corporate / Custom"], [
        ("Pay at sign-up", pct(FP["direct_paid_share_of_signups_pct"]["Solo"]),
         pct(FP["direct_paid_share_of_signups_pct"]["SMEs"]), "n/a", "n/a"),
        ("Free plan", f"Upgrade {FP['monthly_upgrade_pct']}% a month; dormant {pct(FP['monthly_dormancy_pct'])} "
                      "a month", "Same", "n/a", "n/a"),
        ("Acquisition", "Self-serve, Free upgrades, capped paid ads", "Self-serve plus guided onboarding",
         "Inbound plus partnerships managers and country leads", "Inbound only"),
        ("FY3 modelled CAC", rand(sg["Solo"]["cac_zar"]), rand(sg["SMEs"]["cac_zar"]),
         rand(sg["Agencies"]["cac_zar"]), f"{rand(sg['Corporate']['cac_zar'])} / {rand(sg['Enterprise']['cac_zar'])}"),
        ("FY3 modelled LTV:CAC", f"{sg['Solo']['ltv_to_cac']}x", f"{sg['SMEs']['ltv_to_cac']}x",
         f"{sg['Agencies']['ltv_to_cac']}x", f"{sg['Corporate']['ltv_to_cac']}x / {sg['Enterprise']['ltv_to_cac']}x"),
    ], [3.8, 3.4, 3.2, 3.6, 3.0], "Funnel and unit-economics assumptions", size=8.5)
    d.source()
    d.para("**Solo does not pay back on fully loaded CAC** "
           f"({sg['Solo']['ltv_to_cac']}x). Solo customers are worth having through the Free plan and upgrades, "
           "not through paid acquisition at scale.")
    d.para("**Paid acquisition is capped.** Monthly paid spend is limited to R40,000 plus 35% of last month's "
           "net MRR in the Base case, and is switched off where CAC payback would exceed 12 months. In FY1 the "
           f"cap funds {pct(ANN[0]['paid_acquisition_funded_by_cap_pct'])} of the paid acquisition the funnel "
           "wants.")
