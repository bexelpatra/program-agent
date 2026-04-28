---
task_id: TASK-205
agent: coder
status: DONE
severity: observation
started_at: 2026-04-24
finished_at: 2026-04-24
target_artifact: projects/ethics-study/exam-solutions/study-guide/2025-B.md
target_lines: 732
questions: 11
total_points: 40
fudge_hits: 0
dq021_overrides_applied: 4
blockers_preserved: 2
---

# Coder Report — TASK-205 (2025-B 학생용 풀이 가이드 작성)

## 1. 변경 파일

| 파일 | 상태 | 라인 | 비고 |
|------|------|------|------|
| `projects/ethics-study/exam-solutions/study-guide/2025-B.md` | CREATED | 732 | 11문항 40점 전체 — 기입형 Q1—Q2 (2점×2) + 서술형 Q3—Q11 (4점×9) |

신규 생성 단일 파일. task-board / architecture / blocker-log / coverage / data-quality-log / tests / scripts 모두 불변 — 태스크 규정 준수.

작성 전략: **Split-Write 2 단계** — Phase A (`Write` 신규 생성, 헤더+ES 요약+DQ-021 override+BLOCKER 설명+Q1—Q6, 430L) → Phase B (`Edit` append, Q7—Q11, +302L = 732L 최종) → Phase C (heading normalization + 2건 '수렴' fudge token 제거 edit).

## 2. 자기검증 3단계 프로토콜

### Step 1 — 괄호 안 영어 토큰 unique

```
cd projects/ethics-study/exam-solutions/study-guide
grep -oE '\([A-Za-z][^)]*\)' 2025-B.md | sort -u | wc -l
→ 124
```

서양 개념 영문 병기 (`(enactive mastery experience)` · `(social persuasion)` · `(collective efficacy)` · `(freedom as non-domination)` · `(non-interference)` · `(covenant)` · `(sovereign)` · `(social feelings)` · `(principle of utility)` · `(categorical imperative)` · `(hypothetical imperative)` · `(naturalistic fallacy)` · `(Open-Question Argument)` · `(ethics of care)` · `(Heinz dilemma)` · `(three forms of respect)` · `(respect and responsibility)` 등) 및 서지·고유명 괄호 (`(Jeremy Bentham)` · `(John Stuart Mill)` · `(Immanuel Kant)` · `(Thomas Hobbes)` · `(Philip Pettit)` · `(Isaiah Berlin)` · `(Albert Bandura)` · `(Carol Gilligan)` · `(Lawrence Kohlberg)` · `(Thomas Lickona)` · `(George Edward Moore)` · `(Principia Ethica)` · `(Utilitarianism, 1863)` · `(Grundlegung, 1785)` · `(Leviathan, 1651)` · `(On Liberty, 1859)` · `(Two Concepts of Liberty, 1958)` · `(In a Different Voice, 1982)` 등) 포함.

### Step 1b — 그리스·확장 라틴·키릴·산스크리트·독일어 움라우트 확장 문자 토큰 unique

```
grep -oE '\([ĀāĒēĪīŌōŪūĂăĔĕĬĭŎŏŬŭα-ωΑ-Ωа-яА-Яʼ][^)]*\)' 2025-B.md | sort -u | wc -l
→ 0
```

본 시험은 Q1(지눌·한국) · Q2(무어·영국 분석철학) · Q3(리코나·미국) · Q4(콜버그·길리건·미국) · Q5(반두라·미국) · Q6(왕양명·주희·중국 성리학) · Q7(이이·한국 성리학) · Q8(칸트·독일) · Q9(벤담·밀·영국) · Q10(페팃·벌린·영미) · Q11(홉스·영국) 구성이며, **그리스어·라틴어 매크론·키릴·산스크리트 원전 인용이 출제범위 밖**이므로 Step 1b 토큰이 존재하지 않음이 정상. (2025-A 에서 아리스토텔레스·에피쿠로스·에픽테토스 등 그리스어 원전 인용 3건 있던 것과 대비.) 독일어 `(Pflicht)` · `(Sollen)` · `(der gute Wille)` · `(Grundlegung, 1785)` 4건은 움라우트 미포함이므로 Step 1 에 집계됨.

