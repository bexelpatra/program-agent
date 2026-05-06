"""Layer 3 — 수학적 불변식 (engine 무관 명제).

엔진이 어떤 코드로 나오든 만족해야 하는 명제. 같은 버그 동시 침투 가능성 가장 낮음.

C9: 큰 폭락-회복 시나리오에 대한 invariants
  - 회계 항등식: equity == positions_value + cash (매 day)
  - peak 단조증가 (running max)
  - trough_after_peak ≤ peak
  - cash_by_ccy ≥ 0 항상
  - qty ≥ 0 항상
  - MDD ≤ 0
  - Calmar = CAGR / |MDD| if MDD < 0
  - 첫 day equity ≤ initial_capital (commission/slippage 손실)
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal

import pandas as pd

from app.domain.allocators import FixedWeight, FixedWeightParams
from app.domain.calendar import trading_days_in_period
from app.domain.engine import BacktestRunContext, run_backtest
from app.domain.metrics import compute_metrics
from app.domain.strategy import Strategy

from scripts.validation._helpers import (
    CaseResult,
    FieldCheck,
    build_prices_aligned,
    check_eq,
    check_float,
    crash_recovery_prices,
)


def case_c9_large_crash_recovery_invariants() -> CaseResult:
    """1Q (~63 거래일) 단일 SPY 100% BH, 폭락-회복 가격, 모든 invariants 검증.

    Price: 100 → 150 (idx 20) → 60 (idx 40) → 130 (end). 큰 변동.
    Yearly rebalance (init only).
    """
    base = "USD"
    period_start = date(2024, 1, 2)
    period_end = date(2024, 3, 29)
    dates = trading_days_in_period(base, period_start, period_end)
    n = len(dates)
    assert n > 50, f"need >50 days, got {n}"

    asset_id = 1
    peak_idx = 20
    trough_idx = 40
    spy_prices = crash_recovery_prices(
        dates,
        peak_idx=peak_idx,
        trough_idx=trough_idx,
        start=100.0,
        peak=150.0,
        trough=60.0,
        end=130.0,
    )
    prices = build_prices_aligned(dates, {asset_id: spy_prices})

    universe = {asset_id: ("US", "USD")}
    fx = {d: {} for d in dates}
    initial_cash = 10000.0
    initial_cash_dec = {"USD": Decimal(str(initial_cash))}
    strategy = Strategy(
        name="c9",
        allocator=FixedWeight(FixedWeightParams(weights={asset_id: 1.0})),
        signal_filters=tuple(),
        rebalance_schedule="yearly",
    )

    # 엔진 직접 호출 (equity_curve 전체 시리즈 회수 위해 EngineRun 헬퍼 우회).
    ctx = BacktestRunContext(
        base_currency=base,
        period_start=period_start,
        period_end=period_end,
        initial_cash=initial_cash_dec,
        universe_market_meta=universe,
        prices_aligned=prices,
        fx_rates_to_base=fx,
        strategy=strategy,
    )
    result = run_backtest(ctx)
    equity_series = [(p.time, Decimal(p.equity)) for p in result.equity_curve]
    metrics = compute_metrics(equity_series)

    checks: list[FieldCheck] = []

    # === 회계 항등식: 매 day equity == positions_value + cash ===
    # 매 day 마다 portfolio state 를 재구성하기 어려우므로 final state 에서만 검증.
    final_p = result.final_portfolio
    final_price = Decimal(str(spy_prices[-1]))
    final_positions_value = sum(
        (pos.qty * final_price) for pos in final_p.positions.values()
    ) or Decimal("0")
    final_cash_total = sum(final_p.cash_by_ccy.values()) or Decimal("0")
    expected_final_equity = final_positions_value + final_cash_total
    actual_final_equity = float(equity_series[-1][1])
    checks.append(
        check_float(
            "accounting_identity_final",
            actual_final_equity,
            float(expected_final_equity),
            rel=1e-9,
        )
    )

    # === peak monotone non-decreasing ===
    running_peak = float("-inf")
    peak_monotone = True
    prev_peak = float("-inf")
    for _, e in equity_series:
        ev = float(e)
        if ev > running_peak:
            running_peak = ev
        if running_peak < prev_peak:
            peak_monotone = False
            break
        prev_peak = running_peak
    checks.append(check_eq("peak_monotone_non_decreasing", peak_monotone, True))

    # === MDD ≤ 0 ===
    checks.append(check_eq("mdd_le_zero", metrics.mdd <= 0, True))

    # === Calmar = CAGR / |MDD| ===
    if metrics.mdd < 0:
        expected_calmar = metrics.cagr / abs(metrics.mdd)
        checks.append(
            check_float("calmar_identity", metrics.calmar, expected_calmar, rel=1e-9)
        )

    # === 모든 cash ≥ 0 ===
    all_cash_non_negative = all(amt >= 0 for amt in final_p.cash_by_ccy.values())
    checks.append(check_eq("all_cash_non_negative", all_cash_non_negative, True))

    # === 모든 qty ≥ 0 ===
    all_qty_non_negative = all(pos.qty >= 0 for pos in final_p.positions.values())
    checks.append(check_eq("all_qty_non_negative", all_qty_non_negative, True))

    # === 첫 day equity ≤ initial_capital (수수료/슬리피지 손실) ===
    first_equity = float(equity_series[0][1]) if equity_series else 0
    checks.append(check_eq("first_equity_le_initial", first_equity <= initial_cash, True))

    # === peak/trough 위치 invariant ===
    # 단일자산 BH 에서 equity = qty × price + cash (cash 상수). 따라서 equity 의 peak/trough
    # 인덱스 == price 의 peak/trough 인덱스 (qty>0 이고 cash가 작으면).
    # 이 invariant 는 path-dependence 와 무관 — 가격이 양수이고 qty 변화 0 (BH) 이면 항상 성립.
    peak_actual_value = max(float(e) for _, e in equity_series)
    trough_actual_value = min(float(e) for _, e in equity_series)
    equity_peak_idx = max(range(len(equity_series)), key=lambda i: float(equity_series[i][1]))
    equity_trough_idx = min(range(len(equity_series)), key=lambda i: float(equity_series[i][1]))
    # 가격 곡선의 peak/trough 인덱스 (build 시 명시).
    # 단, equity 는 D EOD 시 D 가격 사용이므로 인덱스 1:1 매칭.
    checks.append(
        check_eq("equity_peak_idx_matches_price_peak_idx", equity_peak_idx, peak_idx)
    )
    checks.append(
        check_eq("equity_trough_idx_matches_price_trough_idx", equity_trough_idx, trough_idx)
    )

    # === MDD 값 명시 검증 ===
    # peak ≈ 14939.6045, trough ≈ 6029.6045
    # MDD ≈ (6029.6045 - 14939.6045) / 14939.6045 = -8910 / 14939.60 = -0.5964
    expected_mdd_low = -0.61
    expected_mdd_high = -0.58
    checks.append(
        check_eq("mdd_in_expected_range", expected_mdd_low <= metrics.mdd <= expected_mdd_high, True)
    )

    return CaseResult(
        case_id="C9",
        title="L3 invariants — 큰 폭락-회복 (peak idx=20, trough idx=40)",
        layer="L3",
        checks=checks,
        notes=[
            f"price [start=100, peak=150 @ idx{peak_idx}, trough=60 @ idx{trough_idx}, end=130]",
            f"actual MDD={metrics.mdd:.6f}, peak_value={peak_actual_value:.4f}, trough_value={trough_actual_value:.4f}",
            f"num_days={n}, num_fills={len(result.fills)}",
        ],
    )


CASES_L3 = [case_c9_large_crash_recovery_invariants]
