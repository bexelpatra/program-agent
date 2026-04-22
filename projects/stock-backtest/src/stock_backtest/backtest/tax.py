"""Korean-resident tax module for the backtest engine.

This module implements the tax rules described in ``architecture.md`` §14.
It exposes a small surface the backtest engine can call at trade-close and
year-end time without knowing the underlying tax profile:

* :class:`RealizedTrade` – a value object describing a realized cash-flow
  (capital gain from a sell, or a dividend receipt) in KRW.
* :class:`TaxYearState` – per-calendar-year running accumulator (realized
  gains grouped by asset class, dividend taxes paid, total cash tax paid).
* :class:`KrResidentTax` – applies the Korean-resident tax rules.
* :class:`NoopTax` – zero-tax fallback used when ``tax.enabled=false``.
* :func:`build_tax_policy` – factory that returns the right policy given a
  :class:`~stock_backtest.config.Settings` instance.

Notes & simplifications
-----------------------
* All monetary values are :class:`decimal.Decimal` to avoid float drift in
  tax accrual. Callers are expected to have already converted FX (USD→KRW)
  at the trade's settlement date before constructing a :class:`RealizedTrade`.
* Overseas capital gains (overseas_equity / overseas_etf / kr_overseas_etf)
  are aggregated into a **single annual bucket** with the basic deduction
  (default 2,500,000 KRW). Losses net against gains within the same year;
  carry-over across years is **not** implemented (Korean tax law does not
  currently allow it for these categories in the simplified model).
* Crypto is an independent annual bucket with its own deduction when
  ``crypto_enabled`` is true. If disabled, crypto realizations are not
  taxed.
* Dividends are withheld at a flat 15.4% regardless of source (a
  simplification – foreign-tax-credit and financial-income aggregate
  taxation are intentionally out of scope; domestic-listed foreign ETFs
  distributions are treated the same as foreign dividends here).
* Year-end rollover is modelled at 12/31 UTC; callers drive this by
  invoking :meth:`KrResidentTax.on_year_end` when the backtest clock
  crosses a year boundary.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from decimal import ROUND_HALF_UP, Decimal
from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:  # pragma: no cover - typing only
    from stock_backtest.config import Settings


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

#: Asset classes recognised by the tax module. These strings are what the
#: engine must pass in via :attr:`RealizedTrade.asset_class`.
AssetClass = Literal[
    "overseas_equity",
    "overseas_etf",
    "kr_equity_etf",
    "kr_bond_etf",
    "kr_mixed_etf",
    "kr_overseas_etf",
    "crypto",
    "commodity",
]

#: Asset classes pooled into the overseas capital-gains bucket.
_OVERSEAS_CLASSES: frozenset[str] = frozenset(
    {"overseas_equity", "overseas_etf", "kr_overseas_etf"}
)

#: Asset classes taxed as "dividend income" (15.4%) on realised **capital**
#: gains (bond / mixed ETFs listed domestically).
_KR_DIVIDEND_INCOME_CAP_CLASSES: frozenset[str] = frozenset(
    {"kr_bond_etf", "kr_mixed_etf"}
)

#: Asset classes whose realized capital gains are untaxed.
_TAX_FREE_CAP_CLASSES: frozenset[str] = frozenset({"kr_equity_etf", "commodity"})

#: Flat KR withholding rate on dividends (simplification – see module docstring).
_KR_DIVIDEND_RATE: Decimal = Decimal("0.154")

#: Number of KRW decimals to keep internally. KRW is typically whole won; we
#: round at the very end via :func:`_round_krw`.
_KRW_QUANTUM: Decimal = Decimal("1")

ZERO: Decimal = Decimal("0")


def _to_decimal(value: Decimal | int | float | str) -> Decimal:
    """Coerce ``value`` to :class:`Decimal` without float-string drift."""

    if isinstance(value, Decimal):
        return value
    if isinstance(value, float):
        return Decimal(str(value))
    return Decimal(value)


def _round_krw(amount: Decimal) -> Decimal:
    """Round a KRW amount to whole won (banker-proof half-up)."""

    return amount.quantize(_KRW_QUANTUM, rounding=ROUND_HALF_UP)


# ---------------------------------------------------------------------------
# Value objects
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class RealizedTrade:
    """A single realized cash-flow eligible for tax accrual.

    Parameters
    ----------
    asset_id:
        Opaque asset identifier (matches ``assets.asset_id``). Not used for
        tax computation itself, carried through for logging.
    asset_class:
        One of :data:`AssetClass`. Determines which tax rule applies.
    proceeds_krw:
        Gross sale proceeds (or dividend amount) in KRW. For dividends this
        is the pre-tax dividend amount.
    cost_basis_krw:
        Cost basis in KRW. Ignored for dividends.
    trade_date:
        Settlement date; used for year-boundary checks.
    is_dividend:
        ``True`` if this event is a dividend receipt, otherwise a realized
        capital gain/loss from a sell.
    """

    asset_id: int | str
    asset_class: AssetClass
    proceeds_krw: Decimal
    cost_basis_krw: Decimal
    trade_date: date
    is_dividend: bool = False

    @property
    def realized_gain_krw(self) -> Decimal:
        """Signed capital gain (proceeds − cost basis). May be negative."""

        return _to_decimal(self.proceeds_krw) - _to_decimal(self.cost_basis_krw)


@dataclass
class TaxYearState:
    """Running accumulator for a single tax year.

    Separate buckets are kept per asset-class-group so year-end settlement
    can decide per-group deductions. :attr:`cash_tax_paid` is the sum of
    every tax debit charged to the portfolio during the year.
    """

    year: int
    realized_capital_gains_by_class: dict[str, Decimal] = field(
        default_factory=lambda: {
            "overseas": ZERO,  # pooled overseas bucket
            "kr_dividend_income_cap": ZERO,  # bond/mixed ETFs, taxed on sell
            "crypto": ZERO,
            "tax_free": ZERO,  # kr_equity_etf etc, tracked for reporting
        }
    )
    dividend_taxed: Decimal = ZERO
    cash_tax_paid: Decimal = ZERO


# ---------------------------------------------------------------------------
# Tax policy interface
# ---------------------------------------------------------------------------


class _TaxPolicy:
    """Protocol-ish base class. The engine only cares about three methods."""

    def apply_realized_gain(
        self, trade: RealizedTrade, state: TaxYearState
    ) -> Decimal:  # pragma: no cover - interface
        raise NotImplementedError

    def apply_dividend(
        self, trade: RealizedTrade, state: TaxYearState
    ) -> Decimal:  # pragma: no cover - interface
        raise NotImplementedError

    def on_year_end(
        self, state: TaxYearState
    ) -> TaxYearState:  # pragma: no cover - interface
        raise NotImplementedError


class NoopTax(_TaxPolicy):
    """Zero-tax policy used when ``tax.enabled=false``.

    Every :meth:`apply_*` call is a no-op returning :data:`ZERO`. Year-end
    rollover still advances the state's year so caller code remains uniform.
    """

    def apply_realized_gain(self, trade: RealizedTrade, state: TaxYearState) -> Decimal:
        return ZERO

    def apply_dividend(self, trade: RealizedTrade, state: TaxYearState) -> Decimal:
        return ZERO

    def on_year_end(self, state: TaxYearState) -> TaxYearState:
        return TaxYearState(year=state.year + 1)


class KrResidentTax(_TaxPolicy):
    """Korean-resident tax policy (architecture.md §14).

    The policy is *stateless*; all per-year accumulation lives in the
    caller-owned :class:`TaxYearState`. This makes the policy safe to share
    across runs and easy to unit test.
    """

    def __init__(self, profile: dict) -> None:
        """Build from the ``tax.kr_resident`` profile dict.

        ``profile`` accepts both the ``TaxProfile`` pydantic model (dumped)
        and a raw dict so the factory can feed either shape.
        """

        self._overseas_rate: Decimal = _to_decimal(
            profile.get("overseas_capital_gains_rate", "0.22")
        )
        self._overseas_deduction: Decimal = _to_decimal(
            profile.get("overseas_annual_deduction_krw", 2_500_000)
        )
        self._dividend_rate: Decimal = _to_decimal(
            profile.get("overseas_dividend_rate", _KR_DIVIDEND_RATE)
        )
        self._crypto_enabled: bool = bool(profile.get("crypto_enabled", False))
        self._crypto_rate: Decimal = _to_decimal(
            profile.get("crypto_capital_gains_rate", "0.22")
        )
        self._crypto_deduction: Decimal = _to_decimal(
            profile.get("crypto_annual_deduction_krw", 2_500_000)
        )

    # ------------------------------------------------------------------
    # Factories
    # ------------------------------------------------------------------

    @classmethod
    def from_config(cls, settings: "Settings") -> "_TaxPolicy":
        """Build a policy from the application :class:`Settings` tree.

        Returns a :class:`NoopTax` when ``settings.tax.enabled`` is false
        or when the active profile is empty (e.g. the ``none`` profile).
        """

        if not settings.tax.enabled:
            return NoopTax()

        profile = settings.tax.profiles.get(settings.tax.profile)
        if profile is None:
            return NoopTax()
        # Pydantic v2 dump, excluding None fields for forgiving construction.
        profile_dict = profile.model_dump(exclude_none=True)
        if not profile_dict:
            return NoopTax()
        return cls(profile_dict)

    # ------------------------------------------------------------------
    # Per-trade hooks
    # ------------------------------------------------------------------

    def apply_realized_gain(self, trade: RealizedTrade, state: TaxYearState) -> Decimal:
        """Accrue a realized-gain tax event into ``state`` and return the tax
        charged *by this trade* (i.e. the delta of cumulative tax before vs
        after this trade). Losses reduce the bucket and can refund
        previously-paid tax within the same year; tax charged therefore
        may be negative.
        """

        if trade.is_dividend:
            raise ValueError(
                "apply_realized_gain received a dividend trade; "
                "use apply_dividend instead."
            )

        cls = trade.asset_class
        gain = trade.realized_gain_krw

        if cls in _TAX_FREE_CAP_CLASSES:
            state.realized_capital_gains_by_class["tax_free"] += gain
            return ZERO

        if cls in _OVERSEAS_CLASSES:
            bucket_key = "overseas"
            rate = self._overseas_rate
            deduction = self._overseas_deduction
        elif cls == "crypto":
            if not self._crypto_enabled:
                # Track in bucket for reporting but do not tax.
                state.realized_capital_gains_by_class["crypto"] += gain
                return ZERO
            bucket_key = "crypto"
            rate = self._crypto_rate
            deduction = self._crypto_deduction
        elif cls in _KR_DIVIDEND_INCOME_CAP_CLASSES:
            # Bond/mixed ETFs: domestic 15.4% withheld on *positive* gain.
            # Losses are not refundable (treated as 0 tax for that trade).
            tax = _round_krw(max(gain, ZERO) * self._dividend_rate)
            state.realized_capital_gains_by_class["kr_dividend_income_cap"] += gain
            state.cash_tax_paid += tax
            return tax
        else:
            raise ValueError(f"Unknown asset_class for realized gain: {cls!r}")

        # Overseas / crypto: annual-deduction bucket logic.
        bucket = state.realized_capital_gains_by_class
        prev_cumulative = bucket[bucket_key]
        new_cumulative = prev_cumulative + gain
        bucket[bucket_key] = new_cumulative

        prev_taxable = max(prev_cumulative - deduction, ZERO)
        new_taxable = max(new_cumulative - deduction, ZERO)

        prev_tax = _round_krw(prev_taxable * rate)
        new_tax = _round_krw(new_taxable * rate)
        tax_delta = new_tax - prev_tax

        state.cash_tax_paid += tax_delta
        return tax_delta

    def apply_dividend(self, trade: RealizedTrade, state: TaxYearState) -> Decimal:
        """Withhold 15.4% on the dividend ``proceeds_krw`` and update state."""

        if not trade.is_dividend:
            raise ValueError(
                "apply_dividend received a non-dividend trade; "
                "use apply_realized_gain instead."
            )

        gross = _to_decimal(trade.proceeds_krw)
        if gross <= ZERO:
            return ZERO
        tax = _round_krw(gross * self._dividend_rate)
        state.dividend_taxed += tax
        state.cash_tax_paid += tax
        return tax

    # ------------------------------------------------------------------
    # Year-end
    # ------------------------------------------------------------------

    def on_year_end(self, state: TaxYearState) -> TaxYearState:
        """Return a fresh :class:`TaxYearState` for ``state.year + 1``.

        All buckets reset: overseas losses do **not** carry over in this
        simplified model. Callers should log / persist ``state`` before
        dropping the reference if reporting is needed.
        """

        return TaxYearState(year=state.year + 1)


# ---------------------------------------------------------------------------
# Factory
# ---------------------------------------------------------------------------


def build_tax_policy(settings: "Settings") -> _TaxPolicy:
    """Return the tax policy implied by ``settings``.

    Dispatches on ``settings.tax.enabled`` and ``settings.tax.profile``:

    * ``enabled=false``          → :class:`NoopTax`
    * profile ``kr_resident``    → :class:`KrResidentTax`
    * unknown / empty profile    → :class:`NoopTax` (safe default)
    """

    if not settings.tax.enabled:
        return NoopTax()

    profile_name = settings.tax.profile
    if profile_name == "kr_resident":
        return KrResidentTax.from_config(settings)

    # Unknown profile names fall back to Noop rather than raising, to keep
    # comparison runs (`none: {}` or future profiles) cheap. The config
    # loader already validates that the profile key exists.
    return NoopTax()


__all__ = [
    "AssetClass",
    "KrResidentTax",
    "NoopTax",
    "RealizedTrade",
    "TaxYearState",
    "build_tax_policy",
]
