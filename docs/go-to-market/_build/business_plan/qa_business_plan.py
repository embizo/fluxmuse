"""QA for the business plan: structure, TOC, images, tables, placeholders, forbidden claims, number trace.

    venv/bin/python docs/go-to-market/_build/business_plan/qa_business_plan.py
Exit code 1 if any check fails.
"""
import json
import re
import sys
import zipfile
from pathlib import Path

from docx import Document

HERE = Path(__file__).resolve().parent
GTM = HERE.parent.parent
OUT = GTM / "05_Business_Plan"
DOCX = OUT / "FluxMuse_Business_Plan.docx"
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"

FORBIDDEN = [r"200\+", r"(?<![\d.])4\.9(?!\d)\s*(?:star|rating|/5)?", r"SnapScan", r"Stitch", r"\blifetime\b(?!\s+value)", r"for life",
             r"life of (your|the) account", r"40\s*[–-]\s*60\s*%", r"guarantee", r"Flutterwave",
             r"PayFast", r"M-Pesa", r"R18\.5M", r"18,500,000", r"R335\b",
             r"R5,599[^.]{0,40}(first 2|2 months)"]
INTERNAL_ONLY = ["home-hero.png", "home_mobile.png", "home-full.png", "for-agencies", "features-hero",
                 "features-full", "pricing-za-full", "pricing-ng", "pricing-ke", "demo-step-04",
                 "demo-step-05", "demo.png", "demo-full", "browser-demo", "laptop-demo"]

# Figures that may legitimately appear in text, with where they come from.
M = json.loads((GTM / "06_Financial_Model" / "model_summary.json").read_text())
D = json.loads((HERE / "derived_tables.json").read_text())
FACTS = (GTM / "00_FACTS_AND_ASSUMPTIONS.md").read_text()
NOTES = (GTM / "06_Financial_Model" / "Financial_Model_Notes.md").read_text()
CASE = (GTM / "07_Case_Studies" / "Gauteng_Pilot_Case_Studies.md").read_text()


def all_text(doc):
    parts = [t.text or "" for t in doc.element.body.iter(W + "t")]
    for s in doc.sections:
        for hf in (s.header, s.footer, s.first_page_footer):
            parts += [t.text or "" for t in hf._element.iter(W + "t")]
    return " ".join(parts)


def model_number_strings():
    """Every number the model/facts files can justify, as formatted strings."""
    ok = set()

    def add(*vals):
        for v in vals:
            ok.add(str(v))

    def add_money(x):
        x = float(x)
        add(f"{round(x):,}", f"{abs(round(x)):,}", f"{x / 1e6:,.0f}", f"{x / 1e6:,.1f}", f"{x / 1e6:,.2f}",
            f"{abs(x) / 1e6:,.1f}", f"{abs(x) / 1e6:,.2f}", f"{round(x / 1000):,}",
            f"{abs(round(x / 1000)):,}", f"{round(abs(x)):,}",
            f"{x / 1e9:,.1f}", f"{x / 1e9:,.2f}", f"{abs(x) / 1e9:,.1f}")

    def walk(o):
        if isinstance(o, dict):
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
        elif isinstance(o, (int, float)):
            add_money(o)
            add(f"{o:,}", f"{round(o):,}", f"{o:.1f}", f"{o:.2f}", f"{abs(o):.1f}", f"{abs(o):.2f}",
                f"{round(o)}", f"{o}")
        elif isinstance(o, str):
            for m in re.finditer(r"[\d][\d,.]*", o):
                add(m.group(0))
    walk(M)
    walk(D)
    # numbers stated in the facts, notes and case-study files
    for text in (FACTS, NOTES, CASE):
        for m in re.finditer(r"[\d][\d,.]*", text):
            add(m.group(0))
    # derived percentages and ratios the document computes from model values
    for a in M["annual"]:
        add_money(a["revenue_by_stream_zar"]["enterprise_setup_fees"]
                  + a["revenue_by_stream_zar"]["agency_setup_fees"])
    for dr, ar in zip(D["cash_flow_rows_fy_sum"]["d_dr"], D["cash_flow_rows_fy_sum"]["d_ar"]):
        add_money(dr - ar)
    return ok


