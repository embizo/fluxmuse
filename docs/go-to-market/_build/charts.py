#!/usr/bin/env python3
"""Render FluxMuse financial-model charts (v2) from 06_Financial_Model/model_summary.json.

Each chart is exported four ways into docs/go-to-market/assets/charts/:
  <name>.png            2x resolution (2000 x 1250), white background
  <name>_dark.png       2x resolution, Night (#0F1419) background
  <name>_16x9.png       1920 x 1080 for slides, white background
  <name>_16x9_dark.png  1920 x 1080 for slides, Night background

Palette checked with the dataviz validator (light: orange, blue, green, violet, teal; dark: violet
lifted to #9B6BE0 and orange stepped to #EB6000 to sit inside the dark lightness band). Categorical order is fixed per entity so a market/segment
keeps its colour on every chart. No dual axes: paired measures use separate panels.
"""
import json
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib import font_manager  # noqa: E402
from matplotlib.patches import Circle, FancyBboxPatch  # noqa: E402
from matplotlib.ticker import FuncFormatter  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
GTM = os.path.dirname(HERE)
SRC = os.path.join(GTM, "06_Financial_Model", "model_summary.json")
OUT = os.path.join(GTM, "assets", "charts")

_installed = {f.name for f in font_manager.fontManager.ttflist}
FONT = next((f for f in ["Poppins", "Inter", "Helvetica", "Arial"] if f in _installed), "DejaVu Sans")

THEMES = {
    "light": dict(bg="#FFFFFF", ink="#0F1419", muted="#5F6B73", grid="#E6E8EB", orange="#FF6A00", slate="#37474F",
                  blue="#1E88E5", green="#43A047", violet="#6A2DC8", teal="#00A6A6", tint="#FFE3CC", tint2="#ECEFF1",
                  on_orange="#FFFFFF", neg="#37474F"),
    "dark": dict(bg="#0F1419", ink="#F3F4F6", muted="#A7B0B8", grid="#273038", orange="#EB6000", slate="#90A4AE",
                 blue="#1E88E5", green="#43A047", violet="#9B6BE0", teal="#00A6A6", tint="#4A2A12", tint2="#1F2A33",
                 on_orange="#0F1419", neg="#90A4AE"),
}
SIZES = {"": (10.0, 6.25, 200), "_16x9": (9.6, 5.4, 200)}
FOOT = "Source: FluxMuse Financial Model v2 (Base case, R25M seed), 11 Sep 2026. Forward-looking projections; assumptions to be validated with pilot data."
FY = ["FY1", "FY2", "FY3", "FY4", "FY5"]
FY_SUB = ["Oct 26-Sep 27", "Oct 27-Sep 28", "Oct 28-Sep 29", "Oct 29-Sep 30", "Oct 30-Sep 31"]
MARKET_COLOURS = [("South Africa", "orange"), ("Nigeria", "green"), ("Kenya", "blue"), ("Ghana", "violet"),
                  ("Rest of Africa (USD)", "teal"), ("Botswana & Namibia", "slate")]
SEGMENT_COLOURS = [("Solo", "orange"), ("SMEs", "blue"), ("Agencies", "green"), ("Enterprise", "violet")]


def rm(x):
    return x / 1e6


def fmt_rm(zar, nd=1):
    x = zar / 1e6
    s = f"{abs(x):,.{nd}f}"
    return f"-R{s}m" if x < 0 else f"R{s}m"


def fmt_rk(zar):
    return f"R{zar / 1e3:,.0f}k"


def style_axes(ax, T, grid_axis="y"):
    ax.set_facecolor(T["bg"])
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(T["grid"])
    ax.tick_params(colors=T["muted"], labelsize=10, length=0)
    if grid_axis:
        ax.grid(axis=grid_axis, color=T["grid"], linewidth=0.8)
        ax.set_axisbelow(True)


def header(fig, T, title, subtitle, top=0.95):
    fig.text(0.04, top, title, fontsize=17, fontweight="bold", color=T["ink"], ha="left", va="top")
    fig.text(0.04, top - 0.055, subtitle, fontsize=10.5, color=T["muted"], ha="left", va="top")


def footer(fig, T, text=FOOT):
    fig.text(0.04, 0.025, text, fontsize=8, color=T["muted"], ha="left", va="bottom")


def legend_row(fig, T, items, y, x0=0.04):
    x = x0
    for label, colour in items:
        fig.patches.append(FancyBboxPatch((x, y - 0.012), 0.014, 0.024, boxstyle="round,pad=0,rounding_size=0.003",
                                          transform=fig.transFigure, facecolor=colour, edgecolor="none"))
        t = fig.text(x + 0.02, y, label, fontsize=10, color=T["ink"], va="center", ha="left")
        fig.canvas.draw()
        bb = t.get_window_extent().transformed(fig.transFigure.inverted())
        x = bb.x1 + 0.025


