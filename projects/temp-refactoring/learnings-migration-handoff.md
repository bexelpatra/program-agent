---
title: ~/learnings 마이그레이션 + web-automation 통합 핸드오프
created: 2026-04-27
origin_session: 7d3abfaa-a648-4be7-858a-1ff55e92f105
status: in-progress (스캔 완료 · mv 미실행)
owner_session: 다른 세션에서 재개
---

# 핸드오프 — 학습 자료 외부 ~/learnings 통합 마이그레이션

이 문서는 ethics-study 세션에서 진행하다가 컨텍스트 분리를 위해 다른 세션으로 이관하는 작업의 핸드오프이다. 이 문서를 읽은 뒤 곧바로 재개할 수 있도록 작성됨.

## 1. 사용자 요구 (원문)

> "스터디 자료 관련해서 고민해봤는데 ~/에 새로운 경로를 만들자. program_agents 이외에 다른 곳에서도 학습할 자료들이 생겨날것 같아서 거기에 두는게 맞는것 같아. 업무중에 생긴 내용으로 할거니까 ~/learnings로 하고 그 하위에 경로들을 만들자. 예를들어 program_agents/projects/... 이런 경로에서 발생한 학습내용은 ~/learnings/program_agents/projects/... 이런 식으로 해서 모아두도록 하자. 그런 다음 web_auto에서 해당 경로를 심링크하거나 읽어서 자동으로 입력하도록 작업하도록 해볼까 해."

핵심 결정:
- 외부 경로 `~/learnings/` 신설 (program-agent 트리 밖).
- 작업 디렉토리 mirror 구조: `~/program-agent/projects/X/` → `~/learnings/program-agent/projects/X/`.
- web-automation 이 직접 `~/learnings/` 트리를 읽어 포스팅 (옵션 b — `post_loader` 확장).
- staging 디렉토리 불필요. 심링크 불필요.
- 사용자 확정: "좋아 순서대로 진행하자."

## 2. 합의된 4-step 계획

1. **스캔** — `~/program-agent`, `~/ai-agent`, `~/workspace` 에서 학습 후보 추출 후 사용자 승인 대기. ✅ 완료 (3절).
2. **mv** — 사용자 승인 후 `~/learnings/{mirror-path}` 로 이동. ⏸ 대기.
3. **CLAUDE.md 갱신** — `## 블로그 포스팅 규약` 섹션을 외부 `~/learnings` 경로 + staging 없음 + 심링크 없음으로 재작성. ⏸ 대기.
4. **web-automation `LEARNING_ROOTS` 확장** — `post_loader` / `scheduler` 가 외부 root 트리를 직접 스캔하도록 수정. Coder 발주 필요. ⏸ 대기.

## 3. 스캔 결과 (2026-04-27 실측)

`~/program-agent`, `~/ai-agent`, `~/workspace` 모두 존재 확인.

### `~/program-agent/`
- `learnings/ethics-study/2026-04-27-claude-code-multi-agent-retrospective/post.md` (기존 learnings 트리)
- `projects/web-automation/posts/2026-04-26-message-delivery-patterns/post.md`
- `projects/web-automation/posts/2026-04-22-sample/post.md`

### `~/ai-agent/learnings/`
- `architecture/agent-design-and-frameworks.md`
- `architecture/provider-filter-ownership.md`
- `architecture/per-group-local-preamble.md`
- `architecture/claude-code-structure.md`
- `retrospective/ai_사용평가_20260421.md`
- `techniques/snapshot-json-backward-compat.md`
- `techniques/local-model-tool-scoping.md`
- `techniques/python_동시성과_성능.md`
- `techniques/sqlite-type-affinity-migration.md`

### `~/workspace/`
- 학습 후보 파일 0건 (date-slug 디렉토리 · frontmatter md 모두 미검출).

## 4. 미해결 결정 사항 (사용자 확인 필요)

### 4-1. mirror 경로의 `learnings/` 세그먼트 보존 여부

원본 경로가 이미 `learnings/` 를 포함할 때 어떻게 처리?

