"""Rebuild KDN 2025 report physical PDF page 42 (printed page 27) as editable HWPX.

Usage: python3 work/kdn2025/p42.py <report.pdf> <out.hwpx> [--page N]

윤리경영 평가내용 03 opening page. Built with the shared diagram kit (one flat table per
horizontal band on a grid of PDF x edges). The 평가내용 banner, PART label, section number
bands and the section-1 framework diagram (로드맵 / 추진과제 / 추진체계) are images in the source;
their text was read from a 4x render and typed. The boxed task numbers of that diagram become
①-⑥ (the source prints 1, 4 | 3, 4 | 5, 6 and that numbering is kept as printed). Decorative
chevrons become ▼ / ▶ glyphs; the 'NEW' flourish of the 신규 stickers is dropped.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kit  # noqa: E402
from kit import Layout, recipe_inputs  # noqa: E402

source, target = recipe_inputs(42, "인권교육, 인권침해 구제절차 등 인권존중을 위한 노력과 활동")
L = Layout(top=3100)
kit.setup(source, L)
from kit import *  # noqa: E402,F401,F403  helpers and presets bound to this page

DARK, LABEL = "#6A6A6A", "#E6E6E6"


def hang(lines, base):
    """Bullet lines keep their PDF indent: spaces for the x offset and for the line's own lead."""
    out = []
    for l in lines:
        runs = runs_of(l)
        size = runs[0][1] / 100
        raw = "".join(s["text"] for s in l["spans"])
        offset = l["bbox"][0] - base + (len(raw) - len(raw.lstrip(" "))) * 0.29 * size
        n = max(0, round(offset / (0.29 * size)))
        out.append([(" " * n, runs[0][1], False, INK)] + runs if n else runs)
    return out


def section_band(name, num_line, title_line, top):
    """'1 | heading' band: dark number cell and light gray title cell (images in the PDF)."""
    g = Grid(name, [X0, 84.5, X1], [2300])
    g.put(X0, 84.5, 0, 1, [runs_of(num_line, WHITE)], frame(DARK), line=1700)
    g.put(84.5, X1, 0, 1, [runs_of(title_line)], frame(LABEL), align="LEFT", line=1700)
    block(g, top)


def titled(name, line, sticker_x, top, tag="신규"):
    """'가. title' heading (14pt) followed by a small dark sticker (an image in the PDF)."""
    g = Grid(name, [X0, sticker_x, sticker_x + 25.0, X1] if sticker_x + 25.0 < X1 else [X0, sticker_x, X1], [1650])
    g.put(X0, sticker_x, 0, 1, [line], align="LEFT", line=1450)
    g.put(sticker_x, min(sticker_x + 25.0, X1), 0, 1, tag, frame("#3C3C3C"), size=880, bold=True, color=WHITE,
          line=1000)
    block(g, top)


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

g = Grid("banner", [X0, 124.0, X1], [2860])
g.put(X0, 124.0, 0, 1, [[("평가내용 ", 800, True, WHITE), ("03", 1350, True, WHITE)]], frame("#686868"),
      line=1500)
g.put(124.0, X1, 0, 1, [line1(125, 130, 76, 80)], striped, align="LEFT", line=1450)
block(g, 70.9)

section_band("sec1", line1(60, 70, 116, 120), line1(90, 95, 118, 121), 115.8)

# ---------------------------------------------------------------------------
# Section 1 framework diagram: an image in the PDF; text read from a 4x render.
# ---------------------------------------------------------------------------
xs = [X0, 110.0, 117.0, 167.0, 261.0, 264.0, 314.0, 387.0, 409.0, 412.5, 462.5, 518.5, 543.5, X1]
hs = [2400, 1850, 300, 2050, 3400, 450, 1500, 1650, 1650, 1700]
g = Grid("framework", xs, hs)
g.put(X0, X1, 0, 1, "사람을 존중하는 한전KDN", frame(top="soft", left="soft", right="soft"), size=1250, bold=True)
side = frame(LABEL)
g.put(X0, 110.0, 1, 2, "로드맵", side, size=1100)
g.put(X0, 110.0, 3, 5, "추진과제", side, size=1100)
g.put(X0, 110.0, 6, 10, "추진체계", side, size=1100)
cols = ((117.0, 167.0, 261.0), (264.0, 314.0, 409.0), (412.5, 462.5, X1))
roadmap = (("’24~’26년", "인권경영 체계 고도화"), ("’27~’28년", "인권경영 안정화"), ("’29~’30년", "인권경영 주도화"))
tasks = (("인권Risk 예방·대응체계 고도화", ("①", "사내 인권 취약분야 선별·관리"), ("④", "사내 인권보호 제도 운영 강화")),
         ("인권침해 점검·구제 강화", ("③", "정기적 인권영향평가 시행"), ("④", "인권침해 구제절차 강화")),
         ("인권존중문화 대외 확산", ("⑤", "지역 취약계층 인권 보호"), ("⑥", "협력사 인권경영 실현 지원")))
