"""Rebuild KDN 2025 report physical PDF page 40 (printed page 25) as editable HWPX.

Usage: python3 work/kdn2025/p40.py <report.pdf> <out.hwpx> [--page N]

윤리경영 평가내용 02 opening page. Built with the shared diagram kit (one flat table per
horizontal band on a grid of PDF x edges). The 평가내용 banner, PART label, section number
bands and the whole section-1 diagram (추진목표 ~ 확산·공유) are images in the source PDF; their
text was read from a 3.5x render and typed into editable cells. Person icons, the Kdn logo and the
decorative chevrons are omitted or replaced by plain ▼ / ▶ glyphs.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kit  # noqa: E402
from kit import Layout, recipe_inputs  # noqa: E402

source, target = recipe_inputs(40, "이해충돌방지법 제2조 제4호에 따른 이해충돌 방지를 위한 노력과 성과")
L = Layout(top=3100)
kit.setup(source, L)
from kit import *  # noqa: E402,F401,F403  helpers and presets bound to this page

DARK, LABEL = "#6A6A6A", "#E6E6E6"


def section_band(name, num_line, title_line, top):
    """'1 | heading' band: dark number cell and light gray title cell (images in the PDF)."""
    g = Grid(name, [X0, 84.5, X1], [2300])
    g.put(X0, 84.5, 0, 1, [runs_of(num_line, WHITE)], frame(DARK), line=1700)
    g.put(84.5, X1, 0, 1, [runs_of(title_line)], frame(LABEL), align="LEFT", line=1700)
    block(g, top)


def hang(lines):
    """Continuation lines are indented under their bullet in the source."""
    return [runs_of(l) if l["text"].startswith("∙") else [("  ", 1090, False, INK)] + runs_of(l) for l in lines]


def boxed(name, label_line, body_lines, top, height, label_fill="#D5D5D5", label_color=INK):
    """추진배경 / 주요성과 box: gray label at left, outlined body with bullet lines."""
    g = Grid(name, [X0, 111.7, X1], [height])
    g.put(X0, 111.7, 0, 1, [runs_of(label_line, label_color)],
          frame(label_fill, top="mid", bottom="mid", left="mid"))
    g.put(111.7, X1, 0, 1, body_lines, frame(top="mid", bottom="mid", right="mid"), align="LEFT")
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

# 평가내용 02 banner (image badge + text title).
g = Grid("banner", [X0, 124.0, X1], [2860])
g.put(X0, 124.0, 0, 1, [[("평가내용 ", 800, True, WHITE), ("02", 1350, True, WHITE)]], frame("#686868"),
      line=1500)
g.put(124.0, X1, 0, 1, [line1(125, 130, 76, 80)], striped, align="LEFT", line=1450)
block(g, 70.9)

section_band("sec1", line1(60, 70, 116, 120), line1(90, 95, 118, 121), 115.8)

# ---------------------------------------------------------------------------
# Section 1 diagram: an image in the PDF; text read from a 3.5x render.
# ---------------------------------------------------------------------------
side = frame(LABEL)
g = Grid("goal", [X0, 110.0, X1], [2600])
g.put(X0, 110.0, 0, 1, "추진목표", frame("#BEBEBE"), size=1100, bold=True)
g.put(110.0, X1, 0, 1, "공정한 직무수행과 이행력 제고를 위한 이해충돌방지제도 강화", frame("#DADADA"),
      size=1200, bold=True)
block(g, 148.5)

xs = [X0, 110.0, 116.0, 260.5, 264.0, 405.5, 409.0, 553.0, X1]
g = Grid("direction", xs, [3100])
g.put(X0, 110.0, 0, 1, "추진방향", side, size=1100)
for (a, e), text in zip(((116.0, 260.5), (264.0, 405.5), (409.0, 553.0)),
                        ("선제적 예방 시스템 고도화", "AI 활용한 제도 확산", "실천적 행동기준 정립")):
    g.put(a, e, 0, 1, text, frame("#ECECEC", top="soft", bottom="soft", hatch="#E0E0E0"), size=1150, bold=True)
block(g, 186.0)

g = Grid("tasks", [X0, 110.0, 116.0, 262.0, 409.0, X1], [3700])
g.put(X0, 110.0, 0, 1, "추진과제", side, size=1100)
tasks = [("전문 인력 중심의 선제적", "이해충돌 관리 거버넌스 확립"), ("AI를 접목한 지능형 상시", "예방·상담 플랫폼 구축"),
         ("현장 밀착형 모의훈련 및", "점검을 통한 이해충돌방지 내재화")]
for i, ((a, e), pair) in enumerate(zip(((116.0, 262.0), (262.0, 409.0), (409.0, X1)), tasks)):
    g.put(a, e, 0, 1, list(pair), frame(bottom="soft", right="dot" if i < 2 else None), size=1100, line=1320)
block(g, 221.5)

# 조직: 기존 (two columns, before → after) and 개선; person icons omitted.
xs = [X0, 110.0, 116.0, 131.7, 183.0, 297.4, 404.6, 413.7, X1]
g = Grid("organisation", xs, [1700, 2500, 2500, 2500])
g.put(X0, 110.0, 0, 4, "조  직", side, size=1100)
g.put(183.0, 297.4, 0, 1, "기  존", frame("#E3E3E3"), size=1100)
g.put(297.4, 404.6, 0, 1, "▶", frame("#F0F0F0"), align="RIGHT", size=900, color=ARROW)
g.put(413.7, X1, 0, 1, "개  선", frame("#8C8C8C"), size=1100, bold=True, color=WHITE)
rows = [("책 임 관", "기획처장 겸무", "변호사로 책임관 전담", ["준법경영실장 선임"]),
        ("전담조직", "윤리준법부 담당", "법무와 분리하여 운영", ["내부통제부 전담"]),
        ("관리조직", "전사적 공통 관리", "중요 관리 조직 지정",
         [("인사부", 1100, False), ("(채용, 승진심사) ", 780, False), ("계약부", 1100, False), ("(수의계약)", 780, False)])]
for r, (role, before, after, improved) in enumerate(rows, 1):
    last = r == 3
    g.put(131.7, 183.0, r, r + 1, role, frame("#EDEDED"), size=1100, bold=True)
    g.put(183.0, 297.4, r, r + 1, before, frame(top="soft" if r == 1 else None, left="soft",
                                                 bottom="soft" if last else "dot"), size=1100)
    g.put(297.4, 404.6, r, r + 1, after, frame(top="soft" if r == 1 else None, bottom="strong"), size=1100)
    g.put(413.7, X1, r, r + 1, [improved] if isinstance(improved[0], tuple) else improved,
          frame("#F2F2F2", top="mid" if r == 1 else None, left="mid", right="mid", bottom="mid" if last else "dot"),
          size=1100)
block(g, 264.5)

g = Grid("channels", [X0, 110.0, 114.6, 256.0, 264.6, 406.0, 414.0, X1], [3400])
g.put(X0, 110.0, 0, 1, "운영채널", side, size=1100)
for a, e, text in ((114.6, 256.0, "이해충돌방지 자문위원회"), (264.6, 406.0, "이해충돌방지 상담"),
                   (414.0, X1, "신고채널(K-휘슬)")):
    g.put(a, e, 0, 1, text, frame("#6E6E6E"), size=1200, bold=True, color=WHITE)
block(g, 363.5)

xs = [X0, 110.0, 114.6, 154.6, 332.6, 338.3, 379.0, X1]
g = Grid("share", xs, [2250, 250, 4150])
g.put(X0, 110.0, 0, 3, "확산·공유", side, size=1100)
for a, b, e, badge, title, bullets in (
        (114.6, 154.6, 332.6, "내 부", "이해충돌방지 전담조직",
         ["·유권해석 사례집 배포, 공모전 시행 및 제도 홍보", "·사례 중심 교육 및 직급별 맞춤형 교육"]),
        (338.3, 379.0, X1, "외 부", "빛가람 이해충돌방지 네트워크",
         [[("·빛가람혁신도시 이전 공공기관", 1100, False), ("(16개 기관)", 850, False)],
          "·최신사례 공유 및 공동 대응 체계 구축"])):
    g.put(a, b, 0, 1, badge, frame("#6E6E6E", top="soft"), size=1100, bold=True, color=WHITE)
    g.put(b, e, 0, 1, title, frame(top="soft"), align="LEFT", size=1150)
    g.put(a, e, 2, 3, bullets, frame("#EFEFEF"), align="LEFT", size=1100, line=1400)
block(g, 404.5)

# ---------------------------------------------------------------------------
# Section 2 (text layer)
# ---------------------------------------------------------------------------
section_band("sec2", line1(60, 70, 488, 492), line1(90, 95, 490, 493), 487.8)
boxed("background", line1(65, 70, 528, 532), lines_in(115, 120, 520, 552), 517.1, 3710)

g = Grid("thesis", [X0, X1], [1430, 1150])
g.put(X0, X1, 0, 1, [runs_of(line1(128, 132, 559, 563)) + [(" → ", 1090, True, INK)]
                     + runs_of(line1(350, 355, 559, 563))], line=1260)
g.put(X0, X1, 1, 2, [line1(120, 125, 574, 578)], line=980)
block(g, 559.8)

g = Grid("thesis-arrow", [X0, X1], [1150])
g.put(X0, X1, 0, 1, "▼", frame("#F2F2F2"), size=900, color=ARROW, line=980)
block(g, 588.4)

# Three measure columns: pill + subtitle, hatched body, chevron, result band.
xs = [X0, 78.9, 197.9, 220.6, 224.3, 246.5, 365.6, 388.3, 392.0, 414.2, 533.2, X1]
g = Grid("measures", xs, [1850, 1940, 8440, 660, 2340])
cols = ((X0, 78.9, 197.9, 220.6, 80), (224.3, 246.5, 365.6, 388.3, 250), (392.0, 414.2, 533.2, X1, 410))
for a, b, c, e, x in cols:
    g.put(a, b, 0, 1, [], frame(top="mid"))
    g.put(b, c, 0, 1, [runs_of(line1(b, c, 608, 612), WHITE)],
          frame("#7F7F7F", top="mid"), line=1250)
    g.put(c, e, 0, 1, [], frame(top="mid"))
    g.put(a, e, 1, 2, [line1(a, e, 625, 630)])
    g.put(a, e, 2, 3, hang(lines_in(a, a + 15, 645, 725)), frame("#EEEEEE", hatch="#E2E2E2"), align="LEFT",
          line=1500)
    g.put(a, e, 3, 4, "▼", frame("#EEEEEE"), size=600, color="#9A9A9A", line=480)
    g.put(a, e, 4, 5, [line1(a, e, 738, 742)], frame("#DCDCDC"))
block(g, 606.3)

# 주요성과: second line starts with an inline dark badge (한국감사협회).
g = Grid("result", [X0, 111.7, 125.0, 185.6, X1], [1800, 1910])
res1, res2 = line1(115, 120, 767, 771), line1(115, 120, 783, 787)
g.put(X0, 111.7, 0, 2, [runs_of(line1(65, 70, 776, 780), WHITE)], frame("#6A6A6A", top="mid", bottom="mid", left="mid"))
g.put(111.7, X1, 0, 1, [res1], frame(top="mid", right="mid"), align="LEFT")
g.put(111.7, 125.0, 1, 2, [runs_of(res2, x1=124.0)], frame(bottom="mid"), align="LEFT")
g.put(125.0, 185.6, 1, 2, [runs_of(res2, WHITE, x0=124.0, x1=186.0)], frame("#5E5E5E", bottom="mid"))
g.put(185.6, X1, 1, 2, [strip_runs(runs_of(res2, x0=186.0))], frame(bottom="mid", right="mid"), align="LEFT")
block(g, 765.0)

kit.finish(target, end=803.0)
