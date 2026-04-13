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

## 현재 상태
- 프로젝트 초기화 단계
- 태스크 분해 완료, 실행 대기 중
