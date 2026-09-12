"""FluxMuse financial model v2: monthly row definitions.

Each row carries TWO independent implementations:
  xl(m) -> Excel formula text for month m (written to the workbook)
  py(m) -> Python value for month m (the mirror used for JSON / charts / sensitivity)
The build script evaluates the written formulas with a small Excel evaluator and
asserts that every cell equals the Python mirror.

Compute order matters for the mirror: a row may use same-month values only of rows
defined above it; gates and caps use the previous month's net MRR, so there is no
circularity even though hiring drives acquisition and acquisition drives hiring.
"""
from collections import defaultdict

from openpyxl.utils import get_column_letter

from fm_inputs import (AD, DEPTS, FX_MKTS, MARKET_SHORT, MARKET_STOCKS, MARKETS, NONZA, ROLES, SEG_SHORT,
                       SEGMENTS, ST, STOCKS, TIER_NAME, TIERS, WAVE1, WINDOW_MKTS)

M = 60
MONTHS = range(1, M + 1)
FIRST_ROW = 7
MON = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def fy_of(m):
    return (m - 1) // 12 + 1


def mlabel(m):
    k = 9 + (m - 1)
    return f"{MON[k % 12]} {2026 + k // 12}"


def col(m):
    return get_column_letter(2 + m)


CUR = [None]
ROWPOS = {}
ROWS = []
V = defaultdict(lambda: [0.0] * (M + 1))
P = {}


def sref(sheet):
    return f"'{sheet}'" if any(ch in sheet for ch in " &-") else sheet


def X(key, m):
    sh, r = ROWPOS[key]
    return f"{col(m)}{r}" if sh == CUR[0] else f"{sref(sh)}!{col(m)}{r}"


def XL(key, m, lag=1):
    """Reference to a lagged month; literal 0 before month 1."""
    return "0" if m - lag < 1 else X(key, m - lag)


def XR(key, m1, m2):
    sh, r = ROWPOS[key]
    rng = f"{col(m1)}{r}:${col(m2)}${r}" if m2 == M else f"{col(m1)}{r}:{col(m2)}{r}"
    return rng if sh == CUR[0] else f"{sref(sh)}!{rng}"


def MN(m):
    return f"{col(m)}$3"


def FYC(m):
    return f"{col(m)}$5"


def v(key, m):
    return V[key][m] if m >= 1 else 0.0


def SEC(sheet, title):
    ROWS.append(dict(kind="section", sheet=sheet, label=title))


def R(sheet, key, label, unit, fmt, xl, py, bold=False):
    ROWS.append(dict(kind="row", sheet=sheet, key=key, label=label, unit=unit, fmt=fmt, xl=xl, py=py, bold=bold))


def plus(keys, m):
    return "+".join(X(k, m) for k in keys) if keys else "0"


def choose_fy(prefix, m):
    return f"CHOOSE({FYC(m)}," + ",".join(AD(f"{prefix}{y}") for y in range(1, 6)) + ")"


def vf_xl(r, m):
    return f"*{X('vf_' + r, m)}" if r in FX_MKTS else ""


def vf_py(r, m):
    return v("vf_" + r, m) if r in FX_MKTS else 1.0


def pr(r, t):
    return AD(f"price_{r}_{t}")


RB, C, PL, CF = "Revenue_Build", "Costs", "P&L", "Cash_Flow"

# =============================================================================
# REVENUE BUILD (1): timeline, market launches (MRR-gated), FX & repricing
# =============================================================================
SEC(RB, "Timeline: lean pre-seed mode, pilot, previous-month MRR (drives every gate and cap)")
R(RB, "post_seed", "Seed has landed (1) / lean pre-seed mode (0)", "flag", "n0",
  lambda m: f"IF({MN(m)}>={AD('seed_month')},1,0)", lambda m: 1.0 if m >= P["seed_month"] else 0.0)
R(RB, "pilot_on", "Pilot running (12 brands, not paying)", "flag", "n0",
  lambda m: f"IF({MN(m)}<={AD('pilot_end_month')},1,0)", lambda m: 1.0 if m <= P["pilot_end_month"] else 0.0)
R(RB, "mrr_prev", "Net subscription MRR, previous month", "R", "zar",
  lambda m: "0" if m == 1 else X("subrev_net", m - 1), lambda m: v("subrev_net", m - 1))

SEC(RB, "Market launches: decision needs month >= plan + shift - 2, the seed, and MRR >= gate; launch 2 months after decision")
R(RB, "launched_ZA", "Live: South Africa", "flag", "n0",
  lambda m: f"IF({MN(m)}>={AD('launch_ZA')},1,0)", lambda m: 1.0 if m >= P["launch_ZA"] else 0.0)
for r in NONZA:
    def _cond_xl(m, r=r):
        return (f"AND({AD('on_' + r)}=1,{MN(m)}>={AD('launch_plan_' + r)}+{AD('launch_delay')}-2,"
                f"{MN(m)}>={AD('seed_month')},{X('mrr_prev', m)}>={AD('launch_gate_' + r)}*{AD('gate_mult')})")

    def _cond_py(m, r=r):
        return (P["on_" + r] == 1 and m >= P["launch_plan_" + r] + P["launch_delay"] - 2 and m >= P["seed_month"]
                and v("mrr_prev", m) >= P["launch_gate_" + r] * P["gate_mult"])

    R(RB, f"decided_{r}", f"Launch decided (country lead hired): {MARKET_SHORT[r]}", "flag", "n0",
      lambda m, r=r, c=_cond_xl: f"IF({c(m)},1,0)" if m == 1 else f"IF(OR({X('decided_' + r, m - 1)}=1,{c(m)}),1,0)",
      lambda m, r=r, c=_cond_py: 1.0 if (v("decided_" + r, m - 1) == 1 or c(m)) else 0.0)
    R(RB, f"launched_{r}", f"Live: {MARKET_SHORT[r]}", "flag", "n0",
      lambda m, r=r: XL("decided_" + r, m, 2), lambda m, r=r: v("decided_" + r, m - 2))
for r in MARKETS:
    R(RB, f"launch_now_{r}", f"Launch month: {MARKET_SHORT[r]}", "flag", "n0",
      lambda m, r=r: f"{X('launched_' + r, m)}-{XL('launched_' + r, m)}",
      lambda m, r=r: v("launched_" + r, m) - v("launched_" + r, m - 1))
for r in WINDOW_MKTS:
    R(RB, f"win_{r}", f"Founding Member launch window open: {MARKET_SHORT[r]}", "flag", "n0",
      lambda m, r=r: (f"IF({AD('fm_window')}=0,0,IF({AD('fm_window')}=1,{X('launched_' + r, m)}-{XL('launched_' + r, m, 1)},"
                      f"{X('launched_' + r, m)}-{XL('launched_' + r, m, 2)}))"),
      lambda m, r=r: 0.0 if P["fm_window"] == 0 else v("launched_" + r, m) - v("launched_" + r, m - int(P["fm_window"])))

SEC(RB, "FX drift & quarterly repricing (ZAR value of fixed local / USD price points; 1.000 = parity at Sept 2026 rates)")
for r in FX_MKTS:
    R(RB, f"fx_idx_{r}", f"ZAR value of 1 unit of {MARKET_SHORT[r]} currency (index)", "x", "x3",
      lambda m, r=r: f"(1+{AD('dep_' + r)})^(({MN(m)}-1)/12)*IF({MN(m)}>={AD('fx_shock_month')},1/(1+{AD('fx_shock')}),1)",
      lambda m, r=r: (1 + P["dep_" + r]) ** ((m - 1) / 12) * (1 / (1 + P["fx_shock"]) if m >= P["fx_shock_month"] else 1.0))
    R(RB, f"plvl_{r}", f"Local price level after repricing: {MARKET_SHORT[r]}", "x", "x3",
      lambda m, r=r: "1" if m == 1 else (X("plvl_" + r, m - 1) if m <= 3 else
                                        f"IF(AND({AD('reprice_on')}=1,MOD({MN(m)}-1,3)=0,"
                                        f"ABS({X('plvl_' + r, m - 1)}*{X('fx_idx_' + r, m - 3)}-1)>{AD('reprice_thr')}),"
                                        f"1/{X('fx_idx_' + r, m - 3)},{X('plvl_' + r, m - 1)})"),
      lambda m, r=r: 1.0 if m == 1 else (
          1 / v("fx_idx_" + r, m - 3)
          if (m > 3 and P["reprice_on"] == 1 and (m - 1) % 3 == 0
              and abs(v("plvl_" + r, m - 1) * v("fx_idx_" + r, m - 3) - 1) > P["reprice_thr"])
          else v("plvl_" + r, m - 1)))
    R(RB, f"vf_{r}", f"ZAR value factor of local prices: {MARKET_SHORT[r]}", "x", "x3",
      lambda m, r=r: f"{X('plvl_' + r, m)}*{X('fx_idx_' + r, m)}", lambda m, r=r: v("plvl_" + r, m) * v("fx_idx_" + r, m))

# =============================================================================
# COSTS (1): headcount, MRR-gated (computed before acquisition: PMs and country leads drive agencies)
# =============================================================================
SEC(C, "Headcount: FTEs by role. Non-founder roles need month >= earliest hire, the seed, and last month's MRR >= gate x multiplier")


