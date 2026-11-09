"""Rebuild KDN 2025 report page 52 (second PDF local page 2, printed page 32) as editable HWPX.

Usage: python3 work/kdn2025/p52.py <report2.pdf> <out.hwpx> [--page 2]

일자리 및 균등한 기회 평가내용 02 opening page (even page). Built with the shared diagram kit (one
flat table per horizontal band on a grid of PDF x edges); all running text comes from the PDF text
layer. Images: the PART label, the 평가내용 02 chip, the '지적사항 개선' sticker (hand icon dropped),
the circled task numbers (typed ① ② ③), the ➡ arrows (typed →), the chevrons between the job
tables and the 창출실적 panels (typed ▶) and the 직접 일자리 bar chart, whose printed values
(251명↑, 2,236명, 1,985명, ’24년, ’25년; read from a 5x render, 2,236 - 1,985 = 251) become small
value cells without bars. The Kdn logo in the footer is typed as text.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kit  # noqa: E402
from kit import Layout, recipe_inputs  # noqa: E402

source, target = recipe_inputs(2, "상생의 가치를 실천하는 「민간 일자리 관리체계」 수립")
L = Layout(top=3100)
kit.setup(source, L)
from kit import *  # noqa: E402,F401,F403  helpers and presets bound to this page

DARK, LABEL = "#6A6A6A", "#E6E6E6"
HEAD = "#DADADA"
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


def lead(glyph, line, bold=False):
    """A line whose leading glyph is an image in the PDF (circled number, ➡ arrow)."""
    runs = runs_of(line)
    return [(glyph + " ", runs[0][1], bold, INK)] + runs


def section_band(name, num_line, title_line, top, sticker=None):
    """'1 | heading' band: dark number cell and light gray title cell (images in the PDF)."""
    xs = [X0, 84.5, sticker[0], sticker[1], X1] if sticker else [X0, 84.5, X1]
    g = Grid(name, xs, [2300])
    g.put(X0, 84.5, 0, 1, [runs_of(num_line, WHITE)], frame(DARK), line=1700)
    g.put(84.5, xs[2], 0, 1, [runs_of(title_line)], frame(LABEL), align="LEFT", line=1700)
    if sticker:
        g.put(sticker[0], sticker[1], 0, 1, "지적사항 개선", frame("#3C3C3C"), size=760, bold=True, color=WHITE,
              line=1000)
        g.put(sticker[1], X1, 0, 1, [], frame(LABEL))
    block(g, top)


def heading(name, line, top):
    g = Grid(name, [X0, X1], [1650])
    g.put(X0, X1, 0, 1, [line], align="LEFT", line=1450)
    block(g, top)


class Rows:
    """Row edges given as PDF y values; r(y) is the row index starting at y."""

    def __init__(self, ys):
        self.ys = sorted(set(ys))
        self.hs = [int(round((b - a) * 100)) for a, b in zip(self.ys, self.ys[1:])]

    def __call__(self, y):
        return self.ys.index(y)


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
g.put(X0, 124.0, 0, 1, [[("평가내용 ", 800, True, WHITE), ("02", 1350, True, WHITE)]], frame("#686868"),
      line=1500)
g.put(124.0, X1, 0, 1, [line1(125, 130, 76, 80)], striped, align="LEFT", line=1450)
block(g, 70.9)

# ---------------------------------------------------------------------------
# 1. 민간 일자리 관리체계: 환경분석 / 추진목표 / 추진방향·과제 / 성과지표 (text layer, boxes drawn)
# ---------------------------------------------------------------------------
section_band("sec1", line1(60, 70, 113, 118), line1(90, 95, 114, 118), 111.5)

xs = [X0, 113.6, 116.2, 261.1, 263.6, 323.4, 325.9, 408.5, 411.0, X1]
R = Rows([140.8, 160.0, 197.2, 202.3, 225.4, 230.6, 253.6, 256.1, 287.9, 293.0, 316.1])
g = Grid("system", xs, R.hs)
side = frame(LABEL, top="mid")
g.put(X0, 113.6, R(140.8), R(197.2), [line1(60, 70, 163, 168)], side, bold=True)
g.put(X0, 113.6, R(202.3), R(225.4), [line1(60, 70, 208, 212)], side, bold=True)
g.put(X0, 113.6, R(230.6), R(253.6), [line1(60, 70, 236, 240)], side, bold=True)
g.put(X0, 113.6, R(256.1), R(287.9), [line1(60, 70, 266, 270)], side, bold=True)
g.put(X0, 113.6, R(293.0), R(316.1), [line1(60, 70, 299, 303)], side, bold=True)
head = frame(HEAD, top="soft", left="soft", right="soft", bottom="soft")
body = frame(left="soft", right="soft", bottom="soft")
for a, e, hx, bx in ((116.2, 323.4, 200, 120), (325.9, X1, 420, 330)):
    g.put(a, e, R(140.8), R(160.0), [line1(hx, hx + 5, 144, 148)], head)
    g.put(a, e, R(160.0), R(197.2), lines_in(bx, bx + 5, 162, 195), body, align="LEFT", line=1530)
g.put(116.2, X1, R(202.3), R(225.4), [line1(230, 240, 207, 211)], frame(**BOX))
for a, e, hx, bx in ((116.2, 261.1, 135, 120), (263.6, 408.5, 285, 268), (411.0, X1, 425, 415)):
    g.put(a, e, R(230.6), R(253.6), [line1(hx, hx + 5, 235, 239)], head)
    g.put(a, e, R(253.6), R(287.9), lines_in(bx, bx + 5, 255, 285), body, align="LEFT", line=1530)
bar = "#EBEBEB"
for a, e, x, kw in ((116.2, 263.6, 120, dict(left="soft")), (263.6, 411.0, 268, dict(left="dot")),
                    (411.0, X1, 415, dict(left="dot", right="soft"))):
    g.put(a, e, R(293.0), R(316.1), [line1(x, x + 5, 297, 301)], frame(bar, top="soft", bottom="soft", **kw))
block(g, 140.8)

# ---------------------------------------------------------------------------
# 2. 핵심·미래성장 사업 등 본업연계 (sticker typed)
# ---------------------------------------------------------------------------
section_band("sec2", line1(60, 70, 334, 338), line1(90, 95, 335, 339), 332.4, sticker=(432.0, 486.0))
heading("title-ga", line1(55, 60, 362, 366), 362.0)

COLS = ((113.0, 227.5, 118.9), (229.9, 344.3, 235.8), (346.8, 461.3, 352.7))
XS = [X0, 110.0, 113.0, 227.5, 229.9, 344.3, 346.8, 461.3, 465.1, 479.0, 487.5, 507.8, 517.4, 549.5, X1]
TAG = frame(WHITE, **BOX)
PANEL = "soft"


def jobs_table(name, top, head_end, groups, panel, chevron):
    """사업분야 | 일자리 연계 대상사업 (three numbered boxes + → line per group) ▶ 창출실적 panel.

    groups: [(label_line, (y0, head_end, body_end, y1), head_y, body_y0, body_y1, arrow_y, sep)],
    panel: dict(ys=[...edges...], cells=[(x0, x1, ya, yb, content, fill, kw)]).
    """
    ys = [top, head_end]
    for _, edges, *_ in groups:
        ys += list(edges)
    ys += panel["ys"] + list(chevron)
    R = Rows(ys)
    g = Grid(name, XS, R.hs)
    hrow = (R(top), R(head_end))
    g.put(X0, 110.0, *hrow, [line1(60, 70, top + 3, top + 7)], frame(HEAD, top="soft", left="soft"), bold=True)
    g.put(110.0, 465.1, *hrow, [line1(240, 250, top + 3, top + 7)], frame(HEAD, top="soft", left="soft", right="soft"),
          bold=True)
    g.put(479.0, X1, *hrow, [line1(490, 505, top + 3, top + 7)], frame(HEAD, top="soft", left="soft", right="soft"),
          bold=True)
    for label, (y0, h1, b1, y1), head_y, by0, by1, arrow_y, sep in groups:
        g.put(X0, 110.0, R(y0), R(y1), [label], frame("#EBEBEB", left="soft", bottom=sep))
        for k, (a, e, base) in enumerate(COLS):
            mark = "①②③"[k]
            g.put(a, e, R(y0), R(h1), [lead(mark, line1(a + 3, e, head_y, head_y + 4))], frame("#E9E9E9", **BOX))
            g.put(a, e, R(h1), R(b1), hang(lines_in(base - 1, base + 15, by0, by1), base),
                  frame(left="soft", right="soft", bottom="soft"), align="LEFT", line=1320)
        g.put(461.3, 465.1, R(y0), R(b1), [], frame(right="soft"))
        g.put(110.0, 465.1, R(b1), R(y1), [lead("→", line1(130, 135, arrow_y, arrow_y + 4), bold=True)],
              frame(right="soft", bottom=sep), align="LEFT")
    g.put(465.1, 479.0, R(chevron[0]), R(chevron[1]), "▶", size=1000, color=ARROW)
    for x0, x1, ya, yb, content, fill, kw in panel["cells"]:
        g.put(x0, x1, R(ya), R(yb), content, fill, **kw)
        if fill == TAG:   # 20 pt tag: no side padding, or 직접 / 간접 wraps
            key = (R(ya), g.xs.index(to_x(x0)))
            g.items[key] = g.items[key][:7] + (dict(left=0, right=0),)
    # panel frame: blank cells carrying the panel's left / right / bottom rules
    first, last = R(head_end), len(R.hs)
    covered = {(r, c) for r, c in g.taken}
    col = {x: g.xs.index(to_x(x)) for x in XS}
    for r in range(first, last):
        if (r, col[479.0]) not in covered:
            g.put(479.0, 487.5, r, r + 1, [], frame(left="soft", bottom="soft" if r == last - 1 else None))
        if (r, col[549.5]) not in covered:
            g.put(549.5, X1, r, r + 1, [], frame(right="soft", bottom="soft" if r == last - 1 else None))
    if (last - 1, col[487.5]) not in covered:
        g.put(487.5, 549.5, last - 1, last, [], frame(bottom="soft"))
    block(g, top)
    return g


def value(x0, x1, ya, yb, line, **kw):
    return (x0, x1, ya, yb, [line], "1", kw)


# 가. 전력계통 / ICT운영: 창출실적 panel with 직접 / 간접 tags and the 직접 일자리 chart (image).
chart_pill = frame("#4A4A4A")
axis = frame("#E4E4E4")
cells = [
    (487.5, 549.5, 429.0, 444.5, [line1(490, 495, 432, 436)], "1", {}),
    (487.5, 549.5, 444.5, 462.0, [line1(495, 505, 446, 450)], "1", {}),
    (487.5, 507.8, 465.5, 479.5, [runs_of(line1(489, 492, 466, 470), x1=507.0)], TAG, {}),
    (507.8, 549.5, 465.5, 479.5, [strip_runs(runs_of(line1(489, 492, 466, 470), x0=507.0))], "1", dict(align="RIGHT", line=1240)),
    (487.5, 507.8, 484.8, 498.8, [runs_of(line1(489, 492, 481, 486), x1=507.0)], TAG, {}),
    (507.8, 549.5, 484.8, 498.8, [strip_runs(runs_of(line1(489, 492, 481, 486), x0=507.0))], "1", dict(align="RIGHT", line=1240)),
    (487.5, 549.5, 519.0, 531.0, [[("직접 일자리 251명↑", 820, True, WHITE)]], chart_pill, dict(line=840)),
    (517.4, 549.5, 531.0, 541.0, [[("2,236명", 850, True, INK)]], "1", dict(line=840)),
    (487.5, 517.4, 541.0, 551.0, [[("1,985명", 850, False, INK)]], "1", dict(line=840)),
    (487.5, 517.4, 566.0, 575.4, [[("’24년", 780, False, INK)]], axis, dict(line=780)),
    (517.4, 549.5, 566.0, 575.4, [[("’25년", 780, True, INK)]], axis, dict(line=780)),
]
panel = dict(ys=[429.0, 444.5, 462.0, 465.5, 479.5, 484.8, 498.8, 519.0, 531.0, 541.0, 551.0, 566.0, 575.4],
             cells=cells)
jobs_table("table-ga", 384.6, 406.0,
           [(line1(60, 70, 446, 452), (406.0, 426.0, 484.8, 504.2), 411, 427, 482, 488, "dot"),
            (line1(60, 70, 547, 553), (504.2, 526.6, 585.5, 606.0), 511, 528, 583, 588, "soft")],
           panel, (484.8, 504.2))

g = Grid("note", [X0, X1], [1400])
g.put(X0, X1, 0, 1, [line1(55, 60, 609, 613)], align="LEFT", line=1200)
block(g, 608.6)

heading("title-na", line1(55, 60, 628, 632), 627.4)

cells = [
    (487.5, 549.5, 677.0, 691.5, [line1(490, 495, 680, 684)], "1", {}),
    (487.5, 549.5, 691.5, 707.0, [line1(500, 505, 694, 698)], "1", {}),
    (487.5, 507.8, 713.0, 727.0, [runs_of(line1(489, 492, 714, 718), x1=507.0)], TAG, {}),
    (507.8, 549.5, 713.0, 727.0, [strip_runs(runs_of(line1(489, 492, 714, 718), x0=507.0))], "1", dict(align="RIGHT", line=1240)),
    (487.5, 507.8, 729.7, 743.7, [runs_of(line1(489, 492, 730, 734), x1=507.0)], TAG, {}),
    (507.8, 549.5, 729.7, 743.7, [strip_runs(runs_of(line1(489, 492, 730, 734), x0=507.0))], "1", dict(align="RIGHT", line=1240)),
]
panel = dict(ys=[677.0, 691.5, 707.0, 713.0, 727.0, 729.7, 743.7], cells=cells)
jobs_table("table-na", 650.1, 671.5,
           [(line1(60, 70, 704, 710), (671.5, 691.5, 734.9, 755.4), 677, 692, 732, 738, "soft")],
           panel, (691.5, 713.0))

# 주요성과 (text layer)
g = Grid("result", [X0, 111.7, X1], [4000])
g.put(X0, 111.7, 0, 1, [runs_of(line1(65, 70, 775, 779), WHITE)], frame("#6A6A6A", top="mid", bottom="mid", left="mid"))
g.put(111.7, X1, 0, 1, lines_in(115, 120, 766, 790), frame(top="mid", bottom="mid", right="mid"), align="LEFT",
      line=1540)
block(g, 761.6)

kit.finish(target, end=803.0)
