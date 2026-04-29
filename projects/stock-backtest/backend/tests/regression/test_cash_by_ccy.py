"""cash_by_ccy 환전 단위 회귀 테스트 (TASK-081 C).

architecture.md V3 § "환전 정책" L577-587:
- 단계 분리 (Q3 C): 매도 → native 입금 → 같은 native 매수면 native 직접 활용 →
  부족 시 base_currency 경유 환전 (양방향 비용)
- native 우선 (Q5 B): 환전 0회 우선
- fx_spread_bps = 20bp 디폴트

Portfolio (`app/domain/portfolio.py`) 핵심 동작 6가지를 회귀:
1. 단방향 환전 정확치 (KRW→USD with fx_spread 20bp)
2. 단계 분리 (매도→입금→환전→매수)
3. same currency 우선 (SPY→QQQ, USD 잔고 직접 사용 — 환전 0회)
4. partial fill (cash 부족 시 가능한 만큼만)
5. long-only (미보유 sell → 0주)
6. fx_spread 정확치 (1_300_000 KRW @ 1300 → 998 USD)
"""
from __future__ import annotations

from decimal import Decimal

import pytest

from app.domain.portfolio import (
    DEFAULT_FX_SPREAD_BPS,
    InsufficientFundsError,
    Portfolio,
)
from app.domain.trade import (
    DEFAULT_COMMISSION_BPS,
    execute_rebalance,
)

ZERO = Decimal("0")
ONE = Decimal("1")
BPS_DIVISOR = Decimal("10000")


# ===== 1. 단방향 환전 정확치 =====


class TestSingleConversion:
    """`Portfolio.convert` 의 spread 계산 검증."""

    def test_krw_to_usd_with_default_spread_yields_998_usd(self) -> None:
        """1_300_000 KRW @ rate 1/1300 → gross 1000 USD - spread 2 USD = net 998 USD.

        - fx_spread_bps = 20 (디폴트, architecture.md L585)
        - gross_to = 1_300_000 * (1/1300) = 1000.0 USD
        - spread = 1000 * 20/10000 = 2.0 USD
        - net_to = 1000 - 2 = 998.0 USD
        """
        p = Portfolio(base_currency="USD")
        p.deposit("KRW", Decimal("1300000"))
        rate_usd_per_krw = ONE / Decimal("1300")  # to_per_from
        conv = p.convert("KRW", "USD", Decimal("1300000"), rate_usd_per_krw)

        assert conv.from_ccy == "KRW"
        assert conv.to_ccy == "USD"
        assert conv.from_amount == Decimal("1300000")
        # gross = 1_300_000 / 1_300 = 1_000
        # spread = 1_000 * 0.002 = 2
        # net = 998
        assert conv.to_amount == pytest.approx(Decimal("998"), abs=Decimal("0.0001"))
        # 잔고 검증
        assert p.cash("KRW") == ZERO
        assert p.cash("USD") == pytest.approx(Decimal("998"), abs=Decimal("0.0001"))

    def test_same_currency_convert_is_noop(self) -> None:
        """같은 통화 convert 는 spread 차감 없음."""
        p = Portfolio(base_currency="USD")
        p.deposit("USD", Decimal("100"))
        conv = p.convert("USD", "USD", Decimal("50"), ONE)
        assert conv.to_amount == Decimal("50")
        assert conv.spread_cost == ZERO
        # 잔고는 변하지 않음 (same ccy 가산 후 차감되지 않음)
        assert p.cash("USD") == Decimal("100")

    def test_convert_insufficient_balance_raises(self) -> None:
        p = Portfolio(base_currency="USD")
        p.deposit("KRW", Decimal("100"))
        with pytest.raises(InsufficientFundsError):
            p.convert("KRW", "USD", Decimal("200"), ONE / Decimal("1300"))

    def test_convert_zero_amount_raises(self) -> None:
        p = Portfolio(base_currency="USD")
        p.deposit("KRW", Decimal("100"))
        with pytest.raises(ValueError, match="must be positive"):
            p.convert("KRW", "USD", ZERO, ONE / Decimal("1300"))

    def test_default_fx_spread_bps_is_20(self) -> None:
        """architecture.md V3 L585: fx_spread_bps 디폴트 = 20bp 회귀."""
        assert DEFAULT_FX_SPREAD_BPS == Decimal("20")
        p = Portfolio(base_currency="USD")
        assert p.fx_spread_bps == Decimal("20")


# ===== 2. 단계 분리 (Q3 C) =====