def spread(vals, gap):
    """Push label positions apart (keeps order) so direct labels do not collide."""
    order = sorted(range(len(vals)), key=lambda i: vals[i])
    out = list(vals)
    prev = None
    for i in order:
        if prev is not None and out[i] < out[prev] + gap:
            out[i] = out[prev] + gap
        prev = i
    return out


def save(fig, name, suffix, theme, T):
    path = os.path.join(OUT, f"{name}{suffix}{'_dark' if theme == 'dark' else ''}.png")
    fig.savefig(path, facecolor=T["bg"], transparent=False)
    plt.close(fig)
    return path


def new_fig(T, suffix):
    w, h, dpi = SIZES[suffix]
    return plt.figure(figsize=(w, h), dpi=dpi, facecolor=T["bg"])


def month_ticks(ax, labels, n, T, every=6):
    ticks = list(range(0, n, every))
    ax.set_xticks(ticks)
    ax.set_xticklabels([labels[t] for t in ticks], color=T["ink"])


# ---------------------------------------------------------------------------
def chart_revenue(D, T, suffix):
    ann = D["annual"]
    streams = [("Subscriptions (net)", ["subscriptions"], T["orange"]), ("AI-credit top-ups", ["ai_credit_topups"], T["blue"]),
               ("WhatsApp messaging", ["whatsapp_messaging"], T["green"]), ("Commerce fees", ["commerce_platform_fees"], T["violet"]),
               ("Setup fees", ["enterprise_setup_fees", "agency_setup_fees"], T["teal"])]
    streams = [s for s in streams if any(a["revenue_by_stream_zar"][k] for a in ann for k in s[1])]
    fig = new_fig(T, suffix)
    header(fig, T, "Revenue by stream, FY1-FY5",
           f"Base case, R million, net of launch discounts. FY5 total {fmt_rm(ann[4]['total_revenue_zar'])} (≈US${ann[4]['total_revenue_usd'] / 1e6:,.1f}m); no commerce fee in Base")
    legend_row(fig, T, [(s[0], s[2]) for s in streams], 0.80)
    ax = fig.add_axes([0.08, 0.13, 0.88, 0.60])
    style_axes(ax, T)
    bottom = [0.0] * 5
    for label, keys, colour in streams:
        vals = [rm(sum(a["revenue_by_stream_zar"][k] for k in keys)) for a in ann]
        ax.bar(range(5), vals, 0.55, bottom=bottom, color=colour, edgecolor=T["bg"], linewidth=1.2)
        bottom = [b + v for b, v in zip(bottom, vals)]
    for i, tot in enumerate(bottom):
        ax.text(i, tot + max(bottom) * 0.015, fmt_rm(tot * 1e6), ha="center", va="bottom", fontsize=11, fontweight="bold", color=T["ink"])
    ax.set_xticks(range(5))
    ax.set_xticklabels([f"{a}\n{b}" for a, b in zip(FY, FY_SUB)], color=T["ink"])
    ax.set_ylim(0, max(bottom) * 1.12)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"R{v:,.0f}m"))
    footer(fig, T)
    return fig


def chart_arr_customers(D, T, suffix):
    ann = D["annual"]
    fig = new_fig(T, suffix)
    header(fig, T, "Subscription ARR and paying workspaces", "Base case, end of each fiscal year (September). ARR = September net subscription MRR x 12")
    panels = [("Subscription ARR (R million)", [rm(a["subscription_arr_zar"]) for a in ann], T["orange"], lambda v: f"R{v:,.0f}m" if v >= 10 else f"R{v:,.1f}m"),
              ("Paying workspaces", [a["ending_paying_workspaces"] for a in ann], T["slate"], lambda v: f"{v:,.0f}")]
    for k, (title, vals, colour, lab) in enumerate(panels):
        ax = fig.add_axes([0.06 + k * 0.48, 0.13, 0.42, 0.62])
        style_axes(ax, T, grid_axis=None)
        ax.bar(range(5), vals, 0.55, color=colour)
        for i, v in enumerate(vals):
            ax.text(i, v + max(vals) * 0.015, lab(v), ha="center", va="bottom", fontsize=10.5, fontweight="bold", color=T["ink"])
        ax.set_xticks(range(5))
        ax.set_xticklabels(FY, color=T["ink"])
        ax.set_ylim(0, max(vals) * 1.14)
        ax.set_yticks([])
        ax.set_title(title, loc="left", fontsize=12, color=T["ink"], fontweight="bold", pad=10)
    footer(fig, T)
    return fig


