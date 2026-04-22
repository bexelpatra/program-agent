"""DataSource 추상 인터페이스.

이 모듈은 외부 시계열 데이터 제공자(yfinance, pykrx 등)를 교체 가능한 형태로
캡슐화하기 위한 추상 베이스 클래스와 공통 예외를 정의한다.

architecture.md §'리스크 / 향후 재검토' 참고:
    - yfinance/pykrx 비공식성 → DataSource 추상화로 교체 가능하게 설계
"""

from __future__ import annotations

import abc
from datetime import date
from typing import List

import pandas as pd


class DataSourceError(Exception):
    """DataSource 레이어에서 발생하는 모든 예외의 베이스 클래스."""


class SymbolNotFoundError(DataSourceError):
    """요청된 심볼을 해당 데이터 소스에서 찾을 수 없을 때 발생."""


class RateLimitError(DataSourceError):
    """데이터 소스의 rate limit 에 걸려 일시적으로 요청이 거부되었을 때 발생.

    호출자는 지수 백오프 후 재시도하는 것이 권장된다.
    """


class DataSource(abc.ABC):
    """외부 시계열 데이터 제공자에 대한 추상 인터페이스.

    구현체는 OHLCV 일봉, FX 환율, 심볼 목록을 제공해야 한다.
    반환되는 ``pandas.DataFrame`` 의 스키마는 각 메서드의 docstring 에
    명시된 컬럼 규약을 반드시 따른다.
    """

    @property
    @abc.abstractmethod
    def source_name(self) -> str:
        """데이터 소스의 고유 식별자.

        예: ``"yfinance"``, ``"pykrx"``.
        ``ingestion_log`` 등에 기록되므로 소스간 충돌하지 않아야 한다.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def fetch_ohlcv(
        self,
        symbol: str,
        market: str,
        start: date,
        end: date,
    ) -> pd.DataFrame:
        """지정된 심볼의 일봉 OHLCV 데이터를 반환한다.

        Parameters
        ----------
        symbol : str
            자산 심볼 (예: ``"SPY"``, ``"005930"``).
        market : str
            시장 식별자 (예: ``"US"``, ``"KR"``, ``"CRYPTO"``).
        start : datetime.date
            조회 시작일 (포함).
        end : datetime.date
            조회 종료일 (포함).

        Returns
        -------
        pandas.DataFrame
            다음 컬럼을 가지는 DataFrame. ``time`` 기준 오름차순 정렬.

            - ``time`` (datetime64[ns] 또는 timezone-aware, 일봉 기준)
            - ``open`` (float)
            - ``high`` (float)
            - ``low`` (float)
            - ``close`` (float)
            - ``adj_close`` (float) - 분할/배당 반영 조정 종가
            - ``volume`` (float | int)

            비거래일/결측 로우는 포함하지 않는다. 데이터가 없으면 위 스키마를
            가진 빈 DataFrame 을 반환한다.

        Raises
        ------
        SymbolNotFoundError
            소스가 해당 (symbol, market) 을 인식하지 못하는 경우.
        RateLimitError
            소스의 rate limit 로 인해 호출이 거부된 경우.
        DataSourceError
            그 외 데이터 소스 오류.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def fetch_fx(
        self,
        base_ccy: str,
        quote_ccy: str,
        start: date,
        end: date,
    ) -> pd.DataFrame:
        """환율 시계열을 반환한다.

        ``rate`` 의 의미는 "1 ``base_ccy`` = rate ``quote_ccy``" 로 통일한다.
        예: ``base_ccy='USD', quote_ccy='KRW'`` → 1 USD 당 KRW 가격.

        Parameters
        ----------
        base_ccy : str
            기준 통화 ISO 코드 (예: ``"USD"``).
        quote_ccy : str
            상대 통화 ISO 코드 (예: ``"KRW"``).
        start : datetime.date
            조회 시작일 (포함).
        end : datetime.date
            조회 종료일 (포함).

        Returns
        -------
        pandas.DataFrame
            다음 컬럼을 가지는 DataFrame. ``time`` 기준 오름차순 정렬.

            - ``time`` (datetime64[ns] 또는 timezone-aware, 일 단위)
            - ``rate`` (float) - "1 base_ccy = rate quote_ccy"

            데이터가 없으면 위 스키마를 가진 빈 DataFrame 을 반환한다.

        Raises
        ------
        SymbolNotFoundError
            소스가 해당 통화 페어를 제공하지 않는 경우.
        RateLimitError
            소스의 rate limit 로 인해 호출이 거부된 경우.
        DataSourceError
            그 외 데이터 소스 오류.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def list_symbols(self, market: str) -> List[str]:
        """해당 소스가 주어진 시장에서 제공하는 심볼 목록을 반환한다.

        Parameters
        ----------
        market : str
            시장 식별자 (예: ``"US"``, ``"KR"``, ``"CRYPTO"``).

        Returns
        -------
        list[str]
            심볼 문자열의 리스트. 지원하지 않는 시장이면 빈 리스트를 반환한다.

        Raises
        ------
        DataSourceError
            목록 조회 과정에서 데이터 소스 오류가 발생한 경우.
        """
        raise NotImplementedError


__all__ = [
    "DataSource",
    "DataSourceError",
    "SymbolNotFoundError",
    "RateLimitError",
]
