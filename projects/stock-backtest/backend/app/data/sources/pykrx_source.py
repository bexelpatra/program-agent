"""pykrx 기반 DataSource 구현체 — KR 주식 / ETF.

ticker 형식: 한국거래소 6자리 종목코드 (예: '069500' = KODEX 200).
yfinance 와 달리 .KS / .KQ 접미사 없음.

Rate limit: V1 결정 9 — pykrx 세션당 100ms sleep (yfinance 보다 관대).
공용 헬퍼는 ``_helpers`` 모듈에 응집되어 있다.

수집 레이어 방어 (architecture.md V3 § 비거래일 방어):
- close=0 / null / NaN 인 일봉 행은 어댑터에서 거부 + WARNING 로깅.

배당 (분배금):
- pykrx 는 ETF 분배금/주식 배당을 종합 API 로 제공하지 않음. MVP 는 빈 리스트
  반환하며 BLOCKER-002 (SOFT) 로 등록되어 있음. 한국 ETF 백테스트 시 배당 수익
  누락됨을 UI 에서 명시 필요 (UI/UX 원칙 2).
"""
from __future__ import annotations

import logging
from datetime import date, datetime, timedelta, timezone
from typing import Any

from pykrx import stock

from ._helpers import RateLimiter, is_invalid_close, safe_float
from .base import DividendEvent, OhlcvBar, TickerValidation

logger = logging.getLogger(__name__)

# V1 결정 9: pykrx 세션당 100ms sleep (yfinance 0.5s 보다 관대)
_rate_limiter = RateLimiter(0.1)


def _rate_limit() -> None:
    _rate_limiter.wait()


# pykrx 가 반환하는 naive datetime 에 부여할 한국 표준시 (UTC+9)
_KST = timezone(timedelta(hours=9))


def _to_kst(ts: Any) -> datetime:
    """pykrx 인덱스를 timezone-aware datetime (KST) 으로 변환.

    pandas Timestamp / datetime / date 등 다양한 입력을 허용한다.
    이미 timezone 이 있으면 그대로 사용한다.
    """
    if hasattr(ts, "to_pydatetime"):
        py = ts.to_pydatetime()
    elif isinstance(ts, datetime):
        py = ts
    else:
        # date 인 경우 자정 KST 로 변환
        py = datetime(ts.year, ts.month, ts.day)
    if py.tzinfo is None:
        return py.replace(tzinfo=_KST)
    return py


class PykrxSource:
    """KR 주식/ETF OHLCV 어댑터.

    ticker 형식: 한국거래소 6자리 코드 (예: '069500' = KODEX 200).
    timezone: KST (UTC+9) 강제 부여.
    수정주가: pykrx 의 기본 get_market_ohlcv 는 비조정가. MVP 임시 처방 — split/dividend
    비반영 (한국 ETF 는 분할이 거의 없어 실전 영향 적음). 정공법(SPLIT 이벤트 →
    portfolio.qty 조정 + pykrx 별도 분할 데이터 수집) 은 BLOCKER-003 → Phase 2 백로그.
    """

    def fetch_ohlcv(self, symbol: str, start: date, end: date) -> list[OhlcvBar]:
        _rate_limit()
        df = stock.get_market_ohlcv(
            start.strftime("%Y%m%d"),
            end.strftime("%Y%m%d"),
            symbol,
        )
        if df is None or df.empty:
            return []
        bars: list[OhlcvBar] = []
        for ts, row in df.iterrows():
            close = row.get("종가")
            if is_invalid_close(close):
                logger.warning(
                    "rejected close=0/null/NaN bar symbol=%s time=%s", symbol, ts
                )
                continue
            close_f = float(close)
            bars.append(
                OhlcvBar(
                    time=_to_kst(ts),
                    open=safe_float(row.get("시가")),
                    high=safe_float(row.get("고가")),
                    low=safe_float(row.get("저가")),
                    close=close_f,
                    # MVP: pykrx 비조정 종가를 adj_close 로도 사용
                    # (split/dividend 보정은 향후 별도 호출 필요)
                    adj_close=close_f,
                    volume=safe_float(row.get("거래량")),
                )
            )
        return bars

    def fetch_dividends(
        self, symbol: str, start: date, end: date
    ) -> list[DividendEvent]:
        """배당/분배금 — MVP 빈 구현 (BLOCKER-002 SOFT).

        pykrx 가 ETF 분배금/주식 배당을 종합 API 로 제공하지 않음.
        한국 ETF 백테스트 시 배당 수익이 누락된다 — UI 에 "KR 자산은 배당 미반영"
        고지 필요 (UI/UX 원칙 2).
        향후 KRX 정보시스템 분배금 API 또는 별도 어댑터로 보강.
        """
        logger.info(
            "pykrx dividends not implemented for symbol=%s — returning empty (BLOCKER-002 SOFT)",
            symbol,
        )
        return []

    def validate_ticker(self, symbol: str) -> TickerValidation:
        _rate_limit()
        try:
            today = date.today()
            one_year_ago = today - timedelta(days=365)
            df = stock.get_market_ohlcv(
                one_year_ago.strftime("%Y%m%d"),
                today.strftime("%Y%m%d"),
                symbol,
            )
            if df is None or df.empty:
                return TickerValidation(
                    ticker=symbol,
                    exists=False,
                    has_min_history=False,
                    earliest=None,
                    latest=None,
                    note="한국거래소 종목코드가 아니거나 데이터 없음",
                )
            earliest = df.index.min().date()
            latest = df.index.max().date()
            # KR 거래일 ~240/년, 캘린더일 200 이상이면 1년치 충족 (여유)
            has_year = (latest - earliest).days >= 200
            return TickerValidation(
                ticker=symbol,
                exists=True,
                has_min_history=has_year,
                earliest=earliest,
                latest=latest,
                note=None if has_year else "최소 1년치 데이터 부족",
            )
        except Exception as exc:  # 네트워크/pykrx 내부 예외 광범위 처리
            return TickerValidation(
                ticker=symbol,
                exists=False,
                has_min_history=False,
                earliest=None,
                latest=None,
                note=f"검증 실패: {exc}",
            )

    def earliest_available(self, symbol: str) -> date | None:
        """pykrx 가 알려주는 자산의 가장 오래된 일봉 날짜.

        TASK-213: pykrx 는 yfinance 의 period='max' 같은 옵션이 없어
        넉넉한 과거 시점(1995-01-01) 부터 today 까지 한 번에 조회 후 첫 행 사용.
        한국거래소 일봉 시계열은 1995년경 시작이므로 이 시작일로 사실상 모든 과거를 커버.
        예외는 None 으로 흡수 + warning 로깅 → 호출자 fallback 활성.
        """
        _rate_limit()
        try:
            historical_start = date(1995, 1, 1)
            today = date.today()
            df = stock.get_market_ohlcv(
                historical_start.strftime("%Y%m%d"),
                today.strftime("%Y%m%d"),
                symbol,
            )
            if df is None or df.empty:
                return None
            return df.index.min().date()
        except Exception as exc:  # noqa: BLE001 - 외부 어댑터 경계
            logger.warning(
                "earliest_available failed for symbol=%s: %s", symbol, exc
            )
            return None
