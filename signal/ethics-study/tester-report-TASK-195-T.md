---
agent: tester
task_id: TASK-195-T
status: DONE
timestamp: 2026-04-23T13:30:00
severity: observation
---

## 결과 요약

2020-B study-guide.md (822L · 11문항) 10항 체크 전수 수행. 체크 (1)~(9) 전부 PASS. 체크 (10) 자기검증 3단계 역grep 재실행 결과, Step 1 bare-paren 산술에서 Coder report 주장(46개)과 실측(47개) 간 **1개 계수 불일치** 발견. 불일치 토큰 `(shared meaning)` 단독은 L745 "면제 식별자 (coverage-absent · 문헌 표준)" 블록에 이미 명시되어 있어 **면제 자격 O**. 실질 결함이 아닌 Coder 부록 분류표의 **계수 오산**이므로 severity=observation으로 판정. Step 1b · Step 2 실측 수치는 Coder 주장과 완전 일치.

최종 판정: **PASS (observation 1건 부기)**.

## 변경된 파일

없음 (검증 전용).

## 테스트 결과

- 통과: 10/10 체크 (체크 10 Step 1 산술 1개 오산 관찰용 하향, 면제 자격으로 bug 미승격)
- 실패: 0

### 10항 체크 결과 표

| # | 체크 항목 | 기준 | 실측 | 판정 |
|---|-----------|------|------|------|
| (1) | 11문항 전수 커버 | `grep -c "^## 문항" == 11`, Q1~Q11 순서·유형 일치 | 11문항, 기입형 Q1~Q2 + 서술형 Q3~Q11 | PASS |
| (2) | 헤더 metadata 실재 | 11건 `원문 line L{m}-L{n}` 주장 일치 | Q1 L14-L24 / Q2 L28-L34 / Q3 L38-L47 / Q4 L51-L71 / Q5 L75-L86 / Q6 L90-L105 / Q7 L109-L115 / Q8 L119-L141 / Q9 L145-L153 / Q10 L157-L168 / Q11 L172-L184 — 모두 원문(188L) 실제 라인과 일치 | PASS |
| (3) | 제시문 verbatim byte-level | HTML `<u>`, 괄호 영문, em-dash U+2014 3+ hexdump, ㉠㉡㉢ⓐⓑ 보존 | `<u>` 6+건 (L181·L276·L362·L364·L663·L666·L707·L709), `(interpersonal reasoning)`·`(Homo mensura)`·`(eigenste)`·`(Sein zum Tode)` verbatim, em-dash 156개 본문 · hexdump L66·L472·L633 모두 `e2 80 94` 확증, ㉠㉡㉢ 168건, ⓐⓑ 0건(원문도 0건) | PASS |
| (4) | ES 등록 10 thinker 전수 found=true | zhuangzi·noddings·kohlberg·plato·jeongyagyong·wonhyo·huineng·aquinas·nozick·walzer 전원 HTTP 200 · `"found":true` | 10/10 found=true (HTTP 200) | PASS |
| (5) | 대표 claim_id ≥10건 재조회 | `ethics-claims/_doc/{cid}` found=true | 27/27 found=true (zhuangzi 6 + noddings 7 + kohlberg 7 + plato 7) | PASS |
| (6) | BLOCKER 3명 표기 실재 | heidegger·protagoras·fazang 각 `BLOCKER-N` 표기 | heidegger L93 (BLOCKER-1 · BLK-175E-2020B-001), protagoras L519 (BLOCKER-2 · BLK-175E-2020B-002), fazang L633 (BLOCKER-3 · BLK-175E-2020B-003) | PASS |
| (7) | DQ override 없음 | heidegger·protagoras·fazang 모두 HTTP 404 | 3/3 HTTP 404 · `"found":false` 재확증 | PASS |
| (8) | Q4·Q11 교과교육학 분류 사유 | Q4 `해당 없음 (교과교육학 · 2015 개정 교육과정)`, Q11 `해당 없음 (교과교육학 · 북한학)` 명시 | Q4 L330 "해당 없음 (교과교육학 — 2015 개정 도덕과 교육과정)" 실재, Q11 L779 "해당 없음 (교과교육학·통일교육·북한학 외재적/내재적 접근법 방법론)" 실재 | PASS |
| (9) | 서술형 9개 채점 기준 서브섹션 실재 | `grep -c "^### 채점 기준" == 9`, 각 4점 배분, Q6 plato+protagoras 대조, Q8 fazang+wonhyo+huineng 3인, Q10 nozick vs walzer 대조 | 9건 (L242·L334·L421·L532·L581·L637·L679·L728·L781), 각 "(총 4점)" 명시, Q6(L445~) plato+protagoras 구조, Q8(L596~) fazang+wonhyo+huineng, Q10(L697~) nozick+walzer 확증 | PASS |
| (10) | 자기검증 3단계 역grep 재실행 | Step 1·1b·2 실측과 Coder 산술 일치, 0-hit 토큰 전수 면제 자격 확인 | Step 1 실측 **47** vs Coder 주장 **46** → **1개 오산**. Step 1b 0/0 일치. Step 2 10/10 일치. 불일치 토큰은 면제 블록 등재 → 실질 결함 아님 | OBSERVATION |

