"""Rebuild KDN 2025 report PDF page 91 (second PDF local page 41, printed page 61) as editable HWPX.

Usage: python3 work/kdn2025/p91.py <report2.pdf> <out.hwpx> [--page 41]

상생･협력 및 지역발전, section 4 (사회적경제기업 육성). Built with the shared diagram kit (one flat
table per horizontal band on a grid of PDF x edges); all text comes from the PDF text layer.
Images: the section-number band, the '지적사항 개선' sticker, the side tab and the four card
photos / event photo are typed cells or empty photo cells; the (+) joints become '+' connector
cells; the small 신규 / 개선 / 기존 / 처음수출 / 수출성장 / 창업희망청년 … tags (vector boxes
under text-layer words) become separate boxed or dark cells.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kit  # noqa: E402
from kit import Layout, recipe_inputs  # noqa: E402

source, target = recipe_inputs(41, "사회적경제기업 성장과 자립을 위한 체계적 육성과 생태계 조성")
L = Layout(top=3100)
kit.setup(source, L)
from kit import *  # noqa: E402,F401,F403  helpers and presets bound to this page

DARK, LABEL = "#6A6A6A", "#E6E6E6"
HEAD, HEAD_DARK, GROUP, BAND = "#D7D7D7", "#7E7E7E", "#EBEBEB", "#E6E6E6"
PLUS = "#9A9A9A"
BOXTAG = frame(WHITE, top="soft", bottom="soft", left="soft", right="soft")   # outlined tag
DARKTAG = frame("#7E7E7E")                                                   # dark tag


def hang(lines, base):
    """Lines keep their PDF indent: spaces for the x offset and for the line's own lead."""
    out = []
    for l in lines:
        runs = runs_of(l)
        size = runs[0][1] / 100
        raw = "".join(s["text"] for s in l["spans"])
        offset = l["bbox"][0] - base + (len(raw) - len(raw.lstrip(" "))) * 0.29 * size
        n = max(0, round(offset / (0.29 * size)))
        out.append([(" " * n, runs[0][1], False, INK)] + runs if n else runs)
    return out


def section_band(name, num_line, title_line, top):
    """'4 | heading' band: dark number cell and light gray title cell (images in the PDF)."""
    g = Grid(name, [X0, 84.5, X1], [2300])
    g.put(X0, 84.5, 0, 1, [runs_of(num_line, WHITE)], frame(DARK), line=1700)
    g.put(84.5, X1, 0, 1, [runs_of(title_line)], frame(LABEL), align="LEFT", line=1700)
    block(g, top)


def boxed(name, label_line, body_lines, top, height, label_fill="#D5D5D5", label_color=INK):
    """추진배경 / 주요성과 box: label at left, outlined body with bullet lines."""
    g = Grid(name, [X0, 111.7, X1], [height])
    g.put(X0, 111.7, 0, 1, [runs_of(label_line, label_color)],
          frame(label_fill, top="mid", bottom="mid", left="mid"))
    g.put(111.7, X1, 0, 1, body_lines, frame(top="mid", bottom="mid", right="mid"), align="LEFT")
    block(g, top)


def split(line, cuts, colors=None):
    """One PDF line cut at x positions into run lists (tag words become their own cells)."""
    edges = [-1e9, *cuts, 1e9]
    colors = colors or [INK] * (len(edges) - 1)
    return [strip_runs(runs_of(line, c, x0=a, x1=b)) for a, b, c in zip(edges, edges[1:], colors)]


def tag(g, x0, x1, r, runs, fill):
    """Small tag cell: thin symmetric padding so a two-syllable tag stays on one line."""
    width = to_x(x1) - to_x(x0)
    ratio = min(90, int(90 * (width - 160) / 100 * 0.96 / text_width(runs, 90)))
    g.put(x0, x1, r, r + 1, [runs], fill, line=1000, ratio=ratio, fit=False)
    key = (r, g.xs.index(to_x(x0)))
    g.items[key] = (*g.items[key][:7], dict(left=80, right=80, top=40, bottom=40))


# ---------------------------------------------------------------------------
# Page chrome (odd page): running head over a rule, side tab, footer at the right.
# ---------------------------------------------------------------------------
L.add_table([[cell(0, 3350, 1680, [para([("01", 1380, True, WHITE)], "CENTER")[0]], dark)],
             [cell(0, 3350, 5960, [para([(ch, 950, True, INK)], "CENTER", 1160)[0] for ch in "경영관리"], gray2)]],
            floating=(57800, 15000))
