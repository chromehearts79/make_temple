"""Rebuild KDN 2025 report physical PDF page 19 (printed page 7) as editable HWPX.

Usage: python3 work/kdn2025/p19.py <report.pdf> <out.hwpx> [--page N]

Diagram-heavy page recipe. Every box, flow and chart is one flat Hancom table per
horizontal band, laid on a "union grid": column edges are PDF x coordinates, rows are
heights in 1/100 pt, cells are placed by edge coordinates and every uncovered grid slot is
auto-filled with a borderless blank cell (so rows never end up empty and gutters stay
invisible). Text is taken from PDF lines with their spans (bold / size / superscript size),
and 장평 is fitted per cell from the PDF glyph metrics, never by shortening text.
Photos are left as empty placeholder cells; charts become small value cells.
"""

import sys
from functools import lru_cache
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".claude/skills/pdf-hwpx-layout/scripts"))

import pymupdf  # noqa: E402
from hwpx_layout import Layout, cell  # noqa: E402
from pdf_coords import recipe_inputs  # noqa: E402

source, target = recipe_inputs(19, "5대 핵심가치 도출 및 新행동양식 수립")
L = Layout(top=3100)
W = 49900
X0, X1 = 56.6, 555.6          # PDF x of the body's left / right edge (= HWPX margins)
INK, WHITE = "#161616", "#FFFFFF"
WARN = []

# ---------------------------------------------------------------------------
# Reusable diagram-page kit (candidate for a shared module)
# ---------------------------------------------------------------------------
BOLD_FONTS = ("TTD9974692", "MalgunGothicBold")   # KDN PDF: bold face ids
SYMBOL_FONTS = ("TTF97B79EF",)                     # ･ ∙ : inherit weight of the neighbour


def _source_lines():
    out = []
    for block in source.page.get_text("dict", flags=pymupdf.TEXTFLAGS_TEXT)["blocks"]:
        for line in block.get("lines", []):
            spans = [s for s in line["spans"] if s["text"]]
            text = "".join(s["text"] for s in spans).strip()
            if text:
                out.append(dict(bbox=line["bbox"], spans=spans, text=text))
    return out


LINES = _source_lines()


def lines_in(x0, x1, y0, y1):
    """Same selection rule as SourcePage.region, but returns line dicts with spans."""
    hits = [l for l in LINES if x0 <= l["bbox"][0] < x1 and y0 <= l["bbox"][1] < y1]
    return sorted(hits, key=lambda l: (l["bbox"][1], l["bbox"][0]))


def line1(*bounds):
    hits = lines_in(*bounds)
    if len(hits) != 1:
        raise ValueError(f"Expected one source line in {bounds}, got {[h['text'] for h in hits]}")
    return hits[0]


def runs_of(line, color=INK, scale=1.0, bold=None, x0=-1e9, x1=1e9):
    """PDF spans -> [(text, size, bold, color)] with leading/trailing blanks stripped.
    x0/x1 keep only spans starting inside that x range (split one PDF line across cells)."""
    runs, prev = [], False
    for s in line["spans"]:
        if not x0 <= s["bbox"][0] < x1:
            continue
        b = any(f in s["font"] for f in BOLD_FONTS)
        if any(f in s["font"] for f in SYMBOL_FONTS):
            b = prev
        if bold is not None:
            b = bold
        size = int(round(s["size"] * scale * 10)) * 10
        if runs and runs[-1][1] == size and runs[-1][2] == b:
            runs[-1][0] += s["text"]
        else:
            runs.append([s["text"], size, b, color])
        prev = b
    runs[0][0] = runs[0][0].lstrip()
    runs[-1][0] = runs[-1][0].rstrip()
    return [tuple(r) for r in runs if r[0]]


def strip_runs(runs):
    runs = [list(r) for r in runs]
    runs[0][0] = runs[0][0].lstrip()
    runs[-1][0] = runs[-1][0].rstrip()
    return [tuple(r) for r in runs if r[0]]


