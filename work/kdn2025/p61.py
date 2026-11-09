"""Rebuild KDN 2025 report PDF page 61 (second PDF local page 11, printed page 38) as editable HWPX.

Usage: python3 work/kdn2025/p61.py <report2.pdf> <out.hwpx> [--page 11]

안전 및 재난관리 section 2 "[안전보건경영] 안전관리 주체를 최고 경영층으로 격상 ...". Built with
the shared kit (one flat table per horizontal band on a grid of PDF x edges).

Text layer: section title, 가./나. headings, 기관장 의지 quote, the 중대재해통합관리시스템 boxes,
the □ headings, the three training cards and 주요성과. Image only, read from 4-7x renders and
typed: the 안전 불감 -> 안전 쇄신 comparison, the four 기관장 주도 quadrants with their 신규 /
개선 / 확대 tags and the "기관장 결단! ..." band (y 154-508), the section number band, the □
marks and the "Best Practice" badge (trophy icon omitted). Photos (system screenshot, tower
rescue, KBS broadcast) are empty photo cells; the screenshot's text-layer word "중대재해통합관리"
(4.8 pt) stays in its photo cell. Quadrant icons, the funnel and the decision chevron are
omitted; list circles -> "○", the ⇆ icon -> "↔". Kept as printed: the double space in
"중대재해  대응능력" and the space in "추가 ·위험".
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kit  # noqa: E402
from kit import Layout, recipe_inputs  # noqa: E402

source, target = recipe_inputs(11, "안전관리 주체를 최고 경영층으로 격상")
L = Layout(top=3200)
kit.setup(source, L)
from kit import *  # noqa: E402,F401,F403  helpers and presets bound to this page

LIGHT, DARKTAG = "#E4E4E4", "#4A4A4A"
BOX = frame(WHITE, top="soft", bottom="soft", left="soft", right="soft")


def m(text, size=1030, bold=False, color=INK, small=0.82):
    """Typed run list: {..} = smaller run (parenthetical counts)."""
    runs = []
    for part in re.split(r"(\{[^}]*\})", text):
        if part:
            small_part = part[0] == "{"
            runs.append((part[1:-1] if small_part else part,
                         int(round(size * (small if small_part else 1) / 10)) * 10, bold, color))
    return runs


def hang(lines, base):
    """Lines keep their PDF indent: spaces for the x offset and for the line's own leading blanks."""
    out = []
    for line in lines:
        runs = runs_of(line)
        size = runs[0][1] / 100
        raw = "".join(s["text"] for s in line["spans"])
        offset = line["bbox"][0] - base + (len(raw) - len(raw.lstrip(" "))) * 0.29 * size
        n = max(0, round(offset / (0.29 * size)))
        out.append([(" " * n, runs[0][1], False, INK)] + runs if n else runs)
    return out


# ---------------------------------------------------------------------------
# Page chrome (odd page): side tab and footer float; running head over a rule.
# ---------------------------------------------------------------------------
L.add_table([[cell(0, 3350, 1680, [para([("01", 1380, True, WHITE)], "CENTER")[0]], dark)],
             [cell(0, 3350, 5960, [para([(ch, 950, True, INK)], "CENTER", 1160)[0] for ch in "경영관리"], gray2)]],
            floating=(57800, 15000))
foot = [(text, size, False, INK) for text, size in (
    (line1(450, 455, 818, 822)["text"], 790), ("    ", 790), (line1(540, 546, 816, 820)["text"], 1090))]
L.add_table([[cell(0, W, 1500, [para(foot, "RIGHT", 1300)[0]])]], floating=(5660, 81550))

g = Grid("head", [X0, 399.7, X1], [1680])
g.put(X0, 399.7, 0, 1, [], frame(bottom="soft"))
g.put(399.7, X1, 0, 1, [line1(400, 410, 35, 40)], align="RIGHT")
block(g, 32.0)

