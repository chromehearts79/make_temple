"""Shared builder for the 계량지표 summary pages of the KDN 2025 report (report pages 113-117).

Every page of this type has the same frame: running head (odd) or PART box (even), the
지표명 / 가중치 / 평가방법 box, the contact table, four numbered section bands (1 실적 개요 with its
score table and optional 보정근거 / 보정사유 notes, 2 실적 내용 and 3 항목별 분석 bullet boxes,
4 실적 산출내역 with (단위 : 백만원) and the yearly data table), footnotes and the footer. `frame_page()`
lays all of that out from the PDF's own text, vector rules and image boxes; a page script adds
only its score table (its merges differ per indicator) with the `Table` cell helpers and passes it
in. Image-only parts are typed: the 지표명 / 가중치 / 평가방법 labels, the side tab, the PART box and
the 한전KDN logo name; section bands, rounded boxes and note chips are images in the PDF and
become filled / outlined cells.

usage (work/kdn2025/p1NN.py):

    import metric_page as mp
    mp.start(L, "<signature>")
    t = mp.Table("scores", cols, rules)      # 1 실적 개요 table on the PDF's column / row rules
    ...
    mp.frame_page(odd=True, scores=t, data=dict(cols=..., rules=..., mid=None))
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kit  # noqa: E402
from kit import (Grid, INK, WHITE, Layout, W, X0, X1, block, cell, frame, line1, lines_in,  # noqa: E402,F401
                 para, recipe_inputs, runs_of, to_x)

DARK, BAND = "#6A6A6A", "#E5E5E5"          # section number box / band
HEAD, LIGHT = "#D7D7D7", "#EBEBEB"         # table header / label column
CONTACT = "#EAEAEA"                        # contact table name, phone, e-mail cells
TOP25 = "#7E7E7E"                          # '25년 header of the data table
CHIP = "#D9D9D9"                           # 보정근거 / 보정사유 chips
BULLET = "#999A99"                         # the gray ∙ of the bullet boxes (PDF span colour)

kit.STROKES["heavy"] = ("SOLID", "0.5 mm", "#323232")   # frame around the '25년 column(s)
kit.STROKES["sep"] = ("SOLID", "0.3 mm", "#FFFFFF")     # white separators inside gray header rows

source = target = None


def start(local, signature):
    """Open the PDF page, bind the kit and return (source, Layout)."""
    global source, target
    source, target = recipe_inputs(local, signature)
    layout = Layout(top=3100)
    kit.setup(source, layout)
    return source, layout


def margin(g, x0, r0, **sides):
    """Override a placed cell's padding (1/100 pt); unspecified sides keep the builder default."""
    key = (r0, g.xs.index(to_x(x0)))
    item = g.items[key]
    pad = dict(left=320, right=180, top=80, bottom=80)
    pad.update(item[7] or {})
    pad.update({k: int(v) for k, v in sides.items()})
    g.items[key] = item[:7] + (pad,)


def cell_runs(x0, x1, y0, y1, color=INK):
    """Runs of every PDF line in the y range whose spans start inside [x0, x1) (one paragraph each)."""
    out = []
    for line in sorted((l for l in kit.LINES if y0 <= l["bbox"][1] < y1),
                       key=lambda l: (l["bbox"][1], l["bbox"][0])):
        spans = [s for s in line["spans"] if x0 <= s["bbox"][0] < x1]
        if spans and "".join(s["text"] for s in spans).strip():
            out.append(runs_of(line, color, x0=x0, x1=x1))
    return out


# ---------------------------------------------------------------------------
# Tables on the PDF's rules
# ---------------------------------------------------------------------------
class Table(Grid):
    """Grid whose rows are the PDF's horizontal rules (pt); cells take the text found inside them."""

    def __init__(self, name, cols, rules, extra=()):
        """extra: further column edges (pt) that only some cells use, e.g. split row labels."""
        super().__init__(name, sorted(set(cols) | set(extra)),
                         [int(round((b - a) * 100)) for a, b in zip(rules, rules[1:])])
        self.cols, self.rules = cols, rules

    def text(self, x0, x1, r0, r1, color=INK):
        return cell_runs(x0, x1, self.rules[r0], self.rules[r1], color)

    def head(self, x0, x1, r0=0, r1=1, *, fill=HEAD, color=INK, top="mid", bottom="sep", left=None,
             right="sep", content=None, **kw):
        """Gray header cell: top rule, white separator at the right and below."""
        if x1 == self.cols[-1] and right == "sep":
            right = None
        content = self.text(x0, x1, r0, r1, color) if content is None else content
        self.put(x0, x1, r0, r1, content, frame(fill, top=top, bottom=bottom, left=left, right=right), **kw)

    def body(self, x0, x1, r0, r1=None, *, fill=None, bottom=None, left=None, right="soft", top=None,
             content=None, **kw):
        """Body cell: soft rule below (mid on the last row) and at the right (none at the body edge)."""
        r1 = r0 + 1 if r1 is None else r1
        if bottom is None:
            bottom = "mid" if r1 == len(self.hs) else "soft"
        if x1 == self.cols[-1] and right == "soft":
            right = None
        content = self.text(x0, x1, r0, r1) if content is None else content
        self.put(x0, x1, r0, r1, content, frame(fill, top=top, bottom=bottom, left=left, right=right), **kw)

    def head_row(self, cols=None, r0=0, r1=1, **kw):
        cols = cols or self.cols
        for a, e in zip(cols, cols[1:]):
            self.head(a, e, r0, r1, **kw)


