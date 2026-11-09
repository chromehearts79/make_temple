"""Rebuild KDN 2025 report page 115 (PDF 3 local page 15, printed page 80) as editable HWPX.

Usage: python3 work/kdn2025/p115.py <report3.pdf> <out.hwpx> [--page 15]

계량지표 summary page 재무예산성과(부채비율) 0.5점, built with the shared metric_page module
(running head, side tab, 지표명 box, contacts, bands 1-4, 보정근거 / 보정사유 notes, bullet boxes,
data table with '25년 실제 / 보정, two footnotes). The 1 실적 개요 table is metric_page.split_scores
on this page's rules (2025 split into 실제 / 보정).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import metric_page as mp  # noqa: E402
from metric_page import X0, X1  # noqa: E402

mp.start(15, "재무예산성과(부채비율)")
t = mp.split_scores(92.2, 127.6, [264.2, 282.6, 301.0, 319.4, 353.1, 386.9])
mp.frame_page(odd=True, scores=t, notes_range=(387.0, 450.0),
              data=dict(cols=[X0, 155.9, 213.0, 270.1, 327.1, 384.2, 441.2, 498.3, X1],
                        rules=[680.9, 717.7, 736.1, 754.5, 773.0], mid=699.3))
