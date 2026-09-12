"""FluxMuse financial model v2: annual (FY1-FY5), unit-economics and key-output rows.

Same dual-implementation pattern as fm_rows: xl(y) formula text + py(y) mirror.
Fiscal year y runs Oct..Sep; FY y = model months 12(y-1)+1 .. 12y.
"""
from collections import defaultdict

import fm_rows as F
from fm_inputs import AD, MARKET_SHORT, MARKETS, NONZA, SEG_SHORT, SEGMENTS, TIER_NAME, TIERS, WINDOW_MKTS

YEARS = range(1, 6)
ANN_FIRST_ROW = 7
AROWS = []
ANNPOS = {}
AV = defaultdict(lambda: [0.0] * 6)
SROWS = []
SCALPOS = {}
SV = {}
ACUR = [None]


def acol(y):
    return F.get_column_letter(2 + y)


def ASEC(sheet, title):
    AROWS.append(dict(kind="section", sheet=sheet, label=title))


def AR(sheet, key, label, unit, fmt, xl, py, bold=False):
    AROWS.append(dict(kind="row", sheet=sheet, key=key, label=label, unit=unit, fmt=fmt, xl=xl, py=py, bold=bold))


def _mref_sheet(key):
    sh, r = F.ROWPOS[key]
    return F.sref(sh), r


def FS(key, y):
    sh, r = _mref_sheet(key)
    return f"SUM({sh}!{F.col(12 * (y - 1) + 1)}{r}:{F.col(12 * y)}{r})"


def FMIN(key, y):
    sh, r = _mref_sheet(key)
    return f"MIN({sh}!{F.col(12 * (y - 1) + 1)}{r}:{F.col(12 * y)}{r})"


def FE(key, y):
    sh, r = _mref_sheet(key)
    return f"{sh}!{F.col(12 * y)}{r}"


def AY(key, y):
    sh, r = ANNPOS[key]
    return f"{acol(y)}{r}" if sh == ACUR[0] else f"{F.sref(sh)}!{acol(y)}{r}"


def fs(key, y):
    return sum(F.V[key][12 * (y - 1) + 1:12 * y + 1])


def fmin(key, y):
    return min(F.V[key][12 * (y - 1) + 1:12 * y + 1])


def fe(key, y):
    return F.V[key][12 * y]


def ay(key, y):
    return AV[key][y]


def guard_div(num_xl, den_xl):
    return f"IF({den_xl}=0,0,{num_xl}/{den_xl})"


def gdiv(a, b):
    return 0.0 if b == 0 else a / b


# =============================================================================
# ANNUAL SUMMARY
# =============================================================================
AS = "Annual_Summary"
ASEC(AS, "Revenue by stream (gross subscriptions -> launch discounts -> net)")
SUBS = [("a_rev_subs_gross", "Subscriptions (gross)", "pl_rev_subs_gross"), ("a_disc_fm", "less: Founding Member discount", "pl_disc_fm"),
        ("a_disc_pilot", "less: Pilot Founding terms discount", "pl_disc_pilot")]
for k, lab, src in SUBS:
    AR(AS, k, lab, "R", "zar", lambda y, src=src: FS(src, y), lambda y, src=src: fs(src, y))
AR(AS, "a_rev_subs", "Subscriptions (net)", "R", "zar", lambda y: "+".join(AY(k, y) for k, _, _ in SUBS),
   lambda y: sum(ay(k, y) for k, _, _ in SUBS), bold=True)
AREV = [("a_rev_topup", "AI-credit top-ups", "pl_rev_topup"), ("a_rev_wa", "WhatsApp messaging (pass-through + margin)", "pl_rev_wa"),
        ("a_rev_commerce", "Commerce platform fees (Upside only)", "pl_rev_commerce"),
        ("a_rev_ent_setup", "Enterprise setup fees", "pl_rev_ent_setup"), ("a_rev_agency_setup", "Agency white-label setup fees", "pl_rev_agency_setup")]
for k, lab, src in AREV:
    AR(AS, k, lab, "R", "zar", lambda y, src=src: FS(src, y), lambda y, src=src: fs(src, y))
