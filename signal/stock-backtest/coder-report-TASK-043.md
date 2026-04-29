---
agent: coder
task_id: TASK-043
status: DONE
timestamp: 2026-04-29T10:30:00
---

## 결과 요약

`backend/app/domain/strategy.py` 신규 작성 — Strategy 3요소 조합 (allocator + signal_filters AND + rebalance_schedule) 인터페이스 + 합성 함수 `apply_filters_and_allocator`. Quant Lab CLAUDE.md L10-15 의 핵심 도메인 결정을 코드로 고정.

`backend/app/domain/engine.py` 신규 작성 — 백테스트 메인 루프. **모델 A 의 D+1 look-ahead 차단을 `prices_until_d = ctx.prices_aligned.loc[:d]` 한 줄로 구조적 강제** (engine.py L209). Allocator/Filter 가 인자로 받은 DataFrame 슬라이스 너머의 D+1 데이터에 도달할 수 없는 설계 (수동 prevention 아님).

`backend/app/domain/__init__.py` 끝에 신규 9 public symbol 을 append (병렬 안전성 — 기존 라인 무수정, TASK-031/044 의 추가 import 와도 충돌 없이 공존).

## 변경된 파일

- `projects/stock-backtest/backend/app/domain/strategy.py` (신규, 161 줄)
- `projects/stock-backtest/backend/app/domain/engine.py` (신규, 263 줄)
- `projects/stock-backtest/backend/app/domain/__init__.py` (수정 — 끝에 strategy/engine re-export append)

## 모델 A 구조적 차단 위치

| 위치 | 코드 | 효과 |
|---|---|---|
| `engine.py` L209 | `prices_until_d = ctx.prices_aligned.loc[:d]` | D+1 행은 슬라이스에 포함되지 않음 (pandas `loc[:label]` 은 closed range, label 이 index 마지막이면 자기까지). Allocator/Filter 가 받는 DataFrame 자체에 D+1 row 가 없음. |
| `engine.py` L213-218 | `apply_filters_and_allocator(strategy, universe, prices_until_d, d)` | 필터·알로케이터 호출 시점에 이미 슬라이스된 DataFrame 만 전달 — 시그널 함수 책임에 위임하지 않음 (구조적). |
| `strategy.py` L92-105 | Allocator/Filter Protocol 의 `prices_until_d` 매개변수 docstring | "engine 이 슬라이싱 책임 — Allocator 는 추가 슬라이싱하지 말 것" 명시 (계약 문서화). |

체결 (D+1) 은 별도 호출에서 분리:
- `engine.py` L222: `settlement_d = next_trading_day(ctx.base_currency, d)` (별도 변수)
- `engine.py` L230-235: `settlement_prices = _eod_prices_dict(ctx.prices_aligned, settlement_d, ...)` 로 D+1 행만 따로 조회 후 `execute_rebalance` 에 전달.

→ 시그널 (D 까지) 과 체결 (D+1) 이 메모리 상으로도 별개 객체 (`prices_until_d` vs `settlement_prices`). TASK-081 look-ahead 회귀 테스트에서 검증 가능.

## 신규 public API

### `app.domain.strategy`

| Symbol | Kind | 용도 |
|---|---|---|
| `RebalanceSchedule` | `Literal["daily","weekly","monthly","quarterly","yearly","signal_event"]` | 6 가지 리밸런싱 주기 (CLAUDE.md L13). |
| `Allocator` | Protocol | `name: str`, `required_universe() -> list[int]`, `generate_weights(universe, prices_until_d, signal_date) -> dict[int, Decimal]`. TASK-050~052 가 구현. |
| `SignalFilter` | Protocol | `name: str`, `is_eligible(asset_id, prices_until_d, signal_date) -> bool`. AND 결합. TASK-053~054 가 구현. |
| `Strategy` | `@dataclass(frozen=True)` | `name`, `allocator`, `signal_filters: tuple[SignalFilter,...]`, `rebalance_schedule: RebalanceSchedule`. |
| `apply_filters_and_allocator(strategy, universe, prices_until_d, signal_date) -> dict[int, Decimal]` | function | 합성. 1) AND 필터 → 2) allocator. 빈 universe / 필터 0 통과 시 빈 dict (cash-only). |

### `app.domain.engine`

| Symbol | Kind | 용도 |
|---|---|---|
| `BacktestRunContext` | `@dataclass` | API 가 채워서 run_backtest 호출. base_currency / period / initial_cash / universe_market_meta / prices_aligned / fx_rates_to_base / strategy / progress_callback / cancel_check. |
| `BacktestEquityPoint` | `@dataclass` | (time, equity, cash_total_in_base) — 일별 D 종가 기준 스냅샷. |
| `BacktestRunResult` | `@dataclass` | (equity_curve, fills, final_portfolio, aborted). TASK-062 가 DB 적재. |
| `run_backtest(ctx) -> BacktestRunResult` | function | 메인 루프. timeline 비면 ValueError. |
| `_is_rebalance_day(d, prev_d, schedule) -> bool` | private (테스트 노출) | 6 schedule 별 일자 판정. 첫날 (prev_d=None) 항상 True. |

