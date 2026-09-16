"""Sections 5-8: market analysis, target customers, competition, marketing & sales."""
from bp_doc import ANN, BASE, D, M, TINT, ann, pct, rand, rk, rm

MS = M["market_sizing"]
UE = M["unit_economics_fy3"]
FM = M["founding_member"]
PILOT = M["pilot"]


def s5_market(d):
    d.h1("5. Market analysis", new_page=True)
    d.para("All market figures below are **estimates** and are labelled with their source. They are planning "
           "inputs, not measured results, and should be re-verified before any external commitment "
           "(**[[VERIFY MARKET SIZING WITH A CURRENT SOURCE]]**).")

    d.h2("Market size")
    d.table(["Measure", "Estimate", "Basis"], [
        ("TAM: MSMEs in Sub-Saharan Africa", f"{MS['tam_msmes'] / 1e6:.0f} million businesses",
         "IFC / World Bank est."),
        ("SAM: digitally active SMBs in the 23 rail-covered countries that sell via social or WhatsApp and can "
         "pay US$25 a month or more", f"about {MS['sam_smbs'] / 1e6:.1f} million businesses",
         "Planning estimate (facts file §5)"),
        ("SAM value at US$25 a month", f"about R{MS['sam_value_zar_per_year_at_usd25'] / 1e9:.1f} billion a year",
         "SAM × US$25 × 12 at R18.50 = US$1"),
        ("SOM over 5 years", f"about {MS['som_paying_workspaces']:,} paying workspaces "
                             f"({pct(MS['som_share_of_sam_pct'], 1)} of SAM)", "Planning estimate"),
        ("Base case FY5 in this plan", f"{ANN[4]['ending_paying_workspaces']:,} paying workspaces "
                                       f"({pct(MS['model_fy5_workspaces_pct_of_som'], 1)} of the SOM)",
         "FluxMuse Financial Model v2, Base case"),
    ], [5.8, 5.2, 6.0], "TAM, SAM and SOM (estimates)", size=9)
    d.figure("infographics/why-africa-why-now.png",
             "Market context, with sources. Every figure is an estimate.",
             "Stat cards: about 44 million MSMEs in Sub-Saharan Africa (IFC/World Bank est.), 2.5 to 3 million "
             "SMMEs in South Africa (SEDA/Stats SA est.), about 39 million MSMEs in Nigeria (SMEDAN est.), "
             "about 7.4 million in Kenya (KNBS est.), more than 90% of internet users in South Africa and "
             "Nigeria use WhatsApp (DataReportal 2025 est.), about 70% of global mobile money value is in "
             "Sub-Saharan Africa (GSMA 2025 est.); and the TAM, SAM and SOM planning assumption.")

    d.h2("South Africa: the home market")
    d.para("South Africa has an estimated 2.5–3 million SMMEs (SEDA/Stats SA est.). It is the right first "
           "market for this business: card, instant EFT and mobile-money rails are all available, WhatsApp is "
           "near-universal, SMME support structures are well developed, and the company, team and pilot are "
           "here. Base case FY1 revenue is entirely South African.")

    d.h2("Nigeria, Kenya and Ghana: the first expansion wave")
    d.bullets([
        "**Nigeria**: about 39 million MSMEs (SMEDAN est.); Paystack, pawaPay and Fincra all operate there.",
        "**Kenya**: about 7.4 million MSMEs (KNBS est.); deep mobile-money usage.",
        "**Ghana**: strong mobile money and a large informal trading sector; covered by the same three rails.",
        "All three are priced in **local currency at fixed price points** (section 9), and all three launch "
        "behind a revenue gate, not a calendar date (section 15).",
    ])

    d.h2("Trends")
    d.bullets([
        "**Chat commerce is becoming the default** for small-business selling in these markets, not a channel "
        "add-on.",
        "**Mobile money keeps widening**: Sub-Saharan Africa accounts for about 70% of global mobile money "
        "value, more than US$1 trillion processed a year (GSMA 2025 est.).",
        "**AI lowers the price floor** of marketing services, which opens a segment that agencies cannot "
        "profitably serve.",
        "**Data-protection regimes are maturing** across the continent, which favours platforms built for "
        "compliance from the start.",
    ])

    d.h2("Regulatory environment")
    d.table(["Market", "Regime", "What it means for FluxMuse"], [
        ("South Africa", "Protection of Personal Information Act (POPIA)",
         "Information Officer registered, operator agreements with customers, opt-in marketing, breach "
         "notification. [[INFORMATION OFFICER REGISTRATION CONFIRMED]]"),
        ("Nigeria", "NDPR / Nigeria Data Protection Act",
         "Data-controller registration and local counsel, funded from the expansion budget"),
        ("Kenya", "Kenya Data Protection Act",
         "Registration with the Office of the Data Protection Commissioner"),
        ("Ghana", "Ghana Data Protection Act", "Registration with the Data Protection Commission"),
        ("All markets", "Payments regulation",
         "Handled by the licensed rails. FluxMuse does not take deposits, hold client funds or operate as a "
         "payment institution"),
        ("All markets", "Meta platform policy",
         "WhatsApp Business messaging policy, template approval and opt-in rules govern what may be sent"),
        ("Self-serve markets", "Indirect tax",
         "VAT and digital-services registrations where required; R150,000 is budgeted in the model for "
         "Rest-of-Africa registrations"),
    ], [2.8, 4.4, 9.8], "Regulatory environment", size=9)


