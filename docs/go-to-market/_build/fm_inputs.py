"""FluxMuse financial model v2: input registry (Assumptions, Pricing, headcount plan).

Every driver is registered once here with its cell address, unit, value(s) and
source note. Both the Excel writer and the Python mirror read from this registry,
so an input can never differ between the workbook and the JSON/charts.

v2 (founder decisions 2026-09-11): R25M seed in Feb 2027 must reach profitability alone;
lean pre-seed mode; Gauteng pilot converts Dec 2026; Founding Member launch discount;
markets ZA -> NG/KE/GH -> Rest of rail-covered Africa (USD) -> Botswana & Namibia (off);
local/USD price points at parity with FX drift and quarterly repricing; segment-based
acquisition; MRR-gated hiring and launches; marketing capped as a share of MRR.
"""

SCENARIOS = ["Conservative", "Base", "Upside"]

TIERS = ["S", "G", "Sc", "A", "E"]
TIER_NAME = {"S": "Starter", "G": "Growth", "Sc": "Scale", "A": "Agency", "E": "Enterprise"}

MARKETS = ["ZA", "NG", "KE", "GH", "RoA", "BWNA"]
NONZA = ["NG", "KE", "GH", "RoA", "BWNA"]
WAVE1 = ["NG", "KE", "GH"]
WINDOW_MKTS = ["ZA", "NG", "KE", "GH"]          # markets with a Founding Member launch window
FX_MKTS = ["NG", "KE", "GH", "RoA"]              # markets billed in a non-ZAR currency
MARKET_NAME = {"ZA": "South Africa", "NG": "Nigeria", "KE": "Kenya", "GH": "Ghana",
               "RoA": "Rest of rail-covered Africa (19 countries, USD, self-serve)",
               "BWNA": "Botswana & Namibia (coming soon; off by default)"}
MARKET_SHORT = {"ZA": "South Africa", "NG": "Nigeria", "KE": "Kenya", "GH": "Ghana",
                "RoA": "Rest of Africa (USD)", "BWNA": "Botswana & Namibia"}
CURRENCY = {"ZA": "ZAR", "NG": "NGN", "KE": "KES", "GH": "GHS", "RoA": "USD", "BWNA": "ZAR"}

SEGMENTS = ["SO", "SM", "AG", "EN"]
SEG_NAME = {"SO": "Solo entrepreneurs", "SM": "SMEs", "AG": "Agencies / partners (Agency tier at partner wholesale)",
            "EN": "Enterprise (inbound only)"}
SEG_SHORT = {"SO": "Solo", "SM": "SMEs", "AG": "Agencies", "EN": "Enterprise"}
# stock type: (key, segment, tier, partner-wholesale price?, label)
# v2: agency client sub-accounts are no longer separate paying stocks. Partners buy the Agency tier
# (50 client sub-accounts included) at partner wholesale; clients on their own plans would earn a
# referral commission, which is undecided and not modelled.
STOCK_TYPES = [("SO_S", "SO", "S", False, "Solo: Starter"), ("SO_G", "SO", "G", False, "Solo: Growth (upgraded or direct)"),
               ("SM_G", "SM", "G", False, "SME: Growth"), ("SM_Sc", "SM", "Sc", False, "SME: Scale (upgraded or direct)"),
               ("AG_A", "AG", "A", True, "Agency / partner: Agency tier"),
               ("EN_E", "EN", "E", False, "Enterprise (inbound)")]
ST = {k: (seg, t, w, lab) for k, seg, t, w, lab in STOCK_TYPES}
MARKET_STOCKS = {"ZA": [s[0] for s in STOCK_TYPES],
                 "NG": [s[0] for s in STOCK_TYPES[:5]], "KE": [s[0] for s in STOCK_TYPES[:5]],
                 "GH": [s[0] for s in STOCK_TYPES[:5]],
                 "RoA": [s[0] for s in STOCK_TYPES[:4]], "BWNA": [s[0] for s in STOCK_TYPES[:4]]}
# (stock key, market, stock type)
STOCKS = [(f"{r}_{st}", r, st) for r in MARKETS for st in MARKET_STOCKS[r]]

DEPTS = ["Leadership", "Engineering & product", "Marketing", "Sales & partnerships",
         "Customer success", "G&A & compliance", "Country teams"]

# ---------------------------------------------------------------------------
# Assumptions sheet registry
# ---------------------------------------------------------------------------
ENTRIES = []
ADDR = {}
ASSUMP_FIRST_ROW = 9
_row = [ASSUMP_FIRST_ROW]


def _next():
    r = _row[0]
    _row[0] += 1
    return r


def section(title):
    ENTRIES.append({"kind": "section", "title": title, "row": _next()})


def note(text):
    ENTRIES.append({"kind": "note", "title": text, "row": _next()})


def inp(key, label, unit, value, src, fmt="num"):
    r = _next()
    ENTRIES.append({"kind": "inp", "key": key, "label": label, "unit": unit, "value": value, "src": src, "fmt": fmt, "row": r})
    ADDR[key] = f"Assumptions!$B${r}"


def scen(key, label, unit, triple, src, fmt="num"):
    r = _next()
    ENTRIES.append({"kind": "scen", "key": key, "label": label, "unit": unit, "values": triple, "src": src, "fmt": fmt, "row": r})
    ADDR[key] = f"Assumptions!$B${r}"


