---
agent: coder
task_id: TASK-198-FIX
model: opus-4.7
status: DONE
timestamp: 2026-04-23T07:30:00+09:00
target_file: projects/ethics-study/exam-solutions/study-guide/2022-A.md
depends_on: TASK-198-T
reviewer_verdict: PASS (reviewer-report-TASK-198-FIX.md)
---

## 결과 요약

2022-A 학생용 풀이 가이드(1027L · 12문항 · 40점)에서 Tester TASK-198-T가 지적한 3건 factual contradiction(bug-1·bug-2·bug-3)을 Edit tool 국소 치환으로 정정했다. Reviewer R1 PASS 수정안(6개 라인)을 그대로 적용했고 무결 부분(12문항 구조·verbatim·산술·em-dash·한자·BLOCKER 4건 표기)은 변경하지 않았다.

- **편집 지점**: 6개 라인 (L583·L588·L607·L1000·L1001·L1002·L1005 ← 단 L1001-L1002 는 2줄 단일 Edit)
- **편집 tool**: Edit (Write 미사용 — 원본 1027L 보존)
- **총 라인 수**: 1027 유지 (편집 전후 동일)
- **fudge 문구 0건**: `≈`·`수렴`·`중복 보정`·`대략` grep 결과 본 가이드 전체 0건 (제5차 재발 회피)
- **ES 재확증 curl 실측**: turiel/jinul/pettit 전원 `found=true` (HTTP 200) · turiel-claim-001~003 전원 `found=true` · claim 합계 25건(turiel 8 + jinul 9 + pettit 8)

## 변경된 파일

- `projects/ethics-study/exam-solutions/study-guide/2022-A.md` (수정 · 국소 Edit 6곳)

## 수정 diff (6개 라인 · Edit tool)

### bug-1 정정 (L583·L588·L607 turiel BLOCKER 표기 → DQ-016 override 정상 표기)

**L583 (before)**
```
- **을 identification**: **튜리엘(Elliot Turiel)** (⚠️ BLOCKER BLK-175E-2022A-004 / DQ-016 override 미적용 — 원본 ethics-thinkers ES 미등록)
```
**L583 (after)**
```
- **을 identification**: **튜리엘(Elliot Turiel)** (✅ ES 등록 · DQ-016 override · claim 8건)
```

**L588 (before)**
```
  - **DQ-016 해설**: TASK-196 세션 3차 재발 시정 대상. 현재 ES ethics-thinkers 인덱스에 turiel 미등록 → 본 study-guide는 **BLOCKER 상태 명시적 기재**. 교과서(리코나·튜리엘 영역이론 표준 설명)에 의거해 답안 개념 정리만 제공하며, "ES claim 근거"로는 인용 불가.
```
**L588 (after)**
```
  - **DQ-016 해설**: TASK-176 계열 후속 등록으로 이미 해소(2026-04-23 세션 curl 실측 확증 · `found=true` · claim 8건). coverage md 작성 시점(2026-04-21) 이후 ES 상태 변경분. 본 study-guide는 **DQ-016 override 정상 표기** 적용 — 정상 claim_id 인용 가능.
```

**L607 (before)**
```
- **⚠️ turiel**: ES 미등록(BLK-175E-2022A-004) — 본 답안은 교과서 표준 해설(튜리엘 영역이론)에 근거. ES claim_id 인용 불가.
```
**L607 (after)**
```
- **✅ turiel**: ES 등록 (DQ-016 override) — 대표 claim_id: `turiel-claim-001` · `turiel-claim-002` · `turiel-claim-003` (3영역 모델·도덕 vs 관습·사회인지 영역이론). 본 답안은 DQ-016 override 적용으로 ES claim 근거 사용 가능.
```

### bug-2 정정 (L1000 wonhyo→lickona + Q 대응 11명 정합)

**L1000 (before)**
```
- **ES 등록 사상가 (11명)**: wonhyo (Q1), jeongyagyong (Q4), nozick (Q5), plato (Q7), kohlberg (Q8갑), kant (Q9·Q11갑), huineng (Q10 을), gilligan (Q12)
```
**L1000 (after)**
```
- **ES 등록 사상가 (11명)**: lickona (Q1) · jinul (Q2 · DQ-016) · jeongyagyong (Q4) · nozick (Q5) · pettit (Q6가 · DQ-016) · plato (Q7) · kohlberg (Q8갑) · turiel (Q8을 · DQ-016) · kant (Q9·Q11갑) · huineng (Q10 을) · gilligan (Q12)
```

### bug-3 정정 (L1001-L1002 · L1005 DQ-016 override 적용 + BLOCKER 4명 + 총계 재계산)

