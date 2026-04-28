---
agent: coder(opus)
task_id: TASK-183
status: DONE
timestamp: 2026-04-22
severity: none
---

# Coder Report — TASK-183 (2014-B study-guide 학생용 풀이 가이드)

## 결과 요약

- **생성 파일**: `projects/ethics-study/exam-solutions/study-guide/2014-B.md` (309 lines).
- **문항 구조**: 4문항 전부 커버 (서술형 1·2 + 논술형 1·2), 합계 30점.
  - 서술형 1 (5점, 원문 L16-L28): 국제정치 4대 패러다임 구분 · 경계영역
  - 서술형 2 (5점, 원문 L32-L42): 통일비용·편익 그래프 해독 · 교과교육학
  - 논술형 1 (10점, 원문 L48-L52): 도덕 교과 정당화 · 교과교육학
  - 논술형 2 (10점, 원문 L58-L64): 밀 · 칸트 · 흄 비교 · 사상가형
- **섹션 포맷**: TASK-182(2014-A.md) 선례 그대로 답습. 각 문항당 `발문 / 제시문 verbatim / 정답·핵심 개념 / 관련 ES 근거 / 채점 기준 / 풀이 과정` 6개 서브섹션 모두 구비.
- **4문항 전원 `### 채점 기준` 서브섹션 실재** (완료 조건 7 충족, grep 실측 4건).
- **제시문 verbatim**: coverage/2014-B.md 내 따옴표 구간 + 원본 기출 md 교차 대조로 byte-level 보존. 대괄호 `[S1]·[S2]`, 특수 기호 `A·B·C·D·I·K`, Achtung·sentiment/passion·sympathy·moral sentiment·general point of view 괄호 영문 트레이드마크 모두 유지.

## 논술형 2 ES 매핑 실측 결과

본 세션 curl 실측 (2026-04-22):

**mill_js** — `found=true`, 총 17 claim. 매핑 사용:
- `mill-claim-001` — "쾌락에는 질적 차이가 있으며, 정신적 쾌락은 육체적 쾌락보다 질적으로 우월하다." → 제시문 (가) "양과 질" trademark 직결.
- `mill-claim-003` — "공리의 원리(최대 행복 원리)는 행복을 극대화하는 행위가 도덕적으로 옳다고 규정한다." → (가)→(나) 비판 핵심 원리.
- `mill-claim-014` — "인간의 고차적 능력(이성, 감정, 상상력)의 발휘가 행복의 핵심이며, 이것이 고차 쾌락의 근거이다." → 고차 쾌락 근거.

**kant** — `found=true`, 총 18 claim. 매핑 사용:
- `kant-claim-003` — 정언명법 제1정식(보편법칙 정식) → 보편성 근거 (b).
- `kant-claim-005` — 자율성 · 목적의 왕국 → 보편성 근거 (c).
- `kant-claim-007` — 도덕법칙은 모든 이성적 존재에 타당 · 경험에서 도출 불가 → 보편성 근거 (a).
- `kant-claim-008` — 경외(Achtung)가 도덕의 유일한 동기 → 제시문 (나) "존경심·외경심" trademark 직결.
- `kant-claim-009` — 도덕법칙은 순수 실천이성의 사실 → 실천이성의 보편성.

**hume** — `found=true`, 총 10 claim. 매핑 사용:
- `hume-claim-004` — 이성만으로 도덕 판단 불가 · 감정(sentiment/passion) 기초 → 제시문 (다) "판단된다기보다 느껴진다" trademark 직결.
- `hume-claim-010` — 공감(sympathy)이 도덕 평가의 핵심 메커니즘 · 덕/악덕 식별 기초 → 흄 보편성 근거의 중심.

## 서술형 1·2 + 논술형 1 ES 근거 표기

완료 조건 6에 따라 해당 3문항은 다음과 같이 명시:
- 서술형 1 → "해당 없음 (경계영역 · 국제정치학 4대 패러다임 구분은 ES 사상가 매핑 대상 아님)" (draft L49)
- 서술형 2 → "해당 없음 (교과교육학 · 통일·평화 교육과정)" (draft L93)
- 논술형 1 → "해당 없음 (교과교육학 · 도덕과교육학 교과 정당화론)" (draft L157)

## 자기검증 2단계 결과

### Step 1 — 괄호 안 영어-시작 토큰 (draft 산출물)