def adv(ch):
    """Advance width in em, measured from this PDF's embedded fonts (hangul = 0.865 em)."""
    o = ord(ch)
    if ch == " ":
        return 0.29
    if 0xAC00 <= o <= 0xD7A3 or 0x3130 <= o <= 0x318F or 0x4E00 <= o <= 0x9FFF or 0xF900 <= o <= 0xFAFF:
        return 0.865
    if ch.isdigit():
        return 0.558
    if ch.isupper():
        return 0.65
    if ch.islower():
        return 0.5
    if ch in ".,:;'’‘()[]/|!･∙·":
        return 0.31
    if ch in "“”\"":
        return 0.41
    return 0.9


def text_width(runs, ratio):
    """Estimated KoPub width in pt; ratio 86.5 reproduces the PDF's own width."""
    return sum(adv(ch) * size / 100 for text, size, *_ in runs for ch in text) * ratio / 86.5


STROKES = {"strong": ("SOLID", "0.3 mm", "#555555"), "mid": ("SOLID", "0.2 mm", "#808080"),
           "soft": ("SOLID", "0.1 mm", "#ABABAB"), "dot": ("DOT", "0.1 mm", "#9A9A9A")}


@lru_cache(None)
def frame(fill=None, top=None, bottom=None, left=None, right=None, hatch=None):
    """borderFill with independent sides (builder.border only has 'sides' for both)."""
    el = deepcopy(L.borders[0])
    for side, kind in (("left", left), ("right", right), ("top", top), ("bottom", bottom)):
        if kind:
            edge = L.get(el, f"hh:{side}Border")
            for key, val in zip(("type", "width", "color"), STROKES[kind]):
                edge.set(key, val)
    if fill:
        brush = L.sub(el, "hc:fillBrush")
        attrs = dict(faceColor=fill, hatchColor=hatch or "#E1E1E1", alpha="0")
        if hatch:
            attrs["hatchStyle"] = "BACK_SLASH"
        L.sub(brush, "hc:winBrush", **attrs)
    return L.append_style(L.borders, el)


# Superscript counts (4회, 18개 ...) are 60 % of the line size in this PDF, i.e. Hancom 위 첨자.
# False: small runs on the baseline (safe, previewable). True: emit Hancom's own <hh:supscript/>
# on a full-size run (as python-hwpx and Hancom write it); not yet checked in the target editor
# and invisible to tools/hwpx_preview.py.
SUPERSCRIPT = False
SUP_RATIO = 0.65


@lru_cache(None)
def sup_char(size, bold, color, ratio):
    base = L.characters.find(f"hh:charPr[@id='{L.char(size, bold, color, ratio)}']", L.ns)
    el = deepcopy(base)
    L.sub(el, "hh:supscript")
    return L.append_style(L.characters, el)


def para(runs, align="LEFT", line=None, ratio=90, before=0, after=0):
    top = max(r[1] for r in runs)
    line = line or max(1000, int(round(top * 1.16 / 10)) * 10)
    el = L.p("", top, align=align, line=line, before=before, after=after, ratio=ratio)
    el.remove(el[0])
    for text, size, bold, color in runs:
        if SUPERSCRIPT and size < top * SUP_RATIO:
            ref = sup_char(top, bold, color, ratio)
        else:
            ref = L.char(size, bold, color, ratio)
        L.sub(L.sub(el, "hp:run", charPrIDRef=ref), "hp:t").text = text
    return el, line


def blank():
    return L.p("", 100, line=100)


def to_x(x):
    if not X0 - 0.01 <= x <= X1 + 0.01:
        raise ValueError(f"x {x} outside body")
    return W if abs(x - X1) < 0.01 else int(round((x - X0) * 100))


