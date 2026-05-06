"""Layer 2 — 손계산 박제 케이스.

오라클 = pen+paper 로 풀어 코드에 literal 상수로 박제. 엔진 로직 import 안 함.

C6: 60/40 monthly rebalance 5-day (path-dependent — Jan-Feb 경계로 2회 rebalance)
C7: MDD 합성 equity 시리즈 직접 compute_metrics (엔진 미경유)
C8: 폭락-회복 단일자산 (peak/trough 명확)
"""

from __future__ import annotations

from datetime import date, timedelta
from decimal import Decimal

from app.domain.allocators import FixedWeight, FixedWeightParams
from app.domain.calendar import trading_days_in_period
from app.domain.metrics import compute_metrics
from app.domain.strategy import Strategy

from scripts.validation._helpers import (
    CaseResult,
    build_prices_aligned,
    check_eq,
    check_float,
    flat_prices,
    run_engine_case,
)


# ============================================================================
# C6 — 60/40 monthly rebalance 5-day mini (path-dependent, hand-computed)
# ============================================================================


def case_c6_sixty_forty_monthly_mini() -> CaseResult:
    """5-day 60/40 monthly rebalance — Jan 29 ~ Feb 2 (Jan-Feb 경계 2회 rebalance).

    NYSE 거래일 5개: Jan 29 Mon, 30 Tue, 31 Wed, Feb 1 Thu, Feb 2 Fri.
    가격:
        SPY: Day 0,1 = 100 / Day 2,3,4 = 110 (Jan 31 부터 +10%)
        TLT: 평탄 100

    Hand-trace (slip=0.10%, US comm=0.005%):
        Day 0 = Jan 29: rebalance fires (init). settlement = Jan 30. SPY=100, TLT=100.
            equity_at_settle = 10000 (no positions).
            target_qty_spy = floor(0.6 × 10000 / 100) = 60.
            target_qty_tlt = floor(0.4 × 10000 / 100) = 40.
            BUY SPY 60: gross = 100.1 × 60 = 6006. comm = 0.3003. cost = 6006.3003.
                cash = 10000 - 6006.3003 = 3993.6997.
            BUY TLT 40: cost_per_unit = 100.105005. max_aff = floor(3993.6997 / 100.105005)
                = floor(39.8951...) = 39. actual = min(40, 39) = 39.
                gross = 100.1 × 39 = 3903.9. comm = 0.19520. cost = 3904.0952.
                cash = 89.6045.
            EOD equity (Day 0 prices 100/100): 60×100 + 39×100 + 89.6045 = 9989.6045.
        Day 1 (Jan 30): no rebalance. EOD prices (100/100). equity = 9989.6045.
        Day 2 (Jan 31): no rebalance. EOD prices (110/100). equity = 60×110 + 39×100 + 89.6045
                                                                  = 10589.6045.
        Day 3 (Feb 1): rebalance fires (month change). settlement = Feb 2 (Day 4).
            settlement prices (110/100). equity_at_settle = 10589.6045.
            target_qty_spy = floor(0.6 × 10589.6045 / 110) = floor(57.7615...) = 57.
            target_qty_tlt = floor(0.4 × 10589.6045 / 100) = floor(42.3584...) = 42.
            sells: spy 60→57 = sell 3. buys: tlt 39→42 = buy 3.
            SELL SPY 3 @ 110: effective = 110 × 0.999 = 109.89. gross = 329.67.
                comm = 0.0164835. net = 329.6535165. cash = 89.6045 + 329.6535165
                = 419.2580165.
                spy pos: 60→57.
            BUY TLT 3 @ 100: cost_per_unit = 100.105005. max_aff = floor(419.2580165
                / 100.105005) = floor(4.18820...) = 4. actual = min(3, 4) = 3.
                gross = 100.1 × 3 = 300.3. comm = 0.01502. cost = 300.31502.
                cash = 419.2580165 - 300.31502 = 118.9429965.
                tlt pos: 39→42.
            EOD equity (Day 3 prices 110/100): 57×110 + 42×100 + 118.9430 = 10588.9430.
        Day 4 (Feb 2): no rebalance. EOD prices (110/100). equity = 10588.9430.

    Final state: spy=57, tlt=42, cash=118.9430, equity=10588.9430.
    num_fills = 4 (init buy spy + init buy tlt + rebalance sell spy + rebalance buy tlt).
    equity_curve = [9989.6045, 9989.6045, 10589.6045, 10588.9430, 10588.9430]
    peak = 10589.6045 (Day 2). MDD = (10588.9430 - 10589.6045) / 10589.6045 = -6.2052e-5.
    """
    base = "USD"
    period_start = date(2024, 1, 29)
    period_end = date(2024, 2, 2)
    dates = trading_days_in_period(base, period_start, period_end)
    assert len(dates) == 5, f"expected 5 NYSE days, got {len(dates)}: {dates}"

    spy_id, tlt_id = 1, 2
    spy_prices = [100.0, 100.0, 110.0, 110.0, 110.0]
    tlt_prices = [100.0, 100.0, 100.0, 100.0, 100.0]
    prices = build_prices_aligned(dates, {spy_id: spy_prices, tlt_id: tlt_prices})

    universe = {spy_id: ("US", "USD"), tlt_id: ("US", "USD")}
    fx = {d: {} for d in dates}
    initial_cash = {"USD": Decimal("10000")}
    strategy = Strategy(
        name="c6",
        allocator=FixedWeight(
            FixedWeightParams(weights={spy_id: 0.6, tlt_id: 0.4})
        ),
        signal_filters=tuple(),
        rebalance_schedule="monthly",
    )

    run = run_engine_case(
        base, period_start, period_end, initial_cash, universe, prices, fx, strategy
    )

    # Hand-computed expected (위 docstring 의 trace 결과).
    EXPECTED_QTY_SPY = 57.0
    EXPECTED_QTY_TLT = 42.0
    EXPECTED_CASH = 118.94299650
    EXPECTED_FINAL_EQUITY = 10588.94299650
    EXPECTED_NUM_FILLS = 4
    EXPECTED_PEAK = 10589.6045
    EXPECTED_MDD = (10588.94299650 - 10589.6045) / 10589.6045

    return CaseResult(
        case_id="C6",
        title="60/40 monthly 5-day Jan-Feb 경계 (path-dependent)",
        layer="L2",
        checks=[
            check_eq("num_fills", run.num_fills, EXPECTED_NUM_FILLS),
            check_float("qty_spy_final", run.final_qty_by_asset.get(spy_id, 0), EXPECTED_QTY_SPY),
            check_float("qty_tlt_final", run.final_qty_by_asset.get(tlt_id, 0), EXPECTED_QTY_TLT),
            check_float("cash_USD_final", run.final_cash_by_ccy.get("USD", 0), EXPECTED_CASH, rel=1e-7),
            check_float("final_equity", run.final_equity, EXPECTED_FINAL_EQUITY, rel=1e-7),
            check_float("peak_equity", run.peak_equity, EXPECTED_PEAK, rel=1e-7),
            check_float("mdd", run.mdd, EXPECTED_MDD, rel=1e-4),
            check_eq("num_equity_points", run.num_equity_points, 5),
        ],
        notes=[
            "수동 계산: docstring trace 참조",
            f"기대 equity_curve = [9989.6045, 9989.6045, 10589.6045, 10588.9430, 10588.9430]",
        ],
    )


