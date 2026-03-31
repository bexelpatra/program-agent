# Done Log

(완료된 태스크가 시간순으로 누적된다. Manager가 태스크를 DONE 처리할 때마다 아래에 추가한다.)

### TASK-001 (DONE) - 2026-03-25T18:05
- title: 프로젝트 초기화 (docker-compose, requirements, config, ES 클라이언트)
- assignee: coder
- summary: docker-compose.yml(ES 8.12.0), requirements.txt, src/__init__.py, src/config.py(인덱스 상수 6개), src/es_client.py(CRUD+bulk) 구현. pip install 및 import 검증 완료.
- files: docker-compose.yml, requirements.txt, src/__init__.py, src/config.py, src/es_client.py

### TASK-002 (DONE) - 2026-03-25T18:10
- title: 데이터 모델 + ES 인덱스 매핑 생성
- assignee: coder
- summary: src/models.py 구현. 6개 인덱스 매핑, nori 한국어 analyzer, text+keyword 서브필드, nested verification_log. get_all_mappings(), init_all_indices() 함수.
- files: src/models.py

### TASK-003 (DONE) - 2026-03-25T18:15
- title: YAML 로더 + CLI 기본 커맨드
- assignee: coder
- summary: src/loader.py(YAML→ES 로딩 4함수), src/search.py(검색 6함수), src/cli.py(click CLI 7커맨드), data/fields.yaml(4개 분야 초기 데이터) 구현. import 검증 완료.
- files: src/loader.py, src/search.py, src/cli.py, data/fields.yaml

### TASK-004 (DONE) - 2026-03-25T18:25
- title: 인프라 테스트
- assignee: tester
- summary: 6개 테스트 파일, 83개 테스트 전체 통과. config, es_client, models, loader, search, cli 모든 모듈 커버. 이슈 없음.
- files: tests/__init__.py, tests/test_config.py, tests/test_es_client.py, tests/test_models.py, tests/test_loader.py, tests/test_search.py, tests/test_cli.py

### TASK-005 (DONE) - 2026-03-25T18:25
- title: 서양윤리 데이터 입력 1차 (소크라테스)
- assignee: coder
- summary: data/western/socrates.yaml 작성. thinker 1명, works 6건(변론,크리톤,파이돈,메논,프로타고라스,테아이테토스), claims 10건, keywords 7건, relations 4건. "악법도 법이다"의 정확한 맥락 기술, 그리스어 원문은 불확실하여 빈 문자열 처리.
- files: data/western/socrates.yaml

### TASK-006 (DONE) - 2026-03-26T10:00
- title: 서양윤리 데이터 검증 1차 (소크라테스)
- assignee: tester
- summary: 35개 항목 검증. 정확 27, 수정필요 7, 심각 1. 심각: relations 방향 오류(rel-001~003). 중요: works year 기준 불일관, 프로타고라스 연도, 오타. 경미: term_en 개선, work_id 개선, 맥락 보완.
- files: signal/tester-report-TASK-006.md

### TASK-007 (DONE) - 2026-03-26T10:05
- title: 소크라테스 데이터 이슈 수정 (검증 결과 반영)
- assignee: coder
- summary: 검증 결과 9개 이슈 전부 수정. 심각: relations 방향 오류 3건 수정(influenced_by→influenced, from/to 교정). 중요: works year를 저작 추정 시점으로 통일, 프로타고라스 연도 -385로 수정. 경미: term_en 개선, work_id 변경, 석공 표현 보완, claim-002 context 보완.
- files: data/western/socrates.yaml

### TASK-008 (DONE) - 2026-03-26T10:15
- title: exporter.py 구현 (ES → YAML export)
- assignee: coder
- summary: src/exporter.py 신규 생성 (export_thinker, export_all_thinkers). cli.py에 export, export-all 커맨드 추가. 기존 YAML 형식과 호환.
- files: src/exporter.py, src/cli.py
- tokens: 47,529 (sonnet)

### TASK-009 (DONE) - 2026-03-26T10:20
- title: 소크라테스 수정 데이터 ES 적재 + export 검증
- assignee: coder
- summary: ES 적재 완료 (1 thinker, 6 works, 10 claims, 7 keywords, 4 relations). export round-trip 검증 성공. 버그 수정: elasticsearch-py 9→8 다운그레이드, nori 미설치 시 standard analyzer fallback 추가.
- files: src/models.py, requirements.txt
- tokens: 53,213 (sonnet)

### TASK-010 (DONE) - 2026-03-26T10:40
- title: claims 스키마 보강 + 소크라테스 argument/counterpoint 추가
- assignee: coder
- summary: claims 매핑에 argument, counterpoint 필드 추가. 소크라테스 10개 claim 모두 논증구조(왜?)와 반론/한계 보강. ES 재적재 및 YAML export 완료.
- files: src/models.py, src/loader.py, src/exporter.py, data/western/socrates.yaml
- tokens: 56,887 (sonnet)

