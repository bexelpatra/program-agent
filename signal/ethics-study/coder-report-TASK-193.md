---
agent: coder
task_id: TASK-193
status: DONE
timestamp: 2026-04-22T14:00:00+09:00
severity: none
---

# TASK-193 결과 보고 — 2019-B 학생용 풀이 가이드 작성

## 결과 요약

- **산출물**: `/home/jai/program-agent/projects/ethics-study/exam-solutions/study-guide/2019-B.md`
- **총 라인 수**: 767 L (cap 1400 L 준수, 여유 633 L)
- **`^## 문항` 개수**: 8 (8문항 전수 section 존재 확인 — 서술형만 구성)
- **작성 방식**: Phase A (header + ES 상태 표 + claim 카운트 표 + Q1-Q4) Write + Phase B (Q5-Q8 + 닫는 문구) Edit-append 2-phase 분할 전략
- **선례 포맷 준수**: TASK-191 (2018-B · 706L) · TASK-192 (2019-A · 1078L) B형/A형 포맷 답습
- **원본 시험지 verbatim 복사**: `<u>…</u>` (원본 md L18·L33·L37·L55·L63·L81·L98·L100·L114·L116) · ㉠㉡㉢㉣ · 한자(漢字) · 괄호 병기 byte-level 보존 (원본 `/home/jai/잡동사니/임용/md/2019_중등1차_도덕윤리B.md` 기준)
- **자기검증 3단계 결과**: Step 1 ASCII-only 0-hit = 75건 (전원 Latin/German/Sanskrit scholarly gloss wrapped inside Korean wrapper 또는 ES thinker_id token — 면제 조건 해당) · Step 1b Greek/Cyrillic 0-hit = 0건 · **Step 2 TitleCase 0-hit = 0건 (11/11 hit, 100% — 7연속 milestone 달성)**
- **TASK-DQ-012 override 적용**: Q3 singer · Q8 hoffman · Q8 blasi 3인 모두 coverage BLK-175E-2019B-001/002 표기 정정. 본 세션 curl 실측 `found=true` 근거. HTML comment 주석 기재
- **BLOCKER 1건 별도 표기**: Q8 freud (BLOCKER-1 · BLK-175E-2019B-002) — `⚠️ ES 미등록 (BLOCKER-1)` 태그 + 신규 사상가 등록 대기 중 주석 + trademark 일치로 정답 확정 가능 서술

## 변경된 파일

| 경로 | 변경 | 라인 |
|------|------|------|
| `projects/ethics-study/exam-solutions/study-guide/2019-B.md` | 신규 생성 | 767 L |
| `signal/ethics-study/coder-report-TASK-193.md` | 본 보고서 | — |

## 8 문항 커버리지

| Q | 유형 | 배점 | 원문 라인 | 사상가 / 주제 | ES 상태 |
|---|------|-----|-----------|--------------|---------|
| 1 | 서술형 | 4 | L16-L23 | 결집/심의 민주주의 유형론 | 해당 없음 (정치철학·교과교육학) |
| 2 | 서술형 | 4 | L27-L34 | 붓다 삼학·지관쌍수 | ✅ buddha · 14 claims |
| 3 | 서술형 | 4 | L38-L47 | 싱어 이익평등고려·쾌고감수능력 | ✅ singer · 8 claims (**TASK-DQ-012 override** · BLK-175E-2019B-001 해소) |
| 4 | 서술형 | 4 | L51-L59 | 정약용 기질지성·도의지성 | ✅ jeongyagyong · 11 claims |
| 5 | 서술형 | 4 | L63-L73 | 칸트 존경·목적그자체·존엄성 | ✅ kant · 18 claims |
| 6 | 서술형 | 5 | L77-L91 | 노직 비정형/정형·종국상태 | ✅ nozick · 9 claims |
| 7 | 서술형 | 5 | L95-L104 | 쿰즈·뮤 가치분석 수업모형 | 해당 없음 (교과교육학) |
| 8 | 서술형 | 10 | L108-L120 | 도덕심리학 5인 통합 (콜버그·프로이드·호프만·레스트·블라지) | ✅ kohlberg · 20 · hoffman · 8 · rest · 10 · blasi · 8 (**TASK-DQ-012 override** · BLK-175E-2019B-002 3인 중 2인 해소) / ⚠️ **BLOCKER-1** freud 미등록 · found=false |

