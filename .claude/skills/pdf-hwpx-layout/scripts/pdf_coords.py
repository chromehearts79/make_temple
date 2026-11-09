"""Read positioned PDF text and make a compact visual reference for one page.

The source can be the PDF or a page snapshot (pdf_snapshot.py): a .json.gz file that answers the
same page calls, so recipes, checks and previews run again later without the PDF.
"""

import argparse
import copy
import gzip
import json
from pathlib import Path

import pymupdf

SNAPSHOT_FORMAT = "pdf-page-snapshot/1"
# get_text variants that recipes and the page kit call, stored in a snapshot.
SNAPSHOT_TEXT = [("text", None), ("dict", None), ("dict", pymupdf.TEXTFLAGS_TEXT),
                 ("rawdict", None), ("rawdict", 0)]


def _key(option, flags):
    return f"{option}:{'default' if flags is None else flags}"


def _plain(obj):
    """PyMuPDF results as JSON values: geometry to lists, image bytes dropped."""
    if isinstance(obj, dict):
        return {k: _plain(v) for k, v in obj.items()}
    if isinstance(obj, (bytes, bytearray)):
        return None
    if isinstance(obj, pymupdf.Quad):
        return [list(point) for point in obj]
    if isinstance(obj, (pymupdf.Rect, pymupdf.IRect, pymupdf.Point)):
        return list(obj)
    if isinstance(obj, (list, tuple)):
        return [_plain(v) for v in obj]
    return obj


def snapshot(page):
    """Everything a recipe reads from one PDF page, as a JSON-ready dict."""
    return {
        "format": SNAPSHOT_FORMAT,
        "physical_page": page.number + 1,
        "total_pages": page.parent.page_count,
        "size_pt": [page.rect.width, page.rect.height],
        "text": {_key(o, f): _plain(page.get_text(o) if f is None else page.get_text(o, flags=f))
                 for o, f in SNAPSHOT_TEXT},
        "drawings": _plain(page.get_drawings()),
        "image_info": _plain(page.get_image_info()),
        "images": _plain(page.get_images()),
    }


class SnapshotPage:
    """Stands in for a pymupdf Page, answering from a snapshot."""

    def __init__(self, data, path):
        if data.get("format") != SNAPSHOT_FORMAT:
            raise ValueError(f"{path} is not a {SNAPSHOT_FORMAT} file")
        self.data, self.path = data, Path(path)
        self.number = data["physical_page"] - 1
        self.rect = pymupdf.Rect(0, 0, *data["size_pt"])

    def get_text(self, option="text", *, flags=None, sort=False):
        key = _key(option, flags)
        if sort or key not in self.data["text"]:
            raise ValueError(f"Snapshot {self.path.name} has no get_text({option!r}, flags={flags}, "
                             f"sort={sort}); add it to SNAPSHOT_TEXT and take the snapshot again")
        return copy.deepcopy(self.data["text"][key])

    def get_drawings(self):
        out = []
        for d in copy.deepcopy(self.data["drawings"]):
            d["rect"] = pymupdf.Rect(d["rect"])
            items = []
            for kind, *args in d.get("items", []):
                if kind == "re":
                    items.append((kind, pymupdf.Rect(args[0]), *args[1:]))
                elif kind == "qu":
                    items.append((kind, pymupdf.Quad(*[pymupdf.Point(p) for p in args[0]])))
                else:
                    items.append((kind, *[pymupdf.Point(a) for a in args]))
            d["items"] = items
            for name in ("fill", "color"):
                if d.get(name) is not None:
                    d[name] = tuple(d[name])
            out.append(d)
        return out

    def get_image_info(self, **_):
        return copy.deepcopy(self.data["image_info"])

    def get_images(self, full=False):
        return [tuple(i) for i in self.data["images"]]

    def image_path(self):
        """The page picture saved beside the snapshot (pNNN.json.gz -> pNNN.png)."""
        return self.path.with_name(self.path.name.split(".")[0] + ".png")


def is_snapshot(path):
    return str(path).endswith((".json.gz", ".json"))


def open_page(path, page=1):
    """A PDF page (1-based physical number) or a snapshot page, which ignores `page`."""
    path = Path(path)
    if is_snapshot(path):
        opener = gzip.open if path.suffix == ".gz" else open
        with opener(path, "rt", encoding="utf-8") as f:
            return SnapshotPage(json.load(f), path)
    pdf = pymupdf.open(path)
    if not 1 <= page <= len(pdf):
        raise ValueError(f"Physical page {page} outside 1–{len(pdf)}")
    return pdf[page - 1]