foot = [(only_text, size, False, INK) for only_text, size in (
    (line1(450, 455, 818, 822)["text"], 790), ("    ", 790), (line1(540, 552, 816, 820)["text"], 1090))]
L.add_table([[cell(0, W, 1500, [para(foot, "RIGHT", 1300)[0]])]], floating=(5660, 81550))

g = Grid("head", [X0, 376.0, X1], [1680])
g.put(X0, 376.0, 0, 1, [], frame(bottom="soft"))
g.put(376.0, X1, 0, 1, [line1(375, 385, 35, 40)], align="RIGHT")
block(g, 32.0)

# ---------------------------------------------------------------------------
# 4. / 가. : 추진배경, 협업체계 and four cards
# ---------------------------------------------------------------------------
section_band("sec4", line1(60, 70, 72, 76), line1(90, 95, 73, 77), 70.9)

g = Grid("title-ga", [X0, X1], [1650])
g.put(X0, X1, 0, 1, [line1(55, 60, 100, 105)], align="LEFT", line=1450)
block(g, 100.6)

boxed("background", line1(65, 70, 135, 139), lines_in(115, 120, 125, 150), 123.2, 3710)

xs = [X0, 114.1, 116.2, 171.8, 187.6, 272.3, 289.1, 433.4, 450.2, X1]
g = Grid("partners", xs, [2300])
g.put(X0, 114.1, 0, 1, [line1(60, 70, 172, 176)], frame("#E3E3E3", top="soft"))
fills = ("#D2D2D2", "#EEEEEE", "#D9D9D9", "#EEEEEE")
spots = ((116.2, 171.8, 120), (187.6, 272.3, 190), (289.1, 433.4, 295), (450.2, X1, 455))
for (a, e, x), fill in zip(spots, fills):
    g.put(a, e, 0, 1, [line1(x, x + 10, 170, 176)], frame(fill))
for a, e in ((171.8, 187.6), (272.3, 289.1), (433.4, 450.2)):
    g.put(a, e, 0, 1, "+", size=1300, bold=True, color=PLUS, fit=False)
block(g, 166.6)

# Cards: rounded outlined boxes (title row with a tag, bullets with a dark 개선 tag, photo, result band).
xs = [X0, 59.5, 69.0, 70.4, 84.5, 89.2, 117.5, 253.7, 302.5, 305.0,
      307.5, 310.3, 310.9, 321.2, 338.3, 340.0, 371.3, 383.5, 504.5, 552.7, X1]
TOPC = [410, 1170, 330, 3580, 1170, 280, 2430, 290]
BOTC = [410, 1170, 340, 3570, 1170, 290, 3830, 280]
g = Grid("cards", xs, TOPC + [260] + BOTC)
cards = (  # box x0, x1, tag x0, tag x1, bullet/tag/text cuts, photo x0, row0, y range
    (X0, 305.0, 69.0, 117.5, (59.5, 70.4, 89.2, 253.7), 253.7, 0, (195.9, 292.5)),
    (307.5, X1, 310.9, 383.5, (310.3, 321.2, 340.0, 504.5), 504.5, 0, (195.9, 292.5)),
    (X0, 305.0, 84.5, 117.5, (59.5, 70.4, 89.2, 253.7), 253.7, 9, (295.1, 405.7)),
    (307.5, X1, 338.3, 371.3, (310.3, 321.2, 340.0, 504.5), 504.5, 9, (295.1, 405.7)),
)
for a, e, t0, t1, (b0, b1, b2, b3), ph, r, (y0, y1) in cards:
    inner_r = 302.5 if a == X0 else 552.7
    g.put(a, b0, r, r + 8, [], frame(left="mid", top="mid", bottom="mid"))
    g.put(inner_r, e, r, r + 8, [], frame(right="mid", top="mid", bottom="mid"))
    g.put(b0, inner_r, r, r + 1, [], frame(top="mid"))
    g.put(b0, inner_r, r + 7, r + 8, [], frame(bottom="mid"))
    head = lines_in(a, inner_r, y0 + 2, y0 + 12)[0]
    g.put(b0, t0, r + 1, r + 3, [], frame(bottom="soft"))
    tag(g, t0, t1, r + 1, runs_of(head, x1=t1 - 1.0), BOXTAG)
    g.put(t0, t1, r + 2, r + 3, [], frame(bottom="soft"))
    g.put(t1, inner_r, r + 1, r + 3, [strip_runs(runs_of(head, x0=t1 - 1.0))], frame(bottom="soft"),
          align="LEFT", line=1300)
    body = lines_in(b0, b1, y0 + 20, y0 + 68)
    g.put(b0, ph, r + 3, r + 4, body[:2], align="LEFT", line=1550)
    bullet, tagged, rest = split(body[2], [b1, b2 - 0.5], [INK, WHITE, INK])
    g.put(b0, b1, r + 4, r + 6, [bullet], line=1200)
    tag(g, b1, b2, r + 4, tagged, DARKTAG)
    g.put(b2, ph, r + 4, r + 6, [rest], align="LEFT", line=1250)
    g.put(ph, inner_r, r + 3, r + 6, [], photo)
    band = lines_in(a, e, y1 - (41 if r else 27), y1 - 2)
    g.put(b0, inner_r, r + 6, r + 7, band, frame(BAND), line=1250 if len(band) > 1 else None)
