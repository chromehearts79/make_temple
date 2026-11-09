"""Rebuild KDN 2025 report page 72 (second PDF local page 22, printed page 46) as editable HWPX.

Usage: python3 work/kdn2025/p72.py <report2.pdf> <out.hwpx> [--page 22]

친환경·탄소중립 section 3 (친환경 에너지ICT 플랫폼). Built with the shared kit: one flat table per
horizontal band on a grid of PDF x edges. All text is in the PDF text layer except the
'Best Practice' badge and the '지적사항 개선' sticker (images; typed as dark tags). The weather /
power-grid illustrations of 가. are omitted (their area stays blank); the (+) joint becomes "+",
chevrons become ▼. Inline boxed tags (AI 예측, 통합관리, 국내최대, 기술력, 공공성, 수소E ...) are
separate bordered cells; the text cell that follows a tag starts on the tag's sub-row and is top
aligned so both read as one line.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kit  # noqa: E402
from kit import Layout, recipe_inputs  # noqa: E402

source, target = recipe_inputs(22, "재생에너지 전환을 위한 친환경 에너지ICT 플랫폼 확산")
L = Layout(top=3100)
kit.setup(source, L)
from kit import *  # noqa: E402,F401,F403  helpers and presets bound to this page

DARK, LABEL, HEAD = "#6A6A6A", "#E6E6E6", "#D9D9D9"
TAG = frame(WHITE, top="soft", bottom="soft", left="soft", right="soft")
TOP = []


def put(g, x0, x1, r0, r1, content, fill="1", *, top=False, **kw):
    """Grid.put; top=True aligns the cell's text to the top (text that follows a tag cell)."""
    g.put(x0, x1, r0, r1, content, fill, **kw)
    if top:
        TOP.append(g.items[r0, g.xs.index(to_x(x0))][3][0])


def hang(lines, base):
    """Bullet lines keep their PDF indent: spaces for the x offset."""
    out = []
    for l in lines:
        runs = runs_of(l)
        n = max(0, round((l["bbox"][0] - base) / (0.29 * runs[0][1] / 100)))
        out.append([(" " * n, runs[0][1], False, INK)] + runs if n else runs)
    return out


def section_band(name, num_line, title_line, top):
    g = Grid(name, [X0, 84.5, X1], [2300])
    g.put(X0, 84.5, 0, 1, [runs_of(num_line, WHITE)], frame(DARK), line=1700)
    g.put(84.5, X1, 0, 1, [runs_of(title_line)], frame(LABEL), align="LEFT", line=1700)
    block(g, top)


def titled(name, line, x0, x1, top, tag, size=850):
    """'가. title' heading (14pt) followed by a dark tag (an image in the PDF)."""
    g = Grid(name, [X0, x0, x1, X1], [1650])
    g.put(X0, x0, 0, 1, [line], align="LEFT", line=1450)
    g.put(x0, x1, 0, 1, tag, frame("#3C3C3C"), size=size, bold=True, color=WHITE, line=1000)
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

section_band("sec3", line1(60, 70, 72, 76), line1(90, 95, 73, 77), 70.9)

g = Grid("background", [X0, 111.7, X1], [3140])
g.put(X0, 111.7, 0, 1, [line1(65, 70, 112, 116)], frame("#D5D5D5", top="mid", bottom="mid", left="mid"))
g.put(111.7, X1, 0, 1, lines_in(115, 120, 104, 125), frame(top="mid", bottom="mid", right="mid"), align="LEFT",
      line=1490)
block(g, 103.0)

# ---------------------------------------------------------------------------
# 가. 전력 흐름 내비게이션: two problem boxes (+), thesis, 3-row table
# ---------------------------------------------------------------------------
titled("title-ga", line1(55, 60, 152, 156), 462.5, 533.5, 153.0, "Best Practice")

