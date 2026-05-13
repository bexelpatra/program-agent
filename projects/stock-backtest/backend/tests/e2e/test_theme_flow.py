"""e2e 테마 플로우 스모크 (TASK-310).

1 시나리오, 7 단계로 Phase 2.1 의 backend 전 영역을 통합 검증한다:

  step1. 테마 생성 → 201, ThemeRead 필드 확인
  step2. 자산 2개 추가 → 201, ThemeAssetRead 필드 확인
  step3. 차트 조회 (equal weighting) → 200, members 2 시리즈 + aggregate
  step4. 자산 1개 제거 → 204
  step5. history 자동 append 확인 → ADDED + REMOVED 2 이벤트
  step6. 비교 (테마 2개) → 200, themes dict 에 2 키
  step7. 테마 삭제 → 204

DB 가용성:
    test_themes.py / test_themes_chart.py 와 동일 패턴 — `db_alive` fixture 가
    실패하면 모든 단계 SOFT skip. BLOCKER-001 잔재 환경 + alembic 0005 미적용 모두
    안전 SKIP.

격리:
    - 각 시나리오마다 고유 user_id + 임시 자산 prefix 사용.
    - 모든 themes / theme_assets / asset_theme_history / ohlcv / assets row 는
      finalizer 에서 직접 SQL 정리.
"""

from __future__ import annotations

import math
import uuid
from datetime import date, datetime, time, timedelta, timezone
from decimal import Decimal

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text

from app.core.db import SessionLocal, engine
from app.main import app
from app.models.asset import Asset as AssetModel
from app.models.ohlcv import Ohlcv as OhlcvModel


# ============================================================================
# Fixtures
# ============================================================================


@pytest.fixture(scope="module")
def db_alive() -> bool:
    """alembic 0005 적용 + 핵심 테이블 가용성 ping."""
    try:
        with engine.connect() as c:
            c.execute(text("SELECT 1"))
            c.execute(text("SELECT theme_id FROM themes LIMIT 1"))
            c.execute(text("SELECT asset_id FROM assets LIMIT 1"))
            c.execute(text("SELECT asset_id FROM ohlcv LIMIT 1"))
            return True
    except Exception:
        return False


@pytest.fixture(scope="module")
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture()
def db_session():
    s = SessionLocal()
    try:
        yield s
    finally:
        s.close()


# ============================================================================
# Helpers (test_themes_chart.py 패턴 재사용)
# ============================================================================


def _unique_user() -> str:
    return f"u-{uuid.uuid4().hex[:8]}"


def _make_prefix() -> str:
    return (
        f"E2E310_{int(datetime.now(timezone.utc).timestamp())}_{uuid.uuid4().hex[:6]}"
    )


def _seed_assets(db_session, count: int, prefix: str) -> list[int]:
    ids: list[int] = []
    for i in range(count):
        a = AssetModel(
            symbol=f"{prefix}_A{i}",
            market="KR",
            asset_type="ETF",
            currency="KRW",
            name=f"e2e테마-{prefix}-A{i}",
            meta={},
            active=True,
        )
        db_session.add(a)
        db_session.flush()
        ids.append(a.asset_id)
    db_session.commit()
    return ids


def _make_trending_prices(
    n_days: int, start_price: float, annual_growth: float
) -> list[float]:
    daily = (1.0 + annual_growth) ** (1.0 / 252.0)
    return [start_price * (daily**i) for i in range(n_days)]


def _seed_ohlcv(
    db_session, asset_id: int, start_date: date, prices: list[float]
) -> None:
    for i, p in enumerate(prices):
        d = start_date + timedelta(days=i)
        ts = datetime.combine(d, time(0, 0, tzinfo=timezone.utc))
        db_session.add(
            OhlcvModel(
                asset_id=asset_id,
                time=ts,
                open=Decimal(f"{p:.6f}"),
                high=Decimal(f"{p:.6f}"),
                low=Decimal(f"{p:.6f}"),
                close=Decimal(f"{p:.6f}"),
                adj_close=Decimal(f"{p:.6f}"),
                volume=Decimal("1000"),
            )
        )
    db_session.execute(
        text(
            "UPDATE assets SET start_date = :sd, last_ingested_at = :li "
            "WHERE asset_id = :aid"
        ),
        {
            "sd": start_date,
            "li": datetime.combine(
                start_date + timedelta(days=len(prices) - 1),
                time(23, 59),
                tzinfo=timezone.utc,
            ),
            "aid": asset_id,
        },
    )
    db_session.commit()


