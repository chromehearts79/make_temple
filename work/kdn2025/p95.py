"""Rebuild KDN 2025 report page 95 (PDF 2 local page 45, printed page 65) as editable HWPX.

Usage: python3 work/kdn2025/p95.py <report2.pdf> <out.hwpx> [--page 45]

상생·협력 및 지역발전 평가내용 03 opening page (시설·장비 개방). Built with the shared diagram kit
(one flat table per horizontal band on a grid of PDF x edges). Text comes from the PDF text layer
except these image-only parts, typed from 5x renders: the 평가내용 03 chip (its check icon dropped),
the ①-④ number boxes of 실행과제, the '지적사항 개선' sticker, and the labels of the 개방 지역
현황 map ('24년 1개소, '25년 3개소, 서 울, 충북, 전북, 나주; the map outline and pins are left
out). The 개방 공간 현황 photo is an empty photo cell; the circled arrows become ▶, the down
pointers ▼, the (+) joint "+", the hexagon badges dark cells. The source draws two middle dots
with Wingdings U+F09E (산업단지·타기관, 창업·벤처); they are kept as that character in a Wingdings
run so they print as in the PDF.
"""

import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kit  # noqa: E402
from kit import Layout, recipe_inputs  # noqa: E402

source, target = recipe_inputs(45, "공공기관 보유 시설")
L = Layout(top=3100)
kit.setup(source, L)
from kit import *  # noqa: E402,F401,F403  helpers and presets bound to this page

DARK, BAND = "#6A6A6A", "#E5E5E5"
SIDE = "#EDEDED"
HEADC = "#D9D9D9"
WING = "#16161A"       # run colour marking the Wingdings U+F09E dot; re-mapped in finish
BOX = frame(WHITE, top="soft", bottom="soft", left="soft", right="soft")
HATCH = frame("#E9E9E9", hatch="#D9D9D9")


def wing(runs):
    """Split the Wingdings middle dot (U+F09E) into its own marked run."""
    out = []
    for text, size, bold, color in runs:
        parts = text.split("")
        for k, part in enumerate(parts):
            if k:
                out.append(("", size, bold, WING))
            if part:
                out.append((part, size, bold, color))
    return out


def hang(lines, base):
    """Bullet lines keep their PDF indent: spaces for the x offset and for the line's own lead."""
    out = []
    for l in lines:
        runs = runs_of(l)
        size = runs[0][1] / 100
        raw = "".join(s["text"] for s in l["spans"])
        offset = l["bbox"][0] - base + (len(raw) - len(raw.lstrip(" "))) * 0.29 * size
        n = max(0, round(offset / (0.29 * size)))
        if n:
            runs = [(" " * n, runs[0][1], False, INK)] + runs
        out.append(wing(runs))
    return out


def chip(g, x0, x1, r0, r1, content, fill, **kw):
    """Small tag / pill cell: narrow padding so a short word stays on one line."""
    kw.setdefault("line", 1000)
    g.put(x0, x1, r0, r1, content, fill, fit=False, **kw)
    key = (r0, g.xs.index(to_x(x0)))
    g.items[key] = g.items[key][:7] + (dict(left=40, right=40, top=20, bottom=20),)


def boxed(name, label_line, body_lines, top, height, label_fill=HEADC, label_color=INK):
    """추진배경 / 주요성과 box: label at left, outlined body with bullet lines."""
    g = Grid(name, [X0, 111.7, X1], [height])
    g.put(X0, 111.7, 0, 1, [runs_of(label_line, label_color)],
          frame(label_fill, top="mid", bottom="mid", left="mid"))
    g.put(111.7, X1, 0, 1, body_lines, frame(top="mid", bottom="mid", right="mid"), align="LEFT", line=1540)
    block(g, top)


def heading(name, line, top):
    g = Grid(name, [X0, X1], [1650])
    g.put(X0, X1, 0, 1, [line], align="LEFT", line=1450)
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

g = Grid("head", [X0, 375.0, X1], [1680])
g.put(X0, 375.0, 0, 1, [], frame(bottom="soft"))
g.put(375.0, X1, 0, 1, [line1(375, 385, 35, 40)], align="RIGHT")
block(g, 32.0)

