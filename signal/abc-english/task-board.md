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
| TASK-028 | (분해됨 → TASK-038~041, Phase 9 참조) Kibana 대시보드 구성 | coder | DONE | LOW | TASK-022 | 2026-04-13T21:00 | 2026-04-15T10:00 |
| TASK-029 | 스케줄러 구현 (평일 새 에피소드 자동 감지 + 파이프라인 실행) | coder | DONE | LOW | TASK-023 | 2026-04-13T21:00 | 2026-04-14T00:10 |
| --- | **Phase 7: 웹 학습 UI** | --- | --- | --- | --- | --- | --- |
| TASK-030 | ES 신규 인덱스 2개 (abc-user-vocabulary, abc-llm-cache) + Pydantic 모델 | coder | DONE | HIGH | TASK-002 | 2026-04-14T00:20 | 2026-04-14T00:35 |
| TASK-031 | Ollama 클라이언트 (영어교사 프롬프트, 캐시 연동, idiom 어원 필수, JSON 파싱) | coder | DONE | HIGH | TASK-030 | 2026-04-14T00:20 | 2026-04-14T00:45 |
| TASK-032 | FastAPI 백엔드 (episodes/audio-Range/lookup/notebook API) | coder | DONE | HIGH | TASK-031 | 2026-04-14T00:20 | 2026-04-14T01:00 |
| TASK-033 | Frontend 공용 (base template, 네비, common.js, CSS) | coder | DONE | MEDIUM | TASK-032 | 2026-04-14T00:20 | 2026-04-14T01:20 |
| TASK-034 | Frontend 학습 페이지 (플레이어 + 자막 싱크 + 단어/드래그 lookup + 우측 드로어) | coder | DONE | HIGH | TASK-033 | 2026-04-14T00:20 | 2026-04-14T01:45 |
| TASK-035 | Frontend 단어장 페이지 (필터/정렬, 출처 에피소드 점프) | coder | DONE | MEDIUM | TASK-033 | 2026-04-14T00:20 | 2026-04-14T02:00 |
| TASK-036 | CLI serve 명령 + 통합 스모크 테스트 | coder | DONE | MEDIUM | TASK-032,TASK-034,TASK-035 | 2026-04-14T00:20 | 2026-04-14T02:15 |
| --- | **Phase 8: 배포 환경 (Docker Compose: nginx + gunicorn)** | --- | --- | --- | --- | --- | --- |
| TASK-037 | Docker Compose 배포 환경 구축 (nginx + gunicorn, HTTP, host 8081) | coder | DONE | MEDIUM | TASK-036 | 2026-04-14T02:30 | 2026-04-14T02:45 |
| --- | **Phase 9: ELK 학습 실습 (면접/이직 대비, 학습 우선)** | --- | --- | --- | --- | --- | --- |
| TASK-038 | ES 기본 개념 실습: 4개 인덱스(abc-episodes/sentences/vocabulary/expressions)에 대해 `GET /{index}/_mapping`, `GET /_cat/shards/abc-*?v`, `POST /{index}/_analyze {"analyzer":"standard","text":"..."}` 실행 결과를 `docs/elk-learning.md`에 기록하고 소제목 5개(역색인 원리 / analyzer 파이프라인 / shard·replica / mapping 타입 / dynamic mapping)로 정리. 학습 노트 성격: 위키 복붙 금지, 본인 문장으로 "왜 이렇게 동작하는가" 기술. Kibana Dev Tools(`http://localhost:5601` → Dev Tools) 기준 명령 사용 | user | TODO | MEDIUM | TASK-022 | 2026-04-15T10:00 | 2026-04-15T10:00 |
| TASK-039 | DSL 쿼리 카탈로그 `docs/elk-queries.md` 작성. 10종 쿼리 각각 지정 인덱스·필드로 실행: ① match→abc-episodes.official_transcript ② term→abc-vocabulary.difficulty.keyword ③ bool→abc-sentences(difficulty=B2 AND wer>0.1) ④ range→abc-sentences.wer ⑤ aggs→abc-vocabulary terms on word.keyword ⑥ nested→abc-vocabulary.example_sentences (매핑 nested 여부 먼저 `GET /abc-vocabulary/_mapping`으로 확인) ⑦ multi_match→abc-episodes.title+description ⑧ prefix→abc-vocabulary.word ⑨ fuzzy→abc-vocabulary.word ⑩ highlight→abc-episodes.official_transcript. 각 예제마다 (a) DSL 전체 (b) 주석(왜 이 쿼리인가) (c) 실행 결과 요약: `hits.total.value`, `took(ms)`, 상위 3 hit 3줄. 학습 노트 성격: 본인 문장 | user | TODO | MEDIUM | TASK-038 | 2026-04-15T10:00 | 2026-04-15T10:00 |
| TASK-040 | Kibana 대시보드 구성. 사전: `mkdir -p projects/abc-english/kibana`, Kibana 접속(`docker-compose.yml`의 Kibana 포트 확인, 기본 5601). Data View: 패턴 `abc-*` 1개, time field=`published_date`. Lens 4종 집계 스펙: (1) 단어 빈도 Top 20 — horizontal bar, X=Sum of `frequency`, Y=Terms `word.keyword` size=20, sort sum desc (source: abc-vocabulary) (2) CEFR 난이도 분포 — donut, Terms `difficulty.keyword` (source: abc-vocabulary+abc-expressions) (3) 에피소드별 avg WER — bar, X=Date histogram `published_date` weekly, Y=Average `avg_wer` (source: abc-episodes) (4) Expressions 타입 — metric+table, Terms `type.keyword` count (source: abc-expressions). 대시보드 이름 `ABC English Learning Overview` 저장. Export: Stack Management → Saved Objects → 대시보드 선택 → Export (include related) → `projects/abc-english/kibana/dashboards.ndjson`에 저장. 학습 노트 성격: 본인 문장으로 "각 집계를 왜 이렇게 설계했는가"를 `docs/elk-learning.md`에 "2. Kibana 시각화" 섹션으로 추가 | user | TODO | MEDIUM | TASK-039 | 2026-04-15T10:00 | 2026-04-15T10:00 |
| TASK-041 | ELK 면접 노트 `docs/elk-interview-notes.md` 작성. 5개 항목 각각 (질문 → 3~5줄 답변 → abc-english 인덱스 기반 예제 1개): (1) ES vs RDB — join/스키마/확장성 3축 필수 비교 (2) 역색인 원리 (3) analyzer 동작 (char filter → tokenizer → token filter) (4) aggregation 종류(metric/bucket/pipeline) (5) Kibana 구성요소(Discover/Lens/Dashboard/Data View). 학습 노트 성격: 위키 복붙 금지, 본인 문장 | user | TODO | LOW | TASK-040 | 2026-04-15T10:00 | 2026-04-15T10:00 |
