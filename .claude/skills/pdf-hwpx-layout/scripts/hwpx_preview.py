"""Approximate visual preview of a generated HWPX page, side by side with the source PDF page.

This is NOT a Hancom renderer. Fonts and line breaking differ, so use it only to catch
gross problems: wrong cell mapping, missing columns, broken merges and page overflow.

usage: python3 scripts/hwpx_preview.py draft.hwpx out.png [--pdf report.pdf --page 13]
       python3 scripts/hwpx_preview.py draft.hwpx out.png --pdf p013.json.gz   (page snapshot)
       python3 scripts/hwpx_preview.py draft.hwpx out.png --ref screenshot.png  (any page picture)

Needs Node with the playwright package and a Chromium build (preinstalled in Claude cloud sessions).
"""

import argparse
import html
import json
import subprocess
import tempfile
import zipfile
from pathlib import Path

import pymupdf
from lxml import etree as E

NS = {
    "hh": "http://www.hancom.co.kr/hwpml/2011/head",
    "hc": "http://www.hancom.co.kr/hwpml/2011/core",
    "hp": "http://www.hancom.co.kr/hwpml/2011/paragraph",
}
SCALE = 1.65  # output pixels per point, same as pdf_coords.py page.png
SHOT_JS = Path(__file__).with_name("preview_shot.js")


def pt(hwpunit):
    return int(hwpunit) / 100


class Styles:
    def __init__(self, header):
        fonts = {f.get("id"): f.get("face") for f in
                 header.xpath('.//hh:fontface[@lang="HANGUL"]/hh:font', namespaces=NS)}
        self.chars = {}
        for c in header.xpath(".//hh:charPr", namespaces=NS):
            face = fonts.get(c.find("hh:fontRef", NS).get("hangul"), "")
            self.chars[c.get("id")] = dict(
                size=pt(c.get("height")), color=c.get("textColor"),
                bold="Bold" in face or c.find("hh:bold", NS) is not None,
                ratio=int(c.find("hh:ratio", NS).get("hangul")) / 100)
        self.paras = {}
        for p in header.xpath(".//hh:paraPr", namespaces=NS):
            spacing = p.find("hh:lineSpacing", NS)
            margin = p.find("hh:margin", NS)
            self.paras[p.get("id")] = dict(
                align=p.find("hh:align", NS).get("horizontal"),
                line_type=spacing.get("type"), line=int(spacing.get("value")),
                before=pt(margin.find("hc:prev", NS).get("value")),
                after=pt(margin.find("hc:next", NS).get("value")))
        self.borders = {}
        for b in header.xpath(".//hh:borderFill", namespaces=NS):
            css = []
            for side in ("top", "bottom", "left", "right"):
                edge = b.find(f"hh:{side}Border", NS)
                kind = edge.get("type")
                if kind == "NONE":
                    continue
                width = float(edge.get("width").split()[0])
                style = {"SOLID": "solid", "DOT": "dotted", "DASH": "dashed"}.get(kind, "solid")
                css.append(f"border-{side}:{max(width, 0.1)}mm {style} {edge.get('color')}")
            brush = b.find("hc:fillBrush/hc:winBrush", NS)
            if brush is not None and brush.get("faceColor") not in (None, "none"):
                face = brush.get("faceColor")
                if brush.get("hatchStyle"):
                    css.append(f"background:repeating-linear-gradient(-45deg,{face} 0 3px,"
                               f"{brush.get('hatchColor')} 3px 4px)")
                else:
                    css.append(f"background:{face}")
            self.borders[b.get("id")] = ";".join(css)


