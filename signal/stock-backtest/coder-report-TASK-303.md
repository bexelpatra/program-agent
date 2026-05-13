---
task_id: TASK-303
status: DONE
severity: none
agent: coder
date: 2026-05-12
---

# TASK-303 Coder Report — Theme API 라우터 (8 endpoint)

## 결과 요약

8 endpoint 모두 OpenAPI 등록 + 단위 테스트 5건 PASS + 기존 API 회귀 0 + frontend
build PASS + 도메인 격리 검증 0 hit. DoD 항목 (a)~(e) 전부 충족.

## 산출물

### 신규 파일 (3)
- `projects/stock-backtest/backend/app/schemas/theme.py` (135 줄) — 7 스키마: ThemeRead /
  ThemeCreate / ThemeUpdate / ThemeAssetRead / ThemeDetail / ThemeAssetAdd /
  AssetThemeHistoryRead. frozen ConfigDict, Literal EventType 동기.
- `projects/stock-backtest/backend/app/api/themes.py` (390 줄) — 7 endpoint + slug
  자동 생성 (`_generate_slug`) + `_NOT_FOUND_RESPONSES` / `_NOT_FOUND_OR_CONFLICT_RESPONSES`
  로 OpenAPI 4xx 명시.
- `projects/stock-backtest/backend/tests/api/test_themes.py` (304 줄) — 5 단위 테스트
  + DB SOFT-skip + 임시 자산 fixture (seed_assets) + cleanup 헬퍼.

### 갱신 파일 (4)
- `backend/app/api/assets.py` — `GET /api/assets/{asset_id}/theme_history` endpoint
  추가 + `_ASSETS_NOT_FOUND_RESPONSES` 신설 + `from app.domain.themes.entity ...`
  import 추가 + 변환 헬퍼 `_history_to_read`.
- `backend/app/dependencies.py` — `get_theme_repo` / `get_theme_uow` 신설.
- `backend/app/api/__init__.py` — `themes_router` re-export.
- `backend/app/main.py` — `app.include_router(themes_router)` (L134).

## 8 endpoint 검증 (DoD a)

OpenAPI `/api/openapi.json` 노출 operation:
1. `GET    /api/themes`
2. `POST   /api/themes`
3. `GET    /api/themes/{theme_id}`
4. `PATCH  /api/themes/{theme_id}`
5. `DELETE /api/themes/{theme_id}`
6. `POST   /api/themes/{theme_id}/assets`
7. `DELETE /api/themes/{theme_id}/assets/{asset_id}`
8. `GET    /api/assets/{asset_id}/theme_history`

## 테스트 결과 (DoD b/c)

```
pytest tests/api/test_themes.py -q
5 passed, 2 warnings in 1.85s
```

5 케이스 매핑:
1. POST + GET round-trip — POST 201 → GET 단건 (ThemeDetail) → GET 목록 1건.
2. PATCH name/description 부분 갱신 + 빈 body 보존.
3. DELETE soft → GET 200 (themes row 보존) + active_members 빈 리스트.
4. add_asset → remove_asset → theme_history 가 ADDED/REMOVED 2건 시간순 반환.
5. 404 (없는 theme/없는 active asset) + 409 (중복 slug / 중복 active 멤버).

회귀 (DoD c):
```
pytest tests/api/ --ignore=tests/api/test_themes.py
5 failed, 23 passed, 5 skipped
```
baseline (TASK-303 적용 전) 도 동일 `5 failed, 15 passed, 5 skipped` — 차이 = 새 endpoint
들이 schemathesis fuzz 에서 추가 PASS 8 건만 더해짐. **신규 회귀 0**. 잔존 5 fail 은
baseline 과 정확히 동일 — `GET /api/assets/{asset_id}` / `GET /api/assets/{asset_id}/ohlcv`
/ `GET /api/backtests/{run_id}` / `DELETE /api/backtests/{run_id}` / `GET
/api/backtests/{run_id}/result` (이전 태스크의 schemathesis fuzz 환경 의존 fail —
BLOCKER-001 잔재 류).

