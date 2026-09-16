"""Sections 1-4: executive summary, company overview, problem & opportunity, solution."""
from bp_doc import ANN, BASE, D, DEEP, M, TINT, ann, ann_sub, pct, rand, rk, rm, usd

FY_REV = ann("total_revenue_zar")
FY_EBITDA = ann("ebitda_zar")
FY_WS = ann("ending_paying_workspaces")
FY_ARR = ann("subscription_arr_zar")
FY_CASH = ann("closing_cash_zar")
FY_HC = ann("headcount_end_fy")
CASH = M["cash"]
UOF = M["use_of_funds"]
REC24 = UOF["reconciliation"]["24"]


def s1_executive_summary(d):
    d.h1("1. Executive summary")
    d.para("**FluxMuse is an AI marketing team and a WhatsApp commerce platform, built for African "
           "small and medium businesses.** It plans, writes, publishes and optimises marketing across "
           "WhatsApp, Facebook, email, SMS and USSD, and it closes the sale inside the chat: catalog, cart, "
           "checkout and order updates, paid for through local payment rails. The company is Fluxmuse Pty Ltd, "
           "a South African company and a Meta-verified Tech Provider.")

    d.h2("The opportunity")
    d.bullets([
        "Africa has an estimated **44 million MSMEs** (IFC/World Bank est.), about **2.5–3 million SMMEs in "
        "South Africa** (SEDA/Stats SA est.), **39 million in Nigeria** (SMEDAN est.) and **7.4 million in "
        "Kenya** (KNBS est.). All estimates; see section 5.",
        "They already sell where their customers are: **more than 90% of internet users in South Africa and "
        "Nigeria use WhatsApp** (DataReportal 2025 est.), and Sub-Saharan Africa accounts for about **70% of "
        "global mobile money value** (GSMA 2025 est.).",
        "What they lack is a marketing team they can afford and a way to take payment inside the conversation. "
        "Global tools are priced in dollars, aren't built for local payment methods or languages, and stop at "
        "the post rather than the sale.",
    ])

    d.h2("The solution")
    d.bullets([
        "**Four core AI agents** (Strategist, Creator, Publisher, Analyst) plus 23 specialists, producing "
        "content in isiZulu, Pidgin, Swahili, Afrikaans, English and more.",
        "**WhatsApp commerce**: catalog, cart, checkout, order status and abandoned-cart recovery.",
        "**Five secured payment rails** (Yoco, Ozow, Paystack, pawaPay, Fincra), all live September 2026, "
        "covering **23 African countries**; Botswana and Namibia coming soon.",
        "**Local pricing** from R499 a month, with fixed local price points in Nigeria, Kenya and Ghana and US "
        "dollar pricing in the other 19 rail-covered countries.",
    ])

    d.h2("Where we are today")
    d.bullets([
        "**The product is live and shipping**: agents, WhatsApp commerce, publishing, campaigns, CRM, "
        "automation and integrations.",
        "**Meta Business and Access Verification (Tech Provider): verified**, with WhatsApp messaging and "
        "management permissions approved. Instagram publishing, comments and DMs, Pages posting and business "
        "management are **in Meta App Review and not live yet**.",
        "**A 12-brand Gauteng pilot runs to 30 November 2026.** Pilot brands pay nothing; first paid "
        "conversions and first consented case studies come in **December 2026**. No customer results exist "
        "before then.",
    ])

    d.h2("Business model and go to market")
    d.para("Recurring subscriptions (Starter R499, Growth R1,999, Scale R4,999, Agency R7,999 a month; "
           "Enterprise from R19,999), annual at 10× monthly. Agencies buy the Agency tier at a **partner "
           "wholesale price of R5,599 a month** (30% off list) and set their own retail price. South Africa "
           "first (national launch 1 December 2026), then Nigeria, Kenya and Ghana, then the other 19 "
           "rail-covered countries self-serve in US dollars. Three segments: solo entrepreneurs, SMEs and "
           "agencies; Enterprise is inbound only.")

    d.h2("Financial highlights")
    d.para("Base case of the FluxMuse Financial Model v2. These are forward-looking projections, not results.")
    d.fy_table("Financial highlights, FY1-FY5 (Base case)", [
        ["Revenue (R m)"] + [rm(v) for v in FY_REV],
        ["EBITDA (R m)"] + [rm(v) for v in FY_EBITDA],
        ["EBITDA margin"] + ["n/m"] + [pct(a["ebitda_margin_pct"]) for a in ANN[1:]],
        ["Paying workspaces (Sept)"] + [f"{v:,}" for v in FY_WS],
        ["Subscription ARR (R m)"] + [rm(v) for v in FY_ARR],
        ["Closing cash (R m)"] + [rm(v) for v in FY_CASH],
        ["Headcount at year end"] + [str(v) for v in FY_HC],
    ], total_rows=())
    d.source()
    d.bullets([
        f"**EBITDA break-even {CASH['break_even_month']}**, positive every month from "
        f"{CASH['break_even_month_sustained']}; operating cash flow positive from "
        f"{CASH['cash_flow_positive_month']}.",
        f"**The R25M carries the business to profitability on its own.** Minimum cash after the seed is "
        f"{rm(CASH['min_post_seed_cash_zar'], 2)} in {CASH['min_post_seed_cash_month']}, "
        f"{rm(CASH['headroom_over_buffer_zar'], 2)} above the {rm(CASH['min_cash_buffer_zar'], 1)} "
        "minimum-cash buffer, with no Series A in the plan.",
        "**All three scenarios stay profitable on the R25M alone** (section 12).",
    ])

    d.h2("The ask: R25 million seed")
    d.para("Fluxmuse Pty Ltd is raising **R25 million (about US$1.35 million)**, modelled to close in "
           "February 2027. Instrument and valuation: **[[INSTRUMENT: SAFE OR PRICED EQUITY]]**, "
           "**[[PRE-MONEY VALUATION: TBC]]**.")
    d.table(["Use of funds", "Share", "R million", "What it buys"], [
        (a["category"], pct(a["share_pct"]), rm(a["amount_zar"], 2), a["what_it_buys"].split(";")[0] + ".")
        for a in UOF["allocation"]
    ], [4.4, 1.5, 1.9, 9.2], "Use of the R25M seed", size=9,
        aligns=[None, "right", "right", None])
    d.note("Section 13 reconciles this allocation against modelled spend and explains the two gaps: expansion is "
           "under-spent against its 15% share because the launch gates delay it, and operations is over it "
           "because revenue-linked costs scale with revenue.")

    d.h2("Why this team")
    d.para("**[[FOUNDER NAME, TITLE]]** — [[BACKGROUND: WHAT THEY HAVE BUILT AND SOLD BEFORE, YEARS IN MARKET, "
           "WHY THIS PROBLEM]]. **[[CO-FOUNDER / CTO NAME, TITLE]]** — [[BACKGROUND]].")
    d.para("**[[TEAM: THE CURRENT TEAM AND WHAT THEY HAVE SHIPPED]]** and **[[ADVISORS]]**.")
    d.callout("What is already de-risked", [
        "- The product is built and live, not a concept: the AI agents, WhatsApp commerce and five payment "
        "rails work today.",
        "- Meta Business and Access Verification (Tech Provider) are approved, which is a slow, gated process "
        "for any WhatsApp platform.",
        "- Payment coverage across 23 countries is contracted, so expansion is a sales question.",
        "- The plan needs no second round: the base, conservative and upside cases all reach profitability on "
        "this R25M.",
    ], fill=TINT, caption="Layout: de-risking callout")


