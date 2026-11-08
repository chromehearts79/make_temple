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
        }
        (args.out_dir / "page.json").write_text(json.dumps(info, ensure_ascii=False, indent=2), encoding="utf-8")
        page.get_pixmap(matrix=pymupdf.Matrix(1.65, 1.65), alpha=False).save(args.out_dir / "page.png")
    print(f"Wrote {args.out_dir / 'page.json'} and {args.out_dir / 'page.png'}")


if __name__ == "__main__":
    main()
