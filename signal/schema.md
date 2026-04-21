# Signal Board Schema

이 문서는 에이전트 간 통신에 사용되는 시그널 보드 MD 파일의 작성 규칙을 정의한다.
모든 에이전트는 이 스키마를 반드시 준수해야 한다.

---

## 디렉토리 구조 (멀티프로젝트)

```
signal/
├── registry.md                  # 프로젝트 목록 (Manager 전용)
├── schema.md                    # 이 문서 (공용)
└── {project-id}/                # 프로젝트별 네임스페이스
    ├── task-board.md
    ├── done-log.md
    ├── architecture.md
    ├── coder-report.md
    ├── tester-report.md
    ├── coder-report-TASK-*.md   # 병렬 실행 시
    ├── tester-report-TASK-*.md  # 병렬 실행 시
    ├── data-quality-log.md      # 원본 데이터 품질 이슈(TASK-DQ-*) append-only 로그
    └── retrospective.md         # 프로젝트 완료 시

projects/
└── {project-id}/                # 프로젝트별 코드 루트
    ├── src/
    ├── tests/
    └── ...                      # 프로젝트별 구성 (docker-compose, requirements 등)
```

### 경로 규칙
- 모든 시그널 파일 경로는 `signal/{project-id}/`로 시작한다.
- 모든 프로젝트 코드 경로는 `projects/{project-id}/`로 시작한다.
- Manager가 서브에이전트 호출 시 `PROJECT_ID`, `SIGNAL_DIR`, `PROJECT_ROOT` 를 명시한다.
- 서브에이전트는 전달받은 경로만 사용한다.

---

## registry.md

활성 프로젝트 목록을 관리한다. Manager만 수정한다.

### 형식

```markdown
# Project Registry

| ID | Name | Status | Git Branch | Created | Updated |
|----|------|--------|------------|---------|---------|
| my-project | 프로젝트 이름 | ACTIVE | project/my-project | 2026-01-01 | 2026-01-01 |
```

### Status 값
- `ACTIVE` : 진행 중
- `PAUSED` : 일시 중단 (다른 프로젝트 우선 처리 등)
- `DONE` : 모든 태스크 완료, 아카이브 전
- `ARCHIVED` : 아카이브 완료

### 규칙
- Manager만 수정한다.
- 멀티 세션 환경에서 각 세션은 자기 프로젝트의 행만 수정한다.
- 새 프로젝트 등록은 한 세션에서만 수행한다 (동시 추가 금지).

---

## task-board.md

전체 태스크 목록과 상태를 추적하는 중앙 보드. Manager만 수정한다.

### 형식

```markdown
# Task Board

| ID | Title | Assignee | Execution | Status | Priority | Depends On | Created | Updated |
|----|-------|----------|-----------|--------|----------|------------|---------|---------|
| TASK-001 | 태스크 제목 | coder/tester | agent | TODO | HIGH | - | 2026-03-25T10:00 | 2026-03-25T10:00 |
```

### Task ID prefix 규약
- `TASK-{NNN}` — 일반 태스크
- `TASK-DQ-{NNN}` — DATA-QUALITY 태스크 (원본 입력 데이터 품질 이슈). `signal/{project-id}/data-quality-log.md`에 병행 기록.
- 프로젝트 내부에서 `TASK-XXX-YYYY-A`, `TASK-XXX-FIX`, `TASK-XXX-T` 같은 suffix를 쓸 수 있다 (도메인 의존).

### Status 값
- `TODO` : 아직 시작하지 않음
- `IN_PROGRESS` : 서브에이전트가 작업 중
- `DONE` : 완료
- `FAILED` : 실패 (report에 상세 원인 기록)
- `BLOCKED` : 선행 태스크 미완료로 대기

