---
agent: coder
task_id: TASK-062
status: DONE
timestamp: 2026-04-29T11:45:00
---

## 결과 요약

백테스트 비동기 job API 5개(POST/GET 상태/GET 결과/DELETE/GET 이력)와 그 backbone 인 schemas, repository, services 레이어를 구현했다.
FastAPI BackgroundTasks 로 즉시 pending 응답 후 별도 thread 가 engine 호출, 진행률은 별도 SessionLocal 로 갱신, 취소는 DB 플래그 폴링.
실패 시 `error_json` 에 V2 § 에러 응답 계약 (stage/type/message/request_ctx/trace_id) 적재.

데이터 로더 (prices_aligned/fx_rates) 는 TASK-100 통합 예정이므로 현재 placeholder (빈 DataFrame). engine 이 ValueError 던지면 `_record_failure` 가 잡아 "데이터 로더 미구현" 메시지를 status=failed 로 마무리.

## 변경된 파일

### 신규
- `/home/jai/pa/stock-backtest/projects/stock-backtest/backend/app/schemas/backtest.py` — Pydantic 8개 schema (BacktestStatus, RebalanceSchedule, StrategyConfig, BacktestCreate, BacktestRun, EquityPoint, TradeRecord, MetricsPayload, BacktestResult)
- `/home/jai/pa/stock-backtest/projects/stock-backtest/backend/app/data/repositories/backtest_repository.py` — BacktestRepository + compute_run_hash (universe sorted, sha256[:32])
- `/home/jai/pa/stock-backtest/projects/stock-backtest/backend/app/services/__init__.py` — 패키지 init + re-export
- `/home/jai/pa/stock-backtest/projects/stock-backtest/backend/app/services/backtest_runner.py` — execute_backtest_job + build_strategy_from_config + 진행률/취소 콜백 + _persist_results + _record_failure
- `/home/jai/pa/stock-backtest/projects/stock-backtest/backend/app/api/backtests.py` — 라우터 5개 엔드포인트

### 수정 (append-only)
- `/home/jai/pa/stock-backtest/projects/stock-backtest/backend/app/api/__init__.py` — `backtests_router` 추가
- `/home/jai/pa/stock-backtest/projects/stock-backtest/backend/app/main.py` — `include_router(backtests_router)` 추가

## 신규 public API (Repository / Services)

### `BacktestRepository` (`app.data.repositories.backtest_repository`)
- `create_run(*, run_hash, strategy_name, params, universe, period_start, period_end, base_currency, market_mode='STOCK') -> BacktestRun`
- `find_run(run_id: int) -> BacktestRun | None`
- `find_by_hash(run_hash: str) -> BacktestRun | None`
- `update_status(run_id, *, status=None, progress=None, error_json=None, started_at=None, finished_at=None) -> None`
- `request_cancel(run_id: int) -> bool`
- `is_cancel_requested(run_id: int) -> bool`
- `list_runs(limit=50, offset=0) -> list[BacktestRun]`
- `delete_run(run_id: int) -> bool`
- `insert_equity_points(run_id, points: list[tuple[datetime, Decimal, Decimal, Decimal]]) -> int`
- `get_equity(run_id) -> list[BacktestEquity]`
- `insert_trades(run_id, trades: list[dict]) -> int`
- `get_trades(run_id) -> list[BacktestTrade]`
- `insert_metrics(run_id, metrics: dict[str, float]) -> int`
- `get_metrics(run_id) -> dict[str, float]`
- 모듈 함수 `compute_run_hash(strategy_name, params, universe, period_start, period_end, base_currency) -> str`

### `app.services.backtest_runner`
- `build_strategy_from_config(strategy_config: dict) -> Strategy`
- `execute_backtest_job(run_id: int) -> None`

