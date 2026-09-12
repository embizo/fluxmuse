#!/usr/bin/env python3
"""Build the FluxMuse investor pitch deck (R25M seed).

House style, primitives and icons are copied from ../brand_deck/build_deck.py so both decks read as one
family. Every financial number is read from 06_Financial_Model/model_summary.json (model v2) at build
time; product, pricing and market facts come from 00_FACTS_AND_ASSUMPTIONS.md. Charts and infographics
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
PROJ = "Projection (model v2, base case)"

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
def s_title(prs):
    s = new_slide(prs, dark=True)
    pic(s, "brand/fluxmuse-logo-dark.png", MX, 0.55, 2.6, 0.9, align="tl", alt="FluxMuse logo")
    text(s, MX, 2.0, 6.6, 0.3, "FLUXMUSE · INVESTOR PRESENTATION", size=13, bold=True, color=ORANGE,
         role="eyebrow", spc=150)
    text(s, MX, 2.38, 6.5, 2.2, "AI marketing team + WhatsApp commerce for African businesses", size=34,
         font=HEAD, bold=True, color=PAPER, role="title", lsp=0.95)
    g = gid()
    box(s, MX, 4.8, 3.3, 0.58, fill=ORANGE, shape="round", radius=0.29, role="chip", group=g)
    text(s, MX, 4.8, 3.3, 0.58, f"Seed round · R{BASE['seed_zar'] / 1e6:.0f}M", size=18, bold=True, color=NIGHT,
         align="c", anchor="m", role="chip", group=g)
    text(s, MX, 5.65, 6.5, 0.36, [[("[[DATE]]", {"color": PAPER, "bold": True}),
                                  ("  ·  Confidential", {"color": MUTED_DARK})]], size=16, role="placeholder")
    text(s, MX, 6.1, 6.5, 0.3, "Fluxmuse Pty Ltd · South Africa · fluxmuse.ai", size=14, color=MUTED_DARK, role="body")
    pic(s, "screenshots/composites/hero-laptop-phone_night.png", 7.3, 1.3, 5.6, 5.0,
        crop=(0.02, 0.09, 0.06, 0.02), alt="FluxMuse on a laptop and an order confirmed inside WhatsApp on a phone")
    notes(s, f"""Thank you for your time. FluxMuse, built by Fluxmuse Pty Ltd in South Africa, gives African small
    businesses an AI marketing team and lets them sell and get paid inside WhatsApp. We are raising a
    R25M seed round, about US$1.35M, and the model shows this round alone carries the company to
    profitability, with no Series A required. Every financial figure in this deck comes from financial
    model v2, dated 11 September 2026, and every projection is labelled. Market figures are estimates with
    sources. Sources: model_summary.json → seed_zar ({BASE['seed_zar']:,}) and seed_usd; model_summary.json →
    profitable_on_seed_alone. Replace [[DATE]] before sending and keep the Confidential marker.""")
    return s


def s_problem(prs):
    s = new_slide(prs)
    header(s, "The problem", "Sales happen in chat. The tools don't.")
    cards = [("chat", "Buyers already shop in chats",
              "They discover on social, then ask, order and pay in WhatsApp DMs that owners answer by hand."),
             ("megaphone", "No marketing capacity",
              "Owners post when they find time. A marketer or agency retainer is out of reach for many."),
             ("card", "Checkout breaks the chat",
              "External payment links lose buyers, and checkout often lacks local options like instant EFT or mobile money.")]
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
    text(s, MX + 1.35, 5.62, CW - 1.75, 0.95, "FluxMuse closes the loop: an AI marketing team that fills the chat, "
         "and checkout that gets paid inside it.", size=19, font=HEAD, bold=True, color=PAPER, anchor="m",
         role="card", group=g)
    notes(s, """Start with how small businesses in South Africa actually sell. Buyers find them on Facebook,
    Instagram or a WhatsApp status, then ask questions, order and pay in chat, and the owner handles every
    message by hand. Owners rarely have the time or budget for marketing, so posting is inconsistent and agency
    retainers are out of reach for many. When the sale moves to an external payment link, buyers drop off,
    especially where checkout lacks local ways to pay such as instant EFT or mobile money. We deliberately show
    no market statistics on this slide: the framing comes from our segment work in 00_FACTS_AND_ASSUMPTIONS.md
    §4b, and the Gauteng pilot will quantify it from December 2026.""")
    return s


def s_solution(prs):
    s = new_slide(prs, dark=True)
    header(s, "The solution", "An AI team that markets and sells in chat", dark=True)
    pic(s, "infographics/how-fluxmuse-works_dark.png", MX, 1.62, 7.3, 3.5, crop=(0.08, 0.24, 0.08, 0.06),
        align="tl", alt="Loop: Plan (Strategist), Create (Creator), Publish (Publisher), Sell (WhatsApp commerce), "
        "Learn (Analyst)")
    rows = [("sparkles", "AI marketing team: Strategist, Creator, Publisher and Analyst, plus 23 specialist agents"),
            ("cart", "WhatsApp commerce: catalog, cart and checkout in chat, on 5 local payment rails")]
    for i, (ic, t) in enumerate(rows):
        y = 5.35 + i * 0.72
        g = icon(s, ic, "ink", MX + 0.3, y + 0.3, 0.58, circle=ORANGE)
        text(s, MX + 0.78, y, 6.55, 0.6, t, size=15, color=PAPER, anchor="m", role="body", group=g)
    pic(s, "screenshots/composites/hero-laptop-phone_night.png", 8.2, 1.62, 4.53, 3.5,
        crop=(0.02, 0.09, 0.06, 0.02), alt="FluxMuse website on a laptop and an order confirmed inside WhatsApp")
    text(s, 8.2, 5.35, 4.53, 1.3, "Live today: WhatsApp Cloud API, Facebook Pages, Messenger, email, SMS, USSD, "
         "web chat and landing pages. Instagram: in Meta App Review.", size=14, color=MUTED_DARK, role="body")
    notes(s, """FluxMuse is one loop. The Strategist plans goals, channel mix and budget. The Creator writes copy
    and images in isiZulu, Afrikaans, Pidgin, Swahili, English and more. The Publisher schedules across social,
    WhatsApp, email, SMS and USSD. Buyers browse a catalog, build a cart and pay inside WhatsApp, and the Analyst
    feeds orders and data back into the next plan. Behind the four core agents sit 23 specialist Flux agents.
    The phone on the right is our demo store confirming an order in the chat. Everything named here is live,
    except Instagram, which is in Meta App Review. Sources: 00_FACTS_AND_ASSUMPTIONS.md §1 (shipped capability,
    Meta approvals); assets how-fluxmuse-works_dark and hero-laptop-phone_night.""")
    return s


def s_product(prs):
    s = new_slide(prs)
    header(s, "Product", "Live today, and what's in review")
    pic(s, "screenshots/composites/checkout-in-chat-3-phones.png", MX, 1.62, 5.4, 3.1,
        crop=(0.12, 0.205, 0.12, 0.02), align="tl", alt="WhatsApp checkout demo: catalog, cart, order confirmed")
    caption(s, MX, 4.8, 5.4, 0.5, "WhatsApp checkout demo: catalog, cart, order confirmed in chat "
            "(simulated demo store, no real payment).", size=12)
    stats = [("4", "core AI agents"), ("23", "specialist agents"), ("5", "payment rails")]
    sw = (5.4 - 0.3) / 3
    for i, (v, l) in enumerate(stats):
        tile(s, MX + i * (sw + 0.15), 5.4, sw, 1.45, v, l, fill=TINT, vsize=24)
    LIVE = {"fill": TINT, "color": DEEP, "bold": True}
    REV = {"fill": MIST, "color": INK, "bold": True}
    SOON = {"fill": MIST, "color": MUTED, "bold": True}
    data = [("AI workforce", "4 core agents + 23 specialists, Agent Marketplace", "Live", LIVE),
            ("WhatsApp commerce", "Cloud API, Flows, catalog, cart, orders, recovery", "Live", LIVE),
            ("Payments", "Yoco, Ozow, Paystack, pawaPay, Fincra", "Live Sept 2026", LIVE),
            ("Channels", "Facebook Pages, Messenger, email, SMS, USSD, web chat", "Live", LIVE),
            ("Growth & integrations", "CRM, loyalty, Shopify, WooCommerce, HubSpot, API", "Live", LIVE),
            ("Instagram", "Publishing, comments and DMs (Meta permissions)", "In review", REV),
            ("More social networks", "TikTok, LinkedIn, X, YouTube, Threads, Pinterest", "Coming soon", SOON)]
    rows = [[hdr_cell("Layer", align="l"), hdr_cell("What's included", align="l"), hdr_cell("Status")]]
    for a, b, st, sty in data:
        rows.append([{"text": a, "bold": True}, {"text": b, "align": "l"}, dict(sty, text=st)])
    table(s, 6.3, 1.62, [1.85, 3.33, 1.25], [0.45] + [0.68] * 7, rows, size=14, label="stack")
    notes(s, """This is the product as it stands. On the left are three real screens from our WhatsApp checkout
    demo: browse the catalog, review the cart, and see the order confirmed in the chat. The demo is simulated,
    so no money moves. On the right is the platform stack with an honest status column. The AI workforce,
    WhatsApp commerce, channels, growth tools and integrations are live. All five payment rails are live in
    September 2026, with pawaPay and Fincra from 14 September. Instagram publishing, comments and DMs are in
    Meta App Review, and the other social networks are coming soon through our social adapters work. Sources:
    00_FACTS_AND_ASSUMPTIONS.md §1 and §3; assets/ASSETS_INDEX.md for the approved screenshots.""")
    return s


def s_market(prs):
    s = new_slide(prs)
    header(s, "Why Africa, why now · market estimates", "SMBs already sell and pay on mobile")
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
    caption(s, 5.95, 5.35, 6.78, 1.0, f"TAM: IFC / World Bank est. SAM and SOM: FluxMuse planning estimates "
            f"(facts §5). The base case reaches {num(BASE['fy5_paying_workspaces'])} paying workspaces in FY5, "
            f"{ms['model_fy5_workspaces_pct_of_som']}% of SOM ({PROJ.lower()}). Verify all estimates before "
            "external use.", size=12)
    notes(s, f"""Why Africa, and why now. WhatsApp is where commerce already happens: more than 90% of internet
    users in South Africa and Nigeria use it (DataReportal 2025 est.), and Sub-Saharan Africa handles about 70%
    of global mobile money value (GSMA est.). There are roughly 44 million MSMEs in the region. We size a
    serviceable market of about 3.5 million digitally active SMBs in our 23 rail-covered countries that can pay
    at least US$25 a month, and a five-year obtainable share of 0.5%, or 17,500 paying workspaces. The base case
    needs {num(BASE['fy5_paying_workspaces'])}, about half. These are estimates to verify before external use.
    Sources: 00_FACTS_AND_ASSUMPTIONS.md §5; model_summary.json → market_sizing.""")
    return s


def s_model(prs):
    s = new_slide(prs)
    header(s, "Business model · fixed prices per market", "Subscriptions, priced for each market")
    lm, ws = PT["local_monthly"], PT["partner_wholesale_monthly"]
    zar = PT["zar_list_monthly"]
    rows = [[hdr_cell("Monthly", align="l"), hdr_cell("ZAR"), hdr_cell("NGN"), hdr_cell("KES"), hdr_cell("GHS"),
             hdr_cell("USD")]]
    for t in ["Starter", "Growth", "Scale", "Agency"]:
        fill = TINT if t == "Growth" else PAPER
        lab = t
        rows.append([{"text": lab, "bold": True, "fill": fill}, {"text": rn(zar[t]), "fill": fill, "bold": True},
                     {"text": f"₦{lm['NGN'][t]:,}", "fill": fill}, {"text": f"KSh {lm['KES'][t]:,}", "fill": fill},
                     {"text": f"GH₵ {lm['GHS'][t]:,}", "fill": fill}, {"text": f"${lm['USD'][t]:,}", "fill": fill}])
    W = {"fill": NIGHT_CARD, "color": PAPER, "bold": True, "line": None}
    rows.append([dict(W, text="Partner wholesale", color=ORANGE), dict(W, text=rn(ws["ZAR"])),
                 dict(W, text=f"₦{ws['NGN']:,}"), dict(W, text=f"KSh {ws['KES']:,}"), dict(W, text=f"GH₵ {ws['GHS']:,}"),
                 dict(W, text=f"${ws['USD']:,}")])
    table(s, MX, 1.62, [2.0, 1.0, 1.33, 1.35, 1.32, 0.85], [0.5] + [0.6] * 5, rows, size=14, label="pricing")
    chips = [("Annual = 10× monthly", 2.3), ("14-day free trial, no card", 2.8), ("Enterprise: inbound only", 2.45)]
    x = MX
    for t, wdt in chips:
        g = gid()
        box(s, x, 5.2, wdt, 0.5, fill=MIST, shape="round", radius=0.25, role="chip", group=g)
        text(s, x, 5.2, wdt, 0.5, t, size=14, bold=True, align="c", anchor="m", role="chip", group=g)
        x += wdt + 0.1
    fm = PT["founding_member_first_2_bills_zar"]
    g = gid("fm")
    box(s, MX, 5.9, 7.85, 0.95, fill=TINT, shape="round", radius=0.16, role="card", group=g)
    text(s, MX + 0.25, 5.98, 7.35, 0.8, [[("Founding Member launch offer: ", {"bold": True, "color": DEEP}),
                                          (f"30% off the first 2 monthly bills ({rn(fm['Starter'])} / "
                                           f"{rn(fm['Growth'])} / {rn(fm['Scale'])}) for sign-ups in a 60-day "
                                           "launch window. Not offered on Agency.", {})]],
         size=14, anchor="m", role="card", group=g)
    st = A[4]["revenue_by_stream_zar"]
    g = gid("streams")
    x0, w0 = 8.65, 4.08
    box(s, x0, 1.62, w0, 5.05, fill=MIST, shape="round", radius=0.2, role="card", group=g)
    text(s, x0 + 0.3, 1.82, w0 - 0.6, 0.28, "REVENUE STREAMS · FY5", size=12, bold=True, color=DEEP,
         role="eyebrow", group=g, spc=120)
    text(s, x0 + 0.3, 2.1, w0 - 0.6, 0.28, PROJ, size=12, color=MUTED, role="caption", group=g)
    items = [("Subscriptions (net)", rm(st["subscriptions"]), False),
             ("WhatsApp messaging", rm(st["whatsapp_messaging"]), False),
             ("AI-credit top-ups", rm(st["ai_credit_topups"]), False),
             ("Agency setup fees", rm(st["agency_setup_fees"]), False),
             ("Enterprise setup fees", rm(st["enterprise_setup_fees"]), False),
             ("Commerce fee (Base)", "R0", False),
             ("Total revenue", rm(A[4]["total_revenue_zar"]), True)]
    for i, (lab, v, bold) in enumerate(items):
        y = 2.52 + i * 0.5
        if bold:
            box(s, x0 + 0.3, y - 0.04, w0 - 0.6, 0.02, fill=SLATE, role="deco", group=g)
        text(s, x0 + 0.3, y, 2.4, 0.42, lab, size=15, bold=bold, anchor="m", role="card", group=g)
        text(s, x0 + 2.7, y, w0 - 3.0, 0.42, v, size=15, bold=True, align="r", anchor="m", role="card", group=g)
    caption(s, x0 + 0.3, 6.05, w0 - 0.6, 0.5, "Commerce fee (0.75% of checkout GMV) is Upside only and not in "
            "current pricing.", size=11).name = f"{g}|caption|"
    notes(s, f"""Revenue is mainly subscriptions. Four plans in rand, from Starter at R499 to Agency at R7,999,
    with fixed local price points in Nigeria, Kenya and Ghana and USD in the other 19 rail-covered markets, all
    set at parity and reviewed quarterly. Agencies buy the Agency tier at partner wholesale, R5,599 a month, and
    resell under their own brand. Annual plans are ten times monthly, every plan starts with a 14-day free trial,
    and Founding Member gives 30% off the first two monthly bills in a 60-day launch window. In FY5 the model
    books {rm(st['subscriptions'])} of net subscriptions out of {rm(A[4]['total_revenue_zar'])}. The commerce fee
    is excluded from Base. Sources: facts §2; model_summary.json → price_tables and
    annual[4].revenue_by_stream_zar.""")
    return s


def s_gtm(prs):
    s = new_slide(prs)
    header(s, "Go-to-market · South Africa first", "Three segments, one partner channel")
    zar = PT["zar_list_monthly"]
    cards = [("users", "Solo entrepreneurs", "Founder-run, 1–5 people", f"Starter {rn(zar['Starter'])} → Growth",
              "Self-serve trial, then Founding Member offer"),
             ("briefcase", "SMEs", "5–200 staff", f"Growth {rn(zar['Growth'])} → Scale",
              "Trial plus a guided onboarding call"),
             ("layers", "Agency partners", "Managing 5–50 SMB clients",
              f"Partner wholesale {rn(PT['partner_wholesale_monthly']['ZAR'])}",
              "Demo, pilot client, then reseller billing")]
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
    text(s, MX + 0.8, 4.1, CW - 1.0, 0.56, "Founding Member launch in South Africa: 1 Dec 2026 – 31 Jan 2027. "
         "Pilot brands convert on 1 Dec 2026.", size=15, bold=True, anchor="m", role="card", group=g)
    steps = [("1 · HOME MARKET", "South Africa", "Billed in ZAR · launch 1 Dec 2026", False),
             ("2 · WAVE 1, MRR-GATED", "Nigeria, Kenya, Ghana",
              f"Local currency · {LAUNCH['Nigeria'][:3]} / {LAUNCH['Kenya'][:3]} / {LAUNCH['Ghana'][:3]} 2028", False),
             ("3 · SELF-SERVE", "19 more countries", f"Billed in USD · from {LAUNCH['Rest of Africa (USD)']}", False),
             ("4 · COMING SOON", "Botswana & Namibia", "Opens once a payment rail covers them", True)]
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
    caption(s, MX, 6.74, CW, 0.26, f"Everywhere else: waitlist only (gated). Launch months: {PROJ.lower()}; each "
            "launch waits for its MRR gate.")
    notes(s, f"""We go to market in South Africa first, with three segments. Solo entrepreneurs start self-serve
    on Starter, SMEs start on Growth with a guided onboarding call, and agencies are our partner channel, buying
    the Agency tier at wholesale and serving their own clients under their brand. The Gauteng pilot converts on
    1 December 2026, when the Founding Member window opens, running to 31 January 2027. Nigeria, Kenya and Ghana
    then launch in {LAUNCH['Nigeria']}, {LAUNCH['Kenya']} and {LAUNCH['Ghana']} in the base case, each only once
    monthly recurring revenue clears its gate, followed by 19 USD markets self-serve from
    {LAUNCH['Rest of Africa (USD)']}. Botswana and Namibia are coming soon; everywhere else is waitlist only.
    Sources: facts §3 and §4b; model_summary.json → markets.launch_months.Base.""")
    return s


def s_payments(prs):
    s = new_slide(prs, dark=True)
    header(s, "Payments moat", "Local rails in 23 African countries", dark=True)
    pic(s, "infographics/payment-coverage-map_dark.png", MX, 1.62, 8.9, 4.1, crop=(0, 0.205, 0, 0), align="tl",
        alt="Tile map of 23 African countries covered by 5 live payment rails; Botswana and Namibia coming soon; "
        "40+ mobile money operators")
    cards = [("Collect and pay out", "Cards, instant EFT, bank transfer and mobile money"),
             ("Priced locally", "ZAR, NGN, KES and GHS; USD in 19 markets"),
             ("Gated by design", "No checkout where no rail can collect")]
    for i, (t, b) in enumerate(cards):
        y = 1.62 + i * 1.38
        g = gid("moat")
        box(s, 9.75, y, 2.98, 1.25, fill=NIGHT_CARD, shape="round", radius=0.16, role="card", group=g)
        text(s, 9.98, y + 0.14, 2.55, 0.38, t, size=16, font=HEAD, bold=True, color=ORANGE, role="card", group=g)
        text(s, 9.98, y + 0.52, 2.55, 0.62, b, size=14, color=PAPER, role="card", group=g)
    x = MX
    for r in ["Yoco", "Ozow", "Paystack", "pawaPay", "Fincra"]:
        g = gid()
        box(s, x, 5.98, 1.5, 0.5, fill=NIGHT_CARD, line="37424D", shape="round", radius=0.25, role="chip", group=g)
        text(s, x, 5.98, 1.5, 0.5, r, size=15, bold=True, color=PAPER, align="c", anchor="m", role="chip", group=g)
        x += 1.62
    caption(s, 8.8, 5.9, 3.93, 0.7, "All five live September 2026 (pawaPay and Fincra from 14 Sept). South Sudan "
            "and Zimbabwe: payouts only, gated.", dark=True, size=12)
    notes(s, """Payments are the moat. We have five rails: Yoco for cards and tap-to-pay and Ozow for instant EFT
    in South Africa, Paystack across six countries, pawaPay for mobile money in 20 countries with more than 40
    operators, and Fincra for collections and payouts. Together they cover 23 African countries, all live in
    September 2026. South Africa has four rails; Nigeria, Kenya and Ghana have three each. South Sudan and
    Zimbabwe are payouts only, so they stay gated until subscription collection is confirmed, and Botswana and
    Namibia are coming soon. Replicating this takes contracts, compliance and local pricing in every market.
    Sources: 00_FACTS_AND_ASSUMPTIONS.md §2 (gating) and §3 (rails); infographic payment-coverage-map_dark.""")
    return s


def s_traction(prs):
    s = new_slide(prs)
    header(s, "Traction & proof to date · no customer results yet", "Verified, approved, live and in pilot")
    tiles = [("checkCircle", "Verified Meta Tech Provider", "Business and access verification passed"),
             ("chat", "WhatsApp Business APIs approved", "Messaging and management permissions"),
             ("send", "Facebook Pages publisher live", "In-house; Instagram in App Review"),
             ("card", "5 payment rails live", "September 2026, 23 countries")]
    tw = (CW - 3 * 0.2) / 4
    for i, (ic, t, b) in enumerate(tiles):
        x = MX + i * (tw + 0.2)
        g = gid("proof")
        box(s, x, 1.62, tw, 2.25, fill=MIST, shape="round", radius=0.18, role="card", group=g)
        icon(s, ic, "deep", x + 0.55, 2.15, 0.64, circle=PAPER, group=g)
        text(s, x + 0.25, 2.6, tw - 0.5, 0.7, t, size=16, font=HEAD, bold=True, role="card", group=g)
        text(s, x + 0.25, 3.3, tw - 0.5, 0.52, b, size=14, color=MUTED, role="card", group=g)
    g = gid("pilot")
    box(s, MX, 4.1, 7.4, 2.58, fill=TINT, shape="round", radius=0.2, role="card", group=g)
    text(s, MX + 0.35, 4.3, 6.7, 0.28, "GAUTENG PILOT · UNDERWAY", size=12, bold=True, color=DEEP, role="eyebrow",
         group=g, spc=150)
    text(s, MX + 0.35, 4.62, 6.7, 0.45, "12 brands: solo entrepreneurs, SMEs and agencies", size=18, font=HEAD,
         bold=True, role="card", group=g)
    box(s, MX + 1.3, 5.52, 4.8, 0.04, fill=ORANGE, role="deco", group=g)
    marks = [("Sept 2026", "Pilot starts"), ("30 Nov 2026", "Pilot ends"), ("Dec 2026", "Results + first conversions")]
    for i, (d, l) in enumerate(marks):
        cx = MX + 1.3 + i * 2.4
        box(s, cx - 0.12, 5.42, 0.24, 0.24, fill=ORANGE if i == 2 else PAPER, line=ORANGE, lw=2, shape="oval",
            role="deco", group=g)
        text(s, cx - 1.1, 5.76, 2.2, 0.8, [{"runs": d, "bold": True, "color": DEEP if i == 2 else INK}, l],
             size=14, align="c", role="card", group=g)
    g = gid("kpi")
    box(s, 8.2, 4.1, 4.53, 2.58, fill=NIGHT, shape="round", radius=0.2, role="card", group=g)
    text(s, 8.5, 4.3, 3.95, 0.28, "KPIS WE TRACK", size=12, bold=True, color=ORANGE, role="eyebrow", group=g, spc=150)
    text(s, 8.5, 4.64, 3.95, 1.25, "Brands onboarded, WhatsApp conversations, orders and GMV, content published, "
         "time saved, conversion uplift, NPS", size=14, color=PAPER, role="card", group=g)
    text(s, 8.5, 5.98, 3.95, 0.55, "Published in December 2026, only with each brand's consent.", size=12,
         color=MUTED_DARK, role="caption", group=g)
    notes(s, """Here is what is real today, and we are careful not to overstate it. Fluxmuse Pty Ltd has passed
    Meta Business Verification and Access Verification as a Tech Provider. Meta has approved WhatsApp Business
    messaging and management, plus Pages messaging. Our in-house publisher is live for Facebook Pages, with
    Instagram still in App Review. All five payment rails are live in September 2026. A 12-brand pilot is running
    in Gauteng until 30 November 2026, tracking conversations, orders and GMV, content, time saved, conversion and
    NPS. We report no customer counts, revenue or results until pilot data exists with consent, in December 2026.
    Sources: facts §1 and §6; 07_Case_Studies/Gauteng_Pilot_Case_Studies.md; infographic gauteng-pilot.""")
    return s


def s_competition(prs):
    s = new_slide(prs)
    header(s, "Competition & positioning · qualitative view", "Where FluxMuse sits")
    x0, y0, w, h = 1.05, 2.0, 5.2, 4.2
    g = gid("mx")
    box(s, x0, y0, w, h, fill=MIST, shape="round", radius=0.12, role="deco", group=g)
    box(s, x0 + w / 2 - 0.01, y0 + 0.15, 0.02, h - 0.3, fill="D5D9DE", role="deco", group=g)
    box(s, x0 + 0.15, y0 + h / 2 - 0.01, w - 0.3, 0.02, fill="D5D9DE", role="deco", group=g)
    text(s, x0, 1.62, w, 0.3, "↑ African payment rails & local pricing", size=13, bold=True, color=SLATE,
         role="caption")
    text(s, x0, 6.28, w, 0.3, "AI marketing + commerce in one platform →", size=13, bold=True, color=SLATE,
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
    cats = [("Global social media tools", "Strong at publishing and analytics. FluxMuse adds selling and getting "
             "paid in chat, priced locally."),
            ("WhatsApp BSPs & chatbot vendors", "Strong at messaging infrastructure. FluxMuse adds the AI team that "
             "plans and creates the marketing."),
            ("E-commerce platforms", "Strong at storefronts and catalogs. FluxMuse brings the sale into the chat, on "
             "local rails."),
            ("Local agencies", f"Local knowledge and service. FluxMuse makes them partners, white-label at "
             f"{rn(PT['partner_wholesale_monthly']['ZAR'])}/mo wholesale.")]
    for i, (t, b) in enumerate(cats):
        y = 1.62 + i * 1.28
        g = gid("cat")
        box(s, 6.75, y, 5.98, 1.16, fill=PAPER, line=LINE, lw=1.25, shape="round", radius=0.16, role="card", group=g)
        text(s, 7.05, y + 0.12, 5.38, 0.36, t, size=16, font=HEAD, bold=True, role="card", group=g)
        text(s, 7.05, y + 0.5, 5.38, 0.58, b, size=14, color=SLATE, role="card", group=g)
    notes(s, """We position against categories, not named companies, and this map is our qualitative view, not
    measured data. Global social media tools are strong at publishing and analytics. WhatsApp business solution
    providers and chatbot vendors are strong at messaging infrastructure. E-commerce platforms are strong at
    storefronts. Local agencies bring service and local knowledge. FluxMuse aims for the top right: African
    payment rails and local pricing on one axis, AI marketing and commerce in one platform on the other. We treat
    agencies as a channel: they resell FluxMuse at the R5,599 partner wholesale price. On defensibility, the
    answer is the combination of local rails, local pricing and the agency channel. Sources: facts §1 to §3.""")
    return s


def s_unit(prs):
    s = new_slide(prs)
    bl, seg = UE["blended"], UE["by_segment"]
    header(s, f"Unit economics · FY3 · {PROJ}", f"Blended LTV:CAC {bl['ltv_to_cac']}x, payback "
           f"{bl['cac_payback_months']} months")
    chart(s, "unit_economics", (MX, 1.62, 7.9, 3.62), alt="LTV and CAC by segment in FY3: Solo, SMEs, Agencies, "
          "Enterprise")
    g = gid("solo")
    box(s, MX, 5.42, 7.9, 1.25, fill=MIST, shape="round", radius=0.16, role="card", group=g)
    text(s, MX + 0.3, 5.5, 7.3, 1.1, f"Solo is the thinnest segment ({seg['Solo']['ltv_to_cac']}x LTV:CAC, "
         f"{seg['Solo']['monthly_churn_pct']:.1f}% monthly churn), so its conversion and churn are the first inputs "
         f"we replace with pilot data. SMEs ({seg['SMEs']['ltv_to_cac']}x) and agencies "
         f"({seg['Agencies']['ltv_to_cac']}x) carry the blend.", size=14, anchor="m", role="card", group=g)
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
    notes(s, f"""Unit economics are shown for FY3, when the base case is at steady scale. Blended LTV is
    {rn(bl['ltv_zar'])} against a blended CAC of {rn(bl['cac_zar'])}, so LTV to CAC is {bl['ltv_to_cac']} times,
    and CAC pays back in {bl['cac_payback_months']} months. LTV is ARPA times software gross margin of
    {bl['software_gross_margin_pct']}%, divided by monthly churn. Solo is the thinnest segment at
    {seg['Solo']['ltv_to_cac']} times, SMEs are {seg['SMEs']['ltv_to_cac']} and agencies
    {seg['Agencies']['ltv_to_cac']}. The blend improves from {A[0]['unit_economics']['ltv_to_cac']} times in FY1
    to {A[4]['unit_economics']['ltv_to_cac']} in FY5. {PROJ}. Sources: model_summary.json →
    unit_economics_fy3.blended and by_segment; annual[0], annual[2] and annual[4].unit_economics and
    software_gross_margin_pct.""")
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
    notes(s, f"""This is the five-year base case, net of launch discounts. Revenue grows {rev} from FY1 to FY5,
    about US${A[4]['total_revenue_usd'] / 1e6:.2f}M in the final year. Gross margin rises from
    {pct(A[0]['gross_margin_pct'])} to {pct(A[4]['gross_margin_pct'])} as WhatsApp pass-through becomes a smaller
    share. EBITDA is negative for two years, {rm(A[0]['ebitda_zar'])} and {rm(A[1]['ebitda_zar'])}, turns positive
    at {rm(A[2]['ebitda_zar'])} in FY3 and reaches {rm(A[4]['ebitda_zar'])}, a {A[4]['ebitda_margin_pct']}% margin,
    in FY5. Paying workspaces grow from {num(A[0]['ending_paying_workspaces'])} to
    {num(A[4]['ending_paying_workspaces'])}. {PROJ}. Sources: model_summary.json → annual[0–4].total_revenue_zar,
    gross_margin_pct, ebitda_zar, ebitda_margin_pct, ending_paying_workspaces, subscription_arr_zar.""")
    return s


def s_profit(prs):
    s = new_slide(prs)
    header(s, f"Path to profitability · {PROJ}", "Profitable on the R25M seed, no Series A")
    chart(s, "cash_runway_r25m", (MX, 1.62, 8.0, 3.62), alt="Monthly closing cash on the R25M seed vs the R3.0M "
          "buffer, Oct 2026 to Sep 2030")
    tiles = [(CASH["break_even_month"], f"EBITDA break-even; sustained from {CASH['break_even_month_sustained']}"),
             (CASH["cash_flow_positive_month"], f"Operating cash flow positive; sustained "
              f"{CASH['cash_flow_positive_month_sustained']}"),
             (rm(CASH["min_post_seed_cash_zar"], 2), f"Cash low ({CASH['min_post_seed_cash_month']}) vs "
              f"{rm(CASH['min_cash_buffer_zar'])} buffer"),
             ("No Series A", "Profitable on R25M alone: Conservative, Base and Upside")]
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
    notes(s, f"""The R25M is sized to reach profitability on its own. The seed lands in {CASH['seed_month']}. Cash
    then declines to its low of {rm(CASH['min_post_seed_cash_zar'], 2)} in {CASH['min_post_seed_cash_month']},
    {rm(CASH['headroom_over_buffer_zar'], 2)} above our {rm(CASH['min_cash_buffer_zar'])} minimum buffer. Operating
    cash flow turns positive in {CASH['cash_flow_positive_month']}, and EBITDA breaks even in
    {CASH['break_even_month']}, sustained from {CASH['break_even_month_sustained']}. No Series A is needed in any
    scenario. Gating protects the buffer: every hire waits for an MRR milestone, Nigeria, Kenya and Ghana launch
    only at {rm(GATES['Nigeria'])}, {rm(GATES['Kenya'])} and {rm(GATES['Ghana'])} of monthly recurring revenue,
    and paid acquisition is capped. A pre-seed bridge of {rk(CASH['pre_seed_bridge_required_zar'])} is needed
    before close. Sources: model_summary.json → cash; markets.launch_mrr_gate_zar;
    scenario_definitions.Base.cap_pct.""")
    return s


def s_scenarios(prs):
    s = new_slide(prs)
    header(s, "Scenarios & sensitivities · model v2", "Profitable on R25M in all three scenarios")
    chart(s, "scenarios", (MX, 1.62, 6.6, 3.0), alt="FY5 revenue and EBITDA by scenario")
    rows = [[hdr_cell("Scenario", align="l"), hdr_cell("FY5 revenue"), hdr_cell("FY5 EBITDA"), hdr_cell("Cash low")]]
    for name, sc in [("Conservative", CONS), ("Base", BASE), ("Upside", UP)]:
        fill = TINT if name == "Base" else PAPER
        rows.append([{"text": name, "bold": True, "fill": fill}, {"text": rm(sc["fy5_revenue_zar"]), "fill": fill},
                     {"text": rm(sc["fy5_ebitda_zar"]), "fill": fill},
                     {"text": rm(sc["min_post_seed_cash_zar"], 2), "fill": fill}])
    table(s, 7.5, 1.62, [1.66, 1.2, 1.2, 1.17], [1.0, 0.6, 0.6, 0.6], rows, size=14, label="scen")
    text(s, 7.5, 4.5, 5.23, 0.78, f"Sustained EBITDA break-even: {CONS['breakeven_month_sustained']} · "
         f"{BASE['breakeven_month_sustained']} · {UP['breakeven_month_sustained']}. Cash stays above the "
         f"{rm(CASH['min_cash_buffer_zar'])} buffer every month.", size=14, role="body")
    rp, nr = FX["ZAR 15% stronger (repricing on)"], FX["ZAR 15% stronger (no repricing)"]
    low30 = M["sensitivity_base"]["min_post_seed_cash_zar_m"][2][0]
    cards = [(MIST, "FX SHOCK · ZAR 15% STRONGER",
              f"With quarterly repricing: cash low {rm(rp['min_post_seed_cash_zar'], 2)}, FY5 EBITDA "
              f"{rm(rp['fy5_ebitda_zar'])}. Without it: FY5 EBITDA {rm(nr['change_vs_base_zar']['fy5_ebitda_zar'])} "
              f"vs base, cash low {rm(nr['min_post_seed_cash_zar'], 2)}. Still profitable on R25M."),
             (TINT, "TRIAL VOLUME 30% BELOW PLAN",
              f"Cash low falls to R{low30:.2f}M, below the {rm(CASH['min_cash_buffer_zar'])} buffer. Response: raise "
              f"the hiring gates early, as Conservative does at 1.40x (low {rm(CONS['min_post_seed_cash_zar'], 2)}).")]
    for i, (fill, eb, b) in enumerate(cards):
        x = MX + i * (5.95 + 0.233)
        g = gid("sens")
        box(s, x, 5.32, 5.95, 1.38, fill=fill, shape="round", radius=0.18, role="card", group=g)
        text(s, x + 0.3, 5.44, 5.35, 0.28, eb, size=12, bold=True, color=DEEP, role="eyebrow", group=g, spc=120)
        text(s, x + 0.3, 5.76, 5.35, 0.88, b, size=14, role="card", group=g)
    notes(s, f"""We tested the plan three ways. Conservative, with slower trial growth, lower conversion and higher
    churn, still reaches {rm(CONS['fy5_revenue_zar'])} revenue and {rm(CONS['fy5_ebitda_zar'])} EBITDA in FY5, with
    a cash low of {rm(CONS['min_post_seed_cash_zar'], 2)}; it holds the buffer by waiting for 40% more MRR before
    each hire. Upside reaches {rm(UP['fy5_revenue_zar'])}. On FX, if the rand strengthens 15% against the naira,
    shilling, cedi and dollar, quarterly repricing keeps the low at {rm(rp['min_post_seed_cash_zar'], 2)}; without
    repricing FY5 EBITDA falls by {rm(-nr['change_vs_base_zar']['fy5_ebitda_zar'])} and the plan still passes. The
    real sensitivity is trial volume: 30% fewer trials takes the low to R{low30:.2f}M, below the buffer, so we
    would raise the gates early. Sources: model_summary.json → scenarios; fx_shock.results;
    sensitivity_base.min_post_seed_cash_zar_m[2][0].""")
    return s


def s_risks(prs):
    s = new_slide(prs)
    header(s, "Key risks", "What could go wrong, and how we manage it")
    low30 = M["sensitivity_base"]["min_post_seed_cash_zar_m"][2][0]
    risks = [("target", "Trial volume", f"30% fewer trials would take the cash low to R{low30:.2f}M.",
              "Pilot data first; if trials run 20% below plan, raise hiring gates early."),
             ("globe", "FX", "NGN, KES and GHS can weaken against the rand.",
              "Fixed local prices reviewed quarterly; a ZAR +15% shock still passes."),
             ("shield", "Meta dependency", "WhatsApp and Pages run on Meta; Instagram is in App Review.",
              "Verified Tech Provider on the official Cloud API; email, SMS, USSD and web chat too."),
             ("card", "Rail concentration", "A rail outage or contract change hits checkout.",
              "Five rails: four in South Africa, three each in Nigeria, Kenya and Ghana."),
             ("users", "Competition", "Larger platforms could add local features.",
              "One product for AI marketing, chat checkout and local pricing; agencies as partners."),
             ("briefcase", "Execution & hiring",
              f"From 2 founders to {A[1]['headcount_end_fy']} people by the end of FY2.",
              "Every hire waits for an MRR milestone; country leads only once SA carries them.")]
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
    notes(s, f"""These are the risks we would want an investor to probe. Trial volume matters most: the
    sensitivity grid shows 30% fewer trials takes minimum cash to R{low30:.2f}M, so pilot conversion data replaces
    our assumptions first, and we raise hiring gates if early trials run more than about 20% below plan. FX is
    controlled by fixed local prices and quarterly repricing. Meta dependency is real: we are a verified Tech
    Provider on the official Cloud API, and we also run email, SMS, USSD and web chat. Payments are spread across
    five rails. Competition is answered by the combined product and the agency channel. Execution risk is managed
    by MRR-gated hiring. Sources: Financial_Model_Notes.md §6 and §10; model_summary.json →
    annual[1].headcount_end_fy.""")
    return s


def s_ask(prs):
    s = new_slide(prs)
    header(s, "The ask", "R25M seed to reach profitability")
    g = gid("ask")
    box(s, MX, 1.62, 4.4, 2.6, fill=NIGHT, shape="round", radius=0.2, role="card", group=g)
    text(s, MX + 0.35, 1.7, 3.7, 1.2, "R25M", size=54, font=HEAD, bold=True, color=ORANGE, role="card", group=g)
    text(s, MX + 0.35, 2.94, 3.7, 0.34, f"Seed round · ≈US${BASE['seed_zar'] / M['fx_zar_per_usd'] / 1e6:.2f}M",
         size=16, bold=True, color=PAPER, role="card", group=g)
    text(s, MX + 0.35, 3.32, 3.7, 0.34, "Instrument [[TBC]] · valuation [[TBC]]", size=14, color=PAPER,
         role="placeholder", group=g)
    text(s, MX + 0.35, 3.68, 3.7, 0.5, f"Close {CASH['seed_month']} · pre-seed bridge "
         f"{rk(CASH['pre_seed_bridge_required_zar'])}", size=14, color=MUTED_DARK, role="card", group=g)
    cats = {c["category"]: c for c in REC24["categories"]}
    exp = cats["Market expansion (NG, KE, GH) & payments compliance"]["share_of_spend_pct"]
    ops = cats["Operations & working capital"]["share_of_spend_pct"]
    g = gid("rec")
    box(s, MX, 4.4, 4.4, 2.5, fill=TINT, shape="round", radius=0.2, role="card", group=g)
    text(s, MX + 0.3, 4.56, 3.8, 0.28, "MODELLED SPEND VS ALLOCATION", size=12, bold=True, color=DEEP,
         role="eyebrow", group=g, spc=120)
    text(s, MX + 0.3, 4.88, 3.8, 1.9, f"The seed funds net burn: {rm(REC24['net_cash_consumed_zar'], 2)} is used in "
         f"the first 24 months, leaving {rm(REC24['seed_remaining_zar'], 2)} unspent as a downside reserve if trial "
         f"volume underperforms. Expansion runs at {exp}% of spend, operations at {ops}%.", size=14,
         role="card", group=g)
    chart(s, "use_of_funds", (5.3, 1.62, 7.43, 3.35), crop=(0.12, 0.16, 0.08, 0.1), align="c",
          alt="Use of funds: R10.0M product and engineering, R7.5M sales and marketing, R3.75M operations, "
          "R3.75M market expansion")
    al = {a["category"]: a for a in UOF["allocation"]}
    buys = [(rm(al["Product & engineering"]["amount_zar"]), "product & engineering: ",
             "engineers, AI/ML, design, integrations, hosting"),
            (rm(al["Sales & marketing / partner programme"]["amount_zar"]), "sales & marketing: ",
             "growth team, partnerships, capped paid acquisition"),
            (rm(al["Market expansion (NG, KE, GH) & payments compliance"]["amount_zar"], 2), "expansion: ",
             "NG/KE/GH country teams, compliance, launches"),
            (rm(al["Operations & working capital"]["amount_zar"], 2), "operations: ",
             "customer success, finance, processing, cash buffer")]
    cw2 = (7.43 - 0.15) / 2
    for i, (v, lab, t) in enumerate(buys):
        x = 5.3 + (i % 2) * (cw2 + 0.15)
        y = 5.1 + (i // 2) * 0.9
        g = gid("buy")
        box(s, x, y, cw2, 0.84, fill=MIST, shape="round", radius=0.14, role="card", group=g)
        text(s, x + 0.15, y + 0.03, cw2 - 0.3, 0.78, [[(f"{v} {lab}", {"bold": True, "color": DEEP}), (t, {})]],
             size=14, anchor="m", role="card", group=g)
    notes(s, f"""We are raising R25M, about US$1.35M, with instrument and valuation to be confirmed. The allocation
    is 40% product and engineering, {rm(al['Product & engineering']['amount_zar'])}; 30% sales, marketing and the
    partner programme, {rm(al['Sales & marketing / partner programme']['amount_zar'])}; 15% expansion into Nigeria,
    Kenya and Ghana with payments compliance, R3.75M; and 15% operations and working capital, R3.75M. To be plain
    about the reconciliation: the seed funds net burn, not gross spend. In the first 24 months the model consumes
    {rm(REC24['net_cash_consumed_zar'], 2)}, so about {rm(REC24['seed_remaining_zar'])} stays unspent. That is a
    downside reserve that keeps the plan intact if trial volume underperforms, not money we plan to deploy.
    Sources: model_summary.json → use_of_funds.allocation and use_of_funds.reconciliation["24"].""")
    return s


def s_milestones(prs):
    s = new_slide(prs)
    header(s, "Milestones this round buys", "From pilot to break-even")
    rows = [[("Sept 2026", "All 5 payment rails live, 23 countries", False),
             ("Q4 2026", "Meta permissions incl. Instagram (target)", False),
             ("Dec 2026", "Pilot ends 30 Nov; results and case studies", False),
             ("1 Dec 2026", "SA launch; Founding Member to 31 Jan 2027", False),
             (CASH["seed_month"], "Seed closes (model input); first hires", False)],
            [("2027 onward", "Social adapters, integrations, Flux_Partner (indicative)", False),
             (f"{LAUNCH['Nigeria'][:3]}–{LAUNCH['Ghana']}", "Nigeria, Kenya and Ghana launch (MRR-gated)", True),
             (CASH["cash_flow_positive_month"], "Operating cash flow positive", True),
             (LAUNCH["Rest of Africa (USD)"], "19 USD markets open, self-serve", True),
             (CASH["break_even_month"], f"EBITDA break-even; sustained {CASH['break_even_month_sustained']}", True)]]
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
            text(s, x + 0.2, ly + 0.42, cw_ - 0.4, 0.4, d, size=16, font=HEAD, bold=True, color=DEEP, role="card", group=g)
            text(s, x + 0.2, ly + 0.86, cw_ - 0.4, 1.25, t, size=14, role="card", group=g)
    caption(s, MX, 6.72, CW, 0.26, f"Orange cards: {PROJ.lower()}; launch dates move with MRR gates. Product "
            "order per the founder roadmap; 2027 items are indicative and undated.")
    notes(s, f"""This is what the round buys, in order. All five rails go live in September 2026, and Meta
    permissions, including Instagram, are targeted for Q4 2026. The pilot ends on 30 November and results arrive
    in December, as South Africa launches on 1 December with the Founding Member window. The seed closes in
    {CASH['seed_month']} in the model and funds the first hires. From 2027, in the founder's order: social
    adapters, business app integrations and the Flux_Partner programme, all indicative. Then the modelled
    milestones: Nigeria, Kenya and Ghana from {LAUNCH['Nigeria']} to {LAUNCH['Ghana']}, operating cash flow
    positive in {CASH['cash_flow_positive_month']}, USD markets from {LAUNCH['Rest of Africa (USD)']}, and EBITDA
    break-even in {CASH['break_even_month']}. Sources: facts §1 roadmap, §3, §6; model_summary.json →
    markets.launch_months.Base and cash.""")
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
    header(s, f"Team · headcount {hc[0]} → {hc[1]} → {hc[4]} (FY1, FY2, FY5; model v2)", "The team, and who the seed hires")
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
    text(s, MX, 3.95, 7.0, 0.7, f"R25M to reach profitability on this round alone ({PROJ.lower()}).", size=18,
         color="D5DADF", role="body")
    rows = [("checkCircle", "Verified Meta Tech Provider"), ("card", "5 payment rails · 23 countries"),
            ("calendar", "Gauteng pilot results: December 2026")]
    for i, (ic, t) in enumerate(rows):
        y = 4.8 + i * 0.68
        g = icon(s, ic, "ink", MX + 0.3, y + 0.28, 0.56, circle=ORANGE)
        text(s, MX + 0.8, y, 6.0, 0.56, t, size=17, color=PAPER, anchor="m", role="body", group=g)
    g = gid("contact")
    box(s, 8.2, 2.25, 4.53, 3.6, fill=NIGHT_CARD, shape="round", radius=0.2, role="card", group=g)
    text(s, 8.55, 2.55, 3.85, 0.3, "CONTACT", size=12, bold=True, color=ORANGE, role="eyebrow", group=g, spc=150)
    text(s, 8.55, 2.95, 3.85, 2.6, [{"runs": "[[EMAIL]]", "space_after": 12, "bold": True, "color": PAPER},
                                    {"runs": "[[PHONE]]", "space_after": 12},
                                    {"runs": [("Data room: ", {"color": MUTED_DARK}), ("[[LINK]]", {"color": PAPER, "bold": True})]}],
         size=18, color="D5DADF", role="placeholder", group=g)
    notes(s, f"""Close with the ask and a clear next step. FluxMuse gives African SMBs an AI marketing team and
    WhatsApp checkout on local rails, and in the model the R25M seed carries the plan to profitability in all
    three scenarios, with no Series A. Offer data-room access, including the financial model and notes, Meta
    verification evidence and rail contracts, and promise the pilot results pack in December 2026. Agree a
    follow-up date before the meeting ends. Fill in [[EMAIL]], [[PHONE]] and the data-room [[LINK]] before
    sending. Sources: model_summary.json → profitable_on_seed_alone
    (Conservative {M['profitable_on_seed_alone']['Conservative']}, Base {M['profitable_on_seed_alone']['Base']},
    Upside {M['profitable_on_seed_alone']['Upside']}); facts §6 and §7; Investor_Deck_Guide.md for the data room.""")
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
    market. A3 has the full price tables in rand, local currencies and US dollars, plus partner wholesale. A4 is
    the payment rails matrix by country. A5 is the FX shock sensitivity, and A6 the Founding Member discount cost
    against the alternatives. A7 lists founder confirmations still open: it is for internal use only, so hide or
    delete it before the deck goes to any investor. Sources: model_summary.json; 00_FACTS_AND_ASSUMPTIONS.md.""")
    return s


