"""Sections shared by every FluxMuse proposal template. Facts: ../../08_Prospects/CURRENT_OFFER.md"""
from fmdoc import DEEP, TINT  # noqa: F401

SENDER = "Thabo Malebadi"
SENDER_EMAIL = "thabo@fluxmuse.com"

# Mirrors 08_Prospects/CURRENT_OFFER.md (1 Oct 2026). Edit here when the offer changes.
TIERS = {  # name: (monthly ZAR, annual ZAR, brands, channels, note)
    "Free": ("R0", "R0", "1", "1", "Permanent plan, not a trial"),
    "Nano": ("R149", "R1,490", "1", "3", "Entry paid plan"),
    "Micro": ("R289", "R2,890", "1", "4", "1 WhatsApp number"),
    "Starter": ("R499", "R4,990", "1", "3", ""),
    "Growth": ("R1,999", "R19,990", "3", "15", "+ inbound AI Voice (beta)"),
    "Scale": ("R4,999", "R49,990", "10", "40", "+ inbound and outbound AI Voice (beta)"),
    "Corporate": ("R6,999", "R69,990", "25", "60", "Bring your own cloud"),
    "Agency": ("R9,999", "R99,990", "Unlimited", "80", "White-label, multi-client, bring your own cloud"),
}
FOUNDING_LINE = ("Founding Member: South African sign-ups pay 30% less for their first two monthly bills. "
                 "It is a discount, not a free period.")
GUARANTEE = ("**Lead guarantee:** 3 qualified leads in your first 30 days after go-live. A qualified lead is a unique "
             "WhatsApp number that starts a conversation through a FluxMuse-tracked link or QR code. If fewer than 3 "
             "arrive and you held up your side (shared the link and posted at least weekly), we keep working with you "
             "at no extra charge until you have 3. It is extra support, not a cash payment.")
CHECKOUT_NOTE = ("Checkout through FluxMuse (Paystack, South African bank accounts) is built and being switched on: it "
                 "has not yet been tested end to end with real money. Until it is, orders arrive on your WhatsApp and "
                 "you take payment the way you do today. [[FEE WORDING ONLY ONCE CHECKOUT IS TESTED]]")


def how_to_use(d, template_name, extra=()):
    body = [
        f"This is the **{template_name}**. Fill it in, check it against the rules below, then save a PDF for the client.",
        "[ ] Replace every [[PLACEHOLDER]]: use Find for “[[”. Filled fields keep the yellow shading so a reviewer can "
        "check them; clear the shading (Home › Shading › No Colour) before sending, then search for “[[” once more.",
        "[ ] Quote prices only from 08_Prospects/CURRENT_OFFER.md. Every paid plan starts with payment: no trials, no "
        "free period. Free is a permanent plan, never a trial and never the lead offer.",
        "[ ] Founding Member is live for South African sign-ups: 30% off the first two monthly bills on Starter, Growth "
        "and Scale. No end date "
        "is set, so don't print one. Never on Agency or partner wholesale.",
        "[ ] Guarantee: only the lead guarantee, always with its conditions. Never promise cash back, sales or results.",
        "[ ] FluxMuse has no customers or results yet. No customer counts, ratings, testimonials or case-study "
        "numbers. KPI numbers are always “Target (goal)”. Describe live features as “newly launched”.",
        "[ ] Being switched on, never live: Facebook and Instagram auto-posting, checkout through FluxMuse, AI Voice "
        "(beta), daily digest, store sync. Not available: Instagram DMs and comments, checkout outside South Africa.",
        "[ ] South Africa only for paid plans. Prospects elsewhere join the waitlist: no prices, no checkout.",
        "[ ] Terms marked [[LEGAL REVIEW REQUIRED]] are completed by legal counsel. Don't write your own.",
    ]
    body += list(extra)
    body.append("[ ] Delete this box, update fields (right-click the contents list › Update Field) and check the page count.")
    d.callout("How to use this template (delete this box before sending)", body, fill="FFFBEA", accent=DEEP,
              caption="Layout: template instructions")


