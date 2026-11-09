"""Rebuild KDN 2025 report page 144 (3rd PDF local page 44, printed page 101) as editable HWPX.

Usage: python3 work/kdn2025/p144.py <report3.pdf> <out.hwpx> [--page 44]

조직 운영 및 관리(노사관계), section 2 "노사관계 관리 역량 강화를 위한 교육체계 구축 및 맞춤형 교육
운영". Built with the shared kit (one flat table per horizontal band on a grid of PDF x edges).

Text-layer parts (section title, 가./나. headings, 공통 / 계층별 교육 bands and boxes, 계층별 교육 대상
table, 추진성과, 주요성과, page number) are taken from the PDF lines with their spans. The tags at
the end of lines (신규 / 개선) are separate cells.

Image parts, typed from 5x-10x renders:
- PART 01 box, section number band, the 지적사항 개선 sticker (hand icon dropped), the KDN logo.
- the whole 가. diagram (y 123-406: 환경분석, 교육목표, 추진방향, 운영체계 PDCA and the 역량진단
  note). Shapes become fills and borders: the dark tabs over the 환경분석 heads -> strong top
  border, the corner brackets of 교육목표 -> side borders on a hatched band, the P / D / A / C
  chevrons -> gray tag cells, the PDCA cycle arrows -> ▲ (A to P) and ▼ (D to C) cells, the arrow
  inside the 역량진단 note -> ▶, list dots -> "·". Outlined tags (방법, 구성, 기존 ...) are cells.
- quote marks are kept as printed: ’24년도 / ’24년 (curly), '26년 신규 (straight, bold title),
  ‘26년 교육 계획 반영 (opening quote).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kit  # noqa: E402
from kit import Layout, recipe_inputs  # noqa: E402

source, target = recipe_inputs(44, "노사관계 관리 역량 강화를 위한 교육체계 구축")
L = Layout(top=3100)
kit.setup(source, L)
from kit import *  # noqa: E402,F401,F403  helpers and presets bound to this page

DARK, LABEL, BAND = "#6A6A6A", "#E3E3E3", "#E8E8E8"
BODY, SMALL = 1090, 890
LAB, IN = 110.5, 116.0          # diagram label column end, content start
BOXED = frame(WHITE, top="mid", bottom="mid", left="mid", right="mid")
NEW = frame(WHITE, top="mid", bottom="mid", left="mid", right="mid")
IMPROVED = frame("#6E6E6E")


def S(text, size=BODY, bold=False, color=INK):
    return (text, size, bold, color)


def dot(*parts, size=BODY):
    """'· text' paragraph; parts are str (body size) or (text, size) for smaller runs."""
    runs = [S("· ", size, False, "#8A8A8A")]
    for part in parts:
        runs.append(S(part, size) if isinstance(part, str) else S(*part))
    return runs


def tight(g, x0, r0, left=40, right=40):
    """Narrow the cell padding (kit cells use the builder default 320/180)."""
    c0 = g.xs.index(to_x(x0))
    item = g.items[r0, c0]
    g.items[r0, c0] = (*item[:7], dict(left=left, right=right))


def split(line, x):
    """Text runs before the tag that starts at PDF x, and the tag's own runs."""
    return runs_of(line, x1=x), strip_runs(runs_of(line, x0=x))


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

# Section 2 band (image): dark number box, light title band (text layer).
g = Grid("sec2", [X0, 84.5, X1], [2300])
g.put(X0, 84.5, 0, 1, [runs_of(line1(60, 70, 70, 76), WHITE)], frame(DARK), line=1700)
g.put(84.5, X1, 0, 1, [line1(90, 95, 72, 78)], frame("#E6E6E6"), align="LEFT", line=1700)
block(g, 70.9)

g = Grid("title-ga", [X0, X1], [1650])
g.put(X0, X1, 0, 1, [line1(55, 60, 100, 105)], align="LEFT", line=1450)
block(g, 101.3)

