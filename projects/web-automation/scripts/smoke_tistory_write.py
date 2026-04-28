"""티스토리 글쓰기 스모크 러너.

headful 브라우저로 카카오 로그인 → 글 작성 → 임시저장까지 실행한다.
실제 임시저장 성공 여부는 사용자가 관리자 페이지 '임시저장된 글' 목록에서
육안으로 확인한다.

종료 코드:
    0 = 임시저장 단계까지 예외 없이 완료
    1 = writer.run() False 반환 (현재 경로에서는 논리적으로 미도달)
    2 = 로그인 실패 / 설정 오류 / 예외
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

# PROJECT_ROOT 를 sys.path 에 추가 (PYTHONPATH 미설정 환경 방어)
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.core.browser import BrowserManager  # noqa: E402
from src.core.config import Config  # noqa: E402
from src.core.logger import get_logger  # noqa: E402
from src.sites.tistory.login import TistoryKakaoLogin  # noqa: E402
from src.sites.tistory.writer import TistoryWriter  # noqa: E402


logger = get_logger("smoke.tistory_write")


# 샘플 데이터 (Reviewer #9·#10 확정)
SAMPLE_TITLE = "[스모크] 티스토리 자동화 테스트"
SAMPLE_BODY_HTML = (
    "<h2>스모크 테스트</h2>"
    "<p>본문 <b>굵게</b> + 기울임 <i>italic</i>.</p>"
    "<ul><li>항목 1</li><li>항목 2</li></ul>"
)
SAMPLE_TAGS = ["스모크", "자동화"]
SAMPLE_CATEGORY = "메모"
SAMPLE_CATEGORY_FALLBACK = "카테고리 없음"
SAMPLE_ATTACHMENTS = ["samples/sample.txt"]


async def main() -> int:
    # 1. Config 로드
    try:
        logger.info("Config 로드 시작")
        config = Config()
        config.load_site("tistory")
        logger.info("Config 로드 완료")
    except Exception as exc:
        logger.exception("설정 로드 실패")
        print(f"[스모크][ERROR] 설정 로드 실패: {exc}", file=sys.stderr)
        return 2

    # 2. 브라우저 시작 → 로그인 → 글쓰기
    try:
        async with BrowserManager(config) as browser:
            # 2-1. 카카오 로그인
            login = TistoryKakaoLogin(config, browser)
            logged_in = await login.run()
            if not logged_in:
                print(
                    "[스모크][FAIL] 카카오 로그인 실패 — screenshots/tistory_login_*.png 확인",
                    file=sys.stderr,
                )
                return 2
            print("[스모크][OK] 카카오 로그인 성공")

            # 2-2. 글 작성 → 임시저장
            writer = TistoryWriter(config, browser)
            result = await writer.run(
                title=SAMPLE_TITLE,
                body_html=SAMPLE_BODY_HTML,
                tags=SAMPLE_TAGS,
                category=SAMPLE_CATEGORY,
                category_fallback=SAMPLE_CATEGORY_FALLBACK,
                attachments=SAMPLE_ATTACHMENTS,
                mode="draft",
            )
    except Exception as exc:
        logger.exception("스모크 실행 중 예외")
        print(f"[스모크][ERROR] 스모크 실행 중 예외: {exc}", file=sys.stderr)
        print("               스크린샷 확인: screenshots/tistory_write_*.png", file=sys.stderr)
        return 2

    # 3. 결과 출력
    if result:
        print("[스모크][OK] ✅ 임시저장 요청 전송 완료.")
        print("             관리자 페이지 '임시저장된 글' 목록에서")
        print("             제목·본문·카테고리·태그·첨부파일을 확인하세요.")
        print(f"             - 제목: {SAMPLE_TITLE}")
        print(f"             - 카테고리: {SAMPLE_CATEGORY} (fallback={SAMPLE_CATEGORY_FALLBACK})")
        print(f"             - 태그: {SAMPLE_TAGS}")
        print(f"             - 첨부: {SAMPLE_ATTACHMENTS}")
        return 0
    else:
        print("[스모크][FAIL] writer.run() 이 False 반환 (save_draft 단계 실패)", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