def chart_ebitda_cash(D, T, suffix):
    mb = D["monthly_base"]
    labels = mb["labels"]
    mk = mb["markers"]
    e = [rm(v) for v in mb["ebitda_zar"]]
    cash = [rm(v) for v in mb["closing_cash_zar"]]
    c = D["cash"]
    be_idx = mk["breakeven_month_index"]
    tr_idx = mk["min_post_seed_cash_month_index"]
    seed_idx = mk["seed_month_index"]
    buf = D["min_cash_buffer_zar"] / 1e6
    fig = new_fig(T, suffix)
    ok = D["profitable_on_seed_alone"]["Base"]
    header(fig, T, "Monthly EBITDA and closing cash",
           f"Base case, R million. Seed lands {c['seed_month']}; break-even {c['break_even_month']}; "
           + ("cash stays above the R3.0m buffer" if ok else "cash breaches the R3.0m buffer"))
    ax1 = fig.add_axes([0.08, 0.50, 0.88, 0.28])
    ax2 = fig.add_axes([0.08, 0.12, 0.88, 0.30], sharex=ax1)
    style_axes(ax1, T)
    style_axes(ax2, T)
    ax1.bar(range(60), e, 0.72, color=[T["orange"] if v >= 0 else T["neg"] for v in e])
    ax1.axhline(0, color=T["muted"], linewidth=0.8)
    ax1.set_title("EBITDA (R m per month)", loc="left", fontsize=11, color=T["ink"], fontweight="bold")
    ax1.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"R{v:,.0f}m"))
    ax2.plot(range(60), cash, color=T["orange"], linewidth=2.2, solid_capstyle="round")
    ax2.fill_between(range(60), cash, 0, color=T["orange"], alpha=0.10, linewidth=0)
    ax2.hlines(buf, seed_idx, 59, colors=T["muted"], linestyles=(0, (4, 3)), linewidth=1.1)
    ax2.text(59, buf + max(cash) * 0.03, "R3.0m buffer", ha="right", va="bottom", fontsize=9, color=T["muted"])
    ax2.set_title("Closing cash (R m)", loc="left", fontsize=11, color=T["ink"], fontweight="bold")
    ax2.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"R{v:,.0f}m"))
    ax2.set_ylim(min(0, min(cash)) - max(cash) * 0.05, max(cash) * 1.15)
    ax2.scatter([tr_idx], [cash[tr_idx]], s=46, color=T["orange"], edgecolor=T["bg"], linewidth=2, zorder=5)
    ax2.annotate(f"Post-seed low {fmt_rm(c['min_post_seed_cash_zar'], 2)}\n{c['min_post_seed_cash_month']}",
                 xy=(tr_idx, cash[tr_idx]), xytext=(tr_idx + 3, max(cash) * 0.45), fontsize=9.5, color=T["ink"],
                 arrowprops=dict(arrowstyle="-", color=T["muted"], linewidth=0.8))
    ax2.annotate(f"FY5 close {fmt_rm(cash[-1] * 1e6, 0)}", xy=(59, cash[-1]), xytext=(55, cash[-1] * 0.92),
                 fontsize=9.5, color=T["ink"], ha="right", va="top")
    if be_idx is not None:
        for ax in (ax1, ax2):
            ax.axvline(be_idx, color=T["muted"], linewidth=1)
        ax1.text(be_idx - 0.8, max(e) * 0.9, f"Break-even\n{c['break_even_month']}", fontsize=9.5, color=T["ink"], va="top", ha="right")
    ticks = list(range(0, 60, 12))
    ax2.set_xticks(ticks)
    ax2.set_xticklabels([f"{labels[t]}\n{FY[k]}" for k, t in enumerate(ticks)], color=T["ink"])
    plt.setp(ax1.get_xticklabels(), visible=False)
    ax1.set_xlim(-1, 60)
    footer(fig, T)
    return fig


def _stack_with_labels(fig, T, ax, series, n, end_vals, fmt=lambda v: f"{v:,.0f}"):
    ys = [s[1][:n] for s in series]
    ax.stackplot(range(n), ys, colors=[s[2] for s in series], edgecolor=T["bg"], linewidth=0.8)
    total = sum(y[-1] for y in ys)
    mids, cum = [], 0
    for y in ys:
        mids.append(cum + y[-1] / 2)
        cum += y[-1]
    pos = spread(mids, total * 0.075)
    for (name, _, _), mid, p, v in zip(series, mids, pos, end_vals):
        ax.annotate(f"{name}  {fmt(v)}", xy=(n - 1, mid), xytext=(n + 1.5, p), fontsize=9.5, color=T["ink"], va="center",
                    annotation_clip=False, arrowprops=dict(arrowstyle="-", color=T["muted"], linewidth=0.6))


