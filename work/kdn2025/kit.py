"""Shared kit for diagram-heavy KDN report pages (extracted from p19.py).

Every box, flow and chart is one flat Hancom table per horizontal band, laid on a "union grid":
column edges are PDF x coordinates, rows are heights in 1/100 pt, cells are placed by edge
coordinates and uncovered grid slots are filled with borderless blank cells. Text comes from PDF
lines with their spans, and 장평 is fitted per cell from the PDF glyph metrics.

usage in a page script (work/kdn2025/pNN.py):

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import kit
    from kit import Layout, recipe_inputs
    source, target = recipe_inputs(NN, "<signature>")
    L = Layout(top=3100)
    kit.setup(source, L)
    from kit import *          # helpers and presets bound to this page
    ...
    kit.finish(target, end=<PDF y where the flow ends>)
"""

import sys
from copy import deepcopy
from functools import lru_cache
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".claude/skills/pdf-hwpx-layout/scripts"))

import pymupdf  # noqa: E402
from hwpx_layout import Layout, cell  # noqa: E402,F401
from pdf_coords import recipe_inputs  # noqa: E402,F401

W = 49900
X0, X1 = 56.6, 555.6          # PDF x of the body's left / right edge (= HWPX margins)
INK, WHITE = "#161616", "#FFFFFF"
ARROW = "#A8A8A8"
WARN, BLOCKS, LINES = [], [], []
L = source = None
gray = gray2 = white = dark = outline = striped = pill = photo = None

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



def setup(src, layout):
    """Bind the kit to one page: its PDF source and its Layout. Call before `from kit import *`."""
    global L, source, gray, gray2, white, dark, outline, striped, pill, photo
    L, source = layout, src
    LINES[:] = _source_lines()
    WARN.clear()
    BLOCKS.clear()
    frame.cache_clear()
    sup_char.cache_clear()
    # Shared presets (same look as kdn_p50 / kdn_p51)
    gray = L.border("#E9E9E9", top="soft", bottom="soft")
    gray2 = L.border("#D8D8D8", top="strong", bottom="soft", sides="soft")
    white = L.border(top="soft", bottom="soft", sides="soft")
    dark = L.border("#686868", top="strong", bottom="soft")
    outline = L.border(top="strong", bottom="soft", sides="soft")
    striped = L.border("#E9E9E9", top="strong", bottom="soft", sides="soft", pattern=True)
    pill = frame("#E3E3E3")
    photo = frame("#E4E4E4", top="mid", left="mid", right="mid")


def finish(target, end):
    """Lay out the queued bands (flow ends at PDF y=end), make table ids unique and write."""
    flush(end)
    # Floating and flow tables otherwise share builder ids (5000 + paragraph count).
    for number, table in enumerate(L.section.iter(L.q("hp:tbl")), 5001):
        table.set("id", str(number))
    for message in WARN:
        print("WARN", message)
    print(L.write(target))


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
