---
task_ids: TASK-235, TASK-237
verdict: NEEDS_REVISION
---

# Reviewer Report: Phase 2 Refactor (2 tasks)

## 검증 결과 요약 표

| Task | 라인/심볼 정확성 | Phase 1 충돌 | 분해 합리성 | 판정 |
|------|------------------|--------------|-------------|------|
| TASK-235 | PASS — `assets.py:85-86` 와 `cron_jobs.py:48-52` 모두 실측 일치 | 무 (Phase 1 의 `_helpers.py` 가 어댑터 내부 헬퍼만 변경, 라우팅은 미변경) | PASS | **PASS** |
| TASK-237 | **FAIL — 라인 번호 2건 모두 어긋남** (`new/page.tsx:725-794` 실제 → 717-786, `[run_id]/page.tsx:218-289` 실제 → 215-283 / 시각화 본체 218-282) | 무 (Phase 1 의 `lib/api/types.ts` 가 `BacktestResult` export 함 확인) | 부분 PASS — 테스트 인프라 누락 보강 필요 | **NEEDS_REVISION** |

## 태스크별 상세

### TASK-235 — PASS

**파일/라인 실측**:
- `backend/app/api/assets.py:85-86` — `_RoutingValidator.__init__` 내부에서 `PykrxSource() if market == "KR" else YfinanceSource()` 분기. **일치**.
- `backend/app/scheduler/cron_jobs.py:48-52` — `sources_by_market: dict[str, DataSource] = { "KR": PykrxSource(), "US": YfinanceSource(), "CRYPTO": YfinanceSource() }`. **일치** (L48 시작 — `dict[str, DataSource] = {`, L49-51 KR/US/CRYPTO, L52 `}`).
- `backend/app/data/sources/__init__.py` — 27 줄짜리 re-export 모듈. `get_source_for_market` 추가는 8-16줄 import 블록과 18-28줄 `__all__` 사이에 자연스럽게 들어감. factory 별도 파일 분리는 불필요 (TASK-235 description 의 "또는 factory.py" 문구가 코더에게 선택지를 줘서 추가 협의 가능).

**Phase 1 충돌 점검**:
- TASK-230 이 신규 추가한 `_helpers.py` 는 어댑터 내부 (`yfinance_source.py`, `pykrx_source.py`) 만 수정. `__init__.py` 의 re-export 목록도 그대로 유지된 것을 확인. **충돌 없음**.
- TASK-234 가 수정한 `assets.py` 는 `list_assets` 핸들러 (`L121-148`) 와 `_to_read` 헬퍼만 손댔고, `_RoutingValidator` (L78-96) 는 미변경. **충돌 없음**.

**의존성 정확성**: `Depends On: TASK-230, TASK-234` 모두 task-board 에서 DONE 확인 (L167, L171). 정확.

**시그니처 합리성**: `get_source_for_market(market: str, *, yfinance: YfinanceSource, pykrx: PykrxSource) -> DataSource` — DI 형식이 두 호출처 모두에서 적합:
- `assets.py:78-86` 의 `_RoutingValidator` 는 `__init__` 에서 인스턴스를 그 자리에 만든다. factory 를 호출할 때도 매번 `yfinance=YfinanceSource(), pykrx=PykrxSource()` 를 새로 만들어 주거나, 아니면 lazy 생성을 factory 내부로 옮기는 두 옵션. → **Coder 가 선택할 수 있음** (DI 시그니처는 둘 다 수용).
- `cron_jobs.py:48-59` 는 `sources_by_market` dict 를 한번 만들어 `filtered_sources` 만 추출 후 `backfill_active_assets` 에 넘김 — factory 함수를 dict 자리에서 호출하면 동일 효과. **무리 없음**.

**판정: PASS**.

---

### TASK-237 — NEEDS_REVISION

**파일/라인 실측 — 어긋남 2건**:

#### 1. `frontend/app/backtests/new/page.tsx`
- 파일 총 **786 줄** (Manager 주장 794 줄 → 8줄 차이).
- `BacktestResultPanel` 함수: 실제 위치 **L717-786** (Manager 주장 L725-794 → 8줄 시프트).
  - L712 주석 시작 (`// ─── 인플레이스 결과 패널 ───`)
  - L717 함수 헤드 `function BacktestResultPanel({`
  - L786 닫는 `}`
- 호출부: L696 `<BacktestResultPanel result={result} ...>`.
- import: L31 `import type { BacktestResult, StrategyDescriptor } from "@/lib/api/types";` — TASK-238 의 결과로 이미 적용됨.

#### 2. `frontend/app/backtests/[run_id]/page.tsx`
- 파일 총 **284 줄** (Manager 주장 289 줄 → 5줄 차이).
- 시각화 인라인 JSX 블록: 실제 위치 **L215-283** (`return ( <main ...> ... </main> );` 까지). Manager 주장 L218-289 → 5-7줄 시프트.
  - L215 `return (`
  - L216 `<main className="...">`
  - L218 `<header ...>` ← Manager 가 시작점으로 본 라인은 header 진입
  - L236-281 `EquityChart` / `DrawdownChart` / `MetricsTable` / `MonthlyHeatmap` / `TradesTable` 5 컴포넌트
  - L283 닫는 `}`
