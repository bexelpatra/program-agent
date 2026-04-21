# Done Log

### TASK-001 (DONE) - 2026-04-13T21:35
- title: 프로젝트 초기화 (docker-compose, requirements, config/settings.yaml, ES 클라이언트)
- assignee: coder
- summary: Docker Compose(ES 8.x + Kibana), requirements.txt, config/settings.yaml, src/es_client.py, src/__init__.py 생성 완료
- files: projects/abc-english/docker-compose.yml, requirements.txt, config/settings.yaml, src/__init__.py, src/es_client.py

### TASK-002 (DONE) - 2026-04-13T21:40
- title: 데이터 모델 정의 (Pydantic) + ES 인덱스 매핑 생성 (4개 인덱스)
- assignee: coder
- summary: Pydantic 모델 4개(Episode, Sentence, Vocabulary, Expression) + ES 매핑 + create_indices/delete_indices 함수 구현
- files: projects/abc-english/src/models.py

### TASK-003 (DONE) - 2026-04-13T21:50
- title: Collector 구현 - 에피소드 목록 크롤링
- assignee: coder
- summary: collector.py 신규 작성. fetch_episode_list, fetch_episode_detail, collect_all 구현. __NEXT_DATA__ JSON 파싱, pagination, transcript 유무 판별, retry 로직 포함
- files: projects/abc-english/src/collector.py

### TASK-004 (DONE) - 2026-04-13T22:00
- title: Collector 구현 - 공식 transcript 파싱 + MP3 다운로드
- assignee: coder
- summary: parse_transcript, save_transcript, download_mp3 추가. collect_all에 통합. 스트리밍 다운로드, 중복 방지, tqdm 진행률, atomic write 구현
- files: projects/abc-english/src/collector.py (수정)

### TASK-005 (DONE) - 2026-04-13T22:10
- title: Collector 테스트
- assignee: tester
- summary: 48개 테스트 전부 통과. 모든 함수 커버리지 확보. 이슈 없음.
- files: projects/abc-english/tests/test_collector.py

### TASK-006 (DONE/SKIP) - 2026-04-13T22:10
- title: Collector 이슈 수정
- assignee: coder
- summary: TASK-005 테스트에서 이슈 없음. 수정 불필요.

### TASK-007 (DONE) - 2026-04-13T22:10
- title: Transcriber 구현 - Whisper 연동
- assignee: coder
- summary: transcriber.py 신규 작성. load_model, transcribe_audio, save_whisper_transcript, transcribe_episode, transcribe_all 구현. 싱글톤 모델 캐싱, 중복 방지, 배치 처리.
- files: projects/abc-english/src/transcriber.py

### TASK-008 (DONE) - 2026-04-13T22:25
- title: Comparator 구현 - 공식 vs Whisper WER 계산, 문장별 듣기 난이도 산출
- assignee: coder
- summary: comparator.py 신규 작성. calculate_wer(Levenshtein 기반), compare_sentences(greedy alignment), calculate_listening_difficulty(4단계), compare_episode, compare_all 구현.
- files: projects/abc-english/src/comparator.py

### TASK-011 (DONE) - 2026-04-13T22:25
- title: Analyzer 구현 - spaCy 품사 태깅 + NER 인명 필터링 + 기능어 제거 + 단어 빈도 분석
- assignee: coder
- summary: analyzer.py 신규 작성. load_nlp(싱글톤), analyze_text(POS필터+NER필터+lemma빈도), analyze_episode, analyze_all(에피소드간 병합) 구현.
- files: projects/abc-english/src/analyzer.py

### TASK-014 (DONE) - 2026-04-13T22:25
- title: LLM Analyzer 구현 - 프로바이더 추상화
- assignee: coder
- summary: llm_analyzer.py 신규 작성. LLMProvider ABC, AnthropicProvider(Messages API), OllamaProvider(REST API), get_provider 팩토리(싱글톤), _extract_json 헬퍼 구현.
- files: projects/abc-english/src/llm_analyzer.py

### TASK-009 (DONE) - 2026-04-13T22:40
- title: Transcriber + Comparator 테스트
- assignee: tester
- summary: 52개 테스트 전부 통과 (transcriber 19개, comparator 33개). 이슈 없음.
- files: projects/abc-english/tests/test_transcriber.py, tests/test_comparator.py

### TASK-010 (DONE/SKIP) - 2026-04-13T22:40
- title: Transcriber/Comparator 이슈 수정
- assignee: coder
- summary: TASK-009 테스트에서 이슈 없음. 수정 불필요.

### TASK-012 (DONE) - 2026-04-13T22:40
- title: Analyzer 테스트
- assignee: tester
- summary: 20개 테스트 전부 통과. spaCy mock으로 전체 커버리지 확보. 이슈 없음.
- files: projects/abc-english/tests/test_analyzer.py, tests/conftest.py

### TASK-013 (DONE/SKIP) - 2026-04-13T22:40
- title: Analyzer 이슈 수정
- assignee: coder
- summary: TASK-012 테스트에서 이슈 없음. 수정 불필요.

