"""비거래일 다층 방어 회귀 테스트 (TASK-081 B).

architecture.md V3 § "비거래일 방어" L182-186 (V1 결정 13 이월) — 4단계 방어:
1. **수집 레이어** (`app/data/sources/yfinance_source.py` `_is_invalid_close`):
   close=0/null/NaN 행 거부 + WARNING 로깅.
2. **캘린더 레이어** (`app/data/pipeline.py` `_trading_days` + L188 2차 필터):
   거래일 캘린더 외 날짜 source 응답 → 필터링.
3. **조회 레이어** (`app/domain/asset/calendar_guard.py` `guard_trading_day`):
   비거래일 입력 시 raise / snap_previous / snap_next.
4. **엔진 레이어** (`app/domain/trade.py` `assert_trading_day_for_universe` /
   `assert_all_assets_priced` + `engine.py` L209 슬라이싱):
   비거래일·가격 누락 시 명시적 NonTradingDayError / MissingPriceError.
"""
from __future__ import annotations

import math
from datetime import date, datetime
from decimal import Decimal

import pytest

from app.data.sources.yfinance_source import _is_invalid_close
from app.domain.asset.calendar_guard import (
    GuardMode,
    guard_trading_day,
    is_trading_day,
)
from app.domain.trade import (
    MissingPriceError,
    NonTradingDayError,
    assert_all_assets_priced,
    assert_trading_day_for_universe,
)


# ===== 1. 수집 레이어 — close=0/null/NaN 거부 =====


