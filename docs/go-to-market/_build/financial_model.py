#!/usr/bin/env python3
"""Build the FluxMuse investor financial model (v3: current offer, nine tiers, no trials; R25M seed test).

    venv/bin/python docs/go-to-market/_build/financial_model.py [--no-charts]

Outputs (docs/go-to-market/06_Financial_Model/):
  FluxMuse_Financial_Model.xlsx  live-formula workbook (Base selected)
  model_summary.json             machine-readable outputs quoted by the decks / business plan
Then runs _build/charts.py to render assets/charts/*.png.

Integrity: the workbook formulas are evaluated by fm_eval (a small Excel evaluator) and every
cell is compared with the independent Python mirror; the build fails on any mismatch or error.
"""
import json
import os
import subprocess
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import numpy as np  # noqa: E402

import fm_annual as A  # noqa: E402
import fm_inputs as I  # noqa: E402
import fm_rows as F  # noqa: E402
import fm_writer as W  # noqa: E402
from fm_eval import Evaluator, is_error  # noqa: E402

GTM = os.path.dirname(HERE)
OUT = os.path.join(GTM, "06_Financial_Model")
XLSX = os.path.join(OUT, "FluxMuse_Financial_Model.xlsx")
JSON_PATH = os.path.join(OUT, "model_summary.json")


def run(scen_idx=2, overrides=None):
    p = I.build_params(scen_idx, overrides)
    F.run_monthly(p)
    A.run_annual()
    return p, {k: list(v) for k, v in F.V.items()}, {k: list(v) for k, v in A.AV.items()}, dict(A.SV)


def pack(scen_idx=2, overrides=None):
    p, V, AV, SV = run(scen_idx, overrides)
    return {"p": p, "V": V, "AV": AV, "SV": SV}


def r0(x):
    return int(round(x)) if isinstance(x, (int, float)) else x


def rm(x, nd=1):
    return round(x / 1e6, nd)


def ok(r):
    return r["SV"]["k_profitable"] == "Yes"


# ---------------------------------------------------------------------------
# sensitivities & diagnostics (all computed by the Python mirror)
# ---------------------------------------------------------------------------
NONFOUNDER = [i for i, ro in enumerate(I.ROLES) if ro["type"] != "F"]


def payroll_cut_ov(cut):
    return {f"hc_ctc_{i}": I.ROLES[i]["ctc"] * (1 - cut) for i in NONFOUNDER}


def smallest_fix(scen_idx, base_ov):
    """Smallest gate-multiplier increase and smallest uniform non-founder payroll cut that pass the constraint."""
    base_gm = I.build_params(scen_idx, base_ov)["gate_mult"]
    grid = [round(base_gm + 0.05 * k, 2) for k in range(0, 61)]
    gm_fix = None
    lo, hi = 0, len(grid) - 1
    if ok(pack(scen_idx, {**base_ov, "gate_mult": grid[hi]})):
        while lo < hi:
            mid = (lo + hi) // 2
            if ok(pack(scen_idx, {**base_ov, "gate_mult": grid[mid]})):
                hi = mid
            else:
                lo = mid + 1
        gm_fix = grid[lo]
    cut_fix = None
    lo, hi = 0, 60
    if ok(pack(scen_idx, {**base_ov, **payroll_cut_ov(hi / 100)})):
        while lo < hi:
            mid = (lo + hi) // 2
            if ok(pack(scen_idx, {**base_ov, **payroll_cut_ov(mid / 100)})):
                hi = mid
            else:
                lo = mid + 1
        cut_fix = lo
    return gm_fix, cut_fix


def lever_fix(scen_idx, key, start, step, n, base_ov=None):
    """Smallest value of one lever (start + k * step, k = 0..n) that passes the R25M constraint; None if none does."""
    base_ov = base_ov or {}
    grid = [round(start + step * k, 4) for k in range(n + 1)]
    if not ok(pack(scen_idx, {**base_ov, key: grid[-1]})):
        return None
    lo, hi = 0, n
    while lo < hi:
        mid = (lo + hi) // 2
        if ok(pack(scen_idx, {**base_ov, key: grid[mid]})):
            hi = mid
        else:
            lo = mid + 1
    return grid[lo]


def base_levers(res):
    """Base case: which single lever, moved alone, restores profitability on the R25M seed (honest diagnostics, not adopted)."""
    b = res["Base"]
    out = {"profitable_as_modelled": ok(b), "funding_gap_to_hold_buffer_zar": b["SV"]["k_buf_short"],
           "funding_gap_to_stay_above_zero_zar": b["SV"]["k_funding_gap"]}
    if ok(b):
        return out
    gm, cut = smallest_fix(2, {})
    out["gate_multiplier"] = gm
    out["non_founder_salary_cut_pct"] = cut
    out["signup_volume_multiplier"] = lever_fix(2, "vol_mult", 1.0, 0.05, 80)
    out["conversion_multiplier"] = lever_fix(2, "conv_mult", 1.0, 0.05, 80)
    out["free_upgrade_pct_per_month"] = lever_fix(2, "free_conv", 0.005, 0.0025, 40)
    out["seed_amount_zar"] = lever_fix(2, "seed_amount", 25000000, 1000000, 40)
    return out


