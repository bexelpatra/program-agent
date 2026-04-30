---
task_ids: TASK-230, TASK-231, TASK-232, TASK-233, TASK-234, TASK-236, TASK-237, TASK-238
verdict: NEEDS_REVISION
---

# Reviewer Report: Phase 1 Refactor (8 tasks)

검증 일자: 2026-04-30
검증 방식: 각 라인 / 심볼 / 파일 경로를 grep / Read 로 직접 확인.

## 검증 결과 요약 표

| Task | 라인/심볼 정확성 | 분해 합리성 | 의존성/충돌 | 판정 |
|------|---------------|-----------|------------|------|
| TASK-230 | PASS | PASS | PASS | PASS |
| TASK-231 | PARTIAL — all_weather 4단계 아님 | PASS | PASS | NEEDS_REVISION (minor) |
| TASK-232 | PASS | PASS | PASS | PASS |
| TASK-233 | PASS — 단 의미 차이 주의 | PASS | PASS | NEEDS_REVISION (clarify) |
| TASK-234 | FAIL — asset_repository 경로 오기재 | PASS | PASS | NEEDS_REVISION |
| TASK-236 | PASS | PASS | PASS | PASS |
| TASK-237 | PASS | PASS | **PARTIAL — 238 과 import 블록 충돌 가능** | NEEDS_REVISION (parallel) |
| TASK-238 | FAIL — UniverseSelector 트릭 대상 다름, `as` 캐스트 위치 오류 | PASS | **PARTIAL — 237 과 import 블록 충돌 가능** | NEEDS_REVISION |

## 태스크별 상세

### TASK-230 — source 어댑터 헬퍼 추출

**검증 결과: PASS**

- `backend/app/data/sources/yfinance_source.py` L31-68 — `_RATE_LIMIT_SLEEP_SEC=0.5`, `_rate_lock`, `_last_call_monotonic`, `_rate_limit()`, `_is_nan()`, `_safe_float()`, `_is_invalid_close()` 7개 심볼 모두 실제 위치와 일치.
- `backend/app/data/sources/pykrx_source.py` L31-74 — 동일 7개 심볼 + `_to_kst()` 추가. `_RATE_LIMIT_SLEEP_SEC=0.1` 만 다름 (Manager 가 RateLimiter 인스턴스 인자로 주입 권장 — 합리적).
- 미세 차이: pykrx `_safe_float` 은 `try/except (TypeError, ValueError)` 추가 (L60-64). yfinance 버전은 try-except 없음 (L54-58). 헬퍼 통합 시 안전한 쪽 (try-except 포함) 채택 권장.
- 클린 아키텍처: `_helpers.py` 가 같은 `app/data/sources/` 패키지 내부 → 외부 의존 없이 어댑터 둘만 공유 → 적절.

### TASK-231 — allocator weight dict 검증 통합

**검증 결과: NEEDS_REVISION (minor)**

- `fixed_weight.py` L38-52 — 4단계 검증 (empty / non-negative / total>0 / abs(total-1.0)≤0.05) 일치.
- `ma_signal.py` L53-67 — 4단계 일치.
- **불일치**: `all_weather.py` L60-72 의 `_validate_weights` 는 **3단계** (non-negative / total>0 / total≈1) 만 수행. **empty 검사가 없음** (`category_weights` 가 `Field(default=...)` 라 빈 dict 가 들어오기 어렵기 때문). 별도 `_validate_categories` (L74-79) 가 `asset_categories` 의 empty 만 검사.
- 따라서 Manager 의 "3 allocator 의 4단계 검증 동일" 표현은 부정확. 2 allocator (fixed_weight, ma_signal) 가 4단계 + all_weather 가 3단계.
- **수정 요청**: 태스크 description 을 "fixed_weight / ma_signal 4단계 + all_weather 3단계 (empty 검사 제외)" 로 명확화. 통합 시 `validate_weight_dict(v, *, name, total_tolerance=0.05, allow_empty=False)` 로 empty 검사 옵션화. all_weather 가 호출할 때 `allow_empty=True`.

### TASK-232 — `_persist_results` 분해

**검증 결과: PASS**

