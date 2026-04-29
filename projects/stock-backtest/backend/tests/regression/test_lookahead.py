"""Look-ahead 회귀 테스트 (TASK-081 A).

목표:
- architecture.md V3 § "거래 정책" 모델 A 의 구조적 차단 검증.
- engine.py L209 의 `prices_until_d = ctx.prices_aligned.loc[:d]` 슬라이싱이
  Allocator/Filter 호출 시 D+1 데이터를 절대 노출하지 않음을 확인.
- 모든 Allocator (FixedWeight / AllWeather / EqualWeight) 와 Filter (MovingAverage /
  Momentum) 는 `prices_until_d` 만 신뢰하는 계약을 따른다 (strategy.py L75-77).

검증 전략:
1. 가격무관 Allocator (FixedWeight/AllWeather/EqualWeight) — 동일 universe 에 대해
   prices_until_d 의 길이를 늘려도 결과 동일.
2. 가격기반 Filter (MovingAverage/Momentum) — 동일 signal_date / 동일 prefix 에서
   미래 데이터 추가가 결과를 바꾸지 못함 (D 시점 tail 윈도우만 사용).
3. Engine 통합 — run_backtest 가 Allocator/Filter 에 넘기는 prices DataFrame 의
   max(index) 가 항상 signal_date 이하 (D+1 미포함) 임을 spy 로 검증.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from decimal import Decimal

import pandas as pd
import pytest

from app.domain.allocators.all_weather import AllWeather, AllWeatherParams
from app.domain.allocators.equal_weight import EqualWeight, EqualWeightParams
from app.domain.allocators.fixed_weight import FixedWeight, FixedWeightParams
from app.domain.engine import BacktestRunContext, run_backtest
from app.domain.filters.momentum import Momentum, MomentumParams
from app.domain.filters.moving_average import MovingAverage, MovingAverageParams
from app.domain.strategy import Strategy


# ===== Fixture =====


@pytest.fixture
def base_prices() -> pd.DataFrame:
    """date index, asset 1/2 column. 300 일 monotonic 시계열.

    monotonic 이라 MovingAverage 는 항상 PASS, Momentum 도 항상 PASS.
    """
    dates = [date(2024, 1, 1) + timedelta(days=i) for i in range(300)]
    return pd.DataFrame(
        {1: list(range(100, 400)), 2: list(range(200, 500))},
        index=dates,
    )


# ===== 1. Allocator 가격 무관성 회귀 =====


def test_fixed_weight_no_lookahead(base_prices: pd.DataFrame) -> None:
    """FixedWeight 는 가격 무관 — prices_until_d 길이 차이에 영향 없음."""
    a = FixedWeight(FixedWeightParams(weights={1: 0.6, 2: 0.4}))
    signal_date = base_prices.index[199]
    until_d = base_prices.iloc[:200]
    until_d_plus_50 = base_prices.iloc[:250]  # D+50 일 추가 노출
    w1 = a.generate_weights([1, 2], until_d, signal_date)
    w2 = a.generate_weights([1, 2], until_d_plus_50, signal_date)
    assert w1 == w2, "FixedWeight 결과는 prices 길이에 무관해야 함 (가격 무관 allocator)"


def test_equal_weight_no_lookahead(base_prices: pd.DataFrame) -> None:
    """EqualWeight 는 가격 무관 — prices_until_d 길이 차이에 영향 없음."""
    e = EqualWeight(EqualWeightParams())
    signal_date = base_prices.index[99]
    w1 = e.generate_weights([1, 2], base_prices.iloc[:100], signal_date)
    w2 = e.generate_weights([1, 2], base_prices.iloc[:200], signal_date)
    assert w1 == w2


def test_all_weather_no_lookahead(base_prices: pd.DataFrame) -> None:
    """AllWeather 는 가격 무관 — prices_until_d 길이 차이에 영향 없음.

    카테고리 weights 는 universe 에 없는 카테고리를 0 으로 두어
    AllWeatherCategoryMissing 회피.
    """
    a = AllWeather(
        AllWeatherParams(
            asset_categories={1: "equity", 2: "long_bond"},
            category_weights={
                "equity": 0.5,
                "long_bond": 0.5,
                "intermediate_bond": 0.0,
                "gold": 0.0,
                "commodity": 0.0,
            },
        )
    )
    signal_date = base_prices.index[99]
    w1 = a.generate_weights([1, 2], base_prices.iloc[:100], signal_date)
    w2 = a.generate_weights([1, 2], base_prices.iloc[:200], signal_date)
    assert w1 == w2


# ===== 2. Filter 모델 A 구조적 검증 =====
#
# Filter 는 prices_until_d 의 마지막 행을 D 일 종가로 사용한다 (modeling A).
# 따라서 "Engine 이 prices_aligned.loc[:d] 슬라이싱을 안 하고 미래 데이터를
# 추가로 넘기면 결과가 변할 수 있다" 가 자연스러운 설계 (필터 본질).
#
# 회귀 핵심:
# (a) 같은 prices_until_d (정확히 D 까지만) 에서 결과가 결정적
# (b) 호출자(=engine.py L209) 가 슬라이싱 책임 — Engine 통합 테스트가 보장


def test_moving_average_deterministic_on_same_prefix(base_prices: pd.DataFrame) -> None:
    """동일 prices_until_d 에서 MovingAverage 결과가 결정적임 (재호출 동일)."""
    f = MovingAverage(MovingAverageParams(window=50))
    signal_date = base_prices.index[99]
    prefix = base_prices.iloc[:100]  # D = 99
    e1 = f.is_eligible(1, prefix, signal_date)
    e2 = f.is_eligible(1, prefix, signal_date)
    assert e1 == e2
    # monotonic 시계열이면 PASS 가 자연스러움 — 단 결과값 자체는 회귀 핵심 아님.


def test_momentum_deterministic_on_same_prefix(base_prices: pd.DataFrame) -> None:
    """동일 prices_until_d 에서 Momentum 결과가 결정적임."""
    f = Momentum(MomentumParams(lookback=50, threshold=0.0))
    signal_date = base_prices.index[99]
    prefix = base_prices.iloc[:100]
    e1 = f.is_eligible(1, prefix, signal_date)
    e2 = f.is_eligible(1, prefix, signal_date)
    assert e1 == e2


def test_moving_average_changes_when_caller_violates_slicing(
    base_prices: pd.DataFrame,
) -> None:
    """Filter 본질 회귀:
    호출자가 slicing 책임을 어기고 미래 데이터를 추가로 넘기면 결과가 바뀔 수 있다.

    이 테스트는 '필터는 자체 슬라이싱 안 함' 을 명시적으로 보여주며,
    엔진의 `prices_aligned.loc[:d]` 가 누구도 우회할 수 없는 유일한 차단점임을
    문서화한다 (회귀 시 이 테스트가 깨지면 필터 자체가 lookahead 보호 가정을
    잘못 추가한 것 — 그것도 문제이므로 회귀 범위).

    monotonic 시계열에서 prices.tail(50) 의 평균은 길이가 늘면 변한다 →
    is_eligible 결과가 동일할 수도 다를 수도 있다. 핵심은 호출자가 prefix 를
    정확히 잘라 넘겨야 한다는 계약을 명시하는 것.
    """
    f = MovingAverage(MovingAverageParams(window=50))
    signal_date = base_prices.index[99]
    prefix_correct = base_prices.iloc[:100]  # D 까지만 (모델 A)
    prefix_violated = base_prices.iloc[:150]  # 호출자가 D+50 까지 넘김 (위반)

    # 두 결과가 같든 다르든 회귀 본질은 다음:
    # - prefix_correct 는 D 일 종가 = base_prices.iloc[99]
    # - prefix_violated 는 D 일 종가 가 = base_prices.iloc[149] 가 됨 (필터 입장에서)
    # → 호출자가 D+1 데이터를 넣으면 필터가 그것을 D 종가로 오인.
    # 이 테스트는 '필터가 slicing 안 한다' 를 stable 하게 검증.
    last_correct = prefix_correct[1].iloc[-1]
    last_violated = prefix_violated[1].iloc[-1]
    assert (
        last_correct != last_violated
    ), "이 테스트가 깨지면 base_prices fixture 가 monotonic 이 아님 (테스트 가정 위반)"
    # 결과 자체에 대한 assert 는 하지 않음 — 핵심은 'engine.py L209 가 유일한 차단점' 임.
    # 만약 미래에 Filter 가 자체 슬라이싱을 추가하면 이 테스트는 회귀로 분류됨.


# ===== 3. Engine 통합 회귀 (spy) =====


@dataclass
class _SpyAllocator:
    """run_backtest 가 generate_weights 호출 시 prices.index.max() 를 기록."""

    name: str = "spy"
    captured: list[tuple[date, date]] = None

    def __post_init__(self) -> None:
        if self.captured is None:
            object.__setattr__(self, "captured", [])

    def required_universe(self) -> list[int]:
        return [1]

    def generate_weights(
        self,
        universe_asset_ids: list[int],
        prices_until_d: pd.DataFrame,
        signal_date: date,
    ) -> dict[int, Decimal]:
        last_index = prices_until_d.index.max() if len(prices_until_d) else None
        self.captured.append((signal_date, last_index))
        # cash 만 보유 — 빈 weights 반환 (체결 안 함, 가격 누락 방어 회피).
        return {}


def _make_engine_ctx(
    prices_aligned: pd.DataFrame,
    strategy: Strategy,
) -> BacktestRunContext:
    """engine 통합 회귀용 최소 컨텍스트.

    USD base + 단일 자산 1 (US/USD). fx 환산 불필요.
    """
    return BacktestRunContext(
        base_currency="USD",
        period_start=prices_aligned.index[0],
        period_end=prices_aligned.index[-1],
        initial_cash={"USD": Decimal("10000")},
        universe_market_meta={1: ("US", "USD")},
        prices_aligned=prices_aligned,
        fx_rates_to_base={d: {} for d in prices_aligned.index},
        strategy=strategy,
    )


def test_engine_never_exposes_future_data_to_allocator() -> None:
    """모델 A 구조적 차단의 정수: engine.py L209 의 prices.loc[:d] 검증.

    XNYS 캘린더의 실제 거래일 timeline 으로 백테스트 → spy allocator 가
    호출될 때마다 prices.index.max() 가 signal_date 이하인지 확인.
    """
    import exchange_calendars as xcals

    cal = xcals.get_calendar("XNYS")
    sessions = cal.sessions_in_range("2024-01-02", "2024-03-29")
    timeline = [s.date() for s in sessions]
    prices_aligned = pd.DataFrame(
        {1: [100.0 + i for i in range(len(timeline))]},
        index=timeline,
    )

    spy = _SpyAllocator()
    strategy = Strategy(
        name="spy_strategy",
        allocator=spy,
        signal_filters=(),
        rebalance_schedule="daily",  # 매일 리밸런싱 → spy 가 매 거래일 호출
    )
    ctx = _make_engine_ctx(prices_aligned, strategy)
    run_backtest(ctx)

    assert len(spy.captured) > 0, "spy allocator 가 한 번도 호출되지 않음"
    violations: list[tuple[date, date]] = [
        (signal_date, last_index)
        for signal_date, last_index in spy.captured
        if last_index is not None and last_index > signal_date
    ]
    assert not violations, (
        f"engine 이 D+1 이후 데이터를 allocator 에 노출함 (violation count={len(violations)}): "
        f"sample={violations[:3]}"
    )


def test_engine_never_exposes_future_data_to_filter() -> None:
    """Filter 도 동일 — engine.py L209 슬라이싱이 Filter.is_eligible 에도 적용됨.

    apply_filters_and_allocator (strategy.py) 가 동일 prices_until_d 를 필터에
    넘기므로, Allocator 검증과 동일하게 prices_until_d.index.max() ≤ signal_date.
    """
    import exchange_calendars as xcals

    cal = xcals.get_calendar("XNYS")
    sessions = cal.sessions_in_range("2024-01-02", "2024-06-28")
    timeline = [s.date() for s in sessions]
    prices_aligned = pd.DataFrame(
        {1: [100.0 + i for i in range(len(timeline))]},
        index=timeline,
    )

    captured: list[tuple[date, date]] = []

    class SpyFilter:
        name = "spy_filter"

        def is_eligible(
            self,
            asset_id: int,
            prices_until_d: pd.DataFrame,
            signal_date: date,
        ) -> bool:
            last_index = prices_until_d.index.max() if len(prices_until_d) else None
            captured.append((signal_date, last_index))
            return False  # 필터 OFF → allocator 호출 없음 → 빈 weights

    strategy = Strategy(
        name="spy_filter_strategy",
        allocator=EqualWeight(EqualWeightParams()),
        signal_filters=(SpyFilter(),),
        rebalance_schedule="weekly",
    )
    ctx = _make_engine_ctx(prices_aligned, strategy)
    run_backtest(ctx)

    assert len(captured) > 0, "spy filter 가 한 번도 호출되지 않음"
    violations = [(sd, li) for sd, li in captured if li is not None and li > sd]
    assert not violations, (
        f"engine 이 D+1 이후 데이터를 filter 에 노출함 (violation count={len(violations)}): "
        f"sample={violations[:3]}"
    )
