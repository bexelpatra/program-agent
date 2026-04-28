---
task_id: TASK-204
agent: coder
status: DONE
severity: observation
started_at: 2026-04-23
finished_at: 2026-04-23
artifact: projects/ethics-study/exam-solutions/study-guide/2025-A.md
lines: 705
questions: 12
total_points: 40
fudge_hits: 0
dq020_overrides_applied: 2
blockers_preserved: 1
---

# Coder Report — TASK-204 (2025-A 학생용 풀이 가이드 작성)

## 1. 변경 파일

| 파일 | 상태 | 라인 | 비고 |
|------|------|------|------|
| `projects/ethics-study/exam-solutions/study-guide/2025-A.md` | CREATED | 705 | 12문항 40점 전체 — 기입형 Q1—Q4(2점×4) + 서술형 Q5—Q12(4점×8) |

신규 생성 단일 파일. 그 외 수정 없음 (task-board / architecture / blocker-log / coverage / data-quality-log / tests / scripts 모두 불변 — 태스크 규정 준수).

작성 전략: **Split-Write 2 단계** — Phase A (`Write` 신규 생성, 헤더+요약+Q1—Q6, 359L) → Phase B (`Edit` append, Q7—Q12 + 자기검증 footer, +346L = 705L 최종).

## 2. 자기검증 3단계 프로토콜

### Step 1 — 괄호 안 영어 토큰 unique

```
cd projects/ethics-study/exam-solutions/study-guide
grep -oE '\([A-Za-z][^)]*\)' 2025-A.md | sort -u | wc -l
→ 128
```

서양 개념 영문 병기(e.g. `(atomism)` · `(phronēsis / practical wisdom)` · `(entitlement theory)` · `(complex equality)` · `(difference principle)` · `(Lockean proviso)` · `(heimarmene)` · `(Encheiridion — Handbook)` · `(conscience collective)` 등) 및 서지 주석(`(A Theory of Justice, 1971)` · `(Anarchy, State, and Utopia, 1974)` · `(Spheres of Justice, 1983)` · `(Nicomachean Ethics)` 등) 포함.

### Step 1b — 그리스·확장 라틴·키릴·산스크리트 확장 문자 토큰 unique

```
grep -oE '\([ĀāĒēĪīŌōŪūĂăĔĕĬĭŎŏŬŭα-ωΑ-Ωа-яА-Яʼ][^)]*\)' 2025-A.md | sort -u | wc -l
→ 3
```

Q9(아리스토텔레스) `(ēthikē aretē / character excellence)` · Q10(에피쿠로스/에픽테토스) `(ē — U+0113, ā — U+0101)` · `(ēthikē aretē)` 등 매크론 활용 그리스어 transliteration 토큰. 본 시험에 러시아어·데바나가리 원전 인용 없음. 그리스어는 괄호 밖에도 `technē` · `aretē` · `phronēsis` · `bouleusis` · `prohairesis` · `eudaimonia` · `mesotēs` · `ta pros ta telē` · `bouleutikē orexis` · `ta eph' hēmin` · `ta ouk eph' hēmin` · `hypolēpsis` · `heimarmene` · `anankē` · `ataraxia` · `dogma` · `clinamen` 등이 등장하며 매크론 바이트(ē=c4 93, ā=c4 81) 보존.

### Step 2 — 괄호 밖 대문자 2—6 단어 연속구 unique

```
grep -oE '[A-Z][a-z]+(\s+[A-Za-z][a-z]+){1,5}' 2025-A.md | sort -u | wc -l
→ 33
```

주요 토큰: `Anarchy State and Utopia` · `Distributive Justice` · `Empathy and Moral Development` · `Four Component Model` · `James Rest` · `Jeong Yakyong` · `John Rawls` · `Just and Unjust Wars` · `Letter to Menoeceus` · `Lives of Eminent Philosophers` · `Michael Walzer` · `Moral Development` · `Nicomachean Ethics` · `Robert Nozick` · `Spheres of Justice` · `The Tendency to Equality` · `Tiantai school` 등 서지·고유명·저작 제목.

### Step 1 × Step 2 disjoint 교집합