후보 A — verbatim 보존:
```
~/program-agent/learnings/ethics-study/2026-04-27-...  →  ~/learnings/program-agent/learnings/ethics-study/2026-04-27-...
~/ai-agent/learnings/architecture/agent-design-and-frameworks.md  →  ~/learnings/ai-agent/learnings/architecture/agent-design-and-frameworks.md
```
- 사용자 예시 ("`program_agents/projects/...` → `~/learnings/program_agents/projects/...`") 와 정합.
- 원본 디렉토리 구조 1:1 mirror.

후보 B — `learnings/` 세그먼트 흡수:
```
~/program-agent/learnings/ethics-study/2026-04-27-...  →  ~/learnings/program-agent/ethics-study/2026-04-27-...
~/ai-agent/learnings/architecture/agent-design-and-frameworks.md  →  ~/learnings/ai-agent/architecture/agent-design-and-frameworks.md
```
- 중복 어휘 제거.
- 그러나 사용자 예시와 어긋남.

**제안**: A (verbatim) 가 사용자 예시와 정합. 단, `web-automation/posts/` 의 경우 (이미 `posts/` 컨벤션 사용) `posts/` 도 그대로 유지할지 별도 결정 필요.

### 4-2. `~/program-agent/projects/web-automation/posts/` 처리

해당 디렉토리는 web-automation 자체 입력 경로. 마이그레이션 대상에 포함할지 retain 할지 사용자 확인 필요.

## 5. step 3 (CLAUDE.md 갱신) 적용 범위

현재 `## 블로그 포스팅 규약` (CLAUDE.md L307 부근) 의 변경 항목:
- "저장 위치" 섹션 — `learnings/{project-id}/...` → `~/learnings/program-agent/projects/{project-id}/learnings/...` 또는 mirror 정책에 맞춘 경로로 재작성.
- "심링크" 항목 전체 삭제.
- "아카이브와의 관계" 섹션 — `learnings/` 가 외부에 있으므로 archive 후에도 자연 분리됨을 명문화.

## 6. step 4 (web-automation 확장) 사양 초안

대상: `projects/web-automation/post_loader.py` + `scheduler.py`.

추가 필요:
- `LEARNING_ROOTS` env 또는 settings.yaml 항목 — 외부 root 리스트 (예: `["~/learnings"]`).
- `post_loader.scan()` 가 기존 `posts/` 디렉토리뿐 아니라 `LEARNING_ROOTS` 트리를 walk 해 `post.md` 가 있는 모든 directory 를 등록.
- `.published` / `.draft_id` / `.error` 마커 정책은 외부 root 에서도 동일하게 적용.
- 기존 `posts/` 컨벤션과의 충돌 회피 (동일 slug 중복 등록 금지).

태스크 등록 위치: `signal/web-automation/task-board.md` (해당 프로젝트 시그널 디렉토리 신설 필요할 수 있음).

## 7. 재개 절차 (다른 세션 진입 시)

1. 이 문서를 읽는다.
2. 사용자에게 4-1 (mirror 경로) · 4-2 (web-automation/posts 처리) 두 가지 결정 받는다.
3. step 2 (mv) 실행 — `mkdir -p ~/learnings/{mirror-path}` 후 `mv` 또는 `git mv`.
4. step 3 (CLAUDE.md 갱신) 실행. 다른 세션 영향 가능 — 다중 세션 운영 중인지 사용자에게 확인.
5. step 4 (web-automation 확장) — Coder 발주.

## 8. 주의

- 이 작업 중 ethics-study 세션과 동시 실행 시 `CLAUDE.md` 동시 수정 충돌 주의.
- `~/program-agent/learnings/` 하위에 ethics-study 의 retrospective post 가 이미 존재 — mv 시 ethics-study 세션이 해당 경로를 참조하지 않는지 확인.
- web-automation 의 기존 `posts/` 디렉토리 양식 (`post_loader.py` 검증 규칙 — frontmatter title 필수, ${1} 마커 등) 은 그대로 유지. 외부 root 만 추가 스캔 대상으로.
