"""Rebuild KDN 2025 report page 143 (3rd PDF local page 43, printed page 100) as editable HWPX.

Usage: python3 work/kdn2025/p143.py <report3.pdf> <out.hwpx> [--page 43]

조직 운영 및 관리(노사관계) 평가내용 02 opening page: 평가내용 band, section 1 "전사적 소통체계
구축을 통한 노사 간 공감대 형성 및 협력 기반 강화", 가. 노사 소통 브릿지 (definition box and
the 소통 Bridge | 주요 소통 및 활동 내용 | 추진성과 table), 나. 직원의 목소리 (추진노력, 주요사례,
추진실적), 주요성과. Built with the shared kit (one flat table per band on a grid of PDF x edges);
all text comes from the PDF text layer; the table rows follow the PDF's vector rules.

Images and how they are kept:
- side tab, 평가내용 02 chip, section-1 number band, 'Best Practice' sticker (trophy dropped),
  '지적사항 개선' tag (hand icon dropped), the dark '노사 소통 브릿지(Bridge)란?' tab: typed cells.
- ☑ -> "▣"; the bridge-arc icons between the 회사 / 노조 / 직원 tags -> "⌒"; the ➡ arrow -> "→";
  the gray chevrons -> "▶" / "▼".
- tags (기 관 장, 상임감사, 경 영 진, 위 원 장, 회사, 노조, 직원, 문제인식, 해결방법, 노무TalkTalk,
  익명신문고, 사례1/2, Step1/2) are text-layer runs on their own cells, filled or outlined as printed.
  In the 4th Bridge row the 직원 tag sits a few points higher than printed (one tag row per cell).
- the two case quotes keep their italic.
"""

import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kit  # noqa: E402
from kit import Layout, recipe_inputs  # noqa: E402

source, target = recipe_inputs(43, "전사적 소통체계 구축을 통한 노사 간 공감대 형성 및 협력 기반 강화")
L = Layout(top=3100)
kit.setup(source, L)
from kit import *  # noqa: E402,F401,F403  helpers and presets bound to this page

DARK = "#6A6A6A"
HEAD = "#D8D8D8"
LABEL_FILL = "#ECECEC"
OUTLINE = dict(top="soft", bottom="soft", left="soft", right="soft")
ARROW_RUN = ("→ ", 1000, True, "#505050")


def tight(g, x0, r0, left=0, right=0):
    """Narrow the padding of a placed cell (tags narrower than the default 320/180 padding)."""
    c0 = g.xs.index(to_x(x0))
    g.items[r0, c0] = (*g.items[r0, c0][:7], dict(left=left, right=right))


def tag(g, x0, x1, r0, r1, runs, fill, color=INK):
    """A tag (text-layer run) on its own filled / outlined cell with no padding."""
    runs = [(t, s, True, color) for t, s, _, _ in runs]
    g.put(x0, x1, r0, r1, [runs], frame(fill, **OUTLINE), line=1000, ratio=85, fit=False)
    tight(g, x0, r0)


def hang(line):
    """Continuation line: keep the source indent (runs_of strips leading blanks)."""
    runs = runs_of(line)
    return [("  ", runs[0][1], False, INK)] + runs


def italic(grid, x0, r0):
    """Set every run of a placed cell in italic (charPr copy + <hh:italic/>)."""
    for par in grid.items[r0, grid.xs.index(to_x(x0))][3]:
        for run in par.findall(L.q("hp:run")):
            base = L.characters.find(f"hh:charPr[@id='{run.get('charPrIDRef')}']", L.ns)
            el = deepcopy(base)
            L.sub(el, "hh:italic")
            run.set("charPrIDRef", L.append_style(L.characters, el))


# ---------------------------------------------------------------------------
# Page chrome (odd page): running head over a rule, side tab, footer at the right.
# ---------------------------------------------------------------------------
L.add_table([[cell(0, 3350, 1680, [para([("01", 1380, True, WHITE)], "CENTER")[0]], dark)],
             [cell(0, 3350, 5960, [para([(ch, 950, True, INK)], "CENTER", 1160)[0] for ch in "경영관리"], gray2)]],
            floating=(57800, 15000))
report, number = runs_of(line1(450, 455, 816, 822))      # '2025년도 경영실적보고서' + '100' in one PDF line
foot = [report, ("    ", 790, False, INK), number]
L.add_table([[cell(0, W, 1500, [para(foot, "RIGHT", 1300)[0]])]], floating=(5660, 81550))

g = Grid("head", [X0, 432.0, X1], [1680])
g.put(X0, 432.0, 0, 1, [], frame(bottom="soft"))
g.put(432.0, X1, 0, 1, [line1(430, 440, 35, 40)], align="RIGHT")
block(g, 32.0)

