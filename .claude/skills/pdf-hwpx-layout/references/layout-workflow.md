# 제작 레시피

## 실행

아래 명령은 스킬 폴더를 현재 디렉터리로 가정한다. 입력 PDF와 출력 경로는 작업에 맞게 지정한다.

```bash
python3 -m pip install -r scripts/requirements.txt
python3 scripts/pdf_coords.py "/path/report.pdf" 51 "/path/analysis"
python3 scripts/kdn_p51.py "/path/report.pdf" "/path/draft.hwpx"
python3 scripts/check_hwpx.py "/path/draft.hwpx" --pdf "/path/report.pdf" --page 51
```

`kdn_p49.py`, `kdn_p50.py`, `kdn_p51.py`는 2025년도 한전KDN 경영실적보고서의 인쇄 29~31쪽에 각각 대응한다. 페이지 제목으로 입력을 확인하고, 다른 판본의 좌표는 시각 대조 후 조정한다. PDF에서 이미 대상 한 쪽을 추출했으면 레시피에 `--page 1`을 붙인다. 원본 PDF와 글꼴은 별도 입력이다.

## 새 쪽 구성

1. `page.png`에서 큰 구역을 먼저 나눈다. `page.json`의 좌표와 글꼴 크기로 영역별 줄을 묶는다. PDF 좌표는 포인트이며 원점은 왼쪽 위다. HWPX 생성기 치수는 **1/100포인트**다. 예를 들어 PDF 612×859pt는 61200×85900이다.
2. 새 작업용 스크립트에서 `hwpx_layout.Layout`과 `cell`을 가져온다. `pdf_coords.SourcePage`는 `region(x0, x1, y0, y1)`로 영역 안 글줄을 세로 순서대로 가져온다. 혼합 열을 한 번에 읽으면 숫자가 옆 칸으로 섞일 수 있으므로 셀 단위로 선택한다.
3. 바깥 배치는 일반 문단과 흐름에 놓인 한글 표로 구성한다. 평가내용 띠는 짙은 라벨과 사선 채움 셀, 본문 표는 옅은 머리칸과 얇은 테두리로 만든다. 페이지 번호와 제목은 별도 문단으로 배치한다. 측면 탭만 필요할 때 `floating=(x, y)`를 사용한다.
4. 표의 폭을 본문 폭 안에 맞추고 병합 셀의 너비와 높이에는 병합된 전체 치수를 준다. 표를 담는 문단은 고정 줄 높이를 쓰면 표가 겹칠 수 있다. 생성기의 `add_table`은 흐름에 맞게 문단이 늘어나는 설정을 쓴다. 목표 쪽수를 넘으면 긴 셀의 너비나 장평을 먼저 조정하고 높이와 간격을 다듬는다. 문구나 수치를 줄여 쪽수를 맞추지 않는다.

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

## 도표와 최종 검증

원본의 작은 그래프나 사진은 필요한 경우에만 삽입한다. 실제 한글에서 빈칸으로 나타나는지 반드시 확인한다. 이미지가 표시되지 않으면 편집 가능한 간단한 막대, 값 표, 등급 목록으로 정보를 보존하고 형태가 달라진 점을 알린다. 숫자가 확정되지 않으면 이미지의 모양을 보고 값을 만들어 내지 않는다.

`check_hwpx.py`는 문서 패키지와 텍스트를 검사한다. PDF 글줄이 모두 맞아도 셀 위치, 이미지 표시, 줄 겹침, 쪽 넘침은 판정할 수 없다. 사용자가 쓰는 한글에서 저장하고 재열기한 파일을 다시 검사하고, 시각 확인한 그 파일을 전달한다. 편집기 접근이 없는 환경에서는 그 단계가 남았다고 표시한다.
