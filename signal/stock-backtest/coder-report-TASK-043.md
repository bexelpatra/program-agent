---
agent: coder
task_id: TASK-043
status: DONE
timestamp: 2026-04-14
---

# TASK-043: SimpleMovingAverage 전략 구현

## 결과 요약
단일 이동평균선과 가격의 비교로 risky/safe 를 스위칭하는 `SimpleMovingAverage` 동적 전략을 새 파일로 추가하고 registry 에 등록했다. `crossover.py` 의 설계 패턴(look-ahead 방지 `.shift(1)`, rebalance 시점별 `get_indexer(..., method="pad")` 조회, 워밍업 구간 safe fallback)을 그대로 따랐다.

## 변경 파일
- 신규: `projects/stock-backtest/src/stock_backtest/strategies/dynamic/moving_average/simple.py`
  - `SimpleMovingAverageParams(StrategyParams)`: `risky_symbol`, `safe_symbol` (둘 다 `json_schema_extra={"widget": "asset_symbol"}`), `window: int = 200` (gt=0). `model_validator` 로 risky != safe 검증.
  - `SimpleMovingAverage(Strategy)`: `name = "simple_moving_average"`, `params_schema`, 한 문장 description, `required_universe()` → `[risky_symbol, safe_symbol]`, `generate_weights()` 구현. `@register` 데코레이터로 등록.
  - 핵심 로직: `price = prices[risky].astype(float)` → `ma = rolling_mean(price, window)` → `raw = (price > ma).astype(int)` (ma NaN 구간 0 처리) → `signal = raw.shift(1).fillna(0).astype(int)` → rebalance 일자마다 `get_indexer([date], method="pad")` 로 최근 신호 조회 후 risky/safe 100% 할당.

## Smoke 검증
- `PYTHONPATH=src python -c "from stock_backtest.strategies.dynamic.moving_average.simple import SimpleMovingAverage; print(SimpleMovingAverage.name, SimpleMovingAverage.params_schema.model_fields['risky_symbol'].json_schema_extra)"`
  → `simple_moving_average {'widget': 'asset_symbol'}` OK.
- `discover_strategies()` 후 `list_strategies()` 결과에 `simple_moving_average` 포함 확인 (registry 의 함수명은 `discover_strategies`).

## 이슈/블로커
없음. (참고: registry 모듈의 discover 함수 이름은 `discover_strategies` 이며, 태스크 설명의 "registry discover" 는 이를 지칭하는 것으로 해석함.)
