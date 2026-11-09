#!/usr/bin/env python3
"""경영실적보고서 한 지표의 스토리라인(YAML)을 점검하고 Markdown 초안으로 펼친다.

usage:
  python3 scripts/storyline.py check  <storyline.yaml> [--toc-pdf report.pdf --toc-page N]
  python3 scripts/storyline.py render <storyline.yaml> <out.md>

check는 references/story-grammar.md의 서술 규칙을 기계적으로 확인한다. 오류가 있으면 1로 끝나고,
경고는 원문이나 초안에서 독자가 물어볼 만한 빈틈을 알린다. --toc-pdf를 주면 그 PDF 쪽의 세부목차와
스토리라인의 과제 제목·쪽 번호·평가내용 문구를 대조한다(PyMuPDF 필요).
"""

import argparse
import re
import sys
from pathlib import Path

import yaml

TEXT_KEYS = ("제목", "이름", "문제", "해결", "결과", "주석", "배경", "연결", "비전", "목표", "실적", "내용")
ENDINGS = ("고도화", "달성", "창출", "선도", "수립", "조성", "마련", "확산", "극대화", "구축", "정착", "강화",
           "추진", "운영", "해소", "실현", "제고", "확대", "개선", "정비", "확립", "도입", "혁신", "완료", "기여",
           "확보", "전환", "정립", "내실화", "체계화", "선정", "수상", "지원", "예방", "근절", "향상", "절감",
           "감축", "활성화", "증대", "이행", "차단", "대응", "실천", "완비", "보장")
TITLE_MAX = 50          # 세부목차 한 줄(쪽 번호 포함)에 들어가는 대략의 글자 수
FEEDBACK_BADGE = "지적사항 개선"
NUM = re.compile(r"(?<![’'\d.,])\d[\d,]*(?:\.\d+)?")


# ───────────────────────────── 읽기와 탐색

def load(path):
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict) or "평가내용" not in data:
        sys.exit(f"{path}: '평가내용' 목록이 있는 스토리라인 YAML이 아니다")
    return data


def as_list(value):
    if value is None:
        return []
    return value if isinstance(value, list) else [value]


def texts(node, keys=TEXT_KEYS):
    """노드 아래의 서술 문자열을 모두 모은다(형식·메모 같은 분석 주석은 뺀다)."""
    out = []
    if isinstance(node, dict):
        for k, v in node.items():
            if k in ("형식", "메모", "id", "회수", "축", "핵심어", "배지"):
                continue
            if k in keys and isinstance(v, str):
                out.append(v)
            elif isinstance(v, list) and k in keys:
                out += [x for x in v if isinstance(x, str)]
                for x in v:
                    if not isinstance(x, str):
                        out += texts(x, keys)
            else:
                out += texts(v, keys)
    elif isinstance(node, list):
        for x in node:
            out += texts(x, keys)
    return out


def numbers(text):
    """비교용 수치. ’24년 같은 연도 표기와 4월·12월 같은 날짜는 뺀다."""
    found = set()
    for m in NUM.finditer(text):
        if text[m.end():m.end() + 1] == "월":
            continue
        found.add(m.group().rstrip(",").replace(",", ""))
    return found


def scenes(task):
    return as_list(task.get("장면"))


def strands(node):
    return as_list(node.get("갈래"))


def ref_of(e, t, s=None):
    return f"{e['번호']}-{t['번호']}" + (f"-{s['기호']}" if s and s.get("기호") else "")


def index(data):
    """'평가내용-과제[-기호]' 참조를 노드로 푼다."""
    nodes = {}
    for e in data["평가내용"]:
        for t in as_list(e.get("과제")):
            nodes[ref_of(e, t)] = dict(kind="과제", e=e, t=t, node=t)
            for s in scenes(t):
                if s.get("기호"):
                    nodes[ref_of(e, t, s)] = dict(kind="장면", e=e, t=t, node=s)
    return nodes


def role(node, default="실행"):
    return node.get("역할", default)


