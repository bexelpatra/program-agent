#!/bin/bash
# UserPromptSubmit hook: 첫 번째 사용자 입력 시 세션 재개 프로토콜 트리거
#
# 세션에서 이미 초기화가 완료되었는지 확인하고,
# 아직이면 Manager에게 세션 재개 프로토콜을 실행하도록 안내한다.

PROJECT_DIR="/home/jai/program-agent"
INIT_FLAG="/tmp/claude-session-init-$$"

# 이미 이 세션에서 초기화했으면 스킵
if [ -f "$INIT_FLAG" ]; then
    exit 0
fi

# 초기화 플래그 생성
touch "$INIT_FLAG"

# Manager에게 세션 재개 프로토콜 실행을 지시
cat <<'EOF'
{
  "hookSpecificOutput": {
    "hookEventName": "UserPromptSubmit",
    "additionalContext": "세션 시작 감지. CLAUDE.md의 '세션 재개 프로토콜'을 즉시 실행하라. signal/task-board.md, signal/done-log.md, signal/architecture.md를 읽고 현재 상태를 사용자에게 보고한 뒤, 사용자의 입력에 응답하라."
  }
}
EOF
