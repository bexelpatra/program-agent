---
task_id: TASK-190
verdict: NEEDS_REVISION
---

# Reviewer Report: TASK-190 (2018-A study-guide.md)

## 검증 대상

- Task ID: TASK-190 (Track B 9번째 — 2018-A 연도별 학생용 study-guide.md 신규 작성)
- signal/ethics-study/task-board.md L313 TASK-190 row
- 동반: TASK-190-T (task-board L314)
- 입력 원천: `projects/ethics-study/exam-solutions/coverage/2018-A.md`
- 원본 기출: `/home/jai/잡동사니/임용/md/2018_중등1차_도덕윤리_전공A.md`

## 검증 결과

### A. 원본·입력 파일 실존

| 항목 | 주장 | 실측 | 판정 |
|------|------|------|------|
| coverage/2018-A.md 행수 | 338 lines | `wc -l` = 338 | PASS |
| 기출 md 파일명 (2018) | `2018_중등1차_도덕윤리_전공A.md` (쉼표 없음) | `ls ~/잡동사니/임용/md/ \| grep 2018` = `2018_중등1차_도덕윤리_전공A.md` (16763 bytes) | PASS |
| 2017 파일명 차이 | `2017_중등1차_도덕,윤리_전공A.md` (쉼표 있음) | `ls … \| grep 2017` = `2017_중등1차_도덕,윤리_전공A.md` (16675 bytes) | PASS |
| 2018 기출 md 실제 행수 | (L1~L187) | `wc -l` = 187 | PASS |

### B. 문항별 line 범위

Read 로 `/home/jai/잡동사니/임용/md/2018_중등1차_도덕윤리_전공A.md` 전 구간 1회 직독 후 각 문항 시작줄 · 끝줄 확인.

| 문항 | 주장 범위 | 실측 (md의 `### N. [X점]` 헤더 다음 본문 끝) | 판정 |
|------|-----------|------------------------------------------------|------|
| Q1 | L14-L20 | `### 1. [2점]` L14 · 제시문 L18-L20 | PASS |
| Q2 | L24-L37 | `### 2. [2점]` L24 · 제시문+표 L28-L37 | PASS |
| Q3 | L41-L49 | `### 3. [2점]` L41 · 제시문 L45-L49 | PASS |
| Q4 | L53-L59 | `### 4. [2점]` L53 · 제시문 L57-L59 | PASS |
| Q5 | L63-L69 | `### 5. [2점]` L63 · 제시문 L67-L69 | PASS |
| Q6 | L73-L77 | `### 6. [2점]` L73 · 제시문 L77 | PASS |
| Q7 | L81-L95 | `### 7. [2점]` L81 · 대화 L85-L95 | PASS |
| Q8 | L99-L119 | `### 8. [2점]` L99 · 대화+표 L103-L119 | PASS |
| Q9 | L123-L131 | `### 9. [4점]` L123 · 대화 L127-L131 | PASS |
| Q10 | L135-L139 | `### 10. [4점]` L135 · 제시문 L139 | PASS |
| Q11 | L143-L153 | `### 11. [4점]` L143 · 토론 L147-L153 | PASS |
| Q12 | L157-L163 | `### 12. [4점]` L157 · 갑·을 L161-L163 | PASS |
| Q13 | L167-L173 | `### 13. [4점]` L167 · 제시문 L171-L173 | PASS |
| Q14 | L177-L183 | `### 14. [4점]` L177 · 제시문 L181-L183 | PASS |

14/14 모두 일치.

### C. ES 상태 (curl 실측, 본 세션 2026-04-22)

명령: `curl -s http://localhost:9200/ethics-thinkers/_doc/{id} | python3 -c "import sys,json;d=json.load(sys.stdin);print(d.get('found'))"`

| # | thinker_id | 주장 | 실측 | 판정 |
|---|-----------|------|------|------|
| 1 | lickona | found=true | True | PASS |
| 2 | wonhyo | found=true | True | PASS |
| 3 | kant | found=true | True | PASS |
| 4 | augustine | found=true | True | PASS |
| 5 | raths | found=true | True | PASS |
| 6 | locke | found=true | True | PASS |
| 7 | zhuxi | found=true | True | PASS |
| 8 | wangyangming | found=true | True | PASS |
| 9 | mill_js | found=true | True | PASS |
| 10 | epicurus | found=true | True | PASS |
| 11 | zhuangzi | found=true | True | PASS |
| 12 | aristotle | found=true | True | PASS |
| 13 | regan | 404 (NOT_FOUND) → BLOCKER | False | PASS |
| 14 | kirschenbaum | 404 (NOT_FOUND) → 보강 선택(NOT BLOCKER) | False | PASS |

