"""Rebuild KDN 2025 report page 80 (second PDF local page 30, printed page 52) as editable HWPX.

Usage: python3 work/kdn2025/p80.py <report2.pdf> <out.hwpx> [--page 30]

창업 및 경제활성화, 평가내용 02 opening page. Built with the shared diagram kit (one flat table
per horizontal band on a grid of PDF x edges). Nearly all text is in the PDF text layer and is
taken from it. Images typed here: the PART box, the '평가내용 02' chip, the 'Best Practice'
badge (trophy dropped), the '지적사항 개선' sticker (hand icon dropped) and the boxed task
numbers (1, 2 -> ① ②, numbering kept as printed: 1 2 | 1 2). The ① ② ③ before the 품질 headings
are images too. The ➡ arrow between '데이터 발굴 협의체' and 'Top-Down' (a gap in the text
layer) becomes →; chevrons, round arrow icons and the (+) joints become ▶ / ▼ / + cells.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kit  # noqa: E402
from kit import Layout, recipe_inputs  # noqa: E402

source, target = recipe_inputs(30, "민간수요 맞춤형 개방체계 구축, 협업데이터 공동생산 협력체계 구축")
L = Layout(top=3100)
kit.setup(source, L)
from kit import *  # noqa: E402,F401,F403  helpers and presets bound to this page

DARK, LABEL = "#6A6A6A", "#E6E6E6"
SIDE = frame("#ECECEC", top="dot", hatch="#DDDDDD")       # hatched row labels of section 1
HEAD = frame("#E2E2E2", top="mid", left="mid", right="mid")
PILL = frame(WHITE, top="soft", bottom="soft", left="soft", right="soft")


def hang(lines, base, extra=None):
    """Bullet lines keep their PDF indent: spaces for the x offset and for the line's own lead."""
    out = []
    for l in lines:
        runs = runs_of(l)
        if extra:
            runs = [(extra(t), *rest) for t, *rest in runs]
        size = runs[0][1] / 100
        raw = "".join(s["text"] for s in l["spans"])
        offset = l["bbox"][0] - base + (len(raw) - len(raw.lstrip(" "))) * 0.29 * size
        n = max(0, round(offset / (0.29 * size)))
        out.append([(" " * n, runs[0][1], False, INK)] + runs if n else runs)
    return out


def tight(g, x0, r0, left=60, right=60):
    """Narrow the cell padding (kit cells use the builder default 320/180)."""
    c0 = g.xs.index(to_x(x0))
    item = g.items[r0, c0]
    g.items[r0, c0] = (*item[:7], dict(left=left, right=right))


def lead(glyph, runs):
    runs = list(runs)
    return [(glyph + " ", runs[0][1], True, INK)] + runs


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

g = Grid("banner", [X0, 124.0, X1], [2860])
g.put(X0, 124.0, 0, 1, [[("평가내용 ", 800, True, WHITE), ("02", 1350, True, WHITE)]], frame("#686868"),
      line=1500)
g.put(124.0, X1, 0, 1, [line1(125, 130, 76, 80)], striped, align="LEFT", line=1450)
block(g, 70.9)

g = Grid("sec1", [X0, 84.5, X1], [2300])
g.put(X0, 84.5, 0, 1, [runs_of(line1(60, 70, 112, 118), WHITE)], frame(DARK), line=1700)
g.put(84.5, X1, 0, 1, [line1(90, 95, 113, 118)], frame(LABEL), align="LEFT", line=1700)
block(g, 111.5)

# ---------------------------------------------------------------------------
# Section 1 framework (text layer): 환경분석 / 추진방향 / 추진과제 / 실행체계
# ---------------------------------------------------------------------------
B = ((107.6, 255.4), (257.9, 405.7), (408.1, X1))
xs = [X0, 105.4, 107.6, 199.9, 228.5, 255.4, 257.9, 405.7, 408.1, X1]
g = Grid("env", xs, [1920, 1950, 1550, 440])
g.put(X0, 105.4, 0, 4, [line1(60, 65, 162, 168)], SIDE, bold=True)
body = dict(left="mid", right="mid")
for k, (a, e) in enumerate(B):
    g.put(a, e, 0, 1, [line1(a, e, 144, 150)], frame(WHITE, top="mid", **body))
    if k:
        g.put(a, e, 1, 4, [hang([l], a + 6.0)[0] for l in lines_in(a, e, 165, 190)],
              frame("#EBEBEB", bottom="mid", **body), align="LEFT", line=1540)
