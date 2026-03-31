"""
Database 클래스 유닛 테스트.
clickhouse_connect.get_client를 mock하여 실제 DB 연결 없이 테스트한다.
"""

from unittest.mock import MagicMock, patch, call

import pandas as pd
import pytest

from src.database import (
    Database,
    CREATE_DATABASE_SQL,
    CREATE_ASSET_PRICES_SQL,
    CREATE_MV_MONTHLY_STATS_SQL,
)


@pytest.fixture
def mock_client():
    """Mock ClickHouse client."""
    client = MagicMock()
    client.command = MagicMock()
    client.insert_df = MagicMock()
    client.query_df = MagicMock(return_value=pd.DataFrame())
    client.close = MagicMock()
    return client


@pytest.fixture
def db(mock_client):
    """Database 인스턴스 (mock client 주입)."""
    with patch("src.database.clickhouse_connect.get_client", return_value=mock_client):
        config = {
            "host": "localhost",
            "port": 8123,
            "username": "default",
            "password": "",
            "database": "test_db",
        }
        database = Database(config=config)
        # Force client creation
        _ = database.client
    return database


# =============================================================================
# init_schema 테스트
# =============================================================================


class TestInitSchema:
    def test_init_schema_calls_command_three_times(self, db, mock_client):
        """init_schema는 DB 생성, 테이블 생성, MV 생성 총 3번 command를 호출해야 한다."""
        db.init_schema()
        assert mock_client.command.call_count == 3

    def test_init_schema_creates_database(self, db, mock_client):
        """첫 번째 command는 데이터베이스 생성이어야 한다."""
        db.init_schema()
        first_call_sql = mock_client.command.call_args_list[0][0][0]
        assert "CREATE DATABASE IF NOT EXISTS test_db" in first_call_sql

    def test_init_schema_creates_table(self, db, mock_client):
        """두 번째 command는 asset_prices 테이블 생성이어야 한다."""
        db.init_schema()
        second_call_sql = mock_client.command.call_args_list[1][0][0]
        assert "CREATE TABLE IF NOT EXISTS test_db.asset_prices" in second_call_sql

    def test_init_schema_creates_mv(self, db, mock_client):
        """세 번째 command는 Materialized View 생성이어야 한다."""
        db.init_schema()
        third_call_sql = mock_client.command.call_args_list[2][0][0]
        assert (
            "CREATE MATERIALIZED VIEW IF NOT EXISTS test_db.mv_monthly_stats"
            in third_call_sql
        )


# =============================================================================
# insert_prices 테스트
# =============================================================================


class TestInsertPrices:
    def _make_df(self, n=3):
        """테스트용 OHLCV DataFrame 생성."""
        return pd.DataFrame(
            {
                "symbol": ["^GSPC"] * n,
                "date": pd.date_range("2026-01-01", periods=n, freq="D"),
                "open": [100.0] * n,
                "high": [105.0] * n,
                "low": [95.0] * n,
                "close": [102.0] * n,
                "adj_close": [102.0] * n,
                "volume": [1000000] * n,
            }
        )

    def test_insert_prices_calls_insert_df(self, db, mock_client):
        """insert_prices는 client.insert_df를 호출해야 한다."""
        df = self._make_df()
        db.insert_prices(df)
        mock_client.insert_df.assert_called_once()

    def test_insert_prices_passes_correct_table(self, db, mock_client):
        """insert_df에 올바른 테이블 이름이 전달되어야 한다."""
        df = self._make_df()
        db.insert_prices(df)
        call_kwargs = mock_client.insert_df.call_args
        assert call_kwargs.kwargs["table"] == "test_db.asset_prices"

    def test_insert_prices_passes_correct_columns(self, db, mock_client):
        """insert_df에 올바른 컬럼 목록이 전달되어야 한다."""
        df = self._make_df()
        db.insert_prices(df)
        call_kwargs = mock_client.insert_df.call_args
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
        assert call_kwargs.kwargs["column_names"] == expected_cols

    def test_insert_prices_skips_empty_dataframe(self, db, mock_client):
        """빈 DataFrame이면 insert_df를 호출하지 않아야 한다."""
        df = pd.DataFrame()
        db.insert_prices(df)
        mock_client.insert_df.assert_not_called()

    def test_insert_prices_raises_on_missing_columns(self, db, mock_client):
        """필수 컬럼이 누락되면 ValueError를 발생시켜야 한다."""
        df = pd.DataFrame({"symbol": ["^GSPC"], "date": ["2026-01-01"]})
        with pytest.raises(ValueError, match="필수 컬럼 누락"):
            db.insert_prices(df)

    def test_insert_prices_converts_date_to_string(self, db, mock_client):
        """date 컬럼이 문자열로 변환되어 전달되어야 한다."""
        df = self._make_df(1)
        db.insert_prices(df)
        inserted_df = mock_client.insert_df.call_args.kwargs["df"]
        assert inserted_df["date"].iloc[0] == "2026-01-01"

    def test_insert_prices_converts_volume_to_uint64(self, db, mock_client):
        """volume 컬럼이 uint64 타입이어야 한다."""
        df = self._make_df(1)
        db.insert_prices(df)
        inserted_df = mock_client.insert_df.call_args.kwargs["df"]
        assert inserted_df["volume"].dtype.name == "uint64"


