"""Tax plugin 인터페이스.

V3 § "세금 모듈" L646-657 + Q9:
- MVP: NoTaxPlugin 빈 구현 (디폴트 OFF)
- 추후 (Phase 3+): 한국 거주자 세금 (해외 양도세 22% / 배당 15.4% / 한국 상장 해외 ETF 등) plugin 추가 가능
- 엔진 (engine.py) 은 plugin 호출 시점/방법만 정의

도메인 순수 — Decimal/dataclass/Protocol 만.
"""

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Protocol, runtime_checkable


@dataclass(frozen=True)
class RealizedTrade:
    """매도로 실현된 손익 1건. tax plugin 입력."""

    asset_id: int
    sold_at: date
    qty: int
    proceeds: Decimal           # 매도 대금 (native currency, 수수료 차감 후)
    cost_basis: Decimal         # 매수 평균가 × qty (native)
    realized_pnl: Decimal       # proceeds - cost_basis
    currency: str               # native currency
    fx_rate_at_sale: Decimal | None = None    # 매도일 fx_rate (base_per_native), 환산용. None 이면 native 그대로


@dataclass(frozen=True)
class DividendIncome:
    """배당 소득 1건. tax plugin 입력."""

    asset_id: int
    paid_at: date
    amount: Decimal             # 배당금 (native currency)
    currency: str
    fx_rate_at_pay: Decimal | None = None


@dataclass(frozen=True)
class TaxResult:
    """plugin 이 산출한 연도별 세금 합."""

    year: int
    tax_amount: Decimal         # base_currency 기준 (plugin 이 환산 후 반환)
    breakdown: dict[str, Decimal]   # 항목별 ("capital_gains", "dividend_tax" 등 plugin 정의)
    note: str | None = None     # 사용자 안내 (한국어 가능)


@runtime_checkable
class TaxPlugin(Protocol):
    """세금 계산 plugin. 연 1회 호출 (회계연도 종료 시점).

    구현체 예 (Phase 3+):
    - NoTaxPlugin (MVP, 세금 0)
    - KoreanResidentTaxPlugin (해외 양도세 22% / 배당 15.4% / 한국 상장 해외 ETF kr_tax_class)
    - USResidentTaxPlugin (장단기 분리, AMT 등)
    """

    name: str

    def calculate(
        self,
        realized_trades: list[RealizedTrade],
        dividends: list[DividendIncome],
        year: int,
        base_currency: str,
    ) -> TaxResult:
        """1년치 실현 거래 + 배당 → 세금 산출. base_currency 로 환산해 반환."""


class NoTaxPlugin:
    """MVP 디폴트. 세금 0. UI 토글 OFF 시 사용."""

    name = "no_tax"

    def calculate(
        self,
        realized_trades: list[RealizedTrade],
        dividends: list[DividendIncome],
        year: int,
        base_currency: str,
    ) -> TaxResult:
        return TaxResult(
            year=year,
            tax_amount=Decimal("0"),
            breakdown={},
            note=None,
        )


def apply_tax_to_portfolio(
    plugin: TaxPlugin,
    realized_trades: list[RealizedTrade],
    dividends: list[DividendIncome],
    year: int,
    base_currency: str,
) -> TaxResult:
    """plugin 호출 헬퍼. engine.py 가 회계연도 종료 시점에 호출 → tax_amount 만큼
    base_currency 잔고에서 차감 (호출자가 portfolio.cash_by_ccy[base] -= tax_amount).

    헬퍼 분리 이유: 향후 plugin 검증/로깅을 한 곳에서 추가 가능.
    """
    return plugin.calculate(realized_trades, dividends, year, base_currency)
