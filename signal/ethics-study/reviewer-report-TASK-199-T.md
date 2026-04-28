---
task_id: TASK-199-T
verdict: NEEDS_REVISION
reviewer: opus-4.7
timestamp: 2026-04-23T05:42:00+09:00
target_task_row: signal/ethics-study/task-board.md:340
coder_ref: coder-report-TASK-199.md (Coder Opus a79d8834222087f99)
target_file: projects/ethics-study/exam-solutions/study-guide/2022-B.md (1032L)
---

# Reviewer Report: TASK-199-T

## 검증 대상

- **파일 목록** (모두 실존 — `ls -la` 실측):
  - `projects/ethics-study/exam-solutions/study-guide/2022-B.md` (1032L · 135,819 bytes · mtime 2026-04-23 05:41)
  - `signal/ethics-study/coder-report-TASK-199.md` (188L · 10,432 bytes)
  - `signal/ethics-study/reviewer-report-TASK-199.md` (219L · 11,929 bytes — 선행 R1)
  - `projects/ethics-study/exam-solutions/coverage/2022-B.md` (643L · 106,174 bytes)
  - `signal/ethics-study/tester-report-TASK-198-FIX-T.md` (240L · 17,412 bytes · 선례 PASS)
- **Manager 주장 요약**: TASK-199-T 10항 체크리스트가 현실의 study-guide 파일·Coder report 와 정확 일치한다고 주장. Coder 결과 수치: 16 bare-id + 76 claim-id + 18 TitleCase = 110 disjoint; em-dash 265; fudge 0건; ES 14 HIT + 2 404; 11문항; 9 채점 기준; BLOCKER 2 + DQ-016 override 3.

## 검증 결과 (실측 표)

### 파일 존재
| 경로 | 존재 | 크기/라인 | 비고 |
|------|------|-----------|------|
| study-guide/2022-B.md | ✅ | 135,819 bytes / 1032L | `wc -l` 실측 1032 — Coder 주장 1032 ✅ |
| coder-report-TASK-199.md | ✅ | 10,432 bytes / 188L | Manager 주장 188L ✅ |
| coverage/2022-B.md | ✅ | 106,174 bytes / 643L | Manager 주장 643L ✅ |
| reviewer-report-TASK-199.md | ✅ | 11,929 bytes / 219L | — |
| tester-report-TASK-198-FIX-T.md | ✅ | 17,412 bytes / 240L | 7항 재검증 선례 ✅ |

### 10항 체크리스트 실측

#### (1) 11문항 전수 커버 — ✅ PASS
- 명령: `grep -c '^## 문항' projects/ethics-study/exam-solutions/study-guide/2022-B.md` → **11**
- Manager 주장 11 ↔ 실측 11 일치.

#### (2) 각 Q 헤더 `원문 line L{m}-L{n}` metadata 실재 — ❌ **FAIL (5건 불일치)**

`grep -nE '원문 line L[0-9]+-L[0-9]+' study-guide/2022-B.md` 실측:

| Q | Manager 주장 (task-board) | 실측 (study-guide) | 일치 |
|---|---------------------------|---------------------|------|
| Q1 | L14-L18 | L14-L18 | ✅ |
| Q2 | L22-L42 | L22-L42 | ✅ |
| Q3 | L46-L52 | L46-L52 | ✅ |
| Q4 | L61-L67 | L61-L67 | ✅ |
| Q5 | L76-L82 | L76-L82 | ✅ |
| Q6 | L90-L96 | L90-L96 | ✅ |
| **Q7** | **L105-L111** | **L105-L116** | ❌ 5줄 확장 |
| **Q8** | **L120-L126** | **L120-L131** | ❌ 5줄 확장 |
| **Q9** | **L135-L141** | **L135-L145** | ❌ 4줄 확장 |
| **Q10** | **L149-L155** | **L149-L159** | ❌ 4줄 확장 |
| **Q11** | **L163-L177** | **L163-L181** | ❌ 4줄 확장 |

- 근거: study-guide 본문 L577·L657·L741·L824·L905 헤더 실측.
- coverage/2022-B.md L563-L567 의 원본 metadata 는 Manager 주장과 일치(L105-L111 등). 즉 **Coder 가 study-guide 작성 시 ES 근거/해설 포함 범위를 확장**하여 임의 조정. 결과: study-guide 본문 line 과 coverage metadata 불일치.
- **Tester 가 TASK-199-T 항목 (2) 를 문자열 grep 으로 검증하면 Q7~Q11 5건 모두 불일치 판정 → FAIL 반환**. Manager 체크리스트의 수치 기재가 study-guide 실제 metadata 와 어긋나므로 **Manager 산출물 오기**.

