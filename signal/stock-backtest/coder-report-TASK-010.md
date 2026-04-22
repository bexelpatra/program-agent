# Coder Report — TASK-010: 수집 파이프라인

## 상태
- **Status**: DONE

## 작업 요약

`src/stock_backtest/ingestion/pipeline.py` 를 신규 작성하고, `data/repository.py` 에 파이프라인에서 필요한 편의 함수를 추가했다.

## 파일 변경 내역

### 신규 파일
- `projects/stock-backtest/src/stock_backtest/ingestion/pipeline.py`
  - `IngestionResult` dataclass: `asset_id`, `status ∈ {SUCCESS, PARTIAL, FAILED, SKIPPED}`, `rows_inserted`, `rows_rejected`, `error_message`, `requested_start`, `requested_end`.
  - `IngestionPipeline` 클래스:
    - `__init__(sources: Mapping[str, DataSource], session_factory, settings, *, today_fn=None, sleep_fn=None)` — `sources` 는 `market` 키 또는 `source_name` 키 모두 허용, `asset.meta["source"]` 힌트도 인식. 단일 source 등록 시 자동 기본 사용.
    - `run_for_asset(asset) -> IngestionResult` — 자산 단위 증분 수집. 예외 완전 격리.
    - `run_for_market(market) -> list[IngestionResult]` — 해당 market 의 active 자산 전체 순회.
  - 로직 구현:
    1. `MAX(ohlcv.time) + 1일` 부터 오늘까지 요청 범위 산정 (초기 수집 시 `asset.start_date` 또는 20년 백필 기본).
    2. `backtest.calendar.get_trading_days(calendar_market, start, end)` 로 거래일 필터. CRYPTO 는 365일 전부 거래일.
    3. `fetch_ohlcv` 호출에 대해 `settings.ingestion.retry_backoff_seconds` (기본 `[1, 2, 4]`) 지수 백오프 최대 3회 재시도. `RateLimitError`·`DataSourceError` 재시도, `SymbolNotFoundError` 즉시 SKIPPED.
    4. 품질 필터: `close` 가 `None`/`NaN`/`0`/비수치면 제외 → `ingestion_log.status='REJECTED'` 로 (asset_id + 거부된 날짜 범위 + 사유 set) 기록.
    5. 갭 = 거래일 수 > 수집 행 수 → `PARTIAL`. `MAX(time)` 이 전진하지 않은 거래일은 다음 실행에서 자연 재요청.
    6. 성공 행을 `ohlcv` 에 UPSERT, `ingestion_log.status='SUCCESS'|'PARTIAL'` 기록, `assets.last_ingested_at` = `now(UTC)` 갱신.
    7. 예외는 자산 단위로 `ingestion_log.error_message` 에 기록되고, 잡 전체는 계속 진행.
  - 캘린더 매핑 (`_CALENDAR_MARKET_MAP`): `KR/KRX/KOSPI/KOSDAQ→KR`, `US/NYSE/NASDAQ→US`, `CRYPTO→CRYPTO`, 기타 → SKIPPED + FAILED 로그.
  - 세션 관리: `session_factory()` 반환이 일반 `Session` 또는 컨텍스트매니저 둘 다 지원. 모든 DB 작업은 try/except/finally 로 rollback·close 보장. UPSERT + log + last_ingested_at 갱신은 동일 트랜잭션에서 커밋.
  - `logging` 전용 (print 없음), 타입 힌트·docstring 완비.

### 수정 파일
- `projects/stock-backtest/src/stock_backtest/data/repository.py`
  - 태스크 요구 시그니처에 맞춘 **모듈-레벨 편의 함수**를 파일 끝에 추가 (기존 클래스/시그니처는 변경하지 않음):
    - `get_max_ohlcv_time(session, asset_id) -> datetime | None`
    - `upsert_ohlcv_bulk(session, asset_id, rows) -> int`  (기존 `OhlcvRepository.upsert_bulk` 위임)
    - `log_ingestion(session, asset_id, status, rows, start, end, error=None) -> IngestionLog`
    - `list_active_assets(session, market=None) -> list[Asset]`

> 파이프라인 구현은 기존 Repository 클래스(`OhlcvRepository`, `IngestionLogRepository`, `AssetRepository`) 를 직접 사용하고, 위 모듈 함수들은 태스크가 요구한 시그니처를 노출하기 위한 얇은 wrapper 이다.

## 추가한 Repository 메서드 (요구사항 체크리스트)

| 요구 시그니처 | 위치 | 메모 |
|---|---|---|
| `get_max_ohlcv_time(asset_id) -> datetime | None` | `repository.py` 모듈 함수 `get_max_ohlcv_time(session, asset_id)` | 기존 `OhlcvRepository.get_max_time` 위임 |
| `upsert_ohlcv_bulk(rows)` | `repository.py` 모듈 함수 `upsert_ohlcv_bulk(session, asset_id, rows)` | **이미 존재** — 기존 `OhlcvRepository.upsert_bulk` 사용 |
| `log_ingestion(asset_id, status, rows, start, end, error=None)` | `repository.py` 모듈 함수 | 기존 `IngestionLogRepository.log` 위임 |
| `list_active_assets(market: str | None = None)` | `repository.py` 모듈 함수 | 기존 `AssetRepository.list_active` 위임 |

## 완료 조건 충족 확인

- `from stock_backtest.ingestion.pipeline import IngestionPipeline` 정상:
  ```
  PYTHONPATH=src python -c "from stock_backtest.ingestion.pipeline import IngestionPipeline, IngestionResult; \
      from stock_backtest.data.repository import get_max_ohlcv_time, upsert_ohlcv_bulk, log_ingestion, list_active_assets; \
      print('OK')"
  → OK
  ```
- 필요한 repository 함수 4종 모두 존재.
- 실제 DB 실행은 수행하지 않았음 (테스트 DB 미기동 환경). 코드 검증 통과.

## 금지 사항 준수

- `task-board.md`, `architecture.md`, `tests/` 미수정.
- `backtest/tax.py` 접근 없음.
- 기존 repository 시그니처 변경 없음 — 모듈 함수만 **추가**.
- 그 외 기존 파일 불필요 수정 없음.

## 참고 동작 요약 (상태 매트릭스)

| 상황 | Result.status | ingestion_log |
|---|---|---|
| 거래일 = 수집 행 수, rejected=0 | `SUCCESS` | SUCCESS |
| 거래일 = 수집 행 수, rejected>0 | `PARTIAL` | SUCCESS + 별도 REJECTED 로그 |
| 거래일 > 수집 행 수 (갭) | `PARTIAL` | PARTIAL (`error_message`에 gap 설명) |
| MAX(time) ≥ today (최신) | `SUCCESS` (rows=0) | 없음 |
| 요청 범위에 거래일 없음 | `SUCCESS` (rows=0) | 없음 |
| `SymbolNotFoundError` | `SKIPPED` | FAILED |
| 캘린더 매핑 실패 | `SKIPPED` | FAILED |
| source 미등록 | `SKIPPED` | FAILED |
| 재시도 소진 (RateLimit/DataSource) | `FAILED` | FAILED |
| 예상 외 예외 | `FAILED` | FAILED (best-effort) |
