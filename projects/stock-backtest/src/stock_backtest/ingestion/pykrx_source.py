"""pykrx 기반 :class:`DataSource` 구현.

한국거래소(KRX) 상장 종목/ETF 및 주요 지수 일봉을 제공하는 `pykrx` 라이브러리를
감싸는 :class:`PykrxSource` 를 정의한다.

설계 참고
---------
- architecture.md §9 데이터 수집 - DB 기반 증분:
  "pykrx는 세션당 100ms sleep" 규약에 따라 호출 간 최소 인터벌을 둔다.
- architecture.md §13 비거래일 방어:
  빈 응답/미지 심볼은 :class:`SymbolNotFoundError` 로 신호한다.

특이사항
--------
- pykrx 는 배당/분할 조정 종가(adj_close)를 별도로 제공하지 않는다.
  본 구현체는 ``adj_close = close`` 로 채우며, 향후 `corporate_actions`
  테이블을 통해 별도 조정 가능성을 열어둔다.
- pykrx 는 FX 시계열을 제공하지 않으므로 :meth:`fetch_fx` 는
  :class:`NotImplementedError` 를 발생시킨다. FX 는 :class:`YFinanceSource`
  를 사용하라.
"""

from __future__ import annotations

import time as _time
from datetime import date, timedelta
from typing import List

import pandas as pd

from .base import (
    DataSource,
    DataSourceError,
    SymbolNotFoundError,
)


# pykrx 한글 컬럼 → 표준 컬럼 매핑.
# OHLCV 시리얼라이즈에 사용.
_OHLCV_COLUMN_MAP = {
    "시가": "open",
    "고가": "high",
    "저가": "low",
    "종가": "close",
    "거래량": "volume",
}

# OHLCV 표준 컬럼 순서 (base.py docstring 준수).
_OHLCV_COLUMNS = ["time", "open", "high", "low", "close", "adj_close", "volume"]


# KR 주요 지수 alias → yfinance 심볼 매핑.
#
# pykrx 1.2.4 시점의 상류 버그로 ``stock.get_index_ohlcv`` 가 KRX API 응답에
# 존재하지 않는 ``'지수명'`` 컬럼을 참조해 ``KeyError`` 를 발생시킨다
# (pykrx 내부 ``util.wrapper`` 의 로깅 경로). 숫자 코드(1001/2001/1028)와
# 알파벳 alias(KS11/KQ11/KS200) 모두 동일한 경로로 실패한다.
#
# pykrx 업스트림 수정이 있기 전까지 KR 지수에 한해 ``yfinance`` 로 폴백한다.
# 경계상 pykrx_source 가 yfinance 를 import 하게 되지만, "KR 지수 경로만
# 깨진" 현재 상황에서 파이프라인 계약(market→source 단일 매핑)을 보존하는
# 최소 침습적 선택이다. 업스트림이 고쳐지면 이 매핑을 제거한다.
_KR_INDEX_YF_FALLBACK: dict[str, str] = {
    "KS11": "^KS11",
    "KQ11": "^KQ11",
    "KS200": "^KS200",
    # 숫자 코드도 혹시 seed 에 등장할 수 있어 같이 매핑.
    "1001": "^KS11",
    "2001": "^KQ11",
    "1028": "^KS200",
}


def _empty_ohlcv() -> pd.DataFrame:
    """표준 OHLCV 스키마를 가진 빈 DataFrame 을 반환한다."""
    return pd.DataFrame(
        {
            "time": pd.Series(dtype="datetime64[ns]"),
            "open": pd.Series(dtype="float64"),
            "high": pd.Series(dtype="float64"),
            "low": pd.Series(dtype="float64"),
            "close": pd.Series(dtype="float64"),
            "adj_close": pd.Series(dtype="float64"),
            "volume": pd.Series(dtype="float64"),
        }
    )


def _is_stock_symbol(symbol: str) -> bool:
    """종목/ETF 심볼인지 여부.

    KRX 종목코드와 ETF 코드는 모두 6자리 숫자 문자열이다.
    """
    return len(symbol) == 6 and symbol.isdigit()


def _fmt_date(d: date) -> str:
    """pykrx 가 요구하는 YYYYMMDD 문자열로 포맷."""
    return d.strftime("%Y%m%d")


