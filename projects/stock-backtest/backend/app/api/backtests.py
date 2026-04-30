"""백테스트 비동기 job API.

architecture.md V3 § "비동기 job 실행 모델" L437-446 + § "V2 API" L425-434 + V2 §
"에러 응답 계약" L450 (전역 핸들러 _error.py 가 처리) 근거.

엔드포인트:
    - POST   /api/backtests              — job 생성 (즉시 pending 반환 + 백그라운드 실행)
    - GET    /api/backtests/{run_id}     — 상태 조회 (status/progress/error)
    - GET    /api/backtests/{run_id}/result — 결과 (status='done' 일 때만)
    - DELETE /api/backtests/{run_id}     — 취소 (pending/running) 또는 삭제 (그 외)
    - GET    /api/backtests              — 이력 (최근 created_at 역순)

라우터는 얇게 — 비즈니스 로직은 services/backtest_runner.py + data/repositories/
backtest_repository.py 에 위임.
"""

from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query, Response
from sqlalchemy.orm import Session

from app.api.health import COMMON_ERROR_RESPONSES
from app.data.repositories.backtest_repository import (
    BacktestRepository,
    compute_run_hash,
)
from app.dependencies import get_db
from app.models.backtest import BacktestRun
from app.schemas.backtest import (
    BacktestCreate,
    BacktestResult,
    BacktestRun as BacktestRunSchema,
    EquityPoint,
    MetricsPayload,
    TradeRecord,
)
from app.schemas.common import PaginatedResponse
from app.services.backtest_runner import execute_backtest_job

router = APIRouter(prefix="/api/backtests", tags=["backtests"])


def _to_run_schema(run: BacktestRun, name: str | None = None) -> BacktestRunSchema:
    """ORM BacktestRun → 응답 DTO 변환 (라우터에서만 사용).

    name 은 별도 컬럼이 없어 호출자가 전달 (POST 본문의 BacktestCreate.name 등).
    이력 list 에서는 None.
    """
    return BacktestRunSchema(
        run_id=run.run_id,
        run_hash=run.run_hash,
        status=run.status,  # type: ignore[arg-type]
        progress=float(run.progress),
        name=name,
        strategy_name=run.strategy_name,
        period_start=run.period_start,
        period_end=run.period_end,
        base_currency=run.base_currency,
        created_at=run.created_at,
        started_at=run.started_at,
        finished_at=run.finished_at,
        error=run.error_json,
    )


# ----- POST /api/backtests --------------------------------------------------


@router.post(
    "",
    response_model=BacktestRunSchema,
    status_code=201,
    summary="백테스트 job 생성 (즉시 pending 반환)",
    responses=COMMON_ERROR_RESPONSES,
)
def create_backtest(
    payload: BacktestCreate,
    background_tasks: BackgroundTasks,
    session: Session = Depends(get_db),
) -> BacktestRunSchema:
    """동일 run_hash 가 이미 있으면 기존 run 반환 (V1 § 캐싱 L165-167).

    그렇지 않으면 status='pending' 으로 row 삽입 + 백그라운드 작업 등록.
    """
    repo = BacktestRepository(session)

    # run_hash 입력에는 strategy 직렬화 + initial_cash 모두 포함 — 동일 전략·동일 자본만
    # 같은 hash. universe 는 compute_run_hash 가 sorted 처리.
    full_params = {
        "strategy": payload.strategy.model_dump(),
        "initial_cash": payload.initial_cash,
    }
    run_hash = compute_run_hash(
        payload.strategy.allocator_name,
        full_params,
        payload.universe_asset_ids,
        payload.period_start,
        payload.period_end,
        payload.base_currency,
    )

    existing = repo.find_by_hash(run_hash)
    if existing is not None:
        return _to_run_schema(existing, name=payload.name)

    run = repo.create_run(
        run_hash=run_hash,
        strategy_name=payload.strategy.allocator_name,
        params=full_params,
        universe=payload.universe_asset_ids,
        period_start=payload.period_start,
        period_end=payload.period_end,
        base_currency=payload.base_currency,
    )
    session.commit()

    # FastAPI BackgroundTasks 가 응답 후 별도 thread 에서 호출.
    background_tasks.add_task(execute_backtest_job, run.run_id)

    return _to_run_schema(run, name=payload.name)


# ----- GET /api/backtests/{run_id} -----------------------------------------


@router.get(
    "/{run_id}",
    response_model=BacktestRunSchema,
    summary="백테스트 job 상태 조회",
    responses=COMMON_ERROR_RESPONSES,
)
def get_backtest(
    run_id: int,
    session: Session = Depends(get_db),
) -> BacktestRunSchema:
    repo = BacktestRepository(session)
    run = repo.find_run(run_id)
    if run is None:
        raise HTTPException(status_code=404, detail=f"run_id={run_id} not found")
    return _to_run_schema(run)


