---
task_id: TASK-206
verdict: NEEDS_REVISION
---

# Reviewer Report: TASK-206

## 검증 대상
- 파일:
  - `signal/ethics-study/task-board.md` L361 (TASK-206 행)
  - `signal/ethics-study/task-board.md` L360 (TASK-DQ-023 행 · Depends On 선행)
  - `signal/ethics-study/task-board.md` L362 (TASK-205-FIX-T 행 · Depends On 선행)
  - `signal/ethics-study/architecture.md` (동명이인 suffix 규약 근거)
  - `signal/ethics-study/data-quality-log.md` L335-L377 (DQ-023 entry)
  - `projects/ethics-study/exam-solutions/coverage/2026-A.md` (842L · 입력 원천)
  - `~/잡동사니/임용/md/2026_중등1차_도덕·윤리_전공A.md` (215L · 원문 기출)
  - `projects/ethics-study/exam-solutions/study-guide/2026-A.md` (산출 대상 · 미존재)
- Manager 주장 요약: (A) 파일 실측 라인 수·원문 Q 헤더 라인, (B) ES 실측 (14 HIT + 1 BLK), (C) 문항별 사상가 매핑, (D) TASK-205-FIX 선례 선반영, (E) TASK-DQ-023·TASK-205-FIX-T 의존성, (F) 동명이인 suffix 규약, (G) 3-step 자기검증·fudge 금지·verbatim 바이트.

## 검증 결과

### 파일 존재

| 경로 | 존재 | 비고 |
|------|------|------|
| `projects/ethics-study/exam-solutions/coverage/2026-A.md` | YES | wc -l == 842 (주장 842L 일치) |
| `~/잡동사니/임용/md/2026_중등1차_도덕·윤리_전공A.md` | YES | wc -l == 215 (주장 215L 일치) |
| `projects/ethics-study/exam-solutions/study-guide/2026-A.md` | NO (정상 · 신규 작성 대상) | ls 에러 `No such file` 확인 |
| `projects/ethics-study/exam-solutions/study-guide/2024-B.md`·`2025-A.md`·`2025-B.md` | YES | 선례 (TASK-182~205) 참조 가능 |
| `signal/ethics-study/data-quality-log.md` L335 DQ-023 entry | YES | 347-349 override 3건 · 377 원본 금지 규정 기재 |

### 내용 일치

**(A) 원천 파일 실측 — 대체로 PASS, 세부 오기 1건**
- coverage/2026-A.md: 주장 842L → 실측 `wc -l == 842`. **PASS**
- 원문 md: 주장 215L → 실측 `wc -l == 215`. **PASS**
- 12문항 구조 (기입형 4 × 2점 + 서술형 8 × 4점 = 40점): coverage L663-L678 요약 테이블 및 원문 `### N. [n점]` 헤더 전수 확인. **PASS**
- 원문 Q 헤더 라인 12/12 전수 일치 (Q1=L16·Q2=L30·Q3=L44·Q4=L58·Q5=L72·Q6=L90·Q7=L107·Q8=L122·Q9=L140·Q10=L156·Q11=L177·Q12=L198). grep 실측 근거:
  ```
  16:### 1. [2점]  30:### 2.  44:### 3.  58:### 4.
  72:### 5.  90:### 6.  107:### 7.  122:### 8.
  140:### 9.  156:### 10.  177:### 11.  198:### 12.
  ```
  **PASS**

**(B) ES 실측 — 전수 PASS**
curl loop 재실측 결과 (2026-04-24 현재):
```
cho_sik thinker=404 claims=0     <-- BLK 유지 일치
turiel thinker=200 claims=8      <-- DQ-023 override 주장 일치
taylor_p thinker=200 claims=8    <-- DQ-023 override 주장 일치
leopold thinker=200 claims=7     <-- DQ-023 override 주장 일치
aquinas thinker=200 claims=10
galtung thinker=200 claims=8
noddings thinker=200 claims=12
haidt thinker=200 claims=10
rawls thinker=200 claims=15
kant thinker=200 claims=18
buddha thinker=200 claims=10
confucius thinker=200 claims=17
laozi thinker=200 claims=12
xunzi thinker=200 claims=11
aristotle thinker=200 claims=12
```
주장 claims 수치 15/15 전수 일치. HIT 14 (11 original + 3 DQ override) + BLK 1 (cho_sik) 합계 15 thinker. **PASS**

