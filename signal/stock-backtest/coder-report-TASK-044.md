---
agent: coder
task_id: TASK-044
status: DONE
timestamp: 2026-04-29T00:00:00
---

## 결과 요약

`backend/app/domain/dividend.py` 와 `backend/app/domain/metrics.py` 두 모듈을 도메인 순수로 신규 작성. 배당은 자산 보유분에 대해 native currency 로 cash_by_ccy 에 입금하고 audit 용 DividendCredit 을 반환한다 (V3 § 배당 처리 L640-642 + CLAUDE.md L21). 메트릭은 `(date, equity)` 시계열에서 CAGR / MDD / Sharpe / Sortino / Calmar / 승률 / 연·월 수익률 7개 지표를 1회 호출로 계산한다 (Quant Lab CLAUDE.md L24).

`backend/app/domain/__init__.py` 끝에 신규 7개 public symbol 을 append (기존 라인 미수정).

## 변경된 파일

- `projects/stock-backtest/backend/app/domain/dividend.py` (신규, 76줄)
- `projects/stock-backtest/backend/app/domain/metrics.py` (신규, 138줄)
- `projects/stock-backtest/backend/app/domain/__init__.py` (수정 — dividend/metrics re-export 끝에 append)

## 신규 public API

### dividend.py

| Symbol | Signature | 용도 |
|---|---|---|
| `DividendPayment` | `@dataclass(frozen=True)`: asset_id, pay_date, amount_per_share | 배당 이벤트 1건 (native currency, 1주당) |
| `DividendCredit` | `@dataclass(frozen=True)`: asset_id, pay_date, qty_eligible, amount_per_share, total_amount, currency | 입금 결과 (감사 로깅용) |
| `apply_dividend(portfolio, payment) -> DividendCredit \| None` | 단일 배당 처리; 미보유/0amount 면 None | 단발 호출 |
| `apply_dividends_for_date(portfolio, payments, target_date) -> list[DividendCredit]` | target_date 매칭 일괄 처리 | engine EOD 후크 |

### metrics.py

| Symbol | Signature | 용도 |
|---|---|---|
| `TRADING_DAYS_PER_YEAR` | `int = 252` | 연환산 상수 |
| `MetricsResult` | `@dataclass(frozen=True)`: cagr, mdd, sharpe, sortino, calmar, win_rate, annual_returns, monthly_returns | 결과 컨테이너 |
| `compute_metrics(equity_series: list[tuple[date, Decimal]]) -> MetricsResult` | 7개 지표 1회 계산 | 백테스트 종료 시 1회 호출 |

내부 헬퍼 (`_daily_returns`, `_max_drawdown`, `_cagr`, `_annualized`, `_annualized_return`, `_periodic_returns`) 은 `_` prefix 로 모듈 내부에 한정.

## DoD 결과

### 1. import (PASS)

```
$ cd backend && python -c "from app.domain.dividend import DividendPayment, DividendCredit, apply_dividend, apply_dividends_for_date; from app.domain.metrics import MetricsResult, compute_metrics, TRADING_DAYS_PER_YEAR; print('ok')"
ok
```

### 2. 도메인 순수성 (PASS)

dividend.py imports: `dataclasses`, `datetime`, `decimal`, `app.domain.portfolio` (도메인 내부)
metrics.py imports: `math`, `collections.defaultdict`, `collections.abc.{Callable,Hashable}`, `dataclasses`, `datetime`, `decimal`

banned (`sqlalchemy|fastapi|pandas|yfinance|pykrx|app.data|app.models|app.api`) grep → exit=1 (0건).

### 3. apply_dividend 동작 (PASS)

- 단일: 10주 × $0.5 → cash 100→105, credit.total=5.0
- edge cases: 미보유 자산 → None, amount=0 → None
- `apply_dividends_for_date`: 3개 payments 중 target_date 매칭 2건만 처리, cash 0→10 ($5+$5)

### 4. compute_metrics 동작 (PASS)

선형 상승 시리즈 (366일, 100→110):
```
CAGR=0.100, MDD=0.000, Sharpe=577.975, Sortino=0.000, Calmar=0.000, win_rate=1.000
annual={2024: 0.0996}, monthly count=12
```

낙폭 시리즈 (`100,110,90,95,100`): `MDD=-0.182` (110→90 = -18.18%, 검증식 통과).

빈 시리즈/단일 포인트: 모두 0 반환 (zero-division 방어).

2년치 시리즈: `annual_keys=[2023,2024], monthly_count=24` (groupby 정상).

### 5. 통합 import (PASS)

```
$ python -c "from app.domain import DividendPayment, ..., compute_metrics, TRADING_DAYS_PER_YEAR"
package-level import ok
TRADING_DAYS_PER_YEAR = 252
```

## 클린 코드 점검

- 두 파일 모두 도메인 순수 (banned 0건).
- 모든 public dataclass `frozen=True` (불변성).
- metrics 의 함수 분리 — `_daily_returns`, `_max_drawdown`, `_cagr`, `_annualized`, `_annualized_return`, `_periodic_returns` (단일 책임).
- `TRADING_DAYS_PER_YEAR` 상수화 (매직넘버 제거).
- zero-division 방어 — 빈 시리즈, prev=0, vol=0, mdd=0 (calmar) 모두 0.0 fallback.
- 타입힌트 전부 명시 (Callable/Hashable for group_key).

## 병렬 안전성 확인

- 본 태스크 산출물 (`dividend.py`, `metrics.py`) 신규 생성 — 충돌 없음.
- `__init__.py` 수정: TASK-031/043 의 strategy/engine re-export 가 먼저 들어와 있는 것을 확인 후, 그 이후에 dividend/metrics 만 append (기존 라인 미수정).

## 다음 제안

- **TASK-062 (백테스트 엔진 메인 루프)**: 종료 시 `compute_metrics(result.equity_series)` 를 호출하고 결과를 `backtest_metrics` 테이블에 INSERT (cagr/mdd/sharpe/sortino/calmar/win_rate 컬럼 + JSONB annual_returns/monthly_returns).
- **TASK-EOD 후크 (engine 일일 루프)**: 매 거래일 EOD 시점에 `apply_dividends_for_date(portfolio, payments_for_window, today)` 호출. payments 는 data 레이어가 corporate_actions 테이블에서 backtest 시작 시 1회 lookup 후 list 로 전달.
- **DividendCredit 영속화**: 호출자가 audit 목적으로 `corporate_actions_applied` 테이블에 INSERT (선택적, MVP 이후).
- **단위 테스트**: `backend/tests/domain/test_dividend.py` + `test_metrics.py` 신규 추가 (Tester 태스크). 위 검증 시나리오 + AllWeather 골든 테스트 (Quant Lab 테스트 규칙).
