"""Rebuild KDN 2025 report physical PDF page 39 (printed page 24) as editable HWPX.

Usage: python3 work/kdn2025/p39.py <report.pdf> <out.hwpx> [--page N]

윤리경영 ④-⑤: 공정하고 투명한 기관 운영 (통제활동-③ ④) and 디지털 상시 모니터링 / 쇄신 환류.
All body text is in the PDF text layer; it is placed cell by cell with the shared kit (one flat
table per band on a union grid of PDF x edges, see kit.py / p19.py). Only the section number
bands, the side tab, the 신규 badge and the chevrons are images; they are typed as cells / glyphs.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kit  # noqa: E402
from kit import Layout, recipe_inputs  # noqa: E402

source, target = recipe_inputs(39, "대국민 신뢰도 향상을 위한 공정하고 투명한 기관 운영")
L = Layout(top=3100)
kit.setup(source, L)
from kit import *  # noqa: E402,F401,F403  helpers and presets bound to this page

GRAYL = "#E9E9E9"
soft = "soft"
box = dict(top=soft, bottom=soft, left=soft, right=soft)
tag = frame(WHITE, **box)            # outlined '통제활동-N' tags


def margin(g, x0, r0, **pad):
    """Override the padding of the cell whose top-left slot is (r0, x0)."""
    c0 = g.xs.index(kit.to_x(x0))
    g.items[r0, c0] = g.items[r0, c0][:7] + (pad,)


def run(text, size=1090, bold=False, color=INK):
    return (text, size, bold, color)


def bullets(found):
    """Bullet lines as they are; '- ' lines and continuation lines indented like the source
    (leading blanks are stripped from PDF lines, so the indent is rebuilt from the x offset)."""
    xb = min(l["bbox"][0] for l in found)
    out = []
    for l in found:
        if l["text"].startswith("∙"):
            out.append(l)
            continue
        n = 2 if l["text"].startswith("-") else max(2, round((l["bbox"][0] - xb) / 3.2))
        out.append([run(" " * n)] + runs_of(l))
    return out


def section_band(name, y, top, split=85.0):
    """'N | title' band: dark number box and a light gray title strip (image in the PDF)."""
    g = Grid(name, [X0, split, X1], [2300])
    g.put(X0, split, 0, 1, [line1(60, 80, y - 2, y + 2)], frame("#5E5E5E"), color=WHITE, line=1800)
    g.put(split, X1, 0, 1, [line1(88, 95, y - 1, y + 3)], frame("#E4E4E4"), align="LEFT", line=1700)
    block(g, top)


def number_cell(g, x0, x1, runs):
    g.put(x0, x1, 0, 1, [strip_runs(runs)], align="LEFT", line=1450, fit=False)
    margin(g, x0, 0, left=0, right=0)


# ---------------------------------------------------------------------------
# Page chrome: side tab, footer, running head (odd page, as p19)
# ---------------------------------------------------------------------------
L.add_table([[cell(0, 3350, 1680, [para([("01", 1380, True, WHITE)], "CENTER")[0]], dark)],
             [cell(0, 3350, 5960, [para([(ch, 950, True, INK)], "CENTER", 1160)[0] for ch in "경영관리"], gray2)]],
            floating=(57800, 15000))
foot = [(only_text, size, False, INK) for only_text, size in (
    (line1(450, 455, 818, 822)["text"], 790), ("    ", 790), (line1(540, 552, 816, 820)["text"], 1090))]
L.add_table([[cell(0, W, 1500, [para(foot, "RIGHT", 1300)[0]])]], floating=(5660, 81550))

g = Grid("head", [X0, 466.3, X1], [1680])
g.put(X0, 466.3, 0, 1, [], frame(bottom=soft))
g.put(466.3, X1, 0, 1, [line1(465, 480, 35, 40)], align="RIGHT")
block(g, 32.0)

section_band("section-4", 74.0, 70.9)

# ---------------------------------------------------------------------------
# 가. 회계 신뢰성 [통제활동-③]
# ---------------------------------------------------------------------------
head_a, head_b = line1(55, 60, 100, 104), line1(140, 150, 100, 104)
g = Grid("title-ga", [X0, 76.5, 143.5, 463.5, 521.0, X1], [1650])
number_cell(g, X0, 76.5, runs_of(head_a)[:1])
g.put(76.5, 143.5, 0, 1, [runs_of(head_a)[1]], pill)
g.put(143.5, 463.5, 0, 1, [runs_of(head_b, x1=464)], align="LEFT", line=1450)
g.put(463.5, 521.0, 0, 1, [runs_of(head_b, x0=464)], tag, line=1100)
block(g, 100.0)

xs = [X0, 95.0, 161.5, 190.0, 220.6, 224.3, 262.5, 388.3, 392.0, 430.2, X1]
g = Grid("controls", xs, [2260, 7190, 2990])
hatched = frame("#EFEFEF", hatch="#DADADA")
cols = [((X0, 95.0, 220.6), 58, 95), ((224.3, 262.5, 388.3), 226, 263), ((392.0, 430.2, X1), 394, 431)]
for (a, b, e), tx, hx in cols:
    g.put(a, b, 0, 1, [line1(tx, tx + 6, 128, 131)], frame("#D3D3D3", top="mid"), bold=True)
    title = [line1(hx, hx + 4, 127, 130)]
    if a == X0:
        g.put(b, 161.5, 0, 1, title, frame(top="mid"), align="LEFT")
        g.put(161.5, 190.0, 0, 1, "신규", frame("#3A3A3A", top="mid"), size=800, bold=True, color=WHITE,
              line=950)   # NEW badge image
        g.put(190.0, e, 0, 1, [], frame(top="mid"))
    else:
        g.put(b, e, 0, 1, title, frame(top="mid"), align="LEFT")
    g.put(a, e, 1, 2, bullets(lines_in(a, e, 150, 215)), hatched, align="LEFT", line=1540)
    g.put(a, e, 2, 3, [[run("▼", 700, color="#B5B5B5")], line1(a + 20, e, 228, 231)], frame("#E0E0E0"),
          bold=True, line=1100)
block(g, 122.8)

# ---------------------------------------------------------------------------
# 나. 기관운영 투명성 [통제활동-④]: 구분 | 개선사항 | › | 추진성과
# ---------------------------------------------------------------------------
head = line1(55, 60, 264, 267)
runs = runs_of(head, x1=498)
g = Grid("title-na", [X0, 76.5, 159.8, 496.0, X1], [1650])
number_cell(g, X0, 76.5, runs[:1])
g.put(76.5, 159.8, 0, 1, [runs[1]], pill)
g.put(159.8, 496.0, 0, 1, [strip_runs(runs[2:])], align="LEFT", line=1450)
g.put(496.0, X1, 0, 1, [runs_of(head, x0=498)], tag, line=1100)
block(g, 263.4)

g = Grid("transparency", [X0, 102.2, 353.0, 369.0, X1], [1900, 6800, 7070, 5730])
thead = frame("#DADADA", top="mid", bottom=soft)
g.put(X0, 102.2, 0, 1, [line1(68, 72, 289, 292)], thead, bold=True)
g.put(102.2, 353.0, 0, 1, [line1(205, 212, 289, 292)], thead, bold=True)
g.put(369.0, X1, 0, 1, [line1(440, 448, 289, 292)], frame("#6E6E6E", top="strong", left="strong", right="strong"),
      color=WHITE, bold=True)
rows = [(1, 305, 372), (2, 373, 443), (3, 444, 500)]
for r, y0, y1 in rows:
    last = r == 3
    g.put(X0, 102.2, r, r + 1, lines_in(58, 100, y0, y1), frame("#EDEDED", bottom=soft), line=1430)
    g.put(102.2, 353.0, r, r + 1, bullets(lines_in(104, 108, y0, y1)), frame(bottom=soft), align="LEFT", line=1520)
    g.put(369.0, X1, r, r + 1, bullets(lines_in(371, 383, y0, y1)),
          frame(left="strong", right="strong", bottom="strong" if last else soft), align="LEFT", line=1520)
g.put(353.0, 369.0, 1, 4, "▶", size=1000, color=ARROW, fit=False)
block(g, 285.8)

# ---------------------------------------------------------------------------
# 5. 디지털 상시 모니터링 / 결과 환류
# ---------------------------------------------------------------------------
section_band("section-5", 527.4, 524.4)

xs = [X0, 59.5, 71.5, 108.2, 115.5, 304.8, 307.5, 310.3, 353.5, 359.1, X1]
g = Grid("monitoring", xs, [1900, 8380, 10160])
band = "#DCDCDC"
for (a, c0, c1, e, split, x) in ((X0, 71.5, 115.5, 304.8, 112, 78), (307.5, 310.3, 353.5, X1, 350, 315)):
    line = line1(x - 1, x + 1, 557, 560)
    g.put(a, c0, 0, 1, [], frame(band, top=soft, left=soft))
    g.put(c0, c1, 0, 1, [runs_of(line, WHITE, x1=split)], frame("#707070", top=soft), line=1050)
    margin(g, c0, 0, left=0, right=0)
    g.put(c1, e, 0, 1, [runs_of(line, x0=split)], frame(band, top=soft, right=soft), align="LEFT")
label = frame("#E6E6E6", hatch="#D4D4D4")
# Left panel: 데이터 기반 리스크 상시 추적 / AI 지능형 감사 및 비위 정밀 타격
g.put(X0, 59.5, 1, 3, [], frame(left=soft, bottom=soft))
g.put(59.5, 108.2, 1, 2, lines_in(60, 108, 585, 650), label, line=1440)
g.put(59.5, 108.2, 2, 3, lines_in(60, 108, 670, 745), frame("#E6E6E6", hatch="#D4D4D4", bottom=soft), line=1440)
g.put(108.2, 304.8, 1, 2, bullets(lines_in(110, 130, 575, 655)), frame(right=soft, bottom="dot"), align="LEFT",
      line=1540)
g.put(108.2, 304.8, 2, 3, bullets(lines_in(110, 130, 658, 755)), frame(right=soft, bottom=soft), align="LEFT",
      line=1540)
# Right panel: 청렴도 진단 및 부패 취약점 분석 / 부패실태 근절 및 고강도 쇄신 환류
g.put(307.5, 310.3, 1, 3, [], frame(left=soft, bottom=soft))
g.put(310.3, 359.1, 1, 2, lines_in(310, 360, 578, 655), label, line=1440)
g.put(310.3, 359.1, 2, 3, lines_in(310, 360, 675, 740), frame("#E6E6E6", hatch="#D4D4D4", bottom=soft), line=1440)
g.put(359.1, X1, 1, 2, bullets(lines_in(360, 372, 575, 655)), frame(right=soft, bottom="dot"), align="LEFT",
      line=1540)
g.put(359.1, X1, 2, 3, bullets(lines_in(360, 372, 658, 755)), frame(right=soft, bottom=soft), align="LEFT",
      line=1540)
block(g, 553.8)

g = Grid("results", [X0, 113.0, X1], [3680])
g.put(X0, 113.0, 0, 1, [line1(64, 68, 776, 779)], frame("#6E6E6E", top="mid", bottom="mid", left="mid"),
      color=WHITE, bold=True)
g.put(113.0, X1, 0, 1, lines_in(115, 120, 766, 790), frame(top="mid", bottom="mid", right="mid"), align="LEFT",
      line=1550)
block(g, 765.0)

kit.finish(target, end=801.8)
