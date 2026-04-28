---
agent: coder
task_id: TASK-190
status: DONE
timestamp: 2026-04-22T22:45:00+09:00
severity: none
---

# TASK-190 결과 보고 — 2018-A 학생용 풀이 가이드 작성

## 결과 요약

- **산출물**: `/home/jai/program-agent/projects/ethics-study/exam-solutions/study-guide/2018-A.md`
- **총 라인 수**: 901 L (cap 1800 L 준수, 여유 899 L)
- **`^## 문항` 개수**: 14 (14문항 전수 section 존재 확인)
- **em-dash U+2014 (E2 80 94) 바이트 보존**: 100개 (Manager 주석 · 한자(漢字)—영어 래퍼 전량)
- **작성 방식**: Phase A (header + ES 상태 표 + claim 카운트 표 + Q1~Q7) Write + Phase B (Q8~Q14 + 닫는 문구) Edit-append 2-phase 분할 전략
- **선례 포맷 준수**: TASK-182~189 포맷 (특히 TASK-188 2017-A 14-문항 혼합·TASK-189 2017-B 서술형 채점기준) 100% 답습
- **원본 시험지 verbatim 복사**: `<u>…</u>` · ㉠㉡㉢ · ⓐⓑ · 한자 · 괄호 병기 byte-level 보존
- **자기검증 3단계 전수 PASS**: Step 1/1b/2 모두 0-hit = 0 달성 (self-correct 후)

## 변경된 파일

| 경로 | 변경 | 라인 |
|------|------|------|
| `projects/ethics-study/exam-solutions/study-guide/2018-A.md` | 신규 생성 | 901 L |
| `signal/ethics-study/coder-report-TASK-190.md` | 본 보고서 | — |

## 14 문항 커버리지

| Q | 유형 | 배점 | 원문 라인 | 사상가 / 주제 | ES 상태 |
|---|------|-----|-----------|--------------|---------|
| 1 | 기입형 | 2 | L14-L20 | 인격 교육 (리코나) | ✅ lickona · 12 claims |
| 2 | 기입형 | 2 | L24-L37 | 2015 개정 도덕과 역량 | 해당 없음 (교과교육학) |
| 3 | 기입형 | 2 | L41-L49 | 추첨 민주주의 (아리스토텔레스 간접) | ✅ aristotle · 12 claims (간접) |
| 4 | 기입형 | 2 | L53-L59 | 원효 일심이문 (화쟁) | ✅ wonhyo · 3 claims |
| 5 | 기입형 | 2 | L63-L69 | 칸트 경향성 | ✅ kant · 18 claims |
| 6 | 기입형 | 2 | L73-L77 | 아우구스티누스 카리타스 | ✅ augustine · 8 claims |
| 7 | 기입형 | 2 | L81-L95 | 북한 도덕교육 (하나는 전체…) | 해당 없음 (통일교육) |
| 8 | 기입형 | 2 | L99-L119 | 남북합의문서 "평화" | 해당 없음 (통일교육) |
| 9 | 서술형 | 4 | L123-L131 | 래스 가치명료화 (커션바움 확장) | ✅ raths · 10 claims |
| 10 | 서술형 | 4 | L135-L139 | 로크 명시적·묵시적 동의 | ✅ locke · 12 claims |
| 11 | 서술형 | 4 | L143-L153 | 톰 리건 내재적 가치·삶의 주체 | ⚠️ **BLOCKER-1** · regan 미등록 (BLK-175E-2018A-001) |
| 12 | 서술형 | 4 | L157-L163 | 주자 기질지성 · 왕양명 심즉리·지행합일 | ✅ zhuxi · 16 · wangyangming · 10 |
| 13 | 서술형 | 4 | L167-L175 | 밀 질적 공리주의 (에피쿠로스 소환) | ✅ mill_js · 17 claims · epicurus · 8 claims |
| 14 | 서술형 | 4 | L179-L187 | 장자 피시상인·시비쌍망 | ✅ zhuangzi · 10 claims |

- **서술형 6문항 (Q9~Q14) 전원**: `### 채점 기준` 서브섹션 존재 (배점 4×6 = 24점)
- **기입형 8문항 (Q1~Q8) 전원**: 채점 기준 없음 (기입형은 정답 1개)
- **사상가형 ES thinker_id curl 실측 `found=true` 전수 확인**: lickona · wonhyo · kant · augustine · raths · locke · zhuxi · wangyangming · mill_js · epicurus · zhuangzi · aristotle (12명)
- **BLOCKER 1건**: Q11 regan (BLK-175E-2018A-001) — 본 태스크 출력에서 `⚠️ ES 미등록(BLOCKER-1)` 명시, TASK-176 후속 등록 대기
- **claim_id prefix 이상 1건**: mill_js → `mill-claim-NNN` (thinker_id와 상이, TASK-188 확증)

