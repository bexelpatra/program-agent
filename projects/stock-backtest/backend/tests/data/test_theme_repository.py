"""SqlThemeRepository 통합 테스트 (TASK-302).

실제 PostgreSQL 에 연결해 alembic 0005 schema 위에서 검증한다. 테스트마다
**최외곽 트랜잭션 + savepoint** 패턴으로 격리하여 row 누적을 방지한다.

전제:
    - 환경변수 DATABASE_URL 이 가리키는 PG 에 `alembic upgrade head` 가 완료되어
      있어야 한다 (alembic version >= 0005_theme_tables).
    - `assets` 테이블에 asset_id 가 최소 2개 존재해야 한다 (FK RESTRICT). 시드
      마이그레이션 (TASK-013) 으로 충분.

5 케이스 (DoD (b) 매핑):
    1) create_theme + get_theme + list_themes 정상 흐름
    2) update_theme + soft_delete_theme 정상 (LookupError 분기 포함)
    3) add_asset + list_active_assets (removed_at IS NULL 필터 검증)
    4) remove_asset 후 list_active_assets 에서 제외 (soft-delete)
    5) list_history (theme_assets 변경 시 별도 append_history 호출 후 결과)
"""

from __future__ import annotations

import os
import uuid
from collections.abc import Iterator

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

from app.data.theme_repository import SqlAlchemyUnitOfWork, SqlThemeRepository


# === fixture ================================================================


def _make_engine():
    """conftest.py 의 DATABASE_URL fallback 을 그대로 사용."""
    url = os.environ.get(
        "DATABASE_URL",
        "postgresql+psycopg2://stock:stock@localhost:5432/stock_backtest",
    )
    return create_engine(url, future=True, pool_pre_ping=True)


@pytest.fixture(scope="module")
def _engine():
    eng = _make_engine()
    # 연결 자체가 실패하면 모듈 전체 SKIP (BLOCKER-001 잔재 환경 보호).
    try:
        with eng.connect() as c:
            c.execute(text("SELECT 1"))
    except Exception as ex:  # noqa: BLE001
        pytest.skip(f"PostgreSQL 연결 불가 — 통합 테스트 SKIP: {ex}")
    # alembic 0005 적용 확인 — themes 테이블 존재 여부로 단순 검증.
    with eng.connect() as c:
        ok = c.execute(text("SELECT to_regclass('themes')")).scalar()
        if ok is None:
            pytest.skip(
                "themes 테이블 부재 — alembic upgrade head 필요. 통합 테스트 SKIP."
            )
    yield eng
    eng.dispose()


@pytest.fixture()
def session(_engine) -> Iterator[Session]:
    """테스트 격리를 위한 최외곽 트랜잭션 + savepoint pattern.

    SQLAlchemy 공식 권장 패턴: 함수가 끝나면 connection.rollback() 으로 모든
    INSERT/UPDATE 가 사라진다. 안쪽에서 session.commit() 을 호출해도 savepoint
    이므로 실제 DB 에는 반영되지 않는다.
    """
    connection = _engine.connect()
    trans = connection.begin()
    s = Session(bind=connection, autoflush=False, expire_on_commit=False)
    # SAVEPOINT 시작 — Session.commit() 이 호출돼도 외곽 trans 까지 commit 되지
    # 않게 한다. nested transaction 종료 시 새 SAVEPOINT 를 자동 시작 (SQLAlchemy
    # 2.x 권장 begin_nested + event hook 대안).
    s.begin_nested()
    from sqlalchemy import event

    @event.listens_for(s, "after_transaction_end")
    def _restart_savepoint(sess: Session, transaction):
        if transaction.nested and not transaction._parent.nested:  # type: ignore[attr-defined]
            sess.begin_nested()

    try:
        yield s
    finally:
        s.close()
        trans.rollback()
        connection.close()


@pytest.fixture()
def asset_ids(session: Session) -> tuple[int, int]:
    """FK 충족용 asset_id 2개 — 시드된 자산 중 가장 작은 두 개."""
    rows = session.execute(
        text("SELECT asset_id FROM assets ORDER BY asset_id LIMIT 2")
    ).all()
    if len(rows) < 2:
        pytest.skip("assets 시드 자산 부족 — 통합 테스트에 최소 2개 필요.")
    return rows[0][0], rows[1][0]


