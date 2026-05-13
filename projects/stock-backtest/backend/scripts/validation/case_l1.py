"""Layer 1 — 닫힌식 오라클 (시뮬 0줄, 한 줄 수식).

각 케이스는 yearly rebalance 로 초기 1회 buy 만 발생 (period < 1년) → 결과는
초기 qty/cash 닫힌식 + price[end] 만으로 계산 가능.

엔진 독립성: 오라클은 float 산술 + math.floor 한 줄 수식. 엔진은 Decimal + pandas
+ 일별 루프. 알고리즘 패러다임이 다르므로 같은 버그 동시 침투 가능성 매우 낮음.
"""

from __future__ import annotations

from datetime import date
from decimal import Decimal

from app.domain.allocators import (
    AllWeather,
    AllWeatherParams,
    EqualWeight,
    EqualWeightParams,
    FixedWeight,
    FixedWeightParams,
)
from app.domain.calendar import trading_days_in_period
from app.domain.strategy import Strategy

from scripts.validation._helpers import (
    CaseResult,
    build_fx_constant,
    build_prices_aligned,
    check_eq,
    check_float,
    closed_form_initial_buy,
    flat_prices,
    linear_prices,
    run_engine_case,
)


# 시장별 수수료 bps (engine 디폴트 trade.DEFAULT_COMMISSION_BPS)
COMM_KR = 1.5
COMM_US = 0.5
COMM_CRYPTO = 10.0
SLIP = 10.0  # DEFAULT_SLIPPAGE_BPS


def _initial_equity(cash: dict[str, float], base: str, fx: dict[str, float]) -> float:
    """모든 통화 cash → base 환산 합."""
    total = 0.0
    for ccy, amt in cash.items():
        if ccy == base:
            total += amt
        else:
            total += amt * fx[ccy]
    return total


# ============================================================================
# C1 — 단일자산 BH USD base (SPY 평탄가)
# ============================================================================


def case_c1_spy_bh_flat() -> CaseResult:
    """SPY 100% BH, USD base, 평탄가 100, yearly rebalance.

    EOD equity 회계 (TASK-244 큐잉 패턴):
        Day 0 EOD = pure cash (시그널만 큐잉, 체결 X) = initial_cash = 10000.
        Day 1 EOD = settlement 직후 (Day 1 가격) = qty × 100 + cash_after.
        평탄가이므로 Day 1~N EOD 모두 동일.

    오라클 (한 줄 수식):
        qty = floor(10000 / (100 × 1.001 × 1.00005))
        cash_after = 10000 - qty × 100 × 1.001 × (1 + 0.00005)
        equity[end] = qty × 100 + cash_after  (price 평탄)
        equity[Day 0] = 10000 (pure cash)
        MDD = (post-trade equity − 10000) / 10000  (수수료/슬리피지 손실 1회)
    """
    base = "USD"
    period_start = date(2024, 1, 2)
    period_end = date(2024, 3, 29)  # 1Q
    dates = trading_days_in_period(base, period_start, period_end)

    asset_id = 1
    flat_p = 100.0
    prices = build_prices_aligned(dates, {asset_id: flat_prices(dates, flat_p)})

    universe = {asset_id: ("US", "USD")}
    fx = {d: {} for d in dates}  # base=USD, 환전 없음
    initial_cash = {"USD": Decimal("10000")}
    strategy = Strategy(
        name="c1",
        allocator=FixedWeight(FixedWeightParams(weights={asset_id: 1.0})),
        signal_filters=tuple(),
        rebalance_schedule="yearly",
    )

    run = run_engine_case(
        base, period_start, period_end, initial_cash, universe, prices, fx, strategy
    )

    # 오라클: Day 0 시그널 → Day 1 settlement 가격=100 (평탄).
    qty, _, cash_after = closed_form_initial_buy(
        available_cash_native=10000.0,
        target_value_native=10000.0,
        price_at_settlement=flat_p,
        commission_bps=COMM_US,
        slippage_bps=SLIP,
        fractional=False,
    )
    expected_final_equity = qty * flat_p + cash_after
    expected_initial_equity = 10000.0  # Day 0 EOD = pure cash

    expected_peak = 10000.0  # Day 0 EOD (pure cash) > Day 1+ post-trade
    expected_mdd = (expected_final_equity - expected_peak) / expected_peak

    return CaseResult(
        case_id="C1",
        title="SPY BH USD 평탄가 (yearly)",
        layer="L1",
        checks=[
            check_eq("num_fills", run.num_fills, 1),
            check_float("final_qty", run.final_qty_by_asset.get(asset_id, 0), qty),
            check_float("cash_after_buy_USD", run.final_cash_by_ccy.get("USD", 0), cash_after, rel=1e-7),
            check_float("final_equity", run.final_equity, expected_final_equity, rel=1e-6),
            check_float("initial_equity", run.initial_equity, expected_initial_equity, rel=1e-6),
            check_float("mdd", run.mdd, expected_mdd, rel=1e-6),
            check_float("peak_equity", run.peak_equity, expected_peak, rel=1e-6),
        ],
        notes=[f"qty={qty}", f"cash_after={cash_after:.4f}", f"equity={expected_final_equity:.4f}"],
    )


