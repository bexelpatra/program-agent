---
agent: coder
task_id: TASK-175E-2025-A
status: DONE
timestamp: 2026-04-21T00:00:00
---

## 결과 요약

2025학년도 중등교사 임용 도덕·윤리 전공 A 시험지(12문항 40점 = 2점×4 기입형 + 4점×8 서술형)에 대한 coverage 맵을 `projects/ethics-study/exam-solutions/coverage/2025-A.md`에 신규 작성했다. Phase 6 대전제(추론 금지·원문 직독 3단계 확정·trademark 3중 일치·창작 금지·한자·한글 병기·동명이인 suffix 규약·v2-rejected 참조 금지·재출제 연속성 grep 실증)를 준수했으며, 전체 12문항에 대해 ① 원문 직접 인용, ② 확정 분석(사상가·학파·주제·한자 병기·확정 근거 4항목), ③ row-by-row 표, ④ ES 실존 여부 섹션을 모두 기입했다.

ES dump 후 전수 교차 대조를 수행해 **본 coverage 등장 thinker_id 중 11인 HIT / 3인 MISS** 를 확정했다 (TASK-175E-2025-A-FIX 정정 후 — 초기 Coder 판정은 9인 HIT / 4인 MISS였으나 `rest` MISS 오분류 정정으로 11인 HIT / 3인 MISS). 원문 trademark 키워드 grep 검증(F-literal)은 전 항목 통과했다(한자 병기 형식 고려). ES MISS 사상가(`durkheim`·`hoffman`·`zhiyi` 3건 — 모두 기출 이력 보유)에 대해 `BLK-175E-2025A-001·-002·-004`를 `signal/ethics-study/blocker-log.md`에 append했다. BLK-175E-2025A-003(`rest` MISS)은 FIX에서 false-positive 철회.

배점 검산: 2점×4(Q1~Q4 기입형) + 4점×8(Q5~Q12 서술형) = **40점** (원문 L7 "12문항 40점" 일치).

## 현 세션 내 실제 Read 호출 목록 (Phase 6 Coder 규칙 5항)

| 파일 | offset | limit | 용도 |
|------|--------|-------|------|
| `/home/jai/program-agent/agents/coder.md` | 전체 | — | Coder 역할 지침 |
| `/home/jai/잡동사니/임용/md/2025_중등1차_도덕·윤리_전공A.md` | 1 | 224 | 원문 직독 (Q1~Q12 전수 커버, 파일명 중간점 주의) |
| `/home/jai/잡동사니/임용/md/2025_중등1차_도덕·윤리_전공A.md` | 61 | 90 | Q5~Q8 재확인 (blocker trademark 인용 검증) |
| `/home/jai/program-agent/signal/ethics-study/architecture.md` | 485 | 104 | Phase 6 Coder 규칙(L523-588) + suffix 규약(L491) |
| `/home/jai/program-agent/projects/ethics-study/exam-solutions/coverage/2024-B.md` | 1 | 200 | 선례 형식 참조 (Q1~Q5 구간 + 요약 테이블 · 블로커 섹션) |
| `/home/jai/program-agent/projects/ethics-study/exam-solutions/coverage/2024-B.md` | 440 | 152 | 선례 형식 참조 (파일 후반부 — 블로커 등록 내역·자체 검증 증거) |
| `/home/jai/program-agent/projects/ethics-study/exam-solutions/coverage/2024-A.md` | 1 | 70 | 선례 형식 참조 (2024-A FIX 완료판) |
| `/home/jai/program-agent/signal/ethics-study/blocker-log.md` | 820 | 130 | BLK-175E-2024A-005(fazang) + BLK-175E-2024B-001~006(turiel·durkheim·blasi·bandura·singer·regan) 선례 구조 참조 |
| `/home/jai/program-agent/signal/ethics-study/blocker-log.md` | 900 | 46 | append 지점 확인 (L945 → L978) |
| `/home/jai/program-agent/signal/ethics-study/coder-report-TASK-175E-2024-B.md` | 전체 | — | 보고서 형식 참조 |

ES 조회: `curl -s "localhost:9200/ethics-thinkers/_search?size=100&_source=id,name_en" | jq -r '.hits.hits[]._source | [.id, .name_en] | @tsv' | sort` 로 전수 dump 확보 후 교차 대조(단일 `match` 쿼리 사용 금지 규칙 준수).