def s2_company_overview(d):
    d.h1("2. Company overview", new_page=True)
    d.h2("Legal entity and ownership")
    d.kv_table([
        ("Registered name", "Fluxmuse Pty Ltd"),
        ("Jurisdiction", "South Africa"),
        ("Registration number", "[[COMPANY REGISTRATION NUMBER]]"),
        ("Date of incorporation", "[[FOUNDING DATE]]"),
        ("Registered address", "[[REGISTERED ADDRESS]]"),
        ("Operating location", "[[OPERATING LOCATION / OFFICE]]"),
        ("Directors", "[[DIRECTORS]]"),
        ("Shareholders and cap table", "[[CAP TABLE: SHAREHOLDERS AND PERCENTAGES, OPTION POOL]]"),
        ("B-BBEE status", "[[B-BBEE LEVEL AND VERIFICATION DATE]]"),
        ("Tax and VAT", "[[INCOME TAX NUMBER]] · [[VAT NUMBER / VAT TREATMENT]]"),
        ("Auditor / accountant", "[[AUDITOR OR ACCOUNTING OFFICER]]"),
        ("Banker", "[[BANK]]"),
        ("Product", "FluxMuse (fluxmuse.ai): AI marketing and WhatsApp commerce platform"),
    ], widths=(5.0, 12.0), caption="Layout: company details")
    d.note("Every field marked [[ ]] must be completed from the company records before this plan goes to a "
           "funder. Development-finance funders will also ask for the items listed in Appendix E.")

    d.h2("Mission, vision and promise")
    d.para("**Mission.** Give every African business a marketing team and a checkout, inside the chat app its "
           "customers already use.")
    d.para("**Vision.** A braider in Tembisa, a baker in Lagos and an agency in Nairobi market, sell and get "
           "paid as easily as any global brand, in their own language and their own currency.")
    d.para("**Promise.** Less admin, more sales you can see.")
    d.note("Mission, vision and promise are v1.0 drafts from the brand kit and need founder sign-off before "
           "external use. [[FOUNDER SIGN-OFF ON MISSION, VISION AND PROMISE]]")

    d.h2("Platform verification and regulatory status")
    d.table(["Area", "Status"], [
        ("Meta Business Verification", "Verified"),
        ("Meta Access Verification", "Verified (Tech Provider)"),
        ("Meta permissions approved",
         "pages_show_list, pages_manage_metadata, pages_messaging, whatsapp_business_messaging, "
         "whatsapp_business_management, public_profile"),
        ("In Meta App Review (not live)",
         "pages_manage_posts, pages_read_engagement, instagram_basic, instagram_content_publish, "
         "instagram_manage_comments, instagram_manage_messages, business_management"),
        ("Payment licensing",
         "FluxMuse is not a payment institution. Collections and payouts run through licensed providers: "
         "Yoco, Ozow, Paystack, pawaPay and Fincra, which hold the relevant licences in their markets."),
        ("Data protection",
         "Built to be POPIA, NDPR and GDPR ready: row-level security on every table, encrypted tokens, audit "
         "export, data export and account deletion. Information Officer: [[INFORMATION OFFICER NAME AND EMAIL]]"),
        ("Registrations outstanding",
         "[[NDPR / NDPA, KENYA DPA AND GHANA DPC REGISTRATIONS: STATUS]] · [[VAT REGISTRATIONS FOR "
         "SELF-SERVE MARKETS]]"),
        ("Intellectual property",
         "Platform code, brand and the Muse icon owned by Fluxmuse Pty Ltd. Trade mark registration: "
         "[[TRADE MARK STATUS]]"),
    ], [4.2, 12.8], "Verification and regulatory status", size=9)
    d.note("Instagram features stay switched off in the product until Meta approves them, and are never sold as "
           "live. This is the single biggest platform dependency in the plan (section 14).")


