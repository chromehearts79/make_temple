"""Rebuild KDN 2025 report page 103 (third PDF local page 3, printed page 68) as editable HWPX.

Usage: python3 work/kdn2025/p103.py <report3.pdf> <out.hwpx> [--page 3]
(the third PDF holds report pages 101-150, so this page is local page 3 there)

First body page of the 재무성과관리(재무예산관리) indicator: "Ⅰ. 외부 지적사항 조치실적" table and
the "Ⅱ. 2025년 주요 추진실적" three-column blocks for 평가내용 01-03. Same page type as p35.py,
p59.py and p69.py (light / mid-gray header tabs, gray detail column with an inset darker result
band, 평가내용 chip + hatched title). Built with the shared kit: one flat table per band, rows at
the PDF y positions (the PDF's own gray boxes), all text and run sizes from the PDF text layer
(fragments split at superscripts are merged back into one paragraph, indents kept as spaces).

Images in the source and how they are kept:
- PART 01 box, side tab, 평가내용 chips 01 / 02 / 03 (check icon dropped): typed as cells.
- the ☑ result marks -> ▣ glyphs.
- the three ➡ arrow images that join two text-layer fragments ("(기존) ... 운영 ➡ (개선) ...",
  "(~’24년) ... 중심 ➡ (’25년) ...", "... 270억원 회수 ➡ 미래신사업 ...") -> " → ".
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kit  # noqa: E402
from kit import Layout, recipe_inputs  # noqa: E402

source, target = recipe_inputs(3, "창사이래 최초 월 단위 매출관리 선행지표 도입")
L = Layout(top=3200)
kit.setup(source, L)
from kit import *  # noqa: E402,F401,F403  helpers and presets bound to this page

LIGHT_HEAD = frame("#D9D9D9", top="strong", left="soft", right="soft")
MID_HEAD = frame("#7F7F7F", top="strong", left="soft", right="soft")
GRAY = "#EBEBEB"


def rows_in(x0, x1, y0, y1, base):
    """Text rows of a region: fragments of one visual row (split at superscripts) are merged,
    and the row keeps its PDF indent as leading spaces (offset from `base`)."""
    hits = sorted((l for l in LINES if x0 <= l["bbox"][0] < x1 and y0 <= l["bbox"][1] < y1),
                  key=lambda l: (l["bbox"][1], l["bbox"][0]))
    groups = []
    for l in hits:
        for grp in groups:
            top, bottom = min(g["bbox"][1] for g in grp), max(g["bbox"][3] for g in grp)
            if l["bbox"][1] < bottom - 2 and l["bbox"][3] > top + 2:
                grp.append(l)
                break
        else:
            groups.append([l])
    out = []
    for grp in groups:
        grp.sort(key=lambda l: l["bbox"][0])
        parts = []
        for k, l in enumerate(grp):
            runs = runs_of(l)
            # a horizontal gap of > 8 pt between fragments is a ➡ image in the PDF
            if k and l["bbox"][0] - grp[k - 1]["bbox"][2] > 8:
                parts.append((" → ", runs[0][1], runs[0][2], INK))
            parts += runs
        runs = []
        for r in parts:
            if runs and runs[-1][1:] == r[1:]:
                runs[-1] = (runs[-1][0] + r[0], *r[1:])
            else:
                runs.append(r)
        size = runs[0][1] / 100
        raw = "".join(s["text"] for s in grp[0]["spans"])
        offset = grp[0]["bbox"][0] - base + (len(raw) - len(raw.lstrip(" "))) * 0.29 * size
        n = max(0, round(offset / (0.29 * size)))
        if n:
            runs = [(" " * n, runs[0][1], False, INK)] + runs
        out.append(runs)
    return out


def put_fit(g, x0, x1, r0, r1, pars, fill, line, align="LEFT", ratio=90):
    """Like Grid.put, but 장평 is fitted per paragraph (one tight line does not shrink the cell)."""
    g.put(x0, x1, r0, r1, pars, fill, align=align, line=line, ratio=ratio, fit=False)
    c0 = g.xs.index(to_x(x0))
    item = g.items[r0, c0]
    inner = (item[1] - 500) / 100 * 0.96
    contents = []
    for runs in pars:
        need = text_width(runs, ratio)
        fitted = int(ratio * inner / need) if need > inner else ratio
        if fitted < 68:
            WARN.append(f"{g.name}: ratio {fitted} for {runs[0][0][:20]!r}")
        contents.append(para(runs, align, line, fitted)[0])
    g.items[r0, c0] = (item[0], item[1], item[2], contents, *item[4:])


# ---------------------------------------------------------------------------
# Page chrome (odd page): side tab and footer float; PART box + running head as the first band.
# ---------------------------------------------------------------------------
L.add_table([[cell(0, 3350, 1680, [para([("01", 1380, True, WHITE)], "CENTER")[0]], dark)],
             [cell(0, 3350, 5960, [para([(ch, 950, True, INK)], "CENTER", 1160)[0] for ch in "경영관리"], gray2)]],
            floating=(57800, 15000))
foot = [(text, size, False, INK) for text, size in (
    (line1(450, 455, 818, 822)["text"], 790), ("    ", 790), (line1(540, 546, 816, 820)["text"], 1090))]
L.add_table([[cell(0, W, 1500, [para(foot, "RIGHT", 1300)[0]])]], floating=(5660, 81550))

g = Grid("head", [X0, 99.0, 158.5, 429.5, X1], [1680])
g.put(X0, 99.0, 0, 1, [[("PART ", 800, False, INK), ("01", 1300, True, INK)]], frame("#EFEFEF", top="strong"))
g.put(99.0, 158.5, 0, 1, "경영관리", frame("#333333"), size=1080, bold=True, color=WHITE)
g.put(158.5, 429.5, 0, 1, [], frame(bottom="soft"))
g.put(429.5, X1, 0, 1, [line1(430, 440, 35, 40)], align="RIGHT")
block(g, 32.0)

g = Grid("title-1", [X0, X1], [2400])
g.put(X0, X1, 0, 1, [line1(205, 210, 69, 74)])
block(g, 68.5)

# ---------------------------------------------------------------------------
# Ⅰ. 외부 지적사항 조치실적: issue | actions (gray, inset ▣ result band) | reference page
# ---------------------------------------------------------------------------
xs = [X0, 193.0, 197.0, 200.5, 510.5, 514.5, 518.7, X1]
# per issue: row top, result band top, result band bottom, next row top (the PDF's gray boxes)
ISSUES = [(121.6, 136.2, 153.5, 157.7), (157.7, 185.5, 202.8, 207.0), (207.0, 234.8, 252.2, 256.4),
          (256.4, 284.1, 301.5, 305.7), (305.7, 346.7, 364.1, 368.5)]
hs = [1910]
for a, b, c, e in ISSUES:
    hs += [int(round((b - a) * 100)), int(round((c - b) * 100)), int(round((e - c) * 100))]
g = Grid("issues", xs, hs)
g.put(X0, 193.0, 0, 1, [line1(100, 110, 104, 110)], LIGHT_HEAD)
g.put(197.0, 514.5, 0, 1, [runs_of(line1(315, 325, 104, 110), WHITE)], MID_HEAD)
g.put(518.7, X1, 0, 1, [line1(525, 530, 104, 110)], LIGHT_HEAD)
gray = frame(GRAY)
for k, (a, b, c, e) in enumerate(ISSUES):
    r = 1 + 3 * k
    rule = "soft" if k == len(ISSUES) - 1 else "dot"
    put_fit(g, X0, 197.0, r, r + 3, rows_in(55, 195, a, e, 59.7), frame(bottom=rule), line=1450)
    put_fit(g, 197.0, 514.5, r, r + 1, rows_in(197, 514, a, b - 2, 200.0), gray, line=1300)
    g.put(197.0, 200.5, r + 1, r + 2, [], gray)
    put_fit(g, 200.5, 510.5, r + 1, r + 2, [[("▣ ", 1050, True, INK)] + rows_in(210, 514, b, c, 213.8)[0]],
            frame("#D6D6D6"), line=1300)
    g.put(510.5, 514.5, r + 1, r + 2, [], gray)
    g.put(197.0, 514.5, r + 2, r + 3, [], frame(GRAY, bottom=rule))
    g.put(514.5, X1, r, r + 3, [line1(525, 530, a, e)], frame(bottom=rule))
block(g, 102.5)

g = Grid("note", [X0, X1], [1300])
g.put(X0, X1, 0, 1, [line1(55, 60, 372, 378)], align="LEFT", line=1100)
block(g, 373.5)

g = Grid("title-2", [X0, X1], [2400])
g.put(X0, X1, 0, 1, [line1(209, 213, 396, 402)])
block(g, 396.5)


# ---------------------------------------------------------------------------
# Ⅱ. 2025년 주요 추진실적: 평가내용 band, then '24 / '25 / 개선성과 columns
# ---------------------------------------------------------------------------
def band(number, top, bottom):
    """평가내용 chip in the top-left corner, hatched title over the full band height."""
    h = int(round((bottom - top) * 100))
    g = Grid(f"band-{number}", [X0, 124.0, X1], [1950, h - 1950])
    g.put(X0, 124.0, 0, 1, [[("평가내용 ", 800, True, WHITE), (f"{number:02}", 1350, True, WHITE)]],
          frame("#5F5F5F", top="strong"), line=1500)
    g.put(X0, 124.0, 1, 2, [], frame("#E9E9E9", bottom="soft", left="soft", hatch="#DADADA"))
    g.put(124.0, X1, 0, 2, lines_in(125, 130, top, bottom), frame("#E9E9E9", top="strong", bottom="soft",
                                                                    right="soft", hatch="#DADADA"),
          align="LEFT", line=1480)
    block(g, top)


CX = [X0, 196.0, 199.8, 367.3, 371.2, X1]
BASES = (59.7, 202.8, 374.3)
side_fill = frame(bottom="soft")
mid_fill = frame(GRAY, bottom="soft")


def columns(name, head_y, top, body):
    """Three column heads, then one body row (y0, y1) closed by a full-width rule."""
    y0, y1 = body
    g = Grid(name, CX, [int(round((y0 - top) * 100)), int(round((y1 - y0) * 100))])
    heads = lines_in(55, 560, head_y - 3, head_y + 6)
    assert len(heads) == 3, [h["text"] for h in heads]
    g.put(CX[0], CX[1], 0, 1, [heads[0]], LIGHT_HEAD)
    g.put(CX[2], CX[3], 0, 1, [runs_of(heads[1], WHITE)], MID_HEAD)
    g.put(CX[4], CX[5], 0, 1, [heads[2]], LIGHT_HEAD)
    for k, fill in enumerate((side_fill, mid_fill, side_fill)):
        a, e = CX[2 * k], CX[2 * k + 1]
        put_fit(g, a, e, 1, 2, rows_in(a - 3, e - 15, y0, y1, BASES[k]), fill, line=1320)
        if k < 2:
            g.put(e, CX[2 * k + 2], 1, 2, [], side_fill)
    block(g, top)


band(1, 430.4, 459.0)
columns("cols-1", 465, 463.2, (482.2, 553.0))
band(2, 561.0, 602.4)
columns("cols-2", 608, 606.5, (625.6, 683.2))
band(3, 691.2, 719.9)
columns("cols-3", 726, 724.0, (743.0, 800.6))

kit.finish(target, end=802.4)
