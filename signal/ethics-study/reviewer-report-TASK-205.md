---
task_id: TASK-205 (+ TASK-DQ-021 · TASK-205-T 동반 검증)
verdict: NEEDS_REVISION
---

# Reviewer Report: TASK-205 · TASK-DQ-021 · TASK-205-T

## 검증 대상
- 파일:
  - `signal/ethics-study/task-board.md` L356 (TASK-DQ-021 row)
  - `signal/ethics-study/task-board.md` L357 (TASK-205 row)
  - `signal/ethics-study/task-board.md` L358 (TASK-205-T row)
- 참조:
  - `projects/ethics-study/exam-solutions/coverage/2025-B.md` (550L)
  - `/home/jai/잡동사니/임용/md/2025_중등1차_도덕·윤리_전공B.md` (206L)
  - `signal/ethics-study/data-quality-log.md` (선례 DQ-019 L203 · DQ-020 L232)
  - `signal/ethics-study/tester-report-TASK-204-T.md` (verdict=PASS)

## Manager 주장 요약
1. **TASK-DQ-021**: coverage BLOCKER 6건 중 4명(jinul·moore·bandura·pettit)이 실제 ES `found=true` 재조회 (9·7·8·8 claims=32). 잔존 BLOCKER 2건: berlin + Q7 갑.
2. **TASK-205**: 2025-B 신규 study-guide 작성. 11문항 (Q1·Q2 기입 2점×2 + Q3~Q11 서술 4점×9) = 40점. 원문 라인 Q1=L16·Q2=L32·Q3=L42·Q4=L66·Q5=L83·Q6=L105·Q7=L122·Q8=L138·Q9=L156·Q10=L173·Q11=L190.
3. **TASK-205-T**: 10항 체크리스트 · TASK-205 Depends On.

## 검증 결과

### 파일 존재
| 경로 | 존재 | 비고 |
|------|------|------|
| `projects/ethics-study/exam-solutions/coverage/2025-B.md` | OK | 53985B · 550L (주장 일치) |
| `/home/jai/잡동사니/임용/md/2025_중등1차_도덕·윤리_전공B.md` | OK | 22236B · 206L (주장 일치) |
| `projects/ethics-study/exam-solutions/study-guide/2025-B.md` | 아직 없음 (정상, 신규 작성 대상) | 2015-B~2025-A 20개 파일 존재 확인 |
| `signal/ethics-study/data-quality-log.md` | OK · 24074B · DQ-019/DQ-020 선례 기록 확인 (L203·L232) |
| `signal/ethics-study/tester-report-TASK-204-T.md` | OK · verdict=PASS · severity=observation |

### 원문 라인·배점 실측 (일치)
`awk 'NR==L'` 실측 + `grep -nE '^### [0-9]+\.'` 결과:
| Q | Manager 주장 라인 | 실측 헤더 | 배점 | 일치 |
|---|---|---|---|---|
| Q1 | L16 | `### 1. [2점]` | 2 | OK |
| Q2 | L32 | `### 2. [2점]` | 2 | OK |
| Q3 | L42 | `### 3. [4점]` | 4 | OK |
| Q4 | L66 | `### 4. [4점]` | 4 | OK |
| Q5 | L83 | `### 5. [4점]` | 4 | OK |
| Q6 | L105 | `### 6. [4점]` | 4 | OK |
| Q7 | L122 | `### 7. [4점]` | 4 | OK |
| Q8 | L138 | `### 8. [4점]` | 4 | OK |
| Q9 | L156 | `### 9. [4점]` | 4 | OK |
| Q10 | L173 | `### 10. [4점]` | 4 | OK |
| Q11 | L190 | `### 11. [4점]` | 4 | OK |

**배점 합**: 2+2+4+4+4+4+4+4+4+4+4 = 40 ✓ (기입 4 + 서술 36 = 40)
**문항 수**: 11개 (`grep -nE '^### [0-9]+\.'` 11 hits) ✓

