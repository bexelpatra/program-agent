"""Seed script for the initial asset universe.

Populates :mod:`assets` (master table) with KR / US / global ETF / bond /
commodity / crypto tickers used as the default backtest universe.

Source notes:

- **KR tickers (pykrx)**: Korean ETFs are identified by 6-digit KRX codes.
  A few codes below (notably ``305080 TIGER 미국채10년선물``) could not be
  cross-verified from public sources at authoring time; see inline
  ``# TODO`` markers. Validate with ``pykrx.stock.get_etf_ticker_list``
  before relying on them in production.
- **US tickers (yfinance)**: Standard Yahoo Finance symbols. Indices use
  ``^GSPC`` / ``^NDX`` / ``^DJI`` / ``^RUT``.
- **FX**: This script intentionally does **not** register FX pairs.
  FX series live in the ``fx_rates`` table (see architecture decision #2)
  and are fed by a separate ingestion path. If a future decision is made
  to pipe FX through the normal ``assets`` ingestion for convenience, add
  an ``FX`` market to the model's check constraint first.

Tax classification (``meta.kr_tax_class``) follows architecture decision #14
(한국 거주자 세금 모듈):

- ``kr_equity_etf``:  국내 주식형 ETF — 매매차익 비과세
- ``kr_bond_etf``:    국내 채권형 ETF — 배당소득세 15.4%
- ``kr_mixed_etf``:   국내 혼합/파생/원자재 ETF — 배당소득세 15.4%
- ``kr_overseas_etf``: 국내 상장 해외 ETF — 배당소득세 15.4%
- ``overseas_etf``:   해외 상장 ETF/주식 — 양도세 22% (연 250만원 공제)
- ``crypto``:         암호화폐 — 양도세 22% (유예 여부 설정에 따라 on/off)

지수(EQUITY_INDEX)는 투자 상품이 아니므로 ``kr_tax_class`` 태그를 넣지
않는다.

Usage
-----
    python projects/stock-backtest/scripts/seed_universe.py            # DB 실제 삽입
    python projects/stock-backtest/scripts/seed_universe.py --dry-run  # 카운트만 출력
"""
from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, Optional

# Allow running as a standalone script: ensure the package src/ is importable.
_HERE = Path(__file__).resolve().parent
_SRC = _HERE.parent / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from sqlalchemy.orm import Session  # noqa: E402

from stock_backtest.data.db import get_session  # noqa: E402
from stock_backtest.data.models import Asset  # noqa: E402
from stock_backtest.data.repository import AssetRepository  # noqa: E402


# ---------------------------------------------------------------------------
# Row definition
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class AssetRow:
    """A single asset to be registered.

    ``kr_tax_class`` is persisted into ``assets.meta['kr_tax_class']``.
    Indices (EQUITY_INDEX) should pass ``kr_tax_class=None``.
    Arbitrary extra metadata can be supplied via ``extra_meta``.
    """

    symbol: str
    market: str
    asset_type: str
    currency: str
    name: str
    kr_tax_class: Optional[str] = None
    extra_meta: dict[str, Any] = field(default_factory=dict)
    category: str = ""  # stdout grouping label only; not persisted

    def to_meta(self) -> dict[str, Any]:
        """Build the JSONB ``meta`` payload for this asset."""
        meta: dict[str, Any] = dict(self.extra_meta)
        if self.kr_tax_class is not None:
            meta["kr_tax_class"] = self.kr_tax_class
        return meta


# ---------------------------------------------------------------------------
# KR universe (pykrx)
# ---------------------------------------------------------------------------
def kr_indices() -> list[AssetRow]:
    """Primary KR equity indices. No kr_tax_class (not an investable product)."""
    return [
        AssetRow("KS11",  "KR", "EQUITY_INDEX", "KRW", "KOSPI",
                 kr_tax_class=None, category="KR_INDEX"),
        AssetRow("KQ11",  "KR", "EQUITY_INDEX", "KRW", "KOSDAQ",
                 kr_tax_class=None, category="KR_INDEX"),
        AssetRow("KS200", "KR", "EQUITY_INDEX", "KRW", "KOSPI 200",
                 kr_tax_class=None, category="KR_INDEX"),
    ]


