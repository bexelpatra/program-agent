"""
collector 모듈 유닛 테스트.
yfinance.download와 Database를 mock하여 실제 외부 연결 없이 테스트한다.
"""

from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch, PropertyMock

import pandas as pd
import pytest

from src.collector import _normalize_dataframe, collect_symbol, collect_all


# =============================================================================
# _normalize_dataframe 테스트
# =============================================================================


class TestNormalizeDataframe:
    def test_empty_dataframe_returns_empty_with_correct_columns(self):
        """빈 DataFrame 입력 시 올바른 컬럼을 가진 빈 DataFrame을 반환해야 한다."""
        result = _normalize_dataframe(pd.DataFrame(), "^GSPC")
        assert result.empty
        expected_cols = [
            "symbol",
            "date",
            "open",
            "high",
            "low",
            "close",
            "adj_close",
            "volume",
        ]
        assert list(result.columns) == expected_cols

    def test_standard_dataframe_normalization(self):
        """표준 yfinance DataFrame이 정규화되어야 한다."""
        df = pd.DataFrame(
            {
                "Open": [100.0],
                "High": [105.0],
                "Low": [95.0],
                "Close": [102.0],
                "Adj Close": [102.0],
                "Volume": [1000000],
            },
            index=pd.DatetimeIndex(["2026-01-01"], name="Date"),
        )
        result = _normalize_dataframe(df, "^GSPC")
        assert len(result) == 1
        assert result["symbol"].iloc[0] == "^GSPC"
        assert "date" in result.columns

    def test_multiindex_columns(self):
        """MultiIndex 컬럼을 가진 DataFrame도 처리해야 한다."""
        arrays = [
            ["Open", "High", "Low", "Close", "Volume"],
            ["^GSPC", "^GSPC", "^GSPC", "^GSPC", "^GSPC"],
        ]
        tuples = list(zip(*arrays))
        index = pd.MultiIndex.from_tuples(tuples)
        df = pd.DataFrame(
            [[100.0, 105.0, 95.0, 102.0, 1000000]],
            columns=index,
            index=pd.DatetimeIndex(["2026-01-01"], name="Date"),
        )
        result = _normalize_dataframe(df, "^GSPC")
        assert not result.empty
        assert "close" in result.columns

    def test_adj_close_fallback_to_close(self):
        """adj_close 컬럼이 없으면 close를 사용해야 한다."""
        df = pd.DataFrame(
            {
                "Open": [100.0],
                "High": [105.0],
                "Low": [95.0],
                "Close": [102.0],
                "Volume": [1000000],
            },
            index=pd.DatetimeIndex(["2026-01-01"], name="Date"),
        )
        result = _normalize_dataframe(df, "^GSPC")
        assert result["adj_close"].iloc[0] == 102.0

    def test_drops_nan_close_rows(self):
        """close가 NaN인 행은 제거되어야 한다."""
        df = pd.DataFrame(
            {
                "Open": [100.0, 101.0],
                "High": [105.0, 106.0],
                "Low": [95.0, 96.0],
                "Close": [102.0, float("nan")],
                "Volume": [1000000, 2000000],
            },
            index=pd.DatetimeIndex(["2026-01-01", "2026-01-02"], name="Date"),
        )
        result = _normalize_dataframe(df, "^GSPC")
        assert len(result) == 1

    def test_date_converted_to_date_type(self):
        """date 컬럼이 date 타입으로 변환되어야 한다."""
        df = pd.DataFrame(
            {
                "Open": [100.0],
                "High": [105.0],
                "Low": [95.0],
                "Close": [102.0],
                "Volume": [1000000],
            },
            index=pd.DatetimeIndex(["2026-01-01 14:30:00"], name="Date"),
        )
        result = _normalize_dataframe(df, "^GSPC")
        # Should be a date object, not a datetime
        from datetime import date

        assert isinstance(result["date"].iloc[0], date)

    def test_missing_required_columns_returns_empty(self):
        """필수 컬럼이 누락된 경우 빈 DataFrame을 반환해야 한다.

        _normalize_dataframe은 close 컬럼이 있어야 adj_close 폴백이 가능하므로,
        close는 있지만 open/high/low가 누락된 경우를 테스트한다.
        """
        df = pd.DataFrame(
            {"Close": [100.0]},
            index=pd.DatetimeIndex(["2026-01-01"], name="Date"),
        )
        result = _normalize_dataframe(df, "^GSPC")
        assert result.empty


# =============================================================================
# collect_symbol 테스트
# =============================================================================