# =============================================================================
# select_prices 테스트
# =============================================================================


class TestSelectPrices:
    def test_select_prices_calls_query_df(self, db, mock_client):
        """select_prices는 client.query_df를 호출해야 한다."""
        db.select_prices("^GSPC", "2026-01-01", "2026-01-31")
        mock_client.query_df.assert_called_once()

    def test_select_prices_passes_correct_parameters(self, db, mock_client):
        """query_df에 올바른 파라미터가 전달되어야 한다."""
        db.select_prices("^GSPC", "2026-01-01", "2026-01-31")
        call_kwargs = mock_client.query_df.call_args
        params = call_kwargs.kwargs.get("parameters") or call_kwargs[1].get(
            "parameters"
        )
        assert params["symbol"] == "^GSPC"
        assert params["start_date"] == "2026-01-01"
        assert params["end_date"] == "2026-01-31"

    def test_select_prices_returns_dataframe(self, db, mock_client):
        """select_prices는 DataFrame을 반환해야 한다."""
        expected_df = pd.DataFrame({"symbol": ["^GSPC"], "close": [100.0]})
        mock_client.query_df.return_value = expected_df
        result = db.select_prices("^GSPC", "2026-01-01", "2026-01-31")
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 1


# =============================================================================
# get_last_date 테스트
# =============================================================================


class TestGetLastDate:
    def test_get_last_date_returns_date_string(self, db, mock_client):
        """데이터가 있으면 날짜 문자열을 반환해야 한다."""
        mock_client.query_df.return_value = pd.DataFrame(
            {"symbol": ["^GSPC"], "last_date": [pd.Timestamp("2026-01-15")]}
        )
        result = db.get_last_date("^GSPC")
        assert result == "2026-01-15"

    def test_get_last_date_returns_none_when_empty(self, db, mock_client):
        """데이터가 없으면 None을 반환해야 한다."""
        mock_client.query_df.return_value = pd.DataFrame()
        result = db.get_last_date("^GSPC")
        assert result is None

    def test_get_last_date_handles_string_date(self, db, mock_client):
        """last_date가 이미 문자열인 경우도 처리해야 한다."""
        mock_client.query_df.return_value = pd.DataFrame(
            {"symbol": ["^GSPC"], "last_date": ["2026-01-15"]}
        )
        result = db.get_last_date("^GSPC")
        assert result == "2026-01-15"


# =============================================================================
# get_daily_returns 테스트
# =============================================================================


class TestGetDailyReturns:
    def test_get_daily_returns_calls_query_df(self, db, mock_client):
        """get_daily_returns는 client.query_df를 호출해야 한다."""
        db.get_daily_returns("^GSPC")
        mock_client.query_df.assert_called_once()

    def test_get_daily_returns_passes_symbol_parameter(self, db, mock_client):
        """query_df에 symbol 파라미터가 전달되어야 한다."""
        db.get_daily_returns("^GSPC")
        call_kwargs = mock_client.query_df.call_args
        params = call_kwargs.kwargs.get("parameters") or call_kwargs[1].get(
            "parameters"
        )
        assert params["symbol"] == "^GSPC"

    def test_get_daily_returns_returns_dataframe(self, db, mock_client):
        """get_daily_returns는 DataFrame을 반환해야 한다."""
        expected = pd.DataFrame(
            {
                "symbol": ["^GSPC"],
                "date": ["2026-01-01"],
                "close": [100.0],
                "daily_return": [0.01],
            }
        )
        mock_client.query_df.return_value = expected
        result = db.get_daily_returns("^GSPC")
        assert isinstance(result, pd.DataFrame)


# =============================================================================
# close 테스트
# =============================================================================


class TestClose:
    def test_close_calls_client_close(self, db, mock_client):
        """close()는 client.close()를 호출해야 한다."""
        db.close()
        mock_client.close.assert_called_once()

    def test_close_sets_client_to_none(self, db, mock_client):
        """close() 후 _client는 None이어야 한다."""
        db.close()
        assert db._client is None

    def test_close_noop_when_no_client(self):
        """클라이언트가 없으면 close()는 아무것도 하지 않아야 한다."""
        with patch("src.database.clickhouse_connect.get_client"):
            config = {"host": "localhost", "port": 8123, "database": "test_db"}
            database = Database(config=config)
            # _client is None, close should not raise
            database.close()
