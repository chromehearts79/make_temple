"""Rebuild KDN 2025 report page 73 (second PDF local page 23, printed page 47) as editable HWPX.

Usage: python3 work/kdn2025/p73.py <report2.pdf> <out.hwpx> [--page 23]

친환경·탄소중립 section 4 (KDN Eco-Life). Built with the shared kit: one flat table per horizontal
band on a grid of PDF x edges. Text comes from the PDF text layer except these images, read from
3-5x renders and typed: the 추진경과 timeline ('21년 도입기 / '23년 안정기 / '25년 확산기 / 대국민
환경실천 문화 정착), the Q / A marks, the 'Best Practice' badge and the 지적사항 개선 / NEW 신규
stickers. The person illustrations of 공감성 / 접근성 / 체감성, the timeline icons and the arrow
discs of the table head are omitted (the arrow discs become ▶). Inline boxed tags (국가, 지역, 외부,
시설, 소통, 확산, 강화) are separate cells; the text cell after a tag starts on the tag's row and is
top aligned. The three 활동분야 groups are laid on a grid of PDF y breakpoints (ygrid).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kit  # noqa: E402
from kit import Layout, recipe_inputs  # noqa: E402

source, target = recipe_inputs(23, "대국민 소통 및 친환경 활동 강화")
L = Layout(top=3100)
kit.setup(source, L)
from kit import *  # noqa: E402,F401,F403  helpers and presets bound to this page

DARK, LABEL, HEAD = "#6A6A6A", "#E6E6E6", "#D9D9D9"
TAG = frame(WHITE, top="soft", bottom="soft", left="soft", right="soft")
STICKER = frame("#3C3C3C")
TOP = []


def put(g, x0, x1, r0, r1, content, fill="1", *, top=False, **kw):
    """Grid.put; top=True aligns the cell's text to the top (text that follows a tag cell)."""
    g.put(x0, x1, r0, r1, content, fill, **kw)
    if top:
        TOP.append(g.items[r0, g.xs.index(to_x(x0))][3][0])


def ygrid(name, xs, top, bottom, items):
    """One band whose rows are the union of the items' PDF y edges.
    items: (x0, x1, y0, y1, content, fill, options)."""
    ys = sorted({round(top, 1), round(bottom, 1)} | {round(y, 1) for it in items for y in it[2:4]})
    hs = [int(round((b - a) * 100)) for a, b in zip(ys, ys[1:])]
    small = [h for h in hs if h < 270]
    if small:
        raise ValueError(f"{name}: rows below 2.7 pt {small}")
    g = Grid(name, xs, hs)
    for x0, x1, y0, y1, content, fill, kw in items:
        put(g, x0, x1, ys.index(round(y0, 1)), ys.index(round(y1, 1)), content, fill, **kw)
    block(g, top)


def hang(lines, base):
    """Continuation lines keep their PDF indent: spaces for the x offset."""
    out = []
    for l in lines:
        runs = runs_of(l)
        n = max(0, round((l["bbox"][0] - base) / (0.29 * runs[0][1] / 100)))
        out.append([(" " * n, runs[0][1], False, INK)] + runs if n else runs)
    return out


def lead(line):
    """'  - text' lines: keep the leading blanks of the PDF line."""
    raw = "".join(s["text"] for s in line["spans"])
    runs = runs_of(line)
    n = len(raw) - len(raw.lstrip(" "))
    return [(" " * n, runs[0][1], False, INK)] + runs if n else runs


def section_band(name, num_line, title_line, top):
    g = Grid(name, [X0, 84.5, X1], [2300])
    g.put(X0, 84.5, 0, 1, [runs_of(num_line, WHITE)], frame(DARK), line=1700)
    g.put(84.5, X1, 0, 1, [runs_of(title_line)], frame(LABEL), align="LEFT", line=1700)
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

g = Grid("head", [X0, 401.0, X1], [1680])
g.put(X0, 401.0, 0, 1, [], frame(bottom="soft"))
g.put(401.0, X1, 0, 1, [line1(400, 410, 35, 40)], align="RIGHT")
block(g, 32.0)

section_band("sec4", line1(60, 70, 72, 76), line1(90, 95, 73, 77), 70.9)

g = Grid("title-ga", [X0, 374.5, 445.5, X1], [1650])
g.put(X0, 374.5, 0, 1, [line1(55, 60, 101, 105)], align="LEFT", line=1450)
g.put(374.5, 445.5, 0, 1, "Best Practice", STICKER, size=850, bold=True, color=WHITE, line=1000)
block(g, 101.5)

# Q / A boxes (the Q and A marks are images, typed)
xs = [X0, 94.3, 190.3, 192.7, 232.7, X1]
g = Grid("qa", xs, [3880])
for a, b, e, mark, x in ((X0, 94.3, 190.3, "Q", 100), (192.7, 232.7, X1, "A", 236)):
    g.put(a, b, 0, 1, mark, frame(top="soft", bottom="soft", left="strong", right="soft"), size=1300, bold=True)
    g.put(b, e, 0, 1, lines_in(x, x + 5, 124, 150), frame(top="soft", bottom="soft", right="strong"), align="LEFT",
          line=1530)
