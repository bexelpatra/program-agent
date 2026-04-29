"""비거래일 방어 — 조회 레이어.

architecture.md V3 § "거래 정책" + § "에이전트 위임 영역" 에 따라 사용자/전략이 비거래일을
입력했을 때 정책적으로 처리한다. exchange_calendars 는 도메인 정책에 본질적이므로
domain 에서 직접 import 허용 (라이브러리 dependency injection 으로 분리할 가치는 낮음).

엔진 레이어의 멀티마켓 캘린더 정렬(`backend/app/domain/calendar.py`, TASK-042)과는 별개:
이쪽은 **단일 시점 입력의 방어** 만 담당한다.
"""
from __future__ import annotations

from datetime import date
from typing import Literal

import exchange_calendars as xcals

# 조회 모드:
# - "raise": 비거래일이면 ValueError
# - "snap_previous": 직전 거래일로 보정
# - "snap_next": 다음 거래일로 보정
GuardMode = Literal["raise", "snap_previous", "snap_next"]

# 시장 코드 → exchange_calendars 코드. CRYPTO 는 24/7 이라 캘린더 불필요.
_MARKET_CALENDARS: dict[str, str | None] = {
    "KR": "XKRX",
    "US": "XNYS",
    "CRYPTO": None,
}


def _resolve_calendar_name(market: str) -> str | None:
    if market not in _MARKET_CALENDARS:
        raise ValueError(f"Unknown market: {market!r}. Expected one of {list(_MARKET_CALENDARS)}.")
    return _MARKET_CALENDARS[market]


def is_trading_day(market: str, target: date) -> bool:
    """주어진 날짜가 해당 시장의 거래일인지.

    CRYPTO 는 24/7 이므로 항상 True.
    """
    cal_name = _resolve_calendar_name(market)
    if cal_name is None:
        return True
    cal = xcals.get_calendar(cal_name)
    return cal.is_session(target.isoformat())


def guard_trading_day(
    market: str,
    target: date,
    mode: GuardMode = "snap_previous",
) -> date:
    """비거래일 입력 방어.

    Args:
        market: KR / US / CRYPTO.
        target: 점검할 날짜.
        mode: 처리 정책 (raise / snap_previous / snap_next).

    Returns:
        target 이 거래일이면 그대로, 아니면 정책에 따른 인접 거래일.

    Raises:
        ValueError: mode == "raise" 이고 target 이 비거래일인 경우.
    """
    if is_trading_day(market, target):
        return target

    if mode == "raise":
        raise ValueError(f"{target.isoformat()} is not a trading day for market {market!r}.")

    cal_name = _resolve_calendar_name(market)
    # CRYPTO 는 is_trading_day 가 항상 True 라 여기 도달 불가 — 방어적 분기 생략.
    assert cal_name is not None  # type narrowing; CRYPTO 는 위에서 처리됨
    cal = xcals.get_calendar(cal_name)

    direction: Literal["previous", "next"] = (
        "previous" if mode == "snap_previous" else "next"
    )
    snapped = cal.date_to_session(target.isoformat(), direction=direction)
    return snapped.date()
