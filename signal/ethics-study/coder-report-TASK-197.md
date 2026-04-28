---
task_id: TASK-197
agent: coder
model: opus-4.7
status: DONE
severity: none
date: 2026-04-23
target_file: projects/ethics-study/exam-solutions/study-guide/2021-B.md
---

# Coder Report · TASK-197 · 2021-B 학생용 풀이 가이드

## 요약

- **태스크**: 2021학년도 중등임용 도덕·윤리 전공 B 학생용 풀이 가이드 작성 (Track B 시리즈 16/26)
- **산출물**: `projects/ethics-study/exam-solutions/study-guide/2021-B.md` **1074 라인** (목표 ≤1100L 이내)
- **결과**: 11문항 전건 · 40점 배점(기입형 2점×2 + 서술형 4점×9) · 9건 채점 기준(서술형 Q3-Q11) · 16명 사상가 ES 근거(정상 12 + DQ-015 override 4) · 3건 ⚠️BLOCKER(uicheon·kierkegaard·cicero)
- **특이점**: 본 시험 11문항 **전원 사상가형** — 교과교육학/교육과정/외부 문헌 면제 식별자 문항 0건
- **DQ-015 override 4건**: `jinul`(Q1 을) · `turiel`(Q3 갑) · `durkheim`(Q4 갑) · `hoffman`(Q5 을) 모두 본 세션 curl 실측 `found=true` 확증
- **잔존 BLOCKER 3건**: `uicheon`(Q1 갑 · BLK-175E-2021B-001) · `kierkegaard`(Q8 을 · BLK-175E-2021B-006) · `cicero`(Q10 · BLK-175E-2021B-007). 본 세션 curl 실측 `found=false` 재확증. trademark 3중 일치로 정답 확정은 가능

## 파일 구조 검증

| 항목 | 기대 | 실측 | 판정 |
|------|------|------|------|
| 총 라인 수 | ≤1100 | **1074** | PASS |
| `^## 문항` 섹션 개수 | 11 | **11** | PASS |
| `^### 발문` 섹션 개수 | 11 | **11** | PASS |
| `^### 제시문` 섹션 개수 | 11 | **11** | PASS |
| `^### 정답` 섹션 개수 | 11 | **11** | PASS |
| `^### 관련 ES 근거` 섹션 개수 | 11 | **11** | PASS |
| `^### 채점 기준` 섹션 개수 | 9 (서술형 Q3-Q11) | **9** | PASS |
| `^### 풀이 과정` 섹션 개수 | 11 | **11** | PASS |
| 배점 합계 | 기입형 2점×2 + 서술형 4점×9 = 40점 | 40점 | PASS |

## 문항별 원문 라인 범위 확증

| Q | 스펙 line 범위 | 가이드 헤더 | 실측 유형·점수 |
|---|----------------|-------------|----------------|
| Q1 | L14-L22 | `## 문항 1 · 기입형 · 2점 · 원문 line L14-L22` | 기입형 2점 |
| Q2 | L24-L31 | `## 문항 2 · 기입형 · 2점 · 원문 line L24-L31` | 기입형 2점 |
| Q3 | L33-L46 | `## 문항 3 · 서술형 · 4점 · 원문 line L33-L46` | 서술형 4점 |
| Q4 | L48-L60 | `## 문항 4 · 서술형 · 4점 · 원문 line L48-L60` | 서술형 4점 |
| Q5 | L62-L74 | `## 문항 5 · 서술형 · 4점 · 원문 line L62-L74` | 서술형 4점 |
| Q6 | L76-L88 | `## 문항 6 · 서술형 · 4점 · 원문 line L76-L88` | 서술형 4점 |
| Q7 | L90-L102 | `## 문항 7 · 서술형 · 4점 · 원문 line L90-L102` | 서술형 4점 |
| Q8 | L104-L116 | `## 문항 8 · 서술형 · 4점 · 원문 line L104-L116` | 서술형 4점 |
| Q9 | L118-L130 | `## 문항 9 · 서술형 · 4점 · 원문 line L118-L130` | 서술형 4점 |
| Q10 | L132-L143 | `## 문항 10 · 서술형 · 4점 · 원문 line L132-L143` | 서술형 4점 |
| Q11 | L145-L155 | `## 문항 11 · 서술형 · 4점 · 원문 line L145-L155` | 서술형 4점 |

모든 line 범위 스펙과 1:1 일치.

## 문항별 사상가·claim 매핑

