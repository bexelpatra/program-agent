---
task_id: TASK-212-04
verdict: NEEDS_REVISION
---

# Reviewer Report: TASK-212-04 (zhiyi ES 등록)

## 검증 대상
- 파일:
  - `signal/ethics-study/task-board.md` L379 (TASK-212-04 spec)
  - `projects/ethics-study/exam-solutions/coverage/2022-A.md` (102 lines)
  - `projects/ethics-study/exam-solutions/coverage/2025-A.md` (681 lines)
  - `projects/ethics-study/exam-solutions/study-guide/2022-A.md` (1027 lines)
  - `projects/ethics-study/exam-solutions/study-guide/2025-A.md` (705 lines)
  - `signal/ethics-study/blocker-log.md` (1139 lines)
  - `signal/ethics-study/data-quality-log.md` (DQ-027 = regan, DQ-028 next)
  - `projects/ethics-study/scripts/insert_pettit.py` / `insert_singer.py` / `insert_cho_sik.py` / `insert_schumpeter.py`

- Manager 주장 요약:
  1. zhiyi 출제 row 2회 (2022-A Q10·2025-A Q8). 2022-B 는 false-positive.
  2. 메타: id=zhiyi / field=eastern_ethics / era=고대 / 538-597.
  3. trademark 6종 (삼제원융 / 일심삼관 / 오시 / 화법4교 / 화의4교 / 일념삼천).
  4. 출처 인용 line: coverage/2022-A.md L121-L140, coverage/2025-A.md L138-L165, coverage/2025-A.md L341-L347, blocker-log L726-L734, L976-L982.
  5. study-guide BLOCKER 정정 line: 2022-A 6 곳 (L20·L715·L752·L772·L788·L1002), 2025-A 7 곳 (L19·L40·L50·L52·L415·L434·L445).
  6. claim_id ≥6 권장.
  7. DQ-028 next-numbered.

## 검증 결과

### 파일 존재
| 경로 | 존재 | 비고 |
|------|------|------|
| `signal/ethics-study/task-board.md` | ✅ | TASK-212-04 L379 IN_PROGRESS |
| `projects/ethics-study/exam-solutions/coverage/2022-A.md` | ✅ | **102 lines** |
| `projects/ethics-study/exam-solutions/coverage/2025-A.md` | ✅ | 681 lines |
| `projects/ethics-study/exam-solutions/study-guide/2022-A.md` | ✅ | 1027 lines |
| `projects/ethics-study/exam-solutions/study-guide/2025-A.md` | ✅ | 705 lines |
| `signal/ethics-study/blocker-log.md` | ✅ | 1139 lines |
| `signal/ethics-study/data-quality-log.md` | ✅ | DQ-027 L578 (regan) — DQ-028 next |
| `scripts/insert_pettit.py` | ✅ | 54490 bytes |
| `scripts/insert_singer.py` | ✅ | 62164 bytes |
| `scripts/insert_cho_sik.py` | ✅ | 45274 bytes |
| `scripts/insert_schumpeter.py` | ✅ | 50973 bytes |

### 내용 일치

#### ❌ [선행 자료 line 인용 오류 1] coverage/2022-A.md L121-L140 — **파일 범위 초과**
- 주장: "coverage/2022-A.md L121-L140 (Q10 분석 verbatim)"
- 실제: 파일은 **102 lines**. L121-L140 은 존재하지 않음 (`wc -l` 실측 = 102).
- 실제 Q10 zhiyi 분석 위치: **L24** (단일 row · 한 줄에 trademark 3중 일치 분석 압축).
- 추정: Manager 가 인용한 "L121-L140" 은 study-guide/2022-A.md 원문 line 번호 (또는 원본 기출 md 의 L121-L140) 를 coverage 의 line 번호로 혼동한 것으로 보임. coverage/2022-A.md L24 row 내부 인용 표기 "(L129)·(L133)·(L135)" 는 study-guide/2022-A.md (또는 원본 기출 md) 의 source line 좌표.
- 근거: `wc -l projects/ethics-study/exam-solutions/coverage/2022-A.md` → 102. `grep -nE "천태\|智顗\|zhiyi" coverage/2022-A.md` → L24, L38, L39, L46, L65-L67, L90, L97 (본문 trademark 분석은 L24 단일 셀).