def _fte_xl(i, m):
    ro = ROLES[i]
    cnt = AD(f"hc_count_{i}")
    if ro["type"] == "F":
        return f"IF({MN(m)}>={AD(f'hc_hire_{i}')},{cnt},0)"
    if ro["link"]:
        mk, kind = ro["link"]
        if kind == "lead":
            return f"IF({X('decided_' + mk, m)}=1,{cnt},0)"
        if kind == "launch":
            return f"IF({X('launched_' + mk, m)}=1,{cnt},0)"
        return "0" if m <= 12 else f"IF({X('launched_' + mk, m - 12)}=1,{cnt},0)"
    cond = (f"AND({MN(m)}>={AD(f'hc_hire_{i}')},{MN(m)}>={AD('seed_month')},"
            f"{X('mrr_prev', m)}>={AD(f'hc_gate_{i}')}*{AD('gate_mult')})")
    return f"IF({cond},{cnt},0)" if m == 1 else f"IF(OR({X(f'fte_{i}', m - 1)}>0,{cond}),{cnt},0)"


def _fte_py(i, m):
    ro = ROLES[i]
    cnt = P[f"hc_count_{i}"]
    if ro["type"] == "F":
        return cnt if m >= P[f"hc_hire_{i}"] else 0.0
    if ro["link"]:
        mk, kind = ro["link"]
        if kind == "lead":
            return cnt if v("decided_" + mk, m) == 1 else 0.0
        if kind == "launch":
            return cnt if v("launched_" + mk, m) == 1 else 0.0
        return cnt if (m > 12 and v("launched_" + mk, m - 12) == 1) else 0.0
    cond = m >= P[f"hc_hire_{i}"] and m >= P["seed_month"] and v("mrr_prev", m) >= P[f"hc_gate_{i}"] * P["gate_mult"]
    return cnt if (v(f"fte_{i}", m - 1) > 0 or cond) else 0.0


for i, ro in enumerate(ROLES):
    R(C, f"fte_{i}", ro["name"], "FTE", "n1", lambda m, i=i: _fte_xl(i, m), lambda m, i=i: _fte_py(i, m))
SEC(C, "FTEs by department")
for d in DEPTS:
    idx = [i for i, ro in enumerate(ROLES) if ro["dept"] == d]
    R(C, f"fte_dept_{d}", d, "FTE", "n1", lambda m, idx=idx: plus([f"fte_{i}" for i in idx], m),
      lambda m, idx=idx: sum(v(f"fte_{i}", m) for i in idx))
R(C, "fte_total", "Total headcount", "FTE", "n1", lambda m: plus([f"fte_dept_{d}" for d in DEPTS], m),
  lambda m: sum(v(f"fte_dept_{d}", m) for d in DEPTS), bold=True)
R(C, "new_hires", "New hires in month", "FTE", "n1",
  lambda m: f"MAX(0,{X('fte_total', m)})" if m == 1 else f"MAX(0,{X('fte_total', m)}-{X('fte_total', m - 1)})",
  lambda m: max(0.0, v("fte_total", m) - v("fte_total", m - 1)))
PM_IDX = [i for i, ro in enumerate(ROLES) if ro["type"] == "PM"]
R(C, "pm_active", "Partnerships managers active (SA agency programme)", "FTE", "n1",
  lambda m: plus([f"fte_{i}" for i in PM_IDX], m), lambda m: sum(v(f"fte_{i}", m) for i in PM_IDX))
LEAD_IDX = {r: [i for i, ro in enumerate(ROLES) if ro["link"] == (r, "lead")] for r in WAVE1}
for r in WAVE1:
    R(C, f"lead_{r}", f"Country lead active: {MARKET_SHORT[r]}", "FTE", "n1",
      lambda m, r=r: plus([f"fte_{i}" for i in LEAD_IDX[r]], m), lambda m, r=r: sum(v(f"fte_{i}", m) for i in LEAD_IDX[r]))
SEC(C, "Payroll cost by role (cost-to-company incl. on-costs, escalated annually)")
R(C, "sal_esc_f", "Salary escalation factor", "x", "x3", lambda m: f"(1+{AD('sal_esc')})^({FYC(m)}-1)",
  lambda m: (1 + P["sal_esc"]) ** (fy_of(m) - 1))
for i, ro in enumerate(ROLES):
    R(C, f"cost_{i}", ro["name"], "R", "zar",
      lambda m, i=i: f"{X(f'fte_{i}', m)}*{AD(f'hc_ctc_{i}')}*{X('sal_esc_f', m)}*(1+{AD('oncost')})",
      lambda m, i=i: v(f"fte_{i}", m) * P[f"hc_ctc_{i}"] * v("sal_esc_f", m) * (1 + P["oncost"]))
SEC(C, "Payroll by department")
for d in DEPTS:
    idx = [i for i, ro in enumerate(ROLES) if ro["dept"] == d]
    R(C, f"cost_dept_{d}", d, "R", "zar", lambda m, idx=idx: plus([f"cost_{i}" for i in idx], m),
      lambda m, idx=idx: sum(v(f"cost_{i}", m) for i in idx))
R(C, "cost_total", "Total payroll", "R", "zar", lambda m: plus([f"cost_dept_{d}" for d in DEPTS], m),
  lambda m: sum(v(f"cost_dept_{d}", m) for d in DEPTS), bold=True)
R(C, "pm_team_cost", "of which partnerships managers", "R", "zar", lambda m: plus([f"cost_{i}" for i in PM_IDX], m),
  lambda m: sum(v(f"cost_{i}", m) for i in PM_IDX))

# =============================================================================
# REVENUE BUILD (2): acquisition by market & segment, with the paid-marketing cap
# =============================================================================
SEC(RB, "Self-serve trials by market (start in each market's launch month)")
R(RB, "g_m", "Monthly trial growth rate (scenario, by fiscal year)", "% m/m", "pct", lambda m: choose_fy("g_fy", m),
  lambda m: P[f"g_fy{fy_of(m)}"])
for r in MARKETS:
    R(RB, f"trials_{r}", f"Self-serve trials: {MARKET_SHORT[r]}", "trials", "n0",
      lambda m, r=r: (f"IF({X('launched_' + r, m)}=0,0,{AD('trials_launch_' + r)}*{AD('vol_mult')})" if m == 1 else
                      f"IF({X('launched_' + r, m)}=0,0,IF({X('launched_' + r, m - 1)}=0,{AD('trials_launch_' + r)}*{AD('vol_mult')},"
                      f"{X('trials_' + r, m - 1)}*(1+{X('g_m', m)})))"),
      lambda m, r=r: 0.0 if v("launched_" + r, m) == 0 else (
          P["trials_launch_" + r] * P["vol_mult"] if v("launched_" + r, m - 1) == 0 else v("trials_" + r, m - 1) * (1 + v("g_m", m))))
R(RB, "trials_total", "Total self-serve trials", "trials", "n0", lambda m: plus([f"trials_{r}" for r in MARKETS], m),
  lambda m: sum(v(f"trials_{r}", m) for r in MARKETS), bold=True)


def _upl_xl(r, m):
    return f"*(1+{AD('fm_uplift_eff')}*{X('win_' + r, m)})" if r in WINDOW_MKTS else ""


def _upl_py(r, m):
    return (1 + P["fm_uplift_eff"] * v("win_" + r, m)) if r in WINDOW_MKTS else 1.0


SEC(RB, "Sign-ups wanted before the marketing cap (trials x segment share x conversion x launch-window uplift)")
for r in MARKETS:
    R(RB, f"des_SO_{r}", f"Solo sign-ups wanted: {MARKET_SHORT[r]}", "workspaces", "n1",
      lambda m, r=r: f"{X('trials_' + r, m)}*{AD('solo_share')}*{AD('conv_SO')}*{AD('conv_mult')}" + _upl_xl(r, m),
      lambda m, r=r: v("trials_" + r, m) * P["solo_share"] * P["conv_SO"] * P["conv_mult"] * _upl_py(r, m))
    R(RB, f"des_SM_{r}", f"SME sign-ups wanted: {MARKET_SHORT[r]}", "workspaces", "n1",
      lambda m, r=r: f"{X('trials_' + r, m)}*(1-{AD('solo_share')})*{AD('conv_SM')}*{AD('conv_mult')}" + _upl_xl(r, m),
      lambda m, r=r: v("trials_" + r, m) * (1 - P["solo_share"]) * P["conv_SM"] * P["conv_mult"] * _upl_py(r, m))

SEC(RB, "COST DISCIPLINE: paid acquisition budget = MIN(desired, floor + cap % x last month's MRR); zero before the seed")
R(RB, "paid_share", "Share of sign-ups needing paid acquisition", "%", "pct", lambda m: choose_fy("paid_share_fy", m),
  lambda m: P[f"paid_share_fy{fy_of(m)}"])
R(RB, "cac_infl_f", "CAC inflation factor", "x", "x3", lambda m: f"(1+{AD('cac_infl')})^({FYC(m)}-1)",
  lambda m: (1 + P["cac_infl"]) ** (fy_of(m) - 1))
R(RB, "price_esc_f0", "Price escalator factor (list prices +escalator each October)", "x", "x3", lambda m: f"(1+{AD('price_esc')})^({FYC(m)}-1)",
  lambda m: (1 + P["price_esc"]) ** (fy_of(m) - 1))


