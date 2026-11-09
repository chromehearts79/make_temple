"""Rebuild KDN 2025 report physical PDF page 18 (printed page 6) as editable HWPX.

Usage: python3 work/kdn2025/p18.py <report.pdf> <out.hwpx> [--page N]

Opening page of "Ⅳ. 세부 평가내용별 추진실적" (평가내용 01 banner + section 1). Only the page
title, the banner, the summary box, the section/sub-section headings and the page number are in
the PDF text layer. The STEP 01-03 diagram, the paradigm table, the "평가내용 01" chip, the
"Best Practice" tag and the PART label are images; their text was read from 5x renders and is
typed here. Icons, the globe illustration and the logo are omitted (the logo is typed as text).
Built with the shared kit (one flat table per band on a PDF-x union grid).
"""

import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kit  # noqa: E402
from kit import Layout, recipe_inputs  # noqa: E402

source, target = recipe_inputs(18, "세부 평가내용별 추진실적")
L = Layout(top=3100)
kit.setup(source, L)
from kit import *  # noqa: E402,F401,F403  helpers and presets bound to this page

LIGHT, MID, DEEP = "#EDEDED", "#DADADA", "#6E6E6E"


def underline(grid, key, par_index, run_indexes):
    """Underline some runs of one paragraph of an already placed cell (charPr copy)."""
    par = grid.items[key][3][par_index]
    runs = par.findall(L.q("hp:run"))
    for k in run_indexes:
        base = L.characters.find(f"hh:charPr[@id='{runs[k].get('charPrIDRef')}']", L.ns)
        el = deepcopy(base)
        L.sub(el, "hh:underline", type="BOTTOM", shape="SOLID", color=INK)
        runs[k].set("charPrIDRef", L.append_style(L.characters, el))


# ---------------------------------------------------------------------------
# Page chrome: even page -> PART label at the left of the running rule, footer at the left.
# ---------------------------------------------------------------------------
foot = [(line1(55, 60, 815, 822)["text"], 1090, False, INK), ("     ", 1090, False, INK),
        ("한전KDN㈜", 1090, True, "#5A5A5A")]
L.add_table([[cell(0, W, 1500, [para(foot, "LEFT", 1300)[0]])]], floating=(5660, 81550))

g = Grid("head", [X0, 102.6, 158.0, 160.0, X1], [1600])
g.put(X0, 102.6, 0, 1, [[("PART ", 900, False, INK), ("01", 1400, True, "#7A7A7A")]], frame("#F2F2F2", top="soft"),
      line=1400)
g.put(102.6, 158.0, 0, 1, "경영관리", frame("#333333"), size=1150, bold=True, color=WHITE)
g.put(160.0, X1, 0, 1, [], frame(bottom="soft"))
block(g, 31.0)

# Page title
g = Grid("title", [X0, X1], [2300])
g.put(X0, X1, 0, 1, [line1(195, 205, 68, 75)], line=2100)
block(g, 69.0)

# 평가내용 01 banner: dark chip (image) at the top-left, hatched title area (text layer).
g = Grid("banner", [X0, 122.0, X1], [1500, 2650])
g.put(X0, 122.0, 0, 1, "평가내용 01", frame("#4A4A4A", top="strong"), size=950, bold=True, color=WHITE, line=1100)
g.put(X0, 122.0, 1, 2, [], frame("#E9E9E9", bottom="soft", left="soft", hatch="#D2D2D2"))
g.put(122.0, X1, 0, 2, lines_in(120, 135, 108, 145), frame("#E9E9E9", top="strong", bottom="soft", right="soft",
                                                          hatch="#D2D2D2"), align="LEFT", line=1480)
block(g, 105.5)

