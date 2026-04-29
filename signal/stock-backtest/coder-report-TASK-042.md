---
agent: coder
task_id: TASK-042
status: DONE
timestamp: 2026-04-29T00:00:00
---

## 결과 요약

`backend/app/domain/calendar.py` 신규 작성. 멀티 마켓 백테스트의 시간축을 base_currency 시장 캘린더 (KRW→XKRX, USD→XNYS) 로 고정하고, 비base 시장 자산은 forward-fill 로 base 캘린더 행에 가격을 정렬하는 도메인 순수 모듈이다 (architecture.md V3 § "멀티 마켓 캘린더" L549-555 + Q14).

`backend/app/domain/__init__.py` 에 신규 6개 public symbol 을 re-export.

## 변경된 파일

- `projects/stock-backtest/backend/app/domain/calendar.py` (신규, 105줄)
- `projects/stock-backtest/backend/app/domain/__init__.py` (수정 — calendar re-export 추가)

## 신규 public API

| Symbol | Signature | 용도 |
|---|---|---|
| `BASE_CCY_TO_CALENDAR` | `dict[str, str]` (KRW→XKRX, USD→XNYS) | 통화→시장 매핑 상수 |
| `base_calendar_name(base_currency: str) -> str` | KRW/USD 만 지원, 그 외 ValueError | 미지원 통화 조기 검증 |
| `trading_days_in_period(base_currency, start: date, end: date) -> list[date]` | base 캘린더 거래일 목록 | engine.py 메인 루프 시간축 |
| `align_market_price_to_base_calendar(market, base_currency, base_date, market_prices) -> Decimal \| None` | forward-fill (back-fill 금지) | 단일 자산 가격 정렬 |
| `align_universe_prices(universe_market_meta, universe_market_prices, base_currency, base_date) -> dict[int, Decimal]` | 누락 자산은 결과 dict 에서 제외 | universe 전체 정렬 |
| `next_trading_day(base_currency, target: date) -> date` | target 이 거래일이면 그 다음, 비거래일이면 그 이후 가장 가까운 거래일 | 모델 A D+1 시가 체결일 산출 |
| `previous_trading_day(base_currency, target: date) -> date` | 대칭 | rebalance_schedule 보조 |

### Repository 변경
없음 (도메인 모듈만 추가).

## DoD 검증 결과

| # | 검증 | 명령 | 결과 |
|---|---|---|---|
| 1 | import 6개 + 상수 | `python -c "from app.domain.calendar import ...; print('ok')"` | `ok` |
| 2 | 도메인 순수성 | `grep ^import\|^from calendar.py` | stdlib (datetime/decimal/typing) + exchange_calendars 만 — PASS |
| 3 | base_calendar_name KRW/USD | `print(base_calendar_name('KRW'), base_calendar_name('USD'))` | `XKRX XNYS` |
| 4 | base_calendar_name JPY | `base_calendar_name('JPY')` | `ValueError: unsupported base_currency: JPY (supported: ['KRW', 'USD'])` |
| 5 | trading_days_in_period KR Jan 2024 | `len(trading_days_in_period('KRW', date(2024,1,1), date(2024,1,31)))` | `22` (spec 가이드 ~20개와 일치) |
| 6 | align_market_price forward-fill | exact / 1/8 ffill / 1/11 ffill / 1/3 none | `100 / 100 / 110 / None` — 모두 일치 |
| 7 | next_trading_day KRW 2024-01-01 | `print(next_trading_day('KRW', date(2024,1,1)))` | `2024-01-02` |

추가 sanity:
- `next_trading_day('KRW', 2024-01-02)` (거래일) → `2024-01-03` (다음 거래일, D+1 모델 A 의도와 일치)
- `previous_trading_day('USD', 2024-01-15)` (MLK 휴일) → `2024-01-12`
- `previous_trading_day('KRW', 2024-01-02)` (거래일) → `2023-12-28`
- `align_universe_prices` 3개 자산 mix (KR/US/CRYPTO): full hit / partial (US 데이터 없음 → 결과 dict 에서 제외) 모두 정확

`from app.domain import base_calendar_name, align_market_price_to_base_calendar, trading_days_in_period, next_trading_day` re-export 도 동작 확인.

## 설계 결정 메모