Grep 검증(재출제 연속성 grep 실증 규칙 — TASK-175E-2025-A-FIX 재조사 반영):
- `grep -l '\`durkheim\`' coverage/*.md | sort` → 2021-B·2022-B·2023-A·2023-B·2024-A·2024-B (coverage row 기준 thinker_id 컬럼 등장: 2015-B·2021-B·2022-B·2024-B → 2025-A 추가로 **5회 출제, 2024-B→2025-A 2연속**)
- `grep -E "^\| Q[0-9]+" coverage/*.md | grep hoffman` → row-by-row thinker_id 컬럼 기준: **4회 (2016-A·2019-B·2022-B·2025-A)** — 초기 Coder 주장 "3회 (2019-B·2021-A·2025-A)"는 2016-A·2022-B 누락 + 2021-A 부가 언급 오분류로 잘못된 집계였으며, TASK-175E-2025-A-FIX에서 정정. 2021-A·2021-B·2023-A·2023-B·2024-A·2024-B는 backtick 파일 매치만 있고 본문 사상가 row 등록 없음.
- `grep -E "^\| Q[0-9]+" coverage/*.md | grep rest` → row 기준 2015-B·2016-A·2019-B·2020-A·2021-B·2022-B·2023-A·2025-A = **8회 출제, ES HIT** (TASK-175E-2025-A-FIX에서 MISS→HIT 정정; ES `ethics-thinkers`에 `James Rest`로 등록·`ethics-claims` 10건 확인).
- `grep -l '\`zhiyi\`' coverage/*.md | sort` → row 기준 2022-A·2022-B (+ 2025-A 본 태스크 추가 = 3회, 2022-A·2022-B 2연속 후 4년 단절 재등장).

## 변경된 파일

- **신규**: `projects/ethics-study/exam-solutions/coverage/2025-A.md` (~680행)
- **수정(append)**: `signal/ethics-study/blocker-log.md` (L946 → L978, +33행 / 4건 블로커 엔트리)

## 문항별 thinker_id 확정 결과 (12문항 전수)

| Q | 라인 | 배점 | 분류 | thinker_id (확정) | ES | 핵심 개념 |
|---|------|------|------|-----|----|------|
| Q1 | L16 | 2 | 교과교육학 | [2022 개정 도덕과 교육과정] | N/A | 융합 선택 과목 / 프로젝트 수업 |
| Q2 | L30 | 2 | 사상가형 | 갑 `laozi` + 을 `zhuangzi` | HIT / HIT | 무위자연(無爲自然) / 심재(心齋) |
| Q3 | L41 | 2 | 교과교육학 | [응용윤리 방법론] | N/A | 결의론(決疑論) / 원리의 횡포 |
| Q4 | L49 | 2 | 교과교육학 | [통일교육 — 7·4 공동성명·남북기본합의서·남북공동선언] | N/A | 민족대단결 / 통일헌법 |
| Q5 | L61 | 4 | 교과교육학+사상가 | (가) [직소 I] + (나) `durkheim` | N/A / **MISS** | 직소 I 협동학습 / 도덕성 3요소(규율 정신·집단 애착·자율성) |
| Q6 | L89 | 4 | 사상가형 | 갑 `hoffman` + 을 `rest` | **MISS** / HIT | 공감 이론·공감적 염려·역할 채택 / 4-구성요소 모형·도덕적 민감성 (FIX: `rest` HIT 정정) |
| Q7 | L119 | 4 | 사상가형 | 갑 `confucius` + 을 `jeongyagyong` | HIT / HIT | 인(仁)·종심소욕불유구(從心所欲不踰矩) / 상제(上帝)·신독(愼獨) 재해석·권형(權衡)·성기호설(性嗜好說) |
| Q8 | L136 | 4 | 사상가형 | `zhiyi` (천태 지의) | **MISS** | 삼제원융(三諦圓融)·일심삼관(一心三觀)·오시팔교(五時八敎) — 화법 4교·화의 4교 |
| Q9 | L152 | 4 | 사상가형 | `aristotle` | HIT | 숙고(boulēsis)·합리적 선택(proairesis)·실천적 지혜(phronēsis)·기예(technē) 구분 |
| Q10 | L170 | 4 | 사상가형 | 갑 `epicurus` + 을 `epictetus` | HIT / HIT | 운명 비판·원자론 / 견해(hypolēpsis)·비난의 3단계 |
| Q11 | L187 | 4 | 사상가형 | `rawls` | HIT | 박애(fraternity)-차등 원칙(difference principle) / 시민 불복종(civil disobedience) 정의·정당화 |
| Q12 | L207 | 4 | 사상가형 | 갑 `nozick` + 을 `walzer` | HIT / HIT | 소유 권리 3원칙(획득·이전·교정) / 단순 평등·자유 교환·복합 평등(sphere of justice) |