### Step 2 — 괄호 밖 대문자 2—6 단어 연속구 unique

```
grep -oE '[A-Z][a-z]+(\s+[A-Za-z][a-z]+){1,5}' 2025-B.md | sort -u | wc -l
→ 28
```

주요 토큰: `Albert Bandura` · `Berlin trademark` · `Carol Gilligan` · `Different Voice` · `Educating for Character` · `Essays on Moral Development` · `George Edward Moore` · `Heinz dilemma` · `How Our Schools Can Teach Respect` · `Immanuel Kant` · `Isaiah Berlin` · `Jeremy Bentham` · `John Stuart Mill` · `Lawrence Kohlberg` · `Maurizio Viroli` · `On Liberty` · `Philip Pettit` · `Principia Ethica` · `Principle of Utility` · `Question Argument` · `Social Foundations` · `Social Foundations of Thought and Action` · `The Exercise of Control` · `Theory of Freedom and Government` · `Thomas Hobbes` · `Thomas Lickona` · `Two Concepts of Liberty` · `Who is master` — 서지·고유명·저작 제목.

### Disjoint 교집합 검증

```
grep -oE '\([A-Za-z][^)]*\)' 2025-B.md | sort -u > /tmp/s1.txt
grep -oE '\([ĀāĒēĪīŌōŪūĂăĔĕĬĭŎŏŬŭα-ωΑ-Ωа-яА-Яʼ][^)]*\)' 2025-B.md | sort -u > /tmp/s1b.txt
grep -oE '[A-Z][a-z]+(\s+[A-Za-z][a-z]+){1,5}' 2025-B.md | sort -u > /tmp/s2.txt
comm -12 /tmp/s1.txt /tmp/s1b.txt | wc -l  → 0
comm -12 /tmp/s1.txt /tmp/s2.txt  | wc -l  → 0
comm -12 /tmp/s1b.txt /tmp/s2.txt | wc -l  → 0
```

**3개 집합 완전 disjoint** — Step 1 (124) · Step 1b (0) · Step 2 (28) 중복 카운트 없음. 

### fudge 문구 0건 확증

```
grep -cE '(≈|수렴|중복 보정|대략|얼추|거의)' 2025-B.md
→ 0
```

초판에서 Q6 주희 공부법 서술 2곳에 "거경으로 마음을 **수렴**"(L392, L427) 표현이 발견됨 — 주자학에서 '수렴(收斂)'은 기술적 의미로 "마음을 한 곳에 집중·보존"이라는 본래 뜻을 가지지만, 태스크 금지 토큰 목록의 '수렴'과 형태가 일치하므로 0-hit 원칙을 엄격 적용하여 "한 곳에 집중·보존"으로 교체. 최종 fudge = 0.

### em-dash U+2014 hexdump 표본

```
grep -o '—' 2025-B.md | head -3 | hexdump -C
→ 00000000  e2 80 94 0a e2 80 94 0a  e2 80 94 0a
   0000000c
```

U+2014 (EM DASH) 3-byte UTF-8 sequence `0xE2 0x80 0x94` 직접 확증. 총 147회 사용. 대시 대체(-) 사용 없음. 2025-A (276회) 대비 적은 이유 — 2025-B는 문항이 11개(2025-A 12개)로 1개 적고, 2025-A Q11·Q12(롤스·노직·월저)의 L140 이상 되는 장문 해설이 없음.

## 3. 구조·배점 검증

### 문항 개수

```
grep -c '^## 문항' 2025-B.md → 11
```

원본 `~/잡동사니/임용/md/2025_중등1차_도덕·윤리_전공B.md` (L1—L206) 기준 11문항(Q1—Q11) 일치.

