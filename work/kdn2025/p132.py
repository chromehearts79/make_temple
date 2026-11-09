"""Rebuild KDN 2025 report page 132 (3rd PDF local page 32, printed page 92) as editable HWPX.

Usage: python3 work/kdn2025/p132.py <report3.pdf> <out.hwpx> [--page 32]

조직 및 인적자원관리, 나. (에너지ICT 직무기술 교육: 기존 → 개선 box, GREAT strategy grid,
중점 사업전략 table; 사내전문가 활용: 현황분석 → 애로사항 → 추진방향, 추진노력 | 추진실적 table)
and 다. (리더십 코칭 / DEI 리더십 boxes) plus the 주요성과 box. Built with the shared kit (one flat
table per horizontal band on a grid of PDF x edges); all text comes from the PDF text layer.
The tags printed inside lines (신규, 경영진, 1직급 ~ 3직급, 사업소 팀장, 과장~차장, 주임~대리, 여성 리더,
G / R / E / A / T squares) are separate cells.

Images and how they are kept: PART box, footer logo (typed "한전KDN㈜"), the □ boxes before the two
headings (typed □), the "지적사항 개선" sticker (typed dark tag, hand icon dropped), the chevrons
between boxes (▶), the small down chevrons over the result bars (▼), the black circled numbers
❶ ❷ of 추진방향 and 추진노력 (typed ① ②), the dark tab strips over the GREAT columns (top borders).
In the DEI box the four tagged lines are set on the left box's line pitch, so they sit up to ~7pt
higher than printed; the box keeps its printed height.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kit  # noqa: E402
from kit import Layout, recipe_inputs  # noqa: E402

source, target = recipe_inputs(32, "에너지ICT 직무기술 향상 교육 프로그램 고도화 및 직무전문가 활용 강화")
L = Layout(top=3100)
kit.setup(source, L)
from kit import *  # noqa: E402,F401,F403  helpers and presets bound to this page

DARK, HEAD, SIDE = "#6E6E6E", "#D9D9D9", "#EBEBEB"
OUT_TAG = frame(WHITE, top="soft", bottom="soft", left="soft", right="soft")
HATCHED = frame("#EEEEEE", hatch="#DDDDDD")


def S(text, size=1090, bold=False, color=INK):
    return (text, size, bold, color)


def tight(g, x0, r0, left=0, right=0):
    c0 = g.xs.index(to_x(x0))
    item = g.items[r0, c0]
    g.items[r0, c0] = (*item[:7], dict(left=left, right=right))


def hang(lines, base):
    """Lines keep their PDF indent: spaces for the x offset and for the line's own leading blanks."""
    out = []
    for l in lines:
        runs = runs_of(l)
        size = runs[0][1] / 100
        raw = "".join(s["text"] for s in l["spans"])
        offset = l["bbox"][0] - base + (len(raw) - len(raw.lstrip(" "))) * 0.29 * size
        n = max(0, round(offset / (0.29 * size)))
        out.append([(" " * n, runs[0][1], False, INK)] + runs if n else runs)
    return out


def is_tag(s):
    bold = any(f in s["font"] for f in kit.BOLD_FONTS + kit.SYMBOL_FONTS)
    return 7.5 < s["size"] < 9.6 and bold


