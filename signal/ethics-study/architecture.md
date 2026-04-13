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

### Phase 5: 통일교육/시민윤리
| 순서 | 주제/이론가 | 구분 | 출제비중 | 데이터 규모 | 상태 |
|------|------------|------|----------|------------|------|
| 1 | 갈퉁 | 평화학 | 중요 | 축소 (claims 6~8) | |
| 2 | 통일교육 주제 | 통일 | 중요 | 주제 중심 | |
| 3 | 민주시민교육 | 시민윤리 | 보통 | 주제 중심 | |

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

## 현재 상태
- v2 파이프라인 가동 중 (ES-first 입력 → opus 검증 → 수정 → YAML export)
- Phase 1 서양윤리: 5/10 완료 (소크라테스, 플라톤, 아리스토텔레스, 아우구스티누스, 토마스 아퀴나스)
- 다음 작업: 칸트 (출제비중 "핵심", claims 15+건)
- 스키마 변경 시 이전 사상가에도 소급 적용 필요 (사용자 지시)
