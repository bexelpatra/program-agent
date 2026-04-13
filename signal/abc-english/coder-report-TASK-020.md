# Coder Report — TASK-020

## 상태: DONE

## 요약
`projects/abc-english/src/loader.py`를 신규 작성하여 ES bulk 적재 기능을 구현하였다.

## 작업 내역

### 생성된 파일
- `projects/abc-english/src/loader.py`

### 구현된 함수

1. **`load_episodes(episodes, settings)`** — Episode 리스트를 abc-episodes 인덱스에 bulk 적재. `_id`는 `episode_id`.
2. **`load_sentences(sentences, settings)`** — Sentence 리스트를 abc-sentences 인덱스에 bulk 적재. `_id`는 `"{episode_id}_{sentence_index}"`.
3. **`load_vocabulary(vocabulary, settings)`** — Vocabulary 리스트를 abc-vocabulary 인덱스에 bulk 적재. `_id`는 `"{word}_{pos}"`.
4. **`load_expressions(expressions, settings)`** — Expression 리스트를 abc-expressions 인덱스에 bulk 적재. `_id`는 phrase를 slug화(소문자, 공백→하이픈).
5. **`load_all(episodes, sentences, vocabulary, expressions, settings)`** — 위 4개 함수를 순차 호출하고 전체 결과 요약을 반환.

### 설계 결정
- `elasticsearch.helpers.bulk`를 사용하여 효율적인 bulk 적재 수행
- `chunk_size`는 settings.yaml의 `elasticsearch.bulk_size` (기본 500) 적용
- `raise_on_error=False, stats_only=True`로 에러 발생 시에도 중단하지 않고 카운트만 반환
- 공통 로직을 `_bulk_load()` 내부 헬퍼로 추출하여 중복 제거
- Pydantic 모델은 `model_dump()`으로 dict 변환
- 모든 함수가 `{"loaded": N, "errors": N}` 형태 반환 (load_all은 키별 dict)

## 완료 조건 충족 여부
- [x] `projects/abc-english/src/loader.py` 파일 생성됨
- [x] load_episodes, load_sentences, load_vocabulary, load_expressions, load_all 함수 구현됨
- [x] bulk API를 사용하여 효율적으로 적재
- [x] 각 함수가 loaded/errors 카운트를 반환
