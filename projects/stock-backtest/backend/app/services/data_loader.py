"""백테스트 입력 데이터 로더.

ohlcv 테이블 → prices_aligned (base 캘린더 정렬 + 비base 시장 forward-fill).
fx_rates 테이블 → fx_rates_to_base (date → {ccy → base_per_ccy}).

architecture.md V3 § "멀티 마켓 캘린더" L549-555 + § "Phase 1 MVP" L728 근거.

본 모듈은 Service 계층:
- backtest_runner.execute_backtest_job 가 호출해 BacktestRunContext 의 prices_aligned,
  fx_rates_to_base, universe_market_meta 를 채운다.
- 도메인 레이어 (calendar.align_market_price_to_base_calendar) 만 사용. SQLAlchemy
  ORM 객체는 본 모듈 밖으로 새지 않게 봉인한다 (clean architecture).

FxRate 의미 (models/fx_rates.py 주석):
- USDKRW=1300 → row(base_ccy=USD, quote_ccy=KRW, rate=1300)
- 즉 rate = quote_per_base = "1 base 단위가 quote 통화로 얼마"
- 백테스트 base_currency=KRW, 자산통화=USD 일 때 fx_rates_to_base["USD"] = KRW per USD = 1300
- 따라서 lookup: FxRate(base_ccy=ccy, quote_ccy=base_currency).rate 가 base_per_ccy 와 동일
"""

from __future__ import annotations

from datetime import date, datetime, timedelta
from decimal import Decimal

import pandas as pd
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.calendar import (
    align_market_price_to_base_calendar,
    trading_days_in_period,
)
from app.models.asset import Asset
from app.models.fx_rates import FxRate
from app.models.ohlcv import Ohlcv

# ohlcv/fx 백필 갭 대비 lookback. 첫 거래일 이전 가장 최근 종가/환율을 forward-fill 시작점으로
# 포함시키기 위함 (긴 연휴 + 휴장 누적 마진).
_LOOKBACK_DAYS = 30


def load_universe_market_meta(
    session: Session, asset_ids: list[int]
) -> dict[int, tuple[str, str]]:
    """asset_id → (market, currency) dict. universe 전체 메타를 한 번에 로드.

    누락된 asset_id 는 결과 dict 에서 제외 (호출자 책임으로 결측 처리).
    """
    if not asset_ids:
        return {}
    rows = session.execute(
        select(Asset).where(Asset.asset_id.in_(asset_ids))
    ).scalars().all()
    return {row.asset_id: (row.market, row.currency) for row in rows}


def _load_asset_close_series(
    session: Session,
    asset_id: int,
    start: date,
    end: date,
) -> dict[date, Decimal]:
    """단일 자산의 [start, end] 종가 시계열. {date → close} dict.

    lookback 마진을 두어 forward-fill 시작 시점에 사용할 직전 거래일 종가를 함께 로드한다.
    """
    rows = session.execute(
        select(Ohlcv.time, Ohlcv.close)
        .where(
            Ohlcv.asset_id == asset_id,
            Ohlcv.time >= datetime.combine(
                start - timedelta(days=_LOOKBACK_DAYS), datetime.min.time()
            ),
            Ohlcv.time <= datetime.combine(end, datetime.max.time()),
        )
        .order_by(Ohlcv.time)
    ).all()
    return {row.time.date(): Decimal(str(row.close)) for row in rows}


def load_prices_aligned(
    session: Session,
    asset_ids: list[int],
    base_currency: str,
    period_start: date,
    period_end: date,
    asset_meta: dict[int, tuple[str, str]] | None = None,
) -> pd.DataFrame:
    """ohlcv → base 캘린더 정렬된 종가 DataFrame.

    Returns:
        index = date (base 캘린더 거래일, 오름차순)
        columns = asset_id (int)
        values = float (NaN 가능 — 자산 시장의 가용 종가가 lookback 안에서도 부재)
    """
    timeline = trading_days_in_period(base_currency, period_start, period_end)
    if not asset_ids or not timeline:
        return pd.DataFrame(index=pd.Index(timeline, name="date"))

    if asset_meta is None:
        asset_meta = load_universe_market_meta(session, asset_ids)

    # 각 자산의 종가 시계열을 미리 dict 로 로드 — base 거래일 루프에서 일별 SQL 회피.
    asset_prices: dict[int, dict[date, Decimal]] = {
        aid: _load_asset_close_series(session, aid, period_start, period_end)
        for aid in asset_ids
    }

    columns: dict[int, list[float | None]] = {aid: [] for aid in asset_ids}
    for trading_day in timeline:
        for aid in asset_ids:
            market, _ccy = asset_meta.get(aid, ("US", base_currency))
            aligned = align_market_price_to_base_calendar(
                market, base_currency, trading_day, asset_prices[aid]
            )
            columns[aid].append(float(aligned) if aligned is not None else None)

    df = pd.DataFrame(columns, index=pd.Index(timeline, name="date"))
    return df