| Q | 유형·점수 | 사상가(thinker_id) | 정답 요지 | ES claim 근거 |
|---|----------|-------------------|-----------|---------------|
| Q1 | 기입형 2점 | 갑: `uicheon` ⚠️BLOCKER-1 · 을: `jinul` (DQ-015 override) | 갑 ㉠ 敎觀兼修 교관겸수 · 을 ㉡ 定慧雙修 정혜쌍수 | jinul-claim-* (9건) + uicheon 원전(『원종문류』) |
| Q2 | 기입형 2점 | `locke` | ㉠ 재산(property) · ㉡ 입법권 최고성(supremacy of legislative power) | locke-claim-* (12건) |
| Q3 | 서술형 4점 | 갑: `turiel` (DQ-015 override) + 을: `haidt` | 영역이론 3영역 · 사회적 직관주의 · 코끼리와 기수 | turiel-claim-* (8건) + haidt-claim-* (10건) |
| Q4 | 서술형 4점 | 갑: `durkheim` (DQ-015 override) + 을: `piaget` | 도덕 3요소·자율성 vs 도덕 상대주의·타율→자율 | durkheim-claim-* (8건) + piaget-claim-* (14건) |
| Q5 | 서술형 4점 | 갑: `rest` + 을: `hoffman` (DQ-015 override) | 4구성요소(민감성·판단·동기·품성) · 공감 발달 5단계 | rest-claim-* (10건) + hoffman-claim-* (8건) |
| Q6 | 서술형 4점 | 갑: `laozi` + 을: `zhuangzi` | 현동(玄同)·삼보(三寶) vs 양행(兩行)·제물(齊物) | laozi-claim-* (12건) + zhuangzi-claim-* (10건) |
| Q7 | 서술형 4점 | 갑: `yiyulgok` + 을: `yihwang` | 기발이승일도설 vs 이기호발설·이발이기수지/기발이이승지 | yiyulgok-claim-* (12건) + yihwang-claim-* (12건) |
| Q8 | 서술형 4점 | 갑: `sartre` + 을: `kierkegaard` ⚠️BLOCKER-2 | 실존적 휴머니즘·앙가주망 vs 절망·신 앞의 단독자 | sartre-claim-* (8건) + kierkegaard 원전(『죽음에 이르는 병』) |
| Q9 | 서술형 4점 | 갑: `aristotle` + 을: `mill_js` | 목적(telos)·에우다이모니아 vs 편의(expediency)·덕의 내재화 | aristotle-claim-* (12건) + mill-claim-* (17건 · mill_js prefix 주의) |
| Q10 | 서술형 4점 | `cicero` ⚠️BLOCKER-3 | ㉠ 법(ius) · ㉡ 공동 이익(utilitas communis) · ㉢ 혼합정체 | cicero 원전(『De Re Publica』 I.39/I.45) |
| Q11 | 서술형 4점 | `habermas` | ㉠ 예/아니오 입장 표명(Ja/Nein-Stellungnahme) · ㉢ 심의 민주주의 · ㉡ 3타당성 주장(진리성·정당성·진실성) | habermas-claim-* (8건) |

**총 ES claim 근거**: 16명 사상가(정상 12 + DQ-015 override 4) 전원 `found=true` 확증 · 모두 `ethics-claims` 인덱스 curl 실측.

## ES 실측 결과 (본 세션 curl)

### thinker 존재 확증

| thinker_id | found | name (ES _source) |
|------------|-------|-------------------|
| uicheon | **false** ⚠️BLOCKER-1 | NOT_FOUND |
| jinul | true | 보조국사 지눌 (知訥) |
| locke | true | 존 로크 |
| turiel | true | 튜리엘 (Elliot Turiel) |
| haidt | true | 조너선 하이트 |
| durkheim | true | 에밀 뒤르켐 (Émile Durkheim) |
| piaget | true | 장 피아제 |
| rest | true | 제임스 레스트 |
| hoffman | true | 마틴 호프만 (Martin L. Hoffman) |
| laozi | true | 노자 |
| zhuangzi | true | 장자 |
| yiyulgok | true | 이이 (李珥, 율곡) |
| yihwang | true | 이황 (李滉, 퇴계) |
| sartre | true | 장폴 사르트르 |
| kierkegaard | **false** ⚠️BLOCKER-2 | NOT_FOUND |
| aristotle | true | 아리스토텔레스 |
| mill_js | true | 존 스튜어트 밀 |
| cicero | **false** ⚠️BLOCKER-3 | NOT_FOUND |
| habermas | true | 위르겐 하버마스 |

