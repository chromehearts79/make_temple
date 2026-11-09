"""Rebuild KDN 2025 report page 53 (second PDF local page 3, printed page 33) as editable HWPX.

Usage: python3 work/kdn2025/p53.py <report2.pdf> <out.hwpx> [--page 3]

일자리 및 균등한 기회 평가내용 02, sections 3 and 4 (odd page). Built with the shared diagram kit
(one flat table per horizontal band on a grid of PDF x edges); all running text comes from the PDF
text layer. Images: the boxed card numbers 1-4 (typed ① ② ③ ④), the small chevrons inside the
cards and the down-pointing 성장단계 labels (typed ▼ / plain gray label cells), the two photos of
the 기업탐방 프로그램 (empty photo cells), the side tab and the section number bands.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kit  # noqa: E402
from kit import Layout, recipe_inputs  # noqa: E402

source, target = recipe_inputs(3, "중소･협력기업 및 지역인재 성장 지원을 통한 민간 일자리 창출")
L = Layout(top=3100)
kit.setup(source, L)
from kit import *  # noqa: E402,F401,F403  helpers and presets bound to this page

DARK, LABEL = "#6A6A6A", "#E6E6E6"
HEAD = "#DADADA"
BOX = dict(top="soft", bottom="soft", left="soft", right="soft")
TIGHT = dict(left=0, right=0)


def hang(lines, base):
    """Bullet lines keep their PDF indent: spaces for the x offset and for the line's own lead."""
    out = []
    for l in lines:
        runs = runs_of(l)
        size = runs[0][1] / 100
        raw = "".join(s["text"] for s in l["spans"])
        offset = l["bbox"][0] - base + (len(raw) - len(raw.lstrip(" "))) * 0.29 * size
        n = max(0, round(offset / (0.29 * size)))
        out.append([(" " * n, runs[0][1], False, INK)] + runs if n else runs)
    return out


def tight(g, x0, r0):
    """No side padding for a narrow tag cell (실적 / 중점), or its two syllables wrap."""
    key = (r0, g.xs.index(to_x(x0)))
    g.items[key] = g.items[key][:7] + (TIGHT,)


def section_band(name, num_line, title_line, top):
    g = Grid(name, [X0, 84.5, X1], [2300])
    g.put(X0, 84.5, 0, 1, [runs_of(num_line, WHITE)], frame(DARK), line=1700)
    g.put(84.5, X1, 0, 1, [runs_of(title_line)], frame(LABEL), align="LEFT", line=1700)
    block(g, top)


def heading(name, line, top):
    g = Grid(name, [X0, X1], [1650])
    g.put(X0, X1, 0, 1, [line], align="LEFT", line=1450)
    block(g, top)


class Rows:
    """Row edges given as PDF y values; r(y) is the row index starting at y."""

    def __init__(self, ys):
        self.ys = sorted(set(ys))
        self.hs = [int(round((b - a) * 100)) for a, b in zip(self.ys, self.ys[1:])]

    def __call__(self, y):
        return self.ys.index(y)


# ---------------------------------------------------------------------------
# Page chrome (odd page): running head over a rule, side tab, footer at the right.
# ---------------------------------------------------------------------------
L.add_table([[cell(0, 3350, 1680, [para([("01", 1380, True, WHITE)], "CENTER")[0]], dark)],
             [cell(0, 3350, 5960, [para([(ch, 950, True, INK)], "CENTER", 1160)[0] for ch in "경영관리"], gray2)]],
            floating=(57800, 15000))
foot = [(only_text, size, False, INK) for only_text, size in (
    (line1(450, 455, 818, 822)["text"], 790), ("    ", 790), (line1(540, 552, 816, 820)["text"], 1090))]
L.add_table([[cell(0, W, 1500, [para(foot, "RIGHT", 1300)[0]])]], floating=(5660, 81550))

g = Grid("head", [X0, 378.5, X1], [1680])
g.put(X0, 378.5, 0, 1, [], frame(bottom="soft"))
g.put(378.5, X1, 0, 1, [line1(380, 385, 35, 40)], align="RIGHT")
block(g, 32.0)

# ---------------------------------------------------------------------------
# 3. 중소·협력기업 및 지역인재 성장 지원: 가. four cards (text layer, tabs and numbers drawn)
# ---------------------------------------------------------------------------
section_band("sec3", line1(60, 70, 72, 76), line1(90, 95, 73, 77), 70.9)
heading("title-ga", line1(55, 60, 99, 103), 98.6)

