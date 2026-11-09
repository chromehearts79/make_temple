"""Rebuild every page of the 2025 KDN report (PDF pages 1-50), check each one and merge them.

usage: python3 work/kdn2025/build_all.py <report.pdf> [--pages 1-50] [--no-merge]

Writes output/pNN.hwpx per page and output/kdn2025_report_p001-050.hwpx (one section per page).
Pages whose script is missing are reported and left out of the merge.
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WORK = Path(__file__).resolve().parent
SKILL = ROOT / ".claude/skills/pdf-hwpx-layout/scripts"
OUT = ROOT / "output"

# PDF page -> recipe; every other page N uses work/kdn2025/pNN.py.
SHARED = {**{n: WORK / "blank.py" for n in (2, 4, 6, 8, 10, 46)},
          33: WORK / "p11.py", 47: WORK / "p11.py",      # 지표 정의
          34: WORK / "p12.py", 48: WORK / "p12.py",      # 세부목차
          45: WORK / "p09.py",                            # chapter cover
          44: WORK / "p32.py",                            # logo divider
          49: SKILL / "kdn_p49.py", 50: SKILL / "kdn_p50.py"}


def pages(spec):
    out = []
    for part in spec.split(","):
        a, _, b = part.partition("-")
        out += range(int(a), int(b or a) + 1)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pdf", type=Path)
    ap.add_argument("--pages", default="1-50")
    ap.add_argument("--no-merge", action="store_true")
    args = ap.parse_args()

    built, problems = [], []
    for n in pages(args.pages):
        script = SHARED.get(n, WORK / f"p{n:02}.py")
        target = OUT / f"p{n:02}.hwpx"
        if not script.exists():
            problems.append(f"p{n:02}: no recipe ({script.name})")
            continue
        run = subprocess.run([sys.executable, str(script), str(args.pdf), str(target), "--page", str(n)],
                             capture_output=True, text=True)
        if run.returncode:
            problems.append(f"p{n:02}: build failed\n{run.stderr.strip()[-600:]}")
            continue
        check = subprocess.run([sys.executable, str(SKILL / "check_hwpx.py"), str(target),
                                "--pdf", str(args.pdf), "--page", str(n)], capture_output=True, text=True)
        matched = re.search(r"PDF lines matched: (\d+/\d+)", check.stdout)
        status = "ok" if check.returncode == 0 else "CHECK FAILED"
        print(f"p{n:02}  {script.name:12} {matched.group(1) if matched else '-':>9}  {status}")
        if check.returncode:
            problems.append(f"p{n:02}: check failed\n{check.stdout.strip()[-600:]}")
        built.append(target)

    if not args.no_merge and built:
        merged = OUT / "kdn2025_report_p001-050.hwpx"
        subprocess.run([sys.executable, str(SKILL / "merge_hwpx.py"), str(merged), *map(str, built)], check=True)
    for problem in problems:
        print("PROBLEM", problem)
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
