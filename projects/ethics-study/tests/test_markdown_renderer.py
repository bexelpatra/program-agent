"""Tests for web/markdown_renderer.py — byte-level verbatim preservation."""

from __future__ import annotations

import os
import sys

import pytest

sys.path.insert(
    0,
    os.path.join(os.path.dirname(__file__), "..", "web"),
)

from markdown_renderer import render, verify_verbatim  # noqa: E402


# Fixture md (architecture.md L412 verbatim 5종 + 부분 코드/표/리스트):
# - 한자 朱熹·知訥·頓悟漸修 (8 CJK)
# - em-dash `—` 3건
# - 원문자 ㉠㉡㉢㉣㉤㉥ 6건
# - 그리스 νοῦς (ν·ο·ς = 3 lower 그리스 + ῦ 는 0x1FE6 → range 외)
# - 독일어 Würde·Grundlegung·Maxime (Würde 의 ü 1건)
FIXTURE_MD = """# Verbatim 보존 테스트

朱熹 — 知訥 — 頓悟漸修 —

순서 ㉠ 첫째 ㉡ 둘째 ㉢ 셋째 ㉣ 넷째 ㉤ 다섯째 ㉥ 여섯째.

νοῦς — Würde · Grundlegung · Maxime.

| 사상가 | 핵심 |
|--------|------|
| 朱熹   | 性卽理 |

```python
print("hi")
```

- 항목 1
- 항목 2
"""


@pytest.fixture
def md_text() -> str:
    return FIXTURE_MD


# 1. render() 가 한자 byte 그대로 보존하는지
def test_render_preserves_cjk_bytes(md_text: str) -> None:
    html = render(md_text)
    assert "朱熹" in html
    assert "知訥" in html
    assert "頓悟漸修" in html
    # byte-level: UTF-8 인코딩이 그대로 살아있는지
    assert "朱熹".encode("utf-8") in html.encode("utf-8")


# 2. verify_verbatim() 5종 모두 ±0
def test_verify_verbatim_all_zero_diff(md_text: str) -> None:
    html = render(md_text)
    counts = verify_verbatim(md_text, html)
    for cls, (md_n, html_n) in counts.items():
        assert (
            md_n == html_n
        ), f"{cls}: md={md_n} vs html={html_n} mismatch (verbatim broken)"
    # 카운트 자체도 fixture 와 일치하는지 확인
    assert counts["em_dash"] == (4, 4)  # 본문 3건 + 그리스 줄 1건 = 4
    assert counts["cjk"][0] >= 8  # 朱熹·知訥·頓悟漸修 + 표 안의 朱熹·性卽理
    assert counts["circled_digits"] == (6, 6)
    assert counts["greek_lower"] == (3, 3)  # ν·ο·ς (ῦ 는 0x1FE6 range 외)
    assert counts["german"] == (1, 1)  # Würde 의 ü


# 3. 코드 블록·표·리스트가 깨지지 않음
def test_render_block_elements_intact(md_text: str) -> None:
    html = render(md_text)
    assert "<table>" in html
    assert "<thead>" in html
    assert "<ul>" in html
    assert "<li>" in html
    assert "<pre>" in html
    assert "<code" in html
    # 표 셀 안의 한자도 보존
    assert "性卽理" in html


# 4. 부정 케이스: typographer ON 이면 em-dash 카운트 불일치
def test_typographer_on_breaks_verbatim() -> None:
    """수동으로 typographer=True + replacements 활성화한 MarkdownIt 가
    `---` 를 em-dash 로 자동 변환해 md vs html 카운트 불일치를 일으키는지."""
    from markdown_it import MarkdownIt

    bad_md = MarkdownIt("commonmark", {"typographer": True}).enable(
        ["replacements", "smartquotes"]
    )
    md = "Hello --- world."  # ASCII triple hyphen, em-dash 0건
    html = bad_md.render(md)
    counts = verify_verbatim(md, html)
    md_n, html_n = counts["em_dash"]
    assert md_n == 0
    assert html_n == 1, (
        f"typographer=True 가 `---` 을 em-dash 로 변환했어야 함 " f"(md={md_n} vs html={html_n})"
    )


# 5. raw HTML inline (<script>) 가 escape 되어 텍스트 노드로만 잡히는지
def test_raw_html_is_escaped_for_security() -> None:
    md = "안전 테스트: <script>alert('x')</script> 끝."
    html = render(md)
    # raw <script> 태그가 그대로 살아있으면 XSS, 살아있으면 안 됨
    assert "<script>" not in html
    assert "&lt;script&gt;" in html or "&lt;script" in html
    # verbatim helper 의 _strip_tags 가 escape 된 텍스트는 그대로 살림
    counts = verify_verbatim(md, html)
    # 한자/em-dash 등은 fixture 외이므로 모두 0/0
    for cls, (md_n, html_n) in counts.items():
        assert md_n == html_n, f"{cls}: {md_n} vs {html_n}"
