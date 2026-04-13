---
agent: coder
task_id: TASK-061
status: DONE
timestamp: 2026-04-13T15:30:00+09:00
---

## 결과 요약

맹자 데이터 이슈 4건(심각 3건 + 보통 1건) 모두 수정 완료. 전체 claims 17건 및 relations 4건에 verified: true 설정 완료.

## 수정 내역

### S-1: claim-011 work_id 오류 수정 -- FIXED
- **변경 전**: `work_id: mencius-jinxin` (진심편)
- **변경 후**: `work_id: mencius-mencius` (맹자 전체)
- **사유**: 대장부 구절의 실제 출처는 등문공편(滕文公篇) 하 3.2이나, 등문공편은 독립 works로 등록되어 있지 않으므로 맹자 전체(`mencius-mencius`)로 설정. `source_detail`은 이미 "등문공편 하 3.2"로 올바르게 기재되어 있어 유지.

### S-2: relation mencius→xunzi 방향 수정 -- FIXED
- **변경 전**: `from_thinker: mencius, to_thinker: xunzi, type: criticized` (맹자가 순자를 비판)
- **변경 후**: `from_thinker: xunzi, to_thinker: mencius, type: criticized` (순자가 맹자를 비판)
- **사유**: 역사적으로 순자(기원전 313~238)가 맹자(기원전 372~289)의 성선설을 비판한 것이지, 맹자가 순자를 비판한 것이 아님. 기존 문서(`relation-mencius-xunzi-debate`) 삭제 후 새 문서(`relation-xunzi-mencius-debate`) 생성.
- **description**: 내용 자체는 정확하므로 유지.

### S-3: relation mencius→gaozi description 서술 주어 수정 -- FIXED
- **변경 전**: "고자(告子)는 맹자와 직접 논쟁한 사상가로..." (고자가 주어)
- **변경 후**: "맹자(孟子)는 고자(告子)의 성무선악설(性無善惡說)을 정면으로 논박하며..." (맹자가 주어)
- **사유**: from→to 방향 규칙(from이 to를 criticized)에 맞게 맹자가 주어가 되도록 서술 수정.

### M-1: claim-004 work_id/source_detail 오류 수정 -- FIXED
- **변경 전**: `work_id: mencius-gongsunchou`, `source_detail: "맹자 공손추편(公孫丑篇) 상 2.6, 진심편(盡心篇) 상 7.21"`
- **변경 후**: `work_id: mencius-gaozi`, `source_detail: "맹자 고자편(告子篇) 상 6.6, 진심편(盡心篇) 상 7.21(참고)"`
- **사유**: 원문 "仁義禮智 非由外鑠我也 我固有之也 弗思耳矣"는 고자편 상 6.6의 문장. 진심편 7.21은 관련 참고로만 표기.

## verified 설정 현황

| 대상 | 건수 | 상태 |
|------|------|------|
| 이슈 수정 claims (011, 004) | 2건 | verified: true + verification_log 기록 |
| 이슈 없는 claims (나머지 15건) | 15건 | verified: true + verification_log 기록 |
| 이슈 수정 relations (xunzi, gaozi) | 2건 | verified: true + verification_log 기록 |
| 이슈 없는 relations (zhuxi, wangyangming) | 2건 | verified: true + verification_log 기록 |
| **합계** | **21건** | **모두 verified: true** |

## 수정 스크립트

- `projects/ethics-study/scripts/fix_mencius_issues.py`

## 비고

- confucius→mencius 관계는 `insert_confucius.py`에서 등록된 것이므로 이 태스크에서 처리하지 않음
- 참조 무결성 이슈(xunzi, gaozi, zhuxi, wangyangming이 ethics-thinkers에 미존재)는 해당 사상가 데이터 입력 시 자동 해결 예정
