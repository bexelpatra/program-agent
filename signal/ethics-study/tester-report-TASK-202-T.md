---
agent: tester
task_id: TASK-202-T
status: DONE
severity: observation
---

# Tester Report · TASK-202-T · 2024-A study-guide.md 학생용 검증

## 1. 개요

- 검증 대상: `projects/ethics-study/exam-solutions/study-guide/2024-A.md` (728L, Coder TASK-202)
- Coder report: `signal/ethics-study/coder-report-TASK-202.md`
- 원본: `~/잡동사니/임용/md/2024_중등1차_도덕·윤리_전공A.md` (223L · FOUND)
- coverage: `projects/ethics-study/exam-solutions/coverage/2024-A.md` (765L)
- 실측 시각: 2026-04-23
- 판정: **severity=observation** (전 항목 통과, Step 1b 넓은 scope 측정 gap + BLOCKER 라벨 숫자 표기 관찰 2건)

## 2. 10항 체크 결과 표

| # | 항목 | 결과 | 근거 |
|---|------|------|------|
| 1 | 12문항 전수 커버 | **PASS** | `grep -c '^## 문항' = 12` |
| 2 | 섹션 헤더 `원문 line L{m}—L{n}` 12쌍 실재 (em-dash U+2014) | **PASS** | 12개 모두 task 명세와 정확 일치 (§3 표 참조) |
| 3 | 제시문 verbatim byte-level | **PASS** | `<u>`·㉠㉡㉢㉣㉤㉥·實踐·傳統·功利·超越·法藏·事事無礙法界·一心·四法界·和諍·民族大團結·特殊關係·akrasia·enkratēs·sōphrōn·Callatiae·Hellas·practice·tradition 전수 ≥1 hit |
| 4 | ES 등록 11명 found=true | **PASS** | curl 11회 전수 HTTP=200·found=true |
| 5 | 대표 claim_id 전수 found=true | **PASS** | 40개 unique claim-id 전수 found=true (narvaez-001/002/003 포함) |
| 6 | 잔존 BLOCKER 4건 표기 실재 | **PASS (label observation)** | coombs(BLK-001)·Q5㉢(BLK-003)·Q7갑(BLK-004)·fazang(BLK-005) 모두 `⚠️ES 미등록` 표기 실재. narvaez DQ-018 override 는 BLOCKER 표기 없음 확증. 단 BLOCKER 라벨 숫자는 BLOCKER-1/2/3/4 로 순차 부여 (task 명세의 1/2/4/5 와 시퀀스 차이 · §5 관찰 1 참조) |
| 7 | 해당 없음 처리 | **PASS** | Q1(교과교육학 L72) · Q3(메타윤리 L142) · Q12(경계영역 L684) · Q5 교과교육학 복합 BLOCKER 사유 L254 모두 실재 |
| 8 | 서술형 Q5—Q12 `### 채점 기준` == 8 | **PASS** | `grep -c = 8` · 각 Q5(L268)/Q6(L330)/Q7(L393)/Q8(L456)/Q9(L514)/Q10(L574)/Q11(L642)/Q12(L700) 매핑 정확 |
| 9 | em-dash `e2 80 94` 3+ 샘플 hexdump | **PASS** | L1 offset 0x35, L3 offset 0xb4 & 0xea, L4 offset 0x16c 4+ hit 확증 |
| 10 | 자기검증 3단계 산술 정확 일치 | **PASS (step1b observation)** | Step1=104 일치 · Step2=37 일치 · fudge=0 · disjoint pairwise 0 · BLOCKER 404 2건 재확인 · narvaez HIT 재확인 · HIT 10명 재확인. Step1b 는 narrow=0 일치 / wide=6 토큰 gap (§5 관찰 2) |

## 3. 섹션 헤더 line 범위 전수 실측

| Q | study-guide line | 헤더 (em-dash = e2 80 94) | task 명세 일치 |
|---|------------------|---------------------------|----------------|
| Q1 | L56 | `## 문항 1 · 기입형 · 2점 · 원문 line L16—L26` | ✓ |
| Q2 | L92 | `## 문항 2 · 기입형 · 2점 · 원문 line L28—L35` | ✓ |
| Q3 | L129 | `## 문항 3 · 기입형 · 2점 · 원문 line L37—L44` | ✓ |
| Q4 | L163 | `## 문항 4 · 기입형 · 2점 · 원문 line L46—L53` | ✓ |
| Q5 | L202 | `## 문항 5 · 서술형 · 4점 · 원문 line L55—L101` | ✓ |
| Q6 | L288 | `## 문항 6 · 서술형 · 4점 · 원문 line L103—L117` | ✓ |
| Q7 | L351 | `## 문항 7 · 서술형 · 4점 · 원문 line L119—L137` | ✓ |
| Q8 | L414 | `## 문항 8 · 서술형 · 4점 · 원문 line L139—L157` | ✓ |
| Q9 | L477 | `## 문항 9 · 서술형 · 4점 · 원문 line L159—L172` | ✓ |
| Q10 | L535 | `## 문항 10 · 서술형 · 4점 · 원문 line L174—L188` | ✓ |
| Q11 | L594 | `## 문항 11 · 서술형 · 4점 · 원문 line L190—L205` | ✓ |
| Q12 | L664 | `## 문항 12 · 서술형 · 4점 · 원문 line L207—L221` | ✓ |