def der(key, label, unit, xl, py, src, fmt="num"):
    r = _next()
    ENTRIES.append({"kind": "der", "key": key, "label": label, "unit": unit, "xl": xl, "py": py, "src": src, "fmt": fmt, "row": r})
    ADDR[key] = f"Assumptions!$B${r}"


ADDR["scenario"] = "Assumptions!$B$6"
ADDR["scen_idx"] = "Assumptions!$B$7"

section("General, funding & tax")
inp("fx", "FX rate", "ZAR per US$", 18.50, "Facts file §2: R18.50 = US$1 (ASSUMPTION)", "num2")
inp("tax_rate", "SA corporate income tax rate", "%", 0.27, "SARS 27%. Applied only once cumulative EBITDA is positive (assessed-loss simplification).", "pct")
inp("opening_cash", "Opening cash (1 Oct 2026)", "R", 500000, "[[CONFIRM]] founder to confirm cash in bank at 1 Oct 2026; default R500k", "zar")
inp("seed_amount", "Seed raise", "R", 25000000, "Facts file §7: Seed R25M (≈US$1.35M). Must reach profitability alone (founder, 2026-09-11)", "zar")
inp("seed_month", "Seed lands in model month #", "month #", 5, "Month 5 = Feb 2027: pilot ends 30 Nov 2026, results Dec 2026, close Feb 2027", "int")
inp("min_cash_buffer", "Minimum-cash buffer (closing cash must stay above this from the seed month on)", "R", 3000000, "Founder constraint: never below R3.0M after the seed lands", "zar")
inp("seriesA_on", "Include Series A? (1 = yes, 0 = no)", "switch", 0, "OFF in every scenario. Optional acceleration only, not needed for survival", "int")
inp("seriesA_amount", "Series A amount (optional acceleration, if switched on)", "R", 0, "Default 0 (founder: no Series A in Base or Conservative)", "zar")
inp("seriesA_month", "Series A lands in model month #", "month #", 30, "Month 30 = Mar 2029 (illustrative)", "int")

section("Pilot, launch & lean pre-seed mode")
inp("pilot_brands", "Pilot brands (Gauteng), free during the pilot", "brands", 12, "Facts file §6: 12 brands, Sept-30 Nov 2026, not paying", "int")
inp("pilot_end_month", "Last pilot month #", "month #", 2, "Month 2 = Nov 2026", "int")
inp("pilot_conv", "Pilot brands converting to paid", "%", 0.75, "ASSUMPTION: 75% -> 9 brands; replace with pilot outcome", "pct")
inp("pilot_convert_month", "Pilot conversion month #", "month #", 3, "Month 3 = Dec 2026 (SA commercial launch 1 Dec 2026)", "int")
inp("pilot_disc", "Pilot Founding terms: discount", "% off", 0.50, "Facts file §2: pilot brands get 50% off", "pct")
inp("pilot_disc_months", "Pilot Founding terms: discounted monthly bills", "bills", 2, "First 2 monthly bills", "int")
for _s, _v in [("SO", 0.40), ("SM", 0.45), ("AG", 0.15)]:
    inp(f"pilot_mix_{_s}", f"Pilot conversions by segment: {SEG_SHORT[_s]}", "%", _v,
        "Solo -> Starter, SME -> Growth, Agency -> Agency tier. Case-study slots span solo/SME/agency" if _s == "SO" else "", "pct")
inp("pilot_cost", "Pilot programme cost while the pilot runs", "R / month", 15000, "Onboarding visits, content support, WhatsApp/AI usage for free brands (ASSUMPTION)", "zar")
inp("hosting_lean", "Hosting base before the seed (lean mode)", "R / month", 15000, "Supabase/Vercel at pilot scale (ASSUMPTION)", "zar")
inp("lean_overhead", "Overheads before the seed (accounting, banking, Meta/legal minimum)", "R / month", 15000, "Lean mode replaces fixed G&A and the legal retainer until the seed lands", "zar")
note("Lean mode (months before the seed): founders only, no paid marketing, no office/travel; hiring, brand, partner and legal budgets start in the seed month.")

section("Sensitivity & option levers (leave at defaults for the scenarios)")
inp("vol_mult", "New-customer volume multiplier", "x", 1.0, "Scales self-serve trials in every market; Sensitivity sheet", "x2")
inp("churn_sens", "Churn sensitivity multiplier", "x", 1.0, "Multiplies all churn; Sensitivity sheet", "x2")
inp("disc_option", "Launch discount option (1 = A Launch Sprint, 2 = B Founding Member, 3 = None)", "option", 2, "Facts file §2: B decided; A and None are sensitivities only", "int")
inp("fmA_disc", "Option A (Launch Sprint): discount on the first monthly bill", "% off", 0.50, "Facts file §2 (record only; sensitivity)", "pct")
inp("fmB_disc", "Option B (Founding Member): discount on the first 2 monthly bills", "% off", 0.30, "Facts file §2: R349 / R1,399 / R3,499; not offered on Agency", "pct")
inp("fm_uplift", "New sign-up uplift inside a launch window", "%", 0.20, "ASSUMPTION: +20% sign-ups while the offer runs; validate with ZA Dec-Jan data", "pct")
inp("fm_new_churn", "Churn of new sign-ups between discounted bill 1 and 2", "%", 0.08, "Used only to size the second discounted bill (ASSUMPTION)", "pct")
inp("fx_shock", "FX shock: ZAR stronger vs NGN/KES/GHS/USD", "%", 0.0, "Sensitivity sets 15%", "pct")
inp("fx_shock_month", "FX shock starts in month #", "month #", 25, "Month 25 = Oct 2028, once NG/KE/GH are live", "int")