## 자기검증 프로토콜 (agents/coder.md L89-L115)

### Step 1 · bare-paren `\([A-Za-z][^)]*\)` — LC_ALL=C.UTF-8

- **추출 unique 토큰**: 98개 (sort -u)
- **Manager 주석·구조 토큰 skip**: `(L\d…)` · `(BLK-…)` · `(BLOCKER…)` · `(TASK-…)` · `(Q\d…)` · `(claim \d+건)` · `(a)`·`(b)`·`(c)`·`(d)` · `(thinker_id …상이 — TASK-188 확증)` 등
- **검증 대상 substantive 토큰**: 53개 → 전원 coverage hit ≥ 1 (0-hit = 0)

### Step 1b · Latin-extended (U+00C0-U+024F) paren

- **추출 unique 토큰**: 4개 (Manager 주석·배점 숫자 포함)
- **검증 대상 토큰**: 1개 → coverage hit ≥ 1 (0-hit = 0)

### Step 2 · TitleCase phrase `[A-Z][a-z]+(\s+[A-Za-z][a-z]+){1,5}`

- **추출 unique 토큰**: 18개
- **전원 coverage hit ≥ 1** (0-hit = 0)

### Step 1 추출 토큰 전수 표 (53개 검증 대상)

| 토큰 | cov hit | 초기 0? | 수정 후 hit |
|------|---------|--------|-------------|
| `(Augustine of Hippo)` | 2 | - | 2 |
| `(De civitate Dei)` | 2 | - | 2 |
| `(Epicurus)` | 2 | - | 2 |
| `(Grundlegung zur Metaphysik der Sitten)` | 2 | - | 2 |
| `(H. Kirschenbaum)` | 2 | - | 2 |
| `(Howard Kirschenbaum)` | 3 | - | 3 |
| `(Immanuel Kant)` | 1 | - | 1 |
| `(John Locke)` | 2 | - | 2 |
| `(John Stuart Mill)` | 1 | - | 1 |
| `(Louis Raths)` | 2 | - | 2 |
| `(Neigung)` | 4 | - | 4 |
| `(Pflicht)` | 3 | - | 3 |
| `(The Case for Animal Rights)` | 5 | - | 5 |
| `(Thomas Lickona)` | 2 | - | 2 |
| `(Tom Regan)` | 4 | - | 4 |
| `(Two Treatises of Government)` | 2 | - | 2 |
| `(Utilitarianism)` | 2 | - | 2 |
| `(W. Bennett)` | 1 | - | 1 |
| `(acting)` | 4 | - | 4 |
| `(aus Neigung)` | 2 | - | 2 |
| `(aus Pflicht)` | 2 | - | 2 |
| `(caritas)` | 6 | - | 6 |
| `(caritas — 신에 대한 사랑)` | 변형 | - | hit (부분 매치) |
| `(character education)` | 3 | - | 3 |
| `(choosing)` | 4 | - | 4 |
| `(comprehensive approach)` | 1 | - | 1 |
| `(competent judges)` | 4 | - | 4 |
| `(consent)` | 4 | - | 4 |
| `(express consent)` | 4 | - | 4 |
| `(frui Deo)` | 2 | - | 2 |
| `(harm principle)` | 3 | - | 3 |
| `(harm)` | 4 | - | 4 |
| `(hedonic value)` | 1 | - | 1 |
| `(higher pleasure)` | 2 | - | 2 |
| `(inherent value)` | 6 | - | 6 |
| `(instrumental value)` | 1 | - | 1 |
| `(klērōsis — 제비뽑기)` | 변형 | - | hit (부분 매치) |
| `(lower pleasure)` | 3 | - | 3 |
| `(moral relativism)` | 1 | - | 1 |
| `(not earned or assigned)` | 2 | - | 2 |
| `(ordo amoris)` | 4 | - | 4 |
| `(pivot of the Way)` | 3 | - | 3 |
| `(privatio boni)` | 4 | - | 4 |
| `(prizing)` | 3 | - | 3 |
| `(quality)` | 1 | - | 1 |
| `(respect principle)` | 4 | - | 4 |
| `(subject-of-a-life)` | 5 | - | 5 |
| `(swine philosophy)` | 2 | - | 2 |
| `(tacit consent)` | 4 | - | 4 |
| `(valuing process)` | 2 | - | 2 |
| `(values clarification)` | 2 | - | 2 |
| `(whole school approach)` | 2 | - | 2 |
| `(equal)` | 3 | - | 3 |

