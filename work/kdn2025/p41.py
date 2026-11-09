"""Rebuild KDN 2025 report physical PDF page 41 (printed page 26) as editable HWPX.

Usage: python3 work/kdn2025/p41.py <report.pdf> <out.hwpx> [--page N]

윤리경영 평가내용 02, sections 3 and 4. Built with the shared diagram kit (one flat table per
horizontal band on a grid of PDF x edges); all text comes from the PDF text layer. Images:
the QR code + chatbot mascot and the webtoon sample are empty photo cells; the 'NEW 신규' and
'지적사항 개선' stickers, the side tab and the section number bands are typed; the ➡ arrows
drawn as images become → / ▶ / ▼ glyphs.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kit  # noqa: E402
from kit import Layout, recipe_inputs  # noqa: E402

source, target = recipe_inputs(41, "AI 기반의 24시간 상시 이해충돌 예방")
L = Layout(top=3100)
kit.setup(source, L)
from kit import *  # noqa: E402,F401,F403  helpers and presets bound to this page

DARK, LABEL = "#6A6A6A", "#E6E6E6"


def hang(lines, base, prefix=None):
    """Bullet lines keep their PDF indent: spaces for the x offset and for the line's own lead."""
    out = []
    for l in lines:
        runs = runs_of(l)
        size = runs[0][1] / 100
        raw = "".join(s["text"] for s in l["spans"])
        offset = l["bbox"][0] - base + (len(raw) - len(raw.lstrip(" "))) * 0.29 * size
        n = max(0, round(offset / (0.29 * size)))
        lead = (prefix or {}).get(l["text"], "")
        if n or lead:
            runs = [(" " * n + lead, runs[0][1], False, INK)] + runs
        out.append(runs)
    return out


def section_band(name, num_line, title_line, top):
    """'3 | heading' band: dark number cell and light gray title cell (images in the PDF)."""
    g = Grid(name, [X0, 84.5, X1], [2300])
    g.put(X0, 84.5, 0, 1, [runs_of(num_line, WHITE)], frame(DARK), line=1700)
    g.put(84.5, X1, 0, 1, [runs_of(title_line)], frame(LABEL), align="LEFT", line=1700)
    block(g, top)


def boxed(name, label_line, body_lines, top, height, label_fill="#D5D5D5", label_color=INK):
    """추진배경 / 주요성과 box: label at left, outlined body with bullet lines."""
    g = Grid(name, [X0, 111.7, X1], [height])
    g.put(X0, 111.7, 0, 1, [runs_of(label_line, label_color)],
          frame(label_fill, top="mid", bottom="mid", left="mid"))
    g.put(111.7, X1, 0, 1, body_lines, frame(top="mid", bottom="mid", right="mid"), align="LEFT")
    block(g, top)


def sticker(text):
    """'NEW 신규' / '지적사항 개선' stickers are images; typed as a small dark tag."""
    return [[(w, s, True, WHITE) for w, s in text]]


def titled(name, line, edges, top, tag):
    """'가. [badge] title [sticker]': number, light pill badge, 14pt title and a dark tag."""
    runs = runs_of(line)
    g = Grid(name, edges, [1650])
    g.put(edges[0], edges[1], 0, 1, [strip_runs(runs[:1])], align="LEFT", line=1450)
    g.put(edges[1], edges[2], 0, 1, [runs[1]], pill)
    g.put(edges[2], edges[3], 0, 1, [strip_runs(runs[2:])], align="LEFT", line=1450)
    g.put(edges[3] + 1.0, edges[4], 0, 1, sticker(tag), frame("#3C3C3C"), line=1000)
    block(g, top)


# ---------------------------------------------------------------------------
# Page chrome (odd page): running head over a rule, side tab, footer at the right.
# ---------------------------------------------------------------------------
L.add_table([[cell(0, 3350, 1680, [para([("01", 1380, True, WHITE)], "CENTER")[0]], dark)],
             [cell(0, 3350, 5960, [para([(ch, 950, True, INK)], "CENTER", 1160)[0] for ch in "경영관리"], gray2)]],
            floating=(57800, 15000))
foot = [(only_text, size, False, INK) for only_text, size in (
    (line1(450, 455, 818, 822)["text"], 790), ("    ", 790), (line1(540, 552, 816, 820)["text"], 1090))]
L.add_table([[cell(0, W, 1500, [para(foot, "RIGHT", 1300)[0]])]], floating=(5660, 81550))

g = Grid("head", [X0, 468.0, X1], [1680])
g.put(X0, 468.0, 0, 1, [], frame(bottom="soft"))
g.put(468.0, X1, 0, 1, [line1(465, 480, 35, 40)], align="RIGHT")
block(g, 32.0)

