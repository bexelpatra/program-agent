"""post_builder.build_payload 단위 테스트.

LoadedPost + list[UploadedImage] + category_map → DraftPayload 조립 정확성을 검증한다.
네트워크 / 외부 시스템 의존성 없음. pytest 전용.

실행:
    PYTHONPATH="$(pwd)" PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
        python3 -m pytest tests/test_post_builder.py -v
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

# 프로젝트 src 를 import path 에 추가 (테스트 단독 실행 대비).
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from src.tistory_post.models import (  # noqa: E402
    DraftPayload,
    LoadedPost,
    Marker,
    UploadedImage,
)
from src.tistory_post.post_builder import build_payload  # noqa: E402


# ---------------------------------------------------------------------------
# 헬퍼 — 픽스처 공장 함수
# ---------------------------------------------------------------------------


def _macro(key: str, filename: str, width: int = 100, height: int = 100) -> str:
    """실제 image_uploader 출력과 유사한 매크로 문자열 (`&amp;` escape 포함).

    `|` · `{` · `}` · `"` 가 다수 포함되어 markdown 파서가 본문으로 오해해 왜곡할 수 있는 케이스를
    일부러 구성한다 (placeholder 우회 기법 회귀 테스트).
    """
    json_block = (
        '{"originWidth":'
        + str(width)
        + ',"originHeight":'
        + str(height)
        + ',"style":"alignCenter","filename":"'
        + filename
        + '"}'
    )
    query = "credential=abc&amp;expires=123&amp;signature=xyz"
    return f"[##_Image|kage@test/{key}?{query}|CDM|1.3|{json_block}_##]"


def _uploaded(
    key: str,
    filename: str,
    width: int = 100,
    height: int = 100,
) -> UploadedImage:
    return UploadedImage(
        key=key,
        url=f"https://cdn.example/test/{key}?credential=abc&expires=123&signature=xyz",
        filename=filename,
        size=1024,
        width=width,
        height=height,
        macro=_macro(key, filename, width, height),
    )


def _loaded(
    body_markdown: str,
    markers: list[Marker],
    images: dict[str, Path],
    *,
    title: str = "제목",
    category_name: str | None = "메모",
    tags: list[str] | None = None,
) -> LoadedPost:
    return LoadedPost(
        title=title,
        category_name=category_name,
        tags=list(tags) if tags is not None else ["a", "b"],
        body_markdown=body_markdown,
        markers=markers,
        images=images,
        folder=Path("/fake/folder"),
        skip=False,
    )


# ---------------------------------------------------------------------------
# 1) 정상 케이스 — 2 markers (`${1}` + `${hello.png}`) + 2 uploads
# ---------------------------------------------------------------------------


def test_build_payload_happy_path() -> None:
    body = "첫 문단입니다.\n\n" "첫 번째 이미지 → ${1}\n\n" "두 번째 이미지는 파일명 → ${hello.png}\n"
    markers = [
        Marker(raw_token="${1}", kind="index", value=1, position=body.find("${1}")),
        Marker(
            raw_token="${hello.png}",
            kind="filename",
            value="hello.png",
            position=body.find("${hello.png}"),
        ),
    ]
    # sorted_filenames 순서: 1.png < hello.png (사전순)
    images = {
        "1.png": Path("/fake/1.png"),
        "hello.png": Path("/fake/hello.png"),
    }
    # image_uploader 는 post.images.values() 순서 (정렬은 loader 책임) 대로 업로드하므로
    # uploads 순서는 1.png, hello.png 와 동일하게 맞춘다.
    uploads = [
        _uploaded("k1", "1.png"),
        _uploaded("k2", "hello.png"),
    ]
    post = _loaded(body, markers, images)

    payload = build_payload(post, uploads, {"메모": 944981})

    assert isinstance(payload, DraftPayload)
    assert payload.title == "제목"
    assert payload.categoryId == 944981
    assert payload.tags == "a,b"
    assert payload.thumbnail == "k1"
    assert payload.draftSequence is None
    # content 에 두 매크로가 모두 포함되어야 한다.
    assert uploads[0].macro in payload.content
    assert uploads[1].macro in payload.content
    # markdown 으로 변환된 paragraph 태그가 포함
    assert "<p>" in payload.content
    # 원본 마커 토큰은 남아있지 않아야 한다.
    assert "${1}" not in payload.content
    assert "${hello.png}" not in payload.content


# ---------------------------------------------------------------------------
# 2) category_name=None → categoryId=0
# ---------------------------------------------------------------------------


def test_build_payload_none_category_yields_zero() -> None:
    post = _loaded(
        body_markdown="본문만.",
        markers=[],
        images={},
        category_name=None,
        tags=[],
    )
    payload = build_payload(post, [], {"메모": 1, "기타": 2})

    assert payload.categoryId == 0
    assert payload.tags == ""
    assert payload.thumbnail is None


# ---------------------------------------------------------------------------
# 3) category_map 미매치 → ValueError + 사용 가능 목록 노출
# ---------------------------------------------------------------------------


def test_build_payload_raises_on_unknown_category() -> None:
    post = _loaded(
        body_markdown="본문.",
        markers=[],
        images={},
        category_name="없는카테고리",
        tags=[],
    )
    with pytest.raises(ValueError) as excinfo:
        build_payload(post, [], {"메모": 1, "일기": 2})

    msg = str(excinfo.value)
    assert "없는카테고리" in msg
    # 사용 가능 목록이 sorted 로 노출되어야 한다.
    assert "메모" in msg
    assert "일기" in msg


# ---------------------------------------------------------------------------
# 4) uploads 와 markers 개수 불일치 (참조 파일명이 uploads 에 없음) → ValueError
# ---------------------------------------------------------------------------


def test_build_payload_raises_when_upload_missing_for_marker() -> None:
    body = "이미지 없음 ${missing.png} 끝."
    markers = [
        Marker(
            raw_token="${missing.png}",
            kind="filename",
            value="missing.png",
            position=body.find("${missing.png}"),
        ),
    ]
    images = {"missing.png": Path("/fake/missing.png")}
    post = _loaded(body, markers, images)

    # uploads 에는 전혀 다른 파일만 있음
    uploads = [_uploaded("k_other", "other.png")]

    with pytest.raises(ValueError) as excinfo:
        build_payload(post, uploads, {"메모": 1})

    msg = str(excinfo.value)
    assert "upload 매칭 실패" in msg
    assert "missing.png" in msg


# ---------------------------------------------------------------------------
# 5) 빈 uploads + 빈 markers → thumbnail=None, content 에 매크로 없음
# ---------------------------------------------------------------------------


def test_build_payload_empty_uploads_and_markers() -> None:
    body = "이미지 없는 본문. **굵게**."
    post = _loaded(body, [], {}, tags=["only"])

    payload = build_payload(post, [], {"메모": 1})

    assert payload.thumbnail is None
    assert payload.tags == "only"
    # markdown 변환이 수행됐는지 확인 (strong 태그)
    assert "<strong>" in payload.content
    # 어떤 매크로도 없음
    assert "[##_Image" not in payload.content
    assert "@@TISTORY_MACRO_" not in payload.content


# ---------------------------------------------------------------------------
# 6) 동일 filename 마커 중복 (${1} 두 번) → content 에 매크로 2번 등장
# ---------------------------------------------------------------------------


def test_build_payload_duplicate_marker_appears_twice() -> None:
    body = "처음 ${1} 중간 ${1} 끝."
    markers = [
        Marker(raw_token="${1}", kind="index", value=1, position=body.find("${1}")),
        Marker(
            raw_token="${1}",
            kind="index",
            value=1,
            position=body.find("${1}", body.find("${1}") + 1),
        ),
    ]
    images = {"1.png": Path("/fake/1.png")}
    uploads = [_uploaded("dup_key", "1.png")]
    post = _loaded(body, markers, images)

    payload = build_payload(post, uploads, {"메모": 1})

    assert payload.content.count(uploads[0].macro) == 2
    assert "${1}" not in payload.content


# ---------------------------------------------------------------------------
# 7) 매크로 내 `|`·`{`·`}` 가 markdown 파서에 왜곡되지 않음 (placeholder 우회 검증)
# ---------------------------------------------------------------------------


def test_build_payload_macro_with_markdown_special_chars_preserved() -> None:
    body = "본문 시작.\n\n이미지 → ${1}\n\n본문 끝."
    markers = [
        Marker(raw_token="${1}", kind="index", value=1, position=body.find("${1}")),
    ]
    images = {"complex.png": Path("/fake/complex.png")}
    # macro 에 `|` 3개, `{`/`}` 다수, `"`, `_` 가 포함되어 있음 (_macro 헬퍼 참조)
    uploads = [_uploaded("complex_key", "complex.png")]
    post = _loaded(body, markers, images)

    payload = build_payload(post, uploads, {"메모": 1})

    # 매크로가 **원본 그대로** content 에 존재해야 한다 — markdown 파서가 `|` 를 표 셀 구분자로,
    # `{` `}` 를 attribute syntax 로, `_` 를 emphasis 로 해석해 왜곡하는 일이 없어야 한다.
    assert uploads[0].macro in payload.content
    # `&amp;` escape 상태가 그대로 보존되어야 한다 (재escape / un-escape 금지 계약).
    assert "&amp;" in payload.content
    # placeholder 가 남아있지 않아야 한다.
    assert "@@TISTORY_MACRO_" not in payload.content


# ---------------------------------------------------------------------------
# 8) index 마커의 값이 범위를 초과할 때 ValueError
# ---------------------------------------------------------------------------


def test_build_payload_raises_on_out_of_range_index() -> None:
    body = "이미지 → ${5}"
    markers = [
        Marker(raw_token="${5}", kind="index", value=5, position=body.find("${5}")),
    ]
    # 이미지는 1개만 — loader 단에서 걸러야 하지만, 방어적으로 post_builder 도 ValueError 를 내야 한다.
    images = {"only.png": Path("/fake/only.png")}
    uploads = [_uploaded("k_only", "only.png")]
    post = _loaded(body, markers, images)

    with pytest.raises(ValueError) as excinfo:
        build_payload(post, uploads, {"메모": 1})

    assert "upload 매칭 실패" in str(excinfo.value)
