"""Rebuild KDN 2025 report page 108 (3rd PDF local page 8, printed page 73) as editable HWPX.

Usage: python3 work/kdn2025/p108.py <report3.pdf> <out.hwpx> [--page 8]

재무성과관리(재무예산관리) 평가내용 02 opening page: section 1 "수주형 사업구조의 한계를 뛰어넘는
수익성 검증 기반 전략적 예산 편성". Built with the shared kit (one flat table per band on a grid of
PDF x edges). In the text layer (taken from it): the 평가내용 title, section band, 가./나. titles,
the 사업구조 분석 / 시사점 / 경영전략･정책 boxes, the 예산운영 방향성 box, the 손익예산 / 투자예산
tables, the 중점심의 lines, the labels 편성검증 / 중점심의 / 주요성과, the 주요성과 box heads and the
page number. Images, typed from 4x-6x renders:
- 평가내용 02 chip (check icon dropped), PART box, KDN logo in the footer (typed 한전KDN㈜).
- rows ① 전략방향 및 경영목표, ② 고려요소, ③ 편성방향 (y 343-481) and the 1차~5차 검증 steps
  (y 485-513): typed into cells on the image's own grid; ❶-❺ -> ①-⑤, the round (+) -> "+",
  the chevrons between steps / boxes -> ▶ ◀, the row-3 arrows ➜ -> →, list dots -> ∙.
- the "지적사항 개선" sticker (hand icon dropped): typed in a dark cell.
- the three 주요성과 bar charts: value cells only ('25 value -> '26 value, the dark increase tag);
  every increase checks: 453->1,203 = 750 (165.6 % ≈ 166 %), 1,213->1,493 = 280 (23.1 %),
  198->248 = 50 (25.3 %). Bars and the curved arrows are not drawn ('→' typed between values).
Printed as in the source: "인상율" (row ③, image text).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kit  # noqa: E402
from kit import Layout, recipe_inputs  # noqa: E402

source, target = recipe_inputs(8, "수주형 사업구조의 한계를 뛰어넘는 수익성 검증 기반 전략적 예산 편성")
L = Layout(top=3100)
kit.setup(source, L)
from kit import *  # noqa: E402,F401,F403  helpers and presets bound to this page

LAB, IN = 114.8, 122.5           # diagram label column end, content start
LABEL, HEAD, LIGHT = "#D9D9D9", "#D9D9D9", "#EDEDED"
DARK = "#5A5A5A"
OUTLINED = frame(WHITE, top="soft", bottom="soft", left="soft", right="soft")
TEXT = 1000                       # diagram (image) body text


def S(text, size=TEXT, bold=False, color=INK):
    return (text, size, bold, color)


def dot(*parts, size=TEXT):
    """'∙ text' bullet; parts are str (body size) or (text, size) for smaller runs."""
    runs = [S("∙", size)]
    for part in parts:
        runs.append(S(part, size) if isinstance(part, str) else S(*part))
    return runs


def flat(g, x0, r0, left=320, right=180):
    """Zero top/bottom padding so a cell fits a thin row."""
    c0 = g.xs.index(to_x(x0))
    item = g.items[r0, c0]
    g.items[r0, c0] = (*item[:7], dict(left=left, right=right, top=0, bottom=0))


def label(g, r0, r1, runs_list, fill=LABEL):
    g.put(X0, LAB, r0, r1, runs_list, frame(fill), line=1300)


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

# 평가내용 02 band: chip (image, typed) in the corner, hatched two-line title.
g = Grid("band", [X0, 124.0, X1], [1950, 2190])
g.put(X0, 124.0, 0, 1, "평가내용 02", frame("#565656", top="strong"), size=970, bold=True, color=WHITE, ratio=80)
g.put(X0, 124.0, 1, 2, [], frame("#E9E9E9", bottom="soft", left="soft", hatch="#DADADA"))
g.put(124.0, X1, 0, 2, lines_in(125, 130, 75, 110), frame("#E9E9E9", top="strong", bottom="soft",
                                                          right="soft", hatch="#DADADA"), align="LEFT", line=1480)
block(g, 70.9)

g = Grid("sec1", [X0, 84.5, X1], [2300])
g.put(X0, 84.5, 0, 1, [runs_of(line1(60, 70, 123, 128), WHITE)], frame("#5F5F5F"), line=1700)
g.put(84.5, X1, 0, 1, [line1(90, 95, 124, 129)], frame("#E5E5E5"), align="LEFT", line=1700)
block(g, 121.6)

g = Grid("title-ga", [X0, X1], [1700])
g.put(X0, X1, 0, 1, [line1(55, 60, 150, 154)], align="LEFT", line=1500)
block(g, 150.5)

# ---------------------------------------------------------------------------
# 가. 사업구조 분석 ▶ 시사점 ◀ 경영전략･정책
# ---------------------------------------------------------------------------
xs = [X0, 135.5, 213.8, 227.6, 384.8, 398.6, X1]
g = Grid("analysis", xs, [1870, 1330, 1320, 1600])
side = dict(left="mid", right="mid")
for a, e in ((X0, 213.8), (227.6, 384.8), (398.6, X1)):
    g.put(a, e, 0, 1, [line1(a, e, 172, 176)], frame(HEAD, top="mid", bottom="soft", **side))
for a, e, edge in ((X0, 135.5, dict(left="mid", right="soft")), (135.5, 213.8, dict(right="mid"))):
    g.put(a, e, 1, 2, [line1(a, e, 190, 194)], frame("#E6E6E6", bottom="soft", **edge))
row1 = line1(60, 65, 203, 207)
g.put(X0, 135.5, 2, 3, [runs_of(row1, x1=137)], frame(left="mid", right="dot", bottom="dot"), align="LEFT")
g.put(135.5, 213.8, 2, 3, [runs_of(row1, x0=137)], frame(right="mid", bottom="dot"), align="LEFT")
g.put(X0, 135.5, 3, 4, [line1(60, 65, 216, 220)], frame(left="mid", right="dot", bottom="mid"), align="LEFT")
g.put(135.5, 213.8, 3, 4, [line1(136, 140, 216, 220)], frame(right="mid", bottom="mid"), align="LEFT")
for a, e in ((227.6, 384.8), (398.6, X1)):
    g.put(a, e, 1, 4, lines_in(a, e, 188, 230), frame(bottom="mid", **side), align="LEFT", line=1320)
g.put(213.8, 227.6, 1, 4, "▶", size=1100, color="#BDBDBD", fit=False)
g.put(384.8, 398.6, 1, 4, "◀", size=1100, color="#BDBDBD", fit=False)
block(g, 170.5)

# 예산운영 방향성: dark tag + system line, three heads (pill tag + name) joined by +, bullets.
direction = line1(60, 70, 243, 247)
heads = ((63.7, 115.0, 140.9, 219.1), (228.9, 280.4, 306.4, 384.4), (394.1, 436.8, 462.7, 549.5))
cols = ((59.5, 224.3, 63.9), (224.3, 389.6, 229.1), (389.6, 552.4, 394.4))
xs = sorted({X0, 59.5, 135.5, X1} | {x for h in heads for x in h} | {x for c in cols for x in c[:2]})
g = Grid("direction", xs, [290, 1560, 560, 1710, 3030, 260])
box = frame(top="mid", left="mid", right="mid")
g.put(X0, X1, 0, 1, [], box)
g.put(X0, 59.5, 1, 5, [], frame(left="mid"))
g.put(59.5, 135.5, 1, 2, [runs_of(direction, WHITE, x1=137)], frame("#4F4F4F"))
g.put(135.5, X1, 1, 2, [strip_runs(runs_of(direction, x0=137))], frame(right="mid"), align="LEFT")
g.put(59.5, X1, 2, 3, [], frame(right="mid"))
for k, (a, p0, p1, e) in enumerate(heads):
    line = line1(p0, p1, 266, 270)
    split = p1 - 2.0
    g.put(a, p0, 3, 4, [], frame(HEAD))
    g.put(p0, p1, 3, 4, [runs_of(line, WHITE, x1=split)], frame("#868686"), line=1000)
    g.put(p1, e, 3, 4, [strip_runs(runs_of(line, x0=split))], frame(HEAD), align="LEFT")
    if k < 2:
        g.put(e, heads[k + 1][0], 3, 4, "+", size=1300, bold=True, color="#9A9A9A", fit=False)
g.put(549.5, X1, 3, 4, [], frame(right="mid"))
for k, (a, e, base) in enumerate(cols):
    sep = dict(right="dot") if k < 2 else dict(right="mid")
    g.put(a, e, 4, 5, lines_in(base - 1, e, 284, 300), frame(**sep), align="LEFT", line=1320)
g.put(552.4, X1, 4, 5, [], frame(right="mid"))
g.put(X0, X1, 5, 6, [], frame(bottom="mid", left="mid", right="mid"))
block(g, 239.9)

# ---------------------------------------------------------------------------
# 나. Align: rows ①-③ (image), ④ 편성검증, ⑤ 중점심의, 주요성과
# ---------------------------------------------------------------------------
title_band("title-na", line1(55, 60, 322, 326), [X0, 76.9, 114.5, X1], 322.1)

r1 = ((IN, 227.8), (231.2, 337.0), (341.0, 445.8), (450.0, X1))
r2 = ((IN, 258.5), (271.5, 407.0), (420.0, X1))
r3 = ((IN, 170.5, 173.1, 205.0, 337.0), (341.0, 389.0, 391.3, 423.7, X1))
xs = sorted({X0, LAB, 265.0, 413.5} | {x for b in r1 for x in b} | {x for b in r2 for x in b}
            | {x for b in r3 for x in b})
hs = [1820, 1710, 400, 1720, 2290, 430, 290, 1250, 1250, 1250, 1100, 240]
g = Grid("rows123", xs, hs)
label(g, 0, 2, [[S("①", 1040), S("전략방향", 1040, True)], [S("및 경영목표", 1040, True)]])
label(g, 3, 5, [[S("② ", 1040), S("고려요소", 1040, True)]])
label(g, 6, 12, [[S("③ ", 1040), S("편성방향", 1040, True)]])
goals = (("디지털 융합", "매출 2조원"), ("사업 다각화", "미래신사업 매출 6천억원"),
         ("ESG 선도", "안전, 상생 가치창출"), ("시스템 경영", "시스템 및 기술혁신"))
for (a, e), (head, value) in zip(r1, goals):
    g.put(a, e, 0, 1, head, frame(top="strong", left="mid", right="mid"), size=1100)
    g.put(a, e, 1, 2, value, frame(LIGHT), size=1050)
factors = (("거시경제 환경", ["환율 등 금융시장 변동성 심화", "경기 둔화 및 사업비 부담 상승"]),
           ("정책 환경", ["AI･에너지전환 등 業 연계 정책 강화", "공공기관 재무건전성 요구 확대"]),
           ("경영 전략", ["사업구조 전환을 위한 투자사업 확대", "기저사업 디지털경쟁력 강화"]))
for k, ((a, e), (head, items)) in enumerate(zip(r2, factors)):
    g.put(a, e, 3, 4, head, frame(HEAD), size=1100, bold=True)
    g.put(a, e, 4, 5, [dot(" " + t) for t in items], align="LEFT", line=1100)
    if k < 2:
        b = r2[k + 1][0]
        mid = 265.0 if k == 0 else 413.5
        g.put(e, b, 3, 4, "+", size=1100, bold=True, color="#7A7A7A", fit=False)
        g.put(e, mid, 4, 5, [], frame(right="dot"))
plans = (("수 익 성", "검증 중심", "손익예산"), ("경 영 전 략", "·사업 연계", "투 자 예 산"))
tagged = ((("사업원가", "사업수익 대응 표준원가율 소요액 검증"), ("고정경비", "사회적 책임 실현 예산 우선 편성"),
           ("영업비용", [S("법정경비 제외 인상율 최소화"), S("(1.1%)", 850)])),
          (("미래사업", "재생E 지분투자, 클라우드 사업인프라"), ("기저사업", "플랫폼 · AI기반 신사업 추진"),
           ("공 공 성", "사업연계 안전, 상생 분야 투자")))
results = ("→ 5단계 검증을 통해 요구안 대비 11% 절감편성", "→ 정책연계 미래사업 투자 중심 20% 확대 편성")
for (a, lab, t0, t1, e), plan, rows, result in zip(r3, plans, tagged, results):
    g.put(a, lab, 6, 12, list(plan), frame("#CBCBCB"), size=1050, bold=True, line=1250)
    g.put(lab, e, 6, 7, [], frame(top="soft", right="soft"))
    for i, (tag, text) in enumerate(rows):
        r = 7 + i
        g.put(lab, t0, r, r + 1, [])
        g.put(t0, t1, r, r + 1, tag, OUTLINED, size=950, line=1050)
        flat(g, t0, r, 40, 40)
        runs = text if isinstance(text, list) else [S(text)]
        g.put(t1, e, r, r + 1, [runs], frame(right="soft"), align="LEFT", line=1150)
        flat(g, t1, r)
    g.put(lab, e, 10, 11, result, frame(right="soft"), align="LEFT", size=TEXT, line=1100)
    flat(g, lab, 10)
    g.put(lab, e, 11, 12, [], frame(bottom="soft", right="soft"))
block(g, 343.5)

# ④ 편성검증: five verification steps (image) and the 손익예산 / 투자예산 tables (text layer).
steps = ((123.0, 181.2), (199.4, 294.2), (313.0, 407.8), (426.5, 481.2), (499.6, 554.5))
panel = [IN, 125.4, 128.2, 174.1, 182.3, 196.3, 350.8, 417.3, 469.4, 550.8, 552.1, 555.9]
xs = sorted({X0, LAB} | {x for s in steps for x in s} | set(panel))
hs = [1380, 1460, 530, 420, 1790, 1410, 1220, 1220, 1220, 430, 1790, 1410, 1220, 1220, 1220, 510]
g = Grid("verify", xs, hs)
label(g, 0, 16, [[S("④ ", 1040)] + runs_of(line1(70, 80, 569, 574))])
step_text = (([S("1차 검증", 1050)], "요구안 검증"),
             ([S("2차 검증", 1050, True, WHITE), S("(신규)", 800, True, WHITE)], "본부별 손익 심의"),
             ([S("3차 검증", 1050), S("(강화)", 800)], [S("손익", 900), S("신설", 600), S("/투자심의위원회", 900)]),
             ([S("4차 검증", 1050)], "경영협의회"), ([S("5차 검증", 1050)], "이사회"))
for k, ((a, e), (head, sub)) in enumerate(zip(steps, step_text)):
    fill = "#5A5A5A" if k == 1 else WHITE
    g.put(a, e, 0, 1, [head], frame(fill, top="soft", left="soft", right="soft", bottom="dot"), line=1150)
    g.put(a, e, 1, 2, [sub if isinstance(sub, list) else [S(sub, 900)]],
          frame(bottom="soft", left="soft", right="soft"), line=1100)
    if k < 4:
        g.put(e, steps[k + 1][0], 0, 2, "▶", size=900, color="#8C8C8C", fit=False)
g.put(IN, X1, 3, 4, [], frame(top="mid", left="mid", right="mid"))
g.put(IN, 125.4, 4, 15, [], frame(left="mid"))
g.put(552.1, X1, 4, 15, [], frame(right="mid"))
g.put(IN, X1, 15, 16, [], frame(bottom="mid", left="mid", right="mid"))
TH = frame("#D7D7D7", top="mid")
for r0, ty in ((4, 524), (10, 597)):
    tag, text = line1(130, 135, ty - 1, ty + 3), line1(185, 190, ty - 1, ty + 3)
    g.put(125.4, 128.2, r0, r0 + 1, [])
    g.put(128.2, 174.1, r0, r0 + 1, [tag], OUTLINED, line=1250)
    g.put(174.1, 182.3, r0, r0 + 1, "▶", size=700, color="#9A9A9A", fit=False)
    if r0 == 10:      # 투자예산 line carries the 지적사항 개선 sticker (image, typed)
        g.put(182.3, 417.3, r0, r0 + 1, [text], frame("#EFEFEF"), align="LEFT")
        g.put(417.3, 469.4, r0, r0 + 1, "지적사항 개선", frame("#3C3C3C"), size=760, bold=True, color=WHITE, line=900)
        g.put(469.4, 552.1, r0, r0 + 1, [], frame("#EFEFEF"))
    else:
        g.put(182.3, 552.1, r0, r0 + 1, [text], frame("#EFEFEF"), align="LEFT")
    hy = ty + 18
    for a, e in ((125.4, 196.3), (196.3, 350.8), (350.8, 552.1)):
        g.put(a, e, r0 + 1, r0 + 2, [line1(a, e, hy - 1, hy + 3)], TH, line=1150)
    for i in range(3):
        r, y = r0 + 2 + i, ty + 31 + 12.2 * i
        last = dict(bottom="mid") if i == 2 else dict(bottom="soft")
        g.put(125.4, 196.3, r, r + 1, [line1(125.4, 196.3, y - 2.5, y + 2.5)], frame("#EBEBEB", **last), line=1150)
        flat(g, 125.4, r)
        g.put(196.3, 350.8, r, r + 1, [line1(196.3, 350.8, y - 2.5, y + 2.5)], frame(**last), line=1150)
        flat(g, 196.3, r)
        g.put(350.8, 552.1, r, r + 1, [line1(350.8, 552.1, y - 3.0, y + 2.5)], frame(left="soft", **last),
              line=1150)
        flat(g, 350.8, r)
block(g, 484.4)

# ⑤ 중점심의: three tagged lines in an outlined panel (text layer).
g = Grid("review", [X0, LAB, IN, 125.4, 128.2, 199.3, 552.1, X1], [470, 1510, 1490, 1510, 290])
label(g, 0, 5, [[S("⑤ ", 1040)] + runs_of(line1(70, 80, 691, 695))])
g.put(IN, X1, 0, 1, [], frame(top="mid", left="mid", right="mid"))
g.put(IN, 128.2, 1, 4, [], frame(left="mid"))
g.put(199.3, X1, 1, 4, [], frame(right="mid")) if False else None
for r, (ty, fill) in zip((1, 2, 3), ((678, "#C8C8C8"), (693, "#DADADA"), (708, "#DADADA"))):
    hits = lines_in(128, 200, ty - 1, ty + 3)
    if len(hits) == 1 and hits[0]["bbox"][2] > 300:          # tag and text in one PDF line
        tag, text = runs_of(hits[0], x1=200), strip_runs(runs_of(hits[0], x0=200))
    else:
        tag = runs_of(line1(128, 200, ty, ty + 3))
        text = runs_of(line1(200, 203, ty - 1, ty + 3))
    g.put(128.2, 199.3, r, r + 1, [tag], frame(fill), line=1050)
    flat(g, 128.2, r, 60, 60)
    g.put(199.3, X1, r, r + 1, [text], frame(right="mid"), align="LEFT", line=1250)
    flat(g, 199.3, r, 200, 300)
g.put(IN, X1, 4, 5, [], frame(bottom="mid", left="mid", right="mid"))
block(g, 672.4)

# 주요성과: three headed boxes with value cells for the bar charts (image).
boxes = ((122.3, 265.1), (267.7, 410.5), (413.0, X1))
charts = (("453억원", "1,203억원", "750억원↑", "(166%↑)"), ("1,213억원", "1,493억원", "280억원↑", "(23%↑)"),
          ("198억원", "248억원", "50억원↑", "(25%↑)"))
xs = sorted({X0, LAB} | {x for a, e in boxes for x in (a, a + 3, a + 45, a + 55, a + 97, e - 2, e)})
g = Grid("results", xs, [2010, 300, 2700, 600, 1400, 340])
label(g, 0, 6, [runs_of(line1(65, 75, 757, 761))])
for (a, e), (v25, v26, rise, pct) in zip(boxes, charts):
    g.put(a, e, 0, 1, [line1(a, e, 731, 735)], frame(top="mid", left="mid", right="mid", bottom="soft"))
    g.put(a, e, 1, 2, [], frame(left="mid", right="mid"))
    g.put(a, a + 3, 2, 5, [], frame(left="mid"))
    g.put(a + 3, a + 45, 2, 3, v25, size=900, line=1000)
    g.put(a + 45, a + 55, 2, 3, "→", size=900, color="#8C8C8C", fit=False)
    g.put(a + 55, a + 97, 2, 3, v26, size=900, bold=True, line=1000)
    g.put(a + 97, e - 2, 2, 3, [[S(rise, 1000, True, WHITE)], [S(pct, 1000, True, WHITE)]], frame("#3C3C3C"),
          line=1150)
    g.put(e - 2, e, 2, 5, [], frame(right="mid"))
    g.put(a + 3, a + 45, 4, 5, "’25년", size=750, line=850)
    g.put(a + 55, a + 97, 4, 5, "’26년", size=750, bold=True, line=850)
    g.put(a, e, 5, 6, [], frame(bottom="mid", left="mid", right="mid"))
block(g, 726.5)

kit.finish(target, end=801.6)
