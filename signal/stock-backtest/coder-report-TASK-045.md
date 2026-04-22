---
task_id: TASK-045
agent: coder
status: DONE
severity: none
---

# TASK-045 백테스트 페이지 폼 UX 개선

## 변경 파일
- `projects/stock-backtest/src/stock_backtest/web/pages/backtest.py`

## 구현 내용

### 1. 파라미터 라벨 한글화
- 모듈 상단에 `_FIELD_LABEL_KO: dict[str, str]` 매핑 테이블 추가 (`risky_symbol`, `safe_symbol`, `fast_window`, `slow_window`, `window`, `windows`, `include_price`).
- `_strategy_form_fields` 의 label 생성부를 수정해 한글 라벨을 `<b>` 로, 원 필드명을 `<span color:#999 11px>(fname)</span>` 로 병기. 매핑이 없는 기존 전략 필드는 필드명 폴백 유지.

### 2. Universe 입력 Details 접기
- 기존 "Universe (symbols, comma-separated)" Label + Textarea + 설명 블록을 `html.Details([Summary("고급: Universe 수동 지정"), ...])` 로 감쌈. 기본 닫힘 상태.
- Details 상단에 "이 전략은 위에서 고른 위험자산/안전자산으로 자동 결정됩니다..." 안내 문구 추가.
- `id="bt-universe"` Textarea 는 Details 내부로 이동만 했으므로 기존 callback State 연결 그대로 유지.

### 3. 기간 입력 교체
- `dcc.DatePickerRange(id="bt-date-range", ...)` 제거.
- 두 개의 `dcc.Input(type="text", placeholder="YYYY-MM-DD")` 생성 — `id="bt-start-date"`, `id="bt-end-date"`. 초기값은 기존 default_start.isoformat() / today.isoformat().
- 프리셋 버튼 6개 추가: `bt-preset-1y/3y/5y/10y/20y/all`.
- 새 콜백 `_apply_preset` 추가 — `ctx.triggered_id` 로 분기, "전체" 는 `1990-01-01 ~ today`, 나머지는 `today - 365*years ~ today`.
- `_run_backtest` 콜백의 State 를 `("bt-date-range", "start_date"/"end_date")` → `("bt-start-date", "value")` / `("bt-end-date", "value")` 로 변경. `_run_backtest_impl` 의 `start_date[:10]` 파싱은 그대로 작동.

### 4. 안내 문구
- 전략 설명 박스는 `_strategy_form_fields` 에서 그대로 유지 (기존 코드).
- 기간 섹션 하단에 "YYYY-MM-DD 형식으로 직접 입력하거나 위 버튼으로 프리셋 적용." 얇은 회색 안내 추가.

## Smoke 검증
- `python -m py_compile src/stock_backtest/web/pages/backtest.py` → OK
- `.venv/bin/python -c "from stock_backtest.web.app import create_app; create_app(); from stock_backtest.web.pages import backtest; print('ok')"` → `ok`

웹 서버 재시작은 Manager 지시대로 수행하지 않음.

## 이슈/블로커
없음.