def sensitivity(res):
    churn = [0.70, 0.85, 1.00, 1.15, 1.30]
    vol = [0.70, 0.85, 1.00, 1.15, 1.30]
    grids = {k: [[0.0] * 5 for _ in range(5)] for k in ("rev3", "rev5", "e3", "e5", "cash")}
    for i, cm in enumerate(churn):
        for j, vm in enumerate(vol):
            r = pack(2, {"churn_sens": cm, "vol_mult": vm})
            grids["rev3"][i][j] = r["AV"]["a_rev"][3]
            grids["rev5"][i][j] = r["AV"]["a_rev"][5]
            grids["e3"][i][j] = r["AV"]["a_ebitda"][3]
            grids["e5"][i][j] = r["AV"]["a_ebitda"][5]
            grids["cash"][i][j] = r["SV"]["k_min_post"]
    grid = {"churn": churn, "vol": vol, "base_starter_churn": res["Base"]["p"]["churn_SO_S"],
            "tables": [{"title": "FY3 total revenue (R)", "fmt": "zar", "values": grids["rev3"]},
                       {"title": "FY5 total revenue (R)", "fmt": "zar", "values": grids["rev5"]},
                       {"title": "FY3 EBITDA (R)", "fmt": "zar", "values": grids["e3"]},
                       {"title": "FY5 EBITDA (R)", "fmt": "zar", "values": grids["e5"]},
                       {"title": "Minimum post-seed cash (R; buffer R3.0M)", "fmt": "zar", "values": grids["cash"]}]}

    fx = {"Base": res["Base"], "ZAR 15% stronger (repricing on)": pack(2, {"fx_shock": 0.15}),
          "ZAR 15% stronger (no repricing)": pack(2, {"fx_shock": 0.15, "reprice_on": 0})}
    disc = {"Founding Member (default)": res["Base"], "None": pack(2, {"disc_option": 2})}
    pilot = {"0.25% a month": pack(2, {"free_conv": 0.0025}), "0.5% a month (default)": res["Base"], "1.0% a month": pack(2, {"free_conv": 0.01})}
    cons = res["Conservative"]
    cons_basegates = pack(1, {"gate_mult": 1.0})
    diag = {"cons": cons, "cons_basegates": cons_basegates}
    if ok(cons):
        diag["fix_from"] = "Conservative with Base hiring & launch gates (1.00x)"
        diag["gm_fix"], diag["cut_fix"] = smallest_fix(1, {"gate_mult": 1.0}) if not ok(cons_basegates) else (None, None)
    else:
        diag["fix_from"] = "Conservative as modelled"
        diag["gm_fix"], diag["cut_fix"] = smallest_fix(1, {})

    def blk(title, cols, runs, rows, note=None):
        return {"title": title, "cols": cols, "note": note,
                "rows": [(lab, fmt, [fn(runs[c]) for c in cols]) for lab, fmt, fn in rows]}

    std_rows = []
    for y in (1, 3, 5):
        std_rows += [(f"FY{y} total revenue (R)", "zar", lambda r, y=y: r["AV"]["a_rev"][y]),
                     (f"FY{y} EBITDA (R)", "zar", lambda r, y=y: r["AV"]["a_ebitda"][y])]
    std_rows += [("FY5 EBITDA margin", "pct", lambda r: r["AV"]["a_ebitda_pct"][5]),
                 ("FY5 paying workspaces (end)", "n0", lambda r: r["AV"]["a_cust"][5]),
                 ("FY5 subscription ARR (R)", "zar", lambda r: r["AV"]["a_arr"][5]),
                 ("FY5 headcount", "n0", lambda r: r["AV"]["a_fte"][5]),
                 ("EBITDA break-even (first / sustained)", "text", lambda r: f"{r['SV']['k_be']} / {r['SV']['k_be_sus']}"),
                 ("Operating cash flow positive (first / sustained)", "text", lambda r: f"{r['SV']['k_cfpos']} / {r['SV']['k_cfpos_sus']}"),
                 ("Minimum post-seed cash (R)", "zar", lambda r: r["SV"]["k_min_post"]),
                 ("Month of minimum post-seed cash", "text", lambda r: r["SV"]["k_min_post_month"]),
                 ("Shortfall vs R3.0M buffer (R)", "zar", lambda r: r["SV"]["k_buf_short"]),
                 ("Pre-seed bridge required (R)", "zar", lambda r: r["SV"]["k_bridge"]),
                 ("Launches NG / KE / GH / Rest", "text", lambda r: " / ".join(r["SV"][f"k_launch_{m}"] for m in ("NG", "KE", "GH", "RoA"))),
                 ("FY5 closing cash (R)", "zar", lambda r: r["AV"]["a_close_cash"][5]),
                 ("Profitable on the R25M seed alone?", "text", lambda r: r["SV"]["k_profitable"])]
    blocks = [blk("Scenario comparison (seed only; Series A off)", I.SCENARIOS, res, std_rows)]
    fx_rows = [("FY3 total revenue (R)", "zar", lambda r: r["AV"]["a_rev"][3]), ("FY5 total revenue (R)", "zar", lambda r: r["AV"]["a_rev"][5]),
               ("FY3 EBITDA (R)", "zar", lambda r: r["AV"]["a_ebitda"][3]), ("FY5 EBITDA (R)", "zar", lambda r: r["AV"]["a_ebitda"][5]),
               ("Minimum post-seed cash (R)", "zar", lambda r: r["SV"]["k_min_post"]),
               ("Profitable on the R25M seed alone?", "text", lambda r: r["SV"]["k_profitable"])]
    blocks.append(blk(f"FX shock (Base): ZAR 15% stronger vs NGN/KES/GHS/USD from {F.mlabel(res['Base']['p']['fx_shock_month'])}, after the NG/KE/GH plan months", list(fx), fx, fx_rows,
                      "Repricing on = the quarterly policy restores ZAR value one quarter after drift exceeds 10%."))
    d_rows = [("FY1 total revenue (R)", "zar", lambda r: r["AV"]["a_rev"][1]), ("FY2 total revenue (R)", "zar", lambda r: r["AV"]["a_rev"][2]),
              ("Launch-offer discount cost FY1 (R)", "zar", lambda r: r["AV"]["a_fm_cost"][1]),
              ("Launch-offer discount cost FY1-FY3 (R)", "zar", lambda r: sum(r["AV"]["a_fm_cost"][1:4])),
              ("FY5 EBITDA (R)", "zar", lambda r: r["AV"]["a_ebitda"][5]),
              ("Minimum post-seed cash (R)", "zar", lambda r: r["SV"]["k_min_post"]),
              ("Profitable on the R25M seed alone?", "text", lambda r: r["SV"]["k_profitable"])]
    blocks.append(blk("Founding Member (Base): live offer vs no offer", list(disc), disc, d_rows,
                      "None also removes the +20% sign-up uplift assumed while the offer runs."))
    p_rows = [("FY1 Free users upgrading to paid", "n0", lambda r: r["AV"]["a_free_conv"][1]),
              ("FY3 Free users upgrading to paid", "n0", lambda r: r["AV"]["a_free_conv"][3]),
              ("FY1 total revenue (R)", "zar", lambda r: r["AV"]["a_rev"][1]),
              ("FY3 total revenue (R)", "zar", lambda r: r["AV"]["a_rev"][3]),
              ("FY5 EBITDA (R)", "zar", lambda r: r["AV"]["a_ebitda"][5]),
              ("Pre-seed bridge required (R)", "zar", lambda r: r["SV"]["k_bridge"]),
              ("Minimum post-seed cash (R)", "zar", lambda r: r["SV"]["k_min_post"]),
              ("Profitable on the R25M seed alone?", "text", lambda r: r["SV"]["k_profitable"])]
    blocks.append(blk("Free-to-paid conversion of active Free users (Base)", list(pilot), pilot, p_rows))
    c_rows = [("Minimum post-seed cash (R)", "zar", lambda r: r["SV"]["k_min_post"]),
              ("Month of minimum post-seed cash", "text", lambda r: r["SV"]["k_min_post_month"]),
              ("Shortfall vs R3.0M buffer (R)", "zar", lambda r: r["SV"]["k_buf_short"]),
              ("EBITDA break-even (sustained)", "text", lambda r: r["SV"]["k_be_sus"]),
              ("FY5 EBITDA (R)", "zar", lambda r: r["AV"]["a_ebitda"][5]),
              ("FY5 headcount", "n0", lambda r: r["AV"]["a_fte"][5]),
              ("Profitable on the R25M seed alone?", "text", lambda r: r["SV"]["k_profitable"])]
    cruns = {"Conservative as modelled": cons, "Conservative with Base gates (1.00x)": cons_basegates}
    note = (f"Smallest fix from '{diag['fix_from']}': raise the hiring & launch MRR-gate multiplier to {diag['gm_fix']}x"
            f", or cut all non-founder salaries by {diag['cut_fix']}%." if (diag["gm_fix"] or diag["cut_fix"] is not None) else
            "No cut needed.")
    blocks.append(blk("Conservative: constraint check and the smallest cost cut that fixes it", list(cruns), cruns, c_rows, note))
    levers = base_levers(res)
    lv = [("Raise the hiring & launch MRR-gate multiplier to", levers.get("gate_multiplier"), "x"),
          ("Cut every non-founder salary by", levers.get("non_founder_salary_cut_pct"), "%"),
          ("Sign-up volume multiplier (all markets)", levers.get("signup_volume_multiplier"), "x"),
          ("Conversion multiplier (direct paid and Free upgrades)", levers.get("conversion_multiplier"), "x"),
          ("Free-to-paid upgrades per month", levers.get("free_upgrade_pct_per_month"), "rate"),
          ("Seed size instead of R25M", levers.get("seed_amount_zar"), "zar")]
    blocks.append({"title": "Base: does it reach break-even on the R25M seed? Single levers that would restore the test (each moved alone; NOT adopted)",
                   "cols": ["Value needed"], "note": "Blank = no value in the searched range passes on its own. Funding gap to hold the R3.0M buffer: "
                   f"R{levers['funding_gap_to_hold_buffer_zar'] / 1e6:,.1f}M.",
                   "rows": [(lab, "text", [("not within range" if v is None else (f"{v:.2f}x" if u == "x" else f"{v}%" if u == "%" else f"{v:.2%}" if u == "rate" else f"R{v / 1e6:,.0f}M"))])
                            for lab, v, u in lv] if not levers["profitable_as_modelled"] else []})
    return {"grid": grid, "blocks": blocks, "fx": fx, "disc": disc, "pilot": pilot, "diag": diag, "levers": levers}


