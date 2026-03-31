# Coder Report — TASK-005

## Status: DONE

## Task
엔트리포인트 및 cron 스크립트 구현

## 작업 내역

### 1. src/run_collector.py
- Database 인스턴스 생성 및 `init_schema()` 호출
- `collect_all(db=db)` 실행하여 모든 티커 수집
- 시작/종료 시간, 소요 시간, 결과 요약(성공/스킵/실패 건수) 로깅
- 실패 티커가 있으면 exit code 1, 치명적 오류 시 exit code 2
- `python -m src.run_collector`로 실행 가능

### 2. src/run_analyzer.py
- argparse 기반 CLI, 3개 서브커맨드 구현:
  - `analyze`: `--strategy`(필수), `--symbol`(필수), `--start-date`/`--end-date`(선택)
  - `backtest`: `--strategy`(필수), `--symbol`(필수), `--capital`(기본 10000), `--commission`(기본 0.001), `--start-date`/`--end-date`(선택)
  - `list`: 등록된 전략 목록 출력 (이름 + 설명)
- DB에서 데이터 조회 후 전략에 전달, 결과를 포맷팅하여 터미널 출력
- `python -m src.run_analyzer analyze --strategy moving_average --symbol ^GSPC` 형태로 실행 가능

### 3. run_collector.sh
- 스크립트 위치 기준으로 프로젝트 루트로 이동
- `venv/` 또는 `.venv/` 활성화 (있는 경우)
- `python -m src.run_collector` 실행
- 실행 가능 권한(+x) 설정 완료

## 검증
- 3개 파일 모두 구문 검사(py_compile, bash -n) 통과
- run_collector.sh에 실행 권한 부여 완료

## 생성/수정 파일
- `src/run_collector.py` (신규)
- `src/run_analyzer.py` (신규)
- `run_collector.sh` (신규)