- `backend/app/services/backtest_runner.py` L202-286 (85줄, 정확히 일치) `_persist_results` 함수.
- 3 책임 명확: ① equity_rows + drawdown 계산 (L214-227), ② trade_dicts 변환 (L233-257), ③ metrics 계산 + flatten + status (L259-286).
- `backend/tests/services/` 디렉토리 **부재** 확인 (`tests/` 하위는 `api/`, `data/`, `domain/`, `e2e/`, `golden/`, `regression/` 만). Manager 의 "단위 테스트 부재" 주장 정확.
- 분해 함수 시그니처 합리적. `_compute_and_flatten_metrics` 가 `compute_metrics` 호출 + flatten 까지 수행 — 단일 책임 유지.

### TASK-233 — calendar_guard 사적 심볼 import 정리

**검증 결과: NEEDS_REVISION (semantics clarify)**

- `pipeline.py:29` `from app.domain.asset.calendar_guard import _MARKET_CALENDARS` ✓
- `pipeline.py:67` `cal_name = _MARKET_CALENDARS.get(market)` ✓
- `calendar_guard.py:24` `_MARKET_CALENDARS` 정의 ✓, L31-34 `_resolve_calendar_name` 이미 존재 (단 raise ValueError on unknown market).
- **의미 차이 위험**: pipeline.py L67 은 `.get(market)` → unknown market 일 때 None 반환 (graceful). 그러나 `_resolve_calendar_name` (L31-34) 은 unknown 일 때 `ValueError` raise. 신규 public 함수가 어느 쪽 동작이어야 하는지 태스크에 명시 필요.
- **수정 요청**: TASK-233 description 에 "신규 `get_calendar_name(market) -> str | None` 은 unknown market 일 때 None 반환 (raise 금지). 기존 `_resolve_calendar_name` 의 raise 동작을 그대로 public 승격하면 pipeline.py L60-69 의 graceful fallback (빈 리스트 반환) 회귀 발생" 명시.

### TASK-234 — 페이지네이션 total 정확화

**검증 결과: NEEDS_REVISION (path error)**

- `backend/app/api/assets.py:144` `total=len(items)` ✓
- `backend/app/api/backtests.py:287` `total=len(runs)` ✓
- **경로 오기재**: Manager 가 "`backend/app/data/repositories/asset_repository.py`" 라고 적었으나 실제 파일 위치는 `backend/app/data/asset_repository.py` (`repositories/` 하위 아님). `grep` 으로 import 경로 확인:
  - `dependencies.py:15`, `data/__init__.py:6`, `data/pipeline.py:25` 모두 `from app.data.asset_repository` 사용.
  - `backend/app/data/repositories/` 디렉토리에는 `backtest_repository.py`, `ingestion_log_repository.py`, `ohlcv_repository.py` 만 존재.
- **수정 요청**: TASK-234 description 의 "`asset_repository.py`" 경로를 `backend/app/data/asset_repository.py` 로 정정. `backtest_repository.py` 는 그대로 (`backend/app/data/repositories/backtest_repository.py`).
- 부수 확인: 두 파일에 `count(...)` 메서드 부재 확인 필요 (Coder 가 `Read` 후 추가). 신규 `tests/api/test_pagination.py` 위치 합리적 (`tests/api/` 디렉토리 이미 존재).

### TASK-236 — registration enqueue silent swallow 제거

**검증 결과: PASS**

- `backend/app/domain/asset/registration.py` L162-166 — `try: enqueuer.enqueue(...) except Exception: enqueued = False` (Manager 의 L165 ≈ 정확, except 키워드가 정확히 L165).
- `import logging` 부재 확인 (grep 결과 0 hit) → Manager 의 "logger 추가" 주장 정확.
- `tests/domain/test_registration.py` 부재 확인 (`tests/domain/` 디렉토리 존재하지만 해당 파일 없음).
- `BaseException` 분리 권장 (KeyboardInterrupt/SystemExit 의 의도하지 않은 swallow 방지) — 합리적.

### TASK-237 — BacktestResultView 컴포넌트 추출

**검증 결과: NEEDS_REVISION (parallel risk only)**

