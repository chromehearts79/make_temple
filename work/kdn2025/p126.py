"""Rebuild KDN 2025 report page 126 (3rd PDF local page 26, printed page 86) as editable HWPX.

Usage: python3 work/kdn2025/p126.py <report3.pdf> <out.hwpx> [--page 26]

조직 및 인적자원관리, section 3 "조직개편 방향성(H.O.T)과 연계한 실행력 중심의 직무운영과 인력 운영 고도화"
(가. 직무관리 / 나. 인력배치 / 다. 인력운영). Built with the shared kit (one flat table per band on a
grid of PDF x and y edges). All words come from the PDF text layer.

Images and how they are kept:
- PART box, section number band, footer logo (typed "한전KDN㈜"): typed cells / text.
- heavy arrows (➡) before the 추진배경 directions -> '→' runs (가./나.: the directions keep their own
  column; 다.: one paragraph per line, as the two directions start at different x).
- gray chevrons between boxes -> ▶ ◀ ▲ ▼ connector cells; the down-pointing label shapes of 가.
  (문제점 / 개선실적 / 주요성과) -> graded gray label cells.
- boxed step numbers 1-4 of 다. -> small outlined number cells; circled ①②③ before the three
  results of 다. -> ①②③ runs.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kit  # noqa: E402
from kit import Layout, recipe_inputs  # noqa: E402

source, target = recipe_inputs(26, "조직개편 방향성(H.O.T)과 연계한 실행력 중심의")
L = Layout(top=3100)
kit.setup(source, L)
from kit import *  # noqa: E402,F401,F403  helpers and presets bound to this page

DARK, LABEL, HEAD = "#6A6A6A", "#E3E3E3", "#DCDCDC"
BOX = frame(WHITE, top="soft", bottom="soft", left="soft", right="soft")


def S(text, size=1090, bold=False, color=INK):
    return (text, size, bold, color)


def band(name, xs, ys):
    g = Grid(name, xs, [int(round((b - a) * 100)) for a, b in zip(ys, ys[1:])])
    g.ys = ys
    return g


def P(g, x0, x1, y0, y1, content, fill="1", pad=None, **kw):
    if pad is not None and kw.get("fit", True) and isinstance(content, list) and content:
        inner = ((x1 - x0) * 100 - 2 * pad - 60) / 100
        ratio = kw.pop("ratio", 90)
        for runs in content:
            need = text_width(runs, ratio)
            if need > inner:
                ratio = int(ratio * inner / need)
        kw.update(fit=False, ratio=ratio)
    g.put(x0, x1, g.ys.index(y0), g.ys.index(y1), content, fill, **kw)
    if pad is not None:
        key = (g.ys.index(y0), g.xs.index(to_x(x0)))
        item = g.items[key]
        g.items[key] = (*item[:7], dict(left=pad, right=pad, top=20, bottom=20))


def indent(line, base):
    runs = runs_of(line)
    n = round((line["bbox"][0] - base) / (0.29 * runs[0][1] / 100))
    return [S(" " * n, runs[0][1])] + runs if n > 0 else runs


def pill_heading(name, top, y):
    num, line = line1(55, 60, y - 1, y + 2), line1(85, 90, y - 1, y + 2)
    g = Grid(name, [X0, 78.0, 133.0, X1], [1650])
    g.put(X0, 78.0, 0, 1, [num], align="LEFT", line=1450)
    g.put(78.0, 133.0, 0, 1, [runs_of(line, x1=130)], frame(LABEL), line=1250)
    g.put(133.0, X1, 0, 1, [strip_runs(runs_of(line, x0=132))], align="LEFT", line=1450)
    block(g, top)


def background(name, top, height, label_y, rows, split=None):
    """추진배경: gray label, outlined body; rows = [(issue line, direction line)]."""
    xs = [X0, 111.7, 115.0] + ([split] if split else []) + [X1]
    g = Grid(name, xs, [height])
    g.put(X0, 111.7, 0, 1, [line1(65, 70, label_y - 1, label_y + 2)], frame("#DCDCDC"))
    arrow = S("→ ", 1090, True)
    if split:
        g.put(115.0, split, 0, 1, [runs_of(a) for a, _ in rows], frame(top="mid", bottom="mid", left="mid"),
              align="LEFT", line=1400)
        g.put(split, X1, 0, 1, [[arrow] + runs_of(b) for _, b in rows], frame(top="mid", bottom="mid", right="mid"),
              align="LEFT", line=1400)
    else:
        g.put(115.0, X1, 0, 1, [runs_of(a) + [S(" "), arrow] + runs_of(b) for a, b in rows],
              frame(top="mid", bottom="mid", left="mid", right="mid"), align="LEFT", line=1400)
    block(g, top)


def pairs(y_list):
    out = []
    for y in y_list:
        parts = sorted(lines_in(115, X1, y - 1, y + 2), key=lambda l: l["bbox"][0])
        assert len(parts) == 2, [p["text"] for p in parts]
        out.append(tuple(parts))
    return out


def result(name, top, y, height=1710):
    g = Grid(name, [X0, 111.7, 114.5, X1], [height])
    g.put(X0, 111.7, 0, 1, [runs_of(line1(65, 70, y - 1, y + 2), WHITE)], frame(DARK))
    g.put(114.5, X1, 0, 1, lines_in(115, 120, y - 1, y + 2), frame(top="mid", bottom="mid", left="mid", right="mid"),
          align="LEFT", line=1300)
    block(g, top)


# ---------------------------------------------------------------------------
# Page chrome (even page): PART label at the left of a rule; footer at the left.
# ---------------------------------------------------------------------------
foot = [(line1(55, 60, 815, 822)["text"], 1090, False, INK), ("   ", 1090, False, INK),
        ("한전KDN㈜", 1090, True, INK)]   # the logo is an image; its name is typed
L.add_table([[cell(0, W, 1500, [para(foot, "LEFT", 1300)[0]])]], floating=(5660, 81550))

g = Grid("part-head", [X0, 103.0, 158.5, X1], [1500])
g.put(X0, 103.0, 0, 1, [[("PART ", 800, False), ("01", 1300, True)]], line=1300)
g.put(103.0, 158.5, 0, 1, "경영관리", frame("#333333"), size=1080, bold=True, color=WHITE)
g.put(158.5, X1, 0, 1, [], frame(bottom="soft"))
block(g, 32.0)

g = Grid("sec3", [X0, 84.5, X1], [2300])
g.put(X0, 84.5, 0, 1, [runs_of(line1(60, 70, 72, 77), WHITE)], frame(DARK), line=1700)
g.put(84.5, X1, 0, 1, [line1(90, 95, 73, 78)], frame("#E6E6E6"), align="LEFT", line=1700)
block(g, 70.9)

# Process: three boxes (white head, gray body) joined by chevrons.
boxes = ((X0, 205.5, 62.5), (219.0, 379.3, 225.1), (393.0, X1, 398.9))
g = Grid("process", [X0, 205.5, 219.0, 379.3, 393.0, X1], [1800, 3850])
for k, (a, e, base) in enumerate(boxes):
    g.put(a, e, 0, 1, lines_in(a, e, 103, 107), frame(top="mid", left="mid", right="mid", bottom="soft"), line=1250)
    g.put(a, e, 1, 2, [indent(l, base) for l in lines_in(a, e, 123, 152)],
          frame("#EBEBEB", left="mid", right="mid", bottom="mid"), align="LEFT", line=1330)
    if k < 2:
        g.put(e, boxes[k + 1][0], 1, 2, "▶", size=1300, color="#BDBDBD", fit=False)
block(g, 99.5)

# ---------------------------------------------------------------------------
# 가. 직무관리
# ---------------------------------------------------------------------------
pill_heading("title-ga", 165.0, 166.1)
background("bg-ga", 188.6, 3000, 198.0, pairs((190.9, 205.2)), split=370.0)

xs = [X0, 102.3, 104.5, 328.0, 331.5, X1]
ys = [226.0, 243.5, 279.5, 315.0, 352.0]
g = band("table-ga", xs, ys)
for a, e, x in ((104.5, 328.0, 150), (331.5, X1, 409)):
    P(g, a, e, 226.0, 243.5, [line1(x - 1, x + 2, 229, 232)], frame(HEAD, top="mid", left="mid", right="mid",
                                                                    bottom="soft"))
rows = ((243.5, 279.5, "#E8E8E8", (256.1,), (249, 266), dict(bottom="dot")),
        (279.5, 315.0, "#D3D3D3", (296.8,), (284, 301), dict(bottom="dot")),
        (315.0, 352.0, "#BEBEBE", (333.2,), (317, 337), dict(bottom="mid")))
for y0, y1, fill, (ly,), (cy0, cy1), edge in rows:
    P(g, X0, 102.3, y0, y1, [line1(58, 70, ly - 1, ly + 2)], frame(fill))
    P(g, 104.5, 328.0, y0, y1, lines_in(105, 112, cy0, cy1), frame(left="mid", right="mid", **edge), align="LEFT",
      line=1430)
    P(g, 331.5, X1, y0, y1, lines_in(333, 340, cy0, cy1), frame(left="mid", right="mid", **edge), align="LEFT",
      line=1430)
block(g, 226.0)

# ---------------------------------------------------------------------------
# 나. 인력배치
# ---------------------------------------------------------------------------
pill_heading("title-na", 359.5, 360.6)
background("bg-na", 383.0, 3000, 392.5, pairs((385.3, 399.6)), split=355.5)

xs = [X0, 113.6, 116.5, 120.4, 222.5, 257.1, 261.0, 275.0, 278.4, 335.8, X1]
ys = [420.0, 439.5, 458.5, 471.0, 477.0, 495.5, 502.0, 514.0, 533.0, 536.0]
g = band("table-na", xs, ys)
P(g, X0, 113.6, 420.0, 536.0, [line1(65, 70, 473, 476)], frame(LABEL))
P(g, 116.5, 261.0, 420.0, 439.5, [line1(137, 140, 424, 427)], frame(HEAD, top="mid", left="mid", right="mid"))
P(g, 275.0, X1, 420.0, 439.5, [line1(293, 296, 424, 427)], frame(HEAD, top="mid", left="mid", right="mid"))
left_rows = ((439.5, 458.5, 444.4), (458.5, 477.0, 462.8), (477.0, 495.5, 481.2), (495.5, 514.0, 499.6))
for y0, y1, ty in left_rows:
    P(g, 116.5, 120.4, y0, y1, [], frame(left="mid"))
    P(g, 120.4, 222.5, y0, y1, [line1(120, 222, ty - 1, ty + 2)], frame("#E3E3E3", bottom="dot"))
    P(g, 222.5, 257.1, y0, y1, [line1(225, 240, ty - 1, ty + 2)], frame(bottom="dot"), align="RIGHT")
    P(g, 257.1, 261.0, y0, y1, [], frame(right="mid"))
P(g, 116.5, 120.4, 514.0, 536.0, [], frame(left="mid", bottom="mid"))
P(g, 120.4, 222.5, 514.0, 533.0, [line1(130, 140, 517, 520)], frame("#E3E3E3", top="mid", bottom="mid", left="mid"))
P(g, 222.5, 257.1, 514.0, 533.0, [line1(225, 230, 517, 520)], frame(top="mid", bottom="mid", right="mid"),
  align="RIGHT")
P(g, 120.4, 257.1, 533.0, 536.0, [], frame(bottom="mid"))
P(g, 257.1, 261.0, 514.0, 536.0, [], frame(right="mid", bottom="mid"))
P(g, 261.0, 275.0, 458.5, 514.0, "▶", size=1300, color="#BDBDBD", fit=False)
right_rows = ((439.5, 471.0, frame("#E6E6E6", hatch="#D4D4D4"), INK, (443, 470)),
              (471.0, 502.0, frame("#5E5E5E"), WHITE, (473, 500)),
              (502.0, 533.0, frame("#9A9A9A"), WHITE, (504, 532)))
for k, (y0, y1, fill, color, (cy0, cy1)) in enumerate(right_rows):
    edge = dict(bottom="dot") if k < 2 else {}
    P(g, 275.0, 278.4, y0, y1, [], frame(left="mid"))
    P(g, 278.4, 335.8, y0, y1, [runs_of(l, color) for l in lines_in(280, 330, cy0, cy1)], fill, line=1210)
    P(g, 335.8, X1, y0, y1, lines_in(337, 340, cy0, cy1), frame(right="mid", **edge), align="LEFT", line=1320)
P(g, 275.0, X1, 533.0, 536.0, [], frame(bottom="mid", left="mid", right="mid"))
block(g, 420.0)

result("result-na", 543.0, 546.2)

# ---------------------------------------------------------------------------
# 다. 인력운영
# ---------------------------------------------------------------------------
pill_heading("title-da", 571.3, 572.4)
background("bg-da", 594.8, 3000, 604.3, pairs((597.1, 611.5)))

xs = [X0, 113.6, 117.0, 120.4, 122.5, 131.0, 137.5, 146.5, 222.5, 233.8, 236.0, 244.5, 336.0, 340.0, 343.0,
      345.7, 368.5, X1]
ys = [632.0, 651.0, 653.5, 671.0, 678.5, 705.5, 719.5, 732.0, 737.0, 772.0, 776.0]
g = band("table-da", xs, ys)
P(g, X0, 113.6, 632.0, 776.0, [line1(65, 70, 698, 702)], frame(LABEL))
P(g, 117.0, 340.0, 632.0, 651.0, [line1(124, 127, 635, 638)], frame(HEAD, top="mid", left="mid", right="mid"))
P(g, 343.0, X1, 632.0, 651.0, [line1(357, 360, 635, 638)], frame(HEAD, top="mid", left="mid", right="mid"))
P(g, 117.0, 120.4, 651.0, 776.0, [], frame(left="mid", bottom="mid"))
P(g, 336.0, 340.0, 651.0, 776.0, [], frame(right="mid", bottom="mid"))
P(g, 120.4, 336.0, 772.0, 776.0, [], frame(bottom="mid"))


def step(x0, n0, n1, x1, y0, y1, num, head_y, body, fill, color, base):
    """Step box: gray head with an outlined number cell, outlined body with bullet lines."""
    head = line1(n1, x1, head_y - 1, head_y + 2)
    P(g, x0, n0, y0, y1, [], frame(fill, top="soft", left="soft"))
    P(g, n0, n1, y0, y1, [[S(num, 900, True)]], BOX, line=950, pad=0, fit=False)
    P(g, n1, x1, y0, y1, [runs_of(head, color)], frame(fill, top="soft", right="soft"), align="LEFT", line=1150)
    yb0, yb1 = (671.0, 705.5) if y0 < 700 else (737.0, 772.0)
    P(g, x0, x1, yb0, yb1, [indent(l, base) for l in lines_in(x0 + 2, x1, body[0], body[1])],
      frame(left="soft", right="soft", bottom="soft"), align="LEFT", line=1430)


step(120.4, 137.5, 146.5, 222.5, 653.5, 671.0, "1", 657.3, (674, 702), "#DCDCDC", INK, 126.2)
step(233.8, 236.0, 244.5, 336.0, 653.5, 671.0, "2", 657.3, (674, 702), "#8C8C8C", WHITE, 239.7)
step(120.4, 122.5, 131.0, 222.5, 719.5, 737.0, "4", 723.0, (739, 768), "#DCDCDC", INK, 126.2)
step(233.8, 236.0, 244.5, 336.0, 719.5, 737.0, "3", 723.0, (739, 768), "#DCDCDC", INK, 239.7)
P(g, 222.5, 233.8, 671.0, 705.5, "▶", size=1100, color="#BDBDBD", fit=False)
P(g, 233.8, 336.0, 705.5, 719.5, "▼", size=1000, color="#BDBDBD", line=1000)
P(g, 120.4, 222.5, 705.5, 719.5, "▲", size=1000, color="#BDBDBD", line=1000)
P(g, 222.5, 233.8, 737.0, 772.0, "◀", size=1100, color="#BDBDBD", fit=False)
# right: labelled rows and the hatched results box
P(g, 343.0, 345.7, 651.0, 776.0, [], frame(left="mid", bottom="mid"))
for k, (y0, y1, (ly0, ly1), (cy0, cy1)) in enumerate(((651.0, 678.5, (653, 667), (653, 667)),
                                                       (678.5, 705.5, (680, 694), (680, 694)),
                                                       (705.5, 732.0, (707, 721), (706, 720)))):
    P(g, 345.7, 368.5, y0, y1, lines_in(347, 350, ly0, ly1), frame("#E3E3E3", bottom="dot"), line=1100)
    P(g, 368.5, X1, y0, y1, lines_in(370, 373, cy0, cy1), frame(right="mid", bottom="dot"), align="LEFT", line=1100)
nums = ("①", "②", "③")
results = [[S(n + " ", 990, True)] + runs_of(l) for n, l in zip(nums, lines_in(360, 365, 731, 760))]
P(g, 345.7, X1, 732.0, 772.0, results, frame("#EEEEEE", right="mid", hatch="#DCDCDC"), align="LEFT", line=1200)
P(g, 345.7, X1, 772.0, 776.0, [], frame(right="mid", bottom="mid"))
block(g, 632.0)

result("result-da", 781.5, 784.9)

kit.finish(target, end=801.0)
