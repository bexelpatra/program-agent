---
agent: coder
task_id: TASK-048
status: DONE
timestamp: 2026-04-14T00:00:00
---

## 결과 요약

FixedWeight 전략의 `weights: dict[str, float]` 필드를 JSON Textarea 대신 **자산 Dropdown + 비중 Input 페어의 동적 리스트** 위젯으로 렌더하도록 구현했다.

- 위젯 렌더러 `_render_asset_weight_map` + 행 빌더 `_build_weight_row` 추가
- Pattern-matching 콜백 2개 등록:
  - `_mutate_weight_rows`: `+ 자산 추가` / `✕` 삭제 버튼을 MATCH 로 묶어 한 콜백에서 처리 (n_clicks>0 가드 포함). 새 인덱스는 기존 row index 의 max+1 로 부여해 재배열 없이 pattern matching 으로 식별.
  - `_update_weight_sum`: `weight-map-weight` ALL 값 합계를 `합계: X / 1.0000` 포맷으로 표시하고 1.0 근사/미달/초과에 따라 녹색/주황/빨강 색상 지정.
- `_WIDGET_RENDERERS` 레지스트리에 `"asset_weight_map"` 등록.
- `_coerce_field_value` 의 dict 분기 맨 앞에 `isinstance(raw, dict) → return raw` 통과 분기 추가 (위젯이 조립한 dict 가 JSON 파서에 들어가지 않도록).
- `_run_backtest` / `_run_backtest_impl` 에 `weight-map-symbol`, `weight-map-weight` 의 id/value State(ALL,ALL) 4개를 추가해, 각 필드명별로 `{symbol: weight}` dict 를 `defaultdict(dict)` 로 조립한 뒤 `_widget_name(finfo) == "asset_weight_map"` 인 필드에 한해 `params[fname]` 를 덮어쓴다 (다른 필드 흐름은 기존대로 유지).
- `FixedWeightParams.weights` Field 에 `json_schema_extra={"widget": "asset_weight_map"}` 를 추가. RiskParity 등 다른 전략에는 `dict[str, float]` 필드가 없어 skip.
- 기본값(예: 60/40)이 dict 로 들어오면 초기 행들이 해당 심볼/비중으로 미리 채워진다. 빈 기본값이면 빈 행 1개로 시작.
- 합계 검증은 UI 경고색만 수행하고, 실제 실행 차단은 기존 `FixedWeightParams._validate_weights_sum` pydantic validator 가 담당.

## 변경된 파일

- `projects/stock-backtest/src/stock_backtest/web/pages/backtest.py` (수정)
  - import: `MATCH`, `collections.defaultdict` 추가
  - 함수 추가: `_build_weight_row`, `_render_asset_weight_map`
  - 레지스트리: `_WIDGET_RENDERERS["asset_weight_map"]` 추가
  - 콜백 추가: `_mutate_weight_rows`, `_update_weight_sum`
  - `_coerce_field_value`: dict 분기에 `isinstance(raw, dict)` 통과 분기 추가
  - `_run_backtest` / `_run_backtest_impl`: weight-map State(ALL) 4개 + 조립 로직 추가
- `projects/stock-backtest/src/stock_backtest/strategies/static/fixed_weight.py` (수정)
  - `FixedWeightParams.weights` Field 에 `json_schema_extra={"widget": "asset_weight_map"}` 추가

## 스모크

- `python -m py_compile backtest.py fixed_weight.py` → OK
- dash app 인스턴스화 후 `asset_weight_map in backtest._WIDGET_RENDERERS` → `True`
- `FixedWeightParams.model_fields['weights'].json_schema_extra` → `{'widget': 'asset_weight_map'}`

## 이슈/블로커

없음. 다만 Dash pattern-matching 콜백 특성상 `weight-map` 컨테이너를 가진 form 이 화면에 없는 시점(다른 전략 선택 중)에도 `_run_backtest` 의 State(ALL,ALL) 는 빈 리스트로 안전하게 동작함을 확인했다.

## 다음 제안

- TASK-049(또는 후속) 에서 합계 ≠ 1.0 일 때 실행 버튼을 disable 하는 UX 를 추가하면 pydantic validator 에러 메시지보다 더 친절함.
- 앱 기동 후 실제 브라우저에서 행 추가/삭제/합계 실시간 갱신 / FixedWeight 실행 end-to-end 확인은 Manager 가 수행.