def kr_etfs() -> list[AssetRow]:
    """Representative Korean-listed ETFs covering equity / bond / overseas / mixed."""
    # Tax classes per architecture decision #14.
    rows: list[AssetRow] = [
        # --- KR equity ETFs -------------------------------------------------
        AssetRow("069500", "KR", "ETF", "KRW", "KODEX 200",
                 kr_tax_class="kr_equity_etf", category="KR_ETF"),
        AssetRow("278540", "KR", "ETF", "KRW",
                 "KODEX MSCI Korea ESG 유니버설",
                 kr_tax_class="kr_equity_etf", category="KR_ETF"),
        AssetRow("114800", "KR", "ETF", "KRW", "KODEX 인버스",
                 kr_tax_class="kr_equity_etf", category="KR_ETF"),
        AssetRow("229200", "KR", "ETF", "KRW", "KODEX 코스닥 150",
                 kr_tax_class="kr_equity_etf", category="KR_ETF"),
        AssetRow("102110", "KR", "ETF", "KRW", "TIGER 200",
                 kr_tax_class="kr_equity_etf", category="KR_ETF"),
        AssetRow("232080", "KR", "ETF", "KRW", "TIGER 코스닥150",
                 kr_tax_class="kr_equity_etf", category="KR_ETF"),

        # --- KR overseas-equity ETFs ----------------------------------------
        AssetRow("133690", "KR", "ETF", "KRW", "KODEX 미국 나스닥100",
                 kr_tax_class="kr_overseas_etf", category="KR_ETF"),
        AssetRow("360750", "KR", "ETF", "KRW", "TIGER 미국S&P500",
                 kr_tax_class="kr_overseas_etf", category="KR_ETF"),
        AssetRow("143850", "KR", "ETF", "KRW", "TIGER 미국S&P500선물(H)",
                 kr_tax_class="kr_overseas_etf", category="KR_ETF"),
        AssetRow("381170", "KR", "ETF", "KRW", "TIGER 미국테크TOP10 INDXX",
                 kr_tax_class="kr_overseas_etf", category="KR_ETF"),
        AssetRow("195930", "KR", "ETF", "KRW", "TIGER 유로스탁스50(합성 H)",
                 kr_tax_class="kr_overseas_etf", category="KR_ETF"),
        AssetRow("192090", "KR", "ETF", "KRW", "TIGER 차이나CSI300",
                 kr_tax_class="kr_overseas_etf", category="KR_ETF"),
        AssetRow("136340", "KR", "ETF", "KRW", "TIGER 미국달러선물레버리지",
                 kr_tax_class="kr_overseas_etf", category="KR_ETF"),

        # --- KR bond ETFs ---------------------------------------------------
        AssetRow("148070", "KR", "ETF", "KRW", "KOSEF 국고채10년",
                 kr_tax_class="kr_bond_etf", category="KR_ETF"),
        AssetRow("130730", "KR", "ETF", "KRW", "KOSEF 단기자금",
                 kr_tax_class="kr_bond_etf", category="KR_ETF"),
        # NOTE: ``305080`` was flagged as not independently verifiable at
        # authoring time; treat the symbol as a TODO until confirmed with
        # pykrx.stock.get_etf_ticker_list(). Keeping as placeholder for now.
        AssetRow("305080", "KR", "ETF", "KRW",
                 "TIGER 미국채10년선물",  # TODO: verify ticker with pykrx
                 kr_tax_class="kr_bond_etf", category="KR_ETF",
                 extra_meta={"ticker_unverified": True}),

        # --- KR mixed / commodity ETFs --------------------------------------
        AssetRow("132030", "KR", "ETF", "KRW", "KODEX 골드선물(H)",
                 kr_tax_class="kr_mixed_etf", category="KR_ETF"),
        AssetRow("411060", "KR", "ETF", "KRW", "ACE KRX금현물",
                 kr_tax_class="kr_mixed_etf", category="KR_ETF"),
        AssetRow("261220", "KR", "ETF", "KRW", "KODEX WTI원유선물(H)",
                 kr_tax_class="kr_mixed_etf", category="KR_ETF"),
        AssetRow("139660", "KR", "ETF", "KRW", "TIGER 200 IT",
                 kr_tax_class="kr_equity_etf", category="KR_ETF"),
    ]
    return rows


