---
agent: coder
task_id: TASK-040
status: DONE
timestamp: 2026-04-29T09:35:00
---

## 결과 요약

architecture.md V3 § "현금/FX 모델" L559-600 + § "백엔드 모듈 분할" L654-666 + Q1~Q8 사용자 결정에 따라 `backend/app/domain/portfolio.py` 를 작성했다. B 모델(자산 native 보유 + cash_by_ccy 통화별 분리), Q3-C 단계 분리 환전 + Q5-B native 우선, 20bp fx_spread, FX trade 미기록(FxConversion 별도 감사 레코드), long-only + 1주 정수 + partial fill 모두 구현. domain 순수성 확보(Decimal/dataclass/typing 만 import — sqlalchemy/fastapi/yfinance/pykrx/pandas/app.* 0건). 7개 핵심 시나리오 + 3개 보너스 케이스 모두 자동 검증 통과.

## 변경된 파일

- `projects/stock-backtest/backend/app/domain/portfolio.py` (신규, 약 290줄)
- `projects/stock-backtest/backend/app/domain/__init__.py` (수정 — Portfolio/Position/FxConversion/InsufficientFundsError/DEFAULT_FX_SPREAD_BPS/DEFAULT_SLIPPAGE_BPS re-export 추가)

### 추가된 public API (Portfolio 클래스)

```python
@dataclass(frozen=True)
class Position:
    asset_id: int; currency: str; qty: int; avg_price: Decimal
    def market_value(self, current_price: Decimal) -> Decimal

@dataclass(frozen=True)
class FxConversion:
    from_ccy, to_ccy, from_amount, to_amount, fx_rate, spread_cost  # all Decimal/str

class InsufficientFundsError(Exception):
    currency: str; requested: Decimal; available: Decimal

@dataclass
class Portfolio:
    base_currency: str
    cash_by_ccy: dict[str, Decimal]
    positions: dict[int, Position]
    fx_spread_bps: Decimal = 20

    cash(currency) -> Decimal
    total_cash_in_base(fx_rates: Mapping[str, Decimal]) -> Decimal
    positions_value_in_base(prices, fx_rates) -> Decimal
    equity_in_base(prices, fx_rates) -> Decimal
    convert(from_ccy, to_ccy, amount, fx_rate) -> FxConversion
    ensure_native_funds(target_ccy, required, fx_rates_to_target) -> list[FxConversion]
    buy(asset_id, currency, price, qty_target, commission_bps, slippage_bps=10) -> tuple[int, Decimal]
    sell(asset_id, price, qty, commission_bps, slippage_bps=10) -> tuple[int, Decimal]
    deposit(currency, amount) -> None
```

## DoD 검증 결과

| # | 검증 | 명령 | 결과 |
|---|------|------|------|
| 1 | import smoke | `python -c "from app.domain.portfolio import Portfolio, Position, FxConversion, InsufficientFundsError; print('ok')"` | `ok` |
| 2 | domain 순수성 (banned imports 0건) | ast 분석 — sqlalchemy/fastapi/yfinance/pykrx/pandas/app.models/app.data/app.api 검색 | `domain pure`, imports = `['dataclasses', 'decimal', 'typing']` |
| 3 | 단위 동작 7+3 케이스 | `/tmp/verify_portfolio_task040.py` | 10/10 PASS |
| 4 | float() 호출 0건 (Decimal 정밀도) | `grep -n "float(" backend/app/domain/portfolio.py` | `no float() calls` |
| 5 | re-export 동작 | `python -c "from app.domain import Portfolio, ...; print('re-export ok')"` | `re-export ok` |

## 단위 동작 검증 7개 시나리오

| # | 시나리오 | 입력 | 기대 | 실측 | 판정 |
|---|----------|------|------|------|------|
| 1 | **B 모델** — cash_by_ccy 통화별 분리 입금 | deposit("KRW", 10M); deposit("USD", 0) | KRW=10M, USD=0, USD 키 미생성 | KRW=10000000, USD=0, keys=['KRW'] | PASS |
| 2 | **환전 단방향 (20bp spread)** | KRW 1,300,000 → USD @ rate=1/1300 | USD ≈ 998.0, base spread ≈ 2600 KRW | USD=998.0000, spread_cost=2600.000 KRW | PASS |
| 3 | **Q3-C 양방향 환전** — KR sell → ensure_native USD → US buy 시나리오 | KODEX 100주 @ 12000 KRW 매도 + ensure 510 USD | sell 후 KRW 입금 → USD 환전 1회 → USD ≥ 510 | KRW 입금 1,198,620.18, USD 잔고 510.00, 환전 1건, spread 1328.66 KRW | PASS |
| 4 | **Q5-B same currency 우선** — SPY 매도 USD 입금 → QQQ USD 매수 | sell SPY → ensure_native_funds("USD", 400) | 환전 0회 (native 충분) | USD 잔고 49,947.50, 환전 0건 | PASS |
| 5 | **partial fill** — cash 부족 시 0주 체결 | cash 100 USD, SPY 500 USD 1주 매수 | actual_qty=0, exception 미발생 | actual_qty=0, cost=0, USD 잔고 100 유지 | PASS |
| 6 | **long-only** — 미보유 자산 sell | positions 없는 asset 99 매도 5주 | actual_qty=0, 음수 잔고 방지 | actual_qty=0, received=0, USD 1000 유지, positions[99] 부재 | PASS |
| 7 | **FX trade 미기록** — convert/ensure_native_funds 가 trade 객체 미반환 | conv = convert(...); convs = ensure_native_funds(...) | FxConversion 만 반환, side/asset_id 필드 없음 | hasattr(conv,'side')=False, hasattr(conv,'asset_id')=False | PASS |