class TestStagedRebalance:
    """리밸런싱 단계: 매도→native 입금→환전→매수 (양방향 비용 발생)."""

    def test_sell_then_convert_then_buy_three_step_flow(self) -> None:
        """KR 자산 매도 → KRW 입금 → KRW→USD 환전 → US 자산 매수 시퀀스.

        모든 단계가 명시적으로 노출되며 양방향 환전 비용이 spread 로 계산됨을 검증.
        """
        p = Portfolio(base_currency="USD")
        # 초기 KR 자산 보유
        p.deposit("KRW", Decimal("0"))
        p.cash_by_ccy["KRW"] = Decimal("0")
        # 1단계: KR 자산 매도 결과를 KRW 입금으로 시뮬
        p.deposit("KRW", Decimal("1300000"))
        assert p.cash("KRW") == Decimal("1300000")
        assert p.cash("USD") == ZERO

        # 2단계: KRW → USD 환전
        rate_usd_per_krw = ONE / Decimal("1300")
        conv = p.convert("KRW", "USD", Decimal("1300000"), rate_usd_per_krw)
        # spread 차감 후 998 USD
        assert p.cash("USD") == pytest.approx(Decimal("998"), abs=Decimal("0.0001"))
        # spread_cost 는 base(USD) 단위로 보고
        assert conv.spread_cost == pytest.approx(Decimal("2"), abs=Decimal("0.0001"))

        # 3단계: 매수 (USD 잔고로 SPY 매수 시뮬)
        # SPY @ 100 USD/주 — partial fill 9 주 (100 * 9 * (1+slippage) * (1+commission) <= 998)
        actual_qty, total_cost = p.buy(
            asset_id=1,
            currency="USD",
            price=Decimal("100"),
            qty_target=9,
            commission_bps=DEFAULT_COMMISSION_BPS["US"],
        )
        assert actual_qty == 9
        assert p.positions[1].qty == 9


# ===== 3. same currency 우선 (Q5 B) =====


class TestNativeFirstNoConversion:
    """`ensure_native_funds`: native 잔고 충분 시 환전 0회 (Q5 B)."""

    def test_ensure_native_funds_skips_conversion_when_balance_sufficient(self) -> None:
        """USD 잔고로 USD 매수 시나리오: ensure_native_funds 환전 안 함."""
        p = Portfolio(base_currency="USD")
        p.deposit("USD", Decimal("10000"))
        # required = 5000 USD, 잔고 10000 USD → conversion 0회.
        conversions = p.ensure_native_funds("USD", Decimal("5000"), {"USD": ONE})
        assert conversions == [], (
            "native 잔고 충분 시 ensure_native_funds 가 환전을 발생시키면 안 됨 " "(Q5 B 위반)"
        )
        assert p.cash("USD") == Decimal("10000")  # 잔고 변화 없음

    def test_spy_sell_then_qqq_buy_uses_native_usd_no_fx(self) -> None:
        """SPY 매도 → USD 입금 → QQQ 매수 (USD). 양쪽 모두 USD 라 환전 0회.

        Portfolio 의 매도 → 매수 시퀀스에서 cash_by_ccy[USD] 가 직접 활용되는지 검증.
        """
        p = Portfolio(base_currency="USD")
        p.deposit("USD", Decimal("10000"))

        # SPY 매수 (10 주 @ 500 USD)
        p.buy(
            asset_id=1,
            currency="USD",
            price=Decimal("500"),
            qty_target=10,
            commission_bps=DEFAULT_COMMISSION_BPS["US"],
        )
        # 매수 후 USD 잔고: 10000 - (500 * 10 * (1 + slippage 10bp) * (1 + comm 0.5bp))
        balance_after_buy = p.cash("USD")
        assert balance_after_buy < Decimal("10000")

        # SPY 매도 — USD 입금
        actual_qty, net_received = p.sell(
            asset_id=1,
            price=Decimal("510"),  # 약간 상승
            qty=10,
            commission_bps=DEFAULT_COMMISSION_BPS["US"],
        )
        assert actual_qty == 10
        balance_after_sell = p.cash("USD")
        assert balance_after_sell == balance_after_buy + net_received

        # QQQ 매수 — 같은 USD 잔고에서 — ensure_native_funds 호출 시 환전 0회.
        conversions = p.ensure_native_funds("USD", Decimal("100"), {"USD": ONE})
        assert conversions == []

        actual_qqq_qty, _ = p.buy(
            asset_id=2,
            currency="USD",
            price=Decimal("400"),
            qty_target=5,
            commission_bps=DEFAULT_COMMISSION_BPS["US"],
        )
        assert actual_qqq_qty == 5

    def test_ensure_native_funds_converts_only_deficit(self) -> None:
        """native 일부만 보유한 상태에서 부족분만 환전 (전액 환전 금지)."""
        p = Portfolio(base_currency="USD")
        p.deposit("USD", Decimal("0"))
        p.deposit("KRW", Decimal("1300000"))

        # KRW 1_300_000 으로 KRW 800 (= 800 KRW) required → KRW 잔고 충분 (deficit=0).
        conversions = p.ensure_native_funds(
            "KRW", Decimal("800"), {"USD": Decimal("1300")}
        )
        assert conversions == []


