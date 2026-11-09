"""Rebuild a chapter cover (PDF page 9 "01 경영전략", also page 45 "02 안전 및 책임경영").

The gray background band, the dashes beside the number and the line "2025년도 경영실적보고서"
are part of a background image; that line is typed, the rest is left out. Dot leaders are a
dotted cell border.

usage: python3 work/kdn2025/p09.py <report.pdf> <out.hwpx> [--page 45]
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kit  # noqa: E402
from kit import Layout, recipe_inputs  # noqa: E402

source, target = recipe_inputs(9, "·····")
L = Layout(top=22500)
kit.setup(source, L)
from kit import *  # noqa: E402,F401,F403

number = line1(250, 300, 220, 232)
title = line1(200, 360, 295, 310)
entries = lines_in(160, 170, 370, 530)
BOX_L, IN_L, PAGE_L, IN_R, BOX_R = 136.0, 164.0, 420.0, 445.0, 476.0

split = []
for line in entries:
    name, _, rest = line["text"].partition("·")
    name, page = name.rstrip(), rest.strip("·").strip()
    width = text_width([(name, 1480, False, INK)], 86.5)          # the PDF's own width
    split.append((name, page, round(IN_L + width * 1.2 + 6, 1)))

xs = sorted({X0, BOX_L, IN_L, PAGE_L, IN_R, BOX_R, X1, *(end for *_, end in split)})
hs = [6100, 6100, 2400] + [3100] * len(split) + [int(round((538 - 370) * 100)) - 3100 * len(split)]
g = Grid("cover", xs, hs)
last = len(hs)
g.put(BOX_L, BOX_R, 0, 1, [runs_of(number, bold=True)], line=5900, ratio=100)
g.put(BOX_L, IN_L, 1, last, [], frame(left="mid", top="mid", bottom="mid"))
g.put(IN_R, BOX_R, 1, last, [], frame(right="mid", top="mid", bottom="mid"))
g.put(IN_L, IN_R, 1, 2, [runs_of(title)], frame(top="mid"), ratio=100)
for row, (name, page, end) in enumerate(split, 3):
    g.put(IN_L, end, row, row + 1, name, align="LEFT", size=1480, ratio=100)
    g.put(end, PAGE_L, row, row + 1, [], frame(bottom="dot"))
    g.put(PAGE_L, IN_R, row, row + 1, page, align="RIGHT", size=1480, ratio=100)
g.put(IN_L, IN_R, last - 1, last, [], frame(bottom="mid"))
block(g, 226.0)

# "2025년도 경영실적보고서" under the box is inside the background image; typed here.
foot = Grid("cover-foot", [X0, BOX_L, BOX_R, X1], [2000])
foot.put(BOX_L, BOX_R, 0, 1, "2025년도 경영실적보고서", size=1400, ratio=100)
block(foot, 546.0)

kit.finish(target, end=566.0)
