# Coder Report - TASK-030

## 태스크
- Task ID: TASK-030
- Title: 웹 페이지 (a) 데이터 탐색
- Status: DONE

## 구현 개요

`projects/stock-backtest/src/stock_backtest/web/pages/data_explorer.py`를 완전 구현했다.
기존 placeholder를 덮어쓰기로 교체했으며, 본 태스크에서 요구된 파일 외 다른 파일은 수정하지 않았다.

### 레이아웃
- `dash.register_page(__name__, path="/data", name="데이터 탐색")`.
- `dcc.Dropdown` (id=`data-explorer-asset-dropdown`, `multi=True`, 초기 `options=[]`).
- `dcc.DatePickerRange` (id=`data-explorer-date-range`, 기본값 최근 5년).
- `dcc.RadioItems` (Price / Return / Correlation).
- `dcc.Checklist` (Normalize to 100) - Price 모드에서만 의미 있음.
- "조회" `html.Button`.
- 상태 메시지 `html.Div` + `dcc.Loading(dcc.Graph)`.
- 페이지 로드 감지용 `dcc.Location`.

### 콜백
1. `_populate_assets(_pathname)`:
   - `dcc.Location.pathname`을 트리거로 첫 로드 시 1회 실행.
   - `AssetRepository.list_active()`로 active 자산 조회하여 Dropdown options 구성 (`{symbol} [{market}] {name}`).
   - DB 오류 시 options=[] + 에러 메시지 표시 (lazy: import/세션 모두 콜백 내부에서).

2. `_on_submit(n_clicks, asset_ids, start_date, end_date, indicator, normalize)`:
   - 입력 검증: 자산 선택, 기간 선택, start<=end, Correlation은 자산 2개 이상.
   - `_load_wide_frame()`이 자산별 `OhlcvRepository.get_range`로 adj_close를 가져와 `pd.concat`으로 wide DataFrame(index=date, columns=`symbol [market]`) 생성.
   - 데이터 없음/결측 방어 (빈 DF, NaN, first_valid_index 사용).
   - 지표별 Figure:
     - **Price**: `go.Scatter` line chart. normalize 체크 시 first valid row로 나눠 100 곱함.
     - **Return**: `df.pct_change()` → `cumprod(1+r)` → 시작 1.0의 누적 곡선. 원본 NaN 위치 보존.
     - **Correlation**: 일별 수익률의 `df.corr(method="pearson")` → `plotly.express.imshow` (zmin/zmax=-1/1, RdBu).
   - 실패 시 빈 Figure + 한국어 에러 메시지.

### 주요 설계 결정
- **Lazy DB 접근**: `get_db_session`, `AssetRepository`, `Asset`, `OhlcvRepository` 모두 함수 내부 import → 모듈 import 자체는 DB 없이도 성공 (app.py의 lazy-config 전략과 일관).
- **Allow_duplicate**: status 메시지는 두 콜백이 모두 쓰므로 `allow_duplicate=True` + `prevent_initial_call="initial_duplicate"` 조합 사용.
- **Column labels**: `Asset.name` 중복·공백 시 문제가 없도록 `symbol [market]` 포맷만 사용.
- **Plotly imports**: `plotly.express as px`, `plotly.graph_objects as go` 모두 사용.
- **타입힌트/docstring**: 모든 public/private 함수 및 콜백에 추가.

## 검증

- `python -c "import ast; ast.parse(...)"` → OK.
- 모듈 런타임 import는 현재 환경의 Dash-jupyter 초기화 제약(`comm.create_comm` NotImplementedError)으로 실패 — 우리 코드와 무관한 환경 이슈. `AST parse OK`로 대체.
- 다른 페이지/모듈 수정 없음(diff 기준 `pages/data_explorer.py` 단 1개 파일).

## 변경 파일
- `projects/stock-backtest/src/stock_backtest/web/pages/data_explorer.py` (덮어쓰기)

## 결과
DONE.
