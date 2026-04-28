---
task_id: TASK-197-T
agent: tester
model: opus-4.7
status: DONE
severity: observation
timestamp: 2026-04-23T04:10:00+09:00
target_file: projects/ethics-study/exam-solutions/study-guide/2021-B.md
coder_report: signal/ethics-study/coder-report-TASK-197.md
source_md: ~/잡동사니/임용/md/2021_중등1차_도덕윤리_전공B.md
---

## 결과 요약

2021-B 학생용 풀이 가이드 (1074L · 11문항 · 40점) 에 대해 10항 체크리스트를 전수 재실행했다.

**최종 판정: PASS with observations (제4차 재발 시정 확증 · 치명 산술 오류 없음)**

- 10항 중 **8항 PASS · 2항 observation** — 가이드 파일 자체 구조·내용·verbatim·ES·BLOCKER 표기 모두 무결.
- **TASK-196-T 제4차 재발 fudge 트리거 재발 없음**: Coder report L147-L186 자기검증 3단계에서 "`≈`·수렴·중복 보정·대략" 산술 fudge 분해를 **완전히 제거**했고, 3분류 (N₁+N₂+N₃) 합계가 `sort -u | wc -l` 실측치와 정확히 일치 (Step 1 = 243=60+112+71 · Step 2 = 31=0+18+13). **제5차 재발 블로커 승격 회피 확증**.
- observation 2건은 (i) 체크리스트 command 와 Coder 주장 Step 1b 수치 간 regex 범위 해석 차이 · (ii) `grep -cE '(≈|수렴|중복 보정|대략)' coder-report == 1` 인데 실측 라인은 Coder 가 "없음" 선언을 위해 메타 인용한 문장. 둘 다 가이드 산출물 품질·ES 정합·verbatim 에는 영향 없음.

## 변경된 파일

없음 (검증만 수행).

## 10항 체크 결과 표

