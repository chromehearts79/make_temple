"""Rebuild KDN 2025 report page 82 (second PDF local page 32, printed page 54) as editable HWPX.

Usage: python3 work/kdn2025/p82.py <report2.pdf> <out.hwpx> [--page 32]

창업 및 경제활성화, 평가내용 03 opening page (중소기업기술마켓). Built with the shared diagram kit
(one flat table per horizontal band on a grid of PDF x edges). All text comes from the PDF text
layer. Images typed here: the PART box, the '평가내용 03' chip, the boxed task numbers
(1 2 3 -> ① ② ③) and the large decorative quote marks around the 문제점 boxes (“ ”). The italic
of the quoted complaints is not reproduced. Source oddity kept as printed: 'Fasct Track 17건'.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kit  # noqa: E402
from kit import Layout, recipe_inputs  # noqa: E402

source, target = recipe_inputs(32, "중소기업기술마켓 활성화를 위한 노력과 성과")
L = Layout(top=3100)
kit.setup(source, L)
from kit import *  # noqa: E402,F401,F403  helpers and presets bound to this page

DARK, LABEL = "#6A6A6A", "#E6E6E6"
SIDE = frame("#ECECEC", top="dot", hatch="#DDDDDD")       # hatched row labels of section 1
TAB = frame("#E6E6E6", top="soft")                          # 개선내용 / 추진실적 labels
HATCH = frame("#EEEEEE", hatch="#DEDEDE")
PILL = frame(WHITE, top="soft", bottom="soft", left="soft", right="soft")
QUOTE = "#EDEDED"


def hang(lines, base):
    """Bullet lines keep their PDF indent: spaces for the x offset and for the line's own lead."""
    out = []
    for l in lines:
        runs = runs_of(l)
        size = runs[0][1] / 100
        raw = "".join(s["text"] for s in l["spans"])
        offset = l["bbox"][0] - base + (len(raw) - len(raw.lstrip(" "))) * 0.29 * size
        n = max(0, round(offset / (0.29 * size)))
        out.append([(" " * n, runs[0][1], False, INK)] + runs if n else runs)
    return out


def tight(g, x0, r0, left=60, right=60):
    """Narrow the cell padding (kit cells use the builder default 320/180)."""
    c0 = g.xs.index(to_x(x0))
    item = g.items[r0, c0]
    g.items[r0, c0] = (*item[:7], dict(left=left, right=right))


def lead(glyph, runs, bold=False):
    runs = list(runs)
    return [(glyph + " ", runs[0][1], bold, INK)] + runs


def section_band(name, num_line, title_line, top):
    g = Grid(name, [X0, 84.5, X1], [2300])
    g.put(X0, 84.5, 0, 1, [runs_of(num_line, WHITE)], frame(DARK), line=1700)
    g.put(84.5, X1, 0, 1, [title_line], frame(LABEL), align="LEFT", line=1700)
    block(g, top)


def titled(name, line, top):
    g = Grid(name, [X0, X1], [1650])
    g.put(X0, X1, 0, 1, [line], align="LEFT", line=1450)
    block(g, top)


def complaint(name, pill_line, lines, top, hs):
    """“ rule, gray box with the dark 문제점 pill and centred quotes, rule ”."""
    g = Grid(name, [X0, 65.4, 96.4, 515.8, 547.1, X1], [900] + list(hs) + [900])
    g.put(X0, 65.4, 0, 1, "“", frame(bottom="mid"), size=1200, bold=True, color="#9A9A9A", line=700, fit=False)
    g.put(65.4, X1, 0, 1, [], frame(bottom="mid"))
    g.put(X0, 96.4, 1, 2, [runs_of(pill_line, WHITE)], frame("#5E5E5E"), line=1150)
    g.put(X0, 96.4, 2, 3, [], frame(QUOTE))
    g.put(X0, 96.4, 3, 4, [], frame(QUOTE))
    g.put(96.4, 515.8, 1, 4, lines, frame(QUOTE), line=1440)
    g.put(515.8, X1, 1, 4, [], frame(QUOTE))
    g.put(X0, 547.1, 4, 5, [], frame(top="mid"))
    g.put(547.1, X1, 4, 5, "”", frame(top="mid"), size=1200, bold=True, color="#9A9A9A", line=700, fit=False)
    block(g, top)


