"""Rebuild KDN 2025 report page 130 (3rd PDF local page 30, printed page 90) as editable HWPX.

Usage: python3 work/kdn2025/p130.py <report3.pdf> <out.hwpx> [--page 30]

조직 및 인적자원관리, section 3 "직무 중심 인사제도 운영 ..." with its 추진목표 / 추진방향 /
세부과제 box, the three 가. 나. 다. tables (구분 | 내용 | 주요 실적) and the 주요성과 box. Built
with the shared kit (one flat table per horizontal band on a grid of PDF x edges); all text comes
from the PDF text layer. Every tag printed inside a line (연공성 완화, 전문가 확보, 건축안전,
정보보호, 직무연계, 직위발굴, 신규채용, 신규, 개선, '사람중심'→'직무중심', 승진･경력직 ...) is its own
cell: such lines get one table row each and are cut into lead | tag | text cells at the PDF
span boundaries.

Images and how they are kept: PART box, section-3 number band, footer logo (typed "한전KDN㈜"),
the dark numbered squares of 추진방향 (typed as dark cells with 1 2 3), the chevrons between the
추진방향 segments (▶), the gray pills behind the 가. 나. 다. badges (cell fills) and the
"지적사항 개선" sticker of 다. (typed as a dark tag; hand icon dropped).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kit  # noqa: E402
from kit import Layout, recipe_inputs  # noqa: E402

source, target = recipe_inputs(30, "직무 중심 인사제도 운영을 통한 조직과 구성원의 동반성장 실현")
L = Layout(top=3100)
kit.setup(source, L)
from kit import *  # noqa: E402,F401,F403  helpers and presets bound to this page

DARK, HEAD, SIDE = "#6A6A6A", "#D9D9D9", "#EDEDED"
HATCHED = frame("#E6E6E6", hatch="#D6D6D6")
OUT_TAG = frame(WHITE, top="soft", bottom="soft", left="soft", right="soft")
DARK_TAG = frame("#7F7F7F")


def tight(g, x0, r0, left=0, right=0):
    c0 = g.xs.index(to_x(x0))
    item = g.items[r0, c0]
    g.items[r0, c0] = (*item[:7], dict(left=left, right=right))


def hang(lines, base):
    """Lines keep their PDF indent: spaces for the x offset from the bullet."""
    out = []
    for l in lines:
        runs = runs_of(l)
        size = runs[0][1] / 100
        raw = "".join(s["text"] for s in l["spans"])
        offset = l["bbox"][0] - base + (len(raw) - len(raw.lstrip(" "))) * 0.29 * size
        n = max(0, round(offset / (0.29 * size)))
        out.append([(" " * n, runs[0][1], False, INK)] + runs if n else runs)
    return out


def is_tag(s):
    bold = any(f in s["font"] for f in kit.BOLD_FONTS + kit.SYMBOL_FONTS)
    return 7.5 < s["size"] < 9.6 and bold


def groups(ln):
    """Split a line's spans into consecutive (is_tag, spans) groups."""
    out = []
    for s in ln["spans"]:
        k = is_tag(s)
        if out and out[-1][0] == k:
            out[-1][1].append(s)
        else:
            out.append((k, [s]))
    return out


def tagged(g, r, a, e, ln, rects, base, tag_fill=OUT_TAG, tag_color=INK, edge=None):
    """One PDF line as lead | tag | text | tag | ... cells; rects: the tags' cell edges in order."""
    edge = edge or {}
    slots, tags = [[]], []
    for k, spans in groups(ln):
        if k:
            tags.append(spans)
            slots.append([])
        else:
            slots[-1].extend(spans)
    assert len(tags) == len(rects), (ln["text"], len(tags))
    bounds = [a] + [x for t in rects for x in t] + [e]
    for i, spans in enumerate(slots):
        x0, x1 = bounds[2 * i], bounds[2 * i + 1]
        if x1 - x0 < 0.5:
            continue
        side = {k: v for k, v in edge.items()
                if not (k == "left" and i > 0) and not (k == "right" and i < len(slots) - 1)}
        if not "".join(s["text"] for s in spans).strip():
            g.put(x0, x1, r, r + 1, [], frame(**side))
            continue
        runs = runs_of(dict(spans=spans))
        text = "".join(t for t, *_ in runs)
        if i == 0 and text in ("∙", "-"):
            g.put(x0, x1, r, r + 1, [runs], frame(**side), align="RIGHT", fit=False)
            tight(g, x0, r, 0, 120)
        elif i == 0:
            g.put(x0, x1, r, r + 1, hang([dict(bbox=(spans[0]["bbox"][0],), spans=spans)], base),
                  frame(**side), align="LEFT")
        else:
            g.put(x0, x1, r, r + 1, [runs], frame(**side), align="LEFT")
            tight(g, x0, r, 0, 100)
    for (t0, t1), spans in zip(rects, tags):
        g.put(t0, t1, r, r + 1, [runs_of(dict(spans=spans), tag_color)], tag_fill, line=1000)
        tight(g, t0, r)


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

