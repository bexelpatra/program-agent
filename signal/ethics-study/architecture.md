# Architecture

## 개요

**프로젝트명**: 윤리 임용시험 학습 가이드 (Ethics Study Guide)

윤리 임용시험 범위의 사상가 정보를 저서에 근거하여 정확하게 구조화하고 Elasticsearch에 저장하여, 사상가·키워드 중심으로 검색·학습할 수 있는 CLI 도구.

### 핵심 원칙
- **정확성 최우선**: 모든 주장·견해는 사상가의 저서에 근거해야 함
- **교차 검증**: 데이터 입력 후 반드시 검증 과정을 거침
- **점진적 확장**: 소량씩 입력하고 검증한 뒤 확장

### 기술 스택
- **언어**: Python 3.11+
- **데이터베이스**: Elasticsearch 8.x (Docker)
- **ES 클라이언트**: elasticsearch-py (공식 Python 드라이버)
- **CLI**: click
- **데이터 백업**: YAML (검증 완료 후 ES → YAML export)

## 구조

```
docker-compose.yml          # ES 컨테이너
requirements.txt

src/
├── config.py               # ES 연결 설정
├── es_client.py            # ES 인덱스 관리 및 CRUD
├── models.py               # 데이터 모델 정의
├── loader.py               # YAML → ES 데이터 로딩 (기존 백업용 유지)
├── exporter.py             # ES → YAML export (검증 완료 데이터 백업)
├── search.py               # 검색 기능
└── cli.py                  # CLI 엔트리포인트

data/                        # 검증 완료 데이터 백업 (YAML export)
├── fields.yaml             # 분야 정의
├── western/                # 서양윤리
├── eastern/                # 동양윤리
├── political/              # 정치철학
└── moral_development/      # 도덕발달론

tests/
├── test_es_client.py
├── test_loader.py
└── test_search.py
```

## ES 인덱스 설계

### 1. ethics-thinkers (사상가)
```json
{
  "id": "string",
  "name": "string",
  "name_en": "string",
  "field": "string",
  "era": "string",
  "birth_year": "integer",
  "death_year": "integer",
  "background": "text — 사상 이해에 도움이 되는 배경 정보",
  "core_philosophy": "text — 핵심 사상 요약",
  "philosophical_journey": "text — 사상 형성 과정",
  "keywords": ["string"]
}
```

### 2. ethics-works (저서)
```json
{
  "id": "string — thinker_id-work_slug",
  "thinker_id": "string",
  "title": "string",
  "title_original": "string — 원어 제목",
  "year": "integer",
  "significance": "text — 저서의 의의",
  "key_concepts": ["string"]
}
```

### 3. ethics-claims (주장/견해 — 핵심 인덱스)
```json
{
  "id": "string",
  "thinker_id": "string",
  "work_id": "string",
  "source_detail": "string — 구체적 출처 (장/절)",
  "claim": "text — 주장 내용",
  "original_text": "text — 원문 (가능한 경우)",
  "explanation": "text — 해설",
  "argument": "text — 논증/근거 (왜 이 주장을 하는가, 논리적 구조)",
  "counterpoint": "text — 반론·한계·후대 비판 (선택적)",
  "context": "text — 주장이 나오게 된 맥락",
  "keywords": ["string"],
  "verified": "boolean",
  "verification_log": [{"date": "string", "method": "string", "result": "string"}]
}
```

### 4. ethics-keywords (키워드 사전)
```json
{
  "id": "string",
  "term": "string",
  "term_en": "string",
  "definition": "text",
  "thinker_id": "string",
  "work_id": "string",
  "related_terms": ["string"]
}
```

### 5. ethics-relations (사상 간 관계)
```json
{
  "from_thinker": "string",
  "to_thinker": "string",
  "type": "string — influenced_by | developed | criticized | synthesized",
  "description": "text",
  "evidence": "string — 근거 출처"
}
```

### 6. ethics-fields (분야 — 동적 추가 가능)
```json
{
  "id": "string",
  "name": "string",
  "description": "text",
  "order": "integer"
}
```

## 데이터 투입 순서

### Phase 1: 서양윤리 (시대순)
| 순서 | 사상가 | 출제비중 | 데이터 규모 | 상태 |
|------|--------|----------|------------|------|
| 1 | 소크라테스 | 핵심 | 표준 (claims 10) | ✓ 완료 |
| 2 | 플라톤 | 핵심 | 표준 (claims 12) | ✓ 완료 |
| 3 | 아리스토텔레스 | 핵심 | 표준 (claims 12) | ✓ 완료 |
| 4 | 아우구스티누스 | 보통 | 축소 (claims 8) | ✓ 완료 |
| 5 | 토마스 아퀴나스 | 중요 | 표준 (claims 10) | ✓ 완료 |
| 6 | 칸트 | 핵심 | 확장 (claims 15+) | |
| 7 | 벤담 | 핵심 | 표준 (claims 10~12) | |
| 8 | 밀 | 핵심 | 확장 (claims 15+) | |
| 9 | 흄 | 중요 | 표준 (claims 8~10) | |
| 10+ | 스토아, 에피쿠로스, 스피노자, 헤겔, 사르트르 등 | 보통 | 축소 | |

