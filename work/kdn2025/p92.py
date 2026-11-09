"""Rebuild KDN 2025 report PDF page 92 (second PDF local page 42, printed page 62) as editable HWPX.

Usage: python3 work/kdn2025/p92.py <report2.pdf> <out.hwpx> [--page 42]

상생･협력 및 지역발전, section 5 (계약체계 고도화). Built with the shared diagram kit (one flat
table per horizontal band on a grid of PDF x edges; rows here are given as PDF y edges). Images:
the section-number band, the PART box, the □ marks and the whole 가. P-D-C-A diagram (y 121-283)
are images; the diagram text was read from 4x / 4.5x renders and typed. Its italic quotation
(“불공정 행위 …”) is typed upright (the builder has no italic runs). The circled arrows of the
3중 통제구조 band become ▶ connector cells, the (+) joints '+' cells, the photo an empty cell;
the 기존 / 신규 / 개선 / 지속 / N단계 tags are separate boxed or dark cells.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kit  # noqa: E402
from kit import Layout, recipe_inputs  # noqa: E402

source, target = recipe_inputs(42, "계약 리스크 예방과 공정한 경제질서 확립을 위한 계약체계 고도화")
L = Layout(top=3100)
kit.setup(source, L)
from kit import *  # noqa: E402,F401,F403  helpers and presets bound to this page

DARK, LABEL = "#6A6A6A", "#E6E6E6"
BAND, SIDE, PILLDARK = "#E6E6E6", "#E8E8E8", "#555555"
PLUS = "#9A9A9A"
BOXTAG = frame(WHITE, top="soft", bottom="soft", left="soft", right="soft")
DARKTAG = frame("#7E7E7E")


def hang(lines, base):
    """Lines keep their PDF indent: spaces for the x offset and for the line's own lead."""
    out = []
    for l in lines:
        runs = runs_of(l)
        size = runs[0][1] / 100
        raw = "".join(s["text"] for s in l["spans"])
        offset = l["bbox"][0] - base + (len(raw) - len(raw.lstrip(" "))) * 0.29 * size
        n = max(0, round(offset / (0.29 * size)))
        out.append([(" " * n, runs[0][1], False, INK)] + runs if n else runs)
    return out


def split(line, cuts, colors=None):
    """One PDF line cut at x positions into run lists (tag words become their own cells)."""
    edges = [-1e9, *cuts, 1e9]
    colors = colors or [INK] * (len(edges) - 1)
    return [strip_runs(runs_of(line, c, x0=a, x1=b)) for a, b, c in zip(edges, edges[1:], colors)]


class YGrid:
    """Grid whose rows are given as PDF y edges; cells are placed by (x0, x1, y0, y1)."""

    def __init__(self, name, xs, ys):
        self.ys = ys
        self.g = Grid(name, xs, [round(b * 100) - round(a * 100) for a, b in zip(ys, ys[1:])])

    def row(self, y):
        for i, v in enumerate(self.ys):
            if abs(v - y) < 0.01:
                return i
        raise ValueError(f"{self.g.name}: no row edge at y {y}")

    def put(self, x0, x1, y0, y1, content, fill="1", **kw):
        self.g.put(x0, x1, self.row(y0), self.row(y1), content, fill, **kw)

    def tag(self, x0, x1, y0, y1, runs, fill):
        """Small tag cell: thin symmetric padding so a short tag stays on one line."""
        width = to_x(x1) - to_x(x0)
        ratio = min(90, int(90 * (width - 160) / 100 * 0.96 / text_width(runs, 90)))
        self.put(x0, x1, y0, y1, [runs], fill, line=1000, ratio=ratio, fit=False)
        key = (self.row(y0), self.g.xs.index(to_x(x0)))
        self.g.items[key] = (*self.g.items[key][:7], dict(left=80, right=80, top=40, bottom=40))

    def done(self):
        block(self.g, self.ys[0])


def section_band(name, num_line, title_line, top):
    """'5 | heading' band: dark number cell and light gray title cell (images in the PDF)."""
    g = Grid(name, [X0, 84.5, X1], [2300])
    g.put(X0, 84.5, 0, 1, [runs_of(num_line, WHITE)], frame(DARK), line=1700)
    g.put(84.5, X1, 0, 1, [runs_of(title_line)], frame(LABEL), align="LEFT", line=1700)
    block(g, top)


def title(name, line, top):
    g = Grid(name, [X0, X1], [1650])
    g.put(X0, X1, 0, 1, [line], align="LEFT", line=1450)
    block(g, top)


