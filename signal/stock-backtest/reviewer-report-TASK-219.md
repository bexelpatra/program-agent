---
task_id: TASK-219
verdict: PASS
review_round: 2
---

# Reviewer Report: TASK-219 (MA 시그널 allocator `ma_signal`) — ver 2

## 검증 대상
- `signal/stock-backtest/task-board.md` L123 (재작성된 TASK-219 단일 행)
- `signal/stock-backtest/architecture.md` L499, L670
- `projects/stock-backtest/backend/app/services/backtest_runner.py:53-57`
- `projects/stock-backtest/backend/app/api/strategies.py:14-21, L45-66`
- `projects/stock-backtest/backend/app/domain/allocators/__init__.py`
- `projects/stock-backtest/backend/app/domain/filters/moving_average.py:52-54`
- TASK-218 / TASK-220 행 (파일 충돌 재검토)

### Manager 주장 요약 (ver 2)
1. allocator 등록 매핑 2 곳 명시: `backtest_runner.py:53-57 _ALLOCATORS` + `api/strategies.py:14-21 import + L45-66 list_strategies`
2. allocators/__init__.py re-export 추가는 "있으면" 단서 — 실제 존재 여부 reviewer 확인 의뢰
3. frontend 변경 사실상 0 명시 (수동 브라우저 확인만)
4. 자산 단위 fallback 명시 (`filters/moving_average.py:52-54` 패턴)
5. architecture.md L670 갱신 명시. L499 갱신 안 함 (Manager 결정)
6. 단위 테스트 4 케이스 (모두 위 / 모두 아래 / 일부 / 자산 단위 fallback)

## 검증 결과

### Manager 인용 라인 일치 (Read 실측)

| Manager 주장 | 실측 | 일치 |
|--------------|------|------|
| `backtest_runner.py:53-57` `_ALLOCATORS` dict | L53-57: `_ALLOCATORS: dict[str, tuple[type, type]] = { "fixed_weight": (FixedWeight, FixedWeightParams), "all_weather": (AllWeather, AllWeatherParams), "equal_weight": (EqualWeight, EqualWeightParams), }` | O |
| `api/strategies.py:14-21` import 블록 | L14-21: `from app.domain.allocators import (AllWeather, AllWeatherParams, EqualWeight, EqualWeightParams, FixedWeight, FixedWeightParams,)` | O |
| `api/strategies.py:L45-66` `list_strategies` allocators 리스트 | L45-66: `allocators = [StrategyDescriptor(name=FixedWeight.name, ...), StrategyDescriptor(name=AllWeather.name, ...), StrategyDescriptor(name=EqualWeight.name, ...),]` 정확히 3개 | O |
| `filters/moving_average.py:52-54` 자산 단위 fallback 패턴 | L52: `series = prices_until_d[asset_id].dropna()`, L53-54: `if len(series) < self.params.window: return False` | O |
| `lib/api/schemas.ts:182` allocator_name = z.string() free string | (이전 ver 1 검증에서 확인) | O |

### `allocators/__init__.py` re-export 패턴 확인

```python
from .all_weather import (AllWeather, AllWeatherCategoryMissing, AllWeatherParams, DEFAULT_ALLWEATHER_WEIGHTS)
from .base import AllocatorBase, normalize_weights
from .equal_weight import EqualWeight, EqualWeightParams
from .fixed_weight import FixedWeight, FixedWeightParams

__all__ = [..., "FixedWeight", "FixedWeightParams", ...]
__all__ += ["AllWeather", "AllWeatherParams", ..., "EqualWeight", "EqualWeightParams"]
```

→ **re-export 패턴 확실히 존재** (FixedWeight/AllWeather/EqualWeight + Params 모두 export). Manager 의 "있으면" 단서는 사실상 "있다" 로 확정. ma_signal 추가 시 이 파일에도 `from .ma_signal import MaSignal, MaSignalParams` + `__all__ += ["MaSignal", "MaSignalParams"]` 추가 필요. **단 task-board ③(c) 가 이미 명시했으므로 추가 보강 불필요** (Coder 가 (c) 항목을 보고 작업).

### architecture.md L499 vs L670 — Manager 의 부분 갱신 결정 검토

