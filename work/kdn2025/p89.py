"""Rebuild KDN 2025 report page 89 (2nd PDF local page 39, printed page 59) as editable HWPX.

Usage: python3 work/kdn2025/p89.py <report2.pdf> <out.hwpx> [--page 39]

상생･협력 및 지역발전, section 2 (중소기업 全주기 기술협력 체계 / ESG 통합 관리시스템 성공사례).
Built with the shared kit (one flat table per band on a grid of PDF x edges); all text comes from
the PDF text layer. Images and how they are kept:
- side tab, section-2 number band and the 'Best Practice' sticker (trophy icon dropped): typed.
- the dark tab strips over the 협업체계 heads and the slanted head shapes: plain borders / fills
  (Step heads get light-to-dark gray fills as printed); the round arrow badges -> ▶, the grey
  chevrons -> ▶, the big + signs -> +.
- the large decorative quote marks around the testimonial: dropped (the quote's own “ ” stay);
  the testimonial lines are set in italic as printed.
- text-layer tags (Step pills, 목표, AS-IS / TO-BE, 지원 / 실증 / 도입 / 확대 / 결과) are separate
  cells: outlined white for the light tags, dark fill for the dark ones.
"""

import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kit  # noqa: E402
from kit import Layout, recipe_inputs  # noqa: E402

source, target = recipe_inputs(39, "중소기업 全주기 기술협력 체계 구축 및 기관 주도")
L = Layout(top=3100)
kit.setup(source, L)
from kit import *  # noqa: E402,F401,F403  helpers and presets bound to this page

DARK, LABEL, HEAD = "#6A6A6A", "#E3E3E3", "#D9D9D9"
BOXED = frame(WHITE, top="soft", bottom="soft", left="soft", right="soft")
TAG_DARK = frame("#7A7A7A")
HATCH = frame("#EEEEEE", hatch="#E2E2E2")


def hang(lines, base):
    """Bullet lines keep their PDF indent: spaces for the x offset and for the line's own lead."""
    out = []
    for l in lines:
        runs = runs_of(l)
        size = runs[0][1] / 100
        raw = "".join(s["text"] for s in l["spans"])
        offset = l["bbox"][0] - base + (len(raw) - len(raw.lstrip(" "))) * 0.29 * size
        n = max(0, round(offset / (0.29 * size)))
        out.append([(" " * n, runs[0][1], False, INK)] + runs if n else runs)
    return out


def italic(grid, key, par_index):
    """Set every run of one paragraph of a placed cell in italic (charPr copy + <hh:italic/>)."""
    par = grid.items[key][3][par_index]
    for run in par.findall(L.q("hp:run")):
        base = L.characters.find(f"hh:charPr[@id='{run.get('charPrIDRef')}']", L.ns)
        el = deepcopy(base)
        L.sub(el, "hh:italic")
        run.set("charPrIDRef", L.append_style(L.characters, el))


def key(grid, x0, r0):
    return r0, grid.xs.index(to_x(x0))


def boxed(name, label_line, body, top, height, label_fill, label_color):
    """추진배경 / 주요성과 box: label at left, outlined body with bullet lines."""
    g = Grid(name, [X0, 111.7, X1], [height])
    g.put(X0, 111.7, 0, 1, [runs_of(label_line, label_color)], frame(label_fill, top="mid", bottom="mid", left="mid"))
    g.put(111.7, X1, 0, 1, body, frame(top="mid", bottom="mid", right="mid"), align="LEFT")
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

g = Grid("head", [X0, 375.0, X1], [1680])
g.put(X0, 375.0, 0, 1, [], frame(bottom="soft"))
g.put(375.0, X1, 0, 1, [line1(375, 385, 35, 40)], align="RIGHT")
block(g, 32.0)

# Section 2 band (image): dark number, light title, 'Best Practice' sticker.
g = Grid("sec2", [X0, 84.5, 480.0, X1], [2300])
g.put(X0, 84.5, 0, 1, [runs_of(line1(60, 70, 72, 77), WHITE)], frame(DARK), line=1700)
g.put(84.5, 480.0, 0, 1, [line1(90, 95, 72, 78)], frame("#E6E6E6"), align="LEFT", line=1700)
g.put(480.0, X1, 0, 1, "Best Practice", frame("#4A4A4A"), size=900, bold=True, color=WHITE)
block(g, 70.9)

g = Grid("title-ga", [X0, X1], [1650])
g.put(X0, X1, 0, 1, [line1(55, 60, 100, 105)], align="LEFT", line=1450)
block(g, 101.0)

boxed("background", line1(65, 70, 134, 139), lines_in(115, 120, 126, 150), 123.2, 3710, "#D5D5D5", INK)