def status_table(d, caption="What is live and what is being switched on", extra=()):
    rows = [
        ("WhatsApp Concierge: send product photos, AI drafts the catalogue entry, you reply YES, NO or an edit",
         "Live (newly launched)"),
        ("Hosted shop link (fluxmuse.ai/s/your-name): orders arrive as a WhatsApp message to your own number",
         "Live (newly launched)"),
        ("Order alerts on WhatsApp; reply SOLD to mark an item sold", "Live (newly launched)"),
        ("AI captions and images for posts (send POST), ready to forward to WhatsApp Status", "Live (newly launched)"),
        ("Short AI video clips and voice-note transcription on WhatsApp", "Live (newly launched)"),
        ("WhatsApp Business set-up: number, profile, templates, quick replies, broadcasts to consented contacts",
         "Live (newly launched)"),
        ("Answers in your customer's language", "Live (newly launched)"),
        ("TikTok video posting", "Live (newly launched)"),
        ("Checkout through FluxMuse (Paystack, South African bank accounts)", "Being switched on"),
        ("Auto-posting to Facebook Pages and Instagram (waiting for Meta approval)", "Being switched on"),
        ("Daily digest message", "Being switched on"),
    ] + list(extra)
    d.table(["Capability", "Status"], rows, [12.4, 4.6], caption, size=9)
    d.para("**Newly launched** means built and running, but no outside business has run it end to end yet, so we watch "
           "it closely with you. **Being switched on** means it is waiting on an approval or final testing. Not "
           "available: Instagram DMs and comments, X posting, and paid checkout outside South Africa.", size=9)


def popia_clause(d, client="[[CLIENT NAME]]", heading=True, partner=False):
    if heading:
        d.h2("Protection of personal information (POPIA)")
    d.para("Fluxmuse (Pty) Ltd processes personal information in line with the Protection of Personal Information Act, "
           "2013 (POPIA). For this proposal:")
    items = [
        f"{client} decides why and how its customers' personal information is used; FluxMuse processes it to deliver "
        "the services. [[LEGAL REVIEW REQUIRED: responsible party and operator roles, operator agreement]]",
        "WhatsApp broadcasts go only to people who have opted in, and every broadcast includes a way to opt out.",
        "Platform safeguards: row-level security on database tables, encrypted access tokens, and data export and "
        "account deletion on request.",
        "Screenshots, reports and case studies shared outside the business blur customer names and phone numbers.",
        "Information Officer: [[FLUXMUSE INFORMATION OFFICER NAME AND EMAIL]]. Breach notification and cross-border "
        "processing (hosting regions): [[LEGAL REVIEW REQUIRED]]",
    ]
    if partner:
        items.insert(1, "Where [[AGENCY NAME]] manages client sub-accounts, the roles of FluxMuse, the partner and each end "
                        "client are set out in a data processing agreement. [[LEGAL REVIEW REQUIRED]]")
    d.bullets(items)


