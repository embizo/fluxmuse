# FluxMuse business plan

| File | What it is |
|---|---|
| `FluxMuse_Business_Plan.docx` | The full business plan (~40 pages): 16 sections plus appendices A–F |
| `Business_Plan_Summary.md` | Two-page executive summary in Markdown, for email or a data room |
| `README.md` | This file |

Audience: angels, VCs, banks and development-finance institutions (SEFA, IDC, NEF, TIA and similar),
supporting a **R25M seed raise**.

Every figure traces to `../06_Financial_Model/model_summary.json` (Financial Model v2, Base case),
the model's Python mirror, or `../00_FACTS_AND_ASSUMPTIONS.md`. Nothing is typed by hand, and the QA
script fails the build if a figure cannot be traced.

---

## 1. Placeholders to fill

Every `[[PLACEHOLDER]]` is **bold on yellow** in Word. Use Find for `[[` to walk them. There are 114
placeholder runs. The important groups:

**Company and legal (section 2)** — registration number, founding date, registered and operating
address, directors, cap table, B-BBEE level, tax and VAT numbers, auditor, banker, trade mark status,
Information Officer, data-protection registrations for Nigeria, Kenya and Ghana.

**People (sections 1 and 11)** — founder and CTO names, titles and backgrounds; the rest of the team;
advisors; board composition and investor rights; signing authority and financial controls;
key-person cover.

**The raise (section 13)** — instrument (SAFE or priced equity), pre-money valuation, how the
**R57.5k pre-seed bridge** is covered, exit considerations.

**Impact, for DFI readers (section 16)** — B-BBEE level and ownership, employment equity, skills
development, and the measurement plan for women-owned, youth-owned and township or rural reach.
These are written as *measurement commitments*, not claims. Do not replace them with estimates.

**Model confirmations (Appendix E)** — the 13 founder confirmations, opening cash, seed close month,
pilot conversion, Founding Member uplift and perks duration, FX assumptions, referral commission.

**Operational** — settlement terms per rail, security policy and penetration test, hosting regions,
pilot name, and confirmation that Fincra can collect subscriptions in South Sudan and Zimbabwe.

## 2. Remove before sending

1. **Appendix E** is marked *internal*. It carries a yellow banner saying so. Either delete the
   appendix or delete its open-confirmations table before the plan goes to an investor or funder.
2. **Placeholder shading.** Once a field is filled, clear the yellow (Home › Shading › No Colour),
   then search `[[` once more to be sure none are left.
3. **Section 2's note** telling the founder which fields to complete.
4. Update the TOC (right-click › Update Field) and check the page count before exporting a PDF.

## 3. House rules this document follows

- **No customer results, counts, ratings or testimonials.** The pilot runs to 30 November 2026;
  results exist from December 2026 with consent. Targets are labelled "Target (goal)".
- **Nothing in Meta App Review is described as live** — Instagram publishing, comments and DMs,
  Pages posting and business management are listed as pending.
- **Market figures are labelled "est." with a source** and must be re-verified before external use.
- **No competitor prices and no unverifiable competitor claims**; section 7 compares categories.
- **Partner economics are labelled illustrative**, and no fixed partner margin percentage is quoted.
- **No prices or checkout for gated countries**; Botswana and Namibia are "coming soon".
- The partner price of R5,599/mo is a permanent wholesale price, never a launch discount.

## 4. Rebuilding after the model changes

The financial model is the source of truth. If it changes, rebuild in this order:

```bash
cd <repo root>
V=<venv>/bin/python                      # python-docx + Pillow + openpyxl

# 1. Rebuild the model itself (regenerates model_summary.json and all chart PNGs)
$V docs/go-to-market/_build/financial_model.py

# 2. Re-derive the detail tables (headcount by department, COGS, cash flow, hiring plan)
$V docs/go-to-market/_build/business_plan/derive_model_tables.py

# 3. Rebuild the document
$V docs/go-to-market/_build/business_plan/build_business_plan.py

# 4. QA: structure, TOC, images, tables, placeholders, forbidden claims, number trace
$V docs/go-to-market/_build/business_plan/qa_business_plan.py
```

Step 2 prints `mismatches vs model_summary.json: []`. If that list is ever non-empty, the mirror and
the published JSON disagree — stop and fix the model before rebuilding the document.

Step 4 exits non-zero on failure. Its **number trace** extracts every R, ₦, KSh, GH₵, $ and %
figure in the document and checks it against the model, the derived tables and the facts file; any
figure it cannot justify is listed and fails the build.

Optional preview (no Word or LibreOffice needed; approximate page count, launches and closes its own
headless Chrome):

```bash
$V docs/go-to-market/_build/business_plan/preview_proposals.py html /tmp/bp-preview
CDP_UDD=/tmp/chrome-profile node docs/go-to-market/_build/business_plan/preview_proposals.mjs /tmp/bp-preview
$V docs/go-to-market/_build/business_plan/preview_proposals.py png /tmp/bp-preview
```

## 5. Build files

In `../_build/business_plan/`: `bp_doc.py` (document class, house style, shared data), `bp_s1.py` to
`bp_s5.py` (the sections), `build_business_plan.py` (assembles and saves),
`derive_model_tables.py` (imports the model mirror, writes `derived_tables.json`),
`qa_business_plan.py`, `fmdoc.py` (house style, copied from the proposal kit) and the preview
scripts. `build_manifest.json` records the images, figures and tables in the last build.

## 6. Resolved: roadmap infographic now matches the model

`../assets/infographics/roadmap-2026-2027.png` used to place the Nigeria, Kenya and Ghana launches in
"2027", against Financial Model v2's **February, April and June 2028** (gated on MRR). It was rebuilt
on 2026-09-12 (v4): the horizon runs to 2028, 2027 reads "Scale South Africa, no new market launches",
and the 2028 column carries Nigeria Feb, Kenya Apr, Ghana Jun and Rest of rail-covered Africa Nov 2028,
with a footnote that launch months are milestone-gated and move with actual revenue. The brand decks
and brand kit were rebuilt with it. The business plan still uses its own milestone table (section 15),
which is equivalent; the infographic is now safe to use in any deck or plan.
