---
agent: coder
task_id: TASK-202
status: DONE
severity: none
---

# Coder Report · TASK-202 · 2024-A 학생용 study-guide.md 신규 작성

## 1. 결과 요약

- 산출 파일: `projects/ethics-study/exam-solutions/study-guide/2024-A.md`
- 최종 줄 수: **728L** (1150L 한도 대비 63.3% · 여유 422L)
- 문항 수: **12 문항** (`## 문항` 헤더 `grep -cE '^## 문항' = 12` 실측)
- 채점 기준 블록: **8 블록** (Q5—Q12 서술형 4점×8 · `grep -cE '^### 채점 기준' = 8` 실측)
- 자기검증 3단계 프로토콜 통과 · disjoint 교집합 pairwise 0 확증 · fudge 문구 0건 확증.
- ES 재조회 HIT 11명 · narvaez DQ-018 override 정상 HIT · BLOCKER 2건 (coombs · fazang) 404.

## 2. 작성 파일 목록

| 경로 | 상태 | 줄 수 | 비고 |
|------|------|-------|------|
| `projects/ethics-study/exam-solutions/study-guide/2024-A.md` | CREATED | 728 | 헤더·Q1—Q12·Self-Check 포함 |

## 3. 자기검증 3단계 표

### Step 1 · 괄호 안 영어 토큰 `grep -oE '\([A-Za-z][^)]*\)' | sort -u | wc -l`

- **고유 토큰 수: 104**
- 주요 구성: 사상가 영문 이름/생몰(`Aristotle, 384—322 BC` · `David Hume, 1711—1776` 등), 저서 원제(`A Theory of Justice, 1971` · `Anarchy, State, and Utopia, 1974` 등), 기술 용어(`Hume's Law` · `Enlightenment project` 등), BLOCKER ID(`BLK-175E-2024A-001`~`005`).
- **전수 검증**: coverage/2024-A.md 역grep 결과 모든 토큰 cov ≥ 1 확인. Phase 6 창작 금지 규칙 준수.

### Step 1b · 그리스·확장 라틴·키릴·산스크리트·움라우트 확장 문자 토큰

- **고유 토큰 수: 0** (좁은 문자 클래스 `[ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩαβγδεζηθικλμνξοπρστυφχψωāīūṛṣṇṃḥäöüéèêçñ]+` 기준)
- 정리 내역: 초기 스캔에서 `tathāgatagarbha` (산스크리트) 2건 발견 → coverage + 원문 모두 0 hit 확인 후 삭제 (L443 · L471).

### Step 2 · 괄호 밖 TitleCase 2—6 단어 구 `grep -oE '[A-Z][a-z]+(\s+[A-Za-z][a-z]+){1,5}' | sort -u | wc -l`

- **고유 구 수: 37**
- 전수 검증: 37 phrase 모두 coverage/2024-A.md 에 cov ≥ 1 hit (예: `After Virtue` cov=8, `Alasdair MacIntyre` cov=5, `Spheres of Justice` cov=2, `Yemen unification` cov=1 등). 원문 md 에 cov=0 이어도 **coverage md 는 Phase 6 승인 레퍼런스**이므로 인용 허용.
- 정리 내역: 초기 Phase A 작성 시 Herodotos·Nicomachean Ethics·eudaimonia·proairesis·IEE·Integrated Ethical Education·Values Conflict Resolution Model·Triune Ethics Meta-theory·MacLean triune brain·engagement ethics·imagination ethics·harm principle 등 17건 + 2차 정리에서 "Objectives of Value Analysis"·"Critical Commentary on the Great Learning"·"Lectures on the Doctrine of the Mean"·"Essentials of Mencius"·"Awakening of Mahāyāna Faith"·"Treatise on Reconciliation in Ten Gates"·"Treatise on the Five Teachings of the Huayan School"·"Coder Self-Check"·"Greek Extended…narrow character class" 등 11건 모두 삭제.

### Disjoint 교집합 pairwise = 0 확증

| 쌍 | `comm -12` 수 | 확증 |
|----|---------------|------|
| Step 1 ∩ Step 1b | 0 | pass |
| Step 1 ∩ Step 2 | 0 | pass |
| Step 1b ∩ Step 2 | 0 | pass |

## 4. ES 재조회 결과

### HIT 11명 (`GET /ethics-thinkers/_doc/{tid}` HTTP 200)

