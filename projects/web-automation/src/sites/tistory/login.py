"""티스토리 카카오 로그인 워크플로우.

티스토리의 "카카오 계정으로 로그인" 플로우를 자동화한다.
흐름:
    1. 티스토리 로그인 페이지 방문 → "카카오 계정으로 로그인" 버튼 클릭
    2. 카카오 로그인 폼에 이메일/비밀번호 입력 → 제출
    3. 추가 인증 화면에서 "이메일로 인증하기" 전환
    4. Naver IMAP 으로 수신된 인증번호 폴링 → 첫 매치 반환
    5. 인증번호 입력 후 제출 → 로그인 성공 여부 확인

보안 주의:
    - 비밀번호 / 인증번호는 로그에 직접 출력하지 않는다. len= 같은 간접
      표현만 사용한다.
    - OCR (pytesseract, easyocr 등) 은 사용하지 않는다. DOM 텍스트와
      role/aria 정보만 파싱한다.
"""

from __future__ import annotations

import asyncio
from typing import Optional

from playwright.async_api import Locator, Page

from src.auth.naver_imap import fetch_verification_code
from src.core.browser import BrowserManager
from src.core.config import Config
from src.core.logger import get_logger


logger = get_logger("sites.tistory.login")


# 각 단계의 wait_for 기본 타임아웃 (밀리초)
_STEP_TIMEOUT_MS = 15000

# poll_verification_code 기본 파라미터 (architecture.md / task-board 근거)
_DEFAULT_POLL_MAX_ATTEMPTS = 20
_DEFAULT_POLL_INTERVAL_SEC = 3.0


