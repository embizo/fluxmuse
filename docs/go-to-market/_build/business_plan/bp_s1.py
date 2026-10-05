"""Sections 1-4: executive summary, company overview, problem & opportunity, solution.

Facts: 00_FACTS_AND_ASSUMPTIONS.md and 08_Prospects/CURRENT_OFFER.md. Numbers: model_summary.json (M) and
derived_tables.json (D). Nothing financial is typed by hand.
"""
from bp_doc import ANN, BASE, D, DEEP, M, MODEL_LINE, MV, SEED_M, SEED_WORDS, TINT, ann, ann_sub, pct, rand, rk, rm, usd

FY_REV = ann("total_revenue_zar")
FY_EBITDA = ann("ebitda_zar")
FY_WS = ann("ending_paying_workspaces")
FY_ARR = ann("subscription_arr_zar")
FY_CASH = ann("closing_cash_zar")
FY_HC = ann("headcount_end_fy")
CASH = M["cash"]
UOF = M["use_of_funds"]
REC24 = UOF["reconciliation"]["24"]
PT = M["price_tables"]
ZAR = PT["zar_list_monthly"]
PW = PT["partner_wholesale_monthly"]
PASS = M["profitable_on_seed_alone"]
SC = M["scenarios"]
FG = M["first_group"]
FCS = M["free_conversion_sensitivity"]
SS = M["seed_sizing"]