g.put(107.6, 255.4, 1, 2, [line1(150, 160, 165, 170)], frame("#EBEBEB", left="mid", right="mid"))
second = line1(130, 140, 180, 185)
g.put(107.6, 199.9, 2, 3, [runs_of(second, x1=201.0)], frame("#EBEBEB", left="mid"), align="RIGHT")
g.put(199.9, 228.5, 2, 3, [runs_of(second, x0=201.0)], PILL)
tight(g, 199.9, 2)
g.put(228.5, 255.4, 2, 3, [], frame("#EBEBEB", right="mid"))
g.put(107.6, 255.4, 3, 4, [], frame("#EBEBEB", left="mid", right="mid", bottom="mid"))
block(g, 140.8)

g = Grid("direction", [X0, 105.4, 107.6, 331.7, X1], [2330])
g.put(X0, 105.4, 0, 1, [line1(60, 65, 207, 212)], SIDE, bold=True)
g.put(107.6, 331.7, 0, 1, [line1(160, 170, 207, 212)], frame("#D9D9D9", right="dot"))
g.put(331.7, X1, 0, 1, [line1(380, 390, 207, 212)], frame("#D9D9D9"))
block(g, 203.1)

g = Grid("tasks", [X0, 105.4, 107.6, 331.7, X1], [3840])
g.put(X0, 105.4, 0, 1, [line1(60, 65, 241, 247)], SIDE, bold=True)
for (a, e, x), kw in (((107.6, 331.7, 120.0), dict(left="mid", right="dot")), ((331.7, X1, 345.0), dict(right="mid"))):
    items = lines_in(x, x + 10, 234, 256)
    g.put(a, e, 0, 1, [lead(n, runs_of(l)) for n, l in zip("①②", items)],
          frame(top="mid", bottom="mid", **kw), align="LEFT", line=1540)
block(g, 230.0)

E3 = ((107.6, 247.7), (261.5, 401.6), (415.4, X1))
g = Grid("exec", [X0, 105.4, 107.6, 247.7, 261.5, 401.6, 415.4, X1], [1800, 3940])
g.put(X0, 105.4, 0, 2, [line1(60, 65, 293, 298)], SIDE, bold=True)
for k, (a, e) in enumerate(E3):
    g.put(a, e, 0, 1, [line1(a, e, 275, 281)], HEAD, bold=True)
    g.put(a, e, 1, 2, hang(lines_in(a, a + 10, 294, 315), a + 6.0), frame(left="mid", right="mid", bottom="mid"),
          align="LEFT", line=1540)
    if k < 2:
        g.put(e, E3[k + 1][0], 0, 2, "▶", size=1100, color="#BDBDBD")
block(g, 271.8)

# ---------------------------------------------------------------------------
# Section 2 (text layer): title band with the typed 'Best Practice' badge
# ---------------------------------------------------------------------------
g = Grid("sec2", [X0, 84.5, 480.2, 550.8, X1], [2300])
g.put(X0, 84.5, 0, 1, [runs_of(line1(60, 70, 346, 352), WHITE)], frame(DARK), line=1700)
g.put(84.5, 480.2, 0, 1, [line1(90, 95, 347, 352)], frame(LABEL), align="LEFT", line=1700)
g.put(480.2, 550.8, 0, 1, "Best Practice", frame("#4A4A4A"), size=820, bold=True, color=WHITE)
g.put(550.8, X1, 0, 1, [], frame(LABEL))
block(g, 345.2)

g = Grid("background", [X0, 111.7, X1], [3720])
g.put(X0, 111.7, 0, 1, [line1(65, 70, 385, 390)], frame("#DCDCDC", top="mid", bottom="mid", left="mid"))
g.put(111.7, X1, 0, 1, lines_in(115, 120, 378, 398), frame(top="mid", bottom="mid", right="mid", left="soft"),
      align="LEFT", line=1540)
block(g, 374.4)

