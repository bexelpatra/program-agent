#!/bin/bash
# PostToolUse hook: Write tool 실행 후 자동 lint
# 환경변수 TOOL_INPUT에서 file_path를 읽어 해당 파일에 lint 실행
#
# Claude Code hook은 stdin으로 JSON을 받는다:
# { "tool_name": "Write", "tool_input": { "file_path": "...", "content": "..." } }

INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

# signal/ 디렉토리 파일은 lint 대상이 아님
if [[ "$FILE_PATH" == *"/signal/"* ]]; then
    exit 0
fi

# src/ 또는 tests/ 하위 파일만 lint 대상
if [[ "$FILE_PATH" != *"/src/"* && "$FILE_PATH" != *"/tests/"* ]]; then
    exit 0
fi

EXTENSION="${FILE_PATH##*.}"

case "$EXTENSION" in
    py)
        if command -v ruff &> /dev/null; then
            ruff check --fix "$FILE_PATH" 2>&1
            ruff format "$FILE_PATH" 2>&1
        elif command -v black &> /dev/null; then
            black "$FILE_PATH" 2>&1
        fi
        ;;
    js|ts|jsx|tsx)
        if command -v eslint &> /dev/null; then
            eslint --fix "$FILE_PATH" 2>&1
        elif command -v prettier &> /dev/null; then
            prettier --write "$FILE_PATH" 2>&1
        fi
        ;;
    go)
        if command -v gofmt &> /dev/null; then
            gofmt -w "$FILE_PATH" 2>&1
        fi
        ;;
esac

exit 0
