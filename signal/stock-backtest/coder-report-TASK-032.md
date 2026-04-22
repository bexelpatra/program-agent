# Coder Report - TASK-032

## 태스크
- Task ID: TASK-032
- Title: Cron 스케줄 설치 가이드 + 샘플 crontab
- Status: DONE

## 산출물

### 신규 파일
- `projects/stock-backtest/docs/cron.md`
  - 1) 개요 (시장별 KST 스케줄 표: KR 18:00 / US 07:00 / Crypto 09:00)
  - 2) 사전 조건 (venv, DB 기동, .env, assets 테이블)
  - 3) crontab 편집 방법 (`crontab -e`, CRON_TZ=Asia/Seoul)
  - 4) 샘플 crontab (docker/cron/crontab.example 내용 인용)
  - 5) 로그 디렉토리 생성 (`/var/log/stock_backtest/` 권한 예시)
  - 6) 문제 해결 (종료 코드 확인, `--dry-run` 수동 실행, yfinance rate limit → `min_interval_seconds` 조정, SIGPIPE 리디렉션, TZ 불일치)
  - 7) systemd timer 대안 (stock-backtest-kr.service + .timer unit 파일 예시)

### 수정 파일
- `projects/stock-backtest/README.md`
  - 맨 하단에 `## Cron 설치` 섹션 추가 (3줄: docs/cron.md 와 docker/cron/crontab.example 링크).
  - 기존 섹션 내용 변경 없음.

### 유지 파일
- `projects/stock-backtest/docker/cron/crontab.example` — TASK-011 산출물 그대로 유지, 미변경.

## 금지사항 준수 확인
- task-board.md / architecture.md: 미수정
- `src/`, `tests/`: 미수정
- `docker-compose.yml`: 미수정
- README는 "Cron 설치" 섹션만 append. 기존 섹션 원본 유지.
- crontab.example 기존 내용 미변경 (새 내용 추가 없음).

## 검증
- `docs/cron.md`는 docker/cron/crontab.example의 KR/US/Crypto 스케줄과 정확히 일치.
- systemd timer 예시에서 `OnCalendar=... Asia/Seoul` 형식 사용 (systemd 242+ 가정).
- README 링크(docs/cron.md, docker/cron/crontab.example)는 실제 파일 경로와 일치.

## 이슈/블로커
없음.