# ---------------------------------------------------------------------------
# verification
# ---------------------------------------------------------------------------
def _addr(key, m):
    sh, r = F.ROWPOS[key]
    return sh, f"{F.col(m)}{r}"


def verify(wb, base, uof):
    p, V, AV, SV = base["p"], base["V"], base["AV"], base["SV"]
    ev = Evaluator(wb)
    errors, n_formulas = [], 0
    for ws in wb.worksheets:
        for row in ws.iter_rows():
            for c in row:
                if isinstance(c.value, str) and c.value.startswith("="):
                    n_formulas += 1
                    try:
                        val = ev.value(ws.title, c.coordinate)
                    except Exception as e:  # noqa: BLE001
                        errors.append(f"{ws.title}!{c.coordinate}: {e}")
                        continue
                    if is_error(val):
                        errors.append(f"{ws.title}!{c.coordinate}: non-finite result")
    mism = []

    def val(sh, addr):
        try:
            return ev.value(sh, addr)
        except Exception as e:  # noqa: BLE001
            return f"#ERR {e}"

    n_cmp = [0]

    def cmp(label, xv, pv):
        n_cmp[0] += 1
        if isinstance(pv, str) or isinstance(xv, str):
            if str(xv) != str(pv):
                mism.append(f"{label}: excel={xv!r} python={pv!r}")
            return
        if abs(float(xv) - float(pv)) > 1e-6 * max(1.0, abs(float(pv))):
            mism.append(f"{label}: excel={float(xv):.6f} python={float(pv):.6f}")

    for key, (sh, r) in F.ROWPOS.items():
        for m in F.MONTHS:
            cmp(f"{sh}!{F.col(m)}{r} [{key} m{m}]", val(sh, f"{F.col(m)}{r}"), V[key][m])
    for key, (sh, r) in A.ANNPOS.items():
        for y in A.YEARS:
            cmp(f"{sh}!{A.acol(y)}{r} [{key} FY{y}]", val(sh, f"{A.acol(y)}{r}"), AV[key][y])
    for s in A.SROWS:
        cmp(f"Cash_Flow!B{s['row']} [{s['key']}]", val("Cash_Flow", f"B{s['row']}"), SV[s["key"]])
    for n, w in uof["reconciliation"].items():
        for i, c in enumerate(w["categories"]):
            cmp(f"Use_of_Funds!{W.UOF_CELLS[(n, i)]} [{n}m cat {i}]", val("Use_of_Funds", W.UOF_CELLS[(n, i)]), c["modelled_spend_zar_exact"])
        cmp(f"Use_of_Funds total {n}m", val("Use_of_Funds", W.UOF_CELLS[(n, "total")]), w["total_gross_spend_zar_exact"])
        cmp(f"Use_of_Funds net {n}m", val("Use_of_Funds", W.UOF_CELLS[(n, "net")]), w["net_cash_consumed_zar_exact"])
    # hand checks, independent of both implementations
    m = 13
    hand = (V["close_ZA_SO_N"][m - 1] * (1 - p["churn_SO_N"] * p["churn_mult"] * p["churn_sens"] - p["upg_SO_N"]) + V["newc_ZA_SO_N"][m])
    cmp("hand: ZA Solo Nano closing m13", val(*_addr("close_ZA_SO_N", m)), hand)
    m = 40
    hand_rev = V["close_NG_AG_A"][m] * 579000 / 82.83 * 1.06 ** 3 * (1 - 0.25 * 2 / 12) * V["vf_NG"][m]
    cmp("hand: Nigeria partner-wholesale Agency revenue m40", val(*_addr("rev_NG_AG_A", m)), hand_rev)
    m = 7
    hand_free = V["free_close_ZA"][m - 1] * (1 - p["free_conv"] * p["conv_mult"] - p["free_dormancy"]) + V["trials_ZA"][m] * (1 - p["direct_blend"])
    cmp("hand: ZA active Free users m7", val(*_addr("free_close_ZA", m)), hand_free)
    fy2_rev = sum(float(val(*_addr("total_rev", k))) for k in range(13, 25))
    cmp("hand: FY2 revenue = sum of Revenue_Build months 13-24", val("Annual_Summary", f"D{A.ANNPOS['a_rev'][1]}"), fy2_rev)
    return n_formulas, n_cmp[0], errors, mism


# ---------------------------------------------------------------------------
# JSON
# ---------------------------------------------------------------------------
def use_of_funds(p):
    out = {"seed_zar": r0(p["seed_amount"]), "allocation": [], "reconciliation": {}}
    for cat, pct, buys in W.USE_OF_FUNDS:
        amt = p["seed_amount"] * pct
        out["allocation"].append({"category": cat, "share_pct": round(pct * 100), "amount_zar": r0(amt), "amount_usd": r0(amt / p["fx"]), "what_it_buys": buys})
    for n in W.UOF_WINDOWS:
        m1, m2 = W.uof_window(p, n)
        cats = [W.uof_py(i, m1, m2) for i in range(len(W.USE_OF_FUNDS))]
        tot = sum(cats)
        rev = sum(F.V["pl_rev"][m1:m2 + 1])
        out["reconciliation"][n] = {
            "window": f"{F.mlabel(m1)} - {F.mlabel(m2)} (months {m1}-{m2})",
            "categories": [{"category": W.USE_OF_FUNDS[i][0], "allocation_pct": round(W.USE_OF_FUNDS[i][1] * 100),
                            "modelled_spend_zar": r0(c), "modelled_spend_zar_exact": c,
                            "share_of_spend_pct": round(c / tot * 100, 1) if tot else 0.0,
                            "gap_pp": round((c / tot - W.USE_OF_FUNDS[i][1]) * 100, 1) if tot else 0.0} for i, c in enumerate(cats)],
            "total_gross_spend_zar": r0(tot), "total_gross_spend_zar_exact": tot, "revenue_collected_zar": r0(rev),
            "net_cash_consumed_zar": r0(tot - rev), "net_cash_consumed_zar_exact": tot - rev,
            "seed_remaining_zar": r0(p["seed_amount"] - (tot - rev)),
        }
    return out


def strip_exact(o):
    if isinstance(o, dict):
        return {str(k): strip_exact(v) for k, v in o.items() if not str(k).endswith("_exact")}
    if isinstance(o, list):
        return [strip_exact(v) for v in o]
    return o