def _load_fx_pair_series(
    session: Session,
    ccy: str,
    base_currency: str,
    period_start: date,
    period_end: date,
) -> dict[date, Decimal]:
    """단일 통화쌍의 [start, end] base_per_ccy 시계열 dict.

    FxRate(base_ccy=ccy, quote_ccy=base_currency).rate 가 정확히 base_per_ccy.
    lookback 마진으로 첫 거래일 이전 환율을 forward-fill 시작점에 포함.
    """
    rows = session.execute(
        select(FxRate.time, FxRate.rate)
        .where(
            FxRate.base_ccy == ccy,
            FxRate.quote_ccy == base_currency,
            FxRate.time >= datetime.combine(
                period_start - timedelta(days=_LOOKBACK_DAYS), datetime.min.time()
            ),
            FxRate.time <= datetime.combine(period_end, datetime.max.time()),
        )
        .order_by(FxRate.time)
    ).all()
    return {row.time.date(): Decimal(str(row.rate)) for row in rows}


def load_fx_rates_to_base(
    session: Session,
    base_currency: str,
    period_start: date,
    period_end: date,
    needed_currencies: set[str],
) -> dict[date, dict[str, Decimal]]:
    """date → {ccy → base_per_ccy} dict.

    base_currency 자체는 항상 1.0 (각 거래일 dict 에 자동 포함).
    base 가 아닌 통화는 fx_rates 테이블에서 forward-fill — 환율 휴장일/주말 대비.
    환율 데이터가 전체 기간에 걸쳐 부재한 통화는 해당 거래일 dict 에서 키 자체가 누락 →
    domain.engine 이 MissingFxError 등으로 처리 (look-ahead 금지 정책상 back-fill 미사용).
    """
    timeline = trading_days_in_period(base_currency, period_start, period_end)
    out: dict[date, dict[str, Decimal]] = {
        trading_day: {base_currency: Decimal("1")} for trading_day in timeline
    }

    for ccy in needed_currencies:
        if ccy == base_currency:
            continue
        ccy_rates = _load_fx_pair_series(
            session, ccy, base_currency, period_start, period_end
        )
        last_known: Decimal | None = None
        for trading_day in timeline:
            if trading_day in ccy_rates:
                last_known = ccy_rates[trading_day]
            if last_known is not None:
                out[trading_day][ccy] = last_known

    return out


def build_backtest_context(
    session: Session,
    asset_ids: list[int],
    base_currency: str,
    period_start: date,
    period_end: date,
) -> tuple[
    pd.DataFrame,
    dict[int, tuple[str, str]],
    dict[date, dict[str, Decimal]],
]:
    """run_backtest 에 넘길 (prices_aligned, universe_market_meta, fx_rates_to_base) 묶음 산출.

    backtest_runner.execute_backtest_job 가 BacktestRunContext 구성 직전에 호출.
    초기 자본 (initial_cash) 은 호출자가 별도로 처리한다 (run.params 에서 추출).
    """
    asset_meta = load_universe_market_meta(session, asset_ids)
    needed_currencies = {ccy for _market, ccy in asset_meta.values()}

    prices_aligned = load_prices_aligned(
        session,
        asset_ids,
        base_currency,
        period_start,
        period_end,
        asset_meta=asset_meta,
    )
    fx_rates = load_fx_rates_to_base(
        session, base_currency, period_start, period_end, needed_currencies
    )
    return prices_aligned, asset_meta, fx_rates
