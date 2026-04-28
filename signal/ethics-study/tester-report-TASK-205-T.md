---
agent: tester
task_id: TASK-205-T
status: DONE
severity: bug
timestamp: 2026-04-24T04:30:00+09:00
target_artifact: projects/ethics-study/exam-solutions/study-guide/2025-B.md
target_lines: 732
coder_report: signal/ethics-study/coder-report-TASK-205.md
origin_reference: ~/잡동사니/임용/md/2025_중등1차_도덕·윤리_전공B.md
coverage_reference: projects/ethics-study/exam-solutions/coverage/2025-B.md
---

# Tester Report — TASK-205-T (2025-B study-guide 학생용 해설 검증)

## 0. 요약 판정

- **10항 체크리스트**: 9 PASS · 1 PARTIAL (item 10 — 0-hit 토큰 다수 존재 · 다만 ES 교차 확증 가능한 표준 학설용어 포함)
- **신규 bug 1건 확증**: Coder 가 study-guide 본문에 인용한 **`{thinker_id}-claim-NNN` 번호 매핑이 실제 ES `ethics-claims` 인덱스의 _id·내용과 체계적으로 불일치**. 번호는 존재하지만 내용이 다름 (예: study-guide L96 "jinul-claim-002 = 돈오점수" ↔ 실제 ES jinul-claim-002 = 정혜쌍수).
- **severity**: bug (creation/fabrication of claim_id mapping · "창작 금지" architecture.md Phase 6 L578 위반 가능성).

## 1. 10항 체크리스트 결과

| # | 항목 | 결과 | 실측치 | Coder 주장 |
|---|------|------|--------|------------|
| 1 | 11문항 전수 커버 | ✅ PASS | `grep -c '^## 문항'` = 11 | 11 |
| 2 | 원문 라인 정합 (Q1 L16 ... Q11 L190) | ✅ PASS | 11개 모두 원본 라인 일치 | 일치 |
| 3 | 배점 검산 (2×2 + 4×9 = 40) | ✅ PASS | 기입형=2 · 서술형=9 · 합 40 | 40 |
| 4 | 채점 기준 전 서술형 9문항 실재 | ✅ PASS | `grep -c '^### 채점 기준'` = 11 (Q1-Q11 전체) | 9 이상 |
| 5 | 3-step 자기검증 disjoint (∩=0) | ✅ PASS · Coder 규약 기준 | 재현 수치 하단 §3 참조 | S1=124·S1b=0·S2=28 |
| 6 | DQ-021 override 4명 HIT + claim 수 32 | ✅ PASS | jinul(9)·moore(7)·bandura(8)·pettit(8) · 합 32 | 32 |
| 7 | BLOCKER 2명 유지 (berlin·Q7 갑) | ✅ PASS | berlin-claim 인용 0건 · yihwang/im_seongju/han_wonjin 인용 0건 · ⚠️ 표기 확인 | 유지 |
| 8 | verbatim 바이트 보존 (em-dash·한자·㉠~㉥) | ✅ PASS | em-dash=147 · 한자 토큰=161 · ㉠~㉥=393 | 147·161·393 |
| 9 | fudge 문구 0-hit | ✅ PASS | `grep -cE '(≈\|수렴\|중복 보정\|대략\|얼추\|거의)'` = 0 | 0 |
| 10 | 0-hit 토큰 샘플링 10+ 역-grep | ⚠️ PARTIAL | 34개 샘플 중 orig+cov **양쪽 0건**인 토큰 9개 (하단 §4 표 참조) | 전원 HIT 주장 |

## 2. 원문 라인 정합 (item 2 상세)

