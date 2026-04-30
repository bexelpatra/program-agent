"""FixedWeight allocator. asset_id → 고정 비중 dict 를 그대로 적용.

Quant Lab CLAUDE.md L26 (MVP 프리셋 1번) + architecture.md V3 § "Phase 1 MVP" L754 근거.

특징:
- 사용자가 UI 폼에서 자산별 비중을 직접 입력 (예: SPY 60%, AGG 40%).
- universe 와 교집합 → universe 에 없는 asset 은 자동 제외.
- 교집합 후 합이 1 에서 벗어나면 normalize_weights 로 재정규화.
"""

from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import ClassVar

import pandas as pd
from pydantic import BaseModel, Field, field_validator

from ._validation import validate_weight_dict
from .base import AllocatorBase, normalize_weights


class FixedWeightParams(BaseModel):
    """사용자가 UI 폼에서 입력. asset_id 별 비중 dict.

    Validation (allocators/_validation.py:validate_weight_dict 위임):
        - 빈 dict 금지
        - 음수 비중 금지
        - 합이 1.0 ± 5% 안 (사용자 입력 편의: 60/40 같은 정수 입력 허용,
          미세 오차는 normalize_weights 가 흡수)
    """

    weights: dict[int, float] = Field(
        ...,
        description="asset_id 별 목표 비중 (0~1, 합 ≈ 1)",
    )

    @field_validator("weights")
    @classmethod
    def _validate_weights(cls, v: dict[int, float]) -> dict[int, float]:
        return validate_weight_dict(v, name="weights")


class FixedWeight(AllocatorBase[FixedWeightParams]):
    """params.weights 를 그대로 목표 비중으로 사용 (universe 와 교집합)."""

    name: ClassVar[str] = "fixed_weight"
    params_schema: ClassVar[type[BaseModel]] = FixedWeightParams

    def required_universe(self) -> list[int]:
        """FixedWeight 는 params 에 명시된 asset_id 모두를 universe 가 포함해야
        의미가 있다 (없으면 비중이 깎이거나 0 이 됨). 호출자(engine) 가
        universe 검증 시 이 리스트를 사용.
        """
        return list(self.params.weights.keys())

    def generate_weights(
        self,
        universe_asset_ids: list[int],
        prices_until_d: pd.DataFrame,
        signal_date: date,
    ) -> dict[int, Decimal]:
        """params.weights ∩ universe → 정규화된 비중 dict.

        prices_until_d / signal_date 는 사용하지 않음 (FixedWeight 는 가격
        무관). 다만 Allocator Protocol 시그니처를 준수해야 하므로 인자는 받음.
        """
        universe_set = set(universe_asset_ids)
        filtered = {
            aid: Decimal(str(w))
            for aid, w in self.params.weights.items()
            if aid in universe_set
        }
        return normalize_weights(filtered, allow_cash_slot=True)
