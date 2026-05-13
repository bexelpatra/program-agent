"""Theme Repository Protocol — 의존성 역전.

domain 이 인터페이스를 정의하고 data 레이어 (`app.data.theme_repository`) 가
구현한다 (clean architecture, TASK-302 분담).

architecture.md V3 § "V3 Phase 2" L990-998 (`backend/app/domain/themes/repository.py`)
근거. service 레이어 (`app.domain.themes.service`) 와 API 라우터 (`app.api.themes`)
는 Protocol 만 import 한다 — SQLAlchemy 구현 교체 자유.

트랜잭션 책임 분리 (architecture.md L937 + TASK-301 본문):
    - Repository Protocol 자체는 트랜잭션을 인지하지 않는다. 각 메서드는 단일
      작업만 수행한다.
    - 트랜잭션 경계 (commit / rollback) 제어는 service 가 책임지며, SqlThemeRepository
      는 service 가 주입한 unit-of-work 컨텍스트 안에서 모든 호출을 실행한다.
"""
from __future__ import annotations

from typing import Protocol, runtime_checkable

from app.domain.themes.entity import AssetThemeHistory, Theme, ThemeAsset


@runtime_checkable
class ThemeRepository(Protocol):
    """테마 / 멤버십 / 이력 영속화 인터페이스.

    구현 가이드:
        - 모든 메서드는 트랜잭션 경계를 열지 않는다. 호출자(service) 가 단일
          unit-of-work 안에서 여러 메서드를 호출 후 commit/rollback 한다.
        - 예외 정책: 영속화 실패는 raise (service 가 rollback 결정).
          "이미 활성 멤버" / "없는 멤버" 같은 도메인 위반은 service 가 사전 검증한
          뒤 호출하므로 본 인터페이스에서는 별도 ValueError 를 약속하지 않는다.
    """

    # --- Theme CRUD ----------------------------------------------------------

    def create_theme(
        self,
        name: str,
        slug: str,
        description: str | None,
        user_id: str = "local",
    ) -> Theme:
        """새 테마를 생성하고 PK 가 채워진 Theme 을 반환.

        (user_id, slug) UNIQUE 충돌 시 IntegrityError 가 raise 된다
        (호출자 = service 가 409 매핑 책임).
        """
        ...

    def get_theme(self, theme_id: int) -> Theme | None:
        """PK 단건 조회. 없으면 None. soft-delete 된 테마는 본 인터페이스 범위
        밖이며, 구현체에 따라 None / Theme 둘 다 가능 (TASK-302 결정)."""
        ...

    def list_themes(self, user_id: str = "local") -> list[Theme]:
        """주어진 user_id 의 활성 테마 목록 (이름 정렬).

        soft-delete 된 테마는 제외 (구현체 책임).
        """
        ...

    def update_theme(
        self,
        theme_id: int,
        name: str | None = None,
        description: str | None = None,
    ) -> Theme:
        """name/description 부분 갱신. None 인자는 갱신 스킵.

        Returns:
            갱신된 Theme 엔티티.

        Raises:
            LookupError 류 (구현체 정의) when theme_id not found.
        """
        ...

    def soft_delete_theme(self, theme_id: int) -> None:
        """테마 soft-delete. 멤버십/이력 row 는 보존된다 (architecture.md L1027).

        구현 방법은 구현체 자율 (status 컬럼 추가 vs deleted_at 컬럼 vs 별도 table).
        TASK-302 에서 최종 결정.
        """
        ...

    # --- ThemeAsset 멤버십 ---------------------------------------------------

    def add_asset(
        self,
        theme_id: int,
        asset_id: int,
        note: str | None = None,
    ) -> ThemeAsset:
        """theme_assets 에 INSERT. 동일 (theme_id, asset_id) 가 이미 active 일
        때의 처리 정책은 service 가 사전 검증으로 차단한다 (본 메서드는 단순 INSERT).

        Returns:
            생성된 ThemeAsset (added_at server_default 가 채워진 상태).
        """
        ...

    def remove_asset(self, theme_id: int, asset_id: int) -> None:
        """활성 멤버의 removed_at 을 NOW() 로 갱신 (soft-delete).

        활성 멤버가 없으면 영향 row 0 — service 가 사전 검증으로 차단한다.
        """
        ...

    def list_active_assets(self, theme_id: int) -> list[ThemeAsset]:
        """removed_at IS NULL 인 멤버만 반환 (added_at 정렬).

        ``ix_theme_assets_active`` 부분 인덱스로 가속 (alembic 0005).
        """
        ...

    # --- AssetThemeHistory ---------------------------------------------------

    def append_history(
        self,
        asset_id: int,
        theme_id: int,
        event_type: str,
        from_theme_id: int | None = None,
        source: str = "USER",
        note: str | None = None,
    ) -> AssetThemeHistory:
        """asset_theme_history append-only 로그에 1행 추가.

        service 가 add_asset / remove_asset 직후 같은 unit-of-work 안에서 호출한다
        (architecture.md L937 "application layer 책임"). event_type 은 Literal
        ADDED/REMOVED/RECLASSIFIED — DB CHECK 제약이 위반을 차단한다.

        Returns:
            history_id 가 채워진 AssetThemeHistory.
        """
        ...

    def list_history(self, asset_id: int) -> list[AssetThemeHistory]:
        """특정 자산의 모든 테마 변경 이력 (occurred_at 정렬).

        화면 5 (테마 상세) 및 GET /api/assets/{asset_id}/theme_history 에서 사용
        (architecture.md L1033 + TASK-303).
        """
        ...
