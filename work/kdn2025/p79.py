"""Rebuild KDN 2025 report page 79 (second PDF local page 29, printed page 51) as editable HWPX.

Usage: python3 work/kdn2025/p79.py <report2.pdf> <out.hwpx> [--page 29]

창업 및 경제활성화 평가내용 01, 2-나 (수출바우처 / 협력대출 two-box table) and section 3
(협업방향 band, 가. 세네갈 ODA project table, 나. UAE / 인도네시아 project tables, 주요성과).
Built with the shared kit: one flat table per band at its PDF y, all text from the PDF text layer.

Images in the source and how they are kept: the ~930 vector pieces are the small arrow glyphs
(➡ -> "→"), the (+) joints (-> "+"), the ❶❷❸ digits (-> ①②③), the down chevrons (-> "▼") and
the rounded boxes / pills (-> cells with fills and borders); the 'NEW 신규' stickers are typed as
dark tag cells; the side tab is a floating cell table. No chart or photo on this page.

Source oddity: the header "창업·벤처기업" carries a Wingdings private-use glyph U+F09E as its
middle dot in the PDF text layer; it is kept as-is (KoPub has no glyph for it).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kit  # noqa: E402
from kit import Layout, recipe_inputs  # noqa: E402

source, target = recipe_inputs(29, "금융지원으로 수출의 문을 열다")
L = Layout(top=3200)
kit.setup(source, L)
from kit import *  # noqa: E402,F401,F403  helpers and presets bound to this page

DARK = "#5E5E5E"
LABEL = frame("#EFEFEF", hatch="#E0E0E0")
TAGBOX = frame(WHITE, top="soft", bottom="soft", left="soft", right="soft")
TAGDARK = frame("#6E6E6E")
TAGGRAY = frame("#C4C4C4")
SUB = frame("#E9E9E9")


def tag(g, x0, x1, r0, r1, content, fill, ratio=88, **kw):
    """Small tag / pill cell: 0.6 pt side padding instead of 5 pt, 장평 fitted to that width."""
    items = content if isinstance(content, list) else [content]
    inner = (to_x(x1) - to_x(x0) - 120) / 100 * 0.96
    for item in items:
        runs = [(item, kw.get("size", 1080))] if isinstance(item, str) else (
            runs_of(item) if isinstance(item, dict) else item)
        need = text_width(runs, ratio)
        if need > inner:
            ratio = int(ratio * inner / need)
    g.put(x0, x1, r0, r1, content, fill, fit=False, ratio=ratio, **kw)
    key = (r0, g.xs.index(to_x(x0)))
    g.items[key] = g.items[key][:7] + (dict(left=60, right=60),)


def joined(pieces, glyph="→"):
    """Run pieces joined by a typed arrow (the PDF draws the arrows as images)."""
    out = []
    for k, piece in enumerate(pieces):
        piece = strip_runs(piece)
        if k:
            out.append((f" {glyph} ", piece[0][1], False, INK))
        out += piece
    return out


def sticker(name, line, cut, top, width=None):
    """'가. title [NEW 신규]': heading with the sticker typed as a small dark tag cell."""
    end = cut + width if width else X1
    g = Grid(name, [X0, cut, end, X1] if width else [X0, cut, X1], [1700])
    g.put(X0, cut, 0, 1, [line], align="LEFT", line=1500)
    tag(g, cut, end, 0, 1, [[("NEW ", 480, True, WHITE), ("신규", 780, True, WHITE)]], frame("#3C3C3C"), ratio=75,
        line=950)
    block(g, top)


def body_lines(x0, x1, y0, y1, indent="  "):
    """Bullet lines as run lists; continuation lines get the source's hanging indent."""
    out = []
    for line in lines_in(x0, x1, y0, y1):
        runs = runs_of(line)
        if not runs[0][0].startswith(("∙", "-", "※")):
            runs = [(indent, runs[0][1], False, INK)] + runs
        out.append(runs)
    return out


def with_marks(pieces):
    """'... (' + ① + '컨소시엄 +' + ② + '기술협력)': the ❶❷❸ images typed as ①②③ (KS X 1001)."""
    out = strip_runs(pieces[0])
    for k, piece in enumerate(pieces[1:]):
        if k:
            out.append((" ", piece[0][1], False, INK))
        out.append(("①②③"[k] + " ", 890, True, INK))
        out += strip_runs(piece)
    return out


