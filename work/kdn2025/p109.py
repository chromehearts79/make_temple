"""Rebuild KDN 2025 report page 109 (3rd PDF local page 9, printed page 74) as editable HWPX.

Usage: python3 work/kdn2025/p109.py <report3.pdf> <out.hwpx> [--page 9]

재무성과관리(재무예산관리), section 2 "재무안정성 제고를 위한 투명하고 효율적인 예산집행 선순환 구조
확립" (가. Build 1 / 나. Build 2 / 다. Circulate). Built with the shared kit (one flat table per
band on a grid of PDF x edges); every text line comes from the PDF text layer, including the
신규 / 강화 / 기존 / 개선 / 1단계 tags and the step pills, which become separate cells.
Images and how they are kept:
- side tab, section-2 number band, box outlines, the dark corner tabs (1 내부통제 …) and the
  gradient step strips: fills and borders; the boxed digits of the tabs and of the 위험 단계 strip
  are outlined cells (their digits are in the text layer).
- the small notches over the result bands and the chevrons under the 위험 단계 texts: "▼";
  the circled arrows between steps: "▶"; the thick arrows (➡) inside the 다. boxes: "→".
- the "지적사항 개선" sticker next to the 다. title (hand icon dropped): typed in a dark cell.
- the grey wedge between the step strip and the three 3R boxes: dropped (blank gap).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kit  # noqa: E402
from kit import Layout, recipe_inputs  # noqa: E402

source, target = recipe_inputs(9, "재무안정성 제고를 위한 투명하고 효율적인 예산집행 선순환 구조 확립")
L = Layout(top=3100)
kit.setup(source, L)
from kit import *  # noqa: E402,F401,F403  helpers and presets bound to this page

TAB, HEAD, BAND = "#6E6E6E", "#D9D9D9", "#DFDFDF"
NEW = frame("#7E7E7E")                                               # 신규 / 개선 / n단계 tags
OUTLINED = frame(WHITE, top="soft", bottom="soft", left="soft", right="soft")   # 강화 / 기존 / step n
TAGS = {"신규": (NEW, WHITE), "강화": (OUTLINED, INK)}


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


def tight(g, x0, r0, left=0, right=0):
    c0 = g.xs.index(to_x(x0))
    item = g.items[r0, c0]
    g.items[r0, c0] = (*item[:7], dict(left=left, right=right))


def tag_cell(x):
    """Tag column of a 신규/강화 span by its x (left box: 259 / 280, right box: 531)."""
    if x < 270:
        return 258.8, 277.6
    return (279.8, 298.6) if x < 300 else (530.5, 549.3)


def tab(g, x0, x1, n0, n1, line, r0):
    """Dark corner tab '1 내부통제': dark cell, outlined digit cell, dark label cell. The digit and
    the label share the middle row r0+1 so the text keeps the PDF order."""
    split = n1 - 1.0
    g.put(x0, x1, r0, r0 + 1, [], frame(TAB, top="soft"))
    g.put(x0, n0, r0 + 1, r0 + 2, [], frame(TAB))
    g.put(n0, n1, r0 + 1, r0 + 2, [runs_of(line, x1=split)], frame(WHITE), line=1000, fit=False)
    tight(g, n0, r0 + 1)
    g.put(n1, x1, r0 + 1, r0 + 2, [strip_runs(runs_of(line, WHITE, x0=split))], frame(TAB), align="LEFT")
    g.put(x0, x1, r0 + 2, r0 + 3, [], frame(TAB))


def box_band(name, top, heads, bodies, results, line_tops, pads):
    """Two boxes side by side: tab + title head, tagged bullet lines, notched result band."""
    left, right = (56.6, 304.6), (307.3, X1)
    xs = [X0, 59.4, 71.2, 114.0, 123.5, 258.8, 277.6, 279.8, 298.6, 304.6, 307.3, 492.4, 498.1, 500.8,
          512.5, 530.5, 549.3, X1]
    n = len(line_tops)
    hs = [250, 1370, 250, pads[0]] + [70, 1420, 70] * n + [pads[1], 800, 1650]
    g = Grid(name, xs, hs)
    # heads
    (tab_line, title_line), (title_line2, tab_line2) = heads
    tab(g, X0, 114.0, 59.4, 71.2, tab_line, 0)
    g.put(114.0, 304.6, 0, 3, [title_line], frame(HEAD, top="soft", right="soft"), line=1300)
    g.put(307.3, 498.1, 0, 3, [title_line2], frame(HEAD, top="soft", left="soft"), line=1300)
    tab(g, 498.1, X1, 500.8, 512.5, tab_line2, 0)
    body_end = 3 + 1 + 3 * n + 1
    for (a, e), lines, edge in ((left, bodies[0], 298.6), (right, bodies[1], 549.3)):
        g.put(edge, e, 3, body_end, [], frame(right="soft"))
        g.put(a, edge, 3, 4, [], frame(left="soft"))
        g.put(a, edge, body_end - 1, body_end, [], frame(left="soft"))
        for i, line in enumerate(lines):
            r = 4 + 3 * i
            tags = [s for s in line["spans"] if s["text"].strip() in TAGS and s["size"] < 9]
            text_end = tag_cell(tags[0]["bbox"][0])[0] if tags else edge
            if tags:      # drop the tag spans from the text cell
                cut = tags[0]["bbox"][0] - 0.5
                line = dict(line, spans=[s for s in line["spans"] if s["bbox"][0] < cut])
            runs = hang([line], a + 5.9)[0]
            runs[-1] = (runs[-1][0].rstrip(), *runs[-1][1:])
            g.put(a, edge, r, r + 1, [], frame(left="soft"))
            g.put(a, text_end, r + 1, r + 2, [runs], frame(left="soft"), align="LEFT", line=1260)
            g.put(a, edge, r + 2, r + 3, [], frame(left="soft"))
            for s in tags:
                t0, t1 = tag_cell(s["bbox"][0])
                fill, color = TAGS[s["text"].strip()]
                g.put(t0, t1, r + 1, r + 2, [[(s["text"].strip(), 840, True, color)]], fill, line=950, fit=False)
                tight(g, t0, r + 1)
    # result bands with a notch
    for (a, e), line in zip((left, right), results):
        g.put(a, e, body_end, body_end + 1, "▼", frame(BAND, left="soft", right="soft"), size=700,
              color="#9A9A9A", line=620, fit=False)
        g.put(a, e, body_end + 1, body_end + 2, [line], frame(BAND, bottom="soft", left="soft", right="soft"))
    block(g, top)


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

g = Grid("sec2", [X0, 84.5, X1], [2300])
g.put(X0, 84.5, 0, 1, [runs_of(line1(60, 70, 72, 77), WHITE)], frame("#666666"), line=1700)
g.put(84.5, X1, 0, 1, [line1(90, 95, 73, 78)], frame("#E5E5E5"), align="LEFT", line=1700)
block(g, 70.9)

# ---------------------------------------------------------------------------
# 가. Build 1: four boxes (내부통제 / 모니터링 / 공정거래 / 청렴문화)
# ---------------------------------------------------------------------------
title_band("title-ga", line1(55, 60, 101, 105), [X0, 76.9, 128.7, X1], 101.0)

box_band("boxes-1", 123.8,
         ((line1(60, 65, 127, 131), line1(150, 155, 126, 130)), (line1(345, 355, 126, 130), line1(500, 505, 127, 131))),
         (lines_in(60, 65, 148, 225), lines_in(310, 315, 148, 225)),
         (line1(80, 85, 233, 237), line1(320, 325, 233, 237)),
         (149.4, 165.1, 180.5, 195.8, 211.4), (450, 180))

# box row 2: the '[교      육]' label is two PDF lines on one row: joined with spaces.
left2 = lines_in(60, 65, 279, 340)
gyo, yuk = line1(60, 65, 279, 283), line1(110, 115, 279, 283)
joined = dict(gyo, spans=[*gyo["spans"], dict(gyo["spans"][-1], text="      ", bbox=(90.0, 280.2, 110.0, 292.3)),
                          *yuk["spans"]])
left2 = [joined] + [l for l in left2 if l is not gyo]
box_band("boxes-2", 254.4,
         ((line1(60, 65, 258, 262), line1(140, 145, 257, 261)), (line1(330, 335, 257, 261), line1(500, 505, 258, 262))),
         (left2, lines_in(310, 315, 279, 340)),
         (line1(75, 80, 349, 353), line1(325, 330, 349, 353)),
         (280.1, 295.8, 311.6, 327.3), (450, 260))

# ---------------------------------------------------------------------------
# 나. Build 2: 위험 단계 strip, 예산운영 조치, 추진성과
# ---------------------------------------------------------------------------
title_band("title-na", line1(55, 60, 379, 383), [X0, 76.9, 128.7, X1], 379.6)

cols = ((111.9, 219.6, 115.0), (224.2, 331.6, 226.9), (336.1, 443.5, 338.9), (448.1, X1, 450.8))
strip = ((111.9, 121.5, 133.3, 219.6), (238.9, 238.9, 250.6, 331.6), (348.6, 348.6, 360.3, 443.5),
         (461.1, 468.7, 480.4, X1))
arrows = ((219.6, 238.9), (331.6, 348.6), (443.5, 461.1))
subtags = ((224.2, 295.3, 321.2, 331.6), (336.1, 416.9, 443.5, 443.5), (448.1, 523.8, 549.7, X1))
xs = sorted({X0, 109.6} | {x for c in cols for x in c[:2]} | {x for s in strip for x in s}
            | {x for t in subtags for x in t})
g = Grid("risk", xs, [280, 1170, 280, 2300, 780, 350, 1200, 350, 3670])
g.put(X0, 109.6, 0, 4, lines_in(60, 65, 409, 425), frame("#CCCCCC"), line=1330)
g.put(X0, 109.6, 5, 9, lines_in(60, 75, 465, 480), frame("#CCCCCC"), line=1330)
shades = ("#EDEDED", "#E4E4E4", "#DBDBDB", "#D2D2D2")
for k, ((a, n0, n1, e), shade) in enumerate(zip(strip, shades)):
    head = lines_in(n0 - 4, n1, 404, 408)[0]
    split = head["spans"][1]["bbox"][0]
    if n0 > a:
        g.put(a, n0, 0, 3, [], frame(shade, top="soft"))
    g.put(n0, n1, 0, 1, [], frame(shade, top="soft"))
    g.put(n0, n1, 1, 2, [runs_of(head, x1=split)], OUTLINED, line=1000, fit=False)
    tight(g, n0, 1)
    g.put(n0, n1, 2, 3, [], frame(shade))
    g.put(n1, e, 0, 3, [strip_runs(runs_of(head, x0=split))], frame(shade, top="soft"), align="LEFT")
for k, (a, e) in enumerate(arrows):
    g.put(a, e, 0, 3, "▶", frame(shades[k], top="soft"), size=800, color="#7F7F7F", fit=False)
for k, (a, e, base) in enumerate(cols):
    sep = dict(right="dot") if k < 3 else {}
    g.put(a, e, 3, 4, [line1(a - 1.5, e, 425, 429)], frame(**sep))
    g.put(a, e, 4, 5, "▼", size=700, color="#9A9A9A", line=600, fit=False)
    g.put(a, e, 8, 9, hang(lines_in(a, e, 472, 500), base), frame(**sep), align="LEFT", line=1430)
hatch = dict(hatch="#D9D9D9")
g.put(111.9, 219.6, 5, 8, [line1(111.9, 219.6, 453, 457)], frame("#EEEEEE", **hatch))
for a, t0, t1, e in subtags:
    head = line1(a, t0, 453, 457)
    split = [s for s in head["spans"] if "단계" in s["text"]][0]["bbox"][0] - 0.5
    g.put(a, t0, 5, 8, [strip_runs(runs_of(head, x1=split))], frame("#EEEEEE", **hatch), align="RIGHT")
    g.put(t0, t1, 5, 6, [], frame("#EEEEEE", **hatch))
    g.put(t0, t1, 6, 7, [runs_of(head, WHITE, x0=split)], NEW, line=1000)
    g.put(t0, t1, 7, 8, [], frame("#EEEEEE", **hatch))
    if e > t1:
        g.put(t1, e, 5, 8, [], frame("#EEEEEE", **hatch))
block(g, 402.4)

g = Grid("result-na", [X0, 109.6, X1], [4000])
g.put(X0, 109.6, 0, 1, [line1(62, 68, 523, 527)], frame("#D9D9D9", top="mid", bottom="mid", left="mid"))
g.put(109.6, X1, 0, 1, lines_in(114, 116, 515, 545), frame(top="mid", bottom="mid", right="mid"), align="LEFT",
      line=1650)
block(g, 510.0)

# ---------------------------------------------------------------------------
# 다. Circulate: 기존 / 개선 box, step strip, three 3R boxes, 추진성과
# ---------------------------------------------------------------------------
title = line1(55, 60, 560, 564)
runs = runs_of(title)
g = Grid("title-da", [X0, 76.9, 134.5, 454.7, 506.8, X1], [1700])
g.put(X0, 76.9, 0, 1, [strip_runs(runs[:1])], align="LEFT", line=1450)
g.put(76.9, 134.5, 0, 1, [[runs[1]]], pill)
g.put(134.5, 454.7, 0, 1, [strip_runs(runs[2:])], align="LEFT", line=1450)
g.put(454.7, 506.8, 0, 1, "지적사항 개선", frame("#3C3C3C"), size=760, bold=True, color=WHITE, line=900)
block(g, 561.1)

xs = [X0, 70.4, 89.2, X1]
g = Grid("before-after", xs, [430, 1420, 390, 1420, 310, 1480, 520])
g.put(X0, X1, 0, 1, [], frame(top="soft", left="soft", right="soft"))
for r, y, fill, color in ((1, 590, OUTLINED, INK), (3, 608, NEW, WHITE)):
    line = line1(60, 65, y - 1, y + 2)
    g.put(X0, 70.4, r, r + 1, [runs_of(line, x1=70)], frame(left="soft"), align="RIGHT", line=1260)
    g.put(70.4, 89.2, r, r + 1, [runs_of(line, color, x0=70, x1=88)], fill, line=950, fit=False)
    tight(g, 70.4, r)
    g.put(89.2, X1, r, r + 1, [strip_runs(runs_of(line, x0=88))], frame(right="soft"), align="LEFT", line=1260)
    g.put(X0, X1, r + 1, r + 2, [], frame(left="soft", right="soft"))
g.put(X0, X1, 5, 6, hang([line1(60, 65, 623, 627)], 62.5), frame(left="soft", right="soft"), align="LEFT",
      line=1300)
g.put(X0, X1, 6, 7, [], frame(bottom="soft", left="soft", right="soft"))
block(g, 583.9)

steps = ((X0, 63.5, 95.2, 167.1), (203.0, 203.0, 235.6, 305.0), (321.0, 321.0, 353.8, 441.0),
         (455.5, 455.5, 487.9, X1))
step_arrows = ((188.0, 203.0), (305.0, 321.0), (441.0, 455.5))
shades = ("#F3F3F3", "#E6E6E6", "#D9D9D9", "#C9C9C9")
xs = sorted({x for s in steps for x in s} | {x for a in step_arrows for x in a} | {185.9})
g = Grid("steps", xs, [700, 1170, 710])
for k, ((a, p0, p1, e), shade) in enumerate(zip(steps, shades)):
    line = line1(p0, p1, 655, 659)
    split = p1 - 2.0
    edge = dict(left="soft") if k == 0 else {}
    if p0 > a:
        g.put(a, p0, 0, 3, [], frame(shade, top="soft", bottom="soft", **edge))
    g.put(p0, p1, 0, 1, [], frame(shade, top="soft"))
    g.put(p0, p1, 1, 2, [runs_of(line, x1=split)], OUTLINED, line=1000, fit=False)
    tight(g, p0, 1, 40, 40)
    g.put(p0, p1, 2, 3, [], frame(shade, bottom="soft"))
    edge = dict(right="soft") if k == 3 else {}
    if k == 0:
        new = [s for s in line["spans"] if s["text"] == "신규"][0]["bbox"][0] - 0.5
        g.put(p1, e, 0, 3, [strip_runs(runs_of(line, x0=split, x1=new))], frame(shade, top="soft", bottom="soft"),
              align="LEFT")
        g.put(167.1, 185.9, 0, 1, [], frame(shade, top="soft"))
        g.put(167.1, 185.9, 1, 2, [runs_of(line, x0=new)], OUTLINED, line=950, fit=False)
        tight(g, 167.1, 1)
        g.put(167.1, 185.9, 2, 3, [], frame(shade, bottom="soft"))
        g.put(185.9, 188.0, 0, 3, [], frame(shade, top="soft", bottom="soft"))
    else:
        g.put(p1, e, 0, 3, [strip_runs(runs_of(line, x0=split))], frame(shade, top="soft", bottom="soft", **edge),
              align="LEFT")
for k, (a, e) in enumerate(step_arrows):
    g.put(a, e, 0, 3, "▶", frame(shades[k], top="soft", bottom="soft"), size=800, color="#7F7F7F", fit=False)
block(g, 649.9)


def arrowed(line, lead="  → "):
    runs = runs_of(line)
    return [(lead, runs[0][1], False, INK)] + runs


boxes = ((56.6, 221.3), (223.9, 388.6), (391.1, X1))
xs = sorted({x for b in boxes for x in b})
g = Grid("3r", xs, [2160, 5710])
b1, b2, b3 = (lines_in(a + 3, e, 715, 760) for a, e in boxes)
bodies = (
    [runs_of(b1[0]), arrowed(b1[1]), hang([b1[2]], 62.5)[0]],
    [runs_of(b2[0]), arrowed(b2[1]), arrowed(b2[2])],
    [runs_of(b3[0]), arrowed(b3[1]), [("      ", 1090, False, INK)] + runs_of(b3[2])])
for (a, e), body in zip(boxes, bodies):
    g.put(a, e, 0, 1, [line1(a, e, 693, 697)], frame("#E0E0E0", top="mid", left="mid", right="mid", bottom="soft"))
    g.put(a, e, 1, 2, body, frame(left="mid", right="mid", bottom="mid"), align="LEFT", line=1540)
block(g, 689.6)

g = Grid("result-da", [X0, 109.6, X1], [2720])
g.put(X0, 109.6, 0, 1, [line1(62, 68, 781, 785)], frame("#D9D9D9", top="mid", bottom="mid", left="mid"))
g.put(109.6, X1, 0, 1, [line1(114, 116, 781, 785)], frame(top="mid", bottom="mid", right="mid"), align="LEFT")
block(g, 774.6)

kit.finish(target, end=801.8)