# ============================================================================
# C7 — MDD 합성 equity 시리즈 직접 compute_metrics (엔진 미경유)
# ============================================================================


def case_c7_mdd_synthetic_series() -> CaseResult:
    """compute_metrics 의 MDD/peak 계산 직접 검증 — 엔진 호출 없음.

    equity = [100, 110, 120, 100, 80, 90, 110]
    - Day 0: peak so far = 100, dd = 0
    - Day 1: peak = 110, dd = 0
    - Day 2: peak = 120, dd = 0
    - Day 3: peak = 120, dd = (100-120)/120 = -0.16667
    - Day 4: peak = 120, dd = (80-120)/120 = -0.33333  ← MDD
    - Day 5: peak = 120, dd = (90-120)/120 = -0.25
    - Day 6: peak = 120, dd = (110-120)/120 = -0.08333

    MDD = -1/3 ≈ -0.333333.
    win_rate: returns = [+10%, +9.09%, -16.67%, -20%, +12.5%, +22.22%]
              positive = 4 (idx 0,1,4,5), total = 6 → 0.6667
    """
    dates = [date(2024, 1, 1) + timedelta(days=i) for i in range(7)]
    equity_series = [
        (dates[0], Decimal("100")),
        (dates[1], Decimal("110")),
        (dates[2], Decimal("120")),
        (dates[3], Decimal("100")),
        (dates[4], Decimal("80")),
        (dates[5], Decimal("90")),
        (dates[6], Decimal("110")),
    ]
    metrics = compute_metrics(equity_series)

    EXPECTED_MDD = -1.0 / 3.0  # -0.333333...
    EXPECTED_WIN_RATE = 4.0 / 6.0  # 0.6667 (4 positive returns: idx 0,1,4,5)

    # CAGR: 110/100 = 1.10. 6일 = 6/365.25 년.
    expected_cagr = (110.0 / 100.0) ** (365.25 / 6.0) - 1.0

    return CaseResult(
        case_id="C7",
        title="compute_metrics 직접: MDD 합성 시리즈 [100,110,120,100,80,90,110]",
        layer="L2",
        checks=[
            check_float("mdd", metrics.mdd, EXPECTED_MDD, rel=1e-9),
            check_float("win_rate", metrics.win_rate, EXPECTED_WIN_RATE, rel=1e-9),
            check_float("cagr", metrics.cagr, expected_cagr, rel=1e-9),
        ],
        notes=[
            "엔진 미경유 (compute_metrics 만)",
            f"hand-MDD = (80-120)/120 = -0.333333",
        ],
    )


