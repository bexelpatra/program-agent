---
task_id: TASK-198-T
agent: tester
model: opus-4.7
status: DONE
severity: bug
timestamp: 2026-04-23T06:30:00+09:00
target_file: projects/ethics-study/exam-solutions/study-guide/2022-A.md
coder_report: signal/ethics-study/coder-report-TASK-198.md
source_md: ~/잡동사니/임용/md/2022_중등1차_도덕윤리_전공A.md
---

## 결과 요약

2022-A 학생용 풀이 가이드 (1027L · 12문항 · 40점) 에 대해 10항 체크리스트를 전수 재실행했다.

**최종 판정: NEEDS_REVISION (severity=bug · 구조·verbatim·ES·산술은 무결하나 문서 내부 3건 치명 모순)**

- 10항 중 **7항 PASS · 3항 bug (문서 내부 모순)** — 가이드 파일의 구조·제시문 verbatim·ES curl·BLOCKER 4건·채점 기준·한자·em-dash·산술 자기검증 3분류 (16+59+18=93) 모두 Coder 주장 정확 일치.
- **치명 산술 fudge 없음**: coder-report-TASK-198.md 내 `≈ / 수렴 / 중복 보정 / 대략` 실제 fudge 사용 0건 (L84 "0건 사용" 선언부의 메타 인용 1건만 존재, 선례 TASK-197-T L49 동일 패턴). **제5차 재발 블로커 승격 회피 확증.**
- 그러나 **학생 풀이 가이드 본문 자체에 3건의 치명적 factual contradiction** 발견 — Q8 turiel·L1000 wonhyo·L1001-L1002 DQ-016 override 부정 모순. Tester 본문 어투가 "관찰/참고용"이라도 사양(체크리스트 항목 6 "DQ-016 override 3명은 BLOCKER 표기 없음 확증")과 정면 충돌하므로 **severity=bug** 부여.

## 변경된 파일

없음 (검증만 수행).

## 10항 체크 결과 표

