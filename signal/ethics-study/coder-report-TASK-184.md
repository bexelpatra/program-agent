---
agent: coder(opus)
task_id: TASK-184
status: DONE
severity: none
timestamp: 2026-04-22
---

## 결과 요약

2015학년도 중등임용 도덕·윤리 전공 A (14문항 40점 — 기입형 10 + 서술형 4) 연도별 학생용 풀이 가이드 `/home/jai/program-agent/projects/ethics-study/exam-solutions/study-guide/2015-A.md` 를 신규 작성했다. 선례 `2014-A.md`·`2014-B.md` 포맷을 100% 답습(6개 서브섹션: 발문/제시문 verbatim/정답·핵심 개념/관련 ES 근거/채점 기준(서술형만)/풀이 과정)하고, Reviewer 권고사항대로 BLOCKER-1(기입형 4 (나) 빈칸 정답: 예(禮)·화성기위 양 후보)과 BLOCKER-2(기입형 8 세로 낱말 A: 자연상태 유력 + 사회계약·자연권리 보조)를 섹션 생성 + ⚠️BLOCKER 표기 + 후보군 + 권장 답안 요령으로 커버했다.

## 변경된 파일

- `projects/ethics-study/exam-solutions/study-guide/2015-A.md` (신규, 674 lines)

## 완료 조건 검증

| # | 조건 | 결과 |
|---|------|------|
| 1 | 파일 생성 `study-guide/2015-A.md` | ✅ 신규 생성 (674 lines) |
| 2 | 14문항 전수 커버 (`grep -c '^## 문항' == 14`) | ✅ **14** (기입형 10 + 서술형 4) |
| 3 | 각 문항 섹션 헤더에 `원문 line L{m}-L{n}` metadata (`grep -c '원문 line L' == 14`) | ✅ **14** |
| 4 | 각 문항 제시문 verbatim byte-level 일치 | ✅ 핵심 인용 구절 15개 전수 원본 hit=1 이상 확증 (아래 표) · HTML `<u>` 4개 원본과 일치 |
| 5 | 사상가형 문항의 thinker_id 각 ≥1 + 본 세션 curl 로 ES found=true 재조회 | ✅ macintyre·xunzi·zhuxi·wangyangming·buddha·habermas·hobbes·plato·aristotle·kant·rawls 11명 found=true 전수 확증 (2026-04-22 세션) |
| 6 | 교과교육학·경계영역·ES 미등록 분류 사유 명시 | ✅ 기입형 2(교과교육학 — Newmann ES 미등록) / 기입형 3(교과교육학 — 교육과정 가치·덕목) / 기입형 6(Nāgārjuna ES 미등록) / 기입형 10(경계영역 — 국제 인권 규범) / 서술형 4(교과교육학 — 통일·평화) 전수 명시 |
| 7 | 서술형 4문항 전원 `### 채점 기준` 서브섹션 실재 (`grep -c '^### 채점 기준' == 4`) | ✅ **4** |
| 8 | 자기검증 2단계 결과 표 coder-report 포함 | ✅ 아래 "자기검증 2단계 루프 결과" 섹션 |

## 자기검증 2단계 루프 결과 (agents/coder.md L89-L115)

### Step 1 — 괄호 안 영어 토큰 (grep -oE '\\([A-Za-z][^)]*\\)' sort -u 후 coverage 역grep)

**1차 검증 결과**: 전체 추출 토큰 중 **9건 0-hit 발견**. 아래 9건을 한글 단독 전환·제거·대체:

| 0-hit 토큰 | 조치 | 변경 후 |
|-----------|------|---------|
| `Grundlegung zur Metaphysik der Sitten` | 괄호 포함 영문 원서명 제거 | 한글 "『도덕형이상학 정초』" 단독 |
| `Neigung` | 괄호 영문 제거 | "경향성" (한글 단독) |
| `demokratia` | 괄호 영문 제거 | "민주정" (한글 단독) |
| `mesotes` | 괄호 영문 제거 | "메소테스" (coverage hit=1 한글) |
| `symmetry` | 괄호 영문 제거 | "대칭성" (한글 단독) |
| `theoretical wisdom` | 괄호 영문 제거 | "철학적 지혜" (한글 단독) |
| `practice` | 괄호 영문 제거 | "실천" (한글 단독) |
| `tradition` | 괄호 영문 제거 | "전통" (한글 단독) |
| `virtue` | 괄호 영문 제거 | "덕" (한글 단독) |
| `The first and fundamental law of nature` | 괄호 영문 제거 | 삭제, "자연법 제1조항" (한글 단독) |

