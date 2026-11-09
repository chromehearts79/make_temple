"""Rebuild KDN 2025 report physical PDF page 26 (printed page 14) as editable HWPX.

Usage: python3 work/kdn2025/p26.py <report.pdf> <out.hwpx> [--page N]

평가내용 02 opening page. Only the banner title, the section heading, the 가./나. headings and
the page number are in the PDF text layer; they are taken from it. Everything else (PART box,
평가내용 chip, the 혁신추진계획 diagram and the PDCA diagram) is an image in the PDF: its text
was read from 4x / 8x renders and is typed here, laid out as flat tables on the kit's union
grid (one table per horizontal band). Shapes become fills and borders: chevrons -> graded
fills, pills/tags -> filled cells, the big arrow and the brace -> ▼ rows, round arrow icons ->
▶ connector cells. Bullets drawn as dots become "·" (KS X 1001), ➔ becomes →.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kit  # noqa: E402
from kit import Layout, recipe_inputs  # noqa: E402

source, target = recipe_inputs(26, "국정과제와 New Vision을 동시에 달성하는 혁신추진계획 및 실행체계 개편")
L = Layout(top=3100)
kit.setup(source, L)
from kit import *  # noqa: E402,F401,F403  helpers and presets bound to this page

LIGHT, MIDGRAY, DARKGRAY = "#E4E4E4", "#8C8C8C", "#6A6A6A"


def S(text, size=1050, bold=False, color=INK):
    return (text, size, bold, color)


def bullet(*parts, size=1050):
    """'· text' paragraph; parts are str (body size) or (text, size) for smaller runs."""
    runs = [S("· ", size, False, "#7A7A7A")]
    for part in parts:
        runs.append(S(part, size) if isinstance(part, str) else S(*part))
    return runs


def tight(g, x0, r0, left=60, right=60):
    """Narrow the cell padding (kit cells use the builder default 320/180)."""
    c0 = g.xs.index(to_x(x0))
    item = g.items[r0, c0]
    g.items[r0, c0] = (*item[:7], dict(left=left, right=right))


def fit_ratio(runs, width_pt, pad_pt=1.2, cap=90):
    return min(cap, int(cap * (width_pt - pad_pt) * 0.96 / text_width(runs, cap)))


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

# 평가내용 02 banner (chip is an image; the check-mark icon is dropped).
g = Grid("banner", [X0, 124.0, X1], [2860])
g.put(X0, 124.0, 0, 1, [[("평가내용 ", 800, True, WHITE), ("02", 1350, True, WHITE)]], frame("#5A5A5A"),
      line=1500)
g.put(124.0, X1, 0, 1, [line1(125, 130, 76, 80)], striped, align="LEFT", line=1450)
block(g, 70.9)

# Section heading 1: dark number box + light band.
g = Grid("section-1", [X0, 85.6, X1], [2300])
g.put(X0, 85.6, 0, 1, [line1(60, 70, 108, 114)["text"]], frame("#5E5E5E"), size=1700, bold=True, color=WHITE)
g.put(85.6, X1, 0, 1, [line1(85, 95, 108, 114)], frame(LIGHT), align="LEFT")
block(g, 108.8)

# 가. [혁신추진계획] title: number, pill and title (pill and title are one PDF line).
ga = line1(80, 90, 137, 141)
g = Grid("title-ga", [X0, 76.3, 148.0, X1], [1650])
g.put(X0, 76.3, 0, 1, [line1(55, 60, 137, 141)], align="LEFT", line=1450)
g.put(76.3, 148.0, 0, 1, [runs_of(ga, x1=145.0)], pill)
g.put(148.0, X1, 0, 1, [runs_of(ga, x0=145.0)], align="LEFT", line=1450)
block(g, 137.9)

# ---------------------------------------------------------------------------
# 가. diagram (image in the PDF)
# ---------------------------------------------------------------------------
# Environment box: four headed columns and a hatched conclusion band.
cols = [X0, 180.0, 307.0, 434.0, X1]
chips = [(87.6, 144.4), (214.6, 271.9), (341.8, 399.0), (468.0, 525.2)]
xs = sorted(set(cols + [x for c in chips for x in c] + [64.0, 548.5]))
g = Grid("environment", xs, [1700, 3550, 2350, 650])
heads = ["외부환경", "내부환경", "정부정책", "이해관계자"]
items = [["에너지 산업 AX·DX 가속", "분산E 중심 에너지시장 전환"],
         ["기저사업 성장정체 위기감", "기술전문성 강화 공감대 확산"],
         ["AI·에너지전환 정책 본격추진", "유능한 공공기관에 대한 니즈"],
         ["ESG 등 공익가치 요구 확대", "산업 내 ICT 전문성 선도 요구"]]
for k, ((a, e), (c0, c1)) in enumerate(zip(zip(cols, cols[1:]), chips)):
    g.put(a, c0, 0, 1, [], frame(top="strong", left="soft" if k == 0 else None))
    g.put(c0, c1, 0, 1, heads[k], frame("#707070", top="strong"), size=1150, bold=True, color=WHITE)
    g.put(c1, e, 0, 1, [], frame(top="strong", right="soft" if k == 3 else None))
    g.put(a, e, 1, 2, [bullet(t) for t in items[k]],
          frame(left="soft" if k == 0 else None, right="dot" if k < 3 else "soft"), align="LEFT", line=1300)
g.put(X0, 64.0, 2, 3, [], frame(left="soft"))
g.put(64.0, 548.5, 2, 3, "새정부 국정과제 및 2035 중장기 경영전략과 연계한 혁신전략 재수립 필요",
      frame("#ECECEC", hatch="#DCDCDC"), size=1100, bold=True)
g.put(548.5, X1, 2, 3, [], frame(right="soft"))
g.put(X0, X1, 3, 4, [], frame(left="soft", right="soft", bottom="soft"))
block(g, 160.8)

g = Grid("arrow-1", [X0, X1], [1650])
g.put(X0, X1, 0, 1, "▼", size=1400, color="#A0A0A0", line=1480)
block(g, 243.6)

LAB, IN = 110.4, 116.6     # label column end, content start


def label_band(name, top, height, label, label_fill, content_xs):
    g = Grid(name, sorted(set([X0, LAB] + content_xs)), height if isinstance(height, list) else [height])
    dark_label = label_fill in (MIDGRAY,)
    g.put(X0, LAB, 0, len(g.hs), label, frame(label_fill), size=1150, bold=dark_label,
          color=WHITE if dark_label else INK, line=1350)
    return g


# 국정과제 row: six boxed tags with their titles on a gray band.
tags = [("국정20", "AI고속도로"), ("국정38", "에너지고속도로"), ("국정39", "에너지 대전환"),
        ("국정13", "활력있는 공직사회"), ("국정75", "국민 안전건강"), ("국정99", "AI미래인재 양성")]
edges = [IN, 139.6, 178.0, 201.7, 254.5, 278.2, 325.5, 349.0, 409.5, 433.0, 478.5, 502.2, X1]
g = label_band("national-tasks", 261.0, 2570, "국정과제", MIDGRAY, [LAB] + edges)
band_fill = frame("#D6D6D6")
g.put(LAB, IN, 0, 1, [], band_fill)
text_ratio = min(fit_ratio([S(t, 900)], b - a) for (_, t), a, b in zip(tags, edges[1::2], edges[2::2]))
tag_ratio = min(fit_ratio([S(t, 850)], b - a) for (t, _), a, b in zip(tags, edges[0::2], edges[1::2]))
for k, (tag, title) in enumerate(tags):
    a, b, e = edges[2 * k], edges[2 * k + 1], edges[2 * k + 2]
    g.put(a, b, 0, 1, tag, frame("#D6D6D6", top="mid", bottom="mid", left="mid", right="mid"), size=850,
          ratio=tag_ratio, fit=False, line=1000)
    g.put(b, e, 0, 1, title, band_fill, size=900, ratio=text_ratio, fit=False, line=1050)
    tight(g, a, 0)
    tight(g, b, 0)
block(g, 261.0)

g = label_band("vision", 295.5, 2480, "2035 비전", MIDGRAY, [LAB, X1])
g.put(LAB, X1, 0, 1, "“디지털혁신, 에너지 대전환을 선도하는 글로벌 에너지ICT의 중심”",
      frame("#E2E2E2", hatch="#CFCFCF"), size=1300, bold=True)
block(g, 295.5)

C4 = [(116.6, 221.4), (227.7, 332.5), (338.8, 444.1), (449.9, X1)]
C4X = [LAB] + [x for c in C4 for x in c]
g = label_band("directions", 331.0, 2160, "4대전략방향", LIGHT, C4X)
for (a, e), text in zip(C4, ("디지털 융합", "사업 다각화", "ESG 선도", "시스템 경영")):
    g.put(a, e, 0, 1, text, frame("#DDDDDD"), size=1150, bold=True)
block(g, 331.0)

g = label_band("implications", 357.7, 3080, ["시사점", "도출"], LIGHT, C4X)
for (a, e), lines in zip(C4, (("에너지분야에 특화된", "AI 플랫폼 혁신"), ("탄소중립, 친환경", "에너지 생태계 조성"),
                              ("포용적 사회 구축에", "기여하는 ESG 지속"), ("경영 효율성 · 투명성", "지속 제고"))):
    g.put(a, e, 0, 1, list(lines), frame(top="mid", bottom="mid", left="mid", right="mid"), size=1050, line=1250)
block(g, 357.7)

# Brace gathering the four implications into the goal.
g = Grid("brace", [X0, IN, X1], [850, 1000])
g.put(IN, X1, 0, 1, [], frame(bottom="mid"))
g.put(IN, X1, 1, 2, "▼", size=800, color="#9A9A9A", line=840)
block(g, 388.5)

g = label_band("goal", 407.0, 2400, "혁신목표", LIGHT, [LAB, IN, X1])
g.put(IN, X1, 0, 1, "“에너지 전환 시대의 신뢰받는 에너지ICT 디지털 인프라 선도기업 도약”",
      frame(DARKGRAY, top="soft", bottom="soft", left="soft", right="soft"), size=1250, bold=True, color=WHITE)
block(g, 407.0)

# 4대 혁신방향: shaded area, dashed separators, white pills; 8대 중점과제 below.
CC = [IN, 224.5, 336.0, 447.0, X1]
pills = [(a + 4.0, e - 4.0) for a, e in zip(CC, CC[1:])]
xs = sorted(set([LAB] + CC + [x for p in pills for x in p]))
g = label_band("innovation", 436.0, [3100, 2050, 200], ["4대", "혁신방향"], LIGHT, xs)
leads = [("AI기반 패러다임", "전환을 위한"), ("탄소중립과", "수익다변화를 위한"), ("業특성 기반", "지속성장을 위한"),
         ("생산적", "업무문화를 위한")]
names = ["AX·DX 혁신", "에너지 전환 혁신", "ESG 혁신", "경영시스템 혁신"]
for k, ((a, e), (p0, p1)) in enumerate(zip(zip(CC, CC[1:]), pills)):
    sep = "dot" if k < 3 else None
    g.put(a, e, 0, 1, list(leads[k]), frame("#E2E2E2", right=sep), size=1050, line=1250)
    g.put(a, p0, 1, 3, [], frame("#E2E2E2"))
    g.put(p0, p1, 1, 2, names[k], frame(WHITE), size=1150, bold=True)
    g.put(p0, p1, 2, 3, [], frame("#E2E2E2"))
    g.put(p1, e, 1, 3, [], frame("#E2E2E2", right=sep))
block(g, 436.0)

g = label_band("focus-tasks", 494.6, 3490, ["8대", "중점과제"], LIGHT, [LAB] + CC)
focus = [("AI 보안관제 전담기관 확장", "AI 채용시스템 적용 · 확대"), ("AI기반 수소도시 모델 구축", "해외사업 진출 기반 강화"),
         ("AI기반 온실가스 감축", "기술혁신으로 안전재난 예방"), ("효율성·생산성 증대", "경영개선계획 선제 이행")]
for k, (a, e) in enumerate(zip(CC, CC[1:])):
    g.put(a, e, 0, 1, [bullet(t) for t in focus[k]],
          frame(top="soft", bottom="soft", left="soft" if k == 0 else None, right="dot" if k < 3 else "soft"),
          align="LEFT", line=1300)
block(g, 494.6)

# 나. [실행체계] title (three PDF lines).
g = Grid("title-na", [X0, 76.3, 135.0, X1], [1650])
g.put(X0, 76.3, 0, 1, [line1(55, 60, 539, 543)], align="LEFT", line=1450)
g.put(76.3, 135.0, 0, 1, [line1(85, 95, 540, 545)], pill)
g.put(135.0, X1, 0, 1, [line1(135, 140, 539, 543)], align="LEFT", line=1450)
block(g, 539.6)

# ---------------------------------------------------------------------------
# 나. PDCA diagram (image in the PDF)
# ---------------------------------------------------------------------------
LX, GX = 114.0, 119.0          # label column end, content start
PILL = (72.4, 104.0)


def pdca(name, top, hs, letter, label, extra_xs, pad=(500, 1270, 1500)):
    """Grid with the P/D/C/A label column: letter pill, bold name, rounded-frame borders.

    pad: heights of the space above the pill, the pill row and the name row (1/100 pt)."""
    rest = sum(hs) - sum(pad)
    ys = sorted(set([0] + [sum(pad[:i + 1]) for i in range(3)] + [sum(hs[:i + 1]) for i in range(len(hs))]))
    rows = [b - a for a, b in zip(ys, ys[1:])]
    assert rest > 0
    g = Grid(name, sorted(set([X0, PILL[0], PILL[1], LX, GX] + extra_xs)), rows)
    r = ys.index
    edge = dict(left="mid")
    g.put(X0, LX, 0, r(pad[0]), [], frame(top="mid", **edge))
    g.put(X0, PILL[0], r(pad[0]), r(pad[0] + pad[1]), [], frame(**edge))
    g.put(PILL[0], PILL[1], r(pad[0]), r(pad[0] + pad[1]), letter, frame("#555555"), size=1100, bold=True,
          color=WHITE, line=1110)
    g.put(PILL[1], LX, r(pad[0]), r(pad[0] + pad[1]), [])
    g.put(X0, LX, r(pad[0] + pad[1]), r(sum(pad)), label, frame(**edge), size=1150, bold=True, line=1200)
    g.put(X0, LX, r(sum(pad)), len(rows), [], frame(**edge))
    return g, r


# P: four chevrons (graded fills) and their bullets.
PC = [GX, 226.0, 334.5, 443.5, X1]
g, r = pdca("plan", 562.9, [3150, 3150], "P", "계획수립", PC, pad=(500, 1270, 1380))
chev = [(["혁신전략 수립(5월)"], "#D9D9D9", INK), (["새정부 출범에 따른", "1차 혁신전략 롤링"], "#ABABAB", INK),
        (["비전 2035 재수립", "2차 혁신전략 롤링"], "#8C8C8C", WHITE),
        (["세부 실행과제 추가발굴", "및 혁신전략 고도화(11월)"], "#6A6A6A", WHITE)]
plan = [[bullet("환경분석", ("(SWOT)", 850)), bullet("실행과제 발굴", ("(31건)", 850))],
        [bullet("정부 공약, 정책방향 반영"), bullet("혁신 목표/방향(안) 도출")],
        [bullet("경영전략, 국정과제 반영"), bullet("전문가 컨설팅 + 내부TF")],
        [bullet("실행과제 확정", ("(48개)", 850)), bullet("혁신전략 고도화", ("(11월)", 850))]]
for k, (a, e) in enumerate(zip(PC, PC[1:])):
    lines, fill, color = chev[k]
    g.put(a, e, 0, r(3150), lines, frame(fill), size=1100, bold=True, color=color, align="LEFT", line=1250)
    g.put(a, e, r(3150), r(6300), plan[k], frame(right="dot" if k < 3 else None), align="LEFT", line=1300)
block(g, 562.9)

# D: three numbered task headers.
DC = [GX, 255.0, 411.5, X1]
nums = [(174.0, 204.5), (322.4, 352.7), (470.9, 501.2)]
g, r = pdca("do", 630.0, [1270, 1800, 3290], "D", "과제추진", DC + [x for n in nums for x in n],
            pad=(400, 1270, 1400))
titles = ["조직체계 혁신", "이행체계 혁신", "보상체계 혁신"]
tasks = [[bullet("혁신 추진조직 신설 및 강화"), bullet("혁신 거버넌스 확대")],
         [bullet("직원 체감형 “INNO-CATION” 추진"), bullet("고객/대국민 대상 혁신인식 제고")],
         [bullet("해외 혁신기업 연수 대폭 확대"), bullet("KDN 혁신 경진대회 포상 신설")]]
for k, ((a, e), (n0, n1)) in enumerate(zip(zip(DC, DC[1:]), nums)):
    sep = "dot" if k < 2 else None
    g.put(a, n0, 0, r(1270), [], frame("#E2E2E2", top="mid"))
    g.put(n0, n1, 0, r(1270), str(k + 1), frame("#6A6A6A", top="mid"), size=1050, bold=True, color=WHITE,
          line=1100)
    g.put(n1, e, 0, r(1270), [], frame("#E2E2E2", top="mid", right=sep))
    g.put(a, e, r(1270), r(3070), titles[k], frame("#E2E2E2", right=sep), size=1150, line=1300)
    g.put(a, e, r(3070), r(6360), tasks[k], frame(right=sep), align="LEFT", line=1300)
block(g, 630.0)

# C: 점검 / 보상 boxes with round-arrow icons (-> ▶) and bullets between rules.
CX = [GX, 152.0, 162.5, 311.0, 317.4, 350.5, 361.0, X1]
g, r = pdca("check", 698.8, [4040], "C", "성과점검", CX)
rule = frame(top="soft", bottom="soft")
for a, b, c, e, name, lines in (
        (GX, 152.0, 162.5, 311.0, "점검",
         [bullet("혁신책임관 주재 이행성과 코칭", ("(매주)", 850)),
          bullet("경영현안회의", ("(격주)", 850), " 및 월간회의", ("(매월)", 850))]),
        (317.4, 350.5, 361.0, X1, "보상",
         [bullet("혁신 우수자 우대조치 확대", ("(5명", 850), ("’24년", 550), (" → 51명", 850), ("’25년", 550),
                 (")", 850)),
          bullet("조직평가 차등부여 및 우수과제 포상")])):
    g.put(a, b, 0, len(g.hs), name, frame("#DDDDDD"), size=1200)
    g.put(b, c, 0, len(g.hs), "▶", size=900, color="#8A8A8A", fit=False)
    g.put(c, e, 0, len(g.hs), lines, rule, align="LEFT", line=1350)
block(g, 698.8)

# A: three dark pills with their result lines inside one outlined box.
AX = [GX, 120.4, 212.5, 217.5, X1]
hs = [420, 1340, 310, 1340, 250, 1390, 370]
g, r = pdca("act", 746.8, hs, "A", "공유 · 환류", AX, pad=(420, 1340, 1650))
box = dict(left="mid", right="mid")
results = [
    ("혁신 인식도 조사", [S("혁신인식지수 도입 2년차 → 조사 결과 활용 개선점 도출 및 차년도 혁신계획 반영", 1100)]),
    ("내재화 및 확산", [S("직원 참여형 혁신 행사, 정부 혁신 공모전 참여 → 포상 강화 및 특별승진 추천", 1100)]),
    ("우수과제 공유", [S("찾아가는 대국민 혁신활동", 1100), S("(3,406명)", 850), S(", 사내외 홈페이지 공유 25건", 1100),
                   S("(내부 16건, 외부 9건)", 850)])]
cum = [sum(hs[:i]) for i in range(len(hs) + 1)]
g.put(GX, X1, 0, r(cum[1]), [], frame(top="mid", **box))
for k, (name, runs) in enumerate(results):
    r0, r1, r2 = r(cum[1 + 2 * k]), r(cum[2 + 2 * k]), r(cum[3 + 2 * k])
    g.put(GX, 120.4, r0, r1, [], frame(left="mid"))
    g.put(120.4, 212.5, r0, r1, name, frame("#6E6E6E"), size=1050, bold=True, color=WHITE, line=1150)
    g.put(212.5, 217.5, r0, r1, [])
    g.put(217.5, X1, r0, r1, [runs], frame(right="mid"), align="LEFT", line=1180)
    g.put(GX, X1, r1, r2, [], frame(bottom="mid" if k == 2 else None, **box))
block(g, 746.8)

kit.finish(target, end=803.0)