def designs(data):
    """(설계 노드, 위치) — 과제와 장면에 달린 설계 블록 모두."""
    for e in data["평가내용"]:
        for t in as_list(e.get("과제")):
            if t.get("설계"):
                yield t["설계"], ref_of(e, t)
            for s in scenes(t):
                if s.get("설계"):
                    yield s["설계"], ref_of(e, t, s)


def axes(design):
    for a in as_list(design.get("축")):
        yield a
        for c in as_list(a.get("과제")):
            yield c


def badges(node):
    found = list(as_list(node.get("배지")))
    for s in scenes(node) + strands(node):
        found += badges(s)
    return found


def boxes_for(e, t):
    return [b for b in as_list(e.get("주요성과")) if t["번호"] in as_list(b.get("과제"))]


# ───────────────────────────── 점검

class Report:
    def __init__(self):
        self.items = []

    def error(self, where, msg):
        self.items.append(("오류", where, msg))

    def warn(self, where, msg):
        self.items.append(("경고", where, msg))

    def print(self):
        for level, where, msg in self.items:
            print(f"{level}  {where:<10} {msg}")
        errors = sum(1 for i in self.items if i[0] == "오류")
        print(f"\n오류 {errors}건, 경고 {len(self.items) - errors}건")
        return errors


def check(data, rep):
    nodes = index(data)
    tasks = [(e, t) for e in data["평가내용"] for t in as_list(e.get("과제"))]

    # 번호 차례와 쪽 순서
    last_page = data.get("쪽", {}).get("평가내용별", 0)
    for i, e in enumerate(data["평가내용"], 1):
        if e.get("번호") != i:
            rep.error(f"평가내용{e.get('번호')}", f"평가내용 번호가 {i}이어야 한다")
        for j, t in enumerate(as_list(e.get("과제")), 1):
            if t.get("번호") != j:
                rep.error(ref_of(e, t), f"과제 번호가 {j}이어야 한다")
            page = t.get("쪽")
            if page is None:
                rep.warn(ref_of(e, t), "쪽이 없다")
            elif page < last_page:
                rep.warn(ref_of(e, t), f"쪽 {page}이 앞 과제 쪽 {last_page}보다 앞선다")
            else:
                last_page = page

    # R1 편람 문구 분해 → 과제 매핑
    for e in data["평가내용"]:
        keys = dict(e.get("핵심어") or {})
        if not keys:
            rep.warn(f"평가내용{e['번호']}", "편람 문구를 핵심어로 나누지 않았다")
        claimed = set()
        for t in as_list(e.get("과제")):
            for node, where in [(t, ref_of(e, t))] + [(s, ref_of(e, t, s)) for s in scenes(t)]:
                for k in as_list(node.get("핵심어")):
                    if k not in keys:
                        rep.error(where, f"핵심어 {k}가 평가내용{e['번호']}에 없다")
                    claimed.add(k)
        for k, phrase in keys.items():
            if k not in claimed:
                rep.error(f"평가내용{e['번호']}", f"편람 핵심어 {k}「{phrase}」를 맡은 과제가 없다")

    # R2 설계 선행
    for e in data["평가내용"]:
        ts = as_list(e.get("과제"))
        if not ts:
            rep.error(f"평가내용{e['번호']}", "과제가 없다")
            continue
        first = ts[0]
        opener = role(first) == "설계" or (scenes(first) and role(scenes(first)[0]) in ("설계", "환류"))
        if not opener:
            rep.warn(ref_of(e, first), "평가내용의 첫 과제(또는 첫 장면)가 설계·환류가 아니다 — 왜·무엇을 먼저 세운다")

    # R3 복선과 회수: 설계 축 ↔ 실행 과제
    declared, parent, design_bg = {}, {}, {}
    for design, where in designs(data):
        for a in as_list(design.get("축")):
            for item in [a] + as_list(a.get("과제")):
                if item["id"] in declared:
                    rep.error(where, f"축 id {item['id']}가 중복된다")
                declared[item["id"]] = (item.get("이름", ""), where)
                design_bg[item["id"]] = bool(design.get("배경"))
            for c in as_list(a.get("과제")):
                parent[c["id"]] = a["id"]
    used = {}
    for e, t in tasks:
        for node, where in ([(t, ref_of(e, t))] + [(s, ref_of(e, t, s)) for s in scenes(t)]
                            + [(g, ref_of(e, t, s)) for s in scenes(t) for g in strands(s)]):
            for a in as_list(node.get("축")):
                if a not in declared:
                    rep.error(where, f"축 {a}는 어느 설계에도 없다")
                used.setdefault(a, []).append(where)
                if a in parent:
                    used.setdefault(parent[a], []).append(where)
    for a, (name, where) in declared.items():
        if a in used:
            continue
        if a in parent:
            rep.warn(where, f"추진과제 {a}「{name}」를 회수하는 과제·장면이 없다")
        elif a in parent.values():
            rep.warn(where, f"설계 축 {a}「{name}」의 추진과제가 하나도 회수되지 않았다")
        else:
            rep.warn(where, f"설계 축 {a}「{name}」를 회수하는 과제·장면이 없다")
    for e, t in tasks:
        if role(t) != "실행":
            continue
        refs = as_list(t.get("축")) + [a for s in scenes(t) for a in as_list(s.get("축"))] + \
            [a for s in scenes(t) for g in strands(s) for a in as_list(g.get("축"))]
        if not refs:
            rep.warn(ref_of(e, t), "어느 설계 축을 회수하는지 적지 않았다(축)")

    # R3b 설계 목표·성과지표의 회수
    for design, where in designs(data):
        for group in ("세부목표", "성과지표"):
            for g in as_list(design.get(group)):
                target = g.get("회수")
                if not target:
                    memo = f" — {g['메모']}" if g.get("메모") else ""
                    rep.warn(where, f"{group}「{g.get('항목')}」를 본문에서 실적으로 회수하지 않았다{memo}")
                elif str(target) not in nodes:
                    rep.error(where, f"{group}「{g.get('항목')}」의 회수 위치 {target}가 없다")
                elif not g.get("실적"):
                    rep.warn(where, f"{group}「{g.get('항목')}」에 회수한 실적 문구가 없다")

    # R4 장면 비트: 문제(왜) → 해결 → 결과
    feedback_refs = set()
    for j in as_list(data.get("지적사항")):
        for r in as_list(j.get("회수")):
            feedback_refs.add(str(r))
    for e, t in tasks:
        if role(t) == "설계":
            continue
        for s in scenes(t) or [t]:
            where = ref_of(e, t, s if s is not t else None)
            parts = [s] + strands(s)
            has = {b: any(p.get(b) for p in parts) for b in ("문제", "해결", "결과")}
            if s.get("설계", {}).get("배경"):
                has["문제"] = True
            if not has["문제"]:
                linked = (ref_of(e, t) in feedback_refs or where in feedback_refs
                          or FEEDBACK_BADGE in badges(t))
                axes_here = as_list(t.get("축")) + [a for p in parts for a in as_list(p.get("축"))]
                via_axis = any(design_bg.get(a) or design_bg.get(parent.get(a)) for a in axes_here)
                if not (linked or via_axis):
                    rep.warn(where, "왜(문제·배경·현황)가 없다 — 장면 안이나 설계·지적사항에서 이어 받는다")
            for b in ("해결", "결과"):
                if not has[b]:
                    rep.warn(where, f"{b}이 없다")

    # R5 쪽 결말: 실행 과제마다 주요성과 상자, 상자마다 수치
    for e in data["평가내용"]:
        ts = {t["번호"]: t for t in as_list(e.get("과제"))}
        for b in as_list(e.get("주요성과")):
            covered = as_list(b.get("과제"))
            for n in covered:
                if n not in ts:
                    rep.error(f"평가내용{e['번호']}", f"주요성과(p.{b.get('쪽')})가 없는 과제 {n}을 가리킨다")
            if not any(numbers(x) for x in as_list(b.get("내용"))):
                rep.warn(f"평가내용{e['번호']}", f"주요성과(p.{b.get('쪽')})에 수치가 없다")
            if covered and covered[-1] in ts and ts[covered[-1]].get("쪽") != b.get("쪽"):
                rep.warn(f"평가내용{e['번호']}", f"주요성과 쪽 {b.get('쪽')}이 마지막 과제 쪽과 다르다")
        for t in ts.values():
            if role(t) == "실행" and not boxes_for(e, t):
                rep.warn(ref_of(e, t), "이 과제를 맺는 주요성과 상자가 없다")

    # R6 지적사항 환류: Ⅰ표 ↔ 배지 ↔ 참고쪽 ↔ 같은 수치
    seen = set()
    for j in as_list(data.get("지적사항")):
        where = j.get("id", "지적사항")
        if where in seen:
            rep.error(where, "지적사항 id가 중복된다")
        seen.add(where)
        targets = [str(r) for r in as_list(j.get("회수"))]
        if not targets:
            rep.error(where, "회수 위치가 없다")
            continue
        scope, pages = [], set()
        for r in targets:
            hit = nodes.get(r)
            if not hit:
                rep.error(where, f"회수 위치 {r}가 없다")
                continue
            if hit["e"]["번호"] != j.get("평가내용"):
                rep.error(where, f"회수 위치 {r}가 평가내용{j.get('평가내용')}에 있지 않다")
            if FEEDBACK_BADGE not in badges(hit["node"]) + as_list(hit["t"].get("배지")):
                rep.warn(where, f"{r}에 「{FEEDBACK_BADGE}」 배지가 없다")
            pages.add(hit["t"].get("쪽"))
            scope += texts(hit["node"])
            for b in boxes_for(hit["e"], hit["t"]):
                scope += as_list(b.get("내용"))
        if j.get("참고쪽") not in pages:
            rep.warn(where, f"참고쪽 {j.get('참고쪽')}이 회수 과제 쪽 {sorted(p for p in pages if p)}과 다르다")
        missing = sorted(numbers(" ".join(as_list(j.get("성과")))) - numbers(" ".join(scope)), key=float)
        if missing:
            rep.warn(where, f"Ⅰ표 성과의 수치 {', '.join(missing)}가 참고쪽 본문·주요성과에 그대로 보이지 않는다")
    for ref, hit in nodes.items():
        if FEEDBACK_BADGE in as_list(hit["node"].get("배지")) + [b for g in strands(hit["node"])
                                                                 for b in as_list(g.get("배지"))]:
            t_ref = ref_of(hit["e"], hit["t"])
            if not ({ref, t_ref} & feedback_refs or any(r.startswith(ref + "-") for r in feedback_refs)):
                rep.warn(ref, f"「{FEEDBACK_BADGE}」 배지가 있으나 Ⅰ표의 어느 지적사항도 이곳을 가리키지 않는다")

    # R7 Ⅱ 주요 추진실적: 세 칸과 수치 일치
    for e in data["평가내용"]:
        summary = e.get("요약") or {}
        for col in ("이전", "올해", "개선"):
            if not as_list(summary.get(col)):
                rep.warn(f"평가내용{e['번호']}", f"Ⅱ표 ‘{col}’ 칸이 비었다")
        body = " ".join(texts(e.get("과제")) + [x for b in as_list(e.get("주요성과")) for x in as_list(b.get("내용"))])
        missing = sorted(numbers(" ".join(as_list(summary.get("개선")))) - numbers(body), key=float)
        if missing:
            rep.warn(f"평가내용{e['번호']}", f"Ⅱ표 개선성과의 수치 {', '.join(missing)}가 본문에 그대로 보이지 않는다")

    # R8 제목 문법
    for e, t in tasks:
        for node, where in [(t, ref_of(e, t))] + [(s, ref_of(e, t, s)) for s in scenes(t) if s.get("제목")]:
            title = node.get("제목", "")
            bare = re.sub(r"[」』\s〉)]+$", "", title)
            if not bare.endswith(ENDINGS):
                rep.warn(where, f"제목이 결과를 뜻하는 명사(달성·창출·구축…)로 끝나지 않는다: {title}")
        if len(t.get("제목", "")) > TITLE_MAX:
            rep.warn(ref_of(e, t), f"과제 제목이 {len(t['제목'])}자 — 세부목차 한 줄({TITLE_MAX}자 안팎)을 넘길 수 있다")