def s6_customers(d):
    d.h1("6. Target customers", new_page=True)
    d.para("Three launch segments, all in South Africa first. **Enterprise is not a launch target**: inbound "
           "enterprise deals are taken, but no sales motion, deck or hire is built for enterprise in FY1.")
    d.figure("infographics/target-segments.png",
             "The three launch segments, South Africa first.",
             "Three segment cards: solo entrepreneurs on Starter R499, SMEs on Growth R1,999 moving to Scale "
             "R4,999, and agencies on the partner price of R5,599 a month, each with who they are, their pain, "
             "the promise and the buying motion.")
    d.table(["", "Solo entrepreneurs", "SMEs", "Agencies"], [
        ("Who", "Founder-run businesses of 1–5 people: beauty and braiding, fashion resellers, home bakers, "
                "coaches, informal retailers selling on Instagram, Facebook and WhatsApp",
         "5–200 staff: retail, restaurants and franchises, e-commerce brands, clinics, property, auto dealers, "
         "education, professional services",
         "Marketing, digital and social agencies and freelancers managing 5–50 SMB clients"),
        ("Main tier", "Starter R499 → Growth", "Growth R1,999 → Scale R4,999",
         "Agency tier at partner wholesale R5,599"),
        ("Pain", "No time or budget for a marketer; posts inconsistently; loses sales in WhatsApp DMs; payment "
                 "links drop off",
         "Disconnected tools; agency retainers; no attribution from social to sales; WhatsApp handled manually "
         "by staff",
         "Margin squeeze; manual reporting; too many tools per client; clients want WhatsApp commerce and AI"),
        ("Promise", "“Your AI marketing team for R499/mo, and you sell right inside WhatsApp”",
         "“Replace the tool stack, sell and get paid in chat, see what drives revenue”",
         "“Serve more clients under your brand, at R5,599/mo, and set your own retail price”"),
        ("Buying motion", "Self-serve: 14-day free trial, no card, then the Founding Member offer",
         "Trial plus a guided onboarding call; proposal for multi-brand or Scale",
         "Partner programme: demo → pilot client → Agency tier with reseller billing"),
        ("Base case FY5 workspaces", f"{ANN[4]['ending_customers_by_segment']['Solo']:,}",
         f"{ANN[4]['ending_customers_by_segment']['SMEs']:,}",
         f"{ANN[4]['ending_customers_by_segment']['Agencies']:,}"),
    ], [2.5, 4.9, 4.9, 4.7], "The three launch segments", size=9)
    d.note(f"Enterprise is inbound only: {ANN[0]['ending_customers_by_segment']['Enterprise']} workspace in FY1 "
           f"and {ANN[4]['ending_customers_by_segment']['Enterprise']} by FY5 in the Base case.")

    d.h2("Personas")
    d.callout("Persona 1: the braiding studio owner (solo entrepreneur)", [
        "Runs a braiding and hair studio in a Gauteng township or suburb. Decides alone: no procurement, no IT "
        "department. Already books clients and posts work on WhatsApp, Instagram and Facebook.",
        "- **Needs**: bookings that don't get lost in DMs, deposits to stop no-shows, consistent posting in "
        "isiZulu, Sesotho and English, and money in the account the same day.",
        "- **Buys**: self-serve on Starter R499 after a 14-day free trial, usually on a phone, often on the "
        "strength of a peer's recommendation.",
        "- **Why this persona leads**: lowest barrier, shortest booking cycle, thousands of similar businesses "
        "across Gauteng. It is the lead case study in the pilot.",
    ], caption="Layout: persona solo")
    d.callout("Persona 2: the multi-branch SME marketing lead", [
        "Runs marketing for a 5–200 person business with several branches or an online store. Has a budget, "
        "several tools and an agency, and is asked every month what the marketing actually earned.",
        "- **Needs**: one platform instead of six, WhatsApp handled properly rather than on staff phones, "
        "attribution from campaign to order, and reporting that takes minutes.",
        "- **Buys**: trial, then a guided onboarding call and a proposal; Growth, moving to Scale for more "
        "brands or API access.",
    ], caption="Layout: persona SME")
    d.callout("Persona 3: the agency owner", [
        "Runs a 5–50 client social or digital agency. Margin is squeezed by delivery time and tool costs, and "
        "clients are asking for WhatsApp commerce and AI.",
        "- **Needs**: white-label delivery under their own brand, client sub-accounts, reseller billing, and "
        "reporting that doesn't eat a day a month.",
        "- **Buys**: through the partner programme at R5,599 a month, after a demo and a pilot client, and "
        "sets its own retail price.",
    ], caption="Layout: persona agency")


