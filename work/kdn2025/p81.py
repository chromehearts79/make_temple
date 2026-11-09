"""Rebuild KDN 2025 report page 81 (second PDF local page 31, printed page 53) as editable HWPX.

Usage: python3 work/kdn2025/p81.py <report2.pdf> <out.hwpx> [--page 31]

창업 및 경제활성화, 평가내용 02 section 3. Built with the shared diagram kit (one flat table per
horizontal band on a grid of PDF x edges). Text comes from the PDF text layer. Images typed here:
the boxed numbers (1 2 3 -> ① ② ③), the circled ① ② inside 사례1, the ➡ arrows (gaps in the text
layer) -> →, the ⊕ joint -> +, the round arrow icons -> ▶ cells, the '지적사항 개선' sticker (hand
icon dropped), the running-head rule and side tab. The 'mycontents 포털사이트' screenshot is a
typeset graphic: its labels (read from a 5x / 10x render) are typed as cells, the QR code becomes
an empty photo cell. The URL is printed 'https://mycontents Kdn.com' (space, not a dot); kept.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kit  # noqa: E402
from kit import Layout, recipe_inputs  # noqa: E402

source, target = recipe_inputs(31, "데이터 협력 기반 대국민 AI 서비스 혁신을 통한 에너지")
L = Layout(top=3100)
kit.setup(source, L)
from kit import *  # noqa: E402,F401,F403  helpers and presets bound to this page

DARK, LABEL = "#6A6A6A", "#E6E6E6"
SIDE = frame("#E6E6E6", top="soft")
HATCH = frame("#EEEEEE", hatch="#DEDEDE")
HATCH_L = frame("#EEEEEE", hatch="#DEDEDE", left="mid")
PILL = frame(WHITE, top="soft", bottom="soft", left="soft", right="soft")
ARROW_SIZE = 1000


def hang(lines, base, extra=None):
    """Bullet lines keep their PDF indent: spaces for the x offset and for the line's own lead."""
    out = []
    for l in lines:
        runs = runs_of(l)
        if extra:
            runs = [(extra(t), *rest) for t, *rest in runs]
        size = runs[0][1] / 100
        raw = "".join(s["text"] for s in l["spans"])
        offset = l["bbox"][0] - base + (len(raw) - len(raw.lstrip(" "))) * 0.29 * size
        n = max(0, round(offset / (0.29 * size)))
        out.append([(" " * n, runs[0][1], False, INK)] + runs if n else runs)
    return out


def tight(g, x0, r0, left=60, right=60):
    """Narrow the cell padding (kit cells use the builder default 320/180)."""
    c0 = g.xs.index(to_x(x0))
    item = g.items[r0, c0]
    g.items[r0, c0] = (*item[:7], dict(left=left, right=right))


def lead(glyph, runs, bold=True):
    runs = list(runs)
    return [(glyph + " ", runs[0][1], bold, INK)] + runs


def join(*parts, size=1090):
    """Runs of several PDF lines on one visual line, with typed glyphs (images) between them."""
    out = []
    for part in parts:
        out += [(part, size, False, INK)] if isinstance(part, str) else runs_of(part)
    return out


# ---------------------------------------------------------------------------
# Page chrome (odd page): running head over a rule, side tab, footer at the right.
# ---------------------------------------------------------------------------
L.add_table([[cell(0, 3350, 1680, [para([("01", 1380, True, WHITE)], "CENTER")[0]], dark)],
             [cell(0, 3350, 5960, [para([(ch, 950, True, INK)], "CENTER", 1160)[0] for ch in "경영관리"], gray2)]],
            floating=(57800, 15000))
foot = [(only_text, size, False, INK) for only_text, size in (
    (line1(450, 455, 818, 822)["text"], 790), ("    ", 790), (line1(540, 552, 816, 820)["text"], 1090))]
L.add_table([[cell(0, W, 1500, [para(foot, "RIGHT", 1300)[0]])]], floating=(5660, 81550))

g = Grid("head", [X0, 390.0, X1], [1680])
g.put(X0, 390.0, 0, 1, [], frame(bottom="soft"))
g.put(390.0, X1, 0, 1, [line1(390, 400, 35, 40)], align="RIGHT")
block(g, 32.0)