**2차 재검증 결과 (Step 1 유지된 괄호 안 영어 토큰 최종 전수, coverage+원본 case-sensitive `grep -F` hit)**:

| 토큰 | coverage hit | 원본 hit | 조치 |
|------|-------------|---------|------|
| `A. MacIntyre` | 2 | 1 | ✅ 유지 (원본 L22 직접 표기) |
| `A. Schopenhauer` | 1 | 1 | ✅ 유지 (원본 L111) |
| `After Virtue` | 1 | 0 | ✅ 유지 (coverage L15 trademark 서지) |
| `Aristotle` | 2 | 0 | ✅ 유지 (coverage L25) |
| `Autonomie` | 1 | 0 | ✅ 유지 (coverage L26) |
| `Enlightenment Project` | 1 | 1 | ✅ 유지 (원본 L22 직접 표기) |
| `F. Newmann` | 3 | 0 | ✅ 유지 (coverage L16) |
| `Glückseligkeit` | 1 | 0 | ✅ 유지 (coverage L26) |
| `Heteronomie` | 1 | 0 | ✅ 유지 (coverage L26) |
| `Immanuel Kant` | 1 | 0 | ✅ 유지 (coverage L26) |
| `Jürgen Habermas` | 1 | 0 | ✅ 유지 (coverage L21) |
| `John Rawls` | 1 | 0 | ✅ 유지 (coverage L27) |
| `Justice as Fairness: A Restatement` | 1 | 0 | ✅ 유지 (coverage L27) |
| `K. Marx` | 1 | 1 | ✅ 유지 (원본 L110) |
| `Kritik der praktischen Vernunft` | 1 | 0 | ✅ 유지 (coverage L26) |
| `Newmann` | 4 | 0 | ✅ 유지 (coverage L16 외) |
| `Nicomachean Ethics` | 1 | 0 | ✅ 유지 (coverage L25) |
| `Pflicht` | 1 | 0 | ✅ 유지 (coverage L26) |
| `Plato` | 2 | 0 | ✅ 유지 (coverage L23) |
| `Politeia` | 1 | 0 | ✅ 유지 (coverage L23) |
| `Political Liberalism` | 1 | 0 | ✅ 유지 (coverage L27) |
| `T. Hobbes` | 3 | 1 | ✅ 유지 (원본 L108 직접 표기) |
| `Wille zum Leben` | 1 | 0 | ✅ 유지 (coverage L22) |
| `capacity for a conception of the good` | 1 | 0 | ✅ 유지 (coverage L27) |
| `civic action` | 1 | 0 | ✅ 유지 (coverage L16) |
| `counterfactual presupposition` | 1 | 0 | ✅ 유지 (coverage L21) |
| `deinotés — cleverness` | 부분 hit (deinotés=2, cleverness=1) | deinotés=1, cleverness=0 | ✅ 유지 (원본 deinotés L166 + coverage cleverness) |
| `deinotés` | 2 | 1 | ✅ 유지 (원본 L166 직접 표기) |
| `environmental competence` | 1 | 0 | ✅ 유지 (coverage L16) |
| `episteme — 앎` | episteme=1 | episteme=0 | ✅ 유지 (coverage L25 — "앎" 병기) |
| `false consciousness` | 1 | 0 | ✅ 유지 (coverage L22) |
| `fundamental freedoms` | 1 | 0 | ✅ 유지 (coverage L24) |
| `human rights` | 1 | 0 | ✅ 유지 (coverage L24) |
| `hypothetischer Imperativ` | 1 | 0 | ✅ 유지 (coverage L26) |
| `idea` | 1 | 0 | ✅ 유지 (coverage) |
| `ideale Sprechsituation` | 1 | 0 | ✅ 유지 (coverage L21) |
| `kategorischer Imperativ` | 1 | 0 | ✅ 유지 (coverage L26) |
| `logos` | 1 | 0 | ✅ 유지 (coverage L25) |
| `noble lie, γενναῖον ψεῦδος` | "noble lie"=1 | 0 | ✅ 유지 (coverage L23) |
| `phronēsis` | 1 | 0 | ✅ 유지 (coverage L25) |
| `rational` | 1 | 1 | ✅ 유지 (원본 L186 직접 표기) |
| `reasonable` | 1 | 1 | ✅ 유지 (원본 L186 직접 표기) |
| `sense of justice` | 1 | 0 | ✅ 유지 (coverage L27) |
| `story-telling animal` | 2 | 0 | ✅ 유지 (coverage L15) |
| `the rational` | 1 | 1 | ✅ 유지 (원본 L186) |
| `the reasonable` | 1 | 1 | ✅ 유지 (원본 L186) |
| `trust` | 1 | 0 | ✅ 유지 (coverage L17) |
| `validity claims` | 1 | 0 | ✅ 유지 (coverage L21) |

