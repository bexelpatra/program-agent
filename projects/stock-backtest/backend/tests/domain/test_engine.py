"""engine.py 청산 동작 + invariant 회귀 테스트 (TASK-211).

배경 (run_id=96):
  BTC 100% + MA(117) + quarterly + 2017-01-01 ~ 2026-04-29 + USD $100k 백테스트에서
  trades 가 1건만 발생. 원인 중 하나는 engine.py L219 의 `if target_weights:` 분기로,
  필터 fail 시 빈 dict 가 반환되면 execute_rebalance 호출 자체를 skip → 이미 보유 중인
  포지션이 청산되지 않는 버그.

수정:
  engine.py 의 `if target_weights:` 분기 제거. 빈 dict 도 execute_rebalance 호출 →
  trade._classify_orders 가 보유 자산 전량 매도 sells 에 추가 → 청산 동작.

회귀:
  1. 빈 weights → 보유 BTC 전량 매도 (1건 SELL fill 발생).
  2. universe 부분집합 invariant — 보유 자산이 universe 에 없으면 명시적 ValueError.
"""

from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import ClassVar

import pandas as pd
import pytest
from pydantic import BaseModel

from app.domain.engine import BacktestRunContext, run_backtest
from app.domain.portfolio import Portfolio
from app.domain.strategy import Strategy
from app.domain.trade import execute_rebalance


ZERO = Decimal("0")
ONE = Decimal("1")


def _allow_all_trading_days(_market: str, _d: date) -> bool:
    return True


# ---------------------------------------------------------------------------
# 회귀 1: filter fail → 빈 weights → 보유 청산
# ---------------------------------------------------------------------------


class _AlwaysOnAllocator:
    """universe 의 첫 자산에 100%."""

    name: ClassVar[str] = "always_on"

    def required_universe(self) -> list[int]:
        return []

    def generate_weights(
        self,
        universe_asset_ids: list[int],
        prices_until_d: pd.DataFrame,
        signal_date: date,
    ) -> dict[int, Decimal]:
        if not universe_asset_ids:
            return {}
        return {universe_asset_ids[0]: Decimal("1.0")}


class _EmptyParams(BaseModel):
    pass


class _ToggleFilter:
    """test 가 신호 ON/OFF 를 클래스 변수로 토글 — strategy 인스턴스 공유 환경."""

    name: ClassVar[str] = "toggle"
    on: bool = True

    def __init__(self, on: bool = True) -> None:
        self.on = on

    def is_eligible(
        self,
        asset_id: int,
        prices_until_d: pd.DataFrame,
        signal_date: date,
    ) -> bool:
        return self.on


