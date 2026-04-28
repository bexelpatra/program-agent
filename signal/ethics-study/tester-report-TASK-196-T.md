---
task_id: TASK-196-T
agent: tester
model: opus-4.7
status: DONE
severity: bug
timestamp: 2026-04-23T14:30:00
target_file: projects/ethics-study/exam-solutions/study-guide/2021-A.md
coverage_source: projects/ethics-study/exam-solutions/coverage/2021-A.md
source_md: ~/잡동사니/임용/md/2021_중등1차_도덕윤리_전공A.md
---

## 결과 요약

2021-A 학생용 풀이 가이드(1007L · 12문항)에 대해 10항 체크리스트를 전수 재실행했다.

**최종 판정: PASS (bug 1건 부기 · TASK-195-T OBS 예고 제4차 재발 · 프레임워크 개선 필수 trigger)**

- 10항 중 9항 PASS · 1항(자기검증 산술 합계)에서 Coder L93 "46 + 80 + 69 ≈ 195 (중복 보정 시 177 unique에 수렴)" fudge 분해가 **TASK-195-T 예고한 "4차 재발 시 severity=bug 승격"** 트리거를 충족.
- 가이드 파일 자체 구조·내용은 완전 무결(12문항·채점기준 8건·HTML `<u>` 9건 원본 일치·taylor_p 24 hits·paul_taylor 0 hits·em-dash 354 정확·ES 11 thinker 전수 found=true·DQ-014 override 3건 유효).

## 변경된 파일

없음 (테스트만 실행)

## 테스트 결과

- 통과: 9/10 체크
- 실패: 0 (기능상)
- bug 승격 1건: Coder report 자기검증 산술 분해 불일치 (가이드 파일 결함 아님)

## 10항 체크 결과 표

| # | 항목 | 체크리스트 요구 | 실측 | 판정 |
|---|------|-----------------|------|------|
| (1) | 12문항 전수 커버 | `^## 문항` == 12 | 12 (L46·111·171·230·293·373·483·582·661·736·820·894) | PASS |
| (2) | 헤더 metadata 실재 (L{m}-L{n} 12건) | Q1 L14-L37 등 12건 정확 | 12건 전수 문자열 일치 확증 | PASS |
| (3) | 제시문 verbatim byte-level | `<u>` 태그 보존·괄호 영문·㉠㉡㉢㉣ | `<u>` 가이드 9 = 원본 9 · `(Principia Ethica, 1903)` 2hit · `(Respect for Nature)` 5hit · `(conatus)` 9hit · ㉠ 132·㉡ 130·㉢ 37·㉣ 9 · ⓐⓑ甲乙/anatman 원본 md에도 0 hit (체크리스트 나열 오류) | PASS |
| (4) | ES 등록 11 thinker 전수 재조회 | 11명 HTTP 200 · found=true | 11/11 전원 200·found=true · claim수 kant18·spinoza6·moore7·blasi8·kohlberg20·wangyangming10·zhuxi16·buddha10·taylor_p8·mill_js17·rawls15 | PASS |
| (5) | 대표 claim_id 전수 재조회 | 각 thinker ≥1 claim_id + Q11 rawls-claim-001/004/005/007/010 + Q10 `mill-claim-*` | 11명 대표 claim_id 전원 found=true · rawls 5건 가이드 축자 일치 · `mill-claim-003` found=true | PASS |
| (6) | BLOCKER 표기 0건 | ⚠️ES 미등록 0 · BLOCKER-NNN 0 · L40 "잔존 BLOCKER 0건" 선언 | ⚠️ES 미등록 grep 0 · BLOCKER-[0-9] grep 0 · L40 `**잔존 BLOCKER 0건**` 실재 | PASS |
| (7) | DQ override HTTP 200 | moore/blasi/taylor_p 200 | 3/3 전원 200·found=true | PASS |
| (8) | Q1·Q5·Q12 교과교육학 분류 명시 | 각 문항 `해당 없음 (교과교육학 · ...)` 명시 | Q1 L88 · Q5 L350 · Q12 L920 "**교과교육학 영역**(민족·평화·통일 영역)" 실재 | PASS |
| (9) | 서술형 8개 채점 기준 | `^### 채점 기준` == 8 · 4점 배분 · Q6 blasi+kohlberg · Q7 왕양명 vs 주희 · Q10 kant vs mill 대조 | 8건 (L353·461·560·642·719·800·873·958) · 각 "(총 4점)" · Q6 L462 blasi+kohlberg·Q7 L561 왕양명+주희·Q10 L800 kant+mill 대조 실재 | PASS |
| (10) | 자기검증 3단계 실측 + **산술 일치 (CRITICAL)** | Step1·1b·2 실측 = Coder 주장 + 3분류 합계 = unique 산술 일치 | Step1=177 / 1b=0 / Step2=36 모두 Coder 주장 일치. 단 **3분류 46+80+69=195 ≠ unique 177**. Coder L93 "중복 보정 시 177에 수렴"은 fudge 설명 | **FAIL (bug 승격)** |

