"""Rebuild KDN 2025 report PDF page 93 (second PDF local page 43, printed page 63) as editable HWPX.

Usage: python3 work/kdn2025/p93.py <report2.pdf> <out.hwpx> [--page 43]

상생･협력 및 지역발전 평가내용 02 opening page and its section 1 (안심 빛 환경, 전기차 지원). Built
with the shared diagram kit (one flat table per horizontal band on a grid of PDF x edges; rows here
are given as PDF y edges). All text comes from the PDF text layer. Images: the 평가내용 chip (its
check mark dropped), the section-number band, the side tab and the 'Best Practice' sticker (trophy
dropped) are typed cells; the village illustration (with its LED가로등 / 센서등 / CCTV / 태양광 조명
icon labels) and the four photos are empty photo cells; the handshake icon is omitted. Tags
(신규, 보건복지부, 한국예술인복지재단) are separate boxed cells.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kit  # noqa: E402
from kit import Layout, recipe_inputs  # noqa: E402

source, target = recipe_inputs(43, "기부･봉사활동 등 지역사회 참여, 지역경제 활성화를 위한 프로그램의 개발 및 실행을 위한")
L = Layout(top=3100)
kit.setup(source, L)
from kit import *  # noqa: E402,F401,F403  helpers and presets bound to this page

DARK, LABEL = "#6A6A6A", "#E6E6E6"
SIDE = frame("#E3E3E3", top="soft")
BOXTAG = frame(WHITE, top="soft", bottom="soft", left="soft", right="soft")
HATCH = frame("#EEEEEE", hatch="#E0E0E0")
GRAYBOX = "#EBEBEB"


def hang(lines, base):
    """Lines keep their PDF indent: spaces for the x offset and for the line's own lead."""
    out = []
    for l in lines:
        runs = runs_of(l)
        size = runs[0][1] / 100
        raw = "".join(s["text"] for s in l["spans"])
        offset = l["bbox"][0] - base + (len(raw) - len(raw.lstrip(" "))) * 0.29 * size
        n = max(0, round(offset / (0.29 * size)))
        out.append([(" " * n, runs[0][1], False, INK)] + runs if n else runs)
    return out


def split(line, cuts, colors=None):
    """One PDF line cut at x positions into run lists (tag words become their own cells)."""
    edges = [-1e9, *cuts, 1e9]
    colors = colors or [INK] * (len(edges) - 1)
    return [strip_runs(runs_of(line, c, x0=a, x1=b)) for a, b, c in zip(edges, edges[1:], colors)]


class YGrid:
    """Grid whose rows are given as PDF y edges; cells are placed by (x0, x1, y0, y1)."""

    def __init__(self, name, xs, ys):
        self.ys = ys
        self.g = Grid(name, xs, [round(b * 100) - round(a * 100) for a, b in zip(ys, ys[1:])])

    def row(self, y):
        for i, v in enumerate(self.ys):
            if abs(v - y) < 0.01:
                return i
        raise ValueError(f"{self.g.name}: no row edge at y {y}")

    def put(self, x0, x1, y0, y1, content, fill="1", **kw):
        self.g.put(x0, x1, self.row(y0), self.row(y1), content, fill, **kw)

    def tag(self, x0, x1, y0, y1, runs, fill):
        """Small tag cell: thin symmetric padding so a short tag stays on one line."""
        width = to_x(x1) - to_x(x0)
        ratio = min(90, int(90 * (width - 160) / 100 * 0.96 / text_width(runs, 90)))
        self.put(x0, x1, y0, y1, [runs], fill, line=1000, ratio=ratio, fit=False)
        key = (self.row(y0), self.g.xs.index(to_x(x0)))
        self.g.items[key] = (*self.g.items[key][:7], dict(left=80, right=80, top=40, bottom=40))

    def done(self):
        block(self.g, self.ys[0])


def boxed(name, label_line, body_lines, top, height, label_fill="#D5D5D5", label_color=INK):
    """추진배경 box: label at left, outlined body with bullet lines."""
    g = Grid(name, [X0, 111.7, X1], [height])
    g.put(X0, 111.7, 0, 1, [runs_of(label_line, label_color)],
          frame(label_fill, top="mid", bottom="mid", left="mid"))
    g.put(111.7, X1, 0, 1, body_lines, frame(top="mid", bottom="mid", right="mid"), align="LEFT")
    block(g, top)


# ---------------------------------------------------------------------------
# Page chrome (odd page): running head over a rule, side tab, footer at the right.
# ---------------------------------------------------------------------------
L.add_table([[cell(0, 3350, 1680, [para([("01", 1380, True, WHITE)], "CENTER")[0]], dark)],
             [cell(0, 3350, 5960, [para([(ch, 950, True, INK)], "CENTER", 1160)[0] for ch in "경영관리"], gray2)]],
            floating=(57800, 15000))
foot = [(only_text, size, False, INK) for only_text, size in (
    (line1(450, 455, 818, 822)["text"], 790), ("    ", 790), (line1(540, 552, 816, 820)["text"], 1090))]
L.add_table([[cell(0, W, 1500, [para(foot, "RIGHT", 1300)[0]])]], floating=(5660, 81550))