# Track-1 + Track-2 cards
xs = [X0, 118.5, 139.0, 176.5, 299.5, 313.4, 375.0, 396.0, 433.4, X1]
g = Grid("tracks", xs, [1870, 3970])
t1, t2 = line1(140, 150, 420, 425), line1(400, 410, 421, 426)
g.put(X0, 118.5, 0, 1, [runs_of(line1(60, 70, 421, 427), WHITE)], frame("#5E5E5E"))
g.put(118.5, 139.0, 0, 1, [], frame("#E4E4E4"))
g.put(139.0, 176.5, 0, 1, [runs_of(t1, x1=172.0)], PILL)
tight(g, 139.0, 0)
g.put(176.5, 299.5, 0, 1, [strip_runs(runs_of(t1, x0=172.0))], frame("#E4E4E4"), align="LEFT")
g.put(313.4, 375.0, 0, 1, [runs_of(line1(320, 330, 421, 427), WHITE)], frame("#5E5E5E"))
g.put(375.0, 396.0, 0, 1, [], frame("#E4E4E4"))
g.put(396.0, 433.4, 0, 1, [t2], PILL)
tight(g, 396.0, 0)
g.put(433.4, X1, 0, 1, [line1(433, 440, 420, 426)], frame("#E4E4E4"), align="LEFT")
side = dict(left="mid", right="mid", bottom="mid")
g.put(X0, 299.5, 1, 2, hang(lines_in(60, 65, 441, 462), 62.5), frame(**side), align="LEFT", line=1540)
g.put(299.5, 313.4, 0, 2, "+", size=1500, bold=True, color="#9A9A9A", fit=False)
g.put(313.4, X1, 1, 2, hang(lines_in(318, 322, 441, 462), 319.4, lambda t: t.replace("협의체  ", "협의체 → ")),
      frame(**side), align="LEFT", line=1540)
block(g, 417.9)

g = Grid("summary", [X0, X1], [1570, 1140])
g.put(X0, X1, 0, 1, [line1(145, 155, 477, 482)], line=1150)
g.put(X0, X1, 1, 2, "▼", frame("#F0F0F0"), size=900, color=ARROW, line=960)
block(g, 476.3)

# ---------------------------------------------------------------------------
# ① 데이터 개방·활용 확대: 실적1 / 실적2 / 실적3 cards
# ---------------------------------------------------------------------------
GRADE = frame("#E3E3E3")


def label(g, rows, ys, glyph, x=(60, 112)):
    lines = lines_in(x[0], x[1], *ys)
    pars = [lead(glyph, runs_of(lines[0]))] + [runs_of(l) for l in lines[1:]]
    g.put(X0, 113.6, 0, rows, pars, GRADE, bold=True, line=1320)


C3 = ((116.2, 261.0), (263.5, 408.5), (410.9, X1))
xs = [X0, 113.6, 116.2, 124.0, 155.6, 199.5, 254.5, 261.0, 263.5, 298.2, 329.9, 408.5, 410.9, 430.6, 462.3, X1]
g = Grid("results", xs, [1740, 6990])
label(g, 2, (525, 562), "①")
first = line1(125, 135, 508, 513)
g.put(116.2, 124.0, 0, 1, [], frame(top="mid", left="mid"))
g.put(124.0, 155.6, 0, 1, [runs_of(first, x1=152.0)], PILL)
tight(g, 124.0, 0)
g.put(155.6, 199.5, 0, 1, [strip_runs(runs_of(first, x0=152.0))], frame(top="mid"))
tight(g, 155.6, 0, 40, 20)
g.put(199.5, 254.5, 0, 1, "지적사항 개선", frame("#3C3C3C"), size=740, bold=True, color=WHITE, line=900)
tight(g, 199.5, 0, 40, 40)
g.put(254.5, 261.0, 0, 1, [], frame(top="mid", right="mid"))
for (a, e), (p0, p1), x in (((263.5, 408.5), (298.2, 329.9), 300), ((410.9, X1), (430.6, 462.3), 433)):
    head = line1(x, x + 8, 508, 513)
    g.put(a, p0, 0, 1, [], frame(top="mid", left="mid"))
    g.put(p0, p1, 0, 1, [runs_of(head, x1=p1 - 3.0)], PILL)
    tight(g, p0, 0)
    g.put(p1, e, 0, 1, [strip_runs(runs_of(head, x0=p1 - 3.0))], frame(top="mid", right="mid"), align="LEFT")
for a, e in C3:
    g.put(a, e, 1, 2, hang(lines_in(a, a + 10, 527, 580), a + 5.8), frame(left="mid", right="mid", bottom="mid"),
          align="LEFT", line=1540)
block(g, 505.2)

# ② 데이터 활용도 개선: Step1 ▶ Step2 ▶ Step3
xs = [X0, 113.6, 116.2, 131.9, 163.6, 259.3, 261.0, 276.6, 284.7, 316.4, 407.4, 410.9, 424.7, 430.3, 462.0, X1]
g = Grid("steps", xs, [410, 1870, 3830])
label(g, 3, (612, 640), "②")
STEP = frame("#E6E6E6")
for (a, e, p0, p1, x), fill, pill_fill, color in (
        ((116.2, 259.3, 131.9, 163.6, 136), STEP, PILL, INK),
        ((276.6, 407.4, 284.7, 316.4, 289), STEP, PILL, INK),
        ((424.7, X1, 430.3, 462.0, 434), frame("#D2D2D2"), frame("#6E6E6E"), WHITE)):
    head = line1(x, x + 5, 598, 605)
    g.put(a, p0, 1, 2, [], fill)
    g.put(p0, p1, 1, 2, [runs_of(head, color, x1=p1 - 3.0)], pill_fill)
    tight(g, p0, 1)
    g.put(p1, e, 1, 2, [strip_runs(runs_of(head, x0=p1 - 3.0))], fill, align="LEFT")
