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


def get_source_for_market(
    market: str,
    *,
    yfinance: YfinanceSource,
    pykrx: PykrxSource,
) -> DataSource:
    """시장 코드 → DataSource 라우팅 단일 진입점.

    KR → pykrx, US/CRYPTO → yfinance. 신규 시장 추가는 본 함수만 수정하면
    `api/assets.py` (자산 등록 시 ticker validation 라우팅) 와
    `scheduler/cron_jobs.py` (시장별 cron 백필 라우팅) 양쪽이 동시에 반영된다.

    호출자는 source 인스턴스를 keyword 로 주입한다 (테스트 mock 주입 + DI 친화).
    인스턴스 lifecycle 정책 (싱글톤 vs per-call) 은 호출자가 결정한다.

    Raises:
        ValueError: 알 수 없는 market 코드.
    """
    if market == "KR":
        return pykrx
    if market in ("US", "CRYPTO"):
        return yfinance
    raise ValueError(f"unknown market: {market!r}")


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
    "get_source_for_market",
]
