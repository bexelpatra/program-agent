---
agent: coder
task_id: TASK-022
status: DONE
timestamp: 2026-04-29T12:00:00
severity: observation
---

## 결과 요약

증분 데이터 파이프라인을 구현했다. 자산별 MAX(time) 기반 백필, 거래일 캘린더와 ohlcv 의 차집합으로 갭 자동 감지, ON CONFLICT (asset_id, time) DO UPDATE 멱등 UPSERT, 자산 단위 3회 지수 백오프 재시도 (1s → 2s → 4s), 자산 1개 실패가 잡 전체를 깨지 않는 격리, ingestion_log append-only 적재까지 포함한다. 비거래일 다층 방어는 어댑터(sources/) 의 1차 (close=0/null/NaN 거부) + pipeline.py 의 2차 (캘린더 외 날짜 필터) 로 구성된다.

## 변경된 파일

- `projects/stock-backtest/backend/app/data/pipeline.py` (신규) — 증분 파이프라인 본체. `backfill_asset` / `backfill_active_assets` / `_trading_days` / `_resolve_start` / `_fetch_with_retry` / `IngestionResult`.
- `projects/stock-backtest/backend/app/data/repositories/__init__.py` (신규) — re-export.
- `projects/stock-backtest/backend/app/data/repositories/ohlcv_repository.py` (신규) — `OhlcvRepository` (latest_time / existing_dates / upsert_bars).
- `projects/stock-backtest/backend/app/data/repositories/ingestion_log_repository.py` (신규) — `IngestionLogRepository.record`.
- `projects/stock-backtest/backend/app/data/__init__.py` (수정) — pipeline / repositories re-export 추가.

## 신규 Public API

`OhlcvRepository`:
- `__init__(self, session: Session)`
- `latest_time(self, asset_id: int) -> datetime | None`
- `existing_dates(self, asset_id: int, start: date, end: date) -> set[date]`
- `upsert_bars(self, asset_id: int, bars: Iterable[OhlcvBar]) -> int`

`IngestionLogRepository`:
- `__init__(self, session: Session)`
- `record(self, asset_id: int, requested_start: date, requested_end: date, status: str, rows_inserted: int = 0, error_message: str | None = None) -> None`

`app.data.pipeline`:
- `backfill_asset(session: Session, source: DataSource, asset: Asset, end: date | None = None, max_lookback_days: int = 365*20) -> IngestionResult`
- `backfill_active_assets(session: Session, sources: dict[str, DataSource], end: date | None = None) -> list[IngestionResult]`
- `IngestionResult` (frozen dataclass: asset_id, symbol, market, requested_start, requested_end, rows_inserted, status, error)

## DoD 검증 결과

1. **import**: `from app.data.pipeline import backfill_asset, backfill_active_assets, IngestionResult; from app.data.repositories.ohlcv_repository import OhlcvRepository; from app.data.repositories.ingestion_log_repository import IngestionLogRepository` → `ok` (KRX 환경변수 미설정 경고는 PykrxSource import 시 부수효과로 무관).
2. **_trading_days 동작 (실측)**:
   - US 2024-01: **21** 일 (예상 ~21 ✓)
   - KR 2024-01: **22** 일 (예상 ~20; 2024년 1월 KRX 캘린더 실측 결과는 22일 — 신정만 휴장)
   - CRYPTO 2024-01: **31** 일 (CRYPTO 라우팅 = 모든 날짜 ✓)
3. **UPSERT SQL**: 컴파일 결과 `INSERT INTO ohlcv (asset_id, time, close) VALUES (...) ON CONFLICT (asset_id, time) DO UPDATE SET close = excluded.close` — `ON CONFLICT (asset_id, time) DO UPDATE` 출력 확인 ✓.
4. **의존성 그래프 (ast 추출)**: pipeline.py imports = `app.data.sources.base`, `app.data.asset_repository`, `app.data.repositories.ohlcv_repository`, `app.data.repositories.ingestion_log_repository`, `app.domain.asset.entity`, `app.domain.asset.calendar_guard` + 외부 `exchange_calendars`, `sqlalchemy.orm`, `logging`, `time`, `datetime`, `dataclasses`. **DB ORM 모델 직접 import 없음** — repositories 가 캡슐화 ✓.