### Execution 값
- `agent` : Manager가 서브에이전트(Coder/Tester)를 통해 자동 실행한다 (기본값).
- `user` : 실 인프라(외부 DB/네트워크/크레덴셜)나 수동 판단이 필요해 사용자가 직접 실행한다.
  - Manager는 `user` 태스크를 자동 실행하지 않는다.
  - Manager는 Step 6(회고) 진입 전에 `user` 태스크를 사용자에게 명시적으로 전달한다.
  - 사용자가 결과를 공유하면 Manager가 수동으로 DONE 처리하고 done-log에 반영한다.

### Priority 값
- `HIGH` : 즉시 처리
- `MEDIUM` : 일반
- `LOW` : 후순위

---

## *-report.md (에이전트별 report 파일)

서브에이전트가 작업 완료 후 Manager에게 보고하는 파일.
서브에이전트는 자신의 report 파일만 수정한다.

### 파일명 규칙

- **순차 실행** (같은 에이전트 유형이 한 번에 하나만 실행): 기본 파일명 사용
  - `signal/coder-report.md`, `signal/tester-report.md`
- **병렬 실행** (같은 에이전트 유형이 동시에 여러 태스크 실행): **태스크 ID를 포함한 파일명** 사용
  - `signal/coder-report-TASK-002.md`, `signal/coder-report-TASK-003.md`
  - Manager가 서브에이전트 호출 시 report 파일 경로를 명시적으로 지정한다.
  - Manager는 결과 확인 후 태스크별 report 파일을 정리(삭제)한다.

### 형식

```markdown
---
agent: coder | tester
task_id: TASK-001
status: DONE | FAILED | BLOCKED
timestamp: 2026-03-25T10:30:00
severity: blocker | bug | observation   # tester report에서만 필수. 코드 이슈/블로커가 없으면 생략 가능하나, 있으면 반드시 명시.
---

## 결과 요약
(무엇을 했는지 1-3줄로 간결하게)

## 변경된 파일
- path/to/file.py (신규|수정|삭제)

## 테스트 결과 (tester 전용)
- 통과: N
- 실패: N
- 실패 상세: (실패한 테스트와 원인)

## 이슈/블로커
(있으면 기술, 없으면 "없음")

## 다음 제안
(Manager에게 제안하는 다음 단계)
```

### 규칙
- frontmatter의 모든 필드는 필수
- timestamp는 ISO 8601 형식
- status는 반드시 task-board.md의 해당 태스크 상태와 일치해야 함
- 순차 실행 시 이전 보고 내용은 덮어쓴다 (최신 보고만 유지)
- 병렬 실행 시 태스크별 report 파일을 사용하여 충돌을 방지한다

### severity 규칙 (tester report 전용)
- `blocker` : 해당 기능/릴리스가 불가능한 치명 결함. 즉시 후속 태스크 필요.
- `bug` : 사양에 어긋나는 코드 결함. 후속 태스크 필요.
- `observation` : 관찰/개선 포인트. Manager 판단에 따라 태스크화 여부 결정.
- **Manager 규칙**: severity가 `blocker` 또는 `bug` 인 report는 **반드시** 후속 태스크를 task-board.md에 등록한다. `observation`은 retrospective 또는 후속 태스크 중 선택.

---

## architecture.md

Manager가 관리하는 프로젝트 설계 문서. Manager만 수정한다.

### 형식

```markdown
# Architecture

## 개요
(프로젝트 목적, 기술 스택, 주요 제약사항)

## 구조
(디렉토리 및 모듈 구조 설명)

## 설계 결정
### [결정 제목]
- 결정: (무엇을 결정했는지)
- 이유: (왜 이렇게 결정했는지)
- 대안: (고려한 대안)

## 현재 상태
(전체 진행 현황 요약)
```

---

## data-quality-log.md

원본 입력 파일(외부 소스, 사용자 제공 원문 등)의 포맷·escaping·누락 등 **코드 결함이 아닌 데이터 품질 이슈**를 추적하는 append-only 로그.
`TASK-DQ-*` prefix 태스크가 발생할 때 Manager가 적재한다.

