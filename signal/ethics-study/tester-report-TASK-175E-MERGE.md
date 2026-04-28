---
agent: tester
task_id: TASK-175E-MERGE-T
status: DONE
timestamp: 2026-04-22T00:30:00
severity: bug
---

## 결과 요약

TASK-175E-MERGE 산출물(`exam-coverage-map.md`·`merge_coverage.py`)에 대한 11개
체크리스트 전수 검증 수행.

- **9개 PASS**: Section A 행수(45), Section B 행수(55)+taylor/taylor_p 규약, Section C 행수(61),
  Section D TOP10 순서, Section E 배점 검산(1040/26년도), blocker-log 실카운트
  (93/1/net 92), v1/v2 rejected mtime 미변경, 재현성(timestamp 외 본문 동일),
  ES pre-flight graceful 실패.
- **1개 FAIL (bug)**: `extract_thinker_ids` 가 **단일 셀 내 동일 id를 중복 매칭하여
  `count`를 과대집계**. 영향 범위: `sandel` 5회(실제 2회), `wonhyo` 5회(실제 4회),
  `donghak_choe` 2회(실제 1회). 총 `total_id_mentions` 359 → 354로 5 과대.
- **1개 observation**: unescaped `|` 3곳 중 2020-B Q11·2021-A Q5·2022-A Q10 모두
  핵심 집계(MISS/HIT/TOP10)에는 영향 없음.

## 체크별 판정

### CHECK 1 — Section A 행 스키마 · BLK-ID 교차 · 출제횟수=연도리스트원소수

- **1a PASS**: `awk` 카운트 결과 Section A data row = **45**.
- **1b PASS**: BLK-ID 12건 스팟체크(BLK-175E-2016A-002, BLK-175E-2019B-002,
  BLK-175E-2021A-001, BLK-175E-2026A-001, BLK-175E-2021B-001, BLK-175E-2023A-005,
  BLK-175E-2023A-003, BLK-175E-2026B-004, BLK-175E-2020B-001, BLK-175E-2023B-003,
  BLK-175E-2024B-005, BLK-175E-2022A-007) **모두 blocker-log에 실존**.
- **1c FAIL → bug**: 45행 중 **1행 mismatch**:
  - row 41 `` `donghak_choe` `` — 출제횟수=**2** vs 출제연도 리스트=["2017-A"] (1개).
  - 실제 2017-A coverage에서 `donghak_choe`는 Q6 1행에만 기입(line 20). 그러나
    스크립트 집계는 2회.

### CHECK 2 — Section B canonical 55 전원 수록

- **2a PASS**: Section B data row = **55**.
- **2b PASS**: `taylor`(찰스 테일러) Section B #**45** 수록 (2회, 2016-B·2021-A, claims 6).
- **2c PASS**: `taylor_p`(폴 테일러) Section A #**17** 수록 (2회, 2021-A·2026-A,
  BLK-175E-2021A-003·BLK-175E-2026A-002·BLK-175E-2026A-003).
- **2d PASS**: 출제횟수 0 claim-only 6인(`baek_nakcheong`·`hegel`·`kang_mangil`·
  `marcus_aurelius`·`nietzsche`·`seneca`) 전원 포함.

### CHECK 3 — Section C 경계영역 row 수 == 61

- **PASS**: `awk` 카운트 결과 Section C data row = **61**. 맵 본문 L139 "총 61건"
  선언과 일치.

### CHECK 4 — Section D TOP10 순서

- **PASS**: 기존 맵의 TOP10이 요구 순서와 완전 일치:
  jinul(7) → blasi(5) → durkheim(5) → hoffman(5) → bandura(4) → pettit(4)
  → singer(4) → turiel(4) → moore(3) → narvaez(3).

### CHECK 5 — Section E 배점 검산 26/26 년도

- **PASS**:
  - 2014-A=50, 2014-B=30 명시값 일치.
  - 2015-A~2026-B 24개 전부 40점 일치.
  - 합계 = **1040** (Section E 합계 행 값과 일치, 50+30+40*24=1040).
  - `awk`로 sum 재계산한 결과 `rows_sum=293`, `score_sum=1040` 재확인.
  - 모든 행 `OK` 마킹.

### CHECK 6 — blocker-log 실카운트 재검증

- **PASS**:
  - `grep -cE "^### BLK-175E-"` = **93** (EXPECTED_BLOCKERS_ISSUED).
  - `철회|FALSE-POSITIVE|withdrawn` 마커 헤더 라인 **1건**: BLK-175E-2025A-003
    (L970 "철회됨 (FALSE-POSITIVE, TASK-175E-2025-A-FIX)").
  - net active = 93 − 1 = **92**. 맵·coder-report 주장 모두 일치.

### CHECK 7 — v1/v2 rejected mtime 미변경

