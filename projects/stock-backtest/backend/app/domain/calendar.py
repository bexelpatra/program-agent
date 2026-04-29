"""멀티 마켓 캘린더 정렬.

V3 § "멀티 마켓 캘린더" L549-555:
- 백테스트 기준 캘린더 = base_currency 의 시장 캘린더 (KRW→XKRX, USD→XNYS)
- 비base 시장 자산은 base 캘린더 거래일 행에 직전 자기 시장 거래일 종가 forward-fill
- 암호화폐는 base 캘린더 D 일의 UTC 00:00 종가

V3 § "거래 정책" 모델 A:
- D 일 종가 시그널 → D+1 일 시가 체결
- 멀티 마켓 적용: 각 자산은 자기 시장의 다음 거래일 시가에 체결
"""

from datetime import date, timedelta
from decimal import Decimal
from typing import Mapping

import exchange_calendars as xcals

# base_currency → 시장 캘린더 매핑
BASE_CCY_TO_CALENDAR: dict[str, str] = {
    "KRW": "XKRX",  # Korea Exchange
    "USD": "XNYS",  # NYSE
    # JPY: XJPX, EUR: XAMS 등 미래 확장
}


def base_calendar_name(base_currency: str) -> str:
    """base_currency 의 시장 캘린더 이름. 미지원 통화는 ValueError."""
    name = BASE_CCY_TO_CALENDAR.get(base_currency)
    if name is None:
        raise ValueError(
            f"unsupported base_currency: {base_currency} "
            f"(supported: {list(BASE_CCY_TO_CALENDAR.keys())})"
        )
    return name


def trading_days_in_period(base_currency: str, start: date, end: date) -> list[date]:
    """base_currency 캘린더 기준 [start, end] 거래일 목록. 백테스트 루프 시간축."""
    cal = xcals.get_calendar(base_calendar_name(base_currency))
    sessions = cal.sessions_in_range(start.isoformat(), end.isoformat())
    return [s.date() for s in sessions]


def align_market_price_to_base_calendar(
    market: str,  # 자산 시장 (KR/US/CRYPTO)
    base_currency: str,
    base_date: date,  # base 캘린더의 거래일
    market_prices: Mapping[date, Decimal],  # 자산 시장의 일자별 종가
) -> Decimal | None:
    """base 캘린더의 base_date 행에 표기될 자산 가격을 결정.

    Q14 적용:
    - 자산 시장 == base 시장 (예: KR 자산 + base=KRW): base_date 그대로 사용
    - 자산 시장 != base 시장:
      - 자산 시장의 base_date 거래일이 있으면 그날 종가
      - 없으면 base_date 이전 자기 시장의 가장 최근 거래일 종가 forward-fill
    - CRYPTO: 24/7 시장이므로 base_date 의 UTC 00:00 종가 (또는 forward-fill)

    forward-fill 만 구현 — back-fill 은 look-ahead bias 위험으로 정책상 금지.
    """
    # 직접 일치 시도
    if base_date in market_prices:
        return market_prices[base_date]

    # forward-fill: base_date 이전 가장 최근 날짜
    available = sorted(d for d in market_prices.keys() if d < base_date)
    if not available:
        return None
    return market_prices[available[-1]]


def align_universe_prices(
    universe_market_meta: Mapping[int, str],  # asset_id → market
    universe_market_prices: Mapping[int, Mapping[date, Decimal]],  # asset_id → {date → close}
    base_currency: str,
    base_date: date,
) -> dict[int, Decimal]:
    """universe 전체에 대해 base_date 의 가격 dict 산출. 누락 자산은 결과 dict 에서 제외.

    호출자 (engine.py 또는 trade.py) 가 누락 자산을 NonTradingDayError 또는
    MissingPriceError 로 처리한다.
    """
    out: dict[int, Decimal] = {}
    for asset_id, market in universe_market_meta.items():
        prices = universe_market_prices.get(asset_id, {})
        aligned = align_market_price_to_base_calendar(
            market, base_currency, base_date, prices
        )
        if aligned is not None:
            out[asset_id] = aligned
    return out


def next_trading_day(base_currency: str, target: date) -> date:
    """base 캘린더의 target 다음 거래일. 모델 A 의 D+1 시가 체결일 산출.

    target 이 거래일이면 그 다음 거래일을, 비거래일(주말/공휴일)이면 그 이후
    가장 가까운 거래일을 반환한다. exchange_calendars.next_session() 은 거래일만
    인자로 받으므로 (target+1day) 부터 direction='next' 탐색 패턴을 쓴다.
    """
    cal = xcals.get_calendar(base_calendar_name(base_currency))
    probe = target + timedelta(days=1)
    return cal.date_to_session(probe.isoformat(), direction="next").date()


def previous_trading_day(base_currency: str, target: date) -> date:
    """base 캘린더의 target 직전 거래일.

    target 이 거래일이면 그 직전 거래일을, 비거래일이면 그 이전 가장 가까운
    거래일을 반환한다.
    """
    cal = xcals.get_calendar(base_calendar_name(base_currency))
    probe = target - timedelta(days=1)
    return cal.date_to_session(probe.isoformat(), direction="previous").date()