NUM_RE = re.compile(r"(?:R|US\$|\$|₦|KSh\s?|GH₵\s?)\s?([\d][\d,]*(?:\.\d+)?)\s?(m|k|bn|billion|million)?"
                    r"|([\d][\d,]*(?:\.\d+)?)\s?%")


def number_trace(text):
    """Every currency/percentage figure in the document must be justifiable from the sources."""
    ok = model_number_strings()
    # page furniture, years, small counts and prose numbers that are not financial claims
    allow = {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "14", "15", "16", "18",
             "19", "20", "23", "25", "30", "35", "40", "45", "50", "60", "65", "70", "75", "80", "85", "90",
             "100", "0.5", "1.5", "2.5", "3.0", "3.5", "4.0", "0.75", "27", "28", "21", "22", "29", "31",
             "33", "36", "39", "44", "48", "68", "92", "135", "499", "999", "249", "349", "1,399", "3,499",
             "2,499", "3,999", "1,999", "4,999", "5,599", "7,999", "19,999", "1,500", "30,000", "24,401",
             "150,000", "500,000", "25,000", "2,200", "6,500"}
    bad = []
    for m in NUM_RE.finditer(text):
        val = m.group(1) or m.group(3)
        if val is None:
            continue
        v = val.rstrip(".,")
        if v in allow or v in ok:
            continue
        # try without thousands separators and with common roundings
        alt = {v.replace(",", ""), v.rstrip("0").rstrip("."), v + "0"}
        if alt & ok:
            continue
        bad.append(m.group(0).strip())
    return sorted(set(bad))


