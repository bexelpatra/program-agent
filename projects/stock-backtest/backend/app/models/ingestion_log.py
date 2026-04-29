"""IngestionLog — 일별 수집 멱등 UPSERT 정책의 감사 로그.

status 는 String + 애플리케이션 검증(Pydantic) 으로 처리해 Postgres ENUM 마이그레이션 부담 회피.
"""
from datetime import date, datetime

from sqlalchemy import Date, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class IngestionLog(Base):
    """단일 ingestion 시도 결과 한 건.

    실패/부분 성공 분석 + 재시도 의사결정을 위해 attempt 단위로 기록.
    TimestampedModel mixin 미사용 — updated_at 의미 없음(시도 자체는 불변), attempted_at 만 보유.
    """

    __tablename__ = "ingestion_log"

    log_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    asset_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("assets.asset_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    requested_start: Mapped[date] = mapped_column(Date, nullable=False)
    requested_end: Mapped[date] = mapped_column(Date, nullable=False)
    # OK / FAILED / REJECTED / PARTIAL — Pydantic Literal 로 호출 경계에서 검증.
    status: Mapped[str] = mapped_column(String(16), nullable=False)
    rows_inserted: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
    # 실패 사유 / API 응답 본문 — 길이 제한 없는 TEXT 로 저장.
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    attempted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
