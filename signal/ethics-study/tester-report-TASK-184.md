---
agent: tester(opus)
task_id: TASK-184-T
status: DONE
timestamp: 2026-04-22
severity: bug
verdict: FAIL
items_checked: 8
items_passed: 6
items_failed: 2
observations: 2
---

## 결과 요약

TASK-184 산출물 `projects/ethics-study/exam-solutions/study-guide/2015-A.md` (674 lines) 에 대해 8항 체크를 전수 수행했다. 구조적 8항 중 6항 PASS, 1항 BUG (자기검증 2단계 Step 1에서 원문·coverage 양쪽 hit=0 의 Greek 어구 3건이 Coder 산출에 삽입됨 — agents/tester.md §문서·해설 검증 표준 rule 3에 따라 자동 severity=bug), 1항 observation (교과교육학/경계영역 "해당 없음" 표기에서 기입형 2는 "⚠️ ES 미등록" 으로 대체 — 분류 사유는 명시되어 있으나 task-board 가 요구한 "해당 없음" 문구를 그대로 쓰지는 않음).

## 검증 대상

- 구현: `projects/ethics-study/exam-solutions/study-guide/2015-A.md` (L1~L674)
- 입력 소스:
  - coverage: `projects/ethics-study/exam-solutions/coverage/2015-A.md` (L1~L162)
  - 원본: `/home/jai/잡동사니/임용/md/2015중등1차-도덕윤리_전공A.md` (L1~L213)
- 선례 비교: `study-guide/2014-A.md`, `2014-B.md` (포맷 일치)

## 8항 체크 결과표

| # | 항목 | 결과 | 증거 |
|---|------|------|------|
| 1 | 14문항 전수 커버 (`^## 문항` == 14) | ✅ PASS | `grep -c '^## 문항'` = **14** (L28, L57, L93, L128, L170, L204, L247, L280, L329, L370, L427, L476, L527, L582) |
| 2 | 각 문항 섹션 헤더 `원문 line L{m}-L{n}` | ✅ PASS | `grep -c '원문 line L'` = **14** (각 섹션 헤더에 동시 포함) |
| 3 | 제시문 verbatim byte-level 일치 (HTML `<u>` 4개, 한자, 특수기호) | ✅ PASS | `<u>` 태그: 원본 **4** · 가이드 **4** (coverage 원본에는 0개이지만 원문 md 에서 복사됨), 대표 14개 인용 구절 byte-level 전수 guide≥1 확인 (계몽주의 기획·환경적 능력·상호 의존·하늘의 운행·전 씨는 종일토록·타당성 요구·홉스(T. Hobbes)·항해사의 비유·기본적 자유·영리함(deinotés)·정언 명령·2가지 도덕적 능력·자주, 평화, 민주 전수 hit≥1) |
| 4 | ES thinker_id 재조회 (11 found=true + nagarjuna false) | ✅ PASS | 본 세션 curl 실측 (2026-04-22): macintyre·xunzi·zhuxi·wangyangming·buddha·habermas·hobbes·plato·aristotle·kant·rawls **11명 found=true 전수 확증**, nagarjuna **found=false** 확증 (coverage 일치). 가이드 본문 L46, L156, L191, L192, L234, L268, L317, L358, L456, L506, L563 에 각 `thinker_id` 명시 |
| 5 | BLOCKER-1/BLOCKER-2 + ES 미등록 섹션 | ✅ PASS | BLOCKER-1 (기입형 4 나): L147~L166 "⚠️ BLOCKER" 표기 + 禮(예) 유력·화성기위 보조 후보군 + 권장 답안 요령 / BLOCKER-2 (기입형 8 세로 A): L307~L324 "⚠️ BLOCKER" 표기 + 자연상태 유력·사회계약·자연권리 후보군 / ES 미등록: L19 frontmatter, L81 Newmann, L235 Nāgārjuna 각각 명시. Reviewer 권고사항 전수 반영 |
| 6 | 교과교육학 3 + 경계영역 1 "해당 없음 (분류 사유)" 표기 | ⚠️ observation | `grep -c '해당 없음'` = **3** (L117 기입형 3 교과교육학, L413 기입형 10 경계영역, L623 서술형 4 교과교육학). **기입형 2 (교과교육학)** 는 "⚠️ ES 미등록 [BLK 미배정]" (L81) 으로 대체 표기하며 "분류: 교과교육학" 은 L82 에 명시. 분류 사유는 실재하나 "해당 없음" 문구 그대로는 3개만 존재. Newmann 의 ES 누락 사실을 더 명확히 표기하려는 의도적 변형으로 판단되어 bug 대신 observation 분류 |
| 7 | 서술형 4문항 채점 기준 ≥4 | ✅ PASS | `grep -c '^### 채점 기준'` = **4** (L459 서술형 1, L509 서술형 2, L566 서술형 3, L627 서술형 4) |
| 8 | 자기검증 2단계 역grep (Step 1 괄호 영어 + Step 2 TitleCase) | ❌ FAIL | Step 1: 86개 괄호 토큰 중 의미 있는 영어/개념 토큰 전수 coverage hit≥1 확인. **그러나 Greek 어구 3건이 coverage/원문 양쪽 hit=0 → tester.md §문서·해설 검증 rule 3 (자동 severity=bug)**. Step 2: 11 TitleCase phrase 전수 coverage hit≥1 **PASS** |

