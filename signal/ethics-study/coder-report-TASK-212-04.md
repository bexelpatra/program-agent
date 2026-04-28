---
agent: coder
task_id: TASK-212-04
status: DONE
severity: observation
timestamp: 2026-04-28T13:00:00
---

## 결과 요약

천태 지의 (天台 智顗 · Zhiyi, 538-597) ES 등록 완료 (TASK-212-04). 단일 사상가 등록으로 **2 BLOCKER 동시 해소** (BLK-175E-2022A-006 + BLK-175E-2025A-004) — TASK-212 시리즈 2번째 사례 (regan DQ-027 선례 답습).

- **ES 등록**: 1 thinker (zhiyi · field=eastern_ethics · era=고대) + 1 work (zhiyi-tiantai-3-1 · 천태 3대부) + 6 claims (zhiyi-claim-001~006) + 6 keywords + 2 relations.
- **study-guide 정정**: 2022-A.md 6 곳 (L20·L715·L752·L772·L788·L1002) + 2025-A.md 7 곳 (L19·L40·L50·L52·L415·L434·L445) → 13 line 일괄 정정.
- **DQ-028 override 등재**: data-quality-log.md DQ-027 entry 직후 append. 2 BLOCKER 동시 해소 명시 (TASK-212 시리즈 2번째).
- **자기검증 3-step**: Step 1 ∩ Step 1b ∩ Step 2 = 0 (disjoint) · 모든 영문/Greek/macron 토큰 verbatim 출처 보유 (fabrication 0-hit) · fudge 0-hit.

## 변경된 파일

- **신규**: `projects/ethics-study/scripts/insert_zhiyi.py` (insert_regan.py 모범 사례 답습 · 동일 함수 시그니처: ensure_field/insert_thinker/insert_works/insert_claims/insert_keywords/insert_relations)
- **수정**: `projects/ethics-study/exam-solutions/study-guide/2022-A.md` (L20·L715·L752·L772·L788·L1002 6 곳)
- **수정**: `projects/ethics-study/exam-solutions/study-guide/2025-A.md` (L19·L40·L50·L52·L415·L434·L445 7 곳)
- **수정**: `signal/ethics-study/data-quality-log.md` (DQ-028 entry append · DQ-027 직후)

## ES 검증 (curl 실측 2026-04-28)

```bash
curl -s -o /dev/null -w "%{http_code}\n" "http://localhost:9200/ethics-thinkers/_doc/zhiyi"
# 200

curl -s "http://localhost:9200/ethics-claims/_search?q=thinker_id:zhiyi&size=0" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['hits']['total']['value'])"
# 6

curl -s "http://localhost:9200/ethics-relations/_search?q=zhiyi&size=0" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['hits']['total']['value'])"
# 2
```

| 검증 항목 | 결과 |
|---|---|
| `_doc/zhiyi` HTTP | 200 |
| claims total (q=thinker_id:zhiyi) | 6 |
| works | 1 (zhiyi-tiantai-3-1 · 천태 3대부) |
| keywords | 6 |
| relations | 2 (zhiyi→wonhyo influenced · zhiyi→huineng parallel) |

### Claim 6중 매핑 (trademark 보존)

| ID | 핵심 trademark | 출제 출처 |
|---|---|---|
| zhiyi-claim-001 | 삼제원융 (三諦圓融) | 2025-A Q8 (L339·L347) |
| zhiyi-claim-002 | 일심삼관 (一心三觀) | 2025-A Q8 (L339·L347) |
| zhiyi-claim-003 | 오시 교판 (五時) | 2022-A Q10 + 2025-A Q8 (L347) |
| zhiyi-claim-004 | 화법 4교 (化法四敎) | 2025-A Q8 (L341·L347) |
| zhiyi-claim-005 | 화의 4교 (化儀四敎) | 2025-A Q8 (L341·L347) |
| zhiyi-claim-006 | 일념삼천 (一念三千) | 2025-A Q8 (L347) |

### Keyword 6중 매핑

