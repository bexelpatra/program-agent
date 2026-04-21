# ABC News Daily English Study

ABC News Daily 팟캐스트 에피소드를 수집하여 영어 학습 자료로 자동 변환하는 시스템.

---

## 목적

- 뉴스 영어 어휘/숙어/구동사/관용어를 자동 추출하고 구조화
- CEFR 난이도 분류(A1~C2)로 수준별 학습 지원
- 음성(Whisper) vs 공식 transcript 비교를 통한 듣기 난이도 분석
- Elasticsearch + Kibana 기반 검색/시각화

---

## 빠른 시작

### 1. 사전 요구사항

- Python 3.11+
- Docker & Docker Compose (Elasticsearch, Kibana용)
- (선택) Anthropic API Key 또는 Ollama (LLM 분석용)

### 2. 설치

```bash
cd projects/abc-english

# 가상환경 생성 및 활성화
python -m venv .venv
source .venv/bin/activate

# 의존성 설치
pip install -r requirements.txt

# spaCy 영어 모델 다운로드
python -m spacy download en_core_web_sm
```

### 3. Elasticsearch 실행

```bash
docker-compose up -d
```

- Elasticsearch: http://localhost:9200
- Kibana: http://localhost:5601

### 4. LLM 설정

기본 설정은 Ollama + gemma4:e2b 모델을 사용한다.

```bash
# Ollama 설치 후 gemma4:e2b 모델 다운로드
ollama pull gemma4:e2b

# Ollama 서버가 실행 중인지 확인 (기본: http://localhost:11434)
ollama list
```

Claude API를 사용하려면 `config/settings.yaml`에서 `llm.provider`를 `"anthropic"`으로 변경하고:
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

### 5. 실행

```bash
# 전체 파이프라인 한 번에 실행
python -m src.cli run-all

# 또는 단계별 실행
python -m src.cli collect       # 에피소드 수집
python -m src.cli transcribe    # Whisper 음성 변환
python -m src.cli compare       # WER 비교 분석
python -m src.cli analyze       # spaCy 어휘 분석
python -m src.cli llm-analyze   # LLM 심층 분석
python -m src.cli load          # Elasticsearch 적재
```

### 웹 UI 실행

`python -m src.cli serve`로 FastAPI 기반 학습 웹 UI를 띄운다.

### Docker로 배포 (학습용 HTTP 배포)

`deploy/` 디렉토리에는 nginx(리버스 프록시) + gunicorn(uvicorn worker) 조합으로
FastAPI 앱을 실행하는 학습용 Docker Compose 설정이 있다. 기존
`projects/abc-english/docker-compose.yml` (ES + Kibana 전용)과는 **별개 스택**이며
건드리지 않는다.

```bash
cd projects/abc-english/deploy
docker compose up -d --build
# → http://localhost:8081 (nginx가 /static은 직접, 나머지는 app:8000으로 프록시)

docker compose logs -f
docker compose down
```

전제 조건:

- 호스트에서 Elasticsearch(9200), Ollama(11434)가 이미 실행 중이어야 한다.
  컨테이너는 `host.docker.internal`로 호스트의 두 서비스에 접근한다.
- 설정은 `config/settings.docker.yaml`이 자동 적용된다 (`ABC_CONFIG` 환경변수).

주의:

- `python -m src.cli serve`도 기본 포트가 **8081**이므로, Docker 스택과 동시에 실행할 수 없다.
  Docker로 띄우기 전에 개발용 `serve`는 반드시 중단할 것.
- HTTPS/도메인 설정은 포함하지 않는다. 외부 공개 용도가 아닌 로컬 학습용 구성이다. 기본 포트는 `http://127.0.0.1:8080`이며, `--host`/`--port`로 바인딩을 변경하거나 `--reload`로 개발용 자동 리로드를 활성화할 수 있다 (`config/settings.yaml`의 `web.host`/`web.port` 값이 있으면 CLI 옵션이 없을 때 그 값을 사용한다). 학습 페이지 단축키: `N`은 다음 문장으로 이동, `Space`는 오디오 재생/일시정지, 좌/우 화살표는 이전/다음 문장, 상/하 화살표는 어휘 패널 탐색에 사용한다.

---

## CLI 명령어