# 평가내용 02 band (chip image typed, title from the text layer)
g = Grid("band", [X0, 124.0, X1], [1950, 910])
g.put(X0, 124.0, 0, 1, "평가내용 02", frame("#565656", top="strong"), size=970, bold=True, color=WHITE, ratio=80)
g.put(X0, 124.0, 1, 2, [], frame("#E9E9E9", bottom="soft", left="soft", hatch="#DADADA"))
g.put(124.0, X1, 0, 2, [line1(125, 130, 77, 80)], frame("#E9E9E9", top="strong", bottom="soft", right="soft",
                                                         hatch="#DADADA"), align="LEFT", line=1480)
block(g, 70.9)

# Section band "1 전사적 소통체계 ..."
g = Grid("section", [X0, 84.5, X1], [2300])
g.put(X0, 84.5, 0, 1, [runs_of(line1(64, 70, 113, 116), WHITE)], frame(DARK), line=1700)
g.put(84.5, X1, 0, 1, [line1(90, 95, 114, 117)], frame("#E6E6E6"), align="LEFT", line=1700)
block(g, 111.5)

# ---------------------------------------------------------------------------
# 가. 노사 소통 브릿지
# ---------------------------------------------------------------------------
g = Grid("title-ga", [X0, 486.0, X1], [1650])
g.put(X0, 486.0, 0, 1, [line1(55, 60, 141, 144)], align="LEFT", line=1450)
g.put(486.0, X1, 0, 1, "Best Practice", frame("#4A4A4A"), size=900, bold=True, color=WHITE)
block(g, 142.0)

g = Grid("bridge-def", [X0, 200.0, X1], [2000, 2150])
g.put(X0, 200.0, 0, 1, [runs_of(line1(65, 70, 167, 170), WHITE)], frame("#6E6E6E"), align="LEFT")
g.put(X0, X1, 1, 2, [[("▣ ", 1000, False, "#505050")] + runs_of(line1(73, 77, 189, 192))],
      frame(top="mid", bottom="mid", left="mid", right="mid"), align="LEFT")
block(g, 163.8)

# 소통 Bridge table: label tags (A ⌒ B) | bullets with inline tags | 추진성과 (heavy frame)
groups = (  # row y edges, content sub-rows (line tops; None = pad), tag sub-row
    ((233.6, 253.6, 270.2, 287.1, 303.8, 320.3, 336.8, 357.0), 3),
    ((357.0, 370.0, 384.0, 396.6), 1),
    ((396.6, 404.0, 418.0, 436.5), 1),
    ((436.5, 443.0, 456.3, 470.0, 476.1), 1),
)
hs = [1850]
for edges, _ in groups:
    hs += [int(round((b - a) * 100)) for a, b in zip(edges, edges[1:])]
A, ARC, B = (61.0, 81.5), (81.5, 103.0), (103.0, 122.5)
xs = [X0, A[0], A[1], B[0], B[1], 127.6, 136.5, 171.3, 396.8, X1]
g = Grid("bridge", xs, hs)
g.put(X0, 127.6, 0, 1, [line1(64, 70, 218, 222)], frame(HEAD, top="mid", bottom="soft", right="soft"))
g.put(127.6, 396.8, 0, 1, [line1(210, 220, 218, 222)], frame(HEAD, top="mid", bottom="soft"))
g.put(396.8, X1, 0, 1, [runs_of(line1(455, 460, 218, 222), WHITE)], frame("#7F7F7F", top="strong", left="strong",
                                                                          right="strong"))
