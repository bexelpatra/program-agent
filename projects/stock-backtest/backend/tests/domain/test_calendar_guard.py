"""calendar_guard public API 단위 테스트 (TASK-233).

`get_calendar_name` 은 unknown market 입력 시 raise 하지 않고 None 을 반환해야 한다.
이 graceful 동작은 `app/data/pipeline.py:_trading_days` 가 미지원 market 을 "거래일 0"
으로 처리해 호출자가 REJECTED 분류로 진행할 수 있게 보장한다.

기존 `_resolve_calendar_name` (모듈 사적 함수) 은 ValueError raise 정책을 유지하므로
별도 테스트 대상은 아니다 (TASK-233 변경 범위 외).
"""
from __future__ import annotations

from app.domain.asset.calendar_guard import get_calendar_name


class TestGetCalendarNameKnownMarkets:
    """알려진 market 코드가 정확한 캘린더명에 매핑되는지."""

    def test_kr_returns_xkrx(self) -> None:
        assert get_calendar_name("KR") == "XKRX"

    def test_us_returns_xnys(self) -> None:
        assert get_calendar_name("US") == "XNYS"

    def test_crypto_returns_none(self) -> None:
        # CRYPTO 는 24/7 이라 캘린더 불필요 — None 이 정답.
        assert get_calendar_name("CRYPTO") is None


class TestGetCalendarNameUnknownMarket:
    """unknown market 일 때 raise 하지 않고 None 반환."""

    def test_unknown_market_returns_none(self) -> None:
        # pipeline.py:_trading_days 가 dict.get() 으로 graceful fallback 하던
        # 의도를 public 함수로 보존한다.
        assert get_calendar_name("UNKNOWN") is None

    def test_empty_string_returns_none(self) -> None:
        assert get_calendar_name("") is None

    def test_lowercase_kr_returns_none(self) -> None:
        # market 코드는 대문자 표준 — 소문자 변형은 unknown 취급.
        assert get_calendar_name("kr") is None