AR(AS, "a_rev", "Total revenue", "R", "zar", lambda y: AY("a_rev_subs", y) + "+" + "+".join(AY(k, y) for k, _, _ in AREV),
   lambda y: ay("a_rev_subs", y) + sum(ay(k, y) for k, _, _ in AREV), bold=True)
AR(AS, "a_rev_usd", "Total revenue (US$)", "US$", "usd", lambda y: f"{AY('a_rev', y)}/{AD('fx')}", lambda y: ay("a_rev", y) / F.P["fx"])
AR(AS, "a_growth", "Revenue growth y/y", "%", "pct",
   lambda y: '"n/a"' if y == 1 else guard_div(f"({AY('a_rev', y)}-{AY('a_rev', y - 1)})", AY("a_rev", y - 1)),
   lambda y: "n/a" if y == 1 else gdiv(ay("a_rev", y) - ay("a_rev", y - 1), ay("a_rev", y - 1)))
ASEC(AS, "Launch discounts (cost of the offer, positive = revenue given up)")
AR(AS, "a_fm_cost", "Founding Member discount cost", "R", "zar", lambda y: FS("fm_disc_total", y), lambda y: fs("fm_disc_total", y))
for r in WINDOW_MKTS:
    AR(AS, f"a_fm_cost_{r}", f"of which {MARKET_SHORT[r]}", "R", "zar", lambda y, r=r: FS("fm_disc_" + r, y), lambda y, r=r: fs("fm_disc_" + r, y))
AR(AS, "a_pilot_cost", "Pilot Founding terms discount cost", "R", "zar", lambda y: FS("pilot_disc_rev", y), lambda y: fs("pilot_disc_rev", y))
AR(AS, "a_disc_pct", "Launch discounts as % of gross subscriptions", "%", "pct",
   lambda y: guard_div(f"({AY('a_fm_cost', y)}+{AY('a_pilot_cost', y)})", AY("a_rev_subs_gross", y)),
   lambda y: gdiv(ay("a_fm_cost", y) + ay("a_pilot_cost", y), ay("a_rev_subs_gross", y)))
ASEC(AS, "Net subscription revenue by market")
for r in MARKETS:
    AR(AS, f"a_subnet_{r}", MARKET_SHORT[r], "R", "zar", lambda y, r=r: FS("subnet_" + r, y), lambda y, r=r: fs("subnet_" + r, y))
ASEC(AS, "Gross profit")
AR(AS, "a_cogs", "Cost of revenue", "R", "zar", lambda y: FS("pl_cogs", y), lambda y: fs("pl_cogs", y))
AR(AS, "a_gp", "Gross profit", "R", "zar", lambda y: f"{AY('a_rev', y)}-{AY('a_cogs', y)}", lambda y: ay("a_rev", y) - ay("a_cogs", y), bold=True)
AR(AS, "a_gm", "Gross margin % (all revenue)", "%", "pct", lambda y: guard_div(AY("a_gp", y), AY("a_rev", y)), lambda y: gdiv(ay("a_gp", y), ay("a_rev", y)))
AR(AS, "a_sw_gm", "Software gross margin %", "%", "pct", lambda y: f"IF({FS('sw_rev', y)}=0,0,1-{FS('sw_cogs', y)}/{FS('sw_rev', y)})",
   lambda y: 0.0 if fs("sw_rev", y) == 0 else 1 - fs("sw_cogs", y) / fs("sw_rev", y))
ASEC(AS, "Operating expenses by category")
AOPEX = [("a_opex_hc", "Payroll (excl. customer success)", "pl_hc"), ("a_opex_mkt", "Marketing & sales programmes", "pl_mkt"),
         ("a_opex_ga", "G&A (non-payroll)", "pl_ga"), ("a_opex_legal", "Meta, legal & compliance", "pl_legal"),
         ("a_opex_tools", "Software & tools", "pl_tools"), ("a_opex_travel", "Travel", "pl_travel")]
for k, lab, src in AOPEX:
    AR(AS, k, lab, "R", "zar", lambda y, src=src: FS(src, y), lambda y, src=src: fs(src, y))
AR(AS, "a_opex", "Total operating expenses", "R", "zar", lambda y: "+".join(AY(k, y) for k, _, _ in AOPEX),
   lambda y: sum(ay(k, y) for k, _, _ in AOPEX), bold=True)