ASSUMPTION_TOPICS = ["Timing & cash", "Pilot", "Founding Member", "Pricing", "Partner wholesale", "FX", "Segments",
                     "Churn", "Markets", "Cost discipline", "Other revenue", "COGS", "Funding & tax"]


def a_assumptions(prs):
    ka = M["key_assumptions"]
    heights = [0.2 * max(1, math.ceil(len(t) / 100)) + 0.16 for t in ka]
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
        header(s, f"Appendix A1 · key assumptions ({p + 1} of {len(pages)}) · model v2", "Key model assumptions")
        rows = [[hdr_cell("Topic", align="l", size=12), hdr_cell("Assumption (model_summary.json → key_assumptions)",
                                                                  align="l", size=12)]]
        for i in idxs:
            rows.append([{"text": ASSUMPTION_TOPICS[i], "bold": True, "size": 12},
                         {"text": ka[i], "align": "l", "size": 12}])
        table(s, MX, 1.62, [1.9, 10.23], [0.36] + [heights[i] for i in idxs], rows, size=12, label="assumptions")
        topics = ", ".join(ASSUMPTION_TOPICS[i].lower() for i in idxs)
        notes(s, f"""These assumptions are copied word for word from the model summary, so they always match the
        workbook. This page covers {topics}. Items marked [[CONFIRM]] are still waiting for founder sign-off and
        are listed again in appendix A7. When an investor challenges a number in the deck, trace it here first,
        then to the Assumptions sheet in FluxMuse_Financial_Model.xlsx, where each input sits in its own cell with
        the Conservative, Base and Upside values side by side. The most important inputs to replace with pilot
        data are trial-to-paid conversion, trial volume and early churn. Source: model_summary.json →
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
    caption(s, MX, 4.6, 5.95, 0.9, f"By segment, FY5: Solo {num(seg['Solo'])} · SMEs {num(seg['SMEs'])} · Agencies "
            f"{num(seg['Agencies'])} · Enterprise {num(seg['Enterprise'])}. Bars are rounded per segment, so FY1 and "
            f"FY3 read 422 and 3,821 against model totals of {num(A[0]['ending_paying_workspaces'])} and "
            f"{num(A[2]['ending_paying_workspaces'])}.", size=12)
    caption(s, 6.78, 4.6, 5.95, 0.9, f"By market, Sep 2031: South Africa {num(mk['South Africa'])} · Nigeria "
            f"{num(mk['Nigeria'])} · Kenya {num(mk['Kenya'])} · Ghana {num(mk['Ghana'])} · 19 USD markets "
            f"{num(mk['Rest of Africa (USD)'])}. Botswana & Namibia off; gated countries zero.", size=12)
    notes(s, f"""Two views of the same customer base. By segment, solo entrepreneurs and SMEs make up almost all
    workspaces, with {num(seg['Agencies'])} agency partners and {num(seg['Enterprise'])} inbound enterprise
    customers by FY5. Note that the segment chart rounds each segment before stacking, so its FY1 and FY3 labels
    read one higher than the model totals of {num(A[0]['ending_paying_workspaces'])} and
    {num(A[2]['ending_paying_workspaces'])}; quote the totals. By market, South Africa stays the core with
    {num(mk['South Africa'])} workspaces at the end of FY5, and the markets outside it add the rest, starting with
    Nigeria in {LAUNCH['Nigeria']}. {PROJ}. Sources: model_summary.json →
    annual[].ending_customers_by_segment, ending_customers_by_market and ending_paying_workspaces.""")
    return s


def a_pricing_zar(prs):
    s = new_slide(prs)
    header(s, "Appendix A3 · pricing (1 of 2) · ZAR", "Plans at a glance, in rand")
    zar = PT["zar_list_monthly"]
    fm = PT["founding_member_first_2_bills_zar"]
    hdr = lambda t, **k: hdr_cell(t, size=14, **k)
    grow = lambda t, **k: {"text": t, "fill": TINT, "bold": k.get("bold", False)}
    lab = lambda t: {"text": t, "bold": True, "align": "l"}
    rows = [
        [hdr("Plan", align="l"), hdr("Starter"), hdr("Growth", fill=ORANGE, color=NIGHT), hdr("Scale"), hdr("Agency")],
        [lab("Monthly"), {"text": rn(zar["Starter"]), "bold": True}, grow(rn(zar["Growth"]), bold=True),
         {"text": rn(zar["Scale"]), "bold": True}, {"text": rn(zar["Agency"]), "bold": True}],
        [lab("Annual (10× monthly)"), rn(zar["Starter"] * 10), grow(rn(zar["Growth"] * 10)), rn(zar["Scale"] * 10),
         rn(zar["Agency"] * 10)],
        [lab("Founding Member, first 2 bills"), rn(fm["Starter"]), grow(rn(fm["Growth"])), rn(fm["Scale"]),
         "Not offered"],
        [lab("Partner wholesale / month"), "–", grow("–"), "–", {"text": rn(PT["partner_wholesale_monthly"]["ZAR"]),
                                                                  "bold": True, "color": DEEP}],
        [lab("Brands · channels"), "1 · 3", grow("3 · 15"), "10 · 40", "Unlimited · 80"],
        [lab("AI credits / month"), "5,000", grow("25,000"), "100,000", "500,000"],
    ]
    table(s, MX, 1.62, [3.13, 2.25, 2.25, 2.25, 2.25], [0.5] + [0.52] * 6, rows, size=14, label="pricing-zar")
    caption(s, MX, 5.4, CW, 0.9, [{"runs": f"Enterprise from {rn(zar['Enterprise'])}/mo, inbound only. 14-day free "
                                           "trial, no card required. Pilot brands: 50% off the first 2 bills "
                                           f"({rn(PT['pilot_first_2_bills_zar']['Starter'])} / "
                                           f"{rn(PT['pilot_first_2_bills_zar']['Growth'])} / "
                                           f"{rn(PT['pilot_first_2_bills_zar']['Scale'])} / "
                                           f"{rn(PT['pilot_first_2_bills_zar']['Agency'])}).", "space_after": 4},
                                  "Founding Member does not stack with partner wholesale. Perks duration: founder "
                                  "decision pending."], size=12)
    notes(s, f"""The full rand price list. Starter is {rn(zar['Starter'])} a month, Growth {rn(zar['Growth'])},
    Scale {rn(zar['Scale'])} and Agency {rn(zar['Agency'])}; annual billing is ten times monthly, which is two
    months free. Founding Members pay {rn(fm['Starter'])}, {rn(fm['Growth'])} or {rn(fm['Scale'])} for their first
    two monthly bills, and the offer is not available on Agency: agencies buy at the permanent partner wholesale
    price of {rn(PT['partner_wholesale_monthly']['ZAR'])}. Enterprise starts from {rn(zar['Enterprise'])} and is
    inbound only. The twelve pilot brands get 50% off their first two bills from 1 December 2026. Sources:
    00_FACTS_AND_ASSUMPTIONS.md §2; model_summary.json → price_tables.""")
    return s


def a_pricing_local(prs):
    s = new_slide(prs)
    header(s, "Appendix A3 · pricing (2 of 2) · local currency & USD", "Local-currency, USD and wholesale prices")
    lm, ws = PT["local_monthly"], PT["partner_wholesale_monthly"]
    rows = [[hdr_cell("Plan", align="l", size=12)] + [hdr_cell(t, size=12) for t in
             ["NGN / mo", "NGN / yr", "KES / mo", "KES / yr", "GHS / mo", "GHS / yr", "USD / mo", "USD / yr"]]]
    for t in ["Starter", "Growth", "Scale", "Agency"]:
        fill = TINT if t == "Growth" else PAPER
        vals = [f"₦{lm['NGN'][t]:,}", f"₦{lm['NGN'][t] * 10:,}", f"KSh {lm['KES'][t]:,}", f"KSh {lm['KES'][t] * 10:,}",
                f"GH₵ {lm['GHS'][t]:,}", f"GH₵ {lm['GHS'][t] * 10:,}", f"${lm['USD'][t]:,}", f"${lm['USD'][t] * 10:,}"]
        rows.append([{"text": t, "bold": True, "fill": fill, "size": 12}] + [{"text": v, "fill": fill, "size": 12} for v in vals])
    rows.append([{"text": "Enterprise", "bold": True, "size": 12}] +
                [{"text": v, "size": 12} for v in [f"from ₦{lm['NGN']['Enterprise']:,}", "custom",
                                                   f"from KSh {lm['KES']['Enterprise']:,}", "custom",
                                                   f"from GH₵ {lm['GHS']['Enterprise']:,}", "custom",
                                                   f"from ${lm['USD']['Enterprise']:,}", "custom"]])
    table(s, MX, 1.62, [1.33] + [1.35] * 8, [0.42, 0.42, 0.42, 0.42, 0.42, 0.62], rows, size=12, label="regional")
    rows2 = [[hdr_cell("Partner wholesale (Agency −30%)", align="l", size=12)] +
             [hdr_cell(t, size=12) for t in ["ZAR", "NGN", "KES", "GHS", "USD"]],
             [{"text": "Per month", "bold": True, "size": 12, "fill": TINT}] +
             [{"text": v, "size": 12, "bold": True, "fill": TINT} for v in
              [rn(ws["ZAR"]), f"₦{ws['NGN']:,}", f"KSh {ws['KES']:,}", f"GH₵ {ws['GHS']:,}", f"${ws['USD']:,}"]],
             [{"text": "Per year (10×)", "bold": True, "size": 12}] +
             [{"text": v, "size": 12} for v in
              [rn(ws["ZAR"] * 10), f"₦{ws['NGN'] * 10:,}", f"KSh {ws['KES'] * 10:,}", f"GH₵ {ws['GHS'] * 10:,}",
               f"${ws['USD'] * 10:,}"]]]
    table(s, MX, 4.6, [3.13, 1.8, 1.8, 1.8, 1.8, 1.8], [0.42, 0.42, 0.42], rows2, size=12, label="wholesale")
    caption(s, MX, 6.0, CW, 0.7, "Fixed price points at FX parity with the rand (Sept 2026), reviewed quarterly and "
            "reset if drift exceeds 10%. USD applies in the 19 other rail-covered countries. Countries without a "
            "rail, including Botswana and Namibia (coming soon): waitlist only, no prices.", size=12)
    fxs = PT["fx_price_setting"]
    notes(s, f"""Local-currency prices for the first expansion wave and USD for the other rail-covered markets.
    Nigeria, Kenya and Ghana use fixed, rounded price points set at parity with the rand, using 1 ZAR =
    ₦{fxs['NGN_per_ZAR']}, KSh {fxs['KES_per_ZAR']} and GH₵ {fxs['GHS_per_ZAR']}. The 19 USD markets are billed in
    US dollars at parity. Kenyan annual prices end in 990 by design, as in the facts file. Partner wholesale is
    30% off the Agency list price in every currency. Prices are reviewed quarterly and reset when their rand value
    drifts more than 10%, which is the main FX control tested in appendix A5. Sources: 00_FACTS_AND_ASSUMPTIONS.md
    §2; model_summary.json → price_tables.local_monthly, partner_wholesale_monthly, fx_price_setting.""")
    return s


def a_rails(prs):
    s = new_slide(prs)
    header(s, "Appendix A4 · payment rails", "Payment rails by country")
    pic(s, "infographics/payment-rails-matrix.png", MX, 1.55, CW, 5.35, crop=(0, 0.19, 0, 0.06), align="t",
        alt="Matrix of 23 countries by region against 5 payment rails with billing currency; Botswana and Namibia "
        "coming soon")
    notes(s, """This matrix shows which of the five rails covers each of the 23 countries, grouped by region, with
    the billing currency. South Africa has four rails: Yoco, Ozow, Paystack and Fincra. Nigeria, Ghana and Kenya
    each have Paystack, pawaPay and Fincra, which is why they form the first expansion wave. Most other countries
    are covered by pawaPay mobile money and Fincra. South Sudan and Zimbabwe are Fincra payouts only, so sales
    there open only once subscription collection is confirmed. Botswana and Namibia are coming soon with no rail
    yet, so they are waitlist only. Rail contracts belong in the data room. Sources: 00_FACTS_AND_ASSUMPTIONS.md
    §3; infographic payment-rails-matrix.""")
    return s


def a_fx(prs):
    s = new_slide(prs)
    header(s, "Appendix A5 · FX shock · model v2", "ZAR 15% stronger vs NGN, KES, GHS and USD")
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
            [c("Profitable on R25M", bold=True)] + [c("Yes" if x["profitable_on_seed_alone"] else "No", bold=True,
                                                      color=DEEP) for x in cases]]
    table(s, 8.4, 1.62, [1.15, 1.06, 1.06, 1.06], [0.95, 0.56, 0.56, 0.56, 0.56, 0.8, 0.6], rows, size=12, label="fx")
    nr = FX["ZAR 15% stronger (no repricing)"]["change_vs_base_zar"]
    text(s, MX, 5.3, 7.6, 1.35, f"The shock starts in Oct 2028, once Nigeria, Kenya and Ghana are live. Repricing "
         f"costs one quarter of revenue, then resets. Without repricing, FY5 EBITDA moves "
         f"{rm(nr['fy5_ebitda_zar'])} but the {rm(CASH['min_cash_buffer_zar'])} buffer holds.", size=14, role="body")
    notes(s, f"""This is the currency stress test. From October 2028 the rand is assumed 15% stronger against the
    naira, shilling, cedi and dollar, so every local price is worth less in rand. With our quarterly repricing
    policy, the shock costs one quarter of revenue and then triggers a reset, so FY5 ends slightly above base and
    the cash low is {rm(FX['ZAR 15% stronger (repricing on)']['min_post_seed_cash_zar'], 2)}. Without repricing, FY5
    revenue moves {rm(nr['fy5_revenue_zar'])} and FY5 EBITDA {rm(nr['fy5_ebitda_zar'])}, and the plan is still
    profitable on the seed alone. The lesson is that repricing discipline is the main FX control. Sources:
    model_summary.json → fx_shock.definition and fx_shock.results; Financial_Model_Notes.md §6.""")
    return s


def a_founding(prs):
    s = new_slide(prs)
    fmd = M["founding_member"]
    header(s, f"Appendix A6 · launch discount cost · {PROJ}", "Founding Member costs little")
    chart(s, "founding_member_discount_cost", (MX, 1.62, 7.6, 3.44), alt="Launch discount cost by year and market")
    oc = fmd["option_comparison"]
    rows = [[hdr_cell("Launch offer", align="l"), hdr_cell("FY1–FY3 cost"), hdr_cell("Cash low")]]
    for k, lab in [("B Founding Member (default)", "B · Founding Member"), ("A Launch Sprint", "A · Launch Sprint"),
                   ("None", "None")]:
        fill = TINT if k.startswith("B") else PAPER
        rows.append([{"text": lab, "bold": True, "fill": fill},
                     {"text": rk(oc[k]["discount_cost_fy1_fy3_zar"]) if oc[k]["discount_cost_fy1_fy3_zar"] else "R0",
                      "fill": fill}, {"text": rm(oc[k]["min_post_seed_cash_zar"], 2), "fill": fill}])
    table(s, 8.4, 1.62, [2.3, 1.05, 0.98], [0.66, 0.5, 0.5, 0.5], rows, size=14, label="fm")
    text(s, 8.4, 3.95, 4.33, 1.1, "All three options remain profitable on R25M. B is the only offer used in "
         "external materials.", size=14, role="body")
    dc = fmd["discount_cost_by_fy_zar"]
    text(s, MX, 5.3, 7.6, 1.35, f"Founding Member costs {rk(dc['FY1'], 0)} in FY1, {rk(dc['FY2'], 0)} in FY2 and "
         f"{rk(dc['FY3'], 0)} in FY3, never more than 1.3% of gross subscriptions. FY1 also carries "
         f"{rk(M['pilot']['pilot_discount_cost_fy1_zar'])} of pilot discounts. The +{fmd['window_signup_uplift_pct']}% "
         "sign-up uplift is an assumption to test.", size=14, role="body")
    notes(s, f"""Investors often ask whether the launch discount hurts the plan. It does not. Founding Member,
    30% off the first two monthly bills for solo and SME sign-ups in a 60-day launch window, costs
    {rk(dc['FY1'], 0)}, {rk(dc['FY2'], 0)} and {rk(dc['FY3'], 0)} of revenue in FY1 to FY3. Because the model
    assumes a {fmd['window_signup_uplift_pct']}% sign-up uplift inside each window, option B leaves slightly more
    cash than no offer at all. That uplift is unproven, so the South African December to January window is the
    test. The alternative Launch Sprint offer is kept only as a sensitivity and is never shown externally.
    Sources: model_summary.json → founding_member.discount_cost_by_fy_zar, option_comparison,
    window_signup_uplift_pct; pilot.pilot_discount_cost_fy1_zar.""")
    return s


def a_confirmations(prs):
    s = new_slide(prs)
    header(s, "Appendix A7 · internal only · hide before sending", "Founder confirmations still open")
    items = M["founder_confirmations_needed"]
    hs = [0.2 * max(1, math.ceil(len(t) / 44)) + 0.12 for t in items]
    half = min(range(1, len(items)), key=lambda k: max(sum(hs[:k]), sum(hs[k:])))
    for c, chunk in enumerate([items[:half], items[half:]]):
        off = 0 if c == 0 else half
        heights = hs[:half] if c == 0 else hs[half:]
        rows = [[{"text": str(off + i + 1), "bold": True, "size": 12, "color": DEEP},
                 {"text": t, "size": 12, "align": "l"}] for i, t in enumerate(chunk)]
        table(s, MX + c * (5.95 + 0.233), 1.55, [0.45, 5.5], heights, rows, size=12, label=f"confirm{c}")
        assert sum(heights) < 5.35, f"A7 column {c} is {sum(heights):.2f} in tall"
    notes(s, """Internal slide: hide or delete it before the deck goes to any investor. These are the model inputs
    and decisions the founder still has to confirm, copied from the model summary. The most urgent are opening
    cash and how to cover the pre-seed bridge, the seed close month and instrument, and the pilot conversion rate.
    Market sizing must also be verified before any external use. Once a decision is made, update the Assumptions
    sheet, rebuild the model, rebuild this deck with build_investor_deck.py and rerun the QA script, so that every
    slide picks up the new numbers. Source: model_summary.json → founder_confirmations_needed;
    Financial_Model_Notes.md §12.""")
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
    prs.core_properties.title = "FluxMuse investor pitch deck: R25M seed"
    prs.core_properties.author = "Fluxmuse Pty Ltd"
    prs.core_properties.subject = "Seed round, confidential"
    core = [s_title, s_problem, s_solution, s_product, s_market, s_model, s_gtm, s_payments, s_traction,
            s_competition, s_unit, s_projections, s_profit, s_scenarios, s_risks, s_ask, s_milestones, s_team, s_close]
    slides = [fn(prs) for fn in core]
    slides.append(a_divider(prs, [("A1", "Key model assumptions"), ("A2", "Paying workspaces by segment and market"),
                                  ("A3", "Pricing: ZAR, local currency, USD, partner wholesale"),
                                  ("A4", "Payment rails by country"), ("A5", "FX shock sensitivity"),
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
