#!/usr/bin/env python3
"""
build_handbook_pdf.py — regenerates handbook.pdf from handbook.html

Seasons Schoolhouse LLC. Run from the repo root:

    python3 build_handbook_pdf.py

Requires: reportlab, fonttools, brotli, beautifulsoup4
Fonts are pulled from npm (@fontsource) and converted woff2 -> ttf.
The `font.flavor = None` step is REQUIRED; omitting it silently writes
invalid ttf files that reportlab will reject.

Design constants below were derived from the original deployed PDF so
regenerated output matches the established look.
"""

import os
import re
import subprocess
import sys

from reportlab.lib.colors import Color
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate, Frame, KeepTogether, NextPageTemplate, PageBreak,
    PageTemplate, Paragraph, Spacer, Table, TableStyle,
)

# ---------------------------------------------------------------- constants

PAGE_W, PAGE_H = letter                      # 612 x 792
MARGIN_L = 78
MARGIN_R = 78
TEXT_W = PAGE_W - MARGIN_L - MARGIN_R        # 456
FOOTER_Y = PAGE_H - 761.5 - 6                # footer baseline

INK   = Color(0.243137, 0.180392, 0.133333)  # #3E2E22
MOSS  = Color(0.290196, 0.419608, 0.278431)  # #4A6B47
TAN   = Color(0.658824, 0.525490, 0.349020)  # #A88659
CREAM = Color(0.980392, 0.968627, 0.949020)  # #FAF7F2
SAGE  = Color(0.478431, 0.607843, 0.470588)  # #7A9B78

FONT_DIR = "fonts"
COVER_YEAR = "2 0 2 6 &nbsp;&nbsp; · &nbsp;&nbsp; 2 0 2 7"
# Pull quotes are a PDF-only design element, keyed by the h3 they precede.
PULL_QUOTES = {
    "Student Tuition":
        "\u201cWhat you see here is what you\u2019ll pay. Together, tuition and the "
        "registration fee cover the full cost of participation.\u201d",
}

FOOTER_TXT = "Seasons Schoolhouse LLC  ·  Palm Coast, FL  ·  Page {page} of {total}"


# ------------------------------------------------------------------- fonts

FONT_SPECS = [
    ("jost", "jost-latin-400-normal.woff2", "Jost"),
    ("jost", "jost-latin-400-italic.woff2", "Jost-Italic"),
    ("jost", "jost-latin-500-normal.woff2", "Jost-Medium"),
    ("jost", "jost-latin-600-normal.woff2", "Jost-Bold"),
    ("cormorant-garamond", "cormorant-garamond-latin-300-normal.woff2", "Cormorant"),
    ("cormorant-garamond", "cormorant-garamond-latin-300-italic.woff2", "Cormorant-Italic"),
    ("cormorant-garamond", "cormorant-garamond-latin-600-normal.woff2", "Cormorant-Bold"),
    ("cormorant-garamond", "cormorant-garamond-latin-600-italic.woff2", "Cormorant-BoldItalic"),
]


def ensure_fonts():
    """Download via npm and convert woff2 -> ttf, then register with reportlab."""
    os.makedirs(FONT_DIR, exist_ok=True)
    need_dl = not all(
        os.path.exists(os.path.join(FONT_DIR, f"{name}.ttf"))
        for _, _, name in FONT_SPECS
    )
    if need_dl:
        if not os.path.isdir("node_modules/@fontsource/jost"):
            subprocess.run(
                ["npm", "install", "--silent",
                 "@fontsource/jost", "@fontsource/cormorant-garamond"],
                check=True,
            )
        from fontTools.ttLib import TTFont as FTFont
        for pkg, src_name, out in FONT_SPECS:
            out_path = os.path.join(FONT_DIR, f"{out}.ttf")
            if os.path.exists(out_path):
                continue
            src = f"node_modules/@fontsource/{pkg}/files/{src_name}"
            f = FTFont(src)
            f.flavor = None            # REQUIRED - see module docstring
            f.save(out_path)

    for _, _, name in FONT_SPECS:
        pdfmetrics.registerFont(TTFont(name, os.path.join(FONT_DIR, f"{name}.ttf")))

    pdfmetrics.registerFontFamily(
        "Jost", normal="Jost", bold="Jost-Bold",
        italic="Jost-Italic", boldItalic="Jost-Italic")
    pdfmetrics.registerFontFamily(
        "Cormorant", normal="Cormorant", bold="Cormorant-Bold",
        italic="Cormorant-Italic", boldItalic="Cormorant-BoldItalic")


