"""Rebuild KDN 2025 report PDF page 90 (second PDF local page 40, printed page 60) as editable HWPX.

Usage: python3 work/kdn2025/p90.py <report2.pdf> <out.hwpx> [--page 40]

상생･협력 및 지역발전, section 3 (에너지ICT 동반성장 플랫폼). Built with the shared diagram kit
(one flat table per horizontal band on a grid of PDF x edges); table text comes from the PDF text
layer cell by cell. Images: the section-number band, the '지적사항 개선' stickers, the PART box
and the Synergy-On diagram (y 123-251) are images; the diagram text was read from a 3x render and
typed. The boxed row numbers 1-4 of the first table become ①-④; the rounded gray sub-label pills
and the KDN / 中企 / 기존 / 개선 tags become filled cells; decorative rings and chevrons are dropped
or replaced by a ▼ glyph.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kit  # noqa: E402
from kit import Layout, recipe_inputs  # noqa: E402

source, target = recipe_inputs(40, "에너지ICT 동반성장 플랫폼 기반 상생")
L = Layout(top=3100)
kit.setup(source, L)
from kit import *  # noqa: E402,F401,F403  helpers and presets bound to this page

DARK, LABEL = "#6A6A6A", "#E6E6E6"
HEAD, HEAD_DARK, GROUP, PILL = "#D7D7D7", "#7E7E7E", "#EBEBEB", "#E4E4E4"


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


def section_band(name, num_line, title_line, top):
    """'3 | heading' band: dark number cell and light gray title cell (images in the PDF)."""
    g = Grid(name, [X0, 84.5, X1], [2300])
    g.put(X0, 84.5, 0, 1, [runs_of(num_line, WHITE)], frame(DARK), line=1700)
    g.put(84.5, X1, 0, 1, [runs_of(title_line)], frame(LABEL), align="LEFT", line=1700)
    block(g, top)


def titled(name, line, sticker_x, top, tag="지적사항 개선"):
    """'가. title' heading (14pt) followed by the dark '지적사항 개선' sticker (an image)."""
    g = Grid(name, [X0, sticker_x, X1], [1650])
    g.put(X0, sticker_x, 0, 1, [line], align="LEFT", line=1450)
    g.put(sticker_x, X1, 0, 1, tag, frame("#3C3C3C"), size=760, bold=True, color=WHITE, line=1000)
    block(g, top)


def tagcell(g, x0, x1, r, runs, fill):
    """Small tag cell: thin symmetric padding so the tag stays on one line in its short row."""
    width = to_x(x1) - to_x(x0)
    ratio = min(90, int(90 * (width - 160) / 100 * 0.96 / text_width(runs, 90)))
    g.put(x0, x1, r, r + 1, [runs], fill, line=1000, ratio=ratio, fit=False)
    key = (r, g.xs.index(to_x(x0)))
    g.items[key] = (*g.items[key][:7], dict(left=80, right=80, top=40, bottom=40))


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

section_band("sec3", line1(60, 70, 72, 76), line1(90, 95, 73, 77), 70.9)
titled("title-ga", line1(55, 60, 100, 105), 503.0, 100.6)

# ---------------------------------------------------------------------------
# Synergy-On diagram: an image in the PDF; text read from a 3x render.
# ---------------------------------------------------------------------------
xs = [X0, 70.0, 93.5, 104.5, 250.0, 283.0, 327.0, 362.0, 378.0, 507.0, X1]
g = Grid("synergy", xs, [2000, 600, 3200, 900, 3700, 380, 1920])
band, tab = frame("#E0E0E0", top="soft"), frame("#707070")
dash = frame(left="dot", right="dot")
for r, (num, label, rnum, rlabel) in ((0, ("01", "기반조성", "03", "금융지원")), (6, ("02", "기술개발", "04", "성과공유"))):
    g.put(X0, 93.5, r, r + 1, num, tab, size=1200, bold=True, color=WHITE)
    g.put(93.5, 104.5, r, r + 1, [], band)
    g.put(104.5, 283.0, r, r + 1, label, band, align="LEFT", size=1200, bold=True)
    g.put(327.0, 507.0, r, r + 1, rlabel, band, align="RIGHT", size=1200, bold=True)
    g.put(507.0, X1, r, r + 1, rnum, tab, size=1200, bold=True, color=WHITE)
g.put(283.0, 327.0, 0, 2, [], dash)
g.put(283.0, 327.0, 5, 7, [], dash)
items = ((70.0, 250.0, ("· 함께 키우는 강소기업, 든든한 경영 파트너", "  (스마트공장 및 효율성 개선 지원)"),
          ("· 소중한 혁신 기술, 안전하게 지키는 울타리", "  (협력 기술개발 및 기술보호 지원)")),
         (378.0, X1, ("· 금융 장벽을 넘어, 성장의 날개를 달다", "  (금융대출 이자지원 확대)"),
          ("· 함께 만든 결실, 공정하게 나누는 기쁨", "  (성과 공유제 시행 및 혁신제품 구매)")))
for a, e, first, second in items:
    g.put(a, e, 2, 3, list(first), align="LEFT", size=1090, line=1450)
    g.put(a, e, 3, 4, [], frame(bottom="dot"))
    g.put(a, e, 4, 5, list(second), align="LEFT", size=1090, line=1450)
g.put(250.0, 362.0, 2, 5, [[("Synergy-On", 1800, True, INK)], [("KDN 에너지 ICT 동반성장 플랫폼", 600, False, INK)]],
      line=None)
block(g, 123.0)

g = Grid("note", [X0, X1], [1450, 1500])
g.put(X0, X1, 0, 1, [line1(55, 60, 254, 258)], align="LEFT", line=1200)
g.put(X0, X1, 1, 2, [line1(220, 230, 270, 274)], line=1200)
block(g, 253.6)

g = Grid("chevron", [X0, X1], [1170])
g.put(X0, X1, 0, 1, "▼", frame("#F0F0F0"), size=800, color=ARROW, line=860)
block(g, 285.3)

# ---------------------------------------------------------------------------
# Table 1: 구분 | 추진실적 | 추진성과 (outlined), 4 groups x 2 rows; pills inset in their column.
# ---------------------------------------------------------------------------
xs = [X0, 104.9, 107.7, 173.0, 175.9, 379.9, X1]
SUB = [270, 3000, 270]                     # one 35.4 pt row: pad, pill, pad
g = Grid("table1", xs, [1850] + SUB * 8)
g.put(X0, 104.9, 0, 1, [line1(60, 100, 300, 306)], frame(HEAD, top="mid"))
g.put(104.9, 379.9, 0, 1, [line1(220, 230, 300, 306)], frame(HEAD, top="mid"))
g.put(379.9, X1, 0, 1, [runs_of(line1(440, 460, 300, 306), WHITE)],
      frame(HEAD_DARK, top="strong", left="strong", right="strong"))
for k in range(8):
    top = 317.3 + 35.43 * k
    r = 1 + 3 * k
    last = k == 7
    rule = "mid" if last else "soft"
    if k % 2 == 0:
        label = line1(57, 104, top, top + 70.8)
        g.put(X0, 104.9, r, r + 6, [[("①②③④"[k // 2], 1090, False, INK)], label],
              frame(GROUP, bottom=rule), line=1450)
    g.put(107.7, 173.0, r + 1, r + 2, lines_in(105, 175, top, top + 35), frame(PILL), line=1400)
    g.put(104.9, 175.9, r + 2, r + 3, [], frame(bottom=rule))
    g.put(175.9, 379.9, r, r + 3, lines_in(176, 380, top, top + 35), frame(left="soft", bottom=rule),
          align="LEFT", line=1400)
    g.put(379.9, X1, r, r + 3, hang(lines_in(380, 556, top, top + 35), 382.9),
          frame(left="strong", right="strong", bottom="strong" if last else "soft"), align="LEFT", line=1400)
block(g, 298.8)

# ---------------------------------------------------------------------------
# 나. Table 2: tags (KDN / 中企, 기존 / 개선) are separate filled cells.
# ---------------------------------------------------------------------------
titled("title-na", line1(55, 60, 610, 615), 503.0, 610.6)
xs = [X0, 113.4, 116.2, 137.8, 379.8, X1]
groups = ((651.7, [270, 1230, 270, 1230, 280]), (684.5, [270, 1230, 270, 1230, 280]),
          (717.3, [700, 1230, 270, 1230, 720]))   # pad, tag, gap, tag, pad (no row under 2.7 pt)
g = Grid("table2", xs, [1840] + [h for _, hs in groups for h in hs])
g.put(X0, 113.4, 0, 1, [line1(60, 100, 635, 640)], frame(HEAD, top="mid"))
g.put(113.4, 379.8, 0, 1, [line1(220, 230, 635, 640)], frame(HEAD, top="mid"))
g.put(379.8, X1, 0, 1, [runs_of(line1(440, 460, 635, 640), WHITE)],
      frame(HEAD_DARK, top="strong", left="strong", right="strong"))
tag = frame("#E2E2E2")
for k, (top, hs) in enumerate(groups):
    r = 1 + 5 * k
    last = k == 2
    rule = "mid" if last else "soft"
    bottom = top + sum(hs) / 100
    g.put(X0, 113.4, r, r + 5, [line1(60, 110, top, bottom)], frame(GROUP, bottom=rule))
    first, second = lines_in(115, 120, top, bottom)
    for row, line in ((r + 1, first), (r + 3, second)):
        tagcell(g, 116.2, 137.8, row, runs_of(line, x1=137.0), tag)
        g.put(137.8, 379.8, row, row + 2, [strip_runs(runs_of(line, x0=137.0))],
              frame(bottom=rule) if row == r + 3 else "1", align="LEFT", line=1250)
    g.put(113.4, 137.8, r + 4, r + 5, [], frame(bottom=rule))
    g.put(379.8, X1, r, r + 5, hang(lines_in(380, 556, top, bottom), 382.8),
          frame(left="strong", right="strong", bottom="strong" if last else "soft"), align="LEFT", line=1300)
block(g, 633.3)

# 주요성과
g = Grid("result", [X0, 111.7, X1], [3720])
g.put(X0, 111.7, 0, 1, [runs_of(line1(65, 70, 776, 780), WHITE)], frame(DARK, top="mid", bottom="mid", left="mid"))
g.put(111.7, X1, 0, 1, lines_in(115, 120, 765, 800), frame(top="mid", bottom="mid", right="mid"), align="LEFT",
      line=1500)
block(g, 765.3)

kit.finish(target, end=803.0)
