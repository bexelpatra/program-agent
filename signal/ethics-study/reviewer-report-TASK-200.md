---
task_id: TASK-200
verdict: NEEDS_REVISION
---

# Reviewer Report: TASK-200 (R1 pre-Coder 검증)

## 검증 대상
- 파일:
  - `signal/ethics-study/task-board.md` L343 (TASK-200 row) · L344 (TASK-200-T row) · L342 (TASK-DQ-017 row)
  - `signal/ethics-study/data-quality-log.md` L141-L168 (DQ-017 entry)
  - `projects/ethics-study/exam-solutions/coverage/2023-A.md` (761L)
  - `~/잡동사니/임용/md/2023_중등1차_도덕윤리_전공A.md` (202L)
- Manager 주장 요약:
  1. 12문항·40점·Q1~Q4 기입형 2점+Q5~Q12 서술형 4점 (8+32=40).
  2. Q line starts L14/L36/L46/L60/L76/L93/L107/L122/L141/L159/L175/L188.
  3. ES HIT 13 unique + DQ-017 override 1 (blasi 8 claims) + BLOCKER 5 (404).
  4. N/A 2건 (Q1 교과교육학 · Q2 일반개념).
  5. mill_js 단일 시험 2회 출제 (Q7 『공리주의』 제5장 · Q11 『자유론』 제3장).
  6. blasi 2연속 재출제 (2020-B → 2023-A).
  7. TASK-DQ-017 DONE · data-quality-log.md DQ-017 entry 작성 완료.
  8. 분할 Write 전략, 1150L 상한, 자기검증 3단계 disjoint·fudge 금지 누적 엄수.

## 검증 결과

### 파일 존재

| 경로 | 존재 | 비고 |
|------|------|------|
| signal/ethics-study/task-board.md | ✅ | 344L (L343 TASK-200 · L344 TASK-200-T 실재) |
| signal/ethics-study/data-quality-log.md | ✅ | 168L (L141-L168 DQ-017 entry 실재) |
| projects/ethics-study/exam-solutions/coverage/2023-A.md | ✅ | 761L |
| ~/잡동사니/임용/md/2023_중등1차_도덕윤리_전공A.md | ✅ | 202L |
| projects/ethics-study/exam-solutions/study-guide/2023-A.md | ❌ (신규 · 정상) | TASK-200 작성 대상 |

### 내용 일치 — 실측 대조

#### (A) Q line starts — Manager 주장 vs 실측

| Q | Manager 주장 | coverage/2023-A.md 실측 | 원본 md 실측 | 판정 |
|---|------|------|------|------|
| Q1 | L14 | L11 header (`## Q1 [2점] (L14)`) | L14 `### 1. [2점]` | ✅ |
| Q2 | L36 | L57 header `(L36)` | L36 `### 2. [2점]` | ✅ |
| Q3 | L46 | L93 header `(L46)` | L46 `### 3. [2점]` | ✅ |
| Q4 | L60 | L144 header `(L60)` | L60 `### 4. [2점]` | ✅ |
| Q5 | L76 | L202 header `(L76)` | L76 `### 5. [4점]` | ✅ |
| Q6 | L93 | L272 header `(L93)` | L93 `### 6. [4점]` | ✅ |
| Q7 | L107 | L342 header `(L107)` | L107 `### 7. [4점]` | ✅ |
| Q8 | L122 | L397 header `(L122)` | L122 `### 8. [4점]` | ✅ |
| Q9 | L141 | L471 header `(L141)` | L141 `### 9. [4점]` | ✅ |
| Q10 | L159 | L541 header `(L159)` | L159 `### 10. [4점]` | ✅ |
| Q11 | L175 | L604 header `(L175)` | L175 `### 11. [4점]` | ✅ |
| Q12 | L188 | L654 header `(L188)` | L188 `### 12. [4점]` | ✅ |

**결론**: Q 시작 L 전수 일치. 배점 검산 2×4+4×8=40 ✅.

#### (B) Q line 끝 L (원본 md 실측 vs Manager 주장)

