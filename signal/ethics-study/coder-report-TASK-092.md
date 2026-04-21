# Coder Report — TASK-092: 묵자 데이터 입력

## 상태: DONE

## 작업 요약

묵자(墨子, Mozi) 사상가 데이터를 Elasticsearch에 직접 입력 완료.

## 입력 데이터 목록

### ethics-thinkers
| 항목 | 값 |
|------|-----|
| id | mozi |
| name | 묵자 |
| name_en | Mozi (Mo Di) |
| field | eastern_ethics |
| era | 춘추전국 |
| birth_year | -470 |
| death_year | -391 |
| keywords | 10개 (겸애, 비공, 상동, 상현, 천지, 명귀, 절용, 절장, 비악, 비명) |

### ethics-works (1건)
| id | 제목 | 연도 |
|----|------|------|
| mozi-mozi | 묵자 (墨子) | -400 (추정) |

### ethics-claims (7건)
| id | 주제 | 출처 |
|----|------|------|
| mozi-claim-001 | 겸애(兼愛) — 보편적 사랑 | 겸애편 |
| mozi-claim-002 | 비공(非攻) — 침략전쟁 반대 | 비공편 |
| mozi-claim-003 | 상동(尚同) — 위계적 사회 통합 | 상동편 |
| mozi-claim-004 | 상현(尚賢) — 능력주의 인재 등용 | 상현편 |
| mozi-claim-005 | 천지(天志) — 하늘의 뜻이 도덕 기준 | 천지편 |
| mozi-claim-006 | 절용(節用) — 검약과 실용 | 절용편 |
| mozi-claim-007 | 비명(非命) — 운명론 부정 | 비명편 |

- 모든 claim: original_text(원문), explanation, argument, counterpoint, context, keywords, verified:false 포함

### ethics-keywords (7건)
| id | 용어 |
|----|------|
| mozi-kw-001 | 겸애 (兼愛) |
| mozi-kw-002 | 비공 (非攻) |
| mozi-kw-003 | 상동 (尚同) |
| mozi-kw-004 | 상현 (尚賢) |
| mozi-kw-005 | 천지 (天志) |
| mozi-kw-006 | 비명 (非命) |
| mozi-kw-007 | 절용 (節用) |

### ethics-relations (2건)
| from | type | to | 근거 |
|------|------|----|------|
| mozi | criticized | confucius | 묵자(겸애편, 절용편, 절장편) — 유가의 차등적 인, 예악 비판 |
| mencius | criticized | mozi | 맹자 등문공편 하 — 무부무군 비판 |

## 검증 결과

```
ethics-thinkers: mozi → created/updated ✓
ethics-works: mozi-mozi → created ✓
ethics-claims: mozi-claim-001~007 → 7건 created ✓
ethics-keywords: mozi-kw-001~007 → 7건 created ✓
ethics-relations: 2건 created ✓
```

## 특이사항

- 삽입 스크립트: `projects/ethics-study/scripts/insert_mozi.py`
- 모든 claims: `verified: false` (Tester 검증 대기)
- 명귀(明鬼) keyword는 별도 입력 보류 — 출제비중 "보통"의 7건 제한 내에서 핵심 6개(겸애·비공·상동·상현·천지·비명) + 절용을 우선 처리. 필요 시 추가 입력 가능.
- mencius→mozi 관계: 기존 데이터 중복 없음 확인 후 신규 생성