### 보너스 검증

| # | 시나리오 | 결과 |
|---|----------|------|
| B1 | equity_in_base 멀티 통화 합산 (KRW cash + USD cash + KRW pos + USD pos) | 3,125,000 KRW (계산값과 정확 일치) |
| B2 | convert(KRW, KRW, ...) same-currency no-op | 잔고 변화 0, spread 0 |
| B3 | InsufficientFundsError on direct convert (cash 100, request 500) | 정상 raise (currency/requested/available 필드 보존) |

## 클린 코드 점검

- 도메인 순수: import 3종 (`dataclasses`, `decimal`, `typing`) 만. 외부 의존 0건 — ast 검증으로 구조적 보장.
- 단일 책임: Portfolio 는 잔고 + 포지션 + 환전만, FxConversion 은 감사 레코드만 (frozen).
- buy/sell 은 한 가지 일 (slippage·commission·cash·position 한 트랜잭션). 평균가 갱신은 `_upsert_position` 사적 헬퍼로 추출.
- partial fill 은 InsufficientFundsError 가 아닌 (qty=0 반환) — 호출자(trade engine)가 비중 미달 결과로 받음. convert/ensure_native_funds 만 정확 출금이 필요해 raise.
- 환전 양방향 비용은 호출자가 두 번 호출 (1 호출 = 1 spread). FX rate 는 외부에서 주입 (도메인 순수 유지).
- 음수 잔고 방지는 buy 의 `max_affordable = int(available / cost_per_unit)` 로 구조적 보장 + sell 은 `min(qty, pos.qty)` 로 보장.
- magic number 는 모두 named constant (`ZERO`, `ONE`, `DEFAULT_FX_SPREAD_BPS`, `DEFAULT_SLIPPAGE_BPS`, `BPS_DIVISOR`).
- 주석은 Why 만 (예: "정밀도는 ohlcv Numeric(20,8) 과 정합 위해 Decimal", "Q5 B — native 우선", "spread 차감 후 정확히 deficit 채워지도록 역산").

## 이슈/블로커

없음. TASK-021 (pykrx 어댑터) 와 병렬 실행 안전성 확인 — `app/data/sources/`, `app/domain/asset/`, `app/models/`, `app/api/` 어떤 파일도 건드리지 않았다.

### 사소한 결정 (보고용)

1. **`_spread_in_base` 헬퍼 분리**: convert() 본문 가독성 위해 spread 환산 로직만 사적 메서드로 분리. base 가 from/to 어느 쪽도 아닌 직접 환전 (예: USD↔EUR, base=KRW) 은 MVP 외 케이스이므로 ZERO 반환 (audit 정확도는 떨어지지만 실제 잔고는 정확). architecture.md L582 가 "base_currency 경유" 만 정의하므로 MVP 범위 내.

2. **`ensure_native_funds` base 자체 부족 시 빈 리스트**: target == base_currency 인 경우 환전으로 메울 수 없으므로 빈 리스트 반환 (예외 X). 호출자 (trade engine TASK-041) 가 partial fill 결정. 동일 시그니처로 base/non-base 구분 없이 다룰 수 있어 호출자 코드 단순.

3. **Decimal precision**: getcontext() 변경 없이 디폴트(28 prec) 사용. ohlcv Numeric(20,8) 과 정합. 검증 스크립트에서도 동일.

## 다음 제안

- **TASK-041 (`trade.py`) 가 이 모듈을 직접 import** 한다. `from app.domain.portfolio import Portfolio, FxConversion, InsufficientFundsError, DEFAULT_SLIPPAGE_BPS`. 시장별 commission_bps 매핑 (KR=1.5, US=0.5, Crypto=10 bps) 은 trade.py 또는 `core/defaults.yaml` 로딩 모듈 책임 — Portfolio 는 매개변수로만 받는다 (도메인 순수 유지).
- **TASK-042 (`calendar.py`)** 는 Portfolio 와 직접 의존 없음. 두 모듈은 TASK-043 engine.py 에서 합쳐진다.
- **TASK-080 골든 스냅샷** 작성 시 본 검증 7개 시나리오를 pytest 케이스로 옮길 후보. 특히 (3) Q3-C 양방향 spread 비용은 정확한 수치(1328.66 KRW per 환전)로 회귀 가드 가능.
- 향후 환율 데이터 (TASK-044 또는 별도) 로딩 시 fx_rates dict 의 timestamp 정합 (체결일 종가) 은 호출자가 보장. Portfolio 는 dict 만 받음 — 시점 검증 책임 분리.
- `Position` 이 frozen 이므로 sell 시 매번 새 Position 생성. 대량 reblance 에서도 dict 기반이므로 O(1) — 성능 이슈 없음.