def boxed(name, label_line, body_lines, top, height, label_fill="#D5D5D5", label_color=INK):
    """추진배경 / 주요성과 box: label at left, outlined body with bullet lines."""
    g = Grid(name, [X0, 111.7, X1], [height])
    g.put(X0, 111.7, 0, 1, [runs_of(label_line, label_color)],
          frame(label_fill, top="mid", bottom="mid", left="mid"))
    g.put(111.7, X1, 0, 1, body_lines, frame(top="mid", bottom="mid", right="mid"), align="LEFT")
    block(g, top)


T = 1090   # body text size of the typed diagram


def tagrun(word, color=INK):
    return [(word, 840, True, color)]


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

section_band("sec5", line1(60, 70, 72, 76), line1(90, 95, 73, 77), 70.9)
title("title-ga", line1(55, 60, 98, 102), 98.4)

# ---------------------------------------------------------------------------
# 가. P-D-C-A diagram (an image in the PDF; text read from 4x renders)
# ---------------------------------------------------------------------------
COLS = ((118.5, 136.5, 264.8), (267.8, 285.6, 409.0), (412.3, 430.1, X1))
xs = [X0, 72.2, 104.5, 114.0, 118.5, 136.5, 264.8, 267.8, 285.6, 409.0, 412.3, 430.1, X1]
ys = [121.0, 127.8, 141.0, 157.0,
      161.2, 166.0, 179.0, 182.0, 193.7, 196.4, 208.0, 212.0,
      217.3, 229.0, 231.7, 243.3, 250.0,
      255.8, 269.2, 283.2]
g = YGrid("pdca", xs, ys)


def step(letter, word, y0, pill, text, y1):
    """Left label: bracket lines, dark pill with the PDCA letter, spaced Korean word."""
    g.put(X0, 72.2, y0, y1, [], frame(top="mid", left="mid"))
    g.put(72.2, 114.0, y0, pill[0], [], frame(top="mid"))
    g.put(72.2, 104.5, pill[0], pill[1], letter, frame(PILLDARK), size=1150, color=WHITE, line=1100)
    g.put(72.2, 104.5, text[0], text[1], word, size=1150, bold=True, line=1200)


step("P", "계  획", 121.0, (127.8, 141.0), (141.0, 157.0), 157.0)
step("D", "실  행", 161.2, (166.0, 179.0), (179.0, 196.4), 212.0)
step("C", "점  검", 212.0, (217.3, 231.7), (231.7, 250.0), 250.0)
step("A", "환  류", 250.0, (255.8, 269.2), (269.2, 283.2), 283.2)

g.put(118.5, X1, 121.0, 157.0, [
    [("· 공정한 거래질서 확립을 위한 기관장 의지표명 “불공정 행위 방지를 위한 제도 개선 등 강화해야", T, False, INK),
     ("(기관장 7월 경영서신)", 820, False, INK), ("”", T, False, INK)],
    [("· 중소기업과의 공정거래 질서 확립 및 3대 계약 리스크", T, False, INK), ("(입찰 · 대금 · 하도급)", 880, False, INK),
     (" 해소를 위한 개선 계획 수립", T, False, INK)]], frame(BAND), align="LEFT", line=1450)

heads = ("입찰Risk", "대금Risk", "하도급Risk")
rows = ((("기존", "입찰담합 금지 및 신고 안내 강화"), ("신규", "임직원 입찰담합 근절 다짐 서약")),
        (("기존", "대금지급 7일 전 자동 알림"), ("신규", "SW사업 인력지원 적격심사 도입")),
        (("기존", "하도급 적법성 체크리스트 의무화"), ("신규", "하도급 승인 관리 시스템 구축")))
for k, ((a, b, e), head, (old, new)) in enumerate(zip(COLS, heads, rows)):
    sep = "dot" if k < 2 else None
    g.put(a, b, 161.2, 179.0, str(k + 1), frame("#6E6E6E", top="mid"), size=1150, bold=True, color=WHITE)
    g.put(b, e, 161.2, 179.0, head, frame("#E4E4E4", top="mid", right=sep), size=1150)
    g.put(a, e, 179.0, 182.0, [], frame(right=sep))
    for (word, text), (y0, y1, y2), fill, color in ((old, (182.0, 193.7, 196.4), BOXTAG, INK),
                                                    (new, (196.4, 208.0, 212.0), DARKTAG, WHITE)):
        g.tag(a, b, y0, y1, tagrun(word, color), fill)
        last = y2 == 212.0
        g.put(b, e, y0, y2, [[(text, T, False, INK)]], frame(right=sep, bottom="dot" if last else None),
              align="LEFT", line=1200)
    g.put(a, b, 193.7, 196.4, [], frame())
    g.put(a, b, 208.0, 212.0, [], frame(bottom="dot"))

