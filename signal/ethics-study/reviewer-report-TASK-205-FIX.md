---
agent: reviewer
task_id: TASK-205-FIX
verdict: NEEDS_REVISION
timestamp: 2026-04-24T02:40:00+09:00
subject: Manager TASK-205-FIX spec + TASK-205-FIX-T spec (task-board.md L359-L360) 검증
source_of_truth:
  - signal/ethics-study/tester-report-TASK-205-T.md (severity=bug · 268L)
  - projects/ethics-study/exam-solutions/study-guide/2025-B.md (732L)
  - Elasticsearch localhost:9200/ethics-claims
es_spot_check: PASS (3 / 3 rows confirmed)
---

# Reviewer Report — TASK-205-FIX (Manager spec 검증)

## 0. 판정 요약

**NEEDS_REVISION** — Manager 가 제시한 모든 핵심 수치(85 · 14 · per-thinker 분포 · 147 em-dash · 393 ㉠~㉥ · fudge 0 · BLOCKER 2명 · 3-step 124/0/28)는 실측과 완전 일치하였고, Tester §9.1 BUG-001 의 ES mismatch 샘플 3건(jinul-002 · lickona-002 · pettit-002)도 ES `_doc` 실측으로 BUG 가 확증되어 **수정 필요성과 범위는 정당**하다. 그러나 Manager spec 에 **Coder 가 외부 질문 없이 실행하기 위해 반드시 필요한 ES 치환 정책의 결정 기준**이 불완전하여, 이 상태로 Coder 에게 전달하면 재귀 질문·judgement call 이 발생한다. 아래 3건의 구체적 보강 후 재검증.

---

## 1. 검증 필수 항목 전수 결과

### 1.1 내용 일치 (실측 근거)

| # | 항목 | Manager 주장 | Reviewer 실측 | 결과 |
|---|------|--------------|---------------|------|
| 1 | unique claim_id 총수 | 85 | `grep -oE '[a-z_]+-claim-[0-9]+' 2025-B.md \| sort -u \| wc -l` → **85** | ✅ PASS |
| 2 | unique thinker 총수 | 14 | sort -u 후 prefix 추출 → bandura · bentham · gilligan · hobbes · jinul · kant · kohlberg · lickona · mill_js · moore · pettit · wangyangming · yiyulgok · zhuxi (**14**) | ✅ PASS |
| 3 | thinker 분포 bandura 6 | 6 | **6** | ✅ PASS |
| 4 | bentham 6 | 6 | **6** | ✅ PASS |
| 5 | gilligan 5 | 5 | **5** | ✅ PASS |
| 6 | hobbes 8 | 8 | **8** | ✅ PASS |
| 7 | jinul 6 | 6 | **6** | ✅ PASS |
| 8 | kant 8 | 8 | **8** | ✅ PASS |
| 9 | kohlberg 5 | 5 | **5** | ✅ PASS |
| 10 | lickona 7 | 7 | **7** | ✅ PASS |
| 11 | mill_js 5 | 5 | **5** | ✅ PASS |
| 12 | moore 5 | 5 | **5** | ✅ PASS |
| 13 | pettit 5 | 5 | **5** | ✅ PASS |
| 14 | wangyangming 6 | 6 | **6** | ✅ PASS |
| 15 | yiyulgok 7 | 7 | **7** | ✅ PASS |
| 16 | zhuxi 6 | 6 | **6** | ✅ PASS |
| 17 | `^## 문항` == 11 | 11 | `grep -cE '^## 문항'` → **11** | ✅ PASS |
| 18 | em-dash U+2014 count | 147 | `grep -oE '—' \| wc -l` → **147** | ✅ PASS |
| 19 | ㉠~㉥ count | 393 | `grep -oE '[㉠-㉥]' \| wc -l` → **393** | ✅ PASS |
| 20 | 한자 161 unique | 161 | python token-regex `[\u4e00-\u9fff]+` → **161 unique tokens** (참고: 문자 기준 unique = 222). Manager 와 Coder/Tester 가 **token** 계측을 사용. 단, spec 에 "token" 명시 없음 — §3 권고 참조 | ✅ PASS (정의 일치 하) |
| 21 | fudge grep 0-hit | 0 | `grep -ciE '(≈\|수렴\|중복 보정\|대략\|얼추\|거의)\|fudge'` → **0** | ✅ PASS |
| 22 | BLOCKER 2명 표기 유지 (berlin Q10 을 + Q7 갑) | 2 | `grep -cE 'BLK-175E-2025B-00[56]'` → **17 occurrences** · L19·L20·L57·L61·L434·L470·L484·L618·L643·L656·L670 등 ⚠️BLOCKER 표기 확증 | ✅ PASS |

