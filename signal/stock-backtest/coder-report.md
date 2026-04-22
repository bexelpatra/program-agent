---
task_id: TASK-005
status: DONE
agent: coder
---

# Coder Report - TASK-005

## 작업 범위
config/defaults.yaml 작성 + Pydantic v2 기반 설정 로더(config.py) 구현.

## 산출물
- `projects/stock-backtest/config/defaults.yaml` (신규)
- `projects/stock-backtest/src/stock_backtest/config.py` (신규)

## 설계 요약

### defaults.yaml
architecture.md §4, §7, §9, §13, §14 근거. 최상위 키:
- `base_currency`, `market_mode`
- `costs` (commission/slippage/fx_spread_bps + `market_overrides: {KR, US, CRYPTO}`)
- `rebalance` (frequency: pandas offset alias | threshold, threshold_pct)
- `calendars` (KR→XKRX, US→XNYS, CRYPTO→24/7)
- `crypto_daily_cutoff_utc`
- `tax` (enabled/profile/profiles with `kr_resident`, `none`)
- `ingestion` (retry_max, retry_backoff_seconds, rate_limit, reject_close_zero_or_null)
- `reproducibility` (stale_run_warning)

단위 표기(bps/ms/sec/KRW) 일관. 시장별 오버라이드 미설정 항목은 상위 값 상속.

### config.py
- Pydantic v2 모델: `Settings`, `CostsConfig`, `MarketCostOverride`, `CostsResolved`, `RebalanceConfig`, `TaxConfig`, `TaxProfile`, `IngestionConfig`, `RateLimitConfig`, `ReproducibilityConfig`.
- `extra="forbid"`로 오타 방지 (TaxProfile은 확장 허용).
- 검증 규칙:
  - bps/ms 필드는 `NonNegativeFloat` / `NonNegativeInt`.
  - `market_mode` Literal["STOCK","CRYPTO","MIXED"].
  - `rebalance.frequency` Literal["D","W","ME","Q","Y","threshold"]; `frequency='threshold'`인데 `threshold_pct` 미지정 시 ValidationError.
  - `tax.enabled=true`이고 `profile`이 `profiles`에 없으면 ValidationError.
- 로더:
  - `load_config(path=None)` — path 인자 > `STOCK_BACKTEST_CONFIG` env > 기본 경로 `Path(__file__).parents[2]/config/defaults.yaml`.
- 편의 함수:
  - `get_costs(settings, market) -> CostsResolved`: 상위 디폴트 + 시장 오버라이드 머지. 미등록 market은 상위 디폴트 그대로.
  - `get_tax_profile(settings) -> TaxProfile | None`: `enabled=false`면 None.

## 스모크 검증 결과 (전체 통과)

| # | 검증 | 기대 | 실제 |
|---|---|---|---|
| 1 | `load_config()` | Settings 반환 | OK, base_currency=USD, market_mode=STOCK |
| 2a | `get_costs(s,'KR')` | (10,28,5,20) | (10.0,28.0,5.0,20.0) |
| 2b | `get_costs(s,'US')` | (5,5,3,20) | (5.0,5.0,3.0,20.0) |
| 2c | `get_costs(s,'CRYPTO')` | (25,25,15,20) | (25.0,25.0,15.0,20.0) |
| 2d | `get_costs(s,'UNKNOWN')` | (15,15,5,20) (상속) | (15.0,15.0,5.0,20.0) |
| 3 | `get_tax_profile(s)` | kr_resident 값 | overseas_cg=0.22, deduction=2,500,000, dividend=0.154, crypto_enabled=True, crypto_cg=0.22 |
| 4 | tax.enabled=false 후 `get_tax_profile` | None | None |
| 5 | `costs.commission_buy_bps=-5` | ValidationError | ValidationError (greater_than_equal) |
| 6 | `rebalance.frequency='threshold'` + `threshold_pct=None` | ValidationError | ValidationError |
| 7 | `market_mode='BOGUS'` | ValidationError | ValidationError |
| 8 | `tax.profile='missing'` + `profiles={}` | ValidationError | ValidationError (profile not found) |

## 이슈/블로커
없음.

## 완료 조건 체크
- [x] defaults.yaml 생성 (architecture.md §4/§7/§14 반영, 주석 충실)
- [x] config.py 설정 로더 + Pydantic 모델 구현
- [x] `load_config`, `get_costs`, `get_tax_profile` 구현
- [x] 스모크 검증 8개 항목 전체 통과
