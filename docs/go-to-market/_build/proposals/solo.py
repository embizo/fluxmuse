"""Template 1 (Solo entrepreneur) and template 5 (pre-filled braiding & hair studio sample)."""
from fmdoc import FMDoc, DEEP, TINT, GREY
import common as C


def build_solo(out_path, sample=False):
    S = sample
    client = "[[BRAND NAME]]" if S else "[[CLIENT NAME]]"
    first = "[[OWNER]]" if S else "[[FIRST NAME]]"
    d = FMDoc(sample=S, client_ph=client)

    d.cover("Proposal · Solo entrepreneur" if not S else "Sample proposal · Braiding & hair studio",
            "Your AI marketing team, selling inside WhatsApp" if not S
            else "More bookings, fewer no-shows, all inside WhatsApp",
            f"A FluxMuse plan for {client}" if not S else f"A FluxMuse plan for {client}, [[AREA]], Gauteng")

    extra = []
    if S:
        extra.append("[ ] This sample shows the tone and detail we want. Copy wording into the Solo template; don't send "
                     "the sample itself. Delete the SAMPLE banner and header label if you adapt this file.")
    C.how_to_use(d, "Solo entrepreneur proposal (sample, pre-filled)" if S else "Solo entrepreneur proposal template",
                 extra=extra)

    # 1. Letter -------------------------------------------------------------------------------
    d.h1(f"1. Hi {first}")
    if S:
        d.para(f"Thank you for showing us around {client} in [[AREA]]. Your work speaks for itself: clients book "
               "because they've seen your braids on WhatsApp status, Facebook and word of mouth. What's holding you "
               "back isn't talent, it's the admin: answering the same questions all day, chasing deposits, and "
               "clients who don't pitch after you've blocked out four hours for knotless braids.")
        d.para("FluxMuse gives you an AI marketing team that replies to booking questions straight away (even at "
               "10pm), sends reminders so fewer people forget, collects a deposit before the chair is booked, and "
               "turns your before/after photos into posts in isiZulu, Sesotho and English.")
    else:
        d.para(f"Thank you for telling us about {client}. You said you want [[THEIR MAIN GOAL, e.g. more orders "
               "without living on your phone]]. You're already doing the hard part: people know your work and message "
               "you on WhatsApp. FluxMuse helps you reply faster, post more often and get paid inside the chat, "
               "without hiring a marketer.")
    d.para("This proposal is short on purpose: what we heard, what FluxMuse will set up, your first 60 days, the plan "
           "we recommend and how we'll both know it's working. You can start with the 14-day free trial, no card "
           "required.")
    d.para("Warm regards,", after=0)
    d.para("[[NAME]], [[TITLE]], FluxMuse · [[PHONE / WHATSAPP]]")

    # 2. What we heard ------------------------------------------------------------------------
    d.h1("2. What we heard", new_page=False)
    d.para("Tick what applies. " if not S else "From our first conversation (ticked items came up):", keep=True)
    if S:
        d.checklist([
            ("Booking requests get lost in busy WhatsApp chats, and messages after hours only get answered the next day", True),
            ("Clients book and don't arrive; there's no deposit, so a no-show costs a whole afternoon", True),
            ("Payment is cash or an EFT screenshot that has to be checked by hand", True),
            ("Posting happens when there's a gap between clients, so weeks go by with nothing new", True),
            ("Regulars aren't reminded when it's time to redo their hair, so repeat visits depend on memory", True),
            ("Customers speak isiZulu, Sesotho and English, and captions are usually English only", True),
            ("Braiding hair, extensions and aftercare products are sold only when someone asks", False),
            ("In [[OWNER]]'s words: “[[OWNER'S WORDS FROM THE VISIT]]”", False),
        ])
    else:
        d.checklist([
            "I miss messages and lose sales in busy WhatsApp chats, especially after hours",
            "I don't have time or budget for a marketer, so I post when I can",
            "Buyers drop off when I send them to a payment link or ask for proof of payment",
            "I take cash or EFT screenshots and chase people to pay",
            "Customers don't come back as often as I'd like, and I don't follow up",
            "I want to post in more than one language: [[LANGUAGES]]",
            "In your words: “[[QUOTE FROM THE DISCOVERY CALL]]”",
        ])
    d.figure("infographics/segment-solo.png",
             "Solo entrepreneurs: today vs with FluxMuse. Founding Member pricing applies to South African sign-ups "
             "from 1 December 2026 to 31 January 2027.",
             "Segment card for solo entrepreneurs: three problems (inconsistent posting, sales lost in WhatsApp DMs, "
             "payment-link drop-off) matched to FluxMuse answers, with Starter at R499 a month and the Founding Member "
             "price of R349 a month for the first 2 months.", width_cm=16)

    # 3. What FluxMuse will do ------------------------------------------------------------------
    d.h1("3. What FluxMuse will do for you")
    d.h2("Your AI marketing team")
    if S:
        rows = [
            ("Strategist", "Plans a simple monthly calendar around your busy days: month-end, school holidays, "
                           "December, and a small budget if you boost posts."),
            ("Creator", "Turns your before/after photos into posts and captions in isiZulu, Sesotho and English, "
                        "with style names and prices."),
            ("Publisher", "Schedules posts to your Facebook Page and link-in-bio page, and sends booking reminders "
                          "and rebooking nudges on WhatsApp."),
            ("Analyst", "Shows which styles and posts bring bookings, your no-show rate, and who is due for a "
                        "rebook."),
        ]
    else:
        rows = [
            ("Strategist", "Turns your goal into a simple plan: what to post, when, where, and how to spend a small budget."),
            ("Creator", "Writes posts and captions in [[LANGUAGES]] (isiZulu, Afrikaans, English and more) and makes "
                        "images for them."),
            ("Publisher", "Schedules posts to your Facebook Page and sends WhatsApp broadcasts to customers who opted in."),
            ("Analyst", "Shows which posts bring chats and which chats become sales, and learns from it."),
        ]
    d.table(["Agent", f"What it does for {client}"], rows, [3.4, 13.6], "AI marketing team roles")

    d.h2("Selling on WhatsApp")
    if S:
        d.bullets([
            "Your WhatsApp Business number connected through Meta's Embedded Signup (WhatsApp Cloud API).",
            "A booking chatbot with your hours, price list and styles menu (knotless, box braids, cornrows, "
            "[[STYLES]]), which asks for the date, time and style and books the slot.",
            "A deposit of [[R AMOUNT]] per booking, paid by Yoco card or Ozow instant EFT, so the slot is only held "
            "once the deposit is in.",
            "Automatic reminders 24 hours and 2 hours before the appointment, plus a rebooking nudge after "
            "[[N]] weeks.",
            "A wa.me short link and QR code for the salon mirror, flyers and your bio.",
        ])
    else:
        d.bullets([
            "Your WhatsApp Business number connected through Meta's Embedded Signup (WhatsApp Cloud API).",
            "A chatbot that greets people, answers questions (prices, hours, delivery) and captures orders or "
            "bookings, even after hours.",
            "A wa.me short link and QR code for your bio, flyers and counter, plus a website chat widget and "
            "link-in-bio page.",
            "**On Growth:** a WhatsApp catalog, cart and checkout inside the chat, order status updates and "
            "abandoned-cart recovery.",
        ])
    d.callout("Good to know", [
        "**WhatsApp checkout needs the Growth plan (R1,999/mo).** Starter gives you the AI team, chatbot and scheduled "
        "content. When you want customers to browse a catalog and pay without leaving WhatsApp, move to Growth."
        + (" For the studio, that's the moment to sell braiding hair and aftercare products in the chat." if S else ""),
        "Instagram publishing, comments and DMs are pending Meta approval and not live yet. We'll connect Instagram "
        "once Meta approves it.",
    ])
    if S:
        d.figure("infographics/whatsapp-commerce-flow.png",
                 "From first tap to repeat booking inside WhatsApp. Catalog and in-chat checkout are on the Growth plan.",
                 "WhatsApp commerce flow: discover, chat, catalog, cart, pay with local rails, confirmed, loyalty, "
                 "with abandoned-cart recovery and retargeting loops.")
    else:
        d.figure("screenshots/composites/checkout-in-chat-3-phones.png",
                 "Checkout inside the chat (Growth plan): browse, review the cart, pay locally. Demo store at "
                 "fluxmuse.ai/demo; demo data, not a real business.",
                 "Three phones showing the FluxMuse demo store in WhatsApp: a product catalog, a cart with a checkout "
                 "button, and a payment-received confirmation.", width_cm=16)

    # 4. First 60 days --------------------------------------------------------------------------
    d.h1("4. Your first 60 days")
    d.para("Weeks 1 and 2 fall inside your 14-day free trial. Each week needs about [[N]] minutes of your time.")
    if S:
        rows = [
            ("Week 1", "WhatsApp Business number and greeting; booking chatbot with hours, prices and styles menu",
             "Send your price list, style names and 10 favourite photos"),
            ("Week 2", "Deposit link via [[Yoco / Ozow]]; reminders 24h and 2h before; Facebook Page and link-in-bio "
                       "connected", "Set the deposit amount; approve reminder wording"),
            ("Week 3", "wa.me link and QR code for the mirror and flyers; first 2 weeks of before/after posts in "
                       "isiZulu, Sesotho and English", "Approve posts; print the QR code"),
            ("Week 4", "Baseline check: bookings, no-shows, deposits, reply time, posts. Agree targets together",
             "15-minute review call"),
            ("Week 5", "Broadcast to opted-in regulars: [[OFFER, e.g. mid-week braids special]]",
             "Ask walk-ins to opt in via the QR code"),
            ("Week 6", "Rebooking nudges for clients due in [[N]] weeks; test two post styles (before/after vs "
                       "price card)", "Take before/after photos with consent"),
            ("Week 7", "Analyst review: which styles and days fill up; adjust posting times and offers",
             "Review call"),
            ("Week 8", "60-day review against targets; decide on Starter or Growth (catalog and in-chat checkout "
                       "for products)", "Choose your plan"),
        ]
    else:
        rows = [
            ("Week 1", "Discovery call; WhatsApp Business number (Embedded Signup); greeting and FAQ chatbot",
             "Share price list, photos and FAQs; approve replies"),
            ("Week 2", "Facebook Page and link-in-bio connected; wa.me link and QR code; first 2 weeks of posts in "
                       "[[LANGUAGES]]", "Approve posts; print the QR code"),
            ("Week 3", "Payments: [[Yoco card / Ozow EFT]] for [[orders / deposits]]; confirmation messages",
             "Open or connect your payment account [[CONFIRM SET-UP ROUTE]]"),
            ("Week 4", "Baseline check (chats, reply time, orders, posts); agree Target (goal) numbers",
             "15-minute review call"),
            ("Week 5", "First WhatsApp broadcast to opted-in customers with an approved template: [[OFFER]]",
             "Choose the offer; ask regulars to opt in"),
            ("Week 6", "Follow-up and repeat-order nudges; test two post styles", "Share what customers say"),
            ("Week 7", "Analyst review; adjust posting times, messages and offers", "Review call"),
            ("Week 8", "60-day review against targets; stay on Starter or move to Growth for catalog and checkout",
             "Choose your plan"),
        ]
    d.table(["When", "What we set up together", "Your part"], rows, [2.0, 9.4, 5.6], "First 60 days plan")

    # 5. Plans --------------------------------------------------------------------------------
    d.h1("5. Plans for you")
    rows = [
        ("Monthly price", "R499", "R1,999"),
        ("Founding Member price\n(first 2 monthly bills)", "R349, then R499", "R1,399, then R1,999"),
        ("Annual price (2 months free)", "R4,990", "R19,990"),
        ("Brands · channels · AI credits/mo", "1 · 3 · 5,000", "3 · 15 · 25,000"),
        ("AI marketing team and chatbot", "✓", "✓"),
        ("WhatsApp catalog, checkout in chat, abandoned-cart recovery", "–", "✓"),
        ("USSD and integrations (Shopify, WooCommerce, Takealot and more)", "–", "✓"),
        ("Support", "Community", "Email"),
        ("Free trial", "14 days, no card", "14 days, no card"),
    ]
    d.table(["", "Starter", "Growth"], rows, [7.4, 4.8, 4.8], "Starter and Growth plan comparison",
            aligns=[None, "center", "center"], highlight_rows=(1,))
    d.h2("Founding Member launch offer")
    d.para("Subscribe between **1 December 2026 and 31 January 2027** and pay 30% less for your first 2 monthly bills: "
           "Starter R349 (then R499) or Growth R1,399 (then R1,999). On annual plans you get 2 extra months free "
           "(14 months for the price of 12). Founding Members also get a Founding Member badge and priority support. "
           "The offer comes on top of the 14-day free trial.")
    d.figure("infographics/founding-member-offer.png",
             "Founding Member launch offer for South Africa, 1 December 2026 to 31 January 2027.",
             "Founding Member offer: 30% off the first 2 monthly bills or 2 extra months free on annual plans, "
             "Founding Member badge and priority support, Growth example of R1,399 for months 1 and 2 then R1,999, "
             "and the South Africa launch window.", width_cm=15)
    if S:
        d.para(f"**Our recommendation for {client}:** start on **Starter**. Bookings, deposits, reminders and posts all "
               "work there. Move to **Growth** when you're ready to sell braiding hair, extensions and aftercare in a "
               "WhatsApp catalog with checkout in the chat.")
    else:
        d.para(f"**Our recommendation for {client}:** [[Starter / Growth]], because [[REASON IN ONE SENTENCE]].")

    # 6. Getting paid -------------------------------------------------------------------------
    d.h1("6. How you'll get paid")
    d.table(["Payment option", "How customers pay", "Good for"], [
        ("Yoco", "Card and tap-to-pay", "Deposits and in-store payments" if S else "Card buyers, in person and online"),
        ("Ozow", "Instant EFT (pay-by-bank), no card needed", "Clients who prefer to pay from their banking app"),
        ("Paystack", "Cards and bank transfer", "Also available in South Africa"),
    ], [3.2, 7.0, 6.8], "Payment options in South Africa")
    d.bullets([
        "On Growth, buyers pay inside the WhatsApp checkout and get an order confirmation and status updates on WhatsApp.",
        "Fewer cash handovers and proof-of-payment screenshots to check by hand.",
        "Provider fees are charged by the payment provider: [[FEE ESTIMATE PER PROVIDER]]. Merchant account and "
        "settlement to your bank: [[CONFIRM SET-UP ROUTE WITH PROVIDER]].",
    ] + (["Deposit rule for the studio: [[R AMOUNT]] or [[N]]% of the style price, credited to the final bill; "
          "no-show policy: [[OWNER'S POLICY]]."] if S else []))

    # 7. Measure ------------------------------------------------------------------------------
    d.h1("7. What you'll measure")
    d.para("We set the baseline in week 4. The numbers below are **targets (goals) we agree together, not promised "
           "results**.")
    if S:
        rows = [
            ("WhatsApp conversations handled", "[[ ]]", "+50%", "FluxMuse inbox"),
            ("Median first-reply time", "[[ ]]", "Under 2 min (chatbot)", "FluxMuse inbox"),
            ("Bookings via WhatsApp", "[[ ]]", "+30%", "Booking chatbot"),
            ("Deposits collected in chat", "[[ ]]", "60% of bookings", "Payments report"),
            ("No-show rate", "[[ ]]", "−40%", "Bookings vs arrivals"),
            ("Posts published per month", "[[ ]]", "12+", "Publisher calendar"),
            ("Product sales in chat (R)", "[[ ]]", "First R[[AMOUNT]] (on Growth)", "Orders report"),
            ("Repeat-customer rate", "[[ ]]", "+15%", "Customer segments"),
            ("Owner hours saved per week", "[[ ]]", "5+", "Owner's estimate at review"),
        ]
    else:
        rows = [
            ("WhatsApp conversations per week", "[[ ]]", "[[e.g. +50%]]", "FluxMuse inbox"),
            ("Median first-reply time", "[[ ]]", "[[e.g. under 2 min (chatbot)]]", "FluxMuse inbox"),
            ("Orders or bookings from WhatsApp per week", "[[ ]]", "[[e.g. +30%]]", "Orders or bookings report"),
            ("Payments collected in chat (R)", "[[ ]]", "[[R AMOUNT]]", "Payments report"),
            ("Posts published per month", "[[ ]]", "[[e.g. 12+]]", "Publisher calendar"),
            ("Repeat customers", "[[ ]]", "[[e.g. +15%]]", "Customer segments"),
            ("Hours you save per week", "[[ ]]", "[[e.g. 5+]]", "Your estimate at the review"),
        ]
    d.table(["KPI", "Baseline (week 4)", "Target (goal) by day 60", "How we measure"], rows,
            [5.6, 3.0, 4.4, 4.0], "KPI targets (goals)")

    # 8. Next steps, POPIA, terms, acceptance --------------------------------------------------
    d.h1("8. Next steps")
    d.numbered([
        "Reply “YES” on WhatsApp to [[PHONE / WHATSAPP]] or sign section 10.",
        "We book a 30-minute set-up call on [[DATE]].",
        "Start your 14-day free trial at fluxmuse.ai (no card required).",
        "Week 1 set-up begins, and we check in every week for 60 days.",
    ])
    C.popia_clause(d, client=client)
    C.terms(d, 9, short=True)
    C.acceptance(d, 10, [
        "Starter, monthly (R499/mo; R349 for the first 2 monthly bills if subscribing 1 Dec 2026 to 31 Jan 2027)",
        "Starter, annual (R4,990/yr; 2 extra months free in the launch window)",
        "Growth, monthly (R1,999/mo; R1,399 for the first 2 monthly bills if subscribing in the launch window)",
        "Growth, annual (R19,990/yr; 2 extra months free in the launch window)",
        "Start with the 14-day free trial first",
    ], client=client, terms_num=9)
    d.save(out_path, "FluxMuse proposal: " + ("Sample braiding studio" if S else "Solo entrepreneur"),
           "Marketing proposal template")
    return d
