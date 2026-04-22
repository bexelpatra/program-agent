# Coder Report - TASK-017

## 상태
DONE

## 작업 내용

### 신규 파일
- `projects/stock-backtest/src/stock_backtest/metrics/performance.py`
- `projects/stock-backtest/tests/test_performance.py`

### 공개 API
`performance.py`에 다음 함수 구현:
- `cagr(equity) -> float`
- `annualized_volatility(returns, periods_per_year=252) -> float`
- `sharpe_ratio(returns, risk_free_annual=0.0, periods_per_year=252) -> float`
- `sortino_ratio(returns, risk_free_annual=0.0, periods_per_year=252) -> float`
- `max_drawdown(equity) -> float` (음수 반환)
- `calmar_ratio(equity) -> float` (cagr / |mdd|, MDD=0 시 inf 처리)
- `turnover(trades, equity) -> float` (연환산)
- `win_rate(trades_or_returns) -> float`
- `compute_all(equity, trades=None, risk_free_annual=0.0, trading_days_per_year=252) -> dict[str, float]`
- 보조: `to_returns(equity)`

### 설계 결정
- 내부 계산은 모두 `float` (pandas/numpy). `Decimal` 입력은 `_as_float_series`에서 `float(...)`로 coerce.
- CAGR 연수 산출: `DatetimeIndex`면 실제 달력 일수 / 365.25, 아니면 `len(eq)/252` fallback.
- 종가가 음수/0이면 CAGR은 -1.0 (terminal ruin) 반환.
- Sharpe/Sortino에서 std=0 + mean=0이면 0.0, std=0 + mean>0이면 +inf, mean<0이면 -inf.
- Sortino의 downside deviation은 음수 excess returns의 RMS를 사용.
- Turnover는 `sum(|qty*price|) / mean_equity / years` (연환산).
- `win_rate`는 Series/숫자 iterable → 양수 비율. TradeRecord처럼 PnL이 없는 객체는 0.0.
- `compute_all`은 equity 유효 샘플<2일 때 zero-bundle 반환 (caller crash 방지).

## 테스트 결과
```
21 passed in 0.44s
```

### 커버한 케이스
- Known value: 10% 직선 상승 252일 → CAGR ≈ 예상값, MDD=0, Sharpe 매우 큼, Calmar=+inf.
- 합성 시계열 (seed=42, n=1000, drift=0.0005, vol=0.012): MDD 음수/>-1, Sharpe 합리적 범위, Sortino 유한·양수, annualised vol 수동 계산 일치.
- Edge case: 빈 equity, 1-sample, 음수 최종값, Decimal 입력, known MDD (100→120→60→90 = -0.5), NaN 중간 삽입 시 returns 클린.
- Win rate: returns 양수 비율, 빈 입력.
- Turnover: 빈 trades/None, TradeRecord 기반 수식 검증.
- Sharpe/Sortino 특수값: zero variance, no downside → inf 처리.

## 파일 경로
- 구현: `projects/stock-backtest/src/stock_backtest/metrics/performance.py`
- 테스트: `projects/stock-backtest/tests/test_performance.py`

## 이슈/블로커
없음.
