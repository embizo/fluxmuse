"""Derive detail tables for the business plan from the financial model's Python mirror (Base case).

Imports docs/go-to-market/_build/fm_*.py and financial_model.run() WITHOUT modifying them, and writes
derived_tables.json next to this file. Every derived figure is a sum/end-of-year value of mirror rows
that the workbook itself computes (Costs, P&L, Cash_Flow sheets).

    venv/bin/python docs/go-to-market/_build/business_plan/derive_model_tables.py
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BUILD = HERE.parent
sys.path.insert(0, str(BUILD))

import financial_model as FM  # noqa: E402
import fm_inputs as I  # noqa: E402
from fm_rows import mlabel  # noqa: E402

SUMMARY = BUILD.parent / "06_Financial_Model" / "model_summary.json"


def main():
    p, V, AV, SV = FM.run(2)
    fy_end = [12, 24, 36, 48, 60]
    out = {"source": "FluxMuse Financial Model v2 Python mirror, Base case (financial_model.run(2))"}

    # headcount by department at FY end
    out["headcount_by_dept_fy_end"] = {
        d: [round(V[f"fte_dept_{d}"][m]) for m in fy_end] for d in I.DEPTS}
    out["headcount_total_fy_end"] = [round(V["fte_total"][m]) for m in fy_end]
    out["payroll_by_dept_zar_fy"] = {
        d: [round(sum(V[f"cost_dept_{d}"][m] for m in range(1 + 12 * y, 13 + 12 * y))) for y in range(5)]
        for d in I.DEPTS if f"cost_dept_{d}" in V}

    # roles: first month hired (Base)
    roles = []
    for i, ro in enumerate(I.ROLES):
        first = next((m for m in range(1, 61) if V[f"fte_{i}"][m] > 0), None)
        roles.append({"role": ro["name"], "dept": ro["dept"], "count": ro["count"], "ctc_zar": ro["ctc"],
                      "first_month": mlabel(first) if first else "Not hired within FY5",
                      "fy": f"FY{(first - 1) // 12 + 1}" if first else "-",
                      "mrr_gate_zar": ro["gate"]})
    out["roles"] = roles

    # annual P&L and cash-flow lines
    def a(key):
        return [round(AV[key][y]) for y in range(1, 6)]
    out["annual"] = {k: a(k) for k in ["a_rev", "a_cogs", "a_gp", "a_opex", "a_ebitda", "a_tax", "a_ni",
                                       "a_opcf", "a_funding", "a_close_cash", "a_min_cash"]}
    cf = {}
    for key in [k for k in V if k.startswith("cf_") or k.startswith("cogs_")] + ["d_dr", "d_ar", "op_cf", "seed_in", "net_cf"]:
        cf[key] = [round(sum(V[key][m] for m in range(1 + 12 * y, 13 + 12 * y))) for y in range(5)]
    out["cash_flow_rows_fy_sum"] = cf
    out["opening_cash_fy"] = [500000] + [round(AV["a_close_cash"][y]) for y in range(1, 5)]

    # cross-check against model_summary.json
    js = json.loads(SUMMARY.read_text())
    mism = []
    for y in range(5):
        blk = js["annual"][y]
        for jk, ak in [("total_revenue_zar", "a_rev"), ("ebitda_zar", "a_ebitda"), ("closing_cash_zar", "a_close_cash"),
                       ("gross_profit_zar", "a_gp"), ("operating_cash_flow_zar", "a_opcf"), ("headcount_end_fy", "a_fte")]:
            if abs(blk[jk] - round(AV[ak][y + 1])) > 1:
                mism.append((blk["fy"], jk, blk[jk], AV[ak][y + 1]))
    out["crosscheck_vs_model_summary_mismatches"] = mism
    (HERE / "derived_tables.json").write_text(json.dumps(out, indent=1))
    print("mismatches vs model_summary.json:", mism)
    print(json.dumps({k: out[k] for k in ["headcount_by_dept_fy_end", "headcount_total_fy_end", "annual"]}, indent=0))
    print(json.dumps(out["cash_flow_rows_fy_sum"], indent=0))
    for r in roles:
        print(r["fy"], r["first_month"], r["count"], r["role"])


if __name__ == "__main__":
    main()
