"""Rebuild KDN 2025 report page 88 (2nd PDF local page 38, printed page 58) as editable HWPX.

Usage: python3 work/kdn2025/p88.py <report2.pdf> <out.hwpx> [--page 38]

"Ⅲ. 세부 평가내용별 추진실적" opening page of the 상생･협력 및 지역발전 indicator. Only the page
title, the 평가내용 01 band, the section-1 band, the 가. heading, the 주요성과 box and the page
number are in the PDF text layer. The whole 동반성장 추진체계 diagram (y 211-758: 환경분석 ~
모니터링) is one image; its text was read from 4x-7x renders and typed into editable cells, band
by band on the diagram's own grid (label column | content). Built with the shared kit.

Glyph and shape choices for image-only fragments: list dots -> "·" (KS X 1001), the (+) joints
-> "+", the brace and the small down chevrons -> "▼", the vision arrow label and the roof of
"성과지표 달성을 위한 지원체계" -> plain gray cells; the dark tabs over the 환경분석 heads and the
short rules over the lower labels -> top borders. Printed as in the source: "에너지벨리기업개발원"
(벨리), the double space in "위한  지원 필요", "AI 선도기술 ·인재 확보" spacing.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kit  # noqa: E402
from kit import Layout, recipe_inputs  # noqa: E402

source, target = recipe_inputs(38, "동반성장 추진체계 고도화로 상생")
L = Layout(top=3100)
kit.setup(source, L)
from kit import *  # noqa: E402,F401,F403  helpers and presets bound to this page

DARK = "#6A6A6A"
SIDE = frame("#D9D9D9")             # gray label blocks (환경분석 / 니즈 / 시사점)
RULED = frame(top="mid")             # lower labels: short rule above the word
BODY = frame("#EBEBEB")
TEXT = 1090


def dot(text, small=None):
    """'· text' bullet line; small: a trailing (or inner) parenthetical printed smaller."""
    if small is None:
        return [("· " + text, TEXT, False, INK)]
    head, tail = text.split(small)
    runs = [("· " + head, TEXT, False, INK), (small, 900, False, INK)]
    return runs + [(tail, TEXT, False, INK)] if tail else runs


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

g = Grid("title", [X0, X1], [2400])
g.put(X0, X1, 0, 1, [line1(195, 205, 68, 75)])
block(g, 68.5)

# 평가내용 01 band: chip (image, typed) in the corner, hatched two-line title.
g = Grid("band", [X0, 124.0, X1], [1950, 2190])
g.put(X0, 124.0, 0, 1, "평가내용 01", frame("#565656", top="strong"), size=970, bold=True, color=WHITE, ratio=80)
g.put(X0, 124.0, 1, 2, [], frame("#E9E9E9", bottom="soft", left="soft", hatch="#DADADA"))
g.put(124.0, X1, 0, 2, lines_in(125, 130, 108, 140), frame("#E9E9E9", top="strong", bottom="soft",
                                                           right="soft", hatch="#DADADA"), align="LEFT", line=1480)
block(g, 105.5)

g = Grid("sec1", [X0, 84.5, X1], [2300])
g.put(X0, 84.5, 0, 1, [runs_of(line1(60, 70, 160, 165), WHITE)], frame(DARK), line=1700)
g.put(84.5, X1, 0, 1, [line1(90, 95, 160, 166)], frame("#E6E6E6"), align="LEFT", line=1700)
block(g, 158.9)

g = Grid("title-ga", [X0, X1], [1650])
g.put(X0, X1, 0, 1, [line1(55, 60, 188, 193)], align="LEFT", line=1450)
block(g, 189.0)

# ---------------------------------------------------------------------------
# Diagram (image in the PDF; text typed from 4x renders)
# ---------------------------------------------------------------------------
# 환경분석: three outlined heads over gray bodies; 국정과제 tags in the first column.
xs = [X0, 110.0, 114.8, 119.0, 150.5, 257.8, 263.1, 406.0, 411.3, X1]
g = Grid("env", xs, [2120, 630, 1380, 1380, 550])
g.put(X0, 110.0, 0, 5, "환경분석", SIDE, size=1050)
for a, e, text in ((114.8, 257.8, "정부정책"), (263.1, 406.0, "경영환경"), (411.3, X1, "ESG경영전략")):
    g.put(a, e, 0, 1, text, frame(top="strong", left="mid", right="mid"), size=1150)
g.put(114.8, 257.8, 1, 2, [], BODY)
for r, tag, text in ((2, "국정22번", "AI 선도기술 ·인재 확보"), (3, "국정35번", "성장 ·도약하는 중소기업")):
    g.put(114.8, 119.0, r, r + 1, [], BODY)
    g.put(119.0, 150.5, r, r + 1, tag, frame("#5E5E5E"), size=760, color=WHITE, line=900)
    g.put(150.5, 257.8, r, r + 1, text, BODY, align="LEFT", line=1200)
g.put(114.8, 257.8, 4, 5, [], BODY)
g.put(263.1, 406.0, 1, 5, [dot("AI · 데이터 기반 서비스 경쟁 심화"), dot("공급망 전반의 ESG 관리 체계 필요")], BODY,
      align="LEFT", line=1380)
g.put(411.3, X1, 1, 5, [dot("디지털 기술기반 포용사회 구현"), dot("지속가능한 사회적 가치 창출")], BODY,
      align="LEFT", line=1380)
block(g, 211.3)

# 중소기업･소상공인･사회적기업 니즈: four gray cells.
g = Grid("needs", [X0, 110.0, 114.8, 331.5, 336.8, X1], [2020, 450, 2000])
g.put(X0, 110.0, 0, 3, ["중소기업", "소상공인", "사회적기업", "니즈"], SIDE, size=1000, line=1050)
for r, left, right in ((0, "신기술 R&D 지원, 신시장 진입장벽 완화 필요", "경쟁력 강화와 지속성장을 위한  지원 필요"),
                       (2, "사회적 경제 기업, 소상공인 지원 확대", "납품대금 지연 및 불공정 계약위험 해소")):
    g.put(114.8, 331.5, r, r + 1, left, BODY, size=TEXT)
    g.put(336.8, X1, r, r + 1, right, BODY, size=TEXT)
block(g, 277.0)

# 시사점 도출: outlined box with four dark-tagged findings.
xs = [X0, 110.0, 115.6, 119.4, 182.5, 331.5, 336.8, 398.4, 549.9, X1]
g = Grid("insights", xs, [380, 2150, 420, 2100, 560])
g.put(X0, 110.0, 0, 5, ["시 사 점", "도      출"], SIDE, size=1050, line=1250)
g.put(115.6, X1, 0, 1, [], frame(top="mid", left="mid", right="mid"))
g.put(115.6, X1, 2, 3, [], frame(left="mid", right="mid"))
g.put(115.6, X1, 4, 5, [], frame(bottom="mid", left="mid", right="mid"))
tag = frame("#6E6E6E")
for r, (t1, x1, t2, x2) in ((1, ("기술사업화 지원", "기술개발 사업화, 판로연계 구조 강화", "동반성장 추진", "경쟁력 강화 및 성장 지원 방안 이행")),
                            (3, ("사회적 가치 창출", "사회적 경제기업, 소상공인 맞춤 지원 강화", "공정거래 확립", "계약제도 개선 및 리스크 관리 강화"))):
    g.put(115.6, 119.4, r, r + 1, [], frame(left="mid"))
    g.put(119.4, 182.5, r, r + 1, t1, tag, size=1050, bold=True, color=WHITE)
    g.put(182.5, 331.5, r, r + 1, x1, BODY, align="LEFT", size=1050)
    g.put(331.5, 336.8, r, r + 1, [])
    g.put(336.8, 398.4, r, r + 1, t2, tag, size=1050, bold=True, color=WHITE)
    g.put(398.4, 549.9, r, r + 1, x2, BODY, align="LEFT", size=1050)
    g.put(549.9, X1, r, r + 1, [], frame(right="mid"))
block(g, 328.0)

g = Grid("brace", [X0, 110.0, X1], [1050])
g.put(110.0, X1, 0, 1, "▼", frame(top="soft"), size=1000, color=ARROW, line=850)
block(g, 391.0)

# 동반성장 비전 band.
g = Grid("vision", [X0, 110.0, X1], [430, 2470, 690])
g.put(X0, 110.0, 0, 3, ["동반성장", "비전"], frame("#A8A8A8"), size=1150, bold=True, color=WHITE, line=1300)
g.put(110.0, X1, 0, 1, [])
g.put(110.0, X1, 1, 2, "중소기업과 함께 성장하는 Energy ICT 리더, 한전KDN", frame("#6E6E6E"), size=1250,
      color=WHITE)
g.put(110.0, X1, 2, 3, [])
block(g, 407.0)

# 전략과제 / 실행과제 / 성과지표: four columns.
cols = ((111.8, 221.2, 153.0, 176.0), (221.2, 333.8, 263.3, 286.6), (333.8, 445.9, 375.0, 398.2),
        (445.9, X1, 486.5, 509.8))
xs = sorted({X0, 107.0} | {x for c in cols for x in c})
g = Grid("tasks", xs, [1200, 650, 3700])
g.put(X0, 107.0, 0, 2, "전략과제", RULED, size=1050)
g.put(X0, 107.0, 2, 3, [])
titles = (("중소기업 全주기 기술", "협력을 통한 성장 견인"), ("중소기업 동반성장", "생태계 구축"),
          ("지역 산업생태계 연계", "사회적경제 상생모델 구축"), ("계약체계 고도화로", "공정한 경제질서 확립"))
gray = "#E6E6E6"
for k, ((a, e, t0, t1), pair) in enumerate(zip(cols, titles)):
    sep = dict(right="dot") if k < 3 else {}
    g.put(a, t0, 0, 1, [], frame(gray, top="soft"))
    g.put(t0, t1, 0, 1, f"{k + 1:02}", frame("#5E5E5E"), size=1000, bold=True, color=WHITE, line=1000)
    g.put(t1, e, 0, 1, [], frame(gray, top="soft", **sep))
    g.put(a, e, 1, 3, list(pair), frame(gray, **sep), size=TEXT, line=1500)
block(g, 452.5)

actions = ((dot("기술협력 체계 정립"), dot("공공분야 실증 및 조달지원")),
           (dot("동반성장 협력사업 강화"), dot("기관 시장 참여 구조 개선")),
           (dot("사회적경제 맞춤육성 지원"), dot("사회적경제 판로개척 지원")),
           (dot("공정계약 체계 개선"), dot("‘KDN Fair’ 공정문화 확산")))
xs = [X0, 107.0, 111.8, 221.2, 333.8, 445.9, X1]
g = Grid("actions", xs, [2320, 1640, 960])
g.put(X0, 107.0, 0, 1, "실행과제", RULED, size=1050)
g.put(X0, 107.0, 1, 3, [])
for k, ((a, e, *_), pair) in enumerate(zip(cols, actions)):
    edges = dict(top="mid", bottom="mid", right="dot" if k < 3 else "mid")
    if k == 0:
        edges["left"] = "mid"
    g.put(a, e, 0, 2, list(pair), frame(**edges), align="LEFT", line=1640)
    g.put(a, e, 2, 3, "▼", size=600, color="#8C8C8C", line=600)
block(g, 514.4)

indicators = ((dot("기관주도 사업화 성공 사례"), dot("R&D 성과물 사업화실적")),
              (dot("생산성 등 성과지표 달성율"), dot("공동수주 계약건수 및 금액")),
              (dot("지원기업 매출액 증가율"), dot("사회적경제기업 수출 실적")),
              (dot("공정거래 인식도"), dot("하도급지킴이 이용 실적")))
boxes = ((111.8, 219.1), (223.7, 331.5), (336.0, 443.9), (448.1, X1))
xs = sorted({X0, 107.0} | {x for b in boxes for x in b})
g = Grid("indicators", xs, [2240, 1680])
g.put(X0, 107.0, 0, 1, "성과지표", RULED, size=1050)
g.put(X0, 107.0, 1, 2, [])
for (a, e), pair in zip(boxes, indicators):
    g.put(a, e, 0, 2, list(pair), frame(gray), align="LEFT", line=1500)
block(g, 563.6)

g = Grid("roof", [X0, 107.0, 111.8, 200.0, 462.0, X1], [3000])
g.put(200.0, 462.0, 0, 1, "성과지표 달성을 위한 지원체계", frame("#EBEBEB"), size=TEXT, bold=True)
block(g, 602.8)

# 지원체계: three boxes (gray head, outlined body) joined by + badges.
boxes = ((111.0, 251.0), (260.0, 402.0), (411.0, X1))
support = (("운영조직", [dot("상생협력 전담부서 운영(12명)", "(12명)"), dot("기술마켓 전문인력 배치(34명)", "(34명)"),
                       dot("ESG위원회 · 자문회의 운영")]),
           ("인프라", [dot("中企지원 홈페이지, 입찰시스템 운영"), dot("AI산업 육성 특화 펀드 확대 운영"),
                    dot("디지털 ESG 통합관리 시스템 구축")]),
           ("협의체", [dot("에너지벨리기업개발원, 대학교"), dot("중소기업중앙회, 동반성장위원회"),
                    dot("지자체(전남도) · 광주테크노파크", "(전남도)")]))
xs = sorted({X0, 107.0} | {x for b in boxes for x in b})
g = Grid("support", xs, [1300, 570, 580, 5050])
g.put(X0, 107.0, 0, 2, "지원체계", RULED, size=1050)
g.put(X0, 107.0, 2, 4, [])
for k, ((a, e), (head, lines)) in enumerate(zip(boxes, support)):
    g.put(a, e, 0, 2, head, frame("#D9D9D9", top="soft", left="soft", right="soft"), size=1150, bold=True)
    g.put(a, e, 2, 4, lines, frame(left="soft", right="soft", bottom="soft"), align="LEFT", line=1680)
    if k < 2:
        b = boxes[k + 1][0]
        g.put(e, b, 0, 1, [])
        g.put(e, b, 1, 3, "+", size=900, bold=True, color="#9A9A9A", line=900, fit=False)
        g.put(e, b, 3, 4, [])
block(g, 633.5)

g = Grid("monitoring", [X0, 107.0, 111.8, 352.0, X1], [2270, 2280])
g.put(X0, 107.0, 0, 1, "모니터링", RULED, size=1050)
g.put(X0, 107.0, 1, 2, [])
hatched = frame("#EEEEEE", hatch="#E2E2E2")
g.put(111.8, 352.0, 0, 2, [dot("ESG 추진단 회의(반기)"), dot("동반성장 지원사업 추진현황 및 실적관리(분기)")], hatched,
      align="LEFT", line=1700)
g.put(352.0, X1, 0, 2, [dot("주요사업 분야 · 지역별 중소기업 간담회(수시)"), dot("기업성장응답센터 상시 운영")], hatched,
      align="LEFT", line=1700)
block(g, 712.3)

# 주요성과 (text layer).
g = Grid("result", [X0, 111.7, X1], [3710])
g.put(X0, 111.7, 0, 1, [runs_of(line1(65, 70, 776, 781), WHITE)], frame(DARK, top="mid", bottom="mid", left="mid"))
g.put(111.7, X1, 0, 1, lines_in(115, 120, 765, 790), frame(top="mid", bottom="mid", right="mid"), align="LEFT")
block(g, 764.9)

kit.finish(target, end=802.0)