- `frontend/app/backtests/new/page.tsx:725-794` — 함수 `BacktestResultPanel` 정의 확인 ✓ (props: result/loading/logScale/onToggleLogScale).
- `frontend/app/backtests/[run_id]/page.tsx:218-289` — 인라인 JSX 결과 패널 확인 ✓ (`return (...)` 안의 main / 카드들). L218 = `const monthly = result.metrics?.monthly_returns ?? {};`, L289 = `);` 닫음.
- **차이**: `new/page.tsx` 는 이미 함수로 추출되어 있음. `[run_id]/page.tsx` 는 인라인 JSX. 둘을 단일 `BacktestResultView` 로 통합하면 `new/page.tsx:725-794` 함수는 삭제, `[run_id]/page.tsx` 는 인라인 JSX 를 컴포넌트 호출로 교체.
- props 설계 합리적. logScale state 호출자 보유 — 이 결정 합리적 (좌측 폼에서 토글하지 않음).
- **충돌 risk**: TASK-238 과 동시에 `new/page.tsx` import 블록 (L37-65 부근) 을 모두 만짐. 상세는 "병렬 실행 충돌 분석" 절 참조.

### TASK-238 — BacktestResult 타입 통합 + Zod schema 정리

**검증 결과: NEEDS_REVISION (multiple line/symbol errors)**

- `new/page.tsx:36` `Awaited<ReturnType<typeof api.getBacktestResult>>` ✓
- `[run_id]/page.tsx:45` 동일 ✓
- **틀린 주장 1 — UniverseSelector**: Manager 가 `UniverseSelector.tsx:27-29` 도 동일 `getBacktestResult` 트릭이라 했으나, 실제 L27-29 는 `Awaited<ReturnType<typeof api.listAssets>>["items"][number]` 로 **`listAssets` 트릭** (다른 API). 공통점은 패턴이지 대상 함수 아님.
  - 따라서 TASK-238 의 "BacktestResult 타입 통합" 만으로는 UniverseSelector 의 트릭을 제거할 수 없음. `Asset` 타입 (또는 `UniverseAsset`) 도 함께 `lib/api/types.ts` 로 export 해야 함.
- **틀린 주장 2 — `as` 캐스트 위치**: Manager 가 `StrategyParamsForm.tsx:32-44` 자체 인터페이스 + L96 `as` 캐스트라 했으나, `StrategyParamsForm.tsx` 에는 `as` 캐스트가 **0건** (`grep " as " StrategyParamsForm.tsx` 결과 빈 결과). 실제 `as Record<string, ...>` 캐스트는 **`new/page.tsx:96`** 에 있음 (`(descriptor.params_schema?.properties ?? {}) as Record<...>`). Manager 가 다른 파일의 라인을 혼동.
- **확인된 사실**: `schemas.ts:35,48,96,128,169,179(주석),184,229` 8회 `z.record(z.any())` (단 L179 는 주석 — 코드 라인은 7회). Manager 의 "8회" 주장 ≈ 정확 (주석 포함).
- `StrategyParamsForm.tsx:32-44` 의 `JsonSchemaProperty` + `JsonSchemaObject` 인터페이스 정의 ✓ 정확.
- **수정 요청**:
  1. UniverseSelector 트릭의 대상이 `listAssets` 임을 description 에 명시. `Asset` 또는 `UniverseAsset` 타입도 `types.ts` 로 export 추가.
  2. "L96 `as` 캐스트" 를 `frontend/app/backtests/new/page.tsx:96` 로 정정 (StrategyParamsForm 아님).
  3. 따라서 TASK-238 작업 범위가 `new/page.tsx` 의 L96 도 만짐 → TASK-237 이 같은 파일을 만지므로 충돌 가능성 증가 (아래 절).

## 병렬 실행 충돌 분석

### TASK-237 ↔ TASK-238: `frontend/app/backtests/new/page.tsx` 충돌

두 태스크가 만지는 영역:
- TASK-237: L51-59 (시각화 컴포넌트 import 8개 — 추출 후 삭제), L725-794 (`BacktestResultPanel` 함수 — 삭제), L725 호출 사이트 1곳 (`<BacktestResultPanel ... />` 를 `<BacktestResultView ... />` 로).
- TASK-238: L25-31 (schemas import — `BacktestResult` 가 `types.ts` 로 이동하면 schemas import 변경), L33-36 (`Awaited<...>` 트릭 + 주석 삭제), L96 (`as` 캐스트 제거).

**라인 자체는 비겹침** (237: 51-59 / 725-794, 238: 25-36 / 96). 그러나:
- 두 태스크 모두 **import 블록 (L21-65) 을 수정**. git 3-way merge 가 동일 해당 영역 hunk 두 개를 받으면 conflict 마킹할 가능성 ≥ 50%.
- TASK-237 이 새 import (`import { BacktestResultView } from "@/components/backtest/BacktestResultView"`) 추가 + 기존 8개 시각화 import 삭제 ≈ 큰 hunk.
- TASK-238 이 `BacktestResult` import 추가 (또는 schemas 에서 types 로 이동) + L33-36 삭제 ≈ 인접 hunk.
- 둘이 같은 import 블록 안에서 가까이 붙은 hunk 를 만들면 git 가 깔끔하게 안 합쳐짐.