| # | 항목 | 체크리스트 요구 | 실측 | 판정 |
|---|------|-----------------|------|------|
| (1) | 12문항 전수 커버 | `^## 문항` == 12 | **12** (L47·122·186·243·309·398·490·558·638·715·800·874) | PASS |
| (2) | 헤더 metadata 실재 | 12건 `원문 line L{m}-L{n}` | 12/12 실재. 체크리스트 예시 수치(L76-L87·L89-L103·L105-L119·L121-L141·L143-L157·L159-L204)는 일부 Coder가 원본 실제 범위(L76-L86·L89-L101·L105-L117·L121-L140·L143-L156·L159-L202)로 micro-adjust 했고 원본 md(206L)와 일치. 체크리스트 주석 "Coder가 일부 라인 범위를 미세 조정했을 수 있음 — 실제 파일 내용 기준 검증" 조항 발동 | PASS |
| (3) | 제시문 verbatim byte-level | `<u>` · 괄호 영문 · 한자 · em-dash `e2 80 94` · ㉠㉡㉢㉣ 보존 | `<u>` 원본 11쌍·가이드 11쌍 (본문) + 1회 description(L1017 backtick) · `</u>` 원본·가이드 11회 정확 일치 · em-dash `e2 80 94` hexdump 3샘플 PASS · ㉠ 139회·㉡ 135회·㉢ 58회·㉣ 24회·㉤ 8회 전수 보존 | PASS |
| (4) | ES 등록 11 unique thinker 재조회 | 정상 8 + DQ-016 override 3 전원 HTTP 200·found=true | **11/11 HTTP=200 · found=true**. lickona·jeongyagyong·nozick·plato·kohlberg·kant·huineng·gilligan (8명) + jinul·pettit·turiel (DQ-016 3명). curl `http://localhost:9200/ethics-thinkers/_doc/{id}` 실측 | PASS |
| (5) | 대표 claim_id 전수 found=true (≥10건) | 12건 claim_id 실측 | 12/12 `found=true` 확증: lickona-claim-001·005 · jinul-claim-004 · jeongyagyong-claim-001 · nozick-claim-007 · pettit-claim-001 · plato-claim-006 · kohlberg-claim-012 · kant-claim-003·017 · huineng-claim-001 · gilligan-claim-009 | PASS |
| (6) | BLOCKER 4건 표기 · DQ-016 override 3명 BLOCKER 표기 없음 | `green_th·shenxiu·zhiyi·beccaria` ⚠️BLOCKER (BLK-175E-2022A-003·005·006·007) + jinul·pettit·turiel BLOCKER 표기 0 | green_th ⚠️BLOCKER (L422·L453) · shenxiu ⚠️BLOCKER (L741·L771·L787) · zhiyi ⚠️BLOCKER (L752·L772·L788) · beccaria ⚠️BLOCKER (L825·L845·L861) 전수 실재. 그러나 **turiel 에 ⚠️ BLOCKER 표기 실재 (L583·L588·L607)** — DQ-016 override 에 위배 · L19/L41 요약과 모순 → **bug-1** | **BUG** |
| (7) | Q3 교과교육학 분류 사유 명시 | `해당 없음 (교과교육학 …)` 실재 | L21 "해당 없음 (교과교육학·일반 정치학) \| Q3 … 교과교육학 범주 문항" · L227 "해당 없음 (교과교육학 분류)" 실재 | PASS |
| (8) | 서술형 Q5~Q12 채점 기준 8건 + 대조/통합 매핑 | `^### 채점 기준` == 8 · Q6 pettit+green_th · Q8 kohlberg+turiel · Q10 shenxiu+huineng+zhiyi · Q11 kant vs beccaria | **8건 실재** (L374·465·528·609·685·774·847·948). Q6 pettit(L421)+green_th(L422) · Q8 kohlberg(L578)+turiel(L583) · Q10 shenxiu(L741)+huineng(L747)+zhiyi(L752) 3인 · Q11 kant(L820)+beccaria(L825) 전수 확증 | PASS |
| (9) | 한자 래퍼 em-dash `e2 80 94` 3+ 샘플 hexdump | 3개 샘플 최소 | sample 1 "정치학(미국 공화주의 제도론 — 삼권 분립·탄핵)" offset 0x20 `e2 80 94` · sample 2 "인격(修行的 人格 — performance character …)" offset 0x18 `e2 80 94` · sample 3 "윤리(德 倫理 — virtue ethics)" offset 0x17 `e2 80 94` — 전수 U+2014 정확 확증 | PASS |
| (10) | 자기검증 3단계 재실행 + 산술 정확 일치 + fudge 0건 | Step1=16 · Step1b=59 · Step2=18 · 총 93 unique · fudge 문구 0건 | **Step1=16** 정확 ✅ (Coder regex 재실행 `beccaria·gilligan·green_th·huineng·jeongyagyong·jinul·kant·kohlberg·lickona·nozick·pettit·plato·shenxiu·turiel·wonhyo·zhiyi`) · **Step1b=59** 정확 ✅ · **Step2=18** 정확 ✅ · 총합 93 일치 ✅ · fudge grep = 1건 (L84 "`≈`·`수렴`·`중복 보정`·`대략` 문구 0건 사용" 선언부의 메타 인용 — 실질 사용 아님 · 선례 TASK-197-T 동일 패턴으로 PASS 처리) · **제4차 → 제5차 재발 없음 확증** | PASS |

## 자기검증 3단계 실측 수치 표 (Coder report L26-L84 대조)

| Step | Coder 주장 | Tester 실측 (Coder regex 직접 재실행) | 일치 |
|------|-----------|----------------------------------------|------|
| Step 1 bare-id lowercase thinker_id | 16 (`\b(plato\|kant\|nozick\|pettit\|green_th\|kohlberg\|turiel\|shenxiu\|huineng\|zhiyi\|beccaria\|gilligan\|wonhyo\|jinul\|jeongyagyong\|jeong_yakyong\|green\|lickona)\b` sort -u wc -l) | **16** (beccaria·gilligan·green_th·huineng·jeongyagyong·jinul·kant·kohlberg·lickona·nozick·pettit·plato·shenxiu·turiel·wonhyo·zhiyi) | ✅ 정확 일치 |
| Step 1b claim-id suffix `-claim-NNN` | 59 (`\b[a-z_]+-claim-[0-9]+\b` sort -u wc -l) | **59** | ✅ 정확 일치 |
| Step 2 TitleCase English | 18 (`\b(Plato\|Kant\|Nozick\|Pettit\|Green\|Kohlberg\|Turiel\|Shenxiu\|Huineng\|Zhiyi\|Beccaria\|Gilligan\|Wonhyo\|Jinul\|Jeong\|Lickona\|Immanuel\|Carol\|Lawrence\|Elliot\|Cesare\|Thomas\|Philip\|Robert)\b` sort -u wc -l) | **18** (Beccaria·Carol·Cesare·Elliot·Gilligan·Green·Immanuel·Kant·Kohlberg·Lawrence·Lickona·Nozick·Pettit·Philip·Plato·Robert·Thomas·Turiel) | ✅ 정확 일치 |
| 3분류 disjoint 합계 | 93 (16+59+18) | **93** | ✅ 정확 일치 |
| fudge 문구 (≈·수렴·중복 보정·대략) 실사용 | 0건 선언 | **0건 실사용** (L84 "0건 사용" 선언부 메타 인용 1건만 존재) | ✅ 제5차 재발 회피 |