section("Scenario drivers (switched by the selector above: CHOOSE on columns D:F)")
for _y, _t in zip(range(1, 6), [(0.10, 0.12, 0.14), (0.035, 0.045, 0.06), (0.025, 0.035, 0.045), (0.015, 0.028, 0.032), (0.01, 0.015, 0.02)]):
    scen(f"g_fy{_y}", f"Monthly growth in self-serve trials: FY{_y}", "% m/m", _t, "Per market from its launch month; decays as channels mature" if _y == 1 else "", "pct")
scen("conv_mult", "Trial-to-paid conversion multiplier (on segment conversion)", "x", (0.85, 1.00, 1.20), "Conservative Solo 9.4%; Upside Solo 13.2%", "x2")
scen("churn_mult", "Churn multiplier", "x", (1.20, 1.00, 0.85), "", "x2")
scen("cac_mult", "Paid CAC multiplier", "x", (1.20, 1.00, 0.85), "Ad-auction inflation vs creative & referral efficiency", "x2")
scen("launch_delay", "Expansion timing shift (months, + = later)", "months", (3, 0, -2), "Shifts planned NG/KE/GH/Rest/BW-NA launches (MRR gates still apply)", "int")
scen("ent_mult", "Inbound enterprise deal multiplier", "x", (0.5, 1.0, 1.5), "", "x2")
scen("cap_pct", "COST DISCIPLINE: paid acquisition cap, % of last month's net MRR", "% of MRR", (0.30, 0.35, 0.50), "Paid spend = MIN(desired, floor + cap x MRR); unfunded paid sign-ups are not acquired", "pct")
scen("gate_mult", "COST DISCIPLINE: hiring & launch MRR-gate multiplier", "x", (1.40, 1.00, 0.80), "Each hire/launch waits for its MRR milestone x this. Conservative waits for 40% more MRR (1.35x is the smallest that holds the R3.0M buffer); Upside hires 20% earlier", "x2")
scen("commerce_fee", "Commerce platform fee on WhatsApp checkout GMV", "% of GMV", (0.0, 0.0, 0.0075), "NOT IN CURRENT PRICING: founder decision. 0% in Base & Conservative; 0.75% Upside only", "pct2")

section("Launch discount option parameters (formulas on the option switch)")
der("fm_mo_disc", "Monthly plans: discount on launch-window sign-ups", "% off",
    lambda AD: f"CHOOSE({AD('disc_option')},{AD('fmA_disc')},{AD('fmB_disc')},0)", lambda p: [p["fmA_disc"], p["fmB_disc"], 0.0][p["disc_option"] - 1],
    "A: 50% off month 1; B: 30% off months 1-2; None: 0. Never applied to Agency / partner sign-ups", "pct")
der("fm_mo_months", "Monthly plans: discounted billing months", "months",
    lambda AD: f"CHOOSE({AD('disc_option')},1,2,0)", lambda p: [1, 2, 0][p["disc_option"] - 1], "", "int")
der("fm_bonus", "Annual plans: bonus free months", "months",
    lambda AD: f"CHOOSE({AD('disc_option')},1,2,0)", lambda p: [1, 2, 0][p["disc_option"] - 1],
    "B: 14 months for the price of 12. Modelled by recognising the annual fee over 12 + bonus months", "int")
der("fm_window", "Launch window length", "months",
    lambda AD: f"CHOOSE({AD('disc_option')},1,2,0)", lambda p: [1, 2, 0][p["disc_option"] - 1],
    "A: 30 days; B: 60 days (ZA: 1 Dec 2026-31 Jan 2027); USD markets: no window", "int")
der("fm_uplift_eff", "Sign-up uplift applied inside windows", "%",
    lambda AD: f"IF({AD('disc_option')}=3,0,{AD('fm_uplift')})", lambda p: 0.0 if p["disc_option"] == 3 else p["fm_uplift"], "", "pct")

