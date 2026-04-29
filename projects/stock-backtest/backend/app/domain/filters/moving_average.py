"""MovingAverage 필터.

자산별 가격 > MA(window) → PASS (보유 자격 있음).
약세장 회피용으로 price_above=False (가격 < MA) 도 지원.

architecture.md V3 § "Phase 1 MVP" L728 + Quant Lab CLAUDE.md L26.
"""

from __future__ import annotations

from datetime import date
from typing import ClassVar

import pandas as pd
from pydantic import BaseModel, Field

from .base import SignalFilterBase


class MovingAverageParams(BaseModel):
    """MovingAverage 파라미터.

    - window: 이동평균 윈도우 (거래일). 2~2000.
    - price_above: True 면 가격 > MA 일 때 PASS, False 면 가격 < MA 일 때 PASS.
    """

    window: int = Field(..., ge=2, le=2000, description="이동평균 윈도우 (일)")
    price_above: bool = Field(
        True,
        description="True 면 가격 > MA, False 면 가격 < MA 일 때 PASS",
    )


class MovingAverage(SignalFilterBase[MovingAverageParams]):
    """signal_date 기준 직전 close 가 MA(window) 위/아래에 있으면 보유 자격.

    데이터 부족 (window 만큼의 과거 가격이 없음) 시 False 반환 (보수적 — 잘못된
    PASS 방지). 자산이 prices_until_d.columns 에 없어도 False.
    """

    name: ClassVar[str] = "moving_average"
    params_schema: ClassVar[type[BaseModel]] = MovingAverageParams

    def is_eligible(
        self,
        asset_id: int,
        prices_until_d: pd.DataFrame,
        signal_date: date,
    ) -> bool:
        if asset_id not in prices_until_d.columns:
            return False
        series = prices_until_d[asset_id].dropna()
        if len(series) < self.params.window:
            return False
        # 최근 window 일 평균 (signal_date 일 종가까지 포함 — 모델 A 의 D 종가 시그널).
        recent = series.tail(self.params.window)
        ma = recent.mean()
        last_price = series.iloc[-1]
        if pd.isna(ma) or pd.isna(last_price):
            return False
        if self.params.price_above:
            return bool(last_price > ma)
        return bool(last_price < ma)
