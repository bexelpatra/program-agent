"""Tests for ``stock_backtest.backtest.calendar_guard``."""

from __future__ import annotations

import datetime as dt
import logging

import numpy as np
import pandas as pd
import pytest

from stock_backtest.backtest.calendar import get_trading_days
from stock_backtest.backtest.calendar_guard import (
    MissingPriceError,
    NonTradingDayError,
    align_to_trading_day,
    assert_universe_coverage,
    validate_date_range,
    validate_trading_day,
)


# ---------------------------------------------------------------------------
# validate_trading_day
# ---------------------------------------------------------------------------
class TestValidateTradingDay:
    def test_saturday_error_raises(self):
        # 2024-01-06 is a Saturday (US market).
        with pytest.raises(NonTradingDayError) as exc:
            validate_trading_day("US", dt.date(2024, 1, 6), align="error")
        assert exc.value.market == "US"
        assert exc.value.date == dt.date(2024, 1, 6)

    def test_saturday_align_previous(self):
        result = validate_trading_day("US", dt.date(2024, 1, 6), align="previous")
        assert result == dt.date(2024, 1, 5)  # Friday

    def test_saturday_align_next(self):
        result = validate_trading_day("US", dt.date(2024, 1, 6), align="next")
        assert result == dt.date(2024, 1, 8)  # Monday

    def test_trading_day_passthrough(self):
        assert validate_trading_day("US", dt.date(2024, 1, 5)) == dt.date(2024, 1, 5)

    def test_invalid_align_mode(self):
        # Use a non-trading day so the align branch actually executes.
        with pytest.raises(ValueError):
            validate_trading_day("US", dt.date(2024, 1, 6), align="weird")  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# validate_date_range
# ---------------------------------------------------------------------------
class TestValidateDateRange:
    def _us_jan_2024(self) -> pd.DatetimeIndex:
        return get_trading_days("US", dt.date(2024, 1, 1), dt.date(2024, 1, 31))

    def test_complete_index_passes(self):
        idx = self._us_jan_2024()
        # Should not raise.
        validate_date_range("US", dt.date(2024, 1, 1), dt.date(2024, 1, 31), idx)

    def test_missing_strict_raises(self):
        idx = self._us_jan_2024()
        assert len(idx) == 21  # NYSE January 2024 has 21 sessions (MLK day closed).
        missing_one = idx.delete(5)
        with pytest.raises(MissingPriceError) as exc:
            validate_date_range(
                "US",
                dt.date(2024, 1, 1),
                dt.date(2024, 1, 31),
                missing_one,
                strict=True,
            )
        assert exc.value.date == idx[5].date()

    def test_missing_non_strict_warns(self, caplog):
        idx = self._us_jan_2024()
        missing_one = idx.delete(3)
        with caplog.at_level(
            logging.WARNING, logger="stock_backtest.backtest.calendar_guard"
        ):
            validate_date_range(
                "US",
                dt.date(2024, 1, 1),
                dt.date(2024, 1, 31),
                missing_one,
                strict=False,
            )
        assert any("missing" in rec.message.lower() for rec in caplog.records)


# ---------------------------------------------------------------------------
# align_to_trading_day
# ---------------------------------------------------------------------------
class TestAlignToTradingDay:
    def test_weekend_to_previous_friday(self):
        dates = pd.DatetimeIndex(
            [
                "2024-01-05",  # Fri
                "2024-01-06",  # Sat
                "2024-01-07",  # Sun
                "2024-01-08",  # Mon
            ]
        )
        result = align_to_trading_day("US", dates, direction="previous")
        expected = pd.DatetimeIndex(
            ["2024-01-05", "2024-01-05", "2024-01-05", "2024-01-08"]
        )
        assert list(result) == list(expected)

    def test_weekend_to_next_monday(self):
        dates = pd.DatetimeIndex(
            [
                "2024-01-05",  # Fri
                "2024-01-06",  # Sat
                "2024-01-07",  # Sun
                "2024-01-08",  # Mon
            ]
        )
        result = align_to_trading_day("US", dates, direction="next")
        expected = pd.DatetimeIndex(
            ["2024-01-05", "2024-01-08", "2024-01-08", "2024-01-08"]
        )
        assert list(result) == list(expected)

    def test_invalid_direction(self):
        with pytest.raises(ValueError):
            align_to_trading_day(
                "US", pd.DatetimeIndex(["2024-01-05"]), direction="sideways"  # type: ignore[arg-type]
            )

    def test_empty_passthrough(self):
        result = align_to_trading_day("US", pd.DatetimeIndex([]))
        assert len(result) == 0


# ---------------------------------------------------------------------------
# assert_universe_coverage
# ---------------------------------------------------------------------------
class TestAssertUniverseCoverage:
    def test_full_coverage_passes(self):
        idx = get_trading_days("US", dt.date(2024, 1, 1), dt.date(2024, 1, 31))
        df = pd.DataFrame(
            {1: np.arange(len(idx), dtype=float), 2: np.arange(len(idx), dtype=float)},
            index=idx,
        )
        market_by_asset = {1: "US", 2: "US"}
        assert_universe_coverage(
            market_by_asset, df, dt.date(2024, 1, 1), dt.date(2024, 1, 31)
        )

    def test_multiple_missing_assets_reported(self):
        idx = get_trading_days("US", dt.date(2024, 1, 1), dt.date(2024, 1, 31))
        df = pd.DataFrame(
            {
                1: np.arange(len(idx), dtype=float),
                2: np.arange(len(idx), dtype=float),
                3: np.arange(len(idx), dtype=float),
            },
            index=idx,
        )
        # Asset 1 is missing row 2; asset 3 is missing row 7; asset 2 full.
        df.loc[idx[2], 1] = np.nan
        df.loc[idx[7], 3] = np.nan
        market_by_asset = {1: "US", 2: "US", 3: "US"}

        with pytest.raises(MissingPriceError) as exc:
            assert_universe_coverage(
                market_by_asset, df, dt.date(2024, 1, 1), dt.date(2024, 1, 31)
            )
        msg = str(exc.value)
        assert "asset_id=1" in msg
        assert "asset_id=3" in msg
        assert "asset_id=2" not in msg

    def test_missing_market_mapping_raises(self):
        idx = get_trading_days("US", dt.date(2024, 1, 1), dt.date(2024, 1, 5))
        df = pd.DataFrame({1: np.arange(len(idx), dtype=float)}, index=idx)
        with pytest.raises(KeyError):
            assert_universe_coverage({}, df, dt.date(2024, 1, 1), dt.date(2024, 1, 5))
