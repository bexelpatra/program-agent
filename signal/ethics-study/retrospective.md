# Phase 6 Retrospective — 임용 도덕·윤리 기출 커버리지 재구축

- 작성: 2026-04-22
- 대상: Phase 6 전체 (TASK-175E-2014-A ~ TASK-175E-MERGE-FIX)

## 프로젝트 요약

- **목표**: 2014~2026 (26개 연도×과목) 임용 도덕·윤리 기출 원문을 직독·3단계 확정 규약으로 전수 커버리지화하고, 55명 canonical 사상가 대비 HIT/MISS 집계 맵을 생성.
- **총 태스크**: 59개 (coverage 26 + Tester 검증 26 + FIX 4 + MERGE/MERGE-T/MERGE-FIX 3)
- **재시도(NEEDS_REVISION) 발생**: 5건 (2021-A-T, 2024-B-T, 2025-A-T, 2025-B-T, MERGE-T)
- **첫 시도 PASS**: 54/59 (91.5%)
- **Blocker 발행**: 93건 (철회 1, net active 92)
- **세션 수**: 다수(wakeup 기반 /loop 자율 진행, 약 24시간)
- **최종 산출**:
  - `projects/ethics-study/exam-solutions/coverage/{YYYY-[AB]}.md` × 26
  - `projects/ethics-study/exam-solutions/exam-coverage-map.md` (Section A~E 통합맵)
  - `projects/ethics-study/scripts/merge_coverage.py` (2-path 파서 자동 병합 스크립트)
  - `signal/ethics-study/blocker-log.md` 누적 93 entries

## 잘 된 점

1. **Reviewer→Coder(Opus)→Tester 3단 파이프라인**이 26개 연도 반복에서 안정적으로 동작했다. Reviewer 단계에서 Manager 산출물(특히 task-board 스펙)의 오류를 사전 차단한 사례가 다수(2025-B 발문 범위, MERGE 스펙 8항 누락, MERGE-T Section C 행수 오기, MERGE-FIX 수정 지점 범위 오기).
2. **재출제 연속성 grep 실증 규칙**(TASK-175E-2024-B-FIX에서 확립)이 이후 2025-B/2026-A/2026-B에 일관 적용되어 근거 없는 "N연속" 기록을 방지했다. bandura 3연속(2024-B→2025-B→2026-B, 임용 도덕심리 최장기록), jinul 2연속 등이 grep 검증 기반으로 확증되었다.
3. **thinker_id 동명이인 suffix 규약** (architecture.md:491)이 2021-A-FIX에서 확립된 이후 모든 후속 태스크(2021-B~2026-B, MERGE)에서 taylor/taylor_p 엄격 분리 유지. Section B #45 Charles Taylor + Section A #17 Paul Taylor.
4. **ES dump gold standard** (`size=100&_source=id,name_en` + cross-reference)이 TASK-175E-2024-A부터 확립되어 이후 모든 -T 태스크에서 HIT/MISS 기계 대조의 정확도를 보장했다.
5. **MERGE 스크립트**의 2-path 파서와 column-offset auto-correction, unescaped pipe 복구 fallback이 26개 서로 다른 포맷의 md 파일을 무인 자동화로 병합하는 데 성공.
6. **bug 재발견 및 즉시 FIX 태스크화**: Tester severity=bug 판정 시 Manager가 지체 없이 FIX 태스크를 등록(2021-A-FIX / 2024-B-FIX / 2025-A-FIX / 2025-B-FIX / MERGE-FIX). 100% 회수율.

## 문제점

