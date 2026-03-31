"""
백테스터 테스트.
Backtester 클래스의 시뮬레이션, 포지션 추적, 수수료/슬리피지, 성과 지표를 테스트한다.
"""

import math

import numpy as np
import pandas as pd
import pytest

from src.analyzer.base import Signal, SignalType
from src.backtester import Backtester, Trade


# =============================================================================
# 헬퍼
# =============================================================================


def make_price_df(prices: list[float], start_date: str = "2020-01-01") -> pd.DataFrame:
    """가격 리스트로 간단한 price DataFrame을 생성한다."""
    dates = pd.bdate_range(start=start_date, periods=len(prices))
    return pd.DataFrame(
        {
            "date": dates.strftime("%Y-%m-%d"),
            "close": prices,
        }
    )


# =============================================================================
# 기본 시뮬레이션 테스트
# =============================================================================


class TestBacktesterBasic:
    """기본 시뮬레이션 동작을 검증한다."""

    @pytest.fixture
    def bt(self):
        return Backtester(
            initial_capital=10000.0,
            commission_rate=0.001,
            slippage=0.0005,
            risk_free_rate=0.02,
        )

    @pytest.fixture
    def price_df(self):
        """10일 가격 데이터 (100 → 110 선형 상승)."""
        prices = [100 + i for i in range(10)]
        return make_price_df(prices)

    def test_no_signals_no_trades(self, bt, price_df):
        """시그널이 없으면 거래가 발생하지 않아야 한다."""
        result = bt.run([], price_df)
        assert len(result["trades"]) == 0
        # 현금만 보유 → 포트폴리오 가치 = initial_capital
        assert result["metrics"]["final_value"] == bt.initial_capital

    def test_buy_signal_increases_position(self, bt, price_df):
        """BUY 시그널 후 shares > 0이어야 한다."""
        first_date = price_df["date"].iloc[0]
        signals = [Signal(date=first_date, signal_type=SignalType.BUY, weight=1.0)]
        result = bt.run(signals, price_df)

        portfolio = result["portfolio"]
        # 매수 후 shares > 0
        assert portfolio["shares"].iloc[0] > 0
        # 거래 내역에 BUY가 있어야 함
        assert any(t.action == "BUY" for t in result["trades"])

    def test_sell_signal_decreases_position(self, bt, price_df):
        """BUY 후 SELL하면 shares가 감소해야 한다."""
        dates = price_df["date"].tolist()
        signals = [
            Signal(date=dates[0], signal_type=SignalType.BUY, weight=1.0),
            Signal(date=dates[5], signal_type=SignalType.SELL, weight=1.0),
        ]
        result = bt.run(signals, price_df)

        portfolio = result["portfolio"]
        # 매수 직후 shares > 0
        shares_after_buy = portfolio["shares"].iloc[0]
        assert shares_after_buy > 0

        # 매도 후 shares == 0 (weight=1.0 → 전량 매도)
        shares_after_sell = portfolio["shares"].iloc[5]
        assert abs(shares_after_sell) < 1e-10

    def test_sell_without_position_no_trade(self, bt, price_df):
        """보유 포지션이 없을 때 SELL 시그널은 거래를 생성하지 않아야 한다."""
        first_date = price_df["date"].iloc[0]
        signals = [Signal(date=first_date, signal_type=SignalType.SELL, weight=1.0)]
        result = bt.run(signals, price_df)
        assert len(result["trades"]) == 0

    def test_hold_signal_no_trade(self, bt, price_df):
        """HOLD 시그널은 거래를 생성하지 않아야 한다."""
        first_date = price_df["date"].iloc[0]
        signals = [Signal(date=first_date, signal_type=SignalType.HOLD, weight=1.0)]
        result = bt.run(signals, price_df)
        assert len(result["trades"]) == 0


# =============================================================================
# Weight 반영 테스트
# =============================================================================


