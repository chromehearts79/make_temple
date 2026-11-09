"""Rebuild KDN 2025 report physical PDF page 30 (printed page 18) as editable HWPX.

Usage: python3 work/kdn2025/p30.py <report.pdf> <out.hwpx> [--page N]

"5 ESG 혁신" diagram page, built with the shared kit (one flat table per horizontal band on a
grid of PDF x edges, text taken line by line from the PDF with its spans, 장평 fitted per cell).
The 해상풍력 / 수소 E / VPP grid of 가. is one image in the PDF: its text is typed from a 4x
render (icons omitted). The 단선 pie chart of 나. is an image too: it becomes small value cells
with the labels and counts it prints (read from a 5x render), not a drawn chart. Rounded boxes,
chevrons and gradients become cell fills and borders; arrow and number images become KS X 1001
glyphs (→ ▶ ▼ ⑤ ⑥); the KDN logo in the footer is typed as text.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kit  # noqa: E402
from kit import Layout, recipe_inputs  # noqa: E402

source, target = recipe_inputs(30, "業의 특성 기반 기술 혁신으로 지속성장을 강화하는 ESG 혁신")
L = Layout(top=3100)
kit.setup(source, L)
from kit import *  # noqa: E402,F401,F403  helpers and presets bound to this page

# ---------------------------------------------------------------------------
# Page-specific helpers and fills
# ---------------------------------------------------------------------------
HEAD_GRAY = "#D9D9D9"   # 문제인식 / column headers
HEAD_DARK = "#6B6B6B"   # 혁신 아이디어 탐색, 주요성과 label
LABEL = "#E3E3E3"        # vertical side labels (사업역량혁신 ...)
HATCH = frame("#EEEEEE", hatch="#DEDEDE")


def R(line, **kw):
    return runs_of(line, **kw)


def indent(runs):
    """Continuation line under a bullet: indented like the source."""
    runs = list(runs)
    return [("  ", runs[0][1], runs[0][2], runs[0][3])] + runs


def lead(glyph, runs, size=None):
    """Prefix a typed glyph (image in the PDF) to a line, same weight as the line."""
    runs = list(runs)
    return [(glyph + " ", size or runs[0][1], runs[0][2], runs[0][3])] + runs


def recolor(runs, color):
    return [(t, s, b, color) for t, s, b, _ in runs]


def section_band(name, number, line, top, pill_end):
    """'3 [badge] title' band: dark number box, dark pill badge (spans under 13 pt), gray title band."""
    runs = R(line)
    badge = [r for r in runs if r[1] < 1300]
    g = Grid(name, [X0, 83.3, 91.0, pill_end, X1], [2300])
    g.put(X0, 83.3, 0, 1, number, frame("#5E5E5E"), size=1700, bold=True, color=WHITE, line=1900)
    band = frame("#E4E4E4")
    g.put(83.3, 91.0, 0, 1, [], band)
    g.put(91.0, pill_end, 0, 1, [recolor(strip_runs(badge), WHITE)], frame("#5E5E5E"))
    g.put(pill_end, X1, 0, 1, [strip_runs(runs[len(badge):])], band, align="LEFT", line=1750)
    block(g, top)


def task_heading(name, head, title, edges, top, mark):
    """'가. [혁신과제 ①] title' : number, light pill badge with the typed number, 14pt title."""
    runs = R(head)
    g = Grid(name, edges + [X1], [1650])
    g.put(edges[0], edges[1], 0, 1, [strip_runs(runs[:1])], align="LEFT", line=1450)
    g.put(edges[1], edges[2], 0, 1, [strip_runs(runs[1:]) + [(" " + mark, 1090, True, INK)]], pill)
    g.put(edges[2], X1, 0, 1, [R(title)], align="LEFT", line=1450)
    block(g, top)


def problem_box(name, top, split, heads, left, right, hs=(1900, 3750)):
    """문제인식 (gray head) ▶ 혁신 아이디어 탐색 (dark head) pair of rounded boxes."""
    a, b = split
    g = Grid(name, [X0, a, b, X1], list(hs))
    g.put(X0, a, 0, 1, [heads[0]], frame(HEAD_GRAY, top="mid", left="mid", right="mid", bottom="soft"), line=1250)
    g.put(b, X1, 0, 1, [recolor(R(heads[1]), WHITE)], frame(HEAD_DARK, top="mid", left="mid", right="mid"),
          line=1250)
    g.put(X0, a, 1, 2, left, frame(left="mid", right="mid", bottom="mid"), align="LEFT", line=1600)
    g.put(a, b, 1, 2, "▶", size=1300, color="#BDBDBD", fit=False)
    g.put(b, X1, 1, 2, right, frame(left="mid", right="mid", bottom="mid"), align="LEFT", line=1600)
    block(g, top)


def results_box(name, top, label, lines, height, line=1450):
    """주요성과: dark label and an outlined bold text cell."""
    g = Grid(name, [X0, 112.0, X1], [height])
    g.put(X0, 112.0, 0, 1, [recolor(R(label), WHITE)], frame(HEAD_DARK, top="mid", left="mid", bottom="mid"))
    g.put(112.0, X1, 0, 1, lines, frame(top="mid", right="mid", bottom="mid", left="soft"), align="LEFT", line=line)
    block(g, top)


def chip_split(line, split):
    """One PDF line that starts with an inline chip: (chip runs, text runs)."""
    return strip_runs(R(line, x1=split)), strip_runs(R(line, x0=split))


CHIP_WHITE = frame(WHITE, top="soft", bottom="soft", left="soft", right="soft")
CHIP_DARK = frame("#6E6E6E")

# ---------------------------------------------------------------------------
# Page 30 (even page: PART box head, footer at the left)
# ---------------------------------------------------------------------------
foot = [(line1(55, 60, 815, 820)["text"], 1090, False, INK), ("    ", 1090, False, INK),
        ("한전KDN㈜", 1100, True, INK)]
L.add_table([[cell(0, W, 1500, [para(foot, "LEFT", 1300)[0]])]], floating=(5660, 81550))

g = Grid("head", [X0, 102.7, 158.0, X1], [1560])
g.put(X0, 102.7, 0, 1, [[("PART ", 780, False, INK), ("01", 1350, True, "#555555")]],
      frame("#F4F4F4", top="soft", left="soft", bottom="soft"), line=1380)
g.put(102.7, 158.0, 0, 1, "경영관리", frame("#333333", bottom="soft"), size=1080, bold=True, color=WHITE)
g.put(158.0, X1, 0, 1, [], frame(bottom="soft"))
block(g, 31.7)

section_band("band-5", "5", line1(98, 102, 74, 78), 70.9, 151.0)

# ---- 가. 혁신과제 5 -------------------------------------------------------------
task_heading("title-ga", line1(55, 60, 100, 103), line1(138, 142, 100, 103), [X0, 76.9, 140.1], 99.8, "⑤")

problem_box(
    "problem-ga", 122.7, (297.5, 314.5),
    (line1(155, 165, 125, 130), line1(390, 400, 125, 130)),
    lines_in(60, 65, 145, 175),
    [line1(315, 320, 145, 150), indent(R(line1(325, 330, 160, 165)))])

# 개선점 / 혁신노력 / 추진실적 x 해상풍력 / 수소 E / VPP: an image in the PDF, typed from a 4x render.
B, N = True, False
COLUMNS = [
    dict(title="해상풍력",
         need=["기상변화 대응 발전량 예측", "및 선박경로감시(충돌방지) 기술 필요"],
         safe=["AI기반 선박 경로, 파고 등", "예측으로 해상활동 감시 및", "충돌방지 등 안전사고 예방"],
         eff=["발전량 예측·설비진단·", "모니터링의 지능형 통합운영", "관제 솔루션 도입"],
         done=["국내 최대 규모 400MW급", "낙월해상풍력단지 관제로"],
         gain=[[("온실가스 41.35만tCO", 1030, B), ("2eq", 680, B), (" 절감 효과", 1030, B)],
               [("(소나무 300만 그루 식재 효과)", 960, N)]]),
    dict(title="수소 E",
         need=["수소E 수요량 예측 및 통합운영", "기술로 안전한 수소생태계 구축"],
         safe=["수소 全주기(생산~소비)", "안전 감시, 수소 버스 등 수소", "도시 데이터 통합 관리 확대"],
         eff=["수소 생산 · 소비 데이터 기반", "수요량 최적 예측"],
         done=["전주 · 완주 수소시범도시", "통합센터 운영으로"],
         gain=[[("온실가스 1.13만tCO", 1030, B), ("2eq", 680, B), (" 절감 효과", 1030, B)],
               [("(소나무 8.1만 그루 식재 효과)", 960, N)]]),
    dict(title="VPP",
         need=["기존 전력계통 안전을 위한 신재생E", "발전량 예측 · 출력제어 고도화 필요"],
         safe=["전력계통 안정을 위한", "전력 거래, 실시간 전력 조절", "(급전지시 대응) 등 통합 관리"],
         eff=["실시간 대응 · 정산 · 제어", "가능한 통합발전소(VPP)", "솔루션 실증"],
         done=["기상, 수요를 반영한", "재생E 발전량"],
         gain=[[("재생에너지 AI예측 시스템", 1030, B), ("(정확도 95%)", 820, N), (" 활용", 1030, B)],
               [("제주 VPP 실증 완료", 1030, B)]]),
]
xs = [X0, 82.0, 123.0, 241.0, 280.0, 399.0, 436.5, X1]
g = Grid("three-fields", xs, [1950, 3850, 1500, 3150, 1500, 2900, 3350, 3980])
g.put(X0, 82.0, 0, 2, lines_in(62, 66, 190, 240), frame(LABEL), bold=True, line=1320)
g.put(X0, 82.0, 2, 6, lines_in(62, 66, 262, 322), frame(LABEL), bold=True, line=1320)
g.put(X0, 82.0, 6, 8, lines_in(62, 66, 345, 402), frame(LABEL), bold=True, line=1320)
for k, ((a, c, e), col) in enumerate(zip(((82.0, 123.0, 241.0), (241.0, 280.0, 399.0), (399.0, 436.5, X1)), COLUMNS)):
    sep = "dot" if k < 2 else None
    head = frame("#E4E4E4", right=sep)
    g.put(a, e, 0, 1, col["title"], head, size=1100, bold=True)
    g.put(a, e, 1, 2, col["need"], head, size=1000, line=1300)
    for r, chip, key in ((2, "안전 Up", "safe"), (4, "효율 Up", "eff")):
        g.put(a, c, r, r + 1, chip, CHIP_DARK, size=850, color=WHITE, line=1000)
        g.put(a, c, r + 1, r + 2, [], frame())
        g.put(c, e, r, r + 2, col[key], frame(right=sep), align="LEFT", size=960, line=1250)
    g.put(a, e, 6, 7, col["done"], frame(top="soft", right=sep), size=1030, line=1300)
    g.put(a, e, 7, 8, [[(t, s, b, INK) for t, s, b in runs] for runs in col["gain"]],
          frame("#EDEDED", hatch="#DEDEDE", bottom="soft"), line=1400)
block(g, 185.5)

results_box("results-ga", 413.9, line1(60, 70, 424, 430), lines_in(115, 120, 416, 447), 3520, line=1500)

# ---- 나. 혁신과제 6 -------------------------------------------------------------
task_heading("title-na", line1(55, 60, 461, 465), line1(138, 142, 461, 465), [X0, 76.9, 140.1], 460.2, "⑥")

prob = lines_in(60, 75, 505, 550)
problem_box(
    "problem-na", 483.0, (297.5, 314.5),
    (line1(155, 165, 486, 490), line1(390, 400, 486, 490)),
    [prob[0], indent(R(prob[1])), indent(R(prob[2]))],
    [line1(315, 320, 512, 516), indent(R(line1(325, 330, 527, 532)))], hs=(1900, 5090))

# 개선점: 기존 (pie chart image -> value cells read from a 5x render) ▶ 개선.
xs = [X0, 82.0, 128.0, 139.0, 163.0, 166.0, 200.6, 314.5, 324.5, 377.0, 401.0, X1]
g = Grid("improve-na", xs, [1850, 1100, 1500, 2760])
g.put(X0, 82.0, 0, 4, lines_in(62, 66, 574, 616), frame(LABEL), bold=True, line=1320)
light, darkh = frame("#DADADA", top="soft"), frame("#7A7A7A", top="soft")
chip, text = chip_split(line1(144, 148, 562, 566), 161.5)
g.put(82.0, 139.0, 0, 1, [], light)
g.put(139.0, 163.0, 0, 1, [chip], CHIP_WHITE, line=1000)
g.put(163.0, 314.5, 0, 1, [text], light, align="LEFT")
g.put(314.5, 324.5, 0, 1, "▶", size=900, color="#7A7A7A", fit=False)
chip, text = chip_split(line1(382, 386, 562, 566), 399.5)
g.put(324.5, 377.0, 0, 1, [], darkh)
g.put(377.0, 401.0, 0, 1, [chip], frame("#555555", top="soft", bottom="soft", left="soft", right="soft"),
      color=WHITE, line=1000)
g.put(401.0, X1, 0, 1, [recolor(text, WHITE)], darkh, align="LEFT")
g.put(82.0, 166.0, 1, 2, "(3개년 평균)", size=720, line=820)
g.put(82.0, 128.0, 2, 4, ["그 외", "선로사고", "869건"], frame("#E2E2E2"), size=780, line=880)
g.put(128.0, 166.0, 2, 4, [[("단선사고", 800, True, WHITE)], [("88건", 800, True, WHITE)]], frame("#4A4A4A"), line=950)
g.put(166.0, 200.6, 1, 3, [[("검출", 780, False, WHITE)], [("47건", 780, False, WHITE)]], frame("#7A7A7A"),
      line=880)
g.put(166.0, 200.6, 3, 4, ["미검출", "41건"], frame("#BDBDBD"), size=780, line=880)
issue = lines_in(200, 215, 588, 620)
g.put(200.6, 314.5, 1, 4, [issue[0], indent(R(issue[1]))], align="LEFT", line=1500)
need = lines_in(324, 335, 580, 628)
g.put(324.5, X1, 1, 4, [need[0], indent(R(need[1])), need[2]], frame(left="dot"), align="LEFT", line=1500)
block(g, 559.1)

# 혁신노력: one outlined box, header flow and three chip rows.
xs = [X0, 82.0, 84.5, 110.0, 358.0, 455.0, X1]
g = Grid("effort-na", xs, [2140, 1650, 1550, 2110])
g.put(X0, 82.0, 0, 4, lines_in(62, 66, 648, 705), frame(LABEL), bold=True, line=1320)
flow = (R(line1(218, 222, 640, 645)) + [(" → ", 1090, True, INK)] + R(line1(344, 348, 640, 645))
        + [(" → ", 1090, True, INK)] + R(line1(395, 399, 640, 645)))
g.put(84.5, X1, 0, 1, [flow], frame(top="mid", left="mid", right="mid", bottom="dot"))
for r, y in ((1, 664), (2, 680), (3, 696)):
    line = line1(92, 95, y - 3, y + 2)
    last = r == 3
    side = dict(bottom="mid") if last else {}
    g.put(84.5, 110.0, r, r + 1, [strip_runs(R(line, x1=110.0))],
          frame("#F2F2F2", top="soft", bottom="soft", left="soft", right="soft"), line=1000)
    if r == 1:
        g.put(110.0, 358.0, r, r + 1, [strip_runs(R(line, x0=110.0, x1=358.0))], align="LEFT")
        g.put(358.0, 455.0, r, r + 1, [recolor(strip_runs(R(line, x0=358.0)), WHITE)], CHIP_DARK, line=1000)
        g.put(455.0, X1, r, r + 1, [], frame(right="mid"))
    else:
        g.put(110.0, X1, r, r + 1, [strip_runs(R(line, x0=110.0))], frame(right="mid", **side), align="LEFT")
block(g, 637.1)

# 추진실적: two columns with dark heads.
xs = [X0, 82.0, 84.5, 311.0, X1]
g = Grid("result-na", xs, [2000, 1600, 2010])
g.put(X0, 82.0, 0, 3, lines_in(62, 66, 720, 770), frame(LABEL), bold=True, line=1100)
for (a, e), hx in (((84.5, 311.0), 100), ((311.0, X1), 335)):
    g.put(a, e, 0, 1, [recolor(R(line1(hx, hx + 5, 721, 726)), WHITE)], frame("#7A7A7A", top="soft"))
g.put(84.5, 311.0, 1, 2, [line1(88, 92, 738, 745)], frame(left="soft"), align="LEFT")
g.put(84.5, 311.0, 2, 3, [line1(88, 92, 754, 760)], frame(left="soft", bottom="soft"), align="LEFT")
g.put(311.0, X1, 1, 2, [line1(312, 316, 738, 745)], frame(left="soft", right="soft"), align="LEFT")
g.put(311.0, X1, 2, 3, [indent(lead("→", R(line1(312, 316, 751, 756))))],
      frame(left="soft", right="soft", bottom="soft"), align="LEFT")
block(g, 717.6)

results_box("results-na", 779.0, line1(60, 70, 783, 788), [line1(115, 120, 783, 788)], 2290, line=1350)

kit.finish(target, end=803.0)