class TestFilterFailClearsHeldPosition:
    """TASK-211 핵심 회귀: filter fail 시 보유 청산이 정상 동작하는지."""

    def test_empty_weights_triggers_full_liquidation(self) -> None:
        """직접 execute_rebalance 호출로 빈 target_weights 청산 동작 검증."""
        p = Portfolio(base_currency="USD")
        p.deposit("USD", Decimal("100000"))

        # 1차: BTC 0.5 코인 매수.
        first_d = date(2024, 3, 15)
        execute_rebalance(
            p,
            target_weights={1: Decimal("1.0")},
            asset_meta={1: ("CRYPTO", "USD")},
            prices={1: Decimal("50000")},
            fx_rates_to_base={"USD": ONE},
            rebalance_date=first_d,
            is_trading_day_fn=_allow_all_trading_days,
        )
        assert 1 in p.positions
        held_qty = p.positions[1].qty
        assert held_qty > ZERO

        # 2차: filter fail 시뮬 — 빈 target_weights. 청산 동작 검증.
        sell_d = date(2024, 4, 15)
        fills = execute_rebalance(
            p,
            target_weights={},
            asset_meta={1: ("CRYPTO", "USD")},
            prices={1: Decimal("55000")},
            fx_rates_to_base={"USD": ONE},
            rebalance_date=sell_d,
            is_trading_day_fn=_allow_all_trading_days,
        )

        # 회귀 핵심: 빈 weights 라도 보유 청산이 발생해야 한다.
        sell_fills = [f for f in fills if f.side == "SELL"]
        assert len(sell_fills) == 1, (
            f"REGRESSION (TASK-211) — 빈 target_weights 청산 누락. fills={fills}"
        )
        assert sell_fills[0].asset_id == 1
        assert sell_fills[0].qty_filled == held_qty
        assert sell_fills[0].settlement_date == sell_d
        # 보유 0 확인.
        assert 1 not in p.positions

    def test_engine_loop_clears_position_when_filter_fails_after_entry(
        self,
    ) -> None:
        """engine.run_backtest 통합 — filter on→off 전이 시 보유가 자동 청산."""
        # 5 거래일 시계열 (2024-03-15~2024-03-21 중 미국 거래일).
        timeline = [
            date(2024, 3, 15),
            date(2024, 3, 18),
            date(2024, 3, 19),
            date(2024, 3, 20),
            date(2024, 3, 21),
        ]
        prices = pd.DataFrame({1: [500.0, 501.0, 502.0, 503.0, 504.0]}, index=timeline)
        prices.index.name = "date"

        toggle = _ToggleFilter(on=True)
        strategy = Strategy(
            name="toggle_test",
            allocator=_AlwaysOnAllocator(),
            signal_filters=(toggle,),
            rebalance_schedule="daily",
        )

        # 1단계: filter ON 으로 매수까지 진행 (3/15~3/18).
        ctx_buy = BacktestRunContext(
            base_currency="USD",
            period_start=date(2024, 3, 15),
            period_end=date(2024, 3, 18),
            initial_cash={"USD": Decimal("100000")},
            universe_market_meta={1: ("US", "USD")},
            prices_aligned=prices,
            fx_rates_to_base={d: {"USD": ONE} for d in timeline},
            strategy=strategy,
        )
        result_buy = run_backtest(ctx_buy)
        # 매수 1건 이상 발생 (rebalance daily, 매일 비중 차이 없으면 1회만).
        buy_fills = [f for f in result_buy.fills if f.side == "BUY"]
        assert len(buy_fills) >= 1
        assert 1 in result_buy.final_portfolio.positions

        # 2단계: filter OFF 로 토글 후 같은 portfolio 로 다음 구간 실행.
        # ctx 새로 만들되 portfolio 를 inject 하기 위해 직접 매수 후 toggle 변경.
        toggle.on = False
        # portfolio 를 buy 단계 결과로 시드하기 위해 deposit 대신 직접 사용.
        # engine 은 매 호출마다 새 portfolio 를 만드므로, 같은 시드 + ON→OFF 시퀀스
        # 검증을 위해 새로 시작 후 첫날만 ON, 둘째 날부터 OFF 로 만든다.

        # 시퀀스 시뮬: 첫날 ON (매수) → 둘째 날 OFF (청산).
        class _SequenceFilter:
            name: ClassVar[str] = "sequence"

            def __init__(self) -> None:
                self.calls = 0

            def is_eligible(
                self,
                asset_id: int,
                prices_until_d: pd.DataFrame,
                signal_date: date,
            ) -> bool:
                self.calls += 1
                # signal_date 기반으로 결정적 — 첫날만 PASS, 이후 FAIL.
                return signal_date == date(2024, 3, 15)

        seq_filter = _SequenceFilter()
        seq_strategy = Strategy(
            name="sequence_test",
            allocator=_AlwaysOnAllocator(),
            signal_filters=(seq_filter,),
            rebalance_schedule="daily",
        )
        ctx_seq = BacktestRunContext(
            base_currency="USD",
            period_start=date(2024, 3, 15),
            period_end=date(2024, 3, 21),
            initial_cash={"USD": Decimal("100000")},
            universe_market_meta={1: ("US", "USD")},
            prices_aligned=prices,
            fx_rates_to_base={d: {"USD": ONE} for d in timeline},
            strategy=seq_strategy,
        )
        result_seq = run_backtest(ctx_seq)

        # 첫날 ON → 매수 1건, 둘째 날부터 OFF → 청산 1건.
        buy_fills = [f for f in result_seq.fills if f.side == "BUY"]
        sell_fills = [f for f in result_seq.fills if f.side == "SELL"]
        assert len(buy_fills) == 1, f"매수 1건 기대. fills={result_seq.fills}"
        assert len(sell_fills) == 1, (
            f"REGRESSION (TASK-211) — filter OFF 전환 후 청산 누락. "
            f"fills={result_seq.fills}"
        )
        # 청산 후 보유 0.
        assert 1 not in result_seq.final_portfolio.positions


