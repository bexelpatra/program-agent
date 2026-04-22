# Coder Report - TASK-021

## 태스크
- Task ID: TASK-021
- Title: 동적 전략: Momentum, Dual Momentum
- Status: DONE

## 결과물

### 구현 파일
- `projects/stock-backtest/src/stock_backtest/strategies/dynamic/momentum.py`
  - `MomentumParams(StrategyParams)`
    - `universe: list[str]`
    - `lookback_days: int = 126` (gt=0)
    - `top_n: int = 3` (gt=0)
    - `weight_scheme: Literal['equal', 'rank'] = 'equal'`
  - `Momentum(Strategy)` name='momentum', `@register`
    - 로직: 각 리밸런스일에 `prices[t]/prices[t-lookback] - 1` 계산 → 상위 top_n → 수익률 양수만 보유
    - equal: 동일 비중
    - rank: [N, N-1, ..., 1] 정규화
    - lookback 데이터 부족 시 해당 행 전부 0
    - `get_indexer([date], method="pad")`로 rebalance date가 가격 인덱스에 없어도 직전 거래일 기준 처리
- `projects/stock-backtest/src/stock_backtest/strategies/dynamic/dual_momentum.py`
  - `DualMomentumParams(StrategyParams)`
    - `risky_assets: list[str]` (min_length=1)
    - `safe_asset: str = "BIL"`
    - `lookback_days: int = 252` (gt=0)
  - `DualMomentum(Strategy)` name='dual_momentum', `@register`
    - 로직: risky 중 lookback 수익률 최대 자산 선택 → 그 수익률이 >0 이면 그 자산 100%, 아니면 safe_asset 100%
    - universe = risky + safe (safe가 risky에 있으면 중복 제거)
    - lookback 데이터 부족 시 해당 행 전부 0

### 테스트 파일
- `projects/stock-backtest/tests/test_momentum.py` (11개 테스트)
  1. Momentum equal: SPY/GLD/TLT 중 SPY, GLD 선택(각 0.5), TLT=0
  2. Momentum all-negative → 전부 0
  3. Momentum rank: [3,2,1]/6 = [0.5, 0.333, 0.167]
  4. Momentum lookback 부족 → 전부 0
  5. DualMomentum 둘 다 양수 → 더 높은 risky 100%
  6. DualMomentum 둘 다 음수 → safe 100%
  7. DualMomentum 혼합 → 양수 risky 선택
  8. DualMomentum lookback 부족 → 전부 0
  9. required_universe에 safe 포함
  10. safe가 risky에 이미 있으면 중복 제거
  11. missing symbol → KeyError

### 테스트 결과
```
tests/test_momentum.py ...........                                       [100%]
============================== 11 passed in 0.28s ==============================
```

전체 테스트 스위트 (리그레션 확인):
```
======================== 85 passed, 2 warnings in 0.72s ========================
```

### 레지스트리 확인
```
discover_strategies() → ['dual_momentum', 'fixed_weight', 'momentum', 'permanent', 'risk_parity', 'vaa']
```

## 참고 / 설계 메모
- 첫 리밸런스일 lookback 부족 시 정책: **미보유(0)**로 통일 (태스크 요구사항).
- Momentum의 수익률 음수 자산 제외는 절대 모멘텀 필터로 작용. 선정 자산 수 < top_n이면 행 비중 합 < 1 (현금 잔량).
- `get_indexer(..., method="pad")`로 rebalance_date가 가격 인덱스의 실제 거래일이 아닌 경우에도 직전 거래일 가격으로 평가한다.
- `strategies/dynamic/__init__.py`는 기존 상태 유지(export 추가 불필요). registry 자동 스캔으로 충분.

## 이슈/블로커
없음.