AR(AS, "a_paid", "memo: paid acquisition spend (after cap)", "R", "zar", lambda y: FS("paid_spend", y), lambda y: fs("paid_spend", y))
AR(AS, "a_paid_funded", "memo: share of desired paid acquisition funded by the cap", "%", "pct",
   lambda y: guard_div(FS("paid_spend", y), FS("paid_des", y)), lambda y: gdiv(fs("paid_spend", y), fs("paid_des", y)))
ASEC(AS, "Profit")
AR(AS, "a_ebitda", "EBITDA", "R", "zar", lambda y: f"{AY('a_gp', y)}-{AY('a_opex', y)}", lambda y: ay("a_gp", y) - ay("a_opex", y), bold=True)
AR(AS, "a_ebitda_pct", "EBITDA margin %", "%", "pct", lambda y: guard_div(AY("a_ebitda", y), AY("a_rev", y)), lambda y: gdiv(ay("a_ebitda", y), ay("a_rev", y)))
AR(AS, "a_ebitda_usd", "EBITDA (US$)", "US$", "usd", lambda y: f"{AY('a_ebitda', y)}/{AD('fx')}", lambda y: ay("a_ebitda", y) / F.P["fx"])
AR(AS, "a_tax", "Income tax", "R", "zar", lambda y: FS("tax", y), lambda y: fs("tax", y))
AR(AS, "a_ni", "Net income", "R", "zar", lambda y: f"{AY('a_ebitda', y)}-{AY('a_tax', y)}", lambda y: ay("a_ebitda", y) - ay("a_tax", y), bold=True)
ASEC(AS, "Cash")
AR(AS, "a_opcf", "Operating cash flow (before funding)", "R", "zar", lambda y: FS("op_cf", y), lambda y: fs("op_cf", y))
AR(AS, "a_funding", "Equity funding received", "R", "zar", lambda y: f"{FS('seed_in', y)}+{FS('seriesA_in', y)}",
   lambda y: fs("seed_in", y) + fs("seriesA_in", y))
AR(AS, "a_close_cash", "Closing cash (end of FY)", "R", "zar", lambda y: FE("close_cash", y), lambda y: fe("close_cash", y), bold=True)
AR(AS, "a_min_cash", "Lowest month-end cash in FY", "R", "zar", lambda y: FMIN("close_cash", y), lambda y: fmin("close_cash", y))
ASEC(AS, "Paying workspaces at end of FY: by segment")
for sg in SEGMENTS:
    AR(AS, f"a_seg_{sg}", SEG_SHORT[sg], "workspaces", "n0", lambda y, sg=sg: FE("seg_close_" + sg, y), lambda y, sg=sg: fe("seg_close_" + sg, y))
ASEC(AS, "Paying workspaces at end of FY: by market (gated countries = 0)")
for r in MARKETS:
    AR(AS, f"a_mkt_{r}", MARKET_SHORT[r], "workspaces", "n0", lambda y, r=r: FE("cust_" + r, y), lambda y, r=r: fe("cust_" + r, y))
ASEC(AS, "Paying workspaces at end of FY: by tier")
for t in TIERS:
    AR(AS, f"a_cust_{t}", TIER_NAME[t], "workspaces", "n0", lambda y, t=t: FE(f"tier_close_{t}", y), lambda y, t=t: fe(f"tier_close_{t}", y))
AR(AS, "a_cust", "Total paying workspaces", "workspaces", "n0", lambda y: "+".join(AY(f"a_cust_{t}", y) for t in TIERS),
   lambda y: sum(ay(f"a_cust_{t}", y) for t in TIERS), bold=True)
ASEC(AS, "New customers acquired in FY by segment (excl. upgrades)")
for sg in SEGMENTS:
    AR(AS, f"a_segnew_{sg}", SEG_SHORT[sg], "workspaces", "n0", lambda y, sg=sg: FS("seg_new_" + sg, y), lambda y, sg=sg: fs("seg_new_" + sg, y))
