---
agent: coder
task_id: TASK-056
status: DONE
timestamp: 2026-04-14T22:30:00
---

## 결과 요약
SeasonalMovingAverage 를 새 DSL(`target_symbol` / `exit_action` / `rotate_symbol`)로 마이그레이션. `risky_symbol` / `safe_symbol` 제거, `seasonality_mode` → `mode` 로 개명. cash 모드는 `_CASH_` 컬럼을, rotate 모드는 `rotate_symbol` 컬럼을 쓰도록 `generate_weights` 및 `required_universe` 재작성. 웹 `_FIELD_LABEL_KO` 에 `mode`/`combine_mode`/`alpha`/`custom_months`/`election_dates` 한글 라벨 추가. smoke 3종(py_compile, params 기본값, generate_weights cash/rotate) 모두 통과.

## 변경된 파일
- projects/stock-backtest/src/stock_backtest/strategies/dynamic/moving_average/seasonal.py (수정) — 전체 DSL 교체
- projects/stock-backtest/src/stock_backtest/web/pages/backtest.py (수정) — `_FIELD_LABEL_KO` 에 5개 라벨 추가

## 파라미터 변경 요약
- 제거: `risky_symbol`, `safe_symbol`, `seasonality_mode`
- 추가: `target_symbol` (widget=asset_symbol), `exit_action: Literal["cash","rotate"]="cash"`, `rotate_symbol: str|None=None` (widget=asset_symbol), `mode` (계절성 유형; 기존 `seasonality_mode` 에서 rename)
- 유지: `fast_window`, `slow_window`, `combine_mode`, `alpha`, `custom_months`, `election_dates`
- validator: `exit_action=="rotate"` → `rotate_symbol` 필수 + `rotate_symbol != target_symbol`

## generate_weights 출력 컬럼
- cash 모드: `[target_symbol, "_CASH_"]`, 비중 `[w, 1-w]`
- rotate 모드: `[target_symbol, rotate_symbol]`, 비중 `[w, 1-w]`
- `CASH_SYMBOL` 은 `stock_backtest.backtest.engine` 에서 import, prices 에서 참조하지 않음 (엔진이 `_CASH_` 배제).

## Smoke 결과
- `python -m py_compile seasonal.py` → OK
- `SeasonalMovingAverageParams(target_symbol='SPY', mode='halloween', fast_window=50, slow_window=200, combine_mode='and', alpha=0.5)` → `cash None`
- 합성 시계열 `generate_weights` 호출: cash 모드 컬럼 = `['SPY','_CASH_']`, rotate 모드 컬럼 = `['SPY','BIL']`, 비중 합 = 1.0 확인.

## 영향받는 테스트 (tests/)
- 없음. `tests/` 에서 `risky_symbol` / `safe_symbol` / `seasonality_mode` / `SeasonalMoving` 참조 grep 결과 0건. `tests/test_seasonality_stats.py` 는 존재하지만 전략 클래스/파라미터 네이밍에 의존하지 않음.

## 이슈/블로커
없음. 단, 과거 호환이 필요한 외부 소비자(실제 DB 에 저장된 old-DSL params JSON 등)가 있다면 별도 마이그레이션 태스크가 필요할 수 있음 — 이번 태스크 범위 밖.

## 다음 제안
- SeasonalMovingAverage 의 cash/rotate 분기 및 mode rename 에 대한 단위 테스트(tester) 추가.
- web 폼에서 새 필드(`target_symbol` widget=asset_symbol, `exit_action`, `rotate_symbol`) 렌더 smoke.
