"""Template 2: SME growth proposal."""
from fmdoc import FMDoc, DEEP
import common as C

CL = "[[CLIENT NAME]]"


def regional_appendix(d, letter="A", tiers=("Starter", "Growth", "Scale")):
    d.h1(f"Appendix {letter}. Regional pricing (delete if {CL} only operates in South Africa)", new_page=True)
    d.para("Fixed local prices for Nigeria, Kenya and Ghana, billed in local currency and set at parity with the ZAR "
           "price. The other 19 rail-covered countries are billed in US dollars. Annual = 10× monthly. Prices are "
           "reviewed quarterly.")
    local = {
        "Starter": ("R499", "₦41,000", "KSh 3,999", "GH₵ 339", "$27"),
        "Growth": ("R1,999", "₦165,000", "KSh 15,999", "GH₵ 1,359", "$109"),
        "Scale": ("R4,999", "₦413,000", "KSh 39,999", "GH₵ 3,399", "$269"),
        "Agency": ("R7,999", "₦662,000", "KSh 64,499", "GH₵ 5,439", "$429"),
    }
    annual = {
        "Starter": ("R4,990", "₦410,000", "KSh 39,990", "GH₵ 3,390", "$270"),
        "Growth": ("R19,990", "₦1,650,000", "KSh 159,990", "GH₵ 13,590", "$1,090"),
        "Scale": ("R49,990", "₦4,130,000", "KSh 399,990", "GH₵ 33,990", "$2,690"),
        "Agency": ("R79,990", "₦6,620,000", "KSh 644,990", "GH₵ 54,390", "$4,290"),
    }
    hdr = ["Plan", "South Africa (ZAR)", "Nigeria (NGN)", "Kenya (KES)", "Ghana (GHS)", "USD markets*"]
    w = [2.6, 2.8, 2.9, 2.9, 2.9, 2.9]
    al = [None, "right", "right", "right", "right", "right"]
    d.h2("Monthly")
    d.table(hdr, [(t,) + local[t] for t in tiers], w, "Regional monthly prices", aligns=al)
    d.h2("Annual (10× monthly)")
    d.table(hdr, [(t,) + annual[t] for t in tiers], w, "Regional annual prices", aligns=al)
    d.bullets([
        "*USD markets: Côte d'Ivoire, Rwanda, Uganda, Tanzania, Zambia, Cameroon, Senegal, Benin, Burkina Faso, Republic "
        "of the Congo, Gabon, DR Congo, Malawi, Mozambique, Sierra Leone, Ethiopia, Lesotho, South Sudan and Zimbabwe. "
        "South Sudan and Zimbabwe open for sale only once subscription collection is confirmed; until then they are "
        "waitlist only.",
        "**Founding Member** in Nigeria, Kenya and Ghana applies to sign-ups in the first 60 days after each country's "
        "launch, at 30% off the first 2 monthly bills. USD markets have no launch window.",
        "**Gated countries** (every country without a payment rail, including Botswana and Namibia, coming soon, and "
        "all countries outside Africa) can join the waitlist only: no prices, no checkout.",
        "Enterprise (from R19,999 / ₦1,650,000 / KSh 161,000 / GH₵ 13,600 / $1,099 a month) is quoted on request.",
    ])