모든 명령어는 `python -m src.cli` 접두사로 실행한다.

| 명령어 | 설명 |
|--------|------|
| `collect` | ABC News Daily 에피소드 수집 (목록 크롤링, transcript 파싱, MP3 다운로드) |
| `transcribe` | 수집된 MP3를 Whisper로 텍스트 변환 |
| `compare` | 공식 transcript와 Whisper 결과 간 WER 비교, 듣기 난이도 산출 |
| `analyze` | spaCy로 품사 태깅, 인명 필터링, 기능어 제거, 단어 빈도 분석 |
| `llm-analyze` | LLM으로 숙어/구동사/관용어 탐지, CEFR 분류, 한국어 뜻 매핑 |
| `load` | 분석 결과를 Elasticsearch에 bulk 적재 |
| `run-all` | 위 6단계를 순차 실행 |
| `schedule` | 평일 정해진 시각에 새 에피소드를 자동 감지하여 `run-all` 실행 (포그라운드 데몬) |
| `serve` | FastAPI 웹 UI 기동 (기본 `http://127.0.0.1:8080`) |
| `init-indices` | Elasticsearch 인덱스 생성 |
| `delete-indices` | Elasticsearch 인덱스 삭제 (확인 프롬프트) |

### 스케줄러 사용법

`python -m src.cli schedule`은 `config/settings.yaml`의 `scheduler` 블록을 읽어 평일(월~금) 지정 시각(기본 KST 09:00)에 `data/transcripts/*_official.json`의 기존 에피소드 ID와 ABC 최신 listing을 비교한다. 신규 ID가 있을 때만 `run-all`을 subprocess로 실행하고, 결과는 `data/scheduler.log`에 기록된다. 즉시 1회 테스트 실행은 `--once`, 실행 시각 오버라이드는 `--time HH:MM`을 사용한다.

### 공통 옵션

```bash
python -m src.cli --config path/to/settings.yaml <command>
```

- `--config`: 설정 파일 경로 (기본: `config/settings.yaml`)

---

## 파이프라인 구조

```
1. Collector (수집)
   - ABC News Daily 에피소드 목록 크롤링 (__NEXT_DATA__ JSON 파싱)
   - div#transcript 존재 여부 확인 (없으면 skip)
   - 공식 transcript 텍스트 파싱 및 JSON 저장
   - MP3 다운로드 (중복 방지, 진행률 표시)
        |
        v
2. Transcriber (음성 변환)
   - MP3 -> Whisper transcript 생성 (타임스탬프 포함)
   - 문장 단위 분리 (segments)
        |
        v
3. Comparator (비교 분석)
   - 공식 transcript vs Whisper transcript WER 계산
   - 문장별 듣기 난이도 점수 산출 (easy/medium/hard/very_hard)
   - 고난이도 구간 표시
        |
        v
   +------------------------------+
   |  4, 5번은 독립적으로 처리     |
   +------------------------------+
        |                    |
        v                    v
4. Analyzer (어휘)     5. LLM Analyzer (심층)
   - spaCy 품사 태깅      - 숙어(idiom) 탐지 + 어원 설명
   - NER 인명 필터링       - 구동사(phrasal verb) 탐지
   - 기능어 제거           - 관용어(collocation) 탐지
   - 단어 빈도 집계        - CEFR 난이도 분류 (A1~C2)
   - -> vocabulary         - 한국어 뜻 매핑
        |                  - 배치 처리 + 캐싱
        |                    |
        +--------+-----------+
                 v
6. Loader (적재)
   - Elasticsearch bulk 적재
   - 4개 인덱스: episodes, sentences, vocabulary, expressions
        |
        v
7. (후순위) Kibana 대시보드, 스케줄러
```

### 중요 원칙

- **LLM에게는 원문 전체를 전달한다** (기능어/인명 제거하지 않은 상태)
- spaCy 필터링은 **어휘 빈도 집계 전용**으로만 사용
- 이유: 전처리로 기능어를 먼저 제거하면 구동사(give up), 관용어(kick the bucket) 패턴이 파괴됨

---

## 디렉토리 구조

