---
task_id: TASK-189-T
verdict: PASS
severity: observation
agent: tester(opus)
timestamp: 2026-04-22T00:00:00+09:00
---

# Tester Report: TASK-189-T — 2017-B study-guide.md 학생용 해설 검증 (10항 체크)

## 검증 대상

- **파일**: `/home/jai/program-agent/projects/ethics-study/exam-solutions/study-guide/2017-B.md` (744 lines, `wc -l` 실측)
- **입력 원천**: `/home/jai/program-agent/projects/ethics-study/exam-solutions/coverage/2017-B.md` (229 lines, `wc -l` 실측)
- **Coder report 참조**: `/home/jai/program-agent/signal/ethics-study/coder-report-TASK-189.md` (17 Edit · 22 토큰 해소 주장)
- **선례 검증 완료 태스크**: TASK-188-T (2017-A PASS 10/10) · TASK-187-T (2016-B PASS 10/10)

## 10항 체크 결과

| # | 항목 | 기대 | 실측 | 판정 |
|---|------|------|------|------|
| 1 | 8문항 전수 커버 (서술형 Q1~Q8) | `^## 문항` 헤더 == 8 | Q1(L43)·Q2(L107)·Q3(L176)·Q4(L239)·Q5(L311)·Q6(L389)·Q7(L475)·Q8(L588) = 8건 | ✅ PASS |
| 2 | 섹션 헤더 line metadata 실재 | L14-L22·L26-L32·L36-L42·L46-L55·L59-L67·L71-L77·L81-L89·L93-L101 | 8개 header 전원 해당 metadata 문자열 포함 (grep 확인) | ✅ PASS |
| 3 | 제시문 verbatim byte-level 일치 (HTML `<u>` 9쌍 · 괄호 영문 · 한자 · 특수 기호) | study-guide 9쌍 / coverage 9쌍 (row 37 NOTE 1건 제외) | study-guide: `<u>` 9 · `</u>` 9 balanced · coverage: 실제 제시문 `<u>` 9쌍 (L175 row 37 NOTE 1건은 메타 주석) | ✅ PASS |
| 4 | ES 등록 10 thinker_id 전수 curl `found=true` (rawls·habermas·buddha·kant·sartre·laozi·zhuangzi·mozi·gilligan·noddings) | 10/10 found=True | 10/10 found=True (curl `localhost:9200/ethics-thinkers/_doc/{id}` 실측) | ✅ PASS |
| 5 | 대표 claim_id 전수 curl `found=true` (≥10건) | 10/10 | `{thinker}-claim-001` 10건 모두 found=True · 집계: kant 18 · rawls 15 · gilligan 12 · laozi 12 · noddings 12 · buddha 10 · zhuangzi 10 · habermas 8 · sartre 8 · mozi 7 (총 112건) | ✅ PASS |
| 6 | BLOCKER 0건 확증 | coverage L36 "정식 블로커 0건, NOTE-BLOCKER 0건" + L210-L211 재확증 | coverage L36 + L210-L211 명시 0건 일치 | ✅ PASS |
| 7 | Q3 "해당 없음 (교과교육학 · 통일교육 · 민족주의 유형)" + Q5 "해당 없음 (교과교육학 · 응용윤리 · 안락사 유형)" 분류 사유 명시 | 2건 모두 명시 | L20 ES 상태 표 + L219 (Q3) · L362 (Q5) 본문 상세 서술 | ✅ PASS |
| 8 | 서술형 8문항 전원 `### 채점 기준` 서브섹션 실재 (배점 4/4/4/4/4/5/5/10) | 8 subsection, 배점 일치 | L91(Q1 총 4점)·L158(Q2 4점)·L221(Q3 4점)·L291(Q4 4점)·L364(Q5 4점)·L451(Q6 5점)·L556(Q7 5점)·L707(Q8 10점) = 4+4+4+4+4+5+5+10 == 40점 | ✅ PASS |
| 9 | Q6(갑·을)·Q7(갑·을·병)·Q8(가·나) 다인 문항 label 분리 서술 실재 | label 기반 정답 분리 | Q6: "갑 = 임마누엘 칸트" / "을 = 장폴 사르트르" (L394-L400) · Q7: "갑 = 노자" / "을 = 장자" / "병 = 묵자" (L492-L500) · Q8: "(가) 캐롤 길리건" / "(나) 넬 나딩스" (L611-L612) | ✅ PASS |
| 10 | 자기검증 2단계 + Greek/Cyrillic 확장 + 한자 래퍼 em-dash 바이트 재검증 | bare-paren 영어 0-hit 0건 · Greek/Cyrillic 0개 · TitleCase 19/19 hit · 한자—영어 em-dash E2 80 94 3+ 샘플 | 아래 상세 | ⚠️ PASS (wrapper exception 1건 observation) |

## 10항-(c) 자기검증 재실행 상세

### Step 1 · bare-paren 영어 토큰

