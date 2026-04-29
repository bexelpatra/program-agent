---
agent: coder
task_id: TASK-093
status: DONE
timestamp: 2026-04-29T09:50:00
---

## 결과 요약

`/backtests/[run_id]` 백테스트 결과 화면을 구현했다. 사용자가 결과 페이지에
진입하면 먼저 GET `/api/backtests/{run_id}` 로 status 를 조회하고, `done` 일
때만 GET `/api/backtests/{run_id}/result` 를 호출해 자본 곡선 / 낙폭 / 지표
테이블 / 연·월 히트맵 / 거래 내역 테이블을 카드 단위로 노출한다 (architecture
.md V3 § "UI/UX 원칙 4" L685-688). `pending`·`running`·`cancelled` 상태는
"실행 중" 안내 카드만, `failed` 는 toast(destructive) 로 원인 메시지 +
trace_id 8자리 prefix(원칙 2). NaN/0 ID 같은 잘못된 라우트 파라미터는 "잘못된
백테스트 ID 입니다" 카드로 fail-safe.

지표 6종은 Quant Lab CLAUDE.md §4 (CAGR/MDD/Sharpe/Sortino/Calmar/승률)
전부 표기. 거래 내역 테이블은 통화 그룹 필터 + 20건 페이지네이션 (실거래
백테스트 한 건이 수백 row 단위라 클라이언트 슬라이스로 처리). 자본 곡선은
선형 ↔ 로그 토글 (장기 backtest 의 복리 왜곡 완화).

## 변경된 파일

- `projects/stock-backtest/frontend/lib/api/schemas.ts` (수정 — append-only)
  - 추가: `EquityPointSchema`, `TradeRecordSchema`, `MetricsPayloadSchema`,
    `BacktestResultSchema` 및 동명 type. 백엔드 `app/schemas/backtest.py`
    (TASK-062) 의 BacktestResult 와 일대일.
- `projects/stock-backtest/frontend/lib/api/client.ts` (수정 — append-only)
  - 추가: `api.getBacktestResult(runId) → BacktestResult`. 호출 게이트는
    UI 가 책임 (status==='done' 일 때만).
  - import 에 `BacktestResultSchema` 추가.
  - **참고**: 동시에 TASK-094 도 client.ts 를 append-only 수정해
    `cancelBacktest` 를 추가했음. 두 변경은 서로 다른 줄에 위치해 충돌 없이
    공존 (line 162-167 = getBacktestResult, line 169-219 = cancelBacktest).
- `projects/stock-backtest/frontend/app/backtests/[run_id]/page.tsx` (신규, 290 라인)
  - 클라이언트 컴포넌트, `useParams` → `runId`, `useEffect` 로 status →
    result 2-단계 fetch + cleanup 가드, 카드 5종 + status badge.
- `projects/stock-backtest/frontend/components/backtest/EquityChart.tsx` (신규, 65 라인)
- `projects/stock-backtest/frontend/components/backtest/DrawdownChart.tsx` (신규, 69 라인)
- `projects/stock-backtest/frontend/components/backtest/MetricsTable.tsx` (신규, 74 라인)
- `projects/stock-backtest/frontend/components/backtest/MonthlyHeatmap.tsx` (신규, 79 라인)
- `projects/stock-backtest/frontend/components/backtest/TradesTable.tsx` (신규, 152 라인)

라인 수: 합계 신규 729 + schemas +73 + client +7. 모든 파일 단일 파일 300
라인 기준 통과 (page.tsx 290 가 최대).

## 추가 / 변경된 public API (client.ts)

- `api.getBacktestResult(runId: number) => Promise<BacktestResult>`
  (`BacktestResult = z.infer<typeof BacktestResultSchema>`,
  shape = `{ run, equity_curve[], trades[], metrics? }`)

## DoD 검증 결과

1. **tsc + build**:
   - `npx tsc --noEmit` exit 0 (출력 없음)
   - `npm run build` ✓ Compiled successfully · `/backtests/[run_id]` 라우트
     ƒ Dynamic, 106 kB / First Load 220 kB (recharts 포함 → 큼; 추후 lazy
     load 가능 — "다음 제안" 참조)
2. **라우트 등록**: build 출력에 `├ ƒ /backtests/[run_id]   106 kB   220 kB`
   확인.