g = Grid("sec3", [X0, 84.5, X1], [2300])
g.put(X0, 84.5, 0, 1, [runs_of(line1(64, 70, 73, 78), WHITE)], frame(DARK), line=1700)
g.put(84.5, X1, 0, 1, [line1(90, 95, 74, 78)], frame("#E6E6E6"), align="LEFT", line=1700)
block(g, 70.9)

# 추진목표: outlined box, bullet text and a gray tag inside it.
g = Grid("goal", [X0, 105.4, 107.6, 430.3, 512.8, X1], [550, 1450, 580])
g.put(X0, 105.4, 0, 3, [line1(60, 65, 106, 110)], HATCHED)
ln = line1(112, 115, 106, 110)
g.put(107.6, 430.3, 0, 3, [runs_of(ln, x1=431.0)], frame(top="mid", bottom="mid", left="mid"), align="LEFT")
g.put(430.3, 512.8, 0, 1, [], frame(top="mid"))
g.put(430.3, 512.8, 1, 2, [runs_of(ln, x0=431.0)], frame("#D9D9D9"), line=1050, fit=False)
tight(g, 430.3, 1)
g.put(430.3, 512.8, 2, 3, [], frame(bottom="mid"))
g.put(512.8, X1, 0, 3, [], frame(top="mid", bottom="mid", right="mid"))
block(g, 100.2)

# 추진방향: three chevron segments: dark number square, title, dark tag.
SEG = ((112.2, 124.9, 197.0, 245.5, 250.1, "#EBEBEB"), (264.2, 275.3, 336.4, 399.1, 402.1, "#D6D6D6"),
       (416.2, 427.5, 488.2, 550.9, 554.0, "#EBEBEB"))
xs = sorted({X0, 105.4, X1} | {x for s in SEG for x in s[:5]})
g = Grid("direction", xs, [400, 1530, 400])
g.put(X0, 105.4, 0, 3, [line1(60, 65, 136, 140)], HATCHED)
for k, (a, n1, t0, t1, e, fill) in enumerate(SEG):
    ln = line1(n1 + 1, n1 + 3, 136, 140)
    g.put(a, e, 0, 1, [], frame(fill))
    g.put(a, e, 2, 3, [], frame(fill))
    g.put(a, n1, 1, 2, str(k + 1), frame("#333333"), size=1000, bold=True, color=WHITE, line=1050, fit=False)
    tight(g, a, 1)
    g.put(n1, t0, 1, 2, [runs_of(ln, x1=t0)], frame(fill), align="LEFT", line=1250)
    tight(g, n1, 1, 100, 0)
    g.put(t0, t1, 1, 2, [runs_of(ln, WHITE, x0=t0 - 1)], frame("#8A8A8A"), line=1000)
    tight(g, t0, 1)
    g.put(t1, e, 1, 2, [], frame(fill))
    if k < 2:
        g.put(e, SEG[k + 1][0], 0, 3, "▶", size=900, color="#B0B0B0", fit=False)
block(g, 131.2)

# 세부과제: outlined box with three bullet columns.
C = ((107.6, 257.3), (257.3, 406.2), (406.2, X1))
g = Grid("tasks", [X0, 105.4] + [c[0] for c in C] + [X1], [4030])
g.put(X0, 105.4, 0, 1, [line1(60, 65, 172, 177)], HATCHED)
for k, (a, e) in enumerate(C):
    edges = dict(top="mid", bottom="mid", left="mid" if k == 0 else None, right="mid" if k == 2 else "soft")
    g.put(a, e, 0, 1, hang(lines_in(a, e, 165, 195), a + 6), frame(**edges), align="LEFT", line=1550)