for word, text, (y0, y1, y2), fill, color in (
        ("기존", "공정계약 체크리스트 및 효과성 평가를 통한 공정계약 준수 여부 직원 모니터링 시행", (217.3, 229.0, 231.7),
         BOXTAG, INK),
        ("신규", "「입찰 담합행위 신고센터」 시스템 신설 및 신고 내용 실시간 알림", (231.7, 243.3, 250.0), DARKTAG, WHITE)):
    g.tag(118.5, 136.5, y0, y1, tagrun(word, color), fill)
    g.put(136.5, X1, y0, y2, [[(text, T, False, INK)]], frame(bottom="dot") if y2 == 250.0 else "1",
          align="LEFT", line=1200)
g.put(118.5, 136.5, 243.3, 250.0, [], frame(bottom="dot"))
g.put(118.5, X1, 250.0, 283.2, [
    [("· 내부통제 설계·운영평가 및 모니터링 결과에 대한 리스크 유형별 분석을 통해 향후 개선과제 도출", T, False, INK)],
    [("· 제도, 업무 프로세스 및 시스템 개선에 반영하여 계약 리스크 예방 체계 고도화", T, False, INK)]],
      frame(BAND), align="LEFT", line=1400)
g.done()

# ---------------------------------------------------------------------------
# 나. SW사업 인력지원 제도 개선
# ---------------------------------------------------------------------------
title("title-na", line1(55, 60, 290, 295), 291.0)
heading("head-sw", line1(68, 75, 310, 315), 311.0)
boxed("background", line1(65, 70, 342, 346), lines_in(115, 120, 334, 356), 331.1, 3710)

xs = [X0, 105.4, 110.5, 186.7, 205.4, 313.7, 333.0, 415.3, 434.1, 553.3, X1]
g = YGrid("as-is", xs, [373.5, 378.3, 390.0, 397.5, 446.9])
g.put(X0, 105.4, 373.5, 446.9, lines_in(60, 100, 395, 420), frame(SIDE, top="soft"), bold=True, line=1320)
for a, t0, t1, e, x, color, fill, base in ((110.5, 186.7, 205.4, 313.7, 190, INK, BOXTAG, 113.5),
                                           (333.0, 415.3, 434.1, 553.3, 420, WHITE, DARKTAG, 336.1)):
    head = line1(t0, t1, 376, 382)
    tagged, rest = split(head, [t1 - 0.5], [color, INK])
    g.put(a, t0, 373.5, 397.5, [], frame(top="mid", left="mid"))
    g.put(t0, t1, 373.5, 378.3, [], frame(top="mid"))
    g.tag(t0, t1, 378.3, 390.0, tagged, fill)
    g.put(t1, e, 373.5, 378.3, [], frame(top="mid", right="mid"))
    g.put(t1, e, 378.3, 397.5, [rest], frame(right="mid"), align="LEFT", line=1250)
    g.put(a, e, 397.5, 446.9, hang(lines_in(base - 1, base + 5, 398, 442), base),
          frame("#EBEBEB", left="mid", right="mid", bottom="mid"), align="LEFT", line=1430)
g.put(313.7, 333.0, 397.5, 446.9, "▶", size=1300, color="#C4C4C4")
g.done()

g = Grid("bonus", [X0, 105.4, 110.5, X1], [2610])
g.put(X0, 105.4, 0, 1, [line1(60, 65, 458, 462)], frame(SIDE, top="soft"), bold=True)
g.put(110.5, X1, 0, 1, [line1(110, 115, 458, 462)], frame(top="mid", bottom="mid", left="mid", right="mid"),
      align="LEFT")
block(g, 452.0)

# ---------------------------------------------------------------------------
# □ 3중 통제구조 / 제도효과
# ---------------------------------------------------------------------------
heading("head-sub", line1(68, 75, 484, 489), 485.0)

xs = [X0, 105.5, 110.5, 139.4, 167.8, 236.6, 245.2, 253.9, 255.2, 283.6, 286.5, 305.3, 410.9, 412.0, 428.2,
      456.1, 484.5, X1]
ys = [504.9, 508.4, 520.1, 523.7, 555.5]
g = YGrid("triple", xs, ys)
g.put(X0, 105.5, 504.9, 555.5, lines_in(60, 100, 519, 540), frame(SIDE, top="soft"), bold=True, line=1320)
LIGHT, MID = frame("#E2E2E2", top="soft"), frame("#6E6E6E", top="soft")
stages = (  # band x0, tag x0, tag x1, (other tag), text x1, band fill, text colour, line y
    (110.5, 139.4, 167.8, None, 236.6, LIGHT, INK, 508.7),
    (253.9, 255.2, 283.6, (286.5, 305.3), 410.9, MID, WHITE, 508.7),
    (428.2, 456.1, 484.5, None, X1, LIGHT, INK, 508.7),
)
for a, t0, t1, extra, e, band, color, y in stages:
    line = line1(t0, t1, y - 1, y + 1)
    if extra:
        tagged, new, rest = split(line, [t1 + 1.0, extra[1] - 0.5], [INK, INK, color])
    else:
        tagged, rest = split(line, [t1 - 0.5], [INK, color])
    if t0 > a:
        g.put(a, t0, 504.9, 523.7, [], band)
    g.put(t0, t1, 504.9, 508.4, [], band)
    g.tag(t0, t1, 508.4, 520.1, tagged, BOXTAG)
    g.put(t0, t1, 520.1, 523.7, [], band)
    start = t1
    if extra:
        g.put(t1, extra[0], 504.9, 523.7, [], band)
        g.put(extra[0], extra[1], 504.9, 508.4, [], band)
        g.tag(extra[0], extra[1], 508.4, 520.1, new, BOXTAG)
        g.put(extra[0], extra[1], 520.1, 523.7, [], band)
        start = extra[1]
    g.put(start, e, 504.9, 508.4, [], band)
    g.put(start, e, 508.4, 523.7, [rest], band, align="LEFT", bold=True, line=1250)