class PykrxSource(DataSource):
    """pykrx 기반 한국 시장 DataSource.

    Parameters
    ----------
    min_interval_seconds : float, optional
        pykrx 호출 간 최소 인터벌(초). 기본 0.1 초.
        architecture.md §9 에서 지정된 rate limit 정책(세션당 100ms sleep)과
        일치한다. 0 이상이어야 하며, 0 이면 sleep 을 적용하지 않는다.

    Notes
    -----
    - ``adj_close`` 는 pykrx 가 별도 제공하지 않아 ``close`` 로 채운다.
    - ``fetch_fx`` 는 지원하지 않는다 (:class:`NotImplementedError`).
    """

    def __init__(self, min_interval_seconds: float = 0.1):
        if min_interval_seconds < 0:
            raise ValueError("min_interval_seconds must be >= 0")
        self._min_interval_seconds = float(min_interval_seconds)
        self._last_call_ts: float | None = None

    # ------------------------------------------------------------------
    # 메타
    # ------------------------------------------------------------------

    @property
    def source_name(self) -> str:
        """데이터 소스 식별자."""
        return "pykrx"

    # ------------------------------------------------------------------
    # 내부 유틸
    # ------------------------------------------------------------------

    def _respect_rate_limit(self) -> None:
        """직전 호출로부터 ``min_interval_seconds`` 가 지날 때까지 대기."""
        if self._min_interval_seconds <= 0:
            return
        now = _time.monotonic()
        if self._last_call_ts is not None:
            elapsed = now - self._last_call_ts
            remaining = self._min_interval_seconds - elapsed
            if remaining > 0:
                _time.sleep(remaining)
        self._last_call_ts = _time.monotonic()

    def _normalize_ohlcv(self, df: pd.DataFrame) -> pd.DataFrame:
        """pykrx 응답을 표준 OHLCV 스키마로 변환한다."""
        if df is None or df.empty:
            return _empty_ohlcv()

        out = df.copy()
        # 인덱스(날짜)를 time 컬럼으로 승격.
        out = out.reset_index()
        # 첫 컬럼이 날짜 인덱스. pykrx 는 보통 '날짜' 또는 Timestamp 인덱스를 반환.
        index_col = out.columns[0]
        out = out.rename(columns={index_col: "time"})
        out["time"] = pd.to_datetime(out["time"])

        # 한글 컬럼 → 표준 컬럼 매핑.
        out = out.rename(columns=_OHLCV_COLUMN_MAP)

        # 필수 컬럼 존재 여부 확인. pykrx get_index_ohlcv 의 경우
        # 거래량 컬럼이 없을 수 있다 — 그 때는 0 으로 채운다.
        for col in ("open", "high", "low", "close"):
            if col not in out.columns:
                # 스키마 불일치는 소스 오류로 간주.
                raise DataSourceError(
                    f"pykrx response missing required column: {col!r} "
                    f"(got columns={list(out.columns)})"
                )
        if "volume" not in out.columns:
            out["volume"] = 0.0

        # adj_close 는 close 로 채움.
        out["adj_close"] = out["close"]

        # 숫자형 캐스팅 + 필수 컬럼만 추출 + 정렬.
        for col in ("open", "high", "low", "close", "adj_close", "volume"):
            out[col] = pd.to_numeric(out[col], errors="coerce")

        out = out[_OHLCV_COLUMNS].sort_values("time").reset_index(drop=True)
        return out

    # ------------------------------------------------------------------
    # OHLCV
    # ------------------------------------------------------------------

    def fetch_ohlcv(
        self,
        symbol: str,
        market: str,
        start: date,
        end: date,
    ) -> pd.DataFrame:
        """pykrx 를 통해 KR 자산의 일봉 OHLCV 를 조회한다.

        Parameters
        ----------
        symbol : str
            6자리 숫자면 종목/ETF 코드로 간주하여
            ``pykrx.stock.get_market_ohlcv`` 를 사용한다.
            그 외(예: ``"KS11"``, ``"KQ11"``, ``"KRX100"``, ``"1001"``)는
            지수 코드로 간주하여 ``pykrx.stock.get_index_ohlcv`` 를 사용한다.
        market : str
            ``"KR"``, ``"KOSPI"``, ``"KOSDAQ"`` 를 허용. 그 외 값은
            :class:`DataSourceError` 로 거부한다.
        start, end : datetime.date
            조회 구간 (양 끝 포함).

        Returns
        -------
        pandas.DataFrame
            base.py 에 정의된 표준 OHLCV 스키마. ``adj_close`` 는 ``close``
            값으로 채워져 있다.

        Raises
        ------
        SymbolNotFoundError
            pykrx 가 해당 심볼에 대해 빈 응답을 반환한 경우.
        DataSourceError
            market 이 허용되지 않거나, pykrx 호출 자체가 실패한 경우.
        """
        allowed_markets = {"KR", "KOSPI", "KOSDAQ"}
        if market not in allowed_markets:
            raise DataSourceError(
                f"PykrxSource.fetch_ohlcv: unsupported market={market!r} "
                f"(allowed: {sorted(allowed_markets)})"
            )

        # KR 주요 지수는 pykrx 상류 버그(KeyError: '지수명')로 조회 불가.
        # yfinance 로 폴백 (모듈 상단 주석 참고).
        if symbol in _KR_INDEX_YF_FALLBACK:
            return self._fetch_kr_index_via_yfinance(
                symbol=symbol, start=start, end=end
            )

        # pykrx 는 지연 임포트 — 미설치 환경에서 모듈 로드만은 가능하도록.
        try:
            from pykrx import stock as _pykrx_stock
        except ImportError as exc:  # pragma: no cover
            raise DataSourceError(
                "pykrx is not installed; install 'pykrx' to use PykrxSource"
            ) from exc

        s = _fmt_date(start)
        e = _fmt_date(end)

        self._respect_rate_limit()
        try:
            if _is_stock_symbol(symbol):
                raw = _pykrx_stock.get_market_ohlcv(s, e, symbol)
            else:
                raw = _pykrx_stock.get_index_ohlcv(s, e, symbol)
        except Exception as exc:
            raise DataSourceError(
                f"pykrx fetch_ohlcv failed for symbol={symbol!r} "
                f"market={market!r}: {exc}"
            ) from exc

        if raw is None or raw.empty:
            raise SymbolNotFoundError(
                f"pykrx returned no data for symbol={symbol!r} market={market!r} "
                f"[{s}..{e}]"
            )

        return self._normalize_ohlcv(raw)

    # ------------------------------------------------------------------
    # KR 지수 yfinance 폴백
    # ------------------------------------------------------------------

    def _fetch_kr_index_via_yfinance(
        self,
        symbol: str,
        start: date,
        end: date,
    ) -> pd.DataFrame:
        """KR 주요 지수를 yfinance 로 대체 조회한다.

        pykrx 상류 버그로 ``get_index_ohlcv`` 가 동작하지 않는 동안의 임시
        폴백. ``YFinanceSource`` 는 ``market in {US, CRYPTO, COMMODITY, FX}``
        만 허용하므로 여기서는 yfinance 를 재사용하되 KR 심볼을 ``^KS11`` 등
        yfinance 인덱스 심볼로 변환해 직접 호출한다. yfinance 의 호출/정규화
        로직은 :class:`YFinanceSource` 의 private 메서드를 재사용한다.
        """
        yf_symbol = _KR_INDEX_YF_FALLBACK[symbol]

        # 지연 import: 순환/무거운 import 를 피한다.
        from .yfinance_source import YFinanceSource  # noqa: WPS433

        # lazy-init 싱글톤: 인스턴스 내부에 캐시.
        yf_source = getattr(self, "_yf_fallback", None)
        if yf_source is None:
            yf_source = YFinanceSource()
            self._yf_fallback = yf_source

        self._respect_rate_limit()
        # yfinance end 는 exclusive 이므로 +1 일.
        df = yf_source._yf_download(
            symbol=yf_symbol, start=start, end=end + timedelta(days=1)
        )
        if df is None or df.empty:
            raise SymbolNotFoundError(
                f"yfinance fallback returned no data for KR index "
                f"symbol={symbol!r} -> {yf_symbol!r} [{start}..{end}]"
            )
        return yf_source._normalize_ohlcv(df)

    # ------------------------------------------------------------------
    # FX (미지원)
    # ------------------------------------------------------------------

    def fetch_fx(
        self,
        base_ccy: str,
        quote_ccy: str,
        start: date,
        end: date,
    ) -> pd.DataFrame:
        """지원하지 않음. FX 는 YFinanceSource 를 사용한다."""
        raise NotImplementedError("pykrx does not provide FX; use YFinanceSource")

    # ------------------------------------------------------------------
    # 심볼 목록
    # ------------------------------------------------------------------

    def list_symbols(self, market: str) -> List[str]:
        """KR 시장의 심볼 목록(KOSPI + KOSDAQ)을 반환한다.

        Parameters
        ----------
        market : str
            ``"KR"`` 이면 전체 KOSPI+KOSDAQ 티커를 반환한다.
            그 외 값은 빈 리스트를 반환한다.

        Returns
        -------
        list[str]
            6자리 종목 코드 문자열 리스트. 중복은 제거된다.
        """
        if market != "KR":
            return []

        try:
            from pykrx import stock as _pykrx_stock
        except ImportError as exc:  # pragma: no cover
            raise DataSourceError(
                "pykrx is not installed; install 'pykrx' to use PykrxSource"
            ) from exc

        self._respect_rate_limit()
        try:
            # 기본: 오늘 기준 전체 시장 티커. pykrx 는 market 파라미터를
            # 지원하므로 KOSPI + KOSDAQ 를 각각 조회 후 합친다.
            kospi = _pykrx_stock.get_market_ticker_list(market="KOSPI")
            self._respect_rate_limit()
            kosdaq = _pykrx_stock.get_market_ticker_list(market="KOSDAQ")
        except TypeError:
            # 구 버전 pykrx 는 market 키워드를 지원하지 않을 수 있다 —
            # 기본(KOSPI) 만 반환.
            kospi = _pykrx_stock.get_market_ticker_list()
            kosdaq = []
        except Exception as exc:
            raise DataSourceError(f"pykrx list_symbols failed: {exc}") from exc

        seen: set[str] = set()
        result: list[str] = []
        for sym in list(kospi) + list(kosdaq):
            if sym not in seen:
                seen.add(sym)
                result.append(sym)
        return result


__all__ = ["PykrxSource"]
