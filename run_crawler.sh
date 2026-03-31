#!/bin/bash
# run_crawler.sh - 네이버증권 크롤러 자동 실행 스크립트
# cron에 등록하여 매일 09:30, 15:30에 실행

PROJECT_ROOT="/home/jai/program-agent"
LOG_DIR="${PROJECT_ROOT}/logs"
TODAY=$(date +%Y-%m-%d)
LOG_FILE="${LOG_DIR}/crawler_${TODAY}.log"

# logs 디렉토리 자동 생성
mkdir -p "${LOG_DIR}"

# 프로젝트 루트로 이동
cd "${PROJECT_ROOT}"

# 크롤러 실행 (로그 기록)
echo "========== $(date '+%Y-%m-%d %H:%M:%S') 크롤링 시작 ==========" >> "${LOG_FILE}"
python3 src/main.py >> "${LOG_FILE}" 2>&1
EXIT_CODE=$?
echo "========== $(date '+%Y-%m-%d %H:%M:%S') 크롤링 종료 (exit: ${EXIT_CODE}) ==========" >> "${LOG_FILE}"

exit ${EXIT_CODE}
