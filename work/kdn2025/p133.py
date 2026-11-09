"""Rebuild KDN 2025 report page 133 (third PDF local page 33, printed page 93) as editable HWPX.

Usage: python3 work/kdn2025/p133.py <report3.pdf> <out.hwpx> [--page 33]

조직 및 인적자원관리 평가내용 04 (임금피크제) opening page: section 1 (추진방향 + 제도 운영 현황 /
신규채용 목표 운영 table), section 2 가. (Step1 / Step2 boxes), 나. (내부전수 / 외부전파 boxes),
다. (기존 ▶ 개선, the five-step 재취업지원 table, result band) and the 주요성과 box. Built with the
shared kit (one flat table per horizontal band on a grid of PDF x edges); all running text comes
from the PDF text layer, run by run (superscript years / counts stay small runs on the baseline).

Images in the source and how they are kept:
- 평가내용 chip, section number bands, side tab, Step / 내부전수 / 외부전파 pills, the 보직 ... 면접
  tags, the "지적사항 개선" sticker (hand icon dropped): typed cells.
- the gray plus marks (정년연장형 + 58~60세 ... and 고도화 + 2035 NEW) -> "+" runs in gray.
- the bold arrows before 총 23개 ..., 임금피크제 만족도 ..., 교육중심 ... and 교육 중심에서 ... -> "→".
- the chevron between 기존 and 개선 -> ▶ connector cell; the dark circled step numbers -> ①-⑤.
- the small person / checklist illustrations in the 진단 / 성과 boxes and the three tiny chevrons
  above the result bands are decorative and omitted.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kit  # noqa: E402
from kit import Layout, recipe_inputs  # noqa: E402

source, target = recipe_inputs(33, "임금피크제 절감재원으로 신규 채용 인건비 충당")
L = Layout(top=3100)
kit.setup(source, L)
from kit import *  # noqa: E402,F401,F403  helpers and presets bound to this page

DARK, LIGHT, HEAD = "#6A6A6A", "#E4E4E4", "#D9D9D9"
PLUS = "#9A9A9A"
B = 1090             # body size (10.9 pt)


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


def plus(size=B):
    return (" + ", size, True, PLUS)


def arrow(line, lead="  ", size=None):
    """Bold arrow (image in the PDF) in front of a text-layer line."""
    runs = runs_of(line)
    size = size or runs[0][1]
    return [(lead + "→ ", size, True, INK)] + runs


def section_band(name, y, top):
    g = Grid(name, [X0, 85.5, X1], [2300])
    g.put(X0, 85.5, 0, 1, [runs_of(line1(64, 70, y - 2, y + 4), WHITE)], frame(DARK), line=1850)
    g.put(85.5, X1, 0, 1, [line1(90, 95, y - 2, y + 4)], frame(LIGHT), align="LEFT", line=1750)
    block(g, top)


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
    (line1(450, 455, 818, 822)["text"], 790), ("    ", 790), (line1(540, 552, 816, 820)["text"], 1090))]
L.add_table([[cell(0, W, 1500, [para(foot, "RIGHT", 1300)[0]])]], floating=(5660, 81550))

g = Grid("head", [X0, 378.0, X1], [1680])
g.put(X0, 378.0, 0, 1, [], frame(bottom="soft"))
g.put(378.0, X1, 0, 1, [line1(380, 390, 35, 40)], align="RIGHT")
block(g, 32.0)

# 평가내용 04 band (chip image typed, title from the text layer)
g = Grid("band", [X0, 124.0, X1], [1880, 970])
g.put(X0, 124.0, 0, 1, "평가내용 04", frame("#565656", top="strong"), size=970, bold=True, color=WHITE, ratio=80,
      line=1150)
g.put(X0, 124.0, 1, 2, [], frame("#E9E9E9", bottom="soft", left="soft", hatch="#DADADA"))
g.put(124.0, X1, 0, 2, [line1(125, 130, 75, 85)], frame("#E9E9E9", top="strong", bottom="soft", right="soft",
                                                     hatch="#DADADA"), align="LEFT", line=1480)
block(g, 71.0)

# ---------------------------------------------------------------------------
# 1 정부 권고안에 충실한 최적의 임금피크제 제도 설계
# ---------------------------------------------------------------------------
section_band("section-1", 114.4, 111.5)

g = Grid("direction", [X0, 112.9, X1], [2290])
g.put(X0, 112.9, 0, 1, [line1(60, 70, 144, 150)], frame(HEAD, top="mid", bottom="mid", left="mid"))
g.put(112.9, X1, 0, 1, [line1(115, 120, 144, 150)], frame(top="mid", bottom="mid", right="mid"), align="LEFT")
block(g, 139.7)

# 제도 운영 현황 (label | content rows) and 신규채용 목표 운영 table, side by side
LBOX, RBOX = (X0, 99.2, 304.9), (307.5, 311.0, 373.5, 432.5, 492.5, 552.0, X1)
hs = [2150, 1330, 1300, 1290, 1270, 1320, 300]          # y 166.8 .. 256.4
g = Grid("status", [*LBOX, *RBOX], hs)
head_fill = frame(HEAD, top="mid", left="mid", right="mid", bottom="soft")
g.put(X0, 304.9, 0, 1, [line1(100, 110, 170, 175)], head_fill)
g.put(307.5, X1, 0, 1, [line1(340, 345, 170, 175)], head_fill)
rows = lines_in(60, 65, 185, 250)
assert len(rows) == 5, [r["text"] for r in rows]
for r, line in enumerate(rows, 1):
    rule = "soft" if r < 5 else None
    content = runs_of(line, x0=100)
    if r == 1:
        content += [plus(990)] + runs_of(line1(160, 165, 188, 192)) + [plus(990)] + runs_of(line1(235, 240, 188, 192))
    g.put(X0, 99.2, r, r + 1, [runs_of(line, x1=100)], frame(LIGHT, left="mid", bottom=rule), line=1100)
    g.put(99.2, 304.9, r, r + 1, [content], frame(right="mid", bottom=rule), align="LEFT", line=1100)
g.put(X0, 304.9, 6, 7, [], frame(left="mid", right="mid", bottom="mid"))
cols = RBOX[1:-1]
ys = (186.0, 200.0, 213.0, 226.0, 238.0, 251.0)
for r in range(1, 6):
    for c, (a, e) in enumerate(zip(cols, cols[1:])):
        hits = lines_in(a, e, ys[r - 1], ys[r])
        assert len(hits) == 1, (r, c, [h["text"] for h in hits])
        edges = dict(bottom="soft" if 1 < r < 5 else None)
        fill = LIGHT if r == 1 else None
        if c == 0:
            edges["right"] = "soft"
        if c == 2:
            edges.update(left="strong", right="strong", top="strong" if r == 1 else None,
                         bottom="strong" if r == 5 else edges["bottom"])
        g.put(a, e, r, r + 1, [hits[0]], frame(fill, **edges), line=1100)
    g.put(307.5, 311.0, r, r + 1, [], frame(left="mid"))
    g.put(552.0, X1, r, r + 1, [], frame(right="mid"))
g.put(307.5, X1, 6, 7, [], frame(left="mid", right="mid", bottom="mid"))
block(g, 166.8)

# ---------------------------------------------------------------------------
# 2 경험과 전문성의 가치 극대화를 위한 직무･성과 중심 임금피크제 운영
# ---------------------------------------------------------------------------
section_band("section-2", 272.5, 269.6)

ga = line1(85, 90, 297, 301)
g = Grid("title-ga", [X0, 76.9, 134.4, 437.7, 489.8, X1], [1650])
g.put(X0, 76.9, 0, 1, [line1(55, 60, 297, 301)], align="LEFT", line=1450)
g.put(76.9, 134.4, 0, 1, [runs_of(ga, x1=130.0)], pill)
g.put(134.4, 437.7, 0, 1, [strip_runs(runs_of(ga, x0=130.0))], align="LEFT", line=1450)
g.put(437.7, 489.8, 0, 1, "지적사항 개선", frame("#3C3C3C"), size=800, bold=True, color=WHITE, line=950)
tight(g, 437.7, 0, 60, 60)
block(g, 297.0)

# Step1 / Step2 boxes: header with a dark pill, bullet lines, gray result part
SX = [X0, 105.1, 136.8, 304.9, 307.5, 325.3, 356.9, X1]
g = Grid("steps", SX, [1760, 4440, 5000, 300])     # y 320.4 .. 439.8
step_pill = frame("#808080")
for (a, p0, p1, e), y0 in (((X0, 105.1, 136.8, 304.9), 105), ((307.5, 325.3, 356.9, X1), 325)):
    head = line1(y0, y0 + 10, 323, 328)
    split = head["spans"][1]["bbox"][0] - 0.5
    g.put(a, p0, 0, 1, [], frame(top="mid", left="mid", bottom="soft"))
    g.put(p0, p1, 0, 1, [runs_of(head, WHITE, x1=split)], frame("#808080", top="mid", bottom="soft"), line=1050,
          fit=False)
    tight(g, p0, 0)
    g.put(p1, e, 0, 1, [strip_runs(runs_of(head, x0=split))], frame(top="mid", right="mid", bottom="soft"),
          align="LEFT")
g.put(X0, 304.9, 1, 2, [
    runs_of(line1(60, 65, 342, 346)) + [plus()] + runs_of(line1(205, 215, 342, 346)),
    runs_of(line1(60, 65, 355, 359)),
    runs_of(line1(60, 65, 370, 374))], frame(left="mid", right="mid"), align="LEFT", line=1420)
g.put(307.5, X1, 1, 2, hang(lines_in(310, 320, 342, 375), 313.4), frame(left="mid", right="mid"), align="LEFT",
      line=1420)
g.put(X0, 304.9, 2, 3, [runs_of(line1(60, 65, 391, 395)), arrow(line1(75, 85, 405, 410)),
                        runs_of(line1(60, 65, 420, 424))], frame("#E6E6E6", left="mid", right="mid"),
      align="LEFT", line=1430)
g.put(307.5, X1, 2, 3, [runs_of(line1(310, 320, 391, 395)), arrow(line1(325, 335, 405, 410)),
                        runs_of(line1(310, 320, 420, 424))], frame("#E6E6E6", left="mid", right="mid"),
      align="LEFT", line=1430)
g.put(X0, 304.9, 3, 4, [], frame(left="mid", right="mid", bottom="mid"))
g.put(307.5, X1, 3, 4, [], frame(left="mid", right="mid", bottom="mid"))
block(g, 320.4)

# 나. 내부전수 / 외부전파 boxes: header pill, tagged lines, gray result
g = Grid("title-na", [X0, X1], [1650])
g.put(X0, X1, 0, 1, [line1(55, 60, 446, 450)], align="LEFT", line=1450)
block(g, 446.0)

NX = [X0, 62.5, 81.0, 102.0, 136.8, 304.9, 307.5, 313.2, 331.8, 354.5, 389.0, X1]
g = Grid("transfer", NX, [1980, 1460, 1460, 1460, 330, 2950, 300])   # y 469.0 .. 572.9
tag_box = frame(top="soft", bottom="soft", left="soft", right="soft")
for (a, t0, t1, p0, p1, e), (hx, ty) in (((X0, 62.5, 81.0, 102.0, 136.8, 304.9), (105, 64)),
                                         ((307.5, 313.2, 331.8, 354.5, 389.0, X1), (357, 315))):
    head = line1(hx, hx + 5, 472, 477)
    split = head["spans"][1]["bbox"][0] - 0.5
    g.put(a, p0, 0, 1, [], frame(top="mid", left="mid", bottom="soft"))
    g.put(p0, p1, 0, 1, [runs_of(head, WHITE, x1=split)], frame("#7E7E7E", top="mid", bottom="soft"), line=1000,
          fit=False)
    tight(g, p0, 0)
    g.put(p1, e, 0, 1, [strip_runs(runs_of(head, x0=split))], frame(top="mid", right="mid", bottom="soft"),
          align="LEFT")
    for r, y in enumerate((491.9, 506.5, 521.1), 1):
        line = line1(ty, ty + 3, y - 1, y + 1)
        split = line["spans"][1]["bbox"][0] - 0.5
        g.put(a, t0, r, r + 1, [], frame(left="mid"))
        g.put(t0, t1, r, r + 1, [runs_of(line, x1=split)], tag_box, line=950, fit=False)
        tight(g, t0, r)
        g.put(t1, e, r, r + 1, [strip_runs(runs_of(line, x0=split))], frame(right="mid"), align="LEFT", line=1280)
    g.put(a, e, 4, 5, [], frame(left="mid", right="mid"))
    g.put(a, e, 5, 6, lines_in(a, e, 541, 560), frame("#E6E6E6", left="mid", right="mid"), line=1320)
    g.put(a, e, 6, 7, [], frame(left="mid", right="mid", bottom="mid"))
block(g, 469.0)

# ---------------------------------------------------------------------------
# 다. 기존 ▶ 개선, five steps, result band
# ---------------------------------------------------------------------------
g = Grid("title-da", [X0, X1], [1650])
g.put(X0, X1, 0, 1, [line1(55, 60, 579, 583)], align="LEFT", line=1450)
block(g, 579.3)

g = Grid("before-after", [X0, 81.0, 299.2, 310.4, 337.5, X1], [3710])
g.put(X0, 81.0, 0, 1, [line1(60, 65, 607, 610), line1(60, 65, 620, 623)],
      frame(HEAD, top="mid", bottom="mid", left="mid"), line=1320)
g.put(81.0, 299.2, 0, 1, [runs_of(line1(80, 85, 606, 610)), arrow(line1(100, 102, 621, 624), "    ")],
      frame(top="mid", bottom="mid", right="mid"), align="LEFT", line=1400)
g.put(299.2, 310.4, 0, 1, "▶", size=1000, color=ARROW, fit=False)
g.put(310.4, 337.5, 0, 1, [runs_of(line1(318, 321, 607, 610), WHITE), runs_of(line1(318, 321, 620, 623), WHITE)],
      frame("#7F7F7F", top="mid", bottom="mid", left="mid"), line=1320)
g.put(337.5, X1, 0, 1, [runs_of(line1(338, 342, 606, 610)), arrow(line1(355, 360, 621, 624), "    ")],
      frame(top="mid", bottom="mid", right="mid"), align="LEFT", line=1400)
block(g, 602.2)

CX5 = [X0, 156.9, 256.4, 356.0, 455.4, X1]
g = Grid("steps5", CX5, [1910, 210, 1730, 2920, 1840, 200])     # y 643.5 .. 731.6
g.put(X0, 256.4, 0, 1, [line1(80, 85, 646, 650)], frame(HEAD, top="mid", left="mid", right="soft"))
g.put(256.4, X1, 0, 1, [line1(330, 335, 646, 650)], frame(HEAD, top="mid", right="mid"))
g.put(X0, X1, 1, 2, [], frame(left="mid", right="mid"))
title_lines = sorted(lines_in(70, 560, 666, 670), key=lambda l: l["bbox"][0])
assert len(title_lines) == 5, [t["text"] for t in title_lines]
for k, (a, e) in enumerate(zip(CX5, CX5[1:])):
    side = dict(left="mid" if k == 0 else None, right="mid" if k == 4 else "dot")
    g.put(a, e, 2, 3, [[("①②③④⑤"[k] + " ", B, False, INK)] + runs_of(title_lines[k])], frame("#E3E3E3", **side),
          line=1270)
    g.put(a, e, 3, 4, hang(lines_in(a, e - 5, 683, 700), a + 5.8), frame(**side), align="LEFT", line=1320)
    g.put(a, e, 4, 5, [line1(a, e - 5, 713, 716)], frame("#EEEEEE", hatch="#DEDEDE", **side), line=1150)
    g.put(a, e, 5, 6, [], frame(bottom="mid", left=side["left"], right=side["right"] if k == 4 else None))
block(g, 643.5)

g = Grid("result", [X0, X1], [2440])
g.put(X0, X1, 0, 1, [line1(120, 125, 736, 740)], frame("#CBCBCB"), line=1400)
block(g, 734.6)

g = Grid("key-results", [X0, 112.9, X1], [3720])
g.put(X0, 112.9, 0, 1, [runs_of(line1(60, 70, 777, 780), WHITE)], frame("#7F7F7F", top="mid", bottom="mid", left="mid"))
g.put(112.9, X1, 0, 1, lines_in(115, 120, 768, 790), frame(top="mid", bottom="mid", right="mid"), align="LEFT",
      line=1550)
block(g, 765.3)

kit.finish(target, end=802.5)
