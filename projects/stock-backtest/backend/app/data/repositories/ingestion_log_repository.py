"""IngestionLogRepository — append-only ingestion 감사 로그.

태스크 단위로 1회 record() 호출. update/delete 는 정의하지 않는다 (불변 정책).
"""
from __future__ import annotations

from datetime import date, datetime, timezone

from sqlalchemy.orm import Session

from app.models.ingestion_log import IngestionLog


class IngestionLogRepository:
    """ingestion_log 테이블에 시도 1건을 기록한다."""

    def __init__(self, session: Session):
        self._session = session

    def record(
        self,
        asset_id: int,
        requested_start: date,
        requested_end: date,
        status: str,
        rows_inserted: int = 0,
        error_message: str | None = None,
    ) -> None:
        """단일 ingestion 시도 결과 적재.

        Args:
            asset_id: 대상 자산 PK.
            requested_start: 시도한 백필 구간 시작 (포함).
            requested_end: 시도한 백필 구간 종료 (포함).
            status: OK / FAILED / PARTIAL / REJECTED. 모델 주석에 정의된 4종.
            rows_inserted: 실제 UPSERT 시도 row 수 (멱등 정책 상 update 포함).
            error_message: 실패 시 raw 메시지. 길이 무제한 (TEXT).
        """
        log = IngestionLog(
            asset_id=asset_id,
            requested_start=requested_start,
            requested_end=requested_end,
            status=status,
            rows_inserted=rows_inserted,
            error_message=error_message,
            attempted_at=datetime.now(timezone.utc),
        )
        self._session.add(log)
        self._session.flush()
