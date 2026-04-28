---
agent: coder
task_id: TASK-187
status: DONE
timestamp: 2026-04-22T20:45:00
---

## 결과 요약

2016학년도 중등임용 도덕·윤리 전공 B 학생용 풀이 가이드 `projects/ethics-study/exam-solutions/study-guide/2016-B.md` 신규 작성 완료. 8문항 서술형 전수 커버 (40점 배점 — Q1~Q5 각 4점×5 + Q6~Q7 각 5점×2 + Q8 10점×1). 분할 Write 전략 (Phase A Write: Q1~Q4 + 헤더 225 lines → Phase B Edit append: Q5~Q8 262 lines) 적용, watchdog no-progress 재발 없이 단일 파일 487 lines (47KB) 생성. ES 등록 9명 전수 `found=true` 재확증 + 대표 claim 9건 `found=true`; ES 미등록 2명 (berlin · machiavelli) `⚠️ES 미등록 (BLOCKER-2·3)` 표기. 자기검증 2단계 (Step 1 bare-paren + Step 1b Greek/Cyrillic + Step 2 TitleCase) 전수 실행, 0-hit **실질 bug 0건** (남은 Step 1 17개·Step 2 1개 0-hit은 관리·메타 wrapper로 선례 2016-A와 동형 면제 대상). 자기 교정 수행 항목: 11건 (bare-paren wrapper를 coverage 원문 wrapper 형태로 통일 + 한자 래퍼 em-dash 보존 + Political Liberalism wrapper 정정).

## 변경된 파일

- `projects/ethics-study/exam-solutions/study-guide/2016-B.md` (신규, 487 lines, 47KB)

## 파일 구성 · 완료 조건 충족 매트릭스

| # | 완료 조건 (task-board L306) | 실측 결과 |
|---|-------|--------|
| 1 | 파일 생성 `study-guide/2016-B.md` | ✅ `487 lines / 47KB` |
| 2 | 8문항 전수 커버 (서술형 Q1~Q8) | ✅ `grep -c '^## 문항' == 8` |
| 3 | 각 섹션 헤더 `원문 line L{m}-L{n}` metadata 실재 | ✅ 8/8 전수 — L16-L26·L29-L40·L44-L49·L53-L59·L63-L71·L75-L81·L85-L89·L95-L108 스펙 일치 |
| 4 | 제시문 verbatim byte-level 일치 | ✅ HTML `<u>` 5 쌍 (원본 기출과 동일 개수) · ㉠ 31회·㉡ 20회·㉢ 0회 · em-dash U+2014 (E2 80 94) 128회 · en-dash 0회 · 한자 보존 |
| 5 | ES 등록 9명 전수 `found=true` + 대표 claim_id 각 ≥1 | ✅ 전수 재조회: epicurus·sandel·yiyulgok·xunzi·laozi·rousseau·raths·kohlberg·lickona — thinker 9/9 + claim 9/9 `found=true` |
| 6 | ES 미등록 2명 (berlin·machiavelli) `⚠️ES 미등록 (BLOCKER-2·3)` 표기 | ✅ Q4 (가)·(나) 각각 `⚠️ES 미등록 (BLOCKER-2 · BLK-175E-2016B-002)` / `(BLOCKER-3 · BLK-175E-2016B-003)` 명시 + 헤더 ES 등록 상태 표 기재 |
| 7 | Q2 통일교육 `해당 없음` 분류 사유 명시 | ✅ Q2 "해당 없음 (교과교육학 · 통일교육 · 북한 이해)" · 북한 사회주의 헌법 제63조 외부 근거 참조 명시 |
| 8 | Q3 BLOCKER-1 주석 (공동체주의 일반론 · 단일 사상가 특정 제한) 실재 | ✅ Q3 L149 "⚠️ 단일 사상가 특정 불가 · 공동체주의 일반론 (sandel 대표 매핑 · macintyre/taylor/walzer 가능성 열림) — BLOCKER-1 (BLK-175E-2016B-001)" 주석 + 3후보 열거 |
| 9 | Q5 (가) 『중용』 고전 `해당 없음` 분류 사유 명시 | ✅ Q5 "(가) 해당 없음 (동양 고전 · 자사[子思] 귀속)" · 사서 경서 설명 포함 |
| 10 | 서술형 Q1~Q8 전원 `### 채점 기준` 실재 + 배점 4/4/4/4/4/5/5/10 분할 | ✅ `grep -c '^### 채점 기준' == 8` · 각 배점 명시 |
| 11 | 자기검증 2단계 + Greek/Cyrillic 확장 + 한자 래퍼 보존 결과 표 report 포함 | ✅ 아래 "자기검증 루프 결과" 섹션 |