heavy = dict(left="strong", right="strong")
labels = (  # (tag A runs line, fill, color) per stacked row, tag B (line, fill, color)
    ([((64, 66, 289, 292), "#D9D9D9", INK)], ((104, 106, 290, 293), WHITE, INK)),
    ([((64, 66, 371, 374), "#7F7F7F", WHITE)], ((104, 106, 371, 374), WHITE, INK)),
    ([((64, 66, 411, 414), "#7F7F7F", WHITE)], ((103, 106, 411, 414), "#D9D9D9", INK)),
    ([((60, 62, 443, 446), "#D9D9D9", INK), ((62, 64, 458, 461), "#7F7F7F", WHITE)], ((107, 108, 451, 454), WHITE, INK)),
)
inline_tags = {(0, 0): "#404040", (0, 2): WHITE, (0, 3): WHITE, (2, 0): "#BFBFBF"}
r = 1
for k, ((edges, tag_row), (a_tags, b_tag)) in enumerate(zip(groups, labels)):
    n = len(edges) - 1
    last = k == len(groups) - 1
    bottom = "mid" if last else "soft"
    # label column: fill everywhere, tags in the tag sub-row(s)
    tag_rows = [r + tag_row + i for i in range(len(a_tags))]
    for i in range(n):
        rr = r + i
        edge = dict(bottom=bottom) if i == n - 1 else {}
        if rr in tag_rows:
            (x0, x1, y0, y1), fill, color = a_tags[tag_rows.index(rr)]
            g.put(X0, A[0], rr, rr + 1, [], frame(LABEL_FILL, **edge))
            tag(g, A[0], A[1], rr, rr + 1, runs_of(line1(x0, x1, y0, y1)), fill, color)
            if rr == tag_rows[0]:
                g.put(ARC[0], ARC[1], rr, rr + 1, "⌒", frame(LABEL_FILL, **edge), size=1300, bold=True,
                      color="#404040", line=1000, fit=False)
                (x0, x1, y0, y1), fill, color = b_tag
                tag(g, B[0], B[1], rr, rr + 1, runs_of(line1(x0, x1, y0, y1)), fill, color)
            else:
                g.put(ARC[0], B[1], rr, rr + 1, [], frame(LABEL_FILL, **edge))
            g.put(B[1], 127.6, rr, rr + 1, [], frame(LABEL_FILL, right="soft", **edge))
        else:
            g.put(X0, 127.6, rr, rr + 1, [], frame(LABEL_FILL, right="soft", **edge))
    # content column
    content = lines_in(128, 396, edges[0], edges[-1])
    if k in (1, 3):                      # plain bullets: one cell over the whole group
        g.put(127.6, 396.8, r, r + n, [runs_of(l) for l in content], frame(bottom=bottom), align="LEFT", line=1650)
    else:
        rows_used = range(n) if k == 0 else (1, 2)
        if k == 2:
            g.put(127.6, 396.8, r, r + 1, [])
        for j, (i, ln) in enumerate(zip(rows_used, content)):
            rr = r + i
            edge = dict(bottom=bottom) if i == n - 1 else {}
            if ln["text"].startswith("∙"):
                g.put(127.6, 136.5, rr, rr + 1, [runs_of(ln, x1=137.0)], frame(**edge), line=1200, fit=False)
                tight(g, 127.6, rr, 280, 0)
                fill = inline_tags.get((k, j))
                if fill:
                    t = runs_of(ln, x0=137.0, x1=171.0)
                    tag(g, 136.5, 171.3, rr, rr + 1, t, fill, WHITE if fill in ("#404040",) else INK)
                    g.put(171.3, 396.8, rr, rr + 1, [strip_runs(runs_of(ln, x0=171.0))], frame(**edge), align="LEFT",
                          line=1200)
                else:
                    g.put(136.5, 396.8, rr, rr + 1, [strip_runs(runs_of(ln, x0=137.0))], frame(**edge),
                          align="LEFT", line=1200)
            else:                        # continuation line under the text column
                g.put(127.6, 171.3, rr, rr + 1, [], frame(**edge))
                g.put(171.3, 396.8, rr, rr + 1, [runs_of(ln)], frame(**edge), align="LEFT", line=1200)
    # 추진성과 column
    results = lines_in(399, 550, edges[0], edges[-1])
    g.put(396.8, X1, r, r + n, [runs_of(l) if l["text"].startswith("∙") else hang(l) for l in results],
          frame(bottom="strong" if last else "soft", **heavy), align="LEFT", line=1650)
    r += n
block(g, 215.1)

# ---------------------------------------------------------------------------
# 나. 직원의 목소리: 추진노력, 주요사례, 추진실적
# ---------------------------------------------------------------------------
g = Grid("title-na", [X0, 498.5, 552.0, X1], [1650])
g.put(X0, 498.5, 0, 1, [line1(55, 60, 486, 489)], align="LEFT", line=1450)
g.put(498.5, 552.0, 0, 1, "지적사항 개선", frame("#4A4A4A"), size=800, bold=True, color=WHITE, line=950)
block(g, 487.5)

xs = [X0, 105.1, 107.7, 110.5, 117.5, 126.6, 161.0, 170.3, 328.0, 335.9, 349.0, 383.3, X1]
g = Grid("effort", xs, [1800, 3750, 1550, 1400, 2150])
g.put(X0, 105.1, 0, 5, [line1(60, 65, 557, 560)], frame("#F0F0F0"))
left = line1(125, 132, 512, 515)
g.put(110.5, 126.6, 0, 1, [], frame(HEAD, top="mid", left="mid"))
tag(g, 126.6, 161.0, 0, 1, runs_of(left, x1=160.0), WHITE)
g.put(161.0, 328.0, 0, 1, [strip_runs(runs_of(left, x0=160.0))], frame(HEAD, top="mid", right="mid"), align="LEFT")
right = line1(350, 355, 512, 515)
g.put(335.9, 349.0, 0, 1, [], frame("#6E6E6E", top="mid", left="mid"))
tag(g, 349.0, 383.3, 0, 1, runs_of(right, x1=382.0), WHITE)
g.put(383.3, X1, 0, 1, [strip_runs(runs_of(right, WHITE, x0=382.0))], frame("#6E6E6E", top="mid", right="mid"),
      align="LEFT")
