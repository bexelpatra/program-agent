---
agent: coder
task_id: TASK-108-FIX
status: DONE
timestamp: 2026-04-22T11:14:59+09:00
---

## 결과 요약

Tester 가 TASK-108 에서 지적한 3건의 후속 이슈를 수정했다.

1. `/api/v1/episodes` 의 `since_modified` 검증 경로를 400 HTTPException 에서 FastAPI 표준 422 로 전환. `Query(... , pattern=_ISO8601_REGEX)` 를 적용해 FastAPI 가 malformed 입력을 자동으로 422 로 튕기게 함. 핸들러 내부의 수동 try/except 는 제거.
2. `web/api/v1/notebook.py` 의 Pydantic v1 `.dict()` 호출 2개를 v2 `.model_dump()` 로 치환.
3. `web/app.py` 의 `@app.on_event("startup")` 을 `lifespan` async context manager 로 이관. 기존 `resolve_api_token(settings)` 의 fail-fast 동작은 `create_app()` 호출 지점에 그대로 두어 `test_missing_token_raises_runtime_error` 호환성 보장.

테스트: `pytest tests/test_api_v1.py` → **71/71 PASS**. warnings: 이전 147 → **0**.

## 변경된 파일

- `projects/abc-english/web/api/v1/episodes.py` (수정)
  - `_ISO8601_REGEX` 상수 신규 추가 (module-level).
  - `_parse_iso8601(value)` helper 제거 (더 이상 사용되지 않음).
  - `list_episodes(... since_modified: Optional[str] = Query(None, pattern=_ISO8601_REGEX, ...))` — Query 에 regex 검증 추가. 핸들러 본문에서 수동 검증/400 분기 제거.
  - `from datetime import datetime` import 제거 (사용처 없어짐).
- `projects/abc-english/web/api/v1/notebook.py` (수정)
  - L96: `payload.dict()` → `payload.model_dump()` (POST `/api/v1/notebook`).
  - L110: `payload.dict().items()` → `payload.model_dump().items()` (PATCH `/api/v1/notebook/{entry_id}`).
- `projects/abc-english/web/app.py` (수정)
  - `from contextlib import asynccontextmanager` / `AsyncIterator` import 추가.
  - `create_app()` 내부에 `lifespan` async context manager 정의 → `FastAPI(..., lifespan=lifespan)` 로 전달.
  - `@app.on_event("startup")` 데코레이터 블록 삭제. 같은 Ollama verification 로직은 lifespan 의 startup 페이즈로 이동.
  - `resolve_api_token(settings)` 의 fail-fast 호출 위치는 변경 없음 — 기존 `test_missing_token_raises_runtime_error` 는 그대로 통과.
- `projects/abc-english/tests/test_api_v1.py` (수정 — 태스크에서 명시 예외 허용)
  - `test_since_modified_invalid_returns_400` → `test_since_modified_invalid_returns_422` 로 이름 변경.
  - `assert response.status_code in (400, 422)` 1줄을 `assert response.status_code == 422` 로 조임. 해당 메서드 외 다른 테스트는 건드리지 않음.

## 공개 시그니처 변경

Repository/Service 레이어의 public 메서드 시그니처 변경은 없다. v1 API 경로(`/api/v1/episodes`)의 쿼리 스키마만 변경됐으며 외부 호출자 관점에서는:

- `GET /api/v1/episodes` — `since_modified` 파라미터의 에러 응답 코드가 `400` → `422` 로 변경. 유효 포맷(ISO8601 date/datetime with optional T / Z / offset)은 이전과 실질적으로 동일. 잘못된 값은 FastAPI 표준 `{"detail": [{"type": "string_pattern_mismatch", ...}]}` envelope 을 반환한다.

## 이슈/블로커

없음. 단, 참고:

- `_ISO8601_REGEX` 는 `YYYY-MM-DD(?:[T ]HH:MM(?::SS(?:.ffffff)?)?(?:Z|±HH:MM|±HHMM)?)?` 를 허용한다. 이전 `datetime.fromisoformat` 보다 좁지만, 이전 코드에서도 ES 로 내려보내는 값은 결국 문자열 범위 비교였으므로 수용되는 실제 엔터프라이즈 입력 집합은 동일하다.
- `tests/test_api_v1.py` 내 happy-path 테스트는 `since_modified` 를 전달하지 않으므로 regex 변경의 영향 없음.

## 다음 제안

- `v0` 엔드포인트(`web/api/notebook.py` 등)에도 동일한 `.dict()` → `.model_dump()` 전환이 필요할 가능성. 이번 태스크 스코프는 v1 전용이라 손대지 않았다. 전체 프로젝트에서 `grep -r "\.dict()"` 로 확인 후 별도 FIX 태스크로 분리 권장.
- Lifespan 이관으로 향후 shutdown-phase cleanup(예: ES 클라이언트 close, cache flush) 를 `yield` 이후 블록에 놓을 수 있는 구조가 마련됨. 현재는 no-op.
- `test_api_v1.py` 의 `test_since_modified_invalid_returns_400` 제거된 느슨한 assertion 은 Tester 가 남겨둔 관찰용 TODO 였다. 이제 422 확정으로 tightened.
