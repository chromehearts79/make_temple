"""Rebuild KDN 2025 report page 112 (3rd PDF local page 12, printed page 77) as editable HWPX.

Usage: python3 work/kdn2025/p112.py <report3.pdf> <out.hwpx> [--page 12]

재무성과관리(재무예산관리) 다. (수익제고, Best Practice): 추진배경, 추진경과 (four steps), 과제 5
(4대 분야 cards with illustrations and 주요실적 lines) + 과제 6 (two bullet columns), 주요성과, and
라. the K.D.N. 재무지표 table (목표/실적/증감/달성률 + 성과/환류 lines). Built with the shared kit
(one flat table per band on a grid of PDF x edges, rows at the PDF y positions); all text and
run sizes come from the PDF text layer.

Images in the source and how they are kept:
- PART 01 box, footer logo (its name typed), 다. pill (the N letter is a text-layer run: own dark
  cell), the 'Best Practice' sticker (trophy dropped) and the '지적사항 개선' tag (hand icon
  dropped): typed cells.
- 과제 tab numbers 5 / 6 (black boxes, image only): typed digits in separate dark cells.
- the circled arrows between the 추진경과 steps -> ▶; the bold ➡ arrows -> →; the circled plus
  between 과제 5 and 6 -> +.
- the four 4대 분야 illustrations -> photo placeholder cells.
- area / 수익제고 / 성과 / 환류 tags and the K D N boxes: text-layer runs in separate cells.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kit  # noqa: E402
from kit import Layout, recipe_inputs  # noqa: E402

source, target = recipe_inputs(12, "수익성과 공공성을 모두 확보하는 지속가능 재무성과 창출 체계 구축")
L = Layout(top=3100)
kit.setup(source, L)
from kit import *  # noqa: E402,F401,F403  helpers and presets bound to this page

SIDE = "#D9D9D9"
TAB, NUM, TITLE = "#808080", "#111111", "#D9D9D9"
BOXED = frame(WHITE, top="soft", bottom="soft", left="soft", right="soft")
DARK_TAG = frame("#7E7E7E")
HATCH = frame("#F0F0F0", hatch="#E0E0E0")


def hang(lines, base):
    """Lines keep their PDF indent; a line opened by blanks and no '-' (the ➡ image sits in
    those blanks) starts with a typed → instead."""
    out = []
    for line in lines:
        runs = runs_of(line)
        size = runs[0][1] / 100
        raw = "".join(s["text"] for s in line["spans"])
        lead = len(raw) - len(raw.lstrip(" "))
        if lead and not raw.lstrip().startswith("-"):
            out.append([(" → ", runs[0][1], True, INK)] + runs)
            continue
        offset = line["bbox"][0] - base + lead * 0.29 * size
        n = max(0, round(offset / (0.29 * size)))
        out.append([(" " * n, runs[0][1], False, INK)] + runs if n else runs)
    return out


def tight(g, x0, r0, **margin):
    key = (r0, g.xs.index(to_x(x0)))
    g.items[key] = (*g.items[key][:7], margin)


def quiet(g, *args, **kw):
    """put() for cells whose padding is narrowed afterwards (the kit's size check assumes 160)."""
    n = len(WARN)
    g.put(*args, **kw)
    del WARN[n:]


def pad(g, x0, x1, r, fill="1"):
    """Thin spacer cell (no padding, 1 pt paragraph)."""
    quiet(g, x0, x1, r, r + 1, "", fill, size=100, line=100, fit=False)
    tight(g, x0, r, top=0, bottom=0)


def white(runs):
    return [(t, s, b, WHITE) for t, s, b, _ in runs]


def split_at(line, x):
    """(runs left of x, runs from x on) of one PDF line."""
    return runs_of(line, x1=x), strip_runs(runs_of(line, x0=x))


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

# ---------------------------------------------------------------------------
# 다. [N 수익제고] title  [Best Practice]
# ---------------------------------------------------------------------------
num = line1(55, 60, 71, 75)
runs = runs_of(line1(84, 88, 71, 75))
A, K0, K1, P1, S0 = 76.0, 82.0, 95.6, 142.0, 486.0
g = Grid("title-da", [X0, A, K0, K1, P1, S0, X1], [100, 1450, 100])
quiet(g, X0, A, 0, 3, [num], align="LEFT", line=1450, fit=False)
tight(g, X0, 0, left=0, right=0)
pill = frame(TITLE)
g.put(A, K0, 0, 3, [], pill)
for x0, x1, fill in ((K0, K1, pill), (K1, P1, pill), (P1, S0, "1")):
    pad(g, x0, x1, 0, fill)
    pad(g, x0, x1, 2, fill)
quiet(g, K0, K1, 1, 2, [white(runs[:1])], frame("#3E3E3E"), line=1000, fit=False)
tight(g, K0, 1, left=0, right=0, top=0, bottom=0)
quiet(g, K1, P1, 1, 2, [strip_runs(runs[1:2])], pill, align="LEFT", line=1250)
tight(g, K1, 1, left=150, right=60, top=0, bottom=0)
quiet(g, P1, S0, 1, 2, [strip_runs(runs[2:])], align="LEFT", line=1450)
tight(g, P1, 1, top=0, bottom=0)
g.put(S0, X1, 0, 3, "Best Practice", frame("#3A3A3A"), size=850, bold=True, color=WHITE, line=1000)
block(g, 70.7)

# 추진배경
g = Grid("bg", [X0, 113.0, X1], [5340])
g.put(X0, 113.0, 0, 1, [line1(60, 70, 113, 118)], frame(TITLE, top="mid", bottom="mid", left="mid"))
g.put(113.0, X1, 0, 1, lines_in(115, 120, 97, 135), frame(top="mid", bottom="mid", right="mid"),
      align="LEFT", line=1540)
block(g, 93.5)

# ---------------------------------------------------------------------------
# 추진경과: four graded step heads joined by ▶, two-line bodies split by dotted rules
# ---------------------------------------------------------------------------
heads = ((89.2, 203.3), (218.8, 321.4), (336.9, 439.6), (455.1, X1))
arrows = ((203.3, 218.8), (321.4, 336.9), (439.6, 455.1))
bodies = ((89.2, 204.8), (204.8, 322.4), (322.4, 440.0), (440.0, X1))
shades = ("#F3F3F3", "#E4E4E4", "#D2D2D2", "#C9C9C9")
xs = sorted({X0, 86.6} | {x for h in heads for x in h} | {x for b in bodies for x in b})
g = Grid("steps", xs, [1920, 3580])
g.put(X0, 86.6, 0, 2, [line1(60, 65, 169, 174), line1(60, 65, 182, 187)], frame("#E5E5E5"), bold=True,
      line=1320)
for k, ((a, e), shade) in enumerate(zip(heads, shades)):
    g.put(a, e, 0, 1, [line1(a, e, 156, 160)], frame(shade))
    if k < 3:
        g.put(*arrows[k], 0, 1, "▶", frame(shades[k + 1]), size=900, color="#7F7F7F", fit=False)
for k, (a, e) in enumerate(bodies):
    rule = dict(right="dot") if k < 3 else {}
    g.put(a, e, 1, 2, lines_in(a, e, 175, 205), frame(bottom="soft", **rule), line=1300)
block(g, 153.2)

# ---------------------------------------------------------------------------
# 과제 5: header (tab | number | title | 지적사항 개선), 4대 분야 cards, 주요실적
# ---------------------------------------------------------------------------
IN0, MID, R1 = 119.5, 337.0, X1
subs = ((IN0, 227.9), (227.9, MID), (MID, 446.1), (446.1, R1))
pills = ((125.3, 157.0), (244.1, 275.8), (347.7, 379.4), (456.8, 488.5))
photos = ((146.4, 199.6), (259.1, 305.1), (359.9, 422.8), (469.1, 531.5))
tags = ((123.4, 166.3), (341.6, 384.5))
HEAD5 = (89.2, 110.0, 121.0, 133.2, 501.1, 553.2)
xs = sorted({X0, 86.6, 89.2, IN0, MID, R1, *HEAD5} | {x for s in subs for x in s} | {x for p in pills for x in p}
            | {x for p in photos for x in p} | {x for t in tags for x in t})
hs = [430, 1000, 450, 2330, 1770, 3870, 4100, 2200, 1650, 1600, 1600, 1550, 1650, 1900]
g = Grid("task5", xs, hs)
g.put(X0, 86.6, 0, 14, [line1(60, 70, y - 3, y + 3) for y in (319.0, 332.2, 348.4, 364.6)], frame(SIDE),
      bold=True, line=1500)
a, n0, n1, t1, j0, j1 = HEAD5
tab = frame(TAB)
g.put(a, n0, 0, 3, [runs_of(line1(a, n0, 219, 223), WHITE)], tab, line=1150)
tight(g, a, 0, left=200, right=40)
g.put(n0, n1, 0, 1, [], tab)
quiet(g, n0, n1, 1, 2, "5", frame(NUM), size=900, bold=True, color=WHITE, line=1000, fit=False)
tight(g, n0, 1, left=0, right=0, top=0, bottom=0)
g.put(n0, n1, 2, 3, [], tab)
g.put(n1, t1, 0, 3, [], tab)
g.put(t1, j0, 0, 3, [line1(t1, j0, 217, 221)], frame(TITLE), align="LEFT")
tight(g, t1, 0, left=40)
pad(g, j0, j1, 0, frame(TITLE))
quiet(g, j0, j1, 1, 2, "지적사항 개선", frame("#3A3A3A"), size=780, bold=True, color=WHITE, line=900)
tight(g, j0, 1, left=60, right=60, top=0, bottom=0)
pad(g, j0, j1, 2, frame(TITLE))
g.put(j1, X1, 0, 3, [], frame(TITLE))
# inner labels: 4대 분야 (head to quotes), 주요실적 (hatched head to end)
g.put(89.2, IN0, 3, 7, [line1(95, 100, 282, 286), line1(95, 100, 295, 299)], frame("#CBCBCB", left="mid"),
      bold=True, line=1320)
g.put(89.2, IN0, 7, 14, [line1(95, 100, 404, 408), line1(95, 100, 418, 421)],
      frame("#B2B2B2", left="mid", bottom="mid"), bold=True, line=1320)
for h, (a, e) in enumerate(((IN0, MID), (MID, R1))):
    edge = dict(right="mid") if h else dict(right="soft")
    g.put(a, e, 3, 4, [runs_of(line1(a, e, 240, 244), WHITE)], frame("#868686", **edge))
    g.put(a, e, 7, 8, [line1(a, e, 360, 364)], frame("#F0F0F0", hatch="#E0E0E0", top="soft", **edge))
for k, ((a, e), (p0, p1), (f0, f1)) in enumerate(zip(subs, pills, photos)):
    sep = dict(right="dot") if k in (0, 2) else dict(right="mid") if k == 3 else dict(right="soft")
    area = line1(p0, p1, 259, 263)
    split = next(s["bbox"][0] for s in area["spans"] if s["size"] > 9.5)
    pad_l = frame("#EDEDED")
    g.put(a, p0, 4, 5, [], pad_l)
    quiet(g, p0, p1, 4, 5, [runs_of(area, x1=split)], BOXED, line=1000, fit=False, ratio=88)
    tight(g, p0, 4, left=0, right=0)
    g.put(p1, e, 4, 5, [strip_runs(runs_of(area, x0=split))], frame("#EDEDED", **sep), align="LEFT")
    tight(g, p1, 4, left=150)
    g.put(a, f0, 5, 6, [])
    g.put(f0, f1, 5, 6, [], photo)
    g.put(f1, e, 5, 6, [], frame(**sep))
    g.put(a, e, 6, 7, lines_in(a, e, 314, 353), frame(bottom="soft", **sep), line=1200)
# 주요실적: tag line, then two indented lines; twice per half
left, right = (IN0, MID, 123.5), (MID, R1, 341.8)
for (a, e, base), (k0, k1), lines in ((left, tags[0], lines_in(IN0, MID, 376, 472)),
                                       (right, tags[1], lines_in(MID, R1, 376, 472))):
    edge = dict(right="mid") if e == R1 else dict(right="soft")
    tagged = [l for l in lines if any(s["size"] < 9.2 and s["bbox"][0] < k1 for s in l["spans"][:1])]
    assert len(tagged) == 2, [l["text"] for l in tagged]
    for r, line in zip((8, 11), tagged):
        split = next(s["bbox"][0] for s in line["spans"] if s["bbox"][0] > k1 - 1)
        tag, text = split_at(line, split)
        g.put(a, k0, r, r + 1, [])
        quiet(g, k0, k1, r, r + 1, [white(tag)], DARK_TAG, line=1000, fit=False, ratio=88)
        tight(g, k0, r, left=0, right=0, top=0, bottom=0)
        g.put(k1, e, r, r + 1, [text], frame(**edge), align="LEFT")
        tight(g, k1, r, left=150)
    first, second = [l for l in lines if l["bbox"][1] < tagged[1]["bbox"][1] and l not in tagged], \
                    [l for l in lines if l["bbox"][1] > tagged[1]["bbox"][1] + 2]
    for r, par in zip((9, 10), hang(first, base)):        # one row per line: own 장평 each
        g.put(a, e, r, r + 1, [par], frame(**edge), align="LEFT", line=1420)
    if e == MID:
        # '수탁분야 자체투입률 제고 ➡ 외주비 111억원 절감' is two PDF lines on one row
        dash, cont, tail = sorted(second, key=lambda l: (l["bbox"][1] // 5, l["bbox"][0]))
        pars = hang([dash], base) + [[("    ", 990, False, INK)] + runs_of(cont) + [(" → ", 990, True, INK)]
                                     + runs_of(tail)]
    else:
        pars = hang(second, base)
    g.put(a, e, 12, 13, pars[:1], frame(**edge), align="LEFT", line=1420)
    g.put(a, e, 13, 14, pars[1:], frame(bottom="mid", **edge), align="LEFT", line=1450)
block(g, 214.5)

# circled plus between the two task boxes
g = Grid("plus", [X0, 315.5, 329.3, X1], [1380])
g.put(315.5, 329.3, 0, 1, "+", frame("#A8A8A8"), size=1100, bold=True, color=WHITE, line=1150, fit=False)
block(g, 475.5)

# ---------------------------------------------------------------------------
# 과제 6: header (tab | number | centred title), two columns of bullets
# ---------------------------------------------------------------------------
a, n0, n1, t1, c = 89.2, 110.0, 121.0, 133.2, 322.8
g = Grid("task6", [X0, 86.6, a, n0, n1, t1, c, X1], [430, 1000, 450, 2170, 7200])
g.put(X0, 86.6, 0, 5, [line1(60, 70, y - 3, y + 3) for y in (518.4, 531.6, 547.8, 564.0)], frame(SIDE),
      bold=True, line=1500)
g.put(a, n0, 0, 3, [runs_of(line1(a, n0, 494, 498), WHITE)], tab, line=1150)
tight(g, a, 0, left=200, right=40)
g.put(n0, n1, 0, 1, [], tab)
quiet(g, n0, n1, 1, 2, "6", frame(NUM), size=900, bold=True, color=WHITE, line=1000, fit=False)
tight(g, n0, 1, left=0, right=0, top=0, bottom=0)
g.put(n0, n1, 2, 3, [], tab)
g.put(n1, t1, 0, 3, [], tab)
g.put(t1, X1, 0, 3, [line1(t1, X1, 492, 496)], frame(TITLE))
for k, (x0, x1, base) in enumerate(((a, c, 95.4), (c, X1, 327.5))):
    edge = dict(right="dot") if k == 0 else dict(right="mid")
    lft = dict(left="mid") if k == 0 else {}
    g.put(x0, x1, 3, 4, [line1(x0, x1, 513, 517)], frame("#EDEDED", top="mid", **edge, **lft))
    g.put(x0, x1, 4, 5, hang(lines_in(x0, x1, 530, 600), base), frame(bottom="mid", **edge, **lft),
          align="LEFT", line=1650)
block(g, 489.3)

# 주요성과: two rows, each 'left result ➡ right result'
g = Grid("outcome", [X0, 113.0, 332.0, 345.5, X1], [1855, 1855])
g.put(X0, 113.0, 0, 2, [runs_of(line1(60, 70, 620, 624), WHITE)], frame("#7F7F7F", top="mid", bottom="mid", left="mid"))
for r, y in ((0, 613.4), (1, 628.7)):
    edge = dict(top="mid") if r == 0 else dict(bottom="mid")
    g.put(113.0, 332.0, r, r + 1, [line1(115, 120, y - 1, y + 1)], frame(**edge), align="LEFT")
    g.put(332.0, 345.5, r, r + 1, "→", frame(**edge), size=1090, bold=True, fit=False)
    g.put(345.5, X1, r, r + 1, [line1(345, 350, y - 2, y + 1)], frame(right="mid", **edge), align="LEFT")
    tight(g, 345.5, r, left=60)
block(g, 608.1)

# ---------------------------------------------------------------------------
# 라. K.D.N. 재무지표 table
# ---------------------------------------------------------------------------
g = Grid("title-ra", [X0, X1], [1650])
g.put(X0, X1, 0, 1, [line1(55, 60, 655, 660)], align="LEFT", line=1450)
block(g, 656.0)

C = [X0, 99.24, 141.72, 185.64, 229.62, 273.54, 317.46, X1]
KB, TG = (72.1, 83.8), (320.3, 339.1)
xs = sorted(set(C) | set(KB) | set(TG))
ROWS = (696.0, 731.4, 766.8)
sub = [450, 1110, 420, 1120, 440]
g = Grid("table", xs, [1840] + sub * 3)
light = "#D8D8D8"
heads = lines_in(55, 560, 680, 685)
assert len(heads) == 7, [h["text"] for h in heads]
for k, h in enumerate(heads):
    x0, x1 = C[k], C[k + 1]
    if 2 <= k <= 5:
        box = dict(top="strong", left="strong" if k == 2 else None, right="strong" if k == 5 else None)
        g.put(x0, x1, 0, 1, [runs_of(h, WHITE)], frame("#7F7F7F", **{s: v for s, v in box.items() if v}))
    else:
        g.put(x0, x1, 0, 1, [h], frame(light, top="soft"))
for i, top in enumerate(ROWS):
    r = 1 + 5 * i
    last = i == 2
    rule = dict(bottom="soft")
    ys = (top, top + 35.4)
    # 구분: dark letter box over the dimension name
    gb = frame("#EBEBEB")
    g.put(X0, C[1], r, r + 1, [], gb)
    g.put(X0, KB[0], r + 1, r + 3, [], gb)
    letter = line1(KB[0], KB[1], top + 4, top + 12)
    quiet(g, KB[0], KB[1], r + 1, r + 2, [white(runs_of(letter))], frame("#3E3E3E"), line=1000, fit=False)
    tight(g, KB[0], r + 1, left=0, right=0, top=0, bottom=0)
    g.put(KB[0], KB[1], r + 2, r + 3, [], gb)
    g.put(KB[1], C[1], r + 1, r + 3, [], gb)
    g.put(X0, C[1], r + 3, r + 5, [line1(60, 70, top + 17, top + 23)], frame("#EBEBEB", **rule))
    # 지표 and the four values
    g.put(C[1], C[2], r, r + 5, lines_in(C[1], C[2], *ys), frame(**rule), line=1500)
    vals = [l for l in lines_in(C[2], C[6], *ys)]
    for k in range(2, 6):
        x0, x1 = C[k], C[k + 1]
        spans = [s for l in vals for s in l["spans"] if x0 <= s["bbox"][0] < x1]
        runs = strip_runs(runs_of(dict(spans=spans)))
        box = dict(left="strong" if k == 2 else None, right="strong" if k == 5 else None,
                   bottom="strong" if last else "soft")
        g.put(x0, x1, r, r + 5, [runs], frame(**{s: v for s, v in box.items() if v}), align="RIGHT")
    # 추진성과: 성과 (dark) / 환류 (outlined) tags with their lines
    lines = lines_in(320, 325, *ys)
    assert len(lines) == 2, [l["text"] for l in lines]
    g.put(C[6], X1, r, r + 1, [])
    for (rr, n), line, fill, color in zip(((r + 1, 2), (r + 3, 2)), lines, (DARK_TAG, BOXED), (WHITE, INK)):
        split = line["spans"][1]["bbox"][0] - 0.5
        tag, text = split_at(line, split)
        g.put(C[6], TG[0], rr, rr + n, [], frame(bottom="soft") if rr == r + 3 else "1")
        quiet(g, TG[0], TG[1], rr, rr + 1, [[(t, s, b, color) for t, s, b, _ in tag]], fill, line=1000,
              fit=False, ratio=86)
        tight(g, TG[0], rr, left=0, right=0, top=0, bottom=0)
        g.put(TG[0], TG[1], rr + 1, rr + 2, [], frame(bottom="soft") if rr == r + 3 else "1")
        g.put(TG[1], X1, rr, rr + n, [text], frame(bottom="soft") if rr == r + 3 else "1", align="LEFT")
        tight(g, TG[1], rr, left=80, right=40)
block(g, 677.6)

kit.finish(target, end=803.0)
