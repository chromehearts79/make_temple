"""Rebuild KDN 2025 report page 131 (3rd PDF local page 31, printed page 91) as editable HWPX.

Usage: python3 work/kdn2025/p131.py <report3.pdf> <out.hwpx> [--page 31]

조직 및 인적자원관리, section 4 "중장기 경영전략 추진을 위한 직무 전문 인재 양성 프로그램 고도화":
인재상 / HRD 목표 / 역량진단 / 핵심전문가 / 추진방향 box, then 가. (AI 인재 육성 체계: three
stage boxes, the framed 과정설계 ~ 개발자 과정 block and the 상시학습 e-러닝 part). Built with the
shared kit (one flat table per horizontal band on a grid of PDF x edges); all running text, the
'25년 / ~'30년 / ~'35년 pills and the 니즈분석 / 역량진단 / 상시학습 tags come from the PDF text layer
and are separate cells.

Images and how they are kept: section-4 number band and side tab (typed / text layer), the
chevron joints of 인재상 and the round arrows of 역량진단 (▶), the dark numbered squares of
추진방향 (dark cells with 1 2 3), the black circled numbers of 가. (① ② ③), the 'Best Practice'
sticker (typed as a dark tag, trophy dropped), the gray funnels (▼), the chevron column at the
left of the 과정 block (gray label cells with outlined 기초 / 직무 / 전문 pills) and the e-러닝 course
thumbnail image at the bottom right (y 714-799): its text was read from an 8x render and typed
into a two-column grid of cells (인공지능 | 생성형 AI).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kit  # noqa: E402
from kit import Layout, recipe_inputs  # noqa: E402

source, target = recipe_inputs(31, "중장기 경영전략 추진을 위한 직무 전문 인재 양성 프로그램 고도화")
L = Layout(top=3100)
kit.setup(source, L)
from kit import *  # noqa: E402,F401,F403  helpers and presets bound to this page

DARK, SIDE = "#6A6A6A", "#E4E4E4"
OUT_TAG = frame(WHITE, top="soft", bottom="soft", left="soft", right="soft")
BOX = dict(top="soft", bottom="soft", left="soft", right="soft")


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


def tagged(g, r, a, e, ln, rects, tag_fill=OUT_TAG, tag_color=INK, edge=None):
    """One PDF line as [lead] | tag | text cells; rects: the tags' cell edges in order."""
    edge = edge or {}
    slots, tags = [[]], []
    for s in ln["spans"]:
        if is_tag(s):
            if not tags or slots[-1]:
                tags.append([])
                slots.append([])
            tags[-1].append(s)
        else:
            slots[-1].append(s)
    assert len(tags) == len(rects), (ln["text"], len(tags))
    bounds = [a] + [x for t in rects for x in t] + [e]
    for i, spans in enumerate(slots):
        x0, x1 = bounds[2 * i], bounds[2 * i + 1]
        if x1 - x0 < 0.5:
            continue
        side = {k: v for k, v in edge.items()
                if not (k == "left" and i > 0) and not (k == "right" and i < len(slots) - 1)}
        if not "".join(s["text"] for s in spans).strip():
            g.put(x0, x1, r, r + 1, [], frame(**side))
            continue
        g.put(x0, x1, r, r + 1, [runs_of(dict(spans=spans))], frame(**side), align="LEFT")
        tight(g, x0, r, 0, 100)
    for (t0, t1), spans in zip(rects, tags):
        g.put(t0, t1, r, r + 1, [runs_of(dict(spans=spans), tag_color)], tag_fill, line=1000)
        tight(g, t0, r)


# ---------------------------------------------------------------------------
# Page chrome (odd page): running head over a rule, side tab, footer at the right.
# ---------------------------------------------------------------------------
L.add_table([[cell(0, 3350, 1680, [para([("01", 1380, True, WHITE)], "CENTER")[0]], dark)],
             [cell(0, 3350, 5960, [para([(ch, 950, True, INK)], "CENTER", 1160)[0] for ch in "경영관리"], gray2)]],
            floating=(57800, 15000))
foot = [(text, size, False, INK) for text, size in (
    (line1(450, 455, 818, 822)["text"], 790), ("    ", 790), (line1(540, 546, 816, 820)["text"], 1090))]
L.add_table([[cell(0, W, 1500, [para(foot, "RIGHT", 1300)[0]])]], floating=(5660, 81550))

g = Grid("head", [X0, 378.0, X1], [1680])
g.put(X0, 378.0, 0, 1, [], frame(bottom="soft"))
g.put(378.0, X1, 0, 1, [line1(380, 385, 35, 40)], align="RIGHT")
block(g, 32.0)

