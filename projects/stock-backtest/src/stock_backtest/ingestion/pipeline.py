"""증분 수집 파이프라인.

architecture.md §9 (데이터 수집 - DB 기반 증분) 및 §13 (비거래일 방어) 을 구현한다.

주요 흐름
---------
1. 자산의 최신 ``ohlcv.time`` 을 조회 → 그 다음 날짜부터 오늘까지를 요청 범위로 설정.
2. 거래일 캘린더(``backtest.calendar``)로 요청 범위 내 거래일만 필터링한다.
   (``CRYPTO`` 시장은 365일 전부를 거래일로 취급.)
3. :class:`DataSource.fetch_ohlcv` 를 호출. 실패 시 지수 백오프(1s→2s→4s)
   최대 3 회 재시도. :class:`RateLimitError` 뿐 아니라 일시적 :class:`DataSourceError`
   도 재시도 대상이며, :class:`SymbolNotFoundError` 는 즉시 SKIPPED 로 분류한다.
4. **품질 필터**: ``close`` 가 ``0``, ``None``, ``NaN`` 인 행은 제외하고
   ``ingestion_log`` 에 ``REJECTED`` 로 (자산 + 날짜 범위 + 사유) 기록한다.
   유효 행만 ``ohlcv`` 에 UPSERT.
5. 캘린더상 거래일이나 받아온 데이터에 없는 날짜 = **갭**. 별도 저장 없이
   ``MAX(time)`` 이 아직 이전 날짜로 남으므로 다음 실행에서 자연스럽게 재요청된다
   (단, 부분 갭인 경우 ``PARTIAL`` 로 표기).
6. 성공 시 ``ingestion_log`` 에 ``SUCCESS`` (또는 부분 성공 ``PARTIAL``)
   기록 및 ``assets.last_ingested_at`` 갱신.
7. 예외는 자산 단위로 격리되어 ``ingestion_log.error_message`` 에 기록되며
   시장 전체 잡은 계속 진행된다.
"""

from __future__ import annotations

import logging
import math
import time
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta, timezone
from typing import Any, Callable, Iterable, Mapping, Optional, Sequence

import pandas as pd

from ..backtest.calendar import (
    MarketNotSupportedError,
    get_trading_days,
)
from ..config import Settings
from ..data.models import Asset
from ..data.repository import (
    AssetRepository,
    IngestionLogRepository,
    OhlcvRepository,
)
from .base import (
    DataSource,
    DataSourceError,
    RateLimitError,
    SymbolNotFoundError,
)


logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# market (assets.market 값) → 거래일 캘린더 시장 코드 매핑.
# ``None`` 은 "거래일 캘린더로 매핑할 수 없어 SKIPPED 처리" 를 의미한다.
_CALENDAR_MARKET_MAP: dict[str, str | None] = {
    "KR": "KR",
    "KRX": "KR",
    "KOSPI": "KR",
    "KOSDAQ": "KR",
    "US": "US",
    "NYSE": "US",
    "NASDAQ": "US",
    "CRYPTO": "CRYPTO",
}

# market → DataSource 를 등록할 때 사용하는 정규화된 키도 동일 매핑으로 해석한다
# (IngestionPipeline 생성자에서 받는 sources 딕셔너리는 "market" 또는
# "source_name" 둘 다 허용).
_DEFAULT_BACKOFFS: tuple[float, ...] = (1.0, 2.0, 4.0)


# ---------------------------------------------------------------------------
# Result dataclass
# ---------------------------------------------------------------------------


Status = str  # Literal["SUCCESS", "PARTIAL", "FAILED", "SKIPPED"]