### TASK-011 (DONE) - 2026-03-26T11:10
- title: 소크라테스 argument/counterpoint 품질 개선
- assignee: coder
- summary: 10개 claim의 counterpoint에서 "현대 심리학/신경과학/교육학" 등 막연한 출처 제거, 모두 특정 사상가+저서 근거로 교체 (아리스토텔레스 니코마코스윤리학, 에피쿠로스 Kyriai Doxai, 마르크스 독일이데올로기, 키르케고르 불안의개념, 듀이 민주주의와교육, 칸트 도덕형이상학기초 등). argument도 논리적 흐름 보강. YAML export 완료.
- files: data/western/socrates.yaml
- tokens: 37,640 (sonnet)

### TASK-012 (DONE) - 2026-03-26T11:35
- title: 플라톤 데이터 입력 (ES 직접)
- assignee: coder
- summary: ES-first 파이프라인으로 플라톤 데이터 직접 입력. thinker 1건, works 8건(국가,파이돈,향연,파이드로스,메논,티마이오스,법률,필레보스), claims 12건(모두 argument+counterpoint 포함), keywords 10건, relations 5건. CLI study 조회 정상 확인.
- files: scripts/input_plato.py
- tokens: 59,009 (sonnet)

### TASK-013 (DONE) - 2026-03-26T11:45
- title: 플라톤 데이터 검증
- assignee: tester
- summary: 36개 항목 검증. 정확 30, 수정필요 5, 심각 1. 심각: plato-kw-dihairesis work_id 오류(국가→후기 대화편). 경미: claim-003 counterpoint 출처 보완, claim-008 표현 수정, 향연/메논 연도, rel-004 to_thinker 학파명. counterpoint 품질 양호(12/12 특정 사상가+저서 근거).
- files: signal/tester-report-TASK-013.md
- tokens: 56,421 (opus)

### TASK-014 (DONE) - 2026-03-26T11:50
- title: 플라톤 데이터 이슈 수정 (검증 결과 반영)
- assignee: coder
- summary: 검증 결과 4건 수정. 심각: plato-kw-dihairesis work_id를 plato-politeia→plato-phaidros로 변경, definition에 후기 대화편 명시. 경미: claim-003 counterpoint에 NE I.6 출처 보완, claim-008 "암묵적 비판"→"대조" 표현 수정, rel-004 to_thinker를 neoplatonism→plotinus로 변경.
- files: (ES 직접 수정)
- tokens: 41,353 (sonnet)

### TASK-015 (DONE) - 2026-03-26T12:10
- title: 아리스토텔레스 데이터 입력 (ES 직접)
- assignee: coder
- summary: ES-first 파이프라인으로 아리스토텔레스 데이터 직접 입력. thinker 1건, works 8건(니코마코스윤리학,정치학,형이상학,영혼에관하여,시학,분석론후서,자연학,에우데모스윤리학), claims 12건(모두 argument+counterpoint 포함), keywords 10건, relations 5건.
- files: scripts/insert_aristotle.py
- tokens: 58,502 (sonnet)

### TASK-016 (DONE) - 2026-03-26T12:20
- title: 아리스토텔레스 데이터 검증
- assignee: tester
- summary: 38개 항목 검증. 정확 32, 수정필요 6, 심각 0. 경미: EE significance 해석, claim-008 그리스어 음역, claim-010 counterpoint 출처, keyword 엔텔레케이아 work_id, rel aristotle→kant evidence, rel aristotle→mill 관계 명시. counterpoint 품질 양호(11/12 정확).
- files: signal/tester-report-TASK-016.md
- tokens: 47,387 (opus)

### TASK-017 (DONE) - 2026-03-26T12:25
- title: 아리스토텔레스 데이터 이슈 수정 (검증 결과 반영)
- assignee: coder
- summary: 검증 결과 6건 수정. EE significance 통설 반영, claim-008 그리스어 음역 수정(to diorthotikon), claim-010 counterpoint 출처 경제학-철학수고로 변경, keyword 엔텔레케이아 work_id metaphysica로 변경, rel aristotle→kant evidence 정리, rel aristotle→mill 간접적 관계 명시.
- files: (ES 직접 수정)
- tokens: 44,145 (sonnet)

### TASK-018 (DONE) - 2026-03-26T12:35
- title: 아우구스티누스 데이터 입력 (ES 직접)
- assignee: coder
- summary: 축소 규모로 아우구스티누스 데이터 입력. thinker 1건, works 5건(고백록,신국론,자유의지론,삼위일체론,은총과자유의지), claims 8건(모두 argument+counterpoint), keywords 7건, relations 4건.
- files: (ES 직접 입력)
- tokens: 42,842 (sonnet)

