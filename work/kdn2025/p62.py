"""Rebuild KDN 2025 report PDF page 62 (second PDF local page 12, printed page 39) as editable HWPX.

Usage: python3 work/kdn2025/p62.py <report2.pdf> <out.hwpx> [--page 12]

안전 및 재난관리 sections 3 "[근로환경] ..." and 4 "[건설･협력사] ...". Built with the shared kit
(one flat table per horizontal band on a grid of PDF x edges); all running text, labels, card
tags and chart captions come from the PDF text layer.

Images and how they are kept:
- section number bands, PART box, the "지적사항 개선" sticker (hand icon omitted): typed cells.
- the six small bar charts next to 가. (values in the image, read from a 7x render; every
  difference matches its tag: 15->22 = 7명, 2->7 = 5개소, 3.89->3.97 = 0.08점, 3.79->3.99 = 0.2점,
  16.1->12.3 = 3.8%p, 17.4 vs 13.8 = 3.6%p): value cells only, no bars.
- 나. cards: illustrations -> photo cells; the card-2 labels 체결고리 ▶ 고정나사 / 단일그립 ▶ 이중그립
  and the card-1 caption "고압 전선 작업용 로봇팔" (image text, 4-10x render) are typed.
- section 4 flow: the circled arrows -> ▶, chevrons -> ▼; the two ceremony photos -> photo cells.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kit  # noqa: E402
from kit import Layout, recipe_inputs  # noqa: E402

source, target = recipe_inputs(12, "노동자 참여기반 안전역량 강화")
L = Layout(top=3100)
kit.setup(source, L)
from kit import *  # noqa: E402,F401,F403  helpers and presets bound to this page

LIGHT, MIDGRAY = "#E4E4E4", "#C8C8C8"
TAG = frame("#3C3C3C")


def hang(lines, base):
    """Lines keep their PDF indent: spaces for the x offset and for the line's own leading blanks."""
    out = []
    for line in lines:
        runs = runs_of(line)
        size = runs[0][1] / 100
        raw = "".join(s["text"] for s in line["spans"])
        offset = line["bbox"][0] - base + (len(raw) - len(raw.lstrip(" "))) * 0.29 * size
        n = max(0, round(offset / (0.29 * size)))
        out.append([(" " * n, runs[0][1], False, INK)] + runs if n else runs)
    return out


def joined(lines, sep):
    """PDF splits a spaced label ('참 ... 여', '확 ... 대') into two lines: one paragraph."""
    runs = runs_of(lines[0])
    for line in lines[1:]:
        runs += [(sep, runs[-1][1], runs[-1][2], INK)] + runs_of(line)
    return runs


def section_band(name, num_line, title_line, top):
    g = Grid(name, [X0, 85.5, X1], [2300])
    g.put(X0, 85.5, 0, 1, [runs_of(num_line, WHITE)], frame("#606060"), line=1850)
    g.put(85.5, X1, 0, 1, [title_line], frame(LIGHT), align="LEFT", line=1700)
    block(g, top)


def heading(name, line, top, badge=None, badge_x=None):
    g = Grid(name, [X0, badge_x, X1] if badge else [X0, X1], [1800])
    g.put(X0, badge_x if badge else X1, 0, 1, [line], align="LEFT", line=1600)
    if badge:
        g.put(badge_x, X1, 0, 1, badge, TAG, size=880, bold=True, color=WHITE, line=1000)
    block(g, top)


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
# 3. [근로환경] 가. labels | bullet groups | value charts
# ---------------------------------------------------------------------------
section_band("sec3", line1(64, 70, 72, 78), line1(90, 95, 73, 78), 71.0)
heading("title-3ga", line1(55, 60, 100, 105), 100.0, "지적사항 개선", 503.5)

C1 = (428.0, 444.5, 459.2, 474.0, 490.5)      # chart: edge | tag | half | tag | edge
C2 = (493.5, 510.0, 524.6, 539.1, X1)
xs = [X0, 75.0, 127.5, 131.0, 416.0, 427.0, *C1, *C2]
groups = ((121.8, [1100, 1100, 1000, 1000, 1420]), (178.0, [1100, 1100, 900, 1000, 1400]),
          (233.0, [1100, 1100, 1000, 1000, 1380]))
