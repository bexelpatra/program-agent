"""계절성(Seasonality) 분석 모듈.

월/요일/월말·월초/Sell-in-May/Halloween 효과 계산 함수 집합.

모든 함수는 pandas/numpy만 사용하며, 입력 시리즈의 인덱스는
`pandas.DatetimeIndex` 여야 한다. 그렇지 않으면 ``ValueError`` 를 발생시킨다.

입력 규약
---------
- ``prices``: 일별 조정 종가(`adj_close`) 시계열 (``pd.Series``).
- ``returns``: 일별 단순 수익률(산술) 시계열 (``pd.Series``). 보통
  ``daily_returns(prices)`` 의 반환값. NaN 은 계산 시 자동 제외된다.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

__all__ = [
    "daily_returns",
    "monthly_effect",
    "day_of_week_effect",
    "month_edge_effect",
    "sell_in_may",
    "halloween_indicator",
]


# ---------------------------------------------------------------------------
# 내부 유틸
# ---------------------------------------------------------------------------


def _ensure_datetime_index(s: pd.Series, name: str = "series") -> pd.Series:
    """인덱스가 DatetimeIndex인지 검증하고 정렬/NaN 제거한 사본을 반환."""
    if not isinstance(s.index, pd.DatetimeIndex):
        raise ValueError(
            f"{name} must have a pandas.DatetimeIndex, got {type(s.index).__name__}"
        )
    out = s.sort_index()
    return out


def _summary_stats(group: pd.Series) -> pd.Series:
    """평균/중앙값/표준편차/샘플수/승률을 계산."""
    clean = group.dropna()
    n = int(clean.shape[0])
    if n == 0:
        return pd.Series(
            {
                "mean": np.nan,
                "median": np.nan,
                "std": np.nan,
                "count": 0,
                "win_rate": np.nan,
            }
        )
    return pd.Series(
        {
            "mean": float(clean.mean()),
            "median": float(clean.median()),
            "std": float(clean.std(ddof=1)) if n > 1 else np.nan,
            "count": n,
            "win_rate": float((clean > 0).mean()),
        }
    )


# ---------------------------------------------------------------------------
# 퍼블릭 API
# ---------------------------------------------------------------------------


def daily_returns(prices: pd.Series) -> pd.Series:
    """일별 단순 수익률 계산.

    Parameters
    ----------
    prices : pd.Series
        DatetimeIndex, 일별 ``adj_close`` 가격.

    Returns
    -------
    pd.Series
        ``prices.pct_change()`` 결과에서 첫 날(NaN) 제거한 Series.
        이름은 ``"return"``.
    """
    p = _ensure_datetime_index(prices, "prices")
    ret = p.pct_change().iloc[1:]
    ret.name = "return"
    return ret


def monthly_effect(returns: pd.Series) -> pd.DataFrame:
    """월별(1~12) 수익률 통계 테이블.

    Parameters
    ----------
    returns : pd.Series
        DatetimeIndex, 일별 수익률.

    Returns
    -------
    pd.DataFrame
        index=1..12 (``month``), columns=[``mean``, ``median``, ``std``,
        ``count``, ``win_rate``]. 값은 일별 수익률 기준.
    """
    r = _ensure_datetime_index(returns, "returns")
    grouped = r.groupby(r.index.month).apply(_summary_stats)
    # groupby+apply on a Series returning Series -> DataFrame with MultiIndex or
    # a wide DataFrame. Normalize shape.
    if isinstance(grouped, pd.Series):
        grouped = grouped.unstack()
    grouped.index.name = "month"
    # 누락 월이 있으면 1..12 로 reindex.
    grouped = grouped.reindex(range(1, 13))
    grouped["count"] = grouped["count"].fillna(0).astype(int)
    return grouped[["mean", "median", "std", "count", "win_rate"]]


def day_of_week_effect(returns: pd.Series) -> pd.DataFrame:
    """요일별(Mon~Fri) 수익률 통계 테이블.

    Parameters
    ----------
    returns : pd.Series
        DatetimeIndex, 일별 수익률.

    Returns
    -------
    pd.DataFrame
        index=[``Mon``, ``Tue``, ``Wed``, ``Thu``, ``Fri``],
        columns=[``mean``, ``median``, ``std``, ``count``, ``win_rate``].
        주말(토/일) 데이터가 있을 경우에도 주식시장 분석 목적상 Mon~Fri 만
        반환한다. 크립토 등 주말 데이터를 분석하려면 호출 측에서 직접
        ``groupby(returns.index.day_name())`` 등을 사용해야 한다.
    """
    r = _ensure_datetime_index(returns, "returns")
    labels = ["Mon", "Tue", "Wed", "Thu", "Fri"]
    grouped = r.groupby(r.index.dayofweek).apply(_summary_stats)
    if isinstance(grouped, pd.Series):
        grouped = grouped.unstack()
    # 0=Mon ... 4=Fri
    grouped = grouped.reindex(range(0, 5))
    grouped.index = labels
    grouped.index.name = "day_of_week"
    grouped["count"] = grouped["count"].fillna(0).astype(int)
    return grouped[["mean", "median", "std", "count", "win_rate"]]


def _t_stat(x: np.ndarray, y: np.ndarray) -> float:
    """독립 2표본 Welch t-통계량. 샘플 부족 시 NaN."""
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    nx, ny = x.size, y.size
    if nx < 2 or ny < 2:
        return float("nan")
    vx = x.var(ddof=1)
    vy = y.var(ddof=1)
    denom = np.sqrt(vx / nx + vy / ny)
    if denom == 0 or not np.isfinite(denom):
        return float("nan")
    return float((x.mean() - y.mean()) / denom)


def month_edge_effect(returns: pd.Series, window: int = 3) -> pd.DataFrame:
    """월말 N일 vs 월초 N일 vs 중간 구간 수익률 비교.

    각 달(year, month)의 거래일을 날짜 순으로 나열하여
    - 첫 ``window`` 일 → ``month_start``
    - 마지막 ``window`` 일 → ``month_end``
    - 그 사이 → ``middle``
    로 구분한다. 거래일 수가 ``2*window`` 미만이면 가능한 만큼만
    끝/시작에 배정하고 중간은 비워 둔다.

    Parameters
    ----------
    returns : pd.Series
        DatetimeIndex, 일별 수익률.
    window : int, default 3
        양 끝(월초·월말) 윈도 크기(거래일 기준).

    Returns
    -------
    pd.DataFrame
        index=[``month_start``, ``middle``, ``month_end``],
        columns=[``mean``, ``count``,
                 ``t_stat_vs_middle``, ``t_stat_end_vs_start``].
        ``t_stat_vs_middle`` 은 해당 구간과 middle 의 Welch t-통계량
        (middle 행은 NaN). ``t_stat_end_vs_start`` 는 월말 vs 월초
        t-통계량으로 month_end 행에만 값이 들어가고 나머지는 NaN.
    """
    if window < 1:
        raise ValueError("window must be >= 1")
    r = _ensure_datetime_index(returns, "returns").dropna()

    # 각 날짜에 (year, month) 그룹 내 rank(앞에서)와 reverse rank(뒤에서)를 부여.
    ym = r.index.to_period("M")
    df = pd.DataFrame({"ret": r.values, "ym": ym}, index=r.index)
    df["fwd_rank"] = df.groupby("ym").cumcount()  # 0부터
    # 뒤에서부터 순위: 그룹 크기에서 역산
    grp_size = df.groupby("ym")["ret"].transform("size")
    df["bwd_rank"] = grp_size - 1 - df["fwd_rank"]

    start_mask = df["fwd_rank"] < window
    end_mask = df["bwd_rank"] < window
    # start 와 end 가 겹치는(작은 달) 경우: end 우선(월말 효과 연구가 목적).
    start_only = start_mask & ~end_mask
    middle_mask = ~start_mask & ~end_mask

    start_vals = df.loc[start_only, "ret"].to_numpy()
    end_vals = df.loc[end_mask, "ret"].to_numpy()
    mid_vals = df.loc[middle_mask, "ret"].to_numpy()

    def _mean(a: np.ndarray) -> float:
        return float(a.mean()) if a.size else float("nan")

    out = pd.DataFrame(
        {
            "mean": [_mean(start_vals), _mean(mid_vals), _mean(end_vals)],
            "count": [start_vals.size, mid_vals.size, end_vals.size],
            "t_stat_vs_middle": [
                _t_stat(start_vals, mid_vals),
                float("nan"),
                _t_stat(end_vals, mid_vals),
            ],
            "t_stat_end_vs_start": [
                float("nan"),
                float("nan"),
                _t_stat(end_vals, start_vals),
            ],
        },
        index=["month_start", "middle", "month_end"],
    )
    out.index.name = "segment"
    return out


def sell_in_may(returns: pd.Series) -> pd.DataFrame:
    """Sell-in-May 효과(5~10월 vs 11~4월) 평균/연환산 수익률 비교.

    Parameters
    ----------
    returns : pd.Series
        DatetimeIndex, 일별 수익률.

    Returns
    -------
    pd.DataFrame
        index=[``may_oct``, ``nov_apr``],
        columns=[``mean_daily``, ``annualized``, ``std_daily``,
                 ``count``, ``win_rate``].
        ``annualized`` = ``(1 + mean_daily) ** 252 - 1``.
    """
    r = _ensure_datetime_index(returns, "returns").dropna()
    months = r.index.month
    may_oct = r[(months >= 5) & (months <= 10)]
    nov_apr = r[(months <= 4) | (months >= 11)]

    def _row(x: pd.Series) -> dict:
        n = int(x.shape[0])
        if n == 0:
            return {
                "mean_daily": np.nan,
                "annualized": np.nan,
                "std_daily": np.nan,
                "count": 0,
                "win_rate": np.nan,
            }
            # (unreachable, but kept explicit)
        m = float(x.mean())
        return {
            "mean_daily": m,
            "annualized": float((1.0 + m) ** 252 - 1.0),
            "std_daily": float(x.std(ddof=1)) if n > 1 else np.nan,
            "count": n,
            "win_rate": float((x > 0).mean()),
        }

    out = pd.DataFrame([_row(may_oct), _row(nov_apr)], index=["may_oct", "nov_apr"])
    out.index.name = "period"
    return out[["mean_daily", "annualized", "std_daily", "count", "win_rate"]]


def halloween_indicator(returns: pd.Series) -> pd.DataFrame:
    """Halloween 전략(11~4월 매수, 5~10월 현금) 연도별 비교.

    "연도" 는 해당 Halloween 시즌이 끝나는 해(=4월 종료 연도)를 사용.
    즉 2020-11-01 ~ 2021-04-30 의 nov_apr 수익률은 ``season_end_year=2021``
    로 집계되며, 같은 2021년의 may_oct(2021-05~2021-10) 수익률과 나란히
    비교된다. 이는 Bouman & Jacobsen (2002) 의 정의에 가깝다.

    Parameters
    ----------
    returns : pd.Series
        DatetimeIndex, 일별 수익률.

    Returns
    -------
    pd.DataFrame
        index=``season_end_year`` (int),
        columns=[``nov_apr_return``, ``may_oct_return``,
                 ``halloween_return``, ``buy_hold_return``, ``excess_return``].
        - ``nov_apr_return``: 해당 연도 직전 11월~4월 복리 수익률.
        - ``may_oct_return``: 해당 연도 5월~10월 복리 수익률.
        - ``halloween_return``: nov_apr 구간만 투자한 전략의 연 수익률
          (= ``nov_apr_return``; may_oct 은 현금=0 수익).
        - ``buy_hold_return``: ``(1+nov_apr)*(1+may_oct) - 1``.
        - ``excess_return``: ``halloween_return - buy_hold_return``.
        둘 중 한 시즌이라도 데이터가 전혀 없으면 해당 연도는 NaN 포함.
    """
    r = _ensure_datetime_index(returns, "returns").dropna()
    if r.empty:
        return pd.DataFrame(
            columns=[
                "nov_apr_return",
                "may_oct_return",
                "halloween_return",
                "buy_hold_return",
                "excess_return",
            ]
        )

    years = r.index.year
    months = r.index.month
    # season_end_year 매핑:
    #   month in [1..4]  -> year (그대로)
    #   month in [5..10] -> year (그대로, may_oct 시즌)
    #   month in [11,12] -> year + 1 (다음해 4월에 종료되는 nov_apr 시즌)
    season_end_year = np.where(months >= 11, years + 1, years)
    season = np.where((months >= 5) & (months <= 10), "may_oct", "nov_apr")

    df = pd.DataFrame(
        {"ret": r.values, "sey": season_end_year, "season": season}, index=r.index
    )

    # 복리 수익률 = prod(1+r) - 1
    def _compound(x: pd.Series) -> float:
        if x.empty:
            return np.nan
        return float(np.prod(1.0 + x.to_numpy()) - 1.0)

    grp = df.groupby(["sey", "season"])["ret"].apply(_compound).unstack("season")
    grp = grp.reindex(columns=["nov_apr", "may_oct"])
    grp.index.name = "season_end_year"
    grp.columns = ["nov_apr_return", "may_oct_return"]

    grp["halloween_return"] = grp["nov_apr_return"]  # may_oct = 0 (현금)
    grp["buy_hold_return"] = (1.0 + grp["nov_apr_return"]).fillna(1.0) * (
        1.0 + grp["may_oct_return"]
    ).fillna(1.0) - 1.0
    # 하지만 두 시즌 중 하나라도 원래 NaN이면 buy_hold 도 NaN 으로 표시해
    # 데이터 가용성 혼동을 피한다.
    na_mask = grp["nov_apr_return"].isna() | grp["may_oct_return"].isna()
    grp.loc[na_mask, "buy_hold_return"] = np.nan
    grp["excess_return"] = grp["halloween_return"] - grp["buy_hold_return"]

    return grp[
        [
            "nov_apr_return",
            "may_oct_return",
            "halloween_return",
            "buy_hold_return",
            "excess_return",
        ]
    ]
