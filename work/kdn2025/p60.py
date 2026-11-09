"""Rebuild KDN 2025 report PDF page 60 (second PDF local page 10, printed page 37) as editable HWPX.

Usage: python3 work/kdn2025/p60.py <report2.pdf> <out.hwpx> [--page 10]

안전 및 재난관리 "Ⅲ. 세부 평가내용별 추진실적" opening page. Only the title, the 평가내용 title
and the section band "1 ..." are in the PDF text layer. Everything from y 188 to 802 (the
안전보건경영 체계도: 경영방침, 환경분석, 산업재해 현황분석, 추진목표/방향/과제, 성과지표, 관리체계
and the 안전보건 인프라 charts) is one image; its text was read from 4-8x renders and typed into
editable cells on the diagram's own grid (label column | content). Built with the shared kit.

Glyph choices for image-only fragments: list dots -> "·", the dark boxed task numbers 1-6 ->
①-⑥, bold up arrows in the chart tags -> "↑", the curly brace under 성과지표 -> a bracket cell
and "▼". Superscript years (’24년, ’30년 ...) are small runs on the baseline. The four bar charts
of 안전보건 인프라 keep only their printed values (no bars); the decorative tabs and arrows are
omitted. "•노·사" (no space after the dot) is kept as printed.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kit  # noqa: E402
from kit import Layout, recipe_inputs  # noqa: E402

source, target = recipe_inputs(10, "산업재해 예방과 안전한 일터 구현을 위한 예방중심 안전보건경영체계 고도화")
L = Layout(top=3100)
kit.setup(source, L)
from kit import *  # noqa: E402,F401,F403  helpers and presets bound to this page

LABEL, LABEL2, LIGHT = "#C0C0C0", "#E4E4E4", "#E6E6E6"
LX, CX0 = 111.0, 121.0          # label column end, content start


def m(text, size=1000, bold=False, color=INK, small=0.82, sup=0.58):
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


def label(g, r0, r1, lines, fill=LABEL, size=1000, bold=False, color=INK):
    g.put(X0, LX, r0, r1, [m(t, size, bold, color) for t in lines], frame(fill), line=1200)


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
g.put(X0, X1, 0, 1, [line1(195, 205, 68, 75)])
block(g, 68.5)

# 평가내용 01 band (chip image typed, title from the text layer)
g = Grid("band", [X0, 124.0, X1], [1950, 2130])
g.put(X0, 124.0, 0, 1, "평가내용 01", frame("#565656", top="strong"), size=970, bold=True, color=WHITE, ratio=80)
g.put(X0, 124.0, 1, 2, [], frame("#E9E9E9", bottom="soft", left="soft", hatch="#DADADA"))
g.put(124.0, X1, 0, 2, lines_in(125, 130, 108, 140), frame("#E9E9E9", top="strong", bottom="soft",
                                                           right="soft", hatch="#DADADA"), align="LEFT", line=1480)
block(g, 106.0)

# Section band "1 산업재해 예방과 ..." (number box and band are images, text from the text layer)
g = Grid("section", [X0, 85.5, X1], [2230])
g.put(X0, 85.5, 0, 1, [runs_of(line1(64, 70, 160, 165), WHITE)], frame("#606060"), line=1850)
g.put(85.5, X1, 0, 1, [line1(90, 95, 160, 166)], frame("#E4E4E4"), align="LEFT", line=1750)
block(g, 159.2)

# ---------------------------------------------------------------------------
# 안전보건경영 체계도 (image in the PDF; text read from 4-8x renders)
# ---------------------------------------------------------------------------
g = Grid("policy", [X0, LX, CX0, X1], [2900])
label(g, 0, 1, ["안전보건", "경영방침"])
g.put(CX0, X1, 0, 1, "협력사를 포함, 모든 구성원의 생명 보호와 안전한 작업환경 조성은 경영의 핵심 책무",
      frame("#EDEDED", hatch="#DCDCDC"), size=1200, bold=True)
block(g, 188.5)

xs = [X0, LX, CX0, 336.0, 341.8, X1]
g = Grid("environment", xs, [1650, 3300])
label(g, 0, 2, ["환경분석"])
for a, e, head, items in (
        (CX0, 336.0, "외부환경", ["· 강도 높은 노동안전정책 “안전은 사회적 책무” 요구",
                                 "· OECD 평균 사고사망만인율{(0.39}^’24년^{→0.29}^’30년^{)} 달성"]),
        (341.8, X1, "내부환경", ["· 기관장 확고한 안전경영 의지, 안전 전담조직 강화",
                                "· 고위험 작업장 상존, 근로자 직접 작업 사고 위험 노출"])):
    g.put(a, e, 0, 1, head, frame("#B4B4B4"), size=1100, bold=True)
    g.put(a, e, 1, 2, [m(t, 1050) for t in items], frame(left="soft", right="soft", bottom="soft"),
          align="LEFT", line=1450)
block(g, 224.0)

xs = [X0, LX, CX0, 262.0, 266.5, 408.0, 412.0, X1]
g = Grid("accidents", xs, [2140, 3540])
label(g, 0, 2, ["산업재해", "현황분석"])
for a, e, head, lines in (
        (CX0, 262.0, "작업장 사고", ["’24년 국내 산업재해", "사고 사망자 589명"]),
        (266.5, 408.0, "아차사고", ["’23년 국토부 아차사고 445건 中", "‘관리적 요인’이 45% 차지"]),
        (412.0, X1, "건설현장 재해", ["’24년 국내 전체 산업재해 사망자 中", "건설업이 49% 차지{(추락 51%)}"])):
    g.put(a, e, 0, 1, head, frame(top="mid", left="mid", right="mid"), size=1100)
    g.put(a, e, 1, 2, [m(t, 1050) for t in lines], frame("#E9E9E9"), line=1400)
block(g, 279.2)

g = Grid("goal", [X0, LX, X1], [2940])
label(g, 0, 1, ["추진목표"], "#A8A8A8", bold=True, color=WHITE)
g.put(LX, X1, 0, 1, "안전한 일터 조성을 위한 실행중심 안전보건관리 수준 Jump-UP", frame("#787878"),
      size=1250, bold=True, color=WHITE)
block(g, 339.8)

xs = [X0, LX, CX0, 263.0, 267.2, 408.5, 414.2, X1]
g = Grid("direction", xs, [2300])
label(g, 0, 1, ["추진방향"], LABEL2)
for a, e, text in ((CX0, 263.0, "예방중심 안전경영 UP"), (267.2, 408.5, "안전한 근로환경 UP"),
                   (414.2, X1, "협력사 안전 자생력 UP")):
    g.put(a, e, 0, 1, text, frame("#D8D8D8"), size=1100, bold=True)
block(g, 374.6)

cols = ((CX0, 175.8, 205.8, 266.5), (266.5, 323.0, 354.0, 410.5), (410.5, 471.0, 501.5, X1))
xs = [X0, LX] + [x for col in cols for x in col[:3]] + [X1]
g = Grid("tasks", xs, [1300, 1800, 1500, 1520])
label(g, 0, 4, ["추진과제"], LABEL2)
titles = ("안전보건경영체계 강화", "위험 선제적 제거", "협력사·건설안전 레벨업")
items = (("①", "기관장 주도 안전과제·위험구조 정비"), ("②", "시스템기반 예방·위기 대응 능력 강화"),
         ("③", "참여중심 안전의식↑·보건 사각지대↓"), ("④", "현장중심 위험제거·선제적 안전 강화"),
         ("⑤", "과감한 자원 투입기반 예방체계 강화"), ("⑥", "상생기반 협력사 안전관리 역량 육성"))
for k, ((a, t0, t1, e), title) in enumerate(zip(cols, titles)):
    sep = "dot" if k else None
    g.put(a, t0, 0, 1, [], frame(LIGHT, top="mid", left=sep))
    g.put(t0, t1, 0, 1, f"{k + 1:02}", frame("#6E6E6E", top="mid"), size=1000, bold=True, color=WHITE, line=1100)
    g.put(t1, e, 0, 1, [], frame(LIGHT, top="mid"))
    g.put(a, e, 1, 2, title, frame(LIGHT, left=sep), size=1050)
    for r in (2, 3):
        num, text = items[2 * k + r - 2]
        g.put(a, e, r, r + 1, [[(num + " ", 1000, True, INK), (text, 1000, False, INK)]],
              frame(left=sep, bottom="soft" if r == 3 else None), align="LEFT", line=1150)
block(g, 402.8)

g = Grid("kpi", [X0, LX, CX0, 266.5, 410.5, X1], [2450])
label(g, 0, 1, ["성과지표"], LABEL2)
for (a, e), text, kw in (((CX0, 266.5), "중대산업재해(건)", dict(left="mid", right="dot")),
                         ((266.5, 410.5), "안전관리 등급심사", dict(right="dot")),
                         ((410.5, X1), "건설재해(건)", dict(right="mid"))):
    g.put(a, e, 0, 1, text, frame(top="mid", bottom="mid", **kw), size=1050)
block(g, 469.0)

# the curly brace joining the three columns into the two-column 관리체계 below
g = Grid("brace", [X0, LX, CX0, 330.0, 346.0, X1], [700, 1150, 1130])
g.put(CX0, X1, 1, 2, [], frame(left="mid", right="mid", bottom="mid"))
g.put(330.0, 346.0, 2, 3, "▼", size=700, color="#9A9A9A", line=800)
block(g, 495.0)

xs = [X0, LX, CX0, 153.0, 333.8, 342.0, 374.0, X1]
g = Grid("system", xs, [2270, 5700, 2900, 5530])
label(g, 0, 4, ["안전보건", "관리체계"], LABEL2)
blocks = (
    ((CX0, 153.0, 333.8), [
        ("소통", "기관장 안전 컨트롤타워 가동, 초고속 의사결정!",
         ["· 안전 전담조직 기관장 직속 격상·확대{(2개→3개부서)}",
          "· 기관장 일일 안전현황 직보 체계 가동{(피드백 34건)}",
          "·노·사 협력사 안전회의체 의장직 격상{(CSO→CEO)}"]),
        ("문화", "자율 안전문화 정착! 안전 역량 완성!",
         ["· 안전관리 전문인력 육성{(안전지도사 1명 포함, 22명)}",
          "· 자율적 안전보건활동 우수직원 선발·포상{(63명)}",
          "· 지역축제 연계 참여형 ‘안전체험존’ 개최{(3회, 1,473명)}"])]),
    ((342.0, 374.0, X1), [
        ("혁신", "중대재해 통합관리, 법적의무 이행 강화",
         ["· 중대재해통합관리시스템 구축·안전경영 이행관리",
          "· 현행 안전법 분석·안전관련 절차서 통·폐합{(20종)}",
          "· 기관 최초 유관기관 공조 재난대응 실전형 고강도 훈련"]),
        ("몰입", "스스로 책임지는 안전, 실천형 안전 활동",
         ["· 철탑 등 고위험 현장 기관장 직접 지휘{(12회}^’24년^{→21회}^’25년^{)}",
          "· 전문가 방문 위험성평가 실습 역량강화{(503명 이수)}",
          "· 협력사 안전보건체계 진단{(4개社→11개社)}, ISO45001{(2개社)}"])]))
for (a, b, e), parts in blocks:
    for r, (tag, head, lines) in zip((0, 2), parts):
        g.put(a, b, r, r + 1, tag, frame("#787878", top="soft"), size=1050, color=WHITE, line=1200)
        g.put(b, e, r, r + 1, head, frame(top="soft"), align="LEFT", size=1050, bold=True, line=1200)
        g.put(a, e, r + 1, r + 2, [m(t, 1020) for t in lines], frame(LIGHT), align="LEFT", line=1620)
block(g, 524.8)

# 안전보건 인프라: 조직 (tags + text) and three value charts (bars omitted, printed values kept)
charts = ((231.5, 266.0, 300.0, 335.5), (341.0, 376.0, 408.0, 445.0), (450.2, 484.0, 513.5, X1))
xs = [X0, LX, CX0, 142.0, 226.0] + [x for col in charts for x in col]
g = Grid("infra", xs, [2150, 1750, 1500, 1500, 1480, 2000])
label(g, 0, 6, ["안전보건", "인 프 라"], LABEL2)
head = frame(LIGHT, top="mid", left="mid", right="mid")
g.put(CX0, 226.0, 0, 1, "조  직", head, size=1100)
for (a, *_ , e), text in zip(charts, ("인  력", "교  육", "예  산")):
    g.put(a, e, 0, 1, text, head, size=1100)
pill = frame("#D2D2D2")
g.put(CX0, 142.0, 1, 2, "주 관", pill, size=950)
g.put(142.0, 226.0, 1, 2, [m("안전관리실{(41명)}", 1050)], align="LEFT")
g.put(CX0, 142.0, 2, 3, "현 장", pill, size=950)
g.put(142.0, 226.0, 2, 4, [m("본사, 사업소 부서별", 1050), m("안전담당인력{(54명)}", 1050)], align="LEFT",
      line=1400)
g.put(CX0, 142.0, 5, 6, "신 설", frame(WHITE, top="soft", bottom="soft", left="soft", right="soft"), size=950)
g.put(142.0, 226.0, 5, 6, [m("안전혁신TF{(24명)}", 1050)], frame(LIGHT), align="LEFT")
tag = frame("#3C3C3C")
for (a, b, c, e), before, rise, after, total in zip(
        charts, ("88명", "3,840명", "143억원"), ("8%↑", "44%↑", "2%↑"), ("95명", "5,536명", "146억원"),
        ("안전전담인력 7명 증가", "안전보건교육 1,696명 증가", "전년 대비 3억원 증가")):
    g.put(b, c, 1, 2, rise, tag, size=1000, bold=True, color=WHITE, line=1100)
    g.put(c, e, 1, 2, after, size=950, bold=True, line=1100)
    g.put(a, b, 2, 3, before, size=950, line=1100)
    g.put(a, e, 3, 4, [], frame(bottom="soft"))
    g.put(a, b, 4, 5, "’24년", size=900, line=1050)
    g.put(c, e, 4, 5, "’25년", size=900, bold=True, line=1050)
    g.put(a, e, 5, 6, total, frame(LIGHT), size=1100)
block(g, 698.0)

kit.finish(target, end=802.0)
