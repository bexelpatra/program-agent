# Tester Report — TASK-018

## 태스크 정보
- Task ID: TASK-018
- Title: LLM Analyzer 테스트
- 테스트 파일: `projects/abc-english/tests/test_llm_analyzer.py`
- 대상 파일: `projects/abc-english/src/llm_analyzer.py`

## 실행 결과

| 항목 | 값 |
|------|-----|
| 상태 | DONE |
| 총 테스트 수 | 49 |
| 통과 | 49 |
| 실패 | 0 |
| 실행 시간 | 0.28s |

## 테스트 커버리지 요약

### _extract_json (5건)
- JSON 코드 블록 추출, 배열 추출, 전체 텍스트 파싱, 파싱 실패 시 ValueError, 잘못된 코드 블록 폴스루

### AnthropicProvider (3건)
- API 키 미설정 시 EnvironmentError, 생성 및 generate 호출 검증 (system 포함/미포함)

### OllamaProvider (3건)
- 생성 시 설정 반영, generate REST 호출 검증 (system 포함/미포함)

### get_provider / reset_provider (5건)
- ollama/anthropic 선택, 싱글톤 캐싱, 잘못된 provider 에러, reset 후 재생성

### Caching (7건)
- _make_cache_key 동일/다른 입력/prefix, get/set 캐시, 캐시 미스, 손상 파일 처리, 캐시 히트 시 LLM 호출 생략

### Text Batching (4건)
- 짧은 텍스트 분할 없음, 긴 텍스트 분할, 중복 제거 병합, detect_expressions 긴 텍스트 자동 분할

### _parse_expression_result (6건)
- 리스트, dict 래퍼(expressions/results), 단일 phrase dict, 빈 리스트, 인식 불가 구조

### detect_expressions (3건)
- 정상 결과, dict 래퍼 결과, 빈 결과

### detect_expressions_for_episode (4건)
- 트랜스크립트 로드 + Expression 모델 변환, type 정규화 (phrasal verb -> phrasal_verb), 미인식 type -> collocation, 문자열 트랜스크립트

### classify_vocabulary (5건)
- 빈 단어 목록, 정상 분류, 배치 분할 (batch_size=5, 12단어 -> 3호출), JSON 파싱 실패 폴백, dict 래퍼 응답

### classify_vocabulary_for_episode (4건)
- 빈 vocabulary, 트랜스크립트 미존재, 정상 플로우 (dict 아이템), 객체 아이템 (.word 속성)

## 테스트 전략
- anthropic 모듈: sys.modules에 mock 삽입하여 ImportError 방지
- LLM 호출: get_provider를 mock하여 generate_json 반환값 제어
- 파일 I/O: tmp_path fixture + fake_project_root로 트랜스크립트/캐시 디렉토리 구성
- 캐시: _CACHE_DIR를 tmp_path로 패치하여 격리
- 싱글톤: autouse fixture로 매 테스트 전후 reset_provider 호출

## 이슈/블로커
- 없음
