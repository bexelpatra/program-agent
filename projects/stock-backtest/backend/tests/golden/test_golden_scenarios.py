"""골든 스냅샷 테스트 (TASK-080).

전략 3 × 시나리오 3 = 9 케이스. 각 케이스는 in-memory pandas DataFrame 으로
가격/FX 시리즈를 빌드 → run_backtest() 직접 호출 (DB 우회) → 결과 (final equity,
num_fills, CAGR, MDD) 를 JSON 으로 스냅샷 비교.

데이터 로더 placeholder 우회:
- backtest_runner.py 는 prices_aligned=DataFrame() 으로 엔진을 호출해 ValueError 로
  failed 종료한다 (TASK-100 통합 예정).
- 본 테스트는 도메인 (엔진) 직접 호출이므로 placeholder 영향 없음.

스냅샷 정확도:
- 부동소수 비교는 ±0.01% (rel_tol=1e-4) 까지 허용.
- 첫 실행 시 snapshots/ 디렉토리에 JSON 생성, 이후 실행은 비교.
- snapshot 갱신 필요 시 환경변수 GOLDEN_UPDATE=1 로 덮어쓰기 가능.

시나리오:
1. 단일 통화 KRW universe (KR ETF 2종)
2. 멀티 통화 KRW base + 미국·한국 (KR ETF + SPY)
3. 암호화폐 포함 멀티 마켓 (SPY + BTC, base USD)

전략:
A. FixedWeight 60/40 (universe 의 첫 두 자산을 60/40)
B. AllWeather 표준 (자산을 카테고리에 매핑)
C. EqualWeight (1/N)

base 캘린더는 base_currency 따라 KRW→XKRX, USD→XNYS. exchange_calendars 에서 실거래일
세션을 받아 시계열을 채운다.
"""

from __future__ import annotations

import json
import math
import os
from datetime import date
from decimal import Decimal
from pathlib import Path

import pandas as pd
import pytest

from app.domain.allocators import (
    AllWeather,
    AllWeatherParams,
    EqualWeight,
    EqualWeightParams,
    FixedWeight,
    FixedWeightParams,
)
from app.domain.calendar import trading_days_in_period
from app.domain.engine import BacktestRunContext, run_backtest
from app.domain.metrics import compute_metrics
from app.domain.strategy import Strategy

SNAPSHOT_DIR = Path(__file__).parent / "snapshots"
SNAPSHOT_DIR.mkdir(exist_ok=True)

# 부동소수 비교 허용오차 (±0.01%).
REL_TOL = 1e-4
ABS_TOL = 1e-6


# ============================================================================
# 가격/FX 시리즈 헬퍼
# ============================================================================


def _make_trending_series(
    dates: list[date],
    start_price: float,
    annual_growth: float,
    daily_vol: float = 0.0,
) -> list[float]:
    """우상향 (또는 평탄) 결정적 시계열. vol=0 이면 완전 결정적, 아니면 sin 기반 noise.

    annual_growth 만큼 매일 (1+r/252) 복리 곱셈. 결정적 — 같은 입력은 같은 출력.
    """
    daily_growth = (1.0 + annual_growth) ** (1.0 / 252.0)
    prices: list[float] = []
    for i, _d in enumerate(dates):
        # 결정적 noise: sin(i) 로 ±daily_vol 진동 (random 사용 없이 재현성 확보).
        noise = math.sin(i * 0.1) * daily_vol if daily_vol > 0 else 0.0
        prices.append(start_price * (daily_growth**i) * (1.0 + noise))
    return prices


def _build_prices_aligned(
    dates: list[date],
    asset_specs: dict[
        int, tuple[float, float, float]
    ],  # asset_id → (start, growth, vol)
) -> pd.DataFrame:
    """index=date, columns=asset_id, values=close DataFrame 빌드 (engine 입력 형식)."""
    data = {}
    for aid, (start, growth, vol) in asset_specs.items():
        data[aid] = _make_trending_series(dates, start, growth, vol)
    df = pd.DataFrame(data, index=dates)
    df.index.name = "date"
    return df


def _build_fx_rates(
    dates: list[date],
    pairs: dict[str, tuple[float, float]],  # ccy → (start_rate, end_rate) base_per_ccy
) -> dict[date, dict[str, Decimal]]:
    """date → {ccy → base_per_ccy} 선형 보간 dict. 모든 base 거래일 채움."""
    n = len(dates)
    out: dict[date, dict[str, Decimal]] = {}
    for i, d in enumerate(dates):
        frac = i / max(n - 1, 1)
        out[d] = {
            ccy: Decimal(str(start + (end - start) * frac))
            for ccy, (start, end) in pairs.items()
        }
    return out


# ============================================================================
# 시나리오 빌더
# ============================================================================


