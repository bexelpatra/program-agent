"""Cron 잡 정의 + APScheduler 부트스트랩.

architecture.md V3 § "에이전트 위임 영역 - 데이터 수집" + V1 결정 9 근거.

V1 결정 9 (시장별 cron 시각, 모두 KST):
- KR     18:00: pykrx 일봉 수집 (한국 장 마감 ~15:30 + 정산 여유)
- US     07:00: yfinance 미국 일봉 수집 (US 장 마감 다음 날 오전, KST 기준)
- CRYPTO 09:00: yfinance 암호화폐 일봉 수집 (24/7 시장, 임의 고정 시각)

각 시장은 독립 잡으로 등록되어 한 시장의 실패가 다른 시장 잡에 영향을 주지 않는다.
실제 백필 로직은 `app.data.pipeline.backfill_active_assets` 에 위임하며 본 모듈은
잡 정의 + 시장 라우팅만 담당한다.

scheduler.start() 는 FastAPI lifespan (TASK-061) 에서 호출한다 — 본 모듈은
빌드만 제공해 단위 테스트에서 백그라운드 워커 없이 잡 등록 검증이 가능하게 한다.
"""
from __future__ import annotations

import logging
from typing import Callable

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from app.core.db import SessionLocal
from app.data.pipeline import backfill_active_assets
from app.data.sources import get_source_for_market
from app.data.sources.base import DataSource
from app.data.sources.pykrx_source import PykrxSource
from app.data.sources.yfinance_source import YfinanceSource
from app.domain.asset.entity import Market

logger = logging.getLogger(__name__)

KST_TZ = "Asia/Seoul"


def _run_market_backfill(market: Market) -> None:
    """단일 시장 백필 잡.

    SessionLocal 새 세션을 자체 생성한다 (cron 잡은 FastAPI request scope 외부에서
    실행되므로 Depends 사용 불가). 자산 단위 commit/rollback 격리는
    `backfill_active_assets` 가 보장한다.

    한 시장이 통째로 예외를 던져도 다른 시장 잡에 영향이 없도록 본 함수 내부에서
    최종 catch 한다 (APScheduler 자체도 잡 단위 격리는 하지만 이중 안전망).
    """
    logger.info("cron: starting backfill for market=%s", market)
    # 라우팅 결정은 get_source_for_market 단일 진입점에 위임 (TASK-235).
    # 단일 시장만 라우팅 → backfill_active_assets 가 매칭되지 않는 자산은
    # REJECTED 처리. 시장별 독립 실행을 보장한다.
    try:
        source = get_source_for_market(
            market,
            yfinance=YfinanceSource(),
            pykrx=PykrxSource(),
        )
    except ValueError:
        logger.error("cron: unknown market=%s, skip", market)
        return
    filtered_sources: dict[str, DataSource] = {market: source}

    with SessionLocal() as session:
        try:
            results = backfill_active_assets(session, filtered_sources)
            ok = sum(1 for r in results if r.status == "OK")
            partial = sum(1 for r in results if r.status == "PARTIAL")
            failed = sum(1 for r in results if r.status == "FAILED")
            rejected = sum(1 for r in results if r.status == "REJECTED")
            logger.info(
                "cron: market=%s done — ok=%d partial=%d failed=%d rejected=%d total=%d",
                market,
                ok,
                partial,
                failed,
                rejected,
                len(results),
            )
        except Exception as e:  # noqa: BLE001 - 잡 격리, 한 시장 실패가 다른 잡에 전파되지 않게 흡수
            logger.exception("cron: market=%s uncaught error: %s", market, e)


def build_scheduler(
    on_kr: Callable[[], None] | None = None,
    on_us: Callable[[], None] | None = None,
    on_crypto: Callable[[], None] | None = None,
) -> BackgroundScheduler:
    """APScheduler `BackgroundScheduler` 인스턴스 + 3개 cron 잡 등록.

    `on_*` 콜러블 미지정 시 디폴트로 `_run_market_backfill` 을 사용한다.
    테스트는 mock 콜러블을 주입해 트리거 등록·발화를 검증할 수 있다.

    `replace_existing=True` 로 동일 잡 ID 재등록 시 충돌하지 않는다 (lifespan
    재시작 / 핫리로드 시나리오 안전).

    스케줄러는 빌드만 하고 `.start()` 는 호출자 (FastAPI lifespan, TASK-061) 책임.
    """
    scheduler = BackgroundScheduler(timezone=KST_TZ)

    scheduler.add_job(
        on_kr if on_kr is not None else (lambda: _run_market_backfill("KR")),
        trigger=CronTrigger(hour=18, minute=0, timezone=KST_TZ),
        id="backfill_kr",
        name="KR daily backfill (18:00 KST)",
        replace_existing=True,
    )
    scheduler.add_job(
        on_us if on_us is not None else (lambda: _run_market_backfill("US")),
        trigger=CronTrigger(hour=7, minute=0, timezone=KST_TZ),
        id="backfill_us",
        name="US daily backfill (07:00 KST, next day)",
        replace_existing=True,
    )
    scheduler.add_job(
        on_crypto if on_crypto is not None else (lambda: _run_market_backfill("CRYPTO")),
        trigger=CronTrigger(hour=9, minute=0, timezone=KST_TZ),
        id="backfill_crypto",
        name="Crypto daily backfill (09:00 KST)",
        replace_existing=True,
    )
    return scheduler


__all__ = [
    "KST_TZ",
    "_run_market_backfill",
    "build_scheduler",
]
