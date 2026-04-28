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

---

## Phase 6 TASK-176 TOP10 MISS 회고 (2026-04-22)

- 작성: 2026-04-22 (TASK-176-10-FIX DONE 직후)
- 대상: TASK-176-01 ~ TASK-176-10-FIX (jinul·blasi·durkheim·hoffman·bandura·pettit·singer·turiel·moore·narvaez 10인 ES 등록)
- 진행 방식: Reviewer → Coder(Opus) → Tester 순차, bug 발견 시 Manager inline FIX

### 프로젝트 요약 (TOP10 부분 회고)

- **총 iteration**: 10회 (사상가 1인 = 1 iteration = Coder + Tester + 경우에 따라 FIX)
- **등록 총계**: thinker 10 + works ≥14 + claims ≥80 + keywords ≥90 + relations ≥30 (누계)
- **Bug 궤적**: jinul(0) · blasi(0) · durkheim(0) · hoffman(0) · bandura(0) · **pettit(3)** · **singer(1)** · turiel(0) · moore(0) · **narvaez(3)** — 모두 `severity=bug · Coder 영어 trademark 원문 0-hit`
- **Manager inline FIX**: 3회 (TASK-176-06-FIX pettit 4건 / TASK-176-07-FIX singer 1건 / TASK-176-10-FIX narvaez 6위치 3종)
- **DATA-QUALITY 기록**: TASK-DQ-001~005 누계 (특히 narvaez 는 DQ-005 3항목: canonical map BLK 누락 · 생년 1952 vs 1955 상충 · 영어 토큰 0-hit 다수)

### 잘 된 점

1. **3단 방어선의 안정적 작동**: 부정 키워드 safelist(Manager 스펙) + Coder 자기검증 루프(`grep -oE '\([A-Za-z][^)]*\)'`) + Manager/Tester 독립 재검증. turiel·moore 2연속 0 bug 는 3단 방어 성숙도의 증거.
2. **Manager 대필 프로토콜** (TASK-176-08 turiel, Coder rate limit 대응): Coder 스크립트 본문 무수정 유지 + Manager 가 실행·검증·coder-report.md frontmatter note 필드에 "대필 사유" 명시. 가용성 이슈에 대한 재현 가능 회복 절차 확립.
3. **Reviewer 선행 검증**: moore TASK-176-09 에서 Reviewer 1차 NEEDS_REVISION(4건 off-by-1 수치 오기) → Manager 재작성 → 2차 PASS. Coder 호출 전 스펙 품질 확보.
4. **Tester severity 규칙 100% 준수**: bug 판정된 TASK-176-06-T / -07-T / -10-T 전수 Manager inline FIX 태스크로 전환. 관찰(observation) 은 retrospective/DQ log 로 이월 — CLAUDE.md Step 4 규정과 일치.
5. **Bug 개선 궤적**: pettit(3) → singer(1) 로 66% 감소. Manager 스펙에 "부정 키워드 사전 리스트" + "pettit 교훈 재강조" 추가한 효과 확증 (TASK-176-07 done-log).

### 문제점

1. **narvaez 3 bug 재발** (핵심 문제): turiel·moore 2연속 0 bug 이후 직후 iteration 에서 bug 3건 재발. 개선 궤적이 정점에서 후퇴.
2. **Coder 자기검증 regex 한계**: 현행 `grep -oE '\([A-Za-z][^)]*\)' script.py` 는 **괄호 안 영어 토큰만** 캐치. narvaez 에서 놓친 패턴:
   - **JSON 필드 값**: `"term_en": "safety ethic"` (L852·L872 keyword 필드) — 괄호 구문 아님
   - **본문 괄호 밖 영어 phrase**: `(safety ethic)`·`(engagement ethic)` 이 coverage 에 한글 "안전 윤리"·"관여 윤리" 는 풍부하지만 영어 phrase 자체는 0 hit (Coder 가 괄호로 병기했어도 coverage 역grep 에 case-sensitive 0)
   - **대소문자 변이**: `moral foundations theory` (소문자 L1198) vs coverage 의 `Moral Foundations Theory` (TitleCase 5 hits). case-sensitive 표준 미준수
3. **Coder report 의 Step C "유지된 영어 토큰" 표가 오판**: narvaez coder-report L51 은 `engagement ethic=3` · `safety ethic=2` · `moral foundations theory=2` 로 기재했으나, Tester 실측은 0 hit. Coder 가 coverage md 가 아닌 **자신의 script 본문**에 역grep 했을 가능성 — 자기검증 대상 파일 혼동.
4. **Manager 대필 프로토콜 미명문화**: turiel 에서 전례만 존재. agents/coder.md / CLAUDE.md 에 "Coder rate limit 시 Manager 대필 절차" 미기재 → 재현 가능성 의존.

