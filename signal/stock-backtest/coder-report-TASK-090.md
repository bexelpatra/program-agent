---
task_id: TASK-090
agent: coder
status: DONE
severity: none
date: 2026-04-29
parallel_with: TASK-062
---

# TASK-090 — Frontend foundation (Next.js + shadcn/ui + Zod + ko i18n + API client)

## 요약

`projects/stock-backtest/frontend/` 에 다음을 추가/갱신했다:

- **lib/utils.ts** — `cn()` 헬퍼 (clsx + tailwind-merge, 표준 shadcn 패턴)
- **lib/api/schemas.ts** — 백엔드 Pydantic 1:1 Zod 스키마 (Asset, AssetCreate, PaginatedAssets, StrategyDescriptor, ErrorResponse, Health)
- **lib/api/client.ts** — `fetchAndValidate` 단일 함수 + `ApiError` 클래스 (trace_id 보존). `api.health/listAssets/getAsset/createAsset/listStrategies` 5종 surface
- **lib/i18n/ko.ts** — 한국어 dict + `t(path)` dot-path lookup + missing-key fallback
- **components/ui/{button,input,card,label,select,badge,toast}.tsx** — shadcn 표준 패턴 7종
- **app/layout.tsx** — `<ToastProvider>` 추가
- **app/page.tsx** — 홈 placeholder 를 한국어 + 3-카드 레이아웃 (Card/Button) 으로 갱신

`backend/`, `signal/`, `frontend/package.json`, 기존 백엔드 어떤 파일도 건드리지 않았다 (TASK-062 와 병렬 안전).

## 변경된 파일 (전체)

신규:
- `projects/stock-backtest/frontend/lib/utils.ts`
- `projects/stock-backtest/frontend/lib/api/schemas.ts`
- `projects/stock-backtest/frontend/lib/api/client.ts`
- `projects/stock-backtest/frontend/lib/i18n/ko.ts`
- `projects/stock-backtest/frontend/components/ui/button.tsx`
- `projects/stock-backtest/frontend/components/ui/input.tsx`
- `projects/stock-backtest/frontend/components/ui/card.tsx`
- `projects/stock-backtest/frontend/components/ui/label.tsx`
- `projects/stock-backtest/frontend/components/ui/select.tsx`
- `projects/stock-backtest/frontend/components/ui/badge.tsx`
- `projects/stock-backtest/frontend/components/ui/toast.tsx`

수정:
- `projects/stock-backtest/frontend/app/layout.tsx` — ToastProvider 래핑
- `projects/stock-backtest/frontend/app/page.tsx` — 한국어 + Card/Button 사용

## DoD 검증 결과

| # | 항목 | 명령 | 결과 |
|---|------|------|------|
| 1 | TypeScript 타입체크 | `npx tsc --noEmit` | exit 0, 에러 없음 |
| 2 | Next.js production build | `npm run build` | `✓ Compiled successfully` · `Route(/) 6.98 kB` 정적 prerender |
| 3 | dev 서버 200 + 한국어 | `PORT=3010 npm run dev` → `curl localhost:3010/` | HTTP 200, "Quant Lab" / "퀀트 투자" / "새 백테스트" / "자산 카탈로그" 4문자열 모두 HTML 에 출현 |
| 4 | shadcn 컴포넌트 import | smoke `tsx` 스크립트 | Button/Card/Input/Select/Badge 5종 truthy |
| 5 | `t()` lookup | smoke 스크립트 | `t("app.title")="Quant Lab"`, `t("asset.market.KR")="한국"`, `t("nonexistent.key")="nonexistent.key"` (fallback OK) |
| 추가 | Zod schema parse | smoke 스크립트 | AssetSchema/AssetCreateSchema parse success=true, MarketEnum=[KR,US,CRYPTO], AssetTypeEnum 5종 정상 |

dev 서버 포트는 3001 이 점유돼 3010 으로 변경. ethics-study 8000 포트 규약과는 무관 (frontend 는 dev 시 임의 포트 사용).

## 신규 public API surface

### `@/lib/utils`
- `cn(...ClassValue[]): string` — clsx + tailwind-merge 결합

