"""Rebuild KDN 2025 report page 107 (3rd PDF local page 7, printed page 72) as editable HWPX.

Usage: python3 work/kdn2025/p107.py <report3.pdf> <out.hwpx> [--page 7]

재무성과관리(재무예산관리), section 3 "재무안정 기반 위에서 미래성장 투자 본격화 및 공공가치 창출
확대" (가. 자금운용 / 나. 미래성장 투자 / 다. 상생･협력, 주요성과). Built with the shared kit (one
flat table per band on a grid of PDF x edges); every text line comes from the PDF text layer.
Images and how they are kept:
- side tab, section-3 number band, rounded boxes and label blocks: fills and borders (the small
  diagonal corner strokes of the label blocks are dropped).
- the thick arrows (➡) before 전략적 자금 운용 / 채권･채무 관리강화 / 「국정과제 …」 /
  「공공성･ESG …」: typed "→"; the grey chevrons between the 미래성장 투자 boxes: "▶".
- the boxed numbers in the 사회적 가치 창출 heads: typed "1" "2" "3" in outlined cells.
- 전략1/전략2 and 실행내용 pills (text layer) are separate cells.
Superscript years ('24년, '25년 at 6.5 pt) stay small runs on the baseline (kit default).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kit  # noqa: E402
from kit import Layout, recipe_inputs  # noqa: E402

source, target = recipe_inputs(7, "재무안정 기반 위에서 미래성장 투자 본격화 및 공공가치 창출 확대")
L = Layout(top=3100)
kit.setup(source, L)
from kit import *  # noqa: E402,F401,F403  helpers and presets bound to this page

LAB = 102.6                     # label column end
LIGHT, RESULT, HEAD = "#EDEDED", "#BFBFBF", "#D9D9D9"
BODY_GRAY = "#E5E5E5"
SUB = "#EAEAEA"
BOX = dict(left="mid", right="mid")


def hang(lines, base):
    """Lines keep their PDF indent: spaces for the x offset and for the line's own lead."""
    out = []
    for line in lines:
        runs = runs_of(line)
        size = runs[0][1] / 100
        raw = "".join(s["text"] for s in line["spans"])
        offset = line["bbox"][0] - base + (len(raw) - len(raw.lstrip(" "))) * 0.29 * size
        n = max(0, round(offset / (0.29 * size)))
        out.append([(" " * n, runs[0][1], False, INK)] + runs if n else runs)
    return out


def label(g, r0, r1, lines, fill=LIGHT, color=INK):
    g.put(X0, LAB, r0, r1, [runs_of(l, color) for l in lines], frame(fill), line=1300)


def arrow_line(first, second):
    """'∙ text ➡ 「bold」' on one line: the image arrow typed as →."""
    return runs_of(first) + [(" → ", 1090, False, INK)] + strip_runs(runs_of(second))


def tight(g, x0, r0, left=0, right=0):
    c0 = g.xs.index(to_x(x0))
    item = g.items[r0, c0]
    g.items[r0, c0] = (*item[:7], dict(left=left, right=right))


# ---------------------------------------------------------------------------
# Page chrome (odd page): running head over a rule, side tab, footer at the right.
# ---------------------------------------------------------------------------
L.add_table([[cell(0, 3350, 1680, [para([("01", 1380, True, WHITE)], "CENTER")[0]], dark)],
             [cell(0, 3350, 5960, [para([(ch, 950, True, INK)], "CENTER", 1160)[0] for ch in "경영관리"], gray2)]],
            floating=(57800, 15000))
foot = [(text, size, False, INK) for text, size in (
    (line1(450, 455, 818, 822)["text"], 790), ("    ", 790), (line1(540, 546, 816, 820)["text"], 1090))]
L.add_table([[cell(0, W, 1500, [para(foot, "RIGHT", 1300)[0]])]], floating=(5660, 81550))

g = Grid("head", [X0, 430.0, X1], [1680])
g.put(X0, 430.0, 0, 1, [], frame(bottom="soft"))
g.put(430.0, X1, 0, 1, [line1(430, 440, 35, 40)], align="RIGHT")
block(g, 32.0)

g = Grid("sec3", [X0, 84.5, X1], [2300])
g.put(X0, 84.5, 0, 1, [runs_of(line1(60, 70, 72, 77), WHITE)], frame("#666666"), line=1700)
g.put(84.5, X1, 0, 1, [line1(90, 95, 73, 78)], frame(BODY_GRAY), align="LEFT", line=1700)
block(g, 70.9)

g = Grid("title-ga", [X0, X1], [1650])
g.put(X0, X1, 0, 1, [line1(55, 60, 99, 103)], align="LEFT", line=1450)
block(g, 99.8)