class SourcePage:
    def __init__(self, page):
        self.page = page
        self.lines = []
        for block in page.get_text("dict", flags=pymupdf.TEXTFLAGS_TEXT)["blocks"]:
            for line in block.get("lines", []):
                spans = line["spans"]
                text = "".join(span["text"] for span in spans).strip()
                if text:
                    self.lines.append({
                        "bbox": [round(v, 2) for v in line["bbox"]],
                        "text": text,
                        "sizes": sorted({round(span["size"], 2) for span in spans}),
                    })

    def inline_tags(self):
        """Small boxes that sit inside a line of text: a box inside a box, e.g. "∙[환경분석] 육아…".

        The text layer gives such a tag and its line as plain text, so the boxes come from the
        drawings: a small filled or outlined rectangle (or image) around a span, with other text on
        the same baseline right next to it. Each tag reports its text, the line around it, where it
        sits (start / middle / end), its fill or outline and text colour. White text next to dark
        text is reported too (tags drawn as images). Table label cells next to text can show up as
        well; check the list against page.png.
        """
        spans = []
        for block in self.page.get_text("dict", flags=pymupdf.TEXTFLAGS_TEXT)["blocks"]:
            for line in block.get("lines", []):
                for span in line["spans"]:
                    if span["text"].strip():
                        spans.append(dict(rect=pymupdf.Rect(span["bbox"]), text=span["text"].strip(),
                                          size=span["size"], color=span["color"]))
        if not spans:
            return []
        boxes = []
        for d in self.page.get_drawings():
            fill = tuple(round(v, 3) for v in d["fill"][:3]) if d.get("fill") else None
            if fill and fill != (1, 1, 1):
                boxes.append((pymupdf.Rect(d["rect"]), "#%02X%02X%02X" % tuple(round(v * 255) for v in fill)))
            elif d.get("color") and any(item[0] == "re" for item in d.get("items", [])):
                boxes.append((pymupdf.Rect(d["rect"]), "outline"))
        boxes += [(pymupdf.Rect(i["bbox"]), "image") for i in self.page.get_image_info()]

        def same_row(a, b):
            return abs((a.y0 + a.y1) / 2 - (b.y0 + b.y1) / 2) < min(a.height, b.height) * 0.6

        def cells_of(rect):
            """Small boxes (table cells, tags) holding a span."""
            grown = [b + (-1.5, -1.5, 1.5, 1.5) for b, _ in boxes]
            return [b for b, g in zip((b for b, _ in boxes), grown)
                    if g.contains(rect) and b.height < 2.6 * rect.height]

        def chain(seed, others, size):
            """Spans joined to `seed` left and right on its row with gaps under 2 em. A span in a
            small box that does not also hold `seed` sits in a sibling cell and ends the chain."""
            row = sorted((o for o in others if same_row(o["rect"], seed)
                          and all(c.contains(seed) for c in cells_of(o["rect"]))),
                         key=lambda o: o["rect"].x0)
            left = [o for o in row if o["rect"].x0 < seed.x0][::-1]
            right = [o for o in row if o["rect"].x1 > seed.x1 and o["rect"].x0 >= seed.x0]
            out = {"left": [], "right": []}
            for side, items, edge in (("left", left, seed.x0), ("right", right, seed.x1)):
                for o in items:
                    gap = max(0, edge - o["rect"].x1 if side == "left" else o["rect"].x0 - edge)
                    if gap > 2 * size:
                        break
                    out[side].append(o)
                    edge = o["rect"].x0 if side == "left" else o["rect"].x1
            return out["left"][::-1], out["right"]

        found, seen = [], set()
        for box, style in sorted(boxes, key=lambda b: (b[0].y0, b[0].x0)):
            grown = box + (-1.5, -1.5, 1.5, 1.5)
            inside = sorted((s for s in spans if grown.contains(s["rect"])), key=lambda s: s["rect"].x0)
            if not inside or box.height > max(s["size"] for s in inside) * 2.6:
                continue
            others = [s for s in spans if not grown.contains(s["rect"])]
            size = max(s["size"] for s in inside)
            left, right = chain(box, others, size)
            if not left and not right:
                continue
            key = (round(box.x0), round(box.y0))
            if key in seen:
                continue
            seen.add(key)
            tag = " ".join(s["text"] for s in inside)
            found.append({
                "tag": tag,
                "line": " ".join(s["text"] for s in left) + f" [{tag}] " + " ".join(s["text"] for s in right),
                "position": "start" if not left else "end" if not right else "middle",
                "box": [round(v, 2) for v in box], "style": style,
                "text_color": "#%06X" % inside[0]["color"],
            })
        for s in spans:   # white text beside dark text without a drawn box: a tag in an image
            if s["color"] == 0xFFFFFF and not cells_of(s["rect"]):
                left, right = chain(s["rect"], [o for o in spans if o is not s and o["color"] != 0xFFFFFF], s["size"])
                if left or right:
                    found.append({"tag": s["text"], "line": " ".join(o["text"] for o in left) + f" [{s['text']}] "
                                  + " ".join(o["text"] for o in right),
                                  "position": "start" if not left else "end" if not right else "middle",
                                  "box": None, "style": "image?", "text_color": "#FFFFFF"})
        return found

    def region(self, left, right, top, bottom):
        """Select by line origin, sorted in vertical reading order within the region."""
        matches = [line for line in self.lines
                   if left <= line["bbox"][0] < right and top <= line["bbox"][1] < bottom]
        return [line["text"] for line in sorted(matches, key=lambda line: (line["bbox"][1], line["bbox"][0]))]

    def only(self, *bounds):
        values = self.region(*bounds)
        if len(values) != 1:
            raise ValueError(f"Expected one source line in {bounds}, got {values}")
        return values[0]


