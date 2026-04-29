"""ORM 모델 패키지.

alembic env.py 가 `import app.models` 만 하면 모든 모델이 Base.metadata 에 등록되도록
여기서 명시적 re-export 한다. 신규 모델 추가 시 반드시 본 파일에도 등록.
"""
from app.models.asset import Asset
from app.models.backtest import BacktestEquity, BacktestMetric, BacktestRun, BacktestTrade
from app.models.corporate_actions import CorporateAction
from app.models.fx_rates import FxRate
from app.models.ingestion_log import IngestionLog
from app.models.ohlcv import Ohlcv

__all__ = [
    "Asset",
    "BacktestEquity",
    "BacktestMetric",
    "BacktestRun",
    "BacktestTrade",
    "CorporateAction",
    "FxRate",
    "IngestionLog",
    "Ohlcv",
]
