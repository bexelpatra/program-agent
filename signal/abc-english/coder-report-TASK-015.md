# Coder Report — TASK-015

## Status: DONE

## Task
LLM Analyzer 구현 - 숙어/구동사/관용어 탐지 + 어원 설명 생성 (원문 전체 입력)

## 변경 파일
- `projects/abc-english/src/llm_analyzer.py` — 두 함수 추가, import 보강

## 작업 내역

### 1. import 추가
- `from pathlib import Path`
- `from typing import List` (기존 Optional에 추가)
- `from .models import Expression, ExampleSentence`

### 2. `detect_expressions(text, settings)` 함수 구현
- 시스템 프롬프트: 영어 언어학 전문가 + etymology 전문가 역할 지정, JSON only 응답 요구
- 유저 프롬프트: 원문 전체를 전달, 각 항목에 phrase/type/definition_en/definition_ko/etymology/difficulty 필드 요청
- `generate_json` 호출 후 결과 파싱
- 응답이 list인 경우 그대로 반환, dict인 경우 wrapper key(expressions/results/items/data) 탐색하여 유연하게 처리

### 3. `detect_expressions_for_episode(episode_id, settings)` 함수 구현
- `data/transcripts/{episode_id}_official.json` 로드 (Path(__file__).resolve().parent.parent 패턴)
- transcript JSON이 str/dict 등 다양한 형태일 수 있으므로 유연하게 텍스트 추출
- `detect_expressions` 호출 후 결과를 Expression 모델 리스트로 변환
- type 값 정규화 (e.g. "phrasal verb" -> "phrasal_verb")

### 4. 기존 코드 보존
- LLMProvider, AnthropicProvider, OllamaProvider, get_provider, reset_provider 등 기존 코드 변경 없음

## 완료 조건 충족 여부
- [x] detect_expressions 함수 추가됨
- [x] detect_expressions_for_episode 함수 추가됨
- [x] 기존 프로바이더 코드 변경 없음
- [x] Expression 모델을 올바르게 반환