**(C) 문항별 사상가 매핑 — coverage 요약 테이블 대조 PASS**
coverage L664-L678 summary table 과 L700-L717 ES dump table 대조:
- Q1 [교과교육학] N/A · Q2 aquinas · Q3 cho_sik (BLK) · Q4 galtung · Q5 noddings · Q6 turiel+haidt · Q7 rawls · Q8 kant · Q9 buddha · Q10 confucius+laozi+xunzi · Q11 aristotle · Q12 taylor_p+leopold — 모두 coverage 와 일치. **PASS**
- Q4 "병" 역할: Manager spec "갑·을 민족공동체 통일방안은 교과교육학 공존 문항, galtung=병" 은 coverage L667 ("Q4 현대 평화학 galtung") 및 L703 갑=MOE 교과교육학, 을=MOE 교과교육학, 병=galtung 의 일반 구조와 일치. **PASS**

**(D) TASK-205-FIX 선례 선반영 — 실제 grep 확증 PASS**
TASK-206 본문(task-board.md L361)에 다음 문구 전수 존재:
- "ES mapping 필수 산출물 (TASK-205-FIX 선례 선반영)" 문구 존재
- "key-phrase 3+ overlap" 문구 존재
- "DQ-022 패턴 선제 점검" 문구 존재
- "bash loop 으로 전원 found=true 확증" 문구 존재
- "ES 부재 개념 처리 우선순위: (a) 1순위 인접 claim_id 재서술 · (b) 2순위 claim_id 인용 생략 thinker_id 만 유지 · (c) 금지 존재하지 않는 claim_id 유지" 전수 기재
- "Coder report 에 ES mapping table (14 HIT thinker × 인용 claim · content 요약 40자 · keywords 상위 3)" 수록 요구 기재
- **PASS**

**(E) 선행 의존성 — PASS**
- TASK-205-FIX-T (L362): status 열 `DONE (PASS severity=observation · 10/10 PASS · 84 claim_id 전원 found=true · DQ-022 mill_js→mill 치환 확증 · §9.1 BUG-001 7건 spot-check 전원 content match · kant "신성한 의지" drop 타당 · section-wise breakdown MERGED VERBATIM ±0 · 3-step ∩=0 · fudge 0)`. **DONE PASS 확증**
- TASK-DQ-023 (L360): status 열 `DONE (2026-04-24T18:05 · data-quality-log.md DQ-023 entry append 완료 · 3 FOUND override turiel/taylor_p/leopold 23 claims · 1 NOT_FOUND cho_sik thinker=404 claims=0)`. **DONE 확증**
- data-quality-log.md L335 DQ-023 entry 실존 (override 3건 table L347-L349). **PASS**
- TASK-206 Depends On 열 == `TASK-205-FIX-T · TASK-DQ-023` 일치. **PASS**

**(F) 동명이인 suffix 규약 — 라인 번호 오기재 (FAIL)**
- Manager 주장: `architecture.md:491` 에 taylor vs taylor_p 규약 근거.
- 실측: `grep -n "taylor_p\|동명이인 suffix"` → **L540** 에 해당 문장. `L491` 에는 "도덕·윤리 전공 A/B 파일 내에도 교과교육학 문항이 섞여 있다 …" 교과교육학 분류 규칙이 있을 뿐 동명이인 규약과 무관.
- task-board.md L361 본문에 `architecture.md:491` 이 **2회** 인용됨 (Q12 taylor_p 항 및 마지막 "동명이인 suffix 규약 (taylor vs taylor_p 엄격 구분 · architecture.md:491)" 문구). 두 곳 모두 **실측 오기재**.
- 영향: Coder 가 architecture.md:491 를 열면 무관한 분류 규칙을 읽게 되어 suffix 규약 혼선. Low-severity 지만 Manager 의 "실측 인용 의무" (CLAUDE.md) 위반.
- **FAIL — 수정 필요**

