---
agent: coder
task_id: TASK-054
status: DONE
timestamp: 2026-04-29T00:00:00
---

## 결과 요약

Momentum 필터를 구현했다. 자산별 lookback 기간 단순 수익률 `(price[D] / price[D-lookback]) - 1` 이 `threshold` 를 초과하면 PASS. 디폴트는 lookback=126일 (~6개월), threshold=0.0 (양수 수익률). TASK-053 의 `SignalFilterBase` 를 상속하여 pydantic params_schema 패턴과 SignalFilter Protocol(`name`, `is_eligible`) 을 자동 만족한다. `__init__.py` 는 append-only 로 갱신해 TASK-053 의 export 를 보존했다.

## 변경된 파일

- `projects/stock-backtest/backend/app/domain/filters/momentum.py` (신규, 65 lines)
- `projects/stock-backtest/backend/app/domain/filters/__init__.py` (수정, append-only — `Momentum`, `MomentumParams` 추가; `SignalFilterBase`/`MovingAverage`/`MovingAverageParams` 보존)

## 신규 public API

`backend/app/domain/filters/momentum.py`:
- `class MomentumParams(BaseModel)`:
  - `lookback: int = Field(126, ge=2, le=2000)` — 수익률 측정 기간 (거래일).
  - `threshold: float = Field(0.0, ge=-1.0, le=10.0)` — 통과 기준 수익률.
- `class Momentum(SignalFilterBase[MomentumParams])`:
  - `name: ClassVar[str] = "momentum"` — 카탈로그/직렬화 식별자.
  - `params_schema: ClassVar[type[BaseModel]] = MomentumParams`.
  - `is_eligible(self, asset_id: int, prices_until_d: pd.DataFrame, signal_date: date) -> bool` — `(last/start) - 1 > threshold` 면 True.

`backend/app/domain/filters/__init__.py` __all__ 추가:
- `Momentum`, `MomentumParams`.

## DoD 검증 결과

| # | 검증 | 결과 |
|---|------|------|
| 1 | import smoke (`Momentum, MomentumParams, MovingAverage, SignalFilterBase`) | `ok` |
| 2 | params 디폴트 `(126, 0.0)`, ge/le 경계 4종 (lookback=1, lookback=2001, threshold=-1.5, threshold=10.5) 모두 ValidationError | PASS |
| 3 | is_eligible 동작 — uptrend True / downtrend False / threshold=0.5 strict / 데이터 부족 False / 자산 미포함 False / start_price=0 False / NaN-leading 처리 / 음수 threshold pass·fail | 9/9 PASS |
| 4 | SignalFilter Protocol 만족 (`hasattr(name, is_eligible)`) | `Momentum protocol satisfied` |

## 클린 코드 점검

- 데이터 부족 시 False (보수적, MovingAverage 와 동일 정책)
- `start_price <= 0` 방어 — 분모 0/음수 회피
- `pd.isna(start_price)` / `pd.isna(last_price)` 가드 — NaN 전파로 인한 잘못된 PASS 방지
- pandas `tail(lookback+1)` 활용 — O(window) 메모리, 전체 시리즈 복사 없음
- 음수 threshold 도 ge=-1.0 까지 허용 — "−50% 보다 덜 빠진 자산 PASS" 같은 보호 시나리오 지원
- 함수 단일 책임: `is_eligible` 한 가지 일만 수행 (자격 평가)
- ClassVar 패턴으로 MovingAverage 와 일관성 유지

## 이슈/블로커

없음.

## 다음 제안

- **테스트 커버리지** (Tester 권장): `tests/domain/filters/test_momentum.py` 에 단위 테스트 추가 — 위 DoD 3 의 9개 케이스를 pytest 로 회귀 방어. 특히 `threshold` 가 정확히 같은 경우(`>` vs `>=` 경계: 100→150, threshold=0.5 → 50%==50% → False) 회귀 케이스를 명시적으로 박아두면 좋다.
- **Filter 카탈로그/팩토리** (후속 태스크): allocator 카탈로그(TASK-051+052)와 같이 filter name → class 매핑 dict 가 필요할 시점이 곧 옴. `filters/__init__.py` 에 `FILTER_REGISTRY = {"moving_average": MovingAverage, "momentum": Momentum}` 형식으로 추가하는 별도 태스크 권장 (이번 태스크 범위 밖이므로 미반영).
- **engine 통합**: `signal_filters[]` 가 AND 로 결합되는 부분(architecture.md V3 § 전략 3요소)은 engine 태스크에서 처리될 것. Momentum 단독 동작은 본 태스크에서 검증 완료.
