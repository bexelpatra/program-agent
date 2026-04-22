"""전략(Strategy) 패키지.

``base`` 모듈은 :class:`Strategy` 추상 베이스와 :class:`StrategyParams`
pydantic 베이스를 제공한다. ``registry`` 모듈은 전역 레지스트리와
자동 스캔 기능을 제공한다. ``static/``와 ``dynamic/`` 하위 패키지는
각각 정적/동적 자산배분 전략 구현을 담는다.
"""

from stock_backtest.strategies.base import Strategy, StrategyParams
from stock_backtest.strategies.registry import (
    STRATEGY_REGISTRY,
    discover_strategies,
    get_strategy,
    list_strategies,
    register,
)

__all__ = [
    "Strategy",
    "StrategyParams",
    "STRATEGY_REGISTRY",
    "discover_strategies",
    "get_strategy",
    "list_strategies",
    "register",
]