1. **`next_trading_day` / `previous_trading_day` 의 비거래일 input 처리**: `exchange_calendars.next_session()` 은 인자가 거래일이어야만 동작 (비거래일이면 `NotSessionError`). DoD 7 의 `next_trading_day('KRW', 2024-01-01)` (한국 신정, 비거래일) 케이스를 만족시키기 위해 `target ± 1day` 로 probe 한 뒤 `date_to_session(direction='next'|'previous')` 를 호출하는 패턴으로 구현. 이로써:
   - target 이 거래일 → 다음/직전 거래일 (D+1 모델 A 의 "다음 거래일" 의미와 일치)
   - target 이 비거래일 → 그 이후/이전 가장 가까운 거래일
   둘 다 자연스럽게 처리.

2. **`align_universe_prices` 의 누락 자산**: spec 의 "누락 자산은 None" 표현을 "결과 dict 에서 제외" 로 해석. `dict[int, Decimal]` 시그니처에 None 을 끼워 넣으면 호출자가 `is None` 체크를 매번 해야 하고, `Decimal | None` 으로 타입을 풀면 다운스트림 산술이 모두 None-방어가 필요. 호출자는 `set(meta.keys()) - set(out.keys())` 로 누락 자산을 식별 가능하므로 정보 손실 없음. spec 본문 "호출자가 None 자산은 NonTradingDayError 또는 MissingPriceError 처리" 의도는 동일하게 유지.

3. **CRYPTO 처리**: 현재 구현은 시장 분기를 하지 않고 `market_prices` 의 키만 본다. 24/7 CRYPTO 도 forward-fill 로직이 자연스럽게 동작 (base 캘린더 거래일에 데이터가 있으면 그대로, 없으면 forward-fill). spec L549-555 의 "암호화폐는 base 캘린더 D 일의 UTC 00:00 종가" 도 데이터 적재 시점에 UTC 00:00 종가가 base_date 키로 들어와 있으면 자동 충족. 향후 CRYPTO 만의 특수 처리 (예: timezone shift) 가 필요하면 `market` 인자 분기 추가.

4. **forward-fill 만 구현, back-fill 금지**: spec 명시. 미래 가격 사용은 look-ahead bias.

## 클린 코드 점검

- 도메인 순수: stdlib + exchange_calendars (architecture.md 가 도메인 본질로 허용한 외부 패키지) — PASS
- 함수 분리: 단일 자산 (`align_market_price_to_base_calendar`) vs universe 전체 (`align_universe_prices`) 명확히 분리 — PASS
- 함수 길이: 모든 함수 ≤ 25줄 — PASS
- 매개변수 5개 미만: 가장 많은 `align_universe_prices` 가 4개 — PASS
- BASE_CCY_TO_CALENDAR 확장 가능 (JPY/EUR 미래 추가는 dict 한 줄) — PASS
- 주석은 Why (정책·근거·외부 라이브러리 제약) 만 — PASS

## 이슈/블로커

없음.

병렬 안전성 확인: `__init__.py` 가 TASK-041 (trade.py) 에 의해 trade 관련 import/export 추가가 들어와 있음을 확인. 내가 추가한 calendar re-export 와 충돌 없음 (서로 다른 섹션).

## 다음 제안

- **TASK-043 (engine.py 메인 루프)**: `trading_days_in_period(base_currency, start, end)` 로 시간축 dates 를 만들고, 매 거래일 d 에 대해:
  1. `align_universe_prices(universe_market_meta, universe_market_prices, base_currency, d)` 로 가격 dict 산출
  2. signal_filters 평가 (당일 종가 기준)
  3. allocator 로 target weight 산출
  4. 체결일은 `next_trading_day(base_currency, d)` (모델 A D+1 시가)
  5. 체결 시점의 universe 가격은 `align_universe_prices(...next_trading_day...)` 로 다시 산출 (시가 기반이지만 일별 데이터에서는 보통 종가만 있어 호출자가 OHLC 어느 컬럼을 쓸지 결정)

- **TASK-044+ (테스트)**: `tests/domain/test_calendar.py` 에 골든 케이스 — KR/US 캘린더 cross-check (한국 추석 vs 미국 정상영업일 등 비대칭 휴일에서 forward-fill 정확성), CRYPTO 24/7 자산이 base=KRW 캘린더에 정렬됐을 때 한국 휴일 행이 사라지는지 확인 (V3 § L549-555 의도대로 base 캘린더 외 행은 시간축에 없음).

- **JPY/EUR 확장**: BASE_CCY_TO_CALENDAR 에 추가만 하면 되지만, `Asset.market` enum 도 동기화 필요. 후속 universe 확장 태스크에서.