# 평가내용 03 banner: dark chip (image, typed) over a hatched band with the two-line title.
g = Grid("banner", [X0, 124.0, X1], [1500, 2640])
g.put(X0, 124.0, 0, 1, [[("평가내용 ", 800, True, WHITE), ("03", 1350, True, WHITE)]],
      frame("#4B4B4B", top="mid", left="mid"), line=1300)
g.put(X0, 124.0, 1, 2, [], frame("#E9E9E9", bottom="mid", left="mid", hatch="#DADADA"))
g.put(124.0, X1, 0, 2, lines_in(125, 130, 75, 100), frame("#E9E9E9", top="mid", bottom="mid", right="mid",
                                                          hatch="#DADADA"), align="LEFT", line=1510)
block(g, 70.9)

boxed("background", line1(65, 70, 136, 140), lines_in(115, 120, 128, 150), 124.2, 3720)

# 추진방향: label + hatched band with two pills joined by (+); ▼ pointers under the pills.
xs = [X0, 114.1, 116.2, 151.6, 299.5, 330.0, 344.5, 372.7, 520.5, X1]
g = Grid("direction", xs, [2320, 800])
side = frame(SIDE, top="mid", left="mid", bottom="mid")
g.put(X0, 114.1, 0, 2, [line1(65, 70, 174, 178)], side, bold=True)
band = dict(top="soft", bottom="soft")
g.put(116.2, 151.6, 0, 1, [], frame("#E9E9E9", hatch="#D9D9D9", left="soft", **band))
g.put(151.6, 299.5, 0, 1, [line1(160, 175, 172, 178)], frame("#E3E3E3", top="soft", bottom="soft",
                                                              left="soft", right="soft"))
g.put(299.5, 330.0, 0, 1, [], frame("#E9E9E9", hatch="#D9D9D9", **band))
g.put(330.0, 344.5, 0, 1, "+", frame("#E9E9E9", hatch="#D9D9D9", **band), size=1300, bold=True,
      color="#7A7A7A", fit=False)
g.put(344.5, 372.7, 0, 1, [], frame("#E9E9E9", hatch="#D9D9D9", **band))
g.put(372.7, 520.5, 0, 1, [line1(370, 380, 172, 178)], frame("#E3E3E3", top="soft", bottom="soft",
                                                              left="soft", right="soft"))
g.put(520.5, X1, 0, 1, [], frame("#E9E9E9", hatch="#D9D9D9", right="soft", **band))
g.put(151.6, 299.5, 1, 2, "▼", size=600, color="#9A9A9A", line=600)
g.put(372.7, 520.5, 1, 2, "▼", size=600, color="#9A9A9A", line=600)
block(g, 167.7)

# 실행과제: four outlined boxes; the number boxes are images (typed ①-④).
xs = [X0, 114.1, 116.2, 224.2, 226.7, 334.7, 337.2, 445.2, 447.8, X1]
g = Grid("tasks", xs, [4420])
g.put(X0, 114.1, 0, 1, [line1(65, 70, 216, 220)], side, bold=True)
boxes = ((116.2, 224.2), (226.7, 334.7), (337.2, 445.2), (447.8, X1))
for k, (a, e) in enumerate(boxes):
    first, second = (line1(a, e, y - 1, y + 2) for y in (207.2, 223.5))
    mark = [("①②③④"[k] + " ", 1090, True, INK)]
    g.put(a, e, 0, 1, [mark + runs_of(first), runs_of(second)], frame(top="mid", bottom="mid", left="mid",
                                                                    right="mid"), line=1640)
block(g, 198.9)

# Section 1 band with the 지적사항 개선 sticker (image, typed).
g = Grid("sec1", [X0, 84.5, 367.0, 421.0, X1], [700, 1050, 550])
g.put(X0, 84.5, 0, 3, [runs_of(line1(60, 70, 262, 266), WHITE)], frame(DARK), line=1700)
g.put(84.5, 367.0, 0, 3, [line1(90, 95, 262, 266)], frame(BAND), align="LEFT", line=1700)
g.put(367.0, 421.0, 0, 1, [], frame(BAND))
chip(g, 367.0, 421.0, 1, 2, [[("지적사항 개선", 760, True, WHITE)]], frame("#3C3C3C"), line=880)
g.put(367.0, 421.0, 2, 3, [], frame(BAND))
g.put(421.0, X1, 0, 3, [], frame(BAND))
block(g, 259.4)

