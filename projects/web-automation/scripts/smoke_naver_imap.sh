#!/usr/bin/env bash
# Naver IMAP 인증번호 추출 스모크 테스트
#
# 사용법:
#   ./scripts/smoke_naver_imap.sh                         # 기본 발신자 'noreply@kakaocorp.com'
#   ./scripts/smoke_naver_imap.sh "noreply@tistory.com"   # 발신자 커스텀
#
# 사전 준비:
#   1. projects/web-automation/.env 작성 (.env.example 참조)
#   2. Naver 메일 > 환경설정 > POP3/IMAP 설정 > IMAP 사용함
#   3. 2단계 인증 사용 시 앱 비밀번호 발급해서 .env 에 넣기
#
# 참고:
#   IMAP 접속에 사용하는 계정은 네이버 계정(WA_NAVER_IMAP_EMAIL/PASSWORD)이다.
#   카카오 계정(WA_ACCOUNT_EMAIL/PASSWORD)은 티스토리 로그인용이며 이 스크립트에서는 사용하지 않는다.

set -euo pipefail

# 프로젝트 루트로 이동 (이 스크립트 위치 기준)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

# .env 로드
if [ ! -f ".env" ]; then
    echo "[ERROR] .env 파일이 없습니다."
    echo "        아래 명령으로 템플릿을 복사하고 값을 채워넣으세요:"
    echo "        cp .env.example .env"
    exit 1
fi

# .env 의 모든 변수를 자동 export
set -a
# shellcheck disable=SC1091
source .env
set +a

# 필수 변수 검증 (IMAP 접속은 네이버 계정 사용)
if [ -z "${WA_NAVER_IMAP_EMAIL:-}" ] || [ "${WA_NAVER_IMAP_EMAIL}" = "your_naver_id@naver.com" ]; then
    echo "[ERROR] .env 의 WA_NAVER_IMAP_EMAIL 이 비어있거나 템플릿 값입니다."
    exit 1
fi
if [ -z "${WA_NAVER_IMAP_PASSWORD:-}" ] || [ "${WA_NAVER_IMAP_PASSWORD}" = "your_naver_app_password" ]; then
    echo "[ERROR] .env 의 WA_NAVER_IMAP_PASSWORD 이 비어있거나 템플릿 값입니다."
    exit 1
fi

# 발신자 필터 (인자 > 기본값). 실측 발신자: noreply@kakaocorp.com
SENDER="${1:-noreply@kakaocorp.com}"

echo "[INFO] Naver IMAP 계정: ${WA_NAVER_IMAP_EMAIL}"
echo "[INFO] 발신자 필터: ${SENDER}"
echo "[INFO] 최근 10분 이내 메일에서 6~8자리 인증번호 검색 (최신 메일 우선)..."
echo ""

python3 - <<PYEOF
import sys, traceback
sys.path.insert(0, ".")
from src.core.config import Config
from src.auth import fetch_verification_code

try:
    cfg = Config(".")
    cfg.load_site("tistory")
    code = fetch_verification_code(cfg, sender="${SENDER}", within_minutes=10)
    if code:
        print(f"[OK] 추출된 인증번호: {code}")
        sys.exit(0)
    else:
        print("[WARN] 인증번호 없음 (None).")
        print("       - 발신자 주소가 '${SENDER}' 와 다를 수 있음.")
        print("       - Naver 메일함에서 실제 '보낸사람' 주소 확인 후 인자로 전달:")
        print("         ./scripts/smoke_naver_imap.sh '<실제주소>'")
        sys.exit(2)
except Exception as e:
    print(f"[ERROR] 예외 발생: {type(e).__name__}: {e}")
    traceback.print_exc()
    sys.exit(1)
PYEOF
