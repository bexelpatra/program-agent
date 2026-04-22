---
agent: coder
task_id: TASK-042
status: DONE
timestamp: 2026-04-14
---

# TASK-042 Coder Report

## 결과 요약
- `_build_field_component` 를 위젯 dispatch 테이블 기반으로 리팩터. `json_schema_extra={"widget": ...}` 메타데이터가 있으면 `_WIDGET_RENDERERS` 에서 렌더러를 조회해 우선 적용하고, 없으면 기존 타입 기반 렌더링으로 폴백.
- `asset_symbol` 위젯 구현 (`_render_asset_symbol`): `AssetRepository(session).list_active()` 로 옵션 로딩, 라벨 형식 `"{name} · {symbol} [{market}]"` (name 없으면 `"{symbol} [{market}]"`), `search` 필드로 symbol/name/market 전체 검색, value 는 심볼 문자열. DB/import 실패는 try/except 로 감싸 빈 옵션으로 폴백 + `logger.warning`. 기본값이 옵션에 없으면 상단에 prepend 해 선택 상태 유지.
- `_WIDGET_RENDERERS: dict[str, Callable]` 레지스트리를 모듈 상단에 정의 (향후 `asset_symbol_list`, `date_preset` 등 확장 지점).
- `MovingAverageCrossoverParams.risky_symbol` / `safe_symbol` Field 에 `json_schema_extra={"widget": "asset_symbol"}` 추가. description 은 그대로 유지.
- `_coerce_field_value` 는 기존 `str` 분기가 asset_symbol 반환(심볼 문자열)을 처리하므로 수정 없음 (요구사항 4절과 일치).

## 변경 파일
- `projects/stock-backtest/src/stock_backtest/web/pages/backtest.py`
  - `_widget_name(finfo)` 헬퍼 추가.
  - `_render_asset_symbol(...)` 추가.
  - `_WIDGET_RENDERERS` 레지스트리 추가.
  - `_build_field_component` 시그니처에 `finfo: FieldInfo | None = None` 추가, 본문 앞단에 위젯 dispatch 블록 삽입.
  - `_strategy_form_fields` 호출부를 `_build_field_component(fname, annotation, default, finfo)` 로 업데이트.
- `projects/stock-backtest/src/stock_backtest/strategies/dynamic/moving_average/crossover.py`
  - `risky_symbol`, `safe_symbol` Field 에 `json_schema_extra={"widget": "asset_symbol"}` 추가.

## 스모크 검증
- `py_compile src/stock_backtest/web/pages/backtest.py` → ok.
- Dash app 컨텍스트에서 `from stock_backtest.web.pages import backtest` 임포트 성공, `backtest._WIDGET_RENDERERS` 에 `'asset_symbol'` 등록 확인.
- `MovingAverageCrossoverParams.model_fields['risky_symbol'].json_schema_extra` → `{'widget': 'asset_symbol'}`.
- `MovingAverageCrossoverParams.model_fields['safe_symbol'].json_schema_extra` → `{'widget': 'asset_symbol'}`.

참고: 시스템 전역 python 에서는 dash+comm 초기화 오류가 있고, `register_page` 는 app 인스턴스가 먼저 생성되어야 하므로 맨몸 import 대신 Dash app 컨텍스트에서 import 하는 방식으로 검증함 (실제 웹 앱 실행 경로와 동일).

## 이슈/블로커
- severity: none
- 없음. 기존 타입 기반 렌더링/코어션 경로는 그대로 유지되어 다른 전략의 폼 동작에는 영향 없음.

## 후속 작업 제안 (Manager 참고)
- `asset_symbol_list` 위젯 (list[str] 심볼 다중 선택) 추가 시 `_WIDGET_RENDERERS` 등록 + `_coerce_field_value` list 분기 확인 필요.
- Dropdown 옵션 로딩은 현재 렌더 시점 동기 호출이다. 전략 파라미터 필드 수가 늘거나 자산 수가 많아지면 data_explorer 처럼 lazy 콜백 방식으로 재정리 고려 (현 태스크 범위 밖).
