"""Rebuild KDN 2025 report page 142 (3rd PDF local page 42, printed page 99) as editable HWPX.

Usage: python3 work/kdn2025/p142.py <report3.pdf> <out.hwpx> [--page 42]

조직 운영 및 관리(노사관계), section 3 "합리적이고 적법한 노사관계 운영으로 신뢰받는 노사 협력체계
확립": 가. 노사법치주의 모니터링 (Why?/How?, 모니터링, 문제점 개선, 추진성과), 나. 노사 현안
(노사현안 검토 boxes and the 노사현안 | 주요 이슈 사항 | 대응 노력 table with 성과 bands),
다. 직무 중심 보수체계 (기관장 / 노조위원장 quotes, ①-③ boxes, 추진성과), 주요성과.
Built with the shared kit (one flat table per band on a grid of PDF x edges); all text comes
from the PDF text layer, the table rows follow the PDF's vector rules.

Images and how they are kept:
- PART box, section-3 number band, Why? / How? bubbles: typed cells.
- 기존 / 개선 tags, the 성과 tags, 회사 / 조합 tags: text-layer runs on their own cells
  (outlined, light or dark as printed).
- the gray chevrons -> "▶" / "▼"; the ❶ ❷ ❸ number discs -> ① ② ③; the handshake icon between
  the two quotes is omitted; the quotes keep their italic.
"""

import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kit  # noqa: E402
from kit import Layout, recipe_inputs  # noqa: E402

source, target = recipe_inputs(42, "합리적이고 적법한 노사관계 운영으로 신뢰받는 노사 협력체계 확립")
L = Layout(top=3100)
kit.setup(source, L)
from kit import *  # noqa: E402,F401,F403  helpers and presets bound to this page

DARK = "#6A6A6A"
HEAD = "#D8D8D8"
LABEL = frame("#F0F0F0")
HATCH = frame("#EEEEEE", hatch="#E0E0E0")
BOX = dict(top="mid", bottom="mid", left="mid", right="mid")


def tight(g, x0, r0, left=0, right=0):
    """Narrow the padding of a placed cell (tags narrower than the default 320/180 padding)."""
    c0 = g.xs.index(to_x(x0))
    g.items[r0, c0] = (*g.items[r0, c0][:7], dict(left=left, right=right))


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

# Section 3 band (image): dark number, light title.
g = Grid("sec3", [X0, 84.5, X1], [2300])
g.put(X0, 84.5, 0, 1, [runs_of(line1(60, 70, 72, 77), WHITE)], frame(DARK), line=1700)
g.put(84.5, X1, 0, 1, [line1(90, 95, 73, 78)], frame("#E6E6E6"), align="LEFT", line=1700)
block(g, 70.9)

# ---------------------------------------------------------------------------
# 가. 노사법치주의 모니터링
# ---------------------------------------------------------------------------
g = Grid("title-ga", [X0, X1], [1650])
g.put(X0, X1, 0, 1, [line1(55, 60, 101, 104)], align="LEFT", line=1450)
block(g, 101.2)

g = Grid("why-how", [X0, 92.0, 306.0, 309.5, 342.0, X1], [3875])
strong = dict(top="strong", bottom="strong")
g.put(X0, 92.0, 0, 1, "Why?", frame(left="strong", **strong), size=750, bold=True, color="#3A3A3A")
g.put(92.0, 306.0, 0, 1, lines_in(100, 105, 128, 158), frame(right="strong", **strong), align="LEFT", line=1540)
g.put(309.5, 342.0, 0, 1, "How?", frame("#8A8A8A", left="strong", **strong), size=750, bold=True, color=WHITE)
g.put(342.0, X1, 0, 1, lines_in(350, 355, 128, 158), frame(right="strong", **strong), align="LEFT", line=1540)
block(g, 123.0)

xs = [X0, 105.1, 108.0, 330.5, 333.5, X1]
g = Grid("monitoring", xs, [1650, 4300])
g.put(X0, 105.1, 0, 2, [line1(60, 65, 194, 197)], LABEL)
for (a, e), hx, bx in (((108.0, 330.5), 135, 110), ((333.5, X1), 385, 336)):
    g.put(a, e, 0, 1, [line1(hx, hx + 7, 172, 175)], frame(top="mid", left="mid", right="mid"))
    first, second = lines_in(bx, bx + 8, 193, 224)
    g.put(a, e, 1, 2, [runs_of(first), hang(second)], frame("#E8E8E8", left="mid", right="mid", bottom="mid"),
          align="LEFT", line=1550)
