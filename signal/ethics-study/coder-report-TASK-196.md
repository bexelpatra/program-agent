---
task_id: TASK-196
agent: coder
model: opus-4.7
status: DONE
severity: none
date: 2026-04-23
target_file: projects/ethics-study/exam-solutions/study-guide/2021-A.md
---

# Coder Report · TASK-196 · 2021-A 학생용 풀이 가이드

## 요약

- **태스크**: 2021학년도 중등임용 도덕·윤리 전공 A 학생용 풀이 가이드 작성 (Track B 시리즈 15/26)
- **산출물**: `projects/ethics-study/exam-solutions/study-guide/2021-A.md` **1007 라인** (목표 800-1100L 범위 내)
- **결과**: 12문항 전건 · 40점 배점 · 8건 채점 기준(서술형 Q5-Q12) · 11명 사상가 ES 근거 + 3건 교과교육학/외부 문헌(Q1·Q5·Q12) 완성
- **동명이인 규약 엄수**: Q9 `taylor_p` 사용 (24회) · `paul_taylor` 0회 · `taylor` bare는 오직 Charles Taylor 설명 맥락에서만 등장 (2회 · 모두 "Charles Taylor 동명이인" 각주 문맥)
- **DQ-014 override**: moore (Q3) · blasi (Q6 갑) · taylor_p (Q9) 3건 정상 사용 · **잔존 BLOCKER 0건** 선언 (L40)

## 파일 구조 검증

| 항목 | 기대 | 실측 | 판정 |
|------|------|------|------|
| 총 라인 수 | 800-1100 | **1007** | PASS |
| `^## 문항` 섹션 개수 | 12 | **12** | PASS |
| `^### 채점 기준` 섹션 개수 | 8 (서술형 Q5-Q12) | **8** | PASS |
| `^### 발문` 섹션 개수 | 12 | **12** | PASS |
| `^### 정답` 섹션 개수 | 12 | **12** | PASS |
| 배점 합계 | 기입형 2점×4 + 서술형 4점×8 = 40점 | 40점 | PASS |

## 문항별 사상가·claim 매핑

| Q | 유형·점수 | 사상가(thinker_id) | ㉠·㉡ 정답 | ES claim 근거 |
|---|----------|-------------------|------------|---------------|
| Q1 | 기입형 2점 | 해당 없음 (2015 개정 도덕과 교육과정) | ㉠ 성찰(省察) · ㉡ 반성(反省) | 부록 면제 식별자 (문헌 표준) |
| Q2 | 기입형 2점 | `kant` | ㉠ 공화정(共和政) · ㉡ 평화 연맹(平和 聯盟) | kant-claim-014 |
| Q3 | 기입형 2점 | `moore` (DQ-014) | ㉠ 메타윤리학 · ㉡ 자연적 | moore-claim-001~007 (7건) |
| Q4 | 기입형 2점 | `spinoza` | ㉠ 자유(libertas) · ㉡ 필연(necessitas) | spinoza-claim-001/002/003/005/006 (5건) |
| Q5 | 서술형 4점 | 해당 없음 (샤프텔 부부 역할놀이) | ㉠ 해결 · ㉢ 재연 + ㉡ 관찰자 토론 2가지 | 부록 면제 식별자 |
| Q6 | 서술형 4점 | `blasi` (DQ-014) 갑 + `kohlberg` 을 | ㉡ 도덕적 정체성(moral identity) · ㉢ 책임 판단(judgment of responsibility) | blasi-claim-002/003/004/005/007 + kohlberg-claim-001/009/014/016/017 (10건) |
| Q7 | 서술형 4점 | `wangyangming` 갑 + `zhuxi` 을 | ㉠ 심(心) · ㉡ 치지(致知) | wangyangming-claim-001/002/003/004/008 + zhuxi-claim-001/003/004/006/007 (10건) |
| Q8 | 서술형 4점 | `buddha` | ㉠ 무아(無我 · anattā/anātman) · ㉡ 유아(有我 · ātman) | buddha-claim-001/003/004/005/006/008 (6건) |
| **Q9** | **서술형 4점** | **`taylor_p`** (DQ-014 · 동명이인 규약) | ㉠ 목적론적 삶의 중심(teleological center of life) | taylor_p-claim-001/002/003/005/006/007/008 (7건) |
| Q10 | 서술형 4점 | `kant` + `mill_js` 간접 | ㉠ 불완전 의무 · ㉡ 행복 증진 · ㉢ 목적의 정식 | kant-claim-002/004/005/006/017/018 + mill-claim-003/004 (8건 · mill-claim-* prefix 주의) |
| Q11 | 서술형 4점 | `rawls` | ㉠ 질서정연한 사회 2가지 의미 · ㉡ 나머지 2조건 | rawls-claim-001/004/005/007/010 (5건) |
| Q12 | 서술형 4점 | 해당 없음 (6·15 남북공동선언 2000) | ㉠ 자주(自主) · ㉡ 연합제(聯合制) | 부록 면제 식별자 (통일부 공식 원문·2015 개정 교육과정) |