12/12 등록·2/2 미등록 모두 주장과 일치.

### D. coverage vs task spec 정합성

| 항목 | coverage 실측 | task-board L313 주장 | 판정 |
|------|---------------|----------------------|------|
| Q1 정답·매핑 | L15: 인격 교육 + `lickona` 대표 | "lickona(12c) — 인격교육·존중과 책임·통합적 접근" | PASS |
| Q2 분류 | L16: `교과교육학` / "도덕적 사고 능력" | "해당 없음(교과교육학 · 2015 개정 도덕과 · 교과 역량 6가지)" | PASS |
| Q3 분류 | L17: `경계영역` / aristotle 간접 · 현대 추첨 이론가 미등록이나 이름 거론 없음 | "경계영역 · aristotle 간접 · 현대 이론가 이름 거론 없음 → BLOCKER 아님" | PASS |
| Q7 분류 | L21: `경계영역` 통일교육·북한 사회주의도덕 집단주의 | "해당 없음(통일교육·북한 사회주의도덕)" | PASS (용어 경계영역/해당 없음 혼용이나 내용 일치) |
| Q8 분류 | L22: `경계영역` 통일교육 평화 | "해당 없음(통일교육·남북합의문서)" | PASS (상동) |
| Q11 답·BLOCKER | L25: regan `내재적 가치`·`BLOCKER-1` · coverage L38 `BLK-175E-2018A-001` | "regan ⚠️ES 미등록(BLOCKER-1 · BLK-175E-2018A-001)" | PASS |
| Q12 다인 | L26: 갑 zhuxi(본연지성/기질지성·선지후행) + 을 wangyangming(지행합일) | "(갑) zhuxi + (을) wangyangming" | PASS |
| Q13 이중 매핑 | L27: 본문 화자 mill_js 질적 공리주의 + ㉠ epicurus | "(본문) mill_js + (㉠) epicurus" | PASS |
| BLOCKER 총 개수 | coverage L32: "본 시험 … 1건의 BLOCKER" + L38 단일 row | task-board: "BLOCKER=1 regan" | PASS |

### E. mill_js claim prefix

명령: `curl -s http://localhost:9200/ethics-claims/_search -H 'Content-Type: application/json' -d '{"query":{"match":{"thinker_id":"mill_js"}},"size":3,"_source":["id","thinker_id"]}'`

- 실측 총 17 claims · 상위 3건 id:
  - `mill-claim-002`
  - `mill-claim-003`
  - `mill-claim-004`
- **prefix = `mill-claim-NNN`** (thinker_id `mill_js` ≠ claim prefix `mill`). TASK-188 선례 일관성 유지 확증.
- task-board L313 주장 "mill_js 의 claim prefix 는 `mill-claim-NNN` (TASK-188 확증)" = PASS.

### F. agents/coder.md L89-L115 (자기검증 규약 인용)

| 항목 | Manager 주장 | 실측 (agents/coder.md) | 판정 |
|------|-------------|------------------------|------|
| L89-L115 섹션 실재 | 자기검증 2단계 프로토콜 | L89 "### 자기검증 2단계 프로토콜 (원문 인용 태스크 필수)" ~ L115 "면제 조건" 실재 | PASS |
| Step 1 (bare-paren 영어) | `grep -oE '\([A-Za-z][^)]*\)'` | L93-L96 정확 일치 | PASS |
| Step 1b (Greek/Cyrillic 확장) | `grep -oE '\([^)]*[α-ωΑ-Ωа-яА-Я][^)]*\)'` | **agents/coder.md L89-L115 구간에 "Step 1b" 또는 "Greek/Cyrillic" 문자열 부재** (전체 파일 grep: 매치 0건) | **FAIL (인용 불일치)** |
| Step 2 (TitleCase phrase) | `grep -oE '[A-Z][a-z]+(\s+[A-Za-z][a-z]+){1,5}'` | L98-L106 (Step 2 — 괄호 밖 / JSON 필드 / TitleCase 전수 추출)에 존재 | PASS (본문에 Step 2로 존재) |