xs = [X0, 145.0, 298.7, 313.3, 470.0, X1]
g = Grid("problems", xs, [1830, 5000])
g.put(X0, 298.7, 0, 1, [line1(110, 120, 177, 182)], frame(HEAD, top="mid", left="mid", right="mid"))
g.put(313.3, X1, 0, 1, [line1(370, 375, 177, 182)], frame(HEAD, top="mid", left="mid", right="mid"))
g.put(X0, 145.0, 1, 2, [], frame(left="mid", bottom="mid"))      # illustration omitted
g.put(145.0, 298.7, 1, 2, lines_in(150, 160, 203, 225), frame(right="mid", bottom="mid"), line=1540)
g.put(298.7, 313.3, 1, 2, "+", size=1300, bold=True, color="#9A9A9A", fit=False)
g.put(313.3, 470.0, 1, 2, lines_in(320, 335, 203, 225), frame(left="mid", bottom="mid"), line=1540)
g.put(470.0, X1, 1, 2, [], frame(right="mid", bottom="mid"))      # illustration omitted
block(g, 175.0)

g = Grid("thesis", [X0, X1], [1350, 1250])
g.put(X0, X1, 0, 1, [line1(85, 90, 248, 252)], line=1190)
g.put(X0, X1, 1, 2, "▼", size=900, color="#8A8A8A", line=1000, fit=False)
block(g, 247.5)

# Table: label (pill + lines) | 추진 내용 (gray pill, AI 예측 / 통합관리 tagged lines) | 추진성과
xs = [X0, 68.7, 106.0, 119.3, 124.3, 159.3, 427.7, 431.0, 465.0, X1]
GROUP = [None, 450, 1150, 400, 400, 1300, 300, 1300, 300, None]    # rows stay >= 2.6 pt (cell padding + 1 pt line)
pads = ((720, 520), (680, 550), (650, 580))
hs = [1830]
for top_pad, bottom_pad in pads:
    hs += [top_pad] + GROUP[1:-1] + [bottom_pad]
g = Grid("ga-table", xs, hs)
head = frame(HEAD, top="mid")
g.put(X0, 119.3, 0, 1, [line1(75, 80, 282, 287)], head)
g.put(119.3, 431.0, 0, 1, [line1(250, 260, 282, 287)], head)
g.put(431.0, X1, 0, 1, [line1(470, 480, 282, 287)], head)
groups = [
    dict(pill=(75, 80, 312, 316), label=(60, 115, 325, 345), need=(150, 155, 309, 313), ai=330, mg=347,
         result=(430, 445, 310, 350)),
    dict(pill=(70, 75, 373, 377), label=(60, 115, 386, 420), need=(160, 165, 377, 381), ai=398, mg=415,
         tagged=(433, 440, 379, 383), result=(430, 445, 394, 415)),
    dict(pill=(75, 80, 449, 452), label=(60, 115, 462, 480), need=(158, 162, 445, 449), ai=466, mg=483,
         result=(440, 460, 446, 482))]
lab = frame(LABEL)
for k, d in enumerate(groups):
    b = 1 + 10 * k                                   # first row of the group
    sep = dict(bottom="soft")
    g.put(X0, 119.3, b, b + 2, [], lab)
    g.put(X0, 68.7, b + 2, b + 3, [], lab)
    g.put(68.7, 106.0, b + 2, b + 3, [line1(*d["pill"])], TAG, line=950)
    g.put(106.0, 119.3, b + 2, b + 3, [], lab)
    g.put(X0, 119.3, b + 3, b + 10, lines_in(*d["label"]), frame(LABEL, **sep), line=1350)
    g.put(124.3, 427.7, b + 1, b + 4, [line1(*d["need"])], frame("#DADADA"))
    for r, y in ((b + 5, d["ai"]), (b + 7, d["mg"])):
        ln = line1(120, 125, y, y + 3)
        g.put(124.3, 159.3, r, r + 1, [runs_of(ln, x1=158.0)], TAG, line=950)
        put(g, 159.3, 431.0, r, r + 2, [strip_runs(runs_of(ln, x0=158.0))], align="LEFT", top=True, line=1260)
    g.put(119.3, 431.0, b + 9, b + 10, [], frame(**sep))
    if "tagged" in d:
        ln = line1(*d["tagged"])
        g.put(431.0, X1, b, b + 2, [], frame(left="soft"))
        g.put(431.0, 465.0, b + 2, b + 3, [runs_of(ln, x1=466.0)], TAG, line=950)
        put(g, 465.0, X1, b + 2, b + 4, [strip_runs(runs_of(ln, x0=466.0))], align="LEFT", top=True, line=1260)
        g.put(431.0, 465.0, b + 3, b + 4, [], frame(left="soft"))
        g.put(431.0, X1, b + 4, b + 9, lines_in(*d["result"]), frame(left="soft"), line=1500)
        g.put(431.0, X1, b + 9, b + 10, [], frame(left="soft", **sep))
    else:
        g.put(431.0, X1, b, b + 10, lines_in(*d["result"]), frame(left="soft", **sep), line=1540)
