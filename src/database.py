"""
ClickHouse 데이터베이스 모듈.
연결 관리, 테이블/뷰 생성, 데이터 INSERT/SELECT를 담당한다.
"""

import clickhouse_connect
import pandas as pd

from src.config import CLICKHOUSE_CONFIG, setup_logger

logger = setup_logger("database", "database.log")


# =============================================================================
# SQL 정의
# =============================================================================

CREATE_DATABASE_SQL = "CREATE DATABASE IF NOT EXISTS {database}"

CREATE_ASSET_PRICES_SQL = """
CREATE TABLE IF NOT EXISTS {database}.asset_prices (
    symbol String,
    date Date,
    open Float64,
    high Float64,
    low Float64,
    close Float64,
    adj_close Float64,
    volume UInt64,
    collected_at DateTime DEFAULT now()
) ENGINE = ReplacingMergeTree(collected_at)
PARTITION BY toYYYYMM(date)
ORDER BY (symbol, date)
"""

CREATE_MV_MONTHLY_STATS_SQL = """
CREATE MATERIALIZED VIEW IF NOT EXISTS {database}.mv_monthly_stats
ENGINE = AggregatingMergeTree()
PARTITION BY toYear(month)
ORDER BY (symbol, month)
AS SELECT
    symbol,
    toStartOfMonth(date) AS month,
    avgState(close) AS avg_close,
    maxState(high) AS max_high,
    minState(low) AS min_low,
    sumState(volume) AS total_volume,
    count() AS trading_days
FROM {database}.asset_prices
GROUP BY symbol, toStartOfMonth(date)
"""

SELECT_BY_SYMBOL_SQL = """
SELECT symbol, date, open, high, low, close, adj_close, volume
FROM {database}.asset_prices
FINAL
WHERE symbol = {{symbol:String}}
  AND date >= {{start_date:Date}}
  AND date <= {{end_date:Date}}
ORDER BY date
"""

DAILY_RETURN_SQL = """
SELECT
    symbol, date, close,
    lagInFrame(close, 1) OVER (PARTITION BY symbol ORDER BY date) AS prev_close,
    if(prev_close > 0, (close - prev_close) / prev_close, 0) AS daily_return
FROM {database}.asset_prices
FINAL
WHERE symbol = {{symbol:String}}
ORDER BY date
"""

LAST_DATE_SQL = """
SELECT symbol, max(date) AS last_date
FROM {database}.asset_prices
FINAL
WHERE symbol = {{symbol:String}}
GROUP BY symbol
"""


# =============================================================================
# Database 클래스
# =============================================================================


