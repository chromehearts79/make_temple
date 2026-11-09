"""Rebuild KDN 2025 report page 141 (3rd PDF local page 41, printed page 98) as editable HWPX.

Usage: python3 work/kdn2025/p141.py <report3.pdf> <out.hwpx> [--page 41]

조직 운영 및 관리(노사관계), section 2 "노사 협력체계의 안정적 정착을 통한 경영 참여 및 ESG 실천
내실화": 가. 노동조합 통합 (통합 과정 / 노력 활동 / 추진성과), 나. 노동이사 (three columns),
다. 노사 공동 ESG (추진배경, E/S/G rows), 주요성과. Built with the shared kit (one flat table per
band on a grid of PDF x edges); all text comes from the PDF text layer.

Images and how they are kept:
- side tab, section-2 number band, 'Best Practice' sticker (trophy dropped), '지적사항 개선' tag
  (hand icon dropped): typed cells.
- the ➡ arrow images inside lines -> "→"; the gray chevrons between boxes -> "▶"; the down
  chevrons between the 노동이사 stages -> "▼"; Step / 노력 chevron shapes -> gray cells in the
  printed light-to-dark order; rounded boxes -> plain borders.
- the tags 효율 / 안정 / 화합 and the year pills (’22년~’24년 ...) are text-layer runs on their
  own outlined cells.
- the three photos -> `photo` placeholder cells next to their (text-layer) captions.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kit  # noqa: E402
from kit import Layout, recipe_inputs  # noqa: E402

source, target = recipe_inputs(41, "노사 협력체계의 안정적 정착을 통한 경영 참여 및 ESG 실천 내실화")
L = Layout(top=3100)
kit.setup(source, L)
from kit import *  # noqa: E402,F401,F403  helpers and presets bound to this page

DARK = "#6A6A6A"
HEAD = "#D8D8D8"
OUTLINE = frame(WHITE, top="soft", bottom="soft", left="soft", right="soft")
HATCH = dict(hatch="#D6D6D6")
ARROW_RUN = ("→ ", 1000, True, "#505050")
STEP_FILLS = ("#E8E8E8", "#C8C8C8", "#B0B0B0")


def tight(g, x0, r0, left=0, right=0):
    """Narrow the padding of a placed cell (tags narrower than the default 320/180 padding)."""
    c0 = g.xs.index(to_x(x0))
    g.items[r0, c0] = (*g.items[r0, c0][:7], dict(left=left, right=right))


def hang(line):
    """'  - ...' continuation line: keep the source indent (runs_of strips leading blanks)."""
    runs = runs_of(line)
    return [("  ", runs[0][1], False, INK)] + runs


# ---------------------------------------------------------------------------
# Page chrome (odd page): running head over a rule, side tab, footer at the right.
# ---------------------------------------------------------------------------
L.add_table([[cell(0, 3350, 1680, [para([("01", 1380, True, WHITE)], "CENTER")[0]], dark)],
             [cell(0, 3350, 5960, [para([(ch, 950, True, INK)], "CENTER", 1160)[0] for ch in "경영관리"], gray2)]],
            floating=(57800, 15000))
foot = [(text, size, False, INK) for text, size in (
    (line1(450, 455, 818, 822)["text"], 790), ("    ", 790), (line1(540, 546, 816, 820)["text"], 1090))]
L.add_table([[cell(0, W, 1500, [para(foot, "RIGHT", 1300)[0]])]], floating=(5660, 81550))

g = Grid("head", [X0, 432.0, X1], [1680])
g.put(X0, 432.0, 0, 1, [], frame(bottom="soft"))
g.put(432.0, X1, 0, 1, [line1(430, 440, 35, 40)], align="RIGHT")
block(g, 32.0)

# Section 2 band (image): dark number, light title.
g = Grid("sec2", [X0, 84.5, X1], [2300])
g.put(X0, 84.5, 0, 1, [runs_of(line1(60, 70, 72, 77), WHITE)], frame(DARK), line=1700)
g.put(84.5, X1, 0, 1, [line1(90, 95, 73, 78)], frame("#E6E6E6"), align="LEFT", line=1700)
block(g, 70.9)

# ---------------------------------------------------------------------------
# 가. 노동조합 통합
# ---------------------------------------------------------------------------
g = Grid("title-ga", [X0, 485.8, X1], [1650])
g.put(X0, 485.8, 0, 1, [line1(55, 60, 101, 104)], align="LEFT", line=1450)
g.put(485.8, X1, 0, 1, "Best Practice", frame("#4A4A4A"), size=900, bold=True, color=WHITE)
block(g, 101.2)

g = Grid("dual-union", [X0, 105.4, 108.2, 337.3, 355.7, X1], [3740])
g.put(X0, 105.4, 0, 1, lines_in(60, 70, 128, 156), frame(top="dot"), line=1320)
g.put(108.2, 337.3, 0, 1, lines_in(115, 125, 126, 156), frame(top="mid", bottom="mid", left="mid"), line=1430)
g.put(337.3, 355.7, 0, 1, "▶", frame(top="mid", bottom="mid"), size=1000, color=ARROW)
g.put(355.7, X1, 0, 1, lines_in(370, 375, 127, 156), frame("#EEEEEE", top="mid", bottom="mid", right="mid", **HATCH),
      line=1430)
block(g, 123.2)

# 통합 노력: vertical label, 통합 과정 (Step 1-3) | 노력 활동 (노력 1-3)
xs = [X0, 79.6, 82.2, 123.5, 317.8, 320.3, 361.6, X1]
g = Grid("effort", xs, [1900, 3300, 3250, 3300])
g.put(X0, 79.6, 0, 4, lines_in(60, 70, 198, 255), frame("#F0F0F0"), line=1320)
for (a, b, e), hx in (((82.2, 123.5, 317.8), 175), ((320.3, 361.6, X1), 415)):
    g.put(a, e, 0, 1, [line1(hx, hx + 10, 168, 172)], frame(HEAD, top="mid", left="mid", right="mid"))
    for r, (ys, yt, fill) in enumerate(zip((196.4, 232.8, 264.8), (188.3, 220.9, 253.4), STEP_FILLS), 1):
        last = r == 3
        g.put(a, b, r, r + 1, [line1(a + 4, a + 10, ys - 1, ys + 1)], frame(fill, left="mid",
                                                                           bottom="mid" if last else None))
        title, sub = lines_in(b, e, yt - 1, yt + 16)
        g.put(b, e, r, r + 1, [runs_of(title), [ARROW_RUN] + runs_of(sub)],
              frame(right="mid", bottom="mid" if last else "dot"), align="LEFT", line=1430)
block(g, 165.5)

# 추진성과: label, three tagged lines (tag | text → text), result line, caption + photo
xs = [X0, 116.0, 119.0, 135.0, 430.0, 466.0, X1]
g = Grid("result-ga", xs, [350, 1460, 1460, 1460, 1460, 485])
g.put(X0, 116.0, 0, 6, [line1(65, 70, 316, 320)], frame(HEAD, top="mid", bottom="mid", left="mid"))
box = dict(top="mid")
g.put(116.0, 430.0, 0, 1, [], frame(**box))
for r, y in enumerate((294.6, 309.2, 323.9), 1):
    a, b = lines_in(115, 430, y - 1, y + 1)
    g.put(119.0, 135.0, r, r + 1, [runs_of(a, x1=135)], OUTLINE, line=1000, fit=False)
    tight(g, 119.0, r)
    g.put(135.0, 430.0, r, r + 1, [strip_runs(runs_of(a, x0=135) + [(" → ", 1090, False, "#505050")] + runs_of(b))],
          align="LEFT", line=1250)
g.put(119.0, 430.0, 4, 5, [[ARROW_RUN] + runs_of(line1(130, 135, 337, 340))], align="LEFT", line=1250)
g.put(116.0, 430.0, 5, 6, [], frame(bottom="mid"))
g.put(430.0, 466.0, 0, 6, lines_in(434, 445, 300, 345), frame("#E8E8E8", top="mid", bottom="mid"), line=1000)
g.put(466.0, X1, 0, 6, [], photo)
block(g, 288.5)

# ---------------------------------------------------------------------------
# 나. 노동이사: stages (left) ▶ 전문성 지원 (middle) ▶ 경영제언 성과 (right)
# ---------------------------------------------------------------------------
g = Grid("title-na", [X0, 481.5, 536.0, X1], [1650])
g.put(X0, 481.5, 0, 1, [line1(55, 60, 364, 367)], align="LEFT", line=1450)
g.put(481.5, 536.0, 0, 1, "지적사항 개선", frame("#4A4A4A"), size=800, bold=True, color=WHITE, line=950)
block(g, 364.6)

ys = [387.75, 405.5, 427.5, 439.75, 444.0, 463.0, 465.0, 473.25, 484.0, 500.5, 503.0, 506.75, 519.5, 540.75]
hs = [int(round((b - a) * 100)) for a, b in zip(ys, ys[1:])]
pills = ((61.8, 116.3), (63.8, 92.6), (76.1, 104.9))
xs = sorted({X0, 204.0, 220.0, 251.5, 361.0, 377.5, 397.5, X1} | {x for p in pills for x in p})
g = Grid("director", xs, hs)
side = dict(left="mid", right="mid")
# left: three stage boxes (year pill + title, gray body) joined by ▼
stages = (((0, 1), (1, 2), 390.4, 410.4, 115.0), ((4, 5), (5, 8), 446.7, 466.8, 92.0),
          ((9, 12), (12, 13), 503.1, 523.1, 104.0))
for ((p, q), (b0, b1), y_head, y_body, cut), (pa, pe) in zip(stages, pills):
    head = line1(60, 85, y_head - 1, y_head + 1)
    g.put(X0, pa, p, q, [], frame(top="mid", left="mid"))
    g.put(pa, pe, p, q, [runs_of(head, x1=cut)], frame(WHITE, top="mid", bottom="soft", left="soft", right="soft"),
          line=1050, fit=False)
    tight(g, pa, p)
    g.put(pe, 204.0, p, q, [strip_runs(runs_of(head, x0=cut))], frame(top="mid", right="mid"), align="LEFT")
    g.put(X0, 204.0, b0, b1, [line1(60, 72, y_body - 1, y_body + 3)], frame("#E8E8E8", bottom="mid", **side))
for r0, r1 in ((2, 4), (8, 9)):
    g.put(X0, 204.0, r0, r0 + 1, "▼", size=900, color=ARROW, line=1000)
    if r1 > r0 + 1:
        g.put(X0, 204.0, r0 + 1, r1, [])
# middle: 노동이사 전문성 지원 강화 (hatched tags | two centered lines)
g.put(220.0, 361.0, 0, 1, [line1(230, 240, 389, 393)], frame(HEAD, top="mid", **side))
for (r0, r1), (y0, y1) in zip(((1, 3), (3, 7), (7, 11), (11, 13)),
                              ((405, 439), (439, 473), (473, 506), (506, 540))):
    last = r1 == 13
    g.put(220.0, 251.5, r0, r1, lines_in(225, 230, y0, y1), frame("#E0E0E0", left="mid", bottom="mid" if last else "dot",
                                                                  **HATCH), line=1320)
    g.put(251.5, 361.0, r0, r1, lines_in(252, 360, y0, y1), frame(right="mid", bottom="mid" if last else "dot"),
          line=1440)
# right: 노동이사 이사회 경영제언 성과 (headline, 주요사례 cases)
g.put(377.5, X1, 0, 1, [line1(400, 405, 389, 393)], frame(HEAD, top="mid", **side))
g.put(377.5, X1, 1, 2, [line1(385, 390, 410, 413)], frame(**side))
g.put(377.5, 397.5, 2, 13, lines_in(382, 386, 455, 515), frame("#E0E0E0", left="mid", bottom="mid", **HATCH),
      line=1440)
for (r0, r1), (y0, y1) in zip(((2, 6), (6, 10), (10, 13)), ((433, 463), (468, 500), (506, 537))):
    case, detail = lines_in(398, 402, y0, y1)
    last = r1 == 13
    g.put(397.5, X1, r0, r1, [runs_of(case), hang(detail)],
          frame(right="mid", top="dot" if r0 > 2 else None, bottom="mid" if last else None), align="LEFT", line=1430)
# chevrons between the columns (blank gutter cells keep one single-row cell in every row)
for a, e in ((204.0, 220.0), (361.0, 377.5)):
    for r in range(len(hs)):
        g.put(a, e, r, r + 1, "▶" if r == 4 else [], size=1000, color=ARROW, fit=False)
block(g, 387.75)

# ---------------------------------------------------------------------------
# 다. 노사 공동 ESG
# ---------------------------------------------------------------------------
g = Grid("title-da", [X0, X1], [1650])
g.put(X0, X1, 0, 1, [line1(55, 60, 550, 553)], align="LEFT", line=1450)
block(g, 550.9)

g = Grid("background", [X0, 114.0, 312.0, 329.0, X1], [3725])
g.put(X0, 114.0, 0, 1, [line1(65, 70, 584, 588)], frame(HEAD, top="mid", bottom="mid", left="mid"))
g.put(114.0, 312.0, 0, 1, lines_in(115, 125, 577, 606), frame(top="mid", bottom="mid", right="mid"), line=1430)
g.put(312.0, 329.0, 0, 1, "▶", size=1000, color=ARROW)
g.put(329.0, X1, 0, 1, lines_in(330, 345, 577, 606), frame(top="mid", bottom="mid", left="mid", right="mid"),
      line=1430)
block(g, 572.25)

xs = [X0, 85.0, 133.7, 136.0, 453.5, 487.6, X1]
g = Grid("esg", xs, [4550, 425, 4400, 425, 4550])
for r, (y_letter, y_label, y_caption, y0, y1) in zip((0, 2, 4), ((625, 632, 618, 618, 660),
                                                              (674, 681, 667, 666, 708),
                                                              (722, 729, 719, 713, 757))):
    edge = dict(top="soft", bottom="soft")
    g.put(X0, 85.0, r, r + 1, [runs_of(line1(60, 65, y_letter - 1, y_letter + 1), bold=True)],
          frame("#EEEEEE", left="soft", **edge, **HATCH), line=2100)
    g.put(85.0, 133.7, r, r + 1, [line1(88, 92, y_label - 1, y_label + 1)], frame(right="soft", **edge))
    lines = lines_in(136, 452, y0, y1)
    first = [l for l in lines if abs(l["bbox"][1] - lines[0]["bbox"][1]) < 1]
    rest = [l for l in lines if l not in first]
    lead = runs_of(first[0])
    for extra in first[1:]:          # 'E' line 1 continues after a ➡ image
        lead = lead + [(" → ", 1090, False, "#505050")] + runs_of(extra)
    g.put(136.0, 453.5, r, r + 1, [lead] + [hang(l) for l in rest], frame(**edge), align="LEFT", line=1320)
    g.put(453.5, 487.6, r, r + 1, lines_in(455, 466, y_caption - 1, y_caption + 40), frame("#E8E8E8"), line=1000)
    g.put(487.6, X1, r, r + 1, [], photo)
block(g, 614.75)

g = Grid("result", [X0, 116.0, X1], [3725])
g.put(X0, 116.0, 0, 1, [runs_of(line1(65, 70, 776, 780), WHITE)], frame("#808080", top="mid", bottom="mid", left="mid"))
g.put(116.0, X1, 0, 1, lines_in(115, 120, 766, 800), frame(top="mid", bottom="mid", right="mid"), align="LEFT",
      line=1500)
block(g, 764.5)

kit.finish(target, end=803.0)