def chart_markets(D, T, suffix):
    mb = D["monthly_base"]
    by = mb["paying_workspaces_by_market"]
    end = D["annual"][4]["ending_customers_by_market"]
    tot = D["annual"][4]["ending_paying_workspaces"]
    series = [(n, by[n], T[c]) for n, c in MARKET_COLOURS if max(by[n]) > 0]
    fig = new_fig(T, suffix)
    header(fig, T, "Paying workspaces by market",
           f"Base case, monthly. {tot:,} by Sep 2031; {100 - end['South Africa'] / tot * 100:.0f}% outside South Africa. Botswana & Namibia off; gated countries zero")
    legend_row(fig, T, [(s[0], s[2]) for s in series], 0.80)
    ax = fig.add_axes([0.08, 0.13, 0.66, 0.60])
    style_axes(ax, T)
    _stack_with_labels(fig, T, ax, series, 60, [end[s[0]] for s in series])
    month_ticks(ax, mb["labels"], 60, T, 12)
    ax.set_xlim(0, 59)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:,.0f}"))
    footer(fig, T)
    return fig


def chart_segments(D, T, suffix):
    ann = D["annual"]
    fig = new_fig(T, suffix)
    f1, f5 = ann[0]["ending_customers_by_segment"], ann[4]["ending_customers_by_segment"]
    header(fig, T, "Paying workspaces by segment, FY1-FY5",
           "Base case, end of each fiscal year. Agencies buy the Agency tier at partner wholesale (R5,599/mo); Enterprise is inbound only")
    legend_row(fig, T, [(n, T[c]) for n, c in SEGMENT_COLOURS], 0.80)
    ax = fig.add_axes([0.08, 0.13, 0.64, 0.60])
    style_axes(ax, T)
    bottom = [0.0] * 5
    for name, c in SEGMENT_COLOURS:
        vals = [a["ending_customers_by_segment"][name] for a in ann]
        ax.bar(range(5), vals, 0.55, bottom=bottom, color=T[c], edgecolor=T["bg"], linewidth=1.2)
        bottom = [b + v for b, v in zip(bottom, vals)]
    for i, tt in enumerate(bottom):
        ax.text(i, tt + max(bottom) * 0.015, f"{tt:,.0f}", ha="center", va="bottom", fontsize=10.5, fontweight="bold", color=T["ink"])
    ax.set_xticks(range(5))
    ax.set_xticklabels([f"{a}\n{b}" for a, b in zip(FY, FY_SUB)], color=T["ink"])
    ax.set_ylim(0, max(bottom) * 1.12)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:,.0f}"))
    x0 = 0.75
    fig.text(x0, 0.70, "Segment", fontsize=10, fontweight="bold", color=T["muted"])
    fig.text(x0 + 0.12, 0.70, "FY1", fontsize=10, fontweight="bold", color=T["muted"], ha="right")
    fig.text(x0 + 0.21, 0.70, "FY5", fontsize=10, fontweight="bold", color=T["muted"], ha="right")
    for k, (name, c) in enumerate(SEGMENT_COLOURS):
        y = 0.64 - k * 0.06
        fig.patches.append(FancyBboxPatch((x0, y - 0.01), 0.012, 0.02, boxstyle="round,pad=0,rounding_size=0.003",
                                          transform=fig.transFigure, facecolor=T[c], edgecolor="none"))
        fig.text(x0 + 0.018, y, name, fontsize=10, color=T["ink"], va="center")
        fig.text(x0 + 0.12, y, f"{f1[name]:,}", fontsize=10, color=T["ink"], va="center", ha="right")
        fig.text(x0 + 0.21, y, f"{f5[name]:,}", fontsize=10, color=T["ink"], va="center", ha="right")
    footer(fig, T)
    return fig


def chart_unit_econ(D, T, suffix):
    segs = D["unit_economics_fy3"]["by_segment"]
    fig = new_fig(T, suffix)
    header(fig, T, "Lifetime value vs acquisition cost by segment (FY3)",
           "R thousand per customer. LTV = ARPA x software gross margin / monthly churn. Each panel has its own scale")
    legend_row(fig, T, [("LTV", T["orange"]), ("CAC", T["slate"])], 0.80)
    names = list(segs.keys())
    for k, n in enumerate(names):
        t = segs[n]
        ax = fig.add_axes([0.06 + k * 0.235, 0.22, 0.18, 0.46])
        style_axes(ax, T, grid_axis=None)
        vals = [t["ltv_zar"] / 1e3, t["cac_zar"] / 1e3]
        ax.bar([0, 1], vals, 0.62, color=[T["orange"], T["slate"]])
        for i, v in enumerate(vals):
            ax.text(i, v + max(vals) * 0.02, f"R{v:,.0f}k" if v >= 10 else f"R{v:,.1f}k", ha="center", va="bottom", fontsize=9, color=T["ink"])
        ax.set_xticks([0, 1])
        ax.set_xticklabels(["LTV", "CAC"], color=T["muted"], fontsize=9)
        ax.set_yticks([])
        ax.set_ylim(0, max(vals) * 1.18 if max(vals) > 0 else 1)
        ax.set_title(n, fontsize=12, fontweight="bold", color=T["ink"], pad=26)
        ax.text(0.5, 1.03, f"{t['ltv_to_cac']:.1f}x LTV:CAC", transform=ax.transAxes, ha="center", fontsize=10, color=T["ink"])
        ax.text(0.5, -0.17, f"Payback {t['cac_payback_months']:.1f} mo · churn {t['monthly_churn_pct']:.1f}%/mo", transform=ax.transAxes,
                ha="center", va="top", fontsize=9, color=T["muted"])
    b = D["unit_economics_fy3"]["blended"]
    fig.text(0.04, 0.075, f"Blended FY3: LTV R{b['ltv_zar'] / 1e3:,.0f}k · CAC R{b['cac_zar'] / 1e3:,.1f}k · LTV:CAC {b['ltv_to_cac']:.1f}x · payback {b['cac_payback_months']:.1f} months",
             fontsize=10, fontweight="bold", color=T["ink"])
    footer(fig, T, "CAC: Solo/SME = paid + shared brand & marketing; Agencies = partner programme + team; Enterprise = inbound handling. Source: FluxMuse model v2.")
    return fig


