"""AllWeather Allocator (Ray Dalio 영감).

Quant Lab CLAUDE.md L26 (MVP 프리셋 2번) + architecture.md V3 § "Phase 1 MVP" L754 근거.

표준 디폴트 비중 (사용자 조정 가능):
- 주식 (equity): 30%
- 장기채 (long_bond): 40%
- 중기채 (intermediate_bond): 15%
- 금 (gold): 7.5%
- 원자재 (commodity): 7.5%

universe 자산이 어느 카테고리에 속하는지는 사용자가 매핑 입력 (UI 폼).
universe 에 카테고리가 빠져 있으면 명시적 에러 (AllWeatherCategoryMissing) — 사용자가
의미 있는 AllWeather 포트폴리오를 구성하도록 유도.
"""

from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import ClassVar, Literal

import pandas as pd
from pydantic import BaseModel, Field, field_validator

from ._validation import validate_weight_dict
from .base import AllocatorBase, normalize_weights

Category = Literal["equity", "long_bond", "intermediate_bond", "gold", "commodity"]

DEFAULT_ALLWEATHER_WEIGHTS: dict[Category, float] = {
    "equity": 0.30,
    "long_bond": 0.40,
    "intermediate_bond": 0.15,
    "gold": 0.075,
    "commodity": 0.075,
}


class AllWeatherParams(BaseModel):
    """카테고리별 비중 + asset_id → 카테고리 매핑.

    Validation:
        - category_weights 합 ≈ 1.0 (±5% 허용 — 사용자 입력 편의)
        - 음수 비중 금지
        - asset_categories 는 비어있지 않아야 함 (1개 이상 자산 분류 필요)
    """

    category_weights: dict[Category, float] = Field(
        default_factory=lambda: dict(DEFAULT_ALLWEATHER_WEIGHTS),
        description=(
            "카테고리별 목표 비중 (디폴트: equity 30 / long_bond 40 / "
            "intermediate_bond 15 / gold 7.5 / commodity 7.5)"
        ),
    )
    asset_categories: dict[int, Category] = Field(
        ...,
        description="asset_id → 카테고리 매핑 (universe 의 모든 자산이 분류되어야 함)",
    )

    @field_validator("category_weights")
    @classmethod
    def _validate_weights(cls, v: dict[Category, float]) -> dict[Category, float]:
        # `Field(default_factory=...)` 가 빈 dict 진입을 막아주므로 allow_empty=True.
        # 비중 검증은 fixed_weight / ma_signal 과 동일 정책.
        return validate_weight_dict(v, name="category_weights", allow_empty=True)

    @field_validator("asset_categories")
    @classmethod
    def _validate_categories(cls, v: dict[int, Category]) -> dict[int, Category]:
        if not v:
            raise ValueError("asset_categories must not be empty")
        return v


class AllWeatherCategoryMissing(Exception):
    """universe 에 필수 카테고리 자산이 빠짐 (예: long_bond 없음)."""


class AllWeather(AllocatorBase[AllWeatherParams]):
    """카테고리 비중 → 카테고리 내부 1/N 분배.

    예: equity 30% 카테고리에 자산 2개가 매핑돼 있으면 각각 15%.
    """

    name: ClassVar[str] = "all_weather"
    params_schema: ClassVar[type[BaseModel]] = AllWeatherParams

    def required_universe(self) -> list[int]:
        """asset_categories 매핑된 자산 모두 universe 에 있어야 의미가 있음.

        engine 의 universe 검증이 이 리스트를 사용. (FixedWeight 와 동일 정책)
        """
        return list(self.params.asset_categories.keys())

    def generate_weights(
        self,
        universe_asset_ids: list[int],
        prices_until_d: pd.DataFrame,
        signal_date: date,
    ) -> dict[int, Decimal]:
        """카테고리 비중을 카테고리 내 universe 자산에 1/N 분배.

        prices_until_d / signal_date 는 사용하지 않음 (AllWeather 는 가격 무관).
        Allocator Protocol 시그니처 준수를 위해 인자는 받음.
        """
        universe_set = set(universe_asset_ids)
        by_category: dict[Category, list[int]] = {}
        for asset_id, category in self.params.asset_categories.items():
            if asset_id in universe_set:
                by_category.setdefault(category, []).append(asset_id)

        missing = [
            cat
            for cat, weight in self.params.category_weights.items()
            if weight > 0 and not by_category.get(cat)
        ]
        if missing:
            raise AllWeatherCategoryMissing(
                f"universe 에 다음 카테고리 자산이 없습니다: {', '.join(missing)}. "
                f"각 카테고리에 1개 이상의 자산이 필요합니다."
            )

        result: dict[int, Decimal] = {}
        for cat, weight in self.params.category_weights.items():
            assets = by_category.get(cat, [])
            if not assets or weight <= 0:
                continue
            per_asset = Decimal(str(weight)) / Decimal(len(assets))
            for aid in assets:
                result[aid] = per_asset

        return normalize_weights(result, allow_cash_slot=True)
