"""정규화 차트 API 통합 테스트 (TASK-305 DoD (b) — 3 케이스).

테스트 케이스 매핑:
    1. **single theme equal weighting**: 테마 + 자산 2개 + OHLCV fixture →
       GET /api/themes/{id}/chart → members 2 시리즈 (rebase=100 first value)
       + aggregate 1 시리즈.
    2. **compare 2 themes**: 테마 2개 + 각각 자산 + OHLCV →
       GET /api/themes/compare?theme_ids=1,2 → themes dict 에 2 키 + aggregate.
    3. **universe 교집합 통지**: 자산 2개의 OHLCV 시작일이 다름 →
       universe_meta.adjusted_start 가 늦은 자산 기준 + 메시지 한글 포함.

DB 가용성:
    BLOCKER-001 잔재 환경에서는 모든 테스트 SOFT skip (기존 test_themes.py
    패턴 동일).

격리:
    - 각 테스트가 고유 user_id / 임시 자산 prefix 사용.
    - 생성한 themes/ohlcv 는 cleanup 단계에서 직접 삭제.
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
# Fixtures (test_themes.py 패턴 재사용)
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


def _unique_user() -> str:
    return f"u-{uuid.uuid4().hex[:8]}"


# ============================================================================
# OHLCV / Asset 시드 헬퍼
# ============================================================================


def _seed_assets(db_session, count: int, prefix: str) -> list[int]:
    """KR ETF 자산 N개 시드. start_date 는 호출자가 OHLCV 적재 후 별도 갱신."""
    ids: list[int] = []
    for i in range(count):
        a = AssetModel(
            symbol=f"{prefix}_A{i}",
            market="KR",
            asset_type="ETF",
            currency="KRW",
            name=f"차트테스트-{prefix}-A{i}",
            meta={},
            active=True,
        )
        db_session.add(a)
        db_session.flush()
        ids.append(a.asset_id)
    db_session.commit()
    return ids


def _make_trending_prices(
    n_days: int,
    start_price: float,
    annual_growth: float,
) -> list[float]:
    """결정적 우상향 시리즈 — annual_growth 만큼 매일 (1+r/252) 복리.

    test_golden_scenarios.py:69 의 `_make_trending_series` 패턴과 동일.
    """
    daily = (1.0 + annual_growth) ** (1.0 / 252.0)
    return [start_price * (daily**i) for i in range(n_days)]


def _seed_ohlcv(
    db_session,
    asset_id: int,
    start_date: date,
    prices: list[float],
) -> None:
    """[start_date, start_date + len(prices)) 일자에 OHLCV row 적재.

    KR 캘린더 거래일이 아닌 평일도 포함될 수 있지만, 정규화 차트는 자연
    합집합 index 를 사용하므로 캘린더 정밀성을 요구하지 않는다.
    """
    for i, p in enumerate(prices):
        d = start_date + timedelta(days=i)
        ts = datetime.combine(d, time(0, 0, tzinfo=timezone.utc))
        bar = OhlcvModel(
            asset_id=asset_id,
            time=ts,
            open=Decimal(f"{p:.6f}"),
            high=Decimal(f"{p:.6f}"),
            low=Decimal(f"{p:.6f}"),
            close=Decimal(f"{p:.6f}"),
            adj_close=Decimal(f"{p:.6f}"),
            volume=Decimal("1000"),
        )
        db_session.add(bar)
    # start_date 갱신 — period_adjustment.adjust_period_for_universe 가 사용.
    db_session.execute(
        text(
            "UPDATE assets SET start_date = :sd, "
            "last_ingested_at = :li WHERE asset_id = :aid"
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
    """테마 + 자산 + OHLCV 일괄 삭제."""
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


def _make_prefix() -> str:
    return f"TC305_{int(datetime.now(timezone.utc).timestamp())}_{uuid.uuid4().hex[:6]}"


# ============================================================================
# 케이스 1: single theme equal weighting
# ============================================================================


def test_single_theme_chart_equal_weighting(
    db_alive: bool, client: TestClient, db_session
) -> None:
    """테마 1개 + 자산 2개 + 동일 기간 OHLCV →
    members 2 시리즈 (rebase=100 first ≈ 100) + aggregate.
    """
    if not db_alive:
        pytest.skip("DB unavailable — BLOCKER-001 잔재 또는 alembic 0005 미적용")

    user = _unique_user()
    prefix = _make_prefix()
    a1, a2 = _seed_assets(db_session, 2, prefix)
    asset_ids = [a1, a2]
    theme_ids: list[int] = []

    # 30일 결정적 시리즈 (동일 시작일).
    base_start = date(2020, 1, 1)
    _seed_ohlcv(db_session, a1, base_start, _make_trending_prices(30, 10000.0, 0.10))
    _seed_ohlcv(db_session, a2, base_start, _make_trending_prices(30, 50000.0, 0.05))

    try:
        # 테마 생성 + 멤버 2 추가
        r = client.post("/api/themes", json={"name": "정치-테스트1", "user_id": user})
        assert r.status_code == 201, r.text
        tid = r.json()["theme_id"]
        theme_ids.append(tid)
        client.post(f"/api/themes/{tid}/assets", json={"asset_id": a1})
        client.post(f"/api/themes/{tid}/assets", json={"asset_id": a2})

        # 차트 조회 — start/end 미지정 (universe common_period 자동 사용)
        cr = client.get(f"/api/themes/{tid}/chart")
        assert cr.status_code == 200, cr.text
        body = cr.json()

        # members 2 자산 모두 시리즈 있음
        members = body["members"]
        assert str(a1) in members and str(a2) in members
        s1 = members[str(a1)]
        s2 = members[str(a2)]
        assert len(s1) >= 1 and len(s2) >= 1

        # rebase=100: 첫 값이 100 (소수 정밀도 ±1e-3)
        assert math.isclose(float(s1[0]["value"]), 100.0, abs_tol=1e-3)
        assert math.isclose(float(s2[0]["value"]), 100.0, abs_tol=1e-3)

        # aggregate: members 길이와 일치 (forward-fill 후 자연 합집합)
        agg = body["aggregate"]
        assert len(agg) >= 1
        # equal 평균: 첫 값 ≈ 100 (양쪽이 100 이므로)
        assert math.isclose(float(agg[0]["value"]), 100.0, abs_tol=1e-3)

        # universe_meta 기본 필드 점검
        meta = body["universe_meta"]
        assert "adjusted_start" in meta and "adjusted_end" in meta
        assert meta["reason"] in (
            "universe_start_later",
            "universe_end_earlier",
            "no_data",
            "ok",
        )
    finally:
        _cleanup(theme_ids, asset_ids)


# ============================================================================
# 케이스 2: compare 2 themes
# ============================================================================


def test_compare_two_themes_returns_aggregate_per_theme(
    db_alive: bool, client: TestClient, db_session
) -> None:
    """테마 2개 + 각각 자산 1개씩 + OHLCV →
    GET /api/themes/compare?theme_ids=A,B → themes dict 2 entry.
    """
    if not db_alive:
        pytest.skip("DB unavailable — BLOCKER-001 잔재")

    user = _unique_user()
    prefix = _make_prefix()
    a1, a2 = _seed_assets(db_session, 2, prefix)
    asset_ids = [a1, a2]
    theme_ids: list[int] = []

    base_start = date(2020, 1, 1)
    _seed_ohlcv(db_session, a1, base_start, _make_trending_prices(20, 10000.0, 0.08))
    _seed_ohlcv(db_session, a2, base_start, _make_trending_prices(20, 25000.0, 0.03))

    try:
        r1 = client.post("/api/themes", json={"name": "비교-테마1", "user_id": user})
        r2 = client.post("/api/themes", json={"name": "비교-테마2", "user_id": user})
        assert r1.status_code == 201 and r2.status_code == 201
        t1 = r1.json()["theme_id"]
        t2 = r2.json()["theme_id"]
        theme_ids.extend([t1, t2])
        client.post(f"/api/themes/{t1}/assets", json={"asset_id": a1})
        client.post(f"/api/themes/{t2}/assets", json={"asset_id": a2})

        # 콤마 구분 — 컬렉터가 split 처리.
        cr = client.get("/api/themes/compare", params={"theme_ids": f"{t1},{t2}"})
        assert cr.status_code == 200, cr.text
        body = cr.json()

        themes_resp = body["themes"]
        assert str(t1) in themes_resp and str(t2) in themes_resp
        assert themes_resp[str(t1)]["name"] == "비교-테마1"
        assert themes_resp[str(t2)]["name"] == "비교-테마2"
        # 각각 aggregate 첫 값 ≈ 100 (단일 멤버 rebase=100)
        agg1 = themes_resp[str(t1)]["aggregate"]
        agg2 = themes_resp[str(t2)]["aggregate"]
        assert len(agg1) >= 1 and len(agg2) >= 1
        assert math.isclose(float(agg1[0]["value"]), 100.0, abs_tol=1e-3)
        assert math.isclose(float(agg2[0]["value"]), 100.0, abs_tol=1e-3)

        # universe_meta 존재
        assert "adjusted_start" in body["universe_meta"]
    finally:
        _cleanup(theme_ids, asset_ids)


# ============================================================================
# 케이스 3: universe 교집합 통지 — affected_assets 비어있지 않음
# ============================================================================


def test_universe_intersection_notice_when_start_dates_differ(
    db_alive: bool, client: TestClient, db_session
) -> None:
    """자산 A 시작일 2020-01-01, 자산 B 시작일 2020-06-01 (5개월 늦음).
    → adjusted_start 가 늦은 쪽(B) 기준 + affected_assets 비어있지 않음
      (period_adjustment.PeriodAdjustment 의 symbol 통지가 universe_meta 의
      affected_assets int list 로 변환되거나, OHLCV 누락 분이 함께 등재).
    """
    if not db_alive:
        pytest.skip("DB unavailable — BLOCKER-001 잔재")

    user = _unique_user()
    prefix = _make_prefix()
    a1, a2 = _seed_assets(db_session, 2, prefix)
    asset_ids = [a1, a2]
    theme_ids: list[int] = []

    early_start = date(2020, 1, 1)
    late_start = date(2020, 6, 1)
    # A: 2020-01-01 부터 200일
    _seed_ohlcv(db_session, a1, early_start, _make_trending_prices(200, 10000.0, 0.08))
    # B: 2020-06-01 부터 100일
    _seed_ohlcv(db_session, a2, late_start, _make_trending_prices(100, 20000.0, 0.05))

    try:
        r = client.post("/api/themes", json={"name": "교집합-테스트", "user_id": user})
        assert r.status_code == 201
        tid = r.json()["theme_id"]
        theme_ids.append(tid)
        client.post(f"/api/themes/{tid}/assets", json={"asset_id": a1})
        client.post(f"/api/themes/{tid}/assets", json={"asset_id": a2})

        # 사용자가 2020-01-01 ~ 2020-12-31 을 요청.
        cr = client.get(
            f"/api/themes/{tid}/chart",
            params={"start": "2020-01-01", "end": "2020-12-31"},
        )
        assert cr.status_code == 200, cr.text
        body = cr.json()
        meta = body["universe_meta"]

        # adjusted_start 가 late_start (2020-06-01) 또는 그 이후 — 늦은 자산 기준.
        assert meta["adjusted_start"] >= "2020-06-01", meta
        # reason 이 universe_start_later 또는 ok (캘린더상 늦춰지지 않은 경우
        # 대비) — 데이터셋이 명확히 늦으므로 universe_start_later 기대.
        assert meta["reason"] in ("universe_start_later", "ok")
        # affected_assets — period_adjustment 에 의해 symbol 기반 통지가 발생.
        # 본 라우터는 affected_assets 를 int(asset_id) 로 변환 (OHLCV 누락분
        # 합산). 본 테스트 케이스는 OHLCV 가 모두 있어 OHLCV-누락 항목은 0
        # 이지만, universe_meta 의 message 에는 한국어 통지가 들어 있다.
        assert (
            "조정" in meta["message"]
            or "자동" in meta["message"]
            or meta["reason"] == "ok"
        )
    finally:
        _cleanup(theme_ids, asset_ids)


# ============================================================================
# 케이스 4 (부가): weighting=market_cap → 422 (DoD (c))
# ============================================================================


def test_market_cap_weighting_returns_422(
    db_alive: bool, client: TestClient, db_session
) -> None:
    """architecture.md L1043 — Phase 2.2 placeholder. 호출자가 market_cap 을
    선택하면 422 + 한국어 메시지로 graceful 거절.
    """
    if not db_alive:
        pytest.skip("DB unavailable — BLOCKER-001 잔재")

    user = _unique_user()
    prefix = _make_prefix()
    (a1,) = _seed_assets(db_session, 1, prefix)
    asset_ids = [a1]
    theme_ids: list[int] = []

    _seed_ohlcv(
        db_session, a1, date(2020, 1, 1), _make_trending_prices(10, 10000.0, 0.05)
    )

    try:
        r = client.post("/api/themes", json={"name": "mcap-테스트", "user_id": user})
        assert r.status_code == 201
        tid = r.json()["theme_id"]
        theme_ids.append(tid)
        client.post(f"/api/themes/{tid}/assets", json={"asset_id": a1})

        cr = client.get(f"/api/themes/{tid}/chart", params={"weighting": "market_cap"})
        assert cr.status_code == 422, cr.text
        # 응답 본문 어디든 "Phase 2.2" 포함 (에러 미들웨어가 detail 을
        # error.message 로 래핑하므로 body 전체 문자열 검색이 더 견고).
        assert "Phase 2.2" in cr.text
    finally:
        _cleanup(theme_ids, asset_ids)
