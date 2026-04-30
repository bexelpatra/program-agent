"""yfinance 기반 DataSource / FxSource 구현체.

- US 주식 / Crypto OHLCV + 배당: YfinanceSource
- KRW=X 등 FX: YfinanceFxSource

Rate limit: V1 결정 9 — 초당 1~2 req 이하. 0.5s 간격이면 2 req/s 상한.
공용 헬퍼는 ``_helpers`` 모듈에 응집되어 있다.

수집 레이어 방어: close=0/null/NaN 행은 결과에서 drop + WARNING 로깅
(architecture.md V3 § 비거래일 방어).
"""
from __future__ import annotations

import logging
from datetime import date

import yfinance as yf

from ._helpers import RateLimiter, is_invalid_close, safe_float
from .base import (
    DividendEvent,
    FxBar,
    OhlcvBar,
    TickerValidation,
)

logger = logging.getLogger(__name__)

# V1 결정 9: 초당 ~2 req 이하. 0.5s 간격이면 2 req/s 상한.
_rate_limiter = RateLimiter(0.5)


# 회귀 테스트(test_calendar_defense.py)가 monkeypatch 로 `_rate_limit` 을 교체하기
# 때문에 module-level 심볼을 유지한다. 함수 본체는 인스턴스 메서드로 위임.
def _rate_limit() -> None:
    _rate_limiter.wait()


# 회귀 테스트가 module 경로로 직접 import (`from app.data.sources.yfinance_source
# import _is_invalid_close`) 하므로 backward-compatible alias 를 유지한다.
_is_invalid_close = is_invalid_close
_safe_float = safe_float


class YfinanceSource:
    """US/Crypto OHLCV + 배당 어댑터.

    crypto ticker 형식: 'BTC-USD', 'ETH-USD' (yfinance 표준).
    timezone 은 yfinance 반환값 그대로 사용 (이미 timezone-aware).
    UTC 정규화는 호출자(저장 레이어) 책임.

    수정주가 (TASK-214 MVP 임시처방):
    - `auto_adjust=True` 로 close 자체가 split/dividend 소급 보정된 가격을 반환.
    - OhlcvBar.close 만 사용하면 분할 시 가짜 시그널 발동 방지 (엔진은 close 만 사용).
    - auto_adjust=True 일 때 yfinance 는 'Adj Close' 컬럼을 'Close' 와 동일 값으로
      채우거나 누락시킴. 호환성을 위해 OhlcvBar.adj_close 는 그대로 매핑.
    - 정공법(corporate_actions SPLIT 이벤트를 매일 EOD 시점에 portfolio.position.qty
      에 적용 + pykrx 별도 분할 데이터 수집) 은 BLOCKER-003 → Phase 2 백로그.
    """

    def fetch_ohlcv(self, symbol: str, start: date, end: date) -> list[OhlcvBar]:
        _rate_limit()
        ticker = yf.Ticker(symbol)
        hist = ticker.history(
            start=start.isoformat(), end=end.isoformat(), auto_adjust=True
        )
        bars: list[OhlcvBar] = []
        for ts, row in hist.iterrows():
            close = row.get("Close")
            if is_invalid_close(close):
                logger.warning(
                    "rejected close=0/null/NaN bar symbol=%s time=%s", symbol, ts
                )
                continue
            # auto_adjust=True 일 때 yfinance 가 'Adj Close' 컬럼을 누락할 수
            # 있어 close 값으로 fallback (둘은 정의상 동일).
            adj_close_raw = row.get("Adj Close")
            adj_close = (
                safe_float(adj_close_raw)
                if adj_close_raw is not None
                else float(close)
            )
            bars.append(
                OhlcvBar(
                    time=ts.to_pydatetime(),
                    open=safe_float(row.get("Open")),
                    high=safe_float(row.get("High")),
                    low=safe_float(row.get("Low")),
                    close=float(close),
                    adj_close=adj_close,
                    volume=safe_float(row.get("Volume")),
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

    def earliest_available(self, symbol: str) -> date | None:
        """yfinance period='max' 의 첫 인덱스 날짜.

        TASK-213: 백필 시작일을 소스가 알려주는 가장 오래된 데이터 날짜로 사용.
        네트워크/내부 예외는 None 으로 흡수 + warning 로깅 → 호출자 fallback 활성.
        """
        _rate_limit()
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="max", auto_adjust=False)
            if hist.empty:
                return None
            return hist.index.min().date()
        except Exception as exc:  # noqa: BLE001 - 외부 어댑터 경계
            logger.warning(
                "earliest_available failed for symbol=%s: %s", symbol, exc
            )
            return None


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
            if is_invalid_close(rate):
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
