# Coder Report — TASK-033

- Task: Frontend 공용 (base template, 네비, common.js, CSS)
- Status: DONE
- Project: abc-english

## 변경 요약

공용 웹 UI 골격을 구축했다. 실제 페이지 콘텐츠(목록/스터디/단어장 상세)는 TASK-034/035에서 채워 넣을 수 있도록 hook 지점만 남겼다.

### 추가/수정 파일
- `projects/abc-english/web/app.py` — (수정) Jinja2 템플릿/StaticFiles 연결, pages 라우터 include.
- `projects/abc-english/web/routes/__init__.py` — (신규) 라우트 패키지.
- `projects/abc-english/web/routes/pages.py` — (신규) HTML 페이지 라우트 3종 (`/`, `/study/{episode_id}`, `/notebook`). Starlette 최신 API(`TemplateResponse(request, name, ctx)`) 사용.
- `projects/abc-english/web/templates/base.html` — (신규) 공통 레이아웃. lang="ko", viewport meta, 네비, main, toast-root, scripts hook.
- `projects/abc-english/web/templates/episodes.html` — (신규) 스텁. `#episode-list` 컨테이너.
- `projects/abc-english/web/templates/study.html` — (신규) 스텁. `<body data-episode-id="...">`, `#player`, `#transcript`, `#drawer`, nav_actions 블록에 `📖 단어장` 토글 버튼(`#drawer-toggle` + `#drawer-badge`).
- `projects/abc-english/web/templates/notebook.html` — (신규) 스텁. `#notebook-table`.
- `projects/abc-english/web/static/css/app.css` — (신규) CSS 변수, 다크모드 기본 + `prefers-color-scheme: light` 대응, 네비/버튼/입력/모달/드로어(translateX, 360px, 0.25s)/토스트/반응형(≤720px) 스타일.
- `projects/abc-english/web/static/js/common.js` — (신규, ESM) `api.get/post/patch/del`, `toast`, `fmtDate`, `fmtDuration`, `initNav`, `setupDrawer({ drawerEl, toggleBtnEl, closeBtnEl, badgeEl, shortcutKey })` — ESC/단축키(n, input focus 시 비활성)/토글 버튼/`bumpBadge(count)` 애니메이션 지원. DOMContentLoaded 시 `initNav()` 자동 호출.

### 설계 노트
- `_STATIC_DIR.exists()` 가드를 둬서 개발 중 static 경로가 없어도 앱 생성이 죽지 않도록 했다 (현 태스크에서는 실제로 존재).
- CORS 미들웨어와 static mount가 충돌하지 않도록 기존 include_router 이후에 pages 라우터 + static을 mount 한다.
- `Jinja2Templates` 디렉토리는 `Path(__file__).resolve().parent.parent / "templates"`로 절대경로 계산 — uvicorn을 어느 cwd에서 실행해도 동작.
- Starlette 0.36+의 deprecation을 반영해 `TemplateResponse(request, name, context)` 형태로 호출.

## 검증 결과

1. `python -m py_compile $(find web -name '*.py')` → OK.
2. `python -c "from web.app import create_app; app = create_app('config/settings.yaml'); [print(r.path) for r in app.routes if hasattr(r,'path')]"` — 출력에 아래 경로 모두 포함:
   - `/`, `/study/{episode_id}`, `/notebook`
   - `/static`
   - `/api/episodes`, `/api/episodes/{episode_id}`, `/api/audio/{episode_id}`, `/api/lookup`, `/api/notebook`, `/api/notebook/{term}/viewed`, `/api/notebook/{term}`, `/api/health`
3. `uvicorn --factory web.app:create_app --host 127.0.0.1 --port 18765` 백그라운드 기동 후:
   - `GET /` → HTML(`<html` 포함) 반환 ✔
   - `GET /study/abc123` → body에 `data-episode-id="abc123"` 포함 ✔
   - `GET /notebook` → 200 ✔
   - `GET /static/css/app.css` → 200 ✔
   - `GET /static/js/common.js` → 200 ✔

## 후속 태스크 hook
- TASK-034: `episodes.html`의 `#episode-list`, `study.html`의 `#player`/`#transcript`/`#drawer`를 채운다. `common.js`의 `api`, `toast`, `fmtDate`, `fmtDuration`, `setupDrawer` 사용.
- TASK-035: `notebook.html`의 `#notebook-table` 구현.
