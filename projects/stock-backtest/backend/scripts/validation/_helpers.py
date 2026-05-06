"""Validation harness helpers.

엔진 검증용 — 도메인 직접 호출 (DB/API 우회). 가격/FX 시리즈 생성 + ctx 빌드 + 결과 추출.

오라클 독립성: 이 파일의 헬퍼는 엔진 코드를 import 만 하고 알고리즘은 호출 안 함.
가격 생성은 결정적 함수 (math.sin, 선형, step) 만 사용.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Callable, Iterable

import pandas as pd

from app.domain.calendar import trading_days_in_period
from app.domain.engine import BacktestRunContext, run_backtest
from app.domain.metrics import compute_metrics
from app.domain.strategy import Strategy


# ============================================================================
# 가격 시리즈 생성 (결정적)
# ============================================================================


def flat_prices(dates: list[date], price: float) -> list[float]:
    """모든 날짜에 동일 가격."""
    return [price] * len(dates)


def linear_prices(dates: list[date], start: float, end: float) -> list[float]:
    """start → end 선형 보간."""
    n = len(dates)
    if n == 1:
        return [start]
    return [start + (end - start) * i / (n - 1) for i in range(n)]


def crash_recovery_prices(
    dates: list[date],
    peak_idx: int,
    trough_idx: int,
    start: float,
    peak: float,
    trough: float,
    end: float,
) -> list[float]:
    """[start → peak (peak_idx) → trough (trough_idx) → end] 구간별 선형.

    MDD 검증용. peak/trough 자릿수와 위치를 정확히 통제.
    """
    n = len(dates)
    out: list[float] = []
    for i in range(n):
        if i <= peak_idx:
            # start → peak
            frac = i / max(peak_idx, 1)
            out.append(start + (peak - start) * frac)
        elif i <= trough_idx:
            # peak → trough
            frac = (i - peak_idx) / max(trough_idx - peak_idx, 1)
            out.append(peak + (trough - peak) * frac)
        else:
            # trough → end
            frac = (i - trough_idx) / max(n - 1 - trough_idx, 1)
            out.append(trough + (end - trough) * frac)
    return out


def step_prices(
    dates: list[date], steps: list[tuple[int, float]]
) -> list[float]:
    """지정한 인덱스 이후 가격을 step 함수로. steps = [(0, p0), (i1, p1), ...]."""
    if not steps:
        return [0.0] * len(dates)
    steps = sorted(steps)
    out: list[float] = []
    cur = steps[0][1]
    step_idx = 0
    for i in range(len(dates)):
        while step_idx + 1 < len(steps) and steps[step_idx + 1][0] <= i:
            step_idx += 1
            cur = steps[step_idx][1]
        out.append(cur)
    return out


# ============================================================================
# ctx 빌드 + 엔진 실행
# ============================================================================


def build_prices_aligned(
    dates: list[date],
    price_specs: dict[int, list[float]],
) -> pd.DataFrame:
    """asset_id → price list 를 DataFrame 으로."""
    df = pd.DataFrame(price_specs, index=dates)
    df.index.name = "date"
    return df


def build_fx_constant(
    dates: list[date], rates: dict[str, float]
) -> dict[date, dict[str, Decimal]]:
    """모든 날짜에 동일 FX 비율 (base_per_ccy)."""
    return {
        d: {ccy: Decimal(str(r)) for ccy, r in rates.items()} for d in dates
    }


def build_fx_linear(
    dates: list[date], pairs: dict[str, tuple[float, float]]
) -> dict[date, dict[str, Decimal]]:
    n = len(dates)
    out: dict[date, dict[str, Decimal]] = {}
    for i, d in enumerate(dates):
        frac = i / max(n - 1, 1)
        out[d] = {
            ccy: Decimal(str(start + (end - start) * frac))
            for ccy, (start, end) in pairs.items()
        }
    return out


@dataclass
class EngineRun:
    """엔진 실행 결과 + 파생 통계 (오라클 비교 단위)."""

    final_equity: float
    initial_equity: float
    num_equity_points: int
    num_fills: int
    cagr: float
    mdd: float
    sharpe: float
    win_rate: float
    final_qty_by_asset: dict[int, float]  # asset_id → qty
    final_cash_by_ccy: dict[str, float]
    peak_equity: float
    trough_after_peak: float
    fills_summary: list[dict]  # 처음 5건만 (디버깅용)
    aborted: bool


def run_engine_case(
    base_currency: str,
    period_start: date,
    period_end: date,
    initial_cash: dict[str, Decimal],
    universe_market_meta: dict[int, tuple[str, str]],
    prices_aligned: pd.DataFrame,
    fx_rates_to_base: dict[date, dict[str, Decimal]],
    strategy: Strategy,
) -> EngineRun:
    """엔진 1회 실행 → 통계."""
    ctx = BacktestRunContext(
        base_currency=base_currency,
        period_start=period_start,
        period_end=period_end,
        initial_cash=initial_cash,
        universe_market_meta=universe_market_meta,
        prices_aligned=prices_aligned,
        fx_rates_to_base=fx_rates_to_base,
        strategy=strategy,
    )
    result = run_backtest(ctx)

    equity_series = [(p.time, Decimal(p.equity)) for p in result.equity_curve]
    metrics = compute_metrics(equity_series)

    final_equity = float(equity_series[-1][1]) if equity_series else 0.0
    initial_equity = float(equity_series[0][1]) if equity_series else 0.0

    # peak / trough_after_peak (단조 invariant 검증용)
    peak = initial_equity
    peak_idx = 0
    for i, (_, e) in enumerate(equity_series):
        ev = float(e)
        if ev > peak:
            peak = ev
            peak_idx = i
    trough_after_peak = peak
    for _, e in equity_series[peak_idx:]:
        ev = float(e)
        if ev < trough_after_peak:
            trough_after_peak = ev

    final_qty_by_asset: dict[int, float] = {
        aid: float(pos.qty) for aid, pos in result.final_portfolio.positions.items()
    }
    final_cash_by_ccy: dict[str, float] = {
        ccy: float(amt) for ccy, amt in result.final_portfolio.cash_by_ccy.items()
    }
    fills_summary: list[dict] = []
    for f in result.fills[:5]:
        fills_summary.append(
            {
                "asset_id": f.asset_id,
                "side": f.side,
                "qty": float(f.qty_filled),
                "price": float(f.price),
                "commission": float(f.commission),
                "currency": f.currency,
                "settlement_date": f.settlement_date.isoformat(),
            }
        )

    return EngineRun(
        final_equity=final_equity,
        initial_equity=initial_equity,
        num_equity_points=len(equity_series),
        num_fills=len(result.fills),
        cagr=metrics.cagr,
        mdd=metrics.mdd,
        sharpe=metrics.sharpe,
        win_rate=metrics.win_rate,
        final_qty_by_asset=final_qty_by_asset,
        final_cash_by_ccy=final_cash_by_ccy,
        peak_equity=peak,
        trough_after_peak=trough_after_peak,
        fills_summary=fills_summary,
        aborted=result.aborted,
    )


# ============================================================================
# 비교 (허용 오차)
# ============================================================================


def isclose_rel(actual: float, expected: float, rel: float = 1e-6, abs_: float = 1e-9) -> bool:
    return math.isclose(actual, expected, rel_tol=rel, abs_tol=abs_)


@dataclass
class FieldCheck:
    name: str
    actual: float | int | str
    expected: float | int | str
    passed: bool
    rel_tol: float | None = None

    def format(self) -> str:
        if isinstance(self.actual, (int, str)) and isinstance(self.expected, (int, str)):
            return (
                f"  {'PASS' if self.passed else 'FAIL'} {self.name}: "
                f"actual={self.actual} expected={self.expected}"
            )
        try:
            diff = float(self.actual) - float(self.expected)  # type: ignore[arg-type]
            rel_pct = (
                abs(diff) / abs(float(self.expected)) * 100  # type: ignore[arg-type]
                if float(self.expected) != 0  # type: ignore[arg-type]
                else 0
            )
            return (
                f"  {'PASS' if self.passed else 'FAIL'} {self.name}: "
                f"actual={float(self.actual):.6f} expected={float(self.expected):.6f} "  # type: ignore[arg-type]
                f"diff={diff:+.2e} ({rel_pct:.4f}%)"
            )
        except (TypeError, ValueError):
            return f"  {'PASS' if self.passed else 'FAIL'} {self.name}: actual={self.actual} expected={self.expected}"


def check_float(
    name: str, actual: float, expected: float, rel: float = 1e-6, abs_: float = 1e-9
) -> FieldCheck:
    return FieldCheck(
        name=name,
        actual=actual,
        expected=expected,
        passed=isclose_rel(actual, expected, rel=rel, abs_=abs_),
        rel_tol=rel,
    )


def check_eq(name: str, actual, expected) -> FieldCheck:
    return FieldCheck(
        name=name, actual=actual, expected=expected, passed=actual == expected
    )


@dataclass
class CaseResult:
    case_id: str
    title: str
    layer: str
    checks: list[FieldCheck]
    notes: list[str]

    @property
    def passed(self) -> bool:
        return all(c.passed for c in self.checks)

    def format_md(self) -> str:
        lines = [
            f"### {self.case_id} — {self.title} ({self.layer}) — "
            f"{'✅ PASS' if self.passed else '❌ FAIL'}"
        ]
        for c in self.checks:
            lines.append(c.format())
        if self.notes:
            lines.append("  notes:")
            for n in self.notes:
                lines.append(f"    - {n}")
        return "\n".join(lines)


# ============================================================================
# Buy-and-hold 닫힌식 오라클 (Layer 1 핵심)
# ============================================================================


def closed_form_initial_buy(
    available_cash_native: float,
    target_value_native: float,
    price_at_settlement: float,
    commission_bps: float,
    slippage_bps: float,
    fractional: bool = False,
) -> tuple[float, float, float]:
    """초기 매수 1회 닫힌식 — 엔진 매핑 spec.

    엔진 명세 (trade.py L380-397 + portfolio.buy L249-307) — 이는 검증 대상 *명세* 이며
    오라클은 명세 자체를 (다른 코드 패스로) 다시 적용해 엔진이 spec 을 정확히 구현하는지 본다.
    오라클의 "독립성" 은 알고리즘 패러다임 차이 (벡터 한 줄 vs 일별 시뮬), pandas/Decimal
    미사용 (float), 멀티-day path 미시뮬에서 확보된다.

    Args:
        available_cash_native: 매수 가능 native cash (직전 매수 비용 차감 반영)
        target_value_native: target_qty 산출용 = equity_base × weight 의 native 환산
        price_at_settlement: D+1 raw price (slippage 미적용)
        commission_bps: KR=1.5, US=0.5, CRYPTO=10
        slippage_bps: 디폴트 10
        fractional: True 면 8자리 소수 (CRYPTO)

    Returns:
        (actual_qty, total_cost, cash_after)
    """
    if available_cash_native <= 0 or target_value_native <= 0 or price_at_settlement <= 0:
        return 0.0, 0.0, available_cash_native
    s = slippage_bps / 10000.0
    c = commission_bps / 10000.0
    effective_price = price_at_settlement * (1 + s)
    cost_per_unit = effective_price * (1 + c)
    raw_qty = target_value_native / price_at_settlement  # 명세: trade.py L391 raw price
    if fractional:
        target_qty = math.floor(raw_qty * 1e8) / 1e8
        max_affordable = math.floor(available_cash_native / cost_per_unit * 1e8) / 1e8
    else:
        target_qty = float(math.floor(raw_qty))
        max_affordable = float(math.floor(available_cash_native / cost_per_unit))
    actual_qty = min(target_qty, max_affordable)
    if actual_qty <= 0:
        return 0.0, 0.0, available_cash_native
    gross = effective_price * actual_qty
    commission = gross * c
    total_cost = gross + commission
    return actual_qty, total_cost, available_cash_native - total_cost
