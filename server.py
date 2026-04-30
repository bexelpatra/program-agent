#!/usr/bin/env python3
"""Claude Coach 로컬 대시보드 서버.

표준 라이브러리만 사용. 정적 파일 서빙 + JSON API + Anthropic 코칭 프록시.

사용법:
  server.py [--port 8765] [--host 127.0.0.1]

환경변수 (.env 또는 export):
  ANTHROPIC_API_KEY        — 코칭 기능 활성화에 필요
  ANTHROPIC_MODEL          — 기본 'claude-sonnet-4-5' (Sonnet 4.5)
  COACH_DATA_FILE          — 기본 <repo>/data/sessions.jsonl
  COACH_PRINCIPLES_FILE    — 기본 <repo>/principles.json
  COACH_TRANSCRIPTS_DIR    — 기본 ~/.claude/projects
"""

from __future__ import annotations

import argparse
import json
import os
import ssl
import sys
import time
import urllib.error
import urllib.request
from collections import Counter
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent
WEB_DIR = ROOT / "web"

# ---------- .env 로딩 (stdlib only) ----------

def load_dotenv(path: Path) -> None:
    if not path.exists():
        return
    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        k, v = line.split("=", 1)
        k, v = k.strip(), v.strip()
        if (v.startswith('"') and v.endswith('"')) or (v.startswith("'") and v.endswith("'")):
            v = v[1:-1]
        os.environ.setdefault(k, v)


load_dotenv(ROOT / ".env")

DATA_FILE = Path(os.environ.get("COACH_DATA_FILE") or (ROOT / "data" / "sessions.jsonl"))
PRINCIPLES_FILE = Path(os.environ.get("COACH_PRINCIPLES_FILE") or (ROOT / "principles.json"))
TRANSCRIPTS_DIR = Path(os.environ.get("COACH_TRANSCRIPTS_DIR") or (Path.home() / ".claude" / "projects"))
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
ANTHROPIC_MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-5")
ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"
ANTHROPIC_VERSION = "2023-06-01"

STATIC_TYPES = {
    ".html": "text/html; charset=utf-8",
    ".js": "application/javascript; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".json": "application/json; charset=utf-8",
    ".svg": "image/svg+xml",
    ".ico": "image/x-icon",
}

STATIC_FILES = {"app.js", "style.css", "favicon.ico", "guide.html", "guide.js", "theme.js"}

PRINCIPLES_CACHE: dict | None = None
PRINCIPLES_TEXT: str | None = None


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


def _load_principles() -> tuple[dict, str]:
    global PRINCIPLES_CACHE, PRINCIPLES_TEXT
    if PRINCIPLES_CACHE is None:
        if PRINCIPLES_FILE.exists():
            PRINCIPLES_TEXT = PRINCIPLES_FILE.read_text(encoding="utf-8")
            PRINCIPLES_CACHE = json.loads(PRINCIPLES_TEXT)
        else:
            PRINCIPLES_CACHE = {"axes": [], "session_types": {}}
            PRINCIPLES_TEXT = "{}"
    return PRINCIPLES_CACHE, PRINCIPLES_TEXT


# ---------- guide aggregate ----------

