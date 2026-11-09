"""Rebuild KDN 2025 report page 135 (third PDF local page 35, printed page 95) as editable HWPX.

Usage: python3 work/kdn2025/p135.py <report3.pdf> <out.hwpx> [--page 35]

조직 및 인적자원관리 평가내용 01 continued: 나. (구분 / 추진 내용 / 추진 실적 table), 다. (three boxes
with ▶ connectors and the 임신·출산·육아기·사회적 기여 table whose 추진 실적 column holds four small
bar charts), 라. (추진배경 / 추진내용 / 추진실적 rows) and the 주요성과 box. Built with the shared kit
(one flat table per horizontal band on a grid of PDF x edges); all running text comes from the PDF
text layer, run by run (superscript years stay small runs on the baseline).

Images in the source and how they are kept:
- side tab, the "지적사항 개선" sticker (hand icon dropped), the 국정과제 / 여성가족부 / 문화체육관광부
  tags: typed or text-layer runs in separate cells.
- the bold arrow before 업무처리시간 ... -> "→"; the chevrons between the 다. boxes -> ▶ cells; the
  chevrons between the 라. labels are omitted (the labels keep their three gray steps).
- the four bar charts (임신기 근로단축 / 자녀돌봄휴가 / 육아휴직 / 육아시간 사용자수) -> value cells,
  values read from a 5x render: 22명→30명 (36%↑), 657명→699명 (6%↑), 102명→113명 (11%↑),
  138명→193명 (40%↑); every rise matches its tag (30/22 = 1.36, 699/657 = 1.06, 113/102 = 1.11,
  193/138 = 1.40). Bars and the curved arrows are not drawn; the chart boxes keep a gray plot area.
- the text layer prints "국정과제95번" while the tag image shows "국정과제 95번"; the text layer is kept.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kit  # noqa: E402
from kit import Layout, recipe_inputs  # noqa: E402

source, target = recipe_inputs(35, "실시간 인력 최적화와 AI 도입을 통한")
L = Layout(top=3100)
kit.setup(source, L)
from kit import *  # noqa: E402,F401,F403  helpers and presets bound to this page

LIGHT, HEAD, RESULT_HEAD = "#E4E4E4", "#D6D6D6", "#787878"
TAG = frame("#3C3C3C")
B = 1090


def hang(lines, base):
    """Lines keep their PDF indent: spaces for the x offset and for the line's own leading blanks."""
    out = []
    for line in lines:
        runs = runs_of(line)
        size = runs[0][1] / 100
        raw = "".join(s["text"] for s in line["spans"])
        offset = line["bbox"][0] - base + (len(raw) - len(raw.lstrip(" "))) * 0.29 * size
        n = max(0, round(offset / (0.29 * size)))
        out.append([(" " * n, runs[0][1], False, INK)] + runs if n else runs)
    return out


def joined(lines, sep):
    """A spaced label the PDF splits into two lines ('임 ... 신') as one paragraph."""
    runs = runs_of(lines[0])
    for line in lines[1:]:
        runs += [(sep, runs[-1][1], runs[-1][2], INK)] + runs_of(line)
    return runs


def tight(g, x0, r0, left=0, right=0):
    c0 = g.xs.index(to_x(x0))
    item = g.items[r0, c0]
    g.items[r0, c0] = (*item[:7], dict(left=left, right=right))


def heading(name, y, top, badge_x=None):
    g = Grid(name, [X0, badge_x, X1] if badge_x else [X0, X1], [1650])
    g.put(X0, badge_x or X1, 0, 1, [line1(55, 60, y - 1, y + 1)], align="LEFT", line=1450)
    if badge_x:
        g.put(badge_x, X1, 0, 1, "지적사항 개선", TAG, size=800, bold=True, color=WHITE, line=950)
        tight(g, badge_x, 0, 60, 60)
    block(g, top)


class Rows:
    """Union of PDF y edges -> grid row indices."""

    def __init__(self, ys):
        self.ys = sorted({round(y, 1) for y in ys})

    def __call__(self, y):
        return self.ys.index(round(y, 1))

    def hs(self):
        return [int(round((b - a) * 100)) for a, b in zip(self.ys, self.ys[1:])]