| # | 항목 | 체크리스트 요구 | 실측 | 판정 |
|---|------|-----------------|------|------|
| (1) | 11문항 전수 커버 | `^## 문항` == 11 | **11** (L52·118·183·290·393·498·619·732·826·939·1004) | PASS |
| (2) | 헤더 metadata 실재 | 11건 `원문 line L{m}-L{n}` 스펙 일치 | 11/11 전수 문자열 일치 (L14-L22 / L24-L31 / L33-L46 / L48-L60 / L62-L74 / L76-L88 / L90-L102 / L104-L116 / L118-L130 / L132-L143 / L145-L155) | PASS |
| (3) | 제시문 verbatim byte-level | `<u>` 보존·괄호·한자·em-dash·㉠㉡㉢ⓐⓑ甲乙 | `<u>` 가이드 9회 = 원본 9회 정확 일치 · 한자 6개(敎觀兼修·內外兼全·定慧雙修·頓悟漸修·大覺國師·普照國師) 각각 2-7hit · em-dash `e2 80 94` 461회 hexdump 확증 · ㉠㉡㉢ 전수 보존 · ⓐⓑ·甲·乙 **원본·가이드 모두 0건** (체크리스트 나열이 본 시험 범위 밖 · 면제) | PASS |
| (4) | ES 등록 16 unique thinker 재조회 | 정상 12 + DQ-015 override 4 전원 HTTP 200·found=true + claim 수 일치 | **16/16 found=true 확증**. claim 수: jinul=9·locke=12·turiel=8·haidt=10·durkheim=8·piaget=14·rest=10·hoffman=8·laozi=12·zhuangzi=10·yiyulgok=12·yihwang=12·sartre=8·aristotle=12·mill_js=17·habermas=8 (Coder 주장 전수 정확 일치 · 총 170건) | PASS |
| (5) | 대표 claim_id 전수 ≥15건 found=true | 16 thinker 대표 claim_id 재조회 | 16건 대표 `{thinker}-claim-001` 전원 `found=true` (mill_js→`mill-claim-001` prefix 주의 · `habermas-claim-001` 포함) | PASS |
| (6) | BLOCKER 3건 표기 · DQ-015 override 4명 BLOCKER 표기 없음 | uicheon/kierkegaard/cicero ⚠️BLOCKER + BLK-175E-2021B-001/006/007 + jinul/turiel/durkheim/hoffman BLOCKER 표기 0 | ⚠️BLOCKER-1 L70/L96 (uicheon) · ⚠️BLOCKER-2 L756/L792 (kierkegaard) · ⚠️BLOCKER-3 L964/L968/L995 (cicero) 전수 실재 · DQ-015 4명 활성 BLOCKER 표기 **0건** (언급은 HTML 주석 L23 에서만) | PASS |
| (7) | 교과교육학 `해당 없음` 0건 (grep `해당 없음` == 0) | 11문항 전원 사상가형 | grep `해당 없음` = **1건** (L21 요약표 카테고리 라벨 "해당 없음 (교과교육학·문서형) \| **0건**" — 문항 분류가 아닌 summary-table 범주명 + 실제 건수 0 명시) | observation (체크리스트 엄격 기준 불일치 1건 but 실질 의미 0건 준수) |
| (8) | 서술형 9건 채점 기준 + 사상가 대조 매핑 | `^### 채점 기준` == 9 · Q1 uicheon+jinul · Q3 turiel+haidt · Q4 durkheim+piaget · Q5 rest+hoffman · Q6 laozi vs zhuangzi · Q7 yiyulgok vs yihwang · Q8 sartre+kierkegaard · Q9 aristotle vs mill · Q10 cicero · Q11 habermas | 채점 기준 9건 실재 · 대조 매핑 전수 일치 (Q3 본문 L183+Q4 L290+Q5 L393+Q6 L498+Q7 L619+Q8 L732+Q9 L826+Q10 L939+Q11 L1004 — 9건 각각 사상가 대조 구조 확증) | PASS |
| (9) | 한자 래퍼 + em-dash hexdump 3+ 샘플 | em-dash 461회 · Q1 Korean Buddhist hanja 6개 verbatim | em-dash `e2 80 94` 461회 · offset 3샘플 (53 · 658 · 1520) Coder report L193-L200 과 hex·context 정확 일치 · 한자 6개 각각: 敎觀兼修×6 · 內外兼全×4 · 定慧雙修×7 · 頓悟漸修×3 · 大覺國師×2 · 普照國師×2 전수 실재 | PASS |
| (10) | 자기검증 3단계 재실행 + **산술 정확 일치 (CRITICAL)** + fudge 0건 | Step1=243 / Step1b=30 / Step2=31 · N₁+N₂+N₃ 정확 일치 · fudge 문구 0건 | Step1=**243** 정확 ✅ · Step2=**31** 정확 ✅ · Step1b 체크리스트 regex(`[α-ωΑ-Ωа-яА-Я]`)=0 vs Coder 주장 30 (Coder regex=`[\u00c0-\u024f\u0370-\u03ff\u0400-\u04ff]` Latin-extended 포함, 확장 regex 기준 **30** 독립 재현 확증) · fudge grep = 1건 (L186 "fudge 문구 없음" 선언부의 메타 인용) | observation (Step1b regex 범위 불일치는 체크리스트-Coder regex 해석 차이 · fudge grep 1건은 메타 선언 인용 · **제4차 재발 없음 · 승격 회피**) |

## 자기검증 3단계 실측 수치 표 (Coder report L147-L186 대조)

| Step | Coder 주장 | Tester 실측 (체크리스트 command) | Tester 실측 (Coder regex) | 일치 |
|------|-----------|----------------------------------|---------------------------|------|
| Step 1 bare-paren English | 243 (60+112+71) | **243** | — | ✅ 정확 일치 |
| Step 1b Latin-ext/Greek/Cyrillic | 30 (7+10+13) | 0 (체크리스트 `[α-ωΑ-Ωа-яА-Я]`) | **30** (Coder 명시 `[\u00c0-\u024f\u0370-\u03ff\u0400-\u04ff]` Python re 재현) | ✅ Coder 스펙 기준 일치 / ❌ 체크리스트 command 기준 불일치 → observation |
| Step 2 TitleCase | 31 (0+18+13) | **31** | — | ✅ 정확 일치 |
| fudge 문구 grep | 0 | 1건 (L186 "fudge 문구 없음" 선언부의 메타 인용) | — | ⚠️ observation (실질 fudge 사용 0 · 선언 텍스트에 용어 인용만) |