1. **Manager의 task-board 스펙 오기**가 Reviewer NEEDS_REVISION으로 여러 번 돌려받음 (MERGE v1 스펙 8항 누락, MERGE-T Section C 65→61 오기, MERGE-FIX bare-id 경로 누락). Manager가 스펙을 작성할 때 **실측 grep/Read를 먼저 수행하지 않아서** 나중에 Reviewer가 발견해야 했다.
2. **2025-B BUG-2 (trademark 7개 grep 0건)**: Coder(Opus)가 제시문에 실재하지 않는 한자 고유명(心卽理·氣發理乘一途 등)을 "이 사상가라면 쓰는 개념"으로 자동 보강. Phase 6 L544·L580-582 금지 조항 위반. Reviewer 스펙 검증만으로는 Coder의 창작 보강을 막지 못함.
3. **2025-A `rest` MISS 오분류**: Coder가 ES 실조회 없이 "rest는 사상가명 같지 않아서 MISS"로 판단. ES에 10 claims 실재. Tester grep+ES 실측으로만 발견.
4. **재출제 연속성 기록 오류 (2024-B 15개 지점)**: Coder가 모의 기억으로 "N연속" 기록. 이후 2024-B-FIX에서 grep 실증으로 전수 재작성.
5. **unescaped `|` 3건 (2020-B Q11, 2021-A Q5, 2022-A Q10)**: 구형 coverage md 파일의 파싱 취약점. MERGE 스크립트가 row-level fallback으로 thinker_id만 복구했으나, Section C 원문 셀 표시는 부정확. 원본 수정 금지 규정 때문에 미해결.
6. **dedupe 누락 (MERGE bug-1)**: extract_thinker_ids() 함수가 셀 내 중복 매칭(`sandel` 4×)을 4회로 집계하여 Section B 출제횟수 inflate. 단위 테스트 부재로 Coder 자체 검증에서 누락.

## 파이프라인 개선 제안

### 제안 1: Manager 스펙 작성 전 grep 실측 단계 의무화
- **대상 파일**: `CLAUDE.md` Step 2 (태스크 분해)
- **현재**: 태스크 분해 시 Manager가 architecture.md와 기억에 의존해 스펙을 작성. Reviewer가 사후 실측으로 오기를 찾아냄.
- **제안**: Step 2에 "**태스크 description에 구체 수치/경로/라인 번호를 적기 전, 반드시 grep/ls/Read로 실측한 결과를 인용**"을 명시. 예) "Section C 행 수 == 61" 같은 assertion은 반드시 Manager가 Read로 L139를 눈으로 확인한 뒤 기재.
- **이유**: Reviewer NEEDS_REVISION의 3/5가 Manager 실측 누락이 원인. Reviewer 단계의 목적은 Coder 호출 전 현실 대조인데, Manager가 먼저 대조하면 Reviewer는 순수 스펙 품질(완결성·검증 가능성)에 집중할 수 있다.

### 제안 2: Coder(Opus) 프롬프트에 "원문 grep 실증 없는 보강 금지" 강조문 추가
- **대상 파일**: `agents/coder.md`
- **현재**: Phase 6 규약은 `signal/ethics-study/architecture.md` Phase 6 L544·L580-582에 있음. Coder 프롬프트에는 일반론만.
- **제안**: agents/coder.md에 "**사용자 제시 원문에 grep 0건인 trademark/개념어/한자는 절대 쓰지 말고 원문 구절 그대로 인용한다**"를 일반 규정으로 승격. 프로젝트별 Phase 규정은 별도 참조.
- **이유**: 2025-B BUG-2 같은 "그럴듯한 자동 보강"은 Opus 모델의 강한 생성 편향에서 비롯된다. 일반 규정으로 상향 고지가 필요.

### 제안 3: Tester에게 `grep 0건 trademark 스캔` 자동화 체크 추가
- **대상 파일**: `agents/tester.md`
- **현재**: severity 부여 규칙만 명시. 구체적 검증 체크리스트는 태스크별 Manager 스펙에 의존.
- **제안**: Tester 표준 절차에 "**Coder 산출물에서 백틱/굵은글씨로 표시된 trademark/개념어/한자 고유명을 모두 추출해 원문(coverage 입력 md)에 grep 하여 0건인 것은 자동으로 bug로 분류**" 체크를 추가.
- **이유**: 2025-B에서 Tester가 이 체크를 수동으로 했기에 발견. 표준 체크로 승격하면 향후 자동 방어.

