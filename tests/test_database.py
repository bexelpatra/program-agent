"""
test_database.py - database.py 모듈 테스트

임시 DB 파일을 사용하여 실제 DB에 영향을 주지 않는다.
"""

import asyncio
import os
import sys
import tempfile

import pytest

# src/ 디렉토리를 sys.path에 추가
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import aiosqlite

# database 모듈을 import하기 전에 DB_PATH를 임시 파일로 교체한다
import config

_tmp_dir = tempfile.mkdtemp()
_tmp_db_path = os.path.join(_tmp_dir, "test_market_data.db")
config.DB_PATH = _tmp_db_path

import database  # noqa: E402 — config.DB_PATH 패치 이후에 import


@pytest.fixture(autouse=True)
def clean_db():
    """각 테스트 전후로 임시 DB 파일을 삭제하여 격리한다."""
    if os.path.exists(_tmp_db_path):
        os.remove(_tmp_db_path)
    # database 모듈 내부의 _DB_DIR도 갱신
    database._DB_DIR = os.path.dirname(_tmp_db_path)
    yield
    if os.path.exists(_tmp_db_path):
        os.remove(_tmp_db_path)


# ------------------------------------------------------------------
# init_db 테스트
# ------------------------------------------------------------------


@pytest.mark.asyncio
async def test_init_db_creates_tables():
    """init_db()가 exchange_rates, market_indices 테이블을 생성하는지 확인한다."""
    await database.init_db()

    async with aiosqlite.connect(_tmp_db_path) as db:
        cursor = await db.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        )
        tables = [row[0] for row in await cursor.fetchall()]

    assert "exchange_rates" in tables
    assert "market_indices" in tables


@pytest.mark.asyncio
async def test_init_db_is_idempotent():
    """init_db()를 두 번 호출해도 에러가 발생하지 않는다."""
    await database.init_db()
    await database.init_db()  # 두 번째 호출도 정상이어야 한다

    async with aiosqlite.connect(_tmp_db_path) as db:
        cursor = await db.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        )
        tables = [row[0] for row in await cursor.fetchall()]

    assert "exchange_rates" in tables
    assert "market_indices" in tables


# ------------------------------------------------------------------
# save_exchange_rates 테스트
# ------------------------------------------------------------------


@pytest.mark.asyncio
async def test_save_exchange_rates():
    """save_exchange_rates()가 데이터를 정상 저장하는지 확인한다."""
    await database.init_db()

    sample_rates = [
        {
            "currency": "USD",
            "rate": 1350.50,
            "change_value": 5.30,
            "change_percent": 0.39,
            "collected_at": "2026-03-25T09:30:00+09:00",
        },
        {
            "currency": "EUR",
            "rate": 1470.20,
            "change_value": -3.10,
            "change_percent": -0.21,
            "collected_at": "2026-03-25T09:30:00+09:00",
        },
    ]

    await database.save_exchange_rates(sample_rates)

    async with aiosqlite.connect(_tmp_db_path) as db:
        cursor = await db.execute(
            "SELECT currency, rate, change_value, change_percent, collected_at FROM exchange_rates ORDER BY currency"
        )
        rows = await cursor.fetchall()

    assert len(rows) == 2

    # EUR이 알파벳순으로 먼저 온다
    assert rows[0][0] == "EUR"
    assert rows[0][1] == 1470.20

    assert rows[1][0] == "USD"
    assert rows[1][1] == 1350.50


@pytest.mark.asyncio
async def test_save_exchange_rates_empty():
    """빈 리스트를 전달하면 아무 데이터도 저장되지 않는다."""
    await database.init_db()
    await database.save_exchange_rates([])

    async with aiosqlite.connect(_tmp_db_path) as db:
        cursor = await db.execute("SELECT COUNT(*) FROM exchange_rates")
        count = (await cursor.fetchone())[0]

    assert count == 0


# ------------------------------------------------------------------
# save_market_indices 테스트
# ------------------------------------------------------------------


@pytest.mark.asyncio
async def test_save_market_indices():
    """save_market_indices()가 데이터를 정상 저장하는지 확인한다."""
    await database.init_db()

    sample_indices = [
        {
            "index_name": "코스피",
            "country": "한국",
            "value": 2650.30,
            "change_value": 12.50,
            "change_percent": 0.47,
            "collected_at": "2026-03-25T09:30:00+09:00",
        },
        {
            "index_name": "나스닥",
            "country": "미국",
            "value": 18200.75,
            "change_value": -85.20,
            "change_percent": -0.47,
            "collected_at": "2026-03-25T09:30:00+09:00",
        },
    ]

    await database.save_market_indices(sample_indices)

    async with aiosqlite.connect(_tmp_db_path) as db:
        cursor = await db.execute(
            "SELECT index_name, country, value, change_value, change_percent, collected_at FROM market_indices ORDER BY index_name"
        )
        rows = await cursor.fetchall()

    assert len(rows) == 2

    # index_name 알파벳순: 나스닥 < 코스피 (유니코드 기준)
    names = [row[0] for row in rows]
    assert "코스피" in names
    assert "나스닥" in names

    # 코스피 데이터 검증
    kospi_row = [r for r in rows if r[0] == "코스피"][0]
    assert kospi_row[1] == "한국"
    assert kospi_row[2] == 2650.30
    assert kospi_row[3] == 12.50


@pytest.mark.asyncio
async def test_save_market_indices_empty():
    """빈 리스트를 전달하면 아무 데이터도 저장되지 않는다."""
    await database.init_db()
    await database.save_market_indices([])

    async with aiosqlite.connect(_tmp_db_path) as db:
        cursor = await db.execute("SELECT COUNT(*) FROM market_indices")
        count = (await cursor.fetchone())[0]

    assert count == 0
