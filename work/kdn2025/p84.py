"""Rebuild KDN 2025 report page 84 (2nd PDF local page 34, printed page 56) as editable HWPX.

Usage: python3 work/kdn2025/p84.py <report2.pdf> <out.hwpx> [--page 34]

창업 및 경제활성화, 평가내용 04 opening page (특허 개방 / 기술이전). Built with the shared kit (one
flat table per band on a grid of PDF x edges); all body text comes from the PDF text layer.
Images and how they are kept:
- PART box, 평가내용 04 chip (check-mark icon dropped), section-1 number band: typed cells.
- boxed numbers 1 2 3 of 추진방향 -> ① ② ③; the ➡ arrows (Step2, 온라인 공개) -> →;
  the grey chevrons between boxes -> ▶ / ▼.
- 'NEW 신규' and '지적사항 개선' stickers (images): typed as small dark tag cells. The text-layer
  tags (Step pills, 개선, boxed 신규, 유상/무상, 중소기업/KDN pills) are separate cells.
- Footer logo typed as 한전KDN㈜.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kit  # noqa: E402
from kit import Layout, recipe_inputs  # noqa: E402

source, target = recipe_inputs(34, "기관 보유 미활용 특허")
L = Layout(top=3100)
kit.setup(source, L)
from kit import *  # noqa: E402,F401,F403  helpers and presets bound to this page

DARK, LABEL = "#6A6A6A", "#E3E3E3"
HEAD = "#DADADA"
BOX = "#F4F4F4"


def hang(lines, base, prefix=None):
    """Bullet lines keep their PDF indent: spaces for the x offset and for the line's own lead."""
    out = []
    for l in lines:
        runs = runs_of(l)
        size = runs[0][1] / 100
        raw = "".join(s["text"] for s in l["spans"])
        offset = l["bbox"][0] - base + (len(raw) - len(raw.lstrip(" "))) * 0.29 * size
        n = max(0, round(offset / (0.29 * size)))
        lead = (prefix or {}).get(l["text"], "")
        if n or lead:
            runs = [(" " * n + lead, runs[0][1], False, INK)] + runs
        out.append(runs)
    return out


def boxed(name, label_line, body, top, height):
    """주요성과 box: dark label at left, outlined body."""
    g = Grid(name, [X0, 111.7, X1], [height])
    g.put(X0, 111.7, 0, 1, [runs_of(label_line, WHITE)], frame(DARK, top="mid", bottom="mid", left="mid"))
    g.put(111.7, X1, 0, 1, body, frame(top="mid", bottom="mid", right="mid"), align="LEFT")
    block(g, top)


def title(name, line, top, tag=None, tag_x=None):
    """'가. title' heading (14pt), optionally followed by a dark sticker cell."""
    g = Grid(name, [X0, tag_x, X1] if tag else [X0, X1], [1650])
    g.put(X0, tag_x if tag else X1, 0, 1, [line], align="LEFT", line=1450)
    if tag:
        g.put(tag_x, X1, 0, 1, tag, frame("#3C3C3C"), size=760, bold=True, color=WHITE, line=1000)
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

# 평가내용 04 banner (image chip + text title).
g = Grid("banner", [X0, 124.0, X1], [2860])
g.put(X0, 124.0, 0, 1, [[("평가내용 ", 800, True, WHITE), ("04", 1350, True, WHITE)]], frame("#686868"),
      line=1500)
g.put(124.0, X1, 0, 1, [line1(125, 130, 76, 82)], striped, align="LEFT", line=1450)
block(g, 70.9)

# Section 1 band (image): dark number cell, light title cell.
g = Grid("sec1", [X0, 84.5, X1], [2300])
g.put(X0, 84.5, 0, 1, [runs_of(line1(60, 70, 112, 116), WHITE)], frame(DARK), line=1700)
g.put(84.5, X1, 0, 1, [line1(90, 95, 112, 117)], frame("#E6E6E6"), align="LEFT", line=1700)
block(g, 110.9)