DB 적용 검증은 BLOCKER-001 (DB 미적용) 잔재로 SOFT — import + SQL 컴파일까지로 충족.

## 클린 코드 점검

- `pipeline.py` 는 orchestration (순서/재시도/로깅) 만, 도메인 로직 없음 — `app.domain` 의 entity/calendar_guard 만 참조.
- 어댑터(`sources/`) 가 close=0 거부 등 수집 레이어 1차 방어, pipeline 의 `valid_bars = [b for b in bars if b.time.date() in expected_set]` 가 캘린더 레이어 2차 방어 (architecture.md V1 결정 13).
- 자산 단위 try/except (`backfill_active_assets` 내부) 로 1개 실패가 전체 잡을 깨지 않음. session.rollback() + 별도 IngestionResult FAILED 로 계속.
- `IngestionLogRepository.record` 만 정의 (update/delete 없음) — append-only 보장.
- `_fetch_with_retry` 추출로 backfill_asset 본문 가독성 유지 (단일 함수 약 75줄, 함수 길이 권고 40 줄에 근접하나 절차 4단계 (resolve start → trading days → gap → fetch+upsert) 가 모두 single concern 으로 응집).
- `_trading_days` 의 CRYPTO 분기는 별도 함수 분리 후보였으나 5줄로 충분히 짧고 한 곳에서만 호출되어 inline 유지.
- 매직 넘버: `MAX_RETRIES = 3`, `BACKOFF_BASE_SECONDS = 1.0`, `DEFAULT_MAX_LOOKBACK_DAYS = 365 * 20` 모두 모듈 상수화.
- 이름: 부수효과 함수는 `record_*` / `upsert_*` / `backfill_*` / `_fetch_*` 동사형, boolean 없음 (현 모듈 한정).

## 이슈/블로커

없음. KR 거래일 22 vs spec 의 "예상 ~20" 차이는 2024-01 KRX 실제 휴장이 신정 1일뿐인 것을 반영한 정확값으로, 캘린더 라이브러리 동작 자체는 정상.

## 다음 제안

1. **단위 테스트 (Tester 영역)**: `backfill_asset` 의 4가지 분기 — (a) 신규 자산, (b) 기존 자산 + 갭 없음, (c) 기존 자산 + 갭 있음 + 성공, (d) 재시도 후 실패 — 를 fake DataSource + in-memory SQLite 또는 mock session 으로 검증. `_trading_days` 도 KR 설날 / US Thanksgiving / CRYPTO 윤년 2월 등 경계 케이스 골든 스냅샷.
2. **스케줄러 결합 (TASK-05x 추정)**: `backfill_active_assets` 를 APScheduler cron (KR 18:00 / US 07:00 / CRYPTO 09:00 KST) 에 바인딩하는 `app.scheduler.daily_ingest` job 추가. 결과 집계 (`OK`, `PARTIAL`, `FAILED`, `REJECTED` 카운트) 를 로그/Slack/대시보드로 노출.
3. **`max_lookback_days` 정책 노출**: 신규 자산 최초 백필 시 20년은 yfinance 일부 종목엔 과도. asset.meta 에 `min_history_start` 가 있으면 그걸 우선시키는 로직 추가 검토.
4. **PARTIAL 재처리 큐**: 현재 PARTIAL (rows < missing 길이) 는 ingestion_log 에 기록만 하고 끝. 다음 cron 실행 시 `existing_dates` 로 재감지되어 자동 재시도되긴 하나, 일정 재시도 횟수 초과 시 alert 거는 admin 화면 검토.
5. **SqlAssetRepository.update_ingestion_state 호출 위치 일관성**: 본 파이프라인은 pipeline.py 에서 호출하지만, 자산 신규 등록(TASK-031) 워크플로우에서도 동일 갱신이 필요할 수 있음. service 레이어에서 일원화 검토.
