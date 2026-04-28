---
agent: tester
task_id: TASK-183-T
status: DONE
severity: none
timestamp: 2026-04-22
target_file: projects/ethics-study/exam-solutions/study-guide/2014-B.md
source_coverage: projects/ethics-study/exam-solutions/coverage/2014-B.md
source_exam: /home/jai/잡동사니/임용/md/2014중등1차-3교시-도덕윤리-전공B-문제지-최종.md
---

# TASK-183-T · 2014-B 학생용 study-guide 검증 · Tester Report

## 0. 파일·카운트 요약 (실측)

| 파일 | 라인 수 | 명령 |
|------|---------|------|
| `projects/ethics-study/exam-solutions/study-guide/2014-B.md` | **309** | `wc -l` |
| `projects/ethics-study/exam-solutions/coverage/2014-B.md` | **97** | `wc -l` |
| `/home/jai/잡동사니/임용/md/2014중등1차-3교시-도덕윤리-전공B-문제지-최종.md` | **68** | `wc -l` |

---

## 1. 문항 수 — PASS

- `grep -c '^## 문항' study-guide/2014-B.md` → **4** (서술형 1·2 + 논술형 1·2).
- 헤더 라인 L27(서술형 1) · L83(서술형 2) · L131(논술형 1) · L182(논술형 2). 누락·중복 0건.

## 2. 원문 line metadata 형식 — PASS

- 4문항 전부 `## 문항 {서술형|논술형} N · {서술형|논술형} · {배점}점 · 원문 line L{m}-L{n}` 형식 준수.
- 서술형 1: `L16-L28` (원본 exam L16~L28 = 서술형 【1~2】 헤더 + 발문 + 제시문 가~라)
- 서술형 2: `L32-L42` (원본 exam L32~L42 = 2번 헤더 + 발문 + 정현/현지 대화 + 그림 설명)
- 논술형 1: `L48-L52` (원본 exam L48~L52 = 1번 헤더 + 발문 + 제시문)
- 논술형 2: `L58-L64` (원본 exam L58~L64 = 2번 헤더 + 발문 + 제시문 가·나·다)
- 형식 일탈·metadata 누락 0건.

## 3. 제시문 verbatim byte-level 일치 — PASS

- `grep -c '^### 제시문 verbatim' study-guide/2014-B.md` → **4** 건 (4문항 전부 제시문 섹션 실재).
- 12개 대표 verbatim 구간 `grep -Fc` 3-way 실측 (study-guide·coverage·원본 exam 3개 파일 전부 각 1건씩 매칭):

| 구간 | sg | cov | exam |
|------|----|----|------|
| 무정부 상태이다 (서술형1-가) | 1 | 1 | 1 |
| 집단 안보를 통한 (서술형1-나) | 1 | 1 | 1 |
| 세계 자본주의가 그 문제의 근원 (서술형1-다) | 1 | 1 | 1 |
| 국가의 정체성이나 국가의 목표 (서술형1-라) | 1 | 1 | 1 |
| 통일비용과 통일편익의 관계를 아래 그림처럼 (서술형2-정현) | 1 | 1 | 1 |
| 곡선 A와 곡선 D사이의 면적[S1] (서술형2-현지) | 1 | 1 | 1 |
| 도덕은 지식이 아니기 때문에 학교의 교과로 가르칠 수 없다 (논술형1) | 1 | 1 | 1 |
| 학교 교육은 경제적인 측면의 국가 경쟁력과 직결 (논술형1) | 1 | 1 | 1 |
| 궁극 목적은 양과 질이라는 두 관점 (논술형2-가/밀) | 1 | 1 | 1 |
| 도덕법칙은 가장 완전한 존재자의 의지 (논술형2-나/칸트) | 1 | 1 | 1 |
| 외경심에서 행위를 규정하는 도덕적 강제의 법칙 (논술형2-나/칸트) | 1 | 1 | 1 |
| 도덕성은 판단된다기보다는 느껴진다 (논술형2-다/흄) | 1 | 1 | 1 |