def _build_guide_payload() -> dict:
    sessions = _load_sessions()
    principles, _ = _load_principles()
    if not sessions:
        return {
            "principles": principles,
            "diagnosis": None,
            "type_distribution": {},
            "examples_by_principle": {},
            "stats": {"total": 0},
        }

    # 약한 축 진단
    axes_acc = {a["id"]: [] for a in principles.get("axes", [])}
    for s in sessions:
        sc = (s.get("score") or {}).get("axes") or {}
        for k in axes_acc:
            v = sc.get(k)
            if isinstance(v, (int, float)):
                axes_acc[k].append(v)
    axes_avg = {k: (sum(v) / len(v) if v else 0.0) for k, v in axes_acc.items()}
    axes_recent = {}
    recent = sessions[-10:]
    for k in axes_acc:
        vs = [(r.get("score") or {}).get("axes", {}).get(k) for r in recent if (r.get("score") or {}).get("axes", {}).get(k) is not None]
        axes_recent[k] = sum(vs) / len(vs) if vs else 0.0

    # 약한 축 = 평균이 낮은 순
    sorted_axes = sorted(axes_avg.items(), key=lambda kv: kv[1])
    weakest = [a[0] for a in sorted_axes[:2]]

    # 유형 분포
    type_counts = Counter(s.get("session_type") or "mixed" for s in sessions)

    # 원칙별 worst 세션 매핑 — 각 원칙의 linked_metrics 가 가장 나쁜 세션 상위 3개
    examples_by_principle: dict[str, list[dict]] = {}
    for axis in principles.get("axes", []):
        for p in axis.get("principles", []):
            metrics = p.get("linked_metrics") or []
            scored: list[tuple[float, dict]] = []
            for s in sessions:
                # heuristic: 작을수록 좋은 메트릭/클수록 좋은 메트릭 두 종류
                bad_score = _principle_violation_score(p, s)
                if bad_score > 0:
                    scored.append((bad_score, s))
            scored.sort(key=lambda kv: kv[0], reverse=True)
            top = []
            for _, s in scored[:3]:
                top.append({
                    "session_id": s.get("session_id"),
                    "start_ts": s.get("start_ts"),
                    "cwd": s.get("cwd"),
                    "session_type": s.get("session_type"),
                    "score_total": (s.get("score") or {}).get("total"),
                    "score_axes": (s.get("score") or {}).get("axes"),
                    "metrics_excerpt": {k: s.get(k) for k in metrics},
                    "worst_spots": s.get("worst_spots") or [],
                })
            if top:
                examples_by_principle[p["id"]] = top

    diagnosis = {
        "weakest_axes": weakest,
        "axes_avg": {k: round(v, 1) for k, v in axes_avg.items()},
        "axes_recent": {k: round(v, 1) for k, v in axes_recent.items()},
        "summary": _diagnosis_summary(sessions, weakest, axes_avg, axes_recent, type_counts),
    }

    stats = {
        "total": len(sessions),
        "with_worst_spots": sum(1 for s in sessions if s.get("worst_spots")),
        "avg_score": round(sum((s.get("score") or {}).get("total", 0) for s in sessions) / len(sessions), 1),
        "coach_available": bool(ANTHROPIC_API_KEY),
    }

    return {
        "principles": principles,
        "diagnosis": diagnosis,
        "type_distribution": dict(type_counts),
        "examples_by_principle": examples_by_principle,
        "stats": stats,
    }