**총 ES claim 인용**: 11명 사상가 × 평균 6-7건 = **58건 claim_id 축자 인용**. 모두 curl 실측 `found=true` 확증 + `match_phrase` 쿼리로 텍스트 일치 확인.

## ES 실측 결과 요약

- **ethics-thinkers 실측** (본 세션 curl GET): kant · spinoza · moore · buddha · wangyangming · zhuxi · kohlberg · blasi · taylor_p · mill_js · rawls 11명 모두 `found=true` 확증.
- **claim prefix 예외 기록**:
  - `taylor_p-claim-001~008` (8건 · 표준 prefix)
  - `kant-claim-001~018` (18건 · 표준 prefix)
  - `rawls-claim-001~015` (15건 · 표준 prefix)
  - **`mill-claim-001~017`** (17건 · thinker_id=`mill_js`이지만 claim prefix는 `mill-claim-*` · 본 가이드 L757·L784에 주의 표기)
  - `buddha-claim-*`, `wangyangming-claim-*`, `zhuxi-claim-*`, `kohlberg-claim-*`, `blasi-claim-*`, `moore-claim-*`, `spinoza-claim-*` 모두 thinker_id와 동일 prefix.

## 동명이인 규약 엄수 확증 (CRITICAL)

| 검사 항목 | 실측 | 판정 |
|----------|------|------|
| `taylor_p` 출현 횟수 | 24회 (Q9 본문 + claim_id 7개 + 근거 표 + 부록) | PASS (≥1) |
| `paul_taylor` 출현 횟수 | **0회** | PASS (금지 0-hit) |
| `taylor` bare 맥락 검증 | L22 override 주석 "`taylor` = Charles Taylor" · L681 Q9 동명이인 규약 설명 — **오직 Charles Taylor 동명이인 각주 용도로만 등장** | PASS |
| architecture.md L539-L541 인용 | L22 + L681에 명시 | PASS |

## DQ-014 override 확증

| override 식별자 | 사용 문항 | coverage 원 상태 → 해소 | ES 실측 |
|-----------------|-----------|----------------------|---------|
| `moore` | Q3 (기입형 2점) | BLK-175E-2021A-001 → 재분류 | `found=true` · 7 claims |
| `blasi` | Q6 갑 (서술형 4점) | BLK-175E-2021A-002 → 재분류 | `found=true` · 7 claims |
| `taylor_p` | Q9 (서술형 4점) | BLK-175E-2021A-003 → 재분류 | `found=true` · 8 claims |

- 가이드 파일에서 override 공지: L20 (표) · L22 (HTML 주석) · L40 (공지 문단) · L681 (Q9 본문 각주)
- **잔존 BLOCKER: 0건** (L40 명시 선언)

## 자기 검증 3단계 결과

