"""Rebuild KDN 2025 report page 116 (PDF 3 local page 16, printed page 81) as editable HWPX.

Usage: python3 work/kdn2025/p116.py <report3.pdf> <out.hwpx> [--page 16]

계량지표 summary page 재무예산성과(일반관리비 관리) 1.5점, built with the shared metric_page module
(PART box, 지표명 box, contacts, bands 1-4, 보정근거 / 보정사유 notes, bullet boxes, data table with
'25년 실제 / 보정). This script adds the 1 실적 개요 table on the PDF's rules: 2025 split into
실제 / 보정 with its own 평가산식; 2024 and 2023 each have two sub rows (매출액 / 평균인원 based)
under one merged two-line 평가산식; 평가방법 merged over all rows.
Source oddities kept: '평점 55,839' (comma) in 2 실적 내용; the 2025 year label is not bold.
The label 일반관리비 관리(A/B) is letter-spaced with blanks in the text layer but printed tight; it is
written as printed.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import metric_page as mp  # noqa: E402
from metric_page import LIGHT, X0, X1  # noqa: E402

mp.start(16, "재무예산성과(일반관리비 관리)")

cols = [X0, 92.2, 124.7, 263.7, 314.7, 385.6, 436.6, 484.7, 518.8, X1]
t = mp.Table("scores", cols, [264.2, 282.6, 298.4, 314.3, 344.4, 374.5, 404.6, 434.7])
t.head(X0, 124.7)
t.head_row(cols[2:])
t.body(X0, 92.2, 1, 3, fill=LIGHT)                                   # 2025
for r in (1, 2):
    t.body(92.2, 124.7, r, fill=LIGHT, right=None)                     # 실제 / 보정
    for a, e in ((385.6, 436.6), (436.6, 484.7), (518.8, X1)):
        t.body(a, e, r)
t.body(124.7, 263.7, 1, 3)                                           # 일반관리비÷매출액
t.body(314.7, 385.6, 1, 3, align="LEFT", line=1430)                  # 최고 / 최저
t.body(484.7, 518.8, 1, 3)                                           # 가중치
t.body(124.7, 263.7, 3, 7, line=1540)                                # two-line 평가산식, 2024-2023
t.body(263.7, 314.7, 1, 7, line=1540)                                # 목표부여 (편차)
t.body(X0, 124.7, 3, 5, fill=LIGHT, right=None)                      # 2024
t.body(X0, 124.7, 5, 7, fill=LIGHT, right=None)                      # 2023
for r in (3, 4, 5, 6):
    t.body(314.7, 385.6, r, align="LEFT", line=1420)
    for a, e in zip(cols[5:], cols[6:]):
        t.body(a, e, r)

mp.frame_page(odd=False, scores=t, notes_range=(435.0, 500.0),
              data=dict(cols=[X0, 167.3, 222.7, 278.1, 333.5, 388.9, 444.3, 499.7, X1],
                        rules=[705.9, 742.7, 762.3, 781.8, 801.4], mid=724.3))
