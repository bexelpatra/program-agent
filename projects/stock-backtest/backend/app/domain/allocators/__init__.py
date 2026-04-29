"""Allocator 구현체 모음.

strategy.py 의 Allocator Protocol (TASK-043) 을 구현하는 모든 클래스의 패키지.

MVP 프리셋 (Quant Lab CLAUDE.md L26):
- FixedWeight (TASK-050): 사용자 지정 고정 비중
- AllWeather (TASK-051): 표준 5자산 카테고리 비중
- EqualWeight (TASK-052): 1/N
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
