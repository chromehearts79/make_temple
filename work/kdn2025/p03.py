"""Rebuild the 기관장 확인서 (PDF page 3) as editable HWPX.

The PDF page is a single scanned image; its text was read from a 2.4x render and is typed
here. The handwritten name and seal are not reproduced: the signature line is left blank.

usage: python3 work/kdn2025/p03.py <report.pdf> <out.hwpx> [--page N]
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kit  # noqa: E402
from kit import Layout, recipe_inputs  # noqa: E402

source, target = recipe_inputs(3, "")  # image-only page: no text to check
L = Layout(top=10300)
kit.setup(source, L)
from kit import *  # noqa: E402,F401,F403

BODY = 1150


def text(*runs):
    """One justified paragraph from (text, bold) pairs."""
    return [[(t, BODY, b, INK) for t, b in runs]]


xs = [X0, 84.0, 99.0, 113.0, 270.0, 345.0, 470.0, 505.0, 520.0, 535.0, X1]
hs = [3000, 4600, 2800, 2400, 2400, 2600, 6000, 1400, 4200, 1400,
      6000, 1000, 4200, 1000, 6000, 3500, 3000, 4000]
g = Grid("letter", xs, hs)
last = len(hs)
# Box outline: side columns and the first / last spacer rows carry the border.
g.put(84.0, 99.0, 0, last, [], frame(left="mid", top="mid", bottom="mid"))
g.put(520.0, 535.0, 0, last, [], frame(right="mid", top="mid", bottom="mid"))
g.put(99.0, 520.0, 0, 1, [], frame(top="mid"))
g.put(99.0, 520.0, last - 1, last, [], frame(bottom="mid"))

g.put(99.0, 520.0, 1, 2, "2025년도 경영실적보고서에 대한 기관장 확인서", size=1600, bold=True, ratio=100)
g.put(99.0, 520.0, 3, 4, "재정경제부 장관 및 주무부처 장관 귀중", align="LEFT", size=1200, bold=True, ratio=100)
g.put(99.0, 520.0, 4, 5, "2026년   3월   5일", align="RIGHT", size=1200, bold=True, ratio=100)
wrap = dict(align="JUSTIFY", ratio=100, line=1850, fit=False)
g.put(99.0, 520.0, 6, 7, text(("  이 확인서는 『공공기관의 운영에 관한 법률』에 따른 경영실적 보고에 있어서 ", False),
                               ("한전KDN(주)", True),
                               ("의 경영실적보고서에 기재된 모든 경영실적이 사실과 다름없이 정확하게 작성되었다는 것을 "
                                "확인하기 위해 제공되는 것입니다.", False)), **wrap)
g.put(99.0, 520.0, 8, 9, text(("한전KDN(주)", True),
                               ("의 기관장 본인은 제출하는 모든 경영실적 및 그 근거자료에 대해 아래 사항을 확인합니다.", False)),
      **wrap)
items = [
    "한전KDN(주) 경영실적보고서에 기재된 모든 경영실적 및 그 근거자료는 『2025년도 공공기관 경영평가편람』의 "
    "평가기준 · 방법과 『2025년도 경영실적보고서 작성지침』에 따라 작성되었습니다.",
    "각 지표의 정확한 점수산출을 위하여 정확한 지표 산출 과정과 철저한 내부점검 과정을 거쳤음을 확인합니다.",
    "실적보고서가 거짓으로 작성 · 제출된 경우에는 『공공기관의 운영에 관한 법률』 제48조와 "
    "『2025년도 공공기관 경영평가편람』에 의한 조치에 따르겠습니다.",
]
for k, (row, item) in enumerate(zip((10, 12, 14), items), 1):
    g.put(99.0, 113.0, row, row + 1, f"{k}.", align="LEFT", size=BODY, ratio=100, line=1850)
    g.put(113.0, 520.0, row, row + 1, text((item, False)), **wrap)
# Signature line: the handwritten name and seal are left out on purpose (blank for signing).
g.put(270.0, 345.0, 16, 17, "기   관   장", size=1200, bold=True, ratio=100)
g.put(345.0, 470.0, 16, 17, [], frame(bottom="soft"))
g.put(470.0, 505.0, 16, 17, "(날인)", size=1000, ratio=100)
block(g, 104.0)

flush(end=104.0 + sum(hs) / 100)
# Numbered items: top-align number and text so the first lines line up.
for tc in L.section.iter(L.q("hp:tc")):
    body = "".join(tc.itertext()).strip()
    if body in ("1.", "2.", "3.") or any(body == item for item in items):
        L.get(tc, "hp:subList").set("vertAlign", "TOP")
for number, table in enumerate(L.section.iter(L.q("hp:tbl")), 5001):
    table.set("id", str(number))
for message in WARN:
    print("WARN", message)
print(L.write(target))