g = Grid("section", [X0, 85.5, X1], [2300])
g.put(X0, 85.5, 0, 1, [runs_of(line1(64, 70, 72, 78), WHITE)], frame("#606060"), line=1850)
g.put(85.5, X1, 0, 1, [line1(90, 95, 73, 78)], frame(LIGHT), align="LEFT", line=1700)
block(g, 71.0)

g = Grid("title-ga", [X0, X1], [1780])
g.put(X0, X1, 0, 1, [line1(55, 60, 100, 105)], align="LEFT", line=1600)
block(g, 99.8)

g = Grid("will", [X0, 122.0, X1], [2500])
g.put(X0, 122.0, 0, 1, [line1(60, 70, 127, 132)], frame(WHITE, top="mid", bottom="mid", left="mid", right="mid"))
g.put(122.0, X1, 0, 1, [line1(130, 140, 127, 132)], frame(LIGHT))
block(g, 123.2)

# ---------------------------------------------------------------------------
# 안전 불감 -> 안전 쇄신 (image in the PDF; text read from a 4-7x render)
# ---------------------------------------------------------------------------
xs = [X0, 86.0, 111.5, 291.0, 306.5, 360.0, X1]
g = Grid("shift", xs, [2300, 1800, 1800, 1800, 1800])
g.put(X0, 111.5, 0, 1, "안전 불감", frame("#787878"), size=1150, bold=True, color=WHITE)
g.put(111.5, 291.0, 0, 1, "업무성과 중심의 수동적 안전 의식", frame(LIGHT), size=1100)
g.put(306.5, 360.0, 0, 1, "안전 쇄신", frame(DARKTAG, top="strong", left="strong"), size=1150, bold=True,
      color=WHITE)
g.put(360.0, X1, 0, 1, "기관장 주도의 全주기 집중 안전관리로 전환",
      frame(top="strong", right="strong", bottom="soft"), size=1150, bold=True)
before = (("소   통", "안전정보 공유 미흡, 위험징후 파악·현장대응 지연"),
          ("위   협", "현장 산재, 보여주기식 안전, 사각지대 관리 부재"),
          ("협력사", "안전관리체계 기초체력·인력·환경여건 열악"),
          ("실행력", "안전예산을 비용으로 인식, 중대재해  대응능력 부족"))
after = ("· 일단위 안전현황 파악, 적극 의견 청취, 안전수준 객관화",
         "· 現 안전관리 준수 실태와 위험요인 기관장 참여 진단",
         "· 종사자 개념 확장, 안전전문가 활용, 협력사 안전 동기 강화",
         "· 법정 · 관행적 수준을 넘어 직원 · 협력사 지원 예산 대폭 확대")
hatched = dict(hatch="#DEDEDE")
for r, ((tag, text), right) in enumerate(zip(before, after), 1):
    last = r == 4
    g.put(X0, 86.0, r, r + 1, tag, BOX, size=1000)
    g.put(86.0, 291.0, r, r + 1, [m(text, 1080)], frame(bottom="dot"), align="LEFT")
    g.put(306.5, X1, r, r + 1, [m(right, 1060)],
          frame("#F0F0F0", left="strong", right="strong", bottom="strong" if last else "dot", **hatched),
          align="LEFT")
g.put(291.0, 306.5, 1, 5, "▶", size=1300, color="#7A7A7A")
block(g, 159.5)