# ---------------------------------------------------------------------------
# 가. diagram (image in the PDF; text typed from 5x renders)
# ---------------------------------------------------------------------------
def label(g, r0, r1, text):
    g.put(X0, LAB, r0, r1, text, frame(LABEL), size=1100, line=1300)


# 환경분석: three outlined heads (dark tab on top) over gray bodies.
E = ((IN, 259.2), (264.4, 407.4), (412.7, X1))
g = Grid("env", [X0, LAB] + [x for e in E for x in e], [1800, 3550])
label(g, 0, 2, "환경분석")
env = (("’24년도 환류", [dot("노사 차별화된 맞춤 교육 요구"), dot("노동이사 전문 교육 확대 필요")]),
       ("대외 환경", [dot("노동조합법 개정", ("(노란봉투법)", SMALL)), dot("노사관계 관리 역량 강화 요구")]),
       ("대내 환경", [dot("새정부 기조의 노무교육 운영"), dot("직무역량 향상 교육 강화 요구")]))
for (a, e), (head, items) in zip(E, env):
    g.put(a, e, 0, 1, head, frame(WHITE, top="strong", left="mid", right="mid"), size=1200, line=1350)
    g.put(a, e, 1, 2, items, frame("#EBEBEB"), align="LEFT", line=1400)
block(g, 123.5)

# 교육목표: hatched band with corner rules, bold goal.
g = Grid("goal", [X0, LAB, IN, X1], [2490])
label(g, 0, 1, "교육목표")
g.put(IN, X1, 0, 1, "노사관계 관리 역량 향상과 노사 공동의 목표 달성을 위한 교육체계 활성화",
      frame("#EEEEEE", top="soft", bottom="soft", left="strong", right="strong", hatch="#DCDCDC"),
      size=1200, bold=True, line=1400)
block(g, 181.0)

# 추진방향: two numbered heads, two bullets each, dotted separator; 국정94 tag.
xs = [X0, LAB, IN, 136.5, 293.0, 316.0, 329.5, 335.5, 341.0, 360.5, X1]
g = Grid("direction", xs, [1900, 350, 1430, 1430, 130])
label(g, 0, 5, "추진방향")
num = frame("#A2A2A2")
head = frame("#EFEFEF", bottom="mid")
g.put(IN, 136.5, 0, 1, "1", num, size=1400, color=WHITE, line=1500, fit=False)
g.put(136.5, 329.5, 0, 1, "공통 역량 강화 교육", head, size=1150, bold=True, align="LEFT", line=1350)
g.put(341.0, 360.5, 0, 1, "2", num, size=1400, color=WHITE, line=1500, fit=False)
g.put(360.5, X1, 0, 1, "노 – 사 계층별 차별화 교육", head, size=1150, bold=True, align="LEFT", line=1350)
g.put(329.5, 335.5, 0, 5, [], frame(right="dot"))
g.put(IN, 329.5, 2, 3, [dot("노동조합법 개정", ("(노란봉투법)", SMALL), " 관련 이슈 반영")], align="LEFT", line=1350)
g.put(IN, 293.0, 3, 4, [dot("새정부 노사관계 강화 정책 기조 반영")], align="LEFT", line=1350)
g.put(293.0, 316.0, 3, 4, "국정94", frame("#D2D2D2"), size=760, line=900, fit=False)
tight(g, 293.0, 3)
g.put(341.0, X1, 2, 3, [dot("교육 대상, 직급, 직책에 따른 맞춤형 교육 제공")], align="LEFT", line=1350)
g.put(341.0, X1, 3, 4, [dot("선우재, 경북대 등 노사관계 전문 위탁기관 확대")], align="LEFT", line=1350)
g.put(IN, 329.5, 4, 5, [], frame(bottom="mid"))
g.put(341.0, X1, 4, 5, [], frame(bottom="mid"))
block(g, 210.6)

