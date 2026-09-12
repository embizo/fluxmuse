"""Approximate A4 preview of the proposal .docx files (no LibreOffice/Word needed).

1. python preview_proposals.py html <outdir>   -> reads each .docx XML and writes an A4 print-CSS HTML file
2. node preview_proposals.mjs <outdir>         -> headless Chrome prints each HTML to PDF
3. python preview_proposals.py png <outdir>    -> PyMuPDF renders PDF pages to PNG and prints page counts

Fidelity is approximate (Chrome layout, not Word's), so page counts are estimates.
"""
import base64
import html
import sys
from pathlib import Path

from docx import Document
from docx.oxml.ns import qn

HERE = Path(__file__).resolve().parent
SRC = HERE.parent.parent / "03_Proposal_Templates"
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
WP = "{http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing}"
R = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Poppins:wght@600;700&display=swap');
@page { size: A4; margin: 2.4cm 2cm 2.2cm 2cm; }
body { font-family: Inter, Arial, sans-serif; font-size: 10.5pt; line-height: 1.15; color: #20242B; margin: 0; }
p { margin: 0 0 6pt 0; }
.h1 { font-family: Poppins, Arial; font-weight: 700; font-size: 18pt; margin: 20pt 0 8pt; padding-bottom: 4pt; border-bottom: 1.5pt solid #FF6A00; break-after: avoid; }
.h2 { font-family: Poppins, Arial; font-weight: 700; font-size: 13pt; margin: 14pt 0 4pt; break-after: avoid; }
.h3 { font-family: Poppins, Arial; font-weight: 700; font-size: 11pt; color: #C24E00; margin: 10pt 0 3pt; break-after: avoid; }
.title { font-family: Poppins, Arial; font-weight: 700; font-size: 30pt; margin: 0 0 4pt; line-height: 1.1; }
.caption { font-size: 8.5pt; color: #5B6570; margin: 3pt 0 10pt; }
.li { margin: 0 0 3pt 0.64cm; text-indent: -0.64cm; line-height: 1.1; }
table { border-collapse: collapse; table-layout: fixed; margin: 0 auto; }
td { vertical-align: middle; padding: 2.5pt 5pt; }
td p { margin: 0 0 1pt 0; line-height: 1.05; }
tr { break-inside: avoid; }
.pb { break-after: page; }
img { display: block; margin: 0 auto; }
"""


def px_cm(emu):
    return emu / 360000.0


class Conv:
    def __init__(self, doc):
        self.doc = doc
        self.part = doc.part
        self.num_counts = {}

    def run_html(self, r):
        out = []
        rpr = r.find(W + "rPr")
        style = []
        if rpr is not None:
            if rpr.find(W + "b") is not None and rpr.find(W + "b").get(W + "val") not in ("0", "false"):
                style.append("font-weight:700")
            if rpr.find(W + "i") is not None:
                style.append("font-style:italic")
            c = rpr.find(W + "color")
            if c is not None and c.get(W + "val") not in (None, "auto"):
                style.append(f"color:#{c.get(W + 'val')}")
            sz = rpr.find(W + "sz")
            if sz is not None:
                style.append(f"font-size:{int(sz.get(W + 'val')) / 2}pt")
            s = rpr.find(W + "shd")
            if s is not None:
                style.append(f"background:#{s.get(W + 'fill')}")
            f = rpr.find(W + "rFonts")
            if f is not None and f.get(W + "ascii") == "Poppins":
                style.append("font-family:Poppins,Arial")
        for ch in r:
            if ch.tag == W + "t":
                out.append(html.escape(ch.text or ""))
            elif ch.tag == W + "tab":
                out.append("&emsp;&emsp;")
            elif ch.tag == W + "br" and ch.get(W + "type") == "page":
                out.append('</span><div class="pb"></div><span>')
            elif ch.tag == W + "drawing":
                ext = ch.find(".//" + WP + "extent")
                blip = ch.find(".//" + A + "blip")
                rid = blip.get(R + "embed")
                part = self.cur_part.related_parts[rid]
                data = base64.b64encode(part.blob).decode()
                wcm = px_cm(int(ext.get("cx")))
                hcm = px_cm(int(ext.get("cy")))
                out.append(f'<img src="data:image/png;base64,{data}" style="width:{wcm:.2f}cm;height:{hcm:.2f}cm;display:inline-block">')
        return f'<span style="{";".join(style)}">{"".join(out)}</span>'

    def inline(self, p):
        parts = []
        for ch in p:
            if ch.tag == W + "r":
                if ch.find(W + "instrText") is not None or ch.find(W + "fldChar") is not None:
                    continue
                parts.append(self.run_html(ch))
            elif ch.tag in (W + "fldSimple", W + "hyperlink"):
                parts += [self.run_html(r) for r in ch.findall(W + "r")]
            elif ch.tag == W + "sdt":
                for r in ch.iter(W + "r"):
                    parts.append(self.run_html(r))
        return "".join(parts)

    def para(self, p):
        ppr = p.find(W + "pPr")
        style = "Normal"
        css = []
        cls = ""
        if ppr is not None:
            ps = ppr.find(W + "pStyle")
            if ps is not None:
                style = ps.get(W + "val")
            jc = ppr.find(W + "jc")
            if jc is not None and jc.get(W + "val") in ("center", "right"):
                css.append(f"text-align:{jc.get(W + 'val')}")
            if ppr.find(W + "pageBreakBefore") is not None:
                css.append("break-before:page")
            b = ppr.find(W + "pBdr")
            if b is not None:
                for side in ("top", "bottom"):
                    e = b.find(W + side)
                    if e is not None:
                        css.append(f"border-{side}:{int(e.get(W + 'sz')) / 8}pt solid #{e.get(W + 'color')};padding-{side}:3pt")
            sp = ppr.find(W + "spacing")
            if sp is not None and sp.get(W + "after") is not None:
                css.append(f"margin-bottom:{int(sp.get(W + 'after')) / 20}pt")
            if sp is not None and sp.get(W + "before") is not None:
                css.append(f"margin-top:{int(sp.get(W + 'before')) / 20}pt")
            ind = ppr.find(W + "ind")
            if ind is not None and ind.get(W + "left"):
                css.append(f"padding-left:{int(ind.get(W + 'left')) / 567:.2f}cm;text-indent:{int(ind.get(W + 'hanging', 0) or 0) and -int(ind.get(W + 'hanging')) / 567 or (int(ind.get(W + 'firstLine', 0) or 0) / 567):.2f}cm")
        prefix = ""
        m = {"Heading1": "h1", "Heading2": "h2", "Heading3": "h3", "Title": "title", "Caption": "caption"}
        if style in m:
            cls = m[style]
        elif style in ("ListBullet", "ListBullet2"):
            cls, prefix = "li", "•&emsp;"
        elif style == "ListNumber":
            numid = ppr.find(W + "numPr/" + W + "numId").get(W + "val") if ppr.find(W + "numPr") is not None else "s"
            self.num_counts[numid] = self.num_counts.get(numid, 0) + 1
            cls, prefix = "li", f"{self.num_counts[numid]}.&emsp;"
        body = self.inline(p) or "&nbsp;"
        return f'<p class="{cls}" style="{";".join(css)}">{prefix}{body}</p>'

    def table(self, tbl):
        grid = [int(g.get(W + "w")) / 567 for g in tbl.findall(W + "tblGrid/" + W + "gridCol")]
        borders = tbl.find(W + "tblPr/" + W + "tblBorders")
        has_b = borders is not None and len(borders) > 0
        rows = []
        for tr in tbl.findall(W + "tr"):
            cells = []
            for tc in tr.findall(W + "tc"):
                css = []
                tcpr = tc.find(W + "tcPr")
                if tcpr is not None:
                    s = tcpr.find(W + "shd")
                    if s is not None:
                        css.append(f"background:#{s.get(W + 'fill')}")
                    tb = tcpr.find(W + "tcBorders")
                    if tb is not None:
                        for side in ("top", "left", "bottom", "right"):
                            e = tb.find(W + side)
                            if e is not None and e.get(W + "val") == "single":
                                css.append(f"border-{side}:{int(e.get(W + 'sz')) / 8}pt solid #{e.get(W + 'color')}")
                    mar = tcpr.find(W + "tcMar")
                    if mar is not None:
                        css.append("padding:7pt 10pt 6pt 11pt")
                if has_b:
                    css.insert(0, "border:0.5pt solid #D9DDE2")
                trh = tr.find(W + "trPr/" + W + "trHeight")
                if trh is not None:
                    css.append(f"height:{int(trh.get(W + 'val')) / 567:.2f}cm;vertical-align:bottom")
                inner = "".join(self.block(ch) for ch in tc if ch.tag in (W + "p", W + "tbl"))
                cells.append(f'<td style="{";".join(css)}">{inner}</td>')
            rows.append("<tr>" + "".join(cells) + "</tr>")
        cols = "".join(f'<col style="width:{w:.2f}cm">' for w in grid)
        return f'<table style="width:{sum(grid):.2f}cm"><colgroup>{cols}</colgroup>{"".join(rows)}</table>'

    def block(self, el):
        if el.tag == W + "p":
            return self.para(el)
        if el.tag == W + "tbl":
            return self.table(el)
        return ""

    def convert(self, title):
        self.cur_part = self.part
        body = "".join(self.block(ch) for ch in self.doc.element.body)
        return f"<!doctype html><html><head><meta charset='utf-8'><title>{html.escape(title)}</title><style>{CSS}</style></head><body>{body}</body></html>"


def to_html(outdir):
    outdir.mkdir(parents=True, exist_ok=True)
    for p in sorted(SRC.glob("*.docx")):
        doc = Document(p)
        (outdir / (p.stem + ".html")).write_text(Conv(doc).convert(p.stem))
        print("html", p.stem)


def to_png(outdir, scale=0.9):
    import fitz
    for pdf in sorted(outdir.glob("*.pdf")):
        d = fitz.open(pdf)
        print(f"{pdf.stem}: {d.page_count} pages")
        for i, page in enumerate(d):
            page.get_pixmap(matrix=fitz.Matrix(scale, scale)).save(outdir / f"{pdf.stem}-p{i + 1:02d}.png")


if __name__ == "__main__":
    mode, outdir = sys.argv[1], Path(sys.argv[2])
    to_html(outdir) if mode == "html" else to_png(outdir)
