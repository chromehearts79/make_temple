"""Rebuild KDN 2025 report physical PDF page 35 (printed page 20) as editable HWPX.

Usage: python3 work/kdn2025/p35.py <report.pdf> <out.hwpx> [--page N]

First body page of the 윤리경영 indicator: "Ⅰ. 외부 지적사항 조치실적" table and the
"Ⅱ. 2025년 주요 추진실적" three-column blocks, the same page type as the skill recipe
kdn_p49.py (same fills: light / mid-gray header tabs, gray detail column with a darker
result band, 평가내용 chip + hatched title). Built with the shared kit: one flat table per
band, rows at the PDF y positions, text and run sizes from the PDF text layer.

Images in the source and how they are kept:
- PART 01 box, side tab, 평가내용 chips, the ☑ result marks (→ ▣): typed as cells / glyphs.
- the three small bar charts (기관장 노력도, 신고채널 신뢰도, 협력사 인권경영지수): value cells,
  values read from a 5x render; the people icon is omitted.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kit  # noqa: E402
from kit import Layout, recipe_inputs  # noqa: E402

source, target = recipe_inputs(35, "하도급 입찰 담합 예방 절차의")
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
# Page chrome: side tab and footer float; PART box + running head as the first band.
# ---------------------------------------------------------------------------
L.add_table([[cell(0, 3350, 1680, [para([("01", 1380, True, WHITE)], "CENTER")[0]], dark)],
             [cell(0, 3350, 5960, [para([(ch, 950, True, INK)], "CENTER", 1160)[0] for ch in "경영관리"], gray2)]],
            floating=(57800, 15000))
foot = [(text, size, False, INK) for text, size in (
    (line1(450, 455, 818, 822)["text"], 790), ("    ", 790), (line1(540, 546, 816, 820)["text"], 1090))]
L.add_table([[cell(0, W, 1500, [para(foot, "RIGHT", 1300)[0]])]], floating=(5660, 81550))

g = Grid("head", [X0, 99.0, 158.5, 466.3, X1], [1680])
g.put(X0, 99.0, 0, 1, [[("PART ", 800, False, INK), ("01", 1300, True, INK)]], frame("#EFEFEF", top="strong"))
g.put(99.0, 158.5, 0, 1, "경영관리", frame("#333333"), size=1080, bold=True, color=WHITE)
g.put(158.5, 466.3, 0, 1, [], frame(bottom="soft"))
g.put(466.3, X1, 0, 1, [line1(465, 480, 35, 40)], align="RIGHT")
block(g, 32.0)

g = Grid("title-1", [X0, X1], [2400])
g.put(X0, X1, 0, 1, [line1(200, 215, 68, 75)])
block(g, 68.5)

# ---------------------------------------------------------------------------
# Ⅰ. 외부 지적사항 조치실적: issue | actions (detail + ▣ result band) | reference page
# ---------------------------------------------------------------------------
xs = [X0, 193.0, 197.0, 514.7, 518.7, X1]
rows = [(123.2, 153.6, 176.4), (176.4, 205.5, 228.3), (228.3, 257.4, 280.2), (280.2, 335.7, 358.7)]
hs = [1770]
for a, b, e in rows:
    hs += [int(round((b - a) * 100)), int(round((e - b) * 100))]
g = Grid("issues", xs, hs)
g.put(X0, 193.0, 0, 1, [line1(100, 110, 108, 112)], LIGHT_HEAD)
g.put(197.0, 514.7, 0, 1, [runs_of(line1(315, 325, 108, 112), WHITE)], MID_HEAD)
g.put(518.7, X1, 0, 1, [line1(525, 530, 108, 112)], LIGHT_HEAD)
end = frame(bottom="dot")
detail = frame("#EBEBEB", left="soft", right="soft")
result = frame("#D1D1D1", bottom="dot", left="soft", right="soft")
for k, (a, b, e) in enumerate(rows):
    r = 1 + 2 * k
    g.put(X0, 197.0, r, r + 2, body_lines(55, 195, a, e), end, align="LEFT")
    g.put(197.0, 514.7, r, r + 1, body_lines(198, 210, a, b - 2), detail, align="LEFT")
    res = runs_of(line1(212, 215, b, e))
    g.put(197.0, 514.7, r + 1, r + 2, [[("▣ ", 1050, True, INK)] + res], result, align="LEFT")
    g.put(514.7, X1, r, r + 2, [line1(525, 530, a, e)], end)
block(g, 105.5)

g = Grid("note", [X0, X1], [1300])
g.put(X0, X1, 0, 1, [line1(55, 60, 360, 365)], align="LEFT", line=1100)
block(g, 360.5)

g = Grid("title-2", [X0, X1], [2400])
g.put(X0, X1, 0, 1, [line1(205, 215, 385, 390)])
block(g, 384.5)


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


CX = [X0, 190.2, 194.2, 384.4, 388.4, X1]


def column_heads(g, y):
    heads = lines_in(55, 560, y - 4, y + 4)
    assert len(heads) == 3, [h["text"] for h in heads]
    g.put(CX[0], CX[1], 0, 1, [heads[0]], LIGHT_HEAD)
    g.put(CX[2], CX[3], 0, 1, [runs_of(heads[1], WHITE)], MID_HEAD)
    g.put(CX[4], CX[5], 0, 1, [heads[2]], LIGHT_HEAD)


left_fill = frame(bottom="soft")
mid_fill = frame("#EBEBEB", bottom="soft", left="soft", right="soft")
gap_fill = frame(bottom="soft")
tag = frame("#3C3C3C")
chart_title = frame(top="soft", bottom="soft", left="soft", right="soft")

# 평가내용 01: the right column holds two bar charts (images) -> value cells.
band(1, 421.5, 462.9)
cx = [X0, 190.2, 194.2, 384.4, 388.4, 393.0, 431.0, 470.0, 478.0, 516.0, 553.0, X1]
body = [700, 1550, 700, 1450, 1250, 1350, 520]
g = Grid("cols-1", cx, [2060] + body)
column_heads(g, 474)
n = len(body)
g.put(X0, 190.2, 1, 1 + n, body_lines(55, 190, 490, 560), left_fill, align="LEFT")
g.put(190.2, 194.2, 1, 1 + n, [], gap_fill)
g.put(194.2, 384.4, 1, 1 + n, body_lines(195, 384, 490, 560), mid_fill, align="LEFT")
g.put(384.4, 388.4, 1, 1 + n, [], gap_fill)
charts = [((393.0, 431.0, 470.0), "기관장 노력도", "28.1%↑", "64점", "82점"),
          ((478.0, 516.0, 553.0), "신고채널 신뢰도", "3.5%p↑", "79.9%", "83.4%")]
for (a, b, e), name, rise, before, after in charts:
    g.put(a, e, 2, 3, name, chart_title, size=900, bold=True)
    g.put(a, e, 4, 5, rise, tag, size=900, bold=True, color=WHITE)
    g.put(a, b, 5, 6, before, size=950, line=1080)
    g.put(b, e, 5, 6, after, size=950, bold=True, line=1080)
    g.put(a, b, 6, 7, "’24년", size=850, line=980)
    g.put(b, e, 6, 7, "’25년", size=850, bold=True, line=980)
g.put(388.4, X1, 7, 8, [], frame(bottom="soft"))
block(g, 469.2)

# 평가내용 02: text in all three columns.
band(2, 574.4, 603.0)
g = Grid("cols-2", CX, [2070, 6020])
column_heads(g, 614)
g.put(CX[0], CX[1], 1, 2, body_lines(55, 190, 630, 690), left_fill, align="LEFT")
g.put(CX[1], CX[2], 1, 2, [], gap_fill)
g.put(CX[2], CX[3], 1, 2, body_lines(195, 384, 630, 690), mid_fill, align="LEFT")
g.put(CX[3], CX[4], 1, 2, [], gap_fill)
g.put(CX[4], CX[5], 1, 2, body_lines(389, 400, 630, 690), left_fill, align="LEFT")
block(g, 609.3)

# 평가내용 03: one chart (협력사 인권경영지수) with an icon (omitted) -> value cells.
band(3, 699.4, 728.0)
cx = [X0, 190.2, 194.2, 384.4, 388.4, 393.0, 466.0, 474.0, 513.0, X1]
body = [450, 1500, 1300, 1150, 250]
g = Grid("cols-3", cx, [2070] + body)
column_heads(g, 739)
n = len(body)
g.put(X0, 190.2, 1, 1 + n, body_lines(55, 190, 755, 800), left_fill, align="LEFT")
g.put(190.2, 194.2, 1, 1 + n, [], gap_fill)
g.put(194.2, 384.4, 1, 1 + n, body_lines(195, 384, 755, 800), mid_fill, align="LEFT")
g.put(384.4, 388.4, 1, 1 + n, [], gap_fill)
g.put(393.0, 466.0, 2, 3, "협력사 인권경영지수", chart_title, size=850, bold=True)
g.put(474.0, X1, 2, 3, "4.41%↑", tag, size=900, bold=True, color=WHITE)
g.put(474.0, 513.0, 3, 4, "83.9점", size=950, line=1080)
g.put(513.0, X1, 3, 4, "87.6점", size=950, bold=True, line=1080)
g.put(474.0, 513.0, 4, 5, "’24년", size=850, line=980)
g.put(513.0, X1, 4, 5, "’25년", size=850, bold=True, line=980)
g.put(388.4, X1, 5, 6, [], frame(bottom="soft"))
block(g, 734.3)

kit.finish(target, end=802.0)
