---
task_id: TASK-175E-MERGE
verdict: NEEDS_REVISION
---

# Reviewer Report: TASK-175E-MERGE

## 검증 대상

- 파일:
  - `projects/ethics-study/exam-solutions/coverage/*.md` (26개)
  - `projects/ethics-study/exam-solutions/exam-coverage-map.v1-rejected.md`
  - `projects/ethics-study/exam-solutions/exam-coverage-map.v2-rejected.md`
  - `signal/ethics-study/architecture.md` (L480-L505 canonical 규약)
  - `signal/ethics-study/blocker-log.md`
  - `signal/ethics-study/task-board.md` L249 (TASK-175E-MERGE)
- Manager 주장 요약:
  1. 26개 coverage 파일(2014-A ~ 2026-B) 존재
  2. 자동 스크립트로 `exam-coverage-map.md` 병합 + Section A~E 재집계
  3. v1/v2 rejected 보존, 신규 파일 생성
  4. BLK-175E-* 총 66건 (주장)

---

## 검증 결과

### 1. 입력 파일 전수성 점검

**26개 전수 존재 PASS**. `ls /home/jai/.../coverage/` 기준:

| 파일 | 존재 | size (bytes) | mtime |
|------|------|------|------|
| 2014-A.md | O | 27,725 | 04-20 16:54 |
| 2014-B.md | O | 17,654 | 04-20 20:01 |
| 2015-A.md | O | 38,693 | 04-20 23:23 |
| 2015-B.md | O | 50,387 | 04-20 23:41 |
| 2016-A.md | O | 86,744 | 04-21 00:12 |
| 2016-B.md | O | 93,701 | 04-21 00:40 |
| 2017-A.md | O | 107,905 | 04-21 01:10 |
| 2017-B.md | O | 67,889 | 04-21 07:31 |
| 2018-A.md | O | 85,857 | 04-21 08:17 |
| 2018-B.md | O | 74,761 | 04-21 09:01 |
| 2019-A.md | O | 112,754 | 04-21 10:01 |
| 2019-B.md | O | 68,802 | 04-21 10:38 |
| 2020-A.md | O | 102,792 | 04-21 11:27 |
| 2020-B.md | O | 92,642 | 04-21 12:14 |
| 2021-A.md | O | 95,075 | 04-21 13:12 |
| 2021-B.md | O | 121,770 | 04-21 13:34 |
| 2022-A.md | O | 73,293 | 04-21 14:25 |
| 2022-B.md | O | 106,174 | 04-21 15:13 |
| 2023-A.md | O | 112,366 | 04-21 16:02 |
| 2023-B.md | O | 109,215 | 04-21 16:51 |
| 2024-A.md | O | 130,016 | 04-21 17:43 |
| 2024-B.md | O | 118,757 | 04-21 19:10 |
| 2025-A.md | O | 138,351 | 04-21 20:23 |
| 2025-B.md | O | 53,985 | 04-21 21:23 |
| 2026-A.md | O | 118,642 | 04-21 22:12 |
| 2026-B.md | O | 132,773 | 04-21 23:09 |

모두 비어있지 않으며, 최소 17KB~최대 138KB 실질 내용 보유. 선행 `TASK-175E-2026-B-T`가 done-log L1398에 PASS로 기록됨.

---

### 2. coverage/*.md 구조 일관성 — **NEEDS_REVISION 핵심 사유**

**구조가 두 세대 + 다중 헤더 배리에이션으로 이원화됨.** Manager 주장("각 파일이 동일 요약 테이블 포맷")과 실제 파일시스템이 불일치.

#### (a) 구형 17개 (2014-A ~ 2022-A): 상단 "커버리지 표" 중심
상단에 `| 문항 | 배점 | ... | thinker_id | ... | ES 커버리지 | ... |` 요약 테이블 1개. 헤더 배리에이션 5종 확인:

