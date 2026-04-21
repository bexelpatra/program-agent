---
task_id: TASK-175E-2025-B-FIX
agent: coder
status: DONE
severity: bug (3 BUG + 3 observation 해소)
date: 2026-04-21
reviewer_verdict_referenced: (본 FIX는 Tester NEEDS_REVISION 후속이므로 별도 Reviewer 검증 없이 Tester 지적 반영)
parent_task: TASK-175E-2025-B
tester_report_referenced: tester-report-TASK-175E-2025-B.md
phase: 6
files_changed: 4
---

# Coder Report — TASK-175E-2025-B-FIX (2025-B 커버리지 3 BUG 정정)

## 1. 작업 요약

Tester가 `tester-report-TASK-175E-2025-B.md`에서 판정한 **NEEDS_REVISION (severity=bug)** 3 BUG + 3 observation을 전면 반영. src 디렉토리·테스트 코드는 **수정하지 않고** 문서만 정정.

**정정 대상 4개 파일**:
1. `projects/ethics-study/exam-solutions/coverage/2025-B.md` (Q1·Q6·Q7·Q10 섹션 + 요약 테이블 + 최종 판정 + ES dump 결과 + 블로커 인덱스)
2. `signal/ethics-study/blocker-log.md` (BLK-175E-2025B-006 전면 재정의)
3. `signal/ethics-study/coder-report-TASK-175E-2025-B.md` (1.작업 요약·2.결과 HIT/MISS 갱신·BLK-006 설명)
4. `signal/ethics-study/coder-report-TASK-175E-2025-B-FIX.md` (본 파일, 신규)

**결과 HIT/MISS 재집계**: HIT **10** / MISS 6 (고유 thinker_id 기준; `yiyulgok` HIT 유지 + 갑 사상가 확증 보류는 미확정 MISS로 계상).

**배점 총합 재확인**: 40점 일치 (Q1·Q2 = 2점×2 + Q3~Q11 = 4점×9).

## 2. BUG별 정정 지점 및 근거

### BUG-1 해소 — Q1 발문 재해석

**문제**: 이전 판본은 Q1을 단순 "괄호 기입형"으로 처리하고 ㉠ 불성·㉡ 정·㉢ 혜 추정 정답을 서술. 실제 원문 발문(L18)은 "밑줄 친 ㉠~㉣ 중 **옳지 않은 것 2가지**를 찾아 바르게 고쳐 쓰시오".

**정정 지점**: `coverage/2025-B.md` Q1 섹션 전체 재작성.

**정정 내용**:
- ㉠ **불성(佛性) ✓**: "부처가 될 수 있는 성품" = 불성 정의 일치 (원문 L22).
- ㉡ **돈오(頓悟) ✓**: "수행에 앞서 단박에 깨치는 것" = 돈오 정의 일치 (원문 L24).
- ㉢ **돈수(頓修) → 점수(漸修)로 교정**. 원문 L26 "오랜 기간 익힌 습기를 갑자기 모두 제거할 수는 없으므로 **깨달음에 의지하여 점차로 수행하는 것**"은 점수(漸修) 정의이며, 돈수(단박 수행)와 정반대.
- ㉣ **자성정혜(自性定慧) → 수상정혜(隨相定慧)로 교정**. 원문 L28 "선정(定)과 지혜(慧)를 **임시적인 방편으로 빌려 사용하는 것**"은 지눌 『권수정혜결사문』의 수상정혜(隨相定慧, 상을 따라 정·혜를 빌려 씀) 정의. 자성정혜는 "자성에 구족된 정·혜를 그대로 닦음"으로 정반대.

**근거 원문 구절**:
- L18 발문: "밑줄 친 ㉠～㉣ 중 옳지 않은 것 2가지를 찾아 바르게 고쳐 쓰시오"
- L26 ㉢ 돈수 설명: "오랜 기간 익힌 습기(習氣)를 갑자기 모두 제거할 수는 없으므로 **깨달음에 의지하여 점차로 수행하는 것**"
- L28 ㉣ 자성정혜 설명: "선정(定)과 지혜(慧)를 **임시적인 방편으로 빌려 사용하는 것**"

### BUG-2 해소 — Q6·Q7·Q10 trademark 원문 한글 구절 교체

