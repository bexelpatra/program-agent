#!/usr/bin/env python3
"""Claude Coach 로컬 대시보드 서버.

표준 라이브러리만 사용. 정적 파일 서빙 + JSON API.

사용법:
  server.py [--port 8765] [--host 127.0.0.1]
"""

from __future__ import annotations

import argparse
import json
import sys
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent
WEB_DIR = ROOT / "web"
DATA_FILE = ROOT / "data" / "sessions.jsonl"

STATIC_TYPES = {
    ".html": "text/html; charset=utf-8",
    ".js": "application/javascript; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".json": "application/json; charset=utf-8",
    ".svg": "image/svg+xml",
    ".ico": "image/x-icon",
}

STATIC_FILES = {"app.js", "style.css", "favicon.ico"}


def _load_sessions() -> list[dict]:
    if not DATA_FILE.exists():
        return []
    rows: list[dict] = []
    with DATA_FILE.open("r", encoding="utf-8", errors="replace") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    rows.sort(key=lambda d: d.get("start_ts") or "")
    return rows


class CoachHandler(BaseHTTPRequestHandler):
    server_version = "ClaudeCoach/1.0"

    def log_message(self, fmt, *args):  # noqa: N802 - stdlib signature
        sys.stderr.write("[server] %s - %s\n" % (self.address_string(), fmt % args))

    def _send_json(self, payload, status: HTTPStatus = HTTPStatus.OK):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _send_static(self, path: Path):
        if not path.exists() or not path.is_file():
            self.send_error(HTTPStatus.NOT_FOUND, "Not found")
            return
        try:
            data = path.read_bytes()
        except OSError as exc:
            self.send_error(HTTPStatus.INTERNAL_SERVER_ERROR, str(exc))
            return
        ctype = STATIC_TYPES.get(path.suffix, "application/octet-stream")
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):  # noqa: N802 - stdlib signature
        url = urlsplit(self.path)
        path = url.path

        if path == "/" or path == "/index.html":
            self._send_static(WEB_DIR / "index.html")
            return

        if path == "/api/sessions":
            self._send_json(_load_sessions())
            return

        if path.startswith("/api/session/"):
            sid = path[len("/api/session/"):]
            for s in _load_sessions():
                if s.get("session_id") == sid:
                    self._send_json(s)
                    return
            self._send_json({"error": "not found", "session_id": sid}, HTTPStatus.NOT_FOUND)
            return

        if path == "/api/health":
            self._send_json({"ok": True, "data_file": str(DATA_FILE), "sessions": len(_load_sessions())})
            return

        # 정적 파일 (web/)
        if path.startswith("/"):
            tail = path.lstrip("/")
            if tail in STATIC_FILES or tail.startswith("assets/"):
                target = (WEB_DIR / tail).resolve()
                # 디렉토리 escape 방지
                try:
                    target.relative_to(WEB_DIR.resolve())
                except ValueError:
                    self.send_error(HTTPStatus.FORBIDDEN, "Forbidden")
                    return
                self._send_static(target)
                return

        self.send_error(HTTPStatus.NOT_FOUND, "Not found")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8765)
    args = ap.parse_args()

    if not (WEB_DIR / "index.html").exists():
        print(f"warning: {WEB_DIR / 'index.html'} not found — UI 없이 API만 동작", file=sys.stderr)

    httpd = ThreadingHTTPServer((args.host, args.port), CoachHandler)
    url = f"http://{args.host}:{args.port}/"
    print(f"[server] Claude Coach 대시보드 → {url}", file=sys.stderr)
    print(f"[server] 데이터: {DATA_FILE} ({len(_load_sessions())} 세션)", file=sys.stderr)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[server] 종료", file=sys.stderr)


if __name__ == "__main__":
    main()
