"""Rebuild KDN 2025 report page 96 (PDF 2 local page 46, printed page 66) as editable HWPX.

Usage: python3 work/kdn2025/p96.py <report2.pdf> <out.hwpx> [--page 46]

상생·협력 및 지역발전 평가내용 03, section 2 (AMI 품질시험센터 개방 / KDN 에코로드). Built with the
shared diagram kit (one flat table per horizontal band on a grid of PDF x edges). Text comes from
the PDF text layer except these image-only parts, typed from 4-6x renders: the 'Best Practice'
sticker (trophy dropped), the ①-④ number marks of 개방내용, 복합문화쉼터 and the four facility pills,
and the small bar chart's labels (539건 '24년, 3,441건 '25년; bars and curve arrow left out). The
KDN 에코로드 illustration is an empty photo cell; circled arrows and chevrons become ▶, pointers ▼,
the (+) joint "+". 신규 / 개선 / 기관業 / 문화 / 시설개방 / 비용절감 / MOU체결 / 시설 제공 / 기술 지원
tags are separate boxed or dark cells. The source draws two middle dots with Wingdings U+F09E
(‘시설·장비’ in the section title, 시민 참여형·지역 연계형); they stay that character in a
Wingdings run so they print as in the PDF.
"""

import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kit  # noqa: E402
from kit import Layout, recipe_inputs  # noqa: E402

source, target = recipe_inputs(46, "기관 보유 ‘시설")
L = Layout(top=3100)
kit.setup(source, L)
from kit import *  # noqa: E402,F401,F403  helpers and presets bound to this page

DARK, BAND = "#707070", "#E5E5E5"
HEADC = "#D9D9D9"
WING = "#16161A"       # run colour marking the Wingdings U+F09E dot; re-mapped at the end
BOX = frame(WHITE, top="soft", bottom="soft", left="soft", right="soft")
HATCH = frame("#E6E6E6", hatch="#D6D6D6")


def wing(runs):
    """Split the Wingdings middle dot (U+F09E) into its own marked run."""
    out = []
    for text, size, bold, color in runs:
        for k, part in enumerate(text.split("")):
            if k:
                out.append(("", size, bold, WING))
            if part:
                out.append((part, size, bold, color))
    return out


def hang(lines, base):
    """Bullet lines keep their PDF indent: spaces for the x offset and for the line's own lead."""
    out = []
    for l in lines:
        runs = runs_of(l)
        size = runs[0][1] / 100
        raw = "".join(s["text"] for s in l["spans"])
        offset = l["bbox"][0] - base + (len(raw) - len(raw.lstrip(" "))) * 0.29 * size
        n = max(0, round(offset / (0.29 * size)))
        if n:
            runs = [(" " * n, runs[0][1], False, INK)] + runs
        out.append(wing(runs))
    return out


def chip(g, x0, x1, r0, r1, content, fill, **kw):
    """Small tag / pill cell: narrow padding so a short word stays on one line."""
    kw.setdefault("line", 1000)
    g.put(x0, x1, r0, r1, content, fill, fit=False, **kw)
    key = (r0, g.xs.index(to_x(x0)))
    g.items[key] = g.items[key][:7] + (dict(left=40, right=40, top=20, bottom=20),)


def boxed(name, label_line, body_lines, top, height, label_fill=HEADC, label_color=INK):
    """추진배경 / 주요성과 box: label at left, outlined body with bullet lines."""
    g = Grid(name, [X0, 111.7, X1], [height])
    g.put(X0, 111.7, 0, 1, [runs_of(label_line, label_color)],
          frame(label_fill, top="mid", bottom="mid", left="mid"))
    g.put(111.7, X1, 0, 1, body_lines, frame(top="mid", bottom="mid", right="mid"), align="LEFT", line=1540)
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
# 2. 기관 보유 ‘시설·장비’ 개방 및 대국민 ‘복합문화쉼터’ 확대
# ---------------------------------------------------------------------------
g = Grid("sec2", [X0, 84.5, X1], [2300])
g.put(X0, 84.5, 0, 1, [runs_of(line1(60, 70, 73, 76), WHITE)], frame(DARK), line=1700)
g.put(84.5, X1, 0, 1, [wing(runs_of(line1(90, 95, 73, 76)))], frame(BAND), align="LEFT", line=1700)
block(g, 70.9)