```
projects/abc-english/
├── docker-compose.yml          # ES 8.x + Kibana
├── requirements.txt            # Python 의존성
├── README.md                   # 이 문서
├── config/
│   └── settings.yaml           # 크롤링/Whisper/ES/LLM/spaCy 설정
├── data/
│   ├── audio/                  # 다운로드된 MP3 파일
│   ├── transcripts/            # transcript JSON 파일
│   │   ├── {id}_official.json  # 공식 transcript
│   │   └── {id}_whisper.json   # Whisper 변환 결과
│   └── cache/
│       └── llm/                # LLM 응답 캐시 (SHA-256 해시 키)
├── src/
│   ├── __init__.py
│   ├── cli.py                  # CLI 진입점 (Click)
│   ├── collector.py            # 에피소드 수집, transcript 파싱, MP3 다운로드
│   ├── transcriber.py          # Whisper 음성 변환
│   ├── comparator.py           # WER 계산, 듣기 난이도 분류
│   ├── analyzer.py             # spaCy NLP 어휘 분석
│   ├── llm_analyzer.py         # LLM 프로바이더 + 숙어 탐지 + CEFR 분류
│   ├── loader.py               # Elasticsearch bulk 적재
│   ├── models.py               # Pydantic 모델 + ES 인덱스 매핑
│   └── es_client.py            # ES 연결 관리
└── tests/
    ├── __init__.py
    ├── conftest.py             # 공용 mock 설정
    ├── test_collector.py       # 48개 테스트
    ├── test_transcriber.py     # 19개 테스트
    ├── test_comparator.py      # 33개 테스트
    ├── test_analyzer.py        # 20개 테스트
    ├── test_llm_analyzer.py    # 49개 테스트
    ├── test_loader.py          # 31개 테스트
    ├── test_cli.py             # 18개 테스트
    └── test_integration.py     # 15개 통합 테스트
```

---

## 데이터 모델

### episodes (`abc-episodes`)

에피소드 단위 메타데이터.

| 필드 | 타입 | 설명 |
|------|------|------|
| episode_id | keyword | 고유 식별자 |
| title | text | 에피소드 제목 |
| description | text | 설명 |
| published_date | date | 발행일 |
| duration_seconds | integer | 길이(초) |
| url | keyword | 에피소드 URL |
| audio_url | keyword | MP3 URL |
| official_transcript | text | 공식 transcript 전문 |
| whisper_transcript | text | Whisper 변환 전문 |
| has_transcript | boolean | transcript 존재 여부 |
| sentence_count | integer | 문장 수 |
| word_count | integer | 단어 수 |
| avg_wer | float | 평균 WER |

### sentences (`abc-sentences`)

문장 단위 비교 데이터.

| 필드 | 타입 | 설명 |
|------|------|------|
| episode_id | keyword | 소속 에피소드 |
| sentence_index | integer | 문장 순서 |
| official_text | text | 공식 텍스트 |
| whisper_text | text | Whisper 텍스트 |
| start_time | float | 시작 시간(초) |
| end_time | float | 종료 시간(초) |
| wer | float | Word Error Rate |
| listening_difficulty | keyword | easy / medium / hard / very_hard |
| difficulty | keyword | CEFR 레벨 |

### vocabulary (`abc-vocabulary`)

어휘 빈도 및 정의.

| 필드 | 타입 | 설명 |
|------|------|------|
| word | keyword | 단어 (lemma) |
| pos | keyword | 품사 (spaCy POS 태그) |
| definition_en | text | 영어 뜻 |
| definition_ko | text | 한국어 뜻 |
| difficulty | keyword | CEFR 레벨 (A1~C2) |
| frequency | integer | 출현 빈도 |
| episodes | keyword[] | 출현 에피소드 목록 |
| example_sentences | nested | 예문 (episode_id, text) |

필터링 대상 (적재 제외): 관사, 대명사, 전치사, 접속사, 조동사, 인명/고유명사

### expressions (`abc-expressions`)

숙어, 구동사, 관용어.

| 필드 | 타입 | 설명 |
|------|------|------|
| phrase | keyword | 표현 원문 |
| type | keyword | idiom / phrasal_verb / collocation |
| definition_en | text | 영어 뜻 |
| definition_ko | text | 한국어 뜻 |
| etymology | text | 어원/유래 설명 |
| difficulty | keyword | CEFR 레벨 |
| frequency | integer | 출현 빈도 |
| episodes | keyword[] | 출현 에피소드 목록 |
| example_sentences | nested | 예문 |

