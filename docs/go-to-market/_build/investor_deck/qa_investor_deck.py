#!/usr/bin/env python3
"""QA for the FluxMuse investor pitch deck (no LibreOffice needed).

Same checks as the brand deck's qa_deck.py, plus a number trace:

1. python-pptx pass: slide count, speaker notes on every slide (80-150 words), forbidden claims,
   leftover template text, placeholders (only [[ ]]).
2. Geometry: off-slide shapes, edge margins, overlaps between unrelated groups, font sizes by role
   (body >= 14pt; appendix tables may go to 12pt).
3. Number trace: every "R..." or "...%" token in slide text is matched against model_summary.json,
   00_FACTS_AND_ASSUMPTIONS.md and Financial_Model_Notes.md. Untraced tokens are reported.
4. Visual: exports a layout JSON and renders every slide in headless Chrome with the real Poppins/Inter
   web fonts (preview_deck.mjs), measuring text overflow and table growth, then writes contact sheets.

    python qa_investor_deck.py [preview_dir]      # default: ./preview
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

from PIL import Image
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE
from pptx.util import Emu

HERE = Path(__file__).resolve().parent
GTM = HERE.parent.parent
DECKS = GTM / "04_Investor_Pitch_Deck"
EMU_IN = 914400

FORBIDDEN = [r"200\+", r"\b4\.9\b", r"snapscan", r"stitch", r"lifetime", r"for life", r"life of your account",
             r"40\s*[–-]\s*60\s*%", r"guarantee", r"flutterwave", r"payfast", r"m-pesa", r"R18\.5(?![0-9])", r"18,500,000",
             r"\b335\b", r"founding member[^.\n]{0,60}(R5,599|R3,999)", r"(R5,599|R3,999)[^.\n]{0,40}founding member"]
LEFTOVER = r"lorem|ipsum|\bTODO\b|\bx{3,}\b|\[insert|click to (add|edit)"
MIN_PT = {"body": 14, "card": 14, "chip": 14, "placeholder": 14, "table": 14, "title": 24, "eyebrow": 11,
          "caption": 10, "footer": 10, "slidenum": 10}
APPENDIX_TABLE_MIN = 12
NOTES_MIN, NOTES_MAX = 80, 150
WORD_ROLES = {"body", "card", "chip"}
WORD_LIMIT = 150  # investor slides carry more evidence than the brand deck

NUM_R = re.compile(r"[−-]?R\s?\d[\d,]*(?:\.\d+)?\s?(?:k|K|M|bn)?")
NUM_P = re.compile(r"[−-]?[<>~≈+]?\s?\d+(?:\.\d+)?\s?%")


# ---------------------------------------------------------------- allowed-number corpus
def walk(o, path=""):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from walk(v, f"{path}.{k}")
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from walk(v, f"{path}[{i}]")
    else:
        yield path, o


def parse_r(tok):
    t = tok.replace("−", "-").replace(" ", "")
    neg = t.startswith("-")
    t = t.lstrip("-").lstrip("R")
    mult = 1.0
    if t[-1:] in "kK":
        mult, t = 1e3, t[:-1]
    elif t[-1:] == "M":
        mult, t = 1e6, t[:-1]
    elif t[-2:] == "bn":
        mult, t = 1e9, t[:-2]
    t = t.replace(",", "")
    try:
        v = float(t)
    except ValueError:
        return None, None
    dec = len(t.split(".")[1]) if "." in t else 0
    tol = (0.5 * 10 ** -dec) * mult + 1e-6
    return (-v if neg else v) * mult, tol


def parse_p(tok):
    t = tok.replace("−", "-").replace(" ", "").rstrip("%")
    for ch in "<>~≈+":
        t = t.replace(ch, "")
    neg = t.startswith("-")
    t = t.lstrip("-")
    try:
        v = float(t)
    except ValueError:
        return None, None
    dec = len(t.split(".")[1]) if "." in t else 0
    return (-v if neg else v), 0.5 * 10 ** -dec + 1e-9


def build_corpus():
    """(rand values, percent values) known to the model / facts, each with the source that provided it."""
    rand, pcts = {}, {}

    def add(store, v, src):
        store.setdefault(round(float(v), 4), src)

    model = json.loads((GTM / "06_Financial_Model" / "model_summary.json").read_text())
    for path, v in walk(model):
        if isinstance(v, bool) or v is None:
            continue
        if isinstance(v, (int, float)):
            low = path.lower()
            if "zar" in low or "amount" in low or "monthly" in low or "bills" in low or "gate" in low or \
               "cost" in low or "cash" in low or "seed" in low or "price" in low or "mrr" in low or "ctc" in low:
                add(rand, v, f"model{path}")
                if "_m" in low.split(".")[-1][-3:] or low.endswith("_zar_m"):
                    add(rand, v * 1e6, f"model{path} (x1e6)")
            if low.endswith("_m") or "_zar_m" in low:
                add(rand, v * 1e6, f"model{path} (x1e6)")
            if "pct" in low or "margin" in low or "share" in low or "rate" in low or "uplift" in low:
                add(pcts, v, f"model{path}")
            if "cap_pct" in low or "mult" in low or path.endswith("commerce_fee"):
                add(pcts, v * 100, f"model{path} (x100)")
        if isinstance(v, str):
            for tok in NUM_R.findall(v):
                val, _ = parse_r(tok)
                if val is not None:
                    add(rand, val, f"model{path}: '{tok}'")
            for tok in NUM_P.findall(v):
                val, _ = parse_p(tok)
                if val is not None:
                    add(pcts, val, f"model{path}: '{tok}'")
    for name in ("00_FACTS_AND_ASSUMPTIONS.md", "06_Financial_Model/Financial_Model_Notes.md",
                 "07_Case_Studies/Gauteng_Pilot_Case_Studies.md"):
        txt = (GTM / name).read_text()
        for tok in NUM_R.findall(txt):
            val, _ = parse_r(tok)
            if val is not None:
                add(rand, val, f"{Path(name).name}: '{tok}'")
        for tok in NUM_P.findall(txt):
            val, _ = parse_p(tok)
            if val is not None:
                add(pcts, val, f"{Path(name).name}: '{tok}'")
    # derived values a slide may legitimately show: annual = 10x monthly, and stream sums
    for t, v in model["price_tables"]["zar_list_monthly"].items():
        add(rand, v * 10, f"model.price_tables.zar_list_monthly.{t} x10 (annual = 10x monthly)")
    add(rand, model["price_tables"]["partner_wholesale_monthly"]["ZAR"] * 10,
        "model.price_tables.partner_wholesale_monthly.ZAR x10 (annual = 10x monthly)")
    return rand, pcts


def trace(tok, corpus, parser):
    val, tol = parser(tok)
    if val is None:
        return None
    best = None
    for known, src in corpus.items():
        if abs(known - val) <= tol:
            if best is None or abs(known - val) < best[0]:
                best = (abs(known - val), src)
    return best[1] if best else False


# ---------------------------------------------------------------- pptx analysis
def inch(v):
    return round(Emu(v) / EMU_IN, 3)


def parse_name(name):
    parts = (name or "").split("|")
    return (parts + ["", "", ""])[:3] if len(parts) >= 2 else ("", "", name)


def shape_text_runs(shape):
    paras = []
    for p in shape.text_frame.paragraphs:
        runs = []
        for r in p.runs:
            f = r.font
            color = None
            try:
                color = str(f.color.rgb) if f.color and f.color.type is not None else None
            except Exception:
                pass
            rpr = r._r.find("{http://schemas.openxmlformats.org/drawingml/2006/main}rPr")
            runs.append({"text": r.text, "size": f.size.pt if f.size else 18, "bold": bool(f.bold),
                         "font": f.name or "Inter", "color": color,
                         "spc": int(rpr.get("spc")) / 100 if rpr is not None and rpr.get("spc") else 0})
        for fld in p._p.findall("{http://schemas.openxmlformats.org/drawingml/2006/main}fld"):
            if len(runs) >= len(p._p.findall("{http://schemas.openxmlformats.org/drawingml/2006/main}r")) + 1:
                continue
            runs.append({"text": "".join(fld.itertext()), "size": 10, "bold": False, "font": "Inter",
                         "color": None, "spc": 0})
        algn = p._p.pPr.get("algn") if p._p.pPr is not None else None
        paras.append({"runs": runs, "align": algn or "l",
                      "lsp": p.line_spacing if isinstance(p.line_spacing, float) else None,
                      "space_after": p.space_after.pt if p.space_after is not None else 0})
    return paras


def fill_hex(shape):
    try:
        if shape.fill.type == 1:
            return str(shape.fill.fore_color.rgb)
    except Exception:
        pass
    return None


def analyse(path: Path, pv_dir: Path, corpus):
    rand_c, pct_c = corpus
    prs = Presentation(path)
    W, H = inch(prs.slide_width), inch(prs.slide_height)
    issues, layout, placeholders = [], {"file": path.name, "w": W, "h": H, "slides": []}, set()
    traced, untraced = [], []
    img_dir = pv_dir / "img"
    img_dir.mkdir(parents=True, exist_ok=True)
    for idx, slide in enumerate(prs.slides, 1):
        where = f"s{idx}"
        note = slide.notes_slide.notes_text_frame.text if slide.has_notes_slide else ""
        nw = len(note.split())
        if nw == 0:
            issues.append((where, "notes", "missing speaker notes"))
        elif not NOTES_MIN <= nw <= NOTES_MAX:
            issues.append((where, "notes", f"notes {nw} words (target {NOTES_MIN}-{NOTES_MAX})"))
        bg = None
        try:
            bg = str(slide.background.fill.fore_color.rgb)
        except Exception:
            pass
        sl = {"n": idx, "bg": bg or "FFFFFF", "els": []}
        slide_text, boxes, body_words = [], [], 0
        is_appendix = False
        for shp in slide.shapes:
            if shp.has_text_frame:
                t = "".join(r["text"] for p in shape_text_runs(shp) for r in p["runs"])
                if parse_name(shp.name)[1] == "eyebrow" and t.upper().startswith("APPENDIX"):
                    is_appendix = True
        tmin = APPENDIX_TABLE_MIN if is_appendix else MIN_PT["table"]
        for shp in slide.shapes:
            grp, role, label = parse_name(shp.name)
            x, y, w, h = inch(shp.left), inch(shp.top), inch(shp.width), inch(shp.height)
            el = {"name": shp.name, "role": role, "x": x, "y": y, "w": w, "h": h}
            if shp.shape_type == MSO_SHAPE_TYPE.PICTURE:
                blob = shp.image.blob
                hsh = hashlib.sha1(blob).hexdigest()[:16]
                fp = img_dir / f"{hsh}.{shp.image.ext}"
                if not fp.exists():
                    fp.write_bytes(blob)
                geom = shp._element.find(".//{http://schemas.openxmlformats.org/drawingml/2006/main}prstGeom")
                el.update(type="pic", src=str(fp), crop=[shp.crop_left, shp.crop_top, shp.crop_right, shp.crop_bottom],
                          rounded=geom is not None and geom.get("prst") == "roundRect")
            elif shp.has_table if hasattr(shp, "has_table") else False:
                tbl = shp.table
                cols = [inch(c.width) for c in tbl.columns]
                rows = []
                for r in tbl.rows:
                    cells = []
                    for c in r.cells:
                        f = None
                        try:
                            f = str(c.fill.fore_color.rgb)
                        except Exception:
                            pass
                        paras = shape_text_runs(c)
                        cells.append({"paras": paras, "fill": f})
                        for p in paras:
                            for rr in p["runs"]:
                                slide_text.append(rr["text"])
                                if rr["size"] < tmin:
                                    issues.append((where, "font", f"table run {rr['size']}pt < {tmin}: "
                                                                  f"{rr['text'][:30]}"))
                    rows.append({"h": inch(r.height), "cells": cells})
                el.update(type="table", cols=cols, rows=rows)
                role = "table"
            elif shp.shape_type == MSO_SHAPE_TYPE.AUTO_SHAPE:
                prst = shp._element.find(".//{http://schemas.openxmlformats.org/drawingml/2006/main}prstGeom")
                adj = None
                try:
                    adj = shp.adjustments[0] if len(shp.adjustments) else None
                except Exception:
                    pass
                line = None
                try:
                    if shp.line.fill.type == 1:
                        line = {"color": str(shp.line.color.rgb), "w": shp.line.width.pt,
                                "dash": shp.line.dash_style is not None}
                except Exception:
                    pass
                el.update(type="shape", prst=prst.get("prst") if prst is not None else "rect", adj=adj,
                          fill=fill_hex(shp), line=line)
            if shp.has_text_frame and el.get("type") != "pic":
                paras = shape_text_runs(shp)
                txt = "".join(r["text"] for p in paras for r in p["runs"])
                if txt.strip():
                    anchor = shp.text_frame._txBody.bodyPr.get("anchor") or "t"
                    el.update(type="text" if el.get("type") != "shape" else "shape", paras=paras, anchor=anchor)
                    slide_text.append(txt)
                    placeholders.update(re.findall(r"\[\[[^\]]+\]\]", txt))
                    stripped = re.sub(r"\[\[[^\]]*\]\]", "", txt)
                    if re.search(r"(?<!\[)\[(?!\[)|(?<!\])\](?!\])", stripped):
                        issues.append((where, "placeholder", f"bare bracket in: {txt[:60]}"))
                    for p in paras:
                        for r in p["runs"]:
                            mn = MIN_PT.get(role)
                            if mn and r["size"] < mn and r["text"].strip():
                                issues.append((where, "font", f"{role} run {r['size']}pt < {mn}: {r['text'][:40]}"))
                    if role in WORD_ROLES:
                        body_words += len(txt.split())
            sl["els"].append(el)
            if x < -0.01 or y < -0.01 or x + w > W + 0.01 or y + h > H + 0.01:
                issues.append((where, "offslide", f"{shp.name} at ({x},{y},{w},{h})"))
            if role not in ("bg", "deco", "footer", "slidenum", "") and (x < 0.4 or x + w > W - 0.4 or y < 0.35 or
                                                                        y + h > H - 0.15):
                issues.append((where, "margin", f"{shp.name} near edge ({x},{y},{w},{h})"))
            if role not in ("bg", "deco"):
                boxes.append((grp, role, shp.name, x, y, w, h))
        for i in range(len(boxes)):
            for j in range(i + 1, len(boxes)):
                a, b = boxes[i], boxes[j]
                if a[0] and a[0] == b[0]:
                    continue

                def contains(o, i_):
                    return (o[1] == "card" and o[3] <= i_[3] + 0.01 and o[4] <= i_[4] + 0.01
                            and o[3] + o[5] >= i_[3] + i_[5] - 0.01 and o[4] + o[6] >= i_[4] + i_[6] - 0.01)

                if contains(a, b) or contains(b, a):
                    continue
                ix = min(a[3] + a[5], b[3] + b[5]) - max(a[3], b[3])
                iy = min(a[4] + a[6], b[4] + b[6]) - max(a[4], b[4])
                if ix > 0.02 and iy > 0.02:
                    issues.append((where, "overlap", f"{a[2]} x {b[2]} ({ix:.2f}x{iy:.2f} in)"))
        if body_words > WORD_LIMIT and not is_appendix:
            issues.append((where, "words", f"{body_words} body words (target <= {WORD_LIMIT})"))
        joined = "\n".join(slide_text + [note])
        for pat in FORBIDDEN:
            for m in re.finditer(pat, joined, flags=re.I):
                ctx = joined[max(0, m.start() - 40): m.end() + 40].replace("\n", " ")
                issues.append((where, "FORBIDDEN", f"'{m.group(0)}' in: ...{ctx}..."))
        if re.search(LEFTOVER, joined, flags=re.I):
            issues.append((where, "leftover", re.search(LEFTOVER, joined, flags=re.I).group(0)))
        # number trace (slide text only; notes are reported separately)
        body = "\n".join(slide_text)
        for tok in NUM_R.findall(body):
            src = trace(tok, rand_c, parse_r)
            (traced if src else untraced).append((where, tok, src))
        for tok in NUM_P.findall(body):
            src = trace(tok, pct_c, parse_p)
            (traced if src else untraced).append((where, tok, src))
        for tok in NUM_R.findall(note):
            if not trace(tok, rand_c, parse_r):
                issues.append((where, "notes-number", f"untraced in notes: {tok}"))
        for tok in NUM_P.findall(note):
            if not trace(tok, pct_c, parse_p):
                issues.append((where, "notes-number", f"untraced in notes: {tok}"))
        layout["slides"].append(sl)
    for where, tok, _ in untraced:
        issues.append((where, "NUMBER", f"untraced: {tok}"))
    return prs, issues, layout, placeholders, traced, untraced


def contact_sheets(png_dir: Path, prefix: str, per=6):
    pngs = sorted(png_dir.glob("slide-*.png"))
    sheets = []
    for k in range(0, len(pngs), per):
        chunk = pngs[k:k + per]
        tw, th = 800, 450
        rows = (len(chunk) + 1) // 2
        sheet = Image.new("RGB", (2 * tw + 30, rows * th + (rows + 1) * 10), (120, 120, 120))
        for i, p in enumerate(chunk):
            im = Image.open(p).convert("RGB").resize((tw, th))
            sheet.paste(im, (10 + (i % 2) * (tw + 10), 10 + (i // 2) * (th + 10)))
        out = png_dir.parent / f"{prefix}-sheet-{k // per + 1}.jpg"
        sheet.save(out, quality=85)
        sheets.append(out)
    return sheets


def main():
    pv_root = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "preview"
    pv_root.mkdir(parents=True, exist_ok=True)
    corpus = build_corpus()
    print(f"number corpus: {len(corpus[0])} rand values, {len(corpus[1])} percentages "
          "(model_summary.json + facts + model notes)")
    total = 0
    for path in sorted(DECKS.glob("*.pptx")):
        pv = pv_root / path.stem
        prs, issues, layout, ph, traced, untraced = analyse(path, pv, corpus)
        lj = pv / "layout.json"
        lj.write_text(json.dumps(layout))
        r = subprocess.run(["node", str(HERE / "preview_deck.mjs"), str(lj), str(pv / "png")], capture_output=True,
                           text=True, env=dict(os.environ))
        if r.returncode != 0:
            issues.append((path.name, "preview", r.stderr[-400:]))
        else:
            rep = json.loads((pv / "png" / "overflow.json").read_text())
            for item in rep:
                issues.append((f"s{item['slide']}", "overflow", item["msg"]))
            contact_sheets(pv / "png", path.stem)
        notes_ok = all(s.has_notes_slide and s.notes_slide.notes_text_frame.text.strip() for s in prs.slides)
        print(f"\n== {path.name}: {len(prs.slides)} slides, notes on every slide: {notes_ok}")
        print(f"   numbers on slides: {len(traced)} traced, {len(untraced)} untraced")
        for w, kind, msg in sorted(issues, key=lambda i: (int(i[0][1:]) if i[0][1:].isdigit() else 0, i[1])):
            print(f"  [{kind}] {w}: {msg}")
        if "-v" in sys.argv:
            print("\n   number trace:")
            for w, tok, src in traced:
                print(f"     {w:5} {tok:>12}  <- {src}")
        print("\n   Placeholders:", ", ".join(sorted(ph)))
        total += len(issues)
    print(f"\nTotal findings: {total}")


if __name__ == "__main__":
    main()
