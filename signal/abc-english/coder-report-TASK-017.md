# Coder Report — TASK-017

## Status: DONE

## 수행 내용

### 1. 버그 수정 (3건)

**버그 A: `detect_expressions_for_episode` 필드명 (line 499-501)**
- 변경 전: `transcript_data.get("text") or transcript_data.get("transcript", "")`
- 변경 후: `transcript_data.get("full_text") or " ".join(transcript_data.get("sentences", []))`
- 이유: 공식 transcript JSON 형식은 `{"episode_id": "...", "sentences": [...], "full_text": "..."}`

**버그 B: `classify_vocabulary_for_episode` 파일 경로 (line 680-682)**
- 변경 전: `f"{episode_id}.json"`
- 변경 후: `f"{episode_id}_official.json"`
- 이유: collector가 저장하는 파일명은 `{episode_id}_official.json`

**버그 C: `classify_vocabulary_for_episode` 필드명 (line 693-695)**
- 변경 전: `transcript_data.get("official_transcript", "")`
- 변경 후: `transcript_data.get("full_text") or " ".join(transcript_data.get("sentences", []))`
- 이유: JSON 필드명은 "full_text"이고 "sentences" 폴백

### 2. 캐싱 기능 추가

파일 기반 LLM 응답 캐시를 구현하였다. 캐시 디렉토리: `data/cache/llm/`

**새로 추가된 함수:**
- `_make_cache_key(prefix, content)`: SHA-256 해시 기반 캐시 키 생성
- `_get_cache(cache_key)`: JSON 파일에서 캐시 조회
- `_set_cache(cache_key, data)`: JSON 파일로 캐시 저장

**적용 대상:**
- `detect_expressions()`: 동일 텍스트 재분석 시 캐시 활용
- `classify_vocabulary()`: 동일 단어 목록+텍스트 조합 시 캐시 활용

캐시 키 구성:
- expressions: `expressions_{sha256(text)}`
- vocabulary: `vocabulary_{sha256(sorted_words + text)}`

### 3. 배치 처리 개선

`detect_expressions`에 긴 텍스트 분할 처리를 추가하였다:
- 5000단어 초과 시 문장 경계 기준으로 청크 분할
- 각 청크를 독립적으로 LLM에 전달
- 결과를 병합하면서 phrase 기준 중복 제거

**새로 추가된 헬퍼 함수:**
- `_split_text_into_chunks(text, max_words)`: 문장 경계 기준 텍스트 분할
- `_merge_expression_results(results_list)`: 청크별 결과 병합 + 중복 제거
- `_parse_expression_result(result)`: LLM 응답 정규화 (기존 로직 추출)

## 변경 파일
- `projects/abc-english/src/llm_analyzer.py`

## 인터페이스 변경
- 없음. 기존 공개 함수의 시그니처 유지.