**제4차 재발(TASK-196-T) / 제5차 재발 위협 완전 회피 확증**: Coder는 TASK-197과 동일한 패턴으로 3분류 disjoint 정의 후 Python-style bare regex 재현으로 수치를 정확히 도출했다. "≈"·"수렴"·"중복 보정"·"대략" 어떤 형태의 fudge 산술 분해도 사용하지 않았고, Tester 독립 재현치와 정확 일치한다.

## 이슈/블로커

### bug-1: Q8 turiel 을 BLOCKER 표기 — DQ-016 override 위배 (CRITICAL)

**위치**:
- L583: `- **을 identification**: **튜리엘(Elliot Turiel)** (⚠️ BLOCKER BLK-175E-2022A-004 / DQ-016 override 미적용 — 원본 ethics-thinkers ES 미등록)`
- L588: `- **DQ-016 해설**: TASK-196 세션 3차 재발 시정 대상. 현재 ES ethics-thinkers 인덱스에 turiel 미등록 → 본 study-guide는 **BLOCKER 상태 명시적 기재**. 교과서(리코나·튜리엘 영역이론 표준 설명)에 의거해 답안 개념 정리만 제공하며, "ES claim 근거"로는 인용 불가.`
- L607: `- **⚠️ turiel**: ES 미등록(BLK-175E-2022A-004) — 본 답안은 교과서 표준 해설(튜리엘 영역이론)에 근거. ES claim_id 인용 불가.`

**모순**:
- L19 (요약표): `✅ DQ-016 override 등록 (3명) | jinul (Q2) · pettit (Q6 가) · turiel (Q8 을) | … 본 세션 curl 실측 \`found=true\` 로 해소`
- L23 (HTML 주석): `DQ-016 override: … 3건(jinul/pettit/turiel)은 TASK-176 계열 후속 등록으로 이미 해소. 정상 ES 근거 사용`
- L41: `DQ-016 override ✅ 3명 = 총 11명 unique ES 근거 사용. 잔존 BLOCKER는 4건(green_th·shenxiu·zhiyi·beccaria)`
- 헤더 L558: `## 문항 8 · 서술형 · 4점 · 원문 line L89-L101 · 콜버그 + 튜리엘(DQ-016 override)`
- Tester curl `http://localhost:9200/ethics-thinkers/_doc/turiel` → HTTP 200 · `"found":true` · claim_count=8
- Coder report L152: `DQ-016 override 대상 3명(jinul · pettit · turiel)은 ES curl 실측 found=true로 해소 확인되어 BLOCKER 표기 없이 정상 claim 근거 사용`

**체크리스트 항목 6 요구사항과 직접 충돌**: "DQ-016 override 3명은 BLOCKER 표기 없음 확증 의무".

**영향**: 학생이 Q8 을 구역을 읽으면 "튜리엘은 ES 미등록 · claim_id 인용 불가" 로 오해하게 되어 실제 존재하는 turiel-claim-001~008 을 활용하지 못한다. 또한 동일 문서 내 L19/L41 과 Q8 본문이 상충하여 문서 신뢰도를 훼손한다.

### bug-2: L1000 "ES 등록 사상가 (11명)" 목록에 Q1 을 wonhyo 로 오기 (FACTUAL ERROR)

