---
task_id: TASK-185
verdict: NEEDS_REVISION
items_checked: 10
items_passed: 7
items_failed: 3
round: 1
---

# Reviewer Report: TASK-185 + TASK-DQ-007

## 검증 대상

- 파일: `signal/ethics-study/task-board.md` (TASK-185, TASK-DQ-007 행)
- 참조: `projects/ethics-study/exam-solutions/coverage/2015-B.md`
- ES: `http://localhost:9200/ethics-thinkers`, `http://localhost:9200/ethics-claims`
- Manager 주장 요약:
  1. coverage/2015-B.md = 206 lines, 6문항, 40점
  2. 문항별 원문 line 범위: L14-L31 / L35-L41 / L45-L51 / L55-L67 / L75-L81 / L89-L91
  3. singer: ES found=true, 8 claims / durkheim: ES found=true, 8 claims
  4. rest=10, mencius=17, zhuangzi=10, aquinas=10, mill_js=17, piaget=14, kohlberg=20, yihwang=12, yiyulgok=12
  5. NOTE-BLOCKER-1 coverage L26-L28 실재
  6. TASK-DQ-007: L32-L36 "ES 누락" 목록이 singer·durkheim을 잘못 기재 → override 필요
  7. Greek/Cyrillic regex `[α-ωΑ-Ωа-яА-Я]` 명시 (TASK-184-FIX 교훈 반영)
  8. 분량 상한 1200 lines (Reviewer 호출 시 reference: "2014-A 20문항=약 2700 lines, 2014-B 4문항=309 lines, 2015-A 14문항=674 lines")

---

## 검증 결과

### 1. 파일 존재

| 경로 | 존재 | 비고 |
|------|------|------|
| `projects/ethics-study/exam-solutions/coverage/2015-B.md` | ✅ | 206 lines 확인 |
| `projects/ethics-study/exam-solutions/study-guide/` | ✅ | 디렉토리 실재 (2014-A/B, 2015-A 선례) |
| `projects/ethics-study/exam-solutions/study-guide/2015-B.md` | ✅ 없음 = 정상 | 신규 생성 대상 — 부재가 정확한 상태 |
| `signal/ethics-study/data-quality-log.md` | ✅ | TASK-DQ-006까지 적재 확인 |

### 2. 내용 일치

#### 2-A. coverage 파일 기본 메타데이터 — PASS

| Manager 주장 | 실측 | 판정 |
|---|---|---|
| 206 lines | `wc -l` = 206 | ✅ |
| 6문항 (서술형 1~4 + 논술형 1~2) | coverage 표 6행 + 분류 합계 "6 ✓" | ✅ |
| 40점 (서술형 5점×4 + 논술형 10점×2) | coverage L189 "40점 ✓" | ✅ |

#### 2-B. 원문 line 범위 — PASS

coverage 표 마지막 컬럼(L15~L20)과 소스 파일 실측 전수 일치:

| 문항 | Manager 주장 | coverage 표 실측 | 소스 파일 경계 확인 |
|---|---|---|---|
| 서술형 1 | L14-L31 | L14-L31 | L14="## 서술형 【1 ~ 4】", L31=㉡ blank line ✅ |
| 서술형 2 | L35-L41 | L35-L41 | L35="### 2. [5점]", L41=(나) 안회 제시문 끝 ✅ |
| 서술형 3 | L45-L51 | L45-L51 | L45="### 3. [5점]", L51=을 제시문 끝 ✅ |
| 서술형 4 | L55-L67 | L55-L67 | L55="### 4. [5점]", L67=②통설 문장 끝 ✅ |
| 논술형 1 | L75-L81 | L75-L81 | L75=발문 시작, L81=병 제시문 끝 ✅ |
| 논술형 2 | L89-L91 | L89-L91 | L89=갑 <u>㉠인심</u> 시작, L91=을 제시문 시작 ✅ |

#### 2-C. ES claim 수 — PASS

`ethics-claims` 인덱스 aggregation 실측 (2026-04-22 본 세션 curl):

| thinker_id | Manager 주장 | 실측 | 판정 |
|---|---|---|---|
| singer | 8 | 8 | ✅ |
| durkheim | 8 | 8 | ✅ |
| rest | 10 | 10 | ✅ |
| mencius | 17 | 17 | ✅ |
| zhuangzi | 10 | 10 | ✅ |
| aquinas | 10 | 10 | ✅ |
| mill_js | 17 | 17 | ✅ |
| piaget | 14 | 14 | ✅ |
| kohlberg | 20 | 20 | ✅ |
| yihwang | 12 | 12 | ✅ |
| yiyulgok | 12 | 12 | ✅ |