class Grid:
    """One flat table. xs: column edges in PDF pt; hs: row heights in 1/100 pt."""

    def __init__(self, name, xs, hs):
        self.name, self.xs, self.hs = name, [to_x(x) for x in xs], list(hs)
        self.items, self.taken = {}, set()

    def put(self, x0, x1, r0, r1, content, fill="1", *, align="CENTER", size=1080, bold=False,
            color=INK, ratio=90, line=None, fit=True):
        """content: str | line dict | run list, or a list of those (one paragraph each)."""
        c0, c1 = self.xs.index(to_x(x0)), self.xs.index(to_x(x1))
        width, height = self.xs[c1] - self.xs[c0], sum(self.hs[r0:r1])
        items = content if isinstance(content, list) and not _is_runs(content) else [content]
        pars = []
        for item in items:
            if isinstance(item, str):
                pars.append([(item, size, bold, color)])
            elif isinstance(item, dict):
                pars.append(runs_of(item, color))
            else:
                pars.append([tuple(r) if len(r) == 4 else (*r, color) for r in item])
        if fit and pars:
            inner = (width - 500) / 100 * 0.96
            for runs in pars:
                need = text_width(runs, ratio)
                if need > inner:
                    ratio = int(ratio * inner / need)
            if ratio < 68:
                WARN.append(f"{self.name}: ratio {ratio} for {pars[0][0][0][:20]!r}")
        contents, used = [], 160
        for runs in pars:
            el, ln = para(runs, align, line, ratio)
            contents.append(el)
            used += ln
        if not contents:
            contents = [blank()]
        if used > height:
            WARN.append(f"{self.name}: cell {pars[0][0][0][:16]!r} needs {used} > {height}")
        for r in range(r0, r1):
            for c in range(c0, c1):
                if (r, c) in self.taken:
                    raise ValueError(f"{self.name}: overlap at row {r} col {c}")
                self.taken.add((r, c))
        self.items[r0, c0] = cell(c0, width, height, contents, fill, r1 - r0, c1 - c0)

    def rows(self):
        out = [[] for _ in self.hs]
        for (r, c), item in self.items.items():
            out[r].append(item)
        for r in range(len(self.hs)):
            c = 0
            while c < len(self.xs) - 1:
                if (r, c) in self.taken:
                    c += 1
                    continue
                start = c
                while c < len(self.xs) - 1 and (r, c) not in self.taken:
                    c += 1
                out[r].append(cell(start, self.xs[c] - self.xs[start], self.hs[r], [blank()], "1", 1, c - start))
            if not any(item[5] == 1 for item in out[r]):
                WARN.append(f"{self.name}: row {r} has no single-row cell")
        return [sorted(row, key=lambda item: item[0]) for row in out]


def _is_runs(value):
    return bool(value) and isinstance(value[0], tuple)


BLOCKS = []


def block(grid, top):
    """Queue a grid whose top edge sits at PDF y=top (pt); gaps are derived from the next top."""
    BLOCKS.append((grid, top))


def flush(end):
    for i, (grid, top) in enumerate(BLOCKS):
        nxt = BLOCKS[i + 1][1] if i + 1 < len(BLOCKS) else end
        gap = int(round((nxt - top) * 100)) - sum(grid.hs)
        if gap < 0:
            WARN.append(f"{grid.name}: {-gap} too tall for its PDF slot")
        L.add_table(grid.rows(), gap=max(gap, 0))


# Shared presets (same look as kdn_p50 / kdn_p51)
gray = L.border("#E9E9E9", top="soft", bottom="soft")
gray2 = L.border("#D8D8D8", top="strong", bottom="soft", sides="soft")
white = L.border(top="soft", bottom="soft", sides="soft")
dark = L.border("#686868", top="strong", bottom="soft")
outline = L.border(top="strong", bottom="soft", sides="soft")
striped = L.border("#E9E9E9", top="strong", bottom="soft", sides="soft", pattern=True)
pill = frame("#E3E3E3")
photo = frame("#E4E4E4", top="mid", left="mid", right="mid")
ARROW = "#A8A8A8"


