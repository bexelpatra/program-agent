---
agent: coder
task_id: TASK-015
status: DONE
timestamp: 2026-04-14T11:00:00
---

## 결과 요약
Strategy 추상 베이스(+ pydantic `StrategyParams`)와 파일 자동 스캔 방식의 전략 레지스트리를 구현했다. `list_strategies()`는 전략이 없을 때 빈 리스트를 반환하고, `discover_strategies()`는 `static/`, `dynamic/` 하위 모듈을 재귀 import한다. 중복 이름 등록 시 `ValueError`, 동일 클래스 재등록은 멱등.

## 변경된 파일
- projects/stock-backtest/src/stock_backtest/strategies/base.py (신규)
- projects/stock-backtest/src/stock_backtest/strategies/registry.py (신규)
- projects/stock-backtest/src/stock_backtest/strategies/__init__.py (수정: 공개 API export)
- projects/stock-backtest/src/stock_backtest/strategies/static/__init__.py (수정: docstring)
- projects/stock-backtest/src/stock_backtest/strategies/dynamic/__init__.py (수정: docstring)

## 주요 API
- `Strategy(ABC)`: class attrs `name: str`, `params_schema: type[StrategyParams]`, `description: str = ""`. `__init__(params)`에서 params_schema 타입 검증. abstract: `generate_weights(prices, rebalance_dates) -> pd.DataFrame`, `required_universe() -> list[str] | None`.
- `StrategyParams(BaseModel)`: `extra="forbid"`, `validate_assignment=True`.
- `register(cls)` 데코레이터 + 전역 `STRATEGY_REGISTRY: dict[str, type[Strategy]]`.
- `discover_strategies(package="stock_backtest.strategies")`: `pkgutil.walk_packages`로 하위 모듈 재귀 import, `base`/`registry` 자신은 스킵.
- `get_strategy(name)`, `list_strategies()`.

## 검증
`PYTHONPATH=src python -c ...`로 수동 smoke 테스트:
- import OK
- 빈 레지스트리에서 `list_strategies() == []`
- `discover_strategies()` 호출 정상 (static/, dynamic/ 서브패키지 import)
- `get_strategy('missing')` → KeyError (available 목록 포함)
- `@register` 정상 등록, 중복 이름 시 ValueError, 동일 클래스 재등록은 멱등

## 이슈/블로커
없음.

## 다음 제안
- TASK-016 이후 `strategies/static/fixed_weight.py`, `strategies/static/permanent.py` 등 실제 전략 구현 태스크에서 `@register` + `params_schema`를 사용해 등록하면 된다.
- Tester에게 `tests/test_strategies_registry.py`로 register/duplicate/discover/get/list 단위 테스트 작성을 의뢰할 것.