def s7_competition(d):
    d.h1("7. Competitive landscape", new_page=True)
    d.para("FluxMuse competes with four categories at once, and with none of them completely. The comparison "
           "below is **qualitative and about categories, not named competitors**: it quotes no competitor "
           "prices and makes no claim that cannot be supported.")
    d.table(["Category", "What they do well", "Where they leave the customer", "FluxMuse"], [
        ("Global social media management tools",
         "Scheduling, publishing and analytics across many networks, mature products",
         "Stop at the post: no selling, no local payment methods, priced in hard currency, little local-language "
         "support",
         "Publishes and then sells in the same product, priced in local currency"),
        ("WhatsApp business solution providers and chatbot vendors",
         "Reliable messaging infrastructure and chatbot building",
         "No marketing team, no content creation, no campaign planning; often per-message pricing aimed at "
         "larger businesses",
         "Messaging is one channel inside a marketing platform, on flat plans from R499"),
        ("E-commerce platforms",
         "Storefronts, catalogs and payment integrations",
         "Sell on a website, not inside a conversation; marketing is a separate purchase",
         "Catalog and checkout inside WhatsApp, with the marketing that drives them"),
        ("Local agencies and freelancers",
         "Local knowledge, relationships and creative judgement",
         "Retainer pricing that this market mostly cannot afford; capacity limits growth",
         "Sold to agencies rather than against them: white-label at R5,599 so they serve more clients"),
    ], [3.3, 4.4, 4.9, 4.4], "Competitive categories (qualitative)", size=9)

    d.h2("Our differentiation")
    d.bullets([
        "**The whole loop in one product**: plan, create, publish, sell, get paid, learn.",
        "**Payments coverage**: five secured rails across 23 African countries, including mobile money, instant "
        "EFT and cards, with Botswana and Namibia coming soon.",
        "**Local pricing**: fixed price points in ZAR, NGN, KES and GHS, and US dollars elsewhere, rather than "
        "an FX-converted foreign price.",
        "**Multilingual AI** across isiZulu, Pidgin, Swahili, Afrikaans and English and more, which is a "
        "product feature here rather than a localisation afterthought.",
        "**Meta Tech Provider verification**, already held.",
        "**A partner channel** that turns the most obvious local competitor into a distribution route.",
    ])

    d.h2("Defensibility")
    d.bullets([
        "**Verification and rail contracts take time.** Meta Access Verification and five payment-provider "
        "relationships are months of work a new entrant must repeat.",
        "**Data compounds.** The Analyst agent's RAG memory and cohort data improve with every campaign and "
        "order on the platform.",
        "**Switching costs.** The WhatsApp number, catalog, templates, automations, contact history and "
        "payment setup all live in the workspace.",
        "**Channel lock-in through partners.** An agency that has rebuilt its delivery on a white-label "
        "platform does not move lightly.",
        "**Price position.** A platform built for R499-a-month customers is hard to attack from above.",
    ])
    d.note("Risks to this position, including Meta dependency and rail concentration, are set out in "
           "section 14.")


