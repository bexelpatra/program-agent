# Coder Report — TASK-037

- Task ID: TASK-037
- Title: `Portfolio._ensure_cash` FX-spread 부호 버그 수정
- Status: **DONE**
- Date: 2026-04-14

## 작업 요약

`tester-report-TASK-019.md` 이슈 #1에서 보고된 `_ensure_cash` 의 역방향
스프레드 적용 버그를 수정했다. 수정 전에는 `fx_spread_bps` 가 커질수록
cross-currency 거래에서 오히려 equity 가 **증가**하는 역전 현상이 있었다
(99,970 USD → 100,119 USD). 수정 후 `fx_spread_bps` 가 커질수록 equity 가
**엄격히 감소**하여 architecture decision #4 (스프레드는 포트폴리오에 손실을
부과한다) 와 부합한다.

## 변경 사항

### 1. `src/stock_backtest/backtest/fx.py`

`FXConverter.convert_for_target()` 신규 헬퍼 추가 (기존 `convert` 시그니처/
동작은 변경 없음 — 선택한 방식은 **옵션 A**).

- 입력: `target_amount` (target_ccy 기준 원하는 수취액), `source_ccy`,
  `target_ccy`, `on`, `apply_spread`.
- 동작:
  1. mid rate (`source→target`) 를 조회한 뒤 `source_mid = target_amount /
     rate` 로 중간환율 기준 필요 source 금액 계산.
  2. `apply_spread=True` 이면 `source_mid * (1 + half_spread)` 로 **source
     측**에 스프레드 비용을 가산하여 반환.
- `convert` 와 차이: `convert` 는 *to-side* 의 rate 를 악화시켜 "덜 받게"
  하는 구조인 반면, `convert_for_target` 은 "같은 target 수량을 얻기 위해
  *더 많은* source 를 지출해야 한다"는 구매자 관점. 두 함수 모두 "스프레드가
  커질수록 사용자에게 불리해진다"는 방향성을 유지한다.
- docstring 에 위 구분과 `_ensure_cash` 사용처 코멘트를 명시.

### 2. `src/stock_backtest/backtest/portfolio.py`

`_ensure_cash` 의 back-out 블록에서 `fx.convert(shortfall, ccy, src_ccy,
apply_spread=True)` 를 `fx.convert_for_target(shortfall, src_ccy, ccy,
apply_spread=True)` 로 교체. 기존 `max_from_src` 계산(`convert(src_bal,
src_ccy, ccy, apply_spread=True)`) 는 "src 버킷을 다 태우면 target 을 얼마
받는가" 로 그대로 유효하므로 유지.

버그가 재발하지 않도록 교체 지점에 상세 주석을 추가했다.

### 3. `tests/test_portfolio_fx.py` (신규)

두 개의 검증 테스트 추가:

- `test_fx_spread_monotonic_decrease_in_equity`: EUR 자산 + USD 초기 현금
  단일-자산 buy-and-hold 를 `fx_spread_bps ∈ {0, 100, 300}` 로 돌려
  `final_equity(0) > final_equity(100) > final_equity(300)` 와 base run 이
  100k 근방임을 단언.
- `test_ensure_cash_consumes_more_source_at_wider_spread`: `Portfolio.
  _ensure_cash` 를 직접 호출하여 같은 shortfall (900 EUR) 에 대해 spread 가
  1/100/300bps 로 커질수록 소진되는 USD 양이 엄격히 증가하고, 0bps 에선
  mid-rate 가격 (1000 USD) 에 근사함을 확인.

## 검증

```
$ pytest tests/test_portfolio_fx.py tests/test_engine_regression.py -v
...
tests/test_portfolio_fx.py::test_fx_spread_monotonic_decrease_in_equity PASSED
tests/test_portfolio_fx.py::test_ensure_cash_consumes_more_source_at_wider_spread PASSED
tests/test_engine_regression.py::test_all_cash_no_trades_flat_equity PASSED
tests/test_engine_regression.py::test_buy_and_hold_doubles_with_costs PASSED
tests/test_engine_regression.py::test_monthly_rebalance_maintains_60_40 PASSED
tests/test_engine_regression.py::test_fx_spread_has_effect_on_cross_currency_rebalance PASSED
tests/test_engine_regression.py::test_missing_price_raises_missing_price_error PASSED
tests/test_engine_regression.py::test_tax_on_below_deduction_no_tax PASSED
tests/test_engine_regression.py::test_tax_off_vs_on_same_scenario PASSED
tests/test_engine_regression.py::test_crypto_mode_includes_weekends PASSED
tests/test_engine_regression.py::test_known_good_buy_and_hold_analytical PASSED

11 passed, 2 warnings
```

`test_engine_regression.py::test_fx_spread_has_effect_on_cross_currency_rebalance`
는 tester-report 작성 당시 '크기만 보고 부호는 미검증' 으로 남아있던 케이스
이나, 수정 후에도 magnitude (delta > 50) 조건을 충족하여 기존 assertion
을 깨지 않는다. 방향성 검증은 신규 `test_fx_spread_monotonic_decrease_in_
equity` 가 담당한다.

## 미해결 이슈 / 범위 외

- tester-report 이슈 #2 (engine.py 의 현금 cushion 하드코딩, `equity *
  Decimal("0.995")`) 는 engine.py 가 TASK-038 담당이고 금지 사항에 명시되어
  있어 이번 태스크 범위에서 제외. 단, 이번 수정으로 spread 손실이 올바르게
  source 측에 부과되므로, 300bps 같은 큰 spread 에서 `InsufficientFundsError`
  가 재발할 수 있다 — TASK-038 에서 cushion 동적 산출이 필요하다는 점을
  재확인.

## 변경 파일 목록

- `projects/stock-backtest/src/stock_backtest/backtest/fx.py` (수정: 헬퍼 추가)
- `projects/stock-backtest/src/stock_backtest/backtest/portfolio.py` (수정: `_ensure_cash`)
- `projects/stock-backtest/tests/test_portfolio_fx.py` (신규)

## 완료 조건 체크

- [x] portfolio.py 의 FX-spread 부호 버그 수정
- [x] fx.py 에 `convert_for_target` 헬퍼 추가 (옵션 A), 기존 `convert` 시그니처 보존
- [x] docstring / 인라인 주석으로 두 헬퍼의 역할과 방향 차이 명시
- [x] `tests/test_engine_regression.py` 9/9 통과
- [x] 신규 `tests/test_portfolio_fx.py` 2/2 통과 (monotonic decrease + source-drain monotonicity)
- [x] 금지 파일 미변경 (engine.py, test_engine_regression.py, test_ingestion_pipeline.py, test_run_store.py, strategies/, web/, data/repository.py)
- [x] coder-report 작성
