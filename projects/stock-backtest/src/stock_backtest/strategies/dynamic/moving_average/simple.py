"""단일 이동평균선(Simple Moving Average) 기반 동적 스위칭 전략.

대상 자산(``target_symbol``)의 가격이 단일 이동평균선 위에 있으면
롱 100%, 아래이면 ``exit_action`` 에 따라 현금(`_CASH_`) 또는
로테이션 자산으로 스위칭하는 고전적 추세추종 전략.

설계 노트
---------
- 신호 산출: ``price > ma`` (MA 상향 돌파/상회) 이면 target 100%.
  ``price < ma`` (MA 하회, 데드크로스 류) 이면 exit.
- **look-ahead 방지**: 리밸런싱일 ``t`` 의 판단에는 ``t-1`` 까지의
  가격 기반 이평선을 사용한다 (``.shift(1)`` 적용).
- 워밍업(window 미만) 구간은 신호 OFF 로 fallback.
"""

from __future__ import annotations

from typing import ClassVar, Literal

import pandas as pd
from pydantic import Field, model_validator

from stock_backtest.backtest.engine import CASH_SYMBOL
from stock_backtest.strategies.base import Strategy, StrategyParams
from stock_backtest.strategies.registry import register


def rolling_mean(prices: pd.Series, window: int) -> pd.Series:
    """가격 시계열의 단순 이동평균(SMA)을 반환한다.

    ``window`` 는 양의 정수여야 하며, 초기 ``window - 1`` 개 구간은
    ``min_periods=window`` 정책에 따라 NaN 으로 남는다.
    """
    if window < 1:
        raise ValueError(f"window must be >= 1, got {window}")
    return prices.rolling(window=window, min_periods=window).mean()


class SimpleMovingAverageParams(StrategyParams):
    """:class:`SimpleMovingAverage` 전략 파라미터.

    Attributes
    ----------
    target_symbol : str
        신호 ON 시 롱으로 보유할 대상 자산 심볼.
    exit_action : {"cash", "rotate"}
        신호 OFF 시 동작. 'cash' = base_currency 현금, 'rotate' =
        ``rotate_symbol`` 로 로테이션.
    rotate_symbol : str | None
        exit_action='rotate' 일 때 필수.
    window : int
        단일 이동평균 창(일). 기본 200.
    """

    target_symbol: str = Field(
        ...,
        min_length=1,
        description="가격 > MA 시 100% 보유할 대상 자산 심볼 (예: SPY, QQQ)",
        json_schema_extra={"widget": "asset_symbol"},
    )
    exit_action: Literal["cash", "rotate"] = Field(
        "cash",
        description=(
            "가격 < MA (신호 OFF) 시 동작. "
            "'cash' = base_currency 현금 보유, "
            "'rotate' = rotate_symbol 로 100% 로테이션."
        ),
    )
    rotate_symbol: str | None = Field(
        None,
        description=("exit_action='rotate' 일 때 로테이션 대상 심볼 (예: BIL, SHY, TLT)."),
        json_schema_extra={"widget": "asset_symbol"},
    )
    window: int = Field(
        200,
        gt=0,
        description="단일 이동평균선 기간(일). 가격이 이 MA 위에 있으면 target 보유.",
    )

    @model_validator(mode="after")
    def _check(self) -> "SimpleMovingAverageParams":
        if self.exit_action == "rotate":
            if self.rotate_symbol is None or not self.rotate_symbol:
                raise ValueError("rotate_symbol is required when exit_action='rotate'")
            if self.rotate_symbol == self.target_symbol:
                raise ValueError(
                    f"rotate_symbol must differ from target_symbol "
                    f"(both = {self.target_symbol!r})"
                )
        return self


@register
class SimpleMovingAverage(Strategy):
    """단일 MA 와 가격 비교 기반 롱 스위칭 전략."""

    name: ClassVar[str] = "simple_moving_average"
    params_schema: ClassVar[type[StrategyParams]] = SimpleMovingAverageParams
    description: ClassVar[str] = (
        "가격이 단일 이동평균선 위에 있으면 target_symbol 을 100% 보유, "
        "아래이면 exit_action 에 따라 base_currency 현금(cash) 또는 "
        "rotate_symbol 로 로테이션. 단일 MA 추세추종의 고전."
    )

    def _exit_column(self) -> str:
        assert isinstance(self.params, SimpleMovingAverageParams)
        if self.params.exit_action == "cash":
            return CASH_SYMBOL
        assert self.params.rotate_symbol is not None
        return self.params.rotate_symbol

    def generate_weights(
        self,
        prices: pd.DataFrame,
        rebalance_dates: pd.DatetimeIndex,
    ) -> pd.DataFrame:
        """리밸런싱 시점별 목표 비중 DataFrame을 반환한다."""
        assert isinstance(self.params, SimpleMovingAverageParams)
        target = self.params.target_symbol
        exit_col = self._exit_column()
        window = int(self.params.window)

        required = [target]
        if self.params.exit_action == "rotate":
            required.append(exit_col)
        missing = [s for s in required if s not in prices.columns]
        if missing:
            raise KeyError(
                f"symbols {missing!r} missing from prices universe "
                f"(available: {list(prices.columns)!r})"
            )

        price = prices[target].astype(float)
        ma = rolling_mean(price, window)
        raw = (price > ma).astype(int)
        raw = raw.where(~ma.isna(), 0)
        signal = raw.shift(1).fillna(0).astype(int)

        columns = [target, exit_col]
        out = pd.DataFrame(
            0.0,
            index=pd.DatetimeIndex(rebalance_dates),
            columns=columns,
            dtype=float,
        )

        for date in rebalance_dates:
            locs = signal.index.get_indexer([date], method="pad")
            loc = int(locs[0]) if len(locs) > 0 else -1
            if loc < 0:
                out.at[date, exit_col] = 1.0
                continue
            s_val = int(signal.iloc[loc])
            if s_val == 1:
                out.at[date, target] = 1.0
            else:
                out.at[date, exit_col] = 1.0

        return out

    def required_universe(self) -> list[str]:
        """엔진이 prices 로 로드할 자산 심볼 목록 (``_CASH_`` 제외)."""
        assert isinstance(self.params, SimpleMovingAverageParams)
        if self.params.exit_action == "rotate":
            assert self.params.rotate_symbol is not None
            return [self.params.target_symbol, self.params.rotate_symbol]
        return [self.params.target_symbol]
