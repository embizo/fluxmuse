"""Business-plan document class and shared data.

House style is inherited from the proposal kit (fmdoc.FMDoc): A4, Poppins/Inter with Arial fallback,
Flux Orange table headers with Ink text, [[PLACEHOLDER]] bold on yellow.

Every number used by the sections comes from M (model_summary.json), D (derived_tables.json, built by
derive_model_tables.py from the model's Python mirror) or the facts file. Nothing is typed by hand.
"""
import json
from pathlib import Path

from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT
from docx.shared import Cm, Pt

from fmdoc import (ASSETS, BODY_FONT, CONTENT_W, DEEP, GREY, GTM, HEAD_FONT, INK, MIST, ORANGE,
                   SLATE, TINT, FMDoc, img_stream)

HERE = Path(__file__).resolve().parent
M = json.loads((GTM / "06_Financial_Model" / "model_summary.json").read_text())
D = json.loads((HERE / "derived_tables.json").read_text())

BASE = M["scenarios"]["Base"]
ANN = M["annual"]
FY = ["FY1", "FY2", "FY3", "FY4", "FY5"]
PERIODS = [a["period"] for a in ANN]
DOC_DATE = "September 2026"
VERSION = "v1.0"


# ---------------------------------------------------------------- number formatting
def rm(x, nd=1):
    """R million, from rands."""
    return f"R{x / 1e6:,.{nd}f}m"


def rand(x):
    return f"R{round(x):,}"


def rk(x):
    return f"R{round(x / 1000):,}k"


def usd(x):
    return f"US${x:,.0f}"


def pct(x, nd=0):
    return f"{x:.{nd}f}%"


def fy_row(label, values, fmt=rm):
    return [label] + [fmt(v) for v in values]


def ann(key):
    return [a[key] for a in ANN]


def ann_sub(key, sub):
    return [a[key][sub] for a in ANN]


class BPDoc(FMDoc):
    """The business plan: same house style, its own header/footer and a 1-2 level TOC."""

    toc_levels = "1-2"

    def __init__(self):
        self.doc_label = f"Business Plan · {DOC_DATE} · Confidential"
        super().__init__(sample=False, client_ph="[[CLIENT NAME]]")

    def _footer_para(self, footer):
        p = footer.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        from fmdoc import PPR_ORDER, border_el, put
        put(p._p.get_or_add_pPr(), border_el("w:pBdr", ["top"], sz=4, color="D9DDE2", space=6), PPR_ORDER)
        self.rich(p, "Fluxmuse Pty Ltd · fluxmuse.ai · Business plan · Confidential · Page ", size=8, color=GREY)
        self._field(p, "PAGE")
        self.rich(p, " of ", size=8, color=GREY)
        self._field(p, "NUMPAGES")

    def _header_para(self, header):
        p = header.paragraphs[0]
        pf = p.paragraph_format
        pf.space_after = Pt(0)
        pf.tab_stops.add_tab_stop(Cm(CONTENT_W), WD_TAB_ALIGNMENT.RIGHT)
        from fmdoc import PPR_ORDER, border_el, put
        put(p._p.get_or_add_pPr(), border_el("w:pBdr", ["bottom"], sz=12, color=ORANGE, space=4), PPR_ORDER)
        r = p.add_run()
        r.add_picture(img_stream(ASSETS / "brand/fluxmuse-icon-512.png", 256), height=Cm(0.8))
        self._docpr(r, "FluxMuse icon")
        self._run(p, "  FLUX", font=HEAD_FONT, size=12, color=DEEP, bold=True)
        self._run(p, "MUSE", font=HEAD_FONT, size=12, color=SLATE, bold=True)
        self._run(p, "\tBusiness plan " + VERSION + " · Confidential", size=8, color=GREY)

    # ---- cover
    def cover_page(self):
        self.spacer(6)
        p = self.doc.add_paragraph()
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run()
        r.add_picture(img_stream(ASSETS / "brand/fluxmuse-icon-512.png", 512), height=Cm(2.6))
        self._docpr(r, "FluxMuse Muse icon: a multicolour low-poly head over a node network")
        p = self.doc.add_paragraph()
        p.paragraph_format.space_after = Pt(0)
        self._run(p, "FLUX", font=HEAD_FONT, size=30, color=DEEP, bold=True)
        self._run(p, "MUSE", font=HEAD_FONT, size=30, color=SLATE, bold=True)
        self.para("AI Marketing & WhatsApp Commerce for Africa", size=11, color=GREY, after=18)
        self.eyebrow("Business plan")
        p = self.doc.add_paragraph(style="Title")
        p.paragraph_format.space_after = Pt(4)
        self.rich(p, "An AI marketing team and a checkout, inside the chat app Africa already uses")
        self.para(f"Seed raise of R25 million · {DOC_DATE}", size=13, color=SLATE, after=12)
        self.rule(ORANGE, 24, after=10)
        self.figure("screenshots/composites/hero-laptop-phone_white.png",
                    "FluxMuse on the web app and in WhatsApp: an AI marketing team that plans, creates and "
                    "publishes, and a catalog, cart and checkout inside the chat.",
                    "Laptop showing the FluxMuse web app beside a phone showing a WhatsApp order confirmation "
                    "with a Yoco card payment", width_cm=16.0)
        self.kv_table([
            ("Company", "Fluxmuse Pty Ltd (South Africa) · registration number [[COMPANY REGISTRATION NUMBER]]"),
            ("Document", f"Business Plan · {DOC_DATE} · Confidential · version {VERSION}"),
            ("Prepared by", "[[FOUNDER NAME, TITLE]], Fluxmuse Pty Ltd\n[[EMAIL]] · [[PHONE / WHATSAPP]]"),
            ("Prepared for", "[[INVESTOR / FUNDER NAME]]"),
            ("Financial model", "FluxMuse Financial Model v2, model date 11 September 2026 (Base case)"),
        ], caption="Layout: document details")
        self.para("Confidential. This document contains commercially sensitive information and is provided for "
                  "evaluation only. Figures in South African rand (ZAR) unless stated. US dollar equivalents at "
                  "R18.50 = US$1.", size=8.5, color=GREY, before=8)
        self.page_break()

    def figure(self, rel_path, caption, alt, width_cm=13.6):
        """Body figures sit at 13.6cm so a figure and its caption pack onto a page with text."""
        return super().figure(rel_path, caption, alt, width_cm=width_cm)

    # ---- helpers used across sections
    def note(self, text):
        self.para(text, size=9, color=GREY, italic=True, after=8)

    def source(self, text="FluxMuse Financial Model v2 (Base case), 11 September 2026."):
        self.para("Source: " + text, size=8.5, color=GREY, after=10)

    def fy_table(self, caption, rows, first_header="R million unless stated", size=9.5,
                 total_rows=(), widths=None):
        hdr = [first_header] + [f"{f}\n{p.replace(' - ', '–')}" for f, p in zip(FY, PERIODS)]
        w = widths or [4.6] + [2.48] * 5
        self.table(hdr, rows, w, caption, size=size, aligns=[None] + ["right"] * 5,
                   total_rows=total_rows)