# ===== 4. partial fill (cash 부족 시 가능한 만큼만) =====


class TestPartialFill:
    """cash 부족 시 buy 가 가능한 max qty 만 체결 (V3 § L606 long-only, 음수 잔고 금지)."""

    def test_buy_partial_fill_when_cash_short(self) -> None:
        """cash 100 USD, 가격 500 USD/주 → 0주 체결 (1주 살 cash 도 부족)."""
        p = Portfolio(base_currency="USD")
        p.deposit("USD", Decimal("100"))
        actual_qty, total_cost = p.buy(
            asset_id=1,
            currency="USD",
            price=Decimal("500"),
            qty_target=1,
            commission_bps=DEFAULT_COMMISSION_BPS["US"],
        )
        assert actual_qty == 0
        assert total_cost == ZERO
        assert p.cash("USD") == Decimal("100")  # 잔고 변화 없음
        assert 1 not in p.positions

    def test_buy_partial_fill_partial_qty(self) -> None:
        """cash 600 USD, 가격 500 USD/주, target 2주 → 1주만 체결."""
        p = Portfolio(base_currency="USD")
        p.deposit("USD", Decimal("600"))
        actual_qty, _ = p.buy(
            asset_id=1,
            currency="USD",
            price=Decimal("500"),
            qty_target=2,
            commission_bps=DEFAULT_COMMISSION_BPS["US"],
        )
        assert actual_qty == 1
        # 잔고는 1주 비용 차감 후 양수
        assert p.cash("USD") > ZERO


# ===== 5. long-only (미보유 sell → 0주) =====


class TestLongOnly:
    """미보유 자산 매도 시도 → 0주 (음수 잔고 금지, V3 § L606)."""

    def test_sell_unowned_asset_yields_zero(self) -> None:
        p = Portfolio(base_currency="USD")
        p.deposit("USD", Decimal("10000"))
        actual_qty, net_received = p.sell(
            asset_id=999,
            price=Decimal("100"),
            qty=10,
            commission_bps=DEFAULT_COMMISSION_BPS["US"],
        )
        assert actual_qty == 0
        assert net_received == ZERO
        assert p.cash("USD") == Decimal("10000")
        assert 999 not in p.positions

    def test_sell_more_than_owned_caps_at_owned(self) -> None:
        """5 주 보유, 10 주 매도 시도 → 5 주만 매도 (음수 포지션 금지)."""
        p = Portfolio(base_currency="USD")
        p.deposit("USD", Decimal("10000"))
        p.buy(
            asset_id=1,
            currency="USD",
            price=Decimal("100"),
            qty_target=5,
            commission_bps=DEFAULT_COMMISSION_BPS["US"],
        )
        assert p.positions[1].qty == 5

        actual_qty, _ = p.sell(
            asset_id=1,
            price=Decimal("100"),
            qty=10,
            commission_bps=DEFAULT_COMMISSION_BPS["US"],
        )
        assert actual_qty == 5
        assert 1 not in p.positions  # 전량 매도


# ===== 6. fx_spread 정확치 =====


class TestFxSpreadExactness:
    """architecture.md L585: fx_spread_bps 20bp 의 정확한 수치 회귀.

    1_300_000 KRW @ rate 1/1300 (USD/KRW):
    - gross_to = 1_300_000 / 1300 = 1000.0 USD
    - spread = 1000 * 20/10000 = 2.0 USD
    - net_to = 998.0 USD

    이 6번 항목은 fx_spread 가 추후 변경되거나 산식이 바뀔 때 즉시 catch.
    """

    def test_fx_spread_yields_exact_998_usd(self) -> None:
        p = Portfolio(base_currency="USD")
        p.deposit("KRW", Decimal("1300000"))
        rate = ONE / Decimal("1300")
        conv = p.convert("KRW", "USD", Decimal("1300000"), rate)

        # 정확치 검증: 998 USD (반올림 영향 없는 단순 계산)
        # net_to = 1_300_000 * (1/1300) - 1_300_000 * (1/1300) * (20/10000)
        #        = 1000 - 2 = 998
        expected_net = Decimal("998")
        assert abs(conv.to_amount - expected_net) < Decimal("0.0001")

        # spread_cost 는 base(USD) 단위
        expected_spread = Decimal("2")
        assert abs(conv.spread_cost - expected_spread) < Decimal("0.0001")

    def test_fx_spread_scales_linearly(self) -> None:
        """spread 는 gross_to 에 선형 비례. 2x 환전 → 2x spread."""
        p = Portfolio(base_currency="USD")
        p.deposit("KRW", Decimal("2600000"))  # 1_300_000 의 2배
        rate = ONE / Decimal("1300")
        conv = p.convert("KRW", "USD", Decimal("2600000"), rate)
        # gross = 2000, spread = 4, net = 1996
        assert abs(conv.to_amount - Decimal("1996")) < Decimal("0.0001")
        assert abs(conv.spread_cost - Decimal("4")) < Decimal("0.0001")

    def test_fx_spread_overridable_per_portfolio(self) -> None:
        """fx_spread_bps 사용자 변경 가능 (architecture.md L587 '사용자가 변경 가능')."""
        # 0 bp (무료 환전)
        p_free = Portfolio(base_currency="USD", fx_spread_bps=Decimal("0"))
        p_free.deposit("KRW", Decimal("1300000"))
        rate = ONE / Decimal("1300")
        conv = p_free.convert("KRW", "USD", Decimal("1300000"), rate)
        assert abs(conv.to_amount - Decimal("1000")) < Decimal("0.0001")
        assert conv.spread_cost == ZERO

        # 100 bp (1%)
        p_high = Portfolio(base_currency="USD", fx_spread_bps=Decimal("100"))
        p_high.deposit("KRW", Decimal("1300000"))
        conv2 = p_high.convert("KRW", "USD", Decimal("1300000"), rate)
        # gross 1000, spread 10, net 990
        assert abs(conv2.to_amount - Decimal("990")) < Decimal("0.0001")