# 운영체계: P / D / A / C stages (tag + band, tagged lines), cycle arrows, 역량진단 note.
xs = [X0, LAB, IN, 141.0, 144.0, 165.5, 184.0, 209.0, 334.0, 336.0, 362.0, 387.0, 523.0, 543.0, X1]
hs = [1450, 650, 1250, 1250, 750,      # P / D band, pad, two lines, pad      266.6 .. 320.1
      1450, 600, 1250, 1250, 200,      # A / C band, pad, two lines, pad      320.1 .. 367.6
      600, 1300, 1300, 750]            # 역량진단 note (dotted box)            367.6 .. 407.1
g = Grid("pdca", xs, hs)
label(g, 0, 14, "운영체계")
band = frame(BAND)
stages = ((0, IN, 141.0, "P", "#A8A8A8", 141.0, 334.0, "노사관계 교육 계획 수립"),
          (0, 336.0, 362.0, "D", "#8A8A8A", 362.0, X1, "노-사 맞춤형 교육 실행"),
          (5, IN, 141.0, "A", "#555555", 141.0, 334.0, "'26년 신규 교육과정 계획 수립"),
          (5, 334.0, 362.0, "C", "#727272", 362.0, X1, "교육 실적 점검 및 평가"))
for r, ta, te, tag, fill, ba, be, title in stages:
    g.put(ta, te, r, r + 1, tag, frame(fill), size=1150, color=WHITE, line=1300)
    g.put(ba, be, r, r + 1, title, band, size=BODY, bold=True, align="LEFT", line=1300)
lines = ((2, 141.0, "방법", "’24년 교육 피드백, 대내외 환경 요소 접목"),
         (3, 141.0, "구성", "노-사, 직급에 따른 맞춤 교육 및 공통 교육"),
         (2, 362.0, "회사", "리더십, 분쟁해결방안 등 관리자 역량"),
         (3, 362.0, "노조", "부당노동행위, 노동조합법 등 법 쟁점"),
         (7, 141.0, "방법", "교육 만족도, 역량진단*으로 개선점 도출"),
         (8, 141.0, "개선", "‘26년 교육 계획 반영, 신규 프로그램 개발"),
         (7, 362.0, "양적", "직전년도 대비 신규교육 실적 및 결과"),
         (8, 362.0, "질적", "교육 컨텐츠, 대상, 수준 등 교육 내용"))
for r, a, tag, text in lines:
    t = 165.5 if a < 300 else 387.0
    e = 334.0 if a < 300 else 543.0
    g.put(a, t, r, r + 1, tag, BOXED, size=1030, line=1150, fit=False)
    tight(g, a, r)
    g.put(t, e, r, r + 1, text, size=BODY, align="LEFT", line=1250)
g.put(IN, 141.0, 1, 5, "▲", size=900, color=ARROW, line=1000)        # A -> P
g.put(543.0, X1, 1, 5, "▼", size=900, color=ARROW, line=1000)        # D -> C
# 역량진단 note: dotted box, 기존 (outlined) ▶ 개선 (dark) tags.
note = dict(left="dot", right="dot")
g.put(141.0, 523.0, 10, 11, [], frame(top="dot", **note))
g.put(141.0, 144.0, 11, 13, [], frame(left="dot"))
g.put(144.0, 184.0, 11, 12, "*역량진단", size=BODY, align="LEFT", line=1250)
tight(g, 144.0, 11, 0, 0)
g.put(184.0, 209.0, 11, 12, "기존", BOXED, size=1030, line=1150, fit=False)
tight(g, 184.0, 11)
g.put(209.0, 334.0, 11, 13, [[S("(2개 분야 10항목) 노사관계 역량")], [S("사전·사후진단")]], align="LEFT", line=1300)
g.put(334.0, 362.0, 11, 13, "▶", size=1200, color=ARROW, line=1300, fit=False)
g.put(362.0, 387.0, 11, 12, "개선", IMPROVED, size=1030, color=WHITE, line=1150, fit=False)
tight(g, 362.0, 11)
g.put(387.0, 523.0, 11, 13, [[S("(8개 분야 34항목) 법·제도 실무, 협상·")], [S("의사소통, 갈등관리·문제해결 등 추가")]],
      frame(right="dot"), align="LEFT", line=1300)
