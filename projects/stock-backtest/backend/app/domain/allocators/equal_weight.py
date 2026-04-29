"""EqualWeight Allocator. universe 모든 자산에 1/N 비중.

Quant Lab CLAUDE.md L26 (MVP 프리셋 3번) + architecture.md V3 § "Phase 1 MVP" L754 근거.

가장 단순한 allocator — 파라미터 없음. universe 가 비어있으면 빈 dict.
"""

from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import ClassVar

import pandas as pd
from pydantic import BaseModel

from .base import AllocatorBase


class EqualWeightParams(BaseModel):
    """파라미터 없음. UI 가 빈 폼 ('no params') 으로 자동 표시."""


class EqualWeight(AllocatorBase[EqualWeightParams]):
    name: ClassVar[str] = "equal_weight"
    params_schema: ClassVar[type[BaseModel]] = EqualWeightParams

    def generate_weights(
        self,
        universe_asset_ids: list[int],
        prices_until_d: pd.DataFrame,
        signal_date: date,
    ) -> dict[int, Decimal]:
        """universe 모든 자산에 1/N. 빈 universe → 빈 dict.

        prices_until_d / signal_date 는 사용하지 않음 (EqualWeight 는 가격 무관).
        Allocator Protocol 시그니처 준수를 위해 인자는 받음.
        """
        if not universe_asset_ids:
            return {}
        per_asset = Decimal("1") / Decimal(len(universe_asset_ids))
        return {aid: per_asset for aid in universe_asset_ids}