# ============================================================================
# C8 — 폭락-회복 단일자산 (peak/trough 명확)
# ============================================================================


def case_c8_crash_recovery_single() -> CaseResult:
    """5-day 단일 SPY 100% BH, 가격 [100,100,120,80,90], yearly rebalance.

    Init buy Day 1 @ 100: qty=99, cost=9910.395, cash=89.6045.
    EOD equity:
        Day 0 (P=100): 99×100 + 89.60 = 9989.60
        Day 1 (P=100): 9989.60
        Day 2 (P=120): 99×120 + 89.60 = 12009.60  ← peak
        Day 3 (P=80):  99×80  + 89.60 = 8009.60   ← trough
        Day 4 (P=90):  99×90  + 89.60 = 8999.60
    MDD = (8009.60 - 12009.60) / 12009.60 = -4000 / 12009.60 = -0.333055.
    """
    base = "USD"
    period_start = date(2024, 1, 2)
    period_end = date(2024, 1, 8)
    dates = trading_days_in_period(base, period_start, period_end)
    assert len(dates) == 5, f"expected 5 NYSE days, got {len(dates)}: {dates}"

    asset_id = 1
    spy_prices = [100.0, 100.0, 120.0, 80.0, 90.0]
    prices = build_prices_aligned(dates, {asset_id: spy_prices})

    universe = {asset_id: ("US", "USD")}
    fx = {d: {} for d in dates}
    initial_cash = {"USD": Decimal("10000")}
    strategy = Strategy(
        name="c8",
        allocator=FixedWeight(FixedWeightParams(weights={asset_id: 1.0})),
        signal_filters=tuple(),
        rebalance_schedule="yearly",
    )

    run = run_engine_case(
        base, period_start, period_end, initial_cash, universe, prices, fx, strategy
    )

    # Hand-computed.
    EXPECTED_QTY = 99.0
    EXPECTED_CASH = 89.604505
    EXPECTED_PEAK = 99 * 120 + 89.604505  # 12009.604505
    EXPECTED_TROUGH = 99 * 80 + 89.604505  # 8009.604505
    EXPECTED_FINAL = 99 * 90 + 89.604505   # 8999.604505
    EXPECTED_MDD = (EXPECTED_TROUGH - EXPECTED_PEAK) / EXPECTED_PEAK

    return CaseResult(
        case_id="C8",
        title="폭락-회복 단일 SPY 5-day (peak/trough 명확)",
        layer="L2",
        checks=[
            check_eq("num_fills", run.num_fills, 1),
            check_float("qty_spy", run.final_qty_by_asset.get(asset_id, 0), EXPECTED_QTY),
            check_float("cash_USD", run.final_cash_by_ccy.get("USD", 0), EXPECTED_CASH, rel=1e-7),
            check_float("final_equity", run.final_equity, EXPECTED_FINAL, rel=1e-7),
            check_float("peak_equity", run.peak_equity, EXPECTED_PEAK, rel=1e-7),
            check_float("trough_after_peak", run.trough_after_peak, EXPECTED_TROUGH, rel=1e-7),
            check_float("mdd", run.mdd, EXPECTED_MDD, rel=1e-7),
        ],
        notes=[
            f"prices = {spy_prices}",
            f"peak={EXPECTED_PEAK:.4f}, trough={EXPECTED_TROUGH:.4f}, MDD={EXPECTED_MDD:.6f}",
        ],
    )


CASES_L2 = [
    case_c6_sixty_forty_monthly_mini,
    case_c7_mdd_synthetic_series,
    case_c8_crash_recovery_single,
]
