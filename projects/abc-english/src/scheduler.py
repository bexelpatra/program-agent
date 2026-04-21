"""Scheduler for ABC News Daily pipeline.

Runs the full collection/analysis pipeline on a cron-style schedule,
only on weekdays (Mon-Fri) by default, and only when new episodes are
detected on the ABC News Daily listing page.

Design notes
------------
- Library: APScheduler's BlockingScheduler with a CronTrigger.
  Chosen over the simpler `schedule` library because APScheduler
  supports timezones natively (via ZoneInfo / pytz), a first-class
  "day_of_week" cron field (restricting to Mon-Fri without a custom
  weekday guard), and because it runs fine in the foreground as a
  blocking scheduler without extra threading boilerplate.

- New-episode detection:
  We compare the set of episode IDs present in ``data/transcripts/``
  (``{episode_id}_official.json`` files) to the listing returned by
  ``collector.fetch_episode_list``.  If there is at least one new ID,
  the full pipeline is invoked; otherwise we log "no new episodes"
  and return.

- Pipeline invocation:
  We shell out to ``python -m src.cli run-all`` via ``subprocess`` so
  that a crash inside any pipeline stage does not take the scheduler
  process down.  We capture stdout/stderr and log them to the scheduler
  log file.

- Resilience:
  All exceptions inside the job function are caught and logged with
  traceback.  The scheduler itself never stops because of a job failure.

Usage
-----
    # Foreground daemon (Ctrl+C to stop):
    python -m src.cli schedule

    # Run the check-and-maybe-run logic once, then exit (for testing):
    python -m src.cli schedule --once

    # Override the scheduled time for this run:
    python -m src.cli schedule --time 14:30
"""

from __future__ import annotations

import logging
import re
import subprocess
import sys
import time
import traceback
from datetime import datetime
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Iterable, List, Optional, Set

try:
    from zoneinfo import ZoneInfo  # Python 3.9+
except ImportError:  # pragma: no cover
    ZoneInfo = None  # type: ignore

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Paths / config helpers
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def _get_scheduler_config(settings: dict) -> dict:
    """Return the scheduler section of settings with defaults applied."""
    cfg = dict(settings.get("scheduler", {}) or {})
    cfg.setdefault("enabled", True)
    cfg.setdefault("time", "09:00")
    cfg.setdefault("timezone", "Asia/Seoul")
    cfg.setdefault("weekdays_only", True)
    cfg.setdefault("log_file", "data/scheduler.log")
    return cfg


def _resolve_log_path(cfg: dict) -> Path:
    log_file = cfg.get("log_file", "data/scheduler.log")
    path = Path(log_file)
    if not path.is_absolute():
        path = PROJECT_ROOT / path
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def _transcript_dir() -> Path:
    return PROJECT_ROOT / "data" / "transcripts"


# ---------------------------------------------------------------------------
# Logging setup
# ---------------------------------------------------------------------------


def _configure_file_logging(log_path: Path) -> None:
    """Attach a rotating file handler to the root logger."""
    root = logging.getLogger()
    # Avoid attaching duplicate handlers on repeated calls.
    for h in root.handlers:
        if isinstance(h, RotatingFileHandler) and getattr(
            h, "_abc_scheduler_tag", False
        ):
            return
    handler = RotatingFileHandler(
        log_path, maxBytes=2 * 1024 * 1024, backupCount=3, encoding="utf-8"
    )
    handler.setLevel(logging.INFO)
    handler.setFormatter(
        logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    )
    handler._abc_scheduler_tag = True  # type: ignore[attr-defined]
    root.addHandler(handler)
    if root.level > logging.INFO or root.level == logging.NOTSET:
        root.setLevel(logging.INFO)


# ---------------------------------------------------------------------------
# New-episode detection
# ---------------------------------------------------------------------------


def _collected_episode_ids(transcript_dir: Optional[Path] = None) -> Set[str]:
    """Return the set of episode IDs that already have official transcripts."""
    d = transcript_dir or _transcript_dir()
    if not d.is_dir():
        return set()
    ids: Set[str] = set()
    for f in d.glob("*_official.json"):
        name = f.stem  # {episode_id}_official
        if name.endswith("_official"):
            ep_id = name[: -len("_official")]
            if ep_id:
                ids.add(ep_id)
    return ids