def kdn_row(g, r, y0, y1):
    """KDN | duties  +  중소/기업 | duties (two light boxes joined by '+')."""
    box = frame(top="soft", bottom="soft", right="soft")
    g.put(112.0, 141.0, r, r + 1, [line1(115, 120, y0, y1)], frame("#E3E3E3", top="soft", bottom="soft", left="soft"))
    g.put(141.0, 323.0, r, r + 1, lines_in(145, 150, y0 - 10, y1 + 10), box, align="LEFT", line=1400)
    g.put(323.0, 337.0, r, r + 1, "+", size=1500, bold=True, color="#9A9A9A", fit=False)
    g.put(337.0, 366.0, r, r + 1, lines_in(342, 347, y0 - 10, y1 + 10), frame("#E3E3E3", top="soft", bottom="soft",
                                                                             left="soft"), line=1200)
    g.put(366.0, 551.0, r, r + 1, lines_in(370, 375, y0 - 10, y1 + 10), box, align="LEFT", line=1400)


PX = [X0, 109.0, 112.0, 141.0, 152.0, 154.5, 175.5, 274.0, 284.0, 303.5, 323.0, 337.0, 366.0, 551.0, X1]


def project_head(g, title, top_y):
    g.put(X0, 109.0, 0, 1, [runs_of(line1(64, 70, top_y - 2, top_y + 4), WHITE)], frame(DARK, top="mid"))
    g.put(109.0, X1, 0, 1, [title], frame("#D6D6D6", top="mid"), line=1300)


def project_tail(g, r, label_y, line):
    g.put(X0, 109.0, r, r + 1, [runs_of(line1(64, 70, label_y, label_y + 6), WHITE)], frame("#9C9C9C", left="mid"))
    g.put(109.0, X1, r, r + 1, [line], frame("#E4E4E4", right="mid"), line=1300)
    g.put(X0, X1, r + 1, r + 2, [], frame(bottom="mid", left="mid", right="mid"))


# ---------------------------------------------------------------------------
# Page chrome (odd page): running head over a rule, side tab, footer at the right.
# ---------------------------------------------------------------------------
L.add_table([[cell(0, 3350, 1680, [para([("01", 1380, True, WHITE)], "CENTER")[0]], dark)],
             [cell(0, 3350, 5960, [para([(ch, 950, True, INK)], "CENTER", 1160)[0] for ch in "경영관리"], gray2)]],
            floating=(57800, 15000))
foot = [(only_text, size, False, INK) for only_text, size in (
    (line1(450, 455, 818, 822)["text"], 790), ("    ", 790), (line1(540, 552, 816, 820)["text"], 1090))]
L.add_table([[cell(0, W, 1500, [para(foot, "RIGHT", 1300)[0]])]], floating=(5660, 81550))

g = Grid("head", [X0, 390.0, X1], [1680])
g.put(X0, 390.0, 0, 1, [], frame(bottom="soft"))
g.put(390.0, X1, 0, 1, [line1(390, 400, 35, 40)], align="RIGHT")
block(g, 32.0)

# ---------------------------------------------------------------------------
# 나. 금융지원으로 수출의 문을 열다 ... [NEW 신규]
# ---------------------------------------------------------------------------
sticker("title-na", line1(55, 60, 68, 75), 529.5, 69.5)

xs = [X0, 105.0, 108.0, 121.4, 124.0, 140.6, 179.0, 330.0, 333.0, 336.0, 346.7, 365.7, 413.0, X1]
g = Grid("finance", xs, [1800, 500, 3500, 1650, 750, 1950, 250])
g.put(X0, 105.0, 0, 1, [runs_of(line1(58, 62, 94, 100), WHITE)], frame(DARK))
g.put(X0, 105.0, 2, 5, [line1(60, 65, 134, 140)], LABEL)
g.put(X0, 105.0, 5, 7, [line1(60, 65, 175, 181)], LABEL)
boxes = ((108.0, 124.0, 179.0, 330.0, 121.4, 140.6, 112, 125, (122, 127)),
         (333.0, 336.0, 413.0, X1, 346.7, 365.7, 337, 350, (347, 352)))
