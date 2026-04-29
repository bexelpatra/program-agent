---
agent: coder
task_id: TASK-053
status: DONE
timestamp: 2026-04-29T11:00:00
---

## 결과 요약

`backend/app/domain/filters/base.py` 신규 — `SignalFilterBase[P]` (Generic, abstract `is_eligible`). pydantic `params_schema` ClassVar 패턴은 allocators 와 동일.

`backend/app/domain/filters/moving_average.py` 신규 — `MovingAverage` 필터 + `MovingAverageParams` (window 2~2000, price_above bool). 가격이 MA(window) 위/아래 조건을 자산별 독립 평가. 데이터 부족·자산 부재 시 보수적 False.

`backend/app/domain/filters/__init__.py` 수정 (빈 파일 → 3 public symbol re-export). strategy.py 의 `SignalFilter` Protocol (name + is_eligible) 을 구조적으로 만족.

## 변경된 파일

- `projects/stock-backtest/backend/app/domain/filters/base.py` (신규, 56 줄)
- `projects/stock-backtest/backend/app/domain/filters/moving_average.py` (신규, 60 줄)
- `projects/stock-backtest/backend/app/domain/filters/__init__.py` (수정 — 빈 파일에 base/moving_average re-export 추가)

## 신규 public API

| 심볼 | 모듈 | 역할 |
|---|---|---|
| `SignalFilterBase[P]` | `app.domain.filters.base` | 모든 필터의 공통 베이스 (Generic, abstract `is_eligible`). `name`/`params_schema` ClassVar 정의 강제. |
| `MovingAverage` | `app.domain.filters.moving_average` | name="moving_average". `is_eligible` 이 가격 vs MA(window) 비교. |
| `MovingAverageParams` | `app.domain.filters.moving_average` | `window: int (ge=2, le=2000)`, `price_above: bool = True`. UI 폼 자동 생성용 스키마. |

`from app.domain.filters import SignalFilterBase, MovingAverage, MovingAverageParams` 로 일괄 접근.

## DoD 검증 결과

1. **import**: `python -c "from app.domain.filters import SignalFilterBase, MovingAverage, MovingAverageParams; print('ok')"` → `ok` 출력.

2. **params 검증**:
   - `MovingAverageParams(window=200)` → `window=200, price_above=True`
   - `MovingAverageParams(window=1)` → `ValidationError` (ge=2)
   - `MovingAverageParams(window=3000)` → `ValidationError` (le=2000)

3. **is_eligible 동작**:
   - 평탄 가격 (모두 100, window=20) → `False` (price > MA 가 strict `>` 라 같은 값은 탈락)
   - 우상향 (range(100,300), window=20) → `True`
   - 데이터 부족 ([100,101], window=20) → `False`
   - 자산 미포함 (asset_id=99) → `False`
   - 우하향 + price_above=False → `True` (약세장 회피용)

4. **SignalFilter Protocol 만족**: `MovingAverage` 인스턴스가 `name` 속성 + `is_eligible` callable 보유. strategy.py L97-115 의 Protocol 구조 일치.

## 설계 메모

- **보수적 False 정책**: window 만큼 가격 데이터 없거나 NaN/자산 부재 시 모두 False. 잘못된 PASS (= 보유 자격 부여) 가 백테스트 손실로 직결되므로 안전 측 선택.
- **strict `>` 비교**: 가격 == MA 는 False. 평탄 가격 구간에서 시그널 미발생 의도 (변동성 0 자산은 트렌드 정의 불가).
- **MA 계산 범위**: `series.tail(window).mean()` — signal_date 일 종가까지 포함 (모델 A 의 D 종가 시그널, architecture.md V3 L615-630).
- **price_above=False 의 의미**: 가격 < MA 일 때 PASS. 약세장 회피 (cash 비중 증가) 또는 mean reversion 전략 표현 가능.
- **Field constraint** (ge/le) 만으로 검증 — field_validator 불필요 (단순 범위).

## 클린 코드 점검

- ✅ SignalFilterBase 의 `is_eligible` 은 `@abstractmethod` (직접 인스턴스화 시 호출 시점 에러).
- ✅ pydantic Field constraint (ge=2, le=2000) — 도메인 경계 검증 자동.
- ✅ pandas import 만 사용 — SQLAlchemy/HTTP 없음 (도메인 순수).
- ✅ ClassVar 명시 — instance attr 와 구분.
- ✅ Generic[P] — 타입 시스템에서 params 타입 추론.

## 병렬 안전성 확인

이번 태스크가 건드린 파일은 `backend/app/domain/filters/` 디렉토리 3개뿐. TASK-023/045/050 영역 (data, asset, allocators) 과 무교집합. `strategy.py` 는 import 만 (실제로 strategy.py 의 SignalFilter Protocol 자체는 import 하지 않고 구조적으로 만족 — 직접 의존 없음).

## 다음 제안

**TASK-054 (Momentum 필터)** 가 동일 패턴으로 곧장 작업 가능:

- `backend/app/domain/filters/momentum.py` 신규
- `MomentumParams(lookback: int, threshold: float = 0.0)` — `lookback` 일 수익률 > `threshold` 면 PASS
- `is_eligible`: `(series.iloc[-1] / series.iloc[-lookback - 1]) - 1 > threshold` (데이터 부족 시 False)
- `__init__.py` 에 `Momentum`, `MomentumParams` append (TASK-053 와 동일 위치 끝줄에 추가만 하면 충돌 없음)

DoD 도 본 태스크와 대칭 (params 경계, 우상향/우하향, 데이터 부족, 자산 부재, threshold 변형). Coder 호출 1회로 완결 가능.
