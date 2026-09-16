"""Template 3: Flux_Partner (agency partner) proposal."""
from fmdoc import FMDoc
import common as C

AG = "[[AGENCY NAME]]"


def build_agency(out_path):
    d = FMDoc(client_ph=AG)
    d.cover("Flux_Partner programme proposal", "Serve more clients under your own brand",
            f"Partner proposal for {AG}", client_label="Prepared for")
    C.how_to_use(d, "Agency partner (Flux_Partner) proposal template", pilot_note=False, extra=[
        "[ ] Agencies get the permanent partner wholesale price (R5,599/mo). Never present R5,599 as a 2-month launch "
        "discount, and never add Founding Member on top.",
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
        ("Manual reporting and too many tools per client", "Full white-label, 50 client sub-accounts and reseller "
                                                          "billing on one platform, with custom and white-label reports"),
        ("Clients asking for WhatsApp commerce and AI", "Resell the AI marketing team and checkout inside WhatsApp under your own brand"),
    ], [7.0, 10.0], "Agency pains and FluxMuse answers")
    d.figure("infographics/segment-agency.png",
             "Agencies: today vs with FluxMuse.",
             "Segment card for agencies: margin squeeze, manual reporting and client demand for WhatsApp commerce, "
             "matched to wholesale pricing, white-label sub-accounts and reseller billing.")
    d.callout("Programme status", [
        "Live today on the Agency tier: full white-label, client sub-accounts, reseller billing and the partner directory.",
        "On the roadmap (indicative, not dated): the wider Flux_Partner programme, including referral tracking and "
        "partner-managed workspaces. We'll confirm dates before they're offered.",
    ])

    # 2 ----------------------------------------------------------------------------------------
    d.h1("2. What partners get")
    d.table(["Inclusion", "Detail"], [
        ("Full white-label", "Your brand on the client experience [[CONFIRM: app, reports, custom domain]]"),
        ("50 client sub-accounts", "One workspace per client, managed by your team"),
        ("Reseller billing", "Bill clients at the retail price you set"),
        ("80 channels", "WhatsApp, Facebook Pages, Messenger, email, SMS, USSD and more across your clients "
                        "(Instagram once Meta approves it)"),
        ("500,000 AI credits a month", "For Strategist, Creator, Publisher, Analyst and specialist Flux agents "
                                       "[[CONFIRM HOW CREDITS ARE SHARED ACROSS SUB-ACCOUNTS]]"),
        ("Unlimited brands", "No per-brand limit on the Agency plan"),
        ("Dedicated support", "A named contact at FluxMuse: [[NAME]]"),
        ("WhatsApp commerce for clients", "Catalog, checkout in chat, order updates and abandoned-cart recovery"),
        ("Local payments", "5 payment rails across 23 African countries"),
        ("Partner directory", "Listing so businesses can find you [[CONFIRM LISTING CRITERIA]]"),
    ], [4.6, 12.4], "Partner inclusions")

    # 3 ----------------------------------------------------------------------------------------
    d.h1("3. Partner wholesale pricing")
    d.para("Partners buy the Agency tier at **30% off list**, permanently, then set their own retail price for clients. "
           "Same inclusions as the Agency plan.")
    d.table(["Currency", "Where", "Agency list /mo", "Partner wholesale /mo", "Partner wholesale /yr"], [
        ("ZAR", "South Africa", "R7,999", "R5,599", "R55,990"),
        ("NGN", "Nigeria", "₦662,000", "₦463,000", "₦4,630,000"),
        ("KES", "Kenya", "KSh 64,499", "KSh 44,999", "KSh 449,990"),
        ("GHS", "Ghana", "GH₵ 5,439", "GH₵ 3,799", "GH₵ 37,990"),
        ("USD", "19 other rail-covered countries", "$429", "$299", "$2,990"),
    ], [2.2, 4.6, 3.2, 3.6, 3.4], "Partner wholesale pricing by currency",
        aligns=[None, None, "right", "right", "right"], highlight_rows=(0,))
    d.bullets([
        "Annual = 10× monthly (2 months free).",
        "Wholesale pricing doesn't stack with the Founding Member launch offer, which isn't offered on the Agency tier.",
        "Nigeria, Kenya and Ghana are billed in local currency; prices are reviewed quarterly.",
        "Countries without a payment rail (including Botswana and Namibia, coming soon) are waitlist only: no prices "
        "or checkout.",
        "Pass-through costs (Meta WhatsApp message fees, ad spend, SMS) are separate and can be re-billed to your clients.",
    ])

    # 4 ----------------------------------------------------------------------------------------
    d.h1("4. Partner economics")
    d.h2("Illustrative example")
    d.para("**Illustrative only, not a forecast.** A partner serving 20 clients at a retail price they set:", keep=True)
    d.table(["Line", "Illustrative (ZAR per month)"], [
        ("Clients on sub-accounts", "20"),
        ("Retail price per client (set by the partner)", "R1,500"),
        ("Retail revenue (20 × R1,500)", "R30,000"),
        ("Partner wholesale Agency plan", "− R5,599"),
        ("Gross spread before the partner's own service costs", "R24,401"),
        ("Platform cost per client (R5,599 ÷ 20)", "about R280"),
    ], [11.0, 6.0], "Illustrative partner economics", aligns=[None, "right"], total_rows=(4,))
    d.para("Before VAT, payment fees, ad spend and your team's delivery costs. Your margin depends on your retail price "
           "and costs.", size=9)
    d.figure("infographics/agency-partner-model.png",
             "How the partner model works: FluxMuse bills the partner wholesale; the partner bills clients at their own "
             "price. Example is illustrative.",
             "Partner model diagram: FluxMuse supplies the platform to the agency at the wholesale Agency tier price, "
             "the agency serves its clients on sub-accounts at a retail price it sets, with an illustrative 20-client "
             "example.")
    d.h2("Your numbers")
    d.table(["", "Line", "How to calculate", f"{AG}"], [
        ("A", "Number of clients", "Up to 50 sub-accounts", "[[ ]]"),
        ("B", "Your retail price per client /mo", "You set it", "[[R ]]"),
        ("C", "Monthly retail revenue", "A × B", "[[R ]]"),
        ("D", "Partner wholesale plan /mo", "R5,599 (or local currency)", "[[R ]]"),
        ("E", "Gross spread", "C − D", "[[R ]]"),
        ("F", "Your service costs /mo", "Team hours, design, ad management", "[[R ]]"),
        ("G", "Net contribution /mo", "E − F", "[[R ]]"),
        ("H", "Net contribution per client", "G ÷ A", "[[R ]]"),
    ], [1.0, 5.6, 6.4, 4.0], "Partner economics calculator", aligns=["center", None, None, "right"], total_rows=(6,))

    # 5 ----------------------------------------------------------------------------------------
    d.h1("5. Onboarding plan (first 30 days)")
    d.table(["Days", "Focus", "Activities", "Output"], [
        ("1–5", "Kickoff and white-label", "Partner workspace; white-label set-up (logo, colours, [[DOMAIN]]); reseller "
                                           "billing and retail price list", "Branded workspace ready"),
        ("6–10", "Team training", "AI agents; WhatsApp Embedded Signup for clients; catalog and checkout; campaigns "
                                  "with approvals; reports", "[[N]] team members trained"),
        ("11–20", "First pilot client", "Sub-account for [[PILOT CLIENT]]; WhatsApp number, catalog, payment rail, "
                                        "content calendar; baseline agreed", "First client live"),
        ("21–30", "Report and plan", "First white-label report; review with FluxMuse; plan for the next [[N]] clients",
         "Partner growth plan"),
    ], [1.6, 3.4, 8.4, 3.6], "30-day partner onboarding plan", size=9)

    # 6 ----------------------------------------------------------------------------------------
    d.h1("6. Co-marketing")
    d.table(["Activity", "FluxMuse provides", f"{AG} provides", "Status"], [
        ("Partner directory listing", "Listing and profile", "Services, areas, contact", "Live feature"),
        ("Sales materials", "Brand kit, pitch deck and proposal templates (white-label versions [[TBC]])",
         "Your branding and offer", "[[TBC]]"),
        ("Joint case study", "Case-study format and design", "First client's results and written consent", "After 60 days"),
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
        ("Messaging compliance", "Follow Meta WhatsApp Business policies: approved templates, opted-in contacts, opt-outs honoured"),
        ("Data protection", "POPIA (and NDPR/GDPR where relevant); data processing agreement [[LEGAL REVIEW REQUIRED]]"),
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
         "Promising Instagram publishing, comments or DMs before Meta approval"),
        ("Using FluxMuse brand-kit assets unmodified when co-branding", "Promising clients or investors a fixed FluxMuse margin percentage"),
        ("Quoting FluxMuse list prices from the official price table", "Offering prices or checkout in gated countries, "
                                                                        "or combining Founding Member with wholesale pricing"),
    ], [8.5, 8.5], "Brand usage rules", first_col_bold=False)

    # 10 ---------------------------------------------------------------------------------------
    d.h1("10. Trust and data protection")
    C.trust_bullets(d)
    C.popia_clause(d, client="Each end client", partner=True)

    C.terms(d, 11, extra_rows=[
        ("Wholesale pricing", "30% off Agency list for as long as the partner agreement is active [[LEGAL REVIEW REQUIRED]]"),
        ("White-label and sub-accounts", "Up to 50 client sub-accounts; client data ownership and portability on "
                                         "termination: [[LEGAL REVIEW REQUIRED]]"),
        ("Referral commission", "[[FOUNDER DECISION]] then [[LEGAL REVIEW REQUIRED]]"),
    ])
    C.acceptance(d, 12, [
        "Partner wholesale, monthly: [[R5,599 / ₦463,000 / KSh 44,999 / GH₵ 3,799 / $299]]",
        "Partner wholesale, annual: [[R55,990 / ₦4,630,000 / KSh 449,990 / GH₵ 37,990 / $2,990]]",
        "30-day onboarding plan starting [[DATE]] with first pilot client [[PILOT CLIENT]]",
        "Co-marketing activities: [[LIST]]",
        "Referral programme (once commission terms are published)",
    ], client=AG, terms_num=11)
    d.save(out_path, "FluxMuse proposal: Agency partner", "Flux_Partner programme proposal template")
    return d