### claim 개수 확증 (ethics-claims `_count` with `term: {thinker_id: ...}`)

| thinker_id | claim 수 | 스펙 기대치 | 판정 |
|------------|----------|-------------|------|
| jinul | **9** | 9 | PASS |
| locke | **12** | 12 | PASS |
| turiel | **8** | 8 | PASS |
| haidt | **10** | 10 | PASS |
| durkheim | **8** | 8 | PASS |
| piaget | **14** | 14 | PASS |
| rest | **10** | 10 | PASS |
| hoffman | **8** | 8 | PASS |
| laozi | **12** | 12 | PASS |
| zhuangzi | **10** | 10 | PASS |
| yiyulgok | **12** | 12 | PASS |
| yihwang | **12** | 12 | PASS |
| sartre | **8** | 8 | PASS |
| aristotle | **12** | 12 | PASS |
| mill_js | **17** | 17 | PASS |
| habermas | **8** | 8 | PASS |

16/16 일치. 총 claim = **170건** (9+12+8+10+8+14+10+8+12+10+12+12+8+12+17+8).

## DQ-015 override 확증

DQ-015 데이터 품질 로그 L77-L109 규정에 따라, coverage/2021-B.md의 7건 BLOCKER 중 4건을 재검증해 `found=true` 확정 → 정상 ES 근거로 사용.

| override thinker | 사용 문항 | coverage 원 BLOCKER id → 해소 | 가이드 본문 위치 |
|------------------|-----------|-------------------------------|------------------|
| `jinul` | Q1 을 (기입형 2점) | BLK-175E-2021B-002 → 재분류 | L71 본문 · L97 근거 표 |
| `turiel` | Q3 갑 (서술형 4점) | BLK-175E-2021B-003 → 재분류 | L207 본문 · L248 근거 표 |
| `durkheim` | Q4 갑 (서술형 4점) | BLK-175E-2021B-004 → 재분류 | L313 본문 · L352 근거 표 |
| `hoffman` | Q5 을 (서술형 4점) | BLK-175E-2021B-005 → 재분류 | L418 본문 |

공지 선언:
- L19: ES 등록 상태 요약 표 중 "✅ DQ-015 override 등록 (4명)" 행에 4명 나열
- L23: HTML 주석으로 override 경위 명시
- L46: 공지 문단 "ES 등록 ✅ 12명 + DQ-015 override ✅ 4명 = 총 16명 unique" 선언

## 잔존 BLOCKER 3건 (ES-gap이지만 해설 저지선 아님)

| BLOCKER id | thinker_id | 문항 | 가이드 본문 ⚠️ 표기 위치 |
|------------|-----------|------|-----------------------------|
| BLK-175E-2021B-001 | `uicheon` | Q1 갑 | L70 본문 · L96 근거 표 |
| BLK-175E-2021B-006 | `kierkegaard` | Q8 을 | L756 본문 · L792 근거 표 |
| BLK-175E-2021B-007 | `cicero` | Q10 | L964 본문 |

각 BLOCKER는 trademark 3중 일치 + 원전 직접 인용으로 정답 확정 가능. TASK-176 계열 후속 등록 시 해소 예정.

## 자기검증 3단계 결과 (sort -u | wc -l 실측 기준 · 정확 일치 의무)

### Step 1: bare-paren English 토큰 (`\([A-Za-z][^)]*\)`)

- 실측 `sort -u | wc -l` = **243**
- 분류 (disjoint):
  - N₁ 면제 식별자 (BLK-/DQ-/L\d+/TASK-/BLOCKER/ES-gap/ES 등록/기입형/서술형/원문/검산 등): **60**
  - N₂ coverage-textual (coverage/2021-B.md에 inner 문자열 일치): **112**
  - N₃ coverage-absent (학술 전거·라틴어·독어·불어·ES 어휘 등 coverage 외부 근거): **71**
- 검산: 60 + 112 + 71 = **243** ✅ (정확 일치 · fudge 문구 없음)

### Step 1b: Greek/Cyrillic/Latin-extended paren 토큰 (unicode 범위 [\u00c0-\u024f\u0370-\u03ff\u0400-\u04ff])

- 실측 unique 개수 = **30**
- 분류 (disjoint):
  - N₁ 면제 식별자: **7**
  - N₂ coverage-textual: **10**
  - N₃ coverage-absent: **13**