g = Grid("sec4", [X0, 84.5, X1], [2300])
g.put(X0, 84.5, 0, 1, [runs_of(line1(64, 70, 73, 78), WHITE)], frame(DARK), line=1700)
g.put(84.5, X1, 0, 1, [line1(90, 95, 74, 78)], frame("#E6E6E6"), align="LEFT", line=1700)
block(g, 70.9)

LB = 107.9           # label column end


def label(g, r0, r1, y):
    g.put(X0, LB, r0, r1, [line1(58, 70, y, y + 4)], frame(SIDE))


# 인재상: four chevron segments
SEG = ((114.2, 212.9, "#EBEBEB"), (227.6, 326.2, "#D6D6D6"), (340.9, 439.6, "#EBEBEB"), (454.3, 553.0, "#D6D6D6"))
g = Grid("talent", [X0, LB, 110.5] + [x for s in SEG for x in s[:2]] + [X1], [2500])
label(g, 0, 1, 106)
g.put(110.5, 114.2, 0, 1, [], frame(top="soft", bottom="soft", left="soft"))
for k, (a, e, fill) in enumerate(SEG):
    g.put(a, e, 0, 1, [line1(a, e, 106, 110)], frame(fill, top="soft", bottom="soft"))
    if k < 3:
        g.put(e, SEG[k + 1][0], 0, 1, "▶", frame(top="soft", bottom="soft"), size=900, color="#B0B0B0", fit=False)
g.put(553.0, X1, 0, 1, [], frame(top="soft", bottom="soft", right="soft"))
block(g, 100.2)

g = Grid("hrd", [X0, LB, 110.5, X1], [2450])
label(g, 0, 1, 136)
g.put(110.5, X1, 0, 1, [line1(210, 215, 136, 140)], frame("#D0D0D0"))
block(g, 129.8)

# 역량진단: three step heads joined by ▶, three bullet columns
xs = [X0, LB, 110.5, 256.5, 258.2, 272.9, 405.5, 407.8, 422.2, X1]
g = Grid("diagnosis", xs, [1870, 3630])
label(g, 0, 2, 181)
for a, e, fill in ((110.5, 256.5, "#E6E6E6"), (272.9, 405.5, "#DCDCDC"), (422.2, X1, "#D0D0D0")):
    g.put(a, e, 0, 1, [line1(a, e, 162, 166)], frame(fill))
for a, e in ((256.5, 272.9), (405.5, 422.2)):
    g.put(a, e, 0, 1, "▶", size=900, color="#8C8C8C", fit=False)
for k, (a, e, base) in enumerate(((110.5, 258.2, 113.6), (258.2, 407.8, 263.2), (407.8, X1, 412.9))):
    g.put(a, e, 1, 2, hang(lines_in(a + 1, a + 15, 180, 210), base),
          frame(bottom="mid", right="soft" if k < 2 else None), align="LEFT", line=1550)
block(g, 159.1)

# 핵심전문가: three columns of [pill year] count
COLS = ((110.5, 258.9, 155.6, 184.4), (258.9, 406.8, 299.0, 336.5), (406.8, X1, 446.8, 484.2))
g = Grid("experts", [X0, LB] + sorted({x for c in COLS for x in c} | {X1}), [2500])
label(g, 0, 1, 226)
for k, (a, e, t0, t1) in enumerate(COLS):
    edge = dict(top="soft", bottom="soft", left="soft" if k == 0 else None, right="soft")
    edge = {k2: v for k2, v in edge.items() if v}
    tagged(g, 0, a, e, line1(t0 + 2, t1, 224, 228), ((t0, t1),), edge=edge)
block(g, 218.8)

# 추진방향: three hatched boxes with dark number squares
BOXES = ((113.3, 126.7, 254.7), (262.6, 275.9, 403.9), (411.8, 425.2, 553.1))
g = Grid("direction", [X0, LB, 110.5] + [x for b in BOXES for x in b] + [X1], [1810, 1900])
label(g, 0, 2, 262)
hatched = frame("#EEEEEE", hatch="#DDDDDD", top="soft", bottom="soft", left="soft")
for k, (a, n1, e) in enumerate(BOXES):
    g.put(a, n1, 0, 1, str(k + 1), frame("#333333"), size=1000, bold=True, color=WHITE, line=1050, fit=False)
    tight(g, a, 0)
    g.put(a, n1, 1, 2, [], frame("#EEEEEE", hatch="#DDDDDD", bottom="soft", left="soft"))
    g.put(n1, e, 0, 2, lines_in(n1, n1 + 5, 252, 282), frame("#EEEEEE", hatch="#DDDDDD", top="soft",
                                                           bottom="soft", right="soft"), align="LEFT", line=1450)
    tight(g, n1, 0, 120, 100)
block(g, 248.4)