**세부 판정**: agents/coder.md 본체는 Step 1 + Step 2 로 된 **2단계** 프로토콜이다. "Step 1b · Greek/Cyrillic" 정규식은 `signal/ethics-study/tester-report-TASK-189-T.md` L43 에서 **Tester 가 독립적으로 도입·수행**한 확장 검증이며, 동 report L70 에서 `agents/coder.md L89-L115 Step 1 프로토콜에 "wrapper decomposition" 절차 추가 권장(manager 판단)`으로 명시적으로 "framework 반영은 아직 안 됨" 을 알려주고 있다. Manager 는 task-board L313 에서 "agents/coder.md L89-L115: Step 1 + Step 1b Greek/Cyrillic + Step 2" 라고 **단일 출처로 뭉뚱그려 인용** 하여 Coder 에게 전달 시 소스를 혼동시킬 수 있다. 이는 TASK-187 · TASK-188 · TASK-189 spec 에서도 동일하게 반복되어 Coder 는 이미 실행해 왔으나, 엄밀한 인용 규약(실측 인용 의무) 위반이다.

### G. wrapper decomposition 주의 인용 정확성

| 항목 | 주장 | 실측 | 판정 |
|------|------|------|------|
| TASK-189-T 관찰로 "wrapper 전체 단위로 grounding 판정" 기재 | 본문·done-log 에 실재 | tester-report-TASK-189-T.md L69-L70 "observation 1건 … wrapper 전체로는 Buddha + 석가모니 가 grounded … content-level 결함 아님" + L41 "예외 1건(observation 대상): (Buddha, 석가모니, 고타마 싯다르타) 의 inner segment 고타마 싯다르타(Korean Hangul-only 토큰)가 coverage 0-hit" | PASS |
| 예시 wrapper `(Buddha, 석가모니, 고타마 싯다르타)` 인용 | 정확 | 동일 문자열 L41·L69 실재 | PASS |
| done-log 에 반영 | TASK-189-T 엔트리 | done-log.md L1918-L1922 "Observation: (Buddha, 석가모니, 고타마 싯다르타) wrapper 내 Hangul-only segment … wrapper decomposition 절차 개선 제안 → retrospective 이월" | PASS |

task-board L313 wrapper decomposition 주의는 적절히 실측 근거를 인용함 — PASS.

### H. 분할 Write 전략 경계

| 항목 | 주장 | 실측 | 판정 |
|------|------|------|------|
| 분할 지점 Q1~Q7 초기 Write → Q8~Q14 Edit append | 자연스러움(Q7=통일교육 해당 없음 · Q8=통일교육 해당 없음) | Q7 L81-L95(대화 15행) / Q8 L99-L119(표+대화 21행) — 모두 경계영역 "해당 없음" 섹션이라 길이 짧지 않음. 다만 선례(TASK-188 Q1~Q7 / Q8~Q14, TASK-189 Q1~Q5 / Q6~Q8) 와 일관된 중간 지점 배치. 배점 기준(기입형 Q1~Q8 종료 = Q7 경계 포함) 보다는 문항 번호 기준 분할. | PASS (선례 일관) |

### 기타 교차 확인

- **coverage L57-L62** ES canonical 55명 목록 실재 확인: `lickona · wonhyo · kant · augustine · raths · locke · zhuxi · wangyangming · mill_js · epicurus · zhuangzi · aristotle` 모두 명시. `regan · kirschenbaum` 미등재 (coverage L85-L86 별도 누락 섹션에 등록 필요자로 기재됨). PASS.
- **coverage L38** blocker row: `BLK-175E-2018A-001 · Q11 · 톰 리건` 단일 row 만 존재 — task-board 의 "BLOCKER=1" 주장 정합.

## 판정

**verdict = NEEDS_REVISION**

**근거 요약**:
- A/B/C/D/E/G/H 7개 축 모두 PASS (실측 100% 일치).
- **F (agents/coder.md L89-L115 인용)** 에서 "Step 1b · Greek/Cyrillic" 이 해당 파일 해당 구간에 부재. 실측 인용 의무 위반(CLAUDE.md L 기반 "실측 인용 의무" 규약).