def split_scores(year, sub, rules):
    """1 실적 개요 table whose 2025 row splits into 실제 / 보정 (영업이익률, 부채비율 pages).
    year / sub: x of the 2025 | 실제 and 실제 | 평가산식 edges; rules: header top, header bottom,
    실제 bottom, 보정 bottom, 2024 bottom, 2023 bottom. 목표치 and 가중치 are shared by 실제 / 보정,
    평가산식 and 평가방법 merged over all years."""
    cols = [X0, year, sub, 260.8, 311.8, 382.7, 433.7, 484.7, 518.7, X1]
    t = Table("scores", cols, rules)
    t.head(X0, sub)
    t.head_row(cols[2:])
    t.body(X0, year, 1, 3, fill=LIGHT)                                  # 2025
    for r in (1, 2):
        t.body(year, sub, r, fill=LIGHT, right=None)                      # 실제 / 보정
        for a, e in ((382.7, 433.7), (433.7, 484.7), (518.7, X1)):
            t.body(a, e, r)
    t.body(311.8, 382.7, 1, 3, align="LEFT", line=1540)                 # 최고 / 최저
    t.body(484.7, 518.7, 1, 3)                                          # 가중치
    t.body(sub, 260.8, 1, 5)                                            # 평가산식
    t.body(260.8, 311.8, 1, 5, line=1540)                               # 목표부여 (편차)
    for r in (3, 4):
        t.body(X0, sub, r, fill=LIGHT, right=None)
        t.body(311.8, 382.7, r, align="LEFT", line=1540)
        for a, e in zip(cols[5:], cols[6:]):
            t.body(a, e, r)
    return t


def label_chars(x0, x1, y0, y1):
    """(char, x0, x1) of the PDF glyphs in a label cell, left to right."""
    out = []
    for blk in source.page.get_text("rawdict")["blocks"]:
        for line in blk.get("lines", []):
            if not (x0 <= line["bbox"][0] < x1 and y0 <= line["bbox"][1] < y1):
                continue
            for span in line["spans"]:
                out += [(c["c"], c["bbox"][0], c["bbox"][2]) for c in span["chars"]]
    return sorted(out, key=lambda c: c[1])


def label_parts(x1, y0, y1):
    """Row label such as '매   출   액(A)' -> (words, suffix, first x, split x, end x).
    The PDF letter-spaces with real blanks; a double blank marks a word gap ('일반관리비 관리')."""
    chars = label_chars(X0, x1, y0, y1)
    cut = next(i for i, c in enumerate(chars) if c[0] == "(")
    words = "".join(c[0] for c in chars[:cut]).strip()
    words = words.replace("  ", "\0").replace(" ", "").replace("\0", " ")
    suffix = "".join(c[0] for c in chars[cut:]).strip()
    first, paren, end = chars[0][1], chars[cut][1], chars[-1][2]
    return words, suffix, first, round(paren - 0.15 * (end - paren), 1), end


def split_label(t, x1, r, fill=LIGHT, bottom=None):
    """Letter-spaced words as a distributed cell (배분 정렬) over the PDF extent, the '(A)' suffix
    right-aligned in its own cell ending where the PDF's does."""
    words, suffix, first, split, end = label_parts(x1, t.rules[r], t.rules[r + 1])
    bottom = bottom or ("mid" if r + 1 == len(t.hs) else "soft")
    # a tightly printed label ('일반관리비 관리') may need a narrower 장평 to stay on one line
    inner = (split - first) * 0.96
    need = kit.text_width([(words, 1090, False, INK)], 90)
    ratio = 90 if need <= inner else int(90 * inner / need)
    t.put(X0, split, r, r + 1, words, frame(fill, bottom=bottom), align="DISTRIBUTE", size=1090, ratio=ratio,
          fit=False)
    margin(t, X0, r, left=(first - X0) * 100, right=0)
    t.put(split, x1, r, r + 1, suffix, frame(fill, bottom=bottom, right="soft"), align="RIGHT", size=1090,
          fit=False)
    margin(t, split, r, left=0, right=(x1 - end) * 100)