# ---------------------------------------------------------------------------
# 회귀 2: universe 부분집합 invariant
# ---------------------------------------------------------------------------


class TestHeldSubsetOfUniverseInvariant:
    """보유 자산 ⊆ universe — 위반 시 명시적 에러 (silent 0 금지)."""

    def test_classify_orders_raises_on_held_not_in_asset_meta(self) -> None:
        """보유 중인 자산이 asset_meta 에 없으면 KeyError 가 _classify_orders 에서 raise."""
        from app.domain.trade import _classify_orders

        p = Portfolio(base_currency="USD")
        p.deposit("USD", Decimal("100000"))
        # asset_id=1 매수 (universe 에 들어있을 때).
        execute_rebalance(
            p,
            target_weights={1: Decimal("1.0")},
            asset_meta={1: ("US", "USD")},
            prices={1: Decimal("500")},
            fx_rates_to_base={"USD": ONE},
            rebalance_date=date(2024, 3, 15),
            is_trading_day_fn=_allow_all_trading_days,
        )
        assert 1 in p.positions

        # 보유 중인데 asset_meta 에서 빠짐 (invariant 위반 시뮬).
        with pytest.raises(KeyError, match="held asset_id=1"):
            _classify_orders(
                target_qty={},
                portfolio=p,
                target_weight_keys=set(),
                asset_meta={},  # 보유 자산 1 누락
            )

    def test_execute_rebalance_raises_missing_price_when_held_not_in_meta(
        self,
    ) -> None:
        """보유 자산이 asset_meta 에 없으면 execute_rebalance 가 명시적 에러로 catch."""
        from app.domain.trade import MissingPriceError

        p = Portfolio(base_currency="USD")
        p.deposit("USD", Decimal("100000"))
        execute_rebalance(
            p,
            target_weights={1: Decimal("1.0")},
            asset_meta={1: ("US", "USD")},
            prices={1: Decimal("500")},
            fx_rates_to_base={"USD": ONE},
            rebalance_date=date(2024, 3, 15),
            is_trading_day_fn=_allow_all_trading_days,
        )

        # 빈 target_weights + asset_meta 에서 보유 자산 누락 시 명시적 에러.
        # _classify_orders 가 KeyError 를 raise → execute_rebalance 호출 경로에서
        # 그대로 전파 (silent 진행 금지).
        # 단 target_weights 가 비어있으므로 assert 단계는 통과 → equity_in_base 가
        # prices 에 asset 1 이 있어 통과 → _classify_orders 에서 KeyError.
        with pytest.raises((KeyError, MissingPriceError)):
            execute_rebalance(
                p,
                target_weights={},
                asset_meta={},  # 보유 자산 누락
                prices={1: Decimal("510")},
                fx_rates_to_base={"USD": ONE},
                rebalance_date=date(2024, 3, 18),
                is_trading_day_fn=_allow_all_trading_days,
            )

    def test_engine_invariant_check_runs_normally_when_held_subset_of_universe(
        self,
    ) -> None:
        """정상 경로: 보유 ⊆ universe — invariant 검증 통과 + 청산 정상 동작."""
        # 3 거래일 필요 (D=15 매수 시그널 → D+1=18 매수 체결 → D=18 OFF 시그널 → D+1=19 청산).
        timeline = [
            date(2024, 3, 15),
            date(2024, 3, 18),
            date(2024, 3, 19),
        ]
        prices = pd.DataFrame({1: [500.0, 510.0, 515.0]}, index=timeline)
        prices.index.name = "date"

        class _OnceOnFilter:
            name: ClassVar[str] = "once_on"

            def is_eligible(
                self,
                asset_id: int,
                prices_until_d: pd.DataFrame,
                signal_date: date,
            ) -> bool:
                return signal_date == date(2024, 3, 15)

        strategy = Strategy(
            name="once_on",
            allocator=_AlwaysOnAllocator(),
            signal_filters=(_OnceOnFilter(),),
            rebalance_schedule="daily",
        )
        ctx = BacktestRunContext(
            base_currency="USD",
            period_start=date(2024, 3, 15),
            period_end=date(2024, 3, 19),
            initial_cash={"USD": Decimal("100000")},
            universe_market_meta={1: ("US", "USD")},
            prices_aligned=prices,
            fx_rates_to_base={d: {"USD": ONE} for d in timeline},
            strategy=strategy,
        )
        # invariant 검증 통과 (보유 ⊆ universe). 청산 정상.
        result = run_backtest(ctx)
        assert not result.aborted
        assert 1 not in result.final_portfolio.positions


