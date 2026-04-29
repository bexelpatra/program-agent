"""모델 공용 mixin.

도메인 로직 금지. SQLAlchemy 컬럼 정의/혼합 헬퍼만.
"""
from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column


class TimestampedModel:
    """created_at / updated_at 을 server_default + onupdate 로 자동 관리.

    여러 테이블이 동일 컬럼 패턴을 반복하지 않도록 mixin 으로 추출.
    timezone=True 로 UTC 저장 강제 (Asia/Seoul 변환은 표시 계층 책임).
    """

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
