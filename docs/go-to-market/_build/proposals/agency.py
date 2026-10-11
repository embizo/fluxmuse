"""Template 3: Flux_Partner (agency partner) proposal."""
from fmdoc import FMDoc
import common as C

AG = "[[AGENCY NAME]]"


def build_agency(out_path):
    d = FMDoc(client_ph=AG)
    d.cover("Flux_Partner programme proposal", "Serve more clients under your own brand",
            f"Partner proposal for {AG}", client_label="Prepared for")
    C.how_to_use(d, "Agency partner (Flux_Partner) proposal template", extra=[
        "[ ] Agencies get the partner wholesale price of R6,999/mo (30% off the R9,999 Agency list price), every "
        "month. Founding Member on Agency is also R6,999, but only for the first two bills; the two never stack.",
        "[ ] Partner economics are illustrative. Don't quote a fixed margin percentage: margin depends on the partner's "
        "retail price and costs.",
        "[ ] Partner programme terms (section 7) are live as of 9 October 2026 and come from 08_Prospects/"
        "CURRENT_OFFER.md §1. Quote them exactly; don't add customer discounts or other incentives.",
    ])
    d.toc()
    d.page_break()

    # 1 ----------------------------------------------------------------------------------------
    d.h1("1. Why partner with FluxMuse")
    d.para(f"{AG} manages [[N]] SMB clients who want more from social and WhatsApp than posts and a monthly report. "
           "FluxMuse lets your team run marketing, WhatsApp commerce and reporting for all of them from one platform, "
           "under your brand, at a wholesale price you mark up yourself.")
    d.table(["What agencies tell us", "What FluxMuse changes"], [
        ("Margin squeeze on every client retainer", "Wholesale Agency plan, your own retail price: you keep the spread"),
        ("Manual reporting and too many tools per client", "White-label and multi-client on one platform, "
                                                          "with unlimited brands and 80 channels"),
        ("Clients asking for WhatsApp commerce and AI", "Resell WhatsApp shops, AI posts and order alerts under your own brand"),
    ], [7.0, 10.0], "Agency pains and FluxMuse answers")
    d.figure("infographics/segment-agency.png",
             "Agencies: today vs with FluxMuse.",
             "Segment card for agencies: margin squeeze, manual reporting and client demand for WhatsApp commerce, "
             "matched to wholesale pricing and white-label, multi-client tools.")
    d.callout("Programme status", [
        "FluxMuse is newly launched, and the partner programme opened on 9 October 2026. You would be among the "
        "first partners, and we set you up by hand.",
        "On the Agency tier: white-label, multi-client, unlimited brands, 80 channels, bring your own cloud. "
        "[[FOUNDER TO CONFIRM: reseller billing and partner directory status]]",
        "Live now: the partner programme, with a partner portal, your own ?ref= share link and QR code, and "
        "commission of 15% to 25% on customers you refer (section 7).",
    ])

    # 2 ----------------------------------------------------------------------------------------
    d.h1("2. What partners get")
    d.table(["Inclusion", "Detail"], [
        ("White-label", "Your brand on the client experience [[CONFIRM: app, reports, custom domain]]"),
        ("Multi-client", "One workspace per client, managed by your team [[CONFIRM: sub-account limit]]"),
        ("Unlimited brands, 80 channels", "Across all your clients"),
        ("Bring your own cloud", "Run on your own cloud account if you want to [[CONFIRM SCOPE]]"),
        ("AI credits", "Included; see fluxmuse.ai/pricing [[CONFIRM HOW CREDITS ARE SHARED ACROSS CLIENTS]]"),
        ("Live for your clients (newly launched)", "WhatsApp Concierge, hosted shop links, order alerts, AI captions, "
                                                    "images and short video, WhatsApp broadcasts to opted-in contacts, "
                                                    "TikTok video posting"),
        ("Being switched on", "Checkout through FluxMuse, Facebook and Instagram auto-posting, AI Voice (beta)"),
        ("Support", f"Direct line to {C.SENDER}, {C.SENDER_EMAIL}"),
    ], [4.6, 12.4], "Partner inclusions")

    # 3 ----------------------------------------------------------------------------------------
    d.h1("3. Partner wholesale pricing")
    d.para("Partners buy the Agency tier at **30% off list** for as long as the partner agreement is active, then "
           "set their own retail price for clients. Same inclusions as the Agency plan.")
    d.table(["", "Agency list", "Partner wholesale"], [
        ("Monthly", "R9,999", "R6,999"),
        ("Annual (10\u00d7 monthly)", "R99,990", "R69,990"),
    ], [5.0, 6.0, 6.0], "Partner wholesale pricing", aligns=[None, "right", "right"], highlight_rows=(0,))
    d.bullets([
        "Payment first: the first month is paid when you subscribe. No trial period.",
        "Wholesale pricing doesn't stack with the Founding Member offer or with partner-level discounts.",
        "Paid plans are for South African businesses. Clients outside South Africa can join the waitlist.",
        "Pass-through costs (Meta WhatsApp message fees, ad spend) are separate and can be re-billed to your clients.",
    ])

    # 4 ----------------------------------------------------------------------------------------
    d.h1("4. Partner economics")
    d.h2("Illustrative example")
    d.para("**Illustrative only, not a forecast.** A partner serving 20 clients at a retail price they set:", keep=True)
    d.table(["Line", "Illustrative (ZAR per month)"], [
        ("Clients served", "20"),
        ("Retail price per client (set by the partner)", "R1,500"),
        ("Retail revenue (20 × R1,500)", "R30,000"),
        ("Partner wholesale Agency plan", "− R6,999"),
        ("Gross spread before the partner's own service costs", "R23,001"),
        ("Platform cost per client (R6,999 ÷ 20)", "about R350"),
    ], [11.0, 6.0], "Illustrative partner economics", aligns=[None, "right"], total_rows=(4,))
    d.para("Before payment fees, ad spend and your team's delivery costs. Your margin depends on your retail price "
           "and costs.", size=9)
    d.figure("infographics/agency-partner-model.png",
             "How the partner model works: FluxMuse bills the partner wholesale; the partner bills clients at their own "
             "price. Example is illustrative.",
             "Partner model diagram: FluxMuse supplies the platform to the agency at the wholesale price; the agency "
             "serves its clients at a retail price it sets.")
    d.h2("Your numbers")
    d.table(["", "Line", "How to calculate", f"{AG}"], [
        ("A", "Number of clients", "Your client count", "[[ ]]"),
        ("B", "Your retail price per client /mo", "You set it", "[[R ]]"),
        ("C", "Monthly retail revenue", "A × B", "[[R ]]"),
        ("D", "Partner wholesale plan /mo", "R6,999", "[[R ]]"),
        ("E", "Gross spread", "C − D", "[[R ]]"),
        ("F", "Your service costs /mo", "Team hours, design, ad management", "[[R ]]"),
        ("G", "Net contribution /mo", "E − F", "[[R ]]"),
        ("H", "Net contribution per client", "G ÷ A", "[[R ]]"),
    ], [1.0, 5.6, 6.4, 4.0], "Partner economics calculator", aligns=["center", None, None, "right"], total_rows=(6,))

    # 5 ----------------------------------------------------------------------------------------
    d.h1("5. Onboarding plan (first 30 days)")
    d.table(["Days", "Focus", "Activities", "Output"], [
        ("1–5", "Kickoff and white-label", "Partner workspace; white-label set-up (logo, colours, [[DOMAIN]]); your "
                                           "retail price list", "Branded workspace ready"),
        ("6–10", "Team training", "WhatsApp set-up for clients; WhatsApp Concierge and shop links; POST captions "
                                  "and images; broadcasts", "[[N]] team members trained"),
        ("11–20", "First client", "Workspace for [[FIRST CLIENT]]; WhatsApp number, shop, "
                                        "first posts; targets agreed", "First client live"),
        ("21–30", "Report and plan", "Review with FluxMuse, including the lead guarantee count; plan for the next [[N]] clients",
         "Partner growth plan"),
    ], [1.6, 3.4, 8.4, 3.6], "30-day partner onboarding plan", size=9)

    d.callout("Lead guarantee for each client you bring live", [C.GUARANTEE.replace("your first 30 days", "the "
              "client's first 30 days").replace("you held up your side", "the client held up their side").replace(
              "working with you", "working with you and the client").replace("until you have 3", "until they have 3")])

    # 6 ----------------------------------------------------------------------------------------
    d.h1("6. What FluxMuse provides")
    d.table(["Support", "FluxMuse provides", f"{AG} provides", "Status"], [
        ("Partner portal", "Customers, revenue, commission and payouts in one place", "Your login", "Live"),
        ("Share link and QR code", "Your own ?ref= link and QR code", "Sharing it with prospects", "Live"),
        ("Hands-on setup", "Setup of your first customers, by hand, with you", "Time with your team", "Live"),
        ("Sales materials", "Pitch deck and proposal templates", "Your branding and offer", "Live"),
        ("Joint case study", "Case-study format and design", "First client's written consent", "Later, consent only"),
    ], [3.6, 5.0, 4.8, 3.6], "Partner support", size=9)

    # 7 ----------------------------------------------------------------------------------------
    d.h1("7. Partner programme and commission")
    d.para("Some businesses a partner introduces may prefer their own FluxMuse subscription instead of a sub-account. "
           "They sign up through the partner's ?ref= link, and the partner earns commission at their level:")
    d.table(["Level", "Reached by", "Commission", "Off your own plan"], [
        ("Registered Partner", "Our team enables you", "15%", "10%"),
        ("Silver Partner", "5 paying customers or R5,000/month billed to them", "20%", "20%"),
        ("Gold Partner", "15 paying customers or R15,000/month billed to them", "25%", "30%"),
    ], [3.6, 7.4, 2.8, 3.2], "Partner levels", aligns=[None, None, "center", "center"])
    d.bullets([
        "Commission is on the subscription fees your customers actually pay (after any discount) in their first 12 "
        "months. It isn't paid on SMS, WhatsApp or AI credit top-ups, or on Custom plans.",
        "Commission is held for 30 days, then paid monthly by EFT once it reaches R500.",
        "Partners can't add discounts for customers. Your own plan gets the better of a running offer or your level "
        "discount, not both. Gold on Agency comes to R6,999, the same as partner wholesale.",
        "Your partner portal shows your share link and QR code, customers, revenue, commission and payouts.",
    ])

    # 8 ----------------------------------------------------------------------------------------
    d.h1("8. What partners commit to")
    d.table(["Commitment", "Detail"], [
        ("Honest selling", "Sell within FluxMuse's claims rules: no trials, no invented customer numbers, ratings, "
                           "testimonials or results, and no payment provider names"),
        ("Consent-first prospecting", "POPIA-compliant prospecting: contact people with consent, honour opt-outs, "
                                      "no bulk unsolicited messages"),
        ("Messaging compliance", "Follow POPIA and Meta WhatsApp Business policies: approved templates, opted-in contacts, opt-outs honoured"),
        ("Data protection", "POPIA; data processing agreement [[LEGAL REVIEW REQUIRED]]"),
        ("Bank details", "Keep your bank details current in the partner portal so commission payouts reach you"),
        ("Payment", "Wholesale fees are paid in advance, like every FluxMuse plan"),
    ], [4.6, 12.4], "Partner commitments")

    # 9 ----------------------------------------------------------------------------------------
    d.h1("9. Brand usage rules")
    d.table(["Allowed", "Not allowed"], [
        ("Full white-label: your name, logo and colours for clients", "Changing, recolouring or stretching the FluxMuse logo"),
        ("“Powered by FluxMuse” is optional; use it if you want to", "Presenting FluxMuse customer counts, ratings, "
                                                                     "testimonials or results that aren't in approved materials"),
        ("Describing the product as an AI marketing and WhatsApp commerce platform",
         "Promising Facebook or Instagram auto-posting, or checkout, before they are switched on"),
        ("Using FluxMuse brand-kit assets unmodified when co-branding", "Promising clients or investors a fixed FluxMuse margin percentage"),
        ("Quoting FluxMuse list prices from the official price table", "Offering paid plans outside South Africa, "
                                                                        "or combining Founding Member with wholesale pricing"),
    ], [8.5, 8.5], "Brand usage rules", first_col_bold=False)

    # 10 ---------------------------------------------------------------------------------------
    d.h1("10. Trust and data protection")
    C.trust_bullets(d)
    C.popia_clause(d, client="Each end client", partner=True)

    C.terms(d, 11, extra_rows=[
        ("Wholesale pricing", "30% off Agency list for as long as the partner agreement is active [[LEGAL REVIEW REQUIRED]]"),
        ("White-label and multi-client", "Client data ownership and portability on "
                                         "termination: [[LEGAL REVIEW REQUIRED]]"),
        ("Partner programme", "Levels and commission as in section 7 [[LEGAL REVIEW REQUIRED]]"),
    ])
    C.acceptance(d, 12, [
        "Partner wholesale, monthly: R6,999/mo",
        "Partner wholesale, annual: R69,990/yr",
        "30-day onboarding plan starting [[DATE]] with first client [[FIRST CLIENT]]",
        "Partner programme: start as a Registered Partner (15% commission, 10% off your own plan)",
    ], client=AG, terms_num=11)
    d.save(out_path, "FluxMuse proposal: Agency partner", "Flux_Partner programme proposal template")
    return d