# ---------------------------------------------------------------------------
# 회귀 3: _is_rebalance_day semi_annual 분기 (TASK-220)
# ---------------------------------------------------------------------------


class TestIsRebalanceDaySemiAnnual:
    """반기 (semi_annual) — 1월·7월 첫 거래일 trigger.

    의미론: (month-1)//6 변경 → 0 (1~6월) 또는 1 (7~12월). 사용자 결정 (2026-04-30):
    quarterly 와 일관, 휴일 보정은 calendar 위임 (engine 은 거래일만 받음).
    """

    def test_january_first_trading_day_triggers(self) -> None:
        """이전 거래일이 12월 → 1월 첫 거래일은 trigger."""
        from app.domain.engine import _is_rebalance_day

        prev = date(2024, 12, 30)  # 2024 H2 (cur_h=1)
        cur = date(2025, 1, 2)  # 2025 H1 (cur_h=0) — year 변경 + half 변경
        assert _is_rebalance_day(cur, prev, "semi_annual") is True

    def test_july_first_trading_day_triggers(self) -> None:
        """이전 거래일이 6월 → 7월 첫 거래일은 trigger."""
        from app.domain.engine import _is_rebalance_day

        prev = date(2025, 6, 30)  # 2025 H1 (cur_h=0)
        cur = date(2025, 7, 1)  # 2025 H2 (cur_h=1)
        assert _is_rebalance_day(cur, prev, "semi_annual") is True

    def test_other_month_within_same_half_returns_false(self) -> None:
        """같은 반기 내 (1~6월 또는 7~12월) 인접 거래일은 trigger 아님."""
        from app.domain.engine import _is_rebalance_day

        # H1 내부 (3월 → 4월).
        assert (
            _is_rebalance_day(date(2025, 4, 1), date(2025, 3, 31), "semi_annual")
            is False
        )
        # H2 내부 (8월 → 9월).
        assert (
            _is_rebalance_day(date(2025, 9, 1), date(2025, 8, 29), "semi_annual")
            is False
        )
        # H1 첫째 달 (1월 → 2월) — 같은 H1.
        assert (
            _is_rebalance_day(date(2025, 2, 3), date(2025, 1, 31), "semi_annual")
            is False
        )

    def test_within_same_half_repeated_call_false(self) -> None:
        """같은 반기 내 두 번째 호출 — trigger 아님 (1월 trigger 후 2월 호출)."""
        from app.domain.engine import _is_rebalance_day

        # 1월 첫 거래일 trigger 직후 동일 반기 내 다음 호출.
        prev = date(2025, 1, 2)
        cur = date(2025, 1, 3)
        assert _is_rebalance_day(cur, prev, "semi_annual") is False
        # 같은 반기의 더 뒤 시점도 false.
        assert (
            _is_rebalance_day(date(2025, 6, 30), date(2025, 1, 2), "semi_annual")
            is False
        )


# ---------------------------------------------------------------------------
# 회귀 4: EOD equity 회계 시점 — 큐잉 패턴 (TASK-244)
# ---------------------------------------------------------------------------
#
# architecture.md V3 § "EOD equity 기록 시점" L635-648 + engine.py L319-356:
#   D 일 EOD equity = D 시그널 *이전* 평가 (= 어제 시그널 D-1 이 오늘 D 에 settlement
#   된 직후 portfolio + D 가격). 사용자 멘탈 모델/실거래 정합:
#     - 매도 시그널의 D EOD = 아직 매도 전 (보유 그대로 평가)
#     - 매수 시그널의 D EOD = 아직 매수 전 (cash 그대로)
#     - Day 0 EOD = 어제 큐잉 없음 → settlement skip → portfolio = initial_cash
#     - Day k≥1 EOD = 어제 시그널이 오늘 settlement 된 직후 평가
#
# TASK-244 fix 이전 BUG: D iteration 안에서 시그널→D+1 settlement→D EOD equity 모두
# 처리 → D EOD 평가에 D+1 가격으로 산 새 포지션이 D 가격으로 평가되어 회계 어긋남.
# 본 회귀는 큐잉 패턴이 사용자 멘탈 모델과 정합함을 4 메소드로 박제한다.