def title_band(name, line, edges, top):
    """'다. [badge] title' : number, light pill badge and 14pt title in three cells."""
    runs = runs_of(line)
    g = Grid(name, edges, [1650])
    g.put(edges[0], edges[1], 0, 1, [strip_runs(runs[:1])], align="LEFT", line=1450)
    g.put(edges[1], edges[2], 0, 1, [runs[1]], pill)
    g.put(edges[2], edges[3], 0, 1, [strip_runs(runs[2:])], align="LEFT", line=1450)
    block(g, top)


def heading(name, line, top, badge=None, badge_x=503.0):
    """'□ heading' with an optional dark tag such as 지적사항 개선 (tag typed from its image)."""
    g = Grid(name, [X0, badge_x, X1] if badge else [X0, X1], [1600])
    g.put(X0, badge_x if badge else X1, 0, 1, [[("□ ", 1350, True, INK)] + runs_of(line)], align="LEFT", line=1400)
    if badge:
        g.put(badge_x, X1, 0, 1, badge, dark, size=900, bold=True, color=WHITE)
    block(g, top)


# ---------------------------------------------------------------------------
# Page 19
# ---------------------------------------------------------------------------
# Side tab (image in the PDF; typed like kdn_p51) and footer float outside the flow.
L.add_table([[cell(0, 3350, 1680, [para([("01", 1380, True, WHITE)], "CENTER")[0]], dark)],
             [cell(0, 3350, 5960, [para([(ch, 950, True, INK)], "CENTER", 1160)[0] for ch in "경영관리"], gray2)]],
            floating=(57800, 15000))
foot = [(only_text, size, False, INK) for only_text, size in (
    (line1(450, 455, 818, 822)["text"], 790), ("    ", 790), (line1(545, 552, 816, 820)["text"], 1090))]
L.add_table([[cell(0, W, 1500, [para(foot, "RIGHT", 1300)[0]])]], floating=(5660, 81550))

# Running head
g = Grid("head", [X0, 466.3, X1], [1680])
g.put(X0, 466.3, 0, 1, [], frame(bottom="soft"))
g.put(466.3, X1, 0, 1, [line1(460, 480, 35, 40)], align="RIGHT")
block(g, 32.0)

title_band("title-da", line1(55, 60, 70, 74), [X0, 76.5, 153.6, X1], 70.5)

# 다. Mission / vision / core-value block: an image in the PDF, text read from a 4x render.
xs = [X0, 110.0, 115.5, 139.5, 148.2, 260.4, 284.4, 293.0, 335.1, 368.0, 410.0, 434.0, 442.2, X1]
g = Grid("value-system", xs, [2500, 550, 2200, 550, 2150, 500, 1800, 380, 1800, 1100, 2000])
for r, text in ((0, "미 션"), (2, "비 전"), (4, "전환포인트")):
    g.put(X0, 110.0, r, r + 1, text, gray, size=1200, bold=True)
g.put(X0, 110.0, 6, 9, [[("핵심가치", 1200, True)], [("(V.A.L.U.E)", 1000, False)]], gray)
g.put(115.5, X1, 0, 1, "에너지ICT 기술 전문화 및 고도화를 통해 에너지산업 발전에 기여",
      striped, size=1300, bold=True)
segments = [(115.5, 148.2, 260.4), (260.4, 293.0, 410.0), (410.0, 442.2, X1)]
visions = ["디지털 혁신", "에너지 대전환 선도", "글로벌 에너지ICT의 중심"]
shifts = [("양적 성장 추구", "질적 미래 설계"), ("기술 운영 중심", "신기술 창출 성과"),
          ("안정 중심", "도전을 통한 혁신")]
cores = [("주도가치", "Visionary", "미래주도", "❶"), ("선도가치", "Advance", "기술선도", "❷"),
         ("도약가치", "Leap", "도전의식", "❸")]
