"""Rebuild KDN 2025 report page 139 (third PDF local page 39, printed page 96) as editable HWPX.

Usage: python3 work/kdn2025/p139.py <report3.pdf> <out.hwpx> [--page 39]

First body page of the 조직 운영 및 관리(노사관계) indicator: "Ⅰ. 외부 지적사항 조치실적" table and
the "Ⅱ. 2025년 주요 추진실적" three-column blocks for 평가내용 01-03. Same page type as p35.py,
p59.py and p69.py (light / mid-gray header tabs, gray detail column with an inset darker result
band, 평가내용 chip + hatched title). Built with the shared kit: one flat table per band, rows at
the PDF y positions, all text and run sizes from the PDF text layer.

Images in the source and how they are kept:
- PART 01 box, side tab, 평가내용 chips (check icon dropped): typed as cells.
- the ☑ result marks -> ▣ glyphs; the decorative triangles in the top-left corner are omitted.
- the page prints its footer at the right ("2025년도 경영실적보고서 96") with the side tab, as an
  odd page does, although 96 is even; kept as printed.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kit  # noqa: E402
from kit import Layout, recipe_inputs  # noqa: E402

source, target = recipe_inputs(39, "노동이사 이사회 경영제언 건수 17% 향상")
L = Layout(top=3200)
kit.setup(source, L)
from kit import *  # noqa: E402,F401,F403  helpers and presets bound to this page

LIGHT_HEAD = frame("#D7D7D7", top="strong", left="soft", right="soft")
MID_HEAD = frame("#787878", top="strong", left="soft", right="soft")
GRAY = "#E6E6E6"


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
# Page chrome: side tab and footer float; PART box + running head as the first band.
# ---------------------------------------------------------------------------
L.add_table([[cell(0, 3350, 1680, [para([("01", 1380, True, WHITE)], "CENTER")[0]], dark)],
             [cell(0, 3350, 5960, [para([(ch, 950, True, INK)], "CENTER", 1160)[0] for ch in "경영관리"], gray2)]],
            floating=(57800, 15000))
foot = [(text, size, False, INK) for text, size in (
    (line1(450, 455, 818, 822)["text"], 790), ("    ", 790), (line1(540, 546, 816, 820)["text"], 1090))]
L.add_table([[cell(0, W, 1500, [para(foot, "RIGHT", 1300)[0]])]], floating=(5660, 81550))

g = Grid("head", [X0, 99.0, 158.5, 430.0, X1], [1680])
g.put(X0, 99.0, 0, 1, [[("PART ", 800, False, INK), ("01", 1300, True, INK)]], frame("#EFEFEF", top="strong"))
g.put(99.0, 158.5, 0, 1, "경영관리", frame("#333333"), size=1080, bold=True, color=WHITE)
g.put(158.5, 430.0, 0, 1, [], frame(bottom="soft"))
g.put(430.0, X1, 0, 1, [line1(430, 440, 35, 40)], align="RIGHT")
block(g, 32.0)

g = Grid("title-1", [X0, X1], [2400])
g.put(X0, X1, 0, 1, [line1(205, 210, 69, 75)])
block(g, 68.0)

# ---------------------------------------------------------------------------
# Ⅰ. 외부 지적사항 조치실적: issue | actions (gray, inset ▣ result band) | reference page
# ---------------------------------------------------------------------------
xs = [X0, 212.8, 216.8, 221.0, 510.2, 514.5, 518.8, X1]
# per issue: top, result band top, result band bottom, row end (dotted rule)
ISSUES = [(126.2, 145.8, 162.8, 166.8), (166.8, 201.8, 218.5, 222.8), (222.8, 242.2, 259.2, 263.2),
          (263.2, 282.8, 299.8, 303.8), (303.8, 323.2, 340.2, 345.5)]
GAP = 180
hs = [2070]
for a, b, c, e in ISSUES:
    hs += [int(round((b - a) * 100)), int(round((c - b) * 100)), int(round((e - c) * 100)) - GAP, GAP]
g = Grid("issues", xs, hs)
g.put(X0, 212.8, 0, 1, [line1(110, 120, 108, 113)], LIGHT_HEAD)
g.put(216.8, 514.5, 0, 1, [runs_of(line1(325, 335, 108, 113), WHITE)], MID_HEAD)
g.put(518.8, X1, 0, 1, [line1(525, 530, 108, 113)], LIGHT_HEAD)
gray = frame(GRAY)
for k, (a, b, c, e) in enumerate(ISSUES):
    r = 1 + 4 * k
    rule = "soft" if k == len(ISSUES) - 1 else "dot"
    g.put(X0, 216.8, r, r + 4, hang(lines_in(55, 212, a, e), 59.7), frame(bottom=rule), align="LEFT", line=1550)
    g.put(216.8, 514.5, r, r + 1, hang(lines_in(216, 230, a, b - 2), 219.8), gray, align="LEFT", line=1540)
    g.put(216.8, 221.0, r + 1, r + 2, [], gray)
    g.put(221.0, 510.2, r + 1, r + 2, [[("▣ ", 1050, True, INK)] + runs_of(line1(230, 240, b - 1, c))],
          frame("#C8C8C8"), align="LEFT", line=1300)
    g.put(510.2, 514.5, r + 1, r + 2, [], gray)
    g.put(216.8, 514.5, r + 2, r + 3, [], gray)
    g.put(216.8, 514.5, r + 3, r + 4, [], frame(bottom=rule))
    g.put(514.5, X1, r, r + 4, [line1(520, 530, a, e)], frame(bottom=rule))
block(g, 105.5)

g = Grid("note", [X0, X1], [1300])
g.put(X0, X1, 0, 1, [line1(55, 60, 350, 355)], align="LEFT", line=1100)
block(g, 350.5)

g = Grid("title-2", [X0, X1], [2400])
g.put(X0, X1, 0, 1, [line1(210, 215, 399, 405)])
block(g, 398.5)


# ---------------------------------------------------------------------------
# Ⅱ. 2025년 주요 추진실적: 평가내용 band, then '24 / '25 / 개선성과 columns
# ---------------------------------------------------------------------------
def band(number, top, bottom):
    """평가내용 chip in the top-left corner, hatched title over the full band height."""
    h = int(round((bottom - top) * 100))
    g = Grid(f"band-{number}", [X0, 124.0, X1], [1720, h - 1720])
    g.put(X0, 124.0, 0, 1, f"평가내용 {number:02}", frame("#565656", top="strong"),
          size=970, bold=True, color=WHITE, ratio=80, line=1150)
    g.put(X0, 124.0, 1, 2, [], frame("#E9E9E9", bottom="soft", left="soft", hatch="#DADADA"))
    g.put(124.0, X1, 0, 2, lines_in(125, 130, top, bottom), frame("#E9E9E9", top="strong", bottom="soft",
                                                                    right="soft", hatch="#DADADA"),
          align="LEFT", line=1480)
    block(g, top)


CX = [X0, 220.0, 224.2, 388.0, 391.8, X1]
BASES = (59.7, 227.3, 395.0)
left_fill = frame(bottom="soft")
mid_fill = frame(GRAY, bottom="soft", left="soft", right="soft")
gap_fill = frame(bottom="soft")


def columns(name, head_y, top, body_end):
    """Three column heads over one body row of bullet lines."""
    body_top = top + 20.7
    g = Grid(name, CX, [2070, int(round((body_end - body_top) * 100))])
    heads = lines_in(55, 560, head_y - 4, head_y + 4)
    assert len(heads) == 3, [h["text"] for h in heads]
    g.put(CX[0], CX[1], 0, 1, [heads[0]], LIGHT_HEAD)
    g.put(CX[2], CX[3], 0, 1, [runs_of(heads[1], WHITE)], MID_HEAD)
    g.put(CX[4], CX[5], 0, 1, [heads[2]], LIGHT_HEAD)
    for k, fill in enumerate((left_fill, mid_fill, left_fill)):
        a, e = CX[2 * k], CX[2 * k + 1]
        g.put(a, e, 1, 2, hang(lines_in(a - 3, e - 15, body_top, body_end), BASES[k]), fill, align="LEFT",
              line=1540)
        if k < 2:
            g.put(e, CX[2 * k + 2], 1, 2, [], gap_fill)
    block(g, top)


band(1, 436.0, 477.0)
columns("cols-1", 487.5, 483.5, 561.2)
band(2, 583.5, 611.8)
columns("cols-2", 622.3, 618.2, 681.0)
band(3, 705.0, 733.2)
columns("cols-3", 743.8, 739.8, 802.3)

kit.finish(target, end=802.5)