g = Grid("background", [X0, 109.6, 113.6, X1], [2330])
g.put(X0, 109.6, 0, 1, [line1(70, 75, 124, 128)], frame(HEAD, top="mid"))
g.put(113.6, X1, 0, 1, [line1(118, 122, 124, 128)], frame(**BOX), align="LEFT")
block(g, 119.8)

xs = [X0, 126.7, 305.5, 308.2, 378.3, X1]
CARDS = (((X0, 126.7, 305.5), 62.5, 64.0), ((308.2, 378.3, X1), 314.1, 315.5))


def cards(name, top, ys, marks, tab_y, bullet_y, result_y):
    """Two cards: dark tab with typed number | light title; bullets; ▼; gray result lines."""
    t0, t1, b1, c1, r1, end = ys
    R = Rows(ys)
    g = Grid(name, xs, R.hs)
    for ((a, b, e), bx, rx), mark in zip(CARDS, marks):
        tab = line1(bx + 10, b, tab_y, tab_y + 4)
        g.put(a, b, R(t0), R(t1), [[(mark + " ", 1090, True, WHITE)] + runs_of(tab, WHITE)], frame("#5A5A5A"),
              align="LEFT")
        g.put(b, e, R(t0), R(t1), [line1(b, e, tab_y - 2, tab_y + 3)], frame("#E3E3E3"))
        g.put(a, e, R(t1), R(b1), lines_in(bx - 1, bx + 3, bullet_y[0], bullet_y[1]),
              frame(left="soft", right="soft"), align="LEFT", line=1430)
        g.put(a, e, R(b1), R(c1), "▼", frame(left="soft", right="soft"), size=560, color="#9A9A9A", line=440)
        g.put(a, e, R(c1), R(r1), hang(lines_in(rx - 1, rx + 30, result_y[0], result_y[1]), rx),
              frame("#E6E6E6", left="soft", right="soft"), align="LEFT", line=1440)
        g.put(a, e, R(r1), R(end), [], frame(left="soft", right="soft", bottom="soft"))
    block(g, top)


cards("cards-1", 146.9, [146.9, 165.6, 196.0, 202.1, 233.6, 236.4], "①②", 151, (166, 195), (203, 232))
cards("cards-2", 240.4, [240.4, 259.2, 289.5, 295.7, 327.1, 330.0], "③④", 244.5, (260, 289), (296, 326))

# ---------------------------------------------------------------------------
# 나. 지역인재 성장단계별 맞춤형 지원: 성장단계 | 지원내용 | 지원실적 (+ two photos)
# ---------------------------------------------------------------------------
heading("title-na", line1(55, 60, 337, 341), 336.8)

xs = [X0, 82.7, 101.5, 127.0, 131.0, 385.0, 393.3, 468.5, 470.5, 547.1, X1]
R = Rows([360.8, 377.0, 424.6, 471.5, 485.5, 500.5, 503.0, 516.5, 519.5, 530.0, 562.5, 570.0, 603.0])
g = Grid("stages", xs, R.hs)
g.put(X0, 127.0, R(360.8), R(377.0), [line1(70, 75, 361, 365)], frame(HEAD, top="soft", left="soft", right="soft"),
      bold=True)
g.put(131.0, 385.0, R(360.8), R(377.0), [line1(235, 240, 361, 365)], frame(HEAD, top="soft", left="soft"), bold=True)
g.put(385.0, X1, R(360.8), R(377.0), [line1(450, 455, 361, 365)], frame(HEAD, top="soft", left="dot", right="soft"),
      bold=True)
stage = "#E3E3E3"
side = dict(left="soft", right="soft")
g.put(X0, 127.0, R(377.0), R(424.6), lines_in(60, 120, 385, 405), frame(stage, bottom="mid", **side))
g.put(X0, 127.0, R(424.6), R(471.5), [], frame(stage, **side))
g.put(X0, 82.7, R(471.5), R(485.5), [], frame(stage, left="soft"))
g.put(82.7, 101.5, R(471.5), R(485.5), [line1(84, 86, 473, 476)], frame(WHITE, **BOX), bold=True)
tight(g, 82.7, R(471.5))
g.put(101.5, 127.0, R(471.5), R(485.5), [], frame(stage, right="soft"))
g.put(X0, 127.0, R(485.5), R(530.0), lines_in(60, 120, 486, 520), frame(stage, **side), line=1430)
g.put(X0, 127.0, R(530.0), R(570.0), [], frame(stage, bottom="mid", **side))
g.put(X0, 127.0, R(570.0), R(603.0), [line1(60, 70, 583, 587)], frame(stage, bottom="soft", **side))
body = dict(left="soft", bottom="dot")
g.put(131.0, 385.0, R(377.0), R(424.6), lines_in(135, 140, 380, 410), frame(**body), align="LEFT", line=1320)
g.put(385.0, X1, R(377.0), R(424.6), lines_in(388, 392, 380, 410), frame(left="dot", right="soft", bottom="dot"),
      align="LEFT", line=1320)