# ---------------------------------------------------------------------------
# 가. 추진방향 / 전략적 자금운용 / 채권･채무 관리강화 / 추진실적
# ---------------------------------------------------------------------------
g = Grid("dir-ga", [X0, LAB, 104.8, 416.0, X1], [3570])
label(g, 0, 1, [line1(60, 62, 130, 135)])
g.put(104.8, 416.0, 0, 1, lines_in(113, 114, 120, 152), frame(LIGHT, top="soft", bottom="soft", left="soft"),
      align="LEFT", line=1540)
g.put(416.0, X1, 0, 1, [[("→ ", 1090, True, INK)] + runs_of(l) for l in lines_in(429, 430, 120, 152)],
      frame(LIGHT, top="soft", bottom="soft", right="soft"), align="LEFT", line=1540)
block(g, 119.1)

boxes = ((104.8, 329.0, 116.6, 145.6, 110.7, 149.5, 148.0), (331.6, X1, 356.0, 384.8, 337.4, 376.0, 375.0))
xs = sorted({X0, LAB} | {x for b in boxes for x in b[:6]})
g = Grid("fund", xs, [1950, 1700, 3320])
label(g, 0, 3, lines_in(58, 70, 178, 210))
for a, e, p0, p1, t0, t1, split in boxes:
    head = line1(p0, p1, 162, 166)
    g.put(a, p0, 0, 1, [], frame(HEAD, top="mid", left="mid"))
    g.put(p0, p1, 0, 1, [runs_of(head, WHITE, x1=p1)], frame("#7E7E7E"), line=1000)
    g.put(p1, e, 0, 1, [strip_runs(runs_of(head, x0=p1))], frame(HEAD, top="mid", right="mid"), align="LEFT")
    row = line1(t0, t1, 182, 186)
    g.put(a, t0, 1, 2, [], frame(left="mid"))
    g.put(t0, t1, 1, 2, [runs_of(row, x1=split)], frame("#D0D0D0"), line=1000)
    g.put(t1, e, 1, 2, [strip_runs(runs_of(row, x0=split))], frame(right="mid"), align="LEFT")
    g.put(a, e, 2, 3, hang(lines_in(a, e, 197, 226), t0), frame(bottom="mid", **BOX), align="LEFT", line=1430)
block(g, 158.9)

cols = ((104.8, 253.4, 110.7), (256.0, 404.6, 261.8), (407.1, X1, 413.0))
xs = sorted({X0, LAB} | {x for c in cols for x in c[:2]})
g = Grid("bonds", xs, [1900, 6080])
label(g, 0, 2, lines_in(56, 70, 256, 288))
for a, e, base in cols:
    g.put(a, e, 0, 1, [line1(a, e, 236, 240)], frame(top="mid", bottom="dot", **BOX))
    g.put(a, e, 1, 2, hang(lines_in(a, e, 254, 311), base), frame(bottom="mid", **BOX), align="LEFT", line=1380)
block(g, 232.7)

g = Grid("result-ga", [X0, LAB, 104.8, 109.1, 330.2, 551.3, X1], [470, 1700, 1980, 480])
label(g, 0, 4, [line1(60, 62, 332, 336)], RESULT)
g.put(104.8, X1, 0, 1, [], frame(top="soft", left="soft", right="soft"))
g.put(104.8, X1, 3, 4, [], frame(bottom="soft", left="soft", right="soft"))
for r in (1, 2):
    g.put(104.8, 109.1, r, r + 1, [], frame(left="soft"))
    g.put(551.3, X1, r, r + 1, [], frame(right="soft"))
for a, e in ((109.1, 330.2), (330.2, 551.3)):
    g.put(a, e, 1, 2, [runs_of(line1(a, e, 322, 326), WHITE)], frame("#7E7E7E"))
    g.put(a, e, 2, 3, [line1(a, e, 342, 346)], frame(bottom="soft"))
block(g, 316.2)

# ---------------------------------------------------------------------------
# 나. 미래성장 투자
# ---------------------------------------------------------------------------
g = Grid("title-na", [X0, X1], [1700])
g.put(X0, X1, 0, 1, [line1(55, 60, 369, 373)], align="LEFT", line=1500)
block(g, 370.0)

g = Grid("dir-na", [X0, LAB, 104.8, X1], [2580])
label(g, 0, 1, [line1(60, 62, 396, 400)])
g.put(104.8, X1, 0, 1, [arrow_line(line1(113, 114, 396, 400), line1(396, 397, 396, 400))],
      frame(LIGHT, top="soft", bottom="soft", left="soft", right="soft"), align="LEFT")