class Renderer:
    def __init__(self, styles):
        self.s = styles
        self.floating = []

    def paragraph(self, p):
        para = self.s.paras[p.get("paraPrIDRef")]
        blocks, spans, ratio, size = [], [], 1, 10
        for run in p.findall("hp:run", NS):
            char = self.s.chars[run.get("charPrIDRef")]
            for child in run:
                tag = E.QName(child).localname
                if tag == "tbl":
                    blocks.append(self.table(child, para["align"]))
                elif tag == "t" and child.text:
                    ratio, size = char["ratio"], char["size"]
                    weight = "font-weight:700;-webkit-text-stroke:0.6px currentColor" if char["bold"] else "font-weight:400"
                    spans.append(f'<span style="font-size:{char["size"]}pt;color:{char["color"]};{weight}">'
                                 f"{html.escape(child.text)}</span>")
        if para["line_type"] == "FIXED":
            line = f"{pt(para['line'])}pt"
        else:
            line = f"{para['line'] / 100 * 1.15:.2f}"
        align = {"CENTER": "center", "RIGHT": "right", "JUSTIFY": "justify"}.get(para["align"], "left")
        out = "".join(blocks)
        if spans:
            out += (f'<div style="margin:{para["before"]}pt 0 {para["after"]}pt;line-height:{line};'
                    f'text-align:{align};width:{100 / ratio:.2f}%;transform:scaleX({ratio});'
                    f'transform-origin:left top;white-space:pre-wrap">{"".join(spans)}</div>')
        elif not blocks:
            out += f'<div style="height:{pt(para["line"]) if para["line_type"] == "FIXED" else size}pt"></div>'
        return out

    def table(self, tbl, align="LEFT"):
        cells = []
        for row in tbl.findall("hp:tr", NS):
            for tc in row.findall("hp:tc", NS):
                addr, span, sz = (tc.find(f"hp:{k}", NS) for k in ("cellAddr", "cellSpan", "cellSz"))
                cells.append(dict(r=int(addr.get("rowAddr")), c=int(addr.get("colAddr")),
                                  rs=int(span.get("rowSpan")), cs=int(span.get("colSpan")),
                                  w=pt(sz.get("width")), h=pt(sz.get("height")), tc=tc))
        ncol = max(c["c"] + c["cs"] for c in cells)
        widths = [None] * ncol
        changed = True
        while changed:
            changed = False
            for c in cells:
                cols = range(c["c"], c["c"] + c["cs"])
                unknown = [i for i in cols if widths[i] is None]
                if len(unknown) == 1:
                    widths[unknown[0]] = max(c["w"] - sum(widths[i] for i in cols if widths[i] is not None), 1)
                    changed = True
        table_w = pt(tbl.find("hp:sz", NS).get("width"))
        rest = [i for i, w in enumerate(widths) if w is None]
        for i in rest:
            widths[i] = max((table_w - sum(w for w in widths if w)) / len(rest), 1)
        nrow = max(c["r"] + c["rs"] for c in cells)
        heights = [max([c["h"] for c in cells if c["r"] == r and c["rs"] == 1] or [0]) for r in range(nrow)]
        rows = [[] for _ in range(nrow)]
        for c in sorted(cells, key=lambda c: (c["r"], c["c"])):
            tc = c["tc"]
            sub = tc.find("hp:subList", NS)
            margin = tc.find("hp:cellMargin", NS)
            pad = " ".join(f"{pt(margin.get(k))}pt" for k in ("top", "right", "bottom", "left"))
            valign = {"TOP": "top", "BOTTOM": "bottom"}.get(sub.get("vertAlign"), "middle")
            body = "".join(self.paragraph(p) for p in sub.findall("hp:p", NS))
            rows[c["r"]].append(
                f'<td rowspan="{c["rs"]}" colspan="{c["cs"]}" style="{self.s.borders.get(tc.get("borderFillIDRef"), "")};'
                f'padding:{pad};vertical-align:{valign};overflow:hidden">{body}</td>')
        cols = "".join(f'<col style="width:{w}pt">' for w in widths)
        trs = "".join(f'<tr style="height:{h}pt">{"".join(r)}</tr>' for r, h in zip(rows, heights))
        gap = pt(tbl.find("hp:outMargin", NS).get("bottom"))
        # A table placed like a character follows its paragraph's alignment (e.g. a tag box in a cell).
        side = {"CENTER": "margin-left:auto;margin-right:auto;", "RIGHT": "margin-left:auto;"}.get(align, "")
        markup = (f'<table style="width:{sum(widths)}pt;margin-bottom:{gap}pt;{side}">'
                  f"<colgroup>{cols}</colgroup>{trs}</table>")
        pos = tbl.find("hp:pos", NS)
        if pos.get("treatAsChar") == "0" and pos.get("vertRelTo") == "PAPER":
            self.floating.append(f'<div style="position:absolute;left:{pt(pos.get("horzOffset"))}pt;'
                                 f'top:{pt(pos.get("vertOffset"))}pt">{markup}</div>')
            return ""
        return markup