#### ❌ [선행 자료 line 인용 오류 2] coverage/2025-A.md L138-L165 — **다른 문항 영역**
- 주장: "coverage/2025-A.md L138-L165 (Q8 본문 verbatim)"
- 실제: coverage/2025-A.md L138-L165 은 **Q4 통일교육(민족대단결·통일헌법·남북한 통일방안)** 영역. zhiyi Q8 분석 영역이 아님.
  - L138 = "**확정 근거**:" (Q4 통일방안 분석 시작)
  - L141 = "▶ 답: ㉠ = 민족대단결(民族大團結)"
  - L165 = "(가)는 직소 Ⅰ(Jigsaw Ⅰ) 모형에 대한 설명…" (Q5 시작)
  - **Q8 zhiyi 헤딩 위치**: `## Q8 [4점] (L136)` = coverage/2025-A.md **L333**.
  - **실제 Q8 trademark 분석 영역**: coverage/2025-A.md **L333-L375** (사상가·학파·주제 = L345 / 한자·개념 병기 = L347 / 근거 ① ② ③ ④ ⑤ = L350-L354 / row-by-row 표 = L370-L374 / ES 실존 = L376-L378).
- 보조 근거: 추정컨대 Manager 의 "L138-L165" 는 **study-guide/2025-A.md** 원문 (또는 원본 기출 md) 의 Q8 본문 line 좌표를 coverage 좌표로 혼동. coverage 분석 본문은 trademark 분석 시 study-guide L140·L142 를 inline source 로 인용함.
- 근거: `sed -n '136,170p' coverage/2025-A.md` → "남한 통일방안 … 민족대단결". `grep -nE "Q8 \|천태\|智顗" coverage/2025-A.md` → L333 (Q8 heading), L345 (사상가·학파·주제), L370-L374 (row-by-row).

#### ✅ [선행 자료 line 인용 정확 1] coverage/2025-A.md L341-L347 — **사상가 메타 verbatim**
- 주장: "coverage/2025-A.md L341-L347 (사상가 메타 verbatim)"
- 실제: L341 (원문 인용), L345 (사상가·학파·주제 = "지의(智顗, Zhiyi, 538-597, 수나라 승려, 천태지의 대사")"), L347 (한자·개념 병기 list with 一念三千).
- 합치: ✅ 정확. 사상가 메타 verbatim 영역.

#### ✅ [선행 자료 line 인용 정확 2] blocker-log.md L726-L734 — **BLK-175E-2022A-006**
- 주장: "blocker-log.md L726-L734 (BLK-175E-2022A-006)"
- 실제: L728 = "### BLK-175E-2022A-006 (TASK-175E-2022-A) — Q10 (나) 천태 지의(天台 智顗) ES 미등록", L731 = trademark 3중 일치 분석, L733 = 후속 조치 zhiyi 등록 권고.
- 합치: ✅ 정확.

#### ✅ [선행 자료 line 인용 정확 3] blocker-log.md L976-L982 — **BLK-175E-2025A-004**
- 주장: "blocker-log.md L976-L982 (BLK-175E-2025A-004)"
- 실제: L979 = "### BLK-175E-2025A-004 (TASK-175E-2025-A) — Q8 천태 지의(天台 智顗) ES 미등록 (row 기준 3회째 출제)", L981-L982 = 사유·후속 조치.
- 합치: ✅ 정확.