`ethics-thinkers/_doc/singer` → `found: true` (thinker 문서 존재, claims는 별도 인덱스에 8건)
`ethics-thinkers/_doc/durkheim` → `found: true` (동일)

#### 2-D. TASK-DQ-007 포착 정확성 — PASS (단, 부수 지적 있음)

coverage L32-L33 ("ES에 Peter Singer 사상가 자체가 등록되지 않음(claim 0건)", "ES에 Émile Durkheim 사상가 자체가 등록되지 않음(claim 0건)")이 실재하며, 실제 현 상태(singer=8 claims, durkheim=8 claims)와 불일치함을 TASK-DQ-007이 정확히 포착함. TASK-185 override 지시("✅ES 등록 8 claims")도 실측과 일치.

#### 2-E. NOTE-BLOCKER-1 — PASS

coverage L26: `### NOTE-BLOCKER-1 — 논술형 2 갑 퇴계 판정의 출전 편 미확정` 실재.
coverage L28: `<!-- BLOCKER(TASK-175E-2015-B): ... -->` HTML 주석 실재.
TASK-185에 "coverage NOTE-BLOCKER-1 (논술형 2 퇴계 출전 미확정): coverage L26-L28 에 'NOTE-BLOCKER' 로 기재 — Coder 는 study-guide 에 `⚠️출전 미확정 (판정 가능 범위)` 주석 삽입 (BLK 정식 등록 불요)" 지시 — 내용·형식 일치 ✅.

#### 2-F. Greek/Cyrillic regex 정확성 — PASS (단, 주의사항 있음)

`[α-ωΑ-Ωа-яА-Я]` 분석:
- `α`=U+03B1, `ω`=U+03C9 → 기본 Greek 소문자(U+03B1-03C9) 포괄 ✅
- `Α`=U+0391, `Ω`=U+03A9 → 기본 Greek 대문자(U+0391-03A9) 포괄 ✅
- `а`=U+0430, `я`=U+044F → Cyrillic 소문자 포괄 ✅
- `А`=U+0410, `Я`=U+042F → Cyrillic 대문자 포괄 ✅
- **Greek Extended (U+1F00-U+1FFF)**: U+1F00 > U+03C9이므로 범위 밖 → 미포괄

그러나 2015-B 소스 파일(`2015중등1차-도덕윤리_전공B.md`)에 Greek Extended 문자 0건 실측. 또한 2015-B coverage/2015-B.md에도 Greek Extended 0건. TASK-184-FIX에서 문제가 된 Greek 문자(`γενναῖον`, `μετὰ`, `λόγος`)는 모두 기본 Greek(U+03B1-03C9 범위) — Greek Extended가 아님. 따라서 현실적 위험도는 낮으나 regex 정의 자체의 한계(Greek Extended 미포괄)는 엄밀하게 지적 가능. TASK-184-T-R2가 "U+1F00-1FFF" 범위도 Greek 0건으로 확인한 선례가 있어, 실제 위험은 없음.

---

### 3. NEEDS_REVISION 근거 — 3항목

#### [R-1] ❌ TASK-DQ-007이 data-quality-log.md에 미등록 (BLOCKER CLAUDE.md §Step 4 위반)

**Manager 주장**: "TASK-DQ-007 | ... | manager | DONE (로그 기록만)"

**실측**: `signal/ethics-study/data-quality-log.md`의 마지막 항목은 `TASK-DQ-006`(2026-04-22T14:55). TASK-DQ-007 항목 **0건**.

CLAUDE.md §Step 4 "원본 데이터 품질 이슈 분리 (DATA-QUALITY)" 조항: "data-quality-log.md (append-only)에 적재한다." task-board에는 "DONE (로그 기록만)"이라 명시되어 있음에도 실제 로그 미작성.

**수정 요구**: Manager는 Coder 호출 전에 `signal/ethics-study/data-quality-log.md`에 TASK-DQ-007 항목을 append해야 한다.

---

#### [R-2] ❌ Reviewer 호출 프롬프트의 분량 reference 수치 오류 (실측 기준 요건 위반)

**Manager 주장 (Reviewer 호출 시)**: "TASK-182 2014-A 20문항=약 2700 lines, TASK-183 2014-B 4문항=309 lines, TASK-184 2015-A 14문항=674 lines 실측 기준"

**실측**:
- `projects/ethics-study/exam-solutions/study-guide/2014-A.md`: **655 lines** (20문항) — Manager 주장 "약 2700"과 대비 약 4배 과대
- `projects/ethics-study/exam-solutions/study-guide/2014-B.md`: 309 lines (4문항) ✅
- `projects/ethics-study/exam-solutions/study-guide/2015-A.md`: 674 lines (14문항) ✅

