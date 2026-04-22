# Coder Report — TASK-038

- Task ID: TASK-038
- Title: `_build_rebalance_trades`의 하드코딩 쿠션을 동적 쿠션으로 교체
- Status: **DONE**
- Date: 2026-04-14

## 요약

`engine.py::_build_rebalance_trades`의 `equity * Decimal("0.995")` (50bps 고정
쿠션)을 **config 비용 + 유니버스 통화 구성**에 따라 계산되는 동적 쿠션으로 교체.
`fx_spread_bps > 50`에서 `InsufficientFundsError`가 발생하던 버그가 해소됨
(tester-report-TASK-019 이슈 #2).

## 변경 라인

### `projects/stock-backtest/src/stock_backtest/backtest/engine.py`

1. **Import / 모듈 상수 (line ~37–55)**
   - `import logging` 추가, 모듈 `logger` 생성.
   - 모듈 상수:
     - `_SAFETY_BUFFER_BPS = Decimal("10")` — 하드코딩 10bps 안전 여유분.
     - `_MAX_CUSHION_BPS = Decimal("500")` — 쿠션 상한 5%.

2. **`BacktestEngine._compute_cushion_bps` 신규 (≈line 425)**
   - 시그니처:
     ```python
     def _compute_cushion_bps(
         self,
         universe_currencies: Iterable[str],
         base_currency: str,
         markets: Iterable[str],
     ) -> Decimal
     ```
   - 동작:
     - `markets` 각각에 대해 `self._resolve_costs(market)` 호출
       (`get_costs(settings, market)` 경유 → market_overrides 반영).
     - 각 bucket별로 **가장 큰(보수적) 값** 선택:
       `max_commission_buy_bps`, `max_slippage_bps`, `max_fx_spread_bps`.
     - `fx_component = max_fx_spread_bps if any(ccy != base) else 0`.
     - 합산에 `_SAFETY_BUFFER_BPS(10)` 추가.
     - 합이 `_MAX_CUSHION_BPS(500)`을 초과하면 `logger.warning` 후 500으로 clamp.

3. **`_build_rebalance_trades` 호출부 수정 (line ~560)**
   - 고정 `0.995` 제거.
   - `universe_currencies`, `markets` 추출 → `self._compute_cushion_bps(...)` 호출.
   - `cushion_factor = 1 - cushion_bps / 10000` → `equity *= cushion_factor`.

### `projects/stock-backtest/tests/test_engine_cushion.py` (신규)

5개 테스트:

| # | 함수 | 검증 |
|---|------|------|
| 1 | `test_large_fx_spread_does_not_raise_insufficient_funds` | `fx_spread_bps=100` 시나리오에서 예전에는 `InsufficientFundsError` → 이제 정상 실행, BUY 1건 기록. |
| 2 | `test_cushion_scales_with_cost_bps` | `fx_spread_bps` 5→100 차이(95bps)가 쿠션 차이에 그대로 반영됨. |
| 3 | `test_cushion_no_fx_spread_when_single_currency` | 단일 통화 유니버스는 fx 쿠션 0 (18bps vs 218bps). |
| 4 | `test_cushion_is_clamped_to_max` | `fx_spread_bps=10_000` 설정에도 500bps로 clamp + 경고 로그. |
| 5 | `test_cushion_uses_most_conservative_market_override` | KR 오버라이드(`commission_buy_bps=30`, `slippage_bps=8`)가 US 기본값보다 커서 max가 KR에서 뽑혀 68bps. |

## 쿠션 공식

```
cushion_bps = max_commission_buy_bps(markets)
            + max_slippage_bps(markets)
            + (max_fx_spread_bps(markets) if any(ccy != base_ccy) else 0)
            + _SAFETY_BUFFER_BPS(=10)

if cushion_bps > _MAX_CUSHION_BPS(=500):
    logger.warning(...)
    cushion_bps = 500

equity_investable = equity * (1 - cushion_bps / 10000)
```

- `max_*` 는 유니버스가 커버하는 **모든 market**에 대한 `get_costs(settings, market)`
  결과 중 가장 큰 값. 혼합 유니버스(KR+US 등)에서 보수적 쿠션을 보장.
- fx 성분은 base 통화와 다른 자산이 하나라도 있을 때만 반영.
- 10bps 안전 여유분은 mid-rate target_qty 계산과 실제 체결 사이의 rounding,
  intra-day drift 보호용.
- 5% 상한은 config 오류(예: `fx_spread_bps: 10000`) 시 포트폴리오가 투자 불가
  상태에 빠지지 않도록 방어.

## 검증 결과

```
$ pytest tests/test_engine_cushion.py tests/test_engine_regression.py tests/test_engine_smoke.py -v
16 passed

$ pytest tests/
125 passed, 2 warnings in 0.96s
```

- 신규 `test_engine_cushion.py`: 5/5 통과.
- `test_engine_regression.py`: 9/9 통과 (회귀 없음).
- 전체 스위트: 125/125 통과.

## 완료 조건 체크

- [x] `engine.py` 내 하드코딩 0.995 제거 및 동적 쿠션 적용.
- [x] `_compute_cushion_bps` helper 추가 (max cost 기반).
- [x] market_overrides 반영 (`get_costs` 재사용).
- [x] base 통화와 동일한 유니버스는 fx 쿠션 제외.
- [x] 상한 500bps + 경고 로그.
- [x] `test_engine_cushion.py` 신규 작성 (5 테스트).
- [x] `test_engine_regression.py` 전부 통과 (9/9).
- [x] 전체 테스트 통과 (125/125).
- [x] 금지 파일 미수정: `portfolio.py`, `fx.py`, `strategies/`, `data/repository.py`, `web/` 모두 읽기만 함.
- [x] coder-report-TASK-038.md 작성.

## 특이사항

- `_ensure_cash`의 "spread가 커질수록 equity가 늘어나는" 역방향 이슈
  (tester-report-TASK-019 이슈 #1)는 TASK-037 담당 (`portfolio.py`/`fx.py`)이라
  본 태스크 범위 밖. 본 변경은 그 버그를 건드리지 않는다. 쿠션 증가는 단순히
  "현금을 더 남긴다" 효과만 주므로, 두 수정이 합쳐지면 cross-currency 리밸런싱이
  물리적으로 타당한 방향(wider spread → lower equity)으로 동작하게 된다.
- `fx.py`에는 이미 `convert_for_target`이 존재(라인 165–202)하며 TASK-037에서
  `_ensure_cash`가 이를 사용하도록 교체될 것으로 보인다. 본 태스크는 이와
  무관하게 쿠션만 동적화했다.
