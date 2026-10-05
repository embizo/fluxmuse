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
        "[ ] Checkout through FluxMuse is being switched on: plan orders to arrive on WhatsApp and be paid the client's "
        "usual way. Facebook and Instagram auto-posting await Meta approval: plan manual posting.",
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
        "**Call to action:** \u201cChat to order\u201d via the FluxMuse shop link or QR code: fluxmuse.ai/s/[[NAME]]",
    ])
    d.h2("How FluxMuse runs the campaign")
    d.para("FluxMuse turns product photos into a shop link, writes captions and images for each post in each "
           "language, sends broadcasts to opted-in customers, and alerts you on WhatsApp for every order. We review "
           "what brought leads and adjust the next round.")
    d.figure("infographics/how-fluxmuse-works.png",
             "One loop: plan, create, publish, sell, learn. Some steps are being switched on (section 4).",
             "Loop diagram: plan, create, publish, sell and learn around FluxMuse.")

    # 3 ----------------------------------------------------------------------------------------
    d.h1("3. Audience and segments")
    d.table(["Segment", "Who", "Reached through", "Message", "Size"], [
        ("Opted-in WhatsApp customers", "Past buyers who opted in", "WhatsApp broadcast", "Early access [[ ]]", "[[N]]"),
        ("Lapsed buyers who opted in", "No order in [[90]] days", "WhatsApp broadcast", "Welcome-back offer", "[[N]]"),
        ("Status viewers", "People who see your WhatsApp Status", "Forwarded posts", "Launch and countdown", "[[N]]"),
        ("Social followers", "Facebook, Instagram and TikTok followers", "Posts (TikTok via FluxMuse; others by hand)", "Hero offer", "[[N]]"),
        ("New prospects", "[[AGE, AREA, INTERESTS]]", "Shop link and QR code", "Hero offer", "[[N]]"),
    ], [3.4, 3.8, 3.6, 3.8, 2.4], "Audience segments", size=9)
    d.para("WhatsApp broadcasts go only to people who opted in (POPIA), with an opt-out in every message.", size=9.5)

    # 4 ----------------------------------------------------------------------------------------
    d.h1("4. Channel plan")
    d.table(["Channel", "Role in the campaign", "Formats", "Status"], [
        ("WhatsApp broadcasts and templates", "Main channel: announce, remind", "Meta-approved templates", "Live (newly launched)"),
        ("Shop link and QR code", "Where buyers choose and order", "fluxmuse.ai/s/[[NAME]]", "Live (newly launched)"),
        ("Order alerts", "Every order on your WhatsApp; reply SOLD", "WhatsApp message", "Live (newly launched)"),
        ("WhatsApp Status", "Daily reach", "AI captions and images (POST)", "Live (newly launched)"),
        ("TikTok", "Video reach", "Short AI video clips", "Live (newly launched)"),
        ("Facebook Page and Instagram", "Reach", "Posts made by FluxMuse, posted by hand", "Auto-posting being switched on"),
        ("Checkout through FluxMuse", "Pay in the flow", "Paystack", "Being switched on"),
    ], [3.6, 4.8, 4.8, 3.8], "Channel plan", size=9)
    d.figure("infographics/omnichannel-hub.png",
             "Channels around one WhatsApp-first hub. Facebook and Instagram auto-posting are being switched on.",
             "Hub diagram with FluxMuse at the centre connected to the channels a business uses.")

    # 5 ----------------------------------------------------------------------------------------
    d.h1("5. Content calendar")
    d.para("Weeks relative to launch. Adjust to the campaign type (e.g. Black Friday peak = W3).", size=9.5)
    d.table(["Channel", "W-2 Prep", "W1 Tease", "W2 Launch", "W3 Peak", "W4 Last chance", "W+1 Thank you"], [
        ("WhatsApp", "Templates to Meta; opt-in drive", "\u201cComing soon\u201d to opted-in VIPs", "Launch broadcast + shop link", "Reminder", "Last-chance broadcast", "Thank-you"),
        ("WhatsApp Status", "Plan posts", "Teasers", "Launch post", "Daily posts", "Countdown", "Best-sellers"),
        ("TikTok", "Plan clips", "Teaser clip", "Launch clip", "2 clips", "Countdown clip", "Recap clip"),
        ("Facebook / Instagram*", "Grid plan", "Teasers (by hand)", "Launch (by hand)", "Posts (by hand)", "Stories (by hand)", "Recap (by hand)"),
        ("Shop link", "Products in", "Link shared", "Offer live", "Update stock", "Countdown", "Archive"),
    ], [2.6, 2.4, 2.4, 2.4, 2.4, 2.4, 2.4], "Content calendar by week and channel", size=8)
    d.para("*Facebook and Instagram auto-posting are waiting for Meta approval; FluxMuse makes the posts and you post "
           "them by hand until then. Every cell: [[CONTENT DETAIL]] to be confirmed before scheduling.", size=8.5, color=GREY)

    # 6 ----------------------------------------------------------------------------------------
    d.h1("6. WhatsApp commerce funnel")
    d.table(["Stage", "What happens", "FluxMuse feature", "KPI", "Target (goal)"], [
        ("1. Link or QR", "Buyer taps a post, Status or QR code", "Shop link, QR code", "Link visits", "[[N]]"),
        ("2. Shop", "Buyer browses products", "Hosted shop (Concierge catalogue)", "Qualified leads", "[[N]]"),
        ("3. Order", "Order arrives as a WhatsApp message", "Order alerts, SOLD", "Orders", "[[N]]"),
        ("4. Payment", "Paid the business's usual way", "Checkout through FluxMuse: being switched on", "Orders paid", "[[N]]"),
        ("5. Follow-up", "Offer to buyers who opted in", "Broadcasts", "Repeat orders", "[[N]]"),
    ], [2.8, 4.2, 4.0, 3.4, 2.6], "WhatsApp commerce funnel", size=9)
    d.figure("infographics/whatsapp-commerce-flow.png",
             "From first tap to an order on WhatsApp. Checkout through FluxMuse is being switched on.",
             "WhatsApp commerce flow from a shared link to an order alert on the merchant's WhatsApp.")

    # 7 ----------------------------------------------------------------------------------------
    d.h1("7. Timeline")
    weeks = ["W-3", "W-2", "W-1", "W1", "W2", "W3", "W4", "W+1", "W+2"]
    g = lambda spec: tuple(spec.get(w, "") for w in weeks)
    rows = [
        ("Brief sign-off and big idea",) + g({"W-3": "##"}),
        ("Plan, shop products and link",) + g({"W-3": "#", "W-2": "##"}),
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
        ("Starter", "R499/mo (Founding Member R349 for the first two monthly bills*)", "[[N]]", "[[R]]"),
        ("Growth (3 brands, 15 channels)", "R1,999/mo (Founding Member R1,399 for the first two monthly bills*)", "[[N]]", "[[R]]"),
        ("Scale (10 brands, 40 channels)", "R4,999/mo (Founding Member R3,499 for the first two monthly bills*)", "[[N]]", "[[R]]"),
    ], [5.0, 7.0, 2.4, 2.6], "Budget part A: FluxMuse plan", size=9, aligns=[None, None, "center", "right"])
    d.para("*" + C.FOUNDING_LINE + " Payment first; no trial. Delete the plans you don't recommend.",
           size=8.5, color=GREY)
    d.h2("B. Optional FluxMuse services")
    d.table(["Service", "Fee", "Include"], [
        ("Campaign set-up (shop products, templates, QR codes)", "[[TBC]]", "[ ] "),
        ("Creative review and design", "[[TBC]]", "[ ] "),
        ("Campaign management during live weeks", "[[TBC]]", "[ ] "),
        ("Post-campaign report and workshop", "[[TBC]]", "[ ] "),
    ], [10.5, 4.0, 2.5], "Budget part B: optional services", aligns=[None, None, "center"])
    d.h2("C. Third-party pass-through costs (not FluxMuse fees)")
    d.table(["Cost", "Paid to", "Estimate"], [
        ("Ad spend (Meta [[/ other]])", "Ad platform", "[[estimate R]]"),
        ("WhatsApp conversation and template message fees", "Meta", "[[estimate R]]"),
        ("Printing (QR flyers, in-store)", "Printer", "[[estimate R]]"),
    ], [8.0, 5.0, 4.0], "Budget part C: pass-through costs", aligns=[None, None, "right"])
    d.h2("Budget summary")
    d.table(["Part", "Amount"], [
        ("A. FluxMuse plan", "[[R]]"), ("B. Optional FluxMuse services", "[[R]]"),
        ("C. Pass-through costs (estimate)", "[[R]]"), ("Total campaign budget", "[[R]]"),
    ], [11.0, 6.0], "Budget summary", aligns=[None, "right"], total_rows=(3,))
    d.callout("Our lead guarantee", [C.GUARANTEE])

    # 9 ----------------------------------------------------------------------------------------
    d.h1("9. KPIs and targets")
    d.para("Targets are goals agreed before launch, not promised results.", bold=True)
    d.table(["KPI", "Baseline (last comparable period)", "Target (goal)", "Source"], [
        ("Shop link visits and QR scans", "[[ ]]", "[[ ]]", "Shop link"),
        ("Qualified leads", "[[ ]]", "[[ ]]", "FluxMuse tracking"),
        ("Orders alerted", "[[ ]]", "[[ ]]", "Order alerts"),
        ("Posts and clips made", "[[ ]]", "[[ ]]", "POST history"),
        ("Opted-in contacts", "[[ ]]", "[[ ]]", "Contact list"),
        ("Opt-outs (keep low)", "[[ ]]", "[[ ]]", "Broadcasts"),
    ], [5.4, 4.2, 3.4, 4.0], "Campaign KPI targets (goals)", size=9)

    # 10 ---------------------------------------------------------------------------------------
    d.h1("10. Reporting cadence")
    d.table(["When", "What", "Who"], [
        ("Daily during live weeks", "Check orders, leads and stock; quick fixes", C.SENDER),
        ("Weekly", "Short report and 20-minute call: KPIs vs targets, next week's changes", "Both teams"),
        ("Peak day", "Live monitoring and escalation line: [[PHONE / WHATSAPP]]", "[[NAMES]]"),
        ("W+2", "Final campaign report: results vs targets, learnings, next campaign", "Both teams"),
    ], [4.0, 9.4, 3.6], "Reporting cadence")

    # 11 ---------------------------------------------------------------------------------------
    d.h1("11. Approvals workflow")
    d.para("Nothing goes out without your sign-off.")
    d.table(["Step", "Who", "What happens", "Turnaround"], [
        ("1. Draft", "FluxMuse AI + " + C.SENDER, "Captions, images and broadcast drafts in each language", "[[N]] days"),
        ("2. Internal review", "[[FLUXMUSE REVIEWER]]", "Brand fit, facts, offer terms", "[[N]] day"),
        ("3. Client approval", f"[[APPROVER AT {CL}]]", "Approve or comment on WhatsApp", "[[N]] days"),
        ("4. Compliance check", "Both", "Opt-in lists, Meta template approval, promotion T&Cs", "Before scheduling"),
        ("5. Publish", "FluxMuse and client", "Broadcasts and TikTok via FluxMuse; other posts by hand", "Per calendar"),
        ("6. Live changes", "[[APPROVER]]", "Price or stock changes re-approved", "Same day"),
    ], [3.2, 4.2, 6.4, 3.2], "Approvals workflow", size=9)

    # 12 ---------------------------------------------------------------------------------------
    d.h1("12. Risks and mitigations")
    d.table(["Risk", "Likelihood", "Impact", "Mitigation", "Owner"], [
        ("Meta rejects a WhatsApp template", "[[L/M/H]]", "Launch delay", "Submit templates in W-2 with backups", "FluxMuse"),
        ("Meta auto-posting not approved in time", "[[L/M/H]]", "More manual work", "Post Facebook and Instagram by hand; lean on WhatsApp and TikTok", "Client"),
        ("Small opted-in contact list", "[[L/M/H]]", "Low broadcast reach", "Opt-in drive with QR, link and in-store prompts from W-2", "Both"),
        ("Stock runs out", "[[L/M/H]]", "Unhappy buyers", "Mark items SOLD; stock limits in copy", "Client"),
        ("Message fatigue and opt-outs", "[[L/M/H]]", "List shrinks", "Frequency cap of [[N]] broadcasts a week; segment offers", "FluxMuse"),
        ("Payment or connectivity outages", "[[L/M/H]]", "Lost orders", "Orders kept on WhatsApp; confirm later", "Both"),
        ("Ad costs spike near peak", "[[L/M/H]]", "Budget overrun", "Cap daily spend; shift to owned channels", "Client"),
        ("POPIA complaint", "[[L/M/H]]", "Reputational", "Opted-in lists only; opt-outs honoured", "Both"),
    ], [3.8, 2.0, 2.4, 6.2, 2.6], "Risks and mitigations", size=8.5)

    # 13 ---------------------------------------------------------------------------------------
    d.h1("13. Data protection and compliance")
    C.popia_clause(d, heading=False)
    d.bullets(["Promotions follow [[CLIENT NAME]]'s competition and promotion T&Cs [[LINK]] and the Consumer Protection "
               "Act. [[LEGAL REVIEW REQUIRED]]"])
    C.terms(d, 14, short=True)
    C.acceptance(d, 15, [
        "Campaign plan as described, launching [[DATE]]",
        "FluxMuse plan: [[Starter / Growth / Scale]], [[monthly / annual]]",
        "Optional services: [[LIST]]",
        "Pass-through budget estimate of [[R]] noted (paid to providers)",
    ], terms_num=14)
    d.save(out_path, "FluxMuse proposal: Brand campaign", "Campaign proposal template")
    return d
