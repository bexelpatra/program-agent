---
task_id: TASK-200
round: 2
verdict: NEEDS_REVISION
---

# Reviewer Report: TASK-200 (R2 post-Edit 재검증)

## 검증 범위 (Round 2 한정)

Round 1 (`signal/ethics-study/reviewer-report-TASK-200.md`) 에서 제기된 **2 blocking 지적**의 해소 여부만 집중 재검증.

1. **Blocking 1**: blasi 재출제 이력 `2020-B→2023-A 2연속` → `2017-A→2019-B→2021-A→2023-A 4회차 격년` 정정 + "hoffman 4연속 대비 절반" 프레이밍 제거.
2. **Blocking 2**: Q3 원문 line 범위 `L46-L52` → `L46-L56` (L54 작성 방법 헤더 + L55-L56 ◦ 불릿 포함) 정정.

Round 1 PASS 판정 항목(Q1~Q12 시작 L·ES curl 실측·DQ-017 포맷·BLK 번호·동명이인·mill_js Q7/Q11·fudge 금지 조항·측정 가능성·1150L 상한)은 재확인만 수행하고 새로 뒤집지 않는다.

## Manager 주장 5개 Edit 실적용 검증

### 실측 grep 집계 (L343·L344 한정)

```
awk 'NR==343 || NR==344' task-board.md | grep -o '4회차 격년 재출제' | wc -l
→ 2  (L343 description 1 + L343 완료 조건 blasi subsection 1)

awk 'NR==343 || NR==344' task-board.md | grep -o 'L46-L56' | wc -l
→ 3  (L343 Q3 block header 1 + L343 완료 조건 (3) 라인 목록 1 + L344 TASK-200-T (2) 1)

awk 'NR==343 || NR==344' task-board.md | grep -o 'L46-L52' | wc -l
→ 0  (stale 범위 완전 제거 ✅)

awk 'NR==343 || NR==344' task-board.md | grep -o '2연속 재출제' | wc -l
→ 2  ⚠️ stale 잔존

awk 'NR==343 || NR==344' task-board.md | grep -o '2017-A Q2 → 2019-B Q8 → 2021-A Q6 갑 → 2023-A Q10 을' | wc -l
→ 1  (L343 완료 조건 blasi subsection 서술 1건. description 은 "2017-A→2019-B→2021-A→2023-A 4회차 격년" 압축형으로 다른 스타일 — 중복 아님)

sed -n '155p' data-quality-log.md
→ "| blasi | Q10 을 | 8 | TASK-176 후속 등록. **2017-A Q2 → 2019-B Q8 → 2021-A Q6 갑 → 2023-A Q10 을 = 4회차 격년 재출제** (coverage/2023-A.md L600·L744·L759 '2020-B 선등록' 표기는 원본 오기로 추정 — 2020-B coverage 에는 blasi 가 Q 답안 사상가로 등장하지 않고 2019-B 복기 언급만 존재. 실측 4회차 이력 기준 기재). hoffman 4연속 2016-A·2019-B·2021-B·2022-B 와 출제 총수 동급이나 격년 패턴. |"
```

### Manager 주장 vs 실적용 매핑

| # | Manager 주장 Edit | 실측 결과 | 판정 |
|---|---|---|---|
| 1 | L343 Q3 block header `L46-L52` → `L46-L56` | L343 `Q3 (기입형 2점·L46-L56)` 실재 | ✅ 적용 |
| 2 | L343 description blasi 재출제 이력 chunk 정정 | L343 `blasi (DQ-017 override · ... · 2017-A→2019-B→2021-A→2023-A 4회차 격년 재출제 · coverage/2023-A.md L600·L744·L759 "2020-B 선등록" 표기는 원본 오기로 추정 · 본 study-guide 에서는 실측 4회차 이력으로 기재)` 실재 | ✅ 적용 |
| 3 | L343 완료 조건 (10) blasi subsection 서술 정정 (`4회차 격년 재출제 전용 subsection (2017-A Q2 → 2019-B Q8 → 2021-A Q6 갑 → 2023-A Q10 을 · hoffman 4연속 ... 동급이나 4연속 아닌 격년 패턴)`) | L343 해당 서술 **실재** (격년 4회차 블록). **단 동일 L343 완료 조건 (10) 본문 tail 에 별도 "blasi 2연속 재출제 강조 subsection" 문구가 잔존** (아래 NOT_FIXED-1 참조) | ⚠️ **부분 적용** |
| 4 | L343 완료 조건 (3) 라인 범위 리스트 `L46-L52` → `L46-L56` | L343 `(3) ... L14-L32·L36-L42·L46-L56·L60-L72·...` 실재 | ✅ 적용 |
| 5 | L344 TASK-200-T 항목 (2) `Q3=L46-L52` → `Q3=L46-L56` | L344 `Q3=L46-L56` 실재 | ✅ 적용 |
| 6 | data-quality-log.md L155 비고 정정 | L155 4회차 격년 + coverage self-correction note 실재 | ✅ 적용 |

## 잔존 문제 — NOT_FIXED 2건

### NOT_FIXED-1 — L343 완료 조건 (10) tail 의 stale "blasi 2연속 재출제 강조 subsection"