### 1.2 ES Spot-check (Tester §9.1 BUG-001 샘플 확증)

Manager 는 Tester report §9.1 BUG-001 의 24건 샘플을 "shifted 패턴" 으로 인용. Reviewer 가 이 중 핵심 3건을 `GET /ethics-claims/_doc/{id}` 직접 조회로 spot-check.

#### Spot-check #1: `jinul-claim-002` (Tester 표 row: study=돈오점수 ↔ ES=정혜쌍수)

```
curl -s 'http://localhost:9200/ethics-claims/_doc/jinul-claim-002'
→ found=True
→ claim: "정혜쌍수(定慧雙修)란 선정(定)과 지혜(慧)를 동시에 함께 닦아야 한다는 수행 원리..."
→ keywords: ['정혜쌍수', '정(定)과 혜(慧)', '삼학', '혼침·산란', '정혜결사']
```

study-guide L96 본문은 이 claim_id 를 "돈오점수 trademark" 로 인용 → **BUG-001 확증**.

#### Spot-check #2: `lickona-claim-002` (Tester 표 row: study=존중과 책임 2가치 ↔ ES=도덕적 앎 6요소)

```
curl -s 'http://localhost:9200/ethics-claims/_doc/lickona-claim-002'
→ found=True
→ claim: "도덕적 앎(moral knowing)은 여섯 가지 하위 요소로 구성된다: (1) 도덕적 인식..."
→ keywords: ['도덕적 앎', '도덕적 인식', '관점 채택', '도덕적 추론', '의사결정']
```

study-guide L208 본문은 이 claim_id 를 "존중과 책임 2가치" 로 인용 → **BUG-001 확증**.

#### Spot-check #3: `pettit-claim-002` (Tester 표 row: study=비지배 자유 ↔ ES=자유주의 비판)

```
curl -s 'http://localhost:9200/ethics-claims/_doc/pettit-claim-002'
→ found=True
→ claim: "자유주의는 국가나 타인들의 간섭으로부터 개인을 지켜내는 데는 성공을 거두었지만..."
→ keywords: ['주인으로서의 삶', '자유주의 비판', '비간섭', '비지배', '주인 없는 삶']
```

study-guide L652 본문은 이 claim_id 를 "비지배 자유" 로 인용 → **BUG-001 확증**.

#### Bonus spot-check: bandura `collective efficacy` 부재 확증

```
curl -s 'http://localhost:9200/ethics-claims/_search?q=thinker_id:bandura+AND+content:collective'
→ total=0, hits_count=0
curl -s 'http://localhost:9200/ethics-claims/_search?q=thinker_id:bandura&size=10'
→ 8 hits (bandura-claim-001~008)
→ bandura-claim-005 claim: "인간은 환경 자극의 수동적 반응자가 아니라... 행위 주체성(human agency)..."
→ keywords (claim-005): ['행위 주체성', 'human agency', '도덕적 책임', '의도적 영향력']
```

bandura 전체 claim 에 `collective efficacy` · `집단 효능감` 키워드 **없음** → Tester §9.1 BUG-001 마지막 행 "bandura-claim-005 집단 효능감 ES 부재" **확증**.

**Spot-check 결론**: Tester §9.1 BUG-001 의 표는 실제 ES 상태와 일치. Manager 가 인용한 "shifted 패턴" · "collective efficacy ES 전체 부재" 주장 모두 사실이며, TASK-205-FIX 수정 필요성과 범위는 **정당**.

### 1.3 태스크 완결성