heads = ("추진조직", "추진규범", "평가 및 모니터링")
for i, ((a, b, e), (period, stage), (task, *items), head) in enumerate(zip(cols, roadmap, tasks, heads)):
    first = i == 0
    g.put(a, b, 1, 2, period, frame("#5A5A5A", top="strong" if first else None, left="strong" if first else None),
          size=1100, color=WHITE)
    g.put(b, e, 1, 2, stage, frame("#E3E3E3", top="strong" if first else None, right="strong" if first else None),
          size=1100, bold=True)
    g.put(a, e, 3, 4, task, frame("#E6E6E6", top="strong", left="strong" if first else None,
                                  right="strong" if i == 2 else None), size=1100, bold=True)
    g.put(a, e, 4, 5, [[(n + " ", 1050, True), (t, 1050, False)] for n, t in items],
          frame(left="strong" if first else "soft", right="strong" if i == 2 else None, bottom="strong"),
          align="LEFT", line=1400)
    g.put(a, e, 6, 7, head, frame("#E6E6E6"), size=1100)
g.put(117.0, 261.0, 7, 10, ["·인권경영위원회", "·내부통제부, 한전KDN 인권센터", "·부서별 윤리·인권경영담당자"],
      frame(left="soft", bottom="soft", right="dot"), align="LEFT", size=1050, line=1600)
for r, text in enumerate(("·인권경영 규정 및 시행세칙", "·인권경영헌장, 협력사 행동규범", "·성희롱·성폭력·스토킹 예방지침"), 7):
    g.put(264.0, 387.0, r, r + 1, text, frame(bottom="soft" if r == 9 else None), align="LEFT", size=1050)
    g.put(387.0, 409.0, r, r + 1, "개정", frame(top="soft", bottom="soft", left="soft", right="soft"), size=880)
g.put(409.0, 412.5, 7, 10, [], frame(left="dot", bottom="soft"))
for r, text in enumerate(("·인권영향평가", "·인권경영 수준진단 설문조사"), 7):
    g.put(412.5, X1, r, r + 1, text, frame(right="soft"), align="LEFT", size=1050)
g.put(412.5, 518.5, 9, 10, "·성희롱 방지 조직문화 진단", frame(bottom="soft"), align="LEFT", size=1050)
g.put(518.5, 543.5, 9, 10, "신규", frame(top="soft", bottom="soft", left="soft", right="soft"), size=880)
g.put(543.5, X1, 9, 10, [], frame(right="soft", bottom="soft"))
block(g, 145.5)

# ---------------------------------------------------------------------------
# 2. 사내 인권 취약분야 개선 (text layer)
# ---------------------------------------------------------------------------
section_band("sec2", line1(60, 70, 328, 332), line1(90, 95, 329, 333), 326.9)
titled("title-ga", line1(55, 60, 354, 358), 531.0, 356.0)

g = Grid("survey", [X0, 140.0, 143.3, X1], [2330])
g.put(X0, 140.0, 0, 1, [line1(60, 70, 381, 385)], frame(WHITE, top="mid", bottom="mid", left="mid", right="mid"))
g.put(143.3, X1, 0, 1, [line1(200, 210, 381, 385)], frame("#E6E6E6"))
block(g, 377.2)

g = Grid("thesis", [X0, X1], [1430, 1030])
g.put(X0, X1, 0, 1, [runs_of(line1(170, 180, 402, 406)) + [(" → ", 1090, True, INK)]
                     + runs_of(line1(320, 325, 402, 406))], line=1260)
g.put(X0, X1, 1, 2, "▼", frame("#F2F2F2"), size=800, color=ARROW, line=860)
block(g, 402.0)

