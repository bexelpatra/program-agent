"""Phase 7 폴더 기반 임시저장 자동화 — post.md + 이미지 파싱 로더.

`posts/{YYYY-MM-DD}-{slug}/` 폴더를 입력받아 YAML frontmatter, 본문, 이미지,
`${...}` 마커를 추출하고 LoadedPost 로 반환한다. post_runner 의 첫 단계.
"""

from __future__ import annotations

import logging
import re
from pathlib import Path

import yaml

from src.tistory_post.models import LoadedPost, Marker

logger = logging.getLogger("tistory_post.post_loader")


# 본문 내 `${...}` 마커 추출. `[^}]*` 로 중첩 없는 단일 마커만 허용.
_MARKER_PATTERN = re.compile(r"\$\{([^}]*)\}")

# 폴더 수집 대상 이미지 확장자 (대소문자 무관 비교).
_IMAGE_EXTENSIONS: frozenset[str] = frozenset(
    {".png", ".jpg", ".jpeg", ".gif", ".webp"}
)

# frontmatter 구분자.
_FRONTMATTER_DELIM = "---"


def load_post(folder: Path) -> LoadedPost:
    """폴더 하나를 LoadedPost 로 파싱한다.

    `.published` 존재 시 즉시 skip 반환. 그 외에는 post.md frontmatter 와
    본문을 읽고, 이미지 파일들을 사전순 수집한 뒤, `${...}` 마커를 파일에
    매핑한다. 검증 실패 시 ValueError, post.md 부재 시 FileNotFoundError.
    """
    folder = Path(folder)

    if (folder / ".published").exists():
        logger.info("skip(.published) folder=%s", folder)
        return LoadedPost(
            title="",
            category_name=None,
            tags=[],
            body_markdown="",
            markers=[],
            images={},
            folder=folder,
            skip=True,
        )

    post_md = folder / "post.md"
    if not post_md.exists():
        raise FileNotFoundError(f"post.md 없음: {folder}")

    raw_text = post_md.read_text(encoding="utf-8")

    title, category_name, tags, body_markdown = _split_frontmatter(raw_text)

    images_sorted = _collect_images(folder)

    markers = _extract_markers(body_markdown)

    resolved_images = _resolve_markers(markers, images_sorted, folder)

    _warn_orphan_images(images_sorted, resolved_images)

    logger.info(
        "loaded folder=%s title_len=%d markers=%d images=%d",
        folder,
        len(title),
        len(markers),
        len(resolved_images),
    )

    return LoadedPost(
        title=title,
        category_name=category_name,
        tags=tags,
        body_markdown=body_markdown,
        markers=markers,
        images=resolved_images,
        folder=folder,
        skip=False,
    )


# ---------------------------------------------------------------------------
# frontmatter
# ---------------------------------------------------------------------------


def _split_frontmatter(
    raw_text: str,
) -> tuple[str, str | None, list[str], str]:
    """post.md 원문을 frontmatter + 본문으로 분리한다.

    반환: (title, category_name, tags, body_markdown)
    """
    lines = raw_text.splitlines(keepends=True)
    if not lines or lines[0].rstrip("\r\n") != _FRONTMATTER_DELIM:
        raise ValueError("post.md 첫 줄이 '---' 가 아닙니다")

    closing_index: int | None = None
    for i in range(1, len(lines)):
        if lines[i].rstrip("\r\n") == _FRONTMATTER_DELIM:
            closing_index = i
            break

    if closing_index is None:
        raise ValueError("post.md frontmatter 닫는 '---' 가 없습니다")

    frontmatter_text = "".join(lines[1:closing_index])
    body_markdown = "".join(lines[closing_index + 1 :])

    parsed = yaml.safe_load(frontmatter_text) or {}
    if not isinstance(parsed, dict):
        raise ValueError("frontmatter 는 YAML 매핑(dict) 이어야 합니다")

    title_raw = parsed.get("title")
    if title_raw is None or str(title_raw).strip() == "":
        raise ValueError("frontmatter 에 title 필수")
    title = str(title_raw)

    category_raw = parsed.get("category")
    category_name: str | None
    if category_raw is None:
        category_name = None
    else:
        category_name = str(category_raw)

    tags_raw = parsed.get("tags", [])
    if tags_raw is None:
        tags: list[str] = []
    elif isinstance(tags_raw, list):
        tags = [str(t) for t in tags_raw]
    else:
        raise ValueError("tags 는 list")

    if body_markdown.strip() == "":
        raise ValueError("본문이 비어있음")

    return title, category_name, tags, body_markdown


