#!/usr/bin/env python3
"""Build the FluxMuse brand pitch decks (master + solo, SME and partner variants).

Every image is embedded from docs/go-to-market/assets/ at build time, so re-running this
script picks up re-rendered infographics. Facts come from 08_Prospects/CURRENT_OFFER.md (source of truth)
and 00_FACTS_AND_ASSUMPTIONS.md.

    python build_deck.py            # needs python-pptx + Pillow
    python qa_deck.py               # structural + visual QA (see that file)

Shape names follow "group|role|label" so qa_deck.py can check font sizes, overlaps and
word counts by role. Roles: bg, deco, title, eyebrow, body, card, chip, caption, footer,
slidenum, img, icon, table, placeholder.
"""
from __future__ import annotations

import json
import re
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
OUT = GTM / "02_Brand_Pitch_Deck"
V3_MARKER = ASSETS / ".revision-v3-done"

# ---------------------------------------------------------------- brand tokens
ORANGE, GLOW, TINT = "FF6A00", "FF8533", "FFF4EB"
DEEP = "C24E00"  # orange text on white (AA)
SLATE, INK, NIGHT, PAPER, MIST = "37474F", "20242B", "0F1419", "FFFFFF", "F3F4F6"
NIGHT_CARD = "1B232C"
MUTED = "5B6670"  # captions on white (>= 5:1)
MUTED_DARK = "A7B0B8"  # secondary text on Night
LINE = "E3E6EA"
HEAD, BODY = "Poppins", "Inter"

SW, SH = 13.333, 7.5
MX = 0.6  # side margin
CW = SW - 2 * MX  # content width 12.133

USED_IMAGES: dict[str, set] = {}
_CUR_DECK = [""]
_gid = [0]


def gid(prefix="g"):
    _gid[0] += 1
    return f"{prefix}{_gid[0]}"


# ---------------------------------------------------------------- primitives
def rgb(h):
    return RGBColor.from_string(h)


def set_bg(slide, colour):
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = rgb(colour)


def text(slide, x, y, w, h, paras, *, size=16, font=BODY, color=INK, bold=False, align="l",
         anchor="t", role="body", group=None, label="", lsp=None, spc=None, space_after=0):
    """paras: str | list[str | list[(text, opts)] | dict(runs=..., size=, align=, space_after=)]"""
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


def pic(slide, rel, x, y, w, h, *, crop=(0, 0, 0, 0), align="c", alt="", group=None, role="img",
        rounded=False, base=ASSETS):
    """Fit the cropped image inside the (x, y, w, h) box. align: c | t | l | tl."""
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
    if rounded:
        p.auto_shape_type = MSO_SHAPE.ROUNDED_RECTANGLE
    if base == ASSETS:
        USED_IMAGES.setdefault(_CUR_DECK[0], set()).add(rel)
    return px, py, pw, ph