block(g, 280.0)

# ---------------------------------------------------------------------------
# 나. CHA-ON 확산 및 VGI: two problem→solution boxes
# ---------------------------------------------------------------------------
titled("title-na", line1(55, 60, 518, 522), 487.5, 540.5, 519.0, "지적사항 개선", size=800)
g = Grid("footnote", [X0, X1], [1300])
g.put(X0, X1, 0, 1, [line1(55, 60, 539, 543)], align="LEFT", line=1140)
block(g, 539.5)

LEFT, RIGHT = (X0, 84.3, 118.7, 96.0, 304.3), (307.7, 345.4, 380.0, 347.7, X1)
xs = sorted({X0, 84.3, 96.0, 118.7, 304.3, 307.7, 345.4, 347.7, 380.0, X1})
g = Grid("cha-on", xs, [550, 1150, 460, 2500, 840, 2160, 4170, 4050, 4120])
for a, t0, t1, lab_end, e in (LEFT, RIGHT):
    x = a + 3
    side_l, side_r = dict(left="mid"), dict(right="mid")
    head = line1(t0 + 2, t0 + 8, 561, 565)
    g.put(a, t0, 0, 3, [], frame(top="mid", **side_l))
    g.put(t0, t1, 0, 1, [], frame(top="mid"))
    g.put(t0, t1, 1, 2, [runs_of(head, x1=t1 - 4)], TAG, line=950)
    g.put(t0, t1, 2, 3, [], "1")
    g.put(t1, e, 0, 1, [], frame(top="mid", **side_r))
    put(g, t1, e, 1, 3, [strip_runs(runs_of(head, x0=t1 - 4))], frame(**side_r), align="LEFT", top=True, line=1260)
    g.put(a, e, 3, 4, [line1(x, x + 20, 585, 590)], frame("#EBEBEB", hatch="#DEDEDE", **side_l, **side_r))
    g.put(a, e, 4, 5, "▼", frame(**side_l, **side_r), size=600, color="#555555", line=680, fit=False)
    g.put(a, e, 5, 6, [line1(x, x + 25, 615, 620)], frame("#D3D3D3", **side_l, **side_r))
    for r, (y0, y1) in ((6, (638, 670)), (7, (679, 712))):
        g.put(a, lab_end, r, r + 1, lines_in(a, lab_end, y0, y1), frame(LABEL, **side_l), line=1430)
        g.put(lab_end, e, r, r + 1, hang(lines_in(lab_end, e, y0, y1), lab_end + 3.5),
              frame(bottom="dot" if r == 6 else None, **side_r), align="LEFT", line=1540)
    g.put(a, e, 8, 9, lines_in(a, e, 720, 742), frame("#E3E3E3", bottom="mid", **side_l, **side_r), line=1430)
block(g, 556.7)

# ---------------------------------------------------------------------------
# 주요성과 (text layer; superscripts as small runs)
# ---------------------------------------------------------------------------
g = Grid("result", [X0, 111.7, X1], [3140])
g.put(X0, 111.7, 0, 1, [runs_of(line1(65, 70, 775, 780), WHITE)], frame(DARK, top="mid", bottom="mid", left="mid"))
g.put(111.7, X1, 0, 1, lines_in(115, 120, 767, 790), frame(top="mid", bottom="mid", right="mid"), align="LEFT",
      line=1450)
block(g, 766.4)

kit.flush(803.0)
for sub in L.section.iter(L.q("hp:subList")):
    if len(sub) and any(sub[0] is first for first in TOP):
        sub.set("vertAlign", "TOP")
for number, table in enumerate(L.section.iter(L.q("hp:tbl")), 5001):
    table.set("id", str(number))
for message in WARN:
    print("WARN", message)
print(L.write(target))