def improve(name, label_line, top, hs, heads, rows):
    """개선내용: label | two boxes, each a header (tag + title) and body rows."""
    xs = sorted(({X0, 99.4, 104.8, 325.3, 333.0, X1} | {x for head in heads for x in head[1:3]}
                 | {x for row in rows for item in row for x in item[:2]}) - {None})
    g = Grid(name, xs, hs)
    g.put(X0, 99.4, 0, len(hs), [label_line], TAB, bold=True)
    tight(g, X0, 0, 40, 40)
    for (a, p0, p1, e, line), body in zip(heads, ([r[0] for r in rows], [r[1] for r in rows])):
        head = frame("#DEDEDE", top="mid", left="mid", right="mid", bottom="soft")
        if p0 is None:
            g.put(a, e, 0, 1, [line], head, bold=True)
        else:
            g.put(a, p0, 0, 1, [], frame("#DEDEDE", top="mid", left="mid", bottom="soft"))
            g.put(p0, p1, 0, 1, [runs_of(line, x1=p1 - 1.5)], PILL, line=1000)
            tight(g, p0, 0, 20, 20)
            g.put(p1, e, 0, 1, [strip_runs(runs_of(line, x0=p1 - 1.5))], frame("#DEDEDE", top="mid", right="mid",
                                                                           bottom="soft"), align="LEFT")
            tight(g, p1, 0, 60, 60)
        for r, (t0, t1, content, fill, kw) in enumerate(body, 1):
            last = r == len(hs) - 1
            edge = dict(bottom="mid") if last else {}
            if t0 is None:
                g.put(a, e, r, r + 1, content, frame(left="mid", right="mid", **edge), **kw)
                continue
            g.put(a, t0, r, r + 1, [], frame(left="mid", **edge))
            g.put(t0, t1, r, r + 1, content[0], fill, line=1000, **{k: v for k, v in kw.items() if k == "color"})
            tight(g, t0, r, 20, 20)
            g.put(t1, e, r, r + 1, content[1], frame(right="mid", **edge), align="LEFT", line=1200)
            tight(g, t1, r, 60, 60)
    block(g, top)


def results(name, label_line, tags, top, hs):
    """추진실적: label | light box with two dark tag + text rows."""
    g = Grid(name, [X0, 99.3, 104.8, 107.9, 150.4, X1], hs)
    g.put(X0, 99.3, 0, 4, [label_line], TAB, bold=True)
    tight(g, X0, 0, 40, 40)
    box = "#F0F0F0"
    g.put(104.8, X1, 0, 1, [], frame(box, top="mid", left="mid", right="mid"))
    for r, (tag, text) in enumerate(tags, 1):
        g.put(104.8, 107.9, r, r + 1, [], frame(box, left="mid"))
        g.put(107.9, 150.4, r, r + 1, [runs_of(tag, WHITE)], frame("#7A7A7A"), line=1000)
        tight(g, 107.9, r, 20, 20)
        g.put(150.4, X1, r, r + 1, [text], frame(box, right="mid"), align="LEFT", line=1200)
        tight(g, 150.4, r, 60, 60)
    g.put(104.8, X1, 3, 4, [], frame(box, left="mid", right="mid", bottom="mid"))
    block(g, top)


# ---------------------------------------------------------------------------
# Page chrome (even page): PART label at the left of a rule; footer at the left.
# ---------------------------------------------------------------------------
foot = [(line1(55, 60, 815, 822)["text"], 1090, False, INK), ("   ", 1090, False, INK),
        ("한전KDN㈜", 1090, True, INK)]   # the logo is an image; its name is typed
L.add_table([[cell(0, W, 1500, [para(foot, "LEFT", 1300)[0]])]], floating=(5660, 81550))

g = Grid("part-head", [X0, 103.5, 160.0, X1], [1500])
g.put(X0, 103.5, 0, 1, [[("PART ", 800, False), ("01", 1300, True)]], line=1300)
g.put(103.5, 160.0, 0, 1, "경영관리", frame("#333333"), size=1080, bold=True, color=WHITE)
g.put(160.0, X1, 0, 1, [], frame(bottom="soft"))
block(g, 32.0)