# ---------------------------------------------------------------------------
# 이미지 수집
# ---------------------------------------------------------------------------


def _collect_images(folder: Path) -> list[Path]:
    """폴더에서 이미지 파일을 사전순으로 수집해 반환한다.

    수집 규칙 (우선순위 고정):
        1. `{folder}/imgs/` 가 존재하면 **그 안의 이미지만** 수집.
        2. 없으면 `{folder}/` 바로 아래의 이미지를 수집 (하위 호환).

    여러 이미지를 관리할 때는 `imgs/` 서브폴더 사용을 권장한다.
    """
    subdir = folder / "imgs"
    source = subdir if subdir.is_dir() else folder
    candidates = [
        entry
        for entry in source.iterdir()
        if entry.is_file() and entry.suffix.lower() in _IMAGE_EXTENSIONS
    ]
    return sorted(candidates, key=lambda p: p.name)


# ---------------------------------------------------------------------------
# 마커 추출 + 매핑
# ---------------------------------------------------------------------------


def _extract_markers(body_markdown: str) -> list[Marker]:
    """본문의 `${...}` 마커를 등장 순서대로 Marker 리스트로 반환한다."""
    markers: list[Marker] = []
    for match in _MARKER_PATTERN.finditer(body_markdown):
        content = match.group(1)
        raw_token = match.group(0)
        position = match.start()

        if content == "":
            raise ValueError(f"빈 마커 ${{}} position={position}")

        kind, value = _classify_marker_content(content)

        markers.append(
            Marker(raw_token=raw_token, kind=kind, value=value, position=position)
        )
    return markers


def _classify_marker_content(content: str) -> tuple[str, int | str]:
    """마커 내용을 (kind, value) 로 분류한다.

    - 양의 정수 → ("index", N).
    - 0 또는 음의 정수 → ValueError.
    - 그 외 → ("filename", content).
    """
    # `${-1}` 같은 signed integer 도 검출해 ValueError 로 돌린다.
    if _looks_like_integer(content):
        number = int(content)
        if number <= 0:
            raise ValueError(f"${{{content}}} 은 1-based 양의 정수")
        return "index", number

    return "filename", content


def _looks_like_integer(text: str) -> bool:
    """`123`, `-1`, `+5` 같은 순수 정수 리터럴인지 확인한다."""
    if text == "":
        return False
    head = text[0]
    body = text[1:] if head in ("+", "-") else text
    return body.isdigit() and body != ""


def _resolve_markers(
    markers: list[Marker],
    images_sorted: list[Path],
    folder: Path,
) -> dict[str, Path]:
    """각 마커를 이미지 파일에 매핑한다. 실패 시 ValueError.

    반환: 매핑된 파일만 포함하는 dict (filename → absolute Path).
    중복 마커는 같은 key 로 덮어쓴다 (허용).
    """
    resolved: dict[str, Path] = {}
    name_to_path = {p.name: p for p in images_sorted}

    for marker in markers:
        target = _resolve_single_marker(marker, images_sorted, name_to_path, folder)
        resolved[target.name] = target.resolve()

    return resolved


def _resolve_single_marker(
    marker: Marker,
    images_sorted: list[Path],
    name_to_path: dict[str, Path],
    folder: Path,
) -> Path:
    """마커 하나를 실제 이미지 Path 로 해석한다."""
    if marker.kind == "index":
        index_value = int(marker.value)
        if index_value > len(images_sorted):
            raise ValueError(f"고아 마커: {marker.raw_token} 지만 이미지 {len(images_sorted)} 개")
        return images_sorted[index_value - 1]

    # kind == "filename"
    filename = str(marker.value)
    if filename in name_to_path:
        return name_to_path[filename]

    available = sorted(name_to_path.keys())
    raise ValueError(f"이미지 파일 없음: {filename}. 폴더 내: {available} (folder={folder})")


# ---------------------------------------------------------------------------
# 고아 이미지 경고
# ---------------------------------------------------------------------------


def _warn_orphan_images(
    images_sorted: list[Path], resolved_images: dict[str, Path]
) -> None:
    """마커에 참조되지 않은 이미지를 warning 으로 기록한다."""
    referenced = set(resolved_images.keys())
    orphans = [p.name for p in images_sorted if p.name not in referenced]
    if orphans:
        logger.warning("orphan images (마커 미참조): %s", orphans)