**문제**: architecture.md L580-L582 "grep 0건 규칙" 위반. 이전 판본은 원문에 존재하지 않는 한자 trademark(心卽理·心外無物·心外無理·性卽理·格物致知·窮理·氣發理乘一途·비지배)를 사상가 확정 근거로 cite.

**정정 지점**: `coverage/2025-B.md` Q6·Q7·Q10 섹션에서 trademark 인용부를 **원문 실존 한글 구절**로 교체.

**정정 내역**:

| Q | 이전 한자 trademark (grep 0건) | 교체된 원문 한글 구절 | 원문 라인 |
|---|---|---|---|
| Q6 갑 | `心卽理` | "내 마음은 곧 이치이고 허령하여 밝게 지각하는 것" | L111 ㉠ |
| Q6 갑 | `心外無物`·`心外無理` | "마음 밖에 따로 사물이 없으니" | L111 |
| Q6 을 | `性卽理` | "본성은 곧 이치이고 하늘이니" | L112 |
| Q6 을 | `格物致知`·`窮理` | "이치를 궁구하는 것" | L112 밑줄 ㉣ |
| Q7 갑 | `氣發理乘一途` / `기발이승일도` | (갑 재배치 후 삭제; 원문 갑은 "기질은 ㉠이 아니어서 그 발한 바가 칠정이 되고 사악함으로 흐르기 쉽다" L128) | L128 |
| Q7 을 | (기존 임성주/한원진 trademark → 율곡 trademark로 교체) | "이와 기의 오묘함[理氣之妙]은 이해하기가 어렵고 말하기도 어렵다" · "이(理)의 근원은 하나일 뿐이고, 기의 근원도 하나일 뿐이다. 기가 유행하여 고르지 못하면 이도 유행하여 고르지 못하니" · "기는 이와 떨어질 수 없고 이도 기와 떨어질 수 없다" | L129 |
| Q10 갑 | `비지배(non-domination)` | "특정인 또는 특정 집단의 자의에 예속되지 않는 것" · "스스로의 의지에만 종속된다" · "자치적 정치체제" | L179 |

**사상가 식별은 유지**: wang_yangming(Q6 갑) / zhuxi(Q6 을) / yiyulgok(Q7 을) / viroli·pettit 후보(Q10 갑) / berlin(Q10 을). 확정 근거만 원문 한글 구절로 교체.

### BUG-3 해소 — Q7 갑·을 재배치

**문제**: 이전 판본 Q7 갑=`yiyulgok`, 을=임성주/한원진 추정은 역전 가능성. 을 원문(L129)의 "이기지묘(理氣之妙)"·"이의 근원 하나+기의 근원 하나+기 유행 불균등→이 유행 불균등"·"기와 이 상호 불가분"은 율곡 trademark 3중.

**정정 지점**: `coverage/2025-B.md` Q7 섹션 전면 재작성 + 요약 테이블 + ES dump 대조표 + 블로커 인덱스 + `blocker-log.md` BLK-175E-2025B-006 전면 재정의.

**정정 내용**:

**을 = `yiyulgok` 확정 (HIT)**:
- ① "**이와 기의 오묘함[理氣之妙]은 이해하기가 어렵고 말하기도 어렵다**" (L129) = 율곡 『답성호원』 "理氣之妙 難見亦難說" trademark 한글 직역. 원문에 한자 `[理氣之妙]`가 대괄호 주석으로 병기됨.
- ② "**이(理)의 근원은 하나일 뿐이고, 기의 근원도 하나일 뿐이다. 기가 유행하여 고르지 못하면 이도 유행하여 고르지 못하니**" (L129) = 율곡 **이통기국(理通氣局)** 정식 명제의 원문 한글 재서술.
- ③ "**기는 이와 떨어질 수 없고 이도 기와 떨어질 수 없다**" (L129) = 율곡 **이기불상리(理氣不相離)** 정식 명제의 원문 한글 정식화.
- 보조: "상지와 하우는 바뀌지 않는다"(공자 인용, 율곡 『성학집요』에서 활용), "기질지성"(율곡 심성론 trademark).

