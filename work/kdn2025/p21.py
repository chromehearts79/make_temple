"""Rebuild KDN 2025 report physical PDF page 21 (printed page 9) as editable HWPX.

Usage: python3 work/kdn2025/p21.py <report.pdf> <out.hwpx> [--page N]

Dense diagram page "다. 전략체계 국정과제의 길 위에 실행의 속도를 더하는 한전KDN ‘2035 New Vision’".
Built with the shared kit: one flat table per band on a union grid whose rows are PDF y
edges, so cells of independent columns (labels, boxes, lists) each span the rows they cover.
Text comes from the PDF text layer; tags that are separate PDF spans (국정13, 1-1, AI, Energy,
E/S/G ...) become small bordered cells next to their text. Typed from images: the CEO
organisation chart (read from an 8x render), the "국정과제 → 미래성장" labels of the target
illustration (picture omitted), the boxed / circled / black-square numbers (as cells with
digits or ① ② ③), the "+" / chevron connectors, the "지적사항 개선" tag, the side tab and the
running chrome. The many-to-many arrows from the six 국정과제 to the four 전략방향 are drawn
as one ▶ connector.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kit  # noqa: E402
from kit import Layout, recipe_inputs  # noqa: E402

source, target = recipe_inputs(21, "국정과제의 길 위에 실행의 속도를 더하는")
L = Layout(top=3100)
kit.setup(source, L)
from kit import *  # noqa: E402,F401,F403  helpers and presets bound to this page

LABEL = "#E0E0E0"
BOX = frame(WHITE, top="soft", bottom="soft", left="soft", right="soft")


def ygrid(name, xs, ys):
    """Grid whose rows are given as PDF y edges (pt)."""
    g = Grid(name, xs, [int(round((b - a) * 100)) for a, b in zip(ys, ys[1:])])
    g.ys = list(ys)
    return g


def _row(g, y):
    k = min(range(len(g.ys)), key=lambda i: abs(g.ys[i] - y))
    if abs(g.ys[k] - y) > 0.01:
        raise ValueError(f"{g.name}: y {y} is not a row edge")
    return k


def yput(g, x0, x1, y0, y1, content, fill="1", **kw):
    g.put(x0, x1, _row(g, y0), _row(g, y1), content, fill, **kw)


def tight(g, x0, x1, y0, y1, pars, fill, line, pad=60):
    """Small org-chart box: narrow padding and 장평 fitted to that padding (kit assumes 500)."""
    width = (x1 - x0) * 100 - 2 * pad
    ratio = min(90, min(int(90 * width / 100 * 0.96 / text_width(r, 90)) for r in pars))
    if ratio < 55:
        WARN.append(f"{g.name}: ratio {ratio} for {pars[0][0][0]!r}")
    yput(g, x0, x1, y0, y1, pars, fill, ratio=max(ratio, 50), line=line, fit=False)
    key = (_row(g, y0), g.xs.index(kit.to_x(x0)))
    g.items[key] = g.items[key][:7] + (dict(left=pad, right=pad, top=40, bottom=40),)


# ---------------------------------------------------------------------------
# Page chrome (odd page): side tab, running head over a rule, footer at the right.
# ---------------------------------------------------------------------------
L.add_table([[cell(0, 3350, 1680, [para([("01", 1380, True, WHITE)], "CENTER")[0]], dark)],
             [cell(0, 3350, 5960, [para([(ch, 950, True, INK)], "CENTER", 1160)[0] for ch in "경영관리"], gray2)]],
            floating=(57800, 15000))
foot = [(t, size, False, INK) for t, size in (
    (line1(450, 455, 818, 822)["text"], 790), ("    ", 790), (line1(545, 552, 816, 820)["text"], 1090))]
L.add_table([[cell(0, W, 1500, [para(foot, "RIGHT", 1300)[0]])]], floating=(5660, 81550))

g = Grid("head", [X0, 466.3, X1], [1680])
g.put(X0, 466.3, 0, 1, [], frame(bottom="soft"))
g.put(466.3, X1, 0, 1, [line1(460, 480, 35, 40)], align="RIGHT")
block(g, 32.0)

title_band("title-da", line1(55, 60, 70, 74), [X0, 76.5, 131.0, X1], 70.5)

# ---------------------------------------------------------------------------
# 추진배경: 정부정책 + 한전KDN, target illustration (picture omitted, its two labels kept).
# ---------------------------------------------------------------------------
xs = [X0, 104.0, 108.0, 292.0, 322.0, 338.0, 370.0, X1]
g = ygrid("background", xs, [91.0, 112.5, 150.0])
yput(g, X0, 104.0, 91.0, 150.0, [line1(60, 65, 118, 122)], frame(LABEL, hatch="#D6D6D6"), bold=True)
yput(g, 108.0, 322.0, 91.0, 112.5, [line1(172, 175, 97, 101)], frame(top="mid", left="mid"), line=1300)
yput(g, 322.0, 338.0, 91.0, 112.5, "+", frame(top="mid"), size=1300, bold=True, color="#9A9A9A", fit=False)
yput(g, 338.0, X1, 91.0, 112.5, [line1(392, 395, 97, 101)], frame(top="mid", right="mid"), line=1300)
body = "#E8E8E8"
yput(g, 108.0, 292.0, 112.5, 150.0, lines_in(110, 116, 119, 140), frame(body, left="mid", bottom="mid"),
     line=1440)
yput(g, 292.0, 370.0, 112.5, 150.0, [[("국정과제", 700, True, "#555555"), (" → ", 700, False, "#555555"),
                                       ("미래성장", 700, True, "#555555")]], frame(body, bottom="mid"), line=900)
yput(g, 370.0, X1, 112.5, 150.0, lines_in(370, 390, 119, 140), frame(body, right="mid", bottom="mid"), line=1440)
block(g, 91.0)

# ---------------------------------------------------------------------------
# 국정과제 추진체계: CEO organisation chart (image) | 협업 bullets | 이행 실적 관리 bullets.
# ---------------------------------------------------------------------------
xs = [X0, 104.0, 108.0, 144.0, 157.5, 180.0, 185.0, 200.0, 216.0, 252.0, 262.0, 441.0, 445.0, 452.0, X1]
ys = [156.5, 179.0, 180.5, 191.0, 197.5, 209.5, 216.0, 233.0, 238.5]
g = ygrid("governance", xs, ys)
yput(g, X0, 104.0, 156.5, 238.5, lines_in(60, 65, 187, 215), frame(LABEL, hatch="#D6D6D6"), bold=True, line=1320)
yput(g, 108.0, 252.0, 156.5, 179.0, [line1(110, 112, 162, 166)], frame(bottom="soft"), line=1300)
for a, e in ((252.0, 262.0), (441.0, 452.0)):
    yput(g, a, e, 156.5, 179.0, "▶", frame("#D9D9D9" if a < 300 else "#BDBDBD"), size=800, color="#555555",
         fit=False, line=900)
yput(g, 262.0, 441.0, 156.5, 179.0, [line1(287, 290, 162, 166)], frame("#D9D9D9"), line=1300)
yput(g, 452.0, X1, 156.5, 179.0, [line1(470, 475, 162, 166)], frame("#BDBDBD"), line=1300)
# Organisation chart typed from the image; connecting lines omitted.
tight(g, 157.5, 200.0, 180.5, 191.0, [[("CEO", 950, True, WHITE)]], frame("#4A4A4A"), 880)
tight(g, 108.0, 180.0, 197.5, 209.5, [[("AX국정과제 추진TF", 780, False, INK)]], frame("#C8C8C8"), 900)
tight(g, 185.0, 252.0, 197.5, 209.5, [[("미래사업전략협의체", 780, False, INK)]], frame("#C8C8C8"), 900)
units = [("투자기획분과", "(기획관리본부장)"), ("DX/해외사업분과", "(ICT본부장)"),
         ("전력계통분과", "(전력지능화안전본부장)"), ("신재생E 분과", "(미래사업개발본부장)")]
for (a, e), (unit, head) in zip(((108.0, 144.0), (144.0, 180.0), (180.0, 216.0), (216.0, 252.0)), units):
    tight(g, a, e, 216.0, 233.0, [[(unit, 700, False, INK)], [(head, 520, False, INK)]], BOX, 720, pad=40)
mid = lines_in(255, 258, 183, 210) + [[("→ ", 1050, True, INK)] + runs_of(line1(270, 275, 218, 222))]
yput(g, 252.0, 445.0, 179.0, 238.5, mid, frame(right="dot"), align="LEFT", line=1760)
yput(g, 445.0, X1, 179.0, 238.5, lines_in(444, 447, 183, 225), align="LEFT", line=1760)
block(g, 156.5)

# ---------------------------------------------------------------------------
# 새정부 123대 국정과제 -> 중장기 경영전략 연계 -> 기관장 경영계약 6개 -> 4대 전략방향
# ---------------------------------------------------------------------------
xs = [X0, 64.0, 97.0, 104.0, 108.0, 163.0, 210.0, 212.0, 223.0, 225.0, 281.0, 283.5, 313.5, 431.0, 433.0,
      464.0, 466.7, 470.0, 480.0, 497.0, X1]
list_y = [254.5, 272.9, 291.2, 309.6, 327.9, 346.3, 364.6]
goal_y = [(276.0, 295.0), (298.0, 317.0), (320.5, 339.5), (342.5, 361.5)]
ys = sorted(set([250.0, 288.5, 301.0, 339.5] + list_y + [y for pair in goal_y for y in pair]))
g = ygrid("national-tasks", xs, ys)
hatch = frame(LABEL, hatch="#D6D6D6")
yput(g, X0, 104.0, 250.0, 288.5, [], hatch)
yput(g, X0, 64.0, 288.5, 301.0, [], hatch)
yput(g, 64.0, 97.0, 288.5, 301.0, [line1(65, 70, 289, 292)], frame("#5A5A5A"), color=WHITE, line=1000)
yput(g, 97.0, 104.0, 288.5, 301.0, [], hatch)
yput(g, X0, 104.0, 301.0, 339.5, lines_in(60, 70, 302, 320), hatch, bold=True, line=1320)
yput(g, X0, 104.0, 339.5, 364.6, [], hatch)
yput(g, 108.0, 163.0, 254.5, 364.6, lines_in(110, 160, 262, 352), frame("#D9D9D9", top="mid", left="mid",
                                                                       bottom="mid"), line=1430)
yput(g, 163.0, 210.0, 254.5, 364.6, lines_in(165, 205, 270, 345), frame(top="mid", right="mid", bottom="mid"),
     line=1540)
yput(g, 212.0, 223.0, 254.5, 364.6, "▶", size=1500, color="#9A9A9A", fit=False)
yput(g, 225.0, 281.0, 254.5, 364.6, lines_in(230, 275, 262, 352), frame("#D9D9D9", top="mid", left="mid",
                                                                       bottom="mid"), line=1430)
for k, (y0, y1) in enumerate(zip(list_y, list_y[1:])):
    line = line1(287, 290, y0 + 1, y0 + 5)
    edge = dict(top="mid" if k == 0 else None, bottom="mid" if k == 5 else "dot")
    yput(g, 281.0, 283.5, y0, y1, [], frame(**edge))
    yput(g, 283.5, 313.5, y0, y1, [runs_of(line, x1=300)], frame(WHITE, top="soft", bottom="soft", left="soft",
                                                                 right="soft"), line=1000)
    yput(g, 313.5, 431.0, y0, y1, [strip_runs(runs_of(line, x0=300))], frame(right="mid", **edge), align="LEFT",
         line=1250)
yput(g, 433.0, 464.0, 254.5, 364.6, "▶", size=1500, color="#9A9A9A", fit=False)
yput(g, 466.7, 470.0, 254.5, 364.6, [], frame(top="mid", left="mid", bottom="mid"))
head = line1(483, 485, 256, 260)
yput(g, 470.0, 497.0, 254.5, 272.9, [runs_of(head, x1=500)], frame(WHITE, top="mid", bottom="soft", left="soft",
                                                                  right="soft"), line=1000)
yput(g, 497.0, X1, 254.5, 272.9, [strip_runs(runs_of(head, x0=500))], frame(top="mid", right="mid"),
     align="LEFT", line=1250)
for k, (y0, y1) in enumerate(goal_y):
    yput(g, 470.0, 480.0, y0, y1, str(k + 1), frame("#3A3A3A"), size=1000, bold=True, color=WHITE, fit=False)
    yput(g, 480.0, X1, y0, y1, [line1(484, 486, y0 + 2, y0 + 6)], frame("#DCDCDC", right="mid"), align="LEFT",
         line=1250)
yput(g, 470.0, X1, 361.5, 364.6, [], frame(bottom="mid", right="mid"))
block(g, 250.0)

g = ygrid("linkage", [X0, X1], [364.6, 373.5, 405.5])
yput(g, X0, X1, 364.6, 373.5, "▼", size=800, color="#B4B4B4", line=700, fit=False)
yput(g, X0, X1, 373.5, 405.5, [line1(75, 80, 375, 379), line1(210, 215, 389, 393)], frame("#E6E6E6"), line=1400)
block(g, 364.6)

# ---------------------------------------------------------------------------
# 한전KDN 중장기 경영전략 체계: 비전연계 / 4대 전략방향 / 12대 전략과제 / 53개 실행과제 / KSF
# ---------------------------------------------------------------------------
C = [(156.0, 252.0), (256.0, 354.0), (358.0, 454.0), (458.0, X1)]
xs = [X0, 60.0, 101.0, 104.0, 108.0, 152.0, 156.0, 158.0, 170.0, 178.0, 183.0, 252.0, 256.0, 258.0, 272.0,
      278.0, 285.0, 354.0, 358.0, 372.0, 377.0, 390.0, 392.0, 406.0, 408.0, 430.0, 443.0, 454.0, 458.0, 474.0,
      479.0, 487.0, 499.0, 532.0, X1]
ys = [410.5, 436.5, 440.0, 474.5, 479.5, 499.5, 514.0, 517.0, 520.0, 530.5, 536.5, 552.0, 556.5, 571.0, 574.0,
      590.0, 594.0, 631.0, 634.0, 649.5, 676.5, 679.5]
g = ygrid("strategy-system", xs, ys)
side = frame(LABEL)
yput(g, X0, 104.0, 410.5, 517.0, [], side)
yput(g, X0, 60.0, 517.0, 530.5, [], side)
yput(g, 60.0, 101.0, 517.0, 530.5, [line1(62, 66, 518, 522)], frame("#5A5A5A"), color=WHITE, line=1000)
yput(g, 101.0, 104.0, 517.0, 530.5, [], side)
yput(g, X0, 104.0, 530.5, 571.0, lines_in(60, 75, 530, 565), side, bold=True, line=1290)
yput(g, X0, 104.0, 571.0, 679.5, [], side)
tag_fill = frame("#F0F0F0", top="soft")
for y0, y1, ly in ((410.5, 436.5, (418, 422)), (440.0, 474.5, (445, 470)), (479.5, 590.0, (520, 550)),
                   (594.0, 631.0, (600, 630))):
    yput(g, 108.0, 152.0, y0, y1, lines_in(108, 152, *ly), tag_fill, bold=True, line=1300)
# 비전연계: three outlined boxes, circled numbers are images.
for k, (a, e, x) in enumerate(((156.0, 252.0, 185), (256.0, 406.0, 300), (408.0, X1, 454))):
    yput(g, a, e, 410.5, 436.5, [[("①②③"[k] + " ", 1090, True, INK)] + runs_of(line1(x - 1, x + 2, 418, 422))],
         frame(top="mid", left="soft", right="soft", bottom="soft"), line=1300)
# 4대 전략방향: boxed number cell + bold title on a grey band.
for k, ((a, e), n0, n1, x) in enumerate(zip(C, (170.0, 272.0, 377.0, 474.0), (183.0, 285.0, 390.0, 487.0),
                                            (185, 286, 391, 488))):
    band = frame("#DCDCDC")
    yput(g, a, n0, 440.0, 474.5, [], band)
    yput(g, n0, n1, 440.0, 474.5, str(k + 1), frame(WHITE, top="soft", bottom="soft", left="soft", right="soft"),
         size=1000, bold=True, fit=False)
    yput(g, n1, e, 440.0, 474.5, [line1(x - 1, x + 2, 450, 454)], band, align="LEFT", line=1300)
# 12대 전략과제: tag cell (1-1 ...) + title on a grey band, description below.
tags = [(156.0, 158.0, 178.0, 252.0), (256.0, 258.0, 278.0, 354.0), (358.0, 372.0, 392.0, 454.0),
        (458.0, 479.0, 499.0, X1)]
for (t0, t1, b1), ty in zip(((479.5, 499.5, 514.0), (520.0, 536.5, 552.0), (556.5, 574.0, 590.0)),
                            (483.2, 522.3, 560.0)):
    for k, (a, s0, s1, e) in enumerate(tags):
        line = lines_in(a, e, ty - 1, ty + 2)
        assert len(line) == 1, line
        line = line[0]
        cut = line["spans"][1]["bbox"][0] - 0.5
        grey = frame("#E3E3E3")
        if s0 > a:
            yput(g, a, s0, t0, t1, [], grey)
        yput(g, s0, s1, t0, t1, [runs_of(line, x1=cut)], frame(WHITE, top="soft", bottom="soft", left="soft",
                                                              right="soft"), line=1000)
        if k == 2:   # 환경경영 E / 상생경영 S / 신뢰경영 G : the letter is a dark chip
            yput(g, s1, 430.0, t0, t1, [strip_runs(runs_of(line, x0=cut, x1=430))], grey, align="LEFT", line=1150)
            yput(g, 430.0, 443.0, t0, t1, [runs_of(line, x0=430)], frame("#7A7A7A"), color=WHITE, line=1000)
            yput(g, 443.0, e, t0, t1, [], grey)
        else:
            yput(g, s1, e, t0, t1, [strip_runs(runs_of(line, x0=cut))], grey, align="LEFT", line=1150)
        yput(g, a, e, t1, b1, lines_in(a, e, t1, b1), frame(bottom="soft"), line=1150)
# 53개 실행과제: four hatched boxes.
for a, e in C:
    yput(g, a, e, 594.0, 631.0, lines_in(a, e, 600, 620), frame("#EDEDED", top="soft", bottom="soft", left="soft",
                                                                 right="soft", hatch="#DEDEDE"), line=1300)
# KSF / KRI / KPI roadmap band with the "지적사항 개선" tag (image).
ksf = frame("#EDEDED")
yput(g, 108.0, 479.0, 634.0, 649.5, [line1(130, 135, 636, 640)], ksf, line=1250)
yput(g, 479.0, 532.0, 634.0, 649.5, "지적사항 개선", frame("#4A4A4A"), size=800, bold=True, color=WHITE, line=950)
yput(g, 532.0, X1, 634.0, 649.5, [], ksf)
yput(g, 108.0, X1, 649.5, 676.5, lines_in(110, 165, 650, 668), ksf, line=1220)
block(g, 410.5)

# ---------------------------------------------------------------------------
# 추진실적: two boxes joined by "+"; tags AI / Energy are their own cells.
# ---------------------------------------------------------------------------
xs = [X0, 104.0, 108.0, 121.5, 151.0, 325.0, 336.0, X1]
ys = [681.5, 701.0, 704.5, 719.5, 736.0, 758.5]
g = ygrid("results", xs, ys)
yput(g, X0, 104.0, 681.5, 758.5, [line1(60, 65, 718, 722)], frame(LABEL), bold=True)
yput(g, 108.0, 325.0, 681.5, 701.0, [line1(145, 147, 686, 690)], frame(top="mid", left="mid"), line=1300)
yput(g, 325.0, 336.0, 681.5, 701.0, "+", frame(top="mid"), size=1300, bold=True, color="#9A9A9A", fit=False)
yput(g, 336.0, X1, 681.5, 701.0, [line1(362, 365, 686, 690)], frame(top="mid", right="mid"), line=1300)
yput(g, 108.0, 151.0, 701.0, 704.5, [], frame(left="mid"))
yput(g, 108.0, 121.5, 704.5, 719.5, [line1(112, 115, 705, 708)], frame(left="mid"), line=1200)
yput(g, 121.5, 151.0, 704.5, 719.5, [line1(130, 135, 706, 709)], BOX, line=1000)
yput(g, 151.0, 325.0, 704.5, 719.5, [strip_runs(runs_of(line1(150, 152, 705, 708)))], align="LEFT", line=1250)
energy = line1(112, 115, 720, 724)
yput(g, 108.0, 121.5, 719.5, 736.0, [runs_of(energy, x1=121)], frame(left="mid"), line=1200)
yput(g, 121.5, 151.0, 719.5, 736.0, [runs_of(energy, x0=121, x1=150)], BOX, line=1000)
yput(g, 151.0, 325.0, 719.5, 736.0, [strip_runs(runs_of(energy, x0=150))], align="LEFT", line=1250)
yput(g, 336.0, X1, 701.0, 736.0, lines_in(337, 340, 704, 725), frame(right="mid"), align="LEFT", line=1540)
yput(g, 108.0, 325.0, 736.0, 758.5, [line1(130, 135, 741, 745)], frame("#E3E3E3", left="mid", bottom="mid"),
     line=1300)
yput(g, 336.0, X1, 736.0, 758.5, [line1(360, 365, 741, 745)], frame("#E3E3E3", right="mid", bottom="mid"),
     line=1300)
block(g, 681.5)

# 추진성과: one box, two bullet columns.
g = ygrid("outcomes", [X0, 104.0, 108.0, 331.0, X1], [763.0, 801.0])
yput(g, X0, 104.0, 763.0, 801.0, [line1(60, 65, 780, 784)], frame("#BDBDBD"), bold=True)
yput(g, 108.0, 331.0, 763.0, 801.0, lines_in(112, 115, 770, 790), frame("#F2F2F2", top="soft", bottom="soft",
                                                                      left="soft", right="dot"), align="LEFT",
     line=1540)
yput(g, 331.0, X1, 763.0, 801.0, lines_in(335, 338, 770, 790), frame("#F2F2F2", top="soft", bottom="soft",
                                                                     right="soft"), align="LEFT", line=1540)
block(g, 763.0)

kit.finish(target, end=803.0)