heading("title-ga", line1(55, 60, 289, 293), 288.0)
boxed("background-ga", line1(65, 70, 323, 327), lines_in(115, 120, 315, 336), 311.7, 3710)

# ---------------------------------------------------------------------------
# 「CHA-ON」 diagram (left) and 개방 지역 현황 map labels (right)
# ---------------------------------------------------------------------------
xs = [X0, 60.0, 62.0, 73.0, 91.0, 92.0, 105.5, 157.0, 169.0, 174.5, 202.5, 245.0, 247.5, 250.0, 261.0,
      280.5, 294.5, 315.0, 328.5, 331.0, 364.0, 433.5, 436.9,
      439.3, 459.0, 482.0, 500.0, 524.5, X1]
#      0 head 1 B0  2 B1  3 B2  4 tabs 5 E1  6 E2  7 F1  8 F2  9 gap 10 res 11 pad
hs = [1990, 250, 1500, 250, 1700, 1600, 1750, 1850, 2000, 400, 3800, 450]
g = Grid("cha-on", xs, hs)
n = len(hs)
g.put(X0, 436.9, 0, 1, [line1(110, 120, 358, 362)], frame(HEADC, top="mid", left="mid", right="mid", bottom="soft"))
# stage band: '24 (light) ▶ '25 (dark) ▶ '26~ (light); year pills are white
light, darkf = frame("#D2D2D2"), frame("#828282")
stage = line1(65, 70, 378, 381), line1(175, 185, 378, 381), line1(330, 340, 378, 381)
for r in (1, 3):
    g.put(X0, 169.0, r, r + 1, [], frame("#D2D2D2", left="mid"))
    g.put(169.0, 315.0, r, r + 1, [], darkf)
    g.put(315.0, 436.9, r, r + 1, [], frame("#D2D2D2", right="mid"))
g.put(X0, 62.0, 2, 3, [], frame("#D2D2D2", left="mid"))
chip(g, 62.0, 91.0, 2, 3, [runs_of(stage[0], x1=90.0)], BOX)
g.put(91.0, 157.0, 2, 3, [strip_runs(runs_of(stage[0], x0=90.0))], light, align="LEFT")
g.put(157.0, 169.0, 2, 3, "▶", light, size=900, color="#6A6A6A")
g.put(169.0, 174.5, 2, 3, [], darkf)
chip(g, 174.5, 202.5, 2, 3, [runs_of(stage[1], x1=200.0)], BOX)
g.put(202.5, 315.0, 2, 3, [strip_runs(runs_of(stage[1], WHITE, x0=200.0))], darkf, align="LEFT")
g.put(315.0, 328.5, 2, 3, "▶", light, size=900, color="#6A6A6A")
g.put(328.5, 331.0, 2, 3, [], light)
chip(g, 331.0, 364.0, 2, 3, [runs_of(stage[2], x1=362.0)], BOX)
g.put(364.0, 436.9, 2, 3, [strip_runs(runs_of(stage[2], x0=362.0))], frame("#D2D2D2", right="mid"), align="LEFT")
# 사업소 / 지역사회 tabs
tab_l, tab_r = line1(70, 75, 400, 402), line1(255, 260, 400, 402)
text_l, text_r = line1(105, 110, 398, 401), line1(295, 300, 397, 401)
g.put(X0, 60.0, 4, 5, [], frame(left="mid"))
chip(g, 60.0, 105.5, 4, 5, [runs_of(tab_l)], frame("#F2F2F2", top="soft", bottom="soft", left="soft", right="soft"))
g.put(105.5, 245.0, 4, 5, [strip_runs(runs_of(text_l))], frame(bottom="soft"), align="LEFT")
g.put(245.0, 250.0, 4, 5, [], frame(right="dot"))
chip(g, 250.0, 294.5, 4, 5, [runs_of(tab_r)], frame("#F2F2F2", top="soft", bottom="soft", left="soft", right="soft"))
g.put(294.5, 433.5, 4, 5, [wing(strip_runs(runs_of(text_r)))], frame(bottom="soft"), align="LEFT")
g.put(433.5, 436.9, 4, 5, [], frame(right="mid"))
# bullets: tagged lines split into bullet | boxed tag | text; continuation lines whole
for half, (a, b, c, e, base) in enumerate(((X0, 73.0, 92.0, 247.5, 65.3), (247.5, 261.0, 280.5, 436.9, 253.4))):
    outer = dict(left="mid") if half == 0 else dict(right="mid")
    rest = dict(right="dot") if half == 0 else dict(right="mid")
    for r, y in ((5, 424.0), (7, 455.5)):
        l = [x for x in lines_in(a, e, y - 3, y + 4) if x["bbox"][0] < base + 1][0]
        g.put(a, b, r, r + 1, [runs_of(l, x1=b)], frame(**outer), align="RIGHT")
        chip(g, b, c, r, r + 1, [runs_of(l, x0=b, x1=c - 1.0)], BOX)
        g.put(c, e, r, r + 1, [strip_runs(runs_of(l, x0=c - 1.0))], frame(**rest), align="LEFT")
    for r, y in ((6, 438.5), (8, 473.0)):
        l = [x for x in lines_in(a, e, y - 3, y + 4) if x["bbox"][0] < base + 1][0]
        g.put(a, e, r, r + 1, hang([l], base), frame(**{**outer, **rest}), align="LEFT")