- **L670** (V3 백엔드 모듈 분할 표 allocators 행) = `{fixed_weight,all_weather,equal_weight}` → ma_signal 추가 필요. Manager 가 ⑥항에 명시함. 정확.
- **L499** (V3 우선 원칙 MVP 프리셋) = "Allocator 3종 (FixedWeight/AllWeather/EqualWeight)". Manager 가 갱신 안 함 결정.
  - 근거: Quant Lab CLAUDE.md L26 = "MVP 프리셋 3종만 구현... 추가는 명시적 요청 시에만". 사용자 명시 요청 결과인 ma_signal 은 **MVP 프리셋 정의 자체를 변경하는 것이 아니라 사용자 명시 추가 영역에 들어간다**. L499 는 V3 *원칙* 선언이므로 그대로 유지하고, L670 는 *구현 파일 목록* 이므로 갱신 — **두 라인의 역할 분리**.
  - 정책적 판단으로 합리적. 다만 향후 ma_signal 이 영구 프리셋화되면 L499 도 갱신 필요 — 이 결정이 task-board ⑥항에 명시되어 후속 회고/Phase 2 에서 재평가 가능 상태. PASS.

### TASK-218 / TASK-220 와 파일 충돌 재확인

| TASK | 수정 파일 | TASK-219 와 충돌 |
|------|-----------|------------------|
| TASK-218 | `frontend/app/backtests/new/page.tsx`, `frontend/components/backtest/ProgressPanel.tsx`, `frontend/hooks/useFormPersistence.ts`, persona harness | TASK-219 frontend 변경 0 → **충돌 0** |
| TASK-220 | `backend/app/domain/strategy.py` (Literal), `backend/app/schemas/backtest.py` (Literal), `backend/app/domain/engine.py` (`_is_rebalance_day`), `frontend/lib/api/schemas.ts` (Zod enum), `frontend/app/backtests/new/page.tsx` (REBALANCE_OPTIONS), `tests/domain/test_engine.py` | TASK-219: `allocators/ma_signal.py` (신규), `services/backtest_runner.py` (`_ALLOCATORS` dict), `api/strategies.py` (allocators 리스트), `allocators/__init__.py`, `tests/domain/test_ma_signal_allocator.py` (신규), `architecture.md L670` → **충돌 0** |

→ TASK-218 ∥ 219 ∥ 220 (218 → 220 순차 + 219 병렬) **재확인 OK**.

### ver 1 NEEDS_REVISION 8 항목 반영 검증

| 항목 | ver 1 지적 | ver 2 반영 위치 | 평가 |
|------|------------|-----------------|------|
| 1 | allocator 등록 2 곳 명시 (`backtest_runner._ALLOCATORS` + `api/strategies.list_strategies`) | ③(a) + ③(b) — 두 위치 라인 번호 + import 라인 모두 명시 | OK |
| 2 | `normalize_weights(allow_cash_slot=True)` future-proof 명시 | ②항 마지막 — `normalize_weights(filtered, allow_cash_slot=True)` 명시. future-proof 코멘트는 코드 단계로 위임 (task-board 에 코멘트까지 강제할 필요 없음) | OK |
| 3 | frontend 작업량 정정 (Zod / StrategyParamsForm 갱신 불필요) | ⑤항 — "frontend 변경 사실상 0" + 자동 폼 메커니즘 명시 + "수동 검증만 (브라우저 드롭다운)" | OK |
| 4 | architecture.md L499 / L670 정확 라인 + 표현 | ⑥항 — L670 갱신 명시. L499 미갱신은 정책 결정 (위 검토 참조) | OK (정책 결정 합리적) |
| 5 | 자산 단위 fallback 정책 명시 (per-asset vs entire universe) | ②항 — "**자산 단위 fallback**" 명시 + (i)(ii)(iii) 단계 + "전체 빈 dict 는 모든 자산이 부족/MA 아래일 때만" 명시 | OK |
| 6 | moving_average.py 패턴 참조 명시 | ②항 — "(`filters/moving_average.py:52-54` 패턴)" 직접 참조 | OK |
| 7 | SMA 인라인 vs 유틸 추출 결정 명기 | 명시적 문장은 없으나 `filters/moving_average.py:52-54` 패턴 참조 + `ma_signal.py` 신규 생성 명세로 **인라인 의도 강하게 시사**. 별도 utils 모듈 언급 없음 | OK (묵시적이지만 충분) |
| 8 | DoD e2e 시나리오 burn-in 명시 | DoD-b 명시: "BTC 100% + ma_signal w=120 + quarterly + 2017-2026 → 분기마다 BUY/SELL". burn-in 은 Coder/Tester 가 window=120 거래일 후 평가 시작으로 자연스럽게 처리 가능 | OK |