# 주요 개선사항: four tagged boxes in two columns.
xs = [X0, 88.0, 90.7, 140.0, 321.7, 324.4, 374.0, 533.0, X1]
g = Grid("improve", xs, [1880, 3530, 260, 1870, 4950])
g.put(X0, 88.0, 0, 5, lines_in(60, 70, 473, 515), frame(LABEL, top="mid"), bold=True)
tag = frame("#6E6E6E")
title = frame("#E3E3E3")
body = frame(WHITE, top="soft", bottom="soft", left="soft", right="soft")
for r, y, (b0, b1) in ((0, 432, (450, 485)), (3, 489, (506, 553))):
    for a, b, e, tx, ty in ((90.7, 140.0, 321.7, 92, 140), (324.4, 374.0, X1, 325, 374)):
        g.put(a, b, r, r + 1, [runs_of(line1(tx, b, y, y + 5), WHITE)], tag)
        head = line1(b, e, y - 2, y + 3)
        if head["spans"][-1]["text"] == "개선":
            g.put(b, 533.0, r, r + 1, [strip_runs(runs_of(head, x1=534.0))], title, align="LEFT")
            g.put(533.0, e, r, r + 1, [runs_of(head, WHITE, x0=534.0)], frame("#5E5E5E"))
        else:
            g.put(b, e, r, r + 1, [head], title, align="LEFT")
        base = 96.5 if a < 100 else 330.4
        g.put(a, e, r + 1, r + 2, hang(lines_in(a, b, b0, b1), base), body, align="LEFT", line=1430)
block(g, 430.4)

g = Grid("improve-arrows", [X0, 88.0, 90.7, 321.7, 324.4, X1], [1140])
g.put(90.7, 321.7, 0, 1, "▼", size=900, color=ARROW, line=960)
g.put(324.4, X1, 0, 1, "▼", size=900, color=ARROW, line=960)
block(g, 556.5)

g = Grid("outcomes", [X0, 88.0, 90.7, 321.7, 324.4, X1], [5210, 2350])
g.put(X0, 88.0, 0, 2, lines_in(60, 70, 590, 622), frame(LABEL, top="mid"), bold=True)
g.put(90.7, 321.7, 0, 1, hang(lines_in(95, 100, 572, 616), 96.5), frame("#EEEEEE"), align="LEFT", line=1430)
g.put(324.4, X1, 0, 1, hang(lines_in(328, 335, 572, 616), 330.4), frame("#EEEEEE"), align="LEFT", line=1430)
g.put(90.7, X1, 1, 2, [line1(150, 160, 625, 630)], frame("#D6D6D6"))
block(g, 568.4)

# ---------------------------------------------------------------------------
# 나. 감사관계인 인권보호: As-Is / To-Be table with an outcome column.
# ---------------------------------------------------------------------------
titled("title-na", line1(55, 60, 651, 655), 466.0, 653.0)
xs = [X0, 102.1, 104.8, 251.5, 253.9, 444.1, 457.7, X1]
g = Grid("audit", xs, [1920, 5290, 5540])
g.put(104.8, 251.5, 0, 1, [line1(150, 160, 676, 680)], frame("#E3E3E3", top="soft"))
g.put(253.9, 444.1, 0, 1, [line1(320, 325, 676, 680)], frame("#E3E3E3", top="soft"))
g.put(457.7, X1, 0, 1, [runs_of(line1(485, 490, 677, 681), WHITE)], frame("#6A6A6A", top="mid", left="mid", right="mid"))
for r, (y0, y1), fill in ((1, (698, 745), WHITE), (2, (750, 797), "#F0F0F0")):
    last = r == 2
    g.put(X0, 102.1, r, r + 1, [line1(60, 65, y0 + 14, y0 + 32)], frame(LABEL, bottom="soft"))
    g.put(104.8, 251.5, r, r + 1, hang(lines_in(105, 120, y0, y1), 107.9), frame(fill, bottom="soft"), align="LEFT",
          line=1430)
    g.put(253.9, 444.1, r, r + 1, hang(lines_in(255, 270, y0, y1), 256.7), frame(fill, bottom="soft"), align="LEFT",
          line=1430)
    g.put(457.7, X1, r, r + 1, lines_in(460, 490, y0, y1), frame("#E9E9E9", left="mid", right="mid",
                                                               bottom="mid" if last else "soft"), line=1430)
g.put(444.1, 457.7, 1, 3, "▶", size=1000, color=ARROW)
block(g, 674.3)

kit.finish(target, end=803.0)