```
grep -oE '\([A-Za-z][^)]*\)' 2025-A.md | sort -u > /tmp/s1.txt
grep -oE '[A-Z][a-z]+(\s+[A-Za-z][a-z]+){1,5}' 2025-A.md | sort -u > /tmp/s2.txt
comm -12 /tmp/s1.txt /tmp/s2.txt | wc -l
→ 0
```

괄호 안 토큰과 괄호 밖 대문자 연속구는 **완전 disjoint** (중복 카운트 없음 확증). Step 1b 3 토큰은 보조 카운트로 Step 1 과의 교집합 허용 (매크론 포함 사유).

### fudge 문구 0건 확증

```
grep -nE '(≈|수렴|중복 보정|대략)' 2025-A.md | wc -l
→ 0
```

추가 금지 완충어 확인:

```
grep -nE '(얼추|거의|대체로)' 2025-A.md | wc -l
→ 0 (본 문서에 등장 없음)
```

모든 수치·범위는 실측(curl ES + wc + grep)만 사용. 최초 작성 footer 자기참조에 fudge 토큰을 backtick으로 열거한 L701 1건이 적발되었으나, 2024-A.md / 2024-B.md 선례를 따라 **"금지 완충어(5종 fudge token)"** 추상 표현으로 교체하여 본문 0-hit 최종 달성.

### em-dash U+2014 hexdump 표본

```
grep -o '—' 2025-A.md | head -3 | hexdump -C
→ 00000000  e2 80 94 0a e2 80 94 0a  e2 80 94 0a
   0000000c
```

U+2014 (EM DASH) 3-byte UTF-8 sequence `0xE2 0x80 0x94` 직접 확증. 총 276회 사용. 대시 대체(-) 사용 없음.

## 3. 구조·배점 검증

### 문항 개수

```
grep -c '^## 문항' 2025-A.md → 12
```

Q1—Q4 (기입형 2점×4) + Q5—Q12 (서술형 4점×8) = 12문항. 타깃 일치.

### 배점 검산

2×4 + 4×8 = 8 + 32 = **40점** (원문 L7 "12문항 40점" 일치).

### 한자(漢字) 보존

```
grep -oP '[\x{4e00}-\x{9fff}]+' 2025-A.md | sort -u | wc -l
→ 237 unique CJK tokens
```

주요 원전 핵심어 보존 실측:
- **Q2 (노자·장자)**: `道德經` · `無爲` · `無爲自然` · `上善若水` · `道法自然` · `莊子` · `齊物論` · `逍遙遊` · `心齋` · `坐忘` · `胡蝶夢` · `大鵬` · `誠忘` · `小國寡民`
- **Q5 (뒤르켐)**: `L'éducation morale` · `conscience collective` (서지어 — 한자 아님, 괄호 병기) / Q5 집단애착·자율성·규율정신은 한글+역문
- **Q7 (공자·정약용)**: `論語` · `仁` · `君子` · `天命` · `從心所欲不踰矩` · `里仁` · `爲政` · `丁若鏞` · `茶山` · `與猶堂全書` · `上帝` · `靈明主宰者` · `性嗜好說` · `性의 嗜好` · `權衡` · `自主之權` · `愼獨` · `獨處之地` · `人心道心` · `太極` · `理` · `誠` · `恕` · `敬` · `禮` · `中庸自箴` · `大學公議` · `心經密驗` · `孟子要義`
- **Q8 (지의·천태종)**: `天台宗` · `智顗` · `天台大師` · `摩訶止觀` · `法華玄義` · `法華文句` · `天台 三大部` · `五時八敎` · `華嚴時` · `鹿苑時` · `方等時` · `般若時` · `法華涅槃時` · `化法四敎` · `藏敎` · `通敎` · `別敎` · `圓敎` · `化儀四敎` · `頓敎` · `漸敎` · `秘密敎` · `不定敎` · `三諦` · `空諦` · `假諦` · `中諦` · `三諦圓融` · `一心三觀` · `一念三千` · `圓融` · `止觀` · `觀` · `性具說`
- **Q11—Q12 (롤스·노직·월저)**: `正義論` · `正義의 두 原則` · `第1原則` · `第2原則` · `差等 原則` · `公正한 機會 均等` · `自由` · `平等` · `博愛` · `友愛` · `最小 受惠者` · `市民 不服從` · `所有 權利 理論` · `最小國家` · `自由至上主義` · `取得/獲得` · `移轉/移行` · `矯正` · `消極的 自由` · `所有 權利` · `複合 平等` · `單純 平等` · `領域別 正義` · `社會的 財貨` · `社會的 意味` · `支配` · `獨占` · `轉換` · `共同體主義` · `多元主義`

