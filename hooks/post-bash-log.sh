#!/bin/bash
# PostToolUse hook: Bash tool 실행 후 테스트 결과 로깅
# 테스트 관련 명령어 실행 시 결과를 signal/execution-log.md에 기록
#
# Claude Code hook은 stdin으로 JSON을 받는다:
# { "tool_name": "Bash", "tool_input": { "command": "..." }, "tool_output": "..." }

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')
OUTPUT=$(echo "$INPUT" | jq -r '.tool_output // empty')

# 테스트 관련 명령어인지 확인
IS_TEST=false
case "$COMMAND" in
    *pytest*|*unittest*|*jest*|*mocha*|*go\ test*|*npm\ test*|*cargo\ test*)
        IS_TEST=true
        ;;
esac

if [ "$IS_TEST" = false ]; then
    exit 0
fi

TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%S")
PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
LOG_FILE="$PROJECT_DIR/signal/execution-log.md"

# 로그 파일이 없으면 헤더 생성
if [ ! -f "$LOG_FILE" ]; then
    echo "# Execution Log" > "$LOG_FILE"
    echo "" >> "$LOG_FILE"
fi

# 결과 추가 (최신이 위로)
{
    echo "## $TIMESTAMP"
    echo "- command: \`$COMMAND\`"
    echo "- output:"
    echo '```'
    echo "$OUTPUT" | head -50
    echo '```'
    echo ""
} >> "$LOG_FILE"

exit 0
