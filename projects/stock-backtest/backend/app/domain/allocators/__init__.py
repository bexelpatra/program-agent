"""Allocator 구현체 모음.

strategy.py 의 Allocator Protocol (TASK-043) 을 구현하는 모든 클래스의 패키지.

MVP 프리셋 (Quant Lab CLAUDE.md L26):
- FixedWeight (TASK-050): 사용자 지정 고정 비중
- AllWeather (TASK-051): 표준 5자산 카테고리 비중
- EqualWeight (TASK-052): 1/N

사용자 명시 추가 (TASK-219):
- MaSignal: MA 위 자산만 비중 적용 (allocator 단위 시그널)
"""

from .all_weather import (
    DEFAULT_ALLWEATHER_WEIGHTS,
    AllWeather,
    AllWeatherCategoryMissing,
    AllWeatherParams,
)
from .base import AllocatorBase, normalize_weights
from .equal_weight import EqualWeight, EqualWeightParams
from .fixed_weight import FixedWeight, FixedWeightParams
from .ma_signal import MaSignal, MaSignalParams

__all__ = [
    "AllocatorBase",
    "normalize_weights",
    "FixedWeight",
    "FixedWeightParams",
]
__all__ += [
    "AllWeather",
    "AllWeatherParams",
    "AllWeatherCategoryMissing",
    "DEFAULT_ALLWEATHER_WEIGHTS",
    "EqualWeight",
    "EqualWeightParams",
]
__all__ += ["MaSignal", "MaSignalParams"]