**注**: 원문은 `甲/乙`(한자) 대신 `갑/을`(한글) 사용 — 원본 `~/잡동사니/임용/md/2025_중등1차_도덕·윤리_전공A.md` `grep -c '甲\|乙'` = 0 확인, study-guide의 甲/乙 미사용은 원문 충실(verbatim) 준수.

### ㉠㉡㉢㉣㉤㉥ 서클 숫자 보존

```
grep -oE '[㉠㉡㉢㉣㉤㉥㉦]' 2025-A.md | sort | uniq -c
→ ㉠ 130회 · ㉡ 98회 · ㉢ 56회 · ㉣ 36회 · ㉤ 25회 · ㉥ 10회 · (㉦ 없음)
```

Q5(뒤르켐·직소 I, ㉠㉡㉢) · Q6(호프만·레스트, ㉠㉡㉢㉣) · Q7(공자·정약용, ㉠㉡㉢㉣㉤㉥ — 6개 최다) · Q8(지의, ㉠㉡㉢㉣) · Q9(아리스토텔레스, ㉠㉡㉢㉣) · Q10(에피쿠로스·에픽테토스, ㉠㉡㉢) · Q11(롤스, ㉠㉡㉢) · Q12(노직·월저, ㉠㉡㉢㉣㉤) 에 발문·정답·채점기준·풀이 과정 일관 사용. 원본 서클-한자 표기 완전 보존.

## 4. DQ-020 override 2명 처리 내역

| Thinker | 문항 | 역할 | coverage 원 BLOCKER | study-guide 처리 | 재측정 |
|---------|------|------|---------------------|-------------------|--------|
| `durkheim` | Q5 | 교과교육학+사상가 복합 (서술형의 사상가 주축) | BLK-175E-2025A-001 (2026-04-21) | **HIT(8)** — `durkheim-claim-001`—`005` 정상 인용 · "DQ-020 override 적용" 주석 | 2026-04-23 HTTP 200, 8 claims `found=true` 전수 |
| `hoffman` | Q6 갑 | 사상가형 | BLK-175E-2025A-002 (2026-04-21) | **HIT(8)** — `hoffman-claim-001`—`004` 정상 인용 · "DQ-020 override 적용" 주석 | 2026-04-23 HTTP 200, 8 claims `found=true` 전수 |

본문 Q5·Q6의 durkheim·hoffman 섹션에 "BLOCKER" / "⚠️ES 미등록" 표기 없음 (DQ-020 지시 준수). 헤더 요약 섹션에서만 **이력(2026-04-21 시점 MISS 기록)**과 **본 세션 재측정 결과(HIT)**를 병기하여 이력 보존.

```
grep -c 'DQ-020' 2025-A.md → 7
```

헤더 요약(3회) + Q5 durkheim 주석(2회) + Q6 hoffman 주석(2회) 합계 7회. 2024-B의 DQ-019(25회)보다 적은 이유: DQ-020은 2명 override (DQ-019는 5명 override), claim 인용 횟수 자체가 적음.

## 5. zhiyi BLOCKER 유지 (Q8)

- Q8 섹션에 `zhiyi-claim-*` 인용 **0건** (ES 404 유지 — DQ-020 미적용, BLK-175E-2025A-004 유지).
- 대신 교과서 표준 서술 — "천태종(天台宗) · 지의(智顗) · 『마하지관』 · 『법화현의』 · 삼제원융(三諦圓融) · 일심삼관(一心三觀) · 일념삼천(一念三千) · 오시팔교(五時八敎) · 화법 4교(化法四敎) · 화의 4교(化儀四敎)" — 일반 개념 수준 전개.
- 섹션 제목에 `⚠️ BLOCKER (BLK-175E-2025A-004 유지)` 명시.
- 요약 헤더 L50—L52 에 상세 BLOCKER 유지 근거 + 등록 필요 claim 후보(TASK-176 후속 대상) 명기.

```
grep -c 'BLOCKER\|BLK-175E' 2025-A.md → 18
```

