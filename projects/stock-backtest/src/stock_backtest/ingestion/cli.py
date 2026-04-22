"""Ingestion CLI entrypoint.

architecture.md §9 (DB 기반 증분) 에서 정의한 cron 구성을 실행하기 위한
CLI 래퍼. 시장별로 :class:`IngestionPipeline` 을 실행하고 결과를 로그로
요약 출력한다.

사용 예::

    python -m stock_backtest.ingestion.cli --market KR
    python -m stock_backtest.ingestion.cli --market US --dry-run
    python -m stock_backtest.ingestion.cli --market ALL --log-level DEBUG
    python -m stock_backtest.ingestion.cli --market US --symbols SPY,QQQ

종료 코드
---------
- 0: 전체 자산 수집 성공(SUCCESS 만 존재; SKIPPED 는 성공으로 간주)
- 1: 일부 자산 FAILED 또는 PARTIAL
- 2: 전체 자산 FAILED (또는 내부 예외)
"""

from __future__ import annotations

import argparse
import logging
import sys
from contextlib import nullcontext
from typing import Iterable, Sequence

from ..config import load_config
from ..data import db as _db
from ..data.repository import AssetRepository
from .base import DataSource
from .pipeline import IngestionPipeline, IngestionResult
from .pykrx_source import PykrxSource
from .yfinance_source import YFinanceSource


logger = logging.getLogger("stock_backtest.ingestion.cli")


_MARKETS_ORDER: tuple[str, ...] = ("KR", "US", "CRYPTO")
_VALID_MARKETS: frozenset[str] = frozenset({*_MARKETS_ORDER, "ALL"})


# ---------------------------------------------------------------------------
# argparse
# ---------------------------------------------------------------------------


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m stock_backtest.ingestion.cli",
        description=(
            "OHLCV 증분 수집 CLI. " "시장별 active 자산을 DB 에서 읽어 DataSource 로부터 일봉을 수집한다."
        ),
    )
    parser.add_argument(
        "--market",
        required=True,
        choices=sorted(_VALID_MARKETS),
        help="대상 시장. ALL 은 KR→US→CRYPTO 순차 실행.",
    )
    parser.add_argument(
        "--symbols",
        default=None,
        help=(
            "쉼표로 구분된 심볼 목록 (선택). 지정 시 해당 시장의 자산 중 " "이 심볼만 수집한다. 예: --symbols SPY,QQQ"
        ),
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="쓰기 없이 대상 자산을 열거하고 종료한다.",
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="로그 레벨 (기본 INFO).",
    )
    return parser


# ---------------------------------------------------------------------------
# source mapping
# ---------------------------------------------------------------------------


def _build_sources_for_market(market: str) -> dict[str, DataSource]:
    """market 에 필요한 DataSource 매핑을 구성한다.

    - KR     → PykrxSource
    - US     → YFinanceSource
    - CRYPTO → YFinanceSource
    - FX     → YFinanceSource (보조)
    """
    if market == "KR":
        return {"KR": PykrxSource()}
    if market == "US":
        yf = YFinanceSource()
        return {"US": yf, "FX": yf}
    if market == "CRYPTO":
        yf = YFinanceSource()
        return {"CRYPTO": yf, "FX": yf}
    raise ValueError(f"unsupported market for source mapping: {market!r}")


# ---------------------------------------------------------------------------
# dry-run / run helpers
# ---------------------------------------------------------------------------


def _filter_symbols(symbols: str | None) -> set[str] | None:
    if symbols is None:
        return None
    picks = {s.strip() for s in symbols.split(",") if s.strip()}
    return picks or None


def _dry_run_market(market: str, symbol_filter: set[str] | None) -> None:
    """자산 목록만 열거하고 실제 수집은 하지 않는다."""
    with _db.get_session() as session:
        assets = AssetRepository(session).list_active(market=market)
    if symbol_filter is not None:
        assets = [a for a in assets if a.symbol in symbol_filter]
    logger.info(
        "[dry-run] market=%s target_assets=%d%s",
        market,
        len(assets),
        f" (filtered by symbols={sorted(symbol_filter)})" if symbol_filter else "",
    )
    for a in assets:
        logger.info(
            "[dry-run]   asset_id=%s symbol=%s market=%s type=%s",
            a.asset_id,
            a.symbol,
            a.market,
            getattr(a, "asset_type", "?"),
        )