def tagged(g, r0, r1, a, e, spans, rects, edge=None, bold=None, align="LEFT"):
    """Spans of one PDF line as [lead] | tag | text ... cells over rows r0..r1."""
    edge = edge or {}
    slots, tags = [[]], []
    for s in spans:
        if is_tag(s):
            if not tags or slots[-1]:
                tags.append([])
                slots.append([])
            tags[-1].append(s)
        else:
            slots[-1].append(s)
    assert len(tags) == len(rects), ("".join(s["text"] for s in spans), len(tags))
    bounds = [a] + [x for t in rects for x in t] + [e]
    for i, part in enumerate(slots):
        x0, x1 = bounds[2 * i], bounds[2 * i + 1]
        if x1 - x0 < 0.5:
            continue
        side = {k: v for k, v in edge.items()
                if not (k == "left" and i > 0) and not (k == "right" and i < len(slots) - 1)}
        if not "".join(s["text"] for s in part).strip():
            g.put(x0, x1, r0, r1, [], frame(**side))
            continue
        runs = runs_of(dict(spans=part), bold=bold)
        if i == 0 and "".join(t for t, *_ in runs) == "∙":
            g.put(x0, x1, r0, r1, [runs], frame(**side), align="RIGHT", fit=False)
            tight(g, x0, r0, 0, 150)
        else:
            g.put(x0, x1, r0, r1, [runs], frame(**side), align=align if i == 0 else "LEFT")
            tight(g, x0, r0, 60 if i else 320, 100)
    for (t0, t1), part in zip(rects, tags):
        g.put(t0, t1, r0, r1, [runs_of(dict(spans=part))], OUT_TAG, line=1000)
        tight(g, t0, r0)


# ---------------------------------------------------------------------------
# Page chrome (even page): PART label at the left of a rule; footer at the left.
# ---------------------------------------------------------------------------
foot = [(line1(55, 60, 815, 822)["text"], 1090, False, INK), ("   ", 1090, False, INK),
        ("한전KDN㈜", 1090, True, INK)]   # the logo is an image; its name is typed
L.add_table([[cell(0, W, 1500, [para(foot, "LEFT", 1300)[0]])]], floating=(5660, 81550))

g = Grid("part-head", [X0, 103.5, 160.0, X1], [1500])
g.put(X0, 103.5, 0, 1, [[("PART ", 800, False), ("01", 1300, True)]], line=1300)
g.put(103.5, 160.0, 0, 1, "경영관리", frame("#333333"), size=1080, bold=True, color=WHITE)
g.put(160.0, X1, 0, 1, [], frame(bottom="soft"))
block(g, 32.0)

g = Grid("title-na", [X0, X1], [1650])
g.put(X0, X1, 0, 1, [line1(55, 60, 70, 74)], align="LEFT", line=1450)
block(g, 70.0)

g = Grid("sq1", [X0, X1], [1600])
g.put(X0, X1, 0, 1, [[("□ ", 1350, True, INK)] + runs_of(line1(68, 72, 91, 95))], align="LEFT", line=1400)
block(g, 90.5)

# 기존 → 개선
g = Grid("before-after", [X0, 59.5, 88.5, 297.5, 299.0, 310.4, 316.0, 345.0, 554.0, X1], [3800])
box = dict(top="soft", bottom="soft")
g.put(59.5, 88.5, 0, 1, [line1(62, 66, 125, 129)], frame("#E0E0E0", left="soft", **box))
g.put(88.5, 297.5, 0, 1, hang(lines_in(94, 105, 116, 146), 95.1), frame(right="soft", **box), align="LEFT",
      line=1550)
g.put(299.0, 310.4, 0, 1, "▶", size=1100, color="#B0B0B0", fit=False)
g.put(316.0, 345.0, 0, 1, [runs_of(line1(320, 322, 125, 129), WHITE)], frame(DARK, left="soft", **box))
g.put(345.0, 554.0, 0, 1, hang(lines_in(350, 360, 116, 146), 351.7), frame(right="soft", **box), align="LEFT",
      line=1550)
block(g, 112.2)

