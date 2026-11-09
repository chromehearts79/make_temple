"""Rebuild KDN 2025 report page 74 (second PDF local page 24, printed page 48) as editable HWPX.

Usage: python3 work/kdn2025/p74.py <report2.pdf> <out.hwpx> [--page 24]

친환경･탄소중립 "나. 기후위기 취약계층 대상 에너지 지원 및 생활 자원순환 실천": the 따밝동행
program (추진배경 / 환경분석 / 추진목표 / 개선영역 table with photos / 주요성과) and the 자원순환
block (추진배경, four result cards, 주요성과). Built with the shared kit: one flat table per band
at its PDF y; text from the PDF text layer except the card block.

Images in the source and how they are kept:
- PART box, □ heading boxes, 'NEW 신규' / '지적사항 개선' stickers, the 정책 / 강화 / 지원 and
  맞춤형 / 고효율 / 무사고 tags (text layer) -> cells; the (+) joint -> "+", the chevron -> "▶";
  the decorative funnel under 추진목표 is left out; the three photos -> empty photo cells.
- the four result cards (y 560-759) are one image: their text was read from 4x-14x renders and
  typed; the check-mark bullets -> "◎", the dotted arrows -> "→" / "←"; the three small bar
  charts -> value cells ('24 / '25 values, years, caption); the photo in card 04 -> photo cell
  with its caption. Source oddity kept as printed: card 03 prints "1.561kg" (period) next to
  "1,103kg" (comma) and the card total "1.56톤".
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kit  # noqa: E402
from kit import Layout, recipe_inputs  # noqa: E402

source, target = recipe_inputs(24, "따밝동행")
L = Layout(top=3200)
kit.setup(source, L)
from kit import *  # noqa: E402,F401,F403  helpers and presets bound to this page

LABEL = frame("#EBEBEB", top="soft", hatch="#DDDDDD")
LABEL2 = frame("#D9D9D9", top="mid", bottom="mid", left="mid")
RESULT = frame("#6A6A6A", top="mid", bottom="mid", left="mid")
TAGBOX = frame(WHITE, top="soft", bottom="soft", left="soft", right="soft")
TAGDARK = frame("#6E6E6E")
GRAYTXT = "#8A8A8A"


def tag(g, x0, x1, r0, r1, content, fill, ratio=88, **kw):
    """Small tag / pill cell: 0.6 pt side padding instead of 5 pt, 장평 fitted to that width."""
    items = content if isinstance(content, list) else [content]
    inner = (to_x(x1) - to_x(x0) - 120) / 100 * 0.96
    for item in items:
        runs = [(item, kw.get("size", 1080))] if isinstance(item, str) else (
            runs_of(item) if isinstance(item, dict) else item)
        need = text_width(runs, ratio)
        if need > inner:
            ratio = int(ratio * inner / need)
    g.put(x0, x1, r0, r1, content, fill, fit=False, ratio=ratio, **kw)
    key = (r0, g.xs.index(to_x(x0)))
    g.items[key] = g.items[key][:7] + (dict(left=60, right=60),)


def boxed(name, label_line, lines, top, height, label_fill=LABEL2, label_color=INK):
    """추진배경 / 주요성과 box: label at the left, outlined body with bullet lines."""
    g = Grid(name, [X0, 111.5, 115.0, X1], [height])
    g.put(X0, 111.5, 0, 1, [runs_of(label_line, label_color)], label_fill)
    g.put(111.5, 115.0, 0, 1, [], frame(top="mid", bottom="mid"))
    g.put(115.0, X1, 0, 1, lines, frame(top="mid", bottom="mid", right="mid"), align="LEFT", line=1540)
    block(g, top)


def square_heading(name, line, top, cut, width, label, size=780):
    """'□ heading [sticker]': the □ box is an image in the PDF; the sticker is a dark tag cell."""
    g = Grid(name, [X0, cut, cut + width, X1], [1700])
    g.put(X0, cut, 0, 1, [[("□ ", 1350, True, INK)] + runs_of(line)], align="LEFT", line=1500)
    tag(g, cut, cut + width, 0, 1, label, frame("#3C3C3C"), ratio=80, size=size, bold=True, color=WHITE, line=950)
    block(g, top)


# ---------------------------------------------------------------------------
# Page chrome (even page): PART box with rule, footer page number + KDN logo (typed).
# ---------------------------------------------------------------------------
foot = [(line1(55, 60, 816, 822)["text"], 1090, False, INK), ("    ", 790, False, INK),
        ("한전KDN㈜", 1090, True, INK)]
L.add_table([[cell(0, W, 1500, [para(foot, "LEFT", 1300)[0]])]], floating=(5660, 81550))

g = Grid("head", [X0, 99.0, 158.5, X1], [1680])
g.put(X0, 99.0, 0, 1, [[("PART ", 800, False, INK), ("01", 1300, True, INK)]], frame("#EFEFEF", top="strong"))
g.put(99.0, 158.5, 0, 1, "경영관리", frame("#333333"), size=1080, bold=True, color=WHITE)
g.put(158.5, X1, 0, 1, [], frame(bottom="soft"))
block(g, 32.0)

g = Grid("title-na", [X0, X1], [1800])
g.put(X0, X1, 0, 1, [line1(55, 60, 69, 75)], align="LEFT", line=1550)
block(g, 69.0)

# ---------------------------------------------------------------------------
# □ 따밝동행 program
# ---------------------------------------------------------------------------
square_heading("heading-1", line1(68, 75, 90, 96), 89.5, 400.0, 27.0,
               [[("NEW ", 480, True, WHITE), ("신규", 780, True, WHITE)]])

g = Grid("footnote", [X0, X1], [1350])
g.put(X0, X1, 0, 1, [line1(55, 60, 110, 116)], align="LEFT", line=1150)
block(g, 110.5)

# 추진배경: the 국정과제 43 box closes the first line (own outlined cell)
first, second = lines_in(115, 120, 130, 152)
g = Grid("background-1", [X0, 111.5, 115.0, 404.4, 453.0, X1], [350, 1550, 1550, 250])
g.put(X0, 111.5, 0, 4, [line1(65, 70, 139, 145)], LABEL2)
g.put(111.5, 115.0, 0, 4, [], frame(top="mid", bottom="mid"))
g.put(115.0, X1, 0, 1, [], frame(top="mid", right="mid"))
g.put(115.0, 404.4, 1, 2, [runs_of(first, x1=405.0)], align="LEFT", line=1300)
tag(g, 404.4, 453.0, 1, 2, [runs_of(first, x0=405.0)], TAGBOX, line=1050)
g.put(453.0, X1, 1, 2, [], frame(right="mid"))
g.put(115.0, X1, 2, 3, [second], frame(right="mid"), align="LEFT", line=1300)
g.put(115.0, X1, 3, 4, [], frame(bottom="mid", right="mid"))
block(g, 128.0)

# 환경분석: 대외환경 + 대내여건 ▶ 시사점 (tagged two-line findings)
boxes = ((116.0, 118.9, 139.1, 253.0, 120), (267.0, 275.2, 295.4, 404.0, 276), (419.0, 421.3, 441.5, X1, 422))
xs = [X0, 113.0] + sorted({x for b in boxes for x in b[:4]})
g = Grid("environment", xs, [1800, 450, 1450, 1600, 500])
g.put(X0, 113.0, 0, 5, [line1(65, 70, 195, 200)], LABEL)
for k, (a, t0, t1, e, lx) in enumerate(boxes):
    head = line1(a, e, 175, 180)
    g.put(a, e, 0, 1, [head], frame("#DADADA", top="mid", left="soft", right="soft"), line=1300)
    g.put(a, e, 1, 2, [], frame(left="soft", right="soft"))
    first = line1(lx - 2, lx + 3, 196, 200)
    g.put(a, t0, 2, 3, [], frame(left="soft"))
    tag(g, t0, t1, 2, 3, [runs_of(first, WHITE, x1=t1 - 1)], TAGDARK, line=1050)
    g.put(t1, e, 2, 3, [strip_runs(runs_of(first, x0=t1 - 1))], frame(right="soft"), align="LEFT", line=1280)
    g.put(a, e, 3, 4, [line1(lx - 4, lx + 5, 210, 214)], frame(left="soft", right="soft"), line=1300)
    g.put(a, e, 4, 5, [], frame(left="soft", right="soft", bottom="soft"))
g.put(253.0, 267.0, 1, 4, "+", size=1500, bold=True, color="#9A9A9A", fit=False)
g.put(404.0, 419.0, 1, 4, "▶", size=1100, color=ARROW)
block(g, 172.0)

# 추진목표 band (the funnel graphic under it is decorative and left out)
g = Grid("goal", [X0, 113.0, 116.0, X1], [2600])
g.put(X0, 113.0, 0, 1, [line1(65, 70, 242, 247)], LABEL)
g.put(116.0, X1, 0, 1, [line1(170, 180, 240, 246)], frame("#D6D6D6"), line=1300)
block(g, 235.0)

# 개선영역 | 추진내용 | 추진실적 (+ photo) table; 추진실적 framed by a strong border
XL, XC, XP = 113.4, 357.2, 498.0
rows = ((303.4, 348.8), (348.8, 394.1), (394.1, 439.4))
hs = [1840]
for a, e in rows:
    h = int(round((e - a) * 100))
    hs += [550, 1800, 1700, h - 550 - 1800 - 1700]
xs = [X0, 64.0, 106.0, XL, XC, XP, X1]
g = Grid("areas", xs, hs)
g.put(X0, XL, 0, 1, [line1(65, 70, 287, 292)], frame("#D7D7D7", top="mid"))
g.put(XL, XC, 0, 1, [line1(215, 220, 287, 292)], frame("#D7D7D7", top="mid"))
g.put(XC, X1, 0, 1, [runs_of(line1(435, 440, 287, 292), WHITE)], frame("#7E7E7E", top="strong", left="strong",
                                                                         right="strong"))
label = frame("#EBEBEB", bottom="soft")
for k, (a, e) in enumerate(rows):
    r = 1 + 4 * k
    last = k == 2
    bottom = "mid" if last else "soft"
    g.put(X0, XL, r, r + 1, [], frame("#EBEBEB"))
    g.put(X0, 64.0, r + 1, r + 2, [], frame("#EBEBEB"))
    tag(g, 64.0, 106.0, r + 1, r + 2, [runs_of(line1(70, 75, a + 5, a + 15), WHITE)], TAGDARK, line=1100)
    g.put(106.0, XL, r + 1, r + 2, [], frame("#EBEBEB"))
    g.put(X0, XL, r + 2, r + 3, [line1(58, 62, a + 20, a + 32)], frame("#EBEBEB"), line=1250)
    g.put(X0, XL, r + 3, r + 4, [], frame("#EBEBEB", bottom=bottom))
    g.put(XL, XC, r, r + 4, lines_in(114, 118, a, e), frame(bottom=bottom), align="LEFT", line=1540)
    g.put(XC, XP, r, r + 4, lines_in(358, 362, a, e), frame(bottom=bottom, left="strong"), align="LEFT",
          line=1540)
    g.put(XP, X1, r, r + 4, [], frame("#E4E4E4", top="soft", bottom="strong" if last else "soft",
                                      left="soft", right="strong"))
block(g, 285.0)

boxed("result-1", line1(65, 70, 457, 462), lines_in(115, 120, 449, 470), 446.0, 3700, RESULT, WHITE)

# ---------------------------------------------------------------------------
# □ 자원순환 block
# ---------------------------------------------------------------------------
square_heading("heading-2", line1(68, 75, 494, 500), 494.0, 425.5, 53.5, "지적사항 개선", size=760)
boxed("background-2", line1(65, 70, 528, 533), lines_in(115, 120, 519, 541), 517.0, 3700)

# Banner over the four cards (image in the PDF; typed)
g = Grid("cards-title", [X0, X1], [2150])
g.put(X0, X1, 0, 1, "생활 기반 자원순환 확산을 통한 환경부담 저감 실천", frame(top="mid", left="strong", right="strong"),
      size=1190, bold=True, line=1400)
block(g, 560.0)

CARDS = [
    dict(num="01", head="→ 業의 특성을 살린「폐전산제품 친환경 처리」",
         bullets=["노후 전산장비 회수 및 친환경 분해 · 선별 처리", "자원 재활용 확대를 통한 환경부하 저감"],
         result=[("전년대비 처리량 91% 증가", 1050, True, INK), ("(’25년 약 11톤)", 790, False, INK)],
         chart=("5.7톤", "10.9톤", "폐전산제품 처리량")),
    dict(num="02", head="순환의 가치를 더하는「폐식용유 친환경 재활용」 ←",
         bullets=["폐식용유 수거-자원화 밸류체인 구축",
                  [("친환경 연료", 990), ("(바이오디젤)", 790), (" 전환으로 자원 재순환", 990)]],
         result=[("전년대비 바이오디젤 생산량 75% 증가", 1050, True, INK)],
         chart=("184kg", "322kg", "바이오디젤 생산량")),
    dict(num="03", head="→ 자원순환 체험공간「KDN 에코존(Eco-Zone)」",
         bullets=["IoT 기반 캔·플라스틱 자동수거기기 운영",
                  [("자원순환 교육·체험·전시형 에코존 재조성", 990), ("(1월)", 790)]],
         result=[("에코존 순환자원 누적 회수량 1.56톤", 1050, True, INK)],
         chart=("1,103kg", "1.561kg", "에코존 누적 회수량")),
    dict(num="04", head="자원사용을 줄이는「디지털 친환경 교육장」 ←",
         bullets=["디지털 자료 공유로 종이·인쇄물 사용 Zero",
                  [("종이 없는 친환경 교육장「AI 러닝센터」구축", 990), ("(12월)", 790)]],
         result=[("출력물 없는 디지털 교육장 상시 운영", 1050, True, INK)],
         chart=None),
]


def bullet(item):
    runs = [(item, 990)] if isinstance(item, str) else item
    return [("◎ ", 800, False, "#6A6A6A")] + [(t, s, False, INK) for t, s in runs]


def value(text, bold):
    """Chart value label: number at 7.4 pt, a trailing unit (kg) smaller, as in the image."""
    if text.endswith("kg"):
        return [(text[:-2], 740 if bold else 720, bold, INK), ("kg", 560, bold, INK)]
    return [(text, 780 if bold else 740, bold, INK)]


def card_row(name, top, pair, hs):
    """Two cards side by side. Left card: number at the left; right card: number at the right."""
    left, right = pair
    # card edges: left 56.6-302.2 (chart 251.0-302.2), right 309.0-555.6 (chart 504.0-555.6)
    xs = [X0, 80.0, 248.0, 251.0, 276.5, 302.2, 309.0, 501.0, 504.0, 530.0, 532.0, X1]
    g = Grid(name, xs, hs)
    head_fill = frame("#E3E3E3", top="mid")
    num_fill = frame("#5A5A5A", top="mid")
    g.put(X0, 80.0, 0, 1, left["num"], num_fill, size=1450, bold=True, color=WHITE, line=1600)
    g.put(80.0, 302.2, 0, 1, [[("→ ", 1000, False, GRAYTXT), (left["head"][2:], 1090, False, INK)]], head_fill,
          align="LEFT", line=1300)
    g.put(309.0, 532.0, 0, 1, [[(right["head"][:-2], 1090, False, INK), (" ←", 1000, False, GRAYTXT)]]
          if right["head"].endswith("←") else [right["head"]], head_fill, align="RIGHT", line=1300)
    g.put(532.0, X1, 0, 1, right["num"], num_fill, size=1450, bold=True, color=WHITE, line=1600)
    for card, (a, b, c0, cm, e) in ((left, (X0, 248.0, 251.0, 276.5, 302.2)), (right, (309.0, 501.0, 504.0, 530.0, X1))):
        g.put(a, e, 1, 2, [], frame(left="mid", right="mid"))
        g.put(a, c0, 2, 3, [bullet(card["bullets"][0])], frame(left="mid"), align="LEFT", line=1300)
        g.put(a, c0, 3, 4, [bullet(card["bullets"][1])], frame(left="mid"), align="LEFT", line=1300)
        g.put(a, c0, 4, 5, [], frame(left="mid"))
        g.put(a, b, 5, 7, [card["result"]], frame("#E3E3E3", left="mid"), line=1250)
        g.put(b, c0, 5, 7, [], frame())
        g.put(a, e, 7, 8, [], frame(left="mid", right="mid", bottom="mid"))
        if card["chart"]:
            before, after, caption = card["chart"]
            tag(g, c0, cm, 2, 3, [value(before, False)], "1", ratio=84, line=900)
            tag(g, cm, e, 2, 3, [value(after, True)], frame(right="mid"), ratio=84, line=900)
            g.put(c0, cm, 3, 5, [], frame("#DDDDDD", bottom="soft"))
            g.put(cm, e, 3, 5, [], frame("#8C8C8C", bottom="soft", right="mid"))
            g.put(c0, cm, 5, 6, "’24년", frame("#EEEEEE"), size=720, line=740)
            g.put(cm, e, 5, 6, "’25년", frame("#EEEEEE", right="mid"), size=720, bold=True, line=740)
            tag(g, c0, e, 6, 7, caption, frame(right="mid"), ratio=84, size=720, line=860)
        else:
            g.put(c0, e, 2, 6, [], frame("#E4E4E4", top="soft", left="soft", right="mid"))
            g.put(c0, e, 6, 7, "AI 러닝센터", frame("#4A4A4A", right="mid"), size=760, color=WHITE, line=860)
    block(g, top)


card_row("cards-1", 586.0, CARDS[:2], [2000, 400, 1550, 1550, 550, 900, 1050, 300])
card_row("cards-2", 675.0, CARDS[2:], [2000, 400, 1550, 1550, 500, 900, 1050, 300])

boxed("result-2", line1(65, 70, 776, 781), lines_in(115, 120, 768, 790), 765.0, 3700, RESULT, WHITE)

kit.finish(target, end=803.0)