# Four quadrants: header band (icon omitted) and four ○ items with a 신규 / 개선 / 확대 tag each.
xs = [X0, 279.5, 300.5, 303.5, 527.5, 549.0, X1]
quads = (
    ("공유체계 고도화로 안전정보 인지속도 향상", (
        ("기관장 일일 전사 안전현황 모니터링 체계 최초 가동", "신규"),
        ("안전회의체 의장을 기관장으로, 노동자 의견 현장 수용", "개선"),
        ("(사내) ‘안전혁신 TF’ 구성, 구조적 취약요인 진단", "신규"),
        ("(사외) 외부전문가 ‘안전자문단’ 운영, 객관적 시각 진단", "신규"))),
    ("기관장 현장점검 확대 및 사각지대 집중관리", (
        ("기관장 현장 안전점검, 위해·위험요인 개선 조치{(38건)}", "개선"),
        ("불시점검 확대, 무관용 원칙·업체 계약 해지 지시", "개선"),
        ("고소작업차 14m 탑승, 전력구 밀폐공간 등 직접 점검", "신규"),
        ("안전사각지대 오지·기피사업장 노동자 고위험군 관리", "신규"))),
    ("선제적 안전투자 확대로 위험요인 신속 개선", (
        ("폭염·한파 취약시기 등 안전예산 추가 집행{(5.2억원)}", "개선"),
        ("협력사 ISO 국제인증 취득비용까지 全과정 지원{(2개社)}", "신규"),
        ("건설공사 설계부터 안전비용 6억원 최초 반영, 비작업일수 115일↑", "신규"),
        ("최초 초고위험 철탑작업 중대재해 대응 실전 훈련", "개선"))),
    ("협력사 포함 전반적 안전관리 수준진단 · 개선", (
        ("안전전문기관 합동 원점부터 전면 안전 재진단{(3개분야)}", "신규"),
        ("고위험작업 안전전문가 추가 ·위험 진단강화{(철탑, 건설)}", "신규"),
        ("맞춤형 특별안전교육, 협력사 안전보건체계진단{(11개社)}", "확대"),
        ("안전활동·안전관리 능력 최우수 건설협력사 포상{(1개社)}", "신규"))))
NEW, MARK = frame("#3C3C3C"), frame(WHITE, top="mid", bottom="mid", left="mid", right="mid")


def quad_band(name, top, pair, upper):
    g = Grid(name, xs, [1900, 380 if upper else 640, 1800, 1800, 1800, 1800])
    hr, sr = (0, 1) if upper else (0, 1)
    for (a, t, e), (head, items) in zip(((X0, 279.5, 300.5), (303.5, 527.5, 549.0)), pair):
        band = frame("#D8D8D8", top="strong") if upper else frame("#CDCDCD", bottom="strong")
        g.put(a, X1 if a > 300 else 300.5, hr, hr + 1, head, band, size=1100)
        for r, (text, tag) in enumerate(items, 2):
            g.put(a, t, r, r + 1, [[("○ ", 800, False, "#7A7A7A")] + m(text, 970 if len(text) > 36 else 1030)], frame(bottom="dot"), align="LEFT")
            g.put(t, e, r, r + 1, tag, NEW if tag == "신규" else MARK, size=950, bold=tag == "신규",
                  color=WHITE if tag == "신규" else INK, line=1050)
    block(g, top)


quad_band("quads-top", 277.2, quads[:2], True)
quad_band("quads-bottom", 384.5, quads[2:], False)

g = Grid("decision", [X0, X1], [2300])
g.put(X0, X1, 0, 1, "기관장 결단! 위험 인지에서 현장 통제 · 예산 집행 · 훈련 검증까지 ‘실행 성과’로 입증",
      frame("#6E6E6E", hatch="#7C7C7C"), size=1200, bold=True, color=WHITE)
block(g, 485.5)

# ---------------------------------------------------------------------------
# 나. 중대재해통합관리시스템 (text layer; screenshot -> photo cell)
# ---------------------------------------------------------------------------
g = Grid("title-na", [X0, X1], [1780])
g.put(X0, X1, 0, 1, [line1(55, 60, 518, 523)], align="LEFT", line=1600)
block(g, 517.5)

g = Grid("heading-1", [X0, X1], [1680])
g.put(X0, X1, 0, 1, [[("□ ", 1350, False, INK)] + runs_of(line1(68, 75, 539, 544))], align="LEFT", line=1500)
block(g, 539.0)

