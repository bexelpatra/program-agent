---
agent: tester
task_id: TASK-080+TASK-082
status: DONE
timestamp: 2026-04-29T09:30:00
severity: blocker
---

## 결과 요약

TASK-080(골든 스냅샷, 9 케이스)와 TASK-082(API 계약 + 비동기 job 통합)를 한 묶음으로 완료. backend/tests/golden/ + backend/tests/api/ 두 디렉토리 신규 생성. 합계 **17 통과 / 16 SOFT skip / 0 실패**. 1차 실행으로 9개 골든 스냅샷 JSON 자동 생성, 2차 실행에서 모두 스냅샷 일치 PASS. API 계약 fuzz와 비동기 job 통합 스모크는 **DB 스키마 drift (BLOCKER-001 미해결 잔재)** 로 인해 의도된 SOFT skip 처리 — 코드 결함 아님.

테스트 실행 중 **신규 blocker 1건 발견**: BLOCKER-001 의 baseline migration `0001_v3_baseline` 이 사용자에 의해 적용되지 않은 상태. ORM 모델은 `assets.created_at`, `backtest_runs.status` 등 신규 컬럼을 기대하나 운영 DB(`stock_backtest`)는 이전 0003 스키마를 그대로 보유 → 모든 DB 의존 라우터 (assets, backtests) 가 500 SQLAlchemy ProgrammingError. `signal/stock-backtest/blockers.md` 의 BLOCKER-001 처리 결과(PARTIAL) 와 일치하나, **모든 백엔드 통합 테스트가 막혀있다는 사실을 강조 필요**.

## 변경된 파일

- /home/jai/pa/stock-backtest/projects/stock-backtest/backend/tests/conftest.py (신규)
- /home/jai/pa/stock-backtest/projects/stock-backtest/backend/tests/golden/__init__.py (신규)
- /home/jai/pa/stock-backtest/projects/stock-backtest/backend/tests/golden/test_golden_scenarios.py (신규, 12 테스트)
- /home/jai/pa/stock-backtest/projects/stock-backtest/backend/tests/golden/snapshots/scenario_1_kr_only__fixed_weight.json (신규)
- /home/jai/pa/stock-backtest/projects/stock-backtest/backend/tests/golden/snapshots/scenario_1_kr_only__all_weather.json (신규)
- /home/jai/pa/stock-backtest/projects/stock-backtest/backend/tests/golden/snapshots/scenario_1_kr_only__equal_weight.json (신규)
- /home/jai/pa/stock-backtest/projects/stock-backtest/backend/tests/golden/snapshots/scenario_2_kr_us__fixed_weight.json (신규)
- /home/jai/pa/stock-backtest/projects/stock-backtest/backend/tests/golden/snapshots/scenario_2_kr_us__all_weather.json (신규)
- /home/jai/pa/stock-backtest/projects/stock-backtest/backend/tests/golden/snapshots/scenario_2_kr_us__equal_weight.json (신규)
- /home/jai/pa/stock-backtest/projects/stock-backtest/backend/tests/golden/snapshots/scenario_3_us_crypto__fixed_weight.json (신규)
- /home/jai/pa/stock-backtest/projects/stock-backtest/backend/tests/golden/snapshots/scenario_3_us_crypto__all_weather.json (신규)
- /home/jai/pa/stock-backtest/projects/stock-backtest/backend/tests/golden/snapshots/scenario_3_us_crypto__equal_weight.json (신규)
- /home/jai/pa/stock-backtest/projects/stock-backtest/backend/tests/api/__init__.py (신규)
- /home/jai/pa/stock-backtest/projects/stock-backtest/backend/tests/api/test_api_contract.py (신규, 21 테스트 — 5 통과 + 16 SOFT skip)
- /home/jai/pa/stock-backtest/projects/stock-backtest/backend/requirements.txt (수정: schemathesis>=3.39,<4 추가, pytest>=9 호환 충돌 회피 주석 명시)

## 테스트 결과

### TASK-080 골든 스냅샷 (12 테스트)

전체 통과. 1차 실행: 9 케이스 스냅샷 자동 생성 (`pytest.skip("snapshot created — re-run to verify")`) + 3 엔진 invariant 테스트 통과. 2차 실행: 9 스냅샷 비교 모두 PASS (rel_tol=1e-4) + 3 invariant 모두 PASS.

- 통과: 12 (12/12)
- 실패: 0
- 스냅샷 파일: 9 (각 시나리오 × 전략 매트릭스)

매트릭스 (시나리오 × 전략):

