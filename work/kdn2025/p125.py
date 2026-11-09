"""Rebuild KDN 2025 report page 125 (3rd PDF local page 25, printed page 85) as editable HWPX.

Usage: python3 work/kdn2025/p125.py <report3.pdf> <out.hwpx> [--page 25]

조직 및 인적자원관리, section 2 "One-Team으로의 역량 극대화를 위한 3대 과제(H.O.T.) 중심 조직 재설계"
(가. Harmony / 나. Optimization / 다. Timely). Built with the shared kit (one flat table per band on a
grid of PDF x edges and y edges). Running text, panel heads, 현안 및 방향성 lines, the right panel of 나.,
the 다. bullets / 국정과제 bars and the 주요성과 lines come from the PDF text layer.

Images and how they are kept:
- side tab, section number band, 'Best Practice' sticker (trophy dropped): typed cells.
- the heavy arrows (➡) inside the 현안 및 방향성 lines and the 조직진단 box -> '→' runs; the grey
  chevrons between the three process boxes -> ▶; the arrows between 기존 / 개편 charts -> →; the
  dotted down arrows between the 국정과제 bars -> ▼.
- the org charts (가. both panels, 나. left panel, 다. right panel) are images: their labels were read
  from 4x-5x renders and typed into cells on the band grid (boxes -> filled / outlined cells, pills
  -> gray cells, connector lines dropped except the 협의회 bar, the '····' link typed as dots).
- 신규 / 상향 boxes (text-layer words in drawn boxes) are separate outlined cells.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kit  # noqa: E402
from kit import Layout, recipe_inputs  # noqa: E402

source, target = recipe_inputs(25, "One-Team으로의 역량 극대화를 위한 3대 과제")
L = Layout(top=3100)
kit.setup(source, L)
from kit import *  # noqa: E402,F401,F403  helpers and presets bound to this page

DARK, LABEL, HEAD = "#6A6A6A", "#E3E3E3", "#DCDCDC"
BOX = frame(WHITE, top="soft", bottom="soft", left="soft", right="soft")
CHIEF = frame("#555555")                     # dark org boxes (사 장, 본부)
PILL = frame("#E3E3E3", top="soft", bottom="soft", left="soft", right="soft")
SUBHEAD = frame("#EDEDED")


def S(text, size=1090, bold=False, color=INK):
    return (text, size, bold, color)


def band(name, xs, ys):
    g = Grid(name, xs, [int(round((b - a) * 100)) for a, b in zip(ys, ys[1:])])
    g.ys = ys
    return g


def P(g, x0, x1, y0, y1, content, fill="1", pad=None, **kw):
    if pad is not None and kw.get("fit", True) and isinstance(content, list) and content:
        # kit's fit assumes the default 5 pt padding; fit to the narrowed padding instead.
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


def arrowed(y0, y1, x0=115):
    """One 현안 line: '∙ issue' (image arrow) 'direction' -> one paragraph with a → run."""
    parts = sorted(lines_in(x0, X1, y0, y1), key=lambda l: l["bbox"][0])
    runs = runs_of(parts[0])
    for part in parts[1:]:
        runs += [S(" → ", 1090, True)] + runs_of(part)
    return runs


def pill_heading(name, top, y, pill, title_x):
    """'가. [Harmony] title': number, hatched gray pill with white text, 14pt title."""
    line = line1(55, 60, y - 1, y + 2)
    g = Grid(name, [X0, 79.5, title_x, X1], [1650])
    g.put(X0, 79.5, 0, 1, [runs_of(line, x1=78)], align="LEFT", line=1450)
    g.put(79.5, title_x, 0, 1, [pill], frame("#A4A4A4", hatch="#BABABA"), line=1350, fit=False)
    g.put(title_x, X1, 0, 1, [strip_runs(runs_of(line, x0=title_x - 1))], align="LEFT", line=1450)
    block(g, top)


def issues(name, top, height, label_y, paras):
    """현안 및 방향성: gray label and an outlined body."""
    g = Grid(name, [X0, 113.6, 117.0, X1], [height])
    g.put(X0, 113.6, 0, 1, [line1(59, 61, label_y - 1, label_y + 2)], frame(LABEL), line=1200)
    g.put(117.0, X1, 0, 1, paras, frame(top="mid", bottom="mid", left="mid", right="mid"), align="LEFT", line=1210)
    block(g, top)


def result(name, top, y):
    g = Grid(name, [X0, 112.0, 114.5, X1], [1650])
    g.put(X0, 112.0, 0, 1, [runs_of(line1(65, 70, y - 1, y + 2), WHITE)], frame(DARK))
    g.put(114.5, X1, 0, 1, lines_in(115, 120, y - 1, y + 2), frame(top="mid", bottom="mid", left="mid", right="mid"),
          align="LEFT", line=1300)
    block(g, top)


def tag(text, dark=False):
    return [S(text, 800, dark, WHITE if dark else INK)]


# ---------------------------------------------------------------------------
# Page chrome (odd page): running head over a rule, side tab, footer at the right.
# ---------------------------------------------------------------------------
L.add_table([[cell(0, 3350, 1680, [para([("01", 1380, True, WHITE)], "CENTER")[0]], dark)],
             [cell(0, 3350, 5960, [para([(ch, 950, True, INK)], "CENTER", 1160)[0] for ch in "경영관리"], gray2)]],
            floating=(57800, 15000))
foot = [(text, size, False, INK) for text, size in (
    (line1(450, 455, 818, 822)["text"], 790), ("    ", 790), (line1(540, 546, 816, 820)["text"], 1090))]
L.add_table([[cell(0, W, 1500, [para(foot, "RIGHT", 1300)[0]])]], floating=(5660, 81550))

g = Grid("head", [X0, 378.5, X1], [1680])
g.put(X0, 378.5, 0, 1, [], frame(bottom="soft"))
g.put(378.5, X1, 0, 1, [line1(380, 385, 35, 40)], align="RIGHT")
block(g, 32.0)

# Section 2 band (image): dark number, light title, 'Best Practice' sticker.
g = Grid("sec2", [X0, 84.5, 480.0, X1], [2300])
g.put(X0, 84.5, 0, 1, [runs_of(line1(60, 70, 72, 77), WHITE)], frame(DARK), line=1700)
g.put(84.5, 480.0, 0, 1, [line1(90, 95, 73, 78)], frame("#E6E6E6"), align="LEFT", line=1700)
g.put(480.0, X1, 0, 1, "Best Practice", frame("#4A4A4A"), size=900, bold=True, color=WHITE)
block(g, 70.9)

# Process: three boxes (white head, gray body) joined by chevrons.
boxes = ((X0, 213.8), (227.6, 384.8), (398.6, X1))
g = Grid("process", [X0, 213.8, 227.6, 384.8, 398.6, X1], [1840, 4850])
for k, (a, e) in enumerate(boxes):
    g.put(a, e, 0, 1, lines_in(a, e, 99, 106), frame(top="mid", left="mid", right="mid", bottom="soft"), line=1250)
    body = lines_in(a, e, 120, 162)
    if k == 0:
        paras = [runs_of(body[0]), [S("  → ", 1090, True)] + runs_of(body[1]), [S("     ")] + runs_of(body[2])]
    else:
        paras = [runs_of(l) for l in body]
    g.put(a, e, 1, 2, paras, frame("#EBEBEB", left="mid", right="mid", bottom="mid"), align="LEFT", line=1270)
    if k < 2:
        g.put(e, boxes[k + 1][0], 1, 2, "▶", size=1300, color="#BDBDBD", fit=False)
block(g, 98.0)

# ---------------------------------------------------------------------------
# 가. Harmony
# ---------------------------------------------------------------------------
pill_heading("title-ga", 176.3, 177.0, [S("H", 1200, True, WHITE), S("armony", 1100, False, WHITE)], 133.5)
issues("issue-ga", 195.9, 3440, 208.3, [arrowed(200, 203), arrowed(213, 216)])

# Panels: 전략실-연구원 org charts (image) | 미래사업전략협의회 chart (image).
xs = [X0, 59.5, 62.5, 77.0, 95.5, 102.0, 113.0, 118.0, 125.0, 169.6, 172.0, 189.0, 192.0, 209.0, 226.5, 231.0,
      237.0, 251.0, 254.0, 299.0, 302.6, 305.0, 307.5, 314.0, 345.0, 376.0, 389.0, 400.5, 452.0, 463.0, 468.0,
      473.0, 487.0, 518.2, 549.5, X1]
ys = [234.0, 251.7, 255.7, 268.7, 271.7, 276.7, 282.2, 285.5, 288.0, 297.0, 300.5, 306.5, 309.0, 311.5, 313.5,
      316.5, 323.5, 326.5, 330.0]
g = band("panels-ga", xs, ys)
for a, e, y in ((X0, 305.0, 238.8), (307.5, X1, 238.9)):
    P(g, a, e, 234.0, 251.7, [line1(a, e, y - 1, y + 2)], frame(HEAD, top="mid", left="mid", right="mid"))
    P(g, a, a + (2.9 if a == X0 else 6.5), 251.7, 326.5, [], frame(left="mid"))
    P(g, e - (2.4 if a == X0 else 6.1), e, 251.7, 326.5, [], frame(right="mid"))
    P(g, a, e, 326.5, 330.0, [], frame(bottom="mid", left="mid", right="mid"))
# 기존: 전략-연구 분리
P(g, 59.5, 77.0, 255.7, 268.7, [], SUBHEAD)
P(g, 77.0, 95.5, 255.7, 268.7, tag("기존"), BOX, pad=20, fit=False, line=900)
P(g, 95.5, 172.0, 255.7, 268.7, [[S("전략-연구 분리", 950, True)]], SUBHEAD, align="LEFT", line=1100)
P(g, 102.0, 125.0, 271.7, 282.2, [[S("사 장", 800, True, WHITE)]], CHIEF, line=850, pad=20)
P(g, 62.5, 113.0, 285.5, 297.0, [[S("지속성장전략실", 760)]], PILL, line=860, pad=30)
P(g, 118.0, 169.6, 297.0, 309.0, [[S("전력지능화안전본부", 750)]], frame("#BDBDBD", top="soft", bottom="soft",
  left="soft", right="soft"), line=850, pad=30)
P(g, 118.0, 169.6, 311.5, 323.5, [[S("전 력 I C T 기 술 원", 800)]], PILL, line=900, pad=30)
P(g, 172.0, 189.0, 268.7, 326.5, "→", size=1200, color="#8A8A8A", fit=False)
# 개편: 전략-연구 연계
P(g, 189.0, 209.0, 255.7, 268.7, [], SUBHEAD)
P(g, 209.0, 226.5, 255.7, 268.7, tag("개편", True), frame("#555555"), pad=20, fit=False, line=900)
P(g, 226.5, 302.6, 255.7, 268.7, [[S("전략-연구 연계", 950, True)]], SUBHEAD, align="LEFT", line=1100)
P(g, 231.0, 254.0, 271.7, 282.2, [[S("사 장", 800, True, WHITE)]], CHIEF, line=850, pad=20)
P(g, 192.0, 237.0, 288.0, 300.5, [[S("미래전략실", 850)]], BOX, line=950, pad=30)
P(g, 237.0, 251.0, 288.0, 300.5, [[S("····", 800, False, "#7A7A7A")]], line=900, pad=0, fit=False)
P(g, 251.0, 299.0, 288.0, 300.5, [[S("전력ICT연구원", 850)]], BOX, line=950, pad=30)
for a, e, items in ((192.0, 237.0, ("전사전략수립", "사업개발", "투자전략 · 심의")),
                    (251.0, 299.0, ("연구개발", "기술개발 · 지원", "개발성과물 관리"))):
    P(g, a, e, 300.5, 326.5, [[S(t, 720)] for t in items], frame("#E6E6E6"), line=790, pad=20)
# 미래사업전략협의회 [신설] and three 협의회 columns
P(g, 389.0, 452.0, 255.7, 268.7, [[S("미래사업전략협의회", 850, True, WHITE)]], CHIEF, line=950, pad=30)
P(g, 452.0, 468.0, 255.7, 268.7, tag("신설"), BOX, pad=10, fit=False, line=900)
P(g, 468.0, 473.0, 255.7, 268.7, [], CHIEF)
P(g, 345.0, 518.2, 271.7, 276.7, [], frame(top="soft"))
cols = (((314.0, 376.0), "보 안 협 의 회", (288.0, 297.0, 306.5, 316.5, 326.5),
         ("보안사업단 · 처", "원발전사업단", "정 보 보 호 실", "사이버안전처")),
        ((400.5, 463.0), "A X 협 의 회", (288.0, 300.5, 313.5, 326.5), ("A X 사 업 처", "원발전사업단", "이외 유관조직")),
        ((487.0, 549.5), "R & D 협 의 회", (288.0, 300.5, 313.5, 326.5), ("전력ICT연구원", "미 래 전 략 실", "관련 사업 조직")))
for (a, e), head, edges, items in cols:
    P(g, a, e, 276.7, 288.0, [[S(head, 850)]], BOX, line=900, pad=30)
    for (y0, y1), text in zip(zip(edges, edges[1:]), items):
        P(g, a, e, y0, y1, [[S(text, 720)]], PILL, line=740, pad=30)
block(g, 234.0)

result("result-ga", 335.8, 338.9)

# ---------------------------------------------------------------------------
# 나. Optimization
# ---------------------------------------------------------------------------
pill_heading("title-na", 366.1, 366.9, [S("O", 1200, True, WHITE), S("ptimization", 1100, False, WHITE)], 147.0)
issues("issue-na", 385.8, 3440, 398.1, [arrowed(390, 392), runs_of(line1(120, 125, 402, 404))])

xs = [X0, 59.5, 62.5, 63.6, 81.0, 95.0, 95.5, 96.0, 99.6, 115.0, 117.0, 132.0, 135.6, 137.0, 168.0, 169.0, 172.0,
      189.0, 191.6, 207.5, 209.0, 223.0, 225.0, 226.0, 227.0, 228.0, 255.5, 261.0, 263.0, 264.0, 265.0, 275.0,
      297.0, 300.4, 302.6, 305.0, 307.5, 311.0, 314.6, 362.9, 365.0, 549.5, X1]
ys = [425.5, 442.0, 446.0, 460.0, 465.0, 476.0, 480.0, 490.0, 495.5, 501.0, 506.5, 509.0, 511.0, 520.0, 526.0,
      536.0, 540.0, 549.0, 559.0, 561.0, 564.5, 567.5]
g = band("panels-na", xs, ys)
for a, e, y in ((X0, 305.0, 428.7), (307.5, X1, 428.7)):
    P(g, a, e, 425.5, 442.0, [line1(a, e, y - 1, y + 2)], frame(HEAD, top="mid", left="mid", right="mid"))
    P(g, a, a + (2.9 if a == X0 else 3.5), 442.0, 564.5, [], frame(left="mid"))
    P(g, e - (2.4 if a == X0 else 6.1), e, 442.0, 564.5, [], frame(right="mid"))
    P(g, a, e, 564.5, 567.5, [], frame(bottom="mid", left="mid", right="mid"))


def subhead(x0, tx0, tx1, x1, y0, y1, word, title, new, size=950):
    P(g, x0, tx0, y0, y1, [], SUBHEAD)
    P(g, tx0, tx1, y0, y1, tag(word, new), frame("#555555") if new else BOX, pad=20, fit=False, line=900)
    P(g, tx1, x1, y0, y1, [[S(title, size, True)]], SUBHEAD, align="LEFT", line=1100)


# 기존 발전사업 총괄 조직 부재 -> 개편 원･발전 컨트롤타워 신설
subhead(59.5, 62.5, 81.0, 172.0, 446.0, 460.0, "기존", "발전사업 총괄 조직 부재", False)
P(g, 95.0, 137.0, 465.0, 476.0, [[S("ICT본부", 800, False, WHITE)]], CHIEF, line=900, pad=20)
for a, e, top in ((63.6, 96.0, "동남발전"), (99.6, 132.0, "서남발전"), (135.6, 169.0, "원전")):
    P(g, a, e, 480.0, 501.0, [[S(top, 760)], [S("사업처", 760)]], frame("#D2D2D2"), line=840, pad=20)
P(g, 172.0, 189.0, 460.0, 501.0, "→", size=1200, color="#8A8A8A", fit=False)
subhead(189.0, 207.5, 225.0, 300.4, 446.0, 460.0, "개편", "원 · 발전 컨트롤타워 신설", True, 860)
P(g, 223.0, 265.0, 465.0, 476.0, [[S("전력ICT본부", 800, False, WHITE)]], CHIEF, line=900, pad=20)
P(g, 191.6, 255.5, 480.0, 490.0, [[S("원발전사업단", 760)]], frame("#D2D2D2"), align="RIGHT", line=800, pad=40)
P(g, 255.5, 275.0, 480.0, 490.0, tag("신설"), frame("#BDBDBD", top="soft", bottom="soft", left="soft", right="soft"),
  pad=10, fit=False, line=800)
P(g, 275.0, 297.0, 480.0, 490.0, [], frame("#D2D2D2"))
for a, e, text in ((191.6, 226.0, "원전사업처"), (227.0, 261.0, "동남발전사업처"), (263.0, 297.0, "서남발전사업처")):
    P(g, a, e, 490.0, 501.0, [[S(text, 720)]], frame("#ECECEC"), line=800, pad=20)
# 기존 보안 사업 기능 산재 -> 개편 보안사업 컨트롤타워 신설
subhead(59.5, 62.5, 81.0, 172.0, 506.5, 520.0, "기존", "보안 사업 기능 산재", False)
P(g, 95.0, 137.0, 526.0, 536.0, [[S("2개 본부 예하", 800, False, WHITE)]], CHIEF, line=840, pad=20)
P(g, 63.6, 115.0, 540.0, 549.0, [[S("ICT본부", 720)]], frame("#D2D2D2"), line=740, pad=20)
P(g, 117.0, 168.0, 540.0, 549.0, [[S("미래사업개발본부", 720)]], frame("#D2D2D2"), line=740, pad=20)
P(g, 63.6, 115.0, 549.0, 559.0, [[S("정보보호실, 사이버안전처", 680)]], frame("#ECECEC"), line=760, pad=10)
P(g, 117.0, 168.0, 549.0, 559.0, [[S("보안사업처", 720)]], frame("#ECECEC"), line=760, pad=20)
P(g, 172.0, 189.0, 520.0, 559.0, "→", size=1200, color="#8A8A8A", fit=False)
subhead(189.0, 207.5, 225.0, 300.4, 506.5, 520.0, "개편", "보안사업 컨트롤타워 신설", True, 860)
P(g, 191.6, 255.5, 526.0, 536.0, [[S("보안사업단", 760)]], frame("#D2D2D2"), align="RIGHT", line=800, pad=40)
P(g, 255.5, 275.0, 526.0, 536.0, tag("신설"), frame("#BDBDBD", top="soft", bottom="soft", left="soft", right="soft"),
  pad=10, fit=False, line=800)
P(g, 275.0, 297.0, 526.0, 536.0, [], frame("#D2D2D2"))
for a, e, top, low in ((191.6, 225.0, "보안", "사업처"), (228.0, 261.0, "정보", "보호실"), (264.0, 297.0, "사이버", "안전처")):
    P(g, a, e, 540.0, 559.0, [[S(top, 760)], [S(low, 760)]], frame("#ECECEC"), line=840, pad=20)
# right panel: two bullet heads, 2 + 2 labelled rows (text layer)
P(g, 311.0, 549.5, 446.0, 460.0, [line1(311, 313, 445, 448)], align="LEFT", line=1230)
P(g, 311.0, 549.5, 495.5, 509.0, [line1(311, 313, 497, 499)], align="LEFT", line=1150)
rows = ((460.0, 476.0, (463, 465), (461, 463), dict(top="soft", bottom="dot")),
        (476.0, 490.0, (480, 482), (475, 477), dict(bottom="soft")),
        (511.0, 536.0, (519, 521), (512, 525), dict(top="soft", bottom="dot")),
        (536.0, 561.0, (544, 546), (538, 551), dict(bottom="soft")))
for y0, y1, (ly0, ly1), (cy0, cy1), edges in rows:
    P(g, 314.6, 362.9, y0, y1, [line1(315, 325, ly0, ly1)], frame("#E3E3E3", **edges))
    P(g, 362.9, 365.0, y0, y1, [], frame(**edges))
    P(g, 365.0, 549.5, y0, y1, lines_in(365, 367, cy0, cy1), frame(**edges), align="LEFT", line=1100)
block(g, 425.5)

result("result-na", 574.0, 577.0)

g = Grid("note", [X0, X1], [1150])
g.put(X0, X1, 0, 1, [line1(55, 60, 596, 600)], align="LEFT", line=990)
block(g, 597.0)

# ---------------------------------------------------------------------------
# 다. Timely
# ---------------------------------------------------------------------------
pill_heading("title-da", 617.0, 617.8, [S("T", 1100, True, WHITE), S("imely", 1100, False, WHITE)], 121.5)
issues("issue-da", 636.7, 4220, 653.0, [arrowed(640, 642), arrowed(652, 654), arrowed(664, 666)])

xs = [X0, 59.5, 156.8, 175.6, 177.7, 196.4, 201.7, 204.6, 206.8, 212.6, 360.1, 365.6, 368.3, 372.0, 380.0,
      395.0, 416.0, 431.0, 438.5, 451.0, 455.0, 471.0, 481.0, 523.5, 548.0, 550.5, X1]
ys = [683.5, 702.0, 705.5, 719.0, 732.5, 737.0, 746.0, 750.0, 755.0, 759.5, 764.0, 768.0, 773.0, 775.5]
g = band("panels-da", xs, ys)
for a, e, y in ((X0, 204.6, 688.1), (206.8, 365.6, 688.1), (368.3, X1, 688.1)):
    P(g, a, e, 683.5, 702.0, [line1(a, e, y - 1, y + 2)], frame(HEAD, top="mid", left="mid", right="mid"))
    P(g, a, e, 773.0, 775.5, [], frame(bottom="mid", left="mid", right="mid"))
P(g, X0, 59.5, 702.0, 773.0, [], frame(left="mid"))
P(g, 201.7, 204.6, 702.0, 773.0, [], frame(right="mid"))
P(g, 206.8, 212.6, 702.0, 773.0, [], frame(left="mid"))
P(g, 360.1, 365.6, 702.0, 773.0, [], frame(right="mid"))
P(g, 368.3, 372.0, 702.0, 773.0, [], frame(left="mid"))
P(g, 550.5, X1, 702.0, 773.0, [], frame(right="mid"))
# left: five bullet lines, 신규 / 상향 tags in their own cells
left = lines_in(60, 72, 705, 762)
assert len(left) == 5


def indent(line, base=62.5):
    runs = runs_of(line)
    n = round((line["bbox"][0] - base) / (0.29 * 10.9))
    return [S(" " * n)] + runs if n > 0 else runs


P(g, 59.5, 201.7, 705.5, 719.0, [indent(left[0])], align="LEFT", line=1180)
P(g, 59.5, 177.7, 719.0, 732.5, [[S(" " * 3)] + runs_of(left[1], x1=179)], align="LEFT", line=1180)
P(g, 177.7, 196.4, 719.0, 732.5, [runs_of(left[1], x0=179)], BOX, line=900, pad=0, fit=False)
P(g, 59.5, 156.8, 732.5, 746.0, [runs_of(left[2], x1=158)], align="LEFT", line=1180)
P(g, 156.8, 175.6, 732.5, 746.0, [runs_of(left[2], x0=158)], BOX, line=900, pad=0, fit=False)
P(g, 59.5, 201.7, 746.0, 759.5, [indent(left[3])], align="LEFT", line=1180)
P(g, 59.5, 201.7, 759.5, 773.0, [indent(left[4])], align="LEFT", line=1180)
# middle: three bars with down arrows
for y0, y1, ty in ((705.5, 719.0, 706.8), (732.5, 746.0, 732.3), (759.5, 773.0, 757.8)):
    P(g, 212.6, 360.1, y0, y1, [line1(212, 362, ty - 1, ty + 2)], frame("#DEDEDE"), line=1050)
for y0, y1 in ((719.0, 732.5), (746.0, 759.5)):
    P(g, 212.6, 360.1, y0, y1, "▼", size=700, color="#9A9A9A", line=800)
# right: 기존 / 개편 safety org charts (image, typed)
P(g, 372.0, 395.0, 705.5, 719.0, [], SUBHEAD)
P(g, 416.0, 438.5, 705.5, 719.0, [], SUBHEAD)
P(g, 395.0, 416.0, 705.5, 719.0, tag("기존"), BOX, pad=10, fit=False, line=900)
P(g, 380.0, 431.0, 719.0, 732.5, [[S("전력지능화안전본부", 760, False, WHITE)]], CHIEF, line=820, pad=20)
P(g, 380.0, 431.0, 737.0, 750.0, [[S("안전관리실", 800)]], PILL, line=900, pad=20)
P(g, 380.0, 431.0, 755.0, 768.0, [[S("산업안전보건부", 800)]], PILL, line=900, pad=20)
P(g, 438.5, 451.0, 737.0, 755.0, "→", size=1100, color="#8A8A8A", fit=False)
P(g, 451.0, 455.0, 705.5, 719.0, [], SUBHEAD)
P(g, 455.0, 471.0, 705.5, 719.0, tag("개편", True), frame("#555555"), pad=10, fit=False, line=900)
P(g, 471.0, 550.5, 705.5, 719.0, [[S("기능중심 조직 세분화", 900, True)]], SUBHEAD, align="LEFT", line=1050)
P(g, 481.0, 523.5, 719.0, 732.5, [[S("사 장", 800, True, WHITE)]], CHIEF, line=850, pad=20)
P(g, 451.0, 548.0, 732.5, 746.0, [[S("안전품질실 : 총괄 조직", 880)]], frame("#ECECEC"), line=950, pad=20)
for y0, y1, text in ((746.0, 755.0, "안전총괄부  : 안전경영 기획"), (755.0, 764.0, "산업안전부  : 안전보건경영 관리"),
                     (764.0, 773.0, "안전혁신TF  : 안전 거버넌스 구축")):
    P(g, 455.0, 548.0, y0, y1, [[S(text, 700)]], PILL, line=720, pad=30)
block(g, 683.5)

result("result-da", 782.3, 785.3)

kit.finish(target, end=801.0)