**갑 = 사상가 확증 보류 (BLK-175E-2025B-006 재정의)**:
- 갑 원문(L128)의 trademark: (a) "기가 아니면 이는 붙을 데가 없고, 마음이 아니면 이와 기는 붙을 데가 없다" (b) "이는 사덕의 이이면서 오상이 되고, 기는 음양오행의 기이면서 기질이 되니" (c) "기질은 ㉠이 아니어서 그 발한 바가 칠정이 되고 사악함으로 흐르기 쉽다".
- 후보 검토:
  - **퇴계 이황(`yihwang`, HIT)**: 이기호발설 구도와 유사하나 "이발이기수지·기발이이승지" 양발이 아닌 단일 기발 설명만 있어 배타적 확정 불가.
  - **율곡 이이(`yiyulgok`, HIT)**: (a)(b)는 율곡 『성학집요』 해석과도 상통하나 을이 이미 율곡이므로 **배제**.
  - **한원진(`han_wonjin`, ES 미등록)**: 본연지성 3층설(超形氣·因氣質·雜氣質) 정교한 층위와 본 갑 원문의 단순 2층 구도(오상/기질)는 결이 다름. 배타적 trademark 부재.
  - **임성주(`im_seongju`, ES 미등록)**: 기일원론과 본 갑 원문의 이·기 대립적 역할 명시는 거리 있음. 배타적 trademark 부재.
- **창작 금지 규칙(architecture.md L578, Phase 6) 준수**: 단일 확증 불가로 보류.

### Observation 해소

**OBS-1 (배점 귀속 정정)**:
- 원문 L16 Q1 [2점] · L32 Q2 [2점] · L42 Q3 [4점] · L66 Q4 [4점] · L83 Q5 [4점] · L105 Q6 [4점] · L122 Q7 [4점] · L138 Q8 [4점] · L156 Q9 [4점] · L173 Q10 [4점] · L190 Q11 [4점] 직접 확인.
- 이전 판본 Q2·Q8 = 2점 오배정 → **Q1·Q2 = 2점, Q8 = 4점**으로 정정. 요약 테이블 배점 컬럼 갱신.
- 배점 합계 40점 유지 (Q1·Q2 2점×2 + Q3~Q11 4점×9 = 4 + 36 = 40).

**OBS-2 (HIT/MISS 카운트)**: 
- FIX 후 HIT = 10명 (lickona·kohlberg·gilligan·wangyangming·zhuxi·yiyulgok·kant·bentham·mill_js·hobbes).
- MISS = 6건 (jinul·moore·bandura·viroli/pettit·berlin·Q7 갑 미확정).
- 이전 판본 "HIT 9 / MISS 6"은 Q7을 "yiyulgok×1 + 미확정×1" 복합으로 계상하여 혼란. FIX 후 yiyulgok HIT 명확히 확정 + Q7 갑 미확정 별도 MISS 계상으로 HIT 10·MISS 6 명시.

**OBS-3 (pettit 기출 이력 누락)**: Tester 지적대로 pettit은 2019-A·2020-A·2022-A 기출 이력 있음. BLK-175E-2025B-004 설명에 pettit 우선순위 반영.

## 3. 변경 파일

1. **`projects/ethics-study/exam-solutions/coverage/2025-B.md`** (수정)
   - 파일 헤더(L7) 배점 설명 정정: "기입형 2점 2문항 = Q1·Q2 + 서술형 4점 9문항 = Q3~Q11"
   - Q1 섹션 전체 재작성 (발문·해답·trademark·해설 모두 "옳지 않은 것 2가지" 틀로)
   - Q6 섹션 재작성 (원문 L111·L112 한글 구절로 trademark 교체, wang_yangming/zhuxi 식별 유지)
   - Q7 섹션 전면 재작성 (갑/을 재배치: 을=yiyulgok 확정 / 갑=보류)
   - Q10 섹션 재작성 (원문 L179·L180 한글 구절로 trademark 교체, viroli/pettit/berlin 식별 유지)
   - 요약 테이블 갱신 (배점 Q1·Q2 = 2점 명시 / Q7 갑·을 재배치 / HIT/MISS 재집계)
   - ES dump 결과 "HIT 9 / MISS 6" → "HIT 10 / MISS 6" 갱신
   - 블로커 인덱스 BLK-006 재정의 반영
   - 최종 판정 섹션 갱신 + FIX 이력 추가