def _cleanup(theme_ids: list[int], asset_ids: list[int]) -> None:
    s = SessionLocal()
    try:
        for tid in theme_ids:
            s.execute(
                text("DELETE FROM asset_theme_history WHERE theme_id = :t"),
                {"t": tid},
            )
            s.execute(text("DELETE FROM theme_assets WHERE theme_id = :t"), {"t": tid})
            s.execute(text("DELETE FROM themes WHERE theme_id = :t"), {"t": tid})
        for aid in asset_ids:
            s.execute(
                text("DELETE FROM asset_theme_history WHERE asset_id = :a"),
                {"a": aid},
            )
            s.execute(text("DELETE FROM theme_assets WHERE asset_id = :a"), {"a": aid})
            s.execute(text("DELETE FROM ohlcv WHERE asset_id = :a"), {"a": aid})
            s.execute(text("DELETE FROM assets WHERE asset_id = :a"), {"a": aid})
        s.commit()
    finally:
        s.close()


# ============================================================================
# e2e 시나리오 (7 단계 한 테스트 = 트랜잭션·상태 흐름 일관성 검증)
# ============================================================================


def test_theme_flow_end_to_end(db_alive: bool, client: TestClient, db_session) -> None:
    """Phase 2.1 backend e2e — 7 단계가 모두 성공해야 시나리오 통과."""
    if not db_alive:
        pytest.skip("DB unavailable — BLOCKER-001 잔재 또는 alembic 0005 미적용")

    user = _unique_user()
    prefix = _make_prefix()
    a1, a2 = _seed_assets(db_session, 2, prefix)
    asset_ids = [a1, a2]
    theme_ids: list[int] = []

    # OHLCV 30일 결정적 시리즈 (양쪽 동일 시작일).
    base_start = date(2020, 1, 1)
    _seed_ohlcv(db_session, a1, base_start, _make_trending_prices(30, 10000.0, 0.10))
    _seed_ohlcv(db_session, a2, base_start, _make_trending_prices(30, 50000.0, 0.05))

    try:
        # ──────────────── step1. 테마 생성 ────────────────
        r1 = client.post(
            "/api/themes",
            json={
                "name": "정치-AAA",
                "description": "e2e 테마 플로우 검증용",
                "user_id": user,
            },
        )
        assert r1.status_code == 201, f"step1: {r1.status_code} {r1.text}"
        t1_body = r1.json()
        theme_id = t1_body["theme_id"]
        theme_ids.append(theme_id)
        assert t1_body["name"] == "정치-AAA"
        assert t1_body["description"] == "e2e 테마 플로우 검증용"
        assert t1_body["user_id"] == user
        assert t1_body["slug"]  # 자동 생성

        # ──────────────── step2. 자산 2개 추가 ────────────────
        r2a = client.post(
            f"/api/themes/{theme_id}/assets",
            json={"asset_id": a1, "note": "첫 멤버"},
        )
        assert r2a.status_code == 201, f"step2a: {r2a.status_code} {r2a.text}"
        m1 = r2a.json()
        assert m1["theme_id"] == theme_id and m1["asset_id"] == a1
        assert m1["note"] == "첫 멤버"
        assert m1["removed_at"] is None

        r2b = client.post(f"/api/themes/{theme_id}/assets", json={"asset_id": a2})
        assert r2b.status_code == 201, f"step2b: {r2b.status_code} {r2b.text}"
        m2 = r2b.json()
        assert m2["theme_id"] == theme_id and m2["asset_id"] == a2
        assert m2["removed_at"] is None

        # detail 에서 active_members 가 2 이어야 함
        d = client.get(f"/api/themes/{theme_id}")
        assert d.status_code == 200
        assert d.json()["member_count"] == 2

        # ──────────────── step3. 차트 조회 ────────────────
        cr = client.get(
            f"/api/themes/{theme_id}/chart",
            params={"weighting": "equal"},
        )
        assert cr.status_code == 200, f"step3: {cr.status_code} {cr.text}"
        chart = cr.json()
        members = chart["members"]
        assert str(a1) in members and str(a2) in members, (
            f"step3 members 키 불일치: {list(members)}"
        )
        s1, s2 = members[str(a1)], members[str(a2)]
        assert len(s1) >= 1 and len(s2) >= 1
        # rebase=100 — 첫 값이 100 (소수 정밀도 ±1e-3)
        assert math.isclose(float(s1[0]["value"]), 100.0, abs_tol=1e-3)
        assert math.isclose(float(s2[0]["value"]), 100.0, abs_tol=1e-3)
        # aggregate — 2개 자산 equal weight 첫 값 ≈ 100
        agg = chart["aggregate"]
        assert len(agg) >= 1
        assert math.isclose(float(agg[0]["value"]), 100.0, abs_tol=1e-3)
        # universe_meta 핵심 필드
        meta = chart["universe_meta"]
        assert "adjusted_start" in meta and "adjusted_end" in meta
        assert meta["reason"] in (
            "universe_start_later",
            "universe_end_earlier",
            "no_data",
            "ok",
        )

        # ──────────────── step4. 자산 1개 제거 ────────────────
        rr = client.delete(f"/api/themes/{theme_id}/assets/{a1}")
        assert rr.status_code == 204, f"step4: {rr.status_code} {rr.text}"

        # detail 에서 활성 멤버 1
        d2 = client.get(f"/api/themes/{theme_id}")
        assert d2.status_code == 200
        d2j = d2.json()
        assert d2j["member_count"] == 1
        active_ids = {m["asset_id"] for m in d2j["active_members"]}
        assert active_ids == {a2}

        # ──────────────── step5. history 자동 append ────────────────
        hr = client.get(f"/api/assets/{a1}/theme_history")
        assert hr.status_code == 200, f"step5: {hr.status_code} {hr.text}"
        events = hr.json()
        # 본 테스트가 격리된 자산을 사용하므로 정확히 2건 (ADDED + REMOVED).
        assert len(events) == 2, f"step5 history 건수 != 2: {events}"
        assert [e["event_type"] for e in events] == ["ADDED", "REMOVED"]
        assert all(e["asset_id"] == a1 for e in events)
        assert all(e["theme_id"] == theme_id for e in events)
        assert events[0]["note"] == "첫 멤버"

        # ──────────────── step6. 비교 (2 테마) ────────────────
        # 두 번째 테마 생성 + 자산 추가
        r_t2 = client.post(
            "/api/themes",
            json={"name": "정치-BBB", "user_id": user},
        )
        assert r_t2.status_code == 201
        theme_id_2 = r_t2.json()["theme_id"]
        theme_ids.append(theme_id_2)
        ra = client.post(f"/api/themes/{theme_id_2}/assets", json={"asset_id": a2})
        assert ra.status_code == 201

        cmp_r = client.get(
            "/api/themes/compare",
            params={"theme_ids": f"{theme_id},{theme_id_2}"},
        )
        assert cmp_r.status_code == 200, f"step6: {cmp_r.status_code} {cmp_r.text}"
        cmp_body = cmp_r.json()
        themes_resp = cmp_body["themes"]
        assert str(theme_id) in themes_resp and str(theme_id_2) in themes_resp, (
            f"step6 themes 키 불일치: {list(themes_resp)}"
        )
        assert themes_resp[str(theme_id)]["name"] == "정치-AAA"
        assert themes_resp[str(theme_id_2)]["name"] == "정치-BBB"
        assert len(themes_resp[str(theme_id)]["aggregate"]) >= 1
        assert len(themes_resp[str(theme_id_2)]["aggregate"]) >= 1

        # ──────────────── step7. 테마 삭제 ────────────────
        dr1 = client.delete(f"/api/themes/{theme_id}")
        assert dr1.status_code == 204, f"step7a: {dr1.status_code} {dr1.text}"
        dr2 = client.delete(f"/api/themes/{theme_id_2}")
        assert dr2.status_code == 204, f"step7b: {dr2.status_code} {dr2.text}"

        # soft delete — themes row 는 보존 (alembic 0005 정책), 활성 멤버 0
        g1 = client.get(f"/api/themes/{theme_id}")
        assert g1.status_code == 200
        assert g1.json()["active_members"] == []
        assert g1.json()["member_count"] == 0
    finally:
        _cleanup(theme_ids, asset_ids)