**L1001-L1002 (before)**
```
- **DQ-016 override 후보 (3명)**: jinul (Q2), pettit (Q6가), turiel (Q8을) — coverage md에는 BLOCKER 표기였으나 ES 재확인 결과 **미등록(BLK 확정)**
- **⚠️ BLOCKER (7명)**: jinul (BLK-175E-2022A-001), pettit (BLK-175E-2022A-002), green_th (BLK-175E-2022A-003), turiel (BLK-175E-2022A-004), shenxiu (BLK-175E-2022A-005), zhiyi (BLK-175E-2022A-006), beccaria (BLK-175E-2022A-007)
```
**L1001-L1002 (after)**
```
- **DQ-016 override 적용 (3명)**: jinul (Q2) · pettit (Q6가) · turiel (Q8을) — coverage md 작성 시점에는 BLOCKER 표기였으나 2026-04-23 세션 ES 재확인 결과 **등록 확정 (`found=true` · claim 합계 25건)**. TASK-176 계열 후속 등록으로 해소.
- **⚠️ 잔존 BLOCKER (4명)**: green_th (BLK-175E-2022A-003) · shenxiu (BLK-175E-2022A-005) · zhiyi (BLK-175E-2022A-006) · beccaria (BLK-175E-2022A-007)
```

**L1005 (before)**
```
**총 15명 중 ES 등록 8명 · 미등록 BLOCKER 7명** (coverage md 원본 15명 합산 일치)
```
**L1005 (after)**
```
**총 15명 중 ES 등록 11명 (정상 8 + DQ-016 override 3) · 잔존 BLOCKER 4명** (coverage md 원본 15명 합산 일치)
```

## 재측정 3분류 수치 실측값 (Reviewer 권고 2 준수)

편집 전/후 각각 동일 regex로 `sort -u | wc -l` 실행해 변경 수치를 비교한다. fudge 문구(≈/수렴/중복 보정/대략) 일체 미사용.

### 재측정 명령 (tester-report-TASK-198-T.md L46-L48 regex 동일)

```bash
# Step 1 bare-id
grep -oE '\b(plato|kant|nozick|pettit|green_th|kohlberg|turiel|shenxiu|huineng|zhiyi|beccaria|gilligan|wonhyo|jinul|jeongyagyong|jeong_yakyong|green|lickona)\b' 2022-A.md | sort -u | wc -l
# Step 1b claim-id
grep -oE '\b[a-z_]+-claim-[0-9]+\b' 2022-A.md | sort -u | wc -l
# Step 2 TitleCase
grep -oE '\b(Plato|Kant|Nozick|Pettit|Green|Kohlberg|Turiel|Shenxiu|Huineng|Zhiyi|Beccaria|Gilligan|Wonhyo|Jinul|Jeong|Lickona|Immanuel|Carol|Lawrence|Elliot|Cesare|Thomas|Philip|Robert)\b' 2022-A.md | sort -u | wc -l
```

### 실측 결과표 (변경 전 → 변경 후 · 차이)

| Step | 변경 전 (Coder-198 · Tester-198-T 실측) | Reviewer 예측 | 변경 후 실측 | 차이 | Reviewer 예측 일치 |
|------|------------------------------------------|---------------|--------------|------|---------------------|
| Step 1 bare-id | **16** | 15 (wonhyo 제거 시) | **15** | **-1** (wonhyo 제거) | ✅ 정확 일치 |
| Step 1b claim-id | **59** | 62 (turiel-claim-001·002·003 추가) | **62** | **+3** (turiel-claim-001·002·003 추가) | ✅ 정확 일치 |
| Step 2 TitleCase | **18** | 18 유지 (Turiel 이미 포함) | **18** | **0** | ✅ 정확 일치 |
| **3분류 disjoint 총합** | **93** | **95** (15+62+18) | **95** (15+62+18) | **+2** | ✅ 정확 일치 |

**fudge 문구 실사용**: 본 report 및 2022-A.md 수정 결과 전체에서 `≈`·`수렴`·`중복 보정`·`대략` grep 결과 **0건 실사용** (제5차 재발 위협 완전 회피).

### Step 1 변경 후 전수 목록 (15명)

```
beccaria · gilligan · green_th · huineng · jeongyagyong · jinul · kant · kohlberg · lickona · nozick · pettit · plato · shenxiu · turiel · zhiyi
```

wonhyo 가 바뀐 L1000 목록에서 제거되어 Step 1 에서 감소(16→15). 문서 내 어디에도 wonhyo 가 더 이상 등장하지 않는다.

### Step 1b 변경 후 추가된 claim-id (3건)

```
turiel-claim-001
turiel-claim-002
turiel-claim-003
```