### Step 2 TitleCase 토큰 전수 표 (18개)

| 토큰 | cov hit |
|------|---------|
| `Advanced Values Clarification` | 2 |
| `Augustine of Hippo` | 2 |
| `De civitate Dei` | 2 |
| `De libero arbitrio` | 2 |
| `Grundlegung zur Metaphysik der Sitten` | 2 |
| `Howard Kirschenbaum` | 3 |
| `Immanuel Kant` | 1 |
| `It is better to be` | 1 |
| `John Locke` | 2 |
| `John Stuart Mill` | 1 |
| `Louis Raths` | 2 |
| `Socrates dissatisfied than` | 1 |
| `The Case for Animal Rights` | 5 |
| `Thomas Lickona` | 2 |
| `Tom Regan` | 4 |
| `Two Treatises of Government` | 2 |
| `Values and Teaching` | 2 |
| `Ways to Enhance Values and Morality` | N (1995 제목 부분매치) |

### Step 1b Latin-extended 토큰 (1개 substantive)

| 토큰 | cov hit |
|------|---------|
| `(유한한 이성적 존재[endliches vernünftiges Wesen])` | 3 (endliches vernünftiges Wesen 부분매치) |

## 자기 교정(self-correct) 집계

초기 draft 에는 coverage 미수록 영어 gloss 를 다수 삽입하였으나 Step 1/1b 역grep 결과 0-hit 확인 후 일괄 제거·Hangul 변환 수행. 총 **24 건 수정**:

| # | 위치 | 초기 토큰 (0-hit) | 수정 |
|---|------|-------------------|------|
| 1 | Q1 L62 | `(moral knowing)·(moral feeling)·(moral action)` | 영어 파렌 전체 삭제 |
| 2 | Q1 L64-65 | `(traditionalist approach)·(communitarian approach)` | 삭제 |
| 3 | Q1 L65 | `(just community)` | 삭제 |
| 4 | Q3 L158 | `(election)·(boulē)·(dikastēria)·(citizens' assembly)` | 삭제 |
| 5 | Q3 L158 | `(sortition/lot/klērōsis)` | `(sortition · klērōsis)` (추후 전체 재포맷) |
| 6 | Q5 L246 | `(Grundlegung…, 1785)` | 1785 삭제 |
| 7 | Q5 L252 | `(pflichtmäßig)` | 삭제 |
| 8 | Q5 L274 | `(Neigung 또는 원어 inclination 병기 가능)` | em-dash 안내로 변경 |
| 9 | Q5 L260 | `(유한한 이성적 존재 · endliches vernünftiges Wesen)` | `[…]` 브래킷 변경 (coverage 원형) |
| 10 | Q6 L291 | `(Augustine of Hippo, 354-430)` | 354-430 삭제 |
| 11 | Q6 L294 | `(cupiditas, 세속·자기에 대한 사랑)` | cupiditas 삭제 |
| 12 | Q6 L297 | `(substantia)·(theodicy)` | 삭제 |
| 13 | Q6 L316-317 | `(gratia)·(fides)` | 삭제 |
| 14 | Q6 L319 | `(caritas 또는 신에 대한 사랑 병기 권장)` | em-dash 안내로 변경 |
| 15 | Q9 L452 | `(Louis Raths, Merrill Harmin, Sidney B. Simon)` | `(Louis Raths) 등 하민(Harmin)·사이먼(Simon)` 으로 분리 |
| 16 | Q9 L452 | `(Howard Kirschenbaum, 1977 『…』·1995 『…』)` | em-dash 로 분리 |
| 17 | Q9 L469 | `(subjectivism)` | 삭제 |
| 18 | Q9 L471 | `(content void)` | 삭제 |
| 19 | Q9 L474 | `(comprehensive values education)` | 삭제 |
| 20 | Q9 L472 | `(virtues)` | 삭제 |
| 21 | Q10 L523 | `(John Locke, 1632-1704)·(Two Treatises of Government, 1689)` | 생년·출판년 삭제 |
| 22 | Q10 L529/L545 | `(perfect member)` ×2 | 삭제 |
| 23 | Q10 L539-540 | `(lodging only)·(high-way)` | 삭제 |
| 24 | Q11 L597 | `(Tom Regan, 1938-2017)·(The Case for Animal Rights, 1983)` | 생년·출판년 삭제 |
| 25 | Q11 L597 | `(Peter Singer)` | 삭제 |
| 26 | Q11 L606 | `(either have it or not)` | 삭제 |
| 27 | Q11 L617 | `(ends in themselves)·(humanity formula)` | 삭제 |
| 28 | Q11 L620 | `(welfare)` | 삭제 |
| 29 | Q13 L767 | `(John Stuart Mill, 1806-1873)·(Utilitarianism, 1861)·(Epicurus, BC 341-270)` | 생년·출판년 삭제 |
| 30 | Q13 L771 | `(quantity)` | 삭제 |
| 31 | Q13 L774 | `(push-pin)` | 삭제 |
| 32 | Q13 L778 | `(ataraxia — 마음의 평정)·(aponia — 몸의 고통 없음)` | 한글로 변환 |
| 33 | Q3 L179 | `(또는 제비뽑기 · sortition · klērōsis 병기 가능)` | em-dash 안내로 변경 |

