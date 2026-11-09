# 제작 레시피

## 실행

아래 명령은 스킬 폴더를 현재 디렉터리로 가정한다. 입력 PDF와 출력 경로는 작업에 맞게 지정한다.

```bash
python3 -m pip install -r scripts/requirements.txt
python3 scripts/pdf_snapshot.py "/path/report.pdf" "/path/sources" --number-from 1   # 처음 한 번
python3 scripts/pdf_coords.py "/path/report.pdf" 51 "/path/analysis"
python3 scripts/kdn_p51.py "/path/report.pdf" "/path/draft.hwpx"
python3 scripts/check_hwpx.py "/path/draft.hwpx" --pdf "/path/report.pdf" --page 51
python3 scripts/hwpx_preview.py "/path/draft.hwpx" "/path/preview.png" --pdf "/path/report.pdf" --page 51
python3 scripts/hwpx_preview.py "/path/draft.hwpx" "/path/preview.png" --ref "/path/screenshot.png"
python3 scripts/merge_hwpx.py "/path/merged.hwpx" "/path/p01.hwpx" "/path/p02.hwpx"
```

`hwpx_preview.py`는 Node의 playwright와 Chromium이 있어야 한다. Claude 클라우드 세션에는 미리 설치되어 있다.

### PDF 없이 다시 만들기: 쪽 스냅숏

원본 PDF는 세션마다 따라오지 않는다. PDF가 있을 때 `pdf_snapshot.py`로 쪽마다 `pNNN.json.gz`(글자층, 그림 정보, 이미지 위치)와 `pNNN.png`(쪽 그림)를 한 번 만들어 저장소에 두면, 이후에는 PDF 자리에 스냅숏을 넘겨 레시피, `pdf_coords.py`, `check_hwpx.py --pdf`, `hwpx_preview.py --pdf`를 그대로 돌릴 수 있다. 스냅숏에는 `--page`가 필요 없다. 여러 PDF로 나뉜 보고서는 `--number-from 51`처럼 보고서 쪽 번호로 이름을 맞춘다. 레시피가 스냅숏에 없는 `get_text` 형식을 부르면 오류로 알려 준다. 그때는 `pdf_coords.SNAPSHOT_TEXT`에 그 형식을 더하고 스냅숏을 다시 만든다. 빽빽한 쪽 하나가 약 180KB다.

원본 PDF도 스냅숏도 없으면 사용자에게 그 쪽 화면(스크린샷)을 받는다. `hwpx_preview.py --ref 화면.png`가 결과를 그 옆에 놓아 준다. 다만 글자층이 없으므로 원문 대조는 이전 결과물과 비교하는 것으로 대신한다.

`kdn_p49.py`, `kdn_p50.py`, `kdn_p51.py`는 2025년도 한전KDN 경영실적보고서의 인쇄 29~31쪽에 각각 대응한다. 페이지 제목으로 입력을 확인하고, 다른 판본의 좌표는 시각 대조 후 조정한다. PDF에서 이미 대상 한 쪽을 추출했으면 레시피에 `--page 1`을 붙인다. 원본 PDF와 글꼴은 별도 입력이다.

## 새 쪽 구성

