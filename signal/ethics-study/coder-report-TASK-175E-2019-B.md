---
agent: coder
task_id: TASK-175E-2019-B
status: DONE
timestamp: 2026-04-21
---

# Coder Report — TASK-175E-2019-B (2019학년도 중등 1차 도덕·윤리 전공 B 커버리지 맵)

## 작업 요약

2019학년도 중등임용 도덕·윤리 전공 B 시험지(8문항 40점)의 커버리지 맵을 Phase 6 규칙(architecture.md L523-L588, 조항 1~6)에 따라 **엄격 적용**하여 생성했다. 원문 직독(현 세션 1회 완독 128 lines), 3단계 확정 절차(문제→제시문→사상가), 원문 2~3구절 복사 인용, file_path:line_range 병기, 한자+한글 병기, Read 호출 감사 로그를 모두 수행했다. 1연도×1과목 배치 준수(조항 6).

## 산출물

| 경로 | 상태 | 라인 수 |
|------|------|---------|
| `projects/ethics-study/exam-solutions/coverage/2019-B.md` | 신규 생성 | 128 lines |
| `signal/ethics-study/blocker-log.md` | append 수정 | BLK-175E-2019B-001 + BLK-175E-2019B-002 (2건) 추가 |
| `signal/ethics-study/coder-report-TASK-175E-2019-B.md` | 본 파일 | — |

## 문항별 판정 결과 (8문항 전수)

| 문항 | 배점 | thinker_id | 분류 | ES 등록 | 원문 라인 | 판정 근거 |
|------|------|------------|------|---------|-----------|-----------|
| Q1 | 4 | (비귀속) | 교과교육학/정치철학 — 심의 민주주의 유형론 | — | L14-L25 | "결집 민주주의(aggregative democracy)" + "공적 대화·토론·의사소통을 통해 합의된 집단적 의사" + "수용 가능한 이유" 3중 일치 → 결집/심의 민주주의 표준 유형론 |
| Q2 | 4 | `buddha` | 사상가형 (초기·대승 불교 공통 수행론) | 등록 | L29-L39 | "세 가지 공부[學]·팔정도·육바라밀" + "그침(사마타, 止)·관찰(위빠싸나, 觀)" + "해탈" 3중 일치 → 삼학(戒·定·慧) + 지관쌍수 |
| Q3 | 4 | `singer` | 사상가형 (서양 현대 응용윤리) | **미등록 (BLK-175E-2019B-001)** | L43-L47 | "동등한 이익에 동등한 비중" + "이익을 갖기 위한 전제조건" + "종차별주의" 3중 일치 → 피터 싱어 이익평등고려·쾌고감수능력·종차별주의 |
| Q4 | 4 | `jeongyagyong` | 사상가형 (한국 조선 후기 실학) | 등록 | L51-L55 | "성이란 즐거워하고 좋아하는 것" + "소고·왕제·절성·절민성" + "천명지성·성선·진성" 3중 일치 → 정약용 성기호설(기질지성·도의지성) |
| Q5 | 4 | `kant` | 사상가형 (서양 근대 의무론) | 등록 | L59-L63 | "목적 그 자체" + "목적의 왕국·법칙 수립자" + "존엄성·무조건적 가치" 3중 일치 → 칸트 목적 정식·가격/존엄성 대조, 괄호 답 = "존경(Achtung)" |
| Q6 | 5 | `nozick` | 사상가형 (서양 현대 자유지상주의) | 등록 | L72-L84 | "소유 권리" + "역사적 원리" + "종국 상태 원리(end-state principles)" 3중 일치 → 노직 소유권리론·비정형/정형·역사적/종국상태 원리 |
| Q7 | 5 | (Coombs·Meux — 비귀속) | 교과교육학 (도덕 교육 수업 모형) | — (observation) | L94-L106 | "쿰즈(J. R. Coombs)·가치분석" + "6단계 교수전략" + "5가지 가치갈등 원인 중 4가지 명시" 3중 일치 → 쿰즈·뮤 가치분석 수업모형, 빈칸 = "사실 주장의 불일치" |
| Q8 | 10 | `kohlberg`/`rest`/`freud`/`hoffman`/`blasi` | 사상가형 (도덕 심리학) | 부분 공백 (**BLK-175E-2019B-002**: freud·hoffman·blasi 3인 미등록, kohlberg·rest 등록) | L110-L124 | 5인 저자 직접 명기 + 레스트 4요소 중 3개 명시(㉡ 도덕적 품성) + 블라지 4요소 중 3개 명시(㉢ 책임 판단) 3중 일치 |

