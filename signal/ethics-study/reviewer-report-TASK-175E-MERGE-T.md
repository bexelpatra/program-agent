---
agent: reviewer
task_id: TASK-175E-MERGE-T
verdict: NEEDS_REVISION
reviewed_at: 2026-04-22T00:20
scope: Manager가 signal/ethics-study/task-board.md L250에 등록한 TASK-175E-MERGE-T(Tester 검증) 스펙의 11개 체크 항목이 실제 파일·수치와 일치하는지 독립 검증
---

# Reviewer Report — TASK-175E-MERGE-T

## 판정 요약

**NEEDS_REVISION** — 11개 체크 중 10개 Manager 주장은 실측과 일치하나, **체크 (3) Section C row 수 "65건"은 오기**이다. 실제 `exam-coverage-map.md` 본문 헤더(L139)와 실측 row 카운트는 **61건**. Tester에게 전달하기 전 Manager가 스펙을 고쳐야 한다(그대로 보내면 Tester가 "Section C 65건 불일치 → bug" 리포트를 쓴다).

---

## 실측 결과 (11개 체크 항목)

| # | Manager 주장 | 실측 | 일치 | 증거 |
|---|--------------|------|------|------|
| 1 | Section A 45명 | 45 row | OK | `awk '/^## Section A/,/^## Section B/' map.md \| grep -cE '^\| [0-9]+ \| \`'` = 45 |
| 2 | Section B canonical 55 / taylor vs taylor_p 분리 | 55 row / `taylor`=#45 Section B(찰스 테일러·L125) / `taylor_p`=#17 Section A(폴 테일러·L45) | OK | awk+grep 직접 확인. 출제횟수 0(L130~135: baek_nakcheong·hegel·kang_mangil·marcus_aurelius·nietzsche·seneca) 6명 포함 |
| 3 | **Section C 경계영역 row 수 65건** | **61건** (map.md L139 본문 "총 61건" + awk 실측 61) | **MISMATCH** | `awk '/^## Section C/,/^## Section D/' map.md \| grep -cE '^\| [0-9]{4}-[AB]'` = **61** |
| 4 | Section D TOP10: jinul(7)→blasi(5)→durkheim(5)→hoffman(5)→bandura(4)→pettit(4)→singer(4)→turiel(4)→moore(3)→narvaez(3) | map.md L211-L220 순서 완전 일치 | OK | Read 직접 확인 |
| 5 | Section E 배점 검산 26년도/합계 1040 (2014A=50, 2014B=30, 2015+=40×24) | map.md L225-L252 모두 "OK"; 합계 row "**합계** \| **293** \| — \| — \| — \| **1040**" | OK | 2014A=50, 2014B=30, 나머지 24=40×24=960 → 총 1040 산술 확인 |
| 6 | blocker-log issued=93 / withdrawn=1 / net=92 | `grep -c '^### BLK-175E-' blocker-log.md` = **93**. 철회 레코드 1건(L970 BLK-175E-2025A-003 FALSE-POSITIVE rest). Metadata yaml L264-266 동일 | OK | 일치. ※ 주의: task-board.md L249(MERGE row description)에는 "총 **92건** + 철회 1 = net 92"로 기재되어 있음 — MERGE-T(L250)는 "issued=**93**" 올바르게 표기. MERGE row description 자체가 내부 불일치이나 DONE 태스크라 영향 없음 |
| 7 | v1/v2 rejected mtime 미변경(2026-04-20 이전) | v1=2026-04-19 23:32, v2=2026-04-20 00:26 | OK | `stat -c '%y'` 확인. v2는 04-20 00:26 — MERGE가 04-22 00:13 실행임을 고려할 때 "pre-MERGE 상태 유지" 맞음 |
| 8 | Coder 원문 unescaped `\|` 3건(2020-B Q11, 2021-A Q5, 2022-A Q10) 영향 조사 | 2020-B Q11 / 2021-A Q5는 Section C에 row로 등장(L182, L187). 2022-A Q10은 map에 미등장 | 일부 OK | Tester가 실제로 재현 조사해야 할 사안이므로 Manager 스펙 자체는 정당. 단 "2022-A Q10"이 map에 빠진 이유는 실제로 해당 row가 존재하지 않거나 unescaped 파이프로 swallowed인지 Tester가 검증해야 한다 |
| 9 | 스크립트 재실행 재현성 | `merge_coverage.py` 존재 43181 bytes · 실행 명령 task-board에 명시 | OK(실행 가능) | Tester가 실제 재실행 수행. ES 의존성은 체크 11이 커버 |
| 10 | row=293 / id_mentions=359 / MISS=45 / HIT=49 | map.md L6-L11: 293/359/45/49 전부 일치 | OK | Read 확인. Metadata yaml L259-263 중복 확인 |
| 11 | ES pre-flight 실패 시 graceful fail | 스크립트 실존 · 검증 가능 | OK(실행 가능) | Tester가 실제로 ES down 시뮬레이션하여 재현해야 하는 체크. Manager 스펙 자체는 정당 |

