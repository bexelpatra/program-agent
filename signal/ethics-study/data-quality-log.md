# Data Quality Log

원본 coverage md 입력 파일의 포맷·escaping·사실 정합성 이슈 추적.
`TASK-DQ-*` prefix 태스크로 별도 관리. append-only.

---

### TASK-DQ-001 - 2026-04-22T02:25
- files:
  - `projects/ethics-study/exam-solutions/coverage/2020-B.md` (Q11)
  - `projects/ethics-study/exam-solutions/coverage/2021-A.md` (Q5)
  - `projects/ethics-study/exam-solutions/coverage/2022-A.md` (Q10)
- issue: 원문 인용 셀에 unescaped `|` 3건 → Markdown pipe table 파싱 깨짐. `merge_coverage.py`가 row-level fallback으로 thinker_id만 복구했으나 Section C 원문 셀 표시는 부정확.
- impact: `exam-coverage-map.md` Section C의 해당 3행에서 원문 인용이 잘린 채 표시됨. 핵심 집계(Section A/B 출제횟수, Section D TOP10, Section E 배점)에는 영향 없음. MERGE-FIX Tester 회귀 8/8 PASS로 확인.
- detected_by: TASK-175E-MERGE-T (MERGE 스크립트 검증 단계)
- resolution: 원본 수정 금지 규정으로 현재는 기록만. 배치 정정 시 `|`를 `\|`로 치환 후 `merge_coverage.py` 재실행 필요.

### TASK-DQ-002 - 2026-04-22T02:25
- file: `projects/ethics-study/exam-solutions/coverage/2021-A.md`, `2023-A.md`, `2024-B.md`
- issue: blasi(아우구스토 블라시) 생몰연도가 coverage 파일 간 상호 모순.
  - 2021-A.md L20: 1935-2016
  - 2023-A.md L561: 1931-2013
  - 2024-B.md: (명시 없음, ES 등록치 1936-2014와 일반 정합)
- impact: 출제 해설 생몰연도 표기 부정확. Wikipedia/신콜버그주의 문헌상 통상 1936년생 기준이며, ES ethics-thinkers/blasi에는 1936-2014 등록. coverage 인용 정합성에만 영향.
- detected_by: TASK-176-02-T (blasi ES 등록 검증 시 OBS-1)
- resolution: 원본 수정 금지 규정으로 현재는 기록만. 배치 정정 시 1936-2014(ES 등록 근거)로 통일 권장.

### TASK-DQ-003 - 2026-04-22T13:32
- file: `projects/ethics-study/exam-solutions/exam-coverage-map.md` L38
- issue: narvaez(나바에즈·Darcia Narvaez) 행 BLK 열 누락. canonical map 은 `BLK-175E-2024A-002` 1건만 기재했으나 원본 2016-A.md L41 에 `BLK-175E-2016A-004` (2016-A Q9 IEE·4과정 모형·윤리적 전문가 3중 trademark 문항) 실재.
- impact: Section D TOP10 BLK 집계 누락 가능. narvaez 의 2016-A 출제를 BLK 통계에서 놓칠 수 있음. ES 등록(TASK-176-10) 은 coverage grep 실측으로 BLK 2건 모두 해소 확증.
- detected_by: TASK-176-10 (narvaez 스펙 작성 시 Manager)
- resolution: 원본 수정 금지 규정으로 현재는 기록만. 배치 정정 시 `merge_coverage.py` 의 BLK 자동 수집 로직 점검 + canonical L38 수동 보완 권장.

### TASK-DQ-004 - 2026-04-22T13:32
- file: `projects/ethics-study/exam-solutions/coverage/2024-A.md` L274 vs `projects/ethics-study/exam-solutions/coverage/2026-B.md` L223
- issue: narvaez(Darcia Narvaez) 생년 coverage md 간 상충.
  - 2024-A.md L274: "1952~" (서술형 해설)
  - 2026-B.md L223: "(1955-)" (괄호 표기)
- impact: 출제 해설 생년 부정확. 실제 Darcia Narvaez 는 1952년생 (University of Notre Dame 공식 프로필 기준). ES ethics-thinkers/narvaez 에는 1952-null 등록 (TASK-176-10 시 2024-A 채택).
- detected_by: TASK-176-10 (Coder(Opus) 자기검증 + Tester TASK-176-10-T obs-2)
- resolution: 원본 수정 금지 규정으로 현재는 기록만. 배치 정정 시 2026-B.md L223 "(1955-)" → "(1952-)" 로 통일 권장. 유사 패턴(타 사상가 생몰연도 상충)은 TASK-DQ-002 (blasi) 와 더불어 체크리스트화 필요.

### TASK-DQ-005 - 2026-04-22T13:32
- files: `projects/ethics-study/exam-solutions/coverage/*.md` 전반
- issue: coverage md 는 한글 해설 압축본이라, 원어 영어 개념어가 다수 0-hit 으로 기재됨. narvaez 등록 과정에서 Coder(Opus) 자기검증 루프가 6건 제거: `Just Community`, `automaticity`, `embodied cognition`, `engagement distress`, `inductive discipline`, `social intuitionism`. Tester 추가 발견 3건: `safety ethic`, `engagement ethic`, `moral foundations theory` (소문자).
- impact: Coder 가 "원문 grep 0건 고유명 금지" 규정을 준수하려면 자기검증 루프에 **case-sensitive 전수 역grep** 강제 필요. `\([A-Za-z][^)]*\)` regex 는 괄호 안 토큰만 캐치 → 괄호 밖 영어 phrase 는 누락.
- detected_by: TASK-176-10 (Coder 자기검증) + TASK-176-10-T (Tester 역grep)
- resolution: 향후 agents/coder.md 에 "자기검증 루프 2단계: (1) 괄호 안 영어 토큰 추출 (2) 본문 영어 phrase 전수 역grep" 규약 추가 제안. retrospective 회고 항목.

### TASK-DQ-006 - 2026-04-22T14:55
- file: `projects/ethics-study/exam-solutions/coverage/2014-A.md` L37-L45
- issue: "불확실·블로커 row" 섹션의 "ES 사상가 누락" 목록에 **bandura(L40)·turiel(L44) 2건이 잘못 포함**. TASK-176-05 (bandura, 2026-04-22 DONE) · TASK-176-08 (turiel, 2026-04-22 DONE) 이후 두 사상가 모두 ES `found=true` 로 등록되어 있음. 당시 coverage 작성 시점(2026-04-18 이전) 에는 미등록이 정확했으나, TOP10 MISS 등록 후 coverage md 업데이트 미반영.
- impact: TASK-182 (2014-A study-guide.md 작성) Coder 가 coverage L40·L44 를 "누락"으로 그대로 transcribe 하면 학생이 오해할 위험. 현재 실제 ⚠️ES 미등록은 L39(CDP)·L41(Nāgārjuna)·L42(Burke)·L43(Machiavelli) 4건만.
- detected_by: TASK-182 Reviewer Round 1 (R-3 지적, 2026-04-22T14:50)
- resolution: 원본 수정 금지 규정으로 현재는 기록만. TASK-182 spec 에 override 규정 명시 — Coder 는 coverage L40·L44 를 ✅ES 등록으로 표기. 배치 정정 시 coverage md 본문 "Elliot Turiel(튜리엘) 사회적 영역 이론 누락" / "Albert Bandura(반두라) 누락" 문구를 "(TASK-176-05/08 DONE 으로 해소)" 주석 추가 권장. 유사 선례 검토: 타 coverage md 에서도 TOP10 MISS 10건 사상가가 "누락"으로 잔존할 가능성 — 26개 파일 전수 검토 필요.

## DQ-007 — 2026-04-22T19:25

- task_id: TASK-DQ-007
- file: `projects/ethics-study/exam-solutions/coverage/2015-B.md` L32-L36
- issue: "불확실·블로커 row" 섹션의 "ES 누락" 목록에 **singer(L32)·durkheim(L33) 2건이 잘못 포함**. 본 세션 2026-04-22 curl 실측으로 `ethics-thinkers/_doc/singer.found=true` (claims=8) · `ethics-thinkers/_doc/durkheim.found=true` (claims=8) 확증. coverage 작성 시점(2026-04-20) 이후 TASK-176 시리즈로 등록됨.
- impact: TASK-185 (2015-B study-guide.md 작성) Coder 가 coverage L32·L33 을 "ES 미등록"으로 그대로 transcribe 하면 학생이 오해할 위험. 현재 실제 ⚠️ES 미등록은 **0건** (본 시험 전수 ES 등록).
- detected_by: TASK-185 Manager spec 작성 시 ES 실측 (2026-04-22T19:25)
- resolution: 원본 수정 금지 규정으로 현재는 기록만. TASK-185 spec 에 override 규정 명시 — Coder 는 coverage L32·L33 을 ✅ES 등록으로 표기. DQ-006 (2014-A bandura·turiel) 선례와 동일 패턴. 배치 정정 시 coverage md 본문 수정 권장. 유사 선례 검토: TASK-DQ-006 에서 제기된 "26개 파일 전수 검토 필요" 권고를 다시 확인 — 2014-A·2015-B 이외 파일에서도 TOP10 MISS 10건 사상가·2014-A 이후 등록된 사상가가 "누락"으로 잔존 가능성.

## DQ-014 — 2026-04-23T02:55

- task_id: TASK-DQ-014
- file: `projects/ethics-study/exam-solutions/coverage/2021-A.md`
- issue: "불확실·블로커 row" 또는 ES 미등록 기록 3건 — **moore (Q3 L55-L60) · blasi (Q6 L95-L107) · taylor_p (Q9 L138-L148)** — 본 세션 2026-04-23 curl 실측으로 전원 `ethics-thinkers/_doc/{id}.found=true` 확증 (moore 7 claims · blasi 8 claims · taylor_p 8 claims). coverage 작성 시점(2026-04-21) 이후 TASK-176 후속 등록 결과로 추정.
- impact: TASK-196 (2021-A study-guide.md) Coder 가 coverage BLOCKER 표기를 그대로 transcribe 하면 study-guide 에 ⚠️ES 미등록이 오표기되어 학생 오해. 현재 실제 ⚠️ES 미등록은 **0건** (본 시험 ES 등록 11 slot · unique 10 thinker 전수 FOUND).
- 동명이인 규약 특기: taylor_p = Paul Taylor (생명중심주의·환경윤리, 1923-2015, 『Respect for Nature』 1986) · taylor = Charles Taylor (공동체주의, 1931-). architecture.md L539-L541 규약. Q9 에서는 `taylor_p` 사용 필수 — `taylor` 또는 `paul_taylor` 금지.
- detected_by: TASK-196 Manager spec 작성 시 ES 실측 (2026-04-23T02:55)
- resolution: 원본 수정 금지 규정으로 현재는 기록만. TASK-196 spec 에 override 규정 명시 — Coder 는 study-guide/2021-A.md 에 moore·blasi·taylor_p 모두 정상 thinker_id + claim_id 사용 (⚠️BLOCKER 표기 없음). 유사 선례 DQ-006·DQ-007·DQ-013 과 동일 패턴. 배치 정정 시 coverage md 본문 수정 권장.

