# Coder Report — TASK-036

- Task: CLI `serve` 명령 + 통합 스모크 테스트
- Status: DONE

## 변경 요약

### 1. `projects/abc-english/src/cli.py`
- `serve` 서브커맨드 추가. 옵션: `--host`, `--port`, `--reload`.
- 기본 host/port는 CLI 옵션 > `settings.yaml`의 `web.host`/`web.port` > `127.0.0.1`/`8080` 순.
- `uvicorn.run("web.app:create_app", factory=True, ...)` 로 팩토리 모드 기동.
- 팩토리에 config 경로를 전달하기 위해 `os.environ["ABC_CONFIG"] = str(Path(config_path).resolve())` 설정.

### 2. `projects/abc-english/web/app.py`
- `create_app(settings_path=None)`에서 인자가 `None`이면 `os.environ.get("ABC_CONFIG")`를 폴백으로 사용. 인자 우선 유지.
- `import os` 추가.

### 3. `projects/abc-english/config/settings.yaml`
- `web:` 블록 추가 (`host: 127.0.0.1`, `port: 8080`).

### 4. `projects/abc-english/scripts/smoke_web.py` (신규)
- 임시 포트 18767에서 `python -m uvicorn --factory web.app:create_app` 를 subprocess로 기동.
- `ABC_CONFIG` 환경변수로 설정 경로 전달, `PYTHONPATH`에 프로젝트 루트 추가.
- `/api/health` polling(최대 30s)으로 준비 대기.
- httpx로 `/`, `/static/js/{common,study,notebook,episodes}.js`, `/static/css/app.css`, `/study/TEST`, `/notebook`, `/api/episodes` 검증. `/api/episodes`는 200/500/502/503 허용(ES 미가동 대비).
- 성공 시 `SMOKE OK` + exit 0, 실패 시 exit 1.
- `atexit`으로 서버 프로세스 종료 보장 (terminate → 5s wait → kill fallback).

### 5. `projects/abc-english/README.md`
- `## 빠른 시작` 아래 "웹 UI 실행" 단락 추가: `python -m src.cli serve`, 기본 포트, 단축키(`N`, Space, 좌/우, 상/하) 안내.
- CLI 명령어 표에 `serve` 행 추가.

## 검증 결과

- `python -m py_compile src/cli.py scripts/smoke_web.py` → OK
- `python -m src.cli serve --help` → 정상 출력
- `python scripts/smoke_web.py` → 모든 엔드포인트 200, `SMOKE OK`, exit 0
  - 참고: 실행 환경에 ES가 떠 있어 `/api/episodes`도 200 반환.

## 이슈/블로커

없음.