def _cidx_xl(r):
    return "" if r == "ZA" else f"*{AD('cac_idx_' + r)}"


def _cidx_py(r):
    return 1.0 if r == "ZA" else P["cac_idx_" + r]


ARPA_MIX = {"SO": ("so_mix_G", "S", "G"), "SM": ("sm_mix_Sc", "G", "Sc")}


def _arpa_xl(sg, r):
    k, t1, t2 = ARPA_MIX[sg]
    return f"((1-{AD(k)})*{pr(r, t1)}+{AD(k)}*{pr(r, t2)})"


def _arpa_py(sg, r):
    k, t1, t2 = ARPA_MIX[sg]
    return (1 - P[k]) * P[f"price_{r}_{t1}"] + P[k] * P[f"price_{r}_{t2}"]


SEC(RB, "COST DISCIPLINE: CAC payback test by segment & market (paid acquisition off where payback > maximum)")
for sg in ("SO", "SM"):
    for r in MARKETS:
        R(RB, f"pb_{sg}_{r}", f"CAC payback, {SEG_SHORT[sg]}: {MARKET_SHORT[r]}", "months", "n1",
          lambda m, sg=sg, r=r: (f"{AD('cac_mult')}*{X('cac_infl_f', m)}*{AD('cac_' + sg)}{_cidx_xl(r)}/"
                                 f"({X('price_esc_f0', m)}*{AD('annual_factor')}{vf_xl(r, m)}*{AD('pb_gm')}*{_arpa_xl(sg, r)})"),
          lambda m, sg=sg, r=r: P["cac_mult"] * v("cac_infl_f", m) * P["cac_" + sg] * _cidx_py(r)
          / (v("price_esc_f0", m) * P["annual_factor"] * vf_py(r, m) * P["pb_gm"] * _arpa_py(sg, r)))
        R(RB, f"pbok_{sg}_{r}", f"Paid acquisition allowed (payback <= max), {SEG_SHORT[sg]}: {MARKET_SHORT[r]}", "flag", "n0",
          lambda m, sg=sg, r=r: f"IF({X(f'pb_{sg}_{r}', m)}<={AD('pb_max')},1,0)",
          lambda m, sg=sg, r=r: 1.0 if v(f"pb_{sg}_{r}", m) <= P["pb_max"] else 0.0)
for sg in ("SO", "SM"):
    R(RB, f"paid_des_{sg}", f"Desired paid acquisition spend: {SEG_SHORT[sg]}", "R", "zar",
      lambda m, sg=sg: (f"{X('paid_share', m)}*{AD('cac_mult')}*{X('cac_infl_f', m)}*{AD('cac_' + sg)}*("
                        + "+".join(f"{X(f'des_{sg}_{r}', m)}{_cidx_xl(r)}*{X(f'pbok_{sg}_{r}', m)}" for r in MARKETS) + ")"),
      lambda m, sg=sg: v("paid_share", m) * P["cac_mult"] * v("cac_infl_f", m) * P["cac_" + sg]
      * sum(v(f"des_{sg}_{r}", m) * _cidx_py(r) * v(f"pbok_{sg}_{r}", m) for r in MARKETS))
R(RB, "paid_des", "Desired paid acquisition spend: total", "R", "zar", lambda m: plus(["paid_des_SO", "paid_des_SM"], m),
  lambda m: v("paid_des_SO", m) + v("paid_des_SM", m))
R(RB, "paid_cap", "Paid acquisition cap (floor + cap % x last month's net MRR; 0 before seed)", "R", "zar",
  lambda m: f"{X('post_seed', m)}*({AD('paid_floor')}+{AD('cap_pct')}*{X('mrr_prev', m)})",
  lambda m: v("post_seed", m) * (P["paid_floor"] + P["cap_pct"] * v("mrr_prev", m)))
R(RB, "paid_k", "Share of desired paid acquisition funded", "%", "pct",
  lambda m: f"IF({X('paid_des', m)}=0,{X('post_seed', m)},MIN(1,{X('paid_cap', m)}/{X('paid_des', m)}))",
  lambda m: v("post_seed", m) if v("paid_des", m) == 0 else min(1.0, v("paid_cap", m) / v("paid_des", m)))
for sg in ("SO", "SM"):
    R(RB, f"paid_spend_{sg}", f"Paid acquisition spend: {SEG_SHORT[sg]}", "R", "zar",
      lambda m, sg=sg: f"{X('paid_des_' + sg, m)}*{X('paid_k', m)}", lambda m, sg=sg: v("paid_des_" + sg, m) * v("paid_k", m))
R(RB, "paid_spend", "Paid acquisition spend: total", "R", "zar", lambda m: plus(["paid_spend_SO", "paid_spend_SM"], m),
  lambda m: v("paid_spend_SO", m) + v("paid_spend_SM", m), bold=True)

SEC(RB, "New paying customers by market & segment")
for r in MARKETS:
    for sg in ("SO", "SM"):
        R(RB, f"new_{sg}_{r}", f"New {SEG_SHORT[sg]}: {MARKET_SHORT[r]}", "workspaces", "n1",
          lambda m, r=r, sg=sg: f"{X(f'des_{sg}_{r}', m)}*(1-{X('paid_share', m)}+{X('paid_share', m)}*{X('paid_k', m)}*{X(f'pbok_{sg}_{r}', m)})",
          lambda m, r=r, sg=sg: v(f"des_{sg}_{r}", m) * (1 - v("paid_share", m) + v("paid_share", m) * v("paid_k", m) * v(f"pbok_{sg}_{r}", m)))
R(RB, "pilot_new", "Pilot brands converting (Pilot Founding terms)", "workspaces", "n1",
  lambda m: f"IF({MN(m)}={AD('pilot_convert_month')},{AD('pilot_brands')}*{AD('pilot_conv')},0)",
  lambda m: P["pilot_brands"] * P["pilot_conv"] if m == P["pilot_convert_month"] else 0.0)
R(RB, "new_AG_ZA", "New agencies: South Africa (inbound + partnerships managers)", "agencies", "n2",
  lambda m: f"{X('launched_ZA', m)}*{AD('agency_inbound_ZA')}+{X('pm_active', m)}*{AD('agencies_per_pm')}",
  lambda m: v("launched_ZA", m) * P["agency_inbound_ZA"] + v("pm_active", m) * P["agencies_per_pm"])
for r in WAVE1:
    R(RB, f"new_AG_{r}", f"New agencies: {MARKET_SHORT[r]} (inbound + country lead)", "agencies", "n2",
      lambda m, r=r: f"{X('launched_' + r, m)}*{AD('agency_inbound_' + r)}+{X('lead_' + r, m)}*{AD('agencies_per_lead')}",
      lambda m, r=r: v("launched_" + r, m) * P["agency_inbound_" + r] + v("lead_" + r, m) * P["agencies_per_lead"])
R(RB, "ent_new", "New inbound enterprise deals (SA)", "deals", "n2",
  lambda m: f"{X('launched_ZA', m)}*{choose_fy('ent_fy', m)}/12*{AD('ent_mult')}",
  lambda m: v("launched_ZA", m) * P[f"ent_fy{fy_of(m)}"] / 12 * P["ent_mult"])

# =============================================================================
# REVENUE BUILD (3): cohort stocks by market, segment & tier
# =============================================================================
SEC(RB, "Customer cohorts by market, segment & tier: opening, new (incl. upgrades in), churned, upgraded out, closing")
UPG = {"SO_S": ("upg_SO", "SO_G"), "SM_G": ("upg_SM", "SM_Sc")}


def _new_xl(sk, r, st, m):
    if st == "SO_S":
        s = f"{X('new_SO_' + r, m)}*(1-{AD('so_mix_G')})" + (f"+{X('pilot_new', m)}*{AD('pilot_mix_SO')}" if r == "ZA" else "")
    elif st == "SO_G":
        s = f"{X('new_SO_' + r, m)}*{AD('so_mix_G')}+{X(f'upg_{r}_SO_S', m)}"
    elif st == "SM_G":
        s = f"{X('new_SM_' + r, m)}*(1-{AD('sm_mix_Sc')})" + (f"+{X('pilot_new', m)}*{AD('pilot_mix_SM')}" if r == "ZA" else "")
    elif st == "SM_Sc":
        s = f"{X('new_SM_' + r, m)}*{AD('sm_mix_Sc')}+{X(f'upg_{r}_SM_G', m)}"
    elif st == "AG_A":
        s = X("new_AG_" + r, m) + (f"+{X('pilot_new', m)}*{AD('pilot_mix_AG')}" if r == "ZA" else "")
    else:
        s = X("ent_new", m)
    return s


def _new_py(sk, r, st, m):
    za = r == "ZA"
    if st == "SO_S":
        return v("new_SO_" + r, m) * (1 - P["so_mix_G"]) + (v("pilot_new", m) * P["pilot_mix_SO"] if za else 0.0)
    if st == "SO_G":
        return v("new_SO_" + r, m) * P["so_mix_G"] + v(f"upg_{r}_SO_S", m)
    if st == "SM_G":
        return v("new_SM_" + r, m) * (1 - P["sm_mix_Sc"]) + (v("pilot_new", m) * P["pilot_mix_SM"] if za else 0.0)
    if st == "SM_Sc":
        return v("new_SM_" + r, m) * P["sm_mix_Sc"] + v(f"upg_{r}_SM_G", m)
    if st == "AG_A":
        return v("new_AG_" + r, m) + (v("pilot_new", m) * P["pilot_mix_AG"] if za else 0.0)
    return v("ent_new", m)


