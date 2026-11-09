"""Rebuild KDN 2025 report physical PDF page 31 (printed page 19) as editable HWPX.

Usage: python3 work/kdn2025/p31.py <report.pdf> <out.hwpx> [--page N]

Dense last page of the 전략기획 indicator: "6 경영시스템 혁신" band, 혁신과제 ⑦ (two boxes, two
적극행정 사례 with 주요성과 strips) and 혁신과제 ⑧ (R&R table + 중점과제 keyword table, four
improvement cases). Built with the shared kit: one flat table per horizontal band on PDF x
edges, rows at the PDF y positions; the two small tables use the PDF's own vector rule positions.

All text is in the PDF text layer. Image-only fragments are typed: the ❼ ❽ ① ② number marks
(-> ⑦ ⑧ ① ②), the "지적사항 개선" tags, the circled arrow between the R&R and 중점과제 boxes (-> ▶),
the bold result arrows (-> →), the chevron between 추진배경 and 혁신 포인트 (-> ▶) and the side tab.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kit  # noqa: E402
from kit import Layout, recipe_inputs  # noqa: E402

source, target = recipe_inputs(31, "생산적 업무문화 확산을 위한 경영시스템 혁신")
L = Layout(top=3200)
kit.setup(source, L)
from kit import *  # noqa: E402,F401,F403  helpers and presets bound to this page

T = "soft"
BOX = frame(bottom=T, left=T, right=T)
DARK_PILL = frame("#5E5E5E")
HATCH_PILL = frame("#E2E2E2", hatch="#CBCBCB")
TAG = frame("#3C3C3C")
RESULT_LABEL = frame("#5A5A5A")
RESULT_BOX = frame(top=T, bottom=T, right=T)
SIDE_LABEL = frame("#E6E6E6")


def body_lines(x0, x1, y0, y1, indent="  "):
    """Bullet lines as run lists; continuation and '-' lines get the source's indent."""
    out = []
    for line in lines_in(x0, x1, y0, y1):
        runs = runs_of(line)
        if not runs[0][0].startswith("∙"):
            runs = [(indent, runs[0][1], False, INK)] + runs
        out.append(runs)
    return out


def put_tight(g, x0, x1, r0, r1, content, fill="1", **kw):
    """Cell without top/bottom padding, for 10 pt keyword rows that hold 8.9 pt text."""
    n = len(WARN)
    g.put(x0, x1, r0, r1, content, fill, **kw)
    del WARN[n:]
    key = (r0, g.xs.index(to_x(x0)))
    g.items[key] = g.items[key][:7] + (dict(top=0, bottom=0),)


# ---------------------------------------------------------------------------
# Page chrome (odd page): side tab and footer float; running head over a rule.
# ---------------------------------------------------------------------------
L.add_table([[cell(0, 3350, 1680, [para([("01", 1380, True, WHITE)], "CENTER")[0]], dark)],
             [cell(0, 3350, 5960, [para([(ch, 950, True, INK)], "CENTER", 1160)[0] for ch in "경영관리"], gray2)]],
            floating=(57800, 15000))
foot = [(text, size, False, INK) for text, size in (
    (line1(450, 455, 818, 822)["text"], 790), ("    ", 790), (line1(540, 546, 816, 820)["text"], 1090))]
L.add_table([[cell(0, W, 1500, [para(foot, "RIGHT", 1300)[0]])]], floating=(5660, 81550))

g = Grid("head", [X0, 466.3, X1], [1680])
g.put(X0, 466.3, 0, 1, [], frame(bottom="soft"))
g.put(466.3, X1, 0, 1, [line1(465, 475, 35, 40)], align="RIGHT")
block(g, 32.0)

# 6 [경영시스템 혁신] 생산적 업무문화 확산을 위한 경영시스템 혁신
band_line = line1(95, 100, 74, 78)
g = Grid("section", [X0, 86.0, 89.5, 175.0, X1], [2300])
g.put(X0, 86.0, 0, 1, [runs_of(line1(64, 70, 72, 76), WHITE)], frame("#5A5A5A"), line=1800)
g.put(86.0, 89.5, 0, 1, [], frame("#E1E1E1"))
g.put(89.5, 175.0, 0, 1, [runs_of(band_line, WHITE, x1=175.0)], DARK_PILL)
g.put(175.0, X1, 0, 1, [runs_of(band_line, x0=175.0)], frame("#E1E1E1"), align="LEFT", line=1700)
block(g, 70.9)