class TistoryKakaoLogin:
    """티스토리 카카오 로그인 + 이메일 2FA 흐름을 실행하는 워크플로우 클래스.

    호출 순서는 `run()` 또는 개별 메서드를 순차 호출한다.
    각 단계 실패 시 스크린샷을 `screenshots/tistory_login_{step}.png` 에 저장한 뒤
    예외를 재raise 한다. `verify_logged_in()` 만 False 를 반환할 뿐 예외를 던지지 않는다.
    """

    def __init__(self, config: Config, browser: BrowserManager) -> None:
        """TistoryKakaoLogin 인스턴스를 생성한다.

        Args:
            config: 로드된 Config 인스턴스 (tistory.yaml 이 병합되어 있어야 한다)
            browser: 이미 start() 된 BrowserManager 인스턴스
        """
        self._config = config
        self._browser = browser

    # ------------------------------------------------------------------
    # 공개 진입점
    # ------------------------------------------------------------------

    async def run(self) -> bool:
        """6개 단계를 순서대로 실행하고 최종 로그인 성공 여부를 반환한다.

        Returns:
            로그인 성공 여부. `verify_logged_in()` 결과 그대로.

        Raises:
            단계 실행 중 발생한 예외는 스크린샷 저장 후 재raise 된다.
        """
        await self.open_login_page()
        await self.fill_kakao_credentials()
        await self.switch_to_email_2fa()

        sender_patterns = self._get_sender_patterns()
        within_minutes = int(self._config.get("email_2fa.within_minutes", 5))
        code = await self.poll_verification_code(
            sender_patterns=sender_patterns,
        )
        await self.submit_code(code)
        logger.info(
            "로그인 단계 완료 (within_minutes=%d). 성공 여부 확인 중",
            within_minutes,
        )
        return await self.verify_logged_in()

    # ------------------------------------------------------------------
    # 단계 1: 로그인 페이지 열기
    # ------------------------------------------------------------------

    async def open_login_page(self) -> None:
        """티스토리 로그인 페이지로 이동 후 "카카오 계정으로 로그인" 버튼을 클릭한다."""
        step = "open_login_page"
        try:
            login_url = self._config.get(
                "site.login_url", "https://www.tistory.com/auth/login"
            )
            await self._browser.goto(login_url)
            logger.info("티스토리 로그인 페이지 진입 (url=%s)", login_url)

            selector = self._config.get("selectors.login_kakao_button", "") or ""
            page = self._browser.get_page()

            if selector:
                # yaml 에 명시된 셀렉터가 있으면 우선 사용
                await page.wait_for_selector(selector, timeout=_STEP_TIMEOUT_MS)
                await page.click(selector)
            else:
                # fallback: "카카오" 텍스트 + role=button/link 후보 중 가시/활성 첫 매치
                locator = await self._find_kakao_login_locator(page)
                if locator is None:
                    raise RuntimeError(
                        "카카오 로그인 버튼을 DOM 에서 찾지 못했습니다 " "(selector 공란 + fallback 실패)."
                    )
                await locator.click()
            logger.info("카카오 로그인 버튼 클릭 완료")
        except Exception:
            await self._screenshot_on_error(step)
            raise

    async def _find_kakao_login_locator(self, page: Page) -> Optional[Locator]:
        """DOM 에서 "카카오" 텍스트 + role=button/link 후보를 찾아 첫 매치를 반환."""
        # role 별로 후보를 수집한 뒤, 가시/활성 조건을 만족하는 첫 매치를 선택.
        for role in ("button", "link"):
            candidates = page.get_by_role(role).filter(has_text="카카오")
            count = await candidates.count()
            for idx in range(count):
                locator = candidates.nth(idx)
                if await self._is_visible_enabled(locator):
                    return locator
        return None

    # ------------------------------------------------------------------
    # 단계 2: 카카오 로그인 폼 입력/제출
    # ------------------------------------------------------------------

    async def fill_kakao_credentials(self) -> None:
        """카카오 로그인 폼에 이메일/비밀번호를 입력하고 로그인 버튼을 누른다."""
        step = "fill_kakao_credentials"
        try:
            email = self._config.get("account.email")
            password = self._config.get("account.password")
            if not email or not password:
                raise ValueError("Config 에 account.email / account.password 가 필요합니다.")

            page = self._browser.get_page()

            id_selector = self._config.get("selectors.kakao_id_input", "") or ""
            pw_selector = self._config.get("selectors.kakao_pw_input", "") or ""

            id_target = id_selector or 'input[type="email"]'
            pw_target = pw_selector or 'input[type="password"]'

            await page.wait_for_selector(id_target, timeout=_STEP_TIMEOUT_MS)
            await page.fill(id_target, email)
            # 비밀번호 길이는 간접 표현으로만 기록
            logger.info(
                "카카오 ID 입력 완료 (email_len=%d, pw_len=%d)",
                len(email),
                len(password),
            )

            await page.wait_for_selector(pw_target, timeout=_STEP_TIMEOUT_MS)
            await page.fill(pw_target, password)

            # 제출 버튼: 공통 후보 순회
            await self._submit_kakao_login_form(page)
            logger.info("카카오 로그인 폼 제출 완료")
        except Exception:
            await self._screenshot_on_error(step)
            raise

    async def _submit_kakao_login_form(self, page: Page) -> None:
        """카카오 로그인 제출 버튼을 클릭한다. 여러 후보를 순차 시도."""
        # 우선 button[type=submit], 그 다음 role=button + 이름="로그인"
        submit_candidates = [
            'button[type="submit"]',
            'input[type="submit"]',
        ]
        for sel in submit_candidates:
            locator = page.locator(sel).first
            if await self._is_visible_enabled(locator):
                await locator.click()
                return

        # role=button 에서 "로그인" 포함 텍스트
        role_locator = page.get_by_role("button", name="로그인")
        if await role_locator.count() > 0:
            first = role_locator.first
            if await self._is_visible_enabled(first):
                await first.click()
                return

        raise RuntimeError("카카오 로그인 제출 버튼을 찾지 못했습니다.")

    # ------------------------------------------------------------------
    # 단계 3: 이메일 2FA 로 전환
    # ------------------------------------------------------------------

    async def switch_to_email_2fa(self) -> None:
        """추가 인증 화면에서 "이메일로 인증하기" / "이메일 인증" 버튼을 찾아 클릭한다.

        OCR 은 사용하지 않는다. selectors.email_2fa_button 이 공란이면
        DOM 의 role=button/link 후보 중 텍스트 완전일치 우선, 가시/활성 먼저.
        """
        step = "switch_to_email_2fa"
        try:
            page = self._browser.get_page()
            selector = self._config.get("selectors.email_2fa_button", "") or ""

            if selector:
                await page.wait_for_selector(selector, timeout=_STEP_TIMEOUT_MS)
                await page.click(selector)
                logger.info("이메일 2FA 전환 버튼 클릭 (yaml selector)")
                return

            # fill_kakao_credentials 직후 호출되므로 2FA 화면이 완전히 렌더될 때까지 대기.
            # 기본 흐름은 `#tmsTwoStepVerification` (카카오톡 앱 인증 대기) 화면이며,
            # "이메일로 인증하기" 버튼은 그 화면 하단에 표시된다.
            await page.wait_for_selector("text=이메일로 인증", timeout=_STEP_TIMEOUT_MS)

            locator = await self._find_email_2fa_locator(page)
            if locator is None:
                raise RuntimeError("이메일 2FA 전환 버튼을 DOM 에서 찾지 못했습니다.")
            await locator.click()
            logger.info("이메일 2FA 전환 버튼 클릭 (DOM fallback)")
        except Exception:
            await self._screenshot_on_error(step)
            raise

    async def _find_email_2fa_locator(self, page: Page) -> Optional[Locator]:
        """이메일 2FA 버튼을 DOM 텍스트/role 로 탐색한다.

        우선순위:
            1) "이메일로 인증하기" 완전일치 (role=button/link)
            2) "이메일 인증" 완전일치 (role=button/link)
            3) "이메일" 포함 + 가시/활성 첫 매치 (role=button/link)
        """
        exact_labels = ("이메일로 인증하기", "이메일 인증")
        for label in exact_labels:
            for role in ("button", "link"):
                locator = page.get_by_role(role, name=label)
                count = await locator.count()
                for idx in range(count):
                    candidate = locator.nth(idx)
                    if await self._is_visible_enabled(candidate):
                        return candidate

        # fallback: "이메일" 포함
        for role in ("button", "link"):
            candidates = page.get_by_role(role).filter(has_text="이메일")
            count = await candidates.count()
            for idx in range(count):
                candidate = candidates.nth(idx)
                if await self._is_visible_enabled(candidate):
                    return candidate
        return None

    # ------------------------------------------------------------------
    # 단계 4: 인증번호 폴링 (Naver IMAP)
    # ------------------------------------------------------------------

    async def poll_verification_code(
        self,
        sender_patterns: list[str],
        max_attempts: int = _DEFAULT_POLL_MAX_ATTEMPTS,
        interval: float = _DEFAULT_POLL_INTERVAL_SEC,
    ) -> str:
        """인증 메일을 폴링해 첫 매치된 인증번호 문자열을 반환한다.

        Args:
            sender_patterns: 발신자 후보 문자열 리스트. 각 문자열이 개별적으로
                `fetch_verification_code(config, sender=s, within_minutes=...)` 에
                **단일 str 인자**로 전달된다. 리스트 그대로 전달하지 않는다.
            max_attempts: 최대 폴링 횟수.
            interval: 폴링 간 대기 초.

        Returns:
            6~8자리 인증번호 문자열.

        Raises:
            ValueError: sender_patterns 가 비어 있는 경우.
            TimeoutError: max_attempts 만큼 시도했으나 수신 실패.
        """
        if not sender_patterns:
            raise ValueError("poll_verification_code: sender_patterns 가 비어 있습니다.")

        within_minutes = int(self._config.get("email_2fa.within_minutes", 5))
        code_length_hint = int(self._config.get("email_2fa.code_length", 8))
        logger.info(
            "인증번호 폴링 시작 (senders=%d, max_attempts=%d, interval=%.1fs, "
            "within_minutes=%d, code_length_hint=%d)",
            len(sender_patterns),
            max_attempts,
            interval,
            within_minutes,
            code_length_hint,
        )

        # code_length_hint 를 정규식으로 반영해 카카오 8자리 인증번호가 메일 본문의
        # 6자리 타임스탬프 등에 오매치되는 것을 막는다. naver_imap 기본 패턴은
        # `\b\d{6,8}\b` 라 6자리 숫자가 먼저 발견되면 오답이 반환됨.
        code_pattern = rf"\b\d{{{code_length_hint}}}\b"

        for attempt in range(1, max_attempts + 1):
            for sender in sender_patterns:
                # naver_imap.fetch_verification_code 시그니처는 sender: str (단일 문자열).
                # 리스트를 통째로 넘기면 TypeError 가 발생하므로 반드시 각 원소를
                # 단일 인자로 전달한다.
                code = fetch_verification_code(
                    self._config,
                    sender=sender,
                    within_minutes=within_minutes,
                    code_pattern=code_pattern,
                )
                if code:
                    logger.info(
                        "인증번호 수신 성공 (attempt=%d/%d, sender_len=%d, code_len=%d)",
                        attempt,
                        max_attempts,
                        len(sender),
                        len(code),
                    )
                    return code
            logger.info(
                "인증번호 미수신 (attempt=%d/%d) — %ss 후 재시도",
                attempt,
                max_attempts,
                interval,
            )
            await asyncio.sleep(interval)

        raise TimeoutError(f"인증번호 수신 실패 (max_attempts={max_attempts})")

    # ------------------------------------------------------------------
    # 단계 5: 인증번호 입력/제출
    # ------------------------------------------------------------------

    async def submit_code(self, code: str) -> None:
        """인증번호 입력 필드를 찾아 채우고 제출한다.

        Args:
            code: 6~8자리 인증번호 문자열. 로그에는 직접 출력하지 않는다.
        """
        step = "submit_code"
        try:
            page = self._browser.get_page()
            selector = self._config.get("selectors.auth_code_input", "") or ""

            target = selector or self._default_auth_code_selector()

            await page.wait_for_selector(target, timeout=_STEP_TIMEOUT_MS)
            await page.fill(target, code)
            logger.info(
                "인증번호 입력 완료 (selector=%s, code_len=%d)",
                "yaml" if selector else "fallback",
                len(code),
            )

            # 제출: Enter 키 → 실패 시 폼 내부 submit 버튼 클릭
            await self._submit_auth_code(page, target)
            logger.info("인증번호 제출 완료")
        except Exception:
            await self._screenshot_on_error(step)
            raise

    def _default_auth_code_selector(self) -> str:
        """인증번호 입력 필드의 fallback 셀렉터를 반환.

        Playwright CSS 는 콤마 분리 OR 매치를 지원한다.
        """
        return (
            'input[inputmode="numeric"], '
            'input[maxlength="8"], '
            'input[maxlength="6"]'
        )

    async def _submit_auth_code(self, page: Page, code_selector: str) -> None:
        """인증번호 입력 필드에서 Enter 키로 제출을 시도하고, 실패 시 submit 버튼 클릭."""
        try:
            # Enter 키 누르기 — 많은 로그인 폼이 이것만으로 제출된다.
            await page.press(code_selector, "Enter")
            return
        except Exception as exc:  # noqa: BLE001 - fallback 경로 유지
            logger.info("Enter 키 제출 실패, 폼 submit 버튼 탐색으로 fallback (%s)", exc)

        # 폼 내부 submit 버튼
        for sel in ('button[type="submit"]', 'input[type="submit"]'):
            locator = page.locator(sel).first
            if await self._is_visible_enabled(locator):
                await locator.click()
                return

        raise RuntimeError("인증번호 제출 버튼을 찾지 못했습니다.")

    # ------------------------------------------------------------------
    # 단계 6: 로그인 성공 확인
    # ------------------------------------------------------------------

    async def verify_logged_in(self) -> bool:
        """로그인 성공 여부를 반환한다. 실패해도 예외를 던지지 않는다.

        판정:
            - URL 이 `tistory.com` 도메인으로 리다이렉트되었고, `/auth/login` 경로가
              아닌 경우 성공.
            - 또는 관리자 영역 링크(`a[href*="manage"]`) 가 DOM 에 존재하면 성공.
        """
        try:
            from urllib.parse import urlparse

            page = self._browser.get_page()

            # submit_code 직후 카카오 → kauth → tistory 리다이렉트 체인이 완료되기까지
            # 수 초 걸린다. 1초 간격으로 최대 10초 폴링한다.
            url = ""
            hostname = ""
            path = ""
            for _ in range(10):
                url = page.url or ""
                parsed = urlparse(url)
                # hostname 기준 판정: URL-encoded redirect 파라미터 안의 tistory.com
                # 문자열에 속지 않는다.
                hostname = (parsed.hostname or "").lower()
                path = parsed.path or ""
                on_tistory = hostname == "www.tistory.com" or hostname.endswith(
                    ".tistory.com"
                )
                on_login_path = path.startswith("/auth/login")
                if on_tistory and not on_login_path:
                    logger.info(
                        "로그인 성공 판정: tistory 도메인 리다이렉트 (host=%s path=%s)",
                        hostname,
                        path,
                    )
                    return True
                await asyncio.sleep(1)

            # 관리자 영역 요소 존재 여부 (마지막 폴링 시점 DOM 기준)
            manage_locator = page.locator('a[href*="manage"]').first
            if await manage_locator.count() > 0:
                if await self._is_visible_enabled(manage_locator):
                    logger.info("로그인 성공 판정: 관리자 영역 링크 감지")
                    return True

            logger.warning("로그인 성공 판정 실패 (url=%s)", url)
            return False
        except Exception as exc:  # noqa: BLE001 - verify 는 raise 하지 않음
            logger.warning("verify_logged_in 중 예외 발생, False 반환: %s", exc)
            return False

    # ------------------------------------------------------------------
    # 내부 헬퍼
    # ------------------------------------------------------------------

    def _get_sender_patterns(self) -> list[str]:
        """Config 에서 email_2fa.sender_patterns 를 읽어 리스트로 반환.

        비어 있으면 ValueError. (원자적 Config 계약: TASK-012-B 가 yaml 에 필수 기입)
        """
        raw = self._config.get("email_2fa.sender_patterns")
        if not raw:
            raise ValueError("Config 에 email_2fa.sender_patterns 가 필요합니다 (list[str]).")
        if not isinstance(raw, list):
            raise ValueError(
                "email_2fa.sender_patterns 는 리스트여야 합니다. "
                f"(현재 타입={type(raw).__name__})"
            )
        senders = [str(s) for s in raw if str(s).strip()]
        if not senders:
            raise ValueError("email_2fa.sender_patterns 에 유효한 문자열이 없습니다.")
        return senders

    async def _is_visible_enabled(self, locator: Locator) -> bool:
        """Locator 가 가시 + 활성 상태인지 확인한다."""
        try:
            if not await locator.is_visible():
                return False
            if not await locator.is_enabled():
                return False
            return True
        except Exception:  # noqa: BLE001 - 타이밍 문제 등은 False 로 간주
            return False

    async def _screenshot_on_error(self, step_name: str) -> None:
        """단계 실패 시 스크린샷 저장. 저장 자체 실패는 무시(본래 예외 우선)."""
        try:
            path = await self._browser.screenshot(f"tistory_login_{step_name}")
            logger.error("단계 실패 스크린샷 저장: step=%s, path=%s", step_name, path)
        except Exception as exc:  # noqa: BLE001
            logger.error(
                "단계 실패 스크린샷 저장 중 추가 예외 발생 (step=%s): %s",
                step_name,
                exc,
            )


__all__ = ["TistoryKakaoLogin"]