### 한자문화권 thinker_id (언더바 없음, canonical)
- `laozi` (Q2 갑), `zhuangzi` (Q2 을)
- `confucius` (Q7 갑), `jeongyagyong` (Q7 을)
- `zhiyi` (Q8) — **MISS**

### 서양 thinker_id (suffix 규약 architecture.md L491 준수)
- `durkheim`(MISS), `hoffman`(MISS), `rest`(HIT — FIX 정정), `aristotle`, `epicurus`, `epictetus`, `rawls`, `nozick`, `walzer`
- 동명이인 검토: Q12 (을) `walzer` = Michael Walzer (정의의 영역·복합 평등) — **2024-B Q2 출제 선례와 동일 id**. 동명이인 회피 suffix 불필요(architecture.md L491 기준).

## 재출제 경계 갱신 결과 (grep 실증 기반)

2025-A 반영 — Phase 6 Coder 규칙 8항(재출제 연속성 grep 실증) 엄수:

| 사상가 | 기존 | 2025-A 결과 | 갱신 후 (row 기준) | ES | 비고 |
|--------|------|-------------|--------|----|------|
| `durkheim` | 2024-B BLK-175E-2024B-002 4회 출제 | **Q5 (나) 재출제** | **총 5회 출제 (2015-B·2021-B·2022-B·2024-B·2025-A), 2024-B→2025-A 2연속** | **MISS** | BLK-175E-2025A-001, **최상위** 등록 대상 |
| `hoffman` | 2016-A·2019-B·2022-B row 등장 | **Q6 (갑) 재출제** | **row-by-row thinker_id 컬럼 기준 총 4회 출제 (2016-A·2019-B·2022-B·2025-A — TASK-175E-2025-A-FIX `grep -E "^\| Q[0-9]+"` 재조사 실증)** | **MISS** | BLK-175E-2025A-002 |
| `rest` | 2015-B·2016-A·2019-B·2020-A·2021-B·2022-B·2023-A row 등장 | **Q6 (을) 재출제** | **row 기준 총 8회 출제 (2015-B·2016-A·2019-B·2020-A·2021-B·2022-B·2023-A·2025-A) — ES HIT 사상가 중 상위권 재출제** | HIT | BLK-175E-2025A-003 철회 (FIX false-positive); `rest`는 ES 등록·claim 10건 확인 |
| `zhiyi` | 2022-A·2022-B row 등장 | **Q8 재출제** | **row 기준 총 3회 출제 (2022-A·2022-B·2025-A), 2022-A·2022-B 2연속 후 4년 단절 재등장** | **MISS** | BLK-175E-2025A-004, 중국 천태종 |
| `confucius` | 동양 고전 상시 출제 | **Q7 (갑) 단일 등장** | 상시 출제군 | HIT | 인·종심소욕불유구 |
| `jeongyagyong` | 한국 실학 상시 출제 | **Q7 (을) 단일 등장** | 상시 출제군 | HIT | 상제·신독 재해석·권형·성기호 |
| `laozi`/`zhuangzi` | 도가 상시 출제 | **Q2 동반 등장** | 상시 출제군 | HIT | 무위자연 / 심재 |
| `aristotle` | 상시 출제군 | **Q9 단일 등장** | 상시 출제군 | HIT | 숙고·합리적 선택·실천적 지혜·기예 |
| `epicurus`/`epictetus` | 헬레니즘 — 2014-A·2017-B 이래 단발 재출제 | **Q10 동반 등장** | 헬레니즘 에피쿠로스–스토아 대립 출제 확장 | HIT / HIT | 운명 비판·원자 / 견해·비난 3단계 |
| `rawls` | 상시 출제군 | **Q11 단일 등장** | 차등 원칙·시민 불복종 동시 trademark | HIT | 2024-B 이어 연속 출제 — 임용시험 최빈출 사상가 확증 |
| `nozick`/`walzer` | 분배 정의 대립 출제군 | **Q12 동반 등장** | 자격 이론 vs 복합 평등 대립 출제 확장 | HIT / HIT | 2024-B Q2 walzer 등장 이후 연속 출제 |

**핵심 관찰 (2024-B 대비 2025-A의 특이 패턴)**:

