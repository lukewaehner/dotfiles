#!/usr/bin/env python3
"""
build_report.py — JSON -> Meteora house-format .docx for the antitrust-minute-1 memo.

Only used when the user explicitly asks for a document; the default deliverable
for this skill is the memo in chat. Filename convention (house standard):
"Antitrust Minute-1 - {ACQUIRER} x {TARGET} (MM.DD.YYYY)".

The presentation layer (US Letter, dark header rows, zebra striping, accent-bar
callouts, source captions, small-type appendix) is IDENTICAL on every run of
this skill, so it lives here instead of being re-emitted as ~400 lines of
docx-js each time. The model emits only CONTENT as JSON and runs:

    python3 build_report.py content.json out.docx

It also writes out.checklist.txt from every "verify" string in the JSON, so the
verification checklist is a by-product of authoring rather than a second pass
reconstructed from memory.

JSON schema (all keys optional except title/sections):

{
  "cover": {                                  # Meteora house cover block
     "firm": "METEORA CAPITAL",
     "tagline": "Event-Driven Research  |  Deal Completion Risk Assessment",
     "title_lines": ["Grant Thornton Advisors", "proposed acquisition of",
                     "CBIZ, Inc. (NYSE: CBZ)"],
     "table": { ...standard table spec; use a RAG cell on the
                "Overall completion assessment" row... },
     "disclaimer": "Prepared as internal investment research ...",
     "report_date": "July 29, 2026"},
  "toc": true,                                # Word TOC field (blank in LibreOffice preview)
  "footer": "Internal investment research — not investment, legal, or tax advice",
  "title": "optional plain title (omit when cover is used)",
  "subtitle": "As of <date>. Blind fundamental assessment ...",
  "verdict": {"title": "Verdict", "accent": "C00000",
              "lines": ["one sentence verdict", "compensated tail", "decisive fact"]},
  "exec_summary": [["The deal: ", "..."], ["Where it stands: ", "..."]],
  "exec_note": "italic citation line under the exec summary",
  "sections": [
    {"heading": "1. Executive Summary & Deal Completion Risk Matrix",
     "takeaway": "bold one-liner",
     "blocks": [
        {"p": "prose paragraph"},
        {"assessment": "labelled opinion"},
        {"table": {"title": "Deal Completion Risk Matrix",
                   "headers": [...], "widths": [...],
                   "rows": [["Antitrust / HSR", ["LOW RISK", "G"], "rationale ..."],
                            ["OVERALL", ["HIGH", "G"], "..."]],
                   "caption": "Source: ...",
                   "bold_rows": [0, 3]}},
        {"callout": {"title": "...", "accent": "2E7D32", "lines": [...]}}
     ]}
  ],
  "sources": ["EDGAR: ...", "..."],
  "integrity_note": "...",
  "verify": ["$55.00", "Grisko", "..."]      # -> out.checklist.txt
}

RAG cells: any table cell may be a two-element array ["text", code] with code in
{"G","A","R"} — rendered as a bold, color-shaded assessment cell (green/amber/red)
per the Meteora convention (green = favorable to completion, so "HIGH probability
of completion" is GREEN; red = HIGH RISK). Plain-string cells are unchanged.
The footer is STATIC text only — never a PageNumber field (house constraint).

Stage C assembly mode (zero re-emission fan-out):
    python3 build_report.py --assemble merged.json base.json frag-*.json
Merges drafter fragments ({"sections","verify","sources","crosscuts"}) over the
main loop's base skeleton, orders sections by their leading number, de-dups
sources, and prints crosscuts[] to stdout for reconciliation before building.

Widths are DXA (1440 = 1 inch); they are normalised to the 10000-DXA text
column automatically, so approximate relative weights are fine.
"""

import json
import sys
from pathlib import Path

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_ALIGN_VERTICAL
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, RGBColor, Emu

DARK = "1F3864"
ZEBRA = "F2F2F2"
CALLOUT_BG = "F2F5FB"
TEXT_WIDTH = 10000  # DXA

