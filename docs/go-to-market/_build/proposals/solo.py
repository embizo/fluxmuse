"""Template 1 (Solo entrepreneur) and template 5 (worked example: braiding & hair studio).

Facts: ../../08_Prospects/CURRENT_OFFER.md. The worked example is an imagined prospect with no results."""
from fmdoc import FMDoc
import common as C


def build_solo(out_path, sample=False):
    S = sample
    client = "[[BRAND NAME]]" if S else "[[CLIENT NAME]]"
    first = "[[OWNER]]" if S else "[[FIRST NAME]]"
    d = FMDoc(sample=S, client_ph=client)

    d.cover("Proposal · Solo entrepreneur" if not S else "Example proposal · Braiding & hair studio",
            "Your shop and your posts, run from WhatsApp" if not S
            else "Your styles, your prices and your posts, all from WhatsApp",
            f"A FluxMuse plan for {client}" if not S else f"A FluxMuse plan for {client}, [[AREA]]")

    extra = []
    if S:
        extra.append("[ ] This is a worked example for an imagined prospect. It shows tone and detail, not real results. "
                     "Copy wording into the Solo template; don't send this file. Delete the EXAMPLE banner if you "
                     "adapt it.")
    C.how_to_use(d, "Solo entrepreneur proposal (worked example)" if S else "Solo entrepreneur proposal template",
                 extra=extra)

    # 1. Letter -------------------------------------------------------------------------------
    d.h1(f"1. Hi {first}")
    if S:
        d.para(f"Thank you for showing us around {client} in [[AREA]]. Clients book because they've seen your braids "
               "on WhatsApp Status and through word of mouth. What eats your time is the admin: sending the same price "
               "list again and again, and posting only when there's a gap between clients.")
        d.para("FluxMuse turns your style photos into a price list and a shop link you can share, writes captions for "
               "your before/after photos in the languages your clients speak, and alerts you on WhatsApp when someone "
               "wants to book.")
    else:
        d.para(f"Thank you for telling us about {client}. You said you want [[THEIR MAIN GOAL, e.g. more orders "
               "without living on your phone]]. You're already doing the hard part: people know your work and message "
               "you on WhatsApp. FluxMuse helps you put your products in a shop link, post more often and see every "
               "order on WhatsApp, without hiring a marketer.")
    d.para("FluxMuse is newly launched. We're opening with a small first group of businesses, and we set you up by "
           "hand. This proposal is short on purpose: what we heard, what we'll set up, your first 30 days, the plan we "
           "recommend and how we'll both know it's working.")
    d.para("Warm regards,", after=0)
    d.para(f"{C.SENDER}, Founder, FluxMuse · {C.SENDER_EMAIL} · [[PHONE / WHATSAPP]]")

    # 2. What we heard ------------------------------------------------------------------------
    d.h1("2. What we heard", new_page=False)
    d.para("Tick what applies. " if not S else "From our first conversation (ticked items came up):", keep=True)
    if S:
        d.checklist([
            ("Booking requests get lost in busy WhatsApp chats, and messages after hours wait until the next day", True),
            ("The same price list and style photos get sent to every new enquiry by hand", True),
            ("Posting happens when there's a gap between clients, so weeks go by with nothing new", True),
            ("Clients speak isiZulu, Sesotho and English, and captions are usually English only", True),
            ("Regulars aren't reminded when it's time to redo their hair", False),
            ("Braiding hair and aftercare products are sold only when someone asks", False),
            ("In [[OWNER]]'s words: “[[OWNER'S WORDS FROM THE VISIT]]”", False),
        ])
    else:
        d.checklist([
            "I miss messages and lose sales in busy WhatsApp chats",
            "I send the same photos and prices to every new customer",
            "I don't have time or budget for a marketer, so I post when I can",
            "I want to post in more than one language: [[LANGUAGES]]",
            "Customers don't come back as often as I'd like, and I don't follow up",
            "In your words: “[[QUOTE FROM THE DISCOVERY CALL]]”",
        ])
    d.figure("infographics/segment-solo.png",
             "Solo entrepreneurs: today vs with FluxMuse.",
             "Segment card for solo entrepreneurs: everyday problems matched to what FluxMuse does on WhatsApp.",
             width_cm=16)

    # 3. What FluxMuse will do ------------------------------------------------------------------
    d.h1("3. What FluxMuse will do for you")
    if S:
        d.bullets([
            "**Your styles as a shop.** Send photos of your styles to FluxMuse on WhatsApp. The AI drafts each entry "
            "(name, description, a price guess) and you reply YES, NO or fix it. Knotless, box braids, cornrows, "
            "[[STYLES]].",
            "**A shop link to share** (fluxmuse.ai/s/[[NAME]]) for your bio, Status and a QR code on the mirror. When a "
            "client picks a style, the request arrives on your own WhatsApp as a ready-typed message.",
            "**Alerts on WhatsApp** for every request, and you reply SOLD when a slot or product is taken.",
            "**Posts made for you.** Send POST with a before/after photo and get a caption and image back, ready to "
            "forward to your WhatsApp Status. Captions in isiZulu, Sesotho and English.",
            "**Voice notes typed out**, and short AI video clips for TikTok, which FluxMuse can post for you.",
            "**Broadcasts to regulars who opted in**, using Meta-approved templates, for a mid-week special or a "
            "rebooking nudge.",
        ])
    else:
        d.bullets([
            "**Your products as a shop.** Send product photos to FluxMuse on WhatsApp. The AI drafts each catalogue "
            "entry (name, description, a price guess) and you reply YES, NO or an edit.",
            "**A shop link to share** (fluxmuse.ai/s/[[NAME]]). Orders arrive on your own WhatsApp number as a "
            "ready-typed message, so you never miss one.",
            "**Order alerts on WhatsApp.** Reply SOLD to mark an item sold.",
            "**Posts made for you.** Send POST with a photo and get a caption and image back, ready to forward to "
            "WhatsApp Status, in [[LANGUAGES]].",
            "**Short AI video clips** and **voice notes typed out**. TikTok video posting is available.",
            "**Answers in your customer's language**, and broadcasts to customers who opted in.",
        ])
    d.callout("Being switched on (not live yet)", [
        "**Checkout through FluxMuse.** Built, but not yet tested end to end with real money. Until it is, you take "
        "payment the way you do today" + (" (including deposits)." if S else "."),
        "**Auto-posting to Facebook and Instagram.** Waiting for Meta approval. For now, posts come back to you on "
        "WhatsApp, ready to forward to Status or post yourself.",
    ])
    d.figure("infographics/whatsapp-commerce-flow.png",
             "How a request reaches you on WhatsApp. Checkout through FluxMuse is being switched on.",
             "WhatsApp commerce flow from a shared link to an order alert on the merchant's WhatsApp.")

    # 4. First 30 days --------------------------------------------------------------------------
    d.h1("4. Your first 30 days")
    d.para("We set you up by hand. Each week needs about [[N]] minutes of your time.")
    if S:
        rows = [
            ("Week 1", "WhatsApp Business number and profile; your styles photographed into the shop with prices",
             "Send your price list, style names and 10 favourite photos"),
            ("Week 2", "Shop link live; QR code for the mirror and flyers; first before/after posts in isiZulu, "
                       "Sesotho and English", "Approve posts; print the QR code"),
            ("Week 3", "Opt-in prompt for regulars; first broadcast with an approved template: [[OFFER]]",
             "Ask walk-ins to opt in"),
            ("Week 4", "Review: requests through the link, posts made, leads counted for the guarantee",
             "15-minute review call"),
        ]
    else:
        rows = [
            ("Week 1", "WhatsApp Business number and profile; first products into the shop from your photos",
             "Send photos and prices; approve the drafts"),
            ("Week 2", "Shop link live; QR code; first posts in [[LANGUAGES]]", "Share the link; post at least weekly"),
            ("Week 3", "First broadcast to opted-in customers with an approved template: [[OFFER]]",
             "Choose the offer; ask regulars to opt in"),
            ("Week 4", "Review: leads through the link, orders, posts; agree Target (goal) numbers for the next month",
             "15-minute review call"),
        ]
    d.table(["When", "What we set up together", "Your part"], rows, [2.0, 9.4, 5.6], "First 30 days plan")
    d.callout("Our lead guarantee", [C.GUARANTEE])

    # 5. Plans --------------------------------------------------------------------------------
    d.h1("5. Plans for you")
    d.para("Every paid plan starts with payment. Annual billing is 10× the monthly price for 12 months.")
    rows = [
        ("Monthly price", "R149", "R289", "R499"),
        ("Annual price", "R1,490", "R2,890", "R4,990"),
        ("Brands · channels", "1 · 3", "1 · 4", "1 · 3"),
        ("WhatsApp Concierge, shop link, order alerts", "✓", "✓", "✓"),
        ("AI captions, images and short video clips", "✓", "✓", "✓"),
        ("Own WhatsApp Business number", "[[CONFIRM]]", "1 number", "✓"),
        ("Founding Member (first two monthly bills)", "–", "–", "R349, then R499"),
    ]
    d.table(["", "Nano", "Micro", "Starter"], rows, [6.8, 3.4, 3.4, 3.4], "Nano, Micro and Starter plan comparison",
            aligns=[None, "center", "center", "center"], highlight_rows=(0,))
    d.para("AI credits come with every plan; see fluxmuse.ai/pricing for the current allowance. "
           "[[FOUNDER TO CONFIRM: whether Founding Member also covers Nano and Micro]]", size=9)
    d.bullets([
        "**Nano (R149/mo)** is the place to start for a side-hustle: your shop, your link and posts made for you.",
        "**Micro (R289/mo)** adds a channel and your own WhatsApp number on FluxMuse.",
        "**Starter (R499/mo)** is the step up when the business grows. " + C.FOUNDING_LINE,
        "A **Free plan** exists as a permanent option (1 brand, 1 channel, no card). It is not a trial of the paid "
        "plans.",
    ])
    d.figure("infographics/founding-member-offer.png",
             "Founding Member launch offer for South African sign-ups: 30% off the first two monthly bills.",
             "Founding Member offer: 30% off the first two monthly bills for South African sign-ups.", width_cm=15)
    if S:
        d.para(f"**Our recommendation for {client}:** start on **Micro** so the studio's own WhatsApp number runs "
               "through FluxMuse. Move to **Starter** when you want more from it.")
    else:
        d.para(f"**Our recommendation for {client}:** [[Nano / Micro / Starter]], because [[REASON IN ONE SENTENCE]].")

    # 6. Getting paid -------------------------------------------------------------------------
    d.h1("6. How you'll get paid")
    d.bullets([
        "Today: the shop link sends each order to your WhatsApp, and you take payment the way you already do"
        + (", including any deposit." if S else "."),
        C.CHECKOUT_NOTE,
        "Your FluxMuse subscription is paid through Paystack, Yoco or Ozow.",
    ] + (["Deposit rule for the studio (your own, collected your way for now): [[R AMOUNT]]; no-show policy: "
          "[[OWNER'S POLICY]]."] if S else []))

    # 7. Measure ------------------------------------------------------------------------------
    d.h1("7. What you'll measure")
    d.para("We count from go-live. The numbers below are **targets (goals) we agree together, not promised results**.")
    if S:
        rows = [
            ("Qualified leads through the shop link or QR", "0 at go-live", "3+ in 30 days (lead guarantee)", "FluxMuse tracking"),
            ("Booking requests via the shop link", "[[ ]]", "[[ ]]", "Order alerts"),
            ("Posts made per month", "[[ ]]", "[[e.g. 8+]]", "POST history"),
            ("Regulars opted in to broadcasts", "[[ ]]", "[[ ]]", "Contact list"),
            ("Owner hours saved per week", "[[ ]]", "[[ ]]", "Owner's estimate at review"),
        ]
    else:
        rows = [
            ("Qualified leads through the shop link or QR", "0 at go-live", "3+ in 30 days (lead guarantee)", "FluxMuse tracking"),
            ("Orders via the shop link", "[[ ]]", "[[ ]]", "Order alerts"),
            ("Posts made per month", "[[ ]]", "[[e.g. 8+]]", "POST history"),
            ("Customers opted in to broadcasts", "[[ ]]", "[[ ]]", "Contact list"),
            ("Hours you save per week", "[[ ]]", "[[ ]]", "Your estimate at the review"),
        ]
    d.table(["KPI", "Starting point", "Target (goal) by day 30", "How we measure"], rows,
            [5.6, 3.0, 4.4, 4.0], "KPI targets (goals)")

    # 8. Next steps, POPIA, terms, acceptance --------------------------------------------------
    d.h1("8. Next steps")
    d.numbered([
        f"Reply “YES” on WhatsApp to [[PHONE / WHATSAPP]], email {C.SENDER_EMAIL} or sign section 10.",
        "Subscribe to your plan at fluxmuse.ai (payment first; Founding Member applies to South African sign-ups).",
        "We book a 30-minute set-up call on [[DATE]] and set you up by hand.",
        "Week 1 set-up begins, and we check in every week for the first 30 days.",
    ])
    C.popia_clause(d, client=client)
    C.terms(d, 9, short=True)
    C.acceptance(d, 10, [
        "Nano, monthly (R149/mo) or annual (R1,490/yr)",
        "Micro, monthly (R289/mo) or annual (R2,890/yr)",
        "Starter, monthly (R499/mo; Founding Member R349 for the first two monthly bills)",
        "Starter, annual (R4,990/yr)",
    ], client=client, terms_num=9)
    d.save(out_path, "FluxMuse proposal: " + ("Example braiding studio" if S else "Solo entrepreneur"),
           "Marketing proposal template")
    return d
