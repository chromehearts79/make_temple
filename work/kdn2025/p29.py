"""Rebuild KDN 2025 report physical PDF page 29 (printed page 17) as editable HWPX.

Usage: python3 work/kdn2025/p29.py <report.pdf> <out.hwpx> [--page N]

"4 에너지전환 혁신" diagram page, built with the shared kit (one flat table per horizontal band
on a grid of PDF x edges, text taken line by line from the PDF with its spans, 장평 fitted per
cell). Rounded boxes, chevrons and gray gradients are drawings/images in the PDF and become
cell fills and borders; arrow images become KS X 1001 glyphs (→ ▶ ▼ ↑ ①). The hydrogen-city map
(an image) becomes a small table of the labels it shows, read from a 5x render; pins, the map
outline, the process icons and the handshake icon are omitted. The side tab is typed as in p19.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kit  # noqa: E402
from kit import Layout, recipe_inputs  # noqa: E402

source, target = recipe_inputs(29, "탄소중립 실현 및 수익기반 다변화를 위한 에너지전환 혁신")
L = Layout(top=3100)
kit.setup(source, L)
from kit import *  # noqa: E402,F401,F403  helpers and presets bound to this page

# ---------------------------------------------------------------------------
# Page-specific helpers and fills
# ---------------------------------------------------------------------------
HEAD_GRAY = "#D9D9D9"   # 문제인식 / column headers
HEAD_DARK = "#6B6B6B"   # 혁신 아이디어 탐색, 주요성과 label
LABEL = "#E3E3E3"        # vertical side labels (사업역량혁신 ...)
HATCH = frame("#EEEEEE", hatch="#DEDEDE")


def R(line, **kw):
    return runs_of(line, **kw)


def indent(runs):
    """Continuation line under a bullet: indented like the source."""
    runs = list(runs)
    return [("  ", runs[0][1], runs[0][2], runs[0][3])] + runs


def lead(glyph, runs, size=None):
    """Prefix a typed glyph (image in the PDF) to a line, same weight as the line."""
    runs = list(runs)
    return [(glyph + " ", size or runs[0][1], runs[0][2], runs[0][3])] + runs


def recolor(runs, color):
    return [(t, s, b, color) for t, s, b, _ in runs]


def section_band(name, number, line, top, pill_end):
    """'3 [badge] title' band: dark number box, dark pill badge (spans under 13 pt), gray title band."""
    runs = R(line)
    badge = [r for r in runs if r[1] < 1300]
    g = Grid(name, [X0, 83.3, 91.0, pill_end, X1], [2300])
    g.put(X0, 83.3, 0, 1, number, frame("#5E5E5E"), size=1700, bold=True, color=WHITE, line=1900)
    band = frame("#E4E4E4")
    g.put(83.3, 91.0, 0, 1, [], band)
    g.put(91.0, pill_end, 0, 1, [recolor(strip_runs(badge), WHITE)], frame("#5E5E5E"))
    g.put(pill_end, X1, 0, 1, [strip_runs(runs[len(badge):])], band, align="LEFT", line=1750)
    block(g, top)


def task_heading(name, head, title, edges, top, mark):
    """'가. [혁신과제 ①] title' : number, light pill badge with the typed number, 14pt title."""
    runs = R(head)
    g = Grid(name, edges + [X1], [1650])
    g.put(edges[0], edges[1], 0, 1, [strip_runs(runs[:1])], align="LEFT", line=1450)
    g.put(edges[1], edges[2], 0, 1, [strip_runs(runs[1:]) + [(" " + mark, 1090, True, INK)]], pill)
    g.put(edges[2], X1, 0, 1, [R(title)], align="LEFT", line=1450)
    block(g, top)


def problem_box(name, top, split, heads, left, right, hs=(1900, 3750)):
    """문제인식 (gray head) ▶ 혁신 아이디어 탐색 (dark head) pair of rounded boxes."""
    a, b = split
    g = Grid(name, [X0, a, b, X1], list(hs))
    g.put(X0, a, 0, 1, [heads[0]], frame(HEAD_GRAY, top="mid", left="mid", right="mid", bottom="soft"), line=1250)
    g.put(b, X1, 0, 1, [recolor(R(heads[1]), WHITE)], frame(HEAD_DARK, top="mid", left="mid", right="mid"),
          line=1250)
    g.put(X0, a, 1, 2, left, frame(left="mid", right="mid", bottom="mid"), align="LEFT", line=1600)
    g.put(a, b, 1, 2, "▶", size=1300, color="#BDBDBD", fit=False)
    g.put(b, X1, 1, 2, right, frame(left="mid", right="mid", bottom="mid"), align="LEFT", line=1600)
    block(g, top)


def results_box(name, top, label, lines, height, line=1450):
    """주요성과: dark label and an outlined bold text cell."""
    g = Grid(name, [X0, 112.0, X1], [height])
    g.put(X0, 112.0, 0, 1, [recolor(R(label), WHITE)], frame(HEAD_DARK, top="mid", left="mid", bottom="mid"))
    g.put(112.0, X1, 0, 1, lines, frame(top="mid", right="mid", bottom="mid", left="soft"), align="LEFT", line=line)
    block(g, top)