# ============================================================================
# C2 — KODEX BH KRW base (KR 수수료)
# ============================================================================


def case_c2_kodex_bh_linear() -> CaseResult:
    """KODEX 200 100% BH, KRW base, 선형 +20% 가격 (35000 → 42000), yearly.

    오라클: settlement price = price[D_1] = 선형 보간 1번째 인덱스.
    """
    base = "KRW"
    period_start = date(2024, 1, 2)
    period_end = date(2024, 3, 29)
    dates = trading_days_in_period(base, period_start, period_end)

    asset_id = 1
    p_start = 35000.0
    p_end = 42000.0
    prices_list = linear_prices(dates, p_start, p_end)
    prices = build_prices_aligned(dates, {asset_id: prices_list})

    universe = {asset_id: ("KR", "KRW")}
    fx = {d: {} for d in dates}
    initial_cash = {"KRW": Decimal("10000000")}  # 1천만원
    strategy = Strategy(
        name="c2",
        allocator=FixedWeight(FixedWeightParams(weights={asset_id: 1.0})),
        signal_filters=tuple(),
        rebalance_schedule="yearly",
    )

    run = run_engine_case(
        base, period_start, period_end, initial_cash, universe, prices, fx, strategy
    )

    # 오라클 (TASK-244 큐잉 패턴):
    #   Day 0 EOD = pure cash 10_000_000 (시그널만 큐잉).
    #   Day 1 EOD = settlement 가격 p[1] = 35000 + (42000-35000)/(N-1).
    #   Day k≥1 EOD = qty × p[k] + cash_after (선형 단조증가).
    p_settle = prices_list[1]
    qty, _, cash_after = closed_form_initial_buy(
        available_cash_native=10_000_000.0,
        target_value_native=10_000_000.0,
        price_at_settlement=p_settle,
        commission_bps=COMM_KR,
        slippage_bps=SLIP,
        fractional=False,
    )
    p_final = prices_list[-1]
    expected_final_equity = qty * p_final + cash_after
    expected_initial_equity = 10_000_000.0  # Day 0 EOD = pure cash

    # MDD: Day 0 = 10M (pure cash, peak), Day 1 = qty × p[1] + cash_after (수수료/슬리피지
    # 손실로 < 10M = trough). Day k≥1 = qty × p[k] + cash_after 는 p[k] 단조증가라 monotone
    # 증가. 따라서 MDD = (Day 1 equity - 10M) / 10M (음수, ~수수료+슬립 비율).
    expected_day1_equity = qty * prices_list[1] + cash_after
    expected_mdd = (expected_day1_equity - expected_initial_equity) / expected_initial_equity

    return CaseResult(
        case_id="C2",
        title="KODEX BH KRW 선형 +20%",
        layer="L1",
        checks=[
            check_eq("num_fills", run.num_fills, 1),
            check_float("final_qty", run.final_qty_by_asset.get(asset_id, 0), qty),
            check_float("cash_after_buy_KRW", run.final_cash_by_ccy.get("KRW", 0), cash_after, rel=1e-7),
            check_float("final_equity", run.final_equity, expected_final_equity, rel=1e-6),
            check_float("initial_equity", run.initial_equity, expected_initial_equity, rel=1e-6),
            check_float("mdd", run.mdd, expected_mdd, rel=1e-6),
        ],
        notes=[
            f"p_settle(Day 1)={p_settle:.4f}, p_final={p_final:.4f}",
            f"qty={qty}, cash_after={cash_after:.2f}",
            f"day0={expected_initial_equity:.2f}, day1={expected_day1_equity:.2f}",
        ],
    )


