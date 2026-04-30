#!/usr/bin/env bash
# Claude Coach Stop 훅을 ~/.claude/settings.json 에 등록.
# 멱등(이미 있으면 갱신만), 백업 자동 생성, 비차단 보장.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PY="${PYTHON:-/home/jai/anaconda3/bin/python3}"
SETTINGS="${HOME}/.claude/settings.json"
ANALYZER="${ROOT}/analyzer.py"
HOOK_CMD="${PY} ${ANALYZER} --hook"

if [[ ! -x "${PY}" ]]; then
  echo "[install] python interpreter ${PY} 를 실행할 수 없습니다." >&2
  exit 1
fi
if [[ ! -f "${ANALYZER}" ]]; then
  echo "[install] ${ANALYZER} 가 없습니다." >&2
  exit 1
fi

mkdir -p "${HOME}/.claude"
if [[ ! -f "${SETTINGS}" ]]; then
  echo "{}" > "${SETTINGS}"
fi

BACKUP="${SETTINGS}.bak.$(date +%Y%m%d-%H%M%S)"
cp "${SETTINGS}" "${BACKUP}"
echo "[install] 기존 settings 백업: ${BACKUP}"

"${PY}" - "$SETTINGS" "$HOOK_CMD" <<'PYEOF'
import json, sys
from pathlib import Path

settings_path = Path(sys.argv[1])
hook_cmd = sys.argv[2]

try:
    data = json.loads(settings_path.read_text(encoding="utf-8") or "{}")
except json.JSONDecodeError:
    print(f"[install] 기존 settings.json 파싱 실패 — 새 파일로 덮어씁니다.", file=sys.stderr)
    data = {}

hooks = data.setdefault("hooks", {})
stop_list = hooks.setdefault("Stop", [])

# 같은 명령이 이미 등록돼 있으면 그대로 둠
already = False
for entry in stop_list:
    if not isinstance(entry, dict):
        continue
    for h in entry.get("hooks", []) or []:
        if isinstance(h, dict) and h.get("type") == "command" and h.get("command") == hook_cmd:
            already = True
            break
    if already:
        break

if not already:
    stop_list.append({
        "matcher": "",
        "hooks": [
            {"type": "command", "command": hook_cmd}
        ],
    })

settings_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("[install] Stop 훅 등록 " + ("이미 존재 (변경 없음)" if already else "완료"))
PYEOF

echo "[install] 끝났습니다. 다음 Claude Code 세션이 끝날 때 자동으로 분석됩니다."
echo "[install] 대시보드: ${PY} ${ROOT}/server.py 후 http://127.0.0.1:8765/ 접속"
