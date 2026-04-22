"""통계 유의성 검정 헬퍼.

계절성/정치 사이클 등 조건부 수익률 비교를 위한 공용 통계 함수.

- :func:`welch_t_test`: scipy 기반 Welch 독립 2표본 t-검정.
- :func:`bootstrap_mean_diff`: 두 표본 평균 차이 부트스트랩 CI.
- :func:`bootstrap_ci`: 단일 표본 평균 부트스트랩 CI.
- :func:`annotate_significance`: p-value 를 별표 문자열로 변환.

의존성은 :mod:`numpy`, :mod:`pandas`, :mod:`scipy.stats` 뿐이다. scipy 는
Welch t-test 전용이며 부트스트랩은 순수 numpy 로 구현된다.
"""

from __future__ import annotations

from typing import Iterable

import numpy as np
import pandas as pd
from scipy import stats as _sp_stats

__all__ = [
    "welch_t_test",
    "bootstrap_mean_diff",
    "bootstrap_ci",
    "annotate_significance",
]


ArrayLike = Iterable[float] | np.ndarray | pd.Series


def _to_1d_float(arr: ArrayLike, name: str) -> np.ndarray:
    """입력을 1차원 float ndarray 로 변환하고 NaN 을 제거."""
    if isinstance(arr, pd.Series):
        a = arr.to_numpy(dtype=float)
    else:
        a = np.asarray(
            list(arr) if not isinstance(arr, np.ndarray) else arr, dtype=float
        )
    if a.ndim != 1:
        raise ValueError(f"{name} must be 1-dimensional, got shape {a.shape}")
    a = a[~np.isnan(a)]
    return a


def welch_t_test(a: ArrayLike, b: ArrayLike) -> dict[str, float]:
    """두 독립 표본에 대한 Welch's t-test.

    Welch's t-test 는 두 표본의 분산이 서로 다를 수 있다고 가정한다
    (``equal_var=False``). 샘플 크기가 달라도 사용 가능하다.

    Parameters
    ----------
    a, b : array-like
        표본 1/2. ``pandas.Series`` 또는 ``np.ndarray``/리스트 허용.
        NaN 은 자동 제거된다.

    Returns
    -------
    dict
        keys:
        - ``t``: t-통계량
        - ``p_value``: 양측 p-value
        - ``df``: Welch–Satterthwaite 근사 자유도
        - ``mean_diff``: ``mean(a) - mean(b)``
        - ``n_a``, ``n_b``: 표본 크기(NaN 제거 후)

    Notes
    -----
    각 표본의 크기가 2 미만이면 t/p/df 는 ``NaN`` 으로 반환된다.
    """
    x = _to_1d_float(a, "a")
    y = _to_1d_float(b, "b")
    n_a, n_b = int(x.size), int(y.size)
    mean_diff = (float(x.mean()) - float(y.mean())) if n_a and n_b else float("nan")

    if n_a < 2 or n_b < 2:
        return {
            "t": float("nan"),
            "p_value": float("nan"),
            "df": float("nan"),
            "mean_diff": mean_diff,
            "n_a": float(n_a),
            "n_b": float(n_b),
        }

    res = _sp_stats.ttest_ind(x, y, equal_var=False)
    t_stat = float(res.statistic)
    p_val = float(res.pvalue)

    vx = x.var(ddof=1)
    vy = y.var(ddof=1)
    num = (vx / n_a + vy / n_b) ** 2
    den = (vx / n_a) ** 2 / (n_a - 1) + (vy / n_b) ** 2 / (n_b - 1)
    df = float(num / den) if den > 0 else float("nan")

    return {
        "t": t_stat,
        "p_value": p_val,
        "df": df,
        "mean_diff": mean_diff,
        "n_a": float(n_a),
        "n_b": float(n_b),
    }


