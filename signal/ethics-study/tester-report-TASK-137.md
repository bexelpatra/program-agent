# Tester Report — TASK-137: 콜버그 데이터 검증

## 상태: DONE

## 검증 일시
2026-04-14

---

## 1. 사상가 (ethics-thinkers) 검증

**ID**: `kohlberg` — **존재 확인: ✓**

| 필드 | 값 | 정확성 |
|------|-----|--------|
| id | kohlberg | ✓ |
| name | 로렌스 콜버그 | ✓ |
| name_en | Lawrence Kohlberg | ✓ |
| field | moral_development | ✓ |
| era | 현대 | ✓ |
| birth_year | 1927 | ✓ |
| death_year | 1987 | ✓ |
| background | 브롱스빌 출생, 이스라엘 이민 항해, 시카고 대학교 박사(1958), 예일→시카고→하버드 HGSE 교수, 기생충 감염 이후 만성 우울증, 1987년 익사체 발견 | ✓ |
| core_philosophy | 3수준 6단계 순차 진행, 각 단계별 특성(1~6단계) 상세 기술, 정의·역할채택·인지발달주의 언급 | ✓ |

**학술 정확성 검토:**
- birth_year(1927), death_year(1987) 정확함
- background에서 박사논문(1958)과 경력 기술이 정확함. 자살로 추정된 사인도 정확하게 서술됨
- core_philosophy에서 각 단계 명칭·특성 기술이 학술 표준과 일치함
- 1단계: 벌과 복종(처벌 회피, 권위복종) ✓
- 2단계: 도구적 상대주의(자기이익, 호혜적 교환) ✓
- 3단계: 착한 소년·소녀(타인 기대, 승인 추구) ✓
- 4단계: 법과 질서(사회제도 유지, 법 준수) ✓
- 5단계: 사회계약(민주적 합의, 기본권) ✓
- 6단계: 보편적 윤리 원칙(자율적 선택, 칸트·롤스 기반) ✓

**판정: 이상 없음**

---

## 2. 저서 (ethics-works) 검증

**총 저서 수: 6개** (예상 6개) ✓

| ID | 제목(원문) | 연도 | 확인 |
|----|-----------|------|------|
| kohlberg-dissertation-1958 | The Development of Modes of Thinking and Choices in Years 10 to 16 | 1958 | ✓ |
| kohlberg-philosophy-moral-development-1981 | Essays on Moral Development, Vol. 1: The Philosophy of Moral Development | 1981 | ✓ |
| kohlberg-psychology-moral-development-1984 | Essays on Moral Development, Vol. 2: The Psychology of Moral Development | 1984 | ✓ |
| kohlberg-meaning-measurement-1981 | The Meaning and Measurement of Moral Development | 1981 | ✓ |
| kohlberg-just-community-1985 | The Just Community Approach to Moral Education in Theory and Practice | 1985 | ✓ |
| kohlberg-moral-stages-moralization-1976 | Moral Stages and Moralization: The Cognitive-Developmental Approach | 1976 | ✓ |

**필수 저서 확인:**
- Essays on Moral Development Vol. 1 (1981) ✓
- Essays on Moral Development Vol. 2 (1984) ✓

**학술 정확성 검토:**
- 모든 연도 정확함
- significance 및 key_concepts 내용이 학술적으로 적절함
- 박사논문(1958)은 MJI와 하인츠 딜레마의 원형임을 올바르게 기술

**판정: 이상 없음**

---

## 3. 주장 (ethics-claims) 검증

**총 주장 수: 20개** (예상 20개) ✓

### 단계별 주장 목록

