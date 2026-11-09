"""Rebuild KDN 2025 report page 54 (second PDF local page 4, printed page 34) as editable HWPX.

Usage: python3 work/kdn2025/p54.py <report2.pdf> <out.hwpx> [--page 4]

일자리 및 균등한 기회 평가내용 03 opening page (even page). Built with the shared diagram kit (one
flat table per horizontal band on a grid of PDF x edges); all running text comes from the PDF text
layer. Images: the PART label, the 평가내용 03 chip, the '지적사항 개선' stickers (hand icon dropped),
the 'NEW 신규' sticker (typed as a dark 신규 tag), the filled numbers ❶-❹ (typed ① ② ③ ④), the
chevron between the 지적사항 and 개선과제 boxes (typed ▶), three photos (empty photo cells) and two
small bar charts, whose printed values (사회형평분야 정규직 채용 75%↑ 4명 → 7명; 사회형평분야 인턴
23명 채용 0명 → 23명; ’24년 / ’25년; read from 6x renders, 4 → 7 is +75 %) become value cells
without bars. The Kdn logo in the footer is typed as text.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kit  # noqa: E402
from kit import Layout, recipe_inputs  # noqa: E402

source, target = recipe_inputs(4, "채용제도 개선 및 신규 프로그램을 통한 폭 넓은 취업 기회 마련")
L = Layout(top=3100)
kit.setup(source, L)
from kit import *  # noqa: E402,F401,F403  helpers and presets bound to this page

DARK, LABEL = "#6A6A6A", "#E6E6E6"
HEAD = "#DADADA"
BOX = dict(top="soft", bottom="soft", left="soft", right="soft")
TIGHT = dict(left=0, right=0)


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


def tight(g, x0, r0):
    """No side padding for a narrow tag / number cell, or its two syllables wrap."""
    key = (r0, g.xs.index(to_x(x0)))
    g.items[key] = g.items[key][:7] + (TIGHT,)


def section_band(name, num_line, title_line, top, sticker=None):
    """'1 | heading' band with an optional typed '지적사항 개선' sticker."""
    xs = [X0, 84.5, sticker[0], sticker[1], X1] if sticker else [X0, 84.5, X1]
    g = Grid(name, xs, [2300])
    g.put(X0, 84.5, 0, 1, [runs_of(num_line, WHITE)], frame(DARK), line=1700)
    g.put(84.5, xs[2], 0, 1, [runs_of(title_line)], frame(LABEL), align="LEFT", line=1700)
    if sticker:
        g.put(sticker[0], sticker[1], 0, 1, "지적사항 개선", frame("#3C3C3C"), size=760, bold=True, color=WHITE,
              line=1000)
        g.put(sticker[1], X1, 0, 1, [], frame(LABEL))
    block(g, top)


class Rows:
    """Row edges given as PDF y values; r(y) is the row index starting at y."""

    def __init__(self, ys):
        self.ys = sorted(set(ys))
        self.hs = [int(round((b - a) * 100)) for a, b in zip(self.ys, self.ys[1:])]

    def __call__(self, y):
        return self.ys.index(y)


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

# ---------------------------------------------------------------------------
# 1. 채용제도 개선 / 가. 4대 개선 과제 (text layer; pills, tags and numbers drawn)
# ---------------------------------------------------------------------------
section_band("sec1", line1(60, 70, 113, 118), line1(90, 95, 114, 118), 111.5, sticker=(463.5, 518.0))

g = Grid("title-ga", [X0, X1], [1650])
g.put(X0, X1, 0, 1, [line1(55, 60, 141, 145)], align="LEFT", line=1450)
block(g, 141.2)

xs = [X0, 62.3, 81.1, 126.8, 155.2, 299.0, 313.0, 330.9, 349.7, 380.4, 408.8, 433.0, 447.9, 466.7, X1]
R = Rows([164.0, 182.4, 185.0, 197.4, 200.0, 212.4, 216.6])
g = Grid("feedback", xs, R.hs)
head = frame(HEAD, top="soft")
rows = (R(164.0), R(182.4))
l = line1(130, 135, 166, 170)
g.put(X0, 126.8, *rows, [], frame(HEAD, top="soft", left="soft"))
g.put(126.8, 155.2, *rows, [runs_of(l, x1=155.0)], frame(WHITE, **BOX))
tight(g, 126.8, rows[0])
g.put(155.2, 299.0, *rows, [strip_runs(runs_of(l, x0=155.0))], frame(HEAD, top="soft", right="soft"), align="LEFT")
l = line1(383, 388, 166, 170)
g.put(313.0, 380.4, *rows, [], frame(HEAD, top="soft", left="soft"))
g.put(380.4, 408.8, *rows, [runs_of(l, WHITE, x1=408.0)], frame("#7E7E7E"))
tight(g, 380.4, rows[0])
g.put(408.8, X1, *rows, [strip_runs(runs_of(l, x0=408.0))], frame(HEAD, top="soft", right="soft"), align="LEFT")
g.put(299.0, 313.0, R(182.4), R(212.4), "▶", size=1000, color=ARROW)
g.put(X0, 62.3, R(182.4), R(216.6), [], frame(left="soft", bottom="soft"))
g.put(313.0, 330.9, R(182.4), R(185.0), [], frame(left="soft"))
g.put(313.0, 330.9, R(212.4), R(216.6), [], frame(left="soft", bottom="soft"))
for y, y1, ty in ((185.0, 197.4, 186.1), (200.0, 212.4, 200.7)):
    r = (R(y), R(y1))
    l = line1(64, 66, ty, ty + 4)
    g.put(62.3, 81.1, *r, [runs_of(l, x1=80.0)], frame(WHITE, **BOX), line=1060)
    tight(g, 62.3, r[0])
    g.put(81.1, 299.0, *r, [strip_runs(runs_of(l, x0=80.0))], frame(right="soft"), align="LEFT", line=1060)
    for mark, n0, t0, t1, e in ((("①", "③")[y > 190], 313.0, 330.9, 349.7, 433.0),
                                (("②", "④")[y > 190], 433.0, 447.9, 466.7, X1)):
        l = line1(t0 + 1, t0 + 4, ty, ty + 4)
        g.put(n0, t0, *r, [[(mark, 1090, True, INK)]], frame(left="soft") if n0 == 313.0 else "1",
              align="RIGHT" if n0 == 313.0 else "CENTER", line=1060)
        tight(g, n0, r[0])
        g.put(t0, t1, *r, [runs_of(l, WHITE, x1=t1 - 1.0)], frame("#7E7E7E"), line=1060)
        tight(g, t0, r[0])
        g.put(t1, e, *r, [strip_runs(runs_of(l, x0=t1 - 1.0))], frame(right="soft") if e == X1 else "1", align="LEFT",
              line=1060)
g.put(62.3, 299.0, R(182.4), R(185.0), [], frame(right="soft"))
g.put(330.9, X1, R(182.4), R(185.0), [], frame(right="soft"))
g.put(313.0, 330.9, R(197.4), R(200.0), [], frame(left="soft"))
g.put(62.3, 299.0, R(197.4), R(200.0), [], frame(right="soft"))
g.put(62.3, 299.0, R(212.4), R(216.6), [], frame(right="soft", bottom="soft"))
g.put(330.9, X1, R(197.4), R(200.0), [], frame(right="soft"))
g.put(330.9, X1, R(212.4), R(216.6), [], frame(right="soft", bottom="soft"))
block(g, 164.0)


def cards(name, top, ys, specs):
    """Two cards: gray tab with typed number | light band with a boxed tag; bullets | chart or photo.

    specs: per card (a, tab_end, tag0, tag1, side0, c1, e, mark, tab_y, bullets(x0, y0, y1), base, chart);
    side0..c1 is the chart / photo column, c1..e the card's right margin.
    chart: None for a photo, else (pill, top value, low value); rows t1 | pill | top | low | gap | axis | end.
    """
    R = Rows(ys)
    g = Grid(name, XS, R.hs)
    t0, k0, k1, t1 = ys[:4]
    end = ys[-1]
    for a, tab_end, tag0, tag1, side0, c1, e, mark, tab_y, (bx0, by0, by1), base, chart in specs:
        tab = line1(a + 15, tab_end, tab_y, tab_y + 4)
        g.put(a, tab_end, R(t0), R(t1), [[(mark + " ", 1090, True, WHITE)] + runs_of(tab, WHITE)], frame("#7A7A7A"),
              align="LEFT")
        band = frame("#E3E3E3")
        g.put(tab_end, tag0, R(t0), R(t1), [], band)
        g.put(tag0, tag1, R(t0), R(k0), [], band)
        g.put(tag0, tag1, R(k0), R(k1), [line1(tag0 - 3, tag0 + 4, k0, k0 + 4)], frame(WHITE, **BOX), bold=True,
              line=1000)
        if tag1 - tag0 < 25:
            tight(g, tag0, R(k0))
        g.put(tag0, tag1, R(k1), R(t1), [], band)
        g.put(tag1, e, R(t0), R(t1), [], band)
        g.put(a, side0, R(t1), R(end), hang(lines_in(bx0 - 1, bx0 + 25, by0, by1), base),
              frame(left="soft", bottom="soft"), align="LEFT", line=1540 if chart else 1320)
        mid = round((side0 + c1) / 2, 1)
        if chart is None:
            g.put(side0, c1, R(ys[4]), R(ys[5]), [], photo)
            g.put(side0, e, R(t1), R(ys[4]), [], frame(right="soft"))
            g.put(side0, c1, R(ys[5]), R(end), [], frame(bottom="soft"))
            g.put(c1, e, R(ys[4]), R(end), [], frame(right="soft", bottom="soft"))
            continue
        pill, high, low = chart
        g.put(side0, c1, R(t1), R(ys[4]), [[(pill, 700, True, WHITE)]], frame("#4A4A4A"), line=880)
        g.put(mid, c1, R(ys[4]), R(ys[5]), [[(high, 880, True, INK)]], line=920)
        g.put(side0, mid, R(ys[5]), R(ys[6]), [[(low, 880, False, INK)]], line=920)
        axis = frame("#E6E6E6", top="soft")
        g.put(side0, mid, R(ys[-3]), R(ys[-2]), [[("’24년", 800, False, INK)]], axis, line=860)
        g.put(mid, c1, R(ys[-3]), R(ys[-2]), [[("’25년", 800, True, INK)]], axis, line=860)
        g.put(c1, e, R(t1), R(end), [], frame(right="soft", bottom="soft"))
        g.put(side0, c1, R(ys[-2]), R(end), [], frame(bottom="soft"))
    block(g, top)


XS = [X0, 159.3, 174.3, 193.1, 216.1, 237.4, 258.6, 288.1, 301.1, 304.2, 308.2, 410.9, 425.9, 444.7, 467.7, 510.2,
      552.7, X1]
cards("cards-1", 222.8, [222.8, 226.2, 237.9, 241.6, 253.0, 264.0, 279.0, 282.0, 292.5, 298.4],
      [(X0, 159.3, 174.3, 193.1, 216.1, 301.1, 304.2, "①", 227, (62.5, 247, 290), 62.5,
        ("사회형평분야 정규직 채용 75%↑", "7명", "4명")),
       (308.2, 410.9, 425.9, 444.7, 467.7, 552.7, X1, "②", 227, (314.1, 247, 290), 314.1,
        ("사회형평분야 인턴 23명 채용", "23명", "0명"))])
cards("cards-2", 302.1, [302.1, 305.6, 317.3, 320.9, 323.5, 388.7, 391.7],
      [(X0, 159.3, 174.3, 288.1, 216.1, 301.1, 304.2, "③", 306, (62.5, 322, 382), 62.5, None),
       (308.2, 410.9, 425.9, 444.7, 467.7, 552.7, X1, "④", 306, (314.1, 322, 382), 314.1, None)])

# ---------------------------------------------------------------------------
# 나. KDN-취업드림(Dream) (title with a typed 신규 tag) and its four-row program table.
# ---------------------------------------------------------------------------
g = Grid("title-na", [X0, 493.0, 520.0, X1], [1650])
g.put(X0, 493.0, 0, 1, [line1(55, 60, 402, 406)], align="LEFT", line=1450)
g.put(493.0, 520.0, 0, 1, "신규", frame("#3C3C3C"), size=880, bold=True, color=WHITE, line=1000)
block(g, 401.6)

xs = [X0, 102.7, 107.6, 199.7, 289.0, 378.3, 469.1, X1]
R = Rows([424.1, 448.5, 473.2, 477.9, 491.7, 528.5, 553.9])
g = Grid("dream", xs, R.hs)
side = frame(HEAD, top="soft", bottom="soft")
g.put(X0, 102.7, R(424.1), R(448.5), [line1(60, 65, 429, 433)], side, bold=True)
g.put(107.6, X1, R(424.1), R(448.5), [line1(145, 150, 429, 433)], frame("#D6D6D6", top="soft", bottom="soft"))
g.put(X0, 102.7, R(448.5), R(473.2), [line1(60, 65, 454, 458)], side, bold=True)
g.put(107.6, X1, R(448.5), R(473.2), [line1(150, 155, 452, 456)], frame(**BOX))
g.put(X0, 102.7, R(473.2), R(528.5), lines_in(60, 75, 487, 505), side, bold=True)
for k, (a, e, hx, bx) in enumerate(((107.6, 199.7, 140, 113.5), (199.7, 289.0, 214, 202.8),
                                    (289.0, 378.3, 308, 292.1), (378.3, 469.1, 391, 381.4))):
    sep = dict(left="soft" if k == 0 else "dot")
    g.put(a, e, R(473.2), R(477.9), [], frame(top="soft", **sep))
    g.put(a, e, R(477.9), R(491.7), [[("①②③④"[k] + " ", 1090, True, INK)] + runs_of(line1(hx, hx + 2, 478, 482))],
          frame(**sep), line=1220)
    g.put(a, e, R(491.7), R(528.5), hang(lines_in(bx - 1, bx + 10, 494, 515), bx), frame(bottom="soft", **sep),
          align="LEFT", line=1540)
g.put(469.1, X1, R(473.2), R(528.5), [], photo)
g.put(X0, 102.7, R(528.5), R(553.9), [line1(70, 75, 535, 539)], side, bold=True)
g.put(107.6, X1, R(528.5), R(553.9), [line1(160, 165, 535, 539)], frame("#E0E0E0", top="soft", bottom="soft"))
block(g, 424.1)

# ---------------------------------------------------------------------------
# 2. 사회형평적 인력 맞춤 지원 (a real table in the PDF; 추진성과 column boxed in dark)
# ---------------------------------------------------------------------------
section_band("sec2", line1(60, 70, 571, 575), line1(90, 95, 572, 576), 569.6, sticker=(497.0, 551.5))

R = Rows([598.9, 617.3, 645.8, 661.0, 690.6, 730.8, 770.4])
g = Grid("equity", [X0, 121.9, 433.5, X1], R.hs)
g.put(X0, 121.9, 0, 1, [line1(75, 80, 601, 605)], frame("#D7D7D7", top="soft", bottom="soft"), bold=True)
g.put(121.9, 433.5, 0, 1, [line1(240, 245, 601, 605)], frame("#D7D7D7", top="soft", bottom="soft", left="soft"),
      bold=True)
g.put(433.5, X1, 0, 1, [runs_of(line1(475, 480, 601, 605), WHITE)],
      frame("#7E7E7E", top="strong", left="strong", right="strong", bottom="soft"), bold=True)
label = dict(top="soft", bottom="soft")
body = dict(top="soft", bottom="soft", left="soft")
right = dict(top="soft", left="strong", right="strong")
mixed = line1(59, 60, 623, 627)          # 기초생활수급자 + its bullet on one PDF line
g.put(X0, 121.9, 1, 2, [runs_of(mixed, x1=121.9)], frame("#EBEBEB", **label))
g.put(121.9, 433.5, 1, 2, [strip_runs(runs_of(mixed, x0=121.9))], frame(**body), align="LEFT")
g.put(433.5, X1, 1, 2, hang(lines_in(436, 446, 618, 640), 436.5), frame(**right), align="LEFT", line=1320)
g.put(X0, 121.9, 2, 3, [line1(70, 72, 647, 650)], frame("#EBEBEB", **label))
g.put(121.9, 433.5, 2, 3, [line1(124, 126, 647, 650)], frame(**body), align="LEFT")
g.put(433.5, X1, 2, 3, [line1(436, 437, 647, 650)], frame(**right), align="LEFT")
mixed = line1(61, 62, 669, 672)          # 북한이탈주민 + its row's bullet on one PDF line
g.put(X0, 121.9, 3, 4, [line1(59, 60, 662, 665), runs_of(mixed, x1=121.9)], frame("#EBEBEB", **label), line=1230)
g.put(121.9, 433.5, 3, 4, [strip_runs(runs_of(mixed, x0=121.9))], frame(**body), align="LEFT")
g.put(433.5, X1, 3, 4, hang(lines_in(436, 446, 663, 678), 436.5), frame(**right), align="LEFT", line=1230)
g.put(X0, 121.9, 4, 5, [line1(61, 62, 704, 707)], frame("#EBEBEB", **label))
g.put(121.9, 433.5, 4, 5, hang(lines_in(121, 126, 691, 720), 124.9), frame(**body), align="LEFT", line=1250)
g.put(433.5, X1, 4, 5, [line1(436, 437, 704, 707)], frame(**right), align="LEFT")
g.put(X0, 121.9, 5, 6, [line1(75, 76, 744, 747)], frame("#EBEBEB", **label))
g.put(121.9, 433.5, 5, 6, lines_in(124, 126, 737, 754), frame(**body), align="LEFT", line=1320)
g.put(433.5, X1, 5, 6, hang(lines_in(436, 446, 731, 762), 436.5), frame(top="soft", left="strong", right="strong",
                                                                       bottom="strong"), align="LEFT", line=1240)
block(g, 598.9)

g = Grid("result", [X0, 111.7, X1], [1850])
g.put(X0, 111.7, 0, 1, [runs_of(line1(65, 70, 782, 786), WHITE)], frame("#6A6A6A", top="mid", bottom="mid", left="mid"))
g.put(111.7, X1, 0, 1, [line1(115, 120, 782, 786)], frame(top="mid", bottom="mid", right="mid"), align="LEFT")
block(g, 779.8)

kit.finish(target, end=799.0)   # box ends at 798.3; nothing follows in the flow