g.put(110.5, 328.0, 1, 2, lines_in(112, 116, 530, 562), frame(left="mid", right="mid", bottom="mid"), align="LEFT",
      line=1540)
g.put(335.9, X1, 1, 2, lines_in(337, 341, 530, 562), frame(left="mid", right="mid", bottom="mid"), align="LEFT",
      line=1540)
fn1 = line1(110, 113, 567, 570)
g.put(107.7, 117.5, 2, 3, [runs_of(fn1, x1=117.0)], fit=False)
tight(g, 107.7, 2, 100, 0)
g.put(117.5, 170.3, 2, 3, [strip_runs(runs_of(fn1, x0=117.0, x1=170.0))], frame("#D9D9D9"), line=1000)
tight(g, 117.5, 2, 60, 60)
g.put(170.3, X1, 2, 3, [strip_runs(runs_of(fn1, x0=170.0))], align="LEFT", line=1050)
g.put(107.7, 117.5, 3, 4, [line1(107, 109, 581, 584)], fit=False)
tight(g, 107.7, 3, 0, 0)
g.put(117.5, 170.3, 3, 4, [line1(124, 126, 581, 584)], frame("#D9D9D9"), line=1000)
g.put(170.3, X1, 3, 4, [line1(169, 171, 581, 584)], align="LEFT", line=1050)
g.put(107.7, 117.5, 4, 5, "▶", frame("#EEEEEE"), size=900, color="#9A9A9A", fit=False)
g.put(117.5, X1, 4, 5, [line1(119, 122, 599, 602)], frame("#EEEEEE", hatch="#E0E0E0"), align="LEFT")
block(g, 509.5)

# 주요사례 (two case boxes) continuing into 추진실적
cases = ((110.5, 328.0, (144.8, 176.6), 176.0, (113.4, 145.1), 144.5),
         (335.9, X1, (357.9, 389.7), 389.0, (338.7, 370.4), 369.5))
xs = sorted({X0, 105.1} | {x for a, e, p, _, s, _ in cases for x in (a, e, *p, *s)})
g = Grid("cases", xs, [1950, 1650, 1650, 1700, 1800, 800, 4050])
g.put(X0, 105.1, 0, 5, [line1(60, 65, 662, 665)], frame("#F0F0F0"))
g.put(X0, 105.1, 6, 7, [line1(60, 65, 732, 735)], frame("#C0C0C0"))
for a, e, (p0, p1), cut, (s0, s1), scut in cases:
    side = dict(left="mid", right="mid")
    head = line1(a, e, 625, 628)
    g.put(a, p0, 0, 1, [], frame(top="mid", left="mid", bottom="dot"))
    tag(g, p0, p1, 0, 1, runs_of(head, x1=cut), "#D9D9D9")
    g.put(p1, e, 0, 1, [strip_runs(runs_of(head, x0=cut))], frame(top="mid", right="mid", bottom="dot"), align="LEFT")
    g.put(a, e, 1, 2, [line1(a, e, 646, 649)], frame(**side))
    italic(g, a, 1)
    g.put(a, e, 2, 3, [[ARROW_RUN] + runs_of(line1(a, e, 661, 664))], frame(**side))
    for rr, y in ((3, 679.9), (4, 696.7)):
        step = line1(a, a + 10, y - 1, y + 1)
        g.put(a, s0, rr, rr + 1, [], frame(left="mid"))
        tag(g, s0, s1, rr, rr + 1, runs_of(step, x1=scut), "#7F7F7F", WHITE)
        g.put(s1, e, rr, rr + 1, [strip_runs(runs_of(step, x0=scut))], frame(right="mid"), align="LEFT", line=1250)
    g.put(a, e, 5, 6, "▼", frame(**side), size=700, color=ARROW, line=600, fit=False)
    g.put(a, e, 6, 7, lines_in(a, e, 720, 755), frame("#E8E8E8", bottom="mid", **side), line=1540)
block(g, 621.5)

g = Grid("result", [X0, 116.0, X1], [3700])
g.put(X0, 116.0, 0, 1, [runs_of(line1(65, 70, 777, 780), WHITE)], frame("#686868", top="mid", bottom="mid", left="mid"))
g.put(116.0, X1, 0, 1, lines_in(115, 120, 766, 800), frame(top="mid", bottom="mid", right="mid"), align="LEFT",
      line=1500)
block(g, 765.0)

kit.finish(target, end=803.0)
