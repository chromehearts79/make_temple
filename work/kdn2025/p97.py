"""Rebuild KDN 2025 report page 97 (PDF 2 local page 47, printed page 67) as editable HWPX.

Usage: python3 work/kdn2025/p97.py <report2.pdf> <out.hwpx> [--page 47]

안전 및 책임경영 계량 summary page: 지표명 / 가중치 / 평가방법 box, the contact table and the
"1 실적 개요" score table (가중치 6.9, results 미정). Built with the shared kit on the PDF's own
column and row rules (vector lines). Text comes from the PDF text layer; the labels 지표명, 가중치
and 평가방법 and the small chevron are images in the PDF and are typed. Letter-spaced cells
(직위, 성명, 지표명 groups) use Hancom's distributed alignment (배분 정렬) with the PDF's text
extents as cell padding, as in the 지표 정의 recipe p11.py.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kit  # noqa: E402
from kit import Layout, recipe_inputs  # noqa: E402

source, target = recipe_inputs(47, "부처평가결과")
L = Layout(top=3100)
kit.setup(source, L)
from kit import *  # noqa: E402,F401,F403  helpers and presets bound to this page

DARK, BAND = "#6A6A6A", "#E5E5E5"


def pad(g, x0, r0, left, right):
    """Set a cell's left / right padding (PDF pt) so distributed text spans the PDF's extent."""
    key = (r0, g.xs.index(to_x(x0)))
    g.items[key] = g.items[key][:7] + (dict(left=int(left * 100), right=int(right * 100), top=80, bottom=80),)


# ---------------------------------------------------------------------------
# Page chrome (odd page): running head over a rule, side tab, footer at the right.
# ---------------------------------------------------------------------------
L.add_table([[cell(0, 3350, 1680, [para([("01", 1380, True, WHITE)], "CENTER")[0]], dark)],
             [cell(0, 3350, 5960, [para([(ch, 950, True, INK)], "CENTER", 1160)[0] for ch in "경영관리"], gray2)]],
            floating=(57800, 15000))
foot = [(only_text, size, False, INK) for only_text, size in (
    (line1(450, 455, 818, 822)["text"], 790), ("    ", 790), (line1(540, 552, 816, 820)["text"], 1090))]
L.add_table([[cell(0, W, 1500, [para(foot, "RIGHT", 1300)[0]])]], floating=(5660, 81550))

g = Grid("head", [X0, 480.0, X1], [1680])
g.put(X0, 480.0, 0, 1, [], frame(bottom="soft"))
g.put(480.0, X1, 0, 1, [line1(480, 490, 35, 40)], align="RIGHT")
block(g, 32.0)

# ---------------------------------------------------------------------------
# 지표명 / 가중치 / 평가방법 box (labels are images in the PDF; typed)
# ---------------------------------------------------------------------------
xs = [X0, 103.0, 113.0, 405.0, 413.0, 474.0, 479.0, 551.7, X1]
g = Grid("indicator", xs, [580, 1160, 3340])
g.put(X0, 103.0, 0, 3, "지표명", frame(top="mid", left="mid", bottom="mid"), size=1090, bold=True)
g.put(103.0, 113.0, 0, 3, "▶", size=600, color="#9A9A9A", fit=False)
g.put(113.0, X1, 0, 1, [], frame(top="mid"))
g.put(113.0, 405.0, 1, 3, [line1(210, 215, 89, 94)], frame("#ECECEC", hatch="#DDDDDD"), bold=True, line=1700)
tab = frame(WHITE, top="mid", left="mid", right="mid", bottom="soft")
value = frame("#E5E5E5")
g.put(413.0, 474.0, 1, 2, "가중치", tab, size=1000, bold=True, line=1100)
g.put(413.0, 474.0, 2, 3, [line1(430, 435, 101, 105)], value)
g.put(479.0, 551.7, 1, 2, "평가방법", tab, size=1000, bold=True, line=1100)
g.put(479.0, 551.7, 2, 3, [line1(480, 485, 101, 105)], value)
block(g, 70.9)

# ---------------------------------------------------------------------------
# Contact table (columns and 18.4 pt rows from the PDF's vector rules)
# ---------------------------------------------------------------------------
cols = [X0, 184.3, 260.8, 374.2, X1]
g = Grid("contacts", cols, [1840] + [1842] * 8)
for k, (a, e) in enumerate(zip(cols, cols[1:])):
    g.put(a, e, 0, 1, [line1(a, e, 140, 144)], frame(top="strong", bottom="soft", left="soft" if k else None,
                                                   right="soft" if k < 3 else None), size=1040)
tops = [159.2, 177.7, 196.1, 214.5, 232.9, 251.3, 269.8, 288.2]
for r, y in enumerate(tops, 1):
    edge = "strong" if r == len(tops) else "soft"
    rank = "".join(l["text"] for l in lines_in(X0, 184.3, y - 1, y + 3))
    name = "".join(l["text"] for l in lines_in(184.3, 260.8, y - 1, y + 3))
    g.put(X0, 184.3, r, r + 1, rank, frame(bottom=edge, right="soft"), align="DISTRIBUTE", size=1090)
    pad(g, X0, r, 70.9 - X0, 184.3 - 170.1)
    g.put(184.3, 260.8, r, r + 1, name, frame("#EBEBEB", bottom=edge, right="soft"), align="DISTRIBUTE", size=1090)
    pad(g, 184.3, r, 198.4 - 184.3, 260.8 - 246.6)
    g.put(260.8, 374.2, r, r + 1, [line1(270, 300, y - 1, y + 3)], frame("#EBEBEB", bottom=edge, right="soft"))
    g.put(374.2, X1, r, r + 1, [line1(390, 440, y - 1, y + 3)], frame("#EBEBEB", bottom=edge))
block(g, 137.1)

# ---------------------------------------------------------------------------
# 1 실적 개요
# ---------------------------------------------------------------------------
g = Grid("sec1", [X0, 84.5, X1], [2300])
g.put(X0, 84.5, 0, 1, [runs_of(line1(60, 70, 329, 333), WHITE)], frame(DARK), line=1700)
g.put(84.5, X1, 0, 1, [line1(90, 95, 330, 334)], frame(BAND), align="LEFT", line=1700)
block(g, 327.0)

rules = [356.3, 374.7, 392.9, 411.0, 429.2, 447.3, 465.5, 483.6, 501.7, 519.9, 538.0, 556.1, 574.3, 592.4, 610.5,
         628.7, 646.8, 665.0, 683.1, 701.3, 719.4, 737.6, 755.7, 773.8]
hs = [int(round((b - a) * 100)) for a, b in zip(rules, rules[1:])]
cols = [X0, 121.9, 348.7, 405.4, 496.1, X1]
g = Grid("scores", cols, hs)
HEAD, LIGHT, SUB, TOTAL = "#D8D8D8", "#ECECEC", "#D8D8D8", "#CCCCCC"
heads = [line1(70, 80, 359, 363), line1(200, 210, 359, 363), line1(350, 360, 359, 363)]
both = line1(405, 410, 359, 363)
for k, (a, e, content) in enumerate(((X0, 121.9, [heads[0]]), (121.9, 348.7, [heads[1]]), (348.7, 405.4, [heads[2]]),
                                     (405.4, 496.1, [runs_of(both, x1=496.0)]),
                                     (496.1, X1, [runs_of(both, x0=496.0)]))):
    g.put(a, e, 0, 1, content, frame(HEAD, top="mid"))
groups = []          # (first row, last row) per 지표명 group, rows counted in `rules`
row = 1
for r in range(1, len(hs)):
    y = rules[r]
    if r == len(hs) - 1:       # 합계
        g.put(X0, 348.7, r, r + 1, [line1(185, 195, y + 2, y + 6)], frame(TOTAL, bottom="mid"))
        g.put(348.7, 405.4, r, r + 1, [line1(360, 370, y + 2, y + 6)], frame(TOTAL, bottom="mid"))
        g.put(405.4, 496.1, r, r + 1, [line1(440, 450, y + 2, y + 6)], frame(TOTAL, bottom="mid", left="soft"))
        g.put(496.1, X1, r, r + 1, [line1(520, 525, y + 2, y + 6)], frame(TOTAL, bottom="mid", left="soft"))
        continue
    sub = bool(lines_in(220, 230, y + 2, y + 6))
    edge = "soft"
    if sub:
        groups.append((row, r))
        row = r + 1
        g.put(121.9, 348.7, r, r + 1, [line1(220, 230, y + 2, y + 6)], frame(SUB, bottom=edge, left="soft"))
        fill = SUB
    else:
        g.put(121.9, 348.7, r, r + 1, [line1(125, 130, y + 2, y + 6)], frame(LIGHT, bottom=edge, left="soft"),
              align="LEFT")
        fill = WHITE
    g.put(348.7, 405.4, r, r + 1, [line1(360, 370, y + 2, y + 6)], frame(fill, bottom=edge))
    g.put(405.4, 496.1, r, r + 1, [line1(440, 450, y + 2, y + 6)], frame(fill, bottom=edge, left="soft"))
    g.put(496.1, X1, r, r + 1, [line1(515, 525, y + 2, y + 6)], frame(fill, bottom=edge, left="soft"))
for first, last in groups:
    labels = lines_in(60, 120, rules[first], rules[last + 1])
    g.put(X0, 121.9, first, last + 1, labels, frame(LIGHT, bottom="soft"), align="DISTRIBUTE", line=1430)
    pad(g, X0, first, 63.7 - X0, 121.9 - 114.9)
    item = g.items[first, 0]
    for k, l in enumerate(labels):       # a lone '및' between two distributed lines stays centred
        if len(l["text"]) == 1:
            item[3][k] = para(runs_of(l), "CENTER", 1430)[0]
block(g, 356.3)

g = Grid("notes", [X0, X1], [1400, 1400])
notes = lines_in(55, 75, 776, 796)
g.put(X0, X1, 0, 1, [notes[0]], align="LEFT", line=1150)
g.put(X0, X1, 1, 2, [[("     ", 990, False, INK)] + runs_of(notes[1])], align="LEFT", line=1150)
block(g, 776.5)

kit.finish(target, end=805.0)