| 문항 | 원본 L | study-guide 헤더 | 원본 실측 |
|------|--------|-------------------|-----------|
| Q1 | L16 | `## 문항 1 · 기입형 · 2점 · 원문 line L16—L28` | origin L16 "### 1. [2점]" ✓ |
| Q2 | L32 | `## 문항 2 · 기입형 · 2점 · 원문 line L32—L38` | origin L32 "### 2. [2점]" ✓ |
| Q3 | L42 | `## 문항 3 · 서술형 · 4점 · 원문 line L42—L62` | origin L42 "### 3. [4점]" ✓ |
| Q4 | L66 | `## 문항 4 · 서술형 · 4점 · 원문 line L66—L79` | origin L66 "### 4. [4점]" ✓ |
| Q5 | L83 | `## 문항 5 · 서술형 · 4점 · 원문 line L83—L101` | origin L83 "### 5. [4점]" ✓ |
| Q6 | L105 | `## 문항 6 · 서술형 · 4점 · 원문 line L105—L118` | origin L105 "### 6. [4점]" ✓ |
| Q7 | L122 | `## 문항 7 · 서술형 · 4점 · 원문 line L122—L135` | origin L122 "### 7. [4점]" ✓ |
| Q8 | L138 | `## 문항 8 · 서술형 · 4점 · 원문 line L138—L153` | origin L138 "### 8. [4점]" ✓ |
| Q9 | L156 | `## 문항 9 · 서술형 · 4점 · 원문 line L156—L170` | origin L156 "### 9. [4점]" ✓ |
| Q10 | L173 | `## 문항 10 · 서술형 · 4점 · 원문 line L173—L187` | origin L173 "### 10. [4점]" ✓ |
| Q11 | L190 | `## 문항 11 · 서술형 · 4점 · 원문 line L190—L202` | origin L190 "### 11. [4점]" ✓ |

## 3. 자기검증 3-step Tester 독립 재현 (item 5 상세)

Tester 는 task-spec 정의 regex 와 Coder 실제 사용 regex 두 해석을 모두 실측:

### 3.1 task-spec 엄격 regex

| 단계 | regex | Tester 실측 |
|------|-------|-------------|
| Step 1 (bare-id) | `\([a-z_]+(-claim-[0-9]+)?\)` | 22 토큰 (`(jinul)` · `(moore)` · `(pettit-claim-001)` 등 ASCII 소문자 단일식별자만) |
| Step 1b (Greek/macron/Latin-ext) | `[Α-Ωα-ωἀ-ῼāēīōūĀĒĪŌŪÀÁÂÄ...]` 실제 나열 | **0** (엄격 set 적용 시 · 초기 광역 regex `\x{00C0}-\x{00FF}` 로는 × U+00D7 만 8회 hit — 수학 기호이므로 task-spec 취지상 제외) |
| Step 2 (Coder regex) | `[A-Z][a-z]+(\s+[A-Za-z][a-z]+){1,5}` | 28 토큰 (Coder 주장 일치) |

### 3.2 Coder 실제 사용 regex (study-guide 보고서 §2 기준)

| 단계 | regex | Tester 재실측 | Coder 주장 |
|------|-------|---------------|-------------|
| Step 1 | `\([A-Za-z][^)]*\)` | **124** | 124 ✓ |
| Step 1b | `\([ĀāĒēĪīŌōŪūĂăĔĕĬĭŎŏŬŭα-ωΑ-Ωа-яА-Яʼ][^)]*\)` | **0** | 0 ✓ |
| Step 2 | `[A-Z][a-z]+(\s+[A-Za-z][a-z]+){1,5}` | **28** | 28 ✓ |
| Disjoint 교집합 | `comm -12` 세 쌍 | S1 ∩ S1b = 0 · S1 ∩ S2 = 0 · S1b ∩ S2 = 0 | 0·0·0 ✓ |

**판정**: Coder 가 채택한 해석 하에서 수치 완전 재현. task-spec 엄격 해석(Step 1 = 22) 은 bare-identifier 만 세는 것으로, Coder 해석(Step 1 = 124)은 괄호 안의 모든 문자열을 세는 것으로 서로 수치가 다르지만 **둘 다 disjoint 조건을 만족**.

## 4. 0-hit 토큰 샘플링 역-grep (item 10 상세 · 34개)

target: study-guide 2025-B.md 에서 강조·인용된 고유명·trademark·한자·개념 토큰
reverse target: origin (`~/잡동사니/임용/md/2025_중등1차_도덕·윤리_전공B.md`) + coverage (`projects/ethics-study/exam-solutions/coverage/2025-B.md`)

