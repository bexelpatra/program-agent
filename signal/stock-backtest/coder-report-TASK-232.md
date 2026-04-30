---
agent: coder
task_id: TASK-232
status: DONE
timestamp: 2026-04-30T14:00:00
---

## 결과 요약

`backend/app/services/backtest_runner.py:202-286` 의 `_persist_results` 단일 함수 (3 책임, 85줄) 를 3 module-level 헬퍼로 분해했다.

### 분해 결과

| 함수 | 책임 | 시그니처 |
|------|------|---------|
| `_build_equity_rows` | equity peak 추적 + drawdown 즉석 계산 + UTC midnight 변환 | `(equity_curve: list[Any]) -> list[tuple[datetime, Decimal, Decimal, Decimal]]` |
| `_build_trade_dicts` | TradeFill → backtest_trades insert dict (Decimal 변환 + UTC midnight) | `(fills: list[Any]) -> list[dict[str, Any]]` |
| `_compute_and_flatten_metrics` | compute_metrics 호출 + annual/monthly flatten | `(equity_curve: list[Any]) -> dict[str, float]` |

`_persist_results` 본체는 세 헬퍼 호출 + repo.insert_* + status update 만 남김 (약 22 줄). DB 세션 외 순수 변환 로직이 헬퍼로 빠져 단위 테스트 가능해짐.

### 단위 테스트 (신규 11 케이스, `backend/tests/services/test_backtest_runner.py`)

- `TestBuildEquityRows` (4): 단조 증가 → 모든 dd=0 / peak-then-drop → 음수 dd / date→datetime UTC midnight 변환 / 빈 입력
- `TestBuildTradeDicts` (3): Decimal qty 보존 + UTC midnight time / TASK-212 회귀 (settlement_date 기반, datetime.now() fallback 부재) / 빈 입력
- `TestComputeAndFlattenMetrics` (4): 6 base metric 키 존재 / annual_return_{YYYY} 패턴 / monthly_return_{YYYY-MM} 패턴 / 빈 curve → 0.0 + annual/monthly 키 부재

## 변경된 파일

- `backend/app/services/backtest_runner.py` — `_persist_results` 분해 + 3 헬퍼 추가, unused import `date` 제거 (black 포맷 적용으로 별개 라인 reflow 동반)
- `backend/tests/services/__init__.py` — 신규 (빈 파일)
- `backend/tests/services/test_backtest_runner.py` — 신규 (11 단위 테스트)

## 테스트 결과

- 신규 단위 테스트 (`tests/services/test_backtest_runner.py`): 11 passed (0.78s)
- 골든 회귀 (`tests/golden/`): 12 passed (실측. spec 의 "9 케이스" 대비 더 많음)
- e2e (`tests/e2e/`): 10 passed, 1 deselected
  - deselected: `test_persona_first_use.py::test_step3_strategies_api_exposes_allocator4_filter2` — 본 refactor 와 무관한 **pre-existing failure**. 작업 stash 후 동일 fail 재현 (running backend server 가 `ma_signal` allocator 미반영 상태). TASK-232 변경분은 stash 적용/미적용 모두 동일 결과 → 본 태스크 회귀 아님.
- ruff/black: 변경 파일 2개 모두 통과

## DoD 체크

- [x] 3 분해 함수 단위 테스트 (각 1+ 케이스): 11 케이스로 충족
- [x] 골든 9 케이스 회귀 통과 (실측 12/12 PASS)
- [x] e2e 회귀 통과 (10/11, 1 deselect 는 pre-existing)
- [x] ruff/black 통과

## 이슈/블로커

없음. e2e 의 1 케이스 fail 은 본 태스크 범위 밖이며 (running backend 의 ma_signal 미반영), 다른 Coder 의 작업이거나 서버 재시작이 필요한 것으로 추정.

## 다음 제안

- `_persist_results` 자체도 트랜잭션 boundary 만 관리하므로 추가 테스트 (DB mock 으로 insert_equity_points / insert_trades / update_status 호출 순서 검증) 가능.
- `result: Any` 타입을 `BacktestRunResult` 로 좁히려면 import 순환을 피해야 함 (현재 `from app.domain.engine import BacktestRunContext, run_backtest` 만 import). type-only import 로 좁히는 것은 별도 태스크로 분리 권장.