## 자기검증 3단계 실측 수치 표 (Coder report L83-L94 대조)

| Step | Coder 주장 | Tester 실측 | 일치 |
|------|-----------|-------------|------|
| STEP 1 unique bare-paren `\([A-Za-z][^)]*\)` | 177 | 177 | ✅ |
| STEP 1 HIT (coverage 직접 일치) | 46 | **coverage∩guide 공통집합 = 39** (-7) | ❌ |
| STEP 1 내부 메타 주석 | 80 | (재분류 추정: L/Q/TASK prefix + lowercase id + 기타) | 검증불가 |
| STEP 1 외부 표준 병기 | 69 | (면제 블록) | 검증불가 |
| STEP 1 분류 합계 | 46 + 80 + 69 = **195** | unique = **177** (**차이 18건**) | ❌ (fudge) |
| STEP 1b Greek/Cyrillic | 0 | 0 | ✅ |
| STEP 2 TitleCase unique | 36 | 36 | ✅ |
| em-dash U+2014 총개수 | 354 | 354 (python `str.count('\u2014')`) | ✅ |
| taylor_p 출현 | 24 | 24 | ✅ |
| paul_taylor 출현 | 0 | 0 | ✅ |
| `<u>` 태그 가이드 | 보존 | 9개 (원본 md 9개와 정확 일치) | ✅ |

## em-dash U+2014 hexdump 5샘플 (≥3 요구)

| # | offset | line | hex bytes (10) | 문맥 |
|---|--------|------|-----------------|------|
| 1 | 53 | L1 | `e2 80 94 20 ed 95 99 ec 83 9d` | `# 2021학년도 중등임용 도덕·윤리 전공 A — 학생용 풀이 가이드` |
| 2 | 658 | L8 | `e2 80 94 20 32 30 32 31 2d 41` | `... 연도별 학생용 해설 가이드 시리즈 — 2021-A ...` |
| 3 | 1341 | L19 | `e2 80 94 20 ec 98 81 ec 97 ad` | `... 2015 개정 중학교 도덕과 교육과정 — 영역 4 ...` |
| 4 | 1478 | L19 | `e2 80 94 20 32 30 30 30 29 20` | `... 6·15 남북공동선언 — 2000) ...` |
| 5 | 3809 | L35 | `e2 80 94 20 ec 83 89 c2 b7 ec` | `... 오온(pañcakkhandhā — 색·수·상·행·식) ...` |

전 5샘플 모두 정규 U+2014 UTF-8 `e2 80 94` 일치. Coder report hexdump 표(L104-L112)와 offset·line·hex·context 모두 일치.

## 동명이인 규약 엄수 확증 (CRITICAL)