#### ✅ [study-guide/2022-A.md BLOCKER 6 line 정확] L20·L715·L752·L772·L788·L1002
- L20: `⚠️ ES 미등록 (4명 — BLOCKER 유지) | green_th · shenxiu · zhiyi · beccaria` ✅
- L715: `## 문항 10 · … · 신수(BLOCKER) + 혜능 + 지의(BLOCKER)` ✅
- L752: `(나) 사상 identification: 지의(智顗 — zhiyi …) (⚠️ BLOCKER BLK-175E-2022A-006 / ES 미등록)` ✅
- L772: `⚠️ zhiyi: ES 미등록(BLK-175E-2022A-006). 교과서 …` ✅
- L788: `(나) 사상 확정: … 천태종 지의의 교판론. (⚠️ 지의는 BLK-175E-2022A-006)` ✅
- L1002: `⚠️ 잔존 BLOCKER (4명): green_th · shenxiu · zhiyi · beccaria` ✅
- ⚠️ **누락 추정 (정정 잠재 후보)**: L23 (HTML 주석 `<!-- DQ-016 override … green_th/shenxiu/zhiyi/beccaria 4건만 BLOCKER 표기 유지 -->`) + L41 (`잔존 BLOCKER는 4건(green_th·shenxiu·zhiyi·beccaria)이며 …`). 두 줄 모두 zhiyi BLOCKER 상태 텍스트 — DQ-028 override 후 정합 갱신 시 함께 정정 권장. Coder 가 일관성 유지 차원에서 함께 수정해야 하나 spec 에 명시 부재.

#### ✅ [study-guide/2025-A.md BLOCKER 7 line 정확] L19·L40·L50·L52·L415·L434·L445
- L19: `⚠️ ES 미등록 (1건 — BLOCKER 유지) | zhiyi (Q8 · BLK-175E-2025A-004)` ✅
- L40: `… ES 등록 13명 + 잔존 BLOCKER 1명 zhiyi …` ✅
- L50: `### zhiyi BLOCKER 유지 — Q8 천태종 trademark 직접 인용 금지` ✅
- L52: `Q8 zhiyi: 본 세션 2026-04-23 curl … HTTP 404 … BLK-175E-2025A-004 유지` ✅
- L415: `## 문항 8 · 서술형 · 4점 · 원문 line L136—L148 · ⚠️ BLOCKER (BLK-175E-2025A-004 유지)` ✅
- L434: `⚠️ BLOCKER 유지 (BLK-175E-2025A-004): 본 문항의 종파 … 智顗 … 미등록 …` ✅
- L445: `⚠️ zhiyi — BLOCKER (BLK-175E-2025A-004): ethics-thinkers 인덱스에 미등록 …` ✅

#### ⚠️ [study-guide/2025-A.md "손대지 말 것" 5 line — 부분 부정확]
- L435 (천태종 / 지의 trademark 본문 시작 줄) ✅ 본문 trademark — 손대지 말 것 정확.
- L441 (한자·개념 병기 list with 智顗) ✅ 본문 trademark — 손대지 말 것 정확.
- L458 (1. 종파 특정 — 천태종 trademark 풀이) ✅ 본문 trademark — 손대지 말 것 정확.
- L386 ❌ **zhiyi 무관**. 실제 내용: `**㉣ 신독 내용 서술 ('~ 조심한다' 형식)**: "남이 알지 못하는 자기 마음속의 (상제 앞에 드러나는) 은미한 기미…` — **정약용(jeong_yagyong) Q7** 신독 분석. zhiyi trademark 인용 줄 아님. (해 없음 — Coder 가 zhiyi 작업 범위 밖이므로 어차피 손대지 않음. spec 의 사실관계 오류만)
- L618 ❌ **zhiyi 무관**. 실제 내용: `**`rawls` (John Rawls) — HIT (15 claims)**: rawls-claim-001~015. 핵심 claim …` — **롤스 ES 근거 줄**. zhiyi 무관.
- 영향: 안전상 무해 (Coder 가 zhiyi 무관 줄을 수정할 이유 없음) 하나 spec 의 line# 사실 인용이 부정확하다는 측정 가능한 오류.

### 태스크 완결성

#### ✅ Coder 가 외부 질문 없이 실행 가능한가?
- spec 자체에 trademark 6종 verbatim 인용 + claim_id 6건 안 + 메타 (id·field·era·birth·death) 명시 + reference 스크립트 4건 모두 exists.
- coverage line# 일부 부정확하나 spec 본문에 verbatim 직접 인용 ("( ㉠ )은/는 하나의 진리이면서 셋도 아니고 …") 이 그대로 들어 있어 Coder 가 line 좌표 없이 grep 으로 찾을 수 있음.
- ⚠️ 그러나 "실측 인용 의무" (CLAUDE.md Step 2 규정) 위반 — Manager 가 "L121-L140 grep 실측" 을 주장했으나 해당 line 은 **파일에 존재조차 하지 않음**. Coder 가 이 line# 을 신뢰하고 grep 하면 0-hit 또는 다른 문항 영역을 읽는다.

