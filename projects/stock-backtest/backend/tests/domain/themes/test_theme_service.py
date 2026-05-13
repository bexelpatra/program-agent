"""Theme 멤버십 트랜잭션 박제 service 단위 테스트 (TASK-301 DoD (c)).

검증 범위:
    1) 정상 add_asset_to_theme — theme_assets row 1건 + history 1건 (ADDED) + commit 1회.
    2) 정상 remove_asset_from_theme — theme_assets removed_at 갱신 + history 1건
       (REMOVED) + commit 1회.
    3) 중복 add 거부 — DuplicateActiveMember + history append 0건 (DB 호출 0, commit 0).
    4) 없는 자산 remove 거부 — InactiveMember + history append 0건.
    5) history insert 실패 → rollback 으로 theme_assets insert 도 함께 폐기.

clean architecture: ThemeRepository / UnitOfWork Protocol 을 in-memory fake 로 구현
하여 SQLAlchemy / DB 의존을 끊는다. 실 DB 통합 테스트는 TASK-302 분담.
"""

from __future__ import annotations

from dataclasses import replace
from datetime import datetime, timezone

import pytest

from app.domain.themes import (
    AssetThemeHistory,
    DuplicateActiveMember,
    InactiveMember,
    Theme,
    ThemeAsset,
    ThemeRepository,
    UnitOfWork,
    add_asset_to_theme,
    remove_asset_from_theme,
)


# --- In-memory fake Repository ----------------------------------------------


class _FakeThemeRepository:
    """ThemeRepository Protocol 의 in-memory 구현 (rollback 지원).

    snapshot/restore 패턴으로 rollback 을 모사한다 — UnitOfWork.rollback 호출 시
    가장 최근 commit 시점 상태로 되돌린다.
    """

    def __init__(self, *, fail_on_history: bool = False) -> None:
        # 활성+비활성 멤버 모두 보관. removed_at IS NULL == 활성.
        self.members: list[ThemeAsset] = []
        self.history: list[AssetThemeHistory] = []
        # rollback 용 스냅샷 (commit 시 갱신, rollback 시 복원).
        self._members_snapshot: list[ThemeAsset] = []
        self._history_snapshot: list[AssetThemeHistory] = []
        # append_history 강제 실패 토글 (TC5 용).
        self._fail_on_history = fail_on_history
        # 호출 카운트 (단위 테스트 가시성).
        self.add_asset_calls = 0
        self.remove_asset_calls = 0
        self.append_history_calls = 0

    # --- ThemeRepository 인터페이스 (사용되는 메서드만 구현) -----------------

    def list_active_assets(self, theme_id: int) -> list[ThemeAsset]:
        return [
            m for m in self.members if m.theme_id == theme_id and m.removed_at is None
        ]

    def add_asset(
        self, theme_id: int, asset_id: int, note: str | None = None
    ) -> ThemeAsset:
        self.add_asset_calls += 1
        member = ThemeAsset(
            theme_id=theme_id,
            asset_id=asset_id,
            added_at=datetime(2026, 5, 12, 10, 0, 0, tzinfo=timezone.utc),
            removed_at=None,
            note=note,
        )
        self.members.append(member)
        return member

    def remove_asset(self, theme_id: int, asset_id: int) -> None:
        self.remove_asset_calls += 1
        for i, m in enumerate(self.members):
            if (
                m.theme_id == theme_id
                and m.asset_id == asset_id
                and m.removed_at is None
            ):
                self.members[i] = replace(
                    m,
                    removed_at=datetime(2026, 5, 12, 11, 0, 0, tzinfo=timezone.utc),
                )
                return

    def append_history(
        self,
        asset_id: int,
        theme_id: int,
        event_type: str,
        from_theme_id: int | None = None,
        source: str = "USER",
        note: str | None = None,
    ) -> AssetThemeHistory:
        self.append_history_calls += 1
        if self._fail_on_history:
            raise RuntimeError("forced history insert failure")
        h = AssetThemeHistory(
            history_id=len(self.history) + 1,
            asset_id=asset_id,
            theme_id=theme_id,
            event_type=event_type,  # type: ignore[arg-type]
            from_theme_id=from_theme_id,
            occurred_at=datetime(2026, 5, 12, 10, 0, 1, tzinfo=timezone.utc),
            source=source,  # type: ignore[arg-type]
            note=note,
        )
        self.history.append(h)
        return h

    # --- rollback 모사용 (commit/rollback 시 UnitOfWork 가 호출) -------------

    def _snapshot(self) -> None:
        self._members_snapshot = list(self.members)
        self._history_snapshot = list(self.history)

    def _restore(self) -> None:
        self.members = list(self._members_snapshot)
        self.history = list(self._history_snapshot)


