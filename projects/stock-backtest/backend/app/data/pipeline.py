"""증분 데이터 파이프라인.

architecture.md V3 § "에이전트 위임 영역 - 데이터 수집" + V1 § 결정 9 / 결정 13 근거.

- assets active 자산별 MAX(time) → 다음 날부터 yfinance/pykrx 백필
- 거래일 캘린더 vs ohlcv 커버리지 비교 → 갭 자동 재수집
- 멱등 UPSERT (asset_id, time)
- 자산 단위 3회 재시도 (1s → 2s → 4s 지수 백오프)
- 실패 시 ingestion_log FAILED 기록, 잡은 다른 자산으로 계속 진행
- close=0/null/NaN 거부는 어댑터(sources/) 가 1차 방어 (수집 레이어)
- 캘린더 외 날짜 수집 제외 — 본 모듈이 2차 방어 (캘린더 레이어)

orchestration 만 담당하고 도메인 로직 (allocator/filter/engine) 은 직접 다루지 않는다.
"""
from __future__ import annotations

import logging
import time
from dataclasses import dataclass
from datetime import date, datetime, timedelta

import exchange_calendars as xcals
from sqlalchemy.orm import Session

from app.data.asset_repository import SqlAssetRepository
from app.data.repositories.ingestion_log_repository import IngestionLogRepository
from app.data.repositories.ohlcv_repository import OhlcvRepository
from app.data.sources.base import DataSource, OhlcvBar
from app.domain.asset.calendar_guard import _MARKET_CALENDARS
from app.domain.asset.entity import Asset

logger = logging.getLogger(__name__)

MAX_RETRIES = 3
BACKOFF_BASE_SECONDS = 1.0  # 1, 2, 4 초 (attempt = 0, 1, 2)
DEFAULT_MAX_LOOKBACK_DAYS = 365 * 20  # 신규 자산 최초 백필 상한 — 약 20년


@dataclass(frozen=True)
class IngestionResult:
    """단일 자산 백필 결과 요약. 호출자(스케줄러/CLI) 가 집계 보고에 사용."""

    asset_id: int
    symbol: str
    market: str
    requested_start: date
    requested_end: date
    rows_inserted: int
    status: str  # OK / FAILED / PARTIAL / REJECTED
    error: str | None = None


def _trading_days(market: str, start: date, end: date) -> list[date]:
    """캘린더 레이어 방어 — 거래일 캘린더에 있는 날짜만 반환.

    CRYPTO 는 24/7 이라 [start, end] 의 모든 날짜를 거래일로 간주.
    KR/US 는 exchange_calendars 의 sessions_in_range 결과를 그대로 일자 변환.
    알 수 없는 market 코드는 빈 리스트 (호출자가 REJECTED 처리).
    """
    if market == "CRYPTO":
        days: list[date] = []
        cursor = start
        while cursor <= end:
            days.append(cursor)
            cursor = cursor + timedelta(days=1)
        return days
    cal_name = _MARKET_CALENDARS.get(market)
    if cal_name is None:
        return []
    cal = xcals.get_calendar(cal_name)
    sessions = cal.sessions_in_range(start.isoformat(), end.isoformat())
    return [pd_ts.date() for pd_ts in sessions]


def _resolve_start(latest: datetime | None, end: date, max_lookback_days: int) -> date:
    """ohlcv MAX(time) 으로부터 다음 백필 시작일을 계산.

    None (신규 자산) 이면 end - max_lookback_days. 이미 end 이후면 end + 1 반환
    (호출자가 'no-op' 으로 처리하도록).
    """
    if latest is None:
        return end - timedelta(days=max_lookback_days)
    return latest.date() + timedelta(days=1)


def _fetch_with_retry(
    source: DataSource, symbol: str, fetch_start: date, fetch_end: date
) -> tuple[list[OhlcvBar], Exception | None]:
    """자산 단위 3회 재시도 (1s → 2s → 4s 지수 백오프).

    Returns:
        (bars, last_error). 성공 시 (bars, None), 모두 실패 시 ([], 마지막 예외).
    """
    last_error: Exception | None = None
    for attempt in range(MAX_RETRIES):
        try:
            bars = source.fetch_ohlcv(symbol, fetch_start, fetch_end)
            return bars, None
        except Exception as exc:  # noqa: BLE001 - 외부 어댑터 경계, 모든 예외 흡수 후 재시도
            last_error = exc
            wait = BACKOFF_BASE_SECONDS * (2**attempt)
            logger.warning(
                "backfill retry %d/%d for %s: %s (wait %ss)",
                attempt + 1,
                MAX_RETRIES,
                symbol,
                exc,
                wait,
            )
            if attempt < MAX_RETRIES - 1:
                time.sleep(wait)
    return [], last_error


