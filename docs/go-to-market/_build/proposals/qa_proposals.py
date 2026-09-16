"""QA for the proposal templates: structure, images, table headers, placeholder highlighting, forbidden claims.

    python docs/go-to-market/_build/proposals/qa_proposals.py
Exit code 1 if any check fails.
"""
import re
import sys
import zipfile
from pathlib import Path

from docx import Document
from docx.oxml.ns import qn

HERE = Path(__file__).resolve().parent
OUT = HERE.parent.parent / "03_Proposal_Templates"
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"

FORBIDDEN = [r"200\+", r"4\.9", r"SnapScan", r"Stitch", r"lifetime", r"for life", r"life of (your|the) account",
             r"40\s*[–-]\s*60\s*%", r"guarantee", r"Flutterwave", r"PayFast", r"M-Pesa", r"R5,599[^.]{0,40}(first 2|2 months)"]
INTERNAL_ONLY = ["home-hero.png", "home_mobile.png", "home-full.png", "for-agencies", "features-hero", "features-full",
                 "pricing-za-full", "pricing-ng", "pricing-ke", "demo-step-04", "demo-step-05", "demo.png", "demo-full",
                 "browser-demo", "laptop-demo"]


def all_text(doc):
    parts = []
    body = doc.element.body
    for t in body.iter(W + "t"):
        parts.append(t.text or "")
    for s in doc.sections:
        for hf in (s.header, s.footer, s.first_page_footer):
            for t in hf._element.iter(W + "t"):
                parts.append(t.text or "")
    return " ".join(parts)


def check(path, manifest_imgs=None):
    errs, info = [], {}
    doc = Document(path)
    # headings
    heads = [(p.style.name, p.text) for p in doc.paragraphs if p.style.name.startswith("Heading")]
    info["h1"] = sum(1 for s, _ in heads if s == "Heading 1")
    info["h2"] = sum(1 for s, _ in heads if s == "Heading 2")
    if info["h1"] < 5:
        errs.append("too few Heading 1 sections")
    # heading order: no H3 without an H2 before it since last H1, no H2 before first H1
    seen_h1 = False
    for s, t in heads:
        if s == "Heading 1":
            seen_h1 = True
        elif not seen_h1:
            errs.append(f"{s} before any Heading 1: {t}")
    # images
    with zipfile.ZipFile(path) as z:
        media = [n for n in z.namelist() if n.startswith("word/media/")]
    info["media_files"] = len(media)
    blips = list(doc.element.body.iter("{http://schemas.openxmlformats.org/drawingml/2006/main}blip"))
    info["body_images"] = len(blips)
    missing_alt = [dp for dp in doc.element.body.iter("{http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing}docPr")
                   if not dp.get("descr")]
    if missing_alt:
        errs.append(f"{len(missing_alt)} images without alt text")
    if len(blips) < 3:
        errs.append("fewer than 3 body images")
    # tables
    data_tables = layout_tables = 0
    for tbl in doc.element.body.iter(W + "tbl"):
        cap = tbl.find(W + "tblPr/" + W + "tblCaption")
        capv = cap.get(W + "val") if cap is not None else ""
        if capv.startswith("Layout:"):
            layout_tables += 1
            continue
        data_tables += 1
        first = tbl.find(W + "tr")
        hdr = first.find(W + "trPr/" + W + "tblHeader") if first is not None else None
        if hdr is None:
            errs.append(f"data table without repeating header row: {capv}")
        fills = {s.get(W + "fill") for s in first.iter(W + "shd")}
        if "FF6A00" not in fills:
            errs.append(f"header row not Flux Orange: {capv}")
        # header text must be Ink, never white
        for c in first.iter(W + "color"):
            if c.get(W + "val", "").upper() in ("FFFFFF", "FFF"):
                errs.append(f"white text on orange header: {capv}")
    info["data_tables"], info["layout_tables"] = data_tables, layout_tables
    # white text anywhere on orange cells
    for tc in doc.element.body.iter(W + "tc"):
        s = tc.find(W + "tcPr/" + W + "shd")
        if s is not None and s.get(W + "fill") in ("FF6A00", "FFB27A"):
            for c in tc.iter(W + "color"):
                if c.get(W + "val", "").upper() == "FFFFFF":
                    errs.append("white text in an orange cell")
    # placeholders highlighted
    total = unhl = 0
    roots = [doc.element.body] + [hf._element for s in doc.sections for hf in (s.header, s.footer, s.first_page_footer)]
    for root in roots:
        for r in root.iter(W + "r"):
            t = "".join((x.text or "") for x in r.iter(W + "t"))
            if re.search(r"\[\[[^\[\]]*\]\]", t):
                total += 1
                rpr = r.find(W + "rPr")
                ok = rpr is not None and rpr.find(W + "shd") is not None and rpr.find(W + "b") is not None
                if not ok:
                    unhl += 1
    info["placeholder_runs"] = total
    if unhl:
        errs.append(f"{unhl} placeholder runs not bold+shaded")
    # text checks
    text = all_text(doc)
    for pat in FORBIDDEN:
        for m in re.finditer(pat, text, flags=re.I):
            errs.append(f"forbidden claim /{pat}/: …{text[max(0, m.start() - 40): m.end() + 40]}…")
    if re.search(r"\bresults?\b[^.]{0,30}\b(achieved|delivered)\b", text, re.I):
        errs.append("possible results claim")
    if "Page" not in text or "Confidential proposal for" not in text:
        errs.append("footer text missing")
    # KPI target columns labelled
    if "Target (goal)" not in text:
        errs.append("no 'Target (goal)' label")
    # sections/page setup
    s = doc.sections[0]
    info["page_cm"] = (round(s.page_width.cm, 1), round(s.page_height.cm, 1))
    if info["page_cm"] != (21.0, 29.7):
        errs.append("not A4")
    # internal-only screenshots
    if manifest_imgs:
        for img in manifest_imgs:
            if any(k in img for k in INTERNAL_ONLY):
                errs.append(f"internal-only image used: {img}")
    # unbalanced placeholder brackets
    bal = text.replace("“[[”", "")  # the how-to box tells users to search for “[[”
    if bal.count("[[") != bal.count("]]"):
        errs.append("unbalanced [[ ]] brackets")
    info["words"] = len(text.split())
    return errs, info


def check_md(path):
    errs = []
    text = path.read_text()
    for pat in FORBIDDEN:
        for m in re.finditer(pat, text, flags=re.I):
            ctx = text[max(0, m.start() - 60): m.end() + 60].replace("\n", " ")
            # the README may name forbidden terms inside its rules list
            if path.name == "README.md" and re.search(r"(never|don't|do not|no |not )", ctx, re.I):
                continue
            errs.append(f"forbidden /{pat}/: …{ctx}…")
    return errs


def main():
    import json
    manifest = {}
    mf = HERE / "build_manifest.json"
    if mf.exists():
        manifest = json.loads(mf.read_text()).get("files", {})
    failed = False
    for p in sorted(OUT.glob("*.docx")):
        errs, info = check(p, manifest.get(p.name))
        print(f"\n== {p.name}\n   {info}")
        for e in errs:
            print("   FAIL:", e)
        failed |= bool(errs)
        if not errs:
            print("   OK")
    for p in sorted(OUT.glob("*.md")):
        errs = check_md(p)
        print(f"\n== {p.name}: {'OK' if not errs else ''}")
        for e in errs:
            print("   FAIL:", e)
        failed |= bool(errs)
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
