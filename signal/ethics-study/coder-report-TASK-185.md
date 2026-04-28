---
agent: coder
task_id: TASK-185
status: DONE
timestamp: 2026-04-22T19:30:00
---

## 결과 요약

2015학년도 중등임용 도덕·윤리 전공 B 학생용 풀이 가이드 `projects/ethics-study/exam-solutions/study-guide/2015-B.md` 신규 작성을 완료했다. 6문항(서술형 1~4 + 논술형 1~2, 배점 합계 40점) 전수 커버, 원문 verbatim 인용 + HTML `<u>` 보존 + 한자+한글 병기, 전수 ES 등록(TASK-DQ-007 override 반영으로 ⚠️ES 미등록 0건), NOTE-BLOCKER-1(논술형 2 갑 퇴계 출전 편 미확정) 주석 반영, 자기검증 2단계 프로토콜 + Greek/Cyrillic 확장 검사 PASS 산출물.

## 변경된 파일

- `projects/ethics-study/exam-solutions/study-guide/2015-B.md` (신규, 62,914 byte, 529 lines)

## 완료 조건 검증 표 (8항목)

| # | 완료 조건 | 검증 방법 | 결과 |
|---|----------|-----------|------|
| 1 | 파일 `study-guide/2015-B.md` 생성 | `ls -la` | ✅ 신규 생성 확인 (62914 byte) |
| 2 | 6문항 전수 커버 | `grep -c '^## 문항' study-guide/2015-B.md` | ✅ == 6 |
| 3 | 각 섹션 헤더 `원문 line L{m}-L{n}` metadata | `grep -cE '원문 line L[0-9]+-L[0-9]+'` | ✅ 6건 전수 (L14-L31, L35-L41, L45-L51, L55-L67, L75-L81, L89-L91) |
| 4 | 제시문 verbatim byte-level 일치 | 각 문항 핵심 문장 `grep -Fc` | ✅ 14개 샘플 문장 hit≥1 전수 확증 (HTML `<u>` 태그 4쌍 보존 포함) |
| 5 | thinker_id/claim_id `_doc` found=true 재조회 | `curl ethics-thinkers/_doc/{id}` + `ethics-claims/_doc/{id}` | ✅ 11 thinker 전수 found=true (⚠️ES 미등록 0건), 샘플 11 claim_id 전수 found=true |
| 6 | NOTE-BLOCKER-1 주석 논술형 2 섹션 실재 | `grep 'NOTE-BLOCKER-1'` + `grep '출전 미확정'` | ✅ 논술형 2 섹션 (L386) 경고 블록 삽입 + 상단 공지(L37)·본론(L404/L470)·부록(L514) 연계 참조 |
| 7 | 각 문항 `### 채점 기준` 서브섹션 | `grep -c '^### 채점 기준'` | ✅ == 6 (전원 실재) |
| 8 | 자기검증 2단계 + Greek/Cyrillic 확장 결과 표 coder-report 포함 | 본 report 아래 자기검증 섹션 | ✅ 표 4개 포함 (Step 1 영어 / Step 1 확장 Greek / Step 2 TitleCase / 원본 verbatim 샘플) |

## 자기검증 2단계 프로토콜 결과 (agents/coder.md L89-L115 엄수)

검증 대상: `projects/ethics-study/exam-solutions/study-guide/2015-B.md` (학생용 md 본문).
역-grep 대상: `projects/ethics-study/exam-solutions/coverage/2015-B.md` (case-sensitive, `LC_ALL=C.UTF-8 grep -Fc`).

### Step 1 — 괄호 안 영어 토큰 (유의미 토큰만, 메타 레이블·줄번호·TASK ID 제외)

| 토큰 | coverage hit | 처리 |
|------|-------------|------|
| `(Animal Liberation, 1975)` | 1 | 유지 |
| `(J. Rest)` | 1 | 유지 (제시문 원문에도 있음) |
| `(Jean Piaget)` | 2 | 유지 |
| `(John Stuart Mill)` | 2 | 유지 |
| `(L'Éducation morale, 1902-03)` | 1 | 유지 |
| `(Lawrence Kohlberg)` | 2 | 유지 |
| `(Le Jugement moral chez l'enfant, 1932)` | 1 | 유지 |
| `(On Liberty, 1859)` | 1 | 유지 |
| `(Peter Singer)` | 4 | 유지 |
| `(Summa Theologiae)` | 1 | 유지 |
| `(Summa contra Gentiles)` | 1 | 유지 |
| `(The Philosophy of Moral Development, 1981)` | 1 | 유지 |
| `(Thomas Aquinas)` | 2 | 유지 |
| `(dead dogma)` | 1 | 유지 |
| `(harm principle)` | 2 | 유지 |
| `(living truth)` | 1 | 유지 |
| `(moral character / implementation)` | 1 | 유지 |
| `(moral motivation)` | 1 | 유지 |
| `(other-regarding)` | 1 | 유지 |
| `(self-regarding)` | 1 | 유지 |
| `(speciesism)` | 1 | 유지 |
| `(Regan)` | **0** | **제거·한글 전환** ("동물 권리론(Regan)" → "'동물 권리론'(삶의 주체의 내재적 가치에 근거한 동물 권리 이론)") |