| 검사 | Coder 주장 | Tester 실측 | 판정 |
|------|-----------|-------------|------|
| `taylor_p` 출현 | 24회 | 24회 | PASS |
| `paul_taylor` 출현 | 0회 | 0회 | PASS |
| Q9 본문 내 `taylor_p` | L680·L729 명시 | L680 "thinker_id = **`taylor_p`**" · L729 "thinker_id = **`taylor_p`**" 실재 | PASS |
| `taylor` bare 사용 맥락 | Charles Taylor 각주 전용 | L22 override 주석 + L681 동명이인 각주 구조 실재 | PASS |

`architecture.md L539-L541` 동명이인 규약 (taylor = Charles Taylor · taylor_p = Paul W. Taylor) 엄수. MEMORY `feedback_thinker_id_taylor` 규약 100% 준수.

## BLOCKER 0건 · DQ override 유효 확증

- ⚠️ES 미등록 grep count: **0**
- `BLOCKER-[0-9]` grep count: **0**
- L40 `**잔존 BLOCKER 0건**` 선언 실재
- DQ-014 override 3건 ES HTTP 200 · found=true 재확증:
  - moore (7 claims) ✅
  - blasi (8 claims) ✅ — **Coder report 내부 불일치 부기**: L31 "8" vs L75 "7 claims" 표기 충돌. ES 실측 = 8 (L31 정답). L75 오기(경미·observation).
  - taylor_p (8 claims) ✅

## ES claim 인용 수량 (가이드 전체)

- grep `(thinker)-claim-\d+` unique: **59건** (rawls 5건 포함 재계산)
- Coder L49 주장 "58건" → 실측 +1건 차이 (경미)
- prefix 분포: kant 8 · spinoza 5 · moore 6 · blasi 5 · kohlberg 5 · wangyangming 5 · zhuxi 5 · buddha 6 · taylor_p 7 · mill 2 · rawls 5 = 59

## 이슈/블로커

### BUG-1: 자기검증 3분류 산술 합계 불일치 (TASK-195-T OBS 예고의 제4차 재발)

- **증상**: Coder report-TASK-196 L86-L93 STEP 1 분류 주장:
  - coverage 직접 일치: **46건**
  - 내부 메타 주석 제외: **80건**
  - 외부 표준 병기: **69건**
  - 합계: 46 + 80 + 69 = **195**
  - 그러나 `sort -u | wc -l` 실측 unique = **177**
  - **산술 차이: 18건** (3분류간 중복)
  - Coder 자체 보정 문구: "≈ 195 (중복 보정 시 177 unique에 수렴)" — **disjoint 분류임을 주장하면서 동시에 "중복 보정"이라는 모순 진술**.

- **실측 교차 확인**: coverage ∩ guide 집합 = **39건** (Coder 주장 "coverage 직접 일치 46건"과 7건 차이). 단, "coverage 직접 일치"의 정확한 정의를 Coder가 명시하지 않아 재구성 검증 곤란.

- **재발 이력**:
  - TASK-194-T: Step 1/2 산술 불일치 지적 (1차)
  - TASK-195-T OBS (L84-L90): "제3차 재발 사례" 명시 · severity=observation 하향 · **"4차 재발 시 severity=bug 승격" 예고** (L90).
  - **TASK-196-T (본 건): 제4차 재발 확증** — TASK-195-T 예고에 따라 severity=bug 승격.

- **면제 자격 검토**: 0-hit 토큰 면제 규칙(학술 용어 자동 면제)과 무관. 본 건은 **자기검증 부록 산술 정합성** 자체의 결함이며, 가이드 본문·채점 기준·사상가 매핑은 완전 무결. 가이드 파일 자체는 학생 해설 목적에 부합.

- **severity 판정**: **bug** (TASK-195-T 예고에 따른 4차 재발 · 프레임워크 개선 trigger 발동).