# ---------------------------------------------------------------------------
# 가. AI 인재 육성 체계
# ---------------------------------------------------------------------------
g = Grid("title-ga", [X0, 420.7, 491.3, X1], [1650])
g.put(X0, 420.7, 0, 1, [line1(55, 60, 295, 299)], align="LEFT", line=1450)
g.put(420.7, 491.3, 0, 1, "Best Practice", frame("#4A4A4A"), size=850, bold=True, color=WHITE, line=1000)
tight(g, 420.7, 0, 60, 60)
block(g, 295.3)

STAGE = ((X0, 221.3, 62.5, "soft"), (223.9, 388.6, 229.7, "strong"), (391.1, X1, 397.0, "soft"))
g = Grid("stages", [X0, 221.3, 223.9, 388.6, 391.1, X1], [1870, 3400, 2440])
for k, (a, e, base, w) in enumerate(STAGE):
    side = dict(left=w, right=w)
    head = frame("#6E6E6E" if k == 1 else "#D9D9D9", top=w, **side)
    g.put(a, e, 0, 1, [runs_of(line1(a, e, 318, 322), WHITE if k == 1 else INK)], head)
    g.put(a, e, 1, 2, hang(lines_in(a, e, 338, 368), base), frame(**side), align="LEFT", line=1500)
    g.put(a, e, 2, 3, [line1(a, e, 374, 378)], frame("#E6E6E6", bottom=w, **side))
block(g, 316.8)

g = Grid("funnel", [X0, X1], [1420])
g.put(X0, X1, 0, 1, "▼", size=1000, color="#A8A8A8", line=1000)
block(g, 393.9)

# The framed block (y 408.1-802.0): 과정 column | 과정설계 / ①②③ courses / 교육활용, then 상시학습.
ys = [408.1, 411.3, 428.0, 446.5, 457.0, 468.0, 485.5, 504.0, 515.5, 527.3, 544.5, 563.0, 584.9, 602.0, 609.0,
      620.0, 631.5, 681.0, 689.0, 710.0, 713.6, 725.0, 738.0, 755.0, 772.0, 789.0, 799.0, 802.0]
R = ys.index
xs = [X0, 59.5, 63.8, 72.2, 92.2, 96.6, 99.2, 104.4, 104.9, 106.6, 107.7, 139.3, 146.9, 150.2, 314.9, 325.0,
      328.8, 333.0, 361.5, 370.0, 451.1, 453.7, 501.0, 505.5, 547.9, 553.0, X1]
g = Grid("courses", xs, [int(round((b - a) * 100)) for a, b in zip(ys, ys[1:])])
OUTER = "strong"
g.put(X0, X1, 0, 1, [], frame(top=OUTER, left=OUTER, right=OUTER))
g.put(X0, 59.5, 1, R(799.0), [], frame(left=OUTER))
g.put(553.0, X1, 1, R(799.0), [], frame(right=OUTER))
g.put(X0, X1, R(799.0), R(802.0), [], frame(bottom=OUTER, left=OUTER, right=OUTER))

# left column: 과정 설계 / 기초 입문 과정 / 직무 실무 과정 / 전문 개발자 과정
g.put(59.5, 96.6, R(411.3), R(446.5), lines_in(65, 70, 415, 445), frame("#E3E3E3"), bold=True, line=1300)
PILL = frame(WHITE, top="soft", bottom="soft", left="soft", right="soft")
for (y0, yp, y1, y2), fill, color, pill_y, text_y in (
        ((446.5, 457.0, 468.0, 504.0), "#CFCFCF", INK, 464, (476, 495)),
        ((504.0, 515.5, 527.3, 563.0), "#BDBDBD", INK, 523, (535, 555)),
        ((563.0, 609.0, 620.0, 681.0), "#8E8E8E", WHITE, 612, (624, 645))):
    g.put(59.5, 96.6, R(y0), R(yp), [], frame(fill))
    g.put(59.5, 63.8, R(yp), R(y1), [], frame(fill))
    g.put(63.8, 92.2, R(yp), R(y1), [line1(68, 72, pill_y, pill_y + 2)], PILL, line=900, fit=False)
    tight(g, 63.8, R(yp))
    g.put(92.2, 96.6, R(yp), R(y1), [], frame(fill))
    g.put(59.5, 96.6, R(y1), R(y2), [runs_of(l, color) for l in lines_in(60, 75, *text_y)], frame(fill),
          line=1300)
g.put(59.5, 96.6, R(681.0), R(689.0), [], frame("#8E8E8E"))

# 과정설계: two tagged lines
for y0, y1, ly in ((411.3, 428.0, 417), (428.0, 446.5, 430)):
    tagged(g, R(y0), 99.2, 553.0, line1(105, 110, ly - 1, ly + 1), ((104.9, 139.3),))


