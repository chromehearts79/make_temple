"""Rebuild KDN 2025 report page 114 (PDF 3 local page 14, printed page 79) as editable HWPX.

Usage: python3 work/kdn2025/p114.py <report3.pdf> <out.hwpx> [--page 14]

계량지표 summary page 재무예산성과(영업이익률) 3.0점, built with the shared metric_page module
(PART box, 지표명 box, contacts, bands 1-4, 보정근거 / 보정사유 notes, bullet boxes, data table with
'25년 실제 / 보정). The 1 실적 개요 table is metric_page.split_scores on this page's rules (2025 split
into 실제 / 보정). Source oddity kept: '23년 영업이익률 is printed as 13.823 without %.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import metric_page as mp  # noqa: E402
from metric_page import X0, X1  # noqa: E402

mp.start(14, "재무예산성과(영업이익률)")
t = mp.split_scores(93.5, 127.5, [264.2, 282.6, 303.3, 323.9, 359.9, 395.9])
mp.frame_page(odd=False, scores=t, notes_range=(396.0, 460.0),
              data=dict(cols=[X0, 155.9, 213.0, 270.1, 327.1, 384.2, 441.2, 498.3, X1],
                        rules=[689.9, 726.8, 751.4, 776.1, 800.7], mid=708.3))
