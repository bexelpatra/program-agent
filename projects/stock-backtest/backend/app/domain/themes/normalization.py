"""테마 시계열 정규화 (V3 Phase 2 — rebase=100 / equal weighting).

architecture.md V3 § "정규화 차트 사양" (L1038-1045):
- rebase=100: 시리즈 첫 유효 가격을 100 으로 두고 비율 환산
- weighting=equal: 멤버 시리즈 산술 평균 (디폴트)
- weighting=market_cap: 일자별 시가총액 가중 (Phase 2.2 placeholder)

도메인 순수 (CLAUDE.md L1063-1067 + TASK-309):
허용 import: stdlib (decimal/typing) + pandas 만.
금지: sqlalchemy, fastapi, requests, httpx, yfinance, pykrx, app.data,
app.api, app.services. 또한 `app.domain.themes` ↔
`app.domain.{engine, strategy, allocators, filters, trade, portfolio}` 양방향
import 금지.

수치 정밀도 결정 (Coder):
    base_value 는 Decimal 로 받지만 pandas 시리즈 연산은 float 으로 처리한다.
    이유: pandas Series.dtype=object(Decimal) 은 산술 시 Python 루프로 떨어져
    O(N) 비용이 100~1000x 커지고 NaN 처리 호환성도 떨어진다. 정규화 차트는
    표시용 (소수점 둘째자리 % 단위) 이라 float64 정밀도 (~15 유효숫자) 로
    충분하다. 백테스트 회계 (engine.py) 는 Decimal 유지 (불변).
"""

from decimal import Decimal
from typing import Literal

import pandas as pd


def rebase_series(
    prices: pd.Series, base_value: Decimal = Decimal("100")
) -> pd.Series:
    """첫 유효 가격을 base_value 로 정규화.

    규칙:
        - leading NaN 보존 (첫 유효값 == base_value).
        - 모든 값이 NaN 이면 입력을 그대로 반환 (예외 없음).
        - 첫 유효값이 0 이면 ValueError. (rebase=100 의 의미상 0 으로 나눌 수
          없고, NaN 시리즈로 강등하면 호출자가 "데이터 없음" 과 구별 불가하다.
          0 가격은 입력 데이터 결함으로 호출자가 사전 필터해야 한다.)

    Args:
        prices: float 시계열 (DatetimeIndex 권장).
        base_value: 정규화 기준값 (디폴트 Decimal("100")).

    Returns:
        rebase 된 float Series (입력과 동일 인덱스).
    """
    if prices.empty:
        return prices.copy()

    # 모든 값이 NaN 인 경우 입력을 그대로 반환
    first_valid_idx = prices.first_valid_index()
    if first_valid_idx is None:
        return prices.copy()

    first_value = float(prices.loc[first_valid_idx])
    if first_value == 0.0:
        raise ValueError(
            "rebase_series: first valid price is 0; cannot rebase. "
            "Caller must filter zero-price assets before normalization."
        )

    base = float(base_value)
    return prices.astype(float) * (base / first_value)


def rebase_multi_series(
    prices_df: pd.DataFrame, base_value: Decimal = Decimal("100")
) -> pd.DataFrame:
    """DataFrame 의 각 컬럼을 독립적으로 rebase.

    각 컬럼은 자기 자신의 첫 유효값을 base_value 로 정규화한다 (서로 다른
    상장일/거래 시작일 허용).

    Args:
        prices_df: 컬럼이 asset_id (또는 ticker), index 가 date 인 DataFrame.
        base_value: 정규화 기준값.

    Returns:
        동일 shape / 인덱스 / 컬럼의 rebase 된 DataFrame.
    """
    if prices_df.empty:
        return prices_df.copy()

    return prices_df.apply(
        lambda col: rebase_series(col, base_value=base_value), axis=0
    )


def aggregate_equal_weighted(prices_df: pd.DataFrame) -> pd.Series:
    """일자별 산술 평균 시리즈 (equal weighting).

    NaN skip (pandas `.mean(axis=1, skipna=True)` 기본 동작):
        - 행 내 일부 컬럼만 NaN 이면 나머지 값의 평균.
        - 행 내 모든 컬럼이 NaN 이면 NaN.

    Args:
        prices_df: 멤버 자산 시계열 (rebase 후 시리즈 권장; 그러나 함수는
            rebase 여부를 가정하지 않는다).

    Returns:
        일자별 평균 Series (input.index 와 동일).
    """
    if prices_df.empty:
        # 빈 DataFrame → 빈 Series (인덱스 보존)
        return pd.Series(dtype=float, index=prices_df.index)

    return prices_df.mean(axis=1, skipna=True)


def compute_theme_aggregate(
    prices_df: pd.DataFrame,
    weighting: Literal["equal", "market_cap"] = "equal",
    market_cap_df: pd.DataFrame | None = None,
) -> pd.Series:
    """테마 합산 시계열 계산 (weighting 라우터).

    weighting='equal' → aggregate_equal_weighted.
    weighting='market_cap':
        - market_cap_df is None → NotImplementedError (Phase 2.2 에서 활성화).
        - market_cap_df 제공 → 일자별 시가총액 가중 평균.

    market_cap weighting 수식:
        aggregate[t] = sum_i (prices_df[t, i] * market_cap_df[t, i]) /
                       sum_i (market_cap_df[t, i])
        단, 일자별로 prices/market_cap 둘 다 유효한 자산만 분자/분모에 포함.
        분모가 0 또는 NaN 인 행은 NaN.

    Args:
        prices_df: 멤버 자산 시계열 (rebase 후 권장).
        weighting: 'equal' | 'market_cap'.
        market_cap_df: weighting='market_cap' 시 필수 (prices_df 와 동일
            index/columns). architecture.md L1043 폴백 (시총 누락 자산
            equal 폴백 + UI 경고) 은 호출자 (API 레이어) 책임.

    Returns:
        테마 합산 일별 시리즈 (input.index 와 동일).

    Raises:
        NotImplementedError: weighting='market_cap' 이지만 market_cap_df=None.
        ValueError: 알 수 없는 weighting.
    """
    if weighting == "equal":
        return aggregate_equal_weighted(prices_df)
    if weighting == "market_cap":
        if market_cap_df is None:
            raise NotImplementedError(
                "market_cap weighting requires market_cap_df — Phase 2.2"
            )
        # Phase 2.2 활성화 본체: 인덱스/컬럼 정렬 후 가중 평균.
        aligned_caps = market_cap_df.reindex(
            index=prices_df.index, columns=prices_df.columns
        )
        prices_f = prices_df.astype(float)
        caps_f = aligned_caps.astype(float)
        # 둘 중 어느 쪽이 NaN 이면 양쪽 모두 NaN 처리 (mask)
        valid = prices_f.notna() & caps_f.notna()
        weighted = (prices_f * caps_f).where(valid)
        weights = caps_f.where(valid)
        numerator = weighted.sum(axis=1, skipna=True, min_count=1)
        denominator = weights.sum(axis=1, skipna=True, min_count=1)
        # 분모 0 또는 NaN → NaN
        result = numerator / denominator.where(denominator != 0)
        return result
    raise ValueError(
        f"unknown weighting: {weighting!r} (expected 'equal' | 'market_cap')"
    )