g = Grid("title-ga", [X0, 430.8, 501.4, X1], [1650])
g.put(X0, 430.8, 0, 1, [line1(55, 60, 101, 105)], align="LEFT", line=1450)
chip(g, 430.8, 501.4, 0, 1, [[("Best Practice", 860, True, WHITE)]], frame("#323232"))
block(g, 100.3)

boxed("background", line1(65, 70, 135, 139), lines_in(115, 120, 127, 147), 123.2, 3710)

# 추진방향 / 개방내용 / 개방효과 (label column darkens downwards)
xs = [X0, 105.1, 107.6, 123.0, 157.0, 157.5, 208.5, 219.5, 255.4, 257.9, 273.5, 307.0, 320.5, 328.5, 331.5,
      337.5, 382.5, 405.5, 408.1, 414.0, 432.5, 443.5, 452.0, X1]
#      0 dir-h 1 dir-b 2 pad 3 gap 4 tabs 5 sub 6 bul  7 flow 8 pad 9 gap 10 eff-h 11 mid 12 ▼  13 low 14 pad
hs = [2090, 2300, 300, 530, 1900, 3370, 3370, 1980, 320, 530, 1930, 1570, 580, 2290, 320]
g = Grid("ami", xs, hs)
g.put(X0, 105.1, 0, 4, [line1(60, 65, 184, 188)], frame("#E6E6E6", top="mid"), bold=True)
g.put(X0, 105.1, 4, 10, [line1(60, 65, 271, 275)], frame("#CBCBCB"), bold=True)
g.put(X0, 105.1, 10, 15, [line1(60, 65, 364, 368)], frame("#B2B2B2", bottom="mid"), bold=True)
# 추진방향: two outlined boxes (title / gray bullet) joined by (+)
for a, e, tx, bx in ((107.6, 328.5, 145, 113), (337.5, X1, 400, 338)):
    g.put(a, e, 0, 1, [line1(tx, tx + 10, 170, 174)], frame(top="mid", left="mid", right="mid"))
    g.put(a, e, 1, 2, [line1(bx, bx + 3, 193, 197)], frame("#E6E6E6", left="mid", right="mid"), align="LEFT")
    g.put(a, e, 2, 3, [], frame(left="mid", right="mid", bottom="mid"))
g.put(328.5, 337.5, 0, 1, "+", size=1300, bold=True, color="#9A9A9A", fit=False)
# 개방내용 header: white tabs on a gray band
band = frame(HEADC, top="mid")
chip(g, 107.6, 157.5, 4, 5, [runs_of(line1(110, 115, 222, 226))], frame(WHITE, top="mid", left="mid", right="soft",
                                                                       bottom="soft"))
g.put(157.5, 331.5, 4, 5, [strip_runs(runs_of(line1(160, 165, 222, 226)))], band)
chip(g, 331.5, 382.5, 4, 5, [runs_of(line1(333, 338, 222, 226))], frame(WHITE, top="mid", left="soft", right="soft",
                                                                      bottom="soft"))
g.put(382.5, X1, 4, 5, [strip_runs(runs_of(line1(384, 390, 222, 226)))], frame(HEADC, top="mid", right="mid"))
cols4 = ((107.6, 219.5, 113.5), (219.5, 331.5, 225.1), (331.5, 443.5, 336.6), (443.5, X1, 448.1))
for k, (a, e, base) in enumerate(cols4):
    sides = dict(left="mid" if k == 0 else "soft", right="mid" if k == 3 else None)
    top, sub = (line1(a, e, 242, 246), line1(a, e, 256, 260))
    g.put(a, e, 5, 6, [[("①②③④"[k] + " ", int(round(top["spans"][0]["size"] * 10)) * 10, False, INK)]
                       + runs_of(top), runs_of(sub)], frame("#E1E1E1", **sides), line=1420)
    g.put(a, e, 6, 7, hang(lines_in(a, e, 273, 295), base),
          frame(left="mid" if k == 0 else "dot", right="mid" if k == 3 else None), align="LEFT", line=1550)