g = Grid("head", [X0, 376.0, X1], [1680])
g.put(X0, 376.0, 0, 1, [], frame(bottom="soft"))
g.put(376.0, X1, 0, 1, [line1(375, 385, 35, 40)], align="RIGHT")
block(g, 32.0)

# 평가내용 02 band: dark chip (image, check mark dropped) over a hatched band, two-line title.
g = Grid("band", [X0, 124.0, X1], [1450, 2690])
g.put(X0, 124.0, 0, 1, [[("평가내용 ", 800, True, WHITE), ("02", 1350, True, WHITE)]], frame("#565656", top="strong"),
      line=1300)
g.put(X0, 124.0, 1, 2, [], frame("#E9E9E9", bottom="soft", left="soft", hatch="#DADADA"))
g.put(124.0, X1, 0, 2, lines_in(125, 130, 75, 100), frame("#E9E9E9", top="strong", bottom="soft", right="soft",
                                                         hatch="#DADADA"), align="LEFT", line=1500)
block(g, 70.9)

boxed("background", line1(65, 70, 136, 140), lines_in(115, 120, 127, 150), 124.3, 3710)

# 추진방향: three header boxes
g = Grid("direction", [X0, 114.1, 119.0, 258.0, 266.4, 405.4, 413.8, 552.8, X1], [2580])
g.put(X0, 114.1, 0, 1, [line1(60, 70, 176, 180)], SIDE)
for a, e in ((119.0, 258.0), (266.4, 405.4), (413.8, 552.8)):
    g.put(a, e, 0, 1, [lines_in(a, e, 175, 180)[0]], frame("#EAEAEA", top="soft", bottom="soft", left="soft",
                                                           right="soft"))
block(g, 168.0)

# 실행과제: hatched boxes; the first one has two 신규 tags.
xs = [X0, 114.1, 119.0, 129.9, 148.7, 261.3, 265.0, 407.3, 410.9, 553.3, X1]
g = YGrid("tasks", xs, [201.8, 208.3, 220.0, 224.0, 236.0, 239.7, 251.4, 255.9])
g.put(X0, 114.1, 201.8, 255.9, [line1(60, 70, 225, 230)], SIDE)
g.put(119.0, 261.3, 201.8, 208.3, [], HATCH)
for y0, y1, y2, y in ((208.3, 220.0, 224.0, 208.8), (239.7, 251.4, 255.9, 240.0)):
    line = line1(120, 125, y - 0.5, y + 0.5)
    bullet, tagged, rest = split(line, [129.0, 148.0])
    g.put(119.0, 129.9, y0, y2, [bullet], HATCH, line=1250)
    g.tag(129.9, 148.7, y0, y1, tagged, BOXTAG)
    g.put(148.7, 261.3, y0, y2, [rest], HATCH, align="LEFT", line=1250)
    g.put(129.9, 148.7, y1, y2, [], HATCH)
g.put(119.0, 261.3, 224.0, 239.7, hang([line1(125, 135, 224, 225)], 122.0), HATCH, align="LEFT", line=1250)
for a, e, x in ((265.0, 407.3, 268.0), (410.9, 553.3, 414.0)):
    g.put(a, e, 201.8, 255.9, hang(lines_in(x - 1, x + 10, 205, 245), x), HATCH, align="LEFT", line=1540)
g.done()

# ---------------------------------------------------------------------------
# 1. 지역사회 안전환경 개선 / 가. 안심 빛 환경
# ---------------------------------------------------------------------------
g = Grid("sec1", [X0, 84.5, X1], [2300])
g.put(X0, 84.5, 0, 1, [runs_of(line1(60, 70, 276, 280), WHITE)], frame(DARK), line=1700)
g.put(84.5, X1, 0, 1, [line1(90, 95, 277, 281)], frame(LABEL), align="LEFT", line=1700)
block(g, 274.8)

g = Grid("title-ga", [X0, 409.4, 480.0, X1], [1650])
g.put(X0, 409.4, 0, 1, [line1(55, 60, 304, 308)], align="LEFT", line=1450)
g.put(409.4, 480.0, 0, 1, "Best Practice", frame("#3C3C3C"), size=800, bold=True, color=WHITE, line=1000)
block(g, 304.5)

boxed("background-ga", line1(65, 70, 338, 342), lines_in(115, 120, 330, 352), 327.1, 3710)

# 협력체계: 한전KDN role | (handshake icon omitted) | three partners with their roles
xs = [X0, 114.1, 117.0, 153.3, 303.4, 333.0, 388.0, X1]
g = YGrid("partners", xs, [370.5, 374.3, 391.2, 408.2, 425.4])
g.put(X0, 114.1, 370.5, 425.4, [line1(60, 70, 393, 397)], SIDE)
g.put(117.0, 153.3, 370.5, 425.4, lines_in(120, 150, 384, 405), BOXTAG, line=1430)
g.put(153.3, 303.4, 370.5, 425.4, lines_in(155, 165, 376, 412), frame(GRAYBOX), align="LEFT", line=1430)
rows = ((374.3, 391.2), (391.2, 408.2), (408.2, 425.4))
for k, (y0, y1) in enumerate(rows):
    last = k == 2
    g.put(333.0, 388.0, y0, y1, [lines_in(333, 388, y0, y1)[0]],
          frame(top="soft" if k == 0 else None, left="soft", right="soft", bottom="soft" if last else "dot"))
    g.put(388.0, X1, y0, y1, [lines_in(388, X1, y0, y1)[0]], frame(GRAYBOX, bottom=None if last else "dot"),
          align="LEFT")