- 괄호 영문 `(Achtung)` · `(J.S. Mill)` · `(sympathy)` · `(moral sentiment)` · 특수기호 `[S1]`·`[S2]`·`A·B·C·D` 전부 보존.
- 서술형 2 제시문 `면적[S1]` (공백 없음) byte-level 원본 L38 과 일치 (`grep -Fc "면적[S1]"` → sg=1 · cov=1 · exam=1).
- HTML markup: 원본 exam 에 `<u>` 등 HTML 태그 없음(L1~L68 스캔 0건). 따라서 study-guide 에도 불필요, 누락 없음.
- 한자 출현: 원본 exam · study-guide 모두 0건(서양 근대 윤리 사상가 문항이라 한자 부재). 병기 규정 위반 없음.

## 4. ES 등록 10건 found=true 재조회 — PASS

명령: `curl -s http://localhost:9200/ethics-claims/_doc/{claim_id}` (본 세션 2026-04-22 실측).

| claim_id | HTTP | found | thinker_id |
|----------|------|-------|------------|
| mill-claim-001 | 200 | true | mill_js |
| mill-claim-003 | 200 | true | mill_js |
| mill-claim-014 | 200 | true | mill_js |
| kant-claim-003 | 200 | true | kant |
| kant-claim-005 | 200 | true | kant |
| kant-claim-007 | 200 | true | kant |
| kant-claim-008 | 200 | true | kant |
| kant-claim-009 | 200 | true | kant |
| hume-claim-004 | 200 | true | hume |
| hume-claim-010 | 200 | true | hume |

Manager 명세 10건 전부 `found=true` + thinker_id 일치. mill_js 3건 · kant 5건 · hume 2건.

## 5. 해당 없음 표기 + 분류 사유 확증 — PASS

서술형 1·2 + 논술형 1 (3 문항) 관련 ES 근거 섹션에서 `해당 없음` + 분류별 사유 명시 실재.

| 문항 | 라인 | 표기 |
|------|------|------|
| 서술형 1 | L60 | `해당 없음 (경계영역 · 국제정치학 4대 패러다임 구분은 ES 사상가 매핑 대상 아님)` |
| 서술형 2 | L107 | `해당 없음 (교과교육학 · 통일·평화 교육과정)` |
| 논술형 1 | L162 | `해당 없음 (교과교육학 · 도덕과교육학 교과 정당화론)` |

`grep -nE "해당 없음" study-guide/2014-B.md` → 3건 (문항 개수와 일치). 논술형 2 (사상가형) 에는 `해당 없음` 미기재 (정상).

## 6. 채점 기준 서브섹션 — PASS

- `grep -c '^### 채점 기준' study-guide/2014-B.md` → **4** 건.
- 라인: L64 (서술형 1) · L111 (서술형 2) · L166 (논술형 1) · L259 (논술형 2). 4문항 전원 실재.
- 각 채점 기준은 세부 점수 배분(서술형 = 1.25×4 또는 1+2+1+1 / 논술형 = 2+3+2+3 또는 4+3+3) + 감점 포인트를 포함.

## 7. 자기검증 2단계 역grep — PASS (trademark 자동 bug 규약 clean)

### Step 1 · 괄호 안 영어 토큰 재추출

명령: `grep -oE '\([A-Za-z][^)]*\)' study-guide/2014-B.md | sort -u` → 24개 토큰.

**원문-인용 관련 trademark 11건** coverage grep 결과:

| # | 토큰 | coverage hit | 판정 |
|---|------|--------------|------|
| 1 | `(Achtung)` | 1 | PASS |
| 2 | `(J.S. Mill)` | 1 | PASS |
| 3 | `(Kohlberg·Piaget 도덕발달론 전제)` | 1 | PASS |
| 4 | `(Morgenthau·Waltz·Keohane·Wallerstein·Wendt 등)` | 1 | PASS |
| 5 | `(constructivism)` | 1 | PASS |
| 6 | `(liberalism)` | 1 | PASS |
| 7 | `(moral sentiment)` | 1 | PASS |
| 8 | `(realism)` | 1 | PASS |
| 9 | `(social capital)` | 1 | PASS |
| 10 | `(sympathy)` | 2 | PASS |
| 11 | `(world-system/dependency)` | 1 | PASS |