class _FakeUnitOfWork:
    """UnitOfWork Protocol 의 in-memory 구현.

    commit 시 repo 의 현재 상태를 스냅샷, rollback 시 직전 commit 상태로 복원.
    """

    def __init__(self, repo: _FakeThemeRepository) -> None:
        self._repo = repo
        self.commit_calls = 0
        self.rollback_calls = 0
        # 초기 상태도 commit 된 상태로 간주.
        self._repo._snapshot()

    def commit(self) -> None:
        self.commit_calls += 1
        self._repo._snapshot()

    def rollback(self) -> None:
        self.rollback_calls += 1
        self._repo._restore()


# --- Protocol 컴파일 타임 호환성 ---------------------------------------------

_REPO_PROTOCOL_HINT: type[ThemeRepository] = _FakeThemeRepository  # type: ignore[type-abstract]
_UOW_PROTOCOL_HINT: type[UnitOfWork] = _FakeUnitOfWork  # type: ignore[type-abstract]


# --- 테스트 ------------------------------------------------------------------


def test_add_asset_to_theme_normal() -> None:
    """정상 add — theme_assets row 1건 + history(ADDED) 1건 + commit 1회."""
    repo = _FakeThemeRepository()
    uow = _FakeUnitOfWork(repo)

    member = add_asset_to_theme(repo, uow, theme_id=1, asset_id=10, note="편입사유A")

    # theme_assets row.
    assert len(repo.members) == 1
    assert repo.members[0].theme_id == 1
    assert repo.members[0].asset_id == 10
    assert repo.members[0].removed_at is None
    assert repo.members[0].note == "편입사유A"
    assert member == repo.members[0]

    # history row.
    assert len(repo.history) == 1
    assert repo.history[0].event_type == "ADDED"
    assert repo.history[0].theme_id == 1
    assert repo.history[0].asset_id == 10
    assert repo.history[0].source == "USER"
    assert repo.history[0].note == "편입사유A"

    # 트랜잭션 commit 1회 / rollback 0회.
    assert uow.commit_calls == 1
    assert uow.rollback_calls == 0

    # Repository 호출 카운트.
    assert repo.add_asset_calls == 1
    assert repo.append_history_calls == 1


def test_remove_asset_from_theme_normal() -> None:
    """정상 remove — removed_at 갱신 + history(REMOVED) 1건 + commit 1회."""
    repo = _FakeThemeRepository()
    uow = _FakeUnitOfWork(repo)

    # 사전 멤버 등록 (add 도 같은 service 통과 — 별도 commit).
    add_asset_to_theme(repo, uow, theme_id=2, asset_id=20)
    # add 1회 + remove 1회의 카운트 분리를 위해 베이스라인 캡처.
    base_commit = uow.commit_calls
    base_history = repo.append_history_calls

    remove_asset_from_theme(repo, uow, theme_id=2, asset_id=20, note="제거사유B")

    # 활성 멤버 = 0 (removed_at 채워짐).
    active = repo.list_active_assets(2)
    assert active == []
    # 비활성 row 는 보존.
    assert len(repo.members) == 1
    assert repo.members[0].removed_at is not None

    # history 1건 추가 (event_type=REMOVED).
    assert repo.append_history_calls == base_history + 1
    assert repo.history[-1].event_type == "REMOVED"
    assert repo.history[-1].theme_id == 2
    assert repo.history[-1].asset_id == 20
    assert repo.history[-1].note == "제거사유B"

    # 트랜잭션 commit 1회 추가 / rollback 0회.
    assert uow.commit_calls == base_commit + 1
    assert uow.rollback_calls == 0
    assert repo.remove_asset_calls == 1