1. `page.png`에서 큰 구역을 먼저 나눈다. `page.json`의 좌표와 글꼴 크기로 영역별 줄을 묶는다. PDF 좌표는 포인트이며 원점은 왼쪽 위다. HWPX 생성기 치수는 **1/100포인트**다. 예를 들어 PDF 612×859pt는 61200×85900이다.
2. 새 작업용 스크립트에서 `hwpx_layout.Layout`과 `cell`을 가져온다. `pdf_coords.SourcePage`는 `region(x0, x1, y0, y1)`로 영역 안 글줄을 세로 순서대로 가져온다. 혼합 열을 한 번에 읽으면 숫자가 옆 칸으로 섞일 수 있으므로 셀 단위로 선택한다.
3. 바깥 배치는 일반 문단과 흐름에 놓인 한글 표로 구성한다. 평가내용 띠는 짙은 라벨과 사선 채움 셀, 본문 표는 옅은 머리칸과 얇은 테두리로 만든다. 페이지 번호와 제목은 별도 문단으로 배치한다. 측면 탭만 필요할 때 `floating=(x, y)`를 사용한다.
4. 표의 폭을 본문 폭 안에 맞추고 병합 셀의 너비와 높이에는 병합된 전체 치수를 준다. 표를 담는 문단은 고정 줄 높이를 쓰면 표가 겹칠 수 있다. 생성기의 `add_table`은 흐름에 맞게 문단이 늘어나는 설정을 쓴다. 목표 쪽수를 넘으면 긴 셀의 너비나 장평을 먼저 조정하고 높이와 간격을 다듬는다. 문구나 수치를 줄여 쪽수를 맞추지 않는다.
5. 원본 PDF 글꼴은 한글 폭이 0.85em 안팎으로 좁은 경우가 많다. PDF 글줄 폭에 맞춰 칸을 잡으면 편집기에서 줄이 넘어가므로, 한 줄로 둘 칸은 PDF 폭의 1.2배쯤 여유를 두거나 장평을 낮춘다.
6. 목차 점선(····)은 글자로 넣지 않는다. 점 글자 폭이 글꼴마다 달라 여러 줄로 넘어갈 수 있다. 제목 칸, 아래 테두리만 `border(bottom="dot")`인 빈 칸, 쪽 번호 칸을 한 행에 놓는다. `check_hwpx.py`는 점선 줄을 이 방식 기준으로 대조한다.

## 기호와 연결 칸

화살표, 번호 상자, 체크 표시처럼 원본에서 그림이던 조각은 KS X 1001 기호로 옮긴다. 그 밖의 기호는 KoPub돋움체에 없을 수 있어 한글이 대체 글꼴로 그리고, 크기와 기준선이 틀어져 정렬이 어색해진다. `check_hwpx.py --pdf`는 레시피가 넣은 이런 기호를 실패로 표시하고, 원문에 원래 있던 글자(예: ∙ ･)는 참고로만 알린다.

| 피할 기호 | 대신 쓸 기호 |
|---|---|
| ➜ ➡ (본문 속 화살표) | → |
| ➜ (상자 사이 연결 칸) | ▶ ▼ |
| ❶ ❷ ❸ (동그라미) | ① ② ③ |
| 네모 번호 그림(■1, □1) | `tag("1", …)` 번호 상자 ([상자 속 상자 유형집](box-patterns.md)) |
| ✓ (평가내용 배지) | 지운다 |
| ✓ (목록 머리표) | ◎ |
| ☑ | ▣ |
| ▪ (제목 옆 꼬리표) | ■, 제목보다 작은 글자 run으로 |
| ▬ (막대) | ━ |

PDF 글자층에 Wingdings 같은 기호 글꼴의 사용자 정의 문자(예: 가운뎃점 U+F09E)가 섞여 있으면, 편집기에서는 빈칸이나 네모로 보인다. 생성기는 파일을 쓸 때 이를 KS X 1001 문자(·)로 바꾸고(`PUA_MAP`), `check_hwpx.py`는 둘을 같은 글자로 대조한다. 새 문자를 만나면 두 파일의 `PUA_MAP`에 함께 추가한다.

`+ ▶ ◀ ▲ ▼ → ← ↑ ↓ ↔ ⇒` 가운데 하나만 든 칸은 연결 칸으로 보고, 생성기가 좌우 여백을 0으로 맞춰 기호를 칸 가운데에 둔다. 기본 여백은 왼쪽 320, 오른쪽 180이라 그대로 두면 기호가 오른쪽으로 밀린다. 여백을 직접 정할 때는 `cell(..., margin=dict(left=0, right=0))`을 쓴다.

## 박스 안의 박스

