"""TASK-304 — normalization.py 단위 테스트 (8건).

수학적 성질 검증:
    - rebase 첫 유효값 == base_value
    - equal aggregate[i] == mean(prices_df.iloc[i].dropna())
    - market_cap weighting placeholder (Phase 2.2 NotImplementedError)
"""

from decimal import Decimal

import numpy as np
import pandas as pd
import pytest

from app.domain.themes.normalization import (
    aggregate_equal_weighted,
    compute_theme_aggregate,
    rebase_multi_series,
    rebase_series,
)


def test_rebase_series_basic():
    """1) prices=[100, 110, 121] → [100, 110, 121] (base=100)."""
    prices = pd.Series([100.0, 110.0, 121.0])
    result = rebase_series(prices, base_value=Decimal("100"))
    pd.testing.assert_series_equal(
        result,
        pd.Series([100.0, 110.0, 121.0]),
        check_exact=False,
        rtol=1e-12,
    )
    # 수학적 성질: 첫 유효값 == base_value
    assert result.iloc[0] == pytest.approx(100.0)


def test_rebase_series_with_leading_nan():
    """2) [NaN, NaN, 50, 60, 75] base=100 → [NaN, NaN, 100, 120, 150]."""
    prices = pd.Series([np.nan, np.nan, 50.0, 60.0, 75.0])
    result = rebase_series(prices, base_value=Decimal("100"))
    # leading NaN 보존
    assert pd.isna(result.iloc[0])
    assert pd.isna(result.iloc[1])
    # 첫 유효값 == base_value
    assert result.iloc[2] == pytest.approx(100.0)
    # 비율 보존
    assert result.iloc[3] == pytest.approx(120.0)
    assert result.iloc[4] == pytest.approx(150.0)


def test_rebase_series_all_nan():
    """3) all NaN 입력 → all NaN 출력 (예외 없음)."""
    prices = pd.Series([np.nan, np.nan, np.nan])
    result = rebase_series(prices, base_value=Decimal("100"))
    assert result.isna().all()
    assert len(result) == 3


def test_rebase_multi_series_independent_columns():
    """4) DataFrame 2 컬럼 각각 독립 rebase.

    A: [200, 220, 240] → [100, 110, 120]
    B: [50,  55,  60]  → [100, 110, 120]
    """
    df = pd.DataFrame(
        {
            "A": [200.0, 220.0, 240.0],
            "B": [50.0, 55.0, 60.0],
        }
    )
    result = rebase_multi_series(df, base_value=Decimal("100"))
    # 각 컬럼 첫 유효값 == 100
    assert result["A"].iloc[0] == pytest.approx(100.0)
    assert result["B"].iloc[0] == pytest.approx(100.0)
    # 컬럼별 독립 비율
    assert result["A"].iloc[1] == pytest.approx(110.0)
    assert result["A"].iloc[2] == pytest.approx(120.0)
    assert result["B"].iloc[1] == pytest.approx(110.0)
    assert result["B"].iloc[2] == pytest.approx(120.0)


def test_aggregate_equal_weighted_basic():
    """5) 3 컬럼 [100, 200, 300] → 200, NaN skip."""
    df = pd.DataFrame(
        {
            "A": [100.0],
            "B": [200.0],
            "C": [300.0],
        }
    )
    result = aggregate_equal_weighted(df)
    # 수학적 성질: aggregate[0] == mean([100, 200, 300]) == 200
    assert result.iloc[0] == pytest.approx(200.0)
    # 수학적 성질: aggregate[i] == mean(prices_df.iloc[i].dropna())
    assert result.iloc[0] == pytest.approx(df.iloc[0].dropna().mean())


def test_aggregate_equal_weighted_skipna():
    """6) 일부 NaN 행 → 나머지 값 평균.

    행 0: [100, 200, NaN] → mean(100, 200) = 150
    행 1: [NaN, NaN, NaN] → NaN
    행 2: [50, NaN, 150] → mean(50, 150) = 100
    """
    df = pd.DataFrame(
        {
            "A": [100.0, np.nan, 50.0],
            "B": [200.0, np.nan, np.nan],
            "C": [np.nan, np.nan, 150.0],
        }
    )
    result = aggregate_equal_weighted(df)
    assert result.iloc[0] == pytest.approx(150.0)
    assert pd.isna(result.iloc[1])  # 모든 컬럼 NaN
    assert result.iloc[2] == pytest.approx(100.0)
    # 수학적 성질 재확인
    assert result.iloc[0] == pytest.approx(df.iloc[0].dropna().mean())
    assert result.iloc[2] == pytest.approx(df.iloc[2].dropna().mean())


def test_aggregate_empty_df():
    """7) 빈 DataFrame → 빈 Series."""
    df = pd.DataFrame()
    result = aggregate_equal_weighted(df)
    assert isinstance(result, pd.Series)
    assert len(result) == 0


def test_compute_theme_aggregate_market_cap_not_implemented():
    """8) weighting='market_cap' + market_cap_df=None → NotImplementedError."""
    df = pd.DataFrame({"A": [100.0, 110.0], "B": [200.0, 220.0]})
    with pytest.raises(NotImplementedError, match="Phase 2.2"):
        compute_theme_aggregate(df, weighting="market_cap", market_cap_df=None)
