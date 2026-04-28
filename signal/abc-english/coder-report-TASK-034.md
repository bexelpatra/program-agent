# Coder Report — TASK-034

- Task: Frontend 학습 페이지 (episodes list + study page)
- Status: DONE
- Date: 2026-04-14

## 작업 요약

에피소드 리스트 페이지와 학습 페이지의 전체 프론트엔드 기능을 구현했다.
기존 FastAPI 라우트/템플릿 구조(`web/routes/pages.py`, `web/templates/base.html`,
`web/api/*`)와 공용 JS 유틸(`common.js`)을 재사용하고,
신규 모듈 2개(`episodes.js`, `study.js`)와 CSS 확장으로 기능을 채웠다.

## 변경된/추가된 파일

- `projects/abc-english/web/static/js/episodes.js` (신규)
- `projects/abc-english/web/static/js/study.js` (신규)
- `projects/abc-english/web/templates/episodes.html` (`scripts` 블록 추가)
- `projects/abc-english/web/templates/study.html` (전면 개편: 플레이어/토글/자막바/드로어 검색 영역)
- `projects/abc-english/web/static/css/app.css` (에피소드 카드, 뱃지, 플레이어,
  자막 바, 하이라이트, 룩업 모달, 드로어 리스트 CSS 추가)

## 기능 구현 상세

### A. 에피소드 리스트 (`episodes.js` + `episodes.html`)
- `GET /api/episodes` 로드 → 카드 그리드 렌더.
- 카드에 제목/발행일/길이/문장수/`has_transcript` 뱃지 표시.
- 카드 클릭 시 `/study/{episode_id}`로 이동.
- 상단 검색 입력으로 제목 부분 일치 필터 (클라 사이드, 실시간).
- 일치/전체 카운트 표시.

### B. 학습 페이지 (`study.js` + `study.html`)
1. **데이터 로드**: `body.dataset.episodeId` → `GET /api/episodes/{id}`.
   sentences는 `start_time asc`로 정렬해 보관.
2. **오디오 플레이어**: `<audio src="/api/audio/{id}" preload="metadata">`,
   재생/일시정지 버튼, seek bar, `currentTime / duration` 표시.
   - 배속 select: 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0x.
   - ±N초 스킵 버튼 + 스킵초 입력 (1~30, `localStorage.skipSeconds` 영속).
   - 키보드: Space/←/→/↑/↓ (input·select focus 중 비활성).
3. **자막 싱크**: `timeupdate`에서 현재 idx 캐시 → 인접 idx 확인 → 실패시 이진탐색.
   변경 시에만 `.active` 이동 및 `scrollIntoView({block:'center'})`.
4. **토글** 3종 (전체 스크립트 / 자막 바 / 하이라이트), 상태 localStorage 영속.
5. **단어 클릭 / 드래그 선택 → 룩업 모달**:
   - 각 문장 토큰을 whitespace 기준으로 분리, 구두점 제거한 `data-term`으로 `.word` span 생성.
   - 클릭 → 즉시 모달 오픈.
   - 드래그(1~6단어) → 선택 근처에 "🔍 lookup" 플로팅 버튼 → 클릭 시 모달 오픈.
   - 모달: term + 유형 뱃지(word/phrasal_verb/idiom/collocation),
     explanation_en, etymology(있을 때), examples 리스트,
     "📒 단어장 추가" + "닫기". 로딩 중 spinner + "Ollama 질의 중…".
   - 단어장 추가 성공 → 토스트 + 드로어 prepend 또는 badge bump.
6. **우측 드로어**: `common.js/setupDrawer`로 토글/단축키(N)/ESC 처리.
   - `GET /api/notebook?sort=last_added` 상위 30개.
   - 엔트리: term, term_type 뱃지, added_count, 축약된 explanation_en (details로 펼침).
   - 드로어 내 검색 입력으로 클라 필터.
7. **접근성**: 자막 바 `aria-live="polite"`, 버튼 `<button>`, 모달 `role="dialog" aria-modal`.

## 검증

- `python -m py_compile $(find web -name '*.py')` → OK.
- `node --check` (node v24.14.0): `study.js`, `episodes.js`, `common.js` 모두 syntax OK.
- uvicorn `127.0.0.1:18765` 백그라운드 기동 후:
  - `GET /api/health` → 200.
  - `GET /` HTML에 `episodes.js` 참조 존재.
  - `GET /study/TEST123` HTML에 `study.js`, `data-episode-id="TEST123"` 포함.
  - `/static/js/{study,episodes,common}.js`, `/static/css/app.css` 모두 200 OK.

## 금지 사항 준수

- `task-board.md`, `architecture.md` 미수정.
- `tests/` 미수정.
- 다른 프로젝트 경로 미접근.
- 단어장 전용 페이지(`notebook.html` + `notebook.js`)는 건드리지 않음 (TASK-035).

## 후속 고려

- 드래그 선택 버블은 모바일 터치에서는 `touchend`만 잡고, 짧은 탭은 무시한다.
- 현재 drawer 내 단어 엔트리 클릭 시 해당 에피소드로 점프하는 기능은
  단어장 페이지(TASK-035) 범위로 둠 (이 드로어는 프리뷰 전용).
- 자막 싱크 이진탐색은 "start_time 기준 최대값"을 찾고,
  gap(end_time 이후)에도 직전 문장을 계속 active로 유지한다 — 사용자가
  gap 구간에서 빈 자막을 보는 것보다 낫다고 판단.
