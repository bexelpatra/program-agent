---
agent: coder
task_id: TASK-205
status: DONE
timestamp: 2026-04-29T20:55:00
---

## 결과 요약

V3 Q8 재결정(architecture.md L609-615)을 코드에 반영. 사용자 첫 시도 사고(run_id=56) — BTC 100% × $10,000 초기 자본 → 1코인 ~$50k 라 정수 강제로 0개 체결 → 모든 백테스트 평탄선 — 의 근본 원인을 도메인 레이어에서 분기로 차단했다. 코인(CRYPTO market) 한정 fractional 매매 (소수점 8자리), KR/US (주식·ETF·지수·채권·원자재) 는 1주 단위 정수 유지.

핵심 동작:

- **`is_fractional_market(market)` 헬퍼**: `app.domain.asset.entity` 에 단일 정의. `FRACTIONAL_MARKETS = frozenset({"CRYPTO"})`, `FRACTIONAL_PRECISION = 8`. 주식 fractional shares 가 일부 증권사만 지원하는 한국 실정 반영해 V3 는 코인만 허용.
- **Position.qty 타입 통일 — `Decimal`**: 정수 자산도 `Decimal(int)` 로 표현, CRYPTO 는 8자리. 호출자가 `int` 를 넘겨도 내부 정규화. float 누적 오차 회피.
- **Portfolio.buy/sell `fractional` 플래그**: 디폴트 `False` (정수). True 면 `(available / cost_per_unit).quantize(Decimal("1E-8"), ROUND_DOWN)` 으로 max_affordable 계산. partial fill 정책 그대로 유지.
- **execute_rebalance target_qty 분기**: `is_fractional_market(market)` 이면 8자리 quantize, 아니면 `Decimal(int(...))`. asset_meta 의 market 필드를 키로 분기.
- **TradeFill.qty_filled / TradeOrder.qty_target 시그니처**: `int → Decimal` 변경. backtest_runner 가 그대로 Numeric(20,8) 컬럼에 적재.
- **ORM + 마이그레이션**: `BacktestTrade.qty` Numeric(20,0) → Numeric(20,8). 알렘빅 0004_fractional_qty (up: alter to (20,8), down: alter back with truncation 경고). `quant-lab-postgres` 에 실제 적용 완료 — `\d backtest_trades` 로 `numeric(20,8)` 확인.

호환성:

- 정수 자산 시나리오 (KR/US 단독) — 골든 스냅샷 6/9 케이스 (시나리오 1 KR-only 3종 + 시나리오 2 KR-US 3종) **그대로 통과**, drift 0. Decimal(int) 표현이 정수와 산술적으로 동치라 결과 변화 없음.
- CRYPTO 포함 시나리오 (시나리오 3 SPY+BTC) 3 케이스만 스냅샷 갱신 — fractional 매매로 결과 자체가 의도적 변화 (사고 본질 검증).

## 변경된 파일

- `/home/jai/pa/stock-backtest/projects/stock-backtest/backend/app/domain/asset/entity.py` (수정)
  - `FRACTIONAL_MARKETS`, `FRACTIONAL_PRECISION` 모듈 상수 추가
  - `is_fractional_market(market: str) -> bool` 헬퍼 추가
- `/home/jai/pa/stock-backtest/projects/stock-backtest/backend/app/domain/portfolio.py` (수정)
  - `Position.qty` 타입 `int → Decimal`
  - `_FRACTIONAL_QUANTUM = Decimal(1).scaleb(-FRACTIONAL_PRECISION)` 모듈 상수
  - `buy(..., qty_target: int|Decimal, ..., fractional: bool = False) -> tuple[Decimal, Decimal]` — fractional 분기 (8자리 quantize / 정수 강제)
  - `sell(..., qty: int|Decimal, ..., fractional: bool = False) -> tuple[Decimal, Decimal]` — 동일 분기
  - `_upsert_position(..., added_qty: Decimal, ...)` — Decimal 가중평균
