"""Vectorised backtest engine (architecture decisions #3, #5, #6, #7, #13, #14).

This is the top-level orchestration layer that ties together:

- the price repository (:mod:`stock_backtest.data.repository`)
- the trading calendar (:mod:`.calendar` / :mod:`.calendar_guard`)
- the portfolio state (:mod:`.portfolio`)
- the FX converter (:mod:`.fx`)
- the tax policy (:mod:`.tax`)
- the :class:`~stock_backtest.strategies.base.Strategy` interface

It intentionally avoids any DB persistence of run results; that is TASK-018.

Execution model
---------------
1. Resolve the effective run period as the intersection of the config period
   and each asset's available data window.
2. Load adjusted-close prices for every asset into a wide DataFrame
   (``index=date, columns=asset_id``) via :class:`OhlcvRepository`.
3. Build a trading-day axis according to ``market_mode``:
     - ``STOCK``: union of per-asset market sessions, re-validated per asset.
     - ``CRYPTO``: 365-day calendar.
     - ``MIXED``: union of sessions; crypto columns forward-fill into
       non-crypto sessions.
4. Call ``assert_universe_coverage`` to fail loud on any silent gap.
5. Derive rebalance dates from ``rebalance_freq`` (a pandas freq alias) and
   snap each to a valid trading day with ``previous_trading_day``.
6. Call ``strategy.generate_weights(prices, rebalance_dates)``.
7. Iterate trading days: on rebalance dates, compute the trade list from the
   delta between target and current weights; apply trades with commission /
   slippage / FX spread; record tax on realised sells; cross year-end the
   tax policy rolls the state forward.

All monetary math runs on :class:`decimal.Decimal`.
"""

from __future__ import annotations

import datetime as _dt
import logging
from dataclasses import dataclass, field
from decimal import Decimal
from typing import TYPE_CHECKING, Any, Callable, Iterable, Protocol

import pandas as pd

logger = logging.getLogger(__name__)

# Safety margin added on top of the worst-case trading/FX cost, in bps.
# Protects against intra-day price drift between target-qty computation and
# trade execution and against rounding in commission/slippage math.
_SAFETY_BUFFER_BPS = Decimal("10")
# Hard cap on the cushion to avoid pathological configs starving the portfolio
# of investable capital (e.g. 5% reserved as cash cushion).
_MAX_CUSHION_BPS = Decimal("500")

from stock_backtest.backtest.calendar import (
    get_trading_days,
    previous_trading_day,
    union_trading_days,
)
from stock_backtest.backtest.calendar_guard import assert_universe_coverage
from stock_backtest.backtest.fx import FXConverter
from stock_backtest.backtest.portfolio import Portfolio
from stock_backtest.backtest.tax import (
    RealizedTrade,
    TaxYearState,
    build_tax_policy,
)

if TYPE_CHECKING:  # pragma: no cover - typing only
    from sqlalchemy.orm import Session

    from stock_backtest.config import Settings
    from stock_backtest.strategies.base import Strategy


__all__ = [
    "AssetSpec",
    "BacktestConfig",
    "BacktestEngine",
    "BacktestResult",
    "CASH_SYMBOL",
    "TradeRecord",
    "PriceLoader",
]

# Reserved "asset" symbol that represents an uninvested cash slice in the
# base currency. It is a first-class position in the engine but has no
# OHLCV series and produces no BUY/SELL trade records - the remainder of a
# target-weight vector that does not sum to 1.0 naturally materialises as
# the idle ``cash_by_ccy[base_currency]`` balance. See architecture.md
# section "전략 DSL 및 현금 1급 처리".
CASH_SYMBOL = "_CASH_"

ZERO = Decimal("0")
_ONE = Decimal("1")


# ---------------------------------------------------------------------------
# Config / result dataclasses
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class AssetSpec:
    """Per-asset metadata required by the engine.

    The engine is agnostic to how this is sourced; tests construct it directly
    while production callers will build it from the ``assets`` table.
    """

    asset_id: int
    symbol: str
    market: str  # KR / US / CRYPTO
    currency: str  # ISO 4217 code (e.g. USD, KRW)
    asset_class: str  # matches stock_backtest.backtest.tax.AssetClass
    start_date: _dt.date | None = None  # earliest data; engine clips to this
    end_date: _dt.date | None = None  # latest data