---

## DQ-014 … (skip — 이미 기록됨)

## DQ-015 — coverage/2021-B.md "ES 미등록" 목록 부분 정정 (4 FOUND · 3 NOT_FOUND)

- **ID**: DQ-015
- **관련 태스크**: TASK-197 (2021-B study-guide 작성)
- **file**: `projects/ethics-study/exam-solutions/coverage/2021-B.md`
- **category**: es_state_mismatch (coverage md 작성 시점 이후 ES 상태 변경)
- **coverage 작성일**: 2026-04-21 (TASK-175E-2021-B)
- **본 세션 ES 실측일**: 2026-04-23
- **요약**: coverage/2021-B.md BLOCKER 목록 총 7건(uicheon·jinul·turiel·durkheim·hoffman·kierkegaard·cicero) 중 **4건이 현재 실측에서 FOUND** · 3건 여전히 NOT_FOUND.

### FOUND override 4건 (DQ-015 override · BLOCKER 표기 제거 · 정상 ES 근거 사용)

| thinker_id | 문항 | claim 수 | TASK-176 후속 등록 |
|-----------|------|----------|--------------------|
| jinul | Q1 을 | 9 | 2020-A Q1 선례 재출제, 최우선 등록된 것으로 추정 |
| turiel | Q3 갑 | 8 | 2018-B Q10 재출제, 최우선 등록된 것으로 추정 |
| durkheim | Q4 갑 | 8 | 프랑스 사회학·도덕 교육 3요소, 신규 등록 |
| hoffman | Q5 을 | 8 | 2019-B Q7 재출제, 최우선 등록된 것으로 추정 |

### NOT_FOUND 3건 (study-guide 에 BLOCKER 표기 유지)

| thinker_id | 문항 | status | study-guide 표기 |
|-----------|------|--------|-------------------|
| uicheon | Q1 갑 | 404 | ⚠️ES 미등록 (BLOCKER-1 · BLK-175E-2021B-001) |
| kierkegaard | Q8 을 | 404 | ⚠️ES 미등록 (BLOCKER-2 · BLK-175E-2021B-006) |
| cicero | Q10 | 404 | ⚠️ES 미등록 (BLOCKER-3 · BLK-175E-2021B-007) |

- detected_by: TASK-197 Manager spec 작성 시 ES 실측 (2026-04-23T03:30)
- resolution: 원본 수정 금지 규정으로 현재는 기록만. TASK-197 spec 에 override 규정 명시 — Coder 는 study-guide/2021-B.md 에 jinul·turiel·durkheim·hoffman 모두 정상 thinker_id + claim_id 사용 (⚠️BLOCKER 표기 없음). uicheon·kierkegaard·cicero 3명은 BLOCKER-1~3 유지. 유사 선례 DQ-013·DQ-014 와 동일 패턴.

## DQ-016 — coverage/2022-A.md "ES 미등록" 목록 부분 정정 (3 FOUND · 4 NOT_FOUND)

- **ID**: DQ-016
- **관련 태스크**: TASK-198 (2022-A study-guide 작성)
- **file**: `projects/ethics-study/exam-solutions/coverage/2022-A.md`
- **category**: es_state_mismatch (coverage md 작성 시점 이후 ES 상태 변경)
- **coverage 작성일**: 2026-04-21 (TASK-175E-2022-A)
- **본 세션 ES 실측일**: 2026-04-23
- **요약**: coverage/2022-A.md BLOCKER 총 7건(jinul·pettit·green_th·turiel·shenxiu·zhiyi·beccaria) 중 **3건이 현재 실측에서 FOUND** · 4건 여전히 NOT_FOUND.

### FOUND override 3건 (DQ-016 override · BLOCKER 표기 제거 · 정상 ES 근거 사용)

| thinker_id | 문항 | claim 수 | 비고 |
|-----------|------|----------|------|
| jinul | Q2 | 9 | DQ-015 override 연속 (2021-B 에서도 override) |
| pettit | Q6 (가) | 8 | TASK-176 후속 등록 (2020-A 재출제 선례) |
| turiel | Q8 을 | 8 | DQ-015 override 연속 (2021-B 에서도 override) |

### NOT_FOUND 4건 (study-guide 에 BLOCKER 표기 유지)

| thinker_id | 문항 | status | study-guide 표기 |
|-----------|------|--------|-------------------|
| green_th | Q6 (나) | 404 | ⚠️ES 미등록 (BLOCKER-1 · BLK-175E-2022A-003) |
| shenxiu | Q10 (가) 갑 | 404 | ⚠️ES 미등록 (BLOCKER-2 · BLK-175E-2022A-005) |
| zhiyi | Q10 (나) | 404 | ⚠️ES 미등록 (BLOCKER-3 · BLK-175E-2022A-006) |
| beccaria | Q11 병 | 404 | ⚠️ES 미등록 (BLOCKER-4 · BLK-175E-2022A-007) |

- detected_by: TASK-198 Manager spec 작성 시 ES 실측 (2026-04-23T04:15)
- resolution: 원본 수정 금지. TASK-198 spec 에 override 규정 명시 — Coder 는 study-guide/2022-A.md 에 jinul·pettit·turiel 모두 정상 thinker_id + claim_id 사용 (⚠️BLOCKER 표기 없음). green_th·shenxiu·zhiyi·beccaria 4명은 BLOCKER-1~4 유지. 유사 선례 DQ-014·DQ-015.

## DQ-017 — coverage/2023-A.md "ES 미등록" 목록 부분 정정 (1 FOUND · 5 NOT_FOUND)

- **ID**: DQ-017
- **관련 태스크**: TASK-200 (2023-A study-guide 작성)
- **file**: `projects/ethics-study/exam-solutions/coverage/2023-A.md`
- **category**: es_state_mismatch (coverage md 작성 시점 이후 ES 상태 변경)
- **coverage 작성일**: 2026-04-21 (TASK-175E-2023-A)
- **본 세션 ES 실측일**: 2026-04-23
- **요약**: coverage/2023-A.md BLOCKER 총 6건(tocqueville·viroli·choe_jeu·shweder·choe_chiwon·blasi) 중 **1건이 현재 실측에서 FOUND** · 5건 여전히 NOT_FOUND.

### FOUND override 1건 (DQ-017 override · BLOCKER 표기 제거 · 정상 ES 근거 사용)

| thinker_id | 문항 | claim 수 | 비고 |
|-----------|------|----------|------|
| blasi | Q10 을 | 8 | TASK-176 후속 등록. **2017-A Q2 → 2019-B Q8 → 2021-A Q6 갑 → 2023-A Q10 을 = 4회차 격년 재출제** (coverage/2023-A.md L600·L744·L759 "2020-B 선등록" 표기는 원본 오기로 추정 — 2020-B coverage 에는 blasi 가 Q 답안 사상가로 등장하지 않고 2019-B 복기 언급만 존재. 실측 4회차 이력 기준 기재). hoffman 4연속 2016-A·2019-B·2021-B·2022-B 와 출제 총수 동급이나 격년 패턴. |

### NOT_FOUND 5건 (study-guide 에 BLOCKER 표기 유지)

| thinker_id | 문항 | status | study-guide 표기 |
|-----------|------|--------|-------------------|
| tocqueville | Q3 갑 | 404 | ⚠️ES 미등록 (BLOCKER-1 · BLK-175E-2023A-001) |
| viroli | Q3 을 | 404 | ⚠️ES 미등록 (BLOCKER-2 · BLK-175E-2023A-002) |
| choe_jeu | Q4 | 404 | ⚠️ES 미등록 (BLOCKER-3 · BLK-175E-2023A-003) |
| shweder | Q5 을 | 404 | ⚠️ES 미등록 (BLOCKER-4 · BLK-175E-2023A-004) |
| choe_chiwon | Q6 갑 | 404 | ⚠️ES 미등록 (BLOCKER-5 · BLK-175E-2023A-005) |

- detected_by: TASK-200 Manager spec 작성 시 ES 실측 (2026-04-23T06:30)
- resolution: 원본 수정 금지. TASK-200 spec 에 override 규정 명시 — Coder 는 study-guide/2023-A.md 에 blasi 정상 thinker_id + claim_id 사용 (⚠️BLOCKER 표기 없음). 5명(tocqueville·viroli·choe_jeu·shweder·choe_chiwon)은 BLOCKER-1~5 유지. 유사 선례 DQ-014·DQ-015·DQ-016.

## DQ-018 — coverage/2024-A.md "ES 미등록" 목록 부분 정정 (1 FOUND · 4 NOT_FOUND 또는 ES 조회 대상 X)

- **ID**: DQ-018
- **관련 태스크**: TASK-202 (2024-A study-guide 작성)
- **file**: `projects/ethics-study/exam-solutions/coverage/2024-A.md`
- **category**: es_state_mismatch (coverage md 작성 시점 이후 ES 상태 변경)
- **coverage 작성일**: 2026-04-21 (TASK-175E-2024-A)
- **본 세션 ES 실측일**: 2026-04-23
- **요약**: coverage/2024-A.md BLOCKER 총 5건(coombs · narvaez · Q5 검사명칭 · Q7 갑 한국 성리학자 특정 불능 · fazang) 중 **1건(narvaez)이 현재 실측에서 FOUND** · 나머지 4건은 NOT_FOUND 유지(coombs · fazang 404) 또는 ES 조회 대상 X(Q5 검사명칭 · Q7 갑 사상가 특정 불능).

### FOUND override 1건 (DQ-018 override · BLOCKER 표기 제거 · 정상 ES 근거 사용)

| thinker_id | 문항 | claim 수 | _version | 비고 |
|-----------|------|----------|----------|------|
| narvaez | Q6 나 | 9 | 4 | TASK-176 후속 등록. **2016-A Q9 → 2024-A Q6 (나) 2회차 재출제 (격 8년)**. Darcia Narvaez 1952~ · 삼원 윤리 이론 Triune Ethics Theory · 통합적 윤리 교육 모델 IEE · 신콜버그주의 신경생리학 확장. narvaez-claim-001·002·003 전원 `found=true`. coverage/2024-A.md L735·L760 "BLK-175E-2024A-002" 표기는 2026-04-21 측정 시점 기록으로, 본 세션 2026-04-23 curl 재측정 결과 HTTP 200 · 9 claims · _version=4 확증. |

### NOT_FOUND 2건 (study-guide 에 BLOCKER 표기 유지)

| thinker_id | 문항 | status | study-guide 표기 |
|-----------|------|--------|-------------------|
| coombs | Q5 | 404 | ⚠️ES 미등록 (BLOCKER-1 · BLK-175E-2024A-001) |
| fazang | Q8 갑 | 404 | ⚠️ES 미등록 (BLOCKER-3 · BLK-175E-2024A-005) |

### ES 조회 대상 X 2건 (BLOCKER 표기 유지 · 사상가 id 미정)

| 문항 | 범주 | study-guide 표기 |
|------|------|-------------------|
| Q5 ㉢ | 검사명칭 (coombs 수업 모형 5단계 중 교사 활용 검사명) | ⚠️ES 미등록 (BLOCKER-2 · BLK-175E-2024A-003) · 교과서 표준 확인 필요 |
| Q7 갑 | 한국 성리학자 특정 불능 (성-심-정-의 1로 구조) | ⚠️ES 미등록 (BLOCKER-4 · BLK-175E-2024A-004) · 한국 성리학자 특정 불능 명시 |