# ---------------------------------------------------------------------------
# US universe (yfinance)
# ---------------------------------------------------------------------------
def us_indices() -> list[AssetRow]:
    """Primary US equity indices. No kr_tax_class."""
    return [
        AssetRow("^GSPC", "US", "EQUITY_INDEX", "USD", "S&P 500",
                 kr_tax_class=None, category="US_INDEX"),
        AssetRow("^NDX",  "US", "EQUITY_INDEX", "USD", "Nasdaq 100",
                 kr_tax_class=None, category="US_INDEX"),
        AssetRow("^DJI",  "US", "EQUITY_INDEX", "USD", "Dow Jones Industrial Average",
                 kr_tax_class=None, category="US_INDEX"),
        AssetRow("^RUT",  "US", "EQUITY_INDEX", "USD", "Russell 2000",
                 kr_tax_class=None, category="US_INDEX"),
    ]


def us_equity_etfs() -> list[AssetRow]:
    """Broad-market, sector, country/region, factor ETFs on US exchanges."""
    broad = [
        ("SPY", "SPDR S&P 500 ETF Trust"),
        ("QQQ", "Invesco QQQ Trust (Nasdaq-100)"),
        ("DIA", "SPDR Dow Jones Industrial Average ETF"),
        ("IWM", "iShares Russell 2000 ETF"),
        ("VTI", "Vanguard Total Stock Market ETF"),
        ("VOO", "Vanguard S&P 500 ETF"),
        ("VT",  "Vanguard Total World Stock ETF"),
    ]
    sectors = [
        ("XLK",  "SPDR Technology Select Sector"),
        ("XLF",  "SPDR Financial Select Sector"),
        ("XLV",  "SPDR Health Care Select Sector"),
        ("XLE",  "SPDR Energy Select Sector"),
        ("XLI",  "SPDR Industrial Select Sector"),
        ("XLY",  "SPDR Consumer Discretionary Select Sector"),
        ("XLP",  "SPDR Consumer Staples Select Sector"),
        ("XLU",  "SPDR Utilities Select Sector"),
        ("XLB",  "SPDR Materials Select Sector"),
        ("XLRE", "SPDR Real Estate Select Sector"),
        ("XLC",  "SPDR Communication Services Select Sector"),
    ]
    regions = [
        ("EFA",  "iShares MSCI EAFE ETF"),
        ("EEM",  "iShares MSCI Emerging Markets ETF"),
        ("EWJ",  "iShares MSCI Japan ETF"),
        ("EWG",  "iShares MSCI Germany ETF"),
        ("EWU",  "iShares MSCI United Kingdom ETF"),
        ("EWY",  "iShares MSCI South Korea ETF"),
        ("EWT",  "iShares MSCI Taiwan ETF"),
        ("FXI",  "iShares China Large-Cap ETF"),
        ("INDA", "iShares MSCI India ETF"),
        ("VWO",  "Vanguard FTSE Emerging Markets ETF"),
    ]
    factors = [
        ("MTUM", "iShares MSCI USA Momentum Factor"),
        ("VLUE", "iShares MSCI USA Value Factor"),
        ("USMV", "iShares MSCI USA Min Vol Factor"),
        ("QUAL", "iShares MSCI USA Quality Factor"),
        ("IWD",  "iShares Russell 1000 Value"),
        ("IWF",  "iShares Russell 1000 Growth"),
    ]

    out: list[AssetRow] = []
    for sym, name in broad + sectors + regions + factors:
        out.append(
            AssetRow(sym, "US", "ETF", "USD", name,
                     kr_tax_class="overseas_etf", category="US_EQUITY_ETF")
        )
    return out


def us_bond_etfs() -> list[AssetRow]:
    """Bond ETFs listed in the US."""
    data = [
        ("TLT", "iShares 20+ Year Treasury Bond ETF"),
        ("IEF", "iShares 7-10 Year Treasury Bond ETF"),
        ("SHY", "iShares 1-3 Year Treasury Bond ETF"),
        ("AGG", "iShares Core U.S. Aggregate Bond ETF"),
        ("LQD", "iShares iBoxx $ Investment Grade Corporate Bond ETF"),
        ("HYG", "iShares iBoxx $ High Yield Corporate Bond ETF"),
        ("TIP", "iShares TIPS Bond ETF"),
        ("BND", "Vanguard Total Bond Market ETF"),
        ("BIL", "SPDR Bloomberg 1-3 Month T-Bill ETF"),
    ]
    return [
        AssetRow(sym, "US", "BOND", "USD", name,
                 kr_tax_class="overseas_etf", category="US_BOND_ETF")
        for sym, name in data
    ]