def check():
    errs, info = [], {}
    doc = Document(DOCX)
    heads = [(p.style.name, p.text) for p in doc.paragraphs if p.style.name.startswith("Heading")]
    info["h1"] = sum(1 for s, _ in heads if s == "Heading 1")
    info["h2"] = sum(1 for s, _ in heads if s == "Heading 2")
    info["h3"] = sum(1 for s, _ in heads if s == "Heading 3")
    if info["h1"] < 20:
        errs.append(f"expected 16 sections + 6 appendices + document control, got {info['h1']} H1s")
    seen_h1 = False
    for s, t in heads:
        if s == "Heading 1":
            seen_h1 = True
        elif not seen_h1:
            errs.append(f"{s} before any Heading 1: {t}")

    # TOC field present
    body_xml = doc.element.body.xml
    if "TOC \\o" not in body_xml:
        errs.append("no TOC field")
    if "updateFields" not in doc.settings.element.xml:
        errs.append("updateFields not set (Word will not fill the TOC)")
    text = all_text(doc)
    if "Contents (static fallback)" not in text:
        errs.append("no static contents fallback")

    # images
    with zipfile.ZipFile(DOCX) as z:
        info["media_files"] = len([n for n in z.namelist() if n.startswith("word/media/")])
    blips = list(doc.element.body.iter("{http://schemas.openxmlformats.org/drawingml/2006/main}blip"))
    info["body_images"] = len(blips)
    if len(blips) < 20:
        errs.append(f"expected 20+ body images, got {len(blips)}")
    missing_alt = [dp for dp in doc.element.body.iter(
        "{http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing}docPr")
        if not dp.get("descr")]
    if missing_alt:
        errs.append(f"{len(missing_alt)} images without alt text")

    # tables: repeating header row, keep-with-next on header, orange fill, Ink text
    data_tables = layout_tables = 0
    for tbl in doc.element.body.iter(W + "tbl"):
        cap = tbl.find(W + "tblPr/" + W + "tblCaption")
        capv = cap.get(W + "val") if cap is not None else ""
        if capv.startswith("Layout:"):
            layout_tables += 1
            continue
        data_tables += 1
        first = tbl.find(W + "tr")
        if first is None or first.find(W + "trPr/" + W + "tblHeader") is None:
            errs.append(f"data table without repeating header row: {capv}")
        fills = {s.get(W + "fill") for s in first.iter(W + "shd")}
        if "FF6A00" not in fills:
            errs.append(f"header row not Flux Orange: {capv}")
        if not any(k.find(W + "keepNext") is not None for k in first.iter(W + "pPr")):
            errs.append(f"header row without keep-with-next: {capv}")
        for c in first.iter(W + "color"):
            if c.get(W + "val", "").upper() in ("FFFFFF", "FFF"):
                errs.append(f"white text on orange header: {capv}")
    info["data_tables"], info["layout_tables"] = data_tables, layout_tables
    for tc in doc.element.body.iter(W + "tc"):
        s = tc.find(W + "tcPr/" + W + "shd")
        if s is not None and s.get(W + "fill") in ("FF6A00", "FFB27A"):
            for c in tc.iter(W + "color"):
                if c.get(W + "val", "").upper() == "FFFFFF":
                    errs.append("white text in an orange cell")

    # placeholders bold + shaded
    total = unhl = 0
    roots = [doc.element.body] + [hf._element for s in doc.sections
                                  for hf in (s.header, s.footer, s.first_page_footer)]
    for root in roots:
        for r in root.iter(W + "r"):
            t = "".join((x.text or "") for x in r.iter(W + "t"))
            if re.search(r"\[\[[^\[\]]*\]\]", t):
                total += 1
                rpr = r.find(W + "rPr")
                if not (rpr is not None and rpr.find(W + "shd") is not None and rpr.find(W + "b") is not None):
                    unhl += 1
    info["placeholder_runs"] = total
    if unhl:
        errs.append(f"{unhl} placeholder runs not bold+shaded")
    if text.count("[[") != text.count("]]"):
        errs.append("unbalanced [[ ]] brackets")

    # forbidden claims
    for pat in FORBIDDEN:
        for m in re.finditer(pat, text, flags=re.I):
            errs.append(f"forbidden /{pat}/: …{text[max(0, m.start() - 60):m.end() + 60]}…")
    if re.search(r"\bresults?\b[^.]{0,30}\b(achieved|delivered)\b", text, re.I):
        errs.append("possible results claim")

    # required disclosures
    for needed in ["forward-looking", "Meta App Review", "est.", "Target (goal)", "illustrative",
                   "Financial Model v2"]:
        if needed.lower() not in text.lower():
            errs.append(f"missing required wording: {needed}")

    # footer / header
    if "Business plan" not in text or "Page" not in text:
        errs.append("footer text missing")

    # page setup
    s = doc.sections[0]
    info["page_cm"] = (round(s.page_width.cm, 1), round(s.page_height.cm, 1))
    if info["page_cm"] != (21.0, 29.7):
        errs.append("not A4")

    # internal-only images
    mf = HERE / "build_manifest.json"
    if mf.exists():
        for img in json.loads(mf.read_text()).get("images", []):
            if any(k in img for k in INTERNAL_ONLY):
                errs.append(f"internal-only image used: {img}")

    # number trace
    untraced = number_trace(text)
    info["untraced_numbers"] = untraced
    if untraced:
        errs.append(f"{len(untraced)} figures not traced to the model/facts: {untraced}")

    info["words"] = len(text.split())
    return errs, info


def check_md(path):
    errs = []
    text = path.read_text()
    for pat in FORBIDDEN:
        for m in re.finditer(pat, text, flags=re.I):
            ctx = text[max(0, m.start() - 60):m.end() + 60].replace("\n", " ")
            if path.name == "README.md" and re.search(r"(never|don't|do not|no |not )", ctx, re.I):
                continue
            errs.append(f"forbidden /{pat}/: …{ctx}…")
    untraced = number_trace(text)
    if untraced:
        errs.append(f"figures not traced: {untraced}")
    return errs


def main():
    failed = False
    errs, info = check()
    print(f"== {DOCX.name}")
    for k, v in info.items():
        print(f"   {k}: {v}")
    for e in errs:
        print("   FAIL:", e)
    print("   OK" if not errs else "   FAILED")
    failed |= bool(errs)
    for p in sorted(OUT.glob("*.md")):
        e = check_md(p)
        print(f"\n== {p.name}: {'OK' if not e else 'FAILED'}")
        for x in e:
            print("   FAIL:", x)
        failed |= bool(e)
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