| # | 항목 | 판정 | 근거 |
|---|------|------|------|
| C1 | Coder 가 외부 질문 없이 85 claim_id 를 찾을 수 있나? | ✅ PASS | spec 본문에 `grep -oE '[a-z_]+-claim-[0-9]+' 2025-B.md \| sort -u` 명령 명시 |
| C2 | Coder 가 ES 전수 조회 명령 알 수 있나? | ⚠️ PARTIAL | spec 에 `curl -s 'http://localhost:9200/ethics-claims/_search?q=thinker_id:X&size=20&_source=true'` 명시되어 있어 각 thinker 전수 조회는 가능. 다만 `size=20` 은 최대 claim 수(hobbes 8, kant 8)보다 여유 있어 안전. 단, 각 claim_id 의 content 를 쌍별 비교하려면 `GET /ethics-claims/_doc/{id}` 재조회가 필요한데 이는 spec 에 명시되지 않음 → §3.C 권고 참조 |
| C3 | 완료 조건 측정 가능한가? (85 claim_id 전원 found=true && content match 자동 확증) | ⚠️ PARTIAL | `found=true` 자동 확증은 simple bash loop 로 쉬우나 `content match` 는 judgement call. spec 에 판정 기준 (keyword 몇 개 겹치면 match 인가 · 완전 일치 요구인가) 없음 → §3.A 권고 참조 |
| C4 | 무결 부분 보존 측정 | ✅ PASS | spec 이 수치 전수 (11 · 40점 · 147 · 161 · 393 · fudge 0 · BLOCKER 2명) 명시. Coder/Tester 재측정 가능 |
| C5 | 3-step 재측정 기록 | ✅ PASS | 변경 전 (124·0·28) 대비 변경 후 수치 명시 요구, Coder report 삽입 방침 명확 |
| C6 | "collective efficacy" 부재 개념 처리 방침 명확한가? | ⚠️ PARTIAL | spec (c) 항에 "제거하거나 ES 에 실재하는 인접 개념으로 재서술" 으로 **택일 여지**를 남김. Coder 가 어떤 경우 제거, 어떤 경우 재서술할지 결정 기준 부재 → §3.B 권고 참조 |

### 1.4 의존성·순서

| # | 항목 | 판정 | 근거 |
|---|------|------|------|
| D1 | TASK-205-T DONE 상태 | ✅ PASS | task-board L358 마지막 컬럼 `DONE (NEEDS_REVISION severity=bug ...)` |
| D2 | TASK-205-T severity=bug 확증 | ✅ PASS | tester-report-TASK-205-T.md L5 frontmatter `severity: bug` · L20 본문 반복 |
| D3 | TASK-205-FIX Depends On = TASK-205-T | ✅ PASS | task-board L359 Depends On 컬럼 `TASK-205-T` |
| D4 | TASK-205-FIX-T Depends On = TASK-205-FIX | ✅ PASS | task-board L360 Depends On 컬럼 `TASK-205-FIX` |
| D5 | FIX → FIX-T 순차 실행 구조 | ✅ PASS | Coder → Tester 표준 pipeline |

### 1.5 목적성·분리 원칙

| # | 항목 | 판정 | 근거 |
|---|------|------|------|
| P1 | FIX 가 단일 md 파일(2025-B.md) 국한 | ✅ PASS | spec 대상 파일 1개 · 관심사 단일 (claim_id 매핑 정합) |
| P2 | 재검증 별도 태스크 분리 (FIX-T) | ✅ PASS | task-board L360 FIX-T row 등록 |
| P3 | 수정 범위 명시 (85 · 14) | ✅ PASS | spec 본문 |
| P4 | Coder 국소 Edit 흡수 가능 | ✅ PASS | 단일 md 파일 내 claim_id 치환 및 인접 재서술 |

---

## 2. Manager 주장 수치 실측 근거 (재현 가능 명령)

```bash
# 85 unique claim_id
grep -oE '[a-z_]+-claim-[0-9]+' projects/ethics-study/exam-solutions/study-guide/2025-B.md | sort -u | wc -l
→ 85

# 14 thinker
grep -oE '[a-z_]+-claim-[0-9]+' projects/ethics-study/exam-solutions/study-guide/2025-B.md | sort -u | sed 's/-claim-[0-9]*//' | sort -u
→ bandura bentham gilligan hobbes jinul kant kohlberg lickona mill_js moore pettit wangyangming yiyulgok zhuxi (14)

# thinker 별 claim 수 분포
grep -oE '[a-z_]+-claim-[0-9]+' ...2025-B.md | sort -u | sed 's/-claim-[0-9]*//' | sort | uniq -c | sort -rn
→ 8 kant · 8 hobbes · 7 yiyulgok · 7 lickona · 6 zhuxi · 6 wangyangming · 6 jinul · 6 bentham · 6 bandura · 5 pettit · 5 moore · 5 mill_js · 5 kohlberg · 5 gilligan

# 11문항
grep -cE '^## 문항' ...2025-B.md → 11

# em-dash U+2014
grep -oE '—' ...2025-B.md | wc -l → 147

# ㉠~㉥
grep -oE '[㉠-㉥]' ...2025-B.md | wc -l → 393

# fudge 0-hit
grep -ciE 'fudge' ...2025-B.md → 0

# BLOCKER IDs
grep -nE 'BLK-175E-2025B-00[56]' ...2025-B.md → 17 occurrences · L19·L20·L57·L61·L434·L470·L484·L618·L643·L656·L670·...

# 한자 161 unique tokens (python)
python3 -c "import re; text=open('...2025-B.md').read(); tokens=re.findall(r'[\u4e00-\u9fff]+',text); print(len(set(tokens)))" → 161

# jinul ES 전수 (9 claims)
curl -s 'http://localhost:9200/ethics-claims/_search?q=thinker_id:jinul&size=20' → 9 hits (jinul-claim-001~009)

# moore ES 전수
curl -s '.../ethics-claims/_search?q=thinker_id:moore&size=20' → 7 hits

# bandura ES 전수
curl -s '.../ethics-claims/_search?q=thinker_id:bandura&size=20' → 8 hits

# pettit ES 전수
curl -s '.../ethics-claims/_search?q=thinker_id:pettit&size=20' → 8 hits

# berlin ES 부재 확증
curl -s '.../ethics-claims/_doc/berlin' → found=False
curl -s '.../ethics-claims/_search?q=thinker_id:berlin&size=20' → 0 hits
```

