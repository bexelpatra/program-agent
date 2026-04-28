---
agent: tester
task_id: TASK-182
status: DONE
severity: none
timestamp: 2026-04-22
target_file: projects/ethics-study/exam-solutions/study-guide/2014-A.md
source_coverage: projects/ethics-study/exam-solutions/coverage/2014-A.md
source_exam: /home/jai/잡동사니/임용/md/2014중등1차-2교시-도덕윤리-전공A-문제지-최종.md
---

# TASK-182-T · 2014-A 학생용 study-guide 검증 · Tester Report

## 0. 파일·카운트 요약 (실측)

| 파일 | 라인 수 | 명령 |
|------|---------|------|
| `projects/ethics-study/exam-solutions/study-guide/2014-A.md` | **655** | `wc -l` |
| `projects/ethics-study/exam-solutions/coverage/2014-A.md` | **103** | `wc -l` |
| `/home/jai/잡동사니/임용/md/2014중등1차-2교시-도덕윤리-전공A-문제지-최종.md` | **263** | `wc -l` |

---

## 1. 문항 수 — PASS

- `grep -cE '^## 문항' study-guide/2014-A.md` → **20** 건 (기입형 15 + 서술형 5).
- 헤더 라인(L26·L58·L89·L114·L142·L167·L192·L218·L245·L272·L299·L329·L364·L391·L419·L451·L483·L516·L555·L595) 전수 확인.
- 누락·중복 0건.

## 2. 원문 line metadata 실재 — PASS

- `grep -cE '원문 line L' study-guide/2014-A.md` → **20** 건. 모든 문항 헤더에 `원문 line L{m}-L{n}` 형식 실재.
- 각 range 가 원본 exam md 의 해당 문항 블록과 일치 (Q1=L18-L43 ↔ exam 18-43 / Q5=L81-L85 ↔ exam 81-85 / S5=L255-L259 ↔ exam 255-259 등 spot-check 3건 byte-level 일치).
- 형식 일탈·metadata 누락 0건.

## 3. 제시문 verbatim byte-level 일치 — PASS

- `grep -cE '^### 제시문 verbatim' study-guide/2014-A.md` → **20** 건 (20문항 전부 제시문 섹션 실재, "(제시문 없음)" 표기 필요한 문항 0건).
- 30개 대표 verbatim 구간 `grep -cF` 3-way 실측 — study-guide·coverage·원본 exam 3개 파일 전부에서 각 1 건씩 매칭:

| 구간 (일부) | sg | cov | exam |
|-------------|----|----|------|
| 아동 발달 프로젝트(Child Development Project)를 통해 학생들이 | 1 | 1 | 1 |
| 가치 확인 및 명료화 | 1 | 1 | 1 |
| 환경이 개인의 성격이나 행동을 만드는 것이 아니다 | 1 | 1 | 1 |
| 도덕적 정당화, 완곡한 언어의 사용, 유리한 비교 | 1 | 1 | 1 |
| 이는 공자가 남긴 글이니 | 1 | 1 | 1 |
| 나가르주나(Nāgārjuna, 龍樹)이다 | 1 | 1 | 1 |
| 공의 세계는 생겨[生]나지도 소멸[滅]하지도 않으며 | 1 | 1 | 1 |
| 내 집 앞에 큰 가죽나무가 한 그루 있네 | 1 | 1 | 1 |
| 신인은 재목이 되지 않는다 | 1 | 1 | 1 |
| 오직 우리 해동의 보살만이 | 1 | 1 | 1 |
| 세계가 신의 섭리에 의해서 지배된다는 사실을 받아들인다면 | 1 | 1 | 1 |
| 이로부터 생겨난 법 또한 영원하다 | 1 | 1 | 1 |
| 사유는 사물에 내재하는 정적이고 영원한 성질 | 1 | 1 | 1 |
| 수동적인 정서는 우리가 그것에 대해 명석 판명한 관념을 | 1 | 1 | 1 |
| 참된 자유를 얻기 위해서 | 2 | 1 | 1 (sg 1건은 본문 풀이 과정 재인용, 1건은 제시문 verbatim — 변조 아님) |
| 개인적 선호를 주어진 것으로 간주하고 | 1 | 1 | 1 |
| 무력도발 불용, 흡수통일 불원, 화해협력 추구 | 1 | 1 | 1 |
| 더 오래 지속된 편견일수록 | 1 | 1 | 1 |
| 군주가 되는 것은 전적으로 능력과 행운 | 1 | 1 | 1 |
| 인민이 주도권을 잡고 귀족들의 정치 참여를 용인하는 | 1 | 1 | 1 |
| 자연의 경향을 모두 변화시키고 변질시키는 것 | 1 | 1 | 1 |
| 도덕적 추론은 인지 능력의 발달에 기초하여 | 1 | 1 | 1 |
| 중학생 A는 요즘 들어 | 1 | 1 | 1 |
| 선지후행(先知後行)과 지행병진(知行竝進)을 주장하셨는데 | 1 | 1 | 1 |
| 환인(桓因)의 아들로 환웅(桓雄)이 있었는데 | 1 | 1 | 1 |
| 성인(聖人)이 되는 학문에는 큰 단서가 있고 | 1 | 1 | 1 |
| 행복은 완전한 탁월성에 따르는 영혼의 어떤 활동이다 | 1 | 1 | 1 |