# RAG palette: fill, ink. Green = favorable to completion; red = adverse.
RAG_COLORS = {"G": ("C6EFCE", "006100"),
              "A": ("FFEB9C", "9C6500"),
              "R": ("FFC7CE", "9C0006")}


def _rag(val):
    """Return (text, rag_code) — rag_code None for plain cells."""
    if (isinstance(val, (list, tuple)) and len(val) == 2
            and val[1] in RAG_COLORS):
        return val[0], val[1]
    return val, None


def _shade(cell, hexcolor):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hexcolor)
    tcPr.append(shd)


def _set_cell_width(cell, dxa):
    tcPr = cell._tc.get_or_add_tcPr()
    tcW = tcPr.find(qn("w:tcW"))
    if tcW is None:
        tcW = OxmlElement("w:tcW")
        tcPr.append(tcW)
    tcW.set(qn("w:w"), str(int(dxa)))
    tcW.set(qn("w:type"), "dxa")


def _no_borders(table):
    tblPr = table._tbl.tblPr
    borders = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        el = OxmlElement(f"w:{edge}")
        el.set(qn("w:val"), "none")
        el.set(qn("w:sz"), "0")
        borders.append(el)
    tblPr.append(borders)


def _fixed_layout(table, widths):
    """Force fixed layout + explicit tblGrid, else Word/LO re-flows columns."""
    tblPr = table._tbl.tblPr
    layout = OxmlElement("w:tblLayout")
    layout.set(qn("w:type"), "fixed")
    tblPr.append(layout)
    tblW = OxmlElement("w:tblW")
    tblW.set(qn("w:w"), str(int(sum(widths))))
    tblW.set(qn("w:type"), "dxa")
    tblPr.append(tblW)
    grid = table._tbl.find(qn("w:tblGrid"))
    if grid is not None:
        table._tbl.remove(grid)
    grid = OxmlElement("w:tblGrid")
    for w in widths:
        gc = OxmlElement("w:gridCol")
        gc.set(qn("w:w"), str(int(w)))
        grid.append(gc)
    table._tbl.insert(list(table._tbl).index(tblPr) + 1, grid)


def _repeat_header(row):
    trPr = row._tr.get_or_add_trPr()
    el = OxmlElement("w:tblHeader")
    el.set(qn("w:val"), "true")
    trPr.append(el)


def _write_cell(cell, text, *, bold=False, color=None, size=9):
    cell.text = ""
    para = cell.paragraphs[0]
    para.paragraph_format.space_before = Pt(2)
    para.paragraph_format.space_after = Pt(2)
    run = para.add_run("" if text is None else str(text))
    run.bold = bold
    run.font.size = Pt(size)
    if color:
        run.font.color.rgb = RGBColor.from_string(color)
    cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER


def add_paragraph(doc, text, *, bold=False, italic=False, size=11, after=6):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(after)
    run = p.add_run(text)
    run.bold = bold
    run.italic = italic
    run.font.size = Pt(size)
    return p


def add_labelled(doc, label, text, *, size=11, after=7):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(after)
    r1 = p.add_run(label)
    r1.bold = True
    r1.font.size = Pt(size)
    r2 = p.add_run(text)
    r2.font.size = Pt(size)
    return p


def add_assessment(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(6)
    r1 = p.add_run("Assessment: ")
    r1.bold = True
    r1.italic = True
    r1.font.size = Pt(10.5)
    r2 = p.add_run(text)
    r2.italic = True
    r2.font.size = Pt(10.5)
    return p


def add_callout(doc, spec):
    accent = spec.get("accent", "C00000")
    tbl = doc.add_table(rows=1, cols=2)
    _no_borders(tbl)
    tbl.autofit = False
    _fixed_layout(tbl, [170, TEXT_WIDTH - 170])
    bar, body = tbl.rows[0].cells
    _set_cell_width(bar, 170)
    _set_cell_width(body, TEXT_WIDTH - 170)
    _shade(bar, accent)
    _shade(body, CALLOUT_BG)
    bar.text = ""

    body.text = ""
    first = body.paragraphs[0]
    first.paragraph_format.space_after = Pt(5)
    r = first.add_run(spec.get("title", "Verdict"))
    r.bold = True
    r.font.size = Pt(12)
    for line in spec.get("lines", []):
        p = body.add_paragraph()
        p.paragraph_format.space_after = Pt(4)
        run = p.add_run(line)
        run.font.size = Pt(10.5)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)
    return tbl