| Q | Manager 끝 | 원본 내용 끝(마지막 non-blank) | 차이 |
|---|-----|-----|-----|
| Q1 | L32 | L32 | ✅ exact |
| Q2 | L42 | L42 | ✅ exact |
| Q3 | L52 | **L56** (작성 방법 L54-L56 포함) | ⚠️ **truncation** — 작성 방법 누락 |
| Q4 | L72 | L72 | ✅ exact (Q4는 작성 방법 없음) |
| Q5 | L90 | L89 (L90=blank) | +1 (divider blank) |
| Q6 | L105 | L103 (L104=blank, L105=---) | +2 |
| Q7 | L119 | L118 (L119=blank, L120=---) | +1 |
| Q8 | L139 | L137 (L138=blank, L139=---) | +2 |
| Q9 | L157 | L155 (L156=blank, L157=---) | +2 |
| Q10 | L173 | L171 (L172=blank, L173=---) | +2 |
| Q11 | L186 | L184 (L185=blank, L186=---) | +2 |
| Q12 | L202 | L198 content + L200=--- + L202=수고하셨습니다 | +4 |

**특이사항 Q3**: Manager 주장 L46-L52는 을 제시문(L52) 에서 끊겨 작성 방법 3줄(L54-L56 `◦ 괄호 안의 ㉠...` 등)이 **완전 누락**. TASK-200 study-guide 작성 시 Q3 verbatim 에서 작성 방법이 빠질 위험. 바로잡아야 함.

**Q5~Q12**: Manager 끝 L이 항상 실제 내용 끝 + 1~4 라인으로 blank/divider 포함. 스타일 일관성 차원의 관용. 단 Q3 (L46-L52)는 내용 자체가 truncated 이므로 **구조적 오류**.

#### (C) ES 실측 (2026-04-23T07:XX curl localhost:9200)

**HIT 13 unique + blasi**:
```
kohlberg: 200 (20 claims) ✅
haidt: 200 (10 claims) ✅
confucius: 200 (17 claims) ✅
mozi: 200 (7 claims) ✅
mill_js: 200 (17 claims) ✅
kant: 200 (18 claims) ✅
zhuxi: 200 (16 claims) ✅
yiyulgok: 200 (12 claims) ✅
rousseau: 200 (13 claims) ✅
locke: 200 (12 claims) ✅
rest: 200 (10 claims) ✅
hume: 200 (10 claims) ✅
spinoza: 200 (6 claims) ✅
blasi: 200 (8 claims via ethics-claims index · _doc top-level `claims` field 부재) ✅
```

**BLOCKER 5 전원 404**:
```
tocqueville: 404 ✅
viroli: 404 ✅
choe_jeu: 404 ✅
shweder: 404 ✅
choe_chiwon: 404 ✅
```

**결론**: ES 실측 전원 Manager 주장과 일치. blasi claim count 8 확증 (ethics-claims 인덱스 `thinker_id:blasi` term query hits=8).

**NOTE (observation, 태스크 무영향)**: blasi `_doc` 는 DQ-016 등록 패턴과 다르게 최상위 `claims` 배열이 없는 스키마(kohlberg·rest·hume 등 기등록 사상가와 동일 구조 — claims 는 별도 `ethics-claims` 인덱스에 저장). Manager 가 "blasi 8 claims FOUND 200" 라고 쓴 것은 `ethics-claims` 조회 결과 기준으로 맞음. 혼동 없음.

#### (D) DQ-017 entry (data-quality-log.md L141-L168)

DQ-016 (L111-L139) 과 포맷 일관성 검증:

| 구조 | DQ-016 | DQ-017 | 일치 |
|------|--------|--------|------|
| 헤더 "## DQ-0XX — ... 부분 정정 (N FOUND · M NOT_FOUND)" | ✅ L111 | ✅ L141 | ✅ |
| ID/관련 태스크/file/category/coverage 작성일/본 세션 ES 실측일/요약 블록 | ✅ L113-L119 | ✅ L143-L149 | ✅ |
| "### FOUND override N건" 테이블 (thinker_id · 문항 · claim 수 · 비고) | ✅ L121-L127 | ✅ L151-L155 | ✅ |
| "### NOT_FOUND N건" 테이블 (thinker_id · 문항 · status · study-guide 표기) | ✅ L129-L136 | ✅ L157-L165 | ✅ |
| detected_by / resolution 서술 | ✅ L138-L139 | ✅ L167-L168 | ✅ |

DQ-017 entry 포맷 **완전 일관**. ✅.

#### (E) BLK 번호 충돌 — coverage/2023-A.md 와 일치?

coverage/2023-A.md BLK 번호 실측 (L139-L140, L198, L267, L336, L600, L716-L735, L754-L759):
- BLK-175E-2023A-001 → `tocqueville` ✅ Manager 일치
- BLK-175E-2023A-002 → `viroli` ✅ Manager 일치
- BLK-175E-2023A-003 → `choe_jeu` ✅ Manager 일치
- BLK-175E-2023A-004 → `shweder` ✅ Manager 일치
- BLK-175E-2023A-005 → `choe_chiwon` ✅ Manager 일치
- BLK-175E-2023A-006 → `blasi` → DQ-017 override (study-guide 에서는 미표기) ✅ Manager 일치

번호 충돌 없음. ✅.

#### (F) 동명이인 규약 (architecture.md L539-L541)

2023-A 출제 사상가 14명 검토:
- `kohlberg`·`haidt`·`confucius`·`mozi`·`kant`·`zhuxi`·`yiyulgok`·`rousseau`·`locke`·`rest`·`hume`·`spinoza`·`blasi` — 동명이인 candidate 없음.
- `mill_js` — John Stuart Mill 이니셜 suffix 단일인 · 정상.
- `taylor`·`taylor_p`·`smith` 등 충돌 id **없음** ✅.

### (G) mill_js Q7·Q11 2회 출제 — coverage 요약표 확증

coverage/2023-A.md L720·L724 실측:
- L720: `| Q7 | L107 | 4 | 사상가형 | \`mill_js\` (갑) + \`kant\` (을) | HIT / HIT | — |`
- L724: `| Q11 | L175 | 4 | 사상가형 | \`mill_js\` (단독) | HIT | Q7과 동일 사상가 2문항 |`

Manager task-board TASK-200 row spec:
> **mill_js 단일 시험 2회 출제 (Q7·Q11)**: Q7 『공리주의』 제5장 정의·공리·정의 감정 / Q11 『자유론』 제3장 개성·위해 원칙 — 서로 다른 저작·주제이나 동일 사상가. claim_id 각 문항별 별도 인용.

TASK-200-T row spec 항목 (5):
> 대표 claim_id 전수 found=true (≥ 13건 + **mill_js Q7·Q11 각 별도 인용 확증**).

claim_id 각 문항 별도 인용 의무 명시 ✅.

### (H) **무결 부분 변경·fudge 금지·제5차 재발 조항** 실재?

TASK-200 row 본문 검색 (L343):
- "⚠️ CRITICAL — TASK-199 선례 재엄수: Coder report 자기검증 3분류 수치 `sort -u | wc -l` 실측 결과와 **정확 일치** 의무." ✅
- "**"≈"/"수렴"/"중복 보정"/"대략" 문구 절대 금지**." ✅
- "disjoint 분류 구조 엄수. 제5차 재발 시 severity=blocker 승격(TASK-198/199 회피 유지)." ✅

TASK-200-T row 항목 (10):
- "TASK-198/199 제5차 재발 회피 재엄수 · "≈/수렴/중복 보정/대략" 문구 0건 확증 · 5차 재발 시 severity=blocker 승격" ✅

누적 엄수 조항 실재 ✅.

### (I) 분량 상한

기존 study-guide 파일 최대: 2019-A = 1078L (11문항).
2022-B (11문항) = 1032L.
2023-A = 12문항 + mill_js Q7·Q11 2회 출제 + N/A 2건 + BLOCKER 5건 + DQ-017 override 1건 + blasi 재출제 전용 subsection.

