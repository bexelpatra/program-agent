# Tester Report — TASK-021

## 결과: DONE

## 요약
`src/loader.py`에 대한 단위 테스트 31개를 작성하고 전체 통과를 확인함.

## 테스트 파일
- `projects/abc-english/tests/test_loader.py`

## 테스트 항목 (31개, 전체 PASSED)

| 클래스 | 테스트 수 | 설명 |
|--------|-----------|------|
| TestSlug | 5 | `_slug` 함수: 기본, 공백 제거, 다중 공백, 소문자, 대문자 변환 |
| TestBulkLoad | 6 | `_bulk_load`: 기본 적재, 에러 카운트, 빈 리스트, settings=None 시 자동 로드, bulk_size 설정 반영, 기본값 500 |
| TestLoadEpisodes | 3 | 액션 생성, `_id`가 `episode_id`인지, 빈 리스트 |
| TestLoadSentences | 3 | 액션 생성, `_id`가 `{episode_id}_{sentence_index}`인지, 빈 리스트 |
| TestLoadVocabulary | 3 | 액션 생성, `_id`가 `{word}_{pos}`인지, 빈 리스트 |
| TestLoadExpressions | 4 | 액션 생성, `_id`가 slug화된 phrase인지, 대문자 phrase slug, 빈 리스트 |
| TestLoadAll | 5 | 4개 함수 순차 호출 검증, 전체 빈 입력, 에러 포함 결과, settings=None, 반환 키 검증 |
| TestActionConstruction | 2 | model_dump() 결과가 _source에 올바르게 포함되는지 (Episode, Vocabulary with nested) |

## 실행 결과
```
31 passed in 0.27s
```

## 이슈/블로커
없음.