g = Grid("banner", [X0, 124.0, X1], [2860])
g.put(X0, 124.0, 0, 1, [[("평가내용 ", 800, True, WHITE), ("03", 1350, True, WHITE)]], frame("#686868"),
      line=1500)
g.put(124.0, X1, 0, 1, [line1(125, 130, 76, 80)], striped, align="LEFT", line=1450)
block(g, 70.9)

section_band("sec1", line1(60, 70, 112, 118), line1(90, 95, 113, 118), 111.5)

# ---------------------------------------------------------------------------
# Section 1 framework (text layer)
# ---------------------------------------------------------------------------
xs = [X0, 105.4, 107.6, 137.0, 159.7, 330.8, 333.0, 344.5, 367.1, X1]
g = Grid("env", xs, [400, 1300, 630])
g.put(X0, 105.4, 0, 3, [line1(60, 65, 145, 150)], SIDE, bold=True)
for a, p0, p1, e, x in ((107.6, 137.0, 159.7, 330.8, 141), (333.0, 344.5, 367.1, X1, 347)):
    line = line1(x, x + 2, 145, 150)
    g.put(a, p0, 0, 3, [], HATCH)
    g.put(p0, p1, 0, 1, [], HATCH)
    g.put(p0, p1, 1, 2, [runs_of(line, x1=p1 - 1.5)], PILL, line=900)
    tight(g, p0, 1, 20, 20)
    g.put(p0, p1, 2, 3, [], HATCH)
    g.put(p1, e, 0, 1, [], HATCH)
    g.put(p1, e, 1, 3, [strip_runs(runs_of(line, x0=p1 - 1.5))], HATCH, align="LEFT")
    tight(g, p1, 1, 60, 60)
block(g, 140.8)

g = Grid("goal", [X0, 105.4, 107.6, X1], [2330])
g.put(X0, 105.4, 0, 1, [line1(60, 65, 172, 177)], SIDE, bold=True)
g.put(107.6, X1, 0, 1, [line1(155, 160, 172, 177)], frame("#D9D9D9"))
block(g, 167.7)

B = ((107.6, 255.4), (257.9, 405.7), (408.1, X1))
xs = [X0, 105.4] + [x for pair in B for x in pair]
g = Grid("direction", xs, [2080, 360, 3140, 3290])
g.put(X0, 105.4, 0, 1, [line1(60, 65, 198, 203)], SIDE, bold=True)
g.put(X0, 105.4, 1, 4, [line1(60, 65, 244, 249)], SIDE, bold=True)
for (a, e), num in zip(B, "①②③"):
    g.put(a, e, 0, 1, [line1(a, e, 198, 204)], frame(top="mid", left="mid", right="mid"), bold=True)
    g.put(a, e, 1, 2, [], frame(left="mid", right="mid"))
    first, second = lines_in(a, e, 219, 240)
    g.put(a, e, 2, 3, [lead(num, runs_of(first)), [("    ", 1090, False, INK)] + runs_of(second)],
          frame("#E6E6E6", left="mid", right="mid"), align="LEFT", line=1430)
    bullets = lines_in(a, e, 250, 272)
    g.put(a, e, 3, 4, hang(bullets, bullets[0]["bbox"][0]), frame(left="mid", right="mid", bottom="mid"),
          align="LEFT", line=1440)
block(g, 194.6)

TC = [107.6, 257.9, 321.1, 384.1, 447.2, X1]
g = Grid("targets", [X0, 105.4] + TC, [1950, 1420, 1410])
g.put(X0, 105.4, 0, 3, [line1(60, 65, 304, 309)], SIDE, bold=True)
heads = [[("구", 1090, True, INK), ("           ", 1090, True, INK), ("분", 1090, True, INK)]]
heads += [[line1(a, e, 289, 294)] for a, e in zip(TC[1:-1], TC[2:])]
for k, (a, e) in enumerate(zip(TC, TC[1:])):
    g.put(a, e, 0, 1, heads[k], frame("#D9D9D9", top="mid", left="soft" if k else None), bold=True)
    for r, y in ((1, 306), (2, 320)):
        lines = lines_in(a, e, y, y + 5)
        g.put(a, e, r, r + 1, lines, frame("#EDEDED" if k == 0 else None, left="soft" if k else None,
                                          bottom="mid" if r == 2 else "soft"), line=1200)
