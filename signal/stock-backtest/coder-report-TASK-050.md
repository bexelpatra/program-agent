---
agent: coder
task_id: TASK-050
status: DONE
timestamp: 2026-04-29T11:00:00
---

## 결과 요약

`backend/app/domain/allocators/` 패키지에 Allocator 베이스 + 첫 구현체(FixedWeight) 추가. TASK-043 의 `Allocator` Protocol (strategy.py L44-84) 구조적 준수. pydantic `params_schema` 를 ClassVar 로 보유 → UI 가 JSON Schema 변환해 폼 자동 생성 (V3 § "절대원칙 1 - JSON 노출 금지" 충족). `normalize_weights` 헬퍼는 후속 allocator (AllWeather, EqualWeight) 가 재사용할 수 있도록 base.py 에 분리.

## 변경된 파일

- `projects/stock-backtest/backend/app/domain/allocators/base.py` (신규, 109 줄) — `AllocatorBase[P]` Generic 베이스 + `normalize_weights` 헬퍼
- `projects/stock-backtest/backend/app/domain/allocators/fixed_weight.py` (신규, 84 줄) — `FixedWeightParams` (pydantic) + `FixedWeight` 구현
- `projects/stock-backtest/backend/app/domain/allocators/__init__.py` (수정 — 빈 파일에 4 public symbol re-export append)

## 절대 건드리지 않은 영역 (병렬 안전성)

- `backend/app/domain/strategy.py` — TASK-043 산출물, Allocator Protocol 만 import (수정 0)
- `backend/app/domain/filters/` — TASK-053 영역
- `backend/app/domain/{portfolio,trade,calendar,engine,dividend,metrics}.py` — 다른 태스크 영역
- `backend/app/domain/__init__.py` — 다른 태스크 동시 수정 영역, 이번 라운드는 추가 안 함 (allocators 는 `app.domain.allocators` 로 직접 import)
- `backend/app/domain/asset/`, `backend/app/data/`, `backend/app/api/`

## 신규 public API

### `app.domain.allocators.base`

| Symbol | Kind | 용도 |
|---|---|---|
| `AllocatorBase[P]` | `Generic` ABC-like | 모든 Allocator 의 공통 베이스. ClassVar `name`, `params_schema` + `__init__(params: P)` + `required_universe()` 기본 구현 + `@abstractmethod generate_weights(...)`. P 는 pydantic BaseModel TypeVar. |
| `normalize_weights(weights, allow_cash_slot=True) -> dict[int, Decimal]` | function | 비중 정규화. 합 ≤ 0 → 빈 dict, 합이 1 ± 1bp → 그대로, 그 외 → 합으로 나눔. `allow_cash_slot` 은 future-proof 매개변수 (현재는 호출자가 cash slot 포함해 넘기는 것 허용). |

### `app.domain.allocators.fixed_weight`

| Symbol | Kind | 용도 |
|---|---|---|
| `FixedWeightParams` | `pydantic.BaseModel` | `weights: dict[int, float]`. validator: 빈 dict 금지 / 음수 금지 / 합 1.0 ± 5% 안. |
| `FixedWeight` | `AllocatorBase[FixedWeightParams]` | `name="fixed_weight"`. `required_universe()` 는 params.weights 의 키 전체. `generate_weights` 는 universe ∩ params.weights → `normalize_weights`. 가격 무관 (prices/signal_date 인자 사용 안 함). |

### `app.domain.allocators` (re-export)

`AllocatorBase`, `normalize_weights`, `FixedWeight`, `FixedWeightParams` 4개.

## DoD 결과

