#!/usr/bin/env python3
"""Claude Coach analyzer — 트랜스크립트 1개 → 세션 메트릭 JSON.

사용법:
  analyzer.py <transcript.jsonl>      # 표준출력으로 메트릭 JSON 출력
  analyzer.py --hook                   # Stop 훅: stdin JSON 파싱 → data/sessions.jsonl 갱신
"""

from __future__ import annotations

import json
import os
import re
import statistics
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
SESSIONS_FILE = DATA_DIR / "sessions.jsonl"

CORRECTION_PATTERNS = [
    r"\bno\b", r"\bnope\b", r"\bstop\b", r"\bdon'?t\b", r"\bwait\b",
    r"\bactually\b", r"\bnot that\b", r"\bundo\b", r"\brevert\b",
    r"\bnever mind\b",
    r"아니야", r"아니", r"다시", r"잘못", r"되돌", r"취소", r"멈춰", r"그게 아니",
    r"하지\s*마", r"중단",
]
CORRECTION_RE = re.compile("|".join(CORRECTION_PATTERNS), re.IGNORECASE)

CODE_TOKEN_RE = re.compile(
    r"`[^`]+`"                      # 백틱 코드
    r"|/[\w./\-]+"                  # 경로
    r"|\b\w+\.(?:py|js|ts|tsx|jsx|md|json|yml|yaml|html|css|sh|go|rs|java|cpp|c|h|sql)\b"
    r"|\b\w+\(\)"                   # foo()
    r"|\b\w+::\w+\b"                # rust style
    r"|\b\w+\.\w+\b"                # dotted
)
WORD_RE = re.compile(r"\S+")

PLAN_TOOLS = {"TaskCreate", "TaskUpdate", "TaskList", "EnterPlanMode", "ExitPlanMode", "TodoWrite", "Plan"}
EXPLORE_TOOLS = {"Explore"}