# ---------------------------------------------------------------------------
# 3. AI 기반의 24시간 상시 이해충돌 예방·상담 플랫폼 가동
# ---------------------------------------------------------------------------
section_band("sec3", line1(60, 70, 72, 76), line1(90, 95, 73, 77), 70.9)
boxed("background", line1(65, 70, 111, 115), lines_in(115, 120, 103, 135), 100.2, 3710)

titled("title-ga", line1(55, 60, 148, 152), [X0, 76.9, 128.8, 434.0, 468.0, X1], 148.4,
       [("NEW ", 560), ("신규", 880)])

# 기존 → 개선 boxes; the QR code / chatbot mascot illustration is a photo cell.
xs = [X0, 62.6, 82.8, 228.5, 242.4, 313.7, 332.5, 445.8, 552.6, X1]
g = Grid("anonymous", xs, [2160, 9920])
head = line1(60, 70, 174, 178)
g.put(X0, 62.6, 0, 1, [], frame("#E4E4E4", top="mid", left="mid"))
g.put(62.6, 82.8, 0, 1, [runs_of(head, x1=82.0)], frame(WHITE, top="soft", bottom="soft", left="soft", right="soft"))
g.put(82.8, 228.5, 0, 1, [runs_of(head, x0=82.0)], frame("#E4E4E4", top="mid", right="mid"), align="LEFT")
head = line1(310, 320, 174, 178)
g.put(242.4, 313.7, 0, 1, [], frame("#7A7A7A", top="mid", left="mid"))
g.put(313.7, 332.5, 0, 1, [runs_of(head, WHITE, x1=334.0)], frame("#333333"))
g.put(332.5, X1, 0, 1, [runs_of(head, WHITE, x0=334.0)], frame("#7A7A7A", top="mid", right="mid"), align="LEFT")
arrow_lines = {l["text"] for l in lines_in(60, 65, 233, 282) if not l["text"].startswith("∙")}
g.put(X0, 228.5, 1, 2, hang(lines_in(60, 75, 200, 282), 62.5, {t: "→ " for t in arrow_lines}),
      frame(left="mid", right="mid", bottom="mid"), align="LEFT", line=1650)
g.put(228.5, 242.4, 0, 2, "▶", size=1300, color=ARROW)
g.put(242.4, 445.8, 1, 2, hang(lines_in(245, 265, 195, 287), 248.3), frame(left="mid", bottom="mid"),
      align="LEFT", line=1540)
g.put(445.8, 552.6, 1, 2, [], photo)
g.put(552.6, X1, 1, 2, [], frame(right="mid", bottom="mid"))
block(g, 171.2)

# ---------------------------------------------------------------------------
# 나. 사내망 전용 Platform: three cards with a result band.
# ---------------------------------------------------------------------------
titled("title-na", line1(55, 60, 303, 307), [X0, 76.9, 128.8, 487.0, 521.0, X1], 303.2,
       [("NEW ", 560), ("신규", 880)])
cols = ((X0, 221.3, 62.5), (223.9, 388.6, 229.7), (391.1, X1, 397.0))
xs = [X0, 221.3, 223.9, 388.6, 391.1, X1]
g = Grid("platform", xs, [2310, 7040, 600, 2120])
side = dict(left="mid", right="mid")
for a, e, base in cols:
    g.put(a, e, 0, 1, [line1(a, e, 328, 332)], frame(top="mid", bottom="soft", **side))
    g.put(a, e, 1, 2, hang(lines_in(a, a + 25, 350, 418), base), frame(**side), align="LEFT", line=1650)
    g.put(a, e, 2, 3, "▼", frame(**side), size=560, color="#9A9A9A", line=440)
    g.put(a, e, 3, 4, [line1(a, e, 426, 430)], frame("#DEDEDE", bottom="mid", **side))
block(g, 325.9)

# ---------------------------------------------------------------------------
# 다. 생성형 AI 웹툰: 추진노력 flow (left stack → middle) and 추진성과 bullets.
# ---------------------------------------------------------------------------
titled("title-da", line1(55, 60, 457, 461), [X0, 76.9, 117.4, 490.0, 545.0, X1], 457.8,
       [("지적사항 개선", 760)])