# ---------------------------------------------------------------------------
# 추진배경 (three tabbed boxes) and 추진방향 (numbered gray cells), chevrons between.
# ---------------------------------------------------------------------------
cols = ((107.6, 255.4, 113.5), (257.9, 405.6, 263.8), (408.1, X1, 414.1))
xs = [X0, 102.7, 107.6, 255.4, 257.9, 405.6, 408.1, X1]
g = Grid("background", xs, [1700, 3700, 650, 2050])
g.put(X0, 102.7, 0, 2, [line1(60, 65, 160, 166)], frame(LABEL), bold=True)
g.put(X0, 102.7, 3, 4, [line1(60, 65, 203, 208)], frame(LABEL), bold=True)
for k, (a, e, base) in enumerate(cols):
    g.put(a, e, 0, 1, [line1(a, e, 142, 148)], frame(HEAD, top="mid", left="mid", right="mid"))
    g.put(a, e, 1, 2, hang(lines_in(a, e, 160, 190), base), frame(left="mid", right="mid", bottom="mid"),
          align="LEFT", line=1450)
    g.put(a, e, 2, 3, "▼", size=550, color=ARROW, line=480)
    g.put(a, e, 3, 4, [[("①②③"[k] + " ", 1090, False, INK)] + runs_of(line1(a, e, 203, 208))], frame("#E6E6E6"))
block(g, 140.1)

title("title-ga", line1(55, 60, 232, 237), 233.0)

# ---------------------------------------------------------------------------
# 가. Step1-3 boxes (header: white Step pill + bold title), chevrons, then Step4 box.
# ---------------------------------------------------------------------------
xs = [X0, 68.2, 99.8, 176.0, 189.8, 201.2, 232.9, 299.7, 318.5, 330.0, 343.9, 396.9, 428.6, X1]
g = Grid("steps", xs, [250, 1200, 290, 6110])
pill_cell = frame(WHITE, top="soft", bottom="soft", left="soft", right="soft")
head_l = frame(HEAD, top="mid", left="mid")
head_m = frame(HEAD, top="mid")
head_r = frame(HEAD, top="mid", right="mid")
head = frame(HEAD)
steps = ((X0, 68.2, 99.8, 176.0, 62.5), (189.8, 201.2, 232.9, 330.0, 195.7), (343.9, 396.9, 428.6, X1, 346.7))
for k, (a, p0, p1, e, base) in enumerate(steps):
    line = line1(p0, p1, 258, 262)
    g.put(a, p0, 0, 3, [], head_l)
    g.put(p0, p1, 0, 1, [], head_m)
    g.put(p0, p1, 1, 2, [runs_of(line, x1=p1 - 3)], pill_cell)
    g.put(p0, p1, 2, 3, [], head)
    # Title cells start in the pill's sub-row so the text keeps its reading order.
    if k == 1:   # Step2: dark '개선' tag after the title
        g.put(p1, 299.7, 0, 1, [], head_m)
        g.put(p1, 299.7, 1, 3, [strip_runs(runs_of(line, x0=p1 - 3, x1=299.0))], head, align="LEFT")
        g.put(299.7, 318.5, 0, 1, [], head_m)
        g.put(299.7, 318.5, 1, 2, [runs_of(line, WHITE, x0=299.0)], frame("#7F7F7F"))
        g.put(299.7, 318.5, 2, 3, [], head)
        g.put(318.5, e, 0, 3, [], head_r)
    else:
        g.put(p1, e, 0, 1, [], head_r)
        g.put(p1, e, 1, 3, [strip_runs(runs_of(line, x0=p1 - 3))], frame(HEAD, right="mid"), align="LEFT")
    arrows = {l["text"] for l in lines_in(210, 220, 290, 296)}
    g.put(a, e, 3, 4, hang(lines_in(a, e, 275, 330), base, {t: "→ " for t in arrows}),
          frame(left="mid", right="mid", bottom="mid"), align="LEFT", line=1330)
g.put(176.0, 189.8, 3, 4, "▶", size=1100, color=ARROW)
g.put(330.0, 343.9, 3, 4, "▶", size=1100, color=ARROW)
block(g, 254.9)

g = Grid("steps-arrow", [X0, X1], [1000])
g.put(X0, X1, 0, 1, "▼", size=1000, color=ARROW, line=800)
block(g, 335.0)

