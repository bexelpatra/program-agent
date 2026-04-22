# Coder Report — TASK-016

- Task ID: TASK-016
- Title: 벡터화 백테스트 엔진
- Status: **DONE**
- Date: 2026-04-14

## 작업 요약

`projects/stock-backtest/src/stock_backtest/backtest/` 하위에 4개 모듈을 새로 구현하고, smoke test 1건을 추가하여 세금 on/off 2개 케이스를 통과시켰다.

## 변경 파일

- `src/stock_backtest/backtest/fx.py` (신규) — `FXConverter` + `FXRateUnavailableError`. repository의 `FxRateRepository`를 재사용하고 fx_spread_bps를 편도(half-spread)로 반영. `rate_overrides` dict를 받아 테스트 시 DB 없이 동작 가능.
- `src/stock_backtest/backtest/portfolio.py` (신규) — `Position`, `Portfolio`, `InsufficientFundsError`. 멀티 통화 현금, 매수/매도, mark-to-market, 크로스-커런시 환전(스프레드 적용). 매도 시 `RealizedTrade`(KRW 환산)를 반환.
- `src/stock_backtest/backtest/engine.py` (신규) — `AssetSpec`, `BacktestConfig`, `TradeRecord`, `BacktestResult`, `PriceLoader`, `BacktestEngine`. 공통 기간 계산, repository 기반 가격 로드(`default_price_loader`), market_mode별 거래일 축 구성(STOCK/CRYPTO/MIXED), `assert_universe_coverage` 호출, 리밸런싱 스케줄(`previous_trading_day` 스냅), `Strategy.generate_weights` 호출, sell-first 거래 실행 + 세금 적용 + 연말 rollover, equity_curve 반환.
- `src/stock_backtest/backtest/cache.py` (신규) — `compute_run_hash` (SHA-256, 입력 정규화).
- `tests/test_engine_smoke.py` (신규) — 2년짜리 SPY 100% 전략 smoke. `FXConverter(rate_overrides=...)` + 주입식 `price_loader`로 DB 없이 실행. `test_smoke_no_tax`, `test_smoke_with_tax` 둘 다 PASS.

## 설계 결정 커버리지

- #3 (base_currency) — `BacktestConfig.base_currency` + `Portfolio.mark_to_market`에서 base_ccy로 일별 환산.
- #4 (환전 스프레드) — `FXConverter.convert(apply_spread=True)` 는 half-spread를 감산/가산. `Portfolio._ensure_cash`에서 리밸런싱용 환전에 spread 적용.
- #5 (market_mode) — `_build_sim_index` / `_align_prices`가 STOCK(세션 union), CRYPTO(365일), MIXED(세션 union + crypto 컬럼 forward-fill) 분기.
- #6 (공통 기간) — `_resolve_period` 가 config period ∩ 자산별 start/end.
- #7 (벡터화) — pandas 기반, 이벤트 루프 없이 거래일 loop로 리밸런싱만 이벤트 처리.
- #13 (비거래일 방어) — `assert_universe_coverage` 로 NaN 커버리지 failure 즉시 raise.
- #14 (KR tax) — `build_tax_policy(settings)` 호출, `apply_realized_gain` 결과를 base_ccy로 환전하여 현금 차감. 연말 `on_year_end` rollover, `tax_paid_by_year` dict 반환.

## Smoke test 결과

```
tests/test_engine_smoke.py::test_smoke_no_tax PASSED
tests/test_engine_smoke.py::test_smoke_with_tax PASSED
2 passed, 2 warnings in 0.59s
```

- 초기 equity ≈ initial_capital(100,000 USD) 확인.
- 최종 equity > 0 확인.
- no-tax 케이스에서 tax_paid_by_year 전 연도 0 확인.
- 세금 활성화 케이스에서 최소 1건 이상 trade 기록 확인.

## 특이사항 / 블로커

1. **pandas 버전 호환**. 로컬 환경이 pandas 2.1 이하라 `"ME"` freq를 지원하지 않아 `_build_rebalance_dates` 에서 `{"ME":"M","QE":"Q","YE":"A","Y":"A"}` legacy fallback을 넣었다. 추후 requirements에서 pandas>=2.2 고정 시 제거 가능.
2. **현금 cushion**. 초회 리밸런싱에서 목표 비중 1.0 × equity를 그대로 buy로 환산하면 수수료+슬리피지만큼 현금 부족이 발생한다. `_build_rebalance_trades`에서 equity에 `Decimal("0.995")` (50bps) 버퍼를 곱해 단순 해결했다. 엄밀한 해법은 거래단가를 역산해 현금 잔고와 정합시키는 것이지만(향후 개선), 스모크 수준에서는 충분.
3. **repository 확장 필요 (블로커)**. `OhlcvRepository.get_range`만으로 wide DataFrame을 조립하고 있다. 대용량 universe에서는 "여러 asset_id를 한 번에 가져오는 벡터 쿼리"가 있어야 병목이 없어진다. 엔진 내부 헬퍼(`default_price_loader`)로 루프하여 우회했으므로 정합성은 문제 없음. **향후 repository 확장 필요** — 예: `OhlcvRepository.get_wide(asset_ids, start, end) -> DataFrame`.
4. **배당 처리**. 배당 이벤트 기반 cash-flow는 이번 범위에 포함하지 않았다(`corporate_actions` 테이블 로드 경로 없음). 설계 #14의 dividend 경로(`apply_dividend`)는 tax 모듈에 존재하나 엔진에서는 호출하지 않는다. 추후 "배당 이벤트 주입" 태스크 필요.
5. **threshold 리밸런싱**. `rebalance_freq`에 pandas freq alias만 허용. `frequency='threshold'` (설계상 지원 예정) 는 미구현이므로 별도 태스크로 분리 필요.
6. **DB 저장 없음**. 설계 #11 캐시/저장은 TASK-018 범위. 엔진은 `run_hash`만 계산해 결과에 포함한다.

## 완료 조건 체크

- [x] engine.py / portfolio.py / fx.py / cache.py 모두 작성.
- [x] import 가능.
- [x] smoke test 1건 이상 통과 (2건 PASS).
- [x] 세금 정책 통합.
- [x] FX 환전 스프레드.
- [x] 비거래일 검증(assert_universe_coverage) 포함.
- [x] coder-report 작성.