**(G) 3-step 자기검증 + fudge 금지 + verbatim 바이트 규칙 — PASS**
task-board.md L361 본문에 다음 전수 명시 확인:
- "3-step 자기검증 (Step1 bare-paren + Step1b Greek/macron/Latin-ext/German + Step2 TitleCase) + disjoint 산술 (∩=0)"
- "fudge 문구 절대 금지 (≈·수렴·중복 보정·대략·얼추·거의)"
- "verbatim 바이트 보존 (em-dash U+2014 · ㉠㉡㉢㉣ · 甲/乙 없음 갑/을/병 한글만 · 한자 … 그리스어 없음 · 독일어 Zum ewigen Frieden·Friedensbund·Weltbürgerrecht·Besuchsrecht 포함)"
- **PASS**

### 태스크 완결성 — 일부 라인 범위 오기 (FAIL)

Q 별 원문 라인 범위를 `---` sep 기준 실측하면:

| Q | spec 범위 | 실측 본문 범위 | sep 위치 | 판정 |
|---|---|---|---|---|
| Q1 | L16-L28 | L16-L27 (sep L28) | L28 | spec 가 sep 포함, minor |
| Q2 | L30-L40 | L30-L41 (sep L42) | L42 | ✓ |
| Q3 | L44-L54 | L44-L55 (sep L56) | L56 | ✓ |
| Q4 | L58-L68 | L58-L69 (sep L70) | L70 | ✓ |
| Q5 | L72-L86 | L72-L87 (sep L88) | L88 | ✓ |
| Q6 | L90-L105 | L90-L103 (sep L105) | L105 | spec 가 sep **까지** 포함 (L104 빈줄 · L105 sep), minor |
| Q7 | L107-L118 | L107-L119 (sep L120) | L120 | ✓ |
| Q8 | L122-L136 | L122-L137 (sep L138) | L138 | ✓ |
| Q9 | L140-L152 | L140-L153 (sep L154) | L154 | ✓ |
| Q10 | **L156-L169** | **L156-L173** (sep L175) | L175 | **spec 범위가 4 줄 부족 — Q10 <작성 방법> 2 bullet (L172-L173) 누락** |
| Q11 | L177-L194 | L177-L195 (sep L196) | L196 | ✓ |
| Q12 | L198-L211 | L198-L212 (sep L213) | L213 | ✓ |

**Q10 L170-L173 실측 내용** (Manager spec 이 누락한 구간):
```
L170: **<작성 방법>**
L171:
L172: - 괄호 안에 공통으로 들어갈 용어를 쓸 것.
L173: - 밑줄 친 '이름[名]'에 관한 갑, 을, 병의 핵심 주장을 순서대로 서술할 것. 단, <보기>의 개념들을 사상가마다 2개씩, 중복되지 않게 사용할 것.
```
특히 L173 의 "**<보기>의 개념들을 사상가마다 2개씩, 중복되지 않게 사용할 것**" 제약은 Q10 채점 기준의 핵심(정명·무명·귀천·동이·의무·상대 6개 개념 분배 규칙)이어서, verbatim 범위에서 누락되면 Coder 가 `### 채점 기준` 작성 시 이 제약을 반영하지 못할 위험. **severity=bug 수준 오기**.

Q6 spec L90-L105 는 sep 자체를 범위에 포함 → verbatim 인용 시 `---` 라인 포함 여부 모호. TASK-204 (2025-A) 선례가 sep 제외 관행이라면 여기도 L90-L103 으로 맞추는 것이 일관. **minor** 지만 바이트 보존 원칙상 명시 권고.

Q1 L16-L28 역시 sep 라인 포함 → L16-L27 로 교정 권장. **minor**.