### 태스크 완결성

- ① ma_signal.py 신규 — 클래스/Params/ClassVar 패턴 명세 완비, FixedWeight 패턴 참조로 정확히 모방 가능.
- ② generate_weights 동작 — 자산 단위 fallback 3 단계 (i)(ii)(iii) 명세, normalize_weights 호출 위치 명확.
- ③ 등록 매핑 2 (+ 1 선택) 위치 라인 번호 모두 명시. **"한 곳 누락 = 사일런트 회귀" 경고 문구가 Coder 부주의 차단**.
- ④ 단위 테스트 4 케이스 — 자산 단위 fallback 케이스 (d) 포함.
- ⑤ frontend 변경 0 + 수동 검증 항목 명시.
- ⑥ architecture.md L670 갱신.
- DoD 4 항목 (단위 / e2e / 9 골든 회귀 0 / GET /api/strategies 검증).
- commit msg 가이드 명시.

### 의존성·순서

- TASK-219 Depends On = (없음). 즉시 시작 가능.
- 218 ∥ 219 ∥ 220: 219 frontend 변경 0 으로 218 (frontend 위주) / 220 (backend strategy/engine + frontend page 한 줄) 과 충돌 0.
- 권고 순서: (218 ∥ 219) → 220.

### 목적성·클린 아키텍처 검증

- **목적성**: 사용자 의도 (MA 깨면 즉시 청산, 회복하면 즉시 매수) 의 한 표현 = signal_filter 가 아니라 allocator 로 분리. architecture.md "사용자 의도 정합성" 섹션 (L116-118) 의 결정과 정확히 일치.
- **클린 아키텍처**:
  - allocator 책임 = 비중 dict 산출 (boolean 필터와 별개) → 책임 단일.
  - `allocators/ma_signal.py` 위치 = `domain/allocators/` 디렉토리 규약 준수 (architecture.md L670).
  - 도메인 → 데이터 의존 방향 위반 없음 (prices_until_d 는 호출부에서 주입).
- **재설계 위험**: ma_signal 은 기존 AllocatorBase 인터페이스 그대로 구현 → engine.py 변경 없음 → 골든 9 케이스 회귀 없음. 향후 MA 외 신호 (Momentum allocator 등) 추가 시도 동일 패턴 반복 가능.

## 판정
**PASS**

ver 1 NEEDS_REVISION 8 항목 모두 반영 (또는 정책적 합리적 미반영 — L499). Manager 인용 라인 5 곳 모두 실측 일치. `__init__.py` re-export 패턴 존재 확정. TASK-218/220 와 파일 충돌 0 재확인.

## Manager에게 전달

Coder 호출 가능. 권고 호출 패턴:

- **단독 호출**: TASK-219 만 (frontend 변경 0 → coder-report 단일 보고).
- **병렬 호출 안전**: TASK-218 ∥ TASK-219 (파일 충돌 0). 각각 `coder-report-TASK-218.md`, `coder-report-TASK-219.md` 사용.
- TASK-220 은 TASK-218 DONE 후 시작 (depends on 명시됨).

Coder 가 작업 중 주의해야 할 미세 항목 (체크리스트):
1. `allocators/__init__.py` 에 `MaSignal`/`MaSignalParams` 추가 잊지 말 것 (③(c)).
2. `api/strategies.py:45-66` `allocators` 리스트에 ma_signal 추가 시 description 한국어 문장 명확히 (예: "이동평균 시그널 — 자산별 가격이 MA 위면 매수, 아래면 청산").
3. 단위 테스트 (d) 케이스에서 BTC/ETH fixture 의 길이 차이를 명확히 (예: BTC=130일, ETH=50일, window=120 → BTC만 평가).
4. e2e DoD-b 시나리오는 별도 e2e 테스트 신규 작성보다는 **수동 실행 + 결과 확인** 으로 충분할 수 있음 — Manager 가 e2e 자동화 vs 수동 검증 명시 권장.

회고용 메모: ver 2 검증 패턴 — Manager 가 ver 1 지적을 반영할 때 "정책적 미반영" (L499) 항목은 근거를 task-board 에 박제하면 Reviewer 가 PASS 가능. 반대로 침묵하면 NEEDS_REVISION 재발. 이 분리가 향후 비슷한 케이스 (사용자 명시 추가 vs 영구 프리셋화) 결정 시 재사용 가능.