def _slug() -> str:
    """UNIQUE (user_id, slug) 충돌 회피를 위한 고유 slug 생성."""
    return f"theme-{uuid.uuid4().hex[:8]}"


# === 케이스 1: create_theme + get_theme + list_themes ========================


def test_create_get_list_themes(session: Session):
    repo = SqlThemeRepository(session)
    user = f"u-{uuid.uuid4().hex[:6]}"
    slug = _slug()

    created = repo.create_theme(
        name="정치 - 이재명",
        slug=slug,
        description="2026 대선 관련주",
        user_id=user,
    )
    assert created.theme_id > 0
    assert created.name == "정치 - 이재명"
    assert created.slug == slug
    assert created.user_id == user
    assert created.created_at is not None  # server_default 채워짐.

    # get
    fetched = repo.get_theme(created.theme_id)
    assert fetched is not None
    assert fetched.theme_id == created.theme_id
    assert fetched.description == "2026 대선 관련주"

    # 없는 ID
    assert repo.get_theme(9_999_999) is None

    # list — 동일 user_id 로 2번째 테마 추가 후 정렬 검증
    repo.create_theme(name="가가가", slug=_slug(), description=None, user_id=user)
    themes = repo.list_themes(user_id=user)
    assert len(themes) == 2
    # 이름 정렬 — '가가가' (가나다) < '정치 - 이재명'
    assert themes[0].name == "가가가"
    assert themes[1].name == "정치 - 이재명"

    # 다른 user_id 는 비어있다.
    assert repo.list_themes(user_id="other-user") == []


# === 케이스 2: update_theme + soft_delete_theme ==============================


def test_update_and_soft_delete_theme(session: Session, asset_ids: tuple[int, int]):
    repo = SqlThemeRepository(session)
    user = f"u-{uuid.uuid4().hex[:6]}"

    t = repo.create_theme(
        name="원본명",
        slug=_slug(),
        description="원본 설명",
        user_id=user,
    )

    # 부분 갱신 — name 만 변경
    updated = repo.update_theme(t.theme_id, name="새이름")
    assert updated.name == "새이름"
    assert updated.description == "원본 설명"  # 유지

    # description 만 변경
    updated2 = repo.update_theme(t.theme_id, description="새설명")
    assert updated2.name == "새이름"  # 유지
    assert updated2.description == "새설명"

    # 둘 다 None → 변경 없음
    updated3 = repo.update_theme(t.theme_id)
    assert updated3.name == "새이름"
    assert updated3.description == "새설명"

    # 없는 ID → LookupError
    with pytest.raises(LookupError):
        repo.update_theme(9_999_999, name="x")

    # soft_delete — 활성 멤버 일괄 종료 검증
    a1, a2 = asset_ids
    repo.add_asset(t.theme_id, a1)
    repo.add_asset(t.theme_id, a2)
    active_before = repo.list_active_assets(t.theme_id)
    assert len(active_before) == 2

    repo.soft_delete_theme(t.theme_id)
    active_after = repo.list_active_assets(t.theme_id)
    assert active_after == []  # 모두 removed_at NOW().

    # 없는 ID → LookupError
    with pytest.raises(LookupError):
        repo.soft_delete_theme(9_999_999)


# === 케이스 3: add_asset + list_active_assets ================================


def test_add_asset_and_list_active(session: Session, asset_ids: tuple[int, int]):
    repo = SqlThemeRepository(session)
    user = f"u-{uuid.uuid4().hex[:6]}"
    t = repo.create_theme(name="t3", slug=_slug(), description=None, user_id=user)
    a1, a2 = asset_ids

    m1 = repo.add_asset(t.theme_id, a1, note="m1 note")
    assert m1.theme_id == t.theme_id
    assert m1.asset_id == a1
    assert m1.removed_at is None
    assert m1.note == "m1 note"
    assert m1.added_at is not None

    m2 = repo.add_asset(t.theme_id, a2)
    assert m2.asset_id == a2
    assert m2.note is None

    # 활성 멤버 2개, added_at 정렬
    active = repo.list_active_assets(t.theme_id)
    assert len(active) == 2
    assert {x.asset_id for x in active} == {a1, a2}
    # 다른 theme 의 활성 멤버는 빈 리스트
    assert repo.list_active_assets(9_999_999) == []


# === 케이스 4: remove_asset 후 list_active_assets 제외 =======================


