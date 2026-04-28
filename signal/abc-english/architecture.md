# Architecture

## 개요

ABC News Daily 팟캐스트 에피소드를 수집하여 영어 학습 자료로 변환하는 시스템.
공식 transcript가 있는 에피소드만 대상으로 하며, 음성 데이터도 함께 저장하여 청취 학습에 활용한다.

### 목적
- 뉴스 영어 어휘/숙어/구동사/관용어 자동 추출 및 구조화
- CEFR 난이도 분류로 수준별 학습 지원
- 음성(Whisper) vs 공식 transcript 비교를 통한 듣기 난이도 분석
- ELK 스택 기반 검색/시각화

### 데이터 소스
- URL: https://www.abc.net.au/listen/programs/abc-news-daily
- 에피소드 수: ~250개 (지속 업데이트)
- 에피소드 길이: ~15분
- 로그인: 불필요 (공개 페이지)
- Transcript: `div#transcript`가 있는 에피소드만 대상. 없으면 skip.

---

## 기술 스택

| 영역 | 기술 | 이유 |
|------|------|------|
| 언어 | Python 3.11+ | NLP/ML 생태계 |
| 크롤링 | requests + BeautifulSoup | 공개 페이지, JS 렌더링 불필요 (__NEXT_DATA__ JSON) |
| 음성→텍스트 | OpenAI Whisper (base/small) | 무료, 오프라인, 타임스탬프 추출 |
| NLP 전처리 | spaCy (en_core_web_sm) | 품사 태깅, NER(인명 필터링), 기능어 제거 |
| 심층 분석 | LLM (Claude Haiku 또는 로컬 LLM) | 숙어 탐지, 어원 설명, 난이도 분류, 한국어 뜻 |
| 데이터 저장 | Elasticsearch 8.x | 전문 검색, 집계 |
| 시각화 | Kibana | ES 기본 연동 (후순위) |
| 컨테이너 | Docker Compose | ES + Kibana 간편 배포 |
| 설정 | YAML | 사이트별/모델별 설정 분리 |
| CLI | Click | 명령줄 인터페이스 |

---

## 파이프라인 아키텍처

```
1. Collector (수집)
   - 에피소드 목록 크롤링 (__NEXT_DATA__ JSON 파싱, pagination)
   - div#transcript 존재 여부 확인 → 없으면 skip
   - 공식 transcript 텍스트 파싱 및 저장
   - MP3 다운로드 (중복 방지, 진행률 표시)
        │
        ▼
2. Transcriber (음성 변환)
   - MP3 → Whisper transcript 생성 (타임스탬프 포함)
   - 문장 단위 분리
        │
        ▼
3. Comparator (비교 분석)
   - 공식 transcript vs Whisper transcript WER 계산
   - 문장별 듣기 난이도 점수 산출
   - 고난이도 구간 표시
        │
        ▼
   ┌────────────────────────────────────────┐
   │  4, 5번은 원문을 각각 독립적으로 처리 (병렬 가능)  │
   └────────────────────────────────────────┘
        │                        │
        ▼                        ▼
4. Analyzer (어휘 전용)     5. LLM Analyzer (심층 분석)
   - 입력: 원문 전체            - 입력: 원문 전체 (필터링 없이!)
   - spaCy 품사 태깅            - 숙어(idiom) 탐지 + 어원/유래 설명
   - NER 인명/고유명사 필터링    - 구동사(phrasal verb) 탐지
   - 기능어 제거                - 관용어(collocation) 탐지
   - 단어 빈도 집계             - CEFR 난이도 분류 (A1~C2)
   - 출력: vocabulary 데이터    - 한국어 뜻 매핑
        │                      - 배치 처리 + 캐싱
        │                        │
        └───────────┬────────────┘
                    ▼
6. Loader (적재)
   - Elasticsearch bulk 적재
   - 인덱스 관리
        │
        ▼
7. (후순위) Kibana 대시보드, 스케줄러
```

### 중요: 전처리 순서 원칙
- **LLM에게는 반드시 원문 전체를 전달한다** (기능어/인명 제거하지 않은 상태)
- spaCy 필터링은 **어휘(vocabulary) 빈도 집계 전용**으로만 사용
- 이유: 전처리로 기능어를 먼저 제거하면 구동사(give up), 관용어(kick the bucket),
  관용구(at the end of the day) 등의 패턴이 파괴되어 LLM이 탐지 불가
- 4번과 5번은 서로 독립적이므로 병렬 실행 가능

---

## 디렉토리 구조