g.put(259.3, 276.6, 1, 2, "▶", size=900, color="#9A9A9A")
g.put(407.4, 424.7, 1, 2, "▶", size=900, color="#9A9A9A")
for k, (a, e) in enumerate(((116.2, 261.0), (261.0, 410.9), (410.9, X1))):
    g.put(a, e, 2, 3, hang(lines_in(a, a + 12, 618, 640), a + 3.0), frame(left="dot" if k else None, bottom="mid"),
          align="LEFT", line=1540)
block(g, 592.5)

# ③ 데이터 품질 개선: banner, three numbered headings, value boxes joined by +
xs = [X0, 113.6, 116.2, 123.3, 138.0, 163.5, 184.5, 205.6, 231.0, 253.2, 266.9, 404.3, 418.0, 548.8, X1]
g = Grid("quality", xs, [400, 2070, 2040, 640, 1200, 2440])
label(g, 6, (690, 710), "③")
HATCH = frame("#EEEEEE", hatch="#DEDEDE")
g.put(116.2, 123.3, 1, 2, [], HATCH)
g.put(123.3, 548.8, 1, 2, [line1(130, 140, 663, 668)], frame(WHITE, top="mid", left="mid", right="mid"))
g.put(548.8, X1, 1, 2, [], HATCH)
for (a, e), num in zip(((116.2, 253.2), (266.9, 404.3), (418.0, X1)), "①②③"):
    g.put(a, e, 2, 3, [lead(num, runs_of(line1(a, e, 684, 690)))], frame(top="soft"), bold=True)
    if a > 120:
        g.put(a, e, 3, 6, hang(lines_in(a, a + 10, 706, 728), a + 5.8), frame("#EBEBEB"), align="LEFT", line=1540)
BOX = frame("#EBEBEB")
g.put(116.2, 184.5, 3, 4, [], BOX)
g.put(184.5, 253.2, 3, 4, [], BOX)
g.put(116.2, 138.0, 4, 5, [], BOX)
g.put(138.0, 163.5, 4, 5, [line1(140, 150, 708, 713)], PILL, line=1000)
tight(g, 138.0, 4, 20, 20)
g.put(163.5, 184.5, 4, 5, [], BOX)
g.put(184.5, 205.6, 4, 5, [], BOX)
g.put(205.6, 231.0, 4, 5, [runs_of(line1(208, 215, 708, 713), WHITE)], frame("#7A7A7A"), line=1000)
tight(g, 205.6, 4, 20, 20)
g.put(231.0, 253.2, 4, 5, [], BOX)
g.put(116.2, 184.5, 5, 6, [line1(120, 130, 721, 727)], frame("#EBEBEB", right="dot"))
g.put(184.5, 253.2, 5, 6, [line1(190, 195, 721, 727)], BOX)
for a, e in ((253.2, 266.9), (404.3, 418.0)):
    g.put(a, e, 3, 6, "+", size=1500, bold=True, color="#9A9A9A", fit=False)
block(g, 653.6)

# 점검·환류
xs = [X0, 113.6, 116.2, 238.0, 410.9, X1]
g = Grid("feedback", xs, [420, 2700])
g.put(X0, 113.6, 0, 2, [runs_of(line1(60, 70, 754, 760), WHITE)], frame("#8A8A8A"), line=1320)
for k, (a, e) in enumerate(((116.2, 238.0), (238.0, 410.9), (410.9, X1))):
    g.put(a, e, 1, 2, [line1(a, e, 751, 758)], frame("#E6E6E6", left="soft" if k else None))
block(g, 741.5)

# ---------------------------------------------------------------------------
# 주요성과
# ---------------------------------------------------------------------------
g = Grid("result", [X0, 111.7, X1], [2300])
g.put(X0, 111.7, 0, 1, [runs_of(line1(65, 70, 783, 788), WHITE)], frame("#6A6A6A", top="mid", bottom="mid", left="mid"))
g.put(111.7, X1, 0, 1, [line1(115, 120, 783, 788)], frame(top="mid", bottom="mid", right="mid"), align="LEFT")
block(g, 779.1)

kit.finish(target, end=803.0)