# ============================================================================
# C3 — BTC fractional BH USD base (CRYPTO)
# ============================================================================


def case_c3_btc_fractional_bh() -> CaseResult:
    """BTC 100% fractional BH, USD base, 선형 +50% (50000 → 75000), yearly.

    fractional 분기 검증 — qty 가 8자리 소수 (정수 아님).
    """
    base = "USD"
    period_start = date(2024, 1, 2)
    period_end = date(2024, 3, 29)
    dates = trading_days_in_period(base, period_start, period_end)

    asset_id = 4
    p_start = 50000.0
    p_end = 75000.0
    prices_list = linear_prices(dates, p_start, p_end)
    prices = build_prices_aligned(dates, {asset_id: prices_list})

    universe = {asset_id: ("CRYPTO", "USD")}
    fx = {d: {} for d in dates}
    initial_cash = {"USD": Decimal("10000")}
    strategy = Strategy(
        name="c3",
        allocator=FixedWeight(FixedWeightParams(weights={asset_id: 1.0})),
        signal_filters=tuple(),
        rebalance_schedule="yearly",
    )

    run = run_engine_case(
        base, period_start, period_end, initial_cash, universe, prices, fx, strategy
    )

    # 오라클 (TASK-244 큐잉): Day 0 EOD = pure cash 10000, Day 1 EOD = settlement at p[1].
    p_settle = prices_list[1]
    qty, _, cash_after = closed_form_initial_buy(
        available_cash_native=10000.0,
        target_value_native=10000.0,
        price_at_settlement=p_settle,
        commission_bps=COMM_CRYPTO,
        slippage_bps=SLIP,
        fractional=True,
    )
    p_final = prices_list[-1]
    expected_final_equity = qty * p_final + cash_after
    expected_initial_equity = 10000.0  # Day 0 EOD = pure cash

    # MDD: Day 0 = 10000 = peak (수수료/슬립 차감 전).
    # Day 1 = qty × p[1] + cash_after (commission ≈ 0.1% + slip 0.1% ≈ 0.2% 손실).
    # Day k≥1 = qty × p[k] + cash_after (p 단조증가). 따라서 MDD = (Day 1 - Day 0) / Day 0.
    expected_day1_equity = qty * prices_list[1] + cash_after
    expected_mdd = (expected_day1_equity - expected_initial_equity) / expected_initial_equity

    return CaseResult(
        case_id="C3",
        title="BTC fractional BH USD 선형 +50%",
        layer="L1",
        checks=[
            check_eq("num_fills", run.num_fills, 1),
            check_float("final_qty_btc", run.final_qty_by_asset.get(asset_id, 0), qty, rel=1e-9),
            check_float("cash_after_buy_USD", run.final_cash_by_ccy.get("USD", 0), cash_after, rel=1e-7),
            check_float("final_equity", run.final_equity, expected_final_equity, rel=1e-6),
            check_float("initial_equity", run.initial_equity, expected_initial_equity, rel=1e-6),
            check_float("mdd", run.mdd, expected_mdd, rel=1e-6),
        ],
        notes=[
            f"qty={qty} (fractional 8자리)",
            f"p_settle={p_settle:.2f}, p_final={p_final:.2f}",
            f"cash_after={cash_after:.4f}",
        ],
    )


# ============================================================================
# C4 — 60/40 BH USD base 두 자산 (yearly, init only)
# ============================================================================


