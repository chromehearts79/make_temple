"""Rebuild KDN 2025 report physical PDF page 63 (printed page 40) as editable HWPX.

Usage: python3 work/kdn2025/p63.py <report.pdf> <out.hwpx> [--page N]
(the second PDF holds report pages 51-100, so this page is local page 13 there)

안전 및 재난관리 평가내용 01 opening page. Built with the shared kit (one flat table per
horizontal band on a grid of PDF x edges). Only the running head, the 평가내용 band title, the
section heading, the 기관장 의지 line and the footer are in the PDF text layer; they are taken
from it. The 평가내용 chip, the section number band and the whole 재난관리 diagram below the
기관장 의지 line (환경분석 ~ 재난관리 인프라, PDF y 185-800) are images: their text was read
from 4x / 5x renders and is typed here, row by row on the diagram's own grid (label column |
content). Shapes become fills and borders; the dark numbered squares become ①-⑥, the cycle
arrows between the four 재난관리체계 boxes become ▶ ▼ ◀ ▲ connector cells, the brace becomes a
rule with ▼, bullet dots become "·". The four small charts of 재난관리 인프라 become value
cells with the values they print (no drawn bars); the italic of the 기관장 quote is not kept.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kit  # noqa: E402
from kit import Layout, recipe_inputs  # noqa: E402

source, target = recipe_inputs(13, "에너지ICT 기반 재난 대응체계 구축으로 국민 생활 안정성 제고")
L = Layout(top=3100)
kit.setup(source, L)
from kit import *  # noqa: E402,F401,F403  helpers and presets bound to this page

DARK, LABEL = "#6A6A6A", "#E4E4E4"
DOT = "#8A8A8A"
BODY = 1050          # diagram body text
SMALL = 820          # parenthetical notes inside diagram lines
LAB, IN = 113.8, 121.2   # label column end, content start


def S(text, size=BODY, bold=False, color=INK):
    return (text, size, bold, color)


def bullet(*parts, size=BODY):
    """'· text' line; parts are str (body size) or (text, size) for smaller runs."""
    runs = [S("· ", size, False, DOT)]
    for part in parts:
        runs.append(S(part, size) if isinstance(part, str) else S(*part))
    return runs


def label(g, r0, r1, text, fill=LABEL, **kw):
    lines = text if isinstance(text, list) else [text]
    g.put(X0, LAB, r0, r1, [[S(t, 1090, kw.get("bold", False), kw.get("color", INK))] for t in lines],
          frame(fill), line=1250)


def tight(g, x0, r0, left=60, right=60):
    """Narrow the cell padding (kit cells use the builder default 320/180)."""
    c0 = g.xs.index(to_x(x0))
    item = g.items[r0, c0]
    g.items[r0, c0] = (*item[:7], dict(left=left, right=right))


# ---------------------------------------------------------------------------
# Page chrome (odd page): running head over a rule, side tab, footer at the right.
# ---------------------------------------------------------------------------
L.add_table([[cell(0, 3350, 1680, [para([("01", 1380, True, WHITE)], "CENTER")[0]], dark)],
             [cell(0, 3350, 5960, [para([(ch, 950, True, INK)], "CENTER", 1160)[0] for ch in "경영관리"], gray2)]],
            floating=(57800, 15000))
foot = [(text, size, False, INK) for text, size in (
    (line1(450, 455, 818, 822)["text"], 790), ("    ", 790), (line1(540, 552, 816, 820)["text"], 1090))]
L.add_table([[cell(0, W, 1500, [para(foot, "RIGHT", 1300)[0]])]], floating=(5660, 81550))

g = Grid("head", [X0, 398.0, X1], [1680])
g.put(X0, 398.0, 0, 1, [], frame(bottom="soft"))
g.put(398.0, X1, 0, 1, [line1(400, 410, 35, 40)], align="RIGHT")
block(g, 32.0)

# 평가내용 01 band (chip image typed, title from the text layer)
g = Grid("band", [X0, 124.0, X1], [1950, 2190])
g.put(X0, 124.0, 0, 1, "평가내용 01", frame("#565656", top="strong"), size=970, bold=True, color=WHITE, ratio=80)
g.put(X0, 124.0, 1, 2, [], frame("#E9E9E9", bottom="soft", left="soft", hatch="#DADADA"))
g.put(124.0, X1, 0, 2, lines_in(125, 130, 75, 100), frame("#E9E9E9", top="strong", bottom="soft",
                                                         right="soft", hatch="#DADADA"), align="LEFT", line=1480)
block(g, 70.9)

# Section band "1 에너지ICT 기반 ..."
g = Grid("section-1", [X0, 84.5, X1], [2300])
g.put(X0, 84.5, 0, 1, [runs_of(line1(64, 70, 125, 130), WHITE)], frame(DARK), line=1700)
g.put(84.5, X1, 0, 1, [line1(90, 95, 125, 130)], frame(LABEL), align="LEFT", line=1700)
block(g, 124.2)

# 기관장 의지: outlined label, quote on a gray band (text layer)
g = Grid("will", [X0, 122.1, X1], [2470])
g.put(X0, 122.1, 0, 1, [line1(60, 70, 158, 162)], frame(top="mid", bottom="mid", left="mid", right="mid"))
g.put(122.1, X1, 0, 1, [line1(160, 170, 158, 162)], frame(LABEL))
block(g, 153.5)

# ---------------------------------------------------------------------------
# Diagram (image in the PDF; text read from 4x renders)
# ---------------------------------------------------------------------------
# 환경분석: 외부환경 | 내부환경 boxes
E = [(121.5, 336.5), (341.0, X1)]
g = Grid("env", [X0, LAB] + [x for e in E for x in e], [2020, 3620])
label(g, 0, 2, "환경분석", "#C8C8C8")
env = [("외부환경", ["재난의 복합화에 따른 연쇄 반응 및 피해 대형화",
                    "국가 핵심시설 사이버 공격에 따른 시스템 마비 심각"]),
       ("내부환경", ["전력 ICT 전담 기관으로서 세계 최고품질의 전력망 공급",
                    "53개 공공기관 24시 무결점 통합 보안 관제 체계 가동"])]
for (a, e), (head, items) in zip(E, env):
    g.put(a, e, 0, 1, head, frame("#BEBEBE", top="soft", left="soft", right="soft"), size=1100, bold=True)
    g.put(a, e, 1, 2, [bullet(t) for t in items], frame(bottom="soft", left="soft", right="soft"),
          align="LEFT", line=1500)
block(g, 185.8)

# 시사점: hatched box with a bold conclusion
g = Grid("implication", [X0, LAB, IN, X1], [2800])
label(g, 0, 1, "시 사 점", "#C0C0C0")
g.put(IN, X1, 0, 1, "내부 재난 관리체계 재정립 및 에너지ICT 역량 기반의 국가 안전망 구축 선도 필요",
      frame("#F2F2F2", top="soft", bottom="soft", left="soft", right="soft", hatch="#DCDCDC"),
      size=1150, bold=True, line=1350)
block(g, 248.5)

# 추진목표: dark band from the label column to the right edge
g = Grid("goal", [X0, LAB, X1], [2960])
label(g, 0, 1, "추진목표", "#A8A8A8", bold=True, color=WHITE)
g.put(LAB, X1, 0, 1, "최고수준의 에너지ICT와 사이버 보안 역량으로 선제적 재난 예방 및 실전 대응 역량 확보",
      frame("#787878"), size=1200, bold=True, color=WHITE, line=1400)
block(g, 283.2)

# 추진방향: two pills
g = Grid("direction", [X0, LAB, 121.2, 330.0, 346.5, X1], [2350])
label(g, 0, 1, "추진방향")
g.put(121.2, 330.0, 0, 1, "선제적 재난 대응체계 고도화", frame("#D8D8D8"), size=1100, bold=True)
g.put(346.5, X1, 0, 1, "국가 핵심 기반시설 재난 보호", frame("#D8D8D8"), size=1100, bold=True)
block(g, 320.5)

# 추진과제: 내부 / 외부 boxes, dark tag + title, three numbered tasks each
T = [(121.5, 124.5, 157.5, 300.0, 334.5), (343.0, 346.0, 379.0, 521.0, X1)]
g = Grid("tasks", [X0, LAB] + sorted({x for t in T for x in t}), [2000, 6040])
label(g, 0, 2, "추진과제")
tasks = [("내부", "재난관리 체계 강화",
          [[S("① ", BODY, True), S("業 맞춤형 6대 위기 유형 재정립으로 대응력 제고")],
           [S("② ", BODY, True), S("단절 없는 재난관리 全 주기"), S("(4단계)", SMALL), S(" 역량 강화")],
           [S("③ ", BODY, True), S("재난복구"), S("(DR)", SMALL), S(" 체계 강화를 통한 업무 연속성 확보")]]),
         ("외부", "재난안전망 구축",
          [[S("④ ", BODY, True), S("국민 공공서비스 분야 사이버안전 컨트롤타워 역할 주도")],
           [S("⑤ ", BODY, True), S("‘에너지·물·철도’ 국가 기반시설 사이버 침해 원천 차단")],
           [S("⑥ ", BODY, True), S("전선 단선 검출 기술로 대형 화재 및 감전 재난 예방")]])]
head_fill = "#B4B4B4"
for (a, b, c, d, e), (tag, title, items) in zip(T, tasks):
    g.put(a, b, 0, 1, [], frame(head_fill, top="soft", left="soft"))
    g.put(b, c, 0, 1, tag, frame("#3C3C3C"), size=1100, bold=True, color=WHITE, line=1300)
    g.put(c, d, 0, 1, title, frame(head_fill, top="soft"), size=1100, line=1300)
    g.put(d, e, 0, 1, [], frame(head_fill, top="soft", right="soft"))
    g.put(a, e, 1, 2, items, frame(bottom="soft", left="soft", right="soft"), align="LEFT", line=1800)
block(g, 352.8)

# 성과지표: two outlined boxes
g = Grid("kpi", [X0, LAB, 121.2, 334.8, 341.0, X1], [2300])
label(g, 0, 1, "성과지표")
box = frame("#F4F4F4", top="mid", bottom="mid", left="mid", right="mid")
g.put(121.2, 334.8, 0, 1, "재난대응 모의훈련(회)", box, size=1100)
g.put(341.0, X1, 0, 1, "사이버 보안사고(건)", box, size=1100)
block(g, 442.2)

# Brace gathering both columns into the 재난관리체계 cycle
g = Grid("brace", [X0, 137.0, 537.8, X1], [700, 1100])
g.put(137.0, 537.8, 0, 1, [], frame(bottom="mid"))
g.put(137.0, 537.8, 1, 2, "▼", size=800, color="#9A9A9A", line=900)
block(g, 467.6)

def sb(*parts):
    return bullet(*parts, size=1000)


# 재난관리체계: 예방 → 대비 ↓ 대응 → 복구 ↑ cycle of four boxes
A, B = (121.2, 162.0, 290.5, 331.8), (343.0, 383.8, 512.0, X1)
xs = [X0, LAB] + list(A) + list(B)
hs = [480, 2000, 6080, 1120, 600, 2000, 6000]   # y 490.2 .. 673.0
g = Grid("system", xs, hs)
label(g, 0, 7, ["재      난", "관리체계"])
boxes = [(A, 0, "예 방", "선제적 위험 요인 제거", "#E4E4E4", [
              sb("CEO 주도 중대시민재해 이행점검 확대", ("(연 2회→7회)", SMALL)),
              sb("기상이변 대비 사옥 취약 시설물 선제적 안전진단 강화"),
              sb("재난 대비 동영상 일일 방영으로 Safe KDN 문화 확산")]),
         (B, 0, "대 비", "재난 관리체계 확립", "#CCCCCC", [
              sb("「재난관리 업무 지침」 및 「위기 대응 매뉴얼」 제·개정 및 전파"),
              sb("본사 비상 대피용 ‘재난 구급함’ 전층 확대 설치", ("(18대→54대)", SMALL)),
              sb("실시간 재난대응 기반 위기재난관리시스템", ("(CDS)", SMALL), " 고도화")]),
         (A, 4, "복 구", "신속한 정상화 및 환류", "#BEBEBE", [
              sb("소방서와 재난 대응·복구 실시간 공조 체계 구축 ", ("(MOU체결)", SMALL)),
              sb("新 매뉴얼 기반 재난 대비 실전형 모의훈련 ", ("(연 22회)", SMALL)),
              sb("한전과 ‘재난 핫라인’ 구축, 전력으로 ICT 설비 긴급 복구 체계 완비")]),
         (B, 4, "대 응", "현장 연계 대응역량 강화", "#C0C0C0", [
              sb("국가 위기경보 연계 ‘비상발령체계’일원화 ", ("(3단계→4단계)", SMALL)),
              sb("「자연재난 대응 특화 행동 가이드」 최초 제정 및 전파"),
              sb("해외 재난 대응 ‘해외 인력 24H 7종 케어 서비스’ 운영")])]
for (a, b, c, e), r, tag, title, fill, items in boxes:
    g.put(a, e, r, r + 1, [], frame(top="mid", left="mid", right="mid"))
    g.put(a, b, r + 1, r + 2, tag, frame("#7A7A7A", left="mid"), size=1150, bold=True, color=WHITE, line=1300)
    g.put(b, c, r + 1, r + 2, title, frame(fill), size=1150, line=1300)
    g.put(c, e, r + 1, r + 2, [], frame(fill, right="mid"))
    g.put(a, e, r + 2, r + 3, items, frame(left="mid", right="mid", bottom="mid"), align="LEFT", line=1800)
g.put(331.8, 343.0, 0, 3, "▶", size=1000, color=ARROW, fit=False)
g.put(331.8, 343.0, 4, 7, "◀", size=1000, color=ARROW, fit=False)
g.put(A[0], A[3], 3, 4, "▲", size=800, color=ARROW, line=900)
g.put(B[0], B[3], 3, 4, "▼", size=800, color=ARROW, line=900)
block(g, 490.2)

# 재난관리 인프라: four tabs, 조직 list + three value charts, result row
C = [(121.2, 227.0), (230.8, 336.5), (340.2, 446.0), (449.5, X1)]
ORG = [(121.2, 123.5), (123.5, 143.5), (143.5, 147.0), (147.0, 227.0)]
CH = [(230.8, 266.0, 296.0, 336.5), (340.2, 376.0, 405.0, 446.0), (449.5, 483.0, 508.0, X1)]
xs = sorted(set([X0, LAB] + [x for c in C for x in c] + [x for c in ORG for x in c] + [x for c in CH for x in c]))
hs = [1950, 500, 1500, 1300, 1400, 1400, 1300, 2300]    # y 683.0 .. 799.5: tabs, body rows 1-6, result
g = Grid("infra", xs, hs)
label(g, 0, 8, ["재난관리", "인 프 라"])
tab = frame("#F0F0F0", top="mid", left="mid", right="mid", bottom="soft")
for (a, e), name in zip(C, ("조 직", "인 력", "교육 · 훈련", "예 산")):
    g.put(a, e, 0, 1, name, tab, size=1100, line=1300)
pill = frame("#D2D2D2")
tag = frame("#3C3C3C")
# 조직: tagged lines (rows 2, 4 and 5)
org = {(2, 1): ("전 담", "pill"), (2, 3): ([[S("비상재난부"), S("(23명)", SMALL)]], "text"),
       (4, 1): ("현 장", "pill"), (4, 3): ([[S("본사, 사업소, 부서별")]], "text"),
       (5, 3): ([[S("재난담당"), S("(58명)", SMALL)]], "text")}
for r in range(1, 7):
    for col, (a, e) in enumerate(ORG):
        content, kind = org.get((r, col), ([], None))
        right = dict(right="dot") if col == 3 else {}
        if kind == "pill":
            g.put(a, e, r, r + 1, content, pill, size=950, line=1100, ratio=85, fit=False)
            tight(g, a, r, 0, 0)
        else:
            g.put(a, e, r, r + 1, content, frame(**right), align="LEFT", line=1200)
# charts: rise tags (dark) and the printed values; columns '24 bar | tag | '25 bar
charts = [{(2, 1): ("16%↑", "tag"), (2, 2): ("81명", "b"), (3, 0): ("70명", "r")},
          {(2, 1): ("29%↑", "tag"), (2, 2): ("411명", "b"), (3, 0): ("318명", "r"), (4, 2): ("22회", "r"),
           (5, 0): ("16회", "r"), (5, 1): ("38%↑", "tag")},
          {(2, 1): ("5%↑", "tag"), (2, 2): ("12억원", "b"), (3, 0): ("11억원", "r")}]
for k, ((a, b, c, e), values) in enumerate(zip(CH, charts)):
    cols = [(a, b), (b, c), (c, e)]
    values[6, 0] = ("’24년", "year")
    values[6, 2] = ("’25년", "year-b")
    for r in range(1, 7):
        for col, (x0, x1) in enumerate(cols):
            edges = {}
            if col == 2 and k < 2:
                edges["right"] = "dot"
            if r == 5:
                edges["bottom"] = "soft"
            text, kind = values.get((r, col), ([], None))
            if kind == "tag":
                g.put(x0, x1, r, r + 1, text, frame("#3C3C3C", **edges), size=900, bold=True, color=WHITE,
                      line=1050)
            elif kind and kind.startswith("year"):
                g.put(x0, x1, r, r + 1, text, frame(**edges), size=850, bold=kind == "year-b", line=950)
            else:
                g.put(x0, x1, r, r + 1, text, frame(**edges), size=1050, bold=kind == "b", line=1100)
# result row
g.put(121.2, 123.5, 7, 8, [], frame(LABEL))
g.put(123.5, 143.5, 7, 8, "개선", frame(WHITE, top="soft", bottom="soft", left="soft", right="soft"), size=950,
      line=1100, ratio=85, fit=False)
tight(g, 123.5, 7, 0, 0)
g.put(143.5, 227.0, 7, 8, "비상·재난 일원화", frame(LABEL, right="dot"), size=1100, line=1300)
for (a, e), text in zip(C[1:], ("재난인력 11명 증가", "교육 93명·훈련 6회 증가", "재난예산 약 0.6억원 증가")):
    g.put(a, e, 7, 8, text, frame(LABEL, **({"right": "dot"} if e != X1 else {})), size=1100, line=1300)
block(g, 683.0)

kit.finish(target, end=802.0)
