"""SqlThemeRepository — ThemeRepository Protocol 의 SQLAlchemy 2.0 구현.

domain (`app.domain.themes.entity` / `repository`) 의 frozen dataclass 와 ORM
(`app.models.theme`) 사이를 매핑한다. ORM 객체는 본 모듈을 벗어나지 않게 하여
service / API 가 SQLAlchemy 에 결합되지 않도록 한다.

설계 결정:
    - 패턴 reference: `backend/app/data/asset_repository.py` (TASK-031 DONE) —
      `_to_entity()` 매핑 일원화 + 생성자 Session 주입 + ON CONFLICT 활용.
    - **트랜잭션 책임 분리** (architecture.md L937 + TASK-301 본문): 각 메서드는
      단일 영속화 작업만 수행한다. commit/rollback 은 호출자(service) 가
      `UnitOfWork` 어댑터로 제어한다. 본 Repository 는 `self._session.flush()` 만
      호출해 INSERT/UPDATE 가 같은 트랜잭션 안에서 차후 호출에 가시화되게 한다.
    - **UnitOfWork 위치 결정** (TASK-302 본문 추가 지시):
        후보 (A) 본 파일 안에 `SqlAlchemyUnitOfWork` 함께 배치.
        후보 (B) `_unit_of_work.py` 별도 파일.
      => **(A) 채택**. 근거: ① 어댑터가 4 줄짜리 thin wrapper 라 파일 분리 이득
      없음 (한 곳에서 Theme 영속화 어댑터 set 을 함께 본다는 응집성 이득 > 분리
      이득). ② asset_repository.py 도 동일 컨텍스트(`engine` import 없는 단일
      파일) 패턴 — 일관성 유지. ③ `dependencies.py` 가 두 클래스를 같은 모듈에서
      import 하면 deps 그래프가 단순. 미래에 다른 Repository 들도 같은 UoW 를
      공유하게 되면 그때 _unit_of_work.py 로 추출하면 충분 (현재는 YAGNI).

soft-delete 정책 (TASK-301 인계 메모 응답):
    - `soft_delete_theme`: themes 테이블에 deleted_at 컬럼은 본 마이그레이션
      (alembic 0005) 에 없음. **회피 전략** = ``status`` 같은 신규 컬럼 신설 대신
      `description` prefix 마커 또는 별도 컬럼이 필요하나 alembic 변경은 본 태스크
      범위 밖. **현재 구현**: `soft_delete_theme` 는 themes row 를 **CASCADE 없이
      그대로 두고** `list_themes` 가 이를 필터링하지 않는다 — service/API 가 후속
      태스크에서 status 컬럼 추가 후 갱신. **본 태스크에서는 메서드 시그니처와
      "활성 멤버 일괄 soft-remove" 부수 효과만 보장** (active member 가 있으면
      모두 removed_at = NOW() 처리, history 는 service 책임이므로 본 메서드는
      append 하지 않음).
    - 이 결정은 TASK-303 의 DELETE /api/themes/{id} 가 "현재는 active 멤버 일괄
      해제만 보장한다" 는 명세를 가지게 한다 (Reviewer 의 후속 검토 시 조정 가능).
    - **없는 theme_id 처리**: update/soft_delete 가 LookupError raise — TASK-303
      이 404 매핑.
"""
from __future__ import annotations

from typing import cast

from sqlalchemy import select, update
from sqlalchemy.orm import Session

from app.domain.themes.entity import (
    AssetThemeHistory as AssetThemeHistoryEntity,
)
from app.domain.themes.entity import (
    EventType,
    HistorySource,
    Theme as ThemeEntity,
    ThemeAsset as ThemeAssetEntity,
)
from app.models.theme import (
    AssetThemeHistory as AssetThemeHistoryModel,
    Theme as ThemeModel,
    ThemeAsset as ThemeAssetModel,
)


# === ORM ↔ Entity 매핑 일원화 ================================================


def _theme_to_entity(model: ThemeModel) -> ThemeEntity:
    """ORM Theme → domain Theme."""
    return ThemeEntity(
        theme_id=model.theme_id,
        name=model.name,
        slug=model.slug,
        description=model.description,
        user_id=model.user_id,
        created_at=model.created_at,
    )


def _theme_asset_to_entity(model: ThemeAssetModel) -> ThemeAssetEntity:
    """ORM ThemeAsset → domain ThemeAsset."""
    return ThemeAssetEntity(
        theme_id=model.theme_id,
        asset_id=model.asset_id,
        added_at=model.added_at,
        removed_at=model.removed_at,
        note=model.note,
    )


