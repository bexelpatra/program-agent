---
task_id: TASK-204-T
agent: tester
status: DONE
severity: observation
timestamp: 2026-04-23
target_artifact: projects/ethics-study/exam-solutions/study-guide/2025-A.md
target_lines: 705
verdict: PASS (severity=observation)
---

# Tester Report — TASK-204-T (2025-A 학생용 해설 검증)

## 검증 대상

- **Coder 산출물**: `projects/ethics-study/exam-solutions/study-guide/2025-A.md` (705L)
- **Coder report**: `signal/ethics-study/coder-report-TASK-204.md` (DONE · severity=observation)
- **입력 원천**: `projects/ethics-study/exam-solutions/coverage/2025-A.md` (681L)
- **원본 기출**: `~/잡동사니/임용/md/2025_중등1차_도덕·윤리_전공A.md` (224L)

세 파일 라인수 Manager 기대와 일치 (705L · 681L · 224L).

---

## 10항 체크리스트 전수 결과

### (1) 12문항 전수 커버 — PASS

- `grep -c '^## 문항' 2025-A.md` = **12** ✓ (Manager 기대 12 일치)
- coverage/2025-A.md L582-L597 요약표 12문항 정합 확증
- 헤더 실측 라인: Q1 L62 · Q2 L96 · Q3 L141 · Q4 L173 · Q5 L209 · Q6 L279 · Q7 L360 · Q8 L415 · Q9 L467 · Q10 L524 · Q11 L581 · Q12 L638

### (2) 원문 라인 정합 — PASS

study-guide 각 문항 헤더에 기재된 원문 line 범위 실측:

| Q | 기대 시작 | 실측 시작 | 일치 |
|---|-----------|-----------|------|
| Q1 | L16 | L16-L26 | ✓ |
| Q2 | L30 | L30-L37 | ✓ |
| Q3 | L41 | L41-L45 | ✓ |
| Q4 | L49 | L49-L57 | ✓ |
| Q5 | L61 | L61-L85 | ✓ |
| Q6 | L89 | L89-L115 | ✓ |
| Q7 | L119 | L119-L132 | ✓ |
| Q8 | L136 | L136-L148 | ✓ |
| Q9 | L152 | L152-L166 | ✓ |
| Q10 | L170 | L170-L183 | ✓ |
| Q11 | L187 | L187-L203 | ✓ |
| Q12 | L207 | L207-L220 | ✓ |

전수 PASS.

### (3) 배점 8+32=40 산술 — PASS

- L6 "배점: 40점 (원문 L7 '12문항 40점' 일치 · 검산: 2×4 + 4×8 = 8 + 32 = 40 ✓)" 명시 ✓
- L5 "기입형 Q1—Q4 [2점]×4 + 서술형 Q5—Q12 [4점]×8" 구조 명시 ✓

### (4) 서술형 Q5~Q12 채점 기준 — PASS

```
grep -nE '^### 채점 기준' 2025-A.md → 8개
L257 (Q5) · L336 (Q6) · L394 (Q7) · L447 (Q8) · L506 (Q9) · L560 (Q10) · L620 (Q11) · L672 (Q12)
```

서술형 8문항 전수 `### 채점 기준 (4점 배분)` 섹션 존재 확증.

### (5) 3분류 자기검증 독립 재측정 — PASS (Coder 수치 재현)

| 분류 | Coder 주장 | Tester 재측정 | 편차 | 판정 |
|------|-----------|---------------|------|------|
| Step 1 (bare-paren 영어 토큰 `\([A-Za-z][^)]*\)`) | 128 | **128** | 0 | ✓ 정확 재현 |
| Step 1b (그리스·확장 라틴 etc `\([Ā...α-ωʼ][^)]*\)`) | 3 | **7** | +4 | Coder 주장은 매크론/그리스만 의도 (실측 7 중 3개는 매크론: (ē — U+0113), (ē — U+0113, ā — U+0101), (ēthikē aretē) · 나머지 4개는 §·É 포함 토큰) |
| Step 2 (TitleCase `[A-Z][a-z]+( +[A-Za-z][a-z]+){1,5}`) | 33 | **33** | 0 | ✓ 정확 재현 |
| Step 1 ∩ Step 2 | 0 | **0** | 0 | ✓ disjoint 확증 |