# ---------------------------------------------------------------------------
# 가. 혁신과제 ⑦
# ---------------------------------------------------------------------------
ga = line1(55, 60, 99, 103)
g = Grid("title-ga", [X0, 78.0, 137.0, 503.0, X1], [1750])
g.put(X0, 78.0, 0, 1, [runs_of(ga, x1=77.0)], align="LEFT", line=1550)
g.put(78.0, 137.0, 0, 1, [runs_of(ga, x0=77.0) + [(" ⑦", 1100, True, INK)]], HATCH_PILL)
g.put(137.0, 503.0, 0, 1, [line1(130, 140, 99, 103)], align="LEFT", line=1550)
g.put(503.0, X1, 0, 1, "지적사항 개선", TAG, size=780, bold=True, color=WHITE)
block(g, 99.5)

# Two boxes: 1 조직/제도 혁신 | 2 교육･홍보 강화
xs = [X0, 75.2, 305.4, 308.5, 325.9, X1]
g = Grid("boxes", xs, [1450, 8100])
for a, b, e, nx in ((X0, 75.2, 305.4, 63), (308.5, 325.9, X1, 314)):
    g.put(a, b, 0, 1, [line1(nx, nx + 2, 126, 130)], frame("#D5D5D5", top=T, left=T, right=T), bold=True)
    g.put(b, e, 0, 1, [line1(b + 2, b + 8, 126, 130)], frame("#D5D5D5", top=T, right=T), align="LEFT")
g.put(X0, 305.4, 1, 2, body_lines(58, 300, 144, 218), BOX, align="LEFT", line=1430)
g.put(308.5, X1, 1, 2, body_lines(310, 555, 144, 218), BOX, align="LEFT", line=1430)
block(g, 125.6)

# 적극행정 사례 ①: 추진배경 ▶ 혁신 포인트, then 주요성과
case = line1(60, 65, 232, 236)
g = Grid("case-1", [X0, 128.0, X1], [1560])
g.put(X0, 128.0, 0, 1, [runs_of(case) + [(" ①", 1000, False, INK)]], HATCH_PILL)
g.put(128.0, X1, 0, 1, [line1(129, 132, 231, 235)], align="LEFT", line=1400)
block(g, 230.4)

g = Grid("case-1-body", [X0, 252.0, 268.0, X1], [1450, 3620])
g.put(X0, 252.0, 0, 1, [line1(135, 140, 255, 259)], frame("#D9D9D9", top=T, left=T, right=T))
g.put(268.0, X1, 0, 1, [runs_of(line1(385, 390, 255, 259), WHITE)], frame("#6E6E6E", top=T, left=T, right=T))
g.put(X0, 252.0, 1, 2, body_lines(58, 250, 272, 303), BOX, align="LEFT", line=1430)
g.put(252.0, 268.0, 1, 2, "▶", size=1100, color=ARROW, fit=False)
g.put(268.0, X1, 1, 2, body_lines(270, 555, 272, 303), BOX, align="LEFT", line=1430)
block(g, 254.8)

g = Grid("result-1", [X0, 112.5, X1], [3550])
g.put(X0, 112.5, 0, 1, [runs_of(line1(64, 70, 320, 325), WHITE)], RESULT_LABEL)
g.put(112.5, X1, 0, 1, body_lines(115, 120, 313, 340), RESULT_BOX, align="LEFT", line=1550)
block(g, 311.0)

# 적극행정 사례 ②: 중소기업 지원 | 기업성장응답센터, then 주요성과
case = line1(60, 65, 357, 361)
g = Grid("case-2", [X0, 128.0, 466.0, 522.0, X1], [1560])
g.put(X0, 128.0, 0, 1, [runs_of(case) + [(" ②", 1000, False, INK)]], HATCH_PILL)
g.put(128.0, 466.0, 0, 1, [line1(129, 132, 356, 360)], align="LEFT", line=1400)
g.put(466.0, 522.0, 0, 1, "지적사항 개선", TAG, size=780, bold=True, color=WHITE)
block(g, 355.4)

