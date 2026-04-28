---
task_id: TASK-175E-MERGE-FIX
verdict: PASS
reviewer: Reviewer
reviewed_at: 2026-04-22T00:52
supersedes: reviewer-report-TASK-175E-MERGE-FIX.md
---

# Reviewer Report v2 — TASK-175E-MERGE-FIX (FIX 스펙 재검증)

## 판정: PASS

v1에서 지적한 "수정 지점이 backtick 경로로 한정되어 bare 경로의 실제 버그를
놓친다"는 문제가 task-board.md L251에서 해결됨. Coder가 지시대로 수행하면
tester-report bug-1의 3개 사례(2016-B Q3 `sandel`×4, 2016-A Q5 `wonhyo`×2,
2017-A Q6 `donghak_choe`×2) 모두 정확히 재검산 목표에 도달한다.

---

## v1 지적 3개 기준 재검증

### 기준 1. "두 반환 경로 모두" 문구 존재 — PASS

task-board.md L251 발췌:
> `extract_thinker_ids()` 함수의 **두 반환 경로 모두**에 order-preserving
> dedupe 적용

- "두 반환 경로 모두" 문자열이 bold 강조로 명시됨.
- v1 요구("두 경로 모두 dedup") 충족.

### 기준 2. backtick 경로(L330) + bare-id 경로(L337-L342) 둘 다 언급 — PASS

task-board.md L251 발췌:
> (a) backtick 경로 `THINKER_ID_RE.findall()` 결과 (L330 부근),
> (b) bare-id 경로 `filtered` 리스트 (L337-L342 부근). 두 경로 모두
> `list(dict.fromkeys(ids))` 적용 필수

실측 (`projects/ethics-study/scripts/merge_coverage.py`):
- L330: `ids = THINKER_ID_RE.findall(cell)` — backtick 경로 소스. ✓
- L332: `return ids` — backtick 경로 반환 (dedupe 대상).
- L337-L342: `filtered = []` ~ `filtered.append(tok)` — bare-id 경로 수집. ✓
- L343: `return filtered` — bare-id 경로 반환 (dedupe 대상).

두 경로 모두 명시적으로 호명되었고 line range도 실제 파일과 일치.

### 기준 3. "실제 3개 bug cell은 모두 bare-id 경로" 명시 — PASS

task-board.md L251 발췌:
> 두 경로 모두 `list(dict.fromkeys(ids))` 적용 필수
> **(Tester 근거상 실제 3개 bug cell은 모두 bare-id 경로)**.

- Coder가 우선순위·실측 근거를 이해할 수 있도록 "실제 버그는 bare-id 경로"임을
  명시. v1 지적의 재발 방지 효과.

---

## 부가 검증 (v1 대비 유지 항목)

- `extract_thinker_ids` 함수 위치(L323-L343) — 실제와 일치. PASS.
- 재검산 기준(Section B sandel=2·wonhyo=4, Section A donghak_choe=1,
  total_id_mentions=354) — task-board에 유지됨. PASS.
- 실행 명령(`python3 projects/ethics-study/scripts/merge_coverage.py > ...`) —
  명확·실행가능. PASS.
- Section D TOP10 순서 불변·Section E 배점 불변 재확인 요구 — 유지. PASS.

## 잠재 리스크 (FYI, non-blocking)

- task-board 문언에서 backtick 경로 dedupe도 요구했지만, tester 실측상
  backtick 경로 중복은 현재 데이터셋에 존재하지 않음. 따라서 backtick 경로
  dedupe는 **방어적** 조치이며 회귀 방지 의미. Coder가 두 반환문 모두 수정하면
  결과적으로 안전함. (bug 아님.)
- `list(dict.fromkeys(ids))` 표현이 bare 경로에서는 `filtered`에 적용되어야
  한다는 점은 문맥상 자명하나, Coder 구현 시 변수명 주의 필요 (리뷰 대상
  Coder 산출물 PR에서 확인).

---

## 정리

- v1 NEEDS_REVISION의 3개 요구(두 경로 명시, L330 + L337-L342 둘 다, bare 경로
  실사유 명시) 모두 task-board.md L251에 반영됨.
- Coder 호출 가능. 호출 후 산출물(merge_coverage.py patch + exam-coverage-map.md
  재생성)은 별도 Reviewer 검증 대상.
- 판정: **PASS**.
