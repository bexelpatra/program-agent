"""CLI entry-point for the abc-english pipeline.

Usage:
    python -m src.cli --help
    python -m src.cli collect
    python -m src.cli run-all
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path
from typing import List

import click

from src.es_client import load_settings

logger = logging.getLogger(__name__)


def _setup_logging() -> None:
    """Configure root logger to INFO level with a readable format."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def _load_settings(config: str) -> dict:
    """Load settings from the given config path."""
    return load_settings(Path(config))


def _scan_episode_ids(transcript_dir: Path, suffix: str) -> List[str]:
    """Scan transcript directory for files matching *_{suffix}.json and return episode IDs."""
    if not transcript_dir.is_dir():
        logger.warning("Transcript directory does not exist: %s", transcript_dir)
        return []
    ids = []
    for f in sorted(transcript_dir.glob(f"*_{suffix}.json")):
        # filename pattern: {episode_id}_{suffix}.json
        name = f.stem  # e.g. "106551254_official"
        episode_id = name.rsplit(f"_{suffix}", 1)[0]
        if episode_id:
            ids.append(episode_id)
    return ids


def _get_transcript_dir() -> Path:
    """Return the data/transcripts/ directory relative to the project root."""
    return Path(__file__).resolve().parent.parent / "data" / "transcripts"


@click.group()
@click.option(
    "--config",
    default="config/settings.yaml",
    help="Path to settings YAML file.",
    type=click.Path(),
)
@click.pass_context
def cli(ctx: click.Context, config: str) -> None:
    """ABC News Daily English learning pipeline."""
    _setup_logging()
    ctx.ensure_object(dict)
    ctx.obj["config"] = config


@cli.command()
@click.option(
    "--limit",
    type=int,
    default=None,
    help="Only collect the first N episodes from the listing (useful for testing).",
)
@click.pass_context
def collect(ctx: click.Context, limit: int | None) -> None:
    """Collect episodes (listing, detail, transcript, MP3)."""
    from src.collector import collect_all

    settings = _load_settings(ctx.obj["config"])
    episodes = collect_all(settings, limit=limit)

    has_transcript = sum(1 for ep in episodes if ep.has_transcript)
    click.echo(
        f"Collection complete: {len(episodes)} episodes found, "
        f"{has_transcript} with transcript."
    )


@cli.command()
@click.pass_context
def transcribe(ctx: click.Context) -> None:
    """Transcribe audio files with Whisper."""
    from src.transcriber import transcribe_all

    settings = _load_settings(ctx.obj["config"])
    transcript_dir = _get_transcript_dir()
    episode_ids = _scan_episode_ids(transcript_dir, "official")

    if not episode_ids:
        click.echo("No episodes with official transcripts found. Run 'collect' first.")
        return

    click.echo(f"Found {len(episode_ids)} episodes to transcribe.")
    results = transcribe_all(episode_ids, settings)

    done = sum(1 for r in results if r.get("status") == "done" or not r.get("skipped"))
    skipped = sum(1 for r in results if r.get("skipped"))
    click.echo(f"Transcription complete: {done} processed, {skipped} skipped.")


@cli.command()
@click.pass_context
def compare(ctx: click.Context) -> None:
    """Compare official vs Whisper transcripts (WER)."""
    from src.comparator import compare_all

    settings = _load_settings(ctx.obj["config"])
    transcript_dir = _get_transcript_dir()

    official_ids = set(_scan_episode_ids(transcript_dir, "official"))
    whisper_ids = set(_scan_episode_ids(transcript_dir, "whisper"))
    episode_ids = sorted(official_ids & whisper_ids)

    if not episode_ids:
        click.echo(
            "No episodes with both official and whisper transcripts found. "
            "Run 'collect' and 'transcribe' first."
        )
        return

    click.echo(f"Comparing {len(episode_ids)} episodes.")
    results = compare_all(episode_ids, settings)

    done = sum(1 for r in results if r.get("status") == "done")
    click.echo(f"Comparison complete: {done}/{len(results)} episodes processed.")


