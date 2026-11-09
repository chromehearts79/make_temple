"""Rebuild KDN 2025 report physical PDF page 15 (printed page 3): 4 성과목표 및 성과지표 설정.

Usage: python3 work/kdn2025/p15.py <report.pdf> <out.hwpx> [--page N]

가. 계량 성과지표 table (vector-drawn in the PDF) and 나. 비계량 table, laid out with the shared
kit (work/kdn2025/kit.py) on the PDF's own column and row edges. Text is taken cell by cell
from the PDF text layer with its spans; lines that the PDF joins across two columns
("BestHRD 인증(인증)", the two bullets of the last 비계량 row) are split by span x.
The small 강화/개선/신규/복합지표 tags are white boxes in the PDF; they stay text runs inside
their cells and get a Hancom character border (charPr borderFillIDRef, 글자 테두리) with a
white background. The section band, side tab and table header shading are images in the PDF.
"""

import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kit  # noqa: E402
from kit import Layout, recipe_inputs  # noqa: E402

source, target = recipe_inputs(15, "성과목표 및 성과지표 설정")
L = Layout(top=3100)
kit.setup(source, L)
from kit import *  # noqa: E402,F401,F403  helpers and presets bound to this page

TAGS = {"강화", "개선", "신규", "복합지표"}
SHADE = "#ECECEC"     # 성과지표 column and '25 비계량 cells (PDF fill 0.925)
HEAD = "#D8D8D8"      # header fill (PDF fill 0.847)
HEAD25 = "#7F7F7F"    # '25 header fill (PDF fill 0.498)


def cell_runs(x0, x1, y0, y1, indent_from=None):
    """Runs of every PDF line in y0..y1 that has a span starting in x0..x1, cut to that x range
    (one PDF line may run across two cells). indent_from: keep the PDF's leading blanks."""
    out = []
    for line in sorted(kit.LINES, key=lambda l: (l["bbox"][1], l["bbox"][0])):
        if not y0 <= line["bbox"][1] < y1:
            continue
        if not any(x0 <= s["bbox"][0] < x1 and s["text"].strip() for s in line["spans"]):
            continue
        runs = runs_of(line, x0=x0, x1=x1)
        if indent_from is not None:
            raw = "".join(s["text"] for s in line["spans"] if x0 <= s["bbox"][0] < x1)
            lead = len(raw) - len(raw.lstrip()) + int(round((line["bbox"][0] - indent_from) / 3.3))
            if lead > 0:
                runs = [(" " * lead + runs[0][0], *runs[0][1:])] + runs[1:]
        out.append(runs)
    return out


def tag_borders():
    """Give the 강화/개선/신규/복합지표 runs a boxed, white-backed character style."""
    edge = deepcopy(L.borders[0])
    for side in ("left", "right", "top", "bottom"):
        b = L.get(edge, f"hh:{side}Border")
        b.set("type", "SOLID"), b.set("width", "0.12 mm"), b.set("color", "#3C3C3C")
    L.sub(L.sub(edge, "hc:fillBrush"), "hc:winBrush", faceColor=WHITE, hatchColor="#E1E1E1", alpha="0")
    box = L.append_style(L.borders, edge)
    made = {}
    for run in L.section.iter(L.q("hp:run")):
        t = run.find(L.q("hp:t"))
        if t is None or (t.text or "").strip() not in TAGS:
            continue
        ref = run.get("charPrIDRef")
        if ref not in made:
            el = deepcopy(L.characters.find(f"hh:charPr[@id='{ref}']", L.ns))
            el.set("borderFillIDRef", box)
            made[ref] = L.append_style(L.characters, el)
        run.set("charPrIDRef", made[ref])
        t.text = " " + t.text.strip() + " "


# ---------------------------------------------------------------------------
# Page chrome: odd page -> running head over a rule, side tab, footer at the right.
# ---------------------------------------------------------------------------
L.add_table([[cell(0, 3350, 1680, [para([("01", 1380, True, WHITE)], "CENTER")[0]], dark)],
             [cell(0, 3350, 5960, [para([(ch, 950, True, INK)], "CENTER", 1160)[0] for ch in "경영관리"], gray2)]],
            floating=(57800, 15000))
foot = [(only_text, size, False, INK) for only_text, size in (
    (line1(450, 455, 818, 822)["text"], 790), ("    ", 790), (line1(545, 552, 816, 820)["text"], 1090))]
L.add_table([[cell(0, W, 1500, [para(foot, "RIGHT", 1300)[0]])]], floating=(5660, 81550))

g = Grid("head", [X0, 466.3, X1], [1680])
g.put(X0, 466.3, 0, 1, [], frame(bottom="soft"))
g.put(466.3, X1, 0, 1, [line1(465, 480, 35, 40)], align="RIGHT")
block(g, 32.0)

# Section band: dark number square + light band (an image in the PDF).
g = Grid("section", [X0, 85.0, X1], [2300])
g.put(X0, 85.0, 0, 1, [line1(60, 70, 72, 76)], dark, color=WHITE, line=1850)
g.put(85.0, X1, 0, 1, [line1(85, 95, 72, 76)], frame("#E4E4E4", top="soft", bottom="soft"),
      align="LEFT", line=1750)
block(g, 70.9)

g = Grid("heading-ga", [X0, X1], [1800])
g.put(X0, X1, 0, 1, [line1(55, 60, 100, 105)], align="LEFT", line=1600)
block(g, 101.0)