### 출제비중별 데이터 규모 기준
- **핵심** (거의 매년 출제): claims 12~15+, argument/counterpoint 상세, works 확장
- **중요** (자주 출제): claims 8~10, 표준 수준
- **보통** (간헐적 출제): claims 6~8, 핵심 주장 위주

### Phase 2: 동양윤리
| 순서 | 사상가 | 구분 | 출제비중 | 데이터 규모 | 상태 |
|------|--------|------|----------|------------|------|
| 1 | 공자 | 유교-선진 | 핵심 | 확장 (claims 15+) | |
| 2 | 맹자 | 유교-선진 | 핵심 | 확장 (claims 15+) | |
| 3 | 순자 | 유교-선진 | 핵심 | 표준 (claims 10~12) | |
| 4 | 노자 | 도가 | 핵심 | 표준 (claims 10~12) | |
| 5 | 장자 | 도가 | 중요 | 표준 (claims 8~10) | |
| 6 | 주희(주자) | 성리학 | 핵심 | 확장 (claims 15+) | |
| 7 | 왕양명(왕수인) | 양명학 | 중요 | 표준 (claims 8~10) | |
| 8 | 이황(퇴계) | 한국유학 | 핵심 | 확장 (claims 12+) | |
| 9 | 이이(율곡) | 한국유학 | 핵심 | 확장 (claims 12+) | |
| 10 | 정약용(다산) | 한국유학 | 중요 | 표준 (claims 8~10) | |
| 11 | 붓다(석가모니) | 불교 | 중요 | 표준 (claims 8~10) | |
| 12 | 원효/혜능 | 불교 | 보통 | 축소 (claims 6~8) | |
| 13 | 묵자 | 제자백가 | 보통 | 축소 (claims 6~8) | |
| 14 | 한비자 | 제자백가 | 보통 | 축소 (claims 6~8) | |

### Phase 3: 정치철학/사회사상
| 순서 | 사상가 | 구분 | 출제비중 | 데이터 규모 | 상태 |
|------|--------|------|----------|------------|------|
| 1 | 홉스 | 사회계약론 | 핵심 | 확장 (claims 12+) | |
| 2 | 로크 | 사회계약론 | 핵심 | 확장 (claims 12+) | |
| 3 | 루소 | 사회계약론 | 핵심 | 확장 (claims 12+) | |
| 4 | 롤스 | 정의론 | 핵심 | 확장 (claims 15+) | |
| 5 | 노직 | 자유지상주의 | 중요 | 표준 (claims 8~10) | |
| 6 | 매킨타이어 | 공동체주의 | 중요 | 표준 (claims 8~10) | |
| 7 | 샌델 | 공동체주의 | 중요 | 표준 (claims 8~10) | |
| 8 | 하버마스 | 담론윤리 | 중요 | 표준 (claims 8~10) | |
| 9 | 왈처 | 공동체주의 | 보통 | 축소 (claims 6~8) | |
| 10 | 테일러 | 공동체주의 | 보통 | 축소 (claims 6~8) | |

### Phase 4: 도덕교육론/도덕심리학
| 순서 | 이론가 | 구분 | 출제비중 | 데이터 규모 | 상태 |
|------|--------|------|----------|------------|------|
| 1 | 피아제 | 도덕발달 | 핵심 | 표준 (claims 8~10) | |
| 2 | 콜버그 | 도덕발달 | 핵심 | 확장 (claims 12+) | |
| 3 | 길리건 | 배려윤리 | 중요 | 표준 (claims 8~10) | |
| 4 | 나딩스 | 배려윤리 | 중요 | 표준 (claims 8~10) | |
| 5 | 래스 | 가치명료화 | 중요 | 축소 (claims 6~8) | |
| 6 | 리코나 | 인격교육 | 중요 | 축소 (claims 6~8) | |
| 7 | 하이트 | 도덕심리학 | 중요 | 축소 (claims 6~8) | |
| 8 | 레스트 | 도덕심리학 | 중요 | 축소 (claims 6~8) | |

### Phase 5: 통일교육/시민윤리 (C안: 인물 중심)
| 순서 | 이론가 | field id | 구분 | 출제비중 | 데이터 규모 | 상태 |
|------|--------|----------|------|----------|------------|------|
| 1 | 갈퉁 | peace_studies | 평화학 | 중요 | 축소 (claims 6~8) | |
| 2 | 백낙청 | unification_edu | 통일교육(분단체제론) | 중요 | 축소 (claims 6~8) | |
| 3 | 강만길 | unification_edu | 통일교육(통일지향 역사학) | 보통 | 축소 (claims 6~8) | |
| 4 | 듀이 | civic_edu | 민주시민교육 | 중요 | 표준 (claims 8~10) | |
| 5 | 아렌트 | civic_edu | 민주시민교육(공적 영역) | 중요 | 표준 (claims 8~10) | |