# ---------------------------------------------------------------------------
# 추진 방안: 목표 band, 협업체계 (three shares joined by +), KDN 실행 모델 (Step1-4).
# ---------------------------------------------------------------------------
share_cols = ((143.1, 291.0), (304.6, 424.4), (437.8, 551.9))
heads = ((143.1, 242.3, 176.9, 211.5), (259.6, 345.8, 285.4, 319.9), (363.1, 449.2, 388.9, 423.4),
         (466.6, 551.9, 490.6, 525.2))
arrows = ((242.3, 259.6), (345.8, 363.1), (449.2, 466.6))
bodies = ((143.1, 244.5, 146.2), (244.5, 348.0, 249.6), (348.0, 451.5, 353.0), (451.5, 551.9, 456.5))
goals = (148.0, 251.5, 355.0, 458.4)
xs = sorted({X0, 99.4, 102.0, 143.1, 551.9, X1}
            | {x for c in share_cols for x in c}
            | {x for h in heads for x in h} | {x for b in bodies for x in b[:2]}
            | {x for t in goals for x in (t - 3.0, t + 18.5)})
hs = [4010, 620, 2180, 3600, 1620, 630, 450, 1200, 1540, 3550, 2410, 250]
g = Grid("plan", xs, hs)
g.put(X0, 99.4, 0, 12, lines_in(60, 70, 260, 285), frame(LABEL), bold=True)
g.put(99.4, 102.0, 0, 12, [])
box = dict(top="mid", bottom="mid")
g.put(102.0, 143.1, 0, 1, [line1(110, 115, 177, 183)], frame(left="mid", right="dot", **box))
g.put(102.0, 143.1, 1, 2, [])
g.put(102.0, 143.1, 2, 5, lines_in(110, 115, 234, 253), frame(left="mid", right="dot", **box))
g.put(102.0, 143.1, 5, 6, [])
g.put(102.0, 143.1, 6, 12, lines_in(110, 115, 318, 350), frame(left="mid", right="dot", **box))
g.put(551.9, X1, 0, 1, [], frame(right="mid", **box))
g.put(551.9, X1, 1, 2, [])
g.put(551.9, X1, 2, 5, [], frame(right="mid", **box))
g.put(551.9, X1, 5, 6, [])
g.put(551.9, X1, 6, 12, [], frame(right="mid", **box))
# 목표
g.put(143.1, 551.9, 0, 1, lines_in(160, 210, 170, 190), frame("#E3E3E3", **box), line=1330)
g.put(143.1, 551.9, 1, 2, [])
# 협업체계: heads, hatched shares with + between, footnote
for k, (a, e) in enumerate(share_cols):
    g.put(a, e, 2, 3, [line1(a, e, 218, 224)], frame(top="mid"))
    g.put(a, e, 3, 4, lines_in(a, e, 236, 256), HATCH, line=1450)
    if k < 2:
        b = share_cols[k + 1][0]
        g.put(e, b, 2, 3, [], frame(top="mid"))
        g.put(e, b, 3, 4, "+", size=1500, bold=True, color="#9A9A9A", fit=False)
g.put(143.1, 551.9, 4, 5, [line1(140, 145, 270, 276)], frame(bottom="mid"), align="LEFT")
g.put(143.1, 551.9, 5, 6, [])
# KDN 실행 모델: Step heads (pill + title), arrows, bodies, 목표 tags
g.put(143.1, 551.9, 6, 7, [], frame(top="mid"))
fills = ("#F0F0F0", "#E4E4E4", "#D6D6D6", "#C8C8C8")
for k, ((a, e, p0, p1), fill) in enumerate(zip(heads, fills)):
    step = lines_in(p0, p1, 295, 302)
    assert len(step) == 1
    g.put(a, p0, 7, 8, [], frame(fill))
    g.put(p0, p1, 7, 8, step, BOXED)
    g.put(p1, e, 7, 8, [], frame(fill))
    g.put(a, e, 8, 9, [line1(a, e, 308, 313)], frame(fill))
for a, e in arrows:
    g.put(a, e, 7, 9, "▶", size=900, color="#8C8C8C")
for k, ((a, e, base), t) in enumerate(zip(bodies, goals)):
    sep = dict(right="dot") if k < 3 else {}
    g.put(a, e, 9, 10, hang(lines_in(a, e, 326, 350), base), frame(**sep), align="LEFT", line=1440)
    goal = line1(t - 1, t + 1, 364, 369)
    g.put(a, t - 3.0, 10, 11, [], HATCH)
    g.put(t - 3.0, t + 18.5, 10, 11, [runs_of(goal, x1=t + 16)], BOXED, line=1000)
    g.put(t + 18.5, e, 10, 11, [strip_runs(runs_of(goal, x0=t + 16))], HATCH, align="LEFT")
g.put(143.1, 551.9, 11, 12, [], frame(bottom="mid"))
block(g, 165.5)

