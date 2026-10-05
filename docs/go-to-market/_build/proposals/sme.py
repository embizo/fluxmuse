"""Template 2: SME growth proposal. Facts: ../../08_Prospects/CURRENT_OFFER.md"""
from fmdoc import FMDoc
import common as C

CL = "[[CLIENT NAME]]"


def build_sme(out_path):
    d = FMDoc()
    d.cover("Proposal · SME growth", "Sell and grow on WhatsApp, with an AI team behind you",
            f"A 60-day set-up and growth plan for {CL}")
    C.how_to_use(d, "SME growth proposal template", extra=[
        "[ ] Shopify, WooCommerce and Takealot sync is partly built and not offered yet. Don't promise it.",
        "[ ] AI Voice is beta on Growth (inbound) and Scale (inbound and outbound): offer it as “beta, evaluated "
        "together”, never as a receptionist replacement.",
        "[ ] Optional service fees are [[TBC]] until the founder publishes a services price list.",
    ])
    d.toc()
    d.page_break()

    # 1 ----------------------------------------------------------------------------------------
    d.h1("1. Executive summary")
    d.para(f"{CL} sells to customers who already live on WhatsApp, but [[SUMMARY OF THE PROBLEM IN ONE SENTENCE, e.g. "
           "enquiries are handled by hand on several phones, and posting depends on who has time]].")
    d.para(f"FluxMuse proposes a **60-day set-up and growth plan** on the plan that fits {CL}: your products in a "
           "WhatsApp-ready shop, posts made by AI in your customers' languages, and every order alerted on WhatsApp. "
           "FluxMuse is newly launched; we're opening with a small first group of businesses and we set you up by "
           "hand. We agree targets at kickoff, check in weekly, and review at day 30 and day 60.")
    d.table(["Item", "Proposed"], [
        ("Recommended plan", "[[Starter R499/mo / Growth R1,999/mo / Scale R4,999/mo]]"),
        ("Set-up and review", "60 days from [[START DATE]], with reviews at day 30 and day 60"),
        ("Channels", "WhatsApp, hosted shop link, TikTok video. Facebook and Instagram auto-posting are being "
                     "switched on (Meta approval)"),
        ("Orders", "Orders arrive on your WhatsApp. Checkout through FluxMuse is being switched on"),
        ("Guarantee", "3 qualified leads in 30 days of go-live, with conditions (section 8)"),
        ("Investment", "From R499/mo, plus optional services [[TBC]] and third-party pass-through costs (section 8)"),
        ("Decision needed by", "[[DATE + 30 days]]"),
    ], [4.2, 12.8], "Executive summary")

    # 2 ----------------------------------------------------------------------------------------
    d.h1(f"2. About {CL} and our understanding")
    d.h2("Business snapshot")
    d.table(["Area", f"{CL}"], [
        ("Industry and offer", "[[e.g. restaurant, online beauty brand, clinic, auto services]]"),
        ("Locations and team", "[[N]] branches · [[N]] staff · [[AREAS]]"),
        ("Customers", "[[WHO THEY ARE, LANGUAGES, WHERE THEY BUY]]"),
        ("Channels today", "[[e.g. WhatsApp Business app on 3 phones, Facebook, Instagram, website]]"),
        ("How customers pay today", "[[e.g. card on delivery, EFT, cash]]"),
    ], [4.6, 12.4], "Client business snapshot")
    d.h2("What we heard (hypotheses to check with you)")
    d.checklist([
        "WhatsApp is handled by hand by staff on personal or shared phones",
        "Slow replies after hours and at peak times; enquiries go cold",
        "Product photos and prices are sent one chat at a time",
        "Posting depends on who has time, in one language only",
        "No simple count of which posts or links bring in enquiries",
        "Other: [[IN THE CLIENT'S WORDS]]",
    ])
    d.figure("infographics/segment-sme.png",
             "SMEs: today vs with FluxMuse.",
             "Segment card for SMEs: everyday problems matched to what FluxMuse does on WhatsApp.")

    # 3 ----------------------------------------------------------------------------------------
    d.h1("3. Objectives and success metrics")
    d.para("We confirm the starting point in the first week. **Every number in the target column is a goal agreed at "
           "kickoff, not a promised result.**")
    d.table(["#", "Objective", "KPI", "Baseline", "Target (goal)", "By"], [
        ("O1", "Bring in new WhatsApp leads", "Qualified leads through tracked links", "0 at go-live", "3+ (lead guarantee)", "Day 30"),
        ("O2", "Get products in front of buyers", "Products live in the shop", "[[ ]]", "[[e.g. 30]]", "Day 14"),
        ("O3", "Never miss an order", "Orders alerted on WhatsApp", "[[ ]]", "[[N]]", "Day 60"),
        ("O4", "Publish consistently", "Posts made per month", "[[ ]]", "[[e.g. 12+]]", "Day 30"),
        ("O5", "Grow the opted-in list", "Contacts opted in to broadcasts", "[[ ]]", "[[N]]", "Day 60"),
        ("O6", "Free up staff time", "Staff hours saved per week", "[[ ]]", "[[ ]]", "Day 60"),
    ], [1.0, 4.4, 4.2, 2.1, 3.3, 2.0], "Objectives and KPI targets (goals)", size=9)

    # 4 ----------------------------------------------------------------------------------------
    d.h1("4. What FluxMuse does")
    d.para("Every capability below carries its real status today.")
    C.status_table(d, extra=[
        ("AI Voice: inbound calls on Growth, inbound and outbound on Scale", "Beta, evaluated together"),
        ("Sync from Shopify, WooCommerce or Takealot", "Not offered yet"),
    ])
    d.figure("infographics/platform-stack.png",
             "How FluxMuse fits together. Items being switched on are labelled in the table above.",
             "Platform stack diagram showing channels, the AI team, commerce and trust layers.")

    # 5 ----------------------------------------------------------------------------------------
    d.h1("5. Scope of work and deliverables")
    d.para("**Included** = part of the FluxMuse plan. **Optional** = a FluxMuse service at an extra fee [[TBC]]. "
           f"**Client** = what {CL} provides.", size=9.5)
    d.table(["Area", "Deliverable", "Included", "Optional [[TBC]]", "Client responsibility"], [
        ("Set-up", "WhatsApp Business number, profile and quick replies", "Hand set-up with you",
         "–", "Meta Business account access, number, display name"),
        ("Set-up", "Shop of [[N]] products from your photos", "WhatsApp Concierge drafts; you approve",
         "Catalogue build by our team", "Photos, prices, stock"),
        ("Content", "Posts and captions in [[LANGUAGES]]", "AI captions, images and short video clips",
         "Human review of drafts", "Brand guidelines, approvals"),
        ("Messaging", "Broadcast templates to opted-in contacts", "Templates and Meta submission",
         "–", "Opted-in contact lists"),
        ("Reporting", "Weekly check-ins, 30- and 60-day reviews", "Included", "Monthly review pack",
         "Attend reviews, act on actions"),
    ], [2.0, 4.4, 3.5, 3.3, 3.8], "Scope of work: included, optional and client responsibilities", size=8.5)
    d.para("**Out of scope unless agreed in writing:** [[e.g. photo shoots, website rebuilds, ad management, "
           "printing]].", size=9.5)

    # 6 ----------------------------------------------------------------------------------------
    d.h1("6. 60-day plan")
    d.figure("infographics/brand-engagement-journey.png",
             "How we work together, from discovery call to a plan. Timings are typical; KPI targets are goals.",
             "Journey from discovery call through set-up and review to a plan decision.")
    d.table(["Phase", "Objectives", "Deliverables", "Tracked"], [
        ("Days 1–30\nSet up and go live", "Go live on WhatsApp with a shop link; start counting leads",
         "Number and shop live; QR codes and links; first posts; first broadcast", "Qualified leads; orders alerted; posts"),
        ("Days 31–60\nImprove", "Do more of what brings leads; grow the opted-in list",
         "Two post styles tested; opt-in drive; day-60 review", "Leads; orders; opt-ins; hours saved"),
    ], [3.3, 4.0, 5.2, 4.5], "Plan phases", size=9)
    d.table(["Milestone", "Date"], [
        ("Proposal accepted and first payment", "[[DATE]]"), ("Kickoff", "[[DATE]]"), ("Go-live", "[[DATE]]"),
        ("Day-30 review (lead guarantee check)", "[[DATE]]"), ("Day-60 review", "[[DATE]]"),
    ], [9.0, 8.0], "Key milestones")

    # 7 ----------------------------------------------------------------------------------------
    d.h1("7. Investment options")
    d.para("Every paid plan starts with payment. Annual = 10× monthly for 12 months.")
    d.table(["Plan", "Monthly", "Annual", "Founding Member*", "Includes"], [
        ("Starter", "R499", "R4,990", "R349 for the first two monthly bills", "1 brand, 3 channels"),
        ("Growth", "R1,999", "R19,990", "R1,399 for the first two monthly bills",
         "3 brands, 15 channels, inbound AI Voice (beta)"),
        ("Scale", "R4,999", "R49,990", "R3,499 for the first two monthly bills",
         "10 brands, 40 channels, inbound and outbound AI Voice (beta)"),
    ], [2.4, 2.0, 2.3, 4.1, 6.2], "Plan investment options", size=9, highlight_rows=(1,))
    d.para("*" + C.FOUNDING_LINE + " AI credits come with every plan; see fluxmuse.ai/pricing for the current "
           "allowance. More than 10 brands: Corporate (R6,999/mo) or Custom, by consultation.", size=9)
    d.figure("infographics/pricing-tiers.png",
             "FluxMuse plans in ZAR. Annual = 10× monthly.",
             "FluxMuse pricing tiers in South African rand.")
    d.h2("Optional FluxMuse services")
    d.table(["Service", "Fee", "Notes"], [
        ("Hand set-up", "Included", "We set you up by hand"),
        ("Catalogue build", "[[TBC]]", "Up to [[N]] products"),
        ("Content review", "[[TBC]] /mo", "Human review of AI drafts"),
        ("Extra training", "[[TBC]] per session", "For additional teams or branches"),
    ], [5.0, 3.0, 9.0], "Optional services fees")
    d.h2("Third-party pass-through costs")
    d.para("Charged by the provider at their rates, not by FluxMuse. Estimates until usage is known.", size=9.5)
    d.table(["Cost", "Charged by", "Estimate", "Depends on"], [
        ("WhatsApp template message fees", "Meta", "[[estimate R/mo]]", "Message volume and category"),
        ("Ad spend (if any)", "Meta", "[[estimate R/mo]]", f"Budget set by {CL}"),
    ], [5.6, 3.6, 3.2, 4.6], "Third-party pass-through costs")
    d.h2("First three months at a glance")
    d.table(["Item", "Month 1", "Month 2", "Month 3"], [
        ("FluxMuse plan ([[Starter / Growth / Scale]])", "[[R]]", "[[R]]", "[[R]]"),
        ("Optional services", "[[TBC]]", "[[TBC]]", "[[TBC]]"),
        ("Pass-through costs (estimate)", "[[R]]", "[[R]]", "[[R]]"),
        ("Total", "[[R]]", "[[R]]", "[[R]]"),
    ], [7.0, 3.3, 3.3, 3.4], "Three-month investment summary", total_rows=(3,), aligns=[None, "right", "right", "right"])

    # 8 ----------------------------------------------------------------------------------------
    d.h1("8. Payments and our guarantee")
    d.bullets([
        "Orders from the shop link arrive on your WhatsApp; you take payment the way you do today.",
        C.CHECKOUT_NOTE,
        "Your FluxMuse subscription is paid through Paystack, Yoco or Ozow.",
        "Paid plans are for South African businesses. Businesses elsewhere can join the waitlist.",
    ])
    d.callout("Our lead guarantee", [C.GUARANTEE])

    # 9 ----------------------------------------------------------------------------------------
    d.h1("9. Reporting and governance")
    d.table(["Cadence", "What", "Who", "Format"], [
        ("Weekly", "30-minute check-in: progress against targets, blockers, next actions",
         f"{C.SENDER} + [[CLIENT OWNER]]", "Call + written actions"),
        ("Day 30", "Review, including the lead guarantee count", "Both teams", "Report"),
        ("Day 60", "Review and plan decision", "Decision makers", "Report + meeting"),
    ], [3.0, 7.2, 3.8, 3.0], "Reporting cadence", size=9)
    d.h2("Roles")
    d.table(["Role", "Name", "Responsible for"], [
        ("FluxMuse lead", C.SENDER, "Plan, set-up, reviews, escalations"),
        (f"{CL} project owner", "[[NAME]]", "Access, data, internal decisions"),
        ("Content approver", "[[NAME]]", "Approves posts and broadcasts"),
    ], [5.0, 4.0, 8.0], "Governance roles")

    # 10 ---------------------------------------------------------------------------------------
    d.h1("10. Where we are")
    d.para("FluxMuse is newly launched. We have no customer results to show you yet, and we won't invent any. "
           "We're opening with a small first group of businesses, and we set each one up by hand. Case studies come "
           "later, only with a business's written consent.")

    # 11 ---------------------------------------------------------------------------------------
    d.h1("11. Trust and compliance")
    C.trust_bullets(d)
    C.popia_clause(d)

    # 12 ---------------------------------------------------------------------------------------
    d.h1("12. Assumptions and client dependencies")
    d.bullets([
        f"{CL} gives FluxMuse admin access to its Meta Business account within [[N]] working days of kickoff.",
        "A phone number is available for the WhatsApp Business account and Meta approves the display name.",
        "WhatsApp broadcasts use Meta-approved templates and go only to contacts who opted in.",
        f"{CL} provides product photos and prices, and approves content within [[N]] working days.",
        "Ad budgets and Meta message fees are paid by the client (pass-through).",
        "Facebook and Instagram auto-posting start only after Meta approval; the plan doesn't depend on them.",
        "[[OTHER ASSUMPTIONS]]",
    ])

    C.terms(d, 13)
    C.acceptance(d, 14, [
        "Starter, monthly (R499/mo) or annual (R4,990/yr)",
        "Growth, monthly (R1,999/mo) or annual (R19,990/yr)",
        "Scale, monthly (R4,999/mo) or annual (R49,990/yr)",
        "Founding Member discount (South African sign-up, first two monthly bills)",
        "Optional services: [[LIST]]",
        "60-day plan as described, starting [[DATE]]",
    ], terms_num=13)
    d.save(out_path, "FluxMuse proposal: SME growth", "Marketing proposal template")
    return d