**C안 결정 근거**: `ethics-claims.thinker_id` 외래키를 유지하기 위해 주제를 인물 중심으로 재편. 기존 ES-first 파이프라인·스키마 무변경.
**하버마스 중복 회피**: Phase 3에서 담론윤리로 이미 입력됨. 시민교육 관점은 필요 시 claim 추가로 보강.

**원칙**: 소량씩 입력 → 검증 → 확장 반복, 시대순 투입, 출제비중에 따라 데이터 규모 차등
**병렬 실행**: Phase 1 잔여 + Phase 2 + Phase 3는 서로 다른 사상가(다른 ES 문서)이므로 병렬 입력 가능

## CLI 커맨드

```
ethics-guide load <yaml_path>       # YAML → ES 로딩
ethics-guide load-all               # data/ 전체 로딩
ethics-guide study <사상가>          # 사상가 종합 조회
ethics-guide search <키워드>         # 전문 검색
ethics-guide search --field <분야>   # 분야별 조회
ethics-guide relations <사상가>      # 영향 관계 조회
ethics-guide verify-status           # 미검증 데이터 목록
```

## 데이터 파이프라인

### 입력 → 검증 → 백업 (ES-first)

```
Coder (sonnet)          Tester (opus)           Manager
    │                       │                      │
    ├─ ES API로 직접 입력 ──→│                      │
    │  (thinker, works,     ├─ ES 쿼리로 항목별    │
    │   claims, keywords,   │  검증 (전체 읽기 X)  │
    │   relations)          ├─ 웹 검색 교차 확인   │
    │                       ├─ report 작성 ────────→│
    │                       │                      ├─ 이슈 판단
    │←── 수정 지시 (항목별) ──┤                      │
    │                       │                      │
    ├─ ES에서 해당 문서만   │                      │
    │  update               │                      │
    │                       │                      │
    │  [모든 검증 완료 후]   │                      │
    ├─ ES → YAML export ───→│                      │
    │  (Git 백업용)          │                      │
```

### 핵심 변경 (v2)
- **Before**: YAML 작성 → ES 로딩 → YAML 전체 읽고 검증 → YAML 수정 → 재로딩
- **After**: ES 직접 입력 → ES 쿼리로 항목별 검증 → ES update → 최종 YAML export
- **효과**: 컨텍스트 소모 대폭 감소, 검증/수정 시 해당 항목만 조회

### 에이전트 모델 배정
| Agent | 모델 | 이유 |
|-------|------|------|
| Coder | sonnet | 정형화된 스키마 입력, ES API 호출 — 실행력 중심 |
| Tester | opus | 학술적 사실 검증, 원전 정합성 판단 — 추론력 중심 |

### 토큰 사용량 추적
- Manager가 서브에이전트 호출 결과의 usage(total_tokens, tool_uses, duration_ms)를 done-log에 기록
- 사상가 1명 완료 시 총 토큰 합산 기록

### 검증 방식
1. Coder가 ES에 직접 데이터 입력 (verified: false)
2. Tester가 ES 쿼리로 검증:
   - 주장 ↔ 저서 정합성 (항목별 조회)
   - 키워드 정의 정확성
   - 관계 방향/논리 검증 ("from [type] to" = "from이 to에게 [type]한 것")
   - 웹 검색 교차 확인
3. 이슈 발견 → Coder가 ES update로 수정
4. 검증 완료 → verified: true + verification_log 업데이트
5. 모든 데이터 검증 완료 후 → ES → YAML export (Git 백업)

## 설계 결정

### 1. ES-first 파이프라인 (v2)
- **결정**: 에이전트가 ES에 직접 입력/수정, 검증 완료 후 YAML export로 백업
- **이유**: (v1) YAML 우선 방식은 검증/수정 시 전체 파일을 읽어야 해서 토큰 비효율. ES 쿼리로 항목별 조회하면 컨텍스트 소모 대폭 감소. YAML은 Git 백업 용도로만 유지.

### 2. Elasticsearch Docker
- **결정**: docker-compose로 ES 실행
- **이유**: 로컬 환경 독립적, 재현 가능, 쉬운 초기화

### 3. 검증 필수 플래그
- **결정**: 모든 claim에 verified 필드와 verification_log
- **이유**: 정확성이 최우선 요구사항. 미검증 데이터를 추적하고 검증 이력을 남김.