- HTML `<u>...</u>` 제시문 내부 밑줄 구간 7개 전수 원본 exam md 와 byte-level 일치:

| # | `<u>` 구간 | sg | exam |
|---|------------|----|----|
| 1 | `<u>오직 우리 해동의 보살만이 성(性)과 상(相)을 융화해 밝히고 과거와 지금을 은밀히 통괄해 백가(百家)의 논쟁의 단서를 화해시켜서 한 시대의 지극히 공정한 논의를 얻었다.</u>` | 1 | 1 |
| 2 | `<u>이로부터 생겨난 법 또한 영원하다. 지적 피조물인 인간이 공유하고 있는 영원한 법을 자연법이라 부르며, 인간은 영원한 법을 반영하는 자연적 성향을 갖고 있다.</u>` | 1 | 1 |
| 3 | `<u>편견</u>` | 1 | 1 |
| 4 | `㉠ <u>3가지 정치체제</u>` | 1 | 1 |
| 5 | `㉠ <u>태극</u>` | 1 | 1 |
| 6 | `㉠ <u>욕구적인 것</u>` | 1 | 1 |
| 7 | `㉡ <u>일차적인 의미에서 이성을 자체 안에 가지고 있는 것</u>` | 1 | 1 |

- 원본 exam 의 `<u>` 총 9개 중 2개(`<u>밑줄 친 내용</u>` L101 · `<u>밑줄 친 개념</u>` L167)는 발문 내부에서 "밑줄 친" 을 자연어로 재구성한 형태로 study-guide 의 발문 섹션에 흡수(coder report §7 정책 명시). 제시문 내부 밑줄 구간 7/7 은 원본과 byte-level 일치.
- 괄호 영문 `(Child Development Project)` · `(Nāgārjuna, 龍樹)` · 특수기호 `㉠·㉡·[生]·[滅]·[斷]·[常]·[一]·[異]·[來]·[去]·[名相]·[理觀]·[dharma]·(聖人)·(德)·(眞實)·(無妄)·(無聲)·(無臭)` 전부 보존.

## 4. ES 등록 16건 found=true 재조회 — PASS

명령: `curl -s http://localhost:9200/ethics-thinkers/_doc/{id}` (본 세션 2026-04-22 실측).

| thinker_id | found | 문항 |
|------------|-------|------|
| confucius | True | Q4 |
| wonhyo | True | Q7 |
| aquinas | True | Q8 |
| dewey | True | Q9 |
| spinoza | True | Q10 |
| rousseau | True | Q15 |
| zhuxi | True | Q4·S2 |
| wangyangming | True | S2 |
| yihwang | True | S4 |
| aristotle | True | S5 |
| zhuangzi | True | Q6 |
| habermas | True | Q11 |
| bandura | True | Q3 (★ override) |
| turiel | True | S1 (★ override) |
| raths | True | Q2 (B) |
| lickona | True | Q1 대안 참고 |

16건 전부 `found=true`. Coder 명세 14건 + raths·lickona 2건(Q2·Q1 보조 참조) 추가 포함.

## 5. ES 미등록 6건 found=false 확증 — PASS