block(g, 123.0)

g = Grid("background", [X0, 111.7, X1], [3690])
g.put(X0, 111.7, 0, 1, [line1(65, 70, 179, 183)], frame("#D5D5D5", top="mid", bottom="mid", left="mid"))
g.put(111.7, X1, 0, 1, lines_in(115, 120, 172, 192), frame(top="mid", bottom="mid", right="mid"), align="LEFT",
      line=1530)
block(g, 167.9)

# 추진경과 timeline (an image in the PDF; icons omitted)
xs = [X0, 113.6, 115.8, 127.5, 137.9, 155.0, 240.0, 250.3, 267.5, 359.0, 369.3, 386.5, 476.0, 485.0, 552.7, X1]
g = Grid("timeline", xs, [1450, 1600, 700, 2980])
g.put(X0, 113.6, 0, 4, [line1(65, 70, 240, 244)], frame("#EDEDED", top="soft"))
periods = (((127.5, 155.0), (155.0, 240.0), (137.9, 250.3), "’21년", "도입기",
            ["임직원 중심 친환경 실천", "KDN Eco-Life 브랜드 구축"]),
           ((240.0, 267.5), (267.5, 359.0), (250.3, 369.3), "’23년", "안정기",
            ["지역 참여형 실천 전환", "친환경 체험공간 에코로드 구축"]),
           ((359.0, 386.5), (386.5, 476.0), (369.3, 476.0), "’25년", "확산기",
            ["대국민 참여형 실천 확산", "국가 지역 연계 친환경 활동"]))
for (t0, t1), (n0, n1), (c0, c1), year, stage, lines in periods:
    g.put(t0, t1, 1, 2, year, TAG, size=930, line=1100)
    g.put(n0, n1, 1, 2, "  " + stage, align="LEFT", size=1150, bold=True)
    g.put(c0, c1, 3, 4, [[(t, 1050, False, INK)] for t in lines], frame(left="dot"), line=1350)
g.put(115.8, 476.0, 2, 3, [], frame("#C4C4C4"))
g.put(476.0, 485.0, 2, 3, "▶", size=650, color="#A0A0A0", line=540, fit=False)
g.put(485.0, 552.7, 0, 4, [[("대 국 민", 1150, True, WHITE)], [("환경실천", 1150, True, WHITE)],
                           [("문화 정착", 1150, True, WHITE)]], frame("#4E4E4E", hatch="#5C5C5C"), line=1450)
block(g, 211.5)

# 추진방향: three boxes (gray head, bullet body)
xs = [X0, 114.3, 116.0, 260.0, 264.3, 407.7, 412.0, X1]
g = Grid("direction", xs, [1850, 4000])
g.put(X0, 114.3, 0, 2, [line1(65, 70, 309, 312)], frame("#EDEDED", top="soft"))
for a, e in ((116.0, 260.0), (264.3, 407.7), (412.0, X1)):
    g.put(a, e, 0, 1, [line1(a, e, 288, 292)], frame(HEAD, top="mid", left="soft", right="soft"))
    g.put(a, e, 1, 2, lines_in(a, e, 308, 330), frame(bottom="soft", left="soft", right="soft"), align="LEFT",
          line=1540)
block(g, 285.0)

g = Grid("thesis", [X0, X1], [2070])
g.put(X0, X1, 0, 1, [line1(210, 220, 349, 352)], frame("#F0F0F0"))
block(g, 344.8)

# ---------------------------------------------------------------------------
# 활동분야 table: header + three groups (label | 주요 추진 내용 | 추진성과)
# ---------------------------------------------------------------------------
xs = [X0, 126.0, 137.7, 369.3, 382.7, X1]
g = Grid("table-head", xs, [2020])
head = frame(HEAD, top="mid")
g.put(X0, 126.0, 0, 1, [line1(70, 80, 373, 376)], head)
g.put(126.0, 137.7, 0, 1, "▶", head, size=700, color="#8A8A8A", fit=False)
g.put(137.7, 369.3, 0, 1, [line1(220, 230, 373, 376)], head)
g.put(369.3, 382.7, 0, 1, "▶", head, size=700, color="#8A8A8A", fit=False)
g.put(382.7, X1, 0, 1, [runs_of(line1(445, 455, 373, 376), WHITE)], frame("#5A5A5A", top="mid"))
block(g, 369.6)

MID, RIGHT = 129.3, 371.0
GAP = 131.3      # 129.3-131.3: a spacer column no item covers, so every row keeps a single-row cell
PILL = frame("#5A5A5A")
BAND = frame("#5E5E5E", hatch="#6C6C6C")