g.done()

# 안전 시설 구축 | 마을 예술 경관 조성 box with the illustration, three photos and captions
xs = [X0, 59.5, 245.5, 248.0, 306.1, 347.5, 350.0, 449.5, 452.0, 552.0, X1]
g = YGrid("light", xs, [435.5, 450.0, 503.0, 505.8, 577.6, 594.3, 597.0])
g.put(X0, 306.1, 435.5, 450.0, [line1(140, 160, 436, 440)], frame("#D9D9D9", top="mid", left="mid"), bold=True)
g.put(306.1, X1, 435.5, 450.0, [line1(380, 400, 436, 440)], frame("#D9D9D9", top="mid", right="mid"), bold=True)
g.put(X0, 59.5, 450.0, 597.0, [], frame(left="mid", bottom="mid"))
g.put(552.0, X1, 450.0, 597.0, [], frame(right="mid", bottom="mid"))
g.put(59.5, 306.1, 450.0, 503.0, hang(lines_in(62, 70, 452, 495), 62.5), frame(right="soft", bottom="dot"),
      align="LEFT", line=1540)
g.put(306.1, 552.0, 450.0, 503.0, hang(lines_in(310, 325, 452, 495), 311.3), frame(bottom="dot"), align="LEFT",
      line=1540)
for a, e in ((59.5, 245.5), (248.0, 347.5), (350.0, 449.5), (452.0, 552.0)):
    g.put(a, e, 505.8, 577.6, [], photo)
    g.put(a, e, 577.6, 594.3, [lines_in(a, e, 579, 586)[0]], frame("#EEEEEE", hatch="#E0E0E0", left="mid",
                                                                   right="mid", bottom="soft"), line=1250)
g.put(59.5, 552.0, 594.3, 597.0, [], frame(bottom="mid"))
block(g.g, 435.5)

# ---------------------------------------------------------------------------
# 나. 전기차 지원 / 무료충전
# ---------------------------------------------------------------------------
g = Grid("title-na", [X0, X1], [1650])
g.put(X0, X1, 0, 1, [line1(55, 60, 606, 611)], align="LEFT", line=1450)
block(g, 607.0)

boxed("background-na", line1(65, 70, 640, 645), lines_in(115, 120, 632, 655), 629.5, 3710)

xs = [X0, 110.4, 113.0, 450.0, X1]
g = YGrid("ev", xs, [672.9, 708.6, 744.4])
for y0, y1, (a, b), last in ((672.9, 708.6, (675, 700), False), (708.6, 744.4, (710, 735), True)):
    g.put(X0, 110.4, y0, y1, lines_in(60, 105, a, b), frame("#E3E3E3", bottom="soft"), bold=True, line=1320)
    g.put(113.0, 450.0, y0, y1, hang(lines_in(115, 120, a, b), 118.4),
          frame(top=None if last else "soft", left="soft", bottom="soft" if last else "dot"), align="LEFT", line=1550)
g.put(450.0, X1, 672.9, 744.4, [], frame("#E4E4E4", top="soft", bottom="soft", left="mid", right="soft"))
g.done()

g = Grid("note", [X0, X1], [1450])
g.put(X0, X1, 0, 1, [line1(55, 60, 746, 750)], align="LEFT", line=1200)
block(g, 746.9)

# 주요성과: each line opens with a gray tag (보건복지부 / 한국예술인복지재단).
xs = [X0, 111.7, 125.6, 171.4, 202.5, X1]
g = YGrid("result", xs, [765.2, 769.1, 782.2, 785.2, 798.3, 802.1])
g.put(X0, 111.7, 765.2, 802.1, [runs_of(line1(65, 70, 776, 780), WHITE)],
      frame(DARK, top="mid", bottom="mid", left="mid"))
g.put(111.7, X1, 765.2, 769.1, [], frame(top="mid", right="mid"))
TAG = frame("#E3E3E3")
for (y0, y1, y2), t1, last in (((769.1, 782.2, 785.2), 171.4, False), ((785.2, 798.3, 802.1), 202.5, True)):
    line = line1(115, 120, y0, y1)
    bullet, tagged, rest = split(line, [125.0, t1 - 1.0])
    g.put(111.7, 125.6, y0, y2, [bullet], frame(bottom="mid") if last else "1", align="RIGHT", line=1250)
    g.tag(125.6, t1, y0, y1, tagged, TAG)
    g.put(t1, X1, y0, y2, [rest], frame(right="mid", bottom="mid" if last else None), align="LEFT", line=1250)
g.put(125.6, 202.5, 798.3, 802.1, [], frame(bottom="mid"))
g.done()

kit.finish(target, end=803.0)