def _scenario_1_kr_only() -> dict:
    """단일 통화 KRW universe: KODEX 200 (asset_id=1) + KODEX 채권 (asset_id=2).

    period: 2020-01-01 ~ 2024-12-31 (약 5년, KRW 캘린더 거래일).
    KODEX 200 우상향 (연 8%), 채권 평탄 (연 2%).
    """
    period_start = date(2020, 1, 1)
    period_end = date(2024, 12, 31)
    base_currency = "KRW"
    dates = trading_days_in_period(base_currency, period_start, period_end)
    prices = _build_prices_aligned(
        dates,
        {
            1: (35000.0, 0.08, 0.0),  # KODEX 200 (KRW)
            2: (110000.0, 0.02, 0.0),  # KODEX 국고채 10년
        },
    )
    return {
        "name": "scenario_1_kr_only",
        "base_currency": base_currency,
        "period_start": period_start,
        "period_end": period_end,
        "universe_market_meta": {
            1: ("KR", "KRW"),
            2: ("KR", "KRW"),
        },
        "prices_aligned": prices,
        "fx_rates_to_base": {d: {} for d in dates},  # 모두 KRW
        "initial_cash": {"KRW": Decimal("10000000")},
        "asset_categories": {1: "equity", 2: "long_bond"},
    }


def _scenario_2_kr_us() -> dict:
    """멀티 통화 KRW base + KR/US: KODEX 200 (KR/KRW) + SPY (US/USD).

    forward-fill 정렬은 align_universe_prices 가 책임지지만, 본 테스트는 simplified —
    base 캘린더(XKRX) 거래일에 두 자산 모두 직접 시계열 채운다 (테스트 목적).
    fx: KRW base 의 USD 환율 1300 → 1350.
    """
    period_start = date(2020, 1, 1)
    period_end = date(2024, 12, 31)
    base_currency = "KRW"
    dates = trading_days_in_period(base_currency, period_start, period_end)
    prices = _build_prices_aligned(
        dates,
        {
            1: (35000.0, 0.08, 0.0),  # KODEX 200 (KRW)
            3: (300.0, 0.10, 0.0),  # SPY (USD)
        },
    )
    fx = _build_fx_rates(dates, {"USD": (1300.0, 1350.0)})
    return {
        "name": "scenario_2_kr_us",
        "base_currency": base_currency,
        "period_start": period_start,
        "period_end": period_end,
        "universe_market_meta": {
            1: ("KR", "KRW"),
            3: ("US", "USD"),
        },
        "prices_aligned": prices,
        "fx_rates_to_base": fx,
        "initial_cash": {"KRW": Decimal("10000000")},
        "asset_categories": {1: "equity", 3: "long_bond"},
    }


def _scenario_3_us_crypto() -> dict:
    """SPY (US/USD) + BTC (CRYPTO/USD), base USD. BTC 는 24/7 시장이지만 base 캘린더
    (XNYS) 거래일에만 시계열을 채운다 — base D 일 = UTC 00:00 종가 가정.
    """
    period_start = date(2020, 1, 1)
    period_end = date(2024, 12, 31)
    base_currency = "USD"
    dates = trading_days_in_period(base_currency, period_start, period_end)
    prices = _build_prices_aligned(
        dates,
        {
            3: (300.0, 0.10, 0.0),  # SPY
            4: (8000.0, 0.40, 0.02),  # BTC (변동성 ↑)
        },
    )
    return {
        "name": "scenario_3_us_crypto",
        "base_currency": base_currency,
        "period_start": period_start,
        "period_end": period_end,
        "universe_market_meta": {
            3: ("US", "USD"),
            4: ("CRYPTO", "USD"),
        },
        "prices_aligned": prices,
        "fx_rates_to_base": {d: {} for d in dates},  # 모두 USD
        "initial_cash": {"USD": Decimal("10000")},
        "asset_categories": {3: "equity", 4: "commodity"},
    }


SCENARIOS = {
    "scenario_1_kr_only": _scenario_1_kr_only,
    "scenario_2_kr_us": _scenario_2_kr_us,
    "scenario_3_us_crypto": _scenario_3_us_crypto,
}


# ============================================================================
# 전략 빌더
# ============================================================================