def test_add_asset_duplicate_active_raises_and_no_writes() -> None:
    """이미 active 멤버 add → DuplicateActiveMember + DB 호출 0 + history 0."""
    repo = _FakeThemeRepository()
    uow = _FakeUnitOfWork(repo)

    # 사전: (1, 10) active.
    add_asset_to_theme(repo, uow, theme_id=1, asset_id=10)
    base_add = repo.add_asset_calls
    base_history = repo.append_history_calls
    base_commit = uow.commit_calls

    with pytest.raises(DuplicateActiveMember) as excinfo:
        add_asset_to_theme(repo, uow, theme_id=1, asset_id=10)

    # 한국어 메시지 일부 검증.
    assert "이미 추가된 자산입니다" in str(excinfo.value)
    # 사전 검증에서 차단됐으므로 Repository 쓰기 호출 0 증가.
    assert repo.add_asset_calls == base_add
    assert repo.append_history_calls == base_history
    # commit/rollback 모두 호출되지 않아야 함 (예외가 try 블록 진입 전에 raise).
    assert uow.commit_calls == base_commit
    assert uow.rollback_calls == 0


def test_remove_asset_not_active_raises_and_no_writes() -> None:
    """active 가 아닌 자산 remove → InactiveMember + DB 호출 0 + history 0."""
    repo = _FakeThemeRepository()
    uow = _FakeUnitOfWork(repo)

    # 사전: 멤버 없음. theme_id=3 에 asset_id=30 활성 멤버 없음.
    base_remove = repo.remove_asset_calls
    base_history = repo.append_history_calls
    base_commit = uow.commit_calls

    with pytest.raises(InactiveMember) as excinfo:
        remove_asset_from_theme(repo, uow, theme_id=3, asset_id=30)

    assert "활성 멤버가 아닙니다" in str(excinfo.value)
    assert repo.remove_asset_calls == base_remove
    assert repo.append_history_calls == base_history
    assert uow.commit_calls == base_commit
    assert uow.rollback_calls == 0


def test_add_rolls_back_when_history_insert_fails() -> None:
    """add 트랜잭션 도중 history insert 실패 → theme_assets insert 도 rollback."""
    repo = _FakeThemeRepository(fail_on_history=True)
    uow = _FakeUnitOfWork(repo)

    with pytest.raises(RuntimeError, match="forced history insert failure"):
        add_asset_to_theme(repo, uow, theme_id=5, asset_id=50)

    # rollback 1회 호출 + commit 0회.
    assert uow.rollback_calls == 1
    assert uow.commit_calls == 0

    # rollback 으로 멤버/이력 모두 비어 있는 상태로 복원.
    assert repo.members == []
    assert repo.history == []

    # add_asset 은 호출됐지만 (실패는 history 단계), rollback 이 effects 를 무효화.
    assert repo.add_asset_calls == 1
    assert repo.append_history_calls == 1


# --- 보조: list_active_assets / Theme dataclass smoke ------------------------


def test_theme_dataclass_is_frozen() -> None:
    """Theme / ThemeAsset / AssetThemeHistory 가 frozen 인지 (slots=True 동반)."""
    t = Theme(
        theme_id=1,
        name="정치 — 이재명",
        slug="politics-lee",
        description=None,
        user_id="local",
        created_at=datetime(2026, 5, 12, tzinfo=timezone.utc),
    )
    with pytest.raises((AttributeError, Exception)):
        t.name = "다른 이름"  # type: ignore[misc]
