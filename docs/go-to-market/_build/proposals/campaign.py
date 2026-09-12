"""Template 4: brand campaign proposal (festive, Black Friday, back-to-school, launch...)."""
from fmdoc import FMDoc, GREY
import common as C

CL = "[[CLIENT NAME]]"


def build_campaign(out_path):
    d = FMDoc()
    d.cover("Campaign proposal · [[CAMPAIGN TYPE]]", "[[CAMPAIGN NAME]]: a WhatsApp-first campaign",
            f"For {CL} · [[CAMPAIGN START DATE]] to [[CAMPAIGN END DATE]]")
    C.how_to_use(d, "Brand campaign proposal template", extra=[
        "[ ] Campaign type selector: tick one type in section 1 and set [[CAMPAIGN TYPE]] everywhere (Festive season, "
        "Black Friday / Cyber Monday, Back-to-school, Product launch, or Other). Delete the notes for the other types.",
        "[ ] Keep FluxMuse fees, optional services and pass-through costs (ad spend, Meta message fees) in their "
        "separate budget tables. Never blend them into one FluxMuse price.",
        "[ ] Checkout inside WhatsApp needs Growth or Scale. Plan Instagram as manual posting until Meta approves it.",
    ])
    d.toc()
    d.page_break()

    # 1 ----------------------------------------------------------------------------------------
    d.h1("1. Campaign brief recap")
    d.para("Campaign type (tick one):", bold=True, keep=True)
    d.checklist([
        "Festive season (November to December): gifting, end-of-year specials, delivery cut-off dates",
        "Black Friday / Cyber Monday (late November): time-boxed deals, stock limits, high message volume",
        "Back-to-school (January): uniforms, stationery, services; payday timing matters",
        "Product launch: waitlist, teaser, launch day, early-bird offer",
        "Other: [[CAMPAIGN TYPE]]",
    ])
    d.table(["Brief item", "What we understood"], [
        ("Business goal", "[[e.g. sell out festive gift boxes; grow repeat orders]]"),
        ("Products and offer", "[[PRODUCTS]] · [[OFFER MECHANIC, e.g. 20% off, bundle, free delivery]]"),
        ("Campaign dates", "[[START]] to [[END]], with peak on [[PEAK DATE]]"),
        ("Areas and languages", "[[e.g. Gauteng; English, isiZulu, Sesotho]]"),
        ("Budget range", "FluxMuse plan + [[R]] optional services + [[R]] pass-through (section 8)"),
        ("Mandatories", "[[e.g. brand guidelines, legal copy, T&Cs of promotion, stock limits]]"),
        ("Success looks like", "[[ONE SENTENCE]]"),
    ], [4.4, 12.6], "Campaign brief recap")

    # 2 ----------------------------------------------------------------------------------------
    d.h1("2. The big idea")
    d.callout("[[BIG IDEA IN ONE LINE]]", [
        "**Key message:** [[WHAT WE WANT CUSTOMERS TO FEEL AND DO]]",
        "**Why it works for [[CLIENT NAME]]:** [[INSIGHT ABOUT THE AUDIENCE OR SEASON]]",
        "**Hook lines:** English: [[ ]] · isiZulu: [[ ]] · Sesotho: [[ ]] · Afrikaans: [[ ]]",
        "**Call to action:** “Chat to order” via WhatsApp short link or QR code: [[wa.me LINK]]",
    ])
    d.h2("How FluxMuse runs the campaign")
    d.para("The Strategist sets goals, channel mix and budget; the Creator writes copy and images in each language; the "
           "Publisher schedules posts and broadcasts; buyers order and pay in WhatsApp; the Analyst feeds results back "
           "into the next round of content.")
    d.figure("infographics/how-fluxmuse-works.png",
             "One loop run by your AI marketing team: plan, create, publish, sell, learn.",
             "Loop diagram: Plan (Strategist), Create (Creator), Publish (Publisher), Sell (WhatsApp commerce) and "
             "Learn (Analyst) around a central AI marketing team.")

    # 3 ----------------------------------------------------------------------------------------
    d.h1("3. Audience and segments")
    d.table(["Segment", "Who", "Reached through", "Message", "Size"], [
        ("Opted-in WhatsApp customers", "Past buyers who opted in", "WhatsApp broadcast", "Early access [[ ]]", "[[N]]"),
        ("Lapsed buyers", "No order in [[90]] days (churn-risk score)", "WhatsApp, SMS, email", "Welcome-back offer", "[[N]]"),
        ("Loyalty members / VIPs", "Top customers by spend", "WhatsApp", "VIP preview", "[[N]]"),
        ("Social followers", "Facebook Page followers", "Posts, Messenger", "Launch and countdown", "[[N]]"),
        ("New prospects", "[[AGE, AREA, INTERESTS]]", "Paid ads to WhatsApp", "Hero offer", "[[N]]"),
        ("Abandoned carts", "Started checkout, didn't pay", "Automatic recovery message", "Reminder + [[INCENTIVE]]", "Live"),
    ], [3.4, 3.8, 3.6, 3.8, 2.4], "Audience segments", size=9)
    d.para("Segments come from FluxMuse customer segmentation, lead scoring and churn-risk scoring. WhatsApp, SMS and "
           "email broadcasts go only to people who opted in (POPIA).", size=9.5)

    # 4 ----------------------------------------------------------------------------------------
    d.h1("4. Channel plan")
    d.table(["Channel", "Role in the campaign", "Formats", "Status"], [
        ("WhatsApp broadcasts and templates", "Main sales channel: announce, remind, recover", "Meta-approved templates, catalog messages", "Live"),
        ("WhatsApp chatbot and Flows", "Answer questions, take orders 24/7", "FAQ bot, order flow, checkout", "Live (checkout on Growth)"),
        ("Facebook Page", "Reach and social proof", "Posts, countdowns, carousels", "Live"),
        ("Instagram", "Visual reach", "Posts, reels, stories", "Pending Meta approval: post manually"),
        ("Email", "Detail and gifting guides", "Sequence of [[N]] emails", "Live"),
        ("SMS", "Short reminders and deadlines", "Last-chance SMS", "Live"),
        ("USSD", "Reach feature-phone customers", "Menu: offer, store locator, [[ ]]", "Live (Growth)"),
        ("Link-in-bio", "One link for all offers", "Link page with WhatsApp CTA", "Live"),
        ("Landing page", "Campaign hub, T&Cs, QR to WhatsApp", "FluxMuse landing page builder", "Live"),
    ], [3.6, 4.8, 4.8, 3.8], "Channel plan", size=9)
    d.figure("infographics/omnichannel-hub.png",
             "Every channel your buyers use, one AI team. Instagram is pending Meta approval and not live yet.",
             "Hub diagram: FluxMuse AI team at the centre connected to WhatsApp, Facebook Pages, Messenger, email, "
             "SMS, USSD, website chat widget, link-in-bio and landing pages, with Instagram dashed as in Meta review.")

    # 5 ----------------------------------------------------------------------------------------
    d.h1("5. Content calendar")
    d.para("Weeks relative to launch. Adjust to the campaign type (e.g. Black Friday peak = W3).", size=9.5)
    d.table(["Channel", "W-2 Prep", "W1 Tease", "W2 Launch", "W3 Peak", "W4 Last chance", "W+1 Thank you"], [
        ("WhatsApp", "Templates to Meta; opt-in drive", "“Coming soon” to VIPs", "Launch broadcast + catalog", "Reminder + bundles", "Last-chance broadcast", "Thank-you + review ask"),
        ("Facebook Page", "Page refresh", "2 teaser posts", "Launch post + pinned", "3 posts + countdown", "Final countdown", "Best-sellers recap"),
        ("Instagram*", "Grid plan", "Teasers (manual)", "Launch (manual)", "Reels (manual)", "Stories (manual)", "Recap (manual)"),
        ("Email", "List clean-up", "Save-the-date", "Launch email", "Gift guide", "Last chance", "Thank you"),
        ("SMS / USSD", "USSD menu set", "–", "Launch SMS", "–", "Deadline SMS", "–"),
        ("Landing page / link-in-bio", "Build page", "Waitlist live", "Offer live", "Update stock", "Countdown", "Archive"),
    ], [2.6, 2.4, 2.4, 2.4, 2.4, 2.4, 2.4], "Content calendar by week and channel", size=8)
    d.para("*Instagram is pending Meta approval; plan manual posting until it is live in FluxMuse. Every cell: "
           "[[CONTENT DETAIL]] to be confirmed in the approvals workflow.", size=8.5, color=GREY)

    # 6 ----------------------------------------------------------------------------------------
    d.h1("6. WhatsApp commerce funnel")
    d.table(["Stage", "What happens", "FluxMuse feature", "KPI", "Target (goal)"], [
        ("1. Short link or QR", "Buyer taps an ad, post or QR code", "wa.me short links, QR codes", "Link clicks", "[[N]]"),
        ("2. Chatbot", "Greets, answers questions, shows offers", "Chatbot, WhatsApp Flows", "Conversations started", "[[N]]"),
        ("3. Catalog", "Buyer browses products in chat", "WhatsApp catalog", "Catalog views", "[[N]]"),
        ("4. Checkout", "Cart and payment inside WhatsApp", "Cart checkout; Yoco, Ozow, Paystack", "Chat-to-order conversion", "[[e.g. 5%]]"),
        ("5. Confirmation", "Order confirmed, status updates", "Orders and notifications", "Orders · GMV (R)", "[[N]] · [[R]]"),
        ("6. Recovery", "Reminder if the cart isn't paid", "Abandoned-cart recovery", "Carts recovered", "[[e.g. 10%]]"),
        ("7. Retarget", "Follow-up offer to buyers and browsers", "Segments, broadcasts, loyalty", "Repeat orders", "[[N]]"),
    ], [2.8, 4.2, 4.0, 3.4, 2.6], "WhatsApp commerce funnel", size=9)
    d.figure("infographics/whatsapp-commerce-flow.png",
             "From first tap to repeat order inside WhatsApp. Catalog and checkout in chat are on Growth and Scale.",
             "WhatsApp commerce flow: discover, chat, catalog, cart, pay with local rails, confirmed and loyalty, with "
             "abandoned-cart recovery and retargeting loops.")

    # 7 ----------------------------------------------------------------------------------------
    d.h1("7. Timeline")
    weeks = ["W-3", "W-2", "W-1", "W1", "W2", "W3", "W4", "W+1", "W+2"]
    g = lambda spec: tuple(spec.get(w, "") for w in weeks)
    rows = [
        ("Brief sign-off and big idea",) + g({"W-3": "##"}),
        ("Plan upgrade, catalog and payments",) + g({"W-3": "#", "W-2": "##"}),
        ("WhatsApp templates to Meta for approval",) + g({"W-2": "##", "W-1": "#"}),
        ("Content production and approvals",) + g({"W-2": "#", "W-1": "##", "W1": "#"}),
        ("Opt-in drive (QR, link, in-store)",) + g({"W-2": "#", "W-1": "#", "W1": "#"}),
        ("Campaign live",) + g({"W1": "##", "W2": "##", "W3": "##", "W4": "##"}),
        ("Daily monitoring and optimisation",) + g({"W1": "#", "W2": "#", "W3": "#", "W4": "#"}),
        ("Post-campaign follow-up",) + g({"W+1": "##"}),
        ("Final report",) + g({"W+2": "##"}),
    ]
    d.table(["Activity"] + weeks, rows, [6.2] + [1.2] * 9, "Campaign timeline (Gantt)", size=8.5, gantt=True,
            zebra=False, aligns=[None] + ["center"] * 9)
    d.para("● dark = main activity, ● light = supporting activity. Launch date (W1): [[DATE]].", size=8.5, color=GREY)

    # 8 ----------------------------------------------------------------------------------------
    d.h1("8. Budget")
    d.para("Three separate parts. Only part A and any part B services you choose are FluxMuse charges.")
    d.h2("A. FluxMuse plan")
    d.table(["Plan", "Price", "Campaign months", "Subtotal"], [
        ("Growth (needed for WhatsApp checkout)", "R1,999/mo (Founding Member R1,399 for the first 2 monthly bills*)", "[[N]]", "[[R]]"),
        ("Scale (multi-brand, API, priority support)", "R4,999/mo (Founding Member R3,499 for the first 2 monthly bills*)", "[[N]]", "[[R]]"),
    ], [5.0, 7.0, 2.4, 2.6], "Budget part A: FluxMuse plan", size=9, aligns=[None, None, "center", "right"])
    d.para("*South African sign-ups from 1 December 2026 to 31 January 2027 only. Delete the plan you don't recommend.",
           size=8.5, color=GREY)
    d.h2("B. Optional FluxMuse services")
    d.table(["Service", "Fee", "Include"], [
        ("Campaign set-up (catalog, flows, templates, landing page)", "[[TBC]]", "[ ] "),
        ("Creative review and design", "[[TBC]]", "[ ] "),
        ("Campaign management during live weeks", "[[TBC]]", "[ ] "),
        ("Post-campaign report and workshop", "[[TBC]]", "[ ] "),
    ], [10.5, 4.0, 2.5], "Budget part B: optional services", aligns=[None, None, "center"])
    d.h2("C. Third-party pass-through costs (not FluxMuse fees)")
    d.table(["Cost", "Paid to", "Estimate"], [
        ("Ad spend (Meta [[/ other]])", "Ad platform", "[[estimate R]]"),
        ("WhatsApp conversation and template message fees", "Meta", "[[estimate R]]"),
        ("SMS sending", "SMS provider", "[[estimate R]]"),
        ("Payment processing fees", "Yoco / Ozow / Paystack", "[[provider rates]]"),
        ("Printing (QR flyers, in-store)", "Printer", "[[estimate R]]"),
    ], [8.0, 5.0, 4.0], "Budget part C: pass-through costs", aligns=[None, None, "right"])
    d.h2("Budget summary")
    d.table(["Part", "Amount (excl. VAT)"], [
        ("A. FluxMuse plan", "[[R]]"), ("B. Optional FluxMuse services", "[[R]]"),
        ("C. Pass-through costs (estimate)", "[[R]]"), ("Total campaign budget", "[[R]]"),
    ], [11.0, 6.0], "Budget summary", aligns=[None, "right"], total_rows=(3,))
    d.para("Campaign Financing (instalment plans for campaign spend) may be available: [[CONFIRM ELIGIBILITY]].", size=9.5)

    # 9 ----------------------------------------------------------------------------------------
    d.h1("9. KPIs and targets")
    d.para("Targets are goals agreed before launch, not promised results.", bold=True)
    d.table(["KPI", "Baseline (last comparable period)", "Target (goal)", "Source"], [
        ("Reach and impressions", "[[ ]]", "[[ ]]", "Social metrics, ads"),
        ("Short-link clicks and QR scans", "[[ ]]", "[[ ]]", "Short links"),
        ("WhatsApp conversations started", "[[ ]]", "[[ ]]", "Inbox"),
        ("Chat-to-order conversion", "[[ ]]", "[[ ]]", "Orders"),
        ("Orders and GMV (R)", "[[ ]]", "[[ ]]", "Orders"),
        ("Average order value (R)", "[[ ]]", "[[ ]]", "Orders"),
        ("Abandoned carts recovered", "[[ ]]", "[[ ]]", "Recovery report"),
        ("Median first-reply time", "[[ ]]", "[[ ]]", "Inbox"),
        ("Cost per conversation (R)", "[[ ]]", "[[ ]]", "Ads + Meta fees"),
        ("Return on ad spend", "[[ ]]", "[[ ]]", "Ads + orders"),
        ("Opt-outs (keep low)", "[[ ]]", "[[ ]]", "Broadcasts"),
    ], [5.4, 4.2, 3.4, 4.0], "Campaign KPI targets (goals)", size=9)

    # 10 ---------------------------------------------------------------------------------------
    d.h1("10. Reporting cadence")
    d.table(["When", "What", "Who"], [
        ("Daily during live weeks", "Dashboard check: orders, conversations, spend, stock; quick fixes", "[[FLUXMUSE LEAD]]"),
        ("Weekly", "Short report and 20-minute call: KPIs vs targets, next week's changes", "Both teams"),
        ("Peak day", "Live monitoring and escalation line: [[PHONE / WHATSAPP]]", "[[NAMES]]"),
        ("W+2", "Final campaign report: results vs targets, learnings, next campaign", "Both teams"),
    ], [4.0, 9.4, 3.6], "Reporting cadence")

    # 11 ---------------------------------------------------------------------------------------
    d.h1("11. Approvals workflow")
    d.para("FluxMuse campaigns support approvals, so nothing goes live without sign-off.")
    d.table(["Step", "Who", "What happens", "Turnaround"], [
        ("1. Draft", "Creator agent + [[FLUXMUSE LEAD]]", "Copy, images and broadcast drafts in each language", "[[N]] days"),
        ("2. Internal review", "[[FLUXMUSE REVIEWER]]", "Brand fit, facts, offer terms", "[[N]] day"),
        ("3. Client approval", f"[[APPROVER AT {CL}]]", "Approve or comment in FluxMuse", "[[N]] days"),
        ("4. Compliance check", "Both", "Opt-in lists, Meta template approval, promotion T&Cs", "Before scheduling"),
        ("5. Schedule and publish", "Publisher agent", "Scheduled by channel and time", "Automatic"),
        ("6. Live changes", "[[APPROVER]]", "Price or stock changes re-approved", "Same day"),
    ], [3.2, 4.2, 6.4, 3.2], "Approvals workflow", size=9)

    # 12 ---------------------------------------------------------------------------------------
    d.h1("12. Risks and mitigations")
    d.table(["Risk", "Likelihood", "Impact", "Mitigation", "Owner"], [
        ("Meta rejects a WhatsApp template", "[[L/M/H]]", "Launch delay", "Submit templates in W-2 with backups", "FluxMuse"),
        ("Instagram not approved in time", "[[L/M/H]]", "Less reach", "Manual Instagram posting; lean on WhatsApp and Facebook", "Client"),
        ("Small opted-in contact list", "[[L/M/H]]", "Low broadcast reach", "Opt-in drive with QR, link and in-store prompts from W-2", "Both"),
        ("Stock runs out", "[[L/M/H]]", "Unhappy buyers", "Catalog synced with store; stock limits in copy", "Client"),
        ("Message fatigue and opt-outs", "[[L/M/H]]", "List shrinks", "Frequency cap of [[N]] broadcasts a week; segment offers", "FluxMuse"),
        ("Payment or connectivity outages", "[[L/M/H]]", "Lost orders", "Several payment options; cart recovery; confirm orders later", "Both"),
        ("Ad costs spike near peak", "[[L/M/H]]", "Budget overrun", "Cap daily spend; shift to owned channels", "Client"),
        ("POPIA complaint", "[[L/M/H]]", "Reputational", "Opted-in lists only; suppression and opt-outs honoured", "Both"),
    ], [3.8, 2.0, 2.4, 6.2, 2.6], "Risks and mitigations", size=8.5)

    # 13 ---------------------------------------------------------------------------------------
    d.h1("13. Data protection and compliance")
    C.popia_clause(d, heading=False)
    d.bullets(["Promotions follow [[CLIENT NAME]]'s competition and promotion T&Cs [[LINK]] and the Consumer Protection "
               "Act. [[LEGAL REVIEW REQUIRED]]"])
    C.terms(d, 14, short=True)
    C.acceptance(d, 15, [
        "Campaign plan as described, launching [[DATE]]",
        "FluxMuse plan: [[Growth / Scale]], [[monthly / annual]]",
        "Optional services: [[LIST]]",
        "Pass-through budget estimate of [[R]] noted (paid to providers)",
    ], terms_num=14)
    d.save(out_path, "FluxMuse proposal: Brand campaign", "Campaign proposal template")
    return d