def icon(slide, name, colour, cx, cy, d, *, circle=None, ring=None, group=None, scale=0.56):
    """Icon centred at (cx, cy) inside an optional circle of diameter d."""
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
    """rows: list of list of cell (str | dict(text, bold, color, fill, align, size, font))."""
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
    text(slide, MX, 7.04, 4.0, 0.26, "FluxMuse · fluxmuse.ai", size=10, color=MUTED_DARK if dark else MUTED,
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


def notes(slide, note, v):
    t = (note.get(v) or note["default"]) if isinstance(note, dict) else note
    slide.notes_slide.notes_text_frame.text = " ".join(t.split())


def hero(slide, rel, crop, alt, box_=(MX, 1.52, CW, 5.4), align="c"):
    return pic(slide, rel, *box_, crop=crop, alt=alt, align=align)


# ---------------------------------------------------------------- image crops (l, t, r, b)
# Infographics share one template: eyebrow + title (+ subtitle) in the top ~20% of the canvas,
# which the slide replaces with a native, editable title.
TOP = (0, 0.2, 0, 0)
IMG = {
    "problem": ("infographics/problem-solution.png", (0.02, 0.21, 0.02, 0.15)),
    "how": ("infographics/how-fluxmuse-works.png", TOP),
    "flow": ("infographics/whatsapp-commerce-flow.png", TOP),
    "hub": ("infographics/omnichannel-hub.png", TOP),
    "stack": ("infographics/platform-stack.png", TOP),
    "map": ("infographics/payment-coverage-map.png", (0, 0.205, 0, 0)),
    "solo": ("infographics/segment-solo.png", TOP),
    "sme": ("infographics/segment-sme.png", TOP),
    "agency": ("infographics/segment-agency.png", TOP),
    "partner": ("infographics/agency-partner-model.png", TOP),
    "journey": ("infographics/brand-engagement-journey.png", TOP),
    "case": ("infographics/case-study-template.png", (0, 0.03, 0, 0)),  # keep the "Template · no data yet" stamp
    "tiers": ("infographics/pricing-tiers.png", TOP),
    "founding": ("infographics/founding-member-offer.png", TOP),
    "roadmap": ("infographics/roadmap-2026-2027.png", TOP),
    "matrix": ("infographics/payment-rails-matrix.png", (0, 0.2, 0, 0)),
}

# Lead guarantee: always shown with its conditions (CURRENT_OFFER.md §2; 00_FACTS §2 "Lead guarantee").
GUARANTEE_HEAD = "3 qualified leads in 30 days of go-live"
GUARANTEE_TERMS = ("A qualified lead is a new WhatsApp number that messages you through your FluxMuse link. If fewer "
                   "than 3 arrive in 30 days, and you shared your link and posted at least weekly, we keep supporting "
                   "you at no extra charge until you reach 3. Extra support, not a payout.")


def img(slide, key, alt, box_=(MX, 1.52, CW, 5.4), align="c", rounded=False):
    rel, crop = IMG[key]
    return pic(slide, rel, *box_, crop=crop, alt=alt, align=align, rounded=rounded)


# ================================================================ SLIDES
# Each builder: (prs, v, **kw) -> slide. v in {"master", "solo", "sme", "partner"}.
# Facts: docs/go-to-market/08_Prospects/CURRENT_OFFER.md (source of truth) and 00_FACTS_AND_ASSUMPTIONS.md.

def s_title(prs, v):
    s = new_slide(prs, dark=True)
    pic(s, "brand/fluxmuse-logo-dark.png", MX, 0.55, 2.6, 0.9, align="tl", alt="FluxMuse logo")
    g = gid()
    box(s, 8.55, 1.25, 4.3, 4.3, fill=NIGHT_CARD, shape="oval", role="deco", group=g)
    pic(s, "brand/fluxmuse-icon-512.png", 8.95, 1.65, 3.5, 3.5, alt="FluxMuse Muse icon", group=g)
    if v == "partner":
        eyebrow, l1, l2 = "FluxMuse Partner Programme", "Serve more clients.", "Under your brand."
        sub = "White-label AI marketing and WhatsApp selling for agencies and resellers."
    else:
        eyebrow, l1, l2 = "AI marketing & WhatsApp selling", "Your AI marketing team.", "Selling on WhatsApp."
        sub = "Send photos, get a shop link, and let your AI team help you post and reply. Built for South Africa."
    text(s, MX, 2.05, 7.6, 0.3, eyebrow.upper(), size=13, bold=True, color=ORANGE, role="eyebrow", spc=150)
    text(s, MX, 2.42, 7.7, 1.9, [[(l1, {"color": PAPER})], [(l2, {"color": ORANGE})]], size=38, font=HEAD,
         bold=True, role="title", lsp=0.95)
    text(s, MX, 4.4, 7.2, 0.8, sub, size=18, color="D5DADF", role="body")
    g = gid()
    text(s, MX, 5.45, 7.4, 0.42, [[("Prepared for ", {"color": MUTED_DARK, "bold": False}),
                                   ("[[PROSPECT NAME]]", {"color": PAPER, "bold": True})]],
         size=18, role="placeholder", group=g)
    text(s, MX, 5.92, 7.4, 0.36, "[[DATE]]  ·  Thabo Malebadi, founder", size=15, color=MUTED_DARK,
         role="placeholder", group=g)
    notes(s, {
        "default": """Open warmly and make it about them. "Thanks for your time. FluxMuse is an AI marketing team
        that lives in WhatsApp: send product photos, get a shop link, and get help posting and replying." Say the
        session takes about 20 minutes plus questions. Ask one opening question: "Where do most of your sales
        conversations happen today?" Their answer tells you which slides to lean on. Swap guide: owner-operators get
        the Solo deck, businesses with staff get the SME deck, agencies get the Partner Programme deck. Facts in
        this deck follow CURRENT_OFFER.md.""",
        "solo": """Keep it personal and short. "You're running the business, the marketing and the WhatsApp inbox
        yourself. FluxMuse is an AI marketing team that lives in WhatsApp, with paid plans from R149 a month." Promise
        about 15 minutes. Ask: "How do customers find you, and how do they order today?" Listen for lost messages,
        late replies and no shop page; you'll come back to each one. If they have staff or several brands, switch to
        the SME deck. Prices follow CURRENT_OFFER.md §1.""",
        "sme": """Frame this as a conversation about time and control. "FluxMuse gives your team an AI marketing
        team inside WhatsApp: a shop link built from your photos, an order alert for every sale, and help posting and
        replying." Confirm who's in the room: owner, marketing, operations. Ask: "Which tools do you use today for
        social, WhatsApp and orders, and who runs each one?" If they manage brands for clients, they're an agency:
        use the Partner deck. Facts follow CURRENT_OFFER.md.""",
        "partner": """This deck is for agencies, freelancers and resellers. "FluxMuse lets you offer an AI marketing
        team and WhatsApp selling to your clients under your own brand, on a partner wholesale plan, and keep the
        spread." Ask two questions early: "How many clients do you manage?" and "What do you charge them per month?"
        Those numbers drive the illustrative economics later. Be clear from the start that partner obligations and
        referral commission are still being finalised (CURRENT_OFFER.md; 00_FACTS §2 "Partner wholesale").""",
    }, v)
    return s


def s_reality(prs, v):
    s = new_slide(prs)
    header(s, "The problem we solve", "Marketing and selling, without the patchwork")
    img(s, "problem", "Today: disconnected tools, retainers beyond small budgets, orders lost in chats, after-hours "
        "messages unanswered. With FluxMuse: an AI marketing team in WhatsApp, paid plans from R149, photos to a "
        "catalogue and shop link, answers in the customer's language.")
    notes(s, {
        "default": """Describe the day-to-day reality without numbers we can't back up. Most small businesses juggle
        separate tools for posts, chats and payments. Agency retainers are out of reach for many. Without a shop
        page, orders get lost in chats, and after-hours messages go unanswered. On the right is what changes: an AI
        marketing team that lives in WhatsApp, paid plans from R149 a month, a catalogue and shop link built from
        product photos, and replies in the customer's language. All of these are newly launched (CURRENT_OFFER.md
        §3). Ask which problem hurts most.""",
        "solo": """Talk about their week, not the market. You post when you find time, answer messages late at
        night, and orders get lost in chats because there's no shop page. Paying a marketer or an agency isn't
        realistic yet. On the right: FluxMuse is an AI marketing team in WhatsApp from R149 a month. Send product
        photos and you get a catalogue and a shop link, and the assistant answers in your customer's language. These
        are newly launched, not long-tested (CURRENT_OFFER.md §3). Ask which of these costs them the most sales.""",
        "sme": """For a business with staff, the problem is usually fragmentation. Posts, chats and orders sit in
        separate tools, often run by different people. Agency retainers are hard to justify, staff answer WhatsApp by
        hand, and nobody has a clear view of what sells. On the right is the FluxMuse answer: an AI marketing team
        in WhatsApp, a catalogue and shop link from product photos, and replies in the customer's language. These
        features are newly launched (CURRENT_OFFER.md §3). Ask how many tools they pay for today, and who owns
        each one.""",
    }, v)
    return s


def s_meet(prs, v):
    s = new_slide(prs, dark=True)
    g = gid("hdr")
    text(s, MX, 1.35, 4.3, 0.3, "MEET FLUXMUSE", size=12, bold=True, color=ORANGE, role="eyebrow", group=g, spc=150)
    text(s, MX, 1.72, 4.3, 2.3, "One AI team for marketing and sales", size=34, font=HEAD, bold=True,
         color=PAPER, role="title", group=g, lsp=0.95)
    text(s, MX, 4.1, 4.1, 1.0, "AI marketing and a WhatsApp shop, for South African businesses.",
         size=17, color="D5DADF", role="body")
    g = gid()
    box(s, MX, 5.35, 3.95, 0.52, fill=ORANGE, shape="round", radius=0.26, role="chip", group=g)
    text(s, MX, 5.35, 3.95, 0.52, "Set up by hand", size=14, bold=True, color=NIGHT,
         align="c", anchor="m", role="chip", group=g)
    cols = [("LIVE, NEWLY LAUNCHED", ORANGE, "checkCircle",
             ["Photos to catalogue", "Shop link", "Order alerts", "AI posts & clips", "TikTok video"]),
            ("BEING SWITCHED ON", MUTED_DARK, "clock",
             ["Checkout", "Facebook & Instagram", "AI Voice (beta)"])]
    for c, (head, col, ic, items) in enumerate(cols):
        x = 5.3 + c * 3.83
        g = gid("meet")
        box(s, x, 1.35, 3.6, 5.0, fill=NIGHT_CARD, shape="round", radius=0.2, role="card", group=g)
        text(s, x + 0.3, 1.6, 3.0, 0.3, head, size=12, bold=True, color=col, role="eyebrow", group=g, spc=120)
        for i, t in enumerate(items):
            y = 2.15 + i * 0.78
            gg = icon(s, ic, "orange" if c == 0 else "white", x + 0.55, y + 0.28, 0.5)
            text(s, x + 0.95, y, 2.5, 0.56, t, size=15, color=PAPER, anchor="m", role="card", group=gg)
    notes(s, """Here's FluxMuse in one line: an AI marketing team and WhatsApp shop for South African businesses. Be
    precise about what's live. Live and newly launched: photos to catalogue on WhatsApp, a hosted shop link, order
    alerts with SOLD, AI captions, images and short clips, and TikTok video posting. Being switched on: checkout
    through FluxMuse, Facebook and Instagram auto-posting, and AI Voice in beta. Newly launched means built and
    deployed, but no business has run it end to end yet, so we set you up by hand (CURRENT_OFFER.md §3). Ask
    whether they already use WhatsApp Business.""", v)
    return s


def s_how(prs, v):
    s = new_slide(prs)
    header(s, "How FluxMuse works", "One loop, run by your AI marketing team")
    img(s, "how", "Loop: Plan, Create (captions, images, short clips), Publish (WhatsApp Status, consented "
        "broadcasts, TikTok), Sell (shop link from photos, every order on WhatsApp), Learn")
    notes(s, """FluxMuse works as a loop. Plan: your goals, products and the week ahead. Create: captions, images and
    short video clips, in your customers' languages. Publish: forward to WhatsApp Status, send broadcasts to
    contacts who have opted in, and post video to TikTok. Sell: a shop link built from your photos, with every
    order landing on WhatsApp. Learn: what sold, and what to post next. Facebook and Instagram auto-posting is
    being switched on, so don't promise it yet (CURRENT_OFFER.md §3). The point is that marketing and selling stop
    living in separate tools.""", v)
    return s


def s_sell(prs, v):
    s = new_slide(prs)
    header(s, "WhatsApp selling", "From first tap to repeat order, on WhatsApp")
    img(s, "flow", "Discover, Chat, Catalog, Cart, Pay (Paystack, South Africa, being switched on), Order alert, "
        "Come back; checkout through FluxMuse not yet tested with real money")
    notes(s, """This is the heart of the pitch. A buyer finds you through a Status post, a QR code or your shop link.
    The assistant replies in their language. They browse a catalogue built from your photos, fill a cart, and the
    order lands on your WhatsApp; you reply SOLD to keep track. Be honest about payment: checkout through FluxMuse
    on Paystack is built but being switched on, because it hasn't been tested end to end with real money. Until
    then, orders arrive as a WhatsApp message and you take payment your usual way (CURRENT_OFFER.md §3). Broadcasts
    go only to consented contacts.""", v)
    return s


def s_channels(prs, v):
    s = new_slide(prs)
    if v == "sme":
        header(s, "Platform", "Live today, and being switched on")
        img(s, "stack", "Six layers: channels, AI team, shop and orders, growth, integrations, trust; each chip "
            "marked live, being switched on or not available")
    else:
        header(s, "Channels", "Where FluxMuse works today")
        img(s, "hub", "FluxMuse AI team: live on WhatsApp Business, WhatsApp Status, hosted shop link, TikTok video "
            "and consented broadcasts; Facebook Pages, Instagram posts and WhatsApp ads being switched on; "
            "Instagram DMs and X posting not available")
    notes(s, {
        "default": """Be precise about channels. Live today: WhatsApp Business, WhatsApp Status, the hosted shop
        link, TikTok video posting and broadcasts to consented contacts. Being switched on: Facebook Pages and
        Instagram posting, because Meta hasn't approved those permissions yet, and click-to-WhatsApp ads, which we
        run on our own account first. Not available: Instagram DMs and comments, and X posting. If Instagram is
        their main channel, say so honestly: until Meta approves it, the value is forwarding posts to WhatsApp
        Status (CURRENT_OFFER.md §3).""",
        "sme": """This is the whole platform, with every piece labelled. Solid chips are live and newly launched:
        WhatsApp Business, Status, TikTok video, consented broadcasts, catalogue from photos, captions, images,
        clips, voice-note transcription, the shop link and order alerts. Dashed chips are being switched on:
        Facebook and Instagram posting, AI Voice in beta, Paystack checkout, the daily digest, click-to-WhatsApp ads
        and Shopify, WooCommerce and Takealot sync. Instagram DMs and X posting are not available. Labels follow
        CURRENT_OFFER.md §3. Ask which piece matters most to them.""",
    }, v)
    return s


def s_paid(prs, v):
    s = new_slide(prs)
    header(s, "Payments coverage", "Live in South Africa. The rest is pending.")
    img(s, "map", "Tile map: South Africa live with Paystack; Nigeria, Kenya and Ghana priced, not on sale; other "
        "countries provider contracted, account pending; Botswana and Namibia coming soon")
    notes(s, """Be straight about payments. FluxMuse is open for paid sign-up in South Africa only, where Paystack is
    live. Checkout through FluxMuse for your buyers is built and being switched on; it hasn't been tested end to end
    with real money yet. Nigeria, Kenya and Ghana are priced but not on sale, because the provider accounts are
    still pending. pawaPay and Fincra are contracted for expansion, with accounts pending, so the other countries
    on the map are not open. Botswana and Namibia are coming soon. Source: CURRENT_OFFER.md §3 and §4; 00_FACTS
    §3.""", v)
    return s


def s_segments(prs, v):
    s = new_slide(prs, dark=True)
    g = gid("hdr")
    text(s, MX, 0.85, CW, 0.3, "BUILT FOR YOU", size=12, bold=True, color=ORANGE, role="eyebrow", group=g, spc=150)
    text(s, MX, 1.15, CW, 0.8, "Built for businesses like yours", size=36, font=HEAD, bold=True, color=PAPER,
         role="title", group=g)
    text(s, MX, 1.98, CW, 0.4, "South Africa first.", size=18, color=MUTED_DARK, role="body")
    cards = [("users", "Solo entrepreneurs", "Founder-run, 1–5 people", "Nano · R149/mo"),
             ("briefcase", "SMEs", "5–200 staff", "Growth · R1,999/mo"),
             ("layers", "Agencies & partners", "Managing 5–50 clients", "Partner · R6,999/mo")]
    cwid, gap = 3.84, (CW - 3 * 3.84) / 2
    for i, (ic, name, who, tier) in enumerate(cards):
        x = MX + i * (cwid + gap)
        g = gid("seg")
        box(s, x, 2.85, cwid, 3.7, fill=NIGHT_CARD, shape="round", radius=0.2, role="card", group=g)
        icon(s, ic, "ink", x + 0.8, 3.65, 0.9, circle=ORANGE, group=g)
        text(s, x + 0.35, 4.25, cwid - 0.7, 0.9, name, size=22, font=HEAD, bold=True, color=PAPER, role="card",
             group=g, anchor="b", lsp=0.95)
        text(s, x + 0.35, 5.25, cwid - 0.7, 0.4, who, size=16, color=MUTED_DARK, role="card", group=g)
        text(s, x + 0.35, 5.8, cwid - 0.7, 0.45, tier, size=18, bold=True, color=ORANGE, role="card", group=g)
    notes(s, """FluxMuse is built for three kinds of business, starting in South Africa, the only market open for paid
    sign-up today. Solo entrepreneurs run founder-led businesses of one to five people and usually start on Nano at
    R149 a month, or Micro at R289 for a WhatsApp number. SMEs have five to 200 staff and typically run Growth at
    R1,999, or Starter at R499 for one brand. Agencies managing five to 50 clients join the partner programme at a
    wholesale R6,999 a month. Prices: CURRENT_OFFER.md §1. Ask which fits, then go to that slide.""", v)
    return s


def s_seg_solo(prs, v):
    s = new_slide(prs)
    header(s, "Launch segment · Solo entrepreneurs", "Solo entrepreneurs: 1–5 people")
    img(s, "solo", "Solo entrepreneurs: three pains, three newly launched answers, Nano R149 a month, Founding "
        "Member R104 for the first two bills")
    notes(s, """Solo entrepreneurs are braiders and beauty studios, fashion resellers, home bakers, coaches and
    informal retailers. Their pains are simple: no time or budget for a marketer, messages answered late, and no
    shop page, so orders get lost in chats. FluxMuse answers each one with newly launched features: say POST to get
    a caption and picture, the assistant answers in the customer's language, and product photos become a shop link.
    Nano is R149 a month; Founding Members pay R104 for the first two bills. Micro at R289 adds a channel and their
    own WhatsApp number (CURRENT_OFFER.md §1).""", v)
    return s


def s_seg_sme(prs, v):
    s = new_slide(prs)
    header(s, "Launch segment · SMEs", "SMEs: 5–200 staff")
    img(s, "sme", "SMEs: three pains, three newly launched answers, Growth R1,999 a month, Founding Member R1,399 "
        "for the first two bills")
    notes(s, """SMEs are retailers, restaurants, e-commerce brands, clinics, property, auto and education businesses
    with five to 200 staff. The usual story: disconnected tools and agency retainers, WhatsApp handled by hand by
    busy staff, and no clear view of what sells. FluxMuse puts an AI marketing team on WhatsApp, answers customers
    in their language, and sends an order alert for every sale. Growth at R1,999 a month is the usual start: three
    brands and 15 channels. Scale at R4,999 suits multi-brand groups. Founding Members pay R1,399 for the first two
    Growth bills (CURRENT_OFFER.md §1).""", v)
    return s


def s_seg_agency(prs, v):
    s = new_slide(prs)
    header(s, "Launch segment · Agencies & partners", "Agencies: serve more clients, your brand")
    img(s, "agency", "Agencies: three pains, three answers, Agency tier R9,999 list, partner price R6,999 a month")
    notes(s, """Agencies and freelancers managing five to 50 small-business clients feel a margin squeeze, spend
    hours on reporting and tools per client, and have clients asking for WhatsApp selling and AI. FluxMuse gives
    them one white-label, multi-client platform with unlimited brands and 80 channels. Partners buy the Agency tier
    at a wholesale price of R6,999 a month, 30% off the R9,999 list price, and set their own retail price. Don't
    quote a fixed margin: it depends on the agency's pricing and delivery costs (00_FACTS §2 "Partner
    wholesale").""", v)
    return s


def s_partner_model(prs, v):
    s = new_slide(prs)
    header(s, "Agency partner model · illustrative economics", "Resell FluxMuse under your own brand")
    img(s, "partner", "FluxMuse to agency at the partner price R6,999 a month to clients at a retail price the agency "
        "sets; illustrative example of 20 clients at R1,500 giving a R23,001 gross spread")
    notes(s, """Here's how the partner model works. FluxMuse invoices the agency the partner wholesale price of R6,999 a
    month, 30% off the R9,999 Agency list price. The agency serves its clients under its own brand and bills them a
    retail price it sets. The example is illustrative only, not a forecast: 20 clients at R1,500 a month bills
    R30,000, and after R6,999 the agency keeps a gross spread of R23,001 a month, before its own costs. Encourage
    them to run their own numbers. Referral commission is still to be decided (00_FACTS §2 "Partner
    wholesale").""", v)
    return s


def s_journey(prs, v):
    s = new_slide(prs)
    header(s, "Working with FluxMuse", "From first call to your first orders")
    img(s, "journey", "Discovery call, demo on your products, set up by hand, go live (lead guarantee starts), weekly "
        "check-ins, keep growing; measures agreed together")
    notes(s, """This is how we work together. First a discovery call about your goals and products. Then a demo shop
    built from your own public photos, shown live; that's a demo, not a trial. Once you choose a paid plan, we set
    you up by hand: WhatsApp Business number, catalogue and shop link. On go-live day the lead guarantee starts:
    three qualified leads in 30 days, as long as you share your link and post weekly; if not, we keep supporting you
    at no extra charge. Then weekly check-ins. Goals are agreed together, not promised results (CURRENT_OFFER.md
    §2).""", v)
    return s


def s_first_group(prs, v):
    s = new_slide(prs)
    header(s, "Our first group of businesses", "Starting small, set up by hand")
    g = gid("fg")
    box(s, MX, 1.68, 5.95, 5.05, fill=MIST, shape="round", radius=0.2, role="card", group=g)
    text(s, MX + 0.4, 1.98, 5.1, 0.5, "A small first group", size=22, font=HEAD, bold=True, role="card", group=g)
    rows = [("users", "We set you up by hand"), ("calendar", "Weekly founder check-ins"),
            ("chat", "You tell us what to fix first"), ("shield", "Your story shared only with consent")]
    for i, (ic, t) in enumerate(rows):
        y = 2.75 + i * 0.95
        gg = icon(s, ic, "deep", MX + 0.68, y + 0.36, 0.56, circle=PAPER)
        text(s, MX + 1.15, y, 4.5, 0.74, t, size=16, anchor="m", role="body", group=gg)
    x = MX + 5.95 + 0.233
    g = gid("lg")
    box(s, x, 1.68, 5.95, 5.05, fill=TINT, shape="round", radius=0.2, role="card", group=g)
    icon(s, "target", "deep", x + 0.75, 2.4, 0.86, circle=PAPER, group=g)
    text(s, x + 1.4, 2.12, 4.2, 0.3, "LEAD GUARANTEE", size=13, bold=True, color=DEEP, role="eyebrow", group=g, spc=120)
    text(s, x + 1.4, 2.42, 4.3, 0.95, GUARANTEE_HEAD, size=22, font=HEAD, bold=True, role="card", group=g, lsp=0.95)
    text(s, x + 0.4, 3.75, 5.15, 2.7, GUARANTEE_TERMS, size=15, color=INK, role="caption", group=g, lsp=1.1)
    notes(s, """Be honest about where we are. FluxMuse is newly launched and has no paying customers or case studies
    yet. We're opening with a small first group of South African businesses, and we set each one up by hand, with
    weekly check-ins. That's the offer: close attention, not social proof. It's backed by the lead guarantee: three
    qualified leads in 30 days of go-live. If fewer arrive, and the business shared its link and posted at least
    weekly, we keep supporting them at no extra charge until three arrive. It is extra support, never cash back
    (CURRENT_OFFER.md §2 and §4).""", v)
    return s


def s_case(prs, v):
    s = new_slide(prs)
    header(s, "Case study template · no data yet", "What we'll measure, with your consent")
    img(s, "case", "Empty case-study template stamped Template, no data yet, consent first; goals are not results")
    notes(s, """This is a template, not a case study. No case study exists yet, and we never show projected results.
    When a business in our first group agrees, we record what we set up in week one, using live features only, and
    track three measures: qualified leads, with the lead guarantee's three in 30 days as the goal (if the business shares
    its link and posts weekly), orders through the shop link, and posts made. Each is a goal agreed at kickoff, not a result. We fill it only with measured data and the
    business's signed consent (07_Case_Studies/First_Group_Case_Studies.md; 00_FACTS §6). Hide this slide if time
    is short.""", v)
    return s


def s_pricing(prs, v):
    s = new_slide(prs)
    header(s, "Pricing (ZAR) · every paid plan starts with payment", "Nine plans in three bands, priced in rands")
    img(s, "tiers", "Nine plans: Small (Free, Nano R149, Micro R289), Medium (Starter R499, Growth R1,999, Scale "
        "R4,999), Enterprise (Corporate R6,999, Agency R9,999, Custom); annual 10 times monthly")
    notes(s, """Nine plans in three bands, priced in rands, and the price shown is what you pay. Small: Nano at R149 and
    Micro at R289 for side-hustles and solo sellers. Medium: Starter R499, Growth R1,999 with inbound AI Voice in
    beta, and Scale R4,999 with inbound and outbound AI Voice in beta. Enterprise: Corporate R6,999, Agency R9,999,
    and Custom by consultation. Annual billing is ten times monthly. There are no trials: every paid plan starts with
    payment. Free is a permanent plan, so don't lead with it. Don't quote AI credit allowances; point to the pricing
    page (CURRENT_OFFER.md §1).""", v)
    return s


PLAN_CARDS = {
    "solo": [("Nano", "R149", "R1,490", "1 brand · 3 channels", "Entry plan", "R104"),
             ("Micro", "R289", "R2,890", "1 brand · 4 channels", "Own WhatsApp number", "R202"),
             ("Starter", "R499", "R4,990", "1 brand · 3 channels", "Room to grow", "R349")],
    "sme": [("Starter", "R499", "R4,990", "1 brand · 3 channels", "One brand", "R349"),
            ("Growth", "R1,999", "R19,990", "3 brands · 15 channels", "+ AI Voice (beta)", "R1,399"),
            ("Scale", "R4,999", "R49,990", "10 brands · 40 channels", "+ outbound Voice (beta)", "R3,499")],
}


def s_plans(prs, v):
    s = new_slide(prs)
    header(s, "Pricing (ZAR) · your plans", "Plans that fit a small business" if v == "solo" else "Plans for a growing team")
    cwid = 3.84
    gapx = (CW - 3 * cwid) / 2
    for i, (name, mo, yr, bc, note, fm) in enumerate(PLAN_CARDS[v]):
        x = MX + i * (cwid + gapx)
        g = gid("plan")
        hl = i == (0 if v == "solo" else 1)
        box(s, x, 1.68, cwid, 4.3, fill=TINT if hl else MIST, line=ORANGE if hl else None, lw=2,
            shape="round", radius=0.2, role="card", group=g)
        text(s, x + 0.35, 1.95, cwid - 0.7, 0.5, name, size=22, font=HEAD, bold=True, role="card", group=g)
        text(s, x + 0.35, 2.5, cwid - 0.7, 0.8, [[(mo, {}), ("/mo", {"size": 16, "bold": False, "font": BODY})]],
             size=36, font=HEAD, bold=True, role="card", group=g)
        text(s, x + 0.35, 3.3, cwid - 0.7, 0.3, f"or {yr}/yr", size=13, color=MUTED, role="caption", group=g)
        text(s, x + 0.35, 3.75, cwid - 0.7, 0.4, bc, size=15, role="card", group=g)
        text(s, x + 0.35, 4.2, cwid - 0.7, 0.4, note, size=15, color=DEEP, bold=True, role="card", group=g)
        text(s, x + 0.35, 4.95, cwid - 0.7, 0.8, [{"runs": "FOUNDING MEMBER", "size": 11, "bold": True, "color": DEEP,
                                                   "space_after": 2},
                                                  f"{fm} for your first 2 bills"],
             size=13, color=INK, role="caption", group=g)
    text(s, MX, 6.2, CW, 0.6, [{"runs": "Prices in rands are what you pay. Every paid plan starts with payment; no "
                                        "trials. Annual = 10× monthly. AI credit allowances: see fluxmuse.ai/pricing.",
                                "space_after": 2},
                               "Founding Member: 30% off your first two monthly bills, South African sign-ups, while "
                               "it lasts."],
         size=12, color=MUTED, role="caption")
    notes(s, {
        "solo": """Most solo businesses start on Nano: R149 a month for one brand and three channels. Micro at R289
        adds a fourth channel and connects their own WhatsApp number. Starter at R499 is the step up as they grow.
        Annual billing is ten times monthly. There's no trial: every paid plan starts with payment. As a Founding
        Member, a South African sign-up pays 30% less for the first two monthly bills: R104 on Nano, R202 on Micro.
        It's a discount, not a free period, and it has no set end date. Don't quote AI credit numbers
        (CURRENT_OFFER.md §1).""",
        "sme": """Most SMEs start on Growth at R1,999 a month: three brands, 15 channels and inbound AI Voice in beta.
        Single-brand businesses can start on Starter at R499. Multi-brand groups should look at Scale at R4,999: ten
        brands, 40 channels, and inbound and outbound AI Voice in beta, which we evaluate together. Annual billing is
        ten times monthly. No trials: every paid plan starts with payment. Founding Members in South Africa pay 30%
        less for the first two bills: R1,399 on Growth. Larger groups: Corporate or Custom (CURRENT_OFFER.md §1).""",
    }, v)
    return s


def s_pricing_table(prs, v):
    s = new_slide(prs)
    header(s, "Pricing (ZAR) · editable", "Plans at a glance")
    hdr = {"fill": NIGHT, "color": PAPER, "bold": True, "font": HEAD, "size": 14, "line": None}
    rows = [[dict(hdr, text="Band", align="l"), dict(hdr, text="Plan", align="l"), dict(hdr, text="Monthly"),
             dict(hdr, text="Annual"), dict(hdr, text="Brands · channels"),
             dict(hdr, text="Founding Member, first 2 bills")]]
    data = [("Small", "Free", "R0", "R0", "1 · 1", "Free forever, no card"),
            ("", "Nano", "R149", "R1,490", "1 · 3", "R104"),
            ("", "Micro", "R289", "R2,890", "1 · 4", "R202"),
            ("Medium", "Starter", "R499", "R4,990", "1 · 3", "R349"),
            ("", "Growth", "R1,999", "R19,990", "3 · 15", "R1,399"),
            ("", "Scale", "R4,999", "R49,990", "10 · 40", "R3,499"),
            ("Enterprise", "Corporate", "R6,999", "R69,990", "25 · 60", "Talk to us"),
            ("", "Agency", "R9,999", "R99,990", "Unlimited · 80", "Partner price R6,999"),
            ("", "Custom", "On request", "", "By consultation", "")]
    for r in data:
        fill = TINT if r[1] == "Growth" else PAPER
        rows.append([{"text": r[0], "bold": True, "fill": fill, "align": "l"},
                     {"text": r[1], "bold": True, "fill": fill, "align": "l"},
                     {"text": r[2], "bold": True, "fill": fill}] + [{"text": t, "fill": fill} for t in r[3:]])
    table(s, MX, 1.55, [1.6, 1.6, 1.6, 1.7, 2.3, 3.33], [0.46] + [0.43] * 9, rows, size=14, label="pricing-zar")
    text(s, MX, 6.42, CW, 0.5, "Prices are what you pay. No trials: every paid plan starts with payment; Free is a "
         "permanent plan. AI credit allowances: see fluxmuse.ai/pricing. Paid sign-up is open in South Africa.",
         size=12, color=MUTED, role="caption")
    notes(s, """This is the same pricing as an editable table, useful when you tailor the deck. It shows all nine plans
    with monthly and annual prices, where annual is ten times monthly, plus brands and channels. The Founding Member
    column is 30% off the first two monthly bills for South African sign-ups, rounded down to whole rands. Agencies
    don't get Founding Member pricing; point them to the R6,999 partner price instead. Corporate launch pricing is
    by conversation. If you edit a price, check it against CURRENT_OFFER.md §1 first, and never add per-plan AI
    credit numbers.""", v)
    return s


def s_founding(prs, v):
    s = new_slide(prs)
    header(s, "Launch offer · South Africa · live now", "Become a Founding Member")
    img(s, "founding", "Founding Member: 30% off your first two monthly bills, South African sign-ups, while it "
        "lasts: Nano R104, Micro R202, Starter R349, Growth R1,399, Scale R3,499; a discount, not a free period")
    notes(s, {
        "default": """Our launch offer is Founding Member, and it's live now. South African sign-ups get 30% off
        their first two monthly bills on a paid plan: R104 on Nano, R202 on Micro, R349 on Starter, R1,399 on Growth
        or R3,499 on Scale, then the normal monthly price. It's a discount, not a free period. There's no set end
        date, so say "while it lasts" and never quote a closing date. Agencies get the partner price instead. Don't
        offer annual bonus months or other perks; they aren't confirmed (00_FACTS §2 "Founding Member").""",
        "solo": """Here's the easiest yes. Join as a Founding Member and your first two Nano bills are R104 instead
        of R149, or R202 instead of R289 on Micro. After that it's the normal monthly price. It's a discount on a
        paid plan, not a free period, and it's for South African sign-ups while it lasts; there's no closing date to
        quote. Don't promise extra perks like badges or bonus months; only the discount is confirmed. Then offer the
        demo on their own products (00_FACTS §2 "Founding Member").""",
        "sme": """Founding Member is live now for South African sign-ups: 30% off the first two monthly bills. On
        Growth that's R1,399 instead of R1,999 for two months; on Scale R3,499 instead of R4,999; on Starter R349.
        Then the normal price. It's a discount, not a free period, and there's no set end date, so say "while it
        lasts". Don't offer bonus months on annual plans or other perks; only the discount is confirmed. Larger
        groups on Corporate: talk to us (00_FACTS §2 "Founding Member").""",
    }, v)
    return s


def s_trust(prs, v):
    s = new_slide(prs)
    header(s, "Trust & compliance", "Built to protect your customers' data")
    cards = [("checkCircle", "Meta Tech Provider", "Verified by Meta"),
             ("chat", "Official WhatsApp API", "Meta Cloud API"),
             ("shield", "POPIA-aligned", "Consented broadcasts only"),
             ("layers", "Row-level security", "Your data kept separate"),
             ("plug", "Encrypted tokens", "Connected accounts"),
             ("refresh", "Data export & deletion", "Export data, delete account")]
    cwid, ch = 3.84, 2.42
    gapx = (CW - 3 * cwid) / 2
    for i, (ic, t, sub) in enumerate(cards):
        x = MX + (i % 3) * (cwid + gapx)
        y = 1.68 + (i // 3) * (ch + 0.22)
        g = gid("trust")
        box(s, x, y, cwid, ch, fill=MIST, shape="round", radius=0.18, role="card", group=g)
        icon(s, ic, "deep", x + 0.68, y + 0.68, 0.78, circle=PAPER, group=g)
        text(s, x + 0.32, y + 1.2, cwid - 0.6, 0.5, t, size=18, font=HEAD, bold=True, role="card", group=g)
        text(s, x + 0.32, y + 1.7, cwid - 0.6, 0.45, sub, size=14, color=MUTED, role="card", group=g)
    notes(s, """Trust matters when you're handling customer chats. Fluxmuse (Pty) Ltd is a verified Meta Tech
    Provider, with business and access verification, and WhatsApp runs on Meta's official Cloud API. Broadcasts go
    only to contacts who have opted in, in line with POPIA. Under the hood there's row-level security, encrypted
    tokens for connected accounts, and data export and account deletion. If they ask for a data processing
    agreement, a security questionnaire or certifications, don't improvise: note the request and follow up in
    writing (CURRENT_OFFER.md §4; 00_FACTS §1).""", v)
    return s


def s_roadmap(prs, v):
    s = new_slide(prs)
    header(s, "Roadmap · indicative, no dates", "What comes next, in order")
    img(s, "roadmap", "Indicative order, no dates. Markets: South Africa open now, then checkout through FluxMuse, "
        "then Nigeria, Kenya and Ghana, then other markets in USD. Product: Meta permissions, social adapters, "
        "business apps, partner programme")
    notes(s, {
        "default": """Here's what comes next, in order, with no dates. On markets: South Africa is open now, with
        Paystack live. Next, checkout through FluxMuse, switched on once it's tested end to end with real money.
        Then Nigeria, Kenya and Ghana, once the pawaPay and Fincra accounts are live. Later, other markets in US
        dollars; Botswana and Namibia are coming soon. On product: Meta permissions for Facebook and Instagram
        posting, then social adapters, business app integrations, and the partner programme. Timing depends on
        approvals, so don't give dates (00_FACTS §1 "Roadmap").""",
        "partner": """Here's what comes next, in order, with no dates. On markets: South Africa is open now. Next,
        checkout through FluxMuse once it's tested with real money. Then Nigeria, Kenya and Ghana, once provider
        accounts are live, and later other markets in US dollars. On product: Meta permissions for Facebook and
        Instagram posting, then social adapters, business apps, then the partner programme layer with referral
        tracking and partner-managed workspaces. White-label and multi-client are on the Agency tier today; the
        programme layer comes later (00_FACTS §1 "Roadmap").""",
    }, v)
    return s


CONTACT = [{"runs": "Thabo Malebadi", "bold": True, "color": PAPER, "space_after": 2},
           {"runs": "Founder", "space_after": 4}, {"runs": "thabo@fluxmuse.com", "space_after": 4}, "fluxmuse.ai"]


def s_next(prs, v):
    s = new_slide(prs, dark=True)
    g = gid("hdr")
    text(s, MX, 0.8, CW, 0.3, "NEXT STEPS", size=12, bold=True, color=ORANGE, role="eyebrow", group=g, spc=150)
    title = "Let's build your partner practice" if v == "partner" else "Let's get you selling on WhatsApp"
    text(s, MX, 1.1, CW, 0.8, title, size=36, font=HEAD, bold=True, color=PAPER, role="title", group=g)
    ctas = {
        "default": [("Book a 20-minute call", "Goals, channels, products."),
                    ("See a demo on your products", "Built from your own photos."),
                    ("Choose a plan, we set you up", "Paid plans from R149/mo.")],
        "solo": [("Book a 20-minute call", "Goals, products, customers."),
                 ("See a demo on your products", "Built from your own photos."),
                 ("Join as a Founding Member", "First 2 Nano bills at R104.")],
        "sme": [("Book a 20-minute call", "Goals, channels, tools and team."),
                ("See a demo on your products", "Built from your own photos."),
                ("Get a tailored proposal", "Starter, Growth, Scale or Corporate.")],
        "partner": [("Book a 30-minute partner call", "Your clients, services and pricing."),
                    ("See a white-label demo", "FluxMuse under your brand."),
                    ("Apply to become a partner", "Agency tier at R6,999/mo wholesale.")],
    }
    for i, (t, sub) in enumerate(ctas.get(v, ctas["default"])):
        y = 2.25 + i * 1.42
        g = gid("cta")
        box(s, MX, y, 7.55, 1.22, fill=NIGHT_CARD, shape="round", radius=0.18, role="card", group=g)
        box(s, MX + 0.32, y + 0.3, 0.62, 0.62, fill=ORANGE, shape="oval", role="deco", group=g)
        text(s, MX + 0.32, y + 0.3, 0.62, 0.62, str(i + 1), size=20, font=HEAD, bold=True, color=NIGHT, align="c",
             anchor="m", role="card", group=g)
        text(s, MX + 1.2, y + 0.2, 6.15, 0.45, t, size=20, font=HEAD, bold=True, color=PAPER, role="card", group=g)
        text(s, MX + 1.2, y + 0.7, 6.15, 0.38, sub, size=15, color=MUTED_DARK, role="card", group=g)
    g = gid("contact")
    box(s, 8.5, 2.25, 4.23, 4.06, fill=NIGHT_CARD, shape="round", radius=0.18, role="card", group=g)
    text(s, 8.85, 2.5, 3.6, 0.3, "TALK TO US", size=12, bold=True, color=ORANGE, role="eyebrow", group=g, spc=150)
    text(s, 8.85, 2.85, 3.6, 1.4, CONTACT, size=15, color="D5DADF", role="body", group=g)
    box(s, 8.85, 4.4, 1.5, 1.5, fill=None, line=MUTED_DARK, lw=1.25, dash=True, shape="round", radius=0.1,
        role="deco", group=g)
    text(s, 8.85, 4.4, 1.5, 1.5, "[[wa.me QR CODE]]", size=11, color=MUTED_DARK, align="c", anchor="m",
         role="caption", group=g)
    text(s, 10.55, 4.5, 2.0, 1.4, [{"runs": "Scan to chat on WhatsApp", "space_after": 6},
                                   {"runs": "wa.me/", "color": PAPER, "bold": True},
                                   {"runs": "[[NUMBER]]", "color": PAPER, "bold": True}],
         size=14, color=MUTED_DARK, role="placeholder", group=g)
    notes(s, {
        "default": """Close with one clear next step, and agree it before the call ends. Option one: book a
        20-minute call to map goals, channels and products. Option two: see a demo shop built from their own public
        product photos; it's a demo, not a trial, with nothing to sign up for. Option three: choose a paid plan, and
        we set them up by hand. Contact is Thabo Malebadi, thabo@fluxmuse.com. Follow up within 24 hours with this
        deck and a short summary (CURRENT_OFFER.md §2).""",
        "solo": """Close with one clear next step. The simplest is a demo shop built from their own public product
        photos, shown live; it's a demo, not a trial. If they're ready, they join as a Founding Member on Nano: R104
        for each of the first two bills, then R149, and we set them up by hand. If they want to think first, book a
        20-minute call. Contact is Thabo Malebadi, thabo@fluxmuse.com. Follow up within 24 hours with a short summary
        (CURRENT_OFFER.md §1 and §2).""",
        "sme": """Close with one agreed next step and an owner for it. Option one: a 20-minute call with the people
        who run marketing, sales and operations, to map goals, channels, tools and team. Option two: a demo shop
        built from their own public photos, shown live. Option three: a tailored proposal for Starter, Growth, Scale
        or Corporate. Contact is Thabo Malebadi, thabo@fluxmuse.com. Follow up within 24 hours with the deck and a
        short written summary (CURRENT_OFFER.md §2).""",
        "partner": """Close with a concrete partner next step. Option one: a 30-minute partner call to go through
        their clients, services and pricing. Option two: a white-label demo so they can see FluxMuse under their
        brand. Option three: apply to become a partner on the Agency tier at R6,999 a month wholesale, starting
        with one first client we set up together. Contact is Thabo Malebadi, thabo@fluxmuse.com. Don't commit to
        commission or obligations that are still to be confirmed.""",
    }, v)
    return s


# ---------------------------------------------------------------- SME-only
def s_sme_integrations(prs, v):
    s = new_slide(prs)
    header(s, "Your tools & your team", "Fits how your team already works")
    g = gid("intg")
    box(s, MX, 1.68, 5.95, 5.05, fill=MIST, shape="round", radius=0.2, role="card", group=g)
    icon(s, "plug", "deep", MX + 0.62, 2.22, 0.66, circle=PAPER, group=g)
    text(s, MX + 1.1, 1.97, 4.5, 0.5, "Being switched on", size=20, font=HEAD, bold=True, role="card", group=g)
    chips = ["Shopify sync", "WooCommerce sync", "Takealot sync", "FB/Instagram posts", "AI Voice (beta)",
             "Daily digest"]
    for i, c in enumerate(chips):
        x = MX + 0.35 + (i % 2) * 2.7
        y = 2.9 + (i // 2) * 0.8
        gg = gid()
        box(s, x, y, 2.5, 0.6, fill=PAPER, line=MUTED, lw=1, dash=True, shape="round", radius=0.3, role="chip",
            group=gg)
        text(s, x, y, 2.5, 0.6, c, size=14, bold=True, align="c", anchor="m", role="chip", group=gg)
    text(s, MX + 0.35, 5.45, 5.3, 0.9, "Until sync is on, we build your catalogue from product photos.", size=13,
         color=MUTED, role="caption", group=g)
    g = gid("team")
    box(s, 6.78, 1.68, 5.95, 5.05, fill=TINT, shape="round", radius=0.2, role="card", group=g)
    icon(s, "users", "deep", 6.78 + 0.62, 2.22, 0.66, circle=PAPER, group=g)
    text(s, 6.78 + 1.1, 1.97, 4.5, 0.5, "Live now", size=20, font=HEAD, bold=True, role="card", group=g)
    rows = [("chat", "Templates & quick replies"), ("layers", "10 brands (Scale)"),
            ("bag", "Order alerts"), ("send", "Consented broadcasts"),
            ("globe", "Replies in their language")]
    for i, (ic, t) in enumerate(rows):
        y = 2.92 + i * 0.72
        gg = icon(s, ic, "deep", 7.4, y + 0.28, 0.5, circle=PAPER)
        text(s, 7.85, y, 4.7, 0.56, t, size=16, anchor="m", role="body", group=gg)
    notes(s, """SMEs rarely start from zero, so be honest about what connects today. On the left is what's being
    switched on: sync from Shopify, WooCommerce and Takealot, which is only partly built, so don't promise it, plus
    Facebook and Instagram posting, AI Voice in beta and the daily digest. Until sync is on, we build the catalogue from product
    photos. On the right is what a team can use now: WhatsApp templates and quick replies, several brands on one
    account, order alerts, consented broadcasts and replies in the customer's language. AI Voice is beta, evaluated
    together (CURRENT_OFFER.md §3).""",
          v)
    return s


# ---------------------------------------------------------------- partner-only
def p_squeeze(prs, v):
    s = new_slide(prs)
    header(s, "The agency squeeze", "What agencies are up against")
    today = [("x", "Margin squeeze on retainers"), ("x", "Manual reporting"), ("x", "Too many tools per client")]
    after = [("check", "Partner price, your retail price"), ("check", "White-label, multi-client"),
             ("check", "WhatsApp selling + AI, your brand")]
    cwid = 3.84
    gapx = (CW - 3 * cwid) / 2
    text(s, MX, 1.62, 4, 0.28, "TODAY", size=12, bold=True, color=MUTED, role="eyebrow", spc=150)
    text(s, MX, 4.12, 4, 0.28, "WITH FLUXMUSE", size=12, bold=True, color=DEEP, role="eyebrow", spc=150)
    for row, (items, fill, col, y) in enumerate([(today, MIST, "ink", 1.98), (after, TINT, "deep", 4.48)]):
        for i, (ic, t) in enumerate(items):
            x = MX + i * (cwid + gapx)
            g = gid("sq")
            box(s, x, y, cwid, 1.6, fill=fill, shape="round", radius=0.18, role="card", group=g)
            icon(s, ic, col, x + 0.62, y + 0.8, 0.66, circle=PAPER, group=g)
            text(s, x + 1.15, y + 0.2, cwid - 1.4, 1.2, t, size=18, font=HEAD, bold=True, anchor="m", role="card", group=g)
            if row == 0:
                box(s, x + cwid / 2 - 0.2, 3.66, 0.4, 0.38, fill=ORANGE, shape="down", role="deco", group=gid())
    notes(s, """Start with the agency's reality. Clients expect more every month, from content to WhatsApp selling to
    AI, while retainers stay flat. Reporting eats hours, and every new client adds another set of tools and logins.
    FluxMuse changes that. Partners buy the Agency tier at the partner price and set their own retail price. They
    run clients from one white-label, multi-client platform with unlimited brands. And they offer an AI marketing
    team on WhatsApp under their own brand. Ask how many tools they pay for per client, and how long reporting
    takes them.""", v)
    return s


def p_what_you_get(prs, v):
    s = new_slide(prs)
    header(s, "Partner plan · Agency tier at wholesale", "Everything you need to resell")
    g = gid("price")
    box(s, MX, 1.68, 4.05, 5.05, fill=TINT, shape="round", radius=0.2, role="card", group=g)
    text(s, MX + 0.4, 2.0, 3.3, 0.36, "PARTNER WHOLESALE", size=13, bold=True, color=DEEP, role="eyebrow", group=g, spc=120)
    text(s, MX + 0.4, 2.4, 3.4, 1.2, "R6,999", size=54, font=HEAD, bold=True, role="card", group=g)
    text(s, MX + 0.4, 3.65, 3.3, 0.7, "per month", size=16, role="card", group=g)
    text(s, MX + 0.4, 4.5, 3.3, 0.7, "30% off the R9,999 Agency list price", size=16, bold=True, role="card", group=g)
    text(s, MX + 0.4, 5.4, 3.3, 0.9, "R69,990 a year. Launch offers don't stack.", size=14,
         color=MUTED, role="card", group=g)
    items = [("layers", "Full white-label"), ("users", "Multi-client workspaces"), ("briefcase", "Unlimited brands"),
             ("globe", "80 channels"), ("plug", "Bring your own cloud"), ("chat", "Set up with you by hand")]
    x0, cwid, ch = 4.95, 3.74, 1.5
    for i, (ic, t) in enumerate(items):
        x = x0 + (i % 2) * (cwid + 0.3)
        y = 1.68 + (i // 2) * (ch + 0.275)
        g = gid("inc")
        box(s, x, y, cwid, ch, fill=PAPER, line=LINE, lw=1.25, shape="round", radius=0.18, role="card", group=g)
        icon(s, ic, "deep", x + 0.65, y + ch / 2, 0.72, circle=TINT, group=g)
        text(s, x + 1.2, y + 0.2, cwid - 1.4, ch - 0.4, t, size=18, font=HEAD, bold=True, anchor="m", role="card", group=g)
    notes(s, """This is what a partner gets on the Agency tier at the partner price: R6,999 a month, 30% off the
    R9,999 list price, or R69,990 a year. Full white-label, so clients see the agency's brand. Multi-client
    workspaces with unlimited brands and 80 channels. Bring your own cloud. And we set the first client up with
    them by hand. Clients get the same product as direct sign-ups: the live, newly launched WhatsApp features.
    Launch offers don't stack with partner pricing. Don't quote AI credit numbers (00_FACTS §2 "Partner
    wholesale"; CURRENT_OFFER.md §1).""", v)
    return s


def wholesale_table(s, y):
    hdr = {"fill": NIGHT, "color": PAPER, "bold": True, "font": HEAD, "size": 16, "line": None}
    ws = lambda t: {"text": t, "fill": TINT, "bold": True}
    rows = [
        [dict(hdr, text="ZAR", align="l"), dict(hdr, text="Per month"), dict(hdr, text="Per year (10×)")],
        [{"text": "Agency list price", "bold": True}, "R9,999", "R99,990"],
        [{"text": "Partner wholesale (−30%)", "bold": True, "fill": TINT}, ws("R6,999"), ws("R69,990")],
    ]
    return table(s, MX, y, [4.6, 3.0, 3.0], [0.62, 0.66, 0.66], rows, size=16, label="wholesale")


def p_wholesale(prs, v, label=None):
    s = new_slide(prs)
    eyebrow = f"Appendix {label} · partner wholesale" if label else "30% off the Agency list price"
    header(s, eyebrow, "Partner wholesale pricing")
    wholesale_table(s, 1.65)
    g = gid("illus")
    box(s, MX, 4.25, 7.35, 2.4, fill=MIST, shape="round", radius=0.18, role="card", group=g)
    text(s, MX + 0.35, 4.45, 6.6, 0.3, "ILLUSTRATIVE ONLY · NOT A FORECAST", size=12, bold=True, color=DEEP,
         role="eyebrow", group=g, spc=120)
    text(s, MX + 0.35, 4.85, 6.7, 1.6, [{"runs": "20 clients × R1,500/mo = R30,000 billed", "space_after": 6},
                                        {"runs": "− R6,999 wholesale = R23,001/mo gross spread, before your own costs",
                                         "size": 16, "bold": False}],
         size=19, font=HEAD, bold=True, role="card", group=g)
    text(s, 8.3, 4.35, 4.43, 2.2, [{"runs": "You set your retail price.", "space_after": 8},
                                   {"runs": "Paid sign-up is South Africa only for now.", "space_after": 8},
                                   "Local-currency partner prices: not set yet."],
         size=14, color=MUTED, role="body")
    notes(s, """Partner wholesale pricing is the Agency tier at 30% off list: R6,999 a month instead of R9,999, or
    R69,990 a year, in rands. Paid sign-up is open in South Africa only for now, so there are no local-currency
    partner prices yet. Launch offers don't stack with partner pricing. The example is illustrative only, not a
    forecast: 20 clients at R1,500 bills R30,000; minus R6,999 leaves a R23,001 gross spread before the partner's
    own costs. Don't quote a fixed margin. Referral commission is still a founder decision (00_FACTS §2 "Partner
    wholesale").""", v)
    return s


def p_onboarding(prs, v):
    s = new_slide(prs)
    header(s, "Becoming a partner", "From first call to first client")
    steps = [("search", "Intro call", "Clients, services, pricing"),
             ("sparkles", "White-label demo", "FluxMuse under your brand"),
             ("target", "First client", "Set up together, by hand"),
             ("briefcase", "Go wholesale", "Agency tier at R6,999/mo"),
             ("megaphone", "Roll out", "Onboard more clients")]
    colw = 2.33
    gapx = (CW - 5 * colw) / 4
    box(s, MX + colw / 2, 2.2, CW - colw, 0.05, fill=ORANGE, role="deco", group="line")
    for i, (ic, t, sub) in enumerate(steps):
        x = MX + i * (colw + gapx)
        cx = x + colw / 2
        g = gid("step")
        box(s, cx - 0.4, 1.83, 0.8, 0.8, fill=PAPER, line=ORANGE, lw=2.25, shape="oval", role="deco", group=g)
        text(s, cx - 0.4, 1.83, 0.8, 0.8, str(i + 1), size=20, font=HEAD, bold=True, color=DEEP, align="c",
             anchor="m", role="card", group=g)
        box(s, x, 2.95, colw, 3.2, fill=MIST, shape="round", radius=0.18, role="card", group=g)
        icon(s, ic, "deep", x + 0.6, 3.6, 0.72, circle=PAPER, group=g)
        text(s, x + 0.25, 4.2, colw - 0.45, 0.8, t, size=18, font=HEAD, bold=True, role="card", group=g)
        text(s, x + 0.25, 4.95, colw - 0.45, 1.1, sub, size=14, color=MUTED, role="card", group=g)
    text(s, MX, 6.4, CW, 0.3, "Timings depend on your team. Partner terms and co-marketing: [[TBC]].", size=12,
         color=MUTED, role="caption")
    notes(s, """Becoming a partner follows a simple path. It starts with an intro call about your clients, services
    and pricing. Then a white-label demo so you can see the platform under your brand. Next, pick one first client
    and we set them up together, by hand, so you learn the workflow on a real account; the lead guarantee applies to
    that client's go-live, with its conditions. Once that's working, move onto the Agency tier at R6,999 a month
    and roll out to more clients. We don't quote fixed timings, and formal partner terms are still being
    confirmed.""", v)
    return s


def p_comarketing(prs, v):
    s = new_slide(prs)
    header(s, "Co-marketing & commitments", "What we bring, and what we ask")
    cols = [("FluxMuse provides", TINT, "check",
             ["Hands-on setup of your first client", "This deck and proposal templates",
              "Consented case studies, once they exist", "Co-marketing support: [[TBC]]"]),
            ("Partners commit to", MIST, "file",
             ["Partner obligations: [[TBC]]", "Minimum active clients: [[TBC]]",
              "Brand and POPIA standards: [[TBC]]",
              "Referral commission: [[FOUNDER DECISION: referral commission %]]"])]
    for c, (head, fill, ic, items) in enumerate(cols):
        x = MX + c * (5.95 + 0.233)
        g = gid("col")
        box(s, x, 1.68, 5.95, 5.05, fill=fill, shape="round", radius=0.2, role="card", group=g)
        text(s, x + 0.4, 1.98, 5.1, 0.5, head, size=22, font=HEAD, bold=True, role="card", group=g)
        for i, t in enumerate(items):
            y = 2.75 + i * 0.95
            gg = icon(s, ic, "deep", x + 0.68, y + 0.36, 0.56, circle=PAPER)
            role = "placeholder" if "[[" in t else "body"
            text(s, x + 1.15, y, 4.5, 0.74, t, size=16, anchor="m", role=role, group=gg)
    notes(s, """Be transparent about what's defined and what isn't. FluxMuse provides hands-on setup of the partner's
    first client, sales material such as this deck and proposal templates, and case studies only once they exist
    and the business has consented; there are none yet. Co-marketing specifics are still being finalised. Partner
    obligations, such as minimum active clients, brand standards and data-protection responsibilities under POPIA,
    are to be confirmed. Referral commission is a founder decision that hasn't been made. Don't promise terms; take
    questions and follow up in writing.""", v)
    return s


# ---------------------------------------------------------------- appendix
def a_divider(prs, v, items):
    s = new_slide(prs, dark=True)
    text(s, MX, 1.5, CW, 0.3, "APPENDIX", size=12, bold=True, color=ORANGE, role="eyebrow", spc=150)
    text(s, MX, 1.82, CW, 0.9, "Reference slides", size=40, font=HEAD, bold=True, color=PAPER, role="title")
    for i, (lab, t) in enumerate(items):
        y = 3.05 + i * 0.78
        g = gid("ax")
        box(s, MX, y, 0.95, 0.56, fill=ORANGE, shape="round", radius=0.28, role="chip", group=g)
        text(s, MX, y, 0.95, 0.56, lab, size=16, font=HEAD, bold=True, color=NIGHT, align="c", anchor="m",
             role="chip", group=g)
        text(s, MX + 1.2, y, 8, 0.56, t, size=20, color=PAPER, anchor="m", role="body", group=g)
    notes(s, """The appendix is for questions and follow-up, not the main talk track. It covers payment status by
    country, partner wholesale pricing where relevant, and the questions prospects ask most. Paid sign-up is open in
    South Africa only. Nigeria, Kenya and Ghana are priced but not on sale, so don't show local prices or offer
    checkout there; anyone outside South Africa, including Botswana and Namibia, gets the waitlist link instead:
    [[WAITLIST LINK]]. Regional price sheets are internal only and are not in customer decks (00_FACTS §2 "Market
    gating").""", v)
    return s


def a_rails(prs, v, label):
    s = new_slide(prs)
    header(s, f"Appendix {label} · payment status", "What is live, and what is still pending")
    img(s, "matrix", "Matrix of countries against payment providers: Paystack live in South Africa; Yoco and Ozow "
        "for FluxMuse subscription billing; pawaPay and Fincra contracted, account pending; Botswana and Namibia "
        "coming soon")
    notes(s, """This matrix shows payment status by country. Only South Africa is open for paid sign-up: Paystack is
    live there, and Yoco and Ozow run FluxMuse's own subscription billing. Checkout through FluxMuse for a
    business's buyers is still being switched on. pawaPay and Fincra are contracted for expansion, but the accounts
    are pending, so none of those countries is open. Nigeria, Kenya and Ghana are priced in local currency but not
    on sale. Botswana and Namibia are coming soon with no provider yet. Source: CURRENT_OFFER.md §3; 00_FACTS
    §3.""", v)
    return s


FAQ = [
    ("Is my customers' data safe?",
     "Row-level security, encrypted tokens, broadcasts only to consented contacts, and data export and account "
     "deletion. Fluxmuse is a verified Meta Tech Provider."),
    ("Can I use my own WhatsApp number?",
     "Yes. We connect your WhatsApp Business number through Meta's official Cloud API setup, with you, by hand."),
    ("How do my customers pay?",
     "Today, orders arrive as a WhatsApp message and you take payment your usual way. Checkout through FluxMuse "
     "(Paystack, South Africa) is being switched on."),
    ("Is there a trial? Can I cancel?",
     "No trials: every paid plan starts with payment, monthly or annual (10× monthly). Free is a permanent plan. "
     "Cancellation terms: [[CONFIRM TERMS]]."),
    ("Is there a guarantee?",
     "A lead guarantee: 3 qualified leads in 30 days of go-live. If fewer, and you shared your link and posted "
     "weekly, we keep supporting you free until you reach 3."),
    ("How long does setup take?",
     "We set you up by hand: WhatsApp number, catalogue from your photos, shop link. We aim for your first week; "
     "Meta approvals can stretch it."),
    ("I already use Shopify or WooCommerce.",
     "Keep them. Sync from Shopify, WooCommerce and Takealot is being switched on. Until then, we build your "
     "catalogue from product photos."),
    ("Where can I buy FluxMuse?",
     "South Africa, today. Nigeria, Kenya and Ghana are priced but not yet on sale. Other countries can join the "
     "waitlist."),
]


def a_faq(prs, v, label, part):
    s = new_slide(prs)
    items = FAQ[:4] if part == 1 else FAQ[4:]
    header(s, f"Appendix {label} · FAQ ({part} of 2)", "Questions prospects ask")
    cwid, ch = 5.95, 2.45
    for i, (q, a) in enumerate(items):
        x = MX + (i % 2) * (cwid + 0.233)
        y = 1.68 + (i // 2) * (ch + 0.2)
        g = gid("faq")
        box(s, x, y, cwid, ch, fill=MIST, shape="round", radius=0.18, role="card", group=g)
        icon(s, "chat", "deep", x + 0.55, y + 0.58, 0.6, circle=PAPER, group=g)
        text(s, x + 1.0, y + 0.2, cwid - 1.3, 0.78, q, size=17, font=HEAD, bold=True, anchor="m", role="card", group=g)
        role = "placeholder" if "[[" in a else "card"
        text(s, x + 0.35, y + 1.08, cwid - 0.7, 1.24, a, size=15, role=role, group=g)
    if part == 1:
        n = """Use these answers as written; they follow CURRENT_OFFER.md. On data, stick to the controls listed and
        don't claim certifications we haven't confirmed. On WhatsApp numbers, a number already used in the WhatsApp
        Business app may need extra steps, so check it together during setup. On payments, be clear that checkout
        through FluxMuse is being switched on and hasn't been tested with real money yet. There are no trials, and
        cancellation terms are still to be confirmed, so promise a written answer rather than improvising."""
    else:
        n = """The lead guarantee always comes with its conditions: three qualified leads in 30 days of go-live; if
        fewer, and the business shared its link and posted at least weekly, we extend support at no extra charge
        until three arrive. It is never cash back. Setup is by hand, but Meta approvals and catalogue size can
        stretch it, so set expectations honestly. Store sync is being switched on, so don't promise it. Outside South
        Africa, share the waitlist link, never prices (CURRENT_OFFER.md §2 and §3)."""
    notes(s, n, v)
    return s


# ================================================================ DECKS
def deck_defs():
    B = lambda f, **kw: (f, kw)
    return {
        "FluxMuse_Brand_Pitch_Deck.pptx": ("master", [
            B(s_title), B(s_reality), B(s_meet), B(s_how), B(s_sell), B(s_channels), B(s_paid),
            B(s_segments), B(s_seg_solo), B(s_seg_sme), B(s_seg_agency), B(s_partner_model),
            B(s_journey), B(s_first_group), B(s_case), B(s_pricing), B(s_pricing_table), B(s_founding), B(s_trust),
            B(s_roadmap), B(s_next),
            B(a_divider, items=[("A1", "Payment status by country"), ("A2", "Partner wholesale pricing"),
                                ("A3", "Frequently asked questions")]),
            B(a_rails, label="A1"), B(p_wholesale, label="A2"), B(a_faq, label="A3", part=1),
            B(a_faq, label="A3", part=2),
        ]),
        "FluxMuse_Pitch_Solo_Entrepreneurs.pptx": ("solo", [
            B(s_title), B(s_reality), B(s_meet), B(s_how), B(s_sell), B(s_seg_solo), B(s_journey),
            B(s_first_group), B(s_plans), B(s_founding), B(s_trust), B(s_next),
            B(a_faq, label="A1", part=1), B(a_faq, label="A1", part=2),
        ]),
        "FluxMuse_Pitch_SMEs.pptx": ("sme", [
            B(s_title), B(s_reality), B(s_meet), B(s_how), B(s_sell), B(s_channels),
            B(s_sme_integrations), B(s_paid), B(s_seg_sme), B(s_journey), B(s_first_group), B(s_plans),
            B(s_pricing_table), B(s_founding), B(s_trust), B(s_roadmap), B(s_next),
            B(a_divider, items=[("A1", "Payment status by country"), ("A2", "Frequently asked questions")]),
            B(a_rails, label="A1"), B(a_faq, label="A2", part=1), B(a_faq, label="A2", part=2),
        ]),
        "FluxMuse_Partner_Programme_Deck.pptx": ("partner", [
            B(s_title), B(p_squeeze), B(s_meet), B(s_how), B(s_sell), B(s_channels), B(s_seg_agency),
            B(s_partner_model), B(p_what_you_get), B(p_wholesale), B(p_onboarding), B(p_comarketing), B(s_paid),
            B(s_first_group), B(s_trust), B(s_roadmap), B(s_next),
            B(a_divider, items=[("A1", "Payment status by country"), ("A2", "Frequently asked questions")]),
            B(a_rails, label="A1"), B(a_faq, label="A2", part=1), B(a_faq, label="A2", part=2),
        ]),
    }


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
    marker = V3_MARKER.exists()
    manifest = {"built": date.today().isoformat(), "assets_revision_v3_marker": marker, "decks": {}}
    for fname, (v, slides) in deck_defs().items():
        _CUR_DECK[0] = fname
        prs = Presentation()
        prs.slide_width, prs.slide_height = Inches(SW), Inches(SH)
        set_theme_fonts(prs)
        prs.core_properties.title = "FluxMuse pitch deck" if v != "partner" else "FluxMuse Partner Programme"
        prs.core_properties.author = "Fluxmuse (Pty) Ltd"
        prs.core_properties.subject = "AI marketing & WhatsApp selling"
        for i, (fn, kw) in enumerate(slides):
            s = fn(prs, v, **kw)
            if i > 0:
                chrome(s, i + 1, getattr(s, "_fm_dark", False))
        prs.save(OUT / fname)
        manifest["decks"][fname] = {"variant": v, "slides": len(prs.slides),
                                    "images": sorted(USED_IMAGES.get(fname, []))}
        print(f"built {fname}: {len(prs.slides)} slides")
    (HERE / "build_manifest.json").write_text(json.dumps(manifest, indent=2))
    print(f"assets/.revision-v3-done present: {marker}")


if __name__ == "__main__":
    build()