def _principle_violation_score(principle: dict, session: dict) -> float:
    pid = principle.get("id", "")
    # 각 원칙별로 위반 강도 계산. 클수록 더 많이 어김.
    if pid == "clarity_first_prompt":
        if (session.get("first_prompt_chars") or 0) < 60 and (session.get("assistant_turns") or 0) >= 8:
            return 100 - (session.get("first_prompt_chars") or 0) + (session.get("assistant_turns") or 0)
        return 0
    if pid == "clarity_specificity":
        sp = session.get("prompt_specificity") or 0.0
        if sp < 0.03 and (session.get("user_turns") or 0) >= 3:
            return (0.05 - sp) * 1000 + (session.get("user_turns") or 0)
        return 0
    if pid == "clarity_success_criteria":
        cr = session.get("correction_rate") or 0.0
        if cr >= 0.20:
            return cr * 100 + (session.get("correction_signals") or 0)
        return 0
    if pid == "efficiency_parallel":
        pr = session.get("parallel_rate") or 0.0
        if pr < 0.15 and (session.get("tool_calls_total") or 0) >= 10:
            return (0.4 - pr) * 100 + (session.get("tool_calls_total") or 0) / 10
        return 0
    if pid == "efficiency_pre_check":
        bf = session.get("bash_fail_rate") or 0.0
        if bf >= 0.20 and (session.get("bash_total") or 0) >= 5:
            return bf * 100 + (session.get("bash_total") or 0) / 5
        return 0
    if pid == "efficiency_edit_context":
        return (session.get("edit_string_not_found") or 0) * 5
    if pid == "economy_subagent":
        reads = session.get("file_reads_total") or 0
        sub = session.get("subagent_invocations") or 0
        if reads >= 20 and sub == 0:
            return reads
        return 0
    if pid == "economy_no_reread":
        return (session.get("file_reread_count") or 0)
    if pid == "economy_grep_pattern":
        return (session.get("redundant_searches") or 0) * 3
    if pid == "planning_taskcreate":
        if (session.get("assistant_turns") or 0) >= 15 and (session.get("plan_tool_uses") or 0) == 0:
            return (session.get("assistant_turns") or 0)
        return 0
    if pid == "planning_thinking":
        if (session.get("assistant_turns") or 0) >= 10 and (session.get("thinking_chars_total") or 0) < 300:
            return (session.get("assistant_turns") or 0)
        return 0
    if pid == "planning_plan_mode":
        if (session.get("edit_count") or 0) + (session.get("write_count") or 0) >= 10 and (session.get("plan_tool_uses") or 0) == 0:
            return (session.get("edit_count") or 0) + (session.get("write_count") or 0)
        return 0
    if pid == "health_low_correction":
        return (session.get("correction_signals") or 0) * 10
    if pid == "health_turn_ratio":
        ut = session.get("user_turns") or 0
        at = session.get("assistant_turns") or 0
        if ut and at / ut > 10:
            return at / ut
        return 0
    if pid == "health_small_validation":
        score = (session.get("edit_string_not_found") or 0) * 2 + (session.get("bash_failures") or 0)
        return score if score >= 5 else 0
    return 0


def _diagnosis_summary(sessions, weakest, axes_avg, axes_recent, type_counts) -> str:
    if not weakest:
        return "충분한 데이터를 모아주세요."
    n = len(sessions)
    weakest_label_map = {a["id"]: a["label"] for a in (_load_principles()[0].get("axes") or [])}
    parts = [f"분석된 {n}개 세션을 보면, 가장 약한 축은 **{weakest_label_map.get(weakest[0], weakest[0])}** 입니다 (평균 {axes_avg.get(weakest[0], 0):.1f}/20)."]
    if len(weakest) > 1:
        parts[0] = parts[0][:-1] + f" — 다음으로 **{weakest_label_map.get(weakest[1], weakest[1])}** ({axes_avg.get(weakest[1], 0):.1f}/20)."
    # 최근 추세
    delta = axes_recent.get(weakest[0], 0) - axes_avg.get(weakest[0], 0)
    if abs(delta) >= 0.8:
        if delta > 0:
            parts.append(f"최근 10세션 평균은 {axes_recent.get(weakest[0], 0):.1f} 로 개선되는 추세입니다.")
        else:
            parts.append(f"최근 10세션 평균은 {axes_recent.get(weakest[0], 0):.1f} 로 더 떨어지고 있어 우선순위가 높습니다.")
    # 유형 분포 코멘트
    most_common = type_counts.most_common(1)[0] if type_counts else None
    if most_common:
        parts.append(f"세션 유형은 '{most_common[0]}' 가 가장 많아({most_common[1]}/{n}개) 그 모드의 베스트 프랙티스부터 익히는 게 효과적입니다.")
    return " ".join(parts)


# ---------- Anthropic 코칭 ----------