**영향도 평가**: 이 문제는 TASK-187 · TASK-188 · TASK-189 에서도 동일한 표현으로 반복되어 Coder 는 실제로 Tester 의 Step 1b 를 포함한 3단계 검증을 수행해 왔고, 연속 PASS 로 결과 품질에는 지장이 없다. 그러나 엄밀히는:
1. Step 1b 는 `signal/ethics-study/tester-report-TASK-189-T.md` L43 에서 Tester 가 관측·도입한 실천이고,
2. `agents/coder.md` 본체는 아직 2단계 (Step 1 + Step 2) 에 머물러 있다 (`wrapper decomposition` 프로토콜 반영 권고 상태 — done-log L1921 "retrospective 이월").

즉 task-board L313 은 "요구되는 검증 (Step 1 + Step 1b + Step 2)" 은 옳지만, "그 근거 파일 위치(agents/coder.md L89-L115)" 가 틀렸다. Coder 가 L89-L115 를 Read 한 뒤 Step 1b 정규식을 찾지 못해 혼선을 겪거나, 반대로 "여기 없으면 안 해도 된다" 라고 판단할 위험이 있다.

## 수정 요청 (NEEDS_REVISION)

task-board L313 TASK-190 row 의 `**자기검증 규약** (agents/coder.md L89-L115): …` 문장을 아래 중 하나로 수정:

**수정안 A — 출처를 분리 인용**:
```
**자기검증 규약** (agents/coder.md L89-L115 : Step 1 괄호 안 영어 + Step 2 JSON 필드·TitleCase phrase) + **Step 1b Greek/Cyrillic 확장** (`grep -oE '\([^)]*[α-ωΑ-Ωа-яА-Я][^)]*\)'`, `signal/ethics-study/tester-report-TASK-189-T.md` L43 Tester 도입 실천 · TASK-187/188/189 시리즈 선례 적용): Step 1 + Step 1b + Step 2 전수 추출 → coverage md 역grep 0-hit 금지.
```

**수정안 B — "3단계 통합 관행(TASK-187~189 선례)" 로 명시**:
```
**자기검증 규약**: TASK-187~189 시리즈 선례 (agents/coder.md L89-L115 Step 1·2 + tester-report-TASK-189-T.md L43 Step 1b Greek/Cyrillic 확장) 통합 3단계 적용 — Step 1 bare-paren 영어(`grep -oE '\([A-Za-z][^)]*\)'`) + Step 1b Greek/Cyrillic 괄호(`grep -oE '\([^)]*[α-ωΑ-Ωа-яА-Я][^)]*\)'`) + Step 2 TitleCase phrase(`grep -oE '[A-Z][a-z]+(\s+[A-Za-z][a-z]+){1,5}'`) 전수 추출 → coverage md 역grep 0-hit 금지.
```

- TASK-190-T (L314) 주장 (9)/(10) 의 "자기검증 2단계 + Greek/Cyrillic 확장" 표현도 동일하게 정리 권장(선택·현재는 Tester 쪽이 스스로 도입한 실천이므로 PASS 유지 가능).
- 추가: 이 기회에 agents/coder.md 프레임워크 파일에 Step 1b 를 정식 반영하는 별도 태스크 (retrospective 결정 사항) 를 나중에 Manager 가 단독 세션에서 수행하면, 앞으로의 Track B 연도에서 이 모호성이 사라짐. (본 리뷰의 의견 · 범위 밖).

## Manager 에게 전달

- **검증 요약**: 8개 축 (A/B/C/D/E/F/G/H) 중 F 를 제외한 7개 PASS. F 만 인용 정확성에서 NEEDS_REVISION. 원문·입력 실측 · ES 14명 curl · BLOCKER 1건 · line 범위 · 다인 문항 매핑 · mill_js prefix · wrapper 관찰 인용 · 분할 Write 경계 모두 정합.
- **수정 필요 범위**: task-board L313 L314 의 1개 문장(자기검증 규약 출처 표기)만 수정. 나머지 spec 은 그대로 진행 가능.
- **수정 후 Coder 호출 가능 여부**: 위 수정안 A 또는 B 중 택1 반영 후 즉시 Coder 호출 가능. 실질적인 검증 기대치(Step 1b 포함 3단계)는 이미 TASK-187~189 에서 Coder·Tester 가 일관되게 실행해 온 관행이므로, 수정은 문서상 정확성 확보가 주 목적이다.
- **재검증 요청 여부**: 수정 후 재검증 불필요(수정 범위가 F 한 축에 국한되고 수정안이 명확하므로).