| Scenario | Strategy | final_equity | num_fills | CAGR | MDD | Sharpe |
|----------|----------|--------------|-----------|------|-----|--------|
| 1 KR only | fixed_weight | 12,988,918.58 KRW | 26 | 0.0540 | 0.0 | 3046.93 |
| 1 KR only | all_weather | 12,988,918.58 KRW | 26 | 0.0540 | 0.0 | 3046.93 |
| 1 KR only | equal_weight | 12,632,025.00 KRW | 27 | 0.0482 | 0.0 | 2603.98 |
| 2 KR+US | fixed_weight | 15,102,763.31 KRW | 5 | 0.0865 | 0.0 | 1042.35 |
| 2 KR+US | all_weather | 15,102,763.31 KRW | 5 | 0.0865 | 0.0 | 1042.35 |
| 2 KR+US | equal_weight | 15,330,753.90 KRW | 10 | 0.0898 | 0.0 | 1219.06 |
| 3 US+CRYPTO | fixed_weight | 13,185.84 USD | 4 | 0.0571 | 0.0 | 962.03 |
| 3 US+CRYPTO | all_weather | 13,185.84 USD | 4 | 0.0571 | 0.0 | 962.03 |
| 3 US+CRYPTO | equal_weight | 12,581.36 USD | 4 | 0.0472 | 0.0 | 798.28 |

엔진 invariant 추가 테스트 (스냅샷 없음):

- `test_engine_aborts_when_cancel_check_returns_true`: cancel_check True → result.aborted=True + 부분 결과 반환 PASS
- `test_engine_progress_callback_called`: progress 가 단조증가 + 마지막 값 1.0 PASS
- `test_engine_raises_on_empty_period`: 거래일 0인 기간 → ValueError("no trading days") PASS

### TASK-082 API 계약 + 비동기 job 통합 (21 테스트)

- 통과: 5
- SOFT skip: 16
  - 비-DB 의존 fuzz (GET /api/health, GET /api/strategies): 통과
  - DB 의존 fuzz (assets, backtests, ohlcv) 9건 + 비동기 job lifecycle 6건 + recovery 1건: SOFT skip with explicit BLOCKER-001 reason
- 실패: 0

통과 항목:
- `test_health_endpoint`: GET /api/health → 200 + status=ok + version
- `test_strategies_endpoint_returns_mvp_presets`: allocator 3 (fixed_weight/all_weather/equal_weight) + filter 2 (moving_average/momentum) MVP 일치
- `test_openapi_endpoint`: /api/openapi.json 노출 + paths 검증
- `test_api_contract_fuzz[GET /api/health]`: schemathesis fuzz PASS
- `test_api_contract_fuzz[GET /api/strategies]`: schemathesis fuzz PASS

SOFT skip 사유 (모두 BLOCKER-001 잔재):
- `db_alive` fixture 가 ORM 컬럼 일치 검증 (`SELECT created_at FROM assets`, `SELECT status FROM backtest_runs`) 실패 → False → DB 의존 테스트 일괄 skip
- 실제 DB 는 살아있고(PostgreSQL 16.13 정상 ping) `assets/backtest_runs/ohlcv` 테이블도 존재하나 컬럼 스키마가 ORM 모델과 불일치
- 사용자가 `backend/alembic/README.md` 절차로 baseline migration 적용 시 자동 통과 예상

schemathesis 환경 이슈:
- schemathesis 4.x 는 pytest>=9 요구로 pytest-asyncio 와 충돌 → 3.39.16 으로 핀 (requirements.txt 주석)
- FastAPI 0.115 의 OpenAPI 3.1 출력은 schemathesis 3.x 미완 지원 → `from_asgi(..., force_schema_version="30")` 으로 우회

## 이슈/블로커

### BLOCKER (1건, severity=blocker)

**B-001: BLOCKER-001 baseline migration 미적용 → 모든 DB 의존 API 500**

- 영향: assets, backtests, ohlcv 라우터 전체 SQLAlchemy `ProgrammingError: column ... does not exist` 발생
  - 예: `column assets.created_at does not exist`
  - 예: `column backtest_runs.status does not exist`
- 근본 원인: `signal/stock-backtest/blockers.md` BLOCKER-001 처리 결과가 PARTIAL — `0001_v3_baseline` 작성 완료했으나 사용자가 옵션 A/B (DB drop+recreate or `DROP SCHEMA public CASCADE` + `alembic upgrade head`) 미실행
- 코드 결함이 아니라 인프라 미적용 → 코드는 정합 (ORM 모델 ↔ migration ↔ baseline 일치)
- 그러나 **모든 백엔드 통합 테스트가 막혀있어 사용자 워크플로우 불가** → severity 를 frontmatter 에서 `blocker` 로 격상
- BLOCKER-001 자체는 별도 후속 태스크화 필요 없음 (사용자 액션 필요)

