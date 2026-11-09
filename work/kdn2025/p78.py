"""Rebuild KDN 2025 report page 78 (second PDF local page 28, printed page 50) as editable HWPX.

Usage: python3 work/kdn2025/p78.py <report2.pdf> <out.hwpx> [--page 28]

"Ⅲ. 세부 평가내용별 추진실적" opening page of the 창업 및 경제활성화 indicator: 평가내용 01 band,
section 1 (환경분석 / 추진목표 / STEP 방향·과제 / 협업체계 diagram) and section 2 가. (지원대상 /
니즈 / 추진내용 / 추진성과 three-column table, 대표사례, 주요성과). Built with the shared kit:
one flat table per band at its PDF y, all text from the PDF text layer.

Images in the source and how they are kept: PART box, 평가내용 chip, section number bands,
the hatched label tabs and rounded boxes become cells / fills; the '지적사항 개선' and
'Best Practice' stickers are typed as dark tag cells (icons omitted); the (+) joints -> "+",
the down chevrons -> "▼"; the KDN logo in the footer is typed.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kit  # noqa: E402
from kit import Layout, recipe_inputs  # noqa: E402

source, target = recipe_inputs(28, "협력형 동반진출 체계 구축")
L = Layout(top=3200)
kit.setup(source, L)
from kit import *  # noqa: E402,F401,F403  helpers and presets bound to this page

DARK = "#5E5E5E"
LABEL = frame("#EFEFEF", top="dot", right="soft", hatch="#E0E0E0")
TAGBOX = frame(WHITE, top="soft", bottom="soft", left="soft", right="soft")


def body_lines(x0, x1, y0, y1, indent="  "):
    """Bullet lines as run lists; continuation lines get the source's hanging indent."""
    out = []
    for line in lines_in(x0, x1, y0, y1):
        runs = runs_of(line)
        if not runs[0][0].startswith(("∙", "-", "※")):
            runs = [(indent, runs[0][1], False, INK)] + runs
        out.append(runs)
    return out


def tag(g, x0, x1, r0, r1, content, fill, ratio=88, **kw):
    """Small tag / pill cell: 0.6 pt side padding instead of 5 pt, 장평 fitted to that width."""
    items = content if isinstance(content, list) else [content]
    inner = (to_x(x1) - to_x(x0) - 120) / 100 * 0.96
    for item in items:
        runs = [(item, kw.get("size", 1080))] if isinstance(item, str) else (
            runs_of(item) if isinstance(item, dict) else item)
        need = text_width(runs, ratio)
        if need > inner:
            ratio = int(ratio * inner / need)
    g.put(x0, x1, r0, r1, content, fill, fit=False, ratio=ratio, **kw)
    key = (r0, g.xs.index(to_x(x0)))
    g.items[key] = g.items[key][:7] + (dict(left=60, right=60),)


def section_band(name, num_line, title_line, top, label=None):
    """'2 | heading [sticker]': dark number cell, light gray title band, optional dark tag."""
    xs = [X0, 84.8, 438.0, 496.0, X1] if label else [X0, 84.8, X1]
    g = Grid(name, xs, [2300])
    band = frame("#E2E2E2")
    g.put(X0, 84.8, 0, 1, [runs_of(num_line, WHITE)], frame(DARK), line=1900)
    g.put(84.8, xs[2], 0, 1, [runs_of(title_line)], band, align="LEFT", line=1750)
    if label:
        tag(g, 438.0, 496.0, 0, 1, label, frame("#3C3C3C"), size=820, bold=True, color=WHITE, line=1000)
        g.put(496.0, X1, 0, 1, [], band)
    block(g, top)


# ---------------------------------------------------------------------------
# Page chrome (even page): PART box with rule, footer page number + KDN logo (typed).
# ---------------------------------------------------------------------------
foot = [(line1(55, 60, 816, 822)["text"], 1090, False, INK), ("    ", 790, False, INK),
        ("한전KDN㈜", 1090, True, INK)]
L.add_table([[cell(0, W, 1500, [para(foot, "LEFT", 1300)[0]])]], floating=(5660, 81550))