g = Grid("sec3", [X0, 84.5, X1], [2300])
g.put(X0, 84.5, 0, 1, [runs_of(line1(60, 70, 72, 78), WHITE)], frame(DARK), line=1700)
g.put(84.5, X1, 0, 1, [line1(90, 95, 73, 78)], frame(LABEL), align="LEFT", line=1700)
block(g, 70.9)

# ---------------------------------------------------------------------------
# 가. AI 기반 원자재 가격 예측 서비스
# ---------------------------------------------------------------------------
g = Grid("title-ga", [X0, X1], [1650])
g.put(X0, X1, 0, 1, [line1(55, 60, 98, 104)], align="LEFT", line=1450)
block(g, 97.5)

g = Grid("background", [X0, 107.9, 110.5, 326.0, 340.1, X1], [3410])
g.put(X0, 107.9, 0, 1, [line1(60, 65, 131, 137)], SIDE, bold=True)
g.put(110.5, 326.0, 0, 1, lines_in(140, 145, 123, 143), frame("#DEDEDE"), line=1430)
g.put(326.0, 340.1, 0, 1, "+", size=1500, bold=True, color="#9A9A9A", fit=False)
g.put(340.1, X1, 0, 1, lines_in(355, 372, 123, 143), frame("#DEDEDE"), line=1430)
block(g, 121.2)

xs = [X0, 107.9, 110.5, 255.1, 259.0, 272.3, 405.3, 408.5, 422.6, X1]
g = Grid("work", xs, [1870, 5300])
g.put(X0, 107.9, 0, 2, [line1(60, 65, 189, 195)], SIDE, bold=True)
heads = [(110.5, 255.1, 160), (272.3, 405.3, 305), (422.6, X1, 460)]
for k, ((a, e, x), num) in enumerate(zip(heads, "①②③")):
    fill = frame("#D2D2D2" if k == 2 else "#E6E6E6", top="mid")
    g.put(a, e, 0, 1, [lead(num, runs_of(line1(x, x + 5, 161, 166)))], fill)
for a, e in ((255.1, 272.3), (405.3, 422.6)):
    g.put(a, e, 0, 1, "▶", frame(top="mid"), size=900, color="#9A9A9A")
for k, (a, e, x) in enumerate(((110.5, 259.0, 113.6), (259.0, 408.5, 263.1), (408.5, X1, 412.6))):
    g.put(a, e, 1, 2, hang(lines_in(a, e, 182, 220), x),
          frame(left="dot" if k else None, bottom="mid"), align="LEFT", line=1540)
block(g, 159.3)

g = Grid("effect", [X0, 107.9, 110.5, X1], [3640])
g.put(X0, 107.9, 0, 1, [line1(60, 65, 249, 255)], SIDE, bold=True)
row1 = join(line1(116, 120, 240, 245), " → ", line1(240, 245, 240, 245))
row2 = join(line1(116, 120, 256, 260), " → ", line1(255, 260, 256, 260), " → ", line1(380, 385, 256, 260))
g.put(110.5, X1, 0, 1, [row1, row2], frame(top="mid", bottom="mid", left="mid", right="mid"), align="LEFT",
      line=1540)
block(g, 237.3)

# ---------------------------------------------------------------------------
# 나. 사례1 / 사례2 cards
# ---------------------------------------------------------------------------
g = Grid("title-na", [X0, X1], [1650])
g.put(X0, X1, 0, 1, [line1(55, 60, 283, 289)], align="LEFT", line=1450)
block(g, 283.0)