| 세트 | 파일 수 | 헤더 패턴 |
|------|---------|-----------|
| A | 9 (2014-A~2017-B, 2019-A/B) | `문항 \| 배점 \| 발문 요지 \| 제시문 핵심(원문 복사) \| 사상가/개념 \| thinker_id \| 분류 \| ES 커버리지 \| 원문 line` (10 pipes) |
| B | 1 (2018-B) | `문항 \| 배점 \| 발문 유형 \| 주요 사상가 \| thinker_id \| 분류 \| 핵심 개념 \| ES 커버리지 \| 메모` (10 pipes) |
| C | 1 (2018-A) | `문항 \| 배점 \| 발문 요지 \| ... (10 pipes)` |
| D | 2 (2020-A, 2020-B) | `문항 \| 배점 \| 유형 \| 발문 유형 \| 주요 사상가 \| thinker_id \| 분류 \| 핵심 개념 \| ES 커버리지 \| 메모` (11 pipes) |
| E | 4 (2021-A~2022-A) | `문항 \| 유형 \| 배점 \| 발문 요지 \| 제시문 핵심 \| 사상가/개념 \| thinker_id \| 분류 \| ES 커버리지 \| 원문 line` (11 pipes) |

#### (b) 신형 9개 (2022-B ~ 2026-B): **상단 요약표 없음**, 문항별 섹션 + 파일 말미에 별도 요약 테이블
Grep 확인: `grep "^| 문항 " 2022-B..2026-B` 전부 NO_STANDARD_HEADER.
- `## Q1 [2점] (Lxx)` 또는 `### Q1 (2점, Lxx-Lyy) — ...` 문항별 섹션 11~12개
- 각 섹션 내부에 `### row-by-row` (표), `### ES 실존 여부` (불릿) 하위 구조
- 파일 말미(L555~L722)에 **별도의 Q별 요약 테이블**:

| 파일 | 말미 요약표 라인 | 헤더 패턴 |
|------|-------|-----------|
| 2022-B | L555 | `Q \| 유형 \| 배점 \| 중심 사상가(thinker_id) \| 출제 개념 \| ES 상태 \| 원문 line` |
| 2023-A, 2023-B, 2024-A, 2024-B, 2025-A | L584~L716 | `Q \| 라인 \| 배점 \| 분류 \| 주요 사상가(thinker_id) \| ES \| 비고` |
| 2025-B, 2026-A | L403~L665 | `Q \| 라인 \| 배점 \| 분류 \| thinker_id(s) \| ES \| 비고` |
| 2026-B | L722 | `Q \| 라인 \| 배점 \| 유형 \| thinker_id \| ES 상태 \| 재출제 연속성 / 비고` |

즉 **헤더 배리에이션 최소 9종(구형 5 + 신형 4)**. 단일 정규식·awk 한 줄로는 파싱 불가능. Python으로 per-file header 자동 감지 → 컬럼 인덱스 dynamic mapping이 필요.

#### (c) thinker_id 셀 내부 포맷 복합성
같은 `thinker_id` 컬럼 내에서도 셀 포맷이 상이:
- 단일: `` `popper` `` 또는 `popper`
- 다중(갑/을): `` `locke`(갑) + `nozick`(을) `` 또는 `` `kohlberg`(갑) + `narvaez`(을) ``
- ES 누락: `(없음/누락)`, `(없음, habermas 부분 관련)`, `(없음, 통일정책사)`
- 교과교육학: `[교과교육학]`, `[메타윤리 개념]`
- 미확정: `특정 불능 (tappan/brown 등 추정)`

정규식 `` `([a-z][a-z0-9_]+)` ``만으로 id 추출 가능하나, 교과교육학/경계영역/누락 셀은 별도 플래그 필요. ES HIT/MISS 추출도 파일별 컬럼 이름이 `ES 커버리지` / `ES 상태` / `ES`로 달라 정규화 필요.

---

### 3. canonical id 일관성

- architecture.md L480-L505에 정규화 규칙 확인: `taylor` (Charles Taylor) vs `taylor_p` (Paul Taylor) 구분, `mill_js` 이니셜 suffix 등.
- ES 조회(`curl http://localhost:9200/ethics-thinkers/_count`) **55명 존재 PASS**.
- `curl .../_search?size=100` + jq → 55 canonical id 정상 dump. 2014-A.md L55의 주장 목록과 1:1 일치 확인:
  - aquinas, arendt, aristotle, augustine, baek_nakcheong, bentham, buddha, confucius, dewey, epictetus, epicurus, galtung, gilligan, habermas, haidt, hanfeizi, hegel, hobbes, huineng, hume, jeongyagyong, kang_mangil, kant, kohlberg, laozi, lickona, locke, macintyre, marcus_aurelius, mencius, mill_js, mozi, nietzsche, noddings, nozick, piaget, plato, raths, rawls, rest, rousseau, sandel, sartre, seneca, socrates, spinoza, taylor, walzer, wangyangming, wonhyo, xunzi, yihwang, yiyulgok, zhuangzi, zhuxi

