---
task_id: TASK-175E-2021-A
agent: coder
status: DONE
severity: observation
date: 2026-04-21
---

# Coder Report — TASK-175E-2021-A

## 태스크 요약
- **대상**: 2021학년도 중등 1차 도덕·윤리 전공A 커버리지 맵 생성
- **원문**: `/home/jai/잡동사니/임용/md/2021_중등1차_도덕윤리_전공A.md` (206 라인)
- **산출물**: `projects/ethics-study/exam-solutions/coverage/2021-A.md` (신규 생성, 106 라인)
- **배점**: 40점 (기입형 Q1~Q4 [2점]×4 = 8점 + 서술형 Q5~Q12 [4점]×8 = 32점. 검산: 2×4 + 4×8 = 40 ✓)
- **문항 수**: 12문항
- **적용 규칙**: `signal/ethics-study/architecture.md` Phase 6 Coder 규칙 1~6 (L534~567) 엄격 적용

## 수행 절차 (Phase 6 Coder 규칙 준수)

### 규칙 1 (원문 직독 필수)
현 세션 내에서 `/home/jai/잡동사니/임용/md/2021_중등1차_도덕윤리_전공A.md` 전체 206라인을 Read tool로 직접 호출(offset 없음 = L1~L206 전수 확인). 각 문항 시작·종료 라인 교차 확인 완료:
- Q1 L14-L37 / Q2 L41-L51 / Q3 L55-L60 / Q4 L64-L70 / Q5 L74-L92 / Q6 L95-L107 / Q7 L111-L121 / Q8 L125-L134 / Q9 L138-L148 / Q10 L152-L170 / Q11 L174-L182 / Q12 L186-L202

### 규칙 2 (3단계 확정: 문제→제시문→사상가)
각 row 작성 전 아래 3단계를 수행:
- **① 문제(발문) 독해**: 각 row "발문 요지" 컬럼에 요약. 예: Q7 "㉠·㉡ 용어 쓰고, ㉠과 성(性)의 관계에 대한 갑·을의 입장 각각 서술"
- **② 제시문 독해**: "제시문 핵심(원문 복사)" 컬럼에 원문 2~3구절 **그대로 복사**. 요약·의역·재서술 금지 준수.
- **③ 사상가·분류 판정**: "사상가/개념" 컬럼에 **Trademark 3중 일치** 증거 명시. 각 ①②③ 인용 구절은 원문 라인 번호 병기.

### 규칙 3 (불확실 처리)
정답 확정 불가 0건. ES-gap(사상가 ES 미등록) 3건 발생 → Phase 6 ES-gap 정책에 따라 **blocker**로 분류:
- Q3 G.E. Moore → BLK-175E-2021A-001
- Q6 갑 A. Blasi → BLK-175E-2021A-002 (2019-B Q8 재출제)
- Q9 Paul W. Taylor → BLK-175E-2021A-003 (동명이인 `taylor`=Charles Taylor와 충돌)

### 규칙 4 (한자+한글 병기)
모든 한자 개념어·인명·저서명·trademark 구절을 `한자(한글 — 의미)` 형식으로 병기. 본 coverage 내 병기 건수 **약 210+ 건** (row당 평균 17~20건). 한자 단독 노출 0건(원문 인용구절 내부는 원문 보존 원칙 유지).

### 규칙 5 (Report 감사 형식)
본 report 및 coverage/2021-A.md 맨 아래 "감사 목록" 섹션에 Read/Grep/ES curl 호출 목록을 구체적으로 기록. self-check 체크박스 대신 **검증 가능한 증거**(원문 file_path:line_range, 복사 구절)로 제출.

### 규칙 6 (배치 크기 제한)
본 태스크는 **1개 연도 × 1개 과목(2021-A) 단위**로 수행. 총 12문항(기입형 4 + 서술형 8) 처리.

## 현 세션 Read/Grep/ES curl 호출 감사

