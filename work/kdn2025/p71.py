"""Rebuild KDN 2025 report page 71 (second PDF local page 21, printed page 45) as editable HWPX.

Usage: python3 work/kdn2025/p71.py <report2.pdf> <out.hwpx> [--page 21]

친환경·탄소중립 section 2 (온실가스 감축 전략). Built with the shared kit: one flat table per
horizontal band on a grid of PDF x edges; text comes from the PDF text layer except for these
images, read from 3-5x renders and typed: the 감축 로드맵 table body (연도 / 감축률 / 배출량), the two
추진 성과 bar charts (kept as value cells only: labels and values they print, no bars), the
❶❷❸ markers (typed ①②③) and the 'NEW 신규' stickers. The check boxes become ▣, chevrons and
the bracket arrow become ▶ connector cells, the roadmap's dotted links become ▶ too.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kit  # noqa: E402
from kit import Layout, recipe_inputs  # noqa: E402

source, target = recipe_inputs(21, "탄소중립 달성을 위한 온실가스 감축 전략 이행")
L = Layout(top=3100)
kit.setup(source, L)
from kit import *  # noqa: E402,F401,F403  helpers and presets bound to this page

DARK, LABEL, HEAD = "#6A6A6A", "#E6E6E6", "#D9D9D9"
TAG = frame(WHITE, top="soft", bottom="soft", left="soft", right="soft")   # boxed 공공최초 / 전국최초 ...
CONN = "#A0A0A0"


def section_band(name, num_line, title_line, top):
    """'2 | heading' band: dark number cell and light gray title cell (images in the PDF)."""
    g = Grid(name, [X0, 84.5, X1], [2300])
    g.put(X0, 84.5, 0, 1, [runs_of(num_line, WHITE)], frame(DARK), line=1700)
    g.put(84.5, X1, 0, 1, [runs_of(title_line)], frame(LABEL), align="LEFT", line=1700)
    block(g, top)


def heading(name, line, top):
    g = Grid(name, [X0, X1], [1650])
    g.put(X0, X1, 0, 1, [line], align="LEFT", line=1450)
    block(g, top)


def T(text, size=1000, bold=False, color=INK):
    return [(text, size, bold, color)]


TOP = []   # first paragraphs of cells aligned to the top (text that starts on a tag's row)


def put(g, x0, x1, r0, r1, content, fill="1", *, top=False, bare=False, **kw):
    """Grid.put plus: top -> vertical alignment TOP; bare -> zero left/right cell padding."""
    g.put(x0, x1, r0, r1, content, fill, **kw)
    key = (r0, g.xs.index(to_x(x0)))
    if top:
        TOP.append(g.items[key][3][0])
    if bare:
        g.items[key] = (*g.items[key][:7], dict(left=0, right=0))


def sticker():
    """'NEW 신규' sticker (an image in the PDF), typed as a small dark tag."""
    return [[("NEW ", 520, True, WHITE), ("신규", 860, True, WHITE)]]


# ---------------------------------------------------------------------------
# Page chrome (odd page): running head over a rule, side tab, footer at the right.
# ---------------------------------------------------------------------------
L.add_table([[cell(0, 3350, 1680, [para([("01", 1380, True, WHITE)], "CENTER")[0]], dark)],
             [cell(0, 3350, 5960, [para([(ch, 950, True, INK)], "CENTER", 1160)[0] for ch in "경영관리"], gray2)]],
            floating=(57800, 15000))
foot = [(only_text, size, False, INK) for only_text, size in (
    (line1(450, 455, 818, 822)["text"], 790), ("    ", 790), (line1(540, 552, 816, 820)["text"], 1090))]
L.add_table([[cell(0, W, 1500, [para(foot, "RIGHT", 1300)[0]])]], floating=(5660, 81550))

g = Grid("head", [X0, 401.0, X1], [1680])
g.put(X0, 401.0, 0, 1, [], frame(bottom="soft"))
g.put(401.0, X1, 0, 1, [line1(400, 410, 35, 40)], align="RIGHT")
block(g, 32.0)

section_band("sec2", line1(60, 70, 72, 76), line1(90, 95, 73, 77), 70.9)

# ---------------------------------------------------------------------------
# 감축 로드맵 (table body is an image) ▶ 3대 중점 추진 과제 (text layer, ▣ for the check boxes)
# ---------------------------------------------------------------------------
xs = [X0, 100.0, 144.0, 152.0, 197.0, 205.0, 249.0, 257.0, 296.9, 316.0, X1]
g = Grid("roadmap", xs, [1450, 400, 1450, 2200, 2290])
g.put(X0, 296.9, 0, 1, [line1(75, 85, 103, 108)], frame("#D9D9D9", top="mid", left="mid", right="mid"), bold=True)
g.put(X0, 296.9, 1, 2, [], frame(left="mid", right="mid"))
g.put(316.0, X1, 0, 1, [line1(360, 370, 103, 108)], frame("#B8B8B8", top="mid", left="mid", right="mid"))
g.put(316.0, X1, 1, 5, [[("▣ ", 1090, False, INK)] + runs_of(l) for l in lines_in(328, 335, 125, 170)],
      frame(left="mid", right="mid", bottom="mid"), align="LEFT", line=1750)
g.put(296.9, 316.0, 2, 5, "▶", size=1100, color="#BDBDBD", fit=False)
labels = [[T("연  도", 1000)], [T("감축률", 1000), T("(정부권장)", 780)],
          [T("배출량", 1000), [("(tCO", 780, False, INK), ("2", 520, False, INK), ("eq)", 780, False, INK)]]]
cols = ((100.0, 144.0), (152.0, 197.0), (205.0, 249.0), (257.0, 296.9))
years = ("2018", "2025", "2030", "2035")
rates = ([T("기준", 1100)], [T("17.3%", 1050, True), T("(15.2%)", 850)], [T("37.8%", 1050, True), T("(37.4%)", 850)],
         [T("60%", 1050, True, WHITE), T("(53%)", 850, False, WHITE)])
fills = (frame("#DCDCDC"), frame(WHITE, top="soft", bottom="soft", left="soft", right="soft"), frame("#BDBDBD"),
         frame("#5A5A5A"))
emissions = ("6,761", "5,592", "4,205", "2,704")
for r, lab in enumerate(labels, 2):
    g.put(X0, 100.0, r, r + 1, lab, frame("#D9D9D9", left="mid", bottom="mid" if r == 4 else None), line=1000)
for k, ((a, e), year, rate, fill, value) in enumerate(zip(cols, years, rates, fills, emissions)):
    last = k == 3
    g.put(a, e, 2, 3, year, frame(right="mid" if last else None), size=1050, bold=True)
    g.put(a, e, 3, 4, rate, fill, line=1000)
    g.put(a, e, 4, 5, value, frame(bottom="mid", right="mid" if last else None), size=1100, bold=True)
    if not last:
        g.put(e, cols[k + 1][0], 3, 4, "▶", size=700, color=CONN, fit=False)
        g.put(e, cols[k + 1][0], 4, 5, [], frame(bottom="mid"))
block(g, 103.0)

# ---------------------------------------------------------------------------
# 가. 외부 감축 사업 및 재생E 설비: table with 추진 성과 charts (values only) at the right
# ---------------------------------------------------------------------------
heading("title-ga", line1(55, 60, 194, 198), 194.0)

C0 = 470.0
xs = [X0, 122.0, 124.5, 159.1, 224.3, 233.9, 242.3, 301.0, 335.9, 344.3, 357.7, 449.3, 451.0, 454.5, C0,
      487.0, 498.5, 512.8, 527.0, 538.5, X1]
hs = [1450, 390, 260, 1530, 1650, 260, 1950, 1610, 260, 420, 1750, 1700, 1450, 1400, 1380, 1470, 390]
g = Grid("ga", xs, hs)
head = frame(HEAD, top="mid")
g.put(X0, 122.0, 0, 1, [line1(80, 85, 219, 224)], head)
g.put(122.0, 454.5, 0, 1, [line1(265, 270, 219, 224)], head)
g.put(C0, X1, 0, 1, [runs_of(line1(490, 500, 219, 224), WHITE)], frame(DARK, top="mid"))
g.put(X0, 122.0, 2, 9, lines_in(65, 115, 250, 290), frame(LABEL, bottom="soft"))
g.put(X0, 122.0, 10, 17, lines_in(65, 115, 335, 385), frame(LABEL, bottom="soft"))
g.put(122.0, 454.5, 8, 9, [], frame(bottom="soft"))
g.put(122.0, 454.5, 16, 17, [], frame(bottom="soft"))
for r, y in ((3, 241), (4, 258), (10, 320), (11, 337)):
    ln = line1(125, 128, y - 1, y + 2)
    g.put(124.5, 159.1, r, r + 1, [runs_of(ln, x1=158.0)], frame("#D9D9D9"), line=1000)
    g.put(159.1, 454.5, r, r + 1, [strip_runs(runs_of(ln, x0=158.0))], align="LEFT")
for (a, e), fill in (((124.5, 233.9), "#E6E6E6"), ((242.3, 335.9), "#D6D6D6"), ((344.3, 449.3), "#C4C4C4")):
    g.put(a, e, 6, 8, lines_in(a, e, 278, 300), frame(fill), line=1440)
for a, e in ((233.9, 242.3), (335.9, 344.3)):
    g.put(a, e, 6, 8, "▶", size=800, color=CONN, fit=False)
# inner 도입률 table (text layer; ❶❷❸ markers typed as ①②③)
ih = frame("#E3E3E3", top="soft", bottom="soft")
for a, e, x in ((124.5, 224.3, 165), (224.3, 301.0, 233), (301.0, 357.7, 303)):
    g.put(a, e, 12, 13, [line1(x, x + 5, 355, 358)], ih)
g.put(357.7, 451.0, 12, 13, [runs_of(line1(380, 385, 355, 358), WHITE)], frame(DARK, top="mid", left="mid", right="mid"))
for r, (mark, y) in enumerate(zip("①②③", (370, 384, 397)), 13):
    last = r == 15
    row = frame(bottom="soft" if last else "dot")
    g.put(124.5, 224.3, r, r + 1, [[(mark + " ", 990, False, INK)] + runs_of(line1(139, 142, y - 1, y + 2))], row,
          align="LEFT")
    g.put(224.3, 301.0, r, r + 1, [line1(250, 256, y - 1, y + 3)], row)
    g.put(301.0, 357.7, r, r + 1, [line1(312, 316, y - 1, y + 3)], row)
g.put(357.7, 451.0, 13, 16, [line1(380, 386, 376, 380), line1(365, 370, 390, 394)],
      frame(left="mid", right="mid", bottom="mid"), line=1300)
g.put(454.5, C0, 2, 17, "▶", size=1100, color="#BDBDBD", fit=False)
# 추진 성과 column: chart values (images) and captions (text layer)
side_l, side_r = dict(left="mid"), dict(right="mid")
for k, ((a, e), value, year) in enumerate(zip(((C0, 498.5), (498.5, 527.0), (527.0, X1)), ("100세대", "218세대", "400세대"),
                                              ("’23년", "’24년", "’25년"))):
    edges = side_l if k == 0 else side_r if k == 2 else {}
    put(g, a, e, 1, 6, value, frame(**edges), size=850, bold=k == 2, ratio=82, fit=False, bare=True)
    put(g, a, e, 6, 7, year, frame("#E3E3E3", **edges), size=850, bold=k == 2, ratio=86, fit=False, bare=True)
caption = frame("#EDEDED", left="mid", right="mid", bottom="soft", hatch="#E0E0E0")
g.put(C0, X1, 7, 9, [line1(478, 485, 297, 302)], caption)
g.put(C0, X1, 9, 10, [], frame(left="mid", right="mid"))
g.put(C0, 487.0, 10, 11, [], frame(left="mid"))
g.put(487.0, 538.5, 10, 11, [[("24% 증가↑", 850, True, WHITE)]], frame("#3C3C3C"), line=1000)
g.put(538.5, X1, 10, 11, [], frame(right="mid"))
for (a, e), value, year, edges in (((C0, 512.8), "8.72GWh", "’24년", side_l), ((512.8, X1), "10.81GWh", "’25년", side_r)):
    put(g, a, e, 11, 14, value, frame(**edges), size=850, bold=edges is side_r, ratio=86, fit=False, bare=True)
    g.put(a, e, 14, 15, year, frame("#E3E3E3", **edges), size=850, bold=edges is side_r)
g.put(C0, X1, 15, 17, [line1(478, 485, 397, 401)], frame("#EDEDED", left="mid", right="mid", bottom="mid",
                                                         hatch="#E0E0E0"))
block(g, 219.2)

# ---------------------------------------------------------------------------
# 나. 관리 체계 디지털 전환
# ---------------------------------------------------------------------------
heading("title-na", line1(55, 60, 425, 429), 424.8)
xs = [X0, 61.0, 81.5, 88.0, 184.3, 187.3, 226.0, X1]
g = Grid("na", xs, [2000, 600, 1130, 600, 600, 1130, 620, 600, 1130, 600])
g.put(X0, 184.3, 0, 1, [line1(110, 115, 450, 455)], head)
g.put(184.3, X1, 0, 1, [line1(345, 352, 450, 455)], head)
row1, row3 = line1(185, 190, 471, 475), line1(55, 62, 518, 522)
soft, strong = frame(bottom="soft"), frame(bottom="mid")
# rows 1-2: NEW 신규 sticker | name | text; row 1's text starts with a boxed 공공최초 tag, so that
# text cell starts on the tag's (middle) sub-row and is top aligned.
for r, y in ((1, 471), (4, 494)):
    g.put(X0, 61.0, r, r + 3, [], soft)
    g.put(61.0, 88.0, r + 1, r + 2, sticker(), frame("#3C3C3C"), line=950)
    g.put(61.0, 88.0, r + 2, r + 3, [], soft)
    g.put(88.0, 184.3, r, r + 3, [strip_runs(runs_of(line1(85, 90, y, y + 4)))], soft, align="LEFT")
g.put(187.3, 226.0, 2, 3, [runs_of(row1, x1=225.0)], TAG, line=950)
put(g, 226.0, X1, 2, 4, [strip_runs(runs_of(row1, x0=225.0))], soft, align="LEFT", top=True, line=1000)
g.put(184.3, 226.0, 3, 4, [], soft)
g.put(184.3, X1, 4, 7, [strip_runs(runs_of(line1(185, 190, 494, 498)))], soft, align="LEFT")
# row 3: 개선 tag | name | text, one PDF line: all three start on the tag's row
g.put(X0, 61.0, 7, 10, [], strong)
g.put(61.0, 81.5, 8, 9, [runs_of(row3, WHITE, x1=80.0)], frame("#7E7E7E"), line=950)
g.put(61.0, 81.5, 9, 10, [], strong)
put(g, 81.5, 184.3, 8, 10, [strip_runs(runs_of(row3, x0=80.0, x1=185.0))], strong, align="LEFT", top=True, line=1000)
put(g, 184.3, X1, 8, 10, [strip_runs(runs_of(row3, x0=185.0))], strong, align="LEFT", top=True, line=1000)
block(g, 447.0)

g = Grid("na-result", [X0, 111.7, X1], [3140])
g.put(X0, 111.7, 0, 1, [line1(65, 70, 555, 560)], frame("#D5D5D5", top="mid", bottom="mid", left="mid"))
g.put(111.7, X1, 0, 1, lines_in(115, 120, 545, 570), frame(top="mid", bottom="mid", right="mid"), align="LEFT",
      line=1450)
block(g, 546.0)

# ---------------------------------------------------------------------------
# 다. 기술 협력 강화
# ---------------------------------------------------------------------------
heading("title-da", line1(55, 60, 590, 595), 590.0)
side = frame("#EDEDED", top="soft")
g = Grid("da-background", [X0, 113.6, 116.2, X1], [2570])
g.put(X0, 113.6, 0, 1, [line1(65, 70, 620, 624)], side)
g.put(116.2, X1, 0, 1, [line1(145, 150, 618, 622)], frame("#D6D6D6"))
block(g, 612.6)

xs = [X0, 113.6, 119.0, 131.5, 165.0, 258.4, 266.4, 405.8, 413.8, X1]
g = Grid("da-results", xs, [1440, 1440, 1470, 3710])
g.put(X0, 113.6, 0, 4, [line1(65, 70, 681, 685)], side)
top = dict(top="mid")
gray = "#D6D6D6"
first = line1(130, 135, 648, 652)
g.put(119.0, 131.5, 0, 1, [], frame(gray, left="mid", **top))
g.put(131.5, 165.0, 0, 1, [runs_of(first, x1=164.0)], TAG, line=950)
g.put(165.0, 258.4, 0, 1, [strip_runs(runs_of(first, x0=164.0))], frame(gray, right="mid", **top), align="LEFT")
for (a, e), x in (((266.4, 405.8), 290), ((413.8, X1), 420)):
    g.put(a, e, 0, 1, [line1(x, x + 5, 648, 652)], frame(gray, left="mid", right="mid", **top))
for (a, e) in ((119.0, 258.4), (266.4, 405.8), (413.8, X1)):
    g.put(a, e, 1, 2, [line1(a, e, 662, 666)], frame(gray, left="mid", right="mid"))
    g.put(a, e, 2, 3, [line1(a, e, 676, 680)], frame(gray, left="mid", right="mid"))
    g.put(a, e, 3, 4, lines_in(a, e, 694, 715), frame(left="mid", right="mid", bottom="mid"), line=1540)
block(g, 646.5)

g = Grid("da-outcome", [X0, 113.6, 119.0, 122.5, 156.0, X1], [500, 1130, 530])
g.put(X0, 113.6, 0, 3, [line1(65, 70, 741, 745)], side)
out = line1(120, 125, 739, 742)
g.put(119.0, 156.0, 0, 1, [], frame("#F0F0F0"))
g.put(119.0, 122.5, 1, 3, [], frame("#F0F0F0"))
g.put(122.5, 156.0, 1, 2, [runs_of(out, x1=155.0)], TAG, line=950)
g.put(122.5, 156.0, 2, 3, [], frame("#F0F0F0"))
g.put(156.0, X1, 0, 1, [], frame("#F0F0F0"))
put(g, 156.0, X1, 1, 3, [strip_runs(runs_of(out, x0=155.0))], frame("#F0F0F0"), align="LEFT", top=True, line=1000)
block(g, 737.0)

# ---------------------------------------------------------------------------
# 주요성과 (text layer; superscripts as small runs)
# ---------------------------------------------------------------------------
g = Grid("result", [X0, 111.7, X1], [3140])
g.put(X0, 111.7, 0, 1, [runs_of(line1(65, 70, 776, 780), WHITE)], frame(DARK, top="mid", bottom="mid", left="mid"))
g.put(111.7, X1, 0, 1, lines_in(115, 120, 767, 790), frame(top="mid", bottom="mid", right="mid"), align="LEFT",
      line=1450)
block(g, 768.0)

kit.flush(803.0)
for sub in L.section.iter(L.q("hp:subList")):
    if len(sub) and any(sub[0] is first for first in TOP):
        sub.set("vertAlign", "TOP")
for number, table in enumerate(L.section.iter(L.q("hp:tbl")), 5001):
    table.set("id", str(number))
for message in WARN:
    print("WARN", message)
print(L.write(target))
