"""Rebuild KDN 2025 report page 150 (third PDF local page 50, printed page 105) as editable HWPX.

Usage: python3 work/kdn2025/p150.py <report3.pdf> <out.hwpx> [--page 50]

"Ⅲ. 세부 평가내용별 추진실적" opening page of the 보수 및 복리후생 indicator (same page type as
p60 / p63 / p70 / p88). Title, 평가내용 01 band, both section bands, the 가./나. headings, the two
compliance tables and the 주요성과 box are in the PDF text layer. The 6대 추진과제 diagram
(y 176-368: '25년 환경분석, 핵심POINT, 추진목표, 추진방향, 6대 추진과제) is an image: its text was
read from 4x-5x renders and typed into editable cells on the diagram's own grid (label column |
content). Built with the shared kit.

Tables: cells on the PDF's vector rules; one PDF text line that runs across cells (item | 지침 |
결과 | 준수 여부) is split by span x. The spaced items (인 상 률, 근 무 수 당 ...) are one span per
row in the PDF and are set with distributed alignment over the same extent. The dark outline
around 운영 결과 / 준수 여부 is drawn with strong cell borders.

Glyph choices for image-only fragments: the dark numbered discs -> ① - ⑥, the gray arrow chain in
핵심POINT -> "→ → → →", middle dots in typed text -> "·". The 평가내용 chip's check mark is dropped.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kit  # noqa: E402
from kit import Layout, recipe_inputs  # noqa: E402

source, target = recipe_inputs(50, "국민 눈높이의 ‘원칙’과 직원이 체감하는")
L = Layout(top=3100)
kit.setup(source, L)
from kit import *  # noqa: E402,F401,F403  helpers and presets bound to this page

HEAD, HEAD_DARK, SHADE = "#D8D8D8", "#7F7F7F", "#ECECEC"
TAG = "#787878"
TEXT = 1050          # diagram body text (the image's font is narrower than KoPub)


def R(text, size=TEXT, bold=False, color=INK):
    return [(text, size, bold, color)]


def margins(g, x0, r0, left, right):
    key = (r0, g.xs.index(to_x(x0)))
    g.items[key] = g.items[key][:7] + (dict(left=left, right=right),)


def cell_runs(x0, x1, y0, y1):
    """Runs of every PDF line in y0..y1 with a span starting in x0..x1, cut to that x range."""
    out = []
    for line in sorted(LINES, key=lambda l: (l["bbox"][1], l["bbox"][0])):
        if y0 <= line["bbox"][1] < y1 and any(x0 <= s["bbox"][0] < x1 and s["text"].strip() for s in line["spans"]):
            out.append(runs_of(line, x0=x0, x1=x1))
    return out


def joined(x0, x1, y0, y1):
    """One paragraph from all spans in the box (the PDF sets 인 / 상 / 률 as separate lines)."""
    spans = sorted((s for l in LINES if y0 <= l["bbox"][1] < y1 for s in l["spans"]
                    if x0 <= s["bbox"][0] < x1 and s["text"].strip()), key=lambda s: s["bbox"][0])
    return runs_of(dict(spans=spans))


def indented(x0, x1, y0, y1, base):
    """Lines of a cell; continuation lines keep the PDF indent as leading spaces."""
    out = []
    for line in lines_in(x0, x1, y0, y1):
        runs = runs_of(line)
        size = runs[0][1] / 100
        raw = "".join(s["text"] for s in line["spans"])
        offset = line["bbox"][0] - base + (len(raw) - len(raw.lstrip(" "))) * 0.29 * size
        n = max(0, round(offset / (0.29 * size)))
        out.append([(" " * n, runs[0][1], False, INK)] + runs if n else runs)
    return out


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
g.put(X0, X1, 0, 1, [line1(195, 205, 69, 74)])
block(g, 68.5)

# 평가내용 01 band: chip (image, typed) in the corner, hatched one-line title.
g = Grid("band", [X0, 124.0, X1], [1950, 920])
g.put(X0, 124.0, 0, 1, "평가내용 01", frame("#565656", top="strong"), size=970, bold=True, color=WHITE, ratio=80)
g.put(X0, 124.0, 1, 2, [], frame("#E9E9E9", bottom="soft", left="soft", hatch="#DADADA"))
g.put(124.0, X1, 0, 2, [line1(125, 130, 110, 116)], frame("#E9E9E9", top="strong", bottom="soft", right="soft",
                                                            hatch="#DADADA"), align="LEFT", line=1480)
block(g, 105.5)


def section(name, y, top):
    g = Grid(name, [X0, 85.5, X1], [2300])
    g.put(X0, 85.5, 0, 1, [runs_of(line1(64, 70, y - 2, y + 3), WHITE)], frame("#848484"), line=1800)
    g.put(85.5, X1, 0, 1, [line1(90, 95, y - 1, y + 4)], frame("#E6E6E6"), align="LEFT", line=1700)
    block(g, top)


section("sec1", 149.0, 146.1)

# ---------------------------------------------------------------------------
# 6대 추진과제 diagram (one image in the PDF; text typed from 4x-5x renders)
# ---------------------------------------------------------------------------
LS, LB, C0 = 59.6, 111.5, 117.0       # label strip | label | content start


def label(g, r0, r1, lines, strip, fill="#E4E4E4", color=INK, bold=False, size=1090):
    g.put(X0, LS, r0, r1, [], frame(strip))
    g.put(LS, LB, r0, r1, [R(t, size, bold, color) for t in lines], frame(fill), line=1350)
    margins(g, LS, r0, 0, 200)


# '25년 환경분석: 외부 | 내부 boxes, a gray head and two tagged findings each (dotted separator).
xs = [X0, LS, LB, C0, 120.0, 153.5, 332.0, 337.3, 342.0, 374.3, X1]
g = Grid("env", xs, [1720, 310, 1270, 380, 370, 1280, 345])
label(g, 0, 7, ["’25년", "환경분석"], "#D2D2D2")
for a, b, c, e, head, rows in (
        (C0, 120.0, 153.5, 332.0, "외      부", (("국민여론", "강화된 국민 눈높이에 맞춘 보상체계 운영 요구"),
                                                ("정부관점", "통상임금 변경판례 대응 및 정부지침 준수 요구"))),
        (337.3, 342.0, 374.3, X1, "내      부", (("직원관점", "통상임금 인상 적용 및 복지제도 확충 요구"),
                                               ("회사관점", "임금단체교섭 타결 및 직원 만족도 제고 필요")))):
    g.put(a, e, 0, 1, head, frame("#A8A8A8", top="soft", left="soft", right="soft"), size=1090, bold=True)
    g.put(a, b, 1, 7, [], frame(left="soft", bottom="soft"))
    for k, (tag, text) in enumerate(rows):
        r = 1 + 3 * k
        edge = "dot" if k == 0 else "soft"
        g.put(b, c, r, r + 1, [], "1" if k == 0 else frame())
        g.put(b, c, r + 1, r + 2, tag, frame(TAG), size=950, color=WHITE, line=1100)
        g.put(b, c, r + 2, r + 3, [], frame(bottom=edge))
        g.put(c, e, r, r + 3, [R(text)], frame(bottom=edge, right="soft"), align="LEFT", line=1300)
        margins(g, c, r, 300, 100)
block(g, 176.0)

# 핵심POINT: '24년 (outlined tag) -> arrow chain -> '25년 (dark tag) bold goal.
xs = [X0, LS, LB, C0, 120.0, 153.5, 290.0, 338.0, 340.8, 374.5, X1]
g = Grid("point", xs, [480, 1300, 490])
label(g, 0, 3, ["핵심POINT"], "#CCCCCC")
box = dict(top="soft", bottom="soft")
g.put(C0, 120.0, 0, 3, [], frame(left="soft", **box))
g.put(120.0, 153.5, 0, 1, [], frame(top="soft"))
g.put(120.0, 153.5, 1, 2, "’24년", frame(WHITE, top="mid", bottom="mid", left="mid", right="mid"), size=950,
      line=1100)
g.put(120.0, 153.5, 2, 3, [], frame(bottom="soft"))
g.put(153.5, 290.0, 0, 3, [R("정부지침 준수로 방만경영 방지", 1090)], frame(**box), align="LEFT", line=1300)
g.put(290.0, 338.0, 0, 3, "→ → → →", frame(**box), size=900, bold=True, color="#A8A8A8", line=1100)
g.put(338.0, 340.8, 0, 3, [], frame(**box))
g.put(340.8, 374.5, 0, 1, [], frame(top="soft"))
g.put(340.8, 374.5, 1, 2, "’25년", frame(TAG), size=950, color=WHITE, line=1100)
g.put(340.8, 374.5, 2, 3, [], frame(bottom="soft"))
g.put(374.5, X1, 0, 3, [R("통상임금 변경판례 대응 및 국민신뢰 확보", 1090, True)], frame(right="soft", **box),
      align="LEFT", line=1300)
margins(g, 374.5, 0, 300, 100)
block(g, 238.6)

g = Grid("goal", [X0, LS, LB, C0, X1], [2275])
label(g, 0, 1, ["추진목표"], "#C0C0C0")
g.put(C0, X1, 0, 1, [R("이해관계자(정부·국민·경영진·노조·직원)가 모두 만족하는 보수 및 복리후생 제도 운영", 1090, True)],
      frame("#EFEFEF", hatch="#DCDCDC"), line=1300)
block(g, 268.0)

B3 = ((C0, 260.0), (264.3, 407.7), (412.0, X1))
xs = [X0, LS, LB] + [x for pair in B3 for x in pair]
g = Grid("direction", xs, [2275])
label(g, 0, 1, ["추진방향"], "#C0C0C0")
for (a, e), text in zip(B3, ("원칙 기반의 투명한 예산 운영", "직원 니즈 중심의 비금전 복지 활성화",
                             "합리적 조율을 통한 보수체계 운영")):
    g.put(a, e, 0, 1, [R(text, 1090, True)], frame("#C4C4C4"), line=1300)
block(g, 296.75)

g = Grid("tasks", xs, [4275])
label(g, 0, 1, ["6대", "추진과제"], "#606060", fill=TAG, color=WHITE, bold=True, size=1150)
tasks = (("① 예산·혁신 정부지침 100% 이행", "② 3선통제 및 솔루션 기반 지출 절감"),
         ("③ 新모델로 수요자 참여주도 복지 설계", "④ 만족도 조사 고도화를 통한 실효성 제고"),
         ("⑤ 통상임금 리스크 선제적 대응", "⑥ 노사합의 기반 합리적 보수체계 운영"))
for (a, e), lines in zip(B3, tasks):
    g.put(a, e, 0, 1, [R(t, 1000) for t in lines], frame(top="soft", bottom="soft", left="soft", right="soft"),
          align="LEFT", line=1650)
    margins(g, a, 0, 250, 80)
block(g, 325.75)

section("sec2", 387.9, 385.0)

g = Grid("title-ga", [X0, X1], [1750])
g.put(X0, X1, 0, 1, [line1(55, 60, 414, 420)], align="LEFT", line=1550)
block(g, 414.5)

# ---------------------------------------------------------------------------
# 가. 예산운용: 주요 항목 (group | item) | 정부 지침 내용 | 운영 결과 | 준수 여부
# ---------------------------------------------------------------------------
xs = [X0, 102.1, 161.6, 342.9, 513.0, X1]
ys = [455.7, 474.7, 493.6, 512.5, 531.5, 550.4, 569.3, 588.2]
g = Grid("budget", xs, [1840] + [int(round((b - a) * 100)) for a, b in zip(ys, ys[1:])])


def heads(g, cols, y):
    """Header row: light cells, then the two dark cells inside the strong outline."""
    *light, res, ok = cols
    for a, e in light:
        g.put(a, e, 0, 1, cell_runs(a, e, y - 1, y + 3), frame(HEAD, top="mid", right="soft"))
    g.put(*res, 0, 1, [[(t, s, b, WHITE) for t, s, b, _ in r] for r in cell_runs(*res, y - 1, y + 3)],
          frame(HEAD_DARK, top="strong", left="strong", right="soft"))
    g.put(*ok, 0, 1, [[(t, s, b, WHITE) for t, s, b, _ in r] for r in cell_runs(*ok, y - 1, y + 3)],
          frame(HEAD_DARK, top="strong", right="strong"), fit=False, ratio=84)
    margins(g, ok[0], 0, 60, 60)


def verdict(g, x0, r0, r1, y0, y1, last):
    g.put(x0, X1, r0, r1, cell_runs(x0, X1, y0, y1), frame(bottom="strong" if last else "soft", right="strong"),
          fit=False, ratio=84, line=1350)
    margins(g, x0, r0, 60, 60)


heads(g, [(X0, 161.6), (161.6, 342.9), (342.9, 513.0), (513.0, X1)], 441.1)
for k, (y0, y1) in enumerate(zip(ys, ys[1:])):
    r, last = k + 1, k == len(ys) - 2
    edge = "mid" if last else "soft"
    item = joined(102.1, 161.6, y0, y1)
    small = item[0][1] < 1000                       # 휴･정직･징계자 is 9.7 pt
    g.put(102.1, 161.6, r, r + 1, [item], frame(SHADE, bottom=edge, left="soft"), align="DISTRIBUTE",
          fit=False, ratio=80 if small else 86)
    margins(g, 102.1, r, 150 if small else 490, 150 if small else 500)
    g.put(161.6, 342.9, r, r + 1, cell_runs(161.6, 342.9, y0, y1), frame(bottom=edge), align="LEFT")
    g.put(342.9, 513.0, r, r + 1, cell_runs(342.9, 513.0, y0, y1),
          frame(bottom="strong" if last else "soft", left="strong", right="soft"), align="LEFT")
for r0, r1 in ((1, 5), (5, 8)):
    y0, y1 = ys[r0 - 1], ys[r1 - 1]
    g.put(X0, 102.1, r0, r1, [runs_of(l) for l in lines_in(56, 102, y0, y1)],
          frame(SHADE, bottom="mid" if r1 == 8 else "soft"), line=1450)
    verdict(g, 513.0, r0, r1, y0, y1, r1 == 8)
block(g, 437.3)

g = Grid("title-na", [X0, X1], [1750])
g.put(X0, X1, 0, 1, [line1(55, 60, 598, 603)], align="LEFT", line=1550)
block(g, 598.0)

# ---------------------------------------------------------------------------
# 나. 복리후생: 주요 분야 | 항 목 | 정부 지침 내용 | 운영 결과 | 준수 여부
# ---------------------------------------------------------------------------
xs = [X0, 116.2, 147.4, 343.0, 513.1, X1]
ys = [639.2, 658.7, 678.2, 697.6, 717.1, 736.5, 756.0]
g = Grid("welfare", xs, [1840] + [int(round((b - a) * 100)) for a, b in zip(ys, ys[1:])])
heads(g, [(X0, 116.2), (116.2, 147.4), (147.4, 343.0), (343.0, 513.1), (513.1, X1)], 624.5)
for k, (y0, y1) in enumerate(zip(ys, ys[1:])):
    r, last = k + 1, k == len(ys) - 2
    edge = "mid" if last else "soft"
    if r == 6:                                       # 창립기념일 spans 분야 + 항목
        g.put(X0, 147.4, r, r + 1, cell_runs(56, 147.4, y0, y1), frame(SHADE, bottom=edge))
    else:
        g.put(116.2, 147.4, r, r + 1, cell_runs(116.2, 147.4, y0, y1), frame(SHADE, bottom=edge, left="soft"))
    g.put(147.4, 343.0, r, r + 1, cell_runs(147.4, 343.0, y0, y1), frame(bottom=edge), align="LEFT")
    if r >= 4:
        g.put(343.0, 513.1, r, r + 1, cell_runs(343.0, 513.1, y0, y1),
              frame(bottom="strong" if last else "soft", left="strong", right="soft"), align="LEFT")
for r0, r1 in ((1, 4), (4, 5), (5, 6)):
    g.put(X0, 116.2, r0, r1, cell_runs(56, 116.2, ys[r0 - 1], ys[r1 - 1]), frame(SHADE, bottom="soft"), line=1350)
g.put(343.0, 513.1, 1, 4, indented(343.0, 513.1, ys[0], ys[3], 346.0), frame(bottom="soft", left="strong",
                                                                                right="soft"),
      align="LEFT", line=1500)
verdict(g, 513.1, 1, 6, ys[0], ys[5], False)
verdict(g, 513.1, 6, 7, ys[5], ys[6], True)
block(g, 620.8)

# ---------------------------------------------------------------------------
# 주요성과 (text layer)
# ---------------------------------------------------------------------------
g = Grid("result", [X0, 111.7, 114.8, X1], [3990])
g.put(X0, 111.7, 0, 1, [runs_of(line1(65, 70, 775, 780), WHITE)], frame("#6A6A6A", top="mid", bottom="mid",
                                                                         left="mid"))
g.put(114.8, X1, 0, 1, lines_in(115, 120, 765, 800), frame(top="mid", bottom="mid", left="mid", right="mid"),
      align="LEFT", line=1500)
block(g, 762.6)

kit.finish(target, end=803.0)