---

## 설정 파일 (`config/settings.yaml`)

```yaml
crawling:
  base_url: "https://www.abc.net.au"
  program_url: "https://www.abc.net.au/listen/programs/abc-news-daily"
  request_delay: 1.0        # 요청 간 대기(초)
  request_timeout: 30
  user_agent: "ABCEnglishStudy/1.0"
  max_retries: 3

whisper:
  model: "base"             # base | small | medium | large
  language: "en"
  device: "cpu"             # cpu | cuda (GPU 사용 시)

elasticsearch:
  host: "localhost"
  port: 9200
  scheme: "http"
  indices:
    episodes: "abc-episodes"
    sentences: "abc-sentences"
    vocabulary: "abc-vocabulary"
    expressions: "abc-expressions"
  bulk_size: 500

llm:
  provider: "anthropic"     # anthropic | ollama
  anthropic:
    model: "claude-3-haiku-20240307"
    max_tokens: 4096
    batch_size: 10          # 배치당 단어/문장 수
  ollama:
    model: "llama3"
    base_url: "http://localhost:11434"
    batch_size: 5

spacy:
  model: "en_core_web_sm"
  filter_pos: [DET, PRON, ADP, CCONJ, SCONJ, AUX, PUNCT, SPACE, SYM, NUM, PART]
  filter_ner: [PERSON]

data:
  audio_dir: "data/audio"
  transcript_dir: "data/transcripts"
```

### 주요 설정 변경 가이드

| 상황 | 변경할 항목 |
|------|------------|
| GPU로 Whisper 가속 | `whisper.device: "cuda"` |
| 더 정확한 Whisper 모델 | `whisper.model: "medium"` 또는 `"large"` |
| LLM을 Claude로 전환 | `llm.provider: "anthropic"` + ANTHROPIC_API_KEY 설정 |
| Ollama 모델 변경 | `llm.ollama.model: "모델명"` (예: `gemma4:e2b`, `llama3`) |
| 크롤링 속도 조절 | `crawling.request_delay` 값 조정 |
| ES 배치 크기 조정 | `elasticsearch.bulk_size` 값 조정 |

---

## 모듈 상세

### collector.py

ABC News Daily 웹사이트에서 에피소드를 수집한다.

- **데이터 소스**: Next.js SSR 페이지의 `__NEXT_DATA__` JSON
- **Transcript**: `div#transcript` 요소가 있는 에피소드만 대상
- **출력 파일**: `data/transcripts/{episode_id}_official.json`, `data/audio/{episode_id}.mp3`
- **중복 방지**: 이미 존재하는 파일은 자동 skip
- **에러 처리**: 개별 에피소드 실패 시 로그 후 계속 진행

### transcriber.py

OpenAI Whisper를 사용하여 MP3를 텍스트로 변환한다.

- **모델 캐싱**: 싱글톤 패턴으로 모델 1회 로딩
- **출력 파일**: `data/transcripts/{episode_id}_whisper.json`
- **출력 형식**: `{"episode_id": "...", "segments": [{"text": "...", "start": 0.0, "end": 5.2}], "full_text": "..."}`
- **중복 방지**: Whisper JSON이 이미 존재하면 skip

### comparator.py

공식 transcript와 Whisper 결과를 비교한다.

- **WER 계산**: Levenshtein distance 기반 (단어 단위, 소문자+구두점 제거 후)
- **문장 매칭**: Greedy forward alignment (공식 문장 순서대로 Whisper segments를 누적 매칭)
- **듣기 난이도**: WER 임계값 기반 4단계 분류

| WER 범위 | 난이도 |
|----------|--------|
| 0.00 ~ 0.05 | easy |
| 0.05 ~ 0.15 | medium |
| 0.15 ~ 0.30 | hard |
| 0.30+ | very_hard |

### analyzer.py

spaCy를 사용하여 어휘를 분석한다.

