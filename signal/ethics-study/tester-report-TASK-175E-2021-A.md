---
agent: tester
task_id: TASK-175E-2021-A-T
status: DONE
severity: bug
timestamp: 2026-04-21
---

# Tester Report — TASK-175E-2021-A-T (2021 전공 A coverage 검증)

## 검증 대상 / 절차
- **대상 산출물**: `projects/ethics-study/exam-solutions/coverage/2021-A.md` (106 lines)
- **원문**: `/home/jai/잡동사니/임용/md/2021_중등1차_도덕윤리_전공A.md` (206 lines)
- **선행 Coder report**: `signal/ethics-study/coder-report-TASK-175E-2021-A.md`
- **검증 규칙**: Phase 6 Tester 4규칙 — row 독립 풀이 + 3중 일치 / 원문 인용 verbatim / 한자 병기 점검 / blocker-log 누적 기록
- **검증 절차**:
  1. 원문 206라인 전수 Read — Q1~Q12 발문·제시문·빈칸·밑줄 구조 직독
  2. 12문항 각각에 대해 Tester의 독립 풀이(trademark·thinker_id·정답) 도출
  3. Coder row와 발문·trademark·thinker_id·정답 3중 대조
  4. ES `curl` 재조회로 등록/미등록 상태 검증 (kant/spinoza/kohlberg/wangyangming/zhuxi/buddha/rawls/taylor/mill_js/bentham FOUND, moore/blasi/paul_taylor/hoffman/freud/singer/mill NOT FOUND)
  5. 동명이인 `taylor` 조회 → Charles Taylor(공동체주의, `political_philosophy`, 1931-) 확정
  6. Naming convention 선례 grep — `architecture.md:491`, `coder-report-TASK-174.md:74`

## 테스트 결과 (12/12)

| 문항 | 발문 일치 | Trademark 3중 일치 | thinker_id 일치 | 정답 일치 | 결과 |
|------|-----------|---------------------|------------------|-----------|------|
| Q1 | ✓ | ✓ (2015 개정 도덕과 교육과정 문서·영역 4 `자연·초월과의 관계`) | 교과교육학 비귀속 ✓ | ㉠=성찰 / ㉡=반성 ✓ | PASS |
| Q2 | ✓ | ✓ (3확정조항·특별한 연맹) | `kant` FOUND ✓ | ㉠=공화정 / ㉡=평화 연맹 ✓ | PASS |
| Q3 | ✓ | ✓ (비자연주의·열린 질문 논증) | `moore` NOT FOUND → blocker ✓ | ㉠=메타윤리학 / ㉡=자연적 ✓ | PASS (blocker 부착) |
| Q4 | ✓ | ✓ (conatus·신즉자연·자기원인) | `spinoza` FOUND ✓ | ㉠=자유 / ㉡=필연 ✓ | PASS |
| Q5 | ✓ | ✓ (샤프텔 8단계 도표) | 교과교육학 비귀속 ✓ | ㉠=해결(책)/㉢=재연/㉡ 2가지 서술 타당 ✓ | PASS |
| Q6 | ✓ | ✓ (도덕적 자아 구성·의무/책임 판단) | 갑 `blasi` NOT FOUND → blocker, 을 `kohlberg` FOUND ✓ | ㉡=도덕적 정체성 / ㉢=책임 판단 / 공통점·차이점 서술 타당 ✓ | PASS (blocker 부착) |
| Q7 | ✓ | ✓ (심즉리·치양지 / 심통성정·격물궁리) | `wangyangming` + `zhuxi` 모두 FOUND ✓ | ㉠=심(心) / ㉡=치지(致知) 최종 확정 ✓ | PASS (아래 observation 1건) |
| Q8 | ✓ | ✓ (오온·무아상경 논증) | `buddha` FOUND ✓ | ㉠=무아 / ㉡=유아 ✓ | PASS |
| Q9 | ✓ | ✓ (목적론적 삶의 중심·생명중심적 전망) | `paul_taylor` NOT FOUND → blocker; **id naming 규약 위반 bug** | ㉠=목적론적 삶의 중심 / 근거 + 생태계 중심주의 비교 ✓ | PASS (정답), **bug** (id 명명) |
| Q10 | ✓ | ✓ (완전/불완전 의무·목적의 정식 / 밀 "바랄 만한 유일한 것은 행복") | `kant` FOUND + `mill_js` FOUND ✓ | ㉠=불완전 / ㉡=행복 증진 / 목적의 정식·㉣ 해명 타당 ✓ | PASS |
| Q11 | ✓ | ✓ (질서정연한 사회·시민 불복종 5표지·정당화 3조건) | `rawls` FOUND ✓ | ㉠ 2가지 의미 / ㉡ 나머지 2조건(최후수단·일반화가능성) 타당 ✓ | PASS |
| Q12 | ✓ | ✓ (6·15 남북공동선언 원문) | 교과교육학 통일교육 비귀속 ✓ | ㉠=자주 / ㉡=연합제 / ㉢ 이 방향 서술 타당 ✓ | PASS |

