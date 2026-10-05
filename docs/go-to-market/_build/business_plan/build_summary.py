"""Write 05_Business_Plan/Business_Plan_Summary.md from model_summary.json (no hand-typed model figures).

    python3 docs/go-to-market/_build/business_plan/build_summary.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from bp_doc import ANN, D, GTM, M, MODEL_LINE, SEED_M, SEED_WORDS, pct, rand, rm, usd  # noqa: E402

C, SC, PT, UE = M["cash"], M["scenarios"], M["price_tables"], M["unit_economics_fy3"]
Z, PW, FG, FCS = PT["zar_list_monthly"], PT["partner_wholesale_monthly"], M["first_group"], M["free_conversion_sensitivity"]
PASS = M["profitable_on_seed_alone"]


def row(label, vals):
    return f"| {label} | " + " | ".join(vals) + " |"


def main():
    al = M["use_of_funds"]["allocation"]
    lines = [
        "# FluxMuse business plan: executive summary",
        "",
        f"**Fluxmuse (Pty) Ltd · October 2026 · Confidential · v2.0** Projections from the {MODEL_LINE} (Base "
        "case). Forward-looking projections, not results. FluxMuse has **no paying customers yet**; every volume "
        "is an assumption, and items marked `[[CONFIRM]]` need founder sign-off. Sources: "
        "`00_FACTS_AND_ASSUMPTIONS.md`, `08_Prospects/CURRENT_OFFER.md`, `06_Financial_Model/Financial_Model_Notes.md`.",
        "",
        "## What FluxMuse is",
        "",
        "An AI marketing team and a shop that runs on WhatsApp, for African small businesses. The owner sends "
        "product photos on WhatsApp; FluxMuse drafts the catalogue, builds a hosted shop link, writes captions "
        "and images for WhatsApp Status, and sends each order to the owner's WhatsApp. Fluxmuse (Pty) Ltd is a "
        "verified Meta Tech Provider.",
        "",
        "## Where we are",
        "",
        "- **Live, newly launched in South Africa:** WhatsApp Concierge, hosted shop link, order alerts and SOLD, "
        "AI captions, images and short video, voice-note transcription, WhatsApp Business setup and consented "
        "broadcasts, answers in the customer's language, TikTok video posting.",
        "- **Being switched on:** Facebook and Instagram auto-publishing (Meta permissions pending), checkout "
        "through FluxMuse (not yet tested with real money), AI Voice (beta), daily digest.",
        "- **Payments:** Paystack live in South Africa; Yoco and Ozow for FluxMuse's own billing. pawaPay and "
        "Fincra contracted for expansion, accounts pending. No paid checkout outside South Africa yet.",
        "- **No customers, no pilot, no results.** We are opening with a small first group of businesses and "
        f"setting each one up by hand (model: {FG['per_month']} a month, {FG['months'].replace(' - ', ' to ')} "
        "`[[CONFIRM]]`).",
        "- **Lead guarantee:** 3 qualified leads in 30 days of go-live, or extended support at no extra charge "
        "until 3 arrive (conditions apply). Support, not cash.",
        "",
        "## Pricing",
        "",
        f"Nine plans in three bands, in rands: Small (Free, Nano {rand(Z['Nano'])}, Micro {rand(Z['Micro'])}), "
        f"Medium (Starter {rand(Z['Starter'])}, Growth {rand(Z['Growth'])}, Scale {rand(Z['Scale'])}), Enterprise "
        f"(Corporate {rand(Z['Corporate'])}, Agency {rand(Z['Agency'])}, Custom by consultation). Annual is 10× "
        "monthly. Every paid plan starts with payment; Free is a permanent plan. Partner wholesale "
        f"{rand(PW['ZAR'])} a month. Founding Member: 30% off the first two monthly bills for South African "
        "sign-ups, live now. Nigeria, Kenya and Ghana are priced but not on sale.",
        "",
        "## Financial highlights (Base case)",
        "",
        "| | FY1 | FY2 | FY3 | FY4 | FY5 |",
        "|---|---|---|---|---|---|",
        row("Revenue", [rm(a["total_revenue_zar"]) for a in ANN]),
        row("EBITDA", [rm(a["ebitda_zar"]) for a in ANN]),
        row("Paying workspaces (Sept)", [f"{a['ending_paying_workspaces']:,}" for a in ANN]),
        row("Closing cash", [rm(a["closing_cash_zar"]) for a in ANN]),
        row("Headcount at year end", [str(v) for v in D["headcount_total_fy_end"]]),
        "",
        f"- **EBITDA break-even {C['break_even_month']}**; operating cash flow positive from "
        f"{C['cash_flow_positive_month']}.",
        f"- **Minimum cash after the seed {rm(C['min_post_seed_cash_zar'], 2)} ({C['min_post_seed_cash_month']})**, "
        f"only {rm(C['headroom_over_buffer_zar'], 2)} above the {rm(C['min_cash_buffer_zar'], 1)} buffer. No "
        "Series A in the Base case.",
        f"- **Scenarios on {SEED_M}:** Base {'passes' if PASS['Base'] else 'fails'}, Upside "
        f"{'passes' if PASS['Upside'] else 'fails'}. **The Conservative case fails**: cash below the buffer from "
        f"{SC['Conservative']['first_month_below_buffer']}, no EBITDA break-even by Sep 2031.",
        f"- **The headroom is thin:** Free upgrades at 0.25% a month instead of 0.5% take minimum cash to "
        f"{rm(FCS['0.25% a month']['min_post_seed_cash_zar'], 2)}.",
        f"- FY3 unit economics: blended LTV:CAC {UE['blended']['ltv_to_cac']}×, payback "
        f"{UE['blended']['cac_payback_months']} months. Solo does not pay back on fully loaded CAC "
        f"({UE['by_segment']['Solo']['ltv_to_cac']}×).",
        "",
        f"## The ask: {SEED_WORDS} seed",
        "",
        f"About {usd(M['seed_usd'])}, modelled to close {C['seed_month']} `[[CONFIRM]]`. "
        f"{rm(M['seed_sizing']['smallest_passing_seed_zar_base'], 1)} is the smallest seed at which the Base case "
        f"passes; {SEED_M} rounds it up. Instrument and valuation `[[TBC]]`. Pre-seed bridge "
        f"{rand(C['pre_seed_bridge_required_zar'])} `[[CONFIRM]]`.",
        "",
        "| Use of funds | Share | Amount |",
        "|---|---|---|",
    ] + [f"| {a['category']} | {a['share_pct']}% | {rm(a['amount_zar'], 1)} |" for a in al] + [
        "",
        "Full plan: `FluxMuse_Business_Plan.docx`. Contact: Thabo Malebadi, thabo@fluxmuse.com.",
        "",
    ]
    (GTM / "05_Business_Plan" / "Business_Plan_Summary.md").write_text("\n".join(lines))
    print("wrote Business_Plan_Summary.md")


if __name__ == "__main__":
    main()
