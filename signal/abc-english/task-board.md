# Task Board

| ID | Title | Assignee | Status | Priority | Depends On | Created | Updated |
|----|-------|----------|--------|----------|------------|---------|---------|
| --- | **Phase 1: 인프라 + 수집** | --- | --- | --- | --- | --- | --- |
| TASK-001 | 프로젝트 초기화 (docker-compose, requirements, config/settings.yaml, ES 클라이언트) | coder | DONE | HIGH | - | 2026-04-13T21:00 | 2026-04-13T21:35 |
| TASK-002 | 데이터 모델 정의 (Pydantic) + ES 인덱스 매핑 생성 (4개 인덱스) | coder | DONE | HIGH | TASK-001 | 2026-04-13T21:00 | 2026-04-13T21:40 |
| TASK-003 | Collector 구현 - 에피소드 목록 크롤링 (__NEXT_DATA__ JSON 파싱, pagination, transcript 유무 판별) | coder | DONE | HIGH | TASK-002 | 2026-04-13T21:00 | 2026-04-13T21:50 |
| TASK-004 | Collector 구현 - 공식 transcript 파싱 (div#transcript) + MP3 다운로드 (진행률, 중복방지) | coder | DONE | HIGH | TASK-003 | 2026-04-13T21:00 | 2026-04-13T22:00 |
| TASK-005 | Collector 테스트 | tester | DONE | HIGH | TASK-004 | 2026-04-13T21:00 | 2026-04-13T22:10 |
| TASK-006 | Collector 이슈 수정 (검증 결과 반영) | coder | DONE | HIGH | TASK-005 | 2026-04-13T21:00 | 2026-04-13T22:10 |
| --- | **Phase 2: 음성 변환 + 비교 분석** | --- | --- | --- | --- | --- | --- |
| TASK-007 | Transcriber 구현 - Whisper 연동 (모델 선택, 타임스탬프 추출, 문장 분리) | coder | DONE | HIGH | TASK-001 | 2026-04-13T21:00 | 2026-04-13T22:10 |
| TASK-008 | Comparator 구현 - 공식 vs Whisper WER 계산, 문장별 듣기 난이도 산출 | coder | DONE | HIGH | TASK-004,TASK-007 | 2026-04-13T21:00 | 2026-04-13T22:25 |
| TASK-009 | Transcriber + Comparator 테스트 | tester | DONE | HIGH | TASK-008 | 2026-04-13T21:00 | 2026-04-13T22:40 |
| TASK-010 | Transcriber/Comparator 이슈 수정 | coder | DONE | HIGH | TASK-009 | 2026-04-13T21:00 | 2026-04-13T22:40 |
| --- | **Phase 3: NLP 전처리** | --- | --- | --- | --- | --- | --- |
| TASK-011 | Analyzer 구현 - spaCy 품사 태깅 + NER 인명 필터링 + 기능어 제거 + 단어 빈도 분석 | coder | DONE | HIGH | TASK-004 | 2026-04-13T21:00 | 2026-04-13T22:25 |
| TASK-012 | Analyzer 테스트 | tester | DONE | HIGH | TASK-011 | 2026-04-13T21:00 | 2026-04-13T22:40 |
| TASK-013 | Analyzer 이슈 수정 | coder | DONE | HIGH | TASK-012 | 2026-04-13T21:00 | 2026-04-13T22:40 |
| --- | **Phase 4: LLM 심층 분석** | --- | --- | --- | --- | --- | --- |
| TASK-014 | LLM Analyzer 구현 - 프로바이더 추상화 (Claude API / 로컬 LLM 전환 가능) | coder | DONE | HIGH | TASK-001 | 2026-04-13T21:00 | 2026-04-13T22:25 |
| TASK-015 | LLM Analyzer 구현 - 숙어/구동사/관용어 탐지 + 어원 설명 생성 (원문 전체 입력) | coder | DONE | HIGH | TASK-014 | 2026-04-13T21:00 | 2026-04-13T22:40 |
| TASK-016 | LLM Analyzer 구현 - CEFR 난이도 분류 + 한국어 뜻 매핑 (원문 전체 입력) | coder | DONE | HIGH | TASK-014 | 2026-04-13T21:00 | 2026-04-13T22:40 |
| TASK-017 | LLM Analyzer 구현 - 배치 처리 + 캐싱 (중복 API 호출 방지) + 버그 수정 | coder | DONE | HIGH | TASK-015,TASK-016 | 2026-04-13T21:00 | 2026-04-13T22:50 |
| TASK-018 | LLM Analyzer 테스트 | tester | DONE | HIGH | TASK-017 | 2026-04-13T21:00 | 2026-04-13T23:00 |
| TASK-019 | LLM Analyzer 이슈 수정 | coder | DONE | HIGH | TASK-018 | 2026-04-13T21:00 | 2026-04-13T23:00 |
| --- | **Phase 5: 적재 + CLI** | --- | --- | --- | --- | --- | --- |
| TASK-020 | Loader 구현 - ES bulk 적재 (episodes, sentences, vocabulary, expressions) | coder | DONE | HIGH | TASK-002 | 2026-04-13T21:00 | 2026-04-13T22:40 |
| TASK-021 | Loader 테스트 | tester | DONE | HIGH | TASK-020 | 2026-04-13T21:00 | 2026-04-13T22:50 |
| TASK-022 | Loader 이슈 수정 | coder | DONE | HIGH | TASK-021 | 2026-04-13T21:00 | 2026-04-13T22:50 |
| TASK-023 | CLI 구현 (collect, transcribe, compare, analyze, llm-analyze, load, run-all) | coder | DONE | HIGH | TASK-004,TASK-007,TASK-011,TASK-017,TASK-020 | 2026-04-13T21:00 | 2026-04-13T23:00 |
| TASK-024 | CLI 테스트 | tester | DONE | MEDIUM | TASK-023 | 2026-04-13T21:00 | 2026-04-13T23:10 |
| TASK-025 | CLI 이슈 수정 | coder | DONE | MEDIUM | TASK-024 | 2026-04-13T21:00 | 2026-04-13T23:10 |
| --- | **Phase 6: 통합 + 후순위** | --- | --- | --- | --- | --- | --- |
| TASK-026 | 전체 파이프라인 통합 테스트 (실제 에피소드 1~2개 E2E) | tester | DONE | HIGH | TASK-023 | 2026-04-13T21:00 | 2026-04-13T23:10 |
| TASK-027 | 통합 테스트 이슈 수정 | coder | DONE | HIGH | TASK-026 | 2026-04-13T21:00 | 2026-04-13T23:10 |
| TASK-028 | Kibana 대시보드 구성 (단어 빈도, 난이도 분포, 에피소드별 통계) | coder | TODO | LOW | TASK-022 | 2026-04-13T21:00 | 2026-04-13T21:00 |
| TASK-029 | 스케줄러 구현 (새 에피소드 자동 감지 + 파이프라인 실행) | coder | TODO | LOW | TASK-023 | 2026-04-13T21:00 | 2026-04-13T21:00 |