xs = [X0, 92.2, 194.2, 222.8, 225.8, 256.0, 307.0, 341.6, X1]
g = Grid("step4", xs, [250, 1200, 400, 400, 1300, 800, 3800])
g.put(X0, 194.2, 0, 3, [], head_l)
g.put(194.2, 225.8, 0, 1, [], head_m)
step4 = line1(195, 200, 352, 356)
g.put(194.2, 225.8, 1, 2, [runs_of(step4, x1=223.0)], pill_cell)
g.put(194.2, 225.8, 2, 3, [], head)
g.put(225.8, X1, 0, 1, [], head_r)
g.put(225.8, X1, 1, 3, [strip_runs(runs_of(step4, x0=223.0))], frame(HEAD, right="mid"), align="LEFT")
side_l, side_r = frame(left="mid"), frame(right="mid")
paid, free = line1(65, 70, 374, 380), line1(315, 320, 374, 380)
g.put(X0, 92.2, 3, 4, [], side_l)
g.put(X0, 92.2, 4, 5, [paid], frame("#CFCFCF", left="mid"), line=1100)
g.put(X0, 92.2, 5, 6, [], side_l)
g.put(92.2, 222.8, 3, 6, [line1(95, 100, 374, 380)], align="LEFT")
g.put(222.8, 256.0, 3, 4, [])
g.put(222.8, 256.0, 4, 5, [[("NEW ", 520, True, WHITE), ("신규", 820, True, WHITE)]], frame("#3C3C3C"), line=1000)
g.put(222.8, 256.0, 5, 6, [])
g.put(256.0, 307.0, 3, 6, [])
g.put(307.0, 341.6, 3, 4, [], frame(left="dot"))
g.put(307.0, 341.6, 4, 5, [free], frame("#CFCFCF", left="dot"), line=1100)
g.put(307.0, 341.6, 5, 6, [], frame(left="dot"))
g.put(341.6, X1, 3, 6, [line1(345, 350, 374, 380)], frame(right="mid"), align="LEFT")
hatched = frame("#EEEEEE", hatch="#E2E2E2")
g.put(X0, 307.0, 6, 7, hang(lines_in(60, 65, 395, 415), 62.5), frame("#EEEEEE", left="mid", bottom="mid",
                                                                   hatch="#E2E2E2"), align="LEFT", line=1500)
g.put(307.0, X1, 6, 7, hang(lines_in(310, 315, 395, 415), 311.9), frame("#EEEEEE", left="dot", right="mid",
                                                                         bottom="mid", hatch="#E2E2E2"),
      align="LEFT", line=1500)
block(g, 349.0)

boxed("result-ga", line1(65, 70, 441, 446), [line1(115, 120, 439, 444)], 437.2, 2300)

# ---------------------------------------------------------------------------
# 나. 온･오프라인 공개 table (구분 | 추진 노력); offline row: three sub-columns.
# ---------------------------------------------------------------------------
title("title-na", line1(55, 60, 470, 474), 470.5, "지적사항 개선", 503.0)

xs = [X0, 124.0, 138.5, 160.0, 290.0, 403.5, 434.5, 457.0, X1]
g = Grid("media", xs, [1900, 3900, 2300, 1550, 2350])
g.put(X0, 124.0, 0, 1, [line1(75, 80, 495, 500)], frame(HEAD, top="mid", left="mid"))
g.put(124.0, X1, 0, 1, [line1(315, 320, 495, 500)], frame(HEAD, top="mid", right="mid"))
g.put(X0, 124.0, 1, 2, lines_in(60, 80, 515, 540), frame(left="mid", bottom="dot"))
online = lines_in(125, 135, 528, 535)
assert len(online) == 1
g.put(124.0, X1, 1, 2, [runs_of(line1(125, 135, 515, 522)),
                        [("  ", 1090, False, INK)] + runs_of(online[0]) + [(" → ", 1090, False, INK)]
                        + runs_of(line1(290, 295, 528, 535))],
      frame(right="mid", bottom="dot"), align="LEFT", line=1300)
g.put(X0, 124.0, 2, 5, lines_in(60, 80, 565, 590), frame(left="mid", bottom="mid"))
sub = frame("#E9E9E9")
g.put(124.0, 290.0, 2, 3, [line1(175, 180, 556, 562)], sub)
g.put(290.0, 403.5, 2, 3, [line1(305, 310, 556, 562)], frame("#E9E9E9", left="dot"))
new_head = line1(436, 440, 556, 562)
g.put(403.5, 434.5, 2, 3, [], frame("#E9E9E9", left="dot"))
g.put(434.5, 457.0, 2, 3, [runs_of(new_head, x1=454.0)], frame(WHITE, top="soft", bottom="soft", left="soft",
                                                                 right="soft"), line=1000)
g.put(457.0, X1, 2, 3, [strip_runs(runs_of(new_head, x0=454.0))], frame("#E9E9E9", right="mid"), align="LEFT")
g.put(124.0, 290.0, 3, 4, [line1(130, 135, 575, 580)], align="LEFT")
fair = line1(130, 135, 591, 596)
g.put(124.0, 138.5, 4, 5, [runs_of(fair, x1=140.0)], frame(bottom="mid"), align="RIGHT")
g.put(138.5, 160.0, 4, 5, [runs_of(fair, x0=140.0, x1=158.0)], frame(WHITE, top="soft", bottom="mid",
                                                                    left="soft", right="soft"), line=1000)