글줄 안의 작은 상자(꼬리표, 번호 상자)와 칸 안에 들어간 상자는 PDF 글자층에서 보이지 않는다. 글줄 좌표만으로 만들면 상자가 사라진다. 판단 근거는 그림 정보에 있다. 글줄 일부만 감싸는 작은 채움이나 테두리 사각형이 있고 바로 옆에 같은 줄 글자가 있으면 꼬리표다. `pdf_coords.py`는 이것을 `page.json`의 `inline_tags`로 저장하고, 위치(start·middle·end), 채움색 또는 outline, 글자색을 화면에 찍는다. 옆 칸에 든 글자는 옆에 있어도 같은 줄로 치지 않으므로 표 머리 행은 잡히지 않는다. 그래도 라벨 칸이 섞일 수 있어 `page.png`와 대조한다.

만드는 법과 50쪽에서 쓴 유형별 코드는 [상자 속 상자 유형집](box-patterns.md)에 있다. 레시피를 쓰기 전에 그 문서의 "디자인 목록"부터 만든다.

```python
from hwpx_layout import Layout, cell

page = Layout(top=3180)
page.add_text("Ⅰ. 추진실적", 1800, True, align="CENTER", line=2400)
fill = page.border("#D8D8D8", top="strong", bottom="soft", sides="soft")
page.add_table([
    [cell(0, 10000, 1900, page.center("구분", bold=True), fill),
     cell(1, 39900, 1900, page.center("추진성과", bold=True), fill)],
    [cell(0, 10000, 3400, [page.p("실적")], fill),
     cell(1, 39900, 3400, [page.p("원문 그대로")])],
])
page.write("draft.hwpx")
```

## kordoc으로 보조 점검

npm 패키지 kordoc(4.24.56에서 확인)은 HWPX를 읽고, 검증하고, 렌더링한다. 아래는 선택 사항이다.

```bash
npx kordoc validate draft.hwpx                       # 패키지 구조 검증
npx kordoc draft.hwpx -o draft.md                    # 읽기 순서와 글자 확인(상자 속 상자는 "a / b"로 읽힘)
npx kordoc render draft.hwpx --format png -d pages   # 칸 배치 확인용 렌더
```

생성본은 kordoc이 자체 조판으로 그린다. 이 조판은 칸 안 글을 줄바꿈하지 않고, 이 환경의 대체 글꼴이 넓어 글이 칸 밖으로 넘친다. 그래서 줄 폭과 쪽 넘침은 `hwpx_preview.py`와 한글에서 판단한다. `kordoc generate`(마크다운 → 공문서 HWPX)는 정해진 공문서 서식으로 다시 짜므로, 원본 쪽 배치를 복원하는 용도로는 맞지 않는다. 50쪽에서 시험하자 3쪽으로 늘고 상자 속 상자가 글로 풀렸다. 이미지 OCR 모델은 huggingface.co에서 받으므로 그 호스트가 막힌 환경에서는 쓰지 못한다.

## 도표와 최종 검증

원본의 작은 그래프나 사진은 필요한 경우에만 삽입한다. 실제 한글에서 빈칸으로 나타나는지 반드시 확인한다. 이미지가 표시되지 않으면 편집 가능한 간단한 막대, 값 표, 등급 목록으로 정보를 보존하고 형태가 달라진 점을 알린다. 숫자가 확정되지 않으면 이미지의 모양을 보고 값을 만들어 내지 않는다.

`hwpx_preview.py`는 결과를 원본 쪽 옆에 대략 그리고 넘침을 계산한다. 대체 글꼴이 넓어 높이가 실제보다 0~45pt 크게 나온다. 검증된 레시피(49·50쪽)가 +5pt, +41pt로 나오므로 +20pt 안팎이면 한 쪽에 들어갈 가능성이 높다. 셀 배치와 병합이 어긋났는지 보는 데 쓰고, 최종 판정은 편집기에서 한다.

`check_hwpx.py`는 문서 패키지와 텍스트를 검사한다. PDF 글줄이 모두 맞아도 셀 위치, 이미지 표시, 줄 겹침, 쪽 넘침은 판정할 수 없다. 사용자가 쓰는 한글에서 저장하고 재열기한 파일을 다시 검사하고, 시각 확인한 그 파일을 전달한다. 편집기 접근이 없는 환경에서는 그 단계가 남았다고 표시한다.
