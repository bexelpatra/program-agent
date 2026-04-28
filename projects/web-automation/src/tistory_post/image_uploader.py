"""Tistory `/manage/post/attach.json` 업로더.

이미지 파일 목록을 순차로 tistory CDN 에 업로드하고, 응답을 기반으로
에디터 매크로 문자열(`[##_Image|...CDN key...|CDM|1.3|{...}_##]`) 을 조립해
`UploadedImage` 로 반환한다.

설계 메모
---------
- **브라우저 경유 업로드**: Python 에서 파일을 읽고 base64 로 인코딩한 뒤
  `page.evaluate` 에서 JS `FormData` + `fetch` 로 `/manage/post/attach.json`
  을 호출한다. BrowserContext 의 세션 쿠키가 자동 전파되므로 CSRF/로그인
  처리가 불필요하다 (probe §5 참조).
- **필드명 cache**: tistory multipart 필드명이 서버/스킨별로 `file`/`Filedata`
  중 하나일 수 있어, 최초 성공한 필드명을 모듈 전역 `_SUCCESSFUL_FIELD_NAME`
  에 기록해 후속 이미지 업로드에서 probe 단계를 skip 한다.
- **URL escape 범위**: 응답 `url` query string 의 `&` → `&amp;` 한 글자만
  변환한다. 다른 문자 (`credential` 내 base64 등) 는 이미 percent-encoded
  이므로 재escape 하지 않는다 (probe §1 확인). `macro` 는 이 상태로 반환
  되며 post_builder 는 그대로 본문에 삽입한다 (재escape 금지).
"""

from __future__ import annotations

import base64
import json
import logging
import mimetypes
from pathlib import Path

from PIL import Image

from src.tistory_post.models import PartialUploadError, UploadedImage

logger = logging.getLogger("tistory_post.image_uploader")

# 최초 성공한 multipart 필드명 cache. probe 순서: "file" → "Filedata".
_SUCCESSFUL_FIELD_NAME: str | None = None

# probe 시도 순서.
_FIELD_NAME_CANDIDATES: tuple[str, ...] = ("file", "Filedata")

_ATTACH_ENDPOINT = "/manage/post/attach.json"


async def upload_images(page, image_paths: list[Path]) -> list[UploadedImage]:
    """이미지 파일 리스트를 순차로 tistory CDN 에 업로드.

    Parameters
    ----------
    page:
        로그인된 Playwright Page. BrowserContext 세션 쿠키가 필요하다.
    image_paths:
        업로드할 이미지 파일 경로 리스트. 순서는 그대로 보존된다 (병렬 금지).

    Returns
    -------
    list[UploadedImage]
        입력과 동일 순서의 업로드 결과. `macro` 필드는 `&amp;` escape 완료 상태.

    Raises
    ------
    PartialUploadError
        k-번째 이미지 업로드 실패 시. `uploaded` 에 k 이전까지 성공한 결과가,
        `failed_index` 에 k, `cause` 에 원인 예외가 담긴다.
    """

    uploaded: list[UploadedImage] = []
    for index, image_path in enumerate(image_paths):
        try:
            result = await _upload_single(page, image_path)
        except Exception as exc:  # noqa: BLE001 — 경계에서 PartialUploadError 로 재포장
            logger.error(
                "이미지 업로드 실패 index=%d filename=%s cause=%s",
                index,
                image_path.name,
                exc,
            )
            raise PartialUploadError(
                uploaded=uploaded, failed_index=index, cause=exc
            ) from exc
        uploaded.append(result)
    return uploaded


async def _upload_single(page, image_path: Path) -> UploadedImage:
    """단일 이미지를 업로드하고 매크로를 조립해 UploadedImage 반환."""

    filename = image_path.name
    mime_type = mimetypes.guess_type(filename)[0] or "application/octet-stream"

    width, height = _read_image_dimensions(image_path)
    size_bytes = image_path.stat().st_size
    body_b64 = base64.b64encode(image_path.read_bytes()).decode("ascii")

    logger.info(
        "이미지 업로드 시작 filename=%s size=%d dims=%dx%d",
        filename,
        size_bytes,
        width,
        height,
    )

    response = await _post_multipart_with_field_probe(
        page=page,
        body_b64=body_b64,
        filename=filename,
        mime_type=mime_type,
    )

    macro = _build_macro(
        key=response["key"],
        cdn_filename=response["filename"],
        url=response["url"],
        origin_width=width,
        origin_height=height,
        filename=response["name"],
    )

    logger.info(
        "이미지 업로드 성공 filename=%s key_prefix=%s",
        filename,
        response["key"][:10],
    )

    return UploadedImage(
        key=response["key"],
        url=response["url"],
        filename=response["name"],
        size=response["size"],
        width=width,
        height=height,
        macro=macro,
    )


def _read_image_dimensions(image_path: Path) -> tuple[int, int]:
    """Pillow 로 이미지 픽셀 크기 추출. webp/jpeg/png/gif 지원."""

    with Image.open(image_path) as img:
        return img.size


