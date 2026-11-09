"""Rebuild KDN 2025 report physical PDF page 28 (printed page 16) as editable HWPX.

Usage: python3 work/kdn2025/p28.py <report.pdf> <out.hwpx> [--page N]

"3 AX･DX 혁신" diagram page, built with the shared kit (one flat table per horizontal band on
a grid of PDF x edges, text taken line by line from the PDF with its spans, 장평 fitted per
cell). Rounded boxes, chevrons and the gray gradients are images in the PDF and become cell
fills and borders; arrow and number images become KS X 1001 glyphs (→ ▶ ▼ ① ②); the Q / A
speech icons become the letters they show; the KDN logo in the footer is typed as text.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kit  # noqa: E402
from kit import Layout, recipe_inputs  # noqa: E402

source, target = recipe_inputs(28, "AI기반 패러다임 전환을 위한 AX")
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


# ---------------------------------------------------------------------------
# Page 28 (even page: PART box head, footer at the left)
# ---------------------------------------------------------------------------
foot = [(line1(55, 60, 815, 820)["text"], 1090, False, INK), ("    ", 1090, False, INK),
        ("한전KDN㈜", 1100, True, INK)]
L.add_table([[cell(0, W, 1500, [para(foot, "LEFT", 1300)[0]])]], floating=(5660, 81550))

# Running head: PART 01 | 경영관리 box (image in the PDF) over a rule.
g = Grid("head", [X0, 102.7, 158.0, X1], [1560])
g.put(X0, 102.7, 0, 1, [[("PART ", 780, False, INK), ("01", 1350, True, "#555555")]],
      frame("#F4F4F4", top="soft", left="soft", bottom="soft"), line=1380)
g.put(102.7, 158.0, 0, 1, "경영관리", frame("#333333", bottom="soft"), size=1080, bold=True, color=WHITE)
g.put(158.0, X1, 0, 1, [], frame(bottom="soft"))
block(g, 31.7)

section_band("band-3", "3", line1(95, 100, 74, 78), 70.9, 156.7)

# ---- 가. 혁신과제 1 -------------------------------------------------------------
task_heading("title-ga", line1(55, 60, 100, 103), line1(136, 140, 100, 103), [X0, 75.1, 138.2], 99.8, "①")

problem_box(
    "problem-ga", 122.7, (338.0, 353.0),
    (line1(170, 190, 125, 130), line1(410, 420, 125, 130)),
    [line1(60, 65, 145, 150),
     indent(R(line1(70, 75, 160, 165)) + [(" → ", 1090, False, INK)] + R(line1(140, 150, 160, 165)))],
    [line1(355, 360, 145, 150), indent(R(line1(365, 370, 160, 165)))])

# Q / A boxes (speech-bubble icons are images: typed as their letters).
g = Grid("qa", [X0, 95.0, 184.7, 187.1, 225.6, X1], [3570])
qa = dict(top="soft", bottom="strong")
g.put(X0, 95.0, 0, 1, "Q", frame(**qa, left="strong"), size=1500, bold=True, color="#3C3C3C")
g.put(95.0, 184.7, 0, 1, lines_in(100, 105, 185, 220), frame(**qa, right="strong"), align="LEFT", line=1500)
g.put(187.1, 225.6, 0, 1, "A", frame(**qa, left="strong"), size=1500, bold=True, color="#3C3C3C")
g.put(225.6, X1, 0, 1, lines_in(225, 235, 185, 220), frame(**qa, right="strong"), align="LEFT", line=1500)
block(g, 185.5)

# 사업역량혁신: three stage columns (ISP → services → two ministries).
xs = [X0, 80.5, 234.5, 249.4, 395.1, 410.0, X1]
g = Grid("stages", xs, [1870, 1650, 1640, 1680, 1640, 1680, 2150])
g.put(X0, 80.5, 0, 7, lines_in(60, 75, 245, 335), frame(LABEL), bold=True, line=1320)
heads = [line1(115, 120, 228, 235), line1(260, 265, 228, 235), line1(425, 430, 228, 235)]
for (a, e), head, num, fill in zip(((80.5, 234.5), (249.4, 395.1), (410.0, X1)), heads, "①②③",
                                   ("#EBEBEB", "#EBEBEB", "#D2D2D2")):
    g.put(a, e, 0, 1, [lead(num, R(head))], frame(fill))
for a, e in ((234.5, 249.4), (395.1, 410.0)):
    g.put(a, e, 0, 1, "▶", size=900, color="#9A9A9A")
g.put(80.5, 234.5, 1, 3, lines_in(84, 90, 255, 295), align="LEFT", line=1550)
col1 = lines_in(90, 95, 300, 335)
g.put(80.5, 234.5, 3, 7, [lead("→", R(col1[0])), indent(R(col1[1]))], HATCH, align="LEFT", line=1500)
col2 = lines_in(236, 260, 247, 345)
for r, (item, num) in enumerate(zip(col2, "①x②x③x")):
    if r % 2 == 0:
        g.put(234.5, 395.1, 1 + r, 2 + r, [lead(num, R(item))], frame(left="soft"), align="LEFT", line=1300)
    else:
        runs = R(item)
        g.put(234.5, 395.1, 1 + r, 2 + r, [lead("→", runs) if r == 5 else runs],
              frame("#EEEEEE", left="soft", hatch="#DEDEDE"), align="LEFT", line=1300)
col3 = lines_in(410, 415, 255, 340)
g.put(395.1, X1, 1, 7, [lead(n, R(l)) for n, l in zip("①②③④", col3[:4])] + [indent(R(col3[4]))],
      frame(left="soft"), align="LEFT", line=1700)
block(g, 227.5)

results_box("results-ga", 356.6, line1(60, 70, 373, 380),
            [l if i < 2 else indent(R(l)) for i, l in enumerate(lines_in(115, 130, 358, 395))], 4870)

# ---- 나. 혁신과제 2 -------------------------------------------------------------
task_heading("title-na", line1(55, 60, 416, 420), line1(138, 142, 416, 420), [X0, 76.9, 140.1], 416.4, "②")

problem_box(
    "problem-na", 439.2, (338.0, 353.0),
    (line1(170, 190, 441, 446), line1(410, 420, 441, 446)),
    [line1(60, 65, 460, 465), indent(R(line1(68, 75, 475, 480)))],
    [line1(355, 360, 460, 465), indent(R(line1(365, 370, 475, 480)))], hs=(1900, 3640))

# 혁신노력: three panels; the first holds two dark certificate boxes joined by '+'.
xs = [X0, 89.6, 96.1, 209.9, 215.6, 229.5, 392.6, X1]
g = Grid("effort", xs, [2150, 2420, 1070, 2420, 350, 1680, 1160])
g.put(X0, 89.6, 0, 5, lines_in(60, 65, 528, 557), frame(LABEL), bold=True, line=1320)
panel_head = frame(HEAD_GRAY, top="mid", left="mid", right="mid", bottom="soft")
for (a, e), x in (((89.6, 215.6), 130), ((229.5, 392.6), 248), ((392.6, X1), 425)):
    g.put(a, e, 0, 1, [line1(x, x + 5, 503, 508)], panel_head)
g.put(89.6, 96.1, 1, 5, [], frame(left="mid", bottom="mid"))
g.put(209.9, 215.6, 1, 5, [], frame(right="mid", bottom="mid"))
box = frame("#6E6E6E")
g.put(96.1, 209.9, 1, 2, [recolor(R(l), WHITE) for l in lines_in(105, 120, 522, 548)], box, line=1120)
g.put(96.1, 209.9, 2, 3, "+", size=1100, bold=True, color="#8C8C8C", line=900)
g.put(96.1, 209.9, 3, 4, [recolor(R(l), WHITE) for l in lines_in(114, 125, 556, 582)], box, line=1120)
g.put(96.1, 209.9, 4, 5, [], frame(bottom="mid"))
g.put(215.6, 229.5, 0, 5, "+", size=1500, bold=True, color="#9A9A9A", fit=False)
g.put(229.5, 392.6, 1, 5, lines_in(233, 240, 528, 576), frame(left="mid", right="mid", bottom="mid"),
      align="LEFT", line=1500)
p3 = lines_in(398, 410, 528, 576)
g.put(392.6, X1, 1, 5, [p3[0], p3[1], indent(R(p3[2]))], frame(left="mid", right="mid", bottom="mid"),
      align="LEFT", line=1500)
g.put(X0, X1, 5, 6, [line1(110, 115, 585, 590)], line=1300)
g.put(X0, X1, 6, 7, "▼", frame("#EFEFEF"), size=900, color="#9A9A9A", line=1000)
block(g, 500.9)

# 구축 ('25년上) ▶ 적용 ('25년下)
xs = [X0, 101.6, 306.5, 315.5, 358.7, X1]
g = Grid("build-apply", xs, [3600])
lab1 = lines_in(64, 70, 620, 647)
g.put(X0, 101.6, 0, 1, [lab1[0], R(lab1[1])], frame(top="mid", bottom="mid", left="mid"), line=1250)
g.put(101.6, 306.5, 0, 1, lines_in(104, 108, 620, 650), frame("#EDEDED", top="mid", bottom="mid", right="mid"),
      align="LEFT", line=1420)
g.put(306.5, 315.5, 0, 1, "▶", size=900, color="#9A9A9A", fit=False)
lab2 = lines_in(320, 330, 620, 647)
g.put(315.5, 358.7, 0, 1, [lab2[0], R(lab2[1])], frame(top="mid", bottom="mid", left="mid"), line=1250)
g.put(358.7, X1, 0, 1, lines_in(360, 365, 620, 650), frame(top="mid", bottom="mid", right="mid"),
      align="LEFT", line=1420)
block(g, 616.5)

# 사업역량혁신 → 실적: three numbered columns.
xs = [X0, 89.6, 245.3, 401.2, X1]
g = Grid("business", xs, [1840, 1840, 3150, 1000, 2140])
g.put(X0, 89.6, 0, 3, lines_in(60, 65, 672, 715), frame(LABEL), bold=True, line=1320)
g.put(X0, 89.6, 4, 5, [line1(60, 65, 739, 745)], frame(LABEL), bold=True)
cols = ((89.6, 245.3, 115, 100, 92, 105), (245.3, 401.2, 276, 265, 248, 260), (401.2, X1, 433, 413, 404, 410))
for (a, e, hx, sx, bx, rx), num in zip(cols, "①②③"):
    g.put(a, e, 0, 1, [lead(num, recolor(R(line1(hx, hx + 3, 660, 665)), WHITE))], frame("#7A7A7A", left="soft"))
    g.put(a, e, 1, 2, [line1(sx, sx + 3, 679, 684)], frame(left="soft"))
    bullets = [R(l) for l in lines_in(bx, bx + 3, 697, 727)]
    if bx == 92:   # '수기 입력 ➡ 시스템 자동 연계' : arrow image between the words
        bullets[0] = [(t.replace("입력  시스템", "입력 → 시스템"), s, b, c) for t, s, b, c in bullets[0]]
    g.put(a, e, 2, 3, bullets, HATCH, align="LEFT", line=1420)
    g.put(a, e, 3, 4, "▼", size=700, color="#B0B0B0", line=760)
    g.put(a, e, 4, 5, [line1(rx, rx + 5, 738, 745)], frame("#E6E6E6", left="soft"))
block(g, 658.8)

results_box("results-na", 764.4, line1(60, 70, 775, 780), lines_in(115, 120, 765, 800), 3720, line=1500)

kit.finish(target, end=803.0)
