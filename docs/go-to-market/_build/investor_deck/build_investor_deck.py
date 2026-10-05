#!/usr/bin/env python3
"""Build the FluxMuse investor pitch deck (seed size read from model_summary.json).

House style, primitives and icons are copied from ../brand_deck/build_deck.py so both decks read as one
family. Every financial number is read from 06_Financial_Model/model_summary.json at build
time; product, pricing and market facts come from 00_FACTS_AND_ASSUMPTIONS.md and
08_Prospects/CURRENT_OFFER.md. Charts and infographics
are embedded from docs/go-to-market/assets/.

    python build_investor_deck.py     # needs python-pptx + Pillow + lxml
    python qa_investor_deck.py        # structural QA, number trace, previews

Shape names follow "group|role|label" (roles: bg, deco, title, eyebrow, body, card, chip, caption, footer,
slidenum, img, icon, table, placeholder) so the QA script can check sizes and overlaps by role.
"""
from __future__ import annotations

import json
import math
import re
import sys
from datetime import date
from pathlib import Path

from lxml import etree
from PIL import Image
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.dml import MSO_LINE_DASH_STYLE
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, MSO_AUTO_SIZE, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Inches, Pt

HERE = Path(__file__).resolve().parent
GTM = HERE.parent.parent  # docs/go-to-market
ASSETS = GTM / "assets"
ICONS = HERE / "icons"
OUT = GTM / "04_Investor_Pitch_Deck"
DECK = OUT / "FluxMuse_Investor_Pitch_Deck.pptx"
M = json.loads((GTM / "06_Financial_Model" / "model_summary.json").read_text())
sys.path.insert(0, str(HERE.parent))
import fm_inputs  # noqa: E402  (hiring plan: role, count, earliest month, MRR gate)

# ---------------------------------------------------------------- brand tokens (same as brand deck)
ORANGE, GLOW, TINT = "FF6A00", "FF8533", "FFF4EB"
DEEP = "C24E00"
SLATE, INK, NIGHT, PAPER, MIST = "37474F", "20242B", "0F1419", "FFFFFF", "F3F4F6"
NIGHT_CARD = "1B232C"
MUTED = "5B6670"
MUTED_DARK = "A7B0B8"
LINE = "E3E6EA"
HEAD, BODY = "Poppins", "Inter"

SW, SH = 13.333, 7.5
MX = 0.6
CW = SW - 2 * MX
PROJ = f"Projection (model {M['version']}, base case)"

_gid = [0]


def gid(prefix="g"):
    _gid[0] += 1
    return f"{prefix}{_gid[0]}"


# ---------------------------------------------------------------- number formatting (from JSON only)
MINUS = "−"


def rm(v, d=1):
    """Rand millions: 237982700 -> R238.0M; negatives -> −R7.1M."""
    s = f"R{abs(v) / 1e6:,.{d}f}M"
    return (MINUS + s) if v < 0 else s


def rk(v, d=1):
    s = f"R{abs(v) / 1e3:,.{d}f}k"
    return (MINUS + s) if v < 0 else s


def rn(v):
    return f"R{v:,.0f}"


def pct(v, d=0):
    s = f"{abs(v):.{d}f}%"
    return (MINUS + s) if v < 0 else s


def num(v):
    return f"{round(v):,}"


A = M["annual"]
BASE, CONS, UP = M["scenarios"]["Base"], M["scenarios"]["Conservative"], M["scenarios"]["Upside"]
CASH = M["cash"]
UE = M["unit_economics_fy3"]
UOF = M["use_of_funds"]
REC24 = UOF["reconciliation"]["24"]
FX = M["fx_shock"]["results"]
LAUNCH = M["markets"]["launch_months"]["Base"]
GATES = M["markets"]["launch_mrr_gate_zar"]
PT = M["price_tables"]


# ---------------------------------------------------------------- primitives (copied from brand deck)
def rgb(h):
    return RGBColor.from_string(h)


def set_bg(slide, colour):
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = rgb(colour)


def text(slide, x, y, w, h, paras, *, size=16, font=BODY, color=INK, bold=False, align="l",
         anchor="t", role="body", group=None, label="", lsp=None, spc=None, space_after=0):
    shp = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    shp.name = f"{group or gid()}|{role}|{label}"
    tf = shp.text_frame
    tf.word_wrap = True
    tf.auto_size = MSO_AUTO_SIZE.NONE
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = {"t": MSO_ANCHOR.TOP, "m": MSO_ANCHOR.MIDDLE, "b": MSO_ANCHOR.BOTTOM}[anchor]
    if isinstance(paras, str):
        paras = [paras]
    for i, para in enumerate(paras):
        popts = {}
        if isinstance(para, dict):
            popts = para
            runs = para["runs"]
        else:
            runs = para
        if isinstance(runs, str):
            runs = [(runs, {})]
        runs = [(r, {}) if isinstance(r, str) else r for r in runs]
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = {"l": PP_ALIGN.LEFT, "c": PP_ALIGN.CENTER, "r": PP_ALIGN.RIGHT}[popts.get("align", align)]
        if popts.get("lsp", lsp):
            p.line_spacing = popts.get("lsp", lsp)
        sa = popts.get("space_after", space_after)
        if sa:
            p.space_after = Pt(sa)
        for t, o in runs:
            r = p.add_run()
            r.text = t
            f = r.font
            f.size = Pt(o.get("size", popts.get("size", size)))
            f.name = o.get("font", popts.get("font", font))
            f.bold = o.get("bold", popts.get("bold", bold))
            f.color.rgb = rgb(o.get("color", popts.get("color", color)))
            s = o.get("spc", spc)
            if s:
                r._r.get_or_add_rPr().set("spc", str(s))
    return shp


def box(slide, x, y, w, h, *, fill=None, line=None, lw=1.0, shape="rect", radius=0.14, dash=False,
        role="card", group=None, label=""):
    st = {"rect": MSO_SHAPE.RECTANGLE, "round": MSO_SHAPE.ROUNDED_RECTANGLE, "oval": MSO_SHAPE.OVAL,
          "down": MSO_SHAPE.DOWN_ARROW, "right": MSO_SHAPE.RIGHT_ARROW}[shape]
    s = slide.shapes.add_shape(st, Inches(x), Inches(y), Inches(w), Inches(h))
    s.name = f"{group or gid()}|{role}|{label}"
    if shape == "round":
        s.adjustments[0] = min(0.5, radius / min(w, h))
    if fill:
        s.fill.solid()
        s.fill.fore_color.rgb = rgb(fill)
    else:
        s.fill.background()
    if line:
        s.line.color.rgb = rgb(line)
        s.line.width = Pt(lw)
        if dash:
            s.line.dash_style = MSO_LINE_DASH_STYLE.DASH
    else:
        s.line.fill.background()
    s.shadow.inherit = False
    return s


USED = set()


def pic(slide, rel, x, y, w, h, *, crop=(0, 0, 0, 0), align="c", alt="", group=None, role="img", base=ASSETS):
    path = base / rel
    W, H = Image.open(path).size
    l, t, r, b = crop
    cw, ch = W * (1 - l - r), H * (1 - t - b)
    sc = min(w / cw, h / ch)
    pw, ph = cw * sc, ch * sc
    px = x if "l" in align else x + (w - pw) / 2
    py = y if "t" in align else y + (h - ph) / 2
    p = slide.shapes.add_picture(str(path), Inches(px), Inches(py), Inches(pw), Inches(ph))
    p.crop_left, p.crop_top, p.crop_right, p.crop_bottom = l, t, r, b
    p.name = f"{group or gid()}|{role}|{rel}"
    p._element.nvPicPr.cNvPr.set("descr", alt or Path(rel).stem.replace("-", " "))
    if base == ASSETS:
        USED.add(rel)
    return px, py, pw, ph


def icon(slide, name, colour, cx, cy, d, *, circle=None, ring=None, group=None, scale=0.56):
    g = group or gid()
    if circle or ring:
        box(slide, cx - d / 2, cy - d / 2, d, d, fill=circle, line=ring, lw=2, shape="oval", role="deco", group=g)
    s = d * scale
    pic(slide, f"{name}_{colour}.png", cx - s / 2, cy - s / 2, s, s, base=ICONS, role="icon", group=g, alt="")
    return g


def cell_lines(cell, bottom=LINE, width_pt=1.0):
    tcPr = cell._tc.get_or_add_tcPr()
    for i, tag in enumerate(("a:lnL", "a:lnR", "a:lnT", "a:lnB")):
        ln = etree.Element(qn(tag))
        if tag == "a:lnB" and bottom:
            ln.set("w", str(int(width_pt * 12700)))
            sf = etree.SubElement(ln, qn("a:solidFill"))
            etree.SubElement(sf, qn("a:srgbClr")).set("val", bottom)
        else:
            ln.set("w", "0")
            etree.SubElement(ln, qn("a:noFill"))
        tcPr.insert(i, ln)


def table(slide, x, y, col_w, row_h, rows, *, size=15, group=None, label="table"):
    nr, nc = len(rows), len(col_w)
    heights = row_h if isinstance(row_h, list) else [row_h] * nr
    gf = slide.shapes.add_table(nr, nc, Inches(x), Inches(y), Inches(sum(col_w)), Inches(sum(heights)))
    gf.name = f"{group or gid()}|table|{label}"
    tblPr = gf._element.graphic.graphicData.tbl.tblPr
    tblPr.set("firstRow", "0")
    tblPr.set("bandRow", "0")
    for el in tblPr.findall(qn("a:tableStyleId")):
        tblPr.remove(el)
    tbl = gf.table
    for i, cwid in enumerate(col_w):
        tbl.columns[i].width = Inches(cwid)
    for r, hh in enumerate(heights):
        tbl.rows[r].height = Inches(hh)
    for r, row in enumerate(rows):
        for c, val in enumerate(row):
            d = val if isinstance(val, dict) else {"text": val}
            cell = tbl.cell(r, c)
            cell.fill.solid()
            cell.fill.fore_color.rgb = rgb(d.get("fill", PAPER))
            cell_lines(cell, bottom=d.get("line", LINE))
            cell.margin_left = cell.margin_right = Inches(0.12)
            cell.margin_top = cell.margin_bottom = Inches(0.04)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            tf = cell.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            p.alignment = {"l": PP_ALIGN.LEFT, "c": PP_ALIGN.CENTER, "r": PP_ALIGN.RIGHT}[d.get("align", "l" if c == 0 else "c")]
            run = p.add_run()
            run.text = d["text"]
            f = run.font
            f.size = Pt(d.get("size", size))
            f.name = d.get("font", BODY)
            f.bold = d.get("bold", False)
            f.color.rgb = rgb(d.get("color", INK))
    return gf


def slide_number_box(slide, n, dark):
    shp = slide.shapes.add_textbox(Inches(SW - MX - 1.0), Inches(7.04), Inches(1.0), Inches(0.26))
    shp.name = "chrome|slidenum|"
    tf = shp.text_frame
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.RIGHT
    fld = etree.SubElement(p._p, qn("a:fld"))
    fld.set("id", "{B6F15528-21DE-4FAA-801E-634DDDAF4B2B}")
    fld.set("type", "slidenum")
    rPr = etree.SubElement(fld, qn("a:rPr"))
    rPr.set("lang", "en-ZA")
    rPr.set("sz", "1000")
    sf = etree.SubElement(rPr, qn("a:solidFill"))
    etree.SubElement(sf, qn("a:srgbClr")).set("val", MUTED_DARK if dark else MUTED)
    etree.SubElement(rPr, qn("a:latin")).set("typeface", BODY)
    etree.SubElement(fld, qn("a:t")).text = str(n)


def chrome(slide, n, dark):
    text(slide, MX, 7.04, 4.0, 0.26, "FluxMuse · Confidential", size=10, color=MUTED_DARK if dark else MUTED,
         role="footer", group="chrome")
    slide_number_box(slide, n, dark)


def new_slide(prs, dark=False):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(s, NIGHT if dark else PAPER)
    s._fm_dark = dark
    return s


def header(slide, eyebrow, title, *, dark=False, title_size=32, y=0.42, w=CW):
    g = gid("hdr")
    text(slide, MX, y, w, 0.26, eyebrow.upper(), size=12, bold=True, color=ORANGE if dark else DEEP,
         role="eyebrow", group=g, spc=150)
    text(slide, MX, y + 0.28, w, 0.78, title, size=title_size, font=HEAD, bold=True,
         color=PAPER if dark else INK, role="title", group=g, anchor="t")