def fy_block(r, y):
    AV = r["AV"]
    return {
        "fy": f"FY{y}", "period": f"Oct {2025 + y} - Sep {2026 + y}",
        "subscriptions_gross_zar": r0(AV["a_rev_subs_gross"][y]),
        "founding_member_discount_zar": r0(AV["a_fm_cost"][y]),
        "founding_member_discount_by_market_zar": {I.MARKET_SHORT[m]: r0(AV[f"a_fm_cost_{m}"][y]) for m in I.WINDOW_MKTS},
        "revenue_by_stream_zar": {
            "subscriptions": r0(AV["a_rev_subs"][y]), "ai_credit_topups": r0(AV["a_rev_topup"][y]),
            "whatsapp_messaging": r0(AV["a_rev_wa"][y]), "commerce_platform_fees": r0(AV["a_rev_commerce"][y]),
            "enterprise_setup_fees": r0(AV["a_rev_ent_setup"][y]), "agency_setup_fees": r0(AV["a_rev_agency_setup"][y]),
        },
        "net_subscription_revenue_by_market_zar": {I.MARKET_SHORT[m]: r0(AV[f"a_subnet_{m}"][y]) for m in I.MARKETS},
        "total_revenue_zar": r0(AV["a_rev"][y]), "total_revenue_usd": r0(AV["a_rev_usd"][y]),
        "revenue_growth_pct": None if y == 1 else round(AV["a_growth"][y] * 100, 1),
        "gross_profit_zar": r0(AV["a_gp"][y]), "gross_margin_pct": round(AV["a_gm"][y] * 100, 1),
        "software_gross_margin_pct": round(AV["a_sw_gm"][y] * 100, 1),
        "opex_zar": {"payroll_excl_cs": r0(AV["a_opex_hc"][y]), "marketing_sales_programmes": r0(AV["a_opex_mkt"][y]),
                     "g_and_a": r0(AV["a_opex_ga"][y]), "legal_compliance": r0(AV["a_opex_legal"][y]),
                     "tools": r0(AV["a_opex_tools"][y]), "travel": r0(AV["a_opex_travel"][y]), "total": r0(AV["a_opex"][y])},
        "paid_acquisition_zar": r0(AV["a_paid"][y]), "paid_acquisition_funded_by_cap_pct": round(AV["a_paid_funded"][y] * 100, 1),
        "ebitda_zar": r0(AV["a_ebitda"][y]), "ebitda_usd": r0(AV["a_ebitda_usd"][y]),
        "ebitda_margin_pct": round(AV["a_ebitda_pct"][y] * 100, 1),
        "tax_zar": r0(AV["a_tax"][y]), "net_income_zar": r0(AV["a_ni"][y]),
        "operating_cash_flow_zar": r0(AV["a_opcf"][y]), "equity_funding_zar": r0(AV["a_funding"][y]),
        "closing_cash_zar": r0(AV["a_close_cash"][y]), "min_month_end_cash_zar": r0(AV["a_min_cash"][y]),
        "ending_customers_by_segment": {I.SEG_SHORT[s]: r0(AV[f"a_seg_{s}"][y]) for s in I.SEGMENTS},
        "ending_customers_by_market": {I.MARKET_SHORT[m]: r0(AV[f"a_mkt_{m}"][y]) for m in I.MARKETS},
        "ending_customers_by_tier": {I.TIER_NAME[t]: r0(AV[f"a_cust_{t}"][y]) for t in I.TIERS},
        "new_customers_by_segment": {I.SEG_SHORT[s]: r0(AV[f"a_segnew_{s}"][y]) for s in I.SEGMENTS},
        "free_plan": {"new_free_users": r0(AV["a_free_new"][y]), "free_to_paid_upgrades": r0(AV["a_free_conv"][y]),
                      "active_free_users_end_fy": r0(AV["a_free_active"][y]), "free_plan_cost_zar": r0(AV["a_free_cost"][y])},
        "ending_paying_workspaces": r0(AV["a_cust"][y]),
        "new_workspaces": r0(AV["a_new"][y]), "churned_workspaces": r0(AV["a_churned"][y]),
        "subscription_mrr_sept_zar": r0(AV["a_mrr"][y]),
        "subscription_arr_zar": r0(AV["a_arr"][y]), "subscription_arr_usd": r0(AV["a_arr_usd"][y]),
        "arpa_subscription_zar_per_month": r0(AV["a_arpa"][y]),
        "total_revenue_per_workspace_zar_per_month": r0(AV["a_arpa_total"][y]),
        "headcount_end_fy": r0(AV["a_fte"][y]),
        "unit_economics": {
            "blended_cac_zar": r0(AV["u_cac"][y]), "blended_ltv_zar": r0(AV["u_ltv"][y]),
            "ltv_to_cac": round(AV["u_ltvcac"][y], 1), "cac_payback_months": round(AV["u_payback"][y], 1),
            "blended_monthly_churn_pct": round(AV["u_churn"][y] * 100, 2), "magic_number": round(AV["u_magic"][y], 2),
            "burn_multiple": AV["u_burn_mult"][y] if isinstance(AV["u_burn_mult"][y], str) else round(AV["u_burn_mult"][y], 2),
            "rule_of_40_pct": None if y == 1 else round(AV["u_r40"][y] * 100, 1),
        },
    }


def scen_brief(r):
    AV, SV, p = r["AV"], r["SV"], r["p"]
    return {
        "seed_zar": r0(p["seed_amount"]), "series_a_zar": r0(p["seriesA_amount"] if p["seriesA_on"] else 0),
        "revenue_zar_fy1_fy5": [r0(AV["a_rev"][y]) for y in A.YEARS], "ebitda_zar_fy1_fy5": [r0(AV["a_ebitda"][y]) for y in A.YEARS],
        "ebitda_margin_pct_fy1_fy5": [round(AV["a_ebitda_pct"][y] * 100, 1) for y in A.YEARS],
        "paying_workspaces_fy1_fy5": [r0(AV["a_cust"][y]) for y in A.YEARS], "headcount_fy1_fy5": [r0(AV["a_fte"][y]) for y in A.YEARS],
        "fy3_revenue_zar": r0(AV["a_rev"][3]), "fy3_ebitda_zar": r0(AV["a_ebitda"][3]), "fy3_paying_workspaces": r0(AV["a_cust"][3]),
        "fy5_revenue_zar": r0(AV["a_rev"][5]), "fy5_revenue_usd": r0(AV["a_rev_usd"][5]),
        "fy5_ebitda_zar": r0(AV["a_ebitda"][5]), "fy5_ebitda_margin_pct": round(AV["a_ebitda_pct"][5] * 100, 1),
        "fy5_paying_workspaces": r0(AV["a_cust"][5]), "fy5_arr_zar": r0(AV["a_arr"][5]),
        "breakeven_month": SV["k_be"], "breakeven_month_sustained": SV["k_be_sus"],
        "cashflow_positive_month": SV["k_cfpos"], "cashflow_positive_month_sustained": SV["k_cfpos_sus"],
        "min_cash_zar": r0(SV["k_min_cash"]), "min_cash_month": SV["k_min_cash_month"],
        "min_post_seed_cash_zar": r0(SV["k_min_post"]), "min_post_seed_cash_month": SV["k_min_post_month"],
        "min_cash_buffer_zar": r0(SV["k_buffer"]), "shortfall_vs_buffer_zar": r0(SV["k_buf_short"]),
        "first_month_below_buffer": SV["k_buf_first"],
        "pre_seed_bridge_required_zar": r0(SV["k_bridge"]),
        "additional_funding_needed_to_stay_above_zero_zar": r0(SV["k_funding_gap"]),
        "market_launch_months": {I.MARKET_SHORT[m]: SV[f"k_launch_{m}"] for m in I.NONZA},
        "profitable_on_seed_alone": SV["k_profitable"] == "Yes",
    }


def constraint_check(r):
    SV, V, p = r["SV"], r["V"], r["p"]
    s = int(p["seed_month"])
    below = [F.mlabel(m) for m in F.MONTHS if m >= s and V["close_cash"][m] < p["min_cash_buffer"]]
    return {
        "no_series_a": not (p["seriesA_on"] == 1 and p["seriesA_amount"] > 0),
        "cash_at_or_above_buffer_every_month_from_seed": SV["k_min_post"] >= SV["k_buffer"],
        "evidence_min_post_seed_cash": f"R{SV['k_min_post'] / 1e6:,.2f}M in {SV['k_min_post_month']} vs buffer R{SV['k_buffer'] / 1e6:,.1f}M",
        "months_below_buffer": below,
        "ebitda_breakeven_sustained": SV["k_be_sus_num"] < 999,
        "evidence_ebitda": f"first {SV['k_be']}; >= 0 every month from {SV['k_be_sus']}",
        "operating_cash_flow_positive_sustained": SV["k_cfpos_sus_num"] < 999,
        "evidence_cash_flow": f"first {SV['k_cfpos']}; >= 0 every month from {SV['k_cfpos_sus']}",
        "profitable_on_seed_alone": SV["k_profitable"] == "Yes",
    }


