"""Save PDF pages as snapshots so recipes, checks and previews run later without the PDF.

usage: python3 scripts/pdf_snapshot.py report.pdf out_dir [--pages 1-50] [--number-from 51]

Writes out_dir/pNNN.json.gz (text layer, drawings, image boxes) and out_dir/pNNN.png (page
picture for previews) per page. NNN is the physical page, or --number-from + i when one PDF part
holds report pages 51-100 and so on. Pass a snapshot wherever a recipe, pdf_coords.py,
check_hwpx.py --pdf or hwpx_preview.py --pdf takes the PDF (no --page needed).
"""

import argparse
import gzip
import json
from pathlib import Path

import pymupdf

from pdf_coords import snapshot


def page_list(spec, count):
    if not spec:
        return list(range(1, count + 1))
    out = []
    for part in spec.split(","):
        a, _, b = part.partition("-")
        out += range(int(a), int(b or a) + 1)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pdf", type=Path)
    ap.add_argument("out_dir", type=Path)
    ap.add_argument("--pages", help="physical pages, e.g. 1-50 or 3,7-9 (default: all)")
    ap.add_argument("--number-from", type=int, default=1, help="file number of the PDF's first page")
    args = ap.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    with pymupdf.open(args.pdf) as pdf:
        for n in page_list(args.pages, len(pdf)):
            page = pdf[n - 1]
            stem = args.out_dir / f"p{args.number_from + n - 1:03}"
            with gzip.open(f"{stem}.json.gz", "wt", encoding="utf-8") as f:
                json.dump(snapshot(page), f, ensure_ascii=False, separators=(",", ":"))
            page.get_pixmap(matrix=pymupdf.Matrix(1.65, 1.65), alpha=False).save(f"{stem}.png")
            print(f"{stem}.json.gz")


if __name__ == "__main__":
    main()
