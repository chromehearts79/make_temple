"""Rebuild KDN 2025 report page 83 (second PDF local page 33, printed page 55) as editable HWPX.

Usage: python3 work/kdn2025/p83.py <report2.pdf> <out.hwpx> [--page 33]

창업 및 경제활성화, 평가내용 03 sections 3 and 4 (기술마켓 지원 체계 / 기술마켓 활성화). Built with
the shared diagram kit (one flat table per horizontal band on a grid of PDF x edges). All text
comes from the PDF text layer. Images typed here: the 'NEW 신규' and '지적사항 개선' stickers
(dark tags; the hand icon is dropped), the ➡ arrow in '기존 10억원 ➡ 확대 100억원' (a gap in the
text layer) -> →, the small chevrons under the 주요사례 cards -> ▼, the running-head rule and side
tab. The tiny ▲ tips of the dotted column dividers are omitted. Kept as printed: '(주)쿤O'.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kit  # noqa: E402
from kit import Layout, recipe_inputs  # noqa: E402

source, target = recipe_inputs(33, "‘전담조직’ 및 ‘지원 인프라’ 구성을 통한 상시 기술마켓 지원 체계 구축")
L = Layout(top=3100)
kit.setup(source, L)
from kit import *  # noqa: E402,F401,F403  helpers and presets bound to this page

DARK, LABEL = "#6A6A6A", "#E6E6E6"
SIDE = frame("#DADADA")                     # row labels (추진배경, 추진내용 ...)
BAND = frame("#D3D3D3")                     # 추진배경 statement band
HEADS = "#E9E9E9"                           # light column heads
TAG = frame("#BDBDBD")
MID = 331.7                                 # dotted divider between the two columns


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


def section_band(name, num_line, title_line, top):
    g = Grid(name, [X0, 84.5, X1], [2300])
    g.put(X0, 84.5, 0, 1, [runs_of(num_line, WHITE)], frame(DARK), line=1700)
    g.put(84.5, X1, 0, 1, [title_line], frame(LABEL), align="LEFT", line=1700)
    block(g, top)


def titled(name, line, top, sticker=None, x=None):
    """'가. title' (14pt) with an optional dark sticker (an image in the PDF)."""
    g = Grid(name, [X0, x, X1] if sticker else [X0, X1], [1650])
    g.put(X0, x if sticker else X1, 0, 1, [line], align="LEFT", line=1450)
    if sticker:
        g.put(x, X1, 0, 1, [[(w, s, True, WHITE) for w, s in sticker]], frame("#3C3C3C"), line=1000)
        tight(g, x, 0, 30, 30)
    block(g, top)


def background(name, label_line, text_line, top):
    g = Grid(name, [X0, 102.7, 107.6, X1], [2330])
    g.put(X0, 102.7, 0, 1, [label_line], SIDE, bold=True)
    tight(g, X0, 0, 40, 40)
    g.put(107.6, X1, 0, 1, [text_line], BAND)
    block(g, top)


def label(g, line, rows):
    g.put(X0, 102.7, 0, rows, [line], SIDE, bold=True)
    tight(g, X0, 0, 40, 40)


def tag_rows(g, tags):
    """Rows of 'tag | text' pairs; tags: (r, tag x0, tag x1, column end, tag line, x split, fill, color)."""
    for r, t0, t1, e, line, split, fill, color in tags:
        g.put(t0, t1, r, r + 1, [runs_of(line, color, x1=split)], fill, line=1000)
        tight(g, t0, r, 20, 20)
        g.put(t1, e, r, r + 1, [strip_runs(runs_of(line, x0=split))], align="LEFT")
        tight(g, t1, r, 80, 40)


def results(name, label_line, tags, top, hs):
    """추진실적: label | light box with two dark tag + text rows."""
    g = Grid(name, [X0, 102.7, 110.5, 113.3, 156.3, X1], hs)
    label(g, label_line, len(hs))
    box = "#F0F0F0"
    g.put(110.5, X1, 0, 1, [], frame(box, top="mid", left="mid", right="mid"))
    for r, (tag, text) in enumerate(tags, 1):
        g.put(110.5, 113.3, r, r + 1, [], frame(box, left="mid"))
        g.put(113.3, 156.3, r, r + 1, [runs_of(tag, WHITE)], frame("#7A7A7A"), line=1000)
        tight(g, 113.3, r, 20, 20)
        g.put(156.3, X1, r, r + 1, [text], frame(box, right="mid"), align="LEFT", line=1200)
        tight(g, 156.3, r, 60, 60)
    g.put(110.5, X1, len(hs) - 1, len(hs), [], frame(box, left="mid", right="mid", bottom="mid"))
    block(g, top)


def outcome(name, label_line, lines, top, height, line=1540):
    g = Grid(name, [X0, 111.7, X1], [height])
    g.put(X0, 111.7, 0, 1, [runs_of(label_line, WHITE)], frame("#6A6A6A", top="mid", bottom="mid", left="mid"))
    g.put(111.7, X1, 0, 1, lines, frame(top="mid", bottom="mid", right="mid"), align="LEFT", line=line)
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

g = Grid("head", [X0, 390.0, X1], [1680])
g.put(X0, 390.0, 0, 1, [], frame(bottom="soft"))
g.put(390.0, X1, 0, 1, [line1(390, 400, 35, 40)], align="RIGHT")
block(g, 32.0)

# ---------------------------------------------------------------------------
# 3. 전담조직 및 지원 인프라
# ---------------------------------------------------------------------------
section_band("sec3", line1(60, 70, 72, 78), line1(90, 95, 73, 78), 70.9)
titled("title-3ga", line1(55, 60, 98, 104), 97.5)
background("bg-3ga", line1(62, 63, 125, 130), line1(160, 170, 125, 130), 121.2)

xs = [X0, 102.7, 107.6, 113.5, 151.8, MID, 336.1, 374.3, X1]
g = Grid("work-3ga", xs, [280, 1390, 560, 1500, 1350, 1600, 760])
label(g, line1(62, 63, 176, 181), 7)
g.put(107.6, X1, 0, 1, [], frame(top="soft"))
g.put(107.6, MID, 1, 2, [line1(150, 155, 148, 153)], frame(HEADS), line=1200)
g.put(MID, X1, 1, 2, [line1(365, 366, 148, 153)], frame(HEADS, left="dot"), line=1200)
g.put(MID, X1, 2, 3, [], frame(left="dot"))
tag_rows(g, [(3, 113.5, 151.8, MID, line1(117, 118, 170, 174), 150.0, TAG, INK),
             (5, 113.5, 151.8, MID, line1(117, 118, 199, 203), 150.0, TAG, INK)])
for r, y in ((3, 170), (5, 199)):
    line = line1(340, 342, y, y + 4)
    g.put(MID, 336.1, r, r + 1, [], frame(left="dot"))
    g.put(336.1, 374.3, r, r + 1, [runs_of(line, x1=372.0)], TAG, line=1000)
    tight(g, 336.1, r, 20, 20)
    g.put(374.3, X1, r, r + 1, [strip_runs(runs_of(line, x0=372.0))], align="LEFT")
    tight(g, 374.3, r, 80, 40)
g.put(151.8, MID, 4, 5, [line1(153, 155, 186, 190)], align="LEFT", line=1030)
tight(g, 151.8, 4, 80, 40)
g.put(MID, 374.3, 4, 5, [], frame(left="dot"))
g.put(374.3, X1, 4, 5, [line1(376, 378, 186, 190)], align="LEFT", line=1030)
tight(g, 374.3, 4, 80, 40)
g.put(107.6, MID, 6, 7, [], frame(bottom="soft"))
g.put(MID, X1, 6, 7, [], frame(left="dot", bottom="soft"))
block(g, 146.7)

# 나. 사내 기술마켓 홈페이지
titled("title-3na", line1(55, 60, 230, 236), 229.5, [("NEW ", 560), ("신규", 880)], 517.0)
background("bg-3na", line1(62, 63, 256, 262), line1(160, 170, 256, 262), 252.9)

g = Grid("work-3na", [X0, 102.7, 107.6, MID, X1], [290, 1380, 340, 3800])
label(g, line1(62, 63, 298, 303), 4)
g.put(107.6, X1, 0, 1, [], frame(top="soft"))
g.put(107.6, MID, 1, 2, [line1(140, 145, 280, 285)], frame(HEADS), line=1200)
g.put(MID, X1, 1, 2, [line1(386, 387, 280, 285)], frame(HEADS, left="dot"), line=1200)
g.put(107.6, MID, 2, 3, [], frame())
g.put(MID, X1, 2, 3, [], frame(left="dot"))
g.put(107.6, MID, 3, 4, lines_in(110, MID, 299, 320), frame(bottom="soft"), line=1400)
g.put(MID, X1, 3, 4, lines_in(MID, X1, 299, 320), frame(left="dot", bottom="soft"), line=1400)
block(g, 278.4)

results("done-3na", line1(62, 63, 347, 352), [(line1(120, 122, 341, 345), line1(158, 159, 340, 344)),
                                              (line1(119, 120, 357, 361), line1(158, 159, 356, 360))],
        336.5, [280, 1560, 1560, 340])

outcome("result-3", line1(65, 70, 391, 396), lines_in(115, 120, 384, 404), 381.4, 3460)

# ---------------------------------------------------------------------------
# 4. 등록과 구매, 수요와 공급 매칭
# ---------------------------------------------------------------------------
section_band("sec4", line1(60, 70, 435, 440), line1(90, 95, 436, 441), 433.4)
titled("title-4ga", line1(55, 60, 461, 466), 460.1, [("지적사항 개선", 760)], 503.5)
background("bg-4ga", line1(62, 63, 488, 493), line1(155, 160, 488, 493), 483.7)

g = Grid("work-4ga", [X0, 102.7, 107.6, MID, X1], [280, 1400, 2210])
label(g, line1(62, 63, 521, 526), 3)
g.put(107.6, X1, 0, 1, [], frame(top="soft"))
g.put(107.6, MID, 1, 2, [line1(130, 132, 511, 515)], frame(HEADS), line=1200)
g.put(MID, X1, 1, 2, [line1(342, 343, 511, 515)], frame(HEADS, left="dot"), line=1200)
g.put(107.6, MID, 2, 3, [line1(138, 139, 529, 533)], frame(bottom="soft"))
g.put(MID, X1, 2, 3, [line1(388, 389, 529, 533)], frame(left="dot", bottom="soft"))
block(g, 509.2)

xs = [X0, 102.7, 107.6, 110.5, 139.1, 149.0, 330.1, MID, 333.7, 336.8, 355.1, 375.1, 383.9, X1]
g = Grid("cases-4ga", xs, [290, 1290, 650, 1650, 1700, 660, 1740])
label(g, line1(62, 63, 582, 587), 7)
for a, p0, p1, e, x in ((107.6, 110.5, 139.1, MID, 114), (MID, 355.1, 383.9, X1, 359)):
    head = line1(x, x + 2, 552, 556)
    split = p1 - 3.0
    g.put(a, p0, 1, 2, [], frame(HEADS, left="dot" if a == MID else None))
    g.put(p0, p1, 1, 2, [runs_of(head, x1=split)], frame(WHITE, top="soft", bottom="soft", left="soft", right="soft"),
          line=1000)
    tight(g, p0, 1, 20, 20)
    g.put(p1, e, 1, 2, [strip_runs(runs_of(head, x0=split))], frame(HEADS), align="LEFT", line=1100)
    tight(g, p1, 1, 60, 40)
g.put(107.6, X1, 0, 1, [], frame(top="soft"))
g.put(107.6, MID, 2, 3, [], frame())
g.put(MID, X1, 2, 3, [], frame(left="dot"))
g.put(107.6, MID, 5, 6, "▼", size=600, color=ARROW, line=480)
g.put(MID, X1, 5, 6, "▼", frame(left="dot"), size=600, color=ARROW, line=480)
for r, y in ((3, 574), (4, 591)):
    left = line1(117, 118, y, y + 4)
    g.put(110.5, 149.0, r, r + 1, [left], TAG, line=1000)
    tight(g, 110.5, r, 20, 20)
    g.put(149.0, MID, r, r + 1, [line1(151, 152, y, y + 4)], align="LEFT")
    tight(g, 149.0, r, 60, 40)
    right = line1(340, 341, y, y + 4)
    g.put(MID, 336.8, r, r + 1, [], frame(left="dot"))
    g.put(336.8, 375.1, r, r + 1, [runs_of(right, x1=374.0)], TAG, line=1000)
    tight(g, 336.8, r, 20, 20)
    g.put(375.1, X1, r, r + 1, [strip_runs(runs_of(right, x0=374.0))], align="LEFT")
    tight(g, 375.1, r, 60, 20)
g.put(107.6, 330.1, 6, 7, [line1(115, 116, 612, 617)], frame("#D6D6D6", bottom="soft"))
g.put(330.1, 333.7, 6, 7, [], frame(bottom="soft"))
g.put(333.7, X1, 6, 7, [line1(336, 337, 612, 617)], frame("#D6D6D6", bottom="soft"))
block(g, 550.2)

# 나. 정책금융 우대 프로그램 / 대내·외 홍보
titled("title-4na", line1(55, 60, 639, 644), 638.6)
background("bg-4na", line1(62, 63, 666, 671), line1(175, 180, 666, 671), 661.8)

g = Grid("work-4na", [X0, 102.7, 107.6, MID, X1], [290, 1380, 5490])
label(g, line1(62, 63, 715, 720), 3)
g.put(107.6, X1, 0, 1, [], frame(top="soft"))
g.put(107.6, MID, 1, 2, [line1(170, 171, 689, 694)], frame(HEADS), line=1200)
g.put(MID, X1, 1, 2, [line1(395, 396, 689, 694)], frame(HEADS, left="dot"), line=1200)
g.put(107.6, MID, 2, 3, hang(lines_in(110, 120, 707, 745), 113.5, lambda t: t.replace("10억원  확대", "10억원 → 확대")),
      frame(bottom="soft"), align="LEFT", line=1540)
g.put(MID, X1, 2, 3, hang(lines_in(335, 340, 707, 745), 336.1), frame(left="dot", bottom="soft"), align="LEFT",
      line=1540)
block(g, 687.3)

outcome("result-4", line1(65, 70, 776, 781), lines_in(115, 120, 767, 787), 766.2, 3460, line=1400)

kit.finish(target, end=803.0)