# ------------------------------------------------------------------ styles

def build_styles():
    s = {}
    s["body"] = ParagraphStyle(
        "body", fontName="Jost", fontSize=10.5, leading=16,
        textColor=INK, spaceAfter=9, alignment=TA_LEFT)
    s["h2"] = ParagraphStyle(
        "h2", fontName="Cormorant-Bold", fontSize=24, leading=28,
        textColor=MOSS, spaceBefore=6, spaceAfter=15)
    s["h3"] = ParagraphStyle(
        "h3", fontName="Cormorant-Bold", fontSize=15, leading=18,
        textColor=MOSS, spaceBefore=14, spaceAfter=8)
    s["bullet"] = ParagraphStyle(
        "bullet", fontName="Jost", fontSize=10.5, leading=16,
        textColor=INK, leftIndent=30, bulletIndent=0,
        spaceAfter=3, bulletFontName="Jost", bulletFontSize=11)
    s["quote"] = ParagraphStyle(
        "quote", fontName="Cormorant-Italic", fontSize=13.5, leading=20,
        textColor=MOSS, leftIndent=18, rightIndent=18,
        spaceBefore=14, spaceAfter=14)
    s["cover_title"] = ParagraphStyle(
        "cover_title", fontName="Cormorant", fontSize=64, leading=70,
        textColor=CREAM, alignment=TA_CENTER)
    s["cover_sub"] = ParagraphStyle(
        "cover_sub", fontName="Cormorant-Italic", fontSize=14, leading=22,
        textColor=CREAM, alignment=TA_CENTER)
    s["cover_eyebrow"] = ParagraphStyle(
        "cover_eyebrow", fontName="Jost-Medium", fontSize=10, leading=14,
        textColor=CREAM, alignment=TA_CENTER)
    s["cover_year"] = ParagraphStyle(
        "cover_year", fontName="Cormorant", fontSize=18, leading=24,
        textColor=CREAM, alignment=TA_CENTER)
    s["cover_legal"] = ParagraphStyle(
        "cover_legal", fontName="Cormorant-Italic", fontSize=11, leading=16,
        textColor=CREAM, alignment=TA_CENTER)
    s["cover_city"] = ParagraphStyle(
        "cover_city", fontName="Jost", fontSize=10, leading=14,
        textColor=CREAM, alignment=TA_CENTER)
    s["toc_title"] = ParagraphStyle(
        "toc_title", fontName="Cormorant", fontSize=38, leading=44,
        textColor=MOSS, spaceAfter=6)
    s["toc_sub"] = ParagraphStyle(
        "toc_sub", fontName="Cormorant-Italic", fontSize=13, leading=18,
        textColor=TAN, spaceAfter=40)
    s["toc_row"] = ParagraphStyle(
        "toc_row", fontName="Jost", fontSize=11.5, leading=23, textColor=TAN)
    s["closing"] = ParagraphStyle(
        "closing", fontName="Cormorant-Italic", fontSize=16, leading=24,
        textColor=MOSS, alignment=TA_CENTER, spaceAfter=6)
    s["closing_sig"] = ParagraphStyle(
        "closing_sig", fontName="Jost", fontSize=11, leading=16,
        textColor=TAN, alignment=TA_CENTER, spaceBefore=18)
    s["stamp"] = ParagraphStyle(
        "stamp", fontName="Jost-Italic", fontSize=9, leading=13,
        textColor=TAN, spaceBefore=14)
    return s


# ------------------------------------------------------------ html parsing

def clean_inline(node):
    """Convert an element's inline children into reportlab markup."""
    from bs4 import NavigableString, Tag
    out = []
    for child in node.children:
        if isinstance(child, NavigableString):
            out.append(str(child))
        elif isinstance(child, Tag):
            inner = clean_inline(child)
            if child.name in ("strong", "b"):
                out.append(f"<b>{inner}</b>")
            elif child.name in ("em", "i"):
                out.append(f"<i>{inner}</i>")
            elif child.name == "br":
                out.append("<br/>")
            elif child.name == "a":
                out.append(inner)
            else:
                out.append(inner)
    txt = "".join(out)
    txt = re.sub(r"\s+", " ", txt).strip()
    return txt


