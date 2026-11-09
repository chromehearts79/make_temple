"""Rebuild KDN 2025 report page 149 (third PDF local page 49, printed page 104) as editable HWPX.

Usage: python3 work/kdn2025/p149.py <report3.pdf> <out.hwpx> [--page 49]
(the third PDF holds report pages 101-150, so this page is local page 49 there)

First body page of the 보수 및 복리후생 indicator: "Ⅰ. 외부 지적사항 조치실적" table and the
"Ⅱ. 2025년 주요 추진실적" three-column blocks (평가내용 01-03). Same page type as p35.py, p59.py
and p69.py (light / mid-gray header tabs, gray detail column with inset darker result bands,
평가내용 chip + hatched title). Built with the shared kit: one flat table per band, rows at the
PDF y positions, all text and run sizes from the PDF text layer (fragments split at
superscripts are merged back into one paragraph, indents kept as leading spaces).

Images in the source and how they are kept:
- PART 01 box, side tab, 평가내용 01/02/03 chips (check icon dropped): typed as cells.
- the ☑ result marks -> ▣ glyphs; the result bands -> darker inset cells.
- the "6개 제안 채널" mini table inside the first action cell (기존 / 신규 label images over a
  vector-ruled grid): a 3-column inset grid, label text from the text layer split by span x.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kit  # noqa: E402
from kit import Layout, recipe_inputs  # noqa: E402

source, target = recipe_inputs(49, "비금전적 복지제도 제안 채널 운영 확대")
L = Layout(top=3200)
kit.setup(source, L)
from kit import *  # noqa: E402,F401,F403  helpers and presets bound to this page

LIGHT_HEAD = frame("#D7D7D7", top="strong", left="soft", right="soft")
MID_HEAD = frame("#767676", top="strong", left="soft", right="soft")
GRAY = "#EBEBEB"
RESULT = "#D1D1D1"
LABEL = "#D8D8D8"


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


# ---------------------------------------------------------------------------
# Page chrome (odd page): side tab and footer float; PART box + running head as the first band.
# ---------------------------------------------------------------------------
L.add_table([[cell(0, 3350, 1680, [para([("01", 1380, True, WHITE)], "CENTER")[0]], dark)],
             [cell(0, 3350, 5960, [para([(ch, 950, True, INK)], "CENTER", 1160)[0] for ch in "경영관리"], gray2)]],
            floating=(57800, 15000))
foot_line = line1(450, 455, 816, 822)          # "2025년도 경영실적보고서" + "104" share one PDF line
foot = [(t, 790, False, INK) for t, *_ in runs_of(foot_line, x1=530)] + [("    ", 790, False, INK)] + \
       [(t, 1090, False, INK) for t, *_ in runs_of(foot_line, x0=530)]
L.add_table([[cell(0, W, 1500, [para(foot, "RIGHT", 1300)[0]])]], floating=(5660, 81550))

g = Grid("head", [X0, 99.0, 158.5, 396.9, X1], [1680])
g.put(X0, 99.0, 0, 1, [[("PART ", 800, False, INK), ("01", 1300, True, INK)]], frame("#EFEFEF", top="strong"))
g.put(99.0, 158.5, 0, 1, "경영관리", frame("#333333"), size=1080, bold=True, color=WHITE)
g.put(158.5, 396.9, 0, 1, [], frame(bottom="soft"))
g.put(396.9, X1, 0, 1, [line1(400, 410, 35, 40)], align="RIGHT")
block(g, 32.0)

g = Grid("title-1", [X0, X1], [2400])
g.put(X0, X1, 0, 1, [line1(205, 210, 69, 74)])
block(g, 68.0)

# ---------------------------------------------------------------------------
# Ⅰ. 외부 지적사항 조치실적: issue | actions (gray, inset ▣ result bands and the 제안 채널
# mini table) | reference page
# ---------------------------------------------------------------------------
IN0, CH0, CH1, IN1 = 206.8, 235.3, 367.1, 510.4          # inset edges and mini-table columns
xs = [X0, 198.6, 202.7, IN0, CH0, CH1, IN1, 514.5, 518.7, X1]
# issue 1 rows: detail, result, '* 6개 제안 채널', 3 channel rows, detail, result, gray tail, rule gap
Y1 = [126.1, 148.8, 166.2, 185.5, 201.1, 216.7, 232.3, 253.1, 270.4, 275.9, 277.6]
# issue 2 rows: detail (3 lines), result, gray tail, rule gap
Y2 = [277.6, 332.1, 349.4, 354.9, 357.6]
hs = [2060] + [int(round((b - a) * 100)) for ys in (Y1, Y2) for a, b in zip(ys, ys[1:])]
g = Grid("issues", xs, hs)
g.put(X0, 198.6, 0, 1, [line1(100, 115, 108, 113)], LIGHT_HEAD)
g.put(202.7, 514.5, 0, 1, [runs_of(line1(320, 330, 108, 113), WHITE)], MID_HEAD)
g.put(518.7, X1, 0, 1, [line1(525, 530, 108, 113)], LIGHT_HEAD)
gray = frame(GRAY)
result = frame(RESULT)


def detail(r, y0, y1):
    g.put(202.7, 514.5, r, r + 1, rows_in(200, 240, y0, y1, 205.7), gray, align="LEFT", line=1600)


def result_band(r, y0, y1):
    g.put(202.7, IN0, r, r + 1, [], gray)
    g.put(IN0, IN1, r, r + 1, [[("▣ ", 1050, True, INK)] + runs_of(line1(220, 226, y0, y1))], result,
          align="LEFT", line=1300)
    g.put(IN1, 514.5, r, r + 1, [], gray)


def tail(r, rule):
    g.put(202.7, 514.5, r, r + 1, [], gray)
    g.put(202.7, 514.5, r + 1, r + 2, [], frame(bottom=rule))


# issue 1 (rows 1-10)
n1 = len(Y1) - 1
g.put(X0, 202.7, 1, 1 + n1, rows_in(55, 198, 126, 277, 59.7), frame(bottom="dot"), align="LEFT", line=1600)
g.put(514.5, X1, 1, 1 + n1, [line1(520, 530, 190, 210)], frame(bottom="dot"))
detail(1, 126.1, 148.8)
result_band(2, 148.8, 166.2)
g.put(202.7, 514.5, 3, 4, rows_in(200, 240, 166.2, 185.5, 205.7), gray, align="LEFT", line=1300)
# mini table: 기존 | ① | ② ; 신규 (two rows) | ③ ⑤ | ④ ⑥
chan = [line1(205, 215, 186, 200), line1(205, 215, 202, 216), line1(236, 240, 217, 232)]
right = [line1(368, 372, 186, 200), line1(368, 372, 202, 216), line1(368, 372, 217, 232)]
label = frame(LABEL, top="mid", bottom="mid", right="soft")
for k in range(3):
    r = 4 + k
    top_edge = "mid" if k == 0 else "soft"
    bottom_edge = "mid" if k == 2 else None
    g.put(202.7, IN0, r, r + 1, [], gray)
    g.put(IN1, 514.5, r, r + 1, [], gray)
    left_runs = runs_of(chan[k], x0=CH0) if k < 2 else runs_of(chan[k])
    g.put(CH0, CH1, r, r + 1, [left_runs], frame(WHITE, top=top_edge, bottom=bottom_edge), align="LEFT", line=1300)
    g.put(CH1, IN1, r, r + 1, [runs_of(right[k])], frame(WHITE, top=top_edge, bottom=bottom_edge),
          align="LEFT", line=1300)
g.put(IN0, CH0, 4, 5, [runs_of(chan[0], x1=CH0)], label, line=1300)
g.put(IN0, CH0, 5, 7, [runs_of(chan[1], x1=CH0)], label, line=1300)
detail(7, 232.3, 253.1)
result_band(8, 253.1, 270.4)
tail(9, "dot")

# issue 2 (rows 11-14)
r = 1 + n1
n2 = len(Y2) - 1
g.put(X0, 202.7, r, r + n2, rows_in(55, 198, 278, 357, 59.7), frame(bottom="soft"), align="LEFT", line=1600)
g.put(514.5, X1, r, r + n2, [line1(520, 530, 300, 330)], frame(bottom="soft"))
detail(r, 277.6, 332.1)
result_band(r + 1, 332.1, 349.4)
tail(r + 2, "soft")
block(g, 105.5)

g = Grid("note", [X0, X1], [1300])
g.put(X0, X1, 0, 1, [line1(55, 60, 360, 366)], align="LEFT", line=1100)
block(g, 361.0)

g = Grid("title-2", [X0, X1], [2400])
g.put(X0, X1, 0, 1, [line1(209, 215, 401, 407)])
block(g, 400.5)


# ---------------------------------------------------------------------------
# Ⅱ. 2025년 주요 추진실적: 평가내용 band, then '24 / '25 / 개선성과 columns (three times)
# ---------------------------------------------------------------------------
def band(number, top, bottom):
    """평가내용 chip in the top-left corner, hatched title over the full band height."""
    h = int(round((bottom - top) * 100))
    g = Grid(f"band-{number}", [X0, 124.0, X1], [1950, h - 1950])
    g.put(X0, 124.0, 0, 1, f"평가내용 {number:02}", frame("#565656", top="strong"),
          size=970, bold=True, color=WHITE, ratio=80)
    g.put(X0, 124.0, 1, 2, [], frame("#E9E9E9", bottom="soft", left="soft", hatch="#DADADA"))
    g.put(124.0, X1, 0, 2, lines_in(125, 130, top, bottom), frame("#E9E9E9", top="strong", bottom="soft",
                                                                    right="soft", hatch="#DADADA"),
          align="LEFT", line=1480)
    block(g, top)


CX = [X0, 198.6, 202.7, 378.5, 382.6, X1]


def columns(name, head_top, body_top, body_bottom, rule_y, dash_only=False):
    """Three column heads, one text row (gray middle column) and the closing rule."""
    hs = [int(round((body_top - head_top) * 100)), int(round((body_bottom - body_top) * 100)),
          int(round((rule_y - body_bottom) * 100))]
    g = Grid(name, CX, hs)
    heads = lines_in(55, 560, head_top + 2, body_top - 2)
    assert len(heads) == 3, [x["text"] for x in heads]
    g.put(CX[0], CX[1], 0, 1, [heads[0]], LIGHT_HEAD)
    g.put(CX[2], CX[3], 0, 1, [runs_of(heads[1], WHITE)], MID_HEAD)
    g.put(CX[4], CX[5], 0, 1, [heads[2]], LIGHT_HEAD)
    end = frame(bottom="soft")
    if dash_only:                      # 평가내용 03: the '24 column holds a lone centred "-"
        g.put(CX[0], CX[2], 1, 3, [runs_of(l) for l in lines_in(55, 198, body_top, body_bottom)], end)
    else:
        g.put(CX[0], CX[2], 1, 3, rows_in(55, 198, body_top, body_bottom, 59.7), end, align="LEFT", line=1600)
    g.put(CX[2], CX[3], 1, 2, rows_in(200, 380, body_top, body_bottom, 205.7), frame(GRAY), align="LEFT", line=1600)
    g.put(CX[2], CX[3], 2, 3, [], end)
    g.put(CX[3], CX[4], 1, 3, [], end)
    g.put(CX[4], CX[5], 1, 3, rows_in(380, 560, body_top, body_bottom, 385.7), end, align="LEFT", line=1600)
    block(g, head_top)


band(1, 438.3, 467.0)
columns("cols-1", 473.3, 493.8, 545.6, 547.6)
band(2, 565.5, 594.2)
columns("cols-2", 600.5, 621.0, 672.8, 674.8)
band(3, 692.7, 734.1)
columns("cols-3", 740.4, 761.0, 798.6, 800.6, dash_only=True)

kit.finish(target, end=802.0)