### 4. 분야 동적 추가
- **결정**: ethics-fields 인덱스로 분야를 관리, 하드코딩하지 않음
- **이유**: 사용자가 공부하면서 새 분야를 추가할 수 있어야 함

## relations 방향 규칙
- `from_thinker [type] to_thinker` = "from이 to에게 [type]한 것"
- 예: from: socrates, to: plato, type: influenced = "소크라테스가 플라톤에게 영향을 주었다"
- 예: from: socrates, to: protagoras, type: criticized = "소크라테스가 프로타고라스를 비판했다"

## Web UI (검색/조회 인터페이스)

### 기술 스택
- **백엔드**: FastAPI + Jinja2 템플릿 + uvicorn
- **프론트엔드**: vanilla HTML/CSS/JS (프레임워크 없음)
- **ES 연동**: elasticsearch-py (기존 설치됨)

### 디렉토리 구조
```
projects/ethics-study/
└── web/
    ├── app.py              # FastAPI 앱 (라우트 + ES 쿼리)
    ├── templates/
    │   ├── base.html       # 공통 레이아웃 (nav, footer)
    │   ├── index.html      # 메인: 사상가 목록 (분야별 탭)
    │   ├── thinker.html    # 사상가 상세 (works, claims, keywords, relations)
    │   └── search.html     # 통합 검색 결과
    └── static/
        ├── style.css       # 스타일
        └── app.js          # 클라이언트 JS (탭 전환, 검색 등)
```

### 페이지 구성
1. **메인 (index)**: 사상가 42명 카드형 목록, 분야별 탭 (서양윤리/동양윤리/정치철학), 시대순 정렬
2. **사상가 상세 (thinker)**: 기본 정보, 저작 목록, 주장(claim+argument+counterpoint), 키워드, 관계도
3. **검색 (search)**: claims + keywords + works 통합 전문 검색, ES nori 분석기 활용

### API 엔드포인트
```
GET /                           # 메인 페이지 (사상가 목록)
GET /thinker/{thinker_id}       # 사상가 상세
GET /search?q={query}           # 통합 검색
GET /api/thinkers               # JSON: 전체 사상가
GET /api/thinker/{id}           # JSON: 사상가 상세 + 관련 데이터
GET /api/search?q={query}       # JSON: 검색 결과
```

### 실행
```bash
cd projects/ethics-study/web
uvicorn app:app --host 0.0.0.0 --port 8000
```

## Phase 6: 기출문제 해설 및 ES 보강

### 목적
- 2014~2026년 중등 임용시험 도덕·윤리 전공A/B 기출문제 전수에 대해 **정확한 해설**을 마크다운으로 작성한다.
- 기출문제를 풀이하는 과정에서 ES에 누락되거나 부족한 사상가·주장·저서를 **점진 보강**한다.
- 교과교육학(2022 개정 도덕과 교육과정 등)은 이번 범위에서 제외한다. (별도 프로젝트)
- 교육학 임용(비도덕과)은 **별도 프로젝트**로 분리.

### 입력 소스 (기출 md 원본)
- 경로: `~/잡동사니/임용/md/` (외부)
- 파일 조건: 파일명에 "도덕" 또는 "윤리"가 포함된 파일 (정확히 26개, 2014~2026 × 전공A/B)
- 파일명 패턴은 연도별로 상이:
  - 2014: `2014중등1차-2교시-도덕윤리-전공A-문제지-최종.md` / `-3교시-...-전공B-...`
  - 2015~2016: `YYYY중등1차-도덕윤리_전공A.md` / `-전공A.md` (구분자 혼재)
  - 2017: `2017_중등1차_도덕,윤리_전공A.md` (쉼표 포함)
  - 2018~2023: `YYYY_중등1차_도덕윤리_전공A.md`
  - 2019: `2019_중등1차_도덕윤리A.md` (`_전공` 생략)
  - 2024~2026: `YYYY_중등1차_도덕·윤리_전공A.md` (중점 포함)
- 스캔 시 파일명 정규화: 연도 YYYY, 과목 A|B 추출

### 핵심 원칙
- **할루시네이션 절대 금지**: 모든 해설의 근거는 사상가의 저서(장/절)에 명시되어야 한다.
- **ES claim 우선**: 해설이 인용하는 근거는 가능하면 ES `ethics-claims`에 존재하는 항목을 참조한다. 존재하지 않으면 claim을 ES에 추가한 뒤 인용한다.
- **Tester 엄격 검증**: 해설의 사상가명·저서명·개념·인용 모든 요소를 건건이 검증. 원전 불일치 시 즉시 FAILED 처리.
- **점진 보강 + 선보강 하이브리드**: 스캔 단계에서 명확히 누락된 사상가(예: 튜리엘·폴 테일러·레오폴드)는 선보강, 세부 claim 부족은 해설 작성 중 점진 보강.
- **ES 스키마 불변**: 기존 구조(thinkers/works/claims/keywords/relations/fields) 유지. 새 인덱스 추가 없음.