g.put(141.0, 523.0, 13, 14, [], frame(bottom="dot", **note))
block(g, 266.6)

# ---------------------------------------------------------------------------
# 나. heading with the 지적사항 개선 sticker (image, typed)
# ---------------------------------------------------------------------------
g = Grid("title-na", [X0, 477.5, 531.5, X1], [1650])
g.put(X0, 477.5, 0, 1, [line1(55, 60, 416, 421)], align="LEFT", line=1450)
g.put(477.5, 531.5, 0, 1, "지적사항 개선", frame("#3C3C3C"), size=820, bold=True, color=WHITE, line=1000)
block(g, 417.5)


def course_band(name, tag_line, title_line, tag_x, top):
    """'공통 교육' / '계층별 교육' band: outlined tag on a darker strip, bold title on a gray band."""
    a, e = tag_x
    g = Grid(name, [X0, a, e, 110.0, X1], [1880])
    g.put(X0, a, 0, 1, [], frame("#C9C9C9"))
    g.put(a, e, 0, 1, [runs_of(tag_line)], BOXED, line=1000)
    tight(g, a, 0, 0, 0)
    g.put(e, 110.0, 0, 1, [], frame("#C9C9C9"))
    g.put(110.0, X1, 0, 1, [title_line], frame("#E3E3E3"), align="LEFT", line=1300)
    block(g, top)


course_band("common", line1(60, 70, 444, 448), line1(115, 120, 441, 446), (64.0, 100.5), 439.2)

# 공통 교육 box: 진단결과 (head + gray bullets) ▶ three programmes with 신규 / 개선 tags.
xs = [X0, 60.0, 202.0, 215.8, 524.0, 545.0, X1]
g = Grid("common-box", xs, [300, 1560, 1560, 1560, 520])
outline = dict(left="soft", right="soft")
g.put(X0, X1, 0, 1, [], frame(top="soft", **outline))
g.put(X0, 60.0, 1, 4, [], frame(left="soft"))
g.put(60.0, 202.0, 1, 2, [line1(70, 80, 463, 467)], line=1350)
g.put(60.0, 202.0, 2, 4, lines_in(60, 70, 483, 501), frame("#EBEBEB"), align="LEFT", line=1450)
g.put(202.0, 215.8, 1, 4, "▶", size=1200, color="#B0B0B0", line=1300, fit=False)
for r, y in ((1, 466.0), (2, 481.8), (3, 497.5)):
    line = line1(220, 225, y - 1, y + 1)
    text, tag = split(line, 527.0)
    g.put(215.8, 524.0, r, r + 1, [text], align="LEFT", line=1300)
    g.put(524.0, 545.0, r, r + 1, [tag], NEW if tag[0][0] == "신규" else IMPROVED, line=1000, fit=False,
          color=INK)
    tight(g, 524.0, r, 0, 0)
    if tag[0][0] == "개선":
        cell0 = g.items[r, g.xs.index(to_x(524.0))]
        cell0[3][0][0].set("charPrIDRef", L.char(tag[0][1], True, WHITE, 90))
    g.put(545.0, X1, r, r + 1, [], frame(right="soft"))
g.put(X0, X1, 4, 5, [], frame(bottom="soft", **outline))
block(g, 460.5)

course_band("layered", line1(60, 70, 527, 531), line1(115, 120, 524, 529), (61.0, 103.5), 521.9)

# 계층별 교육 대상 table: 회사 | 대상 (tab head + hatched groups) | 노동조합, lines with 신규 tags.
C1, C2, C3 = (63.5, 241.3), (245.0, 367.1), (371.0, 548.8)
SUB = 306.2
xs = [X0, C1[0], 205.0, 226.0, C1[1], C2[0], SUB, C2[1], C3[0], 530.0, C3[1], X1]
groups = ((565.8, [1620, 1540, 1540, 580]), (618.6, [1600, 1550, 1560, 600]),
          (671.7, [1660, 1540, 1880, 0]))
