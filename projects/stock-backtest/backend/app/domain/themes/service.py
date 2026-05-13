"""테마 멤버십 트랜잭션 박제 서비스.

architecture.md V3 § "V3 Phase 2" L935-937 "이력 트리거 정책":
    `theme_assets` 의 INSERT / UPDATE(removed_at) 가 일어날 때 application layer 가
    `asset_theme_history` row 를 자동 append. DB trigger 도 가능하나 SQLAlchemy/
    Alembic 의존성 단순화를 위해 **application layer 책임**으로 시작.

본 서비스는 두 가지 워크플로우를 단일 트랜잭션으로 박제한다:
    1) add_asset_to_theme — theme_assets INSERT + asset_theme_history INSERT
       (event_type='ADDED')
    2) remove_asset_from_theme — theme_assets UPDATE removed_at=NOW() +
       asset_theme_history INSERT (event_type='REMOVED')

트랜잭션 경계 제어 — UnitOfWork 패턴 선택 근거 (TASK-301 본문 추가 지시):
    "commit_unit_of_work: Callable[[], None] 같은 추상 인자" 또는 "Repository 의
    __enter__/__exit__ 기반 단순화" 중 선택해 근거를 보고하라.
    -> **UnitOfWork Protocol** 채택 (commit/rollback 두 메서드). Callable 1개로는
    실패 시 rollback 분기를 강제하기 어렵고, 컨텍스트 매니저는 본 두 워크플로우
    에서 service 가 "도메인 위반 → 예외 (rollback)" 와 "Repository 예외 → 예외
    (rollback)" 두 분기를 모두 명시적으로 다뤄야 해 try/except 안에서 commit/
    rollback 을 직접 호출하는 편이 흐름이 더 명확하기 때문이다.
    이 결정은 service 만 의존성을 가지며, SqlThemeRepository (TASK-302) 는 SQLAlchemy
    Session.commit/rollback 을 UnitOfWork 로 어댑팅하는 thin wrapper 만 추가하면
    된다.
"""
from __future__ import annotations

from typing import Protocol

from app.domain.themes.entity import AssetThemeHistory, ThemeAsset
from app.domain.themes.repository import ThemeRepository


# --- 예외 (사용자 노출 가능 한국어 메시지) -----------------------------------


class ThemeMembershipError(Exception):
    """테마 멤버십 도메인 규칙 위반 — service 가 사전 검증 단계에서 raise.

    구체 서브클래스 (DuplicateActiveMember / InactiveMember) 를 통해 호출자 (API
    라우터) 가 409 / 404 매핑을 결정한다.
    """


class DuplicateActiveMember(ThemeMembershipError):
    """동일 (theme_id, asset_id) 가 이미 active 인 상태에서 add 시도."""


class InactiveMember(ThemeMembershipError):
    """제거 대상 (theme_id, asset_id) 가 active 상태가 아님 (이미 제거됐거나 없음)."""


# --- 트랜잭션 경계 (UnitOfWork) ----------------------------------------------


class UnitOfWork(Protocol):
    """service 가 commit/rollback 을 직접 제어하기 위한 의존성 역전.

    SqlThemeRepository (TASK-302) 는 SQLAlchemy Session 을 감싸는 어댑터를
    제공할 책임이 있다. 단위 테스트에서는 in-memory fake 가 호출 카운트만
    검증한다.
    """

    def commit(self) -> None:
        """현재 트랜잭션을 commit."""
        ...

    def rollback(self) -> None:
        """현재 트랜잭션을 rollback."""
        ...


# --- 도메인 서비스 -----------------------------------------------------------


def add_asset_to_theme(
    repo: ThemeRepository,
    uow: UnitOfWork,
    theme_id: int,
    asset_id: int,
    note: str | None = None,
) -> ThemeAsset:
    """자산을 테마에 추가하고 history='ADDED' 를 single transaction 으로 박제.

    절차:
        1. 사전 검증 — 이미 active 멤버이면 DuplicateActiveMember raise (DB 호출 0).
        2. repo.add_asset — theme_assets INSERT.
        3. repo.append_history(event_type='ADDED') — asset_theme_history INSERT.
        4. uow.commit. 어느 한 단계라도 raise 하면 uow.rollback 후 예외 전파.

    Args:
        repo: ThemeRepository 구현체.
        uow: 트랜잭션 경계.
        theme_id: 대상 테마.
        asset_id: 추가할 자산.
        note: 편입 사유 사용자 메모 (선택).

    Returns:
        생성된 ThemeAsset.

    Raises:
        DuplicateActiveMember: 이미 active 멤버.
        Exception: Repository 또는 UnitOfWork 가 raise 한 영속화 오류. service 가
            rollback 후 그대로 전파한다.
    """
    # 1) 사전 검증
    active = repo.list_active_assets(theme_id)
    if any(m.asset_id == asset_id for m in active):
        raise DuplicateActiveMember(
            f"이미 추가된 자산입니다: theme_id={theme_id} asset_id={asset_id}"
        )

    # 2~4) 단일 트랜잭션. 어느 INSERT 도 실패하면 rollback 후 전파.
    try:
        member = repo.add_asset(theme_id, asset_id, note=note)
        repo.append_history(
            asset_id=asset_id,
            theme_id=theme_id,
            event_type="ADDED",
            source="USER",
            note=note,
        )
        uow.commit()
    except Exception:
        uow.rollback()
        raise

    return member


def remove_asset_from_theme(
    repo: ThemeRepository,
    uow: UnitOfWork,
    theme_id: int,
    asset_id: int,
    note: str | None = None,
) -> None:
    """자산을 테마에서 제거 (soft) 하고 history='REMOVED' 를 single transaction 으로 박제.

    절차:
        1. 사전 검증 — active 멤버가 아니면 InactiveMember raise.
        2. repo.remove_asset — theme_assets UPDATE removed_at=NOW().
        3. repo.append_history(event_type='REMOVED').
        4. uow.commit. 실패 시 uow.rollback 후 예외 전파.

    Args:
        repo: ThemeRepository 구현체.
        uow: 트랜잭션 경계.
        theme_id: 대상 테마.
        asset_id: 제거할 자산.
        note: 제거 사유 사용자 메모 (선택, history.note 에 적재).

    Raises:
        InactiveMember: 활성 멤버가 아니어서 제거할 수 없음.
        Exception: Repository 또는 UnitOfWork 가 raise 한 영속화 오류 — rollback 후
            그대로 전파.
    """
    # 1) 사전 검증
    active = repo.list_active_assets(theme_id)
    if not any(m.asset_id == asset_id for m in active):
        raise InactiveMember(
            f"활성 멤버가 아닙니다: theme_id={theme_id} asset_id={asset_id}"
        )

    # 2~4) 단일 트랜잭션.
    try:
        repo.remove_asset(theme_id, asset_id)
        repo.append_history(
            asset_id=asset_id,
            theme_id=theme_id,
            event_type="REMOVED",
            source="USER",
            note=note,
        )
        uow.commit()
    except Exception:
        uow.rollback()
        raise


# --- 보조 조회 (편의 함수) ---------------------------------------------------


def list_asset_history(
    repo: ThemeRepository, asset_id: int
) -> list[AssetThemeHistory]:
    """자산의 모든 테마 이력 (occurred_at 정렬).

    GET /api/assets/{asset_id}/theme_history (TASK-303) 에서 사용. 트랜잭션
    불필요 (단순 SELECT) — UnitOfWork 인자 없음.
    """
    return repo.list_history(asset_id)