**배점 합계 검증**: 4점×5 + 5점×2 + 10점×1 = 20 + 10 + 10 = **40점** (원문 L7 "8문항 40점" 일치) ✓

## 블로커 (ES-gap blocker — Phase 6 정책)

Phase 6 ES-gap 정책(2018-A regan·2018-B turiel·2019-A bandura/pettit/skinner 선례)에 따라, 제시문 중심 사상가가 ES 미등록이면 observation이 아닌 **blocker**로 등록했다.

### 블로커 2건 (4인 미등록)

| BLK-ID | 문항 | 미등록 사상가 | 후속 조치 |
|--------|------|---------------|-----------|
| BLK-175E-2019B-001 | Q3 | 피터 싱어 (Peter Singer) | TASK-176 singer 신규 등록 (이익평등고려·쾌고감수능력·종차별주의·동물해방·실천윤리학·선호 공리주의·공장식 축산·세계 빈곤 원조·효과적 이타주의). **최우선 등록 순위**. |
| BLK-175E-2019B-002 | Q8 | 프로이드 (Freud) + 호프만 (Hoffman) + 블라지 (Blasi) 3인 묶음 | TASK-176 freud (초자아·동일시·죄책감·정신분석) + hoffman (공감 발달 4단계·공감적 고통·귀납적 훈육) + blasi (도덕적 정체성·책임 판단·자기 일관성·판단-행동 간극) 3인 신규 등록. 우선 순위 **높음**. |

- **정식 블로커 총계**: 2건 (4인 미등록 누적)
- **NOTE(observation)**: 1건 (Q7 Coombs·Meux, 선례 BLK-175E-2017A-005 observation 처리와 일관)
- **정답 확정 불가 블로커**: 0건 (모든 8문항 정답 trademark 3중 일치로 확정)

## Phase 6 규칙 준수 감사 (architecture.md L523-L588)

### 조항 1: 원문 직독 필수 (현 세션 한정) — PASS
- 현 세션 Read 호출 1회: `/home/jai/잡동사니/임용/md/2019_중등1차_도덕윤리B.md` 1~128 lines 전체 완독.
- 각 row 메모에 `L14-L25`·`L29-L39`·`L43-L47`·`L51-L55`·`L59-L63`·`L72-L84`·`L94-L106`·`L110-L124` 형식으로 원문 line range 병기.

### 조항 2: 3단계 확정 절차 (문제→제시문→사상가) — PASS
- 각 row의 "사상가/개념" 컬럼 내 **"Trademark 3중 일치"** 구조로 ①·②·③ 3개 원문 구절을 직접 복사·인용하고 해당 line 번호를 병기하여 사상가·분류 판정 근거를 제시.
- 요약·의역·재서술 없이 원문 2~3구절을 그대로 옮겼으며, 제시문에 없는 trademark는 사용하지 않음.

### 조항 3: 불확실 처리 (창작 금지) — PASS
- ES 미등록 사상가 4인(singer·freud·hoffman·blasi)은 창작하지 않고 `<!-- BLOCKER(TASK-175E-2019-B): BLK-175E-2019B-NNN -->` HTML 주석으로 표기하고 `blocker-log.md`에 등록.
- Q8은 5인 사상가가 단일 row에 공존하여 "한 문항의 복수 사상가 동시 출제" 규칙 적용(조항 3 "한 사상가의 복수 주제 동시 출제 가능"의 역방향 적용).