# results (hatched boxes)
g.put(X0, 436.9, 9, 10, [], frame(left="mid", right="mid"))
g.put(X0, 60.0, 10, 11, [], frame(left="mid"))
res = frame("#DCDCDC", hatch="#C8C8C8")
g.put(60.0, 245.0, 10, 11, lines_in(70, 100, 495, 515), res, bold=True, line=1300)
g.put(245.0, 250.0, 10, 11, [])
g.put(250.0, 433.5, 10, 11, lines_in(250, 270, 495, 515), res, bold=True, line=1300)
g.put(433.5, 436.9, 10, 11, [], frame(right="mid"))
g.put(X0, 436.9, 11, 12, [], frame(left="mid", right="mid", bottom="mid"))
# 개방 지역 현황 (map labels typed; the map outline and pins are not reproduced)
g.put(439.3, X1, 0, 1, [line1(450, 455, 358, 362)], frame(HEADC, top="mid", left="mid", right="mid", bottom="soft"))
mapf = frame("#F4F4F4")
pin_dark, pin_light = frame("#555555"), BOX
labels = {(2, 500.0): ("’24년", pin_light, INK), (2, 524.5): ("1개소", None, INK),
          (4, 459.0): ("서 울", pin_dark, WHITE), (4, 500.0): ("’25년", pin_dark, WHITE), (4, 524.5): ("3개소", None, INK),
          (5, 500.0): ("충북", pin_dark, WHITE), (7, 482.0): ("전북", pin_dark, WHITE),
          (8, 482.0): ("나주", pin_light, INK)}
edges = [439.3, 459.0, 482.0, 500.0, 524.5, X1]
for r in range(1, n):
    for a, e in zip(edges, edges[1:]):
        fr = dict(left="mid" if a == 439.3 else None, right="mid" if e == X1 else None,
                  bottom="mid" if r == n - 1 else None)
        if (r, a) in labels:
            text, fill, color = labels[r, a]
            if fill is None:
                chip(g, a, e, r, r + 1, [[(text, 900, False, color)]], frame("#E2E2E2", **fr))
            else:
                chip(g, a, e, r, r + 1, [[(text, 900, False, color)]], fill)
        else:
            g.put(a, e, r, r + 1, [], frame(**fr))
block(g, 355.1)

g = Grid("footnote", [X0, X1], [1500])
g.put(X0, X1, 0, 1, [line1(55, 60, 537, 541)], align="LEFT", line=1150)
block(g, 536.5)

# ---------------------------------------------------------------------------
# 나. 「K-동행 공간」: four-step flow, then the space diagram and the photo.
# ---------------------------------------------------------------------------
heading("title-na", line1(55, 60, 558, 562), 557.0)

xs = [X0, 170.0, 181.0, 321.0, 332.0, 439.0, 450.0, X1]
g = Grid("steps", xs, [1870, 2950])
heads = [line1(80, 90, 583, 587), line1(220, 225, 583, 587), line1(355, 360, 583, 587), line1(460, 465, 583, 587)]
fills = ["#DCDCDC", "#DCDCDC", "#B8B8B8", "#ADADAD"]
cols = ((X0, 170.0), (181.0, 321.0), (332.0, 439.0), (450.0, X1))
for k, ((a, e), line, fill) in enumerate(zip(cols, heads, fills)):
    g.put(a, e, 0, 1, [line], frame(fill))
    if k < 3:
        g.put(e, cols[k + 1][0], 0, 1, "▶", frame(fills[k + 1] if k else fill), size=900, color="#6A6A6A",
              fit=False)
