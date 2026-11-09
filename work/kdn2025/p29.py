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


def chip_split(line, split):
    """One PDF line that starts with an inline chip: (chip runs, text runs)."""
    return strip_runs(R(line, x1=split)), strip_runs(R(line, x0=split))


CHIP_WHITE = frame(WHITE, top="soft", bottom="soft", left="soft", right="soft")
MAP = "#EDEDED"

# ---------------------------------------------------------------------------
# Page 29 (odd page: running head at the right, side tab, footer at the right)
# ---------------------------------------------------------------------------
L.add_table([[cell(0, 3350, 1680, [para([("01", 1380, True, WHITE)], "CENTER")[0]], dark)],
             [cell(0, 3350, 5960, [para([(ch, 950, True, INK)], "CENTER", 1160)[0] for ch in "경영관리"], gray2)]],
            floating=(57800, 15000))
foot = [(only_text, size, False, INK) for only_text, size in (
    (line1(450, 455, 818, 822)["text"], 790), ("    ", 790), (line1(540, 545, 816, 820)["text"], 1090))]
L.add_table([[cell(0, W, 1500, [para(foot, "RIGHT", 1300)[0]])]], floating=(5660, 81550))

g = Grid("head", [X0, 466.3, X1], [1680])
g.put(X0, 466.3, 0, 1, [], frame(bottom="soft"))
g.put(466.3, X1, 0, 1, [line1(465, 480, 35, 40)], align="RIGHT")
block(g, 32.0)

section_band("band-4", "4", line1(95, 100, 74, 78), 70.9, 170.8)

# ---- 가. 혁신과제 3 -------------------------------------------------------------
task_heading("title-ga", line1(55, 60, 100, 103), line1(138, 142, 100, 103), [X0, 76.9, 140.1], 99.8, "③")

problem_box(
    "problem-ga", 122.7, (332.0, 348.7),
    (line1(170, 180, 125, 130), line1(405, 415, 125, 130)),
    lines_in(60, 65, 143, 175),
    [line1(350, 355, 143, 150), indent(R(line1(358, 365, 158, 165)))], hs=(1900, 3470))

# 개선점 도출: hydrogen-city map (image; labels read from a 5x render) | issues ▼ improvements.
xs = [X0, 82.0, 110.5, 129.6, 148.8, 168.0, 175.0, 212.0, 247.0, 262.5, 294.0, 409.8, 441.0, X1]
g = Grid("improve", xs, [2260, 1730, 1730, 810, 1700, 2030])
g.put(X0, 82.0, 0, 6, lines_in(62, 66, 200, 270), frame(LABEL), bold=True, line=1320)
map_head = frame("#5A5A5A")
g.put(82.0, 168.0, 0, 1, [[("수소시범도시", 800, True, WHITE), ("(’20~’23)", 620, False, WHITE)]], map_head, line=950)
g.put(175.0, 262.5, 0, 1, [[("통합모델구축", 800, True, WHITE), ("(’24~’27)", 620, False, WHITE)]], map_head, line=950)
g.put(82.0, 168.0, 1, 4, ["안산", "전주･완주"], frame(MAP), size=820, line=1500)
g.put(168.0, 175.0, 0, 6, "▶", size=800, color="#BDBDBD", fit=False)
g.put(175.0, 212.0, 1, 4, [[("NEW ", 620, True, INK), ("당진", 820, False, INK)],
                           [("NEW ", 620, True, INK), ("부안", 820, False, INK)]], frame(MAP), line=1500)
g.put(212.0, 262.5, 1, 4, ["안산", "보령", "전주･완주", "광역센터"], frame(MAP), size=820, line=950)
box = dict(top="soft", bottom="soft")
g.put(82.0, 110.5, 4, 6, ["수소", "전주기", "관리"], frame("#D0D0D0", **box, left="soft"), size=760, line=850)
for (a, e), word in zip(((110.5, 129.6), (129.6, 148.8), (148.8, 168.0)), ("생산", "유통", "소비")):
    g.put(a, e, 4, 6, word, frame(WHITE, **box, right="soft" if word == "소비" else None), size=820)