@cli.command()
@click.pass_context
def analyze(ctx: click.Context) -> None:
    """Run spaCy NLP analysis (vocabulary frequency)."""
    from src.analyzer import analyze_all

    settings = _load_settings(ctx.obj["config"])
    transcript_dir = _get_transcript_dir()
    episode_ids = _scan_episode_ids(transcript_dir, "official")

    if not episode_ids:
        click.echo("No episodes found. Run 'collect' first.")
        return

    click.echo(f"Analysing {len(episode_ids)} episodes.")
    vocab = analyze_all(episode_ids, settings)
    click.echo(f"Analysis complete: {len(vocab)} unique vocabulary items extracted.")


@cli.command("llm-analyze")
@click.pass_context
def llm_analyze(ctx: click.Context) -> None:
    """Run LLM deep analysis (idioms, CEFR, Korean definitions)."""
    from src.llm_analyzer import (
        classify_vocabulary_for_episode,
        detect_expressions_for_episode,
    )

    settings = _load_settings(ctx.obj["config"])
    transcript_dir = _get_transcript_dir()
    episode_ids = _scan_episode_ids(transcript_dir, "official")

    if not episode_ids:
        click.echo("No episodes found. Run 'collect' first.")
        return

    click.echo(f"Running LLM analysis on {len(episode_ids)} episodes.")
    total_expressions = 0
    total_classified = 0

    for idx, ep_id in enumerate(episode_ids, 1):
        click.echo(f"  [{idx}/{len(episode_ids)}] Episode {ep_id}...")
        try:
            expressions = detect_expressions_for_episode(ep_id, settings)
            total_expressions += len(expressions)
        except Exception as exc:
            logger.error("Expression detection failed for %s: %s", ep_id, exc)

        try:
            classified = classify_vocabulary_for_episode(ep_id, [], settings)
            total_classified += len(classified)
        except Exception as exc:
            logger.error("Vocabulary classification failed for %s: %s", ep_id, exc)

    click.echo(
        f"LLM analysis complete: {total_expressions} expressions detected, "
        f"{total_classified} vocabulary items classified."
    )


@cli.command()
@click.pass_context
def load(ctx: click.Context) -> None:
    """Load analysis results into Elasticsearch."""
    from src.loader import load_all

    settings = _load_settings(ctx.obj["config"])

    # We need to gather all data first by running analysis steps
    # Import models that the loader expects
    click.echo("Loading data into Elasticsearch...")

    # Gather episodes
    transcript_dir = _get_transcript_dir()
    episode_ids = _scan_episode_ids(transcript_dir, "official")

    if not episode_ids:
        click.echo("No data to load. Run the pipeline first.")
        return

    # Run collect to get episodes, analyze for vocab, compare for sentences,
    # llm-analyze for expressions -- or load from existing data files.
    # For the load command, we re-run the pipeline stages to gather data.
    from src.analyzer import analyze_all
    from src.collector import collect_all
    from src.comparator import compare_all
    from src.llm_analyzer import detect_expressions_for_episode

    click.echo("Collecting episodes...")
    episodes = collect_all(settings)

    official_ids = set(_scan_episode_ids(transcript_dir, "official"))
    whisper_ids = set(_scan_episode_ids(transcript_dir, "whisper"))
    compare_ids = sorted(official_ids & whisper_ids)

    click.echo("Comparing transcripts...")
    compare_results = compare_all(compare_ids, settings)
    sentences = []
    for r in compare_results:
        sentences.extend(r.get("sentences", []))

    click.echo("Analysing vocabulary...")
    vocabulary = analyze_all(episode_ids, settings)

    click.echo("Detecting expressions...")
    expressions = []
    for ep_id in episode_ids:
        try:
            expressions.extend(detect_expressions_for_episode(ep_id, settings))
        except Exception as exc:
            logger.error("Expression detection failed for %s: %s", ep_id, exc)

    click.echo("Loading into Elasticsearch...")
    summary = load_all(episodes, sentences, vocabulary, expressions, settings)

    for key, counts in summary.items():
        click.echo(
            f"  {key}: {counts.get('loaded', 0)} loaded, {counts.get('errors', 0)} errors"
        )

    click.echo("Load complete.")