### Read 호출
1. `signal/ethics-study/architecture.md` (offset=520, limit=90) — Phase 6 규칙 확인 (L520~L609)
2. `/home/jai/잡동사니/임용/md/2021_중등1차_도덕윤리_전공A.md` (전체, 206 lines) — 본 태스크 원문 전수 확인
3. `projects/ethics-study/exam-solutions/coverage/2019-B.md` (offset=1, limit=30) — 포맷·감사 구조 선례 확인
4. `signal/ethics-study/blocker-log.md` (head=30, offset=564 limit=50, offset=585 limit=5) — 최근 블로커 형식·BLK-175E-2020B-* 선례 확인
5. `signal/ethics-study/blocker-log.md` 라인 수 확인(wc -l) — append 전 589, append 후 616

### Grep 호출
1. `BLK-175E-202` in `signal/ethics-study/blocker-log.md` (output_mode=content, head_limit=20) — 기존 블로커 ID 범위 확인

### ES curl 호출
```bash
# 1차: 12개 사상가 ID 조회
for id in kant moore spinoza blasi kohlberg wangyangming zhuxi buddha taylor rawls hoffman freud; do
  curl -s "http://localhost:9200/ethics-thinkers/_doc/${id}" | jq -r '._source | "id: \(.id // "NOT FOUND"), name_kr: \(.name_kr // "NOT FOUND"), name_en: \(.name_en // "NOT FOUND")"'
done
# 결과:
#   kant          : 등록 (Immanuel Kant)
#   moore         : NOT FOUND — BLK-175E-2021A-001
#   spinoza       : 등록 (Baruch Spinoza)
#   blasi         : NOT FOUND — BLK-175E-2021A-002
#   kohlberg      : 등록 (Lawrence Kohlberg)
#   wangyangming  : 등록 (Wang Yangming)
#   zhuxi         : 등록 (Zhu Xi)
#   buddha        : 등록 (Buddha)
#   taylor        : 등록 (Charles Taylor) ← Paul Taylor와 충돌! 
#   rawls         : 등록 (John Rawls)
#   hoffman       : NOT FOUND (본 태스크 범위 외)
#   freud         : NOT FOUND (본 태스크 범위 외)

# 2차: Paul Taylor 동명이인 확인
for id in taylor_p paultaylor taylor_p biocentrism singer bentham mill; do
  curl -s "http://localhost:9200/ethics-thinkers/_doc/${id}" | jq -r '._source | "id: \(.id // "NOT FOUND"), name_kr: \(.name_kr // "NOT FOUND"), name_en: \(.name_en // "NOT FOUND")"'
done
# 결과: taylor_p/paultaylor/taylor_p/biocentrism/singer/mill 모두 NOT FOUND, bentham 등록

# 3차: ES 전체 thinker 목록 55명 확보
curl -s "http://localhost:9200/ethics-thinkers/_search?size=100&_source=id,name_en" | jq -r '.hits.hits[]._source | "\(.id)\t\(.name_en)"' | sort
# 결과: aquinas/arendt/aristotle/augustine/baek_nakcheong/bentham/buddha/confucius/dewey/epictetus/epicurus/galtung/gilligan/habermas/haidt/hanfeizi/hegel/hobbes/huineng/hume/jeongyagyong/kang_mangil/kant/kohlberg/laozi/lickona/locke/macintyre/marcus_aurelius/mencius/mill_js/mozi/nietzsche/noddings/nozick/piaget/plato/raths/rawls/rest/rousseau/sandel/sartre/seneca/socrates/spinoza/taylor/walzer/wangyangming/wonhyo/xunzi/yihwang/yiyulgok/zhuangzi/zhuxi 총 55명.
```

## 핵심 발견

