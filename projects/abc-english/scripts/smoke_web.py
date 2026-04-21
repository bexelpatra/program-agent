"""End-to-end smoke test for the abc-english web UI.

Starts uvicorn on a temporary port in a background process, then hits the
main routes with ``httpx`` and prints ``SMOKE OK`` on success.

Usage::

    python scripts/smoke_web.py

Exit code is 0 on success, 1 on any failure.
"""

from __future__ import annotations

import atexit
import os
import subprocess
import sys
import time
from pathlib import Path

import httpx

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
_HOST = "127.0.0.1"
_PORT = 18767
_BASE_URL = f"http://{_HOST}:{_PORT}"
_CONFIG_PATH = _PROJECT_ROOT / "config" / "settings.yaml"

_proc: subprocess.Popen | None = None


def _terminate_server() -> None:
    """Best-effort termination of the uvicorn subprocess."""
    global _proc
    if _proc is None:
        return
    if _proc.poll() is None:
        try:
            _proc.terminate()
            try:
                _proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                _proc.kill()
                _proc.wait(timeout=5)
        except Exception as exc:  # pragma: no cover
            print(f"[smoke] failed to terminate server: {exc}", file=sys.stderr)
    _proc = None


atexit.register(_terminate_server)


def _start_server() -> subprocess.Popen:
    """Launch uvicorn factory mode in a subprocess and return the handle."""
    env = os.environ.copy()
    env["ABC_CONFIG"] = str(_CONFIG_PATH)
    # Make sure the project root is on PYTHONPATH so `web.app` imports cleanly.
    existing_pp = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = (
        f"{_PROJECT_ROOT}{os.pathsep}{existing_pp}" if existing_pp else str(_PROJECT_ROOT)
    )

    cmd = [
        sys.executable,
        "-m",
        "uvicorn",
        "--factory",
        "web.app:create_app",
        "--host",
        _HOST,
        "--port",
        str(_PORT),
        "--log-level",
        "warning",
    ]
    proc = subprocess.Popen(
        cmd,
        cwd=str(_PROJECT_ROOT),
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    return proc


def _wait_for_ready(timeout_s: float = 30.0) -> bool:
    """Poll /api/health until it responds or timeout elapses."""
    deadline = time.time() + timeout_s
    last_err: Exception | None = None
    while time.time() < deadline:
        if _proc is not None and _proc.poll() is not None:
            print(
                f"[smoke] server exited early with code {_proc.returncode}",
                file=sys.stderr,
            )
            return False
        try:
            r = httpx.get(f"{_BASE_URL}/api/health", timeout=2.0)
            if r.status_code == 200:
                return True
        except Exception as exc:
            last_err = exc
        time.sleep(0.3)
    print(f"[smoke] server failed to become ready: {last_err}", file=sys.stderr)
    return False


def _check_ok(client: httpx.Client, path: str, contains: str | None = None) -> bool:
    try:
        r = client.get(path)
    except Exception as exc:
        print(f"[smoke] FAIL {path}: request error: {exc}", file=sys.stderr)
        return False
    if r.status_code != 200:
        print(f"[smoke] FAIL {path}: status={r.status_code}", file=sys.stderr)
        return False
    if contains is not None and contains not in r.text:
        print(
            f"[smoke] FAIL {path}: expected substring {contains!r} missing",
            file=sys.stderr,
        )
        return False
    print(f"[smoke] OK   {path} (status=200)")
    return True


def _check_any(client: httpx.Client, path: str, allowed: tuple[int, ...]) -> bool:
    try:
        r = client.get(path)
    except Exception as exc:
        print(f"[smoke] FAIL {path}: request error: {exc}", file=sys.stderr)
        return False
    print(f"[smoke] INFO {path} status={r.status_code}")
    if r.status_code not in allowed:
        print(
            f"[smoke] FAIL {path}: status={r.status_code} not in {allowed}",
            file=sys.stderr,
        )
        return False
    return True


def main() -> int:
    global _proc
    _proc = _start_server()
    if not _wait_for_ready():
        return 1

    ok = True
    with httpx.Client(base_url=_BASE_URL, timeout=10.0) as client:
        ok &= _check_ok(client, "/", contains="<html")
        ok &= _check_ok(client, "/static/js/common.js")
        ok &= _check_ok(client, "/static/js/study.js")
        ok &= _check_ok(client, "/static/js/notebook.js")
        ok &= _check_ok(client, "/static/js/episodes.js")
        ok &= _check_ok(client, "/static/css/app.css")
        ok &= _check_ok(client, "/study/TEST", contains='data-episode-id="TEST"')
        ok &= _check_ok(client, "/notebook", contains="notebook.js")
        # ES may not be up — accept a broad range of responses.
        ok &= _check_any(client, "/api/episodes", allowed=(200, 500, 502, 503))

    if ok:
        print("SMOKE OK")
        return 0
    print("SMOKE FAILED", file=sys.stderr)
    return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    finally:
        _terminate_server()
