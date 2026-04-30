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
from datetime import datetime, timezone
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
    MaSignal,
    MaSignalParams,
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
    "ma_signal": (MaSignal, MaSignalParams),
}

_FILTERS: dict[str, tuple[type, type]] = {
    "moving_average": (MovingAverage, MovingAverageParams),
    "momentum": (Momentum, MomentumParams),
}


def _resolve_symbol_keys_to_asset_ids(params: dict[str, Any]) -> dict[str, Any]:
    """allocator_params 의 dict 형 비중 (예: weights={"BTC-USD": 0.5}) 에서
    string key (symbol) 를 asset_id (int) 로 자동 매핑.

    UI 가 AssetWeightMap 위젯 미구현 상태라 사용자가 symbol 로 입력하는 케이스 대응.
    동일 symbol 이 여러 market 에 존재하면 첫 일치 (active 우선) 사용.
    매핑 실패 symbol 은 ValueError.
    """
    from sqlalchemy import select

    from app.core.db import SessionLocal
    from app.models.asset import Asset

    if not isinstance(params.get("weights"), dict):
        return params

    weights = params["weights"]
    needs_resolve = [
        k for k in weights.keys() if isinstance(k, str) and not k.lstrip("-").isdigit()
    ]
    if not needs_resolve:
        return params

    with SessionLocal() as session:
        rows = (
            session.execute(select(Asset).where(Asset.symbol.in_(needs_resolve)))
            .scalars()
            .all()
        )
        symbol_to_id: dict[str, int] = {}
        for r in rows:
            # active 우선, 같은 symbol 이 여러 market 이면 첫 일치
            if r.symbol not in symbol_to_id or r.active:
                symbol_to_id[r.symbol] = r.asset_id

    missing = [s for s in needs_resolve if s not in symbol_to_id]
    if missing:
        raise ValueError(
            f"weights 의 symbol 을 자산 카탈로그에서 찾을 수 없습니다: {missing}. "
            f"자산 카탈로그(/assets)에서 먼저 등록하거나 정확한 ticker 를 사용하세요."
        )

    new_weights: dict[int, float] = {}
    for k, v in weights.items():
        if isinstance(k, str) and not k.lstrip("-").isdigit():
            new_weights[symbol_to_id[k]] = v
        else:
            new_weights[int(k)] = v

    return {**params, "weights": new_weights}


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
    raw_params = strategy_config["allocator_params"]
    resolved_params = _resolve_symbol_keys_to_asset_ids(raw_params)
    allocator = AllocCls(AllocParams(**resolved_params))

    signal_filters: list[Any] = []
    for fc in strategy_config.get("filter_configs") or []:
        fname = fc["name"]
        if fname not in _FILTERS:
            raise ValueError(f"unknown filter: {fname} (allowed: {list(_FILTERS)})")
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


def _build_equity_rows(
    equity_curve: list[Any],
) -> list[tuple[datetime, Decimal, Decimal, Decimal]]:
    """equity_curve → backtest_equity insert rows (peak 추적 + drawdown 즉석 계산).

    equity_curve 는 BacktestEquityPoint(time=date, equity, cash_total_in_base) 의 list.
    drawdown 은 누적 peak 대비 비율 (음수 또는 0). models.BacktestEquity.time 은
    DateTime(timezone=True) 라 date → datetime(UTC midnight) 변환.
    """
    rows: list[tuple[datetime, Decimal, Decimal, Decimal]] = []
    peak = Decimal("0")
    for point in equity_curve:
        equity_value = Decimal(point.equity)
        if equity_value > peak:
            peak = equity_value
        drawdown = (
            (equity_value / peak - Decimal("1"))
            if peak > Decimal("0")
            else Decimal("0")
        )
        time_dt = datetime.combine(point.time, datetime.min.time(), tzinfo=timezone.utc)
        rows.append(
            (time_dt, equity_value, Decimal(point.cash_total_in_base), drawdown)
        )
    return rows