def course(y_head, ly, y_box, y_end, split, arrow, left_lines, right_lines, mark):
    """'① title' head row with a dotted rule above, then white | ▶ | gray boxes."""
    head = line1(115, 120, ly - 1, ly + 1)
    g.put(99.2, 553.0, R(y_head), R(y_box), [[S(mark + " ", 1090, True)] + runs_of(head)], frame(top="dot"),
          align="LEFT", line=1300)
    g.put(104.4, split, R(y_box), R(y_end), hang(left_lines, 110.3), frame(**BOX), align="LEFT", line=1450)
    g.put(split, arrow, R(y_box), R(y_end), "▶", size=800, color="#9A9A9A", fit=False)
    g.put(arrow, 547.9, R(y_box), R(y_end), hang(right_lines, right_lines[0]["bbox"][0]),
          frame("#E6E6E6", **BOX), align="LEFT", line=1450)


course(446.5, 454, 468.0, 504.0, 361.5, 370.0, lines_in(108, 112, 470, 500), lines_in(371, 374, 468, 500), "①")
course(504.0, 512, 527.3, 563.0, 325.0, 333.0, lines_in(108, 120, 530, 560), lines_in(334, 345, 530, 560), "②")
course(563.0, 571, 584.9, 620.0, 325.0, 333.0, lines_in(108, 112, 588, 618), lines_in(334, 337, 588, 618), "③")
g.put(99.2, 553.0, R(620.0), R(631.5), "▼", size=900, color="#A8A8A8", line=950)
g.put(104.4, 146.9, R(631.5), R(681.0), lines_in(115, 120, 642, 670), frame("#E3E3E3", top="soft", bottom="soft",
                                                                           left="soft"), line=1450)
g.put(150.2, 547.9, R(631.5), R(681.0), lines_in(150, 155, 634, 677), frame(top="soft", bottom="soft",
                                                                           right="soft"), align="LEFT", line=1450)

# 상시학습: hatched header with a dark tag, then two text boxes and the typed course grid
band = frame("#EEEEEE", hatch="#DDDDDD")
head = line1(74, 78, 693, 697)
g.put(59.5, 72.2, R(689.0), R(710.0), [], band)
g.put(72.2, 106.6, R(689.0), R(710.0), [runs_of(head, WHITE, x1=105.0)], frame("#6E6E6E"), line=1000)
tight(g, 72.2, R(689.0))
g.put(106.6, 553.0, R(689.0), R(710.0), [strip_runs(runs_of(head, x0=105.0))], band, align="LEFT", line=1300)
g.put(59.5, 314.9, R(713.6), R(799.0), hang(lines_in(64, 70, 718, 795), 65.4), frame(**BOX), align="LEFT",
      line=1550)
g.put(314.9, 328.8, R(713.6), R(799.0), "▶", size=1100, color="#B0B0B0", fit=False)
g.put(328.8, 451.1, R(713.6), R(799.0), hang(lines_in(333, 345, 718, 795), 334.7), frame("#E6E6E6", **BOX),
      align="LEFT", line=1550)
COURSES = (("인공지능", "AX 혁신", (("슈퍼앱 전성시대,", "너 하나면 돼!"), ("DX시대 협업지성", "-하드 스킬"),
                                   ("DX시대 협업지성", "-하이브리드 스킬")), "머신러닝/딥러닝"),
           ("생성형 AI", "AI 직무활용", (("AI로 쉽고 빠르게", "완성하는 데이터 시각화"),
                                       ("상상을 현실로! 미드저니", "실전 이미지 제작"), ("AI로 레벨업하는", "문서 작성 스킬")),
            "AI 활용 Biz Skill"))
for (a, e), (top, tab, items, bottom) in zip(((453.7, 501.0), (505.5, 553.0)), COURSES):
    for y0, y1, text, fill, color, bold in ((713.6, 725.0, top, "#E3E3E3", INK, True),
                                            (725.0, 738.0, tab, "#6E6E6E", WHITE, False),
                                            (789.0, 799.0, bottom, "#C8C8C8", INK, True)):
        g.put(a, e, R(y0), R(y1), text, frame(fill), size=760, bold=bold, color=color, ratio=80, line=840,
              fit=False)
        tight(g, a, R(y0), 40, 40)
    for (y0, y1), pair in zip(((738.0, 755.0), (755.0, 772.0), (772.0, 789.0)), items):
        g.put(a, e, R(y0), R(y1), [[S(t, 560)] for t in pair], frame(left="soft", right="soft", bottom="soft"),
              ratio=75, line=660, fit=False)
        tight(g, a, R(y0), 40, 40)
block(g, 408.1)

kit.finish(target, end=802.0)
