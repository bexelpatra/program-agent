# Program Agent

Claude Code 기반 멀티에이전트 오케스트레이션 프레임워크.

사용자가 요구사항을 말하면 **Manager Agent**가 자동으로 설계 → 태스크 분해 → 코딩 → 테스트 → 회고까지 전체 개발 파이프라인을 수행합니다.

## 구조

```
CLAUDE.md              # Manager Agent (오케스트레이션 규칙)
agents/
├── coder.md           # Coder Agent (코드 구현)
└── tester.md          # Tester Agent (테스트 작성/실행)
signal/
├── schema.md          # 시그널 보드 스키마 정의
├── task-board.md      # 태스크 현황 (칸반 보드)
├── done-log.md        # 완료 이력 (append-only)
├── architecture.md    # 프로젝트 설계서
├── coder-report.md    # Coder 작업 보고
└── tester-report.md   # Tester 작업 보고
hooks/
└── user-prompt-submit.sh  # 세션 시작 감지 hook
```

## 동작 방식

1. **사용자**가 자연어로 요구사항 전달
2. **Manager**가 `architecture.md`에 설계 작성
3. **Manager**가 `task-board.md`에 태스크 분해/등록
4. **Manager**가 Agent tool로 **Coder/Tester** 서브에이전트 호출
5. 서브에이전트가 작업 후 `*-report.md`에 결과 보고
6. **Manager**가 결과 판단 → 다음 태스크 진행 또는 재시도
7. 모든 태스크 완료 시 회고 및 개선 제안

### 핵심 특징

- **시그널 보드 기반 통신**: 에이전트 간 소통은 `signal/` 디렉토리의 마크다운 파일로 이루어짐
- **병렬 실행**: 독립적인 태스크는 동시에 실행 가능 (태스크별 report 파일로 충돌 방지)
- **세션 간 연속성**: 세션이 끊겨도 `task-board.md`를 기반으로 작업을 이어갈 수 있음
- **프로젝트 아카이브**: 완료된 프로젝트를 `archive/`에 보관하고 새 프로젝트 시작 가능
- **자기 개선**: 매 프로젝트 종료 시 회고를 통해 프레임워크 자체를 개선

## 사용법

### 1. 설치

```bash
git clone https://github.com/bexelpatra/program-agent.git
cd program-agent
```

### 2. Claude Code 실행

```bash
claude
```

### 3. 요구사항 전달

```
파이썬으로 네이버 증권에서 주요 지표를 크롤링하는 프로그램을 만들어줘.
```

Manager가 자동으로:
- 아키텍처 설계
- 태스크 분해 (코딩, 테스트)
- Coder/Tester 에이전트에 작업 분배
- 결과 검증 및 완료 처리

## 에이전트 확장

새 에이전트를 추가하려면:

1. `agents/{이름}.md` 프롬프트 템플릿 작성
2. `signal/{이름}-report.md` 생성
3. `signal/schema.md`에 report 규칙 추가
4. `CLAUDE.md`의 에이전트 목록에 추가

## 요구 사항

- [Claude Code CLI](https://docs.anthropic.com/en/docs/claude-code) 설치 필요
- Anthropic API 키 또는 Claude Pro/Max 구독

## License

MIT