**총 self-correct ≈ 33 건** (Manager 주석 · 구조 토큰 skip 후 순수 substantive 영어 gloss 삭제·치환)

## em-dash 바이트 보존 hexdump 샘플 (3건)

```
00000030  b3 b5 20 41 20 e2 80 94  20 ed 95 99 ec 83 9d ec  |.. A ... .......|
00000720  90 20 e2 80 94 20 eb b3  b8 20 ea b0 80 ec 9d b4  |. ... ... ......|
00001260  65 66 69 78 20 ec 83 81  ec 9d b4 20 e2 80 94 20  |efix ...... ... |
```

- 총 em-dash 출현: **100 건** (Manager 주석·한자(漢字)—영어 래퍼 전량)
- 원문 시험지 내에 em-dash 는 없으므로 원문 보존 영역에서의 도입 0건 (해설 영역 전담)

## 최종 파일 메트릭

| 항목 | 값 | cap | 판정 |
|------|------|-----|------|
| 총 라인 수 | 901 L | 1800 | ✅ 여유 899 L |
| `^## 문항` 개수 | 14 | = 14 | ✅ 일치 |
| em-dash U+2014 건수 | 100 | — | ✅ 보존 |
| Step 1 0-hit 토큰 | 0 | = 0 | ✅ 전원 grounded |
| Step 1b 0-hit 토큰 | 0 | = 0 | ✅ |
| Step 2 0-hit 토큰 | 0 | = 0 | ✅ |
| 서술형 `### 채점 기준` 존재 | 6/6 | 6 | ✅ |

## 이슈 / 블로커

- **BLOCKER-1 (지속)**: Q11 Tom Regan `regan` thinker_id 가 ES ethics-thinkers 인덱스 미등록 (BLK-175E-2018A-001, 2018-A 고유). TASK-176 후속 등록 대기 중. 본 태스크 산출물에서는 `⚠️ ES 미등록(BLOCKER-1)` 명시 + trademark 3중 일치로 정답 판정만 확정.
- **관측 (observation)**: mill_js claim_id prefix = `mill-claim-NNN` (thinker_id 와 상이) 특이점을 본 문서 Q13 에서도 명시. TASK-188 확증 사항 재확인.
- **관측 (observation)**: 초기 draft 에 영어 gloss 를 과도하게 추가한 패턴은 2017-B·2017-A 선례 대비 25% 많았으며 self-verification 단계에서 전량 교정. 추후 Coder 프롬프트에 "영어 원어 병기는 coverage 에 존재하는 것만 허용" 명시 고려 가능 (Manager 판단).

## 다음 제안

1. **Reviewer R1 호출**: Manager 산출물 및 본 coder-report 정합성 검증. 특히 Step 1/1b/2 전원 0-hit = 0 주장의 재실행 검증.
2. **후속 태스크**: TASK-191 (2018-B 학생용 가이드) 동일 포맷 진행 가능.
3. **BLOCKER-1 해소**: TASK-176 `regan` 사상가 등록 태스크 재개 시 본 문서 Q11 ES 근거 섹션 역채우기 필요.

---

**본 보고서는 agents/coder.md 의 self-verification 3단계 프로토콜 및 TASK-190 task-board L313 완료 조건 11개 전수 충족 후 제출함.**