### 배점 검산

```
grep -cE '## 문항 [0-9]+ · 기입형 · 2점' 2025-B.md  → 2
grep -cE '## 문항 [0-9]+ · 서술형 · 4점' 2025-B.md  → 9
2×2 + 4×9 = 4 + 36 = 40점
```

**총 40점** — 원본 표지 "11문항 40점" 일치.

### 한자(漢字) 보존

```
grep -oP '[\x{4e00}-\x{9fff}]+' 2025-B.md | sort -u | wc -l
→ 161 unique CJK tokens
```

주요 원전 핵심어 보존 실측:
- **Q1 (지눌)**: `頓悟漸修` · `定慧雙修` · `隨相定慧` · `自性定慧` · `看話禪` · `節要` · `普照國師` · `眞心` · `空寂靈知` · `寂知`
- **Q6 (왕양명·주희)**: `傳習錄` · `心卽理` · `致良知` · `心外無物` · `良知` · `事上磨鍊` · `知行合一` · `大學章句` · `朱子語類` · `性卽理` · `格物致知` · `卽物窮理` · `居敬窮理` · `本然之性` · `氣質之性` · `存天理去人慾` · `天理` · `人慾`
- **Q7 (이이·갑 미확증)**: `理氣之妙` · `理氣不相離` · `理通氣局` · `氣發理乘一途` · `七包四` · `本然之性` · `氣質之性` · `四德` · `五常` · `陰陽五行` · `四端` · `七情` · `未發` · `中` · `上智` · `下愚`
- **Q8 (칸트)**: `善意志` · `義務` (한글 병기 Pflicht)
- **Q11 (홉스)**: `主權者` · `神` · `社會契約` 등 한글 중심.
- **기타**: `人心` · `道心` · `理氣` · `氣質` · `仁` · `義` · `禮` · `智` · `信` · `性` · `心`

총 **161 unique CJK tokens** — 2025-A (237)보다 적음. 2025-B는 서양 윤리 문항 비중이 높음(Q3 리코나·Q4 콜버그·길리건·Q5 반두라·Q8 칸트·Q9 벤담·밀·Q10 페팃·벌린·Q11 홉스 — 서양 7문 / 한국·동양 4문).

### ㉠㉡㉢㉣㉤㉥ 서클 숫자 보존

```
grep -oE '[㉠㉡㉢㉣㉤㉥]' 2025-B.md | sort | uniq -c
→ ㉠ 105 · ㉡ 110 · ㉢ 97 · ㉣ 63 · ㉤ 8 · ㉥ 10
```

Q1(지눌, ㉠㉡㉢㉣) · Q2(무어, ㉠㉡) · Q3(리코나, ㉠㉡㉢㉣) · Q4(콜버그·길리건, ㉠㉡㉢㉣) · Q5(반두라, ㉠㉡㉢) · Q6(왕양명·주희, ㉠㉡㉢㉣) · Q7(이이+갑 미확증, ㉠㉡) · Q8(칸트, ㉠㉡㉢㉣㉤㉥ — 6개 최다) · Q9(벤담·밀, ㉠㉡㉢㉣) · Q10(페팃·벌린, ㉠㉡㉢㉣) · Q11(홉스, ㉠㉡㉢) 발문·정답·채점기준·풀이 과정 일관 사용. 원본 서클-한자 표기 완전 보존.

## 4. DQ-021 override 4명 처리 내역