def group(name, top, bottom, label, pill_y, rows, result, band, last=False):
    """rows: ('dash', y, y0, y1) or ('tag', y, y0, tag_y1, y1, stickers) with stickers [(x0, x1, content, fill)]."""
    edge = "soft" if last else "dot"
    xs = {X0, MID, GAP, 134.6, 142.6, 162.8, 180.5, RIGHT, X1}
    items = [(X0, MID, top, bottom, lines_in(56, MID, *label), frame(LABEL, right="soft", bottom=edge),
              dict(line=1440))]
    ln = line1(140, 142, pill_y - 1, pill_y + 2)
    y0, y1 = pill_y - 1.5, pill_y + 13.5
    items += [(134.6, 180.5, y0, y1, [runs_of(ln, WHITE, x1=178.0)], PILL, dict(line=1000)),
              (180.5, RIGHT, y0, y1, [strip_runs(runs_of(ln, x0=178.0))], "1", dict(align="LEFT"))]
    for row in rows:
        if row[0] == "dash":
            _, y, y0, y1 = row
            items.append((GAP, RIGHT, y0, y1, [lead(line1(134, 136, y - 1, y + 2))], "1", dict(align="LEFT")))
            continue
        _, y, y0, tag_y1, y1, stickers = row
        ln = line1(134, 136, y - 1, y + 2)
        text_end = stickers[0][0] if stickers else RIGHT
        items += [(GAP, 142.6, y0, y1, [runs_of(ln, x1=142.0)], "1", dict(align="RIGHT", top=True)),
                  (142.6, 162.8, y0, tag_y1, [runs_of(ln, x0=142.0, x1=160.5)], TAG, dict(line=950)),
                  (162.8, text_end, y0, y1, [strip_runs(runs_of(ln, x0=160.5, x1=text_end - 1))], "1",
                   dict(align="LEFT", top=True))]
        for s0, s1, content, fill in stickers:
            xs |= {s0, s1}
            if content is None:            # the tag is in the text layer (강화)
                content = [runs_of(ln, WHITE, x0=s0)]
            items.append((s0, s1, y0, tag_y1, content, fill, dict(size=780, bold=True, color=WHITE, line=950)))
    last_y = max(it[3] for it in items[3:])
    items.append((GAP, RIGHT, last_y, bottom, [], frame(bottom=edge), {}))
    (r0, r1), ((b0, b1), (bx, by)) = result, band
    items += [(RIGHT, X1, top, b0, hang(lines_in(375, 390, r0, r1), 377.2), frame(left="soft"),
               dict(align="LEFT", line=1540)),
              (RIGHT, X1, b0, b1, [runs_of(line1(bx, bx + 3, by, by + 3), WHITE)], BAND, dict(line=1200)),
              (RIGHT, X1, b1, bottom, [], frame(left="soft", bottom=edge), {})]
    ygrid(name, sorted(xs), top, bottom, items)


group("empathy", 390.0, 516.7, (445, 500), 405.0,
      [("tag", 423.3, 423.0, 435.0, 438.0, []), ("dash", 439.0, 438.0, 453.5), ("dash", 454.4, 453.5, 469.0),
       ("tag", 474.9, 474.5, 486.5, 490.0, []), ("dash", 490.6, 490.0, 505.5)],
      (390, 490), ((490.0, 511.0), (380, 495)))
group("access", 516.7, 629.3, (560, 620), 525.4,
      [("tag", 543.8, 543.0, 555.0, 558.0, [(307.5, 362.0, [[("지적사항 개선", 780, True, WHITE)]], STICKER)]),
       ("dash", 559.4, 558.0, 574.0), ("dash", 574.8, 574.0, 589.5),
       ("tag", 595.3, 595.0, 607.0, 610.5, []), ("dash", 610.9, 610.5, 625.0)],
      (516, 604), ((604.0, 625.0), (385, 607)))
group("experience", 629.3, 757.7, (680, 740), 645.8,
      [("tag", 664.1, 663.5, 676.0, 679.0, [(294.0, 320.0, [[("NEW ", 500, True, WHITE), ("신규", 780, True, WHITE)]],
                                             STICKER)]),
       ("dash", 679.8, 679.0, 694.5), ("dash", 695.2, 694.5, 710.0),
       ("tag", 715.7, 715.0, 727.5, 730.5, [(291.0, 311.5, None, frame("#4C4C4C"))]), ("dash", 731.3, 730.5, 746.0)],
      (629, 733), ((733.5, 753.0), (390, 735)), last=True)

# ---------------------------------------------------------------------------
# 주요성과 (text layer; superscripts as small runs)
# ---------------------------------------------------------------------------
g = Grid("result", [X0, 111.7, X1], [3670])
g.put(X0, 111.7, 0, 1, [runs_of(line1(65, 70, 776, 780), WHITE)], frame(DARK, top="mid", bottom="mid", left="mid"))
g.put(111.7, X1, 0, 1, lines_in(115, 120, 767, 790), frame(top="mid", bottom="mid", right="mid"), align="LEFT",
      line=1600)
block(g, 765.0)

kit.flush(803.0)
for sub in L.section.iter(L.q("hp:subList")):
    if len(sub) and any(sub[0] is first for first in TOP):
        sub.set("vertAlign", "TOP")
for number, table in enumerate(L.section.iter(L.q("hp:tbl")), 5001):
    table.set("id", str(number))
for message in WARN:
    print("WARN", message)
print(L.write(target))