section("Markets & sequence (ZA first; NG/KE/GH wave 1; Rest of Africa self-serve; BW/NA coming soon; gated countries = 0)")
inp("launch_ZA", "South Africa commercial launch month #", "month #", 3, "1 Dec 2026 (pilot ends 30 Nov)", "int")
inp("trials_launch_ZA", "Self-serve trials in launch month: South Africa", "trials / month", 250, "2.5-3M SA SMMEs; pilot word of mouth", "int")
_MK = {  # plan, gate, on, trials, launch mkt, entry, ongoing, cac idx, churn idx, agency inbound, source
    "NG": (14, 900000, 1, 220, 350000, 300000, 12000, 0.75, 1.15, 0.25, "Nov 2027: largest MSME base; Paystack/pawaPay/Fincra"),
    "KE": (17, 1200000, 1, 150, 300000, 250000, 12000, 0.80, 1.05, 0.20, "Feb 2028: M-Pesa via pawaPay"),
    "GH": (20, 1500000, 1, 110, 250000, 200000, 10000, 0.80, 1.10, 0.15, "May 2028: MoMo via pawaPay"),
    "RoA": (26, 2500000, 1, 120, 0, 150000, 20000, 0.60, 1.25, 0.0, "Nov 2028: 19 countries, USD, self-serve only, no local team"),
    "BWNA": (30, 3000000, 0, 40, 0, 100000, 6000, 0.90, 1.00, 0.0, "Coming soon: switch on once a rail covers BW/NA"),
}
for _r, (_pl, _gt, _on, _tr, _lm, _en, _og, _ci, _chi, _ai, _src) in _MK.items():
    inp(f"on_{_r}", f"{MARKET_SHORT[_r]}: switch (1 = on)", "switch", _on, "Default OFF: no secured rail yet" if _r == "BWNA" else "", "int")
    inp(f"launch_plan_{_r}", f"{MARKET_SHORT[_r]}: planned launch month # (earliest)", "month #", _pl, _src, "int")
    inp(f"launch_gate_{_r}", f"{MARKET_SHORT[_r]}: MRR gate for the launch decision", "R net MRR", _gt,
        "Decision (and country-lead hire) needs last month's net MRR >= gate x gate multiplier; launch follows 2 months later", "zar")
    inp(f"trials_launch_{_r}", f"{MARKET_SHORT[_r]}: self-serve trials in launch month", "trials / month", _tr, "", "int")
    inp(f"cac_idx_{_r}", f"{MARKET_SHORT[_r]}: paid CAC index vs SA", "x", _ci, "Cheaper media; lower price point", "x2")
    inp(f"churn_idx_{_r}", f"{MARKET_SHORT[_r]}: churn index vs SA", "x", _chi, "FX affordability pressure (ASSUMPTION)", "x2")
    inp(f"entry_{_r}", f"{MARKET_SHORT[_r]}: local compliance & registration (one-off at launch)", "R", _en,
        {"NG": "NDPR registration, entity, local counsel", "KE": "KDPA (ODPC) registration, local counsel",
         "GH": "Ghana DPC registration, local counsel", "RoA": "Digital-services VAT registrations (hub approach)",
         "BWNA": "BW/NA data-protection & tax registration"}[_r], "zar")
    inp(f"ongoing_{_r}", f"{MARKET_SHORT[_r]}: ongoing local compliance", "R / month", _og, "Local accounting, DPO filings, VAT returns", "zar")
    if _r in WAVE1:
        inp(f"launch_mkt_{_r}", f"{MARKET_SHORT[_r]}: launch marketing budget (spread over first 3 months)", "R", _lm, "Launch campaign, local creators, events", "zar")
        inp(f"agency_inbound_{_r}", f"{MARKET_SHORT[_r]}: inbound agency sign-ups after launch", "agencies / month", _ai, "", "num2")
inp("roa_budget", "Rest of Africa: always-on self-serve marketing budget", "R / month", 20000, "Low spend: SEO, WhatsApp short links, French/Portuguese content", "zar")
inp("bwna_budget", "Botswana & Namibia: marketing budget (if on)", "R / month", 10000, "", "zar")
inp("agencies_per_lead", "Agencies signed per country lead (NG/KE/GH)", "agencies / month", 0.4, "Country lead runs the local partner programme", "num2")
inp("travel_per_region", "Travel per live wave-1 country", "R / month", 10000, "Lagos/Nairobi/Accra", "zar")

section("Self-serve funnel by segment (Solo & SME share each market's trials)")
for _y, _v in zip(range(1, 6), [0.65, 0.60, 0.55, 0.50, 0.45]):
    inp(f"paid_share_fy{_y}", f"Share of sign-ups needing paid acquisition: FY{_y}", "%", _v, "Organic/referral grows over time" if _y == 1 else "", "pct")
inp("solo_share", "Solo entrepreneurs' share of self-serve trials", "%", 0.65, "Facts file §4b: solo = Meta/TikTok/WhatsApp self-serve; SMEs = content, networks, referrals", "pct")
inp("conv_SO", "Trial-to-paid conversion: Solo", "%", 0.11, "No-card trials convert 8-15%; validate with pilot", "pct")
inp("conv_SM", "Trial-to-paid conversion: SME", "%", 0.14, "Guided onboarding call lifts conversion", "pct")
inp("so_mix_G", "Solo new customers starting on Growth", "%", 0.10, "Mainly Starter", "pct")
inp("sm_mix_Sc", "SME new customers starting on Scale", "%", 0.15, "Mainly Growth", "pct")
inp("upg_SO", "Monthly upgrade rate: Solo Starter -> Growth", "% / month", 0.010, "ASSUMPTION", "pct")
inp("upg_SM", "Monthly upgrade rate: SME Growth -> Scale", "% / month", 0.008, "ASSUMPTION", "pct")
inp("pb_max", "COST DISCIPLINE: maximum CAC payback for paid acquisition", "months", 12, "Paid acquisition in a segment & market is switched off if CAC / (ARPA x GM) exceeds this [[CONFIRM]]", "int")
inp("pb_gm", "Gross margin assumed in the payback test", "%", 0.70, "Conservative vs modelled software GM", "pct")

