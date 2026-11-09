"""Rebuild KDN 2025 report page 124 (3rd PDF local page 24, printed page 84) as editable HWPX.

Usage: python3 work/kdn2025/p124.py <report3.pdf> <out.hwpx> [--page 24]

조직 운영 및 관리 "Ⅲ. 세부 평가내용별 추진실적" opening page. Only the title, the 평가내용 title,
the section band "1 ...", the 데브옵스 footnote and the page number are in the PDF text layer; they
are taken from it. Everything from y 187 to 787 (2035 NEW 비전 / 전략방향 / 주요경영목표, 조직진단,
진단결과 및 시사점, 중장기 조직·인력 운영방향, H.O.T. 중점과제, 장애요인 및 극복방안, 관리체계 및
성과창출) is one image; its text was read from 4-7x renders and typed into editable cells on the
diagram's own grid (label column | content). Built with the shared kit.

Glyph and shape choices for image-only fragments: list dots -> "·", the check-in-circle bullets
-> ◎, the ➜ arrow -> →, the grey chevrons -> ▶, the brace under 조직진단 -> ▼, the bracket line
from 시사점 to [단기] -> cell borders; the strategy icons are dropped. The three donut charts keep
only their printed values (head count and share per series, on the row of the matching
portfolio, with the legend squares in the series' shade). Superscript years (’24년 ...) and
Dev+Ops are small runs on the baseline.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kit  # noqa: E402
from kit import Layout, recipe_inputs  # noqa: E402

source, target = recipe_inputs(24, "정부정책 이행과 새로운 경영전략 연계를 위한 조직")
L = Layout(top=3100)
kit.setup(source, L)
from kit import *  # noqa: E402,F401,F403  helpers and presets bound to this page

LABEL, LIGHT, DARK, MID = "#E5E5E5", "#E5E5E5", "#666666", "#B2B2B2"
LX, CX0 = 110.2, 115.2          # label column end, content start
BOX = dict(top="mid", bottom="mid", left="mid", right="mid")
HATCH = frame("#F4F4F4", top="soft", hatch="#DCDCDC")
SERIES = {"미래성장": "#7F7F7F", "전력계통": "#B2B2B2", "ICT운영": "#D9D9D9"}


def m(text, size=1050, bold=False, color=INK, small=0.82, sup=0.55, light=False):
    """Typed run list: {..} = smaller run, ^..^ = superscript-size run, *..* = bold run;
    light=True sets the smaller and superscript runs regular (as in the 주요성과 lines)."""
    runs = []
    for part in re.split(r"(\{[^}]*\}|\^[^^]*\^|\*[^*]*\*)", text):
        if not part:
            continue
        if part[0] == "{":
            runs.append((part[1:-1], int(round(size * small / 10)) * 10, bold and not light, color))
        elif part[0] == "^":
            runs.append((part[1:-1], int(round(size * sup / 10)) * 10, bold and not light, color))
        elif part[0] == "*":
            runs.append((part[1:-1], size, True, color))
        else:
            runs.append((part, size, bold, color))
    return runs


def label(g, r0, r1, lines, fill=LABEL, color=INK):
    g.put(X0, LX, r0, r1, [m(t, 1100, False, color) for t in lines], frame(fill), line=1300)


def tight(g, x0, r0, **margin):
    key = (r0, g.xs.index(to_x(x0)))
    g.items[key] = (*g.items[key][:7], margin)


def quiet(g, *args, **kw):
    """put() for cells whose padding is narrowed afterwards (the kit's size check assumes 160)."""
    n = len(WARN)
    g.put(*args, **kw)
    del WARN[n:]


def pad(g, x0, x1, r, fill="1"):
    quiet(g, x0, x1, r, r + 1, "", fill, size=100, line=100, fit=False)
    tight(g, x0, r, top=0, bottom=0)


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
g.put(X0, X1, 0, 1, [line1(195, 205, 69, 74)])
block(g, 68.5)

# 평가내용 01 band (chip image typed, title from the text layer)
g = Grid("band", [X0, 124.0, X1], [1950, 2190])
g.put(X0, 124.0, 0, 1, "평가내용 01", frame("#5F5F5F", top="strong"), size=970, bold=True, color=WHITE, ratio=80)
g.put(X0, 124.0, 1, 2, [], frame("#EEEEEE", bottom="soft", left="soft", hatch="#DADADA"))
g.put(124.0, X1, 0, 2, lines_in(125, 130, 110, 142), frame("#EEEEEE", top="strong", bottom="soft",
                                                           right="soft", hatch="#DADADA"), align="LEFT", line=1510)
block(g, 105.5)

# Section band "1 정부정책 이행과 ..." (number box and band are images, text from the text layer)
g = Grid("section", [X0, 85.5, X1], [2290])
g.put(X0, 85.5, 0, 1, [runs_of(line1(64, 70, 160, 164), WHITE)], frame("#797979"), line=1850)
g.put(85.5, X1, 0, 1, [line1(90, 95, 161, 165)], frame("#EBEBEB"), align="LEFT", line=1750)
block(g, 158.9)

# ---------------------------------------------------------------------------
# 2035 NEW 비전 / 전략방향 & 전략이슈 / 2035 주요경영목표 / 조직진단 (image text)
# ---------------------------------------------------------------------------
boxes = ((CX0, 220.3), (227.4, 332.0), (339.0, 443.6), (450.6, X1))
seps = (CX0, 223.6, 335.2, 447.1, X1)
xs = sorted({X0, LX, CX0, X1} | {x for b in boxes for x in b} | set(seps))
g = Grid("strategy", xs, [250, 2400, 500, 2350, 3370, 460, 1630, 630, 1520, 1140])
g.put(X0, LX, 0, 3, [m("2035", 1150, True, WHITE), m("NEW 비전", 1150, True, WHITE)], frame("#8C8C8C"),
      line=1250)
pad(g, LX, X1, 0)
g.put(LX, CX0, 1, 2, [])
g.put(CX0, X1, 1, 2, [m("디지털 혁신, 에너지 대전환을 선도하는 글로벌 에너지 ICT의 중심", 1200, True, WHITE)],
      frame(DARK))
pad(g, LX, X1, 2)
label(g, 3, 5, ["전략방향", "&", "전략이슈"])
STRAT = (("디지털 융합", "AI 기반의 독자 솔루션으로", "에너지산업 DX주도"),
         ("사업 다각화", "미래신사업 경쟁력 확보로", "글로벌 에너지ICT 신시장 창출"),
         ("ESG 선도", "디지털 기반 ESG 가치 창출로", "에너지ICT 생태계 주도"),
         ("시스템 경영", "혁신주도형 시스템 경영으로", "지속가능성과 확대"))
for (a, e), (head, l1, l2) in zip(boxes, STRAT):
    g.put(a, e, 3, 4, head, frame(top="mid", left="mid", right="mid"), size=1250, bold=True, align="LEFT")
    g.put(a, e, 4, 5, [m(l1, 970), m(l2, 970)], frame(LIGHT), line=1350)
pad(g, LX, X1, 5)
label(g, 6, 9, ["2035", "주요경영목표"])
for k, (goal, a, e) in enumerate(zip(("“매출 2조원”", "“미래신사업 매출 6천억원”", "“중대재해 Zero”",
                                      "“핵심전문가 740명”"), seps, seps[1:])):
    g.put(a, e, 6, 7, goal, frame(right="dot") if k < 3 else "1", size=1150, bold=True)
pad(g, CX0, X1, 7)
g.put(CX0, X1, 8, 9, [m("2035 NEW비전 달성을 위한 조직진단(4개월) : 내부 TF 55명(조직별 Key-Man) + 외부 전문가 6명",
                        1150, True)], frame(LIGHT))
g.put(X0, LX, 9, 10, [])
g.put(CX0, X1, 9, 10, "▼", frame(top="mid"), size=900, color="#9A9A9A", line=900, fit=False)
block(g, 188.5)

# ---------------------------------------------------------------------------
# 진단결과 및 시사점 -> 중장기 조직 운영방향
# ---------------------------------------------------------------------------
cols = ((CX0, 254.3), (265.9, 404.5), (416.4, X1))
LINK = (188.3, 484.4)
xs = sorted({X0, LX, CX0, X1, *LINK} | {x for c in cols for x in c})
g = Grid("diagnosis", xs, [1840, 3250, 790, 790, 1940, 3140])
label(g, 0, 2, ["진단결과", "및", "시사점"])
DIAG = (("외부환경", LIGHT, INK, ("· AI, 에너지 정책의 ICT 역할 확대", "· 민간 대기업의 공격적 AI 투자")),
        ("내부환경", LIGHT, INK, ("· 조직 간 협업체계 미흡", "· 직무 및 기능 중복성 산재")),
        ("시사점", DARK, WHITE, ("· 협업과 시너지 중심 조직 재설계", "· 적소적재 인력 활용 및 전문가 육성")))
for (a, e), (head, fill, color, lines) in zip(cols, DIAG):
    g.put(a, e, 0, 1, head, frame(fill, top="mid", left="mid", right="mid"), size=1150, bold=True, color=color)
    g.put(a, e, 1, 2, [m(t) for t in lines], frame(**BOX), align="LEFT", line=1350)
# bracket line from 시사점 down to [단기]
g.put(LINK[0], LINK[1], 2, 3, [], frame(bottom="strong", right="strong"))
g.put(LINK[0], LINK[1], 3, 4, [], frame(left="strong"))
label(g, 4, 6, ["중장기", "조직", "운영방향"])
PERIODS = (("[단기] (~’25년)", DARK, WHITE, ("협업·전문성 중심 조직·인력체계 구축", "기능과 역할{(R&R)} 명확화 및 고도화")),
           ("[중기] (~’30년)", MID, INK, ("미래 신사업 분야별 실행조직 재배치", "포트폴리오별 직무 재정비 및 조직 연계")),
           ("[장기] (~’35년)", "#D9D9D9", INK, ("플랫폼 서비스형 조직구조 정착", "글로벌 시장 별 주도 조직 상시화")))
for k, ((a, e), (head, fill, color, lines)) in enumerate(zip(cols, PERIODS)):
    g.put(a, e, 4, 5, head, frame(fill), size=1200, bold=True, color=color)
    g.put(a, e, 5, 6, [[("◎ ", 800, True, "#555555")] + m(t, 1000) for t in lines], HATCH, align="LEFT", line=1350)
block(g, 332.6)

# ---------------------------------------------------------------------------
# 중장기 인력 운영방향: 3대 포트폴리오 rows | donut values per period
# ---------------------------------------------------------------------------
TAG, TXT = (CX0, 177.7), (181.2, 277.8)
CH = (281.5, 374.4, 464.8, X1)
xs = sorted({X0, LX, CX0, X1, *TAG, *TXT, *CH})
g = Grid("workforce", xs, [1710, 650, 1450, 670, 650, 1450, 670, 650, 1250, 900])
label(g, 0, 10, ["중장기", "인력", "운영방향"])
g.put(CX0, CH[0], 0, 1, "3대 포트폴리오별 중장기 방향성", frame(MID), size=1150, bold=True, align="LEFT")
for k, (a, e) in enumerate(zip(CH, CH[1:])):
    period = ("단기(~’25년)", "중기(~’30년)", "장기(~’35년)")[k]
    g.put(a, e, 0, 1, period, frame("#E6E6E6"), size=1150)
PORT = (("미래성장사업", "#7F7F7F", WHITE, ("사업다각화 관점 중장기", "인력 확대"), "미래성장",
         ("192명 (7.6%)", "609명 (19.4%)", "830명 (24.0%)")),
        ("ICT운영사업", "#D9D9D9", INK, ("AX·DX기반 인력", "생산성 제고"), "ICT운영",
         ("1,106명 (43.6%)", "1,196명 (38.1%)", "1,226명 (35.4%)")),
        ("전력계통사업", "#B2B2B2", INK, ("전력계통 솔루션 중심", "운영 최적화"), "전력계통",
         ("1,236명 (48.8%)", "1,333명 (42.5%)", "1,403명 (40.6%)")))
for i, (tag, fill, color, lines, series, values) in enumerate(PORT):
    r = 1 + 3 * i
    span = 3 if i < 2 else 2                 # the last row leaves its bottom slot to the legend
    rule = frame(bottom="soft") if i < 2 else "1"
    pad(g, CX0, TXT[0], r)
    quiet(g, TAG[0], TAG[1], r + 1, r + 2, tag, frame(fill), size=1000, color=color, line=1100)
    tight(g, TAG[0], r + 1, top=0, bottom=0, left=100, right=100)
    g.put(TAG[1], TXT[0], r + 1, r + 2, [])
    pad(g, CX0, TXT[0], r + 2)
    g.put(TXT[0], TXT[1], r, r + 3, [m(t, 1100) for t in lines], rule, align="LEFT", line=1250)
    g.put(TXT[1], CH[0], r, r + 3, [])
    for k, (a, e) in enumerate(zip(CH, CH[1:])):
        g.put(a, e, r, r + span, [[("■ ", 850, False, SERIES[series]), (values[k], 950, False, INK)]],
              frame(left="dot"), line=1100)
for a, e in zip(CH, CH[1:]):
    legend = []
    for name, shade in SERIES.items():
        legend += [("■", 750, False, shade), (f"{name} ", 750, False, INK)]
    legend[-1] = (legend[-1][0].rstrip(), 750, False, INK)
    quiet(g, a, e, 9, 10, [legend], frame(left="dot"), line=760)
    tight(g, a, 9, top=0, bottom=0)
block(g, 456.4)

# ---------------------------------------------------------------------------
# '25년 조직·인력 중점과제 (H.O.T.)
# ---------------------------------------------------------------------------
hot = ((CX0, 248.3), (255.8, 400.0), (407.0, X1))
xs = sorted({X0, LX, CX0, X1} | {x for a, e in hot for x in (a, a + 4.5, a + 25.0, e)})
g = Grid("hot", xs, [2360, 420, 1500, 1520, 3280])
label(g, 0, 5, ["’25년", "조직·인력", "중점과제"])
g.put(CX0, X1, 0, 1, "“ 조직 및 인력 역량 극대화를 위한 3대 중점과제 (H.O.T.) 도출 ”", frame(DARK),
      size=1250, bold=True, color=WHITE)
pad(g, CX0, X1, 1)
HOT = (("H", "Harmony", "*시너지* 중심 협업체계 확립", ("· 전략연계 및 실행력 강화 구조수립", "· 시너지 창출형 조직·인력 협업 강화")),
       ("O", "Optimization", "R&R 명확화, 중복 제거로 *최적화*",
        ("· 컨트롤타워 신설로 중복기능 통폐합", "· 데브옵스^Dev+Ops^ 연계 조직·인력배치")),
       ("T", "Timely", "경영현안의 *적시적* 해결 능력 강화", ("· 경영현안 해결을 위한 탄력적 조직", "· 적재적소 배치로 유휴인력 최소화")))
for (a, e), (letter, name, line2, bullets) in zip(hot, HOT):
    g.put(a, a + 4.5, 2, 3, [], frame(top="mid", left="mid"))
    g.put(a + 4.5, a + 25.0, 2, 3, letter, frame("#888888"), size=1200, bold=True, color=WHITE, line=1300, fit=False)
    tight(g, a + 4.5, 2, left=0, right=0)
    g.put(a + 25.0, e, 2, 3, name, frame(top="mid", right="mid"), size=1200, bold=True, align="LEFT", line=1300)
    g.put(a, e, 3, 4, [m(line2, 1100)], frame(left="mid", right="mid"), align="LEFT")
    tight(g, a, 3, left=500)
    g.put(a, e, 4, 5, [m(t) for t in bullets], frame(LIGHT), align="LEFT", line=1350)
block(g, 557.2)

# ---------------------------------------------------------------------------
# 장애요인 및 극복방안 / 관리체계 및 성과창출: left box ▶ right box
# ---------------------------------------------------------------------------
LB, AR, RB = (CX0, 265.2), (265.2, 277.3), (277.3, X1)
TG = (282.0, 323.9)


def tagged_rows(g, rows, r0, fill, color, line=1340):
    """Right box: tag cell | text cell per row, box sides on the outer cells."""
    for r, (tag, text) in enumerate(rows, r0):
        g.put(RB[0], TG[0], r, r + 1, [], frame(left="mid"))
        quiet(g, TG[0], TG[1], r, r + 1, tag, fill, size=950, bold=color == WHITE, color=color, line=1050)
        tight(g, TG[0], r, top=0, bottom=0, left=40, right=40)
        quiet(g, TG[1], RB[1], r, r + 1, [m(text, 1100)], frame(right="mid"), align="LEFT", line=line)
        tight(g, TG[1], r, top=0, bottom=0, left=200)


xs = sorted({X0, LX, CX0, X1, *LB, *AR, *RB, *TG})
g = Grid("barriers", xs, [1800, 300, 1340, 1340, 1340, 260])
label(g, 0, 6, ["장애요인", "및", "극복방안"])
g.put(*LB, 0, 1, "장애요인", frame("#CBCBCB", top="mid", left="mid", right="mid"), size=1200, bold=True)
g.put(*RB, 0, 1, "극복방안", frame(DARK, top="mid", left="mid", right="mid"), size=1200, bold=True, color=WHITE)
g.put(*LB, 1, 6, [m(t, 1100) for t in ("· 정원 제한으로 신사업 인력 확보 어려움", "· 조직 간 상충되는 이해관계 존재",
                                         "· 변화에 대한 거부감 해결필요")], frame(**BOX), align="LEFT", line=1340)
g.put(*AR, 1, 6, "▶", size=1000, color="#9A9A9A", fit=False)
g.put(*RB, 1, 2, [], frame(left="mid", right="mid"))
tagged_rows(g, (("Top-Down", "주기적 회의체, 시스템을 통한 상시 점검체계 가동"),
                ("Bottom-Up", "TF-업무협의체를 통한 직원참여형 개선사항 도출"),
                ("지원체계", "직무교육, 경영소통회 등 온·오프라인 제도 활성화")), 2, frame("#323232"), WHITE)
g.put(*RB, 5, 6, [], frame(left="mid", right="mid", bottom="mid"))
block(g, 654.2)

TG2 = (118.5, 137.0)
xs = sorted({X0, LX, CX0, X1, *LB, *AR, *RB, *TG2})
g = Grid("management", xs, [1770, 400, 1270, 1270, 1270, 410])
label(g, 0, 6, ["관리체계", "및", "성과창출"])
g.put(*LB, 0, 1, "지속가능 관리체계", frame("#CBCBCB", top="mid", left="mid", right="mid"), size=1200, bold=True)
g.put(*RB, 0, 1, "’25년 주요성과", frame("#747474", top="mid", left="mid", right="mid"), size=1200, bold=True,
      color=WHITE)
g.put(*LB, 1, 2, [], frame(left="mid", right="mid"))
for r, tag, text in ((2, "정기", "인력 수요파악 등 정원 증원 노력"), (4, "상시", "현업부서 니즈 검토 및 조정")):
    g.put(LB[0], TG2[0], r, r + 1, [], frame(left="mid"))
    quiet(g, TG2[0], TG2[1], r, r + 1, tag, frame(WHITE, top="soft", bottom="soft", left="soft", right="soft"),
          size=1000, line=1100)
    tight(g, TG2[0], r, top=0, bottom=0, left=0, right=0)
    quiet(g, TG2[1], LB[1], r, r + 1, [m(text, 1100)], frame(right="mid"), align="LEFT", line=1250)
    tight(g, TG2[1], r, top=0, bottom=0, left=150)
quiet(g, *LB, 3, 4, [[("→ ", 1100, True, INK)] + m("AI·안전 등 핵심분야 중심 전략적 증원", 1100)],
      frame(left="mid", right="mid"), align="LEFT", line=1250)
tight(g, LB[0], 3, top=0, bottom=0)
g.put(*LB, 5, 6, [], frame(left="mid", right="mid", bottom="mid"))
g.put(*AR, 1, 6, "▶", size=1000, color="#9A9A9A", fit=False)
g.put(*RB, 1, 6, [m(t, 1100, True, light=True) for t in (
    "· 최근 5개년 최대 정원 증원 확보{(6명}^’24년^{ → 58명}^’25년^{)}로 인력 확충",
    "· 인력활용 극대화로 노동생산성 제고{(1.31억원}^’24년^{ → 1.34억원}^’25년^{)}",
    "· 직원참여 조직재설계로 혁신인식도 최고점 달성{(87.4점}^’24년^{→ 90.1점}^’25년^{)}")],
      frame(**BOX), align="LEFT", line=1300)
block(g, 723.5)

g = Grid("footnote", [X0, X1], [1150])
g.put(X0, X1, 0, 1, [line1(55, 60, 790, 795)], align="LEFT", line=990)
block(g, 791.0)

kit.finish(target, end=803.5)
