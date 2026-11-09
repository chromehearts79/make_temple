"""Rebuild KDN 2025 report page 94 (PDF 2 local page 44, printed page 64) as editable HWPX.

Usage: python3 work/kdn2025/p94.py <report2.pdf> <out.hwpx> [--page 44]

상생·협력 및 지역발전, sections 2 (취약계층 배움 기회 / IT움·IT ON·IT We로) and 3 (전통시장·
소상공인). Built with the shared diagram kit (one flat table per horizontal band on a grid of
PDF x edges); every text line comes from the PDF text layer. Images: the PART box, section number
bands, rounded frames and the two photos (도시락, 포장 시제품 → empty photo cells). The ➡ arrows
drawn as images become → (inside a line) or ▶ (between boxes), the (+) joints become "+". The
신규 / 개선 tags and the 주요성과 source pills are separate boxed / dark / gray cells.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kit  # noqa: E402
from kit import Layout, recipe_inputs  # noqa: E402

source, target = recipe_inputs(44, "배움에 소외되는 사람이 없도록 취약계층 배움 기회 제공")
L = Layout(top=3100)
kit.setup(source, L)
from kit import *  # noqa: E402,F401,F403  helpers and presets bound to this page

DARK, BAND = "#707070", "#E5E5E5"
LABEL = "#E5E5E5"      # row labels (프로그램 / 고도화 과정 / 실적)
SIDE = "#EDEDED"       # KDN 3大, IT We로 labels
HEADC = "#D9D9D9"      # card headers, 추진배경 label
BOX = frame(WHITE, top="soft", bottom="soft", left="soft", right="soft")


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


def arrowed(runs, gap="  "):
    """The PDF leaves a double blank where a ➡ image sits; type → there."""
    out = []
    for text, size, bold, color in runs:
        if gap in text.strip():
            head, _, tail = text.partition(gap)
            out += [(head + " → ", size, bold, color), (tail, size, bold, color)]
        elif text.endswith(gap) and text.strip():
            out.append((text.rstrip() + " → ", size, bold, color))
        else:
            out.append((text, size, bold, color))
    return [r for r in out if r[0]]


def chip(g, x0, x1, r0, r1, content, fill, **kw):
    """Small boxed / dark tag cell: narrow padding so the two-letter word stays on one line."""
    g.put(x0, x1, r0, r1, content, fill, fit=False, line=1000, **kw)
    key = (r0, g.xs.index(to_x(x0)))
    g.items[key] = g.items[key][:7] + (dict(left=40, right=40, top=20, bottom=20),)


def section_band(name, num_line, title_line, top):
    """'2 | heading' band: dark number cell and light gray title cell (images in the PDF)."""
    g = Grid(name, [X0, 84.5, X1], [2300])
    g.put(X0, 84.5, 0, 1, [runs_of(num_line, WHITE)], frame(DARK), line=1700)
    g.put(84.5, X1, 0, 1, [runs_of(title_line)], frame(BAND), align="LEFT", line=1700)
    block(g, top)


def boxed(name, label_line, body_lines, top, height, label_fill=HEADC, label_color=INK):
    """추진배경 / 주요성과 box: label at left, outlined body with bullet lines."""
    g = Grid(name, [X0, 111.7, X1], [height])
    g.put(X0, 111.7, 0, 1, [runs_of(label_line, label_color)],
          frame(label_fill, top="mid", bottom="mid", left="mid"))
    g.put(111.7, X1, 0, 1, body_lines, frame(top="mid", bottom="mid", right="mid"), align="LEFT")
    block(g, top)


def heading(name, line, top):
    g = Grid(name, [X0, X1], [1650])
    g.put(X0, X1, 0, 1, [line], align="LEFT", line=1450)
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

# ---------------------------------------------------------------------------
# 2. 배움에 소외되는 사람이 없도록 ...
# ---------------------------------------------------------------------------
section_band("sec2", line1(60, 70, 73, 76), line1(90, 95, 74, 77), 70.9)
boxed("background2", line1(65, 70, 106, 110), lines_in(115, 120, 104, 120), 99.6, 2440)

# KDN 3大 사회공헌 프로그램: label + three cards joined by (+)
cards = ((114.7, 155.7, 190.3, 252.6, 120.7), (266.4, 302.6, 337.2, 404.2, 272.3),
         (418.0, 449.3, 483.8, X1, 423.9))
xs = [X0, 112.7] + [x for c in cards for x in c[:4]]
g = Grid("programs", xs, [400, 1170, 580, 4470])
g.put(X0, 112.7, 0, 4, lines_in(60, 110, 136, 190), frame(SIDE), bold=True, line=1320)
for k, (a, p0, p1, e, base) in enumerate(cards):
    head = line1(p0, p1, 132, 136)
    g.put(a, e, 0, 1, [], frame(HEADC, top="mid", left="mid", right="mid"))
    g.put(a, p0, 1, 3, [], frame(HEADC, left="mid"))
    g.put(p0, p1, 1, 2, [runs_of(head, x1=p1 - 1.0)], BOX, line=1000)
    g.put(p0, p1, 2, 3, [], frame(HEADC))
    g.put(p1, e, 1, 3, [runs_of(head, x0=p1 - 1.0)], frame(HEADC, right="mid"), align="LEFT", line=1250)
    g.put(a, e, 3, 4, hang(lines_in(a, e, 150, 190), base), frame(left="mid", right="mid", bottom="mid"),
          align="LEFT", line=1320)
    if k < 2:
        g.put(e, cards[k + 1][0], 0, 4, "+", size=1300, bold=True, color="#9A9A9A", fit=False)
block(g, 129.8)

# ---------------------------------------------------------------------------
# 가. 기관의 業과 연계한 고유 사회공헌 프로그램의 고도화
# ---------------------------------------------------------------------------
heading("title-ga", line1(55, 60, 203, 207), 201.5)

xs = [X0, 113.6, 116.2, 129.8, 148.6, 337.3, 348.8, 367.6, X1]
g = Grid("advance", xs, [2280, 270, 2300, 240, 4610, 1440, 440])
lab = frame(LABEL)
g.put(X0, 113.6, 0, 1, [line1(60, 110, 230, 236)], lab, bold=True)
g.put(116.2, 337.3, 0, 1, [line1(130, 140, 230, 236)], frame("#E4E4E4"))
g.put(337.3, X1, 0, 1, [line1(338, 345, 230, 236)], frame("#E4E4E4"))
g.put(X0, 113.6, 2, 3, [line1(58, 70, 256, 260)], lab)
g.put(116.2, X1, 2, 3, [line1(120, 125, 256, 260)], frame(top="soft", bottom="soft", left="soft", right="soft"),
      align="LEFT")
g.put(X0, 113.6, 4, 7, [line1(70, 80, 302, 306)], lab)
g.put(116.2, 337.3, 4, 5, hang(lines_in(120, 335, 279, 320), 122.0), frame(top="soft", left="soft", right="dot"),
      align="LEFT", line=1430)
g.put(337.3, X1, 4, 5, hang(lines_in(338, 345, 279, 320), 341.0), frame(top="soft", right="soft"),
      align="LEFT", line=1430)
for a, b, c, e, y in ((116.2, 129.8, 148.6, 337.3, 122.0), (337.3, 348.8, 367.6, X1, 341.0)):
    left = a < 300          # the left half carries the outer left border and the dotted divider
    tagged = line1(y - 1, y + 1, 322, 326)
    g.put(a, b, 5, 6, [runs_of(tagged, x1=b)], frame(left="soft") if left else frame(), align="RIGHT")
    chip(g, b, c, 5, 6, [runs_of(tagged, x0=b, x1=c - 0.5)], BOX)
    g.put(c, e, 5, 6, [strip_runs(runs_of(tagged, x0=c - 0.5))], frame(right="dot" if left else "soft"),
          align="LEFT")
    g.put(a, e, 6, 7, [], frame(bottom="soft", right="dot" if left else "soft", left="soft" if left else None))
block(g, 225.6)

# ---------------------------------------------------------------------------
# 나. 자립준비청소년·청년 ... 「IT We로」
# ---------------------------------------------------------------------------
heading("title-na", line1(55, 60, 347, 351), 345.5)

xs = [X0, 81.3, 100.1, 125.4, 127.5, X1]
g = Grid("we-ro", xs, [720, 1170, 3240, 400, 730, 1170, 3240])
for r, tag, tag_fill, (y0, y1) in ((0, "신규", BOX, (390, 415)), (4, "개선", frame("#7F7F7F"), (445, 470))):
    tag_line = line1(81, 100, y0 - 14, y0 - 8)
    g.put(X0, 125.4, r, r + 1, [], frame(SIDE, top="mid", left="mid", right="mid"))
    g.put(X0, 81.3, r + 1, r + 2, [], frame(SIDE, left="mid"))
    chip(g, 81.3, 100.1, r + 1, r + 2, [runs_of(tag_line, WHITE if r else INK)], tag_fill)
    g.put(100.1, 125.4, r + 1, r + 2, [], frame(SIDE, right="mid"))
    g.put(X0, 125.4, r + 2, r + 3, lines_in(60, 125, y0, y1), frame(SIDE, left="mid", right="mid", bottom="mid"),
          bold=True, line=1320)
g.put(127.5, X1, 0, 4, lines_in(130, 135, 374, 412), frame(top="mid", left="mid", right="mid", bottom="dot"),
      align="LEFT", line=1540)
g.put(127.5, X1, 4, 7, lines_in(130, 135, 427, 465), frame(left="mid", right="mid", bottom="mid"),
      align="LEFT", line=1540)
block(g, 370.5)

# ---------------------------------------------------------------------------
# 3. 전통시장·소상공인 경쟁력 강화로 자생력 확보 및 지역경제 활성화
# ---------------------------------------------------------------------------
section_band("sec3", line1(60, 70, 492, 496), line1(90, 95, 492, 497), 489.8)
boxed("background3", line1(65, 70, 524, 528), lines_in(115, 120, 523, 535), 518.5, 2440)

xs = [X0, 85.0, 95.9, 131.8, 150.3, 318.0, 331.7, 432.0, 442.3, X1]
g = Grid("market", xs, [1840, 7020, 1810, 6640, 1700, 2060])
head = "#D7D7D7"
g.put(X0, 85.0, 0, 1, [line1(60, 85, 551, 555)], frame(head, top="mid", right="soft"))
g.put(85.0, X1, 0, 1, [line1(290, 310, 551, 555)], frame(head, top="mid"))
side = frame("#EBEBEB", bottom="soft")
g.put(X0, 85.0, 1, 3, lines_in(60, 85, 595, 620), side, line=1430)
market = hang(lines_in(86, 100, 572, 650), 88.0)
g.put(85.0, 442.3, 1, 3, [arrowed(r) for r in market], frame(bottom="soft"), align="LEFT", line=1550)
g.put(442.3, X1, 1, 2, [], photo)
g.put(442.3, X1, 2, 3, [line1(450, 470, 640, 645)], frame("#EDEDED", bottom="soft", hatch="#DEDEDE"), size=990)
g.put(X0, 85.0, 3, 6, lines_in(60, 85, 690, 715), frame("#EBEBEB", bottom="mid"), line=1430)
g.put(85.0, 442.3, 3, 4, hang(lines_in(86, 100, 656, 715), 88.0), align="LEFT", line=1520)
# 협업체계: dark label, ▶, two partner boxes joined by (+) with hatched role cells
g.put(85.0, 95.9, 4, 6, [], frame(bottom="mid"))
g.put(95.9, 131.8, 4, 6, lines_in(100, 130, 724, 748), frame("#CACACA", bottom="mid"), line=1430)
g.put(131.8, 150.3, 4, 6, "▶", frame(bottom="mid"), size=1000, color=ARROW)
g.put(150.3, 318.0, 4, 5, [line1(190, 200, 724, 730)], frame(top="soft"))
g.put(318.0, 331.7, 4, 6, "+", frame(bottom="mid"), size=1300, bold=True, color="#9A9A9A", fit=False)
g.put(331.7, 432.0, 4, 5, [line1(350, 360, 724, 730)], frame(top="soft"))
hatched = frame("#E9E9E9", bottom="mid", hatch="#DCDCDC")
g.put(150.3, 318.0, 5, 6, [line1(155, 165, 740, 745)], hatched)
g.put(331.7, 432.0, 5, 6, [line1(335, 345, 740, 745)], hatched)
g.put(432.0, 442.3, 4, 6, [], frame(bottom="mid"))
g.put(442.3, X1, 3, 5, [], photo)
g.put(442.3, X1, 5, 6, [line1(460, 470, 743, 748)], frame("#E5E5E5", bottom="mid", hatch="#DEDEDE"), size=990)
block(g, 548.7)

# ---------------------------------------------------------------------------
# 주요성과: bullet, gray source pill, bold result per line.
# ---------------------------------------------------------------------------
xs = [X0, 111.7, 125.6, 185.5, 208.2, X1]
g = Grid("result", xs, [390, 1320, 290, 1310, 410])
g.put(X0, 111.7, 0, 5, [line1(65, 70, 777, 781)], frame("#7F7F7F", top="mid", bottom="mid", left="mid"),
      color=WHITE)
g.put(111.7, X1, 0, 1, [], frame(top="mid", right="mid"))
g.put(111.7, X1, 2, 3, [], frame(right="mid"))
g.put(111.7, X1, 4, 5, [], frame(bottom="mid", right="mid"))
pill = frame("#D5D5D5")
for r, y, end in ((1, 770, 185.5), (3, 786, 208.2)):
    l = line1(115, 120, y - 1, y + 2)
    g.put(111.7, 125.6, r, r + 1, [runs_of(l, x1=125.0)], align="RIGHT", line=1150)
    g.put(125.6, end, r, r + 1, [runs_of(l, x0=125.0, x1=end - 1.0)], pill, line=1000)
    g.put(end, X1, r, r + 1, [strip_runs(runs_of(l, x0=end - 1.0))], frame(right="mid"), align="LEFT",
          line=1150)
block(g, 765.3)

kit.finish(target, end=803.0)