def data_table(cols, rules, mid=None):
    """4 실적 산출내역 table. cols: [X0, label | '20년 ... '24년 | '25년 (or 실제, 보정), X1];
    rules: header top, header bottom, then each row bottom; mid: y between '25년 and 실제 / 보정."""
    split = mid is not None
    n25 = 2 if split else 1
    first25 = cols[-1 - n25]
    rows = [rules[0], mid, *rules[1:]] if split else rules
    nh = 2 if split else 1
    cuts = [label_parts(cols[1], a, b)[3] for a, b in zip(rows[nh:], rows[nh + 1:])]
    t = Table("data", cols, rows, cuts)
    for a, e in zip(cols, cols[1:]):
        if a >= first25:
            continue
        right = "heavy" if e == first25 else "sep"
        t.head(a, e, 0, nh, right=right)
    lid = dict(fill=TOP25, color=WHITE, top="heavy", left="heavy", right="heavy")
    if split:
        t.head(first25, X1, 0, 1, content=cell_runs(first25, X1, rules[0], mid, WHITE), **lid)
        t.head(first25, cols[-2], 1, 2, fill=TOP25, color=WHITE, top="sep", left="heavy", right="sep")
        t.head(cols[-2], X1, 1, 2, fill=TOP25, color=WHITE, top="sep", right="heavy")
    else:
        t.head(first25, X1, 0, 1, **lid)
    last = len(t.hs) - 1
    for r in range(nh, len(t.hs)):
        split_label(t, cols[1], r)
        for a, e in zip(cols[1:], cols[2:]):
            bottom = "heavy" if r == last and a >= first25 else None
            if a >= first25:
                left = "heavy" if a == first25 else None
                right = "heavy" if e == X1 else "soft"
            else:
                left, right = None, ("heavy" if e == first25 else "soft")
            t.body(a, e, r, fill=None, bottom=bottom, left=left, right=right)
    return t


# ---------------------------------------------------------------------------
# Page frame
# ---------------------------------------------------------------------------
def chrome(odd):
    L = kit.L
    if odd:
        # running head over a rule, side tab, footer at the right (as p97)
        L.add_table([[cell(0, 3350, 1680, [para([("01", 1380, True, WHITE)], "CENTER")[0]], kit.dark)],
                     [cell(0, 3350, 5960, [para([(ch, 950, True, INK)], "CENTER", 1160)[0] for ch in "경영관리"],
                           kit.gray2)]],
                    floating=(57800, 15000))
        foot = [(line1(450, 455, 818, 822)["text"], 790, False, INK), ("    ", 790, False, INK),
                (line1(540, 552, 816, 820)["text"], 1090, False, INK)]
        L.add_table([[cell(0, W, 1500, [para(foot, "RIGHT", 1300)[0]])]], floating=(5660, 81550))
        head = line1(400, 556, 35, 40)
        edge = round(head["bbox"][0] - 4.7, 1)
        g = Grid("head", [X0, edge, X1], [1680])
        g.put(X0, edge, 0, 1, [], frame(bottom="soft"))
        g.put(edge, X1, 0, 1, [head], align="RIGHT")
        block(g, 32.0)
    else:
        # PART label at the left of a rule; footer at the left with the logo's name (as p96)
        foot = [(line1(55, 60, 815, 822)["text"], 1090, False, INK), ("   ", 1090, False, INK),
                ("한전KDN㈜", 1090, True, INK)]
        L.add_table([[cell(0, W, 1500, [para(foot, "LEFT", 1300)[0]])]], floating=(5660, 81550))
        g = Grid("part-head", [X0, 103.5, 160.0, X1], [1500])
        g.put(X0, 103.5, 0, 1, [[("PART ", 800, False), ("01", 1300, True)]], line=1300)
        g.put(103.5, 160.0, 0, 1, "경영관리", frame("#333333"), size=1080, bold=True, color=WHITE)
        g.put(160.0, X1, 0, 1, [], frame(bottom="soft"))
        block(g, 32.0)