2014-A study-guide가 655 lines인 반면 Manager는 "약 2700 lines"를 Reviewer 호출 프롬프트에 명시했다. 이 수치는 CLAUDE.md §Step 2 "실측 인용 의무" 조항 위반이다.

이 오류는 Reviewer 호출 프롬프트에만 나타나며 **task-board의 TASK-185 행 본문에는 "2700"이 없다**. TASK-185 행 자체에는 "파일 1200 lines 이내 (6문항 × 약 150~200 lines)"만 기재되어 있어 task-board 자체는 영향 없음.

실제 단위 측정값:
- 2014-A: 655/20 = 32.75 lines/Q
- 2014-B: 309/4 = 77.25 lines/Q
- 2015-A: 674/14 = 48.1 lines/Q
- 6문항 추정(실측 기반): ~197~463 lines

TASK-185 행의 "파일 1200 lines 이내" 상한 자체는 보수적 상한으로 허용 가능. 그러나 Reviewer 프롬프트에 사용된 "약 2700 lines"는 비실측값이며 이후 에이전트 호출 프롬프트에도 이 수치가 전달될 경우 혼란을 유발할 수 있다.

**수정 요구**: Reviewer 호출 프롬프트 및 향후 Coder 호출 프롬프트의 reference 수치를 실측값(2014-A=655, 2014-B=309, 2015-A=674)으로 정정할 것.

---

#### [R-3] ⚠️ TASK-185 완료 조건 항목 (5)의 표현 부정확

**Manager 주장 (TASK-185 완료 조건 5)**: "(5) 사상가형 thinker_id·claim_id 각 ≥1 ES found=true 재조회 (전수 ES 등록 — ⚠️ES 미등록 0건)"

**문제**: "claim_id 각 ≥1 ES found=true 재조회"는 ES 인덱스 구조상 `claim_id`가 `ethics-thinkers` 인덱스의 필드가 아니라 `ethics-claims` 인덱스의 별개 document id이다. `ethics-thinkers/_doc/{id}` 조회로 thinker found=true를 검증하고, `ethics-claims` aggregation으로 claim 수를 검증하는 방식이 실제 사용 패턴(coverage L79, done-log 선례 전수)이다.

Coder가 "claim_id ES found=true 재조회" 지시를 문자 그대로 해석하면 잘못된 API 호출 경로를 시도할 수 있다. 선례(2015-A, 2014-A done-log)는 모두 `ethics-claims/_search?query=thinker_id` 방식을 사용.

**수정 요구**: 완료 조건 (5)를 "사상가형 thinker_id 전수 `ethics-thinkers/_doc/{id}` found=true 재조회 + `ethics-claims` 인덱스 thinker별 claim 수 ≥1 확인"으로 표현 정정.

---

### 4. 태스크 완결성

- 6문항 전수 커버 지시: ✅ (서술형 1~4, 논술형 1~2 각 섹션 명시)
- 포맷 지시: ✅ (TASK-182~184 선례 포맷 상세 명시)
- verbatim 규약 지시: ✅ (TASK-178-FIX 선례 명시, HTML `<u>` 보존)
- 자기검증 2단계 + 비-ASCII 확장 지시: ✅ (Step 1 regex + 비-ASCII 확장 grep 명시)
- 채점 기준 서브섹션 지시: ✅
- Tester 분리 지시: ✅ (TASK-185-T 별도 등록 예정 명시)

### 5. 의존성·순서

- TASK-DQ-007 → TASK-185 의존성: task-board 기재 정확. TASK-DQ-007 DONE이어야 TASK-185 진행 가능 구조 ✅
- TASK-184-T-R2 선행 DONE: task-board Depends On 필드에 "TASK-DQ-007" 명시 — 선행 완료 상태 확인 ✅

---

## 판정

**NEEDS_REVISION**

---

## 수정 요청

### [R-1] data-quality-log.md에 TASK-DQ-007 항목 append (필수, BLOCKER)

`signal/ethics-study/data-quality-log.md` 말미에 아래 형식으로 append:

```markdown
### TASK-DQ-007 - 2026-04-22T19:25
- file: `projects/ethics-study/exam-solutions/coverage/2015-B.md` L32-L33
- issue: "불확실·블로커 row" 섹션의 "ES 사상가 누락" 목록에 **singer(L32)·durkheim(L33) 2건이 잘못 포함**. TASK-176 시리즈(2026-04-22 DONE) 이후 두 사상가 모두 ES `found=true`·각 8 claims으로 등록됨. coverage 작성 시점(2026-04-20)에는 미등록이 정확했으나 등록 후 coverage md 업데이트 미반영.
- impact: TASK-185 (2015-B study-guide.md 작성) Coder가 L32·L33을 "누락"으로 그대로 transcribe하면 학생이 오해할 위험. 현재 실제 ⚠️ES 미등록은 0건(본 시험 전수 등록).
- detected_by: Manager 세션 2026-04-22 curl 실측 (TASK-DQ-006 선례 적용)
- resolution: 원본 수정 금지 규정으로 현재는 기록만. TASK-185 spec에 override 규정 명시 — Coder는 coverage L32·L33을 ✅ES 등록으로 표기. 배치 정정 시 coverage md 해당 문구에 "(TASK-176 DONE으로 해소)" 주석 추가 권장.
```

