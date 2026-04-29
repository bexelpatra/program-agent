"""yfinance 기반 DataSource / FxSource 구현체.

- US 주식 / Crypto OHLCV + 배당: YfinanceSource
- KRW=X 등 FX: YfinanceFxSource

Rate limit: V1 결정 9 — 초당 1~2 req 이하. 모듈 레벨 sleep 으로 단순 구현.
추후 token bucket 으로 교체 가능.

수집 레이어 방어: close=0/null/NaN 행은 결과에서 drop + WARNING 로깅
(architecture.md V3 § 비거래일 방어).
"""
from __future__ import annotations

import logging
import time
from datetime import date
from threading import Lock
from typing import Any

import yfinance as yf

from .base import (
    DividendEvent,
    FxBar,
    OhlcvBar,
    TickerValidation,
)

logger = logging.getLogger(__name__)

# V1 결정 9: 초당 ~2 req 이하. 0.5s 간격이면 2 req/s 상한.
_RATE_LIMIT_SLEEP_SEC = 0.5
_rate_lock = Lock()
_last_call_monotonic = [0.0]  # mutable wrapper for lock-protected mutation


def _rate_limit() -> None:
    """모듈 단위 호출 간격 보장. 멀티스레드 안전."""
    with _rate_lock:
        elapsed = time.monotonic() - _last_call_monotonic[0]
        if elapsed < _RATE_LIMIT_SLEEP_SEC:
            time.sleep(_RATE_LIMIT_SLEEP_SEC - elapsed)
        _last_call_monotonic[0] = time.monotonic()


def _is_nan(value: Any) -> bool:
    """NaN 검출 — float NaN 은 자기 자신과 같지 않다."""
    try:
        return value != value
    except Exception:
        return False


def _safe_float(value: Any) -> float | None:
    """None/NaN → None, 그 외 → float."""
    if value is None or _is_nan(value):
        return None
    return float(value)


def _is_invalid_close(close: Any) -> bool:
    """수집 레이어 close 거부 정책: None / NaN / 0 → invalid."""
    if close is None or _is_nan(close):
        return True
    try:
        return float(close) == 0.0
    except (TypeError, ValueError):
        return True


class YfinanceSource:
    """US/Crypto OHLCV + 배당 어댑터.

    crypto ticker 형식: 'BTC-USD', 'ETH-USD' (yfinance 표준).
    timezone 은 yfinance 반환값 그대로 사용 (이미 timezone-aware).
    UTC 정규화는 호출자(저장 레이어) 책임.
    """

    def fetch_ohlcv(self, symbol: str, start: date, end: date) -> list[OhlcvBar]:
        _rate_limit()
        ticker = yf.Ticker(symbol)
        hist = ticker.history(
            start=start.isoformat(), end=end.isoformat(), auto_adjust=False
        )
        bars: list[OhlcvBar] = []
        for ts, row in hist.iterrows():
            close = row.get("Close")
            if _is_invalid_close(close):
                logger.warning(
                    "rejected close=0/null/NaN bar symbol=%s time=%s", symbol, ts
                )
                continue
            bars.append(
                OhlcvBar(
                    time=ts.to_pydatetime(),
                    open=_safe_float(row.get("Open")),
                    high=_safe_float(row.get("High")),
                    low=_safe_float(row.get("Low")),
                    close=float(close),
                    adj_close=_safe_float(row.get("Adj Close")),
                    volume=_safe_float(row.get("Volume")),
                )
            )
        return bars

    def fetch_dividends(
        self, symbol: str, start: date, end: date
    ) -> list[DividendEvent]:
        _rate_limit()
        ticker = yf.Ticker(symbol)
        dividends = ticker.dividends
        events: list[DividendEvent] = []
        for ts, amount in dividends.items():
            event_date = ts.date()
            if start <= event_date <= end and amount > 0:
                events.append(
                    DividendEvent(time=ts.to_pydatetime(), amount=float(amount))
                )
        return events

    def validate_ticker(self, symbol: str) -> TickerValidation:
        _rate_limit()
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="1y")
            if hist.empty:
                return TickerValidation(
                    ticker=symbol,
                    exists=False,
                    has_min_history=False,
                    earliest=None,
                    latest=None,
                    note="데이터 없음",
                )
            earliest = hist.index.min().date()
            latest = hist.index.max().date()
            # 거래일 ~252/년, 캘린더일 기준 300일 이상이면 1년치 충족
            has_year = (latest - earliest).days >= 300
            return TickerValidation(
                ticker=symbol,
                exists=True,
                has_min_history=has_year,
                earliest=earliest,
                latest=latest,
                note=None if has_year else "최소 1년치 데이터 부족",
            )
        except Exception as exc:  # 네트워크/yfinance 내부 예외 광범위 처리
            return TickerValidation(
                ticker=symbol,
                exists=False,
                has_min_history=False,
                earliest=None,
                latest=None,
                note=f"검증 실패: {exc}",
            )


def _fx_symbol(base_ccy: str, quote_ccy: str) -> str:
    """yfinance FX 심볼 규칙.

    'USD' base 인 경우: '{quote}=X' (예: KRW=X 는 USD/KRW)
    그 외: '{base}{quote}=X' (예: EURKRW=X)
    """
    if base_ccy == "USD":
        return f"{quote_ccy}=X"
    return f"{base_ccy}{quote_ccy}=X"


class YfinanceFxSource:
    """yfinance 기반 환율 어댑터."""

    def fetch_fx(
        self, base_ccy: str, quote_ccy: str, start: date, end: date
    ) -> list[FxBar]:
        symbol = _fx_symbol(base_ccy, quote_ccy)
        _rate_limit()
        hist = yf.Ticker(symbol).history(
            start=start.isoformat(), end=end.isoformat()
        )
        bars: list[FxBar] = []
        for ts, row in hist.iterrows():
            rate = row.get("Close")
            if _is_invalid_close(rate):
                logger.warning(
                    "rejected fx close=0/null/NaN base=%s quote=%s time=%s",
                    base_ccy,
                    quote_ccy,
                    ts,
                )
                continue
            bars.append(
                FxBar(
                    time=ts.to_pydatetime(),
                    base_ccy=base_ccy,
                    quote_ccy=quote_ccy,
                    rate=float(rate),
                )
            )
        return bars

    def validate_pair(self, base_ccy: str, quote_ccy: str) -> bool:
        try:
            today = date.today()
            sample = self.fetch_fx(base_ccy, quote_ccy, today.replace(day=1), today)
            return len(sample) > 0
        except Exception:
            return False
