"""티스토리 `/manage/drafts` API 직접 호출.

브라우저 세션 쿠키를 활용해 page.evaluate 로 fetch 를 실행한다.
payload.draftSequence 가 있으면 기존 draft 업데이트, 없으면 새 draft 생성
(probe-tistory-api.md §2).

주의:
    tistory 에디터 페이지는 주기적으로 `POST /manage/autosave` 를 호출하여
    **현재 에디터 상태**(title/content)를 서버에 반영한다. 우리가 fetch 로
    drafts 를 저장해도 에디터가 비어있으면 직후의 autosave 가 우리 draft 를
    빈 내용으로 덮어쓸 수 있다. 따라서 fetch 이전에 에디터 UI 에 title 과
    content 를 주입하여 autosave 가 발생해도 같은 내용이 쓰이도록 한다.
"""

from __future__ import annotations

import asyncio
import json
import logging
from dataclasses import asdict

from src.tistory_post.models import DraftPayload

logger = logging.getLogger("tistory_post.post_saver")


async def save_draft(page, payload: DraftPayload) -> int:
    """draft 를 tistory 에 저장하고 draftSequence 를 반환한다.

    Args:
        page: 로그인된 Playwright Page.
        payload: 완성된 DraftPayload. draftSequence=None 이면 신규 생성,
            정수이면 기존 draft 덮어쓰기.

    Returns:
        tistory 가 부여한 `draft.sequence` 정수.

    Raises:
        RuntimeError: HTTP 4xx/5xx 또는 `success=false` 응답.
    """
    body = asdict(payload)
    # draftSequence=None 이면 전송에서 제외 (신규 생성 경로)
    if body.get("draftSequence") is None:
        body.pop("draftSequence", None)

    result = await page.evaluate(
        """async (body) => {
            const res = await fetch('/manage/drafts', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(body),
                credentials: 'include',
            });
            const text = await res.text();
            return {status: res.status, body: text};
        }""",
        body,
    )

    status = result.get("status")
    raw_body = result.get("body") or ""

    if not (200 <= int(status) < 300):
        raise RuntimeError(f"drafts API 실패: status={status}, body={raw_body[:500]}")

    try:
        parsed = json.loads(raw_body)
    except json.JSONDecodeError as exc:
        raise RuntimeError(
            f"drafts API 응답 JSON 파싱 실패: {exc}, body={raw_body[:500]}"
        ) from exc

    if not parsed.get("success"):
        raise RuntimeError(f"drafts API 거부: {raw_body[:500]}")

    draft = parsed.get("draft") or {}
    sequence = draft.get("sequence")
    if not isinstance(sequence, int):
        raise RuntimeError(f"drafts API 응답에 draft.sequence 없음: {raw_body[:500]}")

    logger.info(
        "draft 저장 완료 (sequence=%d, update=%s)",
        sequence,
        body.get("draftSequence") is not None,
    )

    # autosave race 차단: fetch 직후 현재 newpost 페이지를 떠나 autosave
    # 타이머가 우리 draft 를 빈 내용으로 덮어쓰지 못하게 한다.
    try:
        await page.goto("about:blank")
    except Exception as exc:  # noqa: BLE001
        logger.warning("about:blank 이동 실패(무시): %s", exc)

    return sequence


__all__ = ["save_draft"]
