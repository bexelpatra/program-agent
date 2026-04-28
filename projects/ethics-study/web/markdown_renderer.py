"""Markdown rendering with byte-level verbatim preservation.

Track B (26-year ethics-study study-guide·coverage) requires byte-level
preservation of em-dash (U+2014), CJK, circled digits (U+3220~U+3225),
Greek and German diacritics across markdown -> HTML conversion.

This module provides two functions:
- ``render(md_text)`` : markdown text -> HTML body (typographer OFF, raw HTML escaped).
- ``verify_verbatim(md_text, html_body)`` : 5-class character count comparison.
"""

from __future__ import annotations

import re

from markdown_it import MarkdownIt


# typographer=False + replacements/smartquotes/linkify disabled.
# Track B byte-level verbatim 규약 (architecture.md L412): `---` 가 em-dash 로
# 자동 치환되거나 ASCII quote 가 typographic quote 로 바뀌면 hexdump 검증이 깨진다.
_MD = (
    MarkdownIt("commonmark", {"typographer": False, "html": False, "linkify": False})
    .enable("table")
    .disable(["replacements", "smartquotes", "linkify"])
)


def render(md_text: str) -> str:
    """Render markdown text to an HTML body string.

    Typographic substitution is OFF: `---` stays as three ASCII hyphens,
    ASCII quotes stay as ASCII, etc.  Raw HTML inline is OFF (escaped) for
    security: ``<script>`` ends up as text, not a live tag.
    """
    return _MD.render(md_text)


# study-guide 의 문항 헤더 정규식 (app.py _TOC_PATTERN 과 동일).
_QUESTION_HEADING_RE = re.compile(
    r"^## 문항(?:\s+(?:서술형|논술형|기입형))?\s+\d+",
    re.MULTILINE,
)
_H2_TAG_RE = re.compile(r"<h2>(.*?)</h2>", re.DOTALL)


def render_with_toc(md_text: str) -> tuple[str, list[dict]]:
    """Render md to HTML and build a TOC of question headings with anchors.

    Returns ``(html, toc)`` where ``toc`` is a list of dicts
    ``{"text": str, "id": str}`` in source order. Each matching ``<h2>`` in
    the output HTML gets ``id="q-N"`` injected so that ``href="#q-N"`` from
    the TOC scrolls the page to that question.

    Only ``## 문항`` headings (variants 서술형/논술형/기입형) are listed; other
    H2 headings (예: ``## 시험 정보``) keep no id. Source order in the markdown
    must match render order in the HTML — markdown-it preserves this.
    """
    # Extract question heading source lines in order, stripping the leading "## ".
    question_texts: list[str] = []
    for line in md_text.split("\n"):
        if _QUESTION_HEADING_RE.match(line):
            question_texts.append(line[3:].rstrip())

    html = _MD.render(md_text)

    counter = {"n": 0}

    def _inject_id(match: re.Match) -> str:
        inner = match.group(1)
        # markdown-it inline tokens may render `<strong>...</strong>` etc.;
        # strip tags to test whether this H2 is a question heading.
        stripped = _RE_TAG.sub("", inner).strip()
        if stripped.startswith("문항"):
            counter["n"] += 1
            return f'<h2 id="q-{counter["n"]}">{inner}</h2>'
        return match.group(0)

    html_with_anchors = _H2_TAG_RE.sub(_inject_id, html)

    toc = [
        {"text": text, "id": f"q-{i + 1}"}
        for i, text in enumerate(question_texts)
    ]
    return html_with_anchors, toc


# 5-class verbatim ranges (architecture.md L417-L422).
_RE_TAG = re.compile(r"<[^>]+>")
_RE_EM_DASH = re.compile("\u2014")
_RE_CJK = re.compile(r"[\u4E00-\u9FFF]")
# architecture.md L420 lists "㉠㉡㉢㉣㉤㉥ (U+3220~U+3225)".  실제 study-guide
# 파일의 visible 문자 ㉠㉡㉢㉣㉤㉥ 는 U+3260~U+3265 (CIRCLED HANGUL) 이므로
# 두 range 모두 포함해 spec 의 의도 (이 6 문자) 를 충족한다.
_RE_CIRCLED = re.compile(r"[\u3220-\u3225\u3260-\u3265]")
_RE_GREEK_LOWER = re.compile(r"[\u03B1-\u03C9]")
_RE_GERMAN = re.compile(r"[äöüÄÖÜß]")


def _strip_tags(html_body: str) -> str:
    """Return only the text-node content of an HTML body string."""
    # Regex strip is sufficient because ``render()`` escapes raw HTML, so
    # angle brackets in user text become &lt;/&gt; before this point.
    return _RE_TAG.sub("", html_body)


def _count_em_dash(text: str) -> int:
    return len(_RE_EM_DASH.findall(text))


def _count_cjk(text: str) -> int:
    return len(_RE_CJK.findall(text))


def _count_circled(text: str) -> int:
    return len(_RE_CIRCLED.findall(text))


def _count_greek_lower(text: str) -> int:
    return len(_RE_GREEK_LOWER.findall(text))


def _count_german(text: str) -> int:
    return len(_RE_GERMAN.findall(text))


def verify_verbatim(md_text: str, html_body: str) -> dict[str, tuple[int, int]]:
    """Count 5 verbatim classes in md_text vs HTML body text nodes.

    Returns a dict mapping class name -> (md_count, html_count).  Caller
    asserts equality per class.  HTML body is stripped to text nodes first
    so that tag attributes don't pollute counts.
    """
    html_text = _strip_tags(html_body)
    return {
        "em_dash": (_count_em_dash(md_text), _count_em_dash(html_text)),
        "cjk": (_count_cjk(md_text), _count_cjk(html_text)),
        "circled_digits": (_count_circled(md_text), _count_circled(html_text)),
        "greek_lower": (_count_greek_lower(md_text), _count_greek_lower(html_text)),
        "german": (_count_german(md_text), _count_german(html_text)),
    }
