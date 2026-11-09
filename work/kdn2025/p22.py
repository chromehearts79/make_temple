"""Rebuild KDN 2025 report physical PDF page 22 (printed page 10) as editable HWPX.

Usage: python3 work/kdn2025/p22.py <report.pdf> <out.hwpx> [--page N]

3. AI와 Energy 융합을 통한 사업구조 재편 및 미래성장동력 확보 (even page: PART 01 box, footer left).
Built with work/kdn2025/kit.py (one flat table per band on PDF x edges). Text-layer lines come
from the PDF. Image-only parts (PART box, portfolio icon labels, 3C panel, GE-matrix panel, the
GOOD to GREAT diagram) are typed from 4x renders; icons are omitted, the GE matrix becomes a
3x3 grid of labelled cells and connector graphics become KS X 1001 glyphs (→ ↑ ↗ ▶ ▼).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kit  # noqa: E402
from kit import Layout, recipe_inputs  # noqa: E402

source, target = recipe_inputs(22, "정밀한 사업 포트폴리오 분석을 통한 사업전략 구체화")
L = Layout(top=3100)
kit.setup(source, L)
from kit import *  # noqa: E402,F401,F403  helpers and presets bound to this page

GREY_TXT = "#F2F2F2"
side = dict(left="soft", right="soft")

# ---------------------------------------------------------------------------
# Page chrome (even page): PART 01 box over a rule, page number + company name bottom left.
# ---------------------------------------------------------------------------
foot = [(line1(55, 60, 816, 820)["text"], 1090, False, INK), ("   ", 1090, False, INK),
        ("한전KDN㈜", 1000, True, INK)]
L.add_table([[cell(0, W, 1500, [para(foot, "LEFT", 1300)[0]])]], floating=(5660, 81550))

g = Grid("head", [X0, 102.6, 158.6, X1], [1600])
g.put(X0, 102.6, 0, 1, [[("PART ", 820, False, INK), ("01", 1450, True, "#505050")]], align="LEFT", line=1400,
      fit=False)
g.put(102.6, 158.6, 0, 1, "경영관리", frame("#333333"), size=1080, bold=True, color=WHITE)
g.put(158.6, X1, 0, 1, [], frame(bottom="soft"))
block(g, 31.8)

# Section band: number box + title bar.
g = Grid("section-3", [X0, 84.6, X1], [2300])
g.put(X0, 84.6, 0, 1, [line1(60, 70, 72, 76)], frame("#5A5A5A"), color=WHITE)
g.put(84.6, X1, 0, 1, [line1(90, 95, 72, 77)], frame("#E4E4E4"), align="LEFT")
block(g, 70.9)

# 가. [사업전략] title (number and badge+title are two PDF lines)
ga, title = line1(55, 60, 101, 105), line1(85, 90, 101, 105)
g = Grid("title-ga", [X0, 77.6, 131.0, X1], [1700])
g.put(X0, 77.6, 0, 1, [ga], align="LEFT", line=1450)
g.put(77.6, 131.0, 0, 1, [runs_of(title, x1=130)], pill)
g.put(131.0, X1, 0, 1, [runs_of(title, x0=130)], align="LEFT", line=1450)
block(g, 101.5)

# Portfolio table: three business tabs, icon row (icons omitted, labels typed), three rows.
xs = [X0, 113.4, 116.2, 255.5, 265.0, 404.3, 413.8, 553.1, X1]
g = Grid("portfolio-tabs", xs, [1310, 390])
for a, e, x in ((116.2, 255.5, 158), (265.0, 404.3, 308), (413.8, 553.1, 455)):
    g.put(a, e, 0, 1, [line1(x - 1, x + 1, 127, 131)], frame("#D9D9D9", top="mid", left="mid", right="mid"),
          line=1150)
g.put(113.4, X1, 1, 2, [], frame(top="mid"))
block(g, 127.6)

# Icon labels (image text, read from a 4x render).
pills = [(118.5, 146.0, "발전"), (166.0, 197.0, "송변전"), (217.0, 253.0, "배전/AMI"),
         (269.0, 300.0, "영업"), (319.0, 348.0, "ERP"), (364.0, 404.0, "ICT인프라"),
         (414.0, 451.0, "수소E"), (466.0, 501.0, "재생E"), (515.0, 553.0, "클라우드")]
xs = [X0, 110.6] + [x for a, e, _ in pills for x in (a, e)] + [X1]
g = Grid("portfolio-icons", xs, [2350, 1340])
g.put(X0, 110.6, 0, 2, lines_in(58, 108, 148, 170), gray)
for a, e, text in pills:
    g.put(a, e, 1, 2, text, frame("#DCDCDC"), size=740, bold=True, line=900)
g.put(110.6, X1, 0, 1, [], frame(bottom="dot"))
block(g, 144.6)

xs = [X0, 110.6, 121.0, 156.0, 261.0, 275.5, 309.6, 409.0, 418.0, 458.2, X1]
g = Grid("portfolio-rows", xs, [1700, 1700, 1650])
row = frame(bottom="soft")
rowsep = frame(bottom="soft", right="soft")
for r, y in enumerate((186, 203, 220)):
    g.put(X0, 110.6, r, r + 1, [line1(64, 66, y - 1, y + 1)], gray)
for (a, b, c, e), x in (((110.6, 121.0, 156.0, 261.0), 124), ((261.0, 275.5, 309.6, 409.0), 278),
                        ((409.0, 418.0, 458.2, X1), 420)):
    ln = line1(x - 1, x + 1, 185, 187)
    split = ln["spans"][0]["bbox"][2] + 1
    g.put(a, b, 0, 1, [], row)
    g.put(b, c, 0, 1, [runs_of(ln, x1=split)], frame("#DCDCDC", bottom="soft"))
    g.put(c, e, 0, 1, [runs_of(ln, x0=split)], rowsep if e != X1 else row, align="LEFT")
for (a, e), x in (((110.6, 261.0), 128), ((261.0, 409.0), 267), ((409.0, X1), 425)):
    g.put(a, e, 1, 2, [line1(x - 1, x + 1, 202, 204)], rowsep if e != X1 else row)
g.put(110.6, 409.0, 2, 3, [line1(192, 193, 219, 221)], frame(bottom="mid", right="soft"))
g.put(409.0, X1, 2, 3, [line1(412, 413, 219, 221)], frame(bottom="mid"))
block(g, 183.0)

g = Grid("arrow-3c", [X0, X1], [700])
g.put(X0, X1, 0, 1, "▼", size=650, color="#7A7A7A", line=540)
block(g, 234.0)

# 3C bar: two PDF lines around the 지적사항 개선 tag (image; typed).
g = Grid("bar-3c", [X0, 228.6, 281.0, X1], [1550])
bar = dict(top="mid", bottom="mid")
g.put(X0, 228.6, 0, 1, [line1(59, 60, 243, 246)], frame("#E2E2E2", **bar), align="RIGHT")
g.put(228.6, 281.0, 0, 1, "지적사항 개선", frame("#2E2E2E", **bar), size=740, bold=True, color=WHITE)
g.put(281.0, X1, 0, 1, [line1(281, 282, 243, 246)], frame("#E2E2E2", **bar), align="LEFT")
block(g, 242.8)

# 3C panel and GE-matrix panel: an image in the PDF; text read from a 4x render.
xs = [X0, 170.5, 284.2, 399.5, 402.5, 444.0, 448.0, 478.0, 511.0, X1]
hs = [1450, 600, 900, 1700, 1900, 1100, 1600, 2000]   # edges 266.5 281 287 296 313 332 343 359 379
g = Grid("panel-3c", xs, hs)
cols = [(X0, 170.5, "전력계통사업",
         ["지구 14바퀴(약 58만km)의", "거대한 전력망을 끊김 없이", "감시하고 관리"],
         "→ 한전 송·배전 선로길이", "안전·무정전·고품질"),
        (170.5, 284.2, "ICT운영사업",
         ["한전 및 협력사 1만 8천명이", "함께 사용하는 초대형", "전력시스템을 멈춤 없이 운영"],
         "→ 영업·배전 시스템", "신뢰·무중단·고속처리"),
        (284.2, 399.5, "미래성장사업",
         ["수소와 태양광으로 깨끗한", "전기를 만들고,", "분산에너지를 널리보급"],
         "→ 탄소중립 사업", "친환경·저탄소·분산화")]
for k, (a, e, head, body, note, band) in enumerate(cols):
    sep = "dot" if k < 2 else None
    g.put(a, e, 0, 3, head, frame(bottom="soft", right=sep), size=1100, bold=True)
    g.put(a, e, 3, 6, [[(t, 1050, False, INK)] for t in body], frame("#F4F4F4", right=sep), line=1420)
    g.put(a, e, 6, 7, note, frame("#F4F4F4", right=sep), size=820, color="#3A3A3A", line=1000)
    g.put(a, e, 7, 8, band, frame("#555555", right="soft" if k < 2 else None), size=1220, bold=True, color=WHITE)
# GE matrix: title bar, y-axis label, 3x3 grid with the business bubbles, x-axis label, result pill.
g.put(402.5, X1, 0, 1, [[("포트폴리오별 포지셔닝 재정렬 ", 1000, True, WHITE), ("지적사항 개선", 700, True, WHITE)]],
      frame("#6A6A6A"), line=1150)
g.put(402.5, 444.0, 1, 6, [[("시장", 950, False, INK)], [("매력도", 950, False, INK)], [("+", 800, True, INK)],
                           [("전략·정책", 950, False, INK)], [("부합도", 950, False, INK)]],
      frame(top="soft", bottom="soft", **side), line=1050)
for r in range(1, 6):
    g.put(444.0, 448.0, r, r + 1, [], frame(right="mid"))
g.put(448.0, 478.0, 1, 2, "High", size=550, align="LEFT", color="#3A3A3A", line=440, fit=False)
g.put(448.0, 511.0, 2, 4, [[("미래성장사업", 850, True, WHITE)], [("↑ 기존", 750, False, WHITE)]],
      frame("#7C7C7C", bottom="soft", right="soft", hatch="#9A9A9A"), line=950)
g.put(511.0, X1, 2, 4, [[("전력계통", 800, True, WHITE)], [("사업", 800, True, WHITE)], [("↗ 기존", 700, False, WHITE)]],
      frame("#7C7C7C", bottom="soft"), line=800)
g.put(448.0, 478.0, 4, 5, [], frame("#ECECEC", bottom="soft", right="soft"))
g.put(478.0, X1, 4, 5, [[("ICT운영사업", 850, True, INK)], [("↗ 기존", 750, False, INK)]],
      frame("#C8C8C8", bottom="soft"), line=860)
g.put(448.0, 478.0, 5, 6, "Low", frame(bottom="mid"), size=600, align="LEFT", color="#3A3A3A", line=600)
g.put(478.0, X1, 5, 6, [], frame("#ECECEC", bottom="mid"))
g.put(402.5, X1, 6, 7, [[("기술경쟁력", 900, False, INK), (" + ", 800, True, INK), ("시장진입장벽", 900, False, INK),
                         ("  High", 650, False, "#3A3A3A")]], line=1050)
g.put(402.5, X1, 7, 8, "高성장·高부가영역 중심으로 전환", frame("#5E5E5E"), size=1000, color=WHITE)
block(g, 266.5)

# 추진방향 / 전략과제 / 핵심사업 block.
xs = [X0, 88.2, 92.0, 95.5, 115.0, 125.0, 126.0, 138.0, 150.5, 156.5, 168.5, 245.5, 250.0, 259.3, 263.0,
      269.4, 275.0, 289.0, 313.0, 315.5, 327.5, 401.5, 404.5, 416.0, 424.0, 442.5, 467.0, X1]
hs = [1870, 1870, 3670, 640, 1570, 1560, 820, 1910, 1980]
g = Grid("direction", xs, hs)
for (r0, r1), y in (((0, 3), 421), ((4, 6), 484.5), ((7, 9), 527)):
    g.put(X0, 88.2, r0, r1, lines_in(60, 85, y - 1, y + 16), frame("#D4D4D4"), bold=True, line=1320)
heads = [(92.0, 125.0, 150.5, 245.5, 131), (259.3, 289.0, 313.0, 401.5, 293), (416.0, 442.5, 467.0, X1, 447)]
hdr = "#DCDCDC"
for a, b0, b1, e, x in heads:
    ln = line1(x - 1, x + 1, 399, 401)
    split = ln["spans"][0]["bbox"][2] + 1
    g.put(a, b0, 0, 1, [], frame(hdr, top="mid"))
    g.put(b0, b1, 0, 1, [runs_of(ln, x1=split)], frame(WHITE, top="soft", bottom="soft", left="soft", right="soft"))
    g.put(b1, e, 0, 1, [runs_of(ln, x0=split)], frame(hdr, top="mid"), align="LEFT")
for a, e in ((245.5, 259.3), (401.5, 416.0)):
    g.put(a, e, 0, 1, "▶", size=900, color="#8A8A8A")
for (a, e), x in (((92.0, 245.5), 104), ((245.5, 401.5), 257), ((401.5, X1), 419)):
    g.put(a, e, 1, 2, [line1(x, x + 1, 418, 420)], frame("#ECECEC", right="soft" if e != X1 else None),
          bold=True)
for (a, e), x in (((92.0, 245.5), 104.9), ((245.5, 401.5), 261.2), ((401.5, X1), 417.5)):
    first, second = lines_in(x - 0.5, x + 0.5, 436, 465)
    g.put(a, e, 2, 3, [[("→ ", 1000, True, "#505050")] + runs_of(first), [("    ", 1090, False, INK)] + runs_of(second)],
          frame(bottom="soft", right="soft" if e != X1 else None), align="LEFT", line=1400)
# 전략과제: two numbered lines per column, numbers in outlined tags.
for (a, b, c, e), x in (((92.0, 95.5, 115.0, 245.5), 98.4), ((245.5, 250.0, 269.4, 401.5), 252.9),
                        ((401.5, 404.5, 424.0, X1), 407.4)):
    for r, ln in zip((4, 5), lines_in(x - 0.5, x + 0.5, 478, 496)):
        top, bot = ("soft", None) if r == 4 else (None, "soft")
        split = ln["spans"][0]["bbox"][2] + 1
        g.put(a, b, r, r + 1, [], frame(top=top, bottom=bot, left="soft"))
        g.put(b, c, r, r + 1, [runs_of(ln, x1=split)], frame("#F0F0F0", top=top, bottom=bot), fit=False)
        g.put(c, e, r, r + 1, [runs_of(ln, x0=split)], frame(top=top, bottom=bot, right="soft"), align="LEFT")
# 핵심사업: G / E / R on the first line, A / T on the second; letters in dark tags.
tag = frame("#5A5A5A")
first = [(92.0, 126.0, 138.0, 245.5, 128.2), (245.5, 263.0, 275.0, 401.5, 265.4), (401.5, 404.5, 416.0, X1, 407.3)]
for k, (a, b, c, e, x) in enumerate(first):
    ln = line1(x - 0.5, x + 0.5, 520, 522)
    split = ln["spans"][0]["bbox"][2] + 1
    edge = dict(top="soft", bottom="dot")
    if k == 0:
        g.put(a, b, 7, 8, [], frame(left="soft", **edge))
    elif b > a:
        g.put(a, b, 7, 8, [], frame(**edge))
    g.put(b, c, 7, 8, [runs_of(ln, WHITE, x1=split)], frame("#5A5A5A", **edge))
    g.put(c, e, 7, 8, [runs_of(ln, x0=split)], frame(right="soft", **edge), align="LEFT")
ln = line1(158, 159, 538, 541)
spans = [s["bbox"][0] for s in ln["spans"]]
t_at = next(x for x, s in zip(spans, ln["spans"]) if s["text"].strip() == "T")
g.put(92.0, 156.5, 8, 9, [], frame(left="soft", bottom="soft"))
g.put(156.5, 168.5, 8, 9, [runs_of(ln, WHITE, x1=160)], frame("#5A5A5A", bottom="soft"))
g.put(168.5, 315.5, 8, 9, [runs_of(ln, x0=160, x1=t_at - 1)], frame(bottom="soft"), align="LEFT")
g.put(315.5, 327.5, 8, 9, [runs_of(ln, WHITE, x0=t_at - 1, x1=t_at + 1)], frame("#5A5A5A", bottom="soft"))
g.put(327.5, X1, 8, 9, [runs_of(ln, x0=t_at + 1)], frame(right="soft", bottom="soft"), align="LEFT")
block(g, 396.2)

# 나. [사업전략] “GOOD to GREAT” title (one PDF line)
title_band("title-na", line1(55, 60, 565, 569), [X0, 78.0, 127.0, X1], 565.6)

# GOOD to GREAT diagram: an image in the PDF; text read from a 4x render.
xs = [X0, 154.5, 181.1, 240.8, 245.8, 254.8, 255.5, 270.5, 284.5, 299.8, 313.8, 329.0, 343.0,
      356.7, 358.7, 372.7, 384.2, 400.0, 404.0, 416.0, 457.5, X1]
hs = [1500, 2050, 1200, 1800, 1700, 1600, 1600,
      1860, 1340, 520, 1860, 820, 1040, 1860]   # 590 605 625.5 637.5 655.5 672.5 688.5 704.5 / 708.. 801
g = Grid("good-to-great", xs, hs)
for (a, e), letter in zip(((240.8, 254.8), (270.5, 284.5), (299.8, 313.8), (329.0, 343.0), (358.7, 372.7)), "GREAT"):
    g.put(a, e, 0, 1, letter, frame("#5E5E5E"), size=950, bold=True, color=WHITE, line=1050)
g.put(245.8, 372.7, 1, 2, [], frame(top="mid"))
themes = [("G", "rid", "차세대 전력망"), ("R", "enewable Energy", "재생E 신사업"), ("E", "nergy Platform", "E-플랫폼"),
          ("A", "rtificial Intelligence", "에너지 AI"), ("T", "otal Energy ICT", "E-ICT 통합 솔루션")]
for k, ((a, e), (cap, rest, kor)) in enumerate(zip(((X0, 154.5), (154.5, 255.5), (255.5, 356.7), (356.7, 457.5),
                                                    (457.5, X1)), themes)):
    sep = "dot" if k < 4 else None
    g.put(a, e, 2, 3, [[(cap, 820, True, WHITE), (rest, 780, False, GREY_TXT)]], frame("#6E6E6E", right=sep), line=900)
    g.put(a, e, 3, 4, kor, frame("#E6E6E6", right=sep), size=1100, bold=True)
g.put(X0, X1, 4, 5, "좋은 기업(GOOD)에서 위대한(GREAT) 기업으로의 도약을 위한 “GREAT” 테마별 14개 핵심사업 선정",
      frame(top="soft", bottom="soft", **side), size=1050)
g.put(X0, 181.1, 5, 6, "“GOOD” (Vision 2030)", frame("#E9E9E9", right="dot"), size=1000)
g.put(181.1, 245.8, 5, 6, "to", frame("#DCDCDC", right="dot"), size=1000)
g.put(245.8, X1, 5, 6, "“GREAT”(Vision 2035)", frame("#C4C4C4"), size=1000)
g.put(X0, 181.1, 6, 7, "에너지ICT 플랫폼 기반 구축", frame(bottom="soft", right="dot"), size=950, bold=True)
g.put(181.1, 245.8, 6, 7, "Vision", frame(bottom="soft", right="dot"), size=950, bold=True)
g.put(245.8, X1, 6, 7, "AI와 에너지융합 기반 글로벌 선도기업 도약", frame(bottom="soft"), size=950, bold=True)
stages = [((7, 9), [("클라우드", "개별 ICT 플랫폼 중심 서비스"), ("AX", "(디지털 혁신)"),
                    ("AX · DX 주도", "AI와 에너지 융합을 통한 전력산업 혁신")]),
          ((9, 12), [("고객지원", "그룹사 수주기반 사업 추진"), ("Energy", "(에너지 대전환)"),
                     ("에너지 대전환 선도", "분산 전원 확대 및 에너지 생태계 주도")]),
          ((12, 14), [("국내시장", "국내 중심 안정적 서비스 제공"), ("Global", "(글로벌 중심)"),
                      ("해외시장 도약", "ICT 솔루션 협업 신시장 확대")])]
for (r0, r1), items in stages:
    last = r1 == 14
    fill = "#E9E9E9" if last else None
    for (a, e), (head, sub) in zip(((X0, 181.1), (181.1, 245.8), (245.8, 384.2)), items):
        g.put(a, e, r0, r1, [[(head, 1050, True, INK)], [(sub, 860, False, INK)]],
              frame(fill, bottom="mid" if last else "soft", right="dot" if e < 384 else None), line=1150)
g.put(384.2, 400.0, 7, 14, [[(t, 950, True, WHITE)] for t in ("14", "개", "핵", "심", "사", "업")],
      frame("#A0A0A0", bottom="mid"), line=1080)
items = [("G", "AI 기반 전력망통합 운영 플랫폼 등 ", "2개"), ("R", "수소 全주기에너지ICT 플랫폼 등 ", "4개"),
         ("E", "클라우드 기반 K-ECP 플랫폼 서비스 등 ", "2개"), ("A", "AI 거점 데이터센터(K-AIDC) 등 ", "3개"),
         ("T", "분산형 토탈 에너지 패키지 사업 등 ", "3개")]
for (r0, r1), (letter, text, count) in zip(((7, 8), (8, 10), (10, 11), (11, 13), (13, 14)), items):
    edge = dict(bottom="mid") if r1 == 14 else {}
    g.put(404.0, 416.0, r0, r1, letter, frame("#4A4A4A", **edge), size=950, bold=True, color=WHITE, line=1050)
    g.put(416.0, X1, r0, r1, [[(text, 1000, False, INK), (count, 1050, True, INK)]], frame(**edge), align="LEFT")
block(g, 590.0)


def check_edges():
    """Every inner column edge of a band must be a cell boundary, or its width is undefined."""
    for grid, _ in kit.BLOCKS:
        used = {0, len(grid.xs) - 1}
        for (r, c0), item in grid.items.items():
            used.update((c0, c0 + item[6]))
        for c in range(len(grid.xs)):
            if c not in used:
                print(f"WARN {grid.name}: unused edge x={X0 + grid.xs[c] / 100:.1f}")


check_edges()
kit.finish(target, end=803.0)