def indicator():
    """지표명 / 가중치 / 평가방법 box (labels are images in the PDF; typed), as p97."""
    xs = [X0, 103.0, 113.0, 405.0, 413.0, 474.0, 479.0, 551.7, X1]
    g = Grid("indicator", xs, [580, 1160, 3340])
    g.put(X0, 103.0, 0, 3, "지표명", frame(top="mid", left="mid", bottom="mid"), size=1090, bold=True)
    g.put(103.0, 113.0, 0, 3, "▶", size=600, color="#9A9A9A", fit=False)
    g.put(113.0, X1, 0, 1, [], frame(top="mid"))
    g.put(113.0, 405.0, 1, 3, [line1(150, 300, 89, 94)], frame("#ECECEC", hatch="#DDDDDD"), bold=True, line=1700)
    tab = frame(WHITE, top="mid", left="mid", right="mid", bottom="soft")
    value = frame("#E5E5E5")
    g.put(413.0, 474.0, 1, 2, "가중치", tab, size=1000, bold=True, line=1000)
    g.put(413.0, 474.0, 2, 3, [line1(413, 480, 101, 105)], value)
    g.put(479.0, 551.7, 1, 2, "평가방법", tab, size=1000, bold=True, line=1000)
    g.put(479.0, 551.7, 2, 3, [line1(480, 550, 101, 105)], value)
    block(g, 70.9)


def contacts():
    """직위 / 성명 / 연락처 / e-mail table; letter-spaced cells use distributed alignment (as p97)."""
    cols = [X0, 184.3, 260.8, 374.2, X1]
    tops = [159.2, 177.7, 196.1]
    g = Grid("contacts", cols, [1840, 1840, 1840, 1850])
    for k, (a, e) in enumerate(zip(cols, cols[1:])):
        g.put(a, e, 0, 1, [line1(a, e, 140, 144)], frame(top="strong", bottom="soft", left="soft" if k else None,
                                                       right="soft" if k < 3 else None), size=1040)
    for r, y in enumerate(tops, 1):
        edge = "strong" if r == len(tops) else "soft"
        rank = "".join(l["text"] for l in lines_in(X0, 184.3, y - 1, y + 3)).replace(" ", "")
        name = "".join(l["text"] for l in lines_in(184.3, 260.8, y - 1, y + 3)).replace(" ", "")
        g.put(X0, 184.3, r, r + 1, rank, frame(bottom=edge, right="soft"), align="DISTRIBUTE", size=1090)
        margin(g, X0, r, left=(70.9 - X0) * 100, right=(184.3 - 170.1) * 100)
        g.put(184.3, 260.8, r, r + 1, name, frame(CONTACT, bottom=edge, right="soft"), align="DISTRIBUTE",
              size=1090)
        margin(g, 184.3, r, left=(198.4 - 184.3) * 100, right=(260.8 - 246.6) * 100)
        g.put(260.8, 374.2, r, r + 1, [line1(270, 300, y - 1, y + 3)], frame(CONTACT, bottom=edge, right="soft"))
        g.put(374.2, X1, r, r + 1, [line1(390, 440, y - 1, y + 3)], frame(CONTACT, bottom=edge))
    block(g, 137.1)


def sections():
    """Band rects (4 numbered section bars) and the rounded box rects of sections 2 and 3 (images)."""
    imgs = [item["bbox"] for item in source.page.get_image_info()]
    bands = sorted((b for b in imgs if b[2] - b[0] > 490 and 20 < b[3] - b[1] < 26), key=lambda b: b[1])
    if len(bands) != 4:
        raise ValueError(f"expected 4 section bands, got {bands}")
    boxes = []
    for k in (1, 2):
        parts = [b for b in imgs if b[1] > bands[k][3] and b[3] < bands[k + 1][1] + 0.5 and b[0] < 61]
        boxes.append((min(b[1] for b in parts), max(b[3] for b in parts)))
    return bands, boxes


def band(name, rect, unit=False):
    y0, y1 = rect[1], rect[3]
    number = line1(60, 80, y0, y1)
    title = line1(85, 200, y0, y1)
    edges = [X0, 84.5, 470.0, X1] if unit else [X0, 84.5, X1]
    g = Grid(name, edges, [2300])
    g.put(X0, 84.5, 0, 1, [runs_of(number, WHITE)], frame(DARK), line=1700)
    g.put(84.5, edges[2], 0, 1, [title], frame(BAND), align="LEFT", line=1700)
    if unit:
        u = line1(480, 556, y0, y1)
        g.put(470.0, X1, 0, 1, [u], frame(BAND), align="RIGHT", line=1000)
        # the unit sits on the band's lower edge in the PDF
        shift = (u["bbox"][1] + u["bbox"][3]) / 2 - (y0 + y1) / 2
        margin(g, 470.0, 0, right=(X1 - u["bbox"][2]) * 100, top=80 + 200 * shift, bottom=80)
    block(g, y0)