- detected_by: TASK-202 Manager spec 작성 시 ES 실측 (2026-04-23T08:00)
- resolution: 원본 수정 금지. TASK-202 spec 에 override 규정 명시 — Coder 는 study-guide/2024-A.md 에 narvaez 정상 thinker_id + claim_id 사용 (⚠️BLOCKER 표기 없음). 4건(coombs · Q5 검사명칭 · Q7 갑 특정불능 · fazang)은 BLOCKER-1·3·4·5 표기 유지. 유사 선례 DQ-014·DQ-015·DQ-016·DQ-017.

## DQ-019 — coverage/2024-B.md "ES 미등록" 목록 부분 정정 (5 FOUND · 1 NOT_FOUND · 역대 최대 배치 override)

- **ID**: DQ-019
- **관련 태스크**: TASK-203 (2024-B study-guide 작성)
- **file**: `projects/ethics-study/exam-solutions/coverage/2024-B.md`
- **category**: es_state_mismatch (coverage md 작성 시점 이후 ES 상태 변경)
- **coverage 작성일**: 2026-04-21 (TASK-175E-2024-B)
- **본 세션 ES 실측일**: 2026-04-23
- **요약**: coverage/2024-B.md BLOCKER 총 6건(turiel · durkheim · blasi · bandura · singer · regan) 중 **5건(turiel · durkheim · blasi · bandura · singer)이 현재 실측에서 FOUND** · 1건(regan) 만 NOT_FOUND 유지. **역대 단일 연도 DQ override 최대 배치 (DQ-014 5건과 동률 but TASK-176 후속 집중 대상 thinker 가 2024-B 문항에 집중되어 신규 등록 패턴 관찰)**. 기존 DQ-016(3건)·DQ-017(1건)·DQ-018(1건) 대비 규모 5배.

### FOUND override 5건 (DQ-019 override · BLOCKER 표기 제거 · 정상 ES 근거 사용)

| thinker_id | 문항 | claim 수 | HTTP | 비고 |
|-----------|------|----------|------|------|
| turiel | Q3 을 | 8 | 200 | Elliot Turiel · 영역 이론 (도덕·관습·개인 영역 구분). **4회째 출제 (2018-B·2021-B·2022-A·2024-B)**. TASK-176 후속 등록. coverage/2024-B.md L536·L549·L584 "BLK-175E-2024B-001" 표기는 2026-04-21 측정 시점 기록. DQ-016(2022-A)에서도 동일 override 적용된 선례 있음. |
| durkheim | Q4 가 | 8 | 200 | Émile Durkheim · 사회학적 도덕교육 · 도덕 규율·집단 애착·자율성. **4회째 출제 (2015-B·2021-B·2022-B·2024-B)**. TASK-176 후속 등록. coverage/2024-B.md L537·L550·L585 "BLK-175E-2024B-002" 표기는 2026-04-21 측정 시점 기록. |
| blasi | Q5 갑 | 8 | 200 | Augusto Blasi · 도덕적 정체성·자기 일관성·자아 모델. **5회째 출제 (2017-A·2019-B·2021-A·2023-A·2024-B, 2023-A→2024-B 2연속)**. TASK-176 후속 등록. coverage/2024-B.md L538·L551·L586 "BLK-175E-2024B-003" 표기는 2026-04-21 측정 시점 기록. DQ-017(2023-A)에서도 동일 override 적용된 선례 있음 — 2년 연속 override. |
| bandura | Q5 을 | 8 | 200 | Albert Bandura · 사회인지 이론 · 도덕적 이탈 · 도덕적 자기조절. **4회째 출제 (2014-A·2019-A·2020-A·2024-B)**. TASK-176 후속 등록. coverage/2024-B.md L538·L552·L587 "BLK-175E-2024B-004" 표기는 2026-04-21 측정 시점 기록. |
| singer | Q8 갑 | 8 | 200 | Peter Singer · 동물 해방 · 이익 평등 고려 · 공리주의 응용윤리. **4회째 출제 (2015-B·2019-B·2022-B·2024-B)**. TASK-176 후속 등록. coverage/2024-B.md L541·L553·L588 "BLK-175E-2024B-005" 표기는 2026-04-21 측정 시점 기록. |

### NOT_FOUND 1건 (study-guide 에 BLOCKER 표기 유지)

| thinker_id | 문항 | status | study-guide 표기 |
|-----------|------|--------|-------------------|
| regan | Q8 을 | 404 | ⚠️ES 미등록 (BLOCKER-1 · BLK-175E-2024B-006) · Tom Regan 동물권·삶의 주체·내재적 가치 trademark 직접 인용 불가 |

- detected_by: TASK-203 Manager spec 작성 시 ES 실측 (2026-04-23T08:30)
- resolution: 원본 수정 금지. TASK-203 spec 에 override 규정 명시 — Coder 는 study-guide/2024-B.md 에 turiel · durkheim · blasi · bandura · singer 5명 전원 정상 thinker_id + claim_id 사용 (⚠️BLOCKER 표기 없음). 1건(regan) 만 BLOCKER-1·BLK-175E-2024B-006 표기 유지. 유사 선례 DQ-014·DQ-015·DQ-016·DQ-017·DQ-018. **규모상 역대 최대 배치 override (5건)** — 2024-B 가 TASK-176 후속 등록 thinker 를 집중적으로 채택한 결과로 추정.

## DQ-020 — coverage/2025-A.md "ES 미등록" 목록 부분 정정 (2 FOUND · 1 NOT_FOUND)

- **ID**: DQ-020
- **관련 태스크**: TASK-204 (2025-A study-guide 작성)
- **file**: `projects/ethics-study/exam-solutions/coverage/2025-A.md`
- **category**: es_state_mismatch (coverage md 작성 시점 이후 ES 상태 변경)
- **coverage 작성일**: 2026-04-21 (TASK-175E-2025-A)
- **본 세션 ES 실측일**: 2026-04-23
- **요약**: coverage/2025-A.md BLOCKER 총 3건(durkheim Q5 · hoffman Q6 · zhiyi Q8 — `rest` false-positive 철회된 -003 제외) 중 **2건(durkheim · hoffman)이 현재 실측에서 FOUND** · 1건(zhiyi) NOT_FOUND 유지. coverage 블로커 번호 -003 은 재번호 없음(-001·-002·-004만 유효, TASK-175E-2025-A-FIX 에 의거).

### FOUND override 2건 (DQ-020 override · BLOCKER 표기 제거 · 정상 ES 근거 사용)

| thinker_id | 문항 | claim 수 | HTTP | 비고 |
|-----------|------|----------|------|------|
| durkheim | Q5 | 8 | 200 | Émile Durkheim · 사회학적 도덕교육 · 도덕 규율·집단 애착·자율성. **5회째 출제 (2015-B·2021-B·2022-B·2024-B·2025-A, 2024-B→2025-A 2연속)**. TASK-176 후속 등록. coverage/2025-A.md L590 "BLK-175E-2025A-001" 표기는 2026-04-21 측정 시점 기록. DQ-019(2024-B)에서도 동일 override 적용된 선례 있음 — 2년 연속 override. |
| hoffman | Q6 갑 | 8 | 200 | Martin Hoffman · 공감 발달 4단계 · 공감에 기초한 도덕 동기. **4회째 출제 (2016-A·2019-B·2022-B·2025-A · 2022-B 이후 4연속 유지 파기 → 3회 단절 후 재등장)**. TASK-176 후속 등록. coverage/2025-A.md L591 "BLK-175E-2025A-002" 표기는 2026-04-21 측정 시점 기록. |

### NOT_FOUND 1건 (study-guide 에 BLOCKER 표기 유지)

| thinker_id | 문항 | status | study-guide 표기 |
|-----------|------|--------|-------------------|
| zhiyi | Q8 | 404 | ⚠️ES 미등록 (BLOCKER-1 · BLK-175E-2025A-004) · 智顗 538-597 · 천태종 · 일념삼천 · trademark 직접 인용 불가 · 교과서 표준 해설 대체 |

- detected_by: TASK-204 Manager spec 작성 시 ES 실측 (2026-04-23T09:20)
- resolution: 원본 수정 금지. TASK-204 spec 에 override 규정 명시 — Coder 는 study-guide/2025-A.md 에 durkheim · hoffman 2명 정상 thinker_id + claim_id 사용 (⚠️BLOCKER 표기 없음). zhiyi 1건은 BLOCKER-1·BLK-175E-2025A-004 표기 유지. 유사 선례 DQ-014~DQ-019. `rest` 사상가는 coverage/2025-A.md L606·L638 에 FIX 주의 명시됨 — 초기 -003 false-positive 철회 후 정상 HIT 사상가.

## DQ-021 — coverage/2025-B.md "ES 미등록" 목록 부분 정정 (4 FOUND · 2 NOT_FOUND)

- **ID**: DQ-021
- **관련 태스크**: TASK-205 (2025-B study-guide 작성)
- **file**: `projects/ethics-study/exam-solutions/coverage/2025-B.md`
- **category**: es_state_mismatch (coverage md 작성 시점 이후 ES 상태 변경)
- **coverage 작성일**: 2026-04-21 (TASK-175E-2025-B-FIX 포함)
- **본 세션 ES 실측일**: 2026-04-24
- **요약**: coverage/2025-B.md BLOCKER 총 6건 중 **4건(jinul · moore · bandura · pettit)이 현재 실측에서 FOUND** · 2건(berlin · Q7 갑 사상가 확증 보류)은 NOT_FOUND 또는 미확정 유지. DQ-019(2024-B 5건)·DQ-020(2025-A 2건) 선례 준용. Q10 갑은 coverage md 는 viroli/pettit 양립으로 기록되어 있었으나 ES 실측 결과 pettit FOUND / viroli NOT_FOUND → **pettit 단일 확정 · viroli 폐기**.

### FOUND override 4건 (DQ-021 override · BLOCKER 표기 제거 · 정상 ES 근거 사용)

