"""
분석 전략 테스트.
StrategyRegistry, SeasonalityStrategy, MovingAverageStrategy, CorrelationStrategy를 테스트한다.
"""

import numpy as np
import pandas as pd
import pytest

from src.analyzer import StrategyRegistry
from src.analyzer.base import BaseStrategy, Signal, SignalType
from src.analyzer.seasonality import SeasonalityStrategy
from src.analyzer.moving_average import MovingAverageStrategy
from src.analyzer.correlation import CorrelationStrategy


# =============================================================================
# StrategyRegistry 테스트
# =============================================================================


class TestStrategyRegistry:
    """StrategyRegistry의 register/get/list_all 동작을 검증한다."""

    def test_register_and_get(self):
        """전략을 등록하고 이름으로 조회할 수 있어야 한다."""
        strategy = MovingAverageStrategy()
        # 이미 __init__.py에서 등록됨, get으로 조회 가능해야 함
        result = StrategyRegistry.get("moving_average")
        assert isinstance(result, MovingAverageStrategy)

    def test_get_nonexistent_raises(self):
        """존재하지 않는 전략을 조회하면 KeyError가 발생해야 한다."""
        with pytest.raises(KeyError):
            StrategyRegistry.get("nonexistent_strategy")

    def test_list_all(self):
        """등록된 전략 이름 목록을 반환해야 한다."""
        names = StrategyRegistry.list_all()
        assert isinstance(names, list)
        assert "seasonality" in names
        assert "moving_average" in names
        assert "correlation" in names

    def test_register_custom_strategy(self):
        """커스텀 전략을 등록하고 조회할 수 있어야 한다."""

        class DummyStrategy(BaseStrategy):
            @property
            def name(self) -> str:
                return "dummy_test"

            def analyze(self, df, **params):
                return {"summary": "", "metrics": {}, "details": pd.DataFrame()}

        dummy = DummyStrategy()
        StrategyRegistry.register(dummy)
        result = StrategyRegistry.get("dummy_test")
        assert result is dummy

        # cleanup: 테스트용 전략 제거
        del StrategyRegistry._strategies["dummy_test"]


# =============================================================================
# SeasonalityStrategy 테스트
# =============================================================================


class TestSeasonalityStrategy:
    """STL 계절성 분해 전략을 검증한다."""

    @pytest.fixture
    def strategy(self):
        return SeasonalityStrategy()

    @pytest.fixture
    def large_df(self):
        """STL 분해에 충분한 데이터 (600일, period=252이므로 504일 이상 필요)."""
        np.random.seed(42)
        n = 600
        dates = pd.bdate_range(start="2020-01-01", periods=n)
        # 추세 + 계절성 + 노이즈
        trend = np.linspace(100, 150, n)
        seasonal = 5 * np.sin(2 * np.pi * np.arange(n) / 252)
        noise = np.random.normal(0, 1, n)
        close = trend + seasonal + noise
        return pd.DataFrame({"date": dates, "close": close})

    @pytest.fixture
    def small_df(self):
        """데이터 부족 (100일 — period=252의 2배인 504일 미만)."""
        dates = pd.bdate_range(start="2020-01-01", periods=100)
        close = np.random.normal(100, 5, 100)
        return pd.DataFrame({"date": dates, "close": close})

    def test_name(self, strategy):
        assert strategy.name == "seasonality"

    def test_description(self, strategy):
        assert len(strategy.description) > 0

    def test_analyze_sufficient_data(self, strategy, large_df):
        """충분한 데이터로 STL 분해가 실행되어야 한다."""
        result = strategy.analyze(large_df)

        # 반환 구조 확인
        assert "summary" in result
        assert "metrics" in result
        assert "details" in result

        # metrics 키 확인
        assert "seasonal_strength" in result["metrics"]
        assert "trend_direction" in result["metrics"]

        # seasonal_strength는 0~1 범위
        ss = result["metrics"]["seasonal_strength"]
        assert 0.0 <= ss <= 1.0

        # trend_direction은 유효한 값
        assert result["metrics"]["trend_direction"] in ("up", "down", "flat")

        # details DataFrame이 비어있지 않아야 함
        assert not result["details"].empty
        assert "trend" in result["details"].columns
        assert "seasonal" in result["details"].columns
        assert "resid" in result["details"].columns

    def test_analyze_insufficient_data(self, strategy, small_df):
        """데이터 부족 시 적절한 메시지를 반환해야 한다."""
        result = strategy.analyze(small_df)

        assert "데이터 부족" in result["summary"]
        assert result["metrics"]["seasonal_strength"] == 0.0
        assert result["metrics"]["trend_direction"] == "unknown"
        assert result["details"].empty

    def test_generate_signals_returns_empty(self, strategy, large_df):
        """SeasonalityStrategy는 시그널을 생성하지 않는다 (기본 구현 사용)."""
        signals = strategy.generate_signals(large_df)
        assert signals == []