section("Monthly logo churn by segment & tier (before scenario, market and sensitivity multipliers)")
for _k, _v, _s in [("SO_S", 0.065, "Brief: SMB Starter 5-7%"), ("SO_G", 0.040, ""), ("SM_G", 0.030, "SME Growth 3-4%"),
                   ("SM_Sc", 0.022, "Scale 2-3%"), ("AG_A", 0.020, "Agency 2%"), ("EN_E", 0.010, "Enterprise 1%")]:
    inp(f"churn_{_k}", f"Monthly churn: {ST[_k][3]}", "% / month", _v, _s, "pct")

section("Agency channel & inbound enterprise")
inp("agency_inbound_ZA", "South Africa: inbound agency sign-ups", "agencies / month", 0.5, "/for-agencies page, from SA launch", "num2")
inp("agencies_per_pm", "Agencies signed per partnerships manager (SA)", "agencies / month", 1.5, "Flux_Partner programme", "num2")
note("Partner wholesale price (Agency tier -30%) and the share of agency customers on it live on the Pricing sheet. Partner referral commission: undecided, NOT modelled.")
for _y, _v in zip(range(1, 6), [1, 2, 4, 6, 8]):
    inp(f"ent_fy{_y}", f"Inbound enterprise deals (SA): FY{_y}", "deals / year", _v,
        "Facts file §4b: inbound only, no enterprise sales motion; near-zero in FY1" if _y == 1 else "", "num1")

section("Other revenue streams")
inp("topup_attach", "AI-credit top-up attach rate", "% of workspaces / month", 0.10, "ASSUMPTION", "pct")
inp("topup_pack", "Average top-up pack value (FY1 price)", "R", 350, "Escalates with price escalator", "zar")
inp("topup_credits", "AI credits per average top-up pack", "credits", 14000, "", "int")
for _t, _v in [("S", 0), ("G", 250), ("Sc", 800), ("A", 1500), ("E", 5000)]:
    inp(f"wa_msgs_{_t}", f"Billable WhatsApp template messages per workspace: {TIER_NAME[_t]}", "messages / month", _v, "Meta per-message pricing" if _t == "S" else "", "int")
inp("wa_meta_cost", "Average Meta fee per billable message", "R", 0.60, "Blend of marketing and utility template rates (ASSUMPTION)", "num2")
inp("wa_markup", "Markup on Meta messaging fees (pass-through resale)", "%", 0.25, "Revenue shown gross", "pct")
inp("commerce_active", "Share of Growth/Scale/Enterprise workspaces with live WhatsApp checkout", "%", 0.30, "", "pct")
inp("gmv_per_store", "WhatsApp checkout GMV per active store (FY1)", "R / month", 20000, "Validate with pilot orders/GMV", "zar")
inp("gmv_growth", "Annual growth in GMV per active store", "% / year", 0.15, "", "pct")
inp("ent_setup_fee", "Enterprise onboarding / setup fee", "R per deal", 25000, "", "zar")
inp("agency_setup_fee", "Agency white-label setup fee", "R per new agency", 4999, "", "zar")
note("Campaign Financing (credit facilities / instalment plans) is an UPSIDE NOT included in any scenario.")

section("Cost of revenue (COGS)")
inp("credits_util", "Utilisation of included AI credits", "%", 0.40, "", "pct")
inp("ai_cost_1k", "AI inference cost per 1,000 credits (FY1)", "R", 12.00, "ASSUMPTION", "num2")
inp("ai_cost_decline", "Annual decline in inference cost per credit", "% / year", 0.10, "", "pct")
inp("hosting_fixed", "Hosting base from the seed month", "R / month", 30000, "Supabase + Edge Functions on Vercel", "zar")
inp("hosting_per_ws", "Hosting cost per paying workspace", "R / month", 35, "", "zar")
inp("card_fee", "Blended payment processing fee", "% of billed revenue", 0.029, "Yoco/Ozow/Paystack", "pct")
inp("mm_extra", "Extra mobile-money / FX fee on non-SA revenue", "% of non-SA revenue", 0.015, "pawaPay/Fincra collections + FX spread", "pct")
inp("support_per_ws", "Variable support cost per workspace", "R / month", 50, "", "zar")

section("Operating expenses (budgets scale with MRR: cost discipline)")
inp("sal_esc", "Annual salary escalation", "% / year", 0.06, "", "pct")
inp("oncost", "Employment on-costs", "% of salary", 0.10, "UIF, SDL, benefits", "pct")
inp("cac_SO", "Paid CAC per paid-acquired customer: Solo", "R", 2200, "Meta/TikTok performance (ASSUMPTION)", "zar")
inp("cac_SM", "Paid CAC per paid-acquired customer: SME", "R", 6500, "Content, webinars, networks, paid search (ASSUMPTION)", "zar")
inp("cac_infl", "Annual CAC inflation", "% / year", 0.05, "", "pct")
inp("paid_floor", "Paid acquisition floor budget from the seed month", "R / month", 40000, "Lets paid acquisition start before MRR is large", "zar")
for _y, _v in zip(range(1, 6), [50000, 120000, 220000, 320000, 420000]):
    inp(f"brand_fy{_y}", f"Brand, content & community: ceiling FY{_y}", "R / month", _v, "Budget = MIN(ceiling, floor + % of MRR)" if _y == 1 else "", "zar")
