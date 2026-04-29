"""서비스 레이어 — API 와 도메인 사이 use case 조립.

API 라우터는 얇게 (HTTP 경계만), 도메인은 순수 (외부 의존 없음). 이 둘 사이에서
"여러 도메인 객체 + DB 트랜잭션 + 백그라운드 실행" 을 조립하는 책임이 본 패키지.
"""

from app.services.backtest_runner import (
    build_strategy_from_config,
    execute_backtest_job,
)

__all__ = [
    "build_strategy_from_config",
    "execute_backtest_job",
]
