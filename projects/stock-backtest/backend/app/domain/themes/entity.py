"""Theme / ThemeAsset / AssetThemeHistory 도메인 엔티티.

architecture.md V3 § "V3 Phase 2 — 테마주 추적/관찰 모듈" (L823~) § "도메인 모델"
(L847-875) 근거.

POPO (frozen dataclass + slots) — SQLAlchemy / FastAPI / 시장 데이터 어댑터 의존 금지.
data 레이어 (`app.data.theme_repository.SqlThemeRepository`) 가 ORM 모델 ↔ 본 엔티티
변환을 책임진다.

도메인 격리:
    `backend/app/domain/themes/` 는 `backend/app/domain/{engine, strategy,
    allocators, filters, trade, portfolio}` 와 양방향 import 금지
    (architecture.md L1065 ↔ TASK-309 정적 검증 대상).
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Literal

# ===== Literal 타입 (DB CHECK 제약과 동기) ===================================
# `asset_theme_history.event_type` CHECK ('ADDED','REMOVED','RECLASSIFIED')
# (`backend/app/models/theme.py:106` / alembic 0005 동기).
EventType = Literal["ADDED", "REMOVED", "RECLASSIFIED"]

# Phase 2.3 관심도 소스 — `asset_attention.source` 컬럼 값. 본 도메인에서 직접
# 사용하지는 않지만 도메인 레이어가 관심도 도메인 (Phase 2.3) 정의 전에 Literal
# 합의를 가지도록 선반영 (architecture.md L841 + L925 근거).
AttentionSource = Literal["naver_datalab", "google_trends"]

# `asset_theme_history.source` 컬럼 값 (USER vs AUTO 시스템 트리거).
HistorySource = Literal["USER", "AUTO"]


@dataclass(frozen=True, slots=True)
class Theme:
    """사용자 큐레이션 단일 테마 헤더.

    Attributes:
        theme_id: DB PK (신규 생성 시 0 — Repository 가 부여).
        name: 사용자 가시 이름 (한국어 우선). 예: "정치 — 이재명".
        slug: URL-safe 식별자. (user_id, slug) UNIQUE.
        description: 자유 설명/메모. None 가능.
        user_id: 멀티 사용자 prep — 현재 로컬 단일 사용자 'local' 기본값
            (architecture.md V1 L17).
        created_at: 생성 시각. 신규 생성 시 Repository 가 server_default 로 채움.
    """

    theme_id: int
    name: str
    slug: str
    description: str | None
    user_id: str
    created_at: datetime


@dataclass(frozen=True, slots=True)
class ThemeAsset:
    """테마와 자산의 멤버십 매핑 (N:M).

    동일 자산이 같은 테마에 재추가될 수 있도록 ``added_at`` 도 키에 포함된다
    (ORM PK = (theme_id, asset_id, added_at) — `backend/app/models/theme.py` 동기).

    Attributes:
        theme_id: 소속 테마 PK.
        asset_id: 멤버 자산 PK.
        added_at: 추가 시각 (PK 일부).
        removed_at: soft-delete 시각. NULL = 활성 멤버. 활성 필터링은
            ``ix_theme_assets_active`` 부분 인덱스 가속 (alembic 0005).
        note: 편입 사유 등 사용자 메모. None 가능.
    """

    theme_id: int
    asset_id: int
    added_at: datetime
    removed_at: datetime | None
    note: str | None


@dataclass(frozen=True, slots=True)
class AssetThemeHistory:
    """자산 단위 ADDED/REMOVED/RECLASSIFIED 이벤트 append-only 로그.

    service 레이어가 add/remove 트랜잭션 안에서 ThemeAsset 변경과 동시에 1행
    INSERT 한다 (architecture.md L935-937 "이력 트리거 정책" — application layer
    책임).

    Attributes:
        history_id: BIGSERIAL PK.
        asset_id: 대상 자산 PK.
        theme_id: 이벤트 발생 테마 PK.
        event_type: ADDED / REMOVED / RECLASSIFIED 중 하나
            (DB CHECK 제약 동기 — `backend/app/models/theme.py:106`).
        from_theme_id: RECLASSIFIED 시 출처 테마 PK. 그 외 None.
        occurred_at: 이벤트 발생 시각.
        source: USER (수동 편집) | AUTO (자동 분류). 기본 USER.
        note: 자유 메모.
    """

    history_id: int
    asset_id: int
    theme_id: int
    event_type: EventType
    from_theme_id: int | None
    occurred_at: datetime
    source: HistorySource
    note: str | None
