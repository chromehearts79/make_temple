"""Rebuild KDN 2025 report PDF page 59 (second PDF local page 9, printed page 36) as editable HWPX.

Usage: python3 work/kdn2025/p59.py <report2.pdf> <out.hwpx> [--page 9]

First body page of the 안전 및 재난관리 indicator: "Ⅰ. 외부 지적사항 조치실적" table and the
"Ⅱ. 2025년 주요 추진실적" three-column blocks, the same page type as p35.py and the skill recipe
kdn_p49.py (light / mid-gray header tabs, gray detail column with darker result bands, 평가내용
chip + hatched title). Built with the shared kit: one flat table per band, rows at the PDF y
positions, all text and run sizes from the PDF text layer.

Images in the source and how they are kept:
- PART 01 box, side tab, 평가내용 chips and the ☑ result marks (-> ▣): typed as cells / glyphs.
- the source prints "평가내용 01" on BOTH 평가내용 chips (the second one would be 02); kept as printed.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kit  # noqa: E402
from kit import Layout, recipe_inputs  # noqa: E402

source, target = recipe_inputs(9, "외부 안전교육 이수 후 개선 피드백")
L = Layout(top=3200)
kit.setup(source, L)
from kit import *  # noqa: E402,F401,F403  helpers and presets bound to this page

LIGHT_HEAD = frame("#D7D7D7", top="strong", left="soft", right="soft")
MID_HEAD = frame("#808080", top="strong", left="soft", right="soft")


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

g = Grid("head", [X0, 99.0, 158.5, 399.7, X1], [1680])
g.put(X0, 99.0, 0, 1, [[("PART ", 800, False, INK), ("01", 1300, True, INK)]], frame("#EFEFEF", top="strong"))
g.put(99.0, 158.5, 0, 1, "경영관리", frame("#333333"), size=1080, bold=True, color=WHITE)
g.put(158.5, 399.7, 0, 1, [], frame(bottom="soft"))
g.put(399.7, X1, 0, 1, [line1(400, 410, 35, 40)], align="RIGHT")
block(g, 32.0)

g = Grid("title-1", [X0, X1], [2400])
g.put(X0, X1, 0, 1, [line1(205, 210, 68, 75)])
block(g, 68.5)

# ---------------------------------------------------------------------------
# Ⅰ. 외부 지적사항 조치실적: issue | actions (detail + ▣ result bands) | reference page
# ---------------------------------------------------------------------------
xs = [X0, 201.0, 205.5, 514.5, 519.0, X1]
# per issue: top, end of the detail lines, end of each ▣ result band
rows = [(125.8, 159.5, 182.3), (182.3, 246.5, 269.4), (269.4, 302.5, 323.5, 346.5)]
hs = [2000]
for ys in rows:
    hs += [int(round((b - a) * 100)) for a, b in zip(ys, ys[1:])]
g = Grid("issues", xs, hs)
g.put(X0, 201.0, 0, 1, [line1(100, 115, 108, 113)], LIGHT_HEAD)
g.put(205.5, 514.5, 0, 1, [runs_of(line1(320, 330, 108, 113), WHITE)], MID_HEAD)
g.put(519.0, X1, 0, 1, [line1(525, 530, 108, 113)], LIGHT_HEAD)
end = frame(bottom="dot")
detail = frame("#ECECEC", left="soft", right="soft")
result = frame("#D1D1D1", left="soft", right="soft")
result_end = frame("#D1D1D1", bottom="dot", left="soft", right="soft")
r = 1
for ys in rows:
    a, b, e = ys[0], ys[1], ys[-1]
    n = len(ys) - 1
    g.put(X0, 205.5, r, r + n, hang(lines_in(55, 200, a, e), 59.7), end, align="LEFT")
    g.put(205.5, 514.5, r, r + 1, hang(lines_in(205, 250, a, b - 2), 208.5), detail, align="LEFT")
    for k, (y0, y1) in enumerate(zip(ys[1:], ys[2:])):
        res = runs_of(line1(220, 230, y0, y1))
        g.put(205.5, 514.5, r + 1 + k, r + 2 + k, [[("▣ ", 1050, True, INK)] + res],
              result_end if k == n - 2 else result, align="LEFT")
    g.put(514.5, X1, r, r + n, [line1(525, 530, a, e)], end)
    r += n
block(g, 105.8)

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
    g = Grid(f"band-{number}-{top:.0f}", [X0, 124.0, X1], [1950, h - 1950])
    g.put(X0, 124.0, 0, 1, f"평가내용 {number:02}", frame("#565656", top="strong"),
          size=970, bold=True, color=WHITE, ratio=80)
    g.put(X0, 124.0, 1, 2, [], frame("#E9E9E9", bottom="soft", left="soft", hatch="#DADADA"))
    g.put(124.0, X1, 0, 2, lines_in(125, 130, top, bottom), frame("#E9E9E9", top="strong", bottom="soft",
                                                                    right="soft", hatch="#DADADA"),
          align="LEFT", line=1480)
    block(g, top)


CX = [X0, 210.0, 214.0, 389.8, 394.0, X1]
BASES = (59.7, 217.0, 397.0)
left_fill = frame(bottom="soft")
mid_fill = frame("#ECECEC", bottom="soft", left="soft", right="soft")
gap_fill = frame(bottom="soft")


def columns(name, head_y, top, groups):
    """Three column heads, then text groups (y0, y1) separated by a full-width rule."""
    g = Grid(name, CX, [2000] + [int(round((y1 - y0) * 100)) for y0, y1 in groups])
    heads = lines_in(55, 560, head_y - 4, head_y + 4)
    assert len(heads) == 3, [h["text"] for h in heads]
    g.put(CX[0], CX[1], 0, 1, [heads[0]], LIGHT_HEAD)
    g.put(CX[2], CX[3], 0, 1, [runs_of(heads[1], WHITE)], MID_HEAD)
    g.put(CX[4], CX[5], 0, 1, [heads[2]], LIGHT_HEAD)
    for r, (y0, y1) in enumerate(groups, 1):
        for k, fill in enumerate((left_fill, mid_fill, left_fill)):
            a, e = CX[2 * k], CX[2 * k + 1]
            g.put(a, e, r, r + 1, hang(lines_in(a - 3, e - 15, y0, y1), BASES[k]), fill, align="LEFT")
            if k < 2:
                g.put(e, CX[2 * k + 2], r, r + 1, [], gap_fill)
    block(g, top)


band(1, 436.0, 478.0)
columns("cols-1", 488, 483.8, [(503.8, 552.8), (552.8, 602.4)])
band(1, 620.0, 662.0)          # the source prints 평가내용 01 again
columns("cols-2", 672, 667.8, [(687.8, 751.4), (751.4, 800.0)])

kit.finish(target, end=802.0)
