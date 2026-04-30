"""Portfolio: 통화별 현금 잔고 + 자산 보유 + 환전 엔진.

architecture.md V3 § "현금/FX 모델" (L559-600) 의 B 모델 구현체.

핵심 도메인 결정:
- B 모델: 자산은 native currency 로만 보유, 현금은 cash_by_ccy 로 통화별 분리
- 환전 정책 (Q3 C + Q5 B): 매도 → native 입금 → 같은 native 매수면 직접 활용 →
  부족 시 base_currency 경유 환전 (양방향 비용)
- FX 거래는 trade 미기록 (잔고 이동 + spread 차감만, FxConversion 은 감사용 별도 객체)
- fx_spread_bps = 20bp 디폴트 (한국 증권사 환전 우대 평균)
- long-only, 음수 잔고 금지
- 매매 단위: V3 Q8 재결정 (2026-04-29) — 코인 한정 fractional.
  주식/ETF/지수/채권/원자재(KR/US): 1주 단위 정수.
  암호화폐(CRYPTO): 소수점 8자리 (Decimal). buy/sell 의 fractional 플래그로 분기.
- 매수 cash 부족 시 가능한 만큼만 체결 (partial fill, 호출자가 비중 미달 결과로 받음)

타입 통일 — Position.qty 는 Decimal:
- 정수 자산도 Decimal(int) 로 표현 (Decimal("5") 등). float 누적 오차 회피.
- fractional 자산은 Decimal("0.19994000") 등 8자리.
- 호출자가 int 를 넘겨도 내부에서 Decimal 로 정규화.

도메인 순수: SQLAlchemy/HTTP/외부 라이브러리 import 금지 — Decimal/datetime/dataclass 만 사용.
정밀도는 ohlcv 가격 컬럼 Numeric(20,8) 과 정합 위해 Decimal 사용 (float 누적 오차 회피).
"""

from dataclasses import dataclass, field
from decimal import Decimal, ROUND_DOWN
from typing import Mapping

from app.domain.asset.entity import FRACTIONAL_PRECISION

ZERO = Decimal("0")
ONE = Decimal("1")
DEFAULT_FX_SPREAD_BPS = Decimal("20")  # 0.20%
DEFAULT_SLIPPAGE_BPS = Decimal("10")  # 0.10% (V3 CLAUDE.md 거래 정책 디폴트)
BPS_DIVISOR = Decimal("10000")

# fractional 자산의 Decimal quantize 단위 (10^-8). FRACTIONAL_PRECISION 과 일관.
_FRACTIONAL_QUANTUM = Decimal(1).scaleb(-FRACTIONAL_PRECISION)


@dataclass(frozen=True)
class Position:
    """자산 보유 1단위 — asset_id 별 (qty, avg_price) 만 갖는 불변값.

    qty 는 Decimal — 정수 자산은 Decimal(int), CRYPTO 는 8자리 소수.
    avg_price 는 native currency 기준 평균 매수가 (slippage·commission 포함된 effective_price).
    """

    asset_id: int
    currency: str
    qty: Decimal
    avg_price: Decimal

    def market_value(self, current_price: Decimal) -> Decimal:
        return self.qty * current_price


@dataclass(frozen=True)
class FxConversion:
    """환전 1회 감사용 레코드. backtest_trades 에는 기록되지 않음 (V3 § L569-572)."""

    from_ccy: str
    to_ccy: str
    from_amount: Decimal
    to_amount: Decimal  # spread 차감 후 net
    fx_rate: Decimal  # to_per_from
    spread_cost: Decimal  # base_currency 기준 손실 (감사 용도)


class InsufficientFundsError(Exception):
    """잔고 부족 — 호출자(trade engine)가 partial fill / 0 fill 결정.

    convert() 처럼 정확한 출금이 필요한 경로에서만 raise. buy/sell 은 자동 partial fill.
    """

    def __init__(self, currency: str, requested: Decimal, available: Decimal):
        self.currency = currency
        self.requested = requested
        self.available = available
        super().__init__(
            f"insufficient {currency}: requested {requested}, available {available}"
        )


