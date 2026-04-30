"""MaSignal allocator — 이동평균 시그널 기반 비중 결정.

architecture.md V3 § "사용자 의도 정합성" (L116-118) + task-board TASK-219 근거.

배경 (사용자 의도):
    MA 필터를 `signal_filters[]` 로 사용하면 `rebalance_schedule` 일자에만 평가되어
    "이평선 깨면 즉시 청산, 회복하면 즉시 매수" 의도와 어긋난다. MA 를 allocator 로
    분리하면 자산별 보유/청산 결정을 비중 산출 로직에 통합할 수 있다.

동작:
    - params.assets = asset_id → 비중 dict (FixedWeightParams.weights 와 같은 검증).
    - generate_weights 호출 시 universe ∩ params.assets 각 자산에 대해
      자산 단위 fallback (`filters/moving_average.py:52-54` 패턴) 적용:
        (i) prices_until_d[aid].dropna() 후 len ≥ window 인지 확인
        (ii) 부족 자산은 skip (cash 처리, 결과 dict 에서 제외)
        (iii) 충분 자산은 close[-1] > SMA(window) 면 params.assets[aid], 아니면 0
    - 마지막에 `normalize_weights(filtered, allow_cash_slot=True)`.
    - 전체 빈 dict 는 모든 자산이 데이터 부족이거나 MA 아래일 때만 반환 (cash-only).

clean architecture:
    - 도메인 순수 (pandas/pydantic 만 import — base.py 와 동일 정책).
    - SMA 계산은 인라인 (`filters/moving_average.py` 패턴 답습, 별도 utils 추출은 2~3회
      중복 시점에 검토).
"""

from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import ClassVar

import pandas as pd
from pydantic import BaseModel, Field, field_validator

from ._validation import validate_weight_dict
from .base import AllocatorBase, normalize_weights


class MaSignalParams(BaseModel):
    """MaSignal 파라미터.

    Validation (allocators/_validation.py:validate_weight_dict 위임):
        - window: 이동평균 윈도우 (거래일). 2~500.
        - assets: asset_id 별 비중 dict (FixedWeightParams.weights 와 같은 검증).
            - 빈 dict 금지 / 음수 비중 금지 / 합 1.0 ± 5% 안.
    """

    window: int = Field(120, ge=2, le=500, description="이동평균 윈도우 (거래일)")
    assets: dict[int, float] = Field(
        ...,
        description="asset_id 별 목표 비중 (0~1, 합 ≈ 1). MA 위면 적용, 아래면 0.",
    )

    @field_validator("assets")
    @classmethod
    def _validate_assets(cls, v: dict[int, float]) -> dict[int, float]:
        return validate_weight_dict(v, name="assets")


class MaSignal(AllocatorBase[MaSignalParams]):
    """MA 위 자산만 params.assets 비중 적용, 나머지는 0 (cash 처리).

    universe ∩ params.assets 에서 자산 단위 fallback. window 부족하면 skip,
    MA 아래면 0. normalize_weights 로 합 ≈ 1 로 재정규화.
    """

    name: ClassVar[str] = "ma_signal"
    params_schema: ClassVar[type[BaseModel]] = MaSignalParams

    def required_universe(self) -> list[int]:
        """params.assets 에 명시된 모든 asset_id 가 universe 에 포함되어야 의미가
        있다 (FixedWeight 와 동일 정책 — 빠지면 비중이 깎임).
        """
        return list(self.params.assets.keys())

    def generate_weights(
        self,
        universe_asset_ids: list[int],
        prices_until_d: pd.DataFrame,
        signal_date: date,
    ) -> dict[int, Decimal]:
        """universe ∩ params.assets 각 자산에 MA 필터 적용 후 normalize.

        Args:
            universe_asset_ids: 외부 필터 통과한 자산 목록.
            prices_until_d: index=date 오름차순, columns=asset_id, values=close.
                signal_date 까지 슬라이싱된 상태로 들어옴 (engine 책임).
            signal_date: 시그널 판정 일자 (D).

        Returns:
            asset_id → 비중 (Decimal). 빈 dict 면 cash-only.
        """
        universe_set = set(universe_asset_ids)
        window = self.params.window
        filtered: dict[int, Decimal] = {}

        for aid, target_weight in self.params.assets.items():
            if aid not in universe_set:
                continue
            if aid not in prices_until_d.columns:
                continue
            series = prices_until_d[aid].dropna()
            if len(series) < window:
                # 자산 단위 fallback — 데이터 부족 자산은 skip (cash 처리).
                continue
            recent = series.tail(window)
            ma = recent.mean()
            last_price = series.iloc[-1]
            if pd.isna(ma) or pd.isna(last_price):
                continue
            if last_price > ma:
                filtered[aid] = Decimal(str(target_weight))
            # MA 아래면 0 — filtered 에 추가하지 않음 (= cash 비중으로 흡수).

        return normalize_weights(filtered, allow_cash_slot=True)