def add_table(doc, spec):
    title = spec.get("title")
    if title:
        h = doc.add_heading(title, level=3)
        h.paragraph_format.space_before = Pt(10)
        h.paragraph_format.space_after = Pt(4)

    headers = spec["headers"]
    rows = spec.get("rows", [])
    ncols = len(headers)
    widths = spec.get("widths") or [TEXT_WIDTH // ncols] * ncols
    total = sum(widths) or TEXT_WIDTH
    widths = [w * TEXT_WIDTH / total for w in widths]
    bold_rows = set(spec.get("bold_rows", []))

    tbl = doc.add_table(rows=1, cols=ncols)
    tbl.style = "Table Grid"
    tbl.autofit = False
    _fixed_layout(tbl, widths)

    hdr = tbl.rows[0]
    _repeat_header(hdr)
    for i, htext in enumerate(headers):
        c = hdr.cells[i]
        _set_cell_width(c, widths[i])
        _shade(c, DARK)
        _write_cell(c, htext, bold=True, color="FFFFFF", size=9)

    for ri, row in enumerate(rows):
        cells = tbl.add_row().cells
        for i in range(ncols):
            c = cells[i]
            _set_cell_width(c, widths[i])
            text, rag = _rag(row[i] if i < len(row) else "")
            if rag:
                fill, ink = RAG_COLORS[rag]
                _shade(c, fill)
                _write_cell(c, text, bold=True, color=ink, size=9)
            else:
                if ri % 2 == 1:
                    _shade(c, ZEBRA)
                _write_cell(c, text, bold=(ri in bold_rows), size=9)

    caption = spec.get("caption")
    if caption:
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(3)
        p.paragraph_format.space_after = Pt(8)
        r = p.add_run(caption)
        r.italic = True
        r.font.size = Pt(8.5)
    else:
        doc.add_paragraph().paragraph_format.space_after = Pt(4)
    return tbl


def add_cover(doc, spec):
    """Meteora house cover: firm block, deal title, parameter table,
    disclaimer, report date."""
    def centered(text, *, size, bold=False, italic=False, color=None, after=4):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(after)
        r = p.add_run(text)
        r.bold = bold
        r.italic = italic
        r.font.size = Pt(size)
        if color:
            r.font.color.rgb = RGBColor.from_string(color)
        return p

    centered(spec.get("firm", "METEORA CAPITAL"), size=22, bold=True,
             color=DARK, after=2)
    if spec.get("tagline"):
        centered(spec["tagline"], size=11, color=DARK, after=14)
    for i, line in enumerate(spec.get("title_lines", [])):
        big = i != 1  # middle "proposed acquisition of" line stays small
        centered(line, size=16 if big else 11, bold=big,
                 italic=not big, after=4)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)
    if spec.get("table"):
        add_table(doc, spec["table"])
    if spec.get("disclaimer"):
        add_paragraph(doc, spec["disclaimer"], italic=True, size=9, after=8)
    if spec.get("report_date"):
        add_paragraph(doc, f"Report date: {spec['report_date']}", size=10,
                      after=4)


def add_toc(doc):
    """Word TOC field — blank in LibreOffice preview, populates in Word."""
    doc.add_heading("Table of Contents", level=1)
    p = doc.add_paragraph()
    fld = OxmlElement("w:fldSimple")
    fld.set(qn("w:instr"), r'TOC \o "1-2" \h \z \u')
    r = OxmlElement("w:r")
    t = OxmlElement("w:t")
    t.text = "(In Word: right-click and Update Field to populate.)"
    r.append(t)
    fld.append(r)
    p._p.append(fld)
    doc.add_page_break()