flow = ((107.6, 208.5, "#F2F2F2"), (219.5, 320.5, "#E6E6E6"), (331.5, 432.5, "#D8D8D8"), (443.5, X1, "#C9C9C9"))
for k, (a, e, fill) in enumerate(flow):
    g.put(a, e, 7, 8, [line1(a, e, 308, 312)], frame(fill, left="mid" if k == 0 else None,
                                                     right="mid" if k == 3 else None))
    if k < 3:
        g.put(e, flow[k + 1][0], 7, 8, "▶", frame(fill), size=900, color="#6A6A6A", fit=False)
g.put(107.6, X1, 8, 9, [], frame(left="mid", right="mid", bottom="mid"))
# 개방효과: three boxes (tag + title / text / ▼ / gray result)
boxes = ((107.6, 123.0, 157.0, 255.4, 120), (257.9, 273.5, 307.0, 405.5, 270), (408.1, 414.0, 452.0, X1, 410))
for a, t0, t1, e, tx in boxes:
    head = line1(tx, tx + 10, 337, 341)
    g.put(a, t0, 10, 11, [], frame(top="mid", left="mid"))
    chip(g, t0, t1, 10, 11, [runs_of(head, x1=t1 - 1.0)], BOX)
    g.put(t1, e, 10, 11, [strip_runs(runs_of(head, x0=t1 - 1.0))], frame(top="mid", right="mid"), align="LEFT")
    g.put(a, e, 11, 12, [line1(a, e, 355, 359)], frame(left="mid", right="mid"))
    g.put(a, e, 12, 13, "▼", frame(left="mid", right="mid"), size=600, color="#9A9A9A", line=420)
    g.put(a, e, 13, 14, [line1(a, e, 380, 384)], frame("#E6E6E6", left="mid", right="mid"))
    g.put(a, e, 14, 15, [], frame(left="mid", right="mid", bottom="mid"))
block(g, 166.6)

g = Grid("footnote", [X0, X1], [1350])
g.put(X0, X1, 0, 1, [line1(55, 60, 403, 407)], align="LEFT", line=1050)
block(g, 402.5)

# ---------------------------------------------------------------------------
# 나. KDN 에코로드: 복합문화쉼터 cards, then the 에코로드 facility counts.
# ---------------------------------------------------------------------------
heading("title-na", line1(55, 60, 423, 427), 422.0)

xs = [X0, 106.0, 108.0, 136.0, 257.0, 275.5, 280.0, 283.0, 293.5, 312.0, 318.5, 452.0, 469.5, 511.0, X1]
#      0 head 1 pad 2 cardh 3 bul1 4 bul2 5 sum  6 pad 7 cardh 8 bul1 9 bul2 10 sum
hs = [1920, 500, 1590, 1460, 2070, 2450, 500, 1600, 1460, 2040, 2580]
g = Grid("culture", xs, hs)
g.put(X0, X1, 0, 1, [line1(220, 225, 448, 452)], frame(HEADC, top="mid", left="mid", right="mid"), bold=True)
side = frame("#EBEBEB", left="mid")
g.put(X0, 106.0, 1, 6, [line1(60, 65, 498, 502)], frame("#EBEBEB", left="mid", bottom="soft"))
g.put(X0, 106.0, 6, 11, [line1(60, 65, 578, 582)], frame("#EBEBEB", left="mid", bottom="mid"))
num = frame("#8C8C8C")
cardh = frame("#D8D8D8")
for r0, (y_head, n1, n2) in ((2, (470.5, "①", "②")), (7, (551.3, "③", "④"))):
    g.put(108.0, 136.0, r0, r0 + 1, [[(n1, 1090, True, WHITE)]], num)
    g.put(136.0, 280.0, r0, r0 + 1, [line1(150, 200, y_head - 1, y_head + 2)], cardh)
    g.put(283.0, 312.0, r0, r0 + 1, [[(n2, 1090, True, WHITE)]], num)
    g.put(312.0, 452.0, r0, r0 + 1, [line1(330, 350, y_head - 1, y_head + 2)], cardh)
