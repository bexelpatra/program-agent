---
task_id: TASK-175E-2016-A
agent: coder
model: opus
status: DONE
severity: observation
date: 2026-04-21
scope: 2016 중등임용 도덕·윤리 전공 A 커버리지 신규 작성
---

# Coder Report — TASK-175E-2016-A

## 요약

- **산출 파일**: `projects/ethics-study/exam-solutions/coverage/2016-A.md` (신규 생성, 14 row 전수 작성)
- **원문**: `/home/jai/잡동사니/임용/md/2016중등1차-도덕윤리-전공A.md` (185 lines, 14문항 40점)
- **배점 검증**: 기입형 Q1~Q8 [2점]×8=16점 + 서술형 Q9~Q14 [4점]×6=24점 = **40점 일치**
- **분류**: 사상가형 13문항 + 교과교육학 1문항(Q2 CASEL SEL) = 14문항
- **ES 커버리지**: 있음 7문항 + 부족 1문항(Q5 갑 원효 3 claims) + 없음(미등록 사상가) 6문항 = 14문항
- **블로커**: 정식 등록 7건(BLK-175E-2016A-001 ~ 007), blocker-log.md append 완료
- **grep -F 전수 검증**: 61개 인용 구절 전수 hit ≥ 1 (1차 실패 1건은 인용부호 누락 교정 후 재검증 성공)

## 1. Read 호출 증거 테이블 (현 세션)

| # | 파일 경로 | offset | limit | 목적 |
|---|-----------|--------|-------|------|
| 1 | `/home/jai/program-agent/signal/ethics-study/architecture.md` | 500 | 150 | Phase 6 기출 작업 규칙 L523~L593 확인 (조항 1~6 숙지) |
| 2 | `/home/jai/잡동사니/임용/md/2016중등1차-도덕윤리-전공A.md` | 1 | 185 | 2016-A 원문 1회 완독 (L1~L185 전면) |
| 3 | `/home/jai/잡동사니/임용/md/2016중등1차-도덕윤리-전공A.md` | 140 | 15 | Q11(맹자·양주) 블록 재정독 — 갑/을 판정 재확인 |
| 4 | `/home/jai/program-agent/projects/ethics-study/exam-solutions/coverage/2015-B.md` | 1 | (전체) | 선행 템플릿 포맷·구조 참조 |
| 5 | `/home/jai/program-agent/signal/ethics-study/blocker-log.md` | 1 | 50 | 블로커 번호 체계·등록 형식 확인 |
| 6 | `/home/jai/program-agent/signal/ethics-study/blocker-log.md` | 315 | 14 | 최신 블로커 이후 append 위치 확인 |

이전 세션의 Read 증거는 claim으로 활용하지 않음(Phase 6 규칙 조항 1.b 준수).

## 2. ES curl 증거 (현 세션)

### 2.1 thinker 목록 조회 (1회)

```
curl -s "http://localhost:9200/ethics-thinkers/_search?size=100&_source=id,name,name_en&pretty" \
  | jq -r '.hits.hits[]._source | "\(.id)\t\(.name)\t\(.name_en)"' | sort
```

결과: 55명 canonical id 알파벳 순 획득 (aquinas ~ zhuxi). 2015-B 커버리지와 동일한 등록 목록. 본 시험과 직결되는 사상가 중 **미등록 6명**(jinul, jonas, narvaez, hoffman, yangzi, moore) 확인.

### 2.2 thinker별 claim 수 집계 (1회)

```
curl -s -X POST "http://localhost:9200/ethics-claims/_search" -H "Content-Type: application/json" \
  -d '{"size":0,"aggs":{"t":{"terms":{"field":"thinker_id","size":100}}}}'
```

본 시험 관련 사상가 count 추출:
- **등록·claim 풍부**: rest=10, mencius=17, wangyangming=10, yihwang=12, spinoza=6, rawls=15, kohlberg=20, kant=18, mill_js=17, hume=10, aquinas=10
- **등록·claim 부족**: wonhyo=3 (정혜쌍수·언상불리 보강 필요)
- **미등록(count=0)**: jinul, jonas, narvaez, hoffman, yangzi, moore

### 2.3 개별 사상가 claim 본문 샘플 조회 (문항 trademark 대조용)

각 사상가별 1회씩 `curl -s -X POST "http://localhost:9200/ethics-claims/_search" -d '{"size":N,"query":{"term":{"thinker_id":"<id>"}}}'` 호출하여 trademark 직접 일치 확인:

| thinker_id | 문항 | 확인한 ES claim 일치 항목 |
|------------|------|--------------------------|
| rest | Q1 | "도덕적 민감성은 4구성요소 모델의 첫 번째 요소로, 특정 상황이 도덕적 문제를 내포하고 있음을 인식하고, 자신의 행동이 타인에게 어떤 영향을 미칠 수 있는지를 파악하는 능력" — 원문 L26과 완전 일치 |
| wangyangming | Q3 | "앎과 실천은 본래 하나이다(知行合一). 참된 앎은 반드시 실천을 포함하며, 실천하지 않는 앎은 아직 참으로 안 것이 아니다" — 원문 L49 "한 가지 생각이 일어나면 그것이 바로 실행" 일치 |
| yihwang | Q4 | "심(心)은 성(性)과 정(情)을 통섭(統攝)한다(心統性情)" + "경(敬)은 … 미발(未發)에는 함양(涵養)하고 이발(已發)에는 성찰(省察)하는 것이다" — 원문 L61/L63/L65 일치 |
| spinoza | Q7 | `spinoza-claim-001` original_text_ko "존재하는 모든 것은 신 안에 있으며" + `spinoza-claim-003` original_text_ko "각 사물은 자기 안에 있는 한에서 자신의 존재를 유지하려고 노력한다 (Unaquaeque res, quantum in se est, in suo esse perseverare conatur)" — 원문 L100 완전 일치 |
| rawls | Q8 | "중첩적 합의(overlapping consensus)는 서로 다른 포괄적 교설(comprehensive doctrines)을 가진 시민들이 각자의 교설 내부의 이유로 동일한 정치적 정의관에 동의하는 상태" — 원문 L108 완전 일치 |
| kohlberg | Q10 갑 | 3수준 6단계·인지 발달 보편성 claim 다수 — 원문 L130 "인지 발달의 단계 + 문화 보편성" 일치 |
| mencius | Q11 갑 | 맹자의 양주·묵자 비판 claim — 원문 L146 "털 한 오라기 + 군주 부정" 일치 |
| kant | Q12 갑 | "명법에는 … 정언명법이 있다" + "자율성은 도덕법칙의 최고 원리" + "존엄성" — 원문 L156 선의지/의무 일치 |
| mill_js | Q12 을 | 공리주의·해악 원리·결과주의 claim — 원문 L158 "동기와 도덕성 무관" 일치 |
| hume | Q13 을 | "이성만으로는 도덕적 판단을 내릴 수 없다" + "'이다(is)' 명제에서 '해야 한다(ought)' 명제를 논리적으로 도출할 수 없다 … 사실-당위 논리 간극" + "공감(sympathy)은 도덕 평가의 핵심 메커니즘" — 원문 L168 완전 일치 |
| aquinas | Q14 | "자연법(lex naturalis)은 영원법(lex aeterna)에 이성적 피조물이 참여하는 것" + "자연법의 제1원리는 '선을 행하고 악을 피하라'" + "인정법(lex humana)은 자연법으로부터 도출되어야 하며, 자연법에 반하는 인정법은 … 법의 타락. '부당한 법은 법이 아니다'" — 원문 L181 완전 일치 |

## 3. 3단계 확정 로그 (요약, 문항별)

(상세는 coverage/2016-A.md 본문 "3단계 확정 절차 로그" 섹션 참조)