def _set_footer(doc, text):
    """Static-text footer. Never a PageNumber field (house constraint)."""
    para = doc.sections[0].footer.paragraphs[0]
    para.text = ""
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = para.add_run(text)
    run.italic = True
    run.font.size = Pt(8)


def build(spec, out_path):
    doc = Document()

    sec = doc.sections[0]
    sec.page_width = Emu(12240 * 635)   # US Letter, DXA -> EMU
    sec.page_height = Emu(15840 * 635)
    sec.left_margin = Emu(1080 * 635)
    sec.right_margin = Emu(1080 * 635)
    sec.top_margin = Emu(1080 * 635)
    sec.bottom_margin = Emu(1080 * 635)

    normal = doc.styles["Normal"]
    normal.font.name = "Calibri"
    normal.font.size = Pt(11)

    if spec.get("cover"):
        add_cover(doc, spec["cover"])
        if spec.get("subtitle"):
            add_paragraph(doc, spec["subtitle"], italic=True, size=9, after=8)
        doc.add_page_break()
    if spec.get("toc"):
        add_toc(doc)

    if spec.get("title"):
        title = doc.add_heading(spec["title"], level=0)
        title.paragraph_format.space_after = Pt(3)
        if not spec.get("cover") and spec.get("subtitle"):
            add_paragraph(doc, spec["subtitle"], italic=True, size=10, after=12)

    if spec.get("verdict"):
        add_callout(doc, spec["verdict"])

    if spec.get("exec_summary"):
        doc.add_heading("Executive Summary", level=1)
        for label, text in spec["exec_summary"]:
            add_labelled(doc, label, text)
        if spec.get("exec_note"):
            add_paragraph(doc, spec["exec_note"], italic=True, size=9, after=10)

    for section in spec.get("sections", []):
        doc.add_heading(section["heading"], level=1)
        if section.get("takeaway"):
            add_paragraph(doc, section["takeaway"], bold=True, after=6)
        for block in section.get("blocks", []):
            if "p" in block:
                add_paragraph(doc, block["p"])
            elif "assessment" in block:
                add_assessment(doc, block["assessment"])
            elif "table" in block:
                add_table(doc, block["table"])
            elif "callout" in block:
                add_callout(doc, block["callout"])
            elif "labelled" in block:
                add_labelled(doc, block["labelled"][0], block["labelled"][1])

    if spec.get("integrity_note"):
        doc.add_heading("Integrity Note", level=2)
        add_paragraph(doc, spec["integrity_note"])

    if spec.get("sources"):
        doc.add_heading("Sources", level=1)
        for s in spec["sources"]:
            p = doc.add_paragraph()
            p.paragraph_format.space_after = Pt(2)
            r = p.add_run("• " + s)
            r.font.size = Pt(8.5)

    if spec.get("footer"):
        _set_footer(doc, spec["footer"])

    doc.save(out_path)
    return out_path



# ----------------------------------------------------------------- HTML render