| # | 검증 | 결과 |
|---|---|---|
| 1 | `python -c "from app.domain.allocators import AllocatorBase, normalize_weights, FixedWeight, FixedWeightParams; print('ok')"` | `ok` |
| 2-a | `FixedWeightParams(weights={1:0.6,2:0.4})` | 정상 통과, `{1: 0.6, 2: 0.4}` |
| 2-b | `FixedWeightParams(weights={})` | `ValidationError: weights must not be empty` |
| 2-c | `FixedWeightParams(weights={1:1.5})` | `ValidationError` (합 1.5, 5% 초과) |
| 2-d | `FixedWeightParams(weights={1:-0.5,2:1.5})` | `ValidationError` (음수 감지) |
| 3-a | `generate_weights([1,2], prices, d)` | `{1: Decimal("0.6"), 2: Decimal("0.4")}` |
| 3-b | universe 교집합 (`generate_weights([1], prices, d)`) | `{1: Decimal("1")}` (== `Decimal("1.0")`) — universe 에 없는 자산 2 제외 후 정규화 |
| 3-c | `required_universe()` | `[1, 2]` |
| 4 | `FixedWeightParams.model_json_schema()` | OpenAPI 호환 JSON Schema 출력 (title, type=object, properties.weights, required=["weights"]) — 프런트가 그대로 폼 생성 가능 |
| 5 | Allocator Protocol 구조적 만족 (`hasattr name / generate_weights / required_universe`) | True. `inst.name == "fixed_weight"`. (Protocol 이 `@runtime_checkable` 미적용이라 isinstance 체크는 TypeError — 정상, 구조적 typing 으로 충분) |

## 클린 코드 점검

- `AllocatorBase.generate_weights` 가 `@abstractmethod` — 서브클래스 강제
- `params_schema` / `name` 은 `ClassVar` (pydantic 인스턴스 변수 아님 — 클래스 메타정보)
- `field_validator` 로 입력 검증을 pydantic 경계에서 종료 (도메인은 검증된 인스턴스만 받음)
- `normalize_weights` 헬퍼 분리 → AllWeather/EqualWeight 등 후속 allocator 가 import 만 하면 재사용 가능
- `_CASH_` 슬리브 정책 future-proof (`allow_cash_slot` 파라미터 시그니처에 미리 포함)
- 도메인 순수 유지: `pandas` / `pydantic` 만 import (strategy.py L20-21 정책 동일). SQLAlchemy/HTTP/외부 어댑터 전무

## 이슈/블로커

없음.

## 다음 제안

동일 패턴으로 진행 가능한 후속 태스크:

- **TASK-051 AllWeather**: `AllWeatherParams` 는 빈 BaseModel (파라미터 없음, 비중 고정). `name="all_weather"`. `required_universe()` 는 architecture.md 가 정한 5자산 (예: SPY, IEF, TLT, GLD, DBC) 의 asset_id — 단 asset 등록은 사용자가 카탈로그에서 직접 매핑하는 영역이므로, params 에 5개 asset_id 만 받아도 됨 (예: `class AllWeatherParams(BaseModel): stocks_id, intermediate_treasury_id, long_treasury_id, gold_id, commodity_id: int`). 비중은 30/15/40/7.5/7.5 (Ray Dalio 표준).
- **TASK-052 EqualWeight**: `EqualWeightParams` 도 빈 BaseModel. `required_universe()` 는 빈 리스트 (universe 자유). `generate_weights` 는 universe 의 N 개 asset 에 1/N 균등 분배 (`Decimal(1) / Decimal(N)`).
- **TASK-053/054 (Filter)** 는 별도 패키지 (`domain/filters/`) 로 동일 패턴 (FilterBase + pydantic params + `is_eligible`).
- 후속 태스크 모두 base.py 의 `AllocatorBase`, `normalize_weights` 를 재사용 → 일관성 보장.
- engine 통합 테스트 (TASK-080 부근) 시점에 `apply_filters_and_allocator(strategy, universe, prices_until_d, signal_date)` (strategy.py L135) 가 FixedWeight 인스턴스를 받아 정상 동작하는지 골든 테스트 필요 (Quant Lab CLAUDE.md "테스트 규칙").