class TestBacktesterWeight:
    """weight 파라미터의 반영을 검증한다."""

    @pytest.fixture
    def bt(self):
        return Backtester(
            initial_capital=10000.0,
            commission_rate=0.0,  # 수수료/슬리피지 없이 weight만 테스트
            slippage=0.0,
        )

    def test_weight_half_buy(self, bt):
        """weight=0.5 → 자본의 50%만 사용하여 매수해야 한다."""
        prices = [100.0] * 5
        price_df = make_price_df(prices)
        first_date = price_df["date"].iloc[0]
        signals = [Signal(date=first_date, signal_type=SignalType.BUY, weight=0.5)]
        result = bt.run(signals, price_df)

        portfolio = result["portfolio"]
        # 수수료/슬리피지 = 0이므로 5000 / 100 = 50주, 남은 현금 = 5000
        assert abs(portfolio["shares"].iloc[0] - 50.0) < 1e-6
        assert abs(portfolio["cash"].iloc[0] - 5000.0) < 1e-6

    def test_weight_partial_sell(self, bt):
        """weight=0.5 매도 → 보유 주식의 50%만 매도해야 한다."""
        prices = [100.0] * 5
        price_df = make_price_df(prices)
        dates = price_df["date"].tolist()
        signals = [
            Signal(date=dates[0], signal_type=SignalType.BUY, weight=1.0),  # 전량 매수
            Signal(date=dates[2], signal_type=SignalType.SELL, weight=0.5),  # 절반 매도
        ]
        result = bt.run(signals, price_df)

        portfolio = result["portfolio"]
        shares_after_buy = portfolio["shares"].iloc[0]
        shares_after_sell = portfolio["shares"].iloc[2]
        # 절반이 남아있어야 함
        assert abs(shares_after_sell - shares_after_buy * 0.5) < 1e-6


# =============================================================================
# 수수료 및 슬리피지 테스트
# =============================================================================


class TestBacktesterCosts:
    """수수료와 슬리피지 적용을 검증한다."""

    def test_commission_applied(self):
        """수수료가 적용되면 최종 가치가 수수료 없을 때보다 낮아야 한다."""
        prices = [100.0, 110.0, 105.0, 115.0, 120.0]
        price_df = make_price_df(prices)
        dates = price_df["date"].tolist()
        signals = [
            Signal(date=dates[0], signal_type=SignalType.BUY, weight=1.0),
            Signal(date=dates[3], signal_type=SignalType.SELL, weight=1.0),
        ]

        bt_no_cost = Backtester(
            initial_capital=10000.0, commission_rate=0.0, slippage=0.0
        )
        bt_with_cost = Backtester(
            initial_capital=10000.0, commission_rate=0.01, slippage=0.0
        )

        result_no = bt_no_cost.run(signals, price_df)
        result_with = bt_with_cost.run(signals, price_df)

        assert (
            result_with["metrics"]["final_value"] < result_no["metrics"]["final_value"]
        )

    def test_slippage_applied(self):
        """슬리피지가 적용되면 최종 가치가 슬리피지 없을 때보다 낮아야 한다."""
        prices = [100.0, 110.0, 105.0, 115.0, 120.0]
        price_df = make_price_df(prices)
        dates = price_df["date"].tolist()
        signals = [
            Signal(date=dates[0], signal_type=SignalType.BUY, weight=1.0),
            Signal(date=dates[3], signal_type=SignalType.SELL, weight=1.0),
        ]

        bt_no_slip = Backtester(
            initial_capital=10000.0, commission_rate=0.0, slippage=0.0
        )
        bt_with_slip = Backtester(
            initial_capital=10000.0, commission_rate=0.0, slippage=0.01
        )

        result_no = bt_no_slip.run(signals, price_df)
        result_with = bt_with_slip.run(signals, price_df)

        assert (
            result_with["metrics"]["final_value"] < result_no["metrics"]["final_value"]
        )

    def test_trade_records_commission_and_slippage(self):
        """Trade 기록에 commission과 slippage_cost가 포함되어야 한다."""
        bt = Backtester(initial_capital=10000.0, commission_rate=0.001, slippage=0.0005)
        prices = [100.0, 110.0]
        price_df = make_price_df(prices)
        first_date = price_df["date"].iloc[0]
        signals = [Signal(date=first_date, signal_type=SignalType.BUY, weight=1.0)]

        result = bt.run(signals, price_df)
        trade = result["trades"][0]

        assert isinstance(trade, Trade)
        assert trade.commission > 0
        assert trade.slippage_cost > 0


