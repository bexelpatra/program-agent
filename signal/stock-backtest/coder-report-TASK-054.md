---
agent: coder
task_id: TASK-054
status: DONE
timestamp: 2026-04-14T00:00:00
---

## 결과 요약
- `_load_asset_options()` 가 `_CASH_` 가상 자산 옵션을 옵션 리스트 최상단에 prepend 하도록 수정. `asset_symbol`/`asset_symbol_list`/`asset_weight_map` 세 위젯 모두 공통 헬퍼를 통해 자동 노출.
- `FixedWeight`/`Momentum`/`DualMomentum`/`VAA` 전략이 `_CASH_` 를 validator 에서 허용하고 런타임에서 "가격 1.0 상수 시계열" 합성으로 처리해 수익률 0 안전자산 역할 수행.
- `RiskParity` 는 validator 상 허용하되 `generate_weights` 진입 시 `ValueError("risk_parity 는 _CASH_ 를 지원하지 않습니다")` 로 차단 (후속 태스크 분리).
- 모든 해당 전략의 ClassVar `description` 및 관련 필드 description 에 `_CASH_` 의미를 명시.

## 변경된 파일
- projects/stock-backtest/src/stock_backtest/web/pages/backtest.py (수정)
- projects/stock-backtest/src/stock_backtest/strategies/static/fixed_weight.py (수정)
- projects/stock-backtest/src/stock_backtest/strategies/dynamic/momentum.py (수정)
- projects/stock-backtest/src/stock_backtest/strategies/dynamic/dual_momentum.py (수정)
- projects/stock-backtest/src/stock_backtest/strategies/dynamic/vaa.py (수정)
- projects/stock-backtest/src/stock_backtest/strategies/dynamic/risk_parity.py (수정)

## 구현 세부
### UI (backtest.py)
- `_load_asset_options()` 내부에서 DB 로딩 후 `{"label": "현금 대기 · _CASH_ [CASH]", "value": "_CASH_", "search": "현금 대기 cash _CASH_"}` 를 리스트 맨 앞에 prepend. DB 예외 경로(`options = []`)에서도 동일하게 prepend 되어 DB 장애 시에도 `_CASH_` 선택 가능.

### FixedWeight
- 기존 validator 는 심볼 regex 제약이 없고 "non-empty string" 만 요구하므로 `_CASH_` 는 이미 허용됨 (sum=1 검증도 그대로 통과).
- `generate_weights`: prices 컬럼 체크에서 `_CASH_` 는 skip. `_CASH_` 는 반환 DataFrame 컬럼에 포함되지만 엔진(`engine.py`)이 312 라인에서 drop 후 현금 잔고로 해석.
- `weights` Field description 및 ClassVar description 갱신.

### Momentum / DualMomentum / VAA
- 공통 패턴: prices 컬럼 체크에서 `_CASH_` 제외 → prices DataFrame 복사 후 `prices[CASH_SYMBOL] = 1.0` 으로 합성 시계열 주입 → 기존 rank/score 로직 그대로 동작 (모든 수익률/score = 0).
- Momentum: `universe` 에 `_CASH_` 포함 시 수익률 0 자산으로 취급되어 절대 모멘텀 필터(양수 필터)를 탈락. 즉 `_CASH_` 는 랭킹에 나타나도 편입되지 않으나 top_n 계산엔 참여. 의도: 음의 모멘텀만 존재하는 시장에선 모두 탈락 → 현금(미보유) 유지가 자연.
- DualMomentum: `risky_assets` 에 `_CASH_` 포함 시 상대 모멘텀 비교 대상. `safe_asset="_CASH_"` 도 허용되어 절대 모멘텀 탈락 시 100% 현금.
- VAA: `offensive_assets`/`defensive_assets` 에 `_CASH_` 포함 시 momentum score 0. defensive 중 `_CASH_` 가 유일/최고면 방어 모드=전액 현금.

### RiskParity
- `universe` field description 에 "validator 허용/런타임 차단" 명시.
- `generate_weights` 진입 직후 `CASH_SYMBOL in universe` 면 `ValueError` raise.

## Smoke 결과
```
FixedWeight OK: {'SPY': 0.6, '_CASH_': 0.4}
Momentum OK: ['SPY', 'QQQ', '_CASH_']
DualMomentum OK: ['SPY', 'EFA', '_CASH_'] _CASH_
VAA OK: ['SPY', '_CASH_'] ['_CASH_']
RiskParity validator OK: ['SPY', '_CASH_']
RiskParity runtime blocked OK: risk_parity 는 _CASH_ 를 지원하지 않습니다
```
`py_compile` 통과 (backtest.py + 5 전략 파일). `_load_asset_options` 내 `_CASH_` prepend grep 확인.

## 이슈/블로커
없음.

기존 테스트(`tests/`) 에 대한 깨짐 여부는 본 태스크 범위상 직접 실행하지 않았음. `_load_asset_options` 반환 길이/순서에 의존하는 테스트가 있다면 `_CASH_` 1건 추가로 offset 변화 가능 — Tester 단계에서 확인 필요.

## 다음 제안
- Tester 에게 아래 확인 요청:
  1. `_load_asset_options` 가 `_CASH_` 를 맨 앞에 포함하는지 단위 테스트.
  2. 각 전략 generate_weights 가 `_CASH_` 포함 universe 에서 정상 동작하는지 (특히 Momentum 의 rank 경로, VAA 방어 모드).
  3. RiskParity `_CASH_` 런타임 차단 테스트.
- RiskParity 의 `_CASH_` 지원(0 분산 자산 처리)은 후속 태스크로 분리해 별도 설계 검토.
