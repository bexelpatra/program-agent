# Coder Report — TASK-011

## Status: DONE

## 태스크
Analyzer 구현 - spaCy 품사 태깅 + NER 인명 필터링 + 기능어 제거 + 단어 빈도 분석

## 변경 파일
- `projects/abc-english/src/analyzer.py` (신규 생성)

## 구현 내용

### 1. `load_nlp(settings=None) -> Language`
- settings.yaml의 `spacy.model` (기본: "en_core_web_sm") 로딩
- 모듈 수준 싱글톤 캐싱 (`_nlp`, `_nlp_model_name`)
- transcriber.py의 `load_model` 패턴과 동일한 구조

### 2. `analyze_text(text, episode_id, settings=None) -> List[Vocabulary]`
- spaCy로 품사 태깅 (POS tagging) 수행
- NER로 PERSON 엔티티 식별 → 해당 토큰 인덱스를 필터링 셋에 수집
- settings의 `spacy.filter_pos`에 해당하는 품사 제거
- 남은 토큰의 lemma(소문자) 기반으로 (lemma, pos) 키로 빈도 집계
- 각 단어별 최대 3개의 example_sentences 수집
- 빈도 내림차순 정렬된 Vocabulary 리스트 반환

### 3. `analyze_episode(episode_id, settings=None) -> List[Vocabulary]`
- `data/transcripts/{episode_id}_official.json` 로드
- `full_text` 우선 사용, 없으면 `sentences` 조인으로 폴백
- analyze_text 호출 후 Vocabulary 리스트 반환

### 4. `analyze_all(episode_ids, settings=None) -> List[Vocabulary]`
- 여러 에피소드 순회, 에피소드별 analyze_episode 호출
- 에피소드 간 동일 (lemma, pos)인 단어 병합: frequency 합산, episodes 리스트 합집합, example_sentences 중복 제거 병합
- skip/done/failed 카운트 로깅
- 빈도 내림차순 정렬된 병합 결과 반환

### 설계 원칙 준수
- spaCy 필터링은 vocabulary 빈도 집계 전용으로만 사용
- 원문 전체에 대한 필터링 없는 전달은 LLM Analyzer의 책임
- 경로 해석: `Path(__file__).resolve().parent.parent` 기준

## 의존성
- `spacy` 패키지 및 `en_core_web_sm` 모델
- 기존 모듈: `es_client.load_settings`, `models.Vocabulary`, `models.ExampleSentence`
