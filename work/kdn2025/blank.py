"""Blank page (PDF pages 2, 4, 6, 8, 10, 46): kept so the page sequence and spreads match the PDF.

usage: python3 work/kdn2025/blank.py <report.pdf> <out.hwpx> --page N
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".claude/skills/pdf-hwpx-layout/scripts"))

from hwpx_layout import Layout  # noqa: E402
from pdf_coords import recipe_inputs  # noqa: E402

source, target = recipe_inputs(2, "")
if source.page.get_text().strip() or source.page.get_images():
    raise SystemExit(f"PDF page is not blank: {target}")
print(Layout().write(target))