---

## 3. NEEDS_REVISION 구체 수정 요청 (필수 보강 3건)

Manager 가 아래 3건을 task-board L359 TASK-205-FIX row 의 Description 에 **추가 삽입**해야 Coder 가 외부 질문 없이 실행 가능해진다.

### §3.A (blocker) content match 판정 기준 명시

**위치**: task-board.md L359 TASK-205-FIX row 의 `**수정 절차**` (2) 항과 (3) 항 사이.

**현재**: spec 은 "(a) ES content 가 study 서술 주제와 일치하면 유지 (b) 불일치면 치환" 이라고만 기술.

**문제**: "일치"의 조작적 정의가 없어 Coder 가 judgement call 하게 된다. 특히 Tester §9.1 pettit row 001 과 hobbes row 003·008 은 `≈ 동명사 주체 동일하나 요약 초점 다름` · `≈ 포괄적 일치` · `≈ 부분 일치` 처럼 Tester 스스로도 회색지대라고 적었다.

**추가 문구**:

> **content match 판정 기준**: 각 claim_id 에 대해 ES `_doc` 의 `claim` + `keywords` 필드를 study-guide 해당 문장의 **key-phrase 3개 이상 overlap** 하면 match 로 본다 (예: 주요 개념명·trademark term·저작명 중 3개 이상). Tester §9.1 에서 `≈` 로 표기된 row (pettit-001·hobbes-003·hobbes-008) 는 이 기준으로 **재평가 후 치환 여부를 판정** — 3개 미만이면 치환 대상, 3개 이상이면 유지.

### §3.B (blocker) "collective efficacy" 등 ES 부재 개념 처리 우선순위 명시

**위치**: task-board.md L359 TASK-205-FIX row 의 `**수정 절차**` (2)(c) 항.

**현재**: "제거하거나 ES 에 실재하는 인접 개념으로 재서술" — 택일 여지.

**문제**: Coder 가 문항별로 자의적 선택을 하면 study-guide 의 교육적 가치가 일관성을 잃는다. 또한 Q5 bandura 의 경우 "집단 효능감" 은 교과 과정상 중요 개념이라 단순 제거는 교육 결손이 된다.

**추가 문구**:

> **ES 부재 개념 처리 우선순위**:
> (a) **1순위 — 같은 thinker 내 인접 개념으로 재서술**: 교과교육상 필수 개념이면 (예: bandura 의 "집단 효능감"), ES 에 실재하는 가장 인접한 claim (예: bandura-claim-005 행위 주체성 · bandura-claim-006 자기효능감) 의 claim_id 를 인용하되, study-guide 본문은 **"행위 주체성 및 자기효능감 이론을 공동체 수준으로 확장한 개념"** 처럼 교과서 표준 해설로 보조 서술.
> (b) **2순위 — claim_id 인용 생략**: 인접 개념이 의미적으로 멀어 재서술이 왜곡을 낳으면, claim_id 인용을 **제거**하고 thinker_id (예: `bandura`) + 주제 키워드만 유지.
> (c) **금지**: 존재하지 않는 claim_id 를 유지 · ES 에 없는 개념을 ES 근거로 인용.

### §3.C (recommended) Coder 산출물·커맨드 요구 명시

**위치**: task-board.md L359 TASK-205-FIX row 말미에 새 줄 추가, 또는 `재검증 의무` 항 뒤.

**현재**: "ES 재질의 결과 (mapping table · diff · curl output) 첨부" 만 언급.

**문제**: "첨부" 의 구체 형태(파일 · 섹션 · 컬럼 구조)가 없어 Coder 산출물의 검증 가능성이 떨어진다. 또한 Manager 가 FIX-T 에서 `_doc/{id}` 전수 재조회를 요구하는데, Coder 가 mapping 산출 시에도 동일 `_doc` 조회를 해야 정확도가 보장되므로 spec 에 명시 필요.