g = Grid("safety", xs, [h for _, hs in groups for h in hs])
g.put(X0, 75.0, 0, 10, [line1(60, 65, 162, 168), line1(60, 65, 175, 180)],
      frame("#D9D9D9", bottom="soft", right="dot"), bold=True, line=1320)
g.put(X0, 75.0, 10, 15, [line1(60, 65, 248, 253), line1(60, 65, 261, 266)], frame("#D9D9D9"), bold=True,
      line=1320)
g.put(75.0, 127.5, 0, 5, lines_in(77, 80, 136, 156), frame(LIGHT, bottom="dot"), line=1440)
g.put(75.0, 127.5, 5, 10, [lines_in(77, 80, 180, 186)[0], joined(lines_in(77, 115, 195, 200), "      "),
                           lines_in(77, 80, 209, 215)[0]], frame(LIGHT, bottom="soft"), line=1440)
g.put(75.0, 127.5, 10, 15, lines_in(75, 80, 247, 267), frame(LIGHT), line=1440)
for k, (y0, y1) in enumerate(((122, 177), (178, 232), (233, 288))):
    g.put(127.5, 131.0, 5 * k, 5 * k + 5, [], frame(MIDGRAY))
    g.put(131.0, 416.0, 5 * k, 5 * k + 5, hang(lines_in(130, 140, y0, y1), 132.8),
          frame(bottom="soft" if k < 2 else None), align="LEFT", line=1540)
g.put(416.0, 427.0, 0, 5, [], frame("#EFEFEF"))
g.put(416.0, 427.0, 5, 10, "▶", frame("#EFEFEF"), size=900, color="#9A9A9A", fit=False)
g.put(416.0, 427.0, 10, 15, [], frame("#EFEFEF"))

# Value charts (image): tag on top, '24 | '25 values, axis, years, caption from the text layer.
charts = (
    (0, C1, "15명", "7명", "22명", ("’24년", "’25년"), (163, 167, None, 492)),
    (0, C2, "2개소", "5개소", "7개소", ("’24년", "’25년"), (163, 167, 492, None)),
    (1, C1, "3.89점", "0.08점", "3.97점", ("’24년", "’25년"), (218, 222, None, None)),
    (1, C2, "3.79점", "0.2점", "3.99점", ("’24년", "’25년"), (218, 222, None, None)),
    (2, C1, "16.1%", "3.8%p", "12.3%", ("’24년", "’25년"), (273, 277, None, None)),
    (2, C2, "17.4%", "3.6%p", "13.8%", ("그룹사", "KDN"), (273, 277, None, None)))
for k, (a, b, m, c, e), before, rise, after, (y24, y25), (cy0, cy1, cx0, cx1) in charts:
    r = 5 * k
    sep = frame(left="dot") if a > 490 else "1"
    g.put(a, b, r, r + 1, [], sep)
    g.put(b, c, r, r + 1, rise, TAG, size=700, bold=True, color=WHITE, line=880)
    g.put(c, e, r, r + 1, [])
    g.put(a, m, r + 1, r + 2, before, sep, size=750, line=880)
    g.put(m, e, r + 1, r + 2, after, size=750, bold=True, line=880)
    g.put(a, e, r + 2, r + 3, [], frame(bottom="soft", left="dot" if a > 490 else None))
    g.put(a, m, r + 3, r + 4, y24, sep, size=720, line=850)
    g.put(m, e, r + 3, r + 4, y25, size=720, bold=True, line=850)
    hits = lines_in(a - 3, e, cy0, cy1) or lines_in(425, 500 if a < 490 else 560, cy0, cy1)
    runs = runs_of(hits[0], x0=cx0 if cx0 else -1e9, x1=cx1 if cx1 else 1e9)
    g.put(a, e, r + 4, r + 5, [runs], frame("#E9E9E9", hatch="#DCDCDC", left="dot" if a > 490 else None),
          line=1050)
block(g, 121.8)

# ---------------------------------------------------------------------------
# 나. four cards: tag + quote, finding, detail (+ illustration), result band
# ---------------------------------------------------------------------------
heading("title-3na", line1(55, 60, 296, 301), 296.8)
cards = ((X0, 89.5, 135.0, 180.5), (182.0, 215.5, None, 305.0), (307.0, 340.5, 389.0, 430.5),
         (432.5, 465.0, 524.0, X1))