def _build_coach_messages(session: dict, principles_text: str) -> tuple[str, list[dict]]:
    system_blocks = [
        {
            "type": "text",
            "text": (
                "당신은 'Claude Coach' 의 코칭 에이전트입니다. 사용자가 클로드 코드(Anthropic 의 코딩 CLI)를 더 잘 쓰도록 한국어로 짧고 구체적인 피드백을 제공합니다.\n\n"
                "제공되는 자료:\n"
                "1) `principles` — 5축(명료성·효율성·경제성·계획성·건강도)별 원칙 모음\n"
                "2) 사용자의 한 세션 메트릭 + worst-spot 추출본 + 첫 user 프롬프트 발췌\n\n"
                "출력 형식 (한국어, markdown):\n"
                "## 진단\n"
                "- 이 세션이 무슨 작업이었는지 한 줄 (메트릭 기반)\n"
                "- 가장 큰 개선 포인트 1개를 어느 원칙에 비추어 적시\n\n"
                "## 더 잘 했더라면\n"
                "사용자의 worst-spot 발췌를 인용하면서, '이렇게 첫 프롬프트를 썼다면…' 형태의 구체적 재작성 예시 1-2개를 제시. 코드블록 사용 가능.\n\n"
                "## 다음 세션에 가져갈 1가지\n"
                "- 한 줄짜리 행동 강령\n\n"
                "톤: 짧고 단정적. 비난 대신 설계. 칭찬 끼워넣기 금지(분석에 집중)."
            ),
            "cache_control": {"type": "ephemeral"},
        },
        {
            "type": "text",
            "text": "원칙(principles.json):\n" + principles_text,
            "cache_control": {"type": "ephemeral"},
        },
    ]

    # 세션 요약
    keep_keys = [
        "session_id", "start_ts", "duration_sec", "cwd",
        "session_type", "session_type_reason",
        "user_turns", "assistant_turns", "first_prompt_chars",
        "avg_prompt_chars", "prompt_specificity",
        "correction_signals", "correction_rate",
        "tool_calls_total", "tool_calls_by_name",
        "parallel_rate", "subagent_invocations", "plan_tool_uses",
        "bash_total", "bash_failures", "bash_fail_rate",
        "edit_string_not_found", "edit_count", "write_count",
        "file_reads_total", "file_reread_count", "file_reread_rate",
        "redundant_searches",
        "thinking_chars_total",
        "score",
        "worst_spots",
    ]
    session_summary = {k: session.get(k) for k in keep_keys}

    user_text = (
        "다음은 분석할 한 세션의 메트릭과 발췌본입니다.\n\n```json\n"
        + json.dumps(session_summary, ensure_ascii=False, indent=2)
        + "\n```\n\n"
        "위 메트릭과 worst_spots 의 user_prompt_excerpt 를 근거로 코칭해 주세요. "
        "발췌본이 비어 있으면 메트릭만 가지고 진단하되, 추측보다 메트릭에서 직접 읽히는 사실을 근거로 쓰세요."
    )

    return system_blocks, [{"role": "user", "content": user_text}]


def _call_anthropic(system_blocks, messages, max_tokens=900, timeout=60) -> tuple[int, dict]:
    if not ANTHROPIC_API_KEY:
        return 503, {"error": "ANTHROPIC_API_KEY 가 설정되지 않았습니다.", "hint": ".env 또는 환경변수에 키를 넣고 서버를 재시작하세요."}

    payload = {
        "model": ANTHROPIC_MODEL,
        "max_tokens": max_tokens,
        "system": system_blocks,
        "messages": messages,
    }
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        ANTHROPIC_API_URL,
        data=body,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "x-api-key": ANTHROPIC_API_KEY,
            "anthropic-version": ANTHROPIC_VERSION,
        },
    )
    ctx = ssl.create_default_context()
    started = time.time()
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
            raw = resp.read().decode("utf-8")
            data = json.loads(raw)
    except urllib.error.HTTPError as exc:
        try:
            err_body = exc.read().decode("utf-8")
            err_json = json.loads(err_body)
        except Exception:
            err_json = {"raw": str(exc)}
        return exc.code, {"error": "anthropic_http_error", "status": exc.code, "detail": err_json}
    except urllib.error.URLError as exc:
        return 502, {"error": "anthropic_connection_error", "detail": str(exc)}
    except Exception as exc:
        return 500, {"error": "anthropic_unknown_error", "detail": repr(exc)}

    elapsed = round(time.time() - started, 2)
    text_parts = []
    for block in data.get("content", []) or []:
        if isinstance(block, dict) and block.get("type") == "text":
            text_parts.append(block.get("text", ""))
    return 200, {
        "ok": True,
        "model": data.get("model", ANTHROPIC_MODEL),
        "elapsed_sec": elapsed,
        "usage": data.get("usage"),
        "stop_reason": data.get("stop_reason"),
        "text": "\n".join(text_parts).strip(),
    }