def _history_to_entity(model: AssetThemeHistoryModel) -> AssetThemeHistoryEntity:
    """ORM AssetThemeHistory → domain AssetThemeHistory."""
    return AssetThemeHistoryEntity(
        history_id=model.history_id,
        asset_id=model.asset_id,
        theme_id=model.theme_id,
        event_type=cast(EventType, model.event_type),
        from_theme_id=model.from_theme_id,
        occurred_at=model.occurred_at,
        source=cast(HistorySource, model.source),
        note=model.note,
    )


# === Repository 구현 =========================================================


class SqlThemeRepository:
    """`ThemeRepository` Protocol 의 SQLAlchemy 2.0 구현 (덕 타이핑).

    Protocol 을 명시적으로 상속하지 않는다 — `asset_repository.SqlAssetRepository`
    와 일관성 (structural typing 으로 충분, runtime isinstance 는 Protocol 이
    `@runtime_checkable` 이므로 별도 검증 가능).

    트랜잭션은 호출자가 `SqlAlchemyUnitOfWork` 또는 직접 `session.commit()` 으로
    제어한다. 각 메서드는 `session.flush()` 만 호출해 같은 트랜잭션 내 후속 작업
    (예: history append) 이 INSERT 결과를 볼 수 있게 한다.
    """

    def __init__(self, session: Session):
        self._session = session

    # --- Theme CRUD ----------------------------------------------------------

    def create_theme(
        self,
        name: str,
        slug: str,
        description: str | None,
        user_id: str = "local",
    ) -> ThemeEntity:
        """themes INSERT. (user_id, slug) UNIQUE 충돌 시 IntegrityError 가 raise.

        service 가 IntegrityError 를 409 로 매핑 (TASK-303 책임).
        """
        model = ThemeModel(
            name=name,
            slug=slug,
            description=description,
            user_id=user_id,
        )
        self._session.add(model)
        # flush 로 PK + server_default(created_at) 채움.
        self._session.flush()
        return _theme_to_entity(model)

    def get_theme(self, theme_id: int) -> ThemeEntity | None:
        """PK 단건 조회. 없으면 None.

        현재 alembic 0005 schema 에는 deleted_at 컬럼이 없어 soft-delete 필터링
        없음 (위 모듈 docstring 참조).
        """
        model = self._session.get(ThemeModel, theme_id)
        return _theme_to_entity(model) if model else None

    def list_themes(self, user_id: str = "local") -> list[ThemeEntity]:
        """주어진 user_id 의 테마 목록 (이름 정렬)."""
        stmt = (
            select(ThemeModel)
            .where(ThemeModel.user_id == user_id)
            .order_by(ThemeModel.name)
        )
        rows = self._session.execute(stmt).scalars().all()
        return [_theme_to_entity(m) for m in rows]

    def update_theme(
        self,
        theme_id: int,
        name: str | None = None,
        description: str | None = None,
    ) -> ThemeEntity:
        """name/description 부분 갱신. None 인자는 갱신 스킵.

        Raises:
            LookupError: theme_id 가 존재하지 않음.
        """
        model = self._session.get(ThemeModel, theme_id)
        if model is None:
            raise LookupError(f"theme_id={theme_id} 가 존재하지 않습니다.")
        if name is not None:
            model.name = name
        if description is not None:
            model.description = description
        self._session.flush()
        return _theme_to_entity(model)

    def soft_delete_theme(self, theme_id: int) -> None:
        """테마 soft-delete — 활성 멤버 일괄 removed_at=NOW() 갱신.

        themes row 자체는 alembic 0005 스키마에 deleted_at 이 없어 보존된다
        (모듈 docstring 참조). 활성 멤버는 모두 종료 처리해 list_active_assets
        조회에서 자연스럽게 빠지게 한다. asset_theme_history 의 'REMOVED' 이벤트
        append 는 service 책임 (멤버별 호출) — 본 메서드는 영속화 1 작업만 수행.

        Raises:
            LookupError: theme_id 가 존재하지 않음.
        """
        model = self._session.get(ThemeModel, theme_id)
        if model is None:
            raise LookupError(f"theme_id={theme_id} 가 존재하지 않습니다.")
        # 활성 멤버 일괄 종료 (removed_at IS NULL → NOW()).
        from sqlalchemy import func

        stmt = (
            update(ThemeAssetModel)
            .where(
                ThemeAssetModel.theme_id == theme_id,
                ThemeAssetModel.removed_at.is_(None),
            )
            .values(removed_at=func.now())
        )
        self._session.execute(stmt)
        self._session.flush()

    # --- ThemeAsset 멤버십 ---------------------------------------------------

    def add_asset(
        self,
        theme_id: int,
        asset_id: int,
        note: str | None = None,
    ) -> ThemeAssetEntity:
        """theme_assets INSERT (단일 작업).

        중복 active 멤버 차단은 service 의 사전 검증 책임 (Protocol docstring).
        added_at server_default 가 flush 시 채워진다.
        """
        model = ThemeAssetModel(
            theme_id=theme_id,
            asset_id=asset_id,
            note=note,
        )
        self._session.add(model)
        self._session.flush()
        return _theme_asset_to_entity(model)

    def remove_asset(self, theme_id: int, asset_id: int) -> None:
        """활성 멤버의 removed_at 을 NOW() 로 갱신 (soft-delete, 단일 작업).

        ``removed_at IS NULL`` 조건이 부분 인덱스 ``ix_theme_assets_active`` 를
        트리거하도록 명시적 WHERE 절로 작성. 영향 row 0 인 경우는 service 가
        사전 검증으로 차단했으므로 본 메서드는 별도 raise 하지 않는다.
        """
        from sqlalchemy import func

        stmt = (
            update(ThemeAssetModel)
            .where(
                ThemeAssetModel.theme_id == theme_id,
                ThemeAssetModel.asset_id == asset_id,
                ThemeAssetModel.removed_at.is_(None),
            )
            .values(removed_at=func.now())
        )
        self._session.execute(stmt)
        self._session.flush()

    def list_active_assets(self, theme_id: int) -> list[ThemeAssetEntity]:
        """removed_at IS NULL 인 멤버 (added_at 정렬).

        ``WHERE removed_at IS NULL`` 절로 부분 인덱스 ``ix_theme_assets_active``
        가속을 트리거.
        """
        stmt = (
            select(ThemeAssetModel)
            .where(
                ThemeAssetModel.theme_id == theme_id,
                ThemeAssetModel.removed_at.is_(None),
            )
            .order_by(ThemeAssetModel.added_at)
        )
        rows = self._session.execute(stmt).scalars().all()
        return [_theme_asset_to_entity(m) for m in rows]

    # --- AssetThemeHistory ---------------------------------------------------

    def append_history(
        self,
        asset_id: int,
        theme_id: int,
        event_type: str,
        from_theme_id: int | None = None,
        source: str = "USER",
        note: str | None = None,
    ) -> AssetThemeHistoryEntity:
        """asset_theme_history append-only 로그에 1행 추가.

        event_type DB CHECK ('ADDED','REMOVED','RECLASSIFIED') 위반은
        IntegrityError 로 raise (service 가 사전 Literal 검증).
        """
        model = AssetThemeHistoryModel(
            asset_id=asset_id,
            theme_id=theme_id,
            event_type=event_type,
            from_theme_id=from_theme_id,
            source=source,
            note=note,
        )
        self._session.add(model)
        self._session.flush()
        return _history_to_entity(model)

    def list_history(self, asset_id: int) -> list[AssetThemeHistoryEntity]:
        """특정 자산의 모든 테마 변경 이력 (occurred_at 정렬)."""
        stmt = (
            select(AssetThemeHistoryModel)
            .where(AssetThemeHistoryModel.asset_id == asset_id)
            .order_by(AssetThemeHistoryModel.occurred_at)
        )
        rows = self._session.execute(stmt).scalars().all()
        return [_history_to_entity(m) for m in rows]


# === UnitOfWork 어댑터 ========================================================


class SqlAlchemyUnitOfWork:
    """SQLAlchemy Session 을 `UnitOfWork` Protocol 어댑터로 감싸는 thin wrapper.

    `app.domain.themes.service.UnitOfWork` Protocol (commit/rollback 2 메서드)
    만족. service 가 try/except 안에서 명시적으로 commit/rollback 을 호출하므로
    어댑터는 분기 없이 위임만 한다.

    FastAPI Dependency 가 같은 Session 인스턴스를 SqlThemeRepository 와 본
    어댑터 모두에 주입해야 트랜잭션 일관성이 보장된다 (TASK-303 의
    `get_theme_service` Depends 책임).
    """

    def __init__(self, session: Session):
        self._session = session

    def commit(self) -> None:
        self._session.commit()

    def rollback(self) -> None:
        self._session.rollback()
