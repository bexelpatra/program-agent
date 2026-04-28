"""티스토리 폴더 기반 임시저장 스모크 러너.

CLI: python3 smoke_tistory_post.py <folder_path>

동작:
    1. 카카오 로그인
    2. post_runner.run_post(folder) 호출
    3. RunResult 를 사람이 읽기 쉬운 요약으로 출력

종료 코드:
    0 = 임시저장 완료 (.published 기록)
    1 = skip (.published 이미 존재)
    2 = 예외 (설정·로그인·실행 중 어느 단계든)
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.core.browser import BrowserManager  # noqa: E402
from src.core.config import Config  # noqa: E402
from src.core.logger import get_logger  # noqa: E402
from src.sites.tistory.login import TistoryKakaoLogin  # noqa: E402
from src.tistory_post.post_runner import run_post  # noqa: E402

logger = get_logger("smoke.tistory_post")


async def main() -> int:
    if len(sys.argv) < 2:
        print("[스모크][ERROR] 사용법: smoke_tistory_post.py <폴더경로>", file=sys.stderr)
        return 2
    folder = Path(sys.argv[1]).resolve()
    if not folder.is_dir():
        print(f"[스모크][ERROR] 폴더 없음: {folder}", file=sys.stderr)
        return 2

    try:
        config = Config()
        config.load_site("tistory")
    except Exception as exc:
        logger.exception("Config 로드 실패")
        print(f"[스모크][ERROR] 설정 로드 실패: {exc}", file=sys.stderr)
        return 2

    try:
        async with BrowserManager(config) as browser:
            ok = await TistoryKakaoLogin(config, browser).run()
            if not ok:
                print(
                    "[스모크][ERROR] 카카오 로그인 실패 — screenshots/tistory_login_*.png 확인",
                    file=sys.stderr,
                )
                return 2
            print("[스모크][OK] 카카오 로그인 성공")

            blog_name = config.get("blog.blog_name")
            if not blog_name:
                print("[스모크][ERROR] config blog.blog_name 이 없습니다.", file=sys.stderr)
                return 2
            page = browser.get_page()
            result = await run_post(page, folder, blog_name)
    except Exception as exc:
        logger.exception("run_post 실행 중 예외")
        print(f"[스모크][ERROR] 실행 중 예외: {exc}", file=sys.stderr)
        print(f"               상태 파일: {folder}/.error 확인", file=sys.stderr)
        return 2

    if result.skipped:
        print(f"[스모크][SKIP] .published 이미 존재 — skip: {folder}")
        return 1

    print(f"[스모크][OK] ✅ 임시저장 완료 (draft_sequence={result.draft_sequence})")
    print(f"             폴더: {folder}")
    print(f"             관리자 임시저장 모달에서 확인하세요.")
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