- **품사 태깅**: 각 토큰의 POS 태그 부여
- **NER 필터링**: PERSON 엔티티에 속하는 토큰 제거
- **기능어 필터링**: 설정의 `filter_pos`에 해당하는 품사 제거
- **빈도 집계**: lemma(원형) 기반 (word, pos) 키로 집계
- **예문**: 단어별 최대 3개 예문 수집
- **배치 처리**: 여러 에피소드 간 동일 단어 빈도 합산

### llm_analyzer.py

LLM을 사용하여 심층 분석을 수행한다.

**프로바이더 추상화:**
- `AnthropicProvider`: Claude API (Messages API)
- `OllamaProvider`: 로컬 Ollama REST API
- `settings.yaml`의 `llm.provider` 값으로 전환

**숙어/구동사/관용어 탐지:**
- 원문 전체를 LLM에 전달
- 각 표현에 대해: phrase, type, 영/한 뜻, 어원(etymology), CEFR 난이도

**CEFR 분류 + 한국어 뜻:**
- 단어 리스트 + 원문 컨텍스트를 LLM에 전달
- 문맥 기반 뜻과 난이도 분류
- 배치 단위 처리 (설정의 `batch_size`)

**캐싱:**
- SHA-256 해시 기반 파일 캐시 (`data/cache/llm/`)
- 동일 입력에 대한 LLM 중복 호출 방지
- 텍스트가 5000단어 이상이면 자동 분할 처리

### loader.py

분석 결과를 Elasticsearch에 적재한다.

- **bulk API**: `elasticsearch.helpers.bulk` 사용
- **Document ID 규칙**:
  - episodes: `{episode_id}`
  - sentences: `{episode_id}_{sentence_index}`
  - vocabulary: `{word}_{pos}`
  - expressions: slug화된 phrase (소문자, 공백→하이픈)
- **배치 크기**: `elasticsearch.bulk_size` 설정 (기본 500)

---

## 테스트

```bash
cd projects/abc-english

# 전체 테스트 실행
python -m pytest tests/ -v

# 특정 모듈 테스트
python -m pytest tests/test_collector.py -v
python -m pytest tests/test_comparator.py -v

# 통합 테스트만
python -m pytest tests/test_integration.py -v
```

**테스트 현황**: 233개 전부 통과

| 테스트 파일 | 테스트 수 | 대상 |
|-------------|-----------|------|
| test_collector.py | 48 | 크롤링, transcript 파싱, MP3 다운로드 |
| test_transcriber.py | 19 | Whisper 연동, 싱글톤, 배치 |
| test_comparator.py | 33 | WER 계산, 문장 매칭, 난이도 |
| test_analyzer.py | 20 | spaCy 분석, 필터링, 빈도 |
| test_llm_analyzer.py | 49 | 프로바이더, 숙어 탐지, CEFR, 캐싱 |
| test_loader.py | 31 | ES bulk 적재, ID 생성 |
| test_cli.py | 18 | CLI 명령어 |
| test_integration.py | 15 | 모듈 간 데이터 흐름 E2E |

모든 외부 의존성(HTTP, Whisper, spaCy, LLM API, ES)은 mock 처리되어 네트워크/서비스 없이 실행 가능.

---

## 기술 스택

| 영역 | 기술 | 이유 |
|------|------|------|
| 언어 | Python 3.11+ | NLP/ML 생태계 |
| 크롤링 | requests + BeautifulSoup | 공개 페이지, JS 렌더링 불필요 |
| 음성→텍스트 | OpenAI Whisper | 무료, 오프라인, 타임스탬프 |
| NLP | spaCy (en_core_web_sm) | 품사 태깅, NER |
| 심층 분석 | Claude Haiku / Ollama | 숙어 탐지, 어원, 난이도 |
| 저장 | Elasticsearch 8.x | 전문 검색, 집계 |
| 시각화 | Kibana | ES 기본 연동 |
| 컨테이너 | Docker Compose | ES + Kibana 간편 배포 |
| 설정 | YAML | 사이트별/모델별 설정 분리 |
| CLI | Click | 명령줄 인터페이스 |
| 검증 | Pydantic | 데이터 모델 유효성 |

---

## Java 개발자를 위한 Python 기초 가이드

이 프로젝트는 Python으로 작성되어 있다. Java에 익숙하다면 아래 대응 관계를 참고하면 빠르게 이해할 수 있다.

### Java vs Python 핵심 개념 대응표