LX = (X0, 91.1, 280.5, 299.3, 304.4)                 # left card: tag | title | badge | edge
RX = (307.8, 341.9, 529.6, 548.3, X1)
FLOW = (62.8, 131.0, 147.0, 214.8, 231.2, 304.4)
QR = (310.4, 322.0, 348.0, 360.0)
PX = (362.5, 365.0, 425.0, 427.5, 488.0, 490.5, 550.5, 552.7)
xs = sorted(set(LX + RX + FLOW + QR + PX + (327.8, 378.3)))
hs = [1450, 420, 1150, 880, 880, 890, 600, 950, 1800, 1450, 1800, 420, 3460, 320]
g = Grid("cases", xs, hs)
for (a, b, c, d, e), y, x in ((LX, 310, 62), (RX, 310, 313)):
    head = line1(x, x + 4, y, y + 3)
    g.put(a, b, 0, 1, [runs_of(head, WHITE, x1=b - 1.0)], frame("#5E5E5E", top="mid", left="mid"))
    g.put(b, c, 0, 1, [strip_runs(runs_of(head, x0=b - 1.0, x1=c))], frame("#DCDCDC", top="mid"), align="LEFT")
    g.put(c, d, 0, 1, [runs_of(head, WHITE, x0=c)], frame("#7F7F7F", top="mid"), line=1000)
    tight(g, c, 0, 20, 20)
    g.put(d, e, 0, 1, [], frame("#DCDCDC", top="mid", right="mid"))
# 사례1 body
c1 = lines_in(62, 72, 332, 368)
body = [runs_of(c1[0]),
        [("  ", 1090, False, INK)] + join(c1[1], " ① ", line1(234, 240, 348, 352)),
        [("  ", 1090, False, INK)] + join(c1[2], " ② ", line1(113, 118, 364, 368))]
g.put(X0, 304.4, 1, 8, body, frame(left="mid", right="mid"), align="LEFT", line=1540)
for k, (a, e) in enumerate(zip(FLOW[::2], FLOW[1::2])):
    last = k == 2
    g.put(a, e, 8, 10, lines_in(a - 1.0, e, 381, 400), frame("#C8C8C8", right="mid") if last else frame("#E2E2E2"),
          bold=True, line=1150)
    if last:
        tight(g, a, 8, 40, 40)
for a, e in ((131.0, 147.0), (214.8, 231.2)):
    g.put(a, e, 8, 10, "▶", size=900, color="#9A9A9A")
g.put(X0, 62.8, 8, 10, [], frame(left="mid"))
g.put(X0, 304.4, 10, 12, [join(line1(62, 66, 417, 421), " + ", line1(136, 140, 417, 421))],
      frame(left="mid", right="mid"), align="LEFT", line=1300)
g.put(X0, 304.4, 12, 13, [lead(n, runs_of(l), False) for n, l in zip("①②", lines_in(74, 76, 438, 458))],
      frame("#EEEEEE", left="mid", right="mid", hatch="#DEDEDE"), align="LEFT", line=1540)
g.put(X0, 304.4, 13, 14, [], frame(left="mid", right="mid", bottom="mid"))
# 사례2 body: typeset 'mycontents' graphic (labels typed), then text-layer bullets
g.put(307.8, 310.4, 1, 7, [], frame(left="mid"))
g.put(552.7, X1, 1, 7, [], frame(right="mid"))
g.put(310.4, 360.0, 1, 3, ["mycontents"], frame("#CFCFCF"), size=720, line=820)
g.put(310.4, 360.0, 3, 4, ["포털사이트"], frame("#CFCFCF"), size=720, line=700)
g.put(310.4, 322.0, 4, 6, [], frame("#CFCFCF"))
g.put(322.0, 348.0, 4, 6, [], photo)
g.put(348.0, 360.0, 4, 6, [], frame("#CFCFCF"))
g.put(310.4, 360.0, 6, 7, [], frame("#CFCFCF"))
g.put(362.5, 552.7, 1, 3, ["https://mycontents Kdn.com"], frame("#CFCFCF", top="soft", left="soft", right="soft"),
      size=720, line=820)
menu = [["소셜로그인", "콘텐츠 구독", "콘텐츠 조회"], ["통계 대시보드", "알림톡/친구톡 발생", "분석보고서"],
        ["요약서비스", "평판분석", "서비스관리"]]
for r, labels in enumerate(menu, 3):
    for (a, e), text in zip(((365.0, 425.0), (427.5, 488.0), (490.5, 550.5)), labels):
        g.put(a, e, r, r + 1, text, frame("#E4E4E4"), size=640, line=640)
    g.put(362.5, 365.0, r, r + 1, [], frame(left="soft"))
    g.put(550.5, 552.7, r, r + 1, [], frame(right="soft"))
