"""e2e 페르소나 harness — 비개발자 첫 사용 시나리오 (TASK-202).

가정: systemctl --user is-active quant-lab-backend.service / quant-lab-frontend.service
== active. 서버 미가동 시 fixture 가 SOFT skip.

검증 흐름 (사용자 첫 접속 → 백테스트 1회 실행):
  step1. /assets 페이지 한국어 키워드 (UI/UX 원칙 2)
  step2. /api/assets 시드 카탈로그 (SPY, KODEX 200 (069500), BTC-USD, ETH-USD)
  step3. /api/strategies 가 allocator 3 + filter 2 + JSON Schema 노출
  step4. POST /api/backtests with asset_id 정수 키 weights → 422 없음
  step5. run_id 폴링 → terminal status 도달
  step6. /backtests/new 가 새 위젯들의 한국어 키워드 노출 (UI/UX 원칙 1)
"""

from __future__ import annotations

import os
import time

import pytest
import requests

BACKEND = os.environ.get("E2E_BACKEND_URL", "http://127.0.0.1:8001")
FRONTEND = os.environ.get("E2E_FRONTEND_URL", "http://127.0.0.1:3001")


@pytest.fixture(scope="session")
def backend_alive() -> None:
    try:
        r = requests.get(f"{BACKEND}/api/health", timeout=2)
    except Exception as e:
        pytest.skip(f"backend not reachable at {BACKEND}: {e}")
    if r.status_code != 200:
        pytest.skip(f"backend health != 200 ({r.status_code})")


@pytest.fixture(scope="session")
def frontend_alive() -> None:
    try:
        r = requests.get(f"{FRONTEND}/", timeout=2)
    except Exception as e:
        pytest.skip(f"frontend not reachable at {FRONTEND}: {e}")
    if r.status_code != 200:
        pytest.skip(f"frontend / != 200 ({r.status_code})")


def _lookup_asset(symbol: str, market: str | None = None) -> dict:
    """카탈로그에서 정확 일치하는 1건 반환. 없으면 AssertionError."""
    params: dict[str, str | int] = {"q": symbol, "limit": 20}
    if market:
        params["market"] = market
    r = requests.get(f"{BACKEND}/api/assets", params=params, timeout=5)
    assert r.status_code == 200, f"asset lookup failed: {r.status_code}"
    items = r.json()["items"]
    matches = [a for a in items if a["symbol"] == symbol]
    assert (
        matches
    ), f"symbol not found in catalog: {symbol} (got {[a['symbol'] for a in items]})"
    return matches[0]


# --- step1 ---------------------------------------------------------------


def test_step1_assets_page_renders(frontend_alive: None) -> None:
    """비개발자 사용자가 /assets 페이지에 접속 — 한국어 안내 키워드 노출."""
    r = requests.get(f"{FRONTEND}/assets", timeout=5)
    assert r.status_code == 200, f"/assets status: {r.status_code}"
    body = r.text
    for keyword in ("자산 카탈로그", "심볼 또는 한글명 검색", "자산 추가"):
        assert keyword in body, f"missing keyword on /assets: {keyword!r}"


# --- step2 ---------------------------------------------------------------


def test_step2_assets_api_lists_seed_catalog(backend_alive: None) -> None:
    """시드 자산 (SPY / 069500 KODEX 200 / BTC-USD / ETH-USD) 가 모두 노출."""
    r = requests.get(f"{BACKEND}/api/assets", params={"limit": 200}, timeout=5)
    assert r.status_code == 200
    items = r.json()["items"]
    symbols = {a["symbol"] for a in items}
    for required in ("SPY", "069500", "BTC-USD", "ETH-USD"):
        assert (
            required in symbols
        ), f"seed missing: {required} (have {sorted(symbols)[:20]}...)"


# --- step3 ---------------------------------------------------------------