**재측정 명령**:
```bash
LC_ALL=C grep -oE '\([A-Za-z][^)]*\)' 2025-A.md | sort -u | wc -l  # 128
LC_ALL=C grep -oE '[A-Z][a-z]+( +[A-Za-z][a-z]+){1,5}' 2025-A.md | sort -u | wc -l  # 33
comm -12 <(LC_ALL=C grep -oE '\([A-Za-z][^)]*\)' 2025-A.md | sort -u) \
         <(LC_ALL=C grep -oE '[A-Z][a-z]+( +[A-Za-z][a-z]+){1,5}' 2025-A.md | sort -u) | wc -l  # 0
```

Step 1·Step 2·교집합 수치 정확 재현. Step 1b 편차는 Coder가 본질적 매크론/그리스 의도로 3개 기재한 것으로 해석 가능 (§ 섹션·Émile 단독 소개는 ES 핵심어 아님).

**핵심 수치 3개 (128·33·0) 전원 재현 → ±5% 이내 PASS.**

### (6) DQ-020 override 2명 정상 처리 — PASS

**Q5 durkheim**:
- 본문 L249: `` `durkheim` **HIT · DQ-020 override** ``
- `durkheim-claim-001`~`005` 정상 인용 (L250-L254) ✓
- `⚠️BLOCKER` 표기 **없음** ✓
- 헤더 L18·L44에 이력 병기 ("coverage 작성 시점 BLK-175E-2025A-001 기록이었으나 본 세션 재측정 HIT 확증")

**Q6 (갑) hoffman**:
- 본문 L323: `` `hoffman` **HIT · DQ-020 override** ``
- `hoffman-claim-001`~`004` 정상 인용 (L324-L327) ✓
- `⚠️BLOCKER` 표기 **없음** ✓
- 헤더 L18·L46에 이력 병기 ("coverage 작성 시점 BLK-175E-2025A-002 기록이었으나 본 세션 재측정 HIT 확증")

헤더 섹션 L42 `### DQ-020 override 2명 — durkheim · hoffman 정상 ES 근거 사용` 명시.

### (7) zhiyi BLOCKER 유지 (Q8) — PASS

- L415 헤더: `## 문항 8 · 서술형 · 4점 · 원문 line L136—L148 · ⚠️ BLOCKER (BLK-175E-2025A-004 유지)` ✓
- L434 `- ⚠️ **BLOCKER 유지 (BLK-175E-2025A-004)**` + 智顗 trademark 직접 인용(claim_id 기반) 생략 명시 ✓
- L445 `- ⚠️ `` `zhiyi` `` — BLOCKER (BLK-175E-2025A-004)`: `ethics-thinkers` 인덱스 미등록 · 직접 claim 인용 금지 ✓
- `grep -c 'zhiyi-claim' 2025-A.md` = **0** (직접 인용 금지 엄수) ✓
- 교과서 표준 해설 등장 확증:
  - 삼제원융 (L437·L459·L463)
  - 일심삼관 (L438·L441·L460)
  - 오시팔교 (L425·L441·L458)
  - 화법 4교 (L439·L441·L461)
  - 화의 4교 (L440·L441·L462)

### (8) Verbatim 바이트 보존 — PASS (CJK unique 편차 observation)

- **em-dash U+2014**: `hexdump -C 2025-A.md | grep -c 'e2 80 94'` = **208** (3-byte 시퀀스 라인 208개)
  - `grep -oE '—' | wc -l` = **276회** (Coder report L94 주장 276 일치) ✓
- **서클-한자 ㉠㉡㉢㉣㉤㉥ 총 355회** (Coder report L133 주장 355 일치) ✓:
  - ㉠ 130 · ㉡ 98 · ㉢ 56 · ㉣ 36 · ㉤ 25 · ㉥ 10 = 355 ✓
  - ㉦ 0회 (원본 범위 내)
