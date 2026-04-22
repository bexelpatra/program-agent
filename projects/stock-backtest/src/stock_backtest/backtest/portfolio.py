"""Portfolio state management for the backtest engine.

Holds multi-currency cash balances and per-asset positions, and applies
trades (buy / sell) while generating :class:`RealizedTrade` records that feed
the tax module (architecture decision #14).

All monetary values are :class:`decimal.Decimal`.
"""

from __future__ import annotations

import datetime as _dt
from dataclasses import dataclass, field
from decimal import Decimal
from typing import TYPE_CHECKING

from .tax import RealizedTrade

if TYPE_CHECKING:  # pragma: no cover - typing only
    from .fx import FXConverter


__all__ = ["Position", "Portfolio", "InsufficientFundsError", "FXTradeEvent"]

ZERO = Decimal("0")
_ONE = Decimal("1")
_BPS = Decimal("10000")


class InsufficientFundsError(RuntimeError):
    """Raised when a requested trade cannot be funded even after cross-currency
    rebalancing from other cash buckets."""


@dataclass
class Position:
    """A single open position.

    Notes
    -----
    ``cost_basis_ccy`` is the **total** cost basis in the position's native
    currency (not per-unit); dividing by ``qty`` yields the average cost.
    """

    asset_id: int
    qty: Decimal
    cost_basis_ccy: Decimal  # total cost basis in `currency`
    currency: str
    asset_class: str  # one of stock_backtest.backtest.tax.AssetClass


@dataclass
class FXTradeEvent:
    """An FX conversion emitted by :meth:`Portfolio._ensure_cash`.

    Mirrors the ``side="FX"`` :class:`~stock_backtest.backtest.engine.TradeRecord`
    shape so the engine can re-emit these without knowing portfolio internals.

    - ``qty``: amount converted **in the source currency** (always positive).
    - ``fx_rate``: mid-market rate (before spread) ``source -> target``.
    - ``spread_bps``: the portfolio-level ``fx_spread_bps`` applied.
    """

    date: _dt.date
    currency_from: str
    currency_to: str
    qty: Decimal  # src-currency amount
    fx_rate: Decimal  # mid rate src->dst
    spread_bps: Decimal


