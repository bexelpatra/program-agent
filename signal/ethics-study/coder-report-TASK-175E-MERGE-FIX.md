---
agent: coder
task_id: TASK-175E-MERGE-FIX
status: DONE
timestamp: 2026-04-22T00:35:00
severity: bug-fix
---

## 결과 요약

Tester bug-1(`extract_thinker_ids` 셀 내 중복 매칭으로 인한 count 과대집계)을
해결했다. `projects/ethics-study/scripts/merge_coverage.py` 의
`extract_thinker_ids()` 함수 두 반환 경로 모두에 **order-preserving dedupe**
(`list(dict.fromkeys(...))`)를 적용했다. 맵 재생성 후 Tester가 지적한 5건 수치
정정이 모두 관찰되었으며, 불변 조건(Section D TOP10 순서, Section E 배점
1040/26년도, v1/v2 rejected mtime)도 유지되었다.

## 변경된 파일

- `projects/ethics-study/scripts/merge_coverage.py`
  - `extract_thinker_ids()` L323-L343 패치 (2개 반환 경로에 dedupe + docstring 갱신).
- `projects/ethics-study/exam-solutions/exam-coverage-map.md`
  - 스크립트 재실행으로 재생성 (16350 bytes). 수치 5건 정정.
- `signal/ethics-study/coder-report-TASK-175E-MERGE-FIX.md` (이 파일, 신규).

v1/v2 rejected md 미수정. `coverage/*.md` 원본 미수정. architecture.md ·
task-board.md 직접 수정 없음.

## 패치 내용

```python
def extract_thinker_ids(cell: str, known_ids: set[str] | None = None) -> list[str]:
    """셀에서 thinker_id 추출 (셀 내 중복 제거, 순서 유지).

    1. 백틱 감싼 id 우선 추출.
    2. 백틱 id가 하나도 없으면 bare id 추출 — 단 canonical ES 55 또는
       MISS_NAME_MAP 알려진 id와 매칭되는 토큰만 채택 (오탐 방지).

    동일 셀 내 같은 id가 여러 번 등장해도 1회로 축약 (count 의미 없음).
    서로 다른 row/cell 간의 중복은 호출 측에서 유지한다.
    """
    ids = THINKER_ID_RE.findall(cell)
    if ids:
        return list(dict.fromkeys(ids))   # ← dedupe (backtick path)
    # 백틱 없는 구형 파일: bare token 추출 후 알려진 id만 채택
    if known_ids is None:
        return []
    bare = BARE_ID_RE.findall(cell)
    filtered = []
    for tok in bare:
        if tok in STOPWORDS:
            continue
        if tok in known_ids:
            filtered.append(tok)
    return list(dict.fromkeys(filtered))  # ← dedupe (bare-id path)
```

- 동일 셀 내 반복 등장 id 는 1회로 축약 (count 의미 없음).
- 서로 다른 row/cell 간 중복은 호출 측(`aggregate_all`) 루프에서 그대로 누적
  → Section A/B 출제횟수 집계 의미 보존.
- Reviewer 확인대로 Tester 실측상 정정 3건은 모두 bare-id 경로에 해당하나,
  backtick 경로도 동일한 규약 준수를 위해 양쪽 모두 dedupe 적용.
- 외 로직/시그니처/반환 타입(list[str]) 변경 없음.

## 정정 전/후 수치

| 항목 | 전(bug) | 후(fix) | 증감 |
|------|--------|--------|------|
| Section B `sandel` 출제횟수 | 5 | **2** | −3 |
| Section B `wonhyo` 출제횟수 | 5 | **4** | −1 |
| Section A `donghak_choe` 출제횟수 | 2 | **1** | −1 |
| metadata `total_id_mentions` | 359 | **354** | −5 |
| Section D TOP10 순서 | jinul→blasi→durkheim→hoffman→bandura→pettit→singer→turiel→moore→narvaez | 동일 | **불변** |
| Section E 배점 합 (26/26 년도) | 1040 | 1040 | **불변** |

수치 증감 합계: −5 == `total_id_mentions` 감소치와 정확히 일치(내부 정합성 OK).

## 검증 로그

```
$ python3 projects/ethics-study/scripts/merge_coverage.py
[merge_coverage] WARN: exam-coverage-map.md already exists, overwriting (TASK-175E-MERGE first run).
[merge_coverage] ES cluster status: yellow
[merge_coverage] ethics-thinkers count = 55
[merge_coverage] canonical 55 dump OK (55 ids)
[merge_coverage] ethics-claims aggregation: 55 thinkers with claims
[merge_coverage] blocker-log: issued=93, withdrawn=1, net active=92
[merge_coverage] 2014-A: rows=20, score_sum=50
...
[merge_coverage] 2026-B: rows=11, score_sum=40
[merge_coverage] wrote /home/jai/program-agent/projects/ethics-study/exam-solutions/exam-coverage-map.md (16350 bytes)
[merge_coverage] summary: rows=293, id_mentions=354, MISS_thinkers=45, HIT_thinkers=49
```

맵 본문 grep 결과:
- L122: `| 42 | \`sandel\` | 마이클 샌델 | 2 | 2016-B, 2017-A | 10 |` → **2회 PASS**
- L115: `| 35 | \`wonhyo\` | 원효 (元曉) | 4 | 2014-A, 2016-A, 2018-A, 2024-A | 3 |` → **4회 PASS**
- L54: `| 26 | \`donghak_choe\` | 동학 최제우·최시형 | 1 | 2017-A | — |` → **1회 PASS**
- L263: `total_id_mentions: 354` → **354 PASS**
- L211-L220 TOP10 순서 불변 → **PASS**
- L226-L252 Section E 배점 50+30+40×24=1040, 26/26 OK → **PASS**

6건 전수 검증 PASS.

## 사이드 이펙트 / 비고

- metadata `total_question_rows`(=293) 및 blocker-log 카운트(93/1/92) 등 다른
  집계 수치는 불변.
- Section A 행수 45, Section B 행수 55, Section C 행수 61 불변.
- Section B `taylor`(찰스 테일러, #45 = 2회) / Section A `taylor_p`(폴 테일러,
  #17 = 2회) 동명이인 분리 규약 유지 (architecture.md:491 근거).
- Tester report observation(2020-B Q11·2021-A Q5·2022-A Q10 unescaped `|`)는
  이번 패치 범위 밖. bug-1과 무관하며 집계에 영향 없음(Tester 기 확인).

## 후속 권고

Manager 판단용 메모:
- 본 FIX로 Tester 지적 bug-1은 해소. 재검증은 Manager 재량.
- observation(unescaped `|`)은 별도 태스크 또는 retrospective 이월 가능.
- Section A/B/C/D/E 모든 구조·순서 보존. ES/blocker-log 측 영향 없음.
