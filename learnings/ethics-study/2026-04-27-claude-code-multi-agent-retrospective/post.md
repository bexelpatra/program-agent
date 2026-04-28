---
title: "Claude Code 멀티에이전트로 26개 연도 임용고시 study-guide 자동화하기"
category: "Claude Code"
tags: ["Claude Code", "claude-code", "multi-agent", "AI 에이전트", "오케스트레이션", "회고", "임용고시", "윤리교육", "자동화", "워크플로우"]
---

# Claude Code 멀티에이전트로 26개 연도 study-guide 자동화하기

3일 동안 26개 연도(2014-A ~ 2026-B)의 도덕·윤리 임용고시 학생용 해설서를 한 줄도 직접 타이핑하지 않고 완성했다. 작업의 실체는 단일 LLM 한 명이 다 한 게 아니라, **Manager · Reviewer · Coder · Tester 네 역할의 에이전트가 시그널 보드라는 공유 게시판으로 소통하는 멀티에이전트 파이프라인**이었다. 이 글은 그 구조와, 운영 중에 마주친 5회 반복된 데이터 품질 문제, 그리고 모든 시도가 가치 있었는지에 대한 회고다.

## 무엇을 만들었나

대상은 `ethics-study` 프로젝트의 `exam-solutions/study-guide/{연도}-{시험권}.md`. 한 파일은 보통:

- 한 시험의 11~12 문항을 전부 다룬다
- 각 문항마다 발문 · 제시문 verbatim 인용 · 정답 핵심 개념 · ES(Elasticsearch) 근거 인용 · 채점 기준 · 풀이 과정 7개 섹션을 제공한다
- 평균 700~900 line · em-dash · 한자 · 그리스어 · ㉠~㉥ 같은 특수기호를 byte-level 로 보존한다
- 모든 사상가 인용은 `ethics-thinkers` / `ethics-claims` 두 ES 인덱스에 등록된 claim_id 로만 한다 (인용 1건 = `found=true` 1건)

26개 시험권 × 평균 11.5문항 ≈ **300여 문항**, **20,000라인 이상**의 정합성 있는 텍스트가 산출됐다.

## 4개 에이전트 + 시그널 보드

전체 흐름은 이렇다:

```
사용자 → Manager (오케스트레이터, 본 세션의 Claude Code)
          ├─ Reviewer (Manager 산출물 검증)
          ├─ Coder    (코드/문서 작성)
          └─ Tester   (검증/감수)
              └─ 모두 signal/{project-id}/*.md 파일로 통신
```

핵심 원칙:

1. **모든 통신은 MD 파일로**. 채팅 내용을 에이전트 간에 직접 전달하지 않는다. Manager 가 `task-board.md` 에 태스크를 적고, Coder 가 `coder-report-{TASK-ID}.md` 에 결과를 적는 식. 모든 산출물이 디스크에 남으므로 retroactive 추적이 쉽다.
2. **Reviewer PASS 없이 Coder 호출 금지**. Manager 가 task-board 에 적은 수치(라인 번호 · 문항 개수 · ES 상태 등)를 Reviewer 가 실측으로 재현해서 PASS 받기 전에는 다음 단계로 못 간다. 잘못된 명세로 Coder 가 일단 실행되는 사고를 막는 게이트다.
3. **판단은 Manager 의 몫**. 서브에이전트는 실행만 하고, 결과 해석과 다음 태스크 결정은 항상 Manager 가 한다.

이 구조의 장점은 LLM 환각(hallucination) 으로 잘못된 사실이 흘러들어왔을 때 *어느 단계에서* 들어왔는지를 정확히 짚을 수 있다는 점이다. 실제로 한 번 Coder 가 claim_id 매핑을 헛 만든 사건(BUG-001)이 있었고, 그 발견 자체가 Tester 의 spot-check 검증 단계에서 일어났다.

## 자기검증 프로토콜

Coder 와 Tester 는 산출물을 만들 때 **3-step disjoint 자기검증**을 강제로 통과해야 한다:

| Step | 대상 | 합격 조건 |
|------|------|-----------|
| Step 1 | bare-paren 영문 식별자 (예: `(Kant)`, `(virtue ethics)`) | regex 매치 후 정상 식별자 외 0건 |
| Step 1b | 비-ASCII 학술 용어 (그리스어 · 한자 · 마크론/움라우트) | 본문 출현 vs 사전 등록 일치 |
| Step 2 | TitleCase 사상가 명명 (예: `John Stuart Mill`) | 등록된 thinker_id 와 1:1 |
| **공통** | 세 집합이 pairwise 교집합 = 0 (disjoint) | ∩=0 — 동일 토큰이 두 카테고리에 동시에 속하면 명세 충돌 |