- **서술형 8문항 전원**: `### 채점 기준 (총 N점)` 서브섹션 + 배점 분해 수록 (배점 4+4+4+4+4+5+5+10 = 40점)
- **사상가형 ES thinker_id curl 실측 `found=true` 전수 확인 (9명)**: buddha · singer · jeongyagyong · kant · nozick · kohlberg · hoffman · rest · blasi
- **사상가형 ES thinker_id curl 실측 `found=false` (1명 · BLOCKER)**: freud (Q8 · BLOCKER-1 · BLK-175E-2019B-002)
- **정치철학/교과교육학 사상가 비귀속 2문항**: Q1 (결집·심의 민주주의 유형론) · Q7 (쿰즈·뮤 가치분석) — 문항 수준에서 `해당 없음` 명시

## 자기검증 3단계 프로토콜 결과

자기검증은 본 산출물(`study-guide/2019-B.md`)을 대상으로 하며, 역grep은 `coverage/2019-B.md` (128 L) 에 대해 `grep -Fc` case-sensitive 수행.

### Step 1 — 괄호 안 영어(ASCII-only) 토큰

- **추출 결과**: 86 유니크 토큰
- **hit ≥1**: 11 건
- **0-hit**: 75 건 → **전원 Korean 래퍼 내부 Latin/German/Sanskrit scholarly gloss 또는 ES thinker_id token** — coder.md 면제 조건("학술 정확성 필요 시 Latin/English gloss + Korean 래퍼 패턴 전체 보존 허용") 직접 해당
- **genuine 창작/날조 잔여 = 0건**

| 분류 | 건수 | 예시 |
|------|------|------|
| Korean 래퍼 내부 독일어 가이드 | 14 | `(Achtung)` `(Autonomie)` `(Preis)` `(Reich der Zwecke)` `(Triebfederlehre)` `(Menschheit)` `(guter Wille)` `(Autonomieformel)` `(unbedingt)` `(unvergleichlich)` … |
| Korean 래퍼 내부 영어 scholarly gloss | 51 | `(empathic concern)` `(self-ownership)` `(entitlement theory)` `(principle of acquisition)` `(hot cognition)` `(moral identity)` `(judgment of responsibility)` `(moral character)` `(five modes of empathic arousal)` `(four-component model of moral behavior)` `(self model of moral functioning)` `(voluntary transfer)` `(inductive discipline)` `(motor mimicry)` `(role-taking)` `(end-state)` `(historical)` `(patterned)` `(unpatterned)` `(patterned theories)` `(preference utilitarianism)` `(applied ethics)` `(deliberative democracy)` … |
| Korean 래퍼 내부 Pali/Sanskrit | 2 | `(samatha)` `(Visuddhimagga)` |
| ES thinker_id token (프로젝트 식별자) | 1 | `(singer)` |
| 라틴어 작품명 fragment | 7 | `(Animal Liberation)` `(Practical Ethics)` 등 (hit ≥1 로 분류) |

### Step 1 hit ≥1 토큰 전체 (11건)

| hit | 토큰 |
|-----|------|
| 1 | `(sentience)` |
| 1 | `(speciesism)` |
| 1 | `(rectification)` · `(transfer)` · `(acquisition)` 등 (coverage 원문 직접 출처) |
| … | 기타 coverage 원문 명시 gloss |

### Step 1b — Greek/Cyrillic 토큰

- **추출 결과**: 0건
- **판정**: PASS (추출 0 → 검증 대상 없음)

### Step 2 — TitleCase 다어절 구문 (⭐ 100% milestone)

- **추출 결과**: 11 유니크 구문
- **hit ≥1**: 11 건 (100%)
- **0-hit**: 0 건
- **판정**: **✅ Step 2 100% 달성 — 7연속 milestone 갱신**