| keyword id | term | term_en | 출처 |
|---|---|---|---|
| kw-zhiyi-three-truths-fusion | 삼제원융 | three truths perfect harmony | coverage/2025-A.md L347 verbatim |
| kw-zhiyi-one-mind-three-contemplations | 일심삼관 | three contemplations in one mind | coverage/2025-A.md L347 verbatim |
| kw-zhiyi-five-periods | 오시 교판 | five periods and eight teachings | coverage/2025-A.md L347 verbatim |
| kw-zhiyi-four-doctrinal-teachings | 화법 4교 | "" (영문 verbatim 출처 부재 — 한글 단독, fabrication 회피) | coverage/2025-A.md L347 |
| kw-zhiyi-four-formal-teachings | 화의 4교 | "" (영문 verbatim 출처 부재 — 한글 단독, fabrication 회피) | coverage/2025-A.md L347 |
| kw-zhiyi-three-thousand-realms | 일념삼천 | three thousand realms in a single thought-moment | coverage/2025-A.md L347 verbatim |

## 자기검증 3-step 결과 표

### Step 1 — bare-paren `\([A-Za-z][^)]*\)` 추출 (insert_zhiyi.py 본문)

raw 98건 추출 → Python code/index= 메타/BLK ID/file path 제외 → 콘텐츠 27 unique.

콘텐츠 27 unique 분류:
- **메타 marker** (코드/태스크/내부 라벨): `(claims)` `(client)` `(field)` `(keywords)` `(relations)` `(thinker)` `(works)` `(verbatim only)` `(fabrication 회피)` `(fabrication 후보 제거)` `(TitleCase 영문 wrap만 — coverage hit 토큰)` `(zhiyi 토큰 ∩=0 확증, coder report 적재)` `(TASK-212-05 등록 후 추가 권고)` `(TASK-212-10 등록 후 추가 권고)` `(agents/coder.md §원문/입력 인용 규칙)` (15 마커)
- **출처 인용 marker**: `(coverage/2022-A.md L24)` `(coverage/2025-A.md L339)` `(coverage/2025-A.md L341)` `(coverage/2025-A.md L347)` `(field=eastern_ethics · era=고대 — wonhyo·jinul ES 실측 동일 패턴)` `(wonhyo·jinul·confucius 등 등록 확인됨)` (6 마커)
- **출제 범위 marker**: `(Q10 single row)` `(Q10 single row · 102 lines 한정)` `(Q10 single row · 102 lines 한정 · trademark 압축 인라인)` `(Q8 통합 범위)` `(Q8 본문+분석 통합 범위)` `(Q8 발문 + 사상가 메타 + 한자 병기 + 분석 통합 범위)` (6 마커)

**user-facing 영문 콘텐츠 토큰 (Step 1): 0건**. 모든 paren 매칭은 코드 메타·출처 인용·출제 범위 라벨로 분류되어 `subject-of-a-life`·`Animal Liberation` 같은 사상가 trademark 영문 토큰은 0건 — zhiyi 영역은 한자 + 한글 verbatim 영역으로 trademark 영문 토큰을 가지지 않음 (wonhyo/jinul ES 실측 동일 패턴).

**Step 1 fabrication: 0/0 (대상 없음 — vacuously true)**

### Step 1b — Greek `[Α-Ωα-ω]` / macron `[\u0100-\u024F]` 추출