def _latest_listing_ids(settings: dict) -> List[str]:
    """Fetch the latest episode listing and return IDs in listing order."""
    # Imported lazily so that test environments without network deps
    # (e.g. bs4 missing) can still import this module.
    from src.collector import fetch_episode_list

    items = fetch_episode_list(settings)
    ids: List[str] = []
    for it in items:
        ep_id = it.get("episode_id")
        if ep_id:
            ids.append(str(ep_id))
    return ids


def detect_new_episodes(settings: dict) -> List[str]:
    """Return the list of episode IDs present in the listing but not on disk."""
    already = _collected_episode_ids()
    latest = _latest_listing_ids(settings)
    new_ids = [eid for eid in latest if eid not in already]
    logger.info(
        "Episode check: %d on disk, %d in listing, %d new",
        len(already),
        len(latest),
        len(new_ids),
    )
    return new_ids


# ---------------------------------------------------------------------------
# Pipeline runner
# ---------------------------------------------------------------------------


def _run_pipeline_subprocess(config_path: str = "config/settings.yaml") -> int:
    """Invoke ``python -m src.cli run-all`` via subprocess.

    Returns the process exit code.  stdout/stderr are captured and
    forwarded to the scheduler logger.
    """
    cmd = [sys.executable, "-m", "src.cli", "--config", config_path, "run-all"]
    logger.info("Launching pipeline: %s (cwd=%s)", " ".join(cmd), PROJECT_ROOT)
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(PROJECT_ROOT),
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError as exc:
        logger.error("Pipeline subprocess failed to start: %s", exc)
        return 127

    if proc.stdout:
        logger.info("Pipeline stdout:\n%s", proc.stdout.rstrip())
    if proc.stderr:
        logger.warning("Pipeline stderr:\n%s", proc.stderr.rstrip())
    logger.info("Pipeline exited with code %d", proc.returncode)
    return proc.returncode


# ---------------------------------------------------------------------------
# Job function
# ---------------------------------------------------------------------------


def run_job(
    settings: dict,
    config_path: str = "config/settings.yaml",
    force_check_weekend: bool = False,
) -> dict:
    """Execute one scheduled check-and-run cycle.

    Returns a dict summary (status, new episode count, duration seconds).
    Never raises; all exceptions are caught and logged.
    """
    cfg = _get_scheduler_config(settings)
    start = time.time()
    summary = {
        "status": "unknown",
        "new_episodes": 0,
        "duration_seconds": 0.0,
        "exit_code": None,
    }

    # Weekend guard (defense in depth; the cron trigger also restricts).
    if cfg.get("weekdays_only", True) and not force_check_weekend:
        now = datetime.now(_resolve_tz(cfg))
        if now.weekday() >= 5:  # 5=Sat, 6=Sun
            logger.info("skipped: weekend (weekday=%d)", now.weekday())
            summary["status"] = "skipped_weekend"
            summary["duration_seconds"] = round(time.time() - start, 2)
            return summary

    try:
        new_ids = detect_new_episodes(settings)
    except Exception:
        logger.error("New-episode detection failed:\n%s", traceback.format_exc())
        summary["status"] = "detection_failed"
        summary["duration_seconds"] = round(time.time() - start, 2)
        return summary

    summary["new_episodes"] = len(new_ids)

    if not new_ids:
        logger.info("no new episodes; skipping pipeline")
        summary["status"] = "no_new_episodes"
        summary["duration_seconds"] = round(time.time() - start, 2)
        return summary

    logger.info("Running pipeline for %d new episodes: %s", len(new_ids), new_ids[:10])

    try:
        rc = _run_pipeline_subprocess(config_path=config_path)
        summary["exit_code"] = rc
        summary["status"] = "pipeline_ok" if rc == 0 else "pipeline_failed"
    except Exception:
        logger.error("Pipeline execution raised:\n%s", traceback.format_exc())
        summary["status"] = "pipeline_exception"

    summary["duration_seconds"] = round(time.time() - start, 2)
    logger.info("Job summary: %s", summary)
    return summary