@dataclass
class Portfolio:
    """통화별 현금 잔고 + 자산 포지션. base_currency 는 환전 hub (Q3 C 단계 분리)."""

    base_currency: str
    cash_by_ccy: dict[str, Decimal] = field(default_factory=dict)
    positions: dict[int, Position] = field(default_factory=dict)
    fx_spread_bps: Decimal = DEFAULT_FX_SPREAD_BPS

    # ===== 잔고 조회 =====

    def cash(self, currency: str) -> Decimal:
        return self.cash_by_ccy.get(currency, ZERO)

    def total_cash_in_base(self, fx_rates: Mapping[str, Decimal]) -> Decimal:
        """모든 통화 cash 를 base_currency 로 환산해 합산.

        fx_rates: {ccy → base_per_ccy} (예: base=KRW, USD 잔고면 fx_rates["USD"]=1300).
        """
        total = ZERO
        for ccy, amount in self.cash_by_ccy.items():
            if ccy == self.base_currency:
                total += amount
            else:
                rate = fx_rates.get(ccy)
                if rate is None:
                    raise ValueError(
                        f"missing fx_rate for {ccy} → {self.base_currency}"
                    )
                total += amount * rate
        return total

    def positions_value_in_base(
        self,
        prices: Mapping[int, Decimal],
        fx_rates: Mapping[str, Decimal],
    ) -> Decimal:
        """모든 포지션 시가 평가액을 base_currency 로 합산.

        prices: {asset_id → native price}, fx_rates: {ccy → base_per_ccy}.
        """
        total = ZERO
        for asset_id, pos in self.positions.items():
            price = prices.get(asset_id)
            if price is None:
                raise ValueError(f"missing price for asset_id={asset_id}")
            native_value = pos.market_value(price)
            if pos.currency == self.base_currency:
                total += native_value
            else:
                rate = fx_rates.get(pos.currency)
                if rate is None:
                    raise ValueError(f"missing fx_rate for {pos.currency}")
                total += native_value * rate
        return total

    def equity_in_base(
        self,
        prices: Mapping[int, Decimal],
        fx_rates: Mapping[str, Decimal],
    ) -> Decimal:
        return self.total_cash_in_base(fx_rates) + self.positions_value_in_base(
            prices, fx_rates
        )

    # ===== 환전 (Q3 C + Q5 B) =====

    def convert(
        self,
        from_ccy: str,
        to_ccy: str,
        amount: Decimal,
        fx_rate: Decimal,
    ) -> FxConversion:
        """from_ccy → to_ccy 단방향 환전. spread 1회 차감 (왕복은 호출자가 두 번 호출).

        fx_rate: to_per_from (예: KRW→USD 시 1/1300 ≈ 0.000769).
        amount > cash(from_ccy) 면 InsufficientFundsError.
        """
        if from_ccy == to_ccy:
            return FxConversion(from_ccy, to_ccy, amount, amount, ONE, ZERO)
        if amount <= ZERO:
            raise ValueError(f"convert amount must be positive, got {amount}")
        if self.cash(from_ccy) < amount:
            raise InsufficientFundsError(from_ccy, amount, self.cash(from_ccy))

        gross_to = amount * fx_rate
        spread = gross_to * (self.fx_spread_bps / BPS_DIVISOR)
        net_to = gross_to - spread

        self.cash_by_ccy[from_ccy] = self.cash(from_ccy) - amount
        self.cash_by_ccy[to_ccy] = self.cash(to_ccy) + net_to

        spread_in_base = self._spread_in_base(spread, from_ccy, to_ccy, fx_rate)
        return FxConversion(from_ccy, to_ccy, amount, net_to, fx_rate, spread_in_base)

    def _spread_in_base(
        self,
        spread_in_to_ccy: Decimal,
        from_ccy: str,
        to_ccy: str,
        fx_rate: Decimal,
    ) -> Decimal:
        """spread (to_ccy 단위 손실) 를 base_currency 로 환산."""
        if to_ccy == self.base_currency:
            return spread_in_to_ccy
        if from_ccy == self.base_currency:
            # to_ccy 단위 spread → base 단위 = spread / fx_rate
            return spread_in_to_ccy / fx_rate
        # base 가 끼지 않은 직접 환전 (MVP 외 케이스 — 보고만 ZERO)
        return ZERO

    def ensure_native_funds(
        self,
        target_ccy: str,
        required: Decimal,
        fx_rates_to_target: Mapping[str, Decimal],
    ) -> list[FxConversion]:
        """target_ccy 잔고가 required 미만이면 base_currency 경유로 환전.

        Q3 C 정책: 매도→native 잔고 입금 후 같은 native 매수가 있으면 native 직접 활용 (Q5 B
        — 환전 0회). 부족하면 base_currency 에서 환전 (양방향 비용 — 매도 시 base→native 도
        호출자가 별도 호출).

        fx_rates_to_target: {ccy → target_per_ccy}. 예: target=USD 면
        fx_rates_to_target["KRW"] = 1/1300.

        반환: 발생한 FxConversion 목록 (감사용). native 충분 시 빈 리스트.
        """
        if self.cash(target_ccy) >= required:
            return []  # Q5 B — native 우선

        if target_ccy == self.base_currency:
            # base 자체 부족은 환전으로 못 메움 (호출자가 partial fill 결정)
            return []

        deficit = required - self.cash(target_ccy)
        rate_base_to_target = fx_rates_to_target.get(self.base_currency)
        if rate_base_to_target is None:
            raise ValueError(
                f"missing fx_rate {self.base_currency} → {target_ccy}"
            )

        # spread 차감 후 정확히 deficit 가 채워지도록 역산:
        # net_to = gross_to * (1 - spread_factor) → gross_to = deficit / (1 - spread_factor)
        spread_factor = self.fx_spread_bps / BPS_DIVISOR
        gross_to = deficit / (ONE - spread_factor)
        from_amount = gross_to / rate_base_to_target

        if self.cash(self.base_currency) < from_amount:
            # base 도 부족 → 가능한 만큼만 환전 (호출자가 partial fill 결정)
            from_amount = self.cash(self.base_currency)

        if from_amount <= ZERO:
            return []

        conv = self.convert(
            self.base_currency, target_ccy, from_amount, rate_base_to_target
        )
        return [conv]

    # ===== 자산 매매 (long-only, partial fill, fractional 분기) =====

    def buy(
        self,
        asset_id: int,
        currency: str,
        price: Decimal,
        qty_target: int | Decimal,
        commission_bps: Decimal,
        slippage_bps: Decimal = DEFAULT_SLIPPAGE_BPS,
        fractional: bool = False,
    ) -> tuple[Decimal, Decimal]:
        """매수 실행 — slippage 적용 가격 + 수수료 + cash 차감 + position 갱신.

        cash 부족 시 가능한 max qty 만 체결 (partial fill).
        fractional=False (디폴트): 1주 단위 정수 (KR/US 주식·ETF·지수·채권·원자재).
        fractional=True: 소수점 8자리 (CRYPTO). V3 Q8 재결정 (2026-04-29) 근거.

        Args:
            qty_target: 목표 수량. int 또는 Decimal 허용 — 내부에서 Decimal 정규화.
            fractional: True 면 Decimal 8자리 정밀도 매수 (코인 전용).

        Returns:
            (실제 체결 qty: Decimal, 총 비용 native: Decimal).
            정수 자산도 Decimal(int) 로 반환 (호환).
        """
        target = qty_target if isinstance(qty_target, Decimal) else Decimal(qty_target)
        if target <= ZERO:
            return (ZERO, ZERO)

        effective_price = price * (ONE + slippage_bps / BPS_DIVISOR)
        cost_per_unit = effective_price * (ONE + commission_bps / BPS_DIVISOR)

        available = self.cash(currency)
        if cost_per_unit <= ZERO:
            return (ZERO, ZERO)

        if fractional:
            # 소수점 8자리, 항상 내림 (cash 초과 방지).
            max_affordable = (available / cost_per_unit).quantize(
                _FRACTIONAL_QUANTUM, rounding=ROUND_DOWN
            )
            target_quant = target.quantize(_FRACTIONAL_QUANTUM, rounding=ROUND_DOWN)
            actual_qty = min(target_quant, max_affordable)
        else:
            # 정수 주 — Decimal(int(...)) 로 통일 (Position.qty 타입 일관).
            max_affordable = Decimal(int(available / cost_per_unit))
            target_int = Decimal(int(target))
            actual_qty = min(target_int, max_affordable)

        if actual_qty <= ZERO:
            return (ZERO, ZERO)

        gross = effective_price * actual_qty
        commission = gross * (commission_bps / BPS_DIVISOR)
        total_cost = gross + commission

        self.cash_by_ccy[currency] = available - total_cost
        self._upsert_position(asset_id, currency, actual_qty, effective_price)

        return (actual_qty, total_cost)

    def _upsert_position(
        self,
        asset_id: int,
        currency: str,
        added_qty: Decimal,
        added_price: Decimal,
    ) -> None:
        """평균 매수가 가중평균 갱신. 신규면 생성, 기존이면 누적 평균."""
        existing = self.positions.get(asset_id)
        if existing is None:
            self.positions[asset_id] = Position(
                asset_id, currency, added_qty, added_price
            )
            return

        new_qty = existing.qty + added_qty
        new_avg = (
            existing.avg_price * existing.qty + added_price * added_qty
        ) / new_qty
        self.positions[asset_id] = Position(asset_id, currency, new_qty, new_avg)

    def sell(
        self,
        asset_id: int,
        price: Decimal,
        qty: int | Decimal,
        commission_bps: Decimal,
        slippage_bps: Decimal = DEFAULT_SLIPPAGE_BPS,
        fractional: bool = False,
    ) -> tuple[Decimal, Decimal]:
        """매도 실행 — slippage 매도가 ↓ + 수수료 + position 차감 + cash 입금.

        보유 미만 매도는 가능한 max qty 만 (음수 잔고 방지, long-only).
        fractional 분기는 buy 와 동일 정책 — CRYPTO 만 소수점 8자리, 그 외는 정수.

        Returns:
            (실제 체결 qty: Decimal, 총 입금액 native: Decimal).
        """
        pos = self.positions.get(asset_id)
        qty_dec = qty if isinstance(qty, Decimal) else Decimal(qty)
        if pos is None or pos.qty <= ZERO or qty_dec <= ZERO:
            return (ZERO, ZERO)

        if fractional:
            requested = qty_dec.quantize(_FRACTIONAL_QUANTUM, rounding=ROUND_DOWN)
        else:
            requested = Decimal(int(qty_dec))

        actual_qty = min(requested, pos.qty)
        if actual_qty <= ZERO:
            return (ZERO, ZERO)

        effective_price = price * (ONE - slippage_bps / BPS_DIVISOR)

        gross = effective_price * actual_qty
        commission = gross * (commission_bps / BPS_DIVISOR)
        net_received = gross - commission

        self.cash_by_ccy[pos.currency] = self.cash(pos.currency) + net_received

        new_qty = pos.qty - actual_qty
        if new_qty <= ZERO:
            del self.positions[asset_id]
        else:
            self.positions[asset_id] = Position(
                pos.asset_id, pos.currency, new_qty, pos.avg_price
            )

        return (actual_qty, net_received)

    def deposit(self, currency: str, amount: Decimal) -> None:
        """초기 자본 / 배당 입금. 음수·0 무시."""
        if amount <= ZERO:
            return
        self.cash_by_ccy[currency] = self.cash(currency) + amount