### 제안 4: MERGE-style 자동 집계 스크립트에 단위 테스트 의무
- **대상 파일**: `projects/ethics-study/scripts/`, `agents/coder.md`
- **현재**: merge_coverage.py 같은 자동화 스크립트가 단위 테스트 없이 작성됨. MERGE-FIX의 dedupe 누락도 단위 테스트 부재로 놓침.
- **제안**: Coder가 집계·병합 성격의 스크립트를 작성할 때 **pytest 기반 단위 테스트 3~5개 동봉**(동일 셀 중복 dedupe / 서로 다른 row 중복 유지 / 빈 입력 / malformed row). Manager 태스크 스펙에도 "테스트 동봉 요구" 명시.
- **이유**: MERGE-FIX 같은 one-line 버그는 Tester가 있어서 발견됐지만, 회귀 방지를 위한 단위 테스트가 없으면 스크립트 재수정 시 또 발생.

### 제안 5: unescaped `|` 같은 원문 md 품질 이슈를 별도 `DATA-QUALITY` 태스크로 분리
- **대상 파일**: `CLAUDE.md` Step 4 결과 판단 섹션
- **현재**: 원문 수정 금지 규정 때문에 coverage/*.md의 unescaped `|` 3건이 미해결 observation으로 남음.
- **제안**: observation 중 "**원본 데이터 품질 이슈**"는 별도 `DATA-QUALITY-*` 태스크 유형으로 분리. 즉시 처리는 아니지만 전용 로그(`signal/ethics-study/data-quality-log.md`)에 적재해 향후 배치 정정 가능하게 함.
- **이유**: 현재는 Coder observation에 파묻혀 사라질 위험. 3건이 Section C 표시 부정확의 주된 원인.

### 제안 6: /loop 자율 모드에서 ScheduleWakeup prompt는 verbatim 원형을 유지
- **대상 파일**: 사용자 운영 가이드(개선 제안 기록만)
- **현재**: /loop 원 프롬프트를 매 wakeup에 verbatim 전달. 다음 할 일 힌트를 괄호로 덧붙이는 패턴 시도.
- **제안**: 덧붙인 힌트가 때로 사용자 의도와 다를 수 있으므로, **원 프롬프트 복원 + 직전 done-log 마커를 참조**하는 패턴이 더 안정적. 이 retrospective 작성 후 /loop 종료가 자연스럽다(모든 Phase 6 태스크 DONE).
- **이유**: 이번 세션의 마지막 ScheduleWakeup에 "다음 할 일: retrospective"라고 힌트를 넣었는데, 이 힌트가 없으면 다음 세션이 혼란스러웠을 것.

## 후속 과제 (Phase 6 외부)

- **TASK-176**: Section D TOP10 순서(jinul→blasi→durkheim→hoffman→bandura→pettit→singer→turiel→moore→narvaez)로 ethics-thinkers 인덱스에 10인 신규 등록. 첫 세션에서 각각 사상 요지·claims 3~5건 준비.
- **DATA-QUALITY 배치 정정**: 2020-B Q11 / 2021-A Q5 / 2022-A Q10 unescaped `|` 3곳을 `\|`로 치환해 MERGE Section C 표시 완결.
- **merge_coverage.py 단위 테스트**: dedupe / 중복 row / 빈 입력 / malformed row 최소 4케이스.

## 검토 요청

Manager(사용자)에게 위 6건의 파이프라인 개선 제안 중 적용할 항목을 선택받아 순차 반영한다. **사용자 승인 없이 프레임워크 파일을 수정하지 않는다** (CLAUDE.md Step 6 규정).
