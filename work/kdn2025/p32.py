"""Rebuild the logo divider page (PDF page 32, identical page 44) as editable HWPX.

The page holds one image: a dark band with the slogan and the 한전KDN wordmark. Both are typed
from a 3x render; the wordmark becomes large gray text.

usage: python3 work/kdn2025/p32.py <report.pdf> <out.hwpx> [--page 44]
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kit  # noqa: E402
from kit import Layout, recipe_inputs  # noqa: E402

source, target = recipe_inputs(32, "")  # image-only page: no text to check
L = Layout(top=39500)
kit.setup(source, L)
from kit import *  # noqa: E402,F401,F403

g = Grid("logo", [X0, 187.0, 425.0, X1], [1600, 5200])
g.put(187.0, 425.0, 0, 1, "디지털 혁신, 에너지 대전환을 선도하는 글로벌 에너지ICT의 중심",
      frame("#5A5A5A"), size=1000, bold=True, color=WHITE)
g.put(187.0, 425.0, 1, 2, "한전KDN㈜", size=4600, bold=True, color="#9A9A9A", ratio=100, line=5000)
block(g, 396.0)
kit.finish(target, end=466.0)