@dataclass
class BacktestConfig:
    strategy_name: str
    params: dict[str, Any]
    universe: list[AssetSpec]
    period_start: _dt.date
    period_end: _dt.date
    base_currency: str = "USD"
    market_mode: str = "STOCK"  # STOCK | CRYPTO | MIXED
    initial_capital: Decimal = Decimal("100000")
    rebalance_freq: str = "ME"  # pandas offset alias


@dataclass
class TradeRecord:
    date: _dt.date
    asset_id: int | None
    side: str  # BUY / SELL / FX
    qty: Decimal
    price: Decimal
    currency: str
    commission_bps: Decimal
    slippage_bps: Decimal
    # FX-only fields (populated when side == "FX"). ``asset_id`` is None for
    # FX rows and ``currency`` holds the source currency.
    currency_from: str | None = None
    currency_to: str | None = None
    fx_rate: Decimal | None = None
    spread_bps: Decimal | None = None


@dataclass
class BacktestResult:
    equity_curve: pd.Series
    trades: list[TradeRecord] = field(default_factory=list)
    realized_trades: list[RealizedTrade] = field(default_factory=list)
    tax_paid_by_year: dict[int, Decimal] = field(default_factory=dict)
    run_hash: str | None = None


# ---------------------------------------------------------------------------
# Price loader protocol
# ---------------------------------------------------------------------------


class PriceLoader(Protocol):
    """Callable returning a wide adj_close DataFrame for the universe."""

    def __call__(
        self,
        universe: list[AssetSpec],
        start: _dt.date,
        end: _dt.date,
    ) -> pd.DataFrame:  # pragma: no cover - protocol
        ...


def default_price_loader(session_factory: Callable[[], "Session"]) -> PriceLoader:
    """Build a :class:`PriceLoader` backed by :class:`OhlcvRepository`.

    This helper is the default production path; tests typically inject a
    hand-crafted loader that avoids the DB entirely.
    """

    def _loader(
        universe: list[AssetSpec], start: _dt.date, end: _dt.date
    ) -> pd.DataFrame:
        from stock_backtest.data.repository import OhlcvRepository

        series_by_asset: dict[int, pd.Series] = {}
        with session_factory() as session:  # type: ignore[misc]
            repo = OhlcvRepository(session)
            for spec in universe:
                rows = repo.get_range(spec.asset_id, start, end)
                if not rows:
                    series_by_asset[spec.asset_id] = pd.Series(dtype="float64")
                    continue
                idx = pd.DatetimeIndex(
                    [pd.Timestamp(r.time).tz_localize(None).normalize() for r in rows]
                )
                vals = [
                    r.adj_close if r.adj_close is not None else r.close for r in rows
                ]
                series_by_asset[spec.asset_id] = pd.Series(vals, index=idx).astype(
                    "float64"
                )
        if not series_by_asset:
            return pd.DataFrame()
        df = pd.DataFrame(series_by_asset).sort_index()
        df.columns.name = "asset_id"
        return df

    return _loader


# ---------------------------------------------------------------------------
# Engine
# ---------------------------------------------------------------------------


