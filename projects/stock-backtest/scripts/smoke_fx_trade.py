"""Smoke script: verify Portfolio._ensure_cash emits an FX TradeEvent.

Simulates a KRW-based portfolio buying USD-denominated SPY; ``_ensure_cash``
must convert KRW -> USD and log an ``FXTradeEvent``.
"""
from __future__ import annotations

import datetime as _dt
from decimal import Decimal

from stock_backtest.backtest.fx import FXConverter
from stock_backtest.backtest.portfolio import Portfolio


def main() -> None:
    day = _dt.date(2026, 4, 14)
    # Mid rate: 1 USD = 1350 KRW  => KRW->USD = 1/1350
    fx = FXConverter(
        session=None,
        fx_spread_bps=20,
        rate_overrides={("USD", "KRW", day): Decimal("1350")},
    )
    pf = Portfolio.from_initial("KRW", {"KRW": Decimal("10000000"), "USD": Decimal("0")})

    # Buy 10 SPY @ 500 USD => need 5000 USD (+commission/slippage).
    pf.apply_trade(
        asset_id=1,
        side="BUY",
        qty=Decimal("10"),
        price=Decimal("500"),
        currency="USD",
        asset_class="etf_overseas",
        commission_bps=Decimal("15"),
        slippage_bps=Decimal("5"),
        fx=fx,
        base_ccy="KRW",
        date=day,
    )
    assert pf.fx_trades, "Expected at least one FX trade event"
    ev = pf.fx_trades[0]
    print(
        "FX event:",
        dict(
            date=ev.date,
            from_=ev.currency_from,
            to=ev.currency_to,
            qty=str(ev.qty),
            fx_rate=str(ev.fx_rate),
            spread_bps=str(ev.spread_bps),
        ),
    )
    assert ev.currency_from == "KRW"
    assert ev.currency_to == "USD"
    assert ev.spread_bps == Decimal("20")
    assert ev.qty > Decimal("0")
    # USD bucket should now hold roughly enough to fund the buy (approx 0 post-debit).
    print("cash_by_ccy after:", {k: str(v) for k, v in pf.cash_by_ccy.items()})
    print("positions:", list(pf.positions.keys()))
    print("OK")


if __name__ == "__main__":
    main()