block(g, 195.9)

boxed("result-ga", line1(65, 70, 418, 422), lines_in(115, 120, 415, 425), 412.0, 2440,
      label_fill=DARK, label_color=WHITE)

# ---------------------------------------------------------------------------
# 나. 판로개척 지원 table
# ---------------------------------------------------------------------------
g = Grid("title-na", [X0, 503.0, X1], [1650])
g.put(X0, 503.0, 0, 1, [line1(55, 60, 445, 450)], align="LEFT", line=1450)
g.put(503.0, X1, 0, 1, "지적사항 개선", frame("#3C3C3C"), size=760, bold=True, color=WHITE, line=1000)
block(g, 446.0)

boxed("background-na", line1(65, 70, 480, 485), lines_in(115, 120, 470, 495), 468.6, 3720)

# Header + 국내 판촉･홍보 row
xs = [X0, 73.7, 113.4, 409.6, 428.3, 481.9, X1]
g = Grid("table-domestic", xs, [1850, 360, 1170, 310, 1550, 1590])
g.put(X0, 113.4, 0, 1, [line1(70, 100, 514, 519)], frame(HEAD, top="mid"))
g.put(113.4, 481.9, 0, 1, [line1(270, 290, 514, 519)], frame(HEAD, top="mid"))
g.put(481.9, X1, 0, 1, [runs_of(line1(495, 505, 514, 519), WHITE)],
      frame(HEAD_DARK, top="strong", left="strong", right="strong"))
g.put(X0, 73.7, 1, 6, lines_in(57, 73, 535, 575), frame(GROUP, bottom="soft", right="soft"), line=1430)
g.put(73.7, 113.4, 1, 6, lines_in(74, 110, 535, 575), frame(GROUP, bottom="soft"), line=1430)
first = line1(115, 120, 532, 538)
text, tagged = split(first, [409.0])
g.put(113.4, 409.6, 2, 4, [text], align="LEFT", line=1250)
tag(g, 409.6, 428.3, 2, tagged, BOXTAG)
g.put(113.4, 428.3, 4, 5, hang([line1(115, 120, 548, 553)], 116.4), align="LEFT", line=1300)
g.put(113.4, 428.3, 5, 6, hang([line1(115, 120, 563, 568)], 116.4), frame(bottom="soft"), align="LEFT",
      line=1300)
g.put(428.3, 481.9, 1, 6, [], frame("#E4E4E4", top="soft", left="soft", right="soft", bottom="soft"))
g.put(481.9, X1, 1, 6, hang(lines_in(482, 556, 531, 580), 484.9), frame(left="strong", right="strong",
                                                                        bottom="soft"), align="LEFT", line=1430)
block(g, 512.1)

# 해외: 맞춤형 수출지원 and 해외 유통망 입점지원 (partner flow and three improvement boxes)
xs = [X0, 73.7, 113.4, 116.6, 119.5, 122.3, 131.3, 141.1, 164.3, 197.2, 211.1, 232.5, 235.5, 238.2, 241.1,
      243.9, 262.7, 268.1, 282.0, 337.4, 354.1, 356.2, 357.1, 359.8, 362.7, 365.5, 370.2, 384.1, 475.7, 478.7,
      481.9, X1]