def select_page(pdf, page):
    if not 1 <= page <= len(pdf):
        raise ValueError(f"Physical page {page} outside 1–{len(pdf)}")
    return SourcePage(pdf[page - 1])


def recipe_inputs(default_page, signature):
    parser = argparse.ArgumentParser(description="Reproduce one tested KDN report layout.")
    parser.add_argument("pdf", type=Path, help="the report PDF, or a page snapshot (.json.gz)")
    parser.add_argument("output", type=Path)
    parser.add_argument("--page", type=int, default=default_page,
                        help="Physical page; use 1 for an extracted single-page PDF (ignored for a snapshot)")
    args = parser.parse_args()
    if args.pdf.resolve() == args.output.resolve():
        parser.error("Input and output must be different files")
    source = SourcePage(open_page(args.pdf, args.page))
    if signature not in source.page.get_text():
        parser.error("PDF page does not match this layout recipe")
    return source, args.output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path, help="the PDF, or a page snapshot (.json.gz)")
    parser.add_argument("page", type=int, help="Physical PDF page number, starting at 1 (ignored for a snapshot)")
    parser.add_argument("out_dir", type=Path)
    args = parser.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    page = open_page(args.pdf, args.page)
    src = SourcePage(page)
    shot = isinstance(page, SnapshotPage)
    info = {
        "physical_page": page.number + 1,
        "total_pages": page.data["total_pages"] if shot else page.parent.page_count,
        "size_pt": [page.rect.width, page.rect.height],
        "lines": src.lines,
        "vector_objects": [{"bbox": list(d["rect"]), "fill": d["fill"] if "fill" in d else None}
                           for d in page.get_drawings()],
        "image_boxes": [list(item["bbox"]) for item in page.get_image_info()],
        "inline_tags": src.inline_tags(),
    }
    (args.out_dir / "page.json").write_text(json.dumps(info, ensure_ascii=False, indent=2), encoding="utf-8")
    if shot:
        pymupdf.Pixmap(str(page.image_path())).save(args.out_dir / "page.png")
    else:
        page.get_pixmap(matrix=pymupdf.Matrix(1.65, 1.65), alpha=False).save(args.out_dir / "page.png")
    print(f"Wrote {args.out_dir / 'page.json'} and {args.out_dir / 'page.png'}")
    if info["inline_tags"]:
        print("Tag boxes inside text lines (box in a box; build with Layout.boxed_line):")
        for tag in info["inline_tags"]:
            print(f"  {tag['position']:6} {tag['style']:8} text {tag['text_color']}  {tag['line'].strip()}")


if __name__ == "__main__":
    main()
