"""pipeline._resolve_start 단위 테스트 (TASK-213).

신규 자산 백필 시작일 정책:
- source.earliest_available(symbol) 결과가 있으면 그 날짜 사용
- None 이면 DEFAULT_MAX_LOOKBACK_DAYS fallback
- source/symbol 미제공이면 fallback (역호환)
"""
from __future__ import annotations

from datetime import date, datetime, timedelta
from typing import Any

import pytest

from app.data.pipeline import DEFAULT_MAX_LOOKBACK_DAYS, _resolve_start


class _MockSource:
    """earliest_available 만 모킹하는 최소 DataSource."""

    def __init__(self, earliest: date | None, raise_exc: Exception | None = None):
        self._earliest = earliest
        self._raise_exc = raise_exc
        self.calls: list[str] = []

    def fetch_ohlcv(
        self, symbol: str, start: date, end: date
    ) -> list[Any]:  # pragma: no cover
        return []

    def fetch_dividends(
        self, symbol: str, start: date, end: date
    ) -> list[Any]:  # pragma: no cover
        return []

    def validate_ticker(self, symbol: str) -> Any:  # pragma: no cover
        return None

    def earliest_available(self, symbol: str) -> date | None:
        self.calls.append(symbol)
        if self._raise_exc is not None:
            raise self._raise_exc
        return self._earliest


def test_new_asset_uses_earliest_available_when_present() -> None:
    """신규 자산 (latest=None) + source.earliest_available 결과 있음 → 그 날짜 사용."""
    end = date(2026, 4, 30)
    earliest = date(2014, 9, 17)  # BTC-USD 실제 첫 일봉 날짜
    source = _MockSource(earliest=earliest)

    start = _resolve_start(
        latest=None,
        end=end,
        max_lookback_days=DEFAULT_MAX_LOOKBACK_DAYS,
        source=source,
        symbol="BTC-USD",
    )

    assert start == earliest
    assert source.calls == ["BTC-USD"]


def test_new_asset_falls_back_to_max_lookback_when_earliest_none() -> None:
    """신규 자산 + source.earliest_available 가 None → DEFAULT_MAX_LOOKBACK_DAYS fallback."""
    end = date(2026, 4, 30)
    source = _MockSource(earliest=None)

    start = _resolve_start(
        latest=None,
        end=end,
        max_lookback_days=DEFAULT_MAX_LOOKBACK_DAYS,
        source=source,
        symbol="UNKNOWN",
    )

    expected = end - timedelta(days=DEFAULT_MAX_LOOKBACK_DAYS)
    assert start == expected
    assert source.calls == ["UNKNOWN"]


def test_new_asset_falls_back_when_earliest_raises() -> None:
    """earliest_available 가 예외 발생 → 흡수 후 fallback."""
    end = date(2026, 4, 30)
    source = _MockSource(earliest=None, raise_exc=RuntimeError("network down"))

    start = _resolve_start(
        latest=None,
        end=end,
        max_lookback_days=DEFAULT_MAX_LOOKBACK_DAYS,
        source=source,
        symbol="SPY",
    )

    expected = end - timedelta(days=DEFAULT_MAX_LOOKBACK_DAYS)
    assert start == expected


def test_new_asset_falls_back_when_no_source_provided() -> None:
    """역호환: source/symbol 미제공 시 기존 fallback 동작 유지."""
    end = date(2026, 4, 30)

    start = _resolve_start(
        latest=None,
        end=end,
        max_lookback_days=DEFAULT_MAX_LOOKBACK_DAYS,
    )

    expected = end - timedelta(days=DEFAULT_MAX_LOOKBACK_DAYS)
    assert start == expected


def test_existing_asset_uses_latest_plus_one() -> None:
    """기존 자산 (latest 있음) → latest+1 일. earliest_available 호출 안 함."""
    end = date(2026, 4, 30)
    latest = datetime(2026, 4, 28, 16, 0)
    source = _MockSource(earliest=date(2000, 1, 1))

    start = _resolve_start(
        latest=latest,
        end=end,
        max_lookback_days=DEFAULT_MAX_LOOKBACK_DAYS,
        source=source,
        symbol="SPY",
    )

    assert start == date(2026, 4, 29)
    # 기존 자산은 earliest_available 호출 안 함 (불필요한 네트워크 비용 회피)
    assert source.calls == []


def test_custom_lookback_days_used_when_earliest_none() -> None:
    """fallback 시 custom max_lookback_days 가 적용됨."""
    end = date(2026, 4, 30)
    source = _MockSource(earliest=None)

    start = _resolve_start(
        latest=None,
        end=end,
        max_lookback_days=100,
        source=source,
        symbol="X",
    )

    assert start == end - timedelta(days=100)