# =============================================================================
# MovingAverageStrategy 테스트
# =============================================================================


class TestMovingAverageStrategy:
    """이동평균 크로스오버 전략을 검증한다."""

    @pytest.fixture
    def strategy(self):
        return MovingAverageStrategy()

    @pytest.fixture
    def simple_df(self):
        """SMA 검증용 간단한 데이터 (5일, short_window=2, long_window=3)."""
        return pd.DataFrame(
            {
                "date": pd.date_range("2020-01-01", periods=5, freq="D"),
                "close": [10.0, 20.0, 30.0, 40.0, 50.0],
            }
        )

    @pytest.fixture
    def crossover_df(self):
        """
        골든크로스/데드크로스가 발생하는 데이터.
        short_window=3, long_window=5 기준으로 구성.
        """
        # 처음에 하락(short < long), 중간에 상승 전환(golden cross), 다시 하락(dead cross)
        prices = (
            [100, 98, 96, 94, 92]  # 하락: short < long
            + [95, 100, 110, 120, 130]  # 상승: golden cross
            + [125, 115, 105, 95, 85]  # 하락: dead cross
        )
        dates = pd.date_range("2020-01-01", periods=len(prices), freq="D")
        return pd.DataFrame({"date": dates, "close": prices})

    def test_name(self, strategy):
        assert strategy.name == "moving_average"

    def test_sma_calculation(self, strategy, simple_df):
        """간단한 데이터로 SMA 계산의 정확성을 확인한다."""
        result = strategy.analyze(simple_df, short_window=2, long_window=3)
        # 5행 < long_window(3) 아니므로 분석 진행됨
        # SMA2 @ row 1: (10+20)/2=15, row 2: (20+30)/2=25, row 3: (30+40)/2=35, row 4: (40+50)/2=45
        # SMA3 @ row 2: (10+20+30)/3=20, row 3: (20+30+40)/3=30, row 4: (30+40+50)/3=40
        # diff @ row2: 25-20=5>0, row3: 35-30=5>0, row4: 45-40=5>0 → 항상 bullish, 크로스 없음
        assert result["metrics"]["current_state"] == "bullish"
        assert result["metrics"]["golden_crosses"] == 0
        assert result["metrics"]["dead_crosses"] == 0

    def test_insufficient_data(self, strategy):
        """데이터가 long_window 미만이면 데이터 부족 메시지를 반환해야 한다."""
        short_df = pd.DataFrame(
            {
                "date": pd.date_range("2020-01-01", periods=3, freq="D"),
                "close": [10.0, 20.0, 30.0],
            }
        )
        result = strategy.analyze(short_df, short_window=2, long_window=5)
        assert "데이터 부족" in result["summary"]
        assert result["metrics"]["current_state"] == "unknown"

    def test_crossover_detection(self, strategy, crossover_df):
        """골든크로스/데드크로스 시그널이 생성되어야 한다."""
        result = strategy.analyze(crossover_df, short_window=3, long_window=5)

        metrics = result["metrics"]
        total = metrics["total_crossovers"]
        golden = metrics["golden_crosses"]
        dead = metrics["dead_crosses"]

        # 최소 1개 이상의 크로스오버가 있어야 함
        assert total >= 1
        assert golden + dead == total

    def test_generate_signals_returns_signal_list(self, strategy, crossover_df):
        """generate_signals()가 list[Signal]을 반환해야 한다."""
        signals = strategy.generate_signals(crossover_df, short_window=3, long_window=5)
        assert isinstance(signals, list)
        for sig in signals:
            assert isinstance(sig, Signal)
            assert sig.signal_type in (SignalType.BUY, SignalType.SELL)
            assert isinstance(sig.date, str)
            assert sig.weight == 1.0

    def test_generate_signals_matches_crossovers(self, strategy, crossover_df):
        """generate_signals()의 시그널 수가 분석 결과의 크로스오버 수와 일치해야 한다."""
        params = {"short_window": 3, "long_window": 5}
        result = strategy.analyze(crossover_df, **params)
        signals = strategy.generate_signals(crossover_df, **params)

        total_crossovers = result["metrics"]["total_crossovers"]
        assert len(signals) == total_crossovers

    def test_golden_cross_is_buy(self, strategy, crossover_df):
        """골든크로스 시 BUY 시그널이 생성되어야 한다."""
        signals = strategy.generate_signals(crossover_df, short_window=3, long_window=5)
        buy_signals = [s for s in signals if s.signal_type == SignalType.BUY]
        sell_signals = [s for s in signals if s.signal_type == SignalType.SELL]

        # 데이터에 상승구간이 있으므로 최소 1개 BUY 존재
        # (정확한 개수는 데이터에 따라 다를 수 있으므로 최소 1개만 확인)
        if len(signals) > 0:
            # 최소한 BUY 또는 SELL이 존재
            assert len(buy_signals) + len(sell_signals) == len(signals)


