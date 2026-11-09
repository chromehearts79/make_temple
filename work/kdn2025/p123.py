"""Rebuild KDN 2025 report page 123 (3rd PDF local page 23, printed page 83) as editable HWPX.

Usage: python3 work/kdn2025/p123.py <report3.pdf> <out.hwpx> [--page 23]

First body page of the 조직 운영 및 관리(조직 및 인적자원관리) indicator: "Ⅰ. 외부 지적사항
조치실적" table (seven issues) and "Ⅱ. 2025년 주요 추진실적" with five 평가내용 bands, each over
'24 / '25 / 개선성과 columns. Same page type as p35.py / p59.py / p69.py (light / mid-gray header
tabs, gray detail column with an inset darker result band, 평가내용 chip + hatched title). Built
with the shared kit: one flat table per band, rows at the PDF y positions, all text and run
sizes from the PDF text layer.

Images in the source and how they are kept:
- PART 01 box, side tab, 평가내용 chips (check icon dropped): typed as cells.
- the ☑ result marks -> ▣ glyphs.
- the source prints "평가내용 01" on the fifth chip as well (it would be 05); kept as printed.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kit  # noqa: E402
from kit import Layout, recipe_inputs  # noqa: E402

source, target = recipe_inputs(23, "저성과부서 선정기준 명확화")
L = Layout(top=3200)
kit.setup(source, L)
from kit import *  # noqa: E402,F401,F403  helpers and presets bound to this page

LIGHT_HEAD = frame("#D9D9D9", top="strong", left="soft", right="soft")
MID_HEAD = frame("#7F7F7F", top="strong", left="soft", right="soft")
REF_HEAD = frame("#CCCCCC", top="strong", left="soft", right="soft")
GRAY = "#EBEBEB"


def hang(lines, base):
    """Lines keep their PDF indent: spaces for the x offset and for the line's own leading blanks."""
    out = []
    for line in lines:
        runs = runs_of(line)
        size = runs[0][1] / 100
        raw = "".join(s["text"] for s in line["spans"])
        offset = line["bbox"][0] - base + (len(raw) - len(raw.lstrip(" "))) * 0.29 * size
        n = max(0, round(offset / (0.29 * size)))
        out.append([(" " * n, runs[0][1], False, INK)] + runs if n else runs)
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

g = Grid("head", [X0, 99.0, 158.5, 378.5, X1], [1680])
g.put(X0, 99.0, 0, 1, [[("PART ", 800, False, INK), ("01", 1300, True, INK)]], frame("#EFEFEF", top="strong"))
g.put(99.0, 158.5, 0, 1, "경영관리", frame("#333333"), size=1080, bold=True, color=WHITE)
g.put(158.5, 378.5, 0, 1, [], frame(bottom="soft"))
g.put(378.5, X1, 0, 1, [line1(380, 390, 35, 40)], align="RIGHT")
block(g, 32.0)

g = Grid("title-1", [X0, X1], [2400])
g.put(X0, X1, 0, 1, [line1(205, 210, 69, 74)])
block(g, 68.5)

# ---------------------------------------------------------------------------
# Ⅰ. 외부 지적사항 조치실적: issue | actions (gray, inset ▣ result band) | reference page
# ---------------------------------------------------------------------------
xs = [X0, 176.0, 180.1, 184.8, 509.8, 514.5, 518.7, X1]
TOPS = [116.6, 152.0, 187.4, 222.8, 258.2, 293.6, 329.1, 364.0]
hs = [int(round((TOPS[0] - 94.7) * 100))]
for a, e in zip(TOPS, TOPS[1:]):
    b, c = a + 14.8, a + 30.8          # result band from b to c; white gap with the rule below
    hs += [int(round((b - a) * 100)), int(round((c - b) * 100)), int(round((e - c) * 100))]