### 라우트 (`/api/backtests`)
- `POST   /api/backtests` → 201 `BacktestRun` (즉시 pending, 캐시 hit 시 기존 run)
- `GET    /api/backtests/{run_id}` → `BacktestRun` (404 if not found)
- `GET    /api/backtests/{run_id}/result` → `BacktestResult` (404 / 409 if not done)
- `DELETE /api/backtests/{run_id}` → 204 (pending/running 은 cancel, 그 외 delete-cascade)
- `GET    /api/backtests` → `PaginatedResponse[BacktestRun]` (limit ≤ 200, offset ≥ 0)

## DoD 검증 결과 (실측)

1. **import** (`from app.main import app; from app.services import ...; from app.data.repositories.backtest_repository import ...; from app.schemas.backtest import ...`) → `ok`
2. **routes** → `['/api/backtests', '/api/backtests/{run_id}', '/api/backtests/{run_id}/result']` 모두 포함 (POST + GET 5개)
3. **compute_run_hash 멱등성** — universe 순서 [1,2] vs [2,1] 동일 hash `2d9403a0631e34dc25a31e3dd06c4a58`
4. **build_strategy_from_config** — fixed_weight + moving_average filter 1개 정상 빌드. equal_weight (no params) / all_weather (5 categories) / momentum filter 추가 검증, unknown allocator → `ValueError`
5. **OpenAPI components** — `BacktestCreate / BacktestRun / BacktestResult / EquityPoint / TradeRecord / MetricsPayload / StrategyConfig` 7종 모두 노출 (missing: `[]`)

## 이슈/블로커

- **데이터 로더 placeholder (BLOCKER 후보, SOFT)**: `execute_backtest_job` 가 `prices_aligned=pd.DataFrame()`, `fx_rates_to_base={}` 로 호출 → `run_backtest` 의 `trading_days_in_period` 가 비어있으면 ValueError 발생 → status=failed 로 마무리. 정상 데이터 로딩은 TASK-100 (통합) 시점에 OhlcvRepository + fx 로더 결합 필요. 현재는 import / 라우트 / schema 까지만 충족 (태스크 스펙에 명시된 BLOCKER-001 우회).
- **TradeFill.time 부재**: 도메인 `TradeFill` 에 체결 시각 필드 없음 → DB 적재 시 `now()` fallback. 골든 테스트 정확성 확보 위해 향후 engine.run_backtest 에서 settlement_d 를 fill 에 첨부하는 개선 권장 (다음 제안 참조).
- 직접 건드리지 말라고 지시된 파일 (frontend, domain/, 다른 api/_/schemas/_) 은 모두 보존했음.

## 다음 제안

1. **TASK-100 통합 시점**: `services/backtest_runner.py` 의 `_make_load_prices(run_id)` 헬퍼를 추가해 `OhlcvRepository.list_for_universe(...)` + `align_universe_prices` + fx 로더를 합쳐 `prices_aligned`/`fx_rates_to_base` 를 채운다. 현재의 placeholder 분기는 그 PR 에서 제거.
2. **TradeFill.time 첨부**: `domain.engine.run_backtest` 에서 `execute_rebalance` 가 반환한 fills 에 `settlement_d` 를 attach 하도록 `TradeFill` 에 `time: date` 필드 추가 + engine 에서 채워넣기. trade_repository 가 정확한 시점을 적재할 수 있어 골든 테스트 (TASK-080) 정밀도 ↑.
3. **ASGI 백그라운드 thread 안전성**: FastAPI BackgroundTasks 는 동일 event loop 에서 실행. 장시간 백테스트가 응답 latency 에 영향 없게 하려면 `asyncio.run_in_executor` 또는 별도 worker 프로세스 (ARQ/Celery) 도입 검토 — Phase 2 운영 부하에서 측정 후 결정.
4. **워커 크래시 복구**: 시작 시 `pending` / `running` row 를 `failed` (`error_json={"stage":"recovery","message":"worker crash"}`) 로 일괄 정리하는 lifespan startup hook 권장 (TASK-082 검증 포인트).
5. **`BacktestRun.name` 영속화**: 현재 schema 에는 있으나 DB 컬럼 부재 → 응답에서만 echo. UI 이력 화면이 사용자 친화 라벨이 필요해지면 `backtest_runs.name` 컬럼 마이그레이션 추가.
