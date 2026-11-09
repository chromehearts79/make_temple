#!/usr/bin/env python3
"""storyline.py 회귀 테스트: KDN 예시는 오류 0건·경고 8건, 일부러 망가뜨린 사본은 해당 규칙이 걸린다.

usage: python3 scripts/test_storyline.py
"""

import copy
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
SCRIPT = HERE / "storyline.py"
EXAMPLE = HERE.parent / "examples/kdn2025-jobs.yaml"
TEMPLATE = HERE.parent / "assets/storyline-template.yaml"


def run(path):
    r = subprocess.run([sys.executable, str(SCRIPT), "check", str(path)], capture_output=True, text=True)
    return r.returncode, r.stdout


def run_data(data):
    with tempfile.NamedTemporaryFile("w", suffix=".yaml", delete=False, encoding="utf-8") as f:
        yaml.safe_dump(data, f, allow_unicode=True)
    try:
        return run(f.name)
    finally:
        os.unlink(f.name)


def mutations(base):
    def m(fn):
        d = copy.deepcopy(base)
        fn(d)
        return d

    ev = lambda d, i: d["평가내용"][i]  # noqa: E731
    yield "편람 핵심어 누락", m(lambda d: ev(d, 0)["과제"][3].update(핵심어=[])), "K3「공정채용」를 맡은 과제가 없다"
    yield "지적사항 배지 누락", m(lambda d: ev(d, 0)["과제"][1]["장면"][1].update(배지=[])), "1-2-나에 「지적사항 개선」 배지가 없다"
    yield "참고쪽 불일치", m(lambda d: d["지적사항"][0].update(참고쪽=31)), "참고쪽 31이"
    yield "주요성과 상자 누락", m(lambda d: ev(d, 1).update(주요성과=ev(d, 1)["주요성과"][:1])), "이 과제를 맺는 주요성과 상자가 없다"
    yield "제목 결과어 없음", m(lambda d: ev(d, 0)["과제"][2].update(제목="인턴운영 체계와 청년 일자리")), "결과를 뜻하는 명사"
    yield "없는 축", m(lambda d: ev(d, 0)["과제"][1].update(축=["S9"])), "축 S9는 어느 설계에도 없다"
    yield "추진과제 미회수", m(lambda d: ev(d, 0)["과제"][3]["장면"][1].update(축=[])), "추진과제 S1-3"

    def swap(d):
        t = ev(d, 3)["과제"]
        t[0], t[1] = t[1], t[0]
        t[0]["번호"], t[1]["번호"] = 1, 2
    yield "설계 선행 위반", m(swap), "첫 과제(또는 첫 장면)가 설계"

    def no_why(d):
        t = ev(d, 1)["과제"][2]
        t["축"] = []
        t["장면"][0].pop("문제")
        t["장면"][0]["축"] = []
    yield "왜(문제) 없음", m(no_why), "왜(문제·배경·현황)가 없다"
    yield "Ⅱ표 빈 칸", m(lambda d: ev(d, 2)["요약"].update(올해=[])), "‘올해’ 칸이 비었다"


def main():
    failures = 0
    code, out = run(EXAMPLE)
    ok = code == 0 and "오류 0건, 경고 8건" in out
    failures += not ok
    print(f"{'PASS' if ok else 'FAIL'}  KDN 예시: {out.strip().splitlines()[-1]}")
    code, out = run(TEMPLATE)
    ok = code == 0 and "오류 0건, 경고 0건" in out
    failures += not ok
    print(f"{'PASS' if ok else 'FAIL'}  빈 뼈대: {out.strip().splitlines()[-1]}")
    base = yaml.safe_load(EXAMPLE.read_text(encoding="utf-8"))
    for name, data, needle in mutations(base):
        code, out = run_data(data)
        ok = needle in out
        failures += not ok
        print(f"{'PASS' if ok else 'FAIL'}  {name}")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