inp("brand_floor", "Brand budget floor from the seed month", "R / month", 25000, "", "zar")
inp("brand_pct", "Brand budget as % of last month's net MRR", "% of MRR", 0.04, "", "pct")
inp("partner_cost_per_agency", "Partner programme cost per new agency", "R", 6000, "", "zar")
inp("partner_events", "Partner programme events & directory", "R / month", 15000, "", "zar")
inp("partner_events_start", "Partner programme events start month #", "month #", 8, "May 2027", "int")
inp("ent_sales_per_deal", "Inbound enterprise handling cost per deal", "R", 25000, "Solutioning, security reviews, travel", "zar")
inp("office_per_fte", "Office / co-working per FTE (from seed)", "R / month", 4000, "", "zar")
for _y, _v in zip(range(1, 6), [30000, 55000, 80000, 105000, 130000]):
    inp(f"ga_fy{_y}", f"Fixed G&A (accounting, audit, insurance, banking): FY{_y}", "R / month", _v, "", "zar")
inp("equip_per_hire", "Equipment per new hire (expensed)", "R", 20000, "", "zar")
inp("legal_fixed", "Meta, legal & compliance base (from seed)", "R / month", 20000, "POPIA Information Officer, Meta Tech Provider, contracts", "zar")
inp("tools_per_fte", "Software & tools per FTE", "R / month", 3000, "", "zar")
inp("travel_per_fte", "Travel per FTE (from seed)", "R / month", 2000, "", "zar")

section("Working capital (simplified)")
inp("dr_months", "Deferred revenue held on annual self-serve plans", "months of annual-plan revenue", 5.5, "", "num1")
inp("ar_months", "Receivables on agency & enterprise invoices", "months of revenue", 1.0, "", "num1")

HC_HEADER_ROW = _row[0] + 1
HC_FIRST_ROW = HC_HEADER_ROW + 1

# ---------------------------------------------------------------------------
# Pricing sheet registry (fixed layout)
# ---------------------------------------------------------------------------
PRICING = {  # tier: (ZAR list monthly, included credits, note)
    "S": (499, 5000, "1 brand, 3 channels; solo founders"),
    "G": (1999, 25000, "Most popular: e-commerce, WhatsApp commerce, USSD, integrations"),
    "Sc": (4999, 100000, "10 brands, 40 channels; API, white-label reports"),
    "A": (7999, 500000, "Full white-label, 50 sub-accounts, reseller billing"),
    "E": (19999, 750000, "From R19,999; 'unlimited' credits modelled as 750k/mo"),
}
LOCAL = {  # tier: NGN, KES, GHS, USD monthly price points (facts file §2)
    "S": (41000, 3999, 339, 27), "G": (165000, 15999, 1359, 109), "Sc": (413000, 39999, 3399, 269),
    "A": (662000, 64499, 5439, 429), "E": (1650000, 161000, 13600, 1099),
}
WHOLESALE = (5599, (463000, 44999, 3799, 299))   # partner wholesale Agency tier: ZAR, (NGN, KES, GHS, USD)
PILOT_PRICE = {"S": 249, "G": 999, "Sc": 2499, "A": 3999}
FM_PRICE = {"S": 349, "G": 1399, "Sc": 3499}
PRICE_KEYS = TIERS + ["W"]
LOCAL_COLS = {"NGN": "H", "KES": "I", "GHS": "J", "USD": "K"}
PRICING_TIER_ROW0 = 5
for _i, _t in enumerate(PRICE_KEYS):
    ADDR[f"price_{_t}"] = f"Pricing!$B${PRICING_TIER_ROW0 + _i}"
    ADDR[f"credits_{_t}"] = f"Pricing!$E${PRICING_TIER_ROW0 + _i}"
    for _c, _cl in LOCAL_COLS.items():
        ADDR[f"local_{_c}_{_t}"] = f"Pricing!${_cl}${PRICING_TIER_ROW0 + _i}"
PRICING_SCALARS = [
    ("price_esc", "Annual price escalator (applied each 1 Oct, all markets)", "% / year", 0.06, "CPI-linked list-price increase (ASSUMPTION)", "pct"),
    ("annual_share", "Share of subscriptions on annual billing", "%", 0.25, "Annual = 10x monthly", "pct"),
    ("annual_months", "Months charged on an annual plan", "months", 10, "Facts file §2", "int"),
    ("annual_factor", "Effective price factor from annual-billing mix", "x", None, "Formula: 1 - annual share x (12 - months charged) / 12", "x3"),
    ("partner_share", "Share of agency-segment customers on partner wholesale pricing", "%", 1.0, "Founder decision 2026-09-11: partners buy Agency at 30% off list; default 100% of agency customers", "pct"),
]
PRICING_SCALAR_ROW0 = 12
for _i, _s in enumerate(PRICING_SCALARS):
    ADDR[_s[0]] = f"Pricing!$B${PRICING_SCALAR_ROW0 + _i}"
