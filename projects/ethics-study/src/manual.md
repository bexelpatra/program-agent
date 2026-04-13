# Ethics Study Guide CLI 사용 설명서

윤리 임용시험 학습 가이드 CLI 도구 (`ethics-guide`)의 사용법을 설명합니다.

---

## 목차

1. [시작하기](#시작하기)
2. [명령어 목록](#명령어-목록)
3. [명령어 상세](#명령어-상세)
   - [init — 인덱스 초기화](#init--인덱스-초기화)
   - [load — YAML 데이터 적재](#load--yaml-데이터-적재)
   - [load-all — 전체 데이터 적재](#load-all--전체-데이터-적재)
   - [study — 사상가 종합 조회](#study--사상가-종합-조회)
   - [search — 키워드/분야 검색](#search--키워드분야-검색)
   - [relations — 사상적 관계 조회](#relations--사상적-관계-조회)
   - [verify-status — 미검증 데이터 확인](#verify-status--미검증-데이터-확인)
   - [export — YAML 내보내기 (단일)](#export--yaml-내보내기-단일)
   - [export-all — YAML 내보내기 (전체)](#export-all--yaml-내보내기-전체)
4. [환경 변수](#환경-변수)
5. [YAML 데이터 형식](#yaml-데이터-형식)

---

## 시작하기

### 1. Elasticsearch 실행

모든 명령어를 사용하기 전에 Elasticsearch 컨테이너를 먼저 실행해야 합니다.

```bash
docker-compose up -d
```

정상 기동 확인 (약 10~20초 소요):

```bash
curl http://localhost:9200/_cluster/health
```

### 2. 의존성 설치

```bash
pip install -r requirements.txt
```

### 3. 인덱스 초기화 (최초 1회)

```bash
python -m src.cli init
```

### 4. 데이터 적재

```bash
# 분야 정의 먼저 적재
python -m src.cli load data/fields.yaml

# 사상가 데이터 적재
python -m src.cli load data/western/socrates.yaml
```

---

## 명령어 목록

| 명령어 | 설명 |
|--------|------|
| `init` | Elasticsearch 인덱스를 초기화한다 |
| `load <yaml_path>` | 단일 YAML 파일을 ES에 적재한다 |
| `load-all [--data-dir]` | 디렉토리의 모든 YAML을 ES에 적재한다 |
| `study <사상가명>` | 사상가 종합 정보를 출력한다 |
| `search <키워드>` | 키워드로 사상가·주장·개념을 검색한다 |
| `search --field <분야>` | 분야별 사상가 목록을 조회한다 |
| `relations <사상가명>` | 사상가의 영향 관계를 조회한다 |
| `verify-status` | 미검증 주장(claim) 목록을 출력한다 |
| `export <thinker_id>` | ES에서 특정 사상가를 YAML로 내보낸다 |
| `export-all [--data-dir]` | ES의 모든 사상가를 YAML로 내보낸다 |

---

## 명령어 상세

### init — 인덱스 초기화

Elasticsearch에 필요한 인덱스를 생성합니다. **최초 1회** 또는 데이터를 완전히 초기화할 때 실행합니다.

```bash
python -m src.cli init
```

**출력 예시:**

```
모든 인덱스가 초기화되었습니다.
```

생성되는 인덱스:
- `ethics-thinkers` — 사상가 기본 정보
- `ethics-works` — 저서 목록
- `ethics-claims` — 핵심 주장/견해
- `ethics-keywords` — 키워드 사전
- `ethics-relations` — 사상 간 관계
- `ethics-fields` — 분야 정의

---

### load — YAML 데이터 적재

단일 YAML 파일을 Elasticsearch에 적재합니다. `fields.yaml`과 사상가 파일 모두 이 명령어로 적재합니다.

```bash
python -m src.cli load <yaml_path>
```

**예시:**

```bash
# 분야 정의 적재
python -m src.cli load data/fields.yaml

# 사상가 데이터 적재
python -m src.cli load data/western/socrates.yaml
python -m src.cli load data/western/plato.yaml
python -m src.cli load data/western/aristotle.yaml
```

**출력 예시 (사상가):**

```
적재 완료:
  thinker: 1
  works: 3
  claims: 10
  keywords: 6
  relations: 2
```

**출력 예시 (fields.yaml):**

```
분야 4개 적재 완료
```

---

### load-all — 전체 데이터 적재

`data/` 디렉토리 아래의 모든 YAML 파일을 한 번에 적재합니다.

```bash
python -m src.cli load-all
```

다른 디렉토리를 지정하려면:

```bash
python -m src.cli load-all --data-dir /path/to/data
```

**출력 예시:**

```
전체 적재 완료:
  thinker: 5
  works: 18
  claims: 52
  keywords: 31
  relations: 8
```

---

### study — 사상가 종합 조회

사상가의 전체 정보를 보기 좋게 출력합니다. 이름의 일부만 입력해도 검색됩니다.

```bash
python -m src.cli study <사상가명>
```

**예시:**

```bash
python -m src.cli study 소크라테스
python -m src.cli study 플라톤
python -m src.cli study 아리스토텔레스
python -m src.cli study 칸트
```

**출력 예시:**

```
=== 소크라테스 (-470--399) ===
분야: western_ethics (고대 그리스)

[배경] 아테네의 석공 소프로니스코스의 아들...

[사상 형성 과정] 초기에는 자연철학에 관심을 가졌으나...

[핵심 사상] 소크라테스는 자연철학에서 벗어나 인간의 영혼과 덕의 문제에 집중...

주요 저서
  1. 소크라테스의 변명 (-399)
     의의: 소크라테스의 재판에서의 변론을 담은 저서...

핵심 주장
  [무지의 지, 산파술] 나는 내가 모른다는 것을 안다...
    출처: apology, 17a-35d
    논증: 델포이 신탁이 "소크라테스보다 지혜로운 자가 없다"고 하자...
    반론: 지식의 절대적 기준에 대한 회의주의적 비판이 가능하다...

사상적 관계
  -> plato (influenced): 소크라테스의 문답법과 윤리적 탐구...
  <- protagoras (criticized): ...

핵심 키워드
  - 무지의 지: 자신이 모른다는 것을 아는 것...
```

---

### search — 키워드/분야 검색

#### 키워드 검색

사상가, 주장, 키워드 사전을 전문(full-text) 검색합니다.

```bash
python -m src.cli search <키워드>
```

**예시:**

```bash
python -m src.cli search 덕
python -m src.cli search 영혼
python -m src.cli search 행복
python -m src.cli search "도덕 법칙"
python -m src.cli search 이데아
```

**출력 예시:**

```
관련 사상가:
  - 소크라테스 (고대 그리스)
  - 플라톤 (고대 그리스)
  - 아리스토텔레스 (고대 그리스)

관련 주장:
  [socrates] 덕(아레테)은 곧 지식이다. 악행은 무지에서 비롯...
  [plato] 덕은 영혼의 각 부분이 제 기능을 다할 때 생긴다...

관련 키워드:
  - 덕(아레테): 인간이 탁월하게 기능하는 상태...
```

#### 분야별 검색

특정 분야에 속한 사상가 목록을 조회합니다.

```bash
python -m src.cli search --field <분야ID>
```

**예시:**

```bash
python -m src.cli search --field western_ethics
python -m src.cli search --field eastern_ethics
python -m src.cli search --field political_philosophy
python -m src.cli search --field moral_development
```

**출력 예시:**

```
[western_ethics] 분야 사상가:
  - 소크라테스 (고대 그리스)
  - 플라톤 (고대 그리스)
  - 아리스토텔레스 (고대 그리스)
  - 아우구스티누스 (중세)
  - 토마스 아퀴나스 (중세)
```

---

### relations — 사상적 관계 조회

특정 사상가가 누구에게 영향을 받았고, 누구에게 영향을 주었는지 조회합니다.

```bash
python -m src.cli relations <사상가명>
```

**예시:**

```bash
python -m src.cli relations 플라톤
python -m src.cli relations 아리스토텔레스
python -m src.cli relations 토마스아퀴나스
```

**출력 예시:**

```
=== 플라톤의 사상적 관계 ===

영향 받은 관계 (incoming):
  <- socrates (influenced): 소크라테스의 문답법과 영혼 불멸론을 계승...

영향 준 관계 (outgoing):
  -> aristotle (influenced): 이데아론과 목적론적 세계관을 비판적으로 계승...
  -> neoplatonism (developed): 플로티노스가 플라톤의 이데아론을 발전시켜...
```

관계 유형 설명:
- `influenced` — 사상적 영향을 주었음
- `developed` — 사상을 발전·계승시켰음
- `criticized` — 비판하거나 반박했음
- `synthesized` — 여러 사상을 종합했음

---

### verify-status — 미검증 데이터 확인

`verified: false`로 표시된 주장(claim) 목록을 출력합니다. 데이터 품질 관리에 활용합니다.

```bash
python -m src.cli verify-status
```

**출력 예시 (미검증 데이터 있음):**

```
미검증 주장: 3건

  [socrates] socrates-claim-011
    소크라테스는 민주정을 비판하고 철인통치를 주장했다...

  [plato] plato-claim-005
    플라톤의 국가에서 수호자 계급은 사유재산을 가질 수 없다...
```

**출력 예시 (모두 검증됨):**

```
모든 주장이 검증되었습니다.
```

---

### export — YAML 내보내기 (단일)

ES에 저장된 특정 사상가의 데이터를 YAML 파일로 내보냅니다. 인자는 사상가의 `id`(영문 슬러그)를 사용합니다.

```bash
python -m src.cli export <thinker_id>
```

**예시:**

```bash
python -m src.cli export socrates
python -m src.cli export plato
python -m src.cli export aristotle
python -m src.cli export augustine
python -m src.cli export aquinas
```

출력 경로를 변경하려면:

```bash
python -m src.cli export socrates --data-dir backup/
```

**출력 예시:**

```
export 완료: data/western/socrates.yaml
```

---

### export-all — YAML 내보내기 (전체)

ES에 저장된 모든 사상가를 YAML로 내보냅니다.

```bash
python -m src.cli export-all
```

출력 디렉토리를 변경하려면:

```bash
python -m src.cli export-all --data-dir backup/
```

**출력 예시:**

```
export 완료: 5명
  aquinas: data/western/aquinas.yaml
  aristotle: data/western/aristotle.yaml
  augustine: data/western/augustine.yaml
  plato: data/western/plato.yaml
  socrates: data/western/socrates.yaml
```

---

## 환경 변수

ES 연결 정보를 환경변수로 오버라이드할 수 있습니다.

| 변수 | 기본값 | 설명 |
|------|--------|------|
| `ES_HOST` | `localhost` | Elasticsearch 호스트 |
| `ES_PORT` | `9200` | Elasticsearch 포트 |
| `ES_INDEX_PREFIX` | `ethics` | 인덱스 이름 접두사 |

**예시:**

```bash
ES_HOST=192.168.1.10 python -m src.cli study 소크라테스
ES_INDEX_PREFIX=dev python -m src.cli init
```

---

## YAML 데이터 형식

### 분야 파일 (`fields.yaml`)

```yaml
fields:
  - id: western_ethics
    name: 서양윤리
    description: 고대 그리스부터 현대까지의 서양 윤리 사상
    order: 1
  - id: eastern_ethics
    name: 동양윤리
    description: 유교·불교·도교 등 동양 윤리 사상
    order: 2
```

### 사상가 파일 (`data/western/socrates.yaml`)

```yaml
thinker:
  id: socrates
  name: 소크라테스
  name_en: Socrates
  field: western_ethics
  era: 고대 그리스
  birth_year: -470
  death_year: -399
  background: "아테네의 석공 소프로니스코스의 아들..."
  core_philosophy: "덕(아레테)은 곧 지식이라는 주지주의적 입장..."
  philosophical_journey: "초기에는 자연철학에 관심을 가졌으나..."
  keywords:
    - 무지의 지
    - 산파술

works:
  - id: socrates-apology
    title: 소크라테스의 변명
    title_original: Apologia Sōkratous
    year: -399
    significance: "소크라테스 사상의 핵심이 담긴 변론..."
    key_concepts:
      - 무지의 지
      - 사명감

claims:
  - id: socrates-claim-001
    work_id: socrates-apology
    source_detail: "17a-35d"
    claim: "나는 내가 모른다는 것을 안다."
    original_text: "ἓν δὲ τοῦτο οἶδα, ὅτι οὐκ οἶδα."
    explanation: "무지의 자각이 진정한 지혜의 시작..."
    argument: "델포이 신탁 이후 지혜롭다는 사람들을 찾아다니며 문답한 결과..."
    counterpoint: "지식의 절대적 기준에 대한 회의주의적 비판이 가능하다..."
    context: "소크라테스가 법정에서 자신의 철학적 삶을 변론하는 장면"
    keywords:
      - 무지의 지
      - 산파술
    verified: true
    verification_log:
      - date: "2026-03-25"
        method: "원전 대조 + 웹 검색"
        result: "정확함"

keywords:
  - id: socrates-kw-001
    term: 무지의 지
    term_en: knowing that one does not know
    definition: "자신이 모른다는 것을 아는 것이 진정한 지혜의 출발점..."
    thinker_id: socrates
    work_id: socrates-apology
    related_terms:
      - 산파술
      - 문답법

relations:
  - from_thinker: socrates
    to_thinker: plato
    type: influenced
    description: "소크라테스의 문답법과 윤리적 탐구 방식이 플라톤에게 계승됨"
    evidence: "플라톤의 초기 대화편 전반"
```

---

## 자주 쓰는 명령어 조합

```bash
# 처음 설정 (ES 기동 → 인덱스 초기화 → 데이터 적재)
docker-compose up -d
python -m src.cli init
python -m src.cli load data/fields.yaml
python -m src.cli load-all

# 특정 사상가 공부
python -m src.cli study 칸트
python -m src.cli relations 칸트

# 개념 비교 검색
python -m src.cli search 의무
python -m src.cli search 공리

# 데이터 품질 확인
python -m src.cli verify-status

# 수정 후 YAML 백업
python -m src.cli export socrates
python -m src.cli export-all
```
