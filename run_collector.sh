#!/usr/bin/env bash
# cron 실행용 Collector 셸 스크립트.
# 프로젝트 루트로 이동하고, venv가 있으면 활성화한 뒤 collector를 실행한다.

set -euo pipefail

# 프로젝트 루트 디렉토리 (이 스크립트가 위치한 곳)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# venv 활성화 (있는 경우)
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
elif [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
fi

# Collector 실행
python -m src.run_collector
