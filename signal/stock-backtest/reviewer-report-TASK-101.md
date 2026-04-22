---
task_id: TASK-101
verdict: PASS
---

# Reviewer Report — V2 Reset 재검증 (R1~R5 반영 확인)

이전 라운드에서 NEEDS_REVISION 5건(R1~R5)을 지적했고, Manager 가 반영했다고 주장. 이번 라운드는 task-board 의 현재 문구와 실제 파일/설정의 독립 대조만 수행.

검증 자료:
- `signal/stock-backtest/task-board.md` (TASK-101, 102, 103, 111, 117 행)
- `projects/stock-backtest/requirements.txt`, `pyproject.toml`
- `projects/stock-backtest/tests/` ls
- `/home/jai/.a_service_control/services.yaml`

---

## R1 — TASK-117 API 포트 명시 → PASS

태스크 본문 발췌:
> **서버 포트 `8051` 고정** (기존 8050 웹은 삭제됨), `scripts/run_api.sh` 추가, `services.yaml` 에 `stock-backtest-api` 엔트리 등록 (port: 8051, depends_on: [stock-backtest-db])

- 포트 8051 을 본문과 services.yaml 등록 항목 양쪽에 명시. 측정 가능.
- 충돌 검사: services.yaml 현재 사용 포트(4000/11434/9200/9300/5432/8050/8000/8081/3001/3002/2222) 와 8051 충돌 없음. 8050 은 R4 에서 삭제 대상이라 향후에도 충돌 없음.

## R2 — TASK-111 의 의존성/책임 분리 → PASS

현재 문구:
> 타입 정의 자체는 독립적이며, 엔진/저장소의 `"_CASH_"` 문자열 경로 치환은 TASK-115에서 수행

- `Depends On: -` 로 변경 확인.
- 엔진 치환 책임이 TASK-115 본문("엔진 `_CASH_` 문자열 경로 전수 제거 + `AssetRef` 기반으로 재배선")에 정확히 위치. 책임 경계 명확.

## R3 — TASK-101 완료 조건 구체화 → PASS

현재 문구의 완료 조건 3개 모두 측정 가능:
1. `ls projects/stock-backtest/src/stock_backtest/web` 가 not found
2. `grep -r "stock_backtest.web\|from .web\|stock-backtest-web" projects/stock-backtest /home/jai/.a_service_control/services.yaml` 0 hit
3. `python -c "import stock_backtest"` 성공

services.yaml 까지 grep 범위에 포함시킨 점도 R1 의 `stock-backtest-web` 블록 제거와 일관됨. PASS.

## R4 — TASK-103 run_web.sh + dash/plotly 정리 → PASS

현재 문구:
> (a) `scripts/run_web.sh` 삭제, (b) `README.md` 에서 웹/대시보드/`/backtest` URL 언급 제거, (c) `docs/cron.md` 에서 웹 관련 언급 제거, (d) `requirements.txt`/`pyproject.toml` 에서 `dash`, `dash-*`, `plotly`(다른 곳에서 쓰이지 않으면) 의존성 제거.
> 완료 조건: (1) `grep -ri "dash\|plotly\|/backtest\|run_web" projects/stock-backtest/{README.md,docs,requirements.txt,pyproject.toml}` 0 hit, (2) `pip install -r requirements.txt` dry-run 성공

실제 환경 검증:
- `requirements.txt` 에 `dash`, `plotly` 두 행 실존 확인 → 삭제 대상 매칭 정확.
- `pyproject.toml` 에는 의존성이 선언되어 있지 않으나(현재 dependencies 키 없음), 향후 추가될 가능성을 대비한 grep 검증은 무해.

## R5 — TASK-102 테스트 명시 + pytest collect 통과 → PASS

현재 문구:
> 테스트 파일: `tests/test_momentum.py`, `tests/test_vaa_riskparity.py`, `tests/test_static_strategies.py`, `tests/test_strategy_integration.py` (통합 테스트는 V2 에서 재설계), `tests/test_seasonality_*` (seasonal 전략 연동 부분만).
> 완료 조건: (1) 위 파일 모두 부재, (2) `pytest --collect-only` 에러 없음, (3) `python -c "from stock_backtest.strategies import list_strategies; print(list_strategies())"` 가 `simple_moving_average`, `fixed_weight` 2개만 반환

실제 `tests/` ls 결과 4개 파일 모두 실존 확인:
- `test_momentum.py` ✓
- `test_vaa_riskparity.py` ✓
- `test_static_strategies.py` ✓
- `test_strategy_integration.py` ✓
- `test_seasonality_stats.py` 도 실존 (괄호 주석 "seasonal 전략 연동 부분만" 으로 부분 삭제 범위 명시) ✓

추가 관찰: `test_engine_regression.py`, `test_portfolio_fx.py`, `test_run_store.py` 등은 V2 엔진 재배선(TASK-115) 후 골든 스냅샷(TASK-121)으로 대체될 가능성이 있으나, 본 태스크 범위(전략 + seasonal 연동) 외이므로 R5 판정에는 무관. 만약 TASK-115 이후 collect 가 깨지면 그때 별도 태스크로 처리 가능.

---

## 종합 판정 — PASS

R1~R5 모두 task-board 본문에 정확히 반영. 외부 자료(requirements.txt, tests/, services.yaml)와 교차 검증한 결과 모순 없음. Manager 는 Coder 호출(TASK-101 부터)을 진행해도 좋다.

### 후속 라운드에서 주의할 사소 사항 (이번 라운드 차단 사유 아님)

- TASK-115 가 엔진 `_CASH_` 경로를 재배선한 뒤, `test_engine_*`, `test_portfolio_fx.py`, `test_run_store.py` 의 호환성을 별도 확인할 필요. 필요 시 골든 스냅샷(TASK-121) 범위에서 대체.
- TASK-117 의 `STOCK_BACKTEST_CORS_ORIGINS` 환경변수는 services.yaml 의 env 섹션에 향후 노출될 수 있음 — 등록 단계에서 누락되지 않도록 Coder 지시 시 환기.