## DoD 결과

| # | 검증 | 결과 |
|---|---|---|
| 1 | `python -c "from app.domain.strategy import Strategy, Allocator, SignalFilter, apply_filters_and_allocator, RebalanceSchedule; from app.domain.engine import BacktestRunContext, BacktestRunResult, run_backtest; print('ok')"` | `ok` |
| 2 | `grep "prices_aligned.loc\[:d\]" engine.py` | L209 (코드 본체) + L6, L17 (docstring 참조) — 모델 A 차단 라인 존재 |
| 3 | engine.py / strategy.py AST import 분석 — sqlalchemy/fastapi/yfinance/pykrx/app.models/app.data/app.api 0개 | engine pure / strategy pure |
| 4 | `_is_rebalance_day` 8 케이스 (첫날, monthly/quarterly/yearly/weekly/daily/signal_event 변환점·동일점) | 전부 통과 |
| 5 | mini end-to-end (1 자산 5 영업일 daily) | equity_points=5, fills=1, aborted=False — 첫날 시그널 → D+1 매수 1회, 매일 equity 기록 |
| 추가 | progress_callback + cancel_check hook (3번째 호출에서 cancel) | progress=0.4 까지 호출 후 aborted=True, equity_points=2 — 비동기 job hook 정상 |

## 클린 코드 점검

- `engine.py` 는 메인 루프만, 도메인 모델 (Portfolio/Strategy/Trade/Calendar) 전부 import (자체 정의 없음).
- `strategy.py` 는 Protocol 인터페이스 + dataclass + 합성 함수만 (구체 allocator/filter 0개 — TASK-050~054 가 구현).
- 모델 A 의 D+1 차단은 `prices_aligned.loc[:d]` 한 줄로 구조적 (시그널 함수의 선의에 의존하지 않음).
- `progress_callback` / `cancel_check` 가 비동기 job (TASK-062 BackgroundTasks/asyncio queue) 의 진행률 갱신 / 취소 hook — engine 자체는 동기 함수 (도메인 순수).
- 리밸런싱 실패 (NonTradingDayError / MissingPriceError 등) 는 logging.warning 후 루프 계속 — 1회 누락이 전체 백테스트 중단 사유 아님 (TASK-080 골든 테스트에서 정책 검증).
- 보유 포지션의 가격 누락 시 equity_in_base ValueError 회피용 사전 체크 (`missing_held` 검사) → equity 기록만 스킵, 백테스트 계속.

## 이슈/블로커

없음. 모든 DoD 통과.

## 다음 제안

1. **TASK-050~052 (Allocator 구현)**: `app.domain.strategy.Allocator` Protocol 을 구현. `name` 클래스변수 + `required_universe` + `generate_weights` 3개 메서드. FixedWeight 는 `required_universe()` 빈 리스트, AllWeather 는 정해진 5자산 asset_id 검증.

2. **TASK-053~054 (SignalFilter 구현)**: `app.domain.strategy.SignalFilter` Protocol 구현. `name` + `is_eligible` 2개 메서드. MovingAverage 는 `prices_until_d[asset_id].rolling(window).mean().iloc[-1]` 패턴.

3. **TASK-062 (백테스트 job API)**: `BacktestRunContext` 를 채우는 빌더 — 입력 (POST /api/backtests body) → universe 자산 OHLCV 조회 → calendar.align_universe_prices 로 prices_aligned 구성 → fx_rates_to_base 조회 → Strategy 인스턴스화 (allocators 카탈로그 + filters 카탈로그) → run_backtest 호출. progress_callback 은 `backtest_runs.progress = p` UPDATE, cancel_check 는 `SELECT cancel_requested FROM backtest_runs WHERE run_id=?`.

4. **TASK-080 (골든 테스트)**: mini end-to-end 시나리오를 확장 — FixedWeight/AllWeather/EqualWeight × 단일통화 KRW / 멀티통화 KRW base 미국+한국 / 암호화폐 포함 = 9 케이스. tests/golden/<scenario>.json 스냅샷.

5. **TASK-081 (look-ahead 회귀 테스트)**: 본 task 의 모델 A 차단 (engine.py L209) 검증. mock Allocator 가 prices_until_d.shape[0] 와 (prices_until_d + D+1 행) shape 비교 시 다름을 단언 — D+1 데이터를 추가 노출했을 때 시그널이 변하지 않음을 boundary case 로 확인.

6. **TASK-045 (Tax plugin)**: engine.py 에 plugin 호출 시점/방법 명확화 필요. 현재 engine 은 plugin 미호출 — 리밸런싱 후 또는 연말에 `tax_plugin.apply(realized_trades, dividends, year)` 호출 hook 추가 검토 (MVP NoTax 에서는 noop).