def price_tables(p):
    loc = {"NGN": 0, "KES": 1, "GHS": 2, "USD": 3}
    return {
        "zar_list_monthly": {"Free": 0, **{I.TIER_NAME[t]: I.PRICING[t][0] for t in I.TIERS}},
        "custom_modelled_as": "from R19,999 a month (Custom is sold by consultation) [[CONFIRM]]",
        "bands": {"Small": ["Free", "Nano", "Micro"], "Medium": ["Starter", "Growth", "Scale"], "Enterprise": ["Corporate", "Agency", "Custom"]},
        "annual_multiple_of_monthly": p["annual_months"],
        "vat": "None: Fluxmuse (Pty) Ltd is not VAT-registered; prices are the amounts charged",
        "local_monthly": {c: {I.TIER_NAME[t]: I.LOCAL[t][k] for t in I.TIERS} for c, k in loc.items()},
        "partner_wholesale_monthly": {"ZAR": I.WHOLESALE[0], **{c: I.WHOLESALE[1][k] for c, k in loc.items()},
                                      "discount_vs_agency_list_pct": 30, "share_of_agency_customers_on_wholesale_pct": round(p["partner_share"] * 100),
                                      "stacks_with_founding_member": False,
                                      "local_basis": "No regional wholesale prices exist in the product; the model uses the Corporate local price points (70% of Agency list) [[CONFIRM]]"},
        "founding_member_first_2_bills_zar": {I.TIER_NAME[t]: int(I.PRICING[t][0] * (1 - p["fm_disc"])) for t in I.FM_PRICE},
        "fx_price_setting": {"NGN_per_ZAR": p["rate_NGN"], "KES_per_ZAR": p["rate_KES"], "GHS_per_ZAR": p["rate_GHS"], "ZAR_per_USD": p["fx"]},
        "zar_value_at_parity": {I.MARKET_SHORT[m]: {("Partner wholesale" if t == "W" else I.TIER_NAME[t]): round(p[f"price_{m}_{t}"])
                                                    for t in I.PRICE_KEYS} for m in I.MARKETS},
        "fx_depreciation_vs_zar_pct_per_year": {"NGN": p["dep_NG"] * 100, "KES": p["dep_KE"] * 100, "GHS": p["dep_GH"] * 100, "USD": p["dep_RoA"] * 100},
        "repricing_policy": f"Reviewed quarterly; if the ZAR value of local prices has drifted more than {p['reprice_thr']:.0%}, prices are reset to ZAR parity with a one-quarter lag. Annual list escalator {p['price_esc']:.0%} each October in all markets.",
    }