def chart_use_of_funds(D, T, suffix):
    U = D["use_of_funds"]
    rec = U["reconciliation"]["24"]
    share = {c["category"]: c["share_of_spend_pct"] for c in rec["categories"]}
    rows = sorted(U["allocation"], key=lambda r: r["amount_zar"])
    fig = new_fig(T, suffix)
    header(fig, T, f"Use of funds: R{U['seed_zar'] / 1e6:,.0f}m seed",
           f"Allocation of the seed round (≈US${D['seed_usd'] / 1e6:,.2f}m). Grey: share of modelled gross spend, first 24 months after close")
    ax = fig.add_axes([0.36, 0.14, 0.50, 0.64])
    style_axes(ax, T, grid_axis=None)
    vals = [r["amount_zar"] / 1e6 for r in rows]
    ax.barh(range(len(rows)), vals, 0.55, color=T["orange"])
    for i, r in enumerate(rows):
        ax.text(vals[i] + max(vals) * 0.02, i + 0.08, f"R{vals[i]:,.2f}m  ({r['share_pct']}%)", va="bottom", fontsize=11, fontweight="bold", color=T["ink"])
        ax.text(vals[i] + max(vals) * 0.02, i - 0.05, f"{share[r['category']]:.0f}% of modelled spend", va="top", fontsize=9, color=T["muted"])
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels([r["category"].replace(" & payments compliance", "\n& payments compliance").replace(" / partner programme", "\n/ partner programme")
                        for r in rows], color=T["ink"], fontsize=10.5)
    ax.set_xticks([])
    ax.spines["bottom"].set_visible(False)
    ax.set_xlim(0, max(vals) * 1.45)
    footer(fig, T, "Source: FluxMuse Financial Model v2, Use_of_Funds sheet. Percentages per founder assumption (facts file §7).")
    return fig


def chart_scenarios(D, T, suffix):
    S = D["scenarios"]
    names = ["Conservative", "Base", "Upside"]
    fig = new_fig(T, suffix)
    header(fig, T, "Scenarios: FY5 revenue and EBITDA on the R25m seed alone",
           "R million, FY5 (Oct 2030-Sep 2031). No Series A in any scenario; hiring and launches gated on MRR")
    legend_row(fig, T, [("FY5 revenue", T["orange"]), ("FY5 EBITDA", T["slate"])], 0.80)
    ax = fig.add_axes([0.08, 0.22, 0.88, 0.51])
    style_axes(ax, T)
    rev = [rm(S[n]["fy5_revenue_zar"]) for n in names]
    eb = [rm(S[n]["fy5_ebitda_zar"]) for n in names]
    w = 0.32
    ax.bar([i - w / 2 - 0.01 for i in range(3)], rev, w, color=T["orange"])
    ax.bar([i + w / 2 + 0.01 for i in range(3)], eb, w, color=T["slate"])
    top = max(rev)
    for i in range(3):
        ax.text(i - w / 2 - 0.01, rev[i] + top * 0.015, f"R{rev[i]:,.0f}m", ha="center", va="bottom", fontsize=10.5, fontweight="bold", color=T["ink"])
        ax.text(i + w / 2 + 0.01, max(eb[i], 0) + top * 0.015, f"R{eb[i]:,.0f}m ({S[names[i]]['fy5_ebitda_margin_pct']:.0f}%)", ha="center", va="bottom", fontsize=10, color=T["ink"])
    ax.axhline(0, color=T["muted"], linewidth=0.8)
    ax.set_xticks(range(3))
    sub = []
    for n in names:
        s = S[n]
        status = "profitable on seed alone" if s["profitable_on_seed_alone"] else f"short {fmt_rm(s['shortfall_vs_buffer_zar'])} vs buffer"
        sub.append(f"{n}\n{s['fy5_paying_workspaces']:,} workspaces · break-even {s['breakeven_month_sustained']}\n"
                   f"low cash {fmt_rm(s['min_post_seed_cash_zar'])} · {status}")
    ax.set_xticklabels(sub, color=T["ink"], fontsize=9.5)
    ax.set_ylim(min(0, min(eb)) * 1.2, top * 1.12)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"R{v:,.0f}m"))
    footer(fig, T, "Source: FluxMuse Financial Model v2, 11 Sep 2026. Break-even = EBITDA >= 0 every month thereafter; low cash = minimum closing cash after the seed lands.")
    return fig


