"""End-to-end 스모크 (BLOCKER-001 해소 후 수동 실행).

전제:
    1. docker compose down -v && docker compose up -d  (clean 볼륨)
    2. cd backend && alembic upgrade head
    3. python scripts/seed_catalog.py
    (선택) 4. ohlcv 백필 cron 또는 yfinance/pykrx 수동 백필

검증:
    - 자산 카탈로그가 비어있지 않은가
    - 샘플 자산의 ohlcv 데이터가 적재되었는가
    - data_loader.build_backtest_context 가 universe → (prices_aligned,
      universe_market_meta, fx_rates_to_base) 까지 정상 구성하는가

전체 백테스트 실행은 본 스크립트가 수행하지 않는다 — 그건 API 경유:
    POST /backtests → 폴링.
"""

from __future__ import annotations

import sys
from datetime import date, timedelta

from sqlalchemy import select

from app.core.db import SessionLocal
from app.models.asset import Asset
from app.models.ohlcv import Ohlcv
from app.services.data_loader import build_backtest_context


def main() -> int:
    with SessionLocal() as session:
        assets = session.execute(select(Asset).limit(10)).scalars().all()
        if not assets:
            print(
                "ERROR: 자산 카탈로그가 비어 있습니다. "
                "scripts/seed_catalog.py 를 먼저 실행하세요."
            )
            return 1
        print(f"OK   카탈로그 자산 {len(assets)}건 (sample)")

        sample = assets[0]
        ohlcv_rows = session.execute(
            select(Ohlcv).where(Ohlcv.asset_id == sample.asset_id).limit(5)
        ).scalars().all()
        if not ohlcv_rows:
            print(
                f"WARN {sample.symbol} ({sample.market}) ohlcv 부재 — "
                f"백필 cron 또는 수동 백필 필요. "
                f"data_loader 검증은 시도하지만 prices_aligned 가 NaN 으로 채워질 수 있다."
            )
        else:
            print(
                f"OK   {sample.symbol} ohlcv {len(ohlcv_rows)}+ 행 확인 "
                f"(latest time={ohlcv_rows[-1].time.date()})"
            )

        period_end = date.today()
        period_start = period_end - timedelta(days=180)
        prices_aligned, market_meta, fx_rates = build_backtest_context(
            session=session,
            asset_ids=[sample.asset_id],
            base_currency="KRW",
            period_start=period_start,
            period_end=period_end,
        )
        print(
            f"OK   data_loader: prices_aligned shape={prices_aligned.shape}, "
            f"market_meta keys={list(market_meta.keys())}, "
            f"fx_rates dates={len(fx_rates)}"
        )

    print("\n다음 단계: uvicorn app.main:app --port 8001 + frontend npm run dev")
    return 0


if __name__ == "__main__":
    sys.exit(main())