def notes(slide, t):
    slide.notes_slide.notes_text_frame.text = " ".join(t.split())


# ---------------------------------------------------------------- image crops (l, t, r, b)
CH = (0, 0.145, 0, 0.05)  # model charts: drop the baked-in title/subtitle and source line; slides restate them


def chart(slide, name, box_, *, dark=False, crop=CH, alt="", align="t"):
    rel = f"charts/{name}_16x9{'_dark' if dark else ''}.png"
    return pic(slide, rel, *box_, crop=crop, alt=alt or name.replace("_", " "), align=align)


def caption(slide, x, y, w, h, t, *, dark=False, size=11, align="l"):
    return text(slide, x, y, w, h, t, size=size, color=MUTED_DARK if dark else MUTED, role="caption", align=align)


def tile(slide, x, y, w, h, value, label, *, fill=MIST, vcolor=DEEP, vsize=22, lsize=14, sub=None, dark=False):
    g = gid("tile")
    box(slide, x, y, w, h, fill=fill, shape="round", radius=0.16, role="card", group=g)
    text(slide, x + 0.22, y + 0.14, w - 0.44, 0.52, value, size=vsize, font=HEAD, bold=True, color=vcolor,
         role="card", group=g)
    text(slide, x + 0.22, y + 0.7, w - 0.44, (h - 0.76) if not sub else 0.54, label, size=lsize,
         color=PAPER if dark else INK, role="card", group=g)
    if sub:
        text(slide, x + 0.22, y + 1.3, w - 0.44, h - 1.45, sub, size=12, color=MUTED_DARK if dark else MUTED,
             role="caption", group=g)
    return g


def hdr_cell(t, **k):
    d = {"text": t, "fill": NIGHT, "color": PAPER, "bold": True, "font": HEAD, "size": 14, "line": None}
    d.update(k)
    return d


# ================================================================ CORE SLIDES
SEED_M = f"R{M['seed_zar'] / 1e6:.0f}M"
SEED_USD = f"US${M['seed_usd'] / 1e6:.2f}M"
PASS = M["profitable_on_seed_alone"]
CC = M["constraint_checks"]
FG = M["first_group"]
FP = M["free_plan"]
FCS = M["free_conversion_sensitivity"]
SRC = "Sources: 00_FACTS_AND_ASSUMPTIONS.md; 08_Prospects/CURRENT_OFFER.md; 06_Financial_Model/Financial_Model_Notes.md"


def s_title(prs):
    s = new_slide(prs, dark=True)
    pic(s, "brand/fluxmuse-logo-dark.png", MX, 0.55, 2.6, 0.9, align="tl", alt="FluxMuse logo")
    text(s, MX, 2.0, 6.6, 0.3, "FLUXMUSE · INVESTOR PRESENTATION", size=13, bold=True, color=ORANGE,
         role="eyebrow", spc=150)
    text(s, MX, 2.38, 6.5, 2.2, "An AI marketing team and a WhatsApp shop for African small businesses", size=32,
         font=HEAD, bold=True, color=PAPER, role="title", lsp=0.95)
    g = gid()
    box(s, MX, 4.8, 3.3, 0.58, fill=ORANGE, shape="round", radius=0.29, role="chip", group=g)
    text(s, MX, 4.8, 3.3, 0.58, f"Seed round · {SEED_M}", size=18, bold=True, color=NIGHT,
         align="c", anchor="m", role="chip", group=g)
    text(s, MX, 5.65, 6.5, 0.36, [[("[[DATE]]", {"color": PAPER, "bold": True}),
                                  ("  ·  Confidential", {"color": MUTED_DARK})]], size=16, role="placeholder")
    text(s, MX, 6.1, 6.5, 0.3, "Fluxmuse (Pty) Ltd · South Africa · fluxmuse.ai", size=14, color=MUTED_DARK, role="body")
    pic(s, "infographics/how-fluxmuse-works_square_dark.png", 7.3, 1.3, 5.6, 5.0, crop=(0.04, 0.16, 0.04, 0.04),
        alt="Loop: Plan, Create, Publish, Sell on a WhatsApp shop, Learn, run by the AI marketing team")
    notes(s, f"""Thank you for your time. FluxMuse, built by Fluxmuse (Pty) Ltd in South Africa, gives small
    businesses an AI marketing team and a shop that runs on WhatsApp. The product is newly launched in South
    Africa. We have no paying customers yet, and we say so up front. We are raising a {SEED_M} seed, about
    {SEED_USD}. In the base case of our model this round carries the company to profitability with no Series A;
    the upside case passes too, the conservative case does not, and the headroom is thin. Every figure is from
    financial model {M['version']}, dated {M['model_date']}. {SRC}. Replace [[DATE]] before sending.""")
    return s


def s_problem(prs):
    s = new_slide(prs)
    header(s, "The problem", "Sales happen in chat. The tools don't.")
    cards = [("chat", "Buyers already shop in chats",
              "They find a business on social or a WhatsApp Status, then ask, order and pay in chat, answered by hand."),
             ("megaphone", "No marketing capacity",
              "Owners post when they find time. A marketer or agency retainer is out of reach for many."),
             ("card", "Selling is still manual",
              "Catalogues, prices and orders live in photo albums and chat threads, not in a shop.")]
    cwid, gap = 3.84, (CW - 3 * 3.84) / 2
    for i, (ic, t, b) in enumerate(cards):
        x = MX + i * (cwid + gap)
        g = gid("prob")
        box(s, x, 1.72, cwid, 3.62, fill=MIST, shape="round", radius=0.2, role="card", group=g)
        icon(s, ic, "deep", x + 0.75, 2.45, 0.9, circle=PAPER, group=g)
        text(s, x + 0.32, 3.0, cwid - 0.64, 0.85, t, size=19, font=HEAD, bold=True, role="card", group=g)
        text(s, x + 0.32, 3.92, cwid - 0.64, 1.35, b, size=15, color=SLATE, role="card", group=g)
    g = gid("band")
    box(s, MX, 5.52, CW, 1.15, fill=NIGHT, shape="round", radius=0.2, role="card", group=g)
    icon(s, "sparkles", "ink", MX + 0.72, 6.1, 0.66, circle=ORANGE, group=g)
    text(s, MX + 1.35, 5.62, CW - 1.75, 0.95, "FluxMuse works where the owner already works: on WhatsApp, "
         "turning photos into a shop and posts, and orders into alerts.", size=19, font=HEAD, bold=True,
         color=PAPER, anchor="m", role="card", group=g)
    notes(s, """Start with how small businesses in South Africa actually sell. Buyers find them on Facebook,
    Instagram, TikTok or a WhatsApp Status, then ask questions, order and pay in chat, and the owner handles every
    message by hand. Owners rarely have the time or budget for marketing, so posting is patchy and agency
    retainers are out of reach. The catalogue is a photo album and the order book is a chat thread. We show no
    market statistics here on purpose: this framing comes from our segment work, and we will measure it with the
    first group of businesses we set up by hand. Sources: 00_FACTS_AND_ASSUMPTIONS.md; CURRENT_OFFER.md §3 and §4.""")
    return s


def s_solution(prs):
    s = new_slide(prs, dark=True)
    header(s, "The solution", "An AI team that markets and sells on WhatsApp", dark=True)
    pic(s, "infographics/how-fluxmuse-works_dark.png", MX, 1.62, 7.3, 3.5, crop=(0.08, 0.24, 0.08, 0.06),
        align="tl", alt="Loop: Plan (Strategist), Create (Creator), Publish (Publisher), Sell (WhatsApp shop), "
        "Learn (Analyst)")
    rows = [("sparkles", "AI captions, images, short video clips and voice-note transcription, on WhatsApp"),
            ("cart", "WhatsApp Concierge: send photos, get a catalogue and a hosted shop link")]
    for i, (ic, t) in enumerate(rows):
        y = 5.35 + i * 0.72
        g = icon(s, ic, "ink", MX + 0.3, y + 0.3, 0.58, circle=ORANGE)
        text(s, MX + 0.78, y, 6.55, 0.6, t, size=15, color=PAPER, anchor="m", role="body", group=g)
    pic(s, "infographics/whatsapp-commerce-flow_dark.png", 8.2, 1.62, 4.53, 3.5, crop=(0.03, 0.25, 0.03, 0.08),
        alt="WhatsApp commerce flow: discover, chat, catalogue, cart, pay (being switched on), order alert, come back")
    text(s, 8.2, 5.35, 4.53, 1.3, "Newly launched in South Africa. Facebook and Instagram auto-publishing and "
         "checkout through FluxMuse are being switched on.", size=14, color=MUTED_DARK, role="body")
    notes(s, """FluxMuse is one loop, run from WhatsApp. The owner sends product photos; the Concierge drafts the
    catalogue entry and the owner replies yes, no or edit. A hosted shop link sends each order to the owner's own
    WhatsApp, and they reply SOLD. The POST keyword returns a caption and image ready for WhatsApp Status; short
    video clips, voice-note transcription and answers in the customer's language are live too. All of this is
    newly launched, and no merchant has run it end to end yet. Facebook and Instagram auto-publishing wait on
    Meta permissions. Sources: CURRENT_OFFER.md §3; 00_FACTS_AND_ASSUMPTIONS.md.""")
    return s


def s_product(prs):
    s = new_slide(prs)
    header(s, "Product", "What is live, in setup and not yet available")
    pic(s, "infographics/platform-stack.png", MX, 1.62, 5.4, 3.1, crop=(0.03, 0.18, 0.03, 0.06), align="tl",
        alt="Platform: live chips (WhatsApp, AI content, shop and orders) and dashed chips being switched on")
    caption(s, MX, 4.8, 5.4, 0.5, "Solid chips are live and newly launched; dashed chips are being switched on.",
            size=12)
    stats = [("9", "plans in three bands"), (rn(PT["zar_list_monthly"]["Nano"]), "entry paid plan"),
             ("ZA", "live market")]
    sw = (5.4 - 0.3) / 3
    for i, (v, l) in enumerate(stats):
        tile(s, MX + i * (sw + 0.15), 5.4, sw, 1.45, v, l, fill=TINT, vsize=24)
    LIVE = {"fill": TINT, "color": DEEP, "bold": True}
    SET = {"fill": MIST, "color": INK, "bold": True}
    NO = {"fill": MIST, "color": MUTED, "bold": True}
    data = [("WhatsApp shop", "Concierge, shop link, order alerts, SOLD", "Live", LIVE),
            ("AI content", "Captions, images, short video, voice notes", "Live", LIVE),
            ("WhatsApp Business", "Setup, templates, broadcast to consented contacts", "Live", LIVE),
            ("TikTok", "Video posting (approved)", "Live", LIVE),
            ("Facebook / Instagram", "Auto-publishing (Meta permissions pending)", "In setup", SET),
            ("Checkout, AI Voice", "FluxMuse checkout; AI Voice beta; daily digest", "In setup", SET),
            ("Not yet", "Instagram DMs, X, checkout outside SA", "Not available", NO)]
    rows = [[hdr_cell("Layer", align="l"), hdr_cell("What's included", align="l"), hdr_cell("Status")]]
    for a, b, st, sty in data:
        rows.append([{"text": a, "bold": True}, {"text": b, "align": "l"}, dict(sty, text=st)])
    table(s, 6.3, 1.62, [1.85, 3.18, 1.4], [0.45] + [0.68] * 7, rows, size=14, label="stack")
    notes(s, """This is the product as it stands, with an honest status column taken from the current offer. Live
    and newly launched: the WhatsApp Concierge, hosted shop link, order alerts and SOLD, AI captions, images, short
    video and voice-note transcription, WhatsApp Business setup and consented broadcasts, and TikTok video posting.
    Being switched on: Facebook and Instagram auto-publishing, which waits on Meta permissions, checkout through
    FluxMuse, which is built but not yet tested with real money, AI Voice in beta, and the daily digest. Not
    available: Instagram DMs and comments, X posting, and checkout outside South Africa. Sources: CURRENT_OFFER.md
    §3; infographic platform-stack.""")
    return s


