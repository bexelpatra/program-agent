"""Data sources — 외부 시장 데이터 어댑터.

architecture.md V3 § "fx 데이터 어댑터": DataSource/FxSource 추상에 어댑터를
바인딩한다. 신규 어댑터(pykrx, pyupbit 등)는 base.py 의 Protocol 을 구현하고
본 파일에 re-export 한다.
"""
from app.data.sources.base import (
    DataSource,
    DividendEvent,
    FxBar,
    FxSource,
    OhlcvBar,
    TickerValidation,
)
from app.data.sources.pykrx_source import PykrxSource
from app.data.sources.yfinance_source import YfinanceFxSource, YfinanceSource

__all__ = [
    "DataSource",
    "FxSource",
    "OhlcvBar",
    "FxBar",
    "DividendEvent",
    "TickerValidation",
    "YfinanceSource",
    "YfinanceFxSource",
    "PykrxSource",
]