| thinker_id | 문항 | claim 수 | HTTP | 비고 |
|-----------|------|----------|------|------|
| jinul | Q1 | 9 | 200 | 知訥 보조국사 普照國師 1158-1210 · 고려 조계종 개창 · 돈오점수 頓悟漸修 · 정혜쌍수 定慧雙修 · 자성정혜/수상정혜 · 불성 · 『수심결』·『권수정혜결사문』. **2회째 출제 (2021-B·2025-B)**. TASK-176 후속 등록. coverage/2025-B.md L55 "BLK-175E-2025B-001" 표기는 2026-04-21 측정 시점 기록. DQ-016(2022-A)에서도 동일 override 적용된 선례 있음. |
| moore | Q2 | 7 | 200 | George Edward Moore 1873-1958 · 영국 케임브리지 분석철학자 · 자연주의적 오류 naturalistic fallacy · 열린 질문 논증 Open-Question Argument · 『Principia Ethica, 1903』. **2회째 출제 (2021-A·2025-B)**. TASK-176 후속 등록. coverage/2025-B.md L81 "BLK-175E-2025B-002" 표기는 2026-04-21 측정 시점 기록. |
| bandura | Q5 | 8 | 200 | Albert Bandura 1925-2021 · 자아효능감 · 삼원상호결정론 · 4원천. **5회째 출제 (2014-A·2019-A·2020-A·2024-B·2025-B · 2024-B→2025-B 2연속)**. TASK-176 후속 등록. coverage/2025-B.md L169 "BLK-175E-2025B-003" 표기는 2026-04-21 측정 시점 기록. DQ-019(2024-B)에서도 동일 override 적용된 선례 있음 — 2년 연속 override. |
| pettit | Q10 갑 | 8 | 200 | Philip Pettit 1945- · 비지배 자유 freedom as non-domination · 신로마 공화주의 · 자치적 정치체제 · 『Republicanism, 1997』. **4회째 출제 (2019-A·2020-A·2022-A·2025-B)**. TASK-176 후속 등록. coverage/2025-B.md L320·L335·L365 는 `viroli 또는 pettit` 양립 보류 기록이었으나 ES 실측 결과 pettit FOUND / viroli NOT_FOUND · 원문 L179 trademark 3중 일치(자의에 예속되지 않는 것·자치적 정치체제·스스로의 의지에만 종속) 모두 pettit 『Republicanism, 1997』 비지배 자유 정립자 프로필과 정합 → **pettit 단일 확정 · viroli 폐기**. DQ-016(2022-A)에서도 pettit override 선례 있음. |

### NOT_FOUND/미확정 2건 (study-guide 에 BLOCKER 표기 유지)

| thinker_id | 문항 | status | study-guide 표기 |
|-----------|------|--------|-------------------|
| berlin | Q10 을 | 404 | ⚠️ES 미등록 (BLOCKER-1 · BLK-175E-2025B-005) · Isaiah Berlin 1909-1997 · 두 자유 개념 Two Concepts of Liberty, 1958 · 소극적 자유 · 통제의 근원 vs 범위 · trademark 직접 인용 불가 · 교과서 표준 해설 대체 |
| ??? (Q7 갑) | Q7 갑 | — | ⚠️사상가 확증 보류 (BLOCKER-2 · BLK-175E-2025B-006) · 후보: yihwang(퇴계 HIT)/im_seongju(MISS)/han_wonjin(MISS) · 원문 배타적 trademark 부재 · 교과서 표준 해설 대체 · trademark 직접 인용 금지 |

- detected_by: TASK-205 Manager spec 작성 시 ES 실측 (2026-04-24T07:05)
- resolution: 원본 수정 금지. TASK-205 spec 에 override 규정 명시 — Coder 는 study-guide/2025-B.md 에 jinul · moore · bandura · pettit 4명 전원 정상 thinker_id + claim_id 사용 (⚠️BLOCKER 표기 없음). berlin · Q7 갑 2건은 BLOCKER 표기 유지. 유사 선례 DQ-014~DQ-020. Q10 갑 viroli→pettit 단일 확정 판단 근거: ES 실측 + 원문 trademark 3중 일치.

---

## DQ-022 (2026-04-24 · Coder TASK-205-FIX 작업 중 발견)

### 개요

ES `ethics-claims` 인덱스 내 John Stuart Mill 관련 claim 의 `thinker_id` 필드 값은 `mill_js` (동명이인 suffix 규약 준수) 이나, **_id prefix 는 `mill-claim-*`** (NOT `mill_js-claim-*`) 로 분리됨. Coder 가 TASK-205-FIX 수정 중 Mill 5건 전수 조회 실행 시 `mill_js-claim-NNN` 조회는 HTTP 404 · `mill-claim-NNN` 조회만 found=true 확증.

### ES 실측 (2026-04-24 · TASK-205-FIX Coder)

```bash
# thinker_id=mill_js 인덱스 내 전수
curl -s 'http://localhost:9200/ethics-claims/_search?q=thinker_id:mill_js&size=20'
→ 5 hits · _id = mill-claim-001 / mill-claim-002 / mill-claim-003 / mill-claim-004 / mill-claim-005

# 각 _id found 확인
curl -s 'http://localhost:9200/ethics-claims/_doc/mill-claim-001' → found=true (질적 공리주의)
curl -s 'http://localhost:9200/ethics-claims/_doc/mill-claim-002' → found=true
curl -s 'http://localhost:9200/ethics-claims/_doc/mill-claim-003' → found=true
curl -s 'http://localhost:9200/ethics-claims/_doc/mill-claim-004' → found=true
curl -s 'http://localhost:9200/ethics-claims/_doc/mill-claim-005' → found=true
# mill_js prefix 는 _id 에 부재
curl -s 'http://localhost:9200/ethics-claims/_doc/mill_js-claim-001' → HTTP 404 found=false
```

### 영향 범위

- 2025-B.md (Q9 을 서술형): mill 인용 5건 (mill-claim-001~005) — Coder TASK-205-FIX 에서 `mill_js-claim-*` → `mill-claim-*` 전수 치환 완료
- 기존 study-guide 시리즈 중 mill_js 인용 연도 (2018-A·2019-B·2023-A·2023-B·2025-B 등) 전수 재확인 필요 — 후속 일괄 점검 대상

### 원인 추정

`thinker_id` 는 동명이인 suffix 규약 (mill_js = John Stuart Mill · mill_j = James Mill 가능성 대비) 준수했으나, claim _id 는 초기 등록 시 `{lastname}-claim-{NNN}` 패턴 (다른 사상가들과 일관) 을 채택하여 prefix 단일화. 부모 thinker 와 동기화 원칙 위반.

### 조치

- **TASK-205-FIX 내 즉시 정정**: Coder 가 study-guide 2025-B.md 의 `mill_js-claim-*` 5건을 전원 `mill-claim-*` 로 치환 완료 (content match 확증 포함).
- **Log-only · 원본 ES 수정 금지**: architecture.md "원본 수정 금지" 규정 준수 · mill_js thinker_id 와 mill-claim _id 분리 상태를 **data-quality-log** 에만 기록.
- **후속 태스크 권고**: 다른 연도 study-guide (2018-A·2019-B·2023-A·2023-B) 에서 `mill_js-claim-*` 잔존 여부 `grep -rn 'mill_js-claim-' projects/ethics-study/exam-solutions/study-guide/` 로 일괄 점검 후 동일 치환. Manager 가 TASK-DQ-022-SWEEP 등 별도 등록 검토.

### DQ 분류

- severity: observation (코드 결함 아님 · 데이터 품질 metadata 불일치)
- 자동화 가능성: 가능 (grep 기반 전수 치환)
- 재발 방지: ES 등록 스크립트 (TASK-176 계열) 에서 `_id prefix ← thinker_id` 일치 검증 단계 추가 필요

---

## DQ-023: 2026-A coverage BLOCKER false-positive 3건 (turiel · taylor_p · leopold)

- **발견 시점**: 2026-04-24 (TASK-206 착수 전 ES sweep)
- **발견자**: Manager (세션 재개 후 BLOCKER 후보 실측 · DQ-019/020/021 선례 패턴 재현)
- **근거 파일**: `projects/ethics-study/exam-solutions/coverage/2026-A.md` L707 · L716 · L717
- **severity**: observation (데이터 품질 metadata 불일치 · 코드 결함 아님)

### coverage 기록 vs 2026-04-24 실측

| thinker_id | coverage 기록 | 2026-04-24 curl 실측 | 판정 |
|---|---|---|---|
| cho_sik | MISS (L704) · BLK-175E-2026A-001 | thinker=404 · claims=0 | **진짜 BLOCKER 유지** |
| turiel | MISS (L707) · BLK-175E-2024B-001 누적 5회째 | thinker=200 · claims=8 | **DQ-023 override** |
| taylor_p | MISS (L716) · BLK-175E-2026A-002 (BLK-175E-2021A-003 누적) | thinker=200 · claims=8 | **DQ-023 override** |
| leopold | MISS (L717) · BLK-175E-2026A-003 (최초 등장) | thinker=200 · claims=7 | **DQ-023 override** |

### 실측 curl 결과 (2026-04-24)

```bash
for tid in cho_sik turiel taylor_p leopold; do
  status=$(curl -s -o /dev/null -w "%{http_code}" "http://localhost:9200/ethics-thinkers/_doc/$tid")
  claims=$(curl -s "http://localhost:9200/ethics-claims/_search?q=thinker_id:$tid&size=0" \
    | python3 -c "import sys,json; print(json.load(sys.stdin)['hits']['total']['value'])")
  echo "$tid thinker=$status claims=$claims"
done
# cho_sik thinker=404 claims=0
# turiel thinker=200 claims=8
# taylor_p thinker=200 claims=8
# leopold thinker=200 claims=7
```

### 추정 원인

- coverage/2026-A.md 작성 시점에 turiel · taylor_p · leopold 는 ES 미등록 상태로 기록됨.
- TASK-176 후속 또는 중간 batch 등록으로 2026-04-24 시점에는 HIT.
- cho_sik 은 여전히 미등록 (55 thinker 전수 목록 architecture.md L696 에도 부재).

### 조치

- **TASK-206 study-guide 작성 시**:
  - turiel · taylor_p · leopold: **정상 HIT 으로 취급** · claim_id 인용 가능 · BLOCKER 표기 제거.
  - cho_sik: **BLOCKER 유지** · BLK-175E-2026A-001 표기 · trademark 직접 인용 금지 · 교과서 표준 해설로 대체.
- **coverage md 원본 수정 금지**: architecture.md "원본 수정 금지" 규정 준수 · coverage L704·L707·L716·L717 MISS 기록 유지 · DQ-023 로그로만 override.

### DQ 분류

- severity: observation
- 자동화 가능성: 가능 (coverage BLOCKER 목록 → ES HTTP 상태 일괄 재조회 스크립트)
- 재발 방지: coverage 작성 시 ES 상태 실측 timestamp 기록 후, study-guide 작성 직전 1회 더 재조회 (TASK-DQ-019/020/021 패턴 4회째 반복 — 프레임워크화 retrospective 권고)

---

## DQ-024 · 2026-04-24 · coverage/2026-B.md BLOCKER false-positive 4건 override (5회째 반복 · 프레임워크화 retrospective 최우선)

### 개요

coverage/2026-B.md 작성 시점 (2026-04-21 23:09) 에 기록된 ES 미등록 BLOCKER 5건 중 **4건이 2026-04-24 curl 실측 결과 실제로는 ES HIT** 으로 확인됨. TASK-DQ-019 (2024-B · 2회째) · TASK-DQ-020 (2025-A · 3회째) · TASK-DQ-021 (2025-B · 4회째) · TASK-DQ-023 (2026-A · 4회째) 에 이은 **5회째 반복** · 프레임워크화 retrospective **최우선 권고**.

### coverage md 주장 vs ES 실측

