---
agent: coder
task_id: TASK-061
status: DONE
timestamp: 2026-04-29T00:00:00
severity: observation
---

## 결과 요약

자산/전략 API 를 구현했다.

- **자산 API** (`/api/assets`): 카탈로그 검색 / 단건 상세 / 자유 추가 (POST → TASK-031 `register_asset`) / OHLCV 조회
- **전략 API** (`/api/strategies`): allocator 3종 + filter 2종 목록 + 각 전략 pydantic params JSON Schema (UI 폼 자동 생성용)
- **DI 헬퍼** (`app/dependencies.py`): `get_db` / `get_asset_repo` / `get_ohlcv_repo`
- **MVP 어댑터**: `_RoutingValidator` (TickerValidator Protocol → market 별 yfinance/pykrx 라우팅) + `_LoggingEnqueuer` (BackfillEnqueuer Protocol placeholder, 실제 큐 연결은 TASK-070+)
- HTTP 매핑: 422 (검증 실패) / 409 (중복) / 404 (미존재) / 201 (생성)
- 모든 4xx/5xx 는 TASK-060 의 ErrorResponse 계약 (`stage`/`type`/`message`/`request_ctx`/`trace_id`) 으로 통일됨

## 변경된 파일

- `projects/stock-backtest/backend/app/dependencies.py` (신규)
- `projects/stock-backtest/backend/app/schemas/asset.py` (신규)
- `projects/stock-backtest/backend/app/schemas/strategy.py` (신규)
- `projects/stock-backtest/backend/app/api/assets.py` (신규)
- `projects/stock-backtest/backend/app/api/strategies.py` (신규)
- `projects/stock-backtest/backend/app/api/__init__.py` (수정 — `assets_router` / `strategies_router` re-export append)
- `projects/stock-backtest/backend/app/main.py` (수정 — `include_router(assets_router)` / `include_router(strategies_router)` 2줄 추가)

TASK-060 의 `health.py` / `_error.py` / `schemas/common.py` 는 일절 손대지 않음.

## 신규 public API

### REST 엔드포인트

| Method | Path                              | Response                                   |
|--------|-----------------------------------|--------------------------------------------|
| GET    | `/api/assets`                     | `PaginatedResponse[AssetRead]`             |
| POST   | `/api/assets`                     | `AssetCreateResponse` (201)                |
| GET    | `/api/assets/{asset_id}`          | `AssetRead`                                |
| GET    | `/api/assets/{asset_id}/ohlcv`    | `list[OhlcvPoint]`                         |
| GET    | `/api/strategies`                 | `StrategyListResponse`                     |

### 스키마 (`app.schemas.asset` / `app.schemas.strategy`)

- `AssetRead`, `AssetCreate`, `AssetSearchQuery`, `OhlcvPoint`, `AssetCreateResponse`
- `StrategyDescriptor`, `StrategyListResponse`

### DI 헬퍼 (`app.dependencies`)

- `get_db() -> Iterator[Session]`
- `get_asset_repo(session: Session) -> SqlAssetRepository`
- `get_ohlcv_repo(session: Session) -> OhlcvRepository`

## DoD 결과

### 1. import + routes 확인

```
$ python -c "from app.main import app; print(sorted([r.path for r in app.routes if hasattr(r, 'path')]))"
['/api/assets', '/api/assets', '/api/assets/{asset_id}',
 '/api/assets/{asset_id}/ohlcv', '/api/docs', '/api/health',
 '/api/openapi.json', '/api/strategies', '/docs/oauth2-redirect', '/redoc']
```

목표 5개 엔드포인트 모두 등록됨.

### 2. 서버 기동 + 엔드포인트 응답

`uvicorn app.main:app --port 18002` 백그라운드 기동 후:

- `GET /api/strategies` → 200, allocators 3 + filters 2, 각 schema 의 properties/required 정상:
  ```
  allocator: fixed_weight         props=['weights']                              required=['weights']
  allocator: all_weather          props=['category_weights', 'asset_categories'] required=['asset_categories']
  allocator: equal_weight         props=[]                                       required=[]
  filter:    moving_average       props=['window', 'price_above']                required=['window']
  filter:    momentum             props=['lookback', 'threshold']                required=[]
  ```

- `GET /api/assets?limit=5` → 500 ErrorResponse — **BLOCKER-001 잔재 (DB 컬럼 누락)** 로 SOFT 처리. 서버 자체 동작은 정상이며 ErrorResponse 형식도 정상:
  ```json
  {"error": {"stage":"internal", "type":"ProgrammingError",
   "message":"서버 내부 오류가 발생했습니다. trace_id 로 지원에 문의하세요.",
   "request_ctx": {"path":"/api/assets","method":"GET","query":{"limit":"5"}},
   "trace_id":"4f3af08748ed4a518f96829ae3b1f639"}}
  ```
  서버 로그(stacktrace) 확인:
  ```
  sqlalchemy.exc.ProgrammingError: (psycopg2.errors.UndefinedColumn)
    column assets.created_at does not exist
  ```
  task spec 명시: "DB 가 BLOCKER-001 잔재로 인해 `select assets ...` SQL 이 실패할 수 있음. 그 경우 SOFT — endpoints 등록 + JSON Schema 생성까지가 핵심." → 충족.

- `POST /api/assets` 검증 실패 (필드 누락) → 422 ErrorResponse `stage='validation'`:
  ```json
  {"error": {"stage":"validation", "type":"RequestValidationError",
   "message":"요청 본문/쿼리가 스키마를 만족하지 않습니다.",
   "request_ctx": {"path":"/api/assets","method":"POST","query":{},
                   "errors":[{"type":"missing","loc":["body","currency"],...}]},
   "trace_id":"1ba7414a34fc4d98b2f4b2d60ff52376"}}
  ```
  Pydantic 검증 → 전역 핸들러 → ErrorResponse 흐름이 살아있음. 실제 ticker 검증 422 는 BLOCKER-001 SQL 이 먼저 실패하므로 도달 불가 (DB 마이그레이션 후 자동 통과 예상).

- `GET /api/assets/999999` → 500 (BLOCKER-001 동일 원인). DB 정상화 시 404 로 자동 전환 (`repo.find_by_id is None` 분기).

### 3. JSON Schema 검증

```
$ curl -s http://localhost:18002/api/strategies | python -c "..."
allocators: ['fixed_weight', 'all_weather', 'equal_weight']
filters: ['moving_average', 'momentum']
```

5개 전략 이름 모두 노출. 각 params_schema 는 pydantic v2 `model_json_schema()` 산출 그대로 (UI Zod 검증과 동기 가능).

### 4. openapi.json 신규 엔드포인트 반영

```
$ curl -s http://localhost:18002/api/openapi.json | python -c "..."
paths: ['/api/assets', '/api/assets/{asset_id}',
        '/api/assets/{asset_id}/ohlcv', '/api/health', '/api/strategies']

components.schemas (기여한 신규):
  AssetCreate, AssetCreateResponse, AssetRead, OhlcvPoint,
  StrategyDescriptor, StrategyListResponse, PaginatedResponse_AssetRead_
```

TASK-060 의 `ErrorDetail` / `ErrorResponse` / `HealthResponse` / `PaginatedResponse` / `TimestampedModel` 도 그대로 보존됨.

## 클린 코드 / 클린 아키텍처 점검