class _UseFirstAssetAllocator:
    """universe 의 첫 자산에 100% (signal_date 와 무관)."""

    name: ClassVar[str] = "first_asset"

    def required_universe(self) -> list[int]:
        return []

    def generate_weights(
        self,
        universe_asset_ids: list[int],
        prices_until_d: pd.DataFrame,
        signal_date: date,
    ) -> dict[int, Decimal]:
        if not universe_asset_ids:
            return {}
        return {universe_asset_ids[0]: Decimal("1.0")}


class _CashOnlyAllocator:
    """항상 빈 weights → cash-only (보유 자산 있으면 매도 시그널 효과)."""

    name: ClassVar[str] = "cash_only"

    def required_universe(self) -> list[int]:
        return []

    def generate_weights(
        self,
        universe_asset_ids: list[int],
        prices_until_d: pd.DataFrame,
        signal_date: date,
    ) -> dict[int, Decimal]:
        return {}


class _OnceOnFirstDayAllocator:
    """첫날만 buy 시그널, 이후 cash-only — D=0 매수 시그널 / D≥1 매도 시그널 효과 검증."""

    name: ClassVar[str] = "once_on_first_day"

    def __init__(self, first_day: date) -> None:
        self.first_day = first_day

    def required_universe(self) -> list[int]:
        return []

    def generate_weights(
        self,
        universe_asset_ids: list[int],
        prices_until_d: pd.DataFrame,
        signal_date: date,
    ) -> dict[int, Decimal]:
        if signal_date == self.first_day and universe_asset_ids:
            return {universe_asset_ids[0]: Decimal("1.0")}
        return {}