# ---------- HTTP handler ----------

class CoachHandler(BaseHTTPRequestHandler):
    server_version = "ClaudeCoach/1.1"

    def log_message(self, fmt, *args):  # noqa: N802
        sys.stderr.write("[server] %s - %s\n" % (self.address_string(), fmt % args))

    def _read_body(self) -> dict:
        try:
            length = int(self.headers.get("Content-Length", "0") or 0)
        except ValueError:
            length = 0
        if length <= 0:
            return {}
        raw = self.rfile.read(length)
        try:
            return json.loads(raw.decode("utf-8") or "{}")
        except json.JSONDecodeError:
            return {}

    def _send_json(self, payload, status: HTTPStatus = HTTPStatus.OK):
        if isinstance(status, int):
            code = status
        else:
            code = status.value
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
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

    def do_GET(self):  # noqa: N802
        url = urlsplit(self.path)
        path = url.path

        if path == "/" or path == "/index.html":
            self._send_static(WEB_DIR / "index.html")
            return
        if path == "/guide" or path == "/guide.html":
            self._send_static(WEB_DIR / "guide.html")
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
        if path == "/api/guide":
            self._send_json(_build_guide_payload())
            return
        if path == "/api/health":
            self._send_json({
                "ok": True,
                "data_file": str(DATA_FILE),
                "sessions": len(_load_sessions()),
                "principles_loaded": PRINCIPLES_FILE.exists(),
                "coach_available": bool(ANTHROPIC_API_KEY),
                "model": ANTHROPIC_MODEL,
            })
            return

        if path.startswith("/"):
            tail = path.lstrip("/")
            if tail in STATIC_FILES or tail.startswith("assets/"):
                target = (WEB_DIR / tail).resolve()
                try:
                    target.relative_to(WEB_DIR.resolve())
                except ValueError:
                    self.send_error(HTTPStatus.FORBIDDEN, "Forbidden")
                    return
                self._send_static(target)
                return

        self.send_error(HTTPStatus.NOT_FOUND, "Not found")

    def do_POST(self):  # noqa: N802
        url = urlsplit(self.path)
        path = url.path

        if path.startswith("/api/coach/"):
            sid = path[len("/api/coach/"):]
            if not sid:
                self._send_json({"error": "session_id required"}, HTTPStatus.BAD_REQUEST)
                return
            session = next((s for s in _load_sessions() if s.get("session_id") == sid), None)
            if session is None:
                self._send_json({"error": "session not found"}, HTTPStatus.NOT_FOUND)
                return
            principles, principles_text = _load_principles()
            system_blocks, messages = _build_coach_messages(session, principles_text)
            code, result = _call_anthropic(system_blocks, messages)
            self._send_json(result, code)
            return

        self.send_error(HTTPStatus.NOT_FOUND, "Not found")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8765)
    args = ap.parse_args()

    if not (WEB_DIR / "index.html").exists():
        print(f"warning: {WEB_DIR / 'index.html'} not found — UI 없이 API만 동작", file=sys.stderr)
    _load_principles()  # 시작 시 캐시
    httpd = ThreadingHTTPServer((args.host, args.port), CoachHandler)
    url = f"http://{args.host}:{args.port}/"
    print(f"[server] Claude Coach → {url}", file=sys.stderr)
    print(f"[server] 데이터: {DATA_FILE} ({len(_load_sessions())} 세션)", file=sys.stderr)
    print(f"[server] 코칭: {'활성 (' + ANTHROPIC_MODEL + ')' if ANTHROPIC_API_KEY else '비활성 — .env 에 ANTHROPIC_API_KEY 추가하면 동작'}", file=sys.stderr)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[server] 종료", file=sys.stderr)


if __name__ == "__main__":
    main()
