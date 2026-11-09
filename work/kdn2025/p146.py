"""Rebuild KDN 2025 report page 146 (3rd PDF local page 46, printed page 103) as editable HWPX.

Usage: python3 work/kdn2025/p146.py <report3.pdf> <out.hwpx> [--page 46]

조직 운영 및 관리(노사관계), section 2 "일･가정 양립과 가족친화경영을 위한 근무 여건 및 일하는 방식
혁신": 가. 직원 니즈 / 제도 개선 boxes, 나. 스마트워크 boxes with 추진성과, 다. 임신･출산･양육 flow and
stage table, 주요성과. Built with the shared kit (one flat table per horizontal band on a grid of PDF x
edges). All running text, heads, stage pills and the 개선 / 고용노동부 / 여성가족부 / 문화체육관광부 tags
come from the PDF text layer; tags are separate cells.

Images and how they are kept:
- PART 01 box, section number band, the KDN logo: typed cells.
- round arrow icons of the 가. phase band and the gray chevrons between boxes -> ▶ connector cells;
  the stage chevrons of 다. -> graded gray label cells; the bracket rule from 제도 개선 down to the
  stage table -> cell borders.
- the 지적사항 개선 sticker after "‘종합복지만족도’ 조사" (hand icon dropped): a dark tag cell.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kit  # noqa: E402
from kit import Layout, recipe_inputs  # noqa: E402

source, target = recipe_inputs(46, "일하는 방식 혁신")
L = Layout(top=3100)
kit.setup(source, L)
from kit import *  # noqa: E402,F401,F403  helpers and presets bound to this page

DARK, HEAD = "#6A6A6A", "#D9D9D9"
TAG_DARK = frame("#6E6E6E")
PILL = frame(WHITE, top="soft", bottom="soft", left="soft", right="soft")


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


def tag_runs(line, x, color=INK):
    """Split a PDF line at the tag starting at x: (text runs, tag runs)."""
    return runs_of(line, x1=x - 0.5), strip_runs(runs_of(line, color, x0=x - 0.5))


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

g = Grid("sec2", [X0, 84.5, X1], [2300])
g.put(X0, 84.5, 0, 1, [runs_of(line1(60, 70, 72, 76), WHITE)], frame(DARK), line=1700)
g.put(84.5, X1, 0, 1, [line1(90, 95, 73, 77)], frame("#E6E6E6"), align="LEFT", line=1700)
block(g, 70.9)

g = Grid("title-ga", [X0, X1], [1650])
g.put(X0, X1, 0, 1, [line1(55, 60, 100, 105)], align="LEFT", line=1450)
block(g, 101.2)

# ---------------------------------------------------------------------------
# 가. phase band (▶ icons) and the three need boxes (head | gray tagged lines)
# ---------------------------------------------------------------------------
phases = ((X0, 217.7, 68.4, "#EDEDED"), (232.4, 382.0, 255.5, "#E3E3E3"), (396.8, X1, 404.8, "#D6D6D6"))
g = Grid("phases", [X0, 217.7, 232.4, 382.0, 396.8, X1], [2010])
for k, (a, e, x, fill) in enumerate(phases):
    g.put(a, e, 0, 1, [line1(x - 1, x + 1, 126, 129)], frame(fill), bold=True, line=1300)
    if k < 2:
        g.put(e, phases[k + 1][0], 0, 1, "▶", frame(phases[k + 1][3]), size=900, color="#8A8A8A", line=1000,
              fit=False)
block(g, 123.2)

cols = ((60.9, 219.9, 66.8), (222.5, 392.8, 228.4), (395.3, 551.5, 401.2))
tags = {(1, 0): (341.9, 362.0), (1, 1): (329.7, 350.0)}
ys = (173.2, 188.8, 204.2, 219.7)
xs = sorted({X0, X1} | {x for c in cols for x in c[:2]} | {x for t in tags.values() for x in t})
g = Grid("needs", xs, [420, 1890, 460, 1540, 1540, 1540, 1540, 420, 430])
g.put(X0, X1, 0, 1, [], frame(top="soft", left="soft", right="soft"))
g.put(X0, 60.9, 1, 8, [], frame(left="soft"))
g.put(551.5, X1, 1, 8, [], frame(right="soft"))
g.put(X0, X1, 8, 9, [], frame(bottom="soft", left="soft", right="soft"))
BODY = "#E6E6E6"
for k, (a, e, base) in enumerate(cols):
    g.put(a, e, 1, 2, [line1(a, e, 152, 154)], frame(WHITE, top="mid", left="mid", right="mid"), bold=True,
          line=1300)
    g.put(a, e, 2, 3, [], frame(BODY, left="mid", right="mid"))
    for i, y in enumerate(ys):
        r = 3 + i
        line = line1(base - 1, base + 1, y - 1, y + 1)
        if (k, i) in tags:
            t0, t1 = tags[k, i]
            text, tag = tag_runs(line, t0 + 0.5, WHITE)
            g.put(a, t0, r, r + 1, hang([dict(line, spans=[s for s in line["spans"] if s["bbox"][0] < t0])], base),
                  frame(BODY, left="mid"), align="LEFT", line=1300)
            g.put(t0, t1, r, r + 1, [tag], TAG_DARK, line=1000, fit=False)
            tight(g, t0, r)
            g.put(t1, e, r, r + 1, [], frame(BODY, right="mid"))
        else:
            g.put(a, e, r, r + 1, hang([line], base), frame(BODY, left="mid", right="mid"), align="LEFT", line=1300)
    g.put(a, e, 7, 8, [], frame(BODY, left="mid", right="mid", bottom="mid"))
block(g, 143.3)

g = Grid("progress", [X0, 114.0, 116.2, X1], [2580])
g.put(X0, 114.0, 0, 1, [line1(60, 70, 255, 258)], frame("#D6D6D6", top="mid"), line=1300)
g.put(116.2, X1, 0, 1, [line1(120, 125, 252, 255)], frame("#EFEFEF", top="soft", bottom="soft", left="soft",
                                                           right="soft"), line=1350)
block(g, 247.4)

# ---------------------------------------------------------------------------
# 나. two system boxes ▶ 추진성과 box
# ---------------------------------------------------------------------------
g = Grid("title-na", [X0, X1], [1650])
g.put(X0, X1, 0, 1, [line1(55, 60, 283, 287)], align="LEFT", line=1450)
block(g, 284.6)

g = Grid("smart", [X0, 388.6, 402.5, X1], [1740, 5730, 250, 1740, 5730])
side = dict(left="mid", right="mid")
for r, y0, y1 in ((0, 308, 375), (3, 385, 452)):
    g.put(X0, 388.6, r, r + 1, [line1(110, 130, y0, y0 + 4)], frame(HEAD, top="mid", **side), bold=True, line=1300)
    g.put(X0, 388.6, r + 1, r + 2, lines_in(60, 65, y0 + 15, y1), frame(top="soft", bottom="mid", **side),
          align="LEFT", line=1540)
g.put(388.6, 402.5, 0, 5, "▶", size=1300, color="#B4B4B4", line=1400, fit=False)
g.put(402.5, X1, 0, 1, [runs_of(line1(455, 465, 308, 312), WHITE)], frame(DARK, top="mid", **side), line=1300)
g.put(402.5, X1, 1, 5, hang(lines_in(405, 430, 330, 440), 408.4), frame(bottom="mid", **side), align="LEFT",
      line=1950)
block(g, 305.5)

# ---------------------------------------------------------------------------
# 다. 기반 조성 ▶ 의견 수렴 ▶ 제도 개선, bracket, stage table ▶ results, 주요성과
# ---------------------------------------------------------------------------
g = Grid("title-da", [X0, X1], [1650])
g.put(X0, X1, 0, 1, [line1(55, 60, 467, 471)], align="LEFT", line=1450)
block(g, 468.7)

boxes = ((X0, 208.2, 62.5, HEAD, INK), (222.0, 393.2, 227.9, "#C9C9C9", INK), (407.1, X1, 413.0, DARK, WHITE))
xs = [X0, 208.2, 222.0, 329.5, 382.5, 393.2, 407.1, X1]
g = Grid("process", xs, [1740, 540, 1550, 1550, 1550, 540])
side = dict(left="mid", right="mid")
for k, (a, e, base, fill, color) in enumerate(boxes):
    g.put(a, e, 0, 1, [runs_of(line1(a + 20, e, 493, 496), color)], frame(fill, top="mid", **side), bold=True,
          line=1300)
    g.put(a, e, 1, 2, [], frame(**side))
    for i, y in enumerate((515.2, 530.7, 545.5)):
        line = lines_in(base - 1, base + 30, y - 1, y + 1)
        assert len(line) == 1, (k, i)
        if k == 1 and i == 0:
            g.put(a, 329.5, 2, 3, hang(line, base), frame(left="mid"), align="LEFT", line=1300)
            g.put(329.5, 382.5, 2, 3, "지적사항 개선", frame("#3C3C3C"), size=740, bold=True, color=WHITE,
                  line=900, fit=False)
            tight(g, 329.5, 2)
            g.put(382.5, e, 2, 3, [], frame(right="mid"))
        else:
            g.put(a, e, 2 + i, 3 + i, hang(line, base), frame(**side), align="LEFT", line=1300)
    g.put(a, e, 5, 6, [], frame(bottom="mid", **side))
    if k < 2:
        g.put(e, boxes[k + 1][0], 0, 6, "▶", size=1300, color="#B4B4B4", line=1400, fit=False)
block(g, 489.7)

g = Grid("bracket", [X0, 306.0, 477.7, X1], [700, 640])
g.put(306.0, 477.7, 0, 1, [], frame(right="mid"))
g.put(306.0, 477.7, 1, 2, [], frame(top="mid", left="mid"))
block(g, 564.4)

stages = (("#E4E4E4", [1720, 1300, 1650, 1450], 597.1, 610.9, (584, 632)),
          ("#D2D2D2", [1200, 1250, 1500, 350], 652.9, 665.6, (644, 676)),
          ("#C0C0C0", [2750, 1250, 1650, 1880], 711.2, 725.0, (686, 752)))
hs = [h for s in stages for h in s[1]]
xs = [X0, 74.9, 109.5, 127.9, 128.9, 421.0, 433.6, X1]
g = Grid("stages", xs, hs)
r = 0
for k, (fill, rows, pill_y, label_y, (y0, y1)) in enumerate(stages):
    top = dict(top="mid") if k == 0 else {}
    bottom = dict(bottom="mid") if k == 2 else dict(bottom="dot")
    g.put(X0, 127.9, r, r + 1, [], frame(fill, **top))
    g.put(X0, 74.9, r + 1, r + 2, [], frame(fill))
    g.put(74.9, 109.5, r + 1, r + 2, [line1(78, 83, pill_y - 1, pill_y + 1)], PILL, line=1000)
    tight(g, 74.9, r + 1)
    g.put(109.5, 127.9, r + 1, r + 2, [], frame(fill))
    g.put(X0, 127.9, r + 2, r + 3, [line1(59, 63, label_y - 1, label_y + 1)], frame(fill), line=1300)
    tight(g, X0, r + 2, 100, 100)
    g.put(X0, 127.9, r + 3, r + 4, [], frame(fill, **({"bottom": "mid"} if k == 2 else {})))
    g.put(128.9, 421.0, r, r + 4, lines_in(130, 135, y0, y1), frame(**top, **bottom), align="LEFT", line=1650)
    r += 4
g.put(127.9, 128.9, 0, r, [])
g.put(421.0, 433.6, 0, r, "▶", size=1300, color="#B4B4B4", line=1400, fit=False)
g.put(433.6, X1, 0, r, hang(lines_in(435, 446, 580, 755), 436.7), frame("#EDEDED", hatch="#DEDEDE"),
      align="LEFT", line=1700)
block(g, 577.8)

# 주요성과: dark label; bullet, ministry tags (separate cells) and bold text per line.
xs = [X0, 111.7, 115.0, 125.6, 171.4, 320.1, 380.0, X1]
g = Grid("result", xs, [350, 1550, 1550, 270])
g.put(X0, 111.7, 0, 4, [runs_of(line1(60, 70, 776, 780), WHITE)], frame(DARK, top="mid", bottom="mid", left="mid"))
g.put(111.7, X1, 0, 1, [], frame(top="mid", right="mid"))
g.put(111.7, X1, 3, 4, [], frame(bottom="mid", right="mid"))
ministry = frame("#D9D9D9")
for r, y in ((1, 769.4), (2, 785.4)):
    line = line1(117, 119, y - 1, y + 1)
    part = lambda x0, x1: strip_runs(runs_of(line, x0=x0, x1=x1))
    g.put(111.7, 125.6, r, r + 1, [part(110, 125)], align="RIGHT", line=1300)
    tight(g, 111.7, r, 0, 100)
    g.put(125.6, 171.4, r, r + 1, [part(125, 171)], ministry, line=1000, fit=False)
    tight(g, 125.6, r)
    if r == 1:
        g.put(171.4, X1, r, r + 1, [part(171, 600)], frame(right="mid"), align="LEFT", line=1300)
    else:
        g.put(171.4, 320.1, r, r + 1, [part(171, 320)], align="LEFT", line=1300)
        g.put(320.1, 380.0, r, r + 1, [part(320, 379)], ministry, line=1000, fit=False)
        tight(g, 320.1, r)
        g.put(380.0, X1, r, r + 1, [part(379, 600)], frame(right="mid"), align="LEFT", line=1300)
block(g, 765.0)

kit.finish(target, end=802.2)
