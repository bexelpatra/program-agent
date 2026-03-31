"""
database.py - DB 초기화 및 데이터 저장 모듈

aiosqlite를 사용하여 SQLite DB를 관리한다.
환율(exchange_rates)과 세계 지수(market_indices) 데이터를 저장한다.
"""

import os

import aiosqlite

from config import DB_PATH

# DB 파일의 디렉토리 경로
_DB_DIR = os.path.dirname(DB_PATH)


async def init_db() -> None:
    """DB 파일과 테이블을 생성한다.

    data/ 디렉토리가 없으면 자동으로 생성한다.
    exchange_rates, market_indices 테이블을 IF NOT EXISTS로 생성한다.
    """
    os.makedirs(_DB_DIR, exist_ok=True)

    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS exchange_rates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                currency TEXT NOT NULL,
                rate REAL NOT NULL,
                change_value REAL,
                change_percent REAL,
                collected_at TEXT NOT NULL
            )
            """
        )
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS market_indices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                index_name TEXT NOT NULL,
                country TEXT NOT NULL,
                value REAL NOT NULL,
                change_value REAL,
                change_percent REAL,
                collected_at TEXT NOT NULL
            )
            """
        )
        await db.commit()


async def save_exchange_rates(rates: list[dict]) -> None:
    """환율 데이터를 일괄 저장한다.

    Args:
        rates: 환율 딕셔너리 리스트. 각 딕셔너리는 다음 키를 포함한다:
            - currency (str): 통화 코드 (USD, EUR 등)
            - rate (float): 환율
            - change_value (float): 변동값
            - change_percent (float): 변동률(%)
            - collected_at (str): 수집 시각 (ISO 8601)
    """
    async with aiosqlite.connect(DB_PATH) as db:
        await db.executemany(
            """
            INSERT INTO exchange_rates (currency, rate, change_value, change_percent, collected_at)
            VALUES (:currency, :rate, :change_value, :change_percent, :collected_at)
            """,
            rates,
        )
        await db.commit()


async def save_market_indices(indices: list[dict]) -> None:
    """시장 지수 데이터를 일괄 저장한다.

    Args:
        indices: 지수 딕셔너리 리스트. 각 딕셔너리는 다음 키를 포함한다:
            - index_name (str): 지수명 (KOSPI, NASDAQ 등)
            - country (str): 국가
            - value (float): 현재값
            - change_value (float): 변동값
            - change_percent (float): 변동률(%)
            - collected_at (str): 수집 시각 (ISO 8601)
    """
    async with aiosqlite.connect(DB_PATH) as db:
        await db.executemany(
            """
            INSERT INTO market_indices (index_name, country, value, change_value, change_percent, collected_at)
            VALUES (:index_name, :country, :value, :change_value, :change_percent, :collected_at)
            """,
            indices,
        )
        await db.commit()