## 자기검증 루프 결과 (agents/coder.md L89-L115 전수)

### Step 1 — bare-paren English 토큰 전수

- **추출 명령**: `grep -oE '\([A-Za-z][^)]*\)' 2016-B.md | sort -u`
- **총 추출 토큰**: **78건**
- **coverage 역grep (`LC_ALL=C.UTF-8 grep -Fc` case-sensitive) ≥ 1 hit**: **61건 (78.2%)**
- **0-hit**: **17건 (21.8%) — 전수 관리·메타 wrapper로 면제 정당 (선례 2016-A 동형)**

0-hit 토큰 분류표:

| # | 토큰 | 분류 | 면제 근거 |
|---|------|------|-----------|
| 1 | `(BLK-175E-2016B-001)` | BLOCKER ID | BLK-* prefix 는 task-board blocker id. 관리 메타. |
| 2 | `(BLOCKER-1 주석 참조)` | 메타 참조 | 학생용 가이드 내부 cross-ref. |
| 3 | `(BLOCKER-1)` | BLOCKER ID | 선례 2016-A `(BLOCKER-1)`·`(BLOCKER-3)` 등 동형 사용 확증. |
| 4 | `(BLOCKER-2)` | BLOCKER ID | 동상. |
| 5 | `(BLOCKER-2·3)` | BLOCKER ID 결합 | 헤더 요약 표기. |
| 6 | `(BLOCKER-3)` | BLOCKER ID | 동상. |
| 7 | `(ES lickona-claim-001·lickona-claim-004)` | ES cross-ref | 학생용 해설 내부 claim 참조. |
| 8 | `(ES lickona-claim-005·lickona-claim-009)` | ES cross-ref | 동상. |
| 9 | `(ES sandel-claim-001·002 참조)` | ES cross-ref | 동상. |
| 10 | `(L1~L244)` | 파일 range | 헤더 coverage 원천 라인 범위 메타. |
| 11 | `(Q1~Q5 각 4점 × 5 = 20점 + Q6~Q7 각 5점 × 2 = 10점 + Q8 10점 × 1 = 10점, 배점 불균등)` | 배점 메타 | 헤더 배점 요약. |
| 12 | `(Q4 가)` | 문항 항목 | 헤더 요약 표기. |
| 13 | `(Q4 나)` | 문항 항목 | 동상. |
| 14 | `(TASK-186 산출물)` | 태스크 id | 헤더 선례 파일 언급. |
| 15 | `(TASK-187)` | 태스크 id | 푸터 작성 태스크 언급. |
| 16 | `(sandel 대표 매핑 · macintyre/taylor/walzer 가능성 열림)` | BLOCKER-1 주석 | Q3 ⚠️ 주석 헤더 문구. |
| 17 | `(sandel)` | thinker_id 태그 | 헤더 "샌델(sandel)을 대표로 매핑" — 2016-A 의 `(jonas)`·`(yangzi)` 동형 면제. |

실체(원문 인용) 영어 학술 용어 대상 0-hit = **0건** — bug 0.

### Step 1b — Greek/Cyrillic 확장 괄호 전수 (TASK-184-FIX 교훈)

- **추출 명령**: `grep -oE '\([^)]*[α-ωΑ-Ωа-яА-Я][^)]*\)' 2016-B.md | sort -u`
- **총 추출 토큰**: **4건**
- **0-hit**: **0건 (100% hit)**

| 토큰 | coverage hit |
|------|-------|
| `(ἀπονία — 고통의 부재, 신체적 쾌락의 극한)` | 2 |
| `(ἀταραξία — 마음의 평정, 정신적 쾌락의 극한)` | 2 |
| `(δικαιοσύνη)` | 1 |
| `(λάθε βιώσας — lathe biōsas, live unnoticed)` | 1 |

Q1 에피쿠로스의 Greek 고유명(ἀπονία·ἀταραξία·λάθε βιώσας·κῆπος·δικαιοσύνη)은 **한자 래퍼 보존 규약에 준하여 coverage 원문 wrapper 전체를 그대로 복사 적용**. TASK-185-FIX 선례에 따라 em-dash U+2014 byte 보존.

