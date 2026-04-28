"""post_loader.load_post 단위 테스트.

Phase 7 폴더 기반 자동화의 로더 동작을 tmp_path fixture 로 검증한다.
네트워크 / 외부 시스템 의존성 없음. pytest 전용.

실행:
    pytest projects/web-automation/tests/test_post_loader.py -v
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path

import pytest

# 프로젝트 src 를 import path 에 추가 (테스트 단독 실행 대비).
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from src.tistory_post.post_loader import load_post  # noqa: E402


# ---------------------------------------------------------------------------
# 헬퍼
# ---------------------------------------------------------------------------


def _write_post_md(folder: Path, content: str) -> None:
    """post.md 파일을 UTF-8 로 기록한다."""
    (folder / "post.md").write_text(content, encoding="utf-8")


def _touch_png(folder: Path, name: str) -> Path:
    """최소 크기의 fake PNG (이미지 바이트 무결성은 loader 관심사 아님).

    post_loader 는 파일 존재 여부와 확장자만 보고, Pillow 로 열지 않는다.
    """
    path = folder / name
    # 실제 PNG 시그니처는 불필요 — loader 는 확장자만 체크. 빈 파일로 충분.
    path.write_bytes(b"")
    return path


# ---------------------------------------------------------------------------
# 1) 정상 케이스
# ---------------------------------------------------------------------------


def test_load_post_happy_path(tmp_path: Path) -> None:
    folder = tmp_path / "2026-04-22-hello"
    folder.mkdir()
    _touch_png(folder, "1.png")
    _touch_png(folder, "hello.png")
    _write_post_md(
        folder,
        "---\n"
        'title: "안녕"\n'
        'category: "메모"\n'
        'tags: ["t1", "t2"]\n'
        "---\n"
        "\n"
        "본문 시작. 이미지 → ${1}\n"
        "\n"
        "파일명 마커 → ${hello.png}\n",
    )

    result = load_post(folder)

    assert result.skip is False
    assert result.title == "안녕"
    assert result.category_name == "메모"
    assert result.tags == ["t1", "t2"]
    assert "본문 시작" in result.body_markdown
    assert len(result.markers) == 2

    # 첫 마커: index=1
    assert result.markers[0].raw_token == "${1}"
    assert result.markers[0].kind == "index"
    assert result.markers[0].value == 1

    # 두 번째 마커: filename
    assert result.markers[1].raw_token == "${hello.png}"
    assert result.markers[1].kind == "filename"
    assert result.markers[1].value == "hello.png"

    # images dict 에 두 파일이 매핑되어 있어야 한다.
    assert set(result.images.keys()) == {"1.png", "hello.png"}
    for name, abs_path in result.images.items():
        assert abs_path.is_absolute()
        assert abs_path.name == name

    assert result.folder == folder


# ---------------------------------------------------------------------------
# 2) .published → skip
# ---------------------------------------------------------------------------


def test_load_post_skip_when_published_marker_exists(tmp_path: Path) -> None:
    folder = tmp_path / "2026-04-22-done"
    folder.mkdir()
    (folder / ".published").write_text("2026-04-22T15:00:00", encoding="utf-8")
    # post.md 부재 + 이미지 0개여도 skip 분기가 먼저 타야 한다.

    result = load_post(folder)

    assert result.skip is True
    assert result.folder == folder
    # 나머지 필드는 dummy — 테스트는 skip 플래그만 검증.


# ---------------------------------------------------------------------------
# 3) title 누락 → ValueError
# ---------------------------------------------------------------------------


def test_load_post_raises_when_title_missing(tmp_path: Path) -> None:
    folder = tmp_path / "no-title"
    folder.mkdir()
    _write_post_md(
        folder,
        "---\n" 'category: "메모"\n' "---\n" "\n" "본문만 있음\n",
    )

    with pytest.raises(ValueError, match="title"):
        load_post(folder)


# ---------------------------------------------------------------------------
# 4) 본문 비어있음 → ValueError
# ---------------------------------------------------------------------------


def test_load_post_raises_when_body_empty(tmp_path: Path) -> None:
    folder = tmp_path / "empty-body"
    folder.mkdir()
    _write_post_md(
        folder,
        "---\n" 'title: "제목"\n' "---\n" "\n" "   \n",
    )

    with pytest.raises(ValueError, match="본문"):
        load_post(folder)


# ---------------------------------------------------------------------------
# 5) ${} 빈 마커 → ValueError
# ---------------------------------------------------------------------------


def test_load_post_raises_on_empty_marker(tmp_path: Path) -> None:
    folder = tmp_path / "empty-marker"
    folder.mkdir()
    _touch_png(folder, "1.png")
    _write_post_md(
        folder,
        "---\n" 'title: "제목"\n' "---\n" "\n" "본문에 빈 마커 ${} 포함.\n",
    )

    with pytest.raises(ValueError, match="빈 마커"):
        load_post(folder)


# ---------------------------------------------------------------------------
# 6) ${0} / ${-1} → ValueError
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("bad_content", ["0", "-1", "-5"])
def test_load_post_raises_on_non_positive_index(
    tmp_path: Path, bad_content: str
) -> None:
    folder = tmp_path / f"bad-{bad_content}"
    folder.mkdir()
    _touch_png(folder, "1.png")
    _write_post_md(
        folder,
        "---\n" 'title: "제목"\n' "---\n" "\n" f"본문에 잘못된 인덱스 ${{{bad_content}}} 포함.\n",
    )

    with pytest.raises(ValueError, match="1-based"):
        load_post(folder)


# ---------------------------------------------------------------------------
# 7) 고아 마커 (${5} 인데 이미지 3개) → ValueError
# ---------------------------------------------------------------------------


def test_load_post_raises_on_orphan_index_marker(tmp_path: Path) -> None:
    folder = tmp_path / "orphan-index"
    folder.mkdir()
    _touch_png(folder, "1.png")
    _touch_png(folder, "2.png")
    _touch_png(folder, "3.png")
    _write_post_md(
        folder,
        "---\n" 'title: "제목"\n' "---\n" "\n" "너무 큰 인덱스 ${5}.\n",
    )

    with pytest.raises(ValueError, match="고아 마커"):
        load_post(folder)


# ---------------------------------------------------------------------------
# 8) ${missing.png} 파일 부재 → ValueError
# ---------------------------------------------------------------------------


def test_load_post_raises_on_missing_filename(tmp_path: Path) -> None:
    folder = tmp_path / "missing-file"
    folder.mkdir()
    _touch_png(folder, "1.png")
    _write_post_md(
        folder,
        "---\n" 'title: "제목"\n' "---\n" "\n" "없는 파일 ${missing.png}.\n",
    )

    with pytest.raises(ValueError, match="이미지 파일 없음"):
        load_post(folder)


# ---------------------------------------------------------------------------
# 9) 고아 이미지 → warning 발생, 정상 반환
# ---------------------------------------------------------------------------


def test_load_post_warns_on_orphan_image(
    tmp_path: Path, caplog: pytest.LogCaptureFixture
) -> None:
    folder = tmp_path / "orphan-image"
    folder.mkdir()
    _touch_png(folder, "1.png")
    _touch_png(folder, "unused.png")
    _write_post_md(
        folder,
        "---\n" 'title: "제목"\n' "---\n" "\n" "하나만 사용 ${1}.\n",
    )

    with caplog.at_level(logging.WARNING, logger="tistory_post.post_loader"):
        result = load_post(folder)

    assert result.skip is False
    assert set(result.images.keys()) == {"1.png"}
    assert any(
        "orphan images" in record.getMessage() and "unused.png" in record.getMessage()
        for record in caplog.records
    ), f"orphan warning 없음: {[r.getMessage() for r in caplog.records]}"


# ---------------------------------------------------------------------------
# 10) 동일 마커 중복 → images dict 1건, markers list 2건
# ---------------------------------------------------------------------------


def test_load_post_duplicate_marker_keeps_both_markers_single_image(
    tmp_path: Path,
) -> None:
    folder = tmp_path / "dup-marker"
    folder.mkdir()
    _touch_png(folder, "1.png")
    _write_post_md(
        folder,
        "---\n" 'title: "제목"\n' "---\n" "\n" "처음 ${1}\n" "\n" "다시 ${1} 를 재사용.\n",
    )

    result = load_post(folder)

    assert len(result.markers) == 2
    assert result.markers[0].raw_token == "${1}"
    assert result.markers[1].raw_token == "${1}"
    # 동일 파일 → dict 에 1건.
    assert set(result.images.keys()) == {"1.png"}


# ---------------------------------------------------------------------------
# 11) post.md 부재 → FileNotFoundError
# ---------------------------------------------------------------------------


def test_load_post_raises_when_post_md_missing(tmp_path: Path) -> None:
    folder = tmp_path / "no-post-md"
    folder.mkdir()
    _touch_png(folder, "1.png")

    with pytest.raises(FileNotFoundError, match="post.md"):
        load_post(folder)


# ---------------------------------------------------------------------------
# 12) 첫 줄이 '---' 아님 → ValueError
# ---------------------------------------------------------------------------


def test_load_post_raises_when_no_frontmatter_opening(tmp_path: Path) -> None:
    folder = tmp_path / "no-frontmatter"
    folder.mkdir()
    _write_post_md(folder, "title 없이 본문만\n")

    with pytest.raises(ValueError, match="---"):
        load_post(folder)


# ---------------------------------------------------------------------------
# 13) tags 가 list 아님 (문자열) → ValueError
# ---------------------------------------------------------------------------


def test_load_post_raises_when_tags_not_list(tmp_path: Path) -> None:
    folder = tmp_path / "tags-str"
    folder.mkdir()
    _write_post_md(
        folder,
        "---\n" 'title: "제목"\n' 'tags: "단일문자열"\n' "---\n" "\n" "본문\n",
    )

    with pytest.raises(ValueError, match="tags"):
        load_post(folder)


# ---------------------------------------------------------------------------
# 14) 이미지 없음 + 마커 없음 → 정상 (공통 엣지)
# ---------------------------------------------------------------------------


def test_load_post_no_images_no_markers(tmp_path: Path) -> None:
    folder = tmp_path / "plain"
    folder.mkdir()
    _write_post_md(
        folder,
        "---\n" 'title: "텍스트만"\n' "---\n" "\n" "본문만 있는 글.\n",
    )

    result = load_post(folder)

    assert result.skip is False
    assert result.markers == []
    assert result.images == {}
    assert result.tags == []
    assert result.category_name is None
