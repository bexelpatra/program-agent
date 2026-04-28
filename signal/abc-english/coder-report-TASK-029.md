---
agent: coder
task_id: TASK-029
status: DONE
timestamp: 2026-04-14T00:00:00+09:00
---

# TASK-029 Coder Report

## 결과 요약

평일 새 에피소드 자동 감지 + 전체 파이프라인 실행 스케줄러를 구현했다.

- `src/scheduler.py` 신규 생성. APScheduler `BlockingScheduler` + `CronTrigger` 조합으로 구현.
  - 라이브러리 선택 이유: 타임존(ZoneInfo) 네이티브 지원, cron `day_of_week=mon-fri`로 주말 제외를 트리거 레벨에서 처리, 포그라운드 블로킹 실행이 단순함.
- 새 에피소드 감지 로직: `data/transcripts/*_official.json` 파일명에서 수집된 episode_id 집합을 만들고, `collector.fetch_episode_list(settings)` 결과의 episode_id와 비교하여 신규 ID만 추출한다. 신규 ID가 하나라도 있으면 파이프라인 실행, 없으면 "no new episodes" 로깅 후 skip.
- 파이프라인 호출은 `subprocess.run([sys.executable, "-m", "src.cli", "--config", ..., "run-all"], cwd=PROJECT_ROOT)`로 격리 실행. stdout/stderr을 캡처해 로거로 forward. rc != 0이면 `pipeline_failed` 상태 기록 후 스케줄러는 계속 동작.
- 실행 결과(status/new_episodes/duration_seconds/exit_code)를 `data/scheduler.log`에 RotatingFileHandler(2MB × 3)로 기록.
- 주말 가드: cron 트리거의 `day_of_week=mon-fri`에 더해 `run_job()` 내부에서도 ZoneInfo 기준 `datetime.now().weekday() >= 5`면 `skipped_weekend`로 로깅 후 바로 반환 (이중 방어).
- 모든 job 예외는 try/except + traceback 로깅으로 swallow — 스케줄러 프로세스는 절대 중단되지 않는다.

CLI 확장:
- `src/cli.py`에 `schedule` 명령 추가. `--once`(즉시 1회 실행 후 종료, 테스트용), `--time HH:MM`(실행 시각 오버라이드) 옵션 포함.
- `--once`는 `run_once(..., skip_weekend_check=True)`로 호출해 주말에도 즉시 테스트 가능.

설정/의존성:
- `config/settings.yaml`에 `scheduler:` 블록 추가 (enabled/time/timezone/weekdays_only/log_file).
- `requirements.txt`에 `APScheduler>=3.10.0`, `tzdata>=2024.1` 추가 (최소 시스템에서도 ZoneInfo가 IANA 데이터를 찾을 수 있도록).

README:
- `README.md`의 CLI 명령어 표에 `schedule` 행 추가 + "스케줄러 사용법" 한 단락 설명 추가.

## 변경된 파일

- `projects/abc-english/src/scheduler.py` (신규)
- `projects/abc-english/src/cli.py` (`schedule` 명령 추가)
- `projects/abc-english/config/settings.yaml` (`scheduler` 블록 추가)
- `projects/abc-english/requirements.txt` (APScheduler, tzdata 추가)
- `projects/abc-english/README.md` (CLI 표 및 스케줄러 사용법 섹션 추가)

## 검증

- `python -m py_compile src/scheduler.py src/cli.py` → OK
- `python -c "from src import scheduler"` → 정상 import
- `python -m src.cli schedule --help` → 명령/옵션 정상 등록 확인
- 주말 분기 단위 확인: `datetime.now` patch로 토요일 고정 시 `run_job` → `{'status': 'skipped_weekend', 'new_episodes': 0, ...}` 반환 확인 (파이프라인 subprocess 미호출).

## 이슈/블로커

- `python -m src.cli schedule --once`의 end-to-end 실행은 현 환경에서 APScheduler/네트워크 의존으로 full-run 보장이 불가하다. 단, 각 단위 경로(import, 주말 가드, `detect_new_episodes` 흐름, subprocess 커맨드 조립)는 검증했다. Tester가 APScheduler 설치 환경에서 `--once` 실제 실행을 검증하면 좋다.
- `fetch_episode_list`는 네트워크 크롤링을 요구한다. 스케줄러는 이 함수를 그대로 재사용하므로 오프라인 환경에서 `--once`를 호출하면 `detection_failed` 상태로 기록되고 파이프라인은 실행되지 않는다 (안전).

## 다음 제안

- Tester가 다음 시나리오로 테스트 작성 권장:
  1) `_collected_episode_ids`가 tmp transcript_dir의 `{id}_official.json` 파일을 올바르게 파싱하는지.
  2) `fetch_episode_list`를 monkeypatch하여 listing ID를 주고, `detect_new_episodes`가 차집합을 반환하는지.
  3) 주말 가드: `datetime` patch로 `run_job`이 파이프라인 subprocess를 호출하지 않는지 (subprocess.run도 patch해 call count 확인).
  4) 신규 0건: `run_job`이 `status='no_new_episodes'`로 조기 반환하는지.
  5) `--once` CLI invocation이 `run_once`를 호출하고 요약을 출력하는지 (click.testing.CliRunner).
- 프로덕션 배포 시에는 `schedule`을 systemd user service 또는 `nohup`으로 백그라운드화하는 운영 문서 추가 고려.