def backfill_asset(
    session: Session,
    source: DataSource,
    asset: Asset,
    end: date | None = None,
    max_lookback_days: int = DEFAULT_MAX_LOOKBACK_DAYS,
) -> IngestionResult:
    """단일 자산 증분 백필. 갭 감지 + 재시도 포함.

    절차:
      1. ohlcv MAX(time) 조회 → 다음날부터 시작. 신규 자산이면 max_lookback_days 만큼 과거부터.
      2. 거래일 캘린더 기준 [start, end] 의 expected_days 산출 (CRYPTO 는 모든 날짜).
      3. ohlcv 의 existing_dates 와 비교해 갭 감지.
      4. 갭이 있으면 source.fetch_ohlcv 호출 (close=0/null/NaN 거부는 어댑터 책임).
      5. 캘린더 외 날짜로 들어온 row 는 본 함수가 2차 필터링.
      6. UPSERT + assets.start_date / last_ingested_at 갱신.
      7. ingestion_log 1건 기록.

    예외는 가능한 모두 IngestionResult 로 변환해 호출자가 집계할 수 있게 한다.
    DB commit 은 호출자(backfill_active_assets) 가 자산 단위로 수행.
    """
    end = end or date.today()
    ohlcv_repo = OhlcvRepository(session)
    log_repo = IngestionLogRepository(session)
    asset_repo = SqlAssetRepository(session)

    latest = ohlcv_repo.latest_time(asset.asset_id)
    start = _resolve_start(latest, end, max_lookback_days)
    if start > end:
        # 이미 최신까지 적재되어 있는 상태. no-op 로 OK 기록.
        log_repo.record(asset.asset_id, start, end, "OK", 0)
        return IngestionResult(
            asset.asset_id, asset.symbol, asset.market, start, end, 0, "OK"
        )

    # 캘린더 레이어 1차 — expected_days 산출
    expected_days = _trading_days(asset.market, start, end)
    if not expected_days:
        # 시장 코드 미지원 또는 구간 내 거래일 0. no-op.
        log_repo.record(asset.asset_id, start, end, "OK", 0)
        return IngestionResult(
            asset.asset_id, asset.symbol, asset.market, start, end, 0, "OK"
        )

    expected_set = set(expected_days)
    existing = ohlcv_repo.existing_dates(asset.asset_id, start, end)
    missing = sorted(expected_set - existing)
    if not missing:
        # 갭 없음 — 멱등 no-op.
        log_repo.record(asset.asset_id, start, end, "OK", 0)
        return IngestionResult(
            asset.asset_id, asset.symbol, asset.market, start, end, 0, "OK"
        )

    fetch_start, fetch_end = missing[0], missing[-1]

    bars, last_error = _fetch_with_retry(source, asset.symbol, fetch_start, fetch_end)
    if last_error is not None:
        log_repo.record(
            asset.asset_id, fetch_start, fetch_end, "FAILED", 0, str(last_error)
        )
        return IngestionResult(
            asset.asset_id,
            asset.symbol,
            asset.market,
            fetch_start,
            fetch_end,
            0,
            "FAILED",
            str(last_error),
        )

    # 캘린더 레이어 2차 — source 가 비거래일 데이터를 반환했으면 필터링.
    valid_bars = [bar for bar in bars if bar.time.date() in expected_set]
    rejected = len(bars) - len(valid_bars)
    if rejected > 0:
        logger.warning(
            "calendar-layer rejected %d bars for %s (non-trading days)",
            rejected,
            asset.symbol,
        )

    rows = ohlcv_repo.upsert_bars(asset.asset_id, valid_bars)

    # assets 메타 갱신 (최초 백필이면 start_date 도 채움).
    if valid_bars:
        earliest = min(bar.time.date() for bar in valid_bars)
        latest_dt = max(bar.time for bar in valid_bars)
        asset_repo.update_ingestion_state(
            asset.asset_id,
            start_date=asset.start_date or earliest,
            last_ingested_at=latest_dt,
        )

    status = "OK" if rows == len(missing) else "PARTIAL"
    log_repo.record(asset.asset_id, fetch_start, fetch_end, status, rows)
    return IngestionResult(
        asset.asset_id,
        asset.symbol,
        asset.market,
        fetch_start,
        fetch_end,
        rows,
        status,
    )


def backfill_active_assets(
    session: Session,
    sources: dict[str, DataSource],
    end: date | None = None,
) -> list[IngestionResult]:
    """모든 active 자산 백필. 자산 1개 실패해도 잡 계속.

    Args:
        session: SQLAlchemy 세션. 자산 단위 commit/rollback 정책.
        sources: market 코드 → DataSource 라우팅
            (예: {"KR": PykrxSource(), "US": YfinanceSource(), "CRYPTO": YfinanceSource()}).
        end: 백필 종료 기준일. 기본 today.

    Returns:
        자산별 IngestionResult 리스트. status 별 집계는 호출자 책임.
    """
    asset_repo = SqlAssetRepository(session)
    results: list[IngestionResult] = []
    for asset in asset_repo.list_active():
        source = sources.get(asset.market)
        if source is None:
            results.append(
                IngestionResult(
                    asset.asset_id,
                    asset.symbol,
                    asset.market,
                    date.today(),
                    date.today(),
                    0,
                    "REJECTED",
                    f"no source for market={asset.market}",
                )
            )
            continue
        try:
            result = backfill_asset(session, source, asset, end=end)
            results.append(result)
            session.commit()
        except Exception as exc:  # noqa: BLE001 - 자산 단위 격리, 잡 전체 보호
            session.rollback()
            logger.exception(
                "uncaught error in backfill for asset_id=%d", asset.asset_id
            )
            results.append(
                IngestionResult(
                    asset.asset_id,
                    asset.symbol,
                    asset.market,
                    date.today(),
                    date.today(),
                    0,
                    "FAILED",
                    str(exc),
                )
            )
    return results
