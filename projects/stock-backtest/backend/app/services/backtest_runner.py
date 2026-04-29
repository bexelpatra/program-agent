"""백그라운드 백테스트 실행자 (비동기 job 모델).

architecture.md V3 § "비동기 job 실행 모델" L437-446 + V2 § "에러 응답 계약" L450 근거.

흐름:
    1. API 라우터가 BacktestRun row 를 status='pending' 으로 만들고 즉시 반환.
    2. FastAPI BackgroundTasks 가 별도 thread 에서 execute_backtest_job(run_id) 호출.
    3. 진행률 (engine.progress_callback) → backtest_runs.progress 갱신 (별도 세션).
    4. 취소 (DB 플래그 cancel_requested) → engine.cancel_check 가 폴링 → abort.
    5. 실패 시 error_json 에 {stage, type, message, request_ctx, trace_id} 적재.

세션 정책:
    - 메인 thread 가 SessionLocal() 한 개 — 전체 job 의 트랜잭션 boundary.
    - progress_callback / cancel_check 는 short-lived 별도 세션 — long-running job
      메인 트랜잭션이 lock 잡고 있는 동안에도 외부에서 cancel 갱신 가능하게 함.
"""

from __future__ import annotations

import logging
import traceback
import uuid
from datetime import date, datetime, timezone
from decimal import Decimal
from typing import Any

from app.core.db import SessionLocal
from app.data.repositories.backtest_repository import BacktestRepository
from app.domain.allocators import (
    AllWeather,
    AllWeatherParams,
    EqualWeight,
    EqualWeightParams,
    FixedWeight,
    FixedWeightParams,
)
from app.domain.engine import BacktestRunContext, run_backtest
from app.domain.filters import (
    Momentum,
    MomentumParams,
    MovingAverage,
    MovingAverageParams,
)
from app.domain.metrics import compute_metrics
from app.domain.strategy import Strategy
from app.services.data_loader import build_backtest_context

_logger = logging.getLogger(__name__)


# 카탈로그 (allocator/filter name → (구현 클래스, params 클래스)).
# strategies.py API 가 노출하는 name 과 동기.
_ALLOCATORS: dict[str, tuple[type, type]] = {
    "fixed_weight": (FixedWeight, FixedWeightParams),
    "all_weather": (AllWeather, AllWeatherParams),
    "equal_weight": (EqualWeight, EqualWeightParams),
}

_FILTERS: dict[str, tuple[type, type]] = {
    "moving_average": (MovingAverage, MovingAverageParams),
    "momentum": (Momentum, MomentumParams),
}


def build_strategy_from_config(strategy_config: dict[str, Any]) -> Strategy:
    """API 입력 dict (StrategyConfig.model_dump()) → 도메인 Strategy 객체.

    각 allocator/filter 의 Pydantic params_schema 가 params 검증 — 잘못된 키/타입은
    여기서 ValidationError 로 노출되어 API 가 422 로 매핑.
    """
    allocator_name = strategy_config["allocator_name"]
    if allocator_name not in _ALLOCATORS:
        raise ValueError(
            f"unknown allocator: {allocator_name} (allowed: {list(_ALLOCATORS)})"
        )
    AllocCls, AllocParams = _ALLOCATORS[allocator_name]
    allocator = AllocCls(AllocParams(**strategy_config["allocator_params"]))

    signal_filters: list[Any] = []
    for fc in strategy_config.get("filter_configs") or []:
        fname = fc["name"]
        if fname not in _FILTERS:
            raise ValueError(
                f"unknown filter: {fname} (allowed: {list(_FILTERS)})"
            )
        FilterCls, FilterParams = _FILTERS[fname]
        signal_filters.append(FilterCls(FilterParams(**(fc.get("params") or {}))))

    return Strategy(
        name=allocator_name,
        allocator=allocator,
        signal_filters=tuple(signal_filters),
        rebalance_schedule=strategy_config.get("rebalance_schedule", "monthly"),
    )


def _make_progress_callback(run_id: int):
    """별도 SessionLocal 로 progress 만 갱신 — 메인 세션의 long-running 트랜잭션 영향 회피."""

    def _progress(p: float) -> None:
        with SessionLocal() as session:
            BacktestRepository(session).update_status(run_id, progress=float(p))
            session.commit()

    return _progress


