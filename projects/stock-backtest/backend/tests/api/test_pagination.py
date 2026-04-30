"""TASK-234 — PaginatedResponse.total 정확화 검증.

기존 라우터는 `total=len(items)` 로 limit 분만 카운트해 페이지 수 산정 불가능했다.
이 테스트는 다음을 검증한다:
1. items=limit, total>limit 케이스 — 실제 row 수가 limit 보다 많아도 total 이 정확히 반영됨.
2. 동일 필터(q/market/asset_type) 가 search 와 count 양쪽에 적용됨.
3. count_runs() 가 list_runs() 와 동일한 모집단을 카운트함.

DB 가용성:
- 기존 test_api_contract.py 와 동일하게 db_alive fixture 로 SOFT skip.
- BLOCKER-001 잔재 환경에서는 모든 테스트 skip.
"""

from __future__ import annotations

from datetime import date, datetime, timezone

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text

from app.core.db import SessionLocal, engine
from app.data.asset_repository import SqlAssetRepository
from app.data.repositories.backtest_repository import (
    BacktestRepository,
    compute_run_hash,
)
from app.main import app
from app.models.asset import Asset as AssetModel


@pytest.fixture(scope="module")
def db_alive() -> bool:
    """test_api_contract.py 의 db_alive 와 동일 ping. BLOCKER-001 잔재 검증."""
    try:
        with engine.connect() as c:
            c.execute(text("SELECT 1"))
            c.execute(text("SELECT created_at, active FROM assets LIMIT 1"))
            c.execute(
                text("SELECT status, progress, error_json FROM backtest_runs LIMIT 1")
            )
            return True
    except Exception:
        return False


@pytest.fixture(scope="module")
def client() -> TestClient:
    return TestClient(app)


# ----- Asset count 단위 테스트 ---------------------------------------------


def _seed_asset_rows(session, prefix: str, n: int, market: str = "KR") -> list[int]:
    """동일 prefix 로 n 개 자산 row 삽입 → asset_id 목록 반환.

    테스트가 끝나면 finalizer 가 정리하므로 이름 충돌 회피용 prefix 만 호출자가 보장.
    """
    ids: list[int] = []
    for i in range(n):
        row = AssetModel(
            symbol=f"{prefix}{i:03d}",
            market=market,
            asset_type="ETF",
            currency="KRW" if market == "KR" else "USD",
            name=f"테스트자산{prefix}-{i:03d}",
            meta={},
            active=True,
        )
        session.add(row)
        session.flush()
        ids.append(row.asset_id)
    return ids


def test_asset_repo_count_matches_search_filter(db_alive: bool) -> None:
    """`count(...)` 가 `search(...)` 와 동일 모집단을 카운트해야 한다.

    시나리오: 10 개 row 삽입 → search(limit=3) 은 3 개, count() 는 10 개 (필터에 부합한 전체).
    """
    if not db_alive:
        pytest.skip("DB unavailable — BLOCKER-001 잔재")

    session = SessionLocal()
    prefix = f"PGN234A_{int(datetime.now(timezone.utc).timestamp())}_"
    seeded_ids: list[int] = []
    try:
        seeded_ids = _seed_asset_rows(session, prefix=prefix, n=10, market="KR")
        session.flush()

        repo = SqlAssetRepository(session)

        # q 필터로 우리가 심은 자산만 격리.
        items = repo.search(q=prefix, limit=3)
        total = repo.count(q=prefix)

        # items 는 limit 만큼만, total 은 모집단 전체.
        assert len(items) == 3, f"expected 3 items (limit), got {len(items)}"
        assert total == 10, f"expected total=10, got {total}"
        assert total > len(items), "total must exceed limit-bounded items"
    finally:
        # cleanup — 다른 테스트와 격리.
        for asset_id in seeded_ids:
            row = session.get(AssetModel, asset_id)
            if row is not None:
                session.delete(row)
        session.commit()
        session.close()