for sk, r, st in STOCKS:
    nm = f"{MARKET_SHORT[r]}: {ST[st][3]}"
    R(RB, f"open_{sk}", f"{nm}: opening", "workspaces", "n1",
      lambda m, sk=sk: "0" if m == 1 else X(f"close_{sk}", m - 1), lambda m, sk=sk: v(f"close_{sk}", m - 1))
    R(RB, f"newc_{sk}", f"{nm}: new", "workspaces", "n1",
      lambda m, sk=sk, r=r, st=st: _new_xl(sk, r, st, m), lambda m, sk=sk, r=r, st=st: _new_py(sk, r, st, m))
    R(RB, f"churn_{sk}", f"{nm}: churned", "workspaces", "n1",
      lambda m, sk=sk, r=r, st=st: (f"{X(f'open_{sk}', m)}*{AD('churn_' + st)}*{AD('churn_mult')}*{AD('churn_sens')}"
                                    + ("" if r == "ZA" else f"*{AD('churn_idx_' + r)}")),
      lambda m, sk=sk, r=r, st=st: v(f"open_{sk}", m) * P["churn_" + st] * P["churn_mult"] * P["churn_sens"]
      * (1.0 if r == "ZA" else P["churn_idx_" + r]))
    if st in UPG:
        R(RB, f"upg_{sk}", f"{nm}: upgraded out", "workspaces", "n1",
          lambda m, sk=sk, st=st: f"{X(f'open_{sk}', m)}*{AD(UPG[st][0])}", lambda m, sk=sk, st=st: v(f"open_{sk}", m) * P[UPG[st][0]])
    R(RB, f"close_{sk}", f"{nm}: closing", "workspaces", "n1",
      lambda m, sk=sk, st=st: f"{X(f'open_{sk}', m)}+{X(f'newc_{sk}', m)}-{X(f'churn_{sk}', m)}" + (f"-{X(f'upg_{sk}', m)}" if st in UPG else ""),
      lambda m, sk=sk, st=st: v(f"open_{sk}", m) + v(f"newc_{sk}", m) - v(f"churn_{sk}", m) - (v(f"upg_{sk}", m) if st in UPG else 0.0),
      bold=True)

SEC(RB, "Paying workspaces: by market, segment and tier")
MKT_STK = {r: [sk for sk, rr, st in STOCKS if rr == r] for r in MARKETS}
SEG_STK = {sg: [sk for sk, rr, st in STOCKS if ST[st][0] == sg] for sg in SEGMENTS}
TIER_STK = {t: [sk for sk, rr, st in STOCKS if ST[st][1] == t] for t in TIERS}
UPG_STK = {sg: [sk for sk, rr, st in STOCKS if st in UPG and ST[st][0] == sg] for sg in SEGMENTS}
for r in MARKETS:
    R(RB, f"cust_{r}", f"Paying workspaces: {MARKET_SHORT[r]}", "workspaces", "n0",
      lambda m, r=r: plus([f"close_{s}" for s in MKT_STK[r]], m), lambda m, r=r: sum(v(f"close_{s}", m) for s in MKT_STK[r]), bold=True)
for sg in SEGMENTS:
    for part, lab in [("open", "opening"), ("close", "closing"), ("churn", "churned")]:
        R(RB, f"seg_{part}_{sg}", f"{SEG_SHORT[sg]}: {lab}", "workspaces", "n1",
          lambda m, sg=sg, part=part: plus([f"{part}_{s}" for s in SEG_STK[sg]], m),
          lambda m, sg=sg, part=part: sum(v(f"{part}_{s}", m) for s in SEG_STK[sg]), bold=(part == "close"))
    R(RB, f"seg_new_{sg}", f"{SEG_SHORT[sg]}: new customers acquired (excl. upgrades)", "workspaces", "n1",
      lambda m, sg=sg: plus([f"newc_{s}" for s in SEG_STK[sg]], m) + "".join(f"-{X(f'upg_{s}', m)}" for s in UPG_STK[sg]),
      lambda m, sg=sg: sum(v(f"newc_{s}", m) for s in SEG_STK[sg]) - sum(v(f"upg_{s}", m) for s in UPG_STK[sg]))
for t in TIERS:
    for part, lab in [("open", "opening"), ("close", "closing"), ("churn", "churned")]:
        R(RB, f"tier_{part}_{t}", f"{TIER_NAME[t]} tier: {lab}", "workspaces", "n1",
          lambda m, t=t, part=part: plus([f"{part}_{s}" for s in TIER_STK[t]], m),
          lambda m, t=t, part=part: sum(v(f"{part}_{s}", m) for s in TIER_STK[t]))
for part, lab in [("open", "opening"), ("close", "closing"), ("churn", "churned")]:
    R(RB, f"tot_{part}", f"Total paying workspaces: {lab}", "workspaces", "n0",
      lambda m, part=part: plus([f"seg_{part}_{sg}" for sg in SEGMENTS], m),
      lambda m, part=part: sum(v(f"seg_{part}_{sg}", m) for sg in SEGMENTS), bold=True)
R(RB, "tot_newc", "Total new paying workspaces (excl. upgrades)", "workspaces", "n0",
  lambda m: plus([f"seg_new_{sg}" for sg in SEGMENTS], m), lambda m: sum(v(f"seg_new_{sg}", m) for sg in SEGMENTS), bold=True)
R(RB, "cust_check", "Check: markets minus total (should be 0)", "workspaces", "n2",
  lambda m: f"ROUND({plus([f'cust_{r}' for r in MARKETS], m)}-{X('tot_close', m)},6)",
  lambda m: round(sum(v(f"cust_{r}", m) for r in MARKETS) - v("tot_close", m), 6))

# =============================================================================
# REVENUE BUILD (4): subscription revenue, launch discounts, usage revenue
# =============================================================================
SEC(RB, "Gross subscription revenue (parity price x escalator x annual-billing factor x FX value factor; agencies at partner wholesale)")
R(RB, "price_esc_f", "Price escalator factor", "x", "x3", lambda m: X("price_esc_f0", m), lambda m: v("price_esc_f0", m))


def pr_ag_xl(r):
    return f"({AD('partner_share')}*{pr(r, 'W')}+(1-{AD('partner_share')})*{pr(r, 'A')})"


def pr_ag_py(r):
    return P["partner_share"] * P[f"price_{r}_W"] + (1 - P["partner_share"]) * P[f"price_{r}_A"]


for sk, r, st in STOCKS:
    seg, t, whs, lab = ST[st]
    R(RB, f"rev_{sk}", f"Gross subscription revenue: {MARKET_SHORT[r]}: {lab}", "R", "zar",
      lambda m, sk=sk, r=r, t=t, whs=whs: (f"{X(f'close_{sk}', m)}*{pr_ag_xl(r) if whs else pr(r, t)}*{X('price_esc_f', m)}*{AD('annual_factor')}{vf_xl(r, m)}"),
      lambda m, sk=sk, r=r, t=t, whs=whs: v(f"close_{sk}", m) * (pr_ag_py(r) if whs else P[f"price_{r}_{t}"]) * v("price_esc_f", m) * P["annual_factor"]
      * vf_py(r, m))
for r in MARKETS:
    R(RB, f"subgross_{r}", f"Gross subscription revenue: {MARKET_SHORT[r]}", "R", "zar",
      lambda m, r=r: plus([f"rev_{s}" for s in MKT_STK[r]], m), lambda m, r=r: sum(v(f"rev_{s}", m) for s in MKT_STK[r]))
for sg in SEGMENTS:
    R(RB, f"subgross_seg_{sg}", f"Gross subscription revenue: {SEG_SHORT[sg]}", "R", "zar",
      lambda m, sg=sg: plus([f"rev_{s}" for s in SEG_STK[sg]], m), lambda m, sg=sg: sum(v(f"rev_{s}", m) for s in SEG_STK[sg]))
for t in TIERS:
    R(RB, f"subgross_tier_{t}", f"Gross subscription revenue: {TIER_NAME[t]} tier", "R", "zar",
      lambda m, t=t: plus([f"rev_{s}" for s in TIER_STK[t]], m), lambda m, t=t: sum(v(f"rev_{s}", m) for s in TIER_STK[t]))
R(RB, "subrev_gross", "Gross subscription revenue (before launch discounts)", "R", "zar",
  lambda m: plus([f"subgross_{r}" for r in MARKETS], m), lambda m: sum(v(f"subgross_{r}", m) for r in MARKETS), bold=True)

SEC(RB, "Launch discounts: Founding Member on Solo & SME sign-ups (not Agency; no stacking with partner wholesale). Monthly: % off first bills; annual: fee recognised over 12 + bonus months. Pilot terms")


def _base_xl(r, m):
    return (f"{X('win_' + r, m)}*{X('price_esc_f', m)}{vf_xl(r, m)}*({X('new_SO_' + r, m)}*((1-{AD('so_mix_G')})*{pr(r, 'S')}+{AD('so_mix_G')}*{pr(r, 'G')})"
            f"+{X('new_SM_' + r, m)}*((1-{AD('sm_mix_Sc')})*{pr(r, 'G')}+{AD('sm_mix_Sc')}*{pr(r, 'Sc')}))")


