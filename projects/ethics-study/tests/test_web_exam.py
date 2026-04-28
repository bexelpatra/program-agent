"""TASK-210-T — Phase A integration + regression tests for /exam routes.

Covers 11 spec items:
1. GET /exam 200 + 26 href links (`/exam/2014-A` ~ `/exam/2026-B`).
2. GET /exam/{2026-A,2014-A,2025-B} 200.
3. GET /exam/{9999-A,2014-Z,abcd-A} 404.
4. byte-level verbatim — 3 years × (study-guide+coverage) × 5 classes = 30 ±0.
5. hexdump bytes — em-dash (e2 80 94) · 朱 (e6 9c b1) · ㉠ (e3 89 a0) in /exam/2026-A.
6. regression — 6 existing routes 200 + invariants (lang=ko, title pattern).
7. tab-btn/tab-count baseline counts (`/`=4/0, `/search?q=kant`=2/2).
8. ES blocked — /exam/2026-A still 200 (markdown_renderer only, no ES dep).
9. CSS prefix isolation — `.exam-*` count=37, `.tab-(btn|count)` count=5.
10. TOC regex — 26 study-guide files sum = 293 hits.
11. TASK-208 regression — test_markdown_renderer 5/5 PASS (verified separately).
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

import pytest

# Make web/ importable so `from app import app` resolves.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
WEB_DIR = PROJECT_ROOT / "web"
sys.path.insert(0, str(WEB_DIR))

from bs4 import BeautifulSoup  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

import app as app_module  # noqa: E402
from app import app  # noqa: E402
from markdown_renderer import verify_verbatim  # noqa: E402


# ───────────────────────────────────────────────────────────────────────────
# Fixtures
# ───────────────────────────────────────────────────────────────────────────

EXAM_ROOT = PROJECT_ROOT / "exam-solutions"
SG_DIR = EXAM_ROOT / "study-guide"
CV_DIR = EXAM_ROOT / "coverage"
STYLE_CSS = WEB_DIR / "static" / "style.css"

YEARS_3 = ["2014-A", "2025-B", "2026-A"]


@pytest.fixture(scope="module")
def client() -> TestClient:
    return TestClient(app)


# ───────────────────────────────────────────────────────────────────────────
# 1. GET /exam 200 + 26 link
# ───────────────────────────────────────────────────────────────────────────


def test_exam_index_200_and_26_links(client: TestClient) -> None:
    r = client.get("/exam")
    assert r.status_code == 200, f"status={r.status_code}"
    body = r.text
    # 26 unique hrefs `/exam/{YYYY}-{A|B}` for years 2014~2026.
    hrefs = re.findall(r'href="/exam/(\d{4}-[AB])"', body)
    unique = set(hrefs)
    assert (
        len(unique) == 26
    ), f"expected 26 unique exam hrefs, got {len(unique)}: {sorted(unique)}"
    # spec: 13 years x 2 slots = 26
    expected = {f"{y}-{s}" for y in range(2014, 2027) for s in ("A", "B")}
    assert unique == expected, f"missing={expected - unique} extra={unique - expected}"


# ───────────────────────────────────────────────────────────────────────────
# 2. GET /exam/{2026-A, 2014-A, 2025-B} 200
# ───────────────────────────────────────────────────────────────────────────


@pytest.mark.parametrize("key", YEARS_3)
def test_exam_detail_200(client: TestClient, key: str) -> None:
    r = client.get(f"/exam/{key}")
    assert r.status_code == 200, f"/exam/{key} status={r.status_code}"


# ───────────────────────────────────────────────────────────────────────────
# 3. GET 404 for non-existent / malformed keys
# ───────────────────────────────────────────────────────────────────────────


@pytest.mark.parametrize("key", ["9999-A", "2014-Z", "abcd-A"])
def test_exam_detail_404(client: TestClient, key: str) -> None:
    r = client.get(f"/exam/{key}")
    assert r.status_code == 404, f"/exam/{key} expected 404 got {r.status_code}"


# ───────────────────────────────────────────────────────────────────────────
# 4. byte-level verbatim — 3 years × 2 docs × 5 classes = 30 ±0
# ───────────────────────────────────────────────────────────────────────────


def _extract_articles(body: str) -> tuple[str, str]:
    """Return (study-guide article HTML, coverage article HTML) from /exam/{key}."""
    soup = BeautifulSoup(body, "html.parser")
    sg = soup.select_one('article.exam-tab-content[data-tab="study-guide"]')
    cv = soup.select_one('article.exam-tab-content[data-tab="coverage"]')
    assert sg is not None, "study-guide article not found"
    assert cv is not None, "coverage article not found"
    return str(sg), str(cv)


@pytest.mark.parametrize("key", YEARS_3)
def test_verbatim_zero_diff_per_year(client: TestClient, key: str) -> None:
    """5-class verbatim count: HTML article body == md source (±0) for both docs."""
    r = client.get(f"/exam/{key}")
    assert r.status_code == 200
    sg_html, cv_html = _extract_articles(r.text)
    sg_md = (SG_DIR / f"{key}.md").read_text(encoding="utf-8")
    cv_md = (CV_DIR / f"{key}.md").read_text(encoding="utf-8")

    sg_counts = verify_verbatim(sg_md, sg_html)
    cv_counts = verify_verbatim(cv_md, cv_html)

    for cls, (m, h) in sg_counts.items():
        assert m == h, f"{key} study-guide {cls}: md={m} html={h}"
    for cls, (m, h) in cv_counts.items():
        assert m == h, f"{key} coverage {cls}: md={m} html={h}"


# ───────────────────────────────────────────────────────────────────────────
# 5. hexdump byte sequences in /exam/2026-A response body
# ───────────────────────────────────────────────────────────────────────────


def test_hexdump_em_dash_present(client: TestClient) -> None:
    r = client.get("/exam/2026-A")
    assert r.status_code == 200
    # em-dash (U+2014) in UTF-8 is e2 80 94
    assert b"\xe2\x80\x94" in r.content
    assert r.content.count(b"\xe2\x80\x94") >= 1


def test_hexdump_cjk_zhu_present(client: TestClient) -> None:
    """朱 (U+6731) UTF-8 = e6 9c b1 — appears in 2026-A coverage (朱熹)."""
    r = client.get("/exam/2026-A")
    assert r.status_code == 200
    assert b"\xe6\x9c\xb1" in r.content


def test_hexdump_circled_present(client: TestClient) -> None:
    """㉠ (U+3260) UTF-8 = e3 89 a0 — appears in study-guide / coverage."""
    r = client.get("/exam/2026-A")
    assert r.status_code == 200
    assert b"\xe3\x89\xa0" in r.content


# ───────────────────────────────────────────────────────────────────────────
# 6. Regression — 6 existing routes 200 + invariants
# ───────────────────────────────────────────────────────────────────────────


REGRESSION_ROUTES = [
    "/",
    "/thinker/kant",
    "/thinker/aristotle",
    "/search?q=kant",
    "/api/thinkers",
    "/api/thinker/kant",
    "/api/search?q=kant",
]


@pytest.mark.parametrize("path", REGRESSION_ROUTES)
def test_regression_route_200(client: TestClient, path: str) -> None:
    r = client.get(path)
    assert r.status_code == 200, f"{path} status={r.status_code}"


@pytest.mark.parametrize(
    "path", ["/", "/thinker/kant", "/thinker/aristotle", "/search?q=kant"]
)
def test_regression_html_invariants(client: TestClient, path: str) -> None:
    """HTML pages have lang=ko, valid <title> containing '윤리 학습 가이드' (or default)."""
    r = client.get(path)
    assert r.status_code == 200
    soup = BeautifulSoup(r.text, "html.parser")
    html_tag = soup.find("html")
    assert (
        html_tag is not None and html_tag.get("lang") == "ko"
    ), f"{path} lang missing/wrong"
    assert soup.title is not None, f"{path} <title> missing"
    title = (soup.title.string or "").strip()
    # default title = '윤리 임용시험 학습 가이드'; pages override with custom strings
    # but all should contain '윤리' and '가이드'.
    assert "윤리" in title and "가이드" in title, f"{path} title={title!r}"


def test_api_thinkers_total_baseline(client: TestClient) -> None:
    """/api/thinkers total >= 60 (baseline 67 in current ES). Sanity check."""
    r = client.get("/api/thinkers")
    assert r.status_code == 200
    payload = r.json()
    assert "total" in payload
    assert payload["total"] >= 60, f"thinker total dropped: {payload['total']}"


# ───────────────────────────────────────────────────────────────────────────
# 7. 분야별 탭 회귀 — tab-btn / tab-count baseline
# ───────────────────────────────────────────────────────────────────────────


def test_index_tab_btn_baseline(client: TestClient) -> None:
    """index.html: 4 .tab-btn buttons (분야별 탭), 0 .tab-count (미사용)."""
    r = client.get("/")
    soup = BeautifulSoup(r.text, "html.parser")
    btns = soup.select("button.tab-btn")
    cnts = soup.select(".tab-count")
    assert len(btns) == 4, f"index.html tab-btn buttons: {len(btns)} (baseline 4)"
    assert len(cnts) == 0, f"index.html tab-count: {len(cnts)} (baseline 0)"


def test_search_tab_btn_baseline(client: TestClient) -> None:
    """search.html ?q=kant: 2 .tab-btn buttons, 2 .tab-count badges."""
    r = client.get("/search?q=kant")
    soup = BeautifulSoup(r.text, "html.parser")
    btns = soup.select("button.tab-btn")
    cnts = soup.select(".tab-count")
    assert len(btns) == 2, f"search tab-btn buttons: {len(btns)} (baseline 2)"
    assert len(cnts) == 2, f"search tab-count: {len(cnts)} (baseline 2)"


# ───────────────────────────────────────────────────────────────────────────
# 8. ES 차단 시 /exam/2026-A 200 (route ES 의존 0건)
# ───────────────────────────────────────────────────────────────────────────


class _BrokenES:
    """ES mock that raises on any method call."""

    def __getattr__(self, name):  # noqa: ANN001
        def _raise(*a, **kw):  # noqa: ANN002,ANN003
            raise ConnectionError(f"ES is down (mock); called .{name}")

        return _raise


def test_exam_route_works_when_es_blocked(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(app_module, "es", _BrokenES())
    local = TestClient(app)
    r = local.get("/exam/2026-A")
    assert r.status_code == 200, f"/exam/2026-A under broken ES: {r.status_code}"
    r2 = local.get("/exam")
    assert r2.status_code == 200, f"/exam under broken ES: {r2.status_code}"


# ───────────────────────────────────────────────────────────────────────────
# 9. CSS prefix isolation — file-level grep
# ───────────────────────────────────────────────────────────────────────────


def test_css_exam_prefix_count_baseline() -> None:
    """style.css has 64 `^.exam-` selectors (baseline post Phase A5 가독성·TOC anchor)."""
    text = STYLE_CSS.read_text(encoding="utf-8")
    matches = re.findall(r"^\.exam-", text, flags=re.MULTILINE)
    assert len(matches) == 64, f"`^.exam-` count: {len(matches)} (baseline 64)"


def test_css_tab_btn_baseline_count_5() -> None:
    """style.css has exactly 5 `^.tab-(btn|count)` selectors (baseline unchanged)."""
    text = STYLE_CSS.read_text(encoding="utf-8")
    matches = re.findall(r"^\.tab-(?:btn|count)", text, flags=re.MULTILINE)
    assert len(matches) == 5, f"`^.tab-(btn|count)` count: {len(matches)} (baseline 5)"


def test_css_existing_first_1000_lines_unchanged() -> None:
    """All `^.exam-` selectors live AFTER line 1000 (existing 1000L untouched)."""
    text = STYLE_CSS.read_text(encoding="utf-8")
    lines = text.splitlines()
    exam_line_nos = [i + 1 for i, ln in enumerate(lines) if ln.startswith(".exam-")]
    assert exam_line_nos, ".exam- selectors not found"
    assert (
        min(exam_line_nos) > 1000
    ), f"`.exam-` selector found in pre-existing region (line {min(exam_line_nos)} ≤ 1000)"


# ───────────────────────────────────────────────────────────────────────────
# 10. TOC regex — 26 study-guide files sum hits = 293
# ───────────────────────────────────────────────────────────────────────────


def test_toc_regex_total_293() -> None:
    pat = re.compile(r"^## 문항(?:\s+(?:서술형|논술형|기입형))?\s+\d+", re.MULTILINE)
    files = sorted(SG_DIR.glob("*.md"))
    assert len(files) == 26, f"study-guide file count: {len(files)} (expected 26)"
    total = sum(len(pat.findall(p.read_text(encoding="utf-8"))) for p in files)
    assert (
        total == 293
    ), f"TOC total hits: {total} (expected 293 per exam-coverage-map.md L8)"


# ───────────────────────────────────────────────────────────────────────────
# 11. TASK-208 regression — re-run test_markdown_renderer subprocess
# ───────────────────────────────────────────────────────────────────────────


def test_task_208_markdown_renderer_regression() -> None:
    """Re-confirm test_markdown_renderer.py 5/5 PASS via subprocess (isolated)."""
    env = os.environ.copy()
    env["PYTEST_DISABLE_PLUGIN_AUTOLOAD"] = "1"
    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "tests/test_markdown_renderer.py",
            "-q",
            "--tb=short",
        ],
        cwd=str(PROJECT_ROOT),
        env=env,
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert proc.returncode == 0, (
        f"test_markdown_renderer regression FAILED:\n"
        f"stdout={proc.stdout}\nstderr={proc.stderr}"
    )
    # "5 passed" expected in output
    assert "5 passed" in proc.stdout, f"stdout did not show '5 passed': {proc.stdout}"
