"""Rebuild KDN 2025 report physical PDF page 27 (printed page 15) as editable HWPX.

Usage: python3 work/kdn2025/p27.py <report.pdf> <out.hwpx> [--page N]

'2 전사 혁신 내재화 ... 혁신과제 추진체계의 전면적 재정비': 가. org chart + 주요 개선사항, 나. 추진배경 /
정의 / 추진방식 (INNO-CATION), 다. 동기부여·보상 table and 주요성과 box. Every band is one flat
table on the kit's union grid. Text comes from the PDF text layer, except the 혁신 추진조직 체계
org chart (an image in the PDF; its text was read from a 4x render and is typed) and the circled
①②③ of the title pills and the round arrow icons (images; typed as ① ② ③ / ▶). The tree
lines of the org chart are drawn with cell borders.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kit  # noqa: E402
from kit import Layout, recipe_inputs  # noqa: E402

source, target = recipe_inputs(27, "전사 혁신 내재화 및 우수성과 창출을 위한 혁신과제 추진체계의 전면적 재정비")
L = Layout(top=3100)
kit.setup(source, L)
from kit import *  # noqa: E402,F401,F403  helpers and presets bound to this page

HEADFILL, LINE = "#D9D9D9", "#8A8A8A"


def tight(g, x0, r0, left=60, right=60):
    """Narrow the padding of the cell whose top-left slot is (x0, row r0)."""
    c0 = g.xs.index(to_x(x0))
    item = g.items[r0, c0]
    g.items[r0, c0] = (*item[:7], dict(left=left, right=right))


def fit_ratio(runs, width_pt, pad_pt=1.6, cap=90):
    return min(cap, int(cap * (width_pt - pad_pt) * 0.96 / text_width(runs, cap)))


def indent(line, x_bullet):
    """Continuation lines (no bullet) are indented under the bullet text, as in the PDF."""
    runs = runs_of(line)
    if line["bbox"][0] > x_bullet + 3:
        runs = [("  ", runs[0][1], False, INK)] + runs
    return runs


def subtitle(name, num_y, line, edges, top, mark, split):
    """'가. [① 조직체계 혁신] title': number, light pill (circled number is an image), title."""
    g = Grid(name, edges, [1650])
    g.put(edges[0], edges[1], 0, 1, [line1(55, 60, num_y - 2, num_y + 2)], align="LEFT", line=1450)
    g.put(edges[1], edges[2], 0, 1, [[(mark + " ", 1090, True, INK)] + runs_of(line, x1=split)], pill)
    g.put(edges[2], X1, 0, 1, [runs_of(line, x0=split)], align="LEFT", line=1450)
    block(g, top)


# ---------------------------------------------------------------------------
# Page chrome (odd page): side tab, footer, running head
# ---------------------------------------------------------------------------
L.add_table([[cell(0, 3350, 1680, [para([("01", 1380, True, WHITE)], "CENTER")[0]], dark)],
             [cell(0, 3350, 5960, [para([(ch, 950, True, INK)], "CENTER", 1160)[0] for ch in "경영관리"], gray2)]],
            floating=(57800, 15000))
foot = [(only_text, size, False, INK) for only_text, size in (
    (line1(450, 455, 818, 822)["text"], 790), ("    ", 790), (line1(540, 546, 816, 820)["text"], 1090))]
L.add_table([[cell(0, W, 1500, [para(foot, "RIGHT", 1300)[0]])]], floating=(5660, 81550))

g = Grid("head", [X0, 466.3, X1], [1680])
g.put(X0, 466.3, 0, 1, [], frame(bottom="soft"))
g.put(466.3, X1, 0, 1, [line1(460, 480, 35, 40)], align="RIGHT")
block(g, 32.0)

g = Grid("section-2", [X0, 85.6, X1], [2300])
g.put(X0, 85.6, 0, 1, [line1(60, 70, 70, 76)["text"]], frame("#5E5E5E"), size=1700, bold=True, color=WHITE)
g.put(85.6, X1, 0, 1, [line1(85, 95, 70, 76)], frame("#E4E4E4"), align="LEFT")
block(g, 70.9)

# ---------------------------------------------------------------------------
# 가. 조직체계 혁신
# ---------------------------------------------------------------------------
subtitle("title-ga", 101.0, line1(95, 100, 99, 103), [X0, 76.9, 162.9, X1], 99.8, "①", 160.0)

# Left: 혁신 추진조직 체계 (image in the PDF). Right: 주요 개선사항 (text layer, 신설 tags boxed).
left_xs = [X0, 61.5, 86.5, 111.5, 119.2, 123.0, 131.0, 148.5, 174.0, 177.0, 180.0, 183.0, 185.5, 211.0, 229.0,
           236.5, 241.8, 248.5, 274.5, 300.5, 302.6]
TAG0, TAG1 = 346.3, 368.5
right_xs = [310.3, TAG0, TAG1, X1]
groups = [(141.0, 149.0, 164.0, 179.0, 185.4), (185.4, 191.5, 206.5, 221.5, 228.0),
          (228.0, 234.0, 249.0, 264.0, 270.5), (270.5, 276.5, 291.5, 306.5, 314.6)]
ys = sorted({122.7, 141.0, 145.0, 159.5, 167.5, 182.0, 191.5, 202.5, 217.5, 234.0, 242.5, 264.0, 273.5,
             288.5, 310.5, 314.6} | {y for grp in groups for y in grp})
g = Grid("organization", left_xs + right_xs, [int(round((b - a) * 100)) for a, b in zip(ys, ys[1:])])
r = ys.index
TOP, END = r(141.0), r(314.6)
line_mid = dict(top="mid")
# Left panel frame.
g.put(X0, 302.6, 0, TOP, [line1(140, 145, 125, 130)], frame(HEADFILL, top="strong", left="mid", right="mid",
                                                              bottom="soft"))
g.put(X0, 61.5, TOP, r(310.5), [], frame(left="mid"))
g.put(300.5, 302.6, TOP, r(310.5), [], frame(right="mid"))
g.put(X0, 302.6, r(310.5), END, [], frame(left="mid", right="mid", bottom="mid"))
chair = frame("#4E4E4E", hatch="#5E5E5E")
g.put(131.0, 229.0, r(145.0), r(159.5), "혁신위원장(기관장)", chair, size=1000, bold=True, color=WHITE, line=1150)
g.put(131.0, 180.0, r(159.5), r(167.5), [], frame(right="mid"))
g.put(131.0, 229.0, r(167.5), r(182.0), "혁신책임관(기획관리본부장)", chair, size=1000, bold=True, color=WHITE,
      line=1150)
g.put(131.0, 180.0, r(182.0), r(191.5), [], frame(right="mid"))
for (a, b), last in (((86.5, 148.5), False), ((148.5, 211.0), False), ((211.0, 274.5), True)):
    g.put(a, b, r(191.5), r(202.5), [], frame(top="mid", left="mid", right="mid" if last else None))
    g.put(a, b, r(234.0), r(242.5), [], frame(bottom="mid", left="mid", right="mid" if last else None))
units = [((61.5, 111.5), "AX·DX 혁신", "IT운영사업처장"), ((123.0, 174.0), "에너지전환 혁신", "ICT기획처장"),
         ((185.5, 236.5), "ESG 혁신", "ESG경영처장"), ((248.5, 300.5), "경영시스템 혁신", "기획처장")]
box = dict(top="soft", bottom="soft", left="soft", right="soft")
unit_ratio = min(fit_ratio([(t, 920, False, INK)], b - a) for (a, b), *texts in units for t in texts)
for (a, b), head, name in units:
    g.put(a, b, r(202.5), r(217.5), head, frame(HEADFILL, **box), size=920, ratio=unit_ratio, fit=False, line=1100)
    g.put(a, b, r(217.5), r(234.0), name, frame(**box), size=920, ratio=unit_ratio, fit=False, line=1100)
    tight(g, a, r(202.5))
    tight(g, a, r(217.5))
g.put(61.5, 180.0, r(242.5), r(264.0), "참여·협업", frame(right="mid"), align="RIGHT", size=1000)
g.put(180.0, 300.5, r(242.5), r(264.0), "협의·자문", align="LEFT", size=1000)
g.put(119.2, 180.0, r(264.0), r(273.5), [], frame(top="mid", left="mid"))
g.put(180.0, 241.8, r(264.0), r(273.5), [], frame(top="mid", right="mid"))
networks = [((61.5, 177.0), "혁신 소통채널", ["(외부) 국민제안 혁신 DESK, SNS 등", "(내부) INNO-CATION, 혁신제안시스템 등"]),
            ((183.0, 300.5), "혁신 네트워크", ["(외부) 품질분임조자문그룹, ESG자문단 등", "(내부) 미래사업전략협의회, ESG위원회 등"])]
for (a, b), head, lines in networks:
    g.put(a, b, r(273.5), r(288.5), head, frame(top="soft", left="soft", right="soft"), size=1050, line=1200)
    ratio = min(fit_ratio([(t, 820, False, INK)], b - a, pad_pt=1.6) for t in lines)
    g.put(a, b, r(288.5), r(310.5), lines, frame("#EFEFEF", bottom="soft", left="soft", right="soft"),
          align="LEFT", size=820, ratio=ratio, line=920, fit=False)
    tight(g, a, r(288.5), left=100)
# Right panel.
g.put(310.3, X1, 0, TOP, [line1(400, 405, 125, 130)], frame(HEADFILL, top="strong", left="mid", right="mid",
                                                            bottom="soft"))
for k, (g0, p1, m, p2, g1) in enumerate(groups):
    last = k == len(groups) - 1
    g.put(310.3, TAG0, r(g0), r(g1), lines_in(310, 346, g0 + 2, g1),
          frame("#EDEDED", hatch="#E0E0E0", left="mid", bottom="mid" if last else None), line=1300)
    g.put(TAG0, X1, r(g0), r(p1), [], frame(right="mid"))
    for ln, (a, e) in zip(lines_in(348, 352, g0, g1), ((p1, m), (m, p2))):
        g.put(TAG0, TAG1, r(a), r(e), [runs_of(ln, x1=369.0)], frame(WHITE, **{k: "mid" for k in box}),
              ratio=90, fit=False, line=1000)
        tight(g, TAG0, r(a))
        g.put(TAG1, X1, r(a), r(e), [runs_of(ln, x0=369.0)], frame(right="mid"), align="LEFT", line=1250)
    g.put(TAG0, X1, r(p2), r(g1), [], frame(right="mid", bottom="mid" if last else "dot"))
block(g, 122.7)

# ---------------------------------------------------------------------------
# 나. 이행체계 혁신
# ---------------------------------------------------------------------------
subtitle("title-na", 326.7, line1(94, 98, 325, 329), [X0, 75.4, 161.3, X1], 325.4, "②", 163.0)

g = Grid("background", [X0, 111.7, X1], [3990])
g.put(X0, 111.7, 0, 1, [line1(65, 70, 360, 365)], frame("#D5D5D5", top="mid", bottom="mid", left="mid"))
g.put(111.7, X1, 0, 1, lines_in(115, 120, 350, 385), frame(top="mid", bottom="mid", right="mid"), align="LEFT",
      line=1500)
block(g, 348.5)

g = Grid("need", [X0, X1], [1450, 1250])
g.put(X0, X1, 0, 1, [line1(170, 175, 390, 395)], frame("#F2F2F2"), line=1150)
g.put(X0, X1, 1, 2, "▼", size=1000, color="#9A9A9A", line=1050)
block(g, 390.0)

# 정의: dark brand box on a rule, hatched definition band.
g = Grid("definition", [X0, 93.7, 96.4, 198.5, 453.6, X1], [2000, 370, 2180])
g.put(X0, 93.7, 0, 3, [line1(62, 70, 435, 440)], frame("#E6E6E6", top="mid"))
g.put(96.4, 198.5, 0, 1, [], frame(top="mid"))
g.put(198.5, 453.6, 0, 1, [line1(205, 215, 422, 427)], frame("#6E6E6E"), color=WHITE, line=1250)
g.put(453.6, X1, 0, 1, [], frame(top="mid"))
g.put(96.4, X1, 2, 3, [line1(135, 145, 447, 452)], frame("#ECECEC", hatch="#DCDCDC"), line=1250)
block(g, 420.2)

# 추진방식: three stage headers with ▶ connectors, bullet columns below.
xs = [X0, 93.7, 96.4, 108.0, 145.0, 247.9, 250.9, 262.7, 269.0, 306.5, 402.7, 405.4, 417.7, 451.0, X1]
g = Grid("method", xs, [1870, 3610, 330])
g.put(X0, 93.7, 0, 3, lines_in(62, 70, 486, 505), frame("#E6E6E6", top="mid"), line=1300)
stage = frame("#E6E6E6")
tagf = frame(WHITE, **{k: "soft" for k in box})
for lead, p0, p1, e, x in ((96.4, 108.0, 145.0, 247.9, 117.0), (262.7, 269.0, 306.5, 402.7, 277.0),
                           (None, 417.7, 451.0, X1, 423.0)):
    ln = line1(x, x + 2, 474, 477)
    split = x + 20.0       # '1단계' / '2단계' / '3단계' span ends before this x
    if lead is not None:
        g.put(lead, p0, 0, 1, [], stage)
    g.put(p0, p1, 0, 1, [runs_of(ln, x1=split)], tagf, line=1000)
    g.put(p1, e, 0, 1, [runs_of(ln, x0=split)], stage, align="LEFT", line=1250)
for a, e in ((247.9, 262.7), (402.7, 417.7)):
    g.put(a, e, 0, 1, "▶", size=900, color="#8A8A8A", fit=False)
for k, (a, e, x) in enumerate(((96.4, 250.9, 99.0), (250.9, 405.4, 253.0), (405.4, X1, 408.0))):
    lines = lines_in(x, x + 10, 494, 525)
    g.put(a, e, 1, 2, [indent(ln, x) for ln in lines], frame(right="dot" if k < 2 else None, bottom="mid"),
          align="LEFT", line=1500)
block(g, 471.8)

# ---------------------------------------------------------------------------
# 다. 보상체계 혁신
# ---------------------------------------------------------------------------
subtitle("title-da", 541.8, line1(95, 100, 540, 544), [X0, 76.9, 162.9, X1], 540.7, "③", 164.0)

T0, T1, T2, T3 = 113.4, 178.6, 201.0, 419.5
ys = [563.6, 582.0, 599.4, 614.8, 632.3, 649.7, 667.2, 686.7, 704.1, 721.5, 741.0]
g = Grid("reward-table", [X0, T0, T1, T2, T3, X1], [int(round((b - a) * 100)) for a, b in zip(ys, ys[1:])])
r = ys.index
headf = frame(HEADFILL, top="mid", bottom="soft")
g.put(X0, T0, 0, 1, [line1(70, 75, 565, 570)], headf)
g.put(T0, T1, 0, 1, [line1(130, 135, 565, 570)], headf)
g.put(T1, T3, 0, 1, [line1(255, 260, 565, 570)], headf)
g.put(T3, X1, 0, 1, [line1(460, 465, 565, 570)], frame("#7F7F7F", top="strong", left="strong", right="strong",
                                                       bottom="soft"), color=WHITE)
kind = frame("#ECECEC", bottom="soft", right="soft")
for y0, y1, lines in ((582.0, 686.7, [line1(60, 65, 627, 632)]), (686.7, 721.5, lines_in(60, 110, 688, 720)),
                      (721.5, 741.0, [line1(60, 70, 724, 728)])):
    g.put(X0, T0, r(y0), r(y1), lines, kind, line=1300)
for y0, y1, (x, y) in ((582.0, 632.3, (115, 600)), (632.3, 667.2, (130, 642)), (667.2, 686.7, (130, 670)),
                       (686.7, 721.5, (130, 697)), (721.5, 741.0, (130, 724))):
    g.put(T0, T1, r(y0), r(y1), [line1(x, x + 10, y, y + 4)], frame(bottom="soft", right="soft"))
group_end = {632.3, 667.2, 686.7, 721.5, 741.0}
for ln in lines_in(180, 185, 584, 740):
    y = ln["bbox"][1]
    y0 = max(v for v in ys if v <= y + 1)
    y1 = ys[ys.index(y0) + 1]
    tag = runs_of(ln, x1=199.5)
    new = tag[0][0] == "신규"
    g.put(T1, T2, r(y0), r(y1), [[(t, s, b, WHITE if new else INK) for t, s, b, _ in tag]],
          frame("#7F7F7F" if new else WHITE, top="soft" if new else "mid", bottom="soft" if new else "mid",
                left="soft" if new else "mid", right="soft" if new else "mid"),
          ratio=90, fit=False, line=1000)
    tight(g, T1, r(y0))
    g.put(T2, T3, r(y0), r(y1), [runs_of(ln, x0=199.5)], frame(bottom="soft" if y1 in group_end else None),
          align="LEFT", line=1250)
for y0, y1, last in ((582.0, 686.7, False), (686.7, 721.5, False), (721.5, 741.0, True)):
    lines = lines_in(420, 440, y0 + 1, y1)
    g.put(T3, X1, r(y0), r(y1), [indent(ln, 422.5) for ln in lines],
          frame(left="strong", right="strong", bottom="strong" if last else "soft"), align="LEFT",
          line=1600 if len(lines) > 2 else 1350)
block(g, 563.6)

g = Grid("results", [X0, 111.7, X1], [5340])
g.put(X0, 111.7, 0, 1, [line1(65, 70, 766, 772)], frame("#6E6E6E", top="mid", bottom="mid", left="mid"),
      color=WHITE)
g.put(111.7, X1, 0, 1, lines_in(115, 120, 750, 800), frame(top="mid", bottom="mid", right="mid"), align="LEFT",
      line=1500)
block(g, 747.6)

kit.finish(target, end=803.0)