| thinker_id | coverage md 주장 | 2026-04-24 ES 실측 | 판정 |
|---|---|---|---|
| bandura | MISS (L728·L779) · BLK-175E-2026B-001 (최우선 · 6회째 3연속 최장 기록) | thinker=200 · claims=8 | **DQ-024 override** |
| jinul | MISS (L732·L780) · BLK-175E-2026B-002 (BLK-175E-2025B-001 누적 · 3회째 2연속) | thinker=200 · claims=9 | **DQ-024 override** |
| pettit | MISS (L730·L783) · BLK-175E-2026B-005 (BLK-175E-2025B-004 누적 · 3회째 2연속) | thinker=200 · claims=8 | **DQ-024 override** |
| narvaez | MISS (L727·L769) · BLK-175E-2024A-002 누적 갱신 (2회째) | thinker=200 · claims=9 | **DQ-024 override** |
| schumpeter | MISS (L729·L782) · BLK-175E-2026B-004 (최초 · row 기준 최초 출제) | thinker=404 · claims=0 | **BLOCKER 유지** |
| viroli | MISS (L772·L783) · BLK-175E-2026B-005 경합 (pettit/viroli) | thinker=404 · claims=0 | **폐기** (pettit 단일 확정 · TASK-DQ-021 선례) |
| tappan·brown·kilpatrick | 보류 (L726·L781) · BLK-175E-2026B-003 (서사 도덕교육 · 사상가 특정 불능) | thinker=404 전원 · claims=0 | **보류 유지** (교과교육학 N/A) |

### 실측 curl 결과 (2026-04-24)

```bash
for tid in bandura jinul schumpeter pettit viroli narvaez tappan brown kilpatrick; do
  status=$(curl -s -o /dev/null -w "%{http_code}" "http://localhost:9200/ethics-thinkers/_doc/$tid")
  claims=$(curl -s "http://localhost:9200/ethics-claims/_count?q=thinker_id:$tid" \
    | python3 -c "import sys,json; print(json.load(sys.stdin).get('count',0))")
  echo "$tid thinker=$status claims=$claims"
done
# bandura thinker=200 claims=8
# jinul thinker=200 claims=9
# schumpeter thinker=404 claims=0
# pettit thinker=200 claims=8
# viroli thinker=404 claims=0
# narvaez thinker=200 claims=9
# tappan thinker=404 claims=0
# brown thinker=404 claims=0
# kilpatrick thinker=404 claims=0
```

### 추정 원인

- coverage/2026-B.md 작성 시점 (2026-04-21) 에 bandura·jinul·pettit·narvaez 가 ES 미등록 상태로 기록됨.
- TASK-176 후속 또는 중간 batch 등록으로 2026-04-24 시점에는 HIT.
- schumpeter · viroli · tappan · brown · kilpatrick 는 여전히 미등록 (55 thinker dump architecture.md L696 에도 부재).

### 조치

- **TASK-207 study-guide 작성 시**:
  - bandura · jinul · pettit · narvaez: **정상 HIT 으로 취급** · claim_id 인용 가능 · BLOCKER 표기 제거.
  - schumpeter: **BLOCKER 유지** · BLK-175E-2026B-004 표기 · trademark 직접 인용 금지 · 교과서 표준 해설로 대체.
  - viroli: **폐기** (pettit 단일 확정 · TASK-DQ-021 선례).
  - Q3 서사 도덕교육 (tappan/brown/kilpatrick): **N/A 처리** (교과교육학 · 2022 개정 교육과정 서사적 방법 교수·학습 모형 정형화 · 사상가 실명 특정 불능 · BLK-175E-2026B-003 보류).
- **coverage md 원본 수정 금지**: architecture.md "원본 수정 금지" 규정 준수 · coverage L727·L728·L730·L732·L769·L779·L780·L783 MISS 기록 유지 · DQ-024 로그로만 override.

### DQ 분류

- severity: observation
- 자동화 가능성: 가능 (coverage BLOCKER 목록 → ES HTTP 상태 일괄 재조회 스크립트)
- 재발 방지: **TASK-DQ-019/020/021/023 이후 5회째 반복** — coverage 작성 시 ES 상태 실측 timestamp 기록 후, study-guide 작성 직전 1회 더 재조회를 **파이프라인 표준 단계로 프레임워크화 권고 · retrospective 최우선 반영**. 각 BLOCKER 선언 전 HTTP probe → 404 확정 시에만 BLOCKER 기록.

---

## DQ-025 · 2026-04-28 · cho_sik post-registration override (TASK-212-01 · 2026-A Q3 BLK-175E-2026A-001 해소)

### 개요

`cho_sik` (남명 조식, 南冥 曺植, 1501-1572, 조선 중기 성리학자) 는 coverage/2026-A.md L100-L141 작성 시점 (2026-04-22) ES 미등록 상태 (HTTP 404 · claims=0) 로 BLK-175E-2026A-001 BLOCKER 기록되었음. 본 세션 2026-04-28 TASK-212-01 으로 ES 정식 등록 완료 (1 thinker + 2 works + 5 claims + 7 keywords + 2 relations) → 사후 정정 override.

DQ-024 (2026-B BLOCKER false-positive 4건) 와 분리: DQ-024 는 **false-positive override** (coverage 시점 이미 ES HIT 였으나 잘못 BLOCKER 기록), DQ-025 는 **post-registration override** (coverage 시점 정상 BLOCKER 기록 + 본 태스크에서 신규 ES 등록 후 정정).

### coverage md 주장 vs ES 실측

| thinker_id | coverage md 주장 (2026-04-22) | 2026-04-28 ES 실측 (등록 직후) | 판정 |
|---|---|---|---|
| cho_sik | MISS · BLK-175E-2026A-001 (Q3 · 1회째 row 기준 최초 출제 · 한국 성리학 사림파 trademark 직접 인용 금지) | thinker=200 · claims=5 (TASK-212-01 신규 등록) | **DQ-025 post-registration override** |

### 등록 산출물 (TASK-212-01)

```bash
# 실측 curl (2026-04-28 TASK-212-01 등록 완료 직후)
curl -s -o /dev/null -w "%{http_code}\n" "http://localhost:9200/ethics-thinkers/_doc/cho_sik"
# 200

curl -s "http://localhost:9200/ethics-claims/_count?q=thinker_id:cho_sik" \
  | python3 -c "import sys,json; print(json.load(sys.stdin).get('count',0))"
# 5
```

- **thinker**: `cho_sik` — name="남명 조식 (南冥 曺植)" · name_en="Cho Sik" · field="eastern_ethics" · era="조선" · birth=1501 · death=1572.
- **works (2건)**: `cho_sik-nammyeongjip` (남명집) · `cho_sik-hakgiyupyeon` (학기유편).
- **claims (5건)**:
  - `cho_sik-claim-001` 경의(敬義) 병립 — 경(敬)으로 안을 밝히고 의(義)로 밖을 결단 (해와 달 비유).
  - `cho_sik-claim-002` 패검명(佩劍銘) "內明者敬 外斷者義" — 내면 수양과 외부 결단의 trademark 명문.
  - `cho_sik-claim-003` 학문 단계론 — 소학(小學) → 근사록(近思錄) → 성리대전(性理大全).
  - `cho_sik-claim-004` 출처관 대비 — 퇴계 이황 거경궁리(居敬窮理) 와 대조되는 경의 병립의 실천·외향 강조.
  - `cho_sik-claim-005` 산림처사(山林處士) 정신 — 산천재(山天齋)·뇌룡정 수양처 + 단성현감 사직소.
- **keywords (7건)**: gyeongui-byeongnip · naemyeongjagyeong · paegeommyeong · hakmun-dangye · sanrim-cheosa · sancheonjae · geogyeong-gungri-daejo.
- **relations (2건)**: cho_sik → yi_hwang (compared) · cho_sik → yi_yulgok (compared).

### 추정 원인

- TASK-176 (2026-04-22 DONE) 은 `exam-coverage-map.md` Section D **TOP10 (출제 빈도 ≥3)** 만 다뤘음 — cho_sik 은 출제 빈도 1 (2026-A 신규) 으로 후순위.
- TASK-212 (mother) 잔존 13명 ES 보강 시리즈에서 cho_sik 은 사용자 인사이트 (이황과 동시대 인물로 학습 자료에 충분히 등장했어야 함) 로 HIGH 우선순위 부여 → TASK-212-01 으로 분리 등록.

### 조치

- **study-guide/2026-A.md 정정 (BLOCKER 7곳 → ✅ES 등록 완료)**:
  - **L19** 표 row: `⚠️ ES 미등록 (1건 — BLOCKER 유지)` → `✅ ES 등록 완료 (DQ-025 override · TASK-212-01)`.
  - **L41** 14명 영역 통계: `잔존 BLOCKER 1명 cho_sik` → `(전원 ES 등록 완료, 잔존 BLOCKER 0명 — 2026-04-28 TASK-212-01 cho_sik ES 등록 완료 후 DQ-025 override)`.
  - **L53** 섹션 heading: `### cho_sik BLOCKER 유지` → `### cho_sik ES 등록 완료 (DQ-025 override) — Q3 남명 조식 trademark 인용 가능`.
  - **L55** 본문: BLOCKER 설명 → `cho_sik-claim-001`~`005` 정상 인용 가능 + ES HTTP 200 · total=5 명시.
  - **L140** 문항 3 heading: `⚠️ BLOCKER (BLK-175E-2026A-001 유지)` → `✅ DQ-025 override (cho_sik ES 등록 완료)`.
  - **L158** 사상가 줄: `⚠️BLK-175E-2026A-001 · ES 미등록 확증` → `✅ ES 등록 (TASK-212-01) · cho_sik-claim-001~005 인용 가능`.
  - **L166** 후속 등록 대기 줄: `⚠️ cho_sik ES 미등록 (BLK-175E-2026A-001)` → `✅ cho_sik ES 등록 완료 (DQ-025 override · TASK-212-01)` + 핵심 ES claim 3건 (claim-001 경의 병립 / -002 패검명 / -003 학문 단계론) 인용 추가.
- **coverage/2026-A.md 원본 변경 없음** (architecture.md "원본 수정 금지" 규정 준수 · L100-L141 BLOCKER 기록 유지 · DQ-025 로그로만 override).
- **trademark fabrication 방지**: 5 claims 전원 출처 verbatim 사용 (coverage/2026-A.md L100-L141 · study-guide/2026-A.md L155-L177 · blocker-log.md L1074-L1080) — 사용자 인사이트 (이황 동시대인) 는 우선순위 근거이며 trademark 으로 직접 인용하지 않음.

### DQ 분류

- severity: observation
- 자동화 가능성: 가능 (TASK-212 mother 의 13명 ES 보강 시리즈 자동화 — `insert_{id}.py` 패턴 답습)
- 재발 방지: TASK-176 의 TOP10 한정을 넘어 **출제 빈도 1회 row 기준 최초 등장** 까지 ES 등록 cutoff 확장 필요 — TASK-212 시리즈 (sub 13건) 완주 후 retrospective 반영. 각 study-guide 작성 시점에 BLOCKER thinker 의 ES 등록 가능성 (사용자 인사이트 / 동시대 비교 인물 / 표준 교과서 trademark 보유) 을 별도 검토 단계로 추가.

---