### 파이프라인 개선 제안 (TOP10 기준)

#### 제안 7: agents/coder.md 자기검증 2단계 규약 추가 (narvaez 대응)

- **대상 파일**: `agents/coder.md` (원문/입력 인용 규칙 섹션 L83-87 뒤)
- **현재**: L87 "새로 쓴 고유명·한자·trademark를 원문 파일에 역grep해 0건이면 제거·대체한다" — 일반론만. regex 패턴·대상 범위(괄호 내/외·JSON 필드) 미명시.
- **제안**: 2단계 자기검증 명문화:
  - Step 1: `grep -oE '\([A-Za-z][^)]*\)' script.py | sort -u` (괄호 안 토큰)
  - Step 2 (신규): 괄호 밖 TitleCase 영어 phrase + JSON 필드 값(`term_en` 등) 전수 추출
    - `grep -oE '"term_en"\s*:\s*"[^"]*"' script.py`
    - `grep -oE '[A-Z][a-z]+(\s+[A-Za-z][a-z]+){1,5}' script.py`
    - 각 토큰 coverage/*.md 역grep, **case-sensitive 엄수**
  - 0-hit 토큰은 제거·한글 단독·TitleCase 대체 중 택1
- **이유**: narvaez 3 bug 의 근본 원인은 Step 1 regex 만으로는 JSON 필드 값과 본문 괄호 밖 phrase 를 포착하지 못함. Step 2 추가 시 narvaez 3 bug 모두 저장 전 포착 가능.
- **상세 초안**: `signal/ethics-study/proposal-coder-md-amendment-TASK-176-10.md` 참조.

#### 제안 8: Manager 대필 프로토콜 명문화

- **대상 파일**: `agents/coder.md` 또는 `CLAUDE.md` (서브에이전트 호출 규칙 섹션)
- **현재**: turiel TASK-176-08 에서 Coder rate limit 발생 시 Manager 가 대필한 전례만 존재. 성문 규정 없음.
- **제안**: 대필 허용 조건·절차·note 필드 명시 형식을 표준화.
  - 조건: Coder(특정 모델) 호출 실패·rate limit·세션 만료
  - 절차: (a) Coder 스크립트 본문은 무수정 유지 (b) Manager 가 실행·자기검증·coder-report.md 작성 (c) frontmatter `note:` 필드에 "Manager 대필 (사유: ...)" 명시
  - Tester verdict 에 영향 없음 (본문 수정 없으므로)
- **이유**: 대필은 재현 가능한 회복 절차다. 명문화하지 않으면 다음 세션에서 혼란.

#### 제안 9: Coder report 의 "유지된 영어 토큰" 표 검증 대상 명시

- **대상 파일**: `agents/coder.md` 원문/입력 인용 규칙 섹션
- **현재**: narvaez coder-report L51 이 coverage 역grep 결과를 script 본문 grep 으로 오기재 가능성. "유지된 토큰" 표의 hit count 기준이 모호.
- **제안**: report 포맷에 "hit count 대상 = **coverage md 파일 전수 (case-sensitive)**" 를 명시하는 필드 주석 추가. Coder 가 자기 script 에 grep 하는 실수 방지.
- **이유**: narvaez 이후 혼동 재발 방지.

### 후속 과제 (TOP10 외부)

- **Phase 7 이후**: TOP10 외 Section D 잔여 사상가(green_th·viroli 등 부분 해소 BLK 대상) 추가 등록 검토.
- **DQ 배치 정정**: TASK-DQ-005 (narvaez canonical map BLK 누락 + 생년 상충 + 영어 토큰 0-hit) 일괄 반영.
- **agents/coder.md 수정 제안** (제안 7 근거 diff): `signal/ethics-study/proposal-coder-md-amendment-TASK-176-10.md` 초안 완료 — 사용자 승인 대기.

### 검토 요청

사용자에게 제안 7·8·9 적용 여부를 확인받는다. 특히 **제안 7** (Coder 자기검증 2단계) 은 narvaez 3 bug 재발의 직접 원인 차단책으로 우선 순위 높음. **사용자 승인 없이 `agents/coder.md` 는 수정하지 않는다** (CLAUDE.md Step 6).