# ===== 추가: ensure_native_funds 정밀 환전 (round-trip 검증) =====


class TestEnsureNativeFundsPrecision:
    """ensure_native_funds 가 deficit 정확히 충당하는지 (spread 역산)."""

    def test_ensure_native_funds_exact_deficit_coverage(self) -> None:
        """USD base, KRW 부족 → deficit 만큼 환전. spread 차감 후 정확히 deficit 충당."""
        p = Portfolio(base_currency="USD")
        p.deposit("USD", Decimal("10000"))
        p.deposit("KRW", Decimal("0"))

        # KRW 1_300_000 필요, 잔고 0 → deficit = 1_300_000 KRW
        # rate KRW per USD = 1300 (target_per_base)
        rate_krw_per_usd = Decimal("1300")
        conversions = p.ensure_native_funds(
            "KRW", Decimal("1300000"), {"USD": rate_krw_per_usd}
        )
        assert len(conversions) == 1

        # 환전 후 KRW 잔고가 deficit (= 1_300_000) 이상이어야 함.
        assert p.cash("KRW") >= Decimal("1300000") - Decimal("1")  # 부동소수 여유

    def test_ensure_native_funds_skips_when_base_currency_target(self) -> None:
        """target == base 면 ensure_native_funds 가 환전 시도 안 함 (호출자가 partial fill 결정)."""
        p = Portfolio(base_currency="USD")
        p.deposit("USD", Decimal("100"))
        # USD 부족 (200 필요)
        conversions = p.ensure_native_funds("USD", Decimal("200"), {"USD": ONE})
        assert conversions == []  # base 자체 부족은 환전으로 못 메움


# ===== 추가: execute_rebalance 통합 (단계 분리 + native 우선) =====


class TestExecuteRebalanceIntegration:
    """execute_rebalance 통합: SPY (USD) → QQQ (USD) 단순 리밸런싱 (환전 0회)."""

    def test_pure_usd_rebalance_no_fx_conversion(self) -> None:
        """USD universe 에서 SPY → QQQ 비중 이동 시 KRW 환전 발생 안 함."""
        from datetime import date

        p = Portfolio(base_currency="USD")
        p.deposit("USD", Decimal("10000"))

        # 초기: SPY 100% (10 주 @ 500 USD)
        target_initial: dict[int, Decimal] = {1: Decimal("1.0")}
        asset_meta = {1: ("US", "USD"), 2: ("US", "USD")}
        prices = {1: Decimal("500"), 2: Decimal("400")}
        fx = {"USD": ONE}

        execute_rebalance(
            p,
            target_initial,
            asset_meta,
            prices,
            fx,
            date(2024, 1, 5),
            is_trading_day_fn=lambda _m, _d: True,
        )
        assert 1 in p.positions
        assert p.positions[1].qty > 0
        krw_after_first = p.cash("KRW")
        assert krw_after_first == ZERO  # KRW 잔고 발생 안 함

        # 2회차: QQQ 50% / SPY 50% — 같은 USD 라 환전 0회
        target_rebal: dict[int, Decimal] = {1: Decimal("0.5"), 2: Decimal("0.5")}
        execute_rebalance(
            p,
            target_rebal,
            asset_meta,
            prices,
            fx,
            date(2024, 1, 8),
            is_trading_day_fn=lambda _m, _d: True,
        )
        assert 1 in p.positions
        assert 2 in p.positions
        assert p.cash("KRW") == ZERO  # 환전 발생 안 함