g.put(175.0, 212.0, 4, 6, ["광역", "통합모델"], frame("#D0D0D0", **box, left="soft"), size=760, line=900)
g.put(212.0, 247.0, 4, 6, "데이터 통합", frame(WHITE, **box), size=780)
g.put(247.0, 262.5, 4, 6, "AI", frame(WHITE, **box, right="soft"), size=820)
g.put(262.5, X1, 0, 1, [line1(270, 280, 186, 192)], frame(top="soft"), line=1300)
issue = frame("#F0F0F0")
better = frame("#E4E4E4")
for (a, s, e), (cx, tx), split in (((262.5, 294.0, 409.8), (270, 265), 294.0), ((409.8, 441.0, X1), (418, 412), 441.0)):
    chip, text = chip_split(line1(cx, cx + 5, 207, 212), split)
    g.put(a, s, 1, 2, [chip], frame(WHITE, top="soft", bottom="soft", left="soft", right="soft"), line=1050)
    g.put(s, e, 1, 2, [text], issue, align="LEFT", line=1300)
    g.put(a, e, 2, 3, [line1(tx, tx + 4, 223, 228)], issue, align="LEFT", line=1300)
    g.put(a, e, 3, 4, "▼", size=600, color="#9A9A9A", line=650)
    chip, text = chip_split(line1(cx - 2, cx + 3, 250, 255), split)
    g.put(a, s, 4, 5, [recolor(chip, WHITE)], frame("#808080"), line=1050)
    g.put(s, e, 4, 5, [text], better, align="LEFT", line=1300)
    g.put(a, e, 5, 6, [line1(tx, tx + 4, 264, 270)], better, align="LEFT", line=1300)
block(g, 182.7)

# 사업역량혁신 / 추진실적: two columns of three sub-blocks (chip + title, bullets, → result).
xs = [X0, 82.0, 121.9, 266.0, 303.2, 317.5, 321.7, 359.9, 515.7, X1]
g = Grid("business-ga", xs, [1840, 1980, 3260, 2120, 1980, 3260, 2110, 2000, 3690])
g.put(X0, 82.0, 0, 7, lines_in(62, 66, 335, 415), frame(LABEL), bold=True, line=1320)
g.put(X0, 82.0, 7, 9, lines_in(62, 66, 465, 512), frame(LABEL), bold=True, line=1050)
g.put(82.0, 317.5, 0, 1, [line1(115, 125, 290, 295)], frame("#CCCCCC", top="soft"))
g.put(321.7, X1, 0, 1, [recolor(R(line1(350, 355, 290, 295)), WHITE)], frame("#7A7A7A", top="soft"))
sub_chip = frame("#CCCCCC", bottom="soft")
sub_text = frame(bottom="soft")
# Sub-block 1 carries a second chip at the right (국내최초 / 특허출원).
for (a, b, c, e), (cx, tx), split in (((82.0, 121.9, 266.0, 317.5), (85, 130), 266.0),
                                      ((321.7, 359.9, 515.7, X1), (325, 370), 516.0)):
    g.put(a, b, 1, 2, [line1(cx, cx + 5, 310, 315)], sub_chip, bold=True)
    text, chip = chip_split(line1(tx, tx + 6, 310, 315), split)
    g.put(b, c, 1, 2, [text], sub_text, align="LEFT")
    g.put(c, 303.2 if a < 300 else X1, 1, 2, [chip], CHIP_WHITE, line=1050)
    if a < 300:
        g.put(303.2, 317.5, 1, 2, [], sub_text)
for (a, e), (bx, rx) in (((82.0, 317.5), (85, 95)), ((321.7, X1), (323, 333))):
    g.put(a, e, 2, 3, lines_in(bx, bx + 4, 330, 358), frame("#EDEDED"), align="LEFT", line=1400)
    g.put(a, e, 3, 4, [lead("→", R(line1(rx, rx + 5, 360, 365)))], align="LEFT")
    g.put(a, e, 5, 6, lines_in(bx, bx + 4, 403, 432), frame("#EDEDED"), align="LEFT", line=1400)
    g.put(a, e, 6, 7, [lead("→", R(line1(rx, rx + 5, 434, 438)))], align="LEFT")