g = Grid("head", [X0, 99.0, 158.5, X1], [1680])
g.put(X0, 99.0, 0, 1, [[("PART ", 800, False, INK), ("01", 1300, True, INK)]], frame("#EFEFEF", top="strong"))
g.put(99.0, 158.5, 0, 1, "경영관리", frame("#333333"), size=1080, bold=True, color=WHITE)
g.put(158.5, X1, 0, 1, [], frame(bottom="soft"))
block(g, 32.0)

g = Grid("title", [X0, X1], [2400])
g.put(X0, X1, 0, 1, [line1(195, 205, 68, 75)])
block(g, 68.5)

# 평가내용 01 band (chip image typed, title from the text layer)
g = Grid("band", [X0, 124.0, X1], [1650, 1150])
g.put(X0, 124.0, 0, 1, "평가내용 01", frame("#565656", top="strong"), size=970, bold=True, color=WHITE, ratio=80)
g.put(X0, 124.0, 1, 2, [], frame("#E9E9E9", bottom="soft", left="soft", hatch="#DADADA"))
g.put(124.0, X1, 0, 2, lines_in(125, 130, 108, 132), frame("#E9E9E9", top="strong", bottom="soft",
                                                           right="soft", hatch="#DADADA"), align="LEFT", line=1480)
block(g, 106.0)

# ---------------------------------------------------------------------------
# 1. 에너지ICT 중소기업의 수출부터 해외진출까지 ...
# ---------------------------------------------------------------------------
section_band("sec1", line1(64, 70, 148, 152), line1(90, 95, 148, 153), 146.0)

# 환경분석: 내부 + 외부 boxes
xs = [X0, 105.0, 108.0, 129.0, 324.0, 338.0, 359.0, X1]
g = Grid("env", xs, [3900])
g.put(X0, 105.0, 0, 1, [line1(60, 65, 187, 192)], LABEL)
inner = frame("#EEEEEE", top="soft", bottom="soft", left="soft")
body = frame(top="soft", bottom="soft", right="soft")
g.put(108.0, 129.0, 0, 1, [line1(110, 120, 180, 186), line1(110, 120, 193, 199)], inner, line=1300)
g.put(129.0, 324.0, 0, 1, lines_in(130, 140, 178, 212), body, align="LEFT", line=1540)
g.put(324.0, 338.0, 0, 1, "+", size=1500, bold=True, color="#9A9A9A", fit=False)
g.put(338.0, 359.0, 0, 1, [line1(340, 350, 180, 186), line1(340, 350, 193, 199)], inner, line=1300)
g.put(359.0, X1, 0, 1, lines_in(362, 370, 178, 212), body, align="LEFT", line=1540)
block(g, 175.0)

# 추진목표 band
g = Grid("goal", [X0, 105.0, 108.0, X1], [2300])
g.put(X0, 105.0, 0, 1, [line1(60, 65, 222, 227)], LABEL)
g.put(108.0, X1, 0, 1, [line1(155, 165, 220, 228)], frame("#D2D2D2"), line=1500)
block(g, 218.0)

# 추진방향 / 추진과제: two STEP boxes (header with an outlined STEP pill, bullet body)
xs = [X0, 105.0, 108.0, 137.6, 171.6, 330.0, 333.0, 362.9, 397.0, X1]
g = Grid("steps", xs, [250, 1450, 250, 3950])
g.put(X0, 105.0, 0, 3, [line1(60, 65, 247, 253)], LABEL)
g.put(X0, 105.0, 3, 4, [line1(60, 65, 277, 283)], LABEL)
for a, p0, p1, e, lx in ((108.0, 137.6, 171.6, 330.0, 140), (333.0, 362.9, 397.0, X1, 365)):
    head = line1(lx, lx + 5, 247, 253)
    g.put(a, p0, 0, 3, [], frame("#E6E6E6", top="mid", left="mid"))
    g.put(p0, e, 0, 1, [], frame("#E6E6E6", top="mid", right="mid"))
    tag(g, p0, p1, 1, 2, [runs_of(head, x1=p1 - 1)], TAGBOX, line=1000)
    g.put(p1, e, 1, 2, [strip_runs(runs_of(head, x0=p1 - 1))], frame("#E6E6E6", right="mid"),
          align="LEFT", line=1250)
    g.put(p0, e, 2, 3, [], frame("#E6E6E6", right="mid"))
    g.put(a, e, 3, 4, lines_in(lx - 30, lx - 15, 268, 300), frame(left="mid", right="mid", bottom="soft"),
          align="LEFT", line=1540)
