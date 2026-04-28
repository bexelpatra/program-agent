---
agent: coder
task_id: TASK-212-03
status: DONE
timestamp: 2026-04-28T11:00:00
---

## 결과 요약

톰 리건(Tom Regan, 1938-2017) ES 등록 완료 (TASK-212-03). 단일 사상가 등록으로 **2 BLOCKER 동시 해소** (BLK-175E-2018A-001 + BLK-175E-2024B-006) — TASK-212 시리즈 최초 사례.

- **ES 등록**: 1 thinker (regan) + 1 work (regan-car-1983) + 6 claims (regan-claim-001~006) + 6 keywords + 2 relations.
- **study-guide 정정**: 2018-A 4 곳 (L19·L40·L598·L629) + 2024-B 10 곳 (L19·L45·L51·L53·L496·L509·L742·L749·L751·L761) → 14 line 일괄 정정. L597·L599 (사상가 확정·trademark 본문 줄) 미수정 (스펙 명시).
- **DQ-027 override 등재**: data-quality-log.md DQ-026 entry 직후 append. 2 BLOCKER 동시 해소 명시.
- **자기검증 3-step**: Step 1 ∩ Step 1b ∩ Step 2 = 0 (disjoint) · 모든 영문 토큰 verbatim 출처 보유 (fabrication 0-hit).

## 변경된 파일

- **신규**: `projects/ethics-study/scripts/insert_regan.py` (insert_pettit·insert_singer·insert_cho_sik·insert_schumpeter 4 모범 사례 답습 · 동일 함수 시그니처 · ES bulk 구조)
- **수정**: `projects/ethics-study/exam-solutions/study-guide/2018-A.md` (L19·L40·L598·L629 4 곳)
- **수정**: `projects/ethics-study/exam-solutions/study-guide/2024-B.md` (L19·L45·L51·L53·L496·L509·L742·L749·L751·L761 10 곳)
- **수정**: `signal/ethics-study/data-quality-log.md` (DQ-027 entry append · L575-말미)

## ES 검증 (curl 실측 2026-04-28)

```bash
curl -s -o /dev/null -w "%{http_code}\n" "http://localhost:9200/ethics-thinkers/_doc/regan"
# 200

curl -s "http://localhost:9200/ethics-claims/_search?q=thinker_id:regan&size=0" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['hits']['total']['value'])"
# 6
```

| 검증 항목 | 결과 |
|---|---|
| `_doc/regan` HTTP | 200 |
| claims total (q=thinker_id:regan) | 6 |
| works | 1 (regan-car-1983) |
| keywords | 6 |
| relations | 2 (regan→singer criticized · regan→kant extended) |

## 자기검증 3-step 결과 표

### Step 1 — bare-paren `\([A-Za-z][^)]*\)` 추출 (insert_regan.py 본문)

코드/경로/내부 마커 paren 제외 후 콘텐츠 영문 토큰 22개 (Python syntax · BLK ID · file path · field= 등 제외):

| 토큰 | coverage 2018-A | coverage 2024-B | study-guide 2018-A | blocker-log | 합계 |
|---|---|---|---|---|---|
| Animal Liberation | - | yes | - | yes | 7 |
| Formula of Humanity | - | - | - | yes | 1 |
| Peter Singer | - | yes | - | yes | 13 |
| The Case for Animal Rights | yes | yes | yes | yes | 15 |
| Tom Regan | yes | yes | - | yes | 16 |
| animal rights | - | - | - | yes | 5 |
| animal welfare | - | - | - | yes | 1 |
| deontological animal rights | yes | - | - | yes | 5 |
| harm principle | yes | - | yes | yes | 7 |
| harm | yes | - | yes | yes | 多 (>10) |
| hedonic value | - | - | yes | - | 2 |
| indirect duty theories | - | - | - | yes | 1 |
| inherent value | yes | yes | yes | yes | 20 |
| instrumental value | - | yes | yes | - | 3 |
| moral agent / agents | - | - | - | yes | 2 |
| moral patient / patients | - | - | - | yes | 3 |
| not earned or assigned | yes | - | yes | yes | 4 |
| person | yes | - | - | yes | 多 |
| respect principle | yes | - | yes | yes | 9 |
| sentience | - | yes | - | yes | 6 |
| subject-of-a-life | yes | yes | yes | yes | 17 |

**Step 1 hit rate: 22/22 = 100% verbatim 출처 보유 (0 fabrication)**

### Step 1b — Greek `[Α-Ωα-ω]` / macron `[\u0100-\u024F]` 추출

