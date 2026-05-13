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
    """5-day 60/40 monthly rebalance — Jan 29 ~ Feb 2 (Jan-Feb 경계 2회 시그널).

    NYSE 거래일 5개: Jan 29 Mon, 30 Tue, 31 Wed, Feb 1 Thu, Feb 2 Fri.
    가격:
        SPY: Day 0,1 = 100 / Day 2,3,4 = 110 (Jan 31 부터 +10%)
        TLT: 평탄 100

    TASK-244 큐잉 패턴 (D 시그널 → D+1 settlement, D EOD = pre-체결):
        Day 0 (Jan 29): pending=None → settlement skip. EOD = pure cash 10000.
            init signal 발생 (prev_d=None) → target_weights={SPY:0.6,TLT:0.4} 큐잉.
        Day 1 (Jan 30): pending=Jan 29 시그널 → Day 1 가격 (100/100) 으로 settlement.
            equity_at_settle = 10000.
            target_qty_spy = floor(0.6×10000/100) = 60.
            target_qty_tlt = floor(0.4×10000/100) = 40.
            BUY SPY 60 @ 100: gross=100.1×60=6006, comm=0.3003, cost=6006.3003.
                cash: 10000 → 3993.6997.
            BUY TLT 40 @ 100: cost_per_unit=100.105005. max_aff=floor(3993.6997
                /100.105005)=floor(39.8951)=39. actual=min(40,39)=39.
                gross=100.1×39=3903.9, comm=0.195195, cost=3904.095195.
                cash: 3993.6997 → 89.604505.
            EOD Day 1 (가격 100/100): 60×100 + 39×100 + 89.604505 = 9989.604505.
            month 동일 (Jan→Jan) → 시그널 큐잉 없음. pending=None.
        Day 2 (Jan 31): pending=None → settlement skip. EOD (110/100): 60×110 + 39×100
            + 89.604505 = 10589.604505. month 동일 (Jan) → 시그널 없음.
        Day 3 (Feb 1): pending=None → settlement skip. EOD (110/100) = 10589.604505
            (Day 2 와 동일, 가격 동일 + portfolio 동일).
            month 변경 (Jan→Feb) → 시그널 발생.
            allocator 는 D 종가 prices_until_d 만 사용 (FixedWeight 는 가격 무관, 비중
            그대로 반환). target_weights={SPY:0.6,TLT:0.4} 큐잉.
        Day 4 (Feb 2): pending=Feb 1 시그널 → Day 4 가격 (110/100) 으로 settlement.
            equity_at_settle = 10589.604505.
            target_qty_spy = floor(0.6×10589.604505/110) = floor(57.7615) = 57.
            target_qty_tlt = floor(0.4×10589.604505/100) = floor(42.3584) = 42.
            SELL SPY 3 @ 110: effective=110×0.999=109.89. gross=109.89×3=329.67.
                comm=329.67×0.00005=0.0164835. net=329.6535165.
                cash: 89.604505 → 419.2580215. spy: 60→57.
            BUY TLT 3 @ 100: cost_per_unit=100.105005. max_aff=floor(419.2580215
                /100.105005)=floor(4.18820)=4. actual=min(3,4)=3.
                gross=100.1×3=300.3, comm=300.3×0.00005=0.015015, cost=300.315015.
                cash: 419.2580215 → 118.9430065. tlt: 39→42.
            EOD Day 4 (가격 110/100): 57×110 + 42×100 + 118.9430065 = 10588.9430065.
            month 동일 (Feb) → 시그널 없음. (마지막 timeline 이라도 무관 — 큐잉 안 됨.)

    Final state: spy=57, tlt=42, cash=118.9430065, equity=10588.9430065.
    num_fills = 4 (init buy spy + init buy tlt + 리밸런 sell spy + 리밸런 buy tlt).
    equity_curve = [10000.0000, 9989.6045, 10589.6045, 10589.6045, 10588.9430]
    peak = 10589.604505 (Day 2 / Day 3 tie, running max).
    MDD: Day 1 dd = (9989.6045 - 10000)/10000 = -0.001039550 (가장 큰 낙폭).
         Day 4 dd = (10588.9430 - 10589.6045)/10589.6045 ≈ -6.2052e-5 (작음).
    → MDD = -0.0010395495 (Day 0 → Day 1, 매수 1회 수수료/슬립 손실).
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

    # Hand-computed expected (TASK-244 큐잉 패턴 — 위 docstring trace 결과).
    EXPECTED_QTY_SPY = 57.0
    EXPECTED_QTY_TLT = 42.0
    EXPECTED_CASH = 118.9430065
    EXPECTED_FINAL_EQUITY = 10588.9430065
    EXPECTED_INITIAL_EQUITY = 10000.0  # Day 0 = pure cash
    EXPECTED_DAY1_EQUITY = 9989.604505
    EXPECTED_NUM_FILLS = 4
    EXPECTED_PEAK = 10589.604505
    # 가장 큰 dd 는 Day 0(10000) → Day 1(9989.6045) 매수 직후 수수료/슬립 손실.
    EXPECTED_MDD = (EXPECTED_DAY1_EQUITY - EXPECTED_INITIAL_EQUITY) / EXPECTED_INITIAL_EQUITY

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
            check_float("initial_equity", run.initial_equity, EXPECTED_INITIAL_EQUITY, rel=1e-7),
            check_float("peak_equity", run.peak_equity, EXPECTED_PEAK, rel=1e-7),
            check_float("mdd", run.mdd, EXPECTED_MDD, rel=1e-4),
            check_eq("num_equity_points", run.num_equity_points, 5),
        ],
        notes=[
            "수동 계산: docstring trace 참조 (TASK-244 큐잉 패턴)",
            "기대 equity_curve = [10000.0000, 9989.6045, 10589.6045, 10589.6045, 10588.9430]",
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

    TASK-244 큐잉 패턴:
        Day 0: pure cash 10000 (init signal 큐잉만, settlement X).
        Day 1: settlement at p[1]=100 → qty=99, cost=9910.3955, cash=89.6045.
               EOD prices (P=100): 99×100 + 89.6045 = 9989.6045.
        Day 2 (P=120): no rebalance. EOD = 99×120 + 89.6045 = 11969.6045  ← peak
        Day 3 (P=80):  no rebalance. EOD = 99×80  + 89.6045 = 8009.6045   ← trough
        Day 4 (P=90):  no rebalance. EOD = 99×90  + 89.6045 = 8999.6045
    MDD = (8009.6045 - 11969.6045) / 11969.6045 = -0.330874.
    equity_curve = [10000, 9989.6045, 11969.6045, 8009.6045, 8999.6045].
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
