---
agent: coder
task_id: TASK-041
status: DONE
timestamp: 2026-04-28T23:36:20
---

## 결과 요약

`backend/app/domain/trade.py` 신규 작성 — V3 § "거래 정책" L604-642 + § "백엔드 모듈 분할" L654-666 의 거래 실행 엔진. 시장별 디폴트 수수료 매핑(KR 1.5bps / US 0.5bps / CRYPTO 10bps), 비거래일·가격누락 엔진 레이어 방어(silent 0 금지), `execute_rebalance` 리밸런싱 트랜잭션(SELL→BUY, native 우선 Q5 B + 부족 시 base 환전 Q3 C)을 구현. `Portfolio` 인터페이스만 사용하고 `__init__.py` re-export 추가.

## 변경된 파일

- projects/stock-backtest/backend/app/domain/trade.py (신규, 345 lines)
- projects/stock-backtest/backend/app/domain/__init__.py (수정 — trade 심볼 re-export 추가)

## 신규 public API

도메인 레이어 (`app.domain.trade`):

| 심볼 | 종류 | 시그니처 |
|------|------|----------|
| `DEFAULT_COMMISSION_BPS` | 상수 dict | `dict[str, Decimal]` — KR/US/CRYPTO 디폴트 |
| `DEFAULT_SLIPPAGE_BPS_DEFAULT` | 상수 | `Decimal("10")` (Portfolio 동명 상수 alias) |
| `NonTradingDayError` | Exception | 비거래일 silent 0 방지 |
| `MissingPriceError` | Exception | universe 가격 누락 silent 0 방지 |
| `TradeOrder` | frozen dataclass | `(asset_id, market, currency, side, qty_target, price)` |
| `TradeFill` | frozen dataclass | `(asset_id, side, qty_filled, price, commission, currency)` |
| `commission_bps_for(market, override=None) -> Decimal` | 함수 | 시장별 수수료 bps (defaults.yaml override 우선) |
| `assert_all_assets_priced(target_assets, prices, rebalance_date) -> None` | 함수 | 가격 누락 검증 (raise) |
| `assert_trading_day_for_universe(target_assets, rebalance_date, is_trading_day_fn) -> None` | 함수 | 거래일 검증 (raise) |
| `execute_rebalance(portfolio, target_weights, asset_meta, prices, fx_rates_to_base, rebalance_date, commission_override=None, slippage_bps=DEFAULT, is_trading_day_fn=is_trading_day) -> list[TradeFill]` | 함수 | 리밸런싱 1회 트랜잭션 |

`app.domain` re-export 에 위 9개 모두 추가 (engine 레이어가 `from app.domain import execute_rebalance` 로 사용 가능).

## DoD 검증 결과

| # | 항목 | 결과 |
|---|------|------|
| 1 | import 스모크 (`from app.domain.trade import ...`) | PASS — `ok` |
| 2 | 도메인 순수성 (banned import 없음) | PASS — imports = `[__future__, dataclasses, datetime, decimal, typing, app.domain.asset.calendar_guard, app.domain.portfolio]`. SQLAlchemy/FastAPI/yfinance/pykrx/pandas/app.models/app.data/app.api 0건 |
| 3 | `commission_bps_for('KR'/'US'/'CRYPTO')` | PASS — `1.5 0.5 10`. UNKNOWN → `0`, override 적용 시 `2` |
| 4 | `NonTradingDayError` raise | PASS — `assert_trading_day_for_universe([(1, 'US')], date(2024,1,1), lambda m,d: False)` → `NonTradingDayError("rebalance_date 2024-01-01 is not a trading day for 1 markets: [(1, 'US')]")` |
| 5 | `MissingPriceError` raise | PASS — `assert_all_assets_priced([(1, 'US'), (2, 'US')], {1: Decimal('100')}, date(2024,1,2))` → `MissingPriceError("missing prices for 1 assets on 2024-01-02: [(2, 'US')]")` |

추가 통합 미니 시나리오 (KR 단일 자산 100% 매수, base=KRW, 자본 1,000,000 KRW, 가격 10,000):

```
fills: [TradeFill(asset_id=1, side='BUY', qty_filled=99, price=10000,
                  commission=148.6485, currency='KRW')]
cash: {'KRW': 8861.3515}, positions: {1: Position(qty=99, avg_price=10010.000)}
```

