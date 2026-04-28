---
agent: coder
task_id: TASK-185-FIX
status: DONE
timestamp: 2026-04-22T00:00:00
---

## 결과 요약

TASK-185-T (severity=bug) 지적 2건 수정 완료. `/home/jai/program-agent/projects/ethics-study/exam-solutions/study-guide/2015-B.md` 의 L92·L94 bare-paren 영어 토큰을 coverage 원문(`~/program-agent/projects/ethics-study/exam-solutions/coverage/2015-B.md` L15)과 일치하는 `한자(漢字) — 영어` 완전 래퍼로 교정. em-dash는 U+2014 (`—`) 를 coverage 원문에서 그대로 복사. 주변 한글 맥락 및 나머지 본문 byte-level 불변.

## 변경된 파일

- `projects/ethics-study/exam-solutions/study-guide/2015-B.md` (수정, 2 라인)

### 편집 전/후 diff

**L92**:
- 전: `4구성 요소 모델에서 도덕적 동기(moral motivation)는 "다양한 가치가…`
- 후: `4구성 요소 모델에서 도덕적 동기(道德的 動機 — moral motivation)는 "다양한 가치가…`

**L94**:
- 전: `**도덕적 실행력(moral character / implementation)의 훈련 영역** 정리…`
- 후: `**도덕적 실행력(道德的 實行力 — moral character / implementation)의 훈련 영역** 정리…`

## 자기검증 루프 결과

| 검증 항목 | 명령 | 대상 파일 | 기대 | 실측 |
|-----------|------|-----------|------|------|
| Step 1 bare-paren 잔존 (수정 후 bare 형식 소거 확증) | `grep -Fc '(moral motivation)'` | study-guide/2015-B.md | 0 | **0** |
| Step 1 bare-paren 잔존 | `grep -Fc '(moral character / implementation)'` | study-guide/2015-B.md | 0 | **0** |
| Step 2 coverage 역grep (원문 존재 확증) | `LC_ALL=C.UTF-8 grep -Fc '(道德的 動機 — moral motivation)'` | coverage/2015-B.md | ≥1 | **1** (L15) |
| Step 2 coverage 역grep | `LC_ALL=C.UTF-8 grep -Fc '(道德的 實行力 — moral character / implementation)'` | coverage/2015-B.md | ≥1 | **1** (L15) |
| Step 3 새 토큰 삽입 확증 | `LC_ALL=C.UTF-8 grep -Fc '(道德的 動機 — moral motivation)'` | study-guide/2015-B.md | ≥1 | **1** (L92) |
| Step 3 새 토큰 삽입 확증 | `LC_ALL=C.UTF-8 grep -Fc '(道德的 實行力 — moral character / implementation)'` | study-guide/2015-B.md | ≥1 | **1** (L94) |

모든 토큰은 case-sensitive `grep -F` + `LC_ALL=C.UTF-8` 로 검증. em-dash 문자는 U+2014 (coverage L15 verbatim 복사).

## git diff 범위 보고

`projects/ethics-study/exam-solutions/study-guide/2015-B.md` 는 현재 git 미추적(Untracked) 상태이므로 `git diff` 출력은 빈 값. 파일 시스템 상의 실질 변경 범위는 L92 단일 라인 + L94 단일 라인의 각 1 토큰 치환으로, 나머지 본문 및 주변 한글 맥락은 byte-level 불변(Edit tool 의 정확 문자열 매칭 기반). 완료 조건 4(2 line 이내) 충족.

## 이슈/블로커

없음.

## 다음 제안

Tester 재검증(TASK-185-T re-run) 으로 이전 FAIL 근거(bare-paren 2건)가 해소되었는지 확증 권장. 동일 유형 재발 방지를 위해 coder.md L89-L115 자기검증 2단계 프로토콜을 향후 2015-B 인접 기출(예: 2015-A, 2016-*) 의 `풀이 과정` 섹션에도 적용해 coverage 역grep 누락이 없는지 일괄 확증하는 것이 바람직.