AR(AS, "a_new", "New paying workspaces in FY", "workspaces", "n0", lambda y: FS("tot_newc", y), lambda y: fs("tot_newc", y))
AR(AS, "a_churned", "Churned workspaces in FY", "workspaces", "n0", lambda y: FS("tot_churn", y), lambda y: fs("tot_churn", y))
ASEC(AS, "Recurring revenue & ARPA")
AR(AS, "a_mrr", "Net subscription MRR (September)", "R", "zar", lambda y: FE("subrev_net", y), lambda y: fe("subrev_net", y))
AR(AS, "a_arr", "Subscription ARR (Sept net MRR x 12)", "R", "zar", lambda y: f"{AY('a_mrr', y)}*12", lambda y: ay("a_mrr", y) * 12, bold=True)
AR(AS, "a_arr_usd", "Subscription ARR (US$)", "US$", "usd", lambda y: f"{AY('a_arr', y)}/{AD('fx')}", lambda y: ay("a_arr", y) / F.P["fx"])
AR(AS, "a_arpa", "Blended subscription ARPA (net)", "R / workspace / month", "zar",
   lambda y: guard_div(FS("pl_rev_subs", y), FS("tot_close", y)), lambda y: gdiv(fs("pl_rev_subs", y), fs("tot_close", y)))
AR(AS, "a_arpa_total", "Total revenue per workspace", "R / workspace / month", "zar",
   lambda y: guard_div(FS("pl_rev", y), FS("tot_close", y)), lambda y: gdiv(fs("pl_rev", y), fs("tot_close", y)))
ASEC(AS, "Team")
AR(AS, "a_fte", "Headcount at end of FY", "FTE", "n0", lambda y: FE("fte_total", y), lambda y: fe("fte_total", y))
AR(AS, "a_rev_per_fte", "Revenue per FTE (end-of-FY headcount)", "R", "zar", lambda y: guard_div(AY("a_rev", y), AY("a_fte", y)),
   lambda y: gdiv(ay("a_rev", y), ay("a_fte", y)))

# =============================================================================
# UNIT ECONOMICS (by segment; tier memo; blended)
# =============================================================================
UE = "Unit_Economics"
ASEC(UE, "By segment: ARPA (gross list), churn, LTV = ARPA x software GM % / monthly churn")
for sg in SEGMENTS:
    AR(UE, f"u_arpa_{sg}", f"ARPA: {SEG_SHORT[sg]}", "R / month", "zar",
       lambda y, sg=sg: guard_div(FS("subgross_seg_" + sg, y), FS("seg_close_" + sg, y)),
       lambda y, sg=sg: gdiv(fs("subgross_seg_" + sg, y), fs("seg_close_" + sg, y)))
AR(UE, "u_gm", "Software gross margin % (used for LTV)", "%", "pct", lambda y: AY("a_sw_gm", y), lambda y: ay("a_sw_gm", y))
for sg in SEGMENTS:
    AR(UE, f"u_churn_{sg}", f"Monthly logo churn: {SEG_SHORT[sg]} (churned / opening)", "%", "pct",
       lambda y, sg=sg: guard_div(FS("seg_churn_" + sg, y), FS("seg_open_" + sg, y)),
       lambda y, sg=sg: gdiv(fs("seg_churn_" + sg, y), fs("seg_open_" + sg, y)))
for sg in SEGMENTS:
    AR(UE, f"u_ltv_{sg}", f"LTV: {SEG_SHORT[sg]}", "R", "zar",
       lambda y, sg=sg: f"IF({AY('u_churn_' + sg, y)}=0,0,{AY('u_arpa_' + sg, y)}*{AY('u_gm', y)}/{AY('u_churn_' + sg, y)})",
       lambda y, sg=sg: gdiv(ay("u_arpa_" + sg, y) * ay("u_gm", y), ay("u_churn_" + sg, y)), bold=True)
ASEC(UE, "By segment: acquisition spend, new customers, CAC (self-serve brand/launch/marketing payroll shared by new-customer mix)")
SS_OTHER = ["opex_brand", "opex_launch_mkt", "opex_rest_mkt", "cost_dept_Marketing"]


def _share_xl(sg, y):
    return guard_div(FS("seg_new_" + sg, y), f"({FS('seg_new_SO', y)}+{FS('seg_new_SM', y)})")


