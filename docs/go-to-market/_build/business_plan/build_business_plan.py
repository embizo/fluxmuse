"""Build FluxMuse_Business_Plan.docx into docs/go-to-market/05_Business_Plan/.

    venv/bin/python docs/go-to-market/_build/business_plan/build_business_plan.py

Run derive_model_tables.py first if the financial model has changed. Then qa_business_plan.py.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from bp_doc import DEEP, DOC_DATE, GTM, M, TINT, VERSION, BPDoc  # noqa: E402
import bp_s1, bp_s2, bp_s3, bp_s4, bp_s5  # noqa: E402

OUT = GTM / "05_Business_Plan"
NAME = "FluxMuse_Business_Plan.docx"

SECTIONS = [
    ("1. Executive summary", bp_s1.s1_executive_summary),
    ("2. Company overview", bp_s1.s2_company_overview),
    ("3. Problem and opportunity", bp_s1.s3_problem),
    ("4. Solution: products and services", bp_s1.s4_solution),
    ("5. Market analysis", bp_s2.s5_market),
    ("6. Target customers", bp_s2.s6_customers),
    ("7. Competitive landscape", bp_s2.s7_competition),
    ("8. Marketing and sales strategy", bp_s2.s8_gtm),
    ("9. Pricing strategy", bp_s3.s9_pricing),
    ("10. Operations", bp_s3.s10_operations),
    ("11. Management and organisation", bp_s3.s11_management),
    ("12. Financial plan", bp_s4.s12_financials),
    ("13. Funding request and use of funds", bp_s4.s13_funding),
    ("14. Risk analysis", bp_s5.s14_risks),
    ("15. Milestones and KPIs", bp_s5.s15_milestones),
    ("16. Social and economic impact", bp_s5.s16_impact),
]
APPENDICES = [
    "Appendix A. Pricing tables",
    "Appendix B. Payment rails and country coverage",
    "Appendix C. Gauteng pilot and case-study template",
    "Appendix D. Detailed financial tables",
    "Appendix E. Model assumptions and open confirmations",
    "Appendix F. Glossary",
]


def document_control(d):
    d.h1("Document control and disclaimer")
    d.kv_table([
        ("Document", "FluxMuse Business Plan"),
        ("Version", f"{VERSION} · {DOC_DATE}"),
        ("Status", "Draft for founder review. Contains [[PLACEHOLDERS]] that must be completed"),
        ("Prepared by", "[[FOUNDER NAME, TITLE]], Fluxmuse Pty Ltd"),
        ("Approved by", "[[APPROVER NAME AND DATE]]"),
        ("Financial model", "FluxMuse Financial Model v2, model date 11 September 2026, Base case selected"),
        ("Distribution", "Confidential. [[RECIPIENT]] only"),
    ], widths=(4.4, 12.6), caption="Layout: document control")

    d.h2("Forward-looking statements")
    d.para("This plan contains forward-looking statements: projections of revenue, costs, cash, headcount, "
           "market launches and customer numbers. **They are projections, not results, and not a promise of "
           "performance.** Every financial figure is drawn from the FluxMuse Financial Model v2 (Base case "
           "unless stated). The model's assumptions are listed in Appendix E and will be replaced with "
           "measured data as the Gauteng pilot and the South African launch produce it. Actual outcomes will "
           "differ, potentially materially, because of demand, competition, exchange rates, platform policy "
           "decisions by Meta, payment-provider performance, regulation and execution.")

    d.h2("What this plan does not claim")
    d.bullets([
        "**No customer results.** The Gauteng pilot runs to 30 November 2026. There are no customer counts, "
        "ratings, testimonials or outcome figures anywhere in this document, and none will be used until "
        "consented pilot data exists from December 2026.",
        "**No unapproved capability.** Features in Meta App Review, including Instagram publishing, comments "
        "and DMs, are identified as pending and are never described as live.",
        "**No invented market data.** Market-size figures are labelled as estimates with their sources, and "
        "must be re-verified before external use.",
        "**No valuation or return projection.** Instrument, valuation and terms are for negotiation.",
    ])
    d.para("Market estimates are attributed to their sources in section 5. Third-party names, including Meta, "
           "WhatsApp and the payment providers, are used descriptively and remain the property of their "
           "owners. Nothing in this plan is an offer of securities; any investment would be made on separate, "
           "legally reviewed terms. **[[LEGAL REVIEW OF THIS DISCLAIMER]]**")
    d.page_break()


def contents(d):
    d.toc()
    d.para("If the list above is empty, the static contents below applies.", size=8.5, color="5B6570",
           italic=True, after=6)
    d.h2("Contents (static fallback)")
    for title, _ in SECTIONS:
        d.para(title, size=10, after=1)
    for title in APPENDICES:
        d.para(title, size=10, after=1)
    d.page_break()


def build(path=None):
    d = BPDoc()
    d.cover_page()
    document_control(d)
    contents(d)
    for i, (_, fn) in enumerate(SECTIONS):
        fn(d)
    bp_s5.appendices(d)
    out = Path(path or (OUT / NAME))
    out.parent.mkdir(parents=True, exist_ok=True)
    d.doc.core_properties.keywords = "FluxMuse, business plan, seed, R25M, Fluxmuse Pty Ltd"
    d.save(out, "FluxMuse Business Plan", "Business plan supporting a R25M seed raise, Fluxmuse Pty Ltd")
    return d


def main():
    d = build()
    manifest = {"file": NAME, "version": VERSION, "model": M["version"], "model_date": M["model_date"],
                "images": sorted(set(d.images_used)), "figures": d.fig_n, "tables": d.tab_n,
                "h1_sections": d.h1s}
    (HERE / "build_manifest.json").write_text(json.dumps(manifest, indent=2))
    print(f"built {NAME}: {d.fig_n} figures, {d.tab_n} data tables, {len(d.h1s)} H1 sections")
    print("images:", len(manifest["images"]))


if __name__ == "__main__":
    main()