| ID | 핵심 내용 요약 | work_id 유효 |
|----|--------------|------------|
| kohlberg-claim-001 | 3수준 6단계 순차 진행(전체 개요) | ✓ (Vol.1 1981) |
| kohlberg-claim-002 | 1단계 — 벌과 복종 지향 | ✓ (Vol.2 1984) |
| kohlberg-claim-003 | 2단계 — 도구적 상대주의, 호혜적 교환 | ✓ (Vol.2 1984) |
| kohlberg-claim-004 | 3단계 — 착한 소년·소녀, 대인관계 | ✓ (Vol.2 1984) |
| kohlberg-claim-005 | 4단계 — 법과 질서, 사회체계 도덕성 | ✓ (Vol.2 1984) |
| kohlberg-claim-006 | 5단계 — 사회계약, 기본권 | ✓ (Vol.1 1981) |
| kohlberg-claim-007 | 6단계 — 보편적 윤리 원칙, 칸트·롤스 기반 | ✓ (Vol.1 1981) |
| kohlberg-claim-008 | 보편성 — 다양한 문화권 연구 | ✓ (Vol.1 1981) |
| kohlberg-claim-009 | 역할채택(role-taking) 핵심 메커니즘 | ✓ (Vol.2 1984) |
| kohlberg-claim-010 | 하인츠 딜레마, MJI 방법론 | ✓ (dissertation 1958) |
| kohlberg-claim-011 | +1 전략 교수법 | ✓ (1976 논문) |
| kohlberg-claim-012 | 정의공동체 접근 | ✓ (Just Community 1985) |
| kohlberg-claim-013 | 도덕적 분위기(moral atmosphere) | ✓ (Vol.2 1984) |
| kohlberg-claim-014 | 인지발달주의 도덕교육(덕목 가방 비판) | ✓ (1976 논문) |
| kohlberg-claim-015 | 7단계 가능성 탐구 | ✓ (Vol.1 1981) |
| kohlberg-claim-016 | 도덕 판단과 행동의 관계(2차대전 사례) | ✓ (Vol.2 1984) |
| kohlberg-claim-017 | 인지발달과 도덕발달 관계(형식 조작기) | ✓ (Vol.1 1981) |
| kohlberg-claim-018 | 길리건 비판 수용과 정의 중심 옹호 | ✓ (Vol.2 1984) |
| kohlberg-claim-019 | 도덕 딜레마 토론 교수법 | ✓ (Vol.1 1981) |
| kohlberg-claim-020 | 6단계와 롤스 정의론의 철학적 연결 | ✓ (Vol.1 1981) |

**모든 work_id가 유효한 저서를 참조함: ✓**

### 필수 포함 항목 확인

| 항목 | 확인 |
|------|------|
| 3수준 6단계 전체 구조 | ✓ (claim-001) |
| 1단계 특성 (벌과 복종) | ✓ (claim-002) |
| 2단계 특성 (도구적 상대주의) | ✓ (claim-003) |
| 3단계 특성 (착한 소년·소녀) | ✓ (claim-004) |
| 4단계 특성 (법과 질서) | ✓ (claim-005) |
| 5단계 특성 (사회계약) | ✓ (claim-006) |
| 6단계 특성 (보편적 윤리 원칙) | ✓ (claim-007) |
| 역할채택(role-taking) | ✓ (claim-009) |
| 정의공동체(just community) | ✓ (claim-012) |
| 하인츠 딜레마 | ✓ (claim-010) |
| +1 전략 | ✓ (claim-011) |
| 도덕적 분위기(moral atmosphere) | ✓ (claim-013) |
| 보편성 | ✓ (claim-008) |
| 7단계 | ✓ (claim-015) |

**모든 필수 항목 포함 확인 ✓**

### claim·explanation·argument 필드 적절성

- claim: 각 단계의 핵심 명제를 간결하고 정확하게 서술. 학술 문헌과 일치
- explanation: 하인츠 딜레마에서의 전형적 응답 예시를 포함하여 구체적으로 설명
- argument: 해당 주장의 이론적 근거와 경험적 지지를 적절하게 기술

**6단계 각각 혼동 여부 점검:**
- 1단계(벌·복종) ↔ 2단계(도구적 상대주의) 혼동 없음 ✓
- 3단계(대인관계) ↔ 4단계(법과 질서) 혼동 없음 ✓
- 5단계(사회계약) ↔ 6단계(보편 원칙) 혼동 없음 ✓
- 각 단계의 "사회적 관점(sociomoral perspective)" 특성이 올바르게 반영됨 ✓

**판정: 이상 없음**

---

## 4. 키워드 (ethics-keywords) 검증

**총 키워드 수: 20개** (예상 20개) ✓

