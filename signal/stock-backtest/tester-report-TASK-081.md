---
agent: tester
task_id: TASK-081
status: DONE
timestamp: 2026-04-29T18:00:00
---

## 결과 요약

look-ahead 회귀 + 비거래일 방어 4단계 + cash_by_ccy 환전 단위 회귀 테스트 3개 파일을
신규 작성·실행했다. 모든 회귀 케이스 (50/50) 통과 — 모델 A 구조적 차단 + 비거래일
다층 방어 + Q3 C/Q5 B 환전 정책이 현 구현에서 모두 정상 동작함을 확인.

검증 대상:
- `app/domain/engine.py` L209 `prices_until_d = ctx.prices_aligned.loc[:d]` (모델 A)
- `app/data/sources/yfinance_source.py` `_is_invalid_close` (수집 022)
- `app/data/pipeline.py` `_trading_days` + L188 2차 필터 (캘린더 022)
- `app/domain/asset/calendar_guard.py` `guard_trading_day` (조회 030)
- `app/domain/trade.py` `assert_trading_day_for_universe` + `assert_all_assets_priced` (엔진 041, 043)
- `app/domain/portfolio.py` `convert` / `ensure_native_funds` / `buy` / `sell` (환전 040)
- `app/domain/trade.py` `execute_rebalance` (단계 분리 + native 우선 통합 041)

## 변경된 파일

- `projects/stock-backtest/backend/tests/regression/__init__.py` (신규)
- `projects/stock-backtest/backend/tests/regression/test_lookahead.py` (신규, 8 테스트)
- `projects/stock-backtest/backend/tests/regression/test_calendar_defense.py` (신규, 23 테스트)
- `projects/stock-backtest/backend/tests/regression/test_cash_by_ccy.py` (신규, 19 테스트)

## 테스트 결과

### A. Look-ahead 회귀 (`test_lookahead.py`) — 8/8 통과

| 케이스 | 검증 내용 |
|--------|-----------|
| `test_fixed_weight_no_lookahead` | FixedWeight 가격 무관 → prices_until_d 길이 변화에 비중 결과 동일 |
| `test_equal_weight_no_lookahead` | EqualWeight 가격 무관 (1/N) |
| `test_all_weather_no_lookahead` | AllWeather 가격 무관 (카테고리 비중 분배) |
| `test_moving_average_deterministic_on_same_prefix` | 동일 prefix 에서 결정적 |
| `test_momentum_deterministic_on_same_prefix` | 동일 prefix 에서 결정적 |
| `test_moving_average_changes_when_caller_violates_slicing` | "필터는 자체 슬라이싱 안 함 — 호출자 책임 명시" 회귀 (engine.py L209 가 유일 차단점) |
| `test_engine_never_exposes_future_data_to_allocator` | **모델 A 핵심**: SpyAllocator 로 매 호출 시 `prices.index.max() ≤ signal_date` 검증 |
| `test_engine_never_exposes_future_data_to_filter` | Filter 도 동일 차단 (apply_filters_and_allocator 경유) |

### B. 비거래일 방어 4단계 (`test_calendar_defense.py`) — 23/23 통과

**1. 수집 레이어** (`_is_invalid_close` + `YfinanceSource.fetch_ohlcv`):
- None / NaN / 0 close → invalid 판정
- 양수 close → valid
- (정책 회귀) 음수 close → 현재 valid (거래소 데이터에 음수 close 없음 — 정책 변경 시 catch)
- mock yfinance → NaN 행 1건 자동 drop, 잔여 2건만 반환 검증

**2. 캘린더 레이어** (`pipeline._trading_days` + L188 2차 필터):
- US: 2024-01-06 (토), 2024-01-07 (일) 자동 제외
- KR: 동일 주말 제외
- CRYPTO: 24/7 → 모든 날짜 포함
- 알 수 없는 market 코드 → 빈 리스트 (REJECTED 유도)
- pipeline.py L188 시뮬: source 가 비거래일 bar 줘도 expected_set 으로 차단

**3. 조회 레이어** (`guard_trading_day` 3 모드):
- 거래일은 모드 무관 그대로
- `raise` 모드 → ValueError ("not a trading day")
- `snap_previous` → 직전 금요일로 보정
- `snap_next` → 다음 월요일로 보정
- 알 수 없는 market → ValueError
- CRYPTO 토요일 → 모드 무관 그대로 (24/7)