# =============================================================================
# 성과 지표 테스트
# =============================================================================


class TestBacktesterMetrics:
    """성과 지표 계산을 검증한다."""

    @pytest.fixture
    def bt(self):
        return Backtester(initial_capital=10000.0, commission_rate=0.0, slippage=0.0)

    def test_total_return(self, bt):
        """총 수익률이 올바르게 계산되어야 한다."""
        # 100 → 150: 50% 수익
        prices = [100.0] + [100.0] * 8 + [150.0]
        price_df = make_price_df(prices)
        dates = price_df["date"].tolist()
        signals = [Signal(date=dates[0], signal_type=SignalType.BUY, weight=1.0)]
        result = bt.run(signals, price_df)

        # 전량 매수 후 가격 100→150, 수익률 ~50%
        total_return = result["metrics"]["total_return"]
        assert total_return > 0.45  # 대략 50% 근처

    def test_mdd_calculation(self, bt):
        """MDD(최대 낙폭)가 음수값으로 올바르게 계산되어야 한다."""
        # 가격: 상승 후 하락 → MDD 발생
        prices = [100, 120, 140, 100, 80, 90, 110]
        price_df = make_price_df(prices)
        dates = price_df["date"].tolist()
        signals = [Signal(date=dates[0], signal_type=SignalType.BUY, weight=1.0)]
        result = bt.run(signals, price_df)

        mdd = result["metrics"]["mdd"]
        # MDD는 음수
        assert mdd < 0
        # 140 → 80: ~42.9% 하락
        assert mdd < -0.4

    def test_sharpe_ratio_positive_for_uptrend(self, bt):
        """상승 추세에서 샤프 비율이 양수여야 한다."""
        prices = list(range(100, 200))
        price_df = make_price_df(prices)
        dates = price_df["date"].tolist()
        signals = [Signal(date=dates[0], signal_type=SignalType.BUY, weight=1.0)]
        result = bt.run(signals, price_df)

        assert result["metrics"]["sharpe_ratio"] > 0

    def test_win_rate_and_profit_loss(self, bt):
        """승률과 수익/손실 비율이 계산되어야 한다."""
        # 2번 매매: 첫번째 수익, 두번째 손실
        prices = [100, 110, 120, 110, 100, 90, 95, 85, 80, 75]
        price_df = make_price_df(prices)
        dates = price_df["date"].tolist()
        signals = [
            Signal(date=dates[0], signal_type=SignalType.BUY, weight=1.0),
            Signal(
                date=dates[2], signal_type=SignalType.SELL, weight=1.0
            ),  # 120에 매도 → 수익
            Signal(date=dates[3], signal_type=SignalType.BUY, weight=1.0),
            Signal(
                date=dates[5], signal_type=SignalType.SELL, weight=1.0
            ),  # 90에 매도 → 손실
        ]
        result = bt.run(signals, price_df)

        assert result["metrics"]["total_trades"] == 4
        # 승률은 0~1 범위
        assert 0.0 <= result["metrics"]["win_rate"] <= 1.0

    def test_cagr_positive_for_gain(self, bt):
        """자본이 증가하면 CAGR이 양수여야 한다."""
        prices = list(range(100, 200))
        price_df = make_price_df(prices)
        dates = price_df["date"].tolist()
        signals = [Signal(date=dates[0], signal_type=SignalType.BUY, weight=1.0)]
        result = bt.run(signals, price_df)

        assert result["metrics"]["cagr"] > 0


# =============================================================================
# 벤치마크 테스트
# =============================================================================


