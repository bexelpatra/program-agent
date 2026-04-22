# Tester Report — TASK-033: 수집 복구 시나리오 엔드투엔드 테스트

## 상태
- **Status**: DONE
- **테스트 결과**: 6 passed, 0 failed, 0.48s

## 작성 파일
- 신규: `projects/stock-backtest/tests/test_ingestion_e2e.py`

## 테스트 접근 방식

- **인-메모리 DB 흉내**: `_State` dataclass 가 `ohlcv`(dict keyed by (asset_id, time)), `ingestion_log`(append-only list), `assets`(dict) 를 보유. `MAX(time)` 도 이 dict 에서 계산.
- **Repository 패치**: `stock_backtest.ingestion.pipeline` 모듈의 `OhlcvRepository`, `IngestionLogRepository`, `AssetRepository` 를 `MagicMock` 으로 교체하되, 각 메서드의 `side_effect` 를 동일한 `_State` 인스턴스에 연결된 콜백으로 설정 → 두 번 이상의 파이프라인 호출이 **실제 DB처럼 상태를 공유**한다.
- **Calendar 패치**: `get_trading_days` 를 월~금 business-day 로 대체 (`_weekday_trading_days`). `exchange_calendars` 의존 제거.
- **Source**: `MagicMock(spec=DataSource)`. run 간 `fetch_ohlcv.side_effect`/`return_value` 를 재세팅하여 호출 순서에 따라 다른 응답을 돌려줌.
- **Sleep 주입**: `sleep_fn=lambda _: None` 으로 지수백오프 대기 시간 제거.
- **세션**: `_FakeSession` 이 `commit`/`rollback`/`close` 카운팅.

## 커버 매트릭스

| # | 시나리오 | 테스트 | 결과 |
|---|----------|--------|------|
| E2E-1 | 3회 실패 후 다음 run 에서 전 범위 복구 | `test_e2e_1_failure_then_gap_recovery` | PASS — Run A FAILED/ohlcv 0행/MAX=None → Run B 에서 MAX=None 기반으로 `start_date=2024-01-05` 부터 5 거래일 재요청, SUCCESS, ohlcv 5행, FAILED+SUCCESS 로그 둘 다 존재 |
| E2E-2 | 부분 응답 → 다음 run 에서 나머지 수집 | `test_e2e_2_partial_then_recovery` | PASS — Run A 4 거래일 중 3행만 반환 → PARTIAL (gap 감지), MAX=01-09. Run B 가 MAX+1=01-10 부터 요청하여 2행 추가, 최종 5 거래일 커버 |
| E2E-3 | 동일 범위 즉시 재실행 (멱등) | `test_e2e_3_idempotent_replay` | PASS — Run A SUCCESS(2행), Run B 는 MAX=today 여서 start>end 단락 → SUCCESS(0), ohlcv row count 불변, source 미호출 |
| E2E-4 | RateLimitError → 다음 run 회복 | `test_e2e_4_ratelimit_then_recovery` | PASS — Run A RateLimit 3회 재시도 → FAILED, Run B 정상, 전 범위(4 거래일) 삽입 |
| E2E-5 | 멀티 자산 중 B 만 실패 → 다음 run 복구 | `test_e2e_5_multi_asset_partial_market_failure` | PASS — `run_for_market("US")` 결과 SUCCESS/FAILED/SUCCESS, A·C 는 ohlcv 2행 씩, B 는 0행. Run B 에서 B 만 재시도되어 SUCCESS(2행), A·C 는 up-to-date 라 no-op |
| E2E-6 | close=0 섞인 응답 → REJECTED, 다음 run 에서 후속 날짜 수집 | `test_e2e_6_close_zero_then_recovery` | PASS — Run A 4 거래일 중 01-09 close=0 → REJECTED 로그 + PARTIAL(3행). MAX 는 **가장 최근 UPSERT 된 good row 기준** = 01-10. Run B (today=01-11) 가 MAX+1=01-11 를 요청하여 01-11 1행 추가 |

## pytest 출력

```
$ pytest tests/test_ingestion_e2e.py -v
============================= test session starts ==============================
platform linux -- Python 3.11.3, pytest-9.0.2
configfile: pyproject.toml
collecting ... collected 6 items

tests/test_ingestion_e2e.py::test_e2e_1_failure_then_gap_recovery              PASSED [ 16%]
tests/test_ingestion_e2e.py::test_e2e_2_partial_then_recovery                  PASSED [ 33%]
tests/test_ingestion_e2e.py::test_e2e_3_idempotent_replay                      PASSED [ 50%]
tests/test_ingestion_e2e.py::test_e2e_4_ratelimit_then_recovery                PASSED [ 66%]
tests/test_ingestion_e2e.py::test_e2e_5_multi_asset_partial_market_failure     PASSED [ 83%]
tests/test_ingestion_e2e.py::test_e2e_6_close_zero_then_recovery               PASSED [100%]

============================== 6 passed in 0.48s ===============================
```

> 주의: 로컬 환경에서 `dash` 관련 pytest 플러그인의 `comm.create_comm` 이 `NotImplementedError` 를 던지는 문제가 관측되어 `-p no:dash` 옵션을 붙여 실행했다. 테스트 로직과는 무관한 환경 이슈 (ipykernel comm 미설치). 동일한 이슈는 기존 다른 테스트 실행 시에도 동일하게 발생할 것으로 예상되며, 파이프라인/테스트 자체의 결함이 아니다.

## 이슈/블로커
없음.

## 코드 이슈

### 관찰 (참고 — 수정 강제 없음)

E2E-6 에서 드러난 설계상 **미묘한 엣지**:

- `close=0` 행이 응답 중간(예: 01-09)에 있을 때, 해당 날짜는 REJECTED 되고 뒤따르는 good row (01-10) 는 정상 UPSERT 된다.
- 그 결과 `MAX(ohlcv.time) = 2024-01-10` 이 되므로 **다음 run 은 01-11 부터 요청**하며, REJECTED 당한 01-09 는 자동으로 재요청되지 않는다.
- 즉 "품질 불량으로 거부된 날짜" 의 재시도는 현재 파이프라인의 `MAX(time)+1` 전략만으로는 커버되지 않고, architecture.md §9 "매 실행 시작 시 ... 갭 자동 감지·재수집" 에 별도로 언급된 **갭 스캐너 (트레이딩 캘린더 ↔ ohlcv 실측 비교)** 가 구현되어야 복구된다.

현재 파이프라인 구현은 이 경우 PARTIAL 상태와 REJECTED 로그를 남겨 추적 가능하게 해 두었으므로, 후속 "갭 스캐너" 태스크에서 `ingestion_log.status IN ('REJECTED','PARTIAL')` 이거나 트레이딩 캘린더와의 불일치를 감지해 좁은 범위 재요청을 트리거하면 된다. 본 E2E 테스트는 **현재 계약** 을 명문화해 테스트로 고정했다 (E2E-6 의 `times == {01-05, 01-08, 01-10, 01-11}`, 01-09 가 빠져 있음을 검증).

기타 5개 시나리오(E2E-1~5) 는 `MAX(time)+1` 전략만으로 완전한 복구가 이루어짐을 확인했다.

## 금지사항 준수
- `src/` 수정 없음.
- `task-board.md`, `architecture.md` 수정 없음.
- `web/pages/seasonality.py`, `web/pages/history.py` 접근 없음.
- `tests/test_ingestion_e2e.py` 신규 1개 파일만 작성.
