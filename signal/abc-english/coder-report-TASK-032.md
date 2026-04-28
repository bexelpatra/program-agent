# Coder Report — TASK-032

## 태스크
- Task ID: TASK-032
- Title: FastAPI 백엔드 (episodes/audio-Range/lookup/notebook API)
- Status: DONE

## 구현 요약
`projects/abc-english/web/` 하위에 FastAPI 앱을 신규 구현했다. 앱 팩토리 패턴 (`create_app(settings_path)`)을 채택하여 uvicorn/tests 양쪽에서 재사용 가능하다. 모든 API는 기존 `src/` 모듈(`es_client`, `notebook_store`, `llm_cache`, `ollama_client`)을 재활용하여 중복 로직을 두지 않았다.

### 생성/수정 파일
- `projects/abc-english/web/__init__.py` — `create_app` re-export.
- `projects/abc-english/web/app.py` — FastAPI 팩토리. CORS(`*`), startup 훅에서 `verify_ollama_model` 호출(경고 로그만), `/api/health` 포함.
- `projects/abc-english/web/deps.py` — `get_settings`, `get_es`, `get_index`, `resolve_project_path` 공용 의존성.
- `projects/abc-english/web/api/__init__.py`
- `projects/abc-english/web/api/episodes.py` — `/api/episodes`(목록, `?limit=` 지원, published_date desc), `/api/episodes/{episode_id}`(episode + sentences asc, size=1000).
- `projects/abc-english/web/api/audio.py` — `/api/audio/{episode_id}` (Range 헤더 수동 파싱 + StreamingResponse 64KB 청크). 206/200/404/400/416 반환.
- `projects/abc-english/web/api/lookup.py` — `/api/lookup` (cache-first, use_cache 플래그, 실패 시 503).
- `projects/abc-english/web/api/notebook.py` — 목록(sort/term_type/q), 업서트(캐시 → lookup_term → upsert), PATCH viewed, DELETE(204).
- `projects/abc-english/requirements.txt` — `fastapi`, `uvicorn[standard]`, `jinja2` 추가.

## 검증 결과
1. `python -m py_compile $(find web -name '*.py')` → OK.
2. `python -c "from web.app import create_app; app = create_app('config/settings.yaml'); print([r.path for r in app.routes])"` 출력:
   ```
   ['/openapi.json', '/docs', '/docs/oauth2-redirect', '/redoc',
    '/api/episodes', '/api/episodes/{episode_id}',
    '/api/audio/{episode_id}',
    '/api/lookup',
    '/api/notebook', '/api/notebook',
    '/api/notebook/{term}/viewed', '/api/notebook/{term}',
    '/api/health']
   ```
   요구된 모든 경로가 확인됨.
3. Range 헤더 스모크 테스트 (`/tmp/smoke_range.py`, 커밋 제외): 전체 파일(200), `bytes=0-99`(206), `bytes=1000-`(206), suffix `bytes=-50`(206), unsatisfiable(416), missing(404), path traversal(400/404) 모두 통과.

## 설계 메모
- **Path traversal 방어**: `audio.py`에서 episode_id 정규식(`^[A-Za-z0-9][A-Za-z0-9_-]*$`) + 최종 resolved path가 `data/audio/` 안인지 `Path.relative_to` 로 재확인.
- **단일 Ollama 호출 경로**: notebook `POST`에서도 캐시 hit 시 `lookup_term` 재호출하지 않도록 `llm_cache.get_cached` 를 먼저 확인한다(노트북 응답을 기존 캐시에서 재사용).
- **index resolver**: 경로/인덱스 키 분리를 위해 `get_index(request, "episodes"|"sentences")` 헬퍼를 둠.
- **startup 이벤트 실패 내성**: Ollama 미기동 환경에서도 앱이 뜨도록 verify 예외를 swallow.
- **Note**: Task-board/architecture는 지시대로 수정하지 않았고, tests/ 파일도 건드리지 않았다.

## 다음 단계 제안 (Manager 판단용)
- 프런트엔드 템플릿/정적 자원(`web/templates/`, `web/static/`) 구현 태스크 착수 가능.
- 통합 테스트(`tests/web/test_*.py`)에서 TestClient로 라우트/Range 회귀를 추가하는 별도 Tester 태스크 권장.
