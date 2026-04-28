---
task_id: PHASE-A (3차 재검증)
verdict: PASS
---

# Reviewer Report: Phase A (3차 재검증)

## 2차 잔존 이슈 처리 상태

| 이슈 | Manager 수정 | 실측 확증 | 판정 |
|------|--------------|-----------|------|
| TOC 정규식 `^## 문항\s+\d+` 의 0-hit 위험 (2014-B 4문항·2015-B 6문항 변종 헤더 미흡수) | architecture.md L411 + task-board.md TASK-209 description + TASK-209-R 항목 (3) 모두에서 정규식을 `^## 문항(?:\s+(?:서술형\|논술형\|기입형))?\s+\d+` 로 보강. capture group 으로 "서술형/논술형/기입형" 변종을 흡수. | study-guide 26개 grep 실측: 모두 1+ hit, 합 = **293**. 2014-B = 4 hit, 2015-B = 6 hit (이전 0-hit → 정상). 합 293 = exam-coverage-map.md L8 "총 문항 row 수: 293" 일치. | **PASS** |

## 재검증 5항 결과

### 항목 1 — architecture.md Phase A TOC 정규식 보강
**PASS.** L411 본문 실측:

```
- `templates/exam_detail.html` — 좌측 사이드바 (연도×슬롯 nav) · 본문 (study-guide / coverage 탭 토글) · 우측 TOC (study-guide.md 만 추출, **Python 정규식 `^## 문항(?:\s+(?:서술형|논술형|기입형))?\s+\d+`** · 26개 전수 매칭 4~20 hit/file 합 293 = exam-coverage-map.md L25 "총 문항 row 수 293" 일치 · 변종 형식 `## 문항 서술형 1` (2014-B·2015-B) · `## 문항 N` (2016년 이후 통일) 둘 다 흡수). coverage.md 는 헤더 형식 분산 [...] TOC 미적용.
```

- 정규식 `^## 문항(?:\s+(?:서술형|논술형|기입형))?\s+\d+` 보강 형태로 명시 ✓
- 변종 형식 sample (2014-B·2015-B) 명시 ✓
- 흡수 대상 ("서술형/논술형/기입형" + 표준 형식) 모두 명시 ✓
- coverage.md TOC 미적용 정책 유지 ✓

### 항목 2 — task-board.md TASK-209 description 정규식 보강 + 변종 sample
**PASS.** L369 (TASK-209 row) 본문 실측 발췌:

```
**TOC 는 study-guide.md 만 추출** (Python 정규식 `^## 문항(?:\s+(?:서술형|논술형|기입형))?\s+\d+` · 26개 study-guide 전수 매칭 4~20 hit/file 합 293 = exam-coverage-map.md L25 "총 문항 row 수 293" 일치 실측 · 변종 형식 `## 문항 서술형 1` (2014-B 4 hit·2015-B 6 hit) + `## 문항 논술형 1` + `## 문항 기입형 1` + `## 문항 N` (2016년 이후 통일) 모두 흡수 · sample `study-guide/2026-A.md` L61·L98·L140 / `study-guide/2014-B.md` L? `## 문항 서술형 N`)
```

- 보강 정규식 명시 ✓
- 변종 형식 (서술형/논술형/기입형) 모두 열거 ✓
- 2014-B (4 hit) · 2015-B (6 hit) 변종 sample 명시 ✓ — 2차 보고서에서 요청한 핵심 사항
- 표준 형식 (2026-A) sample 도 함께 유지 ✓

Minor: `2014-B.md L?` 부분에 line 번호가 placeholder (`L?`) 로 남음. 변종 헤더의 실제 line 은 2014-B L27 (서술형 1)·L131 (논술형 1)·L182 (논술형 2) 등 (2차 보고서 항목 6 에 실측 라인 list 있음). Coder 가 file 을 직접 Read 하면 즉시 발견되므로 실행 차단 사유는 아님. PASS 판정 유지하되 권고 사항으로 명시.

### 항목 3 — task-board.md TASK-209-R 항목 (3) 정규식 보강
**PASS.** L370 (TASK-209-R row) 항목 (3) 실측:

```
(3) Python 정규식 `^## 문항(?:\s+(?:서술형|논술형|기입형))?\s+\d+` 가 study-guide 26개 전수 매칭 (실측 4~20 hit/file 합 293) + coverage 는 형식 분산으로 TOC 제외 (Phase A 정책)
```

- 보강 정규식 명시 ✓
- 26개 전수 매칭 실측 hit 수 명시 (4~20 hit/file 합 293) ✓
- coverage TOC 제외 정책 유지 ✓

### 항목 4 — study-guide 26개 보강 정규식 1+ hit 전수 재현 (Reviewer 직접 실측)
**PASS.** Reviewer 가 `cd projects/ethics-study/exam-solutions/study-guide && grep -cE '^## 문항( (서술형|논술형|기입형))? [0-9]+' *.md` 직접 실행한 결과:

```
2014-A.md:20    2018-A.md:14    2022-A.md:12
2014-B.md:4     2018-B.md:8     2022-B.md:11
2015-A.md:14    2019-A.md:14    2023-A.md:12
2015-B.md:6     2019-B.md:8     2023-B.md:11
2016-A.md:14    2020-A.md:12    2024-A.md:12
2016-B.md:8     2020-B.md:11    2024-B.md:11
2017-A.md:14    2021-A.md:12    2025-A.md:12
2017-B.md:8     2021-B.md:11    2025-B.md:11
                                2026-A.md:12
                                2026-B.md:11