### Step 2 — 괄호 밖 TitleCase phrase 전수

- **추출 명령**: `grep -oE '[A-Z][a-z]+(\s+[A-Za-z][a-z]+){1,5}' 2016-B.md | sort -u`
- **총 추출 토큰**: **22건**
- **coverage hit ≥ 1**: **21건 (95.5%)**
- **0-hit**: **1건 (4.5%) — 푸터 메타 wrapper**

| 토큰 | coverage hit | 분류 |
|------|-------|------|
| `Alasdair Mac` | 1 | (전체 `Alasdair MacIntyre` 의 substring 추출) |
| `Charles Taylor` | 1 | 인명 |
| `Coder Agent` | 0 | **푸터 메타 (면제 — 선례 2016-A 동형)** |
| `Discorsi sopra la prima deca di` | 1 | 저서명 |
| `Discourses on Livy` | 1 | 저서명 |
| `Du contrat social` | 1 | 저서명 |
| `Isaiah Berlin` | 1 | 인명 |
| `Jacques Rousseau` | 1 | 인명 |
| `Lawrence Kohlberg` | 1 | 인명 |
| `Letter to Menoeceus` | 1 | 저서명 |
| `Liberalism and the Limits of Justice` | 1 | 저서명 |
| `Louis Raths` | 1 | 인명 |
| `Michael Sandel` | 1 | 인명 |
| `Michael Walzer` | 1 | 인명 |
| `Philip Pettit` | 1 | 인명 |
| `Quentin Skinner` | 1 | 인명 |
| `The Doctrine of the Mean` | 1 | 저서명 |
| `Thomas Lickona` | 1 | 인명 |
| `Tito Livio` | 1 | 인명 |
| `Two Concepts of Liberty` | 1 | 저서명 |
| `Un gouvernement si parfait ne convient` | 1 | 원문 인용 |

실체 0-hit = **0건** — bug 0.

### 자기 교정 이력 (저장 중 교정 건)

| # | 초기 wrapper | coverage 역grep | 교정 후 wrapper | 교정 유형 |
|---|--------------|-----|-------|----------|
| 1 | `(katastematic pleasure)` | 0 | `정적 쾌락, katastematic pleasure — 아포니아·아타락시아` (inline) + `(ἀπονία — 고통의 부재, 신체적 쾌락의 극한)` 등 분리 | coverage wrapper 복원 |
| 2 | `(area of non-interference)` | 0 | `[area of non-interference]` (대괄호) | coverage 원문 bracket 유형 일치 |
| 3 | `(Discorsi, 1531)` | 0 | `(Discorsi sopra la prima deca di Tito Livio, Discourses on Livy, 1531)` | full form 확장 |
| 4 | `(grande simplicité de mœurs)` | 0 | `(소박한 단순성 — grande simplicité de mœurs)` | coverage 한자/한글 대응 래퍼 복원 |
| 5 | `(grande égalité)` (축약) | 0 | `(grande égalité dans les rangs et dans les fortunes)` | full form 확장 |
| 6 | `(très-petit État)` (괄호 wrapper) | 0 | `— très-petit État —` (em-dash inline) + 풀이 과정 별도 full form | inline 형태로 전환 |
| 7 | `(volonté générale)` | 0 | `(一般意志 — volonté générale)` | 한자+한글+프랑스어 full 래퍼 |
| 8 | `(knowing the good, loving the good, doing the good)` | 0 | `"knowing the good, loving the good, doing the good"` (쌍따옴표) | coverage 원문 quoted 형태 |
| 9 | `(sandel-claim-001·002)` | 0 | `(ES sandel-claim-001·002 참조)` 관리 메타 | ES prefix + 참조 명시 (관리 wrapper 분류) |
| 10 | `(claim-001·004)` / `(claim-005·009)` | 0 | `(ES lickona-claim-001·lickona-claim-004)` / `(ES lickona-claim-005·lickona-claim-009)` | full id 확장 + ES prefix |
| 11 | `(Political Liberalism 비판·Justice)` | 0 | `(Political Liberalism 비판·Justice·Liberalism and the Limits of Justice)` | coverage 원문 wrapper 전체 복원 |

총 11건 자기 교정 수행. 모든 교정은 coverage md 원문에 grep-hit ≥ 1 이 보장되는 형태로 재작성.

