# Coder Report — TASK-132

## 상태: DONE

## 작업 요약

`projects/ethics-study/web/app.py` 및 `projects/ethics-study/web/templates/thinker.html` 수정 완료.

---

## 수정 내역

### 이슈 1: 관계 섹션 사상가 이름 한국어 표시

**app.py**
- `get_thinker_id_name_map()` 함수 신규 추가 — ES `ethics-thinkers` 인덱스에서 id→name 매핑 dict를 한 번만 조회해 반환
- `get_thinker_relations()`에서 `name_map = get_thinker_id_name_map()` 호출 후:
  - `src["from_thinker_name"]` = name_map.get(from_id, from_id) (미등록 시 ID 그대로)
  - `src["to_thinker_name"]` = name_map.get(to_id, to_id)

**templates/thinker.html**
- 관계 섹션에서 `rel.to_thinker` / `rel.from_thinker` 대신 `rel.to_thinker_name` / `rel.from_thinker_name` 표시

---

### 이슈 2: 미등록 사상가 링크 404 방지

**app.py**
- `registered_ids = set(name_map.keys())`로 등록된 사상가 집합 구성
- `src["from_thinker_exists"]` / `src["to_thinker_exists"]` boolean 필드 추가

**templates/thinker.html**
- `rel.to_thinker_exists` / `rel.from_thinker_exists`가 true이면 `<a>` 링크 렌더링
- false이면 `<span class="relation-link relation-link-unregistered">` 일반 텍스트로 표시 (404 방지)

---

### 이슈 3: relation type 한국어 매핑

**app.py**
- `RELATION_TYPE_LABELS` 딕셔너리 추가:
  ```python
  RELATION_TYPE_LABELS = {
      "influenced": "영향을 줌",
      "influenced_by": "영향을 받음",
      "criticized": "비판함",
      "developed": "발전시킴",
      "synthesized": "종합함",
  }
  ```
- `get_thinker_relations()`에서 `src["type_label"] = RELATION_TYPE_LABELS.get(rel_type, rel_type)` 추가

**templates/thinker.html**
- `rel.type` 대신 `rel.type_label` 표시

---

### 이슈 5: 예외 처리 로깅 추가

**app.py**
- 파일 상단에 `import logging` + `logger = logging.getLogger(__name__)` 추가
- 모든 `except Exception` 블록에 `logger.exception(...)` 호출 추가:
  - `get_thinker_id_name_map()`: `logging.exception("Failed to build thinker id→name map")`
  - `get_thinker()` 내부 2개 블록
  - `get_thinker_works()`, `get_thinker_claims()`, `get_thinker_keywords()`, `get_thinker_relations()`

---

## 테스트 결과

```
# socrates 페이지 확인
curl http://localhost:8000/thinker/socrates
→ 관계 섹션에 "플라톤", "아리스토텔레스" 등 한국어 이름 표시 확인
→ relation-type에 "영향을 줌" 한국어 표시 확인

# kant 페이지 확인
curl http://localhost:8000/thinker/kant
→ "영향을 줌", "종합함", "비판함" 등 한국어 type_label 정상 표시 확인
```

서버 재시작 및 응답 정상 확인 완료.