def build_html(hwpx):
    with zipfile.ZipFile(hwpx) as z:
        header = E.fromstring(z.read("Contents/header.xml"))
        section = E.fromstring(z.read("Contents/section0.xml"))
    page = section.find(".//hp:pagePr", NS)
    m = {k: pt(v) for k, v in page.find("hp:margin", NS).attrib.items()}
    width, height = pt(page.get("width")), pt(page.get("height"))
    r = Renderer(Styles(header))
    body = "".join(r.paragraph(p) for p in section.findall("hp:p", NS))
    limit = height - m["bottom"]
    return f"""<!doctype html><meta charset="utf-8"><style>
html,body{{margin:0;background:#fff}}
#page{{position:relative;width:{width}pt;min-height:{height}pt;font-family:'KoPub돋움체 Medium','WenQuanYi Zen Hei',sans-serif;color:#161616}}
#flow{{position:absolute;left:{m['left']}pt;top:{m['top']}pt;width:{width - m['left'] - m['right']}pt}}
table{{border-collapse:collapse;table-layout:fixed}} td{{box-sizing:border-box}}
#limit{{position:absolute;left:0;right:0;top:{limit}pt;border-top:1.5px dashed #e00}}
#limit span{{position:absolute;right:4px;top:-14px;font:10px sans-serif;color:#e00}}
</style><div id="page"><div id="flow">{body}</div>{"".join(r.floating)}
<div id="limit"><span>page limit</span></div></div>
<script>window.PAGE={json.dumps(dict(height=height, top=m['top'], limit=limit))}</script>"""


def reference_page(args):
    """(label, (width, height) in pt, draw(canvas, rect)) for the right-hand original, or None."""
    from pdf_coords import SnapshotPage, open_page
    if args.ref:
        name = args.ref.name
        pix = pymupdf.Pixmap(str(args.ref)) if args.ref.suffix.lower() in (".png", ".jpg", ".jpeg") else None
        if pix is None:   # e.g. webp: convert through Pillow when available
            from PIL import Image
            tmp = Path(tempfile.mkdtemp()) / "ref.png"
            Image.open(args.ref).convert("RGB").save(tmp)
            args.ref, pix = tmp, pymupdf.Pixmap(str(tmp))
        width = 612.0   # show the picture at A4-ish width beside the preview
        return (f"Original: {name}", (width, width * pix.height / pix.width),
                lambda canvas, rect: canvas.insert_image(rect, filename=str(args.ref)))
    if not args.pdf:
        return None
    page = open_page(args.pdf, args.page)
    size = (page.rect.width, page.rect.height)
    if isinstance(page, SnapshotPage):
        return (f"PDF page {page.number + 1} (snapshot)", size,
                lambda canvas, rect: canvas.insert_image(rect, filename=str(page.image_path())))
    return (f"PDF page {args.page}", size,
            lambda canvas, rect: canvas.show_pdf_page(rect, page.parent, page.number))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("hwpx", type=Path)
    ap.add_argument("out", type=Path)
    ap.add_argument("--pdf", type=Path, help="source PDF or page snapshot (.json.gz) to show on the right")
    ap.add_argument("--page", type=int, default=1)
    ap.add_argument("--ref", type=Path, help="a picture of the original page (screenshot or scan) instead")
    args = ap.parse_args()
    with tempfile.TemporaryDirectory() as tmp:
        page_html = Path(tmp) / "page.html"
        page_html.write_text(build_html(args.hwpx), encoding="utf-8")
        shot = Path(tmp) / "shot.png"
        result = subprocess.run(["node", str(SHOT_JS), str(page_html), str(shot), str(SCALE)],
                                capture_output=True, text=True, check=True)
        info = json.loads(result.stdout)
        reference = reference_page(args)
        if reference is None:
            shot.replace(args.out)
        else:
            label, size, draw = reference
            img = pymupdf.Pixmap(str(shot))
            width, height = size
            left_h = img.height / SCALE
            doc = pymupdf.open()
            canvas = doc.new_page(width=width * 2 + 20, height=max(height, left_h) + 18)
            canvas.insert_text((4, 12), "HWPX preview (approximate)", fontsize=9, color=(0.8, 0, 0))
            canvas.insert_text((width + 24, 12), label, fontsize=9, color=(0.8, 0, 0))
            canvas.insert_image(pymupdf.Rect(0, 18, width, 18 + left_h), filename=str(shot))
            draw(canvas, pymupdf.Rect(width + 20, 18, width * 2 + 20, 18 + height))
            canvas.draw_line((width + 10, 0), (width + 10, canvas.rect.height), color=(0.7, 0.7, 0.7))
            canvas.get_pixmap(matrix=pymupdf.Matrix(SCALE * 0.75, SCALE * 0.75)).save(args.out)
    over = info["flow_bottom_pt"] - info["limit_pt"]
    print(f"Wrote {args.out}. Flow bottom {info['flow_bottom_pt']:.0f}pt vs page limit {info['limit_pt']:.0f}pt: "
          + (f"OVERFLOW by ~{over:.0f}pt (likely spills to a 2nd page)" if over > 0 else f"fits with ~{-over:.0f}pt spare"))


if __name__ == "__main__":
    main()