| thinker_id | found | 문항 · 표기 라인 |
|------------|-------|------------------|
| nagarjuna | False | Q5 L157 `⚠️ ES 미등록 [BLK 미배정]` |
| burke | False | Q13 L381 `⚠️ ES 미등록 [BLK 미배정]` |
| machiavelli | False | Q14 L409 `⚠️ ES 미등록 [BLK 미배정]` |
| cdp | False | Q1 L47 `⚠️ ES 미등록 [BLK 미배정]` |
| child_development_project | False | (Q1 별칭) |
| coombs_meux | False | Q2 모형 A L79 "`found=false` (보강 필요)" 표기 |

본 명세 4건 (Q1·Q5·Q13·Q14) 전수 `⚠️ ES 미등록 [BLK 미배정]` 표기 실재.

## 6. TASK-DQ-006 override 표기 — PASS

| 문항 | 사상가 | coverage 원본 표기 | study-guide 표기 | 판정 |
|------|--------|-------------------|------------------|------|
| Q3 | bandura | coverage L40 "ES 사상가 누락" | L104 `✅ ES 등록 (커버리지 정정 규정)` | PASS (override 적용) |
| S1 | turiel | coverage L44 "ES 사상가 누락" | L467 `✅ ES 등록 (커버리지 정정 규정)` | PASS (override 적용) |

study-guide L17·L20 ES 등록 상태 요약 공지에서 "coverage 의 오기재를 정정한다" 명시 + TASK-DQ-006 참조 기재. coverage 오기재 복제 0건.

## 7. 채점 기준 섹션 — PASS

- `grep -cE '^### 채점 기준' study-guide/2014-A.md` → **5** 건.
- 라인: L470 (S1) · L504 (S2) · L542 (S3) · L582 (S4) · L622 (S5). 서술형 5문항 전원 실재. 기입형에는 없음 (규정상 불요).
- 각 채점 기준은 점수 배분(2+2 또는 1.5+2.5)·감점 포인트를 포함.

## 8. 자기검증 2단계 역grep — PASS (trademark 자동 bug 규약 clean)

### Step 1 · 괄호 안 영어 토큰 재추출

명령: `grep -oE '\([A-Za-z][^)]*\)' study-guide/2014-A.md | sort -u` → 29개 토큰.

**실질 사상가·개념 토큰 5건** (schema id·면제 keyword·메타 라벨 제외) coverage + 원본 exam 2-way 역grep:

| # | 토큰 | sg | cov | exam | 판정 |
|---|------|----|----|------|------|
| 1 | `CDP` | 7 | 2 | 0 | PASS (coverage hit) |
| 2 | `Child Development Project` | 1 | 3 | 1 | PASS (양측 hit) |
| 3 | `Nāgārjuna, 龍樹` | 3 | 1 | 1 | PASS (양측 hit) |
| 4 | `moral disengagement` | 1 | 1 | 0 | PASS (coverage hit — bandura 표준 어휘) |
| 5 | `sub specie aeternitatis` | 1 | 2 | 0 | PASS (coverage hit — 스피노자 라틴어 표준) |

**면제 토큰 24건** (메타데이터·프레임워크 라벨·열거 지시자) — 사상가/개념 주장 0건:
- 열거 지시자: `(A)·(B)·(a)·(b)·(c)·(d)` — 5건
- 파일 line 참조: `(L1~L103)·(L1~L263)·(L40)·(L44)·(L523~L638)·(coverage L17 / L64)·(coverage L19)·(coverage L23)·(coverage L24)·(coverage L28)·(coverage L32)·(coverage/2014-A.md L91~L97 근거)·(coverage/2014-A.md L99~L103 근거; 본 가이드 정정 규정 반영)` — 13건
- 프레임워크 라벨: `(BLK 미배정)·(TASK-DQ-006 기록)·(coverage 정정 규정)·(thinker 실재·claim 보강 필요)·(Q3)` — 5건
- 한국어 동의어 주석: `(sub specie aeternitatis — 원문 라틴어 표현이나 한국어 번역은 '영원의 상')` — Step 1 핵심어 "sub specie aeternitatis" 는 이미 위 #5에서 PASS 확인 (coverage hit=2).

### Step 2 · TitleCase phrase 재추출

명령: `grep -oE '[A-Z][a-z]+(\s+[A-Za-z][a-z]+){1,5}' study-guide/2014-A.md | sort -u` → 3개 토큰.

