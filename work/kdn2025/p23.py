"""Rebuild KDN 2025 report physical PDF page 23 (printed page 11) as editable HWPX.

Usage: python3 work/kdn2025/p23.py <report.pdf> <out.hwpx> [--page N]

다. R&D and Global / 라. 기능전략 (odd page: running head, side tab, footer right).
Built with work/kdn2025/kit.py (one flat table per band on PDF x edges). Text-layer lines come
from the PDF with their spans; tags (상용기술, 지분참여, 공공성, E/S/G, 경영혁신 ...) are split into
their own cells. Image-only parts (side tab, 지적사항 개선 tag, Why?/How? bubbles, the M-O-V-E-R
diagram) are typed from 4x renders; the photo is an empty placeholder cell and the ➡ arrow
images become →.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kit  # noqa: E402
from kit import Layout, recipe_inputs  # noqa: E402

source, target = recipe_inputs(23, "미래 신기술 확보 및 투자연계")
L = Layout(top=3100)
kit.setup(source, L)
from kit import *  # noqa: E402,F401,F403  helpers and presets bound to this page

GREY_TXT = "#F2F2F2"
side = dict(left="soft", right="soft")
TAG = "#5A5A5A"


def split_at(line, k):
    """x where span k of a PDF line starts (spans with text only)."""
    spans = [s for s in line["spans"] if s["text"].strip()]
    return spans[k]["bbox"][0] - 0.5


# ---------------------------------------------------------------------------
# Page chrome (odd page): side tab, footer, running head (as p19).
# ---------------------------------------------------------------------------
L.add_table([[cell(0, 3350, 1680, [para([("01", 1380, True, WHITE)], "CENTER")[0]], dark)],
             [cell(0, 3350, 5960, [para([(ch, 950, True, INK)], "CENTER", 1160)[0] for ch in "경영관리"], gray2)]],
            floating=(57800, 15000))
foot = [(only_text, size, False, INK) for only_text, size in (
    (line1(450, 455, 818, 822)["text"], 790), ("    ", 790), (line1(540, 545, 816, 820)["text"], 1090))]
L.add_table([[cell(0, W, 1500, [para(foot, "RIGHT", 1300)[0]])]], floating=(5660, 81550))

g = Grid("head", [X0, 466.3, X1], [1680])
g.put(X0, 466.3, 0, 1, [], frame(bottom="soft"))
g.put(466.3, X1, 0, 1, [line1(465, 475, 35, 40)], align="RIGHT")
block(g, 32.0)

# ---------------------------------------------------------------------------
# 다. R&D and Global
# ---------------------------------------------------------------------------
title_band("title-da", line1(55, 60, 70, 74), [X0, 77.6, 165.0, X1], 70.7)
heading("heading-rnd", line1(68, 72, 92, 96), 93.0, badge="지적사항 개선", badge_x=503.0)

# R&D: 추진배경 / 추진방향 / 추진실적 (three tagged boxes)
xs = [X0, 112.2, 117.6, 158.3, 257.4, 265.4, 301.2, 405.2, 413.2, 449.0, 553.0, X1]
hs = [2450, 400, 2440, 410, 1780, 3770]          # 113.7 .. 226.2
g = Grid("rnd", xs, hs)
for (r0, r1), y in (((0, 1), 121.6), ((2, 3), 152.5), ((4, 6), 196.9)):
    g.put(X0, 112.2, r0, r1, [line1(64, 67, y - 1, y + 1)], frame("#D9D9D9", bottom="soft"), bold=True)
box = frame(top="soft", bottom="soft", **side)
g.put(117.6, X1, 0, 1, [line1(119, 122, 119, 122)], box, align="LEFT")
g.put(117.6, X1, 2, 3, [line1(119, 122, 147, 150)], box, align="LEFT")
for a, t, e, x in ((117.6, 158.3, 257.4, 125.2), (265.4, 301.2, 405.2, 268.0), (413.2, 449.0, 553.0, 415.9)):
    ln = line1(x - 1, x + 1, 175, 177)
    cut = split_at(ln, 1)
    g.put(a, t, 4, 5, [runs_of(ln, WHITE, x1=cut)], frame(TAG, top="mid", left="mid"))
    g.put(t, e, 4, 5, [runs_of(ln, x0=cut)], frame(top="mid", right="mid"), align="LEFT")
    body = lines_in(a, e, 194, 212)
    if x == 415.9:   # second line follows a ➡ arrow image
        body = [body[0], [("  → ", 1000, True, "#505050")] + runs_of(body[1])]
    g.put(a, e, 5, 6, body, frame("#EFEFEF", bottom="mid", **dict(left="mid", right="mid")), align="LEFT", line=1400)
block(g, 113.7)

# 주요성과: three bullets with outlined AI / 에너지 / 보안 tags
xs = [X0, 112.2, 116.0, 126.5, 151.0, X1]
g = Grid("rnd-result", xs, [1720, 1720, 1720])
g.put(X0, 112.2, 0, 3, [line1(64, 67, 251, 254)], frame("#5E5E5E"), bold=True, color=WHITE)
bullets = [line1(117, 118, 237, 239), None, line1(117, 118, 266, 268)]
lines = [line1(134, 135, 237, 239), line1(117, 118, 252, 254), line1(130, 131, 266, 268)]
for r, (bul, ln) in enumerate(zip(bullets, lines)):
    edge = dict(top="mid" if r == 0 else None, bottom="mid" if r == 2 else None)
    if bul is None:
        bul_runs, ln_tag = runs_of(ln, x1=126), runs_of(ln, x0=126, x1=151)
        rest = runs_of(ln, x0=151)
    else:
        bul_runs, ln_tag, rest = runs_of(bul), runs_of(ln, x1=151), runs_of(ln, x0=151)
    g.put(112.2, 116.0, r, r + 1, [], frame(**edge))
    g.put(116.0, 126.5, r, r + 1, [bul_runs], frame(**edge), fit=False)
    g.put(126.5, 151.0, r, r + 1, [ln_tag], frame(WHITE, top="soft", bottom="soft", **side))
    g.put(151.0, X1, r, r + 1, [rest], frame(right="soft", **edge), align="LEFT")
block(g, 232.5)

heading("heading-global", line1(68, 72, 292, 295), 292.5)

# Global: quote bar, Why? / How? bubbles (image text) with bullets
xs = [X0, 92.0, 306.0, 340.5, X1]
g = Grid("global", xs, [1760, 3800])
g.put(X0, X1, 0, 1, [line1(176, 179, 317, 319)], frame("#DCDCDC", top="mid", **side))
g.put(X0, 92.0, 1, 2, "Why?", frame(left="soft", bottom="mid"), size=750, bold=True, color="#3A3A3A")
left = lines_in(94, 105, 336, 360)
g.put(92.0, 306.0, 1, 2, [left[0], [("  ", 1090, False, INK)] + runs_of(left[1])],
      frame(bottom="mid", right="dot"), align="LEFT", line=1450)
g.put(306.0, 340.5, 1, 2, "How?", frame("#8A8A8A", bottom="mid"), size=750, bold=True, color=WHITE)
g.put(340.5, X1, 1, 2, lines_in(343, 346, 336, 360), frame(bottom="mid", right="soft"), align="LEFT", line=1450)
block(g, 313.4)


def tagged_rows(name, top, label_y, ys, hs, photo_rows=None, cap=90):
    """Label + bullet lines whose first span is a gray tag; optional 최초 outlined second tag."""
    lines = [line1(99, 100, y - 1, y + 1) for y in ys]
    second = any("최초" in ln["text"] for ln in lines)
    xs = [X0, 90.8, 96.3, 106.0, 141.8] + ([162.0] if second else []) + ([468.0] if photo_rows else []) + [X1]
    g = Grid(name, xs, hs)
    g.put(X0, 90.8, 0, len(hs), lines_in(60, 66, label_y - 1, label_y + 30), frame("#D9D9D9"), bold=True)
    end = 468.0 if photo_rows else X1
    n = len(ys)
    for r, ln in enumerate(lines):
        edge = dict(top="soft" if r == 0 else None, bottom="soft" if r == n - 1 else None)
        g.put(96.3, 106.0, r, r + 1, [runs_of(ln, x1=106)], frame(left="soft", **edge), fit=False)
        g.put(106.0, 141.8, r, r + 1, [runs_of(ln, x0=106, x1=141)], frame("#D6D6D6", **edge))
        spans = [s for s in ln["spans"] if s["text"].strip()]
        if len(spans) > 2 and spans[2]["text"].strip() == "최초":
            g.put(141.8, 162.0, r, r + 1, [runs_of(ln, x0=141, x1=161)], frame(WHITE, top="soft", bottom="soft", **side))
            g.put(162.0, end, r, r + 1, [runs_of(ln, x0=161)], frame(right="soft" if not photo_rows else None, **edge),
                  align="LEFT")
        else:
            g.put(141.8, end, r, r + 1, [runs_of(ln, x0=141)], frame(right="soft" if not photo_rows else None, **edge),
                  align="LEFT", ratio=cap)
    if photo_rows:
        g.put(468.0, X1, 0, n, [], photo)
    block(g, top)


tagged_rows("new-model", 375.3, 384.2, (381.8, 396.7, 411.6), [1810, 1800, 1810], photo_rows=True)
tagged_rows("global-result", 434.7, 442.4, (440.3, 456.4), [1930, 1940], cap=80)

# ---------------------------------------------------------------------------
# 라. 기능전략 “F1rst MOVER”
# ---------------------------------------------------------------------------
title_band("title-ra", line1(55, 60, 484, 488), [X0, 77.6, 127.0, X1], 484.5)

# M-O-V-E-R diagram: an image in the PDF; text read from a 4x render.
xs = [X0, 154.5, 240.8, 245.8, 254.8, 255.5, 270.5, 284.5, 299.8, 313.8, 329.0, 343.0, 356.7, 358.7,
      372.7, 457.5, X1]
g = Grid("mover", xs, [1500, 1600, 1250, 1750])          # 509 524 540 552.5 570
for (a, e), letter in zip(((240.8, 254.8), (270.5, 284.5), (299.8, 313.8), (329.0, 343.0), (358.7, 372.7)), "MOVER"):
    g.put(a, e, 0, 1, letter, frame("#5E5E5E"), size=950, bold=True, color=WHITE, line=1050)
g.put(245.8, 372.7, 1, 2, [], frame(top="mid"))
themes = [("M", "anagement System", "시스템경영"), ("O", "rganization", "최적 조직체계"), ("V", "aluable ESG", "ESG경영"),
          ("E", "xpert", "기술 전문성"), ("R", "eliable Culture", "신뢰의 기업문화")]
for k, ((a, e), (cap, rest, kor)) in enumerate(zip(((X0, 154.5), (154.5, 255.5), (255.5, 356.7), (356.7, 457.5),
                                                    (457.5, X1)), themes)):
    sep = "dot" if k < 4 else None
    g.put(a, e, 2, 3, [[(cap, 820, True, WHITE), (rest, 780, False, GREY_TXT)]], frame("#6E6E6E", right=sep), line=900)
    g.put(a, e, 3, 4, kor, frame("#E6E6E6", right=sep, bottom="soft"), size=1100, bold=True)
block(g, 509.0)

# 추진배경 / 추진방향 / 추진실적 / 추진성과 table
xs = [X0, 112.2, 117.6, 121.0, 132.0, 145.0, 332.3, 339.4, 342.2, 348.0, 375.6, 379.6, X1]
hs = [1720, 1720, 410, 1630, 1600, 1650, 1550, 1600, 1630, 400, 1620, 1610, 1620, 410, 1710, 1720]
g = Grid("ra-table", xs, hs)
for (r0, r1), y in (((0, 2), 588.5), ((3, 9), 661.5), ((10, 13), 738.1), ((14, 16), 783.4)):
    g.put(X0, 112.2, r0, r1, [line1(64, 67, y - 1, y + 1)], frame("#D9D9D9"), bold=True)
# 추진배경: tag + quote, then a centred second line (gray boxes)
bg = "#ECECEC"
for (a, t0, t1, e), x, x2 in (((117.6, 117.6, 145.0, 332.3), 120.4, 138.8), ((339.4, 348.0, 375.6, X1), 350.5, 356.9)):
    ln = line1(x - 1, x + 1, 580, 582)
    cut = split_at(ln, 1)
    if t0 > a:
        g.put(a, t0, 0, 1, [], frame(bg, top="soft", left="soft"))
    g.put(t0, t1, 0, 1, [runs_of(ln, x1=cut)], frame(WHITE, top="soft", left="soft", bottom="soft", right="soft"))
    g.put(t1, e, 0, 1, [runs_of(ln, x0=cut)], frame(bg, top="soft", right="soft"), align="LEFT")
    g.put(a, e, 1, 2, [line1(x2 - 1, x2 + 1, 594, 596)], frame(bg, bottom="soft", **side))


def tag_line(g, r, ln, a, t0, t1, e, edge, tagfill=TAG):
    cut = split_at(ln, 1)
    if t0 > a:
        g.put(a, t0, r, r + 1, [], frame(left="soft", **edge))
    g.put(t0, t1, r, r + 1, [runs_of(ln, WHITE, x1=cut)], frame(tagfill, **edge),
          fit=len(ln["spans"][0]["text"].strip()) > 1)
    g.put(t1, e, r, r + 1, [runs_of(ln, x0=cut)], frame(right="soft", **edge), align="LEFT")


# 추진방향: tagged line + "→ follow-up" line, three pairs per side
for k, y in enumerate((619.1, 650.8, 682.3)):
    r = 3 + 2 * k
    top = dict(top="soft" if k == 0 else "dot")
    for (a, t0, t1, e), x, x2 in (((117.6, 121.0, 132.0, 332.3), 123.7, 137.9), ((339.4, 342.2, 379.6, X1), 345.7, 358.3)):
        ln = line1(x - 1, x + 1, y - 1, y + 1)
        tag_line(g, r, ln, a, t0, t1, e, top)
        follow = line1(x2 - 1, x2 + 1.5, y + 12, y + 15)
        g.put(a, e, r + 1, r + 2, [[("  → ", 1000, True, "#505050")] + runs_of(follow)],
              frame(bottom="soft" if k == 2 else None, **side), align="LEFT")
# 추진실적: three tagged lines per side
for k, y in enumerate((720.4, 733.9, 747.5)):
    r = 10 + k
    edge = dict(top="soft" if k == 0 else None, bottom="soft" if k == 2 else None)
    for (a, t0, t1, e), x in (((117.6, 121.0, 132.0, 332.3), 123.7), ((339.4, 342.2, 379.6, X1), 345.7)):
        tag_line(g, r, line1(x - 1, x + 1, y - 1, y + 1), a, t0, t1, e, edge)
# 추진성과: two bullets per side
for k, y in enumerate((772.2, 786.5)):
    r = 14 + k
    edge = dict(top="soft" if k == 0 else None, bottom="soft" if k == 1 else None)
    for (a, e), x in (((117.6, 332.3), 120.7), ((339.4, X1), 340.3)):
        g.put(a, e, r, r + 1, [line1(x - 1, x + 1, y - 1, y + 1)], frame(**side, **edge), align="LEFT")
block(g, 576.2)


def check_edges():
    """Every inner column edge of a band must be a cell boundary, or its width is undefined."""
    for grid, _ in kit.BLOCKS:
        used = {0, len(grid.xs) - 1}
        for (r, c0), item in grid.items.items():
            used.update((c0, c0 + item[6]))
        for c in range(len(grid.xs)):
            if c not in used:
                print(f"WARN {grid.name}: unused edge x={X0 + grid.xs[c] / 100:.1f}")


check_edges()
kit.finish(target, end=803.0)
