"""Rebuild KDN 2025 report physical PDF page 43 (printed page 28) as editable HWPX.

Usage: python3 work/kdn2025/p43.py <report.pdf> <out.hwpx> [--page N]

윤리경영 평가내용 03, 다. 인권영향평가 and section 3 (지역 사회·공급망 인권경영). Built with the
shared diagram kit (one flat table per horizontal band on a grid of PDF x edges); all text comes
from the PDF text layer. Images: boxed / filled step numbers become ①②③, the circled arrows and
chevrons become ▶ / ▼, the 'NEW 신규' and 'Best Practice' stickers are typed as dark tags (the
'NEW' flourish and trophy icon dropped), the side tab and section number band are typed.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kit  # noqa: E402
from kit import Layout, recipe_inputs  # noqa: E402

source, target = recipe_inputs(43, "지역 사회와 공급망을 아우르는 KDN")
L = Layout(top=3100)
kit.setup(source, L)
from kit import *  # noqa: E402,F401,F403  helpers and presets bound to this page

DARK, LABEL = "#6A6A6A", "#E6E6E6"
BOX = dict(top="soft", bottom="soft", left="soft", right="soft")


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


def numbered(mark, line, color=INK):
    """Step titles whose number is an image in the PDF: typed as a circled digit run."""
    runs = runs_of(line, color)
    return [(mark + " ", runs[0][1], True, color)] + runs


def heading(name, line, top, tag=None, tag_x=None, tag_w=0):
    """'다. / 가. title' line (14pt bold) with an optional typed sticker."""
    xs = [X0, tag_x, tag_x + tag_w, X1] if tag else [X0, X1]
    g = Grid(name, xs, [1650])
    g.put(X0, tag_x if tag else X1, 0, 1, [line], align="LEFT", line=1450)
    if tag:
        g.put(tag_x, tag_x + tag_w, 0, 1, tag, frame("#3C3C3C"), size=860, bold=True, color=WHITE, line=1000)
    block(g, top)


# ---------------------------------------------------------------------------
# Page chrome (odd page): running head over a rule, side tab, footer at the right.
# ---------------------------------------------------------------------------
L.add_table([[cell(0, 3350, 1680, [para([("01", 1380, True, WHITE)], "CENTER")[0]], dark)],
             [cell(0, 3350, 5960, [para([(ch, 950, True, INK)], "CENTER", 1160)[0] for ch in "경영관리"], gray2)]],
            floating=(57800, 15000))
foot = [(only_text, size, False, INK) for only_text, size in (
    (line1(450, 455, 818, 822)["text"], 790), ("    ", 790), (line1(540, 552, 816, 820)["text"], 1090))]
L.add_table([[cell(0, W, 1500, [para(foot, "RIGHT", 1300)[0]])]], floating=(5660, 81550))

g = Grid("head", [X0, 468.0, X1], [1680])
g.put(X0, 468.0, 0, 1, [], frame(bottom="soft"))
g.put(468.0, X1, 0, 1, [line1(465, 480, 35, 40)], align="RIGHT")
block(g, 32.0)

# ---------------------------------------------------------------------------
# 다. 인권영향평가: 평가과정 (three steps) and 평가결과 (two boxes + 성과 및 환류)
# ---------------------------------------------------------------------------
heading("title-da", line1(55, 60, 69, 73), 70.6)

xs = [X0, 88.0, 90.7, 245.0, 258.0, 402.7, 416.0, X1]
g = Grid("process", xs, [1870, 3520])
g.put(X0, 88.0, 0, 2, lines_in(60, 70, 105, 133), frame(LABEL, top="mid"), bold=True)
steps = ((90.7, 245.0, 130, "①", "#ECECEC"), (258.0, 402.7, 285, "②", "#E2E2E2"), (416.0, X1, 430, "③", "#D2D2D2"))
for a, e, x, mark, fill in steps:
    g.put(a, e, 0, 1, [numbered(mark, line1(x, x + 10, 94, 98))], frame(fill, top="soft"))
for a, e in ((245.0, 258.0), (402.7, 416.0)):
    g.put(a, e, 0, 1, "▶", size=800, color="#8A8A8A")
body = dict(bottom="soft")
g.put(90.7, 245.0, 1, 2, hang(lines_in(92, 105, 113, 143), 93.7), frame(right="dot", **body), align="LEFT", line=1440)
g.put(245.0, 402.7, 1, 2, hang(lines_in(248, 260, 113, 143), 250.1), frame(right="dot", **body), align="LEFT",
      line=1440)
g.put(402.7, X1, 1, 2, hang(lines_in(404, 420, 113, 143), 406.4), frame(**body), align="LEFT", line=1440)
block(g, 91.9)

xs = [X0, 88.0, 90.7, 96.5, 135.5, 147.0, 322.0, 324.5, 330.4, 369.5, X1]
g = Grid("results", xs, [2270, 1840, 1920, 410, 3530])
g.put(X0, 88.0, 0, 5, lines_in(60, 70, 185, 213), frame(LABEL, top="mid"), bold=True)
g.put(90.7, 322.0, 0, 1, [line1(185, 190, 152, 156)], frame(top="mid", left="mid", right="mid", bottom="soft"))
g.put(324.5, X1, 0, 1, [line1(400, 405, 152, 156)], frame(top="mid", left="mid", right="mid", bottom="soft"))
tag = frame("#DADADA")
for r, y in ((1, 174), (2, 190)):
    last = dict(bottom="mid") if r == 2 else {}
    row = line1(100, 101, y, y + 4)
    g.put(90.7, 96.5, r, r + 1, [], frame(left="mid", **last))
    g.put(96.5, 135.5, r, r + 1, [runs_of(row, x1=132.0)], frame("#DADADA", **{k: "soft" for k in ("top", "bottom")}))
    g.put(135.5, 322.0, r, r + 1, [strip_runs(runs_of(row, x0=132.0))], frame(right="mid", **last), align="LEFT")
row = line1(330, 335, 175, 179)
g.put(324.5, 330.4, 1, 2, [], frame(left="mid"))
g.put(330.4, 369.5, 1, 2, [runs_of(row, x1=366.0)], frame("#DADADA", top="soft", bottom="soft"))
g.put(369.5, X1, 1, 2, [strip_runs(runs_of(row, x0=366.0))], frame(right="mid"), align="LEFT")
g.put(324.5, X1, 2, 3, [line1(328, 332, 190, 194)], frame(left="mid", right="mid", bottom="mid"), align="LEFT")
g.put(90.7, 147.0, 4, 5, lines_in(100, 130, 217, 247), frame("#DCDCDC", top="mid", bottom="mid", left="mid"), bold=True,
      line=1320)
g.put(147.0, X1, 4, 5, hang(lines_in(150, 155, 217, 247), 151.9), frame(top="mid", bottom="mid", right="mid"),
      align="LEFT", line=1320)
block(g, 149.7)

# ---------------------------------------------------------------------------
# 3. 지역 사회와 공급망을 아우르는 KDN型 인권경영
# ---------------------------------------------------------------------------
g = Grid("sec3", [X0, 84.5, X1], [2300])
g.put(X0, 84.5, 0, 1, [runs_of(line1(60, 70, 267, 271), WHITE)], frame(DARK), line=1700)
g.put(84.5, X1, 0, 1, [line1(90, 95, 268, 272)], frame(LABEL), align="LEFT", line=1700)
block(g, 265.8)

heading("title-ga", line1(55, 60, 293, 297), 294.6)

xs = [X0, 88.0, 90.7, 96.5, 238.4, 241.0, 351.2, 376.2, 383.0, 388.6, 404.1, X1]
g = Grid("community", xs, [2150, 2040, 1750, 1110, 2040, 4100])
g.put(X0, 88.0, 0, 3, lines_in(55, 70, 333, 362), frame(LABEL, top="mid"), bold=True)
g.put(X0, 88.0, 3, 4, "+", size=900, bold=True, color="#7A7A7A", line=900)
g.put(X0, 88.0, 4, 6, lines_in(60, 70, 396, 438), frame(LABEL, bottom="mid"), bold=True)
g.put(90.7, 351.2, 0, 1, [line1(95, 100, 319, 323)], frame(top="soft", left="soft"), align="LEFT")
g.put(351.2, 376.2, 0, 1, "신규", frame("#3C3C3C"), size=860, bold=True, color=WHITE, line=1000)
g.put(376.2, 388.6, 0, 1, [], frame(top="soft", right="soft"))
for (a, e), mark, hx, bx in (((96.5, 238.4), "①", 125, 110), ((241.0, 383.0), "②", 270, 270)):
    g.put(a, e, 1, 2, [numbered(mark, line1(hx, hx + 5, 340, 344))], frame("#E3E3E3", top="soft", left="soft",
                                                                           right="soft"))
    g.put(a, e, 2, 3, [line1(bx, bx + 5, 358, 362)], frame(WHITE, **BOX))
g.put(90.7, 96.5, 1, 3, [], frame(left="soft", bottom="soft"))
g.put(238.4, 241.0, 1, 3, [], frame(bottom="soft"))
g.put(383.0, 388.6, 1, 3, [], frame(right="soft", bottom="soft"))
g.put(90.7, 388.6, 4, 5, [line1(120, 130, 390, 394)], frame("#DADADA", top="soft", left="soft", right="soft"))
g.put(90.7, 388.6, 5, 6, lines_in(95, 100, 410, 442), frame(left="soft", right="soft", bottom="soft"), align="LEFT",
      line=1550)
g.put(388.6, 404.1, 0, 6, "▶", size=1000, color=ARROW)
g.put(404.1, X1, 0, 1, [runs_of(line1(460, 465, 318, 322), WHITE)], frame("#6A6A6A", top="mid", left="mid", right="mid"))
g.put(404.1, X1, 1, 6, hang(lines_in(408, 420, 340, 440), 410.0), frame(left="mid", right="mid", bottom="mid"),
      align="LEFT", line=1550)
block(g, 316.1)

# ---------------------------------------------------------------------------
# 나. 협력사 인권경영: 기존 → 개선 boxes and the 추진배경 ~ 추진성과 matrix.
# ---------------------------------------------------------------------------
heading("title-na", line1(55, 60, 457, 461), 458.6, tag=[[("Best Practice", 860, True, WHITE)]],
        tag_x=453.6, tag_w=60.0)

xs = [X0, 111.0, 133.5, 299.3, 313.1, 333.2, 352.0, X1]
g = Grid("supplier", xs, [2160, 3400])
head = line1(110, 120, 483, 487)
g.put(X0, 111.0, 0, 1, [], frame("#E2E2E2", top="mid", left="mid"))
g.put(111.0, 133.5, 0, 1, [runs_of(head, x1=132.0)], frame(WHITE, **BOX))
g.put(133.5, 299.3, 0, 1, [strip_runs(runs_of(head, x0=132.0))], frame("#E2E2E2", top="mid", right="mid"), align="LEFT")
head = line1(330, 340, 483, 487)
g.put(313.1, 333.2, 0, 1, [], frame("#707070", top="mid", left="mid"))
g.put(333.2, 352.0, 0, 1, [runs_of(head, WHITE, x1=352.0)], frame("#333333"))
g.put(352.0, X1, 0, 1, [strip_runs(runs_of(head, WHITE, x0=352.0))], frame("#707070", top="mid", right="mid"),
      align="LEFT")
g.put(X0, 299.3, 1, 2, hang(lines_in(60, 65, 502, 533), 62.5), frame(left="mid", right="mid", bottom="mid"),
      align="LEFT", line=1430)
g.put(299.3, 313.1, 0, 2, "▶", size=1000, color=ARROW)
g.put(313.1, X1, 1, 2, hang(lines_in(315, 320, 502, 533), 319.1), frame(left="mid", right="mid", bottom="mid"),
      align="LEFT", line=1430)
block(g, 480.2)

xs = [X0, 105.1, 107.6, 111.9, 254.8, 258.3, 262.6, 405.4, 409.0, 413.2, 416.5, 432.3, 446.8, 462.6, X1]
hs = [3700, 410, 1570, 3740, 350, 1660, 1660, 380, 3550, 440, 3720]
g = Grid("matrix", xs, hs)
sep = dict(bottom="mid")
g.put(X0, 105.1, 0, 2, [line1(60, 65, 556, 560)], frame("#D6D6D6", **sep))
g.put(X0, 105.1, 2, 5, [line1(60, 65, 609, 613)], frame(LABEL, **sep))
g.put(X0, 105.1, 5, 10, [line1(60, 65, 677, 681)], frame("#D6D6D6", **sep))
g.put(X0, 105.1, 10, 11, [runs_of(line1(60, 65, 736, 740), WHITE)], frame("#8A8A8A"))
g.put(107.6, X1, 0, 1, hang(lines_in(110, 115, 550, 580), 113.6), frame(WHITE, top="mid", bottom="mid", left="mid",
                                                                       right="mid"), align="LEFT", line=1430)
cols = ((107.6, 111.9, 254.8, 140, "①"), (258.3, 262.6, 405.4, 290, "②"), (409.0, 413.2, X1, 455, "③"))
for i, (a, b, e, hx, mark) in enumerate(cols):
    g.put(b if i < 2 else b, e if i < 2 else X1, 2, 3, [numbered(mark, line1(hx, hx + 5, 590, 594))],
          frame("#D9D9D9", top="soft"))
    g.put(a, e, 3, 4, hang(lines_in(a, a + 6, 609, 640), a + 3.1), frame(bottom="soft"), align="LEFT", line=1430)
    g.put(a, e, 8, 9, lines_in(a, e, 684, 715), frame(WHITE, **BOX), line=1440)
    g.put(a, e, 10, 11, lines_in(a, e, 725, 756), frame("#E6E6E6", top="soft", bottom="soft"), bold=True, line=1440)
for a, b in ((107.6, 111.9), (258.3, 262.6)):
    g.put(a, b, 2, 3, [], frame(top="soft"))
hatched = frame("#EEEEEE", hatch="#E2E2E2")
g.put(107.6, 254.8, 5, 7, lines_in(107, 255, 646, 676), hatched, line=1440)
g.put(258.3, 405.4, 5, 7, lines_in(258, 405, 646, 676), hatched, line=1440)
row = line1(415, 425, 646, 650)
g.put(409.0, 416.5, 5, 6, [], hatched)
g.put(416.5, 446.8, 5, 6, [runs_of(row, WHITE, x1=446.0)], frame("#6E6E6E"))
g.put(446.8, X1, 5, 6, [strip_runs(runs_of(row, x0=446.0))], hatched, align="LEFT")
row = line1(415, 420, 661, 665)
g.put(409.0, 432.3, 6, 7, [runs_of(row, x1=434.0)], hatched)
g.put(432.3, 462.6, 6, 7, [runs_of(row, WHITE, x0=434.0, x1=462.0)], frame("#6E6E6E"))
g.put(462.6, X1, 6, 7, [strip_runs(runs_of(row, x0=462.0))], hatched, align="LEFT")
block(g, 546.8)

# 주요성과: second line starts with an inline dark badge (산업정책연구원).
g = Grid("result", [X0, 111.7, 125.8, 193.9, X1], [1800, 1910])
res1, res2 = line1(115, 120, 767, 771), line1(115, 120, 783, 787)
g.put(X0, 111.7, 0, 2, [runs_of(line1(65, 70, 776, 780), WHITE)], frame("#6A6A6A", top="mid", bottom="mid", left="mid"))
g.put(111.7, X1, 0, 1, [res1], frame(top="mid", right="mid"), align="LEFT")
g.put(111.7, 125.8, 1, 2, [runs_of(res2, x1=125.0)], frame(bottom="mid"), align="LEFT")
g.put(125.8, 193.9, 1, 2, [runs_of(res2, WHITE, x0=125.0, x1=195.0)], frame("#5E5E5E", bottom="mid"))
g.put(193.9, X1, 1, 2, [strip_runs(runs_of(res2, x0=195.0))], frame(bottom="mid", right="mid"), align="LEFT")
block(g, 764.8)

kit.finish(target, end=803.0)