# ---------------------------------------------------------------------------
# Timezone + time parsing
# ---------------------------------------------------------------------------


_TIME_RE = re.compile(r"^(\d{1,2}):(\d{2})$")


def _parse_hhmm(s: str) -> tuple[int, int]:
    m = _TIME_RE.match(s.strip())
    if not m:
        raise ValueError(f"Invalid time format (expected HH:MM): {s!r}")
    hour = int(m.group(1))
    minute = int(m.group(2))
    if not (0 <= hour < 24 and 0 <= minute < 60):
        raise ValueError(f"Time out of range: {s!r}")
    return hour, minute


def _resolve_tz(cfg: dict):
    tz_name = cfg.get("timezone", "Asia/Seoul")
    if ZoneInfo is None:
        return None
    try:
        return ZoneInfo(tz_name)
    except Exception:  # pragma: no cover
        logger.warning(
            "Unknown timezone %r; falling back to system local time", tz_name
        )
        return None


# ---------------------------------------------------------------------------
# Public entry points
# ---------------------------------------------------------------------------


def run_once(
    settings: dict,
    config_path: str = "config/settings.yaml",
    skip_weekend_check: bool = True,
) -> dict:
    """Execute the job a single time and return the summary.

    By default (``skip_weekend_check=True``) this is intended for manual
    testing and does NOT skip on weekends — the operator has explicitly
    asked for an immediate run.  Pass ``skip_weekend_check=False`` to
    honour the weekend guard.
    """
    cfg = _get_scheduler_config(settings)
    log_path = _resolve_log_path(cfg)
    _configure_file_logging(log_path)
    logger.info("=== Scheduler one-shot run ===")
    return run_job(
        settings, config_path=config_path, force_check_weekend=skip_weekend_check
    )


def run_forever(
    settings: dict,
    config_path: str = "config/settings.yaml",
    time_override: Optional[str] = None,
) -> None:
    """Run the blocking scheduler loop until interrupted (Ctrl+C)."""
    cfg = _get_scheduler_config(settings)

    if not cfg.get("enabled", True):
        logger.info("Scheduler disabled in settings; exiting.")
        return

    log_path = _resolve_log_path(cfg)
    _configure_file_logging(log_path)

    hhmm = time_override or cfg.get("time", "09:00")
    hour, minute = _parse_hhmm(hhmm)
    tz = _resolve_tz(cfg)
    weekdays_only = bool(cfg.get("weekdays_only", True))

    # Import APScheduler lazily so module import doesn't hard-fail when
    # the optional dependency is missing (e.g. in minimal test envs).
    try:
        from apscheduler.schedulers.blocking import BlockingScheduler
        from apscheduler.triggers.cron import CronTrigger
    except ImportError as exc:  # pragma: no cover
        logger.error(
            "APScheduler is not installed (%s). "
            "Install it via `pip install APScheduler`.",
            exc,
        )
        raise

    scheduler_kwargs = {}
    if tz is not None:
        scheduler_kwargs["timezone"] = tz

    scheduler = BlockingScheduler(**scheduler_kwargs)

    trigger_kwargs: dict = {"hour": hour, "minute": minute}
    if weekdays_only:
        trigger_kwargs["day_of_week"] = "mon-fri"
    if tz is not None:
        trigger_kwargs["timezone"] = tz

    trigger = CronTrigger(**trigger_kwargs)

    def _job() -> None:
        try:
            run_job(settings, config_path=config_path)
        except Exception:
            # Defensive: run_job already swallows, but in case something
            # leaks we never want to kill the scheduler.
            logger.error("Unhandled job error:\n%s", traceback.format_exc())

    scheduler.add_job(_job, trigger=trigger, id="abc_news_daily_pipeline")

    logger.info(
        "Scheduler started: time=%02d:%02d tz=%s weekdays_only=%s log=%s",
        hour,
        minute,
        cfg.get("timezone"),
        weekdays_only,
        log_path,
    )

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logger.info("Scheduler stopped by user.")
