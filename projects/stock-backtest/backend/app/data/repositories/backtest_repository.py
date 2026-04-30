"""BacktestRun/Equity/Trade/Metric ORM CRUD.

API/services 가 ORM 을 직접 사용하지 않도록 SQLAlchemy 접근을 본 모듈에 캡슐화한다
(asset_repository.py / ohlcv_repository.py 와 동일 정책).

run_hash 캐싱은 architecture.md V3 § "캐싱" L165-167 (V1 살림) 근거 — 동일 입력 재실행
시 기존 run 반환으로 중복 백테스트 방지.
"""

from __future__ import annotations

import hashlib
import json
from datetime import date, datetime
from decimal import Decimal
from typing import Any, Iterable

from sqlalchemy import desc, func, select
from sqlalchemy.orm import Session

from app.models.backtest import (
    BacktestEquity,
    BacktestMetric,
    BacktestRun,
    BacktestTrade,
)


def compute_run_hash(
    strategy_name: str,
    params: dict[str, Any],
    universe: Iterable[int],
    period_start: date,
    period_end: date,
    base_currency: str,
) -> str:
    """캐싱용 결정적 해시.

    universe 는 내부에서 sorted — 동일 자산 묶음이면 입력 순서 무관하게 같은 hash.
    Decimal 등 직렬화 어려운 타입은 default=str 로 fallback.
    sha256 의 앞 32자 (128bit) — UNIQUE 제약 충족 + DB 컬럼 폭(64) 여유.
    """
    payload = json.dumps(
        {
            "s": strategy_name,
            "p": params,
            "u": sorted(universe),
            "ps": str(period_start),
            "pe": str(period_end),
            "bc": base_currency,
        },
        sort_keys=True,
        default=str,
    )
    return hashlib.sha256(payload.encode()).hexdigest()[:32]


