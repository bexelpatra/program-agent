---
agent: coder
task_id: TASK-211
status: DONE
timestamp: 2026-04-30T00:00:00
---

## 결과 요약

`engine.py` 의 `if target_weights:` 분기를 제거하여 빈 dict (filter fail 케이스) 도
`execute_rebalance` 를 호출하도록 변경. 보유 포지션이 `trade._classify_orders` 의
"target_weight_keys 에 없는 보유 자산 전량 매도" 로직으로 자동 청산됨. 이로써 run_id=96
(BTC 100% + MA(117) + quarterly + 2017-01-01~2026-04-29 + USD $100k) 시나리오의
trades 1건만 발생 버그가 해소됨.

추가 invariant 박제:
- engine.py 가 호출 직전 "보유 자산 ⊆ universe" invariant 를 명시 검증 (위반 시 ValueError).
- trade.py `_classify_orders` 가 보유 자산이 `asset_meta` 에 없을 때 명시 KeyError raise
  (silent skip 금지).
- trade.py `_execute_sells` 가 `asset_meta` 누락 시 `MissingPriceError` 변환 (엔진 레이어
  silent 0 정책 일관성).

## 변경된 파일

- backend/app/domain/engine.py (수정)
  - L211-263: `if target_weights:` 분기 제거. 빈 dict 진입 path 도 settlement_d 산출 +
    execute_rebalance 호출하도록 변경.
  - 추가: 보유 자산 ⊆ universe invariant 검증 (held_not_in_universe 위반 시 ValueError).
- backend/app/domain/trade.py (수정)
  - `_classify_orders` 시그니처에 `asset_meta` 파라미터 추가. 보유 자산이 asset_meta 에
    없으면 명시 KeyError raise.
  - `_execute_sells` 의 sells 루프 시작 시점에 `asset_meta` 가드 추가 →
    `MissingPriceError` raise.
  - `execute_rebalance` 의 `_classify_orders` 호출에 `asset_meta` 인자 추가.
- backend/tests/domain/test_engine.py (신규)
  - `TestFilterFailClearsHeldPosition`:
    - `test_empty_weights_triggers_full_liquidation`: 빈 target_weights → 전량 청산 1건.
    - `test_engine_loop_clears_position_when_filter_fails_after_entry`:
      engine.run_backtest 통합 — filter on→off 전이 시 보유 자동 청산.
  - `TestHeldSubsetOfUniverseInvariant`:
    - `test_classify_orders_raises_on_held_not_in_asset_meta`: 보유 ⊄ asset_meta 시
      KeyError raise.
    - `test_execute_rebalance_raises_missing_price_when_held_not_in_meta`:
      execute_rebalance 가 명시 에러 전파 (silent 진행 금지).
    - `test_engine_invariant_check_runs_normally_when_held_subset_of_universe`:
      정상 경로 (보유 ⊆ universe) 청산 통과.
- backend/tests/e2e/test_failure_replay.py (수정 - append)
  - `test_replay_btc_ma_filter_fail_clears_position`: run_id=96 도메인 직접 호출 재현.
    BTC + MA 필터 + 결정적 가격 시계열 (전반 우상향 + 후반 급락) → trades >= 2건 (매수 +
    청산 모두 발생). MA(117) 의미는 동일하게 유지 (filter fail → 청산) 하되 결정적 재현
    위해 window=50 으로 단축.

## Repository / 공개 API 변경

- `app.domain.trade._classify_orders` 의 시그니처 변경 (private 함수, internal only):
  - 이전: `(target_qty, portfolio, target_weight_keys) -> (sells, buys)`
  - 이후: `(target_qty, portfolio, target_weight_keys, asset_meta) -> (sells, buys)`
  - 외부 caller 없음 (`execute_rebalance` 내부에서만 호출). 도메인 단위 테스트 중 본 task
    의 새 테스트 1건이 해당 함수를 직접 호출.

## 테스트 결과

- `pytest tests/domain/ tests/regression/` → 60 passed
- `pytest tests/golden/` → 12 passed (영향 없음 — 기존 9 시나리오 모두 signal_filters 가
  비어 있어 빈 target_weights 케이스 미발생)
- `pytest tests/ --ignore=tests/e2e --ignore=tests/api` → 78 passed
- `pytest tests/e2e/test_failure_replay.py` → 5 passed (신규 1건 포함)

## 골든 baseline 영향

기존 9 골든 스냅샷 시나리오 (`scenario_{1,2,3}_*__{fixed_weight,all_weather,equal_weight}.json`)
는 모두 `signal_filters=tuple()` 이라 빈 target_weights 가 발생하지 않음 → 청산 패턴
변동 없음 → 골든 baseline 갱신 불필요.

TASK-215 (Tester 의 9 케이스 통합 재생성) 는 본 변경의 직접 영향이 아님. 단, 향후
filter 가 들어간 골든 시나리오를 추가할 경우 청산 패턴이 추가되어 baseline 변동 발생할
것 (정상 회귀 동작).

## 이슈/블로커

없음.

## 다음 제안

1. **회귀 의도 commit msg 본문 반영**: "TASK-211: filter fail 시 보유 청산 추가" 와
   함께 "골든 trades 청산 패턴 추가됨 — 단 기존 9 시나리오는 filter 미사용으로 무영향"
   문구를 commit message 에 명시.
2. **Tester 재검증 권장 (TASK-215 와 별개)**: filter 를 사용하는 신규 골든 시나리오 1~2
   건 추가 검토. 본 TASK-211 회귀를 baseline 으로 박제할 수 있음 (예: BTC + MA(50) +
   quarterly).
3. **engine.py 의 broad except 검토**: `except Exception as e:` (L275) 는 NonTradingDayError /
   MissingPriceError / 잔고 부족 / KeyError(_classify_orders 가드) 모두 잡아 silent log
   처리한다. invariant 1차 검증 (held ⊆ universe) 은 try 블록 바깥에서 raise 되므로
   silent 화되지 않지만, trade.py 내부의 KeyError 는 이중 가드 의도와 다르게 silent log
   로 떨어진다. 이중 가드의 의도는 명시적 에러 → 호출자 인지였으므로, except 를
   `(NonTradingDayError, MissingPriceError, InsufficientFundsError)` 로 좁히는 것을
   별도 태스크로 검토 권장.
