"""Rebuild KDN 2025 report page 87 (2nd PDF local page 37, printed page 57) as editable HWPX.

Usage: python3 work/kdn2025/p87.py <report2.pdf> <out.hwpx> [--page 37]

First body page of the 상생･협력 및 지역발전 indicator: "Ⅰ. 외부 지적사항 조치실적" table and the
"Ⅱ. 2025년 주요 추진실적" three-column blocks. Same page type as p35.py / kdn_p49.py (light and
mid-gray header tabs, gray detail column with a darker result band, 평가내용 chip + hatched
title). All text comes from the PDF text layer; images: the PART box and the side tab are typed,
the 평가내용 chips are typed as "평가내용 0N" (check-mark icon dropped), the ☑ result marks -> ▣.
This odd page carries both the PART box (left) and the running head (right), as printed.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kit  # noqa: E402
from kit import Layout, recipe_inputs  # noqa: E402

source, target = recipe_inputs(37, "성과공유제도 건당 지원규모 증가")
L = Layout(top=3200)
kit.setup(source, L)
from kit import *  # noqa: E402,F401,F403  helpers and presets bound to this page

LIGHT_HEAD = frame("#D7D7D7", top="strong", left="soft", right="soft")
MID_HEAD = frame("#808080", top="strong", left="soft", right="soft")


def body_lines(x0, x1, y0, y1, indent="  "):
    """Bullet lines as run lists; continuation lines get the source's hanging indent."""
    out = []
    for line in lines_in(x0, x1, y0, y1):
        runs = runs_of(line)
        if not runs[0][0].startswith(("∙", "-", "※")):
            runs = [(indent, runs[0][1], False, INK)] + runs
        out.append(runs)
    return out


# ---------------------------------------------------------------------------
# Page chrome: side tab and footer float; PART box + rule + running head as the first band.
# ---------------------------------------------------------------------------
L.add_table([[cell(0, 3350, 1680, [para([("01", 1380, True, WHITE)], "CENTER")[0]], dark)],
             [cell(0, 3350, 5960, [para([(ch, 950, True, INK)], "CENTER", 1160)[0] for ch in "경영관리"], gray2)]],
            floating=(57800, 15000))
foot = [(text, size, False, INK) for text, size in (
    (line1(450, 455, 818, 822)["text"], 790), ("    ", 790), (line1(540, 546, 816, 820)["text"], 1090))]
L.add_table([[cell(0, W, 1500, [para(foot, "RIGHT", 1300)[0]])]], floating=(5660, 81550))

g = Grid("head", [X0, 99.0, 158.5, 375.0, X1], [1680])
g.put(X0, 99.0, 0, 1, [[("PART ", 800, False, INK), ("01", 1300, True, INK)]], frame("#EFEFEF", top="strong"))
g.put(99.0, 158.5, 0, 1, "경영관리", frame("#333333"), size=1080, bold=True, color=WHITE)
g.put(158.5, 375.0, 0, 1, [], frame(bottom="soft"))
g.put(375.0, X1, 0, 1, [line1(375, 385, 35, 40)], align="RIGHT")
block(g, 32.0)

g = Grid("title-1", [X0, X1], [2400])
g.put(X0, X1, 0, 1, [line1(200, 215, 68, 75)])
block(g, 68.5)

# ---------------------------------------------------------------------------
# Ⅰ. 외부 지적사항 조치실적: issue | actions (detail + ▣ result band) | reference page
# ---------------------------------------------------------------------------
xs = [X0, 193.0, 197.0, 514.7, 518.7, X1]
rows = [(124.4, 145.5, 168.7), (168.7, 188.0, 211.3), (211.3, 235.5, 263.3), (263.3, 298.0, 321.3)]
hs = [1890]
for a, b, e in rows:
    hs += [int(round((b - a) * 100)), int(round((e - b) * 100))]
g = Grid("issues", xs, hs)
g.put(X0, 193.0, 0, 1, [line1(100, 110, 108, 114)], LIGHT_HEAD)
g.put(197.0, 514.7, 0, 1, [runs_of(line1(315, 325, 108, 114), WHITE)], MID_HEAD)
g.put(518.7, X1, 0, 1, [line1(525, 530, 108, 114)], LIGHT_HEAD)
end = frame(bottom="dot")
detail = frame("#EBEBEB", left="soft", right="soft")
result = frame("#D1D1D1", bottom="dot", left="soft", right="soft")
for k, (a, b, e) in enumerate(rows):
    r = 1 + 2 * k
    g.put(X0, 197.0, r, r + 2, body_lines(55, 195, a, e), end, align="LEFT")
    g.put(197.0, 514.7, r, r + 1, body_lines(198, 210, a, b - 1), detail, align="LEFT")
    res = runs_of(line1(212, 220, b, e))
    g.put(197.0, 514.7, r + 1, r + 2, [[("▣ ", 1050, True, INK)] + res], result, align="LEFT")
    g.put(514.7, X1, r, r + 2, [line1(525, 530, a, e)], end)
block(g, 105.5)

g = Grid("note", [X0, X1], [1300])
g.put(X0, X1, 0, 1, [line1(55, 60, 326, 332)], align="LEFT", line=1100)
block(g, 327.0)

g = Grid("title-2", [X0, X1], [2400])
g.put(X0, X1, 0, 1, [line1(205, 215, 375, 382)])
block(g, 375.5)


# ---------------------------------------------------------------------------
# Ⅱ. 2025년 주요 추진실적: 평가내용 band, then '24 / '25 / 개선성과 columns
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


left_fill = frame(bottom="soft")
mid_fill = frame("#EBEBEB", bottom="soft", left="soft", right="soft")
gap_fill = frame(bottom="soft")


def columns(name, cx, top, head_y, body_y, height):
    """Three tabbed columns: header row then one body row of bullet lines per column."""
    g = Grid(name, cx, [2050, height])
    heads = lines_in(55, 560, head_y - 4, head_y + 4)
    assert len(heads) == 3, [h["text"] for h in heads]
    g.put(cx[0], cx[1], 0, 1, [heads[0]], LIGHT_HEAD)
    g.put(cx[2], cx[3], 0, 1, [runs_of(heads[1], WHITE)], MID_HEAD)
    g.put(cx[4], cx[5], 0, 1, [heads[2]], LIGHT_HEAD)
    y0, y1 = body_y
    g.put(cx[0], cx[1], 1, 2, body_lines(55, cx[1] - 5, y0, y1), left_fill, align="LEFT")
    g.put(cx[1], cx[2], 1, 2, [], gap_fill)
    g.put(cx[2], cx[3], 1, 2, body_lines(cx[2] - 3, cx[3] - 5, y0, y1), mid_fill, align="LEFT")
    g.put(cx[3], cx[4], 1, 2, [], gap_fill)
    g.put(cx[4], cx[5], 1, 2, body_lines(cx[4] - 3, 560, y0, y1), left_fill, align="LEFT")
    block(g, top)


CX = [X0, 210.0, 214.0, 381.5, 385.4, X1]
band(1, 413.0, 454.4)
columns("cols-1", CX, 460.7, 465, (485, 540), 6390)
band(2, 561.5, 602.9)
columns("cols-2", CX, 609.2, 613, (632, 670), 4410)
band(3, 690.1, 731.5)
columns("cols-3", [X0, 204.4, 208.3, 378.7, 382.6, X1], 737.8, 742, (760, 798), 4410)

kit.finish(target, end=802.4)
