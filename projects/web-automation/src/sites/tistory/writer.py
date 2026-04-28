"""티스토리 글쓰기 워크플로우.

TinyMCE 기반 티스토리 신규 글 작성 페이지(`/manage/newpost`) 에서
제목/본문/태그/카테고리/첨부파일을 설정하고 임시저장을 수행한다.

흐름:
    1. `/manage/newpost` 이동 + TinyMCE 초기화 대기
    2. 제목 입력 (`#post-title-inp`)
    3. 본문 주입 (TinyMCE `activeEditor.setContent(h)` + 비어있지 않음 검증)
    4. 태그 입력 (`#tagText` fill + Enter + 200ms 확정 대기)
    5. 카테고리 선택 (`#category-btn` → `#category-list` aria-label **완전일치**)
    6. 첨부파일 업로드 (첨부 드롭다운 → 메뉴 완전일치 → `expect_file_chooser`)
    7. 임시저장 (`a.action[has_text="임시저장"]` → networkidle + 2초 sleep)

보안 주의:
    - OCR 라이브러리는 사용하지 않는다. DOM/텍스트만 파싱한다.
    - 민감 정보(본문·첨부 경로) 를 로그에 직접 출력하지 않고 간접 표현만 사용한다.

`publish` 모드는 본 태스크 범위 외 — 후속 태스크에서 구현한다.
"""

from __future__ import annotations

import asyncio
import re
from pathlib import Path
from typing import Optional

from playwright.async_api import TimeoutError as PlaywrightTimeoutError

from src.core.browser import BrowserManager
from src.core.config import Config
from src.core.logger import get_logger


logger = get_logger("sites.tistory.writer")


# 각 단계의 wait_for 기본 타임아웃 (밀리초) — login.py 복제
_STEP_TIMEOUT_MS = 15000

# 첨부 드롭다운 메뉴 항목 kind → 메뉴 텍스트 매핑.
# 실측 UI 라벨이므로 상수로 고정. substring 오매치 차단을 위해 완전일치로만 사용.
_ATTACH_KIND_TEXT = {
    "file": "파일",
    "image": "사진",
    "slideshow": "슬라이드쇼",
}


