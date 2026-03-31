"""
main.py - 메인 실행 스크립트

네이버증권에서 환율과 세계 지수를 비동기로 동시 크롤링하여 SQLite DB에 저장한다.
"""

import asyncio
import logging
import sys
import os
import time
from datetime import datetime, timezone, timedelta

# src/ 디렉토리를 sys.path에 추가하여 import가 정상 작동하도록 한다
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import init_db, save_exchange_rates, save_market_indices
from scraper import fetch_exchange_rates, fetch_market_indices

# 로깅 설정: INFO 레벨, 콘솔 출력
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
)
logger = logging.getLogger(__name__)

# 한국 표준시 (UTC+9)
KST = timezone(timedelta(hours=9))


async def main() -> None:
    """메인 실행 함수.

    1. DB 초기화
    2. 환율 + 세계지수를 asyncio.gather로 동시 크롤링
    3. collected_at(현재 시각 ISO 8601) 추가
    4. DB에 저장
    5. 결과 요약 로깅
    """
    start_time = time.time()
    logger.info("크롤링 시작")

    # 1. DB 초기화
    await init_db()
    logger.info("DB 초기화 완료")

    # 2. 환율과 세계지수를 동시에 크롤링
    exchange_rates, market_indices = await asyncio.gather(
        fetch_exchange_rates(),
        fetch_market_indices(),
    )

    # 3. collected_at 추가 (현재 시각, ISO 8601, KST)
    collected_at = datetime.now(KST).isoformat()

    for rate in exchange_rates:
        rate["collected_at"] = collected_at

    for index in market_indices:
        index["collected_at"] = collected_at

    # 4. DB에 저장
    if exchange_rates:
        await save_exchange_rates(exchange_rates)
        logger.info("환율 데이터 저장 완료: %d건", len(exchange_rates))
    else:
        logger.warning("저장할 환율 데이터가 없습니다")

    if market_indices:
        await save_market_indices(market_indices)
        logger.info("세계지수 데이터 저장 완료: %d건", len(market_indices))
    else:
        logger.warning("저장할 세계지수 데이터가 없습니다")

    # 5. 결과 요약 로깅
    elapsed = time.time() - start_time
    logger.info(
        "크롤링 완료 - 환율: %d건, 세계지수: %d건, 소요 시간: %.2f초",
        len(exchange_rates),
        len(market_indices),
        elapsed,
    )


if __name__ == "__main__":
    asyncio.run(main())
