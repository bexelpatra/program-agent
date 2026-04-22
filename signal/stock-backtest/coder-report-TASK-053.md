---
agent: coder
task_id: TASK-053
status: DONE
timestamp: 2026-04-14T00:00:00
---

## 결과 요약

세 개의 MA 기반 동적 전략(`MovingAverageCrossover`, `SimpleMovingAverage`, `MultiMovingAverageCrossover`)을 새 DSL(`target_symbol` + `exit_action` + `rotate_symbol`)로 완전 교체했다. 기존 `risky_symbol`/`safe_symbol` 파라미터는 세 전략에서 모두 제거됨. `_CASH_` 1급 현금 처리와 호환되며 엔진(TASK-051)의 `CASH_SYMBOL` 을 재사용한다. 병행 운영 없음.

## 변경된 파일
- `projects/stock-backtest/src/stock_backtest/strategies/dynamic/moving_average/crossover.py` (새 DSL 로 교체)
- `projects/stock-backtest/src/stock_backtest/strategies/dynamic/moving_average/simple.py` (새 DSL 로 교체)
- `projects/stock-backtest/src/stock_backtest/strategies/dynamic/moving_average/multi_crossover.py` (새 DSL 로 교체)

## Public API 변경 — 전략 파라미터 스키마

### 공통 (세 전략)
제거된 필드:
- `risky_symbol: str`
- `safe_symbol: str`

신규 필드:
- `target_symbol: str` (widget=asset_symbol)
- `exit_action: Literal["cash", "rotate"] = "cash"`
- `rotate_symbol: str | None = None` (widget=asset_symbol; `exit_action="rotate"` 일 때 필수)

validator:
- `exit_action == "rotate"` → `rotate_symbol` 필수 + `rotate_symbol != target_symbol`
- `exit_action == "cash"` → `rotate_symbol` 은 None 허용(무시)

### 전략별 추가 필드 (기존 유지)
- `MovingAverageCrossoverParams`: `fast_window`, `slow_window` (fast < slow validator 유지)
- `SimpleMovingAverageParams`: `window`
- `MultiMovingAverageCrossoverParams`: `windows: list[int]`, `include_price: bool = True` (기존 validator 유지)

### `generate_weights` 반환 DataFrame
- cash 모드: 컬럼 `[target_symbol, "_CASH_"]`
- rotate 모드: 컬럼 `[target_symbol, rotate_symbol]`
- 신호 ON → `target_symbol` 1.0, 신호 OFF → exit 컬럼 1.0
- 워밍업 구간 / 가격 이전 시점 → exit 컬럼 1.0 (`_CASH_` fallback, safe 100% 와 동등 의미)

### `required_universe`
- cash 모드: `[target_symbol]` (엔진 prices 로드 대상에서 `_CASH_` 제외)
- rotate 모드: `[target_symbol, rotate_symbol]`

### `@register` name (변경 없음)
- `moving_average_crossover`
- `simple_moving_average`
- `multi_moving_average_crossover`

## 엔진 연동 규약
- `CASH_SYMBOL = "_CASH_"` 을 `stock_backtest.backtest.engine` 에서 import.
- 엔진(TASK-051 적용 완료)은 `generate_weights` 반환에서 `_CASH_` 컬럼을 prices 조회 전에 drop 하여 현금 비중으로 자연스럽게 흡수.
- 전략 내부에서 prices DataFrame 에 `_CASH_` 컬럼을 참조하지 않음 (cash 모드일 때 prices 존재 검사 대상에서 제외).
- look-ahead 방지(`.shift(1)`), crossover_signal/rolling_mean 로직은 기존 그대로 유지.

## Smoke 검증 결과
모두 통과:
1. 세 파일 `py_compile` OK.
2. `MovingAverageCrossoverParams(target_symbol='SPY', fast_window=50, slow_window=200)` → `exit_action='cash', rotate_symbol=None`.
3. `MovingAverageCrossoverParams(target_symbol='SPY', exit_action='rotate', rotate_symbol='TLT', fast_window=50, slow_window=200)` → 정상.
4. `MovingAverageCrossoverParams(target_symbol='SPY', exit_action='rotate', fast_window=50, slow_window=200)` → `ValidationError` (rotate_symbol 필수).
5. `exit_action='rotate'` 인데 `rotate_symbol == target_symbol` → `ValidationError`.
6. 합성 10일치 시계열로 세 전략 모두 `generate_weights` 호출, cash 모드 컬럼 `['SPY', '_CASH_']`, rotate 모드 컬럼 `['SPY', 'TLT']` 확인.
7. `required_universe()`: cash → `['SPY']`, rotate → `['SPY', 'TLT']`.
8. Simple/Multi 에서도 `exit_action='rotate'` 인데 `rotate_symbol` 없음 → `ValidationError` 동일하게 발생.

## 이슈/블로커

### 범위 밖 — 같은 DSL 에 의존하는 외부 참조
아래 파일들도 `risky_symbol`/`safe_symbol` 을 사용하지만 **이번 태스크 범위 밖**이라 건드리지 않았다. 후속 태스크 필요.

- `src/stock_backtest/strategies/dynamic/moving_average/seasonal.py`
  - 자체 `SeasonalMovingAverageParams` 가 `risky_symbol`/`safe_symbol` 을 정의하고 사용. 독립 전략이므로 이번 교체로 import 체인은 깨지지 않음. 하지만 DSL 일관성을 위해 동일하게 마이그레이션 권장(별도 태스크 제안).
- `src/stock_backtest/web/pages/backtest.py`
  - MA 전략 폼에서 `risky_symbol`/`safe_symbol` 레이블이나 디폴트 자동 주입 로직을 참조할 가능성. 실행 시 `KeyError`/폼 렌더 이슈가 생길 수 있음. 새 DSL (`target_symbol`/`exit_action`/`rotate_symbol`) 기준으로 업데이트 필요 (별도 태스크).

### 깨질 가능성이 있는 기존 단위테스트
`projects/stock-backtest/tests/` 에서 `risky_symbol`/`safe_symbol` 직접 참조는 `grep` 결과 **없음**. 세 전략 클래스를 직접 import 하는 테스트도 발견되지 않음 (`MovingAverageCrossover`/`SimpleMovingAverage`/`MultiMovingAverageCrossover` 모두 매칭 0건). 단, registry 기반 전체 로딩(예: `test_strategy_integration.py`)이 `seasonal.py`/`web` 모듈을 간접 import 하면서 기존 DSL 을 기대할 수 있으므로 Tester(TASK-055) 가 full test run 에서 확인 권장.

tests/ 파일은 본 태스크에서 수정 금지 규정에 따라 손대지 않음.

## 다음 제안
1. `seasonal.py` 를 같은 DSL 로 마이그레이션 (별도 coder 태스크).
2. `web/pages/backtest.py` 가 새 전략 파라미터 스키마에 맞게 폼/디폴트를 렌더하도록 갱신 (별도 coder 태스크).
3. Tester(TASK-055) 에서 registry 기반 통합 테스트 실행 및 새 DSL 기반 단위테스트 추가.
