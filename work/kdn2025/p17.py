"""Rebuild KDN's physical PDF page 17 (printed page 5): Ⅲ. 2025년 주요 추진실적.

usage: python3 work/kdn2025/p17.py report.pdf out.hwpx [--page N]

Same three-column '24년/'25년/개선성과 block as the validated kdn_p49.py recipe. Text comes
from the PDF text layer cell by cell; mixed-size lines keep their small parenthesised and
superscript parts as smaller runs. The side tab and the "평가내용 0N" chips are images in the
source and are typed as editable cells, as in kdn_p49.py.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".claude/skills/pdf-hwpx-layout/scripts"))

import pymupdf  # noqa: E402
from hwpx_layout import Layout, cell  # noqa: E402
from pdf_coords import recipe_inputs  # noqa: E402

source, target = recipe_inputs(17, "경영혁신 및 경영성과 개선을 위한 계획수립과 이행을 위한 기관의 노력과 성과")
layout = Layout(top=3180)
add_text, add_table, border = layout.add_text, layout.add_table, layout.border
p = layout.p
reg, only = source.region, source.only
INK = "#161616"
TOP = []  # first paragraphs of cells that are top-aligned like the source columns


def vis(text):
    """Conservative em-width estimate (Hangul and symbols full width) at 100% ratio."""
    width = 0.0
    for ch in text:
        if ch == " ":
            width += .33
        elif ord(ch) < 128:
            width += .62 if (ch.isupper() or ch.isdigit()) else .55 if ch.islower() else .4
        elif ch in "･":
            width += .5
        else:
            width += 1.0
    return width


def runs_width(spans):
    return sum(vis(t) * size for t, size in spans)


def fit(lines, width, cap=90, floor=60):
    """Largest 장평 keeping every line (list of (text, size) runs) on one line in the cell."""
    need = max(runs_width(spans) for spans in lines)
    return max(floor, min(cap, int((width - 500) * 0.97 * 100 / need)))


def source_lines(x0, x1, y0, y1, base=1090, ref=10.89):
    """Lines as (text, size) runs: body-size spans map to `base`, smaller spans are scaled."""
    found = []
    for block in source.page.get_text("dict", flags=pymupdf.TEXTFLAGS_TEXT)["blocks"]:
        for line in block.get("lines", []):
            x, y = line["bbox"][:2]
            if not (x0 <= x < x1 and y0 <= y < y1):
                continue
            spans = []
            for span in line["spans"]:
                size = base if span["size"] >= ref * 0.9 else int(round(span["size"] / ref * base / 10)) * 10
                if spans and spans[-1][1] == size:
                    spans[-1][0] += span["text"]
                else:
                    spans.append([span["text"], size])
            spans[0][0] = spans[0][0].lstrip()
            spans[-1][0] = spans[-1][0].rstrip()
            spans = [(t, s) for t, s in spans if t]
            if spans:
                found.append((y, x, spans))
    lines = [spans for _, _, spans in sorted(found, key=lambda item: item[:2])]
    # Same text as SourcePage.region(), so the check against the PDF stays exact.
    assert ["".join(t for t, _ in spans) for spans in lines] == reg(x0, x1, y0, y1)
    # Continuation lines are indented under the bullet in the source.
    return [spans if spans[0][0].startswith("∙") else [("  " + spans[0][0], spans[0][1]), *spans[1:]]
            for spans in lines]


def para(spans, *, ratio, line=1760, before=0, bold=False, color=INK, align="LEFT"):
    el = p(spans[0][0], spans[0][1], bold, color, align=align, line=line, before=before, ratio=ratio)
    for text, size in spans[1:]:
        el.append(p(text, size, bold, color, align=align, line=line, ratio=ratio)[0])
    return el


def column(i, w, h, lines, fill, *, span=1, cols=1, before=700, line=1760, cap=90):
    ratio = fit(lines, w, cap=cap)
    contents = [para(spans, ratio=ratio, line=line, before=before if k == 0 else 0)
                for k, spans in enumerate(lines)]
    TOP.append(contents[0])
    return cell(i, w, h, contents, fill, span, cols)


def c(i, w, h, text, fill="1", *, bold=False, align="LEFT", size=1090, ratio=90, color=INK,
      span=1, cols=1, line=1250):
    values = [text] if isinstance(text, str) else text
    return cell(i, w, h, [p(t, size, bold, color, align=align, line=line, ratio=ratio) for t in values],
                fill, span, cols)


def tab(rows, gap=0):
    table = add_table(rows, gap=gap)
    for sub in table.iter(layout.q("hp:subList")):
        if len(sub) and any(sub[0] is first for first in TOP):
            sub.set("vertAlign", "TOP")
    return table


# Shared presets (same as the validated p49/p50 recipes).
gray2 = border("#D8D8D8", top="strong", bottom="soft", sides="soft")
grid = border(bottom="soft", sides="soft")
NONE = "1"

# --- side tab and running header ---
add_table([
    [cell(0, 3350, 1680, layout.center("01", 1380, True, "#FFFFFF"), border("#606060", top="strong"))],
    [cell(0, 3350, 5960, [p(ch, 950, True, align="CENTER", line=1160) for ch in "경영관리"], border("#D7D7D7"))],
], floating=(57800, 15000))
head = only(460, 480, 30, 45)
tab([[c(0, 40500, 1600, "", border(bottom="soft"), size=100, line=100),
      c(1, 9400, 1600, head, align="RIGHT", ratio=fit([[(head, 1090)]], 9400, cap=88))]])
add_text(only(200, 220, 65, 75), 1800, True, align="CENTER", line=2400, before=1700, after=1500, ratio=97)

W = (15100, 18900, 15900)  # '24년도까지의 실적 | '25년도 주요 실적 | 전년대비 개선성과
assert sum(W) == 49900


def band(number, titles, gap):
    """평가내용 banner: dark chip at the top-left, hatched title area (as kdn_p49.py)."""
    ratio = fit([[(t, 1240)] for t in titles], 42950)
    chip = [p(f"평가내용 {number:02}", 970, True, "#FFFFFF", align="CENTER", line=1150, ratio=74)]
    hatch = border("#E9E9E9", top="strong", bottom="soft", pattern=True)
    title = [p(t, 1240, line=1500, ratio=ratio) for t in titles]
    if len(titles) == 1:
        tab([[cell(0, 6950, 2650, chip, border("#565656", top="strong", bottom="soft")),
              cell(1, 42950, 2650, title, hatch)]], gap)
    else:
        tab([[cell(0, 6950, 1950, chip, border("#565656", top="strong")),
              cell(1, 42950, 3900, title, hatch, 2)],
             [cell(0, 6950, 1950, [p("", 100, line=100)], border("#E9E9E9", bottom="soft", pattern=True))]], gap)


def heading_row(y):
    heads = reg(50, 560, y - 4, y + 4)
    assert len(heads) == 3
    out, col = [], 0
    for j, (w, t) in enumerate(zip(W, heads)):
        out.append(cell(col, w, 2100, layout.center(t, 1090, True, "#FFFFFF" if j == 1 else INK),
                        border("#808080" if j == 1 else "#D7D7D7", top="strong", sides="soft"), 1,
                        4 if (j == 2 and y < 300) else 1))
        col += 1
    return out


left_fill = border(bottom="soft")
mid_fill = border("#EBEBEB", bottom="soft", sides="soft")

# --- 평가내용 01 ---
band(1, reg(120, 135, 108, 145), 800)
# The right column carries a small editable table: indent | 구 분 | '25년 | 전년대비.
R = (1400, 5600, 4400, 4500)
assert sum(R) == W[2]
H = (2600, 1650, 1800, 1800, 14150)
mini_head = border("#DCDCDC", top="strong", bottom="soft", sides="soft")
mini_name = border("#EDEDED", bottom="soft", sides="soft")
mini_value = grid


def mini(i, w, h, text, fill, bold=False):
    return c(i, w, h, text, fill, bold=bold, align="CENTER", size=990,
             ratio=min(90, int((w - 500) * 0.97 * 100 / (vis(text) * 990))))


rows = [heading_row(158)]
rows.append([column(0, W[0], sum(H), source_lines(55, 210, 180, 390), left_fill, span=5),
             column(1, W[1], sum(H), source_lines(210, 400, 180, 390), mid_fill, span=5),
             column(2, W[2], H[0], source_lines(400, 410, 183, 190), NONE, cols=4)])
rows.append([c(2, R[0], H[1] + H[2] + H[3], "", NONE, size=100, line=100, span=3),
             mini(3, R[1], H[1], only(425, 450, 203, 208), mini_head, True),
             mini(4, R[2], H[1], only(475, 500, 200, 208), mini_head, True),
             mini(5, R[3], H[1], only(510, 520, 203, 208), mini_head, True)])
for y in (219, 238):
    rows.append([mini(3, R[1], H[2], only(415, 425, y, y + 5), mini_name),
                 mini(4, R[2], H[2], only(470, 480, y, y + 5), mini_value),
                 mini(5, R[3], H[2], only(510, 520, y, y + 5), mini_value)])
rows.append([column(2, W[2], H[4], source_lines(400, 560, 270, 390), left_fill, cols=4, before=1700, line=1660)])
tab(rows, 3700)

# --- 평가내용 02 ---
band(2, [only(120, 135, 442, 450)], 1100)
tab([heading_row(478),
     [column(0, W[0], 22800, source_lines(55, 210, 500, 720), left_fill),
      column(1, W[1], 22800, source_lines(210, 400, 500, 720), mid_fill),
      column(2, W[2], 22800, source_lines(400, 560, 500, 720), left_fill)]])

# --- footer: two runs keep the source sizes (7.9pt title, 10.9pt page number) ---
footer = add_text(only(440, 540, 815, 830) + "   ", 800, align="RIGHT", line=1300, before=9100)
footer.append(p(only(545, 560, 815, 832), 1090)[0])

print(layout.write(target))
