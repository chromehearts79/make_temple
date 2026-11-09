---
name: pdf-hwpx-layout
description: Rebuild Korean PDF report pages as editable HWPX while matching their visual layout. Use for PDF-to-HWPX design restoration, especially public-sector reports with tables, achievement boxes and evaluation banners. 호출어 "템플릿 제작" — 사용자가 "템플릿 제작"이라고 부르면 이 스킬을 호출한다.
---

# PDF → 편집 가능한 HWPX 복원

PDF에 보이는 쪽의 배치를 한글 문단과 표로 옮긴다. 본문과 표의 편집성, 원문 수치와 쪽별 배치를 유지한다. 대상은 PDF 뷰어 기준 쪽 번호로 먼저 확정한다. 인쇄된 쪽 번호와 다르면 둘 다 기록한다.

1. 원본 PDF가 있으면 `scripts/pdf_coords.py`로 쪽 이미지와 글줄 좌표를 뽑는다. 이미지로 제목 띠, 열, 병합 셀, 성과 상자, 도표를 확인하고 좌표를 기준으로 원문을 각 영역에 넣는다. 스크린샷이나 스캔에서만 보이는 내용은 별도로 읽고, 불확실한 숫자는 원본과 확인한다. 글줄 안의 작은 색 상자 꼬리표(박스 안의 박스)는 글자층에서 한 줄로 합쳐 나오므로, 이 스크립트가 따로 알리는 `inline_tags`를 보고 `Layout.boxed_line`으로 만든다. 그림으로 된 번호 상자(❶, [1])도 같은 방식으로 넣는다.
2. 같은 한전KDN 경영실적보고서의 실제 PDF 49~51쪽이면 `scripts/kdn_p49.py`, `scripts/kdn_p50.py`, `scripts/kdn_p51.py`로 재현한다. 그 외 쪽은 [제작 레시피](references/layout-workflow.md)를 읽고 `scripts/hwpx_layout.py`로 구성한다. 쪽 전체를 이미지로 붙이는 방식은 편집용 복원으로 취급하지 않는다.
3. `scripts/check_hwpx.py`로 ZIP, XML과 참조를 점검하고 PDF에서 추출한 글줄과 대조한다. `scripts/hwpx_preview.py`로 결과를 원본 쪽 옆에 대략 그려 칸 배치와 쪽 넘침을 본다. 대체 글꼴로 그리므로 높이가 실제보다 0~45pt 크게 나온다. 누락 판정은 영역 분리나 줄 재배치 때문에 생길 수 있으므로 각 항목을 원본과 직접 확인한다. 이미지에만 있던 숫자, 표의 행·열 대응, 도표 값은 별도 대조한다.
4. 사용자의 실제 한글 편집기에서 결과를 열고 저장한 뒤 닫았다가 다시 연다. 모든 쪽의 본문, 표, 서식, 빈 쪽, 겹침, 잘림, 쪽수와 글자 크기를 확인한다. Mac 한글 2014 VP 대상 앱 ID는 `com.hancom.office.hwp.mac.general`이다. 저장본을 수정하면 검증을 반복한다. Claude 환경에서 해당 앱에 접근할 수 없으면 파일을 **편집기 검증 전 시안**으로 표시하고, 구조 검사와 편집기 검증을 구분한다.

도형 조각을 글자로 옮길 때는 KS X 1001 안의 기호, 곧 EUC-KR로 인코딩되는 기호만 쓴다. → ▶ ▼ ① ■ □ ▣ ◎ ※는 그 안에 있고 ➜ ❶ ✓ ▪ ☑ ▬는 밖에 있다. 밖의 기호는 KoPub돋움체 같은 한글 글꼴에 없을 수 있어, 한글이 대체 글꼴로 그리며 크기와 높이가 어긋난다. Mac 한글에서 ➜ ❶ ✓ ▪를 이 기호들로 바꾸자 화살표 정렬이 나아졌다. `check_hwpx.py`는 레시피가 넣은 이런 기호를 실패로 표시한다. 원문에 있던 글자는 바꾸지 않는다. 연결 기호 하나만 든 칸은 생성기가 좌우 여백을 같게 맞춘다.

Python 3.10 이상과 `scripts/requirements.txt`의 PyMuPDF, lxml이 필요하다. 기본 글꼴은 KoPub돋움체 Medium과 Bold이며, 실제 표시에는 편집기 환경에 해당 글꼴이 있어야 한다. 사용자가 다른 글꼴을 지정하면 그 글꼴의 실제 이름을 사용한다.

전권 요청에는 대표 쪽을 유형별로 먼저 복원한다. 표준 레이아웃을 재사용하고, 병합 표·사진·복합 도표가 다른 쪽은 별도로 조정한다. 샘플 레시피가 전권에 맞는다고 가정하지 않는다. 쪽별 파일은 `scripts/merge_hwpx.py`로 한 문서로 합친다. 쪽마다 구역이 되어 여백 같은 쪽 설정이 유지되고, 쪽이 추가한 서식은 번호를 다시 매겨 겹치지 않게 한다.