def s_market(prs):
    s = new_slide(prs)
    header(s, "Why Africa, why now · market estimates", "Small businesses already sell on mobile")
    rows = [(">90%", "of internet users in SA and Nigeria use WhatsApp", "DataReportal 2025 est."),
            ("~70%", "of global mobile money value is in Sub-Saharan Africa", "GSMA State of the Industry 2025 est."),
            ("~44M", "MSMEs in Sub-Saharan Africa", "IFC / World Bank est."),
            ("~39M", "MSMEs in Nigeria; ~7.4M in Kenya; ~2.5–3M SMMEs in South Africa",
             "SMEDAN, KNBS, SEDA / Stats SA est.")]
    for i, (v, l, src) in enumerate(rows):
        y = 1.7 + i * 1.2
        g = gid("why")
        text(s, MX, y, 1.6, 0.62, v, size=26, font=HEAD, bold=True, color=DEEP, anchor="m", role="card", group=g)
        text(s, MX + 1.7, y, 3.35, 0.62, l, size=14, anchor="m", role="body", group=g)
        caption(s, MX + 1.7, y + 0.68, 3.35, 0.3, src).name = f"{g}|caption|"
    chart(s, "tam_sam_som", (5.95, 1.62, 6.78, 3.6), crop=(0.1, 0.14, 0.02, 0.05),
          alt="TAM 44 million MSMEs, SAM 3.5 million SMBs, SOM 17,500 paying workspaces (estimates)")
    ms = M["market_sizing"]
    caption(s, 5.95, 5.35, 6.78, 1.0, f"TAM: IFC / World Bank est. SAM and SOM: FluxMuse planning estimates. "
            f"The base case reaches {num(BASE['fy5_paying_workspaces'])} paying workspaces in FY5, "
            f"{ms['model_fy5_workspaces_pct_of_som']}% of SOM ({PROJ.lower()}). Verify all estimates before "
            "external use.", size=12)
    notes(s, f"""Why Africa, and why now. WhatsApp is where commerce already happens: more than 90% of internet
    users in South Africa and Nigeria use it (DataReportal 2025 est.), and Sub-Saharan Africa handles about 70% of
    global mobile money value (GSMA est.). There are roughly 44 million MSMEs in the region. We size a serviceable
    market of about 3.5 million digitally active small businesses across the African markets our payment partners
    can reach, and an obtainable share of 0.5%, or 17,500 paying workspaces. The base case needs
    {num(BASE['fy5_paying_workspaces'])}. These are estimates to verify before external use. Sources:
    00_FACTS_AND_ASSUMPTIONS.md §5; model_summary.json → market_sizing.""")
    return s


def s_model(prs):
    s = new_slide(prs)
    header(s, "Business model · priced in rands", "Nine plans in three bands")
    zar = PT["zar_list_monthly"]
    bands = PT["bands"]
    rows = [[hdr_cell("Band", align="l"), hdr_cell("Plan", align="l"), hdr_cell("Monthly"), hdr_cell("Annual")]]
    for band, tiers in bands.items():
        for t in tiers:
            fill = TINT if t == "Growth" else PAPER
            if t == "Custom":
                mo, an = "By consultation", "–"
            else:
                mo, an = rn(zar[t]), rn(zar[t] * 10)
            rows.append([{"text": band if t == tiers[0] else "", "bold": True, "fill": fill, "color": DEEP},
                         {"text": t, "bold": True, "fill": fill, "align": "l"},
                         {"text": mo, "fill": fill, "bold": True}, {"text": an, "fill": fill}])
    table(s, MX, 1.62, [1.75, 1.9, 2.25, 1.95], [0.4] + [0.37] * 9, rows, size=14, label="pricing")
    chips = [("Annual = 10× monthly", 2.45), ("Paid plans start with payment", 3.1), ("No VAT added", 2.1)]
    x = MX
    for t, wdt in chips:
        g = gid()
        box(s, x, 5.44, wdt, 0.42, fill=MIST, shape="round", radius=0.21, role="chip", group=g)
        text(s, x, 5.44, wdt, 0.42, t, size=14, bold=True, align="c", anchor="m", role="chip", group=g)
        x += wdt + 0.1
    fm = PT["founding_member_first_2_bills_zar"]
    g = gid("fm")
    box(s, MX, 5.98, 7.85, 0.92, fill=TINT, shape="round", radius=0.16, role="card", group=g)
    text(s, MX + 0.25, 6.02, 7.35, 0.84, [[("Founding Member, live now: ", {"bold": True, "color": DEEP}),
                                          (f"30% off the first two monthly bills for South African sign-ups "
                                           f"(Nano {rn(fm['Nano'])}, Growth {rn(fm['Growth'])}). Partner "
                                           f"wholesale {rn(PT['partner_wholesale_monthly']['ZAR'])}.", {})]],
         size=14, anchor="m", role="card", group=g)
    st = A[4]["revenue_by_stream_zar"]
    g = gid("streams")
    x0, w0 = 8.65, 4.08
    box(s, x0, 1.62, w0, 5.28, fill=MIST, shape="round", radius=0.2, role="card", group=g)
    text(s, x0 + 0.3, 1.82, w0 - 0.6, 0.28, "REVENUE STREAMS · FY5", size=12, bold=True, color=DEEP,
         role="eyebrow", group=g, spc=120)
    text(s, x0 + 0.3, 2.1, w0 - 0.6, 0.28, PROJ, size=12, color=MUTED, role="caption", group=g)
    items = [("Subscriptions (net)", rm(st["subscriptions"]), False),
             ("WhatsApp messaging", rm(st["whatsapp_messaging"]), False),
             ("AI-credit packs", rm(st["ai_credit_topups"]), False),
             ("Custom setup fees", rm(st["enterprise_setup_fees"]), False),
             ("FluxMuse checkout fee", "R0", False),
             ("Total revenue", rm(A[4]["total_revenue_zar"]), True)]
    for i, (lab, v, bold) in enumerate(items):
        y = 2.52 + i * 0.5
        if bold:
            box(s, x0 + 0.3, y - 0.04, w0 - 0.6, 0.02, fill=SLATE, role="deco", group=g)
        text(s, x0 + 0.3, y, 2.4, 0.42, lab, size=15, bold=bold, anchor="m", role="card", group=g)
        text(s, x0 + 2.7, y, w0 - 3.0, 0.42, v, size=15, bold=True, align="r", anchor="m", role="card", group=g)
    caption(s, x0 + 0.3, 5.7, w0 - 0.6, 1.0, "Paystack card and EFT fees pass through to the merchant. FluxMuse "
            "adds no fee on checkout in any scenario.", size=11).name = f"{g}|caption|"
    notes(s, f"""Revenue is mainly subscriptions, priced in rands in three bands. Small: a permanent Free plan,
    Nano at {rn(zar['Nano'])} and Micro at {rn(zar['Micro'])}. Medium: Starter {rn(zar['Starter'])}, Growth
    {rn(zar['Growth'])} and Scale {rn(zar['Scale'])}. Enterprise: Corporate {rn(zar['Corporate'])}, Agency
    {rn(zar['Agency'])} and Custom by consultation. Annual is ten times monthly, and every paid plan starts with
    payment. Agencies resell at partner wholesale of
    {rn(PT['partner_wholesale_monthly']['ZAR'])}. In FY5 the model books {rm(st['subscriptions'])} of net
    subscriptions out of {rm(A[4]['total_revenue_zar'])} of total revenue. Sources: CURRENT_OFFER.md §1; model_summary.json →
    price_tables; Financial_Model_Notes.md §4.""")
    return s


def s_gtm(prs):
    s = new_slide(prs)
    header(s, "Go-to-market · South Africa now", "Three segments, one partner channel")
    zar = PT["zar_list_monthly"]
    cards = [("users", "Solo sellers", "Side-hustles, solo shops", f"Nano {rn(zar['Nano'])} → Micro → Starter",
              "Self-serve; Free plan as the on-ramp"),
             ("briefcase", "SMEs", "Growing small businesses", f"Starter {rn(zar['Starter'])} → Scale",
              "Guided onboarding call"),
             ("layers", "Agency partners", "Managing many SMB clients",
              f"Partner wholesale {rn(PT['partner_wholesale_monthly']['ZAR'])}",
              "Live demo on a client's public catalogue")]
    cwid, gap = 3.84, (CW - 3 * 3.84) / 2
    for i, (ic, name, who, tier, motion) in enumerate(cards):
        x = MX + i * (cwid + gap)
        g = gid("seg")
        box(s, x, 1.62, cwid, 2.32, fill=MIST, shape="round", radius=0.2, role="card", group=g)
        icon(s, ic, "deep", x + 0.55, 2.1, 0.62, circle=PAPER, group=g)
        text(s, x + 0.98, 1.84, cwid - 1.15, 0.52, name, size=17, font=HEAD, bold=True, anchor="m", role="card", group=g)
        text(s, x + 0.3, 2.5, cwid - 0.6, 0.32, who, size=14, color=MUTED, role="card", group=g)
        text(s, x + 0.3, 2.86, cwid - 0.6, 0.36, tier, size=16, bold=True, color=DEEP, role="card", group=g)
        text(s, x + 0.3, 3.26, cwid - 0.6, 0.58, motion, size=14, role="card", group=g)
    g = gid("fmband")
    box(s, MX, 4.1, CW, 0.56, fill=TINT, shape="round", radius=0.28, role="card", group=g)
    icon(s, "calendar", "deep", MX + 0.4, 4.38, 0.4, group=g, scale=1.0)
    text(s, MX + 0.8, 4.1, CW - 1.0, 0.56, f"Opening with a small first group, set up by hand: about {FG['per_month']} "
         f"businesses a month, {span(*FG['months'].split(' - '))} (model input). Founding Member is live.", size=15, bold=True,
         anchor="m", role="card", group=g)
    steps = [("1 · NOW", "South Africa", "Billed in ZAR · Paystack live", False),
             ("2 · WAVE 1, PENDING", "Nigeria, Kenya, Ghana",
              f"Priced, not on sale · {span(LAUNCH['Nigeria'], LAUNCH['Ghana'])}", False),
             ("3 · LATER", "19 more countries", f"USD, self-serve · model {LAUNCH['Rest of Africa (USD)']}", False),
             ("4 · COMING SOON", "Botswana & Namibia", "No payment provider yet", True)]
    bw = 2.75
    bgap = (CW - 4 * bw) / 3
    for i, (eb, t, sub, dashed) in enumerate(steps):
        x = MX + i * (bw + bgap)
        g = gid("step")
        box(s, x, 4.88, bw, 1.78, fill=None if dashed else PAPER, line=MUTED if dashed else LINE, lw=1.5,
            dash=dashed, shape="round", radius=0.18, role="card", group=g)
        text(s, x + 0.2, 5.02, bw - 0.4, 0.26, eb, size=11, bold=True, color=MUTED if dashed else DEEP,
             role="eyebrow", group=g, spc=80)
        text(s, x + 0.2, 5.3, bw - 0.4, 0.66, t, size=15, font=HEAD, bold=True, role="card", group=g)
        text(s, x + 0.2, 5.98, bw - 0.4, 0.6, sub, size=14, color=MUTED, role="card", group=g)
        if i < 3:
            box(s, x + bw + bgap / 2 - 0.13, 5.62, 0.26, 0.3, fill=ORANGE, shape="right", role="deco", group=gid())
    caption(s, MX, 6.74, CW, 0.26, "Expansion waits for Fincra and pawaPay accounts to go live and for each MRR gate. "
            f"Launch months: {PROJ.lower()}.")
    notes(s, f"""We sell in South Africa now, to three segments. Solo sellers start self-serve on Nano or Micro, with
    the Free plan as an on-ramp, not a trial. SMEs start on Starter or Growth with a guided call. Agencies are our
    partner channel at wholesale, and we demo on a client's own public catalogue. We are opening with a small
    first group of businesses and setting each one up by hand. Nigeria, Kenya and Ghana are priced but not on
    sale: checkout there waits for the Fincra and pawaPay accounts. The model opens them in {LAUNCH['Nigeria']},
    {LAUNCH['Kenya']} and {LAUNCH['Ghana']}. Sources: CURRENT_OFFER.md §3 and §4; model_summary.json → markets.""")
    return s