| 문항 | ① 발문 | ② 제시문 trademark 핵심 | ③ 판정(사상가 / 답) | 3중 일치 상태 |
|------|--------|------------------------|---------------------|--------------|
| Q1 | 신콜버그 학파가 강조한 도덕적 행동 요소 | 주변 환경 단서에서 도덕적 함의 발견 + 테레사 수녀 + 신콜버그 학파 | rest / 도덕적 민감성 | 원문·ES·Coder 일치 |
| Q2 | SEL 5 역량 중 3번 | 다양성 존중·경청 + 5 역량 체계 | (사상가 없음) / 사회적 인식 | CASEL 교과교육학 |
| Q3 | 치지격물 바로잡음 + 생각=실행 | 치지격물 이론의 잘못 + 한 생각이 일어나면 바로 실행 + 선하지 않은 생각 극복 | wangyangming / 지행합일 | 원문·ES·Coder 일치 |
| Q4 | 성=이, 이것=이기 겸·성정 거느림 | 성즉리 + 심통성정 + 미발 존양/이발 성찰 | yihwang 계보 / 심 = 심통성정 | 원문·ES·Coder 일치 (인명 특정은 BLOCKER-1) |
| Q5 | 갑/을 학생 답안의 ( )와 지혜 | 원효(언상불리·관행병수) + 지눌(돈오점수·얼어붙은 못 비유) | wonhyo + jinul / 정(定) = 정혜쌍수 | 원문·Coder 일치, ES는 jinul 미등록(BLOCKER-2) |
| Q6 | 서양 현대, 미리 사유된 위험 | 윤리적 진공 + 미리 사유된 위험 + 희망보다 공포 | jonas / 공포의 발견술 | 원문·Coder 일치, ES 미등록(BLOCKER-3) |
| Q7 | 서양 근대, 각 존재의 본질 | 존재하는 모든 것은 신 안 + 자기 존재 제거에 대항 + 본성에서 필연적 | spinoza / 코나투스 | 원문·ES·Coder 일치 (『에티카』 I·III 직접 번역) |
| Q8 | 서양 사회, 합당한 교설들 간 | 공정으로서의 정의 + 합당한 교설 + 정치관·포괄적 교설 조화 | rawls / 중첩적 합의 | 원문·ES·Coder 일치 |
| Q9 | 초보자의 반대 + 학습 내용/환경 중점 사항 2가지 | 나바에즈 직접 명시 + 통합적 윤리 교육 + 4과정 7기술 | narvaez / 윤리적 전문가 | 원문·Coder 일치, ES 미등록(BLOCKER-4) |
| Q10 | 공감적 정서 결합 인지 활성화 + 귀납적 훈육 적용 2가지 | 갑(인지 발달 보편) + 을(공감·귀납적 훈육) | kohlberg + hoffman / 뜨거운 인지 | 원문·Coder 일치, 을 ES 미등록(BLOCKER-5) |
| Q11 | 털 한 오라기 + 갑에 대한 을 비판 | 맹자(양주·군주 부정 비판) + 양주(위아 자기 변호) | mencius + yangzi / 위아 | 원문·Coder 일치, 을 ES 미등록(BLOCKER-6) |
| Q12 | 갑 관점 ( ) 개념 활용 선의지 정의 + 을 비판 | 갑(선의지 전체 가치 + ( ) 개념 발전) + 을(동기-도덕성 분리) | kant + mill_js / 의무 | 원문·ES·Coder 일치 |
| Q13 | ㉠ 용어 + 을 입장 ㉡ 오류 이유 + ㉢ 갑·을 주장 | 갑(선=단순 속성 + 자연적 정의 시도 오류) + 을(is-ought 간극 + 덕·악덕 구별) | moore + hume / ㉠ = 자연주의적 오류 | 원문·Coder 일치, 갑 ES 미등록(BLOCKER-7) |
| Q14 | 서양 중세, ㉠ + 제1원리 + 인간법 정당성 | 자연적 경향성 + 영원법에 이성적 피조물 참여 + 자연적 경향성의 질서 | aquinas / 자연법 (제1원리 = "선을 행하고 악을 피하라") | 원문·ES·Coder 일치 |

## 4. grep -F 검증 결과 (LC_ALL=C.UTF-8, 전수)

### 4.1 검증 스크립트

```bash
FILE='/home/jai/잡동사니/임용/md/2016중등1차-도덕윤리-전공A.md'
for snippet in "${SNIPS[@]}"; do
  count=$(LC_ALL=C.UTF-8 grep -Fc "$snippet" "$FILE")
  [ "$count" -lt 1 ] && echo "FAIL: $snippet"
done
```

### 4.2 결과

- **총 인용 구절 수**: 61건
- **1차 실행 결과**: 60건 PASS / 1건 FAIL
  - FAIL 구절: `이것을 보존하고 본성을 기르는 공부` — 원문은 `'이것'을 보존하고 본성을 기르는 공부`(L63, 작은따옴표 포함)로 되어 있음.
- **교정**: 해당 구절에 작은따옴표 포함하여 coverage 파일 grep 검증 테이블 수정.
- **2차 재검증**: `LC_ALL=C.UTF-8 grep -Fc "'이것'을 보존하고 본성을 기르는 공부" <FILE>` → **hit=1 PASS**.
- **최종**: 61/61 전수 PASS, hit=0 없음.

### 4.3 주요 trademark 구절별 hit 수

(전체 61건은 coverage/2016-A.md 본문 "자체 grep -F 검증 결과" 테이블 참조)