def _base_py(r, m):
    return (v("win_" + r, m) * v("price_esc_f", m) * vf_py(r, m)
            * (v("new_SO_" + r, m) * ((1 - P["so_mix_G"]) * P[f"price_{r}_S"] + P["so_mix_G"] * P[f"price_{r}_G"])
               + v("new_SM_" + r, m) * ((1 - P["sm_mix_Sc"]) * P[f"price_{r}_G"] + P["sm_mix_Sc"] * P[f"price_{r}_Sc"])))


for r in WINDOW_MKTS:
    nm = MARKET_SHORT[r]
    R(RB, f"fm_base_{r}", f"List MRR of new Solo & SME sign-ups inside the launch window: {nm}", "R", "zar",
      lambda m, r=r: _base_xl(r, m), lambda m, r=r: _base_py(r, m))
    R(RB, f"fm_mo_{r}", f"Founding Member discount, monthly plans: {nm}", "R", "zar",
      lambda m, r=r: (f"(1-{AD('annual_share')})*{AD('fm_mo_disc')}*(IF({AD('fm_mo_months')}>=1,{X('fm_base_' + r, m)},0)"
                      f"+IF({AD('fm_mo_months')}>=2,{XL('fm_base_' + r, m)}*(1-{AD('fm_new_churn')}),0))"),
      lambda m, r=r: (1 - P["annual_share"]) * P["fm_mo_disc"] * ((v("fm_base_" + r, m) if P["fm_mo_months"] >= 1 else 0.0)
                                                                  + (v("fm_base_" + r, m - 1) * (1 - P["fm_new_churn"]) if P["fm_mo_months"] >= 2 else 0.0)))
    R(RB, f"fm_ann_{r}", f"Annual-plan Founding Members inside their 12 + bonus month term (list MRR): {nm}", "R", "zar",
      lambda m, r=r: (f"{X('fm_base_' + r, m)}*{AD('annual_share')}" if m == 1 else
                      f"{X('fm_ann_' + r, m - 1)}+({X('fm_base_' + r, m)}-IF({AD('fm_bonus')}=2,{XL('fm_base_' + r, m, 14)},"
                      f"IF({AD('fm_bonus')}=1,{XL('fm_base_' + r, m, 13)},{XL('fm_base_' + r, m, 12)})))*{AD('annual_share')}"),
      lambda m, r=r: v("fm_ann_" + r, m - 1) + (v("fm_base_" + r, m) - v("fm_base_" + r, m - (12 + int(P["fm_bonus"])))) * P["annual_share"])
    R(RB, f"fm_ann_disc_{r}", f"Founding Member discount, annual plans (bonus months): {nm}", "R", "zar",
      lambda m, r=r: f"{X('fm_ann_' + r, m)}*{AD('annual_months')}*(1/12-1/(12+{AD('fm_bonus')}))",
      lambda m, r=r: v("fm_ann_" + r, m) * P["annual_months"] * (1 / 12 - 1 / (12 + P["fm_bonus"])))
    R(RB, f"fm_disc_{r}", f"Founding Member discount: {nm}", "R", "zar",
      lambda m, r=r: f"{X('fm_mo_' + r, m)}+{X('fm_ann_disc_' + r, m)}", lambda m, r=r: v("fm_mo_" + r, m) + v("fm_ann_disc_" + r, m), bold=True)
R(RB, "fm_disc_total", "Founding Member discount: all markets", "R", "zar", lambda m: plus([f"fm_disc_{r}" for r in WINDOW_MKTS], m),
  lambda m: sum(v(f"fm_disc_{r}", m) for r in WINDOW_MKTS), bold=True)
R(RB, "pilot_val", "Converting pilot brands: gross MRR as booked (Agency at partner wholesale blend)", "R", "zar",
  lambda m: (f"{X('pilot_new', m)}*{X('price_esc_f', m)}*({AD('pilot_mix_SO')}*{pr('ZA', 'S')}+{AD('pilot_mix_SM')}*{pr('ZA', 'G')}"
             f"+{AD('pilot_mix_AG')}*{pr_ag_xl('ZA')})"),
  lambda m: v("pilot_new", m) * v("price_esc_f", m) * (P["pilot_mix_SO"] * P["price_ZA_S"] + P["pilot_mix_SM"] * P["price_ZA_G"]
                                                       + P["pilot_mix_AG"] * pr_ag_py("ZA")))
R(RB, "pilot_pay", "Converting pilot brands: pilot price (list x (1 - pilot discount): R249 / R999 / R3,999)", "R", "zar",
  lambda m: (f"{X('pilot_new', m)}*{X('price_esc_f', m)}*(1-{AD('pilot_disc')})*({AD('pilot_mix_SO')}*{pr('ZA', 'S')}+{AD('pilot_mix_SM')}*{pr('ZA', 'G')}"
             f"+{AD('pilot_mix_AG')}*{pr('ZA', 'A')})"),
  lambda m: v("pilot_new", m) * v("price_esc_f", m) * (1 - P["pilot_disc"]) * (P["pilot_mix_SO"] * P["price_ZA_S"] + P["pilot_mix_SM"] * P["price_ZA_G"]
                                                                                + P["pilot_mix_AG"] * P["price_ZA_A"]))
R(RB, "pilot_gap", "Pilot discount per bill (gross booked minus pilot price)", "R", "zar",
  lambda m: f"MAX(0,{X('pilot_val', m)}-{X('pilot_pay', m)})", lambda m: max(0.0, v("pilot_val", m) - v("pilot_pay", m)))
R(RB, "pilot_disc_rev", "Pilot Founding terms discount (50% off first 2 bills)", "R", "zar",
  lambda m: (f"IF({AD('pilot_disc_months')}>=1,{X('pilot_gap', m)},0)"
             f"+IF({AD('pilot_disc_months')}>=2,{XL('pilot_gap', m)}*(1-{AD('fm_new_churn')}),0)"),
  lambda m: ((v("pilot_gap", m) if P["pilot_disc_months"] >= 1 else 0.0)
             + (v("pilot_gap", m - 1) * (1 - P["fm_new_churn"]) if P["pilot_disc_months"] >= 2 else 0.0)), bold=True)
R(RB, "disc_total", "Total launch discounts", "R", "zar", lambda m: plus(["fm_disc_total", "pilot_disc_rev"], m),
  lambda m: v("fm_disc_total", m) + v("pilot_disc_rev", m), bold=True)
R(RB, "subrev_net", "NET SUBSCRIPTION REVENUE (MRR after launch discounts)", "R", "zar",
  lambda m: f"{X('subrev_gross', m)}-{X('disc_total', m)}", lambda m: v("subrev_gross", m) - v("disc_total", m), bold=True)
for r in MARKETS:
    R(RB, f"subnet_{r}", f"Net subscription revenue: {MARKET_SHORT[r]}", "R", "zar",
      lambda m, r=r: X("subgross_" + r, m) + (f"-{X('fm_disc_' + r, m)}" if r in WINDOW_MKTS else "") + (f"-{X('pilot_disc_rev', m)}" if r == "ZA" else ""),
      lambda m, r=r: v("subgross_" + r, m) - (v("fm_disc_" + r, m) if r in WINDOW_MKTS else 0.0) - (v("pilot_disc_rev", m) if r == "ZA" else 0.0))

SEC(RB, "Usage & transaction revenue")
R(RB, "topup_rev", "AI-credit top-ups", "R", "zar",
  lambda m: f"{X('tot_close', m)}*{AD('topup_attach')}*{AD('topup_pack')}*{X('price_esc_f', m)}",
  lambda m: v("tot_close", m) * P["topup_attach"] * P["topup_pack"] * v("price_esc_f", m))
R(RB, "wa_msgs", "Billable WhatsApp messages", "messages", "n0",
  lambda m: "+".join(f"{X(f'tier_close_{t}', m)}*{AD('wa_msgs_' + t)}" for t in TIERS),
  lambda m: sum(v(f"tier_close_{t}", m) * P["wa_msgs_" + t] for t in TIERS))
R(RB, "wa_rev", "WhatsApp messaging (Meta fees resold with markup)", "R", "zar",
  lambda m: f"{X('wa_msgs', m)}*{AD('wa_meta_cost')}*(1+{AD('wa_markup')})", lambda m: v("wa_msgs", m) * P["wa_meta_cost"] * (1 + P["wa_markup"]))
R(RB, "stores", "Commerce-eligible workspaces (Growth, Scale, Enterprise)", "workspaces", "n0",
  lambda m: plus(["tier_close_G", "tier_close_Sc", "tier_close_E"], m),
  lambda m: v("tier_close_G", m) + v("tier_close_Sc", m) + v("tier_close_E", m))
R(RB, "gmv", "WhatsApp checkout GMV", "R", "zar",
  lambda m: f"{X('stores', m)}*{AD('commerce_active')}*{AD('gmv_per_store')}*(1+{AD('gmv_growth')})^({FYC(m)}-1)",
  lambda m: v("stores", m) * P["commerce_active"] * P["gmv_per_store"] * (1 + P["gmv_growth"]) ** (fy_of(m) - 1))
R(RB, "commerce_rev", "Commerce platform fee (NOT IN CURRENT PRICING: 0% Base/Conservative, 0.75% Upside)", "R", "zar",
  lambda m: f"{X('gmv', m)}*{AD('commerce_fee')}", lambda m: v("gmv", m) * P["commerce_fee"])
