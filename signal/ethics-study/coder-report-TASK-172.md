---
agent: coder
task_id: TASK-172
status: DONE
timestamp: 2026-04-15T00:00:00
---

## 결과 요약

Phase 5 신규 분야 문서 3개(peace_studies, unification_edu, civic_edu)를 `ethics-fields` ES 인덱스에 upsert 하였다.

기존 인덱스에는 3개 field(eastern_ethics=2, political_philosophy=3, moral_development=4)가 있었고, 최대 order=4 기준으로 신규 3개를 5/6/7로 연번 배정.

재실행 가능한 스크립트로 작성했으며, 이미 존재하는 id는 order를 보존하면서 name/description만 갱신하도록 멱등성을 보장하였다.

## 변경된 파일
- projects/ethics-study/scripts/insert_phase5_fields.py (신규)

## 실행 결과

```
[info] 기존 max order = 4
[field] peace_studies: created (order=5, result=created)
[field] unification_edu: created (order=6, result=created)
[field] civic_edu: created (order=7, result=created)
```

## 검증 (ES 쿼리)

`GET /ethics-fields/_search?sort=order:asc` 결과 전체 6건:

| id | name | order |
|----|------|-------|
| eastern_ethics | 동양윤리 | 2 |
| political_philosophy | 정치철학 | 3 |
| moral_development | 도덕발달론 | 4 |
| peace_studies | 평화학 | 5 |
| unification_edu | 통일교육 | 6 |
| civic_edu | 민주시민교육 | 7 |

신규 3개 모두 정상 검색됨. description 필드도 지시 사항대로 저장됨을 스크립트 출력(`[verify]` 블록)으로 확인.

## 이슈/블로커
없음.

## 참고
- 기존 스키마의 `order` 필드는 1번(western_ethics)이 없는 상태(2~4만 존재)였다. 본 태스크에서는 "기존 max+1/2/3" 지시에 따라 5/6/7을 사용했으며 누락된 1번 보정은 별도 태스크 영역으로 판단하여 건드리지 않았다.

## 다음 제안
- Phase 5 사상가 데이터 입력 태스크(갈퉁/백낙청/강만길/듀이/아렌트)에서 field 참조값으로 `peace_studies`, `unification_edu`, `civic_edu`를 사용하면 된다.