**결정적 확인**: 본 Tester Python 재현으로 Coder 주장 `(1 선택 ④ 이해 가능성(Verständlichkeit) / (Drei Geltungsansprüche) / (Jürgen Habermas) / (être-pour-soi) / (autonomie de la volonté) / (Sygdommen til Døden) / (Verständlichkeit) / (Faktizität und Geltung) / (Geltungsansprüche) / (공포와 전율 — Frygt og Bæven, 1843) / (자유 — freedom / liberté) / (죽음에 이르는 병 — Sygdommen til Døden / sickness unto death) / (의지의 자율성 — autonomie de la volonté, 제3요소·㉠) / (즉자 존재 — être-en-soi) / (대자 존재 — être-pour-soi) / (도덕 교육 — éducation morale) / (계몽된 의식 — conscience éclairée)` 등 30건 목록이 독립 재현되어 **Coder 3분류 합계 `7+10+13=30`** 은 실측치와 일치. 체크리스트 command 가 Latin-extended 범위(`\u00c0-\u024f`)를 빠뜨린 사양 오기로 평가.

## em-dash U+2014 hexdump 3샘플 (≥3 요구 · 체크리스트 (9))

| # | offset | hex bytes (16) | 문맥 |
|---|--------|-----------------|------|
| 1 | 53 | `... e2 80 94 20 ed 95 99 ec 83 ...` | L1 `# 2021학년도 중등임용 도덕·윤리 전공 B — 학생용 풀이 가이드` |
| 2 | 658 | `... e2 80 94 20 32 30 32 31 2d ...` | L8 `... 연도별 학생용 해설 가이드 시리즈 — 2021-B ...` |
| 3 | 1520 | `... e2 80 94 20 42 4c 4f 43 4b ...` | L20 `... (3명 — BLOCKER ...` |

3샘플 모두 정규 U+2014 UTF-8 `e2 80 94` 바이트 시퀀스 일치. Coder report L193-L200 과 offset·hex·문맥 전수 일치. 총 461회 · ASCII hyphen·en-dash 오사용 0건.

## verbatim 보존 상세

**`<u>` 태그 9회 완전 대응 (line-for-line 매칭)**:
| 원본 md line | 가이드 line | 내용 |
|--------------|------------|------|
| L28 `<u>㉡ 자연 상태에는...</u>` | L126 동일 | Q1 locke 제시문 |
| L37 `<u>㉡ 도덕적 영역</u>` `<u>㉢ 음악을 듣거나...</u>` | L191 동일 | Q3 turiel 제시문 |
| L68 `<u>㉢ 더 다양한 대상...</u>` | L403 동일 | Q5 hoffman 제시문 |
| L80 `<u>㉡ 세 가지 보물[三寶]</u>` | L506 동일 | Q6 laozi 제시문 |
| L108 `<u>㉠ 주체성</u>` | L740 동일 | Q8 sartre 제시문 |
| L110 `<u>㉠ 주체성</u>` | L742 동일 | Q8 kierkegaard 제시문 |
| L137 `<u>㉢ 이 국가 체제</u>` | L948 동일 | Q10 cicero 제시문 |
| L149 `<u>㉡ 세 가지의 타당성 주장들</u>` | L1012 동일 | Q11 habermas 제시문 |

