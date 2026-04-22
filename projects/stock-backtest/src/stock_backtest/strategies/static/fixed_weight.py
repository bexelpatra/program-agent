"""고정 비중(Fixed Weight) 정적 자산배분 전략.

임의의 자산 universe에 대해 사전에 지정된 비중을 리밸런싱 시점마다
동일하게 적용한다. 60/40, All Weather 등 정적 포트폴리오는 별도의
전략 클래스를 만들지 않고 본 전략의 파라미터로 표현한다
(architecture.md 설계 결정 #8).

예시
----
- 60/40 (미국 주식/채권):
    ``weights = {"SPY": 0.6, "AGG": 0.4}``
- All Weather (간소화 버전):
    ``weights = {
        "VTI": 0.30,
        "TLT": 0.40,
        "IEF": 0.15,
        "GLD": 0.075,
        "DBC": 0.075,
    }``
"""

from __future__ import annotations

import math
from typing import ClassVar

import pandas as pd
from pydantic import Field, model_validator

from stock_backtest.backtest.engine import CASH_SYMBOL
from stock_backtest.strategies.base import Strategy, StrategyParams
from stock_backtest.strategies.registry import register

_WEIGHT_SUM_TOLERANCE = 1e-6


class FixedWeightParams(StrategyParams):
    """:class:`FixedWeight` 전략의 파라미터 스키마.

    Attributes
    ----------
    weights : dict[str, float]
        심볼 → 비중 매핑. 값의 합은 1.0 이어야 한다 (tolerance 1e-6).
    rebalance : bool
        각 리밸런싱일마다 비중을 재조정할지 여부. 기본 True.
        False이면 엔진이 드리프트를 허용해야 하지만, 본 전략의
        ``generate_weights``는 리밸런싱 시점별 목표만 반환하므로
        반환 값 자체는 동일하다.
    """

    weights: dict[str, float] = Field(
        ...,
        description=(
            "심볼 → 목표 비중 (합=1). `_CASH_` 키를 포함하면 해당 비중은 " "base_currency 현금으로 보유한다."
        ),
        json_schema_extra={"widget": "asset_weight_map"},
    )
    rebalance: bool = True

    @model_validator(mode="after")
    def _validate_weights_sum(self) -> "FixedWeightParams":
        if not self.weights:
            raise ValueError("weights must not be empty")
        total = sum(self.weights.values())
        if not math.isclose(total, 1.0, abs_tol=_WEIGHT_SUM_TOLERANCE):
            raise ValueError(
                f"weights must sum to 1.0 (got {total!r}, "
                f"tolerance={_WEIGHT_SUM_TOLERANCE})"
            )
        for sym, w in self.weights.items():
            if not isinstance(sym, str) or not sym:
                raise ValueError(f"weight key must be non-empty string, got {sym!r}")
            if not isinstance(w, (int, float)) or math.isnan(float(w)):
                raise ValueError(f"weight for {sym!r} must be a number, got {w!r}")
        return self


@register
class FixedWeight(Strategy):
    """임의 자산에 대한 고정 비중 포트폴리오.

    60/40, All Weather 등 대표적인 정적 자산배분은 본 전략의 파라미터
    (``weights``)로 표현한다.

    Examples
    --------
    >>> params = FixedWeightParams(weights={"SPY": 0.6, "AGG": 0.4})
    >>> strat = FixedWeight(params)
    >>> strat.required_universe()
    ['SPY', 'AGG']
    """

    name: ClassVar[str] = "fixed_weight"
    params_schema: ClassVar[type[StrategyParams]] = FixedWeightParams
    description: ClassVar[str] = (
        "임의 자산에 대한 고정 비중 포트폴리오 "
        "(60/40, All Weather 등 파라미터로 표현). "
        "weights 에 `_CASH_` 를 포함하면 해당 비중은 현금(base_currency)으로 보유."
    )

    def generate_weights(
        self,
        prices: pd.DataFrame,
        rebalance_dates: pd.DatetimeIndex,
    ) -> pd.DataFrame:
        """리밸런싱 시점별 고정 비중 DataFrame을 반환한다.

        Parameters
        ----------
        prices : pd.DataFrame
            일별 가격 시계열. 컬럼은 자산 심볼.
        rebalance_dates : pd.DatetimeIndex
            리밸런싱 일자 목록.

        Returns
        -------
        pd.DataFrame
            index=``rebalance_dates``, columns=``self.params.weights`` 의
            key들 (params 선언 순서 보존). 모든 행이 동일한 비중.

        Raises
        ------
        KeyError
            ``weights``에 지정된 심볼이 ``prices.columns``에 존재하지 않는
            경우.
        """
        assert isinstance(self.params, FixedWeightParams)
        weights: dict[str, float] = self.params.weights

        # `_CASH_` 는 prices 에 없어도 허용 (엔진이 현금 잔고로 처리).
        missing = [s for s in weights if s != CASH_SYMBOL and s not in prices.columns]
        if missing:
            raise KeyError(
                f"symbols {missing!r} missing from prices universe "
                f"(available: {list(prices.columns)!r})"
            )

        columns = list(weights.keys())
        row = [float(weights[s]) for s in columns]
        data = [row for _ in range(len(rebalance_dates))]
        return pd.DataFrame(
            data,
            index=pd.DatetimeIndex(rebalance_dates),
            columns=columns,
            dtype=float,
        )

    def required_universe(self) -> list[str]:
        """``weights``에 선언된 심볼 목록을 반환한다."""
        assert isinstance(self.params, FixedWeightParams)
        return list(self.params.weights.keys())
