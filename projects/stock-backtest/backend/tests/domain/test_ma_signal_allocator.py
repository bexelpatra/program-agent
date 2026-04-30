"""MaSignal allocator 단위 테스트 (TASK-219).

검증 케이스 4종 (task-board ④):
    (a) 모든 자산 MA 위 → 입력 비중 그대로 normalize
    (b) 모든 자산 MA 아래 → 빈 dict (cash-only)
    (c) 일부 위/아래 → 위인 것만 normalize (합이 다시 1.0 으로 재정규화)
    (d) 자산 단위 fallback — 한 자산은 window 충분, 다른 자산은 부족 → 충분한
        자산만 평가됨 (BTC=130일, ETH=50일, window=120)

clean architecture: pandas/Decimal/pytest 만 의존, DB 미접근.
"""

from __future__ import annotations

from datetime import date
from decimal import Decimal

import pandas as pd
import pytest

from app.domain.allocators.ma_signal import MaSignal, MaSignalParams


# 테스트 fixture 헬퍼.
BTC_ID = 1
ETH_ID = 2
SIGNAL_DATE = date(2026, 4, 30)


def _build_prices(
    series_by_asset: dict[int, list[float]],
    end_date: date = SIGNAL_DATE,
) -> pd.DataFrame:
    """asset_id → close 시퀀스 → DataFrame (index=date, columns=asset_id).

    각 시퀀스의 길이만큼 end_date 에서 거꾸로 거래일 (단순 daily) 생성.
    NaN 정렬을 위해 outer join 형태로 만들어진다.
    """
    frames = []
    for aid, prices in series_by_asset.items():
        n = len(prices)
        idx = pd.date_range(end=end_date, periods=n, freq="D")
        frames.append(pd.DataFrame({aid: prices}, index=idx))
    if not frames:
        return pd.DataFrame()
    df = pd.concat(frames, axis=1).sort_index()
    return df


def test_all_assets_above_ma_returns_input_weights() -> None:
    """case (a): 모든 자산이 MA 위 → 입력 비중 그대로 정규화 (이미 합 1.0)."""

    # BTC, ETH 모두 단조 증가 시퀀스 (마지막 가격 > SMA).
    btc_prices = [100.0 + i for i in range(150)]  # 100 → 249
    eth_prices = [50.0 + i for i in range(150)]  # 50  → 199
    prices = _build_prices({BTC_ID: btc_prices, ETH_ID: eth_prices})

    params = MaSignalParams(window=120, assets={BTC_ID: 0.6, ETH_ID: 0.4})
    allocator = MaSignal(params)

    weights = allocator.generate_weights([BTC_ID, ETH_ID], prices, SIGNAL_DATE)

    assert set(weights.keys()) == {BTC_ID, ETH_ID}
    # normalize_weights 는 합이 ±1bp 안이면 그대로 반환 (base.py L109).
    assert weights[BTC_ID] == Decimal("0.6")
    assert weights[ETH_ID] == Decimal("0.4")


def test_all_assets_below_ma_returns_empty_dict() -> None:
    """case (b): 모든 자산이 MA 아래 → 빈 dict (cash-only)."""

    # 단조 감소 시퀀스 → 마지막 가격이 SMA 아래.
    btc_prices = [300.0 - i for i in range(150)]  # 300 → 151
    eth_prices = [200.0 - i for i in range(150)]  # 200 → 51
    prices = _build_prices({BTC_ID: btc_prices, ETH_ID: eth_prices})

    params = MaSignalParams(window=120, assets={BTC_ID: 0.6, ETH_ID: 0.4})
    allocator = MaSignal(params)

    weights = allocator.generate_weights([BTC_ID, ETH_ID], prices, SIGNAL_DATE)

    assert weights == {}


def test_partial_above_below_normalizes_remaining() -> None:
    """case (c): BTC MA 위 / ETH MA 아래 → BTC 만 살아남고 합 1.0 으로 재정규화.

    입력 비중 BTC 0.6 / ETH 0.4 → BTC 살아남으면 0.6 → normalize 거쳐 1.0.
    """

    btc_prices = [100.0 + i for i in range(150)]  # 위
    eth_prices = [200.0 - i for i in range(150)]  # 아래
    prices = _build_prices({BTC_ID: btc_prices, ETH_ID: eth_prices})

    params = MaSignalParams(window=120, assets={BTC_ID: 0.6, ETH_ID: 0.4})
    allocator = MaSignal(params)

    weights = allocator.generate_weights([BTC_ID, ETH_ID], prices, SIGNAL_DATE)

    assert set(weights.keys()) == {BTC_ID}
    # 0.6 / 0.6 = 1.0 (normalize_weights 가 합으로 나눔).
    assert weights[BTC_ID] == Decimal("1")


def test_per_asset_fallback_skips_short_history() -> None:
    """case (d): BTC 130일 / ETH 50일 / window=120 → BTC 만 평가 (ETH skip).

    ETH 는 데이터 부족으로 skip → cash 처리 → 결과 dict 에서 제외.
    BTC 는 window 충분 + MA 위 → 비중 0.5 살아남고 normalize 후 1.0.
    """

    # BTC 130일치 단조 증가 (마지막 > SMA).
    btc_prices = [100.0 + i for i in range(130)]
    # ETH 50일치만 (window=120 미달).
    eth_prices = [50.0 + i for i in range(50)]
    prices = _build_prices({BTC_ID: btc_prices, ETH_ID: eth_prices})

    params = MaSignalParams(window=120, assets={BTC_ID: 0.5, ETH_ID: 0.5})
    allocator = MaSignal(params)

    weights = allocator.generate_weights([BTC_ID, ETH_ID], prices, SIGNAL_DATE)

    assert set(weights.keys()) == {BTC_ID}
    # ETH skip 되어 BTC 0.5 단독 → 0.5 / 0.5 = 1.0.
    assert weights[BTC_ID] == Decimal("1")


# Params 검증 회귀 (FixedWeightParams 와 동일 정책 박제).
def test_params_reject_empty_assets() -> None:
    with pytest.raises(ValueError, match="must not be empty"):
        MaSignalParams(window=120, assets={})


def test_params_reject_negative_weight() -> None:
    with pytest.raises(ValueError, match="non-negative"):
        MaSignalParams(window=120, assets={BTC_ID: -0.1, ETH_ID: 1.1})


def test_params_reject_weights_far_from_one() -> None:
    with pytest.raises(ValueError, match="close to 1.0"):
        MaSignalParams(window=120, assets={BTC_ID: 0.5})  # total=0.5


def test_params_default_window() -> None:
    """window 디폴트 120 (task-board ① ge=2/le=500/default=120)."""

    params = MaSignalParams(assets={BTC_ID: 1.0})
    assert params.window == 120