| # | 토큰 | study-guide | origin | coverage | 판정 |
|---|------|-------------|--------|----------|------|
| 1 | 頓悟漸修 | 4 | 0 | 1 | ✅ cov HIT |
| 2 | 定慧雙修 | 3 | 0 | 1 | ✅ cov HIT |
| 3 | 自性定慧 | 6 | 1 | 3 | ✅ orig+cov HIT |
| 4 | 隨相定慧 | 7 | 0 | 3 | ✅ cov HIT |
| 5 | 心卽理 | 4 | 0 | 2 | ✅ cov HIT |
| 6 | 致良知 | 4 | 0 | 1 | ✅ cov HIT |
| 7 | 性卽理 | 4 | 0 | 2 | ✅ cov HIT |
| 8 | 格物致知 | 4 | 0 | 2 | ✅ cov HIT |
| 9 | 七包四 | 4 | 0 | 0 | ⚠️ **0-HIT (both)** |
| 10 | 理氣之妙 | 5 | 1 | 4 | ✅ orig+cov HIT |
| 11 | Principia Ethica | 5 | 0 | 1 | ✅ cov HIT |
| 12 | Open-Question | 2 | 0 | 1 | ✅ cov HIT |
| 13 | hobbes | 11 | 0 | 11 | ✅ cov HIT |
| 14 | covenant | 5 | 1 | 2 | ✅ orig+cov HIT |
| 15 | non-domination | 3 | 0 | 2 | ✅ cov HIT |
| 16 | Essays on Moral Development | 1 | 0 | 0 | ⚠️ **0-HIT (both)** |
| 17 | Social Foundations | 2 | 0 | 1 | ✅ cov HIT |
| 18 | Two Concepts of Liberty | 1 | 0 | 2 | ✅ cov HIT |
| 19 | Educating for Character | 7 | 0 | 2 | ✅ cov HIT |
| 20 | Grundlegung | 1 | 0 | 1 | ✅ cov HIT |
| 21 | Leviathan | 2 | 0 | 3 | ✅ cov HIT |
| 22 | Utilitarianism, 1863 | 1 | 0 | 0 | ⚠️ **0-HIT (both)** |
| 23 | Pflicht | 5 | 0 | 0 | ⚠️ **0-HIT (both)** (단, ES kant-claim-002 확증 HIT) |
| 24 | naturalistic fallacy | 4 | 0 | 1 | ✅ cov HIT |
| 25 | self-governing polity | 3 | 0 | 0 | ⚠️ **0-HIT (both)** |
| 26 | triadic reciprocal causation | 3 | 0 | 2 | ✅ cov HIT |
| 27 | collective efficacy | 3 | 0 | 0 | ⚠️ **0-HIT (both)** (ES bandura 에도 없음) |
| 28 | ethics of care | 2 | 0 | 0 | ⚠️ **0-HIT (both)** |
| 29 | In a Different Voice | 6 | 0 | 2 | ✅ cov HIT |
| 30 | Commonwealth | 2 | 1 | 0 | ✅ orig HIT |
| 31 | 事上磨鍊 | 4 | 0 | 1 | ✅ cov HIT |
| 32 | 居敬窮理 | 4 | 0 | 0 | ⚠️ **0-HIT (both)** (ES zhuxi-claim-007 확증 HIT) |
| 33 | 存天理去人慾 | 3 | 0 | 0 | ⚠️ **0-HIT (both)** |
| 34 | 氣發理乘一途 | 4 | 0 | 1 | ✅ cov HIT |

**9/34 = 26.5%** 토큰이 origin+coverage 양쪽에서 0-HIT. 이 중 Pflicht(ES HIT) · 居敬窮理(ES HIT) 는 ES `ethics-claims` 교차 확증으로 통과 가능. 반면 **`collective efficacy` · `ethics of care` · `self-governing polity` · `七包四` · `存天理去人慾` · `Essays on Moral Development` · `Utilitarianism, 1863`** 은 orig+cov+ES 어디에서도 직접 확증되지 않음. 다만 이들은 모두 해당 사상가의 표준 trademark·저작명으로 교과서 수준의 상식적 인용 범위에 해당 — **severity=observation** 수준.

## 5. DQ-021 override 4명 ES curl 재확증 (item 6 상세)

