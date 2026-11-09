"""지표 정의 page for indicators with several sub-indicators (report pages 57, 121, 147).

Such a page numbers its definitions (①②…) and, under 세부평가내용, has one gray sub-heading bar per
sub-indicator, each followed by its own numbered items (1, 2, … restarting per bar). The
single-indicator layout of p11.py does not fit, so this script reads the structure from the PDF:
definition lines, bar positions/lengths, whether a bar carries a circled number, the item number
squares and the contact rows. Labels, circled numbers, number squares and the weight-table frame are
images in the PDF and are typed as cells; the look follows p11.py.

usage: python3 work/kdn2025/p57.py <report PDF> <out.hwpx> --page L
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kit  # noqa: E402
from kit import Layout, recipe_inputs  # noqa: E402

source, target = recipe_inputs(7, "지표성격")
L = Layout(top=8400)
kit.setup(source, L)
from kit import *  # noqa: E402,F401,F403

LABEL = frame("#666666")
LBL = dict(size=1150, bold=True, color=WHITE, ratio=93)
TEXT_L, TEXT_R = 163.0, 535.0
CIRCLED = "①②③④⑤⑥⑦⑧⑨"
images = [tuple(i["bbox"]) for i in source.page.get_image_info()]


def boxes(x0, x1, w0, w1, h0, h1, y0=0, y1=900):
    return sorted((b for b in images if x0 <= b[0] <= x1 and w0 <= b[2] - b[0] <= w1
                   and h0 <= b[3] - b[1] <= h1 and y0 <= b[1] <= y1), key=lambda b: b[1])


def edges_to_rows(ys):
    ys = sorted(set(round(y, 1) for y in ys))
    return ys, [int(round((b - a) * 100)) for a, b in zip(ys, ys[1:])]


# 1. 가중치 / 지표성격 / 평가방법 (top right)
g = Grid("weights", [X0, 332.0, 398.0, 401.0, 467.0, 471.0, 537.0, X1], [1900, 2000])
for a, b in ((332.0, 398.0), (401.0, 467.0), (471.0, 537.0)):
    g.put(a, b, 0, 1, [lines_in(a, b, 85, 98)[0]], frame(top="mid"), ratio=100)
    g.put(a, b, 1, 2, [runs_of(lines_in(a, b, 104, 118)[0], bold=True)], frame("#D9D9D9"), ratio=100)
block(g, 85.0)

# 2. 지표명: label and hatched band with the indicator name (the 30 pt line)
name = max(LINES, key=lambda l: max(s["size"] for s in l["spans"]))
g = Grid("name", [X0, 78.0, 160.0, TEXT_L, TEXT_R, X1], [1800, 5600])
g.put(78.0, 160.0, 0, 1, "지   표   명", LABEL, **LBL)
g.put(TEXT_L, TEXT_R, 0, 1, [], frame("#F7F7F7", top="strong", hatch="#E4E4E4"))
g.put(160.0, TEXT_L, 0, 1, [], frame("#F7F7F7", hatch="#E4E4E4"))
g.put(78.0, TEXT_R, 1, 2, [runs_of(name, bold=True)], frame("#F7F7F7", hatch="#E4E4E4"), ratio=95, line=3300)
block(g, 187.0)

# Section rules (the thin image bars under 지표정의 and 세부평가내용).
rules = boxes(160, 166, 360, 380, 2, 6)
def_top, items_top = rules[0][1], rules[1][1]
header = line1(205, 215, items_top + 60, 800)                       # "직 위"
contacts_top = header["bbox"][1] - 4.0

# 3. 지표정의: numbered definitions under a rule
defs = lines_in(178, 184, def_top, items_top - 20)
g = Grid("definition", [X0, 78.0, 160.0, TEXT_L, 180.0, TEXT_R, X1], [600] + [1550] * len(defs))
g.put(78.0, 160.0, 0, 2, "지 표 정 의", LABEL, **LBL)
g.put(TEXT_L, TEXT_R, 0, 1, [], frame(top="strong"))
for row, line in enumerate(defs, 1):
    g.put(TEXT_L, 180.0, row, row + 1, CIRCLED[row - 1], align="RIGHT", size=1100, ratio=100)
    g.put(180.0, TEXT_R, row, row + 1, [line], align="LEFT", ratio=100)
block(g, def_top)

# 4. 세부평가내용: per sub-indicator a gray bar and its numbered items
bars = boxes(170, 173, 100, 400, 14, 20, items_top, contacts_top)
squares = boxes(167, 171, 9, 13, 9, 13, items_top, contacts_top)
groups = []
for k, bar in enumerate(bars):
    nxt = bars[k + 1][1] if k + 1 < len(bars) else contacts_top
    circle = any(abs(b[0] - 176) < 3 and bar[1] <= b[1] <= bar[3] for b in images)
    items = []
    starts = [s for s in squares if bar[3] <= s[1] < nxt]
    for j, sq in enumerate(starts):
        end = starts[j + 1][1] - 3 if j + 1 < len(starts) else nxt - 3
        items.append(lines_in(182, 184, sq[1] - 4, end))
    groups.append((bar, circle, line1(174, 190, bar[1] - 1, bar[3]), items))

ys = [items_top, items_top + 8.0]
for bar, _, _, items in groups:
    ys += [bar[1] - 0.5, bar[3] + 0.5]
    for item in items:
        tops = [l["bbox"][1] - 1.5 for l in item]
        ys += tops + [item[-1]["bbox"][3] + 2.5]
ys, hs = edges_to_rows(ys)
row = {y: i for i, y in enumerate(ys)}
bar_ends = sorted({min(round(bar[2] + 20, 1), TEXT_R) for bar, *_ in groups})
g = Grid("items", sorted({X0, 78.0, 160.0, TEXT_L, 169.0, 180.0, 182.9, TEXT_R, X1, *bar_ends}), hs)
label_end = next(i for i, y in enumerate(ys) if y >= items_top + 20)
g.put(78.0, 160.0, 0, label_end, "세부평가내용", LABEL, **LBL)
g.put(TEXT_L, TEXT_R, 0, 1, [], frame(top="strong"))
for k, (bar, circle, text, items) in enumerate(groups):
    r = row[round(bar[1] - 0.5, 1)]
    runs = ([(CIRCLED[k] + " ", 1090, True, INK)] if circle else []) + runs_of(text, bold=True)
    g.put(169.0, min(round(bar[2] + 20, 1), TEXT_R), r, r + 1, [runs], frame("#E3E3E3", left="strong"),
          align="LEFT", ratio=95)
    for n, item in enumerate(items, 1):
        for i, line in enumerate(item):
            r = row[round(line["bbox"][1] - 1.5, 1)]
            if i == 0:
                g.put(169.0, 180.0, r, r + 1, str(n), frame("#3A3A3A"), size=900, bold=True, color=WHITE, ratio=100)
            g.put(182.9, TEXT_R, r, r + 1, [line], align="LEFT", ratio=100)
block(g, items_top)

# 5. 지표관리부서: contacts table (직위 may be split into single characters in the PDF)
rows = sorted({round(l["bbox"][1], 1) for l in lines_in(170, 560, header["bbox"][1] + 10, 840)})
cols = [TEXT_L, 276.0, 333.0, 415.0, 553.0]
g = Grid("contacts", [X0, 78.0, 160.0, *cols, X1], [1800] + [1840] * len(rows))
g.put(78.0, 160.0, 0, 1, "지표관리부서", LABEL, **LBL)
for j, (a, b) in enumerate(zip(cols, cols[1:])):
    g.put(a, b, 0, 1, [lines_in(a, b, header["bbox"][1] - 1, header["bbox"][1] + 2)[0]],
          frame(top="strong", bottom="soft", left="soft" if j else None), size=1040, ratio=100)
aligns = ["DISTRIBUTE", "DISTRIBUTE", "CENTER", "RIGHT"]
for r, y in enumerate(rows, 1):
    for j, (a, b) in enumerate(zip(cols, cols[1:])):
        hits = lines_in(a, b, y - 1, y + 1)
        text = "".join(h["text"] for h in hits)
        fill = frame("#F3F3F3", bottom="soft", left="soft") if j else frame(bottom="soft")
        g.put(a, b, r, r + 1, text, fill, align=aligns[j], size=990, ratio=100)
block(g, contacts_top)

kit.finish(target, end=contacts_top + 18 + 18.4 * len(rows) + 6)