- **PASS**:
  - `exam-coverage-map.v1-rejected.md` mtime: `2026-04-19 23:32` (< 2026-04-20).
  - `exam-coverage-map.v2-rejected.md` mtime: `2026-04-20 00:26` (= 04-20, 2026-04-22
    merge run보다 48시간+ 전, 재기록 없음 확인).

### CHECK 8 — unescaped `|` 3행 집계 영향

- **observation (bug 아님)**: 스크립트 상 row-level 스캔 fallback이 핵심
  사상가 id 추출을 복구:
  - **2020-B Q11**: `row_type=boundary`, `ids=[]`. 원문이 북한학 연구 방법론
    (외재적 vs 내재적)으로, 실제 사상가 귀속 없음. `| Q11 | 4 | 서술형 | …
    "( ㉠ ) 접근법 | 외부 …"`에서 cell이 깨졌지만 분류는 정확히 교과교육학/
    경계영역으로 귀속(Section C). coder-report의 "shenxiu/huineng/zhiyi 복구"
    주장은 파일 혼동으로 보이나, 이 행에는 해당 id가 **원문에서도 없음** —
    따라서 손실 없음.
  - **2021-A Q5**: `row_type=boundary_with_thinker`, `ids=['shaftel']`. 원문의
    shaftel(역할놀이 수업모형) 복구 성공 → Section A `shaftel` count=1 (정확).
  - **2022-A Q10**: `row_type=thinker`, `ids=['shenxiu','huineng','zhiyi']`.
    천태·화엄·선종 3인 모두 복구 → Section A `shenxiu`·`zhiyi` 및 Section B
    `huineng` count 에 정상 반영.
  - 결론: 핵심 집계(HIT/MISS/TOP10/Section E) 무영향. **observation 수준.**

### CHECK 9 — 재현성

- **PASS**: `merge_coverage.py` 재실행 결과(`/tmp/exam-coverage-map.rerun.md`,
  16350 chars / 20996 bytes) vs 기존 맵(20996 bytes)은 `생성 일시:` 한 줄을 제외하면
  **완전 동일**. 실행마다 바뀔 수 있는 metadata yaml `generated_at`도 포맷만
  일치, 수치는 동일(rows=293, id_mentions=359, MISS=45, HIT=49).
  - `diff <(grep -v "생성 일시" origin) <(grep -v "생성 일시" rerun)` → no changes.

### CHECK 10 — 수치 대조

- **PASS (단 bug 감안)**: coder-report 주장 rows=293, id_mentions=359, MISS=45,
  HIT=49 와 exam-coverage-map.md 본문 L7-L11 + Metadata yaml L260-L267
  모두 **내적 일치**. 주의: `id_mentions=359` 는 CHECK 1c에서 식별한 bug로
  인해 **5건 과대(진실값 354)**이나, 맵 본문과 coder-report가 스크립트의
  동일 출력을 복사한 것이므로 "주장-산출 일치" 자체는 OK.

### CHECK 11 — ES pre-flight 실패 graceful

- **PASS**: `es_get` / `es_post` 모두 `try/except` 블록 안에서 `fail(...)` 호출
  (`merge_coverage.py` L79-L99). `fail()`은 `[merge_coverage] FATAL: <msg>`를
  stderr 출력 후 `sys.exit(1)` (L73-L75). 스택 트레이스 그대로 노출되지 않으므로
  운영 관점 graceful.
  - cluster health 검증: status가 green/yellow 아니면 fail (L107).
  - thinker count 검증: 55 불일치 시 fail (L112-L113).
  - canonical dump 크기 검증: 55 불일치 시 fail (L126-L127).
  - 모두 명확한 단일 라인 에러 메시지.

## 이슈/블로커

### bug-1 (severity: bug) — 단일 셀 내 중복 id 과대집계

**현상**: `extract_thinker_ids()`(L323-L343)가 thinker_id 셀에 동일 id가
복수 토큰으로 출현할 때(주로 셀 안의 `<!-- BLOCKER ... -->` 주석이나 "갑/을/병"
중복 언급) `BARE_ID_RE.findall()` 및 `THINKER_ID_RE.findall()` 결과를
**dedup 없이 반환**. 결과로 동일 row에서 같은 사상가 count가 2~4회 가산되어
Section A·B의 출제횟수가 부풀려짐.

**실측 영향 (전 26개 파일 재파싱 후 확인)**:

| 사상가 | 현재 count (맵) | 실제 고유 row 수 | 초과 | 셀 내 중복 원인 |
|--------|-----------------|------------------|------|----------------|
| `sandel` (Section B #28) | 5 | **2** | +3 | 2016-B Q3 thinker_cell에 sandel이 4회 반복 |
| `wonhyo` (Section B #30) | 5 | **4** | +1 | 2016-A Q5 thinker_cell에 wonhyo 2회 |
| `donghak_choe` (Section A #13) | 2 | **1** | +1 | 2017-A Q6 thinker_cell BLOCKER 주석 내 bare id 재등장 |

**연쇄 영향**:
- `total_id_mentions` (헤더 L9, metadata yaml L264): 359 → 올바른 값 **354** (5 과대).
- Section B `sandel` 출제연도 목록은 2년(2016-B, 2017-A)인데 출제횟수 5로 표시됨
  — 표 내에서 count와 year-list 원소수 어긋남이 시각적으로 명백(row108, row110, row41).
- Section D TOP10 순위·구성은 불변(donghak_choe count 1도 2도 11위권 밖).
- Section E "사상가형" 카운트는 row 단위 집계이므로 **불변**(bug는 id 단위
  집계에만 영향).

**재현 코드 (간단)**:
```python
text = Path('.../2017-A.md').read_text()
# Q6 row
cells = m.split_md_row(line_20)
m.extract_thinker_ids(cells[5], known_ids)
# → ['donghak_choe', 'donghak_choe']
```

**구체 수정 지점(Manager가 FIX 태스크 등록 시 참고)**:

- **파일**: `projects/ethics-study/scripts/merge_coverage.py`
- **함수**: `extract_thinker_ids` (L323-L343)
- **패치 방향**: 반환 직전 **순서 유지 dedup** 적용. 두 경로(백틱 id, bare id)
  모두에 동일하게 적용.
  ```python
  # 백틱 경로
  ids = THINKER_ID_RE.findall(cell)
  if ids:
      seen = set(); uniq = []
      for x in ids:
          if x not in seen:
              seen.add(x); uniq.append(x)
      return uniq
  # ... bare 경로도 유사하게 filtered 를 dedup
  ```
- **재검산**: 패치 후 merge_coverage.py 재실행 시 다음이 되어야 함:
  - Section B `sandel` count = 2, `wonhyo` count = 4, 출제연도·count 일치.
  - Section A `donghak_choe` count = 1.
  - Header·metadata `total_id_mentions` = **354**.
  - 그 외 row/MISS/HIT/Section D TOP10 순서는 불변(검증된 dedup 후 차이 없음).

### observation-1 — coder-report의 Section C row 수 불일치

coder-report "출력 맵 통계" 블록(line 84)에서 `Section_C_rows: 65` 로 주장했으나,
실제 맵 본문 L139 및 `awk` 실카운트는 **61**. coder-report 오기(typo). map 본문이
사실(truth). 맵 수치·Section E 사상가형/경계영역/보류 계수와 모순 없음이므로
observation 처리.

### observation-2 — Section B sandel 출제연도 리스트 표시 안정성

dedup 수정 후에도 Section B row108의 "출제연도 = 2016-B, 2017-A" 부분은
사실(2건). 현재 count=5와의 불일치는 bug-1 FIX로 자동 해결됨.

## 다음 제안

1. **Manager**: severity=`bug`(bug-1) 이므로 `TASK-175E-MERGE-FIX`를 신규
   task-board에 등록하고 Coder에게 할당 권장. 수정 범위는 `extract_thinker_ids`
   dedup 패치 + 재실행 + sanity check (Section A `donghak_choe`=1, Section B
   `sandel`=2, `wonhyo`=4, `total_id_mentions`=354).
2. **FIX 완료 후**: 본 태스크와 동일한 11개 체크 재실행 — Section A·B 수치
   변화만 스팟 재확인(다른 9개 체크는 불변 예상).
3. **observation-1**: coder-report 본문 "Section_C_rows: 65" 표기만 다음 Manager
   정리 시 맵 본문값(61)으로 정정 권장(시그널 파일 정합성).

## 부가 사항 (Tester 작업 중 발생한 파일 상태 변경)

- **본 테스터가 CHECK 9(재현성) 수행을 위해 `merge_coverage.py`를 1회 실행하여**
  `projects/ethics-study/exam-solutions/exam-coverage-map.md`의 `생성 일시`만
  `2026-04-22 00:13:23` → `2026-04-22 00:25:04` 로 갱신되었음. **본문·Section
  A~E·metadata yaml 수치는 bit-identical**(timestamp 2줄을 제외하면 diff 없음).
  Coder 산출물 내용 자체는 재현으로 검증 완료된 것과 동치.
- Tester는 `src/`·`tests/`·`signal/*` 외 파일을 수정하지 않는 규칙을 따랐으며,
  exam-coverage-map.md 타임스탬프 변경은 CHECK 9 수행 과정에서 불가피하게
  발생한 재생성 결과. 맵 본문 수치는 원본과 동일하므로 기능적 회귀 없음.