CSS = """
:root{--dark:#1f3864;--zebra:#f2f2f2;--callout:#f2f5fb;--ink:#1a1a1a;--mut:#5a6472;--line:#d5dbe5}
*{box-sizing:border-box}
body{margin:0;padding:38px 30px 60px;font:15px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Calibri,sans-serif;
     color:var(--ink);max-width:1080px;margin-inline:auto;background:#fff}
h1{font-size:27px;line-height:1.25;margin:0 0 6px;color:var(--dark);font-weight:700}
h2{font-size:20px;margin:34px 0 10px;color:var(--dark);border-bottom:2px solid var(--line);padding-bottom:5px}
h3{font-size:14px;margin:20px 0 7px;color:var(--dark);text-transform:uppercase;letter-spacing:.4px}
.sub{color:var(--mut);font-style:italic;font-size:13px;margin:0 0 20px}
.callout{display:flex;gap:0;background:var(--callout);margin:16px 0 20px;border-radius:3px;overflow:hidden}
.callout .bar{flex:0 0 7px;background:var(--accent,#c00000)}
.callout .body{padding:13px 17px}
.callout .t{font-weight:700;font-size:16px;margin-bottom:7px}
.callout p{margin:0 0 7px;font-size:14px}
.callout p:last-child{margin-bottom:0}
.take{font-weight:700;margin:0 0 9px}
.assess{font-style:italic;color:#333;font-size:14px;margin:9px 0;padding-left:11px;border-left:3px solid var(--line)}
.assess b{font-style:italic}
table{border-collapse:collapse;width:100%;margin:9px 0 4px;font-size:12.5px;table-layout:fixed}
th{background:var(--dark);color:#fff;text-align:left;padding:7px 9px;font-weight:600;vertical-align:middle}
td{padding:6px 9px;border:1px solid var(--line);vertical-align:top;word-wrap:break-word}
tr:nth-child(even) td{background:var(--zebra)}
tr.bold td{font-weight:700}
.cap{font-size:11.5px;color:var(--mut);font-style:italic;margin:3px 0 15px}
.src{font-size:11.5px;color:var(--mut);margin:2px 0}
.note{font-size:12px;color:var(--mut);font-style:italic;margin:9px 0 16px}
p{margin:0 0 10px}
td.rag-G{background:#c6efce!important;color:#006100;font-weight:700}
td.rag-A{background:#ffeb9c!important;color:#9c6500;font-weight:700}
td.rag-R{background:#ffc7ce!important;color:#9c0006;font-weight:700}
.cover{text-align:center;margin:10px 0 26px}
.cover .firm{font-size:30px;font-weight:800;color:var(--dark);letter-spacing:1px}
.cover .tag{font-size:14px;color:var(--dark);margin:4px 0 22px}
.cover .big{font-size:20px;font-weight:700;margin:4px 0}
.cover .small{font-size:13px;font-style:italic;margin:2px 0}
.cover .disc{font-size:11.5px;font-style:italic;color:var(--mut);margin-top:12px}
.footerline{margin-top:40px;padding-top:10px;border-top:1px solid var(--line);
            font-size:11px;font-style:italic;color:var(--mut);text-align:center}
.tocbox{font-size:13.5px;margin:0 0 24px}
.tocbox li{margin:3px 0}
@media print{body{padding:0;max-width:none;font-size:10.5pt}h2{page-break-after:avoid}table{page-break-inside:avoid}}
"""


def _esc(t):
    return (str("" if t is None else t).replace("&", "&amp;")
            .replace("<", "&lt;").replace(">", "&gt;"))


def _html_callout(spec):
    accent = "#" + spec.get("accent", "C00000")
    lines = "".join(f"<p>{_esc(l)}</p>" for l in spec.get("lines", []))
    return (f'<div class="callout" style="--accent:{accent}"><div class="bar"></div>'
            f'<div class="body"><div class="t">{_esc(spec.get("title","Verdict"))}</div>'
            f'{lines}</div></div>')


def _html_table(spec):
    out = []
    if spec.get("title"):
        out.append(f"<h3>{_esc(spec['title'])}</h3>")
    headers = spec["headers"]; rows = spec.get("rows", [])
    widths = spec.get("widths") or [1] * len(headers)
    tot = sum(widths) or 1
    cols = "".join(f'<col style="width:{w/tot*100:.1f}%">' for w in widths)
    bold = set(spec.get("bold_rows", []))
    out.append(f"<table><colgroup>{cols}</colgroup><thead><tr>"
               + "".join(f"<th>{_esc(h)}</th>" for h in headers) + "</tr></thead><tbody>")
    for ri, r in enumerate(rows):
        cls = ' class="bold"' if ri in bold else ""
        cells = []
        for i in range(len(headers)):
            text, rag = _rag(r[i] if i < len(r) else "")
            tdcls = f' class="rag-{rag}"' if rag else ""
            cells.append(f"<td{tdcls}>{_esc(text)}</td>")
        out.append(f"<tr{cls}>{''.join(cells)}</tr>")
    out.append("</tbody></table>")
    if spec.get("caption"):
        out.append(f'<div class="cap">{_esc(spec["caption"])}</div>')
    return "".join(out)


