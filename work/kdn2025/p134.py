"""Rebuild KDN 2025 report page 134 (third PDF local page 34, printed page 94) as editable HWPX.

Usage: python3 work/kdn2025/p134.py <report3.pdf> <out.hwpx> [--page 34]

조직 및 인적자원관리 평가내용 01 (일･가정 양립) opening page: section 1 추진체계 (환경분석 with the
three survey boxes and 내부분석 / 사회트렌드, 시사점, 추진전략, 추진과제) and section 2 가. (Why / How
banner, 고민 ① / ②, What, STEP1-3 boxes) and the 주요성과 box. Built with the shared kit (one
flat table per horizontal band on a grid of PDF x edges); all running text comes from the PDF text
layer, run by run (superscript years stay small runs on the baseline).

Images in the source and how they are kept:
- PART 01 box, 평가내용 chip, section number bands, the Why / How / What pills, STEP pills, the dark
  tabs on the 추진과제 boxes, the "Best Practice" and "지적사항 개선" stickers (trophy / hand icons
  dropped): typed cells; the footer logo is typed as its name 한전KDN㈜.
- the circled plus marks between the survey boxes -> "+" connector cells; the check boxes in front
  of the Why / What lines -> "□"; the circled numbers of 고민 1 / 2 -> ① ②.
- the dotted corner marks of the left labels and the chevrons between the STEP labels are
  decorative and omitted (the STEP label column keeps its three gray steps).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kit  # noqa: E402
from kit import Layout, recipe_inputs  # noqa: E402

source, target = recipe_inputs(34, "남성 육아휴직 제도는 존재하지만")
L = Layout(top=3100)
kit.setup(source, L)
from kit import *  # noqa: E402,F401,F403  helpers and presets bound to this page

DARK, LIGHT, HEAD, BODY_GRAY = "#6A6A6A", "#E4E4E4", "#D9D9D9", "#E6E6E6"
LABEL = frame("#F3F3F3", hatch="#E2E2E2")
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


def tight(g, x0, r0, left=0, right=0):
    c0 = g.xs.index(to_x(x0))
    item = g.items[r0, c0]
    g.items[r0, c0] = (*item[:7], dict(left=left, right=right))


def section_band(name, y, top):
    g = Grid(name, [X0, 85.5, X1], [2300])
    g.put(X0, 85.5, 0, 1, [runs_of(line1(64, 70, y - 2, y + 4), WHITE)], frame(DARK), line=1850)
    g.put(85.5, X1, 0, 1, [line1(90, 95, y - 2, y + 4)], frame(LIGHT), align="LEFT", line=1750)
    block(g, top)


def pill_line(name, line, top, pills, edges, check_x=(X0, 67.3)):
    """'□ [Why] title [How] title': check box, dark pills and title cells cut from one PDF line."""
    g = Grid(name, [check_x[0], check_x[1]] + edges, [1660])
    g.put(*check_x, 0, 1, "□", size=1200, line=1250, fit=False)
    for k, (a, e) in enumerate(zip(edges, edges[1:])):
        runs = strip_runs(runs_of(line, x0=a - 1, x1=e - 1))
        if k % 2 == 0:
            g.put(a, e, 0, 1, [[(t, s, True, WHITE) for t, s, *_ in runs]], frame("#6A6A6A"), line=1250, fit=False)
            tight(g, a, 0)
        else:
            g.put(a, e, 0, 1, [runs], align="LEFT", line=1500)
    block(g, top)


# ---------------------------------------------------------------------------
# Page chrome (even page): PART label at the left of a rule; footer at the left.
# ---------------------------------------------------------------------------
foot = [(line1(55, 60, 815, 822)["text"], 1090, False, INK), ("   ", 1090, False, INK),
        ("한전KDN㈜", 1090, True, INK)]   # the logo is an image; its name is typed
L.add_table([[cell(0, W, 1500, [para(foot, "LEFT", 1300)[0]])]], floating=(5660, 81550))

g = Grid("part-head", [X0, 103.0, 158.5, X1], [1500])
g.put(X0, 103.0, 0, 1, [[("PART ", 800, False), ("01", 1300, True)]], line=1300)
g.put(103.0, 158.5, 0, 1, "경영관리", frame("#333333"), size=1080, bold=True, color=WHITE)
g.put(158.5, X1, 0, 1, [], frame(bottom="soft"))
block(g, 32.0)

g = Grid("band", [X0, 124.0, X1], [1880, 970])
g.put(X0, 124.0, 0, 1, "평가내용 01", frame("#565656", top="strong"), size=970, bold=True, color=WHITE, ratio=80,
      line=1150)
g.put(X0, 124.0, 1, 2, [], frame("#E9E9E9", bottom="soft", left="soft", hatch="#DADADA"))
g.put(124.0, X1, 0, 2, [line1(125, 130, 75, 85)], frame("#E9E9E9", top="strong", bottom="soft", right="soft",
                                                     hatch="#DADADA"), align="LEFT", line=1480)
block(g, 71.0)

# ---------------------------------------------------------------------------
# 1 정부 국정과제 연계형 일･가정 양립 및 AI혁신 기반 추진체계 구축
# ---------------------------------------------------------------------------
section_band("section-1", 114.4, 111.5)

S = [(107.6, 255.1, 261.1), (263.6, 268.9, 416.9, 422.6), (425.1, 430.7, X1)]
xs = [X0, 105.4, 107.6, 136.0, 138.8, 255.1, 261.1, 263.6, 268.9, 323.5, 326.0, 359.8, 362.7, 416.9, 422.6, 425.1,
      430.7, X1]
g = Grid("environment", xs, [1730, 3520, 190, 3560])     # y 140.8 .. 230.8
g.put(X0, 105.4, 0, 4, [line1(60, 65, 179, 183)], LABEL, line=1300)
heads = sorted(lines_in(130, 560, 144, 148), key=lambda l: l["bbox"][0])
assert len(heads) == 3
box_head = frame(HEAD, top="mid", left="mid", right="mid", bottom="soft")
for (a, e), head in zip(((107.6, 255.1), (268.9, 416.9), (430.7, X1)), heads):
    g.put(a, e, 0, 1, [head], box_head)
for a, e in ((255.1, 268.9), (416.9, 430.7)):
    g.put(a, e, 0, 1, "+", frame("#9C9C9C", top="mid"), size=1100, bold=True, color=WHITE, fit=False)
for (a, e), base in (((107.6, 261.1), 113.5), ((263.6, 422.6), 269.5), ((425.1, X1), 431.0)):
    g.put(a, e, 1, 2, hang(lines_in(a + 2, e - 5, 160, 190), base), frame(left="mid", right="mid", bottom="mid"),
          align="LEFT", line=1440)
side = frame(LIGHT)
g.put(107.6, 136.0, 3, 4, [line1(110, 115, 199, 203), line1(110, 115, 212, 216)], side, line=1320)
g.put(138.8, 323.5, 3, 4, hang(lines_in(140, 145, 198, 216), 141.9),
      frame(top="mid", bottom="mid", left="mid", right="mid"), align="LEFT", line=1430)
g.put(326.0, 359.8, 3, 4, [line1(330, 336, 199, 203), line1(326, 331, 212, 216)], side, line=1320)
g.put(362.7, X1, 3, 4, hang(lines_in(363, 368, 198, 216), 365.8),
      frame(top="mid", bottom="mid", left="mid", right="mid"), align="LEFT", line=1430)
block(g, 140.8)

for name, y, top, h, fill in (("implication", 239.5, 234.3, 2060, frame("#ECECEC", hatch="#DCDCDC", left="mid")),
                              ("strategy", 263.6, 258.4, 2040, frame("#DBDBDB", left="mid"))):
    g = Grid(name, [X0, 105.4, 107.6, X1], [h])
    g.put(X0, 105.4, 0, 1, [line1(60, 65, y - 1, y + 1)], LABEL, line=1300)
    g.put(107.6, X1, 0, 1, [line1(108, 112, y - 2, y + 1)], fill, align="LEFT")
    block(g, top)

T = [(107.6, 130.2, 195.2, 218.1), (220.3, 242.9, 307.9, 330.8), (333.0, 355.6, 420.5, 443.5),
     (445.7, 468.2, 533.2, X1)]
xs = sorted({X0, 105.4, *[x for t in T for x in t]})
g = Grid("tasks", xs, [340, 3300])                       # y 282.5 .. 318.9
g.put(X0, 105.4, 0, 2, [line1(60, 65, 294, 297)], LABEL, line=1300)
task_fill = frame("#EDEDED", hatch="#DCDCDC")
for a, t0, t1, e in T:
    g.put(t0, t1, 0, 1, [], TAG)
    g.put(a, e, 1, 2, lines_in(a, e, 288, 306), task_fill, line=1430)
block(g, 282.5)

# ---------------------------------------------------------------------------
# 2 함께하는 육아, 함께 여는 가족친화 혁신
# ---------------------------------------------------------------------------
section_band("section-2", 334.9, 332.0)

g = Grid("title-ga", [X0, 431.3, 501.8, 503.9, X1], [1660])
g.put(X0, 431.3, 0, 1, [line1(55, 60, 360, 364)], align="LEFT", line=1450)
g.put(431.3, 501.8, 0, 1, "Best Practice", TAG, size=800, bold=True, color=WHITE, line=950)
g.put(503.9, X1, 0, 1, "지적사항 개선", TAG, size=800, bold=True, color=WHITE, line=950)
tight(g, 431.3, 0, 60, 60)
tight(g, 503.9, 0, 60, 60)
block(g, 360.8)

g = Grid("note", [X0, X1], [1350])
g.put(X0, X1, 0, 1, hang([line1(55, 60, 379, 383)], 56.7), align="LEFT", line=1150)
block(g, 378.8)

pill_line("why-how", line1(75, 85, 394, 398), 394.2, 2, [70.1, 110.1, 265.3, 305.3, X1])

# banner: bold statement in a white tab on a hatched band
g = Grid("banner", [X0, 71.0, 538.0, X1], [360, 1790])
hatch = frame("#EFEFEF", hatch="#D8D8D8")
g.put(X0, X1, 0, 1, [], hatch)
g.put(X0, 71.0, 1, 2, [], hatch)
g.put(71.0, 538.0, 1, 2, [line1(80, 85, 422, 426)], frame(WHITE, top="mid", left="mid", right="mid"), line=1300)
g.put(538.0, X1, 1, 2, [], hatch)
block(g, 415.2)

# 고민 ① / ② boxes
g = Grid("worries", [X0, 105.6, 304.5, 308.5, 357.4, X1], [1870, 3490])   # y 439.8 .. 493.2
for (a, b, e), num, title_x, base in (((X0, 105.6, 304.5), "①", 125, 62.5),
                                      ((308.5, 357.4, X1), "②", 382, 314.3)):
    tag = line1(a + 5, a + 30, 444, 447)
    g.put(a, b, 0, 1, [runs_of(tag, WHITE) + [(" " + num, 1090, True, WHITE)]], frame("#808080", top="mid"),
          line=1250)
    g.put(b, e, 0, 1, [line1(title_x, title_x + 2, 442, 446)], frame(HEAD, top="mid", right="mid"), line=1250)
    g.put(a, e, 1, 2, hang(lines_in(a + 2, a + 10, 460, 480), base),
          frame(left="mid", right="mid", bottom="mid"), align="LEFT", line=1440)
block(g, 439.8)

g = Grid("conclusion", [X0, X1], [1990])
g.put(X0, X1, 0, 1, [line1(120, 130, 499, 503)], frame("#D4D4D4"), line=1300)
block(g, 496.4)

pill_line("what", line1(75, 80, 522, 526), 521.8, 1, [70.1, 110.1, X1])

# ---------------------------------------------------------------------------
# STEP1-3: gray label column with STEP pills | headed boxes
# ---------------------------------------------------------------------------
xs = [X0, 66.4, 103.9, 113.6, 116.2, 255.4, 257.9, 397.1, 399.6, X1]
ys = [542.7, 548.5, 560.1, 609.6,            # STEP1: spacer, pill + header, body
      613.7, 619.5, 631.1, 680.6,            # STEP2
      684.7, 698.0, 703.5, 709.5, 741.6, 744.8]   # STEP3: header, pill, gap, body, end
hs = [int(round((b - a) * 100)) for a, b in zip(ys, ys[1:])]
g = Grid("steps", xs, hs)
r = {y: i for i, y in enumerate(ys)}
FILLS = ("#E6E6E6", "#CBCBCB", "#B2B2B2")
pill_box = frame(WHITE, top="soft", bottom="soft", left="soft", right="soft")
labels = [(542.7, 548.5, 560.1, 609.6, 613.7), (613.7, 619.5, 631.1, 680.6, 684.7),
          (684.7, 698.0, 709.5, 744.8, 744.8)]
for k, (top, p0, p1, end, nxt) in enumerate(labels):
    fill = frame(FILLS[k])
    pill = line1(70, 75, p0, p1 + 2)
    texts = [l for l in lines_in(56, 113, p1, end) if not l["text"].startswith("STEP")]
    g.put(X0, 113.6, r[top], r[p0], [], fill)
    g.put(X0, 66.4, r[p0], r[p1], [], fill)
    g.put(66.4, 103.9, r[p0], r[p1], [pill], pill_box, line=980, fit=False)
    tight(g, 66.4, r[p0])
    g.put(103.9, 113.6, r[p0], r[p1], [], fill)
    g.put(X0, 113.6, r[p1], r[end], [runs_of(t) for t in texts], fill, line=1320)
    tight(g, X0, r[p1], 60, 60)
    if nxt != end:
        g.put(X0, 113.6, r[end], r[nxt], [], frame(FILLS[k + 1]))
# STEP1 / STEP2 boxes: gray header, three bullet lines
for top, p1, end, head_y in ((542.7, 560.1, 609.6, 547.2), (613.7, 631.1, 680.6, 618.2)):
    g.put(116.2, X1, r[top], r[p1], [line1(190, 260, head_y - 1, head_y + 1)],
          frame(HEAD, top="mid", left="mid", right="mid"))
    g.put(116.2, X1, r[p1], r[end], hang(lines_in(120, 125, p1, end), 122.0),
          frame(left="mid", right="mid", bottom="mid"), align="LEFT", line=1430)
# STEP3: three headed boxes with a gray body
for (a, e), base in (((116.2, 255.4), 122.0), ((257.9, 397.1), 263.8), ((399.6, X1), 405.5)):
    g.put(a, e, r[684.7], r[703.5], [line1(a, e, 688, 692)], frame(top="mid", left="mid", right="mid", bottom="soft"))
    g.put(a, e, r[703.5], r[709.5], [], frame(left="mid", right="mid"))
    g.put(a, e, r[709.5], r[741.6], hang(lines_in(a + 3, e, 710, 730), base),
          frame(BODY_GRAY, left="mid", right="mid"), align="LEFT", line=1440)
    g.put(a, e, r[741.6], r[744.8], [], frame(left="mid", right="mid", bottom="mid"))
block(g, 542.7)

g = Grid("key-results", [X0, 112.9, X1], [5130])
g.put(X0, 112.9, 0, 1, [runs_of(line1(60, 70, 770, 773), WHITE)], frame("#7F7F7F", top="mid", bottom="mid", left="mid"))
g.put(112.9, X1, 0, 1, lines_in(115, 120, 752, 790), frame(top="mid", bottom="mid", right="mid"), align="LEFT",
      line=1430)
block(g, 750.8)

kit.finish(target, end=802.2)
