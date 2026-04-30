---
agent: coder
task_id: TASK-212
status: DONE
timestamp: 2026-04-30T11:30:00
---

## 결과 요약

`TradeFill` dataclass 에 `settlement_date: date` 필드를 추가하고, `_execute_sells`/`_execute_buys`/`execute_rebalance` 가 호출 시 이 값을 전파해 모든 fill 에 정확히 채워지도록 수정했다. `backtest_runner._persist_results` 에서는 `getattr(fill, 'time', now)` fallback (run_id=96 의 trades.time 이 백테스트 실행 시각으로 일괄 기록되던 버그 원인) 을 `datetime.combine(fill.settlement_date, datetime.min.time(), tzinfo=timezone.utc)` 로 교체했다.

5단계 명세 그대로 수행:
- ① `TradeFill` 에 `settlement_date: date` 7번째 필드 추가 (frozen dataclass).
- ② `_execute_sells` (L197) / `_execute_buys` (L233) 시그니처에 `rebalance_date: date` 인자 추가.
- ③ `execute_rebalance` (L361 sell, L366 buy) 호출 시 `rebalance_date=rebalance_date` 전달.
- ④ 두 함수가 `TradeFill(...)` 생성 시 (sell, buy 각 1곳) `settlement_date=rebalance_date` 채움.
- ⑤ `backtest_runner.py:242` `getattr(fill, 'time', now)` → `fill.settlement_date` UTC midnight 변환.

## 변경된 파일

- `/home/jai/pa/stock-backtest/projects/stock-backtest/backend/app/domain/trade.py` (수정)
  - `TradeFill` 필드 추가: `settlement_date: date` (마지막 7번째)
  - `_execute_sells` / `_execute_buys` 시그니처에 `rebalance_date: date` 인자 추가, 두 함수가 TradeFill 생성 시 채움
  - `execute_rebalance` 가 두 함수 호출 시 `rebalance_date` 전달
- `/home/jai/pa/stock-backtest/projects/stock-backtest/backend/app/services/backtest_runner.py` (수정)
  - `_persist_results` 의 trade.time fallback (`getattr(fill, 'time', now)`) 제거
  - `datetime.combine(fill.settlement_date, datetime.min.time(), tzinfo=timezone.utc)` 로 교체
  - `now = datetime.now(timezone.utc)` 변수 제거 (더 이상 fallback 필요 없음)
  - 주석 갱신: TASK-212 (2026-04-30) 버그 수정 이력 명시
- `/home/jai/pa/stock-backtest/projects/stock-backtest/backend/tests/domain/__init__.py` (신규, 빈 파일)
- `/home/jai/pa/stock-backtest/projects/stock-backtest/backend/tests/domain/test_trade.py` (신규)
  - `TestTradeFillSettlementDate`: BUY 1건 / SELL 1건 / 다중 자산 — settlement_date 가 rebalance_date 와 동일 (3개 케이스)
  - `TestTradeFillFieldOrder`: positional 7-arg 생성 검증 (1개), 시장별 디폴트 수수료 회귀 (1개)
  - 총 5 테스트, 모두 통과

## 테스트 결과

신규 단위 테스트 (tests/domain/test_trade.py): **5 passed**.

전체 비-fuzz 회귀 (`tests/regression tests/golden tests/e2e tests/domain`): **77 passed, 0 failed**.
- regression/test_calendar_defense.py: 22/22 통과
- regression/test_cash_by_ccy.py: 19/19 통과 (execute_rebalance 통합 케이스 포함)
- regression/test_lookahead.py: 8/8 통과
- golden/test_golden_scenarios.py: **9 케이스 모두 통과** (settlement_date 필드 추가가 골든 스냅샷 회귀 0)
- e2e (test_failure_replay + test_persona_first_use): 11/11 통과
- domain/test_trade.py: 5/5 통과 (신규)

API fuzz 5건 실패 (`tests/api/test_api_contract.py::test_api_contract_fuzz[GET/DELETE /api/{assets|backtests}/{id}*]`) 는 schemathesis 가 `asset_id=0` / `run_id=0` 로 fuzz 한 후 ErrorResponse 형식 contract mismatch — TASK-212 변경을 stash 한 상태에서도 동일 실패 재현 확인 → **기존 회귀이며 본 태스크와 무관**.

## TradeFill 사용처 grep 검증

`grep -rn "TradeFill" /home/jai/pa/stock-backtest/projects/stock-backtest --include="*.py"` 결과 (테스트 fixtures 의 직접 생성 0건 확인):
- `app/domain/trade.py`: 정의 + 6건 (시그니처/생성/리턴 타입)
- `app/domain/engine.py`: 2건 import + 타입 어노테이션 — 직접 생성 안 함
- `app/domain/__init__.py`: re-export
- `app/services/backtest_runner.py`: 주석 1건 — 직접 생성 안 함
- `tests/`: TradeFill 직접 생성 코드 0건 (test_cash_by_ccy 의 execute_rebalance 통합 케이스만 — 호출 경로로 자동 채워지므로 영향 없음)

## 이슈/블로커

없음.

코드 회귀 의도 확인:
- 골든 스냅샷 9 케이스 모두 통과 → backtest_trades 의 time 값 변경이 스냅샷 비교 대상에 포함되지 않음 (스냅샷이 equity_curve / metrics 위주, trade time 미비교).
- 따라서 명세에 언급된 "TASK-215 가 trade time 변경된 골든 baseline 통합 재생성" 은 **불필요**할 가능성. TASK-215 가 이미 다른 사유 (TASK-211/213/214 변경) 로 baseline 재생성을 하므로 그쪽에서 함께 흡수하면 됨.

## 다음 제안

1. TASK-215 (골든 baseline 9 케이스 통합 재생성) — 본 태스크 변경이 골든을 깨지 않는 것은 확인되었으나, 다른 동행 태스크 (TASK-211 청산 누락 / TASK-213 백필 정책 / TASK-214 yfinance auto_adjust) 가 equity 값을 변경할 가능성이 있어 통합 재생성은 유효.
2. 후속 회귀 보강 (선택): `tests/e2e` 또는 `tests/regression` 에 "백테스트 실행 → 결과 trades.time 가 settlement_date 와 일치하는 정수 일자만" 검증하는 통합 테스트 추가. 현재 e2e/test_failure_replay 가 backtest 실행 후 결과만 확인하므로 trades.time 의 시계열성을 직접 검증하지 않음. (Tester 영역이라 본 태스크 범위 밖)