**요약**: 12/12 정답 및 trademark 판정 전원 PASS. 단, Q9에서 thinker_id 명명 규약 위반(bug) 1건, Q7에서 답안 확정 과정의 서술 혼선(observation) 1건 발견.

## 이슈/블로커

### severity: bug — Q9 Paul Taylor thinker_id 명명 규약 위반

**위치**: 
- `projects/ethics-study/exam-solutions/coverage/2021-A.md` Q9 row (`thinker_id` 컬럼, BLK 설명, 감사 섹션, 요약 섹션)
- `signal/ethics-study/blocker-log.md` L613-614 (BLK-175E-2021A-003)
- `signal/ethics-study/coder-report-TASK-175E-2021-A.md` L35, L83, L110, L143, L146

**사유**: Coder는 Paul W. Taylor의 신규 id로 **`paul_taylor`**를 단정적으로 제안했으나, 본 프로젝트의 아키텍처 결정은 **`taylor_p`**이다.
- `signal/ethics-study/architecture.md:491` — "동명이인 후보가 있으면 ES에서 사전 조회하여 suffix 필요 여부를 결정. 예: `taylor` (Charles Taylor, 공동체주의) vs **`taylor_p`** (Paul Taylor, 생명중심주의) — 별개 인물."
- `signal/ethics-study/coder-report-TASK-174.md:74` — "TASK-185/186/187 (폴 테일러): 생명중심주의, 자연에 대한 존중 — **thinker_id는 `taylor_p`**로 하여 기존 `taylor_c`(찰스 테일러)와 구분"
- 선행 프로젝트 내 선례(`mill_js`): **lastname_suffix** 패턴을 채택. `taylor_p`는 이와 일관. `paul_taylor`는 firstname_lastname으로 본 프로젝트 명명 관례와 어긋남.
- 단, Coder도 coverage L63·blocker-log L614·coder-report L113 곳에서 "`paul_taylor` 또는 `taylor_p`"로 대안 병기는 해두었으나, **1순위 후보 및 row 내 thinker_id 컬럼**에는 `paul_taylor`만 명시하여 TASK-176의 id 선택을 혼란시킬 여지가 있음.

**영향 범위**: 정답(㉠=목적론적 삶의 중심, ㉡ 근거, 생태계 중심주의 비교)의 판정에는 영향 없음(trademark 3중 일치로 확정). 다만 TASK-185/186/187(Paul Taylor 등록 태스크)의 후속 id 선택이 기존 아키텍처 결정과 분기할 위험. 프로젝트 명명 일관성 훼손.

**권고 조치**:
1. `projects/ethics-study/exam-solutions/coverage/2021-A.md` Q9 row의 `thinker_id` 컬럼, BLK 주석, 블로커 요약 표, ES 사상가 커버리지 요약의 "`paul_taylor`" 표기를 모두 **`taylor_p`**로 교체(또는 최소한 "`taylor_p` (primary) / `paul_taylor` (alias)"로 1순위 명시).
2. `signal/ethics-study/blocker-log.md` BLK-175E-2021A-003의 "후보 id: `paul_taylor`"를 "**정식 id: `taylor_p`** (architecture.md L491 준수)"로 수정.
3. `signal/ethics-study/coder-report-TASK-175E-2021-A.md` 동 범위 수정.
4. TASK-176/후속 등록 태스크에서 `taylor_p` id로 ES document 생성하도록 Manager 지시.

### severity: observation — Q7 ㉡ 답안 확정 과정의 서술 혼선

**위치**: `projects/ethics-study/exam-solutions/coverage/2021-A.md` Q7 row 사상가/개념 컬럼 (▶ 답 섹션).