| 개념 | Java | Python (이 프로젝트) |
|------|------|----------------------|
| 프로젝트 구조 | `src/main/java/com/example/` | `src/` (패키지 = 디렉토리) |
| 진입점 | `public static void main(String[] args)` | `if __name__ == "__main__":` |
| 패키지 선언 | `package com.example;` | `__init__.py` 파일이 디렉토리에 존재하면 패키지 |
| 의존성 관리 | `pom.xml` (Maven) / `build.gradle` | `requirements.txt` |
| 의존성 설치 | `mvn install` | `pip install -r requirements.txt` |
| 인터페이스/추상 클래스 | `interface` / `abstract class` | `ABC` + `@abstractmethod` |
| DTO / VO | Record, POJO | `Pydantic BaseModel` (자동 검증 포함) |
| 타입 | 컴파일 타임 강제 | 타입 힌트 (런타임에 강제하지 않음, 가이드용) |
| 빌드 | `mvn package` → JAR | 빌드 없음 (인터프리터 언어, 소스 직접 실행) |
| 실행 | `java -jar app.jar` | `python -m src.cli run-all` |
| 테스트 | JUnit | pytest |
| 싱글톤 | `static` 필드 + `getInstance()` | 모듈 레벨 변수 (`_client = None`) |
| Getter/Setter | `getXxx()` / `setXxx()` | 직접 필드 접근 (`episode.title`) |
| null | `null` | `None` |
| import | `import com.example.Collector;` | `from .collector import collect_all` |

### Python 파일 구조 기본

```python
# 1. 모듈 독스트링 — Java의 Javadoc 클래스 주석과 비슷
"""Episode collector for ABC News Daily."""

# 2. import — Java와 동일한 위치
import json                          # 표준 라이브러리 (java.util.*)
import requests                      # 외부 라이브러리 (Maven 의존성)
from .models import Episode          # 같은 패키지 내 import (. = 현재 패키지)

# 3. 모듈 레벨 변수 — Java의 static 필드
logger = logging.getLogger(__name__)

# 4. 함수 정의 — Java의 static 메서드와 비슷
def collect_all(settings: dict) -> list:
    """에피소드를 전부 수집한다."""  # ← 독스트링 (Javadoc 역할)
    ...

# 5. 클래스 정의 — Java 클래스와 동일한 개념
class LLMProvider(ABC):              # ABC = Java의 abstract class
    @abstractmethod                  # Java의 abstract 메서드
    def generate(self, prompt: str) -> str:
        ...
```

**Java와 가장 큰 차이점:**
- Python에는 `public`, `private` 키워드가 없다. `_변수명`(언더스코어 접두사)은 "private 의도"를 나타내는 관례일 뿐, 실제로 접근을 막지 않는다.
- 하나의 `.py` 파일에 클래스와 함수가 함께 존재할 수 있다. Java처럼 "하나의 파일 = 하나의 클래스"가 아니다.
- `self`는 Java의 `this`와 같다. 다만 메서드 파라미터에 명시적으로 적어야 한다.

### `__init__.py`란?

```
src/
├── __init__.py          ← 이 파일이 있으면 src/는 "패키지"
├── collector.py
├── analyzer.py
└── models.py
```

Java에서 `package com.example;`을 선언하는 것처럼, Python은 디렉토리에 `__init__.py` 파일이 있으면 그 디렉토리를 패키지로 인식한다. 이 파일은 비어있어도 되고(이 프로젝트에서는 독스트링 한 줄만 있음), 패키지 초기화 코드를 넣을 수도 있다.

### `requirements.txt`란?

Java의 `pom.xml`이나 `build.gradle`에 해당하는 의존성 목록이다.

```txt
requests>=2.31.0         # Java의 OkHttp/Apache HttpClient 역할
beautifulsoup4>=4.12.0   # HTML 파서 (Java의 Jsoup)
openai-whisper>=20231117 # 음성→텍스트 변환
spacy>=3.7.0             # NLP 라이브러리
elasticsearch>=8.13.0    # ES 클라이언트 (Java의 RestHighLevelClient)
anthropic>=0.25.0        # Claude API 클라이언트
pyyaml>=6.0.1            # YAML 파서 (Java의 SnakeYAML)
click>=8.1.0             # CLI 프레임워크 (Java의 picocli)
pydantic>=2.6.0          # 데이터 검증 (Java의 Bean Validation + Record)
```