**최종 Step 1 검증 결과**: 유지된 모든 영어 괄호 토큰의 coverage hit ≥ 1 달성 (단일 영어 단어 + 괄호 안 2~6 단어 phrase 모두 포함). 0-hit 토큰 완전 제거.

### Step 2 — 괄호 밖 TitleCase 영어 phrase (grep -oE '[A-Z][a-z]+(\\s+[A-Za-z][a-z]+){1,5}' sort -u 후 coverage 역grep)

| 토큰 | coverage hit | 원본 hit | 조치 |
|------|-------------|---------|------|
| `After Virtue` | 1 | 0 | ✅ 유지 (coverage L15) |
| `Alasdair Mac` | 1 | 0 | ✅ 유지 — "Alasdair MacIntyre" 의 정규식 부분 매치; coverage L15 "Alasdair MacIntyre" 실재 |
| `Enlightenment Project` | 1 | 1 | ✅ 유지 (원본 L22) |
| `Immanuel Kant` | 1 | 0 | ✅ 유지 (coverage L26) |
| `John Rawls` | 1 | 0 | ✅ 유지 (coverage L27) |
| `Justice as Fairness` | 1 | 0 | ✅ 유지 (coverage L27) |
| `Kritik der praktischen Vernunft` | 1 | 0 | ✅ 유지 (coverage L26) |
| `Nicomachean Ethics` | 1 | 0 | ✅ 유지 (coverage L25) |
| `Political Liberalism` | 1 | 0 | ✅ 유지 (coverage L27) |
| `Respect for human rights and fundamental` | 1 | 0 | ✅ 유지 — Respect ~ fundamental freedoms 일부, coverage L24 "Respect for human rights and fundamental freedoms" 실재 |
| `Wille zum Leben` | 1 | 0 | ✅ 유지 (coverage L22) |

**Step 2 최종 결과**: 괄호 밖 TitleCase phrase 전수 coverage hit ≥ 1 달성. 0-hit 없음.

### 면제 조건

해당 없음. 본 태스크는 "원문 인용 태스크"에 해당하여 agents/coder.md L89-L115 자기검증 2단계 프로토콜 전면 적용.

## 제시문 verbatim 교차 검증 (원본 대비 spot-check)

원본 파일 `~/잡동사니/임용/md/2015중등1차-도덕윤리_전공A.md`(213 lines)에 대한 핵심 인용 구절 `grep -Fc` hit:

| 핵심 구절 | 원본 hit |
|-----------|---------|
| `계몽주의 기획(Enlightenment Project)` | 1 |
| `환경적 능력` | 3 |
| `상호 의존에 근거한 심리적 안정감` | 1 |
| `하늘의 운행에는 일정함이 있으니` | 1 |
| `선(善)한 것을 분별하는 법도` | 1 |
| `전 씨는 종일토록 대나무를 궁구` | 1 |
| `불멸(不滅), 불생(不生)` | 1 |
| `타당성 요구` | 1 |
| `홉스(T. Hobbes)의 □□□ 1조항` | 1 |
| `항해사의 비유` | 1 |
| `기본적 자유` | 4 |
| `영리함(deinotés)` | 1 |
| `정언 명령` | 1 |
| `2가지 도덕적 능력` | 2 |
| `자주, 평화, 민주` | 1 |

HTML `<u>` 태그: 원본 4개 · 가이드 4개 일치. 괄호 안 영문·한자(漢字 — 禮·化性·緣起·聖人·太極 등)·특수 기호(□·㉠·㉡) byte-level 보존. TASK-178-FIX verbatim 규정 준수.

## ES canonical thinker_id 재조회 결과 (본 세션 2026-04-22 curl 실측)