# GREAT: five columns (letter square, English / Korean name, business line; A and T share one)
C = (X0, 155.2, 255.8, 356.4, 457.0, X1)
SQ = ((97.6, 112.4), (198.2, 213.0), (298.9, 313.6), (399.5, 414.2), (500.1, 514.9))
g = Grid("great", sorted(set(C) | {x for s in SQ for x in s}), [450, 1500, 3300, 2150])
for k, ((a, e), (s0, s1)) in enumerate(zip(zip(C, C[1:]), SQ)):
    sep = dict(right="dot") if k < 4 else {}
    g.put(a, e, 0, 1, [], frame(top="strong"))
    g.put(a, s0, 1, 2, [])
    g.put(s0, s1, 1, 2, [runs_of(line1(s0, s1, 160, 163), WHITE)], frame("#5A5A5A"), line=1100, fit=False)
    tight(g, s0, 1)
    g.put(s1, e, 1, 2, [], frame(**sep))
    narrow = dict(ratio=72, fit=False) if k == 3 else {}      # 'Artificial Intelligence'
    g.put(a, e, 2, 3, lines_in(a, e, 180, 200), frame("#DCDCDC", **sep), line=1300, **narrow)
for a, e in ((X0, 155.2), (155.2, 255.8), (255.8, 356.4), (356.4, X1)):
    g.put(a, e, 3, 4, [line1(a, e, 214, 217)], frame("#EEEEEE", hatch="#DDDDDD",
                                                     **({"right": "dot"} if e != X1 else {})))
block(g, 156.5)

# 중점 사업전략 | 과정내용 및 수료 인원 | 사업연계 성과
K1, K2 = 221.3, 372.4
g = Grid("strategy", [X0, 62.5, 73.0, K1, K2, X1], [1560, 1930, 1920, 3440])
g.put(X0, K1, 0, 1, [line1(105, 112, 240, 243)], frame(HEAD, top="mid", bottom="soft"))
g.put(K1, K2, 0, 1, [line1(248, 252, 240, 243)], frame(HEAD, top="mid", bottom="soft", left="soft"))
g.put(K2, X1, 0, 1, [line1(430, 436, 240, 243)], frame("#7F7F7F", top="strong", left="strong", right="strong",
                                                       bottom="soft"), color=WHITE)
for r, ys, n in ((1, (257, 260), 1), (2, (276, 279), 1), (3, (303, 306), 1)):
    ln = line1(63, 66, *ys)
    last = dict(bottom="soft")
    g.put(X0, 62.5, r, r + 1, [], frame(SIDE, **last))
    g.put(62.5, 73.0, r, r + 1, [runs_of(ln, WHITE, x1=72.0)], frame("#5A5A5A"), line=1050, fit=False)
    tight(g, 62.5, r)
    g.put(73.0, K1, r, r + 1, [strip_runs(runs_of(ln, x0=72.0, x1=K1))], frame(SIDE, **last), align="LEFT")
    tight(g, 73.0, r, 100, 100)
mixed = line1(63, 66, 276, 279)       # R row: label and both bullets share one PDF line
res = dict(left="strong", right="strong")
g.put(K1, K2, 1, 2, [line1(224, 226, 258, 262)], frame(left="soft", bottom="soft"), align="LEFT")
g.put(K1, K2, 2, 3, [runs_of(mixed, x0=222.0, x1=K2)], frame(left="soft", bottom="soft"), align="LEFT")
g.put(K1, K2, 3, 4, lines_in(224, 226, 296, 326), frame(left="soft", bottom="soft"), align="LEFT", line=1550)
g.put(K2, X1, 1, 2, [line1(375, 377, 258, 262)], frame(bottom="soft", **res), align="LEFT")
g.put(K2, X1, 2, 3, [runs_of(mixed, x0=K2)], frame(bottom="soft", **res), align="LEFT")
g.put(K2, X1, 3, 4, lines_in(375, 377, 296, 326), frame(bottom="strong", **res), align="LEFT", line=1550)
block(g, 239.6)

# □ 사내전문가 ... with the 지적사항 개선 sticker
g = Grid("sq2", [X0, 453.1, 505.2, X1], [1600])
g.put(X0, 453.1, 0, 1, [[("□ ", 1350, True, INK)] + runs_of(line1(68, 72, 337, 340))], align="LEFT", line=1400)
g.put(453.1, 505.2, 0, 1, "지적사항 개선", frame("#3C3C3C"), size=760, bold=True, color=WHITE, line=900)
tight(g, 453.1, 0, 40, 40)
block(g, 336.5)

