"""
Collector 엔트리포인트 (cron용).
Database 스키마를 초기화하고 모든 티커의 가격 데이터를 수집한다.

실행:
    python -m src.run_collector
"""

import sys
from datetime import datetime

from src.config import setup_logger
from src.database import Database
from src.collector import collect_all

logger = setup_logger("run_collector", "collector.log")


def main():
    """Collector 메인 함수. cron에서 호출된다."""
    start_time = datetime.now()
    logger.info("=== Collector 시작: %s ===", start_time.strftime("%Y-%m-%d %H:%M:%S"))

    try:
        # Database 인스턴스 생성 및 스키마 초기화
        db = Database()
        db.init_schema()

        # 전체 티커 수집
        results = collect_all(db=db)

        # 결과 요약
        total_collected = sum(v for v in results.values() if v > 0)
        failed_count = sum(1 for v in results.values() if v < 0)
        skipped_count = sum(1 for v in results.values() if v == 0)
        success_count = sum(1 for v in results.values() if v > 0)

        end_time = datetime.now()
        elapsed = end_time - start_time

        logger.info("=== Collector 완료: %s ===", end_time.strftime("%Y-%m-%d %H:%M:%S"))
        logger.info("소요 시간: %s", str(elapsed))
        logger.info(
            "결과 요약: 총 %d건 수집 | 성공 %d개 | 스킵 %d개 | 실패 %d개",
            total_collected,
            success_count,
            skipped_count,
            failed_count,
        )

        db.close()

        # 실패가 있으면 exit code 1
        if failed_count > 0:
            sys.exit(1)

    except Exception:
        logger.exception("Collector 실행 중 치명적 오류 발생")
        sys.exit(2)


if __name__ == "__main__":
    main()