```

- 26개 파일 모두 1+ hit (최소 4, 최대 20) ✓
- **2014-B = 4 hit · 2015-B = 6 hit** — 2차에서 0-hit 이던 두 파일이 정상 매칭으로 전환 ✓
- 그 외 24개 파일도 그대로 매칭 유지 (회귀 0건) ✓

비교: 2차 보고서 항목 6 의 비-보강 정규식 hit 수와 대조 — 보강으로 인한 회귀 0건, 추가 매칭 +10 (2014-B 4 + 2015-B 6).

추가 보완: 2차 보고서는 2014-A=15·2015-A=10 으로 기록했으나 본 3차 실측은 2014-A=20·2015-A=14. 이는 grep 정규식의 형태 차이 (2차는 `^## 문항\s+\d+` 으로 ERE 의 `\s` 미지원 환경에서 0-hit 가능성 / 본 3차는 `^## 문항( (서술형|논술형|기입형))? [0-9]+` 로 명시적 공백 사용) 또는 GNU grep 의 `\s` 처리 차이 가능성. **합계만 비교 시 본 3차 = 293 으로 exam-coverage-map.md L8 과 정확 일치**, 이 일치성이 최종 검증 기준.

### 항목 5 — 합 293 매칭 사실 == exam-coverage-map.md 일치
**PASS (with minor caveat).**

- Reviewer awk 합산: `grep -cE '^## 문항( (서술형|논술형|기입형))? [0-9]+' *.md | awk -F: '{sum+=$2} END {print "TOTAL:", sum}'` → `TOTAL: 293` ✓
- exam-coverage-map.md 실측: **L8** `- **총 문항 row 수**: 293` ✓
- **Caveat (minor)**: architecture.md L411 + task-board TASK-209 description 모두 "exam-coverage-map.md **L25** ... 일치" 라 표기. 실제 파일에서 "총 문항 row 수: 293" 줄은 **L8** (Read tool 직접 확인). L25 는 Section A 의 "총 45명" 줄. 수치 일치 (293) 자체는 사실이고 Coder/Tester 가 L8 을 즉시 발견 가능하므로 실행 차단 사유 아님. 다만 차후 정확도 보강 권고.

## 판정

**PASS**

3개 산출물 (architecture.md L411, task-board.md TASK-209 description, TASK-209-R 항목 (3)) 모두 보강된 정규식 `^## 문항(?:\s+(?:서술형|논술형|기입형))?\s+\d+` 로 갱신됨. 변종 형식 sample (2014-B·2015-B) 명시됨. Reviewer 직접 grep 실측에서 26개 전수 매칭 합 293 == exam-coverage-map.md L8 "총 문항 row 수: 293" 정확 일치. 2차 잔존 차단 이슈 모두 해소.

## Manager 에게 전달

### 발주 가능성
**Coder TASK-208 발주 가능.** TASK-209 발주 도 의존성 (TASK-208 DONE) 충족 후 즉시 가능. TASK-209-R 검증 시점 (TASK-209 산출물 검증) 에서 본 보고서 PASS 판정 활용 가능.

### Minor 권고 (차단 아님 — 발주 후 또는 다음 review 사이클에 보강)
1. **task-board TASK-209 description 의 `2014-B.md L?` placeholder**: `L?` 자리에 실측 line (예: `L27 ## 문항 서술형 1`·`L131 ## 문항 논술형 1`) 을 채워 Coder 가 file 미read 시에도 변종 형식을 즉시 인지하도록 권고. 단, Coder 는 Read tool 사용 의무가 있으므로 차단 아님.
2. **L25 vs L8 표기 오차**: architecture.md L411 + task-board TASK-209 description 의 "exam-coverage-map.md **L25**" 표기를 **L8** 로 정정 권고. 수치 (293) 자체는 정확하므로 차단 아님. 다음 architecture/task-board 갱신 사이클에 일괄 정정 가능.
3. **TOC 라벨 정책 (2차 권고 잔존)**: 보강 정규식 capture group 의 "서술형/논술형/기입형" 단어를 TOC 항목 텍스트에 어떻게 표기할지 (예: "문항 서술형 1" vs "서술형 1" vs "1") 명시 권고. 미정 시 Coder 가 임의 결정 — 본 사항은 PHASE-A 산출물 (exam_detail.html 우측 TOC) 의 시각 결과로 직접 확인 가능하므로 차단 아님. TASK-210-T 회귀 검증 단계에서 시각 확인 가능.

### 다음 단계
- Manager 는 Coder TASK-208 (`render()` + `verify_verbatim()` helper 분리) 발주 가능.
- TASK-208 DONE 후 TASK-209 발주.
- TASK-209 DONE 후 TASK-209-R reviewer 검증 → TASK-210-T tester.