## DQ-026 · 2026-04-28 · schumpeter post-registration override (TASK-212-02 · 2026-B Q6 (나) BLK-175E-2026B-004 해소)

### 개요

`schumpeter` (조지프 슘페터, Joseph Alois Schumpeter, 1883-1950, 오스트리아-헝가리 제국 모라비아 출생 미국 하버드대 경제학자·사회학자·정치경제학자) 는 coverage/2026-B.md L337-L400 작성 시점 (2026-04-21) ES 미등록 상태 (HTTP 404 · claims=0) 로 BLK-175E-2026B-004 BLOCKER 기록되었음. 본 세션 2026-04-28 TASK-212-02 으로 ES 정식 등록 완료 (1 thinker + 2 works + 6 claims + 6 keywords + 2 relations) → 사후 정정 override.

DQ-024 (2026-B BLOCKER false-positive 4건) · DQ-025 (cho_sik post-registration) 와 분리: DQ-024 는 **false-positive override**, DQ-025·DQ-026 는 **post-registration override**. DQ-026 은 2026-B 정치철학 영역 row 기준 최초 출제 사상가 ES 등록 — 자유주의(밀·롤스·노직 HIT) · 공동체주의(매킨타이어·샌델·왈저 HIT) · 공화주의(페팃 HIT) 에 더해 **경쟁적 엘리트 민주주의(슘페터)** 축 추가로 정치철학 ES 커버리지 확장.

### coverage md 주장 vs ES 실측

| thinker_id | coverage md 주장 (2026-04-21) | 2026-04-28 ES 실측 (등록 직후) | 판정 |
|---|---|---|---|
| schumpeter | MISS · BLK-175E-2026B-004 (Q6 (나) · 1회째 row 기준 최초 출제 · 경쟁적 엘리트 민주주의 trademark 직접 인용 금지 · 교과서 표준 해설 대체) | thinker=200 · claims=6 (TASK-212-02 신규 등록) | **DQ-026 post-registration override** |

### 등록 산출물 (TASK-212-02)

```bash
# 실측 curl (2026-04-28 TASK-212-02 등록 완료 직후)
curl -s -o /dev/null -w "%{http_code}\n" "http://localhost:9200/ethics-thinkers/_doc/schumpeter"
# 200

curl -s "http://localhost:9200/ethics-claims/_search?q=thinker_id:schumpeter&size=0" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['hits']['total']['value'])"
# 6
```

- **thinker**: `schumpeter` — name="조지프 슘페터 (Joseph Alois Schumpeter)" · name_en="Joseph Alois Schumpeter" · field="political_philosophy" · era="현대" · birth=1883 · death=1950.
- **works (2건)**: `schumpeter-csd-1942` (자본주의·사회주의·민주주의) · `schumpeter-twe-1911` (경제 발전의 이론).
- **claims (6건)**:
  - `schumpeter-claim-001` 경쟁적 엘리트 민주주의 (competitive elitist democracy) — 정치인의 국민 표 획득 경쟁 · 『CSD』 22장.
  - `schumpeter-claim-002` 절차적·최소주의 민주주의 — "민주주의는 정치적 방법(political method) / 제도적 장치(institutional arrangement)" 정식.
  - `schumpeter-claim-003` 고전적 민주주의 비판 — 공동선·인민의지·합리적 시민 3전제 부정 · 인민자치(self-government of the people) 허구.
  - `schumpeter-claim-004` 창조적 파괴 (creative destruction) — 자본주의 동력 · 『CSD』 7장.
  - `schumpeter-claim-005` 기업가(entrepreneur) 이론 · 혁신 5유형 (신제품·신생산방법·신시장·신원료·신조직) — 『경제 발전의 이론, 1911』.
  - `schumpeter-claim-006` 자본주의 필연적 쇠퇴 예측 — 합리화·관료화·기업가 정신 소멸 · 사회주의 이행.
- **keywords (6건)**: competitive-elitist-democracy · political-method · classical-doctrine-critique · creative-destruction · entrepreneur · capitalism-decline.
- **relations (2건)**: schumpeter → rousseau (compared · 고전 vs 경쟁적 엘리트 민주주의 정전 대립) · schumpeter → mill_js (compared · 절차적 vs 발전적 민주주의관 대비).

### 추정 원인

- TASK-176 (2026-04-22 DONE) 은 `exam-coverage-map.md` Section D **TOP10 (출제 빈도 ≥3)** 만 다뤘음 — schumpeter 는 출제 빈도 1 (2026-B 신규) 으로 후순위.
- TASK-212 (mother) 잔존 13명 ES 보강 시리즈에서 schumpeter 는 정치철학 민주주의 영역 ES 커버리지 공백 (자유주의 · 공동체주의 · 공화주의 축은 보강되었으나 경쟁적 엘리트 민주주의 축 부재) 해소 목적으로 HIGH 우선순위 부여 → TASK-212-02 으로 분리 등록.

### 조치

- **study-guide/2026-B.md 정정 (BLOCKER 7곳 + footer 3곳 → ✅ES 등록 완료)**:
  - **L19** 표 row: `⚠️ ES 미등록 (1건 — BLOCKER 유지)` → `✅ ES 등록 완료 (DQ-026 override · TASK-212-02)`.
  - **L53** 섹션 heading: `### schumpeter BLOCKER 유지` → `### schumpeter ES 등록 완료 (DQ-026 override) — Q6 나 경쟁적 엘리트 민주주의 trademark 인용 가능`.
  - **L55** 본문: BLOCKER 설명 → `schumpeter-claim-001`~`006` 정상 인용 가능 + ES HTTP 200 · total=6 명시 + trademark 6종 (경쟁적 엘리트 / 절차적 / 고전적 비판 / 창조적 파괴 / 기업가·혁신 5유형 / 쇠퇴 예측) 직접 표기.
  - **L351** 문항 6 heading: `루소(가) · 슘페터(나)` → `루소(가) · 슘페터(나) — ✅ DQ-026 override (schumpeter ES 등록 완료)`.
  - **L377** 사상가 줄: `⚠️ BLK-175E-2026B-004 — ES 미등록` → `✅ ES 등록 (TASK-212-02) · schumpeter-claim-001~006 인용 가능`.
  - **L391** 후속 등록 대기 줄: `⚠️ schumpeter ES 미등록 (HTTP 404 · BLK-175E-2026B-004) claim_id 인용 생략` → `✅ schumpeter ES 등록 (DQ-026 override · TASK-212-02 · HTTP 200 · 6 claims) · claim_id 인용 가능` + 핵심 ES claim 6건 인용 추가 (claim-001 경쟁적 엘리트 / -002 절차적 / -003 고전적 비판 / -004 창조적 파괴 / -005 기업가·혁신 5유형 / -006 쇠퇴 예측).
  - **L396 (현 L402)** 풀이 과정 (나) 사상가 특정 줄: `⚠️ schumpeter ES 미등록이므로 trademark 직접 인용 대신 교과서 표준 해설` → `✅ schumpeter ES 등록 완료 · trademark 직접 인용 가능 (claim_id 001~003 인용)`.
  - **footer L795** 섹션 표 Q6 row: `HIT / ⚠️MISS · BLK-175E-2026B-004` → `HIT × HIT(DQ-026) · BLK-175E-2026B-004 해소(TASK-212-02)`.
  - **footer L806** 재출제 경향: `schumpeter ES 미등록 · 향후 등록 시급` → `schumpeter ES 등록 완료 (DQ-026 override · TASK-212-02 · BLK-175E-2026B-004 해소)`.
  - **footer L819-L821** "BLOCKER 유지 1명" heading: `BLOCKER 유지 1명 · N/A 처리 1건` → `BLOCKER 잔존 0명 · N/A 처리 1건 (DQ-026 schumpeter 해소 후)` + schumpeter 줄 ✅ 표기.
- **coverage/2026-B.md 원본 변경 없음** (architecture.md "원본 수정 금지" 규정 준수 · L337-L400 BLOCKER 기록 유지 · DQ-026 로그로만 override).
- **trademark fabrication 방지**: 6 claims · 6 keywords · 2 relations 전원 출처 verbatim 사용 (coverage/2026-B.md L337-L400 · study-guide/2026-B.md L351-L400 · blocker-log.md L1123-L1129) — 자기검증 3-step 산술 결과 Step 1 trademark 토큰 전원 verbatim 출처 보유 · Step 1 ∩ Step 1b ∩ Step 2 = 0 (`signal/ethics-study/coder-report-TASK-212-02.md` 기록).

### DQ 분류

- severity: observation
- 자동화 가능성: 가능 (TASK-212 mother 의 13명 ES 보강 시리즈 자동화 — `insert_{id}.py` 패턴 답습 · cho_sik (DQ-025) · schumpeter (DQ-026) 2건 동일 절차)
- 재발 방지: TASK-212 시리즈 (sub 13건) 완주 후 retrospective 반영. 정치철학 영역 ES 커버리지 4축 (자유주의·공동체주의·공화주의·경쟁적 엘리트 민주주의) 완성 — 향후 정치철학 출제 사상가 ES gap 발생 가능성 축소.

---

## DQ-027 · 2026-04-28 · regan post-registration override (TASK-212-03 · 2018-A Q11 BLK-175E-2018A-001 + 2024-B Q8 을 BLK-175E-2024B-006 동시 해소)

### 개요

`regan` (톰 리건, Tom Regan, 1938-2017, 미국 노스캐롤라이나 주립대 동물권 철학자, 의무론적 동물권 이론의 정초자) 는 coverage/2018-A.md L143-L165 작성 시점 (2026-04-21) 및 coverage/2024-B.md L350-L385 작성 시점 (2026-04-21) ES 미등록 상태 (HTTP 404 · claims=0) 로 BLK-175E-2018A-001 + BLK-175E-2024B-006 두 BLOCKER 동시 기록되었음. 본 세션 2026-04-28 TASK-212-03 으로 ES 정식 등록 완료 (1 thinker + 1 work + 6 claims + 6 keywords + 2 relations) → 사후 정정 override **2 BLOCKER 단일 등록 동시 해소** (TASK-212 시리즈 최초 사례).

DQ-024 (2026-B BLOCKER false-positive 4건) 와 분리: DQ-024 는 **false-positive override**, DQ-025·DQ-026·DQ-027 는 **post-registration override**. DQ-027 은 응용윤리 동물 윤리 영역 ES 커버리지 공백 완성 — 공리주의 진영 (싱어 HIT) 에 더해 **의무론 진영 (리건)** 축 추가로 동물 윤리 양대 입장 ES 커버리지 완성. 단일 사상가 등록으로 2 BLOCKER (2018-A · 2024-B) 동시 해소는 TASK-212 시리즈 최초.

### coverage md 주장 vs ES 실측

| thinker_id | coverage md 주장 (2026-04-21) | 2026-04-28 ES 실측 (등록 직후) | 판정 |
|---|---|---|---|
| regan | MISS · BLK-175E-2018A-001 (Q11 · 1회째 출제 · 의무론적 동물권 trademark 직접 인용 금지) + BLK-175E-2024B-006 (Q8 을 · 2회째 출제 · 6년 단절 후 재등장 · 교과서 표준 해설 대체) | thinker=200 · claims=6 (TASK-212-03 신규 등록) | **DQ-027 post-registration override (2 BLOCKER 동시 해소)** |

