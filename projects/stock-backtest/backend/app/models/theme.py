"""Theme / ThemeAsset / AssetThemeHistory ORM 모델.

architecture.md V3 § "V3 Phase 2 — 테마주 추적/관찰 모듈" L823~ 의 도메인 모델 매핑.

설계 노트:
- ``themes`` 는 사용자 큐레이션 테마 헤더. ``user_id`` 는 멀티 사용자 확장 prep
  (현재 로컬 단일 사용자 = 'local' 기본값). ``(user_id, slug)`` UNIQUE.
- ``theme_assets`` 는 테마와 자산의 N:M 매핑. ``removed_at`` soft-delete 컬럼 +
  ``(theme_id, asset_id, added_at)`` 복합 PK 로 동일 자산 재추가 이력 보존.
  활성 멤버 조회 가속을 위해 ``removed_at IS NULL`` 부분 인덱스 보유.
- ``asset_theme_history`` 는 자산 단위 ADDED/REMOVED/RECLASSIFIED 이벤트 append-only
  로그. ``from_theme_id`` 는 RECLASSIFIED 시 출처 테마 기록.
- TimestampedModel mixin 미적용: append-only/시계열 성격이라 ``updated_at`` 의미
  없음. ``themes`` 만 ``created_at`` 보유 (사용자 가시 메타데이터).
"""
from datetime import datetime
from typing import Any

from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class Theme(Base):
    """단일 테마 헤더 (예: '한국 정치 관련주', '2차전지 핵심')."""

    __tablename__ = "themes"
    __table_args__ = (
        UniqueConstraint("user_id", "slug", name="uq_themes_user_slug"),
    )

    theme_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    # 사용자 가시 이름 (한국어 우선).
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    # URL/식별자용 slug. (user_id, slug) UNIQUE.
    slug: Mapped[str] = mapped_column(String(120), nullable=False)
    # 설명/메모 — 길이 제한 없는 TEXT.
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    # 멀티 사용자 prep. 현재 로컬 단일 사용자 'local' default.
    user_id: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        server_default="local",
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )


class ThemeAsset(Base):
    """테마-자산 매핑 (N:M).

    동일 자산의 재추가 이력을 보존하기 위해 ``added_at`` 도 PK 에 포함한다.
    ``removed_at`` 이 NULL 인 행만 활성 멤버. 활성 필터링은 부분 인덱스
    ``ix_theme_assets_active`` 가 가속.
    """

    __tablename__ = "theme_assets"

    theme_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("themes.theme_id", ondelete="CASCADE"),
        primary_key=True,
    )
    asset_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("assets.asset_id", ondelete="RESTRICT"),
        primary_key=True,
    )
    added_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        primary_key=True,
        server_default=func.now(),
    )
    removed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    note: Mapped[str | None] = mapped_column(Text, nullable=True)


class AssetThemeHistory(Base):
    """자산 단위 ADDED/REMOVED/RECLASSIFIED 이벤트 append-only 로그.

    Service 레이어가 add/remove 트랜잭션 안에서 ThemeAsset 변경과 동시에
    1 행 INSERT 한다. ``event_type`` CHECK 제약으로 알 수 없는 값 차단.
    ``from_theme_id`` 는 RECLASSIFIED 시 출처 테마, 그 외 NULL.
    """

    __tablename__ = "asset_theme_history"
    __table_args__ = (
        CheckConstraint(
            "event_type IN ('ADDED','REMOVED','RECLASSIFIED')",
            name="ck_asset_theme_history_event_type",
        ),
    )

    history_id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )
    asset_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("assets.asset_id", ondelete="CASCADE"),
        nullable=False,
    )
    theme_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("themes.theme_id", ondelete="CASCADE"),
        nullable=False,
    )
    event_type: Mapped[str] = mapped_column(String(20), nullable=False)
    from_theme_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("themes.theme_id", ondelete="SET NULL"),
        nullable=True,
    )
    occurred_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    # USER / SYSTEM / IMPORT 등. Pydantic Literal 로 호출 경계에서 검증.
    source: Mapped[str] = mapped_column(
        String(16),
        nullable=False,
        server_default="USER",
    )
    note: Mapped[str | None] = mapped_column(Text, nullable=True)