### [R-2] Reviewer·Coder 호출 프롬프트의 2014-A 분량 reference 정정

"약 2700 lines" → **"655 lines"** (실측, `wc -l projects/ethics-study/exam-solutions/study-guide/2014-A.md`).

향후 Coder 호출 프롬프트에서도 실측 기반 값(2014-A=655, 2014-B=309, 2015-A=674) 사용.

### [R-3] TASK-185 완료 조건 (5) 표현 정정

현재: `사상가형 thinker_id·claim_id 각 ≥1 ES found=true 재조회`
→ 수정: `사상가형 thinker_id 전수 \`ethics-thinkers/_doc/{id}\` found=true 재조회 + \`ethics-claims\` thinker별 claim 수 ≥1 확인`

---

## Manager에게 전달

PASS 전환 조건:
1. `signal/ethics-study/data-quality-log.md`에 TASK-DQ-007 항목 append (필수)
2. Coder 호출 프롬프트의 2014-A reference를 "655 lines"로 정정 (필수)
3. TASK-185 완료 조건 (5) 표현 정정 (필수)

수정 완료 후 Reviewer 재호출 (Round 2). 위 3항목 수정 후 다른 검증 항목 전수 통과 상태이므로 Round 2 PASS 예상.

참고: 2015-B 소스 파일에 Greek/Cyrillic 문자 0건으로 확인되어, `[α-ωΑ-Ωа-яА-Я]` regex의 Greek Extended 미포괄 한계는 이 태스크에서 현실적 위험 없음. 다만 regex 정의 자체의 이론적 한계는 retrospective 이월 항목으로 유지.

---

## Round 2 — 2026-04-22T19:35

### 검증 항목

#### [R-1] data-quality-log.md DQ-007 섹션 실재 확인

`signal/ethics-study/data-quality-log.md` 말미 실측:

- `## DQ-007 — 2026-04-22T19:25` 헤더 실재 (L58) ✅
- 6항 전수 실재:
  - `task_id: TASK-DQ-007` ✅
  - `file: projects/ethics-study/exam-solutions/coverage/2015-B.md L32-L36` ✅
  - `issue: singer(L32)·durkheim(L33) 잘못 포함 내용` ✅
  - `impact: TASK-185 Coder transcribe 위험 및 실제 ⚠️ES 미등록 0건 명시` ✅
  - `detected_by: TASK-185 Manager spec 작성 시 ES 실측 (2026-04-22T19:25)` ✅
  - `resolution: override 규정 명시, 배치 정정 권장, DQ-006 선례 패턴 명시` ✅

**판정: PASS** — Round 1 R-1 BLOCKER 해소 확인.

---

#### [R-3] TASK-185 완료 조건 (5) ES 인덱스 분리 명시 확인

task-board.md TASK-185 행 완료 조건 (5) 현재 텍스트:

> "(5) 사상가형 thinker_id 는 `ethics-thinkers/_doc/{id}.found=true` 재조회, claim_id 는 `ethics-claims/_doc/{id}.found=true` 재조회 (각 ≥1, 전수 ES 등록 — ⚠️ES 미등록 0건)"

- `ethics-thinkers/_doc/{id}` 와 `ethics-claims/_doc/{id}` 두 인덱스 분리 명시 ✅
- Round 1 R-3 요청("thinker_id 는 `ethics-thinkers/_doc/{id}` / claim_id 는 `ethics-claims/_doc/{id}`" 식으로 ES 인덱스 분리 명시) 이행 확인 ✅

**판정: PASS** — Round 1 R-3 해소 확인.

---

#### 추가 스캔 — 신규 지적사항 없음

Round 1 이후 TASK-185 행의 다른 내용(6문항 커버, line 범위, ES claim 수, verbatim 규약, 자기검증 2단계, 비-ASCII 확장, 분량 상한, NOTE-BLOCKER-1, 의존성) 변동 없음. 전수 PASS 유지.

---

### Round 2 판정

**PASS**

R-1 (BLOCKER) + R-3 (필수) 수정 반영 완료. 추가 지적사항 없음.

**Manager는 Coder(Opus)를 호출하여 TASK-185를 진행할 수 있다.**
