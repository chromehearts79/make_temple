"""Rebuild KDN 2025 report page 117 (PDF 3 local page 17, printed page 82) as editable HWPX.

Usage: python3 work/kdn2025/p117.py <report3.pdf> <out.hwpx> [--page 17]

계량지표 summary page 효율성 관리(노동/자본생산성) 2.5점/2.5점, built with the shared metric_page
module (running head, side tab, 지표명 box, contacts, bands 1-4, bullet boxes, data table, footnote).
This script adds the 1 실적 개요 table on the PDF's rules: an extra 지표명 column with two groups
(① 노동생산성, ② 자본생산성) of three years each; 지표명, 평가산식 and 평가방법 merged per group. The
header '목표치(백만원, %)  실적치(백만원, %)' is one PDF line, split over its two columns by span.
Source oddity kept: 노동생산성 '25 is 134.364 in the score table but 134.363 in 4 실적 산출내역.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import metric_page as mp  # noqa: E402
from metric_page import LIGHT, X0, X1  # noqa: E402

mp.start(17, "효율성 관리(노동/자본생산성)")

cols = [X0, 90.7, 141.7, 212.6, 260.8, 345.8, 425.2, 479.0, 515.8, X1]
t = mp.Table("scores", cols, [264.2, 282.6, 311.0, 339.3, 367.7, 396.0, 424.4, 452.7])
t.head_row()
for first in (1, 4):                       # ① 노동생산성, ② 자본생산성
    for a, e in ((90.7, 141.7), (141.7, 212.6), (212.6, 260.8)):
        t.body(a, e, first, first + 3, line=1320)
    for r in range(first, first + 3):
        t.body(X0, 90.7, r, fill=LIGHT, right=None)
        t.body(260.8, 345.8, r, align="LEFT", line=1320)
        for a, e in zip(cols[5:], cols[6:]):
            t.body(a, e, r)

mp.frame_page(odd=True, scores=t,
              data=dict(cols=[X0, 184.3, 246.1, 307.9, 369.6, 431.4, 493.2, X1],
                        rules=[688.2, 706.5, 722.7, 738.9, 755.0, 771.2, 787.3]))