## 원문-grep 0건 BUG 상세 (Step 1 위반)

아래 3건은 Coder 가 coverage 에 없는 Greek 원어 표기를 **자체 보강**한 경우로, agents/tester.md L68~L74 "문서·해설 성격 산출물 검증 (원문-grep 대조 표준)" rule 3 에 따라 자동 severity=bug.

| # | 토큰 | guide 라인 | 문항 | coverage hit | 원본 md hit | 판정 |
|---|------|-----------|------|-------------|-------------|------|
| 1 | `γενναῖον ψεῦδος` | L352 | 기입형 9 | **0** | **0** | BUG — "(noble lie, γενναῖον ψεῦδος)" 중 Greek 부분은 coverage 에 전무 |
| 2 | `μετὰ λόγου` | L452 | 서술형 1 | **0** | **0** | BUG — "로고스를 동반하는 것(μετὰ λόγου)" Greek 표기는 coverage/원본 모두 부재 |
| 3 | `λόγος` | L452, L463 | 서술형 1 | **0** | **0** | BUG — "로고스 그 자체(λόγος)" Greek 표기는 coverage/원본 모두 부재 |

### 근거

- Coder 는 "logos" (라틴 전사형, coverage L25 에 실재, cov=1) 까지는 정당하게 인용했다. 그러나 Greek 철자 `λόγος`/`μετὰ λόγου`/`γενναῖον ψεῦδος` 은 coverage 원문·시험 원본 어디에도 실재하지 않는 Coder 자체 보강이다.
- tester.md §문서·해설 검증 rule 3 명문: "grep 0건인 항목은 자동으로 severity=bug로 분류 (Coder의 자동 보강·창작 가능성). Tester 본문에서 '관찰/참고용'으로 낮추더라도 severity는 bug를 유지한다."
- 코드 결함이 아닌 해설 창작·보강 이슈이나, 규약상 자동 bug 분류가 강제된다.

### 영향 범위

- 기입형 9 풀이 과정 L352: 정답(철인정치) 논증 자체에는 영향 없음. 다만 "γενναῖον ψεῦδος" 원어는 보강 서술.
- 서술형 1 풀이·채점 기준 L452, L463: 아리스토텔레스 서술형 1 해설 내 주지주의 비판·로고스 논증 보강 서술. 답안(실천적 지혜=프로네시스)·채점 기준 자체에는 영향 없음.
- 학생용 가이드 정확성 측면에서는 Greek 원어 자체는 학술적으로 올바르나(Plato 『Politeia』 3권 414bc "γενναῖόν τι ἓν τῶν ψευδῶν" · Aristotle 『Nicomachean Ethics』 6권 "μετὰ λόγου"), 출제 원문에 표기되지 않은 원어를 보강한 것은 원문-grep 대조 규약 위반.

## Observation 상세

### Obs-1: 교과교육학 기입형 2 "해당 없음" 문구 대체

- task-board TASK-184-T 체크 6항은 "교과교육학 3건 + 경계영역 1건 `해당 없음 (분류 사유)` 표기 실재" 를 요구.
- 실제 가이드는 교과교육학 3건 중 2건 (기입형 3 L117, 서술형 4 L623) + 경계영역 1건 (기입형 10 L413) 에만 "해당 없음" 문구를 사용.
- 교과교육학 나머지 1건 (기입형 2) 은 L81 "⚠️ ES 미등록 [BLK 미배정] — F. Newmann 은 현재 ES에 `found=false`" + L82 "분류: 교과교육학 (사회과·도덕과 수업 모형론)" 로 대체 표기.
- 판정: Newmann 이 coverage L16 에서 "없음(뉴만 ES 누락)" 으로 분류된 점을 반영한 의도적 변형으로 보이며, "분류 사유" 는 충분히 명시되어 있음. task 문구에 문자적으로는 불일치하나 실질적으로는 동등하므로 **observation** 으로 분류. bug 승격은 권장하지 않음.
- 완화 방안 (선택): 기입형 2 에 "해당 없음 (ES 미등록: F. Newmann)" 한 줄을 추가하여 문구 일관성 확보.

