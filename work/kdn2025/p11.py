"""Rebuild a KDN 2025 '지표 정의' page (physical PDF page 11: 전략기획) as editable HWPX.

The same layout repeats on PDF pages 33 (윤리경영) and 47 (일자리 및 균등한 기회). Text,
section tops, the number of 세부평가내용 items, the number of 지표관리부서 rows and the
vertical gaps are derived from PDF coordinates, so `--page 33` / `--page 47` should need
only visual review.

Labels drawn as images in the PDF (지 표 명, 지 표 정 의, 세부평가내용, 지표관리부서 and the
numbered item boxes) are typed in as editable text; the chamfered label corners are omitted.

usage: python3 work/kdn2025/p11.py report.pdf out.hwpx [--page N]
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".claude/skills/pdf-hwpx-layout/scripts"))

from hwpx_layout import Layout, cell  # noqa: E402
from pdf_coords import recipe_inputs  # noqa: E402

# "지표성격" only occurs on the 지표 정의 pages (PDF 11, 33, 47).
source, target = recipe_inputs(11, "지표성격")
layout = Layout(top=8400, left=7800, right=5640)  # body x = 78 .. 555.6 pt
add_table, border, p = layout.add_table, layout.border, layout.p
reg, only = source.region, source.only
NS = layout.ns


def hu(pt):
    """PDF points to HWP units (1/100 pt)."""
    return round(pt * 100)


def ps(values, size=1080, bold=False, align="LEFT", ratio=90, color="#161616", line=1250, before=0):
    if isinstance(values, str):
        values = [values]
    return [p(t, size, bold, color, align=align, line=line, ratio=ratio, before=before if i == 0 else 0)
            for i, t in enumerate(values)]


def c(i, w, h, v, fill="1", *, bold=False, align="LEFT", size=1080, ratio=90, color="#161616",
      span=1, cols=1, line=1250, before=0):
    return cell(i, w, h, ps(v, size, bold, align, ratio, color, line, before), fill, span, cols)


def label(i, w, h, v, fill=None, **kwargs):
    return c(i, w, h, v, fill or gray, bold=True, align="CENTER", **kwargs)


def blank(i, w, h, fill="1", span=1, cols=1):
    return cell(i, w, h, [p("", 100, line=100)], fill, span, cols)


def tab(rows, gap=0):
    return add_table(rows, gap=round(gap * 100))


def tweak(table, col, *, rows=None, margin=None, valign=None):
    """Adjust cell margins (left, right in pt) or vertical alignment after building a table."""
    for tc in table.iter(layout.q("hp:tc")):
        addr = tc.find("hp:cellAddr", NS)
        if int(addr.get("colAddr")) != col or (rows is not None and int(addr.get("rowAddr")) not in rows):
            continue
        if margin:
            m = tc.find("hp:cellMargin", NS)
            m.set("left", str(hu(margin[0])))
            m.set("right", str(hu(margin[1])))
        if valign:
            tc.find("hp:subList", NS).set("vertAlign", valign)


def slash_hatch(ident):
    """Hatch as '////' like the original band (the builder's pattern default is BACK_SLASH)."""
    for item in layout.borders:
        if item.get("id") == ident:
            brush = item.find("hc:fillBrush/hc:winBrush", NS)
            brush.set("hatchStyle", "SLASH")
            brush.set("hatchColor", "#E8E8E8")
    return ident


gray = border("#E9E9E9", top="soft", bottom="soft")
dark = border("#666666")
top_line = border(top="strong")
band = slash_hatch(border("#F7F7F7", pattern=True))
band_top = slash_hatch(border("#F7F7F7", top="strong", pattern=True))
WHITE = "#FFFFFF"
X0 = 78.0                       # left margin; widths below are PDF x distances
LABEL_W, GAP_W = hu(160.2 - X0), hu(163.0 - 160.2)
TEXT_X0, TEXT_X1 = 163.0, 534.7
LABEL_KW = dict(color=WHITE, size=1150, ratio=93)

# Section tops come from the dark label images (x 78-160): 지표정의, 세부평가내용, 지표관리부서.
images = [item["bbox"] for item in source.page.get_image_info()]
label_tops = sorted(b[1] for b in images if abs(b[0] - 78) < 2 and abs(b[2] - 160.2) < 2)
header_y = next(l["bbox"][1] for l in source.lines if l["text"].replace(" ", "") == "직위")
def_top, items_top, table_top = (label_tops + [325.4, 417.0, header_y - 4])[:3]

# 1. 가중치 / 지표성격 / 평가방법 boxes at the top right (x 329-535, y 85-125).
box_x = [(329.0, 396.0), (398.5, 465.3), (467.8, 534.7)]
head_row, value_row = [blank(0, hu(box_x[0][0] - X0), 1900)], [blank(0, hu(box_x[0][0] - X0), 2100)]
col = 1
for k, (x0, x1) in enumerate(box_x):
    if k:
        head_row.append(blank(col, hu(x0 - box_x[k - 1][1]), 1900))
        value_row.append(blank(col, hu(x0 - box_x[k - 1][1]), 2100))
        col += 1
    head_row.append(c(col, hu(x1 - x0), 1900, only(x0, x1, 85, 104), border(top="strong", sides="soft"),
                      align="CENTER", size=1090, ratio=93))
    value_row.append(c(col, hu(x1 - x0), 2100, only(x0, x1, 104, 125), border("#CBCBCB"),
                       bold=True, align="CENTER", size=1090, ratio=93))
    col += 1
band_top_y, band_bottom_y = 186.6, 260.6
tab([head_row, value_row], band_top_y - 125.0)

# 2. 지표명 band: dark label, hatched band with a top rule, 30 pt centred title.
band_w = hu(534.6 - 163.0)
full_w = LABEL_W + GAP_W + band_w
tab([[label(0, LABEL_W, 2340, "지 표 명", dark, **LABEL_KW),
      blank(1, GAP_W, 2340, band), blank(2, band_w, 2340, band_top)],
     [c(0, full_w, 3800, only(X0, 560, 195, 255), band, cols=3, bold=True, align="CENTER",
        size=3000, ratio=95, line=3300)],
     [blank(0, full_w, 1260, band, cols=3)]], def_top - band_bottom_y)

# 3. 지표정의: label + definition text under a rule.
def_lines = [l for l in source.lines if 165 <= l["bbox"][0] < 560 and def_top <= l["bbox"][1] < items_top - 20]
def_bottom = max(l["bbox"][3] for l in def_lines) + 4.5
def_h = hu(def_bottom - def_top)
tab([[label(0, LABEL_W, 2400, "지 표 정 의", dark, **LABEL_KW),
      blank(1, GAP_W, 2400),
      c(2, hu(TEXT_X1 - TEXT_X0), def_h, reg(165, 560, def_top, items_top - 20), top_line,
        size=1098, ratio=90, line=1536, span=2)],
     [blank(0, LABEL_W + GAP_W, def_h - 2400, cols=2)]], items_top - def_bottom)

# 4. 세부평가내용: one row per numbered item; a wider line gap starts a new item.
item_lines = sorted((l for l in source.lines
                     if 180 <= l["bbox"][0] < 186 and items_top <= l["bbox"][1] < table_top),
                    key=lambda l: l["bbox"][1])
items = []
for line in item_lines:
    if items and line["bbox"][1] - items[-1][-1]["bbox"][1] < 18:
        items[-1].append(line)
    else:
        items.append([line])
number_boxes = [b for b in images if abs(b[0] - 168.7) < 2 and items_top <= b[1] < table_top]
assert len(number_boxes) in (0, len(items)), (len(number_boxes), len(items))
NUM_W, ITEM_W = hu(180.0 - TEXT_X0), hu(TEXT_X1 - 180.0)
starts = [items_top] + [group[0]["bbox"][1] - 4.9 for group in items[1:]]
items_bottom = items[-1][-1]["bbox"][3] + 4.5
rows = []
for k, (group, y0, y1) in enumerate(zip(items, starts, starts[1:] + [items_bottom])):
    first = group[0]["bbox"][1]
    texts = reg(180, 560, first - 1, group[-1]["bbox"][1] + 1)
    assert len(texts) == len(group), texts
    h, pad = hu(y1 - y0), hu(first - y0 - 1.5)
    fill, span = (top_line, 2) if k == 0 else ("1", 1)
    num = c(2, NUM_W, h, "①②③④⑤⑥⑦⑧⑨"[k], fill, bold=True, align="CENTER", size=1098, ratio=100,
            line=1536, before=pad, span=span)
    text = c(3, ITEM_W, h, texts, fill, size=1098, ratio=90, line=1536, before=pad, span=span)
    if k == 0:
        rows.append([label(0, LABEL_W, 2400, "세부평가내용", dark, **LABEL_KW), blank(1, GAP_W, 2400), num, text])
        rows.append([blank(0, LABEL_W + GAP_W, h - 2400, cols=2)])
    else:
        rows.append([blank(0, LABEL_W + GAP_W, h, cols=2), num, text])
items_table = tab(rows, table_top - items_bottom)
tweak(items_table, 2, valign="TOP")
tweak(items_table, 3, valign="TOP")

# 5. 지표관리부서 contact table: header row plus one row per person (column x from the vector rules).
cols_x = [162.8, 276.4, 333.1, 415.3, 554.3]
widths = [hu(b - a) for a, b in zip(cols_x, cols_x[1:])]
row_tops = sorted({round(l["bbox"][1], 1) for l in source.lines
                   if cols_x[0] < l["bbox"][0] < cols_x[1] and l["bbox"][1] > header_y + 5})
HEAD_H, ROW_H = hu(header_y + 14.4 - table_top), 1842
head_fills = [border(top="strong", bottom="soft"), border(top="strong", bottom="soft", sides="soft"),
              border(top="strong", bottom="soft", sides="soft"), border(top="strong", bottom="soft")]
heads = [only(a, b, header_y - 1, header_y + 3) for a, b in zip(cols_x, cols_x[1:])]
rows = [[label(0, LABEL_W, HEAD_H, "지표관리부서", dark, **LABEL_KW), blank(1, GAP_W, HEAD_H)]
        + [label(j + 2, w, HEAD_H, t, f, size=1041, ratio=93)
           for j, (w, t, f) in enumerate(zip(widths, heads, head_fills))]]
aligns = ["DISTRIBUTE", "DISTRIBUTE", "CENTER", "RIGHT"]
for r, y in enumerate(row_tops):
    edge = "strong" if r == len(row_tops) - 1 else "soft"
    fills = [border(bottom=edge), border("#EBEBEB", bottom=edge, sides="soft"),
             border("#EBEBEB", bottom=edge, sides="soft"), border("#EBEBEB", bottom=edge)]
    # 직위 may be split into single characters (e.g. 기 / 획 / 처 / 장); join them back.
    values = ["".join(reg(a, b, y - 1, y + 3)) if j == 0 else only(a, b, y - 1, y + 3)
              for j, (a, b) in enumerate(zip(cols_x, cols_x[1:]))]
    row = [] if r else [blank(0, LABEL_W + GAP_W, ROW_H * len(row_tops), span=len(row_tops), cols=2)]
    row += [c(j + 2, w, ROW_H, v, f, align=a, size=990, ratio=95)
            for j, (w, v, f, a) in enumerate(zip(widths, values, fills, aligns))]
    rows.append(row)
contact = tab(rows)
data_rows = range(1, len(rows))
tweak(contact, 2, rows=data_rows, margin=(177.18 - cols_x[0], cols_x[1] - 262.2))
# 성명 spans 287.8-321.7 in the PDF; 2 pt looser margins keep "한 재 희" on one line.
tweak(contact, 3, rows=data_rows, margin=(287.76 - cols_x[1] - 2, cols_x[2] - 321.72 - 2))
tweak(contact, 5, rows=data_rows, margin=(3.2, cols_x[4] - 547.2))

print(layout.write(target))