@dataclass
class Portfolio:
    """Multi-currency portfolio state.

    Parameters
    ----------
    base_currency:
        ISO currency code used for equity reporting.
    initial_cash:
        Mapping ``ccy -> amount`` describing the starting cash balances. All
        values are coerced to :class:`Decimal`.
    """

    base_currency: str
    cash_by_ccy: dict[str, Decimal] = field(default_factory=dict)
    positions: dict[int, Position] = field(default_factory=dict)
    # FX conversion events emitted by ``_ensure_cash``. The engine drains this
    # list after each ``apply_trade`` call to synthesise ``side='FX'`` trade
    # records. See architecture.md "FX TradeRecord 스키마 확장".
    fx_trades: list["FXTradeEvent"] = field(default_factory=list)

    # ------------------------------------------------------------------
    # Construction helpers
    # ------------------------------------------------------------------
    @classmethod
    def from_initial(
        cls,
        base_currency: str,
        initial_cash: dict[str, Decimal | int | float | str],
    ) -> "Portfolio":
        cash = {k: Decimal(str(v)) for k, v in initial_cash.items()}
        cash.setdefault(base_currency, ZERO)
        return cls(base_currency=base_currency, cash_by_ccy=cash, positions={})

    # ------------------------------------------------------------------
    # Cash helpers
    # ------------------------------------------------------------------
    def _get_cash(self, ccy: str) -> Decimal:
        return self.cash_by_ccy.get(ccy, ZERO)

    def _add_cash(self, ccy: str, amount: Decimal) -> None:
        self.cash_by_ccy[ccy] = self._get_cash(ccy) + amount

    def _ensure_cash(
        self,
        ccy: str,
        amount_needed: Decimal,
        fx: "FXConverter",
        date: _dt.date,
    ) -> None:
        """Ensure that ``cash_by_ccy[ccy] >= amount_needed`` by converting from
        other currency buckets if needed. Converts with spread applied.

        Raises
        ------
        InsufficientFundsError
            If the total portfolio cash (across all currencies) cannot cover
            ``amount_needed`` even after conversion.
        """
        current = self._get_cash(ccy)
        shortfall = amount_needed - current
        if shortfall <= ZERO:
            return

        # Find other currencies with available balance, largest-first.
        others = sorted(
            (
                (c, bal)
                for c, bal in self.cash_by_ccy.items()
                if c != ccy and bal > ZERO
            ),
            key=lambda kv: kv[1],
            reverse=True,
        )
        # The portfolio-level spread (in bps) is published by the converter.
        # It is a ``Decimal`` for safe arithmetic here; engine readers coerce
        # to ``int`` when persisting.
        spread_bps = getattr(fx, "_fx_spread_bps", Decimal("0"))
        for src_ccy, src_bal in others:
            if shortfall <= ZERO:
                break
            # How much of ccy would src_bal produce?
            max_from_src = fx.convert(src_bal, src_ccy, ccy, date, apply_spread=True)
            if max_from_src <= ZERO:
                continue
            # Mid rate (no spread) for the FX trade audit row.
            mid_rate = fx.rate(src_ccy, ccy, date)
            if max_from_src >= shortfall:
                # Convert exactly enough. Back-out the src amount needed.
                #
                # NOTE: we MUST NOT use ``fx.convert(shortfall, ccy, src_ccy,
                # apply_spread=True)`` here. ``convert`` charges the spread on
                # the *to-side* (rate worsened), so a reverse-direction lookup
                # would make wider spreads *reduce* ``src_needed`` — the
                # opposite of the real economic cost. Instead we solve for the
                # source amount directly, charging the spread on the source
                # side (``convert_for_target``). This makes wider
                # ``fx_spread_bps`` consume strictly more source currency, so
                # cross-currency rebalances become monotonically more
                # expensive as the spread widens (architecture decision #4).
                src_needed = fx.convert_for_target(
                    shortfall, src_ccy, ccy, date, apply_spread=True
                )
                # Guard against tiny rounding overdrafts.
                if src_needed > src_bal:
                    src_needed = src_bal
                self.cash_by_ccy[src_ccy] = src_bal - src_needed
                self._add_cash(ccy, shortfall)
                self.fx_trades.append(
                    FXTradeEvent(
                        date=date,
                        currency_from=src_ccy,
                        currency_to=ccy,
                        qty=src_needed,
                        fx_rate=mid_rate,
                        spread_bps=spread_bps,
                    )
                )
                shortfall = ZERO
            else:
                # Drain this bucket entirely.
                self.cash_by_ccy[src_ccy] = ZERO
                self._add_cash(ccy, max_from_src)
                self.fx_trades.append(
                    FXTradeEvent(
                        date=date,
                        currency_from=src_ccy,
                        currency_to=ccy,
                        qty=src_bal,
                        fx_rate=mid_rate,
                        spread_bps=spread_bps,
                    )
                )
                shortfall -= max_from_src

        if shortfall > ZERO:
            raise InsufficientFundsError(
                f"Insufficient funds in {ccy}: need {amount_needed}, "
                f"short by {shortfall} even after cross-currency conversion."
            )

    # ------------------------------------------------------------------
    # Mark-to-market
    # ------------------------------------------------------------------
    def mark_to_market(
        self,
        prices_on_date: dict[int, Decimal],
        fx: "FXConverter",
        base_ccy: str,
        date: _dt.date,
    ) -> Decimal:
        """Return portfolio equity in ``base_ccy`` on ``date``.

        ``prices_on_date`` maps ``asset_id -> latest price`` in the asset's
        native currency.
        """
        equity = ZERO

        # Cash
        for ccy, amount in self.cash_by_ccy.items():
            if amount == ZERO:
                continue
            equity += fx.convert(amount, ccy, base_ccy, date, apply_spread=False)

        # Positions
        for asset_id, pos in self.positions.items():
            price = prices_on_date.get(asset_id)
            if price is None or pos.qty == ZERO:
                continue
            if not isinstance(price, Decimal):
                price = Decimal(str(price))
            native_value = pos.qty * price
            equity += fx.convert(
                native_value, pos.currency, base_ccy, date, apply_spread=False
            )
        return equity

    # ------------------------------------------------------------------
    # Trade application
    # ------------------------------------------------------------------
    def apply_trade(
        self,
        asset_id: int,
        side: str,
        qty: Decimal,
        price: Decimal,
        currency: str,
        asset_class: str,
        commission_bps: Decimal | float,
        slippage_bps: Decimal | float,
        fx: "FXConverter",
        base_ccy: str,
        date: _dt.date,
    ) -> RealizedTrade | None:
        """Apply a trade. Returns a :class:`RealizedTrade` on sells, else None.

        The returned :class:`RealizedTrade` carries proceeds/cost-basis in KRW
        for direct consumption by the tax module. Buys mutate state only.
        """
        if side not in ("BUY", "SELL"):
            raise ValueError(f"Unknown side: {side!r}")
        if qty <= ZERO:
            return None
        if not isinstance(qty, Decimal):
            qty = Decimal(str(qty))
        if not isinstance(price, Decimal):
            price = Decimal(str(price))
        commission_bps = Decimal(str(commission_bps))
        slippage_bps = Decimal(str(slippage_bps))

        slip_factor = slippage_bps / _BPS
        comm_factor = commission_bps / _BPS

        if side == "BUY":
            exec_price = price * (_ONE + slip_factor)
            gross = qty * exec_price
            commission = gross * comm_factor
            total_cost = gross + commission

            # Ensure we have funds in the trade currency.
            self._ensure_cash(currency, total_cost, fx, date)
            self._add_cash(currency, -total_cost)

            pos = self.positions.get(asset_id)
            if pos is None:
                self.positions[asset_id] = Position(
                    asset_id=asset_id,
                    qty=qty,
                    cost_basis_ccy=total_cost,
                    currency=currency,
                    asset_class=asset_class,
                )
            else:
                pos.qty += qty
                pos.cost_basis_ccy += total_cost
            return None

        # SELL
        pos = self.positions.get(asset_id)
        if pos is None or pos.qty < qty:
            raise ValueError(
                f"Cannot sell {qty} of asset_id={asset_id}: current qty="
                f"{pos.qty if pos else 0}"
            )
        exec_price = price * (_ONE - slip_factor)
        gross = qty * exec_price
        commission = gross * comm_factor
        proceeds = gross - commission

        # Average cost basis for the sold portion.
        avg_cost = pos.cost_basis_ccy / pos.qty if pos.qty > ZERO else ZERO
        sold_cost_basis = avg_cost * qty

        pos.qty -= qty
        pos.cost_basis_ccy -= sold_cost_basis
        if pos.qty <= ZERO:
            # Clean up epsilon remainders.
            del self.positions[asset_id]

        self._add_cash(currency, proceeds)

        # Convert to KRW for the tax module regardless of base currency; the
        # KR-resident profile is defined in KRW.
        proceeds_krw = fx.convert(proceeds, currency, "KRW", date, apply_spread=False)
        cost_basis_krw = fx.convert(
            sold_cost_basis, currency, "KRW", date, apply_spread=False
        )
        return RealizedTrade(
            asset_id=asset_id,
            asset_class=asset_class,  # type: ignore[arg-type]
            proceeds_krw=proceeds_krw,
            cost_basis_krw=cost_basis_krw,
            trade_date=date,
            is_dividend=False,
        )
