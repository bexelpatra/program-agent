# Coder Report — TASK-116

## 태스크
샌델(Michael Sandel) 데이터 ES 직접 입력

## 상태
DONE

## 완료 일시
2026-04-13

---

## 입력 결과 요약

### ethics-thinkers
| 항목 | 값 |
|------|-----|
| id | sandel |
| name | 마이클 샌델 |
| name_en | Michael Sandel |
| field | political_philosophy |
| era | 현대 |
| birth_year | 1953 |
| death_year | null |

### ethics-works (5건)
| id | 제목 | 연도 |
|----|------|------|
| sandel-liberalism-limits-justice | 자유주의와 정의의 한계 | 1982 |
| sandel-democracy-discontent | 민주주의의 불만 | 1996 |
| sandel-justice-what-right-thing | 정의란 무엇인가 | 2009 |
| sandel-what-money-cant-buy | 돈으로 살 수 없는 것들 | 2012 |
| sandel-tyranny-of-merit | 공정하다는 착각 | 2020 |

### ethics-claims (10건)
| id | 핵심 주장 요약 |
|----|----------------|
| sandel-claim-001 | 무연고적 자아(unencumbered self) 비판 — 롤스 원초적 입장의 자아 개념 해체 |
| sandel-claim-002 | 구성적 공동체 — 공동체는 자아를 구성하는 것이지 선택하는 것이 아니다 |
| sandel-claim-003 | 정의는 좋은 삶 논의를 회피할 수 없다 — 롤스 중립성 원칙 비판 |
| sandel-claim-004 | 공화주의적 자유 — 지배로부터의 자유 + 시민적 덕을 통한 자아통치 |
| sandel-claim-005 | 시장의 도덕적 한계 — 부패 논거와 공정성 논거 |
| sandel-claim-006 | 능력주의 비판 — 운의 임의성, 오만과 굴욕의 정치 |
| sandel-claim-007 | 도덕·종교적 논의를 정치에서 배제해서는 안 된다 |
| sandel-claim-008 | 아리스토텔레스적 정의 — 목적론적 재화 분배 |
| sandel-claim-009 | 기여적 정의와 노동의 존엄성 — 능력주의 대안 |
| sandel-claim-010 | 시장사회 vs 시장경제 구분 — 비시장 규범 영역 보호 |

### ethics-keywords (10건)
| id | 용어 | 영문 |
|----|------|------|
| sandel-kw-001 | 무연고적 자아 | unencumbered self |
| sandel-kw-002 | 구성적 공동체 | constitutive community |
| sandel-kw-003 | 공동선 | common good |
| sandel-kw-004 | 시민적 덕 | civic virtue |
| sandel-kw-005 | 시장의 도덕적 한계 | moral limits of markets |
| sandel-kw-006 | 능력주의 | meritocracy |
| sandel-kw-007 | 공화주의적 자유 | republican liberty |
| sandel-kw-008 | 도덕적 공론 | moral argument in politics |
| sandel-kw-009 | 기여적 정의 | contributive justice |
| sandel-kw-010 | 중립성 비판 | critique of neutrality |

### ethics-relations (4건 신규, 기존 2건 유지)
| from | type | to | 비고 |
|------|------|----|------|
| rawls | influenced | sandel | 기존 존재 (relation-rawls-sandel) |
| macintyre | influenced | sandel | 기존 존재 (relation-macintyre-sandel) |
| aristotle | influenced | sandel | 신규 입력 |
| sandel | criticized | rawls | 신규 입력 |

> 참고: rawls→sandel, macintyre→sandel 관계가 이전에 이미 입력되어 있었음. 신규 입력 시 중복이 발생하여 자동 ID 부여된 중복 2건을 삭제 처리함.

---

## 검증 결과
- `GET ethics-thinkers/_doc/sandel` → found: true ✓
- works 5건, claims 10건, keywords 10건, relations 4건(sandel 관련) 확인 ✓
- 모든 claims의 verified: false (Tester 검증 대기)

---

## 특이 사항
- 기존에 `relation-rawls-sandel`, `relation-macintyre-sandel` 2건이 이미 입력되어 있었음
- 중복 방지를 위해 신규 중복분 삭제 완료
- aristotle→sandel, sandel→rawls 관계 신규 추가
