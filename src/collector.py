"""
데이터 수집 모듈.
yfinance를 사용하여 자산 가격 데이터를 수집하고 ClickHouse에 저장한다.
백필(전체 히스토리)과 증분(마지막 날짜 이후) 모드를 자동 판단한다.
"""

from datetime import datetime, timedelta

import pandas as pd
import yfinance as yf

from src.config import TICKERS, TICKER_SYMBOLS, setup_logger
from src.database import Database

logger = setup_logger("collector", "collector.log")


def _normalize_dataframe(df: pd.DataFrame, symbol: str) -> pd.DataFrame:
    """
    yfinance에서 반환된 DataFrame을 DB 스키마에 맞게 정규화한다.

    Args:
        df: yfinance가 반환한 OHLCV DataFrame
        symbol: 티커 심볼

    Returns:
        정규화된 DataFrame (symbol, date, open, high, low, close, adj_close, volume)
    """
    if df.empty:
        return pd.DataFrame(
            columns=[
                "symbol",
                "date",
                "open",
                "high",
                "low",
                "close",
                "adj_close",
                "volume",
            ]
        )

    result = df.copy()

    # yfinance가 MultiIndex 컬럼을 반환하는 경우 처리 (단일 티커에서도 발생 가능)
    if isinstance(result.columns, pd.MultiIndex):
        # ('Price', 'Close', 'AAPL') 같은 형태 -> 첫 번째 레벨만 사용
        result.columns = result.columns.get_level_values(0)

    # 컬럼명 소문자 변환 및 매핑
    result.columns = [c.lower().replace(" ", "_") for c in result.columns]

    # 필수 가격 컬럼 존재 확인
    if "close" not in result.columns:
        logger.error("정규화 실패 - 'close' 컬럼 없음 (사용 가능: %s)", list(result.columns))
        return pd.DataFrame(
            columns=[
                "symbol",
                "date",
                "open",
                "high",
                "low",
                "close",
                "adj_close",
                "volume",
            ]
        )

    # adj_close 컬럼 처리: yfinance 버전에 따라 'adj close' 또는 'adj_close' 또는 없을 수 있음
    if "adj_close" not in result.columns:
        if "adjusted_close" in result.columns:
            result = result.rename(columns={"adjusted_close": "adj_close"})
        else:
            # adj_close가 없으면 close를 사용
            result["adj_close"] = result["close"]

    # 인덱스(날짜)를 컬럼으로 변환
    result = result.reset_index()

    # 날짜 컬럼 이름 통일
    date_col = None
    for col in ["Date", "date", "Datetime", "datetime"]:
        if col in result.columns:
            date_col = col
            break
    if date_col and date_col != "date":
        result = result.rename(columns={date_col: "date"})

    # symbol 컬럼 추가
    result["symbol"] = symbol

    # 날짜를 date 타입으로 변환 (시간 정보 제거)
    result["date"] = pd.to_datetime(result["date"]).dt.date

    # 필요한 컬럼만 선택
    required_cols = [
        "symbol",
        "date",
        "open",
        "high",
        "low",
        "close",
        "adj_close",
        "volume",
    ]
    missing = [c for c in required_cols if c not in result.columns]
    if missing:
        logger.error("정규화 실패 - 누락 컬럼: %s (사용 가능: %s)", missing, list(result.columns))
        return pd.DataFrame(columns=required_cols)

    result = result[required_cols].copy()

    # NaN 행 제거 (가격 데이터가 없는 행)
    result = result.dropna(subset=["close"])

    return result


def collect_symbol(db: Database, symbol: str) -> int:
    """
    단일 심볼의 가격 데이터를 수집하여 DB에 저장한다.
    DB에 데이터가 없으면 백필, 있으면 증분 수집한다.

    Args:
        db: Database 인스턴스
        symbol: 티커 심볼

    Returns:
        수집된 행 수
    """
    ticker_info = TICKERS.get(symbol, {})
    ticker_name = ticker_info.get("name", symbol)

    # DB에서 마지막 날짜 확인 -> 백필/증분 자동 판단
    last_date = db.get_last_date(symbol)

    if last_date is None:
        # 백필 모드: 전체 히스토리 수집
        logger.info("[백필] %s (%s) — 전체 히스토리 수집 시작", symbol, ticker_name)
        df = yf.download(symbol, period="max", progress=False)
    else:
        # 증분 모드: 마지막 날짜 다음 날부터 오늘까지
        start_date = (
            datetime.strptime(last_date, "%Y-%m-%d") + timedelta(days=1)
        ).strftime("%Y-%m-%d")
        end_date = datetime.now().strftime("%Y-%m-%d")

        if start_date > end_date:
            logger.info(
                "[증분] %s (%s) — 이미 최신 (마지막: %s)", symbol, ticker_name, last_date
            )
            return 0

        logger.info(
            "[증분] %s (%s) — %s ~ %s 수집 시작",
            symbol,
            ticker_name,
            start_date,
            end_date,
        )
        df = yf.download(symbol, start=start_date, end=end_date, progress=False)

    # 정규화
    normalized = _normalize_dataframe(df, symbol)

    if normalized.empty:
        logger.warning("%s — 수집된 데이터 없음", symbol)
        return 0

    # DB에 저장
    db.insert_prices(normalized)
    row_count = len(normalized)
    logger.info("%s — %d건 저장 완료", symbol, row_count)

    return row_count


def collect_all(db: Database | None = None) -> dict[str, int]:
    """
    config.py의 모든 티커에 대해 데이터를 수집한다.
    개별 티커 실패 시 건너뛰고 다음 티커를 계속 진행한다.

    Args:
        db: Database 인스턴스. None이면 새로 생성한다.

    Returns:
        {symbol: 수집 건수} 딕셔너리
    """
    own_db = db is None
    if own_db:
        db = Database()
        db.init_schema()

    results: dict[str, int] = {}
    failed: list[str] = []

    logger.info("=== 데이터 수집 시작 (총 %d개 티커) ===", len(TICKER_SYMBOLS))

    for symbol in TICKER_SYMBOLS:
        try:
            count = collect_symbol(db, symbol)
            results[symbol] = count
        except Exception:
            logger.exception("수집 실패: %s — 건너뛰고 계속 진행", symbol)
            results[symbol] = -1
            failed.append(symbol)

    # 요약 로깅
    total = sum(v for v in results.values() if v > 0)
    logger.info("=== 데이터 수집 완료 ===")
    logger.info("총 수집: %d건", total)
    for sym, count in results.items():
        status = f"{count}건" if count >= 0 else "실패"
        logger.info("  %s: %s", sym, status)

    if failed:
        logger.warning("실패한 티커: %s", failed)

    if own_db:
        db.close()

    return results


if __name__ == "__main__":
    collect_all()