def test_step3_strategies_api_exposes_allocator3_filter2(backend_alive: None) -> None:
    """MVP 프리셋: allocator 3 + filter 2 = 5 모두 노출 + JSON Schema 포함.

    Quant Lab CLAUDE.md L26 (MVP 3종 + 시그널 필터 2종).
    """
    r = requests.get(f"{BACKEND}/api/strategies", timeout=5)
    assert r.status_code == 200
    data = r.json()
    allocator_names = {a["name"] for a in data["allocators"]}
    filter_names = {f["name"] for f in data["filters"]}
    assert allocator_names == {
        "fixed_weight",
        "all_weather",
        "equal_weight",
    }, f"allocator set drift: {allocator_names}"
    assert filter_names == {
        "moving_average",
        "momentum",
    }, f"filter set drift: {filter_names}"

    # JSON Schema 포함 — frontend 가 폼 자동 생성에 사용
    for desc in data["allocators"] + data["filters"]:
        schema = desc["params_schema"]
        assert isinstance(schema, dict), f"params_schema not dict for {desc['name']}"
        assert (
            "properties" in schema or "type" in schema
        ), f"params_schema missing properties/type: {desc['name']}"


# --- step4 ---------------------------------------------------------------


def test_step4_backtest_create_with_asset_id_keys(backend_alive: None) -> None:
    """AssetWeightMap 위젯이 생성한 정수 asset_id 키 → backend 422 없음 (정상 경로)."""
    spy = _lookup_asset("SPY", market="US")
    btc = _lookup_asset("BTC-USD", market="CRYPTO")

    payload = {
        "name": None,
        "strategy": {
            "allocator_name": "fixed_weight",
            # asset_id 정수를 str() 로 직렬화 (JSON object 키 제약)
            "allocator_params": {
                "weights": {
                    str(spy["asset_id"]): 0.6,
                    str(btc["asset_id"]): 0.4,
                }
            },
            "filter_configs": [],
            "rebalance_schedule": "monthly",
        },
        "universe_asset_ids": [spy["asset_id"], btc["asset_id"]],
        "period_start": "2022-01-01",
        "period_end": "2024-12-31",
        "base_currency": "KRW",
        "initial_cash": {"KRW": 10_000_000},
    }
    r = requests.post(f"{BACKEND}/api/backtests", json=payload, timeout=10)
    assert r.status_code in (
        200,
        201,
    ), f"backtest create failed: {r.status_code} {r.text[:300]}"
    run = r.json()
    assert "run_id" in run, f"response missing run_id: {run}"
    assert run["status"] in (
        "pending",
        "running",
        "done",
    ), f"unexpected initial status: {run['status']}"


# --- step5 ---------------------------------------------------------------


def test_step5_backtest_status_pollable(backend_alive: None) -> None:
    """run_id 가 GET /api/backtests/{run_id} 로 폴링 가능 + terminal status 도달."""
    spy = _lookup_asset("SPY")

    payload = {
        "name": None,
        "strategy": {
            "allocator_name": "equal_weight",
            "allocator_params": {},
            "filter_configs": [],
            "rebalance_schedule": "monthly",
        },
        "universe_asset_ids": [spy["asset_id"]],
        "period_start": "2022-01-01",
        "period_end": "2024-12-31",
        "base_currency": "KRW",
        "initial_cash": {"KRW": 10_000_000},
    }
    r = requests.post(f"{BACKEND}/api/backtests", json=payload, timeout=10)
    assert r.status_code in (200, 201)
    run_id = r.json()["run_id"]

    terminal = {"done", "failed", "cancelled"}
    last_status = None
    for _ in range(30):  # 최대 ~15s 대기
        time.sleep(0.5)
        s = requests.get(f"{BACKEND}/api/backtests/{run_id}", timeout=5)
        assert s.status_code == 200, f"status poll failed: {s.status_code}"
        last_status = s.json()["status"]
        if last_status in terminal:
            break
    assert last_status in terminal, f"never reached terminal status: {last_status}"


# --- step6 ---------------------------------------------------------------


def test_step6_frontend_backtests_new_renders_widgets(frontend_alive: None) -> None:
    """/backtests/new 페이지가 새 위젯들의 한국어 키워드 노출 (UI/UX 원칙 1).

    JSON-string 우회 흔적이 사라지고 AssetWeightMap / FilterConfigBuilder 가 대체.
    """
    r = requests.get(f"{FRONTEND}/backtests/new", timeout=5)
    assert r.status_code == 200, f"/backtests/new status: {r.status_code}"
    body = r.text
    for keyword in (
        "새 백테스트",
        "전략 선택",
        "자산 선택",
        "기축통화",
        "필터 추가",
        "필터 없음",
    ):
        assert keyword in body, f"missing keyword on /backtests/new: {keyword!r}"