def _share_py(sg, y):
    return gdiv(fs("seg_new_" + sg, y), fs("seg_new_SO", y) + fs("seg_new_SM", y))


def _spend_xl(sg, y):
    if sg in ("SO", "SM"):
        return f"{FS('paid_spend_' + sg, y)}+(" + "+".join(FS(k, y) for k in SS_OTHER) + f")*{_share_xl(sg, y)}"
    if sg == "AG":
        return f"{FS('opex_partner', y)}+{FS('pm_team_cost', y)}"
    return FS("opex_ent_sales", y)


def _spend_py(sg, y):
    if sg in ("SO", "SM"):
        return fs("paid_spend_" + sg, y) + sum(fs(k, y) for k in SS_OTHER) * _share_py(sg, y)
    if sg == "AG":
        return fs("opex_partner", y) + fs("pm_team_cost", y)
    return fs("opex_ent_sales", y)


for sg in SEGMENTS:
    AR(UE, f"u_spend_{sg}", f"Acquisition spend: {SEG_SHORT[sg]}", "R", "zar", lambda y, sg=sg: _spend_xl(sg, y), lambda y, sg=sg: _spend_py(sg, y))
for sg in SEGMENTS:
    AR(UE, f"u_new_{sg}", f"New customers: {SEG_SHORT[sg]}", "workspaces", "n0", lambda y, sg=sg: FS("seg_new_" + sg, y),
       lambda y, sg=sg: fs("seg_new_" + sg, y))
for sg in SEGMENTS:
    AR(UE, f"u_cac_{sg}", f"CAC: {SEG_SHORT[sg]}", "R", "zar", lambda y, sg=sg: guard_div(AY("u_spend_" + sg, y), AY("u_new_" + sg, y)),
       lambda y, sg=sg: gdiv(ay("u_spend_" + sg, y), ay("u_new_" + sg, y)), bold=True)
for sg in SEGMENTS:
    AR(UE, f"u_ltvcac_{sg}", f"LTV:CAC: {SEG_SHORT[sg]}", "x", "x1", lambda y, sg=sg: guard_div(AY("u_ltv_" + sg, y), AY("u_cac_" + sg, y)),
       lambda y, sg=sg: gdiv(ay("u_ltv_" + sg, y), ay("u_cac_" + sg, y)))
for sg in SEGMENTS:
    AR(UE, f"u_payback_{sg}", f"CAC payback: {SEG_SHORT[sg]}", "months", "n1",
       lambda y, sg=sg: guard_div(AY("u_cac_" + sg, y), f"({AY('u_arpa_' + sg, y)}*{AY('u_gm', y)})"),
       lambda y, sg=sg: gdiv(ay("u_cac_" + sg, y), ay("u_arpa_" + sg, y) * ay("u_gm", y)))
ASEC(UE, "Memo by tier: ARPA, churn, LTV")
for t in TIERS:
    AR(UE, f"u_arpa_{t}", f"ARPA: {TIER_NAME[t]}", "R / month", "zar", lambda y, t=t: guard_div(FS("subgross_tier_" + t, y), FS("tier_close_" + t, y)),
       lambda y, t=t: gdiv(fs("subgross_tier_" + t, y), fs("tier_close_" + t, y)))
for t in TIERS:
    AR(UE, f"u_churn_{t}", f"Monthly churn: {TIER_NAME[t]}", "%", "pct", lambda y, t=t: guard_div(FS("tier_churn_" + t, y), FS("tier_open_" + t, y)),
       lambda y, t=t: gdiv(fs("tier_churn_" + t, y), fs("tier_open_" + t, y)))
for t in TIERS:
    AR(UE, f"u_ltv_{t}", f"LTV: {TIER_NAME[t]}", "R", "zar",
       lambda y, t=t: f"IF({AY('u_churn_' + t, y)}=0,0,{AY('u_arpa_' + t, y)}*{AY('u_gm', y)}/{AY('u_churn_' + t, y)})",
       lambda y, t=t: gdiv(ay("u_arpa_" + t, y) * ay("u_gm", y), ay("u_churn_" + t, y)))