설치 명령: `pip install -r requirements.txt` (Maven의 `mvn install`에 해당)

### 가상환경(venv)이란?

Java에는 없는 Python 고유 개념이다. 프로젝트마다 독립된 라이브러리 공간을 만든다.

```bash
# 가상환경 생성 (프로젝트 디렉토리 안에 .venv 폴더 생성)
python -m venv .venv

# 가상환경 활성화 (이후 pip install은 이 환경에만 설치됨)
source .venv/bin/activate

# 비활성화
deactivate
```

Java에서 Maven/Gradle이 프로젝트별 `~/.m2` 캐시를 관리하는 것과 비슷하지만, Python은 기본적으로 시스템 전역에 라이브러리를 설치하기 때문에 가상환경으로 격리해야 프로젝트 간 버전 충돌을 방지할 수 있다.

---

## 아키텍처 상세 설명

### 전체 구조 (Java 관점)

```
이 프로젝트를 Java Spring Boot로 비유하면:

src/
├── __init__.py            → 패키지 선언 (package-info.java)
├── cli.py                 → @SpringBootApplication + Controller 역할
│                            (사용자 명령을 받아 적절한 Service를 호출)
├── models.py              → Entity/DTO 클래스들 (Episode, Sentence, ...)
├── es_client.py           → DataSource 설정 + @Bean(싱글톤) ES 클라이언트
├── collector.py           → Service: 웹 크롤링 담당
├── transcriber.py         → Service: 음성→텍스트 변환 담당
├── comparator.py          → Service: 텍스트 비교 분석 담당
├── analyzer.py            → Service: NLP 어휘 분석 담당
├── llm_analyzer.py        → Service: LLM API 호출 담당 (Strategy 패턴)
└── loader.py              → Repository: Elasticsearch 적재 담당
```

### 모듈 간 관계

```
                        cli.py (진입점)
                           │
        ┌──────────┬───────┼───────┬───────────┐
        │          │       │       │           │
        ▼          ▼       ▼       ▼           ▼
   collector   transcriber comparator analyzer  llm_analyzer
        │          │       │       │           │
        └──────────┴───────┴───────┴───────────┘
                           │
                      models.py  (공통 데이터 모델)
                      es_client.py (공통 설정/DB 연결)
                           │
                           ▼
                      loader.py → Elasticsearch
```

### 디자인 패턴 (Java 용어로 설명)

**1. Strategy 패턴 — LLM 프로바이더 전환**

```python
# Java의 interface + 구현체 전환과 같은 구조

class LLMProvider(ABC):           # ← Java: interface LLMProvider
    @abstractmethod
    def generate(self, prompt):   # ← Java: String generate(String prompt);
        ...

class AnthropicProvider(LLMProvider):  # ← Java: class AnthropicProvider implements LLMProvider
    def generate(self, prompt):
        # Claude API 호출
        ...

class OllamaProvider(LLMProvider):     # ← Java: class OllamaProvider implements LLMProvider
    def generate(self, prompt):
        # 로컬 Ollama API 호출
        ...

def get_provider(settings) -> LLMProvider:  # ← Java: @Bean / Factory
    if settings["llm"]["provider"] == "anthropic":
        return AnthropicProvider(settings)
    else:
        return OllamaProvider(settings)
```

settings.yaml에서 `llm.provider` 값만 바꾸면 Claude ↔ Ollama가 전환된다.

**2. Singleton 패턴 — ES 클라이언트, Whisper 모델**

```python
# Java에서는 static 필드 + getInstance()로 구현하지만,
# Python에서는 모듈 레벨 변수로 간단히 구현한다.

_client = None                    # ← Java: private static Elasticsearch INSTANCE;

def get_client(settings):         # ← Java: public static Elasticsearch getInstance()
    global _client
    if _client is not None:
        return _client
    _client = Elasticsearch(...)  # 최초 1회만 생성
    return _client
```

**3. Pipeline 패턴 — CLI의 run-all**