hs = [420, 1450, 390] + [h for _, row in groups for h in row if h] + [580]
g = Grid("layers", xs, hs)
last = len(hs) - 1
g.put(X0, X1, 0, 1, [], frame(top="soft", left="soft", right="soft"))
g.put(X0, C1[0], 1, last, [], frame(left="soft"))
g.put(C3[1], X1, 1, last, [], frame(right="soft"))
head = frame("#E3E3E3")
for (a, e), x in ((C1, 140), (C2, 270), (C3, 440)):
    g.put(a, e, 1, 2, [line1(x, x + 5, 548, 552)], head, bold=True, line=1300)
g.put(X0, X1, last, last + 1, [], frame(bottom="soft", left="soft", right="soft"))
hatch = frame("#EEEEEE", hatch="#DCDCDC")
tab = frame(top="strong")
r0 = 3
for k, (top, row) in enumerate(groups):
    n = 3
    for i in range(n):
        r = r0 + i
        sep = dict(bottom="dot") if (i == n - 1 and k < 2) else {}
        for (a, e), x in ((C1, 66.6), (C3, 374.04)):
            line = lines_in(x - 1, x + 1, top + 2 + 15.4 * i, top + 15.4 * (i + 1) + 2)
            assert len(line) == 1, (k, i, [l["text"] for l in line])
            line = line[0]
            tags = [s for s in line["spans"] if s["text"] in ("신규", "개선")]
            if tags:
                tx = tags[0]["bbox"][0] - 0.5
                text, tag = split(line, tx)
                end = 205.0 if a < 100 else 530.0
                g.put(a, end, r, r + 1, [text], frame(**sep), align="LEFT", line=1300)
                g.put(end, end + (21.0 if a < 100 else 18.8), r, r + 1, [tag], NEW, line=1000, fit=False)
                tight(g, end, r, 0, 0)
                if a < 100:
                    g.put(226.0, e, r, r + 1, [], frame(**sep))
            else:
                g.put(a, e, r, r + 1, [line], frame(**sep), align="LEFT", line=1300)
        if sep:
            g.put(C1[1], C2[0], r, r + 1, [])
            g.put(C2[1], C3[0], r, r + 1, [])
    # middle column: tab-topped head, hatched sub cells
    hy = (571, 624, 676)[k]
    g.put(C2[0], C2[1], r0, r0 + 1, [line1(C2[0], C2[1], hy, hy + 2)], tab, bold=True, line=1200)
    if k < 2:
        sy = (589, 642)[k]
        left = lines_in(C2[0], SUB - 3, sy, sy + 22)
        right = lines_in(SUB - 2, C2[1], sy, sy + 22)
        g.put(C2[0], SUB, r0 + 1, r0 + 3, left, hatch, line=1150)
        g.put(SUB, C2[1], r0 + 1, r0 + 3, right, hatch, line=1150)
        r0 += 4
    else:
        g.put(C2[0], C2[1], r0 + 1, r0 + 2, [line1(270, 275, 693, 695)], hatch, line=1150)
        g.put(C2[0], C2[1], r0 + 2, r0 + 3, [line1(245, 250, 709, 711)], line=1250)
        r0 += 3
block(g, 543.2)

# 추진성과 band and 주요성과 box (text layer).
g = Grid("progress", [X0, 114.0, 116.2, X1], [2580])
g.put(X0, 114.0, 0, 1, [line1(60, 70, 743, 745)], frame("#D6D6D6", top="mid"), line=1300)
g.put(116.2, X1, 0, 1, [line1(175, 185, 740, 742)], frame("#EFEFEF", top="soft", bottom="soft", left="soft",
                                                         right="soft"), line=1350)
block(g, 734.9)

g = Grid("result", [X0, 111.7, X1], [3720])
g.put(X0, 111.7, 0, 1, [runs_of(line1(60, 70, 776, 780), WHITE)], frame(DARK, top="mid", bottom="mid", left="mid"))
g.put(111.7, X1, 0, 1, lines_in(115, 120, 768, 790), frame(top="mid", bottom="mid", right="mid"), align="LEFT",
      line=1450)
block(g, 765.3)

kit.finish(target, end=802.5)
