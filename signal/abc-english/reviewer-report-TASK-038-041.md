---
task_id: TASK-038,TASK-039,TASK-040,TASK-041
verdict: NEEDS_REVISION
---

# Reviewer Report: TASK-038 ~ TASK-041 (Phase 9 ELK 학습 실습)

## 검증 대상
- 파일:
  - `signal/abc-english/task-board.md` (Phase 9 섹션, 라인 50~54)
  - `signal/abc-english/architecture.md` (Phase 9 섹션, 라인 356~383)
  - `projects/abc-english/src/models.py` (INDEX_MAPPINGS, 라인 263~)
  - `projects/abc-english/src/loader.py` (라인 62/89/134/161)
  - `projects/abc-english/` 디렉토리 실존 목록
- Manager 주장 요약:
  - TASK-028을 DONE 처리하고 TASK-038~041 4개 태스크로 분해했다.
  - Phase 9 목적은 ELK 학습(면접/이직 대비)이며 산출물은 docs 3개 + kibana ndjson 1개.
  - 4개 ES 인덱스(abc-episodes/sentences/vocabulary/expressions)는 이미 구현·적재되어 있다.

## 검증 결과

### 파일 존재

| 경로 | 존재 | 비고 |
|------|------|------|
| `signal/abc-english/task-board.md` Phase 9 | O | TASK-038~041 정상 등록, TASK-028은 DONE(분해됨 표기) |
| `signal/abc-english/architecture.md` Phase 9 | O | 라인 356~383, 산출물 경로/패널 테이블 포함 |
| `projects/abc-english/src/models.py` INDEX_MAPPINGS | O | 라인 263 — 4개 인덱스 매핑 정의 |
| `projects/abc-english/src/loader.py` | O | abc-episodes/sentences/vocabulary/expressions 4개 적재 함수 |
| `projects/abc-english/docs/` | X | 아직 없음 (TASK-038/039/041이 생성해야 함 — 정상) |
| `projects/abc-english/kibana/` | X | 아직 없음 (TASK-040에서 생성해야 함 — 정상) |

### 내용 일치

- **4개 인덱스 정의**: 주장 → 실제 일치.
  - `src/models.py:263` INDEX_MAPPINGS에 4개 모두 정의.
  - `src/loader.py` 62/89/134/161에 각 인덱스별 load 함수 존재.
  - 근거: `grep -n "abc-(episodes|sentences|vocabulary|expressions)" src/` 5건 매칭.
- **아키텍처 패널 테이블(라인 378~383)** vs 실제 인덱스 필드:
  - 단어 빈도 Top 20: `abc-vocabulary.word / frequency` → 모델에 존재(word, frequency).
  - CEFR 분포: `abc-vocabulary.difficulty + abc-expressions.difficulty` → 모델에 존재.
  - 에피소드별 avg WER: `abc-episodes.avg_wer + published_date` → 모델에 존재.
  - Expressions 타입: `abc-expressions.type` → 모델에 존재.
  - 판정: 시각화 소스 필드 매칭 OK.
- **task-board TASK-028 처리**: DONE + "(분해됨 → TASK-038~041)" 표기 — 일관성 OK.
- **의존성**: TASK-038→039→040→041 체인, TASK-038은 TASK-022(Loader 이슈 수정, DONE) 선행. DONE 상태 확인됨.

### 태스크 완결성

- **TASK-038**: "CLI로 mapping/shard/analyzer 조회"만 적혀 있고, 구체적 명령(예: `GET /abc-episodes/_mapping`, `_cat/shards`, `_analyze`)이 빠져 있다. Coder가 "CLI"를 `esctl`/`curl`/Kibana Dev Tools 중 어느 것으로 해석할지 모호. 학습 노트에 포함할 최소 섹션 목차(역색인/analyzer/shard/replica/mapping 타입)도 열거되지 않아 완결성 부족.
- **TASK-039**: 10종 쿼리 유형은 명시되었으나, "실행 대상 인덱스"가 지정되지 않았다. abc-english 4개 인덱스 중 어느 필드를 사용할지 (예: `match`는 `official_transcript`, `term`은 `difficulty.keyword`, `nested`는 `example_sentences`) 예시 바인딩이 없어 Coder가 임의 선택하게 된다. 또한 "실행 결과 요약"의 형식(JSON 응답 일부 / hit 수 / took_ms?)이 정해지지 않음.
- **TASK-040**: 가장 취약.
  - Data View 이름 지정 없음 (각 인덱스당 Data View인지, 패턴 `abc-*` 1개인지).
  - Lens 시각화 4종의 "집계 종류"가 명시되지 않음 (예: 단어 빈도 Top 20은 Terms aggregation on `word.keyword` sorted by `sum(frequency)` desc인지, 아니면 doc count인지).
  - `sentences`/`episodes`의 time field(`published_date`)를 Data View 생성 시 지정해야 한다는 사실이 누락.
  - export 명령(Kibana Stack Management → Saved Objects → Export) 절차 미기재.
  - Kibana 접속 URL/포트(docker-compose의 Kibana host port)에 대한 안내 없음.
- **TASK-041**: 주제 5개는 열거되었으나 "면접 답변 수준"의 측정 기준(각 항목 최소 길이/예시 포함 여부)이 없어 Coder가 "1줄 정의"로 끝낼 가능성. 또한 "자기 언어로 쓰기" 지침이 태스크 설명에는 없고 architecture.md Phase 9 원칙에만 있어 Coder 프롬프트로 전달되지 않을 위험.

### 학습 목적 강조 — Coder 지시 전달 가능성