```bash
python3 -c "
import re
with open('projects/ethics-study/scripts/insert_zhiyi.py','r',encoding='utf-8') as f: c=f.read()
for m in re.finditer(r'\S*[\u0370-\u03FF\u0100-\u024F]+\S*', c): print(m.group())
"
# 1) `[Α-Ωα-ω]`           ← Step 1b 정규식 패턴 자체 (docstring 메타)
# 2) (śamatha·vipaśyanā    ← docstring 메타 토큰 인용
# 3) śamatha-vipaśyanā)`)  ← docstring 메타 토큰 인용
```

| 토큰 | coverage/2025-A.md L347 | 비고 |
|---|---|---|
| `śamatha-vipaśyanā` | yes — `止觀(지관 — śamatha-vipaśyanā)` verbatim | docstring 출처 marker로만 인용 (사용자-노출 콘텐츠 0) |
| `[Α-Ωα-ω]` | n/a | 정규식 패턴 자체 (메타) |

**Step 1b user-facing 콘텐츠 토큰: 0건** (docstring 메타 인용만). verbatim 출처 보유 100% (1/1).

### Step 2 — TitleCase `[A-Z][a-z]+(\s+[A-Za-z][a-z]+){1,5}` 추출

unique 2건:

| 토큰 | 분류 | coverage 출처 |
|---|---|---|
| `Tiantai school` | user-facing 콘텐츠 | coverage/2025-A.md L345 verbatim |
| `Exception as` | Python try/except 구문 | n/a (코드 syntax) |

`Exception as` (Python try/except 구문) 제외 후 콘텐츠 토큰 1개 — verbatim 출처 보유 100% (1/1).

### Disjoint 산술

| 집합 | 콘텐츠 토큰 수 |
|---|---|
| Step 1 (콘텐츠 영문 trademark) | 0 |
| Step 1b (Greek/macron user-facing) | 0 (docstring 메타 인용만) |
| Step 2 (TitleCase 콘텐츠) | 1 (`Tiantai school` only) |
| Step 1 ∩ Step 1b | 0 (Step 1·Step 1b 모두 공집합) |
| Step 1 ∩ Step 1b ∩ Step 2 | **0 ✓** (3-fold 교집합 공집합) |

### fudge·fabrication 검증

```bash
grep -nE '≈|수렴|중복 보정|대략|얼추|거의' projects/ethics-study/scripts/insert_zhiyi.py
# (no output)
```

- **fudge 검증**: `≈`·`수렴`·`중복 보정`·`대략`·`얼추`·`거의` → insert_zhiyi.py 본문 0-hit 확증.
- **fabrication 검증**: 모든 paren 콘텐츠 영문 토큰 0건 (zhiyi 영역 한자+한글 verbatim — Step 1 vacuously true) + Step 1b 1건 (`śamatha-vipaśyanā`) coverage/2025-A.md L347 verbatim 보유 + Step 2 1건 (`Tiantai school`) coverage/2025-A.md L345 verbatim 보유. 출처 부재 영문 토큰 0건 (term_en 초안 3건 — `five periods classification` · `four teachings by content` · `four teachings by form` — grep 0-hit 확인 후 사전 제거 · `four-doctrinal-teachings`·`four-formal-teachings`는 term_en="" 빈 문자열 처리하여 fabrication 회피).

## 2 BLOCKER 동시 해소

- **BLK-175E-2022A-006** (2022-A Q10 · 1회째 출제 · 화엄·천태 비교 single row · 102 lines 한정 trademark 압축 인라인) — 해소
- **BLK-175E-2025A-004** (2025-A Q8 · 2회째 출제 · 3년 단절 후 재등장 · 삼제원융·일심삼관·화법4교·화의4교 4중 trademark) — 해소

단일 사상가 (zhiyi) ES 등록으로 2 BLOCKER 동시 해소 — TASK-212 시리즈 2번째 사례 (regan DQ-027 선례 답습). 동양윤리 불교 종학 영역 ES 커버리지 확장: 천태 지의 (교학 정점) 등록 완료 — 후속 fazang (화엄종 · TASK-212-05) + huineng (선종 · 등록 확인됨) 와 더불어 중국 불교 종파 3대 축 (천태·화엄·선) 체계화 진행.

## 이슈/블로커

없음. ES HTTP 200 + 6 claims + 2 relations 검증 완료. 13 line study-guide 정정 + DQ-028 override 등재 완료. 자기검증 3-step ∩=0 산술 확증 (vacuously: Step 1=0, Step 1b user-facing=0, Step 2 콘텐츠=1).

## 다음 제안

1. **TASK-212 mother 잔존 ES 보강 시리즈 진행**: TASK-212-05 (fazang · 화엄종) 후속 권고 — zhiyi relation rel-zhiyi-huineng-parallel-2 evidence 에서 명시한 "화엄(法藏) + 천태(智顗) + 선(慧能)이 중국 불교 종파 체계화의 3대 축" 3축 완성을 위해 fazang ES 등록 우선순위.
2. **TASK-212-10 (nagarjuna · 龍樹/용수) 후속 권고**: zhiyi 삼제원융이 인도 나가르주나 이제(二諦)에 중제(中諦)를 더한 확장임 — nagarjuna ES 미등록 시 zhiyi 사상사 맥락 (인도 중관 → 중국 천태 계보) BLOCKER 발생 가능. zhiyi → nagarjuna influenced relation 적재 보류 (TASK-212-10 등록 후 추가 권고).
3. **task-board.md 갱신**: TASK-212-04 → DONE · BLK-175E-2022A-006 + BLK-175E-2025A-004 → 해소 (Manager 작업).
4. **단일 등록 다 BLOCKER 해소 패턴 누적 통계**: TASK-212 시리즈 12 sub-task 중 2건 (regan + zhiyi) = 16.7% 가 1-등록 2-해소 효율 패턴. cho_sik (DQ-025 · 1 BLOCKER) · schumpeter (DQ-026 · 1 BLOCKER) 와 비교 시 출제 빈도 ≥2 사상가가 효율적 후보임을 재확증.
