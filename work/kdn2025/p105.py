"""Rebuild KDN 2025 report page 105 (third PDF local page 5, printed page 70) as editable HWPX.

Usage: python3 work/kdn2025/p105.py <report3.pdf> <out.hwpx> [--page 5]

재무성과관리(재무예산관리) section 2 "저성장 위기 속 실적 악화에 대비한 재무위험 관리체계 전면 개선":
가. 재무위험 구조 재진단 diagram and 나. 월 단위 매출 선제관리 (추진방향, ■1 3대 선행지표 발굴,
■2 「위험경보 시스템」 가동, 추진실적). Built with the shared kit (one flat table per band on a grid
of PDF x edges); text from the PDF text layer wherever it exists (나. block, headings, labels).

Images and how they are kept:
- the whole 가. diagram (y 121-348: 위험진단 성장성/수익성/안정성, 시사점, 추진목표, 추진방향, 추진과제)
  is one image: its text was read from 4x renders and typed into cells on the diagram's grid.
  The boxed 위험지표 tags are outlined cells, the Ⅰ Ⅱ Ⅲ circles dark cells, the dark numbered
  squares 1-6 -> ①-⑥, list dots -> "·"; the ▼ notches above 시사점 and the dark tabs are dropped.
- section number band, 'Best Practice' sticker (trophy dropped) and the '지적사항 개선' sticker
  (hand icon dropped): typed dark cells. The Ⅰ circle of the 나. badge: a dark cell.
- the ➡ arrows and ■1 / ■2 squares before text-layer runs -> "→" and ①/②; the round arrow icons
  between the 1-3단계 heads -> ▶; the chevron between 위험인식 and 대응조치 -> ▼.
Kept as printed: the second 추진실적 line is regular weight (the first is bold).
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kit  # noqa: E402
from kit import Layout, recipe_inputs  # noqa: E402

source, target = recipe_inputs(5, "저성장 위기 속 실적 악화에 대비한 재무위험 관리체계 전면 개선")
L = Layout(top=3100)
kit.setup(source, L)
from kit import *  # noqa: E402,F401,F403  helpers and presets bound to this page

SIDE = frame("#EDEDED")          # 추진방향 / ■ labels
SUB = "#E5E5E5"                  # sub labels (발굴과정, 지표명 ...)


def m(text, size=1050, bold=False, color=INK, small=0.82):
    """Typed runs: {..} = smaller run, **..** = bold run."""
    runs = []
    for part in re.split(r"(\{[^}]*\}|\*\*[^*]*\*\*)", text):
        if not part:
            continue
        if part[0] == "{":
            runs.append((part[1:-1], int(round(size * small / 10)) * 10, bold, color))
        elif part.startswith("**"):
            runs.append((part[2:-2], size, True, color))
        else:
            runs.append((part, size, bold, color))
    return runs


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


# ---------------------------------------------------------------------------
# Page chrome (odd page): running head over a rule, side tab, footer at the right.
# ---------------------------------------------------------------------------
L.add_table([[cell(0, 3350, 1680, [para([("01", 1380, True, WHITE)], "CENTER")[0]], dark)],
             [cell(0, 3350, 5960, [para([(ch, 950, True, INK)], "CENTER", 1160)[0] for ch in "경영관리"], gray2)]],
            floating=(57800, 15000))
foot = [(text, size, False, INK) for text, size in (
    (line1(450, 455, 818, 822)["text"], 790), ("    ", 790), (line1(540, 546, 816, 820)["text"], 1090))]
L.add_table([[cell(0, W, 1500, [para(foot, "RIGHT", 1300)[0]])]], floating=(5660, 81550))

g = Grid("head", [X0, 429.5, X1], [1680])
g.put(X0, 429.5, 0, 1, [], frame(bottom="soft"))
g.put(429.5, X1, 0, 1, [line1(430, 440, 35, 40)], align="RIGHT")
block(g, 32.0)

# Section band "2 title [Best Practice]"
g = Grid("section", [X0, 85.5, 472.8, 543.4, X1], [2300])
g.put(X0, 85.5, 0, 1, [runs_of(line1(64, 70, 72, 77), WHITE)], frame("#666666"), line=1800)
g.put(85.5, 472.8, 0, 1, [line1(90, 95, 73, 78)], frame("#E5E5E5"), align="LEFT", line=1700)
g.put(472.8, 543.4, 0, 1, "Best Practice", frame("#3C3C3C"), size=900, bold=True, color=WHITE, line=1050)
tight(g, 472.8, 0, 20, 20)
g.put(543.4, X1, 0, 1, [], frame("#E5E5E5"))
block(g, 70.9)

g = Grid("ga", [X0, X1], [1650])
g.put(X0, X1, 0, 1, [line1(55, 60, 95, 100)], align="LEFT", line=1450)
block(g, 95.6)

# ---------------------------------------------------------------------------
# 가. diagram (one image; text read from 4x renders)
# ---------------------------------------------------------------------------
LX, CX0 = 110.8, 121.0
C3 = ((CX0, 262.2), (267.2, 408.8), (413.8, X1))
RISK = (("성장성", ["· AMI공사, 상제품 매출감소 등", "  사업기반 약화로 성장세 둔화"], "매출액",
         ["목표대비 매출부족 규모에", "대한 상시 인지 · 관리 필요"]),
        ("수익성", ["· 재료비 · 인건비 등 비용 증가로", "  사업환경 악화 및 수익성 저하"], "영업이익률",
         ["수익성 악화 적극 대응을 위한", "전사적 손익 통제 필요"]),
        ("안정성", ["· 고배당 및 투자확대 등 대규모", "  자금수요 증가로 유동성부담 확대"], "유동비율, 부채비율",
         ["실적부진이 유동성 위험으로", "전이되지 않도록 선제관리 필요"]))
xs = [X0, LX]
for a, e in C3:
    xs += [a, a + 10.0, a + 48.0, e]
g = Grid("risk", sorted(set(xs)), [2080, 2860, 1630, 4010])
g.put(X0, LX, 0, 3, "위험진단", frame("#CBCBCB"), size=1050)
g.put(X0, LX, 3, 4, "시사점", frame("#CBCBCB"), size=1050)
body = frame("#EDEDED")
for (a, e), (head, bullets, index, note) in zip(C3, RISK):
    g.put(a, e, 0, 1, head, frame(WHITE, top="strong", left="soft", right="soft"), size=1150)
    put_fit(g, a, e, 1, 2, [m(t) for t in bullets], body, line=1250)
    g.put(a, a + 10.0, 2, 3, [], body)
    g.put(a + 10.0, a + 48.0, 2, 3, "위험지표", frame(WHITE, top="mid", bottom="mid", left="mid", right="mid"),
          size=980, line=1150, fit=False)
    tight(g, a + 10.0, 2, 10, 10)
    g.put(a + 48.0, e, 2, 3, [m(index)], body, align="LEFT", line=1250)
    g.put(a, e, 3, 4, [m(t, 1150) for t in note], frame(WHITE, top="soft", bottom="soft", left="soft",
                                                         right="soft"), line=1450)
block(g, 121.2)

g = Grid("goal", [X0, LX, X1], [450, 2900])
g.put(X0, LX, 1, 2, "추진목표", frame("#B2B2B2"), size=1050, bold=True, color=WHITE)
g.put(LX, X1, 1, 2, "저성장 위기에서도 성장·수익·안정의 균형을 통한 지속성장 실현", frame("#7F7F7F"),
      size=1250, bold=True, color=WHITE)
block(g, 227.0)

PLAN = ((m("“", 1300, True) + m("매출부진 신호를 ", 1050) + m("감지한다", 1250, True) + m("”", 1300, True),
         "Ⅰ", "매출 진단체계 정비", ["① 월 매출관리 선행지표 발굴", "② ERP 위험경보 시스템 가동"]),
        (m("“", 1300, True) + m("손익악화 흐름을 ", 1050) + m("방어한다", 1250, True) + m("”", 1300, True),
         "Ⅱ", "수익성 방어 관리체계 운영", ["③ 전사 손익점검 거버넌스 가동", "④ 영업이익률 관리체계 고도화"]),
        (m("“", 1300, True) + m("자금 유동성은 미리 ", 1050) + m("챙긴다", 1250, True) + m("”", 1300, True),
         "Ⅲ", "자금 운용체계 정비", ["⑤ 현금흐름 기반 자금운용 관리", "⑥ 유동성지수 기반 상시모니터링"]))
xs = [X0, LX]
for a, e in C3:
    xs += [a, a + 16.5, e]
g = Grid("plan", sorted(set(xs)), [2900, 2000, 3200])
g.put(X0, LX, 0, 1, "추진방향", frame(SUB), size=1050)
g.put(X0, LX, 1, 3, "추진과제", frame(SUB), size=1050)
for k, ((a, e), (quote, num, head, items)) in enumerate(zip(C3, PLAN)):
    g.put(a, e, 0, 1, [quote], frame("#F2F2F2", hatch="#E3E3E3"), line=1500)
    g.put(a, a + 16.5, 1, 2, num, frame("#4C4C4C"), size=1100, bold=True, color=WHITE, fit=False)
    tight(g, a, 1, 0, 0)
    g.put(a + 16.5, e, 1, 2, head, frame("#E5E5E5"), size=1150, align="LEFT")
    put_fit(g, a, e, 2, 3, [m(t, 1100) for t in items], frame(left="dot" if k else None), line=1350)
block(g, 264.0)

# ---------------------------------------------------------------------------
# 나. 매출 진단체계 정비 (text layer)
# ---------------------------------------------------------------------------
head = line1(100, 105, 359, 364)
g = Grid("na", [X0, 77.5, 92.0, 188.5, 470.6, 522.7, X1], [1650])
g.put(X0, 77.5, 0, 1, [line1(55, 60, 359, 364)], align="LEFT", line=1450)
g.put(77.5, 92.0, 0, 1, "Ⅰ", frame("#4C4C4C"), size=950, bold=True, color=WHITE, line=1100, fit=False)
tight(g, 77.5, 0, 0, 0)
g.put(92.0, 188.5, 0, 1, [runs_of(head, x1=190)], frame("#E3E3E3"), line=1200)
tight(g, 92.0, 0, 40, 40)
g.put(188.5, 470.6, 0, 1, [strip_runs(runs_of(head, x0=190))], align="LEFT", line=1450)
g.put(470.6, 522.7, 0, 1, "지적사항 개선", frame("#3C3C3C"), size=800, bold=True, color=WHITE, line=950)
tight(g, 470.6, 0, 20, 20)
block(g, 359.4)

# 추진방향: label | rounded gray box: need -> (arrow) ①/② action
g = Grid("direction", [X0, 102.6, 107.6, 372.0, X1], [1860, 1860])
g.put(X0, 102.6, 0, 2, [line1(60, 62, 393, 398)], SIDE)
for r, (y, num) in enumerate(((387.3, "①"), (402.8, "②"))):
    edge = dict(top="soft") if r == 0 else dict(bottom="soft")
    g.put(107.6, 372.0, r, r + 1, [line1(112, 115, y - 1, y + 1)], frame("#EDEDED", left="soft", **edge),
          align="LEFT")
    g.put(372.0, X1, r, r + 1, [[("→ ", 1090, False, INK), (num + " ", 1090, True, INK)]
                                + runs_of(line1(392, 395, y - 1, y + 1))],
          frame("#EDEDED", right="soft", **edge), align="LEFT")
block(g, 382.1)

# ■1 3대 선행지표 발굴: sub labels | 1-3단계 heads with bullets | three indicator boxes
STEP = ((144.5, 159.1, 190.3, 271.1, "#F3F3F3", 164), (286.2, 301.6, 332.8, 411.3, "#E4E4E4", 307),
        (426.5, 429.1, 457.5, X1, "#D2D2D2", 433))
BUL = ((141.7, 273.5, 144.7), (273.5, 413.2, 276.5), (413.2, X1, 416.3))
BOX = ((144.5, 275.2), (283.3, 413.9), (422.0, 552.7))
xs = {X0, 102.6, 104.8, 138.2} | {x for s in STEP for x in s[:4]} | {x for b in BUL for x in b[:2]} \
    | {x for b in BOX for x in b}
g = Grid("indicators", sorted(xs), [1870, 3560, 220, 1890, 3170, 3120, 1900])
g.put(X0, 102.6, 0, 7, [[("①", 1090, True, INK)]] + lines_in(55, 102, 485, 525), SIDE, line=1320)
for r0, r1, y in ((0, 3, 437), (3, 4, 483), (4, 5, 509), (5, 6, 540), (6, 7, 566)):
    g.put(104.8, 138.2, r0, r1, lines_in(105, 138, y - 1, y + 20), frame(SUB), line=1430)
    tight(g, 104.8, r0, 20, 20)
for k, (a, t0, t1, e, fill, tx) in enumerate(STEP):
    step = line1(tx - 1, tx + 1, 425, 430)
    tag = frame("#7F7F7F") if k == 2 else frame(WHITE, top="soft", bottom="soft", left="soft", right="soft")
    g.put(a, t0, 0, 1, [], frame(fill))
    g.put(t0, t1, 0, 1, [runs_of(step, WHITE if k == 2 else INK, x1=t1 - 2)], tag, line=1000, fit=False)
    tight(g, t0, 0, 20, 20)
    g.put(t1, e, 0, 1, [strip_runs(runs_of(step, x0=t1 - 2))], frame(fill), align="LEFT")
    if k < 2:
        g.put(e, STEP[k + 1][0], 0, 1, "▶", size=800, color="#7A7A7A", fit=False)
for k, (a, e, base) in enumerate(BUL):
    put_fit(g, a, e, 1, 2, rows_in(a, e, 444, 475, base), frame(left="dot" if k else None), line=1440)
heads = lines_in(150, 560, 483, 488)
assert len(heads) == 3, [h["text"] for h in heads]
for k, (a, e) in enumerate(BOX):
    g.put(a, e, 3, 4, [heads[k]], frame("#D9D9D9", top="strong", left="mid", right="mid"))
    for r, (y0, y1) in zip((4, 5, 6), ((500, 528), (531, 560), (563, 580))):
        rule = "mid" if r == 6 else "dot"
        g.put(a, e, r, r + 1, lines_in(a, e, y0, y1), frame(bottom=rule, left="mid", right="mid"), line=1320)
block(g, 423.4)

# ■2 「위험경보 시스템」 가동: 위험인식 (시스템 개발 | 가동 결과) ▼ 대응조치 (three columns)
xs = [X0, 102.6, 104.8, 133.3, 138.8, 272.0, 277.1, 315.4, 355.0, 470.0, 270.2, 280.0, 411.4, 414.1, 419.1, X1]
g = Grid("alert", sorted(set(xs)), [1920, 1750, 2750, 1550, 2200, 7530])
g.put(X0, 102.6, 0, 6, [[("②", 1090, True, INK)]] + lines_in(55, 102, 660, 692), SIDE, line=1320)
g.put(104.8, 133.3, 0, 4, lines_in(105, 133, 610, 632), frame("#E6E6E6"), line=1440)
tight(g, 104.8, 0, 20, 20)
g.put(104.8, 133.3, 4, 5, "▼", size=900, color="#9A9A9A", fit=False)
g.put(104.8, 133.3, 5, 6, lines_in(105, 133, 705, 735), frame("#CBCBCB"), line=1440)
tight(g, 104.8, 5, 20, 20)
g.put(138.8, 272.0, 0, 1, [line1(175, 180, 586, 592)], frame("#EDEDED"))
g.put(277.1, X1, 0, 1, [line1(378, 382, 586, 592)], frame("#EDEDED", left="dot"))
for r, (y0, y1) in zip((1, 2, 3), ((604, 619), (620, 648), (649, 664))):
    put_fit(g, 138.8, 272.0, r, r + 1, rows_in(138, 272, y0, y1, 139.1), frame(bottom="dot" if r < 3 else None),
            line=1300 if r != 2 else 1220)
alert = line1(318, 322, 605, 610)
g.put(277.1, 315.4, 1, 2, [], frame("#D2D2D2", left="dot"))
g.put(315.4, 355.0, 1, 2, [runs_of(alert, x1=355)], frame(WHITE, top="soft", bottom="soft", left="soft",
                                                           right="soft"), line=1000, fit=False)
tight(g, 315.4, 1, 20, 20)
g.put(355.0, X1, 1, 2, [strip_runs(runs_of(alert, x0=355))], frame("#D2D2D2"), align="LEFT")
put_fit(g, 277.1, 470.0, 2, 4, rows_in(278, 470, 622, 662, 279.4), frame(left="dot"), line=1320)
put_fit(g, 470.0, X1, 2, 4, [[("→ ", 1090, False, INK)] + runs_of(l) for l in lines_in(480, 490, 622, 662)],
        line=1320)
low = lines_in(170, 460, 670, 676)
assert len(low) == 3, [h["text"] for h in low]
for k, ((a, e), (b0, b1), base) in enumerate(zip(((138.8, 270.2), (280.0, 411.4), (419.1, X1)),
                                                  ((138.8, 272.0), (277.1, 414.1), (419.1, X1)),
                                                  (139.1, 280.2, 421.4))):
    g.put(a, e, 4, 5, [low[k]], frame("#D8D8D8"))
    put_fit(g, b0, b1, 5, 6, rows_in(b0 - 1, b1, 686, 760, base), frame(left="dot" if k else None), line=1380)
block(g, 584.8)

# 추진실적
g = Grid("result", [X0, 102.6, 107.6, X1], [3570])
g.put(X0, 102.6, 0, 1, [line1(60, 62, 776, 782)], frame("#BFBFBF"))
put_fit(g, 107.6, X1, 0, 1, rows_in(110, 120, 768, 795, 113.5),
        frame("#E3E3E3", top="soft", bottom="soft", left="soft", right="soft"), line=1500)
block(g, 766.4)

kit.finish(target, end=802.4)
