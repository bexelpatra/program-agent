#!/usr/bin/env bash
# 티스토리 글쓰기 스모크 테스트 wrapper
#
# 사용법:
#   ./scripts/smoke_tistory_write.sh
#
# 사전 준비:
#   1. projects/web-automation/.env 작성 (카카오 + 네이버 IMAP 4필드)
#   2. playwright chromium 바이너리 설치: `playwright install chromium`
#   3. (서버 환경이면) xvfb 설치: sudo apt install xvfb — 없으면 수동 래핑
#
# 종료 코드:
#   0 = 임시저장 단계까지 예외 없이 완료
#   1 = writer.run() False 반환
#   2 = 로그인/설정/예외

set -euo pipefail

# DISPLAY 없고 xvfb-run 있으면 자동 래핑 (재귀 방지 가드)
if [ -z "${DISPLAY:-}" ] && [ -z "${_WA_SMOKE_XVFB_WRAPPED:-}" ]; then
    if command -v xvfb-run >/dev/null 2>&1; then
        echo "[스모크] DISPLAY 미설정 + xvfb-run 감지 → 자동 래핑 실행"
        export _WA_SMOKE_XVFB_WRAPPED=1
        exec xvfb-run -a "$0" "$@"
    else
        echo "[스모크][WARN] DISPLAY 미설정이고 xvfb-run 도 없습니다."
        echo "                sudo apt install xvfb (Ubuntu) 후 재실행하세요."
    fi
fi

# 프로젝트 루트로 이동
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

echo "[스모크] 프로젝트 루트: $PROJECT_ROOT"

# 1. .env 확인
if [ ! -f ".env" ]; then
    echo "[스모크][ERROR] .env 파일이 없습니다."
    echo "                cp .env.example .env 후 계정 정보를 채워넣으세요."
    exit 1
fi

echo "[스모크] .env 로드 중..."
set -a
# shellcheck disable=SC1091
source .env
set +a

# 2. 4필드 검증
missing_fields=()
[ -z "${WA_ACCOUNT_EMAIL:-}" ]         && missing_fields+=("WA_ACCOUNT_EMAIL")
[ -z "${WA_ACCOUNT_PASSWORD:-}" ]      && missing_fields+=("WA_ACCOUNT_PASSWORD")
[ -z "${WA_NAVER_IMAP_EMAIL:-}" ]      && missing_fields+=("WA_NAVER_IMAP_EMAIL")
[ -z "${WA_NAVER_IMAP_PASSWORD:-}" ]   && missing_fields+=("WA_NAVER_IMAP_PASSWORD")

if [ ${#missing_fields[@]} -gt 0 ]; then
    echo "[스모크][ERROR] .env 에서 다음 필수 필드가 비어있습니다:"
    for f in "${missing_fields[@]}"; do
        echo "                - $f"
    done
    exit 1
fi

echo "[스모크] .env 4필드 검증 통과"

export WA_ACCOUNT_EMAIL WA_ACCOUNT_PASSWORD WA_NAVER_IMAP_EMAIL WA_NAVER_IMAP_PASSWORD

# 3. headful 강제
export WA_BROWSER_HEADLESS=false
echo "[스모크] headful 강제: WA_BROWSER_HEADLESS=false"

# 4. 샘플 첨부파일 생성 (Reviewer #9 확정: bash wrapper 책임, idempotent)
mkdir -p samples
[ -f samples/sample.txt ] || echo '테스트 첨부파일 — 티스토리 스모크' > samples/sample.txt
echo "[스모크] 샘플 첨부: samples/sample.txt ($(wc -c < samples/sample.txt) bytes)"

# 5. playwright chromium 바이너리 선행 체크
echo "[스모크] playwright chromium 바이너리 확인 중..."
if ! python3 -c "from playwright.sync_api import sync_playwright; sync_playwright().start().chromium.executable_path" >/dev/null 2>&1; then
    echo "[스모크][ERROR] playwright chromium 바이너리가 없습니다."
    echo "                먼저 실행: playwright install chromium"
    exit 2
fi
echo "[스모크] playwright chromium OK"

# 6. python 엔트리 실행
echo "[스모크] 티스토리 글쓰기 시작 (headful 브라우저)..."
echo ""
PYTHONPATH="$(pwd)" python3 scripts/smoke_tistory_write.py