def terms(d, num, extra_rows=(), short=False):
    d.h1(f"{num}. Terms")
    d.para("These commercial headings are placeholders for the final agreement. Nothing here is binding until legal "
           "counsel has reviewed it and both parties have signed. [[LEGAL REVIEW REQUIRED]]", size=9.5)
    rows = [
        ("Agreement", "This proposal, the FluxMuse Terms of Service [[LINK]] and [[ORDER FORM / MASTER AGREEMENT]]. "
                      "Order of precedence: [[LEGAL REVIEW REQUIRED]]"),
        ("Term and renewal", "Monthly plans renew monthly. Annual plans renew yearly (annual price = 10× monthly). "
                             "Renewal and notice: [[LEGAL REVIEW REQUIRED]]"),
        ("Payment first", "Every paid plan is paid in advance, from the first month. There is no trial period. The "
                          "Free plan is a separate permanent plan."),
        ("Cancellation (per plan)", "Monthly plans: [[LEGAL REVIEW REQUIRED: notice period and effective date]]\n"
                                    "Annual plans: [[LEGAL REVIEW REQUIRED: cancellation of annual plans]]\n"
                                    "Founding Member discount on cancellation: [[LEGAL REVIEW REQUIRED]]"),
        ("Lead guarantee", "3 qualified leads in 30 days of go-live, on the conditions in this proposal; remedy is "
                           "extended support at no extra charge, not a cash payment. [[LEGAL REVIEW REQUIRED]]"),
        ("Payment terms", "Billed in advance in South African rand by [[PAYMENT METHOD: Paystack / Yoco / Ozow]]. "
                          "Late payment: [[LEGAL REVIEW REQUIRED]]"),
        ("Price changes", "Notice of price changes: [[LEGAL REVIEW REQUIRED]]"),
        ("Third-party costs", "Meta WhatsApp message fees, ad spend and payment-processing fees are pass-through "
                              "costs charged by those providers, not FluxMuse fees. Billing route: [[LEGAL REVIEW REQUIRED]]"),
        ("Third-party platforms", "Features that rely on Meta, payment providers or other platforms depend on their "
                                  "policies and approvals. [[LEGAL REVIEW REQUIRED: availability and change clause]]"),
        ("Data protection", "POPIA, as described in this proposal. Operator or data processing agreement: "
                            "[[LEGAL REVIEW REQUIRED]]"),
        ("Intellectual property", "[[LEGAL REVIEW REQUIRED: ownership of client content, AI-generated content, "
                                  "brand assets, platform IP and licences]]"),
    ]
    if not short:
        rows += [
            ("Confidentiality", "[[LEGAL REVIEW REQUIRED]]"),
            ("Support and service levels", "Support channel by plan: [[CONFIRM]]. "
                                           "Service levels: [[LEGAL REVIEW REQUIRED]]"),
        ]
    rows += list(extra_rows)
    rows += [
        ("Limitation of liability", "Liability cap: [[LEGAL REVIEW REQUIRED: cap amount and basis]]. "
                                    "Exclusions: [[LEGAL REVIEW REQUIRED]]"),
        ("Governing law and disputes", "[[LEGAL REVIEW REQUIRED]]"),
    ]
    d.table(["Heading", "Position"], rows, [4.6, 12.4], "Commercial terms placeholders", size=9)


def acceptance(d, num, choices, client="[[CLIENT NAME]]", intro=None, terms_num=None):
    d.h1(f"{num}. Acceptance")
    d.para(intro or f"To go ahead, tick your choices, sign below and send a copy to thabo@fluxmuse.com or WhatsApp "
                    f"[[PHONE / WHATSAPP]] before [[DATE + 30 days]].", keep=True)
    d.checklist(choices, keep=True)
    ref = f" in section {terms_num}" if terms_num else ""
    d.para(f"By signing, {client} accepts proposal [[FM-PRO-YYYY-###]] on the choices ticked above, subject to the "
           f"final terms{ref} once legal review is complete. [[LEGAL REVIEW REQUIRED]]", size=9.5, before=6, keep=True)
    d.signature_block(f"For {client}", "For Fluxmuse (Pty) Ltd")


def trust_bullets(d):
    d.bullets([
        "**Fluxmuse (Pty) Ltd** (South Africa): a verified Meta Tech Provider (business and access verification, "
        "September 2026).",
        "**Meta permissions approved:** WhatsApp Business messaging and management, and Facebook Page messaging.",
        "**Waiting for Meta approval (not live):** posting to Facebook Pages and Instagram, and Instagram comments and "
        "DMs. They are switched on only once Meta approves them.",
        "**Payments:** Paystack is live in South Africa. Yoco and Ozow run FluxMuse's own subscription billing.",
        "**WhatsApp policy:** broadcasts use Meta-approved message templates and go only to contacts who opted in.",
    ])
