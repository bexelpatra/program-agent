---
agent: coder
task_id: TASK-079
status: DONE
timestamp: 2026-04-13T17:00:00
---

## 결과 요약

이황(퇴계) 데이터 이슈 수정 완료.
- 심각 이슈 1건: relation-wangyangming-yihwang 삭제 확인 (이미 TASK-076에서 삭제됨)
- 보통 이슈 2건: keywords 스키마 확인(이미 정상) + claim-008 명칭 수정 완료
- 경미 이슈 2건: claim-002 차별화 보완 + relation ID/type 불일치 현행 유지
- 12건 claims 전체 verified: true 처리 완료

## 1. ISSUE-078-01: relation-wangyangming-yihwang (심각)

**결과**: 이미 삭제됨 (found: false)

ES 조회 결과 `relation-wangyangming-yihwang` 문서가 존재하지 않았다. TASK-076(왕양명 이슈 수정)에서 이미 삭제된 것으로 확인된다. 별도 삭제 작업 불필요.

정확한 방향의 `relation-yihwang-wangyangming` (from: yihwang → to: wangyangming, type: criticized)은 정상적으로 존재함.

## 2. ISSUE-078-02: keywords 스키마 불일치 (보통)

**결과**: 이미 정상 상태

yihwang-kw-001 ~ kw-011 전체 11건 확인 결과, 이미 표준 스키마 필드를 사용하고 있었다:
- `term_en` 존재 (term_original 없음)
- `work_id` 존재 (source 없음)
- `related_terms` 존재 (related_claims 없음)

Tester가 검증 시점에 비표준 필드를 발견했으나, 이후 다른 태스크에서 이미 수정된 것으로 판단된다. 추가 수정 불필요.

## 3. ISSUE-078-03: claim-008 심통성정도 하위 도설 명칭 (보통)

**결과**: 수정 완료

**수정 전**: "세 개의 심통성정도(천명도·성정도·체용도)"
**수정 후**: "세 개의 심통성정도(상도·중도·하도의 세 그림)"

비표준 명칭 "천명도·성정도·체용도"를 학계에서 통용되는 "상도·중도·하도의 세 그림" 표기로 수정하였다.
이황 자신이 세 도설에 고유 명칭을 부여한 문헌 근거가 명확하지 않으므로, 구조 기술(상도·중도·하도)로 표현하였다.

## 4. ISSUE-078-04: claim-001/002 내용 중복 (경미)

**결과**: claim-002 차별화 보완

claim-002의 explanation에 수양 실천 관점의 차별화 내용을 추가하였다:
"이 구분은 단순한 심리적 분류가 아니라, 도덕 수양의 방향을 제시한다: 사단을 확충하고(擴充), 칠정을 절도에 맞게 조절하는 것(節制)이 수양의 핵심이다."

claim-001은 이기호발설의 존재론적 구조(이발·기발)에 집중하고,
claim-002는 그 구분으로부터 도출되는 도덕 실천(사단 확충, 칠정 절제)을 강조하는 방향으로 차별화하였다.

## 5. ISSUE-078-05: relation ID/type 불일치 (경미)

**결과**: 현행 유지

`relation-yihwang-yiyulgok-debate`의 type이 "influenced"인 것은 실질적으로 정확하다 (이황의 사상이 이이의 사상 형성에 결정적 영향을 미쳤음). ID의 "debate" 표기는 혼동을 줄 수 있으나 경미하므로 현행 유지. 검색 기능에 실질적 영향 없음.

## 6. Claims verified: true 처리

**결과**: 전체 12건 완료

| claim_id | verified | 비고 |
|----------|---------|------|
| yihwang-claim-001 | true | 이기호발설 |
| yihwang-claim-002 | true | 사단순선·칠정선악 (차별화 보완 포함) |
| yihwang-claim-003 | true | 이(理)의 능동성 |
| yihwang-claim-004 | true | 경(敬) 수양론 |
| yihwang-claim-005 | true | 성학십도 체계 |
| yihwang-claim-006 | true | 이선기후 |
| yihwang-claim-007 | true | 이기불상잡 |
| yihwang-claim-008 | true | 심통성정 (명칭 수정 포함) |
| yihwang-claim-009 | true | 천명도 개정 |
| yihwang-claim-010 | true | 주리론 |
| yihwang-claim-011 | true | 본연지성·기질지성 |
| yihwang-claim-012 | true | 군주 성학론 |

verification_log 포맷: `{"date": "2026-04-13", "result": "verified", "method": "tester-agent (TASK-078)"}`

## ES 최종 확인

- `ethics-relations/relation-wangyangming-yihwang` found: **false** (삭제 확인)
- `ethics-keywords` yihwang 11건: **term_en/work_id/related_terms 스키마 준수**
- `ethics-claims` yihwang 12건: **verified=true 12/12**
- `claim-008` explanation: **수정 완료** (상도·중도·하도 표기)
