# Coder Report - TASK-014

## Status: DONE

## Task
LLM Analyzer 구현 - 프로바이더 추상화 (Claude API / 로컬 LLM 전환 가능)

## 변경 파일
- `projects/abc-english/src/llm_analyzer.py` (신규 생성)

## 구현 내역

### 1. LLMProvider ABC
- `generate(prompt, system) -> str`: 추상 메서드
- `generate_json(prompt, system) -> dict`: 구현 메서드 (generate 호출 후 JSON 추출)

### 2. AnthropicProvider
- `anthropic` 패키지 사용, Messages API 호출
- `settings.yaml`의 `llm.anthropic` 섹션에서 model, max_tokens 읽기
- `ANTHROPIC_API_KEY` 환경변수에서 API 키 로드 (미설정 시 EnvironmentError)
- 응답 content blocks에서 text 타입만 추출하여 결합

### 3. OllamaProvider
- `requests` 패키지로 `POST {base_url}/api/generate` 호출
- `settings.yaml`의 `llm.ollama` 섹션에서 model, base_url 읽기
- `stream: False`로 설정하여 단일 응답 수신

### 4. get_provider 팩토리
- `settings['llm']['provider']` 값에 따라 인스턴스 생성
- 모듈 수준 싱글톤 캐싱 (`_provider`, `_provider_name`)
- `reset_provider()` 함수로 싱글톤 리셋 가능

### 5. JSON 추출
- `_extract_json()` 헬퍼: ` ```json ... ``` ` 블록 우선 시도, 실패 시 전체 텍스트 파싱
- 파싱 실패 시 `ValueError` raise (응답 첫 500자 포함)

## requirements.txt
- `anthropic>=0.25.0` 이미 포함되어 있음. 추가 불필요.

## 설계 참고
- transcriber.py의 싱글톤 캐싱 패턴을 동일하게 적용
- `requests`를 `http_requests`로 import하여 모듈 내 이름 충돌 방지
- `anthropic` 패키지는 AnthropicProvider.__init__에서 지연 import (Ollama만 쓸 때 불필요한 의존성 로드 방지)