FX_ROWS = [  # key, label, unit, value, note, fmt
    ("rate_NGN", "NGN per R1 at price-setting (Sept 2026)", "NGN per ZAR", 82.83, "Facts file §2 mid-market rate", "num2"),
    ("rate_KES", "KES per R1 at price-setting", "KES per ZAR", 8.07, "Facts file §2", "num2"),
    ("rate_GHS", "GHS per R1 at price-setting", "GHS per ZAR", 0.68, "Facts file §2", "num2"),
    ("dep_NG", "Annual depreciation of NGN vs ZAR", "% / year", -0.10, "ASSUMPTION", "pct"),
    ("dep_KE", "Annual depreciation of KES vs ZAR", "% / year", -0.03, "ASSUMPTION", "pct"),
    ("dep_GH", "Annual depreciation of GHS vs ZAR", "% / year", -0.08, "ASSUMPTION", "pct"),
    ("dep_RoA", "Annual depreciation of USD vs ZAR", "% / year", 0.0, "ASSUMPTION (USD markets)", "pct"),
    ("reprice_thr", "Repricing trigger: drift in ZAR value of local prices", "%", 0.10, "Facts file §2: reprice if FX moves more than ±10%", "pct"),
    ("reprice_on", "Quarterly repricing policy on? (1 = yes)", "switch", 1, "Reviewed each quarter; new price applies one quarter after the drift is observed", "int"),
]
FX_ROW0 = PRICING_SCALAR_ROW0 + len(PRICING_SCALARS) + 2
for _i, _s in enumerate(FX_ROWS):
    ADDR[_s[0]] = f"Pricing!$B${FX_ROW0 + _i}"
PAR_HDR_ROW = FX_ROW0 + len(FX_ROWS) + 1
PAR_ROW0 = PAR_HDR_ROW + 2
PAR_COLS = {"ZA": "B", "NG": "C", "KE": "D", "GH": "E", "RoA": "F", "BWNA": "G"}
for _i, _t in enumerate(PRICE_KEYS):
    for _r, _cl in PAR_COLS.items():
        ADDR[f"price_{_r}_{_t}"] = f"Pricing!${_cl}${PAR_ROW0 + _i}"


def par_price_xl(r, t):
    row = PRICING_TIER_ROW0 + PRICE_KEYS.index(t)
    return {"ZA": f"$B${row}", "BWNA": f"$B${row}", "NG": f"$H${row}/{ADDR['rate_NGN'].split('!')[1]}",
            "KE": f"$I${row}/{ADDR['rate_KES'].split('!')[1]}", "GH": f"$J${row}/{ADDR['rate_GHS'].split('!')[1]}",
            "RoA": f"$K${row}*{ADDR['fx']}"}[r]


def par_price_py(p, r, t):
    ngn, kes, ghs, usd = LOCAL[t] if t != "W" else WHOLESALE[1]
    zar = PRICING[t][0] if t != "W" else WHOLESALE[0]
    return {"ZA": zar, "BWNA": zar, "NG": ngn / p["rate_NGN"], "KE": kes / p["rate_KES"],
            "GH": ghs / p["rate_GHS"], "RoA": usd * p["fx"]}[r]


# ---------------------------------------------------------------------------
# Headcount plan (monthly cost-to-company in 2026 ZAR)
# hire: earliest month #; gate: last month's net subscription MRR (R) needed (x gate multiplier).
# Non-founder roles also wait for the seed month. link=(market, "lead"|"launch"|"exp") ties a
# role to that market's launch decision, launch month, or launch + 12 months.
# ---------------------------------------------------------------------------
def _ro(name, dept, count, ctc, hire=1, gate=0, typ="", link=None):
    return dict(name=name, dept=dept, count=count, ctc=ctc, hire=hire, gate=gate, type=typ, link=link)


EN, MK, SP, CS, GA, CT = ("Engineering & product", "Marketing", "Sales & partnerships", "Customer success",
                          "G&A & compliance", "Country teams")