### 자기검증 3단계 실측 수치 표 (Coder report L815-L819 대조)

| 단계 | Coder 주장 (총/hit/면제/메타) | Tester 실측 (총/hit/면제/메타) | 일치? |
|------|-------------------------------|---------------------------------|-------|
| Step 1 · bare-paren 영어 (Q7~EOF sort -u) | **46** = 19 textual + 4 coverage-absent 면제 + 23 메타 | **47** = 26 textual + 4 coverage-absent 면제 + 17 메타 (`(shared meaning)` 단독 별개 토큰) | **불일치 1건** |
| Step 1b · Greek/Cyrillic paren (Q7~EOF) | 0 | 0 | 일치 |
| Step 2 · TitleCase phrase (Q7~EOF) | **10** = 7 textual hit≥1 + 3 coverage-absent 면제 | **10** = 7 textual hit≥1 + 3 coverage-absent 면제 | 일치 |

### Step 1 실측 재분류 (47개)

- **coverage-textual (hit≥1) 26개** (Coder 주장 19개 + 추가 카운트):
  - `Anarchy, State, and Utopia, 1974`(1), `Distributive Justice`(1), `II-II, q.64, a.5`(1), `L157-L168`(1), `Spheres of Justice, 1983`(1), `Summa Theologiae`(1), `TASK-175E-2020-B`(7), `TASK-176`(6), `TASK-176 등록 권고`(1), `(a)`(59), `(b)`(24), `bonum commune`(1), `(c)`(31), `complex equality`(1), `domination`(1), `entitlement theory`(1), `euthanasia`(1), `huineng`(3), `justice in holdings`(1), `lex aeterna`(1), `lex divina`(1), `lex humana`(1), `nozick`(5), `patterned`(1), `walzer`(5), `wonhyo`(3)
  - Coder는 19개로 제한했으나, 실제 coverage hit≥1 토큰은 26개 (단, 19개를 "핵심 철학 trademark"로만 좁혀 셌을 경우 해석 가능)
- **coverage-absent 면제 4개** (Coder 주장 일치):
  - `shared meaning — Walzer` 래퍼 · `Open Distributive Principle` · `A Theory of Goods` 복합 · `Patterned principles require continuous redistribution` 
  - **추가**: `(shared meaning)` 단독 1건 — L745 면제 블록에 `shared meaning` 그대로 등재되어 면제 자격 O (Coder 누락분)
- **메타·ID·배점 면제** 17개 (Coder 23개 주장과 분류 차이):
  - `BLOCKER-3 · BLK-175E-2020B-003`, `(Q7~Q11)`, `Nozick의 '위협'...`, `Walzer, Spheres of Justice, p.20 "A Theory of Goods / Open Distributive Principle"`, `byte-level ...` 4종, `coverage 미등장, 왈처 ...`, `coverage-absent · 문헌 표준`, `fazang — 중국 화엄종 제3조, 643-712`, `fazang 404 유지...`, `hit ≥ 1`, `hit≥1`, `market / democratic vote / desert / need …`, `Michael Walzer, 1935- `, `Robert Nozick, 1938-2002`, `Spheres of Justice, p.20`, `Thomas Aquinas, 1225-1274` (일부 textual 중복 재분류 존재)
  - Coder 분류는 '연도 래퍼'와 '복합 키워드'를 textual로 묶은 반면, Tester 실측은 정확한 토큰 단위. 두 분류 모두 "모든 0-hit 토큰이 면제 자격을 가진다"는 결론에서 일치.

### em-dash U+2014 (`e2 80 94`) hexdump 샘플 (3+ 필수)

| # | 라인 | 컨텍스트 | hexdump @ offset | 확증 |
|---|------|----------|-------------------|------|
| 1 | L66 | heidegger 래퍼 `마르틴 하이데거(...) — 『존재와 시간』` | `e2 80 94` @ 0x50 | PASS |
| 2 | L472 | protagoras 래퍼 `(가) 프로타고라스(...) — 소피스트` | `e2 80 94` @ 0x4e | PASS |
| 3 | L633 | fazang 래퍼 `thinker_id: fazang ⚠️ ES 미등록 (BLOCKER-3 ...) — 중국 화엄종` | `e2 80 94` @ 0x50 | PASS |
| - | 전체 | 본문 내 `—` 총 등장 | `grep -c "—" == 156` | 다량 |

### BLOCKER 3명 표기 · DQ 404 확증

| thinker_id | study-guide 표기 | ES HTTP | ES found | 판정 |
|------------|--------------------|---------|----------|------|
| heidegger | L66·L93 "BLOCKER-1 · BLK-175E-2020B-001" | 404 | false | PASS |
| protagoras | L472·L519 "BLOCKER-2 · BLK-175E-2020B-002" | 404 | false | PASS |
| fazang | L633 "thinker_id: `fazang` ⚠️ ES 미등록 (BLOCKER-3 · BLK-175E-2020B-003)" + HTML 주석 | 404 | false | PASS |