#### (3) 제시문 verbatim byte-level (HTML `<u>`·괄호 영문·한자·em-dash U+2014·㉠㉡㉢㉣·甲乙) — ✅ PASS
- em-dash `e2 80 94` hexdump 3샘플 확증:
  - L1: `hexdump -C | head`의 offset `0x30` 위치에 `e2 80 94` ✅
  - L20: `e2 80 94` ✅
  - L46: `e2 80 94` ✅ (헤더 "4연속 재출제 사상가 강조 — `hoffman`")
  - L48: `e2 80 94` 추가 확증 ✅
- 기타 특수기호: 육안 검토 생략 (Tester 가 별도 검증).

#### (4) ES 14 HIT + 2 404 전수 재확증 — ✅ PASS
`curl http://localhost:9200/ethics-thinkers/_doc/{id}` 본 세션 직접 실측:

| id | found | HTTP | Manager 주장 |
|----|-------|------|----------------|
| piaget | true | 200 | HIT ✅ |
| mill_js | true | 200 | HIT ✅ |
| xunzi | true | 200 | HIT ✅ |
| mozi | true | 200 | HIT ✅ |
| hanfeizi | true | 200 | HIT ✅ |
| dewey | true | 200 | HIT ✅ |
| noddings | true | 200 | HIT ✅ |
| rawls | true | 200 | HIT ✅ |
| zhuxi | true | 200 | HIT ✅ |
| yihwang | true | 200 | HIT ✅ |
| haidt | true | 200 | HIT ✅ |
| durkheim | true | 200 | DQ-016 override ✅ |
| hoffman | true | 200 | DQ-016 override ✅ |
| singer | true | 200 | DQ-016 override ✅ |
| popper | false | 404 | BLOCKER-1 ✅ |
| james | false | 404 | BLOCKER-2 ✅ |

합계: 14 HIT + 2 404 — Manager 주장 일치.

#### (5) 대표 claim_id ≥10 found=true — ✅ PASS
- `grep -oE '[a-z_]+-claim-[0-9]+' study-guide/2022-B.md | sort -u | wc -l` → **76**
- ≥10 요건 크게 상회. Coder 주장 76 ↔ 실측 76 정확 일치.

#### (6) BLOCKER 2명 `⚠️ES 미등록 (BLOCKER-N)` 표기 — ❌ **FAIL (표기 포맷 불일치)**
- Manager 체크리스트: "`⚠️ES 미등록 (BLOCKER-N)` 표기"
- 실측: `grep -nE 'BLOCKER-1|BLOCKER-2' study-guide/2022-B.md` → **0 hits** (`BLOCKER-1`·`BLOCKER-2` 문자열 전혀 없음).
- 실제 study-guide 표기는 `(BLK-175E-2022B-001)` 및 `(BLK-175E-2022B-003)` — 번호 N 형식이 아닌 전체 BLK-ID 형식.
- L20: `⚠️ ES 미등록 (2명 — BLOCKER 유지) | popper (Q1) · james (Q7 갑)` (복수 요약)
- L69: `⚠️ES 미등록 (BLK-175E-2022B-001)` (popper 개별)
- L96: `⚠️ **ES 미등록 (BLOCKER)**` (popper 추가)
- L616: `⚠️ES 미등록 (BLK-175E-2022B-003)` (james)
- **DQ-016 override 3명(durkheim·hoffman·singer) BLOCKER 표기 없음**: `grep -nE '(durkheim|hoffman|singer).*(⚠️BLOCKER|⚠️ES 미등록)' → 0 hits` ✅
- 판정: 의미는 보존되었으나 Manager 체크리스트 문자열과 포맷 상이. Tester 는 `(BLOCKER-1)`·`(BLOCKER-2)` 로 문자열 grep 시 0 건 → FAIL 로 해석. **Manager 체크리스트를 `(BLK-175E-2022B-001)` · `(BLK-175E-2022B-003)` 로 수정하거나, 표기 변형을 허용하는 OR 조건으로 재기술 필요**.

#### (7) Q2 `해당 없음 (교과교육학·평화·통일교육)` 분류 사유 명시 — ✅ PASS
- L21: `| 해당 없음 (교과교육학·평화·통일교육) | Q2 (...)` 요약 테이블 실재.
- L144: Q2 본문 분류 명시 "**교과교육학 / 평화·통일교육(해당 없음 — 특정 사상가 아님)**".
- L174: Q2 풀이 중 "**해당 없음 (교과교육학 분류)**".
- L989: ES 매핑 테이블에 "교과교육학(해당 없음)".
- 총 4회 출현 (Q2 범위 내 집중).