| ID | term | term_en | work_id |
|----|------|---------|---------|
| kohlberg-kw-001 | 3수준 6단계 | Three Levels and Six Stages | Vol.1 1981 ✓ |
| kohlberg-kw-002 | 전인습적 도덕성 | Pre-conventional Morality | Vol.2 1984 ✓ |
| kohlberg-kw-003 | 인습적 도덕성 | Conventional Morality | Vol.2 1984 ✓ |
| kohlberg-kw-004 | 후인습적 도덕성 | Post-conventional Morality | Vol.1 1981 ✓ |
| kohlberg-kw-005 | 정의공동체 | Just Community | Just Community 1985 ✓ |
| kohlberg-kw-006 | 역할채택 | Role-taking | Vol.2 1984 ✓ |
| kohlberg-kw-007 | 하인츠 딜레마 | Heinz Dilemma | dissertation 1958 ✓ |
| kohlberg-kw-008 | +1 전략 | Plus-one Strategy | 1976 논문 ✓ |
| kohlberg-kw-009 | 도덕적 분위기 | Moral Atmosphere | Just Community 1985 ✓ |
| kohlberg-kw-010 | 도덕 판단 면접(MJI) | Moral Judgment Interview | dissertation 1958 ✓ |
| kohlberg-kw-011 | 인지발달주의 | Cognitive-developmentalism | 1976 논문 ✓ |
| kohlberg-kw-012 | 보편성 | Universality | Vol.1 1981 ✓ |
| kohlberg-kw-013 | 공동체 회의 | Community Meeting | Just Community 1985 ✓ |
| kohlberg-kw-014 | 인지적 불균형 | Cognitive Disequilibrium | 1976 논문 ✓ |
| kohlberg-kw-015 | 사회적 관점 | Sociomoral Perspective | Vol.2 1984 ✓ |
| kohlberg-kw-016 | 순서불변성 | Invariant Sequence | Vol.1 1981 ✓ |
| kohlberg-kw-017 | 덕목 가방 비판 | Bag of Virtues Critique | 1976 논문 ✓ |
| kohlberg-kw-018 | 표준 잠점 채점법 | Standard Issue Scoring | Vol.2 1984 ✓ |
| kohlberg-kw-019 | 사회계약 | Social Contract | Vol.1 1981 ✓ |
| kohlberg-kw-020 | 딜레마 토론 | Dilemma Discussion | Vol.1 1981 ✓ |

**term, term_en, definition, thinker_id, work_id, related_terms 필드 모두 존재 ✓**

**학술 정확성 검토:**
- 모든 키워드의 definition이 학술적으로 정확하고 충분히 설명적임
- work_id 참조가 모두 유효한 저서를 가리킴
- related_terms가 적절하게 연관 개념을 연결함

**판정: 이상 없음**

---

## 5. 관계 (ethics-relations) 검증

**총 관계 수: 6개** (예상 6개) ✓

| ID | from_thinker | type | to_thinker |
|----|------------|------|------------|
| piaget-influenced-kohlberg | piaget | influenced | kohlberg ✓ |
| rawls-influenced-kohlberg | rawls | influenced | kohlberg ✓ |
| kohlberg-influenced-gilligan | kohlberg | influenced | gilligan ✓ |
| kohlberg-influenced-rest | kohlberg | influenced | rest ✓ |
| kohlberg-criticized-noddings | kohlberg | criticized | noddings ✓ |
| kohlberg-influenced-habermas | kohlberg | influenced | habermas ✓ |

**필수 관계 확인:**
- piaget → kohlberg (influenced) ✓ — 피아제의 인지발달론이 콜버그 이론의 직접적 기반임을 기술

**description 적절성:**
- piaget→kohlberg: 2단계→6단계 세분화, MJI의 임상 면접법 발전, 인지발달-도덕발달 대응관계 언급 ✓
- rawls→kohlberg: 원초적 입장, 무지의 베일, 6단계 정당화 연결 ✓
- kohlberg→gilligan: 남성 중심 편향 비판, 배려윤리 발전, "다른 목소리로"(1982) 명시 ✓
- kohlberg→rest: DIT 개발, 4구성요소 모델 언급 ✓
- kohlberg→noddings: 배려 vs 정의 대립, 구체적 관계의 도덕 강조 ✓
- kohlberg→habermas: 담론윤리, 의사소통적 합리성 연결 ✓

**판정: 이상 없음**

---

## 종합 판정

| 항목 | 예상 | 실제 | 판정 |
|------|------|------|------|
| 사상가 (ethics-thinkers) | 1개 | 1개 | ✓ PASS |
| 저서 (ethics-works) | 6개 | 6개 | ✓ PASS |
| 주장 (ethics-claims) | 20개 | 20개 | ✓ PASS |
| 키워드 (ethics-keywords) | 20개 | 20개 | ✓ PASS |
| 관계 (ethics-relations) | 6개 | 6개 | ✓ PASS |

## 이슈/블로커

없음. 모든 검증 항목 통과.

## 학술 정확성 총평

- 콜버그 도덕발달론의 핵심 개념(3수준 6단계)이 각 단계의 명칭, 특성, 사회적 관점(sociomoral perspective), 전형적 반응 예시를 포함하여 정확하게 입력됨
- 6단계 각각의 특성이 혼동 없이 명확하게 구분됨
- 주요 저서의 연도·제목이 정확함 (Essays on Moral Development Vol.1/Vol.2 포함)
- 역할채택, +1 전략, 정의공동체, 도덕적 분위기, 7단계 등 고급 개념이 모두 포함됨
- piaget→kohlberg 관계가 이론적 계보를 정확하게 반영함
- 길리건 비판, 롤스와의 철학적 연결, 하버마스 담론윤리와의 관계 등 학술적 맥락이 충실하게 구현됨