ROLES = [
    _ro("Founder & CEO (reduced salary)", "Leadership", 1, 45000, 1, typ="F"),
    _ro("CTO / founding engineer (reduced salary)", "Leadership", 1, 55000, 1, typ="F"),
    _ro("Senior full-stack engineers", EN, 2, 70000, 5, 0),
    _ro("AI / ML engineer", EN, 1, 80000, 6, 0),
    _ro("Product designer (UX)", EN, 1, 50000, 8, 150000),
    _ro("Full-stack engineers", EN, 2, 55000, 12, 400000),
    _ro("DevOps / QA engineer", EN, 1, 60000, 15, 800000),
    _ro("Integrations engineers (social adapters, commerce, CRM)", EN, 2, 60000, 16, 1000000),
    _ro("Product manager", EN, 1, 70000, 20, 1500000),
    _ro("Security & compliance engineer", EN, 1, 80000, 24, 2500000),
    _ro("Payments & data engineers", EN, 2, 65000, 28, 3500000),
    _ro("Engineers (scale-up I)", EN, 3, 65000, 30, 5000000),
    _ro("VP Engineering", EN, 1, 110000, 36, 7000000),
    _ro("Product manager #2", EN, 1, 75000, 36, 8000000),
    _ro("Engineers (scale-up II)", EN, 4, 70000, 40, 10000000),
    _ro("Data / AI engineers", EN, 2, 85000, 44, 13000000),
    _ro("Engineers (scale-up III)", EN, 4, 75000, 50, 17000000),
    _ro("Engineers (scale-up IV: social adapters & integrations at scale)", EN, 5, 80000, 44, 14000000),
    _ro("Data & AI team II", EN, 3, 90000, 50, 19000000),
    _ro("Head of Growth", MK, 1, 70000, 5, 0),
    _ro("Performance marketer", MK, 1, 40000, 7, 100000),
    _ro("Multilingual content & community", MK, 2, 28000, 9, 300000),
    _ro("Lifecycle & growth marketers", MK, 2, 40000, 20, 1500000),
    _ro("Marketing team expansion I", MK, 3, 42000, 30, 5000000),
    _ro("Marketing team expansion II", MK, 3, 45000, 44, 12000000),
    _ro("Marketing team expansion III", MK, 4, 48000, 46, 15000000),
    _ro("Partnerships manager #1 (agency programme)", SP, 1, 50000, 5, 0, "PM"),
    _ro("Partnerships manager #2", SP, 1, 50000, 14, 800000, "PM"),
    _ro("Partnerships managers (scale-up I)", SP, 2, 50000, 27, 3500000, "PM"),
    _ro("Partnerships managers (scale-up II)", SP, 2, 55000, 38, 9000000, "PM"),
    _ro("SME onboarding & sales-assist", SP, 2, 30000, 12, 600000),
    _ro("Head of Sales & Partnerships", SP, 1, 95000, 30, 5000000),
    _ro("SME account managers", SP, 3, 45000, 40, 10000000),
    _ro("Partnerships managers (scale-up III)", SP, 2, 55000, 44, 14000000, "PM"),
    _ro("SME account managers II", SP, 4, 45000, 48, 16000000),
    _ro("Customer success lead", CS, 1, 40000, 5, 0),
    _ro("CS & onboarding agents", CS, 2, 20000, 8, 150000),
    _ro("CS agents II", CS, 4, 20000, 17, 1200000),
    _ro("CS agents III", CS, 6, 22000, 27, 3500000),
    _ro("CS agents IV", CS, 8, 22000, 39, 9000000),
    _ro("CS agents V", CS, 8, 24000, 50, 16000000),
    _ro("Finance & compliance manager", GA, 1, 55000, 8, 150000),
    _ro("Operations & admin", GA, 1, 22000, 12, 500000),
    _ro("Legal & data-protection counsel", GA, 1, 70000, 22, 2000000),
    _ro("People & HR partner", GA, 1, 45000, 28, 3500000),
    _ro("Finance analyst", GA, 1, 40000, 30, 5000000),
    _ro("CFO", GA, 1, 120000, 36, 8000000),
    _ro("CS agents VI", CS, 10, 24000, 48, 18000000),
    _ro("Finance, legal & people team expansion", GA, 3, 60000, 48, 16000000),
    _ro("Country lead: Nigeria", CT, 1, 60000, link=("NG", "lead")),
    _ro("Nigeria sales & CS", CT, 2, 18000, link=("NG", "launch")),
    _ro("Nigeria team expansion", CT, 3, 20000, link=("NG", "exp")),
    _ro("Country lead: Kenya", CT, 1, 55000, link=("KE", "lead")),
    _ro("Kenya sales & CS", CT, 1, 18000, link=("KE", "launch")),
    _ro("Kenya team expansion", CT, 2, 20000, link=("KE", "exp")),
    _ro("Country lead: Ghana", CT, 1, 45000, link=("GH", "lead")),
    _ro("Ghana sales & CS", CT, 2, 18000, link=("GH", "launch")),
    _ro("Ghana team expansion", CT, 2, 20000, link=("GH", "exp")),
]
for _i, _ro_ in enumerate(ROLES):
    _r = HC_FIRST_ROW + _i
    _ro_["row"] = _r
    ADDR[f"hc_ctc_{_i}"] = f"Assumptions!$B${_r}"
    ADDR[f"hc_count_{_i}"] = f"Assumptions!$D${_r}"
    ADDR[f"hc_hire_{_i}"] = f"Assumptions!$E${_r}"
    ADDR[f"hc_gate_{_i}"] = f"Assumptions!$F${_r}"


def AD(key):
    return ADDR[key]


def build_params(scen_idx=2, overrides=None):
    """Resolve every input for a scenario (1=Conservative, 2=Base, 3=Upside)."""
    overrides = overrides or {}
    p = {"scen_idx": scen_idx}
    for key, label, unit, val, note_, fmt in PRICING_SCALARS:
        if val is not None:
            p[key] = overrides.get(key, val)
    p["annual_factor"] = 1 - p["annual_share"] * (12 - p["annual_months"]) / 12
    for key, label, unit, val, note_, fmt in FX_ROWS:
        p[key] = overrides.get(key, val)
    for t in TIERS:
        p[f"price_{t}"] = PRICING[t][0]
        p[f"credits_{t}"] = PRICING[t][1]
    p["price_W"] = WHOLESALE[0]
    for e in ENTRIES:
        if e["kind"] == "inp":
            p[e["key"]] = overrides.get(e["key"], e["value"])
        elif e["kind"] == "scen":
            p[e["key"]] = overrides.get(e["key"], e["values"][scen_idx - 1])
        elif e["kind"] == "der":
            p[e["key"]] = e["py"](p)
    for r in MARKETS:
        for t in PRICE_KEYS:
            p[f"price_{r}_{t}"] = par_price_py(p, r, t)
    for i, ro in enumerate(ROLES):
        p[f"hc_ctc_{i}"] = overrides.get(f"hc_ctc_{i}", ro["ctc"])
        p[f"hc_count_{i}"] = overrides.get(f"hc_count_{i}", ro["count"])
        p[f"hc_hire_{i}"] = overrides.get(f"hc_hire_{i}", ro["hire"])
        p[f"hc_gate_{i}"] = overrides.get(f"hc_gate_{i}", ro["gate"])
    return p