def s_payments(prs):
    s = new_slide(prs, dark=True)
    header(s, "Payments", "Live in South Africa. The rest is pending.", dark=True)
    pic(s, "infographics/payment-coverage-map_dark.png", MX, 1.62, 8.9, 4.1, crop=(0, 0.205, 0, 0), align="tl",
        alt="Tile map: paid checkout live in South Africa only; Nigeria, Kenya and Ghana priced, not on sale; "
        "pawaPay and Fincra contracted, accounts pending; Botswana and Namibia coming soon")
    cards = [("Live today", "Paystack in SA; Yoco and Ozow for our billing"),
             ("Being switched on", "FluxMuse checkout, not yet tested with real money"),
             ("Pending", "pawaPay, Fincra signed; accounts pending")]
    for i, (t, b) in enumerate(cards):
        y = 1.62 + i * 1.38
        g = gid("moat")
        box(s, 9.75, y, 2.98, 1.25, fill=NIGHT_CARD, shape="round", radius=0.16, role="card", group=g)
        text(s, 9.98, y + 0.14, 2.55, 0.38, t, size=16, font=HEAD, bold=True, color=ORANGE, role="card", group=g)
        text(s, 9.98, y + 0.52, 2.55, 0.68, b, size=14, color=PAPER, role="card", group=g)
    x = MX
    for r, st in [("Paystack", "live"), ("Yoco", "billing"), ("Ozow", "billing"), ("pawaPay", "pending"),
                  ("Fincra", "pending")]:
        g = gid()
        box(s, x, 5.98, 1.5, 0.5, fill=NIGHT_CARD, line="37424D", shape="round", radius=0.25, role="chip", group=g)
        text(s, x, 5.98, 1.5, 0.5, r, size=15, bold=True, color=PAPER if st != "pending" else MUTED_DARK, align="c",
             anchor="m", role="chip", group=g)
        x += 1.62
    caption(s, 8.8, 5.9, 3.93, 0.8, "No paid checkout outside South Africa yet. Card fees are Paystack's, passed "
            "through; no FluxMuse fee.", dark=True, size=12)
    notes(s, """Payments, stated plainly. Paystack is live in South Africa, and Yoco and Ozow run FluxMuse's own
    subscription billing. Checkout through FluxMuse for merchants is built but not yet tested end to end with real
    money, so we describe it as being switched on. pawaPay and Fincra are contracted for expansion, but the
    accounts are pending, so there is no paid checkout in Nigeria, Kenya, Ghana or anywhere outside South Africa
    yet. Card fees are Paystack's standard fee, passed through, with no FluxMuse fee on top. Getting these rails
    live is part of what the expansion money buys. Sources: CURRENT_OFFER.md §2 to §4; infographic
    payment-coverage-map_dark.""")
    return s


def s_traction(prs):
    s = new_slide(prs)
    header(s, "Where we are · no customers yet", "Live, verified, and opening by hand")
    tiles = [("checkCircle", "Verified Meta Tech Provider", "Business and access verification"),
             ("chat", "Live in South Africa", "Newly launched on WhatsApp"),
             ("card", "Paystack live", "South Africa; others pending"),
             ("send", "TikTok posting approved", "Meta publishing in setup")]
    tw = (CW - 3 * 0.2) / 4
    for i, (ic, t, b) in enumerate(tiles):
        x = MX + i * (tw + 0.2)
        g = gid("proof")
        box(s, x, 1.62, tw, 2.25, fill=MIST, shape="round", radius=0.18, role="card", group=g)
        icon(s, ic, "deep", x + 0.55, 2.15, 0.64, circle=PAPER, group=g)
        text(s, x + 0.25, 2.6, tw - 0.5, 0.7, t, size=16, font=HEAD, bold=True, role="card", group=g)
        text(s, x + 0.25, 3.3, tw - 0.5, 0.52, b, size=14, color=MUTED, role="card", group=g)
    g = gid("first")
    box(s, MX, 4.1, 7.4, 2.58, fill=TINT, shape="round", radius=0.2, role="card", group=g)
    text(s, MX + 0.35, 4.3, 6.7, 0.28, "FIRST GROUP · BEING SET UP", size=12, bold=True, color=DEEP, role="eyebrow",
         group=g, spc=150)
    text(s, MX + 0.35, 4.62, 6.7, 0.45, "A small first group of businesses, set up by hand", size=18, font=HEAD,
         bold=True, role="card", group=g)
    box(s, MX + 1.3, 5.52, 4.8, 0.04, fill=ORANGE, role="deco", group=g)
    marks = [("Oct 2026", "Selling opens in SA"), (FG["months"].split(" - ")[1], "First group done (model)"),
             (CASH["seed_month"], "Seed closes (model)")]
    for i, (d, l) in enumerate(marks):
        cx = MX + 1.3 + i * 2.4
        box(s, cx - 0.12, 5.42, 0.24, 0.24, fill=ORANGE if i == 2 else PAPER, line=ORANGE, lw=2, shape="oval",
            role="deco", group=g)
        text(s, cx - 1.1, 5.76, 2.2, 0.8, [{"runs": d, "bold": True, "color": DEEP if i == 2 else INK}, l],
             size=14, align="c", role="card", group=g)
    g = gid("lead")
    box(s, 8.2, 4.1, 4.53, 2.58, fill=NIGHT, shape="round", radius=0.2, role="card", group=g)
    text(s, 8.5, 4.3, 3.95, 0.28, "LEAD GUARANTEE", size=12, bold=True, color=ORANGE, role="eyebrow", group=g, spc=150)
    text(s, 8.5, 4.64, 3.95, 1.25, "3 qualified leads in 30 days of go-live. If fewer, we extend support at no "
         "extra charge until 3 arrive.", size=14, color=PAPER, role="card", group=g)
    text(s, 8.5, 5.98, 3.95, 0.55, "Conditions: the merchant shares the link and posts weekly.", size=12,
         color=MUTED_DARK, role="caption", group=g)
    notes(s, """Here is what is real today. Fluxmuse (Pty) Ltd is a verified Meta Tech Provider. The product is
    live in South Africa and newly launched, and Paystack is live there. TikTok video posting is approved; Facebook
    and Instagram publishing wait on Meta. We have no paying customers, no pilot and no results, and we do not
    show any. We are opening with a small first group of businesses and setting each up by hand. The offer is
    backed by a lead guarantee: three qualified leads in 30 days of go-live, or extended support at no extra
    charge until they arrive. It is support, never cash. Sources: CURRENT_OFFER.md §2 to §4; 07_Case_Studies/
    First_Group_Case_Studies.md.""")
    return s


def s_competition(prs):
    s = new_slide(prs)
    header(s, "Competition & positioning · qualitative view", "Where FluxMuse sits")
    x0, y0, w, h = 1.05, 2.0, 5.2, 4.2
    g = gid("mx")
    box(s, x0, y0, w, h, fill=MIST, shape="round", radius=0.12, role="deco", group=g)
    box(s, x0 + w / 2 - 0.01, y0 + 0.15, 0.02, h - 0.3, fill="D5D9DE", role="deco", group=g)
    box(s, x0 + 0.15, y0 + h / 2 - 0.01, w - 0.3, 0.02, fill="D5D9DE", role="deco", group=g)
    text(s, x0, 1.62, w, 0.3, "↑ WhatsApp-first, priced in rands", size=13, bold=True, color=SLATE,
         role="caption")
    text(s, x0, 6.28, w, 0.3, "AI marketing + selling in one product →", size=13, bold=True, color=SLATE,
         align="r", role="caption")
    pts = [("Global social media tools", 0.38, 0.14), ("WhatsApp BSPs & chatbot vendors", 0.5, 0.42),
           ("E-commerce platforms", 0.3, 0.6), ("Local agencies", 0.15, 0.78)]
    for lab, fx, fy in pts:
        X, Y = x0 + fx * w, y0 + (1 - fy) * h
        g = gid("pt")
        box(s, X - 0.13, Y - 0.13, 0.26, 0.26, fill=SLATE, shape="oval", role="deco", group=g)
        text(s, X + 0.22, Y - 0.26, 2.3, 0.52, lab, size=14, anchor="m", role="body", group=g)
    X, Y = x0 + 0.82 * w, y0 + 0.15 * h
    g = gid("fm")
    box(s, X - 0.22, Y - 0.22, 0.44, 0.44, fill=ORANGE, shape="oval", role="deco", group=g)
    text(s, X - 0.55, Y + 0.3, 1.85, 0.4, "FluxMuse", size=17, font=HEAD, bold=True, color=DEEP, align="c",
         role="body", group=g)
    cats = [("Global social media tools", "Strong at publishing and analytics. FluxMuse runs from WhatsApp and "
             "builds the shop, priced in rands."),
            ("WhatsApp BSPs & chatbot vendors", "Strong at messaging infrastructure. FluxMuse adds the AI team that "
             "creates the marketing."),
            ("E-commerce platforms", "Strong at storefronts. FluxMuse builds the shop from photos sent on "
             "WhatsApp."),
            ("Local agencies", f"Local knowledge and service. FluxMuse makes them partners, white-label at "
             f"{rn(PT['partner_wholesale_monthly']['ZAR'])}/mo wholesale.")]
    for i, (t, b) in enumerate(cats):
        y = 1.62 + i * 1.28
        g = gid("cat")
        box(s, 6.75, y, 5.98, 1.16, fill=PAPER, line=LINE, lw=1.25, shape="round", radius=0.16, role="card", group=g)
        text(s, 7.05, y + 0.12, 5.38, 0.36, t, size=16, font=HEAD, bold=True, role="card", group=g)
        text(s, 7.05, y + 0.5, 5.38, 0.58, b, size=14, color=SLATE, role="card", group=g)
    notes(s, f"""We position against categories, not named companies, and this map is our qualitative view, not
    measured data. Global social media tools are strong at publishing and analytics. WhatsApp business solution
    providers and chatbot vendors are strong at messaging infrastructure. E-commerce platforms are strong at
    storefronts. Local agencies bring service and local knowledge. FluxMuse aims for the top right: WhatsApp-first
    and priced in rands, with AI marketing and selling in one product. We treat agencies as a channel: they resell
    FluxMuse at the {rn(PT['partner_wholesale_monthly']['ZAR'])} partner wholesale price. Sources:
    00_FACTS_AND_ASSUMPTIONS.md; CURRENT_OFFER.md §1.""")
    return s