class Database:
    """ClickHouse 연결 및 CRUD 관리 클래스."""

    def __init__(self, config: dict | None = None):
        """
        Args:
            config: ClickHouse 연결 설정 딕셔너리.
                    None이면 config.py의 기본값 사용.
        """
        self._config = config or CLICKHOUSE_CONFIG.copy()
        self._database = self._config.pop("database", "asset_tracker")
        self._client = None

    @property
    def client(self):
        """ClickHouse 클라이언트를 lazy하게 생성하여 반환한다."""
        if self._client is None:
            self._client = clickhouse_connect.get_client(**self._config)
            logger.info(
                "ClickHouse 연결 완료: %s:%s",
                self._config.get("host"),
                self._config.get("port"),
            )
        return self._client

    def close(self):
        """클라이언트 연결을 종료한다."""
        if self._client is not None:
            self._client.close()
            self._client = None
            logger.info("ClickHouse 연결 종료")

    # -------------------------------------------------------------------------
    # 스키마 초기화
    # -------------------------------------------------------------------------

    def init_schema(self):
        """데이터베이스, 테이블, Materialized View를 생성한다."""
        logger.info("스키마 초기화 시작 (database=%s)", self._database)

        self.client.command(CREATE_DATABASE_SQL.format(database=self._database))
        logger.info("데이터베이스 확인/생성 완료: %s", self._database)

        self.client.command(CREATE_ASSET_PRICES_SQL.format(database=self._database))
        logger.info("테이블 확인/생성 완료: asset_prices")

        self.client.command(CREATE_MV_MONTHLY_STATS_SQL.format(database=self._database))
        logger.info("Materialized View 확인/생성 완료: mv_monthly_stats")

    # -------------------------------------------------------------------------
    # INSERT
    # -------------------------------------------------------------------------

    def insert_prices(self, df: pd.DataFrame):
        """
        DataFrame을 asset_prices 테이블에 bulk insert한다.

        Args:
            df: 컬럼 — symbol, date, open, high, low, close, adj_close, volume
        """
        if df.empty:
            logger.warning("빈 DataFrame — insert 스킵")
            return

        required_cols = [
            "symbol",
            "date",
            "open",
            "high",
            "low",
            "close",
            "adj_close",
            "volume",
        ]
        missing = [c for c in required_cols if c not in df.columns]
        if missing:
            raise ValueError(f"필수 컬럼 누락: {missing}")

        # date 컬럼을 문자열로 변환 (ClickHouse Date 타입 호환)
        insert_df = df[required_cols].copy()
        insert_df["date"] = pd.to_datetime(insert_df["date"]).dt.strftime("%Y-%m-%d")
        insert_df["volume"] = insert_df["volume"].fillna(0).astype("uint64")

        self.client.insert_df(
            table=f"{self._database}.asset_prices",
            df=insert_df,
            column_names=required_cols,
        )
        logger.info(
            "INSERT 완료: %d행 (%s)",
            len(insert_df),
            insert_df["symbol"].unique().tolist(),
        )

    # -------------------------------------------------------------------------
    # SELECT
    # -------------------------------------------------------------------------

    def select_prices(
        self, symbol: str, start_date: str, end_date: str
    ) -> pd.DataFrame:
        """
        특정 심볼의 가격 데이터를 조회한다.

        Args:
            symbol: 티커 심볼 (예: "^GSPC")
            start_date: 조회 시작일 (YYYY-MM-DD)
            end_date: 조회 종료일 (YYYY-MM-DD)

        Returns:
            OHLCV DataFrame
        """
        query = SELECT_BY_SYMBOL_SQL.format(database=self._database)
        result = self.client.query_df(
            query,
            parameters={
                "symbol": symbol,
                "start_date": start_date,
                "end_date": end_date,
            },
        )
        logger.info(
            "SELECT 완료: %s [%s ~ %s] → %d행",
            symbol,
            start_date,
            end_date,
            len(result),
        )
        return result

    def get_daily_returns(self, symbol: str) -> pd.DataFrame:
        """
        심볼의 일간 수익률을 쿼리 시점에 계산하여 반환한다.
        lagInFrame 윈도우 함수를 사용한다.

        Args:
            symbol: 티커 심볼

        Returns:
            DataFrame (symbol, date, close, prev_close, daily_return)
        """
        query = DAILY_RETURN_SQL.format(database=self._database)
        result = self.client.query_df(
            query,
            parameters={"symbol": symbol},
        )
        logger.info("일간 수익률 조회 완료: %s → %d행", symbol, len(result))
        return result

    def get_last_date(self, symbol: str) -> str | None:
        """
        특정 심볼의 마지막 저장 날짜를 반환한다 (증분 수집용).

        Args:
            symbol: 티커 심볼

        Returns:
            마지막 날짜 문자열 (YYYY-MM-DD) 또는 데이터 없으면 None
        """
        query = LAST_DATE_SQL.format(database=self._database)
        result = self.client.query_df(
            query,
            parameters={"symbol": symbol},
        )
        if result.empty:
            logger.info("마지막 날짜 없음 (신규 심볼): %s", symbol)
            return None

        last_date = str(result.iloc[0]["last_date"])
        # pandas Timestamp → 문자열 변환
        if hasattr(result.iloc[0]["last_date"], "strftime"):
            last_date = result.iloc[0]["last_date"].strftime("%Y-%m-%d")

        logger.info("마지막 날짜 조회: %s → %s", symbol, last_date)
        return last_date