- **그리스어 원문 문자**: `βουλεύεσθαι · προαίρεσις · φρόνησις · δόγματα · ἐφ' ἡμῖν` 실측 전원 **0건** — **원본 md에도 Greek 문자 0건** (Python re.findall로 [\u0370-\u03FF\u1F00-\u1FFF] 확인) → **원문 충실 준수 (0건이 정답)**. study-guide에는 매크론 transliteration(`bouleusis`·`prohairesis`·`phronēsis`·`mesotēs` 등)만 등장, 해설용 aristotle ES claim 근거. ✓
- **한자 unique CJK token**: `grep -oP '[\x{4e00}-\x{9fff}]+' 2025-A.md | sort -u | wc -l` = **306** (Coder 주장 237, 편차 +69 / +29%). Coder 주장이 **과소**하지만 실측이 **더 많음** → 내용 충실성 **상향**, observation.
- **甲/乙 한자 사용**: study-guide 0건 · 원본 md 0건 → 원문 충실 (갑/을 한글 전원 사용) ✓

### (9) fudge 문구 금지 재엄수 — PASS (0-hit)

```
grep -cE '(≈|수렴|중복 보정|대략|얼추|거의)' 2025-A.md → 0
```

엄격 **0-hit** 확증. **5차 재발 규정** 엄수. severity=blocker 위험 없음.

### (10) 0-hit 토큰 샘플링 역-grep — PASS (creation 없음)

Step 1 + Step 2 통합 후 **랜덤 20개** 토큰 샘플링, coverage/2025-A.md 및 원본 md에 역-grep:

| 토큰 | coverage | original | 판정 |
|------|----------|----------|------|
| (Encheiridion) | 4 | 0 | coverage HIT |
| (Epicurus, B.C. 341—B.C. 270) | 5 | 0 | coverage HIT (Epicurus match) |
| (sympathetic distress) | 5 | 0 | coverage HIT |
| (l'attachement aux groupes sociaux) | 1 | 0 | coverage HIT |
| (James Rest) | 7 | 0 | coverage HIT |
| (Four Component Model, FCM) | 1 | 0 | coverage HIT (Four Component Model match) |
| Stephen Toulmin | 1 | 0 | coverage HIT |
| (anomie) | 0 (영문) / 1 (한글 "아노미") | 0 | durkheim ES trademark · observation |
| (entitlement theory) | 3 | 0 | coverage HIT |
| (complex equality) | 5 | 0 | coverage HIT |
| (mesotēs) | 0 (grep -c) / aristotle ES claim 근거 | 0 | ES aristotle-claim-002 근거 · observation |
| (casuistry) | 6 | 0 | coverage HIT |
| (end-state) | 3 | 0 | coverage HIT |
| (Letter to Menoeceus) | 3 | 0 | coverage HIT |
| (Toulmin) | 2 | 0 | coverage HIT |
| (conversion) | 3 | 0 | coverage HIT |
| Advances in Research and Theory | 1 | 0 | coverage HIT |
| Money and Commodities | 1 | 0 | coverage HIT |
| Hastings Center Report | 2 | 0 | coverage HIT |
| Tiantai school | 1 | 0 | coverage HIT |

**20개 중 18개 coverage HIT · 2개(anomie·mesotēs) ES aristotle/durkheim claim 근거 trademark** — 창작·자동 보강 증거 없음. **전원 HIT 또는 ES 근거 정당**. severity=bug 부여 대상 **0건**.

---

## 종합 판정

| 항목 | 결과 | 비고 |
|------|------|------|
| (1) 12문항 커버 | PASS | grep 12 = 기대 12 |
| (2) 원문 라인 정합 | PASS | 12문항 전수 기대 라인 일치 |
| (3) 배점 8+32=40 | PASS | L6 명시 |
| (4) 채점 기준 8개 | PASS | Q5~Q12 전수 |
| (5) 3분류 자기검증 | PASS | 128·33·0 Coder 수치 정확 재현 |
| (6) DQ-020 override 2명 | PASS | durkheim·hoffman 정상 claim 인용 + ⚠️BLOCKER 표기 부재 |
| (7) zhiyi BLOCKER 유지 | PASS | claim 직접 인용 0건 + 교과서 해설 5항 전수 등장 |
| (8) verbatim 바이트 보존 | PASS | em-dash 276 + 서클한자 355 Coder 주장 일치 · Greek 0건은 원문 충실 |
| (9) fudge 0-hit | PASS | grep 0 엄격 확증 |
| (10) 0-hit 샘플링 | PASS | 랜덤 20개 전원 HIT 또는 ES 근거 |

**최종 verdict**: `PASS (severity=observation)`

---

## observation 기재 사항 (수정 권고 — 비차단)

### obs-1: Coder report CJK unique 수치 과소 기재

- Coder report L114: "237 unique CJK tokens"
- Tester 재측정 (`grep -oP '[\x{4e00}-\x{9fff}]+' | sort -u | wc -l`): **306**
- 편차 +69 (+29%). 실측이 **더 많음** → 품질 이슈 아님, report 수치만 정정 권고.

### obs-2: Step 1b 수치 보조 해석 필요

- Coder report L46: "→ 3"
- Tester 재측정 정규식 동일 적용: **7**
- 편차 +4. 실측 7개 = 매크론 3개 (Coder 의도) + §17/§55/§57 + (Émile Durkheim...) 4개.
- Coder가 의도한 "매크론/그리스 핵심 transliteration" 수치 3은 맞지만, 기재한 정규식은 § 섹션·É 포함 토큰도 매칭. 정규식 narrow 또는 수치 7로 정정 권고.

### obs-3: Q9 해설 "원문의 매크론 바이트를 보존" 문구 부정확

- study-guide L500: "본 문항에는 그리스어 트랜스리터레이션 `technē`, `aretē`, `phronēsis`, `bouleusis`, `prohairesis`, `ēthikē`, `eudaimonia`, `mesotēs`, `orexis`, `telos`, `ta pros ta telē`, `bouleutikē orexis` 등이 등장. **원문의 매크론(ē — U+0113, ā — U+0101) 바이트를 보존**."
- **원본 md 실측**: `aretē` 1회 · `technē` 1회만 등장 (원문 L158). 나머지 10개는 study-guide에서 해설 보강용으로 추가.
- **정당성**: aristotle ES claim-002 (중용=메소테)·claim-001 등 근거 존재, 학계 표준 aristotle 용어 → 내용 정당.
- **문제**: "원문의 매크론 바이트를 보존"이라는 표현은 오해 유발. "원문 aretē·technē 보존 + 해설용 매크론 transliteration 추가"로 정확히 기술 권고.

### obs-4: BLOCKER/DQ-020 본문 출현 횟수 Coder report 주장과 실측 편차

- Coder report L158 주장: BLOCKER 18회 · DQ-020 7회
- Tester 실측: BLOCKER 9회 · BLK-175E 10회 · DQ-020 7회
- DQ-020은 정확 재현. BLOCKER는 편차 -9. 기능적 문제 없음 (Q8 BLOCKER 명기 + Q5/Q6 override 이력 표기 정상) — 수치 정정만 권고.

---

## 판정 근거 요약

- 핵심 기능 지표 (문항 12 · 배점 40 · Step1 128 · Step2 33 · 교집합 0 · fudge 0 · DQ-020 override 2명 정상 · zhiyi BLOCKER 유지) **전원 PASS**.
- 체크리스트 (1)~(10) **전수 실측 통과**.
- 0-hit 역-grep 샘플링 **creation·자동 보강 증거 없음** (ES 학계 표준 용어 범위 내 해설 보강).
- observation 4건은 모두 **수치·문구 정확성**에 국한, 본문 내용·구조·verbatim 보존에 영향 없음.
- fudge 0-hit (blocker 위험 부재).

**최종**: `PASS (severity=observation)` — Manager는 observation 4건을 retrospective 또는 후속 fix 태스크로 이월 가능. TASK-204는 DONE 유지.