def bullets(lines):
    """Bullet lines: gray ∙ run; a line's leading blanks (sub items '  - ...') kept as spaces."""
    out = []
    for line in lines:
        runs = runs_of(line)
        if runs[0][0].startswith("∙"):
            text, size, bold, _ = runs[0]
            runs = [("∙", size, bold, BULLET)] + ([(text[1:], size, bold, INK)] if text[1:] else []) + runs[1:]
        raw = "".join(s["text"] for s in line["spans"])
        lead = len(raw) - len(raw.lstrip(" "))
        if lead:
            runs = [(" " * lead, runs[0][1], False, INK)] + runs
        out.append(runs)
    return out


def box(name, top, bottom):
    lines = lines_in(60, 556, top, bottom)
    tops = [l["bbox"][1] for l in lines]
    pitch = min((b - a for a, b in zip(tops, tops[1:])), default=17.7)
    g = Grid(name, [X0, X1], [int(round((bottom - top) * 100))])
    g.put(X0, X1, 0, 1, bullets(lines), frame(top="soft", bottom="soft", left="soft", right="soft"),
          align="LEFT", line=int(round(pitch * 100)), fit=False)
    margin(g, X0, 0, left=(lines[0]["bbox"][0] - X0) * 100, right=200)
    block(g, top)


def notes(y0, y1):
    """보정근거 / 보정사유: gray chip (image in the PDF) + text; continuation lines under the text."""
    lines = lines_in(56, 120, y0, y1)
    bounds = [lines[0]["bbox"][1] - 0.3]
    bounds += [(a["bbox"][3] + b["bbox"][1]) / 2 for a, b in zip(lines, lines[1:])]
    bounds.append(lines[-1]["bbox"][3] + 0.5)
    g = Grid("notes", [X0, 93.7, X1], [int(round((b - a) * 100)) for a, b in zip(bounds, bounds[1:])])
    left = 96.4 - 93.7 - 0.5
    for r, line in enumerate(lines):
        # some PDF lines run past the body edge (to x 558); narrow 장평 so each stays on one line
        start = 96.4 if line["bbox"][0] > 80 else next(s["bbox"][0] for s in line["spans"] if s["bbox"][0] > 92)
        ratio = min(90, int(86.5 * (X1 - 93.7 - left) / (line["bbox"][2] - start) * 0.97))
        if line["bbox"][0] < 80:            # chip + text
            g.put(X0, 93.7, r, r + 1, [runs_of(line, x1=92.0)], frame(CHIP), line=1000)
            margin(g, X0, r, left=100, right=100, top=40, bottom=40)
            g.put(93.7, X1, r, r + 1, [runs_of(line, x0=92.0)], align="LEFT", line=1150, ratio=ratio, fit=False)
        else:
            g.put(93.7, X1, r, r + 1, [line], align="LEFT", line=1150, ratio=ratio, fit=False)
        margin(g, 93.7, r, left=left * 100, right=0, top=0, bottom=0)
    block(g, bounds[0])


def footnotes(y0, y1):
    lines = lines_in(55, 70, y0, y1)
    if not lines:
        return
    g = Grid("footnotes", [X0, X1], [1340] * len(lines))
    for r, line in enumerate(lines):
        g.put(X0, X1, r, r + 1, [line], align="LEFT", line=1150, fit=False)
        margin(g, X0, r, left=0, right=0, top=0, bottom=0)
    block(g, lines[0]["bbox"][1] - 0.5)


def frame_page(odd, scores, data, notes_range=None, end=808.0):
    """Lay out the whole page around the page script's score table and write the HWPX."""
    bands, boxes = sections()
    chrome(odd)
    indicator()
    contacts()
    band("sec1", bands[0])
    block(scores, scores.rules[0])
    if notes_range:
        notes(*notes_range)
    band("sec2", bands[1])
    box("result", *boxes[0])
    band("sec3", bands[2])
    box("analysis", *boxes[1])
    band("sec4", bands[3], unit=True)
    t = data_table(**data)
    block(t, t.rules[0])
    footnotes(t.rules[-1], 812)
    kit.finish(target, end=end)