# ---------------------------------------------------------------------------
# 기대효과: three boxes with AS-IS (outlined) / TO-BE (dark) tags.
# ---------------------------------------------------------------------------
cols = ((102.0, 251.5), (254.0, 403.6), (406.1, X1))
xs = sorted({X0, 99.4} | {x for a, e in cols for x in (a, a + 4.5, a + 33.5, e)})
g = Grid("effect", xs, [1920, 1750, 1750, 2800])
g.put(X0, 99.4, 0, 4, lines_in(60, 70, 418, 440), frame(LABEL), bold=True)
side = dict(left="mid", right="mid")
for a, e in cols:
    g.put(a, e, 0, 1, [line1(a, e, 394, 400)], frame(HEAD, top="mid", **side))
    for r, y, fill, color in ((1, 418, BOXED, INK), (2, 436, TAG_DARK, WHITE)):
        line = line1(a, a + 15, y - 1, y + 2)
        g.put(a, a + 4.5, r, r + 1, [], frame(left="mid"))
        g.put(a + 4.5, a + 33.5, r, r + 1, [runs_of(line, color, x1=a + 29.5)], fill, line=900, fit=False)
        g.put(a + 33.5, e, r, r + 1, [strip_runs(runs_of(line, x0=a + 29.5))], frame(right="mid"), align="LEFT")
    g.put(a, e, 3, 4, [line1(a, e, 452, 457)], frame(bottom="mid", **side))
block(g, 391.3)

# ---------------------------------------------------------------------------
# 나. 성공사례: four stage boxes (tagged lines), testimonial, three result boxes.
# ---------------------------------------------------------------------------
g = Grid("title-na", [X0, X1], [1650])
g.put(X0, X1, 0, 1, [line1(55, 60, 483, 488)], align="LEFT", line=1450)
block(g, 483.5)

stages = ((56.6, 171.0), (184.9, 299.3), (313.1, 427.5), (441.4, X1))
xs = sorted({x for a, e in stages for x in (a, a + 5.5, a + 25.0, e)})
g = Grid("stages", xs, [1920, 1500, 1550, 1500, 2020])
side = dict(left="mid", right="mid")
for k, (a, e) in enumerate(stages):
    g.put(a, e, 0, 1, [line1(a, e, 508, 514)], frame(top="mid", bottom="soft", **side))
    for r, (y0, y1), fill, color in ((1, (527, 533), BOXED, INK), (3, (558, 564), TAG_DARK, WHITE)):
        line = line1(a + 5, a + 10, y0, y1)
        g.put(a, a + 5.5, r, r + 1, [], frame(left="mid"))
        g.put(a + 5.5, a + 25.0, r, r + 1, [runs_of(line, color, x1=a + 23.0)], fill, line=1000)
        g.put(a + 25.0, e, r, r + 1, [strip_runs(runs_of(line, x0=a + 23.0))], frame(right="mid"), align="LEFT")
    for r, (y0, y1) in ((2, (541, 548)), (4, (572, 579))):
        sub = [[(" ", 880, False, INK)] + runs_of(l) for l in lines_in(a + 20, e, y0, y1)]
        last = dict(bottom="mid") if r == 4 else {}
        g.put(a, a + 25.0, r, r + 1, [], frame(left="mid", **last))
        g.put(a + 25.0, e, r, r + 1, sub, frame(right="mid", **last), align="LEFT")
    if k < 3:
        g.put(e, stages[k + 1][0], 1, 5, "▶", size=1100, color=ARROW)
block(g, 505.8)

g = Grid("quote", [X0, X1], [400, 5200, 400])
g.put(X0, X1, 0, 1, [], frame(top="mid"))
g.put(X0, X1, 1, 2, lines_in(60, 215, 604, 645), frame("#F0F0F0"), line=1600)
g.put(X0, X1, 2, 3, [], frame(bottom="mid"))
italic(g, key(g, X0, 1), 0)
italic(g, key(g, X0, 1), 1)
block(g, 599.0)

results = ((56.6, 221.3), (223.9, 388.6), (391.1, X1))
xs = sorted({x for a, e in results for x in (a, a + 25.9, e)})
g = Grid("results", xs, [1920, 3620, 3730])
for a, e in results:
    g.put(a, e, 0, 1, [line1(a, e, 668, 674)], frame(HEAD, top="mid", left="mid", right="mid"))
    for r, (y0, y1), edge in ((1, (686, 715), "dot"), (2, (723, 752), "mid")):
        g.put(a, a + 25.9, r, r + 1, lines_in(a + 3, a + 8, y0, y1), frame(LABEL, left="mid", bottom=edge),
              line=1440)
        g.put(a + 25.9, e, r, r + 1, lines_in(a + 27, a + 32, y0, y1), frame(right="mid", bottom=edge),
              align="LEFT", line=1440)
block(g, 665.3)

boxed("result", line1(65, 70, 775, 780), lines_in(115, 120, 766, 790), 764.3, 3720, DARK, WHITE)

kit.finish(target, end=801.5)