**4. 엔진 레이어** (`assert_trading_day_for_universe` + `assert_all_assets_priced` + `engine.py` L209):
- 비거래일 universe → `NonTradingDayError`
- 일부 시장 비거래일 (US MLK 1/15) → 여전히 raise (silent 0 금지)
- 가격 누락 자산 → `MissingPriceError`
- engine.py L209 `prices.loc[:d]` 슬라이싱이 D+1 이후를 절대 포함하지 않음 직접 검증

### C. cash_by_ccy 환전 (`test_cash_by_ccy.py`) — 19/19 통과

**1. 단방향 환전 정확치**:
- 1_300_000 KRW @ rate (1/1300) → **gross 1000 USD - spread 2 USD = net 998 USD** 정확
- same currency convert → no-op (spread 0)
- 잔고 부족 → `InsufficientFundsError`
- amount=0 → ValueError
- `DEFAULT_FX_SPREAD_BPS == Decimal("20")` 회귀 (architecture.md L585)

**2. 단계 분리 (Q3 C)**:
- 매도 → KRW 입금 → KRW→USD 환전 → USD 매수 3단계 시퀀스 검증
- spread_cost 가 base(USD) 단위로 정확히 2 USD

**3. native 우선 (Q5 B)**:
- USD 잔고 충분 시 `ensure_native_funds` 가 환전 발생 안 시킴 (빈 리스트 반환)
- SPY → QQQ 시퀀스 (양쪽 USD) → 환전 0회
- 일부 native 보유 → deficit 만큼만 환전 (전액 환전 금지)

**4. partial fill**:
- cash 100 USD, 가격 500 USD/주, target 1주 → 0주 체결, 잔고 변화 없음
- cash 600 USD, 가격 500 USD/주, target 2주 → 1주만 체결

**5. long-only**:
- 미보유 자산 매도 → 0주, 잔고 변화 없음, 포지션 미생성
- 5주 보유 + 10주 매도 시도 → 5주만 체결 (음수 포지션 금지)

**6. fx_spread 정확치**:
- 1_300_000 KRW → **998 USD 정확** (architecture.md L585 회귀)
- 2x 환전 → 2x spread (선형 비례 검증)
- fx_spread_bps 사용자 변경 가능 (0bp / 20bp / 100bp)

**추가**:
- `ensure_native_funds` 가 deficit 정확히 충당 (spread 역산)
- `target == base_currency` 면 환전 시도 안 함 (호출자 partial fill 결정 위임)
- `execute_rebalance` 통합: 순수 USD universe 리밸런싱 시 KRW 환전 0회

### 전체 회귀 영향 검증

`pytest tests/` (전체 backend) → **67 passed, 16 skipped** — 기존 golden / api 등 다른
영역 회귀 영향 없음.

## 이슈/블로커

없음. 본 회귀 범위 (모델 A + 비거래일 4단계 + Q3 C/Q5 B 환전) 의 모든 검증 케이스가
현 구현에서 통과. 발견한 코드 결함 없음 (severity 부여 없음).

### 검증 부수효과 (관찰, severity 없음)

1. `_is_invalid_close` 는 음수 close 를 valid 로 분류한다. 거래소 데이터에 음수 close
   가 없는 현실 가정상 합리적이지만, 미래에 합성 자산/파생 도입 시 정책 재검토 가치.
   회귀 테스트 (`test_negative_close_is_valid_per_current_policy`) 가 정책 변경을
   즉시 catch 한다.

2. `convert` 의 same-currency 분기에서 잔고 검증을 생략한다 (TestSingleConversion
   내 noop 검증). 같은 통화 환전은 본질적으로 의미 없는 호출이라 문제 없음.

3. anaconda3 글로벌 환경에 `pydantic_settings` 가 없어 글로벌 python 으로는 회귀 실행
   불가. **반드시 `projects/stock-backtest/.venv/bin/python` 으로 실행** 필요. 향후
   CI/Reviewer 가속도 동일 venv 사용 필수 (관찰, severity 없음 — 환경 설정 문서화 권장).

## 다음 제안

1. **TASK-081 DONE 처리** — 모든 회귀 통과, 코드 결함 없음.
2. **TASK-092 (frontend) 와 충돌 없음** — backend/tests/regression/ 만 신규 추가, 다른
   파일 수정 0건.
3. (옵션) `backend/tests/conftest.py` 에 venv 사용 안내 또는 pytest.ini 의 minversion
   체크를 추가해 글로벌 환경 실행 시 명확한 에러 메시지 노출 검토 (별도 태스크).
4. (옵션) Phase 2 진입 시 환전 정책에 변동 spread / 통화별 differential spread 가
   필요해지면 본 회귀 파일을 확장. 현재 6번 항목 (`test_fx_spread_*`) 이 spread 산식
   변경을 즉시 catch 한다.