def s_unit(prs):
    s = new_slide(prs)
    bl, seg = UE["blended"], UE["by_segment"]
    header(s, f"Unit economics · FY3 · {PROJ}", f"Blended LTV:CAC {bl['ltv_to_cac']}x, payback "
           f"{bl['cac_payback_months']} months")
    chart(s, "unit_economics", (MX, 1.62, 7.9, 3.62), alt="LTV and CAC by segment in FY3")
    g = gid("solo")
    box(s, MX, 5.42, 7.9, 1.25, fill=MIST, shape="round", radius=0.16, role="card", group=g)
    text(s, MX + 0.3, 5.5, 7.3, 1.1, f"Solo does not pay back on fully loaded CAC ({seg['Solo']['ltv_to_cac']}x): "
         f"it earns its place through the Free plan and upgrades, not paid ads. SMEs ({seg['SMEs']['ltv_to_cac']}x) "
         f"and agencies ({seg['Agencies']['ltv_to_cac']}x) carry the blend.", size=14, anchor="m", role="card",
         group=g)
    tw = (3.88 - 0.2) / 2
    vals = [(rn(bl["ltv_zar"]), "Blended LTV"), (rn(bl["cac_zar"]), "Blended CAC"),
            (f"{bl['ltv_to_cac']}x", "LTV:CAC"), (f"{bl['cac_payback_months']} mo", "CAC payback")]
    for i, (v, l) in enumerate(vals):
        tile(s, 8.85 + (i % 2) * (tw + 0.2), 1.62 + (i // 2) * 1.42, tw, 1.26, v, l, fill=TINT)
    rows = [[hdr_cell("Blended", align="l"), hdr_cell("FY1"), hdr_cell("FY3"), hdr_cell("FY5")],
            [{"text": "LTV:CAC", "bold": True}] + [f"{A[i]['unit_economics']['ltv_to_cac']}x" for i in (0, 2, 4)],
            [{"text": "Payback (mo)", "bold": True}] + [f"{A[i]['unit_economics']['cac_payback_months']}" for i in (0, 2, 4)],
            [{"text": "Software GM", "bold": True}] + [pct(A[i]["software_gross_margin_pct"]) for i in (0, 2, 4)]]
    table(s, 8.85, 4.62, [1.6, 0.76, 0.76, 0.76], [0.5, 0.5, 0.5, 0.5], rows, size=14, label="ue-trend")
    caption(s, 8.85, 6.68, 3.88, 0.3, f"LTV = ARPA × software GM ({bl['software_gross_margin_pct']}%) ÷ churn",
            size=11)
    notes(s, f"""Unit economics in FY3, all projections. Blended LTV is {rn(bl['ltv_zar'])} against a blended CAC
    of {rn(bl['cac_zar'])}, so LTV to CAC is {bl['ltv_to_cac']} times and CAC pays back in
    {bl['cac_payback_months']} months. The honest weak spot is Solo: with shared marketing costs loaded, it is
    {seg['Solo']['ltv_to_cac']} times, so we grow Solo through the Free plan and upgrades rather than paid
    acquisition at scale. SMEs are {seg['SMEs']['ltv_to_cac']} times and agencies {seg['Agencies']['ltv_to_cac']}.
    Every one of these figures is a {PROJ.lower()}. Sources: model_summary.json → unit_economics_fy3;
    Financial_Model_Notes.md §7.""")
    return s


def s_projections(prs):
    s = new_slide(prs)
    header(s, f"Financial projections · {PROJ}", f"FY5: {rm(A[4]['total_revenue_zar'])} revenue, "
           f"{A[4]['ebitda_margin_pct']}% EBITDA margin")
    chart(s, "revenue_by_stream_fy1_fy5", (MX, 1.62, 6.2, 2.82), alt="Revenue by stream FY1 to FY5, base case")
    tw = (5.68 - 0.3) / 3
    tv = [(rm(A[4]["total_revenue_zar"]), "FY5 revenue", f"≈US${A[4]['total_revenue_usd'] / 1e6:.2f}M"),
          (rm(A[4]["ebitda_zar"]), "FY5 EBITDA", f"{A[4]['ebitda_margin_pct']}% margin"),
          (num(A[4]["ending_paying_workspaces"]), "paying workspaces", f"{A[4]['headcount_end_fy']} people in FY5")]
    for i, (v, l, sub) in enumerate(tv):
        tile(s, 7.05 + i * (tw + 0.15), 1.62, tw, 2.82, v, l, sub=sub, fill=TINT, vsize=19)
    r = lambda t, **k: dict({"text": t, "align": "c"}, **k)
    em = ["n/m"] + [pct(A[i]["ebitda_margin_pct"]) for i in range(1, 5)]
    rows = [[hdr_cell("Base case (FY = Oct–Sep)", align="l")] + [hdr_cell(f"FY{i + 1}") for i in range(5)],
            [{"text": "Revenue", "bold": True}] + [r(rm(a["total_revenue_zar"]), bold=True) for a in A],
            [{"text": "Gross margin", "bold": True}] + [r(pct(a["gross_margin_pct"])) for a in A],
            [{"text": "EBITDA", "bold": True}] + [r(rm(a["ebitda_zar"]), bold=True,
                                                   color=DEEP if a["ebitda_zar"] >= 0 else INK) for a in A],
            [{"text": "EBITDA margin", "bold": True}] + [r(v) for v in em],
            [{"text": "Paying workspaces (Sep)", "bold": True}] + [r(num(a["ending_paying_workspaces"])) for a in A],
            [{"text": "Subscription ARR", "bold": True}] + [r(rm(a["subscription_arr_zar"])) for a in A]]
    table(s, MX, 4.52, [2.93] + [1.84] * 5, [0.4] + [0.34] * 6, rows, size=14, label="pnl")
    rev = ", ".join(rm(a["total_revenue_zar"]) for a in A)
    neg = sum(1 for a in A if a["ebitda_zar"] < 0)
    notes(s, f"""This is the five-year base case, net of the Founding Member discount, with no VAT. Revenue grows
    {rev} from FY1 to FY5, about US${A[4]['total_revenue_usd'] / 1e6:.2f}M in the final year. Gross margin rises
    from {pct(A[0]['gross_margin_pct'])} to {pct(A[4]['gross_margin_pct'])} as AI cost per workspace falls. EBITDA is
    negative for {neg} years, with the deepest loss of {rm(min(a['ebitda_zar'] for a in A))}, and turns positive at
    {rm(A[4]['ebitda_zar'])} in FY5. Paying workspaces grow from {num(A[0]['ending_paying_workspaces'])} to
    {num(A[4]['ending_paying_workspaces'])}. Every volume is an assumption: there are no customers yet. Sources:
    model_summary.json → annual; Financial_Model_Notes.md §1.""")
    return s


def s_profit(prs):
    s = new_slide(prs)
    header(s, f"Path to profitability · {PROJ}", f"Base case: profitable on the {SEED_M} seed, no Series A")
    chart(s, "cash_runway_r25m", (MX, 1.62, 8.0, 3.62), alt=f"Monthly closing cash on the {SEED_M} seed vs the "
          f"{rm(CASH['min_cash_buffer_zar'])} buffer")
    tiles = [(CASH["break_even_month"], f"EBITDA break-even; sustained from {CASH['break_even_month_sustained']}"),
             (CASH["cash_flow_positive_month"], f"Operating cash flow positive; sustained "
              f"{CASH['cash_flow_positive_month_sustained']}"),
             (rm(CASH["min_post_seed_cash_zar"], 2), f"Cash low ({CASH['min_post_seed_cash_month']}), "
              f"{rm(CASH['headroom_over_buffer_zar'])} above the buffer"),
             ("Thin headroom", "Base and Upside pass; Conservative does not")]
    for i, (v, l) in enumerate(tiles):
        tile(s, 8.85, 1.62 + i * 1.3, 3.88, 1.25, v, l, fill=TINT, vsize=20)
    text(s, MX, 5.42, 8.0, 0.28, "MILESTONE GATING PROTECTS THE BUFFER", size=12, bold=True, color=DEEP,
         role="eyebrow", spc=150)
    chips = ["Every hire waits for its MRR milestone",
             f"NG / KE / GH launch at {rm(GATES['Nigeria'])} / {rm(GATES['Kenya'])} / {rm(GATES['Ghana'])} MRR",
             f"Paid spend capped at R40k + {M['scenario_definitions']['Base']['cap_pct'] * 100:.0f}% of MRR"]
    cwid = (8.0 - 0.3) / 3
    for i, t in enumerate(chips):
        g = gid()
        box(s, MX + i * (cwid + 0.15), 5.8, cwid, 0.85, fill=MIST, shape="round", radius=0.16, role="chip", group=g)
        text(s, MX + i * (cwid + 0.15) + 0.15, 5.8, cwid - 0.3, 0.85, t, size=14, bold=True, anchor="m",
             role="chip", group=g)
    notes(s, f"""The seed is sized to the model: {SEED_M} is the smallest passing seed of
    {rm(M['seed_sizing']['smallest_passing_seed_zar_base'])}, rounded up. It lands in {CASH['seed_month']}. In the
    base case cash falls to {rm(CASH['min_post_seed_cash_zar'], 2)} in {CASH['min_post_seed_cash_month']}, only
    {rm(CASH['headroom_over_buffer_zar'], 2)} above our {rm(CASH['min_cash_buffer_zar'])} buffer. Operating cash flow
    turns positive in {CASH['cash_flow_positive_month']} and EBITDA breaks even in {CASH['break_even_month']}. That
    is a long road and thin headroom. Gating protects it: hires and launches wait for MRR, and paid spend is capped.
    A pre-seed bridge of {rk(CASH['pre_seed_bridge_required_zar'])} is needed before close. Sources:
    model_summary.json → cash, seed_sizing; Financial_Model_Notes.md §1 and §3.""")
    return s


def s_scenarios(prs):
    s = new_slide(prs)
    header(s, f"Scenarios & sensitivities · model {M['version']}",
           f"Base and Upside pass on {SEED_M}; Conservative fails")
    chart(s, "scenarios", (MX, 1.62, 6.15, 3.0), alt="FY5 revenue and EBITDA by scenario")
    rows = [[hdr_cell("Scenario", align="l"), hdr_cell("FY5 revenue"), hdr_cell("FY5 EBITDA"), hdr_cell("Cash low"),
             hdr_cell("Pass")]]
    for name, sc in [("Conservative", CONS), ("Base", BASE), ("Upside", UP)]:
        fill = TINT if name == "Base" else PAPER
        rows.append([{"text": name, "bold": True, "fill": fill}, {"text": rm(sc["fy5_revenue_zar"]), "fill": fill},
                     {"text": rm(sc["fy5_ebitda_zar"]), "fill": fill},
                     {"text": rm(sc["min_post_seed_cash_zar"], 2), "fill": fill},
                     {"text": "Yes" if PASS[name] else "No", "fill": fill, "bold": True,
                      "color": INK if PASS[name] else DEEP}])
    table(s, 6.95, 1.62, [1.55, 1.25, 1.1, 1.1, 0.78], [1.0, 0.6, 0.6, 0.6], rows, size=14, label="scen")
    text(s, 6.95, 4.5, 5.78, 0.78, f"Conservative falls below the {rm(CASH['min_cash_buffer_zar'])} buffer from "
         f"{CONS['first_month_below_buffer']} and does not break even by Sep 2031.", size=14, role="body")
    rp, nr = FX["ZAR 15% stronger (repricing on)"], FX["ZAR 15% stronger (no repricing)"]
    low85 = M["sensitivity_base"]["min_post_seed_cash_zar_m"][2][1]
    f25 = FCS["0.25% a month"]
    cards = [(MIST, "FX SHOCK · ZAR 15% STRONGER",
              f"With quarterly repricing it passes (low {rm(rp['min_post_seed_cash_zar'], 2)}). Without repricing it "
              f"fails: cash low {rm(nr['min_post_seed_cash_zar'], 2)}, FY5 EBITDA {rm(nr['fy5_ebitda_zar'])}."),
             (TINT, "THIN HEADROOM",
              f"Free upgrades at 0.25% a month: cash low {rm(f25['min_post_seed_cash_zar'], 2)}, fails. Sign-ups "
              f"at 0.85x plan: low R{low85:.2f}M, below the buffer.")]
    for i, (fill, eb, b) in enumerate(cards):
        x = MX + i * (5.95 + 0.233)
        g = gid("sens")
        box(s, x, 5.32, 5.95, 1.38, fill=fill, shape="round", radius=0.18, role="card", group=g)
        text(s, x + 0.3, 5.44, 5.35, 0.28, eb, size=12, bold=True, color=DEEP, role="eyebrow", group=g, spc=120)
        text(s, x + 0.3, 5.76, 5.35, 0.88, b, size=14, role="card", group=g)
    notes(s, f"""We are plain about this slide. On {SEED_M}, base and upside pass our test; conservative does not.
    Conservative reaches {rm(CONS['fy5_revenue_zar'])} revenue in FY5, stays above zero, but drops below the buffer
    from {CONS['first_month_below_buffer']} and never breaks even within the horizon. The base case headroom is
    thin: Free users upgrading at 0.25% a month instead of 0.5% breaks it, and so do sign-ups 15% below plan. A
    15% stronger rand passes only if we reprice quarterly. Our response is to measure conversion from the first
    month and slow hiring gates early if it lags. Sources: model_summary.json → scenarios, constraint_checks,
    sensitivity_base, free_conversion_sensitivity, fx_shock; Financial_Model_Notes.md §2, §3, §6 and §10.""")
    return s


def s_risks(prs):
    s = new_slide(prs)
    header(s, "Key risks", "What could go wrong, and how we manage it")
    f25 = FCS["0.25% a month"]
    risks = [("target", "Demand is unproven", "No paying customers yet; every volume is an assumption.",
              "Measure sign-ups and Free upgrades from month 1; slow hiring if they lag."),
             ("chart", "Thin headroom", f"Upgrades at 0.25%/mo take the cash low to {rm(f25['min_post_seed_cash_zar'], 2)}.",
              "Gated hiring; raise gates early. Conservative case still fails."),
             ("shield", "Meta dependency", "Facebook and Instagram publishing wait on Meta approval.",
              "Verified Tech Provider; WhatsApp Status and TikTok work today."),
             ("card", "Payment rails", "Only South Africa has live checkout.",
              "pawaPay and Fincra contracted; no expansion until they are live."),
             ("globe", "FX", "NGN, KES and GHS can weaken against the rand.",
              "Quarterly repricing; without it a ZAR +15% shock fails."),
             ("briefcase", "Execution & hiring",
              f"From 2 founders to {A[2]['headcount_end_fy']} people by the end of FY3.",
              "Every hire waits for an MRR milestone.")]
    cwid, ch = 3.84, 2.45
    gapx = (CW - 3 * cwid) / 2
    for i, (ic, t, r, mtg) in enumerate(risks):
        x = MX + (i % 3) * (cwid + gapx)
        y = 1.62 + (i // 3) * (ch + 0.18)
        g = gid("risk")
        box(s, x, y, cwid, ch, fill=MIST, shape="round", radius=0.18, role="card", group=g)
        icon(s, ic, "deep", x + 0.55, y + 0.5, 0.58, circle=PAPER, group=g)
        text(s, x + 0.98, y + 0.24, cwid - 1.2, 0.52, t, size=17, font=HEAD, bold=True, anchor="m", role="card", group=g)
        text(s, x + 0.3, y + 0.9, cwid - 0.6, 0.55, r, size=14, color=MUTED, role="card", group=g)
        text(s, x + 0.3, y + 1.5, cwid - 0.6, 0.85, mtg, size=14, bold=True, role="card", group=g)
    notes(s, """These are the risks we would want an investor to probe. Demand is unproven: there are no paying
    customers, so conversion and sign-up volume are guesses until we measure them. Headroom is thin: a lower Free
    upgrade rate alone breaks the base case, and the conservative case fails on this seed. Meta has not yet approved
    Facebook and Instagram publishing. Only South Africa has live checkout, and expansion waits for pawaPay and
    Fincra. FX needs repricing discipline. Execution risk is managed by MRR-gated hiring. Sources:
    Financial_Model_Notes.md §6 and §10; CURRENT_OFFER.md §3; model_summary.json → free_conversion_sensitivity.""")
    return s


def s_ask(prs):
    s = new_slide(prs)
    header(s, "The ask", f"{SEED_M} seed to reach profitability")
    g = gid("ask")
    box(s, MX, 1.62, 4.4, 2.6, fill=NIGHT, shape="round", radius=0.2, role="card", group=g)
    text(s, MX + 0.35, 1.7, 3.7, 1.2, SEED_M, size=54, font=HEAD, bold=True, color=ORANGE, role="card", group=g)
    text(s, MX + 0.35, 2.94, 3.7, 0.34, f"Seed round · ≈{SEED_USD}", size=16, bold=True, color=PAPER, role="card",
         group=g)
    text(s, MX + 0.35, 3.32, 3.7, 0.34, "Instrument [[TBC]] · valuation [[TBC]]", size=14, color=PAPER,
         role="placeholder", group=g)
    text(s, MX + 0.35, 3.68, 3.7, 0.5, f"Close {CASH['seed_month']} · pre-seed bridge "
         f"{rk(CASH['pre_seed_bridge_required_zar'])}", size=14, color=MUTED_DARK, role="card", group=g)
    g = gid("rec")
    box(s, MX, 4.4, 4.4, 2.5, fill=TINT, shape="round", radius=0.2, role="card", group=g)
    text(s, MX + 0.3, 4.56, 3.8, 0.28, "WHY THIS SIZE", size=12, bold=True, color=DEEP,
         role="eyebrow", group=g, spc=120)
    text(s, MX + 0.3, 4.88, 3.8, 1.9, f"{rm(M['seed_sizing']['smallest_passing_seed_zar_base'])} is the smallest seed "
         f"at which the base case passes. {rm(REC24['net_cash_consumed_zar'], 2)} is used in the first 24 months; "
         f"the rest carries the long loss-making stretch to the {CASH['min_post_seed_cash_month']} low.", size=14,
         role="card", group=g)
    chart(s, "use_of_funds", (5.3, 1.62, 7.43, 3.35), crop=(0.12, 0.16, 0.08, 0.1), align="c",
          alt=f"Use of funds: {SEED_M} split 40 / 30 / 15 / 15")
    al = {a["category"]: a for a in UOF["allocation"]}
    buys = [(rm(al["Product & engineering"]["amount_zar"]), "product & engineering: ",
             "engineers, AI/ML, design, integrations, hosting"),
            (rm(al["Sales & marketing / partner programme"]["amount_zar"]), "sales & marketing: ",
             "growth team, partnerships, capped paid acquisition"),
            (rm(al["Market expansion (NG, KE, GH) & payments compliance"]["amount_zar"]), "expansion: ",
             "NG/KE/GH rails, teams, compliance"),
            (rm(al["Operations & working capital"]["amount_zar"]), "operations: ",
             "customer success, finance, cash buffer")]
    cw2 = (7.43 - 0.15) / 2
    for i, (v, lab, t) in enumerate(buys):
        x = 5.3 + (i % 2) * (cw2 + 0.15)
        y = 5.1 + (i // 2) * 0.9
        g = gid("buy")
        box(s, x, y, cw2, 0.84, fill=MIST, shape="round", radius=0.14, role="card", group=g)
        text(s, x + 0.15, y + 0.03, cw2 - 0.3, 0.78, [[(f"{v} {lab}", {"bold": True, "color": DEEP}), (t, {})]],
             size=14, anchor="m", role="card", group=g)
    notes(s, f"""We are raising {SEED_M}, about {SEED_USD}, with instrument and valuation to be confirmed. It splits
    40% product and engineering, {rm(al['Product & engineering']['amount_zar'])}; 30% sales, marketing and partners,
    {rm(al['Sales & marketing / partner programme']['amount_zar'])}; 15% Nigeria, Kenya and Ghana expansion with
    payments compliance; and 15% operations and working capital. The size is set by the model, not by appetite: it
    is the smallest seed at which the base case stays above our buffer, rounded up. In the base case the round
    carries us to profitability with no Series A; in the conservative case it does not. Sources: model_summary.json
    → use_of_funds, seed_sizing; 00_FACTS_AND_ASSUMPTIONS.md §7.""")
    return s


def span(a, b):
    """'Oct 2026', 'Jan 2027' -> 'Oct ’26–Jan ’27' (fits a milestone card)."""
    return f"{a[:3]} ’{a[-2:]}–{b[:3]} ’{b[-2:]}"


def s_milestones(prs):
    s = new_slide(prs)
    header(s, "Milestones this round buys", "From a first group to break-even")
    rows = [[("Sept 2026", "Verified Meta Tech Provider", False),
             ("Oct 2026", "Selling in South Africa; Founding Member live", False),
             (span(*FG["months"].split(" - ")), "First group set up by hand (model input)", False),
             ("[[TARGET]]", "FluxMuse checkout and Meta publishing switched on", False),
             (CASH["seed_month"], "Seed closes (model input); first hires", False)],
            [("Pending", "Fincra and pawaPay accounts live", False),
             (span(LAUNCH['Nigeria'], LAUNCH['Ghana']),
              "Nigeria, Kenya and Ghana open (MRR-gated)", True),
             (LAUNCH["Rest of Africa (USD)"], "19 USD markets, self-serve", True),
             (CASH["cash_flow_positive_month"], "Operating cash flow positive", True),
             (CASH["break_even_month"], "EBITDA break-even, no Series A", True)]]
    cw_ = (CW - 4 * 0.16) / 5
    for r, items in enumerate(rows):
        ly = 1.86 + r * 2.5
        box(s, MX + cw_ / 2, ly - 0.02, CW - cw_, 0.04, fill=ORANGE, role="deco", group=gid())
        for i, (d, t, proj) in enumerate(items):
            x = MX + i * (cw_ + 0.16)
            g = gid("ms")
            box(s, x + cw_ / 2 - 0.11, ly - 0.11, 0.22, 0.22, fill=ORANGE if proj else PAPER, line=ORANGE, lw=2,
                shape="oval", role="deco", group=g)
            box(s, x, ly + 0.25, cw_, 1.95, fill=TINT if proj else MIST, shape="round", radius=0.16, role="card", group=g)
            text(s, x + 0.2, ly + 0.42, cw_ - 0.4, 0.4, d, size=16, font=HEAD, bold=True, color=DEEP,
                 role="placeholder" if d.startswith("[[") else "card", group=g)
            text(s, x + 0.2, ly + 0.86, cw_ - 0.4, 1.25, t, size=14, role="card", group=g)
    caption(s, MX, 6.72, CW, 0.26, f"Orange cards: {PROJ.lower()} (Base); dates move with MRR gates and with the "
            "payment accounts.")
    notes(s, f"""This is what the round buys, in order. We are a verified Meta Tech Provider, and selling opened in
    South Africa in October with Founding Member live. The model sets up a first group by hand from
    {FG['months']}. Checkout through FluxMuse and Meta publishing are being switched on; the founder will set a
    target date. The seed closes in {CASH['seed_month']} in the model. Expansion needs the Fincra and pawaPay
    accounts live first; the model then opens Nigeria, Kenya and Ghana from {LAUNCH['Nigeria']} to
    {LAUNCH['Ghana']}, reaches operating cash flow positive in {CASH['cash_flow_positive_month']} and EBITDA
    break-even in {CASH['break_even_month']}. Sources: CURRENT_OFFER.md §3; model_summary.json → markets, cash.""")
    return s


def hire_months():
    """Base-case hire month per role: max(earliest month, seed month, first month whose previous-month net
    MRR >= gate x 1.00); market-linked roles follow the Base launch months. Cross-checked against headcount."""
    mb = M["monthly_base"]
    L, mrr, hc = mb["labels"], mb["subscription_mrr_net_zar"], mb["headcount"]
    seed_i = mb["markers"]["seed_month_index"]
    li = mb["markers"]["launch_month_index"]
    code = {"NG": "Nigeria", "KE": "Kenya", "GH": "Ghana"}
    tot = [0] * 60
    out = []
    for ro in fm_inputs.ROLES:
        if ro["type"] == "F":
            idx = 0
        elif ro["link"]:
            mkt, kind = ro["link"]
            base = li[code[mkt]]
            idx = {"lead": base - 2, "launch": base, "exp": base + 12}[kind]
        else:
            idx = next((i for i in range(max(ro["hire"] - 1, seed_i), 60) if mrr[i - 1] >= ro["gate"]), None)
        if idx is None or idx >= 60:
            continue
        for i in range(idx, 60):
            tot[i] += ro["count"]
        out.append((idx, L[idx], ro))
    assert tot == hc, "hire-month reconstruction does not match model headcount"
    return out


def s_team(prs):
    s = new_slide(prs)
    hc = [A[i]["headcount_end_fy"] for i in range(5)]
    header(s, f"Team · headcount {hc[0]} → {hc[1]} → {hc[4]} (FY1, FY2, FY5; model " + M["version"] + ")", "The team, and who the seed hires")
    people = [("[[FOUNDER NAME, TITLE, BIO]]", "Model role: Founder & CEO"),
              ("[[CO-FOUNDER]]", "Model role: CTO / founding engineer"),
              ("[[ADVISORS]]", "Advisory board")]
    cwid, gap = 3.84, (CW - 3 * 3.84) / 2
    for i, (ph, role) in enumerate(people):
        x = MX + i * (cwid + gap)
        g = gid("ppl")
        box(s, x, 1.62, cwid, 1.7, fill=MIST, shape="round", radius=0.18, role="card", group=g)
        box(s, x + 0.3, 1.84, 0.88, 0.88, fill=PAPER, line=MUTED, lw=1.25, dash=True, shape="oval", role="deco", group=g)
        icon(s, "users", "deep", x + 0.74, 2.28, 0.55, group=g, scale=0.8)
        text(s, x + 1.35, 1.78, cwid - 1.6, 0.9, ph, size=16, font=HEAD, bold=True, role="placeholder", group=g)
        text(s, x + 1.35, 2.72, cwid - 1.6, 0.5, role, size=14, color=MUTED, role="card", group=g)
    hm = hire_months()
    by = lambda pred: [h for h in hm if pred(h[2])]
    first = sorted({lbl for idx, lbl, ro in hm if idx == M["monthly_base"]["markers"]["seed_month_index"] and ro["type"] != "F"})
    def month_of(name):
        return next(lbl for idx, lbl, ro in hm if ro["name"] == name)
    def gate(name):
        return next(ro["gate"] for idx, lbl, ro in hm if ro["name"] == name)
    rows = [[hdr_cell("Month (base)", align="l"), hdr_cell("Key hires (MRR-gated)", align="l"),
             hdr_cell("MRR gate (last month)", align="l")],
            [month_of("Senior full-stack engineers"),
             {"text": "2 senior full-stack engineers, Head of Growth, partnerships manager, customer success lead",
              "align": "l"}, {"text": "At seed close", "align": "l"}],
            [f"{month_of('AI / ML engineer')}–{month_of('Product designer (UX)')}",
             {"text": "AI/ML engineer, performance marketer, product designer, finance & compliance manager",
              "align": "l"}, {"text": f"Up to {rm(gate('Product designer (UX)'), 2)}", "align": "l"}],
            [f"{month_of('Country lead: Nigeria')}–{month_of('Country lead: Ghana')}",
             {"text": "Country leads for Nigeria, Kenya and Ghana, 2 months before each launch", "align": "l"},
             {"text": f"Launch gates {rm(GATES['Nigeria'])}–{rm(GATES['Ghana'])}", "align": "l"}],
            [month_of("Integrations engineers (social adapters, commerce, CRM)"),
             {"text": "2 integrations engineers: social adapters, commerce, CRM", "align": "l"},
             {"text": rm(gate("Integrations engineers (social adapters, commerce, CRM)")), "align": "l"}],
            [f"{month_of('Head of Sales & Partnerships')}–{month_of('CFO')}",
             {"text": "Head of Sales & Partnerships, VP Engineering, CFO", "align": "l"},
             {"text": f"{rm(gate('Head of Sales & Partnerships'))} to {rm(gate('CFO'))}", "align": "l"}]]
    table(s, MX, 3.45, [2.0, 6.73, 3.4], [0.5] + [0.6] * 5, rows, size=14, label="hires")
    notes(s, f"""Introduce the founding team here: fill in the founder, co-founder and advisors, with one line on
    why each is right for this problem. The model runs lean before the seed, with two founders on reduced
    salaries. The seed then funds the hires in the table, each waiting for a monthly recurring revenue milestone:
    engineers, a Head of Growth, a partnerships manager and a customer success lead at close; design, AI and
    finance through 2027; country leads before each wave-1 launch; and senior leaders only once MRR supports
    them. Headcount reaches {hc[0]} by the end of FY1, {hc[1]} in FY2 and {hc[4]} in FY5. Sources: hiring plan in
    _build/fm_inputs.py (ROLES) applied to model_summary.json → monthly_base.subscription_mrr_net_zar, reconciled
    to monthly_base.headcount; annual[].headcount_end_fy.""")
    return s


def s_close(prs):
    s = new_slide(prs, dark=True)
    pic(s, "brand/fluxmuse-logo-dark.png", MX, 0.55, 2.6, 0.9, align="tl", alt="FluxMuse logo")
    text(s, MX, 1.9, 7.0, 0.3, "THANK YOU", size=13, bold=True, color=ORANGE, role="eyebrow", spc=150)
    text(s, MX, 2.25, 7.0, 1.55, "Join the FluxMuse seed round", size=34, font=HEAD, bold=True, color=PAPER,
         role="title")
    text(s, MX, 3.95, 7.0, 0.7, f"{SEED_M} to reach profitability with no Series A in the base case "
         f"({PROJ.lower()}).", size=18, color="D5DADF", role="body")
    rows = [("checkCircle", "Verified Meta Tech Provider"), ("card", "Live in South Africa · Paystack"),
            ("users", "First group being set up by hand")]
    for i, (ic, t) in enumerate(rows):
        y = 4.8 + i * 0.68
        g = icon(s, ic, "ink", MX + 0.3, y + 0.28, 0.56, circle=ORANGE)
        text(s, MX + 0.8, y, 6.0, 0.56, t, size=17, color=PAPER, anchor="m", role="body", group=g)
    g = gid("contact")
    box(s, 8.2, 2.25, 4.53, 3.6, fill=NIGHT_CARD, shape="round", radius=0.2, role="card", group=g)
    text(s, 8.55, 2.55, 3.85, 0.3, "CONTACT", size=12, bold=True, color=ORANGE, role="eyebrow", group=g, spc=150)
    text(s, 8.55, 2.95, 3.85, 2.6, [{"runs": "Thabo Malebadi", "space_after": 6, "bold": True, "color": PAPER},
                                    {"runs": "thabo@fluxmuse.com", "space_after": 12, "color": PAPER},
                                    {"runs": "[[PHONE]]", "space_after": 12},
                                    {"runs": [("Data room: ", {"color": MUTED_DARK}), ("[[LINK]]", {"color": PAPER, "bold": True})]}],
         size=18, color="D5DADF", role="placeholder", group=g)
    notes(s, f"""Close with the ask and a clear next step. FluxMuse gives small businesses an AI marketing team and a
    shop on WhatsApp, newly launched in South Africa. In the model the {SEED_M} seed carries the base case to
    profitability with no Series A; upside passes, conservative does not, and we have shown why. Offer data-room
    access: the financial model and notes, Meta verification evidence and payment contracts. Agree a follow-up
    date before the meeting ends. Fill in [[PHONE]] and the data-room [[LINK]] before sending. Sources:
    model_summary.json → profitable_on_seed_alone (Conservative {PASS['Conservative']}, Base {PASS['Base']}, Upside
    {PASS['Upside']}); CURRENT_OFFER.md §2 and §4; Investor_Deck_Guide.md.""")
    return s


# ================================================================ APPENDIX
def a_divider(prs, items):
    s = new_slide(prs, dark=True)
    text(s, MX, 1.2, CW, 0.3, "APPENDIX", size=12, bold=True, color=ORANGE, role="eyebrow", spc=150)
    text(s, MX, 1.52, CW, 0.9, "Reference slides", size=40, font=HEAD, bold=True, color=PAPER, role="title")
    for i, (lab, t) in enumerate(items):
        y = 2.65 + i * 0.6
        g = gid("ax")
        box(s, MX, y, 0.95, 0.46, fill=ORANGE, shape="round", radius=0.23, role="chip", group=g)
        text(s, MX, y, 0.95, 0.46, lab, size=15, font=HEAD, bold=True, color=NIGHT, align="c", anchor="m",
             role="chip", group=g)
        text(s, MX + 1.2, y, 10, 0.46, t, size=18, color=PAPER, anchor="m", role="body", group=g)
    notes(s, """The appendix supports questions and diligence; it is not part of the main talk track. A1 lists the
    model's key assumptions word for word from the model summary. A2 shows paying workspaces by segment and by
    market. A3 has the nine plans in rands, then local-currency prices for markets that are priced but not yet on
    sale. A4 shows payment rails by country, live and pending. A5 is the FX shock, and A6 the Founding Member
    discount cost. A7 lists founder confirmations still open: it is internal, so hide or delete it before the deck
    goes to any investor. Sources: model_summary.json; 00_FACTS_AND_ASSUMPTIONS.md; CURRENT_OFFER.md.""")
    return s


ASSUMPTION_TOPICS = ["Timing & cash", "First group", "Sign-ups & Free plan", "Founding Member", "Pricing",
                     "Partner wholesale", "Segments", "Churn", "Markets", "Cost discipline", "Other revenue", "COGS",
                     "Funding & tax"]


def a_assumptions(prs):
    ka = M["key_assumptions"]
    assert len(ka) == len(ASSUMPTION_TOPICS), "key_assumptions count changed; update ASSUMPTION_TOPICS"
    heights = [0.2 * max(1, math.ceil(len(t) / 92)) + 0.18 for t in ka]
    pages, cur, hsum = [], [], 0.0
    for i, h in enumerate(heights):
        if hsum + h > 4.7 and cur:
            pages.append(cur)
            cur, hsum = [], 0.0
        cur.append(i)
        hsum += h
    pages.append(cur)
    slides = []
    for p, idxs in enumerate(pages):
        s = new_slide(prs)
        header(s, f"Appendix A1 · key assumptions ({p + 1} of {len(pages)}) · model {M['version']}",
               "Key model assumptions")
        rows = [[hdr_cell("Topic", align="l", size=12), hdr_cell("Assumption (model_summary.json → key_assumptions)",
                                                                  align="l", size=12)]]
        for i in idxs:
            rows.append([{"text": ASSUMPTION_TOPICS[i], "bold": True, "size": 12},
                         {"text": ka[i], "align": "l", "size": 12}])
        table(s, MX, 1.62, [1.9, 10.23], [0.36] + [heights[i] for i in idxs], rows, size=12, label="assumptions")
        topics = ", ".join(ASSUMPTION_TOPICS[i].lower() for i in idxs)
        notes(s, f"""These assumptions are copied word for word from the model summary, so they always match the
        workbook. This page covers {topics}. Items marked [[CONFIRM]] still wait for founder sign-off and are listed
        again in appendix A7. When an investor challenges a number in the deck, trace it here first, then to the
        Assumptions sheet in FluxMuse_Financial_Model.xlsx, where each input sits in its own cell with the
        Conservative, Base and Upside values side by side. The inputs to replace with live data first are the
        pay-at-sign-up rates, the Free upgrade rate and sign-up volume. Source: model_summary.json →
        key_assumptions[{idxs[0]}–{idxs[-1]}]; Financial_Model_Notes.md §4 and §11.""")
        slides.append(s)
    return slides


def a_customers(prs):
    s = new_slide(prs)
    header(s, f"Appendix A2 · {PROJ}", "Paying workspaces by segment and market")
    chart(s, "customers_by_segment", (MX, 1.75, 5.95, 3.4), alt="Paying workspaces by segment FY1 to FY5")
    chart(s, "customers_by_region", (6.78, 1.75, 5.95, 3.4), alt="Paying workspaces by market, monthly")
    f5 = A[4]
    seg, mk = f5["ending_customers_by_segment"], f5["ending_customers_by_market"]
    caption(s, MX, 5.25, 5.95, 0.9, f"By segment, FY5: Solo {num(seg['Solo'])} · SMEs {num(seg['SMEs'])} · Agencies "
            f"{num(seg['Agencies'])} · Corporate {num(seg['Corporate'])} · Enterprise (Custom) "
            f"{num(seg['Enterprise'])}. Total {num(f5['ending_paying_workspaces'])}.", size=12)
    caption(s, 6.78, 5.25, 5.95, 0.9, f"By market, Sep 2031: South Africa {num(mk['South Africa'])} · Nigeria "
            f"{num(mk['Nigeria'])} · Kenya {num(mk['Kenya'])} · Ghana {num(mk['Ghana'])} · 19 USD markets "
            f"{num(mk['Rest of Africa (USD)'])}. Outside South Africa, all pending payment accounts.", size=12)
    notes(s, f"""Two views of the same projected customer base. By segment, solo sellers and SMEs make up almost all
    workspaces, with {num(seg['Agencies'])} agency partners, {num(seg['Corporate'])} Corporate customers and
    {num(seg['Enterprise'])} Custom customers by FY5. By market, South Africa stays the core with
    {num(mk['South Africa'])} workspaces at the end of FY5. Every other market waits for its payment accounts and
    MRR gate, starting with Nigeria in {LAUNCH['Nigeria']} in the base case. There are no customers today; these
    are projections. Sources: model_summary.json → annual[].ending_customers_by_segment and
    ending_customers_by_market; Financial_Model_Notes.md §1.""")
    return s


def a_pricing_zar(prs):
    s = new_slide(prs)
    header(s, "Appendix A3 · pricing (1 of 2) · ZAR", "Nine plans in three bands, in rands")
    pic(s, "infographics/pricing-tiers.png", MX, 1.55, CW, 5.35, crop=(0, 0.2, 0, 0), align="t",
        alt="Nine plans in three bands: Small (Free, Nano, Micro), Medium (Starter, Growth, Scale), Enterprise "
        "(Corporate, Agency, Custom)")
    zar = PT["zar_list_monthly"]
    fm = PT["founding_member_first_2_bills_zar"]
    notes(s, f"""The full rand price list as live in the product. Small: Free, a permanent plan with no card, Nano
    {rn(zar['Nano'])} and Micro {rn(zar['Micro'])}. Medium: Starter {rn(zar['Starter'])}, Growth {rn(zar['Growth'])}
    and Scale {rn(zar['Scale'])}. Enterprise: Corporate {rn(zar['Corporate'])}, Agency {rn(zar['Agency'])} and
    Custom by consultation, which the model books from {rn(zar['Custom'])}. Annual is ten times monthly. Founding
    Members in South Africa pay, for example, {rn(fm['Nano'])} or {rn(fm['Growth'])} for their first two monthly
    bills. Agencies resell at partner wholesale of {rn(PT['partner_wholesale_monthly']['ZAR'])}. We never quote AI
    credit allowances per plan. Sources: CURRENT_OFFER.md §1; model_summary.json → price_tables.""")
    return s


def a_pricing_local(prs):
    s = new_slide(prs)
    header(s, "Appendix A3 · pricing (2 of 2) · priced, not yet on sale", "Local-currency and USD prices")
    lm, ws = PT["local_monthly"], PT["partner_wholesale_monthly"]
    rows = [[hdr_cell("Plan / month", align="l", size=12)] + [hdr_cell(t, size=12) for t in ["NGN", "KES", "GHS", "USD"]]]
    for t in ["Nano", "Micro", "Starter", "Growth", "Scale", "Corporate", "Agency"]:
        fill = TINT if t == "Growth" else PAPER
        vals = [f"₦{lm['NGN'][t]:,}", f"KSh {lm['KES'][t]:,}", f"GH₵ {lm['GHS'][t]:,}", f"${lm['USD'][t]:,}"]
        rows.append([{"text": t, "bold": True, "fill": fill, "size": 12}] + [{"text": v, "fill": fill, "size": 12} for v in vals])
    rows.append([{"text": "Custom (from)", "bold": True, "size": 12}] +
                [{"text": v, "size": 12} for v in [f"₦{lm['NGN']['Custom']:,}", f"KSh {lm['KES']['Custom']:,}",
                                                   f"GH₵ {lm['GHS']['Custom']:,}", f"${lm['USD']['Custom']:,}"]])
    W = {"fill": NIGHT_CARD, "color": PAPER, "bold": True, "line": None, "size": 12}
    rows.append([dict(W, text="Partner wholesale", color=ORANGE), dict(W, text=f"₦{ws['NGN']:,}"),
                 dict(W, text=f"KSh {ws['KES']:,}"), dict(W, text=f"GH₵ {ws['GHS']:,}"), dict(W, text=f"${ws['USD']:,}")])
    table(s, MX, 1.62, [2.6, 2.0, 2.0, 2.0, 1.6], [0.4] * 10, rows, size=12, label="regional")
    caption(s, MX, 5.8, CW, 0.9, "Not on sale: checkout outside South Africa waits for the Fincra and pawaPay "
            "accounts. Prices at FX parity with the rand, annual = 10× monthly, reviewed quarterly. Botswana and "
            "Namibia: coming soon, no prices.", size=12)
    fxs = PT["fx_price_setting"]
    notes(s, f"""Local-currency prices for Nigeria, Kenya and Ghana, and USD for the 19 other markets our payment
    partners can reach. These are set in the product but not on sale: there is no paid checkout outside South
    Africa until the Fincra and pawaPay accounts are live. Prices were set at parity with the rand, using 1 ZAR =
    ₦{fxs['NGN_per_ZAR']}, KSh {fxs['KES_per_ZAR']} and GH₵ {fxs['GHS_per_ZAR']}. The product has no regional
    wholesale rows, so the model uses the Corporate local prices for partner wholesale, a point still to confirm.
    Prices are reviewed quarterly, which is the main FX control in appendix A5. Sources: CURRENT_OFFER.md §3;
    model_summary.json → price_tables; Financial_Model_Notes.md §4.""")
    return s


def a_rails(prs):
    s = new_slide(prs)
    header(s, "Appendix A4 · payment rails", "What is live, and what is still pending")
    pic(s, "infographics/payment-rails-matrix.png", MX, 1.55, CW, 5.35, crop=(0, 0.19, 0, 0.0), align="t",
        alt="Payment rails by country: South Africa live on Paystack, with Yoco and Ozow for FluxMuse billing; "
        "pawaPay and Fincra contracted, accounts pending; Botswana and Namibia coming soon")
    notes(s, """This matrix shows payment status by country, live and pending. South Africa is the only country
    open for paid sign-up: Paystack is live there, and Yoco and Ozow run FluxMuse's own subscription billing.
    Nigeria, Kenya and Ghana are priced in local currency but not yet on sale. pawaPay and Fincra are contracted
    for expansion, with accounts pending, and would cover most of the other countries shown. Botswana and Namibia
    have no provider yet. We do not claim coverage that is not live. Contracts and account status belong in the
    data room. Sources: CURRENT_OFFER.md §3 and §4; infographic payment-rails-matrix.""")
    return s


def a_fx(prs):
    s = new_slide(prs)
    header(s, f"Appendix A5 · FX shock · model {M['version']}", "ZAR 15% stronger vs NGN, KES, GHS and USD")
    chart(s, "fx_shock_sensitivity", (MX, 1.62, 7.6, 3.44), alt="FX shock: base vs ZAR +15% with and without repricing")
    cases = [FX["Base"], FX["ZAR 15% stronger (repricing on)"], FX["ZAR 15% stronger (no repricing)"]]
    c = lambda t, **k: dict({"text": t, "size": 12}, **k)
    rows = [[hdr_cell("Base case", align="l", size=12), hdr_cell("Base", size=12), hdr_cell("+15%, repricing", size=12),
             hdr_cell("+15%, none", size=12)],
            [c("FY3 revenue", bold=True)] + [c(rm(x["fy3_revenue_zar"])) for x in cases],
            [c("FY5 revenue", bold=True)] + [c(rm(x["fy5_revenue_zar"])) for x in cases],
            [c("FY3 EBITDA", bold=True)] + [c(rm(x["fy3_ebitda_zar"])) for x in cases],
            [c("FY5 EBITDA", bold=True)] + [c(rm(x["fy5_ebitda_zar"])) for x in cases],
            [c("Cash low", bold=True)] + [c(f"{rm(x['min_post_seed_cash_zar'], 2)} {x['min_post_seed_cash_month']}")
                                          for x in cases],
            [c(f"Passes on {SEED_M}", bold=True)] + [c("Yes" if x["profitable_on_seed_alone"] else "No", bold=True,
                                                       color=INK if x["profitable_on_seed_alone"] else DEEP) for x in cases]]
    table(s, 8.4, 1.62, [1.15, 1.06, 1.06, 1.06], [0.95, 0.56, 0.56, 0.56, 0.56, 0.8, 0.6], rows, size=12, label="fx")
    nr = FX["ZAR 15% stronger (no repricing)"]
    text(s, MX, 5.3, 7.6, 1.35, f"The shock starts in Apr 2029, after Nigeria, Kenya and Ghana open in the model. "
         f"With repricing the plan passes. Without it, FY5 EBITDA falls to {rm(nr['fy5_ebitda_zar'])} and cash drops "
         f"below the {rm(CASH['min_cash_buffer_zar'])} buffer.", size=14, role="body")
    notes(s, f"""This is the currency stress test. From April 2029 the rand is assumed 15% stronger against the
    naira, shilling, cedi and dollar, so every local price is worth less in rand. With quarterly repricing the cash
    low is {rm(FX['ZAR 15% stronger (repricing on)']['min_post_seed_cash_zar'], 2)} and the plan still passes.
    Without repricing, FY5 revenue moves {rm(nr['change_vs_base_zar']['fy5_revenue_zar'])}, FY5 EBITDA turns
    negative and the cash low of {rm(nr['min_post_seed_cash_zar'], 2)} breaks the buffer, so the plan fails.
    Repricing discipline is the main FX control. Sources: model_summary.json → fx_shock; Financial_Model_Notes.md
    §6.""")
    return s


def a_founding(prs):
    s = new_slide(prs)
    fmd = M["founding_member"]
    header(s, f"Appendix A6 · launch discount cost · {PROJ}", "Founding Member costs little")
    chart(s, "founding_member_discount_cost", (MX, 1.62, 7.6, 3.44), alt="Founding Member discount cost by year")
    oc = fmd["option_comparison"]
    rows = [[hdr_cell("Launch offer", align="l"), hdr_cell("FY1–FY3 cost"), hdr_cell("Cash low")]]
    for k, lab in [("Founding Member (default)", "Founding Member"), ("None", "No offer")]:
        fill = TINT if k.startswith("Founding") else PAPER
        rows.append([{"text": lab, "bold": True, "fill": fill},
                     {"text": rk(oc[k]["discount_cost_fy1_fy3_zar"]) if oc[k]["discount_cost_fy1_fy3_zar"] else "R0",
                      "fill": fill}, {"text": rm(oc[k]["min_post_seed_cash_zar"], 2), "fill": fill}])
    table(s, 8.4, 1.62, [2.3, 1.05, 0.98], [0.72, 0.5, 0.5], rows, size=14, label="fm")
    text(s, 8.4, 3.6, 4.33, 1.4, "Live since 1 Oct for South African sign-ups. The model ends it in Mar 2027, "
         "a proposed date the founder has not set.", size=14, role="body")
    dc = fmd["discount_cost_by_fy_zar"]
    text(s, MX, 5.3, 7.6, 1.35, f"Founding Member costs {rk(dc['FY1'], 0)} in FY1 and nothing after. The "
         f"+{fmd['window_signup_uplift_pct']}% sign-up uplift while it runs is an assumption to measure.", size=14,
         role="body")
    notes(s, f"""Investors often ask whether the launch discount hurts the plan. It does not. Founding Member is 30%
    off the first two monthly bills for South African Solo and SME sign-ups. It is a discount, not a free period.
    It costs {rk(dc['FY1'], 0)} of revenue, all in FY1. Because the model assumes a
    {fmd['window_signup_uplift_pct']}% sign-up uplift while it runs, it leaves slightly more cash than no offer.
    That uplift is unproven, so we will measure it. No offer is modelled for Nigeria, Kenya or Ghana. Sources:
    model_summary.json → founding_member; CURRENT_OFFER.md §1; Financial_Model_Notes.md §4.""")
    return s


def a_confirmations(prs):
    s = new_slide(prs)
    header(s, "Appendix A7 · internal only · hide before sending", "Founder confirmations still open")
    items = M["founder_confirmations_needed"]
    hs = [0.2 * max(1, math.ceil(len(t) / 58)) + 0.15 for t in items]
    half = min(range(1, len(items)), key=lambda k: max(sum(hs[:k]), sum(hs[k:])))
    for c, chunk in enumerate([items[:half], items[half:]]):
        off = 0 if c == 0 else half
        heights = hs[:half] if c == 0 else hs[half:]
        rows = [[{"text": str(off + i + 1), "bold": True, "size": 12, "color": DEEP},
                 {"text": t, "size": 12, "align": "l"}] for i, t in enumerate(chunk)]
        table(s, MX + c * (5.95 + 0.233), 1.55, [0.45, 5.5], heights, rows, size=12, label=f"confirm{c}")
        assert sum(heights) < 5.4, f"A7 column {c} is {sum(heights):.2f} in tall"
    notes(s, """Internal slide: hide or delete it before the deck goes to any investor. These are the model inputs
    and decisions the founder still has to confirm, copied from the model summary. The most urgent are opening
    cash and the pre-seed bridge, the seed close month and instrument, the pay-at-sign-up and Free upgrade rates,
    and the Founding Member end date. Market sizing must be verified before external use. Once a decision is made,
    update the Assumptions sheet, rebuild the model, rebuild this deck with build_investor_deck.py and rerun the QA
    script. Source: model_summary.json → founder_confirmations_needed; Financial_Model_Notes.md §12.""")
    return s


# ================================================================ BUILD
def set_theme_fonts(prs):
    for rel in prs.slide_master.part.rels.values():
        if rel.reltype.endswith("/theme"):
            tp = rel.target_part
            blob = tp.blob
            new = re.sub(rb'(<a:majorFont>\s*<a:latin typeface=")[^"]*"', rb'\1Poppins"', blob)
            new = re.sub(rb'(<a:minorFont>\s*<a:latin typeface=")[^"]*"', rb'\1Inter"', new)
            if hasattr(tp, "_element"):
                tp._element = etree.fromstring(new)
            else:
                tp._blob = new


def build():
    OUT.mkdir(parents=True, exist_ok=True)
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(SW), Inches(SH)
    set_theme_fonts(prs)
    prs.core_properties.title = f"FluxMuse investor pitch deck: {SEED_M} seed"
    prs.core_properties.author = "Fluxmuse Pty Ltd"
    prs.core_properties.subject = "Seed round, confidential"
    core = [s_title, s_problem, s_solution, s_product, s_market, s_model, s_gtm, s_payments, s_traction,
            s_competition, s_unit, s_projections, s_profit, s_scenarios, s_risks, s_ask, s_milestones, s_team, s_close]
    slides = [fn(prs) for fn in core]
    slides.append(a_divider(prs, [("A1", "Key model assumptions"), ("A2", "Paying workspaces by segment and market"),
                                  ("A3", "Pricing: nine plans in rands; local prices, not yet on sale"),
                                  ("A4", "Payment rails by country: live and pending"), ("A5", "FX shock sensitivity"),
                                  ("A6", "Founding Member discount cost"),
                                  ("A7", "Founder confirmations (internal: hide before sending)")]))
    slides += a_assumptions(prs)
    for fn in (a_customers, a_pricing_zar, a_pricing_local, a_rails, a_fx, a_founding, a_confirmations):
        slides.append(fn(prs))
    for i, s in enumerate(slides):
        if i > 0:
            chrome(s, i + 1, getattr(s, "_fm_dark", False))
    prs.save(DECK)
    manifest = {"built": date.today().isoformat(), "model_version": M["version"], "model_date": M["model_date"],
                "deck": DECK.name, "slides": len(prs.slides), "core_slides": len(core), "images": sorted(USED)}
    (HERE / "build_manifest.json").write_text(json.dumps(manifest, indent=2))
    print(f"built {DECK.name}: {len(prs.slides)} slides ({len(core)} core)")


if __name__ == "__main__":
    build()