shade = "#EBEBEB"
g.put(131.0, 385.0, R(424.6), R(570.0), hang(lines_in(135, 140, 427, 556), 136.2), frame(shade, **body),
      align="LEFT", line=1380)
g.put(385.0, X1, R(424.6), R(500.5), lines_in(388, 392, 426, 490), frame(shade, left="dot", right="soft"),
      align="LEFT", line=1430)
g.put(385.0, 393.3, R(500.5), R(570.0), [], frame(shade, left="dot"))
g.put(393.3, 547.1, R(500.5), R(503.0), [], frame(shade))
g.put(393.3, 547.1, R(503.0), R(516.5), [line1(400, 410, 503, 507)], frame(WHITE, **BOX), line=1150)
g.put(393.3, 547.1, R(516.5), R(519.5), [], frame(shade))
g.put(393.3, 468.5, R(519.5), R(562.5), [], photo)
g.put(468.5, 470.5, R(519.5), R(562.5), [], frame(shade))
g.put(470.5, 547.1, R(519.5), R(562.5), [], photo)
g.put(393.3, 547.1, R(562.5), R(570.0), [], frame(shade))
g.put(547.1, X1, R(500.5), R(570.0), [], frame(shade, right="soft"))
g.put(131.0, 385.0, R(570.0), R(603.0), hang(lines_in(135, 145, 572, 592), 136.2),
      frame(left="soft", bottom="soft"), align="LEFT", line=1440)
g.put(385.0, X1, R(570.0), R(603.0), hang(lines_in(388, 400, 572, 592), 389.9),
      frame(left="dot", right="soft", bottom="soft"), align="LEFT", line=1440)
block(g, 360.8)

g = Grid("progress", [X0, 111.7, 115.0, X1], [1860])
g.put(X0, 111.7, 0, 1, [line1(65, 70, 613, 617)], frame(HEAD, top="mid"))
g.put(115.0, X1, 0, 1, [line1(116, 120, 613, 617)], frame(**BOX), align="LEFT")
block(g, 610.8)

# ---------------------------------------------------------------------------
# 4. 민간 기업 근로여건 개선 지원: two boxes with a 실적 line
# ---------------------------------------------------------------------------
section_band("sec4", line1(60, 70, 647, 651), line1(90, 95, 648, 652), 645.7)

xs = [X0, 62.3, 81.1, 305.5, 307.5, 313.2, 332.0, X1]
g = Grid("welfare", xs, [1700, 4600, 1390, 260])
for a, t0, t1, e, hx, bx in ((X0, 62.3, 81.1, 305.5, 115, 62.5), (307.5, 313.2, 332.0, X1, 365, 313.4)):
    g.put(a, e, 0, 1, [line1(hx, hx + 10, 678, 682)], frame(HEAD, top="soft", left="soft", right="soft"), bold=True)
    g.put(a, e, 1, 2, lines_in(bx - 1, bx + 3, 696, 730), frame(left="soft", right="soft", bottom="dot"),
          align="LEFT", line=1380)
    row = line1(t0, t0 + 3, 743, 747)
    g.put(a, t0, 2, 3, [], frame(left="soft"))
    g.put(t0, t1, 2, 3, [runs_of(row, x1=t1)], frame(WHITE, **BOX))
    tight(g, t0, 2)
    scale = 0.93 if a == X0 else 1.0   # left 실적 line is 9.7 pt over 218 pt: smaller size, 장평 ~70
    g.put(t1, e, 2, 3, [strip_runs(runs_of(row, x0=t1, scale=scale))], frame(right="soft"), align="LEFT", line=1200)
    g.put(a, e, 3, 4, [], frame(left="soft", right="soft", bottom="soft"))
block(g, 676.0)

g = Grid("result", [X0, 111.7, X1], [3200])
g.put(X0, 111.7, 0, 1, [runs_of(line1(65, 70, 776, 780), WHITE)], frame("#6A6A6A", top="mid", bottom="mid", left="mid"))
g.put(111.7, X1, 0, 1, lines_in(115, 120, 768, 790), frame(top="mid", bottom="mid", right="mid"), align="LEFT",
      line=1480)
block(g, 767.3)

kit.finish(target, end=803.0)