## 4. Coder 수치 vs Tester 독립 측정 대조

| 지표 | Coder 보고 | Tester 실측 | 일치 |
|------|-----------|-------------|------|
| `grep -c '^## 문항'` | 12 | 12 | ✓ |
| `grep -c '^### 채점 기준'` | 8 | 8 | ✓ |
| Step 1 (괄호 영문 고유 토큰) | 104 | **104** | ✓ 산술 정확 일치 |
| Step 1b (narrow class Coder 기준) | 0 | **0** | ✓ 산술 정확 일치 |
| Step 1b (wide class Tester 기준) | (측정 안 함) | **6** | observation — §5 관찰 2 참조 |
| Step 2 (TitleCase 2—6 단어) | 37 | **37** | ✓ 산술 정확 일치 |
| Disjoint Step1 ∩ Step1b | 0 | 0 | ✓ |
| Disjoint Step1 ∩ Step2 | 0 | 0 | ✓ |
| Disjoint Step1b ∩ Step2 | 0 | 0 | ✓ |
| fudge phrases (≈·수렴·중복 보정·대략) | 0 | **0** | ✓ 5차 재발 없음 |
| 줄 수 | 728 | **728** | ✓ |

## 5. 관찰 사항 (observation 근거)

### 관찰 1 · BLOCKER 라벨 숫자 시퀀스 차이 (non-blocking)

Task 명세에서는 BLOCKER 라벨이 (BLOCKER-1, BLOCKER-2, BLOCKER-4, BLOCKER-5) 로 지정되어 있으나, 학생용 가이드 실재 라벨은 (BLOCKER-1, BLOCKER-2, BLOCKER-3, BLOCKER-4) 로 순차 부여되어 있다.

| 항목 | BLK ID (정확 일치) | 가이드 라벨 | task 명세 라벨 |
|------|-------------------|-------------|----------------|
| coombs (Q5) | `BLK-175E-2024A-001` | BLOCKER-1 | BLOCKER-1 ✓ |
| Q5 ㉢ 검사 명칭 | `BLK-175E-2024A-003` | BLOCKER-2 | BLOCKER-2 ✓ |
| Q7 갑 한국 성리학자 | `BLK-175E-2024A-004` | **BLOCKER-3** | **BLOCKER-4** |
| fazang (Q8 갑) | `BLK-175E-2024A-005` | **BLOCKER-4** | **BLOCKER-5** |

- 고유 식별자 `BLK-175E-2024A-XXX` 는 모두 task 명세와 정확 일치.
- 사람 가독 라벨 `BLOCKER-N` 은 학생용 가이드에서 1,2,3,4 순차 부여 (BLK-175E-2024A-002 가 narvaez DQ-018 override 로 제외되면서 가이드 내 라벨 시퀀스가 순차가 됨).
- narvaez DQ-018 override 는 BLOCKER 표기 **없음** 확증 (task 요구 사항 충족).
- Coder 의 선택 (순차 라벨링) 은 학생 독자 관점에서 합리적이며, 핵심 고유 식별자(BLK-ID) 는 정확 일치하므로 **non-blocking**. 태스크 명세 기대치와의 라벨 표기 차이만 관찰로 기록.

### 관찰 2 · Step 1b narrow vs wide scope 측정 gap

Coder 의 narrow character class `[ΑΒ…Ωαβ…ωāīūṛṣṇṃḥäöüéèêçñ]+` 기준 측정값 = 0 (정확).

Tester 의 wide character class `[A-Za-z]*[α-ωΑ-Ωāīūēōṁṃṇṭḍḷṛṅñśṣäöüßéèêàçôùñ][…]*` (Latin prefix 허용) 기준 측정값 = **6 토큰**:

| 토큰 | 발견 위치 | ES 근거 |
|------|----------|---------|
| `aretē` | L109 (L555) | 한자 병기 `卓越性(탁월성 — excellence / aretē)` |
| `enkratēs` | L33, L555, L559, L563, L588 | aristotle-claim-001/002 근거 |
| `epistēmē` | L558, L563, L571, L587 | aristotle-claim-004 근거 |
| `mesotēs` | L33, L559, L560, L563, L569 | aristotle-claim-002 근거 |
| `phronēsis` | L33, L563, L572 | aristotle-claim-005 근거 |
| `sōphrōn` | L33, L555, L559, L560, L563, L588 | aristotle-claim-001 근거 |

- 이 6 토큰은 모두 coverage/2024-A.md 에 근거가 있고 Coder 가 명시적으로 인용한 아리스토텔레스 용어로, 창작·fudge 아님.
- Coder 의 narrow regex 는 `macron ē/ō` 가 포함된 Latin 연결형 토큰 (aretē, sōphrōn 등) 을 범위 밖으로 처리한 것이 원인. Coder 의 Step 1b=0 주장은 자기 regex scope 내에서는 정확.
- 선례: TASK-201-T 에서도 Coder 41 vs Tester 36 gap 이 observation 으로 기록됨.
- **gap 자체는 문서의 정확성·verbatim 준수·BLOCKER 표기와 무관** → severity=observation.

## 6. 삭제된 0-hit 토큰 샘플 검증 (5개)

Coder 가 "원문 0 hit" 사유로 삭제했다고 보고한 28건 중 5개 샘플을 원본 md 로 역검색:

| 토큰 | 원본 md hit | 결론 |
|------|------------|------|
| `tathāgatagarbha` | 0 | 삭제 정당 (원문 부재) |
| `Herodotos` | 0 | 삭제 정당 |
| `eudaimonia` | 0 | 삭제 정당 |
| `proairesis` | 0 | 삭제 정당 |
| `Critical Commentary` | 0 | 삭제 정당 |

Coder 창작물을 잘못 삭제한 사례 **없음** → Phase 6 창작 금지 준수 재확증.

## 7. ES 재조회 curl 실측 전수 결과

### 7-1. 11 thinkers HTTP=200 found=true

```
macintyre       | HTTP=200 | "found":true
mill_js         | HTTP=200 | "found":true
gilligan        | HTTP=200 | "found":true
narvaez         | HTTP=200 | "found":true   ← DQ-018 override 확증
jeongyagyong    | HTTP=200 | "found":true
wonhyo          | HTTP=200 | "found":true
hume            | HTTP=200 | "found":true
aristotle       | HTTP=200 | "found":true
nozick          | HTTP=200 | "found":true
walzer          | HTTP=200 | "found":true
rawls           | HTTP=200 | "found":true
```

### 7-2. BLOCKER thinkers 404

```
coombs          | HTTP=404 | "found":false
fazang          | HTTP=404 | "found":false
```

### 7-3. narvaez DQ-018 override claims

```
narvaez-claim-001 | HTTP=200 | "found":true
narvaez-claim-002 | HTTP=200 | "found":true
narvaez-claim-003 | HTTP=200 | "found":true
```

### 7-4. 전체 40개 unique claim_id found=true

가이드에서 참조된 `<thinker>-claim-NNN` 토큰 40건 전수 curl 조회 → 전원 `found=true`.

- aristotle-claim-001/002/003/004/005 (5건)
- gilligan-claim-001/002/003/004 (4건)
- hume-claim-001/002/003/004 (4건)
- jeongyagyong-claim-001/002/003 (3건)
- macintyre-claim-001/002/003/004 (4건)
- mill-claim-002/010/011/012 (4건 · thinker_id=mill_js 이나 claim id prefix 는 `mill-`)
- narvaez-claim-001/002/003 (3건)
- nozick-claim-001/002/003 (3건)
- rawls-claim-001/002/003/004 (4건)
- walzer-claim-001/002/003 (3건)
- wonhyo-claim-001/002/003 (3건)

**참고 (data-quality idiosyncrasy)**: `mill_js` thinker_id 에 대한 claim 은 ES 내부에서 `mill-claim-*` prefix 로 저장되어 있음 (`mill_js-claim-*` 는 404). Coder 는 이를 정확히 반영하여 가이드에 `mill-claim-002/010/011/012` 형식으로 인용. data-quality 측면에서는 향후 일관성 검토 대상이나, 본 태스크 범위에서는 **claim 존재 확증으로 PASS 처리**.

## 8. 한자 및 em-dash 샘플 hexdump

### 8-1. em-dash U+2014 (`e2 80 94`)