class TestBacktesterBenchmark:
    """Buy & Hold 벤치마크를 검증한다."""

    def test_benchmark_included(self):
        """결과에 benchmark 키가 포함되어야 한다."""
        bt = Backtester(initial_capital=10000.0, commission_rate=0.0, slippage=0.0)
        prices = list(range(100, 120))
        price_df = make_price_df(prices)
        signals = []
        result = bt.run(signals, price_df)

        assert "benchmark" in result
        assert "total_return" in result["benchmark"]
        assert "mdd" in result["benchmark"]

    def test_benchmark_buy_and_hold(self):
        """벤치마크는 첫 날 전액 매수하여 보유하는 전략이어야 한다."""
        bt = Backtester(initial_capital=10000.0, commission_rate=0.0, slippage=0.0)
        prices = [100.0, 110.0, 120.0, 130.0, 140.0]
        price_df = make_price_df(prices)
        result = bt.run([], price_df)

        # 100 → 140: 40% 수익
        bm_return = result["benchmark"]["total_return"]
        assert abs(bm_return - 0.4) < 0.01

    def test_alpha_calculation(self):
        """alpha = 전략 수익률 - 벤치마크 수익률이 계산되어야 한다."""
        bt = Backtester(initial_capital=10000.0, commission_rate=0.0, slippage=0.0)
        prices = [100.0] * 10
        price_df = make_price_df(prices)
        result = bt.run([], price_df)

        # 시그널 없음 → 전략 수익률 = 0, 벤치마크도 0 (가격 불변)
        assert "alpha" in result["metrics"]


# =============================================================================
# summary() 테스트
# =============================================================================


class TestBacktesterSummary:
    """summary() 텍스트 출력을 검증한다."""

    def test_summary_returns_string(self):
        """summary()가 문자열을 반환해야 한다."""
        bt = Backtester(initial_capital=10000.0)
        prices = list(range(100, 120))
        price_df = make_price_df(prices)
        text = bt.summary([], price_df)

        assert isinstance(text, str)
        assert "BACKTEST REPORT" in text
        assert "Total Return" in text
        assert "BENCHMARK" in text
        assert "Alpha" in text

    def test_summary_contains_metrics(self):
        """summary()에 주요 지표가 포함되어야 한다."""
        bt = Backtester(initial_capital=10000.0)
        prices = list(range(100, 120))
        price_df = make_price_df(prices)
        text = bt.summary([], price_df)

        assert "CAGR" in text
        assert "MDD" in text
        assert "Sharpe" in text
        assert "Win Rate" in text


# =============================================================================
# 빈 데이터 처리 테스트
# =============================================================================


class TestBacktesterEmpty:
    """빈 데이터 및 엣지 케이스를 검증한다."""

    def test_empty_price_df(self):
        """빈 price DataFrame이면 빈 결과를 반환해야 한다."""
        bt = Backtester(initial_capital=10000.0)
        empty_df = pd.DataFrame(columns=["date", "close"])
        result = bt.run([], empty_df)

        assert result["metrics"]["total_return"] == 0.0
        assert result["metrics"]["final_value"] == bt.initial_capital
        assert len(result["trades"]) == 0

    def test_missing_date_column(self):
        """date 컬럼이 없으면 빈 결과를 반환해야 한다."""
        bt = Backtester(initial_capital=10000.0)
        bad_df = pd.DataFrame({"close": [100, 110, 120]})
        result = bt.run([], bad_df)
        assert result["metrics"]["total_return"] == 0.0

    def test_missing_close_column(self):
        """close 컬럼이 없으면 빈 결과를 반환해야 한다."""
        bt = Backtester(initial_capital=10000.0)
        bad_df = pd.DataFrame({"date": ["2020-01-01", "2020-01-02"]})
        result = bt.run([], bad_df)
        assert result["metrics"]["total_return"] == 0.0

    def test_single_row_price_df(self):
        """1행짜리 price DataFrame도 처리해야 한다."""
        bt = Backtester(initial_capital=10000.0, commission_rate=0.0, slippage=0.0)
        price_df = make_price_df([100.0])
        result = bt.run([], price_df)
        # 시그널 없음 → 현금만 보유
        assert result["metrics"]["final_value"] == bt.initial_capital
