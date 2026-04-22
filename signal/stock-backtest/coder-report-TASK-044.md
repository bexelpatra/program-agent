---
agent: coder
task_id: TASK-044
status: DONE
timestamp: 2026-04-14T00:00:00
---

## 결과 요약
`MultiMovingAverageCrossover` 전략 신규 구현 및 `@register` 등록. 여러 이동평균선의 정배열(+옵션으로 가격 포함) 판정을 통해 risky/safe 스위칭. `backtest.py::_coerce_field_value` 의 list 코어션이 `list[int]` / `list[float]` 원소 타입을 인식하도록 개선.

## 변경된 파일
- projects/stock-backtest/src/stock_backtest/strategies/dynamic/moving_average/multi_crossover.py (신규)
- projects/stock-backtest/src/stock_backtest/web/pages/backtest.py (수정: `_coerce_field_value` list 분기에서 `_args(annotation)` 으로 원소 타입(int/float) 캐스팅)

## 구현 세부
- `MultiMovingAverageCrossoverParams`:
  - `risky_symbol`, `safe_symbol` (`widget=asset_symbol`)
  - `windows: list[int]` — 최소 2개, 양의 정수, 중복 없음; `model_validator(mode="after")` 에서 `sorted(set(...))` 로 오름차순 정렬(중복 존재 시에도 `len` 비교로 거부).
  - `include_price: bool = True`
  - risky != safe 검증
- `MultiMovingAverageCrossover(Strategy)`:
  - `rolling_mean` 기반 다중 MA 계산
  - `include_price=True` 시 가격 + MA 리스트, False 시 MA 리스트만으로 시리즈 구성
  - 벡터화: `pd.concat(..., axis=1).values` 의 `[:, :-1] > [:, 1:]` 를 `all(axis=1)` 로 정배열 판정 (NaN 워밍업 자동 0 처리)
  - look-ahead 방지: `.shift(1).fillna(0).astype(int)`
  - rebalance_dates 별로 `get_indexer([date], method="pad")` 로 최근 신호 참조, 신호=1 → risky 100%, 아니면 safe 100%.

## Smoke 검증
- params 정렬: `windows=[200,50,20,100]` 입력 → `p.windows == [20, 50, 100, 200]` 확인.
- 합성 시계열 100일 랜덤워크로 `generate_weights` 호출 → 예외 없이 각 행 합=1.0, risky/safe 전환 관찰.

## 이슈/블로커
없음

## 다음 제안
- 테스터가 다중 MA 정배열/붕괴 케이스, `include_price` on/off, `windows` 검증(중복/음수/단일/비정수)에 대한 단위 테스트를 작성할 것.
- 웹 폼에서 `list[int]` 필드가 실제로 `[20,50,100,200]` 문자열 입력으로 정상 파싱되는지 통합 확인.