def summary_json(res, sens, uof):
    base = res["Base"]
    p, V, AV, SV = base["p"], base["V"], base["AV"], base["SV"]
    ue = 3
    segs = {I.SEG_SHORT[s]: {"arpa_zar_per_month": r0(AV[f"u_arpa_{s}"][ue]), "monthly_churn_pct": round(AV[f"u_churn_{s}"][ue] * 100, 2),
                             "ltv_zar": r0(AV[f"u_ltv_{s}"][ue]), "cac_zar": r0(AV[f"u_cac_{s}"][ue]),
                             "ltv_to_cac": round(AV[f"u_ltvcac_{s}"][ue], 1), "cac_payback_months": round(AV[f"u_payback_{s}"][ue], 1),
                             "new_customers": r0(AV[f"u_new_{s}"][ue])} for s in I.SEGMENTS}
    tiers = {I.TIER_NAME[t]: {"arpa_zar_per_month": r0(AV[f"u_arpa_{t}"][ue]), "monthly_churn_pct": round(AV[f"u_churn_{t}"][ue] * 100, 2),
                              "ltv_zar": r0(AV[f"u_ltv_{t}"][ue])} for t in I.TIERS}
    labels = [F.mlabel(m) for m in F.MONTHS]

    def idx_of(num):
        return None if num == 999 else int(num) - 1

    fxr = {}
    for name, r in sens["fx"].items():
        fxr[name] = {"fy3_revenue_zar": r0(r["AV"]["a_rev"][3]), "fy5_revenue_zar": r0(r["AV"]["a_rev"][5]),
                     "fy3_ebitda_zar": r0(r["AV"]["a_ebitda"][3]), "fy5_ebitda_zar": r0(r["AV"]["a_ebitda"][5]),
                     "min_post_seed_cash_zar": r0(r["SV"]["k_min_post"]), "min_post_seed_cash_month": r["SV"]["k_min_post_month"],
                     "profitable_on_seed_alone": r["SV"]["k_profitable"] == "Yes"}
    b = fxr["Base"]
    for name in list(fxr)[1:]:
        fxr[name]["change_vs_base_zar"] = {k: fxr[name][k] - b[k] for k in ("fy3_revenue_zar", "fy5_revenue_zar", "fy3_ebitda_zar", "fy5_ebitda_zar", "min_post_seed_cash_zar")}
    diag = sens["diag"]
    cons = res["Conservative"]
    cb = diag["cons_basegates"]
    scen_defs = {}
    for k, s in enumerate(I.SCENARIOS):
        d = {}
        for e in I.ENTRIES:
            if e["kind"] == "scen":
                d[e["key"]] = e["values"][k]
        scen_defs[s] = d

    ta = [
        f"Month 1 = Oct 2026. Opening cash R{p['opening_cash']:,.0f} [[CONFIRM]]. Lean pre-seed mode until the R{p['seed_amount'] / 1e6:,.0f}M seed lands in {F.mlabel(p['seed_month'])}: two founders on reduced salaries, lean hosting and overheads, the first-group set-up cost; no paid marketing or hires.",
        f"No trials and no pilot. South Africa sells from Oct 2026. A first group of {p['first_group_n']:g} paying businesses a month is set up by hand from Oct 2026 to {F.mlabel(p['first_group_end'])} ({p['first_mix_SO']:.0%} Solo, the rest SMEs) [[CONFIRM]].",
        f"Self-serve sign-ups (Free + paid): South Africa {p['trials_launch_ZA']} in Oct 2026 [[CONFIRM]], growing {p['g_fy1']:.0%} a month in FY1 (Base). {p['conv_SO']:.0%} of Solo and {p['conv_SM']:.0%} of SME sign-ups pay at once [[CONFIRM]]; the rest join Free. Active Free users upgrade at {p['free_conv']:.1%} a month and go dormant at {p['free_dormancy']:.0%} a month [[CONFIRM]].",
        f"Founding Member: {p['fm_disc']:.0%} off the first 2 monthly bills for South African Solo and SME sign-ups, live from Oct 2026; proposed end {F.mlabel(p['fm_end'])} [[CONFIRM]]. Not modelled on Agency, Corporate, Custom or annual plans. +{p['fm_uplift']:.0%} paying sign-ups while it runs [[CONFIRM]]. No NG/KE/GH launch windows.",
        "Pricing (ZAR / month): Free R0, Nano R149, Micro R289, Starter R499, Growth R1,999, Scale R4,999, Corporate R6,999, Agency R9,999, Custom from R19,999 [[CONFIRM]]. NG/KE/GH/USD use the live tier_regional_prices at FX parity. Annual = 10x monthly, 25% of subscriptions on annual billing; +6% list escalator each October. No VAT (not VAT-registered).",
        "Partner wholesale: agency-segment customers (100%) pay R6,999 a month (Agency list -30%); local wholesale at the Corporate local price points [[CONFIRM]]. Partner referral commission undecided and not modelled.",
        f"Segment tier mix: Solo {p['so_mix_N']:.0%} Nano / {p['so_mix_Mi']:.0%} Micro / {p['so_mix_S']:.0%} Starter; SMEs {p['sm_mix_S']:.0%} Starter / {p['sm_mix_G']:.0%} Growth / {p['sm_mix_Sc']:.0%} Scale. Upgrades a month: Nano->Micro {p['upg_SO_N']:.1%}, Micro->Starter {p['upg_SO_Mi']:.1%}, Starter->Growth {p['upg_SM_S']:.1%}, Growth->Scale {p['upg_SM_G']:.1%} [[CONFIRM]]. Agencies: 0.5 inbound a month in SA plus 1.5 per partnerships manager; 0.4 per NG/KE/GH country lead. Corporate inbound {p['corp_fy1']:g}/{p['corp_fy2']:g}/{p['corp_fy3']:g}/{p['corp_fy4']:g}/{p['corp_fy5']:g} deals a year; Custom {p['ent_fy1']:g}/{p['ent_fy2']:g}/{p['ent_fy3']:g}/{p['ent_fy4']:g}/{p['ent_fy5']:g} [[CONFIRM]].",
        f"Monthly churn: Nano {p['churn_SO_N']:.1%}, Micro {p['churn_SO_Mi']:.1%}, Solo Starter {p['churn_SO_S']:.1%}, SME Starter {p['churn_SM_S']:.1%}, SME Growth {p['churn_SM_G']:.1%}, SME Scale {p['churn_SM_Sc']:.1%}, Agency {p['churn_AG_A']:.1%}, Corporate {p['churn_CO_Co']:.1%}, Custom {p['churn_EN_E']:.1%} (Base; NG/KE/GH/Rest churn indices 1.05-1.25x).",
        f"Markets: South Africa only until NG/KE/GH checkout is live (Fincra/pawaPay pending). Planned earliest launches Nigeria {F.mlabel(p['launch_plan_NG'])}, Kenya {F.mlabel(p['launch_plan_KE'])}, Ghana {F.mlabel(p['launch_plan_GH'])}, Rest of Africa (USD) {F.mlabel(p['launch_plan_RoA'])} [[CONFIRM]], each also behind an MRR gate (R0.9M / R1.2M / R1.5M / R2.5M x scenario gate multiplier). Botswana & Namibia off; gated countries zero.",
        f"Cost discipline: every non-founder hire waits for its earliest month, the seed, and an MRR gate x scenario multiplier (Conservative {scen_defs['Conservative']['gate_mult']}x, Base {scen_defs['Base']['gate_mult']}x, Upside {scen_defs['Upside']['gate_mult']}x); paid acquisition = MIN(desired, R{p['paid_floor']:,.0f} + {scen_defs['Base']['cap_pct']:.0%} of last month's MRR in Base) and off where CAC payback > {p['pb_max']} months. Paid CAC Solo R{p['cac_SO']:,.0f} [[CONFIRM]], SME R{p['cac_SM']:,.0f}.",
        f"Other revenue: AI-credit packs (R300 for 1,000 credits, {p['topup_attach']:.0%} of metered workspaces a month [[CONFIRM]]), WhatsApp messages resold at Meta cost +25%, R25,000 Custom setup fee [[CONFIRM]]. No agency setup fee. No FluxMuse checkout fee: Paystack fees pass through to the merchant (0% in every scenario). Campaign Financing excluded.",
        f"COGS: AI at R0.15 of provider cost per credit (ai-credit-math.ts and platform_billing_config), falling 10% a year, 40% utilisation of the live allowances; Corporate, Agency and Custom use their own AI keys. Free users cost {p['free_credits']} credits a month at 40% use plus R{p['free_hosting']:g} hosting. Hosting R30k/month + R35 per workspace after the seed, 3.0% processing + 1.5% mobile-money/FX on non-SA revenue, R50 per workspace support, customer success team in COGS.",
        "Funding & tax: R25M seed only; Series A input kept at R0. Tax 27% only once cumulative EBITDA is positive; D&A, interest and VAT ignored (not VAT-registered).",
    ]
    confirmations = [
        f"Opening cash at 1 Oct 2026 (default R{p['opening_cash']:,.0f}) and how to cover the R{SV['k_bridge']:,.0f} pre-seed bridge if the seed lands {F.mlabel(p['seed_month'])}.",
        f"Seed close month ({F.mlabel(p['seed_month'])}) and instrument (SAFE vs priced equity).",
        f"First group set up by hand: {p['first_group_n']:g} a month, Oct 2026 to {F.mlabel(p['first_group_end'])}, {p['first_mix_SO']:.0%} Solo; R{p['first_group_cost']:,.0f} a month set-up cost.",
        f"South African sign-ups at launch ({p['trials_launch_ZA']} a month) and the pay-at-sign-up rates (Solo {p['conv_SO']:.0%}, SME {p['conv_SM']:.0%}).",
        f"Free plan: {p['free_conv']:.1%} a month upgrade, {p['free_dormancy']:.0%} a month dormancy, R{p['free_hosting']:g} hosting per active Free user. Free allowance is 60 credits in the product (100 in older copy).",
        "Segment tier mixes, the upgrade rates and the new churn rates for Nano, Micro, SME Starter and Corporate.",
        f"Founding Member end date (proposed {F.mlabel(p['fm_end'])}), whether it applies to Corporate or annual plans, and the +{p['fm_uplift']:.0%} sign-up uplift. Whether NG/KE/GH get a launch offer (none modelled).",
        "New NG/KE/GH and Rest-of-Africa plan months (Apr 2028 / Jul 2028 / Oct 2028 / May 2029) and their dependence on Fincra/pawaPay going live.",
        "Corporate and Custom inbound deal volumes, Custom modelled at R19,999, Custom setup fee R25,000, Corporate handling cost.",
        "Local partner wholesale prices (modelled at the Corporate local prices) and whether 100% of agency customers buy at wholesale.",
        "AI-credit pack attach rate (5%) and the R1,500 paid CAC for Solo.",
        "FX depreciation assumptions vs ZAR (NGN -10%, GHS -8%, KES -3%, USD 0% a year) and the quarterly repricing policy.",
        f"Cost-discipline rules: MRR gates per hire and launch, the scenario gate multipliers, the paid-acquisition cap ({scen_defs['Base']['cap_pct']:.0%} of MRR in Base) and the {p['pb_max']}-month CAC payback limit.",
        "Salaries and hiring plan (cost-to-company per role), including founders' reduced salaries.",
        "Market-sizing estimates (TAM/SAM/SOM) before external use.",
    ]
    iterations = [
        {"step": 1, "change": "v3 rebuild for the current offer: nine tiers, Free funnel, no trials or pilot, first group by hand, Founding Member SA-only Oct 2026 - Mar 2027, partner wholesale R6,999, AI at R0.15 a credit, 0% checkout fee, NG/KE/GH later. Hiring plan, gates, caps and the seed left exactly as in v2.",
         "result": f"Base min post-seed cash R{SV['k_min_post'] / 1e6:,.2f}M ({SV['k_min_post_month']}); EBITDA break-even {SV['k_be']} (sustained {SV['k_be_sus']}); profitable on the seed alone: {SV['k_profitable']}. No input was tuned to change this result."},
        {"step": 2, "change": "Conservative: the smallest fix search (gate multiplier, then a uniform non-founder salary cut) is run automatically.",
         "result": f"Conservative as modelled ({scen_defs['Conservative']['gate_mult']}x gates): min post-seed cash R{cons['SV']['k_min_post'] / 1e6:,.2f}M, profitable on seed alone: {cons['SV']['k_profitable']}. Smallest gate multiplier that passes: {diag['gm_fix']}; smallest salary cut: {diag['cut_fix']}%."},
    ]
    mb = {
        "labels": labels,
        "total_revenue_zar": [r0(V["pl_rev"][m]) for m in F.MONTHS],
        "ebitda_zar": [r0(V["ebitda"][m]) for m in F.MONTHS],
        "operating_cash_flow_zar": [r0(V["op_cf"][m]) for m in F.MONTHS],
        "closing_cash_zar": [r0(V["close_cash"][m]) for m in F.MONTHS],
        "min_cash_buffer_zar": [r0(V["buffer_line"][m]) for m in F.MONTHS],
        "subscription_mrr_net_zar": [r0(V["subrev_net"][m]) for m in F.MONTHS],
        "founding_member_discount_zar": [r0(V["fm_disc_total"][m]) for m in F.MONTHS],
        "paying_workspaces": [r0(V["tot_close"][m]) for m in F.MONTHS],
        "active_free_users": [r0(V["free_active"][m]) for m in F.MONTHS],
        "paying_workspaces_by_segment": {I.SEG_SHORT[s]: [round(V[f"seg_close_{s}"][m], 1) for m in F.MONTHS] for s in I.SEGMENTS},
        "paying_workspaces_by_market": {I.MARKET_SHORT[r]: [round(V[f"cust_{r}"][m], 1) for m in F.MONTHS] for r in I.MARKETS},
        "headcount": [r0(V["fte_total"][m]) for m in F.MONTHS],
        "markers": {
            "seed_month_index": int(p["seed_month"]) - 1, "first_group_last_month_index": int(p["first_group_end"]) - 1,
            "founding_member_window_indices": {I.MARKET_SHORT[r]: [m - 1 for m in F.MONTHS if V[f"win_{r}"][m] > 0] for r in I.WINDOW_MKTS},
            "launch_month_index": {I.MARKET_SHORT[r]: idx_of(SV[f"k_launch_num_{r}"]) for r in I.NONZA},
            "breakeven_month_index": idx_of(SV["k_be_num"]), "breakeven_sustained_month_index": idx_of(SV["k_be_sus_num"]),
            "min_post_seed_cash_month_index": int(SV["k_min_post_num"]) - 1,
        },
    }
    fm_cost = {f"FY{y}": r0(AV["a_fm_cost"][y]) for y in A.YEARS}
    js = {
        "model": "FluxMuse Financial Model", "version": W.VERSION, "company": "Fluxmuse Pty Ltd", "model_date": W.MODEL_DATE,
        "workbook": "06_Financial_Model/FluxMuse_Financial_Model.xlsx",
        "disclaimer": "Forward-looking projections. FluxMuse has no paying customers yet; every volume and rate is an assumption to replace with live data.",
        "scenario": "Base", "currency": "ZAR", "fx_zar_per_usd": p["fx"],
        "horizon": "Oct 2026 - Sep 2031 (FY1-FY5; fiscal year Oct-Sep; month 1 = Oct 2026)",
        "seed_zar": r0(p["seed_amount"]), "seed_usd": r0(p["seed_amount"] / p["fx"]), "seed_close_month": F.mlabel(p["seed_month"]),
        "series_a_zar": 0, "opening_cash_zar": r0(p["opening_cash"]),
        "pre_seed_bridge_required_zar": r0(SV["k_bridge"]), "min_cash_buffer_zar": r0(p["min_cash_buffer"]),
        "min_cash_zar": r0(SV["k_min_cash"]), "min_cash_month": SV["k_min_cash_month"],
        "min_post_seed_cash_zar": r0(SV["k_min_post"]), "min_post_seed_cash_month": SV["k_min_post_month"],
        "breakeven_month": SV["k_be"], "breakeven_month_sustained": SV["k_be_sus"],
        "cashflow_positive_month": SV["k_cfpos"], "cashflow_positive_month_sustained": SV["k_cfpos_sus"],
        "profitable_on_seed_alone": {s: res[s]["SV"]["k_profitable"] == "Yes" for s in I.SCENARIOS},
        "annual": [fy_block(base, y) for y in A.YEARS],
        "cash": {
            "opening_cash_zar": r0(p["opening_cash"]), "seed_raise_zar": r0(p["seed_amount"]), "seed_raise_usd": r0(p["seed_amount"] / p["fx"]),
            "seed_month": F.mlabel(p["seed_month"]), "series_a_included": False,
            "break_even_month": SV["k_be"], "break_even_month_sustained": SV["k_be_sus"],
            "cash_flow_positive_month": SV["k_cfpos"], "cash_flow_positive_month_sustained": SV["k_cfpos_sus"],
            "min_cash_zar": r0(SV["k_min_cash"]), "min_cash_month": SV["k_min_cash_month"],
            "min_post_seed_cash_zar": r0(SV["k_min_post"]), "min_post_seed_cash_month": SV["k_min_post_month"],
            "min_cash_buffer_zar": r0(SV["k_buffer"]), "headroom_over_buffer_zar": r0(SV["k_headroom"]),
            "pre_seed_bridge_required_zar": r0(SV["k_bridge"]), "pre_seed_min_cash_month": SV["k_pre_min_month"],
            "months_from_seed_to_cash_trough": r0(SV["k_trough_months"]),
            "runway_at_seed_close_months": SV["k_runway_seed"] if isinstance(SV["k_runway_seed"], str) else round(SV["k_runway_seed"], 1),
            "avg_monthly_net_burn_12m_after_seed_zar": r0(SV["k_burn"]), "cash_runs_out": SV["k_runway_out"],
        },
        "constraint_checks": {s: constraint_check(res[s]) for s in I.SCENARIOS},
        "first_group": {"per_month": p["first_group_n"], "months": f"Oct 2026 - {F.mlabel(p['first_group_end'])}",
                        "total_workspaces": p["first_group_n"] * p["first_group_end"], "solo_share_pct": round(p["first_mix_SO"] * 100),
                        "setup_cost_zar_per_month": r0(p["first_group_cost"]),
                        "note": "A small first group of South African businesses set up by hand, paying list price less Founding Member from the first bill. Not a pilot, not free. [[CONFIRM]]"},
        "free_plan": {"ai_credits_per_month": p["free_credits"], "zar_per_credit_provider_cost": p["ai_cost_1k"] / 1000,
                      "direct_paid_share_of_signups_pct": {"Solo": round(p["conv_SO"] * 100, 1), "SMEs": round(p["conv_SM"] * 100, 1)},
                      "monthly_upgrade_pct": round(p["free_conv"] * 100, 2), "monthly_dormancy_pct": round(p["free_dormancy"] * 100, 1),
                      "implied_lifetime_upgrade_pct": round(p["free_conv"] / (p["free_conv"] + p["free_dormancy"]) * 100, 1),
                      "hosting_zar_per_active_user_month": p["free_hosting"],
                      "active_free_users_fy1_fy5": [r0(AV["a_free_active"][y]) for y in A.YEARS],
                      "free_to_paid_upgrades_fy1_fy5": [r0(AV["a_free_conv"][y]) for y in A.YEARS],
                      "free_plan_cost_zar_fy1_fy5": [r0(AV["a_free_cost"][y]) for y in A.YEARS],
                      "credit_cost_source": "R0.15 per credit: supabase/functions/_shared/ai-credit-math.ts DEFAULT_ZAR_PER_CREDIT and platform_billing_config ai.zar_per_credit (migration 20260926110000). CURRENT_OFFER's 'about R1 per credit' is not what the product uses. Free allowance 60 credits (migration 20260926100000), not the 100 set on 18 Sep."},
        "founding_member": {
            "option_modelled": {1: "Founding Member", 2: "None"}[p["disc_option"]],
            "monthly_plans": f"{p['fm_disc']:.0%} off the first 2 monthly bills; churn of {p['fm_new_churn']:.0%} between bill 1 and 2 applied to the second discounted bill",
            "annual_plans": "No Founding Member discount modelled on annual plans [[CONFIRM]]",
            "eligible": "South African Solo and SME sign-ups (Nano to Scale), including the first group and Free users who upgrade while it runs; not Agency, Corporate or Custom; does not stack with partner wholesale",
            "windows": {"South Africa": f"{F.mlabel(p['fm_start'])} - {F.mlabel(p['fm_end'])} (end date proposed, not set) [[CONFIRM]]", "Nigeria / Kenya / Ghana": "none", "USD markets": "none"},
            "window_signup_uplift_pct": round(p["fm_uplift"] * 100),
            "discount_cost_by_fy_zar": fm_cost,
            "discount_cost_by_market_fy_zar": {I.MARKET_SHORT[m]: [r0(AV[f"a_fm_cost_{m}"][y]) for y in A.YEARS] for m in I.WINDOW_MKTS},
            "launch_discounts_pct_of_gross_subscriptions_fy1_fy5": [round(AV["a_disc_pct"][y] * 100, 2) for y in A.YEARS],
            "option_comparison": {name: {"fy1_revenue_zar": r0(r["AV"]["a_rev"][1]), "fy2_revenue_zar": r0(r["AV"]["a_rev"][2]),
                                         "discount_cost_fy1_fy3_zar": r0(sum(r["AV"]["a_fm_cost"][1:4])),
                                         "min_post_seed_cash_zar": r0(r["SV"]["k_min_post"]),
                                         "profitable_on_seed_alone": r["SV"]["k_profitable"] == "Yes"} for name, r in sens["disc"].items()},
        },
        "markets": {
            "sequence": ["South Africa (only market until NG/KE/GH checkout is live)", "Nigeria, Kenya, Ghana (wave 1, once Fincra/pawaPay are live)", "Rest of rail-covered Africa (19 countries, USD, self-serve)", "Botswana & Namibia (coming soon: off)"],
            "launch_months": {s: {"South Africa": F.mlabel(p["launch_ZA"]), **{I.MARKET_SHORT[m]: res[s]["SV"][f"k_launch_{m}"] for m in I.NONZA}} for s in I.SCENARIOS},
            "planned_earliest_launch_month": {I.MARKET_SHORT[m]: F.mlabel(p[f"launch_plan_{m}"]) for m in I.NONZA},
            "launch_mrr_gate_zar": {I.MARKET_SHORT[m]: r0(p[f"launch_gate_{m}"]) for m in I.NONZA},
            "launch_costs_zar": {I.MARKET_SHORT[m]: {"launch_marketing": r0(p.get(f"launch_mkt_{m}", 0)), "compliance_one_off": r0(p[f"entry_{m}"]),
                                                    "compliance_monthly": r0(p[f"ongoing_{m}"])} for m in I.NONZA},
            "gated_countries": "Zero revenue and customers in every scenario",
            "why": "Paid checkout outside South Africa is not available until the Fincra/pawaPay accounts are live, so v3 moves the plan months about five months later than v2 (Apr 2028 / Jul 2028 / Oct 2028; Rest of Africa May 2029) and keeps the rising MRR gates. Each launch happens at the later of its plan month and its gate.",
        },
        "price_tables": price_tables(p),
        "fx_shock": {"definition": f"ZAR 15% stronger vs NGN, KES, GHS and USD from {F.mlabel(p['fx_shock_month'])} (month {p['fx_shock_month']}), Base case", "results": fxr},
        "unit_economics_fy3": {"by_segment": segs, "by_tier": tiers,
                               "blended": {"arpa_zar_per_month": r0(AV["u_arpa"][ue]), "cac_zar": r0(AV["u_cac"][ue]), "ltv_zar": r0(AV["u_ltv"][ue]),
                                           "ltv_to_cac": round(AV["u_ltvcac"][ue], 1), "cac_payback_months": round(AV["u_payback"][ue], 1),
                                           "software_gross_margin_pct": round(AV["u_gm"][ue] * 100, 1)},
                               "method": "LTV = gross list ARPA x software gross margin / monthly logo churn. Solo/SME CAC = paid acquisition + shared brand, launch and marketing payroll by new-customer mix (Free upgrades and the first group count as new customers); Agencies = partner programme + partnerships team per new agency; Corporate and Enterprise = inbound handling cost per deal."},
        "use_of_funds": strip_exact(uof),
        "market_sizing": {"tam_msmes": 44000000, "sam_smbs": 3500000, "som_share_of_sam_pct": 0.5, "som_paying_workspaces": 17500,
                          "sam_value_zar_per_year_at_usd25": r0(3500000 * 25 * 12 * p["fx"]),
                          "model_fy5_workspaces_pct_of_som": round(AV["a_cust"][5] / 17500 * 100, 1),
                          "sources": "TAM: IFC/World Bank est.; SAM & SOM: planning estimates (facts file §5). All estimates; verify before external use."},
        "scenarios": {s: scen_brief(res[s]) for s in I.SCENARIOS},
        "scenario_definitions": scen_defs,
        "conservative_diagnostics": {
            "as_modelled": {"min_post_seed_cash_zar": r0(cons["SV"]["k_min_post"]), "shortfall_vs_buffer_zar": r0(cons["SV"]["k_buf_short"]),
                            "profitable_on_seed_alone": ok(cons)},
            "with_base_gates_1_00x": {"min_post_seed_cash_zar": r0(cb["SV"]["k_min_post"]), "min_post_seed_cash_month": cb["SV"]["k_min_post_month"],
                                      "shortfall_vs_buffer_zar": r0(cb["SV"]["k_buf_short"]), "profitable_on_seed_alone": ok(cb)},
            "smallest_fix_from": diag["fix_from"], "smallest_gate_multiplier_that_passes": diag["gm_fix"],
            "smallest_uniform_non_founder_salary_cut_pct_that_passes": diag["cut_fix"],
        },
        "calibration_iterations": iterations,
        "base_levers_to_pass_r25m_test": {k: (r0(v) if k.endswith("_zar") and v is not None else v) for k, v in sens["levers"].items()},
        "sensitivity_base": {
            "rows_churn_multiplier": sens["grid"]["churn"], "cols_new_customer_volume_multiplier": sens["grid"]["vol"],
            "fy3_revenue_zar_m": [[rm(x) for x in row] for row in sens["grid"]["tables"][0]["values"]],
            "fy5_revenue_zar_m": [[rm(x) for x in row] for row in sens["grid"]["tables"][1]["values"]],
            "fy3_ebitda_zar_m": [[rm(x) for x in row] for row in sens["grid"]["tables"][2]["values"]],
            "fy5_ebitda_zar_m": [[rm(x) for x in row] for row in sens["grid"]["tables"][3]["values"]],
            "min_post_seed_cash_zar_m": [[rm(x, 2) for x in row] for row in sens["grid"]["tables"][4]["values"]],
        },
        "free_conversion_sensitivity": {name: {"fy1_revenue_zar": r0(r["AV"]["a_rev"][1]), "fy3_revenue_zar": r0(r["AV"]["a_rev"][3]),
                                               "fy5_ebitda_zar": r0(r["AV"]["a_ebitda"][5]),
                                               "min_post_seed_cash_zar": r0(r["SV"]["k_min_post"]),
                                               "profitable_on_seed_alone": r["SV"]["k_profitable"] == "Yes"} for name, r in sens["pilot"].items()},
        "key_assumptions": ta,
        "founder_confirmations_needed": confirmations,
        "not_modelled": ["Campaign Financing (upside only)", "Partner referral commission (undecided)", "Series A (optional acceleration only)",
                         "Botswana & Namibia revenue (switched off until a rail covers them)", "Gated countries",
                         "Any FluxMuse fee on checkout GMV (none in the current offer)", "VAT (not VAT-registered)",
                         "AI Voice minute revenue on Corporate/Agency prepaid balances", "NG/KE/GH launch offers"],
        "monthly_base": mb,
        "scenario_monthly_closing_cash_zar": {s: [r0(res[s]["V"]["close_cash"][m]) for m in F.MONTHS] for s in I.SCENARIOS},
    }
    return js


def main():
    os.makedirs(OUT, exist_ok=True)
    res = {s: pack(k) for k, s in enumerate(I.SCENARIOS, start=1)}
    sens = sensitivity(res)
    base = pack(2)                      # restore Base into module state
    uof = use_of_funds(base["p"])
    wb = W.build_workbook(base["p"], sens)
    n, n_cmp, errors, mism = verify(wb, base, uof)
    print(f"formulas: {n:,}  cells compared with the Python mirror: {n_cmp:,}  evaluation errors: {len(errors)}  mismatches: {len(mism)}")
    for e in (errors + mism)[:25]:
        print("  ", e)
    if errors or mism:
        sys.exit("verification failed")
    wb.save(XLSX)
    print("saved", XLSX)
    js = summary_json(res, sens, uof)
    with open(JSON_PATH, "w") as fh:
        json.dump(js, fh, indent=2, ensure_ascii=False)
    print("saved", JSON_PATH)
    charts = os.path.join(HERE, "charts.py")
    if os.path.exists(charts) and "--no-charts" not in sys.argv:
        subprocess.run([sys.executable, charts], check=True)


if __name__ == "__main__":
    np.seterr(all="ignore")
    main()
