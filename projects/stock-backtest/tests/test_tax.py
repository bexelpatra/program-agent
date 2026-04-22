"""Unit tests for ``stock_backtest.backtest.tax``.

Covers the scenarios enumerated in TASK-036:

1. Overseas realized gain below deduction → 0 tax.
2. Overseas realized gain above deduction → (gain - deduction) * 22%.
3. Intra-year loss then gain nets within the overseas bucket.
4. Domestic equity ETF capital gain → 0 tax.
5. Domestic bond ETF capital gain → 15.4%.
6. Dividend → 15.4% withholding.
7. Crypto when ``crypto_enabled=false`` → 0 tax.
8. Year-end roll-over resets state.
9. ``tax.enabled=false`` → :class:`NoopTax` charges nothing.
"""

from __future__ import annotations

from datetime import date
from decimal import Decimal

import pytest

from stock_backtest.backtest.tax import (
    KrResidentTax,
    NoopTax,
    RealizedTrade,
    TaxYearState,
    build_tax_policy,
)
from stock_backtest.config import Settings


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


KR_PROFILE = {
    "overseas_capital_gains_rate": 0.22,
    "overseas_annual_deduction_krw": 2_500_000,
    "overseas_dividend_rate": 0.154,
    "crypto_enabled": True,
    "crypto_capital_gains_rate": 0.22,
    "crypto_annual_deduction_krw": 2_500_000,
}


@pytest.fixture
def policy() -> KrResidentTax:
    return KrResidentTax(KR_PROFILE)


@pytest.fixture
def state() -> TaxYearState:
    return TaxYearState(year=2026)


def _sell(
    asset_class: str,
    proceeds: int,
    cost: int,
    *,
    trade_date: date = date(2026, 5, 1),
) -> RealizedTrade:
    return RealizedTrade(
        asset_id=1,
        asset_class=asset_class,  # type: ignore[arg-type]
        proceeds_krw=Decimal(proceeds),
        cost_basis_krw=Decimal(cost),
        trade_date=trade_date,
        is_dividend=False,
    )


def _div(
    asset_class: str,
    amount: int,
    *,
    trade_date: date = date(2026, 5, 1),
) -> RealizedTrade:
    return RealizedTrade(
        asset_id=1,
        asset_class=asset_class,  # type: ignore[arg-type]
        proceeds_krw=Decimal(amount),
        cost_basis_krw=Decimal(0),
        trade_date=trade_date,
        is_dividend=True,
    )


# ---------------------------------------------------------------------------
# 1. Overseas below deduction
# ---------------------------------------------------------------------------


def test_overseas_gain_below_deduction_is_untaxed(
    policy: KrResidentTax, state: TaxYearState
) -> None:
    trade = _sell("overseas_equity", proceeds=3_000_000, cost=1_000_000)  # gain 2M
    tax = policy.apply_realized_gain(trade, state)
    assert tax == Decimal(0)
    assert state.cash_tax_paid == Decimal(0)
    assert state.realized_capital_gains_by_class["overseas"] == Decimal(2_000_000)


# ---------------------------------------------------------------------------
# 2. Overseas above deduction
# ---------------------------------------------------------------------------


def test_overseas_gain_above_deduction_uses_22pct(
    policy: KrResidentTax, state: TaxYearState
) -> None:
    trade = _sell("overseas_etf", proceeds=6_000_000, cost=1_000_000)  # gain 5M
    tax = policy.apply_realized_gain(trade, state)
    # (5M - 2.5M) * 22% = 550,000
    assert tax == Decimal(550_000)
    assert state.cash_tax_paid == Decimal(550_000)


# ---------------------------------------------------------------------------
# 3. Loss then gain within same year
# ---------------------------------------------------------------------------


def test_overseas_loss_then_gain_nets_within_year(
    policy: KrResidentTax, state: TaxYearState
) -> None:
    # First: realized loss of 1M (overseas_equity).
    loss = _sell("overseas_equity", proceeds=0, cost=1_000_000)
    tax_loss = policy.apply_realized_gain(loss, state)
    assert tax_loss == Decimal(0)
    assert state.cash_tax_paid == Decimal(0)

    # Then: realized gain of 4M. Cumulative = +3M → taxable = 500k @ 22% = 110k.
    gain = _sell("overseas_equity", proceeds=5_000_000, cost=1_000_000)
    tax_gain = policy.apply_realized_gain(gain, state)
    assert tax_gain == Decimal(110_000)
    assert state.cash_tax_paid == Decimal(110_000)
    assert state.realized_capital_gains_by_class["overseas"] == Decimal(3_000_000)


# ---------------------------------------------------------------------------
# 4. Domestic equity ETF is tax-free
# ---------------------------------------------------------------------------


def test_kr_equity_etf_capital_gain_is_tax_free(
    policy: KrResidentTax, state: TaxYearState
) -> None:
    trade = _sell("kr_equity_etf", proceeds=10_000_000, cost=1_000_000)
    tax = policy.apply_realized_gain(trade, state)
    assert tax == Decimal(0)
    assert state.cash_tax_paid == Decimal(0)
    assert state.realized_capital_gains_by_class["tax_free"] == Decimal(9_000_000)


# ---------------------------------------------------------------------------
# 5. Domestic bond ETF: 15.4%
# ---------------------------------------------------------------------------


