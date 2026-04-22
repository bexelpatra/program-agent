"""Run-hash & cache helpers for the backtest cache (architecture decisions #10, #11).

Covers:

- :func:`compute_run_hash` — canonical config hash.
- :func:`compute_code_commit_hash` — current git HEAD (or "unknown").
- :func:`compute_data_hash` — hash of (max(updated_at), row count) per asset.
- :func:`is_stale` — compare a stored run's data_hash to the live hash.

Actual ``backtest_runs`` persistence lives in :mod:`.run_store`; we keep the
hash primitives here so both the engine and the persistence layer share the
same canonical keys without circular imports.
"""

from __future__ import annotations

import datetime as _dt
import hashlib
import json
import subprocess
from pathlib import Path
from typing import TYPE_CHECKING, Any, Iterable

from sqlalchemy import func, select, text

if TYPE_CHECKING:  # pragma: no cover - typing only
    from sqlalchemy.orm import Session

    from stock_backtest.data.models import BacktestRun


__all__ = [
    "compute_run_hash",
    "compute_code_commit_hash",
    "compute_data_hash",
    "is_stale",
]


def _canonical(value: Any) -> Any:
    """Return a JSON-serialisable canonical form of ``value``.

    Sorts dicts by key, normalises dates to ISO strings, coerces tuples/sets
    to sorted lists so that equivalent semantic inputs hash identically.
    """
    if isinstance(value, dict):
        return {k: _canonical(value[k]) for k in sorted(value)}
    if isinstance(value, (list, tuple)):
        return [_canonical(v) for v in value]
    if isinstance(value, set):
        return sorted(_canonical(v) for v in value)
    if isinstance(value, (_dt.date, _dt.datetime)):
        return value.isoformat()
    return value


def compute_run_hash(
    strategy_name: str,
    params: dict[str, Any],
    universe: Iterable[str],
    period: tuple[_dt.date, _dt.date],
    base_ccy: str,
) -> str:
    """Return a deterministic SHA-256 hash for a backtest run configuration.

    Parameters
    ----------
    strategy_name:
        Canonical strategy identifier (``Strategy.name``).
    params:
        Strategy parameter dict (``StrategyParams.model_dump()``).
    universe:
        Iterable of asset symbols; sorted internally for stability.
    period:
        ``(start_date, end_date)`` tuple.
    base_ccy:
        ISO currency code.
    """
    start, end = period
    payload = {
        "strategy": strategy_name,
        "params": _canonical(params),
        "universe": sorted(str(s) for s in universe),
        "start": _canonical(start),
        "end": _canonical(end),
        "base_ccy": base_ccy,
    }
    blob = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()


def compute_code_commit_hash(cwd: str | Path | None = None) -> str:
    """Return the current git HEAD commit hash, or ``"unknown"`` on failure.

    Runs ``git rev-parse HEAD`` as a subprocess. Returns ``"unknown"`` when
    git is not installed, the directory is not a git repo, or the command
    otherwise fails. Never raises.
    """
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=str(cwd) if cwd is not None else None,
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
    except (FileNotFoundError, OSError, subprocess.SubprocessError):
        return "unknown"
    if result.returncode != 0:
        return "unknown"
    out = result.stdout.strip()
    if not out:
        return "unknown"
    return out


def compute_data_hash(session: "Session", asset_ids: list[int]) -> str:
    """Hash (max(updated_at/time), row count) per asset for a universe.

    ``ohlcv`` has no ``updated_at`` column in the current schema, so we use
    ``MAX(time)`` + ``COUNT(*)`` as a proxy for freshness. This still changes
    whenever new bars arrive or historical rows are upserted with new values
    (because upserts do not change row count, but the latest ``time`` moves
    as data accumulates).

    For empty universes the function returns the hash of an empty payload.
    """
    # Canonical ordering to keep the hash stable across caller ordering.
    ids = sorted(int(a) for a in asset_ids)
    payload: list[dict[str, Any]] = []

    if ids:
        # Try the ORM path first (lets unit tests stub ``session.execute``).
        try:
            from stock_backtest.data.models import Ohlcv

            stmt = (
                select(
                    Ohlcv.asset_id,
                    func.max(Ohlcv.time),
                    func.count(Ohlcv.asset_id),
                )
                .where(Ohlcv.asset_id.in_(ids))
                .group_by(Ohlcv.asset_id)
            )
            rows = list(session.execute(stmt))
        except Exception:  # pragma: no cover - defensive fallback
            rows = list(
                session.execute(
                    text(
                        "SELECT asset_id, MAX(time), COUNT(*) "
                        "FROM ohlcv WHERE asset_id = ANY(:ids) "
                        "GROUP BY asset_id"
                    ),
                    {"ids": ids},
                )
            )

        by_id: dict[int, tuple[Any, int]] = {}
        for row in rows:
            # row may be Row / tuple; support both.
            asset_id = int(row[0])
            max_time = row[1]
            count = int(row[2]) if row[2] is not None else 0
            by_id[asset_id] = (max_time, count)

        for aid in ids:
            max_time, count = by_id.get(aid, (None, 0))
            payload.append(
                {
                    "asset_id": aid,
                    "max_time": _canonical(max_time)
                    if isinstance(max_time, (_dt.date, _dt.datetime))
                    else (str(max_time) if max_time is not None else None),
                    "count": count,
                }
            )

    blob = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()


def is_stale(run_row: "BacktestRun", session: "Session") -> bool:
    """Return True if ``run_row.data_hash`` differs from the live data hash.

    The live hash is recomputed from the run's ``universe`` JSONB field,
    which is expected to contain a list of asset_ids (or dicts with an
    ``asset_id`` key). When the stored ``data_hash`` is NULL the run is
    considered stale by definition.
    """
    stored = getattr(run_row, "data_hash", None)
    if not stored:
        return True

    universe = getattr(run_row, "universe", None) or []
    asset_ids: list[int] = []
    if isinstance(universe, list):
        for item in universe:
            if isinstance(item, dict):
                aid = item.get("asset_id")
                if aid is not None:
                    asset_ids.append(int(aid))
            else:
                try:
                    asset_ids.append(int(item))
                except (TypeError, ValueError):
                    continue
    current = compute_data_hash(session, asset_ids)
    return current != stored