실측 (`awk 'NR==343' | grep -oE '\(10\)[^|]*'`):
```
(10) 한자 래퍼 보존 + em-dash `e2 80 94` 3+ 샘플 hexdump + mill_js Q7·Q11 2회 출제 처리 · blasi 2연속 재출제 강조 subsection. **Tester 검증 태스크 분리**: ...
```

Manager는 L343 completion condition 중 **blasi subsection 서술 블록**(description header 바로 위 위치, Edit #3 대상)은 4회차 격년 문구로 바꿨으나, **같은 L343 완료 조건 item (10) 내부의 "blasi 2연속 재출제 강조 subsection"** 은 놓쳤다. Round 1 수정 요청 **위치 2** 가 L343 에 2번 반영되어야 했는데, Manager 는 1번만 반영.

### NOT_FIXED-2 — L344 TASK-200-T 항목 (10) 의 stale "blasi 2연속 재출제 강조 섹션 실재"

실측 (`awk 'NR==344' | grep -oE '\(10\)[^|]*'`):
```
(10) **자기검증 3단계 재실행 + 3분류 수치 Coder report 와 산술 정확 일치 검증** (...) · disjoint 교집합 0 검증 · mill_js Q7·Q11 2회 출제 별도 인용 확증 · blasi 2연속 재출제 강조 섹션 실재. **라틴/프랑스/독일/한국 불교/중국 한자 Step 1b 확장** (...)
```

Manager Round 1 수정 요청 리스트에는 TASK-200-T 의 경우 항목 (2) 라인 범위만 명시했고 항목 (10) 의 blasi 문구는 별도 항목으로 분리되지 않았으나, **R1 수정 요청 #1 "위치 2" 의 변경 취지("2연속" 프레이밍을 study-guide 계열 전수에서 제거)** 는 TASK-200-T 에도 자연 확장 적용되어야 한다. Tester 는 TASK-200-T 의 (10) 지시에 따라 "2연속 재출제 강조 섹션" 을 확인하러 들어가지만, 실제 study-guide 에는 4회차 격년 subsection 이 작성될 것이므로 **Tester 체크리스트와 Coder 산출물이 어긋나서 false negative 발생 위험** — 엄연히 blocking.

## Round 1 2 Blocking 해소 여부

| Blocking | Round 1 요구 사항 | Round 2 실측 | 해소 |
|---|---|---|---|
| B1 — blasi 재출제 이력 정정 | (a) description 4회차 격년 반영, (b) 완료 조건 (10) subsection 서술 4회차, (c) DQ-017 L155 비고 4회차 + self-correction note | (a) ✅ L343 description, (b) ⚠️ 부분 적용 — 완료 조건 blasi subsection 블록은 정정됐으나 item (10) tail 서술 2건 stale (L343·L344), (c) ✅ DQ-017 L155 | **❌ 부분 해소 (2건 stale 잔존)** |
| B2 — Q3 라인 범위 | L343 Q3 block header + 완료 조건 (3) 목록 + L344 TASK-200-T (2) 전수 `L46-L56` | 3개소 전부 `L46-L56` 실재, `L46-L52` 0건 | ✅ **완전 해소** |

## blasi 4회차 격년 재출제 이력 — coverage/*.md 전수 교차 확증 (Round 1 확증 재확인)

| 연도 | blasi 출제 | 근거 |
|---|---|---|
| 2017-A Q2 | ✅ | coverage/2017-A.md L89 `- **블라지 (blasi)** — Q2. (BLK-175E-2017A-001)` / L121 trademark 블록 |
| 2019-B Q8 | ✅ | coverage/2019-B.md L69 `Q8 블라지 ... blasi ... 미등록(BLK-175E-2019B-002)` |
| 2020-B | ❌ **미출제** | coverage/2020-B.md L127 는 선례 집계 열거에 `2019-B singer/freud/hoffman/**blasi**` 로 등장할 뿐 2020-B 자체 Q 답 사상가 아님. 2020-B 블로커는 heidegger·protagoras·fazang 3인. |
| 2021-A Q6 갑 | ✅ | coverage/2021-A.md L39 `BLK-175E-2021A-002 \| Q6 갑 \| 오거스토 블라지 ... (2019-B Q8 재출제 — 연속 2년차)` |
| 2023-A Q10 을 | ✅ | coverage/2023-A.md L723 / L759 BLK-175E-2023A-006 |

**결론 재확인**: blasi 는 2017·2019·2021·2023 의 홀수년(격년) 4회차 출제. Manager 주장 description "2017-A→2019-B→2021-A→2023-A 4회차 격년" 은 실측과 정면 일치. R1 blocking 1 의 사실 관계 재판정은 필요 없음.

## Q3 라인 범위 L46-L56 원본 실측 재확증

`~/잡동사니/임용/md/2023_중등1차_도덕윤리_전공A.md` L44-L60 실측:
- L44: `---` (Q2 종료 divider)
- L46: `### 3. [2점]` (Q3 헤더)
- L48: 발문
- L50: 갑 제시문
- L52: 을 제시문 (patria/natio)
- L54: `**<작성 방법>**` 헤더
- L55: `◦ 괄호 안의 ㉠에 해당하는 용어를 쓸 것.`
- L56: `◦ 괄호 안의 ㉡, ㉢에 해당하는 용어를 순서대로 쓸 것.`
- L58: `---` (Q3 종료 divider)
- L60: `### 4. [2점]` (Q4 헤더)

**Q3 정규 범위 = L46-L56** 확증. Manager 정정 값 정확.

## Round 1 OBS 항목 재확인 (뒤집기 없음)

| OBS | Round 1 판정 | Round 2 재확인 | 상태 유지 |
|---|---|---|---|
| Q12 끝 L202 (시험 종결자 `수고하셨습니다` 포함) | observation, 블록킹 아님 | 여전히 일관성 관점 선택적 · 구조적 오류 아님 | ✅ 유지 |
| blasi `_doc` top-level claims 배열 부재 vs ethics-claims 인덱스 | observation, ES 실측 결과 일치로 무해 | 변동 없음 | ✅ 유지 |

## 판정

**NEEDS_REVISION (Round 2)**

Manager 는 6개 Edit 중 4개를 정확 반영하고 Q3 라인 범위(B2)는 완전 해소했으나, **blasi "2연속 재출제" 문구 2건(L343 완료 조건 (10) tail · L344 TASK-200-T (10) tail)을 놓쳤다**. 이 2 잔존 문구가 남으면:

1. Coder 는 description/완료 조건 blasi subsection 의 "4회차 격년" 지시를 따라 쓰지만, 같은 완료 조건 (10) 의 "2연속 재출제 강조 subsection" 문구를 보고 **study-guide 제목·heading 을 "2연속 재출제" 로 오기**할 혼선 발생 가능.
2. Tester 는 TASK-200-T (10) 지시에 따라 "2연속 재출제 강조 섹션 실재" 를 확인하려 하지만, Coder 산출물이 4회차 subsection 이면 Tester 가 false negative 로 FAIL 처리할 위험.

factual error 제거는 전수 수행해야 하며, 부분 제거는 일관성 결손을 유발한다.

## 수정 요청 (NEEDS_REVISION R2 blocking)

### R2-B1 — L343 완료 조건 (10) tail 의 "blasi 2연속 재출제 강조 subsection" 정정

**현재 (L343 tail)**:
```
(10) 한자 래퍼 보존 + em-dash `e2 80 94` 3+ 샘플 hexdump + mill_js Q7·Q11 2회 출제 처리 · blasi 2연속 재출제 강조 subsection. **Tester 검증 태스크 분리**: ...
```

**수정**:
```
(10) 한자 래퍼 보존 + em-dash `e2 80 94` 3+ 샘플 hexdump + mill_js Q7·Q11 2회 출제 처리 · blasi 4회차 격년 재출제 강조 subsection. **Tester 검증 태스크 분리**: ...
```

### R2-B2 — L344 TASK-200-T 항목 (10) 의 "blasi 2연속 재출제 강조 섹션 실재" 정정

**현재 (L344)**:
```
(10) **자기검증 3단계 재실행 + ...** (...) · disjoint 교집합 0 검증 · mill_js Q7·Q11 2회 출제 별도 인용 확증 · blasi 2연속 재출제 강조 섹션 실재. **라틴/프랑스/독일/한국 불교/중국 한자 Step 1b 확장** (...)
```

**수정**:
```
(10) **자기검증 3단계 재실행 + ...** (...) · disjoint 교집합 0 검증 · mill_js Q7·Q11 2회 출제 별도 인용 확증 · blasi 4회차 격년 재출제 강조 섹션 실재. **라틴/프랑스/독일/한국 불교/중국 한자 Step 1b 확장** (...)
```

### 수정 후 재검증 명령

```
awk 'NR==343 || NR==344' signal/ethics-study/task-board.md | grep -o '2연속 재출제' | wc -l
# 기대: 0
awk 'NR==343 || NR==344' signal/ethics-study/task-board.md | grep -o '4회차 격년' | wc -l
# 기대: 4 (L343 description 1 + L343 blasi subsection 서술 1 + L343 item (10) 1 + L344 item (10) 1)
```

## Manager 에게 전달

Round 2 차단 사유 2건: **blasi "2연속 재출제" 잔존 2개소**. Q3 라인 범위(B2)는 완전 해소 · DQ-017 L155 · description chunk · 완료 조건 (3) 라인 목록 · TASK-200-T (2) 라인 범위 · 완료 조건 blasi subsection 서술 블록은 모두 정정 완료.

R2-B1, R2-B2 두 Edit 추가 적용 후 Round 3 Reviewer 재호출 요청. PASS 이전에는 **Coder Opus 발주 금지**. PASS 후에만 Coder Opus 발주 가능.

ES 실측·DQ-017 포맷·BLK 번호·동명이인·mill_js Q7/Q11 처리·무결 부분 변경 금지 조항·측정 가능성·1150L 분량 상한·Q3 L46-L56 등 Round 1 Major 2 건 중 1 건(B2) 및 다수 보조 PASS 항목은 여전히 유지.