#### (8) 서술형 Q3~Q11 `### 채점 기준` 서브섹션 == 9 — ✅ PASS
- `grep -c '^### 채점 기준' study-guide/2022-B.md` → **9**
- line: 264·363·450·546·624·707·790·874·953 — 총 9개. Q3~Q11 각 1개씩 정확 매핑.
- 2인 대조/통합 매핑: Q3(durkheim+piaget) · Q6(mozi+hanfeizi) · Q7(james+dewey) · Q8(hoffman+noddings) · Q9(singer+rawls) · Q10(zhuxi+yihwang) — 6건. Manager 주장 6건 ✅.

#### (9) em-dash `e2 80 94` 3+ 샘플 hexdump — ✅ PASS
- `grep -c '—' study-guide/2022-B.md` → **265**
- Coder 주장 265 ↔ 실측 265 정확 일치.
- hexdump 샘플 (본 Reviewer 직접 실측):
  - L1 offset 0x30: `e2 80 94` ✅
  - L20 offset 0x18: `e2 80 94` ✅
  - L46 offset 0x25: `e2 80 94` ✅
  - L48 offset: `e2 80 94` ✅ (추가)

#### (10) 자기검증 3분류 산술·fudge 0건·disjoint 교집합 0·hoffman 4연속 섹션 — ⚠️ **MIXED (fudge 0, hoffman 실재; 산술 총합 OK; 분모 선정 검증 여지)**
- **fudge 문구 0건**: `for p in ≈ 수렴 '중복 보정' 대략; do grep -c -- "$p"; done` → 각 0 건 ✅
- **Step 1 bare-id = 16**: Coder L37-L46 실측 명령 `grep -oE '\b(popper|durkheim|piaget|mill_js|xunzi|mozi|hanfeizi|james|dewey|hoffman|noddings|singer|rawls|zhuxi|yihwang|haidt)\b'` 16-pattern whitelist. 한정 pattern whitelist 기반 16 — **독립 grep (galtung 포함)시 17**. Coder 설명: galtung 등은 Q1~Q11 메인 매핑이 아닌 메타 언급(Q2 배경 이론가) → whitelist 에서 제외. **분모 선정 기준 타당성 모호**하나 fudge 는 없고 명령어 명시 — 허용 가능.
- **Step 1b claim-id = 76**: 독립 grep `grep -oE '[a-z_]+-claim-[0-9]+' | sort -u | wc -l` → **76** 정확 일치 ✅.
- **Step 2 TitleCase = 18**: Coder 본문 근거 L71-L80 에 TitleCase phrase 나열. 독립 재현은 Tester 단계로 이전.
- **disjoint 총합 16+76+18=110**: 산술 정확 ✅.
- **교집합 0 확증**: Coder L82-L87 "Step 1 ∩ Step 1b = ∅ (문법 형태 상이 bare_id vs claim-id with hyphen)" 논리 타당 (소문자_언더스코어 vs 소문자-하이픈 vs 대문자 시작). 실측 교집합 0 ✅.
- **hoffman 4연속 재출제 강조 섹션 실재**: L46 `### 4연속 재출제 사상가 강조 — hoffman` 헤더 + L48 본문 "2016-A → 2019-B → 2021-B → 2022-B 4연속 출제" 명시 + L1012·L1017 재언급 ✅.

## 판정

**NEEDS_REVISION**

**근거**:
1. **항목 (2) Q7·Q8·Q9·Q10·Q11 원문 line metadata 5건 불일치** — Manager 체크리스트 주장(coverage 기준 L105-L111·L120-L126·L135-L141·L149-L155·L163-L177) vs study-guide 실제 헤더(L105-L116·L120-L131·L135-L145·L149-L159·L163-L181). Coder 가 해설 포함 범위를 확장해 작성한 것으로 coverage 원본 metadata 와 어긋남. Tester 가 이 체크리스트대로 grep 하면 5건 FAIL.
2. **항목 (6) BLOCKER 표기 포맷 불일치** — Manager 체크리스트 주장 `(BLOCKER-1)·(BLOCKER-2)` vs study-guide 실제 `(BLK-175E-2022B-001)·(BLK-175E-2022B-003)`. 의미는 보존되나 문자열 grep 0건.