### TASK-015 (DONE) - 2026-04-13T22:40
- title: LLM Analyzer 구현 - 숙어/구동사/관용어 탐지 + 어원 설명 생성
- assignee: coder
- summary: detect_expressions, detect_expressions_for_episode 구현. 원문 전체를 LLM에 전달. 버그 발견: transcript 필드명 "text" → "full_text" 수정 필요.
- files: projects/abc-english/src/llm_analyzer.py (수정)

### TASK-016 (DONE) - 2026-04-13T22:40
- title: LLM Analyzer 구현 - CEFR 난이도 분류 + 한국어 뜻 매핑
- assignee: coder
- summary: classify_vocabulary, classify_vocabulary_for_episode, _get_batch_size 구현. 버그 발견: 파일 경로 및 필드명 수정 필요.
- files: projects/abc-english/src/llm_analyzer.py (수정)

### TASK-020 (DONE) - 2026-04-13T22:40
- title: Loader 구현 - ES bulk 적재
- assignee: coder
- summary: loader.py 신규 작성. load_episodes, load_sentences, load_vocabulary, load_expressions, load_all 구현. elasticsearch.helpers.bulk 사용, bulk_size 설정 적용.
- files: projects/abc-english/src/loader.py

### TASK-017 (DONE) - 2026-04-13T22:50
- title: LLM Analyzer 배치 처리 + 캐싱 + 버그 수정
- assignee: coder
- summary: 3개 버그 수정(transcript 필드명, 파일 경로). SHA-256 기반 파일 캐싱 추가. 5000단어 이상 텍스트 자동 분할 처리 구현.
- files: projects/abc-english/src/llm_analyzer.py (수정)

### TASK-021 (DONE) - 2026-04-13T22:50
- title: Loader 테스트
- assignee: tester
- summary: 31개 테스트 전부 통과. _slug, _bulk_load, load_episodes/sentences/vocabulary/expressions, load_all 커버리지 확보. 이슈 없음.
- files: projects/abc-english/tests/test_loader.py

### TASK-022 (DONE/SKIP) - 2026-04-13T22:50
- title: Loader 이슈 수정
- assignee: coder
- summary: TASK-021 테스트에서 이슈 없음. 수정 불필요.

### TASK-018 (DONE) - 2026-04-13T23:00
- title: LLM Analyzer 테스트
- assignee: tester
- summary: 49개 테스트 전부 통과. 프로바이더, 숙어 탐지, CEFR 분류, 캐싱, 배치 분할 모두 커버. 이슈 없음.
- files: projects/abc-english/tests/test_llm_analyzer.py

### TASK-019 (DONE/SKIP) - 2026-04-13T23:00
- title: LLM Analyzer 이슈 수정
- assignee: coder
- summary: TASK-018 테스트에서 이슈 없음. 수정 불필요.

### TASK-023 (DONE) - 2026-04-13T23:00
- title: CLI 구현
- assignee: coder
- summary: cli.py 신규 작성. Click 기반 9개 명령어: collect, transcribe, compare, analyze, llm-analyze, load, run-all, init-indices, delete-indices. --config 옵션, 로깅 설정 포함.
- files: projects/abc-english/src/cli.py

### TASK-024 (DONE) - 2026-04-13T23:10
- title: CLI 테스트
- assignee: tester
- summary: 18개 테스트 전부 통과. 9개 명령어, _scan_episode_ids, 에피소드 없는 엣지 케이스 커버. 이슈 없음.
- files: projects/abc-english/tests/test_cli.py

### TASK-025 (DONE/SKIP) - 2026-04-13T23:10
- title: CLI 이슈 수정
- assignee: coder
- summary: TASK-024 테스트에서 이슈 없음. 수정 불필요.

### TASK-026 (DONE) - 2026-04-13T23:10
- title: 전체 파이프라인 통합 테스트
- assignee: tester
- summary: 15개 통합 테스트 전부 통과. Collector→Comparator, Analyzer→Loader, LLM→Loader, 데이터 모델 일관성, 전체 파이프라인 E2E 검증. 이슈 없음.
- files: projects/abc-english/tests/test_integration.py

### TASK-027 (DONE/SKIP) - 2026-04-13T23:10
- title: 통합 테스트 이슈 수정
- assignee: coder
- summary: TASK-026 테스트에서 이슈 없음. 수정 불필요.

