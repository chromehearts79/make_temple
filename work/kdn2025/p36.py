"""Rebuild KDN 2025 report physical PDF page 36 (printed page 21) as editable HWPX.

Usage: python3 work/kdn2025/p36.py <report.pdf> <out.hwpx> [--page N]

"Ⅲ. 세부 평가내용별 추진실적" opening page of the 윤리경영 indicator (same page type as the
skill recipe kdn_p50.py). Only the title, the 평가내용 band, the section band, the □ heading and
the 주요성과 box are in the PDF text layer. The whole 윤리경영 추진체계 diagram (y 208-736) is
one image: its text was read from 4x renders and typed into editable cells, row by row on the
diagram's own grid (label column | content), with the source's pills, tabs and dashed column
separators turned into fills and borders.

Glyph choices for image-only fragments: list dots -> "·", the (+) joints -> "+", the down chevron
-> "▼". The small boxed 신규/개정 tags and the dark 개선 tag stay inline as runs with a
character border / character shade (Hancom 글자 테두리 / 음영); the PART box and the KDN logo
in the footer are typed.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kit  # noqa: E402
from kit import Layout, recipe_inputs  # noqa: E402

source, target = recipe_inputs(36, "새로운 시작, 기관장의 강력한 리더십으로")
L = Layout(top=3200)
kit.setup(source, L)
from kit import *  # noqa: E402,F401,F403  helpers and presets bound to this page

TOP = []                      # first paragraphs of top-aligned cells
BOXED, SHADED = "#161617", "#161618"   # run colours re-mapped to tag char styles at the end
LABEL = frame("#E3E3E3")
SOFT = "soft"


def put(g, x0, x1, r0, r1, content, fill="1", *, top=False, **kw):
    g.put(x0, x1, r0, r1, content, fill, **kw)
    if top:
        TOP.append(g.items[r0, g.xs.index(to_x(x0))][3][0])


def dot(text, size=900, *tags):
    """'· text' bullet; tags: (word, kind) appended as small boxed / shaded runs."""
    runs = [("· " + text, size, False, INK)]
    for word, kind in tags:
        runs += [(" ", size, False, INK), (word, 780, kind == "dark", BOXED if kind == "box" else SHADED)]
    return runs


def side(**edges):
    return frame(**{k: SOFT if v is True else v for k, v in edges.items()})


# ---------------------------------------------------------------------------
# Page chrome (even page): PART box with rule, footer page number + KDN logo (typed).
# ---------------------------------------------------------------------------
foot = [(line1(55, 60, 816, 820)["text"], 1090, False, INK), ("    ", 790, False, INK),
        ("한전KDN㈜", 1090, True, INK)]
L.add_table([[cell(0, W, 1500, [para(foot, "LEFT", 1300)[0]])]], floating=(5660, 81550))

g = Grid("head", [X0, 99.0, 158.5, X1], [1680])
g.put(X0, 99.0, 0, 1, [[("PART ", 800, False, INK), ("01", 1300, True, INK)]], frame("#EFEFEF", top="strong"))
g.put(99.0, 158.5, 0, 1, "경영관리", frame("#333333"), size=1080, bold=True, color=WHITE)
g.put(158.5, X1, 0, 1, [], frame(bottom="soft"))
block(g, 32.0)

g = Grid("title", [X0, X1], [2400])
g.put(X0, X1, 0, 1, [line1(195, 205, 68, 75)])
block(g, 68.5)

# 평가내용 01 band (chip image typed, title from the text layer)
g = Grid("band", [X0, 124.0, X1], [1950, 2190])
g.put(X0, 124.0, 0, 1, "평가내용 01", frame("#565656", top="strong"), size=970, bold=True, color=WHITE, ratio=80)
g.put(X0, 124.0, 1, 2, [], frame("#E9E9E9", bottom="soft", left="soft", hatch="#DADADA"))
g.put(124.0, X1, 0, 2, lines_in(125, 130, 108, 145), frame("#E9E9E9", top="strong", bottom="soft",
                                                           right="soft", hatch="#DADADA"), align="LEFT", line=1480)
block(g, 105.5)

# Section band "1 새로운 시작 ..." and the □ heading
g = Grid("section", [X0, 86.9, X1], [2250])
g.put(X0, 86.9, 0, 1, [runs_of(line1(64, 70, 158, 165), WHITE)], frame("#5A5A5A"), line=1850)
g.put(86.9, X1, 0, 1, [line1(90, 95, 158, 165)], frame("#DEDEDE"), align="LEFT", line=1750)
block(g, 158.5)

g = Grid("heading", [X0, X1], [1750])
g.put(X0, X1, 0, 1, [[("□ ", 1350, True, INK)] + runs_of(line1(68, 75, 185, 190))], align="LEFT", line=1570)
block(g, 187.5)

# ---------------------------------------------------------------------------
# 윤리경영 추진체계 diagram (image in the PDF; text read from 4x renders)
# ---------------------------------------------------------------------------
# 환경분석: two boxes (대외동향 / 대내여건), each with two tagged findings.
xs = [X0, 110.5, 115.0, 152.0, 329.8, 339.8, 372.0, X1]
hs = [1850, 570, 1360, 1170, 3370, 1360, 1020, 4380]   # y 208.5 .. 360.8
g = Grid("env", xs, hs)
put(g, X0, 110.5, 0, 8, "환경분석", LABEL, size=1090)
TITLE, BODY = 960, 900
for (a, b, e), head, items in (
        ((115.0, 152.0, 329.8), "대외동향", [
            ("정 부", [[("‘특권없는 공정사회’ 로 강력 드라이브", TITLE, True, INK)]],
             [dot("공공부문의 ‘기득권 카르텔’ 척결 요구 심화"), dot("‘실용적 청렴(유능한 행정)’과 ‘적극 행정’")]),
            ("사 회", [[("‘헌법 수호’가치 부상과 ‘무관용 원칙’의", TITLE, True, INK)],
                      [("사회적 합의", TITLE, True, INK)]],
             [dot("‘법과 원칙(규범준수)’에 대한 국민적 눈높이 최고조"),
              dot("공직자의 갑질, 접대도 ‘민주적 가치 훼손’으로"),
              [("   엄벌하는 사회적 분위기 형성", BODY, False, INK)]])]),
        ((339.8, 372.0, X1), "대내여건", [
            ("위기", [[("조직 내 세대 간 인식 격차 확대 및 관행적 업무에", TITLE, True, INK)],
                     [("따른 잠재적 부패 리스크 임계치 도달", TITLE, True, INK)]],
             [dot("MZ 세대 유입 증가로 조직 구성의 변화"), dot("인적 통제 중심의 ‘아날로그식 관리’ 한계 직면")]),
            ("강 점", [[("기관장의 강력한 ‘Top-Down’ 혁신 의지와", TITLE, True, INK)],
                      [("직원 요구 증대", TITLE, True, INK)]],
             [dot("통제 가능한 시스템 기반 리스크 관리 및"), [("   실질적 행위 기준 요구 증대", BODY, False, INK)],
              [("   (명확한 기준, 안전한 신고)", BODY, False, INK)]])])):
    put(g, a, e, 0, 1, head, frame("#C9C9C9", top="soft", left="soft", right="soft"), size=1000, bold=True)
    put(g, a, b, 1, 2, [], side(left=True))
    put(g, b, e, 1, 2, [], side(right=True))
    (tag1, title1, body1), (tag2, title2, body2) = items
    pill = frame("#6E6E6E")
    put(g, a, b, 2, 3, tag1, pill, size=950, bold=True, color=WHITE)
    put(g, a, b, 3, 5, [], side(left=True))
    put(g, a, b, 5, 6, tag2, pill, size=950, bold=True, color=WHITE)
    put(g, a, b, 6, 8, [], side(left=True, bottom=True))
    if len(title1) == 1:   # 대외동향: one-line title, bullets from row 3
        put(g, b, e, 2, 3, title1, side(right=True), align="LEFT")
        put(g, b, e, 3, 5, body1, side(right=True), align="LEFT", line=1300, top=True)
    else:
        put(g, b, e, 2, 4, title1, side(right=True), align="LEFT", line=1130, top=True)
        put(g, b, e, 4, 5, body1, side(right=True), align="LEFT", line=1300, top=True)
    put(g, b, e, 5, 7, title2, side(right=True), align="LEFT", line=1110, top=True)
    put(g, b, e, 7, 8, body2, side(right=True, bottom=True), align="LEFT", line=1130, top=True)
block(g, 208.5)

# 개선방향: four dark boxes joined by (+)
xs = [X0, 110.5, 115.0, 218.5, 227.5, 331.0, 340.0, 443.5, 452.5, X1]
g = Grid("direction", xs, [3000])
put(g, X0, 110.5, 0, 1, "개선방향", LABEL, size=1090)
boxes = ["윤리경영표준모델 반영", "부패취약분야 관리", "조직문화 관행타파", "업무 투명성 확대"]
for k, text in enumerate(boxes):
    put(g, xs[2 + 2 * k], xs[3 + 2 * k], 0, 1, text, frame("#6B6B6B"), size=1090, bold=True, color=WHITE)
    if k < 3:
        put(g, xs[3 + 2 * k], xs[4 + 2 * k], 0, 1, "+", size=1200, bold=True, color="#7A7A7A", fit=False)
block(g, 366.5)

g = Grid("chevron", [X0, 110.5, 115.0, X1], [1600])
put(g, 115.0, X1, 0, 1, "▼", size=1100, color=ARROW, line=1200)
block(g, 398.5)

# 추진목표 band
g = Grid("goal", [X0, 110.5, X1], [3000])
put(g, X0, 110.5, 0, 1, "추진목표", frame("#BEBEBE"), size=1090, bold=True)
put(g, 110.5, X1, 0, 1, "기본에 충실한 윤리체계 확립으로 국민이 신뢰하는 청렴 KDN 구현", frame("#DADADA"),
    size=1150, bold=True)
block(g, 416.5)

# 추진방향 / 추진과제: three hatched direction cells over three bullet columns
C3 = [115.0, 263.0, 408.5, X1]
g = Grid("strategy", [X0, 110.5] + C3, [2970, 500, 1880, 2350])
put(g, X0, 110.5, 0, 1, "추진방향", LABEL, size=1090)
directions = ["선제적 윤리위험 관리 · 통제", "체감형 윤리적 조직문화 조성", "투명한 기관운영 및 환류 강화"]
for k, text in enumerate(directions):
    put(g, C3[k], C3[k + 1], 0, 1, text, frame("#E6E6E6", top="soft", bottom="soft", left="soft", right="soft",
                                               hatch="#D6D6D6"), size=1000, bold=True)
put(g, X0, 110.5, 2, 3, "추진과제", LABEL, size=1090)
put(g, X0, 110.5, 3, 4, [[("윤리경영", 700, False, INK)], [("표준모델 연계", 700, False, INK)]],
    frame("#CFCFCF"), line=820)
tasks = [["윤리위험 식별", "윤리경영 관리체계 강화", "핵심위험 통제활동"],
         ["임직원 윤리의식 확립", "윤리규범 정비", "윤리경영 소통 확대"],
         ["회계 신뢰성 제고 · 책임 강화", "업무 공정성 · 투명성 확보", "윤리경영 모니터링 및 점검"]]
for k, items in enumerate(tasks):
    put(g, C3[k], C3[k + 1], 2, 4, [dot(t, 990) for t in items],
        frame(bottom="soft", left="dot" if k else None), align="LEFT", line=1250)
block(g, 456.5)


def system_row(name, label, top, heads, bodies, cols=C3, sub=None):
    """Label | tabs on top | one bordered body box with dashed separators."""
    edges = cols if not sub else [cols[0], sub, *cols[1:]]
    g = Grid(name, [X0, 110.5] + edges, [1560, 2970])
    put(g, X0, 110.5, 0, 2, label, LABEL, size=1090)
    for k, head in enumerate(heads):
        put(g, cols[k], cols[k + 1], 0, 1, head, frame("#DCDCDC", top="soft", left="soft", right="soft"), size=1000)
    for k, body in enumerate(bodies):
        first, last = k == 0, k == len(bodies) - 1
        fr = frame(top="soft", bottom="soft", left="soft" if first else ("dot" if sub is None or k > 1 else None),
                   right="soft" if last else None)
        put(g, edges[k], edges[k + 1], 1, 2, body, fr, align="LEFT", line=1250, top=sub is not None)
    block(g, top)


system_row("system", "추진체계", 539.2, ["전담조직", "추진위원회", "확산조직"],
           [[dot("준법경영실", 940), dot("내부통제부", 940)],
            [dot("윤리·인권경영위원회", 940), dot("내부통제위원회", 940)],
            [dot("청렴발전소(7개 조직)", 940), dot("윤리경영담당자(122명)", 940)]])
system_row("rules", "규    범", 589.5, ["윤  리", "인  권", "감  사"],
           [[dot("내부통제 운영규정", 940, ("개선", "dark")), dot("규범준수경영지침", 940, ("신규", "box"))],
            [dot("인권경영 규정", 940, ("개정", "box")), dot("성희롱·성폭력, 스토킹 예방지침", 940, ("개정", "box"))],
            [dot("수감인 등 인권보호 지침", 940, ("신규", "box")), dot("AI 감사활용 매뉴얼", 940, ("신규", "box"))]])
C2 = [115.0, 336.2, X1]
system_row("report", "신고상담", 639.5, ["신  고", "상  담"],
           [[dot("[내부] 익명신고센터", 940), dot("[대리신고] 안심변호사", 940)],
            [dot("[외부] 레드휘슬", 940)],
            [dot("사내 AI 플랫폼, 카카오톡 오픈채팅", 940, ("신규", "box")),
             dot("인권센터, 청렴소통 핫라인        ", 940, ("신규", "box"))]], cols=C2, sub=232.0)
system_row("monitor", "모니터링", 690.0, ["대  내", "대  외"],
           [[dot("자체 청렴도(내·외부), 윤리경영수준진단", 940), dot("인권영향평가, 성희롱방지 조직문화 진단", 940)],
            [dot("국민권익위원회 종합청렴도 평가", 940),
             dot("국제표준 ISO 37301", 940, ("신규", "box")) + [(" & ISO 37001 인증", 940, False, INK)]]], cols=C2)

# ---------------------------------------------------------------------------
# 주요성과 (text layer; the two pills are images with text-layer labels)
# ---------------------------------------------------------------------------
xs = [X0, 112.5, 124.0, 196.0, X1]
g = Grid("result", xs, [530, 1450, 400, 1460, 210, 1600, 250])
put(g, X0, 112.5, 0, 7, [line1(64, 70, 765, 770)], frame("#5A5A5A"), color=WHITE)
for k, kw in enumerate(({"top": "soft", "right": "soft"}, None, {"right": "soft"}, None, {"right": "soft"},
                        None, {"bottom": "soft", "right": "soft"})):
    if kw:
        put(g, 112.5, X1, k, k + 1, [], frame(**kw))
pill = frame("#7A7A7A")
first = line1(115, 120, 748, 752)
put(g, 112.5, 124.0, 1, 2, [runs_of(first, x1=125.0)], align="RIGHT")
put(g, 124.0, 196.0, 1, 2, [runs_of(first, WHITE, x0=125.0, x1=195.0)], pill)
put(g, 196.0, X1, 1, 2, [runs_of(first, x0=195.0)], frame(right="soft"), align="LEFT")
put(g, 112.5, 124.0, 3, 4, [line1(115, 120, 766, 770)], align="RIGHT")
put(g, 124.0, 196.0, 3, 4, [runs_of(line1(130, 140, 766, 770), WHITE)], pill)
put(g, 196.0, X1, 3, 4, [line1(195, 200, 766, 770)], frame(right="soft"), align="LEFT")
put(g, 112.5, X1, 5, 6, [line1(115, 120, 783, 787)], frame(right="soft"), align="LEFT")
block(g, 743.0)

# ---------------------------------------------------------------------------
# finish (kit.finish plus top alignment and the inline tag styles)
# ---------------------------------------------------------------------------
kit.flush(802.0)
for sub in L.section.iter(L.q("hp:subList")):
    if len(sub) and any(sub[0] is first_par for first_par in TOP):
        sub.set("vertAlign", "TOP")
boxed = frame(top="soft", bottom="soft", left="soft", right="soft")
for char in L.characters:
    if char.get("textColor") == BOXED:
        char.set("textColor", INK)
        char.set("borderFillIDRef", boxed)
    elif char.get("textColor") == SHADED:
        char.set("textColor", INK)
        char.set("shadeColor", "#B4B4B4")
for number, table in enumerate(L.section.iter(L.q("hp:tbl")), 5001):
    table.set("id", str(number))
for message in WARN:
    print("WARN", message)
print(L.write(target))
