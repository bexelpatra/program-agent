# Coder Report — TASK-022

## Task
- Task ID: TASK-022
- Title: VAA (Vigilant Asset Allocation), Risk Parity
- Status: DONE

## 작업 요약

### 1) VAA (`src/stock_backtest/strategies/dynamic/vaa.py`)
- `VAAParams(StrategyParams)` 구현:
  - `offensive_assets` (기본 `['SPY','EFA','EEM','AGG']`)
  - `defensive_assets` (기본 `['LQD','IEF','SHY']`)
  - `top_n_offensive: int = 1` (G4 Aggressive)
  - `breadth_threshold: int = 1`
- `VAA(Strategy)` (`name='vaa'`, `@register`):
  - Momentum score = `12*r1 + 4*r3 + 2*r6 + r12`, 월 단위는 21 거래일 근사.
  - Offensive 중 score>0 자산 수 ≥ breadth_threshold → offensive 상위 `top_n_offensive` 동일비중.
  - 미충족 → defensive 중 score 최고 자산 100%.
  - 12개월(≈252 거래일) lookback 부족 → 전체 0.
  - `required_universe()` = offensive + defensive.

### 2) Risk Parity (`src/stock_backtest/strategies/dynamic/risk_parity.py`)
- `RiskParityParams(StrategyParams)`:
  - `universe: list[str]`, `lookback_days: int = 60`, `min_weight: float = 0.0`.
- `RiskParity(Strategy)` (`name='risk_parity'`, `@register`):
  - 각 리밸런스일에 lookback 일별 수익률 std 계산 (ddof=0).
  - 비중 = (1/std) / sum(1/std), std=0/NaN 자산 제외 후 유효 자산끼리 재배분.
  - `min_weight > 0` 이면 유효 자산 floor 적용 후 재정규화.
  - lookback 부족 또는 유효 자산 없음 → equal weight fallback.
  - `required_universe()` = params.universe.

### 3) 테스트 (`tests/test_vaa_riskparity.py`)
- VAA: 4 케이스 (전부 상승 공격 모드, 전부 하락 방어 모드, 부분 breadth, lookback 부족).
- RiskParity: 4 케이스 (저변동 가중 우세, 동일 변동성, std=0 제외, lookback 부족 equal fallback).

## 테스트 결과

```
$ python -m pytest tests/test_vaa_riskparity.py -v
============================= test session starts ==============================
platform linux -- Python 3.11.3, pytest-9.0.2, pluggy-1.6.0
collected 8 items

tests/test_vaa_riskparity.py::test_vaa_all_offensive_up_picks_top_offensive PASSED [ 12%]
tests/test_vaa_riskparity.py::test_vaa_all_offensive_down_picks_defensive PASSED [ 25%]
tests/test_vaa_riskparity.py::test_vaa_partial_breadth_meets_threshold_goes_offensive PASSED [ 37%]
tests/test_vaa_riskparity.py::test_vaa_insufficient_lookback_returns_zero PASSED [ 50%]
tests/test_vaa_riskparity.py::test_risk_parity_low_vol_gets_higher_weight PASSED [ 62%]
tests/test_vaa_riskparity.py::test_risk_parity_equal_vol_equal_weight PASSED [ 75%]
tests/test_vaa_riskparity.py::test_risk_parity_zero_std_excluded PASSED  [ 87%]
tests/test_vaa_riskparity.py::test_risk_parity_insufficient_lookback_equal_weight PASSED [100%]

============================== 8 passed in 0.30s ===============================
```

## 생성된 파일
- `projects/stock-backtest/src/stock_backtest/strategies/dynamic/vaa.py`
- `projects/stock-backtest/src/stock_backtest/strategies/dynamic/risk_parity.py`
- `projects/stock-backtest/tests/test_vaa_riskparity.py`

## 이슈/블로커
없음.
