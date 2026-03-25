# Signal Board Schema

이 문서는 에이전트 간 통신에 사용되는 시그널 보드 MD 파일의 작성 규칙을 정의한다.
모든 에이전트는 이 스키마를 반드시 준수해야 한다.

---

## task-board.md

전체 태스크 목록과 상태를 추적하는 중앙 보드. Manager만 수정한다.

### 형식

```markdown
# Task Board

| ID | Title | Assignee | Status | Priority | Depends On | Created | Updated |
|----|-------|----------|--------|----------|------------|---------|---------|
| TASK-001 | 태스크 제목 | coder/tester | TODO | HIGH | - | 2026-03-25T10:00 | 2026-03-25T10:00 |
```

### Status 값
- `TODO` : 아직 시작하지 않음
- `IN_PROGRESS` : 서브에이전트가 작업 중
- `DONE` : 완료
- `FAILED` : 실패 (report에 상세 원인 기록)
- `BLOCKED` : 선행 태스크 미완료로 대기

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