def us_commodity_etfs() -> list[AssetRow]:
    """Commodity ETFs (metals, energy, broad)."""
    data = [
        ("GLD",  "SPDR Gold Shares"),
        ("IAU",  "iShares Gold Trust"),
        ("SLV",  "iShares Silver Trust"),
        ("PDBC", "Invesco Optimum Yield Diversified Commodity Strategy"),
        ("USO",  "United States Oil Fund"),
        ("DBA",  "Invesco DB Agriculture Fund"),
        ("DBB",  "Invesco DB Base Metals Fund"),
        ("PPLT", "abrdn Physical Platinum Shares ETF"),
        ("PALL", "abrdn Physical Palladium Shares ETF"),
    ]
    return [
        AssetRow(sym, "US", "COMMODITY", "USD", name,
                 kr_tax_class="overseas_etf", category="COMMODITY")
        for sym, name in data
    ]


def crypto_assets() -> list[AssetRow]:
    """Crypto majors via yfinance symbols. ``market='CRYPTO'``."""
    data = [
        ("BTC-USD", "Bitcoin (USD)"),
        ("ETH-USD", "Ethereum (USD)"),
    ]
    return [
        AssetRow(sym, "CRYPTO", "CRYPTO", "USD", name,
                 kr_tax_class="crypto", category="CRYPTO")
        for sym, name in data
    ]


# ---------------------------------------------------------------------------
# Assembly
# ---------------------------------------------------------------------------
def all_rows() -> list[AssetRow]:
    """Concatenate all categories. FX pairs are excluded by design."""
    return (
        kr_indices()
        + kr_etfs()
        + us_indices()
        + us_equity_etfs()
        + us_bond_etfs()
        + us_commodity_etfs()
        + crypto_assets()
    )


def summarize(rows: Iterable[AssetRow]) -> dict[str, int]:
    """Return ``{category: count}`` for stdout reporting."""
    counts: dict[str, int] = {}
    for r in rows:
        counts[r.category] = counts.get(r.category, 0) + 1
    return counts


# ---------------------------------------------------------------------------
# Insertion
# ---------------------------------------------------------------------------
def insert_assets(session: Session, rows: Iterable[AssetRow]) -> dict[str, int]:
    """Insert each asset, skipping (symbol, market) collisions.

    The repository is used read-only + create; :meth:`AssetRepository.upsert`
    is **not** used here because the task spec asks for "skip on conflict"
    behavior rather than update-on-conflict.

    Returns
    -------
    dict with keys ``inserted``, ``skipped``, ``total``.
    """
    rows = list(rows)
    repo = AssetRepository(session)
    inserted = 0
    skipped = 0
    for row in rows:
        existing = repo.get_by_symbol(row.symbol, row.market)
        if existing is not None:
            skipped += 1
            continue
        asset = Asset(
            symbol=row.symbol,
            market=row.market,
            asset_type=row.asset_type,
            name=row.name,
            currency=row.currency,
            active=True,
            meta=row.to_meta(),
        )
        session.add(asset)
        session.flush()
        inserted += 1
    return {"inserted": inserted, "skipped": skipped, "total": len(rows)}


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def _print_summary(rows: list[AssetRow]) -> None:
    """Emit per-category and grand-total counts."""
    counts = summarize(rows)
    print("Universe composition:")
    for cat in sorted(counts):
        print(f"  {cat:20s} {counts[cat]:>4d}")
    print(f"  {'TOTAL':20s} {len(rows):>4d}")


def main(argv: Optional[list[str]] = None) -> None:
    """Entry point. ``--dry-run`` skips DB writes and only prints counts."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print category counts and exit without touching the database.",
    )
    args = parser.parse_args(argv)

    rows = all_rows()
    _print_summary(rows)

    if args.dry_run:
        print("[dry-run] No DB writes performed.")
        return

    with get_session() as session:
        result = insert_assets(session, rows)
    print("Insert result:", result)


if __name__ == "__main__":
    main()
