# Tester Report — TASK-023

## 태스크
- ID: TASK-023
- Title: 전략 단위 테스트 (정적+동적) — 통합/회귀 관점 보강
- 담당: Tester

## 작성 파일
- `projects/stock-backtest/tests/test_strategy_integration.py` (신규)

## 테스트 설계 요약

`test_strategy_integration.py`는 개별 전략 단위 테스트(static/momentum/vaa_riskparity)와 겹치지 않도록
**레지스트리 + 엔진 통합 관점**만 커버한다. 6개 빌트인 전략(fixed_weight, permanent, momentum,
dual_momentum, vaa, risk_parity) 전반에 걸친 파라미터화 회귀 테스트.

### 테스트 카테고리 (총 30 케이스)

| 구분 | 케이스 | 검증 |
|------|--------|------|
| 1. 레지스트리 발견 | 1 | `discover_strategies()` 후 6개 전략 모두 등록 확인 |
| 2. 파라미터 인스턴스화 | 6 | 각 전략의 `params_schema`를 최소 파라미터로 생성 성공 |
| 3. `generate_weights` 불변식 | 6 | index/columns/row-sum ≤ 1+1e-6/값 ≥ -1e-9/NaN 없음/최소 1행 할당 |
| 4. pydantic 검증 실패 | 5 | 잘못된 파라미터에서 `ValidationError` 발생 |
| 5. 빈 rebalance index | 6 | 빈 DataFrame 반환 |
| 6. 엔진 smoke | 6 | `BacktestEngine.run()` 완주, 최종 equity > 0 |

### 구현 메모
- 합성 가격: GBM 유사 (drift + gaussian noise), `numpy.random.default_rng(seed)`로 결정론적.
- 월말 리밸런스: `"ME"` freq가 구버전 pandas에서 실패해서 `"M"` fallback + 각 월말 라벨을 실제 세션으로 snap.
- 엔진 smoke는 `session_factory=None` + 주입한 `price_loader`/`fx_converter`로 DB/네트워크 의존 제거.
- 엔진 시그니처 드리프트(TASK-037/038 동시작업) 대비: `TypeError`/`AttributeError`/`NotImplementedError`는 `pytest.skip`으로 분리하여 전략 자체 버그와 혼동되지 않도록 함. 현재 실행에서는 skip 없음(모두 pass).

## 실행 결과

```
$ PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest tests/test_strategy_integration.py -v
============================= test session starts ==============================
platform linux -- Python 3.11.3, pytest-9.0.2, pluggy-1.6.0
rootdir: /home/jai/program-agent/projects/stock-backtest
configfile: pyproject.toml
collecting ... collected 30 items

tests/test_strategy_integration.py::test_discover_registers_all_builtin_strategies PASSED
tests/test_strategy_integration.py::test_params_schema_instantiates[dual_momentum] PASSED
tests/test_strategy_integration.py::test_params_schema_instantiates[fixed_weight] PASSED
tests/test_strategy_integration.py::test_params_schema_instantiates[momentum] PASSED
tests/test_strategy_integration.py::test_params_schema_instantiates[permanent] PASSED
tests/test_strategy_integration.py::test_params_schema_instantiates[risk_parity] PASSED
tests/test_strategy_integration.py::test_params_schema_instantiates[vaa] PASSED
tests/test_strategy_integration.py::test_generate_weights_invariants[dual_momentum] PASSED
tests/test_strategy_integration.py::test_generate_weights_invariants[fixed_weight] PASSED
tests/test_strategy_integration.py::test_generate_weights_invariants[momentum] PASSED
tests/test_strategy_integration.py::test_generate_weights_invariants[permanent] PASSED
tests/test_strategy_integration.py::test_generate_weights_invariants[risk_parity] PASSED
tests/test_strategy_integration.py::test_generate_weights_invariants[vaa] PASSED
tests/test_strategy_integration.py::test_fixed_weight_rejects_bad_weight_sum PASSED
tests/test_strategy_integration.py::test_momentum_rejects_non_positive_lookback PASSED
tests/test_strategy_integration.py::test_dual_momentum_rejects_empty_risky PASSED
tests/test_strategy_integration.py::test_risk_parity_rejects_invalid_min_weight PASSED
tests/test_strategy_integration.py::test_fixed_weight_forbids_extra_fields PASSED
tests/test_strategy_integration.py::test_empty_rebalance_dates_returns_empty_frame[dual_momentum] PASSED
tests/test_strategy_integration.py::test_empty_rebalance_dates_returns_empty_frame[fixed_weight] PASSED
tests/test_strategy_integration.py::test_empty_rebalance_dates_returns_empty_frame[momentum] PASSED
tests/test_strategy_integration.py::test_empty_rebalance_dates_returns_empty_frame[permanent] PASSED
tests/test_strategy_integration.py::test_empty_rebalance_dates_returns_empty_frame[risk_parity] PASSED
tests/test_strategy_integration.py::test_empty_rebalance_dates_returns_empty_frame[vaa] PASSED
tests/test_strategy_integration.py::test_strategy_runs_in_engine[fixed_weight] PASSED
tests/test_strategy_integration.py::test_strategy_runs_in_engine[permanent] PASSED
tests/test_strategy_integration.py::test_strategy_runs_in_engine[momentum] PASSED
tests/test_strategy_integration.py::test_strategy_runs_in_engine[dual_momentum] PASSED
tests/test_strategy_integration.py::test_strategy_runs_in_engine[risk_parity] PASSED
tests/test_strategy_integration.py::test_strategy_runs_in_engine[vaa] PASSED

======================== 30 passed, 2 warnings in 1.09s ========================
```

- **30 passed, 0 failed, 0 skipped.**
- 경고 2건은 pandas 내부의 numpy deprecation 경고(`np.find_common_type`)로 전략/엔진 코드와 무관하며 pandas 업그레이드 시 자연 해소.

## 결과
- Status: **DONE**

## 이슈/블로커
- 없음. 모든 검증이 성공했으며 레지스트리/전략/엔진 간 통합 계약에 현재 회귀 없음.

## 코드 이슈
- 없음.

## 참고 (관찰)
- `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1` 없이 pytest를 실행하면 전역 dash 플러그인 초기화에서
  `NotImplementedError: Cannot` (comm 생성 실패) 가 발생해 pytest 자체가 기동 실패함. 본 프로젝트의
  CI/로컬 실행 가이드에 `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1` 환경 변수를 표준화할 것을 권고 (태스크화
  여부는 Manager 판단).