```python
# cli.py의 run_all 함수는 6개 단계를 순차 실행한다.
# Java의 Chain of Responsibility와 유사.

@cli.command("run-all")
def run_all(ctx):
    ctx.invoke(collect)       # Step 1: 수집
    ctx.invoke(transcribe)    # Step 2: 음성 변환
    ctx.invoke(compare)       # Step 3: 비교 분석
    ctx.invoke(analyze)       # Step 4: 어휘 분석
    ctx.invoke(llm_analyze)   # Step 5: LLM 분석
    ctx.invoke(load)          # Step 6: ES 적재
```

---

## CLI 명령어 실행 흐름 상세

### 명령어가 실행되는 과정

```bash
python -m src.cli collect
```

위 명령어를 실행하면 내부적으로 이런 흐름이 진행된다:

```
1. python -m src.cli
   → Python이 src/ 패키지의 cli.py를 모듈로 실행
   → cli.py 하단의 if __name__ == "__main__": cli() 가 호출됨

2. cli() — Click 그룹 (Java의 main 메서드)
   → --config 옵션을 파싱 (기본값: config/settings.yaml)
   → 로깅 설정 초기화
   → 서브커맨드(collect, transcribe, ...)로 분기

3. collect 서브커맨드
   → settings.yaml 로드
   → collector.collect_all(settings) 호출
   → 결과 요약 출력
```

### 각 명령어별 동작

| 명령어 | 내부 호출 | 입력 | 출력 |
|--------|-----------|------|------|
| `collect` | `collector.collect_all()` | 웹 크롤링 | `data/transcripts/*_official.json`, `data/audio/*.mp3` |
| `transcribe` | `transcriber.transcribe_all()` | `data/audio/*.mp3` | `data/transcripts/*_whisper.json` |
| `compare` | `comparator.compare_all()` | `*_official.json` + `*_whisper.json` | WER 비교 결과 (메모리) |
| `analyze` | `analyzer.analyze_all()` | `*_official.json` | 어휘 빈도 데이터 (메모리) |
| `llm-analyze` | `llm_analyzer.detect_expressions_for_episode()` | `*_official.json` | 숙어/표현 데이터 + `data/cache/llm/` 캐시 |
| `load` | `loader.load_all()` | 위 단계 결과 전부 | Elasticsearch 4개 인덱스 |
| `run-all` | 위 6개 순차 실행 | 웹 크롤링 | Elasticsearch 적재 |
| `init-indices` | `models.create_indices()` | settings.yaml | ES 인덱스 4개 생성 |
| `delete-indices` | `models.delete_indices()` | 확인 프롬프트 | ES 인덱스 4개 삭제 |

### 데이터 흐름 예시: 에피소드 1개의 여정

```
[ABC 웹사이트]
     │
     ▼  collect
[data/transcripts/106551254_official.json]  ← 공식 텍스트
[data/audio/106551254.mp3]                  ← 음성 파일
     │
     ▼  transcribe
[data/transcripts/106551254_whisper.json]   ← Whisper가 들은 텍스트
     │
     ├─▶ compare  → 문장별 WER + 듣기 난이도 (easy/hard/...)
     │
     ├─▶ analyze  → 단어 빈도 목록 (government: 5회, unprecedented: 2회, ...)
     │
     └─▶ llm-analyze → 숙어 (take the fall, kick the bucket, ...)
                        CEFR 레벨 (unprecedented → C1)
                        한국어 뜻 (unprecedented → 전례 없는)
     │
     ▼  load
[Elasticsearch]
  ├─ abc-episodes     : 에피소드 메타데이터
  ├─ abc-sentences    : 문장별 비교 데이터
  ├─ abc-vocabulary   : 어휘 사전
  └─ abc-expressions  : 숙어/관용어 사전
```

### `-m` 플래그란?

```bash
# 이 두 명령어는 기능적으로 같다:
python src/cli.py collect           # 파일을 직접 실행
python -m src.cli collect           # 모듈로 실행 (권장)

# -m은 Python에게 "src.cli를 모듈로 찾아서 실행해라"고 지시한다.
# Java로 치면:
# java com.example.Cli collect      (클래스패스에서 찾아 실행)
# 와 같은 개념이다.
#
# -m을 쓰면 패키지 내부의 상대 import (from .models import ...)가 정상 동작한다.
```