g.put(362.5, 552.7, 6, 7, [], frame(left="soft", right="soft", bottom="soft"))
c2 = lines_in(313, 314, 372, 392)
g.put(307.8, X1, 7, 9, hang(c2, 313.4), frame(left="mid", right="mid"), align="LEFT", line=1290)
third = line1(313, 314, 404, 408)
g.put(307.8, 327.8, 9, 10, [hang([third], 313.4)[0][:2]], frame(left="mid"), align="LEFT", line=1200)
g.put(327.8, 378.3, 9, 10, [runs_of(third, x0=327.0, x1=378.0)], PILL, line=1000)
tight(g, 327.8, 9, 20, 20)
g.put(378.3, X1, 9, 10, [strip_runs(runs_of(third, x0=378.0))], frame(right="mid"), align="LEFT", line=1200)
tight(g, 378.3, 9, 60, 180)
g.put(307.8, X1, 10, 12, hang([line1(327, 328, 419, 423)], 313.4), frame(left="mid", right="mid"), align="LEFT",
      line=1300)
g.put(307.8, X1, 12, 13, [lead(n, runs_of(l), False) for n, l in zip("①②", lines_in(325, 326, 438, 458))],
      frame("#EEEEEE", left="mid", right="mid", hatch="#DEDEDE"), align="LEFT", line=1540)
g.put(307.8, X1, 13, 14, [], frame(left="mid", right="mid", bottom="mid"))
block(g, 309.3)

# ---------------------------------------------------------------------------
# 다. 民·官·公 협력체계: 데이터 협업 box and ICT 협업 table
# ---------------------------------------------------------------------------
g = Grid("title-da", [X0, X1], [1650])
g.put(X0, X1, 0, 1, [line1(55, 60, 482, 488)], align="LEFT", line=1450)
block(g, 482.5)


def tag_band(name, line_a, line_b, pill_x, top):
    """'(pill) label' dark band, slanted joint and the bold motto on the right."""
    g = Grid(name, [X0, pill_x[0], pill_x[1], 192.5, 209.4, X1], [1990])
    g.put(X0, pill_x[0], 0, 1, [], frame("#5E5E5E"))
    g.put(pill_x[0], pill_x[1], 0, 1, [runs_of(line_a, x1=pill_x[1] - 3.0)], PILL)
    tight(g, pill_x[0], 0, 20, 20)
    g.put(pill_x[1], 192.5, 0, 1, [strip_runs(runs_of(line_a, WHITE, x0=pill_x[1] - 3.0))], frame("#5E5E5E"))
    tight(g, pill_x[1], 0, 60, 60)
    g.put(192.5, 209.4, 0, 1, [], frame(bottom="mid"))
    g.put(209.4, X1, 0, 1, [line_b], frame(bottom="mid"), align="LEFT")
    block(g, top)


tag_band("collab-tag", line1(69, 70, 508, 512), line1(213, 214, 508, 512), (61.0, 118.1), 505.7)

xs = [X0, 77.9, 130.0, 167.8, 169.9, 194.0, 266.5, 280.0, 289.6, 301.4, 327.0, 419.5, 421.1, 422.1, 433.0,
      442.3, 458.0, 552.6, X1]
hs = [240, 400, 1350, 900, 1350, 1050, 310, 230, 1780, 1380, 1250, 1890, 360]
g = Grid("collab", xs, hs)
g.put(X0, X1, 0, 1, [], frame(left="mid", right="mid"))
g.put(X0, 167.8, 1, 7, [lead("①", runs_of(line1(76, 77, 547, 552)))], HATCH_L, align="LEFT")
g.put(169.9, 266.5, 2, 6, lines_in(170, 265, 540, 560), frame(top="soft", bottom="soft", left="soft", right="soft"),
      line=1400)
g.put(266.5, 280.0, 2, 6, "▶", size=900, color="#9A9A9A")
g.put(280.0, 419.5, 2, 6, hang(lines_in(285, 294, 530, 570), 285.3),
      frame(top="soft", bottom="soft", left="soft", right="soft"), align="LEFT", line=1060)
for r, y in ((2, 533), (4, 555)):
    eff = line1(424, 425, y, y + 3)
    g.put(422.1, 442.3, r, r + 1, [runs_of(eff, x1=441.0)], frame("#D6D6D6"), line=1000)
    tight(g, 422.1, r, 20, 20)
    g.put(442.3, X1, r, r + 1, [strip_runs(runs_of(eff, x0=441.0))], frame(right="mid"), align="LEFT")
    tight(g, 442.3, r, 60, 60)
