#!/usr/bin/env python3
"""Claude Coach ingest — ~/.claude/projects 전체를 순회해 sessions.jsonl 백필.

사용법:
  ingest.py [--projects-dir ~/.claude/projects] [--out data/sessions.jsonl] [--quiet]
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import analyzer  # 같은 디렉토리

ROOT = Path(__file__).resolve().parent
DEFAULT_PROJECTS = Path.home() / ".claude" / "projects"
DEFAULT_OUT = ROOT / "data" / "sessions.jsonl"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--projects-dir", default=str(DEFAULT_PROJECTS))
    ap.add_argument("--out", default=str(DEFAULT_OUT))
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    projects_dir = Path(args.projects_dir).expanduser()
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)

    files = sorted(projects_dir.glob("*/*.jsonl"))
    if not files:
        print(f"No transcripts found under {projects_dir}", file=sys.stderr)
        sys.exit(1)

    if not args.quiet:
        print(f"[ingest] {len(files)} transcripts under {projects_dir}", file=sys.stderr)

    by_session: dict[str, dict] = {}
    failed: list[tuple[Path, str]] = []
    started = time.time()

    for i, f in enumerate(files, 1):
        try:
            m = analyzer.analyze(f)
        except Exception as exc:  # pragma: no cover - 개별 실패는 건너뜀
            failed.append((f, repr(exc)))
            continue
        sid = m.get("session_id")
        if not sid:
            continue
        # 같은 session_id 가 여러 .jsonl 에 흩어진 경우 가장 최신 end_ts 우선
        prev = by_session.get(sid)
        if prev is None or (m.get("end_ts") or "") > (prev.get("end_ts") or ""):
            by_session[sid] = m
        if not args.quiet and i % 25 == 0:
            print(f"[ingest] {i}/{len(files)} ({len(by_session)} unique sessions)", file=sys.stderr)

    rows = sorted(by_session.values(), key=lambda d: d.get("start_ts") or "")
    tmp = out.with_suffix(".jsonl.tmp")
    with tmp.open("w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    tmp.replace(out)

    elapsed = time.time() - started
    if not args.quiet:
        print(f"[ingest] wrote {len(rows)} sessions → {out} in {elapsed:.1f}s", file=sys.stderr)
        if failed:
            print(f"[ingest] {len(failed)} files failed:", file=sys.stderr)
            for f, e in failed[:5]:
                print(f"  - {f}: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