3. **dev + curl** (PORT=3099, 백엔드 미가동 상태):
   - `GET /backtests/1` → HTTP 200, body 에 "로딩 중" 한국어 키워드 포함
     (서버 SSR 시점에는 백엔드 fetch 가 client-side, 따라서 초기 페인트는
     loading 스켈레톤만 출력 — 정상 동작)
   - `GET /backtests/abc` → HTTP 200, "잘못된 백테스트 ID 입니다" (NaN 가드)
   - `GET /backtests/0` → HTTP 200, "잘못된 백테스트 ID 입니다" (zero 가드)
4. **UI/UX 원칙 4 적용**:
   - ✅ 자본 곡선 (EquityChart, recharts LineChart, 선형/로그 토글)
   - ✅ 낙폭 차트 (DrawdownChart, AreaChart, 빨강 그라디언트)
   - ✅ 지표 테이블 (MetricsTable, 6 metric × ko.metric.* 라벨)
   - ✅ 연·월 수익률 히트맵 (MonthlyHeatmap, 연 × 12개월 격자, 절대값
     강도 × 부호 색)
   - ✅ 거래 내역 테이블 (TradesTable, 통화 필터 + 20건 페이지네이션 +
     BUY/SELL Badge)
   - ✅ trace_id 8자리 prefix toast (UI/UX 원칙 2)

## 이슈 / 블로커

없음. 다만 구현 중 한 가지 TS 타입 마찰을 정리해 둠 (재발 가능성):

- `fetchAndValidate<T>(path, schema: z.ZodSchema<T>)` 에서 `T` 가
  schema 의 input 타입으로 추론되는 케이스가 있다 (z 의 default 가 들어간
  `MetricsPayloadSchema` 를 `BacktestResultSchema` 안에 nullable.optional
  으로 끼웠을 때 발생). 결과적으로 `result.metrics.annual_returns` 가
  output 에선 `Record<string, number>` 인데 호출 측에선 optional 로 보였다.
  → 우회: `MetricsTable` props 를 의도적으로 loose 하게 정의 (`annual_
  returns?` ) 하고, `BacktestResult` 를 `Awaited<ReturnType<typeof api.
  getBacktestResult>>` 로 anchor. 런타임은 Zod 가 default 를 채워 항상
  존재하므로 안전. `client.ts` 의 `fetchAndValidate` 시그니처를 `<T extends
  z.ZodTypeAny>(schema: T): Promise<z.output<T>>` 로 바꾸는 PR 이 더 깔끔
  (다음 제안 1).

## 다음 제안

1. **fetchAndValidate generic 정정** — 위 이슈처럼 default/optional 이 섞인
   Zod schema 에서 호출 측 타입이 헐거워진다. signature 를 `<T extends z.
   ZodTypeAny>(path: string, schema: T): Promise<z.output<T>>` 로 바꾸면
   `MetricsTable` 의 loose props 를 strict (`MetricsPayload`) 로 되돌릴 수
   있음. client.ts 한 줄 변경 + 모든 호출 사이트 자동 추론 갱신.
2. **차트 lazy load** — `/backtests/[run_id]` First Load 가 220 kB (홈
   94 kB 의 2.3 배). recharts 가 110 kB+ 차지. `next/dynamic` 으로
   EquityChart / DrawdownChart 를 SSR 끄고 lazy import 하면 초기 페이지
   사이즈 절감.
3. **연도별 합계 컬럼** — MonthlyHeatmap 우측에 "연 합계" 컬럼 추가하면
   Quant Lab CLAUDE.md §4 의 "연 수익률 테이블" 도 한 화면에서 충족.
   `metrics.annual_returns` 를 그대로 표기하면 되므로 ~10 라인 추가.
4. **거래 통계 카드** — 통화 필터 위에 "총 매수 N / 매도 M / 통화별
   수수료 합" mini-stat 행 추가하면 trader 가 빠르게 sanity check 가능.
5. **EquityChart Y축 통화 단위** — 현재 raw 숫자만 표기. `run.base_
   currency` 받아서 `${value.toLocaleString()} ${currency}` 로 라벨링
   하면 다중 통화 환경에서 혼동 방지.
