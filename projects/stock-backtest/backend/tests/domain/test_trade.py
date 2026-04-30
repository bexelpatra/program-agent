"""TradeFill.settlement_date 회귀 테스트 (TASK-212).

배경: run_id=96 실측에서 trades 의 time 이 모두 백테스트 실행 시각으로 기록되는 버그 발견.
원인은 backtest_runner.py 가 `getattr(fill, 'time', now)` fallback 을 썼고 TradeFill 에는
time 필드가 없었던 것. 본 테스트는 execute_rebalance 가 모든 fill 에 settlement_date 를
정확히 채우는지 회귀.
"""
from __future__ import annotations

from datetime import date
from decimal import Decimal

from app.domain.portfolio import Portfolio
from app.domain.trade import (
    DEFAULT_COMMISSION_BPS,
    TradeFill,
    execute_rebalance,
)

ZERO = Decimal("0")
ONE = Decimal("1")


def _allow_all_trading_days(_market: str, _d: date) -> bool:
    return True


class TestTradeFillSettlementDate:
    """execute_rebalance 가 생성하는 모든 TradeFill 의 settlement_date 가
    호출 시 인자로 전달한 rebalance_date 와 동일해야 함."""

    def test_buy_fill_has_settlement_date_equal_to_rebalance_date(self) -> None:
        """초기 진입 매수 (BUY 1건) — rebalance_date 가 settlement_date 로 채워진다."""
        p = Portfolio(base_currency="USD")
        p.deposit("USD", Decimal("10000"))

        target = {1: Decimal("1.0")}
        asset_meta = {1: ("US", "USD")}
        prices = {1: Decimal("500")}
        fx = {"USD": ONE}
        rebalance_date = date(2024, 3, 15)

        fills = execute_rebalance(
            p,
            target,
            asset_meta,
            prices,
            fx,
            rebalance_date,
            is_trading_day_fn=_allow_all_trading_days,
        )

        assert len(fills) >= 1
        buy_fills = [f for f in fills if f.side == "BUY"]
        assert len(buy_fills) == 1
        assert buy_fills[0].settlement_date == rebalance_date

    def test_sell_fill_has_settlement_date_equal_to_rebalance_date(self) -> None:
        """기존 보유 자산을 비중 0 으로 만들면 SELL 1건 — settlement_date 정확."""
        p = Portfolio(base_currency="USD")
        p.deposit("USD", Decimal("10000"))

        # 1회차: SPY 100% 매수
        first_date = date(2024, 3, 15)
        execute_rebalance(
            p,
            {1: Decimal("1.0")},
            {1: ("US", "USD")},
            {1: Decimal("500")},
            {"USD": ONE},
            first_date,
            is_trading_day_fn=_allow_all_trading_days,
        )
        assert 1 in p.positions

        # 2회차: SPY 0%, QQQ 100% — SPY 청산 (SELL) + QQQ 매수 (BUY).
        sell_date = date(2024, 4, 12)
        fills = execute_rebalance(
            p,
            {1: Decimal("0"), 2: Decimal("1.0")},
            {1: ("US", "USD"), 2: ("US", "USD")},
            {1: Decimal("510"), 2: Decimal("400")},
            {"USD": ONE},
            sell_date,
            is_trading_day_fn=_allow_all_trading_days,
        )

        sell_fills = [f for f in fills if f.side == "SELL"]
        buy_fills = [f for f in fills if f.side == "BUY"]
        assert len(sell_fills) == 1
        assert sell_fills[0].settlement_date == sell_date
        # 같은 리밸런싱의 BUY 도 같은 settlement_date
        assert len(buy_fills) == 1
        assert buy_fills[0].settlement_date == sell_date

    def test_rebalance_date_propagates_to_every_fill(self) -> None:
        """다중 자산 리밸런싱 — 모든 fill 의 settlement_date 가 동일."""
        p = Portfolio(base_currency="USD")
        p.deposit("USD", Decimal("100000"))

        target = {1: Decimal("0.4"), 2: Decimal("0.3"), 3: Decimal("0.3")}
        asset_meta = {
            1: ("US", "USD"),
            2: ("US", "USD"),
            3: ("US", "USD"),
        }
        prices = {1: Decimal("500"), 2: Decimal("400"), 3: Decimal("300")}
        fx = {"USD": ONE}
        rebalance_date = date(2024, 7, 1)

        fills = execute_rebalance(
            p,
            target,
            asset_meta,
            prices,
            fx,
            rebalance_date,
            is_trading_day_fn=_allow_all_trading_days,
        )

        assert len(fills) >= 3
        assert all(f.settlement_date == rebalance_date for f in fills)


class TestTradeFillFieldOrder:
    """TradeFill dataclass 필드 순서 회귀 — 7개 필드 (settlement_date 가 마지막)."""

    def test_construct_with_positional_args(self) -> None:
        """positional 7-arg 생성이 가능한 순서: asset_id, side, qty_filled,
        price, commission, currency, settlement_date."""
        fill = TradeFill(
            1,
            "BUY",
            Decimal("10"),
            Decimal("500"),
            Decimal("0.5"),
            "USD",
            date(2024, 1, 5),
        )
        assert fill.asset_id == 1
        assert fill.side == "BUY"
        assert fill.qty_filled == Decimal("10")
        assert fill.price == Decimal("500")
        assert fill.commission == Decimal("0.5")
        assert fill.currency == "USD"
        assert fill.settlement_date == date(2024, 1, 5)

    def test_default_commission_us_bps_unchanged(self) -> None:
        """이 회귀는 settlement_date 변경이 시장별 디폴트 수수료를 건드리지 않았는지."""
        assert DEFAULT_COMMISSION_BPS["US"] == Decimal("0.5")
        assert DEFAULT_COMMISSION_BPS["KR"] == Decimal("1.5")
        assert DEFAULT_COMMISSION_BPS["CRYPTO"] == Decimal("10")