for r in (1, 3, 5, 6):
    g.put(552.6, X1, r, r + 1, [], frame(right="mid"))
g.put(X0, X1, 7, 8, [], frame(left="mid", right="mid", top="dot"))
g.put(X0, 167.8, 8, 10, [lead("②", runs_of(line1(76, 77, 601, 606)))], HATCH_L, align="LEFT")
g.put(X0, 77.9, 10, 11, [], HATCH_L)
g.put(77.9, 130.0, 10, 11, "지적사항 개선", frame("#3C3C3C"), size=740, bold=True, color=WHITE, line=900)
tight(g, 77.9, 10, 30, 30)
g.put(130.0, 167.8, 10, 11, [], HATCH)
g.put(X0, 167.8, 11, 12, [], HATCH_L)
for a, b, e, x in ((169.9, 194.0, 289.6, 179), (301.4, 327.0, 421.1, 305), (433.0, 458.0, 552.6, 442)):
    g.put(a, b, 8, 9, [runs_of(line1(x, x + 2, 586, 589), WHITE)], frame("#7A7A7A"))
    g.put(b, e, 8, 9, [line1(b, e, 587, 590)], frame(bottom="soft"), align="LEFT")
    lines = lines_in(a, e, 604, 634)
    g.put(a, e, 9, 12, hang(lines, min(l["bbox"][0] for l in lines)), frame("#E5E5E5"), align="LEFT", line=1210)
for a, e in ((289.6, 301.4), (421.1, 433.0)):
    g.put(a, e, 9, 12, "▶", size=900, color="#9A9A9A")
for r in (8, 9, 10, 11):
    g.put(552.6, X1, r, r + 1, [], frame(right="mid"))
g.put(X0, X1, 12, 13, [], frame(left="mid", right="mid", bottom="mid"))
block(g, 525.6)

tag_band("ict-tag", line1(67, 68, 658, 662), line1(213, 214, 658, 662), (61.4, 104.3), 655.8)

g = Grid("ict", [X0, 89.0, 210.3, X1], [1840, 1870, 1870, 1870, 2170])
head_l = line1(76, 77, 680, 684)
g.put(X0, 210.3, 0, 1, [lead("③", runs_of(head_l))], frame("#D8D8D8", top="mid", left="mid", right="soft"),
      align="LEFT")
g.put(210.3, X1, 0, 1, [line1(280, 285, 680, 684)], frame("#D8D8D8", top="mid", right="mid"))
rows = ((699, "①"), (718, "②"), (737, "③"))
for r, (y, num) in enumerate(rows, 1):
    g.put(X0, 210.3, r, r + 1, [lead(num, runs_of(line1(76, 77, y, y + 4)), False)],
          frame("#EDEDED", left="mid", bottom="soft"), align="LEFT")
    g.put(210.3, X1, r, r + 1, hang([line1(213, 214, y - 1, y + 4)], 213.3, lambda t: t.replace("  본 사업", " → 본 사업")),
          frame(right="mid", bottom="soft"), align="LEFT")
res = line1(66, 67, 757, 761)
g.put(X0, 89.0, 4, 5, [runs_of(res, x1=85.0)], frame("#DCDCDC", left="mid", bottom="mid", hatch="#C8C8C8"))
g.put(89.0, X1, 4, 5, [strip_runs(runs_of(res, x0=85.0))], frame(right="mid", bottom="mid"), align="LEFT")
block(g, 678.8)

# ---------------------------------------------------------------------------
# 주요성과
# ---------------------------------------------------------------------------
g = Grid("result", [X0, 111.7, X1], [2100])
g.put(X0, 111.7, 0, 1, [runs_of(line1(65, 70, 784, 789), WHITE)], frame("#6A6A6A", top="mid", bottom="mid", left="mid"))
g.put(111.7, X1, 0, 1, [line1(115, 120, 783, 788)], frame(top="mid", bottom="mid", right="mid"), align="LEFT")
block(g, 780.5)

kit.finish(target, end=803.0)