### TASK-237 ↔ TASK-238: `frontend/app/backtests/[run_id]/page.tsx` 충돌

- TASK-237: L218-289 (인라인 JSX → 컴포넌트 호출), 시각화 import 삭제.
- TASK-238: L40-45 (`Awaited<...>` 트릭 + 주석 삭제), import 변경.

같은 import 블록 충돌 위험 — 위와 동일 패턴.

### 결론: 병렬 실행 권장하지 않음

- 라인 hunk 가 직접 겹치지는 않으므로 git auto-merge 가 운 좋게 통과할 수도 있으나, **import 블록의 인접 hunk 두 개**가 conflict 될 확률 충분히 높음.
- **권장**: TASK-238 을 먼저 완료 (변경량이 적고 타입 정의 인프라) → TASK-237 이 정리된 타입을 import 해서 props 정의 깨끗하게 작성 → 의미적으로도 자연스러움.
- 또는 TASK-237 / 238 묶어서 단일 Coder 호출로 처리 (두 태스크의 변경이 page.tsx 두 파일에서 함께 발생).
- 그 외 충돌:
  - TASK-230 / 231 / 232 / 233 / 234 / 236 — 백엔드, 서로 다른 모듈. **충돌 없음**.
  - 백엔드 vs 프런트엔드 — 충돌 없음.

## 종합 판정

**NEEDS_REVISION**

대부분 태스크는 본질적으로 합리적이나 다음 5건 수정이 필요:

## 수정 요청 (NEEDS_REVISION 시)

1. **(TASK-231)** description 의 "3 allocator 4단계 검증 동일" 표현을 "fixed_weight / ma_signal 4단계 + all_weather 3단계 (empty 제외, 별도 `_validate_categories` 가 처리)" 로 정정. 통합 시그니처에 `allow_empty: bool = False` 옵션 추가.

2. **(TASK-233)** 신규 public 함수 `get_calendar_name(market) -> str | None` 은 unknown market 일 때 **None 반환** (raise 금지) 임을 명시. 기존 `_resolve_calendar_name` 의 raise 동작을 그대로 public 승격하면 pipeline.py 의 graceful fallback 회귀 발생 — 사용자에게 영향.

3. **(TASK-234)** "`backend/app/data/repositories/asset_repository.py`" 경로를 `backend/app/data/asset_repository.py` 로 정정 (실제 파일 위치). `backtest_repository.py` 는 그대로 `backend/app/data/repositories/backtest_repository.py`.

4. **(TASK-238)** 두 가지 라인/심볼 정정:
   - `UniverseSelector.tsx:27-29` 의 트릭 대상은 `getBacktestResult` 가 아니라 **`listAssets`**. TASK-238 작업 범위에 `Asset` 또는 `UniverseAsset` 타입도 `lib/api/types.ts` 로 export 하는 항목 추가.
   - "L96 `as` 캐스트" 의 위치는 `StrategyParamsForm.tsx:96` 가 아니라 **`frontend/app/backtests/new/page.tsx:96`** (`(descriptor.params_schema?.properties ?? {}) as Record<string, { type?: string }>`). description 정정. StrategyParamsForm.tsx 에는 as 캐스트 0건.

5. **(TASK-237 ↔ TASK-238 병렬)** 병렬 실행 권장 안함. 두 태스크 모두 `new/page.tsx` 와 `[run_id]/page.tsx` 의 import 블록을 만져 git 3-way merge conflict 발생 가능성 높음 (라인 자체는 비겹침이지만 hunk 인접). 권장 순서:
   - 옵션 A: TASK-238 먼저 → 완료 후 TASK-237 (TASK-237 이 정리된 `BacktestResult` 를 그대로 사용).
   - 옵션 B: 두 태스크를 단일 Coder 호출로 합쳐서 처리 (제목/commit 만 둘로 나눠 sequential commit).

위 5건 정정 후 재검증 시 PASS 가능. 그 외 6 태스크 (230, 232, 236) 는 그대로 진행 가능.
