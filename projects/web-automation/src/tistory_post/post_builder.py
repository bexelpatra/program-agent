"""Phase 7 폴더 기반 임시저장 자동화 — DraftPayload 조립 모듈.

`build_payload(post, uploads, category_map) -> DraftPayload` 한 함수만 공개한다.

핵심 단계:
1. `post.markers` 의 각 `${...}` 토큰을 대응하는 `UploadedImage.macro` 로 치환한다.
2. 매크로 안의 markdown 특수문자(`|`, `{`, `}`, `_`, `*` 등)가 markdown 파서에 왜곡되지 않도록
   placeholder 우회 기법을 사용한다: macro → `@@TISTORY_MACRO_{uuid}@@` → markdown 변환 → 역치환.
3. markdown → HTML 변환은 python-markdown 에 `extra` + `nl2br` 확장을 적용해 수행.
4. `category_name` 과 `category_map` 대조로 `categoryId` 를 확정 (None → 0, 미매치 → ValueError).
5. `tags` 는 쉼표 join, `thumbnail` 은 `uploads[0].key or None`.

UploadedImage.macro 는 image_uploader 가 이미 `&amp;` escape 를 완료한 상태이므로
post_builder 에서는 **재escape 금지**. placeholder 역치환 시 원본 macro 가 그대로 복원되어야 한다.
"""

from __future__ import annotations

import logging
import uuid

import markdown

from src.tistory_post.models import DraftPayload, LoadedPost, UploadedImage

logger = logging.getLogger("tistory_post.post_builder")


_PLACEHOLDER_TEMPLATE = "@@TISTORY_MACRO_{token}@@"


def build_payload(
    post: LoadedPost,
    uploads: list[UploadedImage],
    category_map: dict[str, int],
) -> DraftPayload:
    """LoadedPost + uploads + category_map → DraftPayload.

    Args:
        post: post_loader.load_post 결과.
        uploads: image_uploader.upload_images 결과. macro 는 `&amp;` escape 완료 상태.
        category_map: category_fetcher.fetch_category_map 결과 (name → id).

    Returns:
        DraftPayload. draftSequence 는 항상 None (caller 가 필요 시 주입).

    Raises:
        ValueError: upload 매칭 실패 / 카테고리 미매치 / 정수 마커 인덱스 out-of-range.
    """
    logger.info(
        "build 시작: title_len=%d markers=%d uploads=%d",
        len(post.title),
        len(post.markers),
        len(uploads),
    )

    macro_by_filename = {u.filename: u.macro for u in uploads}
    sorted_filenames = sorted(post.images.keys())

    body_with_placeholders, placeholder_to_macro = _replace_markers_with_placeholders(
        body=post.body_markdown,
        markers=post.markers,
        macro_by_filename=macro_by_filename,
        sorted_filenames=sorted_filenames,
    )

    html = markdown.markdown(body_with_placeholders, extensions=["extra", "nl2br"])

    for placeholder, macro in placeholder_to_macro.items():
        html = html.replace(placeholder, macro)

    category_id = _resolve_category_id(post.category_name, category_map)
    tags_str = ",".join(post.tags)
    thumbnail = uploads[0].key if uploads else None

    logger.info(
        "build 완료: content_len=%d categoryId=%d thumbnail=%s",
        len(html),
        category_id,
        thumbnail,
    )

    return DraftPayload(
        title=post.title,
        content=html,
        tags=tags_str,
        categoryId=category_id,
        thumbnail=thumbnail,
        draftSequence=None,
    )


def _replace_markers_with_placeholders(
    body: str,
    markers: list,
    macro_by_filename: dict[str, str],
    sorted_filenames: list[str],
) -> tuple[str, dict[str, str]]:
    """각 Marker 의 raw_token 을 unique placeholder 로 전역 치환한다.

    한 raw_token 이 본문에 여러 번 등장해도 `str.replace` 는 전부 치환하므로
    이미 처리된 raw_token 은 매핑 dict 에 캐시해 중복 작업을 방지한다.

    Returns:
        (body_with_placeholders, placeholder_to_macro)
    """
    result = body
    placeholder_to_macro: dict[str, str] = {}
    token_to_placeholder: dict[str, str] = {}

    for marker in markers:
        if marker.raw_token in token_to_placeholder:
            continue

        filename = _resolve_marker_filename(marker, sorted_filenames)
        macro = macro_by_filename.get(filename)
        if macro is None:
            raise ValueError(
                f"upload 매칭 실패: {filename} (uploads: {list(macro_by_filename)})"
            )

        placeholder = _PLACEHOLDER_TEMPLATE.format(token=uuid.uuid4().hex)
        result = result.replace(marker.raw_token, placeholder)

        token_to_placeholder[marker.raw_token] = placeholder
        placeholder_to_macro[placeholder] = macro

    return result, placeholder_to_macro


def _resolve_marker_filename(marker, sorted_filenames: list[str]) -> str:
    """Marker.kind 에 따라 대응 파일명을 결정한다."""
    if marker.kind == "filename":
        return str(marker.value)

    # kind == "index": 1-based
    index = int(marker.value)
    if index < 1 or index > len(sorted_filenames):
        raise ValueError(
            f"upload 매칭 실패: index {index} 범위 초과 "
            f"(사용 가능 이미지 수={len(sorted_filenames)}, files={sorted_filenames})"
        )
    return sorted_filenames[index - 1]


def _resolve_category_id(
    category_name: str | None,
    category_map: dict[str, int],
) -> int:
    """category_name → categoryId. None 이면 0, 미매치면 ValueError."""
    if category_name is None:
        return 0

    category_id = category_map.get(category_name)
    if category_id is None:
        raise ValueError(
            f"카테고리 '{category_name}' 없음. 사용 가능: {sorted(category_map.keys())}"
        )
    return category_id