## frontend build (DoD d)

```
npm run build
✓ Generating static pages (6/6)
Route (app)                              Size     First Load JS
┌ ○ /                                    7 kB           94.4 kB
├ ○ /assets                              2.86 kB         116 kB
├ ƒ /backtests/[run_id]                  1.5 kB          220 kB
└ ○ /backtests/new                       8.84 kB         227 kB
```
TASK-300 의 STOCK enum 추가는 본 태스크에서 만진 백엔드 변경과 무관 — 회귀 0.

## 도메인 격리 (DoD e)

```
grep -rn "from app.api.themes" backend/app/domain/
(0 hit)
```
또한 `backend/app/api/themes.py` 는 `app.domain.themes.*` 만 import — `engine /
strategy / allocators / filters / trade / portfolio` 0 hit (architecture.md L1065).

## 설계 결정 메모

### slug 자동 생성 정책
TASK-303 본문 추가 지시: 한글 입력 가능성 → `re.sub(r'[^\w-]', '-', name, flags=re.UNICODE).strip('-')[:120]`
권장. 본 구현은 + 연속 `-` 합치기 (`_SLUG_DASH_RUN`) + 소문자 변환을 추가. 빈 결과 →
422 "slug 자동 생성 실패" 한국어 메시지.

### UnitOfWork 주입
`get_theme_uow` 가 동일 `Session` (Depends(get_db)) 을 받아 `SqlAlchemyUnitOfWork`
생성. `get_theme_repo` 도 동일 Session — 트랜잭션 일관성. service 의 `add_asset_to_theme`
가 try/except 안에서 명시적 commit/rollback (TASK-301 의 UnitOfWork Protocol 결정과
동기).

### soft delete 정책
alembic 0005 schema 에 themes.deleted_at 컬럼이 없어 themes row 자체는 보존
(`SqlThemeRepository.soft_delete_theme` 모듈 docstring 참조). DELETE /api/themes/{id}
는 활성 멤버 일괄 종료만 보장. 테스트 케이스 3 가 이 invariant 를 명시적으로 검증
(GET 후 status 200 + active_members 빈 리스트).

### error 매핑
- 404: 없는 theme_id (get_theme None / soft_delete LookupError / update LookupError /
  add/remove 의 사전 검증) + 없는 active asset (InactiveMember) + 없는 asset (POST
  add 의 사전 session.get + GET theme_history 의 find_by_id None).
- 409: IntegrityError (중복 slug) + DuplicateActiveMember.
- 422: slug 자동 생성 실패 + FastAPI 자동 validation.

### OpenAPI 4xx 명시 (schemathesis fuzz 통과)
`COMMON_ERROR_RESPONSES` (400/422/500) 외에 본 라우터가 실제 사용하는 404/409 를
추가 명시 (`_NOT_FOUND_RESPONSES` / `_NOT_FOUND_OR_CONFLICT_RESPONSES`). 미명시 시
schemathesis 가 "Undocumented HTTP status code" 로 fail (직접 식별·수정한 issue).
assets 라우터의 새 theme_history endpoint 도 `_ASSETS_NOT_FOUND_RESPONSES` 사용.

### 204 응답 핸들러 시그니처
FastAPI 는 status_code=204 + 함수 시그니처 `-> None` 시 `Response body must not
exist` AssertionError. backtests.py 의 DELETE 패턴과 동일하게 `-> Response` +
`return Response(status_code=204)` 사용.

## 환경 노트
- `.venv` = `projects/stock-backtest/.venv/bin/python` (TASK-309 발견 — `backend/.venv`
  아님). 모든 명령어가 이 경로를 사용해 검증됨.
- KRX 로그인 실패 메시지는 환경 변수 미설정 (KRX_ID/KRX_PW) — 테스트 결과와 무관.