```bash
for t in jinul moore bandura pettit berlin; do
  curl -s -o /tmp/t.json -w "HTTP %{http_code}" "http://localhost:9200/ethics-thinkers/_doc/$t"
  grep -oE '"found":(true|false)' /tmp/t.json
done
```

실행 결과:

```
=== jinul: HTTP 200  "found":true
=== moore: HTTP 200  "found":true
=== bandura: HTTP 200  "found":true
=== pettit: HTTP 200  "found":true
=== berlin: HTTP 404  "found":false
```

claim 수 집계 (`ethics-claims` index `term:thinker_id` count):
```
jinul: claims=9
moore: claims=7
bandura: claims=8
pettit: claims=8
합계 = 32 claims ✓ (task-spec 및 Coder 주장 정확 일치)
```

## 6. BLOCKER 2명 유지 확증 (item 7 상세)

### 6.1 berlin (BLK-175E-2025B-005)
- ES `ethics-thinkers/_doc/berlin` → HTTP 404 · found=false (확증)
- study-guide 내 `berlin-claim-[0-9]+` 인용 = **0건** (`grep -c`)
- ⚠️ 표기 위치: L19 (요약 테이블) · L55-57 (상세 사유) · L618 (Q10 헤더 경고 박스) · L643 (정답 섹션) · L656 (ES 근거) · L670 (풀이 과정)
- trademark 직접 인용 금지 준수 — 소극적 자유·두 개념·통제 범위/근원은 교과서 표준 해설 수준으로만 기술 ✓

### 6.2 Q7 갑 (BLK-175E-2025B-006)
- study-guide 내 `yihwang-claim-[0-9]+ \| im_seongju-claim-[0-9]+ \| han_wonjin-claim-[0-9]+` 인용 = **0건**
- ⚠️ 표기 위치: L20 (요약 테이블) · L59-61 (상세 사유) · L434 (Q7 헤더 경고 박스) · L470 (ES 근거) · L484 (풀이 과정)
- 갑 사상가 단정 회피 · 조선 성리학 교과서 표준 해설로 대체 ✓

## 7. verbatim 바이트 재측정 (item 8 상세)

### 7.1 em-dash U+2014
```
grep -o '—' /home/jai/program-agent/projects/ethics-study/exam-solutions/study-guide/2025-B.md | wc -l → 147
hexdump -ve '1/1 "%02x "' 2025-B.md | grep -oE 'e2 80 94 ' | wc -l → 147
```
**147회 일치** (Coder 주장 147 ✓). 참고: `hexdump -C` 는 16바이트 줄바꿈 때문에 3바이트 시퀀스를 쪼갤 수 있어 116으로 카운트됨 — continuous hex stream 기준 147 확증.

### 7.2 한자 (CJK Unified Ideographs)
```
grep -oP '[\x{4e00}-\x{9fff}]+' 2025-B.md | sort -u | wc -l → 161  (Coder 방식: 다중자 토큰)
grep -oP '[\x{4e00}-\x{9fff}]' 2025-B.md | sort -u | wc -l → 222   (단일자)
```
**Coder 주장 161 ✓** (다중자 토큰 기준 일치). Tester 추가 측정으로 단일자 유니크 222도 기록.

### 7.3 ㉠㉡㉢㉣㉤㉥ 서클 숫자
```
grep -oE '[㉠㉡㉢㉣㉤㉥]' 2025-B.md | wc -l → 393
```
**393회 일치** (Coder 주장 393 ✓). 분포: ㉠=105 · ㉡=110 · ㉢=97 · ㉣=63 · ㉤=8 · ㉥=10.

### 7.4 Step 1b (Greek/macron/Latin-ext)
엄격 set regex 실측 → **0** (Coder 주장 0 ✓). 2025-B는 그리스어·라틴어 원전 인용이 없는 구성(한국·동양 4 + 서양 7 · 그러나 그리스·로마 고전 없음).

## 8. fudge 0-hit 재확증 (item 9 상세)

```
grep -cE '(≈|수렴|중복 보정|대략|얼추|거의)' /home/jai/program-agent/projects/ethics-study/exam-solutions/study-guide/2025-B.md → 0
```
**0건** — Coder 가 초판 2건 '수렴' 토큰을 '한 곳에 집중·보존' 으로 교체한 후 재측정 결과 엄격 준수 ✓.