### 한자(漢字) — 영어 래퍼 em-dash U+2014 보존 샘플 (TASK-185-FIX 교훈)

- **파일 전체 em-dash count**: 128회 (en-dash U+2013 = 0회, byte-level 교체 없음)
- **byte sample (`\xe2\x80\x94`)**:
  1. `'·윤리 전공 B — 학생용 풀이'` (헤더)
  2. `'시리즈 — 2016-B'` (헤더)
  3. `'감각(感覺)의 소멸(消滅) — 또는 동의'` (Q1 정답)
- coverage 원문의 `한자(漢字) — 영어` 래퍼 (예: `自然的이고 必然的인 欲求 — natural and necessary desires`, `소박한 단순성 — grande simplicité de mœurs`, `一般意志 — volonté générale`, `정적 쾌락, katastematic pleasure — 아포니아·아타락시아`) 전체 verbatim 복사 완료.

## ES 재조회 결과 (본 세션 2026-04-22 curl 실측)

### thinker 9명

| thinker_id | `found` | claim 수 | 본문 매핑 문항 |
|------------|---------|---------|-----------|
| `epicurus` | ✅ true | 8 | Q1 |
| `sandel` | ✅ true | 10 | Q3 (대표 매핑, BLOCKER-1) |
| `yiyulgok` | ✅ true | 12 | Q5 (나) |
| `xunzi` | ✅ true | 11 | Q6 (가) |
| `laozi` | ✅ true | 12 | Q6 (나) |
| `rousseau` | ✅ true | 13 | Q7 |
| `raths` | ✅ true | 10 | Q8 (가) |
| `kohlberg` | ✅ true | 20 | Q8 (나) |
| `lickona` | ✅ true | 10 | Q8 (다) |

### ES 미등록 2명 (curl 재확증)

| thinker_id | `found` | 블로커 |
|------------|---------|--------|
| `berlin` | ❌ false (404) | BLOCKER-2 (BLK-175E-2016B-002) — Q4 (가) |
| `machiavelli` | ❌ false (404) | BLOCKER-3 (BLK-175E-2016B-003) — Q4 (나) |

### 대표 claim_id 9개 전수 `found=true`

- `epicurus-claim-003` · `sandel-claim-001` · `yiyulgok-claim-002` · `xunzi-claim-003` · `laozi-claim-002` · `rousseau-claim-005` · `raths-claim-001` · `kohlberg-claim-011` · `lickona-claim-001` — 전수 `found=true`.

## 이슈/블로커

- **BLOCKER-1 (BLK-175E-2016B-001)** — Q3 공동체주의 일반론으로 단일 사상가 trademark 결정적 구절 부재. sandel 대표 매핑하되 macintyre/taylor/walzer 가능성 열림. coverage 선례 그대로 반영.
- **BLOCKER-2 (BLK-175E-2016B-002)** — Q4 (가) berlin ES 미등록. TASK-176 신규 사상가 등록 대기.
- **BLOCKER-3 (BLK-175E-2016B-003)** — Q4 (나) machiavelli ES 미등록. TASK-176 신규 사상가 등록 대기.

코드 결함 또는 신규 이슈 **없음**.

## 다음 제안

- **Tester 검증**: `TASK-187-T` 이미 task-board 등록 (10항 체크). Tester 실행 요망.
- **ES 보강 제안** (TASK-176 후속):
  1. `berlin` (Isaiah Berlin) 신규 등록 — 『Two Concepts of Liberty』(1958) 기반 claim: 소극적/적극적 자유 / 가치 다원주의 / 긍정적 자유의 위험.
  2. `machiavelli` (Niccolò Machiavelli) 신규 등록 — 『Discorsi sopra la prima deca di Tito Livio』(1531) 기반 claim: 공화주의적 자유·비지배 / 평민-귀족 내분 = 자유의 동력 / virtù·fortuna / 『군주론』 현실주의.
- **claim 보강**:
  1. `rousseau-claim-014` 신규 — 루소의 정부 형태 3분류(민주정·귀족정·군주정) + 민주정 실현 3조건 (작은 국가 · 소박한 풍속 · 신분·재산 평등).
  2. `yiyulgok-claim-013` 신규 — 율곡의 성(誠) 개념 전용 claim (이통기국·이일분수 체계 안에서의 성[誠] 해석).

---

**작성**: 2026-04-22T20:45 · Coder Agent (TASK-187) · `signal/ethics-study/coder-report-TASK-187.md`