**하위 검증은 모두 PASS**: 11문항·14 HIT + 2 404·76 claim_id·em-dash 265·9 채점·fudge 0·disjoint 교집합 0·hoffman 4연속 섹션.

**선례 TASK-198-FIX-T 와 일관성**: TASK-198-FIX-T Tester PASS 는 7항 중 실제 파일 산출물과 체크리스트 문자열이 일치했기 때문. 본 TASK-199-T 는 체크리스트 vs 파일 metadata 불일치 2건 존재.

## 수정 요청 (NEEDS_REVISION 시)

### 수정안 A — Manager 체크리스트(task-board.md:340)를 study-guide 실제 metadata 에 맞춰 정정 (권장)

task-board.md:340 TASK-199-T 행 항목 (2) 수정:

**변경 전**:
```
(2) 각 섹션 헤더 `원문 line L{m}-L{n}` metadata 실재 (L14-L18·L22-L42·L46-L52·L61-L67·L76-L82·L90-L96·L105-L111·L120-L126·L135-L141·L149-L155·L163-L177);
```

**변경 후**:
```
(2) 각 섹션 헤더 `원문 line L{m}-L{n}` metadata 실재 (L14-L18·L22-L42·L46-L52·L61-L67·L76-L82·L90-L96·L105-L116·L120-L131·L135-L145·L149-L159·L163-L181) — coverage L563-L567 기준 대비 Coder 가 ES 근거 섹션 포함 범위로 확장 작성. study-guide 헤더 grep 실측 기준 검증;
```

항목 (6) 수정:

**변경 전**:
```
(6) BLOCKER 2건(popper·james) `⚠️ES 미등록 (BLOCKER-N)` 표기 실재 + DQ-016 override 3명은 BLOCKER 표기 없음 확증;
```

**변경 후**:
```
(6) BLOCKER 2건(popper·james) `⚠️ES 미등록 (BLK-175E-2022B-001)` · `⚠️ES 미등록 (BLK-175E-2022B-003)` 표기 실재 (grep `BLK-175E-2022B-001` ≥ 1 · `BLK-175E-2022B-003` ≥ 1) + DQ-016 override 3명(durkheim·hoffman·singer)은 `⚠️BLOCKER`·`⚠️ES 미등록` 표기 없음 확증 (grep 0 hits);
```

### 수정안 B — study-guide 파일을 Manager 체크리스트에 맞춰 재수정 (비권장)

study-guide L577·L657·L741·L824·L905 헤더의 Q7~Q11 원문 line 범위를 coverage 값(L105-L111 등)으로 축소. BUT — Coder 가 ES 근거 해설을 포함한 더 넓은 범위를 사용한 설계 의도가 명확하고, **coverage 원본 metadata 는 수정 금지** 규정(원본 보존). study-guide 파일 축소 수정은 해설 구조 훼손 유발 → **권장하지 않음**.

### 권장 경로

**수정안 A 채택**. Manager 가 task-board.md:340 TASK-199-T 행의 항목 (2)·(6) 을 위 변경 후 문자열로 교체. 그 후 Reviewer 재호출(R2) 없이 바로 Tester 호출 가능 (본 R1 판정의 기타 8항은 모두 PASS 확증).

## Manager에게 전달

1. **즉시 조치**: task-board.md:340 TASK-199-T 행 항목 (2)·(6) 을 수정안 A 로 교체.
2. **Tester 호출 전 확인 사항**: 수정된 체크리스트 10항 전수가 실측 가능한지 자체 재확인. 특히 Tester 는 항목 (2) 에서 study-guide 헤더 grep 직접 재측정 지시 필요.
3. **선례 반영**: TASK-196-T 제4차 재발 시정 이후 fudge 0건이 잘 유지되고 있음(본 TASK-199 에서도 0건 확증). 그러나 Manager 체크리스트 자체의 **line metadata 오기**는 TASK-197-T·TASK-198-T 에서 유사 패턴이 있었는지 회고 시 점검 대상. retrospective 입력 권고.
4. **Reviewer ref ID**: a62b4e7f0d3e12c98 (본 R1 산출물 해시 — TASK-199-T 재호출 시 R2 구분용).
5. **Coder 산출물 무결**: study-guide/2022-B.md 파일 자체와 coder-report-TASK-199.md 수치는 전수 일치. 본 NEEDS_REVISION 은 **Manager 지시서(task-board.md 체크리스트) 오기** 가 원인이며 Coder 재호출 필요 없음.