for (a, b, e), (cx, tx) in (((82.0, 121.9, 317.5), (85, 130)), ((321.7, 359.9, X1), (325, 370))):
    g.put(a, b, 4, 5, [line1(cx, cx + 5, 384, 388)], sub_chip, bold=True)
    g.put(b, e, 4, 5, [line1(tx, tx + 6, 383, 388)], sub_text, align="LEFT")
    g.put(a, b, 7, 8, [recolor(R(line1(cx - 2, cx + 3, 457, 461)), WHITE)], frame("#6E6E6E", bottom="soft"))
    g.put(b, e, 7, 8, [line1(tx, tx + 6, 457, 461)], sub_text, align="LEFT")
growth = R(line1(85, 90, 476, 480)) + [(" ↑ ", 1090, True, "#8C8C8C")] + R(line1(214, 218, 480, 484))
g.put(82.0, 317.5, 8, 9, [growth, line1(85, 90, 492, 496)], frame("#E2E2E2"), align="LEFT", line=1500)
g.put(321.7, X1, 8, 9, lines_in(323, 327, 479, 507), frame("#E2E2E2"), align="LEFT", line=1500)
block(g, 288.5)

results_box("results-ga", 516.7, line1(60, 70, 528, 533), lines_in(115, 120, 520, 540), 3710, line=1500)

# ---- 나. 혁신과제 4 -------------------------------------------------------------
task_heading("title-na", line1(55, 60, 566, 570), line1(138, 142, 566, 570), [X0, 76.9, 140.1], 564.9, "④")

problem_box(
    "problem-na", 587.7, (332.0, 348.7),
    (line1(170, 180, 590, 595), line1(405, 415, 590, 595)),
    lines_in(60, 65, 608, 640),
    [line1(350, 355, 608, 615), indent(R(line1(358, 365, 622, 628)))], hs=(1880, 3370))

xs = [X0, 82.0, 119.5, 162.2, 200.5, 317.5, 321.7, 386.7, 429.4, X1]
g = Grid("business-na", xs, [1800, 1950, 1670, 3330, 760, 3210])
g.put(X0, 82.0, 0, 4, lines_in(58, 62, 670, 715), frame(LABEL), bold=True, line=1320)
g.put(X0, 82.0, 4, 6, lines_in(58, 62, 745, 775), frame(LABEL), bold=True, line=1250)
head = frame("#D2D2D2", top="soft")
for (a, b, c, e), x, split in (((82.0, 119.5, 162.2, 317.5), 122, 160.0), ((321.7, 386.7, 429.4, X1), 390, 427.0)):
    chip, text = chip_split(line1(x, x + 5, 648, 652), split)
    g.put(a, b, 0, 1, [], head)
    g.put(b, c, 0, 1, [chip], frame(WHITE, top="soft", bottom="soft", left="soft", right="soft"), line=1050)
    g.put(c, e, 0, 1, [text], head, align="LEFT")
company = frame("#E6E6E6", hatch="#D8D8D8")
g.put(82.0, 200.5, 1, 2, [line1(120, 125, 669, 673)], company)
g.put(200.5, 317.5, 1, 2, [line1(228, 233, 669, 673)], company)
g.put(82.0, 200.5, 2, 3, [line1(93, 97, 685, 690)], frame(bottom="soft"))
g.put(200.5, 317.5, 2, 3, [line1(206, 210, 685, 690)], frame(bottom="soft"))
g.put(82.0, 317.5, 3, 4, lines_in(85, 90, 703, 732), align="LEFT", line=1430)
g.put(321.7, X1, 1, 4, lines_in(323, 327, 673, 728), align="LEFT", line=1960)
result = frame("#E2E2E2")
for (a, e), (x0, x1) in (((82.0, 317.5), (130, 136)), ((321.7, X1), (345, 395))):
    g.put(a, e, 4, 5, "▼", size=600, color="#9A9A9A", line=600)
    g.put(a, e, 5, 6, lines_in(x0, x1, 742, 770), result, line=1320)
block(g, 646.5)

results_box("results-na", 779.4, line1(60, 70, 785, 790), [line1(115, 120, 785, 790)], 2300, line=1350)

kit.finish(target, end=803.0)