async def _post_multipart_with_field_probe(
    page,
    body_b64: str,
    filename: str,
    mime_type: str,
) -> dict:
    """multipart 필드명을 probe 하며 `/manage/post/attach.json` 호출.

    1. 모듈 cache `_SUCCESSFUL_FIELD_NAME` 이 있으면 바로 사용.
    2. 없으면 `file` → `Filedata` 순으로 시도.
    3. 둘 다 실패하면 RuntimeError raise (probe route 가로채기는 MVP 미구현).

    Returns
    -------
    dict
        응답 JSON (`name`/`url`/`key`/`filename`/`size` 필드 보장).
    """

    global _SUCCESSFUL_FIELD_NAME

    if _SUCCESSFUL_FIELD_NAME is not None:
        parsed = await _try_post_once(
            page=page,
            body_b64=body_b64,
            filename=filename,
            mime_type=mime_type,
            field_name=_SUCCESSFUL_FIELD_NAME,
        )
        if parsed is not None:
            return parsed
        # cache 가 실패하면 무효화 후 재probe.
        logger.warning("cached fieldName=%s 실패 → 재probe", _SUCCESSFUL_FIELD_NAME)
        _SUCCESSFUL_FIELD_NAME = None

    last_status: int | None = None
    last_body: str | None = None
    for candidate in _FIELD_NAME_CANDIDATES:
        attempt = await _try_post_once(
            page=page,
            body_b64=body_b64,
            filename=filename,
            mime_type=mime_type,
            field_name=candidate,
            capture_failure=True,
        )
        if isinstance(attempt, dict) and "key" in attempt and "url" in attempt:
            _SUCCESSFUL_FIELD_NAME = candidate
            logger.info("multipart fieldName probe 성공: %s", candidate)
            return attempt
        if isinstance(attempt, tuple):
            last_status, last_body = attempt

    # TODO: probe route 가로채기 (page.route) 구현. MVP 에서는 미지원.
    #   이유: UI 업로드 트리거 (attach 메뉴 클릭) 의 사이드이펙트 통제가 복잡해
    #   수동 probe (probe-tistory-api.md L8) 로 fieldName 확정 후 코드 추가
    #   하는 편이 안전. 실제 필요해지면 별도 태스크로 분리.
    body_preview = (last_body or "")[:500]
    raise RuntimeError(
        "multipart field name unknown — probe-tistory-api.md L8 수동 탐색 필요. "
        f"status={last_status}, body={body_preview}"
    )


async def _try_post_once(
    page,
    body_b64: str,
    filename: str,
    mime_type: str,
    field_name: str,
    capture_failure: bool = False,
):
    """단일 시도. 성공이면 dict(parsed JSON) 반환, 실패면 None 또는 (status, body)."""

    js_fetch = """
    async ({b64, filename, mimeType, fieldName, endpoint}) => {
        const bytes = Uint8Array.from(atob(b64), c => c.charCodeAt(0));
        const blob = new Blob([bytes], {type: mimeType});
        const form = new FormData();
        form.append(fieldName, blob, filename);
        const res = await fetch(endpoint, {
            method: 'POST', body: form, credentials: 'include'
        });
        const text = await res.text();
        return {status: res.status, body: text};
    }
    """

    raw = await page.evaluate(
        js_fetch,
        {
            "b64": body_b64,
            "filename": filename,
            "mimeType": mime_type,
            "fieldName": field_name,
            "endpoint": _ATTACH_ENDPOINT,
        },
    )
    status = raw["status"]
    body = raw["body"]

    if 200 <= status < 300:
        try:
            parsed = json.loads(body)
        except json.JSONDecodeError:
            if capture_failure:
                return (status, body)
            return None
        if "key" in parsed and "url" in parsed:
            return parsed

    if capture_failure:
        logger.error(
            "attach.json 실패 fieldName=%s status=%d body_preview=%s",
            field_name,
            status,
            body[:200],
        )
        return (status, body)
    return None


def _build_macro(
    key: str,
    cdn_filename: str,
    url: str,
    origin_width: int,
    origin_height: int,
    filename: str,
) -> str:
    """tistory 에디터 매크로 문자열 조립 (probe §1 공식).

    매크로 경로는 `kage@{key}/{cdn_filename}` 형태다. attach.json 응답의
    `key` 필드에는 CDN 디렉토리 경로만 들어오고, 실제 파일 이름(`img.png`)은
    별도 `filename` 필드로 돌아오므로 조립 시 이를 합쳐야 한다. 이 step 을
    빠뜨리면 매크로 URL 이 불완전해 tistory 에디터가 렌더링에 실패한다.

    `url` query string 의 `&` 만 `&amp;` 로 치환한다. 다른 문자 변환 금지.
    JSON 블록 `filename` 은 **원본 업로드 이름** (response `name`) 이며
    한글 등을 보존하기 위해 `ensure_ascii=False` 로 직렬화한다.
    """

    _, _, query_raw = url.partition("?")
    escaped_query = query_raw.replace("&", "&amp;")

    json_block = json.dumps(
        {
            "originWidth": origin_width,
            "originHeight": origin_height,
            "style": "alignCenter",
            "filename": filename,
        },
        ensure_ascii=False,
    )

    return (
        f"[##_Image|kage@{key}/{cdn_filename}?{escaped_query}"
        f"|CDM|1.3|{json_block}_##]"
    )