block(g, 169.75)

xs = [X0, 105.1, 108.0, 136.6, 322.5, 338.5, 367.6, X1]
g = Grid("problem", xs, [3600])
g.put(X0, 105.1, 0, 1, lines_in(60, 75, 243, 270), LABEL, line=1320)
g.put(108.0, 136.6, 0, 1, [line1(110, 120, 248, 252)], frame(HEAD, top="mid", bottom="mid", left="mid"))
g.put(136.6, 322.5, 0, 1, lines_in(150, 155, 240, 270), frame(top="mid", bottom="mid", right="mid"), line=1540)
g.put(322.5, 338.5, 0, 1, "▶", size=1000, color=ARROW)
g.put(338.5, 367.6, 0, 1, [runs_of(line1(340, 350, 248, 252), WHITE)], frame("#6E6E6E", top="mid", bottom="mid",
                                                                              left="mid"))
g.put(367.6, X1, 0, 1, lines_in(378, 390, 240, 270), frame(top="mid", bottom="mid", right="mid"), line=1540)
block(g, 236.75)

g = Grid("result-ga", [X0, 104.9, 110.5, X1], [2400])
g.put(X0, 104.9, 0, 1, [line1(60, 65, 288, 291)], frame("#C0C0C0"))
g.put(110.5, X1, 0, 1, [line1(140, 145, 286, 289)], frame("#F2F2F2", top="soft", bottom="soft", left="soft",
                                                           right="soft"))
block(g, 281.75)

# ---------------------------------------------------------------------------
# 나. 주요 노사 현안: three issue boxes ▼ table (issues | 회사/조합 responses, 성과 bands)
# ---------------------------------------------------------------------------
g = Grid("title-na", [X0, X1], [1650])
g.put(X0, X1, 0, 1, [line1(55, 60, 316, 319)], align="LEFT", line=1450)
block(g, 316.5)

xs = [X0, 105.1, 108.5, 254.5, 258.8, 405.0, 409.0, X1]
g = Grid("issues", xs, [1650, 2250])
g.put(X0, 105.1, 0, 2, lines_in(60, 75, 346, 375), LABEL, line=1320)
for (a, e), hx, bx in (((108.5, 254.5), 135, 113), ((258.8, 405.0), 283, 282), ((409.0, X1), 435, 418)):
    g.put(a, e, 0, 1, [line1(hx, hx + 2, 340, 344)], frame(HEAD, top="mid", left="mid", right="mid"))
    g.put(a, e, 1, 2, [line1(bx, bx + 2, 361, 364)], frame(left="mid", right="mid", bottom="mid"))
block(g, 339.5)

g = Grid("chevron", [X0, 105.1, X1], [1970])
g.put(105.1, X1, 0, 1, "▼", size=1000, color=ARROW, line=1000)
block(g, 379.25)

rows = ((417.6, 435.0, 452.9, 472.4), (472.4, 490.0, 507.7, 527.3), (527.3, 545.0, 562.5, 582.1))
hs = [1840] + [int(round((b - a) * 100)) for r in rows for a, b in zip(r, r[1:])]
xs = [X0, 104.9, 118.4, 137.2, 330.2, 333.2, 351.0, X1]
g = Grid("issue-table", xs, hs)
head = frame(HEAD, top="mid", bottom="soft")
g.put(X0, 104.9, 0, 1, [line1(60, 65, 402, 405)], head)
g.put(104.9, 330.2, 0, 1, [line1(185, 190, 402, 405)], frame(HEAD, top="mid", bottom="soft", left="soft",
                                                             right="soft"))