**주의**: `taylor` (55인 내)는 **Charles Taylor**이고, 본 출제에서 3회(2020-B/2023-A/2026-A)는 **Paul Taylor=`taylor_p`(MISS)**. Section B(55인 canonical 집계)에 `taylor`를 넣을 때 반드시 Charles Taylor row만 집계해야 하며, Paul Taylor row는 Section A(누락)로 가야 함. 스크립트는 이 구분을 엄수해야 함.

---

### 4. 기존 rejected v1/v2 보존

현재 상태 OK:
- `exam-coverage-map.v1-rejected.md` 53,379 bytes, mtime 04-19 23:32 — 미변경
- `exam-coverage-map.v2-rejected.md` 60,417 bytes, mtime 04-20 00:26 — 미변경
- `exam-coverage-map.md` (신규) **미존재** — 덮어쓰기 위험 없음.

스크립트가 반드시 `exam-coverage-map.md` **신규 파일명**으로 output해야 하며, `.v1-rejected` / `.v2-rejected` suffix 파일은 read-only로 취급. 스크립트 내에 safety guard: `if os.path.exists(out_path): fail`.

---

### 5. Section A~E 집계 정의

Manager가 제시한 5섹션 각각의 정의를 v2-rejected 구조와 비교해 정제:

#### Section A — 출제되지만 ES에 없는 사상가 (누락 집계)
- 집계 방법: 26 coverage 파일 전수에서 `thinker_id` 셀 추출 → ES 55 canonical과 차집합
- 정렬: 출제 빈도 내림차순, 동률 시 이름 오름차순
- 출력 컬럼: `planned_id | 한글명 | 출제 빈도 | 대표 출제 위치(최대 5건) | 블로커 BLK-175E-* 목록 | 비고`
- 교차 검증: 각 row가 blocker-log의 BLK-175E-* 엔트리와 짝이 맞는지 (누락 사상가인데 블로커 없음 → 스크립트가 경고)

