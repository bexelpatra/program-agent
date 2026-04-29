"""백테스트 결과 메트릭.

Quant Lab CLAUDE.md L24: CAGR / MDD / Sharpe / Sortino / Calmar / 승률 / 연·월 수익률 테이블.

도메인 순수: equity 시계열 (date, equity) 입력 → 메트릭 dict 출력.
"""

import math
from collections import defaultdict
from collections.abc import Callable, Hashable
from dataclasses import dataclass
from datetime import date
from decimal import Decimal


TRADING_DAYS_PER_YEAR = 252  # US 표준. KR 은 ~245, 단순화.


@dataclass(frozen=True)
class MetricsResult:
    cagr: float  # 연평균 복리 성장률
    mdd: float  # 최대 낙폭 (음수, 예: -0.25)
    sharpe: float  # 샤프 (rf=0 가정)
    sortino: float  # 소티노
    calmar: float  # CAGR / |MDD|
    win_rate: float  # 양수 일별 수익률 비율
    annual_returns: dict[int, float]  # 연도 → 수익률
    monthly_returns: dict[str, float]  # "YYYY-MM" → 수익률


def _daily_returns(equity_series: list[tuple[date, Decimal]]) -> list[float]:
    if len(equity_series) < 2:
        return []
    returns: list[float] = []
    for i in range(1, len(equity_series)):
        prev = float(equity_series[i - 1][1])
        curr = float(equity_series[i][1])
        if prev > 0:
            returns.append(curr / prev - 1.0)
    return returns


def _max_drawdown(equity_series: list[tuple[date, Decimal]]) -> float:
    if not equity_series:
        return 0.0
    peak = float(equity_series[0][1])
    mdd = 0.0
    for _, e in equity_series:
        ev = float(e)
        if ev > peak:
            peak = ev
        if peak > 0:
            dd = ev / peak - 1.0
            if dd < mdd:
                mdd = dd
    return mdd


def _cagr(equity_series: list[tuple[date, Decimal]]) -> float:
    if len(equity_series) < 2:
        return 0.0
    start_d, start_e = equity_series[0]
    end_d, end_e = equity_series[-1]
    years = (end_d - start_d).days / 365.25
    if years <= 0 or float(start_e) <= 0:
        return 0.0
    return (float(end_e) / float(start_e)) ** (1.0 / years) - 1.0


def _annualized(returns: list[float], downside: bool = False) -> float:
    """연환산 std (downside=True 면 음수 returns 만)."""
    sample = [r for r in returns if r < 0] if downside else returns
    if len(sample) < 2:
        return 0.0
    mean = sum(sample) / len(sample)
    var = sum((r - mean) ** 2 for r in sample) / (len(sample) - 1)
    return math.sqrt(var) * math.sqrt(TRADING_DAYS_PER_YEAR)


def _annualized_return(returns: list[float]) -> float:
    if not returns:
        return 0.0
    mean = sum(returns) / len(returns)
    return mean * TRADING_DAYS_PER_YEAR


def _periodic_returns(
    equity_series: list[tuple[date, Decimal]],
    group_key: Callable[[date], Hashable],
) -> dict:
    """기간별 수익률 (연 또는 월). group_key(date) → key."""
    by_group: dict[Hashable, list[tuple[date, Decimal]]] = defaultdict(list)
    for d, e in equity_series:
        by_group[group_key(d)].append((d, e))
    result: dict = {}
    for key, points in by_group.items():
        if len(points) >= 2:
            start_e = float(points[0][1])
            end_e = float(points[-1][1])
            if start_e > 0:
                result[key] = end_e / start_e - 1.0
    return result


def compute_metrics(equity_series: list[tuple[date, Decimal]]) -> MetricsResult:
    """전체 메트릭 1회 계산. equity_series 는 (date, equity_in_base) 시계열."""
    if not equity_series:
        return MetricsResult(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, {}, {})

    returns = _daily_returns(equity_series)
    cagr = _cagr(equity_series)
    mdd = _max_drawdown(equity_series)

    ann_return = _annualized_return(returns)
    vol_total = _annualized(returns, downside=False)
    vol_downside = _annualized(returns, downside=True)

    sharpe = ann_return / vol_total if vol_total > 0 else 0.0
    sortino = ann_return / vol_downside if vol_downside > 0 else 0.0
    calmar = cagr / abs(mdd) if mdd < 0 else 0.0
    win_rate = sum(1 for r in returns if r > 0) / len(returns) if returns else 0.0

    annual = _periodic_returns(equity_series, lambda d: d.year)
    monthly = _periodic_returns(equity_series, lambda d: f"{d.year:04d}-{d.month:02d}")

    return MetricsResult(
        cagr=cagr,
        mdd=mdd,
        sharpe=sharpe,
        sortino=sortino,
        calmar=calmar,
        win_rate=win_rate,
        annual_returns=annual,
        monthly_returns=monthly,
    )
