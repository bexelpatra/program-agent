---
agent: coder
task_id: TASK-238
status: DONE
timestamp: 2026-04-30T20:38:00
---

## 결과 요약

`lib/api/schemas.ts` 의 `z.record(z.any())` 7회 / `MetricsPayloadSchema.annual_returns·monthly_returns.default({})` 2회 가 만들어 내던 input/output variance 를 제거하고, 신규 `lib/api/types.ts` 를 단일 정의처(SoT) 로 만들었다. 3 호출처 (`/backtests/new`, `/backtests/[run_id]`, `UniverseSelector`) 의 `Awaited<ReturnType<typeof api.X>>` 트릭과 `as Record<string, { type?: string }>` 캐스트(1건) 를 모두 제거했다.

## 변경된 파일

### 신규
- `projects/stock-backtest/frontend/lib/api/types.ts` — `JsonSchemaProperty / JsonSchemaObject` 인터페이스 + `Asset / BacktestResult / StrategyDescriptor` z.infer 타입 단일 export. schemas.ts 에 대한 import 는 모두 `import type` 으로 작성해 런타임 cycle 없음.

### 수정
- `projects/stock-backtest/frontend/lib/api/schemas.ts`
  - JsonSchema 디스크립터 zod schema (`JsonSchemaPropertySchema`, `JsonSchemaObjectSchema`) 를 파일 내부에 정의.
  - L35 `Asset.meta`, L48 `AssetCreate.meta`: `z.record(z.any()).default({})` → `z.record(z.unknown()).optional()`. (배열 element 의 default 가 variance 의 주범)
  - L96 `StrategyDescriptor.params_schema`: `z.record(z.any())` → `JsonSchemaObjectSchema` (구조적 타입).
  - L128 `ErrorResponse.error.request_ctx`: `z.record(z.any()).default({})` → `z.record(z.unknown()).default({})`. (client.ts ApiError 가 required Record 를 기대하므로 default 보존, any → unknown 만 교체.)
  - L169 `FilterConfig.params`, L184 `StrategyConfig.allocator_params`: `z.record(z.any())` → `z.record(z.unknown())`.
  - L229 `BacktestRun.error`: `z.record(z.any()).nullable().optional()` → `z.record(z.unknown()).nullable().optional()`.
  - L286-287 `MetricsPayload.annual_returns / monthly_returns`: `z.record(z.number()).default({})` → `z.record(z.number()).optional()`. (consumer 들이 `?? {}` 로 이미 fallback 하므로 안전. variance 잔재를 마저 정리.)
- `projects/stock-backtest/frontend/components/backtest/StrategyParamsForm.tsx` — `JsonSchemaProperty / JsonSchemaObject` 자체 정의 12 줄 제거 후 `import type { ... } from "@/lib/api/types"` 로 대체.
- `projects/stock-backtest/frontend/app/backtests/new/page.tsx`
  - `type BacktestResult = Awaited<...>` 트릭 + 6 줄 주석 제거.
  - `import type { BacktestResult, StrategyDescriptor } from "@/lib/api/types"` 추가, schemas.ts 에서는 `BacktestCreate / FilterConfig / RebalanceSchedule / StrategyListResponse` 만 유지.
  - `findObjectParamKeys` 내부의 `as Record<string, { type?: string }>` 캐스트 제거 (params_schema.properties 가 이제 `Record<string, JsonSchemaProperty>` 로 정확히 타이핑됨).
- `projects/stock-backtest/frontend/app/backtests/[run_id]/page.tsx` — `type BacktestResult = Awaited<...>` 트릭 + 5 줄 주석 제거 → `import type { BacktestResult } from "@/lib/api/types"`.
- `projects/stock-backtest/frontend/components/backtest/UniverseSelector.tsx` — `Awaited<...>["items"][number]` 트릭 제거, `import type { Asset } from "@/lib/api/types"` 추가, `export type UniverseAsset = Asset` 로 별칭만 유지 (호출 사이트는 `UniverseAsset` 그대로 사용 가능).

## DoD 충족 검증

| 항목 | 결과 |
|------|------|
| 1. `npx tsc --noEmit` 0 에러 | ✅ 통과 (output empty) |
| 2. `as Record<string, { type?: string }>` 1건 제거 | ✅ `grep "as Record<string, { type"` 0 hit |
| 3. 3 호출처 `Awaited<...>` 트릭 + 주석 제거 | ✅ schemas.ts/types.ts/UniverseSelector.tsx 의 historical 주석 외에는 0 hit. (AssetTable.tsx 는 modify list 외라 그대로 — 후속 태스크 후보) |
| 4. `npx vitest run hooks/__tests__/` PASS | ✅ 6 tests pass |
| 5. `npm run build` PASS | ✅ Next.js production build 성공, 6 페이지 정적 생성 |

## 이슈/블로커

없음.

## 다음 제안

- **AssetTable.tsx 후속 정리**: `components/asset/AssetTable.tsx:23` 가 여전히 `Awaited<ReturnType<typeof api.listAssets>>["items"][number]` 를 사용한다. modify list 외였기 때문에 손대지 않았으나, 이제 `Asset` 타입이 `lib/api/types.ts` 에서 깨끗하게 export 되므로 `export type AssetRow = Asset` 로 단순화 가능 (1줄 수정 + 25줄 주석 정리). 별도 태스크로 등록 권장.
- **JsonSchemaObjectSchema export 여부**: 현재 schemas.ts 안에서만 사용되어 export 하지 않았다. 후속에 다른 곳에서 직접 검증할 일이 생기면 export 후 types.ts 가 type-only re-export 하는 식으로 정리.
- **변경된 public API 시그니처**: 없음 (frontend 전용, 백엔드 인터페이스 불변).
