---
agent: coder
task_id: TASK-102
status: DONE
timestamp: 2026-04-15T15:21:03+09:00
---

# TASK-102 — 불필요 전략 + 관련 테스트 삭제

## 결과 요약

V2 Reset 범위 외 전략 9개 파일과 관련 테스트 4개 파일을 모두 삭제했다.
잔존 전략은 `simple_moving_average` 와 `fixed_weight` 두 개뿐이며
레지스트리 자동 스캔 결과가 정확히 `['fixed_weight', 'simple_moving_average']`
임을 확인했다. `pytest --collect-only` 118 tests 수집에서 ImportError /
ModuleNotFoundError 는 발생하지 않았다.

## 변경된 파일

### 삭제된 전략 소스 (9개)
- `projects/stock-backtest/src/stock_backtest/strategies/dynamic/momentum.py`
- `projects/stock-backtest/src/stock_backtest/strategies/dynamic/dual_momentum.py`
- `projects/stock-backtest/src/stock_backtest/strategies/dynamic/risk_parity.py`
- `projects/stock-backtest/src/stock_backtest/strategies/dynamic/vaa.py`
- `projects/stock-backtest/src/stock_backtest/strategies/dynamic/moving_average/crossover.py`
- `projects/stock-backtest/src/stock_backtest/strategies/dynamic/moving_average/multi_crossover.py`
- `projects/stock-backtest/src/stock_backtest/strategies/dynamic/moving_average/seasonal.py`
- `projects/stock-backtest/src/stock_backtest/strategies/dynamic/moving_average/_common.py`
- `projects/stock-backtest/src/stock_backtest/strategies/static/permanent.py`

### 삭제된 테스트 (4개)
- `projects/stock-backtest/tests/test_momentum.py`
- `projects/stock-backtest/tests/test_vaa_riskparity.py`
- `projects/stock-backtest/tests/test_static_strategies.py`
- `projects/stock-backtest/tests/test_strategy_integration.py`

### 수정된 파일 (3개)
- `projects/stock-backtest/src/stock_backtest/strategies/dynamic/moving_average/simple.py`
  - `_common` 삭제로 인한 의존성 제거. `rolling_mean` 헬퍼를 모듈 내부에 인라인.
- `projects/stock-backtest/src/stock_backtest/strategies/dynamic/moving_average/__init__.py`
  - 삭제된 하위 모듈(`_common`, `crossover`, `seasonal`)을 언급하던 docstring 을 V2 Reset 기준으로 축소.
- `projects/stock-backtest/src/stock_backtest/strategies/dynamic/__init__.py`
  - docstring 에서 삭제된 전략군(모멘텀/듀얼모멘텀/VAA/리스크패리티) 언급 제거.
- `projects/stock-backtest/src/stock_backtest/strategies/static/__init__.py`
  - docstring 에서 `permanent` 언급 제거.

### 참고 (건드리지 않음)
- `tests/test_seasonality_stats.py` 는 `analysis.seasonality` 분석 모듈만 사용하고
  `SeasonalMovingAverage` 전략을 import/참조하지 않아 그대로 유지.
- `strategies/base.py`, `strategies/registry.py`, `strategies/__init__.py` 은 의도대로 보존.

## 검증 결과

1. 파일 부재 확인

   ```
   dynamic/           → __init__.py, moving_average/
   dynamic/moving_average/ → __init__.py, simple.py
   static/            → __init__.py, fixed_weight.py
   ```

   tests/ 에서 `test_momentum.py`, `test_vaa_riskparity.py`, `test_static_strategies.py`, `test_strategy_integration.py` 모두 부재 확인.

2. pytest collect-only (venv 에 pytest 가 없어서 `pip install pytest` 로
   설치 후 실행)

   ```
   ========================= 118 tests collected in 1.08s =========================
   ```

   ImportError / ModuleNotFoundError 없음.

3. 레지스트리 스캔 결과

   ```
   $ .venv/bin/python -c "from stock_backtest.strategies.registry import list_strategies, discover_strategies; discover_strategies(); print(sorted(list_strategies()))"
   ['fixed_weight', 'simple_moving_average']
   ```

   정확히 2개, 이름 일치.

## 이슈/블로커

- 없음. 다만 아래는 참고 사항이다.
- **venv 에 pytest 미설치**: 검증을 위해 `pip install pytest`(pytest-9.0.3) 를
  `.venv` 에 추가 설치했다. 프로젝트의 `requirements.txt` 등 의존성 선언과
  어긋날 수 있으니, TASK-103(docs/requirements 정비) 범위에서 pytest 를
  `requirements-dev.txt` 등에 명시할지 검토 필요.
- **`list_strategies()` 는 `discover_strategies()` 를 먼저 호출해야 채워진다.**
  task 완료 조건 예시에서 "정확히 `['fixed_weight', 'simple_moving_average']`"
  라고 기술되어 있는데, `discover_strategies()` 호출 없이 `list_strategies()`
  만 부르면 `[]` 가 반환된다 (기존 동작 그대로). 이는 TASK-102 의 변경과
  무관하며 레지스트리 설계 그대로다.

## 다음 제안

- TASK-103 에서 README / requirements.txt / pyproject 갱신 시
  pytest 등 개발 의존성 분리 정비를 함께 처리.
- engine / CLI / web 쪽에서 레지스트리를 어떻게 호출하는지 (특히
  `discover_strategies()` 를 한 번은 호출하는지) 확인이 필요하면
  후속 태스크에서 추적. 본 태스크 범위에서는 engine 내부가 아직
  삭제된 심볼을 import 하는지 grep 으로 전수 확인했고, 잔존 참조는
  없다 (`seed_universe.py` 의 "Momentum" 문자열은 ETF 설명 텍스트,
  `migrations/0001_initial_schema.py` 의 "seasonality" 는 analysis
  모듈 지칭, `analysis/seasonality.py` 는 전략과 무관).
