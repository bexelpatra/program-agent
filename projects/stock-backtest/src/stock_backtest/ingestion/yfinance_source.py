"""yfinance 기반 DataSource 구현.

yfinance 라이브러리를 감싸 :class:`DataSource` 추상 인터페이스를 충족한다.
지원 시장: ``US``, ``CRYPTO``, ``COMMODITY``, ``FX``.

설계 요점
---------
- ``fetch_ohlcv`` / ``fetch_fx`` 는 소스 스키마를 base.py docstring 규약에 맞춰
  정규화(소문자 컬럼, ``time`` 컬럼)한다.
- rate limit 는 이 모듈 레벨에서 **최소 호출 간격**(``min_interval_seconds``)을
  유지하는 방식으로 구현한다(단일 인스턴스 기준 토큰 버킷 역할).
- 재시도는 수행하지 않는다. 파이프라인 레이어(``ingestion/pipeline.py``)가
  지수 백오프로 재시도하는 설계(architecture.md §9).
- yfinance 가 발생시키는 rate limit 계열 예외/HTTP 429 는 :class:`RateLimitError`
  로 래핑한다. 알려지지 않은 예외는 :class:`DataSourceError` 로 래핑한다.
- ``list_symbols`` 는 yfinance 가 심볼 디렉토리를 제공하지 않으므로
  빈 리스트를 반환한다(docstring 에 명시). 상위 레이어는 ``assets`` 테이블을
  심볼 소스로 사용한다.
"""

from __future__ import annotations

import logging
import threading
import time
from datetime import date, timedelta
from typing import List

import pandas as pd

from ..config import Settings, load_config
from .base import DataSource, DataSourceError, RateLimitError, SymbolNotFoundError


logger = logging.getLogger(__name__)


_DEFAULT_MIN_INTERVAL_SECONDS = 0.7

_OHLCV_COLUMNS = ["time", "open", "high", "low", "close", "adj_close", "volume"]
_FX_COLUMNS = ["time", "rate"]

_SUPPORTED_OHLCV_MARKETS = {"US", "CRYPTO", "COMMODITY", "FX"}


def _looks_like_rate_limit(exc: BaseException) -> bool:
    """문자열 기반 rate-limit 탐지.

    yfinance 는 버전에 따라 rate limit 에 대한 전용 예외 클래스가 없거나
    바뀌어 왔다. 메시지/표현에서 ``rate limit``, ``429``, ``too many requests``
    키워드가 나타나면 rate limit 으로 간주한다.
    """

    text = f"{type(exc).__name__}: {exc}".lower()
    needles = ("rate limit", "too many requests", "429", "throttle")
    return any(n in text for n in needles)