```
projects/abc-english/
├── docker-compose.yml
├── requirements.txt
├── config/
│   └── settings.yaml           # 크롤링/Whisper/ES/LLM 설정
├── data/
│   ├── audio/                  # MP3 파일
│   └── transcripts/            # 공식 transcript + Whisper transcript (JSON)
├── src/
│   ├── __init__.py
│   ├── collector.py            # 에피소드 수집, transcript 파싱, MP3 다운로드
│   ├── transcriber.py          # Whisper STT
│   ├── comparator.py           # 공식 vs Whisper 비교, WER 계산
│   ├── analyzer.py             # spaCy NLP 전처리 (품사, NER, 필터링)
│   ├── llm_analyzer.py         # LLM 기반 심층 분석 (숙어, 어원, 난이도, 한국어)
│   ├── loader.py               # ES 적재
│   ├── models.py               # 데이터 모델 (Pydantic)
│   ├── es_client.py            # ES 연결 관리
│   └── cli.py                  # CLI 진입점
├── tests/
│   ├── __init__.py
│   ├── test_collector.py
│   ├── test_transcriber.py
│   ├── test_comparator.py
│   ├── test_analyzer.py
│   ├── test_llm_analyzer.py
│   └── test_loader.py
└── kibana/
    └── dashboards.ndjson       # (후순위)
```

---

## 데이터 모델

### episodes 인덱스 (`abc-episodes`)
```json
{
  "episode_id": "106551254",
  "title": "Alan Kohler's case to nationalise childcare",
  "description": "...",
  "published_date": "2026-04-12T16:00:00+00:00",
  "duration_seconds": 980,
  "url": "/listen/programs/abc-news-daily/{slug}/{id}",
  "audio_url": "https://mediacore-live-production.akamaized.net/audio/.../{hash}.mp3",
  "official_transcript": "전체 공식 transcript 텍스트",
  "whisper_transcript": "Whisper 변환 텍스트",
  "has_transcript": true,
  "sentence_count": 120,
  "word_count": 2500,
  "avg_wer": 0.08,
  "processed_at": "2026-04-13T00:00:00Z"
}
```

### sentences 인덱스 (`abc-sentences`)
```json
{
  "episode_id": "106551254",
  "sentence_index": 15,
  "official_text": "The government has been under increasing pressure to act.",
  "whisper_text": "The government has been under increasing pressure to act.",
  "start_time": 125.3,
  "end_time": 129.1,
  "wer": 0.0,
  "listening_difficulty": "easy",
  "content_words": ["government", "increasing", "pressure", "act"],
  "difficulty": "B2"
}
```

### vocabulary 인덱스 (`abc-vocabulary`)
```json
{
  "word": "unprecedented",
  "pos": "ADJ",
  "definition_en": "never done or known before",
  "definition_ko": "전례 없는",
  "difficulty": "C1",
  "frequency": 12,
  "episodes": ["106551254", "106548018"],
  "example_sentences": [
    {
      "episode_id": "106551254",
      "text": "This is an unprecedented move by the government."
    }
  ]
}
```

필터링 대상 (적재 제외):
- 관사: a, an, the
- 대명사: I, you, he, she, it, we, they, ...
- 전치사: in, on, at, to, for, ...
- 접속사: and, but, or, ...
- 조동사: is, am, are, was, were, do, does, did, have, has, had, ...
- 인명/고유명사: spaCy NER의 PERSON 엔티티

### expressions 인덱스 (`abc-expressions`)
```json
{
  "phrase": "take the fall",
  "type": "idiom | phrasal_verb | collocation",
  "definition_en": "to accept blame or punishment for something",
  "definition_ko": "대신 책임을 지다, 희생양이 되다",
  "etymology": "Originally from the idea of a person literally falling or being knocked down, later adopted in criminal slang in the early 20th century to mean accepting punishment on behalf of someone else.",
  "difficulty": "B2",
  "frequency": 3,
  "episodes": ["106535374"],
  "example_sentences": [
    {
      "episode_id": "106535374",
      "text": "Will Pete Hegseth take the fall for the Iran war?"
    }
  ]
}
```

---

## 설계 결정

### 1. Transcript 우선, 없으면 skip
- 결정: div#transcript가 있는 에피소드만 처리, 없으면 건너뜀
- 이유: transcript가 있어야 정확한 텍스트 분석 가능. Whisper만으로는 오류 위험.
- Whisper는 보조 역할 (음성 vs 텍스트 비교용)