def _content_to_text(content) -> str:
    """user/assistant content 를 텍스트로 평탄화."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        out = []
        for c in content:
            if not isinstance(c, dict):
                continue
            t = c.get("type")
            if t == "text":
                out.append(c.get("text", ""))
            elif t == "thinking":
                out.append(c.get("thinking", ""))
        return "\n".join(out)
    return ""


def _is_user_prompt(msg: dict) -> bool:
    """True 면 사람이 입력한 프롬프트로 간주. tool_result는 False."""
    if msg.get("type") != "user":
        return False
    if msg.get("isMeta"):
        return False
    content = msg.get("message", {}).get("content")
    if isinstance(content, str):
        return content.strip() != ""
    if isinstance(content, list):
        for c in content:
            if isinstance(c, dict) and c.get("type") == "tool_result":
                return False
        return any(isinstance(c, dict) and c.get("type") == "text" for c in content)
    return False


def _user_prompt_text(msg: dict) -> str:
    content = msg.get("message", {}).get("content")
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "\n".join(c.get("text", "") for c in content if isinstance(c, dict) and c.get("type") == "text")
    return ""


def _prompt_specificity(text: str) -> float:
    if not text:
        return 0.0
    words = WORD_RE.findall(text)
    if not words:
        return 0.0
    matches = CODE_TOKEN_RE.findall(text)
    return min(1.0, len(matches) / len(words))


def _safe_iter_jsonl(path: Path):
    with path.open("r", encoding="utf-8", errors="replace") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                continue


def analyze(transcript_path: Path) -> dict:
    """트랜스크립트 1개 → 메트릭 dict."""
    session_id = None
    cwd = None
    git_branch = None
    version = None
    start_ts = None
    end_ts = None

    user_turns_main = 0
    assistant_turns_main = 0
    prompt_lens = []
    first_prompt_chars = None
    correction_signals = 0
    specificity_scores = []

    tool_calls_total = 0
    tool_calls_by_name = Counter()
    parallel_tool_msgs = 0
    assistant_msgs_with_tools = 0
    subagent_invocations = 0
    subagent_types = Counter()
    plan_tool_uses = 0

    bash_total = 0
    bash_failures = 0
    edit_string_not_found = 0
    file_reads = Counter()
    file_reads_total = 0
    grep_patterns = Counter()
    redundant_searches = 0

    thinking_chars_total = 0
    thinking_blocks = 0
    assistant_text_chars = 0

    sidechain_assistant = 0

    pending_tool_use = {}  # tool_use_id -> tool name

    # 시퀀스 추적 (worst-spot 추출용)
    # 각 원소: ("user", text, ts) 또는 ("asst", [tool_names...], ts)
    sequence: list[tuple] = []
    edit_count = 0
    write_count = 0

    for d in _safe_iter_jsonl(transcript_path):
        t = d.get("type")
        sid = d.get("sessionId")
        if sid and not session_id:
            session_id = sid
        if not cwd and d.get("cwd"):
            cwd = d.get("cwd")
        if not git_branch and d.get("gitBranch"):
            git_branch = d.get("gitBranch")
        if not version and d.get("version"):
            version = d.get("version")
        ts = d.get("timestamp")
        if ts:
            if start_ts is None or ts < start_ts:
                start_ts = ts
            if end_ts is None or ts > end_ts:
                end_ts = ts

        is_side = bool(d.get("isSidechain"))

        if t == "user" and _is_user_prompt(d):
            if is_side:
                continue
            text = _user_prompt_text(d)
            user_turns_main += 1
            L = len(text)
            prompt_lens.append(L)
            if first_prompt_chars is None:
                first_prompt_chars = L
            is_correction = bool(CORRECTION_RE.search(text))
            if is_correction:
                correction_signals += 1
            specificity_scores.append(_prompt_specificity(text))
            sequence.append(("user", text, ts, is_correction))

        elif t == "user":
            content = d.get("message", {}).get("content")
            if isinstance(content, list):
                for c in content:
                    if not isinstance(c, dict):
                        continue
                    if c.get("type") != "tool_result":
                        continue
                    tool_use_id = c.get("tool_use_id")
                    name = pending_tool_use.get(tool_use_id, "")
                    is_err = c.get("is_error")
                    if isinstance(is_err, str):
                        is_err = is_err.lower() == "true"
                    body = c.get("content", "")
                    if isinstance(body, list):
                        body = " ".join(
                            (cc.get("text", "") if isinstance(cc, dict) else str(cc))
                            for cc in body
                        )
                    body_str = body if isinstance(body, str) else ""
                    if name == "Bash":
                        if is_err:
                            bash_failures += 1
                    if name == "Edit":
                        if is_err or "string not found" in body_str.lower() or "string to replace not found" in body_str.lower():
                            edit_string_not_found += 1

        elif t == "assistant":
            if is_side:
                sidechain_assistant += 1
            else:
                assistant_turns_main += 1
            msg = d.get("message", {})
            content = msg.get("content", [])
            if not isinstance(content, list):
                continue
            tool_uses = [c for c in content if isinstance(c, dict) and c.get("type") == "tool_use"]
            text_chars = sum(len(c.get("text", "")) for c in content if isinstance(c, dict) and c.get("type") == "text")
            if not is_side:
                assistant_text_chars += text_chars
                for c in content:
                    if isinstance(c, dict) and c.get("type") == "thinking":
                        th = c.get("thinking", "") or ""
                        if th:
                            thinking_blocks += 1
                            thinking_chars_total += len(th)
            if tool_uses and not is_side:
                assistant_msgs_with_tools += 1
                if len(tool_uses) >= 2:
                    parallel_tool_msgs += 1
                sequence.append(("asst", [tu.get("name", "?") for tu in tool_uses], ts))
            for tu in tool_uses:
                name = tu.get("name", "?")
                tu_id = tu.get("id")
                if tu_id:
                    pending_tool_use[tu_id] = name
                inp = tu.get("input", {}) or {}
                if is_side:
                    continue
                tool_calls_total += 1
                tool_calls_by_name[name] += 1
                if name == "Agent":
                    subagent_invocations += 1
                    st = inp.get("subagent_type", "general-purpose")
                    subagent_types[st] += 1
                if name in PLAN_TOOLS:
                    plan_tool_uses += 1
                if name == "Bash":
                    bash_total += 1
                if name == "Edit":
                    edit_count += 1
                if name == "Write":
                    write_count += 1
                if name == "Read":
                    fp = inp.get("file_path", "")
                    if fp:
                        file_reads[fp] += 1
                        file_reads_total += 1
                if name == "Grep" or (name == "Bash" and isinstance(inp.get("command"), str) and inp["command"].lstrip().startswith(("grep", "rg", "find"))):
                    pat = ""
                    if name == "Grep":
                        pat = str(inp.get("pattern", ""))
                    else:
                        pat = inp.get("command", "")[:80]
                    if pat:
                        grep_patterns[pat] += 1

    # 파생 메트릭
    duration_sec = None
    if start_ts and end_ts:
        try:
            from datetime import datetime
            s = datetime.fromisoformat(start_ts.replace("Z", "+00:00"))
            e = datetime.fromisoformat(end_ts.replace("Z", "+00:00"))
            duration_sec = max(0, int((e - s).total_seconds()))
        except Exception:
            duration_sec = None

    avg_prompt_chars = round(statistics.mean(prompt_lens), 1) if prompt_lens else 0
    median_prompt_chars = round(statistics.median(prompt_lens), 1) if prompt_lens else 0
    avg_specificity = round(statistics.mean(specificity_scores), 4) if specificity_scores else 0.0

    parallel_rate = round(parallel_tool_msgs / assistant_msgs_with_tools, 4) if assistant_msgs_with_tools else 0.0
    bash_fail_rate = round(bash_failures / bash_total, 4) if bash_total else 0.0
    correction_rate = round(correction_signals / user_turns_main, 4) if user_turns_main else 0.0

    file_reread_count = sum(c - 1 for c in file_reads.values() if c > 1)
    file_reread_rate = round(file_reread_count / file_reads_total, 4) if file_reads_total else 0.0
    redundant_searches = sum(c - 1 for c in grep_patterns.values() if c > 1)

    thinking_chars_avg_per_turn = round(thinking_chars_total / assistant_turns_main, 1) if assistant_turns_main else 0.0

    # ---------- 세션 유형 분류 ----------
    session_type, session_type_reason = classify_session_type(
        user_turns=user_turns_main,
        assistant_turns=assistant_turns_main,
        tool_calls_total=tool_calls_total,
        correction_rate=correction_rate,
        edit_string_not_found=edit_string_not_found,
        bash_fail_rate=bash_fail_rate,
        bash_total=bash_total,
        edit_count=edit_count,
        write_count=write_count,
        plan_tool_uses=plan_tool_uses,
        file_reads_total=file_reads_total,
    )

    # ---------- worst-spot 추출 ----------
    worst_spots = extract_worst_spots(sequence)

    metrics = {
        "session_id": session_id,
        "transcript_path": str(transcript_path),
        "cwd": cwd,
        "git_branch": git_branch,
        "version": version,
        "start_ts": start_ts,
        "end_ts": end_ts,
        "duration_sec": duration_sec,

        "user_turns": user_turns_main,
        "assistant_turns": assistant_turns_main,
        "sidechain_assistant_turns": sidechain_assistant,

        "first_prompt_chars": first_prompt_chars or 0,
        "avg_prompt_chars": avg_prompt_chars,
        "median_prompt_chars": median_prompt_chars,
        "prompt_specificity": avg_specificity,
        "correction_signals": correction_signals,
        "correction_rate": correction_rate,

        "tool_calls_total": tool_calls_total,
        "tool_calls_by_name": dict(tool_calls_by_name.most_common()),
        "parallel_tool_calls": parallel_tool_msgs,
        "parallel_rate": parallel_rate,
        "subagent_invocations": subagent_invocations,
        "subagent_types": dict(subagent_types),
        "plan_tool_uses": plan_tool_uses,

        "bash_total": bash_total,
        "bash_failures": bash_failures,
        "bash_fail_rate": bash_fail_rate,
        "edit_string_not_found": edit_string_not_found,

        "file_reads_total": file_reads_total,
        "file_reread_count": file_reread_count,
        "file_reread_rate": file_reread_rate,
        "redundant_searches": redundant_searches,

        "thinking_chars_total": thinking_chars_total,
        "thinking_blocks": thinking_blocks,
        "thinking_chars_avg_per_turn": thinking_chars_avg_per_turn,
        "assistant_text_chars": assistant_text_chars,

        "edit_count": edit_count,
        "write_count": write_count,

        "session_type": session_type,
        "session_type_reason": session_type_reason,
        "worst_spots": worst_spots,
    }
    metrics["score"] = compute_score(metrics)
    metrics["tips"] = generate_tips(metrics)
    return metrics


# ---------- 세션 유형 분류 ----------
SESSION_TYPES = ["one_shot", "exploration", "implementation", "debugging", "mixed"]
SESSION_TYPE_LABELS_KO = {
    "one_shot": "단발 질문",
    "exploration": "탐색형",
    "implementation": "구현형",
    "debugging": "디버깅형",
    "mixed": "복합형",
}


def classify_session_type(
    *,
    user_turns: int,
    assistant_turns: int,
    tool_calls_total: int,
    correction_rate: float,
    edit_string_not_found: int,
    bash_fail_rate: float,
    bash_total: int,
    edit_count: int,
    write_count: int,
    plan_tool_uses: int,
    file_reads_total: int,
) -> tuple[str, str]:
    """세션 유형과 사유 한 줄 반환. 첫 매치 우선."""
    if user_turns <= 2 and assistant_turns <= 5 and tool_calls_total <= 3:
        return "one_shot", "짧은 질문/응답으로 종료"
    debug_signals = 0
    if correction_rate >= 0.30:
        debug_signals += 1
    if edit_string_not_found >= 2:
        debug_signals += 1
    if bash_total >= 3 and bash_fail_rate >= 0.30:
        debug_signals += 1
    if debug_signals >= 1:
        return "debugging", f"정정/실패 신호 {debug_signals}개 (correction_rate={correction_rate:.0%}, edit_err={edit_string_not_found}, bash_fail={bash_fail_rate:.0%})"
    if (edit_count + write_count) >= 5 or plan_tool_uses >= 3:
        return "implementation", f"수정/작성 {edit_count + write_count}회, 계획 도구 {plan_tool_uses}회"
    if file_reads_total >= 8 or tool_calls_total >= 15:
        return "exploration", f"탐색 read {file_reads_total}회, 총 도구 {tool_calls_total}회"
    return "mixed", "단일 분류에 들어맞지 않음"


# ---------- worst-spot 추출 ----------
def extract_worst_spots(sequence: list[tuple]) -> list[dict]:
    """user 프롬프트와 assistant 도구 호출 시퀀스에서 개선 여지가 큰 구간 1-2개."""
    spots: list[dict] = []

    # 1) 직렬 read/grep — 한 메시지당 1개씩 ≥3 연속 (병렬화 누락)
    cur_run_name = None
    cur_run_msgs: list[int] = []  # asst 인덱스
    longest_run: tuple[str, list[int]] = ("", [])
    for i, ev in enumerate(sequence):
        if ev[0] != "asst":
            continue
        names: list[str] = ev[1]
        if len(names) == 1 and names[0] in ("Read", "Grep", "Glob"):
            n = names[0]
            if n == cur_run_name:
                cur_run_msgs.append(i)
            else:
                cur_run_name = n
                cur_run_msgs = [i]
            if len(cur_run_msgs) > len(longest_run[1]):
                longest_run = (n, list(cur_run_msgs))
        else:
            cur_run_name = None
            cur_run_msgs = []
    if len(longest_run[1]) >= 3:
        # 그 직전 user 프롬프트 찾기
        first_idx = longest_run[1][0]
        prev_user = ""
        for j in range(first_idx - 1, -1, -1):
            if sequence[j][0] == "user":
                prev_user = sequence[j][1]
                break
        spots.append({
            "type": "sequential_tool",
            "tool": longest_run[0],
            "count": len(longest_run[1]),
            "user_prompt_excerpt": _trunc(prev_user, 200),
            "summary": f"{longest_run[0]} {len(longest_run[1])}회를 각각 다른 메시지로 직렬 호출",
            "suggestion": f"독립적인 {longest_run[0]} 들은 한 메시지 안에 여러 tool_use 로 묶어 병렬 호출하면 시간·토큰을 크게 아낄 수 있습니다.",
        })

    # 2) 짧은 첫 프롬프트로 큰 작업 시작 — 첫 user 가 60자 미만인데 그 후 assistant 메시지 ≥ 8
    first_user_idx = next((i for i, ev in enumerate(sequence) if ev[0] == "user"), None)
    if first_user_idx is not None:
        first_text = sequence[first_user_idx][1]
        if len(first_text) > 0 and len(first_text) < 60:
            following_asst = sum(1 for ev in sequence[first_user_idx + 1:] if ev[0] == "asst")
            if following_asst >= 8:
                spots.append({
                    "type": "short_first_prompt",
                    "first_prompt_chars": len(first_text),
                    "following_asst_turns": following_asst,
                    "user_prompt_excerpt": _trunc(first_text, 200),
                    "summary": f"{len(first_text)}자 짧은 프롬프트로 시작해 {following_asst}회 왕복",
                    "suggestion": "첫 프롬프트에 (1) 어떤 결과면 성공인가 (2) 제약/금지 (3) 예시 입력·출력 을 함께 넣으면 왕복 횟수를 크게 줄일 수 있습니다.",
                })

    # 3) 정정 신호 클러스터 — 연속한 user 중 correction 가 ≥ 2개
    correction_indices = [i for i, ev in enumerate(sequence) if ev[0] == "user" and len(ev) > 3 and ev[3]]
    if len(correction_indices) >= 2:
        # user 시퀀스 인덱스에서 정정이 인접하면 하나의 "방향 전환"
        user_indices = [i for i, ev in enumerate(sequence) if ev[0] == "user"]
        cluster_size = 0
        max_cluster = (0, None)  # (size, anchor_user_idx)
        for j, ui in enumerate(user_indices):
            if ui in correction_indices:
                cluster_size += 1
                if cluster_size > max_cluster[0]:
                    max_cluster = (cluster_size, ui)
            else:
                cluster_size = 0
        if max_cluster[0] >= 2 and max_cluster[1] is not None:
            text = sequence[max_cluster[1]][1]
            spots.append({
                "type": "correction_cluster",
                "cluster_size": max_cluster[0],
                "user_prompt_excerpt": _trunc(text, 200),
                "summary": f"정정 신호 {max_cluster[0]}회 연속 — 방향 전환이 잦았던 지점",
                "suggestion": "되돌리기를 줄이려면 작업 시작 전 '어떤 결과면 성공인가'를 한 번에 합의해 두고, 큰 변경은 plan mode 로 사용자 승인 후 진행하세요.",
            })

    return spots[:2]


def _trunc(text: str, n: int) -> str:
    if not text:
        return ""
    text = text.replace("\n", " ").strip()
    return text if len(text) <= n else text[: n - 1] + "…"


def _band(value: float, thresholds: list[tuple[float, float]]) -> float:
    """thresholds: [(min_value, points), ...] 큰 값부터 평가. 매칭 없으면 0."""
    for thr, pts in thresholds:
        if value >= thr:
            return pts
    return 0.0


def _band_inv(value: float, thresholds: list[tuple[float, float]]) -> float:
    """value 작을수록 좋음. thresholds [(max_value, points), ...] 작은 값부터."""
    for thr, pts in thresholds:
        if value <= thr:
            return pts
    return 0.0


def compute_score(m: dict) -> dict:
    """0-100 Coach Score (5축 각 0-20)."""
    # 1) Prompt clarity
    fp = m["first_prompt_chars"]
    ap = m["avg_prompt_chars"]
    sp = m["prompt_specificity"]
    cr = m["correction_rate"]
    clarity = (
        _band(fp, [(250, 5), (150, 4), (80, 3), (40, 2), (1, 1)])
        + _band(ap, [(200, 5), (120, 4), (60, 3), (30, 2), (1, 1)])
        + _band(sp, [(0.15, 5), (0.08, 4), (0.04, 3), (0.01, 2)])
        + _band_inv(cr, [(0.05, 5), (0.10, 4), (0.20, 3), (0.30, 2), (1.0, 1)])
    )

    # 2) Tool efficiency
    pr = m["parallel_rate"]
    bf = m["bash_fail_rate"]
    efficiency = (
        _band(pr, [(0.40, 10), (0.25, 8), (0.15, 6), (0.05, 4), (0.001, 2)])
        + _band_inv(bf, [(0.05, 10), (0.10, 8), (0.20, 6), (0.35, 4), (1.0, 2)])
    )

    # 3) Context economy
    sub = m["subagent_invocations"]
    reads = m["file_reads_total"]
    rrate = m["file_reread_rate"]
    sub_pts = _band(sub, [(4, 10), (2, 8), (1, 6)])
    if sub == 0 and reads < 20:
        sub_pts = 4  # 작은 세션은 패널티 약하게
    elif sub == 0 and reads < 40:
        sub_pts = 2
    economy = sub_pts + _band_inv(rrate, [(0.05, 10), (0.15, 8), (0.25, 6), (0.40, 4), (1.0, 2)])

    # 4) Planning
    pt = m["plan_tool_uses"]
    th = m["thinking_chars_total"]
    planning = (
        _band(pt, [(5, 10), (2, 8), (1, 6), (0.5, 3)])
        + _band(th, [(5000, 10), (2000, 8), (500, 6), (100, 4), (1, 2)])
    )

    # 5) Iteration health
    cor_pts = _band_inv(cr, [(0.03, 10), (0.08, 8), (0.15, 6), (0.25, 4), (1.0, 2)])
    ut = m["user_turns"]
    at = m["assistant_turns"]
    if ut == 0:
        ratio_pts = 5
    else:
        ratio = at / ut
        if 2 <= ratio <= 6:
            ratio_pts = 10
        elif 1 <= ratio < 2 or 6 < ratio <= 10:
            ratio_pts = 7
        elif 10 < ratio <= 20:
            ratio_pts = 4
        else:
            ratio_pts = 2
    health = cor_pts + ratio_pts

    axes = {
        "clarity": round(clarity, 1),
        "efficiency": round(efficiency, 1),
        "economy": round(economy, 1),
        "planning": round(planning, 1),
        "health": round(health, 1),
    }
    total = round(sum(axes.values()), 1)
    return {"axes": axes, "total": total}


def generate_tips(m: dict) -> list[dict]:
    tips: list[dict] = []
    pr = m["parallel_rate"]
    sub = m["subagent_invocations"]
    reads = m["file_reads_total"]
    edit_err = m["edit_string_not_found"]
    cr = m["correction_rate"]
    fp = m["first_prompt_chars"]
    rr = m["file_reread_count"]
    bf = m["bash_fail_rate"]
    bt = m["bash_total"]
    pt = m["plan_tool_uses"]
    th = m["thinking_chars_total"]
    at = m["assistant_turns"]

    def add(priority, key, msg):
        tips.append({"priority": priority, "key": key, "message": msg})

    if at >= 5 and pr < 0.20:
        add(1, "low_parallel",
            f"병렬 도구 호출 비율이 {pr:.0%} 입니다. 독립적인 read/grep을 한 메시지에 묶으면 시간·토큰을 아낄 수 있어요.")
    if reads >= 30 and sub == 0:
        add(1, "no_subagent",
            f"파일 read가 {reads}회 인데 서브에이전트 호출이 0회입니다. Explore 에이전트를 쓰면 메인 컨텍스트가 보호됩니다.")
    if edit_err >= 3:
        add(1, "edit_failed",
            f"Edit 실패가 {edit_err}회 발생했습니다. old_string에 주변 3-5줄을 더 포함해 unique하게 만들어 보세요.")
    if m["user_turns"] >= 4 and cr >= 0.20:
        add(1, "high_correction",
            f"되돌림 신호 비율이 {cr:.0%}입니다. 첫 프롬프트에 제약·예시·기대 출력을 한 번에 넣어두면 왕복이 줄어요.")
    if m["user_turns"] >= 1 and fp < 80:
        add(2, "short_first_prompt",
            f"첫 프롬프트가 {fp}자입니다. 효과적인 세션의 평균은 250자+ 입니다.")
    if rr >= 5:
        add(2, "file_reread",
            f"동일 파일을 {rr}회 재read 했습니다. 줄 번호·심볼명을 미리 알려주면 한 번에 끝납니다.")
    if bt >= 5 and bf >= 0.15:
        add(2, "bash_fail",
            f"Bash 실패율이 {bf:.0%}입니다. 명령 실행 전 ls/which 등으로 사전 확인을 권장합니다.")
    if at >= 8 and pt == 0:
        add(2, "no_plan",
            "긴 세션인데 Plan/TaskCreate 사용이 0회입니다. 작업 분해와 진행 추적이 명료해집니다.")
    if at >= 5 and th < 200:
        add(3, "no_thinking",
            "Extended thinking 사용량이 적습니다. 복잡한 작업에선 thinking 토큰이 정확도를 크게 올려요.")
    if sub >= 1:
        add(3, "good_subagent",
            f"서브에이전트를 {sub}회 활용했네요. 메인 컨텍스트 보호 패턴이 잘 잡혀 있습니다.")
    if pr >= 0.35:
        add(3, "good_parallel",
            f"병렬 도구 호출 비율 {pr:.0%}—매우 좋습니다.")

    tips.sort(key=lambda x: x["priority"])
    return tips


def _hook_main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        sys.exit(0)
    transcript = payload.get("transcript_path") or payload.get("transcriptPath")
    if not transcript or not os.path.exists(transcript):
        sys.exit(0)
    try:
        metrics = analyze(Path(transcript))
    except Exception:
        sys.exit(0)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    _upsert_session(metrics)
    sys.exit(0)


def _upsert_session(metrics: dict):
    sid = metrics.get("session_id")
    if not sid:
        return
    existing = []
    if SESSIONS_FILE.exists():
        for d in _safe_iter_jsonl(SESSIONS_FILE):
            if d.get("session_id") != sid:
                existing.append(d)
    existing.append(metrics)
    tmp = SESSIONS_FILE.with_suffix(".jsonl.tmp")
    with tmp.open("w", encoding="utf-8") as fh:
        for d in existing:
            fh.write(json.dumps(d, ensure_ascii=False) + "\n")
    tmp.replace(SESSIONS_FILE)


def main():
    argv = sys.argv[1:]
    if not argv:
        print(__doc__, file=sys.stderr)
        sys.exit(2)
    if argv[0] == "--hook":
        _hook_main()
        return
    p = Path(argv[0])
    metrics = analyze(p)
    print(json.dumps(metrics, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