총 `BLK-175E-2020B` 마커 카운트: 6+건 (머리글 L19, 공지 L39, 본문 3곳, 부록).

### 독일어·고대 그리스어 Step 1b 확장 확인

- heidegger Dasein/Geworfenheit/Angst/Sein zum Tode/Grundstimmung · protagoras Homo mensura/antilogic · fazang 법장 한자 → **Q1·Q6 구간**에 괄호·한자 래퍼로 존재 (Step 1b 전체파일 26개 모두 Q1~Q6 구간, Q7+ 구간은 0개). Coder 주장 "Q7~Q11에 그리스/키릴 괄호 없음 — Q1·Q6 구간에만 존재"와 일치.

## 이슈/블로커

### OBSERVATION-1: Step 1 bare-paren 산술 오산 (TASK-194-T OBS 교훈의 제3차 재발 변형)

- **증상**: Coder report-TASK-195 부록 L815 `grep -oE '\([A-Za-z][^)]*\)' | sort -u | wc -l` **46개** 주장. Tester 실측 `awk 'NR>=558' ... | grep -oE '\([A-Za-z][^)]*\)' | sort -u | wc -l` == **47개**.
- **원인**: Coder가 `shared meaning — Walzer` 래퍼 토큰은 메타 면제로 분류했으나, **동일 문자열 내부에 별개로 등장하는 `(shared meaning)` 단독 토큰**(L719)을 독립 항목으로 계수하지 못함. sort -u 결과에는 두 토큰이 별개로 들어감.
- **면제 자격**: L745 `### 면제 식별자 (coverage-absent · 문헌 표준)` 블록에 `shared meaning` 문자열 명시 존재. 따라서 0-hit 이나 **면제 자격 O** — 사상가 의도 왜곡 없는 학술 용어 자동 면제.
- **severity 판정**: **observation** (실질 결함 아님. Coder 부록 분류표의 수치 정합성 오류만.)
- **TASK-194-T OBS 재발 여부**: TASK-194-T에서도 유사한 Step 1/2 산술 불일치가 지적되었고, TASK-195 발주에 "제3차 재발 시 프레임워크 개선 trigger"가 명시됨. **본 TASK-195-T가 제3차 재발 사례**. 프레임워크 개선 trigger 발동 권고:
  - Coder 부록 작성 시 실제 `sort -u | wc -l` 출력을 **그대로 인용**하고 분류표 합계가 그 수치와 정확 일치하는지 검증하는 **자동 교차검증 단계**를 study-guide Coder 템플릿에 추가.
  - 또는 Coder report 제출 전 `분류표 합계 = grep 실측 wc -l` 식 명시 의무화.

### 기타 발견 (정상 범위)

- Q7~Q11에서 claim_id 직접 인용이 없고 `thinker_id + claim 핵심 설명` 형태로만 등장 — 본 TASK 체크 (5) 기준 "≥10건" 충족 (Q1~Q6에 27개 인용, ES 전수 found=true). 사양 위반 아님.
- Phase A 영역 내 L326~L333 Q4 채점 기준 신규 추가 건은 Coder가 "Manager 승인 가정 범위 내" 보강으로 자기 보고. 본문 결과 `채점 기준 == 9` 요건 충족 PASS.
- L541 오타 복구 (`己所不欠(불원)` → `己所不欲`) 주장 — 해당 구간 실물 검증: Q7 풀이 영역 `己所不欲` 표기 확인됨 (실측 불필요, Coder 자체 교정 타당).

## 다음 제안

1. **PASS 판정 — TASK-195 DONE 처리 권고**. observation 1건은 실질 결함이 아니며 면제 블록으로 방어됨.
2. **프레임워크 개선 trigger 발동** (TASK-194-T OBS 제3차 재발):
   - `agents/coder.md` 또는 study-guide Coder 템플릿에 "부록 자기검증 산술은 `sort -u | wc -l` 실측 출력과 정확 일치해야 함" 의무 추가.
   - Coder report 작성 시 분류표 하위합(19+4+23=46) == grep 실측 총수 자동 검증 script 제시 권장.
3. **TASK-176 별건** (heidegger·protagoras·fazang canonical ES 등록)은 기존 발주 유지.
4. 본 tester-report frontmatter severity=observation 이므로 Manager는 수정 태스크 필수 생성 의무 없음 (schema §164 기준).

## 산출물

- `signal/ethics-study/tester-report-TASK-195-T.md` (본 파일)
- 검증 대상: `projects/ethics-study/exam-solutions/study-guide/2020-B.md` (822L)
- 원천: `projects/ethics-study/exam-solutions/coverage/2020-B.md` (131L)
- 원본: `~/잡동사니/임용/md/2020_중등1차_도덕윤리_전공B.md` (188L)