ASEC(UE, "Blended")
AR(UE, "u_sm", "Total sales & marketing (programmes + marketing & sales payroll)", "R", "zar", lambda y: FS("sm_total", y), lambda y: fs("sm_total", y))
AR(UE, "u_new", "Total new paying workspaces", "workspaces", "n0", lambda y: FS("tot_newc", y), lambda y: fs("tot_newc", y))
AR(UE, "u_cac", "Blended CAC", "R", "zar", lambda y: guard_div(AY("u_sm", y), AY("u_new", y)), lambda y: gdiv(ay("u_sm", y), ay("u_new", y)), bold=True)
AR(UE, "u_arpa", "Blended subscription ARPA (net)", "R / month", "zar", lambda y: AY("a_arpa", y), lambda y: ay("a_arpa", y))
AR(UE, "u_churn", "Blended monthly logo churn (churned / opening)", "%", "pct", lambda y: guard_div(FS("tot_churn", y), FS("tot_open", y)),
   lambda y: gdiv(fs("tot_churn", y), fs("tot_open", y)))
AR(UE, "u_ltv", "Blended LTV", "R", "zar", lambda y: f"IF({AY('u_churn', y)}=0,0,{AY('u_arpa', y)}*{AY('u_gm', y)}/{AY('u_churn', y)})",
   lambda y: gdiv(ay("u_arpa", y) * ay("u_gm", y), ay("u_churn", y)), bold=True)
AR(UE, "u_ltvcac", "Blended LTV:CAC", "x", "x1", lambda y: guard_div(AY("u_ltv", y), AY("u_cac", y)), lambda y: gdiv(ay("u_ltv", y), ay("u_cac", y)), bold=True)
AR(UE, "u_payback", "Blended CAC payback", "months", "n1", lambda y: guard_div(AY("u_cac", y), f"({AY('u_arpa', y)}*{AY('u_gm', y)})"),
   lambda y: gdiv(ay("u_cac", y), ay("u_arpa", y) * ay("u_gm", y)))
ASEC(UE, "Efficiency")
AR(UE, "u_nnarr", "Net new subscription ARR", "R", "zar", lambda y: AY("a_arr", y) if y == 1 else f"{AY('a_arr', y)}-{AY('a_arr', y - 1)}",
   lambda y: ay("a_arr", y) - (ay("a_arr", y - 1) if y > 1 else 0.0))
AR(UE, "u_magic", "Magic number (net new ARR / S&M)", "x", "x2", lambda y: guard_div(AY("u_nnarr", y), AY("u_sm", y)), lambda y: gdiv(ay("u_nnarr", y), ay("u_sm", y)))
AR(UE, "u_netburn", "Net burn (negative operating cash flow)", "R", "zar", lambda y: f"MAX(0,-{AY('a_opcf', y)})", lambda y: max(0.0, -ay("a_opcf", y)))
AR(UE, "u_burn_mult", "Burn multiple (net burn / net new ARR)", "x", "x2",
   lambda y: f"IF({AY('u_nnarr', y)}<=0,\"n/a\",{AY('u_netburn', y)}/{AY('u_nnarr', y)})",
   lambda y: "n/a" if ay("u_nnarr", y) <= 0 else ay("u_netburn", y) / ay("u_nnarr", y))
AR(UE, "u_r40", "Rule of 40 (revenue growth % + EBITDA margin %)", "%", "pct",
   lambda y: '"n/a"' if y == 1 else f"{AY('a_growth', y)}+{AY('a_ebitda_pct', y)}",
   lambda y: "n/a" if y == 1 else ay("a_growth", y) + ay("a_ebitda_pct", y))

# =============================================================================
# KEY OUTPUTS (scalars, Cash_Flow sheet)
# =============================================================================
LABELS = "Revenue_Build!$C$4:$BJ$4"
NOT_IN = "Not within horizon (to Sep 2031)"


def SR(key, label, fmt, xl, py):
    SROWS.append(dict(key=key, label=label, fmt=fmt, xl=xl, py=py))


def K(key):
    return f"$B${SCALPOS[key]}"


def FULL(key):
    sh, r = F.ROWPOS[key]
    rng = f"$C${r}:$BJ${r}"
    return rng if sh == "Cash_Flow" else f"{F.sref(sh)}!{rng}"