def parse_handbook(path="handbook.html"):
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(open(path, encoding="utf-8").read(), "html.parser")
    sections = []
    for div in soup.select("div.handbook-section"):
        h2 = div.find("h2")
        if not h2:
            continue
        title = clean_inline(h2)
        blocks = []
        for el in div.find_all(["h3", "p", "ul", "ol", "table"], recursive=False):
            if el.name == "h3":
                blocks.append(("h3", clean_inline(el)))
            elif el.name == "p":
                t = clean_inline(el)
                if t:
                    blocks.append(("p", t))
            elif el.name in ("ul", "ol"):
                items = [clean_inline(li) for li in el.find_all("li", recursive=False)]
                blocks.append(("ul", items))
            elif el.name == "table":
                rows = []
                for tr in el.find_all("tr"):
                    cells = [clean_inline(td) for td in tr.find_all(["th", "td"])]
                    if cells:
                        rows.append(cells)
                blocks.append(("table", rows))
        sections.append({"title": title, "blocks": blocks})
    return sections


# ------------------------------------------------------------- doc template

class HandbookDoc(BaseDocTemplate):
    def __init__(self, filename, **kw):
        BaseDocTemplate.__init__(self, filename, pagesize=letter,
                                 leftMargin=MARGIN_L, rightMargin=MARGIN_R,
                                 topMargin=70, bottomMargin=58, **kw)
        self.total_pages = 0

        cover_frame = Frame(0, 0, PAGE_W, PAGE_H, id="cover",
                            leftPadding=0, rightPadding=0,
                            topPadding=0, bottomPadding=0)
        content_frame = Frame(MARGIN_L, 58, TEXT_W, PAGE_H - 70 - 58,
                              id="content", leftPadding=0, rightPadding=0,
                              topPadding=0, bottomPadding=0)
        self.addPageTemplates([
            PageTemplate(id="Cover", frames=[cover_frame], onPage=self.draw_cover_bg),
            PageTemplate(id="Content", frames=[content_frame], onPage=self.draw_footer),
        ])

    def draw_cover_bg(self, canvas, doc):
        canvas.saveState()
        canvas.setFillColor(SAGE)
        canvas.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
        canvas.setStrokeColor(CREAM)
        canvas.setLineWidth(0.8)
        canvas.rect(39.6, 39.6, PAGE_W - 79.2, PAGE_H - 79.2, stroke=1, fill=0)
        # rule · · · rule divider above the year
        y = PAGE_H - 421.2
        canvas.setLineWidth(0.6)
        canvas.line(228, y, 288, y)
        canvas.line(324, y, 384, y)
        canvas.setFillColor(CREAM)
        for cx in (294, 306, 318):
            canvas.circle(cx, y, 1.2, stroke=0, fill=1)
        canvas.restoreState()

    def draw_footer(self, canvas, doc):
        canvas.saveState()
        # hairline rule above the footer
        canvas.setStrokeColor(Color(0.658824, 0.768627, 0.647059))
        canvas.setLineWidth(0.5)
        canvas.line(72, PAGE_H - 752.8, 540, PAGE_H - 752.8)
        canvas.setFont("Jost", 8.5)
        canvas.setFillColor(TAN)
        txt = FOOTER_TXT.format(page=doc.page, total=self.total_pages or doc.page)
        canvas.drawCentredString(PAGE_W / 2.0, FOOTER_Y, txt)
        canvas.restoreState()


# ------------------------------------------------------------------- story