| thinker_id | HTTP | 문항 | 주요 claim_id 인용 |
|------------|------|------|---------------------|
| `macintyre` | 200 | Q2 | `macintyre-claim-001`~`003` (실천/전통/서사적 자아) |
| `mill_js` | 200 | Q4 | `mill_js-claim-001`~`002` (공리주의·해악 원리) |
| `gilligan` | 200 | Q6 | `gilligan-claim-001`~`003` (배려 윤리·In a Different Voice) |
| `narvaez` | 200 | Q6 | `narvaez-claim-001`~`003` (DQ-018 override · Triune Ethics Theory) |
| `jeongyagyong` | 200 | Q7 | `jeongyagyong-claim-001`~`005` (영명무형·성기호설·자주지권) |
| `wonhyo` | 200 | Q8 | `wonhyo-claim-001`~`003` (일심이문·화쟁·한 맛) |
| `hume` | 200 | Q9 | `hume-claim-001`~`003` (감정 도덕론·Hume's Law) |
| `aristotle` | 200 | Q10 | `aristotle-claim-001`~`003` (덕 윤리·습관) |
| `nozick` | 200 | Q11 | `nozick-claim-001`~`002` (소유권리론) |
| `walzer` | 200 | Q11 | `walzer-claim-001`~`002` (Spheres of Justice·복합 평등) |
| `rawls` | 200 | Q11 | `rawls-claim-001`~`003` (정의의 두 원칙·차등 원칙) |

### narvaez DQ-018 override

- coverage/2024-A.md 에는 **BLOCKER-5 (narvaez)** 로 기재되어 있으나, 본 세션 curl 실측 시 `ethics-thinkers/_doc/narvaez` HTTP 200 · `ethics-claims` 9건 색인 · `narvaez-claim-001/002/003` `"found":true` 재확인.
- 학생용 가이드에서는 일반 HIT 로 취급 · BLOCKER 마커 부착하지 않음 · claim_id 인용 정상 수행.
- 근거: `signal/ethics-study/data-quality-log.md` DQ-018 엔트리 (L141—L200 참조).

### BLOCKER 404 2건

| thinker_id | HTTP | 사유 | 가이드 처리 |
|------------|------|------|-------------|
| `coombs` | 404 | Jerrold R. Coombs · 교과교육 실천가 · 가치갈등해결 수업 모형 · ethics-study 사상가 DB 미등록 | Q5 BLOCKER-1 (BLK-175E-2024A-001) 마킹 · claim 인용 없이 교과서 공통 명제만 서술 |
| `fazang` | 404 | 법장(法藏, 643—712) · 화엄종 3조 · 사법계/십현문/육상원융 · 중국 화엄 DB 미등록 | Q8 BLOCKER-4 (BLK-175E-2024A-005) 마킹 · 『화엄오교장』·『대승기신론』 등 공통 명제로 ㉠ 사사무애법계 도출 |

### 추가 BLOCKER 2건 (thinker_id 특정 불능)

| ID | 유형 | 사유 | 가이드 처리 |
|----|------|------|-------------|
| BLK-175E-2024A-003 | Q5 ㉢ 검사 명칭 | ethics-study 사상가 DB 조회 대상 X · 교과서 표준 (포섭 검사 유력) | BLOCKER-2 마킹 · 채점 기준에 "포섭 검사" 지정 |
| BLK-175E-2024A-004 | Q7 갑 한국 성리학자 | 심성정의 1로 구조 원문 trademark 3중 일치 미성립 · 퇴계/율곡 등 특정 불능 | BLOCKER-3 마킹 · Phase 6 창작 금지 준수 · 공통 명제만 서술 |

## 5. em-dash (U+2014) 하드코딩 확증 · hexdump 3+ 샘플

모든 가이드의 `—` 는 U+2014 em-dash (`e2 80 94`) 로 통일.

### Sample 1 · L1 헤더

```
# 2024학년도 중등임용 도덕·윤리 전공 A — 학생용 풀이 가이드
```

offset 0x35—0x37: `e2 80 94` (A 와 학생용 사이 em-dash) 확증.

### Sample 2 · L3 L1—L223 표기

```
(L1—L223 · 223 lines · 파일명 중간점 `·` 포함 — 2024년부터 명명 규칙 변경)
```

offset 0x60—0x62: `e2 80 94` (L1 과 L223 사이 em-dash) 확증. `·` 는 U+00B7 (`c2 b7`) 로 구분.

### Sample 3 · L4 coverage 라인 범위

```
- **커버리지 원천**: `projects/ethics-study/exam-solutions/coverage/2024-A.md` (L1—L765)
```

offset 0x48—0x4A: `e2 80 94` (L1 과 L765 사이 em-dash) 확증.

## 6. Fudge 문구 0건 확증

`grep -cE '≈|수렴|중복 보정|대략' 2024-A.md = 0`

- `≈` (근사) 0건
- `수렴` 0건
- `중복 보정` 0건
- `대략` 0건

## 7. 이슈 / 블로커

없음 (severity: none).

`coombs` · `fazang` · BLK-175E-2024A-003 · BLK-175E-2024A-004 는 **예정된 데이터 품질 블로커**로 가이드 내 ⚠️ES 미등록 마커를 사용해 투명하게 고지했으며, 학생이 Phase 6 창작 금지 규정을 이해하는 데 방해되지 않도록 공통 명제·채점 기준만 서술함. 후속 배치 정정 시점에 `signal/ethics-study/data-quality-log.md` 에 일괄 적재 검토 필요 (단, 본 태스크 범위 외).

## 8. 다음 단계 제안

1. TASK-203 (2024-B 또는 후속 연도) 진행 시 동일한 3단계 자기검증 프로토콜 적용.
2. `coombs`·`fazang` 데이터 품질 이슈는 Track B 전체 시리즈(21/26) 진행 후 일괄 DQ 태스크로 분리 검토.
3. Q7 한국 성리학자 특정 불능 이슈(BLK-175E-2024A-004)는 원문 trademark 분석이 가능한 시점에 퇴계 vs 율곡 판별을 위한 별도 태스크 검토 권장.

## 9. 완료 조건 충족 확인

| 조건 | 상태 |
|------|------|
| 12 문항 전체 커버 (Q1—Q12) | pass (`grep -cE '^## 문항' = 12`) |
| 8 서술형 채점 기준 블록 | pass (`grep -cE '^### 채점 기준' = 8`) |
| Step 1·1b·2 자기검증 통과 | pass (104·0·37 · disjoint pairwise 0) |
| Phase 6 창작 금지 준수 | pass (0-hit 토큰 28건 삭제 완료) |
| byte-level verbatim (em-dash U+2014) | pass (3+ hexdump 샘플 확증) |
| narvaez DQ-018 override 반영 | pass (일반 HIT 처리 · claim_id 인용) |
| BLOCKER 4건 마킹 | pass (coombs · fazang · BLK-003 · BLK-004) |
| 1150L 한도 준수 | pass (728L · 여유 422L) |
| fudge 문구 0건 | pass (`grep -cE '≈|수렴|중복 보정|대략' = 0`) |
| Coder report 저장 | pass (본 파일) |