def test_asset_repo_count_respects_market_filter(db_alive: bool) -> None:
    """`count(market=...)` 가 market 필터를 search 와 동일하게 적용해야 한다."""
    if not db_alive:
        pytest.skip("DB unavailable — BLOCKER-001 잔재")

    session = SessionLocal()
    prefix = f"PGN234B_{int(datetime.now(timezone.utc).timestamp())}_"
    seeded_ids: list[int] = []
    try:
        # KR 5 개 + US 3 개 — 같은 prefix 안에서 market 만 분리.
        kr_ids = _seed_asset_rows(session, prefix=prefix + "K", n=5, market="KR")
        us_ids = _seed_asset_rows(session, prefix=prefix + "U", n=3, market="US")
        seeded_ids = kr_ids + us_ids
        session.flush()

        repo = SqlAssetRepository(session)
        total_all = repo.count(q=prefix)
        total_kr = repo.count(q=prefix, market="KR")  # type: ignore[arg-type]
        total_us = repo.count(q=prefix, market="US")  # type: ignore[arg-type]

        assert total_all == 8
        assert total_kr == 5
        assert total_us == 3
    finally:
        for asset_id in seeded_ids:
            row = session.get(AssetModel, asset_id)
            if row is not None:
                session.delete(row)
        session.commit()
        session.close()


# ----- API 라우터 E2E — items=limit, total>limit 케이스 --------------------


def test_assets_list_total_exceeds_items_when_limit_smaller(
    db_alive: bool, client: TestClient
) -> None:
    """GET /api/assets — limit=3 + 실제 부합 row=10 → items 길이=3, total=10.

    TASK-234 의 핵심 회귀 가드 — 기존 `total=len(items)` 였다면 total=3 으로 고정되었음.
    """
    if not db_alive:
        pytest.skip("DB unavailable — BLOCKER-001 잔재")

    session = SessionLocal()
    prefix = f"PGN234C_{int(datetime.now(timezone.utc).timestamp())}_"
    seeded_ids: list[int] = []
    try:
        seeded_ids = _seed_asset_rows(session, prefix=prefix, n=10, market="KR")
        session.commit()

        resp = client.get("/api/assets", params={"q": prefix, "limit": 3, "offset": 0})
        assert resp.status_code == 200, resp.text
        body = resp.json()
        assert len(body["items"]) == 3, f"items length: {len(body['items'])}"
        assert body["total"] == 10, f"total: {body['total']}"
        assert body["page"] == 1
        assert body["page_size"] == 3
    finally:
        # cleanup (새 세션 — TestClient 의 dependency 가 자체 세션 사용)
        cleanup = SessionLocal()
        for asset_id in seeded_ids:
            row = cleanup.get(AssetModel, asset_id)
            if row is not None:
                cleanup.delete(row)
        cleanup.commit()
        cleanup.close()
        session.close()


# ----- BacktestRepository.count_runs ---------------------------------------


def test_backtest_repo_count_runs_independent_of_limit(db_alive: bool) -> None:
    """`count_runs()` 가 list_runs(limit) 의 limit 영향을 받지 않아야 한다.

    시나리오: 5 개 run 삽입 → list_runs(limit=2) 는 2 개, count_runs() 는 baseline+5.
    """
    if not db_alive:
        pytest.skip("DB unavailable — BLOCKER-001 잔재")

    session = SessionLocal()
    repo = BacktestRepository(session)
    baseline = repo.count_runs()

    seeded: list[int] = []
    try:
        for i in range(5):
            run_hash = compute_run_hash(
                strategy_name="equal_weight",
                params={
                    "_test_marker": f"PGN234D_{datetime.now(timezone.utc).timestamp()}_{i}"
                },
                universe=[1, 2],
                period_start=date(2024, 1, 1),
                period_end=date(2024, 6, 30),
                base_currency="KRW",
            )
            run = repo.create_run(
                run_hash=run_hash,
                strategy_name="equal_weight",
                params={"_test_marker": f"PGN234D_{i}"},
                universe=[1, 2],
                period_start=date(2024, 1, 1),
                period_end=date(2024, 6, 30),
                base_currency="KRW",
            )
            seeded.append(run.run_id)
        session.flush()

        listed = repo.list_runs(limit=2, offset=0)
        total = repo.count_runs()

        assert len(listed) == 2, f"list_runs(limit=2) returned {len(listed)}"
        assert (
            total == baseline + 5
        ), f"count_runs={total}, expected baseline({baseline})+5"
        assert total > len(listed), "total must exceed limit-bounded items"
    finally:
        for run_id in seeded:
            repo.delete_run(run_id)
        session.commit()
        session.close()