# ───────────────────────────── 세부목차 대조

def toc_check(data, pdf, page, rep):
    import pymupdf
    doc = pymupdf.open(pdf)
    lines = []
    for block in doc[page - 1].get_text("dict")["blocks"]:
        for line in block.get("lines", []):
            text = "".join(s["text"] for s in line["spans"])
            if text.strip():
                lines.append(re.sub(r"\s+", "", text))
    whole = "".join(lines)
    entries = {}
    for line in lines:
        m = re.match(r"^(.*?)[·.…]{3,}(\d+)$", line)
        if m:
            entries[m.group(1)] = int(m.group(2))
    year = data.get("연도", "")
    expected = [(f"Ⅰ.외부지적사항조치실적", data.get("쪽", {}).get("지적사항")),
                (f"Ⅱ.{year}년주요추진실적", data.get("쪽", {}).get("주요추진실적")),
                ("Ⅲ.세부평가내용별주요추진실적", data.get("쪽", {}).get("평가내용별"))]
    for e in data["평가내용"]:
        phrase = re.sub(r"\s+", "", e["문구"])
        if phrase not in whole:
            rep.error("세부목차", f"평가내용{e['번호']} 문구가 PDF 세부목차와 다르다")
        for t in as_list(e.get("과제")):
            expected.append((f"{t['번호']}.{re.sub(r'\s+', '', t['제목'])}", t.get("쪽")))
    matched = 0
    for title, page_no in expected:
        if title not in entries:
            rep.error("세부목차", f"PDF에 없는 항목: {title}")
        elif entries[title] != page_no:
            rep.error("세부목차", f"쪽 번호가 다르다: {title} — PDF {entries[title]}, 스토리라인 {page_no}")
        else:
            matched += 1
    print(f"세부목차 대조: {matched}/{len(expected)}개 항목 일치 (PDF {Path(pdf).name} {page}쪽)")