### 등록 산출물 (TASK-212-03)

```bash
# 실측 curl (2026-04-28 TASK-212-03 등록 완료 직후)
curl -s -o /dev/null -w "%{http_code}\n" "http://localhost:9200/ethics-thinkers/_doc/regan"
# 200

curl -s "http://localhost:9200/ethics-claims/_search?q=thinker_id:regan&size=0" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['hits']['total']['value'])"
# 6
```

- **thinker**: `regan` — name="톰 리건 (Tom Regan)" · name_en="Tom Regan" · field="western_ethics" · era="현대" · birth=1938 · death=2017.
- **works (1건)**: `regan-car-1983` (동물권 옹호 / The Case for Animal Rights, 1983).
- **claims (6건)**:
  - `regan-claim-001` 내재적 가치 (inherent value) — "획득되거나 부여되지 않음"·삶의 주체 동등 소유 · CAR 7장 §7.5.
  - `regan-claim-002` 삶의 주체 (subject-of-a-life) 7기준 — 믿음·욕망 / 지각·기억·미래의식 / 쾌락·고통 감정적 삶 / 선호·복지 이익 / 욕구·목적 달성 행동능력 / 심리적 동일성 / 개별적 복지 · CAR 7장 §7.1-7.5.
  - `regan-claim-003` 존중의 원리 (respect principle) — 단순 수단 대우 금지·목적 그 자체 존중 · 칸트 인간 목적 정식의 동물 확장 · CAR 8-9장.
  - `regan-claim-004` 해악의 원리 (harm principle) — 복지·삶의 기회 박탈 금지 · 절대적 금지 · CAR 8-9장.
  - `regan-claim-005` 의무론적 동물권 — 싱어 공리주의 비판 (총합 계산으로 상쇄 불가) · 2024-B Q8 을 ㉢ 유용성 비판의 직접 근거.
  - `regan-claim-006` 권리 행사자 (moral agents) vs 권리 보유자 (moral patients) 구분 — 삶의 주체이면 도덕 능력 무관하게 동등한 권리 보유 · 칸트 비판.
- **keywords (6건)**: inherent-value · subject-of-a-life · respect-principle · harm-principle · deontological-animal-rights · moral-agents-patients.
- **relations (2건)**: regan → singer (criticized · 동물 윤리 양대 입장 정전 대립 — 의무론 vs 공리주의) · regan → kant (extended · 인간 목적 정식의 동물 확장).

### 추정 원인

- TASK-176 (2026-04-22 DONE) 은 `exam-coverage-map.md` Section D **TOP10 (출제 빈도 ≥3)** 만 다뤘음 — regan 은 출제 빈도 2 (2018-A · 2024-B) 로 후순위.
- TASK-212 (mother) 잔존 13명 ES 보강 시리즈에서 regan 은 응용윤리 동물 윤리 영역 ES 커버리지 공백 (공리주의 진영 싱어 HIT 만 등록되어 있고 의무론 진영 부재) 해소 목적으로 HIGH 우선순위 부여 → TASK-212-03 으로 분리 등록.
- 단일 사상가 등록으로 2 BLOCKER (BLK-175E-2018A-001 + BLK-175E-2024B-006) 동시 해소 — TASK-212 시리즈 최초 사례.

### 조치

- **study-guide/2018-A.md 정정 (4 곳 → ✅ES 등록 완료)**:
  - **L19** 표 row: `⚠️ ES 미등록 (1명 · BLOCKER) | regan (Q11)` → `✅ ES 등록 완료 (DQ-027 override · TASK-212-03) | regan (Q11 · BLK-175E-2018A-001 해소)`.
  - **L40** 공지: `Q11 regan 만 ⚠️ES 미등록(BLOCKER-1)` → `Q11 regan ✅ES 등록 완료 (DQ-027 override · TASK-212-03)`.
  - **L598** 사상가 줄: `⚠️ ES 미등록(BLOCKER-1 · BLK-175E-2018A-001)` → `✅ ES 등록 완료 (DQ-027 override · TASK-212-03 · regan-claim-001~006 인용 가능)`.
  - **L629** 끝 줄: `⚠️ ES 미등록 (BLOCKER-1 · BLK-175E-2018A-001)` → `✅ ES 등록 완료 (DQ-027 override · TASK-212-03 · curl 실측 _doc/regan HTTP 200 · claims total=6)`.
  - **L597·L599 는 사상가 확정·trademark 본문 줄로 미수정** (BLOCKER 표기 아님 — 원문 보존).
- **study-guide/2024-B.md 정정 (10 곳 → ✅ES 등록 완료)**:
  - **L19** 표 row: `⚠️ ES 미등록 (1건 — BLOCKER 유지)` → `✅ ES 등록 완료 (DQ-027 override · TASK-212-03)`.
  - **L45** 공지: `regan 1명 BLOCKER 유지` → `regan 1명 ✅ ES 등록 완료 (DQ-027 override · TASK-212-03 · BLK-175E-2024B-006 해소)`.
  - **L51** 섹션 heading: `### Q8 (을) regan BLOCKER 유지` → `### Q8 (을) regan ES 등록 완료 (DQ-027 override · TASK-212-03)`.
  - **L53** 본문: `HTTP 404 · trademark 직접 인용 금지` → `HTTP 200 · claims total=6 · trademark 인용 가능 (regan-claim-001~006)`.
  - **L496** 사상가 확정 줄: `⚠️ES 미등록 · BLOCKER-1 · BLK-175E-2024B-006` → `✅ES 등록 완료 · DQ-027 override · TASK-212-03 · BLK-175E-2024B-006 해소` + `regan-claim-001~006` 인용 추가.
  - **L509** 후속 등록 대기 줄: `⚠️ES 미등록 · claim_id 인용 불가` → `✅ ES 등록 완료 · claim_id 인용 가능` + 핵심 ES claim 6건 인용 추가 (claim-001 내재적 가치 / -002 삶의 주체 7기준 / -003 존중의 원리 / -004 해악의 원리 / -005 의무론적 동물권 / -006 권리 행사자/보유자).
  - **L742 (구 L736)** Q8 row: `BLOCKER(404) · regan ⚠️BLOCKER-1 유지` → `HIT(6) · DQ-027 · regan ✅ DQ-027 override`.
  - **L749 (구 L743)** ES 상태 요약: `HIT 18명 · BLOCKER 1명 (regan)` → `HIT 19명 (… + 1 DQ-027 override: regan) · BLOCKER 0명`.
  - **L751 (구 L745)** DQ-019 줄: `regan 만 BLOCKER 유지` → `regan ✅ DQ-027 post-registration override`.
  - **L761 (구 L755)** 블로커 등록 줄: `BLK-175E-2024B-006 regan 유지` → `BLK-175E-2024B-006 regan 해소 → DQ-027`.
- **coverage/2018-A.md · coverage/2024-B.md 원본 변경 없음** (architecture.md "원본 수정 금지" 규정 준수 · BLOCKER 기록 유지 · DQ-027 로그로만 override).
- **trademark fabrication 방지**: 6 claims · 6 keywords · 2 relations 전원 출처 verbatim 사용 (coverage/2018-A.md L143-L165 + L286-L323 · coverage/2024-B.md L350-L385 · study-guide/2018-A.md L597-L629 · blocker-log.md L474-L484 + L946-L952) — 자기검증 3-step 산술 결과 Step 1 trademark 토큰 전원 verbatim 출처 보유 · Step 1 ∩ Step 1b ∩ Step 2 = 0 (`signal/ethics-study/coder-report-TASK-212-03.md` 기록).

### DQ 분류

- severity: observation
- 자동화 가능성: 가능 (TASK-212 mother 의 13명 ES 보강 시리즈 자동화 — `insert_{id}.py` 패턴 답습 · cho_sik (DQ-025) · schumpeter (DQ-026) · regan (DQ-027) 3건 동일 절차 · regan 은 단일 등록으로 2 BLOCKER 동시 해소 최초 사례)
- 재발 방지: TASK-212 시리즈 (sub 13건) 완주 후 retrospective 반영. 응용윤리 동물 윤리 영역 ES 커버리지 양대 입장 (공리주의 싱어 + 의무론 리건) 완성 — 향후 동물 윤리 출제 사상가 ES gap 발생 가능성 축소. 단일 등록으로 다 BLOCKER 동시 해소 가능한 사상가 (출제 빈도 ≥2) 우선 등록 패턴 확정.

---

### TASK-DQ-028 - 2026-04-28 — `zhiyi` post-registration override (2 BLOCKER 동시 해소 · TASK-212-04)
- files:
  - `projects/ethics-study/exam-solutions/study-guide/2022-A.md` (Q10 (나) 6 곳 정정)
  - `projects/ethics-study/exam-solutions/study-guide/2025-A.md` (Q8 7 곳 정정)
- issue: BLK-175E-2022A-006 (2022-A Q10 (나) `zhiyi` ES 미등록) + BLK-175E-2025A-004 (2025-A Q8 `zhiyi` ES 미등록) 두 BLOCKER가 study-guide 2022-A.md 6 곳 + 2025-A.md 7 곳 = **합계 13 곳**에 ⚠️BLOCKER 표기로 누적 기록되어 있었음. 본 세션 2026-04-28 TASK-212-04 ES 정식 등록 완료 (1 thinker + 1 work + 6 claims + 6 keywords + 2 relations) → 사후 정정 override **2 BLOCKER 단일 등록 동시 해소** (TASK-212 시리즈 2번째 사례 — regan DQ-027 에 이은 두 번째).
- impact: 동양 윤리 (eastern_ethics) 영역 중국 천태종(天台宗) 체계화 정점 인물 ES 커버리지 확장. 중국 불교 3대 종파 (천태·화엄·선종) 중 천태(zhiyi) 등록 완료 · 화엄(fazang) BLOCKER 잔존 · 선종(huineng) 등록 완료. 한국 천태종(고려 의천)·일본 천태종(사이초)의 사상적 원천 ES 등재로 동아시아 불교 전통 ES 추적성 확보.

### 개요

`zhiyi` (천태 지의, 天台 智顗, 538-597, 중국 수대 승려, 중국 천태종 실질 창시자·체계화 정점, 『마하지관(摩訶止觀)』·『법화현의(法華玄義)』·『법화문구(法華文句)』 천태 3대부 저자) 는 coverage/2022-A.md L24 작성 시점 (2026-04-21) 및 coverage/2025-A.md L333-L375 작성 시점 (2026-04-21) ES 미등록 상태 (HTTP 404 · claims=0) 로 BLK-175E-2022A-006 + BLK-175E-2025A-004 두 BLOCKER 동시 기록되었음. 본 세션 2026-04-28 TASK-212-04 으로 ES 정식 등록 완료 (1 thinker + 1 work + 6 claims + 6 keywords + 2 relations) → 사후 정정 override **2 BLOCKER 단일 등록 동시 해소** (TASK-212 시리즈 regan DQ-027 에 이은 두 번째 사례).