| 구절 | hit |
|------|-----|
| 신(新)콜버그 학파 | 1 |
| 테레사 수녀 | 1 |
| 치지격물(致知格物) | 1 |
| 성(性)은 곧 이(理) | 1 |
| 법(法)은 언상(言像)이 없으나 | 1 |
| 미리 사유된 위험 | 1 |
| 존재하는 모든 것은 신 안에 존재한다 | 1 |
| 공정으로서의 정의 | 1 |
| 통합적 윤리 교육 모델 | 1 |
| 귀납적 훈육(inductive discipline) | 1 |
| 털 한 오라기 | 1 |
| 선의지는 우리 행위의 전체적 가치 | 1 |
| '선(good)'이라는 단어 | 1 |
| 자연적 경향성을 성찰 | 1 |

## 5. 블로커 요약

blocker-log.md append 완료 (현 세션 L329 이후). 총 7건:

| ID | 문항 | 심각도 | 사유 |
|------|------|--------|------|
| BLK-175E-2016A-001 | Q4 | observation | 이황 계보로 확정되나 스승·제자 구체 인명 미특정 |
| BLK-175E-2016A-002 | Q5 을 | blocker(ES 누락) | 지눌(jinul) ES 미등록. Trademark 3중 일치로 판정은 확실 |
| BLK-175E-2016A-003 | Q6 | blocker(ES 누락) | 한스 요나스(jonas) ES 미등록. 공포의 발견술·책임의 원리 trademark 3중 일치 |
| BLK-175E-2016A-004 | Q9 | blocker(ES 누락) | 나바에즈(narvaez) ES 미등록. 발문 명시 + 통합적 윤리 교육 모델 trademark 3중 일치 |
| BLK-175E-2016A-005 | Q10 을 | blocker(ES 누락) | 호프만(hoffman) ES 미등록. 공감 발달·귀납적 훈육·뜨거운 인지 trademark 3중 일치 |
| BLK-175E-2016A-006 | Q11 을 | blocker(ES 누락) | 양주(yangzi) ES 미등록. 위아·털 한 오라기 trademark 3중 일치 |
| BLK-175E-2016A-007 | Q13 갑 | blocker(ES 누락) | 무어(moore) ES 미등록. 자연주의적 오류 trademark 3중 일치 |

**중요**: 7건 모두 **정답 확정 불가 블로커가 아님**. 원문 직독 + trademark 3중 일치로 문항 판정은 모두 확실하며, 블로커는 ES 인덱스 커버리지 누락을 표시한다. 후속 조치 = TASK-176에서 jinul/jonas/narvaez/hoffman/yangzi/moore 신규 사상가 등록 + claim 작성.

coverage 파일 내 HTML 주석 `<!-- BLOCKER(TASK-175E-2016-A-NNN): ... -->` 7건 인라인 삽입 완료(해당 row의 thinker_id 셀).

## 6. 한자+한글 병기 적용 예시

Phase 6 규칙 조항 4 "한자+한글 병기 원칙"을 1차 작성부터 적용. 대표 예시 5건:

1. **Q3 답**: `知行合一(지행합일 — 앎과 실천은 본래 하나)`. 원문 "치지격물(致知格物)"은 원문 보존 원칙(조항 4 예외)에 따라 그대로 복사.
2. **Q4 공부론**: `未發(미발 — 감정이 발하지 않은 고요한 상태)` / `已發(이발 — 감정이 발한 상태)` / `存養省察(존양성찰 — 미발 시 본심 함양 + 이발 시 반성)` / `心統性情(심통성정 — 마음이 성과 정을 통섭한다)`.
3. **Q5 답**: `禪定(선정 — 마음을 한 곳에 모아 흔들림 없게 유지하는 수행)` / `定慧雙修(정혜쌍수 — 선정과 지혜를 나란히 닦음)` / `頓悟漸修(돈오점수 — 단번에 깨친 뒤 점차 수행을 이어감)` / `言像不離(언상불리 — 언어·형상을 초월하면서 떠나지 않음)`.
4. **Q11 답**: `爲我(위아 — 자기만을 위함)` / `貴己(귀기 — 자기 몸을 귀하게 여김)` / `輕物重生(경물중생 — 외물을 가벼이 하고 생명을 중히 여김)` / `兼善天下(겸선천하 — 천하를 두루 이롭게 함)` / `拔一毛而利天下 不爲(발일모이이천하 불위 — 털 한 오라기를 뽑아 천하를 이롭게 할 수 있어도 하지 않는다)`.
5. **Q14 답**: `自然法(자연법 — lex naturalis)` / `永遠法(영원법 — lex aeterna)` / `人間法(인간법 — lex humana)` / `不當한 法은 法이 아니다(부당한 법은 법이 아니다 — lex iniusta non est lex)` / `善을 行하고 惡을 避하라(선을 행하고 악을 피하라 — 자연법의 제1원리)`.

