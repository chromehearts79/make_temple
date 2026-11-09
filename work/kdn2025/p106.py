"""Rebuild KDN 2025 report page 106 (third PDF local page 6, printed page 71) as editable HWPX.

Usage: python3 work/kdn2025/p106.py <report3.pdf> <out.hwpx> [--page 6]

재무성과관리(재무예산관리) section 2 continued: 다. 수익성 악화 위험 대응을 위한 전사 수익관리 체계
강화 (추진방향, ■3 「손익점검 거버넌스」, ■4 영업이익률 관리체계 고도화, 추진실적) and 라. 현금흐름
예측･유동성 관리 내실화 (추진방향, ■5 자금운용 선제관리, ■6 유동성지수 모니터링, 추진실적), then the
주요성과 box. Built with the shared kit (one flat table per band on a grid of PDF x edges); all
running text, labels and tags come from the PDF text layer.

Images / vector art and how they are kept:
- the Ⅱ / Ⅲ circles of the 다. / 라. badges, the dark ■3-■6 squares (-> ③-⑥ in the label column
  and after the ➡ arrows of 추진방향, the arrows -> "→"), the '지적사항 개선' sticker (hand icon
  dropped): typed cells / glyphs; the grey chevrons between the ■4 columns -> ▶.
- the "KDN유동성지수 점검결과" line chart (vector drawing, no text layer): its title, the five
  printed values and the month axis were read from a 7x render and typed as value cells, each
  value in a row near its plotted height (366.4% 1월, 315.1% 3월, 123.4% 6월, 87.8% 9월,
  122.9% 12월); the line and markers are dropped.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kit  # noqa: E402
from kit import Layout, recipe_inputs  # noqa: E402

source, target = recipe_inputs(6, "수익성 악화 위험 대응을 위한 전사 수익관리 체계 강화")
L = Layout(top=3100)
kit.setup(source, L)
from kit import *  # noqa: E402,F401,F403  helpers and presets bound to this page

LX, BX = 102.6, 107.6            # label column end, content box start
SIDE = frame("#EDEDED")
RESULT = frame("#BFBFBF")
BOXED = dict(left="soft", right="soft")


def rows_in(x0, x1, y0, y1, base):
    """Text rows of a region: fragments of one visual row are merged, indents kept as spaces."""
    hits = sorted((l for l in LINES if x0 <= l["bbox"][0] < x1 and y0 <= l["bbox"][1] < y1),
                  key=lambda l: (l["bbox"][1], l["bbox"][0]))
    groups = []
    for l in hits:
        for grp in groups:
            top, bottom = min(g["bbox"][1] for g in grp), max(g["bbox"][3] for g in grp)
            if l["bbox"][1] < bottom - 2 and l["bbox"][3] > top + 2:
                grp.append(l)
                break
        else:
            groups.append([l])
    out = []
    for grp in groups:
        grp.sort(key=lambda l: l["bbox"][0])
        runs = []
        for r in (r for l in grp for r in runs_of(l)):
            if runs and runs[-1][1:] == r[1:]:
                runs[-1] = (runs[-1][0] + r[0], *r[1:])
            else:
                runs.append(r)
        size = runs[0][1] / 100
        raw = "".join(s["text"] for s in grp[0]["spans"])
        offset = grp[0]["bbox"][0] - base + (len(raw) - len(raw.lstrip(" "))) * 0.29 * size
        n = max(0, round(offset / (0.29 * size)))
        if n:
            runs = [(" " * n, runs[0][1], False, INK)] + runs
        out.append(runs)
    return out


def put_fit(g, x0, x1, r0, r1, pars, fill="1", line=1300, align="LEFT", ratio=90):
    """Like Grid.put, but 장평 is fitted per paragraph (one tight line does not shrink the cell)."""
    g.put(x0, x1, r0, r1, pars, fill, align=align, line=line, ratio=ratio, fit=False)
    c0 = g.xs.index(to_x(x0))
    item = g.items[r0, c0]
    inner = (item[1] - 500) / 100 * 0.96
    contents = []
    for runs in pars:
        need = text_width(runs, ratio)
        fitted = int(ratio * inner / need) if need > inner else ratio
        if fitted < 68:
            WARN.append(f"{g.name}: ratio {fitted} for {runs[0][0][:20]!r}")
        contents.append(para(runs, align, line, fitted)[0])
    g.items[r0, c0] = (item[0], item[1], item[2], contents, *item[4:])


def tight(g, x0, r0, left=40, right=40):
    c0 = g.xs.index(to_x(x0))
    item = g.items[r0, c0]
    g.items[r0, c0] = (*item[:7], dict(left=left, right=right))


def side_label(g, r1, num, y0, y1, fill=SIDE):
    """Label column: ③-⑥ (dark squares in the PDF) over the text-layer label lines."""
    lines = lines_in(55, LX, y0, y1)
    pars = ([[(num, 1090, True, INK)]] if num else []) + [runs_of(l) for l in lines]
    g.put(X0, LX, 0, r1, pars, fill, line=1500 if num else 1300)
    tight(g, X0, 0, 20, 20)


def badge_heading(name, lead, line, split, circle, top, pill_end):
    """'다. (Ⅱ badge) title': number, dark circle cell, light pill with the badge text, 14pt title."""
    g = Grid(name, [X0, 76.9, 92.0, pill_end, X1], [1640])
    g.put(X0, 76.9, 0, 1, [lead], align="LEFT", line=1450)
    g.put(76.9, 92.0, 0, 1, circle, frame("#4C4C4C"), size=950, bold=True, color=WHITE, line=1100, fit=False)
    tight(g, 76.9, 0, 0, 0)
    badge = [r for r in runs_of(line) if r[1] < 1300] if split is None else runs_of(line, x1=split)
    g.put(92.0, pill_end, 0, 1, [strip_runs(badge)], frame("#E3E3E3"), line=1200)
    tight(g, 92.0, 0, 40, 40)
    title = runs_of(line, x0=split) if split is not None else None
    return g, title


def direction(name, top, label_y, rows, split, hs):
    """추진방향: label | gray box, need (bullet) -> (arrow, ③-⑥) action per row."""
    g = Grid(name, [X0, LX, BX, split, X1], hs)
    g.put(X0, LX, 0, 2, [line1(60, 62, label_y - 1, label_y + 1)], SIDE)
    for r, (y, x_right, num) in enumerate(rows):
        edge = dict(top="soft") if r == 0 else dict(bottom="soft")
        g.put(BX, split, r, r + 1, [line1(112, 115, y - 1, y + 1)], frame("#EDEDED", left="soft", **edge),
              align="LEFT")
        g.put(split, X1, r, r + 1, [[("→ ", 1090, False, INK), (num + " ", 1090, True, INK)]
                                    + runs_of(line1(x_right - 1, x_right + 1, y - 1, y + 1))],
              frame("#EDEDED", right="soft", **edge), align="LEFT")
    block(g, top)


def result_box(name, top, label_y, y0, y1, height):
    g = Grid(name, [X0, LX, BX, X1], [height])
    g.put(X0, LX, 0, 1, [line1(60, 62, label_y - 1, label_y + 1)], RESULT)
    put_fit(g, BX, X1, 0, 1, rows_in(110, 120, y0, y1, 113.5),
            frame("#E5E5E5", top="soft", bottom="soft", left="soft", right="soft"), line=1540)
    block(g, top)


# ---------------------------------------------------------------------------
# Page chrome (even page): PART label at the left of a rule; footer at the left.
# ---------------------------------------------------------------------------
foot = [(line1(55, 60, 815, 822)["text"], 1090, False, INK), ("   ", 1090, False, INK),
        ("한전KDN㈜", 1090, True, INK)]   # the logo is an image; its name is typed
L.add_table([[cell(0, W, 1500, [para(foot, "LEFT", 1300)[0]])]], floating=(5660, 81550))

g = Grid("part-head", [X0, 103.0, 158.5, X1], [1500])
g.put(X0, 103.0, 0, 1, [[("PART ", 800, False), ("01", 1300, True)]], line=1300)
g.put(103.0, 158.5, 0, 1, "경영관리", frame("#333333"), size=1080, bold=True, color=WHITE)
g.put(158.5, X1, 0, 1, [], frame(bottom="soft"))
block(g, 32.0)

# ---------------------------------------------------------------------------
# 다. 수익성 방어 관리체계 운영
# ---------------------------------------------------------------------------
g, _ = badge_heading("da", line1(55, 60, 71, 75), line1(103, 106, 72, 76), None, "Ⅱ", 70.7, 225.5)
g.put(225.5, X1, 0, 1, [line1(226, 229, 71, 75)], align="LEFT", line=1450)
block(g, 70.7)

direction("dir-3", 93.5, 106.5, ((98.7, 405.6, "③"), (114.1, 405.6, "④")), 382.0, [1820, 1820])

# ■3 「손익점검 거버넌스」: three columns (dark tag + title, bullets, gray result footer)
COLS = ((BX, 108.4, 125.6, 250.7, 110.7), (258.7, 270.7, 287.6, 401.8, 261.8),
        (409.8, 416.1, 433.2, 552.8, 412.9))
xs = {X0, LX, X1} | {x for c in COLS for x in c[:4]}
g = Grid("governance", sorted(xs), [1830, 10200, 2050, 260])
side_label(g, 4, "③", 195, 225)
heads = sorted(lines_in(105, 560, 137, 142), key=lambda l: l["bbox"][0])
foots = sorted(lines_in(105, 560, 258, 262), key=lambda l: l["bbox"][0])
assert len(heads) == 3 and len(foots) == 3, ([h["text"] for h in heads], [f["text"] for f in foots])
for k, (a, t0, t1, e, base) in enumerate(COLS):
    head = heads[k]
    if t0 > a:
        g.put(a, t0, 0, 1, [], frame(top="strong", left="soft"))
    g.put(t0, t1, 0, 1, [runs_of(head, WHITE, x1=t1 - 1)], frame("#7E7E7E", top="strong"), line=1000,
          fit=False)
    tight(g, t0, 0, 10, 10)
    put_fit(g, t1, e, 0, 1, [strip_runs(runs_of(head, x0=t1 - 1))], frame(top="strong", right="soft"),
            line=1300, align="LEFT")
    tight(g, t1, 0, 60, 20)
    put_fit(g, a, e, 1, 2, rows_in(a, e + 5, 157, 250, base), frame(**BOXED), line=1580)
    g.put(a, e, 2, 3, [foots[k]], frame("#E6E6E6", bottom="soft", **BOXED))
block(g, 134.7)

# ■4 영업이익률 관리체계 고도화: title band (+ sticker), 기존 ▶ 한계 ▶ 개선 columns
SUBS = ((110.5, 244.2, 113.6), (263.6, 397.3, 266.6), (416.6, 550.3, 419.7))
xs = {X0, LX, BX, 205.0, 396.3, 448.4, X1} | {x for s in SUBS for x in s[:2]}
g = Grid("margin", sorted(xs), [2030, 150, 1720, 7130, 300])
side_label(g, 5, "④", 315, 370)
band = frame("#D9D9D9", top="soft")
g.put(BX, 205.0, 0, 1, [], frame("#D9D9D9", top="soft", left="soft"))
put_fit(g, 205.0, 396.3, 0, 1, [runs_of(line1(210, 215, 285, 290))], band, align="RIGHT")
g.put(396.3, 448.4, 0, 1, "지적사항 개선", frame("#3C3C3C"), size=800, bold=True, color=WHITE, line=950)
tight(g, 396.3, 0, 20, 20)
g.put(448.4, X1, 0, 1, [], frame("#D9D9D9", top="soft", right="soft"))
subs = sorted(lines_in(140, 520, 305, 310), key=lambda l: l["bbox"][0])
assert len(subs) == 3, [s["text"] for s in subs]
for k, (a, e, base) in enumerate(SUBS):
    g.put(a, e, 2, 3, [subs[k]], frame("#E5E5E5"))
    put_fit(g, a, e, 3, 4, rows_in(a, e + 5, 325, 390, base), frame("#F7F7F7"), line=1530)
    if k < 2:
        g.put(e, SUBS[k + 1][0], 3, 4, "▶", size=1200, color="#BDBDBD", fit=False)
g.put(BX, X1, 4, 5, [], frame(bottom="soft", **BOXED))
block(g, 282.2)

result_box("result-da", 399.7, 413.4, 403, 430, 3830)

# ---------------------------------------------------------------------------
# 라. 자금 운용체계 정비
# ---------------------------------------------------------------------------
line = line1(102, 104, 449, 454)
g, title = badge_heading("ra", line1(55, 60, 449, 454), line, 190.0, "Ⅲ", 449.1, 191.3)
g.put(191.3, X1, 0, 1, [strip_runs(title)], align="LEFT", line=1450)
block(g, 449.1)

direction("dir-5", 471.9, 484.2, ((476.4, 412.7, "⑤"), (491.9, 412.7, "⑥")), 386.0, [1780, 1780])

# ■5 자금운용 선제관리: three gray-headed boxes
COLS5 = ((BX, 250.8, 110.7), (258.8, 401.9, 261.8), (410.0, 553.1, 413.0))
xs = {X0, LX, X1} | {x for c in COLS5 for x in c[:2]}
g = Grid("cash", sorted(xs), [1900, 3740])
side_label(g, 2, "⑤", 530, 555)
heads = sorted(lines_in(130, 560, 514, 520), key=lambda l: l["bbox"][0])
assert len(heads) == 3, [h["text"] for h in heads]
for k, (a, e, base) in enumerate(COLS5):
    put_fit(g, a, e, 0, 1, [runs_of(heads[k])], frame("#D9D9D9", top="strong", **BOXED), align="CENTER")
    put_fit(g, a, e, 1, 2, rows_in(a, e + 5, 533, 565, base), frame(bottom="soft", **BOXED), line=1550)
block(g, 511.8)

# ■6 유동성지수 모니터링: title + note, four stage boxes (dark number tag), value-cell chart
ST = ((BX, 130.0, 262.8, 113.5, 117.3), (266.4, 289.0, 421.6, 272.3, 276.1))
CH = [425.2 + 25.5 * k for k in range(5)] + [X1]
xs = {X0, LX, BX, X1} | {x for s in ST for x in s[:3]} | set(CH)
g = Grid("liquidity", sorted(xs), [2070, 240, 1730, 1680, 1800, 480, 1660, 2160, 1300, 250])
side_label(g, 10, "⑥", 620, 660)
g.put(BX, CH[1], 0, 1, [line1(212, 216, 574, 579)], frame(top="soft", bottom="dot", left="soft"), align="RIGHT")
g.put(CH[1], X1, 0, 1, [line1(453, 457, 577, 582)], frame(top="soft", bottom="dot", right="soft"),
      align="RIGHT")
tag = frame("#767676")
body = frame("#E4E4E4")
for r_head, r_body, y_head in ((2, 3, 597), (6, 7, 653)):
    for a, t1, e, base, tx in ST:
        num = line1(tx - 1, tx + 1, y_head - 2, y_head + 2)
        g.put(a, t1, r_head, r_head + 1, [runs_of(num, WHITE)], tag, line=1000, fit=False)
        g.put(t1, e, r_head, r_head + 1, [line1(t1 + 6, t1 + 10, y_head - 1, y_head + 3)], align="LEFT")
        put_fit(g, a, e, r_body, r_body + 2, rows_in(a, e, y_head + 15, y_head + 40, base), body, line=1450)
# chart panel: bullet, title band, values at their plotted heights, month axis (typed)
panel = frame("#F3F3F3")
g.put(425.2, X1, 2, 3, [line1(427, 430, 596, 600)], align="LEFT")
g.put(425.2, X1, 3, 4, "KDN유동성지수 점검결과", frame("#CBCBCB"), size=1000)
VALUES = (("366.4%", 4, 5), ("315.1%", 5, 7), ("123.4%", 6, 7), ("87.8%", 7, 8), ("122.9%", 6, 7))
for k, (value, r0, r1) in enumerate(VALUES):
    a, e = CH[k], CH[k + 1]
    for r in range(4, 8):
        if r < r0 or r >= r1:
            g.put(a, e, r, r + 1, [], panel)
    g.put(a, e, r0, r1, value, panel, size=800, line=950)
    tight(g, a, r0, 0, 0)
    g.put(a, e, 8, 9, f"{(1, 3, 6, 9, 12)[k]}월", frame("#F3F3F3", top="soft"), size=850, line=1000)
    tight(g, a, 8, 0, 0)
g.put(BX, X1, 9, 10, [], frame(bottom="soft", **BOXED))
block(g, 571.8)

# 추진실적: label | gray box holding a two-column table (dark heads)
g = Grid("result-ra", [X0, LX, BX, 113.0, 328.5, 330.5, 551.5, X1], [470, 1670, 2280, 460])
g.put(X0, LX, 0, 4, [line1(60, 62, 727, 731)], RESULT)
box = "#E5E5E5"
g.put(BX, X1, 0, 1, [], frame(box, top="soft", left="soft", right="soft"))
g.put(BX, 113.0, 1, 3, [], frame(box, left="soft"))
g.put(551.5, X1, 1, 3, [], frame(box, right="soft"))
g.put(328.5, 330.5, 1, 3, [], frame(box))
g.put(BX, X1, 3, 4, [], frame(box, bottom="soft", left="soft", right="soft"))
for (a, e), hx, vx, vy in (((113.0, 328.5), 201.2, 128.8, 735.3), ((330.5, 551.5), 417.7, 351.7, 737.9)):
    g.put(a, e, 1, 2, [runs_of(line1(hx - 1, hx + 1, 716, 720), WHITE)], frame("#7E7E7E"))
    g.put(a, e, 2, 3, [line1(vx - 1, vx + 1, vy - 1, vy + 1)], frame(WHITE))
block(g, 709.8)

# 주요성과
g = Grid("key", [X0, 111.7, 114.7, X1], [3720])
g.put(X0, 111.7, 0, 1, [runs_of(line1(65, 68, 776, 780), WHITE)], frame("#7F7F7F", top="soft", bottom="soft",
                                                                            left="soft"))
put_fit(g, 114.7, X1, 0, 1, rows_in(115, 125, 768, 795, 117.8),
        frame(top="soft", bottom="soft", left="soft", right="soft"), line=1540)
block(g, 764.9)

kit.finish(target, end=802.4)
