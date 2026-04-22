---
agent: coder
task_id: TASK-103
status: DONE
timestamp: 2026-04-15T12:00:00
---

## 결과 요약
CLI/문서/의존성에서 웹(Dash) 잔재를 정리했다. `scripts/run_web.sh` 삭제, README/requirements의 웹 언급 제거, `pytest-asyncio`를 `requirements-dev.txt`에 추가했다. 검증 4개 조건 모두 통과.

## 변경된 파일
- projects/stock-backtest/scripts/run_web.sh (삭제)
- projects/stock-backtest/README.md (수정 — Dash/웹 페이지 섹션 제거, V2 Reset 안내 추가, 디렉토리 트리에서 `web/` 제거, 테스트 섹션에서 `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1` 관련 문구 삭제)
- projects/stock-backtest/docs/cron.md (변경 없음 — 재확인 결과 웹/Dash/웹 URL 언급이 이미 없었음)
- projects/stock-backtest/requirements.txt (수정 — `dash`, `plotly` 제거)
- projects/stock-backtest/requirements-dev.txt (수정 — `pytest-asyncio` 추가; TASK-102 tester 지적 반영)
- projects/stock-backtest/pyproject.toml (변경 없음 — dash/plotly 의존성 원래부터 없음)

## 테스트 결과 (tester 전용)
N/A

## 이슈/블로커
없음. 완료 조건 검증 결과:
1. `ls projects/stock-backtest/scripts/run_web.sh` → not found (확인).
2. `grep -rni "dash|plotly|/backtest|run_web" README.md docs requirements.txt pyproject.toml` → 1 hit. README.md L7의 V2 Reset 안내 문장("웹(Dash) 계층은 제거되었으며") 뿐. 태스크 지시상 "V2 Reset 진행 중임을 간단히 명시하는 1~2줄 추가 권장"에 해당하므로 Coder 재량으로 예외 판단.
3. `.venv/bin/pip install --dry-run -r requirements.txt` → EXIT 0, 정상 resolve.
4. `.venv/bin/python -c "import stock_backtest"` → OK.

plotly 사용 여부는 `grep -rn "import plotly|from plotly" src tests` 로 0 hit 확인 후 requirements.txt에서 제거했다.

## 다음 제안
TASK-104 진행 가능. FastAPI/uvicorn 의존성은 지시대로 이번 태스크에서 추가하지 않았고 TASK-117 에서 처리될 것.