- 검산: 7 + 10 + 13 = **30** ✅ (정확 일치 · fudge 문구 없음)
- N₃ 예시: `(Drei Geltungsansprüche)`, `(conscience éclairée)`, `(être-pour-soi)`, `(éducation morale)`, `(autonomie de la volonté)`, `(Sygdommen til Døden)`, `(Verständlichkeit)` 등 — 모두 하버마스 독어·뒤르켐/사르트르 불어·키르케고르 덴마크어 원어 표기로 coverage에 등장하지 않는 본 가이드 학술 확장분.

### Step 2: TitleCase phrases (`[A-Z][a-z]+( [A-Za-z][a-z]+){1,5}`)

- 실측 `sort -u | wc -l` = **31**
- 분류 (disjoint):
  - N₁ 면제 식별자: **0**
  - N₂ coverage-textual: **18**
  - N₃ coverage-absent: **13**
- 검산: 0 + 18 + 13 = **31** ✅ (정확 일치 · fudge 문구 없음)
- N₃ 전체 (coverage-absent 13개): `Daode jing`, `Drei Geltungsanspr`, `Enkelte coram Deo`, `Essentials of Sage Learning`, `Intuitions come first`, `Kohlbergian approach`, `Le jugement moral chez`, `Social Cognitive Domain Theory`, `Social Intuitionist Model`, `Subjectivity is truth`, `Ten Diagrams on Sage Learning`, `The utilitarian doctrine is not`, `Western Educated Industrialized Rich Democratic`. 모두 원전·학술 영문 병기 용어.

### 3단계 통합 요약

| Step | pattern | 총 unique | N₁ 면제 | N₂ textual | N₃ absent | 검산 (N₁+N₂+N₃) | fudge 문구 |
|------|---------|-----------|---------|-----------|-----------|-----------------|------------|
| 1 | bare-paren English | 243 | 60 | 112 | 71 | **243** = 243 ✅ | 없음 |
| 1b | Greek/Cyrillic/Latin-extended | 30 | 7 | 10 | 13 | **30** = 30 ✅ | 없음 |
| 2 | TitleCase phrases | 31 | 0 | 18 | 13 | **31** = 31 ✅ | 없음 |

**모든 3단계에서 N₁+N₂+N₃ 합계가 `sort -u | wc -l` 실측치와 정확 일치. fudge 문구("≈", "수렴", "중복 보정", "대략" 등) 없음.**

## em-dash U+2014 hexdump 샘플

파일 전체 em-dash 바이트 시퀀스 (e2 80 94) 총 **461회** 출현 · em-dash 포함 라인 **262개**. 처음 3개 offset의 16바이트 콘텍스트:

```
offset 53   : ea b3 b5 20 42 20 [e2 80 94] 20 ed 95 99 ec 83
  → "공 B — 학" (L1 "... 도덕·윤리 전공 B — 학생용 풀이 가이드")

offset 658  : a6 ac ec a6 88 20 [e2 80 94] 20 32 30 32 31 2d
  → "시리즈 — 2021-" (L8 시리즈 라벨)

offset 1520 : 28 33 eb aa 85 20 [e2 80 94] 20 42 4c 4f 43 4b
  → "(3명 — BLOCK" (L20 BLOCKER 카운트 주석)
```

UTF-8 em-dash (e2 80 94) 바이트 시퀀스 확증. ASCII hyphen(0x2d)이나 en-dash(e2 80 93) 오사용 0건.

## 제시문 verbatim 보존 확증

- 원문 `/home/jai/잡동사니/임용/md/2021_중등1차_도덕윤리_전공B.md` L14-L155 범위의 11문항 제시문을 각 문항 `### 제시문 (verbatim)` 섹션에 blockquote(`>`) 형태로 보존.
- HTML `<u>...</u>` 밑줄 태그 원문 9쌍 보존:
  - Q1: `<u>㉠</u>`·`<u>㉡</u>` (L16/L18)
  - Q3: `<u>㉠</u>`·`<u>㉡</u>` (L35/L37)
  - Q4: `<u>ⓐ</u>`·`<u>ⓑ</u>` (L50/L52)
  - Q5: `<u>ⓐ</u>`·`<u>ⓑ</u>` (L64/L66)
  - Q6: `<u>㉠</u>`·`<u>㉡</u>` (L78/L80)
  - Q7: `<u>㉠</u>`·`<u>㉡</u>` (L92/L94)
  - Q8: `<u>㉠</u>`·`<u>㉡</u>`·`<u>㉢</u>` (L106/L108/L110)
  - Q9: `<u>㉠</u>`·`<u>㉡</u>` (L120/L122)
  - Q10: `<u>㉢ 이 국가 체제</u>` (L137)
  - Q11: `<u>㉡ 세 가지의 타당성 주장들</u>` (L149)