k2 = [182.0, 186.0, 210.0, 215.5, 241.0, 244.5, 268.0, 273.0, 300.0, 305.0]
xs = sorted({X0, 89.5, 135.0, 180.5, *k2, 307.0, 340.5, 389.0, 430.5, 432.5, 465.0, 524.0, X1})
g = Grid("cards", xs, [2030, 1450, 1300, 2300, 450, 1900])
for i, (a, t, p, e) in enumerate(cards):
    head = lines_in(a, a + 12, 320, 326)[0]
    split = head["spans"][1]["bbox"][0] - 0.5
    g.put(a, t, 0, 1, [runs_of(head, x1=split)], frame("#DCDCDC", top="strong", left="mid"))
    g.put(t, e, 0, 1, [strip_runs(runs_of(head, x0=split))], frame(top="strong", right="mid"), align="LEFT")
    first = sorted(lines_in(a, e, 338, 344), key=lambda l: l["bbox"][0])
    runs = runs_of(first[0])
    for extra in first[1:]:
        runs += runs_of(extra)
    g.put(a, e, 1, 2, [runs], frame(left="mid", right="mid"))
    g.put(a, e, 4, 5, [], frame(left="mid", right="mid"))
    g.put(a, e, 5, 6, [line1(a, e, 395, 400)], frame(LIGHT, left="mid", right="mid", bottom="mid"))
    if p:
        g.put(a, p, 2, 4, lines_in(a, p, 355, 380), frame(left="mid"), line=1400)
        caption = [[("고압 전선", 520, True, INK)], [("작업용 로봇팔", 520, True, INK)]] if i == 0 else []
        g.put(p, e, 2, 4, caption, frame("#E4E4E4", right="mid"), align="RIGHT", line=620)
# card 2: labelled illustrations (image text typed), drawings as photo cells
box = frame(top="soft", bottom="soft", left="soft", right="soft")
g.put(182.0, 186.0, 2, 4, [], frame(left="mid"))
g.put(186.0, 210.0, 2, 3, "체결고리", box, size=700, line=820)
g.put(210.0, 215.5, 2, 3, "▶", size=600, line=700, fit=False)
g.put(215.5, 241.0, 2, 3, "고정나사", frame("#6A6A6A"), size=700, color=WHITE, line=820)
g.put(241.0, 244.5, 2, 4, [], frame(right="dot"))
g.put(244.5, 268.0, 2, 3, "단일그립", box, size=700, line=820)
g.put(268.0, 273.0, 2, 3, "▶", size=600, line=700, fit=False)
g.put(273.0, 300.0, 2, 3, "이중그립", frame("#6A6A6A"), size=700, color=WHITE, line=820)
g.put(300.0, 305.0, 2, 4, [], frame(right="mid"))
g.put(186.0, 241.0, 3, 4, [], frame("#E4E4E4"))
g.put(244.5, 300.0, 3, 4, [], frame("#E4E4E4"))
block(g, 318.2)

# ---------------------------------------------------------------------------
# 4. [건설･협력사] 가. 협력사 / 건설사 안전 예산
# ---------------------------------------------------------------------------
section_band("sec4", line1(64, 70, 432, 437), line1(90, 95, 433, 438), 431.5)
heading("title-4ga", line1(55, 60, 460, 465), 460.5)

steps = ((111.0, 217.5), (221.0, 330.0), (334.0, 443.0), (447.0, X1))
heads = ((108.0, 217.5), (231.0, 330.0), (344.0, 443.0), (456.5, X1))
arrows = ((217.5, 231.0), (330.0, 344.0), (443.0, 456.5))
xs = sorted({X0, 105.5, 108.0, *[x for s in steps for x in s], *[x for h in heads for x in h]})
g = Grid("budget", xs, [2000, 1900, 680, 3020])
g.put(X0, 105.5, 0, 4, lines_in(58, 62, 500, 535), frame(LIGHT), bold=True, line=1320)
shades = ("#E8E8E8", "#DEDEDE", "#D4D4D4", "#CACACA")
for k, ((a, e), (ha, he), shade) in enumerate(zip(steps, heads, shades)):
    g.put(ha, he, 0, 1, [line1(ha, he, 484, 490)], frame(shade))
    if k < 3:
        g.put(*arrows[k], 0, 1, "▶", frame(shade), size=800, color="#8A8A8A")
    g.put(a, e, 1, 2, [line1(a - 5, e, 505, 510)], frame(left="soft" if k else None))
    g.put(a, e, 2, 3, "▼", size=500, color="#9A9A9A", line=500)
    g.put(a, e, 3, 4, hang(lines_in(a - 2, e, 527, 548), {0: 110.8, 1: 223.7, 2: 336.7, 3: 449.6}[k]),
          frame("#E6E6E6"), align="LEFT", line=1430)