def s3_problem(d):
    d.h1("3. Problem and opportunity", new_page=True)
    d.h2("The problem")
    d.para("A small business in Johannesburg, Lagos or Nairobi sells through WhatsApp, Instagram and Facebook. "
           "Marketing is a person, usually the owner, doing it late at night between jobs. The tools that exist "
           "were built for somewhere else:")
    d.bullets([
        "**A patchwork of disconnected tools** for posts, chats, email, SMS and payments, none of which talk to "
        "each other.",
        "**Agency retainers priced beyond most small-business budgets**, with little visibility of what the "
        "money bought.",
        "**Buyers drop off** when a conversation sends them to an external payment link.",
        "**Checkout that doesn't offer local ways to pay**, such as instant EFT or mobile money.",
        "**Content in the wrong language and register** for the customer being sold to.",
    ])
    d.figure("infographics/problem-solution.png",
             "The problem we solve, and what replaces it.",
             "Comparison: today, a stack of disconnected tools, agency retainers, payment-link drop-off and "
             "checkout without local payment options; with FluxMuse, one AI marketing team, plans from R499 a "
             "month with a 14-day free trial, catalog and checkout inside WhatsApp, and five local payment rails.")

    d.h2("Why now")
    d.bullets([
        "**The channel is settled.** WhatsApp is where African SMBs already sell, and the WhatsApp Cloud API "
        "makes catalog and checkout inside the chat possible for small businesses, not only enterprises.",
        "**Payments have caught up.** Mobile money and instant EFT now reach across the continent through "
        "aggregators, so a platform can collect and pay out in 23 countries without 23 integrations.",
        "**AI has made the marketing team affordable.** What used to need a strategist, a copywriter, a "
        "designer and an analyst can now run as agents at a price a R499-a-month business can pay.",
        "**The gate is verification, not code.** Meta Tech Provider verification and payment-rail contracts "
        "take months and are already held.",
    ])

    d.h2("The gap in the market")
    d.para("Global social-media tools publish but don't sell, and don't support local payment methods. "
           "WhatsApp chatbot vendors handle conversations but don't do marketing or content. E-commerce "
           "platforms sell on a website, not inside a chat. Local agencies deliver services at retainer prices "
           "that most of this market cannot pay. **Nobody covers plan → create → publish → sell → get paid → "
           "learn in one product, priced in local currency.** Section 7 sets this out in detail.")