DQ-024 (false-positive override) 와 분리: DQ-024 는 **false-positive override**, DQ-025 (cho_sik) · DQ-026 (schumpeter) · DQ-027 (regan) · DQ-028 (zhiyi) 는 **post-registration override**. DQ-028 은 동양 윤리 (eastern_ethics) 영역 중국 천태종(天台宗) 체계화 정점 인물의 ES 커버리지 공백 완성 — 중국 불교 3대 종파 (천태·화엄·선종) 중 천태 축 추가로 동아시아 종학(宗學) 전통 ES 커버리지 확장.

### coverage md 주장 vs ES 실측

| thinker_id | coverage md 주장 (2026-04-21) | 2026-04-28 ES 실측 (등록 직후) | 판정 |
|---|---|---|---|
| zhiyi | MISS · BLK-175E-2022A-006 (Q10 (나) · 2회째 출제 · 오시팔교·방등시·돈점) + BLK-175E-2025A-004 (Q8 · row 기준 2회 출제 · 삼제원융·일심삼관·화법4교·화의4교 · 智顗 trademark 직접 인용 금지) | thinker=200 · claims=6 (TASK-212-04 신규 등록) | **DQ-028 post-registration override (2 BLOCKER 동시 해소)** |

### 등록 산출물 (TASK-212-04)

```bash
# 실측 curl (2026-04-28 TASK-212-04 등록 완료 직후)
curl -s -o /dev/null -w "%{http_code}\n" "http://localhost:9200/ethics-thinkers/_doc/zhiyi"
# 200

curl -s "http://localhost:9200/ethics-claims/_search?q=thinker_id:zhiyi&size=0" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['hits']['total']['value'])"
# 6
```

- **thinker**: `zhiyi` — name="천태 지의 (天台 智顗)" · name_en="Zhiyi" · field="eastern_ethics" · era="고대" · birth=538 · death=597.
- **works (1건)**: `zhiyi-tiantai-3-1` (천태 3대부 / 天台三大部 — 摩訶止觀·法華玄義·法華文句).
- **claims (6건)**:
  - `zhiyi-claim-001` 삼제원융 (三諦圓融) — 공제·가제·중제 삼제의 원융 융합 · 인도 이제(二諦) 천태 확장 · 2025-A Q8 ㉠ 정답.
  - `zhiyi-claim-002` 일심삼관 (一心三觀) — 삼제가 한 마음에 구족·동시 관 · 원돈 지관법 · 마하지관 권5 · 2025-A Q8 ㉡ 정답 (일심).
  - `zhiyi-claim-003` 오시 교판 — 화엄시·녹원시·방등시·반야시·법화열반시 · 2022-A Q10 (나) ㉡ 정답 (방등시).
  - `zhiyi-claim-004` 화법 4교 (化法四敎) — 가르침의 내용 기준 분류: 장교·통교·별교·원교 · 2025-A Q8 ㉢ 정답.
  - `zhiyi-claim-005` 화의 4교 (化儀四敎) — 가르침의 방식·설법 형식 기준 분류: 돈교·점교·비밀교·부정교 · 2022-A 갑(신수) 점수·을(혜능) 돈오 대응 · 2025-A Q8 ㉣ 정답.
  - `zhiyi-claim-006` 일념삼천 (一念三千) — 한 마음의 한 순간에 삼천 세계 구족 · 성구설(性具說) 근거 · 천태 우주론 정점.
- **keywords (6건)**: three-truths-fusion · one-mind-three-contemplations · five-periods · four-doctrinal-teachings · four-formal-teachings · three-thousand-realms.
- **relations (2건)**: zhiyi → wonhyo (influenced · 천태 통섭 사상의 한국 화쟁 영향) · zhiyi → huineng (parallel · 중국 불교 종학 양대 축 — 교학 vs 직관).

### 추정 원인

- TASK-176 (2026-04-22 DONE) 은 `exam-coverage-map.md` Section D **TOP10 (출제 빈도 ≥3)** 만 다뤘음 — zhiyi 는 출제 빈도 2 (2022-A · 2025-A) 로 후순위 (Manager spec L379 "3회 실측" 은 부정확, 실제 row 기준 2회).
- TASK-212 (mother) 잔존 13명 ES 보강 시리즈에서 zhiyi 는 동양 윤리 중국 불교 종학 영역 ES 커버리지 공백 (선종 huineng HIT, 천태 zhiyi · 화엄 fazang 부재) 해소 목적으로 HIGH 우선순위 부여 → TASK-212-04 으로 분리 등록.
- 단일 사상가 등록으로 2 BLOCKER (BLK-175E-2022A-006 + BLK-175E-2025A-004) 동시 해소 — TASK-212 시리즈 regan DQ-027 에 이은 두 번째 사례.

### 조치

- **study-guide/2022-A.md 정정 (6 곳 → ✅ES 등록 완료)**:
  - **L20** 표 row: `⚠️ ES 미등록 (4명 — BLOCKER 유지) | green_th · shenxiu · zhiyi · beccaria` → `⚠️ ES 미등록 (3명 — BLOCKER 유지) + ✅ ES 등록 완료 (1명 · DQ-028 override) · zhiyi (Q10 나) ✅ ES 등록 완료 (DQ-028 override · TASK-212-04 · BLK-175E-2022A-006 해소)`.
  - **L715** Q10 heading: `## 문항 10 ... 신수(BLOCKER) + 혜능 + 지의(BLOCKER)` → `## 문항 10 ... 신수(BLOCKER) + 혜능 + 지의(✅ DQ-028 override · TASK-212-04)`.
  - **L752** 사상 identification 줄: `(⚠️ BLOCKER BLK-175E-2022A-006 / ES 미등록)` → `(✅ ES 등록 완료 · DQ-028 override · TASK-212-04 · BLK-175E-2022A-006 해소 · zhiyi-claim-001~006 인용 가능)`.
  - **L772** zhiyi BLOCKER 본문: `⚠️ zhiyi: ES 미등록 ... 표준 해설에 근거` → `✅ zhiyi: ES 등록 완료 ... claims total=6 · zhiyi-claim-003 (오시 교판) · zhiyi-claim-004 (화법 4교) · zhiyi-claim-005 (화의 4교) 정전 claim 인용`.
  - **L788** 풀이 과정 줄: `(⚠️ 지의는 BLK-175E-2022A-006)` → `(✅ 지의 ES 등록 완료 · DQ-028 override · TASK-212-04)`.
  - **L1002** 잔존 BLOCKER 줄: `⚠️ 잔존 BLOCKER (4명): green_th · shenxiu · zhiyi · beccaria` → `⚠️ 잔존 BLOCKER (3명): green_th · shenxiu · beccaria. zhiyi 는 DQ-028 override 로 해소됨 (TASK-212-04, BLK-175E-2022A-006 해소)`.
- **study-guide/2025-A.md 정정 (7 곳 → ✅ES 등록 완료)**:
  - **L19** 표 row: `⚠️ ES 미등록 (1건 — BLOCKER 유지) · zhiyi (Q8 · BLK-175E-2025A-004)` → `✅ ES 등록 완료 (1건 · DQ-028 override) · zhiyi (Q8 · BLK-175E-2025A-004 해소) · TASK-212-04 (2026-04-28) · curl 실측 HTTP 200 · claims total=6`.
  - **L40** 공지: `(ES 등록 13명 + 잔존 BLOCKER 1명 zhiyi)` → `(ES 등록 13명 + DQ-028 override 1명 zhiyi · 잔존 BLOCKER 0명)`.
  - **L50** 섹션 heading: `### zhiyi BLOCKER 유지 — Q8 천태종 trademark 직접 인용 금지` → `### zhiyi ES 등록 완료 — Q8 천태종 trademark 직접 인용 가능 (DQ-028 override · TASK-212-04)`.
  - **L52** 본문: `**Q8 zhiyi**: 본 세션 2026-04-23 curl 재측정 결과 HTTP 404 유지 ... claim_id 인용은 생략` → `본 세션 2026-04-28 TASK-212-04 ES 등록 완료 ... zhiyi-claim-001~006 으로 직접 인용 가능`.
  - **L415** Q8 heading: `## 문항 8 ... ⚠️ BLOCKER (BLK-175E-2025A-004 유지)` → `## 문항 8 ... ✅ DQ-028 override (TASK-212-04 · BLK-175E-2025A-004 해소)`.
  - **L434** BLOCKER 유지 본문: `⚠️ BLOCKER 유지 (BLK-175E-2025A-004) ... 智顗 trademark 직접 인용(claim_id 기반)은 생략한다` → `✅ DQ-028 override (BLK-175E-2025A-004 해소 · TASK-212-04) ... zhiyi-claim-001~006 직접 인용 가능 (claim-001 삼제원융 · claim-002 일심삼관 · claim-003 오시 교판 · claim-004 화법 4교 · claim-005 화의 4교 · claim-006 일념삼천)`.
  - **L445** ES 근거 줄: `⚠️ zhiyi — BLOCKER (BLK-175E-2025A-004) ... 직접 claim 인용 금지 ... TASK-176 후속 처리 대상` → `✅ zhiyi — ES 등록 완료 (DQ-028 override · TASK-212-04 · BLK-175E-2025A-004 해소) ... 직접 claim 인용 가능 ... 등록된 claim 6건 인용`.
- **coverage/2022-A.md · coverage/2025-A.md 원본 변경 없음** (architecture.md "원본 수정 금지" 규정 준수 · BLOCKER 기록 유지 · DQ-028 로그로만 override).
- **trademark fabrication 방지**: 6 claims · 6 keywords · 2 relations 전원 출처 verbatim 사용 (coverage/2022-A.md L24 · coverage/2025-A.md L333-L375 · blocker-log.md L726-L734 + L976-L982) — 자기검증 3-step 산술 결과 Step 1 user-facing trademark 토큰 0건 (코드/메타 제외) · Step 1b macron `śamatha-vipaśyanā` (docstring 만, 출처 verbatim) · Step 2 `Tiantai school` (출처 verbatim) · Step 1 ∩ Step 1b ∩ Step 2 = 0 (`signal/ethics-study/coder-report-TASK-212-04.md` 기록).

### DQ 분류

- severity: observation
- 자동화 가능성: 가능 (TASK-212 mother 의 13명 ES 보강 시리즈 자동화 — `insert_{id}.py` 패턴 답습 · cho_sik (DQ-025) · schumpeter (DQ-026) · regan (DQ-027) · zhiyi (DQ-028) 4건 동일 절차 · zhiyi 는 단일 등록으로 2 BLOCKER 동시 해소 사례 (regan 에 이은 두 번째))
- 재발 방지: TASK-212 시리즈 (sub 13건) 완주 후 retrospective 반영. 동양 윤리 중국 불교 종학 영역 ES 커버리지 — 천태(zhiyi) ✅ 등록 · 선종(huineng) ✅ 등록 · 화엄(fazang) ⚠️ BLOCKER 잔존 (TASK-212-05 후속 등록 권고). 단일 등록으로 다 BLOCKER 동시 해소 가능한 사상가 (출제 빈도 ≥2) 우선 등록 패턴 재확증 (regan DQ-027 + zhiyi DQ-028).
