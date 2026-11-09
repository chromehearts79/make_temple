"""Rebuild pages of the 2025 KDN report, check each one and merge them into one HWPX.

usage: python3 work/kdn2025/build_all.py <p001-050.pdf> [<p051-100.pdf>] [--pages 1-100] [--no-merge]

The report comes as 50-page PDFs: report page N is local page N-50 of the second PDF, etc.
Writes output/pNN.hwpx per report page and output/kdn2025_report_pAAA-BBB.hwpx for the built range
(one section per page). Pages whose script or PDF is missing are reported and left out of the merge.
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
          45: WORK / "p09.py", 99: WORK / "p09.py",       # chapter covers
          44: WORK / "p32.py", 56: WORK / "p32.py", 66: WORK / "p32.py", 98: WORK / "p32.py",  # logo
          49: SKILL / "kdn_p49.py", 50: SKILL / "kdn_p50.py", 51: SKILL / "kdn_p51.py",
          100: WORK / "blank.py", 120: WORK / "blank.py",
          119: WORK / "p09.py", 118: WORK / "p32.py", 136: WORK / "p32.py",
          **{n: WORK / "p11.py" for n in (101, 137)}, 121: WORK / "p57.py", 147: WORK / "p57.py",
          **{n: WORK / "p12.py" for n in (102, 122, 138, 148)},
          **{n: WORK / "p11.py" for n in (67, 75, 85)},   # 지표 정의 (57 has its own p57.py)
          **{n: WORK / "p12.py" for n in (58, 68, 76, 86)}}   # 세부목차


def pages(spec):
    out = []
    for part in spec.split(","):
        a, _, b = part.partition("-")
        out += range(int(a), int(b or a) + 1)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pdfs", type=Path, nargs="+", help="the report PDFs in order, 50 pages each")
    ap.add_argument("--pages", default=None, help="report pages, e.g. 1-100 or 51-60,70")
    ap.add_argument("--no-merge", action="store_true")
    args = ap.parse_args()

    built, problems = [], []
    wanted = pages(args.pages) if args.pages else range(1, 50 * len(args.pdfs) + 1)
    for n in wanted:
        part, local = (n - 1) // 50, (n - 1) % 50 + 1
        if part >= len(args.pdfs):
            problems.append(f"p{n:02}: no PDF given for report page {n}")
            continue
        pdf = args.pdfs[part]
        script = SHARED.get(n, WORK / f"p{n:02}.py")
        target = OUT / f"p{n:02}.hwpx"
        if not script.exists():
            problems.append(f"p{n:02}: no recipe ({script.name})")
            continue
        run = subprocess.run([sys.executable, str(script), str(pdf), str(target), "--page", str(local)],
                             capture_output=True, text=True)
        if run.returncode:
            problems.append(f"p{n:02}: build failed\n{run.stderr.strip()[-600:]}")
            continue
        check = subprocess.run([sys.executable, str(SKILL / "check_hwpx.py"), str(target),
                                "--pdf", str(pdf), "--page", str(local)], capture_output=True, text=True)
        matched = re.search(r"PDF lines matched: (\d+/\d+)", check.stdout)
        status = "ok" if check.returncode == 0 else "CHECK FAILED"
        print(f"p{n:02}  {script.name:12} {matched.group(1) if matched else '-':>9}  {status}")
        if check.returncode:
            problems.append(f"p{n:02}: check failed\n{check.stdout.strip()[-600:]}")
        built.append(target)

    if not args.no_merge and built:
        first, last = (int(p.stem[1:]) for p in (built[0], built[-1]))
        merged = OUT / f"kdn2025_report_p{first:03}-{last:03}.hwpx"
        subprocess.run([sys.executable, str(SKILL / "merge_hwpx.py"), str(merged), *map(str, built)], check=True)
    for problem in problems:
        print("PROBLEM", problem)
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
