"""Build the portfolio PDF from the all-in-one Markdown guide.

The renderer intentionally supports the small, controlled Markdown subset used by
docs/15-all-in-one-home-lab-build-guide.md. Keeping Markdown as the source of
truth makes the living guide easy to update as the lab grows.
"""

from __future__ import annotations

import html
import re
import sys
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.platypus import (
    BaseDocTemplate,
    Flowable,
    Frame,
    HRFlowable,
    KeepTogether,
    PageBreak,
    PageTemplate,
    Paragraph,
    Preformatted,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs" / "15-all-in-one-home-lab-build-guide.md"
OUTPUT = ROOT / "output" / "pdf" / "Cybersecurity_Home_Lab_All-in-One_Build_Guide.pdf"

NAVY = colors.HexColor("#0B1739")
NAVY_2 = colors.HexColor("#111F46")
INK = colors.HexColor("#15233B")
MUTED = colors.HexColor("#5D6B82")
PAPER = colors.HexColor("#F5F7FB")
LINE = colors.HexColor("#D8DEEA")
BLUE = colors.HexColor("#1676D2")
AMBER = colors.HexColor("#D88A09")
GREEN = colors.HexColor("#228A55")
RED = colors.HexColor("#C93B4B")
PURPLE = colors.HexColor("#7851A9")
TEAL = colors.HexColor("#138A87")

CALLOUT_COLORS = {
    "action": BLUE,
    "why": AMBER,
    "expect": GREEN,
    "warning": RED,
    "concept": PURPLE,
    "mindset": TEAL,
    "status": BLUE,
}

CALLOUT_TINTS = {
    "action": colors.HexColor("#EDF4FF"),
    "why": colors.HexColor("#FFF6E6"),
    "expect": colors.HexColor("#EAF7F0"),
    "warning": colors.HexColor("#FDECEC"),
    "concept": colors.HexColor("#F3EDFB"),
    "mindset": colors.HexColor("#E7F5F5"),
    "status": colors.HexColor("#EDF4FF"),
}


def inline_markup(text: str) -> str:
    """Convert the limited inline Markdown used in the guide to ReportLab XML."""
    text = html.escape(text.strip(), quote=False)
    text = re.sub(r"`([^`]+)`", r'<font name="Courier" color="#0B4F82">\1</font>', text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"\[([^]]+)\]\(([^)]+)\)", r'<link href="\2" color="#1676D2">\1</link>', text)
    return text


class SectionBanner(Flowable):
    def __init__(self, text: str, width: float, height: float = 24 * mm):
        super().__init__()
        self.text = text
        self.width = width
        self.height = height

    def draw(self):
        c = self.canv
        c.saveState()
        c.setFillColor(NAVY)
        c.roundRect(0, 0, self.width, self.height, 4 * mm, fill=1, stroke=0)
        c.setFillColor(BLUE)
        c.rect(0, 0, 4 * mm, self.height, fill=1, stroke=0)
        c.setFillColor(colors.white)
        max_width = self.width - 17 * mm
        title = self.text
        font_size = 17
        while stringWidth(title, "Helvetica-Bold", font_size) > max_width and font_size > 12.5:
            font_size -= 0.5
        while stringWidth(title, "Helvetica-Bold", font_size) > max_width and len(title) > 8:
            title = title[:-1]
        if title != self.text:
            title = title.rstrip() + "..."
        c.setFont("Helvetica-Bold", font_size)
        c.drawString(11 * mm, 9 * mm, title)
        c.restoreState()


class AccentCardTable(Table):
    """A rounded callout card with a curved accent rail and inward color glow."""

    def __init__(self, *args, accent, fill, radius=2.5 * mm, **kwargs):
        super().__init__(*args, **kwargs)
        self.accent = accent
        self.fill = fill
        self.radius = radius

    def _rounded_path(self, width, height):
        r = min(self.radius, width / 2, height / 2)
        k = 0.5522847498
        p = self.canv.beginPath()
        p.moveTo(r, 0)
        p.lineTo(width - r, 0)
        p.curveTo(width - r + k * r, 0, width, r - k * r, width, r)
        p.lineTo(width, height - r)
        p.curveTo(width, height - r + k * r, width - r + k * r, height, width - r, height)
        p.lineTo(r, height)
        p.curveTo(r - k * r, height, 0, height - r + k * r, 0, height - r)
        p.lineTo(0, r)
        p.curveTo(0, r - k * r, r - k * r, 0, r, 0)
        p.close()
        return p

    def draw(self):
        c = self.canv
        width, height = self._width, self._height
        r = min(self.radius, width / 2, height / 2)
        k = 0.5522847498

        c.saveState()
        c.setFillColor(self.fill)
        c.roundRect(0, 0, width, height, r, fill=1, stroke=0)

        # Clip a smooth accent wash to the rounded card. The gradient visually
        # fuses the edge rail into the panel without reducing text contrast.
        c.clipPath(self._rounded_path(width, height), stroke=0, fill=0)
        def mixed(accent_weight):
            base_weight = 1 - accent_weight
            return colors.Color(
                self.fill.red * base_weight + self.accent.red * accent_weight,
                self.fill.green * base_weight + self.accent.green * accent_weight,
                self.fill.blue * base_weight + self.accent.blue * accent_weight,
            )
        c.linearGradient(
            0, 0, 14 * mm, 0,
            (mixed(0.16), mixed(0.055), self.fill),
            positions=(0, 0.42, 1), extend=True,
        )
        c.restoreState()

        super().draw()

        # Follow the top-left and bottom-left corner arcs exactly, as in the
        # reference design, instead of terminating a straight rule abruptly.
        c.saveState()
        c.setStrokeColor(self.accent)
        c.setLineWidth(2.15)
        c.setLineCap(1)
        p = c.beginPath()
        p.moveTo(r, height - 0.15)
        p.curveTo(r - k * r, height - 0.15, 0.8, height - r + k * r, 0.8, height - r)
        p.lineTo(0.8, r)
        p.curveTo(0.8, r - k * r, r - k * r, 0.15, r, 0.15)
        c.drawPath(p, stroke=1, fill=0)
        c.restoreState()


class NumberedCanvasMixin:
    pass


def styles():
    base = getSampleStyleSheet()
    return {
        "cover_kicker": ParagraphStyle(
            "CoverKicker", parent=base["Normal"], fontName="Helvetica-Bold",
            fontSize=9, leading=12, textColor=colors.HexColor("#77B9FF"),
            alignment=TA_CENTER, spaceAfter=8 * mm,
        ),
        "cover_title": ParagraphStyle(
            "CoverTitle", parent=base["Title"], fontName="Helvetica-Bold",
            fontSize=30, leading=35, textColor=colors.white, alignment=TA_CENTER,
            spaceAfter=8 * mm,
        ),
        "cover_sub": ParagraphStyle(
            "CoverSub", parent=base["Normal"], fontName="Helvetica",
            fontSize=13, leading=19, textColor=colors.HexColor("#D9E5F7"),
            alignment=TA_CENTER, spaceAfter=10 * mm,
        ),
        "cover_meta": ParagraphStyle(
            "CoverMeta", parent=base["Normal"], fontName="Helvetica",
            fontSize=9.5, leading=15, textColor=colors.HexColor("#C0CEE2"),
            alignment=TA_CENTER,
        ),
        "h1": ParagraphStyle(
            "H1", parent=base["Heading1"], fontName="Helvetica-Bold",
            fontSize=19, leading=23, textColor=NAVY, spaceBefore=9 * mm,
            spaceAfter=4 * mm, keepWithNext=True,
        ),
        "h2": ParagraphStyle(
            "H2", parent=base["Heading2"], fontName="Helvetica-Bold",
            fontSize=14, leading=18, textColor=NAVY_2, spaceBefore=6 * mm,
            spaceAfter=3 * mm, keepWithNext=True,
        ),
        "h3": ParagraphStyle(
            "H3", parent=base["Heading3"], fontName="Helvetica-Bold",
            fontSize=10.5, leading=14, textColor=INK, spaceBefore=4 * mm,
            spaceAfter=2 * mm, keepWithNext=True,
        ),
        "body": ParagraphStyle(
            "Body", parent=base["BodyText"], fontName="Helvetica",
            fontSize=9.2, leading=13.2, textColor=INK, spaceAfter=2.7 * mm,
        ),
        "bullet": ParagraphStyle(
            "Bullet", parent=base["BodyText"], fontName="Helvetica",
            fontSize=9.1, leading=13, textColor=INK, leftIndent=6 * mm,
            firstLineIndent=-3.5 * mm, bulletIndent=1.5 * mm, spaceAfter=1.4 * mm,
        ),
        "quote": ParagraphStyle(
            "Quote", parent=base["BodyText"], fontName="Helvetica-Oblique",
            fontSize=9.2, leading=13.5, textColor=MUTED, leftIndent=7 * mm,
            rightIndent=5 * mm, borderColor=BLUE, borderWidth=0,
            borderPadding=(2 * mm, 3 * mm, 2 * mm, 4 * mm), spaceAfter=3 * mm,
        ),
        "code": ParagraphStyle(
            "Code", fontName="Courier", fontSize=7.4, leading=10,
            textColor=colors.HexColor("#E8EDF7"), backColor=NAVY_2,
            borderPadding=4 * mm, spaceBefore=2 * mm, spaceAfter=4 * mm,
            splitLongWords=True,
        ),
        "callout_title": ParagraphStyle(
            "CalloutTitle", parent=base["Heading3"], fontName="Helvetica-Bold",
            fontSize=9.2, leading=12, textColor=INK, spaceAfter=1.5 * mm,
        ),
        "callout_body": ParagraphStyle(
            "CalloutBody", parent=base["BodyText"], fontName="Helvetica",
            fontSize=8.7, leading=12.2, textColor=INK, spaceAfter=1.5 * mm,
        ),
        "table_header": ParagraphStyle(
            "TableHeader", parent=base["BodyText"], fontName="Helvetica-Bold",
            fontSize=7.5, leading=9.5, textColor=colors.white,
        ),
        "table_cell": ParagraphStyle(
            "TableCell", parent=base["BodyText"], fontName="Helvetica",
            fontSize=7.2, leading=9.5, textColor=INK,
        ),
    }


S = styles()


def cover_story():
    return [
        Spacer(1, 35 * mm),
        Paragraph("CYBERSECURITY ENGINEERING PORTFOLIO", S["cover_kicker"]),
        Paragraph("Build Your Own<br/>Cybersecurity Home Lab", S["cover_title"]),
        HRFlowable(width="42%", thickness=2, color=BLUE, spaceBefore=2 * mm, spaceAfter=9 * mm),
        Paragraph(
            "Segment networks, centralize Wazuh telemetry, validate detections, "
            "and document the work.", S["cover_sub"]
        ),
        Spacer(1, 18 * mm),
        Paragraph(
            "ADD-ON ALL-IN-ONE BUILD GUIDE<br/>"
            "Verified through DET-001 - Kali build in progress<br/>"
            "VirtualBox | OPNsense | Debian | Ubuntu | Wazuh | Kali Linux<br/><br/>"
            "Version 1.0  |  31 July 2026",
            S["cover_meta"],
        ),
        PageBreak(),
    ]


def parse_table(lines: list[str], width: float):
    rows = []
    for line in lines:
        parts = [p.strip() for p in line.strip().strip("|").split("|")]
        if all(re.fullmatch(r":?-{3,}:?", p or "") for p in parts):
            continue
        rows.append(parts)
    if not rows:
        return Spacer(1, 1)
    ncols = max(len(row) for row in rows)
    for row in rows:
        row.extend([""] * (ncols - len(row)))
    data = []
    for ridx, row in enumerate(rows):
        style = S["table_header"] if ridx == 0 else S["table_cell"]
        data.append([Paragraph(inline_markup(cell), style) for cell in row])
    col_widths = [width / ncols] * ncols
    table = Table(data, colWidths=col_widths, repeatRows=1, hAlign="LEFT")
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.4, LINE),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, PAPER]),
        ("LEFTPADDING", (0, 0), (-1, -1), 2.2 * mm),
        ("RIGHTPADDING", (0, 0), (-1, -1), 2.2 * mm),
        ("TOPPADDING", (0, 0), (-1, -1), 2 * mm),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2 * mm),
    ]))
    return table


