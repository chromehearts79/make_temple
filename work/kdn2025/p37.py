"""Rebuild KDN 2025 report physical PDF page 37 (printed page 22) as editable HWPX.

Usage: python3 work/kdn2025/p37.py <report.pdf> <out.hwpx> [--page N]

윤리경영 ②: 4대 핵심위험 선정과 통제활동. Diagram page built with the shared kit (one flat
table per band on a union grid of PDF x edges, see kit.py / p19.py).
Image-only parts of the source are typed as editable cells, read from 4x renders:
  - the whole 가. analysis diagram (분석과정 / 분석결과 / 핵심위험 / 통제활동, PDF y 123-321),
  - the 준법윤리 거버넌스 organisation sketch (윤리경영위원회 ↔ 청렴시민감사관, 준법경영실),
  - the 신규 / 지적사항 개선 badges, the section number band and the side tab.
Arrows and chevrons drawn as images become KS X 1001 glyphs (→ ↔ ↖↘ ↙↗ ▶ ▼ +).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kit  # noqa: E402
from kit import Layout, recipe_inputs  # noqa: E402

source, target = recipe_inputs(37, "기관장 주도 4대 핵심위험 선정과 타겟형 통제활동으로 선제적 위험관리")
L = Layout(top=3100)
kit.setup(source, L)
from kit import *  # noqa: E402,F401,F403  helpers and presets bound to this page

HDR = "#E4E4E4"      # light header fill of the rounded boxes
GRAYL = "#E9E9E9"    # label tabs
DARKB = "#6A6A6A"    # dark badges / tabs


def margin(g, x0, r0, **pad):
    """Override the padding of the cell whose top-left slot is (r0, x0)."""
    c0 = g.xs.index(kit.to_x(x0))
    g.items[r0, c0] = g.items[r0, c0][:7] + (pad,)


def run(text, size=1090, bold=False, color=INK):
    return (text, size, bold, color)


def section_band(name, y, top, split=85.0):
    """'2 | title' band: dark number box and a light gray title strip (image in the PDF)."""
    g = Grid(name, [X0, split, X1], [2300])
    g.put(X0, split, 0, 1, [line1(60, 80, y - 2, y + 2)], frame("#5E5E5E"), color=WHITE, line=1800)
    g.put(split, X1, 0, 1, [line1(88, 95, y - 1, y + 3)], frame("#E4E4E4"), align="LEFT", line=1700)
    block(g, top)


def title_badge(name, line, edges, top, badge=None):
    """'가. [pill] title [badge]': edges = number | pill | title | (badge) | (rest)."""
    runs = runs_of(line)
    g = Grid(name, edges, [1650])
    g.put(edges[0], edges[1], 0, 1, [strip_runs(runs[:1])], align="LEFT", line=1450, fit=False)
    margin(g, edges[0], 0, left=0, right=0)
    g.put(edges[1], edges[2], 0, 1, [runs[1]], pill)
    g.put(edges[2], edges[3], 0, 1, [strip_runs(runs[2:])], align="LEFT", line=1450)
    if badge:
        g.put(edges[3], edges[4], 0, 1, badge, frame("#4A4A4A"), size=800, bold=True, color=WHITE, line=950)
    block(g, top)


# ---------------------------------------------------------------------------
# Page chrome: side tab, footer, running head (as p19)
# ---------------------------------------------------------------------------
L.add_table([[cell(0, 3350, 1680, [para([("01", 1380, True, WHITE)], "CENTER")[0]], dark)],
             [cell(0, 3350, 5960, [para([(ch, 950, True, INK)], "CENTER", 1160)[0] for ch in "경영관리"], gray2)]],
            floating=(57800, 15000))
foot = [(only_text, size, False, INK) for only_text, size in (
    (line1(450, 455, 818, 822)["text"], 790), ("    ", 790), (line1(540, 552, 816, 820)["text"], 1090))]
L.add_table([[cell(0, W, 1500, [para(foot, "RIGHT", 1300)[0]])]], floating=(5660, 81550))

g = Grid("head", [X0, 466.3, X1], [1680])
g.put(X0, 466.3, 0, 1, [], frame(bottom="soft"))
g.put(466.3, X1, 0, 1, [line1(465, 480, 35, 40)], align="RIGHT")
block(g, 32.0)

section_band("section-2", 74.0, 70.9)

# ---------------------------------------------------------------------------
# 가. 윤리위험 식별 (the diagram below the title is an image; text typed from a 4x render)
# ---------------------------------------------------------------------------
title_badge("title-ga", line1(55, 60, 100, 104), [X0, 76.5, 146.0, 476.0, 503.0, X1], 100.0, badge="신규")

xs = [X0, 110.5, 115.0, 129.0, 150.0, 189.0, 224.0, 254.5, 261.4, 264.5, 278.5, 303.5, 334.0,
      339.5, 362.0, 409.5, 412.5, 426.5, 439.5, 452.0, 548.0, X1]
g = Grid("analysis", xs, [1650, 4700, 550, 1750, 3050, 1700, 1450, 1950, 2100, 500])
label = frame(GRAYL)
g.put(X0, 110.5, 0, 2, "분석과정", label, size=1150)
g.put(X0, 110.5, 3, 5, "분석결과", label, size=1150)
steps = [((115.0, 129.0, 261.4), "윤리위험 식별",
          ["기관장의 경영진 회의 지시 사항", "청렴 · 윤리 법령 및 이슈 반영", "K-CP 기반 부패 리스크 분류"]),
         ((264.5, 278.5, 409.5), "윤리위험 평가",
          ["총 27개 윤리위험 식별", "FGI 인터뷰 및 전문기관 컨설팅", "발생가능성 및 피해영향 평가"]),
         ((412.5, 426.5, X1), "윤리위험 분류",
          ["기관장 주재 리스크 선정 회의", "→핵심위험 확정 및 타겟 설정", "핵심위험 및 일반위험 분류"])]
starts = [115.0, 261.4, 409.5]
for k, ((a, b, e), head, bullets) in enumerate(steps):
    g.put(a, b, 0, 1, str(k + 1), frame(DARKB, top="mid"), size=1050, bold=True, color=WHITE)
    g.put(b, e, 0, 1, head, frame("#EEEEEE", top="mid", hatch="#D2D2D2"), align="LEFT", size=1090, bold=True)
    body = [[run("∙ " if not t.startswith("→") else "  ", 1000), run(t, 1000)] for t in bullets]
    g.put(starts[k], e, 1, 2, body, frame(right="dot") if k < 2 else "1", align="LEFT", line=1300)
strong_box = dict(left="strong", right="strong")
g.put(115.0, 334.0, 3, 4, "기관장 선정 4대 핵심위험", frame(top="strong", **strong_box), size=1100, bold=True)
g.put(115.0, 334.0, 4, 5, ["갑질 / 부정청탁 / 예산 남용 /", "특혜제공(인사운영)"], frame("#EDEDED", **strong_box),
      size=1020, line=1250)
g.put(339.5, X1, 3, 4, "일반위험", frame(top="soft", left="soft", right="soft"), size=1100, bold=True)
g.put(339.5, X1, 4, 5, ["음주운전 / 성관련 비위 / 채용비리 /", "직무상 비밀 이용 / 금품수수 등 23개 위험"],
      frame("#EDEDED", left="soft", right="soft", bottom="soft"), size=1020, line=1250)
# Heavy outline: the 4대 핵심위험 box opens into the 핵심위험 / 통제활동 block below.
g.put(X0, 110.5, 5, 6, [], frame(top="strong", left="strong"))
g.put(110.5, 115.0, 5, 6, [], frame(top="strong"))
g.put(115.0, 334.0, 5, 6, "▼", frame(**strong_box), size=1000, color=ARROW, line=1100)
g.put(334.0, X1, 5, 6, [], frame(top="strong", right="strong"))
g.put(X0, 110.5, 6, 8, "핵심위험", frame(GRAYL, left="strong"), size=1150)
g.put(X0, 110.5, 8, 9, "통제활동", frame("#8C8C8C", left="strong"), size=1150, color=WHITE)
risks = [((115.0, 150.0, 189.0, 224.0), "갑질", "갑질근절 노력", "통제활동-① (p.22)"),
         ((224.0, 254.5, 303.5, 334.0), "부정 청탁", "부패요인 차단", "통제활동-② (p.23)"),
         ((334.0, 362.0, 409.5, 439.5), "예산 남용", "예산 · 회계 신뢰성 강화", "통제활동-③ (p.24)"),
         ((439.5, 452.0, 548.0, X1), "특혜제공(인사운영)", "기관 투명성 제고", "통제활동-④ (p.24)")]
for k, ((a, t0, t1, e), tab, head, ref) in enumerate(risks):
    side = "strong" if k == 3 else "dot"
    g.put(a, t0, 6, 7, [], frame(top="mid"))
    g.put(t0, t1, 6, 7, tab, frame(DARKB, top="mid"), size=1000, bold=True, color=WHITE, line=1150)
    g.put(t1, e, 6, 7, [], frame(top="mid", right=side))
    g.put(a, e, 7, 8, head, frame(right=side), size=1050, bold=True)
    g.put(a, e, 8, 9, ref, frame("#E6E6E6", right=side), size=1050)
g.put(X0, X1, 9, 10, [], frame(left="strong", right="strong", bottom="strong"))
block(g, 122.8)

# ---------------------------------------------------------------------------
# 나. 관리체계 강화
# ---------------------------------------------------------------------------
title_badge("title-na", line1(55, 60, 333, 337), [X0, 76.5, 151.5, X1], 332.6)

xs = [X0, 66.0, 91.0, 99.9, 102.0, 108.0, 112.0, 147.0, 154.0, 160.5, 197.0, 207.0, 253.5, 259.2,
      273.0, 277.0, 310.0, 337.0, 402.0, 410.0, 420.0, X1]
g = Grid("governance", xs, [1750, 500, 1500, 1450, 1650, 450, 1450, 470, 630, 1720, 5460])
soft = "soft"


def box_header(r, y, left_x, title_x):
    """Header strip of one rounded box: pale fill, year pill, title (and → 활동 실적)."""
    hdr = line1(left_x - 2, left_x + 2, y - 1, y + 2)
    if left_x < 200:
        g.put(102.0, 112.0, r, r + 1, [], frame(HDR, top=soft, left=soft))
        g.put(112.0, 147.0, r, r + 1, [runs_of(hdr, x1=title_x)], frame(WHITE, top=soft, bottom=soft, left=soft, right=soft),
              line=1100)
        g.put(147.0, 259.2, r, r + 1, [runs_of(hdr, x0=title_x)], frame(HDR, top=soft, right=soft), align="LEFT")
    else:
        g.put(273.0, 277.0, r, r + 1, [], frame(HDR, top=soft, left=soft))
        g.put(277.0, 310.0, r, r + 1, [runs_of(hdr, WHITE, x1=title_x)], frame(DARKB, top=soft), line=1100)
        g.put(310.0, 402.0, r, r + 1, [runs_of(hdr, x0=title_x)], frame(HDR, top=soft), align="LEFT")
        g.put(402.0, 420.0, r, r + 1, "→", frame(HDR, top=soft), size=1100, bold=True, color="#555555")
        g.put(420.0, X1, r, r + 1, [line1(460, 465, y, y + 3)], frame(HDR, top=soft, right=soft))


# Row group 1: 준법윤리 거버넌스
g.put(X0, 99.9, 0, 1, [], frame(GRAYL))
g.put(X0, 99.9, 1, 4, lines_in(58, 62, 380, 410), frame(GRAYL), line=1320)
g.put(X0, 66.0, 4, 5, [], frame(GRAYL))
g.put(66.0, 91.0, 4, 5, "신규", frame("#3A3A3A"), size=800, bold=True, color=WHITE, line=950)   # badge image
g.put(91.0, 99.9, 4, 5, [], frame(GRAYL))
g.put(X0, 99.9, 5, 8, [], frame(GRAYL))
box_header(0, 358.7, 120.3, 146.0)
box_header(0, 358.7, 283.7, 309.0)
# Organisation sketch (image): committee ↔ citizen auditor, both linked to 준법경영실.
g.put(102.0, 108.0, 1, 6, [], frame(left=soft))
g.put(253.5, 259.2, 1, 6, [], frame(right=soft))
tiny = frame(top=soft, bottom=soft, left=soft, right=soft)
g.put(108.0, 160.5, 2, 3, "윤리경영위원회", tiny, size=900)
g.put(160.5, 197.0, 2, 3, "↔", size=1100, color="#555555")
g.put(197.0, 253.5, 2, 3, "청렴시민감사관", tiny, size=900)
g.put(112.0, 154.0, 3, 4, "↖↘", size=1000, color="#555555")
margin(g, 112.0, 3, left=0, right=0)
g.put(207.0, 253.5, 3, 4, "↙↗", size=1000, color="#555555")
margin(g, 207.0, 3, left=0, right=0)
g.put(154.0, 207.0, 4, 5, "준법경영실", frame(DARKB), size=900, bold=True, color=WHITE)
need = line1(110, 120, 430, 434)
g.put(102.0, 259.2, 6, 8, [[run("→ ")] + runs_of(need)], frame(left=soft, right=soft, bottom=soft), align="LEFT")
g.put(259.2, 273.0, 1, 8, "▶", size=1200, color=ARROW, fit=False)
# '25 준법윤리 전문가 영입: bullet + 개방형 직위 table | 활동 실적
g.put(273.0, 410.0, 1, 3, [line1(275, 280, 378, 380)], frame(left=soft), align="LEFT")
g.put(273.0, 277.0, 3, 7, [], frame(left=soft))
cellhead = frame("#E4E4E4", top=soft, bottom=soft)
g.put(277.0, 337.0, 3, 4, [line1(284, 287, 394, 397)], cellhead, line=1150)
g.put(337.0, 402.0, 3, 4, [line1(352, 356, 394, 397)], cellhead, line=1150)
chief = line1(280, 285, 412, 415)
g.put(277.0, 337.0, 4, 7, [runs_of(chief, x1=330)], frame(bottom=soft, right=soft), size=990)
g.put(337.0, 402.0, 4, 7, [runs_of(chief, x0=330), line1(350, 352, 426, 429)], frame(bottom=soft), line=1250)
g.put(273.0, 410.0, 7, 8, [], frame(left=soft, bottom=soft))
g.put(410.0, X1, 1, 8, lines_in(412, 414, 378, 442), frame(left=soft, right=soft, bottom=soft), align="LEFT",
      line=1540)
# Row group 2: 청렴시민 감사관 전문성 강화
g.put(X0, 99.9, 9, 11, lines_in(58, 70, 462, 516), frame(GRAYL), line=1320)
box_header(9, 457.1, 118.8, 146.0)
box_header(9, 457.1, 283.7, 309.0)
b1 = lines_in(106, 110, 476, 522)
g.put(102.0, 259.2, 10, 11, [b1[0], [run("   ")] + runs_of(b1[1]), [run("→ ")] + runs_of(b1[2])],
      frame(left=soft, right=soft, bottom=soft), align="LEFT", line=1540)
g.put(259.2, 273.0, 10, 11, "▶", size=1200, color=ARROW, fit=False)
b2 = lines_in(277, 290, 476, 522)
g.put(273.0, 410.0, 10, 11, [b2[0], [run("  ")] + runs_of(b2[1]), [run("   ")] + runs_of(b2[2])],
      frame(left=soft, bottom=soft), align="LEFT", line=1540)
g.put(410.0, X1, 10, 11, lines_in(412, 414, 476, 522), frame(left=soft, right=soft, bottom=soft), align="LEFT",
      line=1540)
block(g, 355.4)

# ---------------------------------------------------------------------------
# 다. 핵심위험 통제
# ---------------------------------------------------------------------------
title_badge("title-da", line1(55, 60, 537, 541), [X0, 73.0, 142.5, 503.5, X1], 536.7, badge="지적사항 개선")

head = line1(68, 72, 558, 562)
g = Grid("heading-gap", [X0, 456.5, 510.5, X1], [1600])
g.put(X0, 456.5, 0, 1, [[("□ ", 1350, True, INK)] + runs_of(head, x1=456)], align="LEFT", line=1400)
g.put(456.5, 510.5, 0, 1, [runs_of(head, x0=456)], frame(WHITE, top=soft, bottom=soft, left=soft, right=soft),
      line=1100)
block(g, 558.5)

g = Grid("pledge", [X0, 100.6, 319.9, 333.7, X1], [1800, 4160])
g.put(X0, 100.6, 0, 2, lines_in(60, 70, 595, 615), frame(GRAYL, top=soft, bottom=soft, left=soft), line=1300)
g.put(100.6, 319.9, 0, 1, [line1(130, 135, 584, 588)], frame("#DCDCDC", top=soft, right=soft), bold=True)
g.put(100.6, 319.9, 1, 2, lines_in(120, 170, 603, 622), frame(bottom=soft, right=soft), line=1420)
g.put(319.9, 333.7, 0, 2, "+", size=1500, bold=True, color=ARROW, fit=False)
g.put(333.7, X1, 0, 1, [line1(400, 405, 584, 588)], frame("#DCDCDC", top=soft, left=soft, right=soft))
g.put(333.7, X1, 1, 2, lines_in(370, 380, 603, 622), frame(bottom=soft, left=soft, right=soft), line=1420)
block(g, 579.7)

# Brace joining the two pledges to the three action columns (image): rule + ▼
g = Grid("brace", [X0, 294.0, 318.0, X1], [700, 700])
g.put(X0, 294.0, 0, 1, [], frame(bottom="mid"))
g.put(294.0, 318.0, 0, 2, "▼", size=900, color=ARROW, line=1000)
g.put(318.0, X1, 0, 1, [], frame(bottom="mid"))
block(g, 642.0)

xs = [X0, 221.3, 223.9, 228.0, 384.5, 388.6, 391.1, X1]
g = Grid("actions", xs, [1750, 400, 1700, 2000, 2700, 3300, 1900, 750])
cols = [(X0, 221.3), (223.9, 388.6), (391.1, X1)]
for k, (a, e) in enumerate(cols):
    g.put(a, e, 0, 1, [line1(a + 2, e, 660, 664)], frame("#D8D8D8", top="mid", left=soft, right=soft, bottom=soft),
          bold=True)
    g.put(a, e, 1, 2, [], frame(left=soft, right=soft))
    g.put(a, e, 2, 3, [line1(a + 2, e, 680, 684)], frame("#ECECEC", left=soft, right=soft, hatch="#D6D6D6"))
g.put(X0, 221.3, 3, 8, [lines_in(60, 65, 705, 720)[0]] + [[run("  ")] + runs_of(l) for l in lines_in(60, 80, 720, 790)],
      frame(left=soft, right=soft, bottom=soft), align="LEFT", line=1760)
g.put(391.1, X1, 3, 8, lines_in(395, 400, 705, 790), frame(left=soft, right=soft, bottom=soft), align="LEFT", line=1760)
quote = frame("#EFEFEF", top=soft, bottom=soft, left=soft, right=soft)
g.put(223.9, 228.0, 3, 7, [], frame(left=soft))
g.put(384.5, 388.6, 3, 7, [], frame(right=soft))
g.put(228.0, 384.5, 3, 4, [line1(228, 231, 700, 703)], align="LEFT")
g.put(228.0, 384.5, 4, 5, lines_in(229, 233, 716, 730), quote, size=990, line=1150)
g.put(228.0, 384.5, 5, 6, [line1(228, 231, 746, 749), [run("  ")] + runs_of(line1(236, 239, 760, 763))],
      align="LEFT", line=1450)
g.put(228.0, 384.5, 6, 7, [line1(228, 231, 778, 781)], quote, size=990, line=1150)
g.put(223.9, 388.6, 7, 8, [], frame(left=soft, right=soft, bottom=soft))
block(g, 656.6)

kit.finish(target, end=801.6)