def test_remove_asset_excluded_from_active(
    session: Session, asset_ids: tuple[int, int]
):
    repo = SqlThemeRepository(session)
    user = f"u-{uuid.uuid4().hex[:6]}"
    t = repo.create_theme(name="t4", slug=_slug(), description=None, user_id=user)
    a1, a2 = asset_ids
    repo.add_asset(t.theme_id, a1)
    repo.add_asset(t.theme_id, a2)
    assert len(repo.list_active_assets(t.theme_id)) == 2

    repo.remove_asset(t.theme_id, a1)
    active = repo.list_active_assets(t.theme_id)
    assert len(active) == 1
    assert active[0].asset_id == a2

    # 제거된 a1 row 는 물리 삭제가 아닌 soft-delete — 직접 SELECT 로 확인
    # (removed_at 이 채워져 있어야 한다). list_active_assets 가 부분 인덱스
    # WHERE removed_at IS NULL 로 필터링한다는 invariant 검증.
    raw = session.execute(
        text(
            "SELECT removed_at FROM theme_assets "
            "WHERE theme_id = :tid AND asset_id = :aid"
        ),
        {"tid": t.theme_id, "aid": a1},
    ).all()
    assert len(raw) == 1
    assert raw[0][0] is not None  # removed_at NOW().

    # 다시 remove_asset 호출은 영향 row 0 (이미 removed) — 에러 없이 통과 (sevice 가
    # 사전 검증으로 차단하지만 Repository 자체는 단일 작업만 수행하므로 멱등).
    repo.remove_asset(t.theme_id, a1)
    active2 = repo.list_active_assets(t.theme_id)
    assert len(active2) == 1
    assert active2[0].asset_id == a2


# === 케이스 5: list_history (append_history 별도 호출 후 조회) ===============


def test_append_and_list_history(session: Session, asset_ids: tuple[int, int]):
    repo = SqlThemeRepository(session)
    user = f"u-{uuid.uuid4().hex[:6]}"
    t = repo.create_theme(name="t5", slug=_slug(), description=None, user_id=user)
    a1, _ = asset_ids

    # add → history(ADDED) — service 흐름 모사 (Repository 가 단일 작업만 수행)
    repo.add_asset(t.theme_id, a1)
    h1 = repo.append_history(
        asset_id=a1,
        theme_id=t.theme_id,
        event_type="ADDED",
        source="USER",
        note="추가 사유",
    )
    assert h1.history_id > 0
    assert h1.event_type == "ADDED"
    assert h1.from_theme_id is None
    assert h1.source == "USER"
    assert h1.occurred_at is not None

    # remove → history(REMOVED)
    repo.remove_asset(t.theme_id, a1)
    repo.append_history(
        asset_id=a1,
        theme_id=t.theme_id,
        event_type="REMOVED",
        source="USER",
    )

    # 다른 자산에 대한 history 는 본 asset_id 의 list_history 에 포함되지 않음
    # — RECLASSIFIED 1건을 다른 asset 으로 추가하고 검증.
    _, a2 = asset_ids
    repo.append_history(
        asset_id=a2,
        theme_id=t.theme_id,
        event_type="RECLASSIFIED",
        source="AUTO",
        note="다른 자산",
    )

    hist_a1 = repo.list_history(a1)
    assert len(hist_a1) == 2
    # occurred_at 정렬 — ADDED 가 먼저
    assert [h.event_type for h in hist_a1] == ["ADDED", "REMOVED"]

    hist_a2 = repo.list_history(a2)
    assert len(hist_a2) == 1
    assert hist_a2[0].event_type == "RECLASSIFIED"
    assert hist_a2[0].source == "AUTO"


# === 보조: UnitOfWork 어댑터 ==================================================


def test_unit_of_work_commit_and_rollback(_engine):
    """SqlAlchemyUnitOfWork 가 commit/rollback 을 Session 에 위임하는지 검증."""

    class _SpySession:
        def __init__(self):
            self.commits = 0
            self.rollbacks = 0

        def commit(self):
            self.commits += 1

        def rollback(self):
            self.rollbacks += 1

    spy = _SpySession()
    uow = SqlAlchemyUnitOfWork(spy)  # type: ignore[arg-type]
    uow.commit()
    uow.commit()
    uow.rollback()
    assert spy.commits == 2
    assert spy.rollbacks == 1