def code_box(text: str, width: float):
    pre = Preformatted(text, S["code"], maxLineLength=96)
    box = Table([[pre]], colWidths=[width])
    box.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), NAVY_2),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#27375E")),
        ("LEFTPADDING", (0, 0), (-1, -1), 3.5 * mm),
        ("RIGHTPADDING", (0, 0), (-1, -1), 3.5 * mm),
        ("TOPPADDING", (0, 0), (-1, -1), 3 * mm),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3 * mm),
    ]))
    return box


def callout(kind: str, lines: list[str], width: float):
    color = CALLOUT_COLORS.get(kind, BLUE)
    tint = CALLOUT_TINTS.get(kind, colors.HexColor("#EDF4FF"))
    title = kind.upper()
    body_lines = list(lines)
    if body_lines and body_lines[0].startswith("### "):
        title = body_lines.pop(0)[4:].strip()
    title_style = ParagraphStyle(
        f"CalloutTitle-{kind}", parent=S["callout_title"], textColor=color,
        fontSize=9.3, leading=12,
    )
    content = [Paragraph(inline_markup(title), title_style)]
    inner_width = width - 13 * mm
    i = 0
    while i < len(body_lines):
        line = body_lines[i].rstrip()
        if not line.strip():
            i += 1
            continue
        if line.startswith("```"):
            lang = line[3:].strip()
            i += 1
            block = []
            while i < len(body_lines) and not body_lines[i].startswith("```"):
                block.append(body_lines[i].rstrip())
                i += 1
            i += 1
            label = (lang.upper() + "\n") if lang and lang != "text" else ""
            content.extend([code_box(label + "\n".join(block), inner_width), Spacer(1, 2 * mm)])
            continue
        if line.startswith("|") and "|" in line[1:]:
            block = []
            while i < len(body_lines) and body_lines[i].strip().startswith("|"):
                block.append(body_lines[i])
                i += 1
            content.extend([parse_table(block, inner_width), Spacer(1, 1.5 * mm)])
            continue
        if re.match(r"^[-*] ", line):
            content.append(Paragraph("- " + inline_markup(line[2:]), S["callout_body"]))
            i += 1
            continue
        numbered = re.match(r"^(\d+)\.\s+(.*)", line)
        if numbered:
            content.append(Paragraph(numbered.group(1) + ". " + inline_markup(numbered.group(2)), S["callout_body"]))
            i += 1
            continue
        paragraph = [line.strip()]
        i += 1
        while i < len(body_lines):
            nxt = body_lines[i].rstrip()
            if not nxt.strip() or re.match(r"^(```|\||[-*] |\d+\. )", nxt):
                break
            paragraph.append(nxt.strip())
            i += 1
        content.append(Paragraph(inline_markup(" ".join(paragraph)), S["callout_body"]))
    inner = AccentCardTable(
        [[content]], colWidths=[width - 4 * mm], accent=color, fill=tint,
    )
    inner.setStyle(TableStyle([
        ("LEFTPADDING", (0, 0), (-1, -1), 5 * mm),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4 * mm),
        ("TOPPADDING", (0, 0), (-1, -1), 3.2 * mm),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2.7 * mm),
    ]))
    return KeepTogether([inner, Spacer(1, 3 * mm)])


