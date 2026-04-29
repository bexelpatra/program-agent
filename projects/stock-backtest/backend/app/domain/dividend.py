"""배당 처리.

V3 CLAUDE.md L21: "배당은 현금으로 수령하여 다음 리밸런싱에 편입"
V3 § 배당 처리 L640-642: corporate_actions 기록 + cash_by_ccy 입금

도메인 순수: corporate_actions DB 기록은 호출자 (data 레이어) 책임. 여기서는 배당 이벤트 →
포트폴리오 입금 로직만 담당.
"""

from dataclasses import dataclass
from datetime import date
from decimal import Decimal

from app.domain.portfolio import Portfolio


@dataclass(frozen=True)
class DividendPayment:
    """배당 1회. native currency 기준."""

    asset_id: int
    pay_date: date
    amount_per_share: Decimal  # 1주당 배당금 (native currency)


@dataclass(frozen=True)
class DividendCredit:
    """포트폴리오에 입금된 배당 결과 (감사용)."""

    asset_id: int
    pay_date: date
    qty_eligible: int  # 배당 기준일 보유 주식수
    amount_per_share: Decimal
    total_amount: Decimal  # native currency
    currency: str


def apply_dividend(portfolio: Portfolio, payment: DividendPayment) -> DividendCredit | None:
    """payment.pay_date 시점의 portfolio 보유분에 배당 입금.

    보유 0 이거나 amount 0 이면 None 반환 (이벤트 무시).

    호출 시점: engine 의 매일 EOD 시점 또는 배당락일 처리.
    corporate_actions 데이터에서 호출자가 lookup.
    """
    pos = portfolio.positions.get(payment.asset_id)
    if pos is None or pos.qty <= 0 or payment.amount_per_share <= Decimal("0"):
        return None

    total = Decimal(pos.qty) * payment.amount_per_share
    portfolio.deposit(pos.currency, total)

    return DividendCredit(
        asset_id=payment.asset_id,
        pay_date=payment.pay_date,
        qty_eligible=pos.qty,
        amount_per_share=payment.amount_per_share,
        total_amount=total,
        currency=pos.currency,
    )


def apply_dividends_for_date(
    portfolio: Portfolio,
    payments: list[DividendPayment],
    target_date: date,
) -> list[DividendCredit]:
    """target_date 에 해당하는 모든 배당 일괄 처리.

    engine 의 매일 EOD 후크에서 호출.
    """
    credits: list[DividendCredit] = []
    for p in payments:
        if p.pay_date == target_date:
            credit = apply_dividend(portfolio, p)
            if credit:
                credits.append(credit)
    return credits
