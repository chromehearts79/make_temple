"""Rebuild KDN 2025 report physical PDF page 24 (printed page 12) as editable HWPX.

Usage: python3 work/kdn2025/p24.py <report.pdf> <out.hwpx> [--page N]

4. 미래성장과 국정과제 중심의 전략적 자원배분 및 PDCA 기반 성과관리 강화 (even page: PART 01
box, footer left). Built with work/kdn2025/kit.py (one flat table per band on PDF x edges).
Text-layer lines come from the PDF with their spans; tags are split into their own cells.
Image-only parts (PART box, 지적사항 개선 tag, ①②③ numbers, ➡ / + / ▼ connectors and the three
donut charts) are typed from 4x renders: the charts become a value table (unit, year totals,
three business shares each) with the values printed in the charts.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kit  # noqa: E402
from kit import Layout, recipe_inputs  # noqa: E402

source, target = recipe_inputs(24, "국정과제･비전 연계 우선순위 기반 전략적 자원배분 체계 확립")
L = Layout(top=3100)
kit.setup(source, L)
from kit import *  # noqa: E402,F401,F403  helpers and presets bound to this page

side = dict(left="soft", right="soft")
TAG = "#5A5A5A"
LABEL = frame("#E2E2E2", top="dot")
ARR = "#505050"


def first_cut(line):
    """x just before the second text span (tag | text split)."""
    spans = [s for s in line["spans"] if s["text"].strip()]
    return spans[1]["bbox"][0] - 0.5


# ---------------------------------------------------------------------------
# Page chrome (even page): PART 01 box over a rule, page number + company name bottom left.
# ---------------------------------------------------------------------------
foot = [(line1(55, 60, 816, 820)["text"], 1090, False, INK), ("   ", 1090, False, INK),
        ("한전KDN㈜", 1000, True, INK)]
L.add_table([[cell(0, W, 1500, [para(foot, "LEFT", 1300)[0]])]], floating=(5660, 81550))

g = Grid("head", [X0, 102.6, 158.6, X1], [1600])
g.put(X0, 102.6, 0, 1, [[("PART ", 820, False, INK), ("01", 1450, True, "#505050")]], align="LEFT", line=1400,
      fit=False)
g.put(102.6, 158.6, 0, 1, "경영관리", frame("#333333"), size=1080, bold=True, color=WHITE)
g.put(158.6, X1, 0, 1, [], frame(bottom="soft"))
block(g, 31.8)

g = Grid("section-4", [X0, 84.6, X1], [2300])
g.put(X0, 84.6, 0, 1, [line1(60, 70, 72, 76)], frame("#5A5A5A"), color=WHITE)
g.put(84.6, X1, 0, 1, [line1(90, 95, 72, 77)], frame("#E4E4E4"), align="LEFT")
block(g, 70.9)

# 가. [자원배분] title + 지적사항 개선 tag (image)
runs = runs_of(line1(55, 60, 101, 105))
g = Grid("title-ga", [X0, 77.6, 127.0, 473.5, 527.0, X1], [1700])
g.put(X0, 77.6, 0, 1, [strip_runs(runs[:1])], align="LEFT", line=1450)
g.put(77.6, 127.0, 0, 1, [runs[1]], pill)
g.put(127.0, 473.5, 0, 1, [strip_runs(runs[2:])], align="LEFT", line=1450)
g.put(473.5, 527.0, 0, 1, "지적사항 개선", frame("#2E2E2E"), size=740, bold=True, color=WHITE, line=900)
block(g, 101.5)

# 수립체계 bar and the ▼ chevron below it
g = Grid("plan-system", [X0, 105.4, X1], [2000])
g.put(X0, 105.4, 0, 1, [line1(62, 64, 130, 132)], frame(top="soft", bottom="soft", **side), bold=True)
g.put(105.4, X1, 0, 1, [line1(108, 111, 130, 132)], frame("#E6E6E6", top="soft", bottom="soft"), align="LEFT")
block(g, 127.0)
g = Grid("arrow-1", [X0, X1], [1100])
g.put(X0, X1, 0, 1, "▼", size=1100, color="#9A9A9A", line=900)
block(g, 151.5)

# 우선순위 선정방향: three boxes, numbered heads (①②③ are images) over gray bullet rows
xs = [X0, 105.4, 110.5, 252.7, 260.7, 402.9, 410.9, 553.1, X1]
g = Grid("priority", xs, [2110, 2450])
g.put(X0, 105.4, 0, 2, lines_in(60, 62, 174, 190), LABEL, bold=True)
for (a, e), x, num in (((110.5, 252.7), 141.5, "①"), ((260.7, 402.9), 285.3, "②"), ((410.9, 553.1), 429.4, "③")):
    g.put(a, e, 0, 1, [[(num + " ", 1090, True, INK)] + runs_of(line1(x - 1, x + 1, 169, 171))],
          frame(top="mid", **dict(left="mid", right="mid")))
    g.put(a, e, 1, 2, [lines_in(a, e, 190, 193)[0]], frame("#E9E9E9", bottom="mid", left="mid", right="mid"))
block(g, 164.9)

# 조직운영 및 기능조정: three boxes joined by + connectors
xs = [X0, 105.4, 110.5, 245.2, 264.5, 399.2, 418.5, 553.2, X1]
g = Grid("organisation", xs, [1910, 4770])
g.put(X0, 105.4, 0, 2, lines_in(60, 76, 229, 260), LABEL, bold=True)
for (a, e), x, num in (((110.5, 245.2), 134.5, "①"), ((264.5, 399.2), 293.1, "②"), ((418.5, 553.2), 436.4, "③")):
    g.put(a, e, 0, 1, [[(num + " ", 1090, True, INK)] + runs_of(line1(x - 1, x + 1, 219, 221))],
          frame("#DADADA", top="mid", left="mid", right="mid"))
    body = lines_in(a, e, 237, 270)
    pars = []
    for ln in body:
        runs = runs_of(ln)
        if ln["text"].startswith("∙"):
            pars.append(runs)
        elif runs[0][2]:      # bold lines follow a ➡ arrow image (the second one is a continuation)
            lead = "→ " if not (pars and pars[-1][0][0] == "→ ") else "    "
            pars.append([(lead, 1000, True, ARR)] + runs)
        else:
            pars.append([("  ", 1090, False, INK)] + runs)
    g.put(a, e, 1, 2, pars, frame(bottom="mid", left="mid", right="mid"), align="LEFT", line=1400)
for a, e in ((245.2, 264.5), (399.2, 418.5)):
    g.put(a, e, 1, 2, "+", size=1500, bold=True, color="#9A9A9A")
block(g, 215.4)

# 투자 및 인력 운영계획 table (vector table in the PDF)
xs = [X0, 105.4, 107.7, 157.3, 209.8, 355.6, 422.2, 488.8, X1]
g = Grid("investment", xs, [1840] + [1560] * 6)
g.put(X0, 105.4, 0, 7, lines_in(60, 66, 324, 355), LABEL, bold=True)
head = frame("#D8D8D8", top="mid", bottom="soft")
g.put(107.7, 209.8, 0, 1, [line1(110, 112, 290, 292)], head, bold=True)
g.put(209.8, 355.6, 0, 1, [line1(258, 261, 290, 292)], head, bold=True)
for a, e, x in ((355.6, 422.2, 364.7), (422.2, 488.8, 431.3), (488.8, X1, 497.9)):
    g.put(a, e, 0, 1, [line1(x - 1, x + 1, 288, 290)], head, bold=True)
for k, y in enumerate((308.8, 340.0, 371.2)):
    r = 1 + 2 * k
    last = k == 2
    g.put(107.7, 157.3, r, r + 2, lines_in(110, 157, y - 1, y + 20), frame("#ECECEC", bottom="mid" if last else "soft"))
    for j, ty in enumerate((y - 0.6, y + 15.0)):
        sub = dict(bottom=("mid" if last else "soft") if j else "soft")
        g.put(157.3, 209.8, r + j, r + j + 1, [line1(160, 169, ty - 1, ty + 1)], frame("#ECECEC", left="soft", **sub))
        for a, e in ((355.6, 422.2), (422.2, 488.8), (488.8, X1)):
            g.put(a, e, r + j, r + j + 1, [line1(a + 1, e, ty - 1, ty + 1)], frame(left="soft", **sub), align="RIGHT")
    first, second = lines_in(212, 222, y - 1, y + 17)
    g.put(209.8, 355.6, r, r + 2, [runs_of(first), [("  ", 1090, False, INK)] + runs_of(second)],
          frame(left="soft", bottom="mid" if last else "soft"), align="LEFT", line=1400)
block(g, 287.5)

g = Grid("arrow-2", [X0, X1], [1100])
g.put(X0, X1, 0, 1, "▼", size=1100, color="#9A9A9A", line=900)
block(g, 401.8)

# 사업 포트폴리오별 매출 목표: three donut charts (image) -> value table; then tagged summary lines.
xs = [X0, 105.4, 110.5, 172.0, 258.9, 320.5, 407.3, 469.0, X1,
      131.5, 279.5, 428.0]
xs = sorted(set(xs))
g = Grid("sales-target", xs, [1600, 1900, 1900, 1900, 1900, 1000, 1800, 2000])
g.put(X0, 105.4, 0, 8, lines_in(58, 72, 459, 512), LABEL, bold=True)
g.put(110.5, 258.9, 0, 1, "단위 : 억원, %", frame(top="soft", left="soft"), size=750, align="LEFT", line=900)
g.put(258.9, X1, 0, 1, [], frame(top="soft", right="soft"))
years = [("’26년 ", "0.9조원", [("미래성장사업", "855억원 (10%)"), ("ICT운영사업", "4,025억원 (45%)"),
                               ("전력계통사업", "3,948억원 (45%)")]),
         ("’30년 ", "1.4조원", [("미래성장사업", "3,247억원 (24%)"), ("ICT운영사업", "5,326억원 (39%)"),
                               ("전력계통사업", "5,079억원 (37%)")]),
         ("’35년 ", "2.0조원", [("미래성장사업", "6,233억원 (31%)"), ("ICT운영사업", "6,861억원 (34%)"),
                               ("전력계통사업", "6,881억원 (35%)")])]
groups = [(110.5, 172.0, 258.9), (258.9, 320.5, 407.3), (407.3, 469.0, X1)]
for k, ((a, b, e), (year, total, rows)) in enumerate(zip(groups, years)):
    lft = dict(left="soft") if k == 0 else {}
    rgt = dict(right="soft") if k == 2 else {}
    g.put(a, e, 1, 2, [[(year, 1000, False, WHITE), (total, 1150, True, WHITE)]],
          frame("#6A6A6A", **lft, **rgt, **({"right": "soft"} if k < 2 else {})), line=1300)
    for j, (name, value) in enumerate(rows):
        future = j == 0
        fill = "#D0D0D0" if future else None
        g.put(a, b, 2 + j, 3 + j, name, frame(fill, bottom="soft", **lft, hatch="#B8B8B8" if future else None),
              size=950, bold=future)
        g.put(b, e, 2 + j, 3 + j, value, frame(fill, bottom="soft", right="soft", hatch="#B8B8B8" if future else None),
              size=1000, bold=future)
g.put(110.5, X1, 5, 6, [], frame(**side))
ln = line1(113, 114, 520, 523)
spans = [s for s in ln["spans"] if s["text"].strip()]
mid = spans[2]["bbox"][0] - 0.5
long_ = line1(409, 411, 520, 523)
tag_styles = {"단기": (WHITE, INK), "중기": ("#D6D6D6", INK), "장기": (TAG, WHITE)}
pieces = [(110.5, 131.5, 258.9, ln, -1e9, first_cut(ln), mid), (258.9, 279.5, 407.3, ln, mid, mid + 18, 1e9),
          (407.3, 428.0, X1, long_, -1e9, first_cut(long_), 1e9)]
for a, t, e, line, x0, cut, x1 in pieces:
    tag_runs = runs_of(line, x0=x0, x1=cut)
    fill, ink = tag_styles[tag_runs[0][0].strip()]
    g.put(a, t, 6, 7, [runs_of(line, ink, x0=x0, x1=cut)],
          frame(fill, top="soft", bottom="soft", right="soft", left="soft"), ratio=78)
    g.put(t, e, 6, 7, [runs_of(line, x0=cut, x1=x1)], frame(right="soft" if e == X1 else None), align="LEFT")
g.put(110.5, X1, 7, 8, [line1(127, 128, 538, 540)], frame(bottom="soft", **side))
block(g, 415.1)

# 나. [성과관리] title (number and badge+title are two PDF lines)
na, title = line1(55, 60, 566, 568), line1(85, 90, 566, 568)
g = Grid("title-na", [X0, 77.6, 131.0, X1], [1700])
g.put(X0, 77.6, 0, 1, [na], align="LEFT", line=1450)
g.put(77.6, 131.0, 0, 1, [runs_of(title, x1=130)], pill)
g.put(131.0, X1, 0, 1, [runs_of(title, x0=130)], align="LEFT", line=1450)
block(g, 565.6)


def tab_runs(line):
    """'Plan 계획' style tab: English word white, Korean word in a lighter shade."""
    return [(t, s, b, WHITE if s > 1000 else "#E6E6E6") for t, s, b, _ in runs_of(line)]


# PDCA: Plan / Do boxes
xs = [X0, 99.8, 114.0, 300.0, 315.0, 357.1, 371.1, X1]
g = Grid("pdca-plan-do", xs, [1880, 1970, 1840, 1850])
tabf = frame("#4A4A4A", top="mid")
headf = frame("#DCDCDC", top="mid")
g.put(X0, 114.0, 0, 1, [tab_runs(line1(63, 64, 593, 595))], tabf)
g.put(114.0, 300.0, 0, 1, [line1(180, 181, 592, 593)], headf)
g.put(315.0, 371.1, 0, 1, [tab_runs(line1(324, 325, 593, 595))], tabf)
g.put(371.1, X1, 0, 1, [line1(437, 438, 592, 593)], headf)
tagf = frame("#E2E2E2", bottom="soft", hatch="#EDEDED")
for r, y in enumerate((612.2, 630.6, 649.0), 1):
    last = r == 3
    edge = dict(bottom="mid" if last else "soft")
    left = line1(62, 67, y - 1, y + 2) if r != 2 else None
    if left is None:      # SWOT tag and its text are two PDF lines
        tag_runs, text_runs = runs_of(line1(66, 67, 631, 632)), runs_of(line1(101, 103, 630, 631))
    else:
        tag_runs, text_runs = runs_of(left, x1=99), runs_of(left, x0=99)
    g.put(X0, 99.8, r, r + 1, [tag_runs], frame("#E2E2E2", left="soft", hatch="#EDEDED", **edge))
    g.put(99.8, 300.0, r, r + 1, [text_runs], frame(right="soft", **edge), align="LEFT")
    right = line1(321, 322, y - 1, y + 1)
    g.put(315.0, 357.1, r, r + 1, [runs_of(right, x1=358)], frame("#E2E2E2", left="soft", hatch="#EDEDED", **edge))
    g.put(357.1, X1, r, r + 1, [runs_of(right, x0=358)], frame(right="soft", **edge), align="LEFT")
g.put(300.0, 315.0, 1, 4, "▶", size=1100, color="#A8A8A8")
block(g, 588.6)

g = Grid("pdca-arrows", [X0, 300.0, 315.0, X1], [1300])
g.put(X0, 300.0, 0, 1, "▲", size=1000, color="#A8A8A8", line=1100)
g.put(315.0, X1, 0, 1, "▼", size=1000, color="#A8A8A8", line=1100)
block(g, 665.6)

# PDCA: Act / Check boxes (superscript counts are small runs, as in the PDF)
xs = [X0, 99.8, 236.0, 300.0, 315.0, 356.1, 375.8, 492.3, X1]
g = Grid("pdca-act-check", xs, [1880, 1970, 1840, 1840, 1850])
g.put(X0, 236.0, 0, 1, [line1(100, 102, 682, 684)], headf)
g.put(236.0, 300.0, 0, 1, [tab_runs(line1(250, 252, 684, 685))], tabf)
g.put(315.0, 492.3, 0, 1, [line1(350, 352, 682, 684)], headf)
g.put(492.3, X1, 0, 1, [tab_runs(line1(500, 502, 684, 685))], tabf)
for r, y in enumerate((701.8, 720.2, 739.7, 758.1), 1):
    edge = dict(bottom="mid" if r == 4 else "soft")
    left = line1(61, 65, y - 1, y + 1)
    g.put(X0, 99.8, r, r + 1, [runs_of(left, x1=99)], frame("#E2E2E2", left="soft", hatch="#EDEDED", **edge))
    g.put(99.8, 300.0, r, r + 1, [runs_of(left, x0=99)], frame(right="soft", **edge), align="LEFT")
    first = line1(320, 321, y - 0.5 if r != 2 else y, y + 1.5)
    t1 = 375.8 if r == 1 else 356.1
    text = runs_of(first, x0=t1 - 2 if r == 1 else 356)
    if r == 3:            # the 대외소통 line is split into four PDF lines around its superscripts
        for x in (422.0, 480.7, 539.3):
            text += runs_of(line1(x - 0.5, x + 0.5, 738, 739))
    g.put(315.0, t1, r, r + 1, [runs_of(first, x1=t1 - 2 if r == 1 else 356)],
          frame("#E2E2E2", left="soft", hatch="#EDEDED", **edge))
    g.put(t1, X1, r, r + 1, [text], frame(right="soft", **edge), align="LEFT")
g.put(300.0, 315.0, 1, 5, "◀", size=1100, color="#A8A8A8")
block(g, 679.2)

g = Grid("feedback-bar", [X0, X1], [1850])
g.put(X0, X1, 0, 1, [line1(92, 93, 784, 786)], frame("#CFCFCF", top="mid", bottom="mid"))
block(g, 781.8)


def check_edges():
    """Every inner column edge of a band must be a cell boundary, or its width is undefined."""
    for grid, _ in kit.BLOCKS:
        used = {0, len(grid.xs) - 1}
        for (r, c0), item in grid.items.items():
            used.update((c0, c0 + item[6]))
        for c in range(len(grid.xs)):
            if c not in used:
                print(f"WARN {grid.name}: unused edge x={X0 + grid.xs[c] / 100:.1f}")


check_edges()
kit.finish(target, end=803.0)