def _html_cover(spec):
    out = ['<div class="cover">']
    out.append(f'<div class="firm">{_esc(spec.get("firm", "METEORA CAPITAL"))}</div>')
    if spec.get("tagline"):
        out.append(f'<div class="tag">{_esc(spec["tagline"])}</div>')
    for i, line in enumerate(spec.get("title_lines", [])):
        cls = "small" if i == 1 else "big"
        out.append(f'<div class="{cls}">{_esc(line)}</div>')
    out.append("</div>")
    if spec.get("table"):
        out.append(_html_table(spec["table"]))
    if spec.get("disclaimer"):
        out.append(f'<div class="cover"><div class="disc">{_esc(spec["disclaimer"])}</div></div>')
    if spec.get("report_date"):
        out.append(f"<p>Report date: {_esc(spec['report_date'])}</p>")
    return "".join(out)


def build_html(spec, out_path):
    doc_title = (spec.get("cover", {}) or {}).get("firm") or spec.get("title", "Report")
    h = [f"<!DOCTYPE html><html lang=en><head><meta charset=utf-8>",
         f"<meta name=viewport content='width=device-width,initial-scale=1'>",
         f"<title>{_esc(doc_title)}</title><style>{CSS}</style></head><body>"]
    if spec.get("cover"):
        h.append(_html_cover(spec["cover"]))
        if spec.get("subtitle"):
            h.append(f'<p class="sub">{_esc(spec["subtitle"])}</p>')
    if spec.get("toc"):
        h.append("<h2>Table of Contents</h2><ol class='tocbox'>")
        for s in spec.get("sections", []):
            h.append(f"<li>{_esc(s['heading'])}</li>")
        if spec.get("sources"):
            h.append("<li>Sources</li>")
        h.append("</ol>")
    if spec.get("title"):
        h.append(f"<h1>{_esc(spec['title'])}</h1>")
        if not spec.get("cover") and spec.get("subtitle"):
            h.append(f'<p class="sub">{_esc(spec["subtitle"])}</p>')
    if spec.get("verdict"):
        h.append(_html_callout(spec["verdict"]))
    if spec.get("exec_summary"):
        h.append("<h2>Executive Summary</h2>")
        for label, text in spec["exec_summary"]:
            h.append(f"<p><b>{_esc(label)}</b>{_esc(text)}</p>")
        if spec.get("exec_note"):
            h.append(f'<div class="note">{_esc(spec["exec_note"])}</div>')
    for sec in spec.get("sections", []):
        h.append(f"<h2>{_esc(sec['heading'])}</h2>")
        if sec.get("takeaway"):
            h.append(f'<p class="take">{_esc(sec["takeaway"])}</p>')
        for b in sec.get("blocks", []):
            if "p" in b:
                h.append(f"<p>{_esc(b['p'])}</p>")
            elif "assessment" in b:
                h.append(f'<div class="assess"><b>Assessment:</b> {_esc(b["assessment"])}</div>')
            elif "table" in b:
                h.append(_html_table(b["table"]))
            elif "callout" in b:
                h.append(_html_callout(b["callout"]))
            elif "labelled" in b:
                h.append(f"<p><b>{_esc(b['labelled'][0])}</b>{_esc(b['labelled'][1])}</p>")
    if spec.get("integrity_note"):
        h.append(f"<h2>Integrity Note</h2><p>{_esc(spec['integrity_note'])}</p>")
    if spec.get("sources"):
        h.append("<h2>Sources</h2>")
        for s in spec["sources"]:
            h.append(f'<div class="src">&bull; {_esc(s)}</div>')
    if spec.get("footer"):
        h.append(f'<div class="footerline">{_esc(spec["footer"])}</div>')
    h.append("</body></html>")
    Path(out_path).write_text("".join(h))
    return out_path


