# Coder Report — TASK-130

## 상태: DONE

## 작업 요약

통합 검색 기능(claims + keywords + works 전문 검색)을 구현했다.

## 구현 파일

### 1. `projects/ethics-study/web/search.py` (신규)
- `get_thinker_name_map(es)`: ethics-thinkers에서 thinker_id → name 매핑 조회
- `search_claims(es, query, size)`: ethics-claims 인덱스 multi_match 검색 (claim^3, explanation^2, argument, counterpoint, keywords), fuzziness AUTO, highlight 적용
- `search_keywords(es, query, size)`: ethics-keywords 인덱스 multi_match 검색 (term^3, term_en^2, definition), highlight 적용
- `search_works(es, query, size)`: ethics-works 인덱스 multi_match 검색 (title^3, significance^2, key_concepts), highlight 적용
- `search_all(es, query, size)`: 세 함수 통합 호출, thinker_name resolve, 빈 쿼리 early return

각 결과에 `_type` (claim/keyword/work), `_score`, `_highlight_*` 필드 추가.

### 2. `projects/ethics-study/web/templates/search.html` (재작성)
- base.html 상속
- 검색어 표시: "'{q}' 검색 결과 (N건)" + 유형별 건수 부제목
- 결과 탭: 전체 / 주장 / 키워드 / 저작 (JS로 탭 전환, display none/block)
- 주장 카드: 사상가 링크, 주장 텍스트(highlight), 해설(highlight), 키워드 태그
- 키워드 카드: 사상가 링크, 용어+영문, 정의(highlight), 관련용어
- 저작 카드: 사상가 링크, 저서명+원어, 연도, 의의(highlight), 핵심개념
- 빈 검색어 / 결과 없음 / 결과 있음 세 상태 분기

### 3. `projects/ethics-study/web/app.py` (최소 수정)
- `from search import search_all` import 추가
- `search_page` 함수: `search_all(es, q)` 호출 후 결과를 템플릿 컨텍스트에 전달
- `/api/search` JSON 엔드포인트 추가: `search_all` 결과 JSONResponse 반환
- 다른 라우트는 일절 수정하지 않음

### 4. `projects/ethics-study/web/static/style.css` (끝에 추가)
- `.search-query-text`, `.search-empty-state`, `.search-empty-icon` 등 빈 상태 스타일
- `.section-heading`, `.section-badge`, `.result-type-badge` (badge-claim/keyword/work)
- `.tab-count` 탭 내 건수 뱃지
- `.search-result-list`, `.search-result-card`, `.result-card-header`
- `.result-claim-text`, `.result-explanation`, `.result-definition`
- `.result-term`, `.result-term-en`, `.result-work-title`, `.result-keywords`
- `mark` 하이라이트 스타일 (#fff59d 배경)

## 테스트 결과

```
GET /search?q=덕
→ HTML 200 OK
→ 총 67건 — 주장 30건 / 키워드 20건 / 저작 17건

GET /api/search?q=정의
→ JSON {"total": 56, "claims": 30개, "keywords": 19개, "works": 7개}

GET /search (빈 쿼리)
→ search-empty-state 렌더링 확인
```

## 완료 조건 확인

- [x] /search?q=덕 검색 시 관련 claims, keywords, works 표시
- [x] /api/search?q=정의 JSON 응답 정상
- [x] 빈 검색어 시 안내 메시지 표시
