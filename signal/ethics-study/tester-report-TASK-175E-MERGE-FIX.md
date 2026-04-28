---
task_id: TASK-175E-MERGE-FIX
agent: tester
status: PASS
verdict: DONE
severity: observation
generated_at: 2026-04-22
---

# Tester Report — TASK-175E-MERGE-FIX

## 검증 대상
- 코드: `projects/ethics-study/scripts/merge_coverage.py` (`extract_thinker_ids()` dedupe 패치)
- 산출물: `projects/ethics-study/exam-solutions/exam-coverage-map.md` (재생성)
- 목적: bug-1 회귀(같은 셀 내 동일 id 중복 카운트 오계수) 종결 + 무회귀

## 체크리스트 결과 (8/8 PASS)

| # | 체크 | 기대 | 실측 | 결과 |
|---|------|------|------|------|
| 1 | 패치 실재 (dict.fromkeys dedupe) | backtick/bare 두 경로 모두 | L335 `list(dict.fromkeys(ids))` + L346 `list(dict.fromkeys(filtered))` | PASS |
| 2 | Section B `sandel` | 2 (5→2) | `\| 42 \| \`sandel\` \| 마이클 샌델 \| 2 \|` | PASS |
| 3 | Section B `wonhyo` | 4 (5→4) | `\| 35 \| \`wonhyo\` \| 원효 (元曉) \| 4 \|` | PASS |
| 4 | Section A `donghak_choe` | 1 (2→1) | `\| 26 \| \`donghak_choe\` \| … \| 1 \|` | PASS |
| 5 | `total_id_mentions` | 354 (359→354) | L263 `total_id_mentions: 354` | PASS |
| 6 | Section D TOP10 순서 불변 | jinul(7)→blasi(5)→durkheim(5)→hoffman(5)→bandura(4)→pettit(4)→singer(4)→turiel(4)→moore(3)→narvaez(3) | L211~220 전부 일치 | PASS |
| 7 | Section E 26년 OK + 합계 1040 | 불변 | 26개 연도 모두 `OK`, **합계 293/1040** | PASS |
| 8 | 회귀 없음 | A=45, B=55, C=61; blocker 93/1/92; taylor/taylor_p 분리; v1/v2 mtime 불변 | A=45, B=55, C=61; metadata blockers 93/1/92; `taylor`(찰스, L125) / `taylor_p`(폴, L44) 분리 유지; v1 mtime 2026-04-19 23:32 / v2 mtime 2026-04-20 00:26 (불변) | PASS |

## 세부 근거

### 1. 패치 실재 (`merge_coverage.py`)
```python
# L323~346
def extract_thinker_ids(cell: str, known_ids: set[str] | None = None) -> list[str]:
    ids = THINKER_ID_RE.findall(cell)
    if ids:
        return list(dict.fromkeys(ids))          # L335: backtick 경로
    if known_ids is None:
        return []
    bare = BARE_ID_RE.findall(cell)
    filtered = []
    for tok in bare:
        if tok in STOPWORDS:
            continue
        if tok in known_ids:
            filtered.append(tok)
    return list(dict.fromkeys(filtered))         # L346: bare-id 경로
```
두 반환 경로 모두 `list(dict.fromkeys(...))` dedupe 적용 확인.

### 2~5. 카운트 감소 검증
- sandel: 5 → **2** (bug-1 특정 셀 내 중복 수정 반영)
- wonhyo: 5 → **4**
- donghak_choe: 2 → **1**
- total_id_mentions: 359 → **354** (5건 감소)
- 5건 감소는 4항목 합(3+1+1=5, sandel 감소 3회 + wonhyo 감소 1 + donghak_choe 감소 1) = **5**로 총합 일치, 논리적 일관성 확인.

### 6. Section D TOP10
L211~220 순서 jinul(7) → blasi(5) → durkheim(5) → hoffman(5) → bandura(4) → pettit(4) → singer(4) → turiel(4) → moore(3) → narvaez(3) 으로 체크리스트와 정확히 일치. 최근 출제연도·권고 칼럼도 유지.

### 7. Section E 배점 검산
- 행수: 26개 연도 (2014-A ~ 2026-B) 모두 `일치=OK`
- 합계 행: 문항수 293, 배점합 **1040** — 불변.

### 8. 회귀 없음
- Section A 데이터 행: **45** (awk+grep 카운트)
- Section B 데이터 행: **55**
- Section C 데이터 행: **61**
- Metadata `blockers_issued: 93`, `blockers_withdrawn: 1`, `blockers_net_active: 92` — 불변
- `taylor`(찰스 테일러, canonical 55인 중 #45)와 `taylor_p`(폴 테일러, Section A #16) 분리 유지
- `exam-coverage-map.v1-rejected.md` mtime 2026-04-19 23:32:xx
- `exam-coverage-map.v2-rejected.md` mtime 2026-04-20 00:26:xx
- 두 파일 모두 현재 날짜(2026-04-22) 이전 생성 이후 변경 없음 — 불변 조건 충족.

## 이슈/블로커
없음. 8개 체크리스트 전부 PASS. 수정 태스크 신규 등록 불필요.

## 판정
**verdict=DONE, status=PASS, severity=observation**

TASK-175E-MERGE-FIX의 모든 수용 조건이 충족되었다. `extract_thinker_ids()`의 dedupe 패치는 두 반환 경로 모두 반영되었고, 재생성된 `exam-coverage-map.md`는 bug-1로 지적된 3항목(sandel, wonhyo, donghak_choe) 감소와 전체 id mention 합계 354로의 일관적 감소를 반영하면서, Section D/E 구조·타 섹션 행수·blocker 카운트·canonical id 분리·rejected 스냅샷 등 무회귀 조건을 전부 지켰다.
