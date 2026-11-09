"""Rebuild KDN 2025 report page 140 (3rd PDF local page 40, printed page 97) as editable HWPX.

Usage: python3 work/kdn2025/p140.py <report3.pdf> <out.hwpx> [--page 40]

조직 운영 및 관리(노사관계) "Ⅲ. 세부 평가내용별 추진실적" opening page. Only the page title, the
평가내용 01 band, the section band "1 ...", the □ heading and the page number are in the PDF text
layer. The whole 노사관계 전략 diagram below the heading (y 209-801: 환경분석 ~ 대표성과) is one
image; its text was read from 4x-8x renders and typed into editable cells, band by band on the
diagram's own grid (label column | three content columns). Built with the shared kit.

Glyph and shape choices for image-only fragments: list dots -> "·", the check-circle bullets of
the roadmap -> "◎", the full-width middle dots (세대・직급 ...) -> "·", the bold up arrows -> "↑",
the dash of the footnote -> "-", the two curly braces -> a bottom rule (+ "▼"); the 신규 tags and
the 지적사항개선 badge are separate cells; the decorative tabs over the 의견수렴 heads, the chevrons
and the gray trapezoid under STEP 02 are omitted. Printed as in the source: "노사관계 노드맵"
(not 로드맵), "「광주지방 고용노동청장상」" with a space (page 141 prints it without one).
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kit  # noqa: E402
from kit import Layout, recipe_inputs  # noqa: E402

source, target = recipe_inputs(40, "노사 환경 변화를 반영한 상호협력과 참여 기반의 노사관계 전략 수립")
L = Layout(top=3100)
kit.setup(source, L)
from kit import *  # noqa: E402,F401,F403  helpers and presets bound to this page

LX = 107.5                     # label column end
C3 = ((116.0, 259.3), (264.3, 407.3), (412.5, X1))      # 환경분석 / 의견수렴 boxes
R3 = ((111.8, 258.3), (258.3, 408.8), (408.8, X1))      # roadmap / 전략방향 / 실행과제 / 성과지표
K3 = ((111.8, 256.0), (261.5, 405.8), (411.5, X1))      # 주요협력체계 boxes
BODY, SMALL = 1050, 870
LIGHT = "#F0F0F0"
RULED = frame(top="mid")


def m(text, size=BODY, bold=False, color=INK, small=SMALL):
    """Typed run list: {..} marks a smaller run (parenthetical counts)."""
    runs = []
    for part in re.split(r"(\{[^}]*\})", text):
        if part:
            if part[0] == "{":
                runs.append((part[1:-1], small, bold, color))
            else:
                runs.append((part, size, bold, color))
    return runs


def dot(text, size=BODY):
    return [("· ", size, False, "#808080")] + m(text, size)


def tight(g, x0, r0, left=0, right=0):
    """Narrow the padding of a placed cell (badges narrower than the default 320/180 padding)."""
    c0 = g.xs.index(to_x(x0))
    g.items[r0, c0] = (*g.items[r0, c0][:7], dict(left=left, right=right))


def label(g, r0, r1, lines, fill=RULED, size=1100, bold=False, color=INK):
    g.put(X0, LX, r0, r1, [[(t, size, bold, color)] for t in lines], fill, line=1300)


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
g = Grid("band", [X0, 124.0, X1], [1950, 2190])
g.put(X0, 124.0, 0, 1, "평가내용 01", frame("#565656", top="strong"), size=970, bold=True, color=WHITE, ratio=80)
g.put(X0, 124.0, 1, 2, [], frame("#E9E9E9", bottom="soft", left="soft", hatch="#DADADA"))
g.put(124.0, X1, 0, 2, lines_in(125, 130, 108, 142), frame("#E9E9E9", top="strong", bottom="soft",
                                                           right="soft", hatch="#DADADA"), align="LEFT", line=1480)
block(g, 105.5)

# Section band "1 노사 환경 변화를 ..." (number box and band are images, text from the text layer)
g = Grid("section", [X0, 84.5, X1], [2300])
g.put(X0, 84.5, 0, 1, [runs_of(line1(64, 70, 160, 165), WHITE)], frame("#606060"), line=1850)
g.put(84.5, X1, 0, 1, [line1(90, 95, 160, 166)], frame("#E4E4E4"), align="LEFT", line=1750)
block(g, 158.9)

heading("heading", line1(68, 72, 189, 192), 188.6)

# ---------------------------------------------------------------------------
# 노사관계 전략 diagram (image in the PDF; text read from 4x-8x renders)
# ---------------------------------------------------------------------------
xs = [X0, LX] + [x for c in C3 for x in c]
g = Grid("environment", xs, [2030, 3720])
label(g, 0, 2, ["환경분석"], frame("#E8E8E8"))
env = (("노동조합", ["노동조합 新 집행부 출범(7월)", "복수노조에 따른 노노갈등 존재"]),
       ("경영환경", ["AI 등 기술혁신 발전 가속화", "조직 내 세대·직급 간 갈등 상존"]),
       ("정부정책", ["노동조합법 개정(노란봉투법)", "노동자 권익 향상, 권리 보장 요구"]))
for (a, e), (head, items) in zip(C3, env):
    g.put(a, e, 0, 1, head, frame(left="mid", right="mid"), size=1150)
    g.put(a, e, 1, 2, [dot(t) for t in items], frame(LIGHT), align="LEFT", line=1400)
block(g, 210.75)

g = Grid("opinion", xs, [2230, 2290])
label(g, 0, 2, ["의견수렴"], frame("#E8E8E8"))
opinion = (("노사 간담회", "긴밀한 노사 소통 및 협력 확대"), ("노사 실무진 워크숍", "공감대 형성과 소통 확대 필요"),
           ("노사 간부급 인터뷰", "핵심 쟁점 해소에 노사 역량 집중"))
for (a, e), (head, text) in zip(C3, opinion):
    g.put(a, e, 0, 1, head, frame(top="mid", left="mid", right="mid"), size=1150)
    g.put(a, e, 1, 2, text, frame(LIGHT), size=BODY)
block(g, 273.0)

g = Grid("implication", [X0, LX, 116.0, 259.3, 408.0, X1], [3520])
label(g, 0, 1, ["시 사 점", "도      출"], frame("#C8C8C8"))
implication = (("노동조합 단일화를 위한", "노사 운명공동체적 협력 필요"),
               ("기술혁신 대응 및 세대와 직급을", "아우르는 소통·공감 문화 조성"),
               ("노동법령 준수 및 지속 가능한", "상생의 노사관계 구축"))
for k, ((a, e), pair) in enumerate(zip(((116.0, 259.3), (259.3, 408.0), (408.0, X1)), implication)):
    edges = dict(top="mid", bottom="mid", left="mid" if k == 0 else "dot", right="mid" if k == 2 else None)
    g.put(a, e, 0, 1, [m(t) for t in pair], frame(**edges), line=1400)
block(g, 323.5)

g = Grid("brace-1", [X0, LX, 116.0, X1], [520, 1110])
g.put(116.0, X1, 0, 1, [], frame(bottom="mid"))
g.put(116.0, X1, 1, 2, "▼", size=700, color=ARROW, line=800)
block(g, 358.8)

g = Grid("vision", [X0, LX, 110.5, X1], [430, 2400, 70])
label(g, 0, 3, ["노사비전"], frame("#A8A8A8"), size=1200, bold=True, color=WHITE)
g.put(LX, X1, 1, 2, "대화로 풀고 신뢰로 이어가는 「상생 노사」로 함께 체감할 수 있는 「좋은 일터」 구현",
      frame("#808080"), size=1200, bold=True, color=WHITE, line=1400)
block(g, 376.0)

# 노사관계 노드맵: STEP 01-03 (STEP 02 framed in black), titles and hatched bodies
xs = [X0, LX] + [x for c in R3 for x in c]
g = Grid("roadmap", xs, [600, 1450, 2000, 5500, 950])
label(g, 1, 4, ["노사관계", "노드맵"])
g.put(X0, LX, 0, 1, [])
g.put(X0, LX, 4, 5, [])
steps = (("01", "~ 2023년", "도약기", "#DCDCDC", INK,
          ["상생적 노사관계 가치 내재화", "노사갈등 예방 소통채널 구축", "현장 중심의 근로자 의견수렴"]),
         ("02", "2024년 ~ 2025년", "성숙기", "#C0C0C0", INK,
          ["협력적 노사관계 체계 정착", "노사 소통채널 확대·활성화", "근로조건 실질적 향상 도모"]),
         ("03", "2026년 ~ 2027년", "확산기", "#A8A8A8", WHITE,
          ["노사 공동 가치 창출 및 실현", "노사 간 상시 소통 문화 정착", "노사 일과 삶 균형 성장 실현"]))
hatched = dict(fill="#EEEEEE", hatch="#E0E0E0")
for k, ((a, e), (num, years, stage, fill, color, items)) in enumerate(zip(R3, steps)):
    framed = k == 1
    side = dict(left="strong", right="strong") if framed else {}
    g.put(a, e, 0, 1, [], frame(top="strong", **side) if framed else frame())
    g.put(a, e, 1, 2, [[("STEP ", 700, False, color), (num, 1300, True, color), ("  " + years, 1100, False, color)]],
          frame(fill, **side), align="LEFT", line=1290)
    g.put(a, e, 2, 3, stage, frame(**side), size=1200, bold=True, line=1400)
    g.put(a, e, 3, 4, [[("◎ ", 1000, True, "#505050")] + m(t) for t in items],
          frame(hatched["fill"], hatch=hatched["hatch"], bottom="strong" if framed else None, **side),
          align="LEFT", line=1650)
    g.put(a, e, 4, 5, [])
block(g, 414.5)

xs = [X0, LX, 111.8, 167.0, 198.5, 258.3, 317.5, 349.0, 408.8, 469.5, 500.5, X1]
g = Grid("strategy", xs, [1200, 2400])
label(g, 0, 2, ["전략방향"])
tabs = ((111.8, 167.0, 198.5, 258.3), (258.3, 317.5, 349.0, 408.8), (408.8, 469.5, 500.5, X1))
titles = ("협력과 참여로 함께 하는 노사", "대화와 공감으로 소통하는 노사", "노사 상생의 Win-Win 성과 창출")
for k, ((a, t0, t1, e), title) in enumerate(zip(tabs, titles)):
    sep = dict(right="dot") if k < 2 else {}
    g.put(a, t0, 0, 1, [], frame("#E8E8E8", top="mid"))
    g.put(t0, t1, 0, 1, f"{k + 1:02}", frame("#808080", top="mid"), size=1000, bold=True, color=WHITE, line=1040)
    g.put(t1, e, 0, 1, [], frame("#E8E8E8", top="mid", **sep))
    g.put(a, e, 1, 2, title, frame("#E8E8E8", **sep), size=1150, line=1350)
block(g, 519.5)

xs = [X0, LX] + [x for c in R3 for x in c]
g = Grid("actions", xs, [4100])
label(g, 0, 1, ["실행과제"])
actions = (("협력적 노사관계 정착 추진", "쟁점현안 선제적 관리·대응"),
           ("노사 소통채널 참여 활성화", "노사관계 전문성 역량 강화"),
           ("무분규 임금협약 체결", "근로조건 실질적 향상"))
for k, ((a, e), pair) in enumerate(zip(R3, actions)):
    edges = dict(top="mid", bottom="mid", left="mid" if k == 0 else "dot", right="mid" if k == 2 else None)
    g.put(a, e, 0, 1, [dot(t) for t in pair], frame(**edges), align="LEFT", line=1450)
block(g, 556.2)

# 주요협력체계: three boxes, 신규 tags in their own cells
tags = {(0, 2): (216.7, 232.2), (0, 3): (190.3, 205.8), (1, 2): (321.5, 337.0), (1, 3): (352.3, 367.8),
        (2, 2): (510.3, 525.8)}
xs = sorted({X0, LX} | {x for c in K3 for x in c} | {x for t in tags.values() for x in t})
g = Grid("cooperation", xs, [1625, 1950, 1450, 1650])
label(g, 0, 4, ["주요협력", "체계"])
coop = (("노사 공통 현안 해결", ["임금교섭 대표·실무협의회", "노동조합법 개정 대응TF", "인사제도 개선TF"]),
        ("노사 소통·역량 관리", ["노사 합동 학습동아리", "청년위원회", "한마음 비빔밥 Day"]),
        ("노사 복지·안전 개선", ["직무중심 보수 고도화 협의회", "복지 앰배서더 워크숍", "노사합동 안전점검"]))
NEW = frame(WHITE, top="soft", bottom="soft", left="soft", right="soft")
for k, ((a, e), (head, items)) in enumerate(zip(K3, coop)):
    g.put(a, e, 0, 1, head, frame("#C8C8C8", top="soft", left="soft", right="soft"), size=1150, bold=True)
    for r, text in zip((1, 2, 3), items):
        edges = dict(left="soft", right="soft", bottom="soft" if r == 3 else None)
        tag = tags.get((k, r))
        if tag:
            g.put(a, tag[0], r, r + 1, [dot(text)], frame(left="soft", bottom=edges["bottom"]), align="LEFT",
                  line=1250)
            g.put(tag[0], tag[1], r, r + 1, "신규", NEW, size=780, line=950, ratio=85, fit=False)
            tight(g, tag[0], r)
            g.put(tag[1], e, r, r + 1, [], frame(right="soft", bottom=edges["bottom"]))
        else:
            g.put(a, e, r, r + 1, [dot(text)], frame(**edges), align="LEFT", line=1250)
block(g, 602.3)

# 성과지표 모니터링 (light band, dotted separators) with the 지적사항개선 badge
xs = [X0, LX, 111.8, 124.5, 167.0, 258.3, 408.8, X1]
g = Grid("kpi", xs, [1830, 1870])
label(g, 0, 2, ["성과지표", "모니터링"])
g.put(111.8, 258.3, 0, 1, [dot("노사협력지수*{(89.8점/4.2점↑)}")], frame(LIGHT, right="dot"), align="LEFT")
g.put(111.8, 124.5, 1, 2, [], frame(LIGHT))
g.put(124.5, 167.0, 1, 2, "지적사항개선", frame("#4A4A4A"), size=820, bold=True, color=WHITE, line=1000)
g.put(167.0, 258.3, 1, 2, [], frame(LIGHT, right="dot"))
g.put(258.3, 408.8, 0, 2, [dot("소통활성화지수{(90.5점/0.2점↑)}"), dot("교육수료인원수{(474명/58명↑)}")],
      frame(LIGHT, right="dot"), align="LEFT", line=1500)
g.put(408.8, X1, 0, 2, [dot("무분규 임금협약 체결{(24년 연속)}"), dot("종합복지만족도{(91.3점/1.1점↑)}")],
      frame(LIGHT), align="LEFT", line=1500)
block(g, 674.5)

g = Grid("footnote", [X0, LX, 111.8, 116.0, X1], [1260, 1260, 480, 750])
g.put(116.0, X1, 0, 1, [m("* 한국노동연구원 ‘사업체패널조사’ 항목을 반영해 노사협력지수 분야 설문 개선", 1000)],
      align="LEFT", line=1100)
g.put(116.0, X1, 1, 2, [m("  - 노사관계 전반에 대한 측정 문항 개선{(4개 → 6개)}을 통해 설문 신뢰성·타당성 강화", 1000,
                          small=780)], align="LEFT", line=1100)
g.put(111.8, X1, 2, 3, [], frame(bottom="mid"))
g.put(111.8, X1, 3, 4, "▼", size=600, color=ARROW, line=580, fit=False)
block(g, 711.5)

# 대표성과: dark label, light body split by dashed rules (two lines each: note + award)
cols = ((109.0, 264.5), (264.5, 411.8), (411.8, X1))
g = Grid("result", [X0, 109.0] + [c[1] for c in cols], [4850])
g.put(X0, 109.0, 0, 1, "대표성과", frame("#4A4A4A", top="mid", bottom="mid", left="mid"), size=1250, bold=True,
      color=WHITE)
awards = (("협력적 노사 문화 조성 공로", "「광주지방 고용노동청장상」 수상"),
          ("에너지ICT와 연계한 ESG 고도화", "공공기관 부문 「ESG 대상」 수상"),
          ("고용 확대 및 복리후생 강화 공로", "「고용노동부장관상」 수상"))
for k, ((a, e), (note, award)) in enumerate(zip(cols, awards)):
    edges = dict(top="mid", bottom="mid", right="mid" if k == 2 else "dot")
    g.put(a, e, 0, 1, [m(note, 1050), m(award, 1250)], frame(LIGHT, **edges), line=1550)
block(g, 752.0)

kit.finish(target, end=802.0)