# Summary box: grey rules with a dark centre tab, two centred lines (number chips are images).
g = Grid("summary", [X0, 229.6, 377.0, X1], [320, 3960, 320])
g.put(X0, 229.6, 0, 1, [], frame("#C4C4C4"))
g.put(229.6, 377.0, 0, 1, [], frame("#3A3A3A"))
g.put(377.0, X1, 0, 1, [], frame("#C4C4C4"))
second = [(runs_of(line1(130, 135, 182, 190))[0][0] + " ", 1190, True, INK)]
for k, x in enumerate((158, 232, 366)):
    head, rest = runs_of(line1(x - 1, x + 1, 182, 190))[0][0].split(" ", 1)
    second += [("①②③"[k] + " ", 1190, True, INK), (head, 1190, True, INK), (" " + rest + " ", 1190, True, INK)]
second[-1] = (second[-1][0].rstrip(), *second[-1][1:])
second = [r for r in second if r[0]]
g.put(X0, X1, 1, 2, [line1(145, 150, 165, 170), second], frame(LIGHT), line=1650)
underline(g, (1, 0), 1, [i for i, r in enumerate(second) if r[0] in ("디지털", "에너지", "글로벌")])
g.put(X0, X1, 2, 3, [], frame("#C4C4C4"))
block(g, 159.0)

# Section 1 heading
g = Grid("section-1", [X0, 85.5, 88.5, X1], [2300])
g.put(X0, 85.5, 0, 1, [line1(60, 70, 218, 225)], frame("#6E6E6E"), color=WHITE, line=1900)
g.put(88.5, X1, 0, 1, [line1(90, 95, 218, 225)], frame("#E6E6E6"), align="LEFT", line=1750)
block(g, 217.8)

title_band("title-ga", line1(55, 60, 248, 252), [X0, 76.5, 154.4, X1], 248.9)

# ---------------------------------------------------------------------------
# STEP 01 WHY 환경분석 (image): three tabs joined by "+", bullets, findings bar, conclusion.
# ---------------------------------------------------------------------------
side = dict(left="mid")


def step_label(g, r0, r1, rr0, rr1, num, word, label):
    g.put(63.0, 97.5, r0, r1, [[("STEP ", 700, False, WHITE), (num, 1000, True, WHITE)]], frame("#4A4A4A"),
          line=1050)
    g.put(X0, 103.0, rr0, rr1, [[(word, 1400, True, "#5E5E5E")], [(label, 1000, False, INK)]], frame(**side))


xs = [X0, 63.0, 97.5, 103.0, 244.5, 249.0, 253.5, 398.0, 402.0, 406.5, X1]
g = Grid("step01", xs, [1700, 1350, 1350, 880, 1700, 220, 1720])
g.put(X0, 103.0, 0, 1, [], frame(top="mid", left="mid"))
g.put(X0, 63.0, 1, 2, [], frame(**side))
step_label(g, 1, 2, 2, 6, "01", "WHY", "환경분석")
g.put(X0, 103.0, 6, 7, [], frame(left="mid", bottom="mid"))
tabs = [(103.0, 244.5, "정부정책 정합성"), (253.5, 398.0, "외부환경 변화 대응"),
        (406.5, X1, "3C(경쟁, 고객 · 시장, 내부역량)")]
for a, e, text in tabs:
    g.put(a, e, 0, 1, text, frame("#E2E2E2"), size=1150, bold=True)
for a, e in ((244.5, 253.5), (398.0, 406.5)):
    g.put(a, e, 0, 1, "+", size=1100, bold=True, color="#9A9A9A", fit=False)
cols = [(103.0, 249.0), (249.0, 402.0), (402.0, X1)]
bullets = [("AI · 에너지 고속도로 구축 가속화", "탄소중립 실현, 분산E전환 확대"),
           ("재생E 확대로 전력계통 복잡성 증가", "분산화 · 통합운영 기술 고도화 요구"),
           ("그룹사 AX · DX 자체 투자 및 사업 확대", "디지털 · AI 전문인재 확보 필요")]
