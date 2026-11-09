"""Rebuild KDN 2025 report physical PDF page 69 (printed page 43) as editable HWPX.

Usage: python3 work/kdn2025/p69.py <report.pdf> <out.hwpx> [--page N]
(the second PDF holds report pages 51-100, so this page is local page 19 there)

First body page of the 친환경·탄소중립 indicator: "Ⅰ. 외부 지적사항 조치실적" table and the
"Ⅱ. 2025년 주요 추진실적" three-column block. Same page type as p35.py and the skill recipe
kdn_p49.py (light / mid-gray header tabs, gray detail column with an inset darker result band,
평가내용 chip + hatched title). Built with the shared kit: one flat table per band, rows at the
PDF y positions, all text and run sizes from the PDF text layer (fragments split at
superscripts are merged back into one paragraph, indents kept as leading spaces).

Images in the source and how they are kept:
- PART 01 box, side tab, 평가내용 chip (check icon dropped): typed as cells.
- the ☑ result marks -> ▣ glyphs.
- the boxed 전국최초 / 공공최초 tags are text-layer runs drawn inside image boxes: each tagged
  line gets its own row with the tag in a separate outlined cell.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kit  # noqa: E402
from kit import Layout, recipe_inputs  # noqa: E402

source, target = recipe_inputs(19, "기관별 여건")
L = Layout(top=3200)
kit.setup(source, L)
from kit import *  # noqa: E402,F401,F403  helpers and presets bound to this page

LIGHT_HEAD = frame("#D7D7D7", top="strong", left="soft", right="soft")
MID_HEAD = frame("#767676", top="strong", left="soft", right="soft")
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
        merged = dict(bbox=grp[0]["bbox"], spans=[s for l in grp for s in l["spans"]])
        runs = runs_of(merged)
        size = runs[0][1] / 100
        raw = "".join(s["text"] for s in grp[0]["spans"])
        offset = grp[0]["bbox"][0] - base + (len(raw) - len(raw.lstrip(" "))) * 0.29 * size
        n = max(0, round(offset / (0.29 * size)))
        if n:
            runs = [(" " * n, runs[0][1], False, INK)] + runs
        out.append(runs)
    return out


def tight(g, x0, r0, left=0, right=0):
    c0 = g.xs.index(to_x(x0))
    item = g.items[r0, c0]
    g.items[r0, c0] = (*item[:7], dict(left=left, right=right))


# ---------------------------------------------------------------------------
# Page chrome: side tab and footer float; PART box + running head as the first band.
# ---------------------------------------------------------------------------
L.add_table([[cell(0, 3350, 1680, [para([("01", 1380, True, WHITE)], "CENTER")[0]], dark)],
             [cell(0, 3350, 5960, [para([(ch, 950, True, INK)], "CENTER", 1160)[0] for ch in "경영관리"], gray2)]],
            floating=(57800, 15000))
foot = [(text, size, False, INK) for text, size in (
    (line1(450, 455, 818, 822)["text"], 790), ("    ", 790), (line1(540, 552, 816, 820)["text"], 1090))]
L.add_table([[cell(0, W, 1500, [para(foot, "RIGHT", 1300)[0]])]], floating=(5660, 81550))

g = Grid("head", [X0, 99.0, 158.5, 400.0, X1], [1680])
g.put(X0, 99.0, 0, 1, [[("PART ", 800, False, INK), ("01", 1300, True, INK)]], frame("#EFEFEF", top="strong"))
g.put(99.0, 158.5, 0, 1, "경영관리", frame("#333333"), size=1080, bold=True, color=WHITE)
g.put(158.5, 400.0, 0, 1, [], frame(bottom="soft"))
g.put(400.0, X1, 0, 1, [line1(400, 410, 35, 40)], align="RIGHT")
block(g, 32.0)

g = Grid("title-1", [X0, X1], [2400])
g.put(X0, X1, 0, 1, [line1(205, 210, 69, 74)])
block(g, 68.0)

# ---------------------------------------------------------------------------
# Ⅰ. 외부 지적사항 조치실적: issue | actions (gray, inset ▣ result band) | reference page
# ---------------------------------------------------------------------------
xs = [X0, 194.8, 197.0, 200.4, 511.1, 514.5, 516.8, X1]
ISSUES = [(126.2, 166.8, 184.2, 192.1), (192.1, 232.7, 250.0, 258.1), (258.1, 298.5, 315.9, 323.9),
          (323.9, 347.9, 365.3, 374.3)]
GAP = 300
hs = [2040]
for a, b, c, e in ISSUES:
    hs += [int(round((b - a) * 100)), int(round((c - b) * 100)), int(round((e - c) * 100)) - GAP, GAP]
g = Grid("issues", xs, hs)
g.put(X0, 194.8, 0, 1, [line1(100, 110, 108, 112)], LIGHT_HEAD)
g.put(197.0, 514.5, 0, 1, [runs_of(line1(315, 325, 108, 112), WHITE)], MID_HEAD)
g.put(516.8, X1, 0, 1, [line1(525, 530, 108, 112)], LIGHT_HEAD)
gray = frame(GRAY)
for k, (a, b, c, e) in enumerate(ISSUES):
    r = 1 + 4 * k
    rule = "soft" if k == len(ISSUES) - 1 else "dot"
    g.put(X0, 197.0, r, r + 4, rows_in(55, 195, a, e, 59.7), frame(bottom=rule), align="LEFT", line=1660)
    g.put(197.0, 514.5, r, r + 1, rows_in(197, 214, a, b - 2, 200.0), gray, align="LEFT", line=1660)
    g.put(197.0, 200.4, r + 1, r + 2, [], gray)
    g.put(200.4, 511.1, r + 1, r + 2, [[("▣ ", 1050, True, INK)] + runs_of(line1(214, 219, b, c))],
          frame("#D1D1D1"), align="LEFT", line=1300)
    g.put(511.1, 514.5, r + 1, r + 2, [], gray)
    g.put(197.0, 514.5, r + 2, r + 3, [], gray)
    g.put(197.0, 514.5, r + 3, r + 4, [], frame(bottom=rule))
    g.put(514.5, X1, r, r + 4, [line1(525, 530, a, e)], frame(bottom=rule))
block(g, 105.8)

g = Grid("notes", [X0, X1], [2900])
g.put(X0, X1, 0, 1, [line1(55, 60, 379, 383), line1(55, 60, 393, 397)], align="LEFT", line=1400)
block(g, 378.5)

g = Grid("title-2", [X0, X1], [2400])
g.put(X0, X1, 0, 1, [line1(209, 213, 442, 447)])
block(g, 441.2)

# ---------------------------------------------------------------------------
# Ⅱ. 2025년 주요 추진실적: 평가내용 band, then '24 / '25 / 개선성과 columns
# ---------------------------------------------------------------------------
top, bottom = 478.8, 507.5
h = int(round((bottom - top) * 100))
g = Grid("band-1", [X0, 124.0, X1], [1950, h - 1950])
g.put(X0, 124.0, 0, 1, "평가내용 01", frame("#565656", top="strong"), size=970, bold=True, color=WHITE, ratio=80)
g.put(X0, 124.0, 1, 2, [], frame("#E9E9E9", bottom="soft", left="soft", hatch="#DADADA"))
g.put(124.0, X1, 0, 2, lines_in(125, 130, top, bottom), frame("#E9E9E9", top="strong", bottom="soft",
                                                                right="soft", hatch="#DADADA"),
      align="LEFT", line=1480)
block(g, top)

CX = [X0, 189.2, 191.5, 384.2, 388.2, X1]
TAGS = {1: (209.0, 242.5), 2: (202.5, 235.5)}           # body row -> boxed tag cell (x0, x1) in '25 column
ROWS = [(534.2, 596.6, None), (596.6, 675.6, (5440, 1700)), (675.6, 738.1, (3790, 1700)), (738.1, 800.0, None)]
xs = sorted(set(CX + [x for t in TAGS.values() for x in t]))
hs = [2020]
for a, e, split in ROWS:
    h = int(round((e - a) * 100))
    hs += [h - GAP] if split is None else [split[0], split[1], h - GAP - sum(split)]
    hs.append(GAP)
g = Grid("cols-1", xs, hs)
heads = lines_in(55, 560, 514, 522)
assert len(heads) == 3, [x["text"] for x in heads]
g.put(CX[0], CX[1], 0, 1, [heads[0]], LIGHT_HEAD)
g.put(CX[2], CX[3], 0, 1, [runs_of(heads[1], WHITE)], MID_HEAD)
g.put(CX[4], CX[5], 0, 1, [heads[2]], LIGHT_HEAD)
r = 1
tag_box = frame(WHITE, top="soft", bottom="soft", left="soft", right="soft")
for k, (a, e, split) in enumerate(ROWS):
    n = 2 if split is None else 4
    rule = None if k == len(ROWS) - 1 else "dot"
    g.put(X0, CX[2], r, r + n, rows_in(55, 189, a, e, 59.7), frame(bottom=rule), align="LEFT", line=1660)
    g.put(CX[4], X1, r, r + n, rows_in(388, 560, a, e, 391.3), frame(bottom=rule), align="LEFT", line=1660)
    g.put(CX[3], CX[4], r, r + n, [], frame(bottom=rule))
    mid = rows_in(189, 388, a, e, 194.3)
    if split is None:
        g.put(CX[2], CX[3], r, r + 1, mid, frame(GRAY), align="LEFT", line=1660)
    else:
        t0, t1 = TAGS[k]
        line = [l for l in lines_in(189, 388, a, e) if l["bbox"][1] > a + split[0] / 100 - 6][0]
        head = [s for s in line["spans"] if s["bbox"][0] < t0]
        lead = [("".join(s["text"] for s in head).rstrip(), int(round(head[0]["size"] * 10)) * 10, False, INK)]
        g.put(CX[2], CX[3], r, r + 1, mid[:-1], frame(GRAY), align="LEFT", line=1660)
        g.put(CX[2], t0, r + 1, r + 2, [lead], frame(GRAY), align="LEFT", line=1300)
        g.put(t0, t1, r + 1, r + 2, [runs_of(line, x0=t0, x1=t1)], tag_box, line=1050, ratio=88, fit=False)
        tight(g, t0, r + 1)
        g.put(t1, CX[3], r + 1, r + 2, [strip_runs(runs_of(line, x0=t1))], frame(GRAY), align="LEFT", line=1300)
        g.put(CX[2], CX[3], r + 2, r + 3, [], frame(GRAY))
    g.put(CX[2], CX[3], r + n - 1, r + n, [], frame(bottom=rule))
    r += n
block(g, 514.0)

kit.finish(target, end=802.0)