block(g, 159.4)


# ---------------------------------------------------------------------------
# 가. 나. 다. tables: 구분 | 내용 | 주요 실적 (주요 실적 column framed in dark)
# ---------------------------------------------------------------------------
K0, K1, K2 = 79.4, 102.1, 374.2


def table_head(g, y):
    hf = frame(HEAD, top="mid", bottom="soft")
    g.put(X0, K1, 0, 1, [line1(60, 75, y - 1, y + 2)], hf)
    g.put(K1, K2, 0, 1, [line1(220, 230, y - 1, y + 2)], frame(HEAD, top="mid", bottom="soft", left="soft"))
    g.put(K2, X1, 0, 1, [line1(440, 450, y - 1, y + 2)], frame("#7F7F7F", top="strong", left="strong",
                                                                right="strong", bottom="soft"), color=WHITE)


def res(g, r0, r1, lines, last=False, line=1600):
    g.put(K2, X1, r0, r1, hang(lines, 377.2), frame(left="strong", right="strong",
                                                     bottom="strong" if last else "soft"), align="LEFT", line=line)


def body(g, r0, r1, lines, bottom=True, line=1600):
    g.put(K1, K2, r0, r1, hang(lines, 105.1), frame(left="soft", bottom="soft" if bottom else None), align="LEFT",
          line=line)


ROW_T = ((112.9, 147.2),)


def title_badge(name, line, edges, top, sticker=None):
    runs = runs_of(line)
    g = Grid(name, edges, [1650])
    g.put(edges[0], edges[1], 0, 1, [strip_runs(runs[:1])], align="LEFT", line=1450)
    g.put(edges[1], edges[2], 0, 1, [runs[1]], frame("#E3E3E3", top="soft", bottom="soft", left="soft",
                                                     right="soft"))
    g.put(edges[2], edges[3], 0, 1, [strip_runs(runs[2:])], align="LEFT", line=1450)
    if sticker:
        g.put(edges[3], edges[4], 0, 1, sticker, frame("#3C3C3C"), size=800, bold=True, color=WHITE, line=950)
        tight(g, edges[3], 0, 40, 40)
    block(g, top)


# 가.
title_badge("title-ga", line1(55, 60, 210, 214), [X0, 76.9, 160.1, X1], 210.5)
ys = [233.3, 251.7, 270.5, 287.5, 306.6, 344.3, 363.0, 380.0, 399.6]
tag_x = {120.0, 167.1, 112.9, 147.2, 352.6, 371.4}
g = Grid("table-ga", sorted({X0, K0, K1, K2, X1} | tag_x), [int(round((b - a) * 100)) for a, b in zip(ys, ys[1:])])
table_head(g, 238)
g.put(X0, K0, 1, 5, [line1(58, 60, 292, 296)], frame(SIDE, bottom="soft"))
g.put(K0, K1, 1, 4, lines_in(80, 85, 265, 285), frame(SIDE, bottom="soft"), line=1250)
g.put(K0, K1, 4, 5, lines_in(80, 85, 311, 330), frame(SIDE, bottom="soft"), line=1250)
g.put(X0, K1, 5, 8, lines_in(60, 75, 358, 376), frame(SIDE), line=1250)
body(g, 1, 2, [line1(104, 106, 255, 259)], bottom=False)
tagged(g, 2, K1, K2, line1(104, 106, 272, 276), ((120.0, 167.1),), 105.1, edge=dict(left="soft"))
tagged(g, 3, K1, K2, line1(104, 106, 289, 293), ((120.0, 167.1),), 105.1, edge=dict(left="soft", bottom="soft"))
body(g, 4, 5, lines_in(104, 106, 310, 330))
tagged(g, 5, K1, K2, line1(104, 106, 348, 352), ROW_T, 105.1, edge=dict(left="soft"))
tagged(g, 6, K1, K2, line1(104, 106, 365, 369), ROW_T, 105.1, edge=dict(left="soft"))
tagged(g, 7, K1, K2, line1(104, 106, 382, 386), ROW_T + ((352.6, 371.4),), 105.1, edge=dict(left="soft"))
res(g, 1, 4, lines_in(376, 390, 252, 300), line=1700)
res(g, 4, 5, lines_in(376, 390, 310, 330), line=1500)
res(g, 5, 8, lines_in(376, 390, 348, 390), last=True, line=1700)
block(g, 233.3)

