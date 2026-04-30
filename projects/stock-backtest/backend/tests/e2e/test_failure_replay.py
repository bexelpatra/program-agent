"""Failure replay — 2026-04-29 비개발자 첫 사용 사고 회귀 박제 (TASK-202).

사고 timeline:
  1. 사용자가 /backtests/new 에서 fixed_weight 전략 선택
  2. (당시) StrategyParamsForm 이 dict 파라미터를 JSON-string textarea 로 우회 (TASK-092)
  3. 사용자가 weights 에 ticker symbol 직접 입력 ({"BTC": 0.6, "TLT": 0.4})
  4. backend FixedWeightParams (dict[int, float]) 검증 실패 → 422 ValidationError
  5. raw pydantic 에러 메시지가 화면에 그대로 노출 (UI/UX 원칙 1 위반)

사후 조치 (TASK-200/201):
  - frontend AssetWeightMap 위젯: asset_id 정수 키만 생성 (textarea 제거)
  - frontend FilterConfigBuilder 위젯: filter dict 폼 자동 생성 (textarea 제거)
  - backend backtest_runner._resolve_symbol_keys_to_asset_ids: symbol → asset_id
    자동 매핑 fallback (구버전 frontend 또는 외부 API caller 보호)

회귀 박제 항목:
  - replay_symbol_keys_in_weights_now_resolved: backend fallback 정상 동작
  - replay_unknown_symbol_returns_friendly_error: 미존재 ticker → 친절한 한국어 에러
  - replay_no_json_textarea_in_frontend_build: frontend 빌드물에 JSON 우회 흔적 0
"""

from __future__ import annotations

import os
import subprocess
import time

import pytest
import requests

BACKEND = os.environ.get("E2E_BACKEND_URL", "http://127.0.0.1:8001")

# 이 path 는 build 검증용 (.next/static) — 빌드되지 않은 dev 환경이면 SOFT skip.
FRONTEND_BUILD_DIR = (
    "/home/jai/pa/stock-backtest/projects/stock-backtest/frontend/.next/static"
)


@pytest.fixture(scope="session")
def backend_alive() -> None:
    try:
        r = requests.get(f"{BACKEND}/api/health", timeout=2)
    except Exception as e:
        pytest.skip(f"backend not reachable at {BACKEND}: {e}")
    if r.status_code != 200:
        pytest.skip(f"backend health != 200 ({r.status_code})")


def _lookup_asset(symbol: str) -> dict:
    r = requests.get(
        f"{BACKEND}/api/assets", params={"q": symbol, "limit": 20}, timeout=5
    )
    assert r.status_code == 200
    items = r.json()["items"]
    matches = [a for a in items if a["symbol"] == symbol]
    assert matches, f"symbol not found: {symbol}"
    return matches[0]


# --- replay 1: backend symbol→id fallback --------------------------------