for i, (a, b, e) in enumerate(segments):
    sep = "dot" if i < 2 else None
    g.put(a, a + 24.0, 2, 3, str(i + 1), dark, size=1300, bold=True, color=WHITE)
    g.put(a + 24.0, e, 2, 3, visions[i], frame(top="strong", right=sep), align="LEFT", size=1250, bold=True)
    pre, post = shifts[i]
    g.put(a, e, 4, 5, [[(pre + " ➜ ", 1150, False, INK), (post, 1150, True, INK)]], frame("#E9E9E9", right=sep))
    tag, name, kor, num = cores[i]
    g.put(a, b, 6, 7, tag, dark, size=900, color=WHITE)
    g.put(b, e, 6, 7, [[(name, 1250, True, INK), (f" ({kor}) {num}", 1100, False, INK)]],
          frame(top="strong", bottom="strong", right="strong" if i == 2 else None))
for (a, b, e), (name, kor, num) in zip([(115.5, 148.2, 335.1), (335.1, 368.0, X1)],
                                       [("Unity", "소통협력", "❹"), ("Ethic", "청렴윤리", "❺")]):
    g.put(a, b, 8, 9, "기저가치", frame("#D6D6D6"), size=900)
    g.put(b, e, 8, 9, [[(name, 1250, True, INK), (f" ({kor}) {num}", 1100, False, INK)]],
          frame(top="soft", bottom="soft", right="soft" if name == "Ethic" else None))
g.put(X0, X1, 9, 10, "▼", size=800, color="#8C8C8C", line=820)
g.put(X0, X1, 10, 11, [[("미션 ↔ 비전 ↔ 핵심가치의 정합성 제고로 ", 1150, False, WHITE),
                        ("“가치체계의 유기적 연계성 및 일관성 강화”", 1250, True, WHITE)]],
      frame("#6E6E6E", hatch="#7A7A7A"))
block(g, 93.6)

heading("heading-value", line1(65, 75, 255, 260), 256.5, badge="지적사항 개선")

# Three panels: background → 15 behaviours → company-wide sharing, chevrons in the gutters.
xs = [X0, 130.1, 144.6, 218.5, 232.4, 252.4, 317.5, 436.7, 450.7, 462.0, X1]
g = Grid("behaviour-panels", xs, [2150] + [1430] * 10)
for (a, e), x in (((X0, 218.5), 90), ((232.4, 436.7), 260), ((450.7, X1), 470)):
    g.put(a, e, 0, 1, [line1(x, x + 10, 278, 283)], gray2, bold=True)
side = dict(left="soft", right="soft")
g.put(X0, 218.5, 1, 2, [line1(70, 75, 298, 303)], gray)
g.put(X0, 218.5, 2, 5, lines_in(60, 215, 315, 360), frame(**side, bottom="soft"))
g.put(X0, 218.5, 5, 6, "▼", frame(**side), size=900, color=ARROW, line=1000)
g.put(X0, 218.5, 6, 7, [line1(95, 100, 376, 380)], gray)
g.put(X0, 130.1, 7, 11, lines_in(60, 130, 394, 440), frame(left="soft", bottom="soft"))
g.put(130.1, 144.6, 7, 11, "➜", frame(bottom="soft"), size=1000, color="#7A7A7A")
g.put(144.6, 218.5, 7, 11, lines_in(140, 215, 394, 440), frame(right="soft", bottom="soft"))
for k, y in enumerate((299.7, 328.1, 356.4, 384.8, 413.1)):
    r = 1 + 2 * k
    g.put(232.4, 252.4, r, r + 2, lines_in(235, 250, y - 1, y + 26), gray)
    name, kor = lines_in(265, 275, y - 1, y + 26)
    g.put(252.4, 317.5, r, r + 2, [[("❶❷❸❹❺"[k] + " ", 1090, True, INK)] + runs_of(name), kor],
          frame(bottom="soft"), align="LEFT")
    g.put(317.5, 436.7, r, r + 2, lines_in(320, 430, y - 1, y + 26), frame(bottom="soft", right="soft"))