class YFinanceSource(DataSource):
    """yfinance 기반 :class:`DataSource` 구현체.

    Parameters
    ----------
    min_interval_seconds : float | None, optional
        연속 호출 사이 최소 대기 시간(초). ``None`` 이면 아래 순서로 해석.

        1. ``load_config()`` 로 설정을 읽어 ``ingestion.rate_limit.yfinance_requests_per_sec``
           의 역수를 사용.
        2. 설정 로딩 실패 시 기본값 ``0.7`` 초.

    Notes
    -----
    인스턴스는 스레드 세이프한 내부 락으로 호출 간격을 유지한다.
    """

    source_name: str = "yfinance"

    def __init__(self, min_interval_seconds: float | None = None) -> None:
        self._min_interval_seconds = self._resolve_min_interval(min_interval_seconds)
        self._lock = threading.Lock()
        self._last_call_monotonic: float | None = None

        # Import 지연: 모듈 import 시점에 yfinance 가 네트워크 리소스(캐시
        # 디렉토리 생성 등)에 접근하는 것을 피하기 위해 지연 import.
        try:
            import yfinance  # noqa: F401
        except ImportError as exc:  # pragma: no cover - requirements.txt 에 포함됨
            raise DataSourceError(
                "yfinance 패키지가 설치되어 있지 않습니다. " "requirements.txt 를 확인하세요."
            ) from exc

    # ------------------------------------------------------------------
    # 공용 (DataSource 인터페이스 구현)
    # ------------------------------------------------------------------

    def fetch_ohlcv(
        self,
        symbol: str,
        market: str,
        start: date,
        end: date,
    ) -> pd.DataFrame:
        """일봉 OHLCV 조회.

        Parameters
        ----------
        symbol : str
            yfinance 심볼. 암호화폐는 ``BTC-USD`` 형태, 일반 US 티커는 ``SPY``,
            원자재 ETF 는 ``GLD`` 등.
        market : str
            ``"US"``, ``"CRYPTO"``, ``"COMMODITY"``, ``"FX"`` 중 하나.
        start : datetime.date
            조회 시작일(포함).
        end : datetime.date
            조회 종료일(포함).

        Returns
        -------
        pandas.DataFrame
            ``time, open, high, low, close, adj_close, volume`` 컬럼.
            비거래일은 포함되지 않는다. 데이터가 없어도 이 스키마의 빈
            DataFrame 을 반환하는 것이 원칙이나, 심볼 자체가 잘못된 경우는
            :class:`SymbolNotFoundError` 를 발생시킨다.
        """

        if market not in _SUPPORTED_OHLCV_MARKETS:
            raise DataSourceError(
                f"YFinanceSource 는 market={market!r} 를 지원하지 않습니다. "
                f"지원 시장: {sorted(_SUPPORTED_OHLCV_MARKETS)}"
            )

        # yfinance 의 download 는 end 가 **exclusive** 이므로 +1 일 보정.
        yf_end = end + timedelta(days=1)

        df = self._yf_download(symbol=symbol, start=start, end=yf_end)

        if df is None or df.empty:
            # 빈 응답을 symbol not found 로 해석 (base.py 규약).
            raise SymbolNotFoundError(
                f"yfinance 가 (symbol={symbol!r}, market={market!r}) 에 대해 "
                f"빈 결과를 반환했습니다."
            )

        return self._normalize_ohlcv(df)

    def fetch_fx(
        self,
        base_ccy: str,
        quote_ccy: str,
        start: date,
        end: date,
    ) -> pd.DataFrame:
        """환율 시계열 조회.

        yfinance 심볼 규약 ``{base}{quote}=X`` 를 사용한다
        (예: ``USDKRW=X`` = "1 USD 당 KRW 가격").

        Returns
        -------
        pandas.DataFrame
            ``time, rate`` 컬럼. ``rate`` 의 정의는 "1 base_ccy = rate quote_ccy".
        """

        pair_symbol = f"{base_ccy.upper()}{quote_ccy.upper()}=X"
        yf_end = end + timedelta(days=1)

        df = self._yf_download(symbol=pair_symbol, start=start, end=yf_end)

        if df is None or df.empty:
            raise SymbolNotFoundError(
                f"yfinance 가 FX 페어 {pair_symbol!r} 에 대해 빈 결과를 반환했습니다."
            )

        return self._normalize_fx(df)

    def list_symbols(self, market: str) -> List[str]:
        """심볼 목록 조회.

        yfinance 는 공식적인 심볼 디렉토리 API 를 제공하지 않는다. 상위 레이어
        (``assets`` 테이블, 수집 파이프라인)가 심볼 목록을 관리하므로 여기서는
        항상 빈 리스트를 반환한다. ``NotImplementedError`` 를 던지지 않는 이유는
        호출자가 단순히 "지원하지 않는 시장" 과 동일하게 처리하도록 하기 위함.
        """

        return []

    # ------------------------------------------------------------------
    # 내부
    # ------------------------------------------------------------------

    @staticmethod
    def _resolve_min_interval(explicit: float | None) -> float:
        if explicit is not None:
            if explicit < 0:
                raise ValueError("min_interval_seconds 는 0 이상이어야 합니다.")
            return float(explicit)

        try:
            settings: Settings = load_config()
            rps = settings.ingestion.rate_limit.yfinance_requests_per_sec
            if rps > 0:
                return 1.0 / float(rps)
        except Exception:  # pragma: no cover - config 미존재/손상 시 fallback
            logger.debug(
                "YFinanceSource: config 로드 실패, 기본 min_interval 사용",
                exc_info=True,
            )

        return _DEFAULT_MIN_INTERVAL_SECONDS

    def _throttle(self) -> None:
        """마지막 호출 이후 ``min_interval_seconds`` 가 지나도록 대기."""

        if self._min_interval_seconds <= 0:
            return

        with self._lock:
            now = time.monotonic()
            if self._last_call_monotonic is not None:
                elapsed = now - self._last_call_monotonic
                remaining = self._min_interval_seconds - elapsed
                if remaining > 0:
                    time.sleep(remaining)
                    now = time.monotonic()
            self._last_call_monotonic = now

    def _yf_download(
        self,
        symbol: str,
        start: date,
        end: date,
    ) -> pd.DataFrame | None:
        """``yfinance.download`` 호출 래퍼. rate limit / 예외 래핑 수행."""

        import yfinance as yf

        self._throttle()
        try:
            df = yf.download(
                symbol,
                start=start,
                end=end,
                auto_adjust=False,
                progress=False,
                actions=False,
                threads=False,
            )
        except Exception as exc:
            if _looks_like_rate_limit(exc):
                raise RateLimitError(f"yfinance rate limit: {exc}") from exc
            raise DataSourceError(f"yfinance 호출 실패 (symbol={symbol!r}): {exc}") from exc

        return df

    @staticmethod
    def _normalize_ohlcv(raw: pd.DataFrame) -> pd.DataFrame:
        """yfinance 의 multi-level / 혼합 케이스 DataFrame 을 규약 스키마로 변환."""

        df = raw.copy()

        # yfinance 는 단일 심볼에 대해서도 종종 MultiIndex columns 를 반환.
        if isinstance(df.columns, pd.MultiIndex):
            # (field, ticker) 의 0 번째 레벨만 사용.
            df.columns = df.columns.get_level_values(0)

        # 컬럼명 정규화.
        rename_map = {
            "Open": "open",
            "High": "high",
            "Low": "low",
            "Close": "close",
            "Adj Close": "adj_close",
            "Volume": "volume",
        }
        df = df.rename(columns=rename_map)

        # ``Adj Close`` 가 없는 경우 (auto_adjust=True 인 과거 버전 호환용) close 복사.
        if "adj_close" not in df.columns and "close" in df.columns:
            df["adj_close"] = df["close"]

        df = df.reset_index().rename(columns={"Date": "time", "Datetime": "time"})

        # 필요한 컬럼만 선택 (존재하는 것만).
        available = [c for c in _OHLCV_COLUMNS if c in df.columns]
        df = df[available]

        # 빠진 컬럼이 있으면 NaN 으로 채워 스키마 충족.
        for col in _OHLCV_COLUMNS:
            if col not in df.columns:
                df[col] = pd.NA

        df = df[_OHLCV_COLUMNS]

        # close 가 모두 NaN/null/0 인 행 제거는 상위 ingestion 레이어에서 수행.
        df = df.dropna(subset=["close"])
        df = df.sort_values("time").reset_index(drop=True)

        return df

    @staticmethod
    def _normalize_fx(raw: pd.DataFrame) -> pd.DataFrame:
        """FX DataFrame 정규화 — ``time, rate`` 컬럼으로 축약."""

        df = raw.copy()
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        df = df.reset_index().rename(columns={"Date": "time", "Datetime": "time"})

        # rate 는 Close 우선, 없으면 Adj Close 사용.
        if "Close" in df.columns:
            df["rate"] = df["Close"]
        elif "Adj Close" in df.columns:
            df["rate"] = df["Adj Close"]
        else:
            raise DataSourceError("yfinance FX 응답에서 Close/Adj Close 컬럼을 찾을 수 없습니다.")

        df = df[["time", "rate"]].dropna(subset=["rate"])
        df = df.sort_values("time").reset_index(drop=True)
        return df


__all__ = ["YFinanceSource"]
