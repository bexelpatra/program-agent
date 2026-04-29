"""의존성 스모크 체크.

requirements.txt 의 top-level 패키지를 한 번에 import 해 ABI/버전 충돌이 없는지
확인한다. 새 의존성을 추가하면 여기에도 반영한다.
"""

from __future__ import annotations

import importlib
import sys


PACKAGES: list[str] = [
    "fastapi",
    "uvicorn",
    "pydantic",
    "pydantic_settings",
    "sqlalchemy",
    "alembic",
    "psycopg2",
    "pandas",
    "numpy",
    "yfinance",
    "pykrx",
    "exchange_calendars",
    "apscheduler",
    "httpx",
    "dotenv",
    "pytest",
    "pytest_asyncio",
]


def main() -> int:
    failures: list[tuple[str, str]] = []
    for name in PACKAGES:
        try:
            importlib.import_module(name)
            print(f"OK   {name}")
        except Exception as exc:  # noqa: BLE001 — boundary, want all failures
            print(f"FAIL {name}: {exc}")
            failures.append((name, str(exc)))

    if failures:
        print(f"\n{len(failures)} package(s) failed to import.")
        return 1

    print(f"\nAll {len(PACKAGES)} packages imported successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