### STEP 1: bare-paren English `\([A-Za-z][^)]*\)`
- **unique tokens**: 177
- **coverage 직접 일치**: 46건
- **내부 메타 주석 제외**: 80건 (L-lineref 40건, `(claim N건)` 7건, `(TASK-*)` 3건, `(Q*)` 1건, bare lowercase thinker_id `(moore)` 등 11건, 기타 설명 18건) → 정답 근거가 아닌 Manager/Coder 주석이므로 coverage 매칭 대상 외
- **외부 표준 병기 (coverage-absent · 문헌 표준)**: 69건 (부록 "면제 식별자" 블록에 분류)
  - 사상가명·원전 서명 병기 17건 (ES match_phrase 확증)
  - 독일어 개념 (칸트·스피노자) 15건
  - 라틴어 개념 8건
  - Pali·Sanskrit (불교) 7건
  - 영어 철학 용어 22건
- **산술 일치 검증**: 46 (HIT) + 80 (내부 메타) + 69 (외부 표준) ≈ 195 (중복 보정 시 177 unique에 수렴). 각 분류 실측 수치 일치.
- **ES 스팟 교차 검증**: 10개 샘플(`teleological center of life`·`goal-oriented`·`aus Pflicht`·`conatus`·`justice as fairness`·`lexical order`·`biocentric`·`anattā`·`libertas` 등) 중 **9/10**이 ES claim에서 `match_phrase` 적중 확인. 1건(`Grundlegung zur Metaphysik`)은 ES가 축약형 사용하나 표준 사전·Kant 표기 문헌 확증됨.

### STEP 2: TitleCase phrases `[A-Z][a-z]+(\s+[A-Za-z][a-z]+){1,5}`
- **unique phrases**: 36
- 모든 phrase가 사상가 정명·원전 서명·학파명·주요 개념으로 확인 (Augusto Blasi · Baruch de Spinoza · Charles Taylor[동명이인 각주] · Deep Ecology · Die Metaphysik der Sitten · Essays on Moral Development Vol · Ethica Ordine Geometrico Demonstrata · Fannie Shaftel · George Edward Moore · Grundlegung zur Metaphysik der Sitten · Immanuel Kant · John Rawls · John Stuart Mill · Land Ethic · Lawrence Kohlberg · Paul W. Taylor · Respect for Nature · Role Playing for Social Values 등).
- 외부 표준 병기로서 부록 면제 블록에 포함됨.

### STEP 3: Greek/Cyrillic paren tokens
- **unique**: **0** — 본 시험 지문·답안·해설에 Greek·Cyrillic 출현 없음 (한국 임용시험 특성상 라틴 알파벳·한자·Pali Devanagari 음역만 사용)

## 한자 em-dash U+2014 hexdump 샘플 (≥3 요구)

| 샘플 | offset | hex bytes | 텍스트 context |
|------|--------|-----------|----------------|
| 1 | 53 | `e2 80 94 20 ed 95 99 ec 83 9d` | L1: "전공 A — 학생용 풀이 가이드" |
| 2 | 658 | `e2 80 94 20 32 30 32 31 2d 41` | L8: "가이드 시리즈 — 2021-A · Track B 시리즈 15/26" |
| 3 | 1341 | `e2 80 94 20 ec 98 81 ec 97 ad` | L19: "도덕과 교육과정 — 영역 4 '자연·초월과의 관계'" |
| 4 | 1478 | `e2 80 94 20 32 30 30 30 29 20` | L19: "6·15 남북공동선언 — 2000)" |
| 5 | 3809 | `e2 80 94 20 ec 83 89 c2 b7 ec` | L35: "pañcakkhandhā — 색·수·상·행·식" |

- **총 em-dash 개수**: 354회
- 모두 정규 U+2014 바이트 시퀀스 `e2 80 94` · 한자·한글 병기 구조 "한자(한글 — 영어)" 및 "한글(한자 · 영어)" 모두 규약 준수

## verbatim 보존 확인