for k, (a, p0, p1, e, t0, t1, bx0, bx1, (tx0, tx1)) in enumerate(boxes):
    if k == 0:
        head = line1(125, 130, 94, 100)
        pill_runs, title = runs_of(head, x1=p1), strip_runs(runs_of(head, x0=p1))
    else:
        pill_runs, title = runs_of(line1(340, 345, 95, 100)), runs_of(line1(414, 418, 94, 100))
    side = dict(left="mid", right="mid")
    g.put(a, p0, 0, 1, [], frame(top="mid", left="mid"))
    tag(g, p0, p1, 0, 1, [pill_runs], TAGBOX, line=1000)
    g.put(p1, e, 0, 1, [title], frame(top="mid", right="mid"), line=1300)
    g.put(a, e, 1, 2, [], frame(**side))
    g.put(a, e, 2, 3, body_lines(bx0, bx1, 117, 150), frame(**side), align="LEFT", line=1640)
    tag_ln = line1(tx0, tx1, 150, 156)
    g.put(a, t0, 3, 4, [], frame(left="mid"))
    tag(g, t0, t1, 3, 4, [runs_of(tag_ln, WHITE if k else INK, x1=t1)], TAGDARK if k else TAGBOX, line=1000)
    g.put(t1, e, 3, 4, [strip_runs(runs_of(tag_ln, x0=t1))], frame(right="mid"), align="LEFT", line=1300)
    g.put(a, e, 4, 5, "▼", frame(**side), size=700, color="#9A9A9A", line=580)
    g.put(a, e, 5, 6, [line1(bx0, bx0 + 5, 175, 181)], frame("#E4E4E4", **side), align="LEFT", line=1300)
    g.put(a, e, 6, 7, [], frame(bottom="mid", **side))
block(g, 92.0)

# ---------------------------------------------------------------------------
# 3. 에너지ICT 중소기업과의 파트너십으로 협력형 해외 동반진출 및 수주 지원
# ---------------------------------------------------------------------------
g = Grid("sec3", [X0, 84.8, X1], [2300])
g.put(X0, 84.8, 0, 1, [runs_of(line1(64, 70, 220, 226), WHITE)], frame(DARK), line=1900)
g.put(84.8, X1, 0, 1, [line1(90, 95, 220, 226)], frame("#E2E2E2"), align="LEFT", line=1750)
block(g, 219.0)

# 협업방향: title line, three numbered items joined by "+", three captions (dotted separators)
title = runs_of(line1(115, 120, 251, 257))
title = [(t.replace("구성  정부", "구성 → 정부"), s, b, c) for t, s, b, c in title]
xs = [X0, 105.0, 108.0, 113.0, 250.0, 257.0, 264.0, 398.0, 404.0, 411.0, 549.0, X1]
g = Grid("ways", xs, [2200, 1900, 2200, 500])
g.put(X0, 105.0, 0, 4, [line1(60, 65, 274, 280)], LABEL)
g.put(108.0, X1, 0, 1, [title], frame(top="mid", left="mid", right="mid"), line=1300)
g.put(108.0, 113.0, 1, 3, [], frame(left="mid"))
g.put(549.0, X1, 1, 3, [], frame(right="mid"))
items = (((113.0, 250.0), 172, "①"), ((264.0, 398.0), 318, "②"), ((411.0, 549.0), 465, "③"))
for k, ((a, e), lx, mark) in enumerate(items):
    g.put(a, e, 1, 2, [[(mark + " ", 1090, False, INK)] + runs_of(line1(lx - 2, lx + 2, 272, 278))], SUB, line=1300)
for a, e in ((250.0, 264.0), (398.0, 411.0)):
    g.put(a, e, 1, 2, "+", SUB, size=1300, bold=True, color="#8A8A8A", fit=False)
for k, (a, e, lx) in enumerate(((113.0, 257.0, 129), (257.0, 404.0, 277), (404.0, 549.0, 433))):
    g.put(a, e, 2, 3, [line1(lx - 2, lx + 2, 290, 296)], frame(right="dot") if k < 2 else "1", line=1300)
g.put(108.0, X1, 3, 4, [], frame(bottom="mid", left="mid", right="mid"))
block(g, 248.0)

# ---------------------------------------------------------------------------
# 가. 지역 에너지ICT 중소기업과 아프리카 ODA 사업 동반진출 [NEW 신규]
# ---------------------------------------------------------------------------
sticker("title-ga", line1(55, 60, 325, 330), 393.0, 325.5, width=25.0)

first = runs_of(line1(110, 115, 351, 357))
first = [(t.replace("社  한전", "社 → 한전"), s, b, c) for t, s, b, c in first]
second = joined([runs_of(line1(125, 132, 366, 372)), runs_of(line1(345, 352, 366, 372))])
second = [("  → ", second[0][1], False, INK)] + second
g = Grid("process", [X0, 109.0, X1], [3700])
g.put(X0, 109.0, 0, 1, [line1(60, 65, 352, 357), line1(62, 67, 365, 370)],
      frame(top="mid", bottom="mid", left="mid", right="soft"), line=1300)
g.put(109.0, X1, 0, 1, [first, second], frame("#EDEDED", top="mid", bottom="mid", right="mid"), align="LEFT",
      line=1500)
block(g, 348.0)

# Project 1: 세네갈 에너지자립 로드맵
head = with_marks([runs_of(line1(160, 165, 393, 399)), runs_of(line1(416, 420, 393, 399)),
                   runs_of(line1(468, 472, 393, 399))])