- `/home/jai/pa/stock-backtest/projects/stock-backtest/backend/app/domain/trade.py` (수정)
  - `is_fractional_market`, `_FRACTIONAL_QUANTUM` import
  - `TradeOrder.qty_target: int → Decimal`, `TradeFill.qty_filled: int → Decimal`
  - `_classify_orders` 시그니처 Decimal 화 (target_qty, sells, buys 모두 Decimal)
  - `_execute_sells/_execute_buys` 가 `fractional = is_fractional_market(market)` 계산 후 portfolio.sell/buy 에 전달
  - `execute_rebalance` 의 target_qty 계산: `is_fractional_market(market)` 분기 — CRYPTO 는 8자리 quantize, 그 외는 `Decimal(int(...))`
- `/home/jai/pa/stock-backtest/projects/stock-backtest/backend/app/services/backtest_runner.py` (수정)
  - `_persist_results` 의 `qty_value` 처리: `Decimal` 인스턴스면 그대로, 아니면 캐스트. Numeric(20,8) 컬럼에 적재 시 fractional 8자리 보존.
- `/home/jai/pa/stock-backtest/projects/stock-backtest/backend/app/models/backtest.py` (수정)
  - `BacktestTrade.qty`: `Numeric(20, 0) → Numeric(20, 8)` + docstring 갱신
- `/home/jai/pa/stock-backtest/projects/stock-backtest/backend/alembic/versions/0004_fractional_qty.py` (신규)
  - `revision = "0004_fractional_qty"`, `down_revision = "0003_backtest_tables"`
  - upgrade: `op.alter_column("backtest_trades", "qty", existing_type=Numeric(20,0), type_=Numeric(20,8))`
  - downgrade: 역방향 (CRYPTO 매매 적재된 테이블은 절단 위험 docstring 명시)
- `/home/jai/pa/stock-backtest/projects/stock-backtest/backend/tests/e2e/test_failure_replay.py` (수정 — append-only)
  - `test_replay_btc_fractional_buy_with_small_capital` 추가: BTC $50k @ 초기자본 $10k → fractional 매수로 0 < qty < 1 BTC 체결 회귀 박제. `is_fractional_market("CRYPTO")=True` / `is_fractional_market("US")=False` 동시 검증.
- `/home/jai/pa/stock-backtest/projects/stock-backtest/backend/tests/golden/snapshots/scenario_3_us_crypto__fixed_weight.json` (갱신)
- `/home/jai/pa/stock-backtest/projects/stock-backtest/backend/tests/golden/snapshots/scenario_3_us_crypto__all_weather.json` (갱신)
- `/home/jai/pa/stock-backtest/projects/stock-backtest/backend/tests/golden/snapshots/scenario_3_us_crypto__equal_weight.json` (갱신)

## 갱신된 골든 스냅샷 목록 (사유: fractional BTC 매수 활성화로 결과 자체가 의도적 변화)

시나리오 3 (SPY + BTC, base=USD, 초기자본 $10,000, 2020-01-01 ~ 2024-12-31):

| 케이스 | 변경 전 final_equity | 변경 후 final_equity | num_fills 변경 | cagr 변경 |
|---|---|---|---|---|
| fixed_weight (60/40) | 13,185.84 | 25,971.69 | 4 → 79 | 0.057 → 0.211 |
| all_weather (60/40 equity/commodity) | 13,185.84 | 25,971.69 | 4 → 79 | 0.057 → 0.211 |
| equal_weight (50/50) | 12,581.36 | 29,289.85 | 4 → 80 | 0.047 → 0.241 |

해석:
- 변경 전: BTC 정수 강제 시 1코인 매수 자본 부족 → BTC 0개 체결, 사실상 SPY 단일 자산 백테스트가 됨 → equity 평탄선 + sharpe 800+ (변동성 0 에 가까운 SPY 결정적 시계열).
- 변경 후: 0.x BTC 매수 정상 → 시나리오의 BTC 변동성 (연 40% growth + sin noise) 이 제대로 반영 → cagr/mdd/win_rate 가 현실적 수치. num_fills 79~80 = 5년 월간 리밸런싱(60회) × 2자산 평균 + 추가 SELL/BUY 분류 결과로 정합.

`mdd: -0.000212`, `win_rate: 0.897` 등 — 결정적 시계열이라 여전히 작은 값이지만 fractional 매매로 BTC 노출이 발생해 0이 아닌 의미 있는 숫자가 잡힘.

## DoD 결과