EXPORT = [360, 1170, 400, 1170, 410, 1170, 360]
MALL = [1830, 1590, 2440, 410, 1850, 450, 1170, 350, 1170, 400, 2090, 290]
g = Grid("table-abroad", xs, EXPORT + MALL)
g.put(X0, 73.7, 0, 19, lines_in(57, 73, 655, 690), frame(GROUP, right="soft", bottom="mid"), line=1430)
g.put(73.7, 113.4, 0, 7, lines_in(74, 113, 590, 615), frame(GROUP, bottom="soft"), line=1430)
g.put(481.9, X1, 0, 7, hang(lines_in(482, 556, 581, 630), 484.9), frame(left="strong", right="strong",
                                                                       bottom="soft"), align="LEFT", line=1430)
line = line1(115, 120, 580, 590)
before, tagged, after = split(line, [337.4, 355.9], [INK, WHITE, INK])
g.put(113.4, 337.4, 1, 3, [before], align="LEFT", line=1250)
tag(g, 337.4, 356.2, 1, tagged, DARKTAG)
g.put(356.2, 481.9, 1, 3, [after], align="LEFT", line=1250)
for r, y in ((3, 600.1), (5, 615.8)):
    line = line1(115, 120, y - 1, y + 1)
    dash, tagged, rest = split(line, [131.3, 164.0])
    last = r == 5
    fr = frame(bottom="soft") if last else "1"
    g.put(113.4, 131.3, r, r + 2, [[("   -", 1090, False, INK)] if not dash else dash], fr, align="RIGHT",
          line=1250)
    tag(g, 131.3, 164.3, r, tagged, BOXTAG)
    g.put(164.3, 481.9, r, r + 2, [rest], fr, align="LEFT", line=1250)
g.put(131.3, 164.3, 6, 7, [], frame(bottom="soft"))

R = 7
g.put(73.7, 113.4, R, R + 12, lines_in(74, 113, 675, 715), frame(GROUP, bottom="mid"), line=1430)
g.put(481.9, X1, R, R + 12, hang(lines_in(482, 556, 660, 730), 484.9),
      frame(left="strong", right="strong", bottom="strong"), align="LEFT", line=1550)
g.put(113.4, 481.9, R, R + 1, [line1(115, 120, 630, 637)], align="LEFT", line=1250)
for (a, e), x in zip(((116.6, 197.2), (211.1, 268.1), (282.0, 370.2), (384.1, 478.7)), (139, 223, 286, 387)):
    g.put(a, e, R + 1, R + 2, [line1(x, x + 2, 652, 656)], frame("#EBEBEB", top="soft", left="soft", right="soft"),
          line=1200)
    g.put(a, e, R + 2, R + 3, [lines_in(a, e, 670, 676)[0]], frame(top="soft", left="soft", right="soft",
                                                                   bottom="soft"), line=1200)
for a, e in ((197.2, 211.1), (268.1, 282.0), (370.2, 384.1)):
    g.put(a, e, R + 1, R + 3, "+", size=1300, bold=True, color=PLUS, fit=False)
for a, s0, t0, t1, s1, e in ((116.6, 119.5, 122.3, 141.1, 232.5, 235.5), (238.2, 241.1, 243.9, 262.7, 354.1, 357.1),
                             (359.8, 362.7, 365.5, 384.1, 475.7, 478.7)):
    g.put(a, e, R + 4, R + 5, [lines_in(a, e, 695, 700)[0]], frame("#DCDCDC", top="soft", left="soft", right="soft"),
          line=1250)
    g.put(a, s0, R + 5, R + 11, [], frame(left="soft", bottom="soft"))
    g.put(s1, e, R + 5, R + 11, [], frame(right="soft", bottom="soft"))
    for r, y, fill, color in ((R + 6, 716.8, BOXTAG, INK), (R + 8, 732.0, DARKTAG, WHITE)):
        line = line1(t0, t1, y - 1, y + 1)
        tagged, rest = split(line, [t1 - 1.0], [color, INK])
        tag(g, t0, t1, r, tagged, fill)
        g.put(t1, s1, r, r + 2, [rest], frame(bottom="dot") if r == R + 8 else "1", align="LEFT", line=1250)
    g.put(s0, t1, R + 9, R + 10, [], frame(bottom="dot"))
    g.put(s0, s1, R + 10, R + 11, [line1(a, e, 750, 753)], frame(bottom="soft"), align="LEFT", line=1250)
g.put(113.4, 481.9, R + 11, R + 12, [], frame(bottom="mid"))
block(g, 580.4)

boxed("result-na", line1(65, 70, 783, 787), lines_in(115, 120, 780, 790), 777.7, 2450,
      label_fill=DARK, label_color=WHITE)

kit.finish(target, end=803.0)