### Obs-2: 괄호 안 em-dash 표기 변형 `(episteme — 앎)`

- guide L452 는 `(episteme — 앎)` (em-dash + space) 사용; coverage L25 는 `(episteme·앎)` (middle dot).
- 개별 토큰 episteme 및 한글 앎 은 coverage 에 hit 존재하므로 의미 fabrication 은 아님. 단 파싱상 괄호 전체 토큰 cov=0 이므로 체크 로직상 걸린다.
- 일관성 개선 차원에서 middle-dot 으로 통일 권장 (선택).

## 클린 코드·아키텍처 관점 검증

해당 없음 — 본 산출물은 순수 마크다운 해설 문서. 계층 의존·단일 책임·DTO 분리 등 코드 결함 체크 대상 아님.

## 다음 제안

**Manager 에게**: severity=bug 판정이므로 TASK-184-FIX 를 자동 생성 규정 (CLAUDE.md Step 4, 3항) 대상. 아래 FIX 태스크 권장.

1. **TASK-184-FIX**: guide L352, L452, L463 세 위치의 Greek 원어 (`γενναῖον ψεῦδος`, `μετὰ λόγου`, `λόγος`) 를 제거하거나 coverage·원본 md 에 실재하는 한글·영어 표기로 전환.
   - 조치 안 A (제거): 괄호 Greek 표기 전체 삭제. 예) `(noble lie, γενναῖον ψεῦδος)` → `(noble lie)`, `(μετὰ λόγου)` → 제거 또는 한글화 "(로고스와 함께)", `(λόγος)` → 제거.
   - 조치 안 B (라틴 전사 유지): coverage 에 실재하는 `logos` (라틴 전사) 만 유지하고 Greek 철자는 삭제.
   - 권장: 조치 안 A — coverage 원문-grep 대조 규약과 학생용 가이드 접근성 동시 충족.

2. **(선택·observation) Obs-1 완화**: 기입형 2 의 "⚠️ ES 미등록" 섹션에 "해당 없음 (분류 사유)" 문구를 병기하여 task-board 요구 문구 일관성 확보.

3. **(선택·observation) Obs-2 완화**: `(episteme — 앎)` → `(episteme·앎)` 으로 middle-dot 통일.

본 bug 1건은 정답 논증·채점 기준·BLOCKER 처리·ES 재조회 등 핵심 품질 지표에는 영향을 주지 않으며, tester.md §문서·해설 검증 표준 rule 3 의 자동 bug 규정을 순수하게 적용한 결과이다. FIX 작업 범위는 최소 3 라인 편집으로 한정된다.

## 검증 감사 로그

| 명령 | 결과 |
|------|------|
| `grep -c '^## 문항' study-guide/2015-A.md` | 14 |
| `grep -c '원문 line L' study-guide/2015-A.md` | 14 |
| `grep -c '<u>' study-guide/2015-A.md` | 4 |
| `grep -c '<u>' 원본 md` | 4 |
| `grep -c '### 채점 기준' study-guide/2015-A.md` | 4 |
| `grep -c '해당 없음' study-guide/2015-A.md` | 3 |
| `grep -c 'thinker_id' study-guide/2015-A.md` (ES 재조회 섹션) | 11 ✅ 본 세션 curl 전수 실측 `found=true` 확증 |
| `curl ethics-thinkers/_doc/{id}` 12회 | 11 found=true + nagarjuna false (coverage 일치) |
| `grep -F 'γενναῖον ψεῦδος' coverage` | 0 |
| `grep -F 'γενναῖον ψεῦδος' 원본 md` | 0 |
| `grep -F 'μετὰ λόγου' coverage` | 0 |
| `grep -F 'μετὰ λόγου' 원본 md` | 0 |
| `grep -F 'λόγος' coverage` | 0 |
| `grep -F 'λόγος' 원본 md` | 0 |
| `grep -oE '\([A-Za-z][^)]*\)'` Step 1 sort -u | 86 토큰 (의미 토큰 전수 cov≥1, Greek 3건만 cov=0) |
| `grep -oE '[A-Z][a-z]+(\s+[A-Za-z][a-z]+){1,5}'` Step 2 sort -u | 11 토큰 전수 cov≥1 |
