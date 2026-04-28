# Coder Report - TASK-016

## Status: DONE

## Task
LLM Analyzer 구현 - CEFR 난이도 분류 + 한국어 뜻 매핑 (원문 전체 입력)

## 작업 내용

`projects/abc-english/src/llm_analyzer.py` 파일 끝부분에 다음 함수들을 추가:

### 1. `_get_batch_size(settings)`
- settings.yaml에서 현재 활성 프로바이더의 `batch_size` 설정값을 읽어 반환
- 기본값: 10

### 2. `classify_vocabulary(words, text, settings)`
- 단어 리스트와 원문 전체를 LLM에 전달하여 CEFR 분류 수행
- 시스템 프롬프트: 영어 교육 전문가 + CEFR 분류 전문가 역할
- 유저 프롬프트: 원문 전체 + 단어 리스트 → JSON 배열 응답 요청
- `generate_json` 호출하여 응답 파싱
- dict 래퍼(`{"words": [...]}` 등) 형태 응답도 유연하게 처리
- batch_size에 따라 배치 분할 처리
- JSON 파싱 실패 시 빈 항목으로 대체하여 안정적 반환

### 3. `classify_vocabulary_for_episode(episode_id, vocabulary, settings)`
- `data/transcripts/{episode_id}.json`에서 공식 transcript 로드
- vocabulary 리스트에서 word 필드 추출 (dict/object 모두 지원)
- `classify_vocabulary` 호출
- 결과를 vocabulary 리스트의 각 항목에 difficulty, definition_en, definition_ko 매핑
- Pydantic model_dump() 및 __dict__ 모두 지원

## 변경 파일
- `projects/abc-english/src/llm_analyzer.py` (함수 추가만, 기존 코드 무변경)

## 기존 코드 영향
- 프로바이더 코드(LLMProvider, AnthropicProvider, OllamaProvider, get_provider, _extract_json, reset_provider): 변경 없음
- detect_expressions 관련 함수: 변경 없음
- 새 함수만 파일 끝에 추가함
