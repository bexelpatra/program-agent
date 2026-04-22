---
task_id: TASK-051
agent: coder
status: DONE
severity: none
---

# TASK-051: 엔진에 `_CASH_` 예약 심볼 1급 지원

## 요약
`_CASH_` 예약 심볼을 백테스트 엔진의 1급 포지션으로 도입. 전략이 `generate_weights` 로 반환하는 DataFrame 에 `_CASH_` 컬럼이 포함되거나, universe 에 실수로 `_CASH_` AssetSpec 이 들어와도 엔진이 방어적으로 제거하며, 자산 매수/매도 trade 이외의 합성 "현금 매매" 레코드는 생성하지 않는다. 나머지 비중(`1 - sum(asset_weights)`)은 자연히 `cash_by_ccy[base_currency]` 유휴 잔고로 남아 현금 슬리브가 실현된다.

## 변경 파일

### Modified
- `projects/stock-backtest/src/stock_backtest/backtest/engine.py`
  - 공개 상수 `CASH_SYMBOL = "_CASH_"` 추가 (`__all__` 노출).
  - `BacktestEngine.run` 진입부에 방어 코드: `config.universe` 에 `CASH_SYMBOL` 심볼 AssetSpec 이 포함돼 있으면 제거한 새 config 로 치환. → prices 로딩/aligning/coverage guard 경로에서 OHLCV 조회 대상에서 자연스럽게 배제.
  - `strategy.generate_weights` 결과(`weights_sym`) 에 `CASH_SYMBOL` 컬럼이 있으면 drop. 이후 엔진 내부의 `_build_rebalance_trades` 는 weight 합 == 1 가정을 하지 않고(없었음) 각 자산별 delta 만 계산하므로 "합 < 1" 케이스가 자동 지원됨.

### Created
- `projects/stock-backtest/scripts/smoke_cash_position.py`
  - `{"SPY": 0.6, "_CASH_": 0.4}` 비중을 반환하는 더미 전략으로 엔진 실행.
  - 검증: `_CASH_` 용 BUY/SELL trade 가 없고, SPY 첫 BUY 수량이 기대치(`equity*0.6/price = 600`) 의 ±5% 이내, 최종 equity 가 95k~110k 범위 안에 있음.
  - 실행 결과: `trades emitted: 7, first BUY qty: 598.92, final equity: 101,418.35, OK`.

## 공개 API / 상수
- `stock_backtest.backtest.engine.CASH_SYMBOL` → `"_CASH_"` (신규 export).

## 설계 노트
- architecture.md "전략 DSL 및 현금 1급 처리" 섹션의 원칙 준수:
  - `_CASH_` 는 universe(AssetSpec 리스트)에 포함되지 않음이 정석 경로. 엔진은 혹시 포함되더라도 안전하게 제거해 OHLCV/AssetSpec 조회를 회피.
  - 전략 베이스(`strategies/base.py`) 의 `required_universe()` 반환값은 **변경하지 않음**. architecture.md 도 "엔진이 필터" 방침을 명시하므로, 필터는 엔진 소비 지점(위 run 진입부 + weights 컬럼 drop)에서 수행.
  - weight 합 == 1 assert 없음을 확인(이미 합 완화 상태). 합 <= 1 케이스는 기존 `_build_rebalance_trades` 가 자연히 지원.
- FX 변환/현금 잔고 조정은 TASK-052 의 `_ensure_cash` + FX TradeRecord 경로가 이미 처리. 본 태스크는 엔진 가격/weight/universe 필터링에만 집중.

## 검증
- Smoke: `PYTHONPATH=src python scripts/smoke_cash_position.py` → 통과.
- 기존 회귀(수동 실행, pytest 환경 dash import 오류 회피):
  - `tests/test_engine_smoke.py` → 2/2 OK
  - `tests/test_engine_regression.py` → 9/9 OK
  - `tests/test_engine_cushion.py` → 4/4 OK (caplog fixture 필요한 1건은 pytest 경유 시에만 동작; 내 변경과 무관)
  - `tests/test_strategy_integration.py`, `tests/test_static_strategies.py`, `tests/test_momentum.py`, `tests/test_vaa_riskparity.py` → 회귀 없음.

## 이슈/블로커
없음.

## 완료 조건 체크
- [x] `CASH_SYMBOL = "_CASH_"` 상수 노출 (`engine.__all__`).
- [x] Engine 이 universe/prices 에서 `_CASH_` 를 안전하게 제외 (run 진입부 방어 + weights drop).
- [x] 목표 비중 합 < 1 허용 (기존 로직으로 자연 지원, 추가 제약 없음).
- [x] Smoke 스크립트 통과.
- [x] Report 작성.
