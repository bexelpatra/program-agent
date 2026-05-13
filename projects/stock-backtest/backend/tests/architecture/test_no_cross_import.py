"""백테스트 도메인 ↔ 테마 도메인 격리 정적 검증.

TASK-309 — Phase 2 테마 추적 모듈은 백테스트 엔진과 양방향 import 금지.
services/** 도 테마 모듈을 직접 import 하면 안 된다.

각 invariant 는 위반 시 파일 경로 + 라인 번호 + 매칭 import 라인을 출력해
디버깅을 용이하게 한다.
"""

from __future__ import annotations

import pathlib
import re
from typing import Iterable

# tests/architecture/test_no_cross_import.py -> backend/
BACKEND_ROOT = pathlib.Path(__file__).resolve().parents[2]
APP_ROOT = BACKEND_ROOT / "app"


def _scan_imports(
    target_files: Iterable[pathlib.Path],
    banned_modules: Iterable[str],
) -> list[tuple[pathlib.Path, int, str, str]]:
    """주어진 파일들에서 banned 모듈 import 위반을 수집한다.

    반환: (path, line_no, matched_module, line) 리스트.
    """
    violations: list[tuple[pathlib.Path, int, str, str]] = []
    banned_list = list(banned_modules)
    for path in target_files:
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        for line_no, line in enumerate(text.splitlines(), start=1):
            for module in banned_list:
                escaped = re.escape(module)
                # "from app.foo import ..." 또는 "from app.foo.bar import ..."
                # "import app.foo" 또는 "import app.foo.bar"
                pattern = (
                    rf"^\s*from\s+{escaped}(\.|\s)|^\s*import\s+{escaped}(\.|\s|$)"
                )
                if re.search(pattern, line):
                    violations.append((path, line_no, module, line.strip()))
                    break  # 한 라인에서 첫 매칭만 기록
    return violations


def _format_violations(
    violations: list[tuple[pathlib.Path, int, str, str]],
) -> str:
    lines = []
    for path, line_no, module, content in violations:
        rel = path.relative_to(BACKEND_ROOT)
        lines.append(f"  {rel}:{line_no}  [banned={module}]  {content}")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# invariant ①: domain/themes 는 백테스트 도메인을 import 하지 않는다
# ---------------------------------------------------------------------------


def test_themes_does_not_import_backtest_domain() -> None:
    themes_root = APP_ROOT / "domain" / "themes"
    assert themes_root.is_dir(), f"expected themes package at {themes_root}"

    target_files = list(themes_root.rglob("*.py"))
    banned = [
        "app.domain.engine",
        "app.domain.strategy",
        "app.domain.allocators",
        "app.domain.filters",
        "app.domain.trade",
        "app.domain.portfolio",
    ]
    violations = _scan_imports(target_files, banned)
    assert not violations, (
        "domain/themes 는 백테스트 도메인을 import 하면 안 된다 (Phase 2 격리 위반):\n"
        + _format_violations(violations)
    )


# ---------------------------------------------------------------------------
# invariant ②: 백테스트 도메인은 themes 를 import 하지 않는다
# ---------------------------------------------------------------------------


def test_backtest_domain_does_not_import_themes() -> None:
    domain_root = APP_ROOT / "domain"

    backtest_files: list[pathlib.Path] = []
    for name in ("engine.py", "strategy.py", "trade.py", "portfolio.py"):
        backtest_files.append(domain_root / name)
    for sub in ("allocators", "filters"):
        sub_root = domain_root / sub
        if sub_root.is_dir():
            backtest_files.extend(sub_root.rglob("*.py"))

    banned = ["app.domain.themes"]
    violations = _scan_imports(backtest_files, banned)
    assert not violations, (
        "백테스트 도메인 (engine/strategy/allocators/filters/trade/portfolio) 은 "
        "domain/themes 를 import 하면 안 된다 (Phase 2 격리 위반):\n"
        + _format_violations(violations)
    )


# ---------------------------------------------------------------------------
# invariant ③: services/** 는 themes / theme_repository 를 import 하지 않는다
# ---------------------------------------------------------------------------


def test_services_does_not_import_themes_or_theme_repository() -> None:
    services_root = APP_ROOT / "services"
    assert services_root.is_dir(), f"expected services package at {services_root}"

    target_files = list(services_root.rglob("*.py"))
    banned = [
        "app.domain.themes",
        "app.data.theme_repository",
    ]
    violations = _scan_imports(target_files, banned)
    assert not violations, (
        "services/** 는 테마 도메인 / theme_repository 를 직접 import 하면 안 된다 "
        "(백테스트 ↔ 테마 격리 위반):\n" + _format_violations(violations)
    )
