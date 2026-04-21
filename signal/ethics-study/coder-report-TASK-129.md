# Coder Report — TASK-129

## 상태
DONE

## 작업 내용

### 1. app.py — ES 데이터 로딩 함수 추가
- `get_thinker(thinker_id)`: ES `ethics-thinkers`에서 직접 ID 조회(get), 실패 시 term 쿼리 fallback
- `get_thinker_works(thinker_id)`: `ethics-works`에서 `thinker_id` term 쿼리, year 오름차순 정렬
- `get_thinker_claims(thinker_id)`: `ethics-claims`에서 claim, argument, counterpoint, original_text 등 전체 필드 조회
- `get_thinker_keywords(thinker_id)`: `ethics-keywords`에서 term, definition, related_terms 조회
- `get_thinker_relations(thinker_id)`: `ethics-relations`에서 from_thinker OR to_thinker 쿼리, direction(incoming/outgoing) 태깅

### 2. app.py — 라우트 수정/추가
- `GET /thinker/{thinker_id}`: 5개 ES 조회 결과를 context로 thinker.html 렌더링. 사상가 없을 경우 404 반환.
- `GET /api/thinker/{thinker_id}` (신규): JSON 응답으로 thinker, works, claims, keywords, relations 반환

### 3. thinker.html 템플릿 작성
base.html 상속. 섹션 구성:
- 상단 hero 영역: 이름, 영문명, 시대/분야 배지, 생몰년, 키워드
- 배경/사상 형성: `<details>` 접이식 (background, philosophical_journey)
- 핵심 사상: core_philosophy 전문, 파란 좌측 border 강조 블록
- 저작 목록: work-card (제목, 원제, 연도, 의의, 핵심개념 태그)
- 주요 주장: claim-card (claim 제목, original_text 인용 블록, explanation, argument/counterpoint 2열 색상 구분, 키워드)
- 키워드 사전: 2열 그리드 카드 (term, term_en, definition, related_terms)
- 관계: 영향을 준 / 받은 사상가 2열 분리, 사상가 ID 링크

### 4. style.css — 상세 페이지 스타일 추가
- `.thinker-hero`, `.thinker-name`, `.meta-badge` 등 헤더 스타일
- `.detail-section`, `.section-title`, `.prose-block` 섹션 공통 스타일
- `.collapsible`, `.collapsible-summary` 접이식 스타일
- `.work-card` 저작 카드 스타일
- `.claim-card`, `.claim-quote`, `.claim-argument`(초록), `.claim-counterpoint`(빨간) 스타일
- `.keywords-dict`, `.keyword-entry` 키워드 그리드 스타일
- `.relations-grid`, `.relation-item`, `.relation-link` 관계 스타일
- 모바일 대응 (`@media max-width: 640px`) responsive 추가

## 테스트 결과

```
curl http://localhost:8000/api/thinker/socrates
→ HTTP 200, JSON 응답 정상
  - thinker: 소크라테스 전체 정보
  - works: 6건 (크리톤, 메논 등)
  - claims: 10건
  - keywords: 7건
  - relations: 7건

curl http://localhost:8000/thinker/socrates
→ HTTP 200, HTML 응답 정상
  - <title>소크라테스 — 윤리 학습 가이드</title>
  - 저작 목록 (6), 주요 주장 (10), 키워드 사전 (7), 관계 (7) 모두 렌더링 확인
```

## 특이 사항
- `/search` 라우트 및 `search_page` 함수는 수정하지 않음 (다른 에이전트가 이미 `search.py` 모듈 import 방식으로 구현 완료)
- uvicorn 서버 포트 8000에서 정상 동작 중 (pid=2144320)