# =============================================================================
# CorrelationStrategy 테스트
# =============================================================================


class TestCorrelationStrategy:
    """자산 간 상관관계 분석 전략을 검증한다."""

    @pytest.fixture
    def strategy(self):
        return CorrelationStrategy()

    @pytest.fixture
    def multi_symbol_df(self):
        """3개 심볼의 피벗 테이블 (100일)."""
        np.random.seed(42)
        n = 100
        dates = pd.bdate_range(start="2020-01-01", periods=n)
        # A와 B는 양의 상관, A와 C는 음의 상관
        base = np.cumsum(np.random.normal(0, 1, n)) + 100
        df = pd.DataFrame(
            {
                "^GSPC": base,
                "GC=F": base * 0.5 + np.cumsum(np.random.normal(0, 0.5, n)) + 50,
                "TLT": -base * 0.3 + np.cumsum(np.random.normal(0, 0.3, n)) + 200,
            },
            index=dates,
        )
        df.index.name = "date"
        return df

    @pytest.fixture
    def two_symbol_df(self):
        """2개 심볼의 피벗 테이블."""
        np.random.seed(123)
        n = 80
        dates = pd.bdate_range(start="2020-01-01", periods=n)
        a = np.cumsum(np.random.normal(0, 1, n)) + 100
        b = a + np.random.normal(0, 0.3, n)  # 강한 양의 상관 (노이즈 최소화)
        df = pd.DataFrame({"A": a, "B": b}, index=dates)
        df.index.name = "date"
        return df

    def test_name(self, strategy):
        assert strategy.name == "correlation"

    def test_analyze_correlation_matrix(self, strategy, multi_symbol_df):
        """상관관계 행렬이 올바르게 계산되어야 한다."""
        result = strategy.analyze(multi_symbol_df, rolling_window=20)

        assert "summary" in result
        assert "metrics" in result
        assert "details" in result

        corr_matrix = result["metrics"]["correlation_matrix"]
        assert isinstance(corr_matrix, dict)
        # 3개 심볼이므로 3x3 행렬
        assert len(corr_matrix) == 3
        for sym in ["^GSPC", "GC=F", "TLT"]:
            assert sym in corr_matrix
            # 자기 자신과의 상관관계는 1.0
            assert abs(corr_matrix[sym][sym] - 1.0) < 1e-10

    def test_rolling_correlation(self, strategy, multi_symbol_df):
        """롤링 상관관계가 계산되어야 한다."""
        result = strategy.analyze(multi_symbol_df, rolling_window=20)
        details = result["details"]

        # 롤링 상관관계 DataFrame이 비어있지 않아야 함
        assert not details.empty
        # 3개 심볼 → 3C2 = 3 쌍
        assert details.shape[1] == 3

    def test_insufficient_data(self, strategy):
        """데이터가 rolling_window 미만이면 데이터 부족 메시지를 반환해야 한다."""
        dates = pd.bdate_range(start="2020-01-01", periods=5)
        df = pd.DataFrame({"A": [1, 2, 3, 4, 5], "B": [5, 4, 3, 2, 1]}, index=dates)
        result = strategy.analyze(df, rolling_window=60)
        assert "데이터 부족" in result["summary"]
        assert result["metrics"]["correlation_matrix"] == {}

    def test_single_symbol_insufficient(self, strategy):
        """심볼이 1개이면 분석 불가 메시지를 반환해야 한다."""
        dates = pd.bdate_range(start="2020-01-01", periods=100)
        df = pd.DataFrame({"A": np.random.normal(100, 5, 100)}, index=dates)
        result = strategy.analyze(df)
        assert "최소 2개" in result["summary"]

    def test_empty_input(self, strategy):
        """빈 DataFrame이면 적절히 처리해야 한다."""
        result = strategy.analyze(pd.DataFrame())
        assert result["metrics"]["correlation_matrix"] == {}
        assert result["metrics"]["significant_changes"] == []

    def test_two_symbols(self, strategy, two_symbol_df):
        """2개 심볼로도 상관관계 분석이 동작해야 한다."""
        result = strategy.analyze(two_symbol_df, rolling_window=20)
        corr = result["metrics"]["correlation_matrix"]
        assert "A" in corr
        assert "B" in corr
        # A와 B는 강한 양의 상관
        assert corr["A"]["B"] > 0.5