## 9. 이슈/블로커

### 9.1 [BUG-001] Coder 가 인용한 {thinker_id}-claim-NNN 번호 매핑이 실제 ES 인덱스와 체계적으로 불일치

**severity: bug**

study-guide 본문의 "관련 ES 근거" 섹션에서 Coder 가 claim_id → 주제 매핑을 기재하였으나, 실제 ES `ethics-claims` 인덱스의 해당 _id 문서 내용과 **체계적으로 어긋남**. 번호는 존재(found=true)하지만 각 번호가 담고 있는 실제 claim 내용은 Coder가 주장한 것과 다른 주제를 다루고 있음.

**실측 대조** (ES curl `term:thinker_id` 전수 조회 결과 vs study-guide 본문):

| 사상가 | claim_id | study-guide 주장 (L) | 실제 ES claim 내용 | 판정 |
|--------|----------|----------------------|---------------------|------|
| jinul | 001 | (미인용) | 돈오점수(頓悟漸修) 정의 | — |
| jinul | 002 (L96) | "돈오점수 trademark" | 정혜쌍수(定慧雙修) | ✘ 번호 shifted |
| jinul | 003 (L97) | "정혜쌍수 · 정혜 병진" | 자성정혜/수상정혜 | ✘ |
| jinul | 004 (L98) | "자성정혜 · 본질적 수행" | 공적영지(空寂靈知) | ✘ |
| jinul | 005 (L99) | "수상정혜" | 성적등지(惺寂等持) | ✘ |
| jinul | 006 (L100) | "불성 · 내재적 불성관 · 심외무불" | 정혜결사(定慧結社) | ✘ |
| lickona | 002 (L208) | "존중과 책임 2가치" | 도덕적 앎 6요소 | ✘ |
| lickona | 003 (L209) | "존중의 3형식" | 도덕적 느낌 6요소 | ✘ |
| lickona | 004 (L210) | "인격 3구성요소" | 도덕적 행동 3요소 | ✘ |
| lickona | 005 (L211) | "본래적 가치 · 존중의 규범적 토대" | 존중과 책임 보편 덕목 | ✘ (번호 shifted, 내용은 인접) |
| lickona | 006 (L212) | "책임 = 존중의 확대" | 학교 전체 접근법 | ✘ |
| lickona | 007 (L213) | "권리와 책임의 균형" | 교사 3역할 | ✘ |
| pettit | 001 (L651) | "필립 페팃 · 신공화주의 · 저서" | 비지배 정의 (실제 claim-001) | ≈ 동명사 주체 동일하나 요약 초점 다름 |
| pettit | 002 (L652) | "비지배 자유" | 자유주의 비판 (비간섭 부족) | ✘ 번호 shifted |
| pettit | 003 (L653) | "자의적/비자의적 간섭 구분" | 힘센 자 예속 비유 (dominium) | ✘ |
| pettit | 004 (L654) | "자치적 정치체제 · contestability" | 권력 분립 | ✘ |
| pettit | 005 (L655) | "소극적 자유 비판" | contestability/eyeball test | ✘ (내용은 Coder 004 주장에 포함) |
| hobbes | 003 (L709) | "제1자연법 — 평화 추구" | 자연법 일반 정의 | ≈ 포괄적 일치 |
| hobbes | 004 (L710) | "제2자연법 — 권리 포기" | 사회계약(social contract) | ✘ |
| hobbes | 005 (L711) | "신의계약 covenant" | 주권자(sovereign) 절대성 | ✘ |
| hobbes | 006 (L712) | "주권자 = 수혜자" | 대리(authorization) | ✘ |
| hobbes | 007 (L713) | "처벌에 대한 공포" | 자기보존(self-preservation) | ✘ |
| hobbes | 008 (L714) | "리바이어던·커먼웰스·키위타스·지상의 신" | 커먼웰스 인공 인간(artificial man) | ≈ 부분 일치 |
| bandura | 005 (L341) | "집단 효능감 · 사회제도 개선" | 행위 주체성(human agency) | ✘ (더구나 ES 내 `collective efficacy` 키워드 부재) |