def _lab(n):
    return NOT_IN if n == 999 else F.mlabel(int(n))


def _first(key):
    return min(F.V[key][1:])


def _month_text(num_key):
    return lambda: f"IF({K(num_key)}=999,\"{NOT_IN}\",INDEX({LABELS},{K(num_key)}))"


for base, lab, flag in [("k_be", "Break-even: first month EBITDA >= 0", "flag_be"),
                        ("k_be_sus", "Sustained break-even: EBITDA >= 0 every month thereafter", "flag_be_sus"),
                        ("k_cfpos", "Cash-flow positive: first month operating cash flow >= 0", "flag_cfpos"),
                        ("k_cfpos_sus", "Sustained cash-flow positive: operating cash flow >= 0 every month thereafter", "flag_cfpos_sus")]:
    SR(base + "_num", f"{lab} (month #)", "n0", lambda flag=flag: f"MIN({FULL(flag)})", lambda flag=flag: _first(flag))
    SR(base, lab, "text", _month_text(base + "_num"), lambda base=base: _lab(SV[base + "_num"]))
SR("k_min_cash", "Minimum closing cash (all months, incl. pre-seed)", "zar", lambda: f"MIN({FULL('close_cash')})", lambda: min(F.V["close_cash"][1:]))
SR("k_min_cash_num", "Month # of minimum cash", "n0", lambda: f"MATCH({K('k_min_cash')},{FULL('close_cash')},0)",
   lambda: F.V["close_cash"][1:].index(SV["k_min_cash"]) + 1)
SR("k_min_cash_month", "Month of minimum cash", "text", lambda: f"INDEX({LABELS},{K('k_min_cash_num')})", lambda: F.mlabel(int(SV["k_min_cash_num"])))
SR("k_min_post", "Minimum closing cash from the seed month on", "zar", lambda: f"MIN({FULL('h_cash_post')})", lambda: min(F.V["h_cash_post"][1:]))
SR("k_min_post_num", "Month # of minimum post-seed cash", "n0", lambda: f"MATCH({K('k_min_post')},{FULL('h_cash_post')},0)",
   lambda: F.V["h_cash_post"][1:].index(SV["k_min_post"]) + 1)
SR("k_min_post_month", "Month of minimum post-seed cash (cash trough)", "text", lambda: f"INDEX({LABELS},{K('k_min_post_num')})",
   lambda: F.mlabel(int(SV["k_min_post_num"])))
SR("k_pre_min", "Minimum closing cash before the seed lands", "zar", lambda: f"MIN({FULL('h_cash_pre')})", lambda: min(F.V["h_cash_pre"][1:]))
SR("k_pre_min_num", "Month # of minimum pre-seed cash", "n0", lambda: f"MATCH({K('k_pre_min')},{FULL('h_cash_pre')},0)",
   lambda: F.V["h_cash_pre"][1:].index(SV["k_pre_min"]) + 1)
SR("k_pre_min_month", "Month of minimum pre-seed cash", "text", lambda: f"INDEX({LABELS},{K('k_pre_min_num')})", lambda: F.mlabel(int(SV["k_pre_min_num"])))
SR("k_bridge", "PRE-SEED BRIDGE REQUIRED (shortfall below zero before the seed lands)", "zar", lambda: f"MAX(0,-{K('k_pre_min')})",
   lambda: max(0.0, -SV["k_pre_min"]))
SR("k_buffer", "Minimum-cash buffer", "zar", lambda: AD("min_cash_buffer"), lambda: F.P["min_cash_buffer"])
SR("k_headroom", "Headroom: minimum post-seed cash minus buffer", "zar", lambda: f"{K('k_min_post')}-{K('k_buffer')}",
   lambda: SV["k_min_post"] - SV["k_buffer"])
SR("k_buf_short", "Shortfall vs buffer (extra cash needed to hold the buffer)", "zar", lambda: f"MAX(0,-{K('k_headroom')})",
   lambda: max(0.0, -SV["k_headroom"]))