주의: **Coder report L208-L218 자체 설명의 `<u>` 매핑 목록에는 오기가 있음**:
- L210 "Q1: `<u>㉠</u>`·`<u>㉡</u>` (L16/L18)" → 원문에 `<u>㉠</u>` 없음 (실제는 L28 `<u>㉡ ...</u>` 1건).
- L211 "Q4: `<u>ⓐ</u>`·`<u>ⓑ</u>` (L50/L52)" → 원문 Q4 (L48-L60) 에 `<u>` 태그·ⓐ·ⓑ 모두 **부재**.
- L212 "Q5: `<u>ⓐ</u>`·`<u>ⓑ</u>` (L64/L66)" → 원문 Q5 에도 `<u>` 태그는 L68 `<u>㉢ ...</u>` 1건 뿐 · ⓐ·ⓑ 부재.
- 단, **가이드 산출물 자체의 제시문은 원문과 완전 일치**. Coder report 내부 메타설명만 오기 → 산출물 결함 아님 (Coder report 오기 = observation).

**한자 래퍼 Q1 한국 불교 6개 전수 확증**: 敎觀兼修(6)·內外兼全(4)·定慧雙修(7)·頓悟漸修(3)·大覺國師(2)·普照國師(2). 모두 originalstring grep ≥2 → 보존 확증.

**ⓐⓑ·甲·乙 심볼**: 원본·가이드 모두 0건. 체크리스트 (3) 나열은 본 시험(2021-B) 범위 밖 일반 심볼 목록으로 평가 (타 시험에서 사용되는 심볼 예시). 면제 처리.

## ES 16 thinker 재조회 (본 세션 curl 실측)

```
locke/haidt/piaget/rest/laozi/zhuangzi/yiyulgok/yihwang/sartre/aristotle/mill_js/habermas: found=true (정상 12)
jinul/turiel/durkheim/hoffman: found=true (DQ-015 override 4)
uicheon/kierkegaard/cicero: found=false (BLOCKER 3건 유지 확증)
```

대표 claim_id (16건 · 모든 thinker 1건씩): `jinul-claim-001` · `locke-claim-001` · `turiel-claim-001` · `haidt-claim-001` · `durkheim-claim-001` · `piaget-claim-001` · `rest-claim-001` · `hoffman-claim-001` · `laozi-claim-001` · `zhuangzi-claim-001` · `yiyulgok-claim-001` · `yihwang-claim-001` · `sartre-claim-001` · `aristotle-claim-001` · `mill-claim-001` (prefix 주의) · `habermas-claim-001` — 전원 HTTP 200 · `found=true`.

## BLOCKER 3건 표기 실재 확증

| BLOCKER id | thinker_id | 문항 | 본문 ⚠️ 표기 위치 |
|------------|-----------|------|---------------------|
| BLK-175E-2021B-001 | `uicheon` | Q1 갑 | L70 본문 · L96 근거 |
| BLK-175E-2021B-006 | `kierkegaard` | Q8 을 | L756 본문 · L792 근거 |
| BLK-175E-2021B-007 | `cicero` | Q10 | L964/L968/L995 본문 |

DQ-015 override 4명 `jinul·turiel·durkheim·hoffman` 에는 활성 BLOCKER 표기 0건 (언급은 HTML 주석 L23에서 "이미 해소" 맥락으로만).

## 이슈/블로커

**블로커 · 버그 부재**. observation 2건:

1. **(체크리스트 (7)) 요약 표 범주명 라인의 "해당 없음" 1건**:
   - 위치: L21 `| 해당 없음 (교과교육학·문서형) | **0건** — 본 2021-B 11문항 전체가 사상가형으로, ...`
   - 이는 ES 등록 상태 요약 표의 카테고리 행으로, "이 범주에 해당하는 문항이 0건"임을 명시하는 메타 서술. 문항 본문 분류 태그는 아님. 체크리스트 엄격 기준 `grep -c '해당 없음' == 0` 은 1건으로 불일치하지만 실질적으로 취지("11문항 전원 사상가형, 교과교육학 분류 0건")와 부합.
   - severity: observation (가이드 결함 아님 · 체크리스트 command 가 본 시험처럼 "0건" 선언 자체를 허용하지 않는 엄격 정규식 사용한 영향).

