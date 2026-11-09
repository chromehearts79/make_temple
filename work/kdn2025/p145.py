"""Rebuild KDN 2025 report page 145 (3rd PDF local page 45, printed page 102) as editable HWPX.

Usage: python3 work/kdn2025/p145.py <report3.pdf> <out.hwpx> [--page 45]

조직 운영 및 관리(노사관계) 평가내용 03 opening page: section 1 "노사협력을 통한 합리적 교섭으로
근로조건의 실질적 개선 성과 창출", 가. 임금협약 Step1-4 diagram with 상생기반 갈등해소 / 책임있는 교섭 /
추진성과, 나. 「행복한 일터」 three columns, 주요성과. Built with the shared kit (one flat table per
horizontal band on a grid of PDF x edges). All running text, labels, Step pills and the 소통 / 협력 /
합의 / 회사 / 노조 tags come from the PDF text layer; tags are separate cells.

Images and how they are kept:
- running head rule, side tab, 평가내용 03 chip (check icon dropped), section number band, the
  'Best Practice' sticker (trophy dropped): typed cells.
- the Step chevrons of the left column -> graded gray label cells; the gray chevron arrows between
  boxes and the round arrow icons in the head bands -> ▶ connector cells; the small chevrons in
  나. -> ▼; the circled numbers of the 우선순위 line -> ① ② ③.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kit  # noqa: E402
from kit import Layout, recipe_inputs  # noqa: E402

source, target = recipe_inputs(45, "노사협력을 통한 합리적 교섭으로 근로조건의 실질적 개선")
L = Layout(top=3100)
kit.setup(source, L)
from kit import *  # noqa: E402,F401,F403  helpers and presets bound to this page

DARK, HEAD, BODYGRAY = "#6A6A6A", "#D9D9D9", "#EBEBEB"
LAB = 105.1
PILL = frame(WHITE, top="soft", bottom="soft", left="soft", right="soft")
TAG = frame(WHITE, top="mid", bottom="mid", left="mid", right="mid")


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


def step_label(g, rows, pill_row, label_row, fill, pill_y, label_y, color=INK):
    """Left Step column: graded gray block, outlined Step pill, bold label (text layer)."""
    for r in range(rows):
        if r == pill_row:
            g.put(X0, 63.6, r, r + 1, [], frame(fill))
            g.put(63.6, 98.2, r, r + 1, [line1(68, 72, pill_y - 1, pill_y + 1)], PILL, line=1000)
            tight(g, 63.6, r)
            g.put(98.2, LAB, r, r + 1, [], frame(fill))
        elif r == label_row:
            g.put(X0, LAB, r, r + 1, [runs_of(line1(60, 65, label_y - 1, label_y + 1), color)], frame(fill),
                  line=1300)
            tight(g, X0, r)
        else:
            g.put(X0, LAB, r, r + 1, [], frame(fill))


# ---------------------------------------------------------------------------
# Page chrome (odd page): running head over a rule, side tab, footer at the right.
# ---------------------------------------------------------------------------
L.add_table([[cell(0, 3350, 1680, [para([("01", 1380, True, WHITE)], "CENTER")[0]], dark)],
             [cell(0, 3350, 5960, [para([(ch, 950, True, INK)], "CENTER", 1160)[0] for ch in "경영관리"], gray2)]],
            floating=(57800, 15000))
runs = runs_of(line1(450, 455, 816, 822))
foot = [runs[0], ("    ", 790, False, INK), runs[1]]
L.add_table([[cell(0, W, 1500, [para(foot, "RIGHT", 1300)[0]])]], floating=(5660, 81550))

g = Grid("head", [X0, 430.0, X1], [1680])
g.put(X0, 430.0, 0, 1, [], frame(bottom="soft"))
g.put(430.0, X1, 0, 1, [line1(430, 440, 35, 40)], align="RIGHT")
block(g, 32.0)

# 평가내용 03 band: light chip (image, typed) in the corner, hatched title (text layer).
g = Grid("band", [X0, 124.0, X1], [1700, 1160])
g.put(X0, 124.0, 0, 1, [[("평가내용 ", 800, True, INK), ("03", 1350, True, INK)]],
      frame("#CFCFCF", top="mid", left="soft"), line=1450)
g.put(X0, 124.0, 1, 2, [], frame("#E9E9E9", bottom="soft", left="soft", hatch="#DADADA"))
g.put(124.0, X1, 0, 2, [line1(125, 130, 77, 80)], frame("#E9E9E9", top="mid", bottom="soft", right="soft",
                                                           hatch="#DADADA"), align="LEFT", line=1450)
block(g, 70.9)

g = Grid("sec1", [X0, 84.5, X1], [2300])
g.put(X0, 84.5, 0, 1, [runs_of(line1(60, 70, 113, 116), WHITE)], frame(DARK), line=1700)
g.put(84.5, X1, 0, 1, [line1(90, 95, 114, 117)], frame("#E6E6E6"), align="LEFT", line=1700)
block(g, 111.5)

g = Grid("title-ga", [X0, 477.0, 549.0, X1], [1650])
g.put(X0, 477.0, 0, 1, [line1(55, 60, 141, 145)], align="LEFT", line=1450)
g.put(477.0, 549.0, 0, 1, "Best Practice", frame("#4A4A4A"), size=900, bold=True, color=WHITE)
block(g, 142.0)

# ---------------------------------------------------------------------------
# 가. Step1-2: 입장 / 원칙 / 목표 boxes (gray label | bullets)
# ---------------------------------------------------------------------------
BOX = ((107.6, 139.5, 330.5), (333.0, 364.8, X1))


def two_boxes(name, top, hs, pill, label, fill, y0, y1, rows):
    g = Grid(name, [X0, 63.6, 98.2, LAB] + [x for b in BOX for x in b], hs)
    step_label(g, len(hs), *pill, fill, *label)
    for a, m, e in BOX:
        heads = lines_in(a + 5, m, y0, y1)
        g.put(a, m, 0, rows, heads, frame(HEAD, top="mid", bottom="mid", left="mid"), bold=True, line=1300)
        g.put(m, e, 0, rows, lines_in(m + 3, m + 8, y0, y1), frame(top="mid", bottom="mid", right="mid"),
              align="LEFT", line=1540)
    block(g, top)


two_boxes("step1", 163.8, [1450, 1170, 1700, 1300, 630], (1, 2), (179.7, 193.4), "#E9E9E9", 168, 216, 4)
two_boxes("step2", 226.3, [820, 1200, 1750, 320, 630], (1, 2), (236.3, 250.2), "#D9D9D9", 230, 263, 4)

# Step3: two headed boxes joined by a chevron; the 우선순위 line with ① ② ③ (images, typed).
xs = [X0, 63.6, 98.2, LAB, 107.6, 110.5, 252.7, 255.4, 269.2, 272.0, 553.4, X1]
g = Grid("step3", xs, [1900, 1250, 1700, 1500, 630])
step_label(g, 5, 1, 2, "#BDBDBD", 294.4, 308.2)
for a, i0, i1, e, x in ((107.6, 110.5, 252.7, 255.4, 135), (269.2, 272.0, 553.4, X1, 355)):
    g.put(a, e, 0, 1, [line1(x, x + 5, 277, 280)], frame(top="mid", left="mid", right="mid"), bold=True, line=1300)
    g.put(a, i0, 1, 4, [], frame(left="mid", bottom="mid"))
    g.put(i1, e, 1, 4, [], frame(right="mid", bottom="mid"))
g.put(110.5, 252.7, 1, 4, lines_in(112, 116, 300, 320), frame(BODYGRAY, bottom="mid"), align="LEFT", line=1650)
g.put(255.4, 269.2, 1, 4, "▶", size=1300, color="#B4B4B4", line=1400, fit=False)
first = line1(274, 277, 300, 303)
order = [("  ", 1090, False, INK)] + runs_of(line1(274, 277, 317, 319))
for mark, x in (("①", 348.6), ("②", 403.6), ("③", 494.5)):
    order += [(f" {mark} ", 1090, False, INK)] + runs_of(line1(x - 1, x + 1, 317, 319))
g.put(272.0, 553.4, 1, 4, [runs_of(first), order], frame(BODYGRAY, bottom="mid"), align="LEFT", line=1650)
block(g, 273.5)

# Step4: three head bands (title + tag cells, ▶ icons) over three bullet columns.
heads = ((110.5, 194.5, 214.0, 255.7, 151.7), (270.6, 353.8, 373.5, 405.8, 301.5),
         (420.8, 503.1, 522.8, X1, 450.8))
cols = ((110.5, 254.0, 110.7), (258.6, 404.7, 261.4), (409.3, X1, 412.0))
xs = sorted({X0, 63.6, 98.2, LAB} | {x for h in heads for x in h[:4]} | {x for c in cols for x in c[:2]}
            | {255.7, 270.6, 405.8, 420.8})
g = Grid("step4", xs, [2020, 650, 1200, 1700, 1880, 930])
step_label(g, 6, 2, 3, "#9C9C9C", 371.5, 385.3, WHITE)
fills = ("#EDEDED", "#E3E3E3", "#D8D8D8")
for k, ((a, t, u, e, x), fill) in enumerate(zip(heads, fills)):
    line = line1(x - 1, x + 1, 347, 349)
    tag_x = line["spans"][1]["bbox"][0] - 0.5
    g.put(a, t, 0, 1, [runs_of(line, x1=tag_x)], frame(fill), align="RIGHT", line=1300)
    g.put(t, u, 0, 1, [strip_runs(runs_of(line, x0=tag_x))], TAG, line=1000, fit=False)
    tight(g, t, 0)
    g.put(u, e, 0, 1, [], frame(fill))
    if k < 2:
        g.put(e, heads[k + 1][0], 0, 1, "▶", frame(fill), size=900, color="#8A8A8A", line=1000, fit=False)
for k, (a, e, base) in enumerate(cols):
    g.put(a, e, 1, 5, hang(lines_in(a, e, 368, 416), base), frame(left="soft") if k else "1",
          align="LEFT", line=1540)
g.put(LAB, 110.5, 0, 6, [])
g.put(254.0, 258.6, 1, 5, [])
g.put(404.7, 409.3, 1, 5, [])
g.put(110.5, X1, 5, 6, [], frame(top="soft"))
block(g, 343.3)

# ---------------------------------------------------------------------------
# 상생기반 갈등해소 / 책임있는 교섭 / 추진성과
# ---------------------------------------------------------------------------
LABEL_FILL = frame("#E6E6E6", top="dot")
boxes = ((108.2, 162.5, 182.5, 330.6, 164.3), (333.1, 370.6, 390.6, X1, 372.4))
xs = sorted({X0, LAB} | {x for b in boxes for x in b[:4]})
g = Grid("mutual", xs, [300, 1440, 400, 1540, 1540, 680, 530])
g.put(X0, LAB, 0, 7, lines_in(60, 65, 443, 460), LABEL_FILL, bold=True, line=1320)
for a, t, u, e, x in boxes:
    line = line1(x - 1, x + 1, 431, 433)
    split = line["spans"][1]["bbox"][0] - 0.5
    g.put(a, e, 0, 1, [], frame(HEAD, top="mid", left="mid", right="mid"))
    g.put(a, t, 1, 2, [], frame(HEAD, left="mid"))
    g.put(t, u, 1, 2, [runs_of(line, x1=split)], TAG, line=1000, fit=False)
    tight(g, t, 1)
    g.put(u, e, 1, 2, [strip_runs(runs_of(line, x0=split))], frame(HEAD, right="mid"), align="LEFT", line=1280)
    g.put(a, e, 2, 6, lines_in(a + 3, a + 8, 450, 482), frame(top="soft", bottom="mid", left="mid", right="mid"),
          align="LEFT", line=1540)
block(g, 427.1)

boxes = ((108.2, 248.1), (262.0, 401.9), (415.7, X1))
xs = sorted({X0, LAB} | {x for b in boxes for x in b})
g = Grid("responsible", xs, [280, 1450, 450, 1540, 1540, 1540, 650, 650])
g.put(X0, LAB, 0, 8, lines_in(60, 75, 515, 531), LABEL_FILL, bold=True, line=1320)
for k, (a, e) in enumerate(boxes):
    g.put(a, e, 0, 2, [line1(a, e, 495, 497)], frame(HEAD, top="mid", left="mid", right="mid"), bold=True,
          line=1300)
    g.put(a, e, 2, 7, lines_in(a + 3, a + 8, 515, 550), frame(top="soft", bottom="mid", left="mid", right="mid"),
          align="LEFT", line=1540)
    if k < 2:
        g.put(e, boxes[k + 1][0], 0, 8, "▶", size=1300, color="#B4B4B4", line=1400, fit=False)
block(g, 491.6)

g = Grid("progress", [X0, LAB, 107.7, X1], [500, 1540, 1540, 420])
g.put(X0, LAB, 0, 4, [line1(60, 65, 587, 589)], frame("#D6D6D6", top="mid"), line=1300)
g.put(107.7, X1, 0, 4, lines_in(110, 116, 577, 596), frame("#EDEDED", top="soft", bottom="soft", left="soft",
                                                                 right="soft"), align="LEFT", line=1540)
block(g, 572.6)

# ---------------------------------------------------------------------------
# 나. 심리 지원 / 가족 친화 / 인사 제도: head band, bullets, ▼, gray results
# ---------------------------------------------------------------------------
g = Grid("title-na", [X0, X1], [1650])
g.put(X0, X1, 0, 1, [line1(55, 60, 622, 626)], align="LEFT", line=1450)
block(g, 623.9)

cols = ((X0, 220.1, 59.7), (224.6, 399.1, 227.3), (403.6, X1, 406.3))
xs = [X0, 220.1, 224.6, 237.1, 399.1, 403.6, 415.7, X1]
g = Grid("happy", xs, [2020, 4860, 860, 3520])
heads = ((X0, 220.1, "#EDEDED"), (237.1, 399.1, "#E3E3E3"), (415.7, X1, "#D8D8D8"))
for k, (a, e, fill) in enumerate(heads):
    g.put(a, e, 0, 1, [line1(a + 3, e, 648, 651)], frame(fill), bold=True, line=1300)
    if k < 2:
        g.put(e, heads[k + 1][0], 0, 1, "▶", frame(fill), size=900, color="#8A8A8A", line=1000, fit=False)
for k, (a, e, base) in enumerate(cols):
    g.put(a, e, 1, 2, hang(lines_in(base - 1, base + 10, 668, 714), base), align="LEFT", line=1450)
    g.put(a, e, 2, 3, "▼", size=700, color="#A0A0A0", line=700)
    g.put(a, e, 3, 4, lines_in(base - 1, base + 2, 722, 754), frame("#E3E3E3"), align="LEFT", line=1540)
g.put(220.1, 224.6, 1, 4, [])
g.put(399.1, 403.6, 1, 4, [])
block(g, 644.8)

g = Grid("result", [X0, 111.7, X1], [3710])
g.put(X0, 111.7, 0, 1, [runs_of(line1(60, 70, 776, 780), WHITE)], frame(DARK, top="mid", bottom="mid", left="mid"))
g.put(111.7, X1, 0, 1, lines_in(115, 120, 766, 790), frame(top="mid", bottom="mid", right="mid"), align="LEFT",
      line=1500)
block(g, 764.8)

kit.finish(target, end=801.9)
