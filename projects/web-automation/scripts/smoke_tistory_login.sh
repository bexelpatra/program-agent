#!/usr/bin/env bash
# 티스토리 카카오 로그인 스모크 테스트 wrapper
#
# 사용법:
#   ./scripts/smoke_tistory_login.sh
#
# 사전 준비:
#   1. projects/web-automation/.env 작성 (.env.example 참조)
#      - WA_ACCOUNT_EMAIL / WA_ACCOUNT_PASSWORD        : 카카오 계정 (티스토리 로그인)
#      - WA_NAVER_IMAP_EMAIL / WA_NAVER_IMAP_PASSWORD  : 네이버 IMAP (인증번호 수신)
#   2. Naver 메일 > 환경설정 > POP3/IMAP > IMAP 사용함 + 앱 비밀번호 (2FA 시)
#   3. playwright chromium 바이너리 설치: `playwright install chromium`
#
# 종료 코드:
#   0 = 로그인 성공
#   1 = 로그인 실패 / 설정 오류 (.env 누락·필드 공백)
#   2 = playwright chromium 미설치 또는 python 측 예외

set -euo pipefail

# DISPLAY 가 없고 xvfb-run 이 설치돼 있으면 자동으로 가상 X 서버 래핑 후 재실행한다.
# headful Playwright 는 X 서버가 필요한데 SSH·컨테이너 환경에는 보통 DISPLAY 가 없다.
# 재귀 방지용 가드 변수(`_WA_SMOKE_XVFB_WRAPPED`)로 무한 exec 루프를 차단한다.
if [ -z "${DISPLAY:-}" ] && [ -z "${_WA_SMOKE_XVFB_WRAPPED:-}" ]; then
    if command -v xvfb-run >/dev/null 2>&1; then
        echo "[스모크] DISPLAY 미설정 + xvfb-run 감지 → 자동 래핑 실행"
        export _WA_SMOKE_XVFB_WRAPPED=1
        exec xvfb-run -a "$0" "$@"
    else
        echo "[스모크][WARN] DISPLAY 미설정이고 xvfb-run 도 없습니다."
        echo "                sudo apt install xvfb (Ubuntu) 후 재실행하거나 X11 forwarding 이 있는 세션을 사용하세요."
    fi
fi

# 프로젝트 루트로 이동 (이 스크립트 위치 기준)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

echo "[스모크] 프로젝트 루트: $PROJECT_ROOT"

# 1. .env 존재 확인
if [ ! -f ".env" ]; then
    echo "[스모크][ERROR] .env 파일이 없습니다."
    echo "                cp .env.example .env 후 카카오/네이버 계정 정보를 채워넣으세요."
    exit 1
fi

echo "[스모크] .env 로드 중..."

# 2. .env 의 모든 변수를 자동 export
set -a
# shellcheck disable=SC1091
source .env
set +a

# 3. 4개 필수 필드 검증 (카카오 2 + 네이버 IMAP 2)
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
    echo "                .env.example 을 참조해서 값을 채워넣으세요."
    exit 1
fi

echo "[스모크] .env 4필드 검증 통과 (카카오 계정 / 네이버 IMAP 계정)"

# 4. 명시 export (set -a 로 이미 export 되어 있으나 가독성을 위해 재선언)
export WA_ACCOUNT_EMAIL
export WA_ACCOUNT_PASSWORD
export WA_NAVER_IMAP_EMAIL
export WA_NAVER_IMAP_PASSWORD

# 5. headful 강제 — Config.get 의 WA_ 환경변수 우선권으로 settings.yaml 값을 덮어쓴다.
#    (src/core/config.py:101-104 실측 기준)
#    BrowserManager._headless private 속성 직접 수정 같은 안티패턴을 피하고 공식 override 경로만 사용.
export WA_BROWSER_HEADLESS=false
echo "[스모크] headful 강제: WA_BROWSER_HEADLESS=false"

# 6. playwright chromium 바이너리 선행 체크
echo "[스모크] playwright chromium 바이너리 확인 중..."
if ! python3 -c "from playwright.sync_api import sync_playwright; sync_playwright().start().chromium.executable_path" >/dev/null 2>&1; then
    echo "[스모크][ERROR] playwright chromium 바이너리가 설치되어 있지 않습니다."
    echo "                먼저 실행하세요: playwright install chromium"
    exit 2
fi
echo "[스모크] playwright chromium OK"

# 7. python 엔트리 실행 (종료 코드 그대로 전파)
echo "[스모크] 티스토리 카카오 로그인 시작 (headful 브라우저)..."
echo ""
PYTHONPATH="$(pwd)" python3 scripts/smoke_tistory_login.py