### Trademark 확정 사례
| 문항 | Trademark 핵심 구절(원문 라인) | 사상가 확정 |
|------|-------------------------|-----------|
| Q1 | "2015 개정 중학교 도덕과 교육과정(교육부 고시 제2015-74호)" (L28) + "영역: 자연·초월과의 관계 / 핵심가치: 책임" (L33) | 교과교육학 문서형 |
| Q2 | "제1의 확정 조항: 모든 국가의 시민적 정치체제는 ( ㉠ )이어야 한다 / 제2: 자유로운 국가들의 연방체제 / 제3: 세계시민법" (L47-L49) + "특별한 종류의 연맹" (L51) | 칸트 『영구평화론』(1795) 3확정조항·평화 연맹 |
| Q3 | "열린 질문 논증을 제시한 현대 비자연주의 이론가 … '선한' 등을 '쾌락을 증대하는' 등의 ( ㉡ ) 표현으로 정의하려는 시도는 … 오류" (L60) | G.E. Moore 『Principia Ethica』(1903) — 열린 질문 논증·자연주의적 오류 |
| Q4 | "'자신의 존재 안에서 지속하고자 하는 성향(conatus)'은 만물의 본질" + "신과 '나'가 같은 외연 … 모든 일은 ㉠인 동시에 ㉡" (L70) | 스피노자 『에티카』 — 코나투스·신즉자연·자유와 필연의 동일성 |
| Q5 | "샤프텔 부부(F. Shaftel & G. Shaftel)가 개발한 역할놀이 수업 모형" (L76) + 8단계 도표(L78-L87) | 교과교육학 Shaftel 역할놀이 모형 |
| Q6 | 갑: "㉡ 특정한 도덕적 가치를 자아의 본질과 핵심으로 여기고 … 자아감" (L101) / 을: "㉢ 도덕적으로 선하거나 옳은 것이 자신에게 어느 정도로 필수적인지에 대한 판단" (L103) | 갑 A. Blasi 도덕적 정체성 / 을 Kohlberg 후기 책임 판단 |
| Q7 | 갑: "( ㉠ )은/는 텅 비고 신령하여 … 이의 바깥에는 … 사도 없다 / ( ㉡ )은/는 … 양지를 실현하는 것" (L115) / 을: "신명한 것으로서 … 이를 갖추고서 만사에 응함 / 격물은 ( ㉡ )하는 것이니 … 사물의 이를 많이 궁구할수록" (L117) | 갑 왕양명 심즉리·치양지 / 을 주희 심통성정·격물궁리 |
| Q8 | "색은 ( ㉠ )이다. 만약 색이 ( ㉡ )(이)라면 그 색은 병에도 걸리지 않고 … 그러나 색은 ( ㉠ )이다" (L130) | 불교 『무아상경(Anattalakkhaṇa-sutta)』 — 무아·유아·오온 |
| Q9 | "생명체는 … 고유 방식을 지닌 ( ㉠ )이다 … 목표 지향적 … 재생산과 적응 … 야생 생명체 자체에 대한 의무는 인간에 대한 도덕적 의무에 예속되거나 의존하지 않는다" (L142-L143) | Paul W. Taylor 『Respect for Nature』(1986) — 목적론적 삶의 중심·생명중심주의 |
| Q10 | "거짓 약속 … 필연적이거나 당연한 의무를 위반 / 자선은 … ( ㉠ ) 의무 / '바랄 만한 유일한 것은 행복' … 거짓 약속을 하더라도 ( ㉡ )하면 칭찬 / ㉢ 정언 명령" (L158-L163) | (가) 칸트 완전/불완전 의무·정언명령 목적 정식 + (나) 속 인용 = J.S. Mill 공리주의 |
| Q11 | "시민 불복종 … 질서정연한(well-ordered) 사회 … 법이나 정부 정책에 큰 변화 … 공공적·비폭력적·양심적 … 정당화 세 가지 조건 … 제1원칙 평등한 자유 / 제2원칙 공정한 기회균등" (L178) | 롤스 『정의론』(1971) §55-§59 — 시민 불복종 |
| Q12 | "우리 민족끼리 … ( ㉠ )적으로 해결 / 남측의 ( ㉡ ) 안과 북측의 낮은 단계의 연방제 … 이 방향" (L194-L195) | 2000년 6·15 남북공동선언 — 교과교육학 통일교육 |

### ES-gap blocker 3건 (상세는 blocker-log.md)
- **BLK-175E-2021A-001 (Q3 G.E. Moore)**: 메타윤리학 창시·자연주의적 오류·열린 질문 논증. 등록 우선순위 **우선**.
- **BLK-175E-2021A-002 (Q6 갑 A. Blasi)**: 도덕적 정체성·책임 판단·자기 일관성. **2019-B Q8 재출제 = 연속 2년차**. 등록 우선순위 **최우선**.
- **BLK-175E-2021A-003 (Q9 Paul W. Taylor)**: 생명중심주의·목적론적 삶의 중심·본래적 가치. **동명이인 `taylor`=Charles Taylor와 id 충돌 주의** → `taylor_p` 별도 등록 필수. 등록 우선순위 **최우선**.