g = Grid("case-2-body", [X0, 305.4, 307.5, X1], [1830, 4590])
g.put(X0, 305.4, 0, 1, [line1(150, 155, 381, 385)], frame(top=T), bold=True)
g.put(307.5, X1, 0, 1, [line1(390, 400, 381, 385)], frame(top=T), bold=True)
g.put(X0, 305.4, 1, 2, body_lines(58, 300, 397, 440), frame("#EDEDED"), align="LEFT", line=1430)
g.put(307.5, X1, 1, 2, body_lines(309, 555, 404, 432), frame("#EDEDED"), align="LEFT", line=1330)
block(g, 377.0)

g = Grid("result-2", [X0, 112.5, X1], [2350])
g.put(X0, 112.5, 0, 1, [runs_of(line1(64, 70, 452, 456), WHITE)], RESULT_LABEL)
g.put(112.5, X1, 0, 1, body_lines(115, 120, 451, 456), RESULT_BOX, align="LEFT")
block(g, 447.0)

# ---------------------------------------------------------------------------
# 나. 혁신과제 ⑧
# ---------------------------------------------------------------------------
na = line1(55, 60, 481, 485)
g = Grid("title-na", [X0, 78.0, 140.1, X1], [1750])
g.put(X0, 78.0, 0, 1, [runs_of(na, x1=77.0)], align="LEFT", line=1550)
g.put(78.0, 140.1, 0, 1, [runs_of(na, x0=77.0) + [(" ⑧", 1100, True, INK)]], HATCH_PILL)
g.put(140.1, X1, 0, 1, [line1(138, 142, 481, 485)], align="LEFT", line=1550)
block(g, 480.5)

# 경평 지적사항 분류: R&R table (left) ▶ 중점과제 도출 (right); rules at the PDF's vector positions.
RX = [90.7, 114.4, 175.0, 235.6, 296.2, 356.8]
KX = [365.6, 403.3, 445.9, 488.5, 531.1, 552.7]
xs = [X0, 85.2] + RX + [KX[0], 368.6, 388.5] + KX[1:] + [X1]
hs = [390, 1450, 400, 1570, 1290, 270, 930, 360, 930, 1000, 620, 380, 2300, 410]   # y 503.0 .. 626.0
g = Grid("rnr", xs, hs)
g.put(X0, 85.2, 0, 14, lines_in(58, 85, 535, 595), SIDE_LABEL, line=1320)
g.put(90.7, 356.8, 1, 2, [line1(145, 150, 507, 511)], frame("#D0D0D0", top=T, left=T, right=T), bold=True)
g.put(356.8, 365.6, 1, 2, "▶", size=900, color="#7A7A7A", fit=False)
g.put(365.6, 552.7, 1, 2, [line1(428, 432, 507, 511)], frame("#D0D0D0", top=T, left=T, right=T), bold=True)


def grid_cell(edges, k, last_row, fill=None):
    return frame(fill, bottom=None if last_row else T, right=T if k < len(edges) - 2 else None)


# R&R table rows: (row span, y window, fill of the first column)
for r0, r1, y0, y1, last in ((3, 4, 526, 532, False), (4, 6, 542, 548, False), (6, 8, 557, 562, False),
                             (8, 11, 570, 594, False), (11, 13, 596, 620, True)):
    for k in range(5):
        a, e = RX[k], RX[k + 1]
        items = lines_in(a - 4 if k else a, e, y0, y1)
        fill = "#E1E1E1" if r0 == 3 else ("#F2F2F2" if k == 0 else None)
        fr = frame(fill, bottom=None if last else T) if r0 == 6 else grid_cell(RX, k, last, fill)
        g.put(a, e, r0, r1, items, fr, line=1030 if r0 >= 8 else None)