# row 1 bullets: 신규 tag at the end of the first card line, 기관業 / 문화 tags after the second card's bullets
l1 = line1(108, 112, 490, 493)
g.put(108.0, 257.0, 3, 4, [strip_runs(runs_of(l1, x1=258.0))], align="LEFT")
chip(g, 257.0, 275.5, 3, 4, [runs_of(l1, x0=258.0)], BOX)
g.put(108.0, 280.0, 4, 5, [line1(108, 112, 506, 509)], align="LEFT")
for r, y in ((3, 491.3), (4, 507.0)):
    parts = lines_in(284, 320, y - 1, y + 2)
    bullet, tagline = parts[0], parts[-1]
    g.put(283.0, 293.5, r, r + 1, [runs_of(bullet, x1=293.0)], align="RIGHT")
    chip(g, 293.5, 318.5, r, r + 1, [runs_of(tagline, x0=293.0, x1=318.5)], BOX)
    g.put(318.5, 452.0, r, r + 1, [strip_runs(runs_of(tagline, x0=318.5))], align="LEFT")
g.put(108.0, 280.0, 5, 6, [hang([line1(115, 125, 525, 529)], 120.4)[0]], HATCH)
g.put(283.0, 452.0, 5, 6, [line1(300, 310, 526, 530)], HATCH)
# row 2 bullets: 신규 (boxed) and 개선 (dark) tags after the second card's bullets
g.put(108.0, 280.0, 8, 10, lines_in(108, 112, 570, 590), align="LEFT", line=1540)
for r, y, fill, color in ((8, 572.0, BOX, INK), (9, 587.7, frame("#8C8C8C"), WHITE)):
    l = line1(284, 288, y - 1, y + 2)
    g.put(283.0, 293.5, r, r + 1, [runs_of(l, x1=293.0)], align="RIGHT", line=1300)
    chip(g, 293.5, 312.0, r, r + 1, [runs_of(l, color, x0=293.0, x1=311.0)], fill)
    g.put(312.0, 452.0, r, r + 1, [strip_runs(runs_of(l, x0=311.0))], align="LEFT", line=1300)
HATCH_LOW = frame("#E6E6E6", hatch="#D6D6D6", bottom="mid")
g.put(108.0, 280.0, 10, 11, [line1(110, 120, 606, 610)], HATCH_LOW)
g.put(283.0, 452.0, 10, 11, [line1(290, 295, 606, 610)], HATCH_LOW)
g.put(106.0, 108.0, 10, 11, [], frame(bottom="mid"))
g.put(280.0, 283.0, 10, 11, [], frame(bottom="mid"))
# chevrons and the right-hand panels (bar chart labels typed from the image)
g.put(452.0, 469.5, 1, 6, "▶", size=1300, color="#C8C8C8")
g.put(452.0, 469.5, 6, 11, "▶", frame(bottom="mid"), size=1300, color="#C8C8C8")
g.put(469.5, X1, 1, 4, lines_in(475, 545, 466, 490), frame("#E4E4E4", right="mid"), line=1320)
g.put(469.5, 511.0, 4, 5, [[("539건", 900, False, INK)]], align="CENTER")
g.put(511.0, X1, 4, 5, [[("3,441건", 900, True, INK)]], frame(right="mid"))
g.put(469.5, 511.0, 5, 6, [[("’24년", 800, False, INK)]], frame("#E9E9E9", top="soft", bottom="soft"))
g.put(511.0, X1, 5, 6, [[("’25년", 800, True, INK)]], frame("#E9E9E9", top="soft", bottom="soft", right="mid"))
g.put(469.5, X1, 6, 9, lines_in(475, 545, 548, 570), frame("#E4E4E4", right="mid"), line=1320)
g.put(469.5, X1, 9, 11, lines_in(475, 545, 584, 606), frame(right="mid", bottom="mid"), line=1540)
for r in (1, 6):
    g.put(108.0, 452.0, r, r + 1, [], frame(top="soft") if r == 6 else frame())