- architecture.md Phase 9 "학습 단계 원칙" 블록(라인 372~375)에 "자기 언어로 쓰기", "재현 가능한 명령 예제", "위키 복붙 금지"가 명시됨.
- 그러나 task-board.md TASK-038~041 **설명 셀 자체**에는 "자기 언어로 작성"이라는 문구가 TASK-038에만 들어가 있고 039/040/041에는 없음. Coder는 Manager 프롬프트로 architecture.md 참조 지시를 받지만, 태스크 설명이 최우선 가이드이므로 모든 태스크 설명에 "학습 노트 성격(복붙 금지, 본인 문장)" 문구가 명시되어야 한다.

### 의존성·순서

- TASK-038→039→040→041 선형 의존, 병렬 가능성 없음 (같은 `docs/`에 순차 작성). 문제 없음.
- TASK-022 DONE 확인 완료.

## 판정
**NEEDS_REVISION**

인덱스/모델/로더 쪽 전제는 모두 실제와 일치하고, Phase 9 산출물 경로도 일관적이다. 그러나 **태스크 설명이 Coder 단독 실행 기준으로는 불완전**하다 — 특히 TASK-040(Kibana 조작 절차)과 TASK-039(쿼리 인덱스/필드 바인딩). 이 상태로 Coder에 넘기면 Coder가 임의 해석을 해 학습 목적과 어긋난 산출물이 나올 가능성이 높다.

## 수정 요청

1. **task-board.md TASK-038 설명 보강**
   - 사용할 조회 명령을 예시로 명시: `GET /{index}/_mapping`, `GET /_cat/shards/abc-*?v`, `POST /abc-episodes/_analyze {"analyzer":"standard","text":"..."}`.
   - 학습 노트에 포함할 소제목 5개 명시: "역색인 원리 / analyzer 파이프라인 / shard·replica / mapping 타입 / dynamic mapping".

2. **task-board.md TASK-039 설명 보강**
   - 각 쿼리 유형별로 사용할 **대상 인덱스·필드**를 바인딩. 예:
     - match → `abc-episodes.official_transcript`
     - term → `abc-vocabulary.difficulty.keyword`
     - bool → `abc-sentences` (difficulty=B2 AND wer>0.1)
     - range → `abc-sentences.wer`
     - aggs → `abc-vocabulary` terms on `word.keyword`
     - nested → `abc-vocabulary.example_sentences` (nested 매핑 여부 먼저 확인)
     - multi_match → `abc-episodes.title + description`
     - prefix/fuzzy → `abc-vocabulary.word`
     - highlight → `abc-episodes.official_transcript`
   - 실행 결과 요약 포맷: "hits.total.value, took(ms), 상위 3 hit 요약 3줄" 규격 명시.
   - 주의: `nested` 예제 전, 실제 매핑이 nested type인지 `GET /abc-vocabulary/_mapping`으로 먼저 확인하라는 단계 포함.

3. **task-board.md TASK-040 설명 보강 (최우선)**
   - Kibana 접속: `docker-compose.yml`의 Kibana 포트 확인 후 해당 URL 접속. 접근 불가 시 `docker compose up kibana` 재실행.
   - Data View: 단일 `abc-*` 패턴 1개 생성, time field는 `abc-episodes.published_date` 기준 (또는 각 인덱스별 개별 Data View 4개 — 둘 중 선택 기준 명시).
   - Lens 4종 **집계 스펙**:
     - 단어 빈도 Top 20: horizontal bar, X=`Sum of frequency`, Y=Terms `word.keyword` size=20, sort by sum desc.
     - CEFR 분포: donut, slice by Terms `difficulty.keyword` across `abc-vocabulary,abc-expressions`.
     - 에피소드별 avg WER: bar, X=Date histogram `published_date` (weekly), Y=Average `avg_wer`.
     - Expressions 타입: metric + table, Terms `type.keyword` count.
   - 대시보드 이름: `ABC English Learning Overview`.
   - Export 절차 명시: Stack Management → Saved Objects → 대시보드 선택 → Export (include related) → 파일을 `projects/abc-english/kibana/dashboards.ndjson`로 저장. 해당 디렉토리를 `mkdir -p projects/abc-english/kibana` 로 먼저 생성.

4. **task-board.md TASK-041 설명 보강**
   - 각 항목 최소 분량 기준: "질문 → 3~5줄 답변 + 1개 이상 예제(abc-english 인덱스 기반)" 포맷.
   - "위키 복붙 금지, 본인 문장, ES vs RDB 비교는 join/스키마/확장성 3축 필수" 추가.

5. **공통: 모든 Phase 9 태스크 설명에 학습 원칙 문구 추가**
   - "학습 노트 성격: 위키 복붙 금지. 본인 문장으로 '왜 이렇게 동작하는가'를 기술할 것." 을 TASK-038~041 description 끝에 공통으로 삽입.

6. **architecture.md Phase 9 디렉토리 명시 보강 (선택)**
   - `kibana/dashboards.ndjson` 생성 전 `mkdir` 필요함을 각주로 남겨 Coder가 경로 생성을 빠뜨리지 않게.

## Manager에게 전달

- 인프라(인덱스·모델·로더)와 산출물 경로 체계는 정상. Coder 호출은 **태스크 설명 보강 후** 다시 Reviewer에 돌려 PASS 확인 바람.
- 특히 TASK-040은 Kibana 조작 경험이 없는 Coder에게는 "마법 지시"가 된다. Lens 집계 스펙을 반드시 명시해야 학습 목적대로 "본인이 aggregation을 설계했다"는 노트가 나온다.
- `kibana/` 디렉토리가 미생성 상태인 것은 정상이나, TASK-040 설명에 생성 단계를 넣지 않으면 Coder가 export 단계에서 실패할 수 있다.
