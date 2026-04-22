---
task_id: TASK-047
agent: coder
status: DONE
severity: none
---

# TASK-047 Report: asset_symbol_list 위젯 + 기존 list[str] universe 전환

## 변경 요약

### 1. `web/pages/backtest.py`
- DB 옵션 로딩 로직을 `_load_asset_options()` 헬퍼로 추출해 단일/다중 렌더러가 공유.
- 새 렌더러 `_render_asset_symbol_list` 추가: `dcc.Dropdown(multi=True, searchable=True)` 사용. 라벨 `"{name} · {symbol} [{market}]"`, value 는 심볼 문자열 리스트.
  - default 가 list/tuple 이면 그대로 사용, 아니면 `[]`.
  - default 에 포함된 심볼이 옵션 목록에 없으면 prepend.
  - DB 로딩 실패 시 warning 후 옵션 비움.
- `_WIDGET_RENDERERS` 에 `"asset_symbol_list": _render_asset_symbol_list` 등록.
- `_coerce_field_value` 의 `list / List` 분기를 보강:
  - `raw in (None, "", [])` → `[]`
  - `isinstance(raw, list)` → Dropdown(multi) 반환값으로 간주, split 건너뛰고 타입별 캐스팅 후 반환.
  - 그 외(문자열) → 기존 콤마/줄바꿈 split 유지.
  - `list[int]`, `list[float]` 캐스팅 유지.

### 2. 전략 파라미터 메타데이터 주입 (`json_schema_extra={"widget": "asset_symbol_list"}`)
- `strategies/dynamic/momentum.py` — `MomentumParams.universe` (DualMomentum 도 동일 params 클래스 공유)
- `strategies/dynamic/dual_momentum.py` — `DualMomentumParams.risky_assets`
- `strategies/dynamic/risk_parity.py` — `RiskParityParams.universe`
- `strategies/dynamic/vaa.py` — `VAAParams.offensive_assets`, `VAAParams.defensive_assets`

### 처리 제외 (대상 아님)
- `moving_average/seasonal.py` 의 `election_dates: list[str] | None` → 자산 심볼이 아니라 ISO 날짜 문자열 리스트.
- `moving_average/seasonal.py` 의 `custom_months: list[int] | None`, `multi_crossover.py` 의 `windows: list[int]` → list[int].
- `static/fixed_weight.py` 의 `weights: dict[str, float]` → TASK-048 처리 예정 (지시문대로 dict이므로 제외).
- `static/permanent.py` → list[str] 자산 필드 없음 (자산은 코드 내 상수).

## Smoke

- `python -m py_compile` (수정한 5개 파일) → OK
- Dash app 컨텍스트에서:
  - `'asset_symbol_list' in backtest._WIDGET_RENDERERS` → True
  - 5개 필드 모두 `model_fields[...].json_schema_extra == {'widget': 'asset_symbol_list'}` 확인.
  - `_coerce_field_value` 동작 확인:
    - `(list[str], ['SPY','BIL'])` → `['SPY','BIL']`
    - `(list[str], None)` → `[]`
    - `(list[str], [])` → `[]`
    - `(list[str], 'SPY, BIL')` → `['SPY','BIL']` (Textarea 호환)
    - `(list[int], ['1','2','3'])` → `[1,2,3]`
    - `(list[int], [1,2,3])` → `[1,2,3]`

## 이슈/블로커

없음.

## 후속

- TASK-048: `fixed_weight.weights: dict[str, float]` 용 weight 편집 위젯이 backtest.py 에 추가될 예정. 본 태스크와 backtest.py 를 공유하므로 순차 진행.