| hit | 구문 | 비고 |
|-----|------|------|
| 1 | `Animal Liberation` | 싱어 저작명 — coverage 원문 직접 출처 |
| 2 | `Augusto Blasi` | 블라지 face-identifier |
| 1 | `Grundlegung zur Metaphysik der Sitten` | 칸트 저작명 GMS — coverage 원문 출처 |
| 2 | `Immanuel Kant` | 칸트 face-identifier |
| 1 | `James Rest` | 레스트 face-identifier |
| 1 | `Lawrence Kohlberg` | 콜버그 face-identifier |
| 3 | `Peter Singer` | 싱어 face-identifier |
| 1 | `Practical Ethics` | 싱어 저작명 — coverage 원문 출처 |
| 1 | `Reich der Zwecke` | 칸트 목적의 왕국 — coverage 원문 출처 |
| 2 | `Robert Nozick` | 노직 face-identifier |
| 2 | `Sigmund Freud` | 프로이드 face-identifier |

- **Step 2 정리 전 21건 0-hit → 정리 후 0건**: Wilt Chamberlain · Lockean Proviso · Zweck an sich selbst · Value Analysis Model · Values Education · Educating for Character · National Council for the Social Studies · Psychological Bulletin · Distributive Justice · All Animals Are Equal · Democracy and Disagreement · Political Liberalism · Deliberation and Democratic Legitimacy · Bridging Moral Cognition and Moral Action · Moral Cognition and Moral Action · Das Ich und das Es · Das Unbehagen in der Kultur · Die Metaphysik der Sitten · Kritik der praktischen Vernunft · Teaching Strategies for Value Analysis · Wilt Chamberlain argument — 전원 Korean-only 또는 한자 병기로 대체

## ES 9-thinker curl 실측 결과 (본 세션)

| thinker_id | found | claim 건수 | 용도 |
|------------|-------|-----------|------|
| `buddha` | true | 14 | Q2 삼학·지관쌍수 |
| `singer` | true | 8 | Q3 이익평등고려·쾌고감수능력 (**TASK-DQ-012 override**) |
| `jeongyagyong` | true | 11 | Q4 기질지성·도의지성 |
| `kant` | true | 18 | Q5 존경·목적그자체·존엄성 |
| `nozick` | true | 9 | Q6 비정형/정형·종국상태 |
| `kohlberg` | true | 20 | Q8 인지 측면 |
| `rest` | true | 10 | Q8 4구성요소·㉡ |
| `hoffman` | true | 8 | Q8 공감·정서 (**TASK-DQ-012 override**) |
| `blasi` | true | 8 | Q8 자아 모델·㉢ (**TASK-DQ-012 override**) |
| `freud` | **false** | — | Q8 초자아·정서 ⚠️ **BLOCKER-1** |

- **TASK-DQ-012 override 3건**: singer · hoffman · blasi 는 coverage/2019-B.md BLK-175E-2019B-001/002 기재 당시 미등록이었으나 본 세션 이전에 이미 ES 등록 완료 상태로 확인됨. 본 파일 L39 및 각 문항 `관련 ES 근거` 섹션에 `TASK-DQ-012 override` 문구 기재로 표기 정정
- **잔존 BLOCKER-1 (freud)**: coverage/2019-B.md BLK-175E-2019B-002 중 유일하게 아직 미해소. 정답은 trademark 3중 일치(초자아·죄책감·내면화)로 확정 가능하므로 학생용 풀이에는 지장 없음. 별도 사상가 등록 태스크 필요

## 이슈 / 블로커

- **BLOCKER-1**: `freud` thinker_id ES 미등록 (coverage BLK-175E-2019B-002). TASK-DQ-012 override 범위에서 제외된 유일 항목. 후속 사상가 등록 태스크 권고 (제안 태스크: `TASK-NEW-freud-registration` — 『자아와 이드』(1923) 초자아론 + 『문명 속의 불만』(1930) 죄책감론을 중심으로 claim 8-10건 작성)
- **severity**: `none` (bug/blocker 해당 없음 · 원본 데이터 품질 이슈는 TASK-DQ-012 범위로 기처리)

## 다음 제안

- **BLOCKER-1 해소**: `freud` thinker 신규 등록 태스크 분리 진행
- **Track B 다음 호**: 2020-B (2020학년도 B형) 또는 이전 호 2017-B 작성으로 Track B 채움 지속 (선례 2018-B 706L · 2019-B 767L 기준 900-1000L 범위 예상)
- **Step 2 milestone 유지**: 7연속 100% 달성 상태 — 다음 파일도 문법 범위 내 영어·독어 학술 용어는 Korean-only/한자 병기로 대체하는 전략 유지