- L1 offset 0x35-0x37: `41 20 e2 80 94 20 ed` = "A — 학" 에서 em-dash
- L3 offset 0xb4-0xb6: `4c 31 e2 80 94 4c 32` = "L1—L2" 에서 em-dash
- L3 offset 0xea-0xec: `ed 95 a8 20 e2 80 94 20 32 30 32 34` = "포함 — 2024"
- L4 offset 0x16c-0x16e: `28 4c 31 e2 80 94 4c 37 36 35 29` = "(L1—L765)"

4+ 샘플에서 em-dash U+2014 확증. 하이픈 `-` 대신 U+2014 로 통일된 점 verbatim 준수.

### 8-2. 한자 CJK Unified Ideographs (U+4E00-U+9FFF)

実踐(4) · 傳統(3) · 功利(4) · 超越(3) · 法藏(2) · 事事無礙法界(4) · 一心(7) · 四法界(2) · 和諍(7) · 民族大團結(3) · 特殊關係(1) 모두 UTF-8 3바이트 시퀀스 (`e4-e9`) 로 보존 확증.

## 9. fudge 문구 5차 재발 검증

`grep -cE '≈|수렴|중복 보정|대략' 2024-A.md = 0`

- `≈` = 0
- `수렴` = 0
- `중복 보정` = 0
- `대략` = 0

fudge 문구 0건 확증. 5차 재발 없음. severity=blocker 승격 경고 trigger 되지 않음.

## 10. 최종 판정 · severity=observation

### 10-0. PASS 근거

1. 12문항 전수 커버 ✓
2. 12쌍 line 범위 em-dash 포함 정확 일치 ✓
3. verbatim byte-level 25+ 토큰 보존 ✓
4. ES 11명 전수 HIT · BLOCKER 2건 404 · narvaez DQ-018 override 확증 ✓
5. 40개 claim_id 전수 found=true ✓
6. BLOCKER 4건 표기 실재 · narvaez 표기 없음 ✓ (라벨 숫자 차이는 observation)
7. 해당 없음 4개 영역 처리 ✓
8. 채점 기준 8블록 Q5—Q12 정확 매핑 ✓
9. em-dash hexdump 4+ 샘플 ✓
10. Step1=104 · Step2=37 산술 정확 일치 · fudge=0 · disjoint pairwise 0 ✓

### 10-1. observation 수준 차이 (non-blocking)

- **BLOCKER 라벨 시퀀스 차이** (관찰 1): BLK-ID 는 정확 일치. 사람 가독 라벨은 가이드 1/2/3/4 순차 vs task 명세 1/2/4/5. 학생 가독성 관점에서 Coder 선택이 합리적.
- **Step 1b narrow vs wide scope gap** (관찰 2): Coder narrow=0 자체 정확. Tester wide scope 측정 시 6 토큰 존재 (aristotle 계열 Greek 용어). 모두 verbatim·ES 근거 있음. Coder regex scope 이 좁았을 뿐 창작·fudge 아님.

### 10-2. severity=observation 판정

- 라인 범위 오기 없음 · BLOCKER 누락 없음 · fudge 검출 없음 · Coder 주장 수치 산술 일치 → **severity=bug 조건 불성립**.
- fudge 5차 재발 없음 · ES HIT 전수 확증 · 핵심 thinker 누락 없음 → **severity=blocker 조건 불성립**.
- Step 1b wide scope gap + BLOCKER 라벨 숫자 차이 2건 → **severity=observation 기록**.

### 10-3. 후속 조치 (권고, 필수 아님)

- (권고) TASK-203 이후 동일 프로토콜 적용 시 Step 1b regex scope 에 Latin+macron 결합 토큰(aretē·sōphrōn 계열) 포함 여부를 명시해 Coder/Tester 간 scope 일치 유도.
- (참고) `mill-claim-*` vs thinker_id=`mill_js` prefix 불일치는 ES 데이터 관리 이슈로 별도 DQ 검토 가능하나 본 태스크 범위 외.

## 11. 완료 조건

| 조건 | 상태 |
|------|------|
| 10항 체크 전수 수행 | pass |
| Coder 수치 (Step1 104 · Step2 37 · narrow Step1b 0) 산술 정확 일치 | pass |
| fudge 0건 확증 | pass |
| em-dash hexdump 3+ 샘플 | pass (4+ 실제 샘플) |
| ES curl 재조회 11 HIT + 2 404 + narvaez DQ-018 override 9 claims | pass |
| 40개 claim_id 전수 found=true | pass |
| 0-hit 삭제 토큰 5개 샘플 원본 검증 | pass (창작물 아님) |
| severity 판정 + 근거 | pass (observation) |
| tester-report-TASK-202-T.md 저장 | pass (본 파일) |