Manager 상한 1150L 는 합리적 (+118L over 2022-B, +72L over 2019-A). 단 Q5 3인(kohlberg+shweder+haidt) 통합 + Q6 3인(choe_chiwon+confucius+mozi) 통합은 긴 해설 필요 — **1150L 하한도 무리 없이 충족**할 가능성. 상한 유지 적절.

### (J) TASK-200-T 체크리스트 10항 측정 가능성

(1)~(10) 전부 grep·curl·wc 으로 측정 가능:
- (1) `grep -c '^## 문항' == 12`
- (2) 각 헤더 L{m}-L{n} metadata — 12 ranges grep
- (3) byte-level verbatim — hexdump + diff
- (4) 13+1 thinker_id curl 200
- (5) claim_id ≥ 13 + mill_js Q7/Q11 각각 별도 claim_id
- (6) BLOCKER 5 표기 grep · DQ-017 override 1 표기 없음 grep
- (7) N/A 2건 grep
- (8) `grep -c '^### 채점 기준' == 8` + 대조/통합 매핑 확인
- (9) hexdump em-dash `e2 80 94` 3 샘플
- (10) 자기검증 3분류 disjoint · fudge 문구 0 confirm

전수 측정 가능 ✅.

### 의존성·순서

| Task | Status | 근거 |
|------|--------|------|
| TASK-199 | DONE | task-board L339 `DONE (1032L · 11문항 ...)` |
| TASK-199-T | DONE PASS | task-board L340 `DONE (PASS · 10항 전수 ...)` |
| TASK-DQ-017 | DONE | task-board L342 `DONE (data-quality-log.md L141-L171 DQ-017 entry 기록 완료)` |
| TASK-200 | TODO | 의존성 TASK-199-T · TASK-DQ-017 모두 DONE |
| TASK-200-T | TODO | 의존성 TASK-200 |

**FIX-T 사이클 없음** (TASK-199-T PASS, TASK-198-FIX-T DONE). 정상.

## 중대 문제: blasi 재출제 이력 오기

### Manager 주장
TASK-200 row L343:
> blasi (DQ-017 override · 아우구스토 블라지 1931-2013 · ... · **2020-B→2023-A 2연속 재출제**)

blasi 완료 조건 (10):
> blasi 2연속 재출제 전용 subsection (2020-B → 2023-A · hoffman 4연속 대비 절반).

data-quality-log.md L155:
> blasi | Q10 을 | 8 | TASK-176 후속 등록. **2020-B→2023-A 2연속 재출제** 사상가.

### 실측 (coverage md 전수 grep)
| 연도 | blasi 출제 여부 | 근거 |
|------|----------------|------|
| **2017-A Q2** | ✅ 출제 | coverage/2017-A.md L89 `- **블라지 (blasi)** — Q2. (BLK-175E-2017A-001)` / L121 `블라지(blasi, ES 미등록) 책임(責任 — responsibility)` |
| **2019-B Q8** | ✅ 출제 | coverage/2019-B.md L69 `Q8 블라지 | 오거스토 블라지(Augusto Blasi) | blasi | 미등록(BLK-175E-2019B-002)` |
| **2020-B** | ❌ **미출제** | coverage/2020-B.md L31·L127 는 **retrospective 선례 목록(2019-B 복기)** 언급만; 2020-B 자체 Q 답에 blasi 없음. 2020-B 블로커 목록은 heidegger·protagoras·fazang 3명. |
| **2021-A Q6 갑** | ✅ 출제 | coverage/2021-A.md L39 `BLK-175E-2021A-002 | Q6 갑 | 오거스토 블라지(Augusto Blasi, 1935-2016) | 미등록 (**2019-B Q8 재출제 — 연속 2년차**)` |
| **2023-A Q10 을** | ✅ 출제 | coverage/2023-A.md L600 |

### 결론
**실제 blasi 재출제 이력**: 2017-A → 2019-B → 2021-A → 2023-A (격년 4회차 등장).
**Manager 주장 "2020-B → 2023-A 2연속 재출제"는 오기**.

