"""Tests for analysis.seasonality, analysis.political_cycle, analysis.stats."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from stock_backtest.analysis import (
    annotate_significance,
    bootstrap_ci,
    bootstrap_mean_diff,
    daily_returns,
    earnings_season_effect,
    fomc_week_effect,
    halloween_indicator,
    monthly_effect,
    presidential_term_year_effect,
    sell_in_may,
    welch_t_test,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------
@pytest.fixture
def synthetic_prices() -> pd.Series:
    """10년치 합성 일별 가격 시리즈 (B=business day)."""
    idx = pd.bdate_range("2015-01-01", "2024-12-31")
    rng = np.random.default_rng(42)
    # 일별 수익률 drift 2bp + vol 1%
    rets = rng.normal(loc=2e-4, scale=0.01, size=len(idx))
    prices = 100.0 * np.cumprod(1.0 + rets)
    return pd.Series(prices, index=idx, name="adj_close")


@pytest.fixture
def synthetic_returns(synthetic_prices) -> pd.Series:
    return daily_returns(synthetic_prices)


# ---------------------------------------------------------------------------
# seasonality.* sanity
# ---------------------------------------------------------------------------
def test_daily_returns_known_series():
    idx = pd.DatetimeIndex(pd.date_range("2024-01-01", periods=4, freq="D"))
    prices = pd.Series([100.0, 110.0, 99.0, 99.0], index=idx)
    ret = daily_returns(prices)
    assert ret.name == "return"
    assert len(ret) == 3
    assert ret.iloc[0] == pytest.approx(0.10)
    assert ret.iloc[1] == pytest.approx(-0.10)
    assert ret.iloc[2] == pytest.approx(0.0)


def test_monthly_effect_schema(synthetic_returns):
    df = monthly_effect(synthetic_returns)
    assert df.shape == (12, 5)
    assert list(df.columns) == ["mean", "median", "std", "count", "win_rate"]
    assert list(df.index) == list(range(1, 13))
    # 각 월에 표본이 충분히 있어야 함.
    assert (df["count"] > 20).all()
    assert (df["win_rate"].between(0.0, 1.0)).all()


def test_sell_in_may_schema(synthetic_returns):
    df = sell_in_may(synthetic_returns)
    assert list(df.index) == ["may_oct", "nov_apr"]
    assert set(df.columns) == {
        "mean_daily",
        "annualized",
        "std_daily",
        "count",
        "win_rate",
    }
    # 두 반기 모두 샘플수 > 0
    assert (df["count"] > 0).all()
    # annualized 값이 mean_daily 부호와 일치
    for seg in ("may_oct", "nov_apr"):
        m = df.loc[seg, "mean_daily"]
        ann = df.loc[seg, "annualized"]
        if m > 0:
            assert ann > 0
        elif m < 0:
            assert ann < 0


def test_halloween_indicator_distribution(synthetic_returns):
    df = halloween_indicator(synthetic_returns)
    assert {
        "nov_apr_return",
        "may_oct_return",
        "halloween_return",
        "buy_hold_return",
        "excess_return",
    } <= set(df.columns)
    valid = df.dropna(subset=["buy_hold_return"])
    assert len(valid) >= 5
    # 연도별 총수익(buy_hold)에 양수/음수 모두 존재해야 한다.
    bh = valid["buy_hold_return"]
    assert (bh > 0).any()
    assert (bh < 0).any()


# ---------------------------------------------------------------------------
# stats.* tests
# ---------------------------------------------------------------------------
def test_welch_t_test_known_input():
    a = [1.0, 2.0, 3.0, 4.0, 5.0]
    b = [3.0, 4.0, 5.0, 6.0, 7.0]
    res = welch_t_test(a, b)
    assert res["mean_diff"] == pytest.approx(-2.0)
    assert res["n_a"] == 5
    assert res["n_b"] == 5
    # 두 표본 분산 동일, df = 2*(n-1) = 8
    assert res["df"] == pytest.approx(8.0, rel=1e-3)
    # t = (3-5)/sqrt(2.5/5+2.5/5) = -2/1 = -2
    assert res["t"] == pytest.approx(-2.0, rel=1e-3)
    # p < 0.10 (양측)
    assert 0.0 < res["p_value"] < 0.10


def test_welch_t_test_small_sample_returns_nan():
    res = welch_t_test([1.0], [2.0, 3.0, 4.0])
    assert np.isnan(res["t"])
    assert np.isnan(res["p_value"])
    assert np.isnan(res["df"])
    assert res["n_a"] == 1
    assert res["n_b"] == 3


def test_welch_t_test_drops_nan():
    a = [1.0, 2.0, np.nan, 3.0, 4.0, 5.0]
    b = [3.0, 4.0, 5.0, 6.0, 7.0]
    res = welch_t_test(a, b)
    assert res["n_a"] == 5
    assert res["mean_diff"] == pytest.approx(-2.0)


def test_bootstrap_mean_diff_reproducible_and_ci():
    rng = np.random.default_rng(123)
    a = rng.normal(0.5, 1.0, size=200)
    b = rng.normal(0.0, 1.0, size=200)
    r1 = bootstrap_mean_diff(a, b, n_resamples=2000, seed=7)
    r2 = bootstrap_mean_diff(a, b, n_resamples=2000, seed=7)
    # 재현성
    assert r1 == r2
    # 진짜 평균차(약 0.5) 가 CI 안에 있어야 한다.
    assert r1["ci_low"] <= 0.5 <= r1["ci_high"]
    # mean_diff 는 표본 평균 차이
    assert r1["mean_diff"] == pytest.approx(float(np.mean(a) - np.mean(b)))
    # pseudo_p 는 0..1 범위
    assert 0.0 <= r1["pseudo_p"] <= 1.0


def test_bootstrap_mean_diff_shifted_significant():
    rng = np.random.default_rng(0)
    a = rng.normal(1.0, 0.5, size=500)
    b = rng.normal(0.0, 0.5, size=500)
    res = bootstrap_mean_diff(a, b, n_resamples=3000, seed=0)
    # 평균 차이 약 1, CI 가 0 을 포함하지 않아야 함 -> 유의.
    assert res["ci_low"] > 0
    assert res["pseudo_p"] < 0.05


def test_bootstrap_ci_single_sample():
    rng = np.random.default_rng(1)
    values = rng.normal(0.1, 1.0, size=400)
    mean, lo, hi = bootstrap_ci(values, n_resamples=3000, seed=1)
    assert lo < mean < hi
    # 참 평균(0.1)이 CI 안.
    assert lo <= 0.1 <= hi
    # 재현성
    mean2, lo2, hi2 = bootstrap_ci(values, n_resamples=3000, seed=1)
    assert (mean, lo, hi) == (mean2, lo2, hi2)


def test_bootstrap_ci_empty_returns_nan():
    mean, lo, hi = bootstrap_ci([], n_resamples=100, seed=0)
    assert np.isnan(mean) and np.isnan(lo) and np.isnan(hi)


def test_annotate_significance_thresholds():
    assert annotate_significance(0.001) == "***"
    assert annotate_significance(0.009) == "***"
    assert annotate_significance(0.01) == "**"
    assert annotate_significance(0.049) == "**"
    assert annotate_significance(0.05) == "*"
    assert annotate_significance(0.099) == "*"
    assert annotate_significance(0.10) == ""
    assert annotate_significance(0.5) == ""
    assert annotate_significance(float("nan")) == ""
    assert annotate_significance(None) == ""


# ---------------------------------------------------------------------------
# political_cycle.* sanity
# ---------------------------------------------------------------------------
def test_presidential_term_year_effect_schema():
    idx = pd.bdate_range("2016-11-09", "2021-11-08")  # ~5년
    rng = np.random.default_rng(3)
    r = pd.Series(rng.normal(2e-4, 0.01, size=len(idx)), index=idx)
    elections = pd.DatetimeIndex(["2016-11-08", "2020-11-03"])
    df = presidential_term_year_effect(r, elections)
    assert list(df.index) == [1, 2, 3, 4]
    assert df.index.name == "term_year"
    assert set(df.columns) == {"mean_daily", "annualized", "count", "win_rate"}
    assert (df["count"] > 0).all()


def test_fomc_week_effect_schema(synthetic_returns):
    fomc = pd.DatetimeIndex(
        [
            "2020-01-29",
            "2020-03-18",
            "2020-04-29",
            "2020-06-10",
            "2020-07-29",
            "2020-09-16",
            "2020-11-05",
            "2020-12-16",
            "2021-01-27",
            "2021-03-17",
            "2021-04-28",
            "2021-06-16",
            "2022-03-16",
            "2022-06-15",
            "2022-09-21",
            "2022-12-14",
            "2023-03-22",
            "2023-06-14",
            "2023-09-20",
            "2023-12-13",
        ]
    )
    df = fomc_week_effect(synthetic_returns, fomc)
    assert list(df.index) == ["fomc_week", "other_week"]
    assert {"mean_daily", "annualized", "count", "win_rate", "t_stat"} <= set(
        df.columns
    )
    assert (df["count"] > 0).all()
    # t_stat 은 두 행 동일 값
    assert df.loc["fomc_week", "t_stat"] == df.loc["other_week", "t_stat"]


def test_earnings_season_effect_schema(synthetic_returns):
    peaks = pd.DatetimeIndex(
        [f"{y}-{m:02d}-15" for y in range(2015, 2025) for m in (1, 4, 7, 10)]
    )
    df = earnings_season_effect(synthetic_returns, peaks, window=5)
    assert list(df.index) == ["in_window", "out_window"]
    assert {"mean_daily", "annualized", "count", "win_rate", "t_stat"} <= set(
        df.columns
    )
    assert (df["count"] > 0).all()
    # 반환 타입: 수치
    for col in ("mean_daily", "annualized", "win_rate", "t_stat"):
        assert np.issubdtype(df[col].dtype, np.floating)
    assert np.issubdtype(df["count"].dtype, np.integer)