### 의존성·순서
- TASK-205-FIX-T DONE PASS + TASK-DQ-023 DONE 확증 (L362·L360).
- Depends On 열 일치. **PASS**
- 같은 파일 (2026-A.md 신규) 을 수정하는 병렬 태스크 없음 (단독 실행).

## 판정
**NEEDS_REVISION**

3개 수정 항목 (각각 독립적이므로 일괄 수정 가능):
1. **architecture.md:491 라인 오기** (2회 인용) — 실측 L540 로 교정.
2. **Q10 원문 라인 범위 L156-L169 → L156-L173** — <작성 방법> 2 bullet 누락 방지.
3. (권고) **Q1·Q6 sep 라인 포함 여부 명시** — "verbatim 범위는 `---` sep 라인 제외" 원칙을 TASK-206 본문에 한 줄 추가하거나 Q1=L16-L27, Q6=L90-L103 로 sep 제외 표기.

이 3건은 모두 Coder 의 산출물 품질에 직결되며, 특히 (1)(2) 는 CLAUDE.md "실측 인용 의무 — 실측 없이 적은 숫자는 Reviewer 가 NEEDS_REVISION 으로 돌려보낸다" 규정에 정확히 해당.

다른 모든 검증 (A/B/C/D/E/G + 태스크 완결성·의존성·순서·목적성) 은 전수 PASS — Q10 라인 범위와 architecture.md 라인 오기 2건만 수정되면 즉시 재검 PASS 가능 수준.

## 수정 요청 (NEEDS_REVISION)

1. `signal/ethics-study/task-board.md` L361 내 `architecture.md:491` 2 건을 **`architecture.md:540`** 으로 치환.
   - 위치 1: Q12 taylor_p 항 `**동명이인 suffix 규약 엄수: taylor=Charles Taylor 공동체주의 / taylor_p=Paul W. Taylor 환경윤리 · architecture.md:491**`
   - 위치 2: 말미 `**동명이인 suffix 규약** (taylor vs taylor_p 엄격 구분 · architecture.md:491)`
   - 실측 근거: `grep -n "taylor_p" signal/ethics-study/architecture.md` → `540:- 동명이인 후보가 있으면 ES에서 사전 조회하여 suffix 필요 여부를 결정. 예: taylor (Charles Taylor, 공동체주의) vs taylor_p (Paul Taylor, 생명중심주의) — 별개 인물.`

2. `signal/ethics-study/task-board.md` L361 내 Q10 라인 범위를 **L156-L169 → L156-L173** 로 확장.
   - 해당 문구: `**Q10 (서술형 4점·L156-L169)**` 를 `**Q10 (서술형 4점·L156-L173)**` 로 교정.
   - 이유: 원문 L170 `**<작성 방법>**`, L172-L173 bullet 2 건 (특히 "<보기> 개념 사상가마다 2개씩 중복 없이") 이 Q10 채점 기준 작성에 필수.
   - 실측 근거: sep `---` 위치 L175. Manager 의 다른 Q 의 범위 규칙(본문 끝 라인까지, sep 제외)과 일관되게 적용하면 L156-L173.

3. (권고 · 선택) 본문에 "**verbatim 범위의 L{m}-L{n} 는 `---` sep 라인을 제외한 본문 라인**" 한 문장 추가하거나, Q1=L16-L27, Q6=L90-L103 으로 sep 제외 표기 통일. 이 항목은 PASS/FAIL 경계 외이지만, 1 과 2 교정 시 함께 반영하면 "바이트 보존" 규정과 일관.

## Manager에게 전달

수정 완료 후 Reviewer 재호출. 수정 범위가 task-board.md L361 내부 문자열 치환 3 곳(위 1 의 2 건 + 위 2 의 1 건 · 권고 3 제외)에 국한되어 재검증은 해당 라인 재-grep 으로 빠르게 PASS 판정 가능. 본 report 의 (A)(B)(C)(D)(E)(G) 검증은 재실행 불필요 (상태 변동 없음 확인됨). Coder 발주는 위 3 건 교정 → Reviewer PASS 확정 후에만 진행.
