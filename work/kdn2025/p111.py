"""Rebuild KDN 2025 report page 111 (3rd PDF local page 11, printed page 76) as editable HWPX.

Usage: python3 work/kdn2025/p111.py <report3.pdf> <out.hwpx> [--page 11]

재무성과관리(재무예산관리), section 2 "AX･DX 기반 사업경쟁력 고도화와 재무건전성 강화를 통한 최고
수준 경영성과 달성": 가. (매출성장) and 나. (위험관리), each a 추진배경 box, a 추진노력 block of two
과제 columns (tab + title, dark 추진방향 band with a white tag, hatched sub-headings, bullets),
chevrons and a 주요실적 row of tagged lines; 가. closes with a 주요성과 strip. Built with the shared
kit (one flat table per band on a grid of PDF x edges, rows at the PDF y positions); all text and
run sizes come from the PDF text layer.

Images in the source and how they are kept:
- section band, side tab, title pills (the K / D letters are text-layer runs: own dark cells).
- 과제 tab numbers 1-4 (black boxes, image only): typed digits in separate dark cells.
- the bold ➡ arrows in front of the 나. detail lines -> → ; the grey chevrons -> ▼ rows.
- 주요실적 tags are text-layer runs in drawn boxes: separate outlined (left) / dark (right) cells.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kit  # noqa: E402
from kit import Layout, recipe_inputs  # noqa: E402

source, target = recipe_inputs(11, "디지털 기반 사업경쟁력 강화와 신사업 포트폴리오 확대를 통한 성장 모멘텀 극대화")
L = Layout(top=3100)
kit.setup(source, L)
from kit import *  # noqa: E402,F401,F403  helpers and presets bound to this page

SIDE = "#EDEDED"                     # 추진노력 / 주요실적 side labels
TAB, NUM, TITLE = "#808080", "#111111", "#D9D9D9"
DIR = "#868686"                      # 추진방향 band
HATCH = "#F0F0F0"
BOXED = frame(WHITE, top="soft", bottom="soft", left="soft", right="soft")
DARK_TAG = frame("#7E7E7E")
CHEVRON = "#C4C4C4"


def hang(lines, base, arrow=False):
    """Lines keep their PDF indent; with arrow=True a line opened by blanks (the ➡ image sits
    there) starts with a typed → instead."""
    out = []
    for line in lines:
        runs = runs_of(line)
        size = runs[0][1] / 100
        raw = "".join(s["text"] for s in line["spans"])
        lead = len(raw) - len(raw.lstrip(" "))
        if arrow and lead:
            out.append([(" → ", runs[0][1], True, INK)] + runs)
            continue
        offset = line["bbox"][0] - base + lead * 0.29 * size
        n = max(0, round(offset / (0.29 * size)))
        out.append([(" " * n, runs[0][1], False, INK)] + runs if n else runs)
    return out


def merged(lines):
    """One visual row split by the PDF at superscripts: one line dict with all spans."""
    lines = sorted(lines, key=lambda l: l["bbox"][0])
    return dict(bbox=lines[0]["bbox"], spans=[s for l in lines for s in l["spans"]])


def tight(g, x0, r0, **margin):
    key = (r0, g.xs.index(to_x(x0)))
    g.items[key] = (*g.items[key][:7], margin)


def quiet(g, *args, **kw):
    """put() for cells whose padding is narrowed afterwards (the kit's size check assumes 160)."""
    n = len(WARN)
    g.put(*args, **kw)
    del WARN[n:]


# ---------------------------------------------------------------------------
# Page chrome: running head over a rule, side tab, footer at the right.
# ---------------------------------------------------------------------------
L.add_table([[cell(0, 3350, 1680, [para([("01", 1380, True, WHITE)], "CENTER")[0]], dark)],
             [cell(0, 3350, 5960, [para([(ch, 950, True, INK)], "CENTER", 1160)[0] for ch in "경영관리"], gray2)]],
            floating=(57800, 15000))
foot = [(text, size, False, INK) for text, size in (
    (line1(450, 455, 818, 822)["text"], 790), ("    ", 790), (line1(540, 546, 816, 820)["text"], 1090))]
L.add_table([[cell(0, W, 1500, [para(foot, "RIGHT", 1300)[0]])]], floating=(5660, 81550))

g = Grid("head", [X0, 430.0, X1], [1680])
g.put(X0, 430.0, 0, 1, [], frame(bottom="soft"))
g.put(430.0, X1, 0, 1, [line1(430, 440, 35, 40)], align="RIGHT")
block(g, 32.0)

# Section 2 band (image): dark number, light title band.
g = Grid("sec2", [X0, 85.0, X1], [2300])
g.put(X0, 85.0, 0, 1, [runs_of(line1(60, 70, 72, 77), WHITE)], frame("#707070"), line=1800)
g.put(85.0, X1, 0, 1, [line1(90, 95, 72, 78)], frame("#E6E6E6"), align="LEFT", line=1700)
block(g, 70.9)


def title_row(name, number_line, line, edges, top):
    """'가. [K 매출성장] title': number, pill with a dark letter box, 14 pt title."""
    a, k0, k1, p1 = edges
    runs = runs_of(line)
    g = Grid(name, [X0, a, k0, k1, p1, X1], [250, 1170, 230])
    quiet(g, X0, a, 0, 3, [number_line], align="LEFT", line=1450, fit=False)
    tight(g, X0, 0, left=0, right=0)
    pill = frame(TITLE)
    g.put(a, k0, 0, 3, [], pill)
    g.put(k0, k1, 0, 1, [], pill)
    quiet(g, k0, k1, 1, 2, [[(t, s, b, WHITE) for t, s, b, _ in runs[:1]]], frame("#3E3E3E"), line=900,
          fit=False)
    tight(g, k0, 1, left=0, right=0, top=0, bottom=0)
    g.put(k0, k1, 2, 3, [], pill)
    g.put(k1, p1, 0, 3, [strip_runs(runs[1:2])], pill, align="LEFT", line=1250)
    tight(g, k1, 0, left=150, right=60)
    g.put(p1, X1, 0, 3, [strip_runs(runs[2:])], align="LEFT", line=1450)
    block(g, top)


def background(name, label_y, body_y, top):
    g = Grid(name, [X0, 113.0, X1], [3720])
    g.put(X0, 113.0, 0, 1, [line1(60, 70, label_y - 2, label_y + 3)],
          frame(TITLE, top="mid", bottom="mid", left="mid"))
    g.put(113.0, X1, 0, 1, lines_in(115, 120, *body_y), frame(top="mid", bottom="mid", right="mid"),
          align="LEFT", line=1540)
    block(g, top)


def effort(name, cols, hs, label_ys, rows_y, pitch, top, arrow):
    """추진노력: side label, then per column header (과제 tab | number | title), 추진방향 band
    with a white tag, two hatched sub-headings each followed by bullets.

    cols: (a, t0, n0, n1, t1, b, digit, base) per column; hs: row heights (10 rows);
    rows_y: PDF y ranges of (head, band, hatch1, bullets1, hatch2, bullets2)."""
    edges = {X0, 85.2, X1}
    for c in cols:
        edges |= set(c[:6])
    g = Grid(name, sorted(edges), hs)
    g.put(X0, 85.2, 0, 10, [line1(60, 65, y - 4, y + 3) for y in label_ys], frame(SIDE), bold=True,
          line=1320)
    head_y, band_y, h1, b1, h2, b2 = rows_y
    side = dict(left="mid", right="mid")
    for a, t0, n0, n1, t1, b, digit, base in cols:
        tab = frame(TAB)
        g.put(a, n0, 0, 3, [runs_of(line1(a, n0, *head_y), WHITE)], tab, line=1150)
        tight(g, a, 0, left=200, right=40)
        g.put(n0, n1, 0, 1, [], tab)
        quiet(g, n0, n1, 1, 2, digit, frame(NUM), size=900, bold=True, color=WHITE, line=1000, fit=False)
        tight(g, n0, 1, left=0, right=0, top=0, bottom=0)
        g.put(n0, n1, 2, 3, [], tab)
        g.put(n1, t1, 0, 3, [], tab)
        g.put(t1, b, 0, 3, [line1(t1, b, *head_y)], frame(TITLE))
        # 추진방향 band: dark band, white tag in the middle sub-row
        runs = runs_of(line1(a, b, *band_y))
        band = frame(DIR)
        g.put(a, t0, 3, 6, [], frame(DIR, left="mid"))
        g.put(t0, t1, 3, 4, [], band)
        quiet(g, t0, t1, 4, 5, [runs[:1]], BOXED, line=1000, fit=False, ratio=90)
        tight(g, t0, 4, left=0, right=0, top=0, bottom=0)
        g.put(t0, t1, 5, 6, [], band)
        text = [(t, s, bb, WHITE) for t, s, bb, _ in strip_runs(runs[1:])]
        g.put(t1, b, 3, 6, [text], frame(DIR, right="mid"), align="LEFT", line=1250)
        tight(g, t1, 3, left=120)
        # sub-headings and bullets
        g.put(a, b, 6, 7, [line1(a, b, *h1)], frame(HATCH, hatch="#E0E0E0", **side), line=1300)
        g.put(a, b, 7, 8, hang(lines_in(a, b, *b1), base, arrow), frame(**side), align="LEFT", line=pitch)
        g.put(a, b, 8, 9, [line1(a, b, *h2)], frame(HATCH, hatch="#E0E0E0", top="dot", **side), line=1300)
        g.put(a, b, 9, 10, hang(lines_in(a, b, *b2), base, arrow), frame(bottom="mid", **side), align="LEFT",
              line=pitch)
    block(g, top)


def chevrons(name, centers, top):
    edges = [X0]
    for c in centers:
        edges += [c - 15.0, c + 15.0]
    g = Grid(name, edges + [X1], [1390])
    for c in centers:
        g.put(c - 15.0, c + 15.0, 0, 1, "▼", size=1200, color=CHEVRON, line=1200, fit=False)
    block(g, top)


def results(name, label_ys, cols, rows, hs, top):
    """주요실적: side label, two outlined boxes of tagged lines (tag cell | text cell).

    cols: (a, k0, k1, b, fill, color) per box; rows: per box, the line dicts of its rows."""
    edges = {X0, 85.2, X1}
    for c in cols:
        edges |= set(c[:4])
    g = Grid(name, sorted(edges), hs)
    n = len(hs)
    g.put(X0, 85.2, 0, n, [line1(60, 65, y - 4, y + 3) for y in label_ys], frame(SIDE), bold=True, line=1320)
    for (a, k0, k1, b, fill, color), lines in zip(cols, rows):
        g.put(a, b, 0, 1, [], frame(top="mid", left="mid", right="mid"))
        g.put(a, b, n - 1, n, [], frame(bottom="mid", left="mid", right="mid"))
        for r, line in enumerate(lines, 1):
            split = next(s["bbox"][0] for s in line["spans"] if s["bbox"][0] > k0 + 8 and s["size"] > 9.5) - 0.5
            g.put(a, k0, r, r + 1, [], frame(left="mid"))
            quiet(g, k0, k1, r, r + 1, [runs_of(line, color, x1=split)], fill, line=1000, fit=False, ratio=86)
            tight(g, k0, r, left=0, right=0, top=0, bottom=0)
            g.put(k1, b, r, r + 1, [strip_runs(runs_of(line, x0=split))], frame(right="mid"), align="LEFT",
                  line=1300)
            tight(g, k1, r, left=150, right=60)
    block(g, top)


# ---------------------------------------------------------------------------
# 가. 매출성장
# ---------------------------------------------------------------------------
title_row("title-ga", line1(55, 60, 100, 105), line1(84, 86, 100, 105), (74.4, 80.6, 94.0, 140.4), 99.6)
background("bg-ga", 137.5, (125, 150), 122.7)
effort("effort-ga",
       [(87.8, 92.9, 108.6, 120.4, 130.4, 317.0, "1", 93.7),
        (321.0, 326.3, 342.4, 354.6, 363.7, 553.0, "2", 327.1)],
       [560, 1040, 440, 430, 1310, 460, 2090, 6600, 2130, 3920], (252.4, 265.6),
       ((168, 175), (190, 195), (212, 217), (229, 295), (299, 305), (317, 352)), 1600, 166.2, False)
chevrons("chev-ga", (202.4, 437.0), 356.0)
ga_rows = [[line1(90, 125, y - 2, y + 2) for y in (376.0, 390.7, 405.3)],
           [line1(328, 340, y - 2, y + 2) for y in (376.0, 390.7, 405.3)]]
results("results-ga", (386.2, 399.4),
        [(87.8, 92.8, 120.6, 319.9, BOXED, INK), (323.8, 329.5, 351.0, X1, DARK_TAG, WHITE)],
        ga_rows, [510, 1465, 1465, 1465, 365], 369.9)

g = Grid("outcome-ga", [X0, 113.0, X1], [2260])
g.put(X0, 113.0, 0, 1, [runs_of(line1(60, 70, 433, 438), WHITE)], frame("#7F7F7F", top="mid", bottom="mid", left="mid"))
g.put(113.0, X1, 0, 1, [line1(115, 120, 433, 438)], frame(top="mid", bottom="mid", right="mid"), align="LEFT")
block(g, 428.9)

# ---------------------------------------------------------------------------
# 나. 위험관리
# ---------------------------------------------------------------------------
title_row("title-na", line1(55, 60, 463, 467), line1(85, 88, 463, 467), (76.9, 83.4, 96.5, 143.0), 462.6)
background("bg-na", 500.4, (488, 512), 485.4)
effort("effort-na",
       [(87.8, 93.6, 108.8, 120.2, 131.0, 319.9, "3", 93.7),
        (323.8, 329.7, 344.8, 356.2, 367.1, X1, "4", 329.9)],
       [550, 1040, 420, 450, 1310, 500, 2070, 6570, 2160, 6850], (629.4, 642.6),
       ((530, 537), (552, 557), (574, 579), (592, 658), (662, 667), (680, 745)), 1570, 528.9, True)
chevrons("chev-na", (203.7, 439.8), 748.1)
na_rows = [[line1(90, 105, y - 2, y + 3) for y in (770.3, 783.4)],
           [line1(330, 340, 767, 772), merged(lines_in(330, 545, 781, 786))]]
na_rows[0] = [merged([line1(90, 105, 769, 772), line1(135, 140, 767, 770)]), na_rows[0][1]]
results("results-na", (771.1, 784.3),
        [(87.8, 92.8, 137.6, 319.9, BOXED, INK), (323.8, 329.4, 390.0, X1, BOXED, INK)],
        na_rows, [550, 1460, 1460, 470], 762.0)

kit.finish(target, end=802.0)