for a, e, fill in ((236.6, 253.9, LIGHT), (410.9, 428.2, MID)):
    g.put(a, e, 504.9, 523.7, "▶", fill, size=900, color="#9A9A9A")
for a, e, x in ((110.5, 245.2, 108.0), (245.2, 412.0, 250.0), (412.0, X1, 422.0)):
    g.put(a, e, 523.7, 555.5, lines_in(x, x + 25, 526, 548), frame(bottom="soft", right="soft" if e < X1 else None),
          line=1430)
g.done()

g = Grid("chevron", [X0, 107.6, X1], [1160])
g.put(107.6, X1, 0, 1, "▼", frame("#F0F0F0"), size=800, color=ARROW, line=860)
block(g, 559.9)

xs = [X0, 105.5, 110.5, 245.2, 264.5, 399.2, 418.5, 553.2, X1]
g = YGrid("effects", xs, [573.4, 576.3, 590.8, 623.1])
g.put(X0, 105.5, 573.4, 623.1, [line1(60, 65, 594, 598)], frame(SIDE, top="soft"), bold=True)
for a, e in ((110.5, 245.2), (264.5, 399.2), (418.5, 553.2)):
    g.put(a, e, 576.3, 590.8, [lines_in(a, e, 576, 582)[0]], frame("#D9D9D9", top="mid", left="mid", right="mid"),
          line=1250)
    g.put(a, e, 590.8, 623.1, lines_in(a, e, 594, 615), frame(left="mid", right="mid", bottom="mid"), line=1430)
for a, e in ((245.2, 264.5), (399.2, 418.5)):
    g.put(a, e, 590.8, 623.1, "+", size=1300, bold=True, color=PLUS, fit=False)
g.done()

# ---------------------------------------------------------------------------
# 다. KDN Fair: 소통 / 교육 / 캠페인 with tagged lines and a photo
# ---------------------------------------------------------------------------
title("title-da", line1(55, 60, 633, 638), 634.0)
xs = [X0, 94.0, 102.1, 120.8, 445.0, 447.9, 552.8, X1]
ys = [655.1, 660.1, 671.8, 674.7, 686.4, 690.3, 693.5, 705.2, 708.2, 719.9, 723.7, 726.9, 738.6, 741.6, 753.3,
      758.9]   # the 2pt white gaps between the gray labels are dropped (rows under 2.7pt grow in Hancom)
g = YGrid("fair", xs, ys)
groups = ((655.1, 690.3, ((660.1, 671.8, 674.7), (674.7, 686.4, 690.3))),
          (690.3, 723.7, ((693.5, 705.2, 708.2), (708.2, 719.9, 723.7))),
          (723.7, 758.9, ((726.9, 738.6, 741.6), (741.6, 753.3, 758.9))))
for top, bottom, lines in groups:
    g.put(X0, 94.0, top, bottom, [line1(60, 70, top + 5, bottom - 5)], frame("#E3E3E3", bottom="soft"), bold=True)
    for k, (y0, y1, y2) in enumerate(lines):
        line = line1(100, 110, y0 - 3, y1 - 3)
        tagged, rest = split(line, [120.0])
        fill = frame("#D7D7D7", top="soft", bottom="soft", left="soft", right="soft") if tagged[0][0] == "지속" else BOXTAG
        g.tag(102.1, 120.8, y0, y1, tagged, fill)
        g.put(120.8, 445.0, y0, y2, [rest], frame(bottom="soft") if k else "1", align="LEFT", line=1250)
    g.put(94.0, 120.8, lines[1][1], bottom, [], frame(bottom="soft"))
g.put(447.9, 552.8, 655.1, 758.9, [], photo)
g.done()

boxed("result", line1(65, 70, 776, 780), lines_in(115, 120, 767, 790), 764.9, 3710,
      label_fill=DARK, label_color=WHITE)

kit.finish(target, end=803.0)