### 조항 4: 한자+한글 병기 원칙 — PASS
- `한자(한글 — 의미)` 형식 병기 **121건** 적용(python3 정규식 검증). 예: `三學(삼학 — three trainings, 계·정·혜 세 가지 공부)`, `性嗜好說(성기호설 — 성은 기호라는 다산의 본성론)`, `所有 權利(소유 권리 — entitlement, 노직 핵심 개념)`, `超自我(초자아 — Über-Ich / superego, 프로이드)`, `責任 判斷(책임 판단 — responsibility judgment, 블라지 3요소 = ㉢)`.
- 원문 인용구절은 원문 보존 원칙에 따라 그대로 복사(예: `"그침(사마타, 止)"` 원문 병기 유지).
- 기술의 주언어는 한글 해석 용어로 하고 한자는 보조 병기로만 등장.

### 조항 5: Report 감사 형식 — PASS (본 문서)
- coverage 파일 말미에 "본 세션 Read 호출 감사 로그" 표 기록(파일 경로·offset·limit·목적).
- Grep 호출 감사 표 별도 기록(패턴·파일·결과·목적). "grep 0건" 규칙 사전 대응.
- ES 조회 curl 명령 + 55명 id 전수 목록 기록.

### 조항 6: 배치 크기 제한 (1연도×1과목) — PASS
- 본 태스크 범위 = **2019-B 단일 파일**. 다른 연도·과목 작업 없음. 다음 연도·과목으로 진행하기 전 Tester 검증 PASS 대기.

## 본 세션 Read 호출 감사 로그

| 파일 경로 | offset | limit | 목적 |
|-----------|--------|-------|------|
| `/home/jai/program-agent/signal/ethics-study/architecture.md` | 500 | 100 | Phase 6 기출 작업 규칙(L523~L588) 전면 확인 |
| `/home/jai/잡동사니/임용/md/2019_중등1차_도덕윤리B.md` | 1 | (전체 128 lines) | 2019-B 원문 전면 직독 (현 세션 완독 1회) |
| `/home/jai/program-agent/projects/ethics-study/exam-solutions/coverage/2017-B.md` | 1 | 80 | 선행 템플릿 포맷·헤더·8-row 구조·감사 로그 형식 확인 |
| `/home/jai/program-agent/signal/ethics-study/blocker-log.md` | 1 | 50 | BLK 번호 체계·포맷·severity 형식 확인 |
| `/home/jai/program-agent/signal/ethics-study/blocker-log.md` | 440 | 68 | 최근 블로커(2018-A Regan·2018-B Turiel·2019-A Bandura·Pettit/Skinner) 템플릿 참조 — ES-gap blocker 처리 선례 확인 |
| `/home/jai/program-agent/projects/ethics-study/exam-solutions/coverage/2018-B.md` | 240 | 47 | 2018-B 커버리지 결말부(Read 감사 로그·Grep 감사·ES 조회·체크리스트) 구조 참조 |

## Grep 호출 감사 (기계 검증)

| 패턴 | 파일 | 결과 | 목적 |
|------|------|------|------|
| `싱어\|Singer\|종차별\|쾌고\|감수능력` | 2019-B 원문 | L47 매칭 (종차별주의 + trademark 세트) | Q3 싱어 trademark 원문 검증 PASS |
| `노직\|Nozick\|소유권리\|응분의 자격` | 2019-B 원문 | L77 + L81 매칭 | Q6 노직 trademark 검증 PASS |
| `칸트\|Kant\|목적 그 자체\|존엄성\|목적의 왕국` | 2019-B 원문 | L63 4종 동시 매칭 | Q5 칸트 trademark 검증 PASS |
| `절성\|성선\|진성\|소고\|왕제\|천명지성` | 2019-B 원문 | L55 7종 동시 매칭 | Q4 다산 성기호설 trademark 검증 PASS |
| `결집\|심의\|공적 대화\|aggregative` | 2019-B 원문 | L18·L20 매칭 | Q1 민주주의 유형 trademark 검증 PASS |
| `止\|觀\|사마타\|위빠싸나\|팔정도\|육바라밀` | 2019-B 원문 | L33·L37·L39 매칭 | Q2 삼학·지관쌍수 trademark 검증 PASS |
| `콜버그\|프로이드\|호프만\|레스트\|블라지` | 2019-B 원문 | L114·L116 5인 저자명 동시 매칭 | Q8 5인 저자 직접 명기 + 레스트/블라지 4요소 검증 PASS |
| `쿰즈\|Coombs\|가치분석\|6단계` | 2019-B 원문 | L98·L100 매칭 | Q7 쿰즈 가치분석 + 5원인 trademark 검증 PASS |