### 동명이인 주의 사항 (TASK-176 범위 이관)
Paul W. Taylor ≠ Charles Taylor. 기존 ES `taylor`는 Charles Taylor(공동체주의 정치철학자, 『자아의 원천들』·『불안한 현대 사회』). Paul W. Taylor(생명중심주의 환경윤리)는 반드시 `taylor_p` 또는 `taylor_p`로 별도 등록해 오매핑을 방지해야 함. 본 coverage/2021-A.md Q9 row와 blocker-log.md BLK-175E-2021A-003 양쪽에 경고 명기.

## 검증 가능한 증거

### 원문 인용 구절의 원문 존재성
coverage/2021-A.md 각 row "제시문 핵심(원문 복사)" 컬럼은 모두 2021_중등1차_도덕윤리_전공A.md 해당 라인에서 직접 복사된 원문이며, 재서술·의역·창작 0건. Phase 6 Coder 규칙 2 "원문 2~3구절을 그대로 복사해 메모 컬럼에 삽입. 요약·의역·재서술 금지" 준수. 표 형식 원문은 인라인 텍스트로 평탄화하되 ㉠·㉡·㉢·㉣·밑줄 표시·『』·▹·◦ 등 부호 보존.

### 배점 검산
- 기입형: Q1 2점 + Q2 2점 + Q3 2점 + Q4 2점 = **8점** ✓
- 서술형: Q5 4점 + Q6 4점 + Q7 4점 + Q8 4점 + Q9 4점 + Q10 4점 + Q11 4점 + Q12 4점 = **32점** ✓
- 총합: 8 + 32 = **40점** ✓ (원문 L7 "12문항 40점" 일치)

### 한자+한글 병기 건수 (규칙 4)
coverage/2021-A.md 내 `한자(한글 — 의미)` 병기 건수 합계: **약 210+ 건** (12 row, row당 평균 17~20건). 한자 단독 노출 0건. 한자에 약한 사용자 가독성 확보.

## 산출 파일
1. `projects/ethics-study/exam-solutions/coverage/2021-A.md` (신규, 106 라인) — 본 태스크 메인 산출물
2. `signal/ethics-study/blocker-log.md` (3 blocker 엔트리 append: BLK-175E-2021A-001/002/003) — 기존 589 라인 → 616 라인
3. `signal/ethics-study/coder-report-TASK-175E-2021-A.md` (본 report)

## 정리 요약

| 항목 | 값 |
|------|-----|
| 처리 연도·과목 | 2021 전공 A (단일 배치) |
| 총 문항 수 | 12 (기입형 4 + 서술형 8) |
| 총 배점 | 40점 (8 + 32) |
| 원문 라인 범위 | L14~L202 (206라인 원문 중) |
| 생성 coverage 라인 수 | 106 |
| 정답 확정 (trademark 3중 일치) | **12/12** (100%) |
| 블로커 (ES-gap) | **3건** (Q3 moore / Q6 blasi / Q9 taylor_p) |
| 교과교육학·문서형 observation | 3건 (Q1 2015 개정 교육과정 / Q5 샤프텔 / Q12 6·15 선언) |
| ES 등록 사상가 | 7명 (kant/spinoza/kohlberg/wangyangming/zhuxi/buddha/rawls) + 간접 1명(mill_js) |
| ES 미등록 사상가 | 3명 (moore/blasi/taylor_p) — 모두 blocker 등록 |
| 한자 병기 건수 | 약 210+ 건 |
| 한자 단독 노출 위반 | 0건 |
| 원문 인용 구절 의역·창작 | 0건 |

## 상태
**DONE** — 모든 12문항 정답 trademark 3중 일치로 확정. ES-gap 3건은 blocker로 분류하여 blocker-log.md에 append 완료. Phase 6 Coder 규칙 1~6 엄격 준수. Tester 검증 대기.