### 산출물 디렉토리 구조

```
projects/ethics-study/exam-solutions/
├── 2014-A.md              # 2014학년도 전공A 해설 (문항별 섹션)
├── 2014-B.md
├── 2015-A.md, 2015-B.md
├── ...
├── 2026-A.md, 2026-B.md   # 총 26파일
├── exam-coverage-map.md   # 전수 스캔 결과 (사상가/개념/ES 커버리지)
└── topical/               # 경계 영역 (사상가 없이 쟁점 중심인 문항)
    ├── applied-ethics-bioethics.md
    ├── applied-ethics-environment.md
    └── ...                # 스캔 결과에 따라 추가
```

### 해설 파일 템플릿 (1문항당)

```markdown
## 문항 N [배점]

### 문제 요지
(문제의 핵심 지문·조건을 1~3문장으로 요약. 원문 인용은 인용블록.)

### 정답
- ㉠: ...
- ㉡: ...
- 서술형 답안: ...

### 해설
- **사상가**: ...
- **저서**: 『저서명』 (원어명, 출판연도)
- **출처**: 장·절·구체 위치
- **논리 전개**:
  (사상가 저서 근거를 인용하며 정답이 도출되는 논리를 서술)

### 관련 사상 확장 (차기 시험 대비)
- 이 사상가의 다른 핵심 주장 요약
- 영향 관계 / 비판 / 후속 발전 (중간 깊이)
- 같은 주제에 대한 대표적 반대 입장 1~2개

### 출제 포인트
- 이 문항에서 요구하는 핵심 개념
- 유사 변형 출제 가능성

### ES 참조
- thinker_id: `...`
- related_claim_ids: [`...`, `...`]
- related_work_ids: [`...`]

### 검증 상태
- verified: true/false
- verified_by: tester
- verified_at: YYYY-MM-DD
- verification_notes: (Tester가 확인한 사항)
```

### 경계 영역 처리 (topical/)

다음 유형은 사상가 중심이 아닌 쟁점 중심이므로 `topical/` 하위 파일에 별도 정리:
- 응용윤리 쟁점: 생명의료윤리(낙태·안락사·유전자 조작), 환경윤리(기후·동물권 일반 쟁점), 정보윤리(AI·프라이버시), 직업윤리
- 통일교육 제도/정책: 민족공동체 통일방안 3단계 등 (인물 사상이 아닌 공식 정책)
- 평화/시민 제도 개념: 구체 사상가와 분리되는 일반 개념

**목적**: "시험 대비 수준"으로만 학습 요점 정리. ES 보강은 원칙적으로 하지 않으며, 사상가에 귀속되는 내용이 있으면 해당 사상가 claim으로 편입.

### 교과교육학 문항 제외 규칙

도덕·윤리 전공 A/B 파일 내에도 교과교육학 문항이 섞여 있다 (예: 2022 개정 도덕과 교육과정, 도덕과 평가 방법 등). 스캔 시 아래 규칙으로 분류:
- **사상가형**: 특정 사상가의 주장·저서를 묻거나 사상 개념을 묻는 문항 → 해설 대상
- **경계영역형**: 사상가가 특정되지 않은 응용윤리·통일교육 쟁점 → `topical/` 해설 대상
- **교과교육학형**: "…개정 도덕과 교육과정", "도덕과 수업 모형", "평가 방법 유형" 등 → **이번 범위 제외, 해설 작성 안 함**
  - exam-coverage-map.md에는 식별만 기록 (연도/문항번호/주제)
  - 각 년도 해설 md에는 "## 문항 N [제외 — 교과교육학]" 줄만 남기고 본문 비움
  - 혼합형(사상가 지식 + 교육과정 조항 동시 요구)은 사상가 부분만 해설

### 실행 순서

1. **TASK-173 (Manager)**: architecture.md Phase 6 섹션 추가 (본 작업)
2. **TASK-174 (coder)**: 26개 기출 md 전수 스캔 → `exam-coverage-map.md` 산출
   - 각 문항별 추출 항목: 연도/과목/문항번호/배점/주요 사상가/핵심 개념/주요 저서/ES 커버리지(있음·부족·없음)/경계 영역 여부
   - 누락 사상가 목록(고유), 부족 claim 힌트 목록, 경계 영역 문항 목록 최종 섹션으로 정리