def build_story(sections, s):
    story = []

    # ---- cover -------------------------------------------------------
    story.append(Spacer(1, 175))
    story.append(Paragraph("R E S O U R C E S", s["cover_eyebrow"]))
    story.append(Spacer(1, 30))
    story.append(Paragraph('Parent <i>Handbook</i>', s["cover_title"]))
    story.append(Spacer(1, 14))
    story.append(Paragraph(
        "Everything you need to know about how Seasons Schoolhouse<br/>"
        "operates, what we expect, and how we care for one another.",
        s["cover_sub"]))
    story.append(Spacer(1, 88))
    story.append(Paragraph(COVER_YEAR, s["cover_year"]))
    story.append(Spacer(1, 42))
    story.append(Paragraph(
        "Seasons Schoolhouse LLC — a Florida limited liability company",
        s["cover_legal"]))
    story.append(Paragraph("Palm Coast, Florida", s["cover_city"]))

    story.append(NextPageTemplate("Content"))   # must precede the cover break
    story.append(PageBreak())

    # ---- contents ----------------------------------------------------
    story.append(Paragraph("Contents", s["toc_title"]))
    story.append(Paragraph("A guide to our program, policies, and community",
                           s["toc_sub"]))
    for i, sec in enumerate(sections, start=1):
        label = re.sub(r"^\d+\.\s*", "", sec["title"])
        story.append(Paragraph(f"{i:02d} &nbsp;&nbsp; {label}", s["toc_row"]))
    story.append(PageBreak())

    # ---- sections ----------------------------------------------------
    for i, sec in enumerate(sections, start=1):
        head = [
            Paragraph(sec["title"], s["h2"]),
        ]
        first = sec["blocks"][0] if sec["blocks"] else None
        if first and first[0] == "p":
            head.append(Paragraph(first[1], s["body"]))
            blocks = sec["blocks"][1:]
        else:
            blocks = sec["blocks"]
        story.append(KeepTogether(head))

        for kind, payload in blocks:
            if kind == "h3" and payload in PULL_QUOTES:
                story.append(Paragraph(PULL_QUOTES[payload], s["quote"]))
            if kind == "h3":
                story.append(KeepTogether([Paragraph(payload, s["h3"])]))
            elif kind == "p":
                st = s["stamp"] if payload.startswith("Last updated:") else s["body"]
                story.append(Paragraph(payload, st))
            elif kind == "ul":
                for it in payload:
                    story.append(Paragraph(it, s["bullet"], bulletText="\u2022"))
                story.append(Spacer(1, 4))
            elif kind == "table":
                story.append(Spacer(1, 6))
                story.append(make_table(payload))
                story.append(Spacer(1, 10))

        if i < len(sections):
            story.append(Spacer(1, 22))

    # ---- closing -----------------------------------------------------
    story.append(Spacer(1, 40))
    story.append(Paragraph(
        "Thank you for trusting us with a part of your family’s year.",
        s["closing"]))
    story.append(Spacer(1, 22))
    story.append(Paragraph(
        "May this season be one of joy, growth, and deeper roots<br/>"
        "for your children and for our community.", s["closing"]))
    story.append(Paragraph("— Danyelle &amp; the Seasons Schoolhouse community",
                           s["closing_sig"]))
    return story


def make_table(rows):
    """Fee table. Right-edge column positions 239.4 / 315.0 / 390.6 pt
    were derived from font metrics on the original build — preserved here."""
    body_style = ParagraphStyle(
        "tb", fontName="Jost", fontSize=10, leading=14, textColor=INK)
    head_style = ParagraphStyle(
        "th", fontName="Jost-Medium", fontSize=10, leading=14, textColor=CREAM)
    head_r = ParagraphStyle("thr", parent=head_style, alignment=2)
    body_r = ParagraphStyle("tbr", parent=body_style, alignment=2)
    total_r = ParagraphStyle("tbt", parent=body_r,
                             fontName="Jost-Medium", textColor=MOSS)

    data = []
    for ri, row in enumerate(rows):
        if ri == 0:
            data.append([Paragraph(row[0], head_style)] +
                        [Paragraph(c, head_r) for c in row[1:]])
        else:
            cells = [Paragraph(row[0], body_style)]
            for ci, c in enumerate(row[1:], start=1):
                cells.append(Paragraph(c, total_r if ci == len(row) - 1 else body_r))
            data.append(cells)

    ncols = len(rows[0])
    first_w = TEXT_W - 75.6 * (ncols - 1)
    widths = [first_w] + [75.6] * (ncols - 1)

    t = Table(data, colWidths=widths, hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), MOSS),
        ("TOPPADDING", (0, 0), (-1, 0), 7),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 7),
        ("TOPPADDING", (0, 1), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 1), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 9),
        ("RIGHTPADDING", (0, 0), (-1, -1), 9),
        ("LINEBELOW", (0, 1), (-1, -2), 0.5, Color(0.90, 0.88, 0.84)),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    return t


# -------------------------------------------------------------------- main

def main():
    ensure_fonts()
    styles = build_styles()
    sections = parse_handbook("handbook.html")
    print(f"parsed {len(sections)} sections")

    # Two-pass build so "Page X of N" is accurate.
    doc = HandbookDoc("handbook.pdf")
    doc.build(build_story(sections, styles))
    total = doc.page

    doc = HandbookDoc("handbook.pdf")
    doc.total_pages = total
    doc.build(build_story(sections, styles))
    print(f"wrote handbook.pdf — {total} pages")


if __name__ == "__main__":
    main()