# 나.
title_badge("title-na", line1(55, 60, 411, 414), [X0, 76.9, 160.1, X1], 410.9)
ys = [433.8, 452.1, 487.0, 504.5, 523.2, 542.0, 558.5, 577.8]
g = Grid("table-na", sorted({X0, K1, K2, X1, 352.7, 371.5, 320.5, 339.2, 524.2, 543.0}),
         [int(round((b - a) * 100)) for a, b in zip(ys, ys[1:])])
table_head(g, 438)
g.put(X0, K1, 1, 4, [line1(60, 62, 481, 485)], frame(SIDE, bottom="soft"))
g.put(X0, K1, 4, 7, [line1(60, 62, 544, 548)], frame(SIDE))
body(g, 1, 2, lines_in(104, 106, 456, 476), bottom=False, line=1650)
tagged(g, 2, K1, K2, line1(104, 106, 489, 493), ((352.7, 371.5),), 105.1, edge=dict(left="soft"))
body(g, 3, 4, [line1(104, 106, 506, 510)])
tagged(g, 4, K1, K2, line1(104, 106, 525, 529), ((320.5, 339.2),), 105.1, DARK_TAG, WHITE,
       edge=dict(left="soft"))
body(g, 5, 7, lines_in(104, 106, 544, 565), bottom=True, line=1650)
res(g, 1, 4, lines_in(376, 390, 455, 510), line=1700)
res(g, 4, 5, [line1(376, 378, 524, 528)])
tagged(g, 5, K2, X1, line1(376, 378, 543, 547), ((524.2, 543.0),), 377.2, edge=dict(left="strong",
                                                                                    right="strong"))
res(g, 6, 7, [line1(376, 378, 558, 562)], last=True)
block(g, 433.8)

# 다.
title_badge("title-da", line1(55, 60, 589, 593), [X0, 75.8, 158.9, 503.9, X1], 589.2, sticker="지적사항 개선")
ys = [612.0, 630.4, 651.0, 665.0, 682.0, 701.6, 739.7]
g = Grid("table-da", sorted({X0, K1, K2, X1, 112.9, 147.2}), [int(round((b - a) * 100)) for a, b in zip(ys, ys[1:])])
table_head(g, 616)
g.put(X0, K1, 1, 5, lines_in(60, 70, 652, 682), frame(SIDE, bottom="soft"), line=1300)
mixed = line1(60, 62, 706, 710)          # '인사교류' label and the first bullet share one PDF line
g.put(X0, K1, 5, 6, [runs_of(mixed, x1=100.0)], frame(SIDE))
tagged(g, 1, K1, K2, line1(104, 106, 636, 640), ROW_T, 105.1, edge=dict(left="soft"))
body(g, 2, 3, [line1(101, 103, 653, 657)], bottom=False, line=1100)
tagged(g, 3, K1, K2, line1(104, 106, 666, 670), ROW_T, 105.1, edge=dict(left="soft"))
body(g, 4, 5, [line1(104, 106, 683, 687)])
g.put(K1, K2, 5, 6, [runs_of(mixed, x0=100.0), runs_of(line1(104, 106, 722, 726))], frame(left="soft"),
      align="LEFT", line=1650)
res(g, 1, 5, lines_in(376, 390, 634, 690), line=1650)
res(g, 5, 6, lines_in(376, 390, 705, 730), last=True, line=1650)
block(g, 612.0)

# 주요성과
g = Grid("result", [X0, 111.7, 114.7, X1], [5550])
g.put(X0, 111.7, 0, 1, [runs_of(line1(65, 70, 767, 772), WHITE)], frame(DARK))
g.put(114.7, X1, 0, 1, lines_in(116, 120, 748, 790), frame(top="mid", bottom="mid", left="mid", right="mid"),
      align="LEFT", line=1550)
block(g, 746.3)

kit.finish(target, end=802.0)