def s1_executive_summary(d):
    d.h1("1. Executive summary")
    d.para("**FluxMuse gives African small businesses an AI marketing team and a shop that runs on WhatsApp.** "
           "The owner sends product photos on WhatsApp; FluxMuse drafts the catalogue, builds a hosted shop "
           "link, writes captions and images for WhatsApp Status, and sends each order to the owner's own "
           "WhatsApp. The company is Fluxmuse (Pty) Ltd, a South African company and a verified Meta Tech "
           "Provider. The product is **newly launched in South Africa**. FluxMuse has **no paying customers "
           "yet**, and this plan does not pretend otherwise.")

    d.h2("The opportunity")
    d.bullets([
        "Africa has an estimated **44 million MSMEs** (IFC/World Bank est.), about **2.5–3 million SMMEs in "
        "South Africa** (SEDA/Stats SA est.), **39 million in Nigeria** (SMEDAN est.) and **7.4 million in "
        "Kenya** (KNBS est.). All estimates; see section 5.",
        "They already sell where their customers are: **more than 90% of internet users in South Africa and "
        "Nigeria use WhatsApp** (DataReportal 2025 est.).",
        "What they lack is a marketing team they can afford and a simple shop. Global tools are priced in "
        "dollars, are not built around WhatsApp, and stop at the post rather than the sale.",
    ])

    d.h2("The solution")
    d.bullets([
        "**WhatsApp Concierge**: send photos, get catalogue entries to approve with YES, NO or an edit.",
        "**Hosted shop link**: orders arrive as a WhatsApp message to the owner, who replies SOLD.",
        "**AI content**: captions and images (POST), short video clips and voice-note transcription, with "
        "answers in the customer's language.",
        "**WhatsApp Business setup**, templates and broadcasts to consented contacts, and TikTok video posting.",
        f"**Priced in rands**: nine plans in three bands, paid plans from {rand(ZAR['Nano'])} a month.",
    ])

    d.h2("Where we are today")
    d.bullets([
        "**Live, newly launched**: the capabilities above. No merchant has run them end to end yet, so we "
        "quote no results.",
        "**Being switched on**: Facebook and Instagram auto-publishing (Meta permissions not yet approved), "
        "checkout through FluxMuse (built, not yet tested with real money), AI Voice (beta) and the daily "
        "digest.",
        "**Payments**: Paystack is live in South Africa; Yoco and Ozow run FluxMuse's own subscription billing. "
        "pawaPay and Fincra are contracted for expansion, with accounts pending. There is no paid checkout "
        "outside South Africa yet.",
        f"**Opening by hand**: we are opening with a small first group of businesses and setting each one up "
        f"by hand. The model assumes about {FG['per_month']} a month, {FG['months'].replace(' - ', ' to ')} "
        "**[[CONFIRM]]**.",
    ])

    d.h2("Business model and go to market")
    d.para(f"Recurring subscriptions in three bands: Small (Free, Nano {rand(ZAR['Nano'])}, Micro "
           f"{rand(ZAR['Micro'])}), Medium (Starter {rand(ZAR['Starter'])}, Growth {rand(ZAR['Growth'])}, Scale "
           f"{rand(ZAR['Scale'])}) and Enterprise (Corporate {rand(ZAR['Corporate'])}, Agency "
           f"{rand(ZAR['Agency'])}, Custom by consultation). Annual is 10× monthly. Every paid plan starts with "
           f"payment; Free is a permanent plan, not a trial. Agencies resell at a **partner wholesale price of "
           f"{rand(PW['ZAR'])} a month**. South Africa now; Nigeria, Kenya and Ghana once their payment "
           "accounts are live and their revenue gates are met; then other markets self-serve in US dollars.")

    d.h2("Financial highlights")
    d.para(f"Base case of the {MODEL_LINE}. These are forward-looking projections, not results. Every volume "
           "is an assumption, because there are no customers yet.")
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
        f"**In the Base case the {SEED_M} carries the business to profitability with no Series A.** Minimum "
        f"cash after the seed is {rm(CASH['min_post_seed_cash_zar'], 2)} in {CASH['min_post_seed_cash_month']}, "
        f"only {rm(CASH['headroom_over_buffer_zar'], 2)} above the {rm(CASH['min_cash_buffer_zar'], 1)} buffer.",
        f"**Upside passes too. The Conservative case does not**: on {SEED_M} its cash falls below the buffer "
        f"from {SC['Conservative']['first_month_below_buffer']} and EBITDA does not turn positive by Sep 2031 "
        "(section 12).",
        f"**The headroom is thin.** If Free users upgrade at 0.25% a month instead of 0.5%, minimum cash "
        f"falls to {rm(FCS['0.25% a month']['min_post_seed_cash_zar'], 2)} and the Base case fails too.",
    ])

    d.h2(f"The ask: {SEED_WORDS} seed")
    d.para(f"Fluxmuse (Pty) Ltd is raising **{SEED_WORDS} (about {usd(M['seed_usd'])})**, modelled to close "
           f"in {CASH['seed_month']}. The size comes from the model: {rm(SS['smallest_passing_seed_zar_base'], 1)} "
           "is the smallest seed at which the Base case passes, rounded up **[[CONFIRM]]**. Instrument and "
           "valuation: **[[INSTRUMENT: SAFE OR PRICED EQUITY]]**, **[[PRE-MONEY VALUATION: TBC]]**.")
    d.table(["Use of funds", "Share", "R million", "What it buys"], [
        (a["category"], pct(a["share_pct"]), rm(a["amount_zar"], 2), a["what_it_buys"].split(";")[0] + ".")
        for a in UOF["allocation"]
    ], [4.4, 1.5, 1.9, 9.2], f"Use of the {SEED_M} seed", size=9,
        aligns=[None, "right", "right", None])
    d.note("Section 13 reconciles this allocation against modelled spend. Expansion is under-spent against its "
           "15% share in the first two years because Nigeria, Kenya and Ghana open late; operations runs over "
           "because customer success, hosting and AI cost scale with customers.")

    d.h2("Why this team")
    d.para("**Thabo Malebadi, [[TITLE]]**: [[BACKGROUND: WHAT THEY HAVE BUILT AND SOLD BEFORE, YEARS IN "
           "MARKET, WHY THIS PROBLEM]]. **[[CO-FOUNDER / CTO NAME, TITLE]]**: [[BACKGROUND]].")
    d.para("**[[TEAM: THE CURRENT TEAM AND WHAT THEY HAVE SHIPPED]]** and **[[ADVISORS]]**.")
    d.callout("What is already in place, and what is not", [
        "- The product is built and newly launched in South Africa. It has not yet been run end to end by a "
        "real merchant.",
        "- Fluxmuse (Pty) Ltd is a verified Meta Tech Provider, a slow, gated process for any WhatsApp platform.",
        "- Paystack is live in South Africa. Expansion rails are contracted but pending.",
        f"- There are no customers, no pilot and no results. The {SEED_M} reaches profitability in the Base "
        "and Upside cases only, with thin headroom.",
    ], fill=TINT, caption="Layout: status callout")


