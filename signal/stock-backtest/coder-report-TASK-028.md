# Coder Report - TASK-028

## 태스크
- Task ID: TASK-028
- Title: 웹 페이지 (c) 전략 백테스트
- 대상 파일: `projects/stock-backtest/src/stock_backtest/web/pages/backtest.py` (덮어쓰기)

## 결과
- Status: DONE
- 구현 파일: `projects/stock-backtest/src/stock_backtest/web/pages/backtest.py`

## 구현 내용

### 페이지 등록
- `dash.register_page(__name__, path="/backtest", name="백테스트")`.

### 레이아웃 (`_layout`, `layout = _layout` - 함수형 layout 으로 매 요청마다 전략 레지스트리를 다시 조회)
1. **전략 Dropdown** (`bt-strategy`): `discover_strategies() + list_strategies()` 로 옵션 생성.
2. **전략 파라미터 폼** (`bt-strategy-params`): 전략 선택 콜백 `_update_strategy_form` 이 `params_schema.model_fields` 를 순회하며 타입별로 컴포넌트 동적 생성.
   - `bool` → `dcc.Checklist`
   - `int` → `dcc.Input(type=number, step=1)`
   - `float` → `dcc.Input(type=number, step=any)`
   - `Literal[...]` → `dcc.Dropdown`
   - `list[...]` → `dcc.Textarea` (콤마/줄바꿈 분리)
   - `dict[str, float]` → `dcc.Textarea` (JSON; FixedWeight weights 등)
   - `str` / 기타 → `dcc.Input(type=text)` (fallback)
   - 각 필드는 pattern-matching id `{"type": "strategy-param", "name": <field>}` 사용.
3. **Universe Textarea** (`bt-universe`): `SPY, AGG` 또는 `SPY@US` 로 market 지정 가능.
4. **기간** (`bt-date-range`): `dcc.DatePickerRange` (디폴트 최근 5년).
5. **Base currency Dropdown** (`bt-base-ccy`): USD / KRW.
6. **Market mode Dropdown** (`bt-market-mode`): STOCK / CRYPTO / MIXED.
7. **Initial capital Input** (`bt-initial-capital`).
8. **실행 버튼** (`bt-run`).
9. 결과 영역: `bt-status` (run 메타), `dcc.Loading` 로 감싼 `bt-results`.

### 콜백
- `_update_strategy_form(strategy_name)`: 전략 선택 시 파라미터 폼 재생성.
- `_run_backtest(n_clicks, strategy, param_ids(ALL), param_values(ALL), universe, start, end, base_ccy, market_mode, initial_capital)`:
  - 모든 파라미터는 `State` 로 받아 "실행" 버튼 클릭 시에만 트리거 (`prevent_initial_call=True`).
  - 에러는 배너 형태로 표시 (traceback 포함).

### 실행 파이프라인 (`_run_backtest_impl`)
1. UI 값 → `_coerce_field_value` 로 타입 변환 → `schema_cls(**params)` 로 pydantic 검증 → `model_dump()` 로 정규화.
2. Universe Textarea 가 비어있으면 `strategy.required_universe()` 로 보충 (FixedWeight/Momentum 등).
3. `compute_run_hash(strategy_name, params, symbols, (start, end), base_ccy)` 계산.
4. `get_db_session()` 컨텍스트에서:
   - `_resolve_universe(session, symbols)` 로 `AssetSpec` 리스트 구성 (assets 테이블 조회, `_asset_class_for` 로 tax class 결정).
   - `find_cached_run(session, run_hash)` 조회.
     - 캐시 히트 & `is_stale()` 이 False → `load_run` 으로 equity/trades/metrics 복원 (cache reuse 표시).
     - 그 외 → `BacktestEngine(settings, session_factory).run(config, strategy)` 실행, `compute_code_commit_hash`, `compute_data_hash` 계산 후 `save_run` 으로 저장 + `session.commit()`.
5. 결과 표시:
   - `_render_status`: run_id, run_hash, code_commit_hash, data_hash, 캐시 재사용 / STALE 여부, trade count.
   - `_render_results`:
     - Plotly line chart: equity curve (base_ccy 라벨 포함).
     - Plotly area line chart: drawdown (cummax 기반 재계산).
     - `dash_table.DataTable`: `compute_all` 지표 (cagr/vol/sharpe/sortino/mdd/calmar/turnover/win_rate). `_format_metric` 으로 비율 지표는 %로 표시.
6. DB/캐시/엔진 실패 시 `RuntimeError` 로 래핑 → 콜백 최상단에서 traceback 표시.

### 기타
- Plotly `plotly.graph_objects` 임포트 사용.
- 모든 공개 함수에 docstring.
- 타입힌트 (`pd.Series`, `dict[str, float]` 등) 적용.
- 세션은 `from stock_backtest.web.db_session import get_db_session` 로만 접근.

## 검증
- `python -c "import stock_backtest.web.pages.backtest"` → 현재 환경의 Dash 의 `_jupyter` 모듈이 `comm.create_comm` NotImplementedError 를 던져 실패. Dash 자체 import 단계에서 발생한 환경 버그로, backtest 페이지 코드와는 무관.
- `python -c "import ast; ast.parse(open(...).read())"` → OK (구문 오류 없음). 태스크 설명에 명시된 "dash comm 버그 시 ast.parse 대체 가능" 조건으로 수행.

## 파일 변경
- Modified: `projects/stock-backtest/src/stock_backtest/web/pages/backtest.py` (placeholder → 본 구현)
- 새 파일: 없음 (`web/components/` 추가 파일 불필요)
