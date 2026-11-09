"""Rebuild the PART Ⅰ divider with its chapter contents (PDF page 7) as editable HWPX.

The left decorative column (Kdn logo, circles), "2025 / 경영실적 보고서", the "Ⅰ PART" numeral,
the "경영관리" title, the chapter-number brackets, the "계량" pills and the bottom rule are
images in the PDF; the text among them is typed and the shapes become cells. Dot leaders are
a dotted cell border.

usage: python3 work/kdn2025/p07.py <report.pdf> <out.hwpx> [--page N]
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kit  # noqa: E402
from kit import Layout, recipe_inputs  # noqa: E402

source, target = recipe_inputs(7, "재무성과관리")
L = Layout(top=4900)
kit.setup(source, L)
from kit import *  # noqa: E402,F401,F403

GRAY = "#6E6E6E"
NUM_L, NUM_R, ENTRY_L, PAGE_L, BAR_R = 208.0, 247.0, 253.0, 500.0, 532.0

# Header: "Ⅰ / PART" numeral with a rule, "2025 / 경영실적 보고서" at left, "경영관리" at right.
g = Grid("part-head", [X0, 160.0, 380.0, 485.0, 540.0, X1], [4500, 1500, 2500, 1700, 1800])
g.put(485.0, 540.0, 0, 1, "Ⅰ", size=4400, color=GRAY, ratio=100, line=4400)
g.put(485.0, 540.0, 1, 2, "PART", frame(top="soft"), size=1100, color=GRAY, ratio=100, line=1200)
g.put(540.0, X1, 1, 2, [], frame(top="soft"))
g.put(X0, 160.0, 3, 4, "2025", align="LEFT", size=1300, ratio=100)
g.put(X0, 160.0, 4, 5, "경영실적 보고서", align="LEFT", size=1300, ratio=100)
g.put(380.0, X1, 3, 5, "경영관리", align="RIGHT", size=3000, bold=True, ratio=100, line=3300)
block(g, 50.0)


def entry_cells(g, row, title, pill, page, h):
    """[title][optional 계량 pill][dotted leader][page], laid on this grid's own x edges."""
    g.put(ENTRY_L, row["title_end"], h, h + 1, title, align="LEFT", size=1300, ratio=100)
    start = row["title_end"]
    if pill:
        g.put(start, row["pill_end"], h, h + 1, pill, frame("#DADADA"), size=1000, bold=True, ratio=100)
        start = row["pill_end"]
    g.put(start, PAGE_L, h, h + 1, [], frame(bottom="dot"))
    g.put(PAGE_L, BAR_R, h, h + 1, page, align="RIGHT", size=1300, ratio=100)


chapters = lines_in(215, 220, 200, 700)            # "01" .. "04"
heads = lines_in(250, 255, 200, 700)               # chapter titles (x 252) and entries (x 253)
for k, number in enumerate(chapters):
    top = number["bbox"][1]
    nxt = chapters[k + 1]["bbox"][1] if k + 1 < len(chapters) else 780.0
    title = line1(250, 253, top - 2, top + 6)
    rows = []
    for line in lines_in(253, 254, top + 20, nxt - 10):
        y = line["bbox"][1]
        pills = lines_in(330, 350, y - 2, y + 2)
        name, _, rest = line["text"].partition("·")
        if pills:
            pill_text, _, rest = pills[0]["text"].partition("·")
        elif name.rstrip().endswith("계량"):           # PyMuPDF may join the pill into the title line
            pills, pill_text = [True], "계량"
            name = name.rstrip()[:-2]
        page = rest.strip("·").strip()
        width = text_width([(name.rstrip(), 1300, False, INK)], 86.5)
        end = round(ENTRY_L + width * 1.2 + 6, 1)
        rows.append(dict(name=name.rstrip(), pill=pill_text.strip() if pills else None, page=page,
                         title_end=end, pill_end=round(end + 33, 1)))
    xs = {X0, NUM_L, NUM_R, ENTRY_L, PAGE_L, BAR_R, X1}
    for row in rows:
        xs |= {row["title_end"], row["pill_end"]} if row["pill"] else {row["title_end"]}
    g = Grid(f"chapter-{k + 1}", sorted(xs), [2500, 900] + [1960] * len(rows))
    g.put(NUM_L, NUM_R, 0, 1, [runs_of(number)], frame(left="mid", top="mid", bottom="mid"), ratio=100, line=2300)
    g.put(NUM_R, BAR_R, 0, 1, [runs_of(title)], frame("#EFEFEF"), align="LEFT", ratio=100)
    for h, row in enumerate(rows, 2):
        entry_cells(g, row, row["name"], row["pill"], row["page"], h)
    block(g, top - 3.0)

rule = Grid("bottom-rule", [X0, 79.0, 532.0, X1], [300])
rule.put(79.0, 532.0, 0, 1, [], frame("#C8C8C8"))
block(rule, 794.0)
kit.finish(target, end=798.0)