def _make_cancel_check(run_id: int):
    """별도 SessionLocal 로 cancel 플래그 폴링."""

    def _cancel_check() -> bool:
        with SessionLocal() as session:
            return BacktestRepository(session).is_cancel_requested(run_id)

    return _cancel_check


def _record_failure(
    run_id: int,
    *,
    stage: str,
    exc: BaseException,
    trace_id: str,
) -> None:
    """별도 세션으로 status='failed' + error_json 기록.

    메인 세션이 예외로 인해 rollback 된 상태일 수 있어 새 세션을 사용한다.
    error_json 형식은 V2 § 에러 응답 계약 (stage/type/message/request_ctx/trace_id).
    """
    with SessionLocal() as session:
        repo = BacktestRepository(session)
        repo.update_status(
            run_id,
            status="failed",
            progress=1.0,
            finished_at=datetime.now(timezone.utc),
            error_json={
                "stage": stage,
                "type": type(exc).__name__,
                "message": str(exc),
                "request_ctx": {"run_id": run_id},
                "trace_id": trace_id,
                "stacktrace": traceback.format_exc(),
            },
        )
        session.commit()


def _persist_results(
    run_id: int,
    result: Any,
    base_currency: str,
) -> None:
    """엔진 결과 → equity/trades/metrics 적재 + status='done|cancelled' 마무리."""
    with SessionLocal() as session:
        repo = BacktestRepository(session)

        # equity_curve: BacktestEquityPoint(time=date, equity, cash_total_in_base).
        # drawdown 은 본 단계에서 즉석 계산 (peak 추적). models.BacktestEquity.time 은
        # DateTime(timezone=True) 라 date → datetime(UTC midnight) 변환.
        equity_rows: list[tuple[datetime, Decimal, Decimal, Decimal]] = []
        peak = Decimal("0")
        for point in result.equity_curve:
            equity_value = Decimal(point.equity)
            if equity_value > peak:
                peak = equity_value
            drawdown = (
                (equity_value / peak - Decimal("1")) if peak > Decimal("0") else Decimal("0")
            )
            time_dt = datetime.combine(point.time, datetime.min.time(), tzinfo=timezone.utc)
            equity_rows.append(
                (time_dt, equity_value, Decimal(point.cash_total_in_base), drawdown)
            )
        repo.insert_equity_points(run_id, equity_rows)

        # trades: TradeFill 은 time 미보유 (도메인은 시점을 settlement_d 로 알고 있으나
        # fill 객체에는 적재 안 됨) — 현재 시각 fallback. 향후 engine 이 settlement_d 를
        # fill 에 첨부하면 그 값을 사용하도록 개선 (다음 제안에 명시).
        now = datetime.now(timezone.utc)
        trade_dicts: list[dict[str, Any]] = []
        for fill in result.fills:
            trade_dicts.append(
                {
                    "time": getattr(fill, "time", now),
                    "asset_id": fill.asset_id,
                    "side": fill.side,
                    "qty": Decimal(fill.qty_filled),
                    "price": Decimal(fill.price),
                    "commission": Decimal(fill.commission),
                    "currency": fill.currency,
                }
            )
        repo.insert_trades(run_id, trade_dicts)

        # metrics: equity 시계열에서 계산. annual/monthly 는 별도 metric_name pattern 으로
        # 적재해 향후 단순 query 로 분리 가능 (annual_return_2024 / monthly_return_2024-01).
        equity_series_for_metrics = [
            (point.time, Decimal(point.equity)) for point in result.equity_curve
        ]
        metrics = compute_metrics(equity_series_for_metrics)
        flat_metrics: dict[str, float] = {
            "cagr": metrics.cagr,
            "mdd": metrics.mdd,
            "sharpe": metrics.sharpe,
            "sortino": metrics.sortino,
            "calmar": metrics.calmar,
            "win_rate": metrics.win_rate,
        }
        for year, ret in metrics.annual_returns.items():
            flat_metrics[f"annual_return_{year}"] = ret
        for ym, ret in metrics.monthly_returns.items():
            flat_metrics[f"monthly_return_{ym}"] = ret
        repo.insert_metrics(run_id, flat_metrics)

        final_status = "cancelled" if result.aborted else "done"
        repo.update_status(
            run_id,
            status=final_status,
            progress=1.0,
            finished_at=datetime.now(timezone.utc),
        )
        session.commit()