- **계층 의존**: `api/` → `domain/` + `data/` 만 의존. domain 은 HTTP 무관. 라우터에서만 `HTTPException` 사용.
- **SRP / 모듈 분리**: 라우터(assets/strategies/health), 스키마(asset/strategy/common), DI(dependencies) 모두 독립 모듈.
- **DI 패턴**: `Depends(get_db)` 로 세션 주입 → repository 생성 → 단일 트랜잭션 boundary. 라우터가 객체 생성 책임 가짐.
- **Protocol 어댑터**: `_RoutingValidator` / `_LoggingEnqueuer` 가 TASK-031 의 `TickerValidator` / `BackfillEnqueuer` Protocol 을 명시적 구현. domain 은 source 타입을 누설받지 않음 (`TickerValidation` → `ValidationOutcome` 변환).
- **HTTP 상태 매핑** (코더 가이드 § 8 "오류 처리 — 경계에서만"): 422/409/404/201 매핑이 라우터에서만, domain 예외(`AlreadyRegistered`, `TickerValidationFailed`)는 domain 에 머무름.
- **이름**: 변환 헬퍼 `_to_read`, `_decimal_or_none` 으로 의도 드러냄. 매직 넘버 없음.
- **소스 길이**: assets.py 224줄 — 네 가지 엔드포인트 + 어댑터 2개 + 헬퍼 2개. 책임 응집도 OK (분리 시 어댑터를 별 모듈로 옮길 수 있으나 현재 사용처가 본 라우터 1곳뿐이라 단일 파일 유지가 더 명확).

## 이슈 / 블로커

- **BLOCKER-001 잔재 (SOFT)**: `assets.created_at` / `updated_at` 컬럼이 DB 에 없어 `SqlAssetRepository.search` / `find_by_id` / `find_by_symbol_market` SQL 모두 `ProgrammingError` 발생. 본 태스크 범위는 endpoints 등록 + JSON Schema 노출까지로 spec 명시 → SOFT 진행. 마이그레이션 (alembic revision 생성) 또는 `models/_base.py` 의 `TimestampedModel` 컬럼을 nullable + server_default + 마이그레이션 적용 필요. 후속 별도 태스크 권장 — 본 태스크 범위 외.

- **`SimpleEnqueuer` placeholder**: `_LoggingEnqueuer` 는 로깅만 한다. 실제 비동기 백필 큐 (TASK-070+) 가 들어오면 `app.state.backfill_queue` 등 lifespan 주입으로 교체 필요. 그때까지는 자유 추가된 자산은 다음 cron 주기 (V1 결정 9) 에 자동 백필됨.

- **`OhlcvRepository` 는 DI 만 마련하고 라우터에서 직접 ORM 쿼리 사용**: OHLCV 조회 1곳에서만 사용되며 시계열 SELECT 는 단순한 단발 쿼리라 repository 우회. 향후 OHLCV 조회 패턴이 늘어나면 `repo.fetch_range(asset_id, start, end)` 메서드 추가 권장.

## 다음 제안

- **TASK-062 (제안)**: 백테스트 API 비동기 job 모델. `POST /api/backtests` → `{run_id, status:"pending"}` 즉시 반환, FastAPI `BackgroundTasks` 또는 별도 워커가 엔진 실행. 진행률은 `backtest_runs.progress` (0~1) 컬럼 추가 후 폴링. 취소 / 워커 크래시 복구 / 동시 job 독립성 검증 포인트는 architecture.md V2 § "비동기 job 실행 모델" 참조.

- **BLOCKER-001 처리 별도 태스크**: alembic 으로 `created_at` / `updated_at` 컬럼 추가 마이그레이션. 또는 (단순화) `models/_base.py` 의 `TimestampedModel` 을 `assets` 에서 빼고 명시적 nullable timestamp 컬럼만 두는 방식 검토.

- **OHLCV 조회 repository 메서드 추가** (선택): `OhlcvRepository.fetch_range(asset_id, start, end) -> list[Ohlcv]` 를 추가하면 라우터의 ORM 직접 쿼리를 제거할 수 있어 도메인 레이어 일관성 향상.

- **`/api/assets` total 카운트**: 현재 `total=len(items)` 로 페이지 내 카운트만. 정확한 total 은 `repo.count(...)` 별도 쿼리 필요. UI 페이지네이션 도입 시 추가.