@dataclass
class IngestionResult:
    """단일 자산 수집 결과.

    Attributes
    ----------
    asset_id : int
        대상 자산 id.
    status : str
        ``SUCCESS`` | ``PARTIAL`` | ``FAILED`` | ``SKIPPED``
    rows_inserted : int
        실제 ``ohlcv`` 에 UPSERT 된 행 수.
    rows_rejected : int
        품질 필터에 의해 제외된 행 수(close=0/null/NaN).
    error_message : str | None
        ``FAILED`` / ``PARTIAL`` / ``SKIPPED`` 의 원인 메시지.
    requested_start, requested_end : date | None
        실제 소스에 요청한 기간. 거래일이 없어 SKIPPED 인 경우 None.
    """

    asset_id: int
    status: Status
    rows_inserted: int = 0
    rows_rejected: int = 0
    error_message: Optional[str] = None
    requested_start: Optional[date] = None
    requested_end: Optional[date] = None


# ---------------------------------------------------------------------------
# Pipeline
# ---------------------------------------------------------------------------


SessionFactory = Callable[[], Any]
"""세션 팩토리. ``sessionmaker(bind=engine)`` 또는 컨텍스트 매니저 반환 호출 가능."""


class IngestionPipeline:
    """증분 OHLCV 수집 파이프라인.

    Parameters
    ----------
    sources : Mapping[str, DataSource]
        키는 ``assets.market`` 값(예: ``"KR"``, ``"US"``, ``"CRYPTO"``)
        **또는** :attr:`DataSource.source_name` (예: ``"yfinance"``, ``"pykrx"``)
        둘 다 허용. 동일 자산에 대해 market 키가 우선 매칭된다.
    session_factory : Callable[[], Session]
        SQLAlchemy Session 을 생성하는 팩토리. 파이프라인은 각 자산 처리마다
        새 세션을 열고 닫는다.
    settings : Settings
        :func:`~stock_backtest.config.load_config` 결과. ``ingestion.retry_max``
        / ``ingestion.retry_backoff_seconds`` 를 사용한다.
    today_fn : Callable[[], date], optional
        "오늘" 을 반환하는 함수. 테스트에서 주입 용도.
    sleep_fn : Callable[[float], None], optional
        재시도 대기 함수. 테스트에서 시간 단축 목적으로 주입.
    """

    def __init__(
        self,
        sources: Mapping[str, DataSource],
        session_factory: SessionFactory,
        settings: Settings,
        *,
        today_fn: Callable[[], date] | None = None,
        sleep_fn: Callable[[float], None] | None = None,
    ) -> None:
        if not sources:
            raise ValueError("sources must be a non-empty mapping")
        self._sources: dict[str, DataSource] = dict(sources)
        self._session_factory = session_factory
        self._settings = settings
        self._today_fn = today_fn or (lambda: datetime.now(timezone.utc).date())
        self._sleep_fn = sleep_fn or time.sleep

        # Retry policy from settings with sensible fallback.
        self._retry_max: int = max(1, int(settings.ingestion.retry_max))
        backoffs = list(settings.ingestion.retry_backoff_seconds) or list(
            _DEFAULT_BACKOFFS
        )
        # 재시도 횟수만큼 backoff 목록을 pad/truncate.
        if len(backoffs) < self._retry_max:
            last = backoffs[-1] if backoffs else _DEFAULT_BACKOFFS[-1]
            backoffs = backoffs + [last] * (self._retry_max - len(backoffs))
        self._backoffs: tuple[float, ...] = tuple(backoffs[: self._retry_max])

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def run_for_asset(self, asset: Asset) -> IngestionResult:
        """단일 자산에 대해 증분 수집을 수행한다.

        예외는 자산 단위로 격리되어 :class:`IngestionResult` 로 반환된다.
        """
        try:
            return self._run_for_asset_inner(asset)
        except Exception as exc:  # pragma: no cover - 방어적 최후 방어선
            logger.exception(
                "IngestionPipeline: unexpected error for asset_id=%s symbol=%s",
                asset.asset_id,
                asset.symbol,
            )
            # best-effort log write; 실패해도 결과는 FAILED 로 반환.
            self._safe_log(
                asset_id=asset.asset_id,
                status="FAILED",
                rows=0,
                start=None,
                end=None,
                error=f"unexpected: {type(exc).__name__}: {exc}",
            )
            return IngestionResult(
                asset_id=asset.asset_id,
                status="FAILED",
                error_message=f"unexpected: {type(exc).__name__}: {exc}",
            )

    def run_for_market(self, market: str) -> list[IngestionResult]:
        """``market`` 의 모든 active 자산에 대해 순회 수집을 수행한다.

        한 자산의 실패가 다른 자산을 중단시키지 않는다.
        """
        assets = self._list_active_assets(market=market)
        logger.info(
            "IngestionPipeline.run_for_market market=%s assets=%d",
            market,
            len(assets),
        )
        results: list[IngestionResult] = []
        for asset in assets:
            results.append(self.run_for_asset(asset))
        return results

    # ------------------------------------------------------------------
    # Core logic
    # ------------------------------------------------------------------

    def _run_for_asset_inner(self, asset: Asset) -> IngestionResult:
        asset_id = asset.asset_id
        symbol = asset.symbol
        market = asset.market

        calendar_market = _CALENDAR_MARKET_MAP.get(market.upper())
        if calendar_market is None:
            msg = (
                f"market={market!r} has no calendar mapping; skipping "
                f"asset_id={asset_id} symbol={symbol!r}"
            )
            logger.warning("IngestionPipeline: %s", msg)
            self._safe_log(
                asset_id=asset_id,
                status="FAILED",
                rows=0,
                start=None,
                end=None,
                error=msg,
            )
            return IngestionResult(
                asset_id=asset_id, status="SKIPPED", error_message=msg
            )

        # 1) 요청 범위 결정.
        max_time = self._get_max_time(asset_id)
        today = self._today_fn()
        if max_time is not None:
            start_date = max_time.date() + timedelta(days=1)
        elif asset.start_date is not None:
            start_date = asset.start_date
        else:
            # 디폴트: 20년 백필. architecture.md 에 명시값은 없으나 안전한 상한.
            start_date = today - timedelta(days=365 * 20)

        end_date = today

        if start_date > end_date:
            # 이미 오늘까지 수집되어 있음.
            logger.debug(
                "asset_id=%s symbol=%s already up-to-date (max=%s today=%s)",
                asset_id,
                symbol,
                max_time,
                today,
            )
            return IngestionResult(
                asset_id=asset_id,
                status="SUCCESS",
                rows_inserted=0,
                rows_rejected=0,
                requested_start=None,
                requested_end=None,
                error_message=None,
            )

        # 2) 거래일 필터.
        try:
            trading_days = get_trading_days(calendar_market, start_date, end_date)
        except MarketNotSupportedError as exc:
            msg = f"calendar resolution failed: {exc}"
            logger.warning("IngestionPipeline: asset_id=%s %s", asset_id, msg)
            self._safe_log(
                asset_id=asset_id,
                status="FAILED",
                rows=0,
                start=start_date,
                end=end_date,
                error=msg,
            )
            return IngestionResult(
                asset_id=asset_id,
                status="SKIPPED",
                error_message=msg,
                requested_start=start_date,
                requested_end=end_date,
            )

        if len(trading_days) == 0:
            logger.debug(
                "asset_id=%s no trading days in range [%s, %s]; skipping",
                asset_id,
                start_date,
                end_date,
            )
            return IngestionResult(
                asset_id=asset_id,
                status="SUCCESS",
                rows_inserted=0,
                rows_rejected=0,
                requested_start=start_date,
                requested_end=end_date,
            )

        # 3) DataSource 선택 및 호출 (지수 백오프 재시도).
        source = self._resolve_source(asset)
        if source is None:
            msg = (
                f"no DataSource registered for market={market!r} "
                f"or source for symbol={symbol!r}"
            )
            logger.warning("IngestionPipeline: asset_id=%s %s", asset_id, msg)
            self._safe_log(
                asset_id=asset_id,
                status="FAILED",
                rows=0,
                start=start_date,
                end=end_date,
                error=msg,
            )
            return IngestionResult(
                asset_id=asset_id,
                status="SKIPPED",
                error_message=msg,
                requested_start=start_date,
                requested_end=end_date,
            )

        try:
            df = self._fetch_with_retry(
                source=source,
                symbol=symbol,
                market=market,
                start=start_date,
                end=end_date,
            )
        except SymbolNotFoundError as exc:
            msg = f"symbol not found: {exc}"
            logger.info("IngestionPipeline: asset_id=%s %s", asset_id, msg)
            self._safe_log(
                asset_id=asset_id,
                status="FAILED",
                rows=0,
                start=start_date,
                end=end_date,
                error=msg,
            )
            return IngestionResult(
                asset_id=asset_id,
                status="SKIPPED",
                error_message=msg,
                requested_start=start_date,
                requested_end=end_date,
            )
        except RateLimitError as exc:
            msg = f"rate limit (exhausted retries): {exc}"
            logger.warning("IngestionPipeline: asset_id=%s %s", asset_id, msg)
            self._safe_log(
                asset_id=asset_id,
                status="FAILED",
                rows=0,
                start=start_date,
                end=end_date,
                error=msg,
            )
            return IngestionResult(
                asset_id=asset_id,
                status="FAILED",
                error_message=msg,
                requested_start=start_date,
                requested_end=end_date,
            )
        except DataSourceError as exc:
            msg = f"data source error: {exc}"
            logger.warning("IngestionPipeline: asset_id=%s %s", asset_id, msg)
            self._safe_log(
                asset_id=asset_id,
                status="FAILED",
                rows=0,
                start=start_date,
                end=end_date,
                error=msg,
            )
            return IngestionResult(
                asset_id=asset_id,
                status="FAILED",
                error_message=msg,
                requested_start=start_date,
                requested_end=end_date,
            )

        # 4) 품질 필터 + UPSERT + 로그 + last_ingested_at 갱신.
        good_rows, rejected = self._apply_quality_filter(df)
        status, error_message = self._classify_status(
            trading_days=trading_days,
            good_rows=good_rows,
            rejected_count=len(rejected),
        )

        rows_inserted = self._persist(
            asset_id=asset_id,
            good_rows=good_rows,
            rejected=rejected,
            status=status,
            error_message=error_message,
            requested_start=start_date,
            requested_end=end_date,
        )

        logger.info(
            "IngestionPipeline: asset_id=%s symbol=%s market=%s status=%s "
            "rows=%d rejected=%d range=[%s..%s]",
            asset_id,
            symbol,
            market,
            status,
            rows_inserted,
            len(rejected),
            start_date,
            end_date,
        )

        return IngestionResult(
            asset_id=asset_id,
            status=status,
            rows_inserted=rows_inserted,
            rows_rejected=len(rejected),
            error_message=error_message,
            requested_start=start_date,
            requested_end=end_date,
        )

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _resolve_source(self, asset: Asset) -> Optional[DataSource]:
        """asset.market 또는 source_name 기준으로 DataSource 를 선택한다."""
        # 1) 정확한 market 키 매칭 (대소문자 무관).
        for key, src in self._sources.items():
            if key.upper() == asset.market.upper():
                return src
        # 2) source_name 매칭 (sources 딕셔너리 키가 source_name 인 경우).
        #    asset.meta 에 "source" 힌트가 있으면 우선.
        meta_source = None
        try:
            meta_source = asset.meta.get("source") if asset.meta else None
        except AttributeError:
            meta_source = None
        if meta_source is not None:
            for key, src in self._sources.items():
                if key == meta_source or src.source_name == meta_source:
                    return src
        # 3) 단일 source 만 등록된 경우 기본 사용.
        if len(self._sources) == 1:
            return next(iter(self._sources.values()))
        return None

    def _fetch_with_retry(
        self,
        source: DataSource,
        symbol: str,
        market: str,
        start: date,
        end: date,
    ) -> pd.DataFrame:
        """소스 호출을 최대 ``retry_max`` 회 재시도한다.

        :class:`RateLimitError` 와 일반 :class:`DataSourceError` 만 재시도 대상.
        :class:`SymbolNotFoundError` 는 즉시 전파한다.
        """
        last_exc: Exception | None = None
        for attempt in range(self._retry_max):
            try:
                return source.fetch_ohlcv(
                    symbol=symbol, market=market, start=start, end=end
                )
            except SymbolNotFoundError:
                raise
            except (RateLimitError, DataSourceError) as exc:
                last_exc = exc
                backoff = self._backoffs[attempt]
                logger.warning(
                    "IngestionPipeline: fetch failed "
                    "(symbol=%s attempt=%d/%d backoff=%.1fs): %s",
                    symbol,
                    attempt + 1,
                    self._retry_max,
                    backoff,
                    exc,
                )
                if attempt + 1 >= self._retry_max:
                    break
                self._sleep_fn(backoff)
        assert last_exc is not None
        raise last_exc

    @staticmethod
    def _apply_quality_filter(
        df: pd.DataFrame,
    ) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
        """``close`` 가 0/NaN/None 인 행을 걸러낸다.

        Returns
        -------
        (good_rows, rejected_rows)
            두 리스트 모두 dict 형태. ``rejected_rows`` 에는 사유(``_reason``)
            컬럼이 포함된다.
        """
        if df is None or df.empty:
            return [], []

        good: list[dict[str, Any]] = []
        bad: list[dict[str, Any]] = []
        for rec in df.to_dict(orient="records"):
            close = rec.get("close")
            reason = None
            if close is None:
                reason = "close is None"
            else:
                try:
                    cf = float(close)
                except (TypeError, ValueError):
                    reason = f"close not numeric ({close!r})"
                    cf = None
                if reason is None:
                    if cf is not None and math.isnan(cf):
                        reason = "close is NaN"
                    elif cf == 0.0:
                        reason = "close is zero"
            if reason is not None:
                rec_copy = dict(rec)
                rec_copy["_reason"] = reason
                bad.append(rec_copy)
            else:
                good.append(rec)
        return good, bad

    @staticmethod
    def _classify_status(
        trading_days: pd.DatetimeIndex,
        good_rows: Sequence[dict[str, Any]],
        rejected_count: int,
    ) -> tuple[Status, Optional[str]]:
        """수집 결과를 SUCCESS / PARTIAL 로 분류.

        - 유효 행이 거래일 수와 같음 → SUCCESS (rejected 무시)
        - 유효 행 < 거래일 수 && rejected_count > 0 → PARTIAL (품질 이슈)
        - 유효 행 < 거래일 수 && rejected_count == 0 → PARTIAL (갭 존재)
        - 유효 행이 0 인 경우는 호출자가 FAILED 로 분류할 수도 있으나,
          "거래일 캘린더와 소스가 모두 비어 있음" 케이스는 SUCCESS(0) 로
          이미 상위에서 return 되므로 여기 도달 시엔 갭으로 본다.
        """
        expected = len(trading_days)
        good = len(good_rows)
        if expected == 0 and good == 0:
            return ("SUCCESS", None)
        if good >= expected and rejected_count == 0:
            return ("SUCCESS", None)
        reasons: list[str] = []
        if good < expected:
            reasons.append(f"gap: expected={expected} received={good}")
        if rejected_count > 0:
            reasons.append(f"rejected={rejected_count}")
        return ("PARTIAL", "; ".join(reasons) if reasons else None)

    def _persist(
        self,
        asset_id: int,
        good_rows: Sequence[dict[str, Any]],
        rejected: Sequence[dict[str, Any]],
        status: Status,
        error_message: Optional[str],
        requested_start: date,
        requested_end: date,
    ) -> int:
        """UPSERT + ingestion_log 기록 + last_ingested_at 갱신을 한 트랜잭션에서."""
        session = self._session_factory()
        # session_factory 가 context manager 를 반환하는 패턴도 지원.
        is_cm = hasattr(session, "__enter__") and hasattr(session, "__exit__")
        if is_cm:
            session = session.__enter__()
        try:
            ohlcv_repo = OhlcvRepository(session)
            log_repo = IngestionLogRepository(session)
            asset_repo = AssetRepository(session)

            # REJECTED 로그 먼저 기록 (있다면).
            if rejected:
                dates = [self._row_date(r) for r in rejected if self._row_date(r)]
                rej_start = min(dates) if dates else requested_start
                rej_end = max(dates) if dates else requested_end
                reasons = sorted({r.get("_reason", "unknown") for r in rejected})
                log_repo.log(
                    asset_id=asset_id,
                    requested_start=rej_start,
                    requested_end=rej_end,
                    status="REJECTED",
                    rows_inserted=0,
                    error_message=(f"rejected={len(rejected)} rows; reasons={reasons}"),
                )

            rows_inserted = 0
            if good_rows:
                rows_inserted = ohlcv_repo.upsert_bulk(asset_id, list(good_rows))

            log_repo.log(
                asset_id=asset_id,
                requested_start=requested_start,
                requested_end=requested_end,
                status=status,
                rows_inserted=rows_inserted,
                error_message=error_message,
            )

            if rows_inserted > 0:
                asset_repo.update_last_ingested(asset_id, datetime.now(timezone.utc))

            session.commit()
            return rows_inserted
        except Exception:
            try:
                session.rollback()
            except Exception:  # pragma: no cover - 세션 상태 보호
                pass
            raise
        finally:
            if is_cm:
                session.__exit__(None, None, None)
            else:
                try:
                    session.close()
                except Exception:  # pragma: no cover
                    pass

    def _get_max_time(self, asset_id: int) -> Optional[datetime]:
        session = self._session_factory()
        is_cm = hasattr(session, "__enter__") and hasattr(session, "__exit__")
        if is_cm:
            session = session.__enter__()
        try:
            return OhlcvRepository(session).get_max_time(asset_id)
        finally:
            if is_cm:
                session.__exit__(None, None, None)
            else:
                try:
                    session.close()
                except Exception:  # pragma: no cover
                    pass

    def _list_active_assets(self, market: Optional[str]) -> list[Asset]:
        session = self._session_factory()
        is_cm = hasattr(session, "__enter__") and hasattr(session, "__exit__")
        if is_cm:
            session = session.__enter__()
        try:
            return AssetRepository(session).list_active(market=market)
        finally:
            if is_cm:
                session.__exit__(None, None, None)
            else:
                try:
                    session.close()
                except Exception:  # pragma: no cover
                    pass

    def _safe_log(
        self,
        asset_id: Optional[int],
        status: Status,
        rows: int,
        start: Optional[date],
        end: Optional[date],
        error: Optional[str],
    ) -> None:
        """ingestion_log 기록을 best-effort 로 수행. 실패해도 전파하지 않는다."""
        try:
            session = self._session_factory()
            is_cm = hasattr(session, "__enter__") and hasattr(session, "__exit__")
            if is_cm:
                session = session.__enter__()
            try:
                IngestionLogRepository(session).log(
                    asset_id=asset_id,
                    requested_start=start,
                    requested_end=end,
                    status=status,
                    rows_inserted=rows,
                    error_message=error,
                )
                session.commit()
            finally:
                if is_cm:
                    session.__exit__(None, None, None)
                else:
                    try:
                        session.close()
                    except Exception:  # pragma: no cover
                        pass
        except Exception:  # pragma: no cover - 로그 기록 실패는 삼킨다
            logger.exception(
                "IngestionPipeline: failed to write ingestion_log (asset_id=%s)",
                asset_id,
            )

    @staticmethod
    def _row_date(row: Mapping[str, Any]) -> Optional[date]:
        """row["time"] 을 ``date`` 로 정규화."""
        t = row.get("time")
        if t is None:
            return None
        if isinstance(t, pd.Timestamp):
            return t.date()
        if isinstance(t, datetime):
            return t.date()
        if isinstance(t, date):
            return t
        try:
            return pd.Timestamp(t).date()
        except Exception:
            return None


__all__ = ["IngestionPipeline", "IngestionResult"]