# ---------------------------------------------------------------------------
# Page chrome (odd page): running head over a rule, side tab, footer at the right.
# ---------------------------------------------------------------------------
L.add_table([[cell(0, 3350, 1680, [para([("01", 1380, True, WHITE)], "CENTER")[0]], dark)],
             [cell(0, 3350, 5960, [para([(ch, 950, True, INK)], "CENTER", 1160)[0] for ch in "경영관리"], gray2)]],
            floating=(57800, 15000))
foot = [(text, size, False, INK) for text, size in (
    (line1(450, 455, 818, 822)["text"], 790), ("    ", 790), (line1(540, 552, 816, 820)["text"], 1090))]
L.add_table([[cell(0, W, 1500, [para(foot, "RIGHT", 1300)[0]])]], floating=(5660, 81550))

g = Grid("head", [X0, 378.0, X1], [1680])
g.put(X0, 378.0, 0, 1, [], frame(bottom="soft"))
g.put(378.0, X1, 0, 1, [line1(380, 390, 35, 40)], align="RIGHT")
block(g, 32.0)

# ---------------------------------------------------------------------------
# 나. 구분 | 추진 내용 | 추진 실적 (dark-framed result column)
# ---------------------------------------------------------------------------
heading("title-na", 71.0, 69.8, 503.9)

g = Grid("workload", [X0, 102.0, 410.2, X1], [1850, 4720, 4800])     # y 91.5 .. 205.2
g.put(X0, 102.0, 0, 1, [line1(65, 70, 94, 98)], frame(HEAD, top="mid", right="soft"))
g.put(102.0, 410.2, 0, 1, [line1(230, 240, 94, 98)], frame(HEAD, top="mid"))
g.put(410.2, X1, 0, 1, [runs_of(line1(460, 465, 94, 98), WHITE)], frame(RESULT_HEAD, top="strong", left="strong",
                                                                           right="strong"))
for r, (y0, y1) in enumerate(((110.0, 157.2), (157.2, 204.0)), 1):
    rule = "soft" if r == 1 else "mid"
    g.put(X0, 102.0, r, r + 1, lines_in(55, 104, y0, y1), frame(LIGHT, bottom=rule), line=1430)
    g.put(102.0, 410.2, r, r + 1, hang(lines_in(104, 110, y0, y1), 105.1), frame(bottom=rule), align="LEFT",
          line=1430)
result = hang(lines_in(412, 420, 112, 185), 414.0) + [[("  → ", B, True, INK)] + runs_of(line1(430, 435, 186, 190))]
g.put(410.2, X1, 1, 3, result, frame(left="strong", right="strong", bottom="strong"), align="LEFT", line=1530)
block(g, 91.5)

# ---------------------------------------------------------------------------
# 다. three boxes joined by ▶, then the 임신 ~ 사회적 기여 table with value charts
# ---------------------------------------------------------------------------
heading("title-da", 216.0, 214.6)

g = Grid("steps", [X0, 213.8, 227.8, 384.8, 398.8, X1], [1920, 5250])     # y 236.8 .. 308.5
heads = sorted(lines_in(100, 560, 240, 244), key=lambda l: l["bbox"][0])
for k, ((a, e), head, base) in enumerate(zip(((X0, 213.8), (227.8, 384.8), (398.8, X1)), heads,
                                             (62.5, 233.5, 404.5))):
    if k < 2:
        g.put(a, e, 0, 1, [head], frame(HEAD, top="mid", left="mid", right="mid"))
    else:
        g.put(a, e, 0, 1, [runs_of(head, WHITE)], frame(RESULT_HEAD, top="mid", left="mid", right="mid"))
    g.put(a, e, 1, 2, hang(lines_in(a + 2, e - 5, 258, 300), base), frame(left="mid", right="mid", bottom="mid"),
          align="LEFT", line=1540)
for a, e in ((213.8, 227.8), (384.8, 398.8)):
    g.put(a, e, 1, 2, "▶", size=1100, color=ARROW, fit=False)
block(g, 236.8)