def case_c4_sixty_forty_bh() -> CaseResult:
    """SPY 60% + TLT 40% BH USD, 평탄가 100/95, yearly.

    오라클: 두 자산 독립 초기 매수 (cash 충분).
    """
    base = "USD"
    period_start = date(2024, 1, 2)
    period_end = date(2024, 3, 29)
    dates = trading_days_in_period(base, period_start, period_end)

    spy_id, tlt_id = 1, 2
    p_spy = 100.0
    p_tlt = 95.0
    prices = build_prices_aligned(
        dates,
        {
            spy_id: flat_prices(dates, p_spy),
            tlt_id: flat_prices(dates, p_tlt),
        },
    )

    universe = {spy_id: ("US", "USD"), tlt_id: ("US", "USD")}
    fx = {d: {} for d in dates}
    initial_cash = {"USD": Decimal("10000")}
    strategy = Strategy(
        name="c4",
        allocator=FixedWeight(
            FixedWeightParams(weights={spy_id: 0.6, tlt_id: 0.4})
        ),
        signal_filters=tuple(),
        rebalance_schedule="yearly",
    )

    run = run_engine_case(
        base, period_start, period_end, initial_cash, universe, prices, fx, strategy
    )

    # 오라클 (TASK-244 큐잉): Day 0 EOD = pure cash 10000, Day 1 EOD = post-init-buy.
    # SPY 먼저 buy (insertion order = target_weights 순서), 그 후 cash 잔량으로 TLT.
    # 평탄가이므로 settlement price = 100 / 95.
    qty_spy, cost_spy, cash_after_spy = closed_form_initial_buy(
        available_cash_native=10000.0,
        target_value_native=10000.0 * 0.6,
        price_at_settlement=p_spy,
        commission_bps=COMM_US,
        slippage_bps=SLIP,
    )
    qty_tlt, cost_tlt, cash_after_tlt = closed_form_initial_buy(
        available_cash_native=cash_after_spy,
        target_value_native=10000.0 * 0.4,
        price_at_settlement=p_tlt,
        commission_bps=COMM_US,
        slippage_bps=SLIP,
    )
    expected_equity = qty_spy * p_spy + qty_tlt * p_tlt + cash_after_tlt
    expected_initial_equity = 10000.0  # Day 0 EOD = pure cash
    # 평탄가 + 1회 매수 → Day 0 = 10000 (peak), Day 1+ = expected_equity (수수료/슬립 손실).
    expected_mdd = (expected_equity - expected_initial_equity) / expected_initial_equity

    return CaseResult(
        case_id="C4",
        title="60/40 BH USD 평탄가 (yearly)",
        layer="L1",
        checks=[
            check_eq("num_fills", run.num_fills, 2),
            check_float("qty_spy", run.final_qty_by_asset.get(spy_id, 0), qty_spy),
            check_float("qty_tlt", run.final_qty_by_asset.get(tlt_id, 0), qty_tlt),
            check_float("cash_after_USD", run.final_cash_by_ccy.get("USD", 0), cash_after_tlt, rel=1e-7),
            check_float("final_equity", run.final_equity, expected_equity, rel=1e-6),
            check_float("initial_equity", run.initial_equity, expected_initial_equity, rel=1e-6),
            check_float("mdd", run.mdd, expected_mdd, rel=1e-6),
        ],
        notes=[
            f"qty_spy={qty_spy}, qty_tlt={qty_tlt}",
            f"cash_after={cash_after_tlt:.4f}, equity={expected_equity:.4f}",
        ],
    )


# ============================================================================
# C5 — AllWeather 5자산 BH USD base (yearly, init only)
# ============================================================================