**위치**: L1000 `**ES 등록 사상가 (11명)**: wonhyo (Q1), jeongyagyong (Q4), nozick (Q5), plato (Q7), kohlberg (Q8갑), kant (Q9·Q11갑), huineng (Q10 을), gilligan (Q12)`

**모순**:
- Q1 발문/제시문/정답 전부 리코나(Lickona)를 다룸. L18 요약표: `lickona (Q1 … 덕 윤리 일반)`
- L64 Q1 정답 "(가) 토머스 리코나(Thomas Lickona, 1943~) — `lickona` ES 등록(claim 10건)"
- L96 Q1 ES 근거: `✅ ES 등록: thinker_id: lickona (토머스 리코나)`
- wonhyo는 2022-A 어디에도 출제 대상이 아님. wonhyo ES 등록은 `lickona` 16건 중 Step 1 bare-id 에 wonhyo 가 등장하는 이유가 L39 "wonhyo 는 Q1 대비 '원효의 일심 사상은 리코나의 인격 교육과 대비되지 않음'의 1회 언급(크로스리퍼런스 context)" 뿐임 (coder-report L39 실측 일치).
- 헤더 L47: `## 문항 1 · 기입형 · 2점 · 원문 line L14-L22` — 사상가 지정 없음 (Q1 은 리코나)

**영향**: L1000 의 ES 등록 11명 목록이 L18 (8명) + DQ-016 3명 합산과 일치하지 않는다. 학생이 최종 요약을 읽으면 wonhyo 가 Q1 출제자로 오인하게 된다. 실제로는 "lickona (Q1)" 이어야 한다.

또한 L1000 목록을 집계하면 lickona·pettit·jinul·turiel·beccaria 등 여러 Q 대응이 누락되어 "11명" 합계도 맞지 않는다 (실제 목록 열거는 wonhyo·jeongyagyong·nozick·plato·kohlberg·kant·huineng·gilligan = 8명 + Q9·Q11갑 kant 중복 · Q8갑 kohlberg 중복). 집계 자체가 깨져 있다.

### bug-3: L1001-L1002 최종 요약이 DQ-016 override 를 정면 부정

**위치**:
- L1001: `**DQ-016 override 후보 (3명)**: jinul (Q2), pettit (Q6가), turiel (Q8을) — coverage md에는 BLOCKER 표기였으나 ES 재확인 결과 **미등록(BLK 확정)**`
- L1002: `**⚠️ BLOCKER (7명)**: jinul (BLK-175E-2022A-001), pettit (BLK-175E-2022A-002), green_th (BLK-175E-2022A-003), turiel (BLK-175E-2022A-004), shenxiu (BLK-175E-2022A-005), zhiyi (BLK-175E-2022A-006), beccaria (BLK-175E-2022A-007)`

**모순**:
- L19 "DQ-016 override 등록 (3명) | jinul · pettit · turiel | … curl 실측 `found=true` 로 해소. coverage BLOCKER 표기 정정(DQ-016 override)"
- L41 "잔존 BLOCKER는 4건(green_th·shenxiu·zhiyi·beccaria)"
- L162 Q2 `✅ ES 등록 (DQ-016 override): thinker_id: jinul … found=true`
- L452 Q6 `✅ ES 등록 (DQ-016 override): thinker_id: pettit … found=true`
- Tester curl: jinul·pettit·turiel 모두 `found=true`
- Coder report L152 동일 주장

**영향**: 최종 요약 섹션이 문서 서두 요약과 Q별 본문의 DQ-016 override 기재를 완전히 부정한다. 학생 혼란을 유발하며, "잔존 BLOCKER 4건" (정확한 숫자) vs "BLOCKER 7건" (L1002, 잘못된 숫자) 이 한 문서에 공존한다. 체크리스트 항목 6 "DQ-016 override 3명은 BLOCKER 표기 없음 확증 의무" 에 정면 위배.

### severity 판정 근거

