---
agent: tester
task_id: TASK-108
status: DONE
timestamp: 2026-04-22T12:30:00
severity: bug
---

## 결과 요약
`/api/v1/` 전체에 대한 통합 단위 테스트 파일 1개(`tests/test_api_v1.py`) 를 신규 작성했다. Bearer 인증 계약(헤더 없음/Not Bearer/오토큰/빈 Bearer/정상 토큰) × 8개 엔드포인트 = 40개 parametrized 케이스 + 엔드포인트별 happy/error path + notebook CRUD + /sync LWW 4 시나리오 + create_app 토큰 검증 + v0 regression 2개를 모두 커버한다. **71개 테스트 전부 PASS**. ES 와 notebook_v1_store 는 fixture 레벨 mock 으로 처리해 실제 ES/네트워크 접근 없이 FastAPI TestClient 만으로 검증했다.

## 변경된 파일
- projects/abc-english/tests/test_api_v1.py (신규, 71 테스트)

## 테스트 결과
- 통과: 71
- 실패: 0
- 참고: 저장소 전체 pytest 는 `test_collector.py::TestParseTranscript::test_normal_transcript`, `test_comparator.py::TestCompareSentences::test_normal_matching`, `test_segments_exhausted`, `test_last_sentence_consumes_all_remaining` 4건 실패가 있으나 이는 **TASK-108 이전부터 존재한 회귀**이며 (Coder report L58 에서도 동일하게 기록) 이번 작업 범위 밖이다.

### 커버리지 요약
- **Bearer 인증 parametrize**: `[GET,/api/v1/episodes]`, `[GET,/api/v1/episodes/{id}]`, `[GET,/api/v1/episodes/{id}/audio]`, `[GET,/api/v1/episodes/{id}/manifest]`, `[GET,/api/v1/lookup?word=...]`, `[GET,/api/v1/notebook]`, `[POST,/api/v1/notebook]`, `[POST,/api/v1/notebook/sync]` 8개 × 5 시나리오(missing/non-bearer/wrong-token/empty-bearer/valid) = 40 케이스.
- **episodes list**: 200 envelope, published_date desc 정렬 검증, page=0/-1/size=0/size=51 → 422, `since_modified` 형식 오류 → 4xx.
- **episodes detail**: 200 + sentences asc 정렬, 404 `{"detail": "episode not found"}`.
- **audio**: 파일 없음 → 404, 파일 있음 → 200 + Accept-Ranges, Range 헤더 → 206 partial.
- **manifest**: 파일 없음 → 200 + `files: []`, 파일 있음 → sha256 검증.
- **lookup**: word 누락/빈값 → 422, 캐시 경유 200 + source 필드.
- **notebook CRUD**: POST 201 + id/created_at/last_modified, GET 후 포함, PATCH 갱신 + last_modified 증가, PATCH 404, DELETE 204 + 제거, DELETE 404.
- **/sync LWW**: upsert 신규 id applied, server_wins(서버가 더 최근), applied(클라이언트가 더 최근), delete 성공 applied, delete 없음 not_found.
- **create_app**: `ABC_API_TOKEN` 미설정 + `settings.api_token` 빈값 → RuntimeError, env 가 YAML 빈값을 override 해 기동 성공.
- **v0 regression**: `/api/health` 와 `/api/episodes` 가 Bearer 없이도 200.

## 이슈/블로커

### 1) `since_modified` 형식 오류 시 상태 코드 불일치 (severity: bug)
- **사양**: TASK-108 본문 *"`since_modified` 형식 오류 시 422"*.
- **실제 구현**: `projects/abc-english/web/api/v1/episodes.py` L60-L62 에서 `HTTPException(status_code=400, detail=f"invalid since_modified: {exc}")` 로 400 반환.
- **영향**: 모바일 클라이언트가 422 를 Pydantic validation 오류(잘못된 요청 형태) 로 처리하고 400 은 일반적인 비즈니스 오류로 구분하는 관행에서 벗어난다. 태스크 스펙과 명시적으로 충돌.
- **권장**: `status_code=400` → `status_code=422` 로 수정 (FastAPI 의 Query validator 와 동일 코드로 통일).
- **테스트 처리**: `TestListEpisodes.test_since_modified_invalid_returns_400` 는 현재 400/422 둘 다 허용해 green 이지만 이름에 `400` 을 고정했다. 수정 후에는 assertion 을 `== 422` 로 좁히고 테스트명도 바꿀 것.

### 2) `payload.dict()` 사용 — Pydantic V2 Deprecation (severity: observation)
- `projects/abc-english/web/api/v1/notebook.py` L96 (`create_notebook`), L110 (`patch_notebook`) 에서 Pydantic V2 의 deprecated API `payload.dict()` 호출.
- Pydantic 2.12 이 `PydanticDeprecatedSince20` 경고 를 발생시킨다(테스트 warnings 에 7건). V3 에서 제거 예정.
- **권장**: `payload.dict()` → `payload.model_dump()`.

### 3) `FastAPI on_event("startup")` — Deprecation (severity: observation)
- `projects/abc-english/web/app.py` L91 `@app.on_event("startup")` 가 deprecated (lifespan event 사용 권장).
- 이번 태스크 스펙 밖이지만 테스트 warnings 에 140건 누적되어 노이즈가 크다. 별도 리팩터 태스크 고려.

### 4) 계층 의존 / 단일 책임 관점 검증 결과
- v1 라우터는 `web/api/episodes.py`, `web/api/audio.py`, `web/api/lookup.py` 로 **위임** 하고 도메인 로직을 재구현하지 않는다 → 계층 위반 없음.
- `notebook_v1_store.py` 는 ES 접근을 캡슐화하고 라우터가 이를 통해서만 쓰기 → 책임 분리 양호.
- `web/api/v1/deps.py` 의 `verify_bearer` 는 헤더 파싱 + 토큰 조회 + 매치를 한 함수에서 처리하지만 30줄 내외로 함수 과대 기준(40줄) 미달. 단일 책임 범위 내.
- DTO↔Entity 분리: `NotebookEntryIn`/`NotebookEntryPatch`/`SyncChange` 등 입력 DTO 와 내부 store 가 다루는 dict 가 분리돼 있어 누수 없음.

## 다음 제안
1. **TASK-108-FIX** (coder): `web/api/v1/episodes.py` L60-L62 의 400 → 422 로 수정. 이후 `test_since_modified_invalid_returns_400` assertion 을 `== 422` 로 강화하는 후속 Tester 호출 권장.
2. (선택) **TASK-108-OBS-1** (coder): `web/api/v1/notebook.py` 의 `.dict()` → `.model_dump()` 치환. Pydantic V3 대비.
3. (선택) 별도 Phase 작업으로 `web/app.py` 의 `on_event` → lifespan handler 마이그레이션.