# ───────────────────────────── Markdown 초안

def md(text):
    return str(text).replace("|", "\\|")


def bullets(items, indent="", label=None):
    out = []
    items = as_list(items)
    if not items:
        return out
    if label:
        if len(items) == 1:
            return [f"{indent}- **{label}** {md(items[0])}"]
        out.append(f"{indent}- **{label}**")
        indent += "  "
    out += [f"{indent}- {md(x)}" for x in items]
    return out


def badge_text(node):
    return "".join(f" 〈{b}〉" for b in as_list(node.get("배지")))


def render_design(d, ref_users):
    out = []
    out += bullets(d.get("배경"), label="배경·환경분석")
    for key in ("연결", "비전", "목표"):
        if d.get(key):
            out.append(f"- **{key}** {md(d[key])}")
    if d.get("세부목표"):
        out += ["", "| 세부목표 | 목표 | 회수 | 실적·메모 |", "|---|---|---|---|"]
        for g in d["세부목표"]:
            out.append(f"| {md(g.get('항목'))} | {md(g.get('목표', ''))} | {g.get('회수') or '—'} | "
                       f"{md(g.get('실적') or g.get('메모') or '')} |")
        out.append("")
    out += bullets(d.get("설정근거"), label="설정근거")
    if d.get("축"):
        out += ["", "| 축 | 추진과제 | 회수하는 곳 |", "|---|---|---|"]
        for a in d["축"]:
            kids = as_list(a.get("과제")) or [None]
            for c in kids:
                item = c or a
                out.append(f"| {a['id']} {md(a['이름'])} | {(md(c['id'] + ' ' + c['이름'])) if c else '—'} | "
                           f"{', '.join(sorted(set(ref_users.get(item['id'], [])))) or '—'} |")
        out.append("")
    if d.get("성과지표"):
        out += ["| 성과지표 | 회수 | 실적·메모 |", "|---|---|---|"]
        for g in d["성과지표"]:
            note = " / ".join(x for x in (g.get("실적"), g.get("메모")) if x)
            out.append(f"| {md(g.get('항목'))} | {g.get('회수') or '—'} | {md(note)} |")
        out.append("")
    return out


