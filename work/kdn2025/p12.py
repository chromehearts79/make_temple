"""Rebuild a KDN 2025 '세부목차' page (physical PDF page 12: 전략기획) as editable HWPX.

The same layout repeats on PDF pages 34 (윤리경영) and 48 (일자리 및 균등한 기회). Main
entries (Ⅰ, Ⅱ ...), 평가내용 boxes and their numbered sub-entries are classified from the
PDF lines (font size, x position, leader dots) and placed at their PDF y positions, so
`--page 34` / `--page 48` should need only visual review.

Each TOC entry is a borderless one-row table: [title][leader cell with a dotted bottom
border][right-aligned page number]. The leader dots themselves are not reproduced as text.
Text that is only in images (2025년 경영실적보고서, 세부목차, 평가내용 N) is typed in; the
Kdn logo and the chamfered box corners are omitted.

usage: python3 work/kdn2025/p12.py report.pdf out.hwpx [--page N]
"""

import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".claude/skills/pdf-hwpx-layout/scripts"))

from hwpx_layout import Layout, cell  # noqa: E402
from pdf_coords import recipe_inputs  # noqa: E402

# "세부 평가내용별" + leader dots only occur together on the 세부목차 pages (PDF 12, 34, 48).
source, target = recipe_inputs(12, "세부 평가내용별")
if "·····" not in source.page.get_text():
    sys.exit("PDF page has no table-of-contents leader dots; not a 세부목차 page")
X0, X1 = 78.0, 534.0
layout = Layout(top=10500, left=7800, right=round((612 - X1) * 100))  # body x = 78 .. 534 pt
add_text, add_table, border, p = layout.add_text, layout.add_table, layout.border, layout.p
reg, only = source.region, source.only
NS = layout.ns
BODY_W = round((X1 - X0) * 100)


def hu(pt):
    """PDF points to HWP units (1/100 pt)."""
    return round(pt * 100)


def ps(values, size=1080, bold=False, align="LEFT", ratio=93, color="#161616", line=1250, before=0):
    if isinstance(values, str):
        values = [values]
    return [p(t, size, bold, color, align=align, line=line, ratio=ratio, before=before if i == 0 else 0)
            for i, t in enumerate(values)]


def c(i, w, h, v, fill="1", *, bold=False, align="LEFT", size=1080, ratio=93, color="#161616",
      span=1, cols=1, line=1250, before=0):
    return cell(i, w, h, ps(v, size, bold, align, ratio, color, line, before), fill, span, cols)


def blank(i, w, h, fill="1", span=1, cols=1):
    return cell(i, w, h, [p("", 100, line=100)], fill, span, cols)


def tab(rows, gap=0):
    return add_table(rows, gap=hu(gap))


def valign(table, value, cols=None):
    for tc in table.iter(layout.q("hp:tc")):
        if cols is None or int(tc.find("hp:cellAddr", NS).get("colAddr")) in cols:
            tc.find("hp:subList", NS).set("vertAlign", value)


def variant(ident, *, clear=(), hatch=None):
    """Copy a border fill as a new style: drop some edges or restyle the hatch."""
    el = deepcopy(next(item for item in layout.borders if item.get("id") == ident))
    for side in clear:
        el.find(f"hh:{side}Border", NS).set("type", "NONE")
    if hatch:
        brush = el.find("hc:fillBrush/hc:winBrush", NS)
        brush.set("hatchStyle", "SLASH")
        brush.set("hatchColor", hatch)
    return layout.append_style(layout.borders, el)


leader = border(bottom="dot")
pill = border("#8C8C8C")
hatch_bottom = variant(border("#F7F7F7", bottom="soft", pattern=True), hatch="#E8E8E8")
frame = variant(border(top="soft", bottom="soft", sides="soft"), clear=("left",))

# Positioned characters, to find where each title ends and its leader dots begin.
raw_lines = [(line["bbox"], [ch for span in line["spans"] for ch in span["chars"]])
             for block in source.page.get_text("rawdict", flags=0)["blocks"] for line in block.get("lines", [])]


def leader_start(bbox):
    for box, chars in raw_lines:
        if abs(box[0] - bbox[0]) < 0.5 and abs(box[1] - bbox[1]) < 0.5:
            return next(ch["bbox"][0] for ch in chars if ch["c"] == "·")
    raise ValueError(f"No positioned characters for line at {bbox}")