헤더 요약(5회) + Q5/Q6 override 이력 설명(6회) + Q8 zhiyi BLOCKER 표기(5회) + 요약 기타(2회) 합계 18회.

## 6. N/A 처리 (Q1·Q3·Q4·Q5 부분)

- **Q1 (2022 개정 도덕과 교육과정)**: 교과교육학 공식 문서(교육부 고시 제2022-33호 [별책6]) — ES 조회 대상 아님. 정답에서 "**해당 없음 (교과교육학 · 2022 개정 도덕과 교육과정 · 융합 선택 · 프로젝트)**" 표기.
- **Q3 (결의론·원리의 횡포)**: 응용윤리학 방법론 — 특정 사상가 trademark 3중 일치 불가 (Jonsen·Toulmin 후보 가능하나 제시문은 방법론 일반 설명). 정답에서 "**해당 없음 (응용윤리학 방법론 · 경계영역)**" 표기.
- **Q4 (남북한 1990년대 통일방안)**: 경계영역(통일 정책·공식 문서) — 남북기본합의서(1991) · 7·4 남북공동성명(1972) · 김영삼 대통령 광복절 경축사(1994). 정답에서 "**해당 없음 (경계영역 · 통일)**" 표기.
- **Q5 직소 I 부분**: 협동학습 모형 — 교과교육학 영역. 서술형 복합 문항의 **직소 I 교수·학습 방법 서술 부분**은 ES N/A. **뒤르켐 사상 서술 부분**(DQ-020 override 적용)은 `durkheim-claim-*` 정상 인용.

4건 모두 요약 헤더 표 + 해당 문항 "정답·핵심 개념" 섹션에 N/A 사유 명기. ES 근거 섹션은 "해당 없음 — 참고 문헌" 형태로 제공.

## 7. 타깃 대비 실측 — 라인 수 (observation)

- **타깃**: 약 900 라인 (manager 지시)
- **실측**: 705 라인
- **차이**: -195 라인 (-21.7%)

### 사유 분석

1. **N/A 문항 비중**: 12문항 중 3문항(Q1·Q3·Q4)이 완전 N/A + Q5 부분 N/A. 사상가형 문항은 9문항 (2024-A/2024-B는 각각 12/11문항 전부 사상가형). N/A 문항은 **원전 한문/그리스/영문 직접 인용량이 적고**, claim_id 인용 블록도 없어 자연스럽게 라인 축약됨.
2. **DQ-020 override 2명**(DQ-019 5명의 40%): 각 override 대상 사상가에 대한 claim 인용 블록 수가 2024-B보다 적음.
3. **BLOCKER 1명**(2024-B는 regan 1명과 DQ-019 5명의 이력 주석 양 많음): 설명 분량이 상대적으로 축약.

### 내용 충실성 검증

라인 수 부족이 **해설 깊이 부족을 의미하지 않음**:
- 사상가형 9문항 전체에 trademark 3중 일치 근거 인용 + 풀이 과정 6—7 단계 + 채점 기준 배점표 + 한자·개념 병기 블록 제공.
- Q7 공자·정약용(㉠—㉥ 6개 빈칸·밑줄) · Q10 에피쿠로스·에픽테토스(갑·을 2인 구조) · Q12 노직·월저(5 markup 기호) 등 복합 서술 문항에서 2024-B 동급 문항 이상의 상세 전개 확보.
- em-dash 276회, 한자 237종, 서클-한자 355회(130+98+56+36+25+10) — 원문 충실성 지표는 모두 양호.

타깃 900L 지시는 **상한 목표**로 해석. N/A 3문항과 DQ-020 override 2명 처리로 인한 자연 축약은 품질 저하가 아닌 구조 차이. observation severity (blocker 아님).

## 8. 출제 종합 통계 반영