#### Section B — canonical ES 55인 사상가형 순수 집계
- 집계 대상: thinker_id ∈ ES 55 only
- 분류는 coverage의 "분류" 컬럼이 `사상가형` 또는 `경계영역 (사상가형 포함)`인 row만
- 출력: 55 × (출제 횟수 / 최근 등장 연도 / 첫 등장 연도 / 연속 기록)
- **taylor vs taylor_p 엄수** (주의 #3 참고)

#### Section C — 경계영역 topical 집계
- 집계 대상: 분류 컬럼이 `경계영역` / `교과교육학 경계` / `교과교육학(일반)` / `한국 고유 사상·교과교육학 혼합` 등
- 서브카테고리(토픽): 통일·평화 / 메타윤리 / 한국 고유 사상 / 도덕과 교육과정 / 수업모형 / 국제정치 / 환경윤리(교과) 등
- 출력: `토픽 | 출제 빈도 | 대표 row | 포함 thinker(해당 시)`

#### Section D — 부족 claim 힌트 (TASK-176 우선순위)
- 집계 대상: Section A의 MISS 중 출제 빈도 TOP10 (3회 이상 기준 권장)
- TASK-176 우선순위 추천: `우선순위 | planned_id | 출제 빈도 | 최근 연속 기록 | 대표 trademark` 컬럼
- 2026-B 신규 정보 반영 필수: bandura 6회·3연속, jinul 3회·2연속 등

#### Section E — 분류 카운트 검증
- 집계: `사상가형 / 교과교육학 / 경계영역 / 보류(blocker 미해결)` 각 문항 수
- **총합 검산**: 293문항(2014~2026 13년×약 22문항) 또는 배점 40점(연도별) 교차 검산
- 배점 검산도 병행: `배점 합 = 문항 수 × 단가` vs 각 연도 요약
- 검산 실패 시 CI-level fail, report에 diff 출력

---

### 6. ES canonical 55 dump 확보

- `curl http://localhost:9200/ethics-thinkers/_count` → `{"count":55}` 응답 PASS (본 세션 2026-04-21 확인)
- `curl .../ethics-thinkers/_search?size=100&_source=id` 기반으로 Python이 실행 시점에 직접 ES에서 fetch하거나, 2014-A.md L55의 dump를 재사용 가능
- **권장**: 스크립트 실행 시 ES fetch를 1순위로 하되 fallback으로 architecture.md 또는 2014-A.md dump 사용. 스크립트 내에 55 ≠ len(ids) 시 fail assertion 추가

---

### 7. 블로커 누적 교차 검증 — **NEEDS_REVISION 부차 사유**

Manager 주장 **BLK-175E-* 66건**과 실제 blocker-log 불일치:

- `grep -cE "^### BLK-175E-" blocker-log.md` → **93건**
- 그 중 철회: `BLK-175E-2025A-003 — 철회됨 (FALSE-POSITIVE)` 1건
- **Net active: 92건** (Manager 주장 66건 대비 +26)
- 26 연도별 파일의 BLK 신규 발행 누적을 합산하면 93에 근접. Manager의 66은 과거 집계(특정 시점) 또는 특정 타입(신규 ES-gap만) 집계일 가능성.

**조치 필요**: Section D 작성 시 인용할 "총 블로커 건수"는 **92** (철회 1건 제외) 또는 **93** (총 발행) 중 하나로 통일. Manager가 Section A row별로 BLK ID 매핑할 때, 실제 blocker-log 엔트리가 93건임을 전제로 스크립트를 작성해야 함. 66 전제로 로직을 짜면 누락 발생.

---

### 8. 태스크 완결성 / 의존성

- task-board.md L249에 TASK-175E-MERGE 등록 PASS
- 선행 TASK-175E-2026-B-T PASS (done-log L1398) PASS
- Execution: 미명시(Manager 주장은 "coder에게 자동 스크립트 할당"), Execution=coder로 간주 가능
- 산출물 경로 지정 명확: `projects/ethics-study/exam-solutions/exam-coverage-map.md` (신규)
- 파싱 전략이 2세대 + 9 배리에이션 헤더 때문에 **단순 grep/awk로 불가능** — Manager가 "자동 스크립트"라 했을 뿐 언어/형태가 미지정. PASS 이전에 언어 결정 필요.

---

## 판정

**NEEDS_REVISION**

---

## 수정 요청 (Manager가 task-board.md TASK-175E-MERGE Description 또는 참조 문서에 아래 보완 후 재호출)

1. **(task-board.md L249)** — Description에 스크립트 언어·경로·실행 명령 명시. 권장:
   - 언어: **Python 3** (`scripts/merge_coverage.py`로 `projects/ethics-study/scripts/` 아래 배치 — 기존 `input_plato.py` 외 `insert_*.py`/`fix_*.py` 관행 동일)
   - 실행: `python3 projects/ethics-study/scripts/merge_coverage.py --coverage-dir projects/ethics-study/exam-solutions/coverage --out projects/ethics-study/exam-solutions/exam-coverage-map.md`
   - ES fetch 옵션: `--es-url http://localhost:9200` (default), fallback `--es-dump-md projects/ethics-study/exam-solutions/coverage/2014-A.md`
   - 안전 가드: `out` 경로가 이미 존재하면 `--force` 없이는 abort. `.v1-rejected`·`.v2-rejected` 파일은 read-only 접근.

2. **(task-board.md L249 또는 coder 지시 첨부)** — coverage/*.md 파일의 **헤더 배리에이션 2세대 · 최소 9종**을 명시적으로 고지. 파서는 아래 2-path 로직으로 설계:
   - (path-1) 구형 17개: 파일 상단에서 `^\| 문항 ` 헤더 탐지 → 컬럼 인덱스 dynamic mapping (`thinker_id`, `배점`, `ES 커버리지` 이름으로 lookup)
   - (path-2) 신형 9개: 파일 말미의 `^\| Q ` 헤더 탐지 → 동일 동적 매핑 (`thinker_id(s)` / `중심 사상가(thinker_id)` / `thinker_id` / `주요 사상가(thinker_id)` 4종 별칭 지원; `ES 상태` / `ES 커버리지` / `ES` 3종 별칭 지원)
   - 두 경로 모두 실패 시 해당 파일은 parser-error → report에 기록하고 abort

3. **(task-board.md L249)** — thinker_id 셀 내부 추출 정규식 구체화:
   - 각 row의 셀에서 `` `([a-z][a-z0-9_]+)` `` 패턴 매치 (0~n개 추출)
   - 매치 0개 + `[교과교육학]`/`[메타윤리 개념]`/`[...]` 존재 시 → row type = `교과교육학`
   - 매치 0개 + `없음|누락|특정 불능|보류` 키워드 → row type = `blocker-pending`
   - 매치 1개 이상 → row type = `사상가형 또는 경계영역` (분류 컬럼 보조 판별)
   - 갑/을 구분 마커(`(갑)`, `(을)`, `+`)는 id 1개씩 독립 등장으로 분해

4. **(task-board.md L249)** — Section A~E 각각의 출력 스키마를 **표 컬럼 단위**로 명시(현재 Manager 주장은 집계 방식 정도만). 위 §5의 5개 섹션 정의를 Description에 삽입하거나 architecture.md에 참조 등재.

5. **(blocker-log.md 교차 검증)** — Manager 주장 "총 66건"을 **92건(net active, 철회 1건 제외) 또는 93건(발행 총)**로 수정. 스크립트가 Section A row별 BLK ID 매핑 시 실제 93 엔트리 전수를 기준으로 해야 함.

6. **(Section B 생성 시 주의 명시)** — `taylor` (Charles Taylor, ES canonical, 55인 내)와 `taylor_p` (Paul Taylor, ES 미등록)를 **별개 인물**로 구분. 스크립트는 raw 문자열 `taylor`와 `taylor_p`를 다른 키로 취급(architecture.md L491). `taylor_p` 집계는 Section A로, `taylor` 집계는 Section B로 분리.

7. **(Section E 검산 기준)** — `총 문항 = Σ 연도별 문항` 및 `총 배점 = Σ 연도별 배점 (2014=50, 이후 40점)` 2중 검산. 스크립트는 검산 실패 시 non-zero exit.

8. **(산출 검증 단계 추가)** — Coder 완료 후 Tester가:
   - (a) Section B 55 row와 ES canonical 55 정확 일치 확인
   - (b) Section A row별 blocker-log 교차 확인 (Section A row 있는데 BLK 없음 → FAIL)
   - (c) Section E 총합 검산 재계산
   - (d) 새 파일이 `exam-coverage-map.md`(신규)로 출력, v1/v2 rejected 미변경인지 diff 확인

---

## Manager에게 전달

**재호출 플로우 권장**:

1. 위 1~7 항을 반영해 task-board.md L249 Description 확장(또는 별도 지시 문서 `signal/ethics-study/task-175E-MERGE-spec.md` 첨부) + architecture.md에 "병합 규약" 섹션 추가(선택).
2. Reviewer 재호출(본 파일 덮어쓰기 or `-v2` 접미 신규).
3. PASS 후 Coder 호출 시 프롬프트에 아래 명시:
   - 언어: Python 3
   - 입력: `projects/ethics-study/exam-solutions/coverage/*.md` (26 파일)
   - 출력: `projects/ethics-study/exam-solutions/exam-coverage-map.md` (신규, 기존 시 --force 없이 abort)
   - ES: `curl http://localhost:9200/ethics-thinkers/_search?size=100` (현재 가동 확인됨)
   - 금지: `.v1-rejected` / `.v2-rejected` 읽기 전용
   - 스크립트 자체는 `projects/ethics-study/scripts/merge_coverage.py`
4. Tester는 상기 §8-(a)~(d) 전수 검증 항목을 tester-report-TASK-175E-MERGE-T.md에 기록.

**PASS로 전환하기 위한 최소 조건**: 위 1·2·3·4·7 항이 task-board.md 또는 첨부 spec에 반영됨. 5·6·8은 강력 권장.