def render_scene(s, title_prefix):
    out = []
    tag = f"[{s['태그']}] " if s.get("태그") else ""
    head = f"{title_prefix}{tag}{md(s.get('제목', ''))}" if s.get("제목") else title_prefix.rstrip(". ")
    if head:
        out.append(f"**{head}**{badge_text(s)}" + (f" · 축 {', '.join(as_list(s['축']))}" if s.get("축") else ""))
    if s.get("형식"):
        out.append(f"<sub>형식: {md(s['형식'])}</sub>")
    out.append("")
    for beat in ("문제", "해결"):
        out += bullets(s.get(beat), label=beat)
    for g in strands(s):
        out.append(f"- **{md(g.get('이름', ''))}**{badge_text(g)}"
                   + (f" · 축 {', '.join(as_list(g['축']))}" if g.get("축") else ""))
        for beat in ("문제", "해결", "결과"):
            out += bullets(g.get(beat), indent="  ", label=beat)
    out += bullets(s.get("결과"), label="결과")
    out += [f"<sub>* {md(x)}</sub>" for x in as_list(s.get("주석"))]
    out.append("")
    return out


def render(data):
    nodes = index(data)
    ind = data["지표"]
    year = int(data.get("연도", 0)) or None
    prev = f"’{(year - 1) % 100:02d}년도까지의 실적" if year else "전년도까지의 실적"
    now = f"’{year % 100:02d}년도 주요 실적" if year else "올해 주요 실적"
    pages = data.get("쪽", {})

    users = {}
    for e in data["평가내용"]:
        for t in as_list(e.get("과제")):
            for node, where in ([(t, ref_of(e, t))] + [(s, ref_of(e, t, s)) for s in scenes(t)]
                                + [(g, ref_of(e, t, s)) for s in scenes(t) for g in strands(s)]):
                for a in as_list(node.get("축")):
                    users.setdefault(a, []).append(where)

    out = [f"# {ind['지표명']} — 실적 스토리라인", "",
           f"> {data.get('보고서', '')} · {' > '.join(x for x in (ind.get('범주'), ind.get('평가지표'), ind.get('지표명')) if x)} · "
           f"가중치 {ind.get('가중치', '')} · "
           f"{ind.get('지표성격', '')} · {ind.get('평가방법', '')}  ",
           f"> **지표정의** {ind.get('지표정의', '')}", ""]

    out += ["## 줄거리 지도", "",
            "| 평가내용 | 여는 과제(설계·환류) | 이어지는 실행 과제 | 쪽 결말(주요성과) |", "|---|---|---|---|"]
    for e in data["평가내용"]:
        ts = as_list(e.get("과제"))
        opener = [f"{t['번호']}. {t['제목']}" for t in ts if role(t) == "설계"]
        opener += [f"{t['번호']}-{s['기호']}. {s['제목']}" for t in ts for s in scenes(t) if role(s) in ("설계", "환류")]
        doers = [f"{t['번호']}. {t['제목']}" for t in ts if role(t) == "실행"]
        ends = [f"p.{b.get('쪽')} {as_list(b.get('내용'))[0]}" for b in as_list(e.get("주요성과")) if b.get("내용")]
        out.append(f"| {e['번호']}. {md(e['문구'])} | {md('<br>'.join(opener)) or '—'} | "
                   f"{md('<br>'.join(doers))} | {md('<br>'.join(ends))} |")
    out.append("")

    out += ["## 세부목차", "",
            f"- Ⅰ. 외부 지적사항 조치실적 — {pages.get('지적사항', '')}",
            f"- Ⅱ. {year or ''}년 주요 추진실적 — {pages.get('주요추진실적', '')}",
            f"- Ⅲ. 세부 평가내용별 주요 추진실적 — {pages.get('평가내용별', '')}", ""]
    for e in data["평가내용"]:
        out.append(f"**평가내용 {e['번호']}** {md(e['문구'])}")
        out.append("")
        out += [f"{t['번호']}. {md(t['제목'])} — {t.get('쪽', '')}" for t in as_list(e.get("과제"))]
        out.append("")

    out += ["## Ⅰ. 외부 지적사항 조치실적", "", "| 지적사항 | 조치 및 개선실적 | 회수 위치 | 참고 |", "|---|---|---|---|"]
    for j in as_list(data.get("지적사항")):
        acts = "<br>".join(f"∙{md(x)}" for x in as_list(j.get("조치")))
        acts += "".join(f"<br>▣ **{md(x)}**" for x in as_list(j.get("성과")))
        out.append(f"| ∙{md(j.get('지적', ''))} | {acts} | {', '.join(map(str, as_list(j.get('회수'))))} | "
                   f"p.{j.get('참고쪽', '')} |")
    if data.get("외부지적"):
        out += ["", f"※ {data['외부지적']}"]
    out.append("")

    out += [f"## Ⅱ. {year or ''}년 주요 추진실적", ""]
    for e in data["평가내용"]:
        s = e.get("요약") or {}
        out += [f"**평가내용 {e['번호']:02d}** {md(e['문구'])}", "",
                f"| {prev} | {now} | 전년대비 개선성과 |", "|---|---|---|",
                "| " + " | ".join("<br>".join(f"∙{md(x)}" for x in as_list(s.get(c))) for c in ("이전", "올해", "개선"))
                + " |", ""]

    out += ["## Ⅲ. 세부 평가내용별 주요 추진실적", ""]
    for e in data["평가내용"]:
        out += [f"### 평가내용 {e['번호']:02d} — {md(e['문구'])}", ""]
        keys = e.get("핵심어") or {}
        if keys:
            claim = {}
            for t in as_list(e.get("과제")):
                for node, where in [(t, f"{t['번호']}")] + [(s, f"{t['번호']}-{s['기호']}") for s in scenes(t)
                                                             if s.get("기호")]:
                    for k in as_list(node.get("핵심어")):
                        claim.setdefault(k, []).append(where)
            out.append("편람 문구 분해: " + " · ".join(f"{k}「{md(v)}」→{','.join(claim.get(k, ['—']))}"
                                                 for k, v in keys.items()))
            out.append("")
        for t in as_list(e.get("과제")):
            mark = " `설계`" if role(t) == "설계" else ""
            axis = f" · 축 {', '.join(as_list(t['축']))}" if t.get("축") else ""
            out += [f"#### {t['번호']}. {md(t['제목'])}{mark}{badge_text(t)}", f"<sub>p.{t.get('쪽', '')}{axis}"
                    + (f" · 형식: {md(t['형식'])}" if t.get("형식") else "") + "</sub>", ""]
            if t.get("설계"):
                out += render_design(t["설계"], users)
            for s in scenes(t):
                prefix = f"{s['기호']}. " if s.get("기호") else ""
                out += render_scene(s, prefix)
                if s.get("설계"):
                    out += render_design(s["설계"], users)
            for b in as_list(e.get("주요성과")):
                if as_list(b.get("과제")) and as_list(b["과제"])[-1] == t["번호"]:
                    out.append(f"> **주요성과** (p.{b.get('쪽')}, 과제 {', '.join(map(str, b['과제']))})  ")
                    out += [f"> ∙{md(x)}  " for x in as_list(b.get("내용"))]
                    out.append("")
    return "\n".join(out).rstrip() + "\n"


# ───────────────────────────── main

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check", help="서술 규칙 점검")
    c.add_argument("storyline")
    c.add_argument("--toc-pdf", help="세부목차 쪽이 든 PDF")
    c.add_argument("--toc-page", type=int, help="그 PDF 안의 세부목차 쪽 번호(PDF 뷰어 기준)")
    r = sub.add_parser("render", help="Markdown 초안 생성")
    r.add_argument("storyline")
    r.add_argument("out")
    args = ap.parse_args()

    data = load(args.storyline)
    if args.cmd == "render":
        Path(args.out).write_text(render(data), encoding="utf-8")
        print(f"wrote {args.out}")
        return
    rep = Report()
    check(data, rep)
    if args.toc_pdf:
        if not args.toc_page:
            sys.exit("--toc-pdf에는 --toc-page가 필요하다")
        toc_check(data, args.toc_pdf, args.toc_page, rep)
    sys.exit(1 if rep.print() else 0)


if __name__ == "__main__":
    main()