| Thinker | 문항 | 역할 | coverage 원 BLOCKER | study-guide 처리 | 재측정 결과 |
|---------|------|------|---------------------|-------------------|-------------|
| `jinul` | Q1 | 기입형 사상가 | BLK-175E-2025B-001 (2026-04-21) | **HIT(9)** — `jinul-claim-001`—`005` 정상 인용 · "DQ-021 override" 주석 | 2026-04-24 `curl` ES 200 · 9 claims `found=true` |
| `moore` | Q2 | 기입형 사상가 | BLK-175E-2025B-002 (2026-04-21) | **HIT(7)** — `moore-claim-001`—`005` 정상 인용 · "DQ-021 override" 주석 | 2026-04-24 `curl` ES 200 · 7 claims `found=true` |
| `bandura` | Q5 | 서술형 사상가 | BLK-175E-2025B-003 (2026-04-21) | **HIT(8)** — `bandura-claim-001`—`007` 정상 인용 · "DQ-021 override" 주석 | 2026-04-24 `curl` ES 200 · 8 claims `found=true` |
| `pettit` | Q10 갑 | 서술형 사상가 (viroli 후보 폐기 · 페팃 단일 확정) | BLK-175E-2025B-004 (2026-04-21) | **HIT(8)** — `pettit-claim-001`—`005` 정상 인용 · "DQ-021 override" 주석 | 2026-04-24 `curl` ES 200 · 8 claims `found=true` |

본문 Q1 · Q2 · Q5 · Q10 의 4개 사상가 섹션에 "⚠️ES 미등록" / "BLOCKER 유지" 표기 없음 (DQ-021 지시 준수). ES 근거 섹션에 **DQ-021 override** 명시, 요약 헤더 섹션에서 **이력(2026-04-21 BLOCKER 기록)** 과 **본 세션 재측정 결과(HIT)** 병기.

```
grep -c 'DQ-021' 2025-B.md → 15
```

헤더 요약(5회) + Q1 jinul override(2회) + Q2 moore override(2회) + Q5 bandura override(2회) + Q10 pettit override(4회) = 15회.

## 5. BLOCKER 2건 유지

### 5.1 berlin (Q10 을) — BLK-175E-2025B-005

- Q10 을 섹션에 `berlin-claim-*` 인용 **0건** (ES 404 유지 — DQ-021 미적용, BLOCKER 유지).
- 대신 교과서 표준 서술 — "이사야 벌린 · 『자유의 두 개념』(1958) · 소극적 자유 · 간섭의 부재 · 통제의 범위 vs 근원" — 일반 개념 수준 전개.
- 섹션 제목 상단에 `⚠️ BLOCKER BLK-175E-2025B-005 (을 벌린 ES MISS)` 경고 박스 · 교과서 해설 대체 사유 명기.
- 요약 헤더 L50—L55 에 상세 BLOCKER 유지 근거 + 등록 필요 claim 후보(TASK-176 후속 대상) 명기.

### 5.2 Q7 갑 사상가 확증 보류 — BLK-175E-2025B-006

- Q7 갑 제시문은 조선 성리학 **사칠이원론 표준 문형**을 띠나, 원 제시문을 trademark로 귀속할 **단일 조선 성리학자**(이언적·이황·기대승·이이·권근 후보 등) 확정에 실패 — coverage 단계에서 확증 보류.
- 해설 전략: **갑의 사상가 단정 대신 교과서 표준 성리학 해설**(이기론·사단칠정·본연지성/기질지성 구분)로 대체. 채점은 이기 관계·사단칠정 대응 내용 일치 여부로 평가한다는 방침 명기.
- 섹션 제목 상단에 `⚠️ BLOCKER BLK-175E-2025B-006 (갑 사상가 확증 보류)` 경고 박스.
- 을(이이) HIT 해설은 정상 제공 — yiyulgok claims 7개 인용.

```
grep -cE 'BLOCKER|BLK-175E' 2025-B.md → 18
```

헤더 요약(4회) + Q1—Q5·Q10 DQ-021 override 이력 기술(8회, 각 사상가별 '원 BLOCKER → 재측정 HIT' 문맥) + Q10 berlin BLOCKER 유지(3회) + Q7 갑 BLOCKER 유지(3회) = 18회.

## 6. ES 근거 요약 (14 HIT + 1 MISS)

본 세션 ES 실측(2026-04-24 curl localhost:9200):

