---
task_id: TASK-175E-2022-A
agent: Coder
status: DONE
date: 2026-04-21
severity: observation
---

# TASK-175E-2022-A Coder Report

## 작업 요약

2022학년도 중등임용 도덕·윤리 전공 A(12문항 40점) 커버리지 맵을 Phase 6 Coder 규칙 1~6 엄격 준수하에 작성 완료.

- **산출물**: `projects/ethics-study/exam-solutions/coverage/2022-A.md` (신규 생성, 102 lines)
- **블로커 로그 append**: `signal/ethics-study/blocker-log.md` BLK-175E-2022A-001~007 (7건 추가, 679→742 lines)
- **배점 검증**: 기입형 2점×4 + 서술형 4점×8 = 8 + 32 = **40점 PASS** (원문 L7 "12문항 40점" 일치)

## 문항별 사상가/정답 요약

| Q | 유형 | 사상가 | thinker_id | ES 상태 | 정답 핵심 | 원문 line |
|---|------|--------|-----------|--------|----------|-----------|
| Q1 | 기입형 | 리코나 + 덕 윤리 | `lickona`+개념 | 등록 | ㉠=수행적 인격(performance character) / ㉡=덕 윤리 | L14-L20 |
| Q2 | 기입형 | 지눌 『수심결』 | `jinul` | **미등록** (BLK-001, **3연도 연속**) | ㉠=공적영지(空寂靈知) / ㉡=한 생각(一念) | L24-L28 |
| Q3 | 기입형 | 미국 공화주의(제도론) | (교과교육학) | N/A | ㉠=삼권분립 / ㉡=탄핵 | L32-L36 |
| Q4 | 기입형 | 정약용(다산) | `jeongyagyong` | 등록 | ㉠=대체(大體) / ㉡=소체(小體) | L40-L45 |
| Q5 | 서술형 | 노직 | `nozick` | 등록 | ㉠=자연상태 / ㉢=극소국가 + 공통/차이점 | L49-L58 |
| Q6 | 서술형 | 갑=페팃, 을=T.H.그린 | `pettit`+`green_th` | **둘 다 미등록** (BLK-002 페팃 재출제, BLK-003 그린) | ㉠=비지배 / ㉡=적극적 자유 + ㉡ 문제점 2가지 | L62-L72 |
| Q7 | 서술형 | 플라톤 | `plato` | 등록 | ㉢=철인왕(지혜덕 2특징) + ㉡ 사유재산 금지 이유 2가지 | L76-L85 |
| Q8 | 서술형 | 갑=콜버그, 을=튜리엘 | `kohlberg`+`turiel` | 갑 등록, **을 미등록** (BLK-004, **3연도 연속**) | ㉠=도덕적 분위기 + 도덕/인습 규칙 특징 + ㉤ 원인 | L89-L101 |
| Q9 | 서술형 | 칸트 | `kant` | 등록 | ㉠=행복 / ㉡=의지 + ㉢·㉣ 보편법칙 위반 이유 | L105-L117 |
| Q10 | 서술형 | 갑=신수, 을=혜능, (나)=지의 | `shenxiu`+`huineng`+`zhiyi` | 혜능 등록, **신수·지의 미등록** (BLK-005·006) | ㉠=보리(菩提) / ㉡=방등시 + 점·돈 교 | L121-L140 |
| Q11 | 서술형 | 갑=칸트, 을=비례응보(입장), 병=베카리아 | `kant`+(입장)+`beccaria` | 칸트 등록, **베카리아 미등록** (BLK-007) | ㉠=비례의 원리 / ㉡=예방(억지력) + ㉢ 부정의 2가지 | L143-L156 |
| Q12 | 서술형 | (가) 2015 교육과정 + (나) 길리간 | `gilligan` + (가)교과교육학 | 길리간 등록, (가) observation | ㉠=실천 윤리 / ㉡=내러티브 + ㉢·㉣ 학생활동 | L159-L202 |

## 블로커 요약 (ES-gap 7건)