---

## 부가 확인

- **3개 산출물 파일 실존** (Manager claim #1):
  - `projects/ethics-study/scripts/merge_coverage.py` = **43181 bytes** (mtime 2026-04-22 00:11) ✓
  - `projects/ethics-study/exam-solutions/exam-coverage-map.md` = **20996 bytes** (mtime 2026-04-22 00:13) ✓
  - `signal/ethics-study/coder-report-TASK-175E-MERGE.md` = **7427 bytes** (mtime 2026-04-22 00:13) ✓
- **task-board.md L249**: TASK-175E-MERGE 상태 = `DONE` ✓
- **task-board.md L250**: TASK-175E-MERGE-T `Depends On` = `TASK-175E-MERGE` ✓
- **26개 coverage 입력**: `ls coverage/*.md \| wc -l` = 26 ✓
- **withdrawn 마커**: blocker-log grep에서 `철회` 7건, `FALSE-POSITIVE` 1건이 집계되나, "블로커 엔트리 자체의 철회"는 1건(BLK-175E-2025A-003, L970)뿐이다. 나머지 6건은 hoffman 사상가 개념 설명("사랑의 철회"·"애정 철회형") 문구이므로 집계 제외 정당. Manager 주장 "withdrawn 1" 실질 맞음

---

## 지적 사항 (Manager가 수정해야 할 항목)

### 필수 수정 (PASS 복귀 조건)

1. **task-board.md L250 체크 (3) 수정**: "Section C 경계영역 row 수 **65건** 일치" → "Section C 경계영역 row 수 **61건** 일치" 로 수정. 근거:
   - `exam-coverage-map.md` L139 본문: "총 61건. 사상가형으로 분류되지 못한(또는 혼합) row 전수."
   - 실측 `awk+grep` = 61.
   - 이 체크를 그대로 Tester에게 보내면 Tester는 "65 ≠ 61 → severity=bug" 리포트를 쓴다. 실제 bug가 아닌 스펙 오기에서 파생된 false positive이므로 Manager 책임으로 교정 필요.

### 선택 수정 (권장)

2. (Optional) task-board.md L249 MERGE row description 내부 일관성: "blocker-log 실측 ... 총 **92건** + 철회 1 = net 92" 문구는 `grep -c '^### BLK-175E-'` = 93과 불일치. 실제 headline은 93이므로 "총 **93건** + 철회 1 = net 92"로 교정 권고. 단, MERGE는 이미 DONE이고 맵 본문·metadata yaml은 93/1/92로 올바르게 나오므로 Tester 체크에 직접 영향 없음. 우선순위는 Low.

### Tester에게 상기시킬 주의사항

- 체크 (8) "2022-A Q10 unescaped `\|`": map.md Section C에 해당 row가 없다. Tester가 실측할 때 "map 집계에 영향 없음(swallowed or no row)"인지, "2022-A Q10 자체가 coverage/2022-A.md에 등장하는 문항인지"를 coverage 원문과 교차 확인해야 한다. Manager 스펙이 정당한지는 Tester의 실조사에 달림.
- 체크 (9) 재현성: 스크립트를 재실행했을 때 **ES cluster_status=yellow** 상태 차이가 hash에 영향 줄 수 있다. Metadata yaml L267에 `es_cluster_status: yellow`가 고정 기록되어 있으므로 ES가 green으로 전환되면 hash 불일치 발생 — Tester는 ES 상태 변동을 감안해 "본문 섹션 A~E 핵심 컨텐츠의 diff" 기준으로 재현성 판정할 것을 권고.

---

## 최종 판정

**NEEDS_REVISION** — Manager가 task-board.md L250의 체크 (3) "65건"을 "61건"으로 교정한 뒤 Reviewer를 재호출할 것. 선택 수정 2번은 반영 여부 Manager 재량.