```bash
grep -oE '\([A-Za-z][^)]*\)' projects/ethics-study/exam-solutions/study-guide/2014-B.md | sort -u
```

추출된 영어-시작 괄호 토큰 중 **원문 인용 관련 토큰(coverage 역grep 대상)**:

| 토큰 | coverage hit (grep -Fc) | 처리 |
|------|-------------------------|------|
| `(Achtung)` | 1 | 유지 |
| `(J.S. Mill)` | 1 | 유지 |
| `(Kohlberg·Piaget 도덕발달론 전제)` | 1 | 유지 (coverage 표기와 일치시키기 위해 초기 드래프트 "Kohlberg · Piaget 도덕발달론이 공유하는 전제"를 수정) |
| `(Morgenthau·Waltz·Keohane·Wallerstein·Wendt 등)` | 1 | 유지 (가운뎃점 공백 제거 수정) |
| `(constructivism)` | 1 | 유지 |
| `(liberalism)` | 1 | 유지 |
| `(moral sentiment)` | 1 | 유지 |
| `(realism)` | 1 | 유지 |
| `(social capital)` | 1 | 유지 |
| `(sympathy)` | 2 | 유지 |
| `(world-system/dependency)` | 1 | 유지 |

**메타·구조 토큰 (0-hit이지만 역검증 대상 아님)**:

| 토큰 | 분류 | 이유 |
|------|------|------|
| `(A)` `(D 또는 C)` | 제시문·그림 레이블 | 제시문 verbatim 내 도표 레이블 |
| `(L1~L97)` `(L523~L638)` `(coverage/... 근거)` | 내부 라인/파일 참조 메타 | 산출물 메타 서술 |
| `(a)` `(b)` `(c)` | 번호 매김 | 본문 구조 표기 |
| `(S1, S2, 통일비용, 통일편익)` | 발문 필수 용어 목록 | coverage L34 S1·S2·통일비용·통일편익 각 토큰은 1+ hit 실재 |
| `(TASK-182 산출물)` `(mill_js · kant · hume 3 사상가 ...)` | 태스크/요약 메타 | 본문 참조 서술 |

### Step 2 — 대문자 시작 영어 단어 (draft 산출물)

```bash
grep -oE '[A-Z][A-Za-z][a-zA-Z]+' projects/ethics-study/exam-solutions/study-guide/2014-B.md | sort -u
```

**전수 13개, 모두 coverage 1+ hit 확증**:

| 토큰 | coverage hit | 비고 |
|------|--------------|------|
| Achtung | 1 | coverage L62 (kant trademark) |
| Bentham | 1 | coverage L60 (밀과 대비) |
| Keohane | 1 | coverage L23 (자유주의 이론가) |
| Kohlberg | 1 | coverage 도덕발달론 전제 |
| Mill | 3 | coverage 다수 |
| Morgenthau | 1 | coverage L23 (현실주의) |
| NGO | 1 | 자유주의 행위자 |
| Phase | 2 | architecture.md 참조 메타 (coverage L6·L17 실재) |
| Piaget | 1 | coverage |
| TASK | 1 | 태스크 ID 메타 |
| Wallerstein | 1 | coverage L23 (세계체제론) |
| Waltz | 1 | coverage L23 (현실주의) |
| Wendt | 1 | coverage L23 (구성주의) |

Step 2 **0-hit 0건 확증**.

### 처리 결과 표 (초기 드래프트 vs 최종본)

초기 드래프트에서 coverage 역검증 0-hit이 발견된 4개 토큰 수정 이력:

| 초기 표기 | 0-hit 원인 | 처리 | 최종 표기 |
|-----------|------------|------|-----------|
| `주권 국가(state)` | coverage에 `(state)` 부재 | 괄호 영문 제거, 한글 단독 | `주권 국가` |
| `중심-주변(core-periphery)` | coverage에 `(core-periphery)` 부재 | 괄호 영문 제거, 한글 단독 | `중심-주변` |
| `자율성(Autonomie)는 도덕법칙의 최고 원리` | coverage에 `(Autonomie)` 부재 | 괄호 영문 제거 | `자율성은 도덕법칙의 최고 원리` |
| `경외(Achtung, 존경/경외감)` | 정확 매치 부재 (`Achtung` 단독은 1 hit) | 내부 설명 제거 | `경외(Achtung)` |
| `Morgenthau · Waltz · Keohane · Wallerstein · Wendt 등` (공백 포함) | coverage는 공백 없는 가운뎃점 | 공백 제거 | `Morgenthau·Waltz·Keohane·Wallerstein·Wendt 등` |
| `Kohlberg · Piaget 도덕발달론이 공유하는 전제` | coverage 표기 불일치 | coverage 표기 준수 | `Kohlberg·Piaget 도덕발달론 전제` |
| `일반적 관점(general point of view)` | coverage는 괄호 없이 가운뎃점 구조 | 가운뎃점 구조로 교체 | `일반적 관점·general point of view` |