# 전직원 공유 pledge card: an image in the PDF (about 4-5 pt text), read from a 4x render.
g.put(450.7, X1, 1, 3, [[("핵심가치 “VALUE”를 실현하기 위해", 560, True)],
                         [("다음과 같이 행동규범을 이행할 것을 약속합니다.", 560, True)]], frame(**side), line=900)
pledges = ["나는 트렌드 변화에 관심을 갖고 업무에 반영한다", "나는 최신 동향 학습으로 최고의 전문가로 성장한다",
           "나는 도전적 과제에 주도적으로 임하고 책임을 갖는다", "나는 타인의 의견을 경청하고 다양한 관점을 존중한다",
           "나는 부당한 이익을 요구하거나 수용하지 않는다"]
for i, (letter, text) in enumerate(zip("VALUE", pledges)):
    g.put(450.7, 462.0, 3 + i, 4 + i, letter, frame("#686868", left="soft", bottom="soft"),
          size=900, bold=True, color=WHITE)
    g.put(462.0, X1, 3 + i, 4 + i, text, frame(right="soft", bottom="soft"), align="LEFT", size=480, bold=True)
g.put(450.7, X1, 8, 11, lines_in(455, 550, 398, 440), frame("#E6E6E6", **side, bottom="soft"))
for a, e in ((218.5, 232.4), (436.7, 450.7)):
    g.put(a, e, 4, 8, "▶", size=1000, color=ARROW)
block(g, 275.8)

title_band("title-ra", line1(55, 60, 446, 450), [X0, 76.5, 140.6, X1], 446.5)
heading("heading-internal", line1(65, 75, 468, 472), 468.5)

# Roadmap: three stage boxes with chevrons.
xs = [X0, 90.0, 212.2, 228.6, 262.0, 383.8, 399.6, 433.0, X1]
g = Grid("roadmap", xs, [2130, 1870])
for k, (a, b, e, x) in enumerate(((X0, 90.0, 212.2, 65), (228.6, 262.0, 383.8, 250), (399.6, 433.0, X1, 418))):
    runs = runs_of(line1(x - 1, x + 1, 490, 494))
    badge = [r for r in runs if r[1] < 1000]
    head = runs[len(badge):]
    last = k == 2
    g.put(a, b, 0, 1, [badge], frame(WHITE, top="soft", bottom="soft", left="soft", right="soft"))
    g.put(b, e, 0, 1, [strip_runs([(t, s, bb, WHITE if last else INK) for t, s, bb, _ in head])],
          frame("#686868" if last else "#E9E9E9", top="soft", right="soft"))
    g.put(a, e, 1, 2, lines_in(a, e, 510, 515), frame(left="soft", right="soft", bottom="soft"))
for a, e in ((212.2, 228.6), (383.8, 399.6)):
    g.put(a, e, 0, 2, "▶", size=1300, color=ARROW)
block(g, 488.7)

# Four effort cards (badge + title, two bullets) and a photo + score chart column.
xs = [X0, 90.6, 247.0, 252.2, 286.2, 467.0, 471.6, 513.6, X1]
g = Grid("effort-cards", xs, [1840, 3570, 840, 1580, 1150, 1150, 1230])
for (a, b, e), hx, hy, rows in (((X0, 90.6, 247.0), 60, 537, (0, 1, 2)), ((252.2, 286.2, 467.0), 290, 537, (0, 1, 2)),
                                ((X0, 90.6, 247.0), 75, 597, (3, 4, 7)), ((252.2, 286.2, 467.0), 285, 597, (3, 4, 7))):
    runs = runs_of(line1(hx, hx + 10, hy, hy + 3))
    r0, r1, r2 = rows
    g.put(a, b, r0, r1, [runs[:1]], frame("#EFEFEF", top="mid", left="mid", bottom="soft", right="soft"))
    g.put(b, e, r0, r1, [strip_runs(runs[1:])], frame(top="mid", right="mid", bottom="soft"))
    g.put(a, e, r1, r2, lines_in(a, a + 10, hy + 15, hy + 50), frame("#F2F2F2", left="mid", right="mid", bottom="mid"),
          align="LEFT")