block(g, 482.0)

g = Grid("budget-arrow", [X0, 105.5, 295.0, 318.0, X1], [1300])
g.put(295.0, 318.0, 0, 1, "▼", size=1000, color="#8A8A8A", line=1100)
block(g, 561.5)

xs = [X0, 105.5, 108.0, 112.5, 156.0, 447.0, X1]
g = Grid("construction", xs, [1850, 1600, 2050])
g.put(X0, 105.5, 0, 3, [lines_in(58, 62, 588, 593)[0], lines_in(58, 62, 601, 606)[0],
                        joined(lines_in(58, 95, 615, 620), "         ")], frame(LIGHT), bold=True, line=1320)
g.put(108.0, X1, 0, 1, [line1(108, 115, 582, 588)], frame("#E6E6E6", top="strong", left="mid", right="mid"))
for r, y in ((1, 603), (2, 619)):
    row = line1(112, 120, y - 1, y + 2)
    split = row["spans"][1]["bbox"][0] - 0.5
    g.put(108.0, 112.5, r, r + 1, [], frame(left="mid", bottom="mid" if r == 2 else None))
    g.put(112.5, 156.0, r, r + 1, [runs_of(row, x1=split)], frame("#DCDCDC"), line=1050)
    g.put(156.0, 447.0, r, r + 1, [strip_runs(runs_of(row, x0=split))], frame(bottom="mid" if r == 2 else None),
          align="LEFT")
    g.put(447.0, X1, r, r + 1, [line1(450, 455, y - 2, y + 3)],
          frame(left="dot", right="mid", bottom="mid" if r == 2 else None), align="LEFT")
block(g, 580.0)

# ---------------------------------------------------------------------------
# 나. 협력사 안전 역량 고도화: two boxes with photos, 안전체계진단 band
# ---------------------------------------------------------------------------
heading("title-4na", line1(55, 60, 643, 648), 642.8)
xs = [X0, 105.5, 108.0, 176.5, 249.0, 328.5, 333.0, 414.0, X1]
g = Grid("partners", xs, [1950, 5050, 200, 2300])
g.put(X0, 105.5, 0, 4, lines_in(58, 62, 690, 725), frame(LIGHT), bold=True, line=1320)
g.put(108.0, 328.5, 0, 1, [line1(120, 130, 666, 672)], frame("#E0E0E0", top="mid", left="mid", right="mid"))
g.put(333.0, X1, 0, 1, [line1(340, 350, 666, 672)], frame("#E0E0E0", top="mid", left="mid", right="mid"))
g.put(108.0, 249.0, 1, 2, hang(lines_in(110, 120, 684, 730), 113.6), frame(left="mid", bottom="mid"),
      align="LEFT", line=1540)
g.put(249.0, 328.5, 1, 2, [], frame("#E4E4E4", right="mid", bottom="mid"))
g.put(333.0, 414.0, 1, 2, [], frame("#E4E4E4", left="mid", bottom="mid"))
g.put(414.0, X1, 1, 2, hang(lines_in(412, 435, 684, 730), 415.4), frame(right="mid", bottom="mid"),
      align="LEFT", line=1540)
g.put(108.0, 176.5, 3, 4, [line1(110, 115, 740, 745)], frame(WHITE, top="soft", bottom="soft", left="soft", right="soft"))
g.put(176.5, X1, 3, 4, [line1(176, 180, 737, 742)], frame("#E9E9E9"), align="LEFT")
block(g, 664.0)

g = Grid("result", [X0, 112.5, X1], [3700])
g.put(X0, 112.5, 0, 1, [runs_of(line1(64, 70, 776, 781), WHITE)], frame("#6A6A6A", top="mid", bottom="mid", left="mid"))
g.put(112.5, X1, 0, 1, lines_in(115, 120, 765, 790), frame(top="mid", bottom="mid", right="mid"), align="LEFT",
      line=1500)
block(g, 765.0)

kit.finish(target, end=802.0)
