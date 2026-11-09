"""Rebuild KDN 2025 report page 55 (second PDF local page 5, printed page 35) as editable HWPX.

Usage: python3 work/kdn2025/p55.py <report2.pdf> <out.hwpx> [--page 5]

일자리 및 균등한 기회 평가내용 04 opening page (odd page). Built with the shared diagram kit (one
flat table per horizontal band on a grid of PDF x edges); all running text comes from the PDF text
layer. Images: the 평가내용 04 chip, the section number bands, the 채용 / 육성 / 대표성 pills (their
words are in the text layer), the filled numbers ❶-❸ of 개선방향 (typed ① ② ③), the 'NEW 신규' and
'지적사항 개선' stickers (typed as dark tags; flourish and hand icon dropped), the chevrons (typed ▶),
the (+) joint (typed +), the side tab, and the four 주요성과 bar charts, whose printed values become
value cells without bars (read from a 6x render; each rise matches its two values):
여성 고용비율 17% → 18% (1%p↑), 여성 관리자(1~3직급) 비율 12% → 18% (6%p↑), 여성 장기위탁
교육자 1명 → 3명 (2명↑), 상임·비상임 임원 여성비율 목표 20% → ’25년 25% (5%p↑).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kit  # noqa: E402
from kit import Layout, recipe_inputs  # noqa: E402

source, target = recipe_inputs(5, "여성 인재 전주기 육성")
L = Layout(top=3100)
kit.setup(source, L)
from kit import *  # noqa: E402,F401,F403  helpers and presets bound to this page

DARK, LABEL = "#6A6A6A", "#E6E6E6"
HEAD = "#D7D7D7"
BOX = dict(top="soft", bottom="soft", left="soft", right="soft")
TAG = frame("#3C3C3C")


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


def section_band(name, num_line, title_line, top):
    g = Grid(name, [X0, 84.5, X1], [2300])
    g.put(X0, 84.5, 0, 1, [runs_of(num_line, WHITE)], frame(DARK), line=1700)
    g.put(84.5, X1, 0, 1, [runs_of(title_line)], frame(LABEL), align="LEFT", line=1700)
    block(g, top)


def pill_title(name, number, badge, title, edges, top):
    """'가. (채용) title': number, light pill with the badge word, 14pt title (runs lists)."""
    g = Grid(name, [X0, *edges, X1], [1650])
    g.put(X0, edges[0], 0, 1, [number], align="LEFT", line=1450)
    g.put(edges[0], edges[1], 0, 1, [badge], pill)
    g.put(edges[1], X1, 0, 1, [title], align="LEFT", line=1450)
    block(g, top)


def tag(g, x0, x1, r0, r1, text):
    """Dark sticker typed from its image ('NEW 신규' -> 신규, '지적사항 개선')."""
    g.put(x0, x1, r0, r1, text, TAG, size=760, bold=True, color=WHITE, line=900)


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

g = Grid("banner", [X0, 124.0, X1], [4140])
g.put(X0, 124.0, 0, 1, [[("평가내용 ", 800, True, WHITE), ("04", 1350, True, WHITE)]], frame("#686868"),
      line=1500)
g.put(124.0, X1, 0, 1, lines_in(125, 130, 76, 96), striped, align="LEFT", line=1510)
block(g, 70.9)

# ---------------------------------------------------------------------------
# 1. 여성 인재 활용 및 대표성 제고 개선방향: 환경분석 (three boxes) and 개선방향 (three arrows)
# ---------------------------------------------------------------------------
section_band("sec1", line1(60, 70, 126, 130), line1(90, 95, 127, 131), 124.2)

xs = [X0, 105.1, 108.0, 255.5, 258.0, 405.5, 409.0, X1]
R = Rows([154.0, 172.0, 218.5, 223.8, 249.7])
g = Grid("analysis", xs, R.hs)
side = frame(LABEL, top="mid")
g.put(X0, 105.1, R(154.0), R(218.5), [line1(60, 65, 181, 185)], side, bold=True)
for a, e, hx, bx in ((108.0, 255.5, 130, 113.5), (258.0, 405.5, 259, 263.8), (409.0, X1, 420, 414.1)):
    g.put(a, e, R(154.0), R(172.0), [line1(hx, hx + 4, 157, 161)], frame(HEAD, **BOX), bold=True)
    g.put(a, e, R(172.0), R(218.5), hang(lines_in(bx - 1.5, bx + 11, 174, 210), bx),
          frame(left="soft", right="soft", bottom="soft"), align="LEFT", line=1440)
g.put(X0, 105.1, R(223.8), R(249.7), [line1(60, 65, 231, 235)], side, bold=True)
for k, (a, e, x, fill) in enumerate(((108.0, 255.5, 125, "#F0F0F0"), (255.5, 405.5, 291, "#D9D9D9"),
                                     (405.5, X1, 427, "#F0F0F0"))):
    runs = runs_of(line1(x, x + 1, 230, 233))
    g.put(a, e, R(223.8), R(249.7), [[("①②③"[k] + " ", 1090, True, INK)] + runs],
          frame(fill, top="soft", bottom="soft", left="dot" if k else None))
block(g, 154.0)

# ---------------------------------------------------------------------------
# 2. 여성 인재 전주기 육성·활용 고도화
# ---------------------------------------------------------------------------
section_band("sec2", line1(60, 70, 265, 269), line1(90, 95, 265, 269), 263.0)

# 가. (채용): 분야 | 추진 노력 ▶ 추진 실적 (real table lines; 추진 실적 boxed in dark)
pill_title("title-ga", runs_of(line1(55, 60, 295, 299)), runs_of(line1(84, 86, 296, 300)),
           strip_runs(runs_of(line1(115, 116, 295, 299))), [72.8, 116.0], 294.0)

RIGHT_HEAD = frame("#7E7E7E", top="strong", left="strong", right="strong", bottom="soft")
LEFT_HEAD = dict(top="soft", bottom="soft")
CHEVRON = dict(size=1000, color=ARROW)


def right_cell(last):
    return frame(left="strong", right="strong", bottom="strong" if last else "soft")


xs = [X0, 113.4, 344.2, 369.1, 377.2, 394.0, X1]
R = Rows([315.5, 333.9, 390.1, 404.4, 433.2])
g = Grid("hiring", xs, R.hs)
g.put(X0, 113.4, 0, 1, [line1(70, 75, 318, 322)], frame(HEAD, **LEFT_HEAD), bold=True)
g.put(113.4, 377.2, 0, 1, [line1(225, 226, 318, 322)], frame(HEAD, left="soft", **LEFT_HEAD), bold=True)
g.put(394.0, X1, 0, 1, [runs_of(line1(454, 455, 318, 322), WHITE)], RIGHT_HEAD, bold=True)
g.put(377.2, 394.0, R(333.9), R(433.2), "▶", **CHEVRON)
label = frame("#EBEBEB", bottom="soft")
g.put(X0, 113.4, R(333.9), R(390.1), lines_in(60, 70, 345, 370), label, line=1430)
g.put(113.4, 377.2, R(333.9), R(390.1), lines_in(115, 118, 335, 380), frame(left="soft", bottom="soft"),
      align="LEFT", line=1300)
g.put(394.0, X1, R(333.9), R(390.1), hang(lines_in(396, 410, 335, 385), 397.0), right_cell(False), align="LEFT",
      line=1300)
g.put(X0, 113.4, R(390.1), R(433.2), lines_in(60, 75, 395, 420), label, line=1430)
g.put(113.4, 344.2, R(390.1), R(404.4), [line1(115, 118, 392, 395)], frame(left="soft"), align="LEFT")
tag(g, 344.2, 369.1, R(390.1), R(404.4), "신규")
g.put(113.4, 377.2, R(404.4), R(433.2), hang(lines_in(115, 118, 405, 425), 116.4), frame(left="soft", bottom="soft"),
      align="LEFT", line=1220)
g.put(394.0, X1, R(390.1), R(433.2), hang(lines_in(396, 410, 391, 425), 397.0), right_cell(True), align="LEFT",
      line=1300)
block(g, 315.5)

# 나. (육성): 과정명 | 추진 노력 (with an inner 개설 배경 / 교육내용 pair) ▶ 추진 실적
pill_title("title-na", runs_of(line1(55, 60, 444, 448)), runs_of(line1(88, 90, 445, 449)),
           strip_runs(runs_of(line1(119, 120, 444, 448))), [76.9, 120.1], 443.6)

xs = [X0, 113.4, 117.0, 243.5, 247.5, 322.1, 332.5, 357.4, 374.2, 377.2, 394.0, X1]
R = Rows([465.0, 483.4, 497.0, 514.4, 545.3, 560.5, 563.5, 579.5, 624.5, 627.1])
g = Grid("leaders", xs, R.hs)
g.put(X0, 113.4, 0, 1, [line1(70, 72, 467, 471)], frame(HEAD, **LEFT_HEAD), bold=True)
g.put(113.4, 377.2, 0, 1, [line1(225, 226, 467, 471)], frame(HEAD, left="soft", **LEFT_HEAD), bold=True)
g.put(394.0, X1, 0, 1, [runs_of(line1(454, 455, 467, 471), WHITE)], RIGHT_HEAD, bold=True)
g.put(377.2, 394.0, R(483.4), R(627.1), "▶", **CHEVRON)
# 여성 리더십 최고위 과정
g.put(X0, 113.4, R(483.4), R(514.4), lines_in(58, 112, 485, 505), label, line=1430)
g.put(113.4, 332.5, R(483.4), R(497.0), [line1(115, 118, 485, 489)], frame(left="soft"), align="LEFT")
tag(g, 332.5, 357.4, R(483.4), R(497.0), "신규")
g.put(113.4, 377.2, R(497.0), R(514.4), [line1(115, 118, 497, 500)], frame(left="soft", bottom="soft"), align="LEFT")
g.put(394.0, X1, R(483.4), R(514.4), hang(lines_in(396, 410, 485, 505), 397.0), right_cell(False), align="LEFT",
      line=1430)
# 여성 장기위탁 교육 과정
g.put(X0, 113.4, R(514.4), R(545.3), lines_in(57, 112, 516, 535), label, line=1430)
g.put(113.4, 377.2, R(514.4), R(545.3), hang(lines_in(115, 118, 516, 532), 116.4), frame(left="soft", bottom="soft"),
      align="LEFT", line=1250)
g.put(394.0, X1, R(514.4), R(545.3), hang(lines_in(396, 410, 516, 535), 397.0), right_cell(False), align="LEFT",
      line=1430)
# 여성 역량 강화 워크숍 (Connect&Grow)
g.put(X0, 113.4, R(545.3), R(627.1), lines_in(58, 112, 558, 612), label, line=1300)
g.put(113.4, 322.1, R(545.3), R(560.5), [line1(115, 118, 547, 551)], frame(left="soft"), align="LEFT")
tag(g, 322.1, 374.2, R(545.3), R(560.5), "지적사항 개선")
g.put(113.4, 117.0, R(560.5), R(627.1), [], frame(left="soft", bottom="soft"))
g.put(117.0, 374.2, R(560.5), R(563.5), [], "1")
for a, e, hx, bx in ((117.0, 243.5, 159, 122.1), (247.5, 374.2, 291, 252.4)):
    g.put(a, e, R(563.5), R(579.5), [line1(hx, hx + 1, 566, 570)], frame("#E3E3E3", top="soft", left="soft",
                                                                         right="soft"))
    g.put(a, e, R(579.5), R(624.5), hang(lines_in(bx - 1.5, bx + 12, 583, 615), bx),
          frame(left="soft", right="soft", bottom="soft"), align="LEFT", line=1300)
g.put(243.5, 247.5, R(563.5), R(624.5), [], "1")
g.put(117.0, 374.2, R(624.5), R(627.1), [], frame(bottom="soft"))
g.put(374.2, 377.2, R(560.5), R(627.1), [], frame(bottom="soft"))
g.put(394.0, X1, R(545.3), R(627.1), hang(lines_in(396, 410, 554, 612), 397.0), right_cell(True), align="LEFT",
      line=1550)
block(g, 465.0)

# 다. (대표성): two boxes joined by (+)
l = line1(55, 60, 638, 642)
pill_title("title-da", strip_runs(runs_of(l, x1=76.0)), strip_runs(runs_of(l, x0=76.0, x1=119.0)),
           strip_runs(runs_of(l, x0=119.0)), [76.9, 120.1], 637.5)

xs = [X0, 294.0, 307.5, X1]
g = Grid("representation", xs, [1670, 4880])
for a, e, hx, bx in ((X0, 294.0, 100, 62.5), (307.5, X1, 340, 313.4)):
    g.put(a, e, 0, 1, [line1(hx, hx + 5, 662, 666)], frame(HEAD, **BOX), bold=True)
    g.put(a, e, 1, 2, lines_in(bx - 1, bx + 3, 679, 715), frame(left="soft", right="soft", bottom="soft"),
          align="LEFT", line=1440)
g.put(294.0, 307.5, 0, 2, "+", size=1200, bold=True, color="#9A9A9A")
block(g, 659.5)

# ---------------------------------------------------------------------------
# 주요성과: four bar charts (images) as value cells; titles from the text layer.
# ---------------------------------------------------------------------------
PANELS = (
    ((119.8, 153.3, 186.9, 220.4), 140, "1%p↑", "18%", "17%", "’24년"),
    ((228.9, 262.5, 296.0, 329.6), 233, "6%p↑", "18%", "12%", "’24년"),
    ((338.0, 371.6, 405.1, 438.7), 343, "2명↑", "3명", "1명", "’24년"),
    ((447.1, 480.7, 514.2, 547.8), 449, "5%p↑", "25%", "20%", "목표"),
)
xs = [X0, 111.7] + [x for p in PANELS for x in p[0]] + [X1]
R = Rows([735.2, 739.4, 752.5, 756.5, 767.0, 778.0, 785.5, 794.8, 799.2])
g = Grid("results", xs, R.hs)
g.put(X0, 111.7, 0, len(R.hs), [runs_of(line1(65, 70, 760, 764), WHITE)],
      frame("#6A6A6A", top="mid", bottom="mid", left="mid"))
g.put(111.7, X1, 0, 1, [], frame(top="mid", right="mid"))
g.put(111.7, X1, R(794.8), R(799.2), [], frame(bottom="mid", right="mid"))
g.put(547.8, X1, R(739.4), R(794.8), [], frame(right="mid"))
axis = "#E6E6E6"
for (a, b, c, e), tx, rise, high, low, first in PANELS:
    g.put(a, e, R(739.4), R(752.5), [line1(tx, tx + 1, 738, 743)], frame("#E3E3E3", top="soft", left="soft",
                                                                         right="soft"))
    cols = ((a, b), (b, c), (c, e))
    content = {(756.5, 1): ([[(rise, 800, True, WHITE)]], "#3C3C3C"),
               (756.5, 2): ([[(high, 880, True, INK)]], None),
               (767.0, 0): ([[(low, 880, False, INK)]], None),
               (785.5, 0): ([[(first, 780, False, INK)]], axis),
               (785.5, 1): ([], axis),
               (785.5, 2): ([[("’25년", 780, True, INK)]], axis)}
    for y0, y1 in ((752.5, 756.5), (756.5, 767.0), (767.0, 778.0), (778.0, 785.5), (785.5, 794.8)):
        for k, (x0, x1) in enumerate(cols):
            text, fill = content.get((y0, k), ([], None))
            edges = dict(left="soft" if k == 0 else None, right="soft" if k == 2 else None,
                         bottom="soft" if y1 == 794.8 else None, top="soft" if y0 == 785.5 else None)
            g.put(x0, x1, R(y0), R(y1), text, frame(fill, **{s: v for s, v in edges.items() if v}), line=880)
block(g, 735.2)

kit.finish(target, end=801.0)
