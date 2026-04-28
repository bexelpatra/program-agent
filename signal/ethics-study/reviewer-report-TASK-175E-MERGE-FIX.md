---
task_id: TASK-175E-MERGE-FIX
verdict: NEEDS_REVISION
reviewer: Reviewer
reviewed_at: 2026-04-22T00:45
---

# Reviewer Report — TASK-175E-MERGE-FIX (FIX 스펙 검증)

## 판정: NEEDS_REVISION

Manager의 수정 대상(`THINKER_ID_RE.findall()` 경로 한정 dedupe)이
**실제 버그 원인(bare id 경로의 `filtered` 리스트 중복)**을 **놓침**.
Coder가 task-board 문언 그대로 실행하면 버그가 **그대로 남는다**.
Tester가 명시한 "두 경로(백틱 id, bare id) 모두에 동일하게 적용" 요구도
반영되지 않음.

---

## 재검증 결과 (7항목)

### 1. `extract_thinker_ids` 함수 존재 (L323-L343) — PASS
- `projects/ethics-study/scripts/merge_coverage.py` L323-L343 존재 확인.
- 시그니처: `def extract_thinker_ids(cell: str, known_ids: set[str] | None = None) -> list[str]:`
- 두 경로(백틱 `ids` → early return, bare `filtered` → return) 모두 dedup 없음.

### 2. `THINKER_ID_RE.findall()` 패턴 — PASS
- L183: `THINKER_ID_RE = re.compile(r"`([a-z][a-z0-9_]*)`")`
- L330: `ids = THINKER_ID_RE.findall(cell)` 존재.
- 그 외 L490, L557, L586에서도 사용 (이번 FIX 범위 아님).

### 3. 2016-B Q3 `sandel` 4× 반복 — PARTIAL (위치는 맞으나 형태가 다름)
- coverage 파일: `projects/ethics-study/exam-solutions/coverage/2016-B.md`
- Q3 detail row = line 17, 파이프-분리 **cell index 5 (thinker_id 컬럼)**.
- 해당 셀 내 **bare** `sandel` 4회 (모두 `<!-- BLOCKER(TASK-175E-2016-B-001) ... -->`
  주석 안 설명 텍스트).
- 같은 셀 내 **백틱 `` `sandel` `` 0회**.
- Tester가 말한 4회는 "bare 토큰 4회"임이 실측됨 → `extract_thinker_ids`는
  **bare 경로(`filtered`)**에서 `['sandel','sandel','sandel','sandel']` 반환.
- ⇒ 버그 존재는 확인, 단 **발생 경로는 bare** (backtick 아님).

### 4. 2016-A Q5 `wonhyo` 2× — PARTIAL (동일 이슈)
- coverage/2016-A.md line 19 cell 5: bare `wonhyo` 2회, 백틱 0회.
- bare 경로에서 중복.

### 5. 2017-A Q6 `donghak_choe` 2× — PARTIAL (동일 이슈)
- coverage/2017-A.md line 20 cell 5: bare `donghak_choe` 2회
  (모두 `<!-- BLOCKER(TASK-175E-2017-A-003) -->` 주석 내부), 백틱 0회.
- bare 경로에서 중복.

### 6. tester-report bug-1 근거 명시 — PASS
- `signal/ethics-study/tester-report-TASK-175E-MERGE.md` L128-L182에
  bug-1 현상·실측·재현코드·수정 지점·재검산 기준 모두 명시.
- 재현코드(L156-L158)는 `extract_thinker_ids(cells[5], known_ids)`를 호출해
  `['donghak_choe', 'donghak_choe']` 반환을 명시 → **bare 경로 문제임을 시사**.
- 수정 방향(L165-L176)에 "두 경로(백틱 id, bare id) 모두에 동일하게 적용"
  **명시**.

### 7. task-board MERGE-FIX 행의 수정 지점/실행 명령 구체성 — **FAIL**

task-board.md L251:
> **수정 지점**: `projects/ethics-study/scripts/merge_coverage.py` L323-L343
> `THINKER_ID_RE.findall()` 결과에 order-preserving dedupe 적용
> (`list(dict.fromkeys(ids))`).

문제점:
- (a) **대상 경로가 잘못 좁아짐**: 실제 버그 트리거는 **bare 경로의 `filtered`**
  (L337-L342)인데, 수정 대상으로 `THINKER_ID_RE.findall()` 결과(즉 `ids` 변수,
  L330)만 명시. 테스터 예시 3건 모두 해당 셀에 백틱 id는 0회 → `ids == []` →
  early return 되지 않고 bare 경로 실행 → 거기서 중복 발생.
- (b) Coder가 지시를 문언 그대로 수행하면 `ids = list(dict.fromkeys(THINKER_ID_RE.findall(cell)))`
  로 수정될 것이고, 이는 **버그를 전혀 고치지 못한 채** Section B/A 카운트를
  그대로 남긴다. 재검산(`sandel`=2, `wonhyo`=4, `donghak_choe`=1,
  `total_id_mentions`=354) 모두 미달.
- (c) Tester가 명시적으로 요구한 "두 경로 모두" dedup 적용이 누락됨.

그 외 실행 명령 자체(`python3 .../merge_coverage.py > .../exam-coverage-map.md`)와
재검산 기준(Section B sandel=2, wonhyo=4, donghak_choe=1, total_id_mentions=354)은
명확하고 실행 가능 — 이 부분은 유지해도 무방.

---

## Manager 수정 요청

task-board.md L251 TASK-175E-MERGE-FIX 행 본문의 **수정 지점** 문장을 아래로
교체 (또는 동등한 의미로 보강):

> **수정 지점**: `projects/ethics-study/scripts/merge_coverage.py` L323-L343
> `extract_thinker_ids()` 함수의 **두 반환 경로 모두에** order-preserving
> dedupe 적용.
> - 백틱 경로(L330-L332): `ids = THINKER_ID_RE.findall(cell)` 후 반환 직전
>   `return list(dict.fromkeys(ids))`.
> - bare 경로(L336-L343): `filtered`를 append한 뒤 반환 직전
>   `return list(dict.fromkeys(filtered))` (또는 `seen` set으로 append 단계에서
>   중복 skip).
> - 근거: tester-report bug-1 사례 3건(2016-B Q3 `sandel`×4, 2016-A Q5
>   `wonhyo`×2, 2017-A Q6 `donghak_choe`×2) 모두 **bare 토큰 반복**이며,
>   해당 셀의 backtick id 개수는 0. backtick 경로만 고치면 버그가 잔존함.

재검산 기준(Section B `sandel`=2·`wonhyo`=4, Section A `donghak_choe`=1,
`total_id_mentions`=354) 및 실행 명령은 그대로 유지 가능.

---

## 정리

- **PASS**: 함수 존재, 정규식 존재, tester-report 근거 명시, 실행 명령·재검산 기준.
- **PARTIAL**: Manager 수치(4×/2×/2×)는 실측과 일치하나, **형태는 bare**지
  backtick이 아님. Manager 주장의 "backtick findall 중복 매칭" 서술은 오해 소지.
- **FAIL**: task-board 수정 지점이 **backtick 경로(`ids`)로 한정**되어 있어
  실제 버그 원인(bare 경로 `filtered`)을 건드리지 못함. Coder가 지시대로
  수행하면 버그 잔존 → Tester 재검산 실패.

→ Manager가 수정 지점 문구를 **두 경로 모두** 포함하도록 보강한 뒤 Reviewer
재호출 요청. 그때까지 Coder 호출 보류.
