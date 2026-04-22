"""FX conversion utilities for the backtest engine.

This module wraps :class:`stock_backtest.data.repository.FxRateRepository` and
layers the ``fx_spread_bps`` cost model on top of it, in line with
architecture decision #4.

Design notes
------------
- **Decimal arithmetic.** All monetary values flow through :class:`decimal.Decimal`
  to keep downstream tax accrual free of float drift. The underlying FX rate is
  stored as ``float`` in Postgres, so we stringify on the boundary.
- **Fallback window.** :meth:`FxRateRepository.get_rate` already implements a
  7-day backward fallback; we rely on it and simply raise if the repository
  returns ``None`` (no rate within a week).
- **Spread direction symmetry.** When ``apply_spread=True`` we subtract
  ``fx_spread_bps / 2`` on the from-side and add the same on the to-side, so
  round-tripping USD→KRW→USD at the same spread reproduces the documented
  one-leg cost of roughly ``fx_spread_bps/2`` per direction.
- **Trivial path.** ``from_ccy == to_ccy`` short-circuits at rate 1 so callers
  can mark-to-market base-currency cash without touching the DB.
"""

from __future__ import annotations

import datetime as _dt
from decimal import Decimal
from typing import TYPE_CHECKING, Any

from stock_backtest.data.repository import FxRateRepository

if TYPE_CHECKING:  # pragma: no cover - typing only
    from sqlalchemy.orm import Session


__all__ = ["FXConverter", "FXRateUnavailableError"]


_ONE = Decimal("1")
_BPS = Decimal("10000")
_TWO = Decimal("2")


class FXRateUnavailableError(LookupError):
    """Raised when no FX rate is available for the requested ``(base, quote, date)``
    within the repository's fallback window."""

    def __init__(self, base: str, quote: str, on: _dt.date) -> None:
        self.base = base
        self.quote = quote
        self.date = on
        super().__init__(
            f"No FX rate available for {base}->{quote} on or within 7 days before "
            f"{on.isoformat()}"
        )


class FXConverter:
    """Currency conversion helper with optional spread application.

    Parameters
    ----------
    session:
        SQLAlchemy session used to query ``fx_rates``. May be ``None`` when the
        converter is used against a pre-populated ``rate_overrides`` mapping
        (useful for unit tests without a live DB).
    fx_spread_bps:
        One-way portfolio-level spread expressed in basis points. When
        :meth:`convert` is called with ``apply_spread=True`` the effective rate
        is worsened by ``fx_spread_bps / 2`` on each leg.
    rate_overrides:
        Optional in-memory map ``(base, quote, date) -> rate`` that short-
        circuits DB lookups. Intended for tests and deterministic re-runs.
    """

    def __init__(
        self,
        session: "Session | None",
        fx_spread_bps: int | float,
        *,
        rate_overrides: dict[tuple[str, str, _dt.date], Any] | None = None,
    ) -> None:
        self._session = session
        self._fx_spread_bps = Decimal(str(fx_spread_bps))
        self._half_spread = self._fx_spread_bps / _TWO / _BPS
        self._repo: FxRateRepository | None = (
            FxRateRepository(session) if session is not None else None
        )
        self._overrides: dict[tuple[str, str, _dt.date], Decimal] = {
            (b, q, d): Decimal(str(r))
            for (b, q, d), r in (rate_overrides or {}).items()
        }

    # ------------------------------------------------------------------
    # Raw rate lookup
    # ------------------------------------------------------------------
    def rate(self, base: str, quote: str, on: _dt.date) -> Decimal:
        """Return the mid-market FX rate for ``base -> quote`` on ``on``.

        Raises
        ------
        FXRateUnavailableError
            If the repository has no rate within its 7-day fallback window.
        """
        if base == quote:
            return _ONE

        key = (base, quote, on)
        if key in self._overrides:
            return self._overrides[key]

        # Try the inverse override as well (common for USDKRW vs KRWUSD).
        inv_key = (quote, base, on)
        if inv_key in self._overrides:
            inv = self._overrides[inv_key]
            if inv == 0:
                raise FXRateUnavailableError(base, quote, on)
            return _ONE / inv

        if self._repo is None:
            raise FXRateUnavailableError(base, quote, on)

        raw = self._repo.get_rate(base, quote, on)
        if raw is None:
            # Attempt inverse pair as a last resort.
            inv_raw = self._repo.get_rate(quote, base, on)
            if inv_raw is None or inv_raw == 0:
                raise FXRateUnavailableError(base, quote, on)
            return _ONE / Decimal(str(inv_raw))
        return Decimal(str(raw))

    # ------------------------------------------------------------------
    # Amount conversion
    # ------------------------------------------------------------------
    def convert(
        self,
        amount: Decimal | int | float | str,
        from_ccy: str,
        to_ccy: str,
        on: _dt.date,
        *,
        apply_spread: bool = False,
    ) -> Decimal:
        """Convert ``amount`` from ``from_ccy`` to ``to_ccy`` on ``on``.

        When ``apply_spread`` is true, the effective rate is reduced by
        ``fx_spread_bps / 2`` (so the caller receives less of the destination
        currency than the mid-market rate would yield). This is symmetric: the
        same cost is applied on the reverse leg.
        """
        if not isinstance(amount, Decimal):
            amount = Decimal(str(amount))
        if from_ccy == to_ccy:
            return amount

        rate = self.rate(from_ccy, to_ccy, on)
        if apply_spread:
            # Worsen the rate by half-spread (caller always loses half-spread
            # per leg regardless of direction).
            rate = rate * (_ONE - self._half_spread)
        return amount * rate

    # ------------------------------------------------------------------
    # Source-amount solver (spread applied on source side)
    # ------------------------------------------------------------------
    def convert_for_target(
        self,
        target_amount: Decimal | int | float | str,
        source_ccy: str,
        target_ccy: str,
        on: _dt.date,
        *,
        apply_spread: bool = True,
    ) -> Decimal:
        """Return the amount of ``source_ccy`` required to obtain exactly
        ``target_amount`` of ``target_ccy`` on ``on``.

        When ``apply_spread`` is true the spread cost is charged **on the
        source side**: callers must spend ``mid_source * (1 + half_spread)``
        to acquire ``target_amount``. This is the correct direction for
        ``Portfolio._ensure_cash`` where the portfolio is *buying* target
        currency by draining source currency — widening the spread must
        consume *more* source, never less.

        Contrast with :meth:`convert` which worsens the *to-side*
        (receive less target per unit source). Using ``convert`` to back-
        out a source amount would make wider spreads reduce the source
        requirement, which is the opposite of the real cost.
        """
        if not isinstance(target_amount, Decimal):
            target_amount = Decimal(str(target_amount))
        if source_ccy == target_ccy:
            return target_amount

        # mid rate source -> target
        rate = self.rate(source_ccy, target_ccy, on)
        if rate == 0:
            raise FXRateUnavailableError(source_ccy, target_ccy, on)
        source_mid = target_amount / rate
        if apply_spread:
            # Widening spread consumes more source currency.
            source_mid = source_mid * (_ONE + self._half_spread)
        return source_mid