findings = ["AI · 에너지 융합 정책 확산", "에너지전환 · 탄소중립 가속화", "퀀텀 성장을 위한 동력 마련 필요"]
for k, ((a, e), pair, found) in enumerate(zip(cols, bullets, findings)):
    sep = dict(right="dot") if k < 2 else {}
    for r, text in enumerate(pair, 1):
        g.put(a, e, r, r + 1, [[("▶ ", 750, False, "#7A7A7A"), (text, 1080, False, INK)]], frame(**sep),
              align="LEFT", line=1180)
    g.put(a, e, 3, 4, "▼", frame(**sep), size=700, color="#8C8C8C", line=720)
    g.put(a, e, 4, 5, found, frame("#D6D6D6", **({"right": "soft"} if k < 2 else {})), size=1100)
g.put(103.0, X1, 6, 7, "국정과제 이행과 미래 성장을 동시 달성하는 ‘2035 New Vision 수립’",
      frame("#EBEBEB", hatch="#D4D4D4"), size=1150, bold=True)
block(g, 271.7)

# ---------------------------------------------------------------------------
# STEP 02 WAY 방향수립 (image): Vision 2030 diagnosis -> Vision 2035 expansion.
# ---------------------------------------------------------------------------
xs = [X0, 63.0, 97.5, 103.0, 133.5, 257.5, 305.0, 321.0, 349.5, X1]
g = Grid("step02", xs, [1850, 2700, 1450, 2700, 2700, 1500, 2700, 1200])
g.put(X0, 63.0, 0, 1, [], frame(top="mid", left="mid"))
g.put(97.5, 103.0, 0, 1, [], frame(top="mid"))
step_label(g, 0, 1, 1, 3, "02", "WAY", "방향수립")
g.put(X0, 103.0, 3, 7, [], frame(left="mid", bottom="mid"))
head = frame(top="mid", bottom="soft")
g.put(103.0, 133.5, 0, 1, "구분", head, size=1200)
g.put(133.5, 257.5, 0, 1, "Vision 2030", head, size=1400)
g.put(257.5, 305.0, 0, 1, "진단기준", head, size=1200)
g.put(305.0, 321.0, 0, 1, [], frame(top="mid"))
g.put(321.0, 349.5, 0, 1, "구분", head, size=1200)
g.put(349.5, X1, 0, 1, "Vision 2035", head, size=1400)
label = frame("#DADADA", bottom="soft")
left_rows = [((1, 3), "미션", ["에너지ICT 기술 전문화 및", "고도화를 통해 에너지산업", "발전에 기여"],
              ["목적사업,", "핵심역할,", "지향가치"]),
             ((3, 5), "비전", ["친환경, 디지털 중심의", "에너지ICT 플랫폼 전문기업"],
              ["제공가치,", "미래상,", "핵심역량,", "사업영역"]),
             ((5, 7), ["핵심", "가치"], ["미래선도, 전문기술,", "국민신뢰, 혁신추구"], ["고객, 회사,", "국민, 직원"])]
for (r0, r1), name, vision, basis in left_rows:
    last = r1 == 7
    dash = "soft" if last else "dot"
    g.put(103.0, 133.5, r0, r1, name if isinstance(name, str) else [[(t, 1200, True, INK)] for t in name],
          label, size=1200, bold=True)
    g.put(133.5, 257.5, r0, r1, [[(t, 1080, False, INK)] for t in vision], frame(bottom=dash, right="soft"),
          line=1250)
    g.put(257.5, 305.0, r0, r1, [[(t, 1080, False, INK)] for t in basis], frame(bottom=dash), line=1250)
g.put(305.0, 321.0, 1, 7, "▶", size=1500, color="#8C8C8C", fit=False)
right_rows = [((1, 2, 3), ["의미", "확장"], ["전문성 기반, 설립 목적과 역할 등 에너지ICT", "공기업 존재 이유 명확"],
               ["→사업 범위 확장 및 새정부정책 이행 강화"]),
              ((3, 4, 5), ["미래", "확장"], ["“디지털 혁신, 에너지 대전환을 선도하는", "글로벌 에너지ICT의 중심”"],
               ["→성장 정체의 한계를 넘는 AI가속화(AX) 및", "  에너지ICT 글로벌 시장확장의 미래 지향점 강조"]),
              ((5, 6, 7), ["가치", "확장"], ["“미래주도, 기술선도, 도전의식, 소통협력, 청렴윤리”"],
               ["→신규 비전 달성을 위한 핵심가치 추가", "  [도전적 기술확보, 소통중심의 거버넌스, 청렴한 조직문화]"])]