R(RB, "ent_setup_rev", "Enterprise onboarding / setup fees", "R", "zar", lambda m: f"{X('ent_new', m)}*{AD('ent_setup_fee')}",
  lambda m: v("ent_new", m) * P["ent_setup_fee"])
AG_NEW = ["new_AG_ZA"] + [f"new_AG_{r}" for r in WAVE1]
R(RB, "agency_setup_rev", "Agency white-label setup fees", "R", "zar", lambda m: f"({plus(AG_NEW, m)})*{AD('agency_setup_fee')}",
  lambda m: sum(v(k, m) for k in AG_NEW) * P["agency_setup_fee"])
REV_KEYS = ["subrev_net", "topup_rev", "wa_rev", "commerce_rev", "ent_setup_rev", "agency_setup_rev"]
R(RB, "total_rev", "TOTAL REVENUE (net of launch discounts)", "R", "zar", lambda m: plus(REV_KEYS, m),
  lambda m: sum(v(k, m) for k in REV_KEYS), bold=True)

# =============================================================================
# COSTS (2): COGS & opex
# =============================================================================
SEC(C, "Cost of revenue (COGS)")
R(C, "credits_k", "AI credits consumed ('000)", "'000 credits", "n0",
  lambda m: "(" + "+".join(f"{X(f'tier_close_{t}', m)}*{AD('credits_' + t)}" for t in TIERS)
  + f")*{AD('credits_util')}/1000+{X('tot_close', m)}*{AD('topup_attach')}*{AD('topup_credits')}/1000",
  lambda m: sum(v(f"tier_close_{t}", m) * P["credits_" + t] for t in TIERS) * P["credits_util"] / 1000
  + v("tot_close", m) * P["topup_attach"] * P["topup_credits"] / 1000)
R(C, "ai_rate", "Inference cost per 1,000 credits", "R", "num2", lambda m: f"{AD('ai_cost_1k')}*(1-{AD('ai_cost_decline')})^({FYC(m)}-1)",
  lambda m: P["ai_cost_1k"] * (1 - P["ai_cost_decline"]) ** (fy_of(m) - 1))
R(C, "cogs_ai", "AI inference", "R", "zar", lambda m: f"{X('credits_k', m)}*{X('ai_rate', m)}", lambda m: v("credits_k", m) * v("ai_rate", m))
R(C, "cogs_hosting", "Hosting (lean base before seed, full base after)", "R", "zar",
  lambda m: f"IF({X('post_seed', m)}=1,{AD('hosting_fixed')},{AD('hosting_lean')})+{AD('hosting_per_ws')}*{X('tot_close', m)}",
  lambda m: (P["hosting_fixed"] if v("post_seed", m) == 1 else P["hosting_lean"]) + P["hosting_per_ws"] * v("tot_close", m))
R(C, "cogs_wa", "WhatsApp Meta fees (pass-through cost)", "R", "zar", lambda m: f"{X('wa_msgs', m)}*{AD('wa_meta_cost')}",
  lambda m: v("wa_msgs", m) * P["wa_meta_cost"])
R(C, "nonza_share", "Non-SA share of paying workspaces", "%", "pct",
  lambda m: f"IF({X('tot_close', m)}=0,0,1-{X('cust_ZA', m)}/{X('tot_close', m)})",
  lambda m: 0.0 if v("tot_close", m) == 0 else 1 - v("cust_ZA", m) / v("tot_close", m))
R(C, "proc_rate", "Blended processing rate (card/EFT + mobile money)", "%", "pct2",
  lambda m: f"{AD('card_fee')}+{X('nonza_share', m)}*{AD('mm_extra')}", lambda m: P["card_fee"] + v("nonza_share", m) * P["mm_extra"])
R(C, "cogs_proc", "Payment processing (excl. commerce fee, netted from GMV)", "R", "zar",
  lambda m: f"({X('total_rev', m)}-{X('commerce_rev', m)})*{X('proc_rate', m)}",
  lambda m: (v("total_rev", m) - v("commerce_rev", m)) * v("proc_rate", m))
R(C, "cogs_support", "Variable support cost", "R", "zar", lambda m: f"{X('tot_close', m)}*{AD('support_per_ws')}",
  lambda m: v("tot_close", m) * P["support_per_ws"])
R(C, "cogs_cs_team", "Customer success team (payroll)", "R", "zar", lambda m: X("cost_dept_Customer success", m),
  lambda m: v("cost_dept_Customer success", m))
COGS_KEYS = ["cogs_ai", "cogs_hosting", "cogs_wa", "cogs_proc", "cogs_support", "cogs_cs_team"]
R(C, "cogs_total", "Total COGS", "R", "zar", lambda m: plus(COGS_KEYS, m), lambda m: sum(v(k, m) for k in COGS_KEYS), bold=True)

SEC(C, "Operating expenses: marketing & sales programmes (capped / scaled with MRR; zero before seed except the pilot)")
R(C, "opex_paid", "Paid acquisition (after cap)", "R", "zar", lambda m: X("paid_spend", m), lambda m: v("paid_spend", m))
R(C, "opex_brand", "Brand, content & community = MIN(ceiling, floor + % of MRR)", "R", "zar",
  lambda m: f"{X('post_seed', m)}*MIN({choose_fy('brand_fy', m)},{AD('brand_floor')}+{AD('brand_pct')}*{X('mrr_prev', m)})",
  lambda m: v("post_seed", m) * min(P[f"brand_fy{fy_of(m)}"], P["brand_floor"] + P["brand_pct"] * v("mrr_prev", m)))
R(C, "opex_launch_mkt", "Wave-1 launch marketing (NG/KE/GH, spread over 3 months)", "R", "zar",
  lambda m: "+".join(f"{AD('launch_mkt_' + r)}*({X('launched_' + r, m)}-{XL('launched_' + r, m, 3)})/3" for r in WAVE1),
  lambda m: sum(P["launch_mkt_" + r] * (v("launched_" + r, m) - v("launched_" + r, m - 3)) / 3 for r in WAVE1))
R(C, "opex_rest_mkt", "Rest of Africa & BW/NA self-serve marketing", "R", "zar",
  lambda m: f"{X('launched_RoA', m)}*{AD('roa_budget')}+{X('launched_BWNA', m)}*{AD('bwna_budget')}",
  lambda m: v("launched_RoA", m) * P["roa_budget"] + v("launched_BWNA", m) * P["bwna_budget"])
R(C, "opex_pilot", "Pilot programme", "R", "zar", lambda m: f"{X('pilot_on', m)}*{AD('pilot_cost')}", lambda m: v("pilot_on", m) * P["pilot_cost"])
R(C, "opex_partner", "Partner programme", "R", "zar",
  lambda m: f"{X('post_seed', m)}*(({plus(AG_NEW, m)})*{AD('partner_cost_per_agency')}+IF({MN(m)}>={AD('partner_events_start')},{AD('partner_events')},0))",
  lambda m: v("post_seed", m) * (sum(v(k, m) for k in AG_NEW) * P["partner_cost_per_agency"]
                                 + (P["partner_events"] if m >= P["partner_events_start"] else 0.0)))
R(C, "opex_ent_sales", "Inbound enterprise handling", "R", "zar", lambda m: f"{X('ent_new', m)}*{AD('ent_sales_per_deal')}",
  lambda m: v("ent_new", m) * P["ent_sales_per_deal"])
MKT_KEYS = ["opex_paid", "opex_brand", "opex_launch_mkt", "opex_rest_mkt", "opex_pilot", "opex_partner", "opex_ent_sales"]
R(C, "opex_mkt_prog", "Total marketing & sales programmes", "R", "zar", lambda m: plus(MKT_KEYS, m),
  lambda m: sum(v(k, m) for k in MKT_KEYS), bold=True)

SEC(C, "Operating expenses: G&A, legal & compliance, tools, travel")
R(C, "opex_office", "Office / co-working (from seed)", "R", "zar", lambda m: f"{X('post_seed', m)}*{X('fte_total', m)}*{AD('office_per_fte')}",
  lambda m: v("post_seed", m) * v("fte_total", m) * P["office_per_fte"])
R(C, "opex_ga_fixed", "Fixed G&A (lean overheads before seed)", "R", "zar",
  lambda m: f"IF({X('post_seed', m)}=1,{choose_fy('ga_fy', m)},{AD('lean_overhead')})",
  lambda m: P[f"ga_fy{fy_of(m)}"] if v("post_seed", m) == 1 else P["lean_overhead"])
R(C, "opex_equip", "Equipment for new hires", "R", "zar", lambda m: f"{X('new_hires', m)}*{AD('equip_per_hire')}",
  lambda m: v("new_hires", m) * P["equip_per_hire"])
R(C, "opex_ga", "Total G&A (non-payroll)", "R", "zar", lambda m: plus(["opex_office", "opex_ga_fixed", "opex_equip"], m),
  lambda m: v("opex_office", m) + v("opex_ga_fixed", m) + v("opex_equip", m), bold=True)