g = Grid("issues", xs, hs)
g.put(X0, 176.0, 0, 1, [line1(95, 100, 98, 102)], LIGHT_HEAD)
g.put(180.1, 514.5, 0, 1, [runs_of(line1(310, 315, 98, 102), WHITE)], MID_HEAD)
g.put(518.7, X1, 0, 1, [line1(525, 530, 98, 102)], REF_HEAD)
gray = frame(GRAY)
for k, (a, e) in enumerate(zip(TOPS, TOPS[1:])):
    r = 1 + 3 * k
    b = a + 14.8
    rule = "soft" if k == len(TOPS) - 2 else "dot"
    g.put(X0, 180.1, r, r + 3, hang(lines_in(55, 175, a, e), 59.7), frame(bottom=rule), align="LEFT", line=1330)
    g.put(180.1, 514.5, r, r + 1, [line1(182, 185, a, b - 2)], gray, align="LEFT", line=1300)
    g.put(180.1, 184.8, r + 1, r + 2, [], gray)
    g.put(184.8, 509.8, r + 1, r + 2, [[("▣ ", 1050, True, INK)] + runs_of(line1(200, 203, b, e))],
          frame("#CBCBCB"), align="LEFT", line=1300)
    g.put(509.8, 514.5, r + 1, r + 2, [], gray)
    g.put(180.1, 514.5, r + 2, r + 3, [], frame(bottom=rule))
    g.put(514.5, X1, r, r + 3, [line1(525, 530, a, e)], frame(bottom=rule))
block(g, 94.7)

g = Grid("note", [X0, X1], [1300])
g.put(X0, X1, 0, 1, [line1(55, 60, 366, 370)], align="LEFT", line=1100)
block(g, 366.5)

g = Grid("title-2", [X0, X1], [2400])
g.put(X0, X1, 0, 1, [line1(209, 213, 387, 391)])
block(g, 386.5)

# ---------------------------------------------------------------------------
# Ⅱ. 2025년 주요 추진실적: 평가내용 band, then '24 / '25 / 개선성과 columns
# ---------------------------------------------------------------------------
CX = [X0, 214.7, 218.7, 376.8, 380.8, X1]
chip = frame("#5F5F5F", top="strong")
band_fill = frame("#EEEEEE", top="strong", bottom="soft", right="soft", hatch="#DADADA")
BANDS = ((412.5, 453.9, 456.9, 495.7, 1), (501.8, 530.4, 533.4, 572.3, 2), (578.4, 607.0, 610.0, 648.8, 3),
         (654.9, 683.6, 686.6, 725.4, 4), (731.4, 760.1, 763.1, 801.9, 1))   # 5th chip prints "01"
for top, bottom, head, end, number in BANDS:
    h = int(round((bottom - top) * 100))
    g = Grid(f"band-{top:.0f}", [X0, 124.0, X1], [1950, h - 1950])
    g.put(X0, 124.0, 0, 1, f"평가내용 {number:02}", chip, size=970, bold=True, color=WHITE, ratio=80)
    g.put(X0, 124.0, 1, 2, [], frame("#EEEEEE", bottom="soft", left="soft", hatch="#DADADA"))
    g.put(124.0, X1, 0, 2, lines_in(125, 130, top, bottom), band_fill, align="LEFT", line=1510)
    block(g, top)

    g = Grid(f"cols-{top:.0f}", CX, [1890, int(round((end - head) * 100)) - 1890])
    heads = lines_in(55, 560, head + 1, head + 8)
    assert len(heads) == 3, [x["text"] for x in heads]
    g.put(CX[0], CX[1], 0, 1, [heads[0]], LIGHT_HEAD)
    g.put(CX[2], CX[3], 0, 1, [runs_of(heads[1], WHITE)], MID_HEAD)
    g.put(CX[4], CX[5], 0, 1, [heads[2]], LIGHT_HEAD)
    body = [(CX[0], CX[1], "1"), (CX[2], CX[3], GRAY), (CX[4], CX[5], "1")]
    for x0, x1, fill in body:
        line = line1(x0, x1, head + 20, end)
        g.put(x0, x1, 1, 2, [line], frame(fill if fill != "1" else None, bottom="soft"), align="LEFT")
    g.put(CX[1], CX[2], 1, 2, [], frame(bottom="soft"))
    g.put(CX[3], CX[4], 1, 2, [], frame(bottom="soft"))
    block(g, head)

kit.finish(target, end=802.5)
