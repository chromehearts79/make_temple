"""Rebuild KDN 2025 report page 113 (PDF 3 local page 13, printed page 78) as editable HWPX.

Usage: python3 work/kdn2025/p113.py <report3.pdf> <out.hwpx> [--page 13]

계량지표 summary page 재무예산성과(총자산회전율) 1.5점, built with the shared metric_page module
(running head, side tab, 지표명 box, contacts, bands 1-4, bullet boxes, data table, footnote).
This script adds the 1 실적 개요 score table on the PDF's rules: 평가산식 and 평가방법 merged over
2025-2023, 목표치 as two lines (최고 / 최저).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import metric_page as mp  # noqa: E402
from metric_page import LIGHT, X0, X1  # noqa: E402

mp.start(13, "재무예산성과(총자산회전율)")

cols = [X0, 90.7, 260.8, 311.8, 382.7, 433.7, 484.7, 518.7, X1]
t = mp.Table("scores", cols, [264.2, 282.6, 325.2, 367.7, 410.2])
t.head_row()
t.body(90.7, 260.8, 1, 4)                       # 매출액 ÷ 평균총자산
t.body(260.8, 311.8, 1, 4, line=1540)           # 목표부여 (편차)
for r in (1, 2, 3):
    t.body(X0, 90.7, r, fill=LIGHT, right=None)
    t.body(311.8, 382.7, r, align="LEFT", line=1540)
    for a, e in zip(cols[4:], cols[5:]):
        t.body(a, e, r)

mp.frame_page(odd=True, scores=t,
              data=dict(cols=[X0, 184.3, 246.1, 307.9, 369.8, 431.6, 493.4, X1],
                        rules=[648.8, 667.2, 707.0, 746.6, 786.3]))