### ES 실측 (DQ-021 override 대상)
`curl localhost:9200/ethics-thinkers/_doc/{id}` + `_search q=thinker_id:{id}` 결과:
| id | found | claims | Manager 주장 | 판정 |
|---|---|---|---|---|
| jinul | true | **9** | 9 | OK |
| moore | true | **7** | 7 | OK |
| bandura | true | **8** | 8 | OK |
| pettit | true | **8** | 8 | OK |
| **합계** | — | **32** | 32 | OK |
| berlin | **false** | 0 | BLOCKER 유지 | OK |
| viroli | **false** | 0 | 후보 (coverage 양립) | OK |
| yihwang | true | 12 | Q7 갑 후보 | OK |
| im_seongju | false | 0 | Q7 갑 후보 | OK |
| han_wonjin | false | 0 | Q7 갑 후보 | OK |

### 2025-B 원문 甲/乙 한자 부재 (Manager 주장 확증)
```
grep -cE '甲|乙' 2025_B.md → 0
grep -cE '갑|을' 2025_B.md → 52
```
**갑/을 한글만 사용** 주장 일치 ✓. Manager가 task-board 본문에서 "2025-B 원문에는 甲/乙 한자 없음, 갑/을 한글만 사용"을 명시한 점 확인(L357).

### 선행 태스크·의존성
- **TASK-204-T** L355: DONE (verdict=PASS severity=observation · 2026-04-23T10:15 완료) ✓
- **TASK-DQ-021** Depends On: `TASK-176` — 과거 선례 DQ-019/DQ-020 에서도 `TASK-176` 을 선행으로 둠. 정합.
- **TASK-205** Depends On: `TASK-204-T · TASK-DQ-021` — 정합.
- **TASK-205-T** Depends On: `TASK-205` — 정합.
- 선례 DQ-019 (2024-B, 5건 override · regan 1건 유지) · DQ-020 (2025-A, 2건 override · zhiyi 1건 유지) 패턴을 DQ-021 이 계승 (4건 override · 2건 유지). 구조적 일관성 확인.

### 태스크 완결성
- TASK-205 row 는 Q1~Q11 전 문항 thinker_id·ES hit·trademark·재출제 이력을 제시문 별 상세히 열거 → Coder 외부 질문 없이 실행 가능 수준.
- 분량 목표 700L, Split-Write 전략, 3-step 자기검증, fudge 금지, verbatim 보존, em-dash U+2014 hexdump 등 TASK-204 선례 엄수 조건 모두 명시.
- TASK-205-T 10항 체크리스트는 커버리지·라인·배점·채점기준·자기검증·DQ-021 override·BLOCKER 유지·verbatim·fudge·0-hit 역조회 전 범위 포함.

## 판정
**NEEDS_REVISION**

치명 결함은 아니나 Coder에게 전달되기 전 반드시 정정되어야 할 **정합성 결함 1건** + **사소한 문구 명확화 1건**이 있다.

---

## 수정 요청 (NEEDS_REVISION 시)

### 【수정 1 — Q10 갑 pettit 확정 근거 명시 (MUST)】

**문제점**: coverage/2025-B.md L320, L335-L337, L339, L363-L366, L414, L453, L468, L489, L538 는 Q10 갑을 `viroli 또는 pettit` **양립**으로 기록하고 "BLK-175E-2025B-004 로 등록 유지"라고 명시한다. 그러나 Manager는 TASK-205 row 에서 **pettit 단일 확정**(`pettit (DQ-021 override · ES HIT · 8 · 갑)`)으로 내려 썼다. DQ-021 row 는 이 결정 근거를 `"pettit 가정"` 이라고 에두르며, 왜 pettit 으로 확정했는지(ES 실재 + 2019-A·2020-A·2022-A 기출 연속성)는 task-board 문맥 안에 **명시적 서술 없음**.

**이 불일치를 해소하지 않으면**: Coder 가 coverage 와 task-board 를 교차 읽을 때 어느 쪽이 ground truth 인지 판단 불가 → (a) viroli/pettit 양쪽 나열, (b) pettit 단독 서술, (c) 임의 선택 중 하나를 시도하게 됨. Reviewer 가 PASS 하면 Coder 가 가드레일 없이 진행하므로 study-guide 내 판단 오류 risk가 남는다.

**수정 방안** (TASK-205 row 또는 TASK-DQ-021 row 중 한 곳에 명시):
- TASK-DQ-021 row 에 다음 1문장 삽입 권고:
  > "BLK-175E-2025B-004 는 coverage L320 에서 viroli/pettit 양립 후보였으나, 실제 ES 재조회 결과 pettit `found=true` (8 claims, 2019-A·2020-A·2022-A 3회 기출 ES 연속성) · viroli `found=false` (ES 미등록). 따라서 본 DQ-021 override 는 `pettit` 단일 확정으로 귀결. viroli 후보는 폐기. coverage md 원본 미수정."