# 현황분석 → 애로사항 → 추진방향
B = ((59.5, 185.6, 62.5, HEAD, INK), (205.0, 370.9, 208.1, HEAD, INK), (390.1, 553.1, 405.2, DARK, WHITE))
g = Grid("analysis", [X0, 59.5, 185.6, 205.0, 370.9, 390.1, 553.1, X1], [2160, 3400])
for k, (a, e, base, fill, color) in enumerate(B):
    side = dict(left="soft", right="soft")
    g.put(a, e, 0, 1, [runs_of(line1(a, e, 362, 366), color)], frame(fill, top="soft", **side))
    lines = lines_in(a, e, 380, 412)
    if k < 2:
        body = hang(lines, base)
    else:
        body = [[S(m + " ", 1090, True)] + runs_of(l) for m, l in zip("①②", lines)]
    g.put(a, e, 1, 2, body, frame(bottom="soft", **side), align="LEFT", line=1550)
    if k < 2:
        g.put(e, B[k + 1][0], 0, 2, "▶", size=1100, color="#B0B0B0", fit=False)
block(g, 357.8)

# 추진노력 | 추진실적
xs = [X0, 59.5, 121.5, 124.4, 177.8, 376.4, 383.9, 553.2, X1]
g = Grid("effort", xs, [2160, 3400, 5170, 3720])
g.put(59.5, 376.4, 0, 1, [line1(195, 200, 424, 427)], frame(HEAD, top="soft", left="soft", right="soft"))
g.put(383.9, 553.2, 0, 1, [runs_of(line1(445, 450, 424, 427), WHITE)], frame(DARK, top="soft", left="soft",
                                                                          right="soft"))
g.put(59.5, 121.5, 1, 3, [[S("①", 1090, True)]] + [runs_of(l) for l in lines_in(60, 75, 470, 505)],
      frame("#EEEEEE", hatch="#DDDDDD", left="soft", bottom="soft"), line=1350)
g.put(121.5, 177.8, 1, 2, lines_in(125, 145, 443, 472), frame(HEAD, bottom="soft"), line=1400)
g.put(121.5, 177.8, 2, 3, lines_in(125, 145, 487, 515), frame(HEAD, bottom="soft"), line=1400)
g.put(177.8, 376.4, 1, 2, hang(lines_in(180, 182, 443, 472), 180.7), frame(right="soft", bottom="soft"),
      align="LEFT", line=1500)
g.put(177.8, 376.4, 2, 3, hang(lines_in(180, 190, 479, 523), 180.7), frame(right="soft", bottom="soft"),
      align="LEFT", line=1500)
cert = lines_in(64, 80, 532, 560)
g.put(59.5, 124.4, 3, 4, [[S("② ", 1090, True)] + runs_of(cert[0])] + [runs_of(l) for l in cert[1:]],
      frame(left="soft", bottom="soft"), line=1350)
g.put(124.4, 376.4, 3, 4, hang(lines_in(124, 134, 530, 560), 124.4), frame(right="soft", bottom="soft"),
      align="LEFT", line=1550)
for r, (y0, y1), last in ((1, (442, 472), False), (2, (478, 523), False), (3, (530, 560), True)):
    g.put(383.9, 553.2, r, r + 1, hang(lines_in(386, 396, y0, y1), 386.9),
          frame(left="soft", right="soft", bottom="soft"), align="LEFT", line=1550)
block(g, 419.7)

# ---------------------------------------------------------------------------
# 다. 리더십 프로그램
# ---------------------------------------------------------------------------
g = Grid("title-da", [X0, X1], [1650])
g.put(X0, X1, 0, 1, [line1(55, 60, 575, 579)], align="LEFT", line=1450)
block(g, 574.5)