xs = [X0, 61.0, 191.3, 209.0, 240.5, 297.5, 303.1, 305.6, 328.7, 373.5, 377.2, 391.1, X1]
hs = [2150, 500, 1350, 2420, 1140, 1060, 1170, 1130, 2230, 830]
g = Grid("webtoon", xs, hs)
g.put(X0, 377.2, 0, 1, [line1(190, 200, 483, 487)], frame("#D9D9D9", top="mid", left="mid", right="mid"), bold=True)
g.put(391.1, X1, 0, 1, [runs_of(line1(450, 460, 483, 487), WHITE)], frame("#6A6A6A", top="mid", left="mid", right="mid"))
g.put(X0, 61.0, 1, 10, [], frame(left="mid", bottom="mid"))
g.put(373.5, 377.2, 1, 10, [], frame(right="mid", bottom="mid"))
box = frame(WHITE, top="soft", bottom="soft", left="soft", right="soft")
g.put(61.0, 191.3, 1, 2, [], frame())
g.put(61.0, 191.3, 2, 4, lines_in(60, 110, 511, 530), box, line=1430)
g.put(61.0, 191.3, 4, 5, "▼", size=700, color="#9A9A9A", line=700)
g.put(61.0, 191.3, 5, 7, [line1(60, 75, 560, 564)], box)
g.put(61.0, 191.3, 7, 8, "▼", size=700, color="#9A9A9A", line=700)
g.put(61.0, 191.3, 8, 9, [line1(60, 75, 594, 598)], box)
g.put(61.0, 373.5, 9, 10, [], frame(bottom="mid"))
g.put(191.3, 209.0, 3, 8, "▶", size=1100, color=ARROW)
pills = line1(210, 220, 503, 507)
g.put(209.0, 240.5, 1, 3, [runs_of(pills, x1=240.0)],
      frame(WHITE, top="soft", bottom="soft", left="soft", right="soft"))
g.put(240.5, 297.5, 1, 3, [runs_of(pills, x0=240.0, x1=300.0) + [("→", 1000, True, "#555555")]])
g.put(297.5, 328.7, 1, 3, [runs_of(pills, WHITE, x0=300.0, x1=325.0)], frame("#5E5E5E"))
g.put(328.7, 373.5, 1, 3, [strip_runs(runs_of(pills, x0=325.0))], align="LEFT")
hatched = frame("#EAEAEA", hatch="#DEDEDE")
g.put(209.0, 303.1, 3, 6, lines_in(215, 225, 530, 560), hatched)
g.put(209.0, 303.1, 6, 9, lines_in(215, 230, 578, 608), hatched)
g.put(305.6, 373.5, 3, 9, [], photo)
g.put(377.2, 391.1, 3, 7, "▶", size=1100, color=ARROW)
g.put(391.1, X1, 1, 4, hang(lines_in(395, 410, 502, 542), 397.0), frame(left="mid", right="mid", bottom="soft"),
      align="LEFT", line=1330)
g.put(391.1, X1, 4, 8, hang(lines_in(395, 410, 545, 586), 397.0), frame(left="mid", right="mid", bottom="soft"),
      align="LEFT", line=1360)
g.put(391.1, X1, 8, 10, hang(lines_in(395, 410, 589, 618), 397.0), frame(left="mid", right="mid", bottom="mid"),
      align="LEFT", line=1430)
block(g, 480.5)

# ---------------------------------------------------------------------------
# 4. 실전형 모의훈련 및 취약분야 집중 점검
# ---------------------------------------------------------------------------
section_band("sec4", line1(60, 70, 638, 642), line1(90, 95, 639, 642), 636.6)
cols = ((X0, 105.9, 170.9, 220.6, 59.7), (224.3, 273.6, 338.6, 388.3, 227.3), (392.0, 441.2, 506.2, X1, 395.0))
xs = [X0, 105.9, 170.9, 220.6, 224.3, 273.6, 338.6, 388.3, 392.0, 441.2, 506.2, X1]
g = Grid("training", xs, [310, 1950, 7000])
body = frame("#EEEEEE", hatch="#E2E2E2")
for a, b, c, e, base in cols:
    g.put(a, b, 0, 1, [], frame("#CFCFCF"))
    g.put(b, c, 0, 1, [], frame("#3C3C3C"))
    g.put(c, e, 0, 1, [], frame("#CFCFCF"))
    g.put(a, e, 1, 2, [line1(a, e, 671, 675)], bold=True)
    g.put(a, e, 2, 3, hang(lines_in(a, a + 15, 690, 756), base), body, align="LEFT", line=1650)
block(g, 665.9)

boxed("result", line1(65, 70, 776, 780), lines_in(115, 120, 767, 800), 764.6, 3710,
      label_fill="#6A6A6A", label_color=WHITE)

kit.finish(target, end=803.0)