3. **TASK-175 (Manager+Tester)**: 커버리지 맵 검증 → 누락 사상가 보강 태스크 일괄 등록
4. **누락 사상가 보강 태스크**: 사상가별 3-tuple (입력/검증/수정) — Phase 1~5와 동일 패턴
5. **경계 영역 해설 태스크**: topical/*.md 파일 작성 (Coder) + 검증 (Tester)
6. **연도별 해설 작성** (2014 → 2026 순차, A/B는 병렬):
   - 각 연도당 Coder 작성 태스크 2건(A, B) 병렬 호출 → Tester 검증 태스크 2건 → 수정 루프 → DONE
   - Tester 검증 실패 시 즉시 FAILED로 되돌려 Coder 재작성

### Tester 검증 체크리스트 (해설)

Tester는 각 문항 해설에 대해 아래 항목을 전건 확인:
1. **사상가명 정확성**: 표기·한자·원어 모두 확인
2. **저서명 정확성**: 번역 제목·원어 제목·출판 연도
3. **출처 구체성**: 장·절·구체 위치 기재 여부 (모호 시 FAILED)
4. **인용 정합성**: 인용된 구절이 실제 저서에 존재하는지 (웹·기존 claim 교차 확인)
5. **정답 타당성**: 해설이 실제로 정답을 뒷받침하는지
6. **ES 참조 유효성**: thinker_id·claim_id가 실제 ES에 존재하는지
7. **확장 내용의 사실성**: 영향관계·비판 주장도 근거 필수

한 항목이라도 문제 있으면 `severity: bug` 이상으로 리포트 → Manager는 반드시 수정 태스크 등록.

## 프로젝트 운영 규칙 (ethics-study 전용)

### Coder 서브에이전트 모델 규칙

**ethics-study 프로젝트의 모든 Phase에서 Coder 서브에이전트는 반드시 `claude-opus-4-7` (Opus)로 호출한다.**

- Manager는 `Agent` 툴 호출 시 `model: "opus"` 인자를 명시한다.
- 이유: Phase 6 TASK-174에서 비-Opus Coder가 광범위한 문항-사상가 오매핑·원문 인용 할루시네이션을 일으켜 Tester 블로커 판정을 받음 (2026-04-18). 본 프로젝트의 학술 정확도 요구 수준이 높아 상위 모델 필수.
- Tester·Reviewer는 기본 모델 유지.

### thinker_id 정규화 규칙

사상가 id 표기 통일 기준:

**한자문화권 (한국·중국·일본) 이름**
- 언더바 유무는 의미 없음. 비교 시 `"_"` 제거 후 소문자 기준으로 동일인 판정.
- 예: `yi_hwang == yihwang`, `zhu_xi == zhuxi`, `wang_yangming == wangyangming`, `jeong_yakyong == jeongyagyong`
- ES에 이미 저장된 표기를 canonical로 간주하며, 신규 문서는 canonical을 사용한다.

**서양 이름**
- 언더바 뒤 suffix가 동명이인 구분자·이니셜·성/이름 순서 표시일 수 있어 **반드시 개별 검토**.
- 동명이인 후보가 있으면 ES에서 사전 조회하여 suffix 필요 여부를 결정. 예: `taylor` (Charles Taylor, 공동체주의) vs `taylor_p` (Paul Taylor, 생명중심주의) — 별개 인물.
- 예: `mill_js` (John Stuart Mill) — 이니셜 suffix, 단일인이므로 표기 유지.

**Canonical 조회 명령**

```bash
curl -s "http://localhost:9200/ethics-thinkers/_search?size=100&_source=id,name,name_en" \
  | jq '.hits.hits[]._source'
```

문서 작성·검증 시 위 결과를 근거로 id를 기록한다.

### 블로커 누적 처리 정책

서브에이전트(특히 Tester)가 `severity: blocker`를 판정했을 때의 처리 단계:

1. **1차 재시도**: Coder(Opus)로 재작업 지시.
2. **2차 재시도 이후에도 블로커가 해소되지 않으면 작업 중단하지 않음**. 대신:
   - `signal/ethics-study/blocker-log.md`에 블로커 내역 누적 기록.
   - 문제가 된 산출물(md·데이터)의 해당 위치에 `<!-- BLOCKER(TASK-XXX): {사유} -->` 주석을 삽입하여 후속 작업자·사용자가 식별 가능하게 표시.
   - 해당 태스크는 `BLOCKED(user-review-pending)` 상태로 표기하고, 의존 관계가 없는 다음 태스크로 진행.
3. **사용자 일괄 검토**: 사용자가 적절한 시점에 `blocker-log.md`를 열어 한 번에 확인·판정하고, 필요한 수정안을 Manager에게 지시한다.
4. **의존성 있는 후속 작업**: 해당 블로커 산출물에 직접 의존하는 태스크만 자동 보류. 독립 태스크는 계속 진행.

### 커버리지 맵 작업 재시도 규칙 (TASK-174 후속)

- TASK-175A: Coder(Opus)가 `exam-coverage-map.md`를 **원문 인용 근거 직접 제시** 조건으로 전면 재작성한다. 각 문항 row의 "메모" 컬럼에 원문 2~3구절을 복사 삽입.
- 원문 번호 체계를 그대로 보존한다: 2014-A "기입형 1~15 + 서답형 1~5", 2015-A "기입형 1~10 + 서술형 1~4" 등 연도별 분리 번호 유지.
- 총 문항 수는 **293** 확정 (Tester 검증 기준). 서술·요약·산식 모든 위치에서 동일 수치 사용.
- 사상가 id는 canonical만 사용. 불명확한 경우 "사상가 불명(확인 필요)"로 남김.
- 재시도 후 Tester가 다시 블로커 판정 시 위 "블로커 누적 처리 정책"에 따라 `blocker-log.md` 기록 + 주석 처리 후 후속 작업 진행.

### Phase 6 기출 작업 규칙 (Coder/Tester 공통, 2026-04-20 확정)

Phase 6 기출문제 커버리지 맵·해설 작성에서 대량 할루시네이션·오매핑이 반복 발생함에 따라(BLK-001, BLK-175B-001~008 누적), 본 프로젝트의 모든 기출 관련 태스크(TASK-174 이후 전부)는 아래 규칙을 **강제**한다. 규칙 위반 시 Tester는 즉시 blocker 판정한다.

#### 대전제: 추론 금지

- "이 시기면 이 사상가가 나왔겠지", "이 정도 난이도면 X일 것이다", "전년도와 유사 패턴이면 Y이다", "기출에 자주 나오는 A일 거다" 같은 **패턴 추론·빈도 추론·상식 추론·시대적 예상으로 사상가를 확정하는 행위는 절대 금지**한다.
- 사상가 확정의 유일한 근거는 **해당 문항의 문제 발문 + 제시문의 직접 독해**다. LLM 내재 지식만으로 row를 채우지 않는다.

#### Coder 규칙

1. **원문 직독 필수 (현 세션 한정)**
   - 각 문항 row를 작성하기 전, 해당 연도 md 파일의 문항 영역을 **현 세션 내에서 Read tool로 직접 호출**해야 한다.
   - "이전 세션에 읽었다", "익숙한 파일이다" 같은 claim은 **인정되지 않는다**. 현 세션 Read 증거가 없는 row는 작성 금지.
   - 각 row 메모 컬럼에 원문 `file_path:line_range`를 병기한다. 예: `원문: 2014_전공A.md L45-L68`

2. **문제 → 제시문 → 사상가 3단계 확정 절차**
   모든 문항은 반드시 아래 순서로 작성한다.
   - **① 문제(발문) 독해**: "무엇을 묻는가"를 먼저 파악한다. (예: "㉠에 해당하는 사상가의 이름을 쓰시오", "A와 B 수업모형의 차이를 서술하시오", "㉮~㉰ 중 옳지 않은 것을 고르시오")
   - **② 제시문 독해**: 인용된 텍스트에서 **고유 개념어·인명·저서명·trademark 구절**을 추출한다. 한자어·원어 표기도 누락 없이 수집.
   - **③ 사상가·분류 판정**: ②에서 추출한 근거가 어느 사상가·어느 분류(사상가형/교과교육학/경계영역)에 해당하는지 확정. canonical thinker_id로 표기.
   - ③의 근거가 된 제시문 구절 **2~3개를 그대로 복사**해 메모 컬럼에 삽입한다. 요약·의역·재서술 금지.

3. **불확실 처리 (창작 금지)**
   - 제시문에 명확한 trademark가 없거나 사상가 특정이 어려우면 **창작하지 말고** "사상가 불명(확인 필요)" + HTML 주석 `<!-- BLOCKER(TASK-XXX): {미확정 사유 + 후보군} -->`로 표기하고 `blocker-log.md`에 등록한다.
   - 도표·그림·대조 구조가 포함된 문항은 **도표 전체를 텍스트로 재현**하여 메모에 삽입한다. 일부만 옮기면서 "핵심만 전달"하는 행위 금지.
   - **한 사상가의 복수 주제 동시 출제 가능**: 기출에서는 하나의 문항이 (가)/(나)/㉠/㉡ 등 복수 제시문으로 구성되어, 같은 사상가의 **서로 다른 주제**를 동시에 다루는 경우가 빈번하다. 이 경우 메모 컬럼에 제시문 묶음별로 **복수 주제를 모두 열거**한다. 대표 주제 하나만 적고 나머지를 생략하는 행위 금지. 단, **사전 힌트로 특정 개념어를 강제하지 않는다** — 각 빈칸·제시문의 정답은 Coder가 원문 직독 후 독립 확정하고, 불확실하면 위 3항의 "불확실 처리" 규칙에 따라 blocker 처리한다.

4. **한자+한글 병기 원칙 (사용자 가독성)**
   - 본 프로젝트 산출물(coverage/*.md, ES claims, 해설, 사상가 개념 설명 등)은 **학습 가이드**로서 사용되며, 사용자가 한자에 약하다. 따라서 한자 개념어·인명·저서명·trademark 구절을 노출할 때는 반드시 `한자(한글독음 — 간단 의미)` 형식으로 **병기**한다.
   - 예: `禮義(예의 — 예와 의)`, `化性起僞(화성기위 — 본성을 교화하여 인위를 일으킴)`, `天人分異(천인분이 — 하늘과 사람의 직분을 구분함)`.
   - 기술의 주언어는 **한글 해석 용어**여야 한다. 한자는 보조적 병기로만 등장.
   - 예외: 원문 인용구절 자체는 원문 그대로 복사(원문 보존 원칙). 단, 그 주변의 해설·판정 근거·메모 서술은 한글 중심 + 한자 병기 규칙을 적용.
   - Tester 는 한자 단독 노출(한글 병기 누락)을 발견하면 `severity: observation` 이상으로 지적한다.

5. **Report 감사 형식**
   - Coder report는 "26파일 전수 Read"와 같은 추상적 주장 대신, **현 세션 내 실제 Read 호출 목록**(파일명·offset·limit)을 기록한다.
   - self-check 체크박스는 신뢰되지 않는다. 체크박스 대신 **검증 가능한 증거**(원문 file_path:line_range, 복사 구절)로 제출한다.

6. **배치 크기 제한 (1회 Coder 호출 단위)**
   - 기출 관련 Coder 호출 1회의 작업 단위는 **1개 연도 × 1개 과목(A 또는 B)**으로 고정한다. (예: "2016-A", "2019-B" 단일 파일)
   - 한 호출에서 복수 연도·복수 과목·커버리지 맵 전체를 처리하는 태스크는 금지한다. 이는 TASK-175A에서 293 row 일괄 처리가 성실성 붕괴(2014~2019 구간 대량 오매핑)를 유발한 사례를 반영한 제약이다.
   - 각 호출은 해당 시험지 1개(기입형·서술형·논술형 전체 포함, 통상 14~23 문항)에 대해 원문 직독·3단계 확정·메모 복사 인용·line range 병기를 빠짐없이 수행해야 한다.
   - 다음 연도·과목으로 진행하기 전 **반드시 Tester 검증 PASS**를 받아야 한다. 누락 시 Manager가 차단한다.
   - 태스크 수가 늘어도 허용한다. 정확도가 속도보다 우선한다.

#### Tester 규칙

1. **직접 풀이 후 대조**
   - 각 row 검증 시 Tester는 원문 **문제 + 제시문을 직접 Read**하고 **직접 풀이**해 사상가·개념·분류를 독립적으로 도출한 뒤 Coder의 row와 대조한다.
   - Coder가 기재한 답을 선입견으로 받아들이지 않는다. Tester 독립 풀이와 일치할 때에만 PASS.

2. **3중 일치 검증**
   - **문제 ↔ Coder 분류 일치**: 발문이 요구하는 답 형태(사상가 지명/개념 설명/비교/고르기)가 분류와 맞는지
   - **제시문 ↔ Coder 인용구절 일치**: Coder가 메모에 복사한 구절이 원문에 실제 존재하는지 `grep -F`로 기계 검증
   - **사상가 ↔ 제시문 내용 일치**: 사상가의 trademark(저서명·핵심 개념·고유 용어)가 제시문에 등장하는지 확인

3. **"grep 0건" 규칙**
   - Coder 인용 구절 또는 주장 사상가의 trademark 키워드(한글·한자·영문)가 원문 파일에서 `grep -F`/`grep -E`로 0건이면 **즉시 blocker 판정**. 예외 없음.

4. **row-by-row 전수 검증 (필수, spot-check 금지)**
   - ethics-study 프로젝트의 모든 기출 관련 Tester 태스크는 **전수 검증만 허용**한다. spot-check·sample-only 판정은 금지한다.
   - 근거: TASK-175B에서 "2020~2026 spot-check 통과"로 내린 판정이 실제로는 2020-B/2021-A-B/2022-A-B 전면 오매핑을 놓친 허위 통과였음(BLK-175D-011). Tester 자체의 감사 부실이 블로커 누적을 악화시킴.
   - 규모가 커 1세션 내 처리 불가능하면 **Manager와 사전에 sample 범위·미검증 영역을 합의**하고, 미검증 row는 "미검증(TASK-XXX 이관)"으로 명시 표기한다. 암묵적 누락 금지.
   - Tester report에는 검증한 원문 파일별 Read 호출 증거(file_path + offset/limit)를 반드시 기록한다.
   - 본 규칙은 ethics-study 프로젝트 전용이며, 공용 `agents/tester.md`는 수정하지 않는다.

## 현재 상태
- Phase 1~5 완료: 55명 사상가, 568 claims (ES 실측)
- Phase 6 진행 중: 기출 스캔 → 보강 → 해설 작성