SR("k_buf_first_num", "First post-seed month below the buffer (month #; 999 = never)", "n0", lambda: f"MIN({FULL('flag_buf')})", lambda: _first("flag_buf"))
SR("k_buf_first", "First post-seed month below the buffer", "text", lambda: f"IF({K('k_buf_first_num')}=999,\"Never\",INDEX({LABELS},{K('k_buf_first_num')}))",
   lambda: "Never" if SV["k_buf_first_num"] == 999 else F.mlabel(int(SV["k_buf_first_num"])))
SR("k_profitable", "PROFITABLE ON THE SEED ALONE? (no Series A, cash >= buffer, sustained EBITDA and cash-flow break-even)", "text",
   lambda: (f"IF(AND(OR({AD('seriesA_on')}=0,{AD('seriesA_amount')}=0),{K('k_min_post')}>={K('k_buffer')},"
            f"{K('k_be_sus_num')}<999,{K('k_cfpos_sus_num')}<999),\"Yes\",\"No\")"),
   lambda: "Yes" if ((F.P["seriesA_on"] == 0 or F.P["seriesA_amount"] == 0) and SV["k_min_post"] >= SV["k_buffer"]
                     and SV["k_be_sus_num"] < 999 and SV["k_cfpos_sus_num"] < 999) else "No")
SR("k_first_neg_num", "First post-seed month closing cash < 0 (month #; 999 = never)", "n0", lambda: f"MIN({FULL('flag_neg')})", lambda: _first("flag_neg"))
SR("k_runway_out", "Months from seed until cash runs out", "n0",
   lambda: f"IF({K('k_first_neg_num')}=999,\"Not exhausted within 60 months\",{K('k_first_neg_num')}-{AD('seed_month')})",
   lambda: "Not exhausted within 60 months" if SV["k_first_neg_num"] == 999 else SV["k_first_neg_num"] - F.P["seed_month"])
SR("k_cash_seed", "Closing cash in seed month", "zar", lambda: f"SUM({FULL('h_cash_seed')})", lambda: sum(F.V["h_cash_seed"][1:]))
SR("k_burn", "Average monthly net burn, 12 months after seed", "zar", lambda: f"-SUM({FULL('h_burn')})/12", lambda: -sum(F.V["h_burn"][1:]) / 12)
SR("k_runway_seed", "Runway at seed close (cash / avg burn of next 12 months)", "n1",
   lambda: f"IF({K('k_burn')}<=0,\"Cash generative\",{K('k_cash_seed')}/{K('k_burn')})",
   lambda: "Cash generative" if SV["k_burn"] <= 0 else SV["k_cash_seed"] / SV["k_burn"])
SR("k_trough_months", "Months from seed to cash trough", "n0", lambda: f"{K('k_min_post_num')}-{AD('seed_month')}",
   lambda: SV["k_min_post_num"] - F.P["seed_month"])
SR("k_funding_gap", "Additional funding needed to keep post-seed cash >= 0", "zar", lambda: f"MAX(0,-{K('k_min_post')})",
   lambda: max(0.0, -SV["k_min_post"]))
for r in NONZA:
    SR(f"k_launch_num_{r}", f"Effective launch month #: {MARKET_SHORT[r]} (999 = not launched)", "n0",
       lambda r=r: f"IF(SUM({FULL('launched_' + r)})=0,999,61-SUM({FULL('launched_' + r)}))",
       lambda r=r: 999 if sum(F.V["launched_" + r][1:]) == 0 else 61 - sum(F.V["launched_" + r][1:]))
    SR(f"k_launch_{r}", f"Effective launch month: {MARKET_SHORT[r]}", "text",
       lambda r=r: f"IF({K('k_launch_num_' + r)}=999,\"Not launched\",INDEX({LABELS},{K('k_launch_num_' + r)}))",
       lambda r=r: "Not launched" if SV[f"k_launch_num_{r}"] == 999 else F.mlabel(int(SV[f"k_launch_num_{r}"])))


def run_annual():
    AV.clear()
    SV.clear()
    for rw in AROWS:
        if rw["kind"] == "row":
            for y in YEARS:
                AV[rw["key"]][y] = rw["py"](y)
    for s in SROWS:
        SV[s["key"]] = s["py"]()
    return AV, SV
