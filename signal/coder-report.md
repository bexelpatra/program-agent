---
agent: coder
task_id: TASK-028
status: DONE
timestamp: 2026-03-30T01:00:00+09:00
---

## 결과 요약

tester-report-TASK-025.md에서 지적된 칸트 데이터 이슈 4건 모두 수정 완료.

---

## 수정 항목 목록

### 1. kant-lectures-ethics — year 및 significance 수정
- **수정 전**: `year: 1780`, significance에 노트 종류별 연도 언급 없음
- **수정 후**: `year: 1775`, significance에 "Collins 노트(c.1775), Mrongovius 노트(1784-85), Vigilantius 노트(1793-94)" 언급 추가
- **근거**: Collins 노트가 가장 대표적이며 c.1775년 기준이 통용됨

### 2. kant-claim-017 — source_detail 수정
- **수정 전**: `MS 6:429~431 (도덕형이상학 덕론 §9); 『진실을 말할 의무에 관하여』(1797) 8:425~430`
- **수정 후**: `MS 6:429~431 (도덕형이상학 덕론 §9); 『인간애에서 거짓말할 권리가 있다는 주장에 관하여(Über ein vermeintes Recht aus Menschenliebe zu lügen)』(1797) 8:423~430`
- **변경사항**: 에세이 제목 정정, 독일어 원제 추가, 시작 페이지 8:425 → 8:423

### 3. kant-claim-018 — source_detail 수정
- **수정 전**: `KpV 5:21~26, 59~65 (실천이성비판 제1부 제1편 제3장)`
- **수정 후**: `KpV 5:22~26, 35~41 (실천이성비판 제1부 제1편 실천원칙론)`
- **변경사항**: 페이지 범위 조정(5:22~26, 35~41), 장 구분 명칭 수정

### 4. aristotle-rel-004 — description 초점 재조정
- **수정 전**: 주로 칸트의 아리스토텔레스 비판에 집중한 서술
- **수정 후**: (1) 아리스토텔레스의 문제 설정이 칸트 윤리학의 출발점이 된 점, (2) 20세기 덕 윤리학 부흥(매킨타이어, 너스바움 등)을 통한 간접적 영향으로 재기술
- **근거**: "influenced" 관계에 맞게, 아리스토텔레스가 칸트에게 영향을 준 관점으로 초점 이동

---

## ES 업데이트 확인

| 문서 | 인덱스 | 이전 _version | 수정 후 _version | result |
|------|--------|--------------|-----------------|--------|
| kant-lectures-ethics | ethics-works | 1 | 2 | updated |
| kant-claim-017 | ethics-claims | 2 | 3 | updated |
| kant-claim-018 | ethics-claims | 2 | 3 | updated |
| aristotle-rel-004 | ethics-relations | 2 | 3 | updated |

---

## 이슈/블로커

없음.