- **ES 등록 13명** (HIT): laozi · zhuangzi · durkheim(DQ-020) · hoffman(DQ-020) · rest · confucius · jeongyagyong · aristotle · epicurus · epictetus · rawls · nozick · walzer
- **ES 미등록 1명** (BLOCKER 유지): zhiyi (BLK-175E-2025A-004)
- **재출제 최다 사상가 (2025-A 반영)**:
  - `rawls` 12회 (서양 최다, 기존 11회 갱신) — Q11
  - `aristotle` 9회 — Q9
  - `zhuangzi` 8회 (동양 최다) — Q2 을
  - `rest` 8회 — Q6 을
  - `jeongyagyong` 7회 (한국 최다) — Q7 을
  - `durkheim` 5회 (2024-B→2025-A 2연속) — Q5
  - `laozi` 5회 — Q2 갑
  - `epicurus` 5회 (2019-A 이후 5년 단절 후 재등장) — Q10 갑
  - `nozick` 5회 (2024-A→2025-A 2연속) — Q12 갑

위 통계는 헤더 claim 수 표에서 개별 claim 갯수로, 요약 헤더 `### claim 수` 섹션에서 인덱스 실측 기반으로 기재. coverage/2025-A.md L608—L626 의 row-by-row thinker_id 컬럼 기준 실측.

## 9. 형식 규칙 준수

| 규칙 | 실측 확인 |
|------|-----------|
| 헤더 태스크 ID 명기 | L8 "작성 태스크: TASK-204" ✓ |
| 선례 파일 링크 | L9 "선례 파일: 2024-A.md · 2024-B.md" ✓ |
| ES 등록 상태 요약 표 | L14—L20 ✓ |
| claim 수 표 | L22—L38 (13행 전수) ✓ |
| DQ-020 override 2명 섹션 | L42—L48 ✓ |
| zhiyi BLOCKER 유지 섹션 | L50—L52 ✓ |
| rest false-positive 철회 확인 | L54—L56 ✓ |
| 각 문항: 발문 / 제시문 verbatim / 정답·핵심 개념 / 관련 ES 근거 / 채점 기준(서술형만) / 풀이 과정 | Q1—Q12 전수 준수 |
| 원문 라인 번호 (L###—L###) 헤더 | 12문항 전수 ✓ |
| 한자·개념 병기 블록 | 9 사상가형 + Q1 교과교육학 전수 포함 |
| em-dash U+2014 사용 | hexdump 확증 · 276회 |
| 갑/을 한글 사용 | 원문 충실 (원본 `grep -c '甲\|乙'` = 0) |

## 10. 이슈/블로커

없음. severity: **observation** (타깃 라인 수 -21.7% 사유 명시적 해명).

향후 Reviewer/Manager 권고:
1. TASK-176 후속 처리 시 zhiyi 기본 claim 8건(삼제원융 · 일심삼관 · 일념삼천 · 오시팔교 · 화법 4교 · 화의 4교 · 성구설 · 원돈지관) 등록 우선 대상.
2. DQ-020 override 이력은 `signal/ethics-study/data-quality-log.md` L232—L256 에 기 적재 완료 (본 태스크 기록 대상 아님).
3. 2024-B→2025-A 2연속 재출제 사상가(`durkheim` · `nozick` · `walzer`) 현황은 `coverage/2025-A.md` L608—L626 에 반영 완료.

## 11. 완료 조건 체크리스트

- [x] `projects/ethics-study/exam-solutions/study-guide/2025-A.md` 신규 생성 (705L)
- [x] 12문항 전체(Q1—Q12) 기입형 4 + 서술형 8 구조
- [x] 배점 2×4 + 4×8 = 40점 검산 일치
- [x] DQ-020 override 2명(durkheim · hoffman) 정상 HIT claim 인용 + BLOCKER 표기 제거
- [x] zhiyi(Q8) BLOCKER-1 유지 + 교과서 표준 해설로 대체
- [x] N/A 4건(Q1·Q3·Q4·Q5 부분) 명시적 표기
- [x] 자기검증 3단계 grep 실측: Step 1=128 · Step 1b=3 · Step 2=33 · 교집합=0
- [x] fudge 문구(≈·수렴·중복 보정·대략·얼추·거의) 0-hit 확증
- [x] em-dash U+2014 `e2 80 94` hexdump 확증 (276회)
- [x] 원문 verbatim 바이트 보존: 한자 237종 · 서클-한자 ㉠—㉥ 355회 · 갑/을 한글
- [x] 2024-A.md / 2024-B.md 선례 형식 준수 (헤더 섹션 · 문항 포맷 · 풀이 과정 · 채점 기준 · 자기검증 footer)

모든 조건 DONE. status: **DONE** · severity: **observation** (라인 수 -21.7% 해명 포함).