### `@/lib/api/schemas`
- 타입: `Asset`, `AssetCreate`, `AssetCreateResponse`, `PaginatedAssets`, `StrategyDescriptor`, `StrategyListResponse`, `HealthResponse`, `ErrorResponse`, `Market`, `AssetType`
- 스키마: 위 각 타입에 대응하는 `*Schema` Zod 객체
- enum: `MarketEnum`, `AssetTypeEnum`

### `@/lib/api/client`
```ts
api.health(): Promise<HealthResponse>
api.listAssets(params?: ListAssetsParams): Promise<PaginatedAssets>
api.getAsset(assetId: number): Promise<Asset>
api.createAsset(payload: AssetCreate): Promise<AssetCreateResponse>
api.listStrategies(): Promise<StrategyListResponse>

class ApiError extends Error {
  status: number; stage: string; type: string;
  traceId: string; requestCtx: Record<string, unknown>;
}
```
- `BASE_URL`은 `process.env.NEXT_PUBLIC_API_BASE_URL` 우선, 미설정 시 `http://localhost:8001`
- 네트워크 실패 → `ApiError(stage="network")`
- 백엔드 ErrorResponse 디코딩 성공 → `ApiError(stage=원본 stage, traceId=원본)`
- Zod validation 실패 → `ApiError(stage="client_validation")`

### `@/lib/i18n/ko`
- `ko` (deeply readonly dict)
- `t(path: string): string` — dot-path lookup, 미스 시 path 반환

### `@/components/ui/*`
- `<Button variant size>` — default/secondary/destructive/outline/ghost · default/sm/lg/icon
- `<Input>` — 표준 shadcn input
- `<Card>` `<CardHeader>` `<CardTitle>` `<CardDescription>` `<CardContent>` `<CardFooter>`
- `<Label>` — 단순 label, peer-disabled 대응
- `<Select>` — 네이티브 `<select>` + shadcn 크롬 (Radix 추후 swap 가능)
- `<Badge variant>` — default/secondary/success/warning/destructive/outline
- `<ToastProvider>` + `useToast()` + `toast({title, description, variant, durationMs})` — sonner 없이 자체 구현, API 는 sonner-호환

## 클린 코드 점검

- ✅ DRY: 모든 fetch 가 `fetchAndValidate` 단일 함수 통과
- ✅ 단일 진실 원본: Zod schema → TS 타입 (`z.infer`) 1방향 도출
- ✅ 에러 모델: `ApiError.traceId` 로 백엔드 trace_id 보존 → UI 에서 노출 가능 (UI/UX 원칙 2 충족)
- ✅ 한국어 우선: ko.ts 가 단일 catalogue, 영문 약어는 metric 명에만 병기 ("샤프지수 (Sharpe)")
- ✅ shadcn 표준: cva variants + ref forwarding + displayName
- ✅ `any` 0건 (smoke 검증), strict 모드 통과

## 다음 제안

- **TASK-091 자산 카탈로그 화면** — `app/assets/page.tsx` 에서 `useState` + `api.listAssets({q, market})` 로 검색 + `api.createAsset()` 폼. 본 태스크의 모든 surface 가 즉시 사용 가능. shadcn Card/Input/Select/Button + ToastProvider 의 `useToast()` 로 백필 enqueue 알림.
- **TASK-094 next-intl 풀 셋업 (선택)** — 현재 `t()` 는 단순 dict lookup. 만약 영문 locale 추가 또는 plural/interpolation 이 필요해지면 next-intl (이미 deps 에 설치됨) 도입. 마이그레이션은 ko.ts → `messages/ko.json` 평탄화 후 `useTranslations()` 치환.
- **에러 토스트 헬퍼** — `useToast()` + `ApiError` 조합을 `useApiErrorToast()` 훅으로 추출하면 `try { await api.x() } catch (e) { showApiError(e) }` 패턴이 더 짧아진다. TASK-091 진행하면서 패턴이 굳어지면 추출.
- **Sonner 또는 Radix Toast 로 교체 (선택)** — 현재 자체 구현은 swipe-to-dismiss / 큐잉 / 애니메이션이 없다. UX 가 더 필요해지면 `npm i sonner` 후 `ToastProvider`/`useToast` 만 wrapper 로 교체.

## 이슈/블로커

없음.