def chart_tam(D, T, suffix):
    ms = D["market_sizing"]
    fig = new_fig(T, suffix)
    header(fig, T, "Market: TAM, SAM and SOM", "Estimates; circles not to scale (TAM is ~2,500x SOM)")
    ax = fig.add_axes([0.03, 0.08, 0.50, 0.76])
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_facecolor(T["bg"])
    for rad, colour in [(1.0, T["tint2"]), (0.62, T["tint"]), (0.28, T["orange"])]:
        ax.add_patch(Circle((0, rad - 1.0), rad, facecolor=colour, edgecolor=T["bg"], linewidth=2))
    ax.text(0, 0.72, "TAM", ha="center", fontsize=13, fontweight="bold", color=T["ink"])
    ax.text(0, 0.02, "SAM", ha="center", fontsize=13, fontweight="bold", color=T["ink"])
    ax.text(0, -0.76, "SOM", ha="center", fontsize=13, fontweight="bold", color=T["on_orange"])
    ax.set_xlim(-1.05, 1.05)
    ax.set_ylim(-2.02, 1.02)
    items = [("TAM", f"{ms['tam_msmes'] / 1e6:,.0f} million", "MSMEs in Sub-Saharan Africa (IFC / World Bank est.)"),
             ("SAM", f"{ms['sam_smbs'] / 1e6:,.1f} million", "Digitally active SMBs in the 23 rail-covered countries that sell via social / WhatsApp and can pay ≥US$25/mo"),
             ("SOM", f"{ms['som_paying_workspaces']:,}", f"Paying workspaces by FY5 (~{ms['som_share_of_sam_pct']}% of SAM). Base case reaches {D['annual'][4]['ending_paying_workspaces']:,}")]
    for k, (lab, big, desc) in enumerate(items):
        y = 0.72 - k * 0.24
        fig.text(0.56, y, lab, fontsize=11, fontweight="bold", color=T["muted"])
        fig.text(0.56, y - 0.065, big, fontsize=22, fontweight="bold", color=T["ink"])
        fig.text(0.56, y - 0.105, _wrap(desc, 58), fontsize=9.5, color=T["muted"], va="top")
    footer(fig, T, "Sources: IFC / World Bank MSME estimates; SAM and SOM are FluxMuse planning estimates (facts file §5). Verify before external use.")
    return fig