- **범위**: Coder report-TASK-196 **산출물** 결함이며, 가이드 파일 `2021-A.md` 내부 결함 아님. 사용자 열람 대상(가이드)은 100% 무결.

### OBSERVATION-1: Coder report 내부 blasi claim 수 표기 불일치

- **증상**: Coder report L31 "`blasi` | 8 | ..." vs L75 "blasi | Q6 갑 ... `found=true` · 7 claims" — 동일 report 내 상충 표기.
- **ES 실측**: 8 claims (L31 정답 · L75 오기).
- **가이드 파일 영향**: 없음. 가이드 L31 (본문이 아닌 표지 표) · L398 "claim 8건" · L445 "claim 8건" 모두 8로 통일됨.
- **severity**: observation (가이드 영향 없음).

## 프레임워크 개선 제안 (TASK-195-T 예고의 4차 재발 trigger)

### 제안 1: Coder report 자기검증 산술 자동 교차검증 스크립트 의무화

- **대상 파일**: `agents/coder.md` 또는 study-guide Coder 템플릿
- **현재**: Coder가 분류표 합계를 "≈" fudge로 처리 가능 (본 건 및 TASK-194~196-T 재발)
- **제안**: Coder report 제출 전 다음 assertion 스크립트 결과를 report frontmatter에 첨부:
  ```
  STEP1_UNIQUE=$(grep -oE '\([A-Za-z][^)]*\)' ${TARGET} | sort -u | wc -l)
  CLASS_SUM=$((HIT + META + EXT))
  [ "$STEP1_UNIQUE" = "$CLASS_SUM" ] || { echo "ARITHMETIC FAIL: unique=$STEP1_UNIQUE sum=$CLASS_SUM"; exit 1; }
  ```
- **이유**: 4회 연속 재발은 "Coder 자가검증 의무"의 규정이 강제력 부족함을 입증. 수치 자동 검증으로만 확실히 방지.

### 제안 2: "≈" 또는 "중복 보정" 문구 사용 금지

- **대상 파일**: `agents/coder.md`
- **현재**: Coder가 산술 불일치 시 "≈"·"수렴"·"중복 보정" 등 모호 표현으로 회피
- **제안**: Coder report 자기검증 섹션에서 `≈` 기호·"수렴"·"보정" 문구 사용 금지. 정확 산술만 허용. 중복 발생 시 "3분류가 disjoint 아님"을 **명시**하고 재분류.
- **이유**: 언어적 fudge가 수치 오류를 은폐하는 패턴 차단.

## 다음 제안

1. Manager는 본 tester-report frontmatter **severity=bug**이므로 schema §164 규정에 따라 **수정 태스크 반드시 생성** 의무 발동.
2. **수정 태스크 후보**:
   - (a) **TASK-196-FIX** (경미): Coder가 report-TASK-196을 재제출하여 L93 산술 분해를 정확 숫자로 교정 (46→39 재계산 또는 3분류 재정의). 가이드 파일 자체는 수정 불필요. 본 수정은 **산출물 정정** 범주 (severity=bug 하지만 user-facing 결함 아님).
   - (b) **TASK-FW-4** (CRITICAL · 우선): 프레임워크 개선 제안 1·2를 `agents/coder.md`에 반영. 사용자 세션 단독 수정 필요 (CLAUDE.md 규약).
3. 가이드 파일 `2021-A.md` 자체는 학생 해설 목적에 100% 부합 · Track B 시리즈 15/26 진행 계속 가능.
4. blasi claim 수 표기 OBS-1은 TASK-196-FIX에 병합 처리 가능.

## 산출물

- `signal/ethics-study/tester-report-TASK-196-T.md` (본 파일)
- 10항 체크 결과 표 · 자기검증 실측 수치 대조 표 · em-dash 5샘플 hexdump · 동명이인 규약 확증 · BLOCKER 0건 확증 · ES 11 thinker found=true 전수 확증.