def build_sme(out_path):
    d = FMDoc()
    d.cover("Proposal · SME growth", "Sell, get paid and grow on WhatsApp and social",
            f"A 60-day pilot and growth plan for {CL}")
    C.how_to_use(d, "SME growth proposal template", extra=[
        "[ ] Integrations: keep only the ones the client uses (Shopify, WooCommerce, Takealot, HubSpot, accounting, "
        "Slack, Zapier). Keep Appendix A only if the client trades outside South Africa.",
        "[ ] Optional service fees are [[TBC]] until the founder publishes a services price list.",
    ])
    d.toc()
    d.page_break()

    # 1 ----------------------------------------------------------------------------------------
    d.h1("1. Executive summary")
    d.para(f"{CL} sells to customers who already live on WhatsApp and social media, but [[SUMMARY OF THE PROBLEM IN "
           "ONE SENTENCE, e.g. enquiries are handled manually by staff across several tools, and nobody can see which "
           "campaigns bring in sales]].")
    d.para(f"FluxMuse proposes a **60-day pilot on the Growth plan** that puts an AI marketing team, WhatsApp "
           f"commerce and local payments on one platform for {CL}. We agree the baseline and targets at kickoff, "
           "report weekly, and at day 60 you decide whether to continue on Growth or move to Scale.")
    d.table(["Item", "Proposed"], [
        ("Recommended plan", "Growth, R1,999/mo ([[or Scale, R4,999/mo, for up to 10 brands or API access]])"),
        ("Pilot", "60 days from [[START DATE]]; optional days 61–90 to scale what works"),
        ("Channels", "WhatsApp, Facebook Page, Messenger, [[email / SMS / USSD]], link-in-bio and landing pages. "
                     "Instagram once Meta approves it"),
        ("Commerce", "WhatsApp catalog, cart checkout in chat, order updates, abandoned-cart recovery"),
        ("Payments", "[[Yoco card / Ozow instant EFT / Paystack]]"),
        ("Integrations", "[[Shopify / WooCommerce / Takealot / HubSpot / accounting sync]]"),
        ("Investment", "From R1,999/mo, plus optional services [[TBC]] and third-party pass-through costs (section 8)"),
        ("Decision needed by", "[[DATE + 30 days]]"),
    ], [4.2, 12.8], "Executive summary")

    # 2 ----------------------------------------------------------------------------------------
    d.h1(f"2. About {CL} and our understanding")
    d.h2("Business snapshot")
    d.table(["Area", f"{CL}"], [
        ("Industry and offer", "[[e.g. restaurant group, online beauty brand, clinic, auto dealer]]"),
        ("Locations and team", "[[N]] branches · [[N]] staff · [[AREAS]]"),
        ("Customers", "[[WHO THEY ARE, LANGUAGES, WHERE THEY BUY]]"),
        ("Channels today", "[[e.g. WhatsApp Business app on 3 phones, Facebook, Instagram, website]]"),
        ("Tools today", "[[e.g. separate tools for email, scheduling, chat, CRM and store]]"),
        ("Marketing spend today", "[[R PER MONTH: agency retainer, ads, tools]]"),
        ("How customers pay today", "[[e.g. card on delivery, EFT with proof of payment, cash]]"),
    ], [4.6, 12.4], "Client business snapshot")
    d.h2("What we heard")
    d.checklist([
        "Marketing runs across 6 or more disconnected tools",
        "Agency retainers of R15,000 or more a month, with little visibility of results",
        "No attribution from social posts and ads to sales",
        "WhatsApp is handled manually by staff on personal or shared phones",
        "Slow replies after hours and at peak times; enquiries go cold",
        "Buyers drop off when sent to external payment links",
        "Reporting takes hours each month",
        "Other: [[IN THE CLIENT'S WORDS]]",
    ])
    d.figure("infographics/segment-sme.png",
             "SMEs: today vs with FluxMuse. Founding Member pricing applies to South African sign-ups from "
             "1 December 2026 to 31 January 2027.",
             "Segment card for SMEs: disconnected tools, manual WhatsApp handling and no attribution, matched to one "
             "platform, WhatsApp commerce and Analyst reporting; Growth at R1,999 a month, Founding Member R1,399 for "
             "the first 2 months.")

    # 3 ----------------------------------------------------------------------------------------
    d.h1("3. Objectives and success metrics")
    d.para("Each objective is SMART: specific, measurable, achievable, relevant and time-bound. We confirm the baseline "
           "in the first week. **Every number in the target column is a goal agreed at kickoff, not a promised result.**")
    d.table(["#", "Objective", "KPI", "Baseline", "Target (goal)", "By"], [
        ("O1", "Answer every WhatsApp enquiry quickly", "Median first-reply time", "[[ ]]", "[[e.g. under 2 min]]", "Day 30"),
        ("O2", "Turn more chats into orders", "Chat-to-order conversion", "[[ ]]", "[[e.g. +20%]]", "Day 60"),
        ("O3", "Grow revenue through WhatsApp", "Orders and GMV via WhatsApp (R)", "[[ ]]", "[[R AMOUNT]]", "Day 60"),
        ("O4", "Recover lost sales", "Abandoned carts recovered", "[[ ]]", "[[e.g. 10% of carts]]", "Day 60"),
        ("O5", "Publish consistently", "Content pieces published per month", "[[ ]]", "[[e.g. 20+]]", "Day 30"),
        ("O6", "Free up staff time", "Staff hours saved per week", "[[ ]]", "[[e.g. 10+]]", "Day 60"),
        ("O7", "See what drives revenue", "Campaigns with attributed orders", "[[ ]]", "[[e.g. all campaigns]]", "Day 45"),
        ("O8", "Keep customers happy", "NPS", "[[ ]]", "[[e.g. +10 points]]", "Day 60"),
    ], [1.0, 4.4, 4.2, 2.1, 3.3, 2.0], "SMART objectives and KPI targets (goals)", size=9)

    # 4 ----------------------------------------------------------------------------------------
    d.h1("4. Recommended solution")
    d.h2("AI agents")
    d.table(["Agent", f"Role for {CL}"], [
        ("Strategist", "Breaks the goal into campaigns, allocates budget across channels and forecasts ROI."),
        ("Creator", "Writes multilingual copy ([[LANGUAGES]]) and generates images for posts, broadcasts and ads."),
        ("Publisher", "Schedules content, runs WhatsApp catalog and checkout flows."),
        ("Analyst", "Keeps campaign memory, runs cohort analysis and optimises what's working."),
        ("Specialist Flux agents (as needed)", "[[e.g. Flux Sales, Support, Commerce, Nurture, Insights]] from the "
                                               "23 specialist agents and the AI Agent Marketplace."),
    ], [4.6, 12.4], "AI agents and roles")
    d.h2("Channels")
    d.table(["Channel", "Use", "Status"], [
        ("WhatsApp (Cloud API)", "Chatbot, WhatsApp Flows, broadcasts with approved templates, catalog and checkout", "Live"),
        ("Facebook Page and Messenger", "Scheduled posts, Messenger bot, social metrics", "Live"),
        ("Instagram", "Publishing, comments and DMs", "Pending Meta approval, not live"),
        ("Email", "Sending domains, sequences, suppression lists", "Live"),
        ("SMS and USSD", "SMS broadcasts; USSD menus for feature phones (Growth)", "Live"),
        ("Website chat widget, landing pages, link-in-bio", "Capture and convert traffic into WhatsApp chats", "Live"),
    ], [4.6, 8.8, 3.6], "Channels and status")
    d.h2("WhatsApp commerce")
    d.bullets([
        "Catalog of [[N]] products synced from [[Shopify / WooCommerce / manual upload]].",
        "Cart checkout inside the chat, paid through [[Yoco / Ozow / Paystack]], with order status notifications.",
        "Abandoned-cart recovery messages and segments for retargeting.",
        "wa.me short links and QR codes for ads, packaging, in-store and staff.",
    ])
    d.h2("Integrations (tick what applies)")
    d.table(["Applies", "Integration", "What it does for the pilot"], [
        ("[ ] ", "Shopify", "Sync products, stock and orders with the WhatsApp catalog"),
        ("[ ] ", "WooCommerce", "Sync products and orders from the website store"),
        ("[ ] ", "Takealot", "Keep marketplace listings and campaigns aligned [[CONFIRM SCOPE]]"),
        ("[ ] ", "HubSpot / CRM sync", "Push leads, deals and conversations to the CRM"),
        ("[ ] ", "Accounting sync", "Send orders and payments to [[ACCOUNTING PACKAGE]]"),
        ("[ ] ", "Slack", "Alerts for escalations, big orders and approvals"),
        ("[ ] ", "Zapier and public API", "Connect other tools (API access is on Scale)"),
    ], [1.8, 4.0, 11.2], "Integrations checklist", first_col_bold=False, aligns=["center", None, None])
    d.h2("Growth and CRM")
    d.para("Lead scoring, CRM deals, customer segmentation, loyalty programmes, churn-risk scoring, sentiment analysis "
           "with escalation, A/B testing, competitor tracking and custom reports. Workflows run in Flux Automate.")
    d.figure("infographics/platform-stack.png",
             "One platform from channel to checkout. Instagram is pending Meta approval and not live yet.",
             "Six-layer platform stack: channels, AI workforce, commerce and payments with five live rails, growth "
             "and CRM, integrations, and trust.")

    # 5 ----------------------------------------------------------------------------------------
    d.h1("5. Scope of work and deliverables")
    d.para("**Included** = part of the FluxMuse plan. **Optional** = a FluxMuse service at an extra fee [[TBC]]. "
           f"**Client** = what {CL} provides.", size=9.5)
    d.table(["Area", "Deliverable", "Included", "Optional [[TBC]]", "Client responsibility"], [
        ("Setup", "WhatsApp Business number via Embedded Signup and business profile",
         "Platform and guided onboarding call", "Hands-on set-up service", "Meta Business account access, number, display name"),
        ("Setup", "Catalog of [[N]] products", "Catalog tools and store sync", "Catalog build by our team",
         "Product data, images, prices, stock"),
        ("Setup", "Payment rail for checkout in chat", "Yoco, Ozow or Paystack connection", "–",
         "Merchant account and provider verification"),
        ("Setup", "Integrations", "Native connectors", "Custom API or Zapier work", "Admin access and API keys"),
        ("Content", "Content calendar, copy and images in [[LANGUAGES]]", "Creator agent drafts and AI images",
         "Human copy and design review", "Brand guidelines, approvals, product photos"),
        ("Automation", "Chatbot, WhatsApp Flows and broadcast templates", "Builders and templates",
         "Flow design workshop", "FAQs, policies, opted-in contact lists"),
        ("Automation", "Order updates and abandoned-cart recovery", "Included on Growth", "–", "Approve message wording"),
        ("Automation", "Workflows (Flux Automate)", "Workflow builder", "Advanced workflow build", "Process owner"),
        ("Training", "Team onboarding", "Guided onboarding call", "Extra training sessions", "[[N]] staff attend"),
        ("Reporting", "Dashboards, weekly check-ins, 30- and 60-day reports", "Analyst and custom reports",
         "Monthly strategy review pack", "Attend reviews, act on actions"),
        ("Paid media", "Ads for the pilot", "AI ad procurement tools [[CONFIRM SCOPE]]", "Campaign management",
         "Ad budget (pass-through)"),
    ], [2.0, 4.4, 3.5, 3.3, 3.8], "Scope of work: included, optional and client responsibilities", size=8.5)
    d.para("**Out of scope unless agreed in writing:** [[e.g. photo or video shoots, website rebuilds, paid influencer "
           "fees, printing]].", size=9.5)

    # 6 ----------------------------------------------------------------------------------------
    d.h1("6. 60-day pilot plan")
    d.para(f"The pilot follows the same structure as FluxMuse's Gauteng pilot. For {CL} we run days 1–60, with days "
           "61–90 as an optional extension.")
    d.figure("infographics/brand-engagement-journey.png",
             "How we work together, from discovery call to a plan. Timings are typical; KPI targets are goals.",
             "Six-step journey: discovery call, audit and strategy, setup, pilot campaign, report and optimise, "
             "convert to a plan, with KPIs tracked from day one.")
    d.table(["Phase", "Objectives", "Deliverables", "Metrics tracked"], [
        ("Days 1–30\nLaunch and baseline", "Go live on WhatsApp plus one social channel; measure a clean baseline",
         "Number and catalog live; payment rail connected; 30-day content calendar; chatbot or FAQ flow; baseline report",
         "Conversations started; catalog views and first orders; content published on schedule"),
        ("Days 31–60\nOptimise conversion", "Lift chat-to-order conversion; test offers, messages and audiences",
         "A/B tests; abandoned-cart recovery on; segments and broadcast templates; mid-pilot report",
         "Chat-to-order conversion; recovered carts; cost per conversation; response time"),
        ("Days 61–90 (optional)\nScale what works", "Double down on winning channels; choose a plan",
         "Add email, SMS or USSD; loyalty programme; end-of-pilot report and case study (with consent)",
         "Orders and GMV; conversion uplift; repeat purchases; hours saved; NPS"),
    ], [3.3, 4.0, 5.2, 4.5], "Pilot phases", size=9)
    d.figure("infographics/pilot-campaign-framework.png",
             "The 30/60/90-day pilot framework used in the Gauteng pilot (12 brands, September to 30 November 2026). "
             "Targets are goals agreed at kickoff.",
             "Three pilot phases (launch and baseline, optimise conversion, scale what works) with objectives, "
             "deliverables and metrics tracked for each.")

    # 7 ----------------------------------------------------------------------------------------
    d.h1("7. Timeline")
    weeks = ["W0", "W1", "W2", "W3", "W4", "W5", "W6", "W7", "W8", "W9"]
    g = lambda spec: tuple(spec.get(w, "") for w in weeks)
    rows = [
        ("Discovery call and audit",) + g({"W0": "##", "W1": "#"}),
        ("Setup: WhatsApp, catalog, payments",) + g({"W1": "##", "W2": "##"}),
        ("Integrations",) + g({"W1": "#", "W2": "#"}),
        ("Content calendar and chatbot flows",) + g({"W1": "#", "W2": "##", "W3": "#"}),
        ("Launch and baseline (days 1–30)",) + g({"W2": "##", "W3": "##", "W4": "##", "W5": "##"}),
        ("Mid-pilot report",) + g({"W5": "##"}),
        ("Optimise conversion (days 31–60)",) + g({"W6": "##", "W7": "##", "W8": "##", "W9": "#"}),
        ("Weekly check-ins",) + g({w: "#" for w in weeks[2:]}),
        ("60-day report and plan decision",) + g({"W9": "##"}),
    ]
    d.table(["Activity"] + weeks, rows, [5.0] + [1.2] * 10, "Pilot timeline (Gantt)", size=8.5, gantt=True,
            zebra=False, aligns=[None] + ["center"] * 10)
    d.para("● dark = main activity, ● light = supporting activity. W0 = the week before go-live.", size=8.5, color="5B6570")
    d.table(["Milestone", "Date"], [
        ("Proposal accepted", "[[DATE]]"), ("Kickoff and discovery", "[[DATE]]"), ("Go-live", "[[DATE]]"),
        ("Mid-pilot review (day 30)", "[[DATE]]"), ("Final review and plan decision (day 60)", "[[DATE]]"),
    ], [9.0, 8.0], "Key milestones")

    # 8 ----------------------------------------------------------------------------------------
    d.h1("8. Investment options")
    d.table(["Plan", "Monthly", "Annual (10×)", "Founding Member*", "Includes"], [
        ("Growth (recommended)", "R1,999", "R19,990", "R1,399 for the first 2 monthly bills",
         "3 brands, 15 channels, 25,000 AI credits/mo; e-commerce and WhatsApp commerce, USSD, integrations; email support"),
        ("Scale", "R4,999", "R49,990", "R3,499 for the first 2 monthly bills",
         "10 brands, 40 channels, 100,000 AI credits/mo; API access, white-label reports, priority support"),
    ], [3.0, 2.0, 2.3, 3.5, 6.2], "Plan investment options", size=9, highlight_rows=(0,))
    d.para("*Founding Member: South African sign-ups from 1 December 2026 to 31 January 2027 pay 30% less for the "
           "first 2 monthly bills, or get 2 extra months free on an annual plan, plus a Founding Member badge and "
           "priority support. [[DELETE IF NOT ELIGIBLE]] Gauteng pilot brands: Growth R999 or Scale R2,499 for the first "
           "2 monthly bills from 1 December 2026. Every plan starts with a 14-day free trial, no card required.",
           size=9)
    d.figure("infographics/pricing-tiers.png",
             "FluxMuse plans in ZAR. Annual = 10× monthly. Enterprise is quoted on request.",
             "Pricing tiers: Starter R499, Growth R1,999 (most popular), Scale R4,999 and Agency R7,999 a month, with "
             "brands, channels, AI credits and highlights, and the Founding Member ribbon.")
    d.h2("Optional FluxMuse services")
    d.table(["Service", "Fee", "Notes"], [
        ("Guided onboarding call", "Included", "Part of every Growth and Scale onboarding"),
        ("Hands-on set-up service", "[[TBC]]", "Number, catalog, flows and integrations set up by our team"),
        ("Catalog build", "[[TBC]]", "Up to [[N]] products"),
        ("Content and design review", "[[TBC]] /mo", "Human review of AI drafts"),
        ("Campaign management", "[[TBC]] /mo", "Planning, launch and optimisation of paid campaigns"),
        ("Extra training", "[[TBC]] per session", "For additional teams or branches"),
    ], [5.0, 3.0, 9.0], "Optional services fees")
    d.h2("Third-party pass-through costs")
    d.para("These are charged by the provider at their rates, not by FluxMuse. They are estimates until usage is known.",
           size=9.5)
    d.table(["Cost", "Charged by", "Estimate", "Depends on"], [
        ("WhatsApp conversation and template message fees", "Meta", "[[estimate R/mo]]", "Message volume and category"),
        ("Ad spend", "Meta [[/ other ad platforms]]", "[[estimate R/mo]]", f"Budget set by {CL}"),
        ("SMS sending", "SMS provider", "[[estimate R/mo]]", "Number of messages"),
        ("Payment processing", "Yoco / Ozow / Paystack", "[[provider rates]]", "Transaction value and method"),
    ], [5.6, 3.6, 3.2, 4.6], "Third-party pass-through costs")
    d.h2("First three months at a glance")
    d.table(["Item", "Month 1", "Month 2", "Month 3"], [
        ("FluxMuse plan ([[Growth / Scale]])", "[[R]]", "[[R]]", "[[R]]"),
        ("Optional services", "[[TBC]]", "[[TBC]]", "[[TBC]]"),
        ("Pass-through costs (estimate)", "[[R]]", "[[R]]", "[[R]]"),
        ("Total (excl. VAT)", "[[R]]", "[[R]]", "[[R]]"),
    ], [7.0, 3.3, 3.3, 3.4], "Three-month investment summary", total_rows=(3,), aligns=[None, "right", "right", "right"])
    d.para("Campaign Financing (campaign credit facilities and instalment plans) may be available for ad spend: "
           "[[CONFIRM ELIGIBILITY]].", size=9.5)

    # 9 ----------------------------------------------------------------------------------------
    d.h1("9. Payments and markets")
    d.para(f"In South Africa {CL}'s customers can pay by Yoco card, Ozow instant EFT or Paystack, and Fincra supports "
           f"collections. {C.RAILS_LINE}")
    d.table(["Rail", "Type", "Countries"], [
        ("Yoco", "Card acquiring, tap-to-pay", "South Africa"),
        ("Ozow", "Instant EFT / pay-by-bank", "South Africa"),
        ("Paystack", "Cards, bank transfer, USSD, mobile money", "Nigeria, Ghana, South Africa, Kenya, Côte d'Ivoire, Rwanda"),
        ("pawaPay", "Mobile money collections and payouts, 40+ mobile money operators", "20 countries, including Ghana, Kenya, Nigeria, Uganda, Tanzania, Zambia"),
        ("Fincra", "Collections (virtual accounts, cards, bank, mobile money) and payouts", "Collections hubs: Nigeria, Ghana, Kenya, Uganda, South Africa"),
    ], [2.4, 6.2, 8.4], "Payment rails", size=9)
    d.figure("infographics/payment-coverage-map.png",
             "Local payments in 23 African countries; Botswana and Namibia coming soon.",
             "Tile map of Africa showing 23 rail-covered countries shaded by number of rails, South Africa with four, "
             "and Botswana and Namibia as coming soon.")
    d.bullets([
        f"If {CL} sells in Nigeria, Kenya or Ghana, those customers are billed in local currency; the other 19 "
        "rail-covered countries in USD. See Appendix A.",
        "Countries without a payment rail are gated: businesses there can join the waitlist, but we don't quote prices "
        "or open checkout.",
    ])

    # 10 ---------------------------------------------------------------------------------------
    d.h1("10. Reporting and governance")
    d.table(["Cadence", "What", "Who", "Format"], [
        ("Always on", "Live dashboard: conversations, orders, GMV, content, campaigns", f"{CL} team", "FluxMuse app"),
        ("Weekly (pilot)", "30-minute check-in: progress against targets, blockers, next actions",
         "[[FLUXMUSE LEAD]] + [[CLIENT OWNER]]", "Call + written actions"),
        ("Day 30", "Mid-pilot report and test plan for days 31–60", "Both teams", "Report"),
        ("Monthly", "Performance report and recommendations", "[[FLUXMUSE LEAD]]", "Custom report"),
        ("Day 60", "Final pilot review and plan decision", "Decision makers", "Report + meeting"),
        ("Quarterly (after pilot)", "Business review [[OPTIONAL]]", "Decision makers", "Meeting"),
    ], [3.0, 7.2, 3.8, 3.0], "Reporting cadence", size=9)
    d.h2("Roles")
    d.table(["Role", "Name", "Responsible for"], [
        ("FluxMuse account lead", "[[NAME]]", "Plan, setup, reports, escalations"),
        (f"{CL} project owner", "[[NAME]]", "Access, data, internal decisions"),
        ("Content approver", "[[NAME]]", "Approves campaigns in FluxMuse's approvals workflow"),
        ("Escalation contact", "[[NAME]]", "Commercial and service issues"),
    ], [5.0, 4.0, 8.0], "Governance roles")

    # 11 ---------------------------------------------------------------------------------------
    d.h1("11. Proof")
    d.para("FluxMuse is running a **12-brand pilot in Gauteng from September to 30 November 2026** across solo "
           "entrepreneurs, SMEs and agencies. The pilot is underway and results will be published from December 2026, "
           "only with each brand's written consent.")
    d.figure("infographics/case-study-template.png",
             "Case-study format (template). It will be completed with consented pilot data from December 2026; "
             "it contains no results today.",
             "Case study template for a Gauteng braiding and hair studio with placeholder fields for brand, "
             "challenge, set-up, three metrics with target goals, and an owner quote, stamped pilot data pending.")
    d.table(["Relevant pilot archetype", "Why it matters to " + CL, "Status"], [
        ("Restaurant or shisanyama with WhatsApp orders", "[[RELEVANCE]]", "Pilot underway, results December 2026"),
        ("Online fashion or beauty brand (Shopify / WooCommerce)", "[[RELEVANCE]]", "Pilot underway, results December 2026"),
        ("Clinic, dental or optometry practice", "[[RELEVANCE]]", "Pilot underway, results December 2026"),
        ("Car wash, auto services or dealership", "[[RELEVANCE]]", "Pilot underway, results December 2026"),
        ("Multi-branch retailer or franchise", "[[RELEVANCE]]", "Pilot underway, results December 2026"),
    ], [6.4, 5.6, 5.0], "Pilot case study placeholders", size=9)

    # 12 ---------------------------------------------------------------------------------------
    d.h1("12. Trust and compliance")
    C.trust_bullets(d)
    C.popia_clause(d)

    # 13 ---------------------------------------------------------------------------------------
    d.h1("13. Assumptions and client dependencies")
    d.bullets([
        f"{CL} gives FluxMuse admin access to its Meta Business account, Facebook Page and store within [[N]] working days of kickoff.",
        "A phone number is available for the WhatsApp Business account and Meta approves the display name.",
        "WhatsApp broadcasts use Meta-approved templates and go only to contacts who opted in.",
        f"{CL} provides product data, prices, stock, images and brand guidelines, and approves content within [[N]] working days.",
        "Payment provider merchant accounts are opened and verified by the client.",
        "Ad budgets and third-party message fees are paid by the client (pass-through).",
        "Instagram features become available only after Meta approval; the pilot plan doesn't depend on them.",
        "Targets are set against the baseline measured in the first weeks of the pilot.",
        "[[OTHER ASSUMPTIONS]]",
    ])

    C.terms(d, 14)
    C.acceptance(d, 15, [
        "Growth, monthly (R1,999/mo)", "Growth, annual (R19,990/yr)",
        "Scale, monthly (R4,999/mo)", "Scale, annual (R49,990/yr)",
        "Founding Member pricing (subscribing 1 Dec 2026 to 31 Jan 2027)",
        "Optional services: [[LIST]]",
        "60-day pilot as described, starting [[DATE]]",
    ], terms_num=14)
    regional_appendix(d)
    d.save(out_path, "FluxMuse proposal: SME growth", "Marketing proposal template")
    return d
