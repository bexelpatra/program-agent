# Coder Report — TASK-103

## 상태: DONE

## 태스크
- **Task ID**: TASK-103
- **Title**: 로크 데이터 이슈 수정 (검증 결과 반영)

## 수행 내용

### 이슈 1: claim-005와 claim-011 내용 중복 해소

**locke-claim-005 수정 완료:**

| 항목 | 수정 전 | 수정 후 |
|------|---------|---------|
| source_detail | Chapters 11-14, §134-168 | Chapters 11-14, §134, §143-148, §159-168 |
| original_text | §149 인용 (입법부는 수탁적 권력...) | §143 인용 (입법권과 집행권의 분리 근거) |
| claim | 입법권 최고 + 인민 신탁 제약 (claim-011과 중복) | 입법·집행·동맹권 분립, 대권(prerogative) 집중 |
| explanation | 입법권 우위 설명 포함 (중복) | 권력 분립의 구조적 근거에 집중 (§143, §148, §159-168) |
| argument | (3)번에서 입법권 최고 이유 설명 (중복) | 입법-집행 분리 필요성, 동맹권 배치, 대권 정당화로 재구성 |

**변경된 original_text (§143):**
> "The legislative and executive power come often to be separated... and because it may be too great a temptation to human frailty, apt to grasp at power, for the same persons, who have the power of making laws, to have also in their hands the power to execute them..."

**차별화 결과:**
- claim-005: 권력 분립론 (입법·집행·동맹권 구분, 분리의 근거 §143, 대권 §159-168)
- claim-011: 인민주권론 (인민 > 입법부 > 집행부 위계, 신탁 위반 시 권력 귀속, §149)

### verified 설정

- locke-claim-005: `verified: true` 설정 완료
- locke-claim-011: `verified: true` 설정 완료
- 양쪽 모두 `verification_log`에 TASK-103 기록 추가

### 이슈 2: relation-locke-american-founders의 to_thinker 참조 (인지 사항)

- `to_thinker: "jefferson"` — jefferson이 ethics-thinkers에 미존재하여 orphan reference 상태.
- Manager 지시에 따라 **수정하지 않음**. 제퍼슨은 임용시험 범위가 아니므로 향후에도 입력되지 않을 가능성이 높으나, 데이터 무결성에 즉각적 영향은 없음.
- 향후 프로젝트 전반 스키마 정비 시 일괄 처리 권장.

## 변경 파일
- `projects/ethics-study/scripts/fix_locke_claim005.py` (신규 생성 — 수정 스크립트)

## ES 변경 문서
- `ethics-claims/locke-claim-005`: source_detail, claim, original_text, original_text_ko, explanation, argument, verified, verification_log 업데이트
- `ethics-claims/locke-claim-011`: verified, verification_log 업데이트