CH = (445.0, 451.5, 478.0, 484.4, 518.6, 552.7)      # label | tag | label edge | '24 | '25 | box edge
CHARTS = [(337.8, ["임신기 근로", "단축 사용자수"], "36%↑", "22명", "30명"),
          (386.5, ["자녀돌봄휴가", "사 용 자 수"], "6%↑", "657명", "699명"),
          (435.0, ["육 아 휴 직", "사 용 자 수"], "11%↑", "102명", "113명"),
          (484.0, ["육 아 시 간", "사 용 자 수"], "40%↑", "138명", "193명")]
SUB = (1150, 1150, 1050, 950)                            # label / '25 value, '24 value, tag + axis, years
LEFT_ROWS = (333.2, 366.0, 412.5, 487.2, 561.5)
ys = [314.5, *LEFT_ROWS, 527.0]
for top, *_ in CHARTS:
    ys += [top + sum(SUB[:i]) / 100 for i in range(5)]
R = Rows(ys)
xs = [X0, 102.0, 441.2, *CH, X1]
g = Grid("family", xs, R.hs())
g.put(X0, 102.0, 0, 1, [line1(65, 70, 317, 321)], frame(HEAD, top="mid", right="soft"))
g.put(102.0, 441.2, 0, 1, [line1(245, 255, 317, 321)], frame(HEAD, top="mid"))
g.put(441.2, X1, 0, 1, [runs_of(line1(475, 480, 317, 321), WHITE)], frame(RESULT_HEAD, top="strong", left="strong",
                                                                          right="strong"))
labels = [[joined([line1(60, 66, 336, 339), line1(84, 88, 336, 339)], "      "), runs_of(line1(60, 66, 350, 353))],
          [runs_of(line1(60, 66, 382, 386))],
          [runs_of(line1(60, 66, 443, 446))],
          [runs_of(line1(60, 66, 511, 514)), joined([line1(60, 66, 525, 528), line1(84, 88, 525, 528)], "      ")]]
for k, (y0, y1) in enumerate(zip(LEFT_ROWS, LEFT_ROWS[1:])):
    rule = "soft" if k < 3 else "mid"
    g.put(X0, 102.0, R(y0), R(y1), labels[k], frame(LIGHT, bottom=rule), line=1410)
    g.put(102.0, 441.2, R(y0), R(y1), hang(lines_in(104, 110, y0, y1 - 1), 105.1), frame(bottom=rule),
          align="LEFT", line=1410)
# result column: margins carry the dark frame (single-row cells keep every row defined)
last = len(R.ys) - 2
for r in range(1, last + 1):
    g.put(441.2, 445.0, r, r + 1, [], frame(left="strong", bottom="strong" if r == last else None))
    g.put(552.7, X1, r, r + 1, [], frame(right="strong", bottom="strong" if r == last else None))
box = dict(left="soft", right="soft")
plot = "#EEEEEE"
for top, names, rise, before, after in CHARTS:
    r0, r1, r2, r3, r4 = (R(top + sum(SUB[:i]) / 100) for i in range(5))
    g.put(445.0, 484.4, r0, r2, [[(t, 850, False, INK)] for t in names], frame(top="soft", **box), line=950)
    g.put(445.0, 451.5, r2, r3, [], frame(left="soft"))
    g.put(451.5, 478.0, r2, r3, rise, TAG, size=850, bold=True, color=WHITE, line=900, fit=False)
    tight(g, 451.5, r2)
    g.put(478.0, 484.4, r2, r3, [], frame(right="soft"))
    g.put(445.0, 484.4, r3, r4, [], frame(bottom="soft", **box))
    g.put(484.4, 518.6, r0, r1, [], frame(plot))
    g.put(518.6, 552.7, r0, r1, after, frame(plot), size=900, bold=True, line=980)
    g.put(484.4, 518.6, r1, r2, before, frame(plot), size=900, line=980)
    g.put(518.6, 552.7, r1, r2, [], frame(plot))
    g.put(484.4, 518.6, r2, r3, [], frame(plot, bottom="mid"))
    g.put(518.6, 552.7, r2, r3, [], frame(plot, bottom="mid"))
    g.put(484.4, 518.6, r3, r4, "’24년", frame(plot), size=800, line=790)
    g.put(518.6, 552.7, r3, r4, "’25년", frame(plot), size=800, bold=True, line=790)