이게 단순 lint 보다 까다로운 이유는 `John Stuart Mill` 이 Step 2 에 잡히면 안 되고, `(Mill)` 이 Step 1 에서 thinker 명에 매칭되면 Step 2 에 또 안 잡혀야 하기 때문이다. ∩=0 자체가 **동일 사상가를 동시에 두 명명 규약으로 표기하지 않았는지**를 보장한다.

추가로:

- **`fudge` 문구 절대 금지** — `≈`, `수렴`, `중복 보정`, `대략`, `얼추`, `거의` 같은 모호 표현이 0-hit 이어야 PASS. AI 가 "그럴듯하게" 보이려고 흘리는 정량 회피 문구를 차단한다.
- **byte-level verbatim 보존** — em-dash(U+2014, hexdump `e2 80 94`), 한자(漢字), 그리스어(εὐδαιμονία), 원형부호(㉠㉡㉢㉣㉤㉥)가 원본 기출 문제 대비 byte ±0 일치해야 한다. 인용을 '예쁘게' 다듬는 LLM 본능을 막는 장치.

## DQ-019부터 DQ-024까지 — 같은 함정에 5번 빠진 이야기

이번 프로젝트에서 가장 많이 배운 패턴은 **데이터 품질 이슈(DATA-QUALITY)와 코드 결함을 분리해서 추적하는 것**의 중요성이다.

상황은 이랬다. coverage 단계 (어떤 사상가가 ES 에 있는지 사전 확인) 결과 "이 사상가는 BLOCKER (ES 미등록)" 으로 분류된 인물이, 막상 study-guide 작성 시점에 다시 `curl localhost:9200` 로 찍어보면 **HTTP 200 으로 멀쩡히 등록되어 있다.** coverage 가 옛날 스냅샷을 본 것이다.

매번 작성 시점에 ES 상태를 재실측해서 override 처리해야 했다. 이게 5회 반복됐다:

| 사건 ID | 영향 사상가 | 발생 연도 |
|---------|-------------|-----------|
| DQ-019 | 2024-A 누락분 | 2026-04-23 |
| DQ-020 | durkheim · hoffman | 2026-04-23 |
| DQ-021 | viroli (별도 폐기 결정) | 2026-04-23 |
| DQ-023 | 2026-A 누락분 | 2026-04-24 |
| DQ-024 | bandura · jinul · pettit · narvaez (4명) | 2026-04-24 |

5회째인 DQ-024 에 와서야 "이건 우리 워크플로우의 구조적 결함이다, 회고 최우선 안건이다" 가 문서화됐다. 더 일찍 깨달았으면 coverage 결과를 매 태스크 시작 시 자동으로 재실측하는 단계를 파이프라인에 넣었을 것이다. 지금은 그게 retrospective 의 1순위 개선안이다.

교훈은 명확하다: **같은 종류의 우회를 두 번 이상 했다면 그건 케이스가 아니라 패턴이다.**

## 동명이인 suffix 라는 작은 함정

존 스튜어트 밀(John Stuart Mill, 19세기 공리주의자) 과 제임스 밀(James Mill, 그의 아버지) 처럼 같은 성을 쓰는 사상가가 등장하면, 한 명은 `mill` thinker_id 를, 다른 한 명은 `mill_js` 같은 suffix 가 붙은 id 를 쓴다. 그런데 claim_id 의 prefix 는 thinker_id 와 다를 수 있다 — 예를 들어 `mill_js` 사상가의 claim 들이 legacy 사정으로 `mill-claim-001`, `mill-claim-002` 로 등록돼 있는 경우다.

이게 왜 문제가 되냐면, Coder 가 "thinker 가 mill_js 면 claim 도 mill_js-claim-* 이겠지" 라고 자연스럽게 추론해서 claim_id 를 잘못 만들면 ES에서 `found=false` 가 잔뜩 나와 인용이 무너진다. 실제로 TASK-205 (2025-B) 에서 이 BUG-001 변종이 발생했고, 그 이후로 architecture.md L491 에 명시적 동명이인 suffix 규약을 박아두고 매 태스크 명세에 "**`mill_js` 사상가의 claim_id prefix 는 `mill-claim-*` 이다**" 같은 명시를 강제하게 됐다.