def _build_strategy(strategy_name: str, scenario: dict) -> Strategy:
    """시나리오에 맞춰 3종 전략 인스턴스화.

    FixedWeight: universe 첫 두 자산을 60/40.
    AllWeather: 시나리오의 asset_categories 매핑을 그대로 (카테고리 디폴트 비중 합 ≠ 1
        이라 _validate_weights 에서 5% 허용 한도를 넘으면 적절히 정규화). 본 테스트는
        category_weights 도 시나리오에 맞게 단순화 (equity 60 / long_bond 또는 commodity 40).
    EqualWeight: 1/N (universe 전체).
    """
    asset_ids = list(scenario["universe_market_meta"].keys())
    if strategy_name == "fixed_weight":
        # universe 의 첫 두 자산을 60/40.
        params = FixedWeightParams(weights={asset_ids[0]: 0.6, asset_ids[1]: 0.4})
        return Strategy(
            name="fixed_weight_60_40",
            allocator=FixedWeight(params),
            signal_filters=tuple(),
            rebalance_schedule="monthly",
        )
    if strategy_name == "all_weather":
        # 시나리오에 맞춰 2-카테고리 단순화 (asset_categories 매핑 활용).
        # category_weights 는 자산 분류에 따라 결정 — equity vs (long_bond|commodity).
        cats = scenario["asset_categories"]
        present_cats = set(cats.values())
        # 디폴트 비중 그대로 사용하되, 본 universe 에 없는 카테고리는 가중치 0 으로 만들고
        # equity/{사용된 채권 또는 원자재 카테고리} 만 남긴다 (validation 5% 허용 내).
        if present_cats == {"equity", "long_bond"}:
            cw = {"equity": 0.6, "long_bond": 0.4}
        elif present_cats == {"equity", "commodity"}:
            cw = {"equity": 0.6, "commodity": 0.4}
        else:
            cw = {c: 1.0 / len(present_cats) for c in present_cats}
        params = AllWeatherParams(category_weights=cw, asset_categories=cats)
        return Strategy(
            name="all_weather_simplified",
            allocator=AllWeather(params),
            signal_filters=tuple(),
            rebalance_schedule="monthly",
        )
    if strategy_name == "equal_weight":
        return Strategy(
            name="equal_weight",
            allocator=EqualWeight(EqualWeightParams()),
            signal_filters=tuple(),
            rebalance_schedule="monthly",
        )
    raise ValueError(f"unknown strategy: {strategy_name}")


# ============================================================================
# 백테스트 실행 + 스냅샷 비교
# ============================================================================


def _run_scenario_strategy(scenario: dict, strategy_name: str) -> dict:
    """단일 케이스 실행 → 결과 dict 반환 (스냅샷 비교 단위)."""
    strategy = _build_strategy(strategy_name, scenario)
    ctx = BacktestRunContext(
        base_currency=scenario["base_currency"],
        period_start=scenario["period_start"],
        period_end=scenario["period_end"],
        initial_cash=scenario["initial_cash"],
        universe_market_meta=scenario["universe_market_meta"],
        prices_aligned=scenario["prices_aligned"],
        fx_rates_to_base=scenario["fx_rates_to_base"],
        strategy=strategy,
        progress_callback=None,
        cancel_check=None,
    )
    result = run_backtest(ctx)

    # 메트릭 계산 (compute_metrics 가 받는 (date, Decimal) 리스트로 변환).
    equity_series = [(p.time, Decimal(p.equity)) for p in result.equity_curve]
    metrics = compute_metrics(equity_series)

    # 스냅샷 dict (정밀도는 필요한 자릿수만 — 1e-6 이하 변동은 plain 비교에서 무시).
    final_equity = float(equity_series[-1][1]) if equity_series else 0.0
    return {
        "scenario": scenario["name"],
        "strategy": strategy_name,
        "num_equity_points": len(equity_series),
        "num_fills": len(result.fills),
        "final_equity": round(final_equity, 4),
        "cagr": round(metrics.cagr, 6),
        "mdd": round(metrics.mdd, 6),
        "sharpe": round(metrics.sharpe, 6),
        "win_rate": round(metrics.win_rate, 6),
        "aborted": result.aborted,
    }


def _compare_snapshot(actual: dict, snapshot_path: Path) -> None:
    """스냅샷 비교 — 부재 시 생성, 존재 시 비교 (±0.01%)."""
    update_mode = os.environ.get("GOLDEN_UPDATE") == "1"

    if not snapshot_path.exists() or update_mode:
        snapshot_path.write_text(json.dumps(actual, indent=2, sort_keys=True))
        if not update_mode:
            pytest.skip(f"snapshot created at {snapshot_path.name} — re-run to verify")
        return

    expected = json.loads(snapshot_path.read_text())

    # int/str 필드는 정확 비교, float 는 rel_tol 비교.
    int_or_str_keys = {
        "scenario",
        "strategy",
        "num_equity_points",
        "num_fills",
        "aborted",
    }
    float_keys = {"final_equity", "cagr", "mdd", "sharpe", "win_rate"}

    mismatches: list[str] = []
    for k in int_or_str_keys:
        if actual.get(k) != expected.get(k):
            mismatches.append(f"{k}: actual={actual.get(k)} expected={expected.get(k)}")
    for k in float_keys:
        a = float(actual.get(k, 0))
        e = float(expected.get(k, 0))
        if not math.isclose(a, e, rel_tol=REL_TOL, abs_tol=ABS_TOL):
            mismatches.append(
                f"{k}: actual={a} expected={e} (rel_tol={REL_TOL}, abs_tol={ABS_TOL})"
            )

    if mismatches:
        pytest.fail(
            f"snapshot drift in {snapshot_path.name}:\n  " + "\n  ".join(mismatches)
        )