- 한자(漢字) 보존: `敎·禪·觀·因果·三寶·因是·天鈞·四端·七情·誠·敬·理·氣·발·所以·正理·私邪·朱子·十圖·形而上·形而下·知者·言者·祖師·聖人·敎宗·禪宗·善·惡·心·道·大` 등 원문 한자 그대로 보존 및 한글 병기.
- 원문 괄호 식별자(㉠㉡㉢ⓐⓑ · 甲·乙) 전원 보존.
- 원문에는 em-dash(U+2014) 없음 — 본 가이드의 em-dash 461건은 모두 본 가이드 메타·해설 부분(제시문 밖)에서 정답 해설용으로 사용.

## 구현 특징 및 주의점

1. **교과교육학 면제 식별자 문항 0건**: 본 시험은 11문항 전원이 사상가형. 따라서 "해당 없음 (교육과정·외부 문헌)" 타입 문항 없음 — 모든 문항에 ES 근거 또는 ⚠️BLOCKER 표기.
2. **mill_js claim prefix 주의**: thinker_id=`mill_js`이지만 claim prefix는 `mill-claim-*` (mill-claim-001~017, 17건). Q9 본문 L896에 주의 표기 "※ thinker_id=mill_js, claim prefix=mill-claim-*".
3. **trademark 3중 일치**: 각 사상가별로 원전·핵심 개념·claim_id 3중 일치 검증. 특히 BLOCKER 3건은 ES claim 부재를 원전 직접 인용으로 보완.
4. **라틴어·그리스어·불어·독어·덴마크어 원어 병기**: Cicero(라틴어), Aristotle(그리스어), Durkheim·Sartre(불어), Habermas(독어), Kierkegaard(덴마크어) 모두 원어 용어 병기로 학술적 정확도 확보.
5. **채점 기준 표준화**: 서술형 Q3-Q11 (9건) 모두 배점 분할(㉠/㉡/갑/을) + 감점 포인트 + 키워드 포함 최소치 명시.
6. **풀이 과정 표준 구조**: 모든 11문항이 ① 문항 유형 식별 → ② 사상가 확정(trademark n중 근거) → ③ 용어 특정 → ④ 답안 작성(배점 합산) 4단계 형식 준수.

## 완료 조건 대비 체크리스트

| 조건 | 상태 |
|------|------|
| 1. 11문항 전건 작성(기입형 Q1·Q2 + 서술형 Q3~Q11) | PASS |
| 2. 각 문항 7섹션(발문·제시문 verbatim·정답·ES 근거·채점 기준(서술형만)·풀이 과정) | PASS |
| 3. 헤더 metadata `원문 line L{m}-L{n}` 스펙 일치 | PASS (11/11) |
| 4. 제시문 verbatim (HTML `<u>`·한자·원문 괄호 기호 보존) | PASS |
| 5. 16명 unique 사상가 ES 근거 (정상 12 + DQ-015 override 4) | PASS (curl 실측 확증) |
| 6. BLOCKER 3건 ⚠️ 표기 (uicheon/kierkegaard/cicero) | PASS |
| 7. DQ-015 override 4건 (jinul/turiel/durkheim/hoffman) 정상 ES 사용 | PASS |
| 8. em-dash U+2014 사용 확증 (e2 80 94 hexdump) | PASS (461회) |
| 9. 자기검증 3단계 결과 표 · 3분류 `sort -u | wc -l` 정확 일치 · fudge 문구 금지 | PASS (243=60+112+71 · 30=7+10+13 · 31=0+18+13) |
| 10. 라인 캡 ≤1100 | PASS (1074) |
| 11. coder-report-TASK-197.md 생성 | PASS (본 파일) |

## 참고 파일

- 원문: `/home/jai/잡동사니/임용/md/2021_중등1차_도덕윤리_전공B.md` (157 lines · 11문항 · 18357 bytes)
- coverage 사전 분석: `projects/ethics-study/exam-solutions/coverage/2021-B.md` (137 lines · 121770 bytes)
- DQ-015 로그: `signal/ethics-study/data-quality-log.md` L77-L109
- 선행 참조: `projects/ethics-study/exam-solutions/study-guide/2021-A.md` (1007 lines · 12문항)
- 가이드 산출물: `projects/ethics-study/exam-solutions/study-guide/2021-B.md` (**1074 lines · 11문항 · 40점**)