# Page heading: running head under the (omitted) logo, 세부목차, indicator title, grey rule.
add_text("2025년 경영실적보고서", 1020, color="#6E6E6E", align="RIGHT", line=1300, ratio=95)
add_text("세부목차", 1750, True, color="#595959", line=2200, before=900, ratio=95)
heading = next(l for l in source.lines if l["bbox"][1] < 200 and max(l["sizes"]) > 20)
add_text(only(X0, 400, heading["bbox"][1] - 1, heading["bbox"][1] + 1), 2500, True,
         line=3000, before=1000, after=800, ratio=95)
rule_bottom = 206.0

# Classify the TOC lines below the rule.
toc = sorted((l for l in source.lines if l["bbox"][1] > rule_bottom), key=lambda l: l["bbox"][1])
elements = []  # (kind, top, bottom, payload)
for line in toc:
    x, y0, y1 = line["bbox"][0], line["bbox"][1], line["bbox"][3]
    if "·" in line["text"]:
        kind = "main" if max(line["sizes"]) > 11 else "sub"
        elements.append([kind, y0 - 3, y1 + 1, [line]])
    elif elements and elements[-1][0] == "box" and y0 - elements[-1][3][-1]["bbox"][1] < 16:
        elements[-1][3].append(line)
        elements[-1][2] = y1
    else:
        elements.append(["box", y0, y1, [line]])

# 평가내용 boxes: take the frame extent from the hatched label images when present.
images = [item["bbox"] for item in source.page.get_image_info()]
for element in elements:
    if element[0] != "box":
        continue
    lines = element[3]
    near = [b for b in images if abs(b[0] - 79.3) < 1.5
            and lines[0]["bbox"][1] - 15 <= b[1] <= lines[-1]["bbox"][3] + 10]
    element[1] = min((b[1] for b in near), default=lines[0]["bbox"][1] - 7.6)
    element[2] = max((b[3] for b in near), default=lines[-1]["bbox"][3] + 7.5)

first_top = elements[0][1]
tab([[blank(0, hu(533.0 - X0), 800, border("#BFBFBF"))]], first_top - rule_bottom)

PILL_W, NUM_W = hu(121.5 - X0), hu(138.7 - 121.5)
TITLE_W = hu(533.2 - 138.7)
PAGE_W = 2400
box_number = 0
for k, (kind, top, bottom, lines) in enumerate(elements):
    gap = elements[k + 1][1] - bottom if k + 1 < len(elements) else 0
    height = hu(bottom - top)
    if kind == "box":
        box_number += 1
        texts = reg(138, 560, lines[0]["bbox"][1] - 1, lines[-1]["bbox"][1] + 1)
        assert len(texts) == len(lines), texts
        pill_h = 1740
        table = tab([[c(0, PILL_W, pill_h, "평가내용", pill, align="CENTER", size=830,
                        color="#FFFFFF", line=1000),
                      c(1, NUM_W, height, str(box_number), hatch_bottom, bold=True, align="CENTER",
                        size=2200, ratio=80, line=2400, span=2),
                      c(2, TITLE_W, height, texts, frame, bold=True, size=1050, ratio=93, line=1396, span=2)],
                     [blank(0, PILL_W, height - pill_h, hatch_bottom)]], gap)
        valign(table, "TOP", cols=(1,))
        continue
    line = lines[0]
    x, y = line["bbox"][0], line["bbox"][1]
    text = only(x - 1, x + 1, y - 1, y + 1)
    match = re.fullmatch(r"(.*?)\s*·{3,}\s*(\d+)", text)
    assert match, text
    title, page_no = match.groups()
    main = kind == "main"
    spacer = hu(x - 3.2 - X0)
    # Title cell: PDF title width x 1.08 plus cell padding; the leader takes the rest.
    title_w = hu((leader_start(line["bbox"]) - x) * 1.08 + 5.0)
    leader_w = BODY_W - spacer - title_w - PAGE_W
    ratio = 93
    if leader_w < 800:  # very long title: keep a short leader and condense the title instead
        ratio = max(70, int(93 * (title_w - (800 - leader_w)) / title_w))
        title_w -= 800 - leader_w
        leader_w = 800
    size, line_h = (1187, 1400) if main else (939, 1150)
    table = tab([[blank(0, spacer, height),
                  c(1, title_w, height, title, bold=main, size=size, ratio=ratio, line=line_h),
                  blank(2, leader_w, height, leader),
                  c(3, PAGE_W, height, page_no, align="RIGHT", size=939, ratio=93, line=line_h)]], gap)
    valign(table, "BOTTOM")

print(layout.write(target))