@cli.command("run-all")
@click.pass_context
def run_all(ctx: click.Context) -> None:
    """Run the full pipeline: collect -> transcribe -> compare -> analyze -> llm-analyze -> load."""
    click.echo("=== Starting full pipeline ===")

    click.echo("\n--- Step 1/6: Collect ---")
    ctx.invoke(collect)

    click.echo("\n--- Step 2/6: Transcribe ---")
    ctx.invoke(transcribe)

    click.echo("\n--- Step 3/6: Compare ---")
    ctx.invoke(compare)

    click.echo("\n--- Step 4/6: Analyze ---")
    ctx.invoke(analyze)

    click.echo("\n--- Step 5/6: LLM Analyze ---")
    ctx.invoke(llm_analyze)

    click.echo("\n--- Step 6/6: Load ---")
    ctx.invoke(load)

    click.echo("\n=== Full pipeline complete ===")


@cli.command("schedule")
@click.option(
    "--once",
    is_flag=True,
    default=False,
    help="Run the check-and-maybe-run cycle immediately once, then exit.",
)
@click.option(
    "--time",
    "time_override",
    type=str,
    default=None,
    help="Override the scheduled time (HH:MM, 24h) for this run.",
)
@click.pass_context
def schedule(ctx: click.Context, once: bool, time_override: str | None) -> None:
    """Run the weekday scheduler that auto-detects new episodes."""
    from src import scheduler as sched

    settings = _load_settings(ctx.obj["config"])
    config_path = ctx.obj["config"]

    if once:
        summary = sched.run_once(settings, config_path=config_path)
        click.echo(f"One-shot run complete: {summary}")
        return

    click.echo("Starting scheduler (Ctrl+C to stop)...")
    sched.run_forever(settings, config_path=config_path, time_override=time_override)


@cli.command("init-indices")
@click.pass_context
def init_indices(ctx: click.Context) -> None:
    """Create Elasticsearch indices."""
    from src.models import create_indices

    settings = _load_settings(ctx.obj["config"])
    results = create_indices(settings)

    for key, info in results.items():
        status = "created" if info["created"] else "already exists"
        click.echo(f"  {key}: {info['index_name']} ({status})")

    click.echo("Index initialization complete.")


@cli.command("delete-indices")
@click.pass_context
def delete_indices(ctx: click.Context) -> None:
    """Delete Elasticsearch indices (with confirmation)."""
    from src.models import delete_indices as _delete_indices

    if not click.confirm(
        "Are you sure you want to delete all indices? This cannot be undone."
    ):
        click.echo("Aborted.")
        return

    settings = _load_settings(ctx.obj["config"])
    results = _delete_indices(settings)

    for key, info in results.items():
        status = "deleted" if info["deleted"] else "not found"
        click.echo(f"  {key}: {info['index_name']} ({status})")

    click.echo("Index deletion complete.")


@cli.command("serve")
@click.option(
    "--host",
    default=None,
    help="Bind host (default: 127.0.0.1 or web.host in settings).",
)
@click.option(
    "--port",
    type=int,
    default=None,
    help="Bind port (default: 8080 or web.port in settings).",
)
@click.option(
    "--reload", is_flag=True, default=False, help="Enable uvicorn auto-reload."
)
@click.pass_context
def serve(ctx: click.Context, host: str | None, port: int | None, reload: bool) -> None:
    """Start the FastAPI web UI via uvicorn."""
    import os

    import uvicorn

    config_path = ctx.obj["config"]
    settings = _load_settings(config_path)
    web_cfg = settings.get("web") or {}

    final_host = host or web_cfg.get("host") or "127.0.0.1"
    final_port = port or web_cfg.get("port") or 8080

    # Pass config path to factory via env var (uvicorn does not pass args to factory).
    os.environ["ABC_CONFIG"] = str(Path(config_path).resolve())

    click.echo(
        f"Starting web server on http://{final_host}:{final_port} (reload={reload})"
    )
    uvicorn.run(
        "web.app:create_app",
        factory=True,
        host=final_host,
        port=int(final_port),
        reload=reload,
    )


if __name__ == "__main__":
    cli()