class BacktestEngine:
    """Main backtest orchestrator.

    Parameters
    ----------
    settings:
        Loaded :class:`~stock_backtest.config.Settings` instance.
    session_factory:
        Zero-arg callable returning a SQLAlchemy ``Session``. Used for the
        default price loader and FX converter. May be ``None`` when both
        ``price_loader`` and ``fx_converter`` are injected.
    price_loader:
        Optional override for price retrieval (tests inject this).
    fx_converter:
        Optional pre-built :class:`FXConverter` (tests inject this).
    """

    def __init__(
        self,
        settings: "Settings",
        session_factory: Callable[[], "Session"] | None = None,
        *,
        price_loader: PriceLoader | None = None,
        fx_converter: FXConverter | None = None,
    ) -> None:
        self.settings = settings
        self._session_factory = session_factory
        self._price_loader = price_loader
        self._fx_converter = fx_converter

    # ------------------------------------------------------------------
    # Public entry
    # ------------------------------------------------------------------
    def run(self, config: BacktestConfig, strategy: "Strategy") -> BacktestResult:
        """Execute a single backtest and return its :class:`BacktestResult`."""
        from stock_backtest.backtest.cache import compute_run_hash

        # Defensive: strip any ``_CASH_`` pseudo-asset that slipped into the
        # universe. Cash is handled by the engine directly and must not be
        # subject to OHLCV loading or AssetSpec resolution.
        if any(spec.symbol == CASH_SYMBOL for spec in config.universe):
            config = BacktestConfig(
                strategy_name=config.strategy_name,
                params=config.params,
                universe=[s for s in config.universe if s.symbol != CASH_SYMBOL],
                period_start=config.period_start,
                period_end=config.period_end,
                base_currency=config.base_currency,
                market_mode=config.market_mode,
                initial_capital=config.initial_capital,
                rebalance_freq=config.rebalance_freq,
            )

        # --- 1. Effective period (intersection with per-asset windows) ----
        start, end = self._resolve_period(config)

        # --- 2. Price load ------------------------------------------------
        loader = self._price_loader or self._default_loader()
        prices = loader(config.universe, start, end)
        if prices.empty:
            raise ValueError(f"No prices returned for universe over [{start}..{end}]")
        prices = prices.sort_index()
        prices.index = pd.DatetimeIndex(prices.index).tz_localize(None).normalize()

        # --- 3. Trading-day axis -----------------------------------------
        sim_index = self._build_sim_index(config, prices, start, end)

        # Reindex (allowing forward-fill for crypto under MIXED mode only).
        prices_aligned = self._align_prices(config, prices, sim_index)

        # --- 4. Coverage guard -------------------------------------------
        market_by_asset = {spec.asset_id: spec.market for spec in config.universe}
        assert_universe_coverage(market_by_asset, prices_aligned, start, end)

        # --- 5. Rebalance schedule ---------------------------------------
        rebalance_dates = self._build_rebalance_dates(config, sim_index, start, end)

        # --- 6. Strategy weights -----------------------------------------
        # Strategy generate_weights signature uses asset symbols as cols; we
        # build a symbol-indexed DataFrame then translate back to asset_id.
        symbol_by_id = {spec.asset_id: spec.symbol for spec in config.universe}
        id_by_symbol = {spec.symbol: spec.asset_id for spec in config.universe}
        prices_by_symbol = prices_aligned.rename(columns=symbol_by_id)

        weights_sym = strategy.generate_weights(prices_by_symbol, rebalance_dates)
        # Drop the reserved cash pseudo-symbol if the strategy emitted it.
        # The residual weight ``1 - sum(asset_weights)`` automatically
        # remains as idle ``cash_by_ccy[base_currency]`` balance, so no
        # trade record is needed for cash.
        if CASH_SYMBOL in weights_sym.columns:
            weights_sym = weights_sym.drop(columns=[CASH_SYMBOL])
        # Normalise to asset_id columns and align to rebalance index.
        weights = weights_sym.rename(columns=id_by_symbol)
        missing = [c for c in prices_aligned.columns if c not in weights.columns]
        for c in missing:
            weights[c] = 0.0
        weights = weights[list(prices_aligned.columns)].fillna(0.0)
        weights.index = pd.DatetimeIndex(weights.index).tz_localize(None).normalize()

        # --- 7. FX converter & tax policy --------------------------------
        fx = self._fx_converter or FXConverter(
            self._open_session_or_none(),
            fx_spread_bps=self.settings.costs.fx_spread_bps,
        )
        tax_policy = build_tax_policy(self.settings)

        # --- 8. Portfolio init -------------------------------------------
        portfolio = Portfolio.from_initial(
            config.base_currency,
            {config.base_currency: Decimal(str(config.initial_capital))},
        )

        tax_state = TaxYearState(year=start.year)
        tax_paid_by_year: dict[int, Decimal] = {}
        trade_records: list[TradeRecord] = []
        realized_trades: list[RealizedTrade] = []

        equity_values: list[Decimal] = []
        rebalance_set = {d.date() for d in rebalance_dates}

        prev_year = start.year

        spec_by_id = {spec.asset_id: spec for spec in config.universe}

        for ts in sim_index:
            day = ts.date()

            # Year-end rollover first (so the new year starts fresh).
            if day.year != prev_year:
                tax_paid_by_year[prev_year] = tax_state.cash_tax_paid
                tax_state = tax_policy.on_year_end(tax_state)
                prev_year = day.year

            # Current prices on this day (as Decimal).
            row = prices_aligned.loc[ts]
            prices_today: dict[int, Decimal] = {
                int(aid): Decimal(str(val)) for aid, val in row.items() if pd.notna(val)
            }

            # Rebalance if scheduled.
            if day in rebalance_set and day in {d.date() for d in weights.index}:
                target = weights.loc[pd.Timestamp(day)]
                trades = self._build_rebalance_trades(
                    portfolio=portfolio,
                    target_weights=target,
                    prices_today=prices_today,
                    spec_by_id=spec_by_id,
                    fx=fx,
                    base_ccy=config.base_currency,
                    date=day,
                )
                # Execute sells first to free cash, then buys.
                for t in sorted(trades, key=lambda x: 0 if x["side"] == "SELL" else 1):
                    spec = spec_by_id[t["asset_id"]]
                    costs = self._resolve_costs(spec.market)
                    comm_bps = (
                        costs["commission_sell_bps"]
                        if t["side"] == "SELL"
                        else costs["commission_buy_bps"]
                    )
                    slip_bps = costs["slippage_bps"]
                    # Snapshot the FX-event count so we can capture any
                    # conversions triggered by ``apply_trade``'s internal
                    # ``_ensure_cash`` call.
                    fx_events_before = len(portfolio.fx_trades)
                    realized = portfolio.apply_trade(
                        asset_id=t["asset_id"],
                        side=t["side"],
                        qty=t["qty"],
                        price=prices_today[t["asset_id"]],
                        currency=spec.currency,
                        asset_class=spec.asset_class,
                        commission_bps=comm_bps,
                        slippage_bps=slip_bps,
                        fx=fx,
                        base_ccy=config.base_currency,
                        date=day,
                    )
                    # Emit FX trade records for any conversion done during
                    # this trade's ``_ensure_cash`` pass, before the BUY/SELL
                    # record so readers see the cash prep first.
                    for ev in portfolio.fx_trades[fx_events_before:]:
                        trade_records.append(
                            TradeRecord(
                                date=ev.date,
                                asset_id=None,
                                side="FX",
                                qty=ev.qty,
                                price=ev.fx_rate,
                                currency=ev.currency_from,
                                commission_bps=ZERO,
                                slippage_bps=ZERO,
                                currency_from=ev.currency_from,
                                currency_to=ev.currency_to,
                                fx_rate=ev.fx_rate,
                                spread_bps=ev.spread_bps,
                            )
                        )
                    trade_records.append(
                        TradeRecord(
                            date=day,
                            asset_id=t["asset_id"],
                            side=t["side"],
                            qty=t["qty"],
                            price=prices_today[t["asset_id"]],
                            currency=spec.currency,
                            commission_bps=Decimal(str(comm_bps)),
                            slippage_bps=Decimal(str(slip_bps)),
                        )
                    )
                    if realized is not None:
                        realized_trades.append(realized)
                        tax = tax_policy.apply_realized_gain(realized, tax_state)
                        if tax != ZERO:
                            # Tax is paid in KRW; convert to base_ccy for cash
                            # debit. A negative tax (loss refund within year)
                            # credits cash back.
                            debit_base = fx.convert(
                                tax, "KRW", config.base_currency, day
                            )
                            portfolio.cash_by_ccy[config.base_currency] = (
                                portfolio.cash_by_ccy.get(config.base_currency, ZERO)
                                - debit_base
                            )

            # Mark-to-market end of day.
            equity = portfolio.mark_to_market(
                prices_today, fx, config.base_currency, day
            )
            equity_values.append(equity)

        # Flush final year.
        tax_paid_by_year[prev_year] = tax_state.cash_tax_paid

        equity_curve = pd.Series(
            [float(v) for v in equity_values], index=sim_index, name="equity"
        )

        return BacktestResult(
            equity_curve=equity_curve,
            trades=trade_records,
            realized_trades=realized_trades,
            tax_paid_by_year=tax_paid_by_year,
            run_hash=compute_run_hash(
                config.strategy_name,
                config.params,
                [spec.symbol for spec in config.universe],
                (start, end),
                config.base_currency,
            ),
        )

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------
    def _default_loader(self) -> PriceLoader:
        if self._session_factory is None:
            raise ValueError(
                "BacktestEngine requires a session_factory or an explicit "
                "price_loader override."
            )
        return default_price_loader(self._session_factory)

    def _open_session_or_none(self) -> "Session | None":
        if self._session_factory is None:
            return None
        return self._session_factory()

    def _compute_cushion_bps(
        self,
        universe_currencies: Iterable[str],
        base_currency: str,
        markets: Iterable[str],
    ) -> Decimal:
        """Return the dynamic cash-cushion in bps for the next rebalance.

        Formula
        -------
        ``cushion_bps = max_commission_buy_bps + max_slippage_bps
                        + fx_component + _SAFETY_BUFFER_BPS``

        - ``max_*`` is taken across every market represented in the universe
          (fully-resolved via :func:`stock_backtest.config.get_costs` so market
          overrides like ``KR.commission_sell_bps=28`` are accounted for).
        - ``fx_component`` is ``max_fx_spread_bps`` when the universe contains
          at least one asset whose currency differs from ``base_currency``;
          otherwise zero.
        - The total is capped at ``_MAX_CUSHION_BPS`` (500bps = 5%) and a
          warning is logged when the raw value hits or exceeds that cap.
        """
        currencies = set(universe_currencies)
        markets_list = [m for m in set(markets)] or [""]

        max_commission_buy = Decimal("0")
        max_slippage = Decimal("0")
        max_fx_spread = Decimal("0")
        for market in markets_list:
            costs = self._resolve_costs(market)
            if costs["commission_buy_bps"] > max_commission_buy:
                max_commission_buy = costs["commission_buy_bps"]
            if costs["slippage_bps"] > max_slippage:
                max_slippage = costs["slippage_bps"]
            if costs["fx_spread_bps"] > max_fx_spread:
                max_fx_spread = costs["fx_spread_bps"]

        needs_fx = any(ccy != base_currency for ccy in currencies)
        fx_component = max_fx_spread if needs_fx else Decimal("0")

        raw = max_commission_buy + max_slippage + fx_component + _SAFETY_BUFFER_BPS
        if raw > _MAX_CUSHION_BPS:
            logger.warning(
                "rebalance cushion %s bps exceeds cap %s bps; clamping. "
                "markets=%s currencies=%s base=%s",
                raw,
                _MAX_CUSHION_BPS,
                sorted(markets_list),
                sorted(currencies),
                base_currency,
            )
            return _MAX_CUSHION_BPS
        return raw

    def _resolve_costs(self, market: str) -> dict[str, Decimal]:
        from stock_backtest.config import get_costs

        resolved = get_costs(self.settings, market)
        return {
            "commission_buy_bps": Decimal(str(resolved.commission_buy_bps)),
            "commission_sell_bps": Decimal(str(resolved.commission_sell_bps)),
            "slippage_bps": Decimal(str(resolved.slippage_bps)),
            "fx_spread_bps": Decimal(str(resolved.fx_spread_bps)),
        }

    def _resolve_period(self, config: BacktestConfig) -> tuple[_dt.date, _dt.date]:
        starts: list[_dt.date] = [config.period_start]
        ends: list[_dt.date] = [config.period_end]
        for spec in config.universe:
            if spec.start_date is not None:
                starts.append(spec.start_date)
            if spec.end_date is not None:
                ends.append(spec.end_date)
        start = max(starts)
        end = min(ends)
        if start > end:
            raise ValueError(
                f"Effective period empty: start={start} > end={end}. Check "
                "per-asset start/end dates."
            )
        return start, end

    def _build_sim_index(
        self,
        config: BacktestConfig,
        prices: pd.DataFrame,
        start: _dt.date,
        end: _dt.date,
    ) -> pd.DatetimeIndex:
        mode = config.market_mode.upper()
        markets = {spec.market for spec in config.universe}
        if mode == "CRYPTO":
            return get_trading_days("CRYPTO", start, end)
        if mode == "STOCK":
            # Union of actual equity calendars in use.
            return union_trading_days(sorted(markets), start, end)
        if mode == "MIXED":
            return union_trading_days(sorted(markets), start, end)
        raise ValueError(f"Unknown market_mode: {config.market_mode!r}")

    def _align_prices(
        self,
        config: BacktestConfig,
        prices: pd.DataFrame,
        sim_index: pd.DatetimeIndex,
    ) -> pd.DataFrame:
        mode = config.market_mode.upper()
        aligned = prices.reindex(sim_index)
        if mode == "MIXED":
            # Forward-fill only columns whose asset.market == CRYPTO.
            crypto_ids = [
                spec.asset_id
                for spec in config.universe
                if spec.market.upper() == "CRYPTO"
            ]
            if crypto_ids:
                present = [c for c in crypto_ids if c in aligned.columns]
                aligned[present] = aligned[present].ffill()
        return aligned

    def _build_rebalance_dates(
        self,
        config: BacktestConfig,
        sim_index: pd.DatetimeIndex,
        start: _dt.date,
        end: _dt.date,
    ) -> pd.DatetimeIndex:
        freq = config.rebalance_freq
        # First trading day always triggers an initial allocation.
        try:
            raw = pd.date_range(start=start, end=end, freq=freq)
        except ValueError:
            # Fallback: older pandas uses 'M'/'Q'/'A' instead of 'ME'/'QE'/'YE'.
            legacy = {"ME": "M", "QE": "Q", "YE": "A", "Y": "A"}
            raw = pd.date_range(start=start, end=end, freq=legacy.get(freq, freq))
        if len(raw) == 0:
            raw = pd.DatetimeIndex([pd.Timestamp(start)])
        # Snap to valid trading days using the primary market of the universe.
        # For MIXED, prefer a non-crypto market if any; else CRYPTO.
        markets = [spec.market for spec in config.universe]
        primary = next((m for m in markets if m.upper() != "CRYPTO"), markets[0])
        snapped: list[pd.Timestamp] = []
        for ts in raw:
            d = ts.date()
            if d < start:
                continue
            if d > end:
                d = end
            snap = previous_trading_day(primary, d)
            if snap < start:
                continue
            snapped.append(pd.Timestamp(snap))
        # Ensure the first sim_index date is in the rebalance set (initial allocation).
        if len(sim_index) > 0:
            first = pd.Timestamp(sim_index[0].date())
            if first not in snapped:
                snapped.insert(0, first)
        out = pd.DatetimeIndex(sorted(set(snapped)))
        # Keep only points that are in the simulation index.
        sim_set = set(sim_index)
        return pd.DatetimeIndex([d for d in out if d in sim_set])

    def _build_rebalance_trades(
        self,
        portfolio: Portfolio,
        target_weights: pd.Series,
        prices_today: dict[int, Decimal],
        spec_by_id: dict[int, AssetSpec],
        fx: FXConverter,
        base_ccy: str,
        date: _dt.date,
    ) -> list[dict[str, Any]]:
        """Translate target weights into an unordered list of trades.

        The trade list is a list of dicts with keys ``asset_id``, ``side`` and
        ``qty``; the caller applies them in sell-first order.
        """
        equity = portfolio.mark_to_market(prices_today, fx, base_ccy, date)
        if equity <= ZERO:
            return []
        # Reserve a dynamic cushion for commission + slippage + fx-spread so
        # the resulting buy orders don't overdraft cash on the first rebalance.
        # The cushion is derived from the most-conservative (largest) per-
        # market costs plus a safety buffer (see ``_compute_cushion_bps``).
        universe_currencies = {spec.currency for spec in spec_by_id.values()}
        cushion_bps = self._compute_cushion_bps(
            universe_currencies=universe_currencies,
            base_currency=base_ccy,
            markets={spec.market for spec in spec_by_id.values()},
        )
        cushion_factor = _ONE - (cushion_bps / Decimal("10000"))
        equity = equity * cushion_factor

        trades: list[dict[str, Any]] = []
        for asset_id, weight_raw in target_weights.items():
            asset_id_int = int(asset_id)
            weight = Decimal(str(float(weight_raw)))
            spec = spec_by_id[asset_id_int]
            price = prices_today.get(asset_id_int)
            if price is None or price <= ZERO:
                continue

            target_value_base = equity * weight
            # Convert target value from base_ccy to asset's native ccy.
            target_value_native = fx.convert(
                target_value_base, base_ccy, spec.currency, date
            )
            target_qty = target_value_native / price if price > ZERO else ZERO

            current_qty = (
                portfolio.positions[asset_id_int].qty
                if asset_id_int in portfolio.positions
                else ZERO
            )
            delta = target_qty - current_qty
            # Ignore trivial deltas (<1e-9 of a share) to avoid noise.
            if abs(delta) < Decimal("1e-9"):
                continue
            if delta > ZERO:
                trades.append({"asset_id": asset_id_int, "side": "BUY", "qty": delta})
            else:
                trades.append({"asset_id": asset_id_int, "side": "SELL", "qty": -delta})
        return trades
