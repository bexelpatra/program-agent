---
agent: coder
task_id: TASK-034
status: DONE
timestamp: 2026-04-14T00:00:00
---

## 결과 요약

사용자/개발자용 README 를 한국어로 전면 재작성했다. 기존 README 는 설치와
docker 기동만 다루던 초기 상태였으므로, 지시된 10개 섹션 구조로 교체했다.

주요 내용:
1. 프로젝트 소개 — KR 세금, FX, Timescale, 전략 registry, Dash 웹의 특징을
   architecture.md §14 / §3 / §4 / §8 근거로 요약.
2. 아키텍처 개요 — 기술 스택과 `src/stock_backtest/` 디렉토리 요점.
3. 설치 — Python 3.11+, venv, requirements (main/dev), `.env.example → .env`,
   `docker compose up -d`, `alembic upgrade head`, `scripts/seed_universe.py`,
   `scripts/seed_market_events.py`.
4. 데이터 수집 — `python -m stock_backtest.ingestion.cli` 의 실제 구현
   (`--market`, `--symbols`, `--dry-run`, `--log-level`) 과 종료 코드를 명시,
   Cron 스케줄 표 + `docs/cron.md` / `docker/cron/crontab.example` 링크.
5. 백테스트 실행 — (a) `python -m stock_backtest.web` 로 Dash 기동,
   (b) Python API 예시 (`BacktestConfig` + `BacktestEngine.run` + registry
   `get_strategy` 경유).
6. 새 전략 추가법 — `@register` + pydantic `StrategyParams` 서브클래스,
   `generate_weights` / `required_universe` 구현 샘플. 임의 코드 업로드
   불허 정책 명시.
7. 웹 페이지 안내 — 데이터 탐색 / 계절성 / 전략 백테스트 / 이력 비교
   4개 페이지를 각각 한 단락으로 설명. 실제 pages/ 모듈 docstring 내용
   기반.
8. 테스트 — `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 pytest` 와 dash pytest 플러그인
   autoload 이슈(done-log §TASK-023/026 근거) 언급.
9. 디렉토리 레이아웃 — 핵심 디렉토리만 트리화.
10. 라이선스/면책 — "투자 조언 아님" 한 줄.

실재성 검증:
- `ingestion.cli` 의 argparse 정의를 직접 확인해 `--market ALL` 포함
  choices, `--symbols`, `--dry-run`, `--log-level` 및 종료 코드를 그대로
  인용했다 (존재하지 않는 플래그 생성 없음).
- `BacktestConfig` / `BacktestEngine.run` 시그니처와 `get_strategy` 는
  `backtest/engine.py`, `strategies/registry.py` 에 존재한다.
- `scripts/seed_universe.py`, `scripts/seed_market_events.py`,
  `docs/cron.md`, `docker/cron/crontab.example` 경로 실재 확인.
- `pyproject.toml` `[tool.pytest.ini_options]` 에 `testpaths=["tests"]`,
  `pythonpath=["src"]` 확인 → README 의 `pytest` 명령 유효.

## 변경된 파일
- projects/stock-backtest/README.md (전면 재작성)

## 이슈/블로커
없음.

## 다음 제안
- `.env.example` 내용 변경이 있다면 README §3 의 "`.env` 편집" 항목에
  주요 키(DB URL, 기타 옵션)를 예시로 추가하는 후속 태스크를 고려할 만
  하다.
- CHANGELOG / 기여 가이드가 필요해지면 별도 문서로 분리 권장.
