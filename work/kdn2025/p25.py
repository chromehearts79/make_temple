"""Rebuild KDN 2025 report physical PDF page 25 (printed page 13) as editable HWPX.

Usage: python3 work/kdn2025/p25.py <report.pdf> <out.hwpx> [--page N]

'5 2035 New Vision 조기 달성 ... 4대 전략방향별 가시적 성과 창출': four 전략방향 bands. Each band is
one flat table on the kit's union grid: a dark tab with the 전략방향 pill, a light title band,
three label/body rows on the left and two result panels on the right (chart or photo).
Body text comes from the PDF text layer; the ➡ arrows are images in the PDF and become "→".
Photos are empty placeholder cells; charts keep only the values printed on them (read from a
4x render): 20초/3초, 32억원/109억원, 17.3%/25.8% (계획/실적), 87.4점/90.1점, 455명/480명.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kit  # noqa: E402
from kit import Layout, recipe_inputs  # noqa: E402

source, target = recipe_inputs(25, "조기 달성을 견인하는 4대 전략방향별 가시적 성과 창출")
L = Layout(top=3100)
kit.setup(source, L)
from kit import *  # noqa: E402,F401,F403  helpers and presets bound to this page

# ---------------------------------------------------------------------------
# Page chrome (odd page): side tab, footer, running head
# ---------------------------------------------------------------------------
L.add_table([[cell(0, 3350, 1680, [para([("01", 1380, True, WHITE)], "CENTER")[0]], dark)],
             [cell(0, 3350, 5960, [para([(ch, 950, True, INK)], "CENTER", 1160)[0] for ch in "경영관리"], gray2)]],
            floating=(57800, 15000))
foot = [(only_text, size, False, INK) for only_text, size in (
    (line1(450, 455, 818, 822)["text"], 790), ("    ", 790), (line1(540, 546, 816, 820)["text"], 1090))]
L.add_table([[cell(0, W, 1500, [para(foot, "RIGHT", 1300)[0]])]], floating=(5660, 81550))

g = Grid("head", [X0, 466.3, X1], [1680])
g.put(X0, 466.3, 0, 1, [], frame(bottom="soft"))
g.put(466.3, X1, 0, 1, [line1(460, 480, 35, 40)], align="RIGHT")
block(g, 32.0)

# Section heading: dark number box + light band (images in the PDF, text in the text layer).
g = Grid("section-5", [X0, 85.6, X1], [2300])
g.put(X0, 85.6, 0, 1, [line1(60, 70, 70, 76)["text"]], frame("#5E5E5E"), size=1700, bold=True, color=WHITE)
g.put(85.6, X1, 0, 1, [line1(85, 95, 70, 76)], frame("#E4E4E4"), align="LEFT")
block(g, 70.9)

# ---------------------------------------------------------------------------
# 전략방향 bands
# ---------------------------------------------------------------------------
LAB, TAB, BODY, GUT = 108.2, 172.0, 455.1, 459.0
MID = 507.3
XS = [X0, LAB, TAB, BODY, GUT, MID, X1]
label_fill = dict(fill="#ECECEC", hatch="#E0E0E0")
PANEL = "mid"


def arrow(line):
    """'   text' second lines: the ➡ image becomes a KS X 1001 arrow."""
    return [("  → ", 1090, False, INK)] + runs_of(line)


def band(name, top, tab_y, rows, panels, badges=None):
    """rows: [(y0, y1, label_lines | label_runs, body paragraphs)], panels: two dicts.

    tab_y: y of the tab line; rows give the left box rows (y0 of the first = box top);
    panels: dict(y0, y1, title=[lines], kind='chart'|'photo', split=y, values=(a, b), axis=(a, b)).
    """
    ys = {top, rows[-1][1]}
    for y0, y1, *_ in rows:
        ys |= {y0, y1}
    for p in panels:
        ys |= {p["y0"], p["y1"], p["split"]}
        if p["kind"] == "chart":
            ys.add(p["axis_y"])
    for b in badges or []:
        ys |= {b[0], b[1]}
    edges = sorted(ys)
    xs = sorted(XS + [77.0, 90.2]) if badges else XS
    g = Grid(name, xs, [int(round((b - a) * 100)) for a, b in zip(edges, edges[1:])])
    r = edges.index
    box_top = rows[0][0]
    # Tab: pill with 전략방향N, dark tab with the direction name, light title band.
    tab = line1(55, 60, tab_y - 2, tab_y + 2)
    g.put(X0, LAB, r(top), r(box_top), [runs_of(tab, x1=103.0)],
          frame(WHITE, top="soft", bottom="soft", left="soft", right="soft"))
    g.put(LAB, TAB, r(top), r(box_top), [runs_of(tab, WHITE, x0=103.0)], frame("#6A6A6A"), align="LEFT")
    title = lines_in(150, 250, tab_y - 3, tab_y + 3)
    g.put(TAB, BODY, r(top), r(box_top), title, frame("#E2E2E2"))
    # Left box rows.
    for k, (y0, y1, label, body) in enumerate(rows):
        last = k == len(rows) - 1
        sep = "soft" if last else "dot"
        badge = badges[k] if badges else None
        if badge:
            b0, b1, letter = badge
            g.put(X0, LAB, r(y0), r(b0), [], frame(**label_fill, left="soft", top="soft" if k == 0 else None))
            g.put(X0, 77.0, r(b0), r(b1), [], frame(**label_fill, left="soft"))
            g.put(77.0, 90.2, r(b0), r(b1), [letter], frame("#5A5A5A"), size=890, bold=True, color=WHITE)
            g.put(90.2, LAB, r(b0), r(b1), [], frame(**label_fill))
            g.put(X0, LAB, r(b1), r(y1), label, frame(**label_fill, left="soft", bottom=sep), line=1300)
        else:
            g.put(X0, LAB, r(y0), r(y1), label, frame(**label_fill, left="soft", top="soft" if k == 0 else None,
                                                       bottom=sep), line=1300)
        g.put(LAB, BODY, r(y0), r(y1), body, frame(right="soft", top="soft" if k == 0 else None, bottom=sep),
              align="LEFT", line=min(1700, int((y1 - y0) * 100 - 300) // len(body) // 10 * 10))
    # Right panels.
    for p in panels:
        side = dict(left=PANEL, right=PANEL)
        g.put(GUT, X1, r(p["y0"]), r(p["split"]), p["title"], frame("#E4E4E4", top=PANEL, bottom="soft", **side),
              line=1180)
        if p["kind"] == "photo":
            g.put(GUT, X1, r(p["split"]), r(p["y1"]), [], frame("#E4E4E4", bottom=PANEL, **side))
            continue
        a, b = p["values"]
        ya, yb = p["axis"]
        g.put(GUT, MID, r(p["split"]), r(p["axis_y"]), a, frame(left=PANEL), size=900, line=1100)
        g.put(MID, X1, r(p["split"]), r(p["axis_y"]), b, frame(right=PANEL), size=900, bold=True, line=1100)
        g.put(GUT, MID, r(p["axis_y"]), r(p["y1"]), ya, frame(top="soft", bottom=PANEL, left=PANEL), size=850, line=1000)
        g.put(MID, X1, r(p["axis_y"]), r(p["y1"]), yb, frame(top="soft", bottom=PANEL, right=PANEL), size=850,
              bold=True, line=1000)
    block(g, top)


def left(y0, y1):
    return lines_in(60, 105, y0, y1)


def body(y0, y1):
    """Bullet line(s) and the arrowed second line(s) of one left-box row."""
    out = []
    for ln in lines_in(105, 112, y0, y1):
        if ln["text"].startswith("∙"):
            out.append(ln)
        elif ln["text"].startswith("*"):
            out.append([("     ", 890, False, INK)] + runs_of(ln))
        else:
            out.append(arrow(ln))
    return out


def ptitle(y0, y1):
    return lines_in(459, 556, y0, y1)


# 전략방향 1
band("dir-1", 100.2, 105.5,
     [(119.0, 169.8, left(120, 168), body(120, 168)),
      (169.8, 219.4, left(170, 218), body(170, 218)),
      (219.4, 270.6, left(220, 268), body(220, 268))],
     [dict(y0=100.2, split=129.0, axis_y=169.8, y1=184.4, title=ptitle(100, 128), kind="chart",
           values=("20초", "3초"), axis=("’24년", "’25년")),
      dict(y0=186.8, split=216.0, y1=270.6, title=ptitle(186, 215), kind="photo")])

# 전략방향 2
band("dir-2", 277.1, 282.3,
     [(296.0, 346.7, left(297, 345), body(297, 345)),
      (346.7, 396.4, left(347, 395), body(347, 395)),
      (396.4, 447.5, left(397, 446), body(397, 446))],
     [dict(y0=277.1, split=306.2, y1=360.9, title=ptitle(278, 305), kind="photo"),
      dict(y0=363.5, split=392.6, axis_y=432.5, y1=447.5, title=ptitle(364, 392), kind="chart",
           values=("32억원", "109억원"), axis=("’24년", "’25년"))])

# 전략방향 3 (E / S / G badges are small dark squares in the PDF)
band("dir-3", 453.9, 459.1,
     [(473.0, 523.5, [line1(60, 105, 498, 515)], body(474, 523)),
      (523.5, 573.2, [line1(60, 105, 548, 565)], body(524, 573)),
      (573.2, 624.3, [line1(60, 105, 597, 615)], body(574, 623))],
     [dict(y0=453.9, split=483.2, axis_y=523.5, y1=537.9, title=ptitle(455, 482), kind="chart",
           values=("17.3%", "25.8%"), axis=("계획", "실적")),
      dict(y0=540.5, split=569.7, y1=624.3, title=ptitle(541, 569), kind="photo")],
     badges=[(485.4, 498.8, line1(78, 84, 486, 489)), (535.1, 548.4, line1(78, 84, 535, 538)),
             (584.7, 597.9, line1(78, 84, 585, 588))])

# 전략방향 4: the PDF merges '경영자원' and its bullet into one text line.
merged = line1(60, 70, 708, 713)
band("dir-4", 630.9, 636.1,
     [(650.5, 700.6, left(651, 699), body(651, 699)),
      (700.6, 750.2, [runs_of(merged, x1=105.0)], [runs_of(merged, x0=105.0)] + body(712, 749)),
      (750.2, 801.2, left(751, 800), body(751, 800))],
     [dict(y0=630.9, split=660.0, axis_y=700.6, y1=714.8, title=ptitle(632, 659), kind="chart",
           values=("87.4점", "90.1점"), axis=("’24년", "’25년")),
      dict(y0=717.3, split=746.5, axis_y=787.0, y1=801.2, title=ptitle(718, 746), kind="chart",
           values=("455명", "480명"), axis=("’24년", "’25년"))])

kit.finish(target, end=803.0)