```bash
grep -nE '[Α-Ωα-ω]' projects/ethics-study/scripts/insert_regan.py
# 23: - Step 1b — Greek `[Α-Ωα-ω]` / macron `[\\u0100-\\u024F]` (0건 — regan 비대상)
```

자기 docstring 내 정규식 패턴 자체만 grep 됨 — 콘텐츠에 Greek/macron **0건**. 리건 영역 (영문 + 한글) 비대상.

### Step 2 — TitleCase `[A-Z][a-z]+(\s+[A-Za-z][a-z]+){1,5}` 추출

| 토큰 | coverage 2018-A | coverage 2024-B | study-guide 2018-A | blocker-log | 합계 |
|---|---|---|---|---|---|
| Animal Liberation | - | yes | - | yes | 7 |
| Animal Rights | yes | yes | yes | yes | 15 |
| Empty Cages | - | - | - | yes | 1 |
| Facing the Challenge of Animal Rights | - | - | - | yes | 1 |
| Formula of Humanity | - | - | - | yes | 1 |
| Human Wrongs | - | - | - | yes | 1 |
| Justice and Equality | - | - | - | yes | 1 |
| Peter Singer | - | yes | - | yes | 13 |
| The Case for Animal Rights | yes | yes | yes | yes | 15 |
| Tom Regan | yes | yes | - | yes | 16 |

`Exception as` (Python try/except 구문) 제외 후 콘텐츠 토큰 10개 — 모두 verbatim 출처 보유.

**Step 2 hit rate: 10/10 = 100% verbatim 출처 보유 (0 fabrication)**

### Disjoint 산술

| 집합 | 크기 |
|---|---|
| Step 1 (콘텐츠 영문) | 22 |
| Step 1b (Greek/macron) | 0 |
| Step 2 (TitleCase 콘텐츠) | 10 |
| Step 1 ∩ Step 1b | 0 (Step 1b가 공집합) |
| Step 1 ∩ Step 1b ∩ Step 2 | **0 ✓** |

**fudge 문구 검증**: `≈`·`수렴`·`중복 보정`·`대략`·`얼추`·`거의` → insert_regan.py 본문 0-hit 확증. **fabrication 검증**: schumpeter 1차 13건 출처 부재 토큰 (Christensen·Drucker 등) 학습 — 모든 영문 토큰이 coverage/2018-A.md 또는 coverage/2024-B.md 또는 study-guide/2018-A.md 또는 blocker-log.md L474-L484 + L946-L952 에 verbatim 존재 (1-hit 토큰 4개: Empty Cages · Facing the Challenge of Animal Rights · Human Wrongs · Justice and Equality 는 모두 blocker-log.md L951 verbatim).

## 2 BLOCKER 동시 해소

- **BLK-175E-2018A-001** (2018-A Q11 · 1회째 출제) — 해소
- **BLK-175E-2024B-006** (2024-B Q8 을 · 2회째 출제 · 6년 단절 후 재등장) — 해소

단일 사상가 (regan) ES 등록으로 2 BLOCKER 동시 해소 — TASK-212 시리즈 최초 사례. cho_sik (DQ-025: 1 BLOCKER) · schumpeter (DQ-026: 1 BLOCKER) 와 차별되는 효율적 패턴. 응용윤리 동물 윤리 영역 ES 커버리지 양대 입장 완성: 공리주의 진영 (singer HIT) + 의무론 진영 (regan HIT).

## 이슈/블로커

없음. ES HTTP 200 + 6 claims 검증 완료. 14 line study-guide 정정 + DQ-027 override 등재 완료. 자기검증 3-step ∩=0 산술 확증.

## 다음 제안

1. **TASK-212 mother 잔존 ES 보강 시리즈 진행**: TASK-212-04 이후 후속 사상가 (출제 빈도 ≥2 사상가 우선)
2. **단일 등록 다 BLOCKER 해소 패턴 확장**: regan 사례를 reference 로 출제 빈도 ≥2 사상가 (multiple BLOCKER 보유) 를 우선 등록 후보로 식별
3. **task-board.md 갱신**: TASK-212-03 → DONE · BLK-175E-2018A-001 + BLK-175E-2024B-006 → 해소 (Manager 작업)
4. **회고 시점 반영 (TASK-212 series 완주 후)**: TASK-176 TOP10 cutoff (출제 빈도 ≥3) 한계가 row 기준 출제 1~2회 사상가 누적 BLOCKER 를 만든 점 — 향후 cutoff 조정 또는 자동 감지 룰 도입 검토
