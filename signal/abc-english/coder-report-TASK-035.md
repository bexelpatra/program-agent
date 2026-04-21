# Coder Report — TASK-035

- Task: Frontend 단어장 전용 페이지 (필터/정렬, 출처 에피소드 점프)
- Status: DONE

## 변경 파일
- `projects/abc-english/web/templates/notebook.html` — 검색/유형/정렬 툴바 + `#notebook-list` 컨테이너 + `notebook.js` 모듈 로드 블록 추가.
- `projects/abc-english/web/static/js/notebook.js` (신규) — ESM 모듈. 툴바 이벤트 바인딩, `api.get('/api/notebook?...')` 호출, 카드 렌더링, 펼치기 시 `PATCH /api/notebook/{term}/viewed` 호출, 삭제(confirm → `api.del` → DOM 제거 + 토스트), 출처 에피소드 링크(`/study/{id}#s={sentence_index}`).
- `projects/abc-english/web/static/js/study.js` — 문장 렌더 시 `data-sentence-index` 속성 추가 + `handleHashJump()` 신설(스크롤 + `.hash-flash` 1.6s 하이라이트). 기존 로직 비침투적 최소 패치.
- `projects/abc-english/web/static/css/app.css` — 노트북 카드/툴바/etymology 보라 좌측 보더 박스/소스 링크/빈 상태 스타일 및 `.hash-flash` keyframe 추가.

## 구현 포인트
- 검색(`q`)은 클라이언트 사이드 필터. 서버 재요청은 정렬/유형 변경 시에만 수행.
- `PATCH .../viewed` 응답을 현재 엔트리에 머지해 view_count/last_viewed를 즉시 반영.
- 삭제 시 `confirm` 후 DOM에서 제거(전체 재요청 없음) + success 토스트.
- etymology가 있으면 보라색 좌측 보더(`#a78bfa`) 강조 박스로 렌더.
- study.js hash 파싱은 `new URLSearchParams(location.hash.slice(1))` 방식으로 `s=` 파싱 → `document.querySelector('[data-sentence-index="…"]')` → `scrollIntoView({behavior:'smooth',block:'center'})` + `.hash-flash` 일시 하이라이트. 기존 timeupdate/highlight 로직 미변경.

## 검증
- `python -m py_compile $(find web -name '*.py')` → OK
- `node --check web/static/js/notebook.js` → OK
- `node --check web/static/js/study.js` → OK
- uvicorn 127.0.0.1:18766 기동 후 `curl /notebook` → 200, 응답 본문에 `notebook.js` 참조 포함 확인.

## 비고
- 서버 API(`/api/notebook`)는 `q` 파라미터를 이미 지원하지만 UX 반응성을 위해 클라이언트 필터로 처리. 필요 시 서버 위임으로 쉽게 전환 가능.
- 기존 `.notebook-table` 클래스 이름은 더 이상 사용하지 않음. 새 레이아웃은 `.notebook-list` 플렉스 컬럼 카드 구조.
