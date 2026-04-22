# Coder Report - TASK-020

## 태스크
- Task ID: TASK-020
- Title: 정적 전략 구현 (FixedWeight 일반화 + Permanent Portfolio)
- Status: DONE

## 작업 내용

### 신규 파일
1. `projects/stock-backtest/src/stock_backtest/strategies/static/fixed_weight.py`
   - `FixedWeightParams(StrategyParams)`: `weights: dict[str, float]`, `rebalance: bool = True`.
   - pydantic `model_validator(mode="after")`로 합=1 검증 (tolerance `1e-6`), 빈 dict/비문자열 키/NaN 값 거부.
   - `FixedWeight(Strategy)`: `name="fixed_weight"`.
     - `generate_weights(prices, rebalance_dates)`: `weights`에 없는 심볼이 prices.columns에 없으면 `KeyError`. 반환 DataFrame은 index=리밸런스일, columns=params 선언 순서, 모든 행 동일 비중.
     - `required_universe()` → `list(self.params.weights.keys())`.
   - `@register` 적용. docstring에 60/40 · All Weather 예시 포함.
2. `projects/stock-backtest/src/stock_backtest/strategies/static/permanent.py`
   - `PermanentPortfolioParams`: `equity_symbol="SPY"`, `bond_symbol="TLT"`, `gold_symbol="GLD"`, `cash_symbol="BIL"`.
   - `PermanentPortfolio(Strategy)`: `name="permanent"`, 4자산 25/25/25/25.
   - `required_universe` → `[equity, bond, gold, cash]` 순서.
   - 슬롯 심볼이 `prices.columns`에 없으면 `KeyError`.
   - `@register` 적용.
3. `projects/stock-backtest/tests/test_static_strategies.py` — 9개 테스트.

### 설계 결정 준수
- 설계 결정 #8: 60/40, All Weather 전용 클래스를 만들지 않고 `FixedWeight` 파라미터로 표현. docstring에 두 가지 예시 가중치 포함.
- `base.py`, `registry.py`는 수정하지 않음 (읽기 전용 준수).
- `metrics/`, `tests/test_ingestion*` 미접근.

## 테스트 결과

```
$ python -m pytest tests/test_static_strategies.py -v
...
tests/test_static_strategies.py::test_fixed_weight_60_40_shape_and_values PASSED
tests/test_static_strategies.py::test_fixed_weight_sum_not_one_raises PASSED
tests/test_static_strategies.py::test_fixed_weight_empty_weights_raises PASSED
tests/test_static_strategies.py::test_fixed_weight_missing_symbol_in_universe_raises PASSED
tests/test_static_strategies.py::test_fixed_weight_required_universe_preserves_order PASSED
tests/test_static_strategies.py::test_permanent_portfolio_25_each PASSED
tests/test_static_strategies.py::test_permanent_portfolio_required_universe_order PASSED
tests/test_static_strategies.py::test_permanent_portfolio_missing_symbol_raises PASSED
tests/test_static_strategies.py::test_discover_strategies_registers_static PASSED

============================== 9 passed in 0.28s ===============================
```

## 이슈/메모
- 개발 환경 pandas 버전이 `"ME"` 주기 별칭을 지원하지 않아 테스트에서 `"M"` + 월말 시작일(`2020-01-31`)로 리밸런스 일자를 구성했다. 구현 코드 자체는 pandas 버전 의존성이 없다 (호출자가 넘긴 DatetimeIndex를 그대로 사용).
- `FixedWeight.generate_weights`는 `weights` dict의 선언 순서를 DataFrame 컬럼 순서로 유지한다 (Python 3.7+ dict 순서 보장).

## 완료 조건 체크
- [x] `fixed_weight.py`, `permanent.py`, `test_static_strategies.py` 신규 작성
- [x] pytest 9/9 통과
- [x] `discover_strategies()` 후 `list_strategies()`에 `"fixed_weight"`, `"permanent"` 등록 확인
- [x] 타입힌트 · docstring 완비
- [x] `base.py`, `registry.py` 미수정
