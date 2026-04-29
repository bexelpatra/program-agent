"""Momentum 필터.

자산별 lookback 기간 수익률이 임계값 이상이면 PASS.
디폴트: lookback=126일 (~6개월), threshold=0.0 (양수 수익률).

architecture.md V3 § "Phase 1 MVP" L728 + Quant Lab CLAUDE.md L26 (Momentum filter).
"""

from __future__ import annotations

from datetime import date
from typing import ClassVar

import pandas as pd
from pydantic import BaseModel, Field

from .base import SignalFilterBase


class MomentumParams(BaseModel):
    """Momentum 파라미터.

    - lookback: 수익률 측정 기간 (거래일). 디폴트 126 (~6개월).
    - threshold: 통과 기준 수익률 (디폴트 0.0 = 양수 수익률 PASS).
        음수 허용 — "−50% 보다 덜 빠진 자산 PASS" 같은 시나리오.
    """

    lookback: int = Field(
        126, ge=2, le=2000, description="수익률 측정 기간 (일). 디폴트 ~6개월"
    )
    threshold: float = Field(
        0.0, ge=-1.0, le=10.0, description="통과 기준 수익률 (디폴트 0.0 = 양수)"
    )


class Momentum(SignalFilterBase[MomentumParams]):
    """자산별 (price[D] / price[D-lookback]) - 1 > threshold 면 PASS.

    데이터 부족 (lookback+1 개의 과거 가격이 없음) 시 False 반환 (보수적 — 잘못된
    PASS 방지). 자산이 prices_until_d.columns 에 없거나 시작 가격이 0 이하면 False.
    """

    name: ClassVar[str] = "momentum"
    params_schema: ClassVar[type[BaseModel]] = MomentumParams

    def is_eligible(
        self,
        asset_id: int,
        prices_until_d: pd.DataFrame,
        signal_date: date,
    ) -> bool:
        if asset_id not in prices_until_d.columns:
            return False
        series = prices_until_d[asset_id].dropna()
        if len(series) < self.params.lookback + 1:
            return False
        # 최근 lookback+1 일 — 시점 가격 + lookback 전 가격으로 수익률 계산.
        recent = series.tail(self.params.lookback + 1)
        start_price = recent.iloc[0]
        last_price = recent.iloc[-1]
        if pd.isna(start_price) or pd.isna(last_price) or start_price <= 0:
            return False
        ret = (last_price / start_price) - 1.0
        return bool(ret > self.params.threshold)
