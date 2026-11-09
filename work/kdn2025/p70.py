"""Rebuild KDN 2025 report page 70 (second PDF local page 20, printed page 44) as editable HWPX.

Usage: python3 work/kdn2025/p70.py <report2.pdf> <out.hwpx> [--page 20]

"Ⅲ. 세부 평가내용별 추진실적" opening page of the 친환경·탄소중립 indicator (same page type as
p36). Only the title, the 평가내용 01 band, the section band and the 주요성과 box are in the
PDF text layer. The whole strategy diagram (y 173-758: 기관장 신년사 quote, 환경분석, 시사점,
ESG 전략 고도화, ESG VISION, 2035 중장기 목표, 추진방향, 추진과제, 성과지표, 실행체계) is one image:
its text was read from 4x renders and typed into editable cells on the diagram's own grid
(label column | content). The 지적사항 개선 sticker is a separate image, typed as a dark tag.
Icons (plants, wind turbine, globe, hand) are omitted; the ◐ joints of 시사점 become ▶, the
brace below 시사점 becomes ▼, list dots become "·". The italic quote is set upright (bold).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kit  # noqa: E402
from kit import Layout, recipe_inputs  # noqa: E402

source, target = recipe_inputs(20, "환경보전 및 탄소저감 기술 확산으로")
L = Layout(top=3100)
kit.setup(source, L)
from kit import *  # noqa: E402,F401,F403  helpers and presets bound to this page

DARK, LABEL, LABEL2 = "#6A6A6A", "#E3E3E3", "#C4C4C4"
BODY, SMALL = 1000, 820


def R(*parts, bold=False, color=INK):
    """Typed runs: (text, size) pairs, size defaults to BODY."""
    out = []
    for part in parts:
        text, size = (part, BODY) if isinstance(part, str) else part
        out.append((text, size, bold, color))
    return out


def dot(*parts):
    first, *rest = parts
    first = ("· " + first, BODY) if isinstance(first, str) else ("· " + first[0], first[1])
    return R(first, *rest)


def label(g, r0, r1, text, fill=None, top=True):
    """Left label column: plain text under a thin rule (the PDF's rule with a dark mid tick)."""
    lines = text if isinstance(text, list) else [text]
    g.put(X0, 110.0, r0, r1, [R((t, 1100)) for t in lines],
          frame(fill, top="soft") if fill is None and top else frame(fill) if fill else "1", line=1300)


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

# 평가내용 01 band: dark chip (image, typed; its check mark is dropped) over a hatched strip.
g = Grid("band", [X0, 124.0, X1], [1750, 1100])
g.put(X0, 124.0, 0, 1, [[("평가내용 ", 800, True, WHITE), ("01", 1350, True, WHITE)]],
      frame("#565656", top="mid", left="mid"), line=1500)
g.put(X0, 124.0, 1, 2, [], frame("#E9E9E9", bottom="mid", left="mid", hatch="#DADADA"))
g.put(124.0, X1, 0, 2, [line1(125, 130, 110, 116)], frame("#E9E9E9", top="mid", bottom="mid", right="mid",
                                                            hatch="#DADADA"), align="LEFT", line=1450)
block(g, 105.5)

g = Grid("section", [X0, 86.0, X1], [2300])
g.put(X0, 86.0, 0, 1, [runs_of(line1(64, 70, 147, 152), WHITE)], frame(DARK), line=1800)
g.put(86.0, X1, 0, 1, [line1(90, 95, 147, 152)], frame("#E3E3E3"), align="LEFT", line=1700)
block(g, 146.1)

# ---------------------------------------------------------------------------
# Strategy diagram (one image in the PDF; text read from 4x renders)
# ---------------------------------------------------------------------------
g = Grid("quote", [X0, X1], [3060])
g.put(X0, X1, 0, 1, [R(("“디지털 혁신과 플랫폼 중심의 기술력으로 사회적 책임과 환경적 가치 확대”", 1200),
                       (" (기관장 신년사, 1월)", 1200), bold=True, color=WHITE)], frame("#5A5A5A"), line=1450)
block(g, 175.6)

# 환경분석: 외부환경 | 내부환경, three tagged findings each (dark tag pills, dashed separators).
xs = [X0, 110.0, 115.5, 120.0, 163.0, 331.0, 340.0, 344.5, 387.0, X1]
hs = [2050] + [450, 1380, 450] * 3
g = Grid("env", xs, hs)
label(g, 0, 10, "환경분석", LABEL)
items = {
    (115.5, 120.0, 163.0, 331.0, "외부환경"): [
        ("글 로 벌", R("글로벌 기후 규제 및 공시 요구 강화")),
        ("정부정책", R("재생에너지 중심 에너지 전환", ("(국정39)", SMALL))),
        ("기후위기", R("기후위기 관련 선제적 대응 활동 중요"))],
    (340.0, 344.5, 387.0, X1, "내부환경"): [
        ("I  C  T", R("ICT 역량 기반 탄소 저감 기술 개발 및 보유")),
        ("온실가스", R("신축 사옥, 데이터 센터 등 배출량 증가 위험")),
        ("환경경영", R("자체 환경 브랜드 지속 운영 및 확대 필요"))]}
for (a, b, c, e, head), rows in items.items():
    g.put(a, e, 0, 1, head, frame(top="mid", left="mid", right="mid"), size=1100)
    for k, (tag, text) in enumerate(rows):
        r = 1 + 3 * k
        edge = "dot" if k < 2 else None
        g.put(a, b, r, r + 3, [], frame("#F0F0F0", bottom=edge))
        g.put(b, c, r, r + 1, [], frame("#F0F0F0"))
        g.put(b, c, r + 1, r + 2, tag, frame("#6E6E6E"), size=950, color=WHITE, line=1150)
        g.put(b, c, r + 2, r + 3, [], frame("#F0F0F0", bottom=edge))
        g.put(c, e, r, r + 3, [text], frame("#F0F0F0", bottom=edge), align="LEFT")
block(g, 212.0)

# 시사점: gray tab ▶ three-line finding, twice.
xs = [X0, 110.0, 115.5, 164.0, 172.0, 331.0, 340.0, 388.0, 396.0, X1]
g = Grid("implication", xs, [5030])
label(g, 0, 1, "시사점", LABEL2)
for a, b, c, e, tag, lines in (
        (115.5, 164.0, 172.0, 331.0, "탄소중립",
         ["業의 특성을 살린 에너지 ICT 플랫폼", "개발로 재생에너지 확산 및 실질적인", "온실가스 감축 노력 필요"]),
        (340.0, 388.0, 396.0, X1, "친환경",
         ["친환경 브랜드 「KDN Eco-Life」 확산", "및 대외 소통 강화를 통한 기관의", "환경경영 신뢰 확보 중요"])):
    g.put(a, b, 0, 1, tag, frame("#E3E3E3"), size=1050)
    g.put(b, c, 0, 1, "▶", size=700, color="#7A7A7A", fit=False)
    g.put(c, e, 0, 1, [R(t) for t in lines], frame(top="dot", bottom="dot"), align="LEFT", line=1380)
block(g, 307.1)

g = Grid("brace", [X0, 110.0, 115.5, X1], [1500])
g.put(115.5, X1, 0, 1, "▼", frame(top="soft"), size=800, color=ARROW, line=900)
block(g, 359.5)

# ESG 전략 고도화: hatched strip in three parts.
xs = [X0, 110.0, 115.5, 260.0, 410.0, X1]
g = Grid("esg-strategy", xs, [2800])
label(g, 0, 1, ["ESG 전략", "고도화"])
for k, (a, e, text) in enumerate(((115.5, 260.0, "NEW 비전 설정"), (260.0, 410.0, "중장기 목표 구체화 및 세분화"),
                                  (410.0, X1, "환경(E) 전략 추진 과제발굴"))):
    g.put(a, e, 0, 1, text, frame("#ECECEC", left="dot" if k else None, hatch="#DEDEDE"), size=1050)
block(g, 375.5)

g = Grid("vision", [X0, 110.0, X1], [2850])
g.put(X0, 110.0, 0, 1, [R(("ESG", 1150), color=WHITE), R(("VISION", 1150), color=WHITE)], frame("#A9A9A9"),
      line=1300)
g.put(110.0, X1, 0, 1, "Digital ESG로 열어가는 지속 가능한 미래", frame("#7A7A7A"), size=1150, color=WHITE)
block(g, 409.5)

# 2035 중장기 목표: three gray boxes (icons above them omitted).
B3 = ((115.5, 255.3), (265.0, 405.0), (415.4, X1))
xs = [X0, 110.0, 115.5, 255.3, 265.0, 405.0, 415.4, X1]
g = Grid("goals", xs, [1900, 5700])
label(g, 0, 2, ["2035", "중장기 목표"])
for (a, e), lines in zip(B3, (["온실가스 배출량", "60% 감축"], ["신재생에너지 서비스", "2,600억원 달성"],
                              ["ESG 평가", "최우수 등급"])):
    g.put(a, e, 1, 2, [R((t, 1100)) for t in lines], frame("#D6D6D6"), line=1450)
block(g, 446.0)

# 추진방향: numbered tab on a light box.
xs = [X0, 110.0, 115.5, 169.9, 200.9, 255.3, 265.0, 319.5, 350.5, 405.0, 415.4, 469.8, 500.8, X1]
g = Grid("direction", xs, [1300, 3800])
label(g, 0, 2, "추진방향")
for k, ((a, e), lines) in enumerate(zip(B3, (["탄소중립 달성을 위한", "온실가스 감축 전략 이행"],
                                             ["재생에너지 전환을 위한", "친환경 에너지 ICT 플랫폼 확산"],
                                             ["KDN 業의 특성을 살린", "대국민 소통 및 친환경 활동 강화"]))):
    c0, c1 = xs[3 + 4 * k], xs[4 + 4 * k]
    g.put(a, c0, 0, 1, [], frame("#E6E6E6", top="mid"))
    g.put(c0, c1, 0, 1, f"0{k + 1}", frame("#6A6A6A"), size=950, bold=True, color=WHITE, line=1100)
    g.put(c1, e, 0, 1, [], frame("#E6E6E6", top="mid"))
    g.put(a, e, 1, 2, [R((t, 1100)) for t in lines], frame("#E6E6E6"), line=1450)
block(g, 530.2)


def bullet_box(name, head, columns, top, height):
    """추진과제 / 성과지표: one outlined box, three dashed-separated bullet columns."""
    xs = [X0, 110.0, 115.5, 260.0, 410.0, X1]
    g = Grid(name, xs, [height])
    label(g, 0, 1, head)
    for k, ((a, e), items) in enumerate(zip(((115.5, 260.0), (260.0, 410.0), (410.0, X1)), columns)):
        g.put(a, e, 0, 1, items, frame(top="mid", bottom="mid", left="mid" if k == 0 else "dot",
                                       right="mid" if k == 2 else None), align="LEFT", line=1500)
    block(g, top)


bullet_box("tasks", "추진과제",
           [[dot("실질적 감축 추진 및 관리 디지털化"), dot("지속가능한 감축을 위한 기술 협력")],
            [dot("AI 기반 재생E 기술 지속 확산"), dot("EVC 기술 기반 친환경 인프라 확대")],
            [dot("KDN Eco-Life 다채널 소통 확대"), dot("기후위기 대응 및 자원순환 실천")]], 589.0, 3930)
bullet_box("kpi", "성과지표",
           [[dot("온실가스 감축 목표 달성률", ("(%)", SMALL)), dot("외부 감축 사업 누적 실적", ("(%)", SMALL))],
            [dot("AI 기반 재생E 예측 정확도", ("(%)", SMALL)), dot("에너지 ICT 솔루션 확보 건수", ("(건)", SMALL))],
            [dot("환경 실천 프로그램 참여 인원", ("(명)", SMALL)),
             dot("자원순환 부문 온실가스 감축률", ("(%)", SMALL))]], 635.9, 3910)

# 실행체계: four heads (the last one an arrow in the PDF) over dashed-separated bodies.
xs = [X0, 110.0, 115.5, 220.1, 222.9, 226.5, 331.8, 334.8, 338.1, 443.2, 447.0, 449.6, X1]
g = Grid("execution", xs, [2000, 350, 1150, 3770])
g.put(X0, 110.0, 0, 1, [R(("실행체계", 1100))], frame(top="soft"), line=1300)
g.put(X0, 110.0, 2, 3, "지적사항 개선", frame("#3C3C3C"), size=800, bold=True, color=WHITE, line=950)
for (a, e), head, fill in (((115.5, 220.1), "전략수립", "#E3E3E3"), ((226.5, 331.8), "추진기구", "#D3D3D3"),
                           ((338.1, 443.2), "성과관리", "#BDBDBD"), ((449.6, X1), "환류체계", "#ABABAB")):
    g.put(a, e, 0, 1, head, frame(fill), size=1100, bold=True)
BODY, S = 950, 820
bodies = [
    [R("2035 ESG 전략 고도화 및"), R("전략 추진 과제 구체화"), R(("(9개 과제, 23개 Action item)", S))],
    [R("환경이행조직 개편", ("(팀 → 부 격상)", S), " 및"), R("심의 · 의결기구 통합"), R(("(ESG 위원회 +ESG 자문단)", S))],
    [R("KPI 「ESG 전략 이행성과」개편으로"), R("중장기 전략연계성 강화"), R(("(평가항목 3건 구체화)", S))],
    [R("환경경영시스템", ("(ISO14001)", S), " 인증 및"), R("TCFD 가이드라인 기반"), R("환경 활동 점검", ("(연1회)", S))]]
for k, ((a, e), lines) in enumerate(zip(((115.5, 222.9), (222.9, 334.8), (334.8, 447.0), (447.0, X1)), bodies)):
    g.put(a, e, 1, 4, lines, frame(bottom="soft", left="soft" if k == 0 else "dot", right="soft" if k == 3 else None),
          line=1450)
block(g, 684.5)

# ---------------------------------------------------------------------------
# 주요성과 (text layer)
# ---------------------------------------------------------------------------
g = Grid("result", [X0, 111.7, X1], [3710])
g.put(X0, 111.7, 0, 1, [runs_of(line1(65, 70, 775, 780), WHITE)], frame(DARK, top="mid", bottom="mid", left="mid"))
g.put(111.7, X1, 0, 1, lines_in(115, 120, 765, 800), frame(top="mid", bottom="mid", right="mid"), align="LEFT",
      line=1500)
block(g, 764.5)

kit.finish(target, end=803.0)