block(g, 286.7)

g = Grid("result1", [X0, 111.7, X1], [3400])
g.put(X0, 111.7, 0, 1, [runs_of(line1(65, 70, 351, 356), WHITE)], frame("#6A6A6A", top="mid", bottom="mid", left="mid"))
g.put(111.7, X1, 0, 1, lines_in(115, 120, 342, 362), frame(top="mid", bottom="mid", right="mid"), align="LEFT",
      line=1400)
block(g, 341.5)

# ---------------------------------------------------------------------------
# Section 2: 가. Fast Track / 공동심의제
# ---------------------------------------------------------------------------
section_band("sec2", line1(60, 70, 389, 395), line1(90, 95, 390, 395), 388.1)
titled("title-ga", line1(55, 60, 415, 421), 415.3)
complaint("problem-ga", line1(60, 65, 441, 446), lines_in(110, 500, 443, 476), 433.0, (1450, 1470, 1600))

h1, h2 = line1(170, 172, 499, 503), line1(400, 402, 499, 503)
rows = []
for y in (518, 532):
    pair = []
    for t0, t1, x in ((107.7, 126.5, 109), (335.9, 354.7, 337)):
        line = line1(x, x + 2, y, y + 3)
        tag = runs_of(line, x1=t1 - 1.0)
        is_new = tag[0][0] == "개선"
        pair.append((t0, t1, ([runs_of(line, WHITE if is_new else INK, x1=t1 - 1.0)],
                               [strip_runs(runs_of(line, x0=t1 - 1.0))]),
                     frame("#7F7F7F") if is_new else PILL, {}))
    rows.append(pair)
rows.append([(None, None, [hang([line1(128, 130, 546, 550)], 126.5)[0]], None, dict(align="LEFT", line=1000)),
             (None, None, [hang([line1(357, 358, 546, 550)], 354.7)[0]], None, dict(align="LEFT", line=1000))])
improve("improve-ga", line1(59, 60, 521, 526), 496.5, [1750, 1680, 1440, 1270],
        [(104.8, 168.8, 187.6, 325.3, h1), (333.0, 398.2, 416.9, X1, h2)], rows)

results("done-ga", line1(59, 60, 575, 580),
        [(line1(114, 115, 569, 573), line1(153, 154, 568, 572)), (line1(114, 115, 584, 588), line1(153, 154, 583, 587))],
        564.5, [300, 1420, 1420, 290])

# ---------------------------------------------------------------------------
# 나. Zero-Barrier
# ---------------------------------------------------------------------------
titled("title-na", line1(55, 60, 604, 610), 604.6)
complaint("problem-na", line1(60, 65, 630, 635), lines_in(105, 500, 632, 665), 622.4, (1450, 1450, 1620))

rows = [[(None, None, [line1(105, 325, 708, 712)], None, dict(line=1250)),
         (None, None, [line1(333, X1, 707, 711)], None, dict(line=1250))],
        [(None, None, [line1(105, 325, 720, 724)], None, dict(line=1150)),
         (None, None, [line1(333, X1, 720, 724)], None, dict(line=1150))]]
improve("improve-na", line1(59, 60, 704, 709), 686.4, [1760, 1450, 1460],
        [(104.8, None, None, 325.3, line1(170, 171, 689, 693)), (333.0, None, None, X1, line1(381, 382, 689, 693))],
        rows)

results("done-na", line1(59, 60, 750, 755),
        [(line1(115, 116, 744, 748), line1(153, 154, 743, 747)), (line1(115, 116, 759, 763), line1(153, 154, 758, 762))],
        740.2, [300, 1420, 1420, 290])

g = Grid("result2", [X0, 111.7, X1], [2150])
g.put(X0, 111.7, 0, 1, [runs_of(line1(65, 70, 783, 788), WHITE)], frame("#6A6A6A", top="mid", bottom="mid", left="mid"))
g.put(111.7, X1, 0, 1, [line1(115, 120, 783, 788)], frame(top="mid", bottom="mid", right="mid"), align="LEFT")
block(g, 779.8)

kit.finish(target, end=803.0)