이 오류의 원천은 coverage/2023-A.md 자체 (L600·L744·L759 "2020-B 선등록" · "2연속") — 작성 당시 Coder 가 2019-B 를 2020-B 로 오기한 것으로 추정. Manager 가 이를 그대로 인용하면서 data-quality-log.md DQ-017 · task-board TASK-200 row 양쪽에 오류 전파.

### 영향
- study-guide/2023-A.md 의 blasi 재출제 subsection 이 **학생에게 잘못된 빈도 맥락 전달**.
- "hoffman 4연속 대비 절반" 비교도 반박 — 실제 blasi 는 4회 출제이므로 hoffman(4연속 2016-A·2019-B·2021-B·2022-B) 과 출제 총수 동급. "절반" 은 잘못된 프레이밍.
- TASK-176 후속 등록 연계성 논리도 영향 가능 (blasi 는 2017-A 당시에도 BLK 였음).

### 판단
1. coverage/2023-A.md 자체 수정 금지 (원본 정정 금지 규정). 하지만 **TASK-200 study-guide 에는 정확한 재출제 이력을 기록**해야 함.
2. 해법: TASK-200 row description 및 data-quality-log.md DQ-017 L155 "비고" 란을 수정 — "2017-A Q2 → 2019-B Q8 → 2021-A Q6 갑 → 2023-A Q10 을 (4회 출제, 격년)" 로 정정. coverage md 오기 사실은 **별도 DATA-QUALITY 로그(DQ-018)** 로 추적 또는 DQ-017 body 내 `coverage/2023-A.md L600·L744·L759 self-correction note` 로 병기.
3. 완료 조건 (10) 의 "blasi 2연속 재출제 전용 subsection (2020-B → 2023-A · hoffman 4연속 대비 절반)" 재서술.

## 기타 지적

### Q3 원문 line 범위 truncation (L46-L52 → L46-L56)

TASK-200 완료 조건 (3) 및 TASK-200-T 항목 (2) 에서:
> Q3=L46-L52

**실측**: 원본 md Q3 는 L46(헤더) ~ L56(작성 방법 마지막 줄) 까지가 한 문항 단위. L54 `**<작성 방법>**`, L55·L56 `◦ 괄호 안의 ...` 3줄이 Q3 구성요소임에도 Manager 범위는 L52 에서 끊김. study-guide Q3 섹션의 `원문 line L46-L52` 메타데이터 및 verbatim 영역이 작성 방법 누락 상태로 기록될 위험.

다른 Q 범위는 내용 끝 + 1~4 라인(blank/---)을 포함하는 일관 관용이나, Q3 만은 **실제 내용이 truncated**. 수정 필요: `Q3 L46-L52` → `Q3 L46-L56`.

### Q12 끝 라인 L202 적정성

Q12 끝 Manager 주장 L202 = `**<수고하셨습니다.>**` (시험 종결 문구). 제시문/발문/작성 방법 아닌 시험지 종결자. 관용적으로 포함해도 무방하나 다른 Q 와 일관성 측면에서 `L188-L200` (`---` 포함) 이 더 정확. 단 **이 건은 OBS-level, 블록킹 아님** — 선택적 정정.

## 판정
**NEEDS_REVISION**

근거:
1. **blasi 재출제 이력 오기** (2017-A/2019-B/2021-A/2023-A 4회차가 실제임에도 Manager 는 "2020-B→2023-A 2연속" 기재). **실측과 정면 충돌**하는 factual error 이며 학생용 study-guide 의 핵심 맥락을 오도함. "hoffman 4연속 대비 절반" 비교도 근거 소실.
2. **Q3 원문 line 범위 truncation** (L46-L52 → L46-L56). 작성 방법 3줄 누락으로 verbatim 영역이 불완전.

두 건 모두 R1 단계에서 차단하지 않으면 Coder 가 그대로 반영 → study-guide 에 factual error 가 각인됨. 무결 부분 변경 금지 조항과도 상충.