- import: L39 `import type { BacktestResult } from "@/lib/api/types";` — TASK-238 의 결과로 이미 적용됨.

→ **라인 번호 모두 8/5줄씩 시프트**. 실측 시점이 Phase 1 commit `bca9131` 직후 — Phase 1 의 TASK-238 변경 (import 라인 정리, `Awaited<ReturnType<typeof ...>>` 트릭 주석 제거) 으로 두 파일 모두 상단 import 영역이 줄어듦. Manager 가 Phase 1 직전 라인 번호를 그대로 쓴 것으로 추정.

**Phase 1 충돌 점검**:
- `lib/api/types.ts` (TASK-238 신규) 에 `BacktestResult` 가 L68 `export type BacktestResult = z.infer<typeof BacktestResultSchema>;` 로 export 되어 있음. **import 경로 정확**.
- `BacktestResultSchema` 는 `lib/api/schemas.ts:335` 에서 정의됨 (`grep` 확인).

**시각화 컴포넌트 소비 패턴 일치성** — 두 페이지 모두 동일한 5 컴포넌트 사용:
- `new/page.tsx:752-782`: EquityChart / DrawdownChart / MetricsTable / MonthlyHeatmap / TradesTable
- `[run_id]/page.tsx:249-279`: EquityChart / DrawdownChart / MetricsTable / MonthlyHeatmap / TradesTable

→ 컴포넌트화 가능성 자체는 명확.

**테스트 인프라 누락**:
- `frontend/components/backtest/__tests__/` 디렉토리 **부재** (`ls` 결과 "no __tests__ dir").
- `find -name "*.test.tsx"` 결과 frontend 내 0건.
- `package.json` 에 vitest + @testing-library/react + jsdom 은 설치돼 있음 → 테스트는 작성 가능.
- `vitest.config.ts` / `vitest.setup.ts` 등 설정 파일 존재 여부는 미확인 (Coder 가 첫 테스트 작성 시 setup 부재면 같이 만들어야 함). **Coder 작업 단위 추가 필요**.

**시그니처 합리성**:
- props `result: BacktestResult, logScale: boolean, onLogScaleChange: (v: boolean) => void, layout?: "compact" | "full"` — Manager description 과 일치.
- 단, `[run_id]/page.tsx:236-255` 가 자본곡선/낙폭을 `md:grid-cols-2` 로 좌우 병치하는 반면 `new/page.tsx:740-758` 는 세로 stack. 이 차이가 `layout?: "compact" | "full"` prop 의 의미. → **layout prop 의 두 모드를 description 에 명시하는 것이 좋음** (compact = 세로 stack / full = 자본곡선·낙폭 grid-cols-2).

**판정: NEEDS_REVISION**.

수정 요청:
1. `new/page.tsx:725-794` → **`new/page.tsx:717-786`** 로 정정.
2. `[run_id]/page.tsx:218-289` → **`[run_id]/page.tsx:215-283`** (또는 시각화 본체만 가리키려면 `L218-282` — L218 의 header 부터 L282 닫는 `</main>`) 로 정정.
3. `layout?: "compact" | "full"` 의 의미를 description 에 명시 (compact: 세로 stack — `new` 페이지 / full: `md:grid-cols-2` 병치 — `[run_id]` 페이지).
4. **테스트 인프라 부재 처리** — DoD 의 "snapshot 1건" 작성 전 `frontend/vitest.config.ts` + `vitest.setup.ts` 존재 여부를 Coder 가 먼저 확인 후, 부재 시 같이 작성. (또는 Manager 가 별도 선행 태스크로 분리). 현 description 은 이 부분이 묵시적 — 명시 권장.

---

## 병렬 실행 충돌 분석

- **TASK-235** = backend Python (`backend/app/data/sources/__init__.py` + `api/assets.py:85-86` + `scheduler/cron_jobs.py:48-52`).
- **TASK-237** = frontend TypeScript (`frontend/components/backtest/BacktestResultView.tsx` 신규 + `frontend/app/backtests/new/page.tsx` + `frontend/app/backtests/[run_id]/page.tsx`).

영역 완전 분리 — git merge 충돌 0. **병렬 실행 OK**.

단, TASK-237 의 라인 번호와 layout prop 명세를 정정하고 Coder 호출 시점에 task-board 의 description 도 동기 갱신할 것 (Coder 가 description 을 그대로 인용해 commit msg/주석에 쓸 수 있어 부정확한 라인이 코드 베이스에 흔적으로 남는 것을 차단).

---

## 종합 판정

**NEEDS_REVISION**

- TASK-235: 그대로 PASS — Coder 호출 가능.
- TASK-237: 라인 번호 2건 정정 + layout prop 의미 명시 + 테스트 인프라 부재 처리 후 재검증.

Manager 가 task-board 의 TASK-237 description 만 수정해 라인 시프트 + layout prop 의미 + (선택) 테스트 인프라 선행 작업을 반영한 뒤, 별도 재검증 없이 바로 Coder 2 병렬 호출해도 무방. (라인 번호 정정은 Coder 가 실측으로 우회할 수 있는 류이지만, description 의 정확성 자체가 Reviewer 통과 기준이므로 정정 후 진행 권장.)
