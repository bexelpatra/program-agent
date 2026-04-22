# Tester Report — TASK-012: 수집 파이프라인 단위/통합 테스트

## 상태
- **Status**: DONE
- **테스트 결과**: 11 passed, 0 failed, 0.49s

## 작성 파일
- 신규: `projects/stock-backtest/tests/test_ingestion_pipeline.py`
- (conftest.py 는 불필요하여 추가하지 않음 — 테스트 파일 내부에 fixture/helper 를 모두 국지화.)

## 테스트 접근 방식

- **No network, no DB**: `DataSource` 는 `MagicMock(spec=DataSource)`, Repository 3종(`OhlcvRepository`, `IngestionLogRepository`, `AssetRepository`)은 `unittest.mock.patch` 로 파이프라인 모듈 임포트 지점에서 교체.
- **Calendar 결정성**: `stock_backtest.ingestion.pipeline.get_trading_days` 를 월~금 business-day 로 돌려주는 fake 함수(`_weekday_trading_days`)로 패치 → 실제 `exchange_calendars` 비의존.
- **Session 추상**: `_FakeSession` 이 `commit`/`rollback`/`close` 호출 수를 카운트.
- **Sleep 주입**: `sleep_fn=list.append` 로 backoff 값을 그대로 캡처 (시간 소모 0, 백오프 수열 검증 가능).

## 커버 매트릭스 (요구사항 대응)

| # | 요구 | 테스트 | 결과 |
|---|------|--------|------|
| 1 | 정상 증분 (MAX+1..today) | `test_incremental_from_max_time_plus_one` | PASS — `start=2024-01-06`, `end=2024-01-10`, UPSERT 1회 3행, SUCCESS 로그, `update_last_ingested` 1회, commit 1회 |
| 2 | 빈 DB (MAX=None → start_date) | `test_first_backfill_uses_asset_start_date` | PASS — `asset.start_date` 가 요청 start 로 사용됨 |
| 3 | 재시도 지수백오프 | `test_retry_then_success_calls_sleep_with_backoff` | PASS — 2회 실패 후 3회차 성공, `fetch_ohlcv.call_count==3`, `sleeps==[1.0, 2.0]` |
| 4 | 3회 전부 실패 | `test_three_failures_yield_failed_status_and_log` | PASS — `FAILED`, 예외 전파 없음, UPSERT 미호출, FAILED 로그 기록 |
| 5 | RateLimitError 분류 | `test_ratelimit_error_logged_with_rate_limit_message` | PASS — `error_message` 에 "rate limit" 포함, 3회 재시도 동일 로직 |
| 6 | close=0/NaN/None REJECTED | `test_rejects_invalid_close_and_logs_rejected` | PASS — 5행 중 3행 REJECTED, UPSERT 2행, REJECTED 로그 1건 + PARTIAL 로그 1건 |
| 7 | 멱등성 | `test_idempotent_upsert_on_repeat_run` | PASS — 두 번 실행 시 각 SUCCESS, UPSERT 2회(페이로드 동일 크기) — 실제 중복 방지는 `ON CONFLICT DO UPDATE` 책임이고 파이프라인 계약은 "재호출해도 예외 없이 같은 페이로드를 UPSERT 한다" 임을 검증 |
| 8 | 비거래일 필터 | `test_weekend_only_range_skipped_without_datasource_call` | PASS — 금요일 MAX + 일요일 today → 거래일 0 → DataSource 미호출, SUCCESS(0) |
| 9 | 갭 복구 | `test_gap_recovery_uses_max_time_plus_one_on_next_run` | PASS — MAX=1/3 이면 다음 run 이 1/4 부터 요청 |
| 10 | run_for_market (부분 실패 격리) | `test_run_for_market_isolates_failures_per_asset` | PASS — QQQ 실패, SPY/IWM 성공, 결과 list 길이 3 |
| 추가 | SymbolNotFound 즉시 SKIPPED | `test_symbol_not_found_skipped_without_retry` | PASS — 재시도 없이 1회 호출 |

## pytest 출력 (요약)

```
$ pytest tests/test_ingestion_pipeline.py -v
platform linux -- Python 3.11.3, pytest-9.0.2
rootdir: /home/jai/program-agent/projects/stock-backtest
configfile: pyproject.toml
collecting ... collected 11 items

tests/test_ingestion_pipeline.py::test_incremental_from_max_time_plus_one            PASSED [  9%]
tests/test_ingestion_pipeline.py::test_first_backfill_uses_asset_start_date          PASSED [ 18%]
tests/test_ingestion_pipeline.py::test_retry_then_success_calls_sleep_with_backoff   PASSED [ 27%]
tests/test_ingestion_pipeline.py::test_three_failures_yield_failed_status_and_log    PASSED [ 36%]
tests/test_ingestion_pipeline.py::test_ratelimit_error_logged_with_rate_limit_message PASSED [ 45%]
tests/test_ingestion_pipeline.py::test_rejects_invalid_close_and_logs_rejected       PASSED [ 54%]
tests/test_ingestion_pipeline.py::test_idempotent_upsert_on_repeat_run               PASSED [ 63%]
tests/test_ingestion_pipeline.py::test_weekend_only_range_skipped_without_datasource_call PASSED [ 72%]
tests/test_ingestion_pipeline.py::test_gap_recovery_uses_max_time_plus_one_on_next_run PASSED [ 81%]
tests/test_ingestion_pipeline.py::test_run_for_market_isolates_failures_per_asset    PASSED [ 90%]
tests/test_ingestion_pipeline.py::test_symbol_not_found_skipped_without_retry        PASSED [100%]

============================== 11 passed in 0.49s ==============================
```

## 이슈/블로커
없음.

## 코드 이슈
없음. 파이프라인 구현은 TASK-012 스펙에 대응하는 모든 동작을 정상 수행한다.

### 관찰 사항 (참고, 수정 불필요)
- 멱등성 계약은 파이프라인 레이어 자체가 아니라 `OhlcvRepository.upsert_bulk` 의 `ON CONFLICT ... DO UPDATE` 에 의존한다. 현재 테스트는 Repository 를 모킹하여 파이프라인이 반복 호출 시 예외 없이 동일 페이로드로 UPSERT 를 시도함만 확인한다. 실제 DB 중복 회피 검증은 DB 통합 테스트(후속 태스크)에서 커버하는 것이 자연스럽다.
- 거래일 캘린더는 `get_trading_days` 를 패치해 테스트한다. 실제 `exchange_calendars` 연동 검증은 `test_calendar_guard.py` (기존) 에서 별도로 수행 중.

## 금지사항 준수
- `task-board.md`, `architecture.md` 미수정.
- `src/` 하위 파일 미수정.
- `tests/test_performance.py`, `tests/test_static_strategies.py` 접근 없음.
- `tests/test_ingestion_pipeline.py` 신규 1개 파일만 작성.
