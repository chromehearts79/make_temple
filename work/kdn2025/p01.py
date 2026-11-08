"""Rebuild the report cover (PDF page 1) as editable HWPX.

usage: python3 work/kdn2025/p01.py <report.pdf> <out.hwpx> [--page N]
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".claude/skills/pdf-hwpx-layout/scripts"))

from hwpx_layout import Layout, cell  # noqa: E402
from pdf_coords import recipe_inputs  # noqa: E402

source, target = recipe_inputs(1, "공기업 산업진흥·서비스 유형")
only = source.only
layout = Layout()
p, add_text, add_table, border = layout.p, layout.add_text, layout.add_table, layout.border


def blank(width, height):
    return cell(0, width, height, [p("", 100, line=100)])


# Type label box at the top right (PDF x 342–544pt, y 99–126pt).
add_text("", 100, line=6500)
label = only(340, 360, 100, 110)
add_table([[blank(28540, 2700),
            cell(1, 20200, 2700, layout.center(label, 1490), border(top="strong", bottom="strong", sides="strong")),
            cell(2, 1160, 2700, [p("", 100, line=100)])]])

# Title block. Spacing follows the PDF tops: title 241pt, subtitle 304pt, date 483pt, company 739pt.
add_text(only(70, 80, 238, 245), 3900, True, align="CENTER", line=4700, before=11000)
add_text(only(200, 215, 300, 308), 3170, True, align="CENTER", line=3800, before=1500)
add_text(only(260, 275, 480, 486), 2000, True, align="CENTER", line=2400, before=13300)
add_text(only(230, 245, 735, 742), 2500, True, align="CENTER", line=3000, before=22400)

print(layout.write(target))