block(g, 245.0)

# 협업체계: three boxes (outlined tag + bold name, gray bullet body) joined by "+"
boxes = ((108.0, 139.5, 172.5, 247.0, 140, 115), (262.0, 295.0, 328.0, 401.0, 296, 270),
         (416.0, 432.4, 465.4, X1, 433, 423))
xs = [X0, 105.0, 108.0, 139.5, 172.5, 247.0, 262.0, 295.0, 328.0, 401.0, 416.0, 432.4, 465.4, X1]
g = Grid("partners", xs, [200, 1400, 200, 550, 3400, 300])
g.put(X0, 105.0, 0, 6, [line1(60, 65, 330, 336)], LABEL)
for k, (a, p0, p1, e, lx, bx) in enumerate(boxes):
    head = line1(lx - 2, lx + 3, 310, 316)
    g.put(a, p0, 0, 3, [], frame(top="mid", left="mid"))
    g.put(p0, e, 0, 1, [], frame(top="mid", right="mid"))
    tag(g, p0, p1, 1, 2, [runs_of(head, x1=p1 - 1)], TAGBOX, line=1000)
    g.put(p1, e, 1, 2, [strip_runs(runs_of(head, x0=p1 - 1))], frame(right="mid"), align="LEFT", line=1230)
    g.put(p0, e, 2, 3, [], frame(right="mid"))
    g.put(a, e, 3, 4, [], frame(left="mid", right="mid"))
    g.put(a, e, 4, 5, lines_in(bx - 3, bx + 3, 330, 366), frame("#EBEBEB", left="mid", right="mid"),
          align="LEFT", line=1540)
    g.put(a, e, 5, 6, [], frame(left="mid", right="mid", bottom="mid"))
    if k < 2:
        g.put(e, boxes[k + 1][0], 3, 5, "+", size=1500, bold=True, color="#9A9A9A", fit=False)
block(g, 308.0)

# ---------------------------------------------------------------------------
# 2. 중소기업 해외진출 발판 마련을 위한 맞춤형 해외판로 지원 [지적사항 개선]
# ---------------------------------------------------------------------------
section_band("sec2", line1(64, 70, 387, 392), line1(90, 95, 388, 393), 385.0, label="지적사항 개선")

runs = runs_of(line1(55, 60, 412, 418))
g = Grid("title-ga", [X0, 487.0, X1], [1700])
g.put(X0, 487.0, 0, 1, [runs], align="LEFT", line=1500)
tag(g, 487.0, X1, 0, 1, "Best Practice", frame("#4A4A4A"), size=820, bold=True, color=WHITE, line=1000)
block(g, 413.0)

C = [102.0, 251.5, 254.0, 403.0, 406.0, X1]
COLS = ((102.0, 251.5), (254.0, 403.0), (406.0, X1))

# 추진방향 box
g = Grid("direction", [X0, 99.0, 102.0, X1], [3700])
g.put(X0, 99.0, 0, 1, [line1(58, 62, 446, 452)], LABEL)
g.put(102.0, X1, 0, 1, lines_in(105, 110, 438, 470), frame(top="soft", bottom="soft", left="soft", right="soft"),
      align="LEFT", line=1430)
block(g, 435.0)

