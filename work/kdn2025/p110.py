"""Rebuild KDN 2025 report page 110 (3rd PDF local page 10, printed page 75) as editable HWPX.

Usage: python3 work/kdn2025/p110.py <report3.pdf> <out.hwpx> [--page 10]

재무성과관리(재무예산관리) 평가내용 03 opening page. Only the 평가내용 title, the section-1 band,
the 가. / 나. titles and the page number are in the PDF text layer; they are taken from it. Both
diagrams (가. y 161-502: 환경분석 ~ '25년 과제, 나. y 534-802: P-D-C-A 관리체계) are images: their
text was read from 5x-6x renders and is typed into cells on the image's own grid (label column |
content), band by band. Built with the shared kit.
Shapes and glyphs: the K / D / N hexagons and tabs -> dark cells with the letter; the P / D / C / A
pills -> dark cells; numbered dark squares 1-6 -> ①-⑥; the circled arrows of 점검 / 협력 -> ▶;
list dots -> ·; the chevron step shapes -> plain fills; the wedges under the target table and the
"Kdn" logo in the 시사점 band are dropped; the thick black frames around the '25년 목표 column and
the 8,080억원 / 본부 values -> strong borders. Table values cross-check: CAGR '25->'35
(8,080->19,974 = 9.5 %, 34.4->44.9 = 2.7 %, 10.7->15.2 = 3.6 %), 445/7,255 = 6.1 %,
742/7,891 = 9.4 %, 866/8,080 = 10.7 %, 3,207 + 4,229 + 644 = 8,080.
Printed as in the source: the double space in "사업조직  및 사업관리 조직".
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kit  # noqa: E402
from kit import Layout, recipe_inputs  # noqa: E402

source, target = recipe_inputs(10, "재무성과 극대화를 위한 도전적 중장기 재무목표 설정과 전사적 실행체계 강화")
L = Layout(top=3100)
kit.setup(source, L)
from kit import *  # noqa: E402,F401,F403  helpers and presets bound to this page

LAB, IN = 114.0, 122.0           # label column end, content start (가. diagram)
LABEL, HEAD, LIGHT = "#E3E3E3", "#D9D9D9", "#EBEBEB"
TAG_DARK = "#7E7E7E"
OUTLINED = frame(WHITE, top="soft", bottom="soft", left="soft", right="soft")
HATCH = frame("#EEEEEE", hatch="#DCDCDC")
TEXT = 1050


def S(text, size=TEXT, bold=False, color=INK):
    return (text, size, bold, color)


def dot(*parts, size=TEXT):
    """'· text' bullet; parts are str (body size) or (text, size) for smaller runs."""
    runs = [S("· ", size, False, "#8A8A8A")]
    for part in parts:
        runs.append(S(part, size) if isinstance(part, str) else S(*part))
    return runs


def flat(g, x0, r0, left=320, right=180):
    """Zero top/bottom padding so a cell fits a thin row."""
    c0 = g.xs.index(to_x(x0))
    item = g.items[r0, c0]
    g.items[r0, c0] = (*item[:7], dict(left=left, right=right, top=0, bottom=0))


def label(g, r0, r1, lines, fill=LABEL, color=INK, bold=False, x1=LAB, **edges):
    g.put(X0, x1, r0, r1, [[S(t, 1100, bold, color)] for t in lines], frame(fill, **edges), line=1300)


def pill(g, r, letter):
    """P / D / C / A: dark pill in the label column (row r)."""
    g.put(70.0, 104.0, r, r + 1, letter, frame("#4A4A4A"), size=1250, bold=True, color=WHITE, line=1300, fit=False)
    flat(g, 70.0, r)


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

# 평가내용 03 band: chip (image, typed) in the corner, hatched one-line title.
g = Grid("band", [X0, 124.0, X1], [1950, 910])
g.put(X0, 124.0, 0, 1, "평가내용 03", frame("#565656", top="strong"), size=970, bold=True, color=WHITE, ratio=80)
g.put(X0, 124.0, 1, 2, [], frame("#E9E9E9", bottom="soft", left="soft", hatch="#DADADA"))
g.put(124.0, X1, 0, 2, [line1(125, 130, 76, 82)], frame("#E9E9E9", top="strong", bottom="soft", right="soft",
                                                             hatch="#DADADA"), align="LEFT", line=1480)
block(g, 70.9)

g = Grid("sec1", [X0, 84.5, X1], [2300])
g.put(X0, 84.5, 0, 1, [runs_of(line1(60, 70, 112, 117), WHITE)], frame("#5F5F5F"), line=1700)
g.put(84.5, X1, 0, 1, [line1(90, 95, 113, 117)], frame("#E5E5E5"), align="LEFT", line=1700)
block(g, 110.9)

g = Grid("title-ga", [X0, X1], [1700])
g.put(X0, X1, 0, 1, [line1(55, 60, 139, 143)], align="LEFT", line=1500)
block(g, 140.0)

# ---------------------------------------------------------------------------
# 가. diagram (image): 환경분석, 시사점, 추진방향
# ---------------------------------------------------------------------------
xs = [X0, LAB, IN, 152.8, 337.0, 341.8, 525.2, X1]
g = Grid("env", xs, [180, 1380, 3920])
label(g, 0, 3, ["환경분석"])
g.put(IN, 152.8, 1, 2, "대내", frame("#6E6E6E"), size=1050, color=WHITE)
g.put(152.8, 337.0, 1, 2, "사업구조 고도화 및 신사업 전환 필요성 확대", frame(HEAD, right="soft"), size=1100,
      align="LEFT")
flat(g, 152.8, 1)
g.put(341.8, 525.2, 1, 2, "정책이행 기반 재무건전성 및 공공성 제고", frame(HEAD, left="soft"), size=1100)
flat(g, 341.8, 1)
g.put(525.2, X1, 1, 2, "대외", frame("#6E6E6E"), size=1050, color=WHITE)
g.put(IN, 337.0, 2, 3, [dot("AX · DX 신수요 대응을 위한 신사업 추진역량 필요"), dot("주력사업 이익 둔화로 포트폴리오 전환 필요성 증대")],
      frame(bottom="soft", left="soft", right="soft"), align="LEFT", line=1500)
g.put(341.8, X1, 2, 3, [dot("정책환경 변화 대응을 위한 재무안전성 제고"), dot("ESG · 동반성장 등 공공성 강화 요구 확대")],
      frame(bottom="soft", left="soft", right="soft"), align="LEFT", line=1500)
block(g, 162.0)

g = Grid("insight", [X0, LAB, X1], [550, 2400, 830])
label(g, 0, 3, ["시 사 점"], "#9C9C9C", WHITE, True)
g.put(LAB, X1, 1, 2, "“안정성과 공공성 강화를 기반으로 지속가능한 성장과 수익성 제고”", frame("#6E6E6E"), size=1250,
      bold=True, color=WHITE)
block(g, 220.0)

dirs = ((IN, 263.0, 127.0, 148.0, "K", "Keep Growing", "지속적인 매출액 성장"),
        (270.0, 411.0, 275.0, 296.0, "D", "Durable Stability", "안정적 재무위험 관리"),
        (417.0, X1, 422.0, 443.0, "N", "Net-profit Enhance", "사업별 수익성 제고"))
xs = sorted({X0, LAB} | {x for d in dirs for x in d[:4]})
g = Grid("direction", xs, [3220])
label(g, 0, 1, ["추진방향"])
for a, e, b0, b1, letter, eng, kor in dirs:
    box = dict(top="soft", bottom="soft")
    g.put(a, b0, 0, 1, [], frame(left="soft", **box))
    g.put(b0, b1, 0, 1, letter, frame("#6A6A6A", hatch="#7A7A7A"), size=1300, bold=True, color=WHITE, fit=False)
    g.put(b1, e, 0, 1, [[S(eng, 1000)], [S(kor, 1150)]], frame(right="soft", **box), align="LEFT", line=1300)
block(g, 257.8)

# 중장기 목표설정 기준: hatched 지표선정 / 목표수준 lines and the target table.
cols = (IN, 136.0, 170.0, 217.5, 269.0, 320.0, 372.0, 424.0, 476.0, X1)
xs = sorted({X0, LAB, 128.0, 162.0} | set(cols))
g = Grid("targets", xs, [300, 1600, 1600, 520, 1680, 1560, 1700, 2070])
label(g, 0, 8, ["중 장 기", "목표설정", "기       준"])
for r, tag, runs in ((1, "지표선정", [S("중점 관리분야별", 1100), S("(성장성, 안정성, 수익성)", 850),
                                       S(" 재무예산 성과 계량평가지표 연계", 1100)]),
                     (2, "목표수준", [S("장기 재무관리계획 연계 매출 시나리오", 1100), S("(낙관, 기준, 비관)", 850),
                                       S(" 별 재무목표 설정", 1100)])):
    g.put(IN, 128.0, r, r + 1, [], HATCH)
    g.put(128.0, 162.0, r, r + 1, tag, OUTLINED, size=1000, line=1150)
    flat(g, 128.0, r, 40, 40)
    g.put(162.0, X1, r, r + 1, [runs], HATCH, align="LEFT", line=1250)
    flat(g, 162.0, r)
g.put(IN, X1, 0, 1, [])
flat(g, IN, 0)
heads = ("과거 3개년 평균", "’25년 목표", "’28년 계획", "’30년 계획", "’35년 계획", "중장기(’25~’35년) 평균(CAGR)")
rows = (("K", "성장성", "매  출  액", ("7,533억원", "8,080억원", "11,077억원", "13,652억원", "19,974억원", "9.5%")),
        ("D", "안정성", "부 채 비 율", ("44.9%", "34.4%", "56.3%", "66.6%", "44.9%", "2.7%")),
        ("N", "수익성", "영업이익률", ("9.4%", "10.7%", "11.8%", "12.3%", "15.2%", "3.6%")))
TOP = dict(top="mid", bottom="soft")
g.put(IN, 217.5, 4, 5, "재무지표", frame(**TOP), size=1000)
for k, text in enumerate(heads):
    a, e = cols[3 + k], cols[4 + k]
    fill = "#C8C8C8" if k == 5 else "#E6E6E6"
    edge = dict(left="strong", right="strong", top="strong", bottom="soft") if k == 1 else TOP
    g.put(a, e, 4, 5, text, frame(fill, **edge), size=(1000, 900)[k == 0] if k < 5 else 780)
for i, (letter, name, kpi, values) in enumerate(rows):
    r = 5 + i
    last = i == 2
    line = dict(bottom="mid" if last else "dot")
    g.put(IN, 136.0, r, r + 1, letter, frame("#E6E6E6", **line), size=1050, bold=True, color=INK)
    g.put(136.0, 170.0, r, r + 1, name, frame("#E6E6E6", **line), size=1050, bold=True, align="LEFT")
    g.put(170.0, 217.5, r, r + 1, kpi, frame("#E6E6E6", **line), size=1050)
    for k, value in enumerate(values):
        a, e = cols[3 + k], cols[4 + k]
        edge = dict(left="strong", right="strong", bottom="strong" if last else "dot") if k == 1 else line
        g.put(a, e, r, r + 1, value, frame(**edge), size=1050, align="CENTER" if k == 5 else "RIGHT")
block(g, 292.0)

# '25년 3대 재무목표 and '25년 과제.
goal_cols = ((IN, 158.5, 184.8, 266.0, "K", "매출 성장", 136.0, 165.0, "성장성", "매출액 8천억원 이상"),
             (266.0, 302.2, 328.2, 410.0, "D", "위험 관리", 279.0, 306.0, "안정성", "부채비율 40% 미만"),
             (410.0, 447.0, 473.2, X1, "N", "수익 제고", 422.0, 450.0, "수익성", "영업이익률 10% 이상"))
xs = sorted({X0, LAB} | {c for gc in goal_cols for c in gc[:4]} | {c for gc in goal_cols for c in gc[6:8]})
g = Grid("goals", xs, [2400, 2120, 1800, 1780])
label(g, 0, 2, ["’25년 3대", "재무목표"], WHITE, top="mid")
label(g, 2, 4, ["’25년 과제"], WHITE, top="mid", bottom="soft")
tasks = (([S("① 기저사업 매출성장 및 경쟁력 강화", 1000)], [S("② 사업다각화 및 시장다변화", 1000)]),
         ([S("③ 자산운용 효율화 및 부채구조 최적화", 1000)], [S("④ 사업 및 재무위험 사전 차단구조 강화", 1000)]),
         ([S("⑤ 수익성과 공공성 확보체계 고도화", 1000)],
          [S("⑥ 全주기", 1000), S("(편성-집행-절감)", 800), S(" 예산운영 효율화", 1000)]))
for k, ((a, t0, t1, e, letter, head, s0, s1, tag, text), pair) in enumerate(zip(goal_cols, tasks)):
    sep = dict(right="dot") if k < 2 else dict(right="soft")
    g.put(a, t0, 0, 1, [], frame(HEAD, top="mid"))
    g.put(t0, t1, 0, 1, letter, frame(TAG_DARK, top="mid"), size=1150, bold=True, color=WHITE, fit=False)
    g.put(t1, e, 0, 1, "  " + head, frame(HEAD, top="mid", **sep), size=1150, align="LEFT")
    g.put(a, s0, 1, 2, [], frame(LIGHT))
    g.put(s0, s1, 1, 2, tag, frame("#4F4F4F"), size=1000, color=WHITE, line=1200, ratio=80, fit=False)
    flat(g, s0, 1, 40, 40)
    g.put(s1, e, 1, 2, " " + text, frame(LIGHT, **sep), size=1100, align="LEFT")
    left = dict(left="soft") if k == 0 else {}
    g.put(a, e, 2, 3, [pair[0]], frame(top="soft", **sep, **left), align="LEFT")
    g.put(a, e, 3, 4, [pair[1]], frame(bottom="soft", **sep, **left), align="LEFT")
block(g, 420.0)

g = Grid("title-na", [X0, X1], [1700])
g.put(X0, X1, 0, 1, [line1(55, 60, 512, 516)], align="LEFT", line=1500)
block(g, 512.5)

# ---------------------------------------------------------------------------
# 나. diagram (image): P 계획수립 / D 달성노력 / C 점검·관리 / A 평가·환류
# ---------------------------------------------------------------------------
steps = ((121.0, 226.0, "01", "재무목표 기본(안) 수립", HEAD, INK),
         (226.0, 336.0, "02", "연간 재무목표 협의", "#4C4C4C", WHITE),
         (336.0, 443.0, "03", "연간 재무목표 확정", "#8C8C8C", WHITE),
         (443.0, X1, "04", "재무목표 배분", "#D0D0D0", INK))
plans = ([dot("전년 실적 및 사업 환경"), [S("   종합 고려 재무목표 도출")]],
         [dot("사업조직  및 사업관리 조직"), [S("   사업목표 협의체 신설"), S("(3회)", 850)]],
         [dot("경영진 보고 및 목표 재조정"), [S("   (Stretch Goal)", 900)]],
         [dot("사업/기획/전략부서 참여"), [S("   단위조직 목표 배분")]])
tables = ((121.0, 174.0, 223.0, (("매      출", "7,255억원"), ("영 업 이 익", "445억원"), ("영업이익률", "6.1%"))),
          (230.0, 283.0, 333.0, (("매      출", "7,891억원"), ("영 업 이 익", "742억원"), ("영업이익률", "9.4%"))),
          (338.0, 389.0, 440.0, (("매      출", "8,080억원"), ("영 업 이 익", "866억원"), ("영업이익률", "10.7%"))),
          (447.0, 508.0, X1, (("ICT본부", "3,207억원"), ("전력지능화본부", "4,229억원"), ("미래사업개발본부", "644억원"))))
xs = sorted({X0, 70.0, 104.0, LAB} | {x for s in steps for x in s[:2]} | {x for t in tables for x in t[:3]})
g = Grid("plan", xs, [600, 1300, 470, 3450, 1580, 1540, 1560, 340])
lab = frame(top="soft", left="soft")
g.put(X0, LAB, 0, 1, [], lab)
pill(g, 1, "P")
g.put(X0, LAB, 3, 4, [[S("계획수립", 1150)]], frame(left="soft"), line=1300)
g.put(X0, LAB, 4, 8, [], frame(left="soft", bottom="soft"))
for k, ((a, e, num, title, fill, color), bullets) in enumerate(zip(steps, plans)):
    g.put(a, e, 0, 3, [[S("STEP ", 750, False, color), S(num, 950, True, color)], [S(title, 1200, True, color)]],
          frame(fill), align="LEFT", line=1150)
    flat(g, a, 0)
    g.put(a, e, 3, 4, bullets, frame(right="dot") if k < 3 else "1", align="LEFT", line=1450)
for k, (a, m, e, pairs) in enumerate(tables):
    for i, (name, value) in enumerate(pairs):
        r = 4 + i
        edge = dict(top="mid" if i == 0 else None, bottom="soft")
        name_fill = frame("#E6E6E6", **edge) if k == 3 else frame(**edge)
        g.put(a, m, r, r + 1, name, name_fill, size=950 if k == 3 else 1000, align="CENTER" if k == 3 else "LEFT")
        box = k == 3 or (k == 2 and i == 0)
        vedge = dict(left="strong", right="strong", top="strong" if i == 0 else None,
                     bottom="strong" if (k == 2 or i == 2) else "soft") if box else edge
        g.put(m, e, r, r + 1, value, frame(**vedge), size=1050, align="RIGHT")
block(g, 534.8)

# D 달성노력: K / D / N tabs over gray heads, bullets.
dcols = ((120.0, 174.0, 205.0, 265.0, "K", "[매출] 안정적인 매출 성장", ("사업고도화 · 수탁역무 확대", "고객다변화 및 신사업 선점 투자")),
         (265.0, 325.0, 354.0, 409.5, "D", "[위험] 체계적 재무위험 관리", ("자산운용 및 부채요인 심의 강화", "사업리스크 검증절차 고도화")),
         (409.5, 472.0, 500.0, X1, "N", "[수익] 지속가능한 수익 제고", ("수익성과 공공성 균형과제 집중", "예산편성 · 집행 · 절감 체계화")))
xs = sorted({X0, 70.0, 104.0, LAB} | {x for d in dcols for x in d[:4]})
g = Grid("do", xs, [1200, 1900, 3300])
pill(g, 0, "D")
g.put(X0, 70.0, 0, 1, [], frame(top="soft", left="soft"))
g.put(104.0, LAB, 0, 1, [], frame(top="soft"))
g.put(X0, LAB, 1, 3, [[S("달성노력", 1150)], [S("(실행포인트)", 950)]], frame(left="soft", bottom="soft"), line=1300)
for k, (a, t0, t1, e, letter, head, items) in enumerate(dcols):
    sep = dict(right="dot") if k < 2 else {}
    g.put(a, t0, 0, 1, [], frame("#E6E6E6", top="mid"))
    g.put(t0, t1, 0, 1, letter, frame("#6A6A6A", top="mid"), size=1050, bold=True, color=WHITE, line=1100, fit=False)
    flat(g, t0, 0)
    g.put(t1, e, 0, 1, [], frame("#E6E6E6", top="mid"))
    g.put(a, e, 1, 2, head, frame("#E6E6E6", **sep), size=1150)
    g.put(a, e, 2, 3, [dot(t) for t in items], frame(**sep), align="LEFT", line=1500)
block(g, 648.0)

# C 점검/관리: 점검 / 협력 blocks with tagged lines.
check = (("상시", OUTLINED, INK, [S("EIS 연계 조직별 달성 수준 모니터링")]),
         ("신규", frame("#4A4A4A"), WHITE, [S("본부별 사업실적 개선 토론회"), S("(2회)", 850)]),
         ("개선", OUTLINED, INK, [S("연간손익전망"), S("(3회", 850), S("’24년", 600), S("→5회", 850), S("’25년", 600),
                                  S(")", 850)]))
coop = (("사업개발", [S("미래사업 분야별 자문위원 신규 선임"), S("(10명)", 850)]),
        ("상생성장", [S("중소기업 동반사업 확대"), S("(16건", 850), S("’24년", 600), S("→20건", 850), S("’25년", 600),
                     S(")", 850)]),
        ("투자협력", [S("산·학·관 사업 MOU 확대"), S("(29건", 850), S("’24년", 600), S("→38건", 850), S("’25년", 600),
                     S(")", 850)]))
xs = [X0, 70.0, 104.0, LAB, 120.0, 156.0, 164.5, 183.5, 317.2, 353.5, 358.8, 393.0, X1]
g = Grid("check", xs, [450, 1350, 1350, 1350, 200])
g.put(X0, 70.0, 0, 2, [], frame(top="soft", left="soft"))
g.put(104.0, LAB, 0, 2, [], frame(top="soft"))
g.put(70.0, 104.0, 0, 1, [])
pill(g, 1, "C")
g.put(X0, LAB, 2, 5, [[S("점검/관리", 1150)]], frame(left="soft", bottom="soft"), line=1300)
flat(g, X0, 2)
g.put(120.0, 156.0, 0, 5, "점검", frame("#D9D9D9"), size=1100)
g.put(317.2, 353.5, 0, 5, "협력", frame("#D9D9D9"), size=1100)
g.put(156.0, 164.5, 0, 5, "▶", size=650, color="#7A7A7A", fit=False)
g.put(353.5, 358.8, 0, 5, "▶", size=550, color="#7A7A7A", fit=False)
g.put(164.5, 317.2, 0, 1, [], frame(top="dot"))
g.put(358.8, X1, 0, 1, [], frame(top="dot"))
for i, ((tag, fill, color, runs), (tag2, runs2)) in enumerate(zip(check, coop)):
    r = 1 + i
    g.put(164.5, 183.5, r, r + 1, tag, fill, size=950, color=color, line=1050, ratio=85, fit=False)
    flat(g, 164.5, r, 30, 30)
    g.put(183.5, 317.2, r, r + 1, [runs], align="LEFT", line=1250)
    flat(g, 183.5, r, 200, 100)
    g.put(358.8, 393.0, r, r + 1, tag2, OUTLINED, size=950, line=1050, ratio=80, fit=False)
    flat(g, 358.8, r, 30, 30)
    g.put(393.0, X1, r, r + 1, [runs2], align="LEFT", line=1250)
    flat(g, 393.0, r, 200, 100)
g.put(164.5, 317.2, 4, 5, [], frame(bottom="dot"))
flat(g, 164.5, 4, 0, 0)
g.put(358.8, X1, 4, 5, [], frame(bottom="dot"))
flat(g, 358.8, 4, 0, 0)
block(g, 714.0)

# A 평가·환류: dark pills with the two lines in an outlined box.
g = Grid("act", [X0, 70.0, 104.0, LAB, 120.2, 216.2, X1], [1800, 1780])
g.put(X0, 70.0, 0, 1, [], frame(top="soft", left="soft"))
g.put(104.0, LAB, 0, 1, [], frame(top="soft"))
pill(g, 0, "A")
g.put(X0, LAB, 1, 2, [[S("평가·환류", 1150)]], frame(left="soft"), line=1300)
for r, tag, runs in ((0, "내부성과평가 연계", [S("全조직 매출액/영업이익 목표 달성률 지표 및 경상경비 절감률 지표 부여", 1100)]),
                     (1, "차년도 재무목표 수립", [S("全보직자 참여 미흡사항 개선 및 차년도 사업계획 공유 리더 워크숍", 1100),
                                             S("(11월)", 850)])):
    edge = dict(top="soft") if r == 0 else dict(bottom="soft")
    g.put(120.2, 216.2, r, r + 1, tag, frame(TAG_DARK, **edge), size=1100, bold=True, color=WHITE)
    g.put(216.2, X1, r, r + 1, [runs], frame(right="soft", **edge), align="LEFT", line=1300)
block(g, 766.2)

kit.finish(target, end=802.0)
