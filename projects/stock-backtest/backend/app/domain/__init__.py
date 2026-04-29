"""Domain 레이어 — 순수 엔티티 + Repository Protocol.

외부 의존(SQLAlchemy/HTTP/UI 프레임워크) 금지. 단 exchange_calendars 는 도메인 정책에
본질적이므로 예외 (architecture.md V3 § "비거래일 방어" 가 도메인 결정).
"""
from app.domain.asset import (
    Asset,
    AssetRepository,
    AssetType,
    GuardMode,
    Market,
    Universe,
    guard_trading_day,
    is_trading_day,
)
from app.domain.calendar import (
    BASE_CCY_TO_CALENDAR,
    align_market_price_to_base_calendar,
    align_universe_prices,
    base_calendar_name,
    next_trading_day,
    previous_trading_day,
    trading_days_in_period,
)
from app.domain.portfolio import (
    DEFAULT_FX_SPREAD_BPS,
    DEFAULT_SLIPPAGE_BPS,
    FxConversion,
    InsufficientFundsError,
    Portfolio,
    Position,
)
from app.domain.trade import (
    DEFAULT_COMMISSION_BPS,
    DEFAULT_SLIPPAGE_BPS_DEFAULT,
    MissingPriceError,
    NonTradingDayError,
    TradeFill,
    TradeOrder,
    assert_all_assets_priced,
    assert_trading_day_for_universe,
    commission_bps_for,
    execute_rebalance,
)
from app.domain.strategy import (
    Allocator,
    RebalanceSchedule,
    SignalFilter,
    Strategy,
    apply_filters_and_allocator,
)
from app.domain.engine import (
    BacktestEquityPoint,
    BacktestRunContext,
    BacktestRunResult,
    run_backtest,
)
from app.domain.dividend import (
    DividendCredit,
    DividendPayment,
    apply_dividend,
    apply_dividends_for_date,
)
from app.domain.metrics import (
    TRADING_DAYS_PER_YEAR,
    MetricsResult,
    compute_metrics,
)
from app.domain.tax import (
    DividendIncome,
    NoTaxPlugin,
    RealizedTrade,
    TaxPlugin,
    TaxResult,
    apply_tax_to_portfolio,
)

__all__ = [
    "Asset",
    "AssetRepository",
    "AssetType",
    "GuardMode",
    "Market",
    "Universe",
    "guard_trading_day",
    "is_trading_day",
    "BASE_CCY_TO_CALENDAR",
    "align_market_price_to_base_calendar",
    "align_universe_prices",
    "base_calendar_name",
    "next_trading_day",
    "previous_trading_day",
    "trading_days_in_period",
    "DEFAULT_FX_SPREAD_BPS",
    "DEFAULT_SLIPPAGE_BPS",
    "FxConversion",
    "InsufficientFundsError",
    "Portfolio",
    "Position",
    "DEFAULT_COMMISSION_BPS",
    "DEFAULT_SLIPPAGE_BPS_DEFAULT",
    "MissingPriceError",
    "NonTradingDayError",
    "TradeFill",
    "TradeOrder",
    "assert_all_assets_priced",
    "assert_trading_day_for_universe",
    "commission_bps_for",
    "execute_rebalance",
    "Allocator",
    "RebalanceSchedule",
    "SignalFilter",
    "Strategy",
    "apply_filters_and_allocator",
    "BacktestEquityPoint",
    "BacktestRunContext",
    "BacktestRunResult",
    "run_backtest",
    "DividendCredit",
    "DividendPayment",
    "apply_dividend",
    "apply_dividends_for_date",
    "TRADING_DAYS_PER_YEAR",
    "MetricsResult",
    "compute_metrics",
    "DividendIncome",
    "NoTaxPlugin",
    "RealizedTrade",
    "TaxPlugin",
    "TaxResult",
    "apply_tax_to_portfolio",
]
