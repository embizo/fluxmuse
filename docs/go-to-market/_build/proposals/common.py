"""Sections shared by every FluxMuse proposal template. Facts: ../../00_FACTS_AND_ASSUMPTIONS.md"""
from fmdoc import DEEP, TINT

RAILS_LINE = "All five payment rails live September 2026 (pawaPay and Fincra from the week of 14 September)."


def how_to_use(d, template_name, extra=(), pilot_note=True):
    body = [
        f"This is the **{template_name}**. Fill it in, check it against the rules below, then save a PDF for the client.",
        "[ ] Replace every [[PLACEHOLDER]]: use Find for “[[”. Filled fields keep the yellow shading so a reviewer can "
        "check them; clear the shading (Home › Shading › No Colour) before sending, then search for “[[” once more.",
        "[ ] Quote prices only from the facts file (00_FACTS_AND_ASSUMPTIONS.md). Founding Member prices (Starter R349, "
        "Growth R1,399, Scale R3,499 for the first 2 monthly bills) apply to South African sign-ups from "
        "1 December 2026 to 31 January 2027; in Nigeria, Kenya and Ghana the same 30% applies in the first 60 days "
        "after each country's launch. Never on the Agency tier. Say “Founding Member badge and priority support” "
        "with no duration.",
    ]
    if pilot_note:
        body.append("[ ] Gauteng pilot brands get pilot prices instead: Starter R249, Growth R999, Scale R2,499, Agency R3,999 "
                    "for the first 2 monthly bills from 1 December 2026. Delete the offer that doesn't apply.")
    body += [
        "[ ] KPI numbers are always “Target (goal)”, never results. No customer counts, ratings, testimonials or pilot "
        "results until consented pilot data exists (from December 2026).",
        "[ ] Instagram publishing, comments and DMs are pending Meta approval (in App Review). Never promise them as live.",
        "[ ] Quote prices only to businesses in the 23 rail-covered countries. Everyone else, including Botswana and "
        "Namibia (coming soon), joins the waitlist: no prices, no checkout.",
        "[ ] Terms marked [[LEGAL REVIEW REQUIRED]] are completed by legal counsel. Don't write your own.",
    ]
    body += list(extra)
    body.append("[ ] Delete this box, update fields (right-click the contents list › Update Field) and check the page count.")
    d.callout("How to use this template (delete this box before sending)", body, fill="FFFBEA", accent=DEEP,
              caption="Layout: template instructions")


def popia_clause(d, client="[[CLIENT NAME]]", heading=True, partner=False):
    if heading:
        d.h2("Protection of personal information (POPIA)")
    d.para("Fluxmuse Pty Ltd processes personal information in line with the Protection of Personal Information Act, "
           "2013 (POPIA), and the platform is built to be POPIA, NDPR and GDPR ready. For this proposal:")
    items = [
        f"{client} decides why and how its customers' personal information is used; FluxMuse processes it to deliver "
        "the services. [[LEGAL REVIEW REQUIRED: responsible party and operator roles, operator agreement]]",
        "Marketing messages on WhatsApp, SMS and email go only to people who have opted in, and every broadcast "
        "includes a way to opt out. Email suppression lists are kept in FluxMuse.",
        "Platform safeguards: row-level security on every database table, encrypted access tokens, audit export, "
        "and data export and account deletion on request.",
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
        ("Free trial", "14-day free trial, no card required. Conversion to a paid plan: [[LEGAL REVIEW REQUIRED]]"),
        ("Cancellation (per plan)", "Monthly plans: [[LEGAL REVIEW REQUIRED: notice period and effective date]]\n"
                                    "Annual plans: [[LEGAL REVIEW REQUIRED: refunds or pro-rating]]\n"
                                    "Launch or pilot pricing on cancellation: [[LEGAL REVIEW REQUIRED]]"),
        ("Payment terms", "Billed in advance in [[CURRENCY]] by [[PAYMENT METHOD]], due [[N]] days from invoice. "
                          "Late payment: [[LEGAL REVIEW REQUIRED]]"),
        ("Price changes", "Notice of price changes: [[LEGAL REVIEW REQUIRED]]. Local-currency prices in Nigeria, Kenya "
                          "and Ghana are reviewed quarterly."),
        ("Third-party costs", "Meta WhatsApp message fees, ad spend, SMS and payment-processing fees are pass-through "
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
            ("Support and service levels", "Support channel by plan (community, email, priority or dedicated). "
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
    d.para(intro or f"To go ahead, tick your choices, sign below and send a copy to [[EMAIL]] or WhatsApp "
                    f"[[PHONE / WHATSAPP]] before [[DATE + 30 days]].", keep=True)
    d.checklist(choices, keep=True)
    ref = f" in section {terms_num}" if terms_num else ""
    d.para(f"By signing, {client} accepts proposal [[FM-PRO-YYYY-###]] on the choices ticked above, subject to the "
           f"final terms{ref} once legal review is complete. [[LEGAL REVIEW REQUIRED]]", size=9.5, before=6, keep=True)
    d.signature_block(f"For {client}", "For Fluxmuse Pty Ltd")


def trust_bullets(d):
    d.bullets([
        "**Fluxmuse Pty Ltd** (South Africa): Meta Business Verification: Verified. Meta Access Verification: "
        "Verified (Tech Provider).",
        "**Meta permissions approved:** pages_show_list, pages_manage_metadata, pages_messaging, "
        "whatsapp_business_messaging, whatsapp_business_management, public_profile.",
        "**Pending Meta approval (in App Review, not live yet):** pages_manage_posts, pages_read_engagement, instagram_basic, "
        "instagram_content_publish, instagram_manage_comments, instagram_manage_messages, business_management. "
        "Instagram features are switched on only once Meta approves them.",
        "**Data protection:** POPIA, NDPR and GDPR ready; row-level security on every table; encrypted tokens; audit "
        "export; data export and account deletion.",
        "**WhatsApp policy:** broadcasts use Meta-approved message templates and go only to contacts who opted in.",
    ])
