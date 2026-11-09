"""Rebuild KDN 2025 report physical PDF page 20 (printed page 8) as editable HWPX.

Usage: python3 work/kdn2025/p20.py <report.pdf> <out.hwpx> [--page N]

Dense diagram page "2 ‘2035 New Vision’ 실현을 위한 전략체계 혁신과 미래성장기반 구축".
Built with the shared kit: one flat table per band on a union grid. Bands whose source
columns do not share row edges (the goal table and its right-hand rationale column) use
y-edge lists, so every cell spans the PDF rows it covers. All text comes from the PDF
text layer; only the glyph-like images are typed: the black circled numbers (as ① ...),
the "+" and chevron connectors, the boxed 1/2/3 (as ① ② ③), the ① ② ③ of the right-hand
pills, the "지적사항 개선" tag and the PART label / logo of the page chrome.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kit  # noqa: E402
from kit import Layout, recipe_inputs  # noqa: E402

source, target = recipe_inputs(20, "실현을 위한 전략체계 혁신과 미래성장기반 구축")
L = Layout(top=3100)
kit.setup(source, L)
from kit import *  # noqa: E402,F401,F403  helpers and presets bound to this page

GREY = "#808080"
NUM = "①②③④⑤⑥"


def ygrid(name, xs, ys):
    """Grid whose rows are given as PDF y edges (pt)."""
    g = Grid(name, xs, [int(round((b - a) * 100)) for a, b in zip(ys, ys[1:])])
    g.ys = list(ys)
    return g


def yput(g, x0, x1, y0, y1, content, fill="1", **kw):
    def row(y):
        k = min(range(len(g.ys)), key=lambda i: abs(g.ys[i] - y))
        if abs(g.ys[k] - y) > 0.01:
            raise ValueError(f"{g.name}: y {y} is not a row edge")
        return k
    g.put(x0, x1, row(y0), row(y1), content, fill, **kw)


def indent(runs, pad="  "):
    runs = list(runs)
    runs[0] = (pad + runs[0][0], *runs[0][1:])
    return runs


# ---------------------------------------------------------------------------
# Page chrome (even page): PART label at the left of the running rule, footer at the left.
# ---------------------------------------------------------------------------
foot = [(line1(55, 60, 815, 822)["text"], 1090, False, INK), ("     ", 1090, False, INK),
        ("한전KDN㈜", 1090, True, "#5A5A5A")]
L.add_table([[cell(0, W, 1500, [para(foot, "LEFT", 1300)[0]])]], floating=(5660, 81550))

g = Grid("head", [X0, 102.6, 158.0, 160.0, X1], [1600])
g.put(X0, 102.6, 0, 1, [[("PART ", 900, False, INK), ("01", 1400, True, "#7A7A7A")]], frame("#F2F2F2", top="soft"),
      line=1400)
g.put(102.6, 158.0, 0, 1, "경영관리", frame("#333333"), size=1150, bold=True, color=WHITE)
g.put(160.0, X1, 0, 1, [], frame(bottom="soft"))
block(g, 31.0)

# 2 section heading
g = Grid("section-2", [X0, 85.5, 88.5, X1], [2300])
g.put(X0, 85.5, 0, 1, [line1(60, 70, 72, 76)], frame("#6E6E6E"), color=WHITE, line=1900)
g.put(88.5, X1, 0, 1, [line1(90, 95, 72, 77)], frame("#E6E6E6"), align="LEFT", line=1750)
block(g, 70.8)

# 가. title: "가." and "[방향성] title" are two PDF lines.
runs = runs_of(line1(85, 90, 98, 102))
g = Grid("title-ga", [X0, 77.0, 114.6, X1], [1700])
g.put(X0, 77.0, 0, 1, [line1(55, 60, 98, 102)], align="LEFT", line=1450)
g.put(77.0, 114.6, 0, 1, [runs[:1]], pill)
g.put(114.6, X1, 0, 1, [strip_runs(runs[1:])], align="LEFT", line=1450)
block(g, 98.5)

# ---------------------------------------------------------------------------
# Governance: dark band and three stakeholder boxes joined by "+".
# ---------------------------------------------------------------------------
xs = [X0, 102.0, 213.0, 228.0, 383.0, 399.0, 510.0, X1]
g = ygrid("governance", xs, [121.5, 138.0, 142.5, 162.5, 208.5])
yput(g, X0, 102.0, 121.5, 138.0, [], frame(top="soft"))
yput(g, 102.0, 510.0, 121.5, 138.0, [line1(125, 135, 122, 128)], frame("#5E5E5E", top="soft"), color=WHITE,
     line=1350)
yput(g, 510.0, X1, 121.5, 138.0, [], frame(top="soft"))
for a, e, x in ((X0, 213.0, 90), (228.0, 383.0, 233), (399.0, X1, 408)):
    yput(g, a, e, 142.5, 162.5, [line1(x - 1, x + 1, 145, 150)], frame(top="mid", left="mid", right="mid",
                                                                   bottom="soft"), bold=True, line=1300)
    yput(g, a, e, 162.5, 208.5, lines_in(a + 2, a + 12, 165, 200), frame("#EBEBEB", left="mid", right="mid",
                                                                         bottom="mid"), align="LEFT", line=1320)
for a, e in ((213.0, 228.0), (383.0, 399.0)):
    yput(g, a, e, 162.5, 208.5, "+", size=1700, bold=True, color="#9A9A9A", fit=False)
block(g, 121.5)

# ---------------------------------------------------------------------------
# Environment analysis -> 시사점 -> 비전연계 경영목표 도출
# ---------------------------------------------------------------------------
xs = [X0, 78.0, 108.5, 112.0, 121.0, 124.5, 137.5, 146.0, 156.0, 159.5, 182.0, 255.5, 259.0, 262.0, 283.5,
      404.0, 407.5, 417.0, 439.5, X1]
ys = [214.0, 216.5, 230.7, 244.9, 259.1, 262.5, 276.7, 290.9, 305.1, 315.5, 356.0, 372.5, 392.5, 414.0, 418.5,
      440.5]
g = ygrid("environment", xs, ys)
label = frame("#E3E3E3")
yput(g, X0, 78.0, 214.0, 315.5, lines_in(60, 75, 236, 290), label, bold=True, line=1320)
yput(g, 78.0, 108.5, 214.0, 262.5, lines_in(80, 90, 225, 245), frame("#E3E3E3", bottom="soft"), line=1320)
yput(g, 78.0, 108.5, 262.5, 315.5, lines_in(80, 90, 274, 295), label, line=1320)
items = [(216.5, 230.7, 219), (230.7, 244.9, 233), (244.9, 259.1, 247),
         (262.5, 276.7, 266), (276.7, 290.9, 280), (290.9, 305.1, 294)]
for k, (y0, y1, y) in enumerate(items):
    edge = dict(bottom="soft") if k not in (2, 5) else {}
    yput(g, 112.0, 156.0, y0, y1, [[(NUM[k] + " ", 1090, True, INK)] + runs_of(line1(127, 130, y, y + 3))],
         frame("#EBEBEB", hatch="#DCDCDC", **edge), line=1250)
    yput(g, 159.5, X1, y0, y1, [line1(160, 162, y, y + 3)], frame(**edge), align="LEFT", line=1250)
yput(g, 112.0, X1, 305.1, 315.5, "▼", size=1000, color="#5A5A5A", line=860, fit=False)
# 시사점: the black circled numbers and the circled arrow are images; the brackets are text.
yput(g, X0, 112.0, 315.5, 356.0, [line1(65, 70, 336, 340)], frame("#CFCFCF"), bold=True)
groups = [("①,②,③,⑥", 185, 136), ("②,④,⑥", 325, 270), ("②,⑤,⑥", 473, 422)]
for (nums, x, x2), (a, e) in zip(groups, ((112.0, 259.0), (259.0, 407.5), (407.5, X1))):
    first = [(f"[{nums}] → ", 1090, True, INK)] + runs_of(line1(x - 1, x + 1, 325, 330))
    yput(g, a, e, 315.5, 356.0, [first, line1(x2 - 1, x2 + 1, 339, 344)],
         frame("#E2E2E2", right="soft" if a < 400 else None), line=1350)
yput(g, 112.0, X1, 356.0, 372.5, "▼", size=1300, color="#C4C4C4", line=1300, fit=False)
yput(g, X0, 108.5, 372.5, 440.5, lines_in(60, 65, 388, 420), frame("#BDBDBD"), bold=True, line=1320)
boxes = [(112.0, 124.5, 146.0, 255.5, 164, 127), (259.0, 262.0, 283.5, 404.0, 302, 264),
         (407.5, 417.0, 439.5, X1, 452, 420)]
for k, (a, t0, t1, e, hx, tx) in enumerate(boxes):
    yput(g, a, e, 372.5, 392.5, [[(NUM[k] + " ", 1090, True, INK)] + runs_of(line1(hx - 1, hx + 1, 378, 382))],
         frame(top="mid", left="mid", right="mid"), line=1300)
    line = line1(tx - 1, tx + 1, 398, 402)
    yput(g, a, t0, 392.5, 414.0, [], frame("#E6E6E6", left="mid", bottom="mid"))
    yput(g, t0, t1, 392.5, 414.0, [runs_of(line, x1=tx + 5)], frame(WHITE, top="soft", bottom="soft", left="soft",
                                                                       right="soft"), line=1000)
    yput(g, t1, e, 392.5, 414.0, [strip_runs(runs_of(line, x0=tx + 5))], frame("#E6E6E6", right="mid",
                                                                              bottom="mid"), align="LEFT")
band = line1(140, 142, 424, 428)
hatch = frame("#E9E9E9", hatch="#D8D8D8")
yput(g, 112.0, 121.0, 418.5, 440.5, "▶", hatch, size=1000, color="#9A9A9A", fit=False)
yput(g, 121.0, 137.5, 418.5, 440.5, [], hatch)
yput(g, 137.5, 182.0, 418.5, 440.5, [runs_of(band, x1=180)], frame(WHITE, top="soft", bottom="soft",
                                                                    left="soft", right="soft"), line=1000)
yput(g, 182.0, X1, 418.5, 440.5, [strip_runs(runs_of(band, x0=180))], hatch, align="LEFT")
block(g, 214.0)

# 나. title with the "지적사항 개선" tag (image).
runs = runs_of(line1(85, 90, 452, 456))
g = Grid("title-na", [X0, 77.0, 133.0, 502.0, X1], [1700])
g.put(X0, 77.0, 0, 1, [line1(55, 60, 452, 456)], align="LEFT", line=1450)
g.put(77.0, 133.0, 0, 1, [runs[:1]], pill)
g.put(133.0, 502.0, 0, 1, [strip_runs(runs[1:])], align="LEFT", line=1450)
g.put(502.0, X1, 0, 1, "지적사항 개선", frame("#4A4A4A"), size=820, bold=True, color=WHITE, line=1000)
block(g, 451.5)

# 주요 개선사항: two outlined boxes with a tag, a bold arrow line and a note line.
xs = [X0, 105.0, 108.0, 110.0, 150.0, 327.0, 333.0, 350.0, 391.0, X1]
g = Grid("improvements", xs, [1700, 1750])
g.put(X0, 105.0, 0, 2, [line1(65, 75, 478, 482), line1(60, 65, 490, 494)], frame("#EDEDED", top="mid"),
      bold=True, line=1300)
for a, t0, t1, e, x, nx in ((108.0, 110.0, 150.0, 327.0, 121, 112), (333.0, 350.0, 391.0, X1, 355, 337)):
    line = line1(x - 1, x + 1, 478, 482)
    g.put(a, t0, 0, 1, [], frame(top="soft", left="soft"))
    g.put(t0, t1, 0, 1, [runs_of(line, x1=x + 25)], frame(WHITE, top="soft", bottom="soft", left="soft",
                                                         right="soft"), line=1000)
    g.put(t1, e, 0, 1, [strip_runs(runs_of(line, x0=x + 25))], frame(top="soft", right="soft"), align="LEFT")
    g.put(a, e, 1, 2, [line1(nx - 1, nx + 1, 491, 495)], frame(bottom="soft", left="soft", right="soft"))
block(g, 474.0)

# ---------------------------------------------------------------------------
# Goal table (left) and rationale column (right) on one y-edge grid.
# ---------------------------------------------------------------------------
V = [(209.6, 239.5), (239.5, 269.4), (269.4, 299.2), (299.2, 329.0)]
xs = [X0, 100.0, 138.0, 186.0, 209.6, 239.5, 269.4, 299.2, 329.0, 331.0, 341.0, 385.0, 393.0, 412.0, X1]
rows_y = [546.5, 572.0, 590.0, 607.5, 625.0, 643.0, 660.0, 678.0, 695.5, 713.0, 731.0, 749.0, 766.0, 784.0, 801.5]
extra = [604.5, 619.0, 703.0, 726.0, 763.0, 776.0, 647.0, 682.0, 717.5, 753.0, 788.0]
ys = sorted(set([511.5, 529.3] + rows_y + extra))
g = ygrid("goal-table", xs, ys)

head = frame("#D9D9D9", top="strong", bottom="soft")
yput(g, X0, 209.6, 511.5, 546.5, [line1(85, 90, 522, 526)], head, bold=True)
dark25 = frame("#6A6A6A", top="strong", left="strong", right="strong", bottom="soft")
yput(g, 209.6, 269.4, 511.5, 529.3, [line1(225, 230, 511, 515)], dark25, color=WHITE, line=1250)
yput(g, 209.6, 239.5, 529.3, 546.5, [line1(214, 216, 530, 534)], frame("#6A6A6A", left="strong", bottom="soft"),
     color=WHITE, line=1250)
yput(g, 239.5, 269.4, 529.3, 546.5, [line1(244, 246, 530, 534)], frame("#6A6A6A", right="strong", bottom="soft"),
     color=WHITE, line=1250)
for a, e, x in ((269.4, 299.2, 272), (299.2, 329.0, 301)):
    yput(g, a, e, 511.5, 546.5, lines_in(x - 1, x + 4, 512, 535), head, bold=True, line=1500)
yput(g, 331.0, X1, 511.5, 546.5, [line1(375, 380, 522, 526)], head, bold=True)

name = frame("#EFEFEF", bottom="soft", right="soft")
cat = frame("#E3E3E3", bottom="soft", right="soft")


def value_cells(y0, y1, values):
    for k, ((a, e), v) in enumerate(zip(V, values)):
        edge = dict(left="strong") if k == 0 else dict(right="strong") if k == 1 else {}
        if y1 == 801.5 and k < 2:
            edge["bottom"] = "strong"
        else:
            edge.setdefault("bottom", "soft")
        yput(g, a, e, y0, y1, v, frame(**edge), line=1050)


def plain_row(y0, y1, ny, span_name=(100.0, 186.0)):
    """Name, unit and four values, each its own PDF line."""
    a, e = span_name
    yput(g, a, e, y0, y1, [line1(a, e, ny - 1, ny + 3)], name, line=1050)
    yput(g, 186.0, 209.6, y0, y1, [line1(186, 209.6, ny - 1, ny + 3)], name, line=1050)
    value_cells(y0, y1, [[line1(a0, e0, ny - 1, ny + 3)] for a0, e0 in V])


plain_row(546.5, 572.0, 554, (X0, 186.0))
yput(g, X0, 100.0, 572.0, 590.0, [line1(58, 60, 575, 578)], cat, bold=True, line=1050)
plain_row(572.0, 590.0, 576)
yput(g, X0, 100.0, 590.0, 625.0, [line1(58, 60, 601, 604)], cat, bold=True, line=1050)
plain_row(590.0, 607.5, 593.5)
plain_row(607.5, 625.0, 611)
yput(g, X0, 100.0, 625.0, 731.0, [line1(60, 64, 672, 675)], cat, bold=True, line=1050)
yput(g, X0, 100.0, 731.0, 801.5, [line1(58, 60, 760, 763)], frame("#E3E3E3", bottom="strong", right="soft"),
     bold=True, line=1050)
# Sub-categories with their 복합지표 chip; the indicator rows beside them.
groups = [(625.0, 647.0, 660.0, 626, 649), (660.0, 682.0, 695.5, 662, 683), (695.5, 717.5, 731.0, 697, 718),
          (731.0, 753.0, 766.0, 732, 754), (766.0, 788.0, 801.5, 768, 789)]
for y0, ym, y1, ny, cy in groups:
    yput(g, 100.0, 138.0, y0, ym, lines_in(99, 110, ny, ny + 15), frame("#EFEFEF", right="soft"), line=980)
    last = y1 == 801.5
    yput(g, 100.0, 138.0, ym, y1, [line1(100, 110, cy - 1, cy + 2)],
         frame(WHITE, top="soft", left="soft", right="soft", bottom="strong" if last else "soft"), line=950)
plain_row(625.0, 643.0, 629, (138.0, 186.0))
plain_row(643.0, 660.0, 646.5, (138.0, 186.0))
plain_row(660.0, 678.0, 664.5, (138.0, 186.0))


def combined_row(y0, y1, ny):
    """Name, unit and all four values are one PDF line here: split it by span and by value."""
    line = line1(138.0, 186.0, ny - 1, ny + 3)
    yput(g, 138.0, 186.0, y0, y1, [runs_of(line, x1=186.0)], name, line=1050)
    yput(g, 186.0, 209.6, y0, y1, [runs_of(line, x0=186.0, x1=209.0)], name, line=1050)
    text = line["spans"][-1]["text"]
    values = re.findall(r"최우수|\d월 결과", text)
    assert "".join(values) == text, values
    value_cells(y0, y1, [[(v, 890, False, INK)] for v in values])


combined_row(678.0, 695.5, 681.4)
plain_row(695.5, 713.0, 699.5, (138.0, 186.0))
combined_row(713.0, 731.0, 716.7)


def run_pair_row(y0, y1, ny):
    """Name and unit share one PDF line; values are separate lines."""
    line = line1(138.0, 186.0, ny - 1, ny + 3)
    yput(g, 138.0, 186.0, y0, y1, [runs_of(line, x1=186.0)], name, line=1050)
    yput(g, 186.0, 209.6, y0, y1, [runs_of(line, x0=186.0)], name, line=1050)
    value_cells(y0, y1, [[line1(a0, e0, ny - 1, ny + 3)] for a0, e0 in V])


run_pair_row(731.0, 749.0, 734.7)
plain_row(749.0, 766.0, 752.5, (138.0, 186.0))
plain_row(766.0, 784.0, 770.0, (138.0, 186.0))
run_pair_row(784.0, 801.5, 788.0)

# Right-hand rationale column.
plain = frame()
band_fill = frame("#DCDCDC")
l1, l2 = lines_in(331, 345, 546, 570)
yput(g, 331.0, X1, 546.5, 572.0, [l1, indent(runs_of(l2))], plain, align="LEFT", line=1050)
for k, (y0, y1, py, ty, tx) in enumerate(((572.0, 590.0, 576, 575, 393), (643.0, 660.0, 650, 649, 383),
                                          (731.0, 749.0, 735, 734, 392))):
    yput(g, 331.0, 385.0, y0, y1, [[(NUM[k] + " ", 1090, True, INK)] + runs_of(line1(346, 348, py - 1, py + 2))],
         frame(top="soft", bottom="soft", left="soft", right="soft"), line=1200)
    yput(g, 385.0, X1, y0, y1, [line1(tx - 1, tx + 1, ty - 1, ty + 2)], frame(top="soft"), align="LEFT",
         line=1250)
for y0, y1, ly, cut, end in ((590.0, 604.5, 592, 411.0, 412.0), (660.0, 678.0, 665.5, 411.0, 412.0),
                             (749.0, 763.0, 750.5, 391.0, 393.0)):
    line = line1(343, 345, ly - 1, ly + 2)
    yput(g, 331.0, 341.0, y0, y1, "▶", size=800, color="#333333", fit=False, line=900)
    yput(g, 341.0, end, y0, y1, [runs_of(line, x1=cut)], frame(top="soft", bottom="soft", left="soft",
                                                              right="soft"), line=950)
    yput(g, end, X1, y0, y1, [strip_runs(runs_of(line, x0=cut))], align="LEFT", line=1150)
yput(g, 331.0, X1, 604.5, 619.0, [line1(335, 337, 605, 608)], band_fill, align="LEFT", line=1100)
l1, l2 = lines_in(335, 345, 618, 632)
yput(g, 331.0, X1, 619.0, 643.0, [l1, indent(runs_of(l2))], plain, align="LEFT", line=1030)
yput(g, 331.0, X1, 678.0, 703.0, lines_in(335, 370, 679, 693), band_fill, line=1120)
l1, l2 = lines_in(335, 345, 703, 716)
yput(g, 331.0, X1, 703.0, 726.0, [l1, indent(runs_of(l2))], plain, align="LEFT", line=1030)
yput(g, 331.0, X1, 763.0, 776.0, [line1(345, 350, 764, 767)], band_fill, line=1100)
l1, l2 = lines_in(335, 345, 775, 790)
yput(g, 331.0, X1, 776.0, 801.5, [l1, indent(runs_of(l2))], frame(bottom="strong"), align="LEFT", line=1030)
block(g, 511.5)

kit.finish(target, end=803.0)