R(C, "opex_legal", "Meta, legal & compliance (POPIA base from seed + local compliance per market)", "R", "zar",
  lambda m: f"{X('post_seed', m)}*{AD('legal_fixed')}+" + "+".join(
      f"{X('launch_now_' + r, m)}*{AD('entry_' + r)}+{X('launched_' + r, m)}*{AD('ongoing_' + r)}" for r in NONZA),
  lambda m: v("post_seed", m) * P["legal_fixed"] + sum(v("launch_now_" + r, m) * P["entry_" + r] + v("launched_" + r, m) * P["ongoing_" + r] for r in NONZA))
R(C, "opex_tools", "Software & tools", "R", "zar", lambda m: f"{X('fte_total', m)}*{AD('tools_per_fte')}", lambda m: v("fte_total", m) * P["tools_per_fte"])
R(C, "opex_travel", "Travel", "R", "zar",
  lambda m: f"{X('post_seed', m)}*{X('fte_total', m)}*{AD('travel_per_fte')}+" + "+".join(f"{X('launched_' + r, m)}*{AD('travel_per_region')}" for r in WAVE1),
  lambda m: v("post_seed", m) * v("fte_total", m) * P["travel_per_fte"] + sum(v("launched_" + r, m) for r in WAVE1) * P["travel_per_region"])

# =============================================================================
# P&L
# =============================================================================
SEC(PL, "Revenue: gross subscriptions -> launch discounts -> net")
R(PL, "pl_rev_subs_gross", "Subscriptions (gross, at list / parity prices)", "R", "zar", lambda m: X("subrev_gross", m), lambda m: v("subrev_gross", m))
R(PL, "pl_disc_fm", "less: Founding Member launch discount", "R", "zar", lambda m: f"-{X('fm_disc_total', m)}", lambda m: -v("fm_disc_total", m))
R(PL, "pl_disc_pilot", "less: Pilot Founding terms discount", "R", "zar", lambda m: f"-{X('pilot_disc_rev', m)}", lambda m: -v("pilot_disc_rev", m))
R(PL, "pl_rev_subs", "Subscriptions (net)", "R", "zar", lambda m: plus(["pl_rev_subs_gross", "pl_disc_fm", "pl_disc_pilot"], m),
  lambda m: v("pl_rev_subs_gross", m) + v("pl_disc_fm", m) + v("pl_disc_pilot", m), bold=True)
OTHER_REV = [("pl_rev_topup", "AI-credit top-ups", "topup_rev"), ("pl_rev_wa", "WhatsApp messaging (pass-through + margin)", "wa_rev"),
             ("pl_rev_commerce", "Commerce platform fees (Upside only; not in current pricing)", "commerce_rev"),
             ("pl_rev_ent_setup", "Enterprise setup fees", "ent_setup_rev"), ("pl_rev_agency_setup", "Agency white-label setup fees", "agency_setup_rev")]
for k, lab, src in OTHER_REV:
    R(PL, k, lab, "R", "zar", lambda m, src=src: X(src, m), lambda m, src=src: v(src, m))
R(PL, "pl_rev", "Total revenue", "R", "zar", lambda m: plus(["pl_rev_subs"] + [k for k, _, _ in OTHER_REV], m),
  lambda m: v("pl_rev_subs", m) + sum(v(k, m) for k, _, _ in OTHER_REV), bold=True)
SEC(PL, "Cost of revenue")
COGS_LINES = [("pl_cogs_ai", "AI inference", "cogs_ai"), ("pl_cogs_hosting", "Hosting", "cogs_hosting"),
              ("pl_cogs_wa", "WhatsApp Meta fees", "cogs_wa"), ("pl_cogs_proc", "Payment processing", "cogs_proc"),
              ("pl_cogs_support", "Variable support", "cogs_support"), ("pl_cogs_cs", "Customer success team", "cogs_cs_team")]
for k, lab, src in COGS_LINES:
    R(PL, k, lab, "R", "zar", lambda m, src=src: X(src, m), lambda m, src=src: v(src, m))
R(PL, "pl_cogs", "Total cost of revenue", "R", "zar", lambda m: plus([k for k, _, _ in COGS_LINES], m),
  lambda m: sum(v(k, m) for k, _, _ in COGS_LINES), bold=True)
R(PL, "gp", "Gross profit", "R", "zar", lambda m: f"{X('pl_rev', m)}-{X('pl_cogs', m)}", lambda m: v("pl_rev", m) - v("pl_cogs", m), bold=True)
R(PL, "gm_pct", "Gross margin %", "%", "pct", lambda m: f"IF({X('pl_rev', m)}=0,0,{X('gp', m)}/{X('pl_rev', m)})",
  lambda m: 0.0 if v("pl_rev", m) == 0 else v("gp", m) / v("pl_rev", m))
SEC(PL, "Operating expenses")
OPEX_DEPTS = [d for d in DEPTS if d != "Customer success"]
for d in OPEX_DEPTS:
    R(PL, f"pl_hc_{d}", f"Payroll: {d}", "R", "zar", lambda m, d=d: X(f"cost_dept_{d}", m), lambda m, d=d: v(f"cost_dept_{d}", m))
R(PL, "pl_hc", "Total payroll (excl. customer success in COGS)", "R", "zar", lambda m: plus([f"pl_hc_{d}" for d in OPEX_DEPTS], m),
  lambda m: sum(v(f"pl_hc_{d}", m) for d in OPEX_DEPTS), bold=True)
OPEX_LINES = [("pl_mkt", "Marketing & sales programmes", "opex_mkt_prog"), ("pl_ga", "G&A (non-payroll)", "opex_ga"),
              ("pl_legal", "Meta, legal & compliance", "opex_legal"), ("pl_tools", "Software & tools", "opex_tools"),
              ("pl_travel", "Travel", "opex_travel")]
for k, lab, src in OPEX_LINES:
    R(PL, k, lab, "R", "zar", lambda m, src=src: X(src, m), lambda m, src=src: v(src, m))
R(PL, "pl_opex", "Total operating expenses", "R", "zar", lambda m: plus(["pl_hc"] + [k for k, _, _ in OPEX_LINES], m),
  lambda m: v("pl_hc", m) + sum(v(k, m) for k, _, _ in OPEX_LINES), bold=True)
SEC(PL, "Profit")
R(PL, "ebitda", "EBITDA", "R", "zar", lambda m: f"{X('gp', m)}-{X('pl_opex', m)}", lambda m: v("gp", m) - v("pl_opex", m), bold=True)
R(PL, "ebitda_pct", "EBITDA margin %", "%", "pct", lambda m: f"IF({X('pl_rev', m)}=0,0,{X('ebitda', m)}/{X('pl_rev', m)})",
  lambda m: 0.0 if v("pl_rev", m) == 0 else v("ebitda", m) / v("pl_rev", m))
R(PL, "cum_ebitda", "Cumulative EBITDA (assessed-loss tracker; D&A and interest ignored)", "R", "zar",
  lambda m: X("ebitda", m) if m == 1 else f"{X('cum_ebitda', m - 1)}+{X('ebitda', m)}", lambda m: v("cum_ebitda", m - 1) + v("ebitda", m))
R(PL, "tax", "Income tax (27% once cumulatively profitable)", "R", "zar",
  lambda m: f"{AD('tax_rate')}*MAX(0,{X('cum_ebitda', m)})" if m == 1 else
  f"{AD('tax_rate')}*(MAX(0,{X('cum_ebitda', m)})-MAX(0,{X('cum_ebitda', m - 1)}))",
  lambda m: P["tax_rate"] * (max(0.0, v("cum_ebitda", m)) - (max(0.0, v("cum_ebitda", m - 1)) if m > 1 else 0.0)))
R(PL, "net_income", "Net income", "R", "zar", lambda m: f"{X('ebitda', m)}-{X('tax', m)}", lambda m: v("ebitda", m) - v("tax", m), bold=True)
SEC(PL, "Memo: software gross margin (net subscriptions, top-ups, setup fees; excl. WhatsApp pass-through & commerce)")
R(PL, "sw_rev", "Software revenue", "R", "zar", lambda m: plus(["pl_rev_subs", "pl_rev_topup", "pl_rev_ent_setup", "pl_rev_agency_setup"], m),
  lambda m: v("pl_rev_subs", m) + v("pl_rev_topup", m) + v("pl_rev_ent_setup", m) + v("pl_rev_agency_setup", m))
R(PL, "sw_cogs", "Software COGS", "R", "zar",
  lambda m: f"{plus(['pl_cogs_ai', 'pl_cogs_hosting', 'pl_cogs_support', 'pl_cogs_cs'], m)}+{X('sw_rev', m)}*{X('proc_rate', m)}",
  lambda m: v("pl_cogs_ai", m) + v("pl_cogs_hosting", m) + v("pl_cogs_support", m) + v("pl_cogs_cs", m) + v("sw_rev", m) * v("proc_rate", m))
R(PL, "sw_gm_pct", "Software gross margin %", "%", "pct", lambda m: f"IF({X('sw_rev', m)}=0,0,1-{X('sw_cogs', m)}/{X('sw_rev', m)})",
  lambda m: 0.0 if v("sw_rev", m) == 0 else 1 - v("sw_cogs", m) / v("sw_rev", m))
R(PL, "sm_total", "Sales & marketing total (programmes + marketing & sales payroll)", "R", "zar",
  lambda m: f"{X('pl_mkt', m)}+{X('pl_hc_Marketing', m)}+{X('pl_hc_Sales & partnerships', m)}",
  lambda m: v("pl_mkt", m) + v("pl_hc_Marketing", m) + v("pl_hc_Sales & partnerships", m))