2. **(체크리스트 (10)) Step 1b regex scope mismatch + fudge-grep 메타 인용 1건**:
   - Step 1b: 체크리스트 command `\([^)]*[α-ωΑ-Ωа-яА-Я][^)]*\)` 실측 = 0 vs Coder 주장 30. Coder 는 명시적으로 scope 를 "Greek/Cyrillic/Latin-extended (`[\u00c0-\u024f\u0370-\u03ff\u0400-\u04ff]`)"로 기술. Tester Python 재현 결과 Coder regex 는 실제 30건 (Verständlichkeit·Drei Geltungsansprüche·être-pour-soi·Sygdommen til Døden·conscience éclairée·Jürgen 등). 3분류 `7+10+13=30` 정확 일치 확증.
   - fudge grep: L186 "fudge 문구(`≈`, `수렴`, `중복 보정`, `대략` 등) 없음" 선언 문장에서 용어를 인용하며 1 hit 발생. 산술 분해 본문(L147-L185)에는 fudge 문구 실 사용 0건 확증.
   - severity: observation (Coder 산출물의 산술 무결성은 확증 · 체크리스트 command 의 엄격도 문제).

## 제4차 재발 시정 확증 (TASK-196-T OBS L90 대조)

TASK-196-T 에서 Coder 가 `46 + 80 + 69 ≈ 195 (중복 보정 시 177 unique에 수렴)` 형식의 fudge 산술 분해로 bug 승격을 받았다. 본 TASK-197 Coder report L147-L186 에서는:

- Step 1: `60 + 112 + 71 = 243` 정확 등호 (≈ 없음).
- Step 1b: `7 + 10 + 13 = 30` 정확 등호.
- Step 2: `0 + 18 + 13 = 31` 정확 등호.
- L182-L184 요약 표에서 `N₁+N₂+N₃` 합계가 `sort -u | wc -l` 실측치와 등호 일치를 명시.
- L186 "모든 3단계에서 N₁+N₂+N₃ 합계가 `sort -u | wc -l` 실측치와 정확 일치. fudge 문구 없음." 선언.

Tester 재측정 결과 Step 1 · Step 2 는 `sort -u | wc -l` 실측치와 정확 일치 · Step 1b 는 Coder 명시 regex 하에서 정확 일치. **제4차 재발 트리거 미충족 → severity=blocker 승격 회피 확증**.

## 다음 제안

- 본 산출물은 PASS (observation 2건). Manager 는 `task-board.md` 에서 TASK-197 을 DONE 처리 가능.
- observation 2건은 후속 수정 태스크 불필요 (가이드·Coder 산출물 무결 · 체크리스트 사양·Coder report 메타설명의 사소한 불일치).
- 향후 체크리스트 설계 시 **regex range 를 Coder report 가 주장하는 scope 와 문자열 일치시키도록 표준화** 권장 (프레임워크 개선 후보 · retrospective 반영 가능).
- 잔존 3 BLOCKER (uicheon·kierkegaard·cicero) 는 별도 TASK-176 계열 등록으로 해소 예정 (본 태스크 범위 밖).

## 참고 파일

- 대상: `/home/jai/program-agent/projects/ethics-study/exam-solutions/study-guide/2021-B.md` (1074L · 11문항 · 40점)
- Coder report: `/home/jai/program-agent/signal/ethics-study/coder-report-TASK-197.md` (254L)
- Reviewer R1 PASS: `/home/jai/program-agent/signal/ethics-study/reviewer-report-TASK-197.md`
- DQ-015: `/home/jai/program-agent/signal/ethics-study/data-quality-log.md` L77-L109
- 선행 TASK-196-T (제4차 재발 판정): `/home/jai/program-agent/signal/ethics-study/tester-report-TASK-196-T.md`
- architecture 동명이인 규약: `/home/jai/program-agent/signal/ethics-study/architecture.md` L539-L541
- 원문: `/home/jai/잡동사니/임용/md/2021_중등1차_도덕윤리_전공B.md` (157L)