# 지원대상: dark tag + bold name per column; 니즈: hatched cells
tag_x = ((146.0, 208.0), (298.0, 360.0), (450.0, 512.0))
xs = [X0, 99.0] + sorted({x for c in COLS for x in c} | {x for t in tag_x for x in t})
g = Grid("target", xs, [1650, 1450, 250, 3400])
g.put(X0, 99.0, 0, 2, [line1(58, 62, 485, 490)], LABEL)
g.put(X0, 99.0, 2, 4, [line1(64, 67, 520, 526)], LABEL)
for (a, e), (t0, t1) in zip(COLS, tag_x):
    g.put(a, t0, 0, 1, [], frame(top="soft"))
    tag(g, t0, t1, 0, 1, [runs_of(line1(t0, t1, 480, 486), WHITE)], frame("#7A7A7A"), line=1050)
    g.put(t1, e, 0, 1, [], frame(top="soft"))
    g.put(a, e, 1, 2, [line1(a, e, 495, 501)], line=1280)
    g.put(a, e, 3, 4, lines_in(a, e, 514, 545), frame("#EDEDED", hatch="#DEDEDE"), line=1310)
block(g, 479.0)

# 추진내용: head band, bullets, ▼, 개선 tag line and follow-up line per column (dotted separators)
improve = ((105, 126.0, 640, 645, 650, 656), (255, 275.5, 639, 644, 650, 656), (408, 427.5, 637, 642, 652, 658))
xs = [X0, 99.0, 102.0, 126.0, 251.5, 254.0, 275.5, 403.0, 406.0, 427.5, X1]
g = Grid("content", xs, [2150, 6050, 800, 1400, 1400, 550])
g.put(X0, 99.0, 0, 6, [line1(58, 62, 603, 608)], LABEL)
for k, ((a, e), (lx, t1, y0, y1, z0, z1)) in enumerate(zip(COLS, improve)):
    sep = dict(right="dot") if k < 2 else {}
    g.put(a, e, 0, 1, [line1(a, e, 552, 558)],
          frame("#E3E3E3", top="soft"), line=1250)
    g.put(a, e, 1, 2,
          body_lines(a, a + 15, 570, 632), frame(**sep), align="LEFT", line=1470)
    g.put(a, e, 2, 3, "▼", frame(**sep), size=700,
          color="#9A9A9A", line=620)
    tag_line = line1(lx, lx + 6, y0, y1)
    tag(g, a, t1, 3, 4, [runs_of(tag_line, WHITE, x1=t1 - 1)], frame("#7A7A7A"), line=1050)
    g.put(t1, e, 3, 4, [strip_runs(runs_of(tag_line, x0=t1 - 1))], frame(**sep),
          align="LEFT", line=1200)
    g.put(a, e, 4, 6,
          [line1(lx, lx + 6, z0, z1)], frame(bottom="soft", **sep), align="LEFT", line=1300)
block(g, 549.0)

# 추진성과: three gray boxes
xs = [X0, 99.0] + C
g = Grid("results", xs, [5300])
g.put(X0, 99.0, 0, 1, [line1(58, 62, 695, 700)], LABEL)
box = frame("#E9E9E9", top="soft", bottom="soft", left="soft", right="soft")
for (a, e), bx in zip(COLS, (107.9, 259.9, 412.0)):
    g.put(a, e, 0, 1, body_lines(bx - 1, bx + 10, 680, 725), box, align="LEFT", line=1430)
block(g, 676.0)

# 대표사례 (label shares the first PDF line with the first bullet)
first = line1(60, 62, 738, 745)
g = Grid("cases", [X0, 99.0, 102.0, X1], [3900])
g.put(X0, 99.0, 0, 1, [runs_of(first, x1=100.0)], frame("#EFEFEF", top="soft", bottom="soft", left="soft"))
g.put(102.0, X1, 0, 1, [strip_runs(runs_of(first, x0=100.0)), line1(104, 106, 753, 758)],
      frame(top="soft", bottom="soft", left="soft", right="soft"), align="LEFT", line=1430)
block(g, 734.0)

# 주요성과
g = Grid("result", [X0, 111.5, X1], [2300])
g.put(X0, 111.5, 0, 1, [runs_of(line1(65, 70, 783, 789), WHITE)], frame("#6A6A6A", top="mid", bottom="mid",
                                                                            left="mid"))
g.put(111.5, X1, 0, 1, [line1(115, 120, 781, 787)], frame(top="mid", bottom="mid", right="mid"), align="LEFT")
block(g, 779.0)

kit.finish(target, end=803.0)
