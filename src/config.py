"""
프로젝트 설정 모듈.
티커 목록, ClickHouse 연결 설정, 로깅 설정을 관리한다.
"""

import os
import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path


# =============================================================================
# 프로젝트 경로
# =============================================================================
PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOGS_DIR = PROJECT_ROOT / "logs"
LOGS_DIR.mkdir(exist_ok=True)


# =============================================================================
# 추적 자산 설정 (Phase 1)
# =============================================================================
TICKERS = {
    "^GSPC": {
        "name": "S&P 500",
        "description": "미국 대형주 지수",
        "data_start": "1927-01-01",
    },
    "GC=F": {
        "name": "Gold Futures",
        "description": "금 선물",
        "data_start": "2000-01-01",
    },
    "TLT": {
        "name": "US 20Y+ Treasury Bond ETF",
        "description": "미국 중장기 국채 ETF",
        "data_start": "2002-01-01",
    },
}

TICKER_SYMBOLS = list(TICKERS.keys())


# =============================================================================
# ClickHouse 연결 설정
# =============================================================================
CLICKHOUSE_CONFIG = {
    "host": os.getenv("CLICKHOUSE_HOST", "localhost"),
    "port": int(os.getenv("CLICKHOUSE_PORT", "8123")),
    "username": os.getenv("CLICKHOUSE_USER", "default"),
    "password": os.getenv("CLICKHOUSE_PASSWORD", ""),
    "database": os.getenv("CLICKHOUSE_DATABASE", "asset_tracker"),
}


# =============================================================================
# 로깅 설정
# =============================================================================
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def setup_logger(name: str, log_file: str | None = None) -> logging.Logger:
    """
    로거를 설정하고 반환한다.
    - 콘솔 핸들러: 항상 추가
    - 파일 핸들러: log_file이 지정되면 일별 로테이션으로 추가

    Args:
        name: 로거 이름 (예: "collector", "analyzer")
        log_file: 로그 파일명 (예: "collector.log"). None이면 콘솔만.

    Returns:
        설정된 logging.Logger 인스턴스
    """
    logger = logging.getLogger(name)

    # 이미 핸들러가 설정된 경우 중복 추가 방지
    if logger.handlers:
        return logger

    logger.setLevel(getattr(logging, LOG_LEVEL, logging.INFO))

    formatter = logging.Formatter(LOG_FORMAT, datefmt=LOG_DATE_FORMAT)

    # 콘솔 핸들러
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # 파일 핸들러 (일별 로테이션)
    if log_file:
        file_path = LOGS_DIR / log_file
        file_handler = TimedRotatingFileHandler(
            filename=str(file_path),
            when="midnight",
            interval=1,
            backupCount=30,
            encoding="utf-8",
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
