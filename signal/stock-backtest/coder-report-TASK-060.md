---
agent: coder
task_id: TASK-060
status: DONE
timestamp: 2026-04-29T08:01
---

# TASK-060: docs/openapi.yaml 초안 + FastAPI 스캐폴드 + 전역 예외 핸들러 + 공통 base 스키마

## 요약

V3 architecture.md V2 § "에러 응답 계약" (L450~) 을 준수하는 FastAPI 백엔드 스캐폴드를 구축했다.
`GET /api/health` 엔드포인트, 4xx/5xx 통합 예외 핸들러 (stage/type/message/request_ctx/trace_id),
cross-endpoint base 스키마(ErrorResponse/ErrorDetail/PaginatedResponse/TimestampedModel/HealthResponse),
OpenAPI 3.1.0 사양 yaml 초안을 작성했다.

TASK-002 와의 충돌 회피 (`core/` 미터치) 위해 전역 예외 핸들러는 `backend/app/api/_error.py` 로 배치.

## 변경된 파일

### 신규 (/home/jai/pa/stock-backtest/projects/stock-backtest/)

- `backend/app/main.py` — FastAPI 앱 팩토리 (`create_app()`). CORS(localhost:3000), 예외 핸들러 등록, health 라우터 include, OpenAPI 커스터마이저로 base 스키마 강제 노출.
- `backend/app/api/__init__.py` — `add_exception_handlers`, `health_router` re-export.
- `backend/app/api/_error.py` — 전역 예외 핸들러 (StarletteHTTPException / RequestValidationError / Exception). trace_id=uuid4 hex 생성, request_ctx={path, method, query}, 서버 logger 로 `trace_id=... stage=... ctx=... status=... exc=...` 접두사 + stacktrace.
- `backend/app/api/health.py` — `GET /api/health` (HealthResponse 반환). `COMMON_ERROR_RESPONSES` 상수로 400/422/500 ErrorResponse 응답 스키마 노출 (후속 라우터에서 import 사용 가능).
- `backend/app/schemas/common.py` — Cross-endpoint base 스키마 5종:
  - `ErrorDetail` (frozen): stage/type/message/request_ctx/trace_id.
  - `ErrorResponse` (frozen): `{error: ErrorDetail}` wrapper.
  - `PaginatedResponse[T]` (Generic): items/total/page/page_size.
  - `TimestampedModel`: created_at/updated_at mixin.
  - `HealthResponse`: status:Literal["ok"], version:str.
- `docs/openapi.yaml` — OpenAPI 3.1.0 초안. info.title="Quant Lab API" version=0.1.0, `GET /api/health` 만 paths 등재, components.schemas 에 ErrorResponse/ErrorDetail/HealthResponse/PaginatedResponse 정의. 후속 TASK-061/062 가 paths 추가.

### 미변경 (TASK-002 영역 회피 확인)

- `backend/app/core/` — 건드리지 않음. TASK-002 가 작성한 `config.py`(1002B), `db.py`(1086B) 그대로.
- `backend/alembic/` — 건드리지 않음.

## 완료 검증 (DoD) — 전부 통과

| # | 검증 | 결과 |
|---|------|------|
| 1 | `python -c "from app.main import app; print([r.path for r in app.routes])"` 에 `/api/health` 포함 | PASS — `['/api/openapi.json', '/api/docs', '/docs/oauth2-redirect', '/redoc', '/api/health']` |
| 2 | `curl http://localhost:18001/api/health` → `{"status":"ok","version":"0.1.0"}` | PASS — exact match |
| 3 | `curl http://localhost:18001/api/nonexistent` → ErrorResponse + trace_id | PASS — `{"error":{"stage":"/api/nonexistent","type":"HTTPException","message":"Not Found","request_ctx":{"path":"/api/nonexistent","method":"GET","query":{}},"trace_id":"2a6ba4e4ee73496f8895a0b16e77d607"}}` |
| 4 | `curl /api/openapi.json \| jq '.components.schemas \| keys'` → ErrorResponse, ErrorDetail, HealthResponse, PaginatedResponse 포함 | PASS — `['ErrorDetail', 'ErrorResponse', 'HealthResponse', 'PaginatedResponse', 'TimestampedModel']` |
| 5 | `python -c "import yaml; yaml.safe_load(open('docs/openapi.yaml'))"` 파싱 성공 | PASS — 4개 base schema 모두 yaml 에 포함 확인 |