**추가 문구**:

> **Coder report 필수 산출물**:
> 1. **ES mapping table** — 14 thinker × (각 claim_id, claim 요약 40자 이내, keywords 상위 3개) 총 98 rows (14 thinker 전 claim 합계. jinul 9·moore 7·bandura 8·pettit 8·hobbes 8·kant 8·기타 5-7 = **≈98 rows**). 각 thinker 에 대해 `curl -s 'http://localhost:9200/ethics-claims/_search?q=thinker_id:X&size=20&_source=claim,keywords'` 로 1회 수집.
> 2. **replacement diff table** — study-guide 에서 치환된 claim_id 리스트 (before → after · 해당 line · 치환 이유 · match_score). 최소 24건 (Tester §9.1 BUG-001 표 기준), 추가 발견 분 포함.
> 3. **재검증 curl output** — 치환 후 85 claim_id 각각에 대한 `GET /ethics-claims/_doc/{id}` loop 결과: `found=true` 및 content match (§3.A 기준 3+ overlap) 확증. bash loop 예:
>    ```bash
>    for id in $(grep -oE '[a-z_]+-claim-[0-9]+' 2025-B.md | sort -u); do
>      found=$(curl -s "http://localhost:9200/ethics-claims/_doc/$id" | python3 -c "import sys,json; print(json.load(sys.stdin).get('found'))")
>      echo "$id $found"
>    done
>    ```
> 4. **3-step 재측정 수치** — 변경 전 (Step1=124 · Step1b=0 · Step2=28) 대비 변경 후 수치. disjoint ∩=0 재확증.
> 5. **무결 부분 재측정** — `^## 문항 == 11`, em-dash 147 (변경 허용 ±0), ㉠~㉥ 393 (±0), fudge 0, 한자 161 unique tokens (±0), BLOCKER 2명 표기 유지.

---

## 4. 참고 사항 (non-blocking)

### 4.1 Tester §9.1 라인 범위 정정

Manager spec 본문: "§9.1 BUG-001 표 (L195-L232 샘플 24건)". **Reviewer 실측**: §9.1 헤더 L195 · 표 헤더 L203-L204 · 표 **데이터 rows L205-L228** (총 24 rows · 사상가 일부 미매칭 포함) · 표 끝 L228 · 뒤이어 영향·원인·수정제안 L229-L237. Manager 의 "L195-L232" 는 §9.1 섹션 전체 범위 의미로 해석 가능하여 오류라기보다 **표기 모호**. spec 본문에서 "표 rows L205-L228 · 섹션 범위 L195-L237" 로 교체 권고 (blocker 아님).

### 4.2 한자 161 의 정의 명시 권고

Manager · Coder · Tester 모두 "한자 161 unique" 라 기록하나 **문자 기준 unique = 222** · **token 기준 unique = 161**. 측정 방식이 혼동될 여지가 있으므로 spec 에 `python3 -c "import re; ...; tokens=re.findall(r'[\u4e00-\u9fff]+', text); len(set(tokens))"` 와 같이 **token 정의** 를 명시 권고 (blocker 아님).

### 4.3 viroli 처리

Manager spec 은 DQ-021 결과 "pettit 단일 확정 · viroli 폐기" 로 확증했고 2025-B.md 본문에 viroli 인용은 0건 (grep 결과 없음). TASK-205-FIX 수정 범위에서 viroli 는 고려 대상 아님 (이미 TASK-205 에서 해소). FIX spec 에 별도 지시 불필요 (blocker 아님).

---

## 5. 최종 판정

**NEEDS_REVISION**

Manager 가 §3.A · §3.B 2건을 task-board L359 TASK-205-FIX row 에 삽입하면 PASS. §3.C 는 Coder report 검증 가능성 강화를 위한 권고이나 FIX-T 재검증이 이미 동일 검증을 수행하므로 strong recommendation 수준 (PASS 조건에 포함하지는 않음, 그러나 포함 시 FIX-T 가 더 수월해짐).

수정 후 Reviewer 재호출 → PASS 확증 후 Coder 호출 권고.

---

## 6. 금지 사항 준수 확증

- task-board.md 미수정 ✅
- architecture.md 미수정 ✅
- 2025-B.md 미수정 ✅
- Coder/Tester 미호출 ✅
- 다른 프로젝트 경로 미접근 ✅
- 본 보고서만 신규 작성 (`signal/ethics-study/reviewer-report-TASK-205-FIX.md`) ✅