def case_c5_allweather_bh() -> CaseResult:
    """AllWeather 표준 5자산 (주식30/장기채40/중기채15/금7.5/원자재7.5) BH, yearly.

    엔진은 카테고리당 1자산 매핑이라 effectively FixedWeight 와 동일 (단일자산-카테고리).
    오라클: 5 buy 닫힌식.
    """
    base = "USD"
    period_start = date(2024, 1, 2)
    period_end = date(2024, 3, 29)
    dates = trading_days_in_period(base, period_start, period_end)

    # 자산 5종, 모두 평탄가 (검증 단순화)
    spy_id, tlt_id, ief_id, gld_id, dbc_id = 1, 2, 3, 4, 5
    prices = build_prices_aligned(
        dates,
        {
            spy_id: flat_prices(dates, 400.0),
            tlt_id: flat_prices(dates, 90.0),
            ief_id: flat_prices(dates, 95.0),
            gld_id: flat_prices(dates, 180.0),
            dbc_id: flat_prices(dates, 22.0),
        },
    )
    universe = {
        spy_id: ("US", "USD"),
        tlt_id: ("US", "USD"),
        ief_id: ("US", "USD"),
        gld_id: ("US", "USD"),
        dbc_id: ("US", "USD"),
    }
    fx = {d: {} for d in dates}
    initial_cash = {"USD": Decimal("100000")}

    # AllWeather params: category_weights × asset_categories
    asset_categories = {
        spy_id: "equity",
        tlt_id: "long_bond",
        ief_id: "intermediate_bond",
        gld_id: "gold",
        dbc_id: "commodity",
    }
    category_weights = {
        "equity": 0.30,
        "long_bond": 0.40,
        "intermediate_bond": 0.15,
        "gold": 0.075,
        "commodity": 0.075,
    }
    strategy = Strategy(
        name="c5",
        allocator=AllWeather(
            AllWeatherParams(
                category_weights=category_weights,
                asset_categories=asset_categories,
            )
        ),
        signal_filters=tuple(),
        rebalance_schedule="yearly",
    )

    run = run_engine_case(
        base, period_start, period_end, initial_cash, universe, prices, fx, strategy
    )

    # 오라클: 카테고리당 자산 1개이므로 자산 비중 = 카테고리 비중.
    weights = {
        spy_id: 0.30,
        tlt_id: 0.40,
        ief_id: 0.15,
        gld_id: 0.075,
        dbc_id: 0.075,
    }
    settle_prices = {
        spy_id: 400.0,
        tlt_id: 90.0,
        ief_id: 95.0,
        gld_id: 180.0,
        dbc_id: 22.0,
    }
    cash = 100000.0
    initial_equity = 100000.0
    expected_qty: dict[int, float] = {}
    expected_positions_value = 0.0
    # 자산 처리 순서는 allocator 가 반환한 dict order. AllWeather 는 asset_categories
    # 순회 순서에 의존 — 우리가 dict 를 위에서 정의한 순서대로 들어감.
    for aid in [spy_id, tlt_id, ief_id, gld_id, dbc_id]:
        qty, _, cash = closed_form_initial_buy(
            available_cash_native=cash,
            target_value_native=initial_equity * weights[aid],
            price_at_settlement=settle_prices[aid],
            commission_bps=COMM_US,
            slippage_bps=SLIP,
        )
        expected_qty[aid] = qty
        expected_positions_value += qty * settle_prices[aid]
    expected_equity = expected_positions_value + cash

    expected_initial_equity = 100000.0  # Day 0 EOD = pure cash (TASK-244 큐잉)
    expected_mdd = (expected_equity - expected_initial_equity) / expected_initial_equity

    return CaseResult(
        case_id="C5",
        title="AllWeather 5자산 BH USD (yearly)",
        layer="L1",
        checks=[
            check_eq("num_fills", run.num_fills, 5),
            check_float("qty_spy", run.final_qty_by_asset.get(spy_id, 0), expected_qty[spy_id]),
            check_float("qty_tlt", run.final_qty_by_asset.get(tlt_id, 0), expected_qty[tlt_id]),
            check_float("qty_ief", run.final_qty_by_asset.get(ief_id, 0), expected_qty[ief_id]),
            check_float("qty_gld", run.final_qty_by_asset.get(gld_id, 0), expected_qty[gld_id]),
            check_float("qty_dbc", run.final_qty_by_asset.get(dbc_id, 0), expected_qty[dbc_id]),
            check_float("cash_after_USD", run.final_cash_by_ccy.get("USD", 0), cash, rel=1e-7),
            check_float("final_equity", run.final_equity, expected_equity, rel=1e-6),
            check_float("initial_equity", run.initial_equity, expected_initial_equity, rel=1e-6),
            check_float("mdd", run.mdd, expected_mdd, rel=1e-6),
        ],
        notes=[
            f"qtys={expected_qty}",
            f"cash_after={cash:.2f}",
        ],
    )


CASES_L1 = [
    case_c1_spy_bh_flat,
    case_c2_kodex_bh_linear,
    case_c3_btc_fractional_bh,
    case_c4_sixty_forty_bh,
    case_c5_allweather_bh,
]