## 수정 요청 (NEEDS_REVISION)

### 1. task-board.md L343 TASK-200 row — blasi 재출제 이력 정정

**위치 1**: `**blasi (DQ-017 override · ...  · 2020-B→2023-A 2연속 재출제)**`
→ `**blasi (DQ-017 override · 아우구스토 블라지 1931-2013 · 도덕적 자아 동일성 · 도덕적 인격 3요소 도덕적 욕구·의지력·자기통합성 · 2017-A→2019-B→2021-A→2023-A 4회차 격년 재출제 · coverage/2023-A.md L600·L744·L759 "2020-B 선등록" 표기는 원본 오기로 추정 · 본 study-guide 에서는 실측 4회차 이력으로 기재)`

**위치 2** (완료 조건 블록): `blasi 2연속 재출제 전용 subsection (2020-B → 2023-A · hoffman 4연속 대비 절반)`
→ `blasi 4회차 격년 재출제 전용 subsection (2017-A Q2 → 2019-B Q8 → 2021-A Q6 갑 → 2023-A Q10 을 · hoffman 4연속 2016-A·2019-B·2021-B·2022-B 와 출제 총수 동급이나 4연속 아닌 격년 패턴)`

### 2. data-quality-log.md L155 — DQ-017 FOUND override 테이블 비고 정정

```markdown
| blasi | Q10 을 | 8 | TASK-176 후속 등록. 2020-B→2023-A 2연속 재출제 사상가. |
```
→
```markdown
| blasi | Q10 을 | 8 | TASK-176 후속 등록. 2017-A Q2→2019-B Q8→2021-A Q6 갑→2023-A Q10 을 4회차 격년 재출제 (coverage/2023-A.md L600·L744·L759 "2020-B 선등록·2연속" 표기는 원본 오기 · 본 DQ-017 entry 실측 기준). |
```

### 3. task-board.md L343 TASK-200 row — Q3 원문 line 범위 정정

**위치 1** (문항별 ES 상태 블록): `**Q3 (기입형 2점·L46-L52)**:`
→ `**Q3 (기입형 2점·L46-L56)**:`

**위치 2** (완료 조건 (3) 라인 범위 목록): `L14-L32·L36-L42·**L46-L52**·L60-L72·L76-L90·L93-L105·L107-L119·L122-L139·L141-L157·L159-L173·L175-L186·L188-L202`
→ `L14-L32·L36-L42·**L46-L56**·L60-L72·L76-L90·L93-L105·L107-L119·L122-L139·L141-L157·L159-L173·L175-L186·L188-L202`

### 4. task-board.md L344 TASK-200-T row — Q3 원문 line 범위 정정

항목 (2): `Q3=L46-L52` → `Q3=L46-L56`

### 5. (선택, 비블로킹) Q12 끝 L 재확인

Manager L188-L202 는 L200 `---` + L202 `**<수고하셨습니다.>**` 를 포함. 다른 Q(Q6-Q11)는 `---` divider 에서 끝나는 관용 → 일관성 위해 `L188-L200` 고려 가능. 단 현 범위도 verbatim 에 해로움 없음 (시험지 종결자 보존이면 오히려 더 완전). **Observation-level · 판정에 영향 없음**.

## Manager에게 전달

R1 차단 사유 2건:
- **blasi 재출제 이력 factual error** (coverage md 오기 전파). 수정 후 DQ-017 entry · TASK-200 row · TASK-200 완료 조건 (10) 동기화 필수.
- **Q3 원문 line L46-L52 → L46-L56** (작성 방법 3줄 포함) 정정.

두 항목 수정 후 Reviewer 재호출 요청. PASS 이전에는 Coder 호출 금지.

ES 실측·DQ-017 포맷·BLK 번호·동명이인·mill_js Q7/Q11 처리·무결 부분 변경 금지 조항·측정 가능성·분량 상한은 모두 통과. 본질적 task-board 구조·포맷은 건전하며 위 2건만 정정하면 PASS 가능.