def s2_company_overview(d):
    d.h1("2. Company overview", new_page=True)
    d.h2("Legal entity and ownership")
    d.kv_table([
        ("Registered name", "Fluxmuse (Pty) Ltd"),
        ("Jurisdiction", "South Africa"),
        ("Registration number", "[[COMPANY REGISTRATION NUMBER]]"),
        ("Date of incorporation", "[[FOUNDING DATE]]"),
        ("Registered address", "[[REGISTERED ADDRESS]]"),
        ("Operating location", "[[OPERATING LOCATION / OFFICE]]"),
        ("Directors", "[[DIRECTORS]]"),
        ("Shareholders and cap table", "[[CAP TABLE: SHAREHOLDERS AND PERCENTAGES, OPTION POOL]]"),
        ("B-BBEE status", "[[B-BBEE LEVEL AND VERIFICATION DATE]]"),
        ("Tax and VAT", "[[INCOME TAX NUMBER]] · not VAT-registered (no active tax types on eFiling, Sept 2026)"),
        ("Auditor / accountant", "[[AUDITOR OR ACCOUNTING OFFICER]]"),
        ("Banker", "[[BANK]]"),
        ("Product", "FluxMuse (fluxmuse.ai): an AI marketing team and a WhatsApp shop for small businesses"),
        ("Contact", "Thabo Malebadi, thabo@fluxmuse.com"),
    ], widths=(5.0, 12.0), caption="Layout: company details")
    d.note("Every field marked [[ ]] must be completed from the company records before this plan goes to a "
           "funder. Development-finance funders will also ask for the items listed in Appendix E.")

    d.h2("Mission, vision and promise")
    d.para("**Mission.** Give every African small business a marketing team and a shop, inside the chat app "
           "its customers already use.")
    d.para("**Vision.** A braider in Tembisa, a baker in Lagos and an agency in Nairobi market and sell as "
           "easily as any global brand, in their own language and their own currency.")
    d.para("**Promise.** Less admin, more sales you can see.")
    d.note("Mission, vision and promise are drafts from the brand kit and need founder sign-off before "
           "external use. [[FOUNDER SIGN-OFF ON MISSION, VISION AND PROMISE]]")

    d.h2("Platform verification and regulatory status")
    d.table(["Area", "Status"], [
        ("Meta Business and Access Verification", "Verified Meta Tech Provider (Sept 2026)"),
        ("WhatsApp Business", "Live: number connection, profile, templates, quick replies, broadcast to "
                              "consented contacts"),
        ("TikTok", "Video posting approved"),
        ("Facebook Pages and Instagram auto-publishing",
         "Being switched on: Meta permissions not yet approved. Never sold as live"),
        ("Instagram DMs and comments, X posting", "Not available"),
        ("Payment licensing",
         "FluxMuse is not a payment institution and does not hold merchants' money. Paystack is live in South "
         "Africa; Yoco and Ozow run FluxMuse's own subscription billing; pawaPay and Fincra are contracted, "
         "accounts pending"),
        ("Data protection",
         "Built to be POPIA ready: row-level security on every table, encrypted tokens, data export and account "
         "deletion. Information Officer: [[INFORMATION OFFICER NAME AND EMAIL]]"),
        ("VAT", "Not VAT-registered. Prices are the amounts charged; no VAT is added"),
        ("Intellectual property",
         "Platform code, brand and the Muse icon owned by Fluxmuse (Pty) Ltd. Trade mark registration: "
         "[[TRADE MARK STATUS]]"),
    ], [5.2, 11.8], "Verification and regulatory status", size=9)
    d.note("Features waiting on Meta stay switched off until Meta approves them, and are never sold as live. "
           "This is the biggest platform dependency in the plan (section 14).")