## 사용자와의 협업 — 어디까지 자동화하고 어디서 멈추나

3일 내내 자동 실행된 게 아니라, 사용자가 정확히 짚어준 지점에서 멈춰서 입력을 받는 패턴이 있었다:

- **새 연도 시작 전**: coverage 파일 갱신 여부, 신규 BLOCKER 정책 (override 할지 N/A 처리할지) 확인
- **severity=bug 이슈 발견 시**: Tester 가 코드 결함을 보고하면 Manager 는 본인이 몰래 처리하지 않고 반드시 task-board 에 FIX 태스크로 등록 (CLAUDE.md 규칙)
- **DQ 5회째 반복 인지 시점**: "이건 회고에 넣어야 한다" 사용자 명시
- **새 프로젝트 (web-automation 연결) 검토 시**: 이번 글처럼 도구 연동 규약을 코드부터 다 같이 읽고 트레이드오프 비교

특히 마지막은 **사용자가 의문을 던지는 방식이 결정 품질을 끌어올린다**는 걸 잘 보여줬다. 처음 내가 제안한 단순한 "직접 web-automation/posts/ 에 저장" 안은 작동은 했겠지만, "어느 프로젝트에서 공부한 건지 섞이게 된다", "아카이브하면 어떻게 되나" 같은 질문이 추가될수록 공유 저장소 + 심링크 + (필요 시) archive 훅 이라는 더 견고한 설계가 나왔다.

## 잘 된 점

1. **시그널 보드의 회복 탄력성**. 세 차례 세션이 컨텍스트 한계로 자동 압축됐는데도 task-board.md / done-log.md 만 다시 읽으면 어느 태스크가 몇 번째까지 완료됐는지 정확히 복원됐다. "세션 재개 프로토콜"이 매번 일관되게 작동.
2. **Reviewer 게이트의 가치**. Coder 호출 전에 Reviewer 가 NEEDS_REVISION 으로 돌려보낸 케이스가 여러 번 있었고, 매번 Manager 의 명세에 실제 측정값과 다른 수치(원문 라인 번호 등)가 섞여 있었다. 게이트가 없었다면 Coder 가 잘못된 라인을 인용하기 시작했을 것.
3. **자기검증 수치의 객관성**. "fudge 문구 0-hit", "Step1=128 · Step1b=3 · Step2=33 · ∩=0" 같은 수치가 매 산출물에 박혀 있어서, 다음 세션에서 봐도 "이건 실제로 검증됐구나" 가 즉시 확인됐다.

## 문제점과 개선 제안

1. **DQ 5회 반복 — 자동 재측정 도입 필요**. coverage 결과를 매 study-guide 태스크 시작 시 자동으로 ES 에 재 sweep 해서 BLOCKER/HIT 차이를 즉시 보고하는 단계를 파이프라인에 추가해야 한다. (1순위)
2. **세션 압축 직후 `/loop` 같은 영속 명령어가 stale 한 상태로 깨어남**. 이번 세션에서도 이미 완료된 TASK-204 를 다시 처리하라는 stale 프롬프트가 발화돼서 한 차례 정리해야 했다. 영속 명령에 "현재 task-board 상태를 먼저 확인하고 obsolete 면 종료" 가드를 기본 내장하면 좋겠다.
3. **동명이인 suffix 같은 도메인 특수 규약은 architecture.md 에 박더라도 매 태스크 명세에 reminder 한 줄 들어가는 게 안전하다**. TASK-205 에서 한 번 무너졌고, 그 이후 모든 태스크에 명시적 reminder 가 들어갔다.

## 다음으로

이 글이 첫 사례인 새로운 워크플로우가 하나 더 생겼다 — **`learnings/{project-id}/{날짜}-{slug}/post.md` 에 회고/학습/사용기를 남기고, 자동 업로드가 필요하면 web-automation 의 `posts/` 폴더에 심링크를 건다.** 프로젝트가 archive 로 이동해도 `learnings/` 는 영속 저장소로 남아 지식이 보존된다.

26개 study-guide 도, 이 회고도, 결국 같은 패턴의 산출물이다: 명확한 명세 → Reviewer 게이트 → 산출 → 자기검증 → 디스크에 모든 흔적이 남는 협업.