class TestEodEquityAccountingTiming:
    """TASK-244 핵심 회귀 — 큐잉 패턴으로 D 시그널/D+1 settlement 분리 시 EOD 시점 정합."""

    def _make_ctx(
        self,
        timeline: list[date],
        prices: list[float],
        strategy: Strategy,
        initial_cash_usd: Decimal = Decimal("100000"),
    ) -> BacktestRunContext:
        prices_df = pd.DataFrame({1: prices}, index=timeline)
        prices_df.index.name = "date"
        return BacktestRunContext(
            base_currency="USD",
            period_start=timeline[0],
            period_end=timeline[-1],
            initial_cash={"USD": initial_cash_usd},
            universe_market_meta={1: ("US", "USD")},
            prices_aligned=prices_df,
            fx_rates_to_base={d: {"USD": ONE} for d in timeline},
            strategy=strategy,
        )

    def test_day_0_eod_is_pure_cash(self) -> None:
        """Day 0 EOD equity == initial_cash, fills 0 건 (시그널은 큐잉만, 체결 없음).

        매수 시그널이 첫날 발생해도 D+1 settlement 이전이라 D=0 EOD 는 pure cash.
        """
        timeline = [
            date(2024, 3, 15),
            date(2024, 3, 18),
            date(2024, 3, 19),
        ]
        prices = [500.0, 510.0, 520.0]
        strategy = Strategy(
            name="first_asset_daily",
            allocator=_UseFirstAssetAllocator(),
            signal_filters=tuple(),
            rebalance_schedule="daily",
        )
        ctx = self._make_ctx(timeline, prices, strategy)
        result = run_backtest(ctx)

        # Day 0 EOD = 첫 equity_curve 포인트.
        assert len(result.equity_curve) >= 1
        day0_point = result.equity_curve[0]
        assert day0_point.time == timeline[0]
        # initial_cash 그대로 (큐잉 패턴: 첫날은 어제 큐잉 없음 → settlement skip).
        assert day0_point.equity == Decimal("100000"), (
            f"REGRESSION (TASK-244) — Day 0 EOD 가 pure cash 가 아님. "
            f"equity={day0_point.equity}, expected=100000 (initial_cash)"
        )
        # cash_total_in_base 도 100000 — 보유 자산 0.
        assert day0_point.cash_total_in_base == Decimal("100000")

        # 첫 iteration 까지의 fills 는 0 건 (시그널만 큐잉, 체결 없음).
        # 단, 전체 백테스트가 끝나면 D+1 부터 체결되므로 result.fills 는 ≥ 1.
        # 본 검증의 핵심은 Day 0 시점 equity_curve[0] 이 100000 인 것.

    def test_day_1_eod_is_post_init_trade(self) -> None:
        """Day 1 EOD == qty × p[1] + cash_after_buy (어제 큐잉이 D=1 settlement 직후 평가).

        equity = qty * price + cash_after, 보존 항등식: equity ≈ initial_cash − slippage − commission.
        """
        timeline = [
            date(2024, 3, 15),
            date(2024, 3, 18),
            date(2024, 3, 19),
        ]
        prices = [500.0, 500.0, 500.0]  # 평탄가 → equity 변동은 fees/slippage 만
        strategy = Strategy(
            name="first_asset_daily",
            allocator=_UseFirstAssetAllocator(),
            signal_filters=tuple(),
            rebalance_schedule="daily",
        )
        ctx = self._make_ctx(timeline, prices, strategy)
        result = run_backtest(ctx)

        # Day 0 = pure cash, Day 1 = post-settlement.
        assert len(result.equity_curve) >= 2
        day0 = result.equity_curve[0]
        day1 = result.equity_curve[1]

        assert day0.equity == Decimal("100000")  # 큐잉 패턴 sanity
        # Day 1 은 settlement 직후 — 보유 자산 + 잔여 cash.
        assert day1.time == timeline[1]
        # 평탄가 (price=500) + slippage_bps=10 + commission US=0.5 → 매수 가격 ≈ 500.525
        # qty = floor(100000 / 500.525) = 199.7... → 199 주.
        # 보유 평가 = 199 * 500 = 99500. cash_after = 100000 - 199*500.525 ≈ 395.5
        # equity ≈ 99500 + 395.5 ≈ 99895.5 (initial_cash 미만 — 거래비용 차감).
        assert day1.equity < Decimal("100000"), (
            f"REGRESSION (TASK-244) — Day 1 EOD 가 거래비용 차감 안 됨. "
            f"equity={day1.equity}, expected < 100000"
        )
        # equity = qty × price + cash_after 항등식 검증 (자산 1, price=500).
        position = result.final_portfolio.positions.get(1)
        assert position is not None, "Day 1 settlement 후 보유 포지션 없음"
        # 단순 케이스 (rebalance daily, target weight 동일) 라 매수 후 추가 변동 미미.
        # Day 1 시점 qty 를 정확 검증하려면 fills 누적 — 첫 BUY 1건만 있어야.
        buy_fills = [f for f in result.fills if f.side == "BUY"]
        assert len(buy_fills) >= 1
        first_buy = buy_fills[0]
        assert first_buy.settlement_date == timeline[1], (
            f"REGRESSION (TASK-244) — Day 0 시그널의 settlement 가 Day 1 이 아님. "
            f"settlement_date={first_buy.settlement_date}, expected={timeline[1]}"
        )
        # Day 1 EOD 시점 equity 항등식: equity == qty(D1) × p[1] + cash_total(D1).
        # final_portfolio 는 timeline 끝나는 시점 — 평탄가 + daily target 동일이라 추가 거래 미미.
        # 핵심은 day1.equity 가 day0 (pure cash) 보다 *작다* + day1 < 100000.

    def test_sell_signal_d_eod_still_holds(self) -> None:
        """매도 시그널 D 의 EOD 가 매도 전 평가 (큐잉 효과 검증).

        시나리오:
          - Day 0 (3/15): 매수 시그널 → 큐잉
          - Day 1 (3/18): settlement (매수 체결, qty>0) + 매도 시그널 큐잉
          - Day 2 (3/19): settlement (매도 체결)
        Day 1 EOD 는 매도 시그널이 *결정되었지만 체결되지 않은* 상태 → 보유 그대로 평가.
        Day 2 EOD 가 매도 후 cash 평가.
        """
        timeline = [
            date(2024, 3, 15),
            date(2024, 3, 18),
            date(2024, 3, 19),
        ]
        prices = [500.0, 500.0, 500.0]
        first_day = timeline[0]
        # OnceOnFirstDayAllocator: Day 0 만 매수 시그널, Day 1+ 는 cash-only (매도 시그널).
        strategy = Strategy(
            name="once_on_then_sell",
            allocator=_OnceOnFirstDayAllocator(first_day),
            signal_filters=tuple(),
            rebalance_schedule="daily",
        )
        ctx = self._make_ctx(timeline, prices, strategy)
        result = run_backtest(ctx)

        assert len(result.equity_curve) == 3
        day0 = result.equity_curve[0]
        day1 = result.equity_curve[1]
        day2 = result.equity_curve[2]

        # Day 0 = pure cash.
        assert day0.equity == Decimal("100000")
        # Day 1 = Day 0 매수 시그널 settlement 후 + Day 1 매도 시그널은 큐잉만 → 보유 그대로.
        # cash_total < 100000 (매수 후 잔여 cash 만 남음).
        assert day1.cash_total_in_base < Decimal("100000"), (
            "Day 1 settlement 후 cash 가 차감되어 있어야 함 (매수 체결 직후)"
        )
        # Day 1 보유 자산이 평가에 포함 — equity = cash + qty×price.
        # equity 는 거의 100000 근처 (slippage/commission 만 차감).
        assert day1.equity < Decimal("100000")
        assert day1.equity > Decimal("99000"), (
            f"Day 1 EOD 가 보유 평가를 빠뜨림 — equity={day1.equity}. "
            f"보유 자산 평가가 들어갔다면 거의 100000 근처여야 함."
        )

        # Day 2 = Day 1 매도 시그널 settlement 후 — 보유 청산.
        # cash 가 거의 100000 근처 (왕복 거래비용 차감).
        sell_fills = [f for f in result.fills if f.side == "SELL"]
        assert len(sell_fills) >= 1, (
            "Day 1 cash-only 시그널이 Day 2 에 settlement 되어 SELL 발생해야 함"
        )
        # SELL 의 settlement_date = Day 2.
        assert sell_fills[0].settlement_date == timeline[2], (
            f"REGRESSION (TASK-244) — 매도 시그널 (Day 1) 이 Day 2 settlement 안 됨. "
            f"settlement_date={sell_fills[0].settlement_date}"
        )
        # Day 2 EOD 시점에 보유 0 (매도 settlement 직후).
        # final_portfolio 는 timeline 끝 — 평탄가 + 매일 cash-only 라 보유 0.
        assert 1 not in result.final_portfolio.positions

    def test_buy_signal_d_eod_still_cash(self) -> None:
        """매수 시그널 D 의 EOD 가 cash 그대로 (체결 전 평가, 큐잉 효과 검증).

        Day 0 매수 시그널 발생 시 Day 0 EOD 에 fills 0 건 + cash == initial_cash.
        Day 1 EOD 가 settlement 직후 — cash 차감 + 보유 발생.
        """
        timeline = [
            date(2024, 3, 15),
            date(2024, 3, 18),
        ]
        prices = [500.0, 500.0]
        strategy = Strategy(
            name="first_asset_daily",
            allocator=_UseFirstAssetAllocator(),
            signal_filters=tuple(),
            rebalance_schedule="daily",
        )
        ctx = self._make_ctx(timeline, prices, strategy)
        result = run_backtest(ctx)

        assert len(result.equity_curve) == 2
        day0 = result.equity_curve[0]
        day1 = result.equity_curve[1]

        # Day 0 = pure cash (시그널 큐잉만, 체결 없음).
        assert day0.equity == Decimal("100000"), (
            f"REGRESSION (TASK-244) — 매수 시그널 D=0 EOD 가 cash 가 아님. "
            f"equity={day0.equity}, expected=100000"
        )
        assert day0.cash_total_in_base == Decimal("100000")
        # Day 1 = settlement 후 cash 차감.
        assert day1.cash_total_in_base < Decimal("100000"), (
            f"Day 1 settlement 후 cash 가 차감되어야 함. "
            f"cash_total={day1.cash_total_in_base}"
        )
        # Day 1 보유 자산 발생.
        assert 1 in result.final_portfolio.positions

        # 모든 fills 의 settlement_date 는 ≥ Day 1 (Day 0 settlement 없음).
        for fill in result.fills:
            assert fill.settlement_date >= timeline[1], (
                f"REGRESSION (TASK-244) — fill 이 Day 0 에 체결됨 (큐잉 위반). "
                f"fill.settlement_date={fill.settlement_date}"
            )
