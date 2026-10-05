"""Template 3: Flux_Partner (agency partner) proposal."""
from fmdoc import FMDoc
import common as C

AG = "[[AGENCY NAME]]"


def build_agency(out_path):
    d = FMDoc(client_ph=AG)
    d.cover("Flux_Partner programme proposal", "Serve more clients under your own brand",
            f"Partner proposal for {AG}", client_label="Prepared for")
    C.how_to_use(d, "Agency partner (Flux_Partner) proposal template", extra=[
        "[ ] Agencies get the partner wholesale price of R6,999/mo (30% off the R9,999 Agency list price). Never "
        "present it as a launch discount, and never add Founding Member on top.",
        "[ ] Partner economics are illustrative. Don't quote a fixed margin percentage: margin depends on the partner's "
        "retail price and costs.",
        "[ ] Referral commission and partner obligations stay as founder placeholders until decided.",
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
        "FluxMuse is newly launched and has no agency partners yet. You would be among the first, and we set you up "
        "by hand.",
        "On the Agency tier: white-label, multi-client, unlimited brands, 80 channels, bring your own cloud. "
        "[[FOUNDER TO CONFIRM: reseller billing and partner directory status]]",
        "On the roadmap (indicative, not dated): referral tracking and the wider Flux_Partner programme.",
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
        "Wholesale pricing doesn't stack with the Founding Member offer, which isn't offered on the Agency tier.",
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
    d.h1("6. Co-marketing")
    d.table(["Activity", "FluxMuse provides", f"{AG} provides", "Status"], [
        ("Partner directory listing", "Listing and profile", "Services, areas, contact", "[[FOUNDER TO CONFIRM]]"),
        ("Sales materials", "Brand kit, pitch deck and proposal templates (white-label versions [[TBC]])",
         "Your branding and offer", "[[TBC]]"),
        ("Joint case study", "Case-study format and design", "First client's written consent", "Later, consent only"),
        ("Webinar or workshop", "Speaker and demo", "Audience and venue", "[[TBC]]"),
        ("Referral leads", "Leads that need an agency", "Follow-up within [[N]] days", "[[FOUNDER DECISION]]"),
        ("Launch announcement", "Social post and newsletter mention", "Joint post", "[[TBC]]"),
    ], [3.6, 5.0, 4.8, 3.6], "Co-marketing activities", size=9)

    # 7 ----------------------------------------------------------------------------------------
    d.h1("7. Referral commission")
    d.para("Some businesses a partner introduces may prefer their own Starter, Growth or Scale subscription instead of a "
           "sub-account. For those referrals:")
    d.table(["Item", "Position"], [
        ("Commission rate", "[[FOUNDER DECISION: referral commission %]]"),
        ("Basis and duration", "[[FOUNDER DECISION: e.g. first-year subscription fees]]"),
        ("Payout timing and method", "[[FOUNDER DECISION]]"),
        ("Tracking", "Referral tracking is on the roadmap; interim tracking: [[TBC]]"),
    ], [5.0, 12.0], "Referral commission terms")
    d.para("Referral commission is separate from wholesale pricing and isn't a discount on the partner's own plan.",
           size=9.5)

    # 8 ----------------------------------------------------------------------------------------
    d.h1("8. Partner obligations [[TBC]]")
    d.table(["Obligation", "Detail"], [
        ("Minimum commitment", "[[TBC: e.g. minimum active client sub-accounts after 90 days]]"),
        ("First-line client support", "[[TBC]]"),
        ("Training", "Complete onboarding training within 30 days [[TBC]]"),
        ("Messaging compliance", "Follow POPIA and Meta WhatsApp Business policies: approved templates, opted-in contacts, opt-outs honoured"),
        ("Data protection", "POPIA; data processing agreement [[LEGAL REVIEW REQUIRED]]"),
        ("Claims", "Only use approved FluxMuse facts: no invented customer numbers, ratings, testimonials or results"),
        ("Payment", "Wholesale fees paid in advance [[TBC]]"),
        ("Reporting to FluxMuse", "[[TBC: e.g. quarterly partner review]]"),
    ], [4.6, 12.4], "Partner obligations")

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
        ("Referral commission", "[[FOUNDER DECISION]] then [[LEGAL REVIEW REQUIRED]]"),
    ])
    C.acceptance(d, 12, [
        "Partner wholesale, monthly: R6,999/mo",
        "Partner wholesale, annual: R69,990/yr",
        "30-day onboarding plan starting [[DATE]] with first client [[FIRST CLIENT]]",
        "Co-marketing activities: [[LIST]]",
        "Referral programme (once commission terms are published)",
    ], client=AG, terms_num=11)
    d.save(out_path, "FluxMuse proposal: Agency partner", "Flux_Partner programme proposal template")
    return d