def s3_problem(d):
    d.h1("3. Problem and opportunity", new_page=True)
    d.h2("The problem")
    d.para("A small business in Johannesburg, Lagos or Nairobi sells through WhatsApp, Instagram and Facebook. "
           "Marketing is a person, usually the owner, doing it late at night between jobs. The tools that exist "
           "were built for somewhere else:")
    d.bullets([
        "**A patchwork of disconnected tools** for posts, chats, email, SMS and payments.",
        "**Agency retainers priced beyond most small-business budgets.**",
        "**No shop page**, so the catalogue is a photo album and orders get lost in chats.",
        "**After-hours messages go unanswered**, and the sale goes cold.",
        "**Content in the wrong language and register** for the customer being sold to.",
    ])
    d.figure("infographics/problem-solution.png",
             "The problem we solve, and what replaces it.",
             "Comparison: today, a stack of disconnected tools, agency retainers, no shop page and unanswered "
             "after-hours messages; with FluxMuse, an AI marketing team that lives in WhatsApp, paid plans from "
             "R149 a month priced in rands, a catalogue and shop link from product photos, and an assistant "
             "that answers in the customer's language.")

    d.h2("Why now")
    d.bullets([
        "**The channel is settled.** WhatsApp is where African small businesses already sell, and the WhatsApp "
        "Cloud API makes a shop around the chat possible for small businesses, not only enterprises.",
        "**AI has made the marketing team affordable.** Captions, images, short video and catalogue entries "
        f"can now be produced at a price a {rand(ZAR['Nano'])}-a-month business can pay.",
        "**The gate is verification, not code.** Meta Tech Provider verification takes months, and FluxMuse "
        "already holds it.",
        "**Payments are reaching across the continent** through aggregators. FluxMuse has contracts in place "
        "for expansion; the accounts are pending.",
    ])

    d.h2("The gap in the market")
    d.para("Global social-media tools publish but don't sell. WhatsApp chatbot vendors handle conversations but "
           "don't create marketing. E-commerce platforms sell on a website, not around a chat. Local agencies "
           "charge retainers most of this market cannot pay. **Nobody covers photos → catalogue → shop link → "
           "posts → orders on WhatsApp in one product, priced in rands.** Section 7 sets this out.")