def _wrap(s, n):
    words, lines, cur = s.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 > n:
            lines.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}".strip()
    lines.append(cur)
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# v2 charts
# ---------------------------------------------------------------------------
def chart_cash_runway(D, T, suffix):
    mb = D["monthly_base"]
    mk = mb["markers"]
    labels = mb["labels"]
    c = D["cash"]
    cash = [rm(v) for v in mb["closing_cash_zar"]]
    buf = D["min_cash_buffer_zar"] / 1e6
    seed = mk["seed_month_index"]
    launches = mk["launch_month_index"]
    be = mk["breakeven_month_index"]
    last = max(i for i in [mk["breakeven_sustained_month_index"], mk["min_post_seed_cash_month_index"], launches.get("Ghana")] if i is not None)
    n = min(60, ((last + 12) // 12 + 1) * 12)
    cash = cash[:n]
    tr = mk["min_post_seed_cash_month_index"]
    fig = new_fig(T, suffix)
    header(fig, T, "Cash runway on the R25m seed",
           f"Base case, monthly closing cash vs the R3.0m minimum-cash buffer, {labels[0]} - {labels[n - 1]}. No Series A")
    ax = fig.add_axes([0.08, 0.12, 0.88, 0.70])
    style_axes(ax, T)
    top = max(cash) * 1.42
    for name, idxs in mk["founding_member_window_indices"].items():
        idxs = [i for i in idxs if i < n]
        if idxs:
            ax.axvspan(min(idxs) - 0.5, max(idxs) + 0.5, color=T["tint"], alpha=0.9 if T["bg"] == "#0F1419" else 1.0, linewidth=0, zorder=0)
    ax.plot(range(n), cash, color=T["orange"], linewidth=2.4, solid_capstyle="round", zorder=3)
    ax.fill_between(range(n), cash, 0, color=T["orange"], alpha=0.08, linewidth=0, zorder=2)
    ax.hlines(buf, seed, n - 1, colors=T["slate"], linestyles=(0, (5, 3)), linewidth=1.4, zorder=3)
    ax.text(n - 1, buf - top * 0.012, "R3.0m minimum-cash buffer (from the seed month)", ha="right", va="top", fontsize=9, color=T["ink"])
    ax.axhline(0, color=T["muted"], linewidth=0.8)
    xt = ax.get_xaxis_transform()
    marks = [(mk["pilot_last_month_index"], f"Pilot ends\n{labels[mk['pilot_last_month_index']]}", 0),
             (min(mk["founding_member_window_indices"].get("South Africa", [2])), "Founding Member\nwindows (shaded)", 1),
             (seed, f"Seed R25m lands\n{labels[seed]}", 2)]
    for k, name in enumerate(["Nigeria", "Kenya", "Ghana"]):
        if launches.get(name) is not None and launches[name] < n:
            marks.append((launches[name], f"{name} launch\n{labels[launches[name]]}", k))
    if be is not None and be < n:
        marks.append((be, f"EBITDA break-even\n{labels[be]}", 0 if (launches.get("Nigeria") or 0) < be - 7 else 1))
    rows = [0.985, 0.875, 0.765]
    for x, text, row in marks:
        ax.axvline(x, color=T["muted"], linewidth=0.9, ymax=rows[row] - 0.02, zorder=1)
        ax.text(x + 0.35, rows[row], text, transform=xt, fontsize=8.8, color=T["ink"], va="top", ha="left", linespacing=1.15)
    ax.scatter([tr], [cash[tr]], s=52, color=T["orange"], edgecolor=T["bg"], linewidth=2, zorder=5)
    ax.annotate(f"Post-seed low {fmt_rm(c['min_post_seed_cash_zar'], 2)} ({c['min_post_seed_cash_month']})\n"
                f"{fmt_rm(c['headroom_over_buffer_zar'], 2)} above the buffer",
                xy=(tr, cash[tr]), xytext=(tr + 2.5, cash[tr] + top * 0.22), fontsize=9.5, color=T["ink"],
                arrowprops=dict(arrowstyle="-", color=T["muted"], linewidth=0.8))
    if c["pre_seed_bridge_required_zar"] > 0:
        ax.annotate(f"Pre-seed bridge\n{fmt_rk(c['pre_seed_bridge_required_zar'])}", xy=(seed - 1, 0), xytext=(seed + 1.2, top * 0.12),
                    fontsize=9, color=T["ink"], arrowprops=dict(arrowstyle="-", color=T["muted"], linewidth=0.8))
    ax.set_ylim(min(0, min(cash)) - top * 0.03, top)
    ax.set_xlim(-0.5, n - 0.5)
    month_ticks(ax, labels, n, T, 6)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"R{v:,.0f}m"))
    footer(fig, T)
    return fig


def chart_fm_cost(D, T, suffix):
    ann = D["annual"]
    years = [y for y in range(5) if ann[y]["founding_member_discount_zar"] + ann[y]["pilot_discount_zar"] > 0] or [0]
    years = list(range(0, max(years) + 1))
    series = [("South Africa", "orange"), ("Nigeria", "green"), ("Kenya", "blue"), ("Ghana", "violet")]
    fig = new_fig(T, suffix)
    tot = sum(ann[y]["founding_member_discount_zar"] + ann[y]["pilot_discount_zar"] for y in years)
    gross = sum(ann[y]["subscriptions_gross_zar"] for y in years)
    header(fig, T, "Launch discount cost: Founding Member and pilot",
           f"Base case, R thousand of revenue given up, Founding Member by market plus pilot. {fmt_rk(tot)} over {FY[years[0]]}-{FY[years[-1]]} = {tot / gross * 100:.1f}% of gross subscriptions")
    legend_row(fig, T, [(n, T[c]) for n, c in series] + [("Pilot brands (50% off)", T["slate"])], 0.80)
    ax = fig.add_axes([0.08, 0.13, 0.88, 0.60])
    style_axes(ax, T)
    bottom = [0.0] * len(years)
    for name, c in series:
        vals = [ann[y]["founding_member_discount_by_market_zar"][name] / 1e3 for y in years]
        ax.bar(range(len(years)), vals, 0.5, bottom=bottom, color=T[c], edgecolor=T["bg"], linewidth=1.2)
        bottom = [b + v for b, v in zip(bottom, vals)]
    vals = [ann[y]["pilot_discount_zar"] / 1e3 for y in years]
    ax.bar(range(len(years)), vals, 0.5, bottom=bottom, color=T["slate"], edgecolor=T["bg"], linewidth=1.2)
    bottom = [b + v for b, v in zip(bottom, vals)]
    for i, y in enumerate(years):
        pct = (ann[y]["founding_member_discount_zar"] + ann[y]["pilot_discount_zar"]) / ann[y]["subscriptions_gross_zar"] * 100 if ann[y]["subscriptions_gross_zar"] else 0
        ax.text(i, bottom[i] + max(bottom) * 0.015, f"R{bottom[i]:,.0f}k\n{pct:.1f}% of gross subs", ha="center", va="bottom", fontsize=10, fontweight="bold", color=T["ink"])
    ax.set_xticks(range(len(years)))
    ax.set_xticklabels([f"{FY[y]}\n{FY_SUB[y]}" for y in years], color=T["ink"])
    ax.set_ylim(0, max(bottom) * 1.25)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"R{v:,.0f}k"))
    footer(fig, T, "Founding Member: 30% off the first 2 monthly bills (Solo & SME, not Agency); annual plans +2 months. Source: FluxMuse model v2.")
    return fig


