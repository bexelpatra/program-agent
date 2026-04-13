# Coder Report — TASK-100

## 상태: DONE

## 태스크
- **Task ID**: TASK-100
- **Title**: 홉스 데이터 이슈 수정 (검증 결과 반영)

## 작업 내역

### 이슈 1 (보통): hobbes-claim-014 — "동일한 정당성" 표현 수정
- **인덱스/문서**: ethics-claims / hobbes-claim-014
- **필드**: claim
- **변경 전**: "...동일한 정당성을 가진다."
- **변경 후**: "...동일한 주권자 권리와 신민의 의무를 가진다."
- **근거**: 홉스 원문(Leviathan II.20)은 "same rights and consequences"이지 "same legitimacy"가 아님
- **결과**: updated (version 2)

### 이슈 2 (경미): hobbes-elements-of-law — significance 시기 표현 수정
- **인덱스/문서**: ethics-works / hobbes-elements-of-law
- **필드**: significance
- **변경 전**: "영국 내전 직전(1640년 장기의회 소집)에 왕당파 입장을 담아 작성"
- **변경 후**: "영국 내전 직전(1640년 단기의회·장기의회 소집 시기)에 왕당파 입장을 담아 작성·유통되었으며"
- **근거**: Elements of Law는 1640년 5월(단기의회 시기) 유통 시작. 장기의회는 11월 소집.
- **결과**: updated (version 2)

### 이슈 3 (경미): hobbes-claim-013 — argument (2b) 단순화 보완
- **인덱스/문서**: ethics-claims / hobbes-claim-013
- **필드**: argument
- **변경 전**: (2b) "인민이 부유해야 군주도 부유"
- **변경 후**: (2b) "군주의 부, 힘, 안전이 인민의 그것에 의존하므로 사적 이익과 공적 이익이 일치하는 경향이 있다"
- **근거**: 원문은 단순한 부의 관계가 아니라 부·힘·안전 전반의 의존 관계를 논증
- **결과**: updated (version 2)

### 이슈 4 (경미): thinker background — 수정 생략
- **사유**: 테스터가 "수정 불필요 (임용시험 맥락에서 과도한 상세)"로 판정. 참고사항으로만 기록.

## 검증 마킹

hobbes-claim-001 ~ hobbes-claim-014 (14건) 모두에 다음 필드 추가:
- `verified`: true
- `verification_log`: `{ task_id: "TASK-099", date: "2026-04-13", result: "정확", note: "..." }`
  - claim-013, claim-014: "수정 후 검증 완료 (TASK-100)"
  - 나머지 12건: "검증 완료 — 정확 (TASK-099)"

## 수정 후 조회 확인
- hobbes-claim-014: claim 필드에 "동일한 주권자 권리와 신민의 의무를 가진다" 확인
- hobbes-elements-of-law: significance에 "단기의회·장기의회 소집 시기" 확인
- hobbes-claim-013: argument (2b)에 "군주의 부, 힘, 안전이 인민의 그것에 의존" 확인

## 변경 없는 항목
- thinker (hobbes): 수정 없음
- works (hobbes-leviathan, hobbes-de-cive, hobbes-de-corpore, hobbes-de-homine): 수정 없음
- keywords (10건): 수정 없음
- relations (5건): 수정 없음