def execute_backtest_job(run_id: int) -> None:
    """백그라운드 thread entry (FastAPI BackgroundTasks 가 호출).

    실패 시 status='failed' + error_json 기록 후 swallow — BackgroundTasks 는 예외를
    재전파해도 클라이언트가 알 길이 없으므로 (이미 응답 보낸 후) DB 에 남기는 게 유일한
    수단.

    데이터 로더 (TASK-100 통합 완료):
        services.data_loader.build_backtest_context 가 ohlcv → prices_aligned + fx_rates →
        fx_rates_to_base + assets → universe_market_meta 를 일괄 구성한다. ohlcv 백필이
        부재한 자산이 universe 에 포함되면 prices_aligned 컬럼이 전부 NaN 이 되어
        run_backtest 가 stage='run_engine' 에서 ValueError 로 종료된다.
    """
    trace_id = uuid.uuid4().hex
    stage = "init"

    with SessionLocal() as session:
        repo = BacktestRepository(session)
        run = repo.find_run(run_id)
        if run is None:
            _logger.error(
                "execute_backtest_job: run_id=%d not found trace_id=%s",
                run_id,
                trace_id,
            )
            return

        try:
            stage = "starting"
            repo.update_status(
                run_id,
                status="running",
                started_at=datetime.now(timezone.utc),
            )
            session.commit()

            stage = "build_strategy"
            strategy = build_strategy_from_config(run.params.get("strategy", run.params))

            stage = "build_context"
            initial_cash_raw = run.params.get("initial_cash") or {"KRW": 10_000_000}
            initial_cash = {
                ccy: Decimal(str(amt)) for ccy, amt in initial_cash_raw.items()
            }
            # universe 는 list[int] (create_run 호출자가 그렇게 넘김).
            universe_ids: list[int] = list(run.universe or [])

            stage = "load_market_data"
            prices_aligned, universe_market_meta, fx_rates_to_base = (
                build_backtest_context(
                    session=session,
                    asset_ids=universe_ids,
                    base_currency=run.base_currency,
                    period_start=run.period_start,
                    period_end=run.period_end,
                )
            )

            stage = "build_context"
            ctx = BacktestRunContext(
                base_currency=run.base_currency,
                period_start=run.period_start,
                period_end=run.period_end,
                initial_cash=initial_cash,
                universe_market_meta=universe_market_meta,
                prices_aligned=prices_aligned,
                fx_rates_to_base=fx_rates_to_base,
                strategy=strategy,
                progress_callback=_make_progress_callback(run_id),
                cancel_check=_make_cancel_check(run_id),
            )

            stage = "run_engine"
            try:
                result = run_backtest(ctx)
            except ValueError as exc:
                # 데이터 부재 (universe 의 ohlcv 백필 누락, fx 환율 누락 등) 로 인한
                # 종료를 일반 예외 path 와 동일하게 status='failed' + error_json 으로 마무리.
                _logger.warning(
                    "run_id=%d engine refused due to data gap: %s trace_id=%s",
                    run_id,
                    exc,
                    trace_id,
                )
                _record_failure(
                    run_id, stage="run_engine", exc=exc, trace_id=trace_id
                )
                return

            stage = "persist_results"
            _persist_results(run_id, result, run.base_currency)

            _logger.info(
                "run_id=%d completed status=%s trace_id=%s",
                run_id,
                "cancelled" if result.aborted else "done",
                trace_id,
            )

        except Exception as exc:  # noqa: BLE001 — 백그라운드 job 의 last-resort
            _logger.exception(
                "run_id=%d failed at stage=%s trace_id=%s",
                run_id,
                stage,
                trace_id,
            )
            session.rollback()
            _record_failure(run_id, stage=stage, exc=exc, trace_id=trace_id)
