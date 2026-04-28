"""Playwright 브라우저 엔진 모듈.

브라우저 시작/종료, 페이지 이동, 요소 대기/클릭/입력,
스크린샷 등 공통 브라우저 조작 기능을 제공한다.
async context manager를 지원하여 안전한 리소스 관리를 보장한다.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from playwright.async_api import (
    Browser,
    BrowserContext,
    Page,
    Playwright,
    async_playwright,
)

from src.core.config import Config


class BrowserManager:
    """Playwright 기반 브라우저 관리 클래스.

    Config에서 브라우저 설정을 로드하고, Playwright 브라우저의
    생명주기(시작/종료)를 관리한다. async context manager로
    사용할 수 있다.

    사용 예시::

        async with BrowserManager(config) as browser:
            await browser.goto("https://example.com")
            await browser.fill("#email", "user@example.com")
            await browser.click("#submit")
            await browser.screenshot("after_login")
    """

    def __init__(self, config: Config) -> None:
        """BrowserManager 인스턴스를 생성한다.

        Args:
            config: 설정 객체 (settings.yaml의 browser/screenshot 섹션 사용)
        """
        self._config = config

        # 브라우저 설정 로드
        self._headless: bool = config.get("browser.headless", False)
        self._slow_mo: int = config.get("browser.slow_mo", 0)
        self._timeout: int = config.get("browser.timeout", 30000)
        self._viewport_width: int = config.get("browser.viewport.width", 1280)
        self._viewport_height: int = config.get("browser.viewport.height", 720)
        self._user_agent: str = config.get("browser.user_agent", "")

        # 스크린샷 설정 로드
        self._screenshot_dir: str = config.get("screenshot.directory", "screenshots")

        # Playwright 리소스 (start() 이후 초기화)
        self._playwright: Optional[Playwright] = None
        self._browser: Optional[Browser] = None
        self._context: Optional[BrowserContext] = None
        self._page: Optional[Page] = None

    async def start(self) -> None:
        """브라우저, 컨텍스트, 페이지를 생성하고 초기화한다.

        Playwright를 시작하고 Chromium 브라우저를 실행한 뒤,
        설정에 맞는 브라우저 컨텍스트와 페이지를 생성한다.
        """
        self._playwright = await async_playwright().start()

        # 브라우저 실행 옵션
        launch_options: dict = {
            "headless": self._headless,
            "slow_mo": self._slow_mo,
        }
        self._browser = await self._playwright.chromium.launch(**launch_options)

        # 컨텍스트 옵션 (뷰포트, User-Agent 등)
        context_options: dict = {
            "viewport": {
                "width": self._viewport_width,
                "height": self._viewport_height,
            },
        }
        if self._user_agent:
            context_options["user_agent"] = self._user_agent

        self._context = await self._browser.new_context(**context_options)

        # 기본 타임아웃 설정
        self._context.set_default_timeout(self._timeout)

        # 페이지 생성
        self._page = await self._context.new_page()

    async def stop(self) -> None:
        """브라우저와 Playwright 리소스를 안전하게 종료한다."""
        if self._context:
            await self._context.close()
            self._context = None
            self._page = None

        if self._browser:
            await self._browser.close()
            self._browser = None

        if self._playwright:
            await self._playwright.stop()
            self._playwright = None

    async def goto(self, url: str) -> None:
        """지정한 URL로 페이지를 이동한다.

        Args:
            url: 이동할 URL
        """
        page = self._ensure_page()
        await page.goto(url)

    async def wait_for(self, selector: str, timeout: Optional[int] = None) -> None:
        """지정한 셀렉터의 요소가 나타날 때까지 대기한다.

        Args:
            selector: CSS 셀렉터
            timeout: 대기 타임아웃 (밀리초). None이면 기본 타임아웃 사용.
        """
        page = self._ensure_page()
        options: dict = {}
        if timeout is not None:
            options["timeout"] = timeout
        await page.wait_for_selector(selector, **options)

    async def click(self, selector: str) -> None:
        """지정한 셀렉터의 요소를 클릭한다.

        Args:
            selector: CSS 셀렉터
        """
        page = self._ensure_page()
        await page.click(selector)

    async def fill(self, selector: str, value: str) -> None:
        """지정한 셀렉터의 입력 필드에 값을 입력한다.

        Args:
            selector: CSS 셀렉터
            value: 입력할 값
        """
        page = self._ensure_page()
        await page.fill(selector, value)

    async def screenshot(self, name: str) -> Path:
        """현재 페이지의 스크린샷을 저장한다.

        스크린샷은 설정의 screenshot.directory에 저장된다.
        파일명에 .png 확장자가 자동으로 추가된다.

        Args:
            name: 스크린샷 파일명 (확장자 제외)

        Returns:
            저장된 스크린샷 파일의 경로
        """
        page = self._ensure_page()

        # 스크린샷 디렉토리 생성
        screenshot_path = Path(self._screenshot_dir)
        screenshot_path.mkdir(parents=True, exist_ok=True)

        # 파일 경로 생성
        file_path = screenshot_path / f"{name}.png"
        await page.screenshot(path=str(file_path))

        return file_path

    def get_page(self) -> Page:
        """현재 Page 객체를 반환한다.

        Playwright API를 직접 사용해야 할 때 호출한다.

        Returns:
            현재 활성 Page 객체
        """
        return self._ensure_page()

    def _ensure_page(self) -> Page:
        """페이지가 초기화되었는지 확인하고 반환한다.

        Returns:
            현재 활성 Page 객체

        Raises:
            RuntimeError: 브라우저가 시작되지 않은 경우
        """
        if self._page is None:
            raise RuntimeError(
                "브라우저가 시작되지 않았습니다. " "start()를 호출하거나 async with 문을 사용하세요."
            )
        return self._page

    async def __aenter__(self) -> "BrowserManager":
        """async context manager 진입 시 브라우저를 시작한다."""
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """async context manager 종료 시 브라우저를 정리한다."""
        await self.stop()