def _run_market(market: str, symbol_filter: set[str] | None) -> list[IngestionResult]:
    """단일 시장에 대해 IngestionPipeline 을 실행한다."""
    settings = load_config()
    sources = _build_sources_for_market(market)

    # session_factory: get_session 컨텍스트 매니저 자체를 넘긴다.
    # IngestionPipeline 은 __enter__/__exit__ 패턴을 인식한다.
    pipeline = IngestionPipeline(
        sources=sources,
        session_factory=_db.get_session,
        settings=settings,
    )

    if symbol_filter is None:
        results = pipeline.run_for_market(market)
    else:
        # 심볼 필터가 있으면 active 자산 중 매칭만 대상.
        with _db.get_session() as session:
            assets = [
                a
                for a in AssetRepository(session).list_active(market=market)
                if a.symbol in symbol_filter
            ]
        logger.info(
            "market=%s filtered_assets=%d by symbols=%s",
            market,
            len(assets),
            sorted(symbol_filter),
        )
        results = [pipeline.run_for_asset(a) for a in assets]

    for r in results:
        logger.info(
            "result asset_id=%s status=%s rows_inserted=%d rows_rejected=%d%s",
            r.asset_id,
            r.status,
            r.rows_inserted,
            r.rows_rejected,
            f" error={r.error_message!r}" if r.error_message else "",
        )
    return results


# ---------------------------------------------------------------------------
# summary / exit code
# ---------------------------------------------------------------------------


def _summarize(all_results: Sequence[IngestionResult]) -> dict[str, int]:
    tally = {"SUCCESS": 0, "PARTIAL": 0, "FAILED": 0, "SKIPPED": 0}
    for r in all_results:
        tally[r.status] = tally.get(r.status, 0) + 1
    return tally


def _exit_code(tally: dict[str, int]) -> int:
    total = sum(tally.values())
    if total == 0:
        # 대상 자산이 없으면 성공으로 취급.
        return 0
    failed = tally.get("FAILED", 0)
    partial = tally.get("PARTIAL", 0)
    success = tally.get("SUCCESS", 0)
    skipped = tally.get("SKIPPED", 0)
    # 전체 실패: success + partial == 0 이고 failed > 0
    if failed > 0 and success == 0 and partial == 0:
        return 2
    # 일부 실패 / 일부 부분 성공
    if failed > 0 or partial > 0:
        return 1
    # success + skipped 만 존재
    _ = skipped  # 로그용
    return 0


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------


def _markets_for(market: str) -> tuple[str, ...]:
    if market == "ALL":
        return _MARKETS_ORDER
    return (market,)


def main(argv: Iterable[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)

    logging.basicConfig(
        level=getattr(logging, args.log_level),
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    symbol_filter = _filter_symbols(args.symbols)
    markets = _markets_for(args.market)

    logger.info(
        "ingestion CLI start: markets=%s dry_run=%s symbols=%s",
        list(markets),
        args.dry_run,
        sorted(symbol_filter) if symbol_filter else None,
    )

    all_results: list[IngestionResult] = []
    per_market_summary: list[tuple[str, dict[str, int]]] = []

    try:
        for m in markets:
            if args.dry_run:
                _dry_run_market(m, symbol_filter)
                per_market_summary.append((m, {"DRY_RUN": 0}))
                continue
            results = _run_market(m, symbol_filter)
            all_results.extend(results)
            per_market_summary.append((m, _summarize(results)))
    except Exception:
        logger.exception("ingestion CLI fatal error")
        return 2

    # 전체 요약.
    if args.dry_run:
        for m, _tally in per_market_summary:
            logger.info("[dry-run summary] market=%s", m)
        return 0

    overall = _summarize(all_results)
    logger.info("=" * 60)
    for m, tally in per_market_summary:
        logger.info(
            "market=%s SUCCESS=%d PARTIAL=%d FAILED=%d SKIPPED=%d",
            m,
            tally.get("SUCCESS", 0),
            tally.get("PARTIAL", 0),
            tally.get("FAILED", 0),
            tally.get("SKIPPED", 0),
        )
    logger.info(
        "TOTAL assets=%d SUCCESS=%d PARTIAL=%d FAILED=%d SKIPPED=%d",
        len(all_results),
        overall.get("SUCCESS", 0),
        overall.get("PARTIAL", 0),
        overall.get("FAILED", 0),
        overall.get("SKIPPED", 0),
    )

    return _exit_code(overall)


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())


# Silence unused import warning for nullcontext (kept for potential future use).
_ = nullcontext


__all__ = ["main"]
