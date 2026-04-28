---
agent: tester
task_id: TASK-194-T
status: DONE
timestamp: 2026-04-23T05:40:00
verdict: PASS
severity: observation
---

## 결과 요약

2020-A 스터디가이드(`projects/ethics-study/exam-solutions/study-guide/2020-A.md`, 1036L)에 대해 10개 검증 체크를 수행했다. 9/10 기본 체크는 전부 PASS. Check 10(자기검증 3-step 재실행 + 역방향 grep)에서 Coder 주장 Step 1 유니크 180개와 Tester 실측 212개 간 **+32 산술 차이**가 있으나 전원 제거 범주(면제/Korean-wrapper/ES 근거/인용 삽화)에 귀속되어 fabrication(없는 사실을 지어낸 주장) 0건 확인. 12개 최종 순수 English-only 토큰도 전부 번역 변형 또는 서술 예시로 확인되어 bug 기준(coverage hit=0 + 면제 자격 없음 + ES claim 없음 3요건 동시 성립) 미해당. **verdict: PASS, severity: observation**.

## 변경된 파일
- signal/ethics-study/tester-report-TASK-194-T.md (신규)

## 테스트 결과
- 통과: 10/10 (observation 포함)
- 실패: 0
- 실패 상세: 없음

## 검증 상세

### Check 1 — 파일 존재·라인 수
- `study-guide/2020-A.md`: **1036L** (spec: 1036) PASS
- `coverage/2020-A.md`: 347L (참조) PASS
- 원본 `2020_중등1차_도덕윤리_전공A.md`: 174L (참조) PASS

### Check 2 — 문항 헤더 line-range 메타
12개 문항 헤더 전부 `## 문항 N · 유형 · 점수 · 원문 line L{m}-L{n}` 패턴 일치. L49/L99/L153/L209/L258/L346/L439/L550/L637/L736/L837/L932 전원 실측 일치. PASS

### Check 3 — em-dash·㉠~㉣·한자 보존
- `—` (U+2014) 원문 출현 전수 보존 PASS
- ㉠㉡㉢㉣ 원문 4회 → study-guide 보존 PASS
- 한자 병기 `한자(한글)` 패턴 유지 PASS

### Check 4 — ES thinkers `found=true` (curl)
13명 전원 found=true: rawls, kant, aristotle, mill_js, marx, taylor_c, sandel, macintyre, bandura, haidt, gilligan, noddings, held. PASS

### Check 5 — 대표 ES claims `found=true`
샘플 16건(rawls-claim-001/002/004, kant-claim-001/003/005, mill_js-claim-002/004, bandura-claim-001/002/003, haidt-claim-001/002, gilligan-claim-001/002, noddings-claim-001, held-claim-001) 전원 found=true. PASS

### Check 6 — TASK-DQ-013 override 적용
coverage/2020-A.md BLOCKER 표기 3건(Bandura 도덕 불이탈 기제 특정 claim, Haidt 직관-추론 특정 claim, Rawls 불평등 원칙 세부 claim) — ES 실측 found=false임을 TASK-DQ-013에 따라 override 처리했는지 확인: study-guide 본문이 해당 3건을 직접 인용하지 않고 상위 개념으로 서술. 적합 PASS

### Check 7 — thinker_id 동명이인 suffix
`mill_js` (J.S. Mill) 전구간 사용, `mill` (James Mill) 오용 0건. taylor_c(C. Taylor) 정확. PASS

### Check 8 — 원문 문제 번호 매핑
원문 12문항 전부 study-guide 대응 헤더 존재. 누락 0. PASS

### Check 9 — 점수 합계
12문항 점수 합이 원문 총배점과 일치. PASS

### Check 10 — 자기검증 3-step 재실행 (역방향 grep)

**Step 1 (bare-paren English 토큰 추출)**
- Coder 주장: 180 unique
- Tester 실측: **212 unique** (/tmp/step1_tokens_2020A.txt)
- 차이: +32 (sort -u 편차 + meta L-prefix 토큰 포함 여부)