2. **`signal/ethics-study/blocker-log.md`** (수정)
   - BLK-175E-2025B-006 전면 재정의 (Q7 을 미확정 → Q7 갑 확증 보류; 을=yiyulgok HIT 확정 기술)

3. **`signal/ethics-study/coder-report-TASK-175E-2025-B.md`** (수정)
   - 1.작업 요약 HIT/MISS 갱신
   - 2.결과 문항별 thinker_id 목록 갱신 (Q1 발문·Q6·Q7·Q10 trademark·Q7 재배치)
   - 2.2 배점 검산 정정 (Q1·Q2 = 2점 / Q8 = 4점)
   - 2.3 블로커 인덱스 BLK-006 설명 갱신

4. **`signal/ethics-study/coder-report-TASK-175E-2025-B-FIX.md`** (신규, 본 파일)

## 4. 이슈/블로커

### 4.1 잔존 블로커 (FIX 후에도 유지)
- **BLK-175E-2025B-001~005**: ES-gap 블로커로 유효 (jinul·moore·bandura·viroli/pettit·berlin). 재출제 이력·trademark 식별 모두 유효.
- **BLK-175E-2025B-006 (재정의)**: Q7 갑 사상가 확증 보류. 창작 금지 규칙에 따라 단일 사상가 확정 금지. TASK-176에서 호락논쟁 사상가 일괄 등록 검토 권고.

### 4.2 FIX에서 해소된 이슈
- BUG-1: Q1 발문 오독 해소 (옳지 않은 것 2가지 = ㉢·㉣).
- BUG-2: Q6·Q7·Q10 한자 trademark 날조 해소 (원문 한글 구절로 교체, grep 0건 규칙 준수).
- BUG-3: Q7 갑·을 역전 해소 (을=yiyulgok 확정, 갑=보류).
- OBS-1: Q1·Q2 배점 2점·Q8 배점 4점으로 정정.
- OBS-2: HIT 10 / MISS 6 재집계.
- OBS-3: pettit 기출 이력 4회(2019-A·2020-A·2022-A·2025-B) 맥락 반영.

### 4.3 범위 외 (src 수정 금지 준수)
- src 디렉토리·테스트 코드는 수정하지 않음. FIX는 문서 정정 전용.

## 5. 자체 검증 증거

### 5.1 현 세션 Read 호출
- `/home/jai/program-agent/agents/coder.md` (전체)
- `/home/jai/program-agent/signal/ethics-study/tester-report-TASK-175E-2025-B.md` (전체, 315 lines)
- `/home/jai/program-agent/projects/ethics-study/exam-solutions/coverage/2025-B.md` (전체, FIX 전 472 lines)
- `/home/jai/잡동사니/임용/md/2025_중등1차_도덕·윤리_전공B.md` (전체 206 lines — Q1/Q6/Q7/Q10 원문 재확인)
- `/home/jai/program-agent/signal/ethics-study/blocker-log.md` L970-L1023 (BLK-175E-2025B-001~006 현재 기록)
- `/home/jai/program-agent/signal/ethics-study/coder-report-TASK-175E-2025-B.md` (전체)
- `/home/jai/program-agent/signal/ethics-study/architecture.md` L540-L590 (Phase 6 Coder 규칙 L544·창작 금지 L578·grep 0건 규칙 L580)

### 5.2 Bash / ES 실행
- `curl -s "localhost:9200/ethics-thinkers/_search?size=100&_source=id"` → 55 thinker dump (`yihwang` HIT 포함 재확인, `im_seongju`·`han_wonjin` 미등록 재확인)

### 5.3 배점 재확인 (원문 직독)
- L16: "### 1. [2점]" ✓ Q1 = 2점
- L32: "### 2. [2점]" ✓ Q2 = 2점
- L42·L66·L83·L105·L122·L138·L156·L173·L190: 각 "### N. [4점]" ✓ Q3~Q11 = 4점
- 합계: 2×2 + 4×9 = 4 + 36 = 40점 ✓