**사유**: Q7 ㉡의 최종 답 "㉡ = 치지(致知)"를 확정하기 전에, row 본문 중간에서 "갑의 ㉡ = 치지(致知) / 을의 ㉡ = 궁리(窮理)"로 한 차례 단정한 뒤, 곧바로 "교과서 표준 해석은 ㉡ = 치지로 공통 지정"이라며 **수정 답**으로 덮어쓰는 흔적이 남아 있음. 원문 L115·L117을 직독하면 갑·을이 동일 빈칸 기호 ㉠·㉡를 공유하며 각자의 학설로 해석하는 구조가 명확하므로(갑의 치지=치양지 맥락 / 을의 치지=격물로서의 치지), 최초부터 **㉡=치지** 공통 답으로 확정하는 것이 간명.

**영향 범위**: 최종 답은 정확하므로 정답성 문제는 없음. 단, 독자 가독성·미래 Coder 세션의 오독 가능성 때문에 관찰 권고.

**권고 조치**: 후속 정리 태스크 발생 시 Q7 row ▶ 답 섹션을 "㉠ = 심(心, 마음) / ㉡ = 치지(致知, 앎을 극진히 함 — 갑은 치양지致良知의 맥락, 을은 격물窮理로서의 치지)"로 1문장 확정형으로 축약.

### 참고(severity 외 관찰)

- **블로커 분류 정당성**: Q3 moore / Q6 blasi / Q9 paul_taylor 3건 blocker 지정은 Phase 6 ES-gap 정책(제시문 중심 사상가 미등록 → blocker) 및 2018-A~2020-B 선례(regan, turiel, bandura/pettit/skinner, singer/freud/hoffman/blasi, jinul/bandura/pettit/skinner, berlin/gidaeseung, heidegger/protagoras/fazang)와 일관. **적절**.
- **observation 분류 정당성**: Q1(2015 개정 교육과정) / Q5(샤프텔 역할놀이) / Q12(6·15 남북공동선언) 3건을 "교과교육학·문서형 비귀속"으로 observation 처리. 선례 BLK-175E-2017A-005(쿰즈·뮤 가치분석), BLK-175E-2020A-004(헌법·통일교육지원법)와 일관. **적절**.
- **blocker-log.md 누적 기록**: BLK-175E-2021A-001/002/003 3건이 L591-L616에 정상 append. HTML 주석(`<!-- BLOCKER(TASK-175E-2021-A): BLK-175E-2021A-00X -->`)이 coverage/2021-A.md Q3·Q6·Q9 row에 각각 삽입됨 — 확인 완료.
- **원문 인용 verbatim 점검**: 각 row "제시문 핵심(원문 복사)" 컬럼의 인용구절을 원문 L14-L202 해당 범위와 대조 — 재서술·의역·창작 0건. `( ㉠ )`, `( ㉡ )`, `( ㉢ )`, 밑줄 `㉡`, 저서명·한자 표기 등 부호 보존. **규칙 2 준수**.
- **한자 병기 점검**: row당 17~20건, 합계 ~210건의 `한자(한글 — 의미)` 병기. 한자 단독 노출 0건(원문 인용 내부 한자 표기는 원문 보존). **규칙 3 준수**.
- **배점 합계 점검**: 2×4 + 4×8 = 40점, 원문 L7 "12문항 40점" 일치. **합격**.
- **문항 라인 매핑 점검**: task 지시(L14/L41/L55/L64/L74/L95/L111/L125/L138/L152/L174/L186)와 coverage 라인 범위(Q1 L14-L37 / Q2 L41-L51 / Q3 L55-L60 / Q4 L64-L70 / Q5 L74-L92 / Q6 L95-L107 / Q7 L111-L121 / Q8 L125-L134 / Q9 L138-L148 / Q10 L152-L170 / Q11 L174-L182 / Q12 L186-L202) 완전 일치.

## 결론
- **통과/실패**: **12/12 통과** (정답·trademark·thinker_id 3중 일치 모두 확정).
- **최종 severity**: **bug** — Q9 thinker_id 명명 규약(`paul_taylor` → `taylor_p`) 불일치. 정답 자체는 확정이나 후속 TASK-185/186/187의 id 정합성을 위해 수정 필요.
- **후속 조치 요청**: Manager는 이 bug에 대한 수정 태스크(`paul_taylor` → `taylor_p` 1차 표기 일괄 치환)를 task-board에 등록해 Coder에게 할당할 것. Q7 ㉡ 서술 혼선은 observation으로 retrospective 이월 또는 후속 정리 태스크에서 처리 권장.