# =============================================================================
# CASH FLOW
# =============================================================================
SEC(CF, "Operating cash flow")
R(CF, "cf_ebitda", "EBITDA", "R", "zar", lambda m: X("ebitda", m), lambda m: v("ebitda", m))
R(CF, "cf_tax", "Tax paid (same month, simplified)", "R", "zar", lambda m: f"-{X('tax', m)}", lambda m: -v("tax", m))
R(CF, "dr_bal", "Deferred revenue balance (annual self-serve plans: Solo + SME)", "R", "zar",
  lambda m: f"({X('subgross_seg_SO', m)}+{X('subgross_seg_SM', m)})*{AD('annual_share')}*{AD('dr_months')}",
  lambda m: (v("subgross_seg_SO", m) + v("subgross_seg_SM", m)) * P["annual_share"] * P["dr_months"])
R(CF, "d_dr", "Increase in deferred revenue", "R", "zar", lambda m: X("dr_bal", m) if m == 1 else f"{X('dr_bal', m)}-{X('dr_bal', m - 1)}",
  lambda m: v("dr_bal", m) - v("dr_bal", m - 1))
R(CF, "ar_bal", "Receivables balance (agency & enterprise invoices)", "R", "zar",
  lambda m: f"({plus(['subgross_seg_AG', 'subgross_seg_EN', 'ent_setup_rev', 'agency_setup_rev'], m)})*{AD('ar_months')}",
  lambda m: (v("subgross_seg_AG", m) + v("subgross_seg_EN", m) + v("ent_setup_rev", m) + v("agency_setup_rev", m)) * P["ar_months"])
R(CF, "d_ar", "Increase in receivables", "R", "zar", lambda m: X("ar_bal", m) if m == 1 else f"{X('ar_bal', m)}-{X('ar_bal', m - 1)}",
  lambda m: v("ar_bal", m) - v("ar_bal", m - 1))
R(CF, "op_cf", "Operating cash flow (before funding)", "R", "zar",
  lambda m: f"{X('cf_ebitda', m)}+{X('cf_tax', m)}+{X('d_dr', m)}-{X('d_ar', m)}",
  lambda m: v("cf_ebitda", m) + v("cf_tax", m) + v("d_dr", m) - v("d_ar", m), bold=True)
SEC(CF, "Funding (seed only; Series A switched off in every scenario)")
R(CF, "seed_in", "Seed equity", "R", "zar", lambda m: f"IF({MN(m)}={AD('seed_month')},{AD('seed_amount')},0)",
  lambda m: P["seed_amount"] if m == P["seed_month"] else 0.0)
R(CF, "seriesA_in", "Series A equity (optional acceleration; off)", "R", "zar",
  lambda m: f"IF(AND({AD('seriesA_on')}=1,{MN(m)}={AD('seriesA_month')}),{AD('seriesA_amount')},0)",
  lambda m: P["seriesA_amount"] if (P["seriesA_on"] == 1 and m == P["seriesA_month"]) else 0.0)
R(CF, "net_cf", "Net cash flow", "R", "zar", lambda m: plus(["op_cf", "seed_in", "seriesA_in"], m),
  lambda m: v("op_cf", m) + v("seed_in", m) + v("seriesA_in", m), bold=True)
SEC(CF, "Cash (no pre-seed bridge is added: any pre-seed shortfall shows as negative cash and is absorbed by the seed)")
R(CF, "open_cash", "Opening cash", "R", "zar", lambda m: AD("opening_cash") if m == 1 else X("close_cash", m - 1),
  lambda m: P["opening_cash"] if m == 1 else v("close_cash", m - 1))
R(CF, "close_cash", "Closing cash", "R", "zar", lambda m: f"{X('open_cash', m)}+{X('net_cf', m)}", lambda m: v("open_cash", m) + v("net_cf", m), bold=True)
R(CF, "buffer_line", "Minimum-cash buffer (applies from the seed month)", "R", "zar",
  lambda m: f"IF({MN(m)}>={AD('seed_month')},{AD('min_cash_buffer')},0)", lambda m: P["min_cash_buffer"] if m >= P["seed_month"] else 0.0)
R(CF, "headroom", "Headroom over the buffer", "R", "zar", lambda m: f"{X('close_cash', m)}-{X('buffer_line', m)}",
  lambda m: v("close_cash", m) - v("buffer_line", m))
R(CF, "burn3", "Average operating cash flow, trailing 3 months", "R", "zar", lambda m: f"AVERAGE({XR('op_cf', max(1, m - 2), m)})",
  lambda m: sum(v("op_cf", k) for k in range(max(1, m - 2), m + 1)) / (m - max(1, m - 2) + 1))
R(CF, "runway_m", "Runway at trailing burn (months)", "months", "n1",
  lambda m: f"IF({X('burn3', m)}>=0,\"CF positive\",{X('close_cash', m)}/-{X('burn3', m)})",
  lambda m: "CF positive" if v("burn3", m) >= 0 else v("close_cash", m) / -v("burn3", m))
SEC(CF, "Helper rows for key outputs (999 = condition not met; 1E+15 = month excluded)")
R(CF, "flag_be", "EBITDA >= 0 (month #)", "month #", "n0", lambda m: f"IF({X('ebitda', m)}>=0,{MN(m)},999)", lambda m: m if v("ebitda", m) >= 0 else 999)
R(CF, "fwd_min_ebitda", "Lowest EBITDA from this month onward", "R", "zar", lambda m: f"MIN({XR('ebitda', m, M)})", lambda m: min(V["ebitda"][m:M + 1]))
R(CF, "flag_be_sus", "EBITDA stays >= 0 from this month (month #)", "month #", "n0",
  lambda m: f"IF({X('fwd_min_ebitda', m)}>=0,{MN(m)},999)", lambda m: m if v("fwd_min_ebitda", m) >= 0 else 999)
R(CF, "flag_cfpos", "Operating cash flow >= 0 (month #)", "month #", "n0", lambda m: f"IF({X('op_cf', m)}>=0,{MN(m)},999)",
  lambda m: m if v("op_cf", m) >= 0 else 999)
R(CF, "fwd_min_opcf", "Lowest operating cash flow from this month onward", "R", "zar", lambda m: f"MIN({XR('op_cf', m, M)})",
  lambda m: min(V["op_cf"][m:M + 1]))
R(CF, "flag_cfpos_sus", "Operating cash flow stays >= 0 from this month (month #)", "month #", "n0",
  lambda m: f"IF({X('fwd_min_opcf', m)}>=0,{MN(m)},999)", lambda m: m if v("fwd_min_opcf", m) >= 0 else 999)
R(CF, "flag_neg", "Closing cash < 0 after the seed lands (month #)", "month #", "n0",
  lambda m: f"IF(AND({MN(m)}>={AD('seed_month')},{X('close_cash', m)}<0),{MN(m)},999)",
  lambda m: m if (m >= P["seed_month"] and v("close_cash", m) < 0) else 999)
R(CF, "flag_buf", "Closing cash below buffer after the seed lands (month #)", "month #", "n0",
  lambda m: f"IF(AND({MN(m)}>={AD('seed_month')},{X('close_cash', m)}<{AD('min_cash_buffer')}),{MN(m)},999)",
  lambda m: m if (m >= P["seed_month"] and v("close_cash", m) < P["min_cash_buffer"]) else 999)
R(CF, "h_cash_seed", "Closing cash in seed month", "R", "zar", lambda m: f"IF({MN(m)}={AD('seed_month')},{X('close_cash', m)},0)",
  lambda m: v("close_cash", m) if m == P["seed_month"] else 0.0)
R(CF, "h_cash_post", "Closing cash from the seed month (1E+15 before)", "R", "zar",
  lambda m: f"IF({MN(m)}>={AD('seed_month')},{X('close_cash', m)},1E+15)", lambda m: v("close_cash", m) if m >= P["seed_month"] else 1e15)
R(CF, "h_cash_pre", "Closing cash before the seed month (1E+15 after)", "R", "zar",
  lambda m: f"IF({MN(m)}<{AD('seed_month')},{X('close_cash', m)},1E+15)", lambda m: v("close_cash", m) if m < P["seed_month"] else 1e15)
R(CF, "h_burn", "Operating cash flow in the 12 months after seed", "R", "zar",
  lambda m: f"IF(AND({MN(m)}>{AD('seed_month')},{MN(m)}<={AD('seed_month')}+12),{X('op_cf', m)},0)",
  lambda m: v("op_cf", m) if (P["seed_month"] < m <= P["seed_month"] + 12) else 0.0)


def run_monthly(p):
    """Python mirror: evaluate every row month by month in compute order."""
    V.clear()
    P.clear()
    P.update(p)
    for pass_ in (1, 2):
        for m in MONTHS:
            for rw in ROWS:
                if rw["kind"] != "row":
                    continue
                if pass_ == 1 and rw["key"] in ("fwd_min_ebitda", "flag_be_sus", "fwd_min_opcf", "flag_cfpos_sus"):
                    continue
                if pass_ == 2 and rw["key"] not in ("fwd_min_ebitda", "flag_be_sus", "fwd_min_opcf", "flag_cfpos_sus"):
                    continue
                V[rw["key"]][m] = rw["py"](m)
    return V