### Observation (3건, severity=observation 수준)

**O-001: 데이터 로더 placeholder — 비동기 job 모두 failed 종료 예상**
- `services/backtest_runner.execute_backtest_job` L283-289 가 `prices_aligned=pd.DataFrame(), fx_rates_to_base={}` 로 ctx 생성 → 엔진 첫 리밸런싱에서 `ValueError("no trading days")` 또는 빈 결과
- `_record_failure` 가 status='failed' + error_json (stage/type/message/trace_id) 로 정상 기록 — 코드 결함 아니라 known limitation (TASK-100 통합 예정)
- BLOCKER-001 해소 후 lifecycle 테스트 (`test_backtest_lifecycle_failed_due_to_data_loader_placeholder`) 가 자동으로 검증

**O-002: 메트릭 모듈 — 결정적 시계열에서 Sharpe 비정상 큰 값**
- 골든 시나리오의 Sharpe 가 798~3046 등 비현실적
- 원인: 결정적 우상향 시계열 (vol=0) → 일별 수익률이 거의 동일 → annualized vol ≈ 0 → ann_return / vol → 큰 값
- `domain/metrics.py:118` `sharpe = ann_return / vol_total if vol_total > 0 else 0.0` 의 분모 가드는 정상 작동 — 하지만 vol_total 이 매우 작은 양수 (10^-6 수준) 일 때 보호 안 됨
- 실 시장 데이터는 vol_daily ~ 1% 수준이라 실무에서 문제 없음 — 다만 합성 데이터 골든 테스트의 Sharpe 자릿수가 실측과 무관하다는 점은 retrospective 에 메모 권장
- 개선안: vol_total 이 일정 임계값 (예: 1e-4) 미만이면 0 반환 — 향후 metrics_robust 태스크에서 검토

**O-003: 워커 크래시 후 pending/running 복구 미구현**
- `test_recovery_after_worker_crash` skip 처리 (MVP 외)
- BackgroundTasks 가 process restart 후 손실 — 별도 reaper 태스크 또는 Redis/Celery 도입 필요
- Phase 2 권장

### 클린 아키텍처 위반 검사 (Coder 산출물)

전체 PASS — 위반 없음.

- domain/ 디렉토리는 SQLAlchemy/HTTP/외부 라이브러리 import 없음 (pandas/exchange_calendars 만, 정책상 허용)
- presentation 없는 백엔드 — N/A
- repository pattern 정상 (services/backtest_runner 가 BacktestRepository 경유, 라우터가 직접 ORM 미사용)
- DTO ↔ Entity 분리 정상 (schemas/backtest.py 가 도메인 BacktestRunContext 와 분리)
- 함수 길이: backtest_runner.execute_backtest_job 100줄 — 단일 책임 (job 라이프사이클) 이고 try/except 계층 분기 명확하므로 문제 없음

## 다음 제안

### 즉시 (Manager → 사용자)

1. **사용자 액션 필요 (Execution=user)**: BLOCKER-001 해소 절차 실행 — `cd projects/stock-backtest && docker compose down -v && docker compose up -d && cd backend && alembic upgrade head` 또는 `psql -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;" && alembic upgrade head`
2. 사용자가 위 절차를 완료하면 본 테스트 묶음을 다시 실행하여 `test_api_contract_fuzz[*assets*]`, `test_backtest_lifecycle_*`, `test_concurrent_backtests_independent`, `test_run_hash_caching_returns_same_run`, `test_get_result_404_for_unknown_run`, `test_backtest_create_validation_error_422` 가 통과하는지 검증

### TASK-100 통합 시점

3. 데이터 로더 placeholder 제거 (`OhlcvRepository` → `align_universe_prices` → `prices_aligned` DataFrame 빌드) 후 `test_backtest_lifecycle_failed_due_to_data_loader_placeholder` 테스트는 status='done' 경로로 자동 전환되도록 분기 갱신

### Phase 2

4. 메트릭 robustness — vol_total 임계값 가드 추가 (O-002)
5. 워커 크래시 복구 — reaper 태스크 또는 Celery/Redis 도입 (O-003)

### 골든 테스트 갱신 정책

6. 데이터 로더 통합 후 시나리오 가격 시리즈를 실 시장 데이터 (yfinance/pykrx 캐시 fixture) 로 교체 권장 — 합성 데이터의 비현실적 Sharpe 회피
7. 갱신 시 `GOLDEN_UPDATE=1 pytest tests/golden/` 로 일괄 재생성 가능 (test 코드에 환경변수 hook 내장)
