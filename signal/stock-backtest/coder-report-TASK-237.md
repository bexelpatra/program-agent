---
agent: coder
task_id: TASK-237
status: DONE
timestamp: 2026-04-30T21:38:00
---

## 결과 요약
`/backtests/new` 의 `BacktestResultPanel` 함수 (786줄 파일 중 L717-786) 와
`/backtests/[run_id]` 페이지의 인라인 결과 JSX (284줄 파일 중 L215-283) 가
거의 동일한 5개 시각화 (EquityChart / DrawdownChart / MetricsTable /
MonthlyHeatmap / TradesTable) 블록을 두 번 렌더하던 중복을, 단일 컴포넌트
`frontend/components/backtest/BacktestResultView.tsx` 로 통합했다.

`layout` prop (`"compact" | "full"`) 으로 두 진입 경로의 레이아웃 차이만
분기한다:
- `compact` — `space-y-6` 단일 컬럼 stack (new/page.tsx 우측 패널이
  lg breakpoint sticky 폼과 병치되므로 폭이 좁음)
- `full` — `grid md:grid-cols-2` 로 자본곡선/낙폭 좌우 병치 + 나머지
  (지표/월별/거래) 단일 컬럼 ([run_id] 전용 페이지)

5개 시각화 컴포넌트 직접 import 가 두 페이지에서 모두 제거되어
`BacktestResultView.tsx` 한 곳으로 응집됐다.

## 변경된 파일
- projects/stock-backtest/frontend/components/backtest/BacktestResultView.tsx (신규, 133줄)
- projects/stock-backtest/frontend/components/backtest/__tests__/BacktestResultView.test.tsx (신규, 164줄)
- projects/stock-backtest/frontend/components/backtest/__tests__/__snapshots__/BacktestResultView.test.tsx.snap (신규, vitest 자동 생성)
- projects/stock-backtest/frontend/app/backtests/new/page.tsx (수정: 786→712줄, BacktestResultPanel 함수 삭제 + 5개 시각화 import 제거 + BacktestResultView 호출로 교체)
- projects/stock-backtest/frontend/app/backtests/[run_id]/page.tsx (수정: 284→237줄, 인라인 JSX 영역 삭제 + 5개 시각화 import 제거 + BacktestResultView 호출로 교체)
- projects/stock-backtest/frontend/vitest.config.ts (수정: `esbuild.jsx='automatic'` 추가 — tsconfig 의 jsx='preserve' 가 vitest 에서는 적용되지 않아 .tsx 테스트가 React 미정의 오류를 냈음)

## 신규/변경된 public API
없음. `BacktestResultViewProps` 인터페이스는 신규지만 컴포넌트 1곳에서만
소비된다 (두 페이지). 외부 API 표면 영향 없음.

## DoD 검증

### (1) typecheck + build
```
$ npx tsc --noEmit       # 0 에러 (무출력)
$ npm run build          # ✓ Compiled successfully + Generating static pages (6/6)
$ npm run lint           # ✔ No ESLint warnings or errors
```

### (2) vitest 단위 테스트
```
$ npx vitest run components/backtest/
 ✓ components/backtest/__tests__/BacktestResultView.test.tsx  (4 tests) 63ms
   Snapshots  2 written
 Test Files  1 passed (1)
      Tests  4 passed (4)

$ npx vitest run                # 전체 회귀
 ✓ hooks/__tests__/useFormPersistence.test.ts  (6 tests)
 ✓ components/backtest/__tests__/BacktestResultView.test.tsx  (4 tests)
 Test Files  2 passed (2)
      Tests  10 passed (10)
```

테스트 4건:
- `layout='compact'` 5개 시각화 슬롯 렌더 + grid 미사용 검증 + snapshot
- `layout='full'` md:grid-cols-2 적용 + 5개 시각화 슬롯 렌더 + snapshot
- logScale 토글 버튼 클릭 → onLogScaleChange(true) 콜백 호출
- metrics=null 케이스 — fallback 카드 + monthly heatmap 숨김

snapshot 2건 (compact/full 각 1건) 작성됨.

### (3) 시각화 컴포넌트 5개 import 두 페이지에서 제거
```
$ grep -nE "EquityChart|DrawdownChart|MetricsTable|MonthlyHeatmap|TradesTable" \
    frontend/app/backtests/new/page.tsx frontend/app/backtests/[run_id]/page.tsx
(0 matches)
```

### (4) ESLint 통과
`npm run lint` → No warnings or errors.

## 이슈/블로커

### 처리한 사항 (보고)
1. **vitest jsx runtime** — `.tsx` 테스트 도입 시 첫 실행에서 `ReferenceError: React is not defined` 발생. 원인: 프런트의 `tsconfig.json` 은 `jsx: "preserve"` (Next.js 빌드용) 이라 vitest 의 esbuild 변환에는 React JSX 자동 임포트가 활성화되지 않음. `vitest.config.ts` 에 `esbuild: { jsx: 'automatic' }` 를 추가해 해결. 기존 `.ts` 테스트 (useFormPersistence) 는 영향 없음 (재실행 시 6/6 PASS 확인).
2. **@testing-library/react cleanup** — vitest config 의 `globals: false` 환경에서는 라이브러리의 자동 afterEach cleanup 이 등록되지 않아 다음 테스트로 DOM 누적 → "Found multiple elements by data-testid" 에러. 테스트 파일 상단에 `afterEach(cleanup)` 명시.

### 미해결 블로커
없음.

## 다음 제안
- TASK-239 (`/new/page.tsx` 794줄 분해) 가 후속 태스크. 이번 추출로
  786 → 712 줄로 74줄 줄었으므로, 4 hook + 5 카드 분리 후 목표 280줄
  달성에 부담이 약간 줄어든 셈이다.
- 회귀 0 검증을 e2e 로 보강하려면 `tests/e2e/test_persona_first_use.py`
  (Tester 영역) 가 결과 화면 시각 비교까지 다루는지 확인 필요. 현
  태스크에서는 build PASS + 4건 unit + snapshot 으로 DoD 충족.