### TASK-029 (DONE) - 2026-04-14T00:10
- title: 스케줄러 구현 (평일 새 에피소드 자동 감지 + 파이프라인 실행)
- assignee: coder
- summary: APScheduler BlockingScheduler + CronTrigger(day_of_week=mon-fri) 기반. data/transcripts/*_official.json 집합 ↔ collector.fetch_episode_list() 차집합으로 신규 감지. subprocess로 `python -m src.cli run-all` 호출. 주말 이중 가드, 예외 swallow, RotatingFileHandler 로그. CLI `schedule` 명령(--once, --time) 추가.
- report: signal/abc-english/coder-report-TASK-029.md

### TASK-030 (DONE) - 2026-04-14T00:35
- title: ES 신규 인덱스 2개 (abc-user-vocabulary, abc-llm-cache) + Pydantic 모델
- assignee: coder
- summary: UserVocabularyEntry/LlmCacheEntry/SourceEpisodeRef 모델 + INDEX_MAPPINGS에 2개 추가. notebook_store.py (upsert/mark_viewed/list/delete, source_episodes max 20, painless script), llm_cache.py (sha1 cache_key, get/set) 신규. settings.yaml indices 2개 추가. init-indices로 6개 인덱스 생성 확인.
- report: signal/abc-english/coder-report-TASK-030.md

### TASK-031 (DONE) - 2026-04-14T00:45
- title: Ollama 클라이언트 (영어교사 프롬프트, 캐시 연동, idiom 어원 필수, JSON 파싱)
- assignee: coder
- summary: ollama_client.py (async lookup_term / lookup_term_sync / verify_ollama_model + LookupResult). 캐시 우선 → /api/generate(format=json) → idiom etymology 누락 시 1회 재질의 → miss도 cache 저장. 프롬프트 v1(system+user_template) settings에서 override 가능. config에 llm.ollama.host/timeout_seconds/prompt_version/prompts.v1 추가. requirements에 httpx 추가.
- report: signal/abc-english/coder-report-TASK-031.md

### TASK-032 (DONE) - 2026-04-14T01:00
- title: FastAPI 백엔드 (episodes/audio-Range/lookup/notebook API)
- assignee: coder
- summary: web/ 하위 FastAPI 앱 (app.py create_app 팩토리, deps.py, api/{episodes,audio,lookup,notebook}.py). /api/audio는 Range 지원 (200/206/416 + path traversal 방어). /api/notebook POST는 ollama lookup + notebook upsert 연동. startup에서 verify_ollama_model 경고 로그. requirements에 fastapi/uvicorn/jinja2 추가.
- report: signal/abc-english/coder-report-TASK-032.md

### TASK-033 (DONE) - 2026-04-14T01:20
- title: Frontend 공용 (base template, 네비, common.js, CSS)
- assignee: coder
- summary: Jinja2 templates + /static 마운트. HTML 페이지 라우트 3종 (/, /study/{id}, /notebook) web/routes/pages.py. base.html + 스텁 3종 (episodes/study/notebook). 다크모드 기본 CSS. ESM common.js (api/toast/fmtDate/fmtDuration/initNav/setupDrawer). TemplateResponse 신규 시그니처 사용.
- report: signal/abc-english/coder-report-TASK-033.md

### TASK-034 (DONE) - 2026-04-14T01:45
- title: Frontend 학습 페이지
- assignee: coder
- summary: episodes.js (카드 렌더, 제목 검색), study.js (플레이어 + 자막 싱크 + 드래그/클릭 lookup + 드로어). 배속 0.5-2x, 스킵 3s 기본(1-30 설정, localStorage), 키보드 Space/←/→/↑/↓. 자막 싱크 currentIdx 캐시+인접 확인+이진탐색 fallback. 토글 3종 localStorage 영속. 1-6단어 드래그 선택시 lookup 모달. 드로어 N 토글/ESC. node --check syntax OK, uvicorn HTTP 200 확인.
- report: signal/abc-english/coder-report-TASK-034.md

### TASK-035 (DONE) - 2026-04-14T02:00
- title: Frontend 단어장 전용 페이지 (필터/정렬, 출처 에피소드 점프)
- assignee: coder
- summary: notebook.html 툴바(q/term_type/sort) + #notebook-list. notebook.js (ESM): loadList, 펼치기 시 viewed PATCH 자동, confirm 삭제, source 링크 /study/{id}#s={idx}. study.js 최소 패치: data-sentence-index 속성 + handleHashJump 핸들러(hash-flash 1.5s 애니메이션). CSS etymology 보라 좌측 보더, 빈 상태, hash-flash keyframe.
- report: signal/abc-english/coder-report-TASK-035.md

### TASK-036 (DONE) - 2026-04-14T02:15
- title: CLI serve 명령 + 통합 스모크 테스트
- assignee: coder
- summary: cli.py serve 명령 (--host/--port/--reload, ABC_CONFIG env로 factory에 config 전달). create_app이 settings_path=None이면 env fallback. settings.yaml web 블록(host/port). scripts/smoke_web.py (subprocess uvicorn + httpx 9개 엔드포인트 검증 + atexit 종료). README 웹 UI 실행 섹션. SMOKE OK 확인.
- report: signal/abc-english/coder-report-TASK-036.md

### TASK-037 (DONE) - 2026-04-14T02:45
- title: Docker Compose 배포 환경 구축 (nginx + gunicorn, HTTP, host 8081)
- assignee: coder
- summary: deploy/ 하위 Dockerfile(python:3.11-slim + gunicorn), docker-compose.yml(app expose-only 8000 + nginx 8081:80, host.docker.internal:host-gateway, data/config ro 볼륨), nginx.conf(/static alias + / proxy_pass app:8000, Range용 buffering off + HTTP/1.1, read_timeout 300s). settings.docker.yaml (ES/Ollama host.docker.internal 오버라이드). .dockerignore, README Docker 섹션 추가. compose config OK.
- report: signal/abc-english/coder-report-TASK-037.md