수치 검증:
- effective price = 10,000 × 1.001 (slippage) = 10,010
- max affordable = floor(1,000,000 / (10,010 × 1.00015)) = floor(99.836...) = 99
- gross = 99 × 10,010 = 990,990
- commission = 990,990 × 0.00015 = 148.6485 (정확 일치)
- 잔여 cash = 1,000,000 − 991,138.6485 = 8,861.3515 (정확 일치)

## 클린 코드 점검

- 도메인 순수: `app.domain.portfolio` + `app.domain.asset.calendar_guard` 만 import (asset 정책상 calendar_guard 의 exchange_calendars 는 도메인 본질로 허용됨)
- `TradeOrder`/`TradeFill` frozen dataclass (불변값)
- `execute_rebalance` 단일 책임 (리밸런싱 1회). 내부적으로 헬퍼 4개로 분리:
  - `_native_value_from_base` (base→native 환산)
  - `_classify_orders` (target_qty 비교 → SELL/BUY 분류)
  - `_execute_sells` (매도 시퀀스)
  - `_execute_buys` (매수 시퀀스 — native 우선 + 부족 시 환전)
- `is_trading_day_fn` 의존성 주입 (테스트 mock 가능, 디폴트는 `calendar_guard.is_trading_day`)
- partial fill 표현: `TradeFill.qty_filled < TradeOrder.qty_target` 으로 호출자가 식별. 0주 체결은 fills 미포함 (빈 리스트가 아닌 누락)
- 책임 분리 명확: Portfolio (잔고/매매 메커니즘) ↔ Trade (시장별 매핑/시퀀스/엔진 방어)
- Magic number: `BPS_DIVISOR = 10000`, `ZERO`, `ONE` named constant
- 함수 길이: `execute_rebalance` 본문 약 35줄, 헬퍼 분리로 40줄 가이드 준수

## 이슈/블로커

없음. 모든 DoD 통과.

다만 **책임 경계** 관련 작은 관찰사항 (observation, 후속 태스크 필요 없음):

1. 매도 시 `prices` 에서 가격 누락이면 `Position.avg_price` 로 fallback 하도록 했음. 이는 청산 전용 시나리오(예: delisting 이전 마지막 잔량 처리)에서 BUY 단계 전에 누락 검증을 통과한 자산은 해당 없음 — 현재 흐름은 항상 `assert_all_assets_priced` 가 BUY+SELL 모두 검증 후이므로 fallback 분기는 사실상 도달 불가. 방어적 코드로 남김.

2. `Portfolio.buy` 의 `currency` 인자가 `asset_meta` 의 currency 와 일치한다고 가정함. asset_meta 구성 시점(TASK-043 strategy 또는 engine 레이어)에서 `Asset.currency` 와 동기 보장 필요.

3. `commission_override` 를 `Mapping[str, Decimal]` 로 받지만 defaults.yaml 로더(추후 태스크)가 어떤 형식으로 변환할지는 미정. 현 시그니처는 시장별 dict 형식만 가정.

## 다음 제안

1. **TASK-043 strategy.py + engine.py** — Strategy 인터페이스(allocator + filters AND + rebalance_schedule) 와 백테스트 메인 루프. `execute_rebalance` 를 일자별로 호출하는 형태. `is_trading_day_fn` 디폴트를 그대로 쓰되 테스트는 mock 주입.

2. **단위 테스트** (Tester 전용 영역) — 권장 케이스:
   - `commission_bps_for` 의 override / 미지정 시장 → 0 fallback
   - `assert_trading_day_for_universe` 의 multi-market mixed 거래일 (KR 휴장 + US 거래일 같은 날짜)
   - `execute_rebalance` 의 partial fill (자본 부족 시 정수 주 절삭 검증, 위 미니 시나리오 99주가 그 예)
   - `execute_rebalance` 의 SELL→BUY 순서 보장 (native 입금이 BUY 에 활용되는지: KR 자산 50% → 100% 시 SELL 없음, 100% → KR 0% + US 100% 시 SELL 후 환전 후 BUY)
   - `execute_rebalance` 의 base→native 환전 트리거 (USD 100% 매수, base=KRW, USD 0)

3. **defaults.yaml 로더** (별도 태스크) — `commission_override` / `slippage_bps` 를 yaml 에서 읽어 `execute_rebalance` 호출자(engine)에 주입하는 어댑터. `app/core/config.py` 에 둘 가능성.

4. **architecture.md "Domain Public API" 섹션 갱신** (Manager 작업) — TASK-040~042 누적 + 본 태스크의 trade 모듈 9개 심볼을 누적 기록.