def test_kr_bond_etf_capital_gain_taxed_at_15_4(
    policy: KrResidentTax, state: TaxYearState
) -> None:
    trade = _sell("kr_bond_etf", proceeds=2_000_000, cost=1_000_000)  # +1M
    tax = policy.apply_realized_gain(trade, state)
    # 1_000_000 * 0.154 = 154_000
    assert tax == Decimal(154_000)
    assert state.cash_tax_paid == Decimal(154_000)


def test_kr_bond_etf_loss_is_not_refundable(
    policy: KrResidentTax, state: TaxYearState
) -> None:
    loss = _sell("kr_bond_etf", proceeds=0, cost=1_000_000)  # -1M
    tax = policy.apply_realized_gain(loss, state)
    assert tax == Decimal(0)
    assert state.cash_tax_paid == Decimal(0)


# ---------------------------------------------------------------------------
# 6. Dividend withholding
# ---------------------------------------------------------------------------


def test_dividend_withholds_15_4(policy: KrResidentTax, state: TaxYearState) -> None:
    trade = _div("overseas_equity", amount=1_000_000)
    tax = policy.apply_dividend(trade, state)
    assert tax == Decimal(154_000)
    assert state.dividend_taxed == Decimal(154_000)
    assert state.cash_tax_paid == Decimal(154_000)


def test_apply_dividend_rejects_non_dividend_trade(
    policy: KrResidentTax, state: TaxYearState
) -> None:
    trade = _sell("overseas_equity", proceeds=1_000_000, cost=0)
    with pytest.raises(ValueError):
        policy.apply_dividend(trade, state)


def test_apply_realized_gain_rejects_dividend_trade(
    policy: KrResidentTax, state: TaxYearState
) -> None:
    trade = _div("overseas_equity", amount=1_000_000)
    with pytest.raises(ValueError):
        policy.apply_realized_gain(trade, state)


# ---------------------------------------------------------------------------
# 7. Crypto disabled → untaxed
# ---------------------------------------------------------------------------


def test_crypto_disabled_does_not_tax() -> None:
    profile = {**KR_PROFILE, "crypto_enabled": False}
    policy = KrResidentTax(profile)
    state = TaxYearState(year=2026)
    trade = _sell("crypto", proceeds=10_000_000, cost=1_000_000)  # +9M
    tax = policy.apply_realized_gain(trade, state)
    assert tax == Decimal(0)
    assert state.cash_tax_paid == Decimal(0)


def test_crypto_enabled_uses_22pct_with_deduction(
    policy: KrResidentTax, state: TaxYearState
) -> None:
    trade = _sell("crypto", proceeds=5_000_000, cost=0)  # +5M
    tax = policy.apply_realized_gain(trade, state)
    # (5M - 2.5M) * 22% = 550k
    assert tax == Decimal(550_000)


# ---------------------------------------------------------------------------
# 8. Year-end rollover
# ---------------------------------------------------------------------------


def test_on_year_end_resets_state(policy: KrResidentTax, state: TaxYearState) -> None:
    gain = _sell("overseas_equity", proceeds=6_000_000, cost=1_000_000)
    policy.apply_realized_gain(gain, state)
    assert state.cash_tax_paid > Decimal(0)
    assert state.realized_capital_gains_by_class["overseas"] == Decimal(5_000_000)

    new_state = policy.on_year_end(state)
    assert new_state.year == state.year + 1
    assert new_state.cash_tax_paid == Decimal(0)
    assert new_state.dividend_taxed == Decimal(0)
    for bucket in new_state.realized_capital_gains_by_class.values():
        assert bucket == Decimal(0)


# ---------------------------------------------------------------------------
# 9. NoopTax when disabled
# ---------------------------------------------------------------------------


def test_noop_tax_charges_nothing() -> None:
    policy = NoopTax()
    state = TaxYearState(year=2026)

    cap = _sell("overseas_equity", proceeds=100_000_000, cost=0)
    div = _div("overseas_equity", amount=100_000_000)

    assert policy.apply_realized_gain(cap, state) == Decimal(0)
    assert policy.apply_dividend(div, state) == Decimal(0)
    assert state.cash_tax_paid == Decimal(0)

    rolled = policy.on_year_end(state)
    assert rolled.year == 2027


def test_build_tax_policy_respects_enabled_flag() -> None:
    raw = {
        "base_currency": "USD",
        "market_mode": "STOCK",
        "tax": {
            "enabled": False,
            "profile": "kr_resident",
            "profiles": {
                "kr_resident": KR_PROFILE,
                "none": {},
            },
        },
    }
    settings = Settings.model_validate(raw)
    policy = build_tax_policy(settings)
    assert isinstance(policy, NoopTax)


def test_build_tax_policy_returns_kr_resident_when_enabled() -> None:
    raw = {
        "base_currency": "USD",
        "market_mode": "STOCK",
        "tax": {
            "enabled": True,
            "profile": "kr_resident",
            "profiles": {
                "kr_resident": KR_PROFILE,
            },
        },
    }
    settings = Settings.model_validate(raw)
    policy = build_tax_policy(settings)
    assert isinstance(policy, KrResidentTax)


def test_unknown_asset_class_raises(policy: KrResidentTax, state: TaxYearState) -> None:
    bad = RealizedTrade(
        asset_id=1,
        asset_class="unknown_class",  # type: ignore[arg-type]
        proceeds_krw=Decimal(1_000_000),
        cost_basis_krw=Decimal(0),
        trade_date=date(2026, 5, 1),
    )
    with pytest.raises(ValueError):
        policy.apply_realized_gain(bad, state)