for (r0, rm, r1), name, quote, arrow in right_rows:
    last = r1 == 7
    g.put(321.0, 349.5, r0, r1, [[(t, 1200, True, INK)] for t in name], label)
    g.put(349.5, X1, r0, rm, [[(t, 1080, False, INK)] for t in quote], frame("#EBEBEB", left="soft"), line=1250)
    runs = [[(t, 1080 if k == 0 else 1000, False, INK)] for k, t in enumerate(arrow)]
    g.put(349.5, X1, rm, r1, runs, frame(left="soft", bottom="soft" if last else "dot"), align="LEFT", line=1250)
g.put(X0, X1, 7, 8, "▼", size=1000, color="#8C8C8C", line=1000)
block(g, 365.0)

# ---------------------------------------------------------------------------
# STEP 03 WIN 포인트 선정 (image): conclusion band and three numbered cards.
# ---------------------------------------------------------------------------
cards = [(103.0, 156.5, 194.5, 250.0), (254.0, 308.5, 346.5, 404.0), (408.0, 460.5, 498.5, X1)]
xs = [X0, 63.0, 97.5, 103.0] + sorted({x for c in cards for x in c} - {103.0})
g = Grid("step03", xs, [1900, 1500, 1800, 2700])
g.put(X0, 103.0, 0, 1, [], frame(top="mid", left="mid"))
g.put(X0, 63.0, 1, 2, [], frame(**side))
step_label(g, 1, 2, 2, 4, "03", "WIN", "포인트 선정")
g.put(103.0, X1, 0, 1, "① AI기반 기술 혁신으로 ② 에너지 대전환을 선도하여 ③ 글로벌 리더로 도약하는 선순환 체계 확립",
      frame("#EBEBEB", hatch="#D4D4D4"), size=1180, bold=True)
titles = [("디지털", " 혁신(AX · DX) 주도"), ("에너지", " 대전환 선도"), ("글로벌", " 에너지ICT기업 도약")]
bodies = [("단순 ICT 기업을 넘어 AI데이터센터,", "플랫폼 기반 사업포트폴리오 변화"),
          ("분산E · 계통 운영ICT 기술 고도화를", "통한 에너지 산업 생태계 전환"),
          ("자체 솔루션 경쟁력기반 국내시장 한계", "극복 및 질적성장 추진")]
for k, ((a, b, c_, e), (bold_word, rest), body) in enumerate(zip(cards, titles, bodies)):
    g.put(a, b, 1, 2, [], frame(top="mid", left="mid"))
    g.put(b, c_, 1, 2, f"0{k + 1}", frame("#6A6A6A"), size=1150, bold=True, color=WHITE)
    g.put(c_, e, 1, 2, [], frame(top="mid", right="mid"))
    g.put(a, e, 2, 3, [[(bold_word, 1300, True, INK), (rest, 1150, False, INK)]],
          frame("#D6D6D6", left="mid", right="mid"), line=1500)
    g.put(a, e, 3, 4, [[(t, 1080, False, INK)] for t in body], frame("#EFEFEF", left="mid", right="mid",
                                                                       bottom="soft"), line=1250)
block(g, 533.0)

# 나. heading with the "Best Practice" tag (image) at the right.
runs = runs_of(line1(55, 60, 622, 627))
g = Grid("title-na", [X0, 76.5, 142.1, 485.8, X1], [1650])
g.put(X0, 76.5, 0, 1, [strip_runs(runs[:1])], align="LEFT", line=1450)
g.put(76.5, 142.1, 0, 1, [runs[1]], pill)
g.put(142.1, 485.8, 0, 1, [strip_runs(runs[2:])], align="LEFT", line=1450)
g.put(485.8, X1, 0, 1, "Best Practice", frame("#4A4A4A"), size=900, bold=True, color=WHITE)
block(g, 623.5)

