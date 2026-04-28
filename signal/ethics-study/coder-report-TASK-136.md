# Coder Report — TASK-136

## Task
콜버그(Lawrence Kohlberg) 데이터 입력 (ES 직접) — 도덕발달 핵심, claims 15+

## Status
DONE

## 작업 내용

### 스크립트 작성
- 파일: `projects/ethics-study/scripts/insert_kohlberg.py`
- 기존 `insert_piaget.py`, `insert_rawls.py` 패턴을 따라 작성

### ES 적재 결과

| 항목 | 수량 | 상세 |
|------|------|------|
| 사상가 (ethics-thinkers) | 1명 | kohlberg (created) |
| 저서 (ethics-works) | 6개 | 박사논문~정의공동체 |
| 주장 (ethics-claims) | **20개** | 6단계 전부, 교육론, 후기 이론 포함 |
| 키워드 (ethics-keywords) | **20개** | 3수준 6단계, 정의공동체, 역할채택 등 |
| 관계 (ethics-relations) | 6개 | piaget→kohlberg, rawls→kohlberg, kohlberg→gilligan 등 |
| 분야 (ethics-fields) | — | moral_development 이미 존재 확인 |

모든 항목 `created` 또는 `updated` 성공. 오류 없음.

### 주장(claims) 목록 (20개)

- claim-001: 3수준 6단계 전체 개요
- claim-002: 1단계 — 벌과 복종 지향
- claim-003: 2단계 — 도구적 상대주의 지향
- claim-004: 3단계 — 착한 소년·소녀 지향
- claim-005: 4단계 — 법과 질서 지향
- claim-006: 5단계 — 사회계약 지향
- claim-007: 6단계 — 보편적 윤리 원칙 지향
- claim-008: 도덕발달의 보편성(문화 초월적)
- claim-009: 역할채택(role-taking) 메커니즘
- claim-010: 하인츠 딜레마와 도덕 판단 면접(MJI)
- claim-011: +1 전략(Plus-one strategy)
- claim-012: 정의공동체 접근(Just Community Approach)
- claim-013: 도덕적 분위기(moral atmosphere)
- claim-014: 인지발달주의 관점 — 덕목 가방 비판
- claim-015: 7단계 — 우주적·종교적 관점(후기)
- claim-016: 도덕 판단과 도덕 행동의 관계
- claim-017: 도덕발달과 인지발달의 관계
- claim-018: 길리건의 배려윤리와의 관계
- claim-019: 딜레마 토론을 통한 도덕교육
- claim-020: 롤스 정의론과 6단계의 철학적 연결

### 저서(works) 목록 (6개)

1. 박사논문 (1958) — 6단계 모델 원형
2. 도덕 발달의 철학 Vol.1 (1981) — 철학적 기초
3. 도덕 발달의 심리학 Vol.2 (1984) — 심리학적 기초
4. 도덕 발달의 의미와 측정 (1981) — 방법론 강연
5. 정의공동체 접근 (1985) — 실천 이론
6. 도덕 단계와 도덕화 (1976) — 인지발달주의 도덕교육 논문

### 관계(relations) 목록 (6개)

- piaget → kohlberg (influenced): 인지발달론 기반 확장
- rawls → kohlberg (influenced): 정의론의 철학적 기반 강화
- kohlberg → gilligan (influenced): 비판적 계승으로 배려윤리 발전
- kohlberg → rest (influenced): DIT·4구성요소 모델 발전
- kohlberg → noddings (criticized): 추상적 정의 중심 비판
- kohlberg → habermas (influenced): 담론윤리로의 재해석

## 완료 조건 확인

- [x] `projects/ethics-study/scripts/insert_kohlberg.py` 스크립트 작성
- [x] 스크립트 실행하여 ES에 데이터 적재 완료 (오류 없음)
- [x] claims 15개 이상: **20개** 입력
- [x] keywords 15개 이상: **20개** 입력
- [x] 관계 5개 이상: **6개** 입력