def _build_trade_dicts(fills: list[Any]) -> list[dict[str, Any]]:
    """fills → backtest_trades insert dicts.

    TradeFill.settlement_date (모델 A 의 D+1 체결일) → backtest_trades.time (UTC midnight).
    TASK-212 (2026-04-30) 회귀: 이전에는 fill 에 time 필드 없어 datetime.now() fallback
    이 적용되어 모든 trades 가 백테스트 실행 시각으로 기록되는 버그가 있었음.

    V3 Q8 재결정 (2026-04-29): qty_filled 는 Decimal — 정수 자산은 Decimal(int),
    CRYPTO 는 8자리 소수. backtest_trades.qty 컬럼이 0004 마이그레이션으로 Numeric(20,8)
    이라 그대로 적재 가능.
    """
    dicts: list[dict[str, Any]] = []
    for fill in fills:
        qty_value = (
            fill.qty_filled
            if isinstance(fill.qty_filled, Decimal)
            else Decimal(fill.qty_filled)
        )
        trade_time = datetime.combine(
            fill.settlement_date, datetime.min.time(), tzinfo=timezone.utc
        )
        dicts.append(
            {
                "time": trade_time,
                "asset_id": fill.asset_id,
                "side": fill.side,
                "qty": qty_value,
                "price": Decimal(fill.price),
                "commission": Decimal(fill.commission),
                "currency": fill.currency,
            }
        )
    return dicts


def _compute_and_flatten_metrics(equity_curve: list[Any]) -> dict[str, float]:
    """equity_curve → backtest_metrics insert dict (flat name → value).

    annual/monthly 는 별도 metric_name pattern (annual_return_{YYYY} / monthly_return_{YYYY-MM})
    으로 적재해 향후 단순 query 로 분리 가능.
    """
    equity_series = [(point.time, Decimal(point.equity)) for point in equity_curve]
    metrics = compute_metrics(equity_series)
    flat: dict[str, float] = {
        "cagr": metrics.cagr,
        "mdd": metrics.mdd,
        "sharpe": metrics.sharpe,
        "sortino": metrics.sortino,
        "calmar": metrics.calmar,
        "win_rate": metrics.win_rate,
    }
    for year, ret in metrics.annual_returns.items():
        flat[f"annual_return_{year}"] = ret
    for ym, ret in metrics.monthly_returns.items():
        flat[f"monthly_return_{ym}"] = ret
    return flat


def _persist_results(
    run_id: int,
    result: Any,
    base_currency: str,
) -> None:
    """엔진 결과 → equity/trades/metrics 적재 + status='done|cancelled' 마무리."""
    equity_rows = _build_equity_rows(result.equity_curve)
    trade_dicts = _build_trade_dicts(result.fills)
    flat_metrics = _compute_and_flatten_metrics(result.equity_curve)
    final_status = "cancelled" if result.aborted else "done"

    with SessionLocal() as session:
        repo = BacktestRepository(session)
        repo.insert_equity_points(run_id, equity_rows)
        repo.insert_trades(run_id, trade_dicts)
        repo.insert_metrics(run_id, flat_metrics)
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
            strategy = build_strategy_from_config(
                run.params.get("strategy", run.params)
            )

            stage = "build_context"
            initial_cash_raw = run.params.get("initial_cash") or {"KRW": 10_000_000}
            initial_cash = {
                ccy: Decimal(str(amt)) for ccy, amt in initial_cash_raw.items()
            }
            # universe 는 list[int] (create_run 호출자가 그렇게 넘김).
            universe_ids: list[int] = list(run.universe or [])

            stage = "load_market_data"
            (
                prices_aligned,
                universe_market_meta,
                fx_rates_to_base,
            ) = build_backtest_context(
                session=session,
                asset_ids=universe_ids,
                base_currency=run.base_currency,
                period_start=run.period_start,
                period_end=run.period_end,
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
                _record_failure(run_id, stage="run_engine", exc=exc, trace_id=trace_id)
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