1. **`durkheim` 2024-B→2025-A 2연속 재출제** — ES 미등록 사상가 중 최초의 연속 재출제 확증 사례. BLK-175E-2024B-002 등록 직후 후속 재출제로, TASK-176에서 `durkheim` 등록 긴급 우선 처리 필요.
2. **`rest`는 ES HIT (FIX 정정)** — 초기 Coder 판정의 `rest` MISS는 오분류였으며, ES `ethics-thinkers`에 `James Rest`로 등록·`ethics-claims` 10건 확인으로 명백한 HIT임이 TASK-175E-2025-A-FIX에서 확증되었다. `blasi` 5회가 ES 미등록 사상가 최다 기록으로 복원.
3. **중국 불교 3대 종파 대표자 동시 ES 공백 패턴 재확증** — 2024-A Q8 BLK-175E-2024A-005(`fazang`, 화엄종)에 이어 2025-A Q8 BLK-175E-2025A-004(`zhiyi`, 천태종). 중국 불교 종학(宗學) 체계화 정점 인물들의 구조적 부재.
4. **사상가 ES MISS 3인(`durkheim`·`hoffman`·`zhiyi`) 모두 기출 재출제 확증** — 2024-B에 이어 2025-A에서도 ES MISS = 기출 재출제 보유 패턴 연속, 재출제 경계 리스트의 ES 커버리지 반영 필요성 명확. (FIX 정정 후 4인 → 3인)
5. **교과교육학 문항 비중 확대** — Q1·Q3·Q4 3문항이 순수 교과교육학(사상가 trademark 아님), Q5도 교과교육학+사상가 혼합. 2024-B는 Q1~Q11 전원 사상가형. **2025-A는 교과교육학 문항 4개 증가**로 문항 구성 전환 가능성.

## 이슈/블로커

### ES 미등록 사상가 3건 (BLK-175E-2025A-001·-002·-004) — blocker-log.md append 완료 / TASK-175E-2025-A-FIX 후 최종

1. **BLK-175E-2025A-001**: `durkheim` (Émile Durkheim, 사회학적 도덕교육·도덕성 3요소) — Q5 — **5회째 출제, 2024-B→2025-A 2연속** (2015-B·2021-B·2022-B·2024-B·2025-A) — **최상위 우선**
2. **BLK-175E-2025A-002**: `hoffman` (Martin L. Hoffman, 공감 이론·공감적 염려·역할 채택) — Q6 (갑) — **row-by-row thinker_id 컬럼 기준 4회째** (2016-A·2019-B·2022-B·2025-A — TASK-175E-2025-A-FIX `grep -E "^\| Q[0-9]+"` 재조사 실증) — 최우선
3. ~~**BLK-175E-2025A-003**: `rest`~~ → **철회 (FALSE-POSITIVE, TASK-175E-2025-A-FIX)**. `rest`는 ES HIT (`ethics-thinkers`에 `James Rest` 등록 + `ethics-claims` 10건). 초기 Coder의 MISS 판정은 오분류였다. blocker-log.md에서 엔트리 삭제·철회 표기.
4. **BLK-175E-2025A-004**: `zhiyi` (天台 智顗, 중국 천태종·삼제원융·일심삼관·오시팔교) — Q8 — **row 기준 3회째** (2022-A·2022-B·2025-A; 2022-A·2022-B 2연속 후 4년 단절 재등장) — 최우선

모든 사상가(MISS 3인)는 coverage 본문에서 정답 서술·trademark 3중 일치로 확정되어 있으며, ES 커버리지 공백만 존재한다.

### 기타 관찰

- **Q5 ㉠ (직소 I 중간 절차)** — 원문 "**홈팀, ( ㉠ ), 전문가팀**" + (나) 표 "( ㉠ ) · 도덕성 3요소 탐구를 위한 개인별 소주제 선택"에서 ㉠ 명칭은 **개인별 소주제/학습 자료 분담(선택) 단계**에 해당한다. 직소 I 모형(Aronson, 1978)의 표준 절차 명칭은 교과서별로 "전문가 주제 분담"·"학습 자료 분담"·"소주제 선택" 등으로 다양하게 표기될 수 있으며, Phase 6 창작 금지 원칙상 단일 명칭 확정 없이 **개인별 소주제/학습 자료 분담 선택**으로 병기. 본 표기가 교과서 표준과 일치하지 않을 경우 Tester 검증 단계에서 정정 필요 — coverage 본문 내 HTML 주석 형식 블로커 마크 삽입. 교과서 표준 명칭 확인 필요 포인트.
- **Q1 ㉠ (새 교육과정 선택 과목 유형)** — 2022 개정 도덕과 교육과정상 "선택 과목 중 ( ㉠ ) 과목"은 **융합 선택**에 해당한다(일반 선택·진로 선택·융합 선택 3유형 중). 본 coverage는 "융합 선택"으로 확정. 교과교육학 전문 조문 인용 여부는 Tester에서 재확인 가능.
- **Q7 갑·을** — 갑은 **공자(孔子)** 자명(종심소욕불유구 = 공자 자서전 『논어』 「위정편」 trademark), 을은 **정약용(丁若鏞)** 명백 확증(상제·신독 재해석·권형·성기호설 4중 trademark — 『중용자잠』·『심경밀험』·『여유당전서』). 양자 HIT, 블로커 없음.
- **Q12 갑·을** — 갑 노직(Robert Nozick), 을 왈저(Michael Walzer) 명백 확증. 양자 HIT. 2024-B Q2 (을) `walzer` 등장 후 연속 출제 — 현대 정의론 다원주의 입장의 상시 출제군 확증.