def test_replay_symbol_keys_in_weights_now_resolved(backend_alive: None) -> None:
    """사고 재현: weights 에 ticker symbol (asset_id 아님) 직접 입력.

    TASK-201 의 backend fallback (_resolve_symbol_keys_to_asset_ids) 가 자동 매핑.
    이 테스트가 실패하면 fallback 이 깨진 것 → 비개발자 사용자가 다시 422 를 보게 됨.
    """
    spy = _lookup_asset("SPY")
    btc = _lookup_asset("BTC-USD")

    payload = {
        "name": None,
        "strategy": {
            "allocator_name": "fixed_weight",
            # 사고 재현: 정수 asset_id 가 아닌 symbol 을 키로 (구버전 UI / 외부 caller)
            "allocator_params": {"weights": {"SPY": 0.6, "BTC-USD": 0.4}},
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
    # 사고 시점: 422 raw pydantic. 해결 후: 200/201 + run_id
    assert r.status_code in (200, 201), (
        "REGRESSION — backend symbol→asset_id fallback 깨짐. "
        f"status={r.status_code} body={r.text[:300]}"
    )
    run = r.json()
    assert "run_id" in run


# --- replay 2: 미존재 ticker → 친절한 한국어 에러 ------------------------


def test_replay_unknown_symbol_returns_friendly_error(backend_alive: None) -> None:
    """카탈로그에 없는 ticker 입력 → raw pydantic 노출 금지, 한국어 안내.

    경로 A: POST 시점에 422 → detail/error.message 에 친절 메시지
    경로 B: POST 200/201 (pending) → background worker 가 build_strategy 단계에서
            ValueError → status=failed + error.message 한국어
    둘 중 하나로 사용자 친화 메시지가 전달되어야 함.
    """
    spy = _lookup_asset("SPY")
    payload = {
        "name": None,
        "strategy": {
            "allocator_name": "fixed_weight",
            "allocator_params": {"weights": {"NONEXISTENT_TICKER_ZZZ": 1.0}},
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

    if r.status_code in (200, 201):
        # 경로 B: pending 등록 후 worker 에서 실패
        run_id = r.json()["run_id"]
        terminal = {"done", "failed", "cancelled"}
        s_json: dict = {}
        for _ in range(30):  # ~15s 대기
            time.sleep(0.5)
            s = requests.get(f"{BACKEND}/api/backtests/{run_id}", timeout=5)
            assert s.status_code == 200
            s_json = s.json()
            if s_json["status"] in terminal:
                break
        assert (
            s_json.get("status") in terminal
        ), f"never reached terminal: {s_json.get('status')}"
        # done 으로 끝나면 fallback 이 어떻게든 매칭한 셈 — 사고 의미 없으므로 통과
        if s_json["status"] == "failed":
            err = s_json.get("error") or {}
            err_text = " ".join(
                str(v) for v in (err.get("message"), err.get("type"), err.get("stage"))
            )
            assert (
                "찾을 수 없" in err_text
                or "NONEXISTENT_TICKER_ZZZ" in err_text
                or "asset" in err_text.lower()
            ), f"unfriendly error payload: {err}"
    elif r.status_code == 422:
        # 경로 A: 즉시 422
        try:
            body = r.json()
        except ValueError:
            pytest.fail(f"422 with non-JSON body: {r.text[:300]}")
        msg = ""
        if isinstance(body, dict):
            err = body.get("error") or {}
            msg = (
                str(err.get("message", "")) or str(body.get("detail", "")) or str(body)
            )
        assert (
            "찾을 수 없" in msg
            or "NONEXISTENT_TICKER_ZZZ" in msg
            or "ticker" in msg.lower()
            or "asset" in msg.lower()
        ), f"unfriendly 422 detail: {msg[:300]}"
    else:
        pytest.fail(f"unexpected status: {r.status_code} {r.text[:200]}")


# --- replay 3: frontend 빌드물에 JSON 우회 흔적 0 ------------------------


def test_replay_no_json_textarea_in_frontend_build() -> None:
    """frontend 빌드 산출물에 raw JSON input 패턴이 없어야 한다 (UI/UX 원칙 1 강제).

    검사 패턴:
      - JSON.parse(...) 로 폼 입력을 파싱하는 흔적 (구버전 StrategyParamsForm)
      - <textarea> 내 JSON / weights 키워드
    빌드 디렉토리(.next/static) 가 없으면 dev 모드 가정으로 SKIP.
    """
    if not os.path.isdir(FRONTEND_BUILD_DIR):
        pytest.skip(f"frontend build dir absent (dev mode?): {FRONTEND_BUILD_DIR}")

    out = subprocess.run(
        [
            "grep",
            "-rE",
            r"JSON\.parse[^;]*params|<textarea[^>]*JSON|textarea[^>]*weights",
            FRONTEND_BUILD_DIR,
        ],
        capture_output=True,
        text=True,
    )
    # grep exit code: 0 = matched (REGRESSION), 1 = no match (정상), 2 = error
    assert out.returncode != 0, (
        "REGRESSION — JSON-string input 패턴이 빌드물에 등장. "
        "StrategyParamsForm 우회 잔재 또는 신규 우회 발생.\n"
        f"hits:\n{out.stdout[:800]}"
    )
    assert (
        out.returncode == 1
    ), f"grep error (exit {out.returncode}): {out.stderr[:300]}"


# --- replay 4: BTC fractional 매수 회귀 (V3 Q8 재결정, 2026-04-29) -----------


def test_replay_btc_fractional_buy_with_small_capital() -> None:
    """BTC $50k @ 초기자본 $10k → 정수 강제 시 0개 매수 (사고 run_id=56 재현).

    V3 Q8 재결정 후: CRYPTO market 은 fractional=True 로 매수 → 0.x BTC 체결 가능.
    이 테스트가 실패하면 fractional 분기가 깨진 것 → 사용자가 다시 평탄선 결과를 보게 됨.

    도메인 직접 호출 (DB / 백엔드 서버 불필요) — backend_alive fixture 미사용.
    """
    from decimal import Decimal

    from app.domain.asset.entity import is_fractional_market
    from app.domain.portfolio import Portfolio

    # 사고 재현: BTC 1코인 = $50k, 초기자본 $10k.
    # 정수 강제 시: int(10000 / 50000) = 0 → 매수 실패 (평탄선).
    # fractional 후: ~ 0.1996 BTC (수수료/슬리피지 차감 후).
    assert is_fractional_market("CRYPTO"), (
        "REGRESSION — CRYPTO 가 fractional 시장 목록에서 빠짐. " "사용자 사고 재발 (모든 코인 백테스트 평탄선)."
    )
    assert not is_fractional_market(
        "US"
    ), "REGRESSION — US 시장이 fractional 로 분류됨. 정수 주 정책 위반."

    p = Portfolio(base_currency="USD")
    p.deposit("USD", Decimal("10000"))
    qty, cost = p.buy(
        asset_id=999,
        currency="USD",
        price=Decimal("50000"),
        qty_target=Decimal("1"),
        commission_bps=Decimal("10"),  # CRYPTO 0.1%
        slippage_bps=Decimal("10"),
        fractional=True,
    )
    # 정수 강제였다면 qty == 0 (사고 재현). fractional 정상이면 0 < qty < 1.
    assert qty > Decimal("0"), (
        "REGRESSION — fractional buy 가 0개 체결. "
        "CRYPTO 정수 강제 회귀 (사용자 첫 시도 사고 run_id=56 재현)."
    )
    assert qty < Decimal("1"), f"비정상 — qty={qty} 가 1 이상. cost_per_unit 계산 이상."
    # 비용은 초기 자본 이내 (음수 잔고 금지).
    assert cost <= Decimal("10000")
    assert p.cash("USD") >= Decimal("0")


# --- replay 5: BTC + MA 필터 fail 시 보유 청산 (TASK-211, run_id=96 재현) -----


def test_replay_btc_ma_filter_fail_clears_position() -> None:
    """run_id=96 재현: BTC 100% + MA(117) + quarterly + USD $100k.

    사고 timeline:
      1. 2017~2026 구간에서 BTC 가격이 MA 위에 있을 때 매수 진입.
      2. 이후 MA 깨짐 (가격 < MA) → 시그널 OFF → apply_filters_and_allocator 가 빈 dict
         반환.
      3. (수정 전 버그) engine.py L219 `if target_weights:` 분기로 execute_rebalance
         호출 자체를 skip → 보유 청산 누락.
      4. (수정 후) 빈 dict 라도 호출 → trade._classify_orders 가 보유 자산 전량 매도.

    이 테스트는 도메인 직접 호출 — yfinance/DB 의존 없이 결정적 가격 시계열로 재현.
    가격 시계열은 매수 진입 + 이후 하락 시나리오를 만족하도록 의도적으로 설계.

    검증:
      - trades 가 2건 이상 (매수 1건 + 청산 1건).
      - filter fail 시점에 SELL 발생.
    """
    from datetime import date
    from decimal import Decimal
    from typing import ClassVar

    import pandas as pd

    from app.domain.calendar import trading_days_in_period
    from app.domain.engine import BacktestRunContext, run_backtest
    from app.domain.filters.moving_average import MovingAverage, MovingAverageParams
    from app.domain.strategy import Strategy

    # 짧은 결정적 구간 (2024 한 해 — 250 거래일 정도). MA(50) 사용해 lookback 단축.
    # MA(117) 의미는 "lookback 충분 후 가격이 MA 위→아래로 전환" 시나리오. 결정적
    # 시계열 재현 목적상 window=50 으로 단축 (회귀 의미는 동일 — filter fail → 청산).
    base_currency = "USD"
    period_start = date(2024, 1, 1)
    period_end = date(2024, 12, 31)
    timeline = trading_days_in_period(base_currency, period_start, period_end)
    assert len(timeline) > 200, "lookback 위 + 아래 양쪽 시나리오 위해 충분한 거래일 필요"

    # 가격 시계열: 전반부는 우상향 (MA 위 → 매수 진입) → 후반부 급락 (MA 아래 → 청산).
    # 결정적 — random 사용 X.
    n = len(timeline)
    crossover = int(n * 0.55)  # 55% 지점에서 급락 시작
    prices_list = []
    for i in range(n):
        if i < crossover:
            # 8000 → 12000 우상향.
            prices_list.append(8000.0 + (i / crossover) * 4000.0)
        else:
            # 12000 → 4000 급락 (MA 아래로 충분히 깨짐).
            frac = (i - crossover) / (n - crossover)
            prices_list.append(12000.0 - frac * 8000.0)

    prices = pd.DataFrame({1: prices_list}, index=timeline)
    prices.index.name = "date"

    class _BtcOnlyAllocator:
        name: ClassVar[str] = "btc_only"

        def required_universe(self) -> list[int]:
            return [1]

        def generate_weights(
            self,
            universe_asset_ids: list[int],
            prices_until_d: pd.DataFrame,
            signal_date: date,
        ) -> dict[int, Decimal]:
            if 1 not in universe_asset_ids:
                return {}
            return {1: Decimal("1.0")}

    # MA(50) 필터 (window 단축으로 결정적 재현 — TASK-211 회귀 본질은 동일).
    ma_filter = MovingAverage(MovingAverageParams(window=50, price_above=True))

    strategy = Strategy(
        name="btc_ma_quarterly",
        allocator=_BtcOnlyAllocator(),
        signal_filters=(ma_filter,),
        rebalance_schedule="quarterly",
    )

    ctx = BacktestRunContext(
        base_currency=base_currency,
        period_start=period_start,
        period_end=period_end,
        initial_cash={"USD": Decimal("100000")},
        universe_market_meta={1: ("CRYPTO", "USD")},
        prices_aligned=prices,
        fx_rates_to_base={d: {"USD": Decimal("1")} for d in timeline},
        strategy=strategy,
    )

    result = run_backtest(ctx)

    buy_fills = [f for f in result.fills if f.side == "BUY"]
    sell_fills = [f for f in result.fills if f.side == "SELL"]

    # 핵심 회귀 (TASK-211): 매수 + 청산 양쪽 발생해야 trades >= 2 건.
    # 수정 전엔 매수 1건만 (filter fail 시 청산 skip) → 이 assertion 이 실패.
    assert len(result.fills) >= 2, (
        f"REGRESSION (TASK-211) — run_id=96 재현. "
        f"매수 + 청산 = trades >= 2 기대. 실제 fills={result.fills}"
    )
    assert len(buy_fills) >= 1, "MA 위 진입 매수가 없음 (시계열 설계 오류)"
    assert len(sell_fills) >= 1, (
        "REGRESSION (TASK-211) — filter fail 후 청산 누락. "
        "engine.py L219 `if target_weights:` 분기 회귀."
    )