| # | 항목 | 결과 |
|---|---|---|
| 1 | import: `is_fractional_market('CRYPTO')=True, ('US')=False` | PASS — `True False` 출력, FRACTIONAL_PRECISION=8, FRACTIONAL_MARKETS=frozenset({'CRYPTO'}) |
| 2 | alembic upgrade head — 0004 적용 | PASS — `quant-lab-postgres` 의 `backtest_trades.qty` 가 `numeric(20,8)` 로 변경 확인 (`\d backtest_trades`) |
| 3 | Portfolio.buy fractional: BTC $50k @ $10k 자본 → ~0.1996 BTC | PASS — qty=0.19960059, cost=9999.99953902950000, cash_left=0.00046097 |
| 4a | regression 50개 (test_calendar_defense + test_cash_by_ccy + test_lookahead) | PASS 50/50 |
| 4b | golden 12개 (9 시나리오 + 3 엔진 무결성) | PASS 12/12 (시나리오 3 스냅샷 갱신 후) |
| 4c | API contract fuzz | baseline 5 fail / 변경 후 5 fail (동일) — 환경 의존 fuzz, 코드 변경 회귀 없음 |
| 4d | tests/ 전체 (API 제외) | PASS 72/72 |
| 5 | e2e 추가: BTC $10k 자본 → 0.x 코인 매수 회귀 박제 | PASS — `test_replay_btc_fractional_buy_with_small_capital` 신규 |

API contract fuzz 5 케이스 (`GET /api/assets/{asset_id}` 등) 는 schemathesis 가 무작위 hypothesis 입력으로 5xx 를 유발하는 환경 의존 실패 — 변경 전 stash 상태에서도 동일 5개 fail (회귀 0). 본 태스크와 무관.

## 클린 코드 점검

- `is_fractional_market` 단일 정의 (`app.domain.asset.entity`) — portfolio/trade 두 곳에서 import.
- `_FRACTIONAL_QUANTUM = Decimal(1).scaleb(-FRACTIONAL_PRECISION)` 도 portfolio/trade 양쪽에 같은 값. 도메인 entity 에 한 번만 두는 게 더 좋지만, 도메인 분리(Portfolio 와 Trade 가 entity 에서 quantum 까지 끌어쓰는 것은 과도) 고려해 모듈 상수로 유지. 추후 통합 정리 가능.
- Portfolio.buy/sell 의 `fractional` 디폴트 `False` — 기존 호출자 (테스트 14곳, regression 6곳) 모두 정수 동작 유지로 후방호환.
- `qty_target: int | Decimal` 유니온 — 호출자가 int 넘겨도 자동 Decimal 정규화 (regression 호환).
- Numeric(20, 8) 마이그레이션 양방향 (down 도 정의), 단 fractional 매매 적재된 후 down 시 절단 가능을 docstring 에 경고.

## 다음 제안

1. **TASK-206 (Manager 판단)**: ohlcv 컬럼이 이미 Numeric(20,8) 이고 BTC 가격은 8자리 충분, 단 BTC 가격 ohlcv 백필이 실제 환경에서 정상 적재되어야 사용자 시나리오에서 fractional 효과가 살아남. data_loader → backtest_runner 경로의 BTC 자산 ohlcv 가용성 회귀 테스트가 이미 있는지 점검 필요.
2. **AllocatorParams 사후 검증** (선택): FixedWeightParams 에서 weights 가 dict 키가 asset_id 인지 검증할 때, asset_id 의 market 까지 확인해 "코인 비중 100% 인데 초기 자본이 1코인 가격보다 작음" 경고를 backend 에서도 발신 (TASK-204 frontend 경고와 이중 방어). 우선순위 낮음 — TASK-204 에서 frontend 가 충분 차단.
3. **Position.qty Decimal 통일 영향**: `app.domain.allocators` (FixedWeight/EqualWeight/AllWeather) 가 Position 을 직접 다루지 않으므로 영향 0. `app.domain.metrics.compute_metrics` 도 equity 시계열만 받아 영향 0. 회귀 72/72 PASS 가 이를 입증.
4. **frontend 표시 정밀도** (TASK-204 와 후속): 매매 내역 UI 가 qty 표시 시 CRYPTO 만 8자리, 나머지는 정수 — 같은 fractional/integer 분기를 frontend 에도 도입할지 여부 manager 판단.
