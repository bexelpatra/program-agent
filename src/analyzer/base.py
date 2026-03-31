"""
분석 전략 기본 클래스 및 시그널 정의.
모든 분석/매매 전략은 BaseStrategy를 상속받아 구현한다.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum

import pandas as pd


class SignalType(Enum):
    """매매 시그널 유형."""

    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"


@dataclass
class Signal:
    """
    매매 시그널.
    - date: 시그널 발생일 (YYYY-MM-DD 문자열)
    - signal_type: BUY / SELL / HOLD
    - weight: 0.0~1.0, 자본 대비 포지션 비율
    """

    date: str
    signal_type: SignalType
    weight: float = 1.0


class BaseStrategy(ABC):
    """모든 분석/매매 전략의 기본 클래스."""

    @property
    @abstractmethod
    def name(self) -> str:
        """전략 이름."""

    @property
    def description(self) -> str:
        """전략 설명 (선택)."""
        return ""

    @abstractmethod
    def analyze(self, df: pd.DataFrame, **params) -> dict:
        """
        분석 실행.

        Args:
            df: OHLCV DataFrame (symbol, date, open, high, low, close, adj_close, volume)
            **params: 전략별 파라미터 (이동평균 기간, 윈도우 크기 등)

        Returns:
            {"summary": str, "metrics": dict, "details": DataFrame}
        """

    def generate_signals(self, df: pd.DataFrame, **params) -> list[Signal]:
        """
        매매 시그널 생성 (백테스팅용).
        기본 구현은 빈 시그널. 매매 전략만 오버라이드.
        weight로 포지션 크기 조절 가능 (향후 포트폴리오 전략 대비).
        """
        return []