block(g, 390.1)

cols = ((105.1, 246.1, 111.0), (260.0, 401.0, 265.9), (414.9, X1, 420.8))
xs = sorted({X0, LAB} | {x for c in cols for x in c[:2]})
g = Grid("future", xs, [2270, 1750, 5790])
label(g, 0, 3, lines_in(58, 75, 455, 485))
for k, (a, e, base) in enumerate(cols):
    g.put(a, e, 0, 1, [line1(a, e, 422, 426)], frame(top="mid", bottom="dot", **BOX), line=1300)
    sub = frame(SUB, hatch="#D6D6D6", **BOX) if k == 2 else frame(SUB, **BOX)
    g.put(a, e, 1, 2, [line1(a, e, 444, 448)], sub)
    g.put(a, e, 2, 3, hang(lines_in(a, e, 460, 515), base), frame(bottom="mid", **BOX), align="LEFT", line=1330)
    if k < 2:
        g.put(e, cols[k + 1][0], 0, 3, "▶", size=1300, color="#BDBDBD", fit=False)
block(g, 420.0)

g = Grid("result-na", [X0, LAB, 104.8, X1], [2610])
label(g, 0, 1, [line1(60, 62, 528, 532)], RESULT)
g.put(104.8, X1, 0, 1, [line1(113, 114, 528, 532)], frame(BODY_GRAY, top="soft", bottom="soft", left="soft",
                                                           right="soft"), align="LEFT")
block(g, 522.0)

# ---------------------------------------------------------------------------
# 다. 상생･협력 기반 지원
# ---------------------------------------------------------------------------
g = Grid("title-da", [X0, X1], [1700])
g.put(X0, X1, 0, 1, [line1(55, 60, 555, 559)], align="LEFT", line=1500)
block(g, 555.6)

g = Grid("dir-da", [X0, LAB, 104.8, X1], [2580])
label(g, 0, 1, [line1(60, 62, 582, 586)])
g.put(104.8, X1, 0, 1, [arrow_line(line1(113, 114, 582, 586), line1(357, 358, 582, 586))],
      frame(LIGHT, top="soft", bottom="soft", left="soft", right="soft"), align="LEFT")
block(g, 575.9)

cols = ((104.8, 253.4, 138.5, 150.5, 110.7), (256.0, 404.6, 289.7, 301.5, 261.8),
        (407.1, X1, 445.4, 457.3, 413.0))
xs = sorted({X0, LAB} | {x for c in cols for x in c[:4]})
g = Grid("social", xs, [350, 1200, 350, 7650])
label(g, 0, 4, lines_in(58, 75, 633, 675))
for k, (a, e, b0, b1, base) in enumerate(cols):
    g.put(a, b0, 0, 3, [], frame(HEAD, top="mid", left="mid", bottom="soft"))
    g.put(b0, b1, 0, 1, [], frame(HEAD, top="mid"))
    g.put(b0, b1, 1, 2, str(k + 1), frame(WHITE, top="soft", bottom="soft", left="soft", right="soft"),
          size=950, bold=True, line=1050, fit=False)
    tight(g, b0, 1)
    g.put(b0, b1, 2, 3, [], frame(HEAD, bottom="soft"))
    g.put(b1, e, 0, 3, [line1(b1, e, 609, 613)], frame(HEAD, top="mid", right="mid", bottom="soft"), align="LEFT")
    g.put(a, e, 3, 4, hang(lines_in(a, e, 628, 698), base), frame(bottom="mid", **BOX), align="LEFT", line=1380)
block(g, 605.8)

cols = ((104.8, 253.4, 110.7), (256.0, 404.6, 261.8), (407.1, X1, 413.0))
xs = sorted({X0, LAB} | {x for c in cols for x in c[:2]})
g = Grid("result-da", xs, [3610])
label(g, 0, 1, [line1(60, 62, 716, 720)], RESULT)
for a, e, base in cols:
    g.put(a, e, 0, 1, hang(lines_in(a, e, 709, 737), base),
          frame(BODY_GRAY, top="soft", bottom="soft", left="soft", right="soft"), align="LEFT", line=1450)
block(g, 705.0)

# 주요성과
g = Grid("result", [X0, 112.5, X1], [5420])
g.put(X0, 112.5, 0, 1, [runs_of(line1(65, 70, 768, 772), WHITE)], frame("#7F7F7F", top="mid", bottom="mid", left="mid"))
g.put(112.5, X1, 0, 1, lines_in(117, 118, 750, 797), frame(top="mid", bottom="mid", right="mid"), align="LEFT",
      line=1600)
block(g, 747.4)

kit.finish(target, end=801.6)