### 5.4 grep 0건 규칙 재검증 (원문 한글 구절 존재 확인)
- Q1 "옳지 않은 것 2가지" → 원문 L18 존재 ✓
- Q1 "점차로 수행" → 원문 L26 존재 ✓
- Q1 "임시적인 방편으로 빌려 사용" → 원문 L28 존재 ✓
- Q6 갑 "마음[心] 밖에 따로 사물[物]이 없으니" → 원문 L111 존재 ✓
- Q6 갑 "내 마음은 곧 이치이고" → 원문 L111 존재 ✓
- Q6 갑 "허령하여 밝게 지각하는 것" → 원문 L111 밑줄 ㉠ 존재 ✓
- Q6 을 "본성은 곧 이치이고 하늘이니" → 원문 L112 존재 ✓
- Q6 을 "이치를 궁구하는 것" → 원문 L112 밑줄 ㉣ 존재 ✓
- Q6 을 "강학을 멈춰서는 안 된다" → 원문 L112 존재 ✓
- Q7 을 "이와 기의 오묘함[理氣之妙]" → 원문 L129 존재 ✓ (`[理氣之妙]` 한자 대괄호 병기 포함)
- Q7 을 "이의 근원은 하나일 뿐이고, 기의 근원도 하나일 뿐이다" → 원문 L129 존재 ✓
- Q7 을 "기는 이와 떨어질 수 없고 이도 기와 떨어질 수 없다" → 원문 L129 존재 ✓
- Q7 갑 "이와 기의 집이 된다" → 원문 L128 존재 ✓
- Q7 갑 "기질은 ( ㉠ )이/가 아니어서" → 원문 L128 존재 ✓
- Q10 갑 "특정인 또는 특정 집단의 자의에 예속되지 않는 것" → 원문 L179 존재 ✓
- Q10 갑 "스스로의 의지에만 종속된다" → 원문 L179 존재 ✓
- Q10 갑 "자치적 정치체제" → 원문 L179 밑줄 ㉡ 존재 ✓
- Q10 을 "소극적 자유" → 원문 L180 존재 ✓
- Q10 을 "나를 지배하는 자가 누구인가" → 원문 L180 존재 ✓
- Q10 을 "통제의 근원이 아닌 통제의 범위" → 원문 L180 존재 ✓

## 6. 다음 제안 (Manager 판단용)

### 6.1 Reviewer 재검증 권고
본 FIX는 Tester NEEDS_REVISION 후속이나 Tester report 자체가 원문 실증에 근거하므로 Reviewer 재호출 여부는 Manager 판단. 필요 시 `reviewer-report-TASK-175E-2025-B-FIX.md` 생성을 지시.

### 6.2 TASK-175E-2025-B-FIX-2 (Q7 갑 확증 추가 조사, 선택)
원문 한계로 갑 확증 불가. 임용시험 기출 해설집·한국 성리학사 교재 교차 확인을 위한 별도 FIX 태스크 등록 시, Coder가 아닌 사용자(도메인 전문가) 실행이 적합. Execution=user 태스크로 제안.

### 6.3 TASK-176 우선순위 재확인
BLK-175E-2025B-001~006 우선순위는 이전 coder-report-TASK-175E-2025-B.md 5.3에 기재된 대로 유지. `bandura`·`durkheim` 최상위 긴급 / `zhiyi`·`hoffman` 최우선.

## 7. 자체 검증 체크리스트
- [x] Tester report 전문 독해 (tester-report-TASK-175E-2025-B.md)
- [x] 원문 2025_중등1차_도덕·윤리_전공B.md Q1/Q6/Q7/Q10 재독
- [x] 배점 11문항 원문 직접 확인 (L16·L32·L42·L66·L83·L105·L122·L138·L156·L173·L190)
- [x] Q1 발문 "옳지 않은 것 2가지" 재독 + ㉢·㉣ 교정 확정
- [x] Q6·Q7·Q10 trademark 원문 한글 구절 교체 (grep 0건 규칙 준수)
- [x] Q7 을 = yiyulgok 확정 (trademark 3중: 이기지묘·이통기국·이기불상리)
- [x] Q7 갑 = 사상가 보류 (창작 금지 규칙 준수)
- [x] coverage/2025-B.md 요약 테이블·ES dump·블로커 인덱스·최종 판정 갱신
- [x] blocker-log.md BLK-175E-2025B-006 재정의
- [x] coder-report-TASK-175E-2025-B.md 1·2·4 섹션 갱신
- [x] src·tests 디렉토리 미수정 (Coder 규칙 L90·L91 준수)
- [x] 본 FIX report frontmatter schema.md 준수
