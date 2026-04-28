# Coder Report — TASK-128

## 태스크
FastAPI 앱 기본 구조 + 메인 페이지 (사상가 목록, 분야별 탭)

## 상태
DONE

## 구현 내용

### 생성된 파일

| 파일 | 설명 |
|------|------|
| `projects/ethics-study/web/app.py` | FastAPI 앱 (ES 연결, 라우트 4개, 그룹화 로직) |
| `projects/ethics-study/web/templates/base.html` | 공통 레이아웃 (헤더 nav + 검색바 + footer) |
| `projects/ethics-study/web/templates/index.html` | 메인 페이지 (분야별 탭 + 사상가 카드 그리드) |
| `projects/ethics-study/web/templates/thinker.html` | 사상가 상세 (placeholder — TASK-129에서 구현) |
| `projects/ethics-study/web/templates/search.html` | 검색 페이지 (placeholder — 다음 태스크에서 구현) |
| `projects/ethics-study/web/static/style.css` | 학습 도구 스타일 (반응형, 탭 UI, 카드 그리드) |
| `projects/ethics-study/web/static/app.js` | 탭 전환 + 검색바 엔터 처리 |

### 수정된 파일
| 파일 | 변경 내용 |
|------|-----------|
| `projects/ethics-study/requirements.txt` | fastapi, uvicorn[standard], jinja2, python-multipart 추가 |

### 라우트 구성

```
GET /                   → index.html (사상가 42명 카드 + 분야별 탭)
GET /thinker/{id}       → thinker.html (placeholder)
GET /search?q=          → search.html (placeholder)
GET /api/thinkers       → JSON: 전체 사상가 목록 (42개)
```

### 특이사항

- Starlette 1.0.0 (설치된 버전)에서는 `TemplateResponse` API가 변경됨
  - Before: `TemplateResponse(name, {"request": req, ...})`
  - After: `TemplateResponse(request=req, name=name, context={...})`
  - 이 방식으로 수정하여 정상 동작 확인

## 테스트 결과

### curl / — HTML 응답
```
HTTP 200 OK
- 사상가 카드 42개 렌더링 확인 (class="thinker-card" x42)
- 탭 버튼 4개 (전체, 서양윤리, 동양윤리, 정치철학·사회사상)
- 첫 카드: 노자 (birth_year -571, 시대순 정렬 확인)
```

### curl /api/thinkers — JSON 응답
```json
{
  "total": 42,
  "thinkers": [...]
}
분야 분포: eastern_ethics 15, western_ethics 17, political_philosophy 10
```

## 완료 조건 충족 여부

- [x] `projects/ethics-study/web/app.py` 동작 확인
- [x] 메인 페이지에서 42명 사상가 분야별 탭으로 표시
- [x] `curl localhost:8000` → HTML 응답 (200 OK)
- [x] `curl localhost:8000/api/thinkers` → JSON 응답 (total: 42)

## 실행 방법

```bash
pip install fastapi "uvicorn[standard]" jinja2 python-multipart
cd projects/ethics-study/web
uvicorn app:app --host 0.0.0.0 --port 8000
```