#### ✅ 완료 조건 측정 가능
- (1) ES `_doc/zhiyi` HTTP 200 + `claims?q=thinker_id:zhiyi` total≥6 → curl 측정 가능.
- (2) study-guide 13 line BLOCKER 정정 → grep 측정 가능 (단, line# 정정 필요는 위와 같이 정확).
- (3) DQ-028 entry append → grep 측정 가능.
- (4) Coder report 자기검증 표 → 산술 검증 가능.

#### ✅ 검증 명령어 실행 가능
- `curl http://localhost:9200/ethics-thinkers/_doc/zhiyi`
- `curl http://localhost:9200/ethics-claims/_search?q=thinker_id:zhiyi`
- `grep -nE "zhiyi\|BLK-175E" study-guide/{2022-A,2025-A}.md` — 모두 실행 가능.

### 의존성·순서

#### ✅ TASK-212-03 (regan) DONE
- task-board.md L378 = `TASK-212-03 | … DONE 2026-04-28T12:21 …`. ✅ TASK-212-04 IN_PROGRESS 정상.

#### ✅ 같은 파일 수정 IN_PROGRESS 충돌 없음
- task-board.md grep `IN_PROGRESS` → TASK-212-04 단일.
- TASK-212-04 가 수정할 파일 (study-guide/2022-A.md · study-guide/2025-A.md · scripts/insert_zhiyi.py · data-quality-log.md) 가 다른 IN_PROGRESS 태스크와 겹치지 않음.

#### ✅ DQ-028 next-numbered
- data-quality-log.md grep `^## DQ-027` → L578 (regan post-registration override · TASK-212-03). DQ-028 next 정확.

### 목적성·클린 아키텍처·분리

#### ✅ 목적성
- TASK-212 (mother): "잔존 미등록 사상가 ES 등록 시리즈". TASK-212-04 = zhiyi 단일 사상가 1태스크 — 순수 봉사 항목. 범위 밖 요소 없음.

#### ✅ 클린 아키텍처
- 생성 파일: `scripts/insert_zhiyi.py` (data layer · ES write). 수정 파일: 2 study-guide md (BLOCKER 표기 정정) + data-quality-log.md (append). 디렉토리 위치 부합.
- 의존 방향 위반 없음.

#### ✅ 소스·함수 분리
- 단일 사상가 1태스크 — 책임 단일 (ES `_doc/zhiyi` 1건 + claims ≥6 + 2 study-guide 정정 + DQ-028).

#### ✅ 이름·인터페이스
- id=`zhiyi` (단일·동명이인 충돌 없음 — feedback_thinker_id_taylor 규약 적용 불필요).
- claim_id naming 일관 (zhiyi-claim-001~006).

#### ✅ field 표준 부합
- `eastern_ethics` ∈ ethics-fields 7건 (curl 실측 — civic_edu / eastern_ethics / moral_development / peace_studies / political_philosophy / unification_edu / western_ethics). ✅

#### ✅ 한자 verbatim 보존 명시
- spec 에 한자 일관 병기 (智顗·天台·三諦圓融·一心三觀·摩訶止觀·法華玄義 등) 명시.

#### ✅ fudge 금지 / fabrication 방지 명시
- spec 마지막 조항: "자기검증 3-step (Step1+Step1b+Step2 ∩=0)" 적시. agents/coder.md 기본 원칙으로 fabrication 방지 자동 적용.

#### ✅ 추후 수정 용이성
- 단일 사상가 단위 — 향후 fazang·berlin 등 다른 사상가 추가도 동일 패턴 (insert_{id}.py + study-guide 정정 + DQ-NNN). 재설계 필요 없음.

## 판정
**NEEDS_REVISION** (line# 좌표 정정만 — 가벼운 수정. 의미 변경 없음. R2 면제 권고 가능 (regan 선례))

## 수정 요청 (NEEDS_REVISION 시)

### [필수 1] 선행 자료 line# 정정 (실측 좌표로 교체)
- spec 본문 "**선행 자료**" 절:
  - **변경 전**: `coverage/2022-A.md` **L121-L140** (Q10 분석 verbatim)
  - **변경 후**: `coverage/2022-A.md` **L24** (Q10 row · 단일 셀 · trademark 3중 일치 분석. "L121-L140" 은 study-guide/2022-A.md 또는 원본 기출 md 의 source line 좌표였음)
  - **변경 전**: `coverage/2025-A.md` **L138-L165** (Q8 본문 verbatim)
  - **변경 후**: `coverage/2025-A.md` **L333-L375** (Q8 trademark 분석 영역. heading=L333 / 사상가·학파·주제=L345 / 한자·개념 병기=L347 / 근거 ① ② ③ ④ ⑤ = L350-L354 / row-by-row 표 L370-L374. study-guide/2025-A.md 의 Q8 source line 은 별개)
  - `coverage/2025-A.md` **L341-L347** 은 그대로 유지 ✅
  - blocker-log L726-L734 / L976-L982 는 그대로 유지 ✅
- spec 본문 "**trademark (출처 verbatim · …)**" 의 출처 표기 절도 동일 정정 — `coverage/2022-A.md L121-L140` → `coverage/2022-A.md L24` / `coverage/2025-A.md L138-L165` → `coverage/2025-A.md L333-L375`.

### [선택 2 — 권장] 2022-A study-guide 정정 line 보강
- 현재 spec 6 line (L20·L715·L752·L772·L788·L1002) 외에 zhiyi 텍스트 잔존 2 line 추가 권장:
  - **L23**: `<!-- DQ-016 override: … green_th/shenxiu/zhiyi/beccaria 4건만 BLOCKER 표기 유지. -->` (HTML 주석)
  - **L41**: `… 잔존 BLOCKER는 4건(green_th·shenxiu·zhiyi·beccaria)이며, 모두 …`
- 두 줄 모두 BLOCKER 4명 통계 텍스트 — DQ-028 override 후 zhiyi 제외하여 "BLOCKER 3건 (green_th · shenxiu · beccaria)" 으로 재계산하지 않으면 study-guide 내부 정합 깨짐. Coder 가 일관성 차원에서 함께 정정해야 함.
- 미보강 시 Tester 가 정합 검증에서 잔존 zhiyi BLOCKER 표기를 잡아낼 수 있음 (severity=observation 가능성).

### [선택 3 — 권장] 2025-A "손대지 말 것" 5 line 정정
- L435·L441·L458 ✅ 그대로 유지 (실제 본문 trademark 인용 줄).
- L386 (정약용 신독 줄)·L618 (롤스 줄) **삭제 또는 zhiyi 무관 명기**. 안전상 무해하나 spec 의 사실 인용 정확성 향상.

## Manager에게 전달
- **R2 면제 권고**: Manager 의 spec 본문은 6 trademark + 6 claim_id + 메타·field·era·birth/death 모두 정확하며, 실제 verbatim 인용 텍스트가 spec 안에 그대로 들어 있어 Coder 가 line# 없이도 grep 으로 위치 특정 가능. 수정 요청 [필수 1] 은 line# 좌표 교체로 의미 변경 0 — regan 선례 (TASK-212-03) 와 같이 R2 면제 후 line# 정정만 반영 후 IN_PROGRESS 유지하고 Coder 호출해도 좋음.
- 수정 요청 [선택 2·3] 은 권고 — 미반영 시 Tester observation 으로 잔존 가능. Manager 판단으로 spec 에 반영 여부 결정.
- 모든 다른 검증 항목 (BLOCKER 13 line · DQ-028 next · TASK-212-03 DONE · field 표준 · 4 reference 스크립트 exists · IN_PROGRESS 충돌 없음 · 한자 verbatim · fudge 방지) 통과.