# ---------------------------------------------------------------------------
# 가. 계량 성과지표: 성과지표 | 단위 | '24년 실적 | '25년 목표 | 목표설정 수준 및 근거
# ---------------------------------------------------------------------------
XG, XS, XU, X24, X25, XR = 102.1, 170.1, 201.2, 241.0, 280.6, X1
rows_y = [123.2, 160.1, 213.8, 250.9, 288.0, 325.2, 345.8, 380.5, 414.9, 449.6, 483.9, 518.7,
          553.1, 587.7, 608.4, 643.1]
hs = [int(round((b - a) * 100)) for a, b in zip(rows_y, rows_y[1:])]
g = Grid("kpi-table", [X0, XG, XS, XU, X24, X25, XR], hs)
head = frame(HEAD, top="strong", bottom="soft", right="soft")
head25 = frame(HEAD25, top="strong", bottom="soft", left="strong", right="strong")
g.put(X0, XS, 0, 1, cell_runs(X0, XS, 130, 150), head)
g.put(XS, XU, 0, 1, cell_runs(XS, XU, 130, 150), head)
g.put(XU, X24, 0, 1, cell_runs(XU, X24, 125, 158), head, line=1300)
g.put(X24, X25, 0, 1, [[(t, s, b, WHITE) for t, s, b, _ in r] for r in cell_runs(X24, X25, 125, 158)],
      head25, line=1300)
g.put(X25, XR, 0, 1, cell_runs(X25, XR, 130, 150), frame(HEAD, top="strong", bottom="soft"))


def values(r0, r1, y0, y1, last=False):
    """단위 | '24 | '25 cells of one (sub)row."""
    bottom = "mid" if last else "soft"
    g.put(XS, XU, r0, r1, cell_runs(XS, XU, y0, y1), frame(bottom=bottom, right="soft"))
    g.put(XU, X24, r0, r1, cell_runs(XU, X24, y0, y1), frame(bottom=bottom))
    g.put(X24, X25, r0, r1, cell_runs(X24, X25, y0, y1),
          frame(bottom="strong" if last else "soft", left="strong", right="strong"))


def reasons(r0, r1, y0, y1, last=False):
    g.put(X25, XR, r0, r1, cell_runs(279.0, XR, y0, y1, indent_from=283.6),
          frame(bottom="mid" if last else "soft"), align="LEFT", line=1650)


# Single indicators (rows 1-4): name (with its tag) across both 성과지표 sub-columns.
for r in range(1, 5):
    y0, y1 = rows_y[r], rows_y[r + 1]
    g.put(X0, XS, r, r + 1, [[x for runs in cell_runs(X0, XS, y0, y1) for x in runs]],
          frame(SHADE, bottom="soft"))
    values(r, r + 1, y0, y1)
    reasons(r, r + 1, y0, y1)

# Composite indicators (rows 5-14): group label + 복합지표 tag, two sub-indicators each.
for r in range(5, 15, 2):
    y0, ym, y1 = rows_y[r], rows_y[r + 1], rows_y[r + 2]
    last = r == 13
    bottom = "mid" if last else "soft"
    g.put(X0, XG, r, r + 2, cell_runs(X0, XG, y0, y1), frame(SHADE, bottom=bottom, right="soft"), line=1380)
    g.put(XG, XS, r, r + 1, cell_runs(XG, XS, y0, ym), frame(SHADE, bottom="soft"), line=1380)
    g.put(XG, XS, r + 1, r + 2, cell_runs(XG, XS, ym, y1), frame(SHADE, bottom=bottom), line=1270)
    values(r, r + 1, y0, ym)
    values(r + 1, r + 2, ym, y1, last)
    reasons(r, r + 2, y0, y1, last)
block(g, 123.2)

g = Grid("heading-na", [X0, X1], [1800])
g.put(X0, X1, 0, 1, [line1(55, 60, 652, 658)], align="LEFT", line=1600)
block(g, 653.5)

# ---------------------------------------------------------------------------
# 나. 비계량 성과지표: three columns with 4 pt gutters, '25 column shaded.
# ---------------------------------------------------------------------------
xs = [X0, 220.3, 224.3, 388.1, 392.0, X1]
g = Grid("non-kpi-table", xs, [2060, 5950, 4340])
cols = [(X0, 220.3, 59.7), (224.3, 388.1, 227.3), (392.0, X1, 395.0)]
for k, (a, e, bx) in enumerate(cols):
    fill = frame(HEAD25 if k == 2 else HEAD, top="strong", left="soft", right="soft")
    runs = cell_runs(a, e, 676, 690)
    if k == 2:
        runs = [[(t, s, b, WHITE) for t, s, b, _ in r] for r in runs]
    g.put(a, e, 0, 1, runs, fill)
    body = SHADE if k == 2 else None
    g.put(a, e, 1, 2, cell_runs(a, e, 700, 755, indent_from=bx), frame(body, bottom="dot" if k < 2 else None),
          align="LEFT", line=1650)
    g.put(a, e, 2, 3, cell_runs(a, e, 760, 799, indent_from=bx), frame(body, top="soft" if k == 2 else None,
                                                                       bottom="mid"),
          align="LEFT", line=1650)
block(g, 675.6)

tag_borders()
kit.finish(target, end=803.0)
