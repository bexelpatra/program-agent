---
agent: coder
task_id: TASK-051+TASK-052
status: DONE
timestamp: 2026-04-29T09:15:00
---

## 결과 요약
allocators 패키지에 AllWeather (TASK-051) 와 EqualWeight (TASK-052) 두 allocator 를 구현. AllocatorBase 를 상속하고 normalize_weights 를 재사용. TASK-050 의 base/FixedWeight re-export 는 보존하면서 `__init__.py` 에 새 심볼을 append.

## 변경된 파일
- projects/stock-backtest/backend/app/domain/allocators/all_weather.py (신규)
- projects/stock-backtest/backend/app/domain/allocators/equal_weight.py (신규)
- projects/stock-backtest/backend/app/domain/allocators/__init__.py (수정 — append-only, 기존 FixedWeight/AllocatorBase/normalize_weights export 보존)

## 신규 public API
- `AllWeather(AllocatorBase[AllWeatherParams])` — `name="all_weather"`, `required_universe()` override (asset_categories 의 모든 asset_id 반환), `generate_weights()` 가 카테고리 비중을 카테고리 내 universe 자산에 1/N 분배
- `AllWeatherParams(BaseModel)` — `category_weights: dict[Category, float]` (디폴트=DEFAULT_ALLWEATHER_WEIGHTS), `asset_categories: dict[int, Category]` (필수). validation: 합 ≈ 1.0±5%, 음수 금지, asset_categories 비어있으면 거부
- `Category = Literal["equity", "long_bond", "intermediate_bond", "gold", "commodity"]`
- `AllWeatherCategoryMissing(Exception)` — 비중 > 0 인 카테고리에 universe 자산이 0개일 때 raise
- `DEFAULT_ALLWEATHER_WEIGHTS: dict[Category, float]` — equity 0.30 / long_bond 0.40 / intermediate_bond 0.15 / gold 0.075 / commodity 0.075
- `EqualWeight(AllocatorBase[EqualWeightParams])` — `name="equal_weight"`, `required_universe()` 디폴트(빈 리스트), `generate_weights()` 가 1/N 분배 (빈 universe → `{}`)
- `EqualWeightParams(BaseModel)` — 파라미터 없음 (UI 가 빈 폼 자동 표시)

## DoD 검증 결과
1. **Import smoke**: `from app.domain.allocators import AllWeather, AllWeatherParams, AllWeatherCategoryMissing, DEFAULT_ALLWEATHER_WEIGHTS, EqualWeight, EqualWeightParams, FixedWeight` → `ok` (FixedWeight 동시 import 로 TASK-050 보존 확인)
2. **AllWeather 동작**:
   - 표준 5자산: `{1: 0.3, 2: 0.4, 3: 0.15, 4: 0.075, 5: 0.075}`, total=1.000
   - commodity 누락 시 `AllWeatherCategoryMissing` raise (메시지 한국어)
   - equity 카테고리 다중 자산 (1, 6): 각 0.15, long_bond=0.40 정상
   - `required_universe()` → `[1,2,3,4,5]`
   - validation: 합=1.2 → ValueError, 음수 → ValueError, 빈 asset_categories → ValueError
3. **EqualWeight 동작**:
   - 4자산: 모두 `Decimal("0.25")`
   - 빈 universe → `{}`
   - 1자산: `{7: Decimal("1")}`
   - `required_universe()` → `[]` (디폴트)
   - `name="equal_weight"`, `params_schema=EqualWeightParams`
4. **JSON Schema 출력**: 양쪽 BaseModel 의 `model_json_schema()` 정상 (UI 폼 생성 가능)

## 이슈/블로커
없음

## 다음 제안
- TASK-061 (allocator REST 카탈로그 API) 가 `name` ClassVar 와 `params_schema.model_json_schema()` 를 사용해 3종 (FixedWeight/AllWeather/EqualWeight) 을 자동 노출할 수 있다. `Category` Literal 도 schema 에 enum 으로 자동 변환되어 UI 의 카테고리 드롭다운 선택지 소스가 된다.
- AllWeather 의 `category_weights` 디폴트는 mutable dict 로 직접 노출하지 않고 `default_factory=lambda: dict(DEFAULT_ALLWEATHER_WEIGHTS)` 를 통해 인스턴스마다 복사. 디폴트 변조 risk 없음.
- 단위 테스트 (Tester 태스크): 골든 케이스(표준 5자산 0.3/0.4/0.15/0.075/0.075), 카테고리 다중 자산 분배, missing 예외, 빈 universe (EqualWeight), validation edge cases 를 권장.
- `category_weights` 검증을 ±1% 로 좁힐지 (FixedWeight 처럼 ±5% 유지 vs 카테고리 비중은 더 엄격) 는 architecture 레벨 결정 — 현재는 FixedWeight 와 동일하게 ±5%.
