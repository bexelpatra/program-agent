#!/usr/bin/env bash
# 티스토리 폴더 기반 임시저장 스모크 테스트 wrapper
#
# 사용법:
#   ./scripts/smoke_tistory_post.sh [폴더경로]
#   - 인자 없으면 posts/2026-04-22-sample/ 사용.
#
# 종료 코드:
#   0 = 임시저장 완료 (.published 마커 기록)
#   1 = skip (.published 이미 존재)
#   2 = 로그인/설정/실행 예외 (.error 마커 참조)

set -euo pipefail

# DISPLAY 없고 xvfb-run 있으면 자동 래핑
if [ -z "${DISPLAY:-}" ] && [ -z "${_WA_SMOKE_XVFB_WRAPPED:-}" ]; then
    if command -v xvfb-run >/dev/null 2>&1; then
        echo "[스모크] DISPLAY 미설정 + xvfb-run 감지 → 자동 래핑 실행"
        export _WA_SMOKE_XVFB_WRAPPED=1
        exec xvfb-run -a "$0" "$@"
    fi
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

echo "[스모크] 프로젝트 루트: $PROJECT_ROOT"

# .env 로드 + 4필드 검증
if [ ! -f ".env" ]; then
    echo "[스모크][ERROR] .env 없음. cp .env.example .env 후 값을 채우세요."
    exit 1
fi
set -a; source .env; set +a

missing=()
[ -z "${WA_ACCOUNT_EMAIL:-}" ]       && missing+=("WA_ACCOUNT_EMAIL")
[ -z "${WA_ACCOUNT_PASSWORD:-}" ]    && missing+=("WA_ACCOUNT_PASSWORD")
[ -z "${WA_NAVER_IMAP_EMAIL:-}" ]    && missing+=("WA_NAVER_IMAP_EMAIL")
[ -z "${WA_NAVER_IMAP_PASSWORD:-}" ] && missing+=("WA_NAVER_IMAP_PASSWORD")
if [ ${#missing[@]} -gt 0 ]; then
    echo "[스모크][ERROR] .env 에서 다음 필드가 비어있습니다:"
    for f in "${missing[@]}"; do echo "                - $f"; done
    exit 1
fi
echo "[스모크] .env 4필드 검증 통과"

export WA_BROWSER_HEADLESS=false

# playwright chromium 체크
if ! python3 -c "from playwright.sync_api import sync_playwright; sync_playwright().start().chromium.executable_path" >/dev/null 2>&1; then
    echo "[스모크][ERROR] playwright install chromium 을 먼저 실행하세요."
    exit 2
fi

# 대상 폴더
TARGET_FOLDER="${1:-posts/2026-04-22-sample}"
if [ ! -d "$TARGET_FOLDER" ]; then
    echo "[스모크][ERROR] 폴더 없음: $TARGET_FOLDER"
    exit 2
fi

echo "[스모크] 대상 폴더: $TARGET_FOLDER"
echo "[스모크] 실행 시작..."
echo ""

PYTHONPATH="$(pwd)" python3 scripts/smoke_tistory_post.py "$TARGET_FOLDER"