class TestCollectSymbol:
    def _make_yf_df(self, n=5):
        """yfinance가 반환하는 형태의 DataFrame 생성."""
        return pd.DataFrame(
            {
                "Open": [100.0] * n,
                "High": [105.0] * n,
                "Low": [95.0] * n,
                "Close": [102.0] * n,
                "Adj Close": [102.0] * n,
                "Volume": [1000000] * n,
            },
            index=pd.DatetimeIndex(
                pd.date_range("2026-01-01", periods=n, freq="D"), name="Date"
            ),
        )

    @patch("src.collector.yf.download")
    def test_backfill_mode_when_no_last_date(self, mock_download):
        """get_last_date가 None을 반환하면 백필 모드(period='max')로 수집해야 한다."""
        mock_db = MagicMock()
        mock_db.get_last_date.return_value = None
        mock_download.return_value = self._make_yf_df()

        result = collect_symbol(mock_db, "^GSPC")

        mock_download.assert_called_once_with("^GSPC", period="max", progress=False)
        assert result == 5
        mock_db.insert_prices.assert_called_once()

    @patch("src.collector.yf.download")
    def test_incremental_mode_when_last_date_exists(self, mock_download):
        """get_last_date가 날짜를 반환하면 증분 모드로 수집해야 한다."""
        mock_db = MagicMock()
        mock_db.get_last_date.return_value = "2026-01-10"
        mock_download.return_value = self._make_yf_df(3)

        result = collect_symbol(mock_db, "^GSPC")

        call_kwargs = mock_download.call_args
        assert call_kwargs.kwargs.get("start") or call_kwargs[1].get("start")
        assert result == 3

    @patch("src.collector.yf.download")
    def test_incremental_skip_when_already_up_to_date(self, mock_download):
        """마지막 날짜가 오늘이면 수집을 스킵하고 0을 반환해야 한다."""
        mock_db = MagicMock()
        # Set last_date to today so start_date > end_date
        mock_db.get_last_date.return_value = datetime.now().strftime("%Y-%m-%d")

        result = collect_symbol(mock_db, "^GSPC")

        mock_download.assert_not_called()
        assert result == 0

    @patch("src.collector.yf.download")
    def test_returns_zero_when_no_data_collected(self, mock_download):
        """수집된 데이터가 없으면 0을 반환해야 한다."""
        mock_db = MagicMock()
        mock_db.get_last_date.return_value = None
        mock_download.return_value = pd.DataFrame()

        result = collect_symbol(mock_db, "^GSPC")

        assert result == 0
        mock_db.insert_prices.assert_not_called()


# =============================================================================
# collect_all 테스트
# =============================================================================


class TestCollectAll:
    @patch("src.collector.collect_symbol")
    @patch("src.collector.Database")
    def test_collect_all_processes_all_tickers(self, MockDatabase, mock_collect):
        """모든 티커에 대해 collect_symbol이 호출되어야 한다."""
        mock_db_instance = MagicMock()
        MockDatabase.return_value = mock_db_instance
        mock_collect.return_value = 10

        results = collect_all()

        from src.config import TICKER_SYMBOLS

        assert mock_collect.call_count == len(TICKER_SYMBOLS)
        mock_db_instance.init_schema.assert_called_once()
        mock_db_instance.close.assert_called_once()

    @patch("src.collector.collect_symbol")
    @patch("src.collector.Database")
    def test_collect_all_continues_on_failure(self, MockDatabase, mock_collect):
        """개별 티커 실패 시 나머지 티커 수집을 계속해야 한다."""
        mock_db_instance = MagicMock()
        MockDatabase.return_value = mock_db_instance

        # First call raises, rest succeed
        mock_collect.side_effect = [Exception("API error"), 10, 20]

        results = collect_all()

        from src.config import TICKER_SYMBOLS

        assert mock_collect.call_count == len(TICKER_SYMBOLS)
        # First ticker should have -1 (failed)
        first_symbol = TICKER_SYMBOLS[0]
        assert results[first_symbol] == -1

    @patch("src.collector.collect_symbol")
    def test_collect_all_uses_provided_db(self, mock_collect):
        """db 인스턴스를 전달하면 새로 생성하지 않아야 한다."""
        mock_db = MagicMock()
        mock_collect.return_value = 5

        results = collect_all(db=mock_db)

        # Should NOT call init_schema or close when db is provided
        mock_db.init_schema.assert_not_called()
        mock_db.close.assert_not_called()

    @patch("src.collector.collect_symbol")
    @patch("src.collector.Database")
    def test_collect_all_returns_results_dict(self, MockDatabase, mock_collect):
        """결과 딕셔너리가 올바른 형식이어야 한다."""
        mock_db_instance = MagicMock()
        MockDatabase.return_value = mock_db_instance
        mock_collect.return_value = 100

        results = collect_all()

        from src.config import TICKER_SYMBOLS

        for symbol in TICKER_SYMBOLS:
            assert symbol in results
            assert results[symbol] == 100
