"""티스토리 카테고리 이름 → id 매핑 추출.

`/manage/newpost` 페이지에서 `#category-btn` 클릭 후 동적으로 나타나는
`#category-list` DOM 에서 각 옵션의 `aria-label` (카테고리 이름) 과
`category-id` (DOM custom attribute) 를 읽어 dict 로 돌려준다.

카테고리 이름과 id 는 블로그마다 다르고 사용자가 수시로 바꿀 수 있으므로
하드코딩하지 않고 실행 시점에 UI 에서 추출한다 (probe-tistory-api.md §4).
"""

from __future__ import annotations

import logging

logger = logging.getLogger("tistory_post.category_fetcher")


async def fetch_category_map(page, blog_name: str) -> dict[str, int]:
    """`#category-list` 에서 이름 → id 매핑을 추출해 반환한다.

    Args:
        page: 로그인된 Playwright Page.
        blog_name: 티스토리 블로그 이름 (config `blog.blog_name`).
            이미 해당 블로그 `/manage/newpost` 에 있으면 드롭다운만 연다.

    Returns:
        `{"카테고리 없음": 0, "메모": 944981, ...}` 형태의 dict.
        드롭다운에 옵션이 하나도 없으면 `{"카테고리 없음": 0}` 폴백.
    """
    target_prefix = f"https://{blog_name}.tistory.com/manage/newpost"
    if not (page.url or "").startswith(target_prefix):
        await page.goto(target_prefix)

    await page.wait_for_selector("#category-btn", timeout=15000)
    await page.click("#category-btn")
    await page.wait_for_selector("#category-list", timeout=15000)

    raw = await page.evaluate(
        """() => {
            const list = document.querySelector('#category-list');
            if (!list) return [];
            return Array.from(list.querySelectorAll('[aria-label][category-id]')).map(n => ({
                name: n.getAttribute('aria-label'),
                id: n.getAttribute('category-id'),
            }));
        }"""
    )

    mapping: dict[str, int] = {}
    for item in raw:
        name = (item.get("name") or "").strip()
        raw_id = item.get("id") or ""
        if not name:
            continue
        try:
            mapping[name] = int(raw_id)
        except ValueError:
            logger.warning("categoryId 변환 실패 (name=%s, raw=%r) — skip", name, raw_id)

    if not mapping:
        logger.warning("#category-list 비어있음 — '카테고리 없음' 폴백 반환")
        mapping = {"카테고리 없음": 0}

    logger.info("카테고리 맵 추출 완료 (%d개)", len(mapping))
    return mapping


__all__ = ["fetch_category_map"]
