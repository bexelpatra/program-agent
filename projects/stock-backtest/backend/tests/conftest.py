"""테스트 공통 fixture (TASK-080 + TASK-082).

backend/tests/ 의 모든 하위 디렉토리(golden/ + api/)가 공유하는 fixture 만 모은다.
- 환경변수 (DATABASE_URL) 가 누락되어 있어도 import 단계에서 ImportError 가 나지 않도록
  최소 fallback 을 주입한다 — pydantic-settings 가 require 하는 필드를 채우는 용도.
- DB 가 없는 환경 (BLOCKER-001 잔재) 에서도 골든 테스트는 도메인 단(엔진)만 호출하므로
  DB 의존이 없다. API 테스트는 DB 가 살아있을 때만 의미 있는 항목을 SOFT 로 다룬다.
"""

from __future__ import annotations

import os

# Settings 가 lru_cache 되기 전에 fallback 주입 (CI 환경 안전).
os.environ.setdefault(
    "DATABASE_URL",
    "postgresql+psycopg2://stock:stock@localhost:5432/stock_backtest",
)