xs = [X0, 141.0, 226.0, 240.0, X1]
g = Grid("system", xs, [2200, 2200, 2200, 2250])
head = frame("#D6D6D6", top="mid", left="mid", right="mid")
g.put(X0, 226.0, 0, 1, [line1(80, 90, 563, 568)], head)
g.put(240.0, X1, 0, 1, [line1(260, 270, 563, 568)], head)
shot = line1(85, 90, 590, 595)
g.put(X0, 141.0, 1, 4, [runs_of(shot)], frame("#E4E4E4", left="mid", bottom="mid"), size=480)
for r, y in enumerate((587, 609, 632), 1):
    g.put(141.0, 226.0, r, r + 1, [line1(140, 145, y - 2, y + 3)],
          frame("#EDEDED", right="mid", bottom="mid" if r == 3 else "soft"))
    g.put(240.0, X1, r, r + 1, [line1(245, 250, y - 2, y + 3)],
          frame(left="mid", right="mid", bottom="mid" if r == 3 else "dot"), align="LEFT")
g.put(226.0, 240.0, 1, 4, "↔", size=1100, color="#9A9A9A")
block(g, 561.0)

# □ heading with the "Best Practice" badge (image, typed; trophy omitted)
g = Grid("heading-2", [X0, 486.5, X1], [1680])
g.put(X0, 486.5, 0, 1, [[("□ ", 1350, False, INK)] + runs_of(line1(68, 75, 657, 662))], align="LEFT", line=1500)
g.put(486.5, X1, 0, 1, "Best Practice", frame("#3C3C3C"), size=850, bold=True, color=WHITE, line=1000)
block(g, 657.8)

# Three cards: boxed tag + title, body bullets; tower and broadcast photos as photo cells.
xs = [X0, 85.0, 202.0, 204.0, 247.0, 339.5, 392.0, 394.0, 397.0, 427.5, 500.5, X1]
g = Grid("cards", xs, [2200, 1550, 3200, 1950])
side = dict(left="mid", right="mid")
for a, t, e, tx in ((X0, 85.0, 202.0, 64.0), (204.0, 247.0, 394.0, 226.0), (397.0, 427.5, X1, 406.0)):
    head = line1(tx, tx + 6, 682, 687)
    g.put(a, t, 0, 1, [runs_of(head, x1=tx + 18)], frame(LIGHT, top="mid", left="mid"), align="RIGHT")
    g.put(t, e, 0, 1, [strip_runs(runs_of(head, x0=tx + 18))], frame(LIGHT, top="mid", right="mid"), align="LEFT")
body = frame(**side, bottom="mid")
g.put(X0, 202.0, 1, 4, hang(lines_in(60, 75, 700, 768), 62.5), body, align="LEFT", line=1540)
g.put(204.0, 394.0, 1, 2, hang(lines_in(205, 215, 702, 708), 209.9), frame(**side), align="LEFT")
g.put(204.0, 339.5, 2, 4, hang(lines_in(205, 215, 716, 768), 209.9), frame(left="mid", bottom="mid"),
      align="LEFT", line=1540)
g.put(339.5, 392.0, 2, 4, [], photo)
g.put(392.0, 394.0, 2, 4, [], frame(right="mid", bottom="mid"))
g.put(397.0, X1, 1, 2, hang(lines_in(400, 410, 702, 708), 402.7), frame(**side), align="LEFT")
g.put(397.0, 500.5, 2, 3, hang(lines_in(400, 415, 716, 745), 402.7), frame(left="mid"), align="LEFT",
      line=1500)
g.put(500.5, X1, 2, 3, [], frame("#E4E4E4", top="mid", left="mid", right="mid"))
g.put(397.0, 500.5, 3, 4, hang(lines_in(400, 415, 747, 760), 402.7), frame(left="mid", bottom="mid"),
      align="LEFT")
g.put(500.5, X1, 3, 4, [line1(500, 505, 749, 755)], frame("#D6D6D6", right="mid", bottom="mid", left="mid"))
block(g, 679.0)

# 주요성과
g = Grid("result", [X0, 112.5, X1], [2600])
g.put(X0, 112.5, 0, 1, [runs_of(line1(64, 70, 781, 787), WHITE)], frame("#6A6A6A", top="mid", bottom="mid", left="mid"))
g.put(112.5, X1, 0, 1, [line1(115, 120, 781, 787)], frame(top="mid", bottom="mid", right="mid"), align="LEFT")
block(g, 776.0)

kit.finish(target, end=802.0)