# ----- GET /api/backtests/{run_id}/result ----------------------------------


@router.get(
    "/{run_id}/result",
    response_model=BacktestResult,
    summary="백테스트 결과 (equity/trades/metrics)",
    responses=COMMON_ERROR_RESPONSES,
)
def get_backtest_result(
    run_id: int,
    session: Session = Depends(get_db),
) -> BacktestResult:
    """status='done' 일 때만 호출. 그 외 (pending/running/failed/cancelled) 는 409."""
    repo = BacktestRepository(session)
    run = repo.find_run(run_id)
    if run is None:
        raise HTTPException(status_code=404, detail=f"run_id={run_id} not found")
    if run.status != "done":
        raise HTTPException(
            status_code=409,
            detail=(
                f"run_id={run_id} status={run.status}, not yet done — poll "
                f"GET /api/backtests/{run_id} until status='done'"
            ),
        )

    equity_rows = repo.get_equity(run_id)
    trade_rows = repo.get_trades(run_id)
    metrics_dict = repo.get_metrics(run_id)

    equity_curve = [
        EquityPoint(
            time=row.time.date() if hasattr(row.time, "date") else row.time,
            equity=float(row.equity),
            cash=float(row.cash),
            drawdown=float(row.drawdown),
        )
        for row in equity_rows
    ]
    trades = [
        TradeRecord(
            time=row.time,
            asset_id=row.asset_id,
            side=row.side,  # type: ignore[arg-type]
            qty=float(row.qty),
            price=float(row.price),
            commission=float(row.commission),
            currency=row.currency,
        )
        for row in trade_rows
    ]

    metrics: MetricsPayload | None
    if metrics_dict:
        # annual_return_YYYY / monthly_return_YYYY-MM 패턴 분리 → dict 재조립.
        annual_returns: dict[int, float] = {}
        monthly_returns: dict[str, float] = {}
        flat: dict[str, float] = {}
        for name, value in metrics_dict.items():
            if name.startswith("annual_return_"):
                try:
                    annual_returns[int(name.removeprefix("annual_return_"))] = value
                except ValueError:
                    continue
            elif name.startswith("monthly_return_"):
                monthly_returns[name.removeprefix("monthly_return_")] = value
            else:
                flat[name] = value
        metrics = MetricsPayload(
            cagr=flat.get("cagr", 0.0),
            mdd=flat.get("mdd", 0.0),
            sharpe=flat.get("sharpe", 0.0),
            sortino=flat.get("sortino", 0.0),
            calmar=flat.get("calmar", 0.0),
            win_rate=flat.get("win_rate", 0.0),
            annual_returns=annual_returns,
            monthly_returns=monthly_returns,
        )
    else:
        metrics = None

    return BacktestResult(
        run=_to_run_schema(run),
        equity_curve=equity_curve,
        trades=trades,
        metrics=metrics,
    )


# ----- DELETE /api/backtests/{run_id} --------------------------------------


@router.delete(
    "/{run_id}",
    status_code=204,
    summary="백테스트 취소 (pending/running) 또는 삭제 (그 외)",
    responses=COMMON_ERROR_RESPONSES,
)
def cancel_or_delete_backtest(
    run_id: int,
    session: Session = Depends(get_db),
) -> Response:
    """단일 DELETE 동사로 두 의미를 표현 (UI 가 휴지통 버튼 1개로 노출).

    - pending/running: cancel_requested=True 만 set. 엔진이 폴링 후 abort, 부분 결과
      는 보존 (status='cancelled' 로 마무리).
    - done/failed/cancelled: row 삭제 (cascade 로 결과도 함께).
    """
    repo = BacktestRepository(session)
    run = repo.find_run(run_id)
    if run is None:
        raise HTTPException(status_code=404, detail=f"run_id={run_id} not found")

    if run.status in ("pending", "running"):
        repo.request_cancel(run_id)
    else:
        repo.delete_run(run_id)
    session.commit()

    return Response(status_code=204)


# ----- GET /api/backtests ---------------------------------------------------


@router.get(
    "",
    response_model=PaginatedResponse[BacktestRunSchema],
    summary="백테스트 이력 (최근 created_at 역순)",
    responses=COMMON_ERROR_RESPONSES,
)
def list_backtests(
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    session: Session = Depends(get_db),
) -> PaginatedResponse[BacktestRunSchema]:
    repo = BacktestRepository(session)
    runs = repo.list_runs(limit=limit, offset=offset)
    page = (offset // limit) + 1 if limit > 0 else 1
    return PaginatedResponse(
        items=[_to_run_schema(r) for r in runs],
        total=len(runs),
        page=page,
        page_size=limit,
    )
