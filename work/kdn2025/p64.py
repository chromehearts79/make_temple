"""Rebuild KDN 2025 report physical PDF page 64 (printed page 41) as editable HWPX.

Usage: python3 work/kdn2025/p64.py <report.pdf> <out.hwpx> [--page N]
(the second PDF holds report pages 51-100, so this page is local page 14 there)

안전 및 재난관리 section 2 (가. 6대 위기 유형 / 나. 재난관리 全 주기 / 다. 재해복구·업무 연속성).
Built with the shared kit (one flat table per horizontal band on a grid of PDF x edges); all
text comes from the PDF text layer, line fragments split by superscripts are merged back into
one paragraph. Images: the PART box, the section number band, the '지적사항 개선' sticker (hand
icon dropped), the circled step arrows (-> ▶), the stage chevrons of the 나. table (-> filled
stage cells), the circled ① ② ③ of the 역량강화 cards (typed), the four 복구훈련 photos (the
second one is a screenshot of the alert document; all four become empty photo cells) and the
footer logo (typed as 한전KDN㈜).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kit  # noqa: E402
from kit import Layout, recipe_inputs  # noqa: E402

source, target = recipe_inputs(14, "조직 특성에 맞춘 위기유형 재정립과 선제 대응으로 대국민 재난 예방")
L = Layout(top=3100)
kit.setup(source, L)
from kit import *  # noqa: E402,F401,F403  helpers and presets bound to this page

DARK, LABEL = "#6A6A6A", "#E6E6E6"
BG_LABEL, BG_BODY = "#D8D8D8", "#F2F2F2"


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
    """'2 | heading' band: dark number cell and light gray title cell (images in the PDF)."""
    g = Grid(name, [X0, 84.5, X1], [2300])
    g.put(X0, 84.5, 0, 1, [runs_of(num_line, WHITE)], frame(DARK), line=1700)
    g.put(84.5, X1, 0, 1, [runs_of(title_line)], frame(LABEL), align="LEFT", line=1700)
    block(g, top)


def heading(name, line, top, tag=None):
    """'가. title' (14 pt, text layer) with an optional dark sticker at the right."""
    edges = [X0, 503.8, X1] if tag else [X0, X1]
    g = Grid(name, edges, [1650])
    g.put(X0, edges[1], 0, 1, [runs_of(line)], align="LEFT", line=1450)
    if tag:
        g.put(503.8, X1, 0, 1, tag, frame("#3C3C3C"), size=900, bold=True, color=WHITE, line=1000)
    block(g, top)


def boxed(name, label_line, body, top, height, label_fill=BG_LABEL, label_color=INK, body_fill=BG_BODY):
    """추진배경 / 주요성과 box: label at left, outlined body with bullet lines."""
    g = Grid(name, [X0, 114.7, X1], [height])
    g.put(X0, 114.7, 0, 1, [runs_of(label_line, label_color)],
          frame(label_fill, top="mid", bottom="mid", left="mid"))
    g.put(114.7, X1, 0, 1, body, frame(body_fill, top="mid", bottom="mid", right="mid"), align="LEFT", line=1540)
    block(g, top)


# ---------------------------------------------------------------------------
# Page chrome (even page): PART box with rule, footer page number + KDN logo (typed).
# ---------------------------------------------------------------------------
foot = [(line1(55, 60, 816, 820)["text"], 1090, False, INK), ("    ", 790, False, INK),
        ("한전KDN㈜", 1090, True, INK)]
L.add_table([[cell(0, W, 1500, [para(foot, "LEFT", 1300)[0]])]], floating=(5660, 81550))

g = Grid("head", [X0, 99.0, 158.5, X1], [1680])
g.put(X0, 99.0, 0, 1, [[("PART ", 800, False, INK), ("01", 1300, True, INK)]], frame("#EFEFEF", top="strong"))
g.put(99.0, 158.5, 0, 1, "경영관리", frame("#333333"), size=1080, bold=True, color=WHITE)
g.put(158.5, X1, 0, 1, [], frame(bottom="soft"))
block(g, 32.0)

section_band("sec2", line1(60, 70, 72, 76), line1(90, 95, 73, 77), 70.9)

# ---------------------------------------------------------------------------
# 가. 6대 위기 유형 재난대응 체계
# ---------------------------------------------------------------------------
heading("title-ga", line1(55, 60, 100, 106), 100.8, tag="지적사항 개선")
boxed("bg-ga", line1(65, 70, 134, 138), lines_in(115, 120, 125, 150), 123.2, 3710)

# 정비 → 정립 → 확산: three graded segments, boxed tag + bold title, ▶ between
SEG = [(56.6, 60.2, 78.4, 222.4), (237.1, 239.6, 257.6, 389.5), (404.3, 407.8, 425.9, X1)]
xs = sorted({x for s in SEG for x in s})
g = Grid("steps", xs, [2020])
tag_frame = frame(WHITE, top="soft", bottom="soft", left="soft", right="soft")
for (a, b, c, e), fill, x in zip(SEG, ("#E6E6E6", "#DCDCDC", "#D2D2D2"), (61.9, 240.9, 409.3)):
    line = line1(x - 1, x + 1, 169, 173)
    g.put(a, b, 0, 1, [], frame(fill))
    g.put(b, c, 0, 1, [runs_of(line, x1=c)], tag_frame, line=1050, ratio=85, fit=False)
    g.put(c, e, 0, 1, [strip_runs(runs_of(line, x0=c))], frame(fill), align="LEFT", line=1250)
for a, e in ((222.4, 237.1), (389.5, 404.3)):
    g.put(a, e, 0, 1, "▶", size=900, color="#8C8C8C", fit=False)
for k, (a, b, c, e) in enumerate(SEG):
    item = g.items[0, g.xs.index(to_x(b))]
    g.items[0, g.xs.index(to_x(b))] = (*item[:7], dict(left=0, right=0))
block(g, 166.6)

# Three columns: actions (white) over results (gray), thin rules between the columns
COL = [(X0, 222.2, 59.7), (222.2, 389.7, 227.3), (389.7, X1, 394.9)]
g = Grid("steps-body", [X0, 222.2, 389.7, X1], [5030, 4060])
for k, (a, e, base) in enumerate(COL):
    left = dict(left="soft") if k else {}
    g.put(a, e, 0, 1, rows_in(a, e, 188, 236, base), frame(**left), align="LEFT", line=1540)
    g.put(a, e, 1, 2, rows_in(a, e, 244, 276, base), frame("#E4E4E4", bottom="mid", **left), align="LEFT",
          line=1540)
block(g, 187.8)

# ---------------------------------------------------------------------------
# 나. 재난관리 全 주기 (예방·대비·대응·복구) table
# ---------------------------------------------------------------------------
heading("title-na", line1(55, 60, 291, 296), 291.6)
boxed("bg-na", line1(65, 70, 325, 329), lines_in(115, 120, 316, 340), 314.1, 3720)

TX = [X0, 85.2, 326.0, X1]
STAGES = [(376.0, 413.0, "#E4E4E4", INK), (413.0, 450.0, "#C0C0C0", INK), (450.0, 486.6, "#A8A8A8", INK),
          (486.6, 523.8, "#9C9C9C", WHITE)]
hs = [1880] + [int(round((b - a) * 100)) for a, b, *_ in STAGES]
g = Grid("cycle", TX, hs)
head = frame("#CCCCCC", top="strong", bottom="soft")
for (a, e), x in zip(zip(TX, TX[1:]), (61.6, 185.5, 420.7)):
    g.put(a, e, 0, 1, [line1(x - 1, x + 1, 359, 363)], head)
for k, (a, b, fill, color) in enumerate(STAGES):
    r = k + 1
    last = r == len(STAGES)
    rule = "strong" if last else "soft"
    g.put(X0, 85.2, r, r + 1, [runs_of(line1(60, 65, a, b), color)], frame(fill, bottom=rule))
    g.put(85.2, 326.0, r, r + 1, rows_in(85.2, 326.0, a, b, 88.0), frame(bottom=rule), align="LEFT",
          line=1550)
    g.put(326.0, X1, r, r + 1, rows_in(326.0, X1, a, b, 329.0), frame(bottom=rule, left="soft"), align="LEFT",
          line=1550)
block(g, 357.2)

# ---------------------------------------------------------------------------
# 다. 재해복구(DR)와 업무 연속성
# ---------------------------------------------------------------------------
heading("title-da", line1(55, 60, 533, 538), 533.6)
boxed("bg-da", line1(65, 70, 567, 571), lines_in(115, 120, 558, 582), 556.0, 3720)

# 역량강화: three numbered cards
CARD = [(93.5, 245.9, 99.4), (248.4, 400.9, 254.3), (403.3, X1, 409.2)]
g = Grid("capacity", [X0, 91.0, 93.5, 245.9, 248.4, 400.9, 403.3, X1], [1740, 5370])
g.put(X0, 91.0, 0, 2, [line1(60, 70, 623, 627), line1(60, 70, 636, 640)], frame("#E4E4E4"), line=1320)
for k, (a, e, base) in enumerate(CARD):
    title = line1(a, e, 602, 606)
    g.put(a, e, 0, 1, [[("①②③"[k] + " ", 1060, True, INK)] + runs_of(title)],
          frame(BG_LABEL, top="mid", bottom="mid", left="mid", right="mid"), line=1250)
    g.put(a, e, 1, 2, rows_in(a, e, 620, 668, base), frame(BG_BODY, bottom="mid", left="mid", right="mid"),
          align="LEFT", line=1540)
block(g, 599.4)

# 복구훈련: four photos with captions, ▶ between them
PH = [(93.5, 198.8), (212.6, 317.8), (331.6, 436.9), (450.7, X1)]
xs = [X0, 91.0] + [x for p in PH for x in p]
g = Grid("drill", xs, [1730, 400, 5670, 310])
g.put(X0, 91.0, 0, 4, [line1(60, 70, 705, 709), line1(60, 70, 718, 722)], frame("#E4E4E4"), line=1320)
for k, (a, e) in enumerate(PH):
    g.put(a, e, 0, 1, [line1(a, e, 680, 684)], frame(BG_LABEL, top="mid", bottom="mid", left="mid", right="mid"),
          line=1250)
    g.put(a, e, 2, 3, [], photo)
    g.put(a, e, 3, 4, [], frame(top="mid"))
    if k < 3:
        g.put(e, PH[k + 1][0], 2, 3, "▶", size=1000, color=ARROW, fit=False)
block(g, 677.2)

boxed("result", line1(65, 70, 776, 780), lines_in(115, 120, 767, 800), 764.6, 3710,
      label_fill="#787878", label_color=WHITE, body_fill=WHITE)

kit.finish(target, end=803.0)