def markdown_story(text: str, width: float):
    lines = text.splitlines()
    story = []
    i = 0
    # The first title and subtitle are represented by the designed cover.
    skipped_title = skipped_subtitle = False
    while i < len(lines):
        line = lines[i].rstrip()
        if not line.strip():
            i += 1
            continue
        if line.startswith("```"):
            lang = line[3:].strip()
            i += 1
            block = []
            while i < len(lines) and not lines[i].startswith("```"):
                block.append(lines[i].rstrip())
                i += 1
            i += 1
            label = (lang.upper() + "\n") if lang and lang != "text" else ""
            story.extend([code_box(label + "\n".join(block), width), Spacer(1, 4 * mm)])
            continue
        if line.startswith("::: "):
            kind = line[4:].strip()
            i += 1
            block = []
            while i < len(lines) and lines[i].strip() != ":::":
                block.append(lines[i])
                i += 1
            i += 1
            story.append(callout(kind, block, width))
            continue
        if line.startswith("|") and "|" in line[1:]:
            block = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                block.append(lines[i])
                i += 1
            story.extend([parse_table(block, width), Spacer(1, 4 * mm)])
            continue
        if line.startswith("# "):
            title = line[2:].strip()
            i += 1
            if not skipped_title:
                skipped_title = True
                continue
            if story and not isinstance(story[-1], PageBreak):
                story.append(PageBreak())
            story.extend([SectionBanner(title, width), Spacer(1, 6 * mm)])
            continue
        if line.startswith("## "):
            title = line[3:].strip()
            i += 1
            if not skipped_subtitle:
                skipped_subtitle = True
                continue
            # Keep the recovery step with its warning instead of orphaning the
            # warning on an otherwise nearly empty page before Part 4.
            if title.startswith(("STEP 12", "STEP 17")):
                story.append(PageBreak())
            story.append(Paragraph(inline_markup(title), S["h1"]))
            continue
        if line.startswith("### "):
            story.append(Paragraph(inline_markup(line[4:]), S["h2"]))
            i += 1
            continue
        if line.startswith("#### "):
            story.append(Paragraph(inline_markup(line[5:]), S["h3"]))
            i += 1
            continue
        if re.match(r"^[-*] ", line):
            story.append(Paragraph(inline_markup(line[2:]), S["bullet"], bulletText="-"))
            i += 1
            continue
        numbered = re.match(r"^(\d+)\.\s+(.*)", line)
        if numbered:
            story.append(Paragraph(inline_markup(numbered.group(2)), S["bullet"], bulletText=numbered.group(1) + "."))
            i += 1
            continue
        if line.startswith("> "):
            story.append(Paragraph(inline_markup(line[2:]), S["quote"]))
            i += 1
            continue
        paragraph = [line.strip()]
        i += 1
        while i < len(lines):
            nxt = lines[i].rstrip()
            if not nxt.strip() or re.match(r"^(#|```|:::|\||[-*] |\d+\. |> )", nxt):
                break
            paragraph.append(nxt.strip())
            i += 1
        story.append(Paragraph(inline_markup(" ".join(paragraph)), S["body"]))
    return story