# ============================================================================
# 파라메트릭 케이스 (3 시나리오 × 3 전략 = 9)
# ============================================================================


@pytest.mark.parametrize(
    "scenario_name",
    list(SCENARIOS.keys()),
)
@pytest.mark.parametrize(
    "strategy_name",
    ["fixed_weight", "all_weather", "equal_weight"],
)
def test_golden_snapshot(scenario_name: str, strategy_name: str) -> None:
    """전략 × 시나리오 매트릭스 — 9 케이스.

    각 케이스는 결정적 가격 시계열로 백테스트 실행 후 스냅샷 비교.
    BLOCKER: data loader placeholder 영향 없음 (도메인 직접 호출).
    """
    scenario = SCENARIOS[scenario_name]()
    actual = _run_scenario_strategy(scenario, strategy_name)
    snapshot_path = SNAPSHOT_DIR / f"{scenario_name}__{strategy_name}.json"
    _compare_snapshot(actual, snapshot_path)


# ============================================================================
# 엣지 케이스 — 엔진 무결성 (스냅샷 없이 invariant 검증)
# ============================================================================


def test_engine_aborts_when_cancel_check_returns_true() -> None:
    """cancel_check 가 True 면 즉시 abort + 부분 결과 반환 (TASK-062)."""
    scenario = _scenario_1_kr_only()
    strategy = _build_strategy("equal_weight", scenario)
    cancel_calls = {"n": 0}

    def cancel_after_3_days() -> bool:
        cancel_calls["n"] += 1
        return cancel_calls["n"] >= 3

    ctx = BacktestRunContext(
        base_currency=scenario["base_currency"],
        period_start=scenario["period_start"],
        period_end=scenario["period_end"],
        initial_cash=scenario["initial_cash"],
        universe_market_meta=scenario["universe_market_meta"],
        prices_aligned=scenario["prices_aligned"],
        fx_rates_to_base=scenario["fx_rates_to_base"],
        strategy=strategy,
        cancel_check=cancel_after_3_days,
    )
    result = run_backtest(ctx)
    assert result.aborted is True
    # 부분 결과 보존 — 최소 1점 이상 (첫 진입 후 abort).
    assert len(result.equity_curve) >= 1


def test_engine_progress_callback_called() -> None:
    """progress_callback 이 매 거래일 1회 호출되며 마지막 값은 1.0 에 도달."""
    scenario = _scenario_1_kr_only()
    strategy = _build_strategy("equal_weight", scenario)
    progress_values: list[float] = []

    ctx = BacktestRunContext(
        base_currency=scenario["base_currency"],
        period_start=scenario["period_start"],
        period_end=scenario["period_end"],
        initial_cash=scenario["initial_cash"],
        universe_market_meta=scenario["universe_market_meta"],
        prices_aligned=scenario["prices_aligned"],
        fx_rates_to_base=scenario["fx_rates_to_base"],
        strategy=strategy,
        progress_callback=lambda p: progress_values.append(p),
    )
    run_backtest(ctx)
    assert len(progress_values) > 0
    assert math.isclose(progress_values[-1], 1.0, abs_tol=1e-9)
    # 단조증가 확인.
    for a, b in zip(progress_values, progress_values[1:]):
        assert b >= a


def test_engine_raises_on_empty_period() -> None:
    """기간이 base 캘린더 거래일을 포함하지 않으면 ValueError."""
    # KRW XKRX 캘린더에서 토요일 → 일요일 (둘 다 비거래일).
    period_start = date(2024, 5, 4)  # 토
    period_end = date(2024, 5, 5)  # 일
    base_currency = "KRW"
    strategy = Strategy(
        name="equal_weight",
        allocator=EqualWeight(EqualWeightParams()),
        signal_filters=tuple(),
        rebalance_schedule="monthly",
    )
    ctx = BacktestRunContext(
        base_currency=base_currency,
        period_start=period_start,
        period_end=period_end,
        initial_cash={"KRW": Decimal("10000000")},
        universe_market_meta={1: ("KR", "KRW")},
        prices_aligned=pd.DataFrame(),
        fx_rates_to_base={},
        strategy=strategy,
    )
    with pytest.raises(ValueError, match="no trading days"):
        run_backtest(ctx)