values = [line1(80, 85, 607, 611), line1(185, 190, 607, 611), line1(335, 340, 607, 611), line1(440, 445, 607, 611)]
vcols = ((X0, 170.0), (170.0, 321.0), (321.0, 439.0), (439.0, X1))
for k, ((a, e), line) in enumerate(zip(vcols, values)):
    g.put(a, e, 1, 2, [line], frame(bottom="soft", right="soft" if k < 3 else None))
block(g, 580.6)

xs = [X0, 60.0, 228.0, 265.0, 433.5, 436.9, 439.3, X1]
#      head  pad  t1    b1    gap  t2    b2    pad
hs = [1880, 300, 1950, 2500, 500, 1900, 2450, 740]
g = Grid("space", xs, hs)
g.put(X0, 436.9, 0, 1, [line1(210, 220, 640, 644)], frame(HEADC, top="mid", left="mid", right="mid", bottom="soft"))
g.put(X0, 436.9, 1, 2, [], frame(left="mid", right="mid"))
g.put(X0, 436.9, 4, 5, [], frame(left="mid", right="mid"))
g.put(X0, 436.9, 7, 8, [], frame(left="mid", right="mid", bottom="mid"))
title = frame("#D8D8D8")
for r, y, hexa in ((2, 662.5, (670, 690)), (5, 712.5, (720, 740))):
    g.put(X0, 60.0, r, r + 2, [], frame(left="mid"))
    g.put(433.5, 436.9, r, r + 2, [], frame(right="mid"))
    left_t = line1(60, 230, y - 1, y + 2)
    right_t = line1(265, 330, y - 1, y + 2)
    g.put(60.0, 228.0, r, r + 1, [left_t], title)
    g.put(265.0, 433.5, r, r + 1, [strip_runs(runs_of(right_t))], title)
    left_b, right_b = line1(60, 70, y + 18, y + 26), line1(260, 275, y + 18, y + 26)
    g.put(60.0, 228.0, r + 1, r + 2, hang([left_b], 65.4), frame(bottom="dot"), align="LEFT")
    g.put(265.0, 433.5, r + 1, r + 2, hang([right_b], right_b["bbox"][0]), frame(bottom="dot"), align="LEFT")
    g.put(228.0, 265.0, r, r + 2, lines_in(225, 240, *hexa), frame("#909090"), color=WHITE, bold=True, line=1100)
g.put(439.3, X1, 0, 1, [line1(460, 470, 640, 644)], frame(HEADC, top="mid", left="mid", right="mid", bottom="soft"))
g.put(439.3, X1, 1, 8, [], frame("#E4E4E4", left="mid", right="mid", bottom="mid"))
block(g, 636.2)

g = Grid("result", [X0, 111.7, X1], [3710])
g.put(X0, 111.7, 0, 1, [runs_of(line1(65, 70, 776, 780), WHITE)], frame("#7F7F7F", top="mid", bottom="mid",
                                                                       left="mid"))
g.put(111.7, X1, 0, 1, lines_in(115, 120, 767, 790), frame(top="mid", bottom="mid", right="mid"), align="LEFT",
      line=1600)
block(g, 764.7)

# ---------------------------------------------------------------------------
# finish: Wingdings face for the U+F09E dots, then the kit's own finish
# ---------------------------------------------------------------------------
wing_ids = {}
for family in L.header.iter(L.q("hh:fontface")):
    font = deepcopy(family[0])
    ident = str(max(int(f.get("id")) for f in family) + 1)
    font.set("id", ident)
    font.set("face", "Wingdings")
    family.append(font)
    family.set("fontCnt", str(len(family)))
    wing_ids[family.get("lang").lower()] = ident
for char in L.characters:
    if char.get("textColor") == WING:
        char.set("textColor", INK)
        ref = L.get(char, "hh:fontRef")
        for lang in ref.attrib:
            ref.set(lang, wing_ids[lang])
kit.finish(target, end=803.0)
