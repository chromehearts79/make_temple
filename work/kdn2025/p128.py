"""Rebuild KDN 2025 report page 128 (3rd PDF local page 28, printed page 88) as editable HWPX.

Usage: python3 work/kdn2025/p128.py <report3.pdf> <out.hwpx> [--page 28]

조직 및 인적자원관리, section 3 "평가제도 환류 강화를 통한 성과 향상 및 평가 수용성 제고" (가. 조직평가:
의견수렴 절차 / 결과, 성과도약 조직 지원; 나. 인사평가 table, 다면평가 4단계). Built with the shared kit
(one flat table per band on a grid of PDF x and y edges). Words come from the PDF text layer except
the 다면평가 4단계 diagram (y 649-759), which is one image: its text was read from 4x / 8x renders and
typed into cells (tabs, titles, gray / dark label cells and their two-line texts).

Other images: PART box, section band, footer logo (typed "한전KDN㈜"), the □ check boxes before the
sub-headings (-> '□' runs), the round arrow badges between the 수렴절차 steps and the chevrons
(-> ▶ / ▼), the 지적사항 개선 stickers (hand icon dropped -> dark tag cells).
Printed as in the source: "인사 인계" (4단계 label, probably 연계), "특성 ･장단점" and "강 ･약점" spacing.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kit  # noqa: E402
from kit import Layout, recipe_inputs  # noqa: E402

source, target = recipe_inputs(28, "평가제도 환류 강화를 통한 성과 향상")
L = Layout(top=3100)
kit.setup(source, L)
from kit import *  # noqa: E402,F401,F403  helpers and presets bound to this page

DARK, LABEL, HEAD = "#6A6A6A", "#E3E3E3", "#DCDCDC"
BOX = frame(WHITE, top="soft", bottom="soft", left="soft", right="soft")
TAG = frame("#3C3C3C")


def S(text, size=1090, bold=False, color=INK):
    return (text, size, bold, color)


def band(name, xs, ys):
    g = Grid(name, xs, [int(round((b - a) * 100)) for a, b in zip(ys, ys[1:])])
    g.ys = ys
    return g


def P(g, x0, x1, y0, y1, content, fill="1", pad=None, **kw):
    if pad is not None and kw.get("fit", True) and isinstance(content, list) and content:
        inner = ((x1 - x0) * 100 - 2 * pad - 60) / 100
        ratio = kw.pop("ratio", 90)
        for runs in content:
            need = text_width(runs, ratio)
            if need > inner:
                ratio = int(ratio * inner / need)
        kw.update(fit=False, ratio=ratio)
    g.put(x0, x1, g.ys.index(y0), g.ys.index(y1), content, fill, **kw)
    if pad is not None:
        key = (g.ys.index(y0), g.xs.index(to_x(x0)))
        item = g.items[key]
        g.items[key] = (*item[:7], dict(left=pad, right=pad, top=20, bottom=20))


def one(y, x0):
    return line1(x0 - 1, x0 + 3, y - 1, y + 2)


def part(line, x0=-1e9, x1=1e9, color=INK):
    return strip_runs(runs_of(line, color, x0=x0, x1=x1))


def indent(line, base):
    runs = runs_of(line)
    n = round((line["bbox"][0] - base) / (0.29 * runs[-1][1] / 100))
    return [S(" " * n, runs[-1][1])] + runs if n > 0 else runs


def sub_heading(name, top, y, x0, pill=None, badge=None):
    """'□ [pill] title' sub-heading; the box is an image (typed □)."""
    line = one(y, x0)
    box = S("□ ", 1350, False)
    if pill:
        g = band(name, [X0, 68.5, 128.5, X1], [0, 18.0])
        P(g, X0, 68.5, 0, 18.0, [[S("□", 1300)]], align="LEFT", line=1500, pad=0, fit=False)
        g.put(68.5, 128.5, 0, 1, [part(line, x1=125)], frame(LABEL), line=1250)
        g.put(128.5, X1, 0, 1, [part(line, x0=125)], align="LEFT", line=1500)
    else:
        xs = [X0, badge[0], badge[1], X1] if badge else [X0, X1]
        g = Grid(name, xs, [1800])
        g.put(X0, xs[1], 0, 1, [[box] + runs_of(line)], align="LEFT", line=1500)
        if badge:
            g.put(badge[0], badge[1], 0, 1, "지적사항 개선", TAG, size=800, bold=True, color=WHITE, line=950)
    block(g, top)


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

g = Grid("sec3", [X0, 84.5, X1], [2300])
g.put(X0, 84.5, 0, 1, [runs_of(line1(60, 70, 72, 77), WHITE)], frame(DARK), line=1700)
g.put(84.5, X1, 0, 1, [line1(90, 95, 73, 78)], frame("#E6E6E6"), align="LEFT", line=1700)
block(g, 70.9)

# 가. [조직평가] title
num, line = one(103.1, 56.7), one(103.1, 87.0)
g = Grid("title-ga", [X0, 78.0, 133.0, X1], [1650])
g.put(X0, 78.0, 0, 1, [num], align="LEFT", line=1450)
g.put(78.0, 133.0, 0, 1, [part(line, x1=130)], frame(LABEL), line=1250)
g.put(133.0, X1, 0, 1, [part(line, x0=130)], align="LEFT", line=1450)
block(g, 102.0)

sub_heading("sub-1", 122.5, 124.7, 70.1)

# 수렴절차: four steps (pill + title heads joined by arrow badges), bodies with dotted separators.
heads = ((79.5, 96.4, 124.7, 199.1), (214.5, 220.9, 249.3, 317.1), (334.1, 339.8, 368.2, 435.2),
         (452.3, 455.9, 484.3, X1))
bodies = ((79.5, 199.1, 85.2), (199.1, 318.6, 204.6), (318.6, 438.0, 324.1), (438.0, X1, 443.5))
xs = sorted({X0, 79.5} | {x for h in heads for x in h} | {x for b in bodies for x in b[:2]})
ys = [145.0, 163.7, 200.5, 203.4]
g = band("procedure", xs, ys)
P(g, X0, 79.5, 145.0, 203.4, [runs_of(l) for l in lines_in(60, 75, 150, 202)], frame("#D9D9D9"), line=1180)
step_fill = frame("#E6E6E6")
for k, (a, p0, p1, e) in enumerate(heads):
    head = one(148.8, {0: 100.5, 1: 225.1, 2: 343.9, 3: 460.0}[k])
    P(g, a, p0, 145.0, 163.7, [], step_fill)
    P(g, p0, p1, 145.0, 163.7, [part(head, x1=p1 - 2)], BOX, pad=0, fit=False, line=1000)
    P(g, p1, e, 145.0, 163.7, [part(head, x0=p1 - 2)], step_fill, align="LEFT")
    if k < 3:
        P(g, e, heads[k + 1][0], 145.0, 163.7, "▶", step_fill, size=800, color="#7A7A7A", fit=False)
for k, (a, e, base) in enumerate(bodies):
    sep = dict(left="dot") if k else {}
    P(g, a, e, 163.7, 200.5, [indent(l, base) for l in lines_in(a + 3, e, 167, 198)], frame(**sep), align="LEFT",
      line=1530)
    P(g, a, e, 200.5, 203.4, [], frame(bottom="soft"))
block(g, 145.0)

g = Grid("procedure-arrow", [X0, 294.7, 317.7, X1], [1260])
g.put(294.7, 317.7, 0, 1, "▼", size=1200, color="#9A9A9A", line=1100)
block(g, 204.5)

# 수렴결과: 주요의견 ▶ 제도개선
xs = [X0, 79.5, 82.5, 312.5, 326.0, X1]
ys = [219.0, 237.0, 276.5]
g = band("result-opinion", xs, ys)
P(g, X0, 79.5, 219.0, 276.5, [runs_of(l) for l in lines_in(60, 75, 224, 274)], frame("#D9D9D9"), line=1150)
P(g, 82.5, 312.5, 219.0, 237.0, [one(223.3, 178.5)], frame(HEAD, top="mid", left="mid", right="mid"))
P(g, 82.5, 312.5, 237.0, 276.5, lines_in(87, 90, 242, 262), frame(left="mid", right="mid", bottom="mid"),
  align="LEFT", line=1530)
P(g, 312.5, 326.0, 237.0, 276.5, "▶", size=1100, color="#BDBDBD", fit=False)
P(g, 326.0, X1, 219.0, 237.0, [runs_of(one(223.3, 422.3), WHITE)], frame("#7A7A7A", top="mid", left="mid",
                                                                          right="mid"))
P(g, 326.0, X1, 237.0, 276.5, lines_in(331, 334, 242, 262), frame(left="mid", right="mid", bottom="mid"),
  align="LEFT", line=1530)
block(g, 219.0)

sub_heading("sub-2", 285.0, 286.6, 70.1, badge=(380.5, 433.0))

# 선정기준: 기존 ▶ 개선
xs = [X0, 105.4, 109.0, 134.9, 297.5, 313.0, 316.0, 340.4, X1]
g = Grid("criteria", xs, [2610])
g.put(X0, 105.4, 0, 1, [one(314.1, 61.3)], frame("#D9D9D9", top="dot"))
old, new = one(314.1, 111.2), one(314.1, 316.7)
g.put(109.0, 134.9, 0, 1, [part(old, x1=135)], frame("#D0D0D0", top="mid", bottom="mid", left="mid"), fit=False)
g.put(134.9, 297.5, 0, 1, [part(old, x0=135)], frame(top="mid", bottom="mid", right="mid"), align="LEFT")
g.put(297.5, 313.0, 0, 1, "▶", size=1000, color="#BDBDBD", fit=False)
g.put(313.0, 340.4, 0, 1, [part(new, x1=340, color=WHITE)], frame("#7A7A7A", top="mid", bottom="mid", left="mid"),
      fit=False)
g.put(340.4, X1, 0, 1, [part(new, x0=340)], frame(top="mid", bottom="mid", right="mid"), align="LEFT")
block(g, 306.8)

# 지원내용: two boxes (white head, gray body)
xs = [X0, 105.4, 108.0, 330.5, 333.5, X1]
ys = [338.0, 356.3, 398.5]
g = band("support", xs, ys)
P(g, X0, 105.4, 338.0, 398.5, [one(362.3, 61.3)], frame("#D9D9D9", top="dot"))
for a, e, hx, bx in ((108.0, 330.5, 174.4, 113.5), (333.5, X1, 382.9, 338.9)):
    P(g, a, e, 338.0, 356.3, [one(343.1, hx)], frame(top="mid", left="mid", right="mid"))
    P(g, a, e, 356.3, 398.5, lines_in(bx - 1, bx + 3, 362, 384), frame("#ECECEC", left="mid", right="mid",
                                                                        bottom="mid"), align="LEFT", line=1540)
block(g, 338.0)

# ---------------------------------------------------------------------------
# 나. 인사평가 table
# ---------------------------------------------------------------------------
g = Grid("title-na", [X0, X1], [1650])
g.put(X0, X1, 0, 1, [one(409.0, 56.7)], align="LEFT", line=1450)
block(g, 408.5)

sub_heading("sub-3", 430.0, 431.8, 79.9, pill=True)

xs = [X0, 70.4, 122.5, 134.0, 140.3, 256.9, 260.9, 272.3, 276.4, 407.1, 415.0, 417.0, X1]
ys = [452.5, 470.5, 522.5, 559.5, 579.5, 596.5, 614.5, 618.5]
g = band("hr-table", xs, ys)
P(g, X0, 134.0, 452.5, 470.5, [one(456.8, 83.3)], frame(HEAD, top="mid", left="mid", right="soft"))
P(g, 134.0, 415.0, 452.5, 470.5, [one(456.8, 242.8)], frame(HEAD, top="mid", right="mid"))
P(g, 417.0, X1, 452.5, 470.5, [runs_of(one(456.8, 466.1), WHITE)], frame("#7A7A7A", top="mid", left="mid", right="mid"))
rows = ((470.5, 522.5, (476, 512), (475, 506), (475, 519)),
        (522.5, 559.5, (527, 556), (527, 556), (527, 556)))
for y0, y1, (ly0, ly1), (cy0, cy1), (ry0, ry1) in rows:
    P(g, X0, 134.0, y0, y1, lines_in(58, 80, ly0, ly1), frame(left="mid", right="soft", bottom="dot"), line=1430)
    P(g, 134.0, 415.0, y0, y1, lines_in(138, 141, cy0, cy1 + 2), frame(right="mid", bottom="dot"), align="LEFT",
      line=1430)
    P(g, 417.0, X1, y0, y1, [indent(l, 422.6) for l in lines_in(421, 432, ry0, ry1)],
      frame(left="mid", right="mid", bottom="dot"), align="LEFT", line=1300)
# 긴급현안대응 조직: label + sticker, bullet, two-step model, results
P(g, X0, 134.0, 559.5, 596.5, lines_in(58, 70, 567, 586), frame(left="mid", right="soft"), line=1430)
P(g, X0, 70.4, 596.5, 618.5, [], frame(left="mid", bottom="mid"))
P(g, 70.4, 122.5, 596.5, 614.5, "지적사항 개선", TAG, size=760, bold=True, color=WHITE, line=900)
P(g, 70.4, 122.5, 614.5, 618.5, [], frame(bottom="mid"))
P(g, 122.5, 134.0, 596.5, 618.5, [], frame(right="soft", bottom="mid"))
P(g, 134.0, 415.0, 559.5, 579.5, [one(564.7, 139.1)], frame(right="mid"), align="LEFT", line=1300)
P(g, 134.0, 140.3, 579.5, 618.5, [], frame(bottom="mid"))
for a, e, hx, bx in ((140.3, 256.9, 141.2, 143.4), (276.4, 407.1, 291.4, 279.4)):
    P(g, a, e, 579.5, 596.5, [one(583.7, hx)], frame("#E3E3E3", top="soft", left="soft", right="soft"), line=1150)
    P(g, a, e, 596.5, 614.5, [one(598.7, bx)], frame(left="soft", right="soft", bottom="soft"), line=1200)
    P(g, a, e, 614.5, 618.5, [], frame(bottom="mid"))
P(g, 256.9, 276.4, 579.5, 614.5, "▶", size=1000, color="#BDBDBD", fit=False)
P(g, 256.9, 276.4, 614.5, 618.5, [], frame(bottom="mid"))
P(g, 407.1, 415.0, 579.5, 618.5, [], frame(right="mid", bottom="mid"))
P(g, 417.0, X1, 559.5, 618.5, lines_in(421, 425, 574, 604), frame(left="mid", right="mid", bottom="mid"),
  align="LEFT", line=1430)
block(g, 452.5)

sub_heading("sub-4", 627.0, 628.9, 79.9, pill=True)

# ---------------------------------------------------------------------------
# 다면평가 4단계 (image; typed)
# ---------------------------------------------------------------------------
cols = ((X0, 65.0, 93.0, 190.5), (190.5, 191.5, 218.5, 321.5), (321.5, 322.5, 350.0, 443.5),
        (443.5, 444.5, 472.0, X1))
tabs = ((X0, 176.0, frame("#E9E9E9", hatch="#D6D6D6"), INK), (183.5, 302.0, frame("#D9D9D9"), INK),
        (315.0, 433.5, frame("#B4B4B4"), INK), (436.0, X1, frame("#7A7A7A"), WHITE))
xs = sorted({x for c in cols for x in c} | {x for t in tabs for x in t[:2]})
ys = [649.5, 666.0, 687.0, 722.0, 725.5, 758.5]
g = band("multi-rater", xs, ys)
stages = (("1단계", ("입체적 진단", "(Diagnosis)"),
           (["역량", "평가"], [[S("2직급 보직자 대상", 1050)], [S("역량평가 최초 시행", 1050), S("(9월)", 820)]]),
           (["리더십", "평가"], [[S("서술형", 1050), S("(강·약점)", 820), S(" 평가", 1050)],
                               [S("항목 신설", 1050), S("(10월)", 820)]])),
          ("2단계", ("객관적 인식", "(Feedback)"),
           (["환류"], [[S("전문기관이 분석한 개인별", 1050)], [S("리포트 제공", 1050), S("(11월)", 820)]]),
           (["자기", "성찰"], [[S("결과 확인을 통한", 1050)], [S("본인 리더십 수준 인지", 1050)]])),
          ("3단계", ("역량 개발", "(Development)"),
           (["행동", "개선"], [[S("개인별 행동 특성 ·장단점", 1050)], [S("제공으로 행동 개선 촉진", 1050)]]),
           (["역량", "강화"], [[S("강 ·약점 진단 결과를", 1050)], [S("반영한 역량 향상 유도", 1050)]])),
          ("4단계", ("성과 창출 및 연계", "(Growth)"),
           (["성과", "창출"], [[S("역량평가 결과에 따른", 1050)], [S("상향보직", 1050), S("(4명)", 820), S(" 부여", 1050)]]),
           (["인사", "인계"], [[S("평가 결과를 승진·보직 등", 1050)], [S("인사 참고자료로 활용", 1050)]])))
for (c0, l0, l1, c1), (t0, t1, tab_fill, tab_color), (name, (title, eng), row_a, row_b) in zip(cols, tabs, stages):
    P(g, t0, t1, 649.5, 666.0, [[S(name, 1150, True, tab_color)]], tab_fill, align="LEFT", line=1300)
    P(g, c0, c1, 666.0, 687.0, [[S(title, 1200, True), S(" " + eng, 950, True)]], frame(left="dot"), align="LEFT",
      line=1400)
    for (y0, y1), (label, text), (lab_fill, lab_color, text_fill) in (
            ((687.0, 722.0), row_a, ("#D2D2D2", INK, frame("#EEEEEE"))),
            ((725.5, 758.5), row_b, ("#7A7A7A", WHITE, "1"))):
        P(g, c0, l0, y0, y1, [], frame(left="dot"))
        P(g, l0, l1, y0, y1, [[S(t, 1050, True, lab_color)] for t in label], frame(lab_fill), line=1250, pad=20)
        P(g, l1, c1, y0, y1, text, text_fill, align="LEFT", line=1400, pad=200)
    P(g, c0, c1, 722.0, 725.5, [], frame(left="dot"))
block(g, 649.5)

# 주요성과 (two result lines)
g = Grid("result", [X0, 111.7, 114.5, X1], [3130])
g.put(X0, 111.7, 0, 1, [runs_of(line1(65, 70, 777, 781), WHITE)], frame(DARK))
g.put(114.5, X1, 0, 1, lines_in(115, 120, 766, 790), frame(top="mid", bottom="mid", left="mid", right="mid"),
      align="LEFT", line=1450)
block(g, 768.0)

kit.finish(target, end=801.0)
