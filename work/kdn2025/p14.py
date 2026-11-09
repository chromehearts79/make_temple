"""Rebuild KDN 2025 report physical PDF page 14 (printed page 2): 3 추진전략 및 실행계획.

Usage: python3 work/kdn2025/p14.py <report.pdf> <out.hwpx> [--page N]

Almost the whole page (strategy system chart, 2035 roadmap and the business-line table) is one
image in the PDF; only the page number and the section heading are in the text layer. The chart
text below is typed from 4-6x renders of that image and laid out with the shared kit
(work/kdn2025/kit.py) as one flat table per band on the image's own x/y edges: gray label column
at the left, boxes as filled or outlined cells, dashed separators as dotted borders, the small
number chips as dark cells, the ▼ chevrons and roadmap arrows as connector glyphs. Rounded
corners, gradients and the dark tab above 사업전략/기능전략 are not reproduced.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kit  # noqa: E402
from kit import Layout, recipe_inputs  # noqa: E402

source, target = recipe_inputs(14, "추진전략 및 실행계획")
L = Layout(top=3100)
kit.setup(source, L)
from kit import *  # noqa: E402,F401,F403  helpers and presets bound to this page

kit.STROKES["gap"] = ("SOLID", "0.7 mm", "#FFFFFF")   # white gap between stacked label boxes

LABEL_DARK = frame("#9A9A9A")
GRAYH = "#E5E5E5"   # light box / card header fill
CHIP = "#4A4A4A"
XL, XC = 110.5, 116.0                                    # label column end, content start
COLS4 = [(XC, 221.75), (227.0, 333.5), (338.75, 444.75), (450.5, X1)]
SPLIT4 = [XC, 223.6, 336.8, 445.5, X1]                   # dashed separators of one wide box


def label(g, r0, r1, lines, bottom=None):
    """Gray label box of the left column (a white bottom edge separates stacked labels)."""
    g.put(X0, XL, r0, r1, [[(t, 1100, False, INK)] for t in lines], frame("#D9D9D9", bottom=bottom), line=1300)


def text(lines, size, bold=False, color=INK):
    return [[(t, size, bold, color)] for t in lines]


# ---------------------------------------------------------------------------
# Page chrome: even page -> "PART 01 | 경영관리" box at the left over a rule, footer at left.
# ---------------------------------------------------------------------------
foot = [(line1(55, 60, 816, 822)["text"], 1090, False, INK), ("    ", 1090, False, INK),
        ("한전KDN㈜", 1090, True, INK)]   # the logo is an image in the PDF
L.add_table([[cell(0, W, 1500, [para(foot, "LEFT", 1300)[0]])]], floating=(5660, 81550))

g = Grid("head", [X0, 102.6, 159.6, X1], [1600])
g.put(X0, 102.6, 0, 1, "PART 01", frame("#EFEFEF", top="strong"), size=1000, bold=True)
g.put(102.6, 159.6, 0, 1, "경영관리", frame("#333333"), size=1080, bold=True, color=WHITE)
g.put(159.6, X1, 0, 1, [], frame(bottom="soft"))
block(g, 31.0)

# Section band: dark number square + light band (an image in the PDF; text from the text layer).
g = Grid("section", [X0, 85.0, X1], [2300])
g.put(X0, 85.0, 0, 1, [line1(60, 70, 72, 76)], dark, color=WHITE, line=1850)
g.put(85.0, X1, 0, 1, [line1(85, 95, 72, 76)], frame("#E4E4E4", top="soft", bottom="soft"),
      align="LEFT", line=1750)
block(g, 70.9)

# ---------------------------------------------------------------------------
# Strategy system chart (image): label column + content boxes, one table per band.
# ---------------------------------------------------------------------------
g = Grid("mission-vision", [X0, XL, XC, X1], [2925, 750, 2500])
g.put(X0, XL, 0, 1, text(["설립목적", "(미션)"], 1100, color=WHITE), LABEL_DARK, line=1250)
g.put(XC, X1, 0, 1, "에너지ICT 기술 전문화 및 고도화를 통해 에너지산업 발전에 기여",
      frame("#6C6C6C"), size=1300, bold=True, color=WHITE)
g.put(X0, XL, 2, 3, text(["2035", "New Vision"], 1050, color=WHITE), LABEL_DARK, line=1150)
g.put(XC, X1, 2, 3, "디지털 혁신, 에너지 대전환을 선도하는 글로벌 에너지ICT의 중심",
      frame("#E2E2E2", hatch="#CDCDCD"), size=1300, bold=True)
block(g, 100.5)

xs = [X0, XL, XC, 200.25, 204.5, 289.0, 293.25, 378.0, 382.25, 466.75, 471.0, X1]
g = Grid("core-values", xs, [2875])
label(g, 0, 1, ["5대", "핵심가치"])
values = [("Visionary", "미래주도"), ("Advance", "기술선도"), ("Leap", "도전의식"), ("Unity", "소통협력"),
          ("Ethic", "청렴윤리")]
for k, (eng, kor) in enumerate(values):
    g.put(xs[2 + 2 * k], xs[3 + 2 * k], 0, 1, text([eng, kor], 1050, True), frame("#EEEEEE"), line=1200)
block(g, 173.0)

g = Grid("goals", [X0, XL] + SPLIT4, [4375])
label(g, 0, 1, ["9대", "경영목표"])
goals = [["① 매출액 2조원", "② AX·DX 5단계"], ["③ 미래신사업 매출 6천억원", "④ 해외사업 매출 1천억원"],
         ["⑤ 탄소중립 기여도", "⑥ 상생가치 창출성과", "⑦ 국민신뢰 소통지수"],
         ["⑧ 시스템 및 기술혁신성과", "⑨ 인적자원 역량지수"]]
for k, items in enumerate(goals):
    box = frame(top="mid", bottom="mid", left="mid" if k == 0 else None, right="mid" if k == 3 else "dot")
    g.put(SPLIT4[k], SPLIT4[k + 1], 0, 1, text(items, 960), box, align="LEFT", line=1300)
block(g, 207.0)

g = Grid("ceo", [X0, XL] + sorted({x for c in COLS4 for x in c}), [2700])
label(g, 0, 1, ["CEO", "경영방침"])
for (a, e), t in zip(COLS4, ["디지털 혁신 주도", "지속성장 실현", "ESG경영 강화", "시스템경영 구현"]):
    g.put(a, e, 0, 1, t, frame("#D1D1D1"), size=1150, bold=True)
block(g, 255.75)

# 4대 전략방향: two outlined halves (사업전략 | 기능전략), numbered sub-columns, dashed split.
halves = [(XC, 224.0, 333.5, "사 업 전 략"), (338.75, 447.0, X1, "기 능 전 략")]
xs = [X0, XL, XC, 130.0, 224.0, 238.0, 333.5, 338.75, 352.75, 447.0, 461.0, X1]
g = Grid("directions", xs, [1650, 1650, 3750])
label(g, 0, 3, ["4대", "전략방향"])
titles = ["디지털 융합", "사업 다각화", "ESG 선도", "시스템 경영"]
bodies = [["AI 기반의 독자", "솔루션으로", "에너지산업 DX주도"], ["미래신사업 경쟁력", "확보로 글로벌", "에너지ICT 신시장 창출"],
          ["디지털 기반", "ESG가치 창출로", "에너지ICT 생태계 주도"], ["혁신주도형 시스템", "경영으로", "지속가능성과 확대"]]
for h, (a, m, e, name) in enumerate(halves):
    g.put(a, e, 0, 1, name, frame(top="mid", left="mid", right="mid"), size=1100, bold=True)
    for j, (s0, s1) in enumerate(((a, m), (m, e))):
        k = 2 * h + j
        g.put(s0, s0 + 14.0, 1, 2, str(k + 1), frame(CHIP, left="mid" if j == 0 else None),
              size=900, bold=True, color=WHITE)
        g.put(s0 + 14.0, s1, 1, 2, titles[k], frame("#CBCBCB", right="mid" if j == 1 else None), size=1100)
        g.put(s0, s1, 2, 3, text(bodies[k], 960),
              frame(bottom="mid", left="mid" if j == 0 else None, right="mid" if j == 1 else "dot"), line=1120)
block(g, 288.0)

# 12대 전략과제: three cards per column (gray header with a dark number chip, outlined body).
tasks = [
    [("1-1", "DX기반 차세대 전력망", ["디지털 혁신 기술 기반", "전력망 지능화 선도"]),
     ("1-2", "ICT운영 서비스", ["ICT 인프라 및 운영 서비스", "디지털 경쟁력 강화"]),
     ("1-3", "AI 융합 플랫폼 서비스", ["AI 융합 에너지 플랫폼 중심", "사업 패러다임 대전환"])],
    [("2-1", "분산E 서비스 다각화", ["新 수요시장 대응", "분산에너지 서비스 다각화"]),
     ("2-2", "New ICT O&M", ["AI 적용 New ICT O&M", "서비스 혁신"]),
     ("2-3", "투자기반 에너지신사업", ["전략적 투자 기반", "에너지신사업 자생력 및 영역 확대"])],
    [("3-1", "환경경영(E)", ["탄소중립 선도", "친환경 디지털경영 강화"]),
     ("3-2", "상생경영(S)", ["사회적 동행가치 창출", "상생협력경영 차별화"]),
     ("3-3", "신뢰경영(G)", ["소통과 투명한 거버넌스 기반", "국민신뢰경영 확립"])],
    [("4-1", "경영혁신", ["지속가능성과 창출", "경영시스템 혁신 정착"]),
     ("4-2", "경영자원", ["시너지와 효율 극대화 지향", "자원배분 최적화"]),
     ("4-3", "전문역량", ["고객과 산업을 리드하는", "직무중심 전문가 육성체계 강화"])],
]
xs = [X0, XL] + sorted({x for a, e in COLS4 for x in (a, a + 4.0, a + 19.0, e)})
g = Grid("tasks", xs, [1550, 2750, 375, 1550, 2725, 425, 1525, 2750])
label(g, 0, 8, ["12대", "전략과제"])
for (a, e), cards in zip(COLS4, tasks):
    for i, (chip, title, body) in enumerate(cards):
        r = 3 * i
        g.put(a, a + 4.0, r, r + 1, [], frame(GRAYH, top="soft", left="soft"))
        g.put(a + 4.0, a + 19.0, r, r + 1, chip, frame(CHIP, top="soft"), size=880, bold=True, color=WHITE)
        g.put(a + 19.0, e, r, r + 1, title, frame(GRAYH, top="soft", right="soft"), size=950)
        g.put(a, e, r + 1, r + 2, text(body, 950), frame(left="soft", right="soft", bottom="soft"), line=1100)
block(g, 364.5)

g = Grid("chevrons", [X0, XL] + sorted({x for c in COLS4 for x in c}), [525])
for a, e in COLS4:
    g.put(a, e, 0, 1, "▼", size=520, color="#7A7A7A", line=520)
block(g, 501.0)

# 53개 실행과제 (outlined) over 주요성과지표(KPI) (gray).
actions = [("에너지 클라우드", "플랫폼(K-ECP) 등 ", "15개"), ("수소, 스마트 시티·산단", "등 ", "14개"),
           ("친환경ICT 솔루션 및", "스마트 안전관리 등 ", "12개"), ("AI기반 클라우드 시스템", "전환 등 ", "12개")]
kpis = [("IDPP플랫폼 개발실적", "등 54개"), ("수소ICT사업 매출실적", "등 46개"), ("탄소중립목표 달성실적", "등 37개"),
        ("AI솔루션 도입실적", "등 36개")]
g = Grid("actions-kpi", [X0, XL] + sorted({x for c in COLS4 for x in c}), [3200, 2675])
label(g, 0, 1, ["53개", "실행과제"], bottom="gap")
label(g, 1, 2, ["주요성과", "지표(KPI)"])
for (a, e), (first, pre, count), kpi in zip(COLS4, actions, kpis):
    g.put(a, e, 0, 1, [[(first, 1050, False, INK)], [(pre, 1050, False, INK), (count, 1250, True, INK)]],
          frame(top="mid", bottom="mid", left="mid", right="mid"), line=1350)
    g.put(a, e, 1, 2, text(kpi, 1050), frame(GRAYH), line=1250)
block(g, 506.25)

# 실행 및 모니터링 체계: 조직(BSC) | 개인(MBO) | 모니터링 및 공유.
mon = [((XC, 221.75), "조직(BSC)", ["조직평가", "계량(KPI)+비계량(KI)", "+경영실적 연계"], "CENTER"),
       ((227.0, 333.5), "개인(MBO)", ["인사평가", "(역량평가+업적평가)", "(상향·하향·동료평가)"], "CENTER"),
       ((338.75, X1), "모니터링 및 공유",
        ["(점검) 주간(처장)·현안(본부장)·월간(기관장), 리더워크숍 등",
         "(평가) KPI 중간/최종 평가, 전략과제이행도, 국정과제이행 평가 등",
         "(공유) 경영소통회, 전략설명회, 교육(승진, 입사 등), 노사합동TF등"], "LEFT")]
g = Grid("monitoring", [X0, XL, XC, 221.75, 227.0, 333.5, 338.75, X1], [1525, 3825])
label(g, 0, 2, ["실행 및", "모니터링", "체계"])
for (a, e), head, body, align in mon:
    g.put(a, e, 0, 1, head, frame(GRAYH), size=960)
    g.put(a, e, 1, 2, text(body, 940), frame(left="soft", right="soft", bottom="soft"), align=align, line=1150)
block(g, 569.0)

# 환류체계: one outlined box, four columns with dashed separators.
heads = ["경영진", "조직", "개인", "대외 이해관계자"]
bodies = [["경영계약 지표 연계", "(자율책임경영체제)"], ["성과급 차등, 저성과 진단", "및 제도개선 발굴 등"],
          ["특별승진, 국내/외 연수", "및 교육, 포상 등"], ["주요 이해관계자 의견 및", "국민제안 아이디어 반영 등"]]
g = Grid("feedback", [X0, XL] + SPLIT4, [1425, 2575])
label(g, 0, 2, ["환류체계"])
for k, (head, body) in enumerate(zip(heads, bodies)):
    side = dict(left="mid" if k == 0 else None, right="mid" if k == 3 else "dot")
    g.put(SPLIT4[k], SPLIT4[k + 1], 0, 1, head, frame(GRAYH, top="mid", **side), size=960)
    g.put(SPLIT4[k], SPLIT4[k + 1], 1, 2, text(body, 940), frame(bottom="mid", **side), line=1130)
block(g, 626.5)

# ---------------------------------------------------------------------------
# 2035 roadmap (image): staggered slogan pills with arrows, three STEP bars.
# ---------------------------------------------------------------------------
g = Grid("roadmap-title", [X0, X1], [1700])
g.put(X0, X1, 0, 1, "“2035 한전KDN 미래 성장 로드맵”", align="LEFT", size=1400, bold=True, line=1600)
block(g, 671.5)

xs = [X0, 190.5, 221.75, 223.75, 225.3, 356.5, 388.75, 391.0, 522.0, 541.0, X1]
ys = [686.0, 691.0, 695.8, 701.2, 706.2, 707.8, 710.8, 712.3, 717.8, 735.3]
g = Grid("roadmap", xs, [int(round((b - a) * 100)) for a, b in zip(ys, ys[1:])])
fills = [("#BFBFBF", INK), ("#7F7F7F", WHITE), ("#585858", WHITE)]
pills = [(X0, 190.5, 2, 6, "AI 혁신으로 에너지산업 AX·DX 주도"), (225.3, 356.5, 1, 4, "탄소중립 대응을 넘어 에너지전환 선도"),
         (391.0, 522.0, 0, 3, "글로벌 에너지 생태계의 중심으로 도약")]
for (a, e, r0, r1, t), (fill, color) in zip(pills, fills):
    g.put(a, e, r0, r1, t, frame(fill), size=1000, color=color, line=1150)
g.put(190.5, 225.3, 2, 5, "→", size=1300, color="#8C8C8C", line=1300)
g.put(356.5, 391.0, 1, 4, "→", size=1300, color="#8C8C8C", line=1300)
steps = [(X0, 221.75, 8, "01", "전환기", "(’26~’28년)"), (223.75, 388.75, 7, "02", "성장기", "(’29~’32년)"),
         (391.0, 541.0, 5, "03", "성숙기", "(’33년~’35년)")]
for (a, e, r0, num, name, years), (fill, color) in zip(steps, fills):
    g.put(a, e, r0, 9, [[("  STEP ", 650, False, color), (num, 1400, False, color), ("  " + name, 1350, True, color),
                         (" " + years, 1000, False, color)]], frame(fill), align="LEFT", line=1560)
g.put(541.0, X1, 5, 9, "▶", size=1500, color="#585858", line=1500)
block(g, 686.0)

# Business lines per stage: gray label pill + text, dotted row separators.
lines = [["AX·DX 기반 지능형 계통운영전환", "신기술 적용 O&M 자동화/효율화", "분산E 시장 투자 확대 및 신사업 발굴"],
         ["AI융합 차세대 전력망 구축", "AI Agent 기반 O&M 패러다임 전환", "AI 데이터센터 구축 및 서비스 발굴"],
         ["AI기반 계통운영 솔루션 글로벌 확산", "AI, SaaS 기반 서비스형 운영모델 정착", "에너지 솔루션 패키지 기반 해외 확장"]]
groups = [(X0, 102.5, 221.75), (223.75, 269.25, 388.75), (391.25, 436.75, X1)]
xs = [X0, 102.5, 221.75, 223.75, 269.25, 388.75, 391.25, 436.75, X1]
g = Grid("business-lines", xs, [1725, 1825, 1700])
for (a, m, e), items, (fill, color) in zip(groups, lines, fills):
    for r, (name, item) in enumerate(zip(["전력계통사업", "ICT운영사업", "미래성장사업"], items)):
        g.put(a, m, r, r + 1, name, frame(fill, bottom="gap" if r < 2 else None), size=900, color=color)
        g.put(m, e, r, r + 1, item, frame(bottom="dot" if r < 2 else None), align="LEFT", size=980)
block(g, 744.5)

kit.finish(target, end=801.6)