**면제 토큰 13건** (메타데이터·열거 지시자·계수 설명) — 사상가/개념 주장 0건, coverage 대조 불요:
- 열거/참조: `(A)`, `(a)`, `(b)`, `(c)`, `(D 또는 C)`
- 파일 line 참조: `(L1~L68)`, `(L1~L97)`, `(L523~L638)`, `(coverage/2014-B.md L82~L88 근거)`, `(coverage/2014-B.md L90~L94 근거)`
- 프레임워크 라벨: `(TASK-182 산출물)`, `(mill_js · kant · hume 3 사상가 모두 ES 등록 + 핵심 claim 매핑 완료)`, `(S1, S2, 통일비용, 통일편익)`

### Step 2 · 대문자 시작 단어 재추출

명령: `grep -oE '[A-Z][A-Za-z][a-zA-Z]+' study-guide/2014-B.md | sort -u` → 13개 토큰.

| # | 토큰 | coverage hit | 판정 |
|---|------|--------------|------|
| 1 | Achtung | 1 | PASS |
| 2 | Bentham | 1 | PASS |
| 3 | Keohane | 1 | PASS |
| 4 | Kohlberg | 1 | PASS |
| 5 | Mill | 3 | PASS |
| 6 | Morgenthau | 1 | PASS |
| 7 | NGO | 1 | PASS |
| 8 | Phase | 2 | PASS |
| 9 | Piaget | 1 | PASS |
| 10 | TASK | 1 | PASS |
| 11 | Wallerstein | 1 | PASS |
| 12 | Waltz | 1 | PASS |
| 13 | Wendt | 1 | PASS |

### 자기검증 결론

- Step 1 실질 11건 + Step 2 전수 13건 coverage hit ≥ 1.
- **coverage 0-hit 토큰 = 0건** → trademark 자동 severity=bug 규약 **발동 없음**.
- 면제 토큰 13건은 프레임워크 메타데이터(파일 라인 참조·태스크 ID·열거 지시자·내부 참조 라벨)로 사상가 이론 주장을 담지 않음.

## 8. 배점 합계 30점 — PASS

- `grep -nE "30점|= \*\*30" study-guide/2014-B.md` → L6 · L302 2건 실재.
- L6 메타: `배점: 30점 (서술형 2×5점 + 논술형 2×10점)`
- L302 합계: `서술형 1(5) + 서술형 2(5) + 논술형 1(10) + 논술형 2(10) = **30점** ✓`
- 헤더 metadata 배점 (서술형 = 5점 × 2 · 논술형 = 10점 × 2) 전수 일치. 합계 산식 30점 일치.

---

## 이슈 / 블로커

**없음.** 8항 체크리스트 전수 PASS.

---

## 참고 관찰 (severity=observation — Manager 판단, 본 태스크 영향 없음)

1. **(관찰 · 발문 섹션 볼드 강조)** 논술형 2 발문 L185 는 원본 exam L58 의 평문 발문에 `**(가)의 관점에서 (나)를 비판**` / `**(나)와 (다) 사상가의 주장이 보편성을 획득할 수 있는 근거**` 두 마크다운 볼드 강조가 추가되어 있다. "제시문 verbatim" 이 아닌 "발문" 섹션이므로 byte-level 일치 요구 대상은 아니지만, TASK-182 선례의 발문은 원문 평문을 그대로 또는 축약해 기재하는 방식이 다수였다. 학생 가독성 강조로 해석 가능한 범위. 향후 해설 시리즈 전체의 발문 섹션 처리 정책 통일 필요 시 회고 아이템.