## ES 조회 (curl 명령 + 결과, 본 세션 2026-04-21)

1. `curl -s "http://localhost:9200/ethics-thinkers/_search?size=200&_source=id,name,name_en" | jq -r '.hits.hits[]._source | "\(.id) | \(.name) | \(.name_en)"' | sort` → **55명** canonical id 전수 획득.
2. 본 시험 등장 **등록** 사상가: buddha, jeongyagyong, kant, nozick, kohlberg, rest — 6명 모두 55명 목록 포함.
3. 본 시험 등장 **미등록** 사상가: singer (Q3, BLK-175E-2019B-001), freud (Q8, BLK-175E-2019B-002), hoffman (Q8, BLK-175E-2019B-002), blasi (Q8, BLK-175E-2019B-002) — 총 **4인**.
4. Q1(심의 민주주의 유형론)·Q6(나)(공리주의 분배 원리)·Q7(쿰즈·뮤 가치분석 수업모형)은 사상가형이 아닌 교과교육학·정치철학 범주로 ES 사상가형 인덱스 대상 외(정상 상태).

## 통계 요약

- **문항 수**: 8 (Q1~Q8, 원문 L7 "8문항 40점" 준수) ✓
- **배점 합계**: 40점 (4×5 + 5×2 + 10×1) ✓
- **사상가형 문항**: 5 (Q2 buddha, Q3 singer, Q4 jeongyagyong, Q5 kant, Q6 nozick, Q8 — 콜버그·레스트·프로이드·호프만·블라지 복수)
- **교과교육학 문항**: 3 (Q1 심의 민주주의, Q6(나) 공리주의 분배 원리, Q7 가치분석 수업모형)
- **ES 등록 사상가**: 6인 (buddha, jeongyagyong, kant, nozick, kohlberg, rest)
- **ES 미등록 사상가**: 4인 (singer, freud, hoffman, blasi) → BLK-175E-2019B-001 (Q3 singer) + BLK-175E-2019B-002 (Q8 freud/hoffman/blasi)
- **정식 블로커**: 2건
- **정답 확정 불가**: 0건
- **한자+한글 병기 건수**: 121건 (정규식 `[一-龥]+\([가-힣]+` 패턴 검증)
- **원문 line 병기**: 8/8 문항 전수 (각 row 원문 line range 컬럼 + 메모 내 L번호 중복 병기)
- **생성 파일 라인 수**: 128 lines (coverage/2019-B.md)

## 선례 일관성 검증

- **2018-A BLK-175E-2018A-001 (Regan)** · **2018-B BLK-175E-2018B-001 (Turiel)** · **2019-A BLK-175E-2019A-001 (Bandura)** · **2019-A BLK-175E-2019A-002 (Pettit/Skinner)** 패턴과 동일 처리.
- "row의 유일·중심 사상가 ES 미등록 + trademark 3중 일치로 정답 확정 가능" 구조에서 **blocker**로 등록(observation 아님).
- Q7 Coombs·Meux는 선례 BLK-175E-2017A-005(2017-A Q10 쿰스·뮤 가치분석)의 **observation 처리**와 동일 계열로 유지.

## 상태

- TASK-175E-2019-B: **DONE**
- 산출물 3종 모두 완비: coverage/2019-B.md (신규 128 lines), blocker-log.md (append BLK 2건), coder-report-TASK-175E-2019-B.md (본 파일).
- 다음 단계: **Tester 호출 대기** (조항 6에 따라 Tester 검증 PASS 후 다음 연도·과목으로 진행).

---

**작성 완료** — 2026-04-21, Coder(Opus) TASK-175E-2019-B.