- 그리고 TASK-205 row Q10 서술 말미에 `(DQ-021 에서 viroli→pettit 단일 확정 근거 명시)` 짧은 cross-ref 추가.

### 【수정 2 — DQ-021 BLK-175E-2025B-004 "pettit 가정" 문구의 모호성 (SHOULD)】

**문제점**: TASK-DQ-021 row 본문 "BLK-175E-2025B-001 (jinul) · BLK-175E-2025B-002 (moore) · BLK-175E-2025B-003 (bandura) · BLK-175E-2025B-004 (**pettit 가정**) false-positive". "pettit 가정"은 coverage md L320·L365 의 "`viroli`(또는 `pettit`)" 양립 상태를 존중하는 표현이지만, 같은 태스크 본문에서 claim=8 · 32 합계 확정으로 쓰여 **가정/확정의 어투 충돌**. 독자(Coder)는 "가정을 override 로 쓴다"는 모호함을 느낄 수 있다.

**수정 방안**:
- "BLK-175E-2025B-004 (**Q10 갑 `pettit` · coverage viroli 대안 폐기 · ES `found=true` 8 claims**) false-positive" 로 표현 일원화.

---

## 추가 확인 사항 (PASS 전 Manager 자체 확증 요청, 수정 대상 아님)

1. **coverage md L468** 에 "viroli 가정 시 2회(2023-A·2025-B)" 라고 적혀 있음. DQ-021 에서 pettit 으로 귀결시키면 이 2회 카운트는 **pettit 기준 4회(2019-A·2020-A·2022-A·2025-B)** 로 재계산됨. study-guide 의 재출제 이력 서술(`2019-A·2020-A·2022-A·2025-B 4회째`)이 이 재계산과 일관되는지 Coder 에게 명시 전달 권고. (현 TASK-205 row Q10 서술에는 기출 이력 회차 미표기 — Q4 gilligan "3회째" 등 다른 문항 포맷과 비대칭)
2. **Q7 갑 BLK-175E-2025B-006**: 원문 L124 "기가 아니면 이는 붙을 데가 없고… 사덕의 이… 오상… 기질은 ( ㉠ )이 아니어서 칠정으로 흐름" 직접 읽음. 후보 3명(yihwang·im_seongju·han_wonjin) 중 yihwang 만 ES HIT(12 claims). im_seongju·han_wonjin MISS. Manager 가 "사상가 확증 보류"로 BLOCKER 유지 판정은 trademark 배타성 부재 기준 합리. 단 교과서 범위 내 대체 해설 서술 시 yihwang 설(ES 근거 있음) 치우침을 피하고 세 후보 중립 서술하도록 Coder 명시 전달 권고.
3. **TASK-205-T 체크리스트 (6)**: "DQ-021 override 4명 (jinul 9 · moore 7 · bandura 8 · pettit 8)" 수치 task-board 와 일치 · ES 실측과도 일치. OK.
4. **선례와의 규모 비교**: DQ-019=5건 · DQ-020=2건 · DQ-021=**4건**. 모두 TASK-176 등록 후행. 패턴 일관.
5. **분량 목표 700L**: 2024-B(757L) · 2025-A(705L) 선례 근접. 합리.

---

## Manager에게 전달

**다음 단계**:
1. 위 【수정 1】 을 TASK-DQ-021 및/또는 TASK-205 row 에 반영 (pettit 단일 확정 근거 1문장 삽입).
2. 위 【수정 2】 "pettit 가정" → "pettit 확정" 어투 정리.
3. 재호출 시 Reviewer 는 위 2개 항목만 재확인 → PASS 가능.
4. 【추가 확인 사항】 1~2 는 PASS 에 필수 아님. 다만 Coder 지시 품질 향상 관점에서 권고.

**파일 라인·배점·ES 실측·의존성·목적성·분리 원칙·선례 일관성은 모두 통과**. Q10 갑 양립→단일 확정 근거의 task-board 내 **명시성** 결함만 해소하면 TASK-205/205-T 는 Coder/Tester 투입 가능.

Reviewer 는 코드·task-board 수정 없이 본 보고서로만 회신한다.