def page_background(canvas, doc):
    page = canvas.getPageNumber()
    canvas.saveState()
    canvas.setTitle("Cybersecurity Home Lab - All-in-One Build Guide")
    canvas.setAuthor("Cybersecurity Home Lab Project")
    canvas.setSubject("Portfolio-ready VirtualBox, OPNsense, Wazuh, and Kali home lab build guide")
    if page == 1:
        canvas.setFillColor(NAVY)
        canvas.rect(0, 0, A4[0], A4[1], fill=1, stroke=0)
        canvas.setFillColor(BLUE)
        canvas.rect(0, A4[1] - 7 * mm, A4[0], 7 * mm, fill=1, stroke=0)
        canvas.setFillColor(colors.HexColor("#182A56"))
        canvas.circle(A4[0] - 14 * mm, 25 * mm, 52 * mm, fill=1, stroke=0)
    else:
        canvas.setStrokeColor(LINE)
        canvas.line(18 * mm, 15 * mm, A4[0] - 18 * mm, 15 * mm)
        canvas.setFont("Helvetica", 7.5)
        canvas.setFillColor(MUTED)
        canvas.drawString(18 * mm, 10 * mm, "CYBERSECURITY HOME LAB  |  ALL-IN-ONE BUILD GUIDE")
        canvas.drawRightString(A4[0] - 18 * mm, 10 * mm, f"PAGE {page - 1}")
    canvas.restoreState()


def build():
    if not SOURCE.exists():
        raise FileNotFoundError(SOURCE)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    page_width, page_height = A4
    left = right = 18 * mm
    top = 15 * mm
    bottom = 18 * mm
    frame = Frame(left, bottom, page_width - left - right, page_height - top - bottom, id="main")
    template = PageTemplate(id="portfolio", frames=[frame], onPage=page_background)
    doc = BaseDocTemplate(
        str(OUTPUT), pagesize=A4, leftMargin=left, rightMargin=right,
        topMargin=top, bottomMargin=bottom, pageTemplates=[template],
        title="Cybersecurity Home Lab - All-in-One Build Guide",
        author="Cybersecurity Home Lab Project",
    )
    usable_width = page_width - left - right
    text = SOURCE.read_text(encoding="utf-8")
    story = cover_story() + markdown_story(text, usable_width)
    doc.build(story)
    print(OUTPUT)


if __name__ == "__main__":
    try:
        build()
    except Exception as exc:
        print(f"PDF build failed: {exc}", file=sys.stderr)
        raise
