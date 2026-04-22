# Coder Report - TASK-031

## 태스크
- Task ID: TASK-031
- Title: 웹 페이지 (d) 백테스트 이력 비교
- 상태: DONE

## 변경 파일
- `projects/stock-backtest/src/stock_backtest/web/pages/history.py` (placeholder → 완전 구현, 덮어쓰기)

## 구현 요약

### 페이지 등록
- `dash.register_page(__name__, path="/history", name="이력 비교")`.

### 레이아웃
- 상단 툴바:
  - `Refresh` 버튼 (`history-refresh-btn`).
  - 전략 필터 `dcc.Dropdown` (`history-strategy-filter`, 전체 run 에서 strategy_name 유니크 추출).
  - `dcc.DatePickerSingle` 2개 — 기간 시작 이후 / 기간 끝 이전 필터.
- Run 목록 `dash_table.DataTable` (`history-run-table`):
  - 컬럼: run_id, strategy_name, period_start, period_end, base_currency, market_mode, created_at, STALE.
  - `row_selectable="multi"`, 페이지당 20행, 정렬·필터 활성화.
  - STALE 행은 `style_data_conditional` 로 빨간 배경+굵은 글씨 강조.
- 하단:
  - `dcc.Graph` (`history-equity-graph`) — equity curve 겹쳐 그리기.
  - `Div` (`history-metrics-container`) — metrics pivot DataTable 렌더 컨테이너.

### 데이터 접근
- `_fetch_recent_runs(limit=100)`:
  - `session.scalars(select(BacktestRun).order_by(BacktestRun.created_at.desc()).limit(100))` 직접 쿼리 (repository 에 list_runs 가 없음).
  - 각 run 에 대해 `is_stale(run, session)` 계산 (예외 시 STALE 로 간주).
  - DB 예외는 로깅만 하고 빈 리스트 반환 → 페이지 임포트/렌더 보호.
- `_build_equity_figure(run_ids)`:
  - 각 run_id 에 `load_run(session, rid)` 으로 equity 로드.
  - 동일 `go.Figure` 에 `Scatter` 를 추가 (label = `f"{strategy_name}#{run_id}"`).
  - 빈 선택 시 "선택된 run 없음" 타이틀 반환.
- `_build_metrics_pivot(run_ids)`:
  - 각 run 의 metrics dict 를 모아 (metric_name × run_id) pivot.
  - 컬럼은 `metric` + `run_{rid}` (헤더는 `strategy_name#run_id`).
  - 값은 `f"{v:.6g}"` 포맷.

### 콜백
1. `_refresh_runs` — 페이지 로드/Refresh/필터 변경 시:
   - `_fetch_recent_runs` → `_apply_filters(strategy, start, end)` 적용.
   - 전략 드롭다운 옵션 갱신.
   - 기존 선택된 run_id 를 새 데이터에서 인덱스로 재매핑해 유지.
2. `_on_selection_change` — row 선택 변경 시:
   - 선택된 run_id 들로 equity Figure + metrics DataTable 생성.
   - 선택 0개면 안내 메시지, metrics 없음이면 "성과지표 없음" 메시지.

### 타입 / docstring
- 모듈/함수/상수 전반에 docstring 및 타입 힌트.
- Plotly `graph_objects` 사용.

## 검증
- `python -c "import ast; ast.parse(open(...))"` → `OK` (문법 통과).
- DB/모델 import 경로 기존 코드(backtest.py, run_store.py) 와 동일 패턴.

## 금지 사항 준수
- task-board.md, architecture.md 미수정.
- seasonality.py, tests/, 그 외 src/ 미수정 — `web/pages/history.py` 만 덮어쓰기.

## 비고
- `BacktestRun.run_id` 는 ORM int 이므로 JSON 직렬화 위해 `int()` 로 캐스팅.
- `is_stale` 호출 시 예외는 UI 를 중단시키지 않도록 STALE=True 로 fail-closed 처리.
- DatePicker 의 `date` prop 은 `YYYY-MM-DD` 문자열이라 `period_start`/`period_end` ISO 문자열과 직접 문자열 비교로 필터링 가능.
