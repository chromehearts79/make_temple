"""Rebuild the report contents page (PDF page 5) as editable HWPX.

The title box, "Contents" heading, gray rules and PART numerals are a single image in the PDF;
they are rebuilt here as editable text and table cells. Dot leaders are drawn as a dotted cell
border instead of a run of "·" characters, so they cannot wrap when the editor's font differs.

usage: python3 work/kdn2025/p05.py <report.pdf> <out.hwpx> [--page N]
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".claude/skills/pdf-hwpx-layout/scripts"))

from hwpx_layout import Layout, cell  # noqa: E402
from pdf_coords import recipe_inputs  # noqa: E402

source, target = recipe_inputs(5, "주요사업 계량지표 구성의 적합성")
layout = Layout()
p, add_text, add_table, border = layout.p, layout.add_text, layout.add_table, layout.border
GRAY_TEXT = "#555555"
NUMERAL = "#6E6E6E"


def rich(parts, align="LEFT", line=1500):
    """One paragraph with several runs: parts are (text, size, bold, color)."""
    el = layout.p("", 100, align=align, line=line)
    el.remove(el[0])
    for text, size, bold, color in parts:
        run = layout.sub(el, "hp:run", charPrIDRef=layout.char(size, bold, color, 100))
        layout.sub(run, "hp:t").text = text
    return el


def empty():
    return [p("", 100, line=100)]


box = border(top="strong", sides="strong")
bar = border("#C8C8C8")
leader = border(bottom="dot")

# Title box, "Contents" and the gray rule (image in the PDF, x 77–535pt, y 92–322pt).
add_text("", 100, line=5900)
cols = [2040, 15900, 29900, 2060]
add_table([
    [cell(0, cols[0], 14400, empty()),
     cell(1, cols[1], 14400, [rich([("2025", 4000, True, GRAY_TEXT), ("년도", 2700, True, GRAY_TEXT)], "CENTER", 4400),
                              p("경영실적", 3800, True, GRAY_TEXT, align="CENTER", line=4400, ratio=100),
                              p("보 고 서", 3800, True, GRAY_TEXT, align="CENTER", line=4400, ratio=100)], box),
     cell(2, cols[2] + cols[3], 14400, empty(), colspan=2)],
    [cell(0, sum(cols), 3000, empty(), colspan=4)],
    [cell(0, cols[0], 4800, empty()),
     cell(1, sum(cols[1:]), 4800, [p("Contents", 3400, True, "#333333", line=3800, ratio=100)], colspan=3)],
    [cell(0, cols[0], 800, empty()),
     cell(1, cols[1] + cols[2], 800, empty(), bar, colspan=2),
     cell(3, cols[3], 800, empty())],
], gap=3300)

INDENT, NUM_COL, TITLE_COL, PAGE_COL = 13940, 4600, 29360, 2600
TAIL = 49900 - INDENT - NUM_COL - TITLE_COL


def split_entry(line):
    """'1. 경영전략·····1' -> ('1. 경영전략', '1')."""
    title, _, page = line.partition("·")
    return title.rstrip(), page.strip("·").strip()


def title_width(text_width_pt, room):
    """Cell width and 장평 for a title. The PDF font's Hangul is narrow (~0.85em), so leave
    ~20% slack for the editor's font; squeeze with 장평 only when the row has no room left."""
    needed = round(text_width_pt * 100 * 1.2)
    limit = room - 900
    if needed + 700 <= limit:
        return needed + 700, 100
    return limit, max(80, (limit - 700) * 100 // needed)


def entry_cells(title, size, bold, page, text_width_pt, height):
    """[title][dotted leader][page][tail] cells, starting at grid column 2."""
    room = TITLE_COL - PAGE_COL
    tw, ratio = title_width(text_width_pt, room)
    cells = [cell(2, tw, height, [p(title, size, bold, "#161616", line=round(size * 1.25), ratio=ratio)])]
    if page:
        cells += [cell(3, room - tw, height, empty(), leader),
                  cell(4, PAGE_COL, height, [p(page, 1133, False, "#161616", align="RIGHT", line=1400, ratio=100)])]
    else:
        cells += [cell(3, room - tw + PAGE_COL, height, empty(), colspan=2)]
    return cells + [cell(5, TAIL, height, empty())]


def entry_row(title, page, text_width_pt):
    return [cell(0, INDENT, 1890, empty()), cell(1, NUM_COL, 1890, empty()),
            *entry_cells(title, 1283, False, page, text_width_pt, 1890)]


def heading_rows(roman, title, page, text_width_pt):
    """PART numeral spanning two rows; the heading sits in the lower row so a dotted
    leader (bottom border) lands just under the text, as in the PDF."""
    top, bottom = 1700, 2500
    return [[cell(0, INDENT, top + bottom, empty(), span=2),
             cell(1, NUM_COL, top + bottom, numeral(roman), span=2),
             cell(2, TITLE_COL + TAIL, top, empty(), colspan=4)],
            entry_cells(title, 1781, True, page, text_width_pt, bottom)]


def numeral(roman):
    return [p(roman, 2700, False, NUMERAL, align="CENTER", line=2800, ratio=100),
            p("PART", 760, False, NUMERAL, align="CENTER", line=900, ratio=100)]


def spans(line_text):
    """Width of the title span of a PDF line (first span), in pt."""
    for block in source.page.get_text("dict")["blocks"]:
        for line in block.get("lines", []):
            text = "".join(s["text"] for s in line["spans"]).strip()
            if text == line_text:
                first = line["spans"][0]
                return first["bbox"][2] - first["bbox"][0]
    raise ValueError(line_text)


parts = [("Ⅰ", 372, 470, 2300), ("Ⅱ", 517, 640, 2300), ("Ⅲ", 681, 703, 2300), ("Ⅳ", 746, 770, 1900)]
for roman, top, bottom, gap_after in parts:
    head, *entries = source.region(240, 250, top, bottom)
    title, page = split_entry(head)
    add_table(heading_rows(roman, title, page, spans(head)), gap=460 if entries else gap_after)
    for index, line in enumerate(entries):
        title, page = split_entry(line)
        add_table([entry_row(title, page, spans(line))], gap=gap_after if index == len(entries) - 1 else 0)

# Bottom gray rule (image in the PDF, y ≈ 791pt).
add_table([[cell(0, cols[0], 300, empty()), cell(1, cols[1] + cols[2], 300, empty(), bar, colspan=2),
            cell(3, cols[3], 300, empty())]])

print(layout.write(target))