> 메타 레이블 (A)/(B)/(C)/(a)/(b)/(c)/(d)/(A-①)/(A-②)/(B-①)/(B-②) 와 줄번호 (L14-L31 등), 내부 인용 (TASK-183 산출물)/(TASK-184 산출물)/(coverage/2015-B.md L176~L180 근거)/(yihwang) 단독 식별자 등은 자기검증 대상에서 제외 — 원문에 역grep할 성격이 아닌 내부 메타 표기.

**0-hit 토큰 1건**: `(Regan)` — 제거·한글 전환 완료(재grep 결과 `Regan` 0-hit 확인).

### Step 1 확장 — Greek/Cyrillic 알파벳 (신규, TASK-184-FIX 교훈)

```bash
LANG=ko_KR.UTF-8 LC_ALL=ko_KR.UTF-8 grep -oE '\([^)]*[α-ωΑ-Ωа-яА-Я][^)]*\)' study-guide/2015-B.md
```

| 결과 | 개수 | 처리 |
|------|------|------|
| Greek/Cyrillic 문자 포함 괄호 토큰 | **0** | 처리 불요 (권장 0-hit 달성) |

### Step 2 — 괄호 밖 TitleCase 2~6 단어 phrase

```bash
LC_ALL=C.UTF-8 grep -oE '[A-Z][a-z]+(\s+[A-Za-z][a-z]+){1,5}' study-guide/2015-B.md | sort -u
```

| TitleCase phrase | coverage hit (case-sensitive) | 처리 |
|------------------|--------------------------------|------|
| `Animal Liberation` | 1 | 유지 |
| `Jean Piaget` | 2 | 유지 |
| `John Stuart Mill` | 2 | 유지 |
| `Lawrence Kohlberg` | 2 | 유지 |
| `Le Jugement moral chez` | 1 | 유지 |
| `On Liberty` | 1 | 유지 |
| `Peter Singer` | 4 | 유지 |
| `Summa Theologiae` | 1 | 유지 |
| `Summa contra Gentiles` | 1 | 유지 |
| `The Philosophy of Moral Development` | 1 | 유지 |
| `Thomas Aquinas` | 2 | 유지 |

**0-hit 토큰 0건** — 전수 coverage 존재. TitleCase 원문-grep 실증 통과.

### 원본 verbatim byte-level 샘플 검증 (문항별 핵심 문장)

| 문항 | 검증 구절 | study-guide hit | 기대 |
|------|----------|-----------------|------|
| 서술형 1 | "4가지 요소가 '4구성 요소 모델'을 이룹니다" | 1 | ≥1 ✅ |
| 서술형 1 | "학생들의 자아 강도를 높이는 수업" | 1 | ≥1 ✅ |
| 서술형 2 | "의(義)와 도(道)가 배합된 것이다" | 1 | ≥1 ✅ |
| 서술형 2 | "기(氣)는 텅 비어서 무엇이든 받아들이려 기다린다" | 2 | ≥1 ✅ |
| 서술형 3 | "문제는 그들이 고통을 느낄 수 있는가이다" | 3 | ≥1 ✅ |
| 서술형 3 | "자연의 과정에서 인간이 사용하도록 운명으로 결정되었기 때문이다" | 1 | ≥1 ✅ |
| 서술형 4 | `<u>㉠원리</u>` (HTML 보존) | 1 | ≥1 ✅ |
| 서술형 4 | "통설의 의미가 퇴색되어 사람들에게 영향을 미치지 못하게 될 것이기 때문이다" | 1 | ≥1 ✅ |
| 논술형 1 | "비사회적인 존재를 사회적인 존재로 만드는 과정이다" | 1 | ≥1 ✅ |
| 논술형 1 | `<u>내가 보기에 4단계의 관점은 분명한 한계점을 가지고 있다.</u>` (HTML 보존) | 1 | ≥1 ✅ |
| 논술형 2 | `<u>㉠인심(人心)</u>` (HTML 보존) | 1 | ≥1 ✅ |
| 논술형 2 | `<u>㉡도심(道心)</u>` (HTML 보존) | 1 | ≥1 ✅ |
| 논술형 2 | "어찌 이발(理發)과 기발(氣發)의 구분이 있겠는가?" | 1 | ≥1 ✅ |

