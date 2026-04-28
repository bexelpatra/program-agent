"""티스토리 카카오 로그인 스모크 러너.

headful 브라우저로 TistoryKakaoLogin.run() 을 끝까지 실행하고
성공/실패를 표준출력 + 종료 코드로 알린다.

종료 코드:
    0 = 로그인 성공
    1 = 로그인 실패 (verify_logged_in False)
    2 = 예외 또는 설정 오류
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

# PROJECT_ROOT 를 sys.path 에 추가 (PYTHONPATH 미설정 환경 방어).
# 엔트리 파일 독립 실행(`python3 scripts/smoke_tistory_login.py`)을 대비한다.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.core.browser import BrowserManager  # noqa: E402
from src.core.config import Config  # noqa: E402
from src.core.logger import get_logger  # noqa: E402
from src.sites.tistory.login import TistoryKakaoLogin  # noqa: E402


logger = get_logger("smoke.tistory_login")


async def main() -> int:
    # 1. Config 로드 — config/settings.yaml + config/tistory.yaml + WA_ 환경변수 오버라이드
    try:
        logger.info("Config 로드 시작")
        config = Config()
        config.load_site("tistory")
        logger.info("Config 로드 완료 (site=tistory)")
    except Exception as exc:
        logger.exception("설정 로드 실패")
        print(f"[스모크][ERROR] 설정 로드 실패: {exc}", file=sys.stderr)
        return 2

    # 2. headful 브라우저로 로그인 시도
    try:
        async with BrowserManager(config) as browser:
            logger.info("BrowserManager 초기화 완료, TistoryKakaoLogin.run() 시작")
            runner = TistoryKakaoLogin(config, browser)
            success = await runner.run()
    except Exception as exc:
        logger.exception("스모크 실행 중 예외")
        print(f"[스모크][ERROR] 스모크 실행 중 예외: {exc}", file=sys.stderr)
        print("                스크린샷 확인: screenshots/tistory_login_*.png", file=sys.stderr)
        return 2

    # 3. 결과 판정
    if success:
        print("[스모크][OK] 티스토리 카카오 로그인 성공")
        print("              단계별 스크린샷: screenshots/tistory_login_*.png")
        return 0
    else:
        print(
            "[스모크][FAIL] 로그인 실패 — verify_logged_in() 이 False 를 반환했습니다.",
            file=sys.stderr,
        )
        print(
            "               screenshots/tistory_login_*.png 을 확인해 셀렉터/흐름을 교정하세요.",
            file=sys.stderr,
        )
        return 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