### 2. Whisper 유지 (비교 분석용)
- 결정: MP3를 Whisper로 변환하여 공식 transcript와 비교
- 이유: WER 기반 듣기 난이도 분석, 타임스탬프 기반 구간 분할
- 대안: Whisper 제거 → 듣기 분석 불가

### 3. spaCy + LLM 이원화
- 결정: spaCy로 전처리(품사, NER, 필터링), LLM으로 심층 분석(숙어, 어원, 난이도)
- 이유: 기능어/인명 필터링은 spaCy가 빠르고 저렴. 의미 분석은 LLM이 정확.
- LLM은 배치로 실행하여 비용 절감

### 4. LLM 유연성
- 결정: Claude API (Haiku/Sonnet) 또는 로컬 LLM (Ollama) 선택 가능
- 이유: 비용 상황에 따라 전환 가능하도록 설정 파일에서 제어
- 구현: settings.yaml의 llm.provider 설정으로 분기

### 5. 기능어/인명 필터링
- 결정: 관사, 전치사, 접속사, 조동사, 인명 등 제외
- 이유: 학습 가치 낮은 단어가 빈도 상위를 차지하는 것 방지
- 구현: spaCy POS 태그 + NER PERSON 엔티티 기반

### 6. 관용어 어원 설명 필수
- 결정: 숙어/관용어 저장 시 왜 그런 뜻을 가지는지 etymology 필드 필수
- 이유: 단순 뜻 암기보다 유래를 알면 기억에 남고 이해도 향상
- 구현: LLM이 어원/유래 설명 생성

---

## 웹 학습 UI (2026-04-14 추가)

### 목적
브라우저에서 에피소드를 골라 듣고, 자막 싱크·단어 즉시 조회·단어장 관리까지 한 곳에서 수행한다.

### 스택
- Backend: FastAPI (기존 ES 클라이언트/모델 재사용), `httpx.AsyncClient`로 Ollama 호출, uvicorn 서빙
- Frontend: 단일 페이지 정적 HTML 3종(`/`, `/study/{id}`, `/notebook`) + vanilla JS 모듈. 빌드 도구 없음.
- 템플릿: Jinja2 (서버사이드 초기 렌더링) + 이후 fetch API로 상호작용
- 오디오: `<audio>` + HTTP Range 스트리밍 (서버에서 Range 헤더 수동 처리)
- LLM: Ollama HTTP API (`http://localhost:11434/api/generate`), 모델 기본 `gemma4:e2b` (설정으로 변경 가능)

### 디렉토리
```
projects/abc-english/web/
├── __init__.py
├── app.py              # FastAPI 앱
├── api/
│   ├── episodes.py     # /api/episodes, /api/episodes/{id}
│   ├── audio.py        # /api/audio/{id} (Range 지원)
│   ├── lookup.py       # /api/lookup (ollama + 캐시)
│   └── notebook.py     # /api/notebook CRUD
├── templates/
│   ├── base.html
│   ├── episodes.html
│   ├── study.html
│   └── notebook.html
└── static/
    ├── css/app.css
    └── js/
        ├── common.js
        ├── study.js
        └── notebook.js
```

### 신규 데이터 모델

#### abc-user-vocabulary (단어장)
```json
{
  "term": "take the fall",
  "term_type": "idiom | phrasal_verb | word",
  "explanation_en": "...",
  "etymology": "...",           // idiom일 때 필수
  "added_count": 3,
  "view_count": 12,
  "first_added": "2026-04-14T10:00:00Z",
  "last_added": "2026-04-20T15:00:00Z",
  "last_viewed": "2026-04-22T20:00:00Z",
  "source_episodes": [
    {"episode_id": "106551254", "sentence_index": 15, "added_at": "2026-04-14T10:00:00Z"}
  ],
  "note": ""                    // 사용자 메모
}
```
key: `term`(lowercase, 공백 정규화).

#### abc-llm-cache (Ollama 응답 캐시)
```json
{
  "cache_key": "sha1(term + model + prompt_version)",
  "term": "...",
  "model": "gemma4:e2b",
  "prompt_version": "v1",
  "response": { "term_type": "...", "explanation_en": "...", "etymology": "...", "examples": [] },
  "created_at": "2026-04-14T10:00:00Z"
}
```

### 주요 API
| Method | Path | 설명 |
|--------|------|------|
| GET | /api/episodes | 에피소드 목록 (published_date desc) |
| GET | /api/episodes/{id} | 에피소드 상세 + sentences (timestamps 포함) |
| GET | /api/audio/{id} | MP3 스트리밍 (Range 지원) |
| POST | /api/lookup | {term, context?} → ollama 질의 + 캐시. 캐시 hit 시 즉시 반환 |
| GET | /api/notebook | 단어장 목록 (sort/filter) |
| POST | /api/notebook | 단어장 추가/업서트 (added_count++, source_episodes append) |
| PATCH | /api/notebook/{term}/viewed | last_viewed 갱신, view_count++ |
| DELETE | /api/notebook/{term} | 단어장에서 제거 |