| BLK ID | 인물 | 우선순위 | 재출제 여부 |
|--------|------|---------|------------|
| BLK-175E-2022A-001 | 보조국사 지눌 (jinul) | **최최우선** | **2020-A·2021-B·2022-A 3연도 연속** |
| BLK-175E-2022A-002 | 필립 페팃 (pettit) | 최우선 | **2020-A 재출제** |
| BLK-175E-2022A-003 | 토머스 힐 그린 (green_th) | 최우선 | 신규 |
| BLK-175E-2022A-004 | 엘리엇 튜리엘 (turiel) | **최최우선** | **2018-B·2021-B·2022-A 3연도 연속** |
| BLK-175E-2022A-005 | 북종 신수 (shenxiu) | 우선 | 신규 |
| BLK-175E-2022A-006 | 천태 지의 (zhiyi) | 우선 | 신규 |
| BLK-175E-2022A-007 | 체사레 베카리아 (beccaria) | 최우선 | 신규 |

**3연도 이상 재출제**: `jinul`, `turiel` — TASK-176 ES 등록 시 **최최우선**.

## 감사 (현 세션 Read/Grep/ES curl 호출 목록)

### Read 호출
1. `signal/ethics-study/architecture.md` offset=485 limit=120 → Phase 6 Coder 규칙 1~6 + thinker_id suffix 규약(L491)
2. `/home/jai/잡동사니/임용/md/2022_중등1차_도덕윤리_전공A.md` offset=0 (전체 206 lines) → 본 태스크 원문 전수 직독
3. `projects/ethics-study/exam-solutions/coverage/2021-A.md` offset=0 limit=60 + bash awk 샘플 + 전체 wc → 선례 포맷 확인
4. `projects/ethics-study/exam-solutions/coverage/2021-B.md` wc → 137 lines 확인
5. `projects/ethics-study/exam-solutions/coverage/2020-A.md` wc → 347 lines 확인
6. `signal/ethics-study/blocker-log.md` offset=0 limit=50 → 초두 정책·BLK-001 구조 확인
7. `signal/ethics-study/blocker-log.md` offset=618 limit=70 → BLK-175E-2021B-001~007 전체 포맷 확인
8. `signal/ethics-study/blocker-log.md` offset=670 limit=10 → 파일 말미 라인 확인 (append 지점 결정)
9. `signal/ethics-study/blocker-log.md` 전체 wc → 679 lines (append 전)
10. `signal/ethics-study/coder-report-TASK-175E-2021-B.md` offset=0 limit=80 → 선례 coder-report 포맷 확인

### Grep 호출
- `grep "^### BLK-175E-2022" blocker-log.md` → 0건 (신규 append)
- `grep -c "^### BLK-175E" blocker-log.md` → 40건 (append 전)
- `grep "^### BLK-175E-202" blocker-log.md | tail -20` → 기존 2021-B 번호 체계 확인
- `ls signal/ethics-study/ | grep coder-report-TASK-175E` → 기존 coder-report 19개 확인 (2022-A는 신규)

### ES curl 호출
- **1차** (21 id 개별 조회): `lickona`·`jinul`·`wonhyo`·`plato`·`kant`·`nozick`·`pettit`·`green_th`·`green`·`aristotle`·`bentham`·`beccaria`·`kohlberg`·`turiel`·`jeong_yakyong`·`jeongyagyong`·`gilligan`·`nagarjuna`·`huineng`·`shenxiu`·`zhiyi` — 결과: 등록(11) = lickona·wonhyo·plato·kant·nozick·aristotle·bentham·kohlberg·jeongyagyong·gilligan·huineng / 미등록(10) = jinul·pettit·green_th·green·beccaria·turiel·jeong_yakyong(canonical은 jeongyagyong)·nagarjuna·shenxiu·zhiyi
- **2차** (전체 사상가 목록): `curl -s "http://localhost:9200/ethics-thinkers/_search?size=100&_source=id,name_kr,name_en" | jq ...` → 55명 전체 확보. Q1~Q12 출제 중심 16명 중 9 등록, 7 미등록 최종 확정 (Q3 미국 공화주의는 제도론이라 사상가 N/A).

### 원문 인용 구절 존재성
본 coverage/2022-A.md 각 row의 "제시문 핵심(원문 복사)" 컬럼은 모두 2022_중등1차_도덕윤리_전공A.md 해당 라인에서 직접 복사된 원문이며, 재서술·요약·창작 없음. line 범위(Q1 L14-L20, Q2 L24-L28, Q3 L32-L36, Q4 L40-L45, Q5 L49-L58, Q6 L62-L72, Q7 L76-L85, Q8 L89-L101, Q9 L105-L117, Q10 L121-L140, Q11 L143-L156, Q12 L159-L202)는 Read 호출 확인 범위와 일치.