| Thinker | found | claims | 역할 |
|---------|-------|--------|------|
| jinul | true | 9 | Q1 (DQ-021 override) |
| moore | true | 7 | Q2 (DQ-021 override) |
| lickona | true | 10 | Q3 |
| kohlberg | true | 20 | Q4 |
| gilligan | true | 12 | Q4 |
| bandura | true | 8 | Q5 (DQ-021 override) |
| wangyangming | true | 10 | Q6 갑 |
| zhuxi | true | 16 | Q6 을 |
| yiyulgok | true | 12 | Q7 을 |
| kant | true | 18 | Q8 |
| bentham | true | 12 | Q9 갑 |
| mill_js | true | 17 | Q9 을 |
| pettit | true | 8 | Q10 갑 (DQ-021 override) |
| hobbes | true | 14 | Q11 |
| **berlin** | **false** | **0** | **Q10 을 (BLOCKER BLK-175E-2025B-005)** |

총 14명 HIT + 1명 MISS (berlin). Q7 갑은 사상가 미확증(BLK-175E-2025B-006)이므로 ES 조회 대상 자체 부재.

## 7. 타깃 대비 실측 — 라인 수 (observation)

- **타깃**: 약 700 라인 (manager 지시)
- **실측**: 732 라인
- **오차**: +32L (+4.6%)
- **판정**: 타깃 허용 범위 — 2025-A (705L · 12문항) 대비 문항 -1이지만 Q7 BLOCKER 설명·Q10 DQ-021+BLOCKER 이중 처리로 라인 증가.

## 8. 이슈/블로커

- 없음 (severity: observation).
- BLOCKER 2건(berlin · Q7 갑)은 coverage 시점 확정 상태 그대로 본 study-guide 에도 유지 — 신규 BLOCKER 발생 없음.
- DQ-021 override 4건(jinul · moore · bandura · pettit)은 본 세션 ES 재측정으로 정상 HIT 확증.

## 9. 선행 태스크/참고

- **TASK-200** (coverage 2025-B.md · 550L) — 사상가 식별·BLOCKER 등록
- **TASK-202** (study-guide 2024-B.md · 728L · 12문항)
- **TASK-203** (study-guide 2024-A.md · 757L · 11문항)
- **TASK-204** (study-guide 2025-A.md · 705L · 12문항)
- **architecture.md Phase 6** (L578 ff) — 기출 해설 작업 규칙 (verbatim · grep 0건 · 창작 금지 · fudge 금지)
- **data-quality-log.md L257—L285** — DQ-021 override 선언

## 10. 완료 조건 대조

| 조건 | 결과 |
|------|------|
| 11문항 전체 커버 (Q1—Q11) | ✅ 11개 `## 문항` 헤더 |
| 총 40점 배점 (2점×2 + 4점×9) | ✅ 산술 검산 40 |
| verbatim 발문·제시문 보존 | ✅ 원본 L16—L202 blockquote 인용 |
| em-dash U+2014 사용 | ✅ 147회 · 0xE2 0x80 0x94 확증 |
| 한자 보존 | ✅ 161 unique CJK |
| ㉠㉡㉢㉣㉤㉥ 보존 | ✅ 393회 총합 |
| ES claim_id 인용 (HIT 사상가) | ✅ 14명 전원 |
| DQ-021 override 4명 처리 | ✅ jinul · moore · bandura · pettit 해설 본문 정상 HIT 서술 |
| BLOCKER 2건 유지 | ✅ berlin (BLK-175E-2025B-005) · Q7 갑 (BLK-175E-2025B-006) |
| 자기검증 3단계 disjoint | ✅ S1 ∩ S1b = 0 · S1 ∩ S2 = 0 · S1b ∩ S2 = 0 |
| fudge 토큰 0 | ✅ 초판 2건 → 교체 후 0 |
| 타깃 ~700L | ✅ 732L (+4.6% 허용 범위) |

**DONE** — 사용자 검토 대기.
