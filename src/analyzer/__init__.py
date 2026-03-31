"""
분석 프레임워크 — StrategyRegistry 및 기본 전략 자동 등록.
"""

from src.analyzer.base import BaseStrategy


class StrategyRegistry:
    """전략을 이름으로 등록/조회. 새 전략 파일 추가 시 여기에 등록."""

    _strategies: dict[str, BaseStrategy] = {}

    @classmethod
    def register(cls, strategy: BaseStrategy):
        """전략 인스턴스를 등록한다."""
        cls._strategies[strategy.name] = strategy

    @classmethod
    def get(cls, name: str) -> BaseStrategy:
        """이름으로 전략을 조회한다. 없으면 KeyError."""
        if name not in cls._strategies:
            raise KeyError(f"등록되지 않은 전략: '{name}'. 등록된 전략: {cls.list_all()}")
        return cls._strategies[name]

    @classmethod
    def list_all(cls) -> list[str]:
        """등록된 전략 이름 목록을 반환한다."""
        return list(cls._strategies.keys())


# =============================================================================
# 기본 전략 자동 등록
# =============================================================================

from src.analyzer.seasonality import SeasonalityStrategy
from src.analyzer.moving_average import MovingAverageStrategy
from src.analyzer.correlation import CorrelationStrategy

StrategyRegistry.register(SeasonalityStrategy())
StrategyRegistry.register(MovingAverageStrategy())
StrategyRegistry.register(CorrelationStrategy())