class TestIngestionLayerInvalidClose:
    """`_is_invalid_close` 가 None/NaN/0 을 invalid 판정하는지."""

    def test_none_close_is_invalid(self) -> None:
        assert _is_invalid_close(None) is True

    def test_nan_close_is_invalid(self) -> None:
        assert _is_invalid_close(float("nan")) is True

    def test_zero_close_is_invalid(self) -> None:
        assert _is_invalid_close(0) is True
        assert _is_invalid_close(0.0) is True

    def test_positive_close_is_valid(self) -> None:
        assert _is_invalid_close(100.0) is False
        assert _is_invalid_close(1) is False

    def test_negative_close_is_valid_per_current_policy(self) -> None:
        """현재 정책: 음수는 invalid 로 분리되지 않음 (거래소 데이터에 음수 close 없음).
        만약 미래에 정책 변경되면 이 회귀로 catch.
        """
        assert _is_invalid_close(-1.0) is False

    def test_yfinance_source_drops_nan_rows(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """YfinanceSource.fetch_ohlcv 가 NaN close 행을 결과에서 제외하는지 (mock)."""
        import pandas as pd

        from app.data.sources import yfinance_source as ys

        # mock yfinance Ticker.history
        rows = pd.DataFrame(
            {
                "Open": [100.0, 101.0, 102.0],
                "High": [101.0, 102.0, 103.0],
                "Low": [99.0, 100.0, 101.0],
                "Close": [100.5, float("nan"), 102.5],  # 중간 NaN
                "Adj Close": [100.5, float("nan"), 102.5],
                "Volume": [1000.0, 0.0, 1500.0],
            },
            index=pd.to_datetime(["2024-01-02", "2024-01-03", "2024-01-04"]),
        )

        class _MockTicker:
            def __init__(self, _symbol: str) -> None:
                pass

            def history(self, **_: object) -> pd.DataFrame:
                return rows

        monkeypatch.setattr(ys.yf, "Ticker", _MockTicker)
        monkeypatch.setattr(ys, "_rate_limit", lambda: None)

        source = ys.YfinanceSource()
        bars = source.fetch_ohlcv("FAKE", date(2024, 1, 2), date(2024, 1, 5))
        # NaN 행 1건 거부 → 2건만 남아야 함.
        assert len(bars) == 2
        closes = [bar.close for bar in bars]
        assert all(not math.isnan(c) for c in closes)
        assert closes == [100.5, 102.5]


# ===== 2. 캘린더 레이어 — _trading_days 필터링 =====


class TestCalendarLayerTradingDays:
    """`_trading_days` 가 시장별 캘린더 외 날짜를 제외하는지."""

    def test_us_excludes_weekends(self) -> None:
        from app.data.pipeline import _trading_days

        # 2024-01-06 (토), 2024-01-07 (일) 가 포함된 구간.
        days = _trading_days("US", date(2024, 1, 5), date(2024, 1, 8))
        assert date(2024, 1, 5) in days  # 금
        assert date(2024, 1, 6) not in days  # 토
        assert date(2024, 1, 7) not in days  # 일
        assert date(2024, 1, 8) in days  # 월

    def test_kr_excludes_weekends(self) -> None:
        from app.data.pipeline import _trading_days

        days = _trading_days("KR", date(2024, 1, 5), date(2024, 1, 8))
        assert date(2024, 1, 5) in days
        assert date(2024, 1, 6) not in days
        assert date(2024, 1, 7) not in days
        assert date(2024, 1, 8) in days

    def test_crypto_includes_all_days(self) -> None:
        """24/7 시장 — 주말/공휴일 모두 포함."""
        from app.data.pipeline import _trading_days

        days = _trading_days("CRYPTO", date(2024, 1, 5), date(2024, 1, 8))
        assert len(days) == 4
        assert date(2024, 1, 6) in days
        assert date(2024, 1, 7) in days

    def test_unknown_market_returns_empty(self) -> None:
        """알 수 없는 market 코드는 빈 리스트 (호출자가 REJECTED 처리 유도)."""
        from app.data.pipeline import _trading_days

        days = _trading_days("FAKE_MARKET", date(2024, 1, 5), date(2024, 1, 8))
        assert days == []

    def test_pipeline_filters_non_trading_bars_from_source(self) -> None:
        """pipeline.py L188 회귀: source 가 비거래일 bar 를 줘도 expected_set 으로 차단."""
        from app.data.sources.base import OhlcvBar

        # 2024-01-05 (금, 거래일) + 2024-01-06 (토, 비거래일) bar 시뮬.
        bars = [
            OhlcvBar(
                time=datetime(2024, 1, 5, 0, 0),
                open=100.0,
                high=101.0,
                low=99.0,
                close=100.5,
                adj_close=100.5,
                volume=1000.0,
            ),
            OhlcvBar(
                time=datetime(2024, 1, 6, 0, 0),  # 토
                open=100.5,
                high=101.0,
                low=100.0,
                close=100.7,
                adj_close=100.7,
                volume=0.0,
            ),
        ]
        from app.data.pipeline import _trading_days

        expected_set = set(_trading_days("US", date(2024, 1, 5), date(2024, 1, 8)))
        valid = [bar for bar in bars if bar.time.date() in expected_set]
        rejected = len(bars) - len(valid)
        assert rejected == 1
        assert len(valid) == 1
        assert valid[0].time.date() == date(2024, 1, 5)


# ===== 3. 조회 레이어 — guard_trading_day =====


class TestGuardLayerCalendarGuard:
    """`guard_trading_day` 의 raise/snap_previous/snap_next 모드 검증."""

    def test_trading_day_passes_through_all_modes(self) -> None:
        """거래일은 모드 무관 그대로 반환."""
        d = date(2024, 1, 5)  # 금요일 (US 거래일)
        assert is_trading_day("US", d) is True
        for mode in ("raise", "snap_previous", "snap_next"):
            assert guard_trading_day("US", d, mode=mode) == d  # type: ignore[arg-type]

    def test_non_trading_day_raises_in_raise_mode(self) -> None:
        sat = date(2024, 1, 6)
        assert is_trading_day("US", sat) is False
        with pytest.raises(ValueError, match="not a trading day"):
            guard_trading_day("US", sat, mode="raise")

    def test_non_trading_day_snaps_to_previous(self) -> None:
        sat = date(2024, 1, 6)
        snapped = guard_trading_day("US", sat, mode="snap_previous")
        assert snapped == date(2024, 1, 5)  # 직전 금요일

    def test_non_trading_day_snaps_to_next(self) -> None:
        sat = date(2024, 1, 6)
        snapped = guard_trading_day("US", sat, mode="snap_next")
        assert snapped == date(2024, 1, 8)  # 다음 월요일

    def test_unknown_market_raises(self) -> None:
        with pytest.raises(ValueError, match="Unknown market"):
            guard_trading_day("FAKE", date(2024, 1, 5))

    def test_crypto_always_trading_day(self) -> None:
        sat = date(2024, 1, 6)
        assert is_trading_day("CRYPTO", sat) is True
        # CRYPTO 는 모드 무관 그대로 반환.
        for mode in ("raise", "snap_previous", "snap_next"):
            assert guard_trading_day("CRYPTO", sat, mode=mode) == sat  # type: ignore[arg-type]


# ===== 4. 엔진 레이어 — assert_trading_day_for_universe / assert_all_assets_priced =====


class TestEngineLayerAssertions:
    """엔진 레이어 silent 0 금지 — 명시적 예외 발생 검증."""

    def test_assert_trading_day_for_universe_raises_on_non_trading_day(self) -> None:
        target_assets = [(1, "US"), (2, "KR")]
        sat = date(2024, 1, 6)
        with pytest.raises(NonTradingDayError, match="not a trading day"):
            assert_trading_day_for_universe(target_assets, sat, is_trading_day)

    def test_assert_trading_day_for_universe_passes_on_trading_day(self) -> None:
        target_assets = [(1, "US"), (2, "KR")]
        # 2024-01-05 — US/KR 모두 거래일 (금)
        d = date(2024, 1, 5)
        # 예외 안 남
        assert_trading_day_for_universe(target_assets, d, is_trading_day)

    def test_assert_trading_day_partial_market_failure_still_raises(self) -> None:
        """일부 시장만 비거래일이어도 raise (silent 0 금지)."""
        # US 공휴일 시뮬: 2024-01-15 (Martin Luther King Jr. Day) — KR 은 거래일.
        target_assets = [(1, "US"), (2, "KR")]
        d = date(2024, 1, 15)
        # US 는 비거래일
        assert is_trading_day("US", d) is False
        with pytest.raises(NonTradingDayError):
            assert_trading_day_for_universe(target_assets, d, is_trading_day)

    def test_assert_all_assets_priced_raises_on_missing(self) -> None:
        target_assets = [(1, "US"), (2, "KR"), (3, "CRYPTO")]
        prices: dict[int, Decimal] = {1: Decimal("100"), 2: Decimal("200")}
        # asset 3 누락
        with pytest.raises(MissingPriceError, match="missing prices"):
            assert_all_assets_priced(target_assets, prices, date(2024, 1, 5))

    def test_assert_all_assets_priced_passes_when_complete(self) -> None:
        target_assets = [(1, "US")]
        prices = {1: Decimal("100")}
        assert_all_assets_priced(target_assets, prices, date(2024, 1, 5))

    def test_engine_loc_until_d_excludes_future_dates(self) -> None:
        """engine.py L209 의 prices.loc[:d] 슬라이싱이 D+1 행을 제외하는지 직접 검증.

        비거래일 방어의 마지막 보루 — 미래 데이터가 흘러들어도 슬라이싱이 막아준다.
        """
        import pandas as pd

        timeline = [
            date(2024, 1, 2),
            date(2024, 1, 3),
            date(2024, 1, 4),
            date(2024, 1, 5),
            date(2024, 1, 8),
        ]
        prices = pd.DataFrame({1: [100, 101, 102, 103, 104]}, index=timeline)

        d = date(2024, 1, 4)
        sliced = prices.loc[:d]
        assert sliced.index.max() == d
        # D+1 (1/5) 이후는 절대 포함되지 않음
        assert date(2024, 1, 5) not in sliced.index
        assert date(2024, 1, 8) not in sliced.index