def s4_solution(d):
    d.h1("4. Solution: products and services", new_page=True)
    d.para("FluxMuse is one platform that runs a marketing loop and closes the sale in the same place.")
    d.figure("infographics/how-fluxmuse-works.png",
             "The loop: Plan, Create, Publish, Sell, Learn, run by the four core agents.",
             "Circular diagram: Strategist plans goals, channel mix, budget and ROI forecast; Creator writes "
             "multilingual copy and images; Publisher schedules to social, WhatsApp, email, SMS and USSD; "
             "WhatsApp commerce sells with catalog, cart and local payments; Analyst learns from orders and "
             "data and feeds insights back to the Strategist.")

    d.h2("The AI marketing team")
    d.table(["Agent", "What it does"], [
        ("Strategist", "Goal decomposition, budget allocation, ROI forecasting"),
        ("Creator", "Multilingual copy in isiZulu, Pidgin, Swahili, Afrikaans, English and more; image "
                    "generation"),
        ("Publisher", "Scheduling, WhatsApp catalog and checkout flows"),
        ("Analyst", "RAG memory, cohort analysis, auto-optimisation"),
        ("23 specialist Flux agents",
         "Content, Create, Design, Ads, Growth, Nurture, Sales, Support, Commerce, Community, Insights, "
         "Advisor, Finance, Compliance, Ops, DevOps, Integrate, Onboarding, Partner, Product, Discover, "
         "Personal and Agentic, plus an AI Agent Marketplace"),
    ], [4.2, 12.8], "The AI marketing team", size=9.5)
    d.figure("infographics/ai-agent-roster.png",
             "Four core agents, backed by 23 specialists and an agent marketplace.",
             "Cards for Strategist, Creator, Publisher and Analyst with their responsibilities, and the 23 "
             "specialist Flux agents grouped into marketing and content, sales and service, and business and "
             "operations.")

    d.h2("WhatsApp commerce")
    d.para("The differentiator: the customer never leaves the conversation. Discovery through an ad, post, QR "
           "code or wa.me link; a chatbot or WhatsApp Flow replies; the buyer browses the catalog, fills a cart "
           "and pays through a local rail; the order is confirmed with status updates; loyalty and retargeting "
           "bring them back. Abandoned carts trigger an automatic recovery message.")
    d.figure("infographics/whatsapp-commerce-flow.png",
             "From first tap to repeat order, inside WhatsApp.",
             "Flow: Discover, Chat, Catalog, Cart, Pay through Yoco card, Ozow EFT, Paystack, pawaPay mobile "
             "money and Fincra, Confirmed, Loyalty, with abandoned-cart recovery and retargeting loops.")

    d.h2("The platform")
    d.figure("infographics/platform-stack.png",
             "One platform, from channel to checkout. Instagram is marked as in Meta review, not live.",
             "Six-layer stack: channels including WhatsApp Cloud API, Facebook Pages, Instagram in Meta review, "
             "Messenger, email, SMS, USSD, website chat widget and link-in-bio; the AI workforce; commerce and "
             "payments with five live rails; growth and CRM; integrations; and trust.")

    d.h2("What is live, in review, and on the roadmap")
    d.table(["Capability", "Status"], [
        ("AI agents, content, campaigns, calendar, templates", "Live"),
        ("WhatsApp Cloud API: contacts, templates, Flows, chatbots, catalog, cart checkout, orders, "
         "abandoned-cart recovery", "Live"),
        ("Facebook Pages publishing and Messenger bot", "Live"),
        ("Email marketing, SMS broadcasts, USSD handler, landing pages, link-in-bio, A/B testing", "Live"),
        ("Growth and CRM: lead scoring, deals, segmentation, loyalty, churn risk, sentiment, custom reports",
         "Live"),
        ("Automation and integrations: workflow builder, Zapier, public API, Shopify, WooCommerce, Takealot, "
         "HubSpot, accounting sync, Slack", "Live"),
        ("Agency white-label, sub-accounts, reseller billing, partner directory", "Live"),
        ("Payments: Yoco, Ozow, Paystack live in product; pawaPay and Fincra live September 2026",
         "Live September 2026"),
        ("Instagram publishing, comments and DMs; Facebook Pages posting and engagement insights; "
         "business management", "In Meta App Review, not live"),
        ("Social adapters: Instagram Login, Threads, LinkedIn, X, TikTok, YouTube, Pinterest", "Roadmap stage 2"),
        ("Further business-app integrations: commerce, CRM, accounting, email and SMS providers",
         "Roadmap stage 3"),
        ("Flux_Partner programme: referral tracking, partner-managed workspaces", "Roadmap stage 4"),
        ("Fixed local price points in the app for Nigeria, Kenya and Ghana, and a Ghana region",
         "Roadmap: the app currently converts ZAR at the day's FX rate"),
    ], [11.0, 6.0], "What is live, in review and on the roadmap", size=9)
    d.note("Nothing in Meta App Review is sold, demonstrated or priced as live until Meta approves it.")

    d.h2("The agency and white-label offering")
    d.para("Agencies and resellers join the Flux_Partner programme and buy the Agency tier at the partner "
           "wholesale price of **R5,599 a month** (30% off the R7,999 list price): full white-label, 50 client "
           "sub-accounts, reseller billing, 80 channels, 500,000 AI credits and dedicated support. The partner "
           "sets its own retail price for its clients and keeps the difference.")
    d.figure("infographics/agency-partner-model.png",
             "The partner model. The worked example is illustrative, not a forecast: margin depends on the "
             "retail price the partner sets and on its own costs.",
             "Diagram: FluxMuse bills the agency the partner price of R5,599 a month for full white-label, 50 "
             "client sub-accounts and reseller billing; the agency bills its clients at a retail price it sets. "
             "Illustrative example: 20 clients at R1,500 a month bills R30,000, less R5,599, leaves a gross "
             "spread of R24,401 a month before the partner's own costs.")
    d.note("Illustrative only. FluxMuse does not quote a fixed partner margin percentage, because it depends on "
           "the partner's retail price and delivery costs.")

    d.h2("Trust and compliance")
    d.bullets([
        "Built to be **POPIA, NDPR and GDPR ready**, with row-level security on every database table, encrypted "
        "access tokens, audit export, and data export and account deletion on request.",
        "**WhatsApp policy**: broadcasts use Meta-approved message templates and go only to contacts who opted "
        "in; every broadcast carries a way to opt out.",
        "**Payments** are handled by licensed providers; FluxMuse does not hold customer funds.",
    ])