g.put(330.2, X1, 0, 1, [line1(420, 425, 402, 405)], head)
last_row = len(rows) - 1
for k, (y0, y1, y2, y3) in enumerate(rows):
    r = 1 + 3 * k
    edge = "mid" if k == last_row else "soft"
    g.put(X0, 104.9, r, r + 3, lines_in(60, 100, y0, y3), frame("#ECECEC", bottom=edge), line=1320)
    issues = lines_in(105, 330, y0, y2)
    g.put(104.9, 330.2, r, r + 2, [runs_of(l) if l["text"].startswith("∙") else hang(l) for l in issues],
          frame(right="soft"), align="LEFT", line=1540)
    for rr, ln in zip((r, r + 1), lines_in(333, 337, y0, y2)):
        tag = runs_of(ln, x1=351.0)
        is_company = tag[0][0].startswith("회사")
        g.put(330.2, 333.2, rr, rr + 1, [])
        g.put(333.2, 351.0, rr, rr + 1, [tag], frame(WHITE if is_company else "#D9D9D9", top="soft", bottom="soft",
                                                     left="soft", right="soft"), line=1000, fit=False)
        tight(g, 333.2, rr)
        g.put(351.0, X1, rr, rr + 1, [strip_runs(runs_of(ln, x0=351.0))], align="LEFT", line=1250)
    result = line1(110, 115, y2, y3)
    g.put(104.9, 118.4, r + 2, r + 3, "▶", frame("#EEEEEE", bottom=edge), size=900, color="#9A9A9A", fit=False)
    g.put(118.4, 137.2, r + 2, r + 3, [runs_of(result, WHITE, x1=136.0)], frame("#7F7F7F", bottom=edge),
          line=1000, fit=False)
    tight(g, 118.4, r + 2)
    g.put(137.2, X1, r + 2, r + 3, [strip_runs(runs_of(result, x0=136.0))],
          frame("#EEEEEE", hatch="#E0E0E0", bottom=edge), align="LEFT", line=1250)
block(g, 399.2)

# ---------------------------------------------------------------------------
# 다. 직무 중심 보수체계
# ---------------------------------------------------------------------------
g = Grid("title-da", [X0, X1], [1650])
g.put(X0, X1, 0, 1, [line1(55, 60, 592, 596)], align="LEFT", line=1450)
block(g, 593.3)

g = Grid("quotes", [X0, 287.0, 326.0, X1], [1900, 2300])
for (a, e), hx, qx in (((X0, 287.0), 155, 58), ((326.0, X1), 415, 328)):
    g.put(a, e, 0, 1, [line1(hx, hx + 5, 618, 621)], frame(HEAD, top="mid", left="mid", right="mid"))
    g.put(a, e, 1, 2, [line1(qx, qx + 4, 639, 642)], frame(left="mid", right="mid", bottom="mid"))
    italic(g, a, 1)
block(g, 614.75)

boxes = ((X0, 222.6, "①", 103), (224.8, 389.0, "②", 276), (391.6, X1, "③", 433))
g = Grid("job-boxes", [X0, 222.6, 224.8, 389.0, 391.6, X1], [2150, 3950])
for a, e, num, hx in boxes:
    g.put(a, e, 0, 1, [[(num + " ", 1090, True, INK)] + runs_of(line1(hx, hx + 4, 669, 672))],
          frame(top="mid", left="mid", right="mid"))
    g.put(a, e, 1, 2, lines_in(a, a + 12, 690, 722), frame("#E8E8E8", left="mid", right="mid", bottom="mid"),
          align="LEFT", line=1530)
block(g, 664.75)

g = Grid("result-da", [X0, 113.5, 119.0, X1], [2575])
g.put(X0, 113.5, 0, 1, [line1(65, 70, 740, 743)], frame("#C0C0C0"))
g.put(119.0, X1, 0, 1, [line1(138, 142, 737, 741)], frame("#F2F2F2", top="soft", bottom="soft", left="soft",
                                                           right="soft"))
block(g, 733.0)

g = Grid("result", [X0, 116.0, X1], [3700])
g.put(X0, 116.0, 0, 1, [runs_of(line1(65, 70, 776, 780), WHITE)], frame("#686868", top="mid", bottom="mid", left="mid"))
g.put(116.0, X1, 0, 1, lines_in(115, 120, 766, 800), frame(top="mid", bottom="mid", right="mid"), align="LEFT",
      line=1500)
block(g, 764.75)

kit.finish(target, end=803.0)
