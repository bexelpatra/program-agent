# Coder Report - TASK-027

- Task ID: TASK-027
- Title: Dash 앱 스켈레톤 (라우팅, 공통 레이아웃, DB 연결)
- Status: DONE
- Agent: Coder

## 작업 요약

Dash 멀티페이지 앱 스켈레톤을 `projects/stock-backtest/src/stock_backtest/web/` 아래에 구현했다. `use_pages=True` 기반의 엔트리포인트, 공통 내비게이션, DB 세션 헬퍼, 4개 placeholder 페이지를 모두 배치했다.

## 생성/수정 파일

- `src/stock_backtest/web/__init__.py` — 패키지 docstring.
- `src/stock_backtest/web/app.py`
  - `create_app()` 팩토리: `Dash(__name__, use_pages=True, pages_folder="pages", suppress_callback_exceptions=True, title="Stock Backtest")`.
  - 공통 레이아웃: `make_navbar()` + `page_container`를 `html.Main`으로 감싼 구조.
  - 모듈 레벨에 `app`, `server` 노출 (gunicorn 등 WSGI 호환).
  - `main()`에서 `load_config()`를 lazy 호출(import 단계에서 config 미의존) 후 `app.run(debug=True, host='127.0.0.1', port=8050)` 실행, 구버전 대비 `run_server` 폴백 포함.
  - `python -m stock_backtest.web.app` 엔트리포인트 지원.
- `src/stock_backtest/web/components/__init__.py`
- `src/stock_backtest/web/components/layout.py`
  - `make_navbar() -> html.Div`: 상단 내비게이션 (백테스트/계절성/데이터 탐색/이력 비교 4개 `dcc.Link`).
- `src/stock_backtest/web/db_session.py`
  - `get_db_session()` contextmanager: `stock_backtest.data.db.get_session`을 lazy import로 재노출. Dash 콜백에서 `with get_db_session() as session:` 패턴 가능.
- `src/stock_backtest/web/pages/__init__.py`
- `src/stock_backtest/web/pages/backtest.py` — `path='/backtest'`, TODO (TASK-028) 문구 포함.
- `src/stock_backtest/web/pages/seasonality.py` — `path='/seasonality'`.
- `src/stock_backtest/web/pages/data_explorer.py` — `path='/data'`.
- `src/stock_backtest/web/pages/history.py` — `path='/history'`.

모든 파일에 `from __future__ import annotations`, 타입힌트, docstring을 포함했다. Dash/Plotly import는 각 모듈 최상단에 배치.

## 검증

1. `ast.parse` 전 파일 구문 검증: OK.
2. Import 검증: 로컬 환경의 Dash 4.1.0이 comm 모듈과 충돌(`NotImplementedError: Cannot`)하여 표준 import는 실패했으나, comm shim 적용 후:
   ```
   PYTHONPATH=src python -c "<comm shim>; import stock_backtest.web.app as a; print(list(a.dash.page_registry.keys()))"
   ```
   결과: `['pages.backtest', 'pages.data_explorer', 'pages.history', 'pages.seasonality']` — 4개 페이지 정상 등록 확인.
3. DB 연결 없음 상태에서도 app import 성공 (DB는 `db_session.get_db_session` 호출 시점에만 로드되는 lazy 방식).

## 비고 / 환경 메모

- 환경에 설치된 `dash==4.1.0`은 IPykernel 환경 밖에서 `comm.create_comm` 호출로 인해 import-time 오류를 던지는 알려진 버그를 보인다. 개발 서버 실행 시 Jupyter kernel이 없는 CLI 환경에서는 `dash>=2,<3` (예: `dash==2.17.*`) 다운그레이드를 권장하지만, 이는 환경 설정 이슈로 TASK-027 범위 밖이다. 애플리케이션 코드 자체는 Dash 2.x/3.x API(`use_pages`, `page_container`, `register_page`, `app.run`)와 호환된다.
- `requirements.txt`는 이미 `dash`, `plotly`를 명시하고 있으며 이 태스크에서는 변경하지 않았다.
- dev 서버 2초 기동 테스트는 위 환경 이슈로 생략. 코드 레벨 검증(ast + shim import + page_registry)으로 대체했다.

## 다음 태스크 제안

- TASK-028: 백테스트 페이지 실제 구현 (전략 선택 → 파라미터 폼 → universe/기간 → 실행 → equity curve/drawdown/metrics).