재검증 후 Step 1 원문-인용 관련 영어 토큰 전수 1+ hit, Step 2 대소문자 단어 전수 1+ hit 확증.

## 완료 조건 체크리스트 대조

| 조건 | 충족 여부 | 근거 |
|------|-----------|------|
| 1. 파일 신규 생성 | ✅ | `projects/ethics-study/exam-solutions/study-guide/2014-B.md` 309 lines |
| 2. 4문항 전부 커버 | ✅ | `grep -cE '^## 문항' = 4` |
| 3. 원문 line metadata 기재 | ✅ | 서술형 1 (L16-L28), 서술형 2 (L32-L42), 논술형 1 (L48-L52), 논술형 2 (L58-L64) |
| 4. 제시문 verbatim byte-level 일치 | ✅ | 대괄호·괄호 영문·특수 기호 전수 보존 (`[S1]`, `[S2]`, `A·B·C·D·I·K`, `(Achtung)` 등) |
| 5. 논술형 2 ES 근거 (mill_js·kant·hume 각 thinker_id + claim_id ≥ 1) | ✅ | mill_js 3 claim / kant 5 claim / hume 2 claim 매핑 |
| 6. 서술형 1·2 + 논술형 1 ES 근거 표기 | ✅ | "해당 없음" 표기 + 분류 사유 명시 |
| 7. 4문항 전원 `### 채점 기준` 실재 | ✅ | `grep -c '### 채점 기준' = 4` |
| 8. 자기검증 2단계 결과 3개 표 coder-report 포함 | ✅ | 본 report "자기검증 2단계 결과" 섹션 |

## Observation

- 본 시험(2014-B)은 4문항 중 **사상가형이 1문항(논술형 2)**에 불과하다. 나머지 75%는 교과교육학·경계영역으로, ES 사상가 매핑이 적용되지 않는 영역이다. 학생용 가이드 상단의 "ES 등록 상태 요약" 표에서 이를 명시했다.
- 코딩 과정에서 0-hit 토큰 처리 이력 7건은 모두 **draft 본문 자체가 coverage를 넘어선 해설을 풀어쓰는 과정에서 발생한 영문 병기**였다. 실질 내용 변경 없이 표기 조정으로 해결 가능했으며, coverage를 정답 근거로 삼는 원칙에서 벗어난 부분은 없다.
- `Phase` 단어는 초기 드래프트의 "Phase 6 기출 작업 규칙"(architecture.md 참조 메타) 표기에서 등장하며, coverage L6·L17에도 동일 맥락으로 실재하므로 유지했다.

## 본 세션 주요 파일 Read/Bash 감사 로그

| 경로/명령 | 목적 |
|-----------|------|
| `study-guide/2014-A.md` (전체) | 선례 포맷 전수 참조 |
| `coverage/2014-B.md` (전체) | 제시문·ES 매핑·분류 원천 |
| `/home/jai/잡동사니/임용/md/2014중등1차-3교시-도덕윤리-전공B-문제지-최종.md` (전체) | 원본 기출 byte-level 대조 |
| `curl http://localhost:9200/ethics-claims/_search?q=thinker_id:mill_js` | mill_js 17 claim 실측 |
| `curl http://localhost:9200/ethics-claims/_search?q=thinker_id:kant` | kant 18 claim 실측 |
| `curl http://localhost:9200/ethics-claims/_search?q=thinker_id:hume` | hume 10 claim 실측 |
| `grep -oE '\([A-Za-z][^)]*\)' draft \| sort -u` | 자기검증 Step 1 |
| `grep -oE '[A-Z][A-Za-z][a-zA-Z]+' draft \| sort -u` | 자기검증 Step 2 |
| `grep -Fc "$tok" coverage` | 각 토큰 역grep case-sensitive 실측 |
