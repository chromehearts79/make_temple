"""Rebuild the 지표 정의 page of 안전 및 재난관리 (report page 57 = local page 7 of the 51-100 PDF).

This indicator has two sub-indicators (산업재해 / 재난), so 지표정의 has two numbered lines and
세부평가내용 has a gray sub-heading bar per sub-indicator, each with its own numbered item. The
single-indicator layout of p11.py does not fit, so this page is laid out with the kit; it keeps
p11's look (dark labels, hatched title band, rules). Labels, ①②, the black number squares and the
weight table frame are images in the PDF and are typed as cells.

usage: python3 work/kdn2025/p57.py <report p051-100.pdf> <out.hwpx> [--page 7]
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kit  # noqa: E402
from kit import Layout, recipe_inputs  # noqa: E402

source, target = recipe_inputs(7, "재난관리시스템(예방･대비･대응･복구)")
L = Layout(top=8400)
kit.setup(source, L)
from kit import *  # noqa: E402,F401,F403

LABEL = frame("#666666")
LBL = dict(size=1150, bold=True, color=WHITE, ratio=93)
TEXT_L, TEXT_R = 163.0, 535.0

# 1. 가중치 / 지표성격 / 평가방법 (top right)
xs = [X0, 332.0, 398.0, 401.0, 467.0, 471.0, 537.0, X1]
g = Grid("weights", xs, [1900, 2000])
for (a, b), x in zip(((332.0, 398.0), (401.0, 467.0), (471.0, 537.0)), (348, 413, 478)):
    g.put(a, b, 0, 1, [line1(x, x + 8, 85, 95)], frame(top="mid"), ratio=100)
    g.put(a, b, 1, 2, [runs_of(line1(x - 6, x + 8, 105, 115), bold=True)], frame("#D9D9D9"), ratio=100)
block(g, 85.0)

# 2. 지표명: label and hatched band with the indicator name
g = Grid("name", [X0, 78.0, 160.0, TEXT_L, TEXT_R, X1], [1800, 5600])
g.put(78.0, 160.0, 0, 1, "지   표   명", LABEL, **LBL)
g.put(TEXT_L, TEXT_R, 0, 1, [], frame("#F7F7F7", top="strong", hatch="#E4E4E4"))
g.put(160.0, TEXT_L, 0, 1, [], frame("#F7F7F7", hatch="#E4E4E4"))
g.put(78.0, TEXT_R, 1, 2, [runs_of(line1(200, 210, 205, 215), bold=True)], frame("#F7F7F7", hatch="#E4E4E4"),
      ratio=95, line=3300)
block(g, 187.0)

# 3. 지표정의: two numbered definitions under a rule
defs = lines_in(180, 182, 330, 365)
g = Grid("definition", [X0, 78.0, 160.0, TEXT_L, 180.0, TEXT_R, X1], [600, 1550, 1550])
g.put(78.0, 160.0, 0, 2, "지 표 정 의", LABEL, **LBL)
g.put(TEXT_L, TEXT_R, 0, 1, [], frame(top="strong"))
for row, (num, line) in enumerate(zip("①②", defs), 1):
    g.put(TEXT_L, 180.0, row, row + 1, num, align="RIGHT", size=1100, ratio=100)
    g.put(180.0, TEXT_R, row, row + 1, [line], align="LEFT", ratio=100)
block(g, 325.0)

# 4. 세부평가내용: per sub-indicator a gray bar (①/②) and its numbered item
heads = lines_in(186, 190, 420, 520)
items = [lines_in(182, 184, 445, 485), lines_in(182, 184, 515, 555)]
ys = [417.0, 425.0, 443.0, 449.0, 465.0, 481.0, 495.5, 513.5, 520.0, 536.0, 552.0]
hs = [int(round((b - a) * 100)) for a, b in zip(ys, ys[1:])]
g = Grid("items", [X0, 78.0, 160.0, TEXT_L, 169.0, 180.0, 182.9, TEXT_R, X1], hs)
g.put(78.0, 160.0, 0, 2, "세부평가내용", LABEL, **LBL)
g.put(TEXT_L, TEXT_R, 0, 1, [], frame(top="strong"))
for k, (head, lines, top) in enumerate(zip(heads, items, (1, 6))):
    g.put(169.0, TEXT_R, top, top + 1, [[("①②"[k] + " ", 1090, True, INK)] + runs_of(head, bold=True)],
          frame("#E3E3E3", left="strong"), align="LEFT", ratio=95)
    g.put(169.0, 180.0, top + 2, top + 3, "1", frame("#3A3A3A"), size=900, bold=True, color=WHITE, ratio=100)
    for r, line in enumerate(lines, top + 2):
        g.put(182.9, TEXT_R, r, r + 1, [line], align="LEFT", ratio=100)
block(g, 417.0)

# 5. 지표관리부서: contacts table
rows = sorted({round(l["bbox"][1], 1) for l in lines_in(170, 560, 728, 805)})
cols = [TEXT_L, 276.0, 333.0, 415.0, 553.0]
g = Grid("contacts", [X0, 78.0, 160.0, *cols, X1], [1800] + [1840] * len(rows))
g.put(78.0, 160.0, 0, 1, "지표관리부서", LABEL, **LBL)
for j, (a, b) in enumerate(zip(cols, cols[1:])):
    head = lines_in(a, b, 708, 718)
    g.put(a, b, 0, 1, [head[0]], frame(top="strong", bottom="soft", left="soft" if j else None),
          size=1040, ratio=100)
aligns = ["DISTRIBUTE", "DISTRIBUTE", "CENTER", "RIGHT"]
for r, y in enumerate(rows, 1):
    for j, (a, b) in enumerate(zip(cols, cols[1:])):
        hit = lines_in(a, b, y - 1, y + 1)
        fill = frame("#F3F3F3", bottom="soft", left="soft") if j else frame(bottom="soft")
        g.put(a, b, r, r + 1, [hit[0]] if hit else [], fill, align=aligns[j], ratio=100)
block(g, 709.0)

kit.finish(target, end=805.0)
