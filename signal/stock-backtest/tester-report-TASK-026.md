# Tester Report - TASK-026

- Task: 계절성 통계 유의성 검정 + 분석 모듈 테스트
- Status: DONE
- Date: 2026-04-14

## 작업 요약

### A) 통계 유의성 헬퍼 추가 (예외적 코드 추가 범위)
- 신규 파일: `projects/stock-backtest/src/stock_backtest/analysis/stats.py`
  - `welch_t_test(a, b) -> dict`: scipy.stats.ttest_ind(equal_var=False). 반환 dict 키 = `t`, `p_value`, `df`(Welch-Satterthwaite 근사), `mean_diff`, `n_a`, `n_b`. 표본 < 2 면 t/p/df = NaN 안전 반환. NaN 자동 제거.
  - `bootstrap_mean_diff(a, b, *, n_resamples=10_000, seed=0, alpha=0.05) -> dict`: `numpy.random.default_rng` 복원추출. 반환 dict = `mean_diff`, `ci_low`, `ci_high`(percentile CI), `pseudo_p = 2*min(P(diff>0), P(diff<0))`.
  - `bootstrap_ci(values, *, n_resamples=10_000, seed=0, alpha=0.05) -> (mean, ci_low, ci_high)`: 단일 표본 평균 부트스트랩 CI.
  - `annotate_significance(p) -> str`: "\*\*\*" (p<0.01) / "\*\*" (p<0.05) / "\*" (p<0.10) / "". NaN/None 안전.
  - 의존성: numpy, pandas, scipy.stats (t-test 전용). 타입힌트, docstring 완비.
- `analysis/__init__.py` 에 4개 함수 export 추가 (seasonality.py / political_cycle.py 는 수정하지 않음).

### B) 분석 모듈 테스트
- 신규 파일: `projects/stock-backtest/tests/test_seasonality_stats.py`
- 테스트 15개 (synthetic 10년 영업일 가격 fixture 기반):
  1. `test_daily_returns_known_series` – 알려진 시리즈 pct_change 검증.
  2. `test_monthly_effect_schema` – 12행 × 5열, win_rate 범위, count>0.
  3. `test_sell_in_may_schema` – 두 반기 샘플>0, annualized 부호 일치.
  4. `test_halloween_indicator_distribution` – buy_hold_return 에 양/음수 모두 존재.
  5. `test_welch_t_test_known_input` – a=[1..5], b=[3..7] → mean_diff=-2, t≈-2, df≈8, p<0.10.
  6. `test_welch_t_test_small_sample_returns_nan` – n<2 안전 처리.
  7. `test_welch_t_test_drops_nan` – NaN 제거 후 동일 결과.
  8. `test_bootstrap_mean_diff_reproducible_and_ci` – 같은 seed 결과 동일, 참 차이 CI 포함.
  9. `test_bootstrap_mean_diff_shifted_significant` – 평균차 ≈1, CI>0 & pseudo_p<0.05.
  10. `test_bootstrap_ci_single_sample` – 참 평균 CI 포함, 재현성.
  11. `test_bootstrap_ci_empty_returns_nan` – 빈 표본 안전.
  12. `test_annotate_significance_thresholds` – 0.009, 0.01, 0.049, 0.05, 0.099, 0.10, NaN, None 경계 검증.
  13. `test_presidential_term_year_effect_schema` – 5년 합성 데이터, index=[1..4], 스키마 검증.
  14. `test_fomc_week_effect_schema` – 스키마, t_stat 두 행 동일.
  15. `test_earnings_season_effect_schema` – 스키마, dtype(float/int) 검증.

## 실행 결과

```
$ PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest tests/test_seasonality_stats.py -v
============================= test session starts ==============================
platform linux -- Python 3.11.3, pytest-9.0.2
configfile: pyproject.toml
collected 15 items

tests/test_seasonality_stats.py::test_daily_returns_known_series PASSED
tests/test_seasonality_stats.py::test_monthly_effect_schema PASSED
tests/test_seasonality_stats.py::test_sell_in_may_schema PASSED
tests/test_seasonality_stats.py::test_halloween_indicator_distribution PASSED
tests/test_seasonality_stats.py::test_welch_t_test_known_input PASSED
tests/test_seasonality_stats.py::test_welch_t_test_small_sample_returns_nan PASSED
tests/test_seasonality_stats.py::test_welch_t_test_drops_nan PASSED
tests/test_seasonality_stats.py::test_bootstrap_mean_diff_reproducible_and_ci PASSED
tests/test_seasonality_stats.py::test_bootstrap_mean_diff_shifted_significant PASSED
tests/test_seasonality_stats.py::test_bootstrap_ci_single_sample PASSED
tests/test_seasonality_stats.py::test_bootstrap_ci_empty_returns_nan PASSED
tests/test_seasonality_stats.py::test_annotate_significance_thresholds PASSED
tests/test_seasonality_stats.py::test_presidential_term_year_effect_schema PASSED
tests/test_seasonality_stats.py::test_fomc_week_effect_schema PASSED
tests/test_seasonality_stats.py::test_earnings_season_effect_schema PASSED

============================== 15 passed in 0.51s ==============================
```

## 이슈/블로커

없음.

## 완료 조건 체크

- [x] `src/stock_backtest/analysis/stats.py` 작성
- [x] `tests/test_seasonality_stats.py` 작성
- [x] `pytest tests/test_seasonality_stats.py -v` 전부 통과 (15/15)
- [x] `signal/stock-backtest/tester-report-TASK-026.md` 작성

## 금지사항 준수

- task-board.md, architecture.md 비수정.
- `src/stock_backtest/web/`, `docker/`, 전략/엔진/데이터 소스 미접근.
- `seasonality.py`, `political_cycle.py` 는 읽기만 수행, 수정 없음.
- 예외 허용 범위(`analysis/stats.py` 신규 + `analysis/__init__.py` export 추가)만 변경.