- **추출** (`LC_ALL=C.UTF-8 grep -oE '\([A-Za-z][^)]*\)'`): 81 unique, 관리 토큰 제거 후 56 개.
- **coverage 2017-B.md 역grep 결과**:
  - **외곽 wrapper 그대로 0-hit**: 34개 (Coder report 언급 wrapper false-positive 현상).
  - **inner token 해체 후 재검증**: 외곽 wrapper 0-hit 토큰 34개 중 33개는 내부 핵심 영어 단어(`Lebenswelt`·`das Erhabene`·`best self`·`projet`·`veil of ignorance`·`confirmation`·`modeling`·`discourse`·`practice`·`dialogue`·`one-caring`·`cared-for`·`l'existence précède l'essence` 등)가 coverage ≥1 hit 확증.
  - **예외 1건 (observation 대상)**: `(Buddha, 석가모니, 고타마 싯다르타)` 의 inner segment `고타마 싯다르타` (Korean Hangul-only 토큰) 가 coverage 0-hit. 단, 같은 wrapper의 `Buddha` (cov 2 hits) 및 `석가모니` (cov 2 hits)는 모두 그라운딩되며, `고타마 싯다르타` 는 `buddha` ES thinker의 표준 속명으로 학생용 해설 맥락에서 동의어 확장에 해당. bare-paren "영어" 토큰 regex 대상 외 (한글 전용)이므로 본 검증 범위 밖이나, 투명성 차원에서 observation 로 기록.

### Step 1b · Greek/Cyrillic `\([^)]*[α-ωΑ-Ωа-яА-Я][^)]*\)`

- Python regex (`\u0370-\u03FF` · `\u0400-\u04FF`) 실측 추출: **0개** (본 연도 문항 그리스어·키릴문자 병기 대상 없음)
- Coder report 의 claim 과 일치.

### Step 2 · TitleCase `[A-Z][a-z]+(\s+[A-Za-z][a-z]+){1,5}`

- 추출: 19 unique.
- coverage 역grep: **19/19 전원 ≥1 hit** (Carol Gilligan · Different Voice · Discourse Principle · Existentialisme est un humanisme · Formula of Humanity · Immanuel Kant · James Rachels · John Rawls · Karen Ann Quinlan · Kolonisierung der Lebenswelt · Nancy Cruzan · Nel Noddings · Paul Sartre · The Challenge to Care in Schools · Theorie des kommunikativen Handelns · Theory of Justice · Tom Beauchamp · Universalization Principle · Zweck an sich).
- Coder report 표와 100% 일치.

### 한자(漢字) — 영어 래퍼 em-dash U+2014 byte-level 보존 (Q7 노자·장자·묵자 집중)

Python 바이너리 read + `.find(b'\xe2\x80\x94')` 검증:

| # | 샘플 | 파일 offset | em-dash 바이트 | 판정 |
|---|------|-------------|-----------------|------|
| 1 | `無爲之治 — 무위의 다스림` (Q7 노자 trademark) | 63031 | `e2 80 94` | ✅ U+2014 |
| 2 | `照之於天 — 하늘에 비추어 봄` (Q7 장자 trademark) | 63746 | `e2 80 94` | ✅ U+2014 |
| 3 | `兼愛 — jian-ai` (Q7 묵자 trademark) | 64507 | `e2 80 94` | ✅ U+2014 |

총 em-dash 카운트 (study-guide): 206 (coder report 일치) · 커버리지: 301 (Manager 주석+커버리지 자체 사용).

## 이슈/블로커

- **없음 (blocker=0, bug=0)**.
- **observation 1건**: Step 1 외곽 wrapper `(Buddha, 석가모니, 고타마 싯다르타)` 의 Korean Hangul segment `고타마 싯다르타` 가 coverage 역grep 0-hit. wrapper 전체로는 `Buddha` + `석가모니` 가 grounded 이므로 content-level 결함 아님 (buddha ES thinker 표준 속명의 동의어 확장). 투명성·추후 회귀 예방 목적 기록.
  - Coder report Step 1 표(40 core token) 에는 이 wrapper가 inner segment 별로 분해 기록되지 않아 누락. 이후 동형 태스크(2018-B 이후)에서는 wrapper 전체 0-hit 시 inner segment 별 검증을 명시하도록 agents/coder.md L89-L115 Step 1 프로토콜에 "wrapper decomposition" 절차 추가를 권장 (manager 판단).

## 최종 판정

- **verdict = PASS** (10/10 항목 통과).
- **severity = observation** (1건 — content-level bug 아님, 투명성 기록).
- **근거 요약**:
  - 8문항 전수 커버 + `### 채점 기준` 8개 + 배점 합 40점 정확.
  - HTML `<u>` 9/9 balanced · 섹션 헤더 line metadata 8개 전수 일치.
  - ES 10 thinker + 10 대표 claim_id curl `found=true` 100%.
  - BLOCKER 0 · Q3/Q5 교과교육학 분류 사유 명시 · Q6/Q7/Q8 다인 label 분리 전수 실재.
  - Step 1 bare-paren / Step 1b Greek-Cyrillic / Step 2 TitleCase 재grep 결과 Coder 주장 100% 재현 (core trademark 40+ · 인명 19 · TitleCase 19 모두 ≥1 hit).
  - Q7 한자 — 영어 em-dash 3샘플 hexdump `e2 80 94` 바이트 보존 확증.
- **Manager 액션**: 추가 FIX 태스크 불필요. observation 1건 은 retrospective/agents-doc 개선 제안으로 이월.
