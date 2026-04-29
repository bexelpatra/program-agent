"""거래 실행 엔진.

architecture.md V3 § "거래 정책" L604-642 + § "백엔드 모듈 분할" L654-666 근거.

책임:
- 시장별 디폴트 수수료 매핑 (KR 0.015% / US 0.005% / CRYPTO 0.1%, defaults.yaml override 가능)
- 비거래일 방어 — 엔진 레이어 (universe 전수 검증, silent 0 금지)
- 가격 누락 방어 — 엔진 레이어 (universe 자산 중 일부 결측 시 명시적 에러)
- 리밸런싱 1회 트랜잭션: target_weights → SELL 먼저 → BUY (native 우선, 부족 시 base 환전)

분리 원칙 (V3 § L654-666):
- Portfolio (TASK-040): 잔고/매매/환전 메커니즘
- Trade (이 파일): 시장별 매핑 + 리밸런싱 시퀀스 + 엔진 레이어 방어
- Engine (TASK-043): 시간 루프 (다중 리밸런싱 일자에 execute_rebalance 반복 호출)

도메인 순수: SQLAlchemy/HTTP/외부 라이브러리 import 금지.
calendar_guard (exchange_calendars) 는 도메인 정책에 본질적이라 예외 (asset/__init__ 정책 참조).
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Callable, Mapping

from app.domain.asset.calendar_guard import is_trading_day
from app.domain.portfolio import DEFAULT_SLIPPAGE_BPS, Portfolio

ZERO = Decimal("0")
ONE = Decimal("1")
BPS_DIVISOR = Decimal("10000")

# V3 CLAUDE.md L19 + architecture L632-636 디폴트.
# defaults.yaml 또는 호출자 override 우선 적용.
DEFAULT_COMMISSION_BPS: dict[str, Decimal] = {
    "KR": Decimal("1.5"),  # 0.015%
    "US": Decimal("0.5"),  # 0.005%
    "CRYPTO": Decimal("10"),  # 0.1%
}

# Portfolio.DEFAULT_SLIPPAGE_BPS 와 동일 값이지만 trade 레이어 디폴트로 별도 노출.
# 호출자가 trade 레벨에서 override 하기 쉽게 하기 위함 (V3 L635 "사용자 조정 가능").
DEFAULT_SLIPPAGE_BPS_DEFAULT = DEFAULT_SLIPPAGE_BPS


# ===== 예외 (silent 0 금지) =====


class NonTradingDayError(Exception):
    """비거래일 방어 — 엔진 레이어. silent 0 금지 (V3 § L626-630)."""


class MissingPriceError(Exception):
    """universe 자산 중 일부 가격 누락 — silent 0 금지 (V3 § L606)."""


# ===== 값 객체 =====


@dataclass(frozen=True)
class TradeOrder:
    """엔진이 생성하는 매매 의도. Portfolio.buy/sell 호출 직전의 의도 표현."""

    asset_id: int
    market: str  # 수수료 매핑용 (KR/US/CRYPTO)
    currency: str
    side: str  # "BUY" | "SELL"
    qty_target: int  # 정수 주 (V3 § L611). buy 는 partial fill 가능, sell 도 보유분만큼만
    price: Decimal  # 체결가 (어댑터 슬리피지 적용 전, native)


@dataclass(frozen=True)
class TradeFill:
    """실제 체결 결과. trade_id 는 DB 가 부여 (도메인은 미보유)."""

    asset_id: int
    side: str
    qty_filled: int
    price: Decimal  # 슬리피지 적용 후 effective price (native)
    commission: Decimal  # native
    currency: str


# ===== 시장별 수수료 매핑 =====


def commission_bps_for(
    market: str, override: Mapping[str, Decimal] | None = None
) -> Decimal:
    """시장별 수수료 bps. override 가 있으면 우선 (defaults.yaml 경유)."""
    if override and market in override:
        return override[market]
    return DEFAULT_COMMISSION_BPS.get(market, ZERO)


# ===== 엔진 레이어 방어 =====


def assert_all_assets_priced(
    target_assets: list[tuple[int, str]],
    prices: Mapping[int, Decimal],
    rebalance_date: date,
) -> None:
    """universe 전체에 가격이 있는지 검증. 누락 시 MissingPriceError."""
    missing = [
        (asset_id, market)
        for asset_id, market in target_assets
        if prices.get(asset_id) is None
    ]
    if missing:
        truncated = missing[:5]
        suffix = "..." if len(missing) > 5 else ""
        raise MissingPriceError(
            f"missing prices for {len(missing)} assets on {rebalance_date}: "
            f"{truncated}{suffix}"
        )


def assert_trading_day_for_universe(
    target_assets: list[tuple[int, str]],
    rebalance_date: date,
    is_trading_day_fn: Callable[[str, date], bool],
) -> None:
    """rebalance_date 가 universe 모든 시장의 거래일인지.

    base_currency 캘린더 기준으로 이미 정렬되었어야 함 (TASK-042 calendar.py).
    정렬 누락 / 캘린더 mismatch 가 있으면 여기서 catch.
    """
    non_trading = [
        (asset_id, market)
        for asset_id, market in target_assets
        if not is_trading_day_fn(market, rebalance_date)
    ]
    if non_trading:
        truncated = non_trading[:5]
        raise NonTradingDayError(
            f"rebalance_date {rebalance_date} is not a trading day for "
            f"{len(non_trading)} markets: {truncated}"
        )


# ===== 리밸런싱 트랜잭션 =====


def _native_value_from_base(
    target_value_base: Decimal,
    currency: str,
    base_currency: str,
    fx_rates_to_base: Mapping[str, Decimal],
) -> Decimal:
    """base_currency 환산 가치를 native currency 가치로 역산."""
    if currency == base_currency:
        return target_value_base
    rate_base_per_native = fx_rates_to_base.get(currency)
    if rate_base_per_native is None or rate_base_per_native <= ZERO:
        raise ValueError(f"missing or invalid fx_rate for {currency} → {base_currency}")
    return target_value_base / rate_base_per_native


def _classify_orders(
    target_qty: Mapping[int, int],
    portfolio: Portfolio,
    target_weight_keys: set[int],
) -> tuple[list[tuple[int, int]], list[tuple[int, int]]]:
    """현재 보유 vs target_qty 비교 → (sells, buys) 분류.

    target_weights 에 없으나 보유 중인 자산은 전량 매도.
    """
    sells: list[tuple[int, int]] = []
    buys: list[tuple[int, int]] = []
    for asset_id, target in target_qty.items():
        current_pos = portfolio.positions.get(asset_id)
        current = current_pos.qty if current_pos else 0
        diff = target - current
        if diff < 0:
            sells.append((asset_id, -diff))
        elif diff > 0:
            buys.append((asset_id, diff))
    for asset_id, pos in list(portfolio.positions.items()):
        if asset_id not in target_weight_keys and pos.qty > 0:
            sells.append((asset_id, pos.qty))
    return sells, buys


def _execute_sells(
    sells: list[tuple[int, int]],
    portfolio: Portfolio,
    asset_meta: Mapping[int, tuple[str, str]],
    prices: Mapping[int, Decimal],
    commission_override: Mapping[str, Decimal] | None,
    slippage_bps: Decimal,
) -> list[TradeFill]:
    """매도 시퀀스 실행. native cash 입금 후 BUY 단계가 활용 (Q5 B native 우선)."""
    fills: list[TradeFill] = []
    for asset_id, qty in sells:
        market, currency = asset_meta[asset_id]
        price = prices.get(asset_id)
        if price is None:
            # 매도 시 가격 누락 — 평균매수가로 fallback (sell-only 청산 시나리오 방어)
            pos = portfolio.positions.get(asset_id)
            if pos is None:
                continue
            price = pos.avg_price
        commission_bps = commission_bps_for(market, commission_override)
        actual_qty, net_received = portfolio.sell(
            asset_id, price, qty, commission_bps, slippage_bps
        )
        if actual_qty <= 0:
            continue
        # net_received = gross - commission, gross = effective_price * qty
        # commission = gross * (commission_bps / 10000)
        # → commission = net_received * commission_bps / (10000 - commission_bps)
        commission = net_received * commission_bps / (BPS_DIVISOR - commission_bps)
        fills.append(
            TradeFill(asset_id, "SELL", actual_qty, price, commission, currency)
        )
    return fills


def _execute_buys(
    buys: list[tuple[int, int]],
    portfolio: Portfolio,
    asset_meta: Mapping[int, tuple[str, str]],
    prices: Mapping[int, Decimal],
    fx_rates_to_base: Mapping[str, Decimal],
    commission_override: Mapping[str, Decimal] | None,
    slippage_bps: Decimal,
) -> list[TradeFill]:
    """매수 시퀀스 실행. native 우선 (Q5 B), 부족 시 base 경유 환전 (Q3 C)."""
    fills: list[TradeFill] = []
    for asset_id, qty in buys:
        market, currency = asset_meta[asset_id]
        price = prices[asset_id]
        commission_bps = commission_bps_for(market, commission_override)

        # 필요 native 추정 (정확치는 partial fill 후 결정).
        # 매수 cost = effective_price * qty * (1 + commission_bps/10000)
        # effective_price = price * (1 + slippage_bps/10000)
        cost_per_unit = (
            price
            * (ONE + slippage_bps / BPS_DIVISOR)
            * (ONE + commission_bps / BPS_DIVISOR)
        )
        required = cost_per_unit * Decimal(qty)

        # ensure_native_funds: native 부족 시 base 에서 환전 (양방향 비용 발생).
        if currency != portfolio.base_currency:
            rate_base_per_native = fx_rates_to_base.get(currency)
            if rate_base_per_native is None or rate_base_per_native <= ZERO:
                raise ValueError(
                    f"missing or invalid fx_rate for {currency} → "
                    f"{portfolio.base_currency}"
                )
            rate_native_per_base = ONE / rate_base_per_native
            portfolio.ensure_native_funds(
                currency,
                required,
                {portfolio.base_currency: rate_native_per_base},
            )

        actual_qty, total_cost = portfolio.buy(
            asset_id, currency, price, qty, commission_bps, slippage_bps
        )
        if actual_qty <= 0:
            continue
        # total_cost = gross + commission, gross = effective_price * qty
        # commission = gross * (commission_bps / 10000)
        # → commission = total_cost * commission_bps / (10000 + commission_bps)
        commission = total_cost * commission_bps / (BPS_DIVISOR + commission_bps)
        fills.append(
            TradeFill(asset_id, "BUY", actual_qty, price, commission, currency)
        )
    return fills


def execute_rebalance(
    portfolio: Portfolio,
    target_weights: Mapping[int, Decimal],
    asset_meta: Mapping[int, tuple[str, str]],
    prices: Mapping[int, Decimal],
    fx_rates_to_base: Mapping[str, Decimal],
    rebalance_date: date,
    commission_override: Mapping[str, Decimal] | None = None,
    slippage_bps: Decimal = DEFAULT_SLIPPAGE_BPS_DEFAULT,
    is_trading_day_fn: Callable[[str, date], bool] = is_trading_day,
) -> list[TradeFill]:
    """리밸런싱 1회 실행 (V3 § L626-642 + Q3 C + Q5 B).

    Args:
        portfolio: 잔고/포지션 (in-place 수정).
        target_weights: {asset_id → 목표 비중 (0~1)}. 합 ≤ 1 권장 (남으면 base cash).
        asset_meta: {asset_id → (market, currency)}. 수수료 매핑 + 환전 판단.
        prices: {asset_id → native price} (체결 슬리피지 적용 전).
        fx_rates_to_base: {ccy → base_per_ccy}.
        rebalance_date: 이 리밸런싱이 실행되는 일자 (방어 로그용).
        commission_override: 시장별 bps override (defaults.yaml 경유).
        slippage_bps: 슬리피지 (V3 디폴트 0.1%).
        is_trading_day_fn: 캘린더 함수 주입 (테스트용; 디폴트 = calendar_guard).

    Returns:
        체결된 TradeFill 목록 (partial fill 시 qty_filled < target).
    """
    target_assets: list[tuple[int, str]] = [
        (aid, asset_meta[aid][0]) for aid in target_weights.keys()
    ]

    # 1. 엔진 레이어 방어 — silent 0 금지.
    assert_trading_day_for_universe(target_assets, rebalance_date, is_trading_day_fn)
    assert_all_assets_priced(target_assets, prices, rebalance_date)

    # 2. 현재 equity (base_currency).
    equity = portfolio.equity_in_base(prices, fx_rates_to_base)

    # 3. target qty (정수 주, V3 § Q8).
    target_qty: dict[int, int] = {}
    for asset_id, weight in target_weights.items():
        _, currency = asset_meta[asset_id]
        price = prices[asset_id]
        target_value_base = equity * weight
        target_value_native = _native_value_from_base(
            target_value_base, currency, portfolio.base_currency, fx_rates_to_base
        )
        target_qty[asset_id] = int(target_value_native / price)

    # 4. BUY/SELL 분류.
    sells, buys = _classify_orders(target_qty, portfolio, set(target_weights.keys()))

    # 5. SELL 먼저 (Q3 C 단계 분리 — native 입금 후 BUY 가 활용).
    sell_fills = _execute_sells(
        sells, portfolio, asset_meta, prices, commission_override, slippage_bps
    )

    # 6+7. BUY (native 우선 Q5 B, 부족 시 base 환전).
    buy_fills = _execute_buys(
        buys,
        portfolio,
        asset_meta,
        prices,
        fx_rates_to_base,
        commission_override,
        slippage_bps,
    )

    return sell_fills + buy_fills