L607 정정안에 신규 추가. 기존 59건은 모두 유지되어 59+3 = 62건 (Reviewer 예측 정확 일치).

### Step 2 변경 후 전수 목록 (18명 유지)

```
Beccaria · Carol · Cesare · Elliot · Gilligan · Green · Immanuel · Kant · Kohlberg · Lawrence · Lickona · Nozick · Pettit · Philip · Plato · Robert · Thomas · Turiel
```

Turiel 은 편집 전부터 L583 "Elliot Turiel" 에 포함되어 있었고 편집 후에도 동일 위치에 유지되므로 Step 2 개수는 불변(18 유지).

## ES 실측 재확증 (curl · 2026-04-23 세션)

### DQ-016 override 3명

| thinker_id | HTTP | `found` | claim 수 |
|------------|------|---------|----------|
| ethics-thinkers/turiel | **200** | **true** | **8** |
| ethics-thinkers/jinul | **200** | **true** | **9** |
| ethics-thinkers/pettit | **200** | **true** | **8** |
| **합계** | | | **25** |

### L607 정정안에 인용된 대표 claim_id 3건

| claim_id | HTTP | `found` | 비고 |
|----------|------|---------|------|
| ethics-claims/turiel-claim-001 | 200 | **true** | 영역이론 핵심 |
| ethics-claims/turiel-claim-002 | 200 | **true** | 도덕 vs 관습 |
| ethics-claims/turiel-claim-003 | 200 | **true** | 사회인지 3영역 |

→ **L1001 "claim 합계 25건" 및 L607 "대표 claim_id 3건 인용 가능" 주장은 ES 실측과 정확 일치**.

## 무결 부분 보존 실측 확증

Reviewer 의 "무결 부분 변경 금지" 조항별 편집 후 실측:

| 항목 | 변경 전 (Tester · Coder) | 변경 후 실측 | 판정 |
|------|---------------------------|---------------|------|
| 총 라인 수 | 1027 | `wc -l == 1027` | ✅ 불변 |
| `^## 문항` 헤더 수 | 12 | `grep -c == 12` (L47·122·186·243·309·398·490·558·638·715·800·874 동일) | ✅ 불변 |
| em-dash `—` 총계 | 233 | `grep -c '—' == 233` | ✅ 불변 |
| 한자 문자수 (CJK Unified Ideographs) | 1208 (본 편집 후 기준선) | `python3 re.findall(r'[\u4e00-\u9fff]') == 1208` | ✅ 편집 라인에 한자 신규 추가 없음 |
| `<u>` open tag | 12 (Tester `grep -oE`) | `grep -oE '<u>' == 12` | ✅ 불변 (FIX 범위 밖 · 손대지 않음) |
| `</u>` close tag | 11 | `grep -oE '</u>' == 11` | ✅ 불변 |
| BLOCKER 4건 표기 (green_th·shenxiu·zhiyi·beccaria) | `grep -c '⚠️ BLOCKER BLK-175E-2022A-(003\|005\|006\|007)' == 4` | 동일 실측(L422·L741·L752·L825) | ✅ 불변 |
| BLK-175E-2022A-004 "⚠️ BLOCKER" 표기 제거 (Reviewer 완료 조건 #1) | `grep -c '⚠️ BLOCKER BLK-175E-2022A-004' == 1` 이전 | `grep -c == 0` 현재 | ✅ 완료 조건 충족 |
| wonhyo (Q1) 오기 제거 | `grep -c 'wonhyo (Q1)' == 1` | `grep -c == 0` | ✅ 완료 조건 충족 |
| lickona (Q1) 정정 | `grep -c 'lickona (Q1)' == 0` (L1000 기준) | `grep -c 'lickona (Q1)' == 1` | ✅ 완료 조건 충족 |
| "잔존 BLOCKER (4명)" 표기 | 0 | `grep -c '잔존 BLOCKER \(4명\)' == 1` | ✅ 완료 조건 충족 |
| "BLOCKER (7명)" 오표기 제거 | 1 | `grep -c 'BLOCKER \(7명\)' == 0` | ✅ 완료 조건 충족 |

## 완료 조건 체크리스트 (5개 전수 충족)

1. ✅ L583·L588·L607 turiel BLOCKER 표기 제거 + DQ-016 override 정상 표기 (`⚠️ BLOCKER BLK-175E-2022A-004` 실측 0건)
2. ✅ L1000 wonhyo→lickona + Q 대응 11명 정합 (`wonhyo (Q1)` 0건 · `lickona (Q1)` 1건 · 11명 목록 L18 요약표와 정합)
3. ✅ L1001-L1002·L1005 DQ-016 override 적용/잔존 BLOCKER 4명/총계 재계산 정합 (`잔존 BLOCKER (4명)` 1건 · `BLOCKER (7명)` 0건 · "ES 등록 11명 (정상 8 + DQ-016 override 3)" 명시)
4. ✅ 12문항 구조·산술·verbatim 무결 유지 (문항 12건 · em-dash 233 · `<u>` 12/11 · 한자 1208 · 총 1027L 불변)
5. ✅ coder-report-TASK-198-FIX.md 에 diff·재측정 3분류 수치 실측값·BLOCKER 실측 재확증(curl) 포함 · fudge 문구 0건

## 이슈/블로커

### OBS-1 (FIX 범위 밖 · 손대지 않음): L627 "(⚠️ BLK-175E-2022A-004)" 잔존

**위치**: L627 `4. **을 사상가 확정**: "영역 구분 + 도덕 vs 인습 vs 개인 + 영역 혼합·2차적 현상·애매성" 3중 trademark → **튜리엘**. (⚠️ BLK-175E-2022A-004)`

**상태**:
- Reviewer 완료 조건 #1 `grep -c '⚠️ BLOCKER BLK-175E-2022A-004' == 0` 패턴은 **"BLOCKER" 단어를 포함하는 형태**에만 매칭 → L627 의 `(⚠️ BLK-175E-2022A-004)` (BLOCKER 단어 없음)는 grep 0 에 이미 부합하여 **완료 조건 충족**.
- 본 줄은 Tester TASK-198-T의 bug-1 지적(L583·L588·L607)에도, Reviewer R1 수정안(6개 라인)에도 포함되지 않음 → **Manager FIX spec 의 "무결 부분 변경 금지" 조항 · Reviewer 권고 "Write 전략 지양 · 국소 Edit" 범위 밖**.
- 그러나 L583 을 `✅ ES 등록` 으로 정정한 결과 L627 의 `⚠️ BLK-175E-2022A-004` 표기와 **문서 내부 사소 모순**이 잔존. 학생 혼란 가능성은 L583·L607 대비 낮음(풀이 과정 단계 식별 괄호의 사소 메모).

**처분**: Manager 판단으로 후속 TASK-199 등 별도 FIX 태스크로 분리 가능. 본 TASK-198-FIX 범위에서는 **의도적으로 손대지 않음** (task spec · Reviewer 권고 준수).

### OBS-2 (FIX 범위 밖 · 참고): `<u>` 태그 open 12 / close 11 불균형

- Reviewer R1 L58·L132 명시: `<u>` open 12 / close 11 불균형은 description 영역 L1017 잉여 `<u>` 1개 추정 · **FIX 범위 밖 · 손대지 말 것**
- 본 Coder 는 `<u>` 태그를 일체 편집하지 않았고 편집 후 실측도 동일(open 12 / close 11 유지).
- 후속 태스크에서 처리 여부 Manager 판단.

## 선례 연속성

- **TASK-196**: 제3차 재발(fudge `≈`·`수렴` 대거 사용) 시정 실패 선례
- **TASK-197-T**: 제4차 재발 시정 확증 PASS (fudge 0건)
- **TASK-198**: 제5차 재발 위협 회피 (fudge 0건 · 산술 정확) 단 문서 내부 factual contradiction 3건 발견
- **TASK-198-FIX (본 report)**: 3건 factual contradiction 정정 완료. 재측정 3분류 수치 `15+62+18=95` 로 변경 전 `16+59+18=93` 대비 +2 (wonhyo -1, turiel-claim 3건 +3, Step2 ±0). Reviewer 예측과 정확 일치. fudge 0건 재엄수. ES curl 실측 25건 claim 재확증.

## 다음 제안

1. **TASK-198-FIX-T (Tester 재검증)** 호출 권고 — Reviewer R1 L101 · task-board.md L339 등록 상태. 7항 체크 리스트(Reviewer 지정) 전수 실행하여 본 6개 라인 정정이 문서 내부 factual consistency 를 완전 확보했는지 확증.
2. **Manager 판단 사항 (OBS-1)**: L627 `(⚠️ BLK-175E-2022A-004)` 잔존을 별도 TASK-199 로 분리할지, 본 FIX 범위가 이미 PASS 기준을 충족하므로 보류할지 판단 필요. Reviewer 완료 조건은 이미 충족(grep 0건).
3. **Manager 판단 사항 (OBS-2)**: `<u>` open 12 / close 11 불균형(L1017 description 영역 추정)은 본 FIX 와 독립. 별도 cleanup 태스크 검토.
4. **TASK-198-T · TASK-198-FIX 세트 종결 시 2022-A.md 정정 반영본을 signal/ethics-study/done-log.md 에 append 권고** (bug severity 해소 기록 + 재측정 수치 `15+62+18=95` 명시).