| thinker_id | found | 관련 문항 |
|-----------|-------|-----------|
| `macintyre` | True | 기입형 1 |
| `xunzi` | True | 기입형 4 |
| `zhuxi` | True | 기입형 5 갑 |
| `wangyangming` | True | 기입형 5 을 |
| `buddha` | True | 기입형 6 (참고) |
| `habermas` | True | 기입형 7 |
| `hobbes` | True | 기입형 8 |
| `plato` | True | 기입형 9 |
| `aristotle` | True | 서술형 1 |
| `kant` | True | 서술형 2 |
| `rawls` | True | 서술형 3 |
| `nagarjuna` | **False** | 기입형 6 — coverage와 일치(ES 미등록 표기) |

본 시험에 직접 등장한 사상가형 문항 10건의 thinker_id·claim_id 각 ≥ 1 할당 완료. Nāgārjuna는 ES 미등록 상태로 ⚠️ 표기 + buddha 참조 처리.

## BLOCKER 처리 (Reviewer 권고사항 반영)

| BLOCKER ID | 문항 | 원인 | 후보군 | 가이드 처리 |
|------------|------|------|--------|-------------|
| BLOCKER-1 | 기입형 4 (나) 빈칸 | 원문에 "예(禮)·예의·化性·화성기위" 한자·한글 어느 형태도 hit=0 | ① 예(禮) 유력 (순자 『수신편』·『권학편』 trademark 대응) / ② 화성기위(化性起僞) 보조 (성악편 trademark) | ⚠️BLOCKER 표기 + 후보군 + "권장 답안 작성 요령" 3 문단으로 커버 |
| BLOCKER-2 | 기입형 8 세로 낱말 (A) 4글자 | 십자말풀이 격자 정보가 그림 형태로만 제공, 텍스트로 미복원 | ① 자연상태(自然狀態) 유력 / ② 사회계약(社會契約) / ③ 자연권리(自然權利) | ⚠️BLOCKER 표기 + 후보군 + "실제 시험장 시 퍼즐 격자 직접 확인" 권장 |

두 BLOCKER 모두 Manager 지시대로 섹션 생성 + BLOCKER 표기 방식으로 14문항 전수 커버 조건을 충족했다.

## 분류 카운트 (coverage/2015-A.md L142~L148 근거)

- 사상가형: 기입형 1·4·5·6·7·8·9 + 서술형 1·2·3 = **10문항**
- 교과교육학: 기입형 2·3 + 서술형 4 = **3문항**
- 경계영역: 기입형 10 = **1문항**
- 합계: **14** ✓

## ES 커버리지 요약

- 있음(직접 claim 실재): 7문항 (macintyre · zhuxi+wangyangming · habermas · plato · aristotle · kant · rawls)
- 부족(claim 보강 권장): 3문항 (xunzi 禮(예)·化性 / buddha·Nāgārjuna / hobbes 자연상태)
- 없음(ES 미등록 or 매핑 대상 아님): 4문항 (Newmann / 교육과정 가치·덕목 / 국제 인권 / 남북 통일방안)
- 합계: **14** ✓

## 이슈/블로커

- **BLOCKER-1**(기입형 4 (나)) · **BLOCKER-2**(기입형 8 세로 A): Reviewer 권고사항대로 가이드 본문 섹션 내에 표기 + 후보군 제시 방식으로 처리 완료. 코드 결함이 아닌 **원문 데이터 품질 이슈**(퍼즐 격자 정보 미복원·빈칸 정답 미인쇄)로, 원본 수정 금지 규정하에서는 BLOCKER 상태를 유지하는 것이 규약.
- 기타 코드 결함 없음.

## 다음 제안

1. ES 보강 대상 2건: `F. Newmann` (시민 행동 수업 모형) · `Nāgārjuna` (중관·팔불중도). 별도 태스크로 ES 등록 고려.
2. claim 직접 보강 권장 4건: xunzi "예(禮)·禮義·화성기위" / buddha "연기·팔불중도(Nāgārjuna 교차)" / hobbes "자연법 제1조항(평화 추구)·자연상태" / rawls "2가지 도덕적 능력(선 관념·정의감)".
3. 2015-B·2016-A 등 후속 연도 study-guide 작성 시 본 파일(2015-A.md)을 2014-A·B와 동등한 3번째 포맷 선례로 참조 가능. 특히 BLOCKER 처리 포맷(섹션 생성 + 후보군 + 권장 답안 요령 3단 구성)이 신규 기준으로 정착될 수 있다.
4. 동명이인 suffix 규약(architecture.md L539-L541) 해당 사례 없음 — 2015-A 사상가 11명 중 동명 충돌 없음 확인.