2. **(관찰 · 서술형 2 발문 부연 확장)** 서술형 2 발문 L86 에서 원본 exam L34 의 발문("정현의 답변 내용을 S1, S2, 통일비용, 통일편익 등의 용어를 포함하여 서술하시오") 뒤에 `구체적으로는, 통일시점 이후 I 시점까지 곡선 A와 곡선 D 사이의 면적 [S1]이 통일시점 이후 K 시점까지 곡선 A와 곡선 C 사이의 면적 [S2]보다 작은 이유를 설명하라는 요구.` 라는 저자의 부연 해석이 이어진다. 다른 문항 발문(서술형 1·논술형 1·논술형 2) 은 원본 발문의 축약·그대로 인용에 그치는 반면 이 문항은 부연 해석까지 포함하여 스타일 불균일. 발문 섹션은 원문 재서술 허용 구간이므로 bug 아님.

3. **(관찰 · `면적[S1]` 공백 처리 혼용)** 원본 exam L38 은 `면적[S1]` (공백 없음). 서술형 2 제시문 verbatim(L91) 은 원본대로 공백 없음 유지(PASS), 반면 저자가 요약한 발문(L86) 은 `면적 [S1]` (공백 포함) 로 자연어 가독성을 위해 공백 삽입. 제시문 섹션은 byte-level 일치, 발문 섹션은 저자 재서술이므로 모순 없음. 학생용 가이드 스타일 가이드 차원의 관찰.

4. **(관찰 · 서술형 1 [S1]/[S2] 이외 특수기호 `A·B·C·D` 표기)** 서술형 2 제시문은 `곡선 A`, `곡선 B, C, D` 와 같이 알파벳 곡선명을 쉼표·공백으로 보존하며, `A·B·C·D` 가운뎃점 연결 형식은 저자 해설(예: L121 (b) 곡선 형태 설명)에서만 사용. 본 태스크 명세 "특수기호 `A·B·C·D`" 요건은 저자 해설 차원으로 해석되며 원문 verbatim 은 `A, B, C, D` (쉼표) 형식 그대로 유지 — 규정 위반 없음.

---

## 최종 판정

- **severity: none**
- **verdict: PASS**
- 8항 체크리스트 전수 PASS.
- 문항 4/4 · 원문 line metadata 4/4 · 제시문 verbatim 12/12 대표 구간 3-way byte-level 일치 · ES claim 10/10 found=true · 해당 없음 표기 3/3 · 채점 기준 4/4 · 자기검증 2단계 0-hit trademark 0건 · 배점 합계 30점 일치.
- study-guide/2014-B.md (309 lines) 는 학생용 해설 산출물로 DONE 처리 가능.

## 본 세션 실측 명령 감사 로그

- Read: `study-guide/2014-B.md` 전체 · `coverage/2014-B.md` 전체 · `2014중등1차-3교시-도덕윤리-전공B-문제지-최종.md` 전체 · `agents/tester.md` 전체 · `architecture.md` 전체 · `tester-report-TASK-182.md` 전체 · `study-guide/2014-A.md` offset=58 limit=50 (발문 선례 확인)
- `wc -l` × 3 파일
- `grep -c '^## 문항'` × 1 · `grep -c '^### 채점 기준'` × 1 · `grep -c '^### 제시문 verbatim'` × 1 · `grep -nE '^## 문항'` × 1 · `grep -nE '^### (제시문|관련 ES|채점|풀이 과정|정답|발문)'` × 1
- `grep -Fc "…"` 원본 exam 대조 × 12 verbatim 구간
- `grep -nE "해당 없음"` × 1 · `grep -nE "30점|= \*\*30"` × 1
- `grep -oE '\([A-Za-z][^)]*\)' | sort -u` × 1 · `grep -oE '[A-Z][A-Za-z][a-zA-Z]+' | sort -u` × 1
- `grep -Fc "$tok"` × 11 (Step 1 trademark) + × 13 (Step 2 대문자) = 24 call
- Python 한자 regex 스캔 × 1 (결과: 한자 0건)
- `curl -s http://localhost:9200/ethics-claims/_doc/{claim_id}` × 10 (전수 found=true)
- `curl -s http://localhost:9200/` healthcheck × 1
- `grep -Fn "면적[S1]"` · `grep -Fn "면적 [S1]"` × 3-way 파일 (공백 혼용 관찰용)
- `grep -Fn` 발문 3건 원본 대조