g.put(445.0, 552.7, R(527.0), R(561.5), hang(lines_in(444, 455, 529, 550), 445.2), frame(bottom="strong"),
      align="LEFT", line=1520)
block(g, 314.5)

# ---------------------------------------------------------------------------
# 라. 추진배경 / 추진내용 / 추진실적
# ---------------------------------------------------------------------------
heading("title-ra", 573.0, 571.6)

BX = [(116.2, 260.5), (263.8, 407.8), (411.0, X1)]
xs = [X0, 113.6, 116.2, 260.5, 263.8, 407.8, 411.0, 414.0, 465.5, X1]
g = Grid("cooperation", xs, [1790, 1920, 500, 1900, 6180, 540, 3660])   # y 593.9 .. 758.8
g.put(X0, 113.6, 0, 3, [line1(60, 70, 606, 609)], frame("#E6E6E6"))
g.put(X0, 113.6, 3, 6, [line1(60, 70, 673, 677)], frame("#D2D2D2"))
g.put(X0, 113.6, 6, 7, [line1(60, 70, 737, 740)], frame("#BEBEBE"))
first = line1(120, 125, 598, 601)
g.put(116.2, 414.0, 0, 1, [runs_of(first, x1=415.0)], frame(top="mid", left="mid"), align="LEFT", line=1300)
g.put(414.0, 465.5, 0, 1, [strip_runs(runs_of(first, x0=415.0))],
      frame(top="mid", bottom="soft", left="soft", right="soft"), line=1000, fit=False)
tight(g, 414.0, 0)
g.put(465.5, X1, 0, 1, [], frame(top="mid", right="mid"))
g.put(116.2, X1, 1, 2, [runs_of(line1(120, 125, 613, 616))], frame(bottom="mid", left="mid", right="mid"),
      align="LEFT", line=1300)
heads = sorted(lines_in(115, 560, 639, 642), key=lambda l: l["bbox"][0])
for (a, e), head in zip(BX, heads):
    g.put(a, e, 3, 4, [head], frame(HEAD, top="mid", left="mid", right="mid"))
    base = lines_in(a, e, 657, 660)[0]["bbox"][0]
    g.put(a, e, 4, 5, hang(lines_in(a, e, 657, 712), base), frame(left="mid", right="mid", bottom="mid"),
          align="LEFT", line=1430)
g.put(116.2, X1, 6, 7, hang(lines_in(120, 125, 725, 745), 122.0), frame("#E4E4E4", top="soft", bottom="soft",
                                                                         left="soft", right="soft"),
      align="LEFT", line=1540)
block(g, 593.9)

# 주요성과: dark label; first line carries two outlined ministry tags
TX = [X0, 112.9, 125.6, 171.4, 327.2, 387.1, X1]
g = Grid("key-results", TX, [1900, 1750])               # y 765.5 .. 802.0
g.put(X0, 112.9, 0, 2, [runs_of(line1(60, 70, 777, 780), WHITE)], frame("#7F7F7F", top="mid", bottom="mid",
                                                                           left="mid"))
first = line1(115, 120, 769, 772)
cuts = [(112.9, 125.6, -1e9, 125.0), (125.6, 171.4, 125.0, 170.0), (171.4, 327.2, 170.0, 329.0),
        (327.2, 387.1, 329.0, 386.0), (387.1, X1, 386.0, 1e9)]
for k, (a, e, c0, c1) in enumerate(cuts):
    runs = strip_runs(runs_of(first, x0=c0, x1=c1))
    edge = dict(top="mid", right="mid" if e == X1 else None)
    if k in (1, 3):
        g.put(a, e, 0, 1, [runs], frame("#DADADA", **edge), line=1000, fit=False)
        tight(g, a, 0)
    else:
        g.put(a, e, 0, 1, [runs], frame(**edge), align="RIGHT" if k == 0 else ("LEFT" if k == 4 else "CENTER"),
              line=1270)
g.put(112.9, X1, 1, 2, [runs_of(line1(115, 120, 785, 788))], frame(bottom="mid", right="mid"), align="LEFT",
      line=1270)
block(g, 765.5)

kit.finish(target, end=802.2)