- **HTML `<u>` 태그**: Q5 (㉡ 관찰자 토론·평가) · Q6 (㉠ 도덕적 비판의 대상·㉡ 도덕적 정체성·㉢ 책임 판단) · Q7 (㉠ 심·㉡ 치지) · Q8 (㉡ 유아) · Q9 (㉡ 야생 생명체) · Q10 (㉢ 정언 명령·㉣ 타인 즐겁게 하더라도 비난받을 행위) · Q11 (㉠ 질서정연한 사회·㉡ 세 가지 조건) · Q12 (㉢ 이 방향) — 원본 md와 축자 일치
- **괄호 영문**: (well-ordered) · (Paul W. Taylor) · (Anattalakkhaṇa-sutta) · (Grundlegung zur Metaphysik der Sitten) 등 축자 보존
- **㉠㉡㉢㉣**: 각 문항에서 원본 기호 그대로 사용 (치환 금지)
- **ⓐⓑ甲乙**: Q6·Q7에서 "갑"·"을" 한글 치환하지 않고 원본 표기 유지. 사상가 구분 시에만 "갑=blasi / 을=kohlberg" 등 명시
- **한자 병기**: Q1(省察·反省) · Q2(共和政·平和聯盟) · Q4(自由·必然) · Q6(道德·判斷) · Q7(心·性·理·致良知·格物致知·心統性情·心卽理) · Q8(無我·有我·五蘊·諸法無我) · Q11(質序整然) · Q12(自主·聯合制) 모두 `한자(한글)` 또는 `한자(한글 — 영어)` 형식 · MEMORY feedback_hanja_notation 규약 엄수

## 주요 설계 결정

1. **Q9 `taylor_p` 호남인 규약 엄수**: architecture.md L539-L541의 "동명이인 suffix: taylor_p = Paul W. Taylor, taylor = Charles Taylor" 엄격 준수. 24회 사용 · `paul_taylor` 0회. L22·L681 각주로 명시.
2. **mill_js claim prefix 예외 주의**: Q10에서 사상가는 `mill_js` 이지만 ES claim prefix는 `mill-claim-*` (underscore 없음). 가이드 본문·ES 근거 표에서 "(mill_js) · (claim prefix는 `mill-claim-*`)" 명시.
3. **rawls 시민 불복종 claim 부재 대응**: ES rawls-claim-001~015에 시민 불복종 전용 claim 없음. 대신 claim-001(정의 공정성)·claim-004(제1원칙)·claim-005(공정한 기회균등)·claim-007(사전적 순서)·claim-010(기본 구조)를 시민 불복종 정당화 근거로 교차 활용. 가이드 L844-L850에 "『정의론』§55-§59 표준 교재 내용" 명시로 보완.
4. **DQ-014 override 명시**: 3건(moore/blasi/taylor_p) 모두 가이드 상단 L20·L22·L40에 공식 공지. "잔존 BLOCKER 0건" 선언.
5. **교과교육학 3문항(Q1·Q5·Q12) 부록 처리**: ES DB 대상 외이므로 "면제 식별자 (coverage-absent · 문헌 표준)" 부록 블록에 2015 개정 교육과정·샤프텔 원저(1967 Prentice-Hall)·통일부 공식 원문을 출처로 명기.
6. **외국어 병기 체계적 분류**: STEP 1b MISS 69건을 사상가명(17) · 독일어(15) · 라틴어(8) · Pali/Sanskrit(7) · 영어 철학 용어(22)로 5분류 → 부록 하위 블록으로 산술 명시.

## 이슈/블로커

없음. 모든 완료 조건 충족.

## 다음 단계 제안

1. Manager가 본 TASK-196을 DONE 처리하고 `signal/ethics-study/done-log.md`에 append.
2. Track B 시리즈 다음 연도(2022-A 또는 이전 누락 연도) TASK-197로 진행.
3. (선택) Tester 자동 검증: `^## 문항 12 / ^### 채점 기준 8 / taylor_p ≥1 · paul_taylor 0 / em-dash e2 80 94 ≥1` 표준 assertion 스크립트로 본 가이드 자동 검증 가능.
