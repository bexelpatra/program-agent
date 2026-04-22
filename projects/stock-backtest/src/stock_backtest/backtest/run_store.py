"""Persist / load backtest runs (architecture decisions #10, #11).

Wraps :mod:`stock_backtest.data.repository` helpers to:

- ``save_run``: persist a :class:`BacktestResult` + derived metrics.
- ``find_cached_run``: look up an existing run by ``run_hash``.
- ``load_run``: rehydrate a stored run into engine-friendly shapes.

The engine itself is not modified; callers wrap the engine run with this
module. A minimal ``run_with_cache`` helper lives in :mod:`.engine_cache` to
avoid touching the engine module directly.
"""

from __future__ import annotations

import datetime as _dt
from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING, Any, Optional

import pandas as pd
from sqlalchemy import select

from stock_backtest.data.models import (
    BacktestEquity,
    BacktestMetric,
    BacktestRun,
    BacktestTrade,
)
from stock_backtest.data.repository import (
    bulk_insert_equity,
    bulk_insert_trades,
    get_run_by_hash,
    insert_metrics,
    insert_run,
)

if TYPE_CHECKING:  # pragma: no cover - typing only
    from sqlalchemy.orm import Session

    from stock_backtest.backtest.engine import BacktestConfig, BacktestResult


__all__ = [
    "save_run",
    "find_cached_run",
    "load_run",
]


def _to_datetime(value: Any) -> datetime:
    """Coerce date/datetime/Timestamp to a naive-safe datetime."""
    if isinstance(value, datetime):
        return value
    if isinstance(value, _dt.date):
        return datetime.combine(value, _dt.time.min)
    if isinstance(value, pd.Timestamp):
        ts = value.to_pydatetime()
        return ts
    # Fallback: treat as ISO string.
    return datetime.fromisoformat(str(value))


def save_run(
    session: "Session",
    config: "BacktestConfig",
    result: "BacktestResult",
    strategy_name: str,
    data_hash: str,
    code_hash: str,
) -> int:
    """Persist a backtest run (row, equity, trades, metrics) and return ``run_id``.

    The derived metrics are computed via
    :func:`stock_backtest.metrics.performance.compute_all`.
    """
    from stock_backtest.metrics.performance import compute_all

    run_hash = result.run_hash
    if run_hash is None:
        from stock_backtest.backtest.cache import compute_run_hash

        run_hash = compute_run_hash(
            strategy_name,
            config.params,
            [spec.symbol for spec in config.universe],
            (config.period_start, config.period_end),
            config.base_currency,
        )

    universe_payload = [
        {
            "asset_id": spec.asset_id,
            "symbol": spec.symbol,
            "market": spec.market,
            "currency": spec.currency,
        }
        for spec in config.universe
    ]

    run_id = insert_run(
        session,
        run_hash=run_hash,
        user_id="local",
        strategy_name=strategy_name,
        params=dict(config.params or {}),
        universe=universe_payload,
        period_start=config.period_start,
        period_end=config.period_end,
        base_currency=config.base_currency,
        market_mode=config.market_mode,
        code_commit_hash=code_hash,
        data_hash=data_hash,
    )

    # --- Equity ---------------------------------------------------------
    equity_rows: list[dict[str, Any]] = []
    equity = result.equity_curve
    if equity is not None and len(equity) > 0:
        # Compute drawdown inline to avoid an extra metrics pass.
        eq_floats = [float(v) for v in equity.values]
        running_max = float("-inf")
        for ts, v in zip(equity.index, eq_floats):
            running_max = max(running_max, v)
            dd = (v - running_max) / running_max if running_max > 0 else 0.0
            equity_rows.append(
                {
                    "time": _to_datetime(ts),
                    "equity": v,
                    "cash": 0.0,
                    "drawdown": dd,
                }
            )
    bulk_insert_equity(session, run_id, equity_rows)

    # --- Trades ---------------------------------------------------------
    trade_rows = [
        {
            "time": _to_datetime(t.date),
            "asset_id": t.asset_id,
            "side": t.side,
            "qty": float(t.qty) if isinstance(t.qty, Decimal) else float(t.qty),
            "price": float(t.price) if isinstance(t.price, Decimal) else float(t.price),
            "commission": float(t.commission_bps)
            if isinstance(t.commission_bps, Decimal)
            else float(t.commission_bps),
            "currency": t.currency,
            "currency_from": getattr(t, "currency_from", None),
            "currency_to": getattr(t, "currency_to", None),
            "fx_rate": (
                float(t.fx_rate) if getattr(t, "fx_rate", None) is not None else None
            ),
            "spread_bps": (
                int(t.spread_bps)
                if getattr(t, "spread_bps", None) is not None
                else None
            ),
        }
        for t in (result.trades or [])
    ]
    bulk_insert_trades(session, run_id, trade_rows)

    # --- Metrics --------------------------------------------------------
    metrics = compute_all(result.equity_curve, trades=result.trades or [])
    insert_metrics(session, run_id, metrics)

    return run_id


def find_cached_run(session: "Session", run_hash: str) -> Optional[BacktestRun]:
    """Return the stored :class:`BacktestRun` with matching hash, or ``None``."""
    return get_run_by_hash(session, run_hash)


def load_run(
    session: "Session", run_id: int
) -> tuple[BacktestRun, pd.Series, list[dict[str, Any]], dict[str, float]]:
    """Rehydrate a stored run.

    Returns
    -------
    (run_row, equity_series, trade_rows, metrics_dict)
        ``equity_series`` is indexed by timestamp. ``trade_rows`` is a list
        of dicts with keys ``time, asset_id, side, qty, price, commission,
        currency``. ``metrics_dict`` maps metric name to float value.
    """
    run_row = session.get(BacktestRun, run_id)
    if run_row is None:
        raise ValueError(f"backtest_runs run_id={run_id} not found")

    eq_stmt = (
        select(BacktestEquity.time, BacktestEquity.equity)
        .where(BacktestEquity.run_id == run_id)
        .order_by(BacktestEquity.time.asc())
    )
    eq_rows = list(session.execute(eq_stmt))
    if eq_rows:
        idx = pd.DatetimeIndex([r[0] for r in eq_rows])
        values = [float(r[1]) for r in eq_rows]
        equity = pd.Series(values, index=idx, name="equity")
    else:
        equity = pd.Series(dtype="float64", name="equity")

    tr_stmt = (
        select(BacktestTrade)
        .where(BacktestTrade.run_id == run_id)
        .order_by(BacktestTrade.time.asc())
    )
    trades = [
        {
            "time": t.time,
            "asset_id": t.asset_id,
            "side": t.side,
            "qty": t.qty,
            "price": t.price,
            "commission": t.commission,
            "currency": t.currency,
            "currency_from": t.currency_from,
            "currency_to": t.currency_to,
            "fx_rate": t.fx_rate,
            "spread_bps": t.spread_bps,
        }
        for t in session.execute(tr_stmt).scalars().all()
    ]

    m_stmt = select(BacktestMetric.metric_name, BacktestMetric.value).where(
        BacktestMetric.run_id == run_id
    )
    metrics = {name: float(val) for name, val in session.execute(m_stmt)}

    return run_row, equity, trades, metrics