# ---------------------------------------------------------------------------
# Paradigm table (image): HOW / WHAT / WHERE x four keyword columns, then the declaration band.
# ---------------------------------------------------------------------------
xs = [X0, 127.5, 130.0, 170.0, 234.0, 238.0, 341.5, 345.5, 458.0, 462.0, X1]
cols = [(130.0, 234.0), (238.0, 341.5), (345.5, 458.0), (462.0, X1)]
g = Grid("paradigm", xs, [1800, 1500, 1450, 400, 1500, 1450, 450, 1500, 1450, 1250, 2150])
heads = ["Vision 2030 키워드", "전환 배경", "기관의 역할", "Vision 2035 키워드"]
for k, ((a, e), text) in enumerate(zip(cols, heads)):
    last = k == 3
    g.put(a, e, 0, 1, text, frame("#707070" if last else None, top="mid", left="mid", right="mid"),
          size=1200, bold=not last, color=WHITE if last else INK)
rows = [("HOW", " to change", "전환의 방식",
         [("디지털 중심", "(디지털 전환)"), (None, ["AI전환 가속화 시대,", [("축적된 디지털 역량 ", 1050, False), ("강화", 1300, True)]]),
          ("미래 주도", "AI 혁신으로 에너지산업 AX·DX 주도"), ("디지털 혁신", "(AX · DX)")]),
        ("WHAT", " to change", "전환의 대상",
         [("친환경", "(탄소저감, 환경대응 중심)"), (None, ["기후위기를 돌파하고", [("에너지질서의 주도권 ", 1050, False), ("선점", 1300, True)]]),
          ("기술 선도", "탄소중립 대응을 넘어 에너지전환 선도"), ("에너지 대전환", "(분산E 체계로의 전력망 재편)")]),
        ("WHERE", " to stand", "전환 후 위치",
         [("에너지ICT 플랫폼 전문기업", "(국내ICT, 전문기업)"), (None, ["사업영역의 다각화로", [("시장과 고객 ", 1050, False), ("확장", 1300, True)]]),
          ("글로벌 도약", "글로벌 에너지ICT 생태계의 중심으로 도약"), ("글로벌", "(글로벌, 에너지 생태계 허브)")])]
for k, (word, tail, name, values) in enumerate(rows):
    r = 1 + 3 * k
    g.put(X0, 127.5, r, r + 1, [[(word, 1000, True, INK), (tail, 900, False, "#808080")]], frame("#E6E6E6"),
          align="LEFT", line=1150)
    g.put(X0, 127.5, r + 1, r + 2, name, frame("#BDBDBD"), align="RIGHT", size=1150, line=1280)
    for j, ((a, e), (top, low)) in enumerate(zip(cols, values)):
        fill = frame("#D9D9D9" if j == 3 else "#EBEBEB")
        if top is None:
            g.put(a, e, r, r + 2, [[(low[0], 1050, False, INK)], [(t, s, b, INK) for t, s, b in low[1]]], fill,
                  line=1380)
        else:
            g.put(a, e, r, r + 1, top, fill, size=1220, bold=True, line=1340)
            g.put(a, e, r + 1, r + 2, low, fill, size=1050 if j != 2 else 950, line=1220)
g.put(X0, X1, 9, 10, "▼", size=1000, color="#8C8C8C", line=1000)
g.put(X0, 170.0, 10, 11, "2035 New Vision 선포", frame("#C8C8C8"), size=1250, bold=True)
g.put(170.0, X1, 10, 11, [[("“ ", 1500, True, INK), ("디지털 혁신, 에너지 대전환을 선도하는 글로벌 에너지ICT의 중심", 1300, True, INK),
                            (" ”", 1500, True, INK)]], frame("#E9E9E9", hatch="#D4D4D4"), align="LEFT", line=1550)
block(g, 646.4)

kit.finish(target, end=802.0)