g = Grid("project-1", PX, [1700, 200, 1950, 3700, 2000, 2000, 2000, 300])
project_head(g, head, 393)
g.put(X0, 109.0, 1, 4, [line1(64, 70, 431, 437)], frame("#EFEFEF", left="mid", hatch="#E0E0E0"))
g.put(X0, 109.0, 4, 6, [line1(64, 70, 480, 486)], frame("#EFEFEF", left="mid", hatch="#E0E0E0"))
g.put(551.0, X1, 1, 6, [], frame(right="mid"))
tag_ln = line1(115, 120, 413, 419)
tag(g, 112.0, 152.0, 2, 3, [runs_of(tag_ln, WHITE, x1=152.0)], TAGDARK, line=1100)
g.put(152.0, 551.0, 2, 3, [strip_runs(runs_of(tag_ln, x0=152.0))], align="LEFT", line=1300)
kdn_row(g, 3, 439, 447)
for r, (ya, yb) in ((4, (472, 478)), (5, (489, 495))):
    left = line1(114, 118, ya, yb)
    right = line1(280, 285, ya, yb)
    tag(g, 112.0, 152.0, r, r + 1, [runs_of(left, x1=152.0)], TAGGRAY, line=1050)
    tag(g, 154.5, 175.5, r, r + 1, [runs_of(left, x0=152.0, x1=176.0)], TAGBOX, line=1050)
    g.put(175.5, 274.0, r, r + 1, [strip_runs(runs_of(left, x0=176.0))], align="LEFT", line=1300)
    g.put(274.0, 284.0, r, r + 1, "→", size=1000, bold=True, color="#555555", fit=False)
    tag(g, 284.0, 303.5, r, r + 1, [runs_of(right, WHITE, x1=303.5)], TAGDARK, line=1050)
    g.put(303.5, 551.0, r, r + 1, [strip_runs(runs_of(right, x0=303.5))], align="LEFT", line=1300)
project_tail(g, 6, 511, line1(110, 115, 511, 516))
block(g, 392.0)

# 나. 기관 자체 해외사업 협업을 통한 ...
g = Grid("title-na2", [X0, X1], [1700])
g.put(X0, X1, 0, 1, [line1(55, 60, 540, 546)], align="LEFT", line=1500)
block(g, 541.0)


def project(name, top, head_y, head_parts, tag_line, plan_line, cuts, kdn_y, label_y, result_y):
    """사업명 band | 추진내용 (추진방향 tag + arrow line, KDN + 중소기업 boxes) | 추진성과 band."""
    head = with_marks([runs_of(line1(x - 2, x + 2, head_y - 2, head_y + 4)) for x in head_parts])
    g = Grid(name, PX, [1700, 200, 2000, 3900, 2000, 300])
    project_head(g, head, head_y)
    g.put(X0, 109.0, 1, 4, [line1(64, 70, label_y, label_y + 6)], frame("#EFEFEF", left="mid", hatch="#E0E0E0"))
    g.put(551.0, X1, 1, 4, [], frame(right="mid"))
    tag(g, 112.0, 152.0, 2, 3, [runs_of(tag_line, WHITE, x1=150.0)], TAGDARK, line=1100)
    a, b = cuts
    g.put(152.0, 551.0, 2, 3, [joined([runs_of(plan_line, x0=150.0, x1=a), runs_of(plan_line, x0=a, x1=b),
                                      runs_of(plan_line, x0=b)])], align="LEFT", line=1300)
    kdn_row(g, 3, kdn_y, kdn_y + 8)
    project_tail(g, 4, result_y, line1(125, 135, result_y, result_y + 6))
    block(g, top)


# Project 2: UAE 원전 DB (its 추진방향 tag is a PDF line of its own); project 3: 인도네시아 SEDA
project("project-2", 564.0, 567, (204, 376, 427), line1(115, 120, 586, 592), line1(152, 156, 584, 590),
        (262.0, 410.0), 611, 604, 645)
project("project-3", 672.0, 675, (132, 397, 448, 500), line1(115, 120, 692, 698), line1(115, 120, 692, 698),
        (279.0, 440.0), 719, 712, 753)

# 주요성과
g = Grid("result", [X0, 111.5, X1], [2300])
g.put(X0, 111.5, 0, 1, [runs_of(line1(65, 70, 783, 789), WHITE)], frame("#6A6A6A", top="mid", bottom="mid",
                                                                            left="mid"))
g.put(111.5, X1, 0, 1, [line1(115, 120, 783, 789)], frame(top="mid", bottom="mid", right="mid"), align="LEFT")
block(g, 779.5)

kit.finish(target, end=803.0)