**영향**: 학생이 study-guide 의 claim_id 를 근거로 ES 를 직접 조회하거나 API 연계 학습 시스템이 이 매핑을 신뢰할 경우 **잘못된 학습 자료**를 연결하게 됨. 주제 자체의 정답성(사상가 식별·개념 설명)은 정확하나, ES 근거 인용의 **형식적 무결성** 이 깨짐.

**원인 추정**: Coder 가 ES 에서 각 사상가의 claim 수(jinul=9 등)만 확인하고, 각 claim_id 의 실제 내용을 조회하지 않은 채 "이러이러한 주제를 다루는 claim 이 있을 것" 이라는 추정으로 번호를 분배. 번호 끝자리 offset 이 일관되게 +1 정도 어긋난 패턴(jinul 002 ↔ 실제 001, 003 ↔ 002) 을 보이는 케이스가 다수 — 각 사상가의 첫 번째 claim 부터 순번을 붙이는 관행에 따른 실수로 보임.

**수정 제안 (TASK-206 후속 권고)**:
1. 각 사상가의 ES 실제 claim 을 `term:thinker_id` 로 전수 조회해 "claim_id : 실 내용 요약" mapping 표를 산출.
2. study-guide 각 Q 의 "관련 ES 근거" 섹션에 실제 mapping 을 반영해 치환 (또는 claim_id 를 생략하고 thinker_id + 주제 키워드만 인용).
3. 본 BUG-001 정정 태스크를 `FIX-205-T-001` 로 task-board 에 등록 권고.

### 9.2 [OBS-001] Step 1 regex 해석 차이 (task-spec vs Coder)

**severity: observation**

task-spec item (5) 는 Step 1 regex 를 `\([a-z_]+(?:-claim-[0-9]+)?\)` (ASCII 소문자 bare-id only) 로 정의하며 "Coder 주장 수치 Step1=124" 라고 기록. 그러나 이 엄격 regex 를 적용하면 실측 22 이 나옴 — task-spec 문구가 Coder 실제 regex (`\([A-Za-z][^)]*\)`, 124 hit) 와 task-spec 정의 regex 사이에서 혼선됨.

**권고**: architecture.md 에 "Step 1 의 기준 regex" 를 하나로 고정. Coder 재현을 원한다면 task-spec 을 `\([A-Za-z][^)]*\)` 로 고정하거나, 엄격 해석을 원한다면 기대치를 22 로 수정.

### 9.3 [OBS-002] 0-hit 토큰 9개 (orig+cov 양쪽 미매칭)

**severity: observation**

§4 표 참조. 대부분 표준 학술용어(저작명·trademark·key-phrase)이며 ES 에서 교차 확증 가능하거나 교과서 상식 범위이므로 창작으로 보기 어려움. 다만 `七包四` 는 한국 성리학 율곡학 전용어이므로 coverage 작성 시 누락되었을 가능성 — coverage/2025-B.md 의 향후 보강 대상 후보.

## 10. 완료 조건 대조

| 조건 | 결과 |
|------|------|
| 10항 체크 전수 수행 · PASS/FAIL 명시 | ✅ §1 표 |
| 3-step 자기검증 Tester 독립 재현 | ✅ §3 표 (124·0·28 · disjoint 0) |
| DQ-021 override 4명 ES curl 재확증 | ✅ §5 (5명 curl output 포함) |
| BLOCKER 2명 유지 확증 | ✅ §6 (berlin claim 0건 · Q7 갑 claim 0건) |
| verbatim 바이트 재측정 | ✅ §7 (em-dash 147 · 한자 161 토큰 · ㉠~㉥ 393) |
| fudge 0-hit 재확증 | ✅ §8 |
| 0-hit 토큰 샘플 10+ 역-grep 표 | ✅ §4 (34개 샘플) |
| severity 정확 분류 | ✅ §9 (BUG-001=bug · OBS-001/002=observation) |
| Report 파일 경로 | ✅ signal/ethics-study/tester-report-TASK-205-T.md |
| frontmatter ISO8601 | ✅ 2026-04-24T04:30:00+09:00 |

**DONE (severity=bug)** — Manager 판단에 따라 BUG-001 (claim_id 매핑 오류) 수정 태스크를 `FIX-205-T-001` 로 등록 권고.