- tester.md L88 "bug : 사양에 어긋나거나 명백히 잘못된 동작. 수정 태스크가 반드시 필요하다."
- tester.md L91 "본문 어투를 '관찰/참고용'이라고 낮췄더라도, 실제로 사양에 어긋나는 결함이면 `bug` 를 부여해야 한다."
- 체크리스트 항목 6 은 DQ-016 override 3명의 BLOCKER 표기 부재를 **명시적으로 요구**하는 사양 조항 — bug-1 은 이를 직접 위반.
- bug-2·bug-3 은 문서 내부 factual contradiction 으로 사양 위반 + 신뢰성 훼손.
- 제5차 재발(fudge·산술 불일치)은 아니므로 blocker 승격은 불필요. severity=**bug** 가 적정.

## 테스트 결과

- 테스트 항목: 10개 (체크리스트)
- PASS: 7 ((1)·(2)·(3)·(4)·(5)·(7)·(8)·(9)·(10) 중 9개 PASS 실체상으로는 PASS 이나 (6) bug 로 분리해 7개로 표시함이 적정)
- 재분류: (1)·(2)·(3)·(4)·(5)·(7)·(8)·(9)·(10) = 9개 PASS, (6) = 1개 bug
- bug 세부: (6) 안에 3건의 문서 내부 모순 (bug-1 Q8 turiel · bug-2 L1000 wonhyo · bug-3 L1001-L1002 DQ-016 부정)

## 다음 제안

Manager 에게 Coder 수정 태스크 (예: TASK-199 또는 TASK-198-FIX) 등록 권고. 수정 범위 3곳:

1. **Q8 을 turiel 구역 (L583·L588·L607)**: `⚠️ BLOCKER BLK-175E-2022A-004 / DQ-016 override 미적용` → `✅ ES 등록 (DQ-016 override · claim 8건)` 로 정정. L588 "DQ-016 해설" 단락을 "TASK-176 계열 후속 등록으로 이미 해소. 정상 claim_id 인용 가능" 로 전면 재작성. L607 `⚠️ turiel: ES 미등록` 줄을 `✅ turiel: ES 등록 (DQ-016 override)` + 대표 claim_id 3~5건 인용으로 교체.

2. **L1000 ES 등록 11명 목록**: `wonhyo (Q1)` → `lickona (Q1)` 정정. 목록을 L19 요약표 (lickona·jeongyagyong·nozick·plato·kohlberg·kant·huineng·gilligan 8명 + jinul·pettit·turiel DQ-016 3명 = 11명) 와 정확히 일치시킴. Q 대응도 lickona=Q1·jinul=Q2·jeongyagyong=Q4·nozick=Q5·pettit=Q6가·plato=Q7·kohlberg=Q8갑·turiel=Q8을·kant=Q9·Q11갑·huineng=Q10을·gilligan=Q12 로 정합.

3. **L1001-L1002 최종 블록**: `DQ-016 override 후보 (3명) … 미등록(BLK 확정)` 줄 완전 삭제 또는 `DQ-016 override 적용 (3명): jinul·pettit·turiel — ES 재확인 결과 등록 확정 (found=true)` 로 정정. `⚠️ BLOCKER (7명)` → `⚠️ BLOCKER (4명): green_th · shenxiu · zhiyi · beccaria` 로 단축. 이어지는 L1005 "총 15명 중 ES 등록 8명 · 미등록 BLOCKER 7명" 도 "총 15명 중 ES 등록 11명 (정상 8 + DQ-016 3) · BLOCKER 4명" 로 재계산.

자기검증 3분류 (16+59+18=93) · 12문항 구조 · verbatim 보존 · em-dash hexdump 등 나머지 요소는 무결하므로 수정 필요 없음. 본 3곳 정정만으로 PASS 가능.

## 선례 연속성

- TASK-196-T: 제3차 재발 (fudge `≈`·`수렴` 대거 사용) 시정 요구
- TASK-197-T: 제4차 재발 시정 확증 PASS (observation · fudge 0건)
- TASK-198-T (본 보고서): 제5차 재발 위협 완전 회피 (fudge 0건 · 산술 정확 일치). **산술·verbatim 차원은 완벽**. 단 **문서 내부 factual consistency** 차원에서 3건 bug 발견 — 새로운 유형의 결함. blocker 승격은 아님 (산술 측 재발 없음).

---

**최종 판정: NEEDS_REVISION (severity=bug · 문서 내부 3건 factual contradiction — Q8 turiel BLOCKER 표기 · L1000 wonhyo 오기 · L1001-L1002 DQ-016 override 부정)**
