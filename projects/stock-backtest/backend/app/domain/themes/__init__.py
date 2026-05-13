"""Theme 도메인 패키지 (V3 Phase 2 — 테마주 추적/관찰 모듈).

architecture.md V3 § "V3 Phase 2 — 테마주 추적/관찰 모듈" (L823~) 의 도메인 레이어.
SQLAlchemy/HTTP/시장 데이터 어댑터 의존을 배제한 순수 엔티티 + Repository Protocol +
멤버십 트랜잭션 박제 service 를 정의한다.

data 레이어 (`app.data.theme_repository.SqlThemeRepository`, TASK-302) 가 Protocol
을 구현하여 의존성 역전을 이룬다. API 라우터 (`app.api.themes`, TASK-303) 와
service 는 Protocol 만 import 한다.

도메인 격리 (architecture.md L1063-1067 + TASK-309):
    `app.domain.themes` ↔ `app.domain.{engine, strategy, allocators, filters,
    trade, portfolio}` 양방향 import 금지.
"""
from app.domain.themes.entity import (
    AssetThemeHistory,
    AttentionSource,
    EventType,
    HistorySource,
    Theme,
    ThemeAsset,
)
from app.domain.themes.normalization import (
    aggregate_equal_weighted,
    compute_theme_aggregate,
    rebase_multi_series,
    rebase_series,
)
from app.domain.themes.repository import ThemeRepository
from app.domain.themes.service import (
    DuplicateActiveMember,
    InactiveMember,
    ThemeMembershipError,
    UnitOfWork,
    add_asset_to_theme,
    list_asset_history,
    remove_asset_from_theme,
)

__all__ = [
    # entity
    "AssetThemeHistory",
    "AttentionSource",
    "EventType",
    "HistorySource",
    "Theme",
    "ThemeAsset",
    # repository
    "ThemeRepository",
    # service
    "DuplicateActiveMember",
    "InactiveMember",
    "ThemeMembershipError",
    "UnitOfWork",
    "add_asset_to_theme",
    "list_asset_history",
    "remove_asset_from_theme",
    # normalization (TASK-304)
    "aggregate_equal_weighted",
    "compute_theme_aggregate",
    "rebase_multi_series",
    "rebase_series",
]
