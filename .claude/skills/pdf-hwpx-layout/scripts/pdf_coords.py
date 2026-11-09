"""Read positioned PDF text and make a compact visual reference for one page."""

import argparse
import json
from pathlib import Path

import pymupdf


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
        """Spans set on a small filled box that covers only part of their text line.

        Such a tag (a box inside a box, e.g. "[환경분석] 육아휴직 등 …") comes out of the text
        layer as one line with the text after it, so only the drawings show the box. A span in
        white text next to dark text is reported too, for tags drawn as images.
        """
        boxes = [pymupdf.Rect(d["rect"]) for d in self.page.get_drawings()
                 if d.get("fill") and tuple(round(v, 2) for v in d["fill"][:3]) != (1, 1, 1)]
        boxes += [pymupdf.Rect(i["bbox"]) for i in self.page.get_image_info()]
        found = []
        for block in self.page.get_text("dict", flags=pymupdf.TEXTFLAGS_TEXT)["blocks"]:
            for line in block.get("lines", []):
                spans = [s for s in line["spans"] if s["text"].strip()]
                text = "".join(s["text"] for s in line["spans"]).strip()
                line_box = pymupdf.Rect(line["bbox"])
                dark = any(s["color"] != 0xFFFFFF for s in spans)
                for span in spans:
                    r = pymupdf.Rect(span["bbox"])
                    box = next((b for b in boxes if (b + (-1.5, -1.5, 1.5, 1.5)).contains(r)
                                and b.height < span["size"] * 2.6
                                and b.width < line_box.width - span["size"]), None)
                    white = span["color"] == 0xFFFFFF and dark
                    if box is not None or white:
                        found.append({"tag": span["text"].strip(), "line": text,
                                      "bbox": [round(v, 2) for v in r],
                                      "box": [round(v, 2) for v in box] if box is not None else None,
                                      "white_text": white})
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
    parser.add_argument("pdf", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--page", type=int, default=default_page,
                        help="Physical page; use 1 for an extracted single-page PDF")
    args = parser.parse_args()
    if args.pdf.resolve() == args.output.resolve():
        parser.error("Input and output must be different files")
    pdf = pymupdf.open(args.pdf)
    source = select_page(pdf, args.page)
    if signature not in source.page.get_text():
        parser.error("PDF page does not match this layout recipe")
    return source, args.output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path)
    parser.add_argument("page", type=int, help="Physical PDF page number, starting at 1")
    parser.add_argument("out_dir", type=Path)
    args = parser.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    with pymupdf.open(args.pdf) as pdf:
        src = select_page(pdf, args.page)
        page = src.page
        info = {
            "physical_page": args.page,
            "total_pages": len(pdf),
            "size_pt": [page.rect.width, page.rect.height],
            "lines": src.lines,
            "vector_objects": [{"bbox": list(d["rect"]), "fill": d["fill"] if "fill" in d else None}
                               for d in page.get_drawings()],
            "image_boxes": [list(item["bbox"]) for item in page.get_image_info()],
            "inline_tags": src.inline_tags(),
        }
        (args.out_dir / "page.json").write_text(json.dumps(info, ensure_ascii=False, indent=2), encoding="utf-8")
        page.get_pixmap(matrix=pymupdf.Matrix(1.65, 1.65), alpha=False).save(args.out_dir / "page.png")
    print(f"Wrote {args.out_dir / 'page.json'} and {args.out_dir / 'page.png'}")
    if info["inline_tags"]:
        print("Tag boxes inside text lines (box in a box; build with Layout.boxed_line):")
        for tag in info["inline_tags"]:
            print(f"  [{tag['tag']}] in line {tag['line']!r}")


if __name__ == "__main__":
    main()