def chart_fx_shock(D, T, suffix):
    R = D["fx_shock"]["results"]
    names = list(R.keys())
    colours = [T["slate"], T["orange"], T["blue"]]
    short = ["Base", "ZAR +15%, repricing on", "ZAR +15%, no repricing"]
    metrics = [("FY3 revenue", "fy3_revenue_zar"), ("FY5 revenue", "fy5_revenue_zar"), ("FY3 EBITDA", "fy3_ebitda_zar"),
               ("FY5 EBITDA", "fy5_ebitda_zar"), ("Min. post-seed cash", "min_post_seed_cash_zar")]
    fig = new_fig(T, suffix)
    worst = R[names[2]]["change_vs_base_zar"]
    header(fig, T, "FX shock: ZAR 15% stronger vs NGN, KES, GHS and USD",
           f"Base case, R million; shock from Oct 2028. Without repricing FY5 revenue moves {fmt_rm(worst['fy5_revenue_zar'])}, FY5 EBITDA {fmt_rm(worst['fy5_ebitda_zar'])}")
    legend_row(fig, T, list(zip(short, colours)), 0.80)
    for k, (title, key) in enumerate(metrics):
        ax = fig.add_axes([0.05 + k * 0.19, 0.16, 0.16, 0.52])
        style_axes(ax, T, grid_axis=None)
        vals = [rm(R[n][key]) for n in names]
        ax.bar(range(3), vals, 0.66, color=colours)
        lo = min(0, min(vals))
        hi = max(vals)
        for i, v in enumerate(vals):
            ax.text(i, max(v, 0) + (hi - lo) * 0.02, f"R{v:,.1f}m" if abs(v) < 100 else f"R{v:,.0f}m", ha="center", va="bottom", fontsize=8.3, color=T["ink"], rotation=0)
        ax.axhline(0, color=T["muted"], linewidth=0.8)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_ylim(lo * 1.15, hi * 1.18 if hi > 0 else 1)
        ax.set_title(title, fontsize=11, fontweight="bold", color=T["ink"], pad=8)
        base = R[names[0]][key]
        d = R[names[2]][key] - base
        ax.text(0.5, -0.06, f"no repricing: {'+' if d >= 0 else '-'}R{abs(d) / 1e6:,.1f}m", transform=ax.transAxes, ha="center", va="top", fontsize=9, color=T["muted"])
    prof = all(R[n]["profitable_on_seed_alone"] for n in names)
    fig.text(0.04, 0.085, "Profitable on the R25m seed alone in all three cases" if prof else "The shock breaks the R25m profitability constraint in at least one case",
             fontsize=10, fontweight="bold", color=T["ink"])
    footer(fig, T, "Repricing on = quarterly review restores ZAR value one quarter after drift exceeds 10%. Source: FluxMuse Financial Model v2, Sensitivity sheet.")
    return fig


CHARTS = [("revenue_by_stream_fy1_fy5", chart_revenue), ("arr_and_customers", chart_arr_customers),
          ("ebitda_and_cash", chart_ebitda_cash), ("customers_by_region", chart_markets),
          ("unit_economics", chart_unit_econ), ("use_of_funds", chart_use_of_funds),
          ("scenarios", chart_scenarios), ("tam_sam_som", chart_tam),
          ("cash_runway_r25m", chart_cash_runway), ("customers_by_segment", chart_segments),
          ("founding_member_discount_cost", chart_fm_cost), ("fx_shock_sensitivity", chart_fx_shock)]


def main():
    os.makedirs(OUT, exist_ok=True)
    plt.rcParams.update({"font.family": FONT, "axes.unicode_minus": False})
    with open(SRC) as fh:
        D = json.load(fh)
    n = 0
    for name, fn in CHARTS:
        for theme, T in THEMES.items():
            for suffix in SIZES:
                fig = fn(D, T, suffix)
                save(fig, name, suffix, theme, T)
                n += 1
    print(f"rendered {n} chart files to {OUT} (font: {FONT})")


if __name__ == "__main__":
    main()