g.put(160.0, 290.0, 4, 5, [strip_runs(runs_of(fair, x0=158.0))], frame(bottom="mid"), align="LEFT")
for a, e, base in ((290.0, 403.5, 295.3), (403.5, X1, 408.7)):
    edge = dict(right="mid") if e == X1 else {}
    first, second = lines_in(a + 3, a + 10, 575, 580), lines_in(a + 3, a + 10, 591, 596)
    g.put(a, e, 3, 4, hang(first, base), frame(left="dot", **edge), align="LEFT")
    g.put(a, e, 4, 5, hang(second, base), frame(left="dot", bottom="mid", **edge), align="LEFT")
block(g, 492.5)

boxed("result-na", line1(65, 70, 624, 629), [line1(115, 120, 622, 627)], 620.4, 2300)

# ---------------------------------------------------------------------------
# 다. 추진 노력 table: Fast-Track (left) | 기술 중계 (right, three linked boxes).
# ---------------------------------------------------------------------------
title("title-da", line1(55, 60, 652, 657), 653.5)

xs = [X0, 270.0, 273.7, 390.2, 404.0, 448.9, 462.8, 547.4, X1]
g = Grid("transfer", xs, [1940, 2100, 1750, 1650, 1750, 680])
g.put(X0, X1, 0, 1, [line1(285, 290, 678, 684)], frame(HEAD, top="mid", left="mid", right="mid"))
g.put(X0, 270.0, 1, 2, [line1(95, 100, 698, 704)], frame("#E9E9E9", left="mid"))
g.put(270.0, X1, 1, 2, [line1(350, 355, 698, 704)], frame("#E9E9E9", left="dot", right="mid"))
g.put(X0, 270.0, 2, 6, hang(lines_in(64, 70, 718, 760), 66.0), frame(left="mid", bottom="mid"), align="LEFT",
      line=1500)
g.put(270.0, X1, 2, 3, [line1(272, 278, 714, 722)], frame(left="dot", right="mid"), align="LEFT")
g.put(270.0, 273.7, 3, 6, [], frame(left="dot", bottom="mid"))
box_head = frame(HEAD, top="soft", left="soft", right="soft")
box_body = frame(WHITE, bottom="soft", left="soft", right="soft")
for a, e, hx, bx in ((273.7, 390.2, 289.0, 278.2), (404.0, 448.9, 408.2, 408.2), (462.8, 547.4, 482.6, 466.6)):
    g.put(a, e, 3, 4, [line1(hx - 1, hx + 1, 736, 742)], box_head)
    g.put(a, e, 4, 5, [line1(bx - 1, bx + 1, 750, 757)], box_body)
    g.put(a, e, 5, 6, [], frame(bottom="mid"))
g.put(390.2, 404.0, 3, 5, [line1(390, 395, 744, 748)])
g.put(390.2, 404.0, 5, 6, [], frame(bottom="mid"))
g.put(448.9, 462.8, 3, 5, [line1(450, 455, 744, 748)])
g.put(448.9, 462.8, 5, 6, [], frame(bottom="mid"))
g.put(547.4, X1, 3, 6, [], frame(right="mid", bottom="mid"))
block(g, 675.6)

# 주요성과 with two inline pills (중소기업 outlined, KDN dark).
res = line1(120, 125, 780, 785)
xs = [X0, 111.7, 117.6, 157.7, 409.0, 437.8, X1]
g = Grid("result-da", xs, [520, 1200, 570])
g.put(X0, 111.7, 0, 3, [runs_of(line1(65, 70, 782, 787), WHITE)], frame(DARK, top="mid", bottom="mid", left="mid"))
g.put(111.7, 117.6, 0, 3, [], frame(top="mid", bottom="mid"))
for a, e, fill, color in ((117.6, 157.7, frame("#EFEFEF", top="soft", bottom="soft", left="soft", right="soft"), INK),
                          (409.0, 437.8, frame("#7A7A7A"), WHITE)):
    g.put(a, e, 0, 1, [], frame(top="mid"))
    g.put(a, e, 1, 2, [runs_of(res, color, x0=a - 5, x1=a + 15)], fill, line=1030)
    g.put(a, e, 2, 3, [], frame(bottom="mid"))
for a, e, x0, x1, side in ((157.7, 409.0, 157.0, 409.0, {}), (437.8, X1, 437.0, 1e9, dict(right="mid"))):
    g.put(a, e, 0, 1, [], frame(top="mid", **side))   # text starts in the pills' row (reading order)
    g.put(a, e, 1, 3, [strip_runs(runs_of(res, x0=x0, x1=x1))], frame(bottom="mid", **side), align="LEFT")
block(g, 778.3)

kit.finish(target, end=801.2)