class BacktestRepository:
    """backtest_runs / backtest_equity / backtest_trades / backtest_metrics 4 테이블
    접근을 한 곳에 모은다.

    cascade 삭제 (ondelete=CASCADE) 가 ORM 레벨에서 정의되어 있으므로 delete_run 1회로
    하위 결과 row 도 함께 정리된다 (models/backtest.py).
    """

    def __init__(self, session: Session):
        self._session = session

    # ----- BacktestRun -----------------------------------------------------

    def create_run(
        self,
        *,
        run_hash: str,
        strategy_name: str,
        params: dict[str, Any],
        universe: list[int],
        period_start: date,
        period_end: date,
        base_currency: str,
        market_mode: str = "STOCK",
    ) -> BacktestRun:
        """status='pending' 으로 신규 row 삽입. flush 후 run_id 보장."""
        # universe 는 JSONB 컬럼이라 list[int] 그대로 직렬화됨.
        run = BacktestRun(
            run_hash=run_hash,
            strategy_name=strategy_name,
            params=params,
            universe=universe,
            period_start=period_start,
            period_end=period_end,
            base_currency=base_currency,
            market_mode=market_mode,
            status="pending",
            progress=0.0,
            cancel_requested=False,
        )
        self._session.add(run)
        self._session.flush()
        return run

    def find_run(self, run_id: int) -> BacktestRun | None:
        return self._session.get(BacktestRun, run_id)

    def find_by_hash(self, run_hash: str) -> BacktestRun | None:
        return self._session.execute(
            select(BacktestRun).where(BacktestRun.run_hash == run_hash)
        ).scalar_one_or_none()

    def update_status(
        self,
        run_id: int,
        *,
        status: str | None = None,
        progress: float | None = None,
        error_json: dict[str, Any] | None = None,
        started_at: datetime | None = None,
        finished_at: datetime | None = None,
    ) -> None:
        """부분 업데이트 — None 인 필드는 변경하지 않는다 (서비스 계층에서 호출 빈도 高)."""
        run = self._session.get(BacktestRun, run_id)
        if run is None:
            return
        if status is not None:
            run.status = status
        if progress is not None:
            run.progress = progress
        if error_json is not None:
            run.error_json = error_json
        if started_at is not None:
            run.started_at = started_at
        if finished_at is not None:
            run.finished_at = finished_at
        self._session.flush()

    def request_cancel(self, run_id: int) -> bool:
        """DELETE 호출이 pending/running run 에 들어왔을 때 cancel 플래그 set.

        엔진 루프(BacktestRunContext.cancel_check) 가 폴링하여 abort.
        이미 종료된 run (done/failed/cancelled) 에는 무효.
        """
        run = self._session.get(BacktestRun, run_id)
        if run is None or run.status not in ("pending", "running"):
            return False
        run.cancel_requested = True
        self._session.flush()
        return True

    def is_cancel_requested(self, run_id: int) -> bool:
        run = self._session.get(BacktestRun, run_id)
        return bool(run and run.cancel_requested)

    def list_runs(self, limit: int = 50, offset: int = 0) -> list[BacktestRun]:
        """최근 created_at 역순. UI 이력 화면 용도."""
        return list(
            self._session.execute(
                select(BacktestRun)
                .order_by(desc(BacktestRun.created_at))
                .limit(limit)
                .offset(offset)
            )
            .scalars()
            .all()
        )

    def count_runs(self) -> int:
        """`list_runs(...)` 와 동일 필터(전체 — list_runs 자체에 필터 없음) 의 row 수.

        TASK-234: PaginatedResponse.total 정확화 — limit/offset 미적용 전체 카운트.
        list_runs 가 추후 필터(status 등) 를 받게 되면 이 함수도 동일 시그니처로 확장한다.
        """
        return int(
            self._session.execute(
                select(func.count()).select_from(BacktestRun)
            ).scalar_one()
        )

    def delete_run(self, run_id: int) -> bool:
        """cascade 로 equity/trades/metrics 함께 삭제 (models/backtest.py FK ondelete)."""
        run = self._session.get(BacktestRun, run_id)
        if run is None:
            return False
        self._session.delete(run)
        self._session.flush()
        return True

    # ----- BacktestEquity --------------------------------------------------

    def insert_equity_points(
        self,
        run_id: int,
        points: list[tuple[datetime, Decimal, Decimal, Decimal]],
    ) -> int:
        """equity 시계열 일괄 적재.

        Args:
            points: [(time, equity, cash, drawdown), ...].

        Returns:
            적재 시도된 row 수.
        """
        rows = [
            BacktestEquity(
                run_id=run_id,
                time=t,
                equity=e,
                cash=c,
                drawdown=d,
            )
            for t, e, c, d in points
        ]
        if not rows:
            return 0
        self._session.add_all(rows)
        self._session.flush()
        return len(rows)

    def get_equity(self, run_id: int) -> list[BacktestEquity]:
        return list(
            self._session.execute(
                select(BacktestEquity)
                .where(BacktestEquity.run_id == run_id)
                .order_by(BacktestEquity.time)
            )
            .scalars()
            .all()
        )

    # ----- BacktestTrade ---------------------------------------------------

    def insert_trades(self, run_id: int, trades: list[dict[str, Any]]) -> int:
        """매매 체결 일괄 적재. trades 는 dict (time/asset_id/side/qty/price/commission/currency)."""
        rows = [BacktestTrade(run_id=run_id, **t) for t in trades]
        if not rows:
            return 0
        self._session.add_all(rows)
        self._session.flush()
        return len(rows)

    def get_trades(self, run_id: int) -> list[BacktestTrade]:
        return list(
            self._session.execute(
                select(BacktestTrade)
                .where(BacktestTrade.run_id == run_id)
                .order_by(BacktestTrade.time)
            )
            .scalars()
            .all()
        )

    # ----- BacktestMetric --------------------------------------------------

    def insert_metrics(self, run_id: int, metrics: dict[str, float]) -> int:
        """metric_name → value 적재. (run_id, metric_name) UNIQUE 보장 (models)."""
        rows = [
            BacktestMetric(run_id=run_id, metric_name=name, value=Decimal(str(value)))
            for name, value in metrics.items()
        ]
        if not rows:
            return 0
        self._session.add_all(rows)
        self._session.flush()
        return len(rows)

    def get_metrics(self, run_id: int) -> dict[str, float]:
        rows = (
            self._session.execute(
                select(BacktestMetric).where(BacktestMetric.run_id == run_id)
            )
            .scalars()
            .all()
        )
        return {m.metric_name: float(m.value) for m in rows}