class TistoryWriter:
    """티스토리 신규 글 작성 워크플로우.

    호출 순서는 `run()` 또는 개별 메서드를 순차 호출한다.
    각 단계 실패 시 `screenshots/tistory_write_{step}.png` 에 스크린샷을 저장한 뒤
    예외를 재raise 한다 (login.py 와 동일 패턴).
    """

    def __init__(self, config: Config, browser: BrowserManager) -> None:
        """TistoryWriter 인스턴스를 생성한다.

        Args:
            config: 로드된 Config 인스턴스 (tistory.yaml 병합 상태여야 한다)
            browser: 이미 start() 된 BrowserManager 인스턴스 (로그인 완료 상태)
        """
        self._config = config
        self._browser = browser

    # ------------------------------------------------------------------
    # 공개 진입점
    # ------------------------------------------------------------------

    async def run(
        self,
        *,
        title: str,
        body_html: str,
        tags: Optional[list[str]] = None,
        category: Optional[str] = None,
        category_fallback: Optional[str] = None,
        attachments: Optional[list[str]] = None,
        mode: str = "draft",
    ) -> bool:
        """글 작성 전체 흐름을 실행한다.

        Args:
            title: 글 제목.
            body_html: TinyMCE 에 주입할 HTML 문자열.
            tags: 태그 리스트. None/빈 리스트면 태그 단계 skip.
            category: 카테고리 이름 (aria-label 완전일치). None 이면 skip.
            category_fallback: `category` 선택이 실패했을 때 재시도할 카테고리 이름.
                None 이면 fallback 없이 최초 ValueError 를 그대로 raise.
            attachments: 첨부파일 경로 리스트. None/빈 리스트면 skip.
            mode: "draft" 또는 "publish". 현재 "publish" 는 미구현 — 진입 즉시
                `NotImplementedError` 를 raise 한다.

        Returns:
            `save_draft()` 의 반환값 (현재 구현에서는 True).

        Raises:
            NotImplementedError: mode="publish" 인 경우.
            ValueError: category 가 목록에 없고 fallback 도 실패한 경우.
        """
        # mode="publish" 는 후속 태스크에서 구현 — silently skip 금지.
        if mode == "publish":
            raise NotImplementedError("publish mode 는 후속 태스크에서 구현")
        if mode != "draft":
            raise ValueError(f"지원하지 않는 mode='{mode}' (draft|publish 만 허용)")

        await self.open_newpost()
        await self.fill_title(title)
        await self.set_body_html(body_html)

        # 첨부는 툴바 '첨부' 드롭다운에서 파일을 선택하는 경로라서
        # 카테고리 드롭다운·태그 입력 전에 호출해야 툴바 DOM 이 안정적이다.
        # (카테고리 선택 후 TinyMCE 툴바 `title="첨부"` 속성이 일부 환경에서
        # 제거/가려지는 현상을 스모크에서 실측.)
        if attachments:
            for path in attachments:
                await self.attach_file(path, kind="file")

        if tags:
            await self.add_tags(tags)

        if category is not None:
            try:
                await self.select_category(category)
            except ValueError:
                if category_fallback is None:
                    raise
                logger.warning(
                    "카테고리 '%s' 실패 — fallback='%s' 로 재시도",
                    category,
                    category_fallback,
                )
                await self.select_category(category_fallback)

        return await self.save_draft()

    # ------------------------------------------------------------------
    # 단계 1: 신규 글 페이지 열기
    # ------------------------------------------------------------------

    async def open_newpost(self) -> None:
        """`/manage/newpost` 이동 + 제목 입력란·TinyMCE init 대기."""
        step = "open_newpost"
        try:
            blog_name = self._config.get("blog.blog_name")
            if not blog_name:
                raise ValueError("blog.blog_name 이 필요합니다")

            page = self._browser.get_page()
            url = f"https://{blog_name}.tistory.com/manage/newpost"
            await page.goto(url)

            title_sel = (
                self._config.get("selectors.write_title_input", "") or "#post-title-inp"
            )
            await page.wait_for_selector(title_sel, timeout=_STEP_TIMEOUT_MS)

            # TinyMCE 인스턴스가 초기화되고 getBody() 가 유효해질 때까지 대기.
            # 이 시점 전에 setContent 를 호출하면 silently 무시된다.
            await page.wait_for_function(
                "() => window.tinymce && window.tinymce.activeEditor "
                "&& window.tinymce.activeEditor.getBody()",
                timeout=_STEP_TIMEOUT_MS,
            )
            logger.info("단계 완료 (open_newpost, blog=%s)", blog_name)
        except Exception:
            await self._screenshot_on_error(step)
            raise

    # ------------------------------------------------------------------
    # 단계 2: 제목 입력
    # ------------------------------------------------------------------

    async def fill_title(self, title: str) -> None:
        """제목 입력란(`#post-title-inp`) 에 값을 채운다."""
        step = "fill_title"
        try:
            page = self._browser.get_page()
            title_sel = (
                self._config.get("selectors.write_title_input", "") or "#post-title-inp"
            )
            await page.fill(title_sel, title)
            # 제목 본문은 민감하지 않으나 일관성 유지를 위해 길이만 기록한다.
            logger.info("단계 완료 (fill_title, title_len=%d)", len(title))
        except Exception:
            await self._screenshot_on_error(step)
            raise

    # ------------------------------------------------------------------
    # 단계 3: 본문 주입
    # ------------------------------------------------------------------

    async def set_body_html(self, html: str) -> None:
        """TinyMCE `activeEditor.setContent(h)` 로 본문 HTML 을 주입한다.

        티스토리 스킨이 `data-ke-size` 등 속성을 자동 추가하지만 HTML
        구조·텍스트는 보존된다. 주입 직후 `getContent().length > 0` 으로
        비어있지 않음을 검증해 silently 삼켜진 주입을 감지한다.
        """
        step = "set_body_html"
        try:
            page = self._browser.get_page()
            await page.evaluate(
                "(h) => window.tinymce.activeEditor.setContent(h)", html
            )
            await page.wait_for_function(
                "() => window.tinymce.activeEditor.getContent().length > 0",
                timeout=_STEP_TIMEOUT_MS,
            )
            logger.info("단계 완료 (set_body_html, html_len=%d)", len(html))
        except Exception:
            await self._screenshot_on_error(step)
            raise

    # ------------------------------------------------------------------
    # 단계 4: 태그 추가
    # ------------------------------------------------------------------

    async def add_tags(self, tags: list[str]) -> None:
        """각 태그를 `#tagText` 에 fill+Enter+200ms 순서로 주입한다."""
        step = "add_tags"
        try:
            page = self._browser.get_page()
            tag_sel = self._config.get("selectors.tag_input", "") or "#tagText"
            for tag in tags:
                if not tag:
                    continue
                await page.fill(tag_sel, tag)
                await page.press(tag_sel, "Enter")
                # 태그 칩 렌더 확정 대기 (즉시 다음 태그를 입력하면 마지막 한 건만
                # 남거나 중복되는 이슈가 있어 200ms 고정 대기).
                await page.wait_for_timeout(200)
            logger.info("단계 완료 (add_tags, count=%d)", len(tags))
        except Exception:
            await self._screenshot_on_error(step)
            raise

    # ------------------------------------------------------------------
    # 단계 5: 카테고리 선택
    # ------------------------------------------------------------------

    async def select_category(self, name: Optional[str]) -> None:
        """카테고리 목록에서 `name` 과 aria-label 이 **완전일치** 하는 항목을 선택.

        None/빈 문자열이면 즉시 return. 완전일치 매치가 0 건이면 사용 가능한
        aria-label 전체 목록을 포함한 ValueError 를 raise 한다.
        """
        step = "select_category"
        try:
            if not name:
                return

            page = self._browser.get_page()
            cat_btn_sel = (
                self._config.get("selectors.category_btn", "") or "#category-btn"
            )
            cat_list_sel = (
                self._config.get("selectors.category_list", "") or "#category-list"
            )

            await page.click(cat_btn_sel)
            await page.wait_for_selector(cat_list_sel, timeout=_STEP_TIMEOUT_MS)

            # aria-label 완전일치 — 부분일치("여행"이 "해외여행"에 hit) 차단.
            option = page.locator(
                f"{cat_list_sel} [aria-label]",
                has_text=name,
            )
            count = await option.count()
            if count == 0:
                labels = await page.locator(
                    f"{cat_list_sel} [aria-label]"
                ).evaluate_all("nodes => nodes.map(n => n.getAttribute('aria-label'))")
                raise ValueError(f"카테고리 '{name}' 없음. 사용 가능: {labels}")

            await option.first.click()
            logger.info("단계 완료 (select_category, name_len=%d)", len(name))
        except Exception:
            await self._screenshot_on_error(step)
            raise

    # ------------------------------------------------------------------
    # 단계 6: 첨부파일 업로드
    # ------------------------------------------------------------------

    async def attach_file(self, path: Optional[str], kind: str = "file") -> None:
        """첨부 드롭다운을 열어 해당 kind 메뉴 항목 클릭 → file_chooser 로 업로드.

        Args:
            path: 업로드할 파일 경로. None/빈값이면 조용히 skip.
            kind: "file"/"image"/"slideshow" 중 하나. 그 외는 ValueError.
        """
        step = "attach_file"
        try:
            if not path:
                return

            if kind not in _ATTACH_KIND_TEXT:
                raise ValueError(
                    f"지원하지 않는 attach kind='{kind}' " f"(허용: {list(_ATTACH_KIND_TEXT)})"
                )
            text_for_kind = _ATTACH_KIND_TEXT[kind]

            page = self._browser.get_page()
            attach_btn_sel = (
                self._config.get("selectors.attach_btn", "")
                or 'div[role="button"][aria-label="첨부"]'
            )
            attach_option_prefix = (
                self._config.get("selectors.attach_option_prefix", "")
                or ".mce-tistory-attach-item"
            )

            # DOM 에 숨겨진 동일 요소가 복수 존재(실측 3개 중 1개만 표시).
            # Playwright `:visible` pseudo 는 버전별 동작 차이가 있어
            # 모든 매치를 순회하며 `is_visible()` 로 확인해 첫 번째를 클릭한다.
            candidates = page.locator(attach_btn_sel)
            total = await candidates.count()
            clicked = False
            for idx in range(total):
                cand = candidates.nth(idx)
                if await cand.is_visible():
                    await cand.click()
                    clicked = True
                    break
            if not clicked:
                raise RuntimeError(
                    f"첨부 버튼을 찾지 못했습니다 (selector={attach_btn_sel}, "
                    f"total={total}, visible=0)"
                )

            # has_text 완전일치 — substring 오매치 차단 (예: "슬라이드쇼 파일" ↛ "파일")
            menu_item = page.locator(
                attach_option_prefix,
                has_text=text_for_kind,
            )

            # file_chooser 는 반드시 click 전에 expect_file_chooser 컨텍스트에 진입.
            # 아래 순서가 뒤바뀌면 chooser 이벤트를 놓치고 타임아웃이 발생한다.
            async with page.expect_file_chooser() as fc_info:
                await menu_item.first.click()
            chooser = await fc_info.value
            await chooser.set_files(str(Path(path).resolve()))

            # 업로드 완료 대기 — 카카오 CDN(kage) 업로드 + signed URL 생성까지 수 초 소요.
            # tistory 에디터는 이미지 업로드 중에 `getContent()` 를 호출하면
            # **"이미지 업로드가 완료된 후 시도해 주세요."** 예외를 throw 한다
            # (keditor kImage plugin). 따라서 polling 조건을 try/catch 로 감싸
            # 예외 발생 시 계속 대기하고, 정상 반환 후 kind 별 마커(image: `[##_Image`,
            # file: `[##_File`)가 포함되는지 확인한다.
            kind_marker = {"image": "[##_Image", "file": "[##_File"}.get(kind, "")
            try:
                await page.wait_for_function(
                    """(marker) => {
                        try {
                            const e = window.tinymce && window.tinymce.activeEditor;
                            if (!e) return false;
                            const c = e.getContent();
                            if (marker) return c && c.includes(marker);
                            return true;  // 슬라이드쇼 등 marker 미확정 kind
                        } catch (err) {
                            // 업로드 중: keditor 가 "이미지 업로드가 완료된 후 시도해 주세요" throw
                            return false;
                        }
                    }""",
                    arg=kind_marker,
                    timeout=45000,
                )
                logger.info(
                    "attach_file: 업로드 완료 확인 (kind=%s, marker=%s)",
                    kind,
                    bool(kind_marker),
                )
            except PlaywrightTimeoutError:
                # 45초 타임아웃 — 명시적 실패.
                raise RuntimeError(
                    f"첨부 업로드가 45초 내 완료되지 않았습니다 (kind={kind}, path={path})"
                )
            try:
                await page.wait_for_load_state("networkidle", timeout=_STEP_TIMEOUT_MS)
            except PlaywrightTimeoutError:
                logger.info("attach_file: networkidle 타임아웃 — 무시하고 계속")
            await asyncio.sleep(2)
            logger.info(
                "단계 완료 (attach_file, kind=%s, path_len=%d)",
                kind,
                len(path),
            )
        except Exception:
            await self._screenshot_on_error(step)
            raise

    # ------------------------------------------------------------------
    # 단계 7: 임시저장
    # ------------------------------------------------------------------

    async def save_draft(self) -> bool:
        """임시저장 버튼 클릭 후 networkidle + 2초 sleep.

        예외 없이 종료되면 True 를 반환한다. 실제 임시저장 성공 여부(관리 페이지
        '임시저장된 글' 목록 반영) 는 TASK-013-D (사용자 육안) 에서 검증.
        """
        step = "save_draft"
        try:
            page = self._browser.get_page()
            save_btn_sel = (
                self._config.get("selectors.save_draft_btn", "") or "a.action"
            )

            # has_text 완전일치 — "임시저장 예약" 같은 유사 버튼 오매치 차단.
            save_locator = page.locator(
                save_btn_sel,
                has_text="임시저장",
            )
            await save_locator.first.click()

            # 티스토리 자동저장 등 백그라운드 요청 지속 — networkidle 미도달 가능.
            try:
                await page.wait_for_load_state("networkidle", timeout=_STEP_TIMEOUT_MS)
            except PlaywrightTimeoutError:
                logger.info("save_draft: networkidle 타임아웃 — 무시하고 계속")
            await asyncio.sleep(2)
            logger.info("단계 완료 (save_draft)")
            return True
        except Exception:
            await self._screenshot_on_error(step)
            raise

    # ------------------------------------------------------------------
    # 내부 헬퍼
    # ------------------------------------------------------------------

    async def _screenshot_on_error(self, step_name: str) -> None:
        """단계 실패 시 스크린샷 저장. 저장 자체 실패는 무시(본래 예외 우선)."""
        try:
            path = await self._browser.screenshot(f"tistory_write_{step_name}")
            logger.error("단계 실패 스크린샷 저장: step=%s, path=%s", step_name, path)
        except Exception as exc:  # noqa: BLE001
            logger.error(
                "단계 실패 스크린샷 저장 중 추가 예외 발생 (step=%s): %s",
                step_name,
                exc,
            )


__all__ = ["TistoryWriter"]
