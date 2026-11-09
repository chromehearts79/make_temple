"""Rebuild KDN 2025 report physical PDF page 65 (printed page 42) as editable HWPX.

Usage: python3 work/kdn2025/p65.py <report.pdf> <out.hwpx> [--page N]
(the second PDF holds report pages 51-100, so this page is local page 15 there)

안전 및 재난관리 section 3 (가. 사이버 안전센터 / 나. 기반시설 제어망 / 다. 은폐형 단선).
Built with the shared kit (one flat table per horizontal band on a grid of PDF x edges); all
body text comes from the PDF text layer (fragments split at superscripts merged back into one
paragraph). Images: the section number band, the side tab, the boxed 1 2 3 of the 가. cards
(-> ① ② ③), the circled step arrows and the chevron (-> ▶), the ➡ in front of '데이터 수집…'
(-> →), the 'Best Practice' sticker (trophy icon dropped, typed as a dark tag), the cover of the
가이드라인 (its title read from an 8x render and typed small into a photo cell), the 업무협약서
thumbnail (photo cell holding its text-layer title; its tiny body text is not typed) and the
broken-wire illustration (empty photo cell).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kit  # noqa: E402
from kit import Layout, recipe_inputs  # noqa: E402

source, target = recipe_inputs(15, "통합 관제로 재난")
L = Layout(top=3100)
kit.setup(source, L)
from kit import *  # noqa: E402,F401,F403  helpers and presets bound to this page

DARK, LABEL = "#6A6A6A", "#E6E6E6"
SIDE = "#E4E4E4"                      # 추진실적 / 추진경과 label column
HEAD, BODY = "#D8D8D8", "#F4F4F4"     # card header / card body
LAB = 91.0                            # label column end


def rows_in(x0, x1, y0, y1, base):
    """Text rows of a region: fragments of one visual row (split at superscripts) are merged,
    and the row keeps its PDF indent as leading spaces (offset from `base`)."""
    hits = sorted((l for l in LINES if x0 <= l["bbox"][0] < x1 and y0 <= l["bbox"][1] < y1),
                  key=lambda l: (l["bbox"][1], l["bbox"][0]))
    groups = []
    for l in hits:
        for grp in groups:
            top, bottom = min(g["bbox"][1] for g in grp), max(g["bbox"][3] for g in grp)
            if l["bbox"][1] < bottom - 2 and l["bbox"][3] > top + 2:
                grp.append(l)
                break
        else:
            groups.append([l])
    out = []
    for grp in groups:
        grp.sort(key=lambda l: l["bbox"][0])
        merged = dict(bbox=grp[0]["bbox"], spans=[s for l in grp for s in l["spans"]])
        runs = runs_of(merged)
        size = runs[0][1] / 100
        raw = "".join(s["text"] for s in grp[0]["spans"])
        offset = grp[0]["bbox"][0] - base + (len(raw) - len(raw.lstrip(" "))) * 0.29 * size
        n = max(0, round(offset / (0.29 * size)))
        if n:
            runs = [(" " * n, runs[0][1], False, INK)] + runs
        out.append(runs)
    return out


def section_band(name, num_line, title_line, top):
    g = Grid(name, [X0, 84.5, X1], [2300])
    g.put(X0, 84.5, 0, 1, [runs_of(num_line, WHITE)], frame(DARK), line=1700)
    g.put(84.5, X1, 0, 1, [runs_of(title_line)], frame(LABEL), align="LEFT", line=1700)
    block(g, top)


def heading(name, line, top, tag=None, tag_x=485.8):
    edges = [X0, tag_x, X1] if tag else [X0, X1]
    g = Grid(name, edges, [1650])
    g.put(X0, edges[1], 0, 1, [runs_of(line)], align="LEFT", line=1450)
    if tag:
        g.put(tag_x, X1, 0, 1, tag, frame("#3C3C3C"), size=900, bold=True, color=WHITE, line=1000)
    block(g, top)


def boxed(name, label_line, body, top, height, label_fill="#CECECE", label_color=INK, body_fill="#F2F2F2"):
    """추진배경 / 주요성과 box: label at left, outlined body with bullet lines."""
    g = Grid(name, [X0, 114.7, X1], [height])
    g.put(X0, 114.7, 0, 1, [runs_of(label_line, label_color)],
          frame(label_fill, top="mid", bottom="mid", left="mid"))
    g.put(114.7, X1, 0, 1, body, frame(body_fill, top="mid", bottom="mid", right="mid"), align="LEFT", line=1540)
    block(g, top)


def side_label(g, r0, r1, y):
    """Two-line bold label (추진 / 실적, 추진 / 경과) of a block, from the text layer."""
    g.put(X0, LAB, r0, r1, [line1(60, 70, y, y + 4), line1(60, 70, y + 13, y + 17)], frame(SIDE), line=1320)


def result_bar(name, label_y, line, top, height=2500):
    """성과: darker label and a light bar with one centred line."""
    g = Grid(name, [X0, LAB, 93.5, X1], [height])
    g.put(X0, LAB, 0, 1, [line1(60, 70, label_y, label_y + 4)], frame("#B4B4B4"))
    g.put(93.5, X1, 0, 1, [line], frame("#E0E0E0"))
    block(g, top)


def tight(g, x0, r0, left=0, right=0):
    c0 = g.xs.index(to_x(x0))
    item = g.items[r0, c0]
    g.items[r0, c0] = (*item[:7], dict(left=left, right=right))


def card_head():
    return frame(HEAD, top="mid", bottom="mid", left="mid", right="mid")


def card_body(fill=BODY):
    return frame(fill, bottom="mid", left="mid", right="mid")


TAG_BOX = frame(WHITE, top="soft", bottom="soft", left="soft", right="soft")
TAG_DARK = frame("#4A4A4A")

# ---------------------------------------------------------------------------
# Page chrome (odd page): running head over a rule, side tab, footer at the right.
# ---------------------------------------------------------------------------
L.add_table([[cell(0, 3350, 1680, [para([("01", 1380, True, WHITE)], "CENTER")[0]], dark)],
             [cell(0, 3350, 5960, [para([(ch, 950, True, INK)], "CENTER", 1160)[0] for ch in "경영관리"], gray2)]],
            floating=(57800, 15000))
foot = [(text, size, False, INK) for text, size in (
    (line1(450, 455, 818, 822)["text"], 790), ("    ", 790), (line1(540, 552, 816, 820)["text"], 1090))]
L.add_table([[cell(0, W, 1500, [para(foot, "RIGHT", 1300)[0]])]], floating=(5660, 81550))

g = Grid("head", [X0, 398.0, X1], [1680])
g.put(X0, 398.0, 0, 1, [], frame(bottom="soft"))
g.put(398.0, X1, 0, 1, [line1(400, 410, 35, 40)], align="RIGHT")
block(g, 32.0)

section_band("sec3", line1(60, 70, 72, 76), line1(90, 95, 72, 77), 70.9)

# ---------------------------------------------------------------------------
# 가. 사이버 안전센터
# ---------------------------------------------------------------------------
heading("title-ga", line1(55, 60, 100, 105), 100.7)
boxed("bg-ga", line1(65, 70, 134, 138), lines_in(115, 120, 125, 150), 123.2, 3710)

CARD = [(93.5, 245.9, 99.4), (248.4, 400.9, 254.3), (403.3, X1, 409.2)]
g = Grid("act-ga", [X0, LAB] + [x for c in CARD for x in c[:2]], [1930, 5200])
side_label(g, 0, 2, 190)
for k, (a, e, base) in enumerate(CARD):
    title = line1(a, e, 169, 173)
    g.put(a, e, 0, 1, [[("①②③"[k] + " ", 1090, True, INK)] + runs_of(title)], card_head(), line=1250)
    g.put(a, e, 1, 2, rows_in(a, e, 188, 236, base), card_body(), align="LEFT", line=1440)
block(g, 166.5)

result_bar("res-ga", 250, line1(110, 116, 247, 252), 244.5)

# ---------------------------------------------------------------------------
# 나. 기반시설 제어망 (Best Practice)
# ---------------------------------------------------------------------------
heading("title-na", line1(55, 60, 279, 284), 279.2, tag="Best Practice")
boxed("bg-na", line1(65, 70, 313, 317), lines_in(115, 120, 304, 330), 302.0, 3680)

# 추진경과: 위협 증가 ▶ '24년 개발 ▶ '25년 실증 (graded header), tagged findings and bullets
xs = [X0, LAB, 93.5, 97.0, 114.6, 238.1, 241.0, 255.4, 285.0, 399.7, 401.8, 416.9, 445.3, X1]
g = Grid("flow-na", xs, [1860, 250, 1470, 1470, 1470, 240])
side_label(g, 0, 6, 366)
g.put(93.5, 238.1, 0, 1, [line1(110, 114, 347, 351)], frame("#EEEEEE", top="mid", left="mid"))
g.put(238.1, 255.4, 0, 1, "▶", frame("#E4E4E4", top="mid"), size=900, color="#8C8C8C", fit=False)
for (a, b, e, fill, cut) in ((255.4, 285.0, 399.7, "#E0E0E0", 284.0), (416.9, 445.3, X1, "#D2D2D2", 444.0)):
    line = line1(a, a + 8, 346, 350)
    g.put(a, b, 0, 1, [runs_of(line, x1=cut)], frame(WHITE, top="soft", bottom="soft", left="soft", right="soft"),
          line=1050, ratio=88, fit=False)
    tight(g, a, 0, 0, 0)
    g.put(b, e, 0, 1, [strip_runs(runs_of(line, x0=cut))], frame(fill, top="mid", right="mid" if e == X1 else None),
          align="LEFT", line=1250)
g.put(399.7, 416.9, 0, 1, "▶", frame("#D8D8D8", top="mid"), size=900, color="#8C8C8C", fit=False)
# column 1: 현황 / 문제 / 역량 tags (outlined) + text
g.put(93.5, 241.0, 1, 2, [], frame(left="mid"))
g.put(93.5, 241.0, 5, 6, [], frame(left="mid", bottom="mid"))
for r, y in zip((2, 3, 4), (367.6, 382.3, 397.0)):
    line = line1(97, 100, y - 1, y + 1)
    g.put(93.5, 97.0, r, r + 1, [], frame(left="mid"))
    g.put(97.0, 114.6, r, r + 1, [runs_of(line, x1=114.0)], TAG_BOX, line=1050, ratio=88, fit=False)
    tight(g, 97.0, r)
    g.put(114.6, 241.0, r, r + 1, [strip_runs(runs_of(line, x0=114.0))], align="LEFT", line=1300)
# column 2: bullets, the ➡ line becomes '→ '
mid = rows_in(241.0, 401.8, 365, 410, 246.2)
mid = [[("→ ", r[0][1], False, INK)] + r[1:] if r[0][0].isspace() else r for r in mid]
g.put(241.0, 401.8, 1, 6, mid, frame(left="soft", bottom="mid"), align="LEFT", line=1440)
g.put(401.8, X1, 1, 6, rows_in(401.8, X1, 365, 410, 407.2), frame(left="soft", right="mid", bottom="mid"),
      align="LEFT", line=1440)
block(g, 345.2)

# 추진실적: two boxes (가이드라인 cover, 업무협약서 thumbnail)
xs = [X0, LAB, 93.5, 269.5, 321.0, 323.9, 326.0, 328.9, 379.2, X1]
g = Grid("act-na", xs, [1800, 3870])
side_label(g, 0, 2, 435)
g.put(93.5, 323.9, 0, 1, [line1(95, 100, 421, 425)], card_head(), line=1250)
g.put(326.0, X1, 0, 1, [line1(330, 334, 421, 425)], card_head(), line=1250)
g.put(93.5, 269.5, 1, 2, rows_in(93.5, 269.5, 440, 472, 99.4), frame(BODY, left="mid", bottom="mid"),
      align="LEFT", line=1540)
g.put(269.5, 321.0, 1, 2, [[("제어시스템 보안 모니터링", 560, True, INK)], [("구축 가이드라인", 560, True, INK)]],
      frame("#E4E4E4", bottom="mid"), align="LEFT", line=700)
g.put(321.0, 323.9, 1, 2, [], frame(BODY, right="mid", bottom="mid"))
g.put(326.0, 328.9, 1, 2, [], frame(BODY, left="mid", bottom="mid"))
g.put(328.9, 379.2, 1, 2, [line1(338, 342, 444, 447)], frame("#E4E4E4", bottom="mid"), line=800)
g.put(379.2, X1, 1, 2, rows_in(379.2, X1, 440, 472, 382.1), frame(BODY, right="mid", bottom="mid"), align="LEFT",
      line=1440)
block(g, 419.8)

result_bar("res-na", 489, line1(100, 105, 487, 492), 483.2)

# ---------------------------------------------------------------------------
# 다. 은폐형 단선
# ---------------------------------------------------------------------------
heading("title-da", line1(55, 60, 516, 521), 517.0)
boxed("bg-da", line1(65, 70, 550, 555), lines_in(115, 120, 541, 570), 539.5, 3700)

# 추진경과: risk box (illustration + outlined tags) ▶ technology box (dark tags), footnote
xs = [X0, LAB, 93.5, 150.3, 152.0, 168.6, 293.5, 307.0, 313.0, 330.0, X1]
g = Grid("flow-da", xs, [1780, 200, 1450, 1450, 1450, 430, 1640])
side_label(g, 0, 7, 612)
g.put(93.5, 293.5, 0, 1, [line1(95, 98, 586, 590)], card_head(), line=1250)
g.put(307.0, X1, 0, 1, [line1(335, 338, 586, 590)], card_head(), line=1250)
g.put(93.5, 150.3, 1, 6, [], frame("#E4E4E4", left="mid", bottom="mid"))
g.put(150.3, 152.0, 1, 6, [], frame(bottom="mid"))
g.put(152.0, 293.5, 1, 2, [], frame(right="mid"))
g.put(152.0, 293.5, 5, 6, [], frame(right="mid", bottom="mid"))
g.put(307.0, X1, 1, 2, [], frame(left="mid", right="mid"))
g.put(307.0, X1, 5, 6, [], frame(left="mid", right="mid", bottom="mid"))
for r, y in zip((2, 3, 4), (606.9, 621.5, 636.0)):
    # left box
    line = lines_in(152.0, 293.5, y - 1, y + 1)[0]
    if line["bbox"][0] < 160:
        g.put(152.0, 168.6, r, r + 1, [runs_of(line, x1=168.0)], TAG_BOX, line=1050, ratio=88, fit=False)
        tight(g, 152.0, r)
        g.put(168.6, 293.5, r, r + 1, [strip_runs(runs_of(line, x0=168.0))], frame(right="mid"), align="LEFT",
              line=1250)
    else:
        g.put(152.0, 168.6, r, r + 1, [])
        g.put(168.6, 293.5, r, r + 1, [line], frame(right="mid"), align="LEFT", line=1250)
    # right box
    line = lines_in(307.0, X1, y - 1, y + 1)[0]
    g.put(307.0, 313.0, r, r + 1, [], frame(left="mid"))
    if line["bbox"][0] < 320:
        g.put(313.0, 330.0, r, r + 1, [runs_of(line, WHITE, x1=330.5)], TAG_DARK, line=1050, ratio=88, fit=False)
        tight(g, 313.0, r)
        g.put(330.0, X1, r, r + 1, [strip_runs(runs_of(line, x0=330.5))], frame(right="mid"), align="LEFT", line=1250)
    else:
        g.put(313.0, 330.0, r, r + 1, [])
        g.put(330.0, X1, r, r + 1, [line], frame(right="mid"), align="LEFT", line=1250)
g.put(293.5, 307.0, 1, 6, "▶", size=1100, color=ARROW, fit=False)
g.put(LAB, X1, 6, 7, [line1(92, 95, 655, 659)], align="LEFT", line=1100)
tight(g, LAB, 6, 150, 0)
block(g, 584.2)

# 추진실적: two boxes
B = [(93.5, 312.4, 99.4, 115.9), (314.4, X1, 320.4, 323.0)]
g = Grid("act-da", [X0, LAB, 93.5, 312.4, 314.4, X1], [1800, 3420])
side_label(g, 0, 2, 688)
for a, e, base, hx in B:
    g.put(a, e, 0, 1, [line1(hx - 1, hx + 1, 676, 680)], card_head(), line=1250)
    g.put(a, e, 1, 2, rows_in(a, e, 695, 725, base), card_body(), align="LEFT", line=1430)
block(g, 675.0)

result_bar("res-da", 740, line1(120, 126, 738, 742), 733.5, 2530)

boxed("result", line1(65, 70, 776, 780), lines_in(115, 120, 768, 800), 766.0, 3550,
      label_fill="#787878", label_color=WHITE, body_fill=WHITE)

kit.finish(target, end=803.0)