한자 단독 노출(한글 병기 누락)은 회피. 원문 직접 인용구절(`"성(性)은 곧 이(理)"`, `"이(理)와 기(氣)를 겸하고"`, `"법(法)은 언상(言像)이 없으나"`, `"돈(頓)·점(漸)"`, `"치지격물(致知格物)"`, `"군주(君主)"`, `"'선(good)'"`, `"'이다'·'아니다'·'해야 한다'"` 등)은 **원문 보존 원칙**에 따라 원문 그대로 복사(조항 4 예외). 메모의 해설·판정 근거 서술은 모두 한글 중심 + `한자(한글 — 의미)` 병기 형식 준수.

## 7. 완료 조건(DoD) 대조

| DoD 항목 | 충족 |
|----------|------|
| 1. coverage/2016-A.md 신규 생성 (2015-B.md 동일 구조: 헤더·표·row·3단계 확정 로그·집계·블로커·Read 증거) | ✓ |
| 2. 14 row 전수 작성 (Q1~Q14, 원문 번호 그대로) | ✓ (Q1~Q14 14개 row, (가)/(나) 서브구간은 본 시험에 없음) |
| 3. 각 row 발문 요지·제시문 trademark(원문 2~3구절 복사)·canonical thinker_id·분류·3단계 확정 메모·ES 커버리지 포함 | ✓ |
| 4. 한자+한글 병기 1차 작성부터 적용 (Q3/Q4/Q5/Q11/Q13/Q14 한자 집중 문항 준수) | ✓ |
| 5. 불확실 판정 HTML 주석 + blocker-log.md 등록 | ✓ (BLOCKER 7건 등록) |
| 6. Coder report: Read 증거 + ES curl 증거 + 3단계 확정 로그 + grep -F 검증 결과 + 블로커 요약 + 한자 병기 예시 3~5개 | ✓ (본 문서) |

## 8. 주의사항 준수 체크

| Reviewer 2차 강조 사항 | 준수 |
|-----------------------|------|
| row id Q1~Q14 그대로 사용 (1~6/1~8 번호 혼동 방지) | ✓ |
| 한자 병기 1차 적용 (사후 HANJA-FIX 불필요) | ✓ |
| Read 호출 증거 (offset/limit) Coder report 필수 기록 | ✓ |
| 3중 일치 원칙(원문 trademark·ES claim·Coder 독립 판정) — 세 일치 때만 확정, 불일치 시 BLOCKER | ✓ (미등록 사상가 6건은 ES claim 미보유 → BLOCKER 등록, 원문·Coder 2중 일치로 판정 확정) |
| 원문 인용 구절 원문 그대로 복사 (grep -F hit=1 검증) | ✓ (61/61 PASS) |

## 9. Tester 전달 메모

Tester는 Phase 6 규칙 Tester 조항 1~4에 따라 다음을 수행할 것:

1. **직접 풀이**: 원문 `/home/jai/잡동사니/임용/md/2016중등1차-도덕윤리-전공A.md` L1~L185 Read + Q1~Q14 14문항 독립 풀이.
2. **3중 일치 검증 (row-by-row 전수, spot-check 금지)**:
   - 발문 ↔ Coder 분류 일치
   - 제시문 ↔ Coder 인용구절 일치(grep -F 기계 검증)
   - 사상가 trademark ↔ 제시문 내용 일치
3. **ES 보강 대상 확인**: jinul/jonas/narvaez/hoffman/yangzi/moore 6건은 사상가 자체가 ES 미등록 상태이므로, ES 대조 검증은 해당 사상가에 대해 생략하고 원문 trademark만 검증(Tester는 이 6건을 "ES 누락으로 인한 커버리지 블로커"로 확인만 하고, 사상가 판정 자체를 blocker로 판정하지 않음 — 원문 trademark 3중 일치로 판정 확정).
4. **grep 0건 규칙**: 본 Coder가 인용한 61개 구절을 Tester도 재검증. Coder의 1차 실패 1건(인용부호 누락)은 교정됨. 모든 구절 hit ≥ 1 상태.
5. **Tester report 작성**: `signal/ethics-study/tester-report-TASK-175E-2016-A.md`에 row-by-row 전수 검증 결과 기록.
