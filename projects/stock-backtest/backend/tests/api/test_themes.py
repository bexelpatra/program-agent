"""Theme API 단위 테스트 (TASK-303 DoD (b) — 5 케이스).

테스트 케이스 매핑:
    1. POST + GET round-trip (정상 CRUD 1순환).
    2. PATCH 갱신 정상.
    3. DELETE soft delete 후 GET 200 (themes row 보존) + active_members 빈 리스트.
    4. add_asset + DELETE asset 정상 + theme_history 로 ADDED/REMOVED 이벤트 2건 조회.
    5. 404 (없는 theme_id GET / 없는 active asset DELETE) + 409 (중복 slug POST).

DB 가용성:
    BLOCKER-001 잔재 환경에서는 모든 테스트 SOFT skip (기존 test_api_contract.py
    패턴 동일).

격리:
    - 각 테스트가 고유 user_id 와 고유 slug 를 사용 (uuid suffix) 해 동일 DB 에서
      병렬/반복 실행 시 충돌 회피.
    - 생성한 themes 와 history row 는 cleanup 단계에서 직접 삭제 (CASCADE 가
      theme_assets / asset_theme_history 까지 일괄 정리).
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text

from app.core.db import SessionLocal, engine
from app.main import app
from app.models.asset import Asset as AssetModel


@pytest.fixture(scope="module")
def db_alive() -> bool:
    """test_api_contract.py 와 동일한 ping (alembic 0005 적용 + assets 시드)."""
    try:
        with engine.connect() as c:
            c.execute(text("SELECT 1"))
            # themes 테이블 존재 확인 (alembic 0005 적용 검증).
            c.execute(text("SELECT theme_id FROM themes LIMIT 1"))
            # assets 시드 확인 (FK RESTRICT 충족용).
            c.execute(text("SELECT asset_id FROM assets LIMIT 1"))
            return True
    except Exception:
        return False


@pytest.fixture(scope="module")
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture()
def db_session():
    """라우터 격리 외부에서 직접 SELECT/cleanup 하기 위한 세션."""
    s = SessionLocal()
    try:
        yield s
    finally:
        s.close()


@pytest.fixture()
def seed_assets(db_alive: bool, db_session) -> list[int]:
    """테스트 격리용 임시 자산 2개를 시드 후 finalizer 가 삭제.

    기존 시드 자산을 빌리면 다른 테스트와 충돌 (FK RESTRICT) 위험이 있어 본
    fixture 가 prefix-기반 임시 자산을 생성한다.
    """
    if not db_alive:
        pytest.skip("DB unavailable — BLOCKER-001 잔재 또는 alembic 0005 미적용")

    prefix = (
        f"TH303_{int(datetime.now(timezone.utc).timestamp())}_{uuid.uuid4().hex[:6]}"
    )
    seeded: list[int] = []
    rows = [
        AssetModel(
            symbol=f"{prefix}_A",
            market="KR",
            asset_type="ETF",
            currency="KRW",
            name=f"테마테스트A-{prefix}",
            meta={},
            active=True,
        ),
        AssetModel(
            symbol=f"{prefix}_B",
            market="KR",
            asset_type="ETF",
            currency="KRW",
            name=f"테마테스트B-{prefix}",
            meta={},
            active=True,
        ),
    ]
    for r in rows:
        db_session.add(r)
        db_session.flush()
        seeded.append(r.asset_id)
    db_session.commit()
    try:
        yield seeded
    finally:
        # 1) 자산이 멤버로 들어간 theme_assets / asset_theme_history 를 먼저 제거
        #    (FK RESTRICT 방어).
        cleanup = SessionLocal()
        try:
            for aid in seeded:
                cleanup.execute(
                    text("DELETE FROM asset_theme_history WHERE asset_id = :aid"),
                    {"aid": aid},
                )
                cleanup.execute(
                    text("DELETE FROM theme_assets WHERE asset_id = :aid"),
                    {"aid": aid},
                )
            cleanup.commit()
            for aid in seeded:
                row = cleanup.get(AssetModel, aid)
                if row is not None:
                    cleanup.delete(row)
            cleanup.commit()
        finally:
            cleanup.close()


def _unique_user() -> str:
    return f"u-{uuid.uuid4().hex[:8]}"


def _unique_slug() -> str:
    return f"theme-{uuid.uuid4().hex[:8]}"


def _cleanup_theme(theme_id: int) -> None:
    """테마와 그에 매달린 history/assets 일괄 삭제 (FK CASCADE 보강)."""
    s = SessionLocal()
    try:
        s.execute(
            text("DELETE FROM asset_theme_history WHERE theme_id = :tid"),
            {"tid": theme_id},
        )
        s.execute(
            text("DELETE FROM theme_assets WHERE theme_id = :tid"),
            {"tid": theme_id},
        )
        s.execute(text("DELETE FROM themes WHERE theme_id = :tid"), {"tid": theme_id})
        s.commit()
    finally:
        s.close()


# ============================================================================
# 케이스 1: POST + GET round-trip (정상 CRUD 1순환)
# ============================================================================


def test_create_get_list_round_trip(db_alive: bool, client: TestClient) -> None:
    """POST 로 테마 생성 → GET 단건 → GET 목록 → 단일 테마가 정확히 포함됨."""
    if not db_alive:
        pytest.skip("DB unavailable — BLOCKER-001 잔재")

    user = _unique_user()
    payload = {
        "name": "정치 - 이재명",
        "description": "2026 대선 관련주",
        "user_id": user,
    }
    # POST
    resp = client.post("/api/themes", json=payload)
    assert resp.status_code == 201, resp.text
    body = resp.json()
    theme_id = body["theme_id"]
    try:
        assert body["name"] == "정치 - 이재명"
        assert body["slug"]  # 자동 생성
        assert body["user_id"] == user
        assert body["description"] == "2026 대선 관련주"

        # GET 단건 (ThemeDetail — active_members 포함).
        resp2 = client.get(f"/api/themes/{theme_id}")
        assert resp2.status_code == 200
        detail = resp2.json()
        assert detail["theme_id"] == theme_id
        assert detail["active_members"] == []
        assert detail["member_count"] == 0

        # GET 목록 (해당 user_id 만 격리).
        resp3 = client.get("/api/themes", params={"user_id": user})
        assert resp3.status_code == 200
        listing = resp3.json()
        assert listing["total"] == 1
        assert len(listing["items"]) == 1
        assert listing["items"][0]["theme_id"] == theme_id
        # member_count 가 목록에 노출됨.
        assert listing["items"][0]["member_count"] == 0
    finally:
        _cleanup_theme(theme_id)


# ============================================================================
# 케이스 2: PATCH 갱신 정상
# ============================================================================


def test_patch_updates_name_and_description(db_alive: bool, client: TestClient) -> None:
    """PATCH 로 name 갱신 → description 갱신 → 모두 반영, 다른 필드 보존."""
    if not db_alive:
        pytest.skip("DB unavailable — BLOCKER-001 잔재")

    user = _unique_user()
    resp = client.post(
        "/api/themes",
        json={"name": "원본명", "description": "원본설명", "user_id": user},
    )
    assert resp.status_code == 201
    theme_id = resp.json()["theme_id"]
    try:
        # PATCH name 만
        r1 = client.patch(f"/api/themes/{theme_id}", json={"name": "새이름"})
        assert r1.status_code == 200, r1.text
        b1 = r1.json()
        assert b1["name"] == "새이름"
        assert b1["description"] == "원본설명"

        # PATCH description 만
        r2 = client.patch(f"/api/themes/{theme_id}", json={"description": "새설명"})
        assert r2.status_code == 200
        b2 = r2.json()
        assert b2["name"] == "새이름"
        assert b2["description"] == "새설명"

        # PATCH 빈 body — 모두 보존
        r3 = client.patch(f"/api/themes/{theme_id}", json={})
        assert r3.status_code == 200
        b3 = r3.json()
        assert b3["name"] == "새이름"
        assert b3["description"] == "새설명"
    finally:
        _cleanup_theme(theme_id)


# ============================================================================
# 케이스 3: DELETE soft delete 후 GET 200 (보존) + active_members 빈 리스트
# ============================================================================


def test_delete_soft_preserves_theme_row_but_clears_active_members(
    db_alive: bool, client: TestClient, seed_assets: list[int]
) -> None:
    """DELETE /api/themes/{id} 후 themes row 는 alembic 0005 schema 상 보존되며
    (deleted_at 컬럼 없음 — theme_repository 모듈 docstring) 활성 멤버만 일괄 종료.
    """
    if not db_alive:
        pytest.skip("DB unavailable — BLOCKER-001 잔재")

    user = _unique_user()
    a1, a2 = seed_assets

    # 테마 + 멤버 2개 추가.
    r = client.post("/api/themes", json={"name": "삭제대상", "user_id": user})
    assert r.status_code == 201
    theme_id = r.json()["theme_id"]
    try:
        client.post(f"/api/themes/{theme_id}/assets", json={"asset_id": a1})
        client.post(f"/api/themes/{theme_id}/assets", json={"asset_id": a2})

        # DELETE
        dr = client.delete(f"/api/themes/{theme_id}")
        assert dr.status_code == 204

        # themes row 는 보존 — GET 단건 200.
        gr = client.get(f"/api/themes/{theme_id}")
        assert gr.status_code == 200
        detail = gr.json()
        assert detail["theme_id"] == theme_id
        # 활성 멤버는 모두 종료 — 빈 리스트.
        assert detail["active_members"] == []
        assert detail["member_count"] == 0
    finally:
        _cleanup_theme(theme_id)


# ============================================================================
# 케이스 4: add_asset + DELETE asset 정상 + theme_history 2건 조회
# ============================================================================


def test_add_then_remove_asset_appends_history_events(
    db_alive: bool, client: TestClient, seed_assets: list[int]
) -> None:
    """POST asset → DELETE asset → GET /assets/{id}/theme_history 가 ADDED/REMOVED
    두 이벤트를 시간순으로 반환.
    """
    if not db_alive:
        pytest.skip("DB unavailable — BLOCKER-001 잔재")

    user = _unique_user()
    a1, _ = seed_assets

    r = client.post("/api/themes", json={"name": "히스토리테마", "user_id": user})
    assert r.status_code == 201
    theme_id = r.json()["theme_id"]
    try:
        # add — 201 + ThemeAssetRead
        ar = client.post(
            f"/api/themes/{theme_id}/assets",
            json={"asset_id": a1, "note": "편입사유"},
        )
        assert ar.status_code == 201, ar.text
        member = ar.json()
        assert member["theme_id"] == theme_id
        assert member["asset_id"] == a1
        assert member["note"] == "편입사유"
        assert member["removed_at"] is None

        # detail 에 활성 멤버 1
        d1 = client.get(f"/api/themes/{theme_id}")
        assert d1.status_code == 200
        assert len(d1.json()["active_members"]) == 1

        # remove — 204
        rr = client.delete(f"/api/themes/{theme_id}/assets/{a1}")
        assert rr.status_code == 204

        # 활성 멤버 0
        d2 = client.get(f"/api/themes/{theme_id}")
        assert d2.status_code == 200
        assert d2.json()["active_members"] == []

        # history 조회 — 2 events 시간순
        hr = client.get(f"/api/assets/{a1}/theme_history")
        assert hr.status_code == 200, hr.text
        events = hr.json()
        # 본 테스트가 격리된 자산을 사용하므로 이 자산의 이력은 정확히 2 건.
        assert len(events) == 2
        assert [e["event_type"] for e in events] == ["ADDED", "REMOVED"]
        assert all(e["asset_id"] == a1 for e in events)
        assert all(e["theme_id"] == theme_id for e in events)
        assert events[0]["note"] == "편입사유"
        assert events[0]["source"] == "USER"
    finally:
        _cleanup_theme(theme_id)


# ============================================================================
# 케이스 5: 404 + 409 에러 매핑
# ============================================================================


def test_error_mappings_404_and_409(
    db_alive: bool, client: TestClient, seed_assets: list[int]
) -> None:
    """- 없는 theme_id GET → 404
    - 없는 active asset DELETE → 404 (InactiveMember 또는 theme_id 부재)
    - 중복 slug POST → 409
    - 중복 active 멤버 add → 409 (DuplicateActiveMember)
    """
    if not db_alive:
        pytest.skip("DB unavailable — BLOCKER-001 잔재")

    user = _unique_user()
    a1, _ = seed_assets

    # 1) 없는 theme_id GET → 404
    r404a = client.get("/api/themes/99999999")
    assert r404a.status_code == 404

    # 2) 명시적 slug 로 테마 생성 → 같은 (user_id, slug) 로 두 번째 POST → 409
    explicit_slug = _unique_slug()
    r1 = client.post(
        "/api/themes",
        json={"name": "slug중복1", "slug": explicit_slug, "user_id": user},
    )
    assert r1.status_code == 201
    theme_id = r1.json()["theme_id"]
    try:
        r2 = client.post(
            "/api/themes",
            json={"name": "slug중복2", "slug": explicit_slug, "user_id": user},
        )
        assert r2.status_code == 409, r2.text

        # 3) 자산 추가 후 같은 자산 다시 add → 409 (DuplicateActiveMember).
        ar = client.post(f"/api/themes/{theme_id}/assets", json={"asset_id": a1})
        assert ar.status_code == 201
        ar_dup = client.post(f"/api/themes/{theme_id}/assets", json={"asset_id": a1})
        assert ar_dup.status_code == 409, ar_dup.text

        # 4) 없는 active asset DELETE → 404 (InactiveMember). 일단 remove 한 다음 또 remove.
        rr = client.delete(f"/api/themes/{theme_id}/assets/{a1}")
        assert rr.status_code == 204
        rr2 = client.delete(f"/api/themes/{theme_id}/assets/{a1}")
        assert rr2.status_code == 404, rr2.text

        # 5) 없는 theme_id 에서 asset 제거 → 404
        rr3 = client.delete(f"/api/themes/99999999/assets/{a1}")
        assert rr3.status_code == 404
    finally:
        _cleanup_theme(theme_id)