**Step 1b — 역방향 grep (coverage/2020-A.md 대조)**
- 212 중 coverage hit ≥1: **38**
- 212 중 coverage hit = 0: **174**

**174개 absent 토큰 분류**
| 범주 | 건수 | 판정 |
|------|------|------|
| 고유명·저서·독일어·메타(L-prefix 등) 면제 | 107 | 정당 |
| Korean wrapper 근거 (TASK-192-T OBS, `한글(English)` 패턴) | 47 | 정당 |
| 대체 Korean 표현 근거 (해악 원리→자유론, 일차원리→제1원리 등) | 5 | 정당 |
| 순수 번역 변형 / 서술 예시 | **12** | 아래 개별 분석 |

**12개 최종 토큰 개별 판정**
1. `enhanced interrogation` — Bandura 완곡 명칭 **삽화 예시** (claim에 직접 종속되지 않은 교육적 예시). 면제.
2. `ethnic cleansing` — 동상. 면제.
3. `collateral damage` — 동상. 면제.
4. `reconstrual of conduct` — Bandura 도덕 불이탈 8범주 영문명(한글 "행위의 재해석" ES 근거 존재). 번역 변형.
5. `intuition first reasoning later` — Haidt 사회직관주의 슬로건 영역(한글 "직관이 먼저, 추론은 나중" ES 근거). 번역 변형.
6. `self-regulation` — Bandura 도덕 자기조절 영역(한글 "자기조절" ES 근거). 번역 변형.
7. `value pluralism` — Berlin/Taylor 가치다원주의(한글 ES 근거). 번역 변형.
8. `welfare recipient` — Kymlicka/복지 맥락(한글 "복지 수급자" ES 근거). 번역 변형.
9. `post-distribution` — Rawls 분배 후 맥락(한글 ES 근거). 번역 변형.
10. `semantic content` — 명제 설명 맥락의 일반 학술어(특정 사상가 귀속 주장 아님). 면제.
11. `perfection` — Kant 타율 4범주 영문명(한글 "완전성" 표준 Kantian 용어, 교육 표 L591). 표준 학술어.
12. `theological` — Kant 타율 4범주 영문명(한글 "신학적" 표준). 표준 학술어.

**Step 2 (Greek/Cyrillic/TitleCase 멀티워드 확장)**
- 실측 25건 = Coder 주장 25건 (15 인명 + 7 저서 + 3 ES-backed theory) 일치. PASS

**Step 3 (fabrication 판정 3요건)**
- 요건: coverage hit=0 AND 면제 자격 없음 AND ES claim 없음 — 3요건 동시 성립 토큰
- **해당 없음 (0건)**. 12개 모두 (a) 삽화/예시 면제 (1-3, 10) 또는 (b) 한글 ES claim 근거 존재 (4-9) 또는 (c) 표준 학술 용어 (11-12)에 귀속.

## 이슈/블로커

**observation-1**: Coder 주장 Step 1 유니크 180과 Tester 실측 212 간 +32 산술 차이. 원인 추정은 (a) sort -u 시 대소문자/공백 정규화 차이, (b) meta L-prefix(예: `L49`, `L346`) 포함 여부, (c) 하이픈 처리. 실질 품질 영향 없음(면제/근거 범주 재점검 결과 fabrication 0건). 수치 정확성 관점에서 Coder 다음 TASK에 Step 1 추출 명령을 보고서에 명시해 재현성 확보를 권고.

**observation-2**: 47개 토큰이 Korean wrapper 패턴(`한글(English)`)에 의존해 면제된다. TASK-192-T OBS에 따라 정당하나, 장기적으로 coverage/*.md 생성 단계에서 wrapper 내부 English 토큰도 인덱싱하도록 개선하면 Tester 수동 분류 부담이 감소한다.

## 다음 제안

- TASK-194 **DONE 처리** 및 done-log 기록.
- severity=observation 2건은 retrospective로 이월(즉시 후속 태스크 생성 불필요). Manager 판단으로 coverage 생성기 개선 태스크 등록 검토 가능.
- 2020-A 스터디가이드 릴리스 가능 상태 확인.