서버 로그 샘플 (DoD 3 케이스):
```
2026-04-29 08:00:19,279 ERROR app.api.error trace_id=2a6ba4e4ee73496f8895a0b16e77d607 stage=/api/nonexistent ctx={'path': '/api/nonexistent', 'method': 'GET', 'query': {}} status=404 exc=HTTPException
Traceback (most recent call last):
  ...
starlette.exceptions.HTTPException: 404: Not Found
```

trace_id (응답) ↔ trace_id (서버 로그) 일치 → 클라이언트가 trace_id 만 들고 와도 grep 으로 stacktrace 즉시 재현 가능.

## 설계 메모

### OpenAPI 커스터마이저
FastAPI 의 자동 OpenAPI 는 라우트가 실제 reference 한 모델만 `components.schemas` 에 포함한다.
후속 TASK-061/062 가 활용할 base 스키마(`PaginatedResponse`, `TimestampedModel` 등)를 미리 노출하기 위해
`main.py:_build_custom_openapi` 에서 `pydantic.json_schema.models_json_schema` 로 강제 주입했다.
generic instantiation (`PaginatedResponse_HealthResponse_`) 은 베이스 이름(`PaginatedResponse`) 으로 정규화.
TASK-061/062 가 실제 `PaginatedResponse[Asset]` 등을 endpoint 에 사용하면 이 hack 은 자연스레 불필요해진다.

### 핸들러 위치
원래 task description 은 `core/exception_handlers.py` 였으나 TASK-002 와의 `core/` 충돌 회피를 위해
`backend/app/api/_error.py` 로 변경 배치 (task description 4번 항목에 명시된 배치 변경 지시 그대로 따름).
Manager 가 향후 `core/` 로 이전을 원하면 단순 파일 이동만으로 가능 (의존성: app.schemas.common 만).

### 클린 코드 점검
- `main.py` — 앱 조립 + OpenAPI 커스터마이저만. 비즈니스 로직 0.
- `api/_error.py` — 예외 → ErrorResponse 변환 + 로깅만. 도메인 로직 0.
- `schemas/common.py` — cross-endpoint base 5종만. 특정 도메인 스키마는 TASK-061/062 의 `schemas/asset.py`, `schemas/strategy.py`, `schemas/backtest.py` 로 분리.
- `api/health.py` — health 엔드포인트 + `COMMON_ERROR_RESPONSES` 상수만. 후속 라우터가 동일 상수를 import 해 일관성 유지.
- 계층 의존: api → schemas (단방향). schemas 는 외부 의존 없음 (pydantic 만). 도메인 미참조.

## 이슈 / 블로커

없음.

TASK-002 와의 충돌 영역 0건 확인:
- TASK-002 가 작성한 `backend/app/core/{config,db}.py`, `backend/alembic/{env.py,script.py.mako,versions/}` 모두 미터치.
- `backend/app/__init__.py` (TASK-001 산출물) 미수정.
- `backend/app/schemas/__init__.py` 0바이트 미수정 (필요 시 TASK-061/062 가 도메인 스키마 추가하면서 re-export).

## 다음 제안

1. **TASK-061/062 진행 시 `COMMON_ERROR_RESPONSES` 활용**: `backend/app/api/health.py` 에 정의해 둔 상수를 다른 라우터에서도 import 해 응답 스키마 일관성 확보.
2. **OpenAPI 커스터마이저 정리 시점**: TASK-061/062 에서 `PaginatedResponse[Asset]` 등 실제 사용이 등장하면 `main.py:_build_custom_openapi` 의 강제 주입 로직은 단순화 가능 (`ErrorResponse` / `ErrorDetail` 만 남기면 됨, `TimestampedModel` 도 도메인 스키마에 mixin 으로 사용되면 자동 노출).
3. **logging 설정**: 현재 `main.py` 에서 `logging.basicConfig` 만 호출. 운영 시점에 JSON 로거 / log file rotation 이 필요해지면 별도 `app/core/logging.py` (TASK-002 영역) 로 이전 권장.
4. **CORS allow_origins**: 현재 `http://localhost:3000` 하드코딩. 추후 `app/core/config.py` 의 settings 로 노출하는 것이 자연스러움 (TASK-002 의 Settings 가 정착되면 main.py 가 import).
5. **schemathesis 준비**: TASK-082 (API 계약 테스트) 가 `docs/openapi.yaml` 또는 `app.openapi()` 결과를 fuzz 한다. 현재 base 스키마가 모두 노출되어 있어 schemathesis 가 ErrorResponse 형태도 검증 가능.