def bootstrap_mean_diff(
    a: ArrayLike,
    b: ArrayLike,
    *,
    n_resamples: int = 10_000,
    seed: int = 0,
    alpha: float = 0.05,
) -> dict[str, float]:
    """부트스트랩으로 ``mean(a) - mean(b)`` 분포와 신뢰구간 추정.

    각 표본에서 복원추출로 같은 크기의 표본을 ``n_resamples`` 회 뽑아
    ``mean(a*) - mean(b*)`` 분포를 만든다. 분위수 기반 CI 와
    의사 p-value (``2 * min(P(diff>0), P(diff<0))``) 를 계산한다.

    Parameters
    ----------
    a, b : array-like
        표본 1/2. NaN 은 제거된다.
    n_resamples : int, default 10_000
        부트스트랩 반복 횟수. 양의 정수.
    seed : int, default 0
        난수 시드 (:func:`numpy.random.default_rng`). 재현성 보장.
    alpha : float, default 0.05
        유의수준. CI 는 ``[alpha/2, 1 - alpha/2]`` 분위수.

    Returns
    -------
    dict
        keys: ``mean_diff`` (원 표본 차이), ``ci_low``, ``ci_high``,
        ``pseudo_p`` (2 * min(P(diff>0), P(diff<0)), 0..1 로 클램프).
    """
    if n_resamples < 1:
        raise ValueError("n_resamples must be >= 1")
    if not (0.0 < alpha < 1.0):
        raise ValueError("alpha must be in (0, 1)")

    x = _to_1d_float(a, "a")
    y = _to_1d_float(b, "b")
    if x.size < 1 or y.size < 1:
        return {
            "mean_diff": float("nan"),
            "ci_low": float("nan"),
            "ci_high": float("nan"),
            "pseudo_p": float("nan"),
        }

    rng = np.random.default_rng(seed)
    idx_a = rng.integers(0, x.size, size=(n_resamples, x.size))
    idx_b = rng.integers(0, y.size, size=(n_resamples, y.size))
    means_a = x[idx_a].mean(axis=1)
    means_b = y[idx_b].mean(axis=1)
    diffs = means_a - means_b

    ci_low = float(np.quantile(diffs, alpha / 2))
    ci_high = float(np.quantile(diffs, 1.0 - alpha / 2))

    p_gt = float((diffs > 0).mean())
    p_lt = float((diffs < 0).mean())
    pseudo_p = 2.0 * min(p_gt, p_lt)
    pseudo_p = float(max(0.0, min(1.0, pseudo_p)))

    return {
        "mean_diff": float(x.mean() - y.mean()),
        "ci_low": ci_low,
        "ci_high": ci_high,
        "pseudo_p": pseudo_p,
    }


def bootstrap_ci(
    values: ArrayLike,
    *,
    n_resamples: int = 10_000,
    seed: int = 0,
    alpha: float = 0.05,
) -> tuple[float, float, float]:
    """단일 표본 평균에 대한 부트스트랩 신뢰구간.

    Parameters
    ----------
    values : array-like
        표본. NaN 은 제거된다.
    n_resamples : int, default 10_000
        부트스트랩 반복 횟수.
    seed : int, default 0
        난수 시드.
    alpha : float, default 0.05
        유의수준. CI 는 ``[alpha/2, 1 - alpha/2]`` 분위수.

    Returns
    -------
    tuple[float, float, float]
        ``(mean, ci_low, ci_high)``. 표본이 비었으면 모두 ``NaN``.
    """
    if n_resamples < 1:
        raise ValueError("n_resamples must be >= 1")
    if not (0.0 < alpha < 1.0):
        raise ValueError("alpha must be in (0, 1)")

    v = _to_1d_float(values, "values")
    if v.size == 0:
        return (float("nan"), float("nan"), float("nan"))

    rng = np.random.default_rng(seed)
    idx = rng.integers(0, v.size, size=(n_resamples, v.size))
    means = v[idx].mean(axis=1)
    ci_low = float(np.quantile(means, alpha / 2))
    ci_high = float(np.quantile(means, 1.0 - alpha / 2))
    return (float(v.mean()), ci_low, ci_high)


def annotate_significance(p: float) -> str:
    """p-value 를 관례적 별표 문자열로 변환.

    Thresholds:
    - ``p < 0.01`` → ``"***"``
    - ``p < 0.05`` → ``"**"``
    - ``p < 0.10`` → ``"*"``
    - 그 외 (NaN 포함) → ``""``

    Parameters
    ----------
    p : float
        양측 p-value.

    Returns
    -------
    str
        별표 문자열.
    """
    if p is None:
        return ""
    try:
        pv = float(p)
    except (TypeError, ValueError):
        return ""
    if not np.isfinite(pv):
        return ""
    if pv < 0.01:
        return "***"
    if pv < 0.05:
        return "**"
    if pv < 0.10:
        return "*"
    return ""
