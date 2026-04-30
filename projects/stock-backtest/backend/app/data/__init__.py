"""Data 레이어 — domain Repository Protocol 의 SQLAlchemy 구현체 + 외부 데이터 소스 어댑터.

신규 Repository 추가 시 본 파일에 re-export 등록.
신규 데이터 소스 어댑터는 app.data.sources 에 추가하고 본 파일에 re-export.
"""
from app.data.asset_repository import SqlAssetRepository
from app.data.pipeline import (
    IngestionResult,
    backfill_active_assets,
    backfill_asset,
)
from app.data.repositories import IngestionLogRepository, OhlcvRepository
from app.data.sources import (
    DataSource,
    DividendEvent,
    FxBar,
    FxSource,
    OhlcvBar,
    PykrxSource,
    TickerValidation,
    YfinanceFxSource,
    YfinanceSource,
    get_source_for_market,
)

__all__ = [
    "SqlAssetRepository",
    # repositories
    "OhlcvRepository",
    "IngestionLogRepository",
    # pipeline
    "IngestionResult",
    "backfill_asset",
    "backfill_active_assets",
    # data sources
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