# 중점과제 도출: 1st / 2nd / 3rd steps, then the keyword table.
for r0, r1, y in ((3, 4, 527), (4, 5, 539), (5, 7, 552)):
    step = line1(368, 375, y, y + 3)
    g.put(368.6, 388.5, r0, r1, [runs_of(step, x1=388.0)], frame(top=T, bottom=T, left=T, right=T),
          line=1030 if r0 > 3 else None)
    g.put(388.5, X1, r0, r1, [runs_of(step, x0=388.0)], align="LEFT", line=1030 if r0 > 3 else None)
for r0, r1, y0, y1, last in ((7, 9, 567, 572, False), (9, 10, 579, 584, False), (10, 12, 589, 594, False),
                             (12, 13, 600, 615, True)):
    for k in range(5):
        a, e = KX[k], KX[k + 1]
        items = lines_in(a + 1 if k else a, e, y0, y1)
        fill = "#E1E1E1" if r0 == 7 else ("#F2F2F2" if k == 0 else None)
        fr = grid_cell(KX, k, last, fill)
        if r0 in (9, 10):
            put_tight(g, a, e, r0, r1, items, fr, line=1000)
        else:
            g.put(a, e, r0, r1, items, fr, line=1030)
block(g, 503.0)

# 지적사항 주요개선사례: four cases (pill title, two-column mini table, → result line)
xs = [X0, 85.2, 87.9, 100.0, 130.4, 203.7, 319.5, 323.9, 336.0, 366.4, 439.7, X1]
hs = [410, 1560, 280, 1560, 1560, 1680, 590, 1560, 280, 1560, 1560, 1750, 400]   # y 630.0 .. 777.5
g = Grid("cases", xs, hs)
g.put(X0, 85.2, 0, 13, lines_in(58, 85, 665, 740), SIDE_LABEL, line=1320)
sub_head = frame("#CCCCCC", right=T)
for (a, p, m, e), (t0, h0, v0, res0) in (
        ((87.9, 130.4, 203.7, 319.5), (1, 3, 4, 5)), ((323.9, 366.4, 439.7, X1), (1, 3, 4, 5)),
        ((87.9, 130.4, 203.7, 319.5), (7, 9, 10, 11)), ((323.9, 366.4, 439.7, X1), (7, 9, 10, 11))):
    y = 636.4 if t0 == 1 else 708.7
    title = line1(a + 2, a + 5, y - 1, y + 1)
    g.put(a, p, t0, t0 + 1, [runs_of(title, WHITE, x1=a + 40)], frame("#6E6E6E"))
    g.put(p, e, t0, t0 + 1, [runs_of(title, x0=a + 40)], align="LEFT", line=1400)
    hy, vy = (654, 668) if t0 == 1 else (726, 742)
    g.put(a, m, h0, h0 + 1, lines_in(a, m - 4, hy, hy + 4), frame("#CCCCCC", right=T), bold=True)
    g.put(m, e, h0, h0 + 1, lines_in(m - 4, e, hy, hy + 4), frame("#CCCCCC"), bold=True)
    g.put(a, m, v0, v0 + 1, lines_in(a, m - 4, vy, vy + 5), frame(bottom=T, right=T))
    g.put(m, e, v0, v0 + 1, lines_in(m - 4, e, vy, vy + 5), frame(bottom=T))
    ry = 685.2 if t0 == 1 else 759.0
    result = runs_of(line1(a + 10, a + 16, ry - 1, ry + 1))
    result = [(text.replace("시행  채용", "시행 → 채용"), *rest) for text, *rest in result]
    g.put(a, a + 12.1, res0, res0 + 1, "→", size=1200, bold=True, color="#8C8C8C", fit=False)
    g.put(a + 12.1, e, res0, res0 + 1, [result], align="LEFT", line=1400)
block(g, 630.0)

g = Grid("result-3", [X0, 112.5, X1], [2150])
g.put(X0, 112.5, 0, 1, [runs_of(line1(64, 70, 784, 788), WHITE)], RESULT_LABEL)
g.put(112.5, X1, 0, 1, body_lines(115, 120, 784, 788), RESULT_BOX, align="LEFT")
block(g, 780.5)

kit.finish(target, end=802.0)
