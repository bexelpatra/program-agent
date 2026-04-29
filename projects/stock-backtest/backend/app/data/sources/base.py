"""DataSource / FxSource 추상 인터페이스.

architecture.md V3 § "fx 데이터 어댑터" L596-600 + V1 결정 9 근거.
어댑터(yfinance, pykrx, pyupbit, 한국은행 등)가 동일 Protocol 을 구현하므로
교체 가능한 데이터 소스를 도메인이 의존성 역전으로 사용할 수 있다.

수집 레이어 방어 정책 (architecture.md V3 § 비거래일 방어):
- close=0 / null / NaN 인 일봉 행은 어댑터에서 거부한다 (Protocol 계약).
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from typing import Protocol


@dataclass(frozen=True)
class OhlcvBar:
    """소스 어댑터가 반환하는 일봉 1행. asset_id 매핑은 호출자(repository) 책임."""

    time: datetime  # timezone-aware (UTC 또는 시장 timezone, 호출자가 정규화)
    open: float | None
    high: float | None
    low: float | None
    close: float  # NOT NULL — 어댑터가 0/null/NaN 행을 미리 거른다
    adj_close: float | None
    volume: float | None


@dataclass(frozen=True)
class FxBar:
    """일봉 환율 1행. base_ccy → quote_ccy 1 단위당 rate."""

    time: datetime
    base_ccy: str
    quote_ccy: str
    rate: float


@dataclass(frozen=True)
class DividendEvent:
    """배당 이벤트. amount 는 native currency 기준."""

    time: datetime
    amount: float


@dataclass(frozen=True)
class TickerValidation:
    """자산 자유 추가 (TASK-031) 의 즉시 검증 결과 (3초 이내 목표).

    note 는 한국어 가능 (UI/UX 원칙 2 — 사용자 직접 노출).
    """

    ticker: str
    exists: bool
    has_min_history: bool  # 최소 1년치 데이터 보유 여부
    earliest: date | None
    latest: date | None
    note: str | None  # 실패 사유 또는 부가 안내


class DataSource(Protocol):
    """일봉 OHLCV / 배당 데이터 소스 인터페이스.

    구현체(YfinanceSource, PykrxSource 등)는 동일 Protocol 을 구현해야 하며,
    domain 레이어는 이 Protocol 만 의존한다.
    """

    def fetch_ohlcv(self, symbol: str, start: date, end: date) -> list[OhlcvBar]:
        """[start, end] 구간 일봉. close=0/null/NaN 행은 어댑터가 제거한다."""
        ...

    def fetch_dividends(self, symbol: str, start: date, end: date) -> list[DividendEvent]:
        """[start, end] 구간 배당 이벤트."""
        ...

    def validate_ticker(self, symbol: str) -> TickerValidation:
        """3초 이내 ticker 존재 + 최소 1년치 데이터 유무 검증."""
        ...


class FxSource(Protocol):
    """환율 전용 인터페이스.

    DataSource 와 분리한다 — fx 는 ticker 가 아니라 통화 페어 기반.
    갭(주말/휴일) forward-fill 책임은 호출자에 있다.
    """

    def fetch_fx(
        self, base_ccy: str, quote_ccy: str, start: date, end: date
    ) -> list[FxBar]:
        """[start, end] 구간 일봉 환율."""
        ...

    def validate_pair(self, base_ccy: str, quote_ccy: str) -> bool:
        """환율 페어 지원 여부."""
        ...