### TASK-019 (DONE) - 2026-03-26T12:40
- title: 아우구스티누스 데이터 검증
- assignee: tester
- summary: 25개 항목 검증. 심각 2건(조명설 source_detail 부정확, 원죄 에페소공의회→카르타고공의회), 보통 5건(privatio boni 출처/원문, 시간론 원문, 은총/두도성론 counterpoint 저서명 미명시), 경미 2건. counterpoint 품질 양호.
- files: signal/tester-report-TASK-019.md
- tokens: 37,104 (opus)

### TASK-020 (DONE) - 2026-03-26T12:45
- title: 아우구스티누스 데이터 이슈 수정 (검증 결과 반영)
- assignee: coder
- summary: 7건 수정. 심각: 조명설 source_detail 제9권/14~15권으로 수정, 원죄 에페소공의회→카르타고공의회(418) 수정. 보통: privatio boni 출처/원문, 시간론 원문 전문, 은총 칼뱅 Institutio 명시, 두도성론 오로시우스 Historiarum 명시.
- files: (ES 직접 수정)
- tokens: 34,000 (sonnet)

### TASK-021 (DONE) - 2026-03-26T13:05
- title: 토마스 아퀴나스 데이터 입력 (ES 직접)
- assignee: coder
- summary: ES-first 파이프라인으로 토마스 아퀴나스 데이터 입력. thinker 1건, works 6건(신학대전,대이교도대전,진리론,악론,존재와본질,니코마코스윤리학주석), claims 10건(모두 argument+counterpoint, 9/10 라틴어 원문), keywords 8건, relations 4건.
- files: scripts/insert_aquinas.py
- tokens: 86,665 (sonnet)

### TASK-022 (DONE) - 2026-03-26T13:10
- title: 토마스 아퀴나스 데이터 검증
- assignee: tester
- summary: 29개 항목 검증. 정확 23, 수정필요(경미) 5, 수정필요(보통) 1, 심각 0. 보통: 신학대전 year 1274→1265. 경미: 대이교도대전 year, claim-007 출처 순서, claim-008 아우구스티누스 인용 명시, claim-009 ST 출처 q.48→q.48-49, rel-003 evidence 명확화.
- files: signal/tester-report-TASK-022.md
- tokens: 70,594 (opus)

### TASK-028 (DONE) - 2026-03-30T00:15
- title: 칸트 데이터 이슈 수정 (검증 결과 반영)
- assignee: coder
- summary: 4건 수정. 경미: kant-lectures-ethics year 1780→1775(Collins 노트 기준), significance에 강의록 시기 명시. kant-claim-017 에세이 제목/독일어 원제 추가·8:425→8:423. kant-claim-018 페이지 범위 KpV 5:22~26, 35~41로 조정. 보통: aristotle-rel-004 description을 "영향" 관계에 부합하도록 재기술.
- files: (ES 직접 수정)
- tokens: 28,745 (sonnet)

### TASK-026 (DONE) - 2026-03-30T00:01
- title: original_text_ko 필드 스키마 추가 (models.py)
- assignee: coder
- summary: ethics-claims 인덱스 ES 매핑 및 src/models.py에 original_text_ko 필드(text, korean/standard analyzer) 추가. PUT mapping으로 실제 ES 인덱스에 반영 확인.
- files: src/models.py
- tokens: 25,846 (sonnet)

### TASK-027 (DONE) - 2026-03-30T00:05
- title: 칸트 claims 한국어 번역 추가 (ES update)
- assignee: coder
- summary: 칸트 18개 claim 전부 original_text_ko 필드에 자연스러운 한국어 번역 추가 완료. 독일어 핵심 용어 괄호 병기, 표준 철학 번역어(선의지, 정언명법, 준칙, 자율성, 경외 등) 사용. 모든 ES update result: "updated" 확인.
- files: (ES 직접 수정)
- tokens: 34,066 (sonnet)

### TASK-025 (DONE) - 2026-03-30T00:10
- title: 칸트 데이터 검증
- assignee: tester
- summary: 47개 항목 검증. 정확 41, 수정필요(경미) 4, 수정필요(보통) 1, 심각 0. original_text(독일어 원문)·original_text_ko(한국어 번역) 품질 양호. 수정 필요: kant-lectures-ethics year(1780→1775), kant-claim-017 에세이 제목/페이지(8:425→8:423), kant-claim-018 페이지 범위 조정(선택), aristotle-rel-004 description 초점 조정.
- files: signal/tester-report-TASK-025.md
- tokens: 89,097 (opus)

### TASK-023 (DONE) - 2026-03-26T13:15
- title: 토마스 아퀴나스 데이터 이슈 수정 (검증 결과 반영)
- assignee: coder
- summary: 6건 수정. 보통: 신학대전 year 1274→1265. 경미: 대이교도대전 year 1265→1259, claim-007 source_detail SCG 우선 재배치, claim-008 아우구스티누스 인용 명시, claim-009 source_detail q.48→q.48-49, rel-003 evidence 핀니스 문헌 성격 명확화.
- files: (ES 직접 수정)
- tokens: 40,998 (sonnet)