### 한자 병기 건수
약 **280+ 건** (row 평균 23~28건). Phase 6 Coder 규칙 4 엄격 준수. 한자 단독 노출 0건(원문 인용구절 내부 한자 표기는 원문 보존 원칙에 따라 유지).

### 배점 검산
- 기입형: Q1 2 + Q2 2 + Q3 2 + Q4 2 = **8점**
- 서술형: Q5~Q12 각 4점 × 8 = **32점**
- 총합: 8 + 32 = **40점** ✓ (원문 L7 "12문항 40점" 일치)

## 완료 조건 충족 여부

| 완료 조건 | 상태 | 증거 |
|-----------|------|------|
| 1. coverage/2022-A.md 생성 (헤더·배점 검증·문항별 행·블로커 섹션·감사) | **PASS** | 102 lines, 12 row, 7 BLK HTML 주석, 감사 섹션 포함 |
| 2. blocker-log.md에 BLK-175E-2022A-001~007 append | **PASS** | 7건 append (679→742 lines) |
| 3. coder-report-TASK-175E-2022-A.md 작성 | **PASS** | 본 파일 |
| 4. Phase 6 Coder 규칙 1: 원문 직독 | **PASS** | 원문 206 lines 전수 Read 완료 |
| 5. Phase 6 Coder 규칙 2: 3단계 확정 + 2~3 구절 복사 | **PASS** | 12 row 모두 trademark 3중 일치 + 복사 인용 |
| 6. Phase 6 Coder 규칙 3: 불확실 처리 | **PASS** | ES 미등록 7건 모두 BLOCKER 주석 + blocker-log 등록 |
| 7. Phase 6 Coder 규칙 4: 한자+한글 병기 | **PASS** | 약 280+ 건 병기, 단독 노출 0건 |
| 8. Phase 6 Coder 규칙 5: Report 감사 | **PASS** | Read 10·Grep 4·ES curl 22 호출 목록 기록 |
| 9. Phase 6 Coder 규칙 6: 배치 크기 1연도×1과목 | **PASS** | 2022-A 단일 과목만 처리 |

## 특이 사항 (재출제 패턴 누적)

- **`jinul`(지눌)의 3연도 연속 재출제** (2020-A Q1 → 2021-B Q1 을 → 2022-A Q2): 한국 불교 최빈도 출제 인물이 ES 미등록 상태로 3연도 누적 — TASK-176 최최우선.
- **`turiel`(튜리엘)의 3연도 연속 재출제** (2018-B Q10 → 2021-B Q3 갑 → 2022-A Q8 을): 도덕 발달 심리학 단골 출제 인물이 ES 미등록 상태로 3연도 누적 — TASK-176 최최우선.
- **`pettit`(페팃)의 재출제** (2020-A Q10 → 2022-A Q6 가): 2연도 출제.
- **Q3 미국 공화주의(삼권분립·탄핵)**: 특정 사상가 지명 없는 **제도론·교과교육학** 분류로 observation 처리 (ES 조회 대상 아님).
- **Q11 을 — 특정 사상가 지명 없음**: "수정된 응보의 원리"는 헤겔적이지만 원문이 사상가를 지명하지 않아 **입장 기술**로 처리. 갑(칸트), 병(베카리아)만 사상가 귀속.
- **Q1 (나) 덕 윤리**: 특정 사상가가 아닌 **덕 윤리 일반 개념**(앤스콤·매킨타이어 전통)으로 처리 — 개념형 분류.
- **Q12 (가) 2015 개정 교육과정**: 교과교육학 observation (ES 조회 대상 아님), (나)만 길리간 사상가형.

## 다음 태스크 제언

- **TASK-175E-2022-B**: 2022학년도 전공 B (아직 미착수)
- **TASK-176 ES 등록 우선순위 갱신**: `jinul` + `turiel` → 최최우선 (3연도 연속 재출제 확인), `pettit` → 최우선 (2연도), `green_th`·`shenxiu`·`zhiyi`·`beccaria` → 최우선 (신규 정전)
