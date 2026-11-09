"""Rebuild KDN 2025 report page 127 (3rd PDF local page 27, printed page 87) as editable HWPX.

Usage: python3 work/kdn2025/p127.py <report3.pdf> <out.hwpx> [--page 27]

조직 및 인적자원관리, 평가내용 02 "합리적 조직･개인 성과평가시스템 구축을 위한 노력과 성과": section 1
(성과관리 운영체계 cycle: 제도 수립 -> 운영･모니터링 -> 평가･검증 -> 보상･환류) and section 2 (국정과제
조직 KPI). Built with the shared kit (one flat table per band on a grid of PDF x and y edges). All words
come from the PDF text layer except the typed chip "평가내용 02", the "Best Practice" sticker and the
circled numbers.

Images and how they are kept:
- 평가내용 chip (check icon dropped), section number bands, side tab: typed cells.
- cycle arrows between the four boxes -> ▶ ◀ ▲ ▼ connector cells; the round ↓ icon between
  내부환경 and 지표수립 -> a small '↓' line in the 지표수립 label; the big chevron -> ▼.
- 과제 ①/② boxes: the ① ② and the dotted arrow icon (-> '→') are images, typed.
- 평가 운영 ①-④ (image digits) -> ①-④ runs; Lv.1 / Lv.2 pills, 국정NN tags and department tags
  (text layer words on drawn pills) are separate cells; the tall chevron before the results -> ▶.
- 개선 (dark) / 신규 (outlined) boxes are separate cells.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kit  # noqa: E402
from kit import Layout, recipe_inputs  # noqa: E402

source, target = recipe_inputs(27, "합리적 조직")
L = Layout(top=3100)
kit.setup(source, L)
from kit import *  # noqa: E402,F401,F403  helpers and presets bound to this page

DARK, LABEL, HEAD = "#6A6A6A", "#E3E3E3", "#DCDCDC"
BOX = frame(WHITE, top="soft", bottom="soft", left="soft", right="soft")
TAG_DARK = frame("#7F7F7F")


def S(text, size=1090, bold=False, color=INK):
    return (text, size, bold, color)


def band(name, xs, ys):
    g = Grid(name, xs, [int(round((b - a) * 100)) for a, b in zip(ys, ys[1:])])
    g.ys = ys
    return g


def P(g, x0, x1, y0, y1, content, fill="1", pad=None, **kw):
    if pad is not None and kw.get("fit", True) and isinstance(content, list) and content:
        inner = ((x1 - x0) * 100 - 2 * pad - 60) / 100
        ratio = kw.pop("ratio", 90)
        for runs in content:
            need = text_width(runs, ratio)
            if need > inner:
                ratio = int(ratio * inner / need)
        kw.update(fit=False, ratio=ratio)
    g.put(x0, x1, g.ys.index(y0), g.ys.index(y1), content, fill, **kw)
    if pad is not None:
        key = (g.ys.index(y0), g.xs.index(to_x(x0)))
        item = g.items[key]
        g.items[key] = (*item[:7], dict(left=pad, right=pad, top=20, bottom=20))


def one(y, x0, x1=None):
    """The single line starting near x0 at PDF y."""
    return line1(x0 - 1, (x1 or x0 + 3), y - 1, y + 2)


def part(line, x0=-1e9, x1=1e9, color=INK):
    return strip_runs(runs_of(line, color, x0=x0, x1=x1))


# ---------------------------------------------------------------------------
# Page chrome (odd page): running head over a rule, side tab, footer at the right.
# ---------------------------------------------------------------------------
L.add_table([[cell(0, 3350, 1680, [para([("01", 1380, True, WHITE)], "CENTER")[0]], dark)],
             [cell(0, 3350, 5960, [para([(ch, 950, True, INK)], "CENTER", 1160)[0] for ch in "경영관리"], gray2)]],
            floating=(57800, 15000))
foot = [(text, size, False, INK) for text, size in (
    (line1(450, 455, 818, 822)["text"], 790), ("    ", 790), (line1(540, 546, 816, 820)["text"], 1090))]
L.add_table([[cell(0, W, 1500, [para(foot, "RIGHT", 1300)[0]])]], floating=(5660, 81550))

g = Grid("head", [X0, 381.3, X1], [1680])
g.put(X0, 381.3, 0, 1, [], frame(bottom="soft"))
g.put(381.3, X1, 0, 1, [line1(380, 385, 35, 40)], align="RIGHT")
block(g, 32.0)

# 평가내용 02 band: chip (image, typed) in the corner, hatched title.
g = Grid("band", [X0, 122.0, X1], [1360, 1500])
g.put(X0, 122.0, 0, 1, "평가내용 02", frame("#565656", top="strong"), size=970, bold=True, color=WHITE, ratio=80)
g.put(X0, 122.0, 1, 2, [], frame("#E9E9E9", bottom="soft", left="soft", hatch="#DADADA"))
g.put(122.0, X1, 0, 2, [line1(125, 130, 77, 80)], frame("#E9E9E9", top="strong", bottom="soft", right="soft",
                                                         hatch="#DADADA"), align="LEFT", line=1480)
block(g, 70.9)

g = Grid("sec1", [X0, 84.5, X1], [2300])
g.put(X0, 84.5, 0, 1, [runs_of(line1(60, 70, 113, 118), WHITE)], frame(DARK), line=1700)
g.put(84.5, X1, 0, 1, [line1(90, 95, 114, 118)], frame("#E6E6E6"), align="LEFT", line=1700)
block(g, 111.5)

# ---------------------------------------------------------------------------
# Section 1: four boxes in a cycle
# ---------------------------------------------------------------------------
xs = [X0, 86.4, 103.3, 160.0, 195.0, 298.7, 313.3, 329.9, 342.9, 365.3, 417.0, 452.0, 514.9, 530.5, 533.6,
      549.3, X1]
ys = [140.7, 158.1, 178.5, 195.5, 209.0, 225.3, 240.3, 257.4, 278.5, 296.0, 314.0, 332.0]
g = band("cycle", xs, ys)
SL = frame(LABEL, left="mid")
for a, e, y0, x in ((X0, 298.7, 140.7, 158), (313.3, X1, 140.7, 404), (X0, 298.7, 240.3, 157), (313.3, X1, 240.3, 413)):
    P(g, a, e, y0, ys[ys.index(y0) + 1], [line1(x - 1, x + 2, y0 + 3, y0 + 7)],
      frame(HEAD, top="mid", left="mid", right="mid", bottom="soft"), line=1250)
# 제도 수립
P(g, X0, 103.3, 158.1, 178.5, [one(168.2, 62.9)], SL)
P(g, X0, 103.3, 178.5, 195.5, [one(182.5, 62.9)], frame(LABEL, left="mid", bottom="dot"))
jipyo = one(207.0, 62.9)
P(g, X0, 103.3, 195.5, 225.3, [[S("↓", 700, True, "#8A8A8A")], part(jipyo, x1=100)],
  frame(LABEL, left="mid", bottom="mid"), line=None)
P(g, 103.3, 298.7, 158.1, 178.5, [one(167.0, 105.7)], frame(right="mid"), align="LEFT")
P(g, 103.3, 298.7, 178.5, 195.5, [one(183.6, 105.7)], frame(right="mid", bottom="dot"), align="LEFT")
P(g, 103.3, 298.7, 195.5, 225.3, [part(jipyo, x0=104)], frame(right="mid", bottom="mid"), align="LEFT")
# 운영･모니터링
kwan, jeom, jiwon = one(163.4, 320.2), one(180.1, 320.2), one(196.9, 320.2)
jiwon2 = one(210.5, 345.2)
P(g, 313.3, 342.9, 158.1, 178.5, [part(kwan, x1=340)], frame(LABEL, left="mid", bottom="dot"))
P(g, 313.3, 342.9, 178.5, 195.5, [part(jeom, x1=340)], frame(LABEL, left="mid", bottom="dot"))
P(g, 313.3, 342.9, 195.5, 225.3, [part(jiwon, x1=340)], frame(LABEL, left="mid", bottom="mid"))
P(g, 342.9, X1, 158.1, 178.5, [part(kwan, x0=343)], frame(right="mid", bottom="dot"), align="LEFT")
P(g, 342.9, X1, 178.5, 195.5, [part(jeom, x0=343)], frame(right="mid", bottom="dot"), align="LEFT")
P(g, 342.9, 530.5, 195.5, 209.0, [part(jiwon, x0=343, x1=532)], align="LEFT", line=1180)
P(g, 530.5, 549.3, 195.5, 209.0, [part(jiwon, x0=532, color=WHITE)], frame("#7F7F7F"), pad=0, fit=False, line=900)
P(g, 549.3, X1, 195.5, 209.0, [], frame(right="mid"))
P(g, 342.9, 530.5, 209.0, 225.3, [part(jiwon2, x1=532)], frame(bottom="mid"), align="LEFT", line=1250)
P(g, 530.5, 549.3, 209.0, 225.3, [part(jiwon2, x0=532)], BOX, pad=0, fit=False, line=900)
P(g, 549.3, X1, 209.0, 225.3, [], frame(right="mid", bottom="mid"))
P(g, 298.7, 313.3, 158.1, 225.3, "▶", size=1100, color="#BDBDBD", fit=False)
P(g, 160.0, 195.0, 225.3, 240.3, "▲", size=1000, color="#BDBDBD", line=1000)
P(g, 417.0, 452.0, 225.3, 240.3, "▼", size=1000, color="#BDBDBD", line=1000)
# 보상･환류
bosu, insa, hwan = one(264.1, 63.7), one(283.6, 63.7), one(303.1, 63.7)
for y0, y1, line, edge in ((257.4, 278.5, bosu, "dot"), (278.5, 296.0, insa, "dot")):
    P(g, X0, 86.4, y0, y1, [part(line, x1=86)], frame(LABEL, left="mid", bottom=edge))
    P(g, 86.4, 298.7, y0, y1, [part(line, x0=87)], frame(right="mid", bottom=edge), align="LEFT")
P(g, X0, 86.4, 296.0, 332.0, [part(hwan, x1=86)], frame(LABEL, left="mid", bottom="mid"))
P(g, 86.4, 298.7, 296.0, 332.0, [part(hwan, x0=87), runs_of(one(316.4, 88.7))], frame(right="mid", bottom="mid"),
  align="LEFT", line=1330)
P(g, 298.7, 313.3, 257.4, 332.0, "◀", size=1100, color="#BDBDBD", fit=False)
# 평가･검증
P(g, 313.3, 329.9, 257.4, 314.0, [[S(ch)] for ch in "조직평가"], frame(LABEL, left="mid", bottom="dot"), line=1100)
for y0, y1, (lx, ly), (cy, tag_x, dark_tag) in ((257.4, 278.5, (338.5, 264.4), (263.3, None, False)),
                                                 (278.5, 296.0, (338.5, 281.3), (281.1, None, False)),
                                                 (296.0, 314.0, (333.5, 298.4), (299.1, 530.5, False))):
    P(g, 329.9, 365.3, y0, y1, [one(ly, lx)], frame(LABEL, bottom="dot"))
    line = one(cy, 367.8)
    if tag_x:
        P(g, 365.3, tag_x, y0, y1, [part(line, x1=tag_x + 1)], frame(bottom="dot"), align="LEFT")
        P(g, tag_x, 549.3, y0, y1, [part(line, x0=tag_x + 1)], BOX, pad=0, fit=False, line=900)
        P(g, 549.3, X1, y0, y1, [], frame(right="mid", bottom="dot"))
    else:
        P(g, 365.3, X1, y0, y1, [line], frame(right="mid", bottom="dot"), align="LEFT")
personal = one(317.1, 322.2)
P(g, 313.3, 365.3, 314.0, 332.0, [part(personal, x1=362)], frame(LABEL, left="mid", bottom="mid"))
P(g, 365.3, 514.9, 314.0, 332.0, [part(personal, x0=362, x1=516)], frame(bottom="mid"), align="LEFT")
P(g, 514.9, 533.6, 314.0, 332.0, [part(personal, x0=516, color=WHITE)], frame("#7F7F7F"), pad=0, fit=False,
  line=900)
P(g, 533.6, X1, 314.0, 332.0, [], frame(right="mid", bottom="mid"))
block(g, 140.7)

g = Grid("cycle-caption", [X0, X1], [1450])
g.put(X0, X1, 0, 1, [line1(120, 130, 333, 337)], line=1150)
block(g, 333.5)

g = Grid("cycle-arrow", [X0, 294.7, 317.7, X1], [1360])
g.put(294.7, 317.7, 0, 1, "▼", size=1200, color="#9A9A9A", line=1200)
block(g, 348.5)

# 과제 ① / 과제 ② boxes
xs = [X0, 66.3, 101.0, 113.6, 303.7, 308.8, 318.4, 353.0, 365.7, X1]
g = Grid("tasks", xs, [2020])
for a, b, c, d, e, n, (lx, tx) in ((X0, 66.3, 101.0, 113.6, 303.7, "①", (67.9, 116.1)),
                                    (308.8, 318.4, 353.0, 365.7, X1, "②", (319.9, 376.1))):
    edge = dict(top="soft", bottom="soft")
    g.put(a, b, 0, 1, "→", frame(left="soft", **edge), size=800, color="#8A8A8A", fit=False)
    g.put(b, c, 0, 1, [runs_of(one(372.0, lx)) + [S(" " + n, 1090, True)]], frame(**edge), line=1250)
    g.put(c, d, 0, 1, [], frame(**edge))
    g.put(d, e, 0, 1, [one(372.0, tx)], frame("#E3E3E3", right="soft", **edge), line=1250)
block(g, 367.5)

# ---------------------------------------------------------------------------
# Section 2: 국정과제 조직 KPI
# ---------------------------------------------------------------------------
g = Grid("sec2", [X0, 84.5, 480.0, X1], [2300])
g.put(X0, 84.5, 0, 1, [runs_of(line1(60, 70, 408, 412), WHITE)], frame(DARK), line=1700)
g.put(84.5, 480.0, 0, 1, [line1(90, 95, 409, 413)], frame("#E6E6E6"), align="LEFT", line=1700)
g.put(480.0, X1, 0, 1, "Best Practice", frame("#4A4A4A"), size=900, bold=True, color=WHITE)
block(g, 406.1)

xs = [X0, 219.3, 234.3, 389.3, 404.3, 412.9, 441.7, X1]
ys = [436.0, 453.5, 473.5, 491.0]
g = band("kpi-boxes", xs, ys)
P(g, X0, 219.3, 436.0, 453.5, [one(440.4, 73.5)], frame(HEAD, top="mid", left="mid", right="mid"))
P(g, X0, 219.3, 453.5, 491.0, [runs_of(one(459.6, 62.5)), [S("   ")] + runs_of(one(475.0, 70.6))],
  frame(left="mid", right="mid", bottom="mid"), align="LEFT", line=1540)
P(g, 234.3, 389.3, 436.0, 453.5, [one(440.4, 242.6)], frame(HEAD, top="mid", left="mid", right="mid"))
P(g, 234.3, 389.3, 453.5, 491.0, [runs_of(one(459.6, 239.2)), [S("   ")] + runs_of(one(475.0, 247.2))],
  frame(left="mid", right="mid", bottom="mid"), align="LEFT", line=1540)
P(g, 219.3, 234.3, 453.5, 491.0, "▶", size=1100, color="#BDBDBD", fit=False)
P(g, 389.3, 404.3, 453.5, 491.0, "▶", size=1100, color="#BDBDBD", fit=False)
P(g, 404.3, X1, 436.0, 453.5, [runs_of(one(440.4, 420.1), WHITE)], frame("#7A7A7A", top="strong", left="strong",
                                                                          right="strong"))
for y0, y1, y in ((453.5, 473.5, 459.5), (473.5, 491.0, 475.2)):
    line = one(y, 418.9)
    P(g, 404.3, 412.9, y0, y1, [], frame(left="strong"))
    P(g, 412.9, 441.7, y0, y1, [part(line, x1=437)], BOX, pad=0, fit=False, line=1000)
    P(g, 441.7, X1, y0, y1, [part(line, x0=437)], frame(right="strong"), align="LEFT")
block(g, 436.0)

# Lower block: 관리 과정 / 평가 운영 / 이행 실적 (thick outer frame)
xs = [X0, 59.5, 85.1, 89.2, 114.2, 138.1, 142.9, 166.9, 289.3, 299.0, 303.6, 316.3, 332.1, 341.6, 377.0,
      405.8, 551.3, 553.2, X1]
ys = [491.0, 496.8, 515.6, 566.0, 570.5, 588.0, 625.5, 630.0, 648.0, 650.5, 667.5, 684.5, 701.5, 718.5, 735.5,
      752.5, 758.2]
g = band("kpi-ops", xs, ys)
P(g, X0, X1, 491.0, 496.8, [], frame(top="strong", left="strong", right="strong"))
P(g, X0, 59.5, 496.8, 752.5, [], frame(left="strong"))
P(g, 553.2, X1, 496.8, 752.5, [], frame(right="strong"))
P(g, X0, X1, 752.5, 758.2, [], frame(bottom="strong", left="strong", right="strong"))
for y0, y1, (a, b), fill in ((496.8, 566.0, (520, 534), "#E6E6E6"), (570.5, 625.5, (591, 605), "#D6D6D6"),
                             (630.0, 752.5, (684, 698), "#C8C8C8")):
    P(g, 59.5, 85.1, y0, y1, [line1(62, 64, a - 1, a + 2), line1(62, 64, b - 1, b + 2)], frame(fill), line=1320)
# 관리 과정
for a, p0, p1, e, y, fill in ((89.2, 138.1, 166.9, 299.0, 500.6, "#E6E6E6"), (316.3, 377.0, 405.8, 553.2, 500.6,
                                                                             "#D8D8D8")):
    head = one(y, p0 + 6.1, p1)
    P(g, a, p0, 496.8, 515.6, [], frame(fill))
    P(g, p0, p1, 496.8, 515.6, [part(head, x1=p1 - 3)], BOX, pad=0, fit=False, line=1000)
    P(g, p1, e, 496.8, 515.6, [part(head, x0=p1 - 3)], frame(fill), align="LEFT")
P(g, 299.0, 316.3, 496.8, 515.6, [], frame("#DFDFDF"))
P(g, 89.2, 299.0, 515.6, 566.0, lines_in(89, 91, 519, 562), frame(right="soft"), align="LEFT", line=1430)
P(g, 303.6, 553.2, 515.6, 566.0, lines_in(306, 308, 519, 562), align="LEFT", line=1430)
# 평가 운영
P(g, 89.2, 551.3, 570.5, 588.0, [one(574.1, 239.8)], frame(HEAD, top="mid", left="mid", right="mid"))
ops = [[S(n + " ")] + runs_of(one(y, x)) for n, y, x in (("①", 593.7, 104.3), ("③", 609.1, 104.3))]
P(g, 89.2, 303.6, 588.0, 625.5, ops, frame(left="mid", bottom="mid"), align="LEFT", line=1540)
ops = [[S(n + " ")] + runs_of(one(y, x)) for n, y, x in (("②", 593.7, 324.7), ("④", 609.1, 324.7))]
P(g, 303.6, 551.3, 588.0, 625.5, ops, frame(right="mid", bottom="mid"), align="LEFT", line=1540)
# 이행 실적
P(g, 89.2, 551.3, 630.0, 648.0, [one(633.5, 213.5)], frame(HEAD, top="mid", left="mid", right="mid"))
P(g, 89.2, 551.3, 648.0, 650.5, [], frame(left="mid", right="mid"))
rows = ((650.5, 667.5, 653.3, 653.4), (667.5, 684.5, 670.4, 670.4), (684.5, 701.5, 687.4, 687.4),
        (701.5, 718.5, 704.3, 704.4), (718.5, 735.5, 721.4, 721.4), (735.5, 752.5, 738.4, 735.7))
hatched = frame("#E8E8E8", left="mid", hatch="#D4D4D4")
P(g, 89.2, 114.2, 650.5, 701.5, [one(670.4, 91.2)], hatched, line=1250)
lv2 = one(721.4, 91.2)
P(g, 89.2, 114.2, 701.5, 718.5, [], hatched)
P(g, 89.2, 114.2, 718.5, 735.5, [part(lv2, x1=112)], hatched, line=1250)   # same row as 국정75: one text line
P(g, 89.2, 114.2, 735.5, 752.5, [], frame("#E8E8E8", left="mid", bottom="mid", hatch="#D4D4D4"))
for k, (y0, y1, ty, ry) in enumerate(rows):
    line = lv2 if k == 4 else one(ty, 116.1)
    edge = dict(bottom="mid") if k == 5 else {}
    P(g, 114.2, 142.9, y0, y1, [part(line, x0=115, x1=142)], frame("#D6D6D6", **edge), pad=10, line=1000)
    P(g, 142.9, 289.3, y0, y1, [part(line, x0=142, x1=289)], frame(**edge), align="LEFT", line=1250)
    if any(sp["bbox"][0] >= 289 and sp["text"].strip() for sp in line["spans"]):
        dept = part(line, x0=289, color=WHITE)
    else:
        dept = runs_of(line1(289, 300, ty - 1, ty + 2), WHITE)
    P(g, 289.3, 332.1, y0, y1, [dept], frame("#7F7F7F", **edge), pad=10, line=1000)
    P(g, 341.6, 551.3, y0, y1, [runs_of(one(ry, 344.0))], frame(right="mid", **edge), align="LEFT", line=1250, pad=80)
P(g, 332.1, 341.6, 650.5, 752.5, "▶", frame(bottom="mid"), size=900, color="#BDBDBD", fit=False)
block(g, 491.0)

# 주요성과 (two lines, the second indented)
g = Grid("result", [X0, 111.7, 114.5, X1], [3140])
g.put(X0, 111.7, 0, 1, [runs_of(line1(65, 70, 776, 780), WHITE)], frame(DARK))
g.put(114.5, X1, 0, 1, [runs_of(one(769.8, 117.8)), [S("  ")] + runs_of(one(785.3, 125.8))],
      frame(top="mid", bottom="mid", left="mid", right="mid"), align="LEFT", line=1450)
block(g, 767.4)

kit.finish(target, end=801.0)