### Ollama 프롬프트 규격 (prompt_version: v1)
System: "You are an expert English teacher helping Korean learners with news English."
User 입력: term + 선택적 context 문장.
지시:
- term의 유형을 판별: `word` / `phrasal_verb` / `idiom` / `collocation`
- 영어 설명(explanation_en) 작성
- **idiom이면 etymology(왜 그런 뜻이 되었는지) 반드시 포함**
- 2~3개 예문 제공
- 출력은 JSON (Pydantic 파싱)

### UI/UX 결정
- **학습 페이지**: 오디오 플레이어(재생/정지/배속 0.5~2x/앞뒤 스킵 **기본 3초, 설정 가능**) + 전체 스크립트 토글 + 자막 하이라이트 토글. 단어 클릭 또는 드래그 선택 → lookup 모달. "단어장 추가" 버튼 → ollama 설명까지 함께 저장.
- **우측 슬라이드 드로어**(단어장 프리뷰): `N` 단축키(input focus 시 비활성) 또는 우상단 버튼으로 토글. 드로어 열려도 학습 영역은 유지. 단어 추가 시 드로어 닫혀있으면 뱃지 카운터 +1 애니메이션.
- **단어장 전용 페이지**: 필터(term_type), 정렬(last_added/added_count/last_viewed), 출처 에피소드 클릭 → 해당 에피소드 학습 페이지로 점프.

### 설계 결정
- **캐시와 단어장 이중 저장**: 캐시는 term 기반 영구, 단어장은 캐시 스냅샷 복사. 사용자가 단어장 설명을 개인 수정할 여지를 남김.
- **자막 싱크 최적화**: 현재 세그먼트 인덱스를 JS에서 캐시하고 `timeupdate`마다 인접 범위만 체크 (O(1) 전환).
- **Path traversal 방지**: 오디오 엔드포인트는 `episode_id`만 입력받고 파일명은 서버에서 결정.
- **Ollama 모델명 검증**: 서버 시작 시 `ollama /api/tags` 호출, 없으면 경고 로그. 질의는 설정값 그대로 시도.
- **인증 없음**: 로컬 단일 사용자 도구.

---

## Phase 9: ELK 학습 실습 (2026-04-15 추가)

### 목적
사용자는 ELK 스택 초심자. 목표는 "대시보드를 만든다"가 **아니라** "면접/이직에서 설명 가능한 수준으로 ELK 개념을 익힌다"이다. 실행 산출물보다 **학습 노트**가 중심 결과물.

### 산출물
```
projects/abc-english/
├── docs/
│   ├── elk-learning.md          # TASK-038: ES 구조 학습 노트 (인덱스/매핑/shard/analyzer)
│   ├── elk-queries.md           # TASK-039: DSL 쿼리 10종 카탈로그 (주석+실행결과)
│   └── elk-interview-notes.md   # TASK-041: 면접 답변 수준 요약
└── kibana/
    └── dashboards.ndjson        # TASK-040: Kibana export
```

### 학습 단계 원칙
- **멈춤 포인트**: 각 태스크마다 사용자가 직접 curl/Dev Tools로 쿼리를 찔러볼 수 있도록 Coder는 **재현 가능한 명령 예제**를 학습 노트에 남긴다.
- **자기 언어로 쓰기**: 노트는 위키 요약 복붙 금지. "왜 이렇게 동작하는가"를 본인 문장으로 정리.
- **시각 자료**: Kibana 대시보드는 스크린샷 대신 `dashboards.ndjson`으로 export해 재현 가능하게 저장.

### 4개 인덱스 기준 시각화 (TASK-040)
| 패널 | 소스 인덱스 | 타입 | 목적 |
|------|-------------|------|------|
| 단어 빈도 Top 20 | abc-vocabulary | Bar (horizontal) | 학습 가치 높은 어휘 식별 |
| CEFR 난이도 분포 | abc-vocabulary + abc-expressions | Donut | 전체 컨텐츠 수준 파악 |
| 에피소드별 평균 WER | abc-episodes | Bar (time) | 듣기 난이도 추이 |
| Expressions 타입 카운트 | abc-expressions | Metric + Table | idiom/phrasal_verb/collocation 비율 |

