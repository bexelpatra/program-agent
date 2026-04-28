# Coder Report — TASK-098

## 상태: DONE

## 태스크
- **Task ID**: TASK-098
- **Title**: 홉스 데이터 입력 (ES 직접)

## 수행 내용

### 1. 분야(field) 추가
- `political_philosophy` (정치철학) 분야를 `ethics-fields` 인덱스에 신규 추가 (order: 3)

### 2. 사상가 (thinker) — 1건
- **id**: hobbes
- **name**: 토머스 홉스 (Thomas Hobbes), 1588~1679, 영국
- **field**: political_philosophy
- background, core_philosophy, philosophical_journey, keywords 포함

### 3. 저서 (works) — 5건
| ID | 제목 | 원제 | 연도 |
|----|------|------|------|
| hobbes-leviathan | 리바이어던 | Leviathan | 1651 |
| hobbes-de-cive | 시민론 | De Cive | 1642 |
| hobbes-de-corpore | 물체론 | De Corpore | 1655 |
| hobbes-de-homine | 인간론 | De Homine | 1658 |
| hobbes-elements-of-law | 법의 원리 | The Elements of Law | 1640 |

### 4. 주장 (claims) — 14건
| ID | 주제 |
|----|------|
| hobbes-claim-001 | 자연 상태 — 만인에 대한 만인의 투쟁 |
| hobbes-claim-002 | 자연권 — 자기보존의 권리 |
| hobbes-claim-003 | 자연법 — 이성의 명령 |
| hobbes-claim-004 | 사회계약 — 자연권의 상호 양도 |
| hobbes-claim-005 | 주권자론 — 절대주권 |
| hobbes-claim-006 | 대리(Authorization) 개념 |
| hobbes-claim-007 | 자기보존의 양도 불가능성 |
| hobbes-claim-008 | 커먼웰스 — 인공 인간 |
| hobbes-claim-009 | 유물론적 인간관 |
| hobbes-claim-010 | 정의 — 약속 이행 |
| hobbes-claim-011 | 신민의 자유 — 법의 침묵이 있는 곳 |
| hobbes-claim-012 | 자연적 평등 |
| hobbes-claim-013 | 주권자의 세 가지 형태 |
| hobbes-claim-014 | 공포와 복종의 정당성 |

- 모든 claim에 `argument`, `counterpoint`, `original_text` (영어 원문), `original_text_ko` (한국어 번역) 포함
- 모든 counterpoint에 특정 사상가 + 저서 근거 명시

### 5. 키워드 (keywords) — 10건
자연 상태, 사회계약, 주권자, 자연법, 자연권, 리바이어던, 대리(Authorization), 커먼웰스, 만인에 대한 만인의 투쟁, 자기보존

### 6. 관계 (relations) — 5건
| ID | 방향 | 유형 |
|----|------|------|
| relation-machiavelli-hobbes | 마키아벨리 → 홉스 | influenced |
| relation-hobbes-locke | 홉스 → 로크 | influenced |
| relation-hobbes-rousseau | 홉스 → 루소 | influenced |
| relation-hobbes-rawls | 홉스 → 롤스 | influenced |
| relation-hobbes-spinoza | 홉스 → 스피노자 | influenced |

## 검증 결과
- ES refresh 후 전수 확인 완료
- field: 1건, thinker: 1건, works: 5건, claims: 14건, keywords: 10건, relations: 5건
- 모든 claim: argument + counterpoint + original_text + original_text_ko 존재 확인
- 모든 verified: false (Tester 검증 대기)

## 생성 파일
- `projects/ethics-study/scripts/insert_hobbes.py`
