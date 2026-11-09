"""Rebuild KDN 2025 report physical PDF page 16 (printed page 4): Ⅱ. 외부 지적사항 조치실적.

Usage: python3 work/kdn2025/p16.py <report.pdf> <out.hwpx> [--page N]

Same 지적사항 | 조치 및 개선실적 | 참고 table as the validated kdn_p49.py recipe, laid out with the
shared kit (work/kdn2025/kit.py): every band is one flat table placed at its PDF y. Text comes
from the PDF text layer cell by cell with its spans (bold, 8.9 pt parentheses, superscript
years). The PART box, the section number band, the gray strips and the check-box icons are
images in the source; the PART box and band are typed as cells, the check-box icon becomes ▣.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kit  # noqa: E402
from kit import Layout, recipe_inputs  # noqa: E402

source, target = recipe_inputs(16, "경영평가단 지적사항")
L = Layout(top=3100)
kit.setup(source, L)
from kit import *  # noqa: E402,F401,F403  helpers and presets bound to this page


def indented(line, spaces):
    """Runs of a PDF line with a visual indent (PDF continuation lines start further right)."""
    runs = runs_of(line)
    return [(" " * spaces + runs[0][0], *runs[0][1:])] + runs[1:] if spaces else runs


def para_lines(lines, base_x, step=3.4):
    """Each line indented by its PDF x offset from the column's bullet position, plus the
    leading blanks the PDF text itself carries ('  - ...')."""
    out = []
    for line in lines:
        lead = len(line["spans"][0]["text"]) - len(line["spans"][0]["text"].lstrip())
        offset = max(0, int(round((line["bbox"][0] - base_x) / step)))
        out.append(indented(line, lead + offset))
    return out


# ---------------------------------------------------------------------------
# Page chrome: even page -> "PART 01 | 경영관리" box at the left over a rule, footer at left.
# ---------------------------------------------------------------------------
foot = [(line1(55, 60, 816, 822)["text"], 1090, False, INK), ("    ", 1090, False, INK),
        ("한전KDN㈜", 1090, True, INK)]   # the logo is an image in the PDF
L.add_table([[cell(0, W, 1500, [para(foot, "LEFT", 1300)[0]])]], floating=(5660, 81550))

g = Grid("head", [X0, 102.6, 159.6, X1], [1600])
g.put(X0, 102.6, 0, 1, "PART 01", frame("#EFEFEF", top="strong"), size=1000, bold=True)
g.put(102.6, 159.6, 0, 1, "경영관리", frame("#333333"), size=1080, bold=True, color=WHITE)
g.put(159.6, X1, 0, 1, [], frame(bottom="soft"))
block(g, 31.0)

# Chapter title, centered (Ⅱ. regular 17.8 pt, title bold 18 pt).
g = Grid("title", [X0, X1], [2500])
g.put(X0, X1, 0, 1, [line1(200, 210, 68, 75)], line=2300, ratio=97)
block(g, 68.5)

# Section band: dark number square + light band (an image in the PDF).
g = Grid("section", [X0, 85.0, X1], [2300])
g.put(X0, 85.0, 0, 1, [line1(60, 70, 105, 112)], dark, color=WHITE, line=1850)
g.put(85.0, X1, 0, 1, [line1(85, 95, 105, 112)], frame("#E4E4E4", top="soft", bottom="soft"),
      align="LEFT", line=1750)
block(g, 105.5)

# ---------------------------------------------------------------------------
# 지적사항 | 조치 및 개선실적 | 참고  (eight items; achievement strip below the details)
# ---------------------------------------------------------------------------
XL, XR = 189.3, 516.7
bounds = [155.3, 226.4, 346.0, 430.6, 501.6, 572.6, 643.6, 714.6, 785.6]
strips = [198.6, 302.7, 402.8, 473.8, 544.8, 615.8, 686.8, 757.8]   # top of each gray strip
hs = [2050]
for k in range(8):
    hs += [int(round((strips[k] - 2.0 - bounds[k]) * 100)), int(round((bounds[k + 1] - strips[k] + 2.0) * 100))]
g = Grid("table", [X0, XL, XR, X1], hs)
head_light = frame("#D7D7D7", top="strong", left="soft", right="soft")
g.put(X0, XL, 0, 1, [line1(100, 110, 138, 142)], head_light)
g.put(XL, XR, 0, 1, [line1(315, 320, 138, 142)], frame("#808080", top="strong", left="soft", right="soft"),
      color=WHITE)
g.put(XR, X1, 0, 1, [line1(525, 530, 138, 142)], head_light)
end = frame(bottom="dot")
for k in range(8):
    lo, hi = bounds[k], bounds[k + 1]
    r = 1 + 2 * k
    issue = lines_in(55, 190, lo, hi)
    details = [l for l in lines_in(190, 515, lo, hi) if l["bbox"][0] < 205]
    results = [l for l in lines_in(190, 515, lo, hi) if l["bbox"][0] >= 205]
    ref = line1(520, 550, lo, hi)
    assert issue and details and results, k
    g.put(X0, XL, r, r + 2, para_lines(issue, 59.7, 3.0), end, align="LEFT", line=1650)
    g.put(XL, XR, r, r + 1, para_lines(details, 194.3), frame("#EBEBEB", left="soft", right="soft"),
          align="LEFT", line=1650 if len(details) < 4 else 1640)
    g.put(XL, XR, r + 1, r + 2, [[("▣ ", r_[0][1], True, INK)] + r_ for r_ in (runs_of(l) for l in results)],
          frame("#D1D1D1", left="soft", right="soft", bottom="dot"), align="LEFT", line=1400)
    g.put(XR, X1, r, r + 2, [ref], end)
block(g, 134.8)

g = Grid("note", [X0, X1], [1500])
g.put(X0, X1, 0, 1, [line1(55, 60, 788, 795)], align="LEFT", line=1250)
block(g, 788.5)

kit.finish(target, end=805.0)