| # | 토큰 | sg | cov | exam | 판정 |
|---|------|----|----|------|------|
| 1 | `Albert Bandura` | 1 | 3 | 0 | PASS (coverage hit — bandura 풀네임) |
| 2 | `Child Development Project` | 1 | 3 | 1 | PASS (양측 hit) |
| 3 | `Edmund Burke` | 1 | 3 | 0 | PASS (coverage hit — burke 풀네임) |

**Step 2a JSON id/name_en 패턴** → 0건 (study-guide 에는 JSON 블록 없음, 마크다운 산문 형식).

### 자기검증 결론

- Step 1 실질 5건 + Step 2 실질 3건 = **총 8건**의 사상가·개념 영어 토큰 전수 coverage hit ≥ 1.
- **coverage 0 hit & 원본 exam 0 hit** 토큰 = **0건** → trademark 자동 severity=bug 규약 발동 없음.
- 0-hit 토큰은 전부 프레임워크 메타데이터(파일 라인 참조·태스크 ID·상태 라벨·열거 지시자)이며 사상가 이론에 대한 영어 주장을 담지 않으므로 면제.
- Coder 자기검증 표와 Tester 재검증 결과 일치.

---

## 이슈 / 블로커

**없음.** 8항 체크리스트 전수 PASS.

---

## 참고 관찰 (severity=observation — Manager 판단, 본 태스크 영향 없음)

1. (관찰) Coder 가 § 6 자기검증 표에서 "(Q3)"·"(coverage L17 / L64)" 등 메타 토큰을 Step 1 역grep 결과에 열거한 이유: 면제 규정 적용 이유를 투명하게 기록한 설계로, 본 tester 재검증에서도 동일 면제 규정이 정당하게 적용됨을 확인.
2. (관찰) "참된 자유를 얻기 위해서" 가 study-guide 에서 sg=2 (제시문 verbatim 1건 + 풀이 과정 재인용 1건). verbatim 변조가 아니라 풀이 과정에서 같은 어구를 재인용한 것으로, 제시문 섹션 byte-level 일치는 유지.
3. (관찰) `<u>` 태그 수 원본 exam=9 vs study-guide=7. 차이 2건은 발문 안 `<u>밑줄 친 내용</u>` · `<u>밑줄 친 개념</u>` 을 학생용 발문에서 자연어로 재구성한 것으로, 제시문 내부 밑줄은 전부 보존(7/7). Coder report §7 정책과 정합.
4. (관찰) Coder가 후속 태스크 참고로 제시한 claim 보강 후보(zhuxi 신독·zhuangzi 무용지용·spinoza sub specie aeternitatis·habermas 심의민주주의·rousseau 불평등 기원론·yihwang 리발설) 및 ES 신규 등록 후보(CDP·nagarjuna·burke·machiavelli·coombs_meux) 전수 ES 재조회 결과와 일치. Manager가 별도 태스크화를 판단할 수 있는 근거 확보.

---

## 최종 판정

- **severity: none**
- 8항 체크리스트 전수 PASS.
- 문항 20/20 · 원문 line metadata 20/20 · 제시문 verbatim 20/20 · ES 등록 16/16 found=true · ES 미등록 4/4 found=false · TASK-DQ-006 override 2/2 · 채점 기준 5/5 · 자기검증 2단계 0-hit trademark 0건.
- study-guide/2014-A.md (655 lines) 는 학생용 해설 산출물로 DONE 처리 가능.

## 본 세션 실측 명령 감사 로그

- `wc -l` · `grep -cE '^## 문항'` · `grep -cE '^### 채점 기준'` · `grep -c '원문 line L'` · `grep -cE '^### 제시문 verbatim'` · `grep -cE '<u>'` (6건)
- `grep -cF -- "…"` 3-way (study-guide · coverage · exam) × 30 verbatim 구간 = 90 call
- `grep -cF -- "<u>…</u>"` × 7 = 21 call
- `grep -cF -- "$term"` 2-way Step1 5건 + Step2 3건 + 메타 13건 = 21 × 2 = 42 call
- `curl -s http://localhost:9200/ethics-thinkers/_doc/{id}` × 22 (16 true + 6 false)
- `grep -oE '\([A-Za-z][^)]*\)' | sort -u` × 1 · `grep -oE '"(name_en|id)"\s*:\s*"[^"]*"' | sort -u` × 1 · `grep -oE '[A-Z][a-z]+(\s+[A-Za-z][a-z]+){1,5}' | sort -u` × 1
- `grep -n '<u>'` × 2 (sg · exam) — 차이 2건 원인 확인