def s8_gtm(d):
    d.h1("8. Marketing and sales strategy", new_page=True)
    d.h2("Sequence")
    d.para("The order is fixed: **South Africa, then Nigeria, Kenya and Ghana, then the other 19 rail-covered "
           "countries self-serve in US dollars.** Botswana and Namibia are shown as coming soon. Every country "
           "without a rail that can collect is waitlist only: no prices, no checkout.")
    d.figure("infographics/market-entry-sequence.png",
             "Market entry order. Launch dates in this plan are set by revenue gates; see section 15.",
             "Four stages: South Africa billed in ZAR with the Gauteng pilot then national; Nigeria, Kenya and "
             "Ghana in local currency; 19 other rail-covered countries billed in USD, self-serve, with no local "
             "team until traction justifies one; Botswana and Namibia waitlist only, coming soon. Everywhere "
             "else is gated: waitlist only.")

    d.h2("Channels by segment")
    d.table(["Segment", "Acquisition channels", "Key proof"], [
        ("Solo entrepreneurs",
         "Meta and TikTok ads, WhatsApp short links, creators and influencers, community markets, link-in-bio",
         "Pilot case studies from solo-run brands"),
        ("SMEs",
         "Content and SEO, webinars, chamber and business networks such as Gauteng SMME hubs, bank and fintech "
         "partnerships, referrals from pilot brands",
         "Pilot KPIs: conversations, orders, GMV, hours saved"),
        ("Agencies",
         "Direct outreach, agency communities, the partner directory, co-marketing, referral fees",
         "White-label demo and the partner economics"),
    ], [3.4, 8.6, 5.0], "Channels and proof by segment", size=9)

    d.h2("The Founding Member launch offer")
    d.para("One launch offer, in every market: **Founding Member, a 60-day window per market**. Monthly plans "
           "get **30% off the first two monthly bills** (Starter R349, Growth R1,399, Scale R3,499); annual "
           "plans get **two extra months free**, 14 for the price of 12. Sign-ups also keep a Founding Member "
           "badge and priority support. The offer is **not available on the Agency tier**: agencies are pointed "
           "to the permanent partner wholesale price of R5,599 a month instead, which is never presented as a "
           "launch discount.")
    d.table(["Market", "Founding Member window"], [
        ("South Africa", FM["windows"]["South Africa"]),
        ("Nigeria, Kenya and Ghana", FM["windows"]["Nigeria / Kenya / Ghana"]),
        ("USD self-serve markets", "No window: these markets are self-serve"),
    ], [5.0, 12.0], "Founding Member windows", size=9.5)
    d.figure("infographics/founding-member-offer.png",
             "The Founding Member offer, South Africa window.",
             "Launch offer: 30% off the first two monthly bills or two extra months free on annual plans, a "
             "Founding Member badge and priority support on Starter, Growth and Scale, agencies see partner "
             "pricing, a Growth example of R1,399 for months one and two then R1,999, and the South Africa "
             "window of 1 December 2026 to 31 January 2027.")
    d.para(f"**The offer is cheap and it is modelled.** It costs {rand(FM['discount_cost_by_fy_zar']['FY1'])} in "
           f"FY1, {rand(FM['discount_cost_by_fy_zar']['FY2'])} in FY2 and "
           f"{rand(FM['discount_cost_by_fy_zar']['FY3'])} in FY3, never more than "
           f"{pct(max(FM['launch_discounts_pct_of_gross_subscriptions_fy1_fy5']), 1)} of gross subscriptions. "
           "Because sign-ups inside a window are assumed to rise 20% (an unproven assumption, flagged for "
           "testing in the South African window), the offer leaves slightly **more** cash than no offer at all, "
           "and does not threaten profitability on the R25M.")

    d.h2("The Gauteng pilot and case studies")
    d.para(f"**{PILOT['brands']} brands in Gauteng, September to 30 November 2026.** They pay nothing during "
           f"the pilot. On 1 December 2026 the model assumes **{PILOT['conversion_pct']}% convert** "
           f"({PILOT['converting_brands']:.0f} brands) on deepened pilot terms: 50% off the first two monthly "
           "bills (Starter R249, Growth R999, Scale R2,499, Agency R3,999), in exchange for a case study and "
           f"logo permission. That discount costs {rand(PILOT['pilot_discount_cost_fy1_zar'])} in FY1.")
    d.figure("infographics/gauteng-pilot.png",
             "The Gauteng pilot. No results exist yet: the first come in December 2026.",
             "Pilot overview: 12 brands from September to 30 November 2026, a suggested mix of five solo "
             "entrepreneurs, five SMEs and two agencies as archetypes with no brand names, the KPIs tracked, "
             "the braiding and hair studio as lead case study, and results in December 2026.")
    d.note("Until consented pilot data exists, all materials say “pilot underway, results December 2026”. No "
           "customer counts, ratings, testimonials or results are used anywhere in this plan.")

    d.h2("The partner programme")
    d.para("Agencies and freelancers are a channel, not only a segment. Partners buy the Agency tier at "
           "**R5,599 a month** and set their own retail price. In the Base case the partner channel grows from "
           f"{ANN[0]['ending_customers_by_segment']['Agencies']} agency workspaces in FY1 to "
           f"{ANN[4]['ending_customers_by_segment']['Agencies']} in FY5, acquired through a partnerships team "
           "rather than paid advertising.")
    d.note("Illustrative partner economics, always labelled as such: a partner serving 20 clients at a retail "
           "price it sets of R1,500 a month bills R30,000, pays FluxMuse R5,599, and keeps a R24,401 a month "
           "gross spread before its own delivery costs. Margin depends on the partner's own pricing and costs.")

    d.h2("Brand positioning and messaging")
    d.para("**Positioning.** For solo entrepreneurs, SMEs and agencies in South Africa and across Africa who "
           "sell on social media and WhatsApp but have no time, budget or tools for a marketing team, FluxMuse "
           "is the AI marketing team and WhatsApp commerce platform that plans, creates, publishes and sells in "
           "one place, in their language and their currency.")
    d.para("**Voice.** Warm, direct, African-first, no jargon: “receipts and revenue, not jargon”. Primary "
           "tagline: *AI Marketing & WhatsApp Commerce for Africa*.")

    d.h2("Sales process and funnel")
    d.para("Solo and SME customers arrive self-serve: a 14-day free trial with no card, then conversion to a "
           "paid plan. Agencies go through demo, pilot client and partner plan. The funnel assumptions that "
           "drive the model are:")
    d.table(["Funnel assumption", "Solo", "SMEs", "Agencies", "Enterprise"], [
        ("Share of self-serve trials", "65%", "35%", "n/a", "n/a"),
        ("Trial-to-paid conversion", "11%", "14%", "n/a", "n/a"),
        ("Acquisition", "Paid and organic self-serve", "Paid and organic self-serve, plus onboarding help",
         "0.5 inbound a month in South Africa plus 1.5 per partnerships manager; 0.4 per country lead",
         "Inbound only: 1 deal in FY1"),
        ("Paid CAC assumption", "R2,200", "R6,500", "Partner programme and team cost",
         "R25,000 handling per deal"),
        ("Monthly churn assumption", "6.5% Starter / 4.0% Growth", "3.0% Growth / 2.2% Scale", "2.0%", "1.0%"),
        ("FY3 modelled CAC", rand(UE["by_segment"]["Solo"]["cac_zar"]),
         rand(UE["by_segment"]["SMEs"]["cac_zar"]), rand(UE["by_segment"]["Agencies"]["cac_zar"]),
         rand(UE["by_segment"]["Enterprise"]["cac_zar"])),
        ("FY3 modelled LTV:CAC", f"{UE['by_segment']['Solo']['ltv_to_cac']}x",
         f"{UE['by_segment']['SMEs']['ltv_to_cac']}x", f"{UE['by_segment']['Agencies']['ltv_to_cac']}x",
         f"{UE['by_segment']['Enterprise']['ltv_to_cac']}x"),
    ], [4.0, 3.4, 3.4, 3.6, 2.6], "Funnel and unit-economics assumptions", size=8.5)
    d.source()
    d.para("**Paid acquisition is capped, not open-ended.** Monthly paid spend is limited to R40,000 plus 35% "
           "of last month's net MRR in the Base case, and is switched off in any segment or market where CAC "
           "payback would exceed 12 months. In FY1 the cap funds "
           f"{pct(ANN[0]['paid_acquisition_funded_by_cap_pct'])} of the paid acquisition the funnel wants, and "
           "100% from FY2 on. Growth is therefore self-financing by design.")
