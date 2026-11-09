"""Rebuild KDN 2025 report page 104 (third PDF local page 4, printed page 69) as editable HWPX.

Usage: python3 work/kdn2025/p104.py <report3.pdf> <out.hwpx> [--page 4]

"Ⅲ. 세부 평가내용별 추진실적" opening page of the 재무성과관리(재무예산관리) indicator. Only the
page title, the 평가내용 01 band title, the section-1 band, the 가./나. headings, the 유사기업 note
and the page number are in the PDF text layer; they are taken from it. Both diagrams are images
(가. y 197-381: 비전 / 중장기 경영목표 / 환경변화 / 시사점; 나. y 413-787: 중장기 경영전략 / 성장
로드맵 / 중장기 재무목표). Their text was read from 4-5x renders and is typed into editable cells on
the diagram's own grid (label column | content), built with the shared kit.

Glyph and shape choices for image-only fragments: list dots -> "·", the ➔ arrows of the target
values -> "→", the chevron above 시사점 -> "▼", rounded / tabbed boxes -> fills and borders,
the slanted step heads 01-03 -> plain gray cells. The three donut charts of 성장 로드맵 keep only
their printed values (category, amount, share and the year total in the centre); rings, hatching
and the big growth arrow are dropped. Values cross-checked: 3,926 + 429 + 3,725 = 8,080억원
(0.8조원, 49+5+46 %), 5,326 + 3,247 + 5,079 = 13,652억원 (1.4조원, 39+24+37 %),
6,861 + 6,233 + 6,881 = 19,975억원 (2.0조원, 34+31+35 %; 6,881 / 19,975 is 34.4 %, printed 35 %).
Superscript years (’25년, ’35년) are small runs on the baseline.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kit  # noqa: E402
from kit import Layout, recipe_inputs  # noqa: E402

source, target = recipe_inputs(4, "2035 경영목표와 환경변화를 고려한 중장기 재무관리계획 수립")
L = Layout(top=3100)
kit.setup(source, L)
from kit import *  # noqa: E402,F401,F403  helpers and presets bound to this page

LX, CX0 = 113.5, 121.5           # label column end, content start
LABEL = frame("#E5E5E5")
COLS3 = ((CX0, 265.8), (266.2, 410.8), (411.2, X1))


def m(text, size=1050, bold=False, color=INK, small=0.82, sup=0.6):
    """Typed run list: {..} = smaller run (parenthetical counts), ^..^ = superscript-size run."""
    runs = []
    for part in re.split(r"(\{[^}]*\}|\^[^^]*\^)", text):
        if not part:
            continue
        if part[0] == "{":
            runs.append((part[1:-1], int(round(size * small / 10)) * 10, bold, color))
        elif part[0] == "^":
            runs.append((part[1:-1], int(round(size * sup / 10)) * 10, bold, color))
        else:
            runs.append((part, size, bold, color))
    return runs


def label(g, r0, r1, lines, fill=LABEL, color=INK):
    g.put(X0, LX, r0, r1, [m(t, 1050, False, color) for t in lines], fill, line=1250)


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

g = Grid("title", [X0, X1], [2400])
g.put(X0, X1, 0, 1, [line1(195, 205, 69, 75)])
block(g, 68.5)

# 평가내용 01 band: dark chip (image, typed; its check mark is dropped) over a hatched strip.
g = Grid("band", [X0, 127.0, X1], [1730, 1140])
g.put(X0, 127.0, 0, 1, [[("평가내용 ", 800, True, WHITE), ("01", 1350, True, WHITE)]],
      frame("#5F5F5F", top="mid", left="mid"), line=1500)
g.put(X0, 127.0, 1, 2, [], frame("#E9E9E9", bottom="mid", left="mid", hatch="#DADADA"))
g.put(127.0, X1, 0, 2, [line1(125, 130, 110, 116)], frame("#E9E9E9", top="mid", bottom="mid", right="mid",
                                                            hatch="#DADADA"), align="LEFT", line=1450)
block(g, 105.5)

g = Grid("section", [X0, 85.5, X1], [2240])
g.put(X0, 85.5, 0, 1, [runs_of(line1(64, 70, 147, 152), WHITE)], frame("#666666"), line=1800)
g.put(85.5, X1, 0, 1, [line1(90, 95, 148, 153)], frame("#E5E5E5"), align="LEFT", line=1700)
block(g, 146.5)

g = Grid("ga", [X0, X1], [1650])
g.put(X0, X1, 0, 1, [line1(55, 60, 174, 178)], align="LEFT", line=1450)
block(g, 174.0)

# ---------------------------------------------------------------------------
# 가. diagram (image; text read from 4x renders)
# ---------------------------------------------------------------------------
# 비전: two-tone dark label, hatched statement band.
g = Grid("vision", [X0, 85.0, LX, X1], [420, 2440])
g.put(X0, 85.0, 0, 2, "비", frame("#9A9A9A"), size=1150, bold=True, color=WHITE)
g.put(85.0, LX, 0, 2, "전", frame("#8B8B8B"), size=1150, bold=True, color=WHITE)
g.put(LX, X1, 1, 2, "디지털 혁신, 에너지 대전환을 선도하는 글로벌 에너지ICT의 중심",
      frame("#CDCDCD", hatch="#D9D9D9"), size=1150, bold=True)
block(g, 196.8)

# 중장기 경영목표: four boxes, outlined head over a gray bullet body.
B4 = ((CX0, 227.0), (230.8, 336.5), (340.2, 446.0), (449.8, X1))
GOALS = (("디지털 융합", ["매출액 2조원", "AX-DX레벨 5단계"]),
         ("사업 다각화", ["미래신사업매출 6천억원", "해외사업매출 1천억원"]),
         ("ESG 선도", ["동반성장평가 최우수", "탄소저감 60%"]),
         ("시스템 경영", ["품질경쟁력 우수기업", "핵심전문가 740명"]))
g = Grid("goals", [X0, LX, CX0] + [x for b in B4 for x in b][1:], [480, 2220, 3430])
label(g, 0, 3, ["중 장 기", "경영목표"])
for (a, e), (head, items) in zip(B4, GOALS):
    g.put(a, e, 1, 2, head, frame(WHITE, top="strong", left="soft", right="soft"), size=1150)
    g.put(a, e, 2, 3, [m("· " + t) for t in items], frame("#EDEDED"), align="LEFT", line=1400)
block(g, 226.0)

# 환경변화: three heads (dark rule on top, gray rule below), two tagged findings each.
ENV = (((CX0, 147.2, 263.2), "대외환경", [("기회", "에너지산업의 구조적 전환"), ("위기", "민간ICT업계와의 경쟁우려")]),
       ((267.2, 293.5, 409.0), "내부환경", [("강점", "신재생ICT사업 경험 보유"), ("약점", "그룹사 매출 의존도 편중")]),
       ((413.0, 439.5, X1), "정책 · 제도 변화", [("기회", "AI·에너지전환 산업정책 확대"),
                                              ("책임", "ESG·지속가능경영 요구강화")]))
xs = [X0, LX, CX0, 123.2]
for (a, b, e), *_ in ENV:
    xs += [a, a + 1.7, b, e]
xs = sorted(set(xs))
g = Grid("env", xs, [2050, 550, 1250, 1250, 200])
label(g, 0, 5, ["환경변화"])
for (a, b, e), head, rows in ENV:
    g.put(a, e, 0, 1, head, frame(top="strong", bottom="mid"), size=1150)
    g.put(a, e, 1, 2, [], frame("#EFEFEF"))
    for k, (tag, text) in enumerate(rows):
        g.put(a, a + 1.7, 2 + k, 3 + k, [], frame("#EFEFEF"))
        g.put(a + 1.7, b, 2 + k, 3 + k, tag, frame("#CBCBCB"), size=950, line=1100, fit=False)
        g.put(b, e, 2 + k, 3 + k, [m(text)], frame("#EFEFEF"), align="LEFT", line=1250)
    g.put(a, e, 4, 5, [], frame("#EFEFEF"))
block(g, 292.5)

g = Grid("chevron", [X0, 330.0, 347.0, X1], [1170])
g.put(330.0, 347.0, 0, 1, "▼", size=900, color="#9A9A9A", line=1000, fit=False)
block(g, 345.5)

g = Grid("implication", [X0, LX, CX0, X1], [2360])
label(g, 0, 1, ["시 사 점"])
g.put(CX0, X1, 0, 1, "안정적 재무 운영을 기반으로 지속가능한 신성장동력 창출", frame("#7F7F7F", hatch="#737373"),
      size=1200, bold=True, color=WHITE)
block(g, 357.2)

g = Grid("na", [X0, X1], [1650])
g.put(X0, X1, 0, 1, [line1(55, 60, 390, 395)], align="LEFT", line=1450)
block(g, 391.0)

# ---------------------------------------------------------------------------
# 나. diagram (image; text read from 4-5x renders)
# ---------------------------------------------------------------------------
# 중장기 경영전략: dark term tag + strategy head, gray subtitle, bullets; dotted dividers.
STRAT = (("단기", "’25년 성장전략", "기저사업 강화 및 신시장 진출",
          ["· 기존 핵심 고객 서비스 강화", "· SPC 지분투자형 신사업 참여"]),
         ("중기", "’30년 성장전략", "수익구조 다변화 및 사업역량 강화",
          ["· 데이터센터, AI 등 사업영역 확장", "· 해외원전 등 글로벌사업 동반진출"]),
         ("장기", "’35년 성장전략", "신사업 확대를 통한 미래성장",
          ["· AX · DX기반 서비스 확대", "  - 국가 에너지 AI데이터센터 구축 등"]))
xs = [X0, LX, CX0]
for a, e in COLS3:
    xs += [a, a + 33.3, e]
xs = sorted(set(xs))
g = Grid("strategy", xs, [2100, 1980, 2790])
label(g, 0, 3, ["중 장 기", "경영전략"])
for k, ((a, e), (tag, head, sub, items)) in enumerate(zip(COLS3, STRAT)):
    side = "dot" if k else None
    g.put(a, a + 33.3, 0, 1, tag, frame("#7F7F7F", top="strong"), size=1000, bold=True, color=WHITE, fit=False)
    g.put(a + 33.3, e, 0, 1, head, frame("#D4D4D4", top="strong"), size=1200, bold=True)
    g.put(a, e, 1, 2, sub, frame("#E5E5E5", left=side), size=1150)
    g.put(a, e, 2, 3, [m(t, 1100) for t in items], frame(left=side), align="LEFT", line=1330)
block(g, 413.2)

# 성장 로드맵: three donut charts -> value cells (label blocks around the year total).
DONUTS = (((CX0, 170.0, 212.0, 265.8), "’25년", "0.8조원",
           ("3,926억원", "49%"), ("429억원", "5%"), ("3,725억원", "46%"), 2),
          ((266.2, 315.0, 357.0, 410.8), "’30년", "1.4조원",
           ("5,326억원", "39%"), ("3,247억원", "24%"), ("5,079억원", "37%"), 1),
          ((411.2, 456.0, 496.0, X1), "’35년", "2.0조원",
           ("6,861억원", "34%"), ("6,233억원", "31%"), ("6,881억원", "35%"), 1))
xs = sorted({X0, LX, CX0} | {x for d in DONUTS for x in d[0]})
g = Grid("roadmap", xs, [300, 3200, 1500, 1500, 3200, 480])
label(g, 0, 6, ["성        장", "로  드  맵"])
for (a, b, c, e), year, total, ict, future, power, ict_row in DONUTS:
    def block3(name, value, share, bold, align):
        return [m(name, 850, bold), m(value, 850, bold), m("(" + share + ")", 750, bold)]
    g.put(c, e, 1, 2, block3("미래성장사업", *future, True, "RIGHT"), align="RIGHT", line=950)
    if ict_row == 2:
        g.put(a, b, 2, 4, block3("ICT운영사업", *ict, False, "LEFT"), align="LEFT", line=940)
        g.put(b, c, 2, 5, [m(year, 900), m(total, 1150, True)], frame("#E3E3E3"), line=1300)
    else:
        g.put(a, b, 1, 2, block3("ICT운영사업", *ict, False, "LEFT"), align="LEFT", line=950)
        g.put(b, c, 2, 4, [m(year, 900), m(total, 1150, True)], frame("#E3E3E3"), line=1300)
    g.put(c, e, 4, 5, block3("전력계통사업", *power, False, "RIGHT"), align="RIGHT", line=950)
block(g, 487.2)

# 중장기 재무목표: outlined process box (title, three step heads, bullets), then three target boxes.
STEP_X = ((CX0, 266.2), (270.2, 415.8), (419.8, X1))
BUL_X = ((CX0, 257.5), (257.5, 407.5), (407.5, X1))
STEPS = (("01", "추세 분석 및 변수설정", "#E5E5E5",
          ["· 최근 5개년 사업 추이 분석", "· 매출규모를 좌우하는 전략사업", "  수주·사업화 핵심변수 설정"]),
         ("02", "매출 시나리오 도출", "#D9D9D9",
          ["· 추세와 핵심변수를 반영한", "  낙관·기준·비관 시나리오 도출", "· 3개 시나리오별 매출규모 확정"]),
         ("03", "재무목표 설정", "#BFBFBF",
          ["· 매출 시나리오 기반 손익·재무", "  상태 시뮬레이션을 통해 2035", "  재무목표 설정"]))
TARGET_X = ((120.2, 155.8, 226.0, 261.8), (267.0, 302.8, 373.0, 408.5), (414.0, 449.8, 520.0, X1))
xs = sorted({X0, LX, CX0} | {x for p in STEP_X + BUL_X + TARGET_X for x in p})
g = Grid("finance", xs, [2200, 1850, 4720, 200, 480, 1700, 1700, 1850, 4600])
label(g, 0, 9, ["중 장 기", "재무목표"])
g.put(CX0, X1, 0, 1, "중장기 경영목표 · 매출 시나리오와 연계한 2035 재무목표 재설정",
      frame(top="mid", left="mid", right="mid"), size=1150, bold=True)
for (a, e), (num, head, fill, _) in zip(STEP_X, STEPS):
    g.put(a, e, 1, 2, [[(num + "  ", 1300, False, "#9A9A9A"), (head, 1150, True, INK)]], frame(fill),
          align="LEFT", line=1450)
for k, ((a, e), (*_, items)) in enumerate(zip(BUL_X, STEPS)):
    g.put(a, e, 2, 3, [m(t) for t in items], frame(left="dot" if k else None), align="LEFT", line=1400)
g.put(CX0, X1, 3, 4, [], frame(bottom="mid"))
TARGETS = (("매출액", m("8,080억원", 1200, True) + m("’25년", 700, True) + m(" → 2조원", 1200, True)
            + m("’35년", 700, True), "성장 목표",
            [m("· 전력산업 변화 · 사업추진 실적을"), m("  고려한 시나리오 방식 목표 설정"),
             m("· 기준 시나리오 채택 {(CAGR 9.5%)}")]),
           ("영업이익률", m("10.7%", 1200, True) + m("’25년", 700, True) + m(" →15.2%", 1200, True)
            + m("’35년", 700, True), "수익 목표",
            [m("· 5개년 산업평균{(9.0%)} 대비 우수"), m("· 유사* 민간ICT기업 수익성 지표"),
             m("  벤치마킹 통한 목표 타당성 검증")]),
           ("부채비율", m("34.4%", 1200, True) + m("’25년", 700, True) + m(" → 44.9%", 1200, True)
            + m("’35년", 700, True), "안정 목표",
            [m("· 5개년 산업평균{(96.8%)} 대비 우수"), m("· 유사* 공기업 안정성 지표"),
             m("  벤치마킹 통한 목표 타당성 검증")]))
for (a, b, c, e), (pill, value, head, items) in zip(TARGET_X, TARGETS):
    g.put(b, c, 5, 6, pill, frame("#7F7F7F"), size=1100, bold=True, color=WHITE, line=1250)
    g.put(a, e, 6, 7, [value], frame(top="dot", left="dot", right="dot"), line=1400)
    g.put(a, e, 7, 8, head, frame("#CBCBCB", left="dot", right="dot"), size=1150, bold=True)
    g.put(a, e, 8, 9, items, frame(bottom="dot", left="dot", right="dot"), align="LEFT", line=1400)
block(g, 594.5)

g = Grid("note", [X0, X1], [1100])
g.put(X0, X1, 0, 1, [line1(55, 60, 790, 795)], align="LEFT", line=1000)
block(g, 790.8)

kit.finish(target, end=802.0)