## 다음 제안

1. **Tester 검증**: 2025-A.md에 대해 Phase 6 Tester 규칙(직접 풀이 대조 / 3중 일치 / grep 0건 / row-by-row 전수)에 따라 검증. 특히 다음 포인트를 우선 검토할 것:
   - Q5 ㉠ = "개인별 소주제/학습 자료 분담 선택" 단계의 교과서 표준 명칭 — "전문가 주제 분담" / "주제별 분담" / "학습 자료 분담" / "소주제 선택" 중 표준 표현 확인 (본 coverage는 HTML 주석 BLOCKER 마크 포함).
   - Q1 ㉡ = **프로젝트 수업**의 교과교육학 교과서 표준 정답 여부 (2022 개정 도덕과 교육과정 교수·학습 방법 조문 직접 확인 필요).
   - Q5 <작성 방법> 3항 "뒤르켐 입장에서 ㉢(자율성) 도덕 행동 특징을 '사회의 도덕규범' 사용" — 본 coverage 답안 "사회의 도덕규범을 과학적·합리적으로 이해한 바탕에서 자발적으로 실천한다"의 교과서 표준 표현 재확인.

2. **TASK-176 우선 등록 대상 (TASK-175E-2025-A-FIX 정정 후)**:
   - **최상위(5회·2연속)**: `durkheim` (2015-B·2021-B·2022-B·2024-B·2025-A — 2024-B→2025-A 연속 재출제 확증) — 유일한 ES 미등록 연속 재출제 사례
   - **최우선(3~5회)**: `blasi` 5회(BLK-175E-2024B-003, ES 미등록 최다 기록 복원), `turiel`·`bandura`·`singer` 4회, `hoffman` 4회(FIX 정정)·`zhiyi` 3회
   - **중국 불교 3대 종파 일괄 등록 권고**: `zhiyi`(천태) + `fazang`(화엄, BLK-175E-2024A-005) + `huineng`(선종, ES HIT 여부 재확인) 일괄 검토
   - 기존 BLK-175E-2024A-002(`narvaez`), BLK-175E-2024A-005(`fazang`), BLK-175E-2024B-001~006(`turiel`·`durkheim`·`blasi`·`bandura`·`singer`·`regan`), BLK-175E-2025A-001·-002·-004(`durkheim`·`hoffman`·`zhiyi`) 일괄 TASK-176 등록 범위 (FIX 정정: BLK-175E-2025A-003 `rest`는 제외 — HIT 확증)

3. **다음 coverage 태스크**: 2025-A 완료 후 시간순으로 **2025-B** 또는 **미확보 연도**로 진행 (Phase 6 Coder 규칙 6항: 1회 호출 = 1연도 × 1과목). Manager 판단. 기출 보유 원본 파일 `/home/jai/잡동사니/임용/md/` 범위 재확인 필요.

4. **2024-B 요약 vs row 기준 `hoffman` 집계 불일치 — TASK-175E-2025-A-FIX에서 해소**: `grep -E "^\| Q[0-9]+" coverage/*.md | grep hoffman` 재조사 결과 hoffman row-by-row thinker_id 컬럼 기준 정확 누적은 **4회 (2016-A·2019-B·2022-B·2025-A)**로 확정. 2024-B 요약의 "4연속(2016-A/2019-B/2021-B/2022-B)" 표기는 2021-B가 본문 row가 아닌 언급 포함이었기 때문으로, FIX에서 2021-B를 제외하고 2022-B를 포함한 정확 4회로 정정. 초기 Coder 주장 "3회 (2019-B·2021-A·2025-A)"도 오분류였다 (2016-A·2022-B 누락 + 2021-A 부가 언급을 row로 오분류).