### 파일명 규칙
- `TASK-DQ-{NNN}`: DATA-QUALITY 태스크 ID. 원본 수정 금지 프로젝트에서도 배치 정정 시점에 일괄 처리 가능하도록 기록만 한다.

### 형식

```markdown
# Data Quality Log

### TASK-DQ-001 - 2026-04-22T01:00
- file: projects/my-project/data/source-2020-B.md
- issue: 원문 Q11에 unescaped `|` 3개 → 파싱 깨짐 (스크립트 row-level fallback으로 복구)
- impact: Section C 원문 셀 표시 부정확. 핵심 집계에는 영향 없음.
- detected_by: Tester TASK-175E-MERGE-T
- resolution: 원본 수정 금지 규정으로 현재는 기록만. 배치 정정 필요.
```

### 규칙
- Manager만 기록한다.
- append-only. 기존 내용 수정/삭제 금지.
- 해결되면 해당 엔트리 하단에 `- resolved_at: YYYY-MM-DDTHH:MM` + `- resolved_by: TASK-XXX`를 추가 (기존 내용은 유지).

---

## done-log.md

완료된 태스크의 히스토리를 시간순으로 누적하는 append-only 로그.
Manager가 태스크를 DONE 처리할 때마다 아래 형식으로 추가한다.
**절대 기존 내용을 삭제하거나 수정하지 않는다.**

### 형식

```markdown
# Done Log

### TASK-001 (DONE) - 2026-03-25T10:30
- title: 로그인 API 구현
- assignee: coder
- summary: JWT 기반 인증 API 구현 완료. handler.py, token.py 신규 작성.
- files: src/auth/handler.py, src/auth/token.py, src/models/user.py

### TASK-002 (DONE) - 2026-03-25T11:00
- title: 인증 API 테스트
- assignee: tester
- summary: 단위 테스트 8개 작성, 7개 통과. token expiry 버그 발견.
- files: tests/test_auth_handler.py, tests/test_token.py
```

### 규칙
- Manager만 기록한다.
- 태스크를 DONE으로 변경하는 시점에 report 내용을 요약하여 추가한다.
- 기존 내용은 절대 수정/삭제하지 않는다 (append-only).
- FAILED 후 재시도하여 DONE이 된 경우에도 기록한다.

---

## retrospective.md

프로젝트 완료 후 Manager가 작성하는 회고 문서.
파이프라인 개선 제안을 포함하며, 사용자 승인 후 프레임워크에 반영된다.
아카이브 시 함께 보관된다.

### 형식

```markdown
# Retrospective

## 프로젝트 요약
- 이름: (프로젝트명)
- 태스크 수: N개 (첫 시도 성공: X, 재시도 필요: Y)
- 세션 수: (추정)

## 잘 된 점
- (구체적으로)

## 문제점
- (무엇이 문제였고 왜 발생했는지)

## 파이프라인 개선 제안
### 제안 1: (제목)
- 대상 파일: (agents/coder.md 등)
- 현재: (지금 상태)
- 제안: (구체적 변경 내용)
- 이유: (왜 필요한지)
```

### 규칙
- Manager만 작성한다.
- 모든 태스크 DONE 이후, 사용자에게 보고하기 전에 작성한다.
- 개선 제안은 사용자 승인 없이 적용하지 않는다.

---

## 공통 규칙

1. **파일 소유권**: 각 에이전트는 자신의 report 파일만 쓴다. task-board.md와 architecture.md는 Manager 전용이다.
2. **덮어쓰기**: 순차 실행 시 report 파일은 매 태스크마다 전체를 덮어쓴다. 병렬 실행 시 태스크별 report 파일을 사용한다. 히스토리가 필요하면 Manager가 판단하여 별도 로그를 남긴다.
3. **읽기 권한**: 모든 에이전트는 모든 signal/ 파일을 읽을 수 있다.
4. **스키마 확장**: 새 에이전트 추가 시 `{에이전트명}-report.md` 파일을 추가하고, 이 문서에 해당 에이전트의 report 규칙을 추가한다.
