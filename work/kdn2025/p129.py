"""Rebuild KDN 2025 report page 129 (3rd PDF local page 29, printed page 89) as editable HWPX.

Usage: python3 work/kdn2025/p129.py <report3.pdf> <out.hwpx> [--page 29]

조직 및 인적자원관리, 평가내용 03 opening page (sections 1 and 2). Built with the shared kit
(one flat table per horizontal band on a grid of PDF x edges). All running text, the step heads,
the small score tables and the 개선 / 직원 / 대리 ... tags come from the PDF text layer.

Images and how they are kept:
- 평가내용 03 chip (check mark dropped), side tab, footer: typed / text layer as usual.
- the "KDN 경력개발체계 기반 ... 개선과제 도출" diagram (y 205-447) is one image: its text was read
  from 4x renders and typed into cells on the diagram's own grid (HRM column | 경력·역량개발 체계 |
  HRD column). Rounded pills -> gray cells, the HRM / HRD circles -> outlined cells, the
  '유기적 연계' ring -> an outlined cell, the side arrows -> ◀ ▶, dashed frames -> dotted borders.
- round arrow badges between the 단계 heads -> ▶ connector cells.
- the 추천 교육과정 screenshot (y 691-752) -> one photo cell.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kit  # noqa: E402
from kit import Layout, recipe_inputs  # noqa: E402

source, target = recipe_inputs(29, "구성원의 역량 및 직무 전문성 제고를 위한 노력과 성과")
L = Layout(top=3100)
kit.setup(source, L)
from kit import *  # noqa: E402,F401,F403  helpers and presets bound to this page

DARK, LABEL = "#6A6A6A", "#E5E5E5"
TAG = frame("#7F7F7F")
BOXED = frame(WHITE, top="soft", bottom="soft", left="soft", right="soft")
PILL = frame(WHITE, top="soft", bottom="soft", left="soft", right="soft")
D = 1050               # diagram body text (image, typed)
SM = 850               # small parentheticals in the diagram


def S(text, size=D, bold=False, color=INK):
    return (text, size, bold, color)


def tight(g, x0, r0, left=0, right=0):
    c0 = g.xs.index(to_x(x0))
    item = g.items[r0, c0]
    g.items[r0, c0] = (*item[:7], dict(left=left, right=right))


def hang(lines, base):
    """Bullet lines keep their PDF indent: spaces for the x offset from the bullet."""
    out = []
    for l in lines:
        runs = runs_of(l) if isinstance(l, dict) else l[1]
        x = l["bbox"][0] if isinstance(l, dict) else l[0]
        n = max(0, round((x - base) / (0.29 * runs[0][1] / 100)))
        out.append([(" " * n, runs[0][1], False, INK)] + runs if n else runs)
    return out


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

# 평가내용 03 band: dark chip (image, typed; check mark dropped) over a hatched strip.
g = Grid("band", [X0, 124.0, X1], [1750, 1110])
g.put(X0, 124.0, 0, 1, [[("평가내용 ", 800, True, WHITE), ("03", 1350, True, WHITE)]],
      frame("#565656", top="mid", left="mid"), line=1500)
g.put(X0, 124.0, 1, 2, [], frame("#E9E9E9", bottom="mid", left="mid", hatch="#DADADA"))
g.put(124.0, X1, 0, 2, [line1(125, 130, 76, 80)], frame("#E9E9E9", top="mid", bottom="mid", right="mid",
                                                       hatch="#DADADA"), align="LEFT", line=1450)
block(g, 70.9)

g = Grid("sec1", [X0, 84.5, X1], [2300])
g.put(X0, 84.5, 0, 1, [runs_of(line1(64, 70, 112, 116), WHITE)], frame(DARK), line=1700)
g.put(84.5, X1, 0, 1, [line1(90, 95, 113, 118)], frame("#E6E6E6"), align="LEFT", line=1700)
block(g, 111.5)

# 현황분석: hatched label, two boxes (bold head, gray body with two bullets each).
xs = [X0, 105.4, 107.6, 330.5, 333.0, X1]
g = Grid("status", xs, [1880, 4000])
g.put(X0, 105.4, 0, 2, [line1(60, 65, 164, 168)], frame("#E6E6E6", hatch="#D6D6D6"))
for a, e in ((107.6, 330.5), (333.0, X1)):
    g.put(a, e, 0, 1, [line1(a, e, 145, 150)], frame(top="strong", left="mid", right="mid"))
    g.put(a, e, 1, 2, lines_in(a, e, 165, 195), frame("#EBEBEB", bottom="mid", left="mid", right="mid"),
          align="LEFT", line=1550)
block(g, 140.8)

# ---------------------------------------------------------------------------
# Diagram (image in the PDF; text typed from 4x renders)
# ---------------------------------------------------------------------------
COL, PL = "#EDEDED", "#D6D6D6"          # side columns, their rounded pills
CH, CB = "#D2D2D2", "#E6E6E6"           # center gray boxes: head, body
xs = [X0, 80.0, 163.5, 178.5, 183.0, 271.0, 293.5, 297.5, 304.0, 308.5, 331.0, 418.5, 423.5, 441.0, 528.0, X1]
# y: 205.5 title | 224.5 heads | 250.5 | 257 | 269 | 280 | 291 | 324 | 329 | 348 | 386 | 392 | 412 | 444 | 447
hs = [1900, 2600, 650, 1200, 1100, 1100, 3300, 500, 1900, 3800, 600, 2000, 3200, 300]
g = Grid("diagram", xs, hs)
g.put(X0, X1, 0, 1, [[S("“ ", 1250, True), S("KDN 경력개발체계 기반 분야별 직무 전문성 제고 개선과제 도출", 1250, True),
                      S(" ”", 1250, True)]], line=1450)
# left column (HRM) and right column (HRD)
ring = frame(WHITE, top="mid", bottom="mid", left="mid", right="mid")
g.put(X0, 80.0, 1, 2, "HRM", ring, size=1000, bold=True, fit=False)
tight(g, X0, 1)
g.put(80.0, 163.5, 1, 2, "직무중심 인사운영", frame(PL), size=1150, bold=True)
g.put(441.0, 528.0, 1, 2, "직무전문 인재양성", frame(PL), size=1150, bold=True)
g.put(528.0, X1, 1, 2, "HRD", ring, size=1000, bold=True, fit=False)
tight(g, 528.0, 1)
side = {
    (X0, 163.5): [
        ((2, 3), [], None),
        ((3, 5), "직무경력관리 고도화", "pill"),
        ((5, 7), [[S("新 직무관리 활용")], [S("직무관리시스템 개선")]], None),
        ((7, 9), "직군별 직무관리 강화", "pill"),
        ((9, 11), [[S("직무 적합도 및 업무 특성")], [S("고려한 적소적재 인력배치")], [S("(보직 · 전보)", SM)]], None),
        ((11, 12), "인사혁신과제 완수", "pill"),
        ((12, 13), [[S("특별승진 ·인사교류 ·")], [S("개방형직위 시행")]], None),
        ((13, 14), [], None)],
    (441.0, X1): [
        ((2, 3), [], None),
        ((3, 5), "역량 맞춤 교육 운영", "pill"),
        ((5, 7), [[S("역량진단기반 개발")], [S("필요역량 향상")], [S("교육 추천")]], None),
        ((7, 9), "미래산업 선도 AI 인재육성", "pill"),
        ((9, 11), [[S("AI 인재육성 체계 구축")], [S("및 대상별 맞춤,")], [S("교육 신설")]], None),
        ((11, 12), "경영전략 연계 교육체계", "pill"),
        ((12, 13), [[S("2035 전략방향에 따른")], [S("교육체계 재편")]], None),
        ((13, 14), [], None)]}
for (a, e), items in side.items():
    for (r0, r1), content, kind in items:
        if kind == "pill":
            g.put(a, e, r0, r1, content, frame(PL), size=1100, line=1300)
        else:
            g.put(a, e, r0, r1, content, frame(COL), line=1400)
g.put(163.5, 178.5, 7, 11, "◀", size=1100, color="#555555", fit=False)
g.put(423.5, 441.0, 7, 11, "▶", size=1100, color="#555555", fit=False)
# center: hatched header, two dotted frames with three gray boxes each, '유기적 연계' ring
g.put(178.5, 423.5, 1, 2, "KDN 특화 경력 · 역량개발 체계", frame("#EEEEEE", hatch="#DDDDDD"), size=1150)
FA, FB = (178.5, 183.0, 293.5, 297.5), (304.0, 308.5, 418.5, 423.5)
for (f0, b0, b1, f1), title in ((FA, "인사운영제도"), (FB, "교육훈련 프로그램")):
    g.put(f0, f1, 2, 4, title, frame(top="dot", left="dot", right="dot"), size=1150, bold=True, line=1300)
    for r0, r1 in ((4, 7), (7, 8), (8, 10), (10, 11), (11, 13)):
        if r0 in (8,):
            continue
        g.put(f0, b0, r0, r1, [], frame(left="dot"))
        g.put(b1, f1, r0, r1, [], frame(right="dot"))
    g.put(f0, f1, 13, 14, [], frame(bottom="dot"))
    g.put(b0, b1, 7, 8, [], frame())
    g.put(b0, b1, 10, 11, [], frame())
g.put(178.5, 183.0, 8, 10, [], frame(left="dot"))
g.put(418.5, 423.5, 8, 10, [], frame(right="dot"))
boxes = [((183.0, 293.5), 4, 6, "인재 채용", [[S("직무수행능력평가"), S("(필기)", SM)], [S("비중 및 면접 강화")]]),
         ((308.5, 418.5), 4, 6, "개인별 역량 개발", [[S("개인별 미흡역량 중심")], [S("커리큘럼 설정")]]),
         ((183.0, 271.0), 8, 9, "직무중심 전보관리", [[S("직무별 전문성 고려")], [S("전보관리 시행")]]),
         ((331.0, 418.5), 8, 9, "직무전문 역량 개발", [[S("직무전문 특화")], [S("프로그램 설계 및 운영")]]),
         ((183.0, 293.5), 11, 12, "업무성과 보상", [[S("성과에 따른 포상 및")], [S("승진 시행"), S("(연공성↓)", SM)]]),
         ((308.5, 418.5), 11, 12, "역량개발 효과측정", [[S("교육생 니즈 반영 및")], [S("현업적용 중심교육")]])]
for (a, e), r0, r1, head, body in boxes:
    g.put(a, e, r0, r1, head, frame(CH), size=1100, line=1300)
    g.put(a, e, r1, r1 + 1, body, frame(CB), line=1400)
g.put(271.0, 331.0, 8, 10, [[S("유기적", 1150, True)], [S("연계", 1150, True)]], ring, line=1350)
block(g, 205.5)

g = Grid("sec2", [X0, 84.5, X1], [2300])
g.put(X0, 84.5, 0, 1, [runs_of(line1(64, 70, 465, 470), WHITE)], frame(DARK), line=1700)
g.put(84.5, X1, 0, 1, [line1(90, 95, 466, 470)], frame("#E6E6E6"), align="LEFT", line=1700)
block(g, 463.1)


# ---------------------------------------------------------------------------
# Section 2 rows: gray label column | content
# ---------------------------------------------------------------------------
def steps(g, r, y, segs, fills):
    """Step heads: [lead gray][pill 'N단계'][title gray] per segment, ▶ between segments.
    segs: (band start, pill start, pill end, band end, arrow end or None)."""
    for (b0, p0, p1, b1, arr), fill in zip(segs, fills):
        ln = line1(p0, p1, y - 1, y + 2)
        if p0 > b0:
            g.put(b0, p0, r, r + 1, [], frame(fill))
        g.put(p0, p1, r, r + 1, [runs_of(ln, x1=p1 - 1)], PILL, line=1000, fit=False)
        tight(g, p0, r)
        g.put(p1, b1, r, r + 1, [strip_runs(runs_of(ln, x0=p1 - 1))], frame(fill), align="LEFT", line=1300)
        if arr:
            g.put(b1, arr, r, r + 1, "▶", size=900, color="#8C8C8C", fit=False)


def tag(g, a, e, r, ln, color=WHITE, fill=TAG):
    g.put(a, e, r, r + 1, [runs_of(ln, color, x0=a - 1, x1=e)], fill, line=1000, fit=False)
    tight(g, a, r)


C1, C2, C3 = (110.5, 258.2), (258.2, 407.8), (407.8, X1)
STEP_FILLS = ("#E6E6E6", "#DCDCDC", "#D0D0D0")

# 직무중심 지원체계 (y 492.3-586.1)
xs = [X0, 107.7, 110.5, 116.2, 145.0, 255.1, 258.2, 272.0, 275.6, 304.4, 332.3, 351.1, 405.3, 407.8, 419.8,
      422.5, 451.3, 533.7, 552.5, X1]
g = Grid("support", xs, [2020, 1750, 1650, 1670, 2290])
g.put(X0, 107.7, 0, 5, lines_in(60, 70, 525, 555), frame(LABEL))
steps(g, 0, 497, ((110.5, 116.2, 145.0, 255.1, 272.0), (272.0, 275.6, 304.4, 405.3, 419.8),
                  (419.8, 422.5, 451.3, X1, None)), STEP_FILLS)
sep = dict(right="soft")
last = dict(bottom="mid")
g.put(*C1, 1, 5, hang(lines_in(110, 125, 515, 580), 113.6), frame(**sep, **last), align="LEFT", line=1650)
g.put(*C2, 1, 2, hang([line1(262, 264, 516, 520)], 263.2), frame(**sep), align="LEFT")
l2 = line1(270, 272, 533, 537)
g.put(258.2, 332.3, 2, 3, hang([(l2["bbox"][0], runs_of(l2, x1=333.0))], 263.2), frame(), align="LEFT")
tag(g, 332.3, 351.1, 2, l2)
g.put(351.1, 407.8, 2, 3, [], frame(**sep))
g.put(*C2, 3, 5, hang(lines_in(262, 272, 550, 580), 263.2), frame(**sep, **last), align="LEFT", line=1650)
g.put(*C3, 1, 4, hang(lines_in(412, 422, 515, 564), 412.9), frame(), align="LEFT", line=1630)
l4 = line1(420, 422, 566, 570)
g.put(407.8, 533.7, 4, 5, hang([(l4["bbox"][0], runs_of(l4, x1=535.0))], 412.9), frame(**last), align="LEFT")
tag(g, 533.7, 552.5, 4, l4)
g.put(552.5, X1, 4, 5, [], frame(**last))
block(g, 492.3)

# 경력개발 경로예시 (y 590.8-632.1): gray head, path line with outlined rank tags
T = ((130.3, 149.1), (232.5, 251.3), (314.3, 333.1), (432.5, 451.3))
xs = [X0, 107.7, 110.5] + [x for t in T for x in t] + [X1]
g = Grid("path", xs, [1920, 2210])
g.put(X0, 107.7, 0, 2, lines_in(60, 70, 598, 626), frame(LABEL))
g.put(110.5, X1, 0, 1, [line1(240, 245, 594, 598)], frame("#E6E6E6", top="soft", left="soft", right="soft"))
ln = line1(130, 135, 614, 618)
box = dict(bottom="soft")
g.put(110.5, 130.3, 1, 2, [], frame(left="soft", **box))
for k, (a, e) in enumerate(T):
    g.put(a, e, 1, 2, [runs_of(ln, x0=a, x1=e - 1)], frame(WHITE, top="soft", bottom="soft", left="soft",
                                                     right="soft"), line=1000, fit=False)
    tight(g, a, 1)
    nxt = T[k + 1][0] if k < 3 else X1
    g.put(e, nxt, 1, 2, [strip_runs(runs_of(ln, x0=e - 1, x1=nxt - 1))], frame(right="soft" if k == 3 else None, **box),
          align="LEFT")
block(g, 590.8)

# 개인역량 개발 프로그램 (y 636.8-757.5): step heads, bullets, two score tables and a screenshot
TA = (112.4, 180.4, 254.1)
TB = (262.1, 310.3, 341.4, 372.6, 403.8)
xs = sorted({X0, 107.7, 110.5, 139.1, 167.9, 255.1, 258.2, 272.0, 293.6, 322.4, 405.3, 407.8, 413.1, 419.8,
             442.4, 471.2, 552.0, X1} | set(TA) | set(TB))
g = Grid("program", xs, [2020, 1700, 1720, 1560, 1520, 1510, 1510, 530])
g.put(X0, 107.7, 0, 8, lines_in(60, 75, 676, 718), frame(LABEL), line=1300)
steps(g, 0, 642, ((110.5, 139.1, 167.9, 255.1, 272.0), (272.0, 293.6, 322.4, 405.3, 419.8),
                  (419.8, 442.4, 471.2, X1, None)), STEP_FILLS)
g.put(*C1, 1, 3, hang(lines_in(112, 125, 658, 690), 113.6), frame(**sep), align="LEFT", line=1550)
g.put(*C2, 1, 3, hang(lines_in(262, 275, 658, 690), 263.2), frame(**sep), align="LEFT", line=1550)
g.put(*C3, 1, 3, hang(lines_in(412, 425, 658, 690), 412.9), frame(), align="LEFT", line=1550)
thead = frame("#E5E5E5", bottom="soft")
for k, (a, e) in enumerate(zip(TA, TA[1:])):
    vr = dict(right="soft") if k == 0 else {}
    for r, y in enumerate((694, 709.5, 724.5, 739.6), 3):
        g.put(a, e, r, r + 1, [line1(a, e, y - 3, y + 2)], frame("#E5E5E5" if r == 3 else None, bottom="soft", **vr),
              size=990, line=1150)
for k, (a, e) in enumerate(zip(TB, TB[1:])):
    vr = dict(right="soft") if k < 3 else {}
    for r, y in enumerate((694, 709.5, 724.5, 739.6), 3):
        hits = lines_in(a, e, y - 1, y + 2)
        g.put(a, e, r, r + 1, hits, frame("#E5E5E5" if r == 3 else None, bottom="soft", **vr), line=1150)
g.put(110.5, 112.4, 3, 7, [])
g.put(254.1, 258.2, 3, 7, [], frame(**sep))
g.put(258.2, 262.1, 3, 7, [])
g.put(403.8, 407.8, 3, 7, [], frame(**sep))
g.put(407.8, 413.1, 3, 7, [])
g.put(413.1, 552.0, 3, 7, [], photo)
g.put(552.0, X1, 3, 7, [])
g.put(110.5, X1, 7, 8, [], frame(bottom="mid"))
block(g, 636.8)

# 환류계획 (y 762.2-802.2)
g = Grid("feedback", [X0, 107.7, 110.5, X1], [4000])
g.put(X0, 107.7, 0, 1, [line1(60, 70, 776, 780)], frame(LABEL))
g.put(110.5, X1, 0, 1, lines_in(114, 120, 766, 790), frame(top="mid", bottom="mid", left="mid", right="mid"),
      align="LEFT", line=1550)
block(g, 762.2)

kit.finish(target, end=802.5)
