"""Rebuild KDN 2025 report page 77 (second PDF local page 27, printed page 49) as editable HWPX.

Usage: python3 work/kdn2025/p77.py <report2.pdf> <out.hwpx> [--page 27]

First body page of the 창업 및 경제활성화 indicator: "Ⅰ. 외부 지적사항 조치실적" table and the
"Ⅱ. 2025년 주요 추진실적" four 평가내용 blocks with '24 / '25 / 개선성과 columns. Same page type
as p35.py and the skill recipe kdn_p49.py (light / mid-gray header tabs, gray detail column
with a darker result band, 평가내용 chip + hatched title). Built with the shared kit: one flat
table per band, rows at the PDF y positions, text and run sizes from the PDF text layer.

Images in the source and how they are kept: PART box, side tab, 평가내용 chips, the ☑ result
marks (-> ▣) are typed as cells / glyphs. All other text is in the PDF text layer.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kit  # noqa: E402
from kit import Layout, recipe_inputs  # noqa: E402

source, target = recipe_inputs(27, "수출성과가 중소기업 실적에")
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
# Page chrome (odd page): side tab and footer float; PART box + running head as the first band.
# ---------------------------------------------------------------------------
L.add_table([[cell(0, 3350, 1680, [para([("01", 1380, True, WHITE)], "CENTER")[0]], dark)],
             [cell(0, 3350, 5960, [para([(ch, 950, True, INK)], "CENTER", 1160)[0] for ch in "경영관리"], gray2)]],
            floating=(57800, 15000))
foot = [(text, size, False, INK) for text, size in (
    (line1(450, 455, 818, 822)["text"], 790), ("    ", 790), (line1(540, 546, 816, 820)["text"], 1090))]
L.add_table([[cell(0, W, 1500, [para(foot, "RIGHT", 1300)[0]])]], floating=(5660, 81550))

g = Grid("head", [X0, 99.0, 158.5, 390.0, X1], [1680])
g.put(X0, 99.0, 0, 1, [[("PART ", 800, False, INK), ("01", 1300, True, INK)]], frame("#EFEFEF", top="strong"))
g.put(99.0, 158.5, 0, 1, "경영관리", frame("#333333"), size=1080, bold=True, color=WHITE)
g.put(158.5, 390.0, 0, 1, [], frame(bottom="soft"))
g.put(390.0, X1, 0, 1, [line1(390, 400, 35, 40)], align="RIGHT")
block(g, 32.0)

g = Grid("title-1", [X0, X1], [2400])
g.put(X0, X1, 0, 1, [line1(200, 215, 68, 75)])
block(g, 68.5)

# ---------------------------------------------------------------------------
# Ⅰ. 외부 지적사항 조치실적: issue | actions (detail + ▣ result band) | reference page
# ---------------------------------------------------------------------------
xs = [X0, 193.0, 197.0, 514.7, 518.7, X1]
rows = [(123.3, 144.0, 165.7), (165.7, 186.0, 208.2), (208.2, 228.5, 250.7), (250.7, 271.0, 293.5)]
hs = [1730]
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
    g.put(197.0, 514.7, r, r + 1, body_lines(198, 210, a, b - 1), detail, align="LEFT")
    res = runs_of(line1(214, 220, b, e))
    g.put(197.0, 514.7, r + 1, r + 2, [[("▣ ", 1050, True, INK)] + res], result, align="LEFT")
    g.put(514.7, X1, r, r + 2, [line1(525, 530, a, e)], end)
block(g, 105.8)

g = Grid("note", [X0, X1], [1300])
g.put(X0, X1, 0, 1, [line1(55, 60, 297, 302)], align="LEFT", line=1100)
block(g, 297.5)

g = Grid("title-2", [X0, X1], [2400])
g.put(X0, X1, 0, 1, [line1(205, 215, 331, 337)])
block(g, 331.5)


# ---------------------------------------------------------------------------
# Ⅱ. 2025년 주요 추진실적: 평가내용 band, then '24 / '25 / 개선성과 columns
# ---------------------------------------------------------------------------
def band(number, top, bottom):
    """평가내용 chip in the top-left corner, hatched title over the full band height."""
    h = int(round((bottom - top) * 100))
    g = Grid(f"band-{number}", [X0, 124.0, X1], [1650, h - 1650])
    g.put(X0, 124.0, 0, 1, f"평가내용 {number:02}", frame("#565656", top="strong"),
          size=970, bold=True, color=WHITE, ratio=80)
    g.put(X0, 124.0, 1, 2, [], frame("#E9E9E9", bottom="soft", left="soft", hatch="#DADADA"))
    g.put(124.0, X1, 0, 2, lines_in(125, 130, top, bottom), frame("#E9E9E9", top="strong", bottom="soft",
                                                                    right="soft", hatch="#DADADA"),
          align="LEFT", line=1480)
    block(g, top)


CX = [X0, 190.0, 194.2, 361.4, 366.0, X1]
left_fill = frame(bottom="soft")
mid_fill = frame("#EBEBEB", bottom="soft", left="soft", right="soft")
gap_fill = frame(bottom="soft")


def columns(number, top, head_y, body_h, y0, y1):
    """Three column heads (light / mid-gray / light) over three bullet cells."""
    g = Grid(f"cols-{number}", CX, [1800, body_h])
    heads = lines_in(55, 560, head_y - 4, head_y + 4)
    assert len(heads) == 3, [h["text"] for h in heads]
    g.put(CX[0], CX[1], 0, 1, [heads[0]], LIGHT_HEAD)
    g.put(CX[2], CX[3], 0, 1, [runs_of(heads[1], WHITE)], MID_HEAD)
    g.put(CX[4], CX[5], 0, 1, [heads[2]], LIGHT_HEAD)
    g.put(CX[0], CX[1], 1, 2, body_lines(55, 190, y0, y1), left_fill, align="LEFT")
    g.put(CX[1], CX[2], 1, 2, [], gap_fill)
    g.put(CX[2], CX[3], 1, 2, body_lines(195, 361, y0, y1), mid_fill, align="LEFT")
    g.put(CX[3], CX[4], 1, 2, [], gap_fill)
    g.put(CX[4], CX[5], 1, 2, body_lines(366, 400, y0, y1), left_fill, align="LEFT")
    block(g, top)


band(1, 368.0, 396.0)
columns(1, 400.5, 403.0, 3880, 418, 458)
band(2, 475.5, 504.0)
columns(2, 510.0, 512.5, 3880, 527, 567)
band(3, 585.0, 613.5)
columns(3, 619.5, 622.0, 3880, 637, 676)
band(4, 694.5, 722.5)
columns(4, 729.0, 731.5, 5280, 746, 800)

kit.finish(target, end=802.0)