# Chart (image): photo omitted, values read from a 4x render.
g.put(471.6, X1, 0, 3, [], photo)
g.put(471.6, X1, 3, 4, "2.1점↑", frame("#5A5A5A", left="mid", right="mid"), size=900, bold=True, color=WHITE)
g.put(471.6, 513.6, 4, 5, "91.6점", frame(left="mid"), size=880, line=980)
g.put(513.6, X1, 4, 5, "93.7점", frame(right="mid"), size=880, bold=True, line=980)
g.put(471.6, 513.6, 5, 6, "’24년", frame(left="mid"), size=820, line=960)
g.put(513.6, X1, 5, 6, "’25년", frame(right="mid"), size=820, bold=True, line=960)
g.put(471.6, X1, 6, 7, [line1(470, 480, 634, 638)], frame("#E9E9E9", left="mid", right="mid", bottom="mid"), line=1000)
block(g, 533.9)

heading("heading-external", line1(65, 75, 655, 660), 656.0)

# Stakeholder table (one bullet per half row) and a photo + score chart column.
xs = [X0, 80.0, 121.0, 274.0, 468.0, 470.6, 513.2, X1]
g = Grid("stakeholder-table", xs, [1820] + [1350] * 8)
g.put(X0, 121.0, 0, 1, [line1(75, 80, 678, 682)], gray2, bold=True)
g.put(121.0, 274.0, 0, 1, [line1(165, 170, 678, 682)], gray2, bold=True)
g.put(274.0, 468.0, 0, 1, [line1(335, 340, 678, 682)], gray2, bold=True)
cellf = frame(bottom="soft", left="soft", right="soft")
g.put(X0, 80.0, 1, 7, lines_in(58, 62, 720, 750), cellf)
g.put(X0, 80.0, 7, 9, lines_in(58, 62, 775, 802), cellf)
customer = line1(85, 90, 775, 779)
for r, (y0, y1) in zip((1, 3, 5), ((694, 722), (722, 748), (748, 775))):
    g.put(80.0, 121.0, r, r + 2, lines_in(85, 120, y0, y1), cellf)
    g.put(121.0, 274.0, r, r + 2, lines_in(122, 272, y0, y1), cellf)
g.put(80.0, 121.0, 7, 9, [runs_of(customer, x1=120.0)], cellf)
g.put(121.0, 274.0, 7, 9, [runs_of(customer, x0=120.0), line1(130, 140, 788, 792)], cellf)
for r, bullet in enumerate(lines_in(274, 280, 690, 802), 1):
    g.put(274.0, 468.0, r, r + 1, [bullet], frame(left="soft", right="soft", bottom="soft" if r % 2 == 0 else None),
          align="LEFT", line=1180)
g.put(470.6, X1, 0, 4, [], photo)
g.put(470.6, X1, 4, 5, "2점↑", frame("#5A5A5A", left="mid", right="mid"), size=900, bold=True, color=WHITE)
g.put(470.6, 513.2, 5, 7, "85.6점", frame(left="mid"), size=900)
g.put(513.2, X1, 5, 7, "87.6점", frame(right="mid"), size=900, bold=True)
g.put(470.6, 513.2, 7, 8, "’24년", frame(left="mid"), size=850)
g.put(513.2, X1, 7, 8, "’25년", frame(right="mid"), size=850, bold=True)
g.put(470.6, X1, 8, 9, [line1(475, 480, 786, 790)], frame("#E9E9E9", left="mid", right="mid", bottom="mid"))
block(g, 675.9)

flush(end=803.0)
# Floating and flow tables otherwise share builder ids (5000 + paragraph count): make them unique.
for number, table in enumerate(L.section.iter(L.q("hp:tbl")), 5001):
    table.set("id", str(number))
for message in WARN:
    print("WARN", message)
print(L.write(target))