def s4_solution(d):
    d.h1("4. Solution: products and services", new_page=True)
    d.para("FluxMuse is one product that runs a marketing loop and takes orders in the same place: WhatsApp.")
    d.figure("infographics/how-fluxmuse-works.png",
             "The loop: Plan, Create, Publish, Sell, Learn.",
             "Circular diagram: Plan (Strategist) from your goals, products and the week ahead; Create "
             "(Creator) captions, images and short video clips in your customers' languages; Publish (Publisher) "
             "to WhatsApp Status, consented broadcasts and TikTok; Sell (WhatsApp shop) with a shop link from "
             "your photos and every order on WhatsApp; Learn (Analyst) what sold and what to post next.")

    d.h2("What it does today")
    d.table(["Capability", "What the owner does", "Status"], [
        ("WhatsApp Concierge", "Sends product photos; approves each catalogue entry with YES, NO or an edit",
         "Live, newly launched"),
        ("Hosted shop link", "Shares fluxmuse.ai/s/<name>; each order arrives as a WhatsApp message",
         "Live, newly launched"),
        ("Order alerts and SOLD", "Gets an alert per order; replies SOLD to mark it sold", "Live, newly launched"),
        ("AI captions and images (POST)", "Gets a caption and photo back, ready for WhatsApp Status",
         "Live, newly launched"),
        ("Short AI video clips, voice-note transcription", "Asks on WhatsApp", "Live, newly launched"),
        ("WhatsApp Business setup", "Number, profile, templates, quick replies, broadcasts to consented "
                                    "contacts", "Live, newly launched"),
        ("Answers in the customer's language", "Nothing: the assistant follows the customer",
         "Live, newly launched"),
        ("TikTok posting", "Video only", "Live (approved)"),
        ("Facebook Pages and Instagram auto-publishing", "Until approved, forwards to WhatsApp Status",
         "Being switched on"),
        ("Checkout through FluxMuse (Paystack, South Africa)", "Built; not yet tested with real money",
         "Being switched on"),
        ("AI Voice (inbound on Growth; inbound and outbound on Scale)", "Beta, evaluated together",
         "Being switched on"),
        ("Daily digest; click-to-WhatsApp ads (FluxLoop)", "Digest in dry run; ads on FluxMuse's own account "
                                                           "first", "Being switched on"),
        ("Shopify, WooCommerce and Takealot sync", "Exists in part; tenant catalogue sync is a gap",
         "Being switched on"),
        ("Instagram DMs and comments; X posting; checkout outside South Africa", "—", "Not available"),
    ], [5.6, 7.6, 3.8], "What is live, being switched on and not available", size=8.5)
    d.note("Source: CURRENT_OFFER.md §3. Live features are newly launched; no merchant has run them end to end, "
           "so the plan quotes no results.")

    d.h2("WhatsApp commerce")
    d.para("The buyer finds the business through a Status post, a QR code or a shop link, chats with the "
           "assistant, browses a shop built from the owner's photos and sends the order. The owner gets the "
           "order on WhatsApp and replies SOLD. A broadcast to consented contacts starts the next sale. Paid "
           "checkout through FluxMuse is built and being switched on; until it has been tested with real money, "
           "orders arrive as a WhatsApp message to the owner's own number.")
    d.figure("infographics/whatsapp-commerce-flow.png",
             "From first tap to repeat order, on WhatsApp. Checkout is being switched on.",
             "Flow: Discover, Chat, Catalog, Cart, Pay (Paystack, South Africa, being switched on), Order alert "
             "with reply SOLD, Come back through broadcasts to consented contacts.")

    d.h2("The platform")
    d.figure("infographics/platform-stack.png",
             "Live today, and being switched on. Solid chips are live; dashed chips are being switched on.",
             "Six rows: channels (WhatsApp Business, WhatsApp Status, TikTok video and consented broadcasts live; "
             "Facebook Pages and Instagram posts being switched on; Instagram DMs and X not available); AI team; "
             "shop and orders; growth; integrations (being switched on); and trust.")

    d.h2("The agency and white-label offering")
    d.para(f"Agencies buy the Agency tier ({rand(ZAR['Agency'])} list) at the partner wholesale price of "
           f"**{rand(PW['ZAR'])} a month** ({PW['discount_vs_agency_list_pct']}% off): white-label, multi-client, "
           "unlimited brands, 80 channels and bring-your-own-cloud. The partner sets its own retail price for its "
           "clients and keeps the difference. Wholesale does not stack with Founding Member.")
    d.figure("infographics/agency-partner-model.png",
             "The partner model. The worked example is illustrative, not a forecast.",
             "Diagram: FluxMuse bills the agency the partner price of R6,999 a month, 30% off the R9,999 Agency "
             "tier; the agency bills its clients at a retail price it sets. Illustrative example: 20 clients at "
             "R1,500 a month bills R30,000, less R6,999, leaves a gross spread of R23,001 a month before the "
             "partner's own costs.")
    d.note("Illustrative only. FluxMuse does not quote a fixed partner margin, because it depends on the "
           "partner's retail price and delivery costs.")

    d.h2("The lead guarantee")
    d.para("FluxMuse backs the offer with a **lead guarantee, paid in support, not cash**: 3 qualified leads in 30 days of "
           "go-live, counted as unique WhatsApp numbers that start a conversation through a FluxMuse-tracked "
           "entry point. If fewer than 3 arrive and the merchant held up their side (shared the link, posted at "
           "least weekly), FluxMuse extends support at no extra charge until 3 are reached.")

    d.h2("Trust and compliance")
    d.bullets([
        "Built to be **POPIA ready**, with row-level security on every database table, encrypted access tokens, "
        "and data export and account deletion on request.",
        "**WhatsApp policy**: broadcasts use Meta-approved message templates and go only to contacts who "
        "opted in, with a way to opt out.",
        "**Payments** are handled by licensed providers; FluxMuse does not hold merchants' money.",
    ])