## ES 전수 재조회 결과 (본 세션, 2026-04-22, curl 실측)

### thinker_id (`ethics-thinkers/_doc/{id}`)

| thinker_id | found | claim 수 |
|------------|-------|---------|
| rest | true | 10 |
| mencius | true | 17 |
| zhuangzi | true | 10 |
| singer | **true** (TASK-DQ-007 override 이후) | 8 |
| aquinas | true | 10 |
| mill_js | true | 17 |
| durkheim | **true** (TASK-DQ-007 override 이후) | 8 |
| piaget | true | 14 |
| kohlberg | true | 20 |
| yihwang | true | 12 |
| yiyulgok | true | 12 |

**⚠️ES 미등록 0건** — 완료 조건 2 (task spec) 달성.

### claim_id 샘플 재조회 (`ethics-claims/_doc/{id}`)

| claim_id | found |
|----------|-------|
| rest-claim-001 | true |
| mencius-claim-001 | true |
| zhuangzi-claim-001 | true |
| singer-claim-001 | true |
| aquinas-claim-001 | true |
| mill-claim-001 (※ mill_js thinker의 claim prefix는 `mill-claim-`으로 실제 네이밍 확인) | true |
| durkheim-claim-001 | true |
| piaget-claim-001 | true |
| kohlberg-claim-001 | true |
| yihwang-claim-001 | true |
| yiyulgok-claim-001 | true |

## NOTE-BLOCKER-1 반영 위치

- `study-guide/2015-B.md` L37 (상단 공지): "논술형 2 갑(퇴계)의 출전 편은 coverage 단계에서 NOTE-BLOCKER-1로 주의 주석이 삽입되었으며, 본 가이드에도 동일 주석을 반영한다(사상가 확정은 유효)."
- `study-guide/2015-B.md` L386 (논술형 2 섹션 상단 경고 블록): "⚠️ **출전 미확정 (판정 가능 범위 — 사상가 확정은 유효)**: coverage/2015-B.md NOTE-BLOCKER-1. …" 전문 경고 인용.
- `study-guide/2015-B.md` L404 (본론 갑 판정 bullet): "(출전 편은 NOTE-BLOCKER-1 대로 미확정이나, 사상가 판정은 유효.)"
- `study-guide/2015-B.md` L470 (풀이 과정 1단계): "정확한 출전 편은 NOTE-BLOCKER-1 대로 미확정. 사상가 판정은 유효."
- `study-guide/2015-B.md` L514 (부록 후속 메모): "기존 NOTE-BLOCKER-1은 '사상가 확정은 유효 + 출전 편만 미확정'의 판정 가능 범위 이슈로, 학생 풀이에는 영향이 없다."

BLK 정식 등록은 하지 않음 — coverage 판정 그대로 유지.

## 이슈/블로커

없음.

- Reviewer Round 2 PASS 사양대로 시행.
- TASK-DQ-007 override에 의한 singer·durkheim ES 등록 상태 반영.
- Step 1 에서 `(Regan)` 0-hit 토큰 1건이 발견되었으나, 태스크 범위 안에서 `'동물 권리론'(삶의 주체의 내재적 가치에 근거한 동물 권리 이론)`으로 제거·한글 전환 후 재검 통과 (narvaez 3-bug 교훈 반영).

## 다음 제안

- Tester 검증 시 집중 포인트: ① 6문항 원문 line metadata 정합성, ② verbatim byte-level 일치 (원본 시험지 L14-L91 대비), ③ HTML `<u>` 태그 4쌍 보존, ④ Step 2 TitleCase phrase 전수 coverage 실재 확증, ⑤ `### 채점 기준` 서브섹션 6건 전수, ⑥ NOTE-BLOCKER-1 반영 위치 5지점 확인.
- singer·durkheim 관련 claim이 ES에 이미 8건씩 등록되어 있으므로, 본 시험 대응 claim 키워드 보강(이익 평등 고려·종차별주의·사회화·도덕성 3요소)은 별도 태스크 검토 여지가 있으나, 본 가이드 자체 품질에는 영향 없음.
- 연도별 study-guide 시리즈 포맷이 이제 2014-A / 2014-B / 2015-A / 2015-B 4회차에 걸쳐 안정화되었다. 후속 회차(예: 2016-A 등)에서 동일 포맷 유지 권장.
