"""
test_scraper.py - scraper.py 모듈 테스트

네이버증권에 실제 HTTP 요청을 보내는 라이브 테스트이다.
네트워크 환경에 따라 실패할 수 있다.
"""

import os
import sys

import pytest

# src/ 디렉토리를 sys.path에 추가
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from scraper import fetch_exchange_rates, fetch_market_indices


# ------------------------------------------------------------------
# fetch_exchange_rates 라이브 테스트
# ------------------------------------------------------------------


@pytest.mark.asyncio
async def test_fetch_exchange_rates_returns_list():
    """fetch_exchange_rates()가 list를 반환하는지 확인한다."""
    result = await fetch_exchange_rates()
    assert isinstance(result, list)


@pytest.mark.asyncio
async def test_fetch_exchange_rates_non_empty():
    """fetch_exchange_rates()가 비어 있지 않은 리스트를 반환하는지 확인한다."""
    result = await fetch_exchange_rates()
    assert len(result) > 0, "환율 데이터가 비어 있음 — 네트워크 또는 페이지 구조 변경 확인 필요"


@pytest.mark.asyncio
async def test_fetch_exchange_rates_dict_keys():
    """반환된 각 dict가 올바른 키를 포함하는지 확인한다."""
    result = await fetch_exchange_rates()
    expected_keys = {"currency", "rate", "change_value", "change_percent"}

    for item in result:
        assert isinstance(item, dict)
        assert expected_keys.issubset(
            item.keys()
        ), f"누락된 키: {expected_keys - item.keys()}"


@pytest.mark.asyncio
async def test_fetch_exchange_rates_currency_values():
    """반환된 통화 코드가 TARGET_CURRENCIES에 속하는지 확인한다."""
    from config import TARGET_CURRENCIES

    result = await fetch_exchange_rates()
    for item in result:
        assert item["currency"] in TARGET_CURRENCIES, f"예상 외 통화: {item['currency']}"


@pytest.mark.asyncio
async def test_fetch_exchange_rates_rate_positive():
    """환율 값이 양수인지 확인한다."""
    result = await fetch_exchange_rates()
    for item in result:
        assert item["rate"] > 0, f"{item['currency']} 환율이 0 이하: {item['rate']}"


# ------------------------------------------------------------------
# fetch_market_indices 라이브 테스트
# ------------------------------------------------------------------


@pytest.mark.asyncio
async def test_fetch_market_indices_returns_list():
    """fetch_market_indices()가 list를 반환하는지 확인한다."""
    result = await fetch_market_indices()
    assert isinstance(result, list)


@pytest.mark.asyncio
async def test_fetch_market_indices_non_empty():
    """fetch_market_indices()가 비어 있지 않은 리스트를 반환하는지 확인한다."""
    result = await fetch_market_indices()
    assert len(result) > 0, "세계지수 데이터가 비어 있음 — 네트워크 또는 페이지 구조 변경 확인 필요"


@pytest.mark.asyncio
async def test_fetch_market_indices_dict_keys():
    """반환된 각 dict가 올바른 키를 포함하는지 확인한다."""
    result = await fetch_market_indices()
    expected_keys = {"index_name", "country", "value", "change_value", "change_percent"}

    for item in result:
        assert isinstance(item, dict)
        assert expected_keys.issubset(
            item.keys()
        ), f"누락된 키: {expected_keys - item.keys()}"


@pytest.mark.asyncio
async def test_fetch_market_indices_value_positive():
    """지수 현재값이 양수인지 확인한다."""
    result = await fetch_market_indices()
    for item in result:
        assert item["value"] > 0, f"{item['index_name']} 값이 0 이하: {item['value']}"