def assemble(out_path, base_path, fragment_paths):
    """Merge Stage C drafter fragments over the main loop's base spec.

    Base: the full spec skeleton (cover, toc, footer, subtitle, the main
    loop's own sections, integrity_note). Each fragment: {"sections": [...],
    "verify": [...], "sources": [...], "crosscuts": [...]}. Sections are
    ordered by the leading number in their heading ("4. Acquirer Profile"),
    non-numbered sections keep insertion order at the end. Crosscuts are
    printed to stdout for reconciliation — they are NOT written to the report.
    """
    import re as _re
    base = json.loads(Path(base_path).read_text())
    crosscuts = []
    for fp in fragment_paths:
        frag = json.loads(Path(fp).read_text())
        base.setdefault("sections", []).extend(frag.get("sections") or [])
        base.setdefault("verify", []).extend(frag.get("verify") or [])
        base.setdefault("sources", []).extend(frag.get("sources") or [])
        for c in frag.get("crosscuts") or []:
            crosscuts.append(f"{Path(fp).name}: {c}")

    def key(sec, idx=[0]):
        m = _re.match(r"\s*(\d+)\.", sec.get("heading", ""))
        return (0, int(m.group(1))) if m else (1, idx[0])

    base["sections"] = sorted(base.get("sections", []), key=key)
    # de-dup sources while preserving order
    seen = set()
    base["sources"] = [s for s in base.get("sources", [])
                       if not (s in seen or seen.add(s))]
    Path(out_path).write_text(json.dumps(base, indent=1))
    print(f"assembled {out_path}: {len(base['sections'])} sections, "
          f"{len(base.get('verify', []))} verify entries")
    if crosscuts:
        print("CROSSCUTS to reconcile before building:")
        for c in crosscuts:
            print("  - " + c)
    else:
        print("no crosscuts flagged")


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = [a for a in sys.argv[1:] if a.startswith("--")]

    if "--assemble" in flags:
        if len(args) < 2:
            sys.exit("usage: build_report.py --assemble merged.json base.json frag1.json [frag2.json ...]")
        assemble(args[0], args[1], args[2:])
        return

    if not args:
        sys.exit("usage: build_report.py content.json [out_stem] [--format docx|html|both]\n"
                 "       build_report.py --assemble merged.json base.json frag*.json")

    fmt = "docx"
    for f in flags:
        if f.startswith("--format"):
            fmt = f.split("=", 1)[1] if "=" in f else "docx"
    if "--html" in flags:
        fmt = "html"
    if "--both" in flags:
        fmt = "both"

    spec = json.loads(Path(args[0]).read_text())
    stem = args[1] if len(args) > 1 else "report"
    stem = stem[:-5] if stem.endswith(".docx") else stem
    stem = stem[:-5] if stem.endswith(".html") else stem

    written = []
    if fmt in ("docx", "both"):
        written.append(build(spec, stem + ".docx"))
    if fmt in ("html", "both"):
        written.append(build_html(spec, stem + ".html"))

    checklist = spec.get("verify") or []
    if checklist:
        cl = stem + ".checklist.txt"
        Path(cl).write_text("\n".join(checklist) + "\n")
        written.append(cl)
        # HTML needs no render to verify - grep the source directly.
        if fmt in ("html", "both"):
            src = Path(stem + ".html").read_text()
            missing = [c for c in checklist if c not in src]
            print("VERIFIED: all %d checklist facts present in HTML" % len(checklist)
                  if not missing else
                  "MISSING from HTML (%d): %s" % (len(missing), "; ".join(missing)))
    print("wrote " + ", ".join(written))


if __name__ == "__main__":
    main()