block(g, 445.1)

# 「KDN 에코로드」 illustration (photo cell) and the facility counts (total 3,441 = 2,143+1,082+37+179)
xs = [X0, 202.5, 205.0, 289.5, 392.5, 394.4, 474.1, X1]
hs = [2290, 1000, 350, 1900, 2250, 400, 1900, 2490]
g = Grid("ecoroad", xs, hs)
g.put(X0, 202.5, 0, 1, [line1(90, 100, 638, 642)], frame("#E3E3E3", top="mid", left="mid", hatch="#D3D3D3"))
g.put(X0, 202.5, 1, 8, [], frame("#E4E4E4", left="mid", bottom="mid", top="soft"))
g.put(205.0, X1, 0, 1, [runs_of(line1(245, 255, 638, 642), WHITE)], frame("#707070", top="mid", right="mid"))
g.put(205.0, X1, 1, 2, "▼", frame(right="mid"), size=700, color="#8C8C8C", line=700)
g.put(205.0, X1, 2, 3, [], frame(right="mid"))
g.put(205.0, X1, 5, 6, [], frame(right="mid"))
pill = frame("#E3E3E3", top="soft", bottom="soft", left="soft", right="soft")
items = (((3, 4), (205.0, 289.5, 392.5), (225, 674), (350, 674), (210, 693), "①"),
         ((3, 4), (394.4, 474.1, X1), (414, 674), (510, 674), (400, 693), "②"),
         ((6, 7), (205.0, 289.5, 392.5), (225, 719), (365, 719), (210, 738), "③"),
         ((6, 7), (394.4, 474.1, X1), (414, 719), (520, 719), (400, 738), "④"))
for (rp, rd), (a, b, e), (px, py), (cx, cy), (dx, dy), mark in items:
    last = e == X1
    head = line1(px, px + 3, py, py + 3)
    chip(g, a, b, rp, rp + 1, [[(mark + " ", 990, True, INK)] + runs_of(head)], pill)
    g.put(b, e, rp, rp + 1, [line1(cx, cx + 10, cy, cy + 3)], frame(top="soft", right="mid" if last else None),
          align="RIGHT")
    g.put(a, e, rd, rd + 1, [line1(dx - 2, dx + 2, dy, dy + 3)], frame("#ECECEC", hatch="#DCDCDC",
                                                                         right="mid" if last else None,
                                                                         bottom="mid" if rd == 7 else None),
          align="LEFT")
block(g, 633.1)

boxed("result", line1(65, 70, 777, 781), lines_in(115, 120, 768, 790), 765.2, 3710, label_fill="#7F7F7F",
      label_color=WHITE)

# ---------------------------------------------------------------------------
# finish: Wingdings face for the U+F09E dots, then the kit's own finish
# ---------------------------------------------------------------------------
wing_ids = {}
for family in L.header.iter(L.q("hh:fontface")):
    font = deepcopy(family[0])
    ident = str(max(int(f.get("id")) for f in family) + 1)
    font.set("id", ident)
    font.set("face", "Wingdings")
    family.append(font)
    family.set("fontCnt", str(len(family)))
    wing_ids[family.get("lang").lower()] = ident
for char in L.characters:
    if char.get("textColor") == WING:
        char.set("textColor", INK)
        ref = L.get(char, "hh:fontRef")
        for lang in ref.attrib:
            ref.set(lang, wing_ids[lang])
kit.finish(target, end=803.0)