LT = (70.4, 97.6)              # left tags
RT = (321.2, 365.5)            # right tags
ys = [596.4, 617.9, 634.3, 650.0, 665.5, 681.2, 696.8, 712.4, 729.5, 735.5, 755.2, 758.1]
R = ys.index
xs = sorted({X0, 305.0, 307.5, X1, 217.3, 236.0, 495.8, 514.6} | set(LT) | set(RT))
g = Grid("leadership", xs, [int(round((b - a) * 100)) for a, b in zip(ys, ys[1:])])
for (a, e), (t0, t1), y in (((X0, 305.0), (217.3, 236.0), 601), ((307.5, X1), (495.8, 514.6), 601)):
    ln = line1(a, e, y - 1, y + 1)
    edge = dict(top="mid", bottom="soft", left="mid", right="mid")
    g.put(a, t0, 0, 1, [strip_runs(runs_of(ln, x1=t0))], frame(top="mid", bottom="soft", left="mid"), align="RIGHT")
    tight(g, a, 0, 100, 140)
    g.put(t0, t1, 0, 1, [runs_of(ln, x0=t0)], frame(WHITE, top="soft", bottom="soft", left="soft", right="soft"),
          line=1000)
    tight(g, t0, 0)
    g.put(t1, e, 0, 1, [], frame(top="mid", bottom="soft", right="mid"))
# left box: tagged bullets, dash lines, continuation
LE = dict(left="mid", right="mid")
for y0, y1, ly in ((617.9, 634.3, 621), (634.3, 650.0, 637), (665.5, 681.2, 668), (696.8, 712.4, 699)):
    tagged(g, R(y0), R(y1), X0, 305.0, line1(62, 63, ly - 1, ly + 1)["spans"], (LT,), edge=LE)
for y0, y1, ly in ((650.0, 665.5, 652), (681.2, 696.8, 683)):
    g.put(X0, 305.0, R(y0), R(y1), hang([line1(62, 63, ly - 1, ly + 1)], 62.5), frame(**LE), align="LEFT")
g.put(X0, 305.0, R(712.4), R(729.5), hang([line1(100, 101, 713, 716)], 62.5), frame(**LE), align="LEFT")
# right box: four tagged bullets (two have their bullet on a separate PDF line), dash line, footnote
RE = dict(left="mid", right="mid")
for y0, y1, ly in ((617.9, 634.3, 621), (634.3, 650.0, 638), (650.0, 665.5, 655), (665.5, 681.2, 672.5)):
    hits = lines_in(312, 330, ly - 1, ly + 1.5)
    spans = [s for h in sorted(hits, key=lambda h: h["bbox"][0]) for s in h["spans"]]
    tagged(g, R(y0), R(y1), 307.5, X1, spans, (RT,), edge=RE)
g.put(307.5, X1, R(681.2), R(696.8), hang([line1(313, 314, 685, 687)], 313.4), frame(**RE), align="LEFT")
g.put(307.5, X1, R(696.8), R(729.5), hang(lines_in(310, 330, 703, 717), 313.4), frame(**RE), align="LEFT",
      line=1150)
for a, e, x in ((X0, 305.0, 85), (307.5, X1, 325)):
    g.put(a, e, R(729.5), R(735.5), "▼", frame(**LE), size=500, color="#A0A0A0", line=440, fit=False)
    g.put(a, e, R(735.5), R(755.2), [line1(x, x + 5, 738, 741)], frame("#E3E3E3", **LE))
    g.put(a, e, R(755.2), R(758.1), [], frame(bottom="mid", **LE))
block(g, 596.4)

# 주요성과
g = Grid("result", [X0, 59.5, 111.7, 114.7, X1], [3720])
g.put(59.5, 111.7, 0, 1, [runs_of(line1(65, 70, 777, 781), WHITE)], frame(DARK))
g.put(114.7, X1, 0, 1, lines_in(116, 120, 768, 798), frame(top="mid", bottom="mid", left="mid", right="mid"),
      align="LEFT", line=1500)
block(g, 764.4)

kit.finish(target, end=802.0)
