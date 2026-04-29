/**
 * Zod schemas mirroring the backend FastAPI / Pydantic contract.
 *
 * Source of truth: backend `app/schemas/*.py` and the OpenAPI document
 * served at `/openapi.json` (TASK-060 / TASK-061).
 *
 * Whenever a backend schema changes, update the matching Zod schema here
 * and regenerate API client typings (TS compiler will surface the diff).
 */
import { z } from "zod";

// ─── Enums ─────────────────────────────────────────────────────────────

export const MarketEnum = z.enum(["KR", "US", "CRYPTO"]);
export type Market = z.infer<typeof MarketEnum>;

export const AssetTypeEnum = z.enum([
  "EQUITY_INDEX",
  "ETF",
  "BOND",
  "COMMODITY",
  "CRYPTO",
]);
export type AssetType = z.infer<typeof AssetTypeEnum>;

// ─── Asset ─────────────────────────────────────────────────────────────

export const AssetSchema = z.object({
  asset_id: z.number().int(),
  symbol: z.string(),
  market: MarketEnum,
  asset_type: AssetTypeEnum,
  currency: z.string(),
  name: z.string(),
  meta: z.record(z.any()).default({}),
  active: z.boolean(),
  start_date: z.string().nullable().optional(),
  last_ingested_at: z.string().nullable().optional(),
});
export type Asset = z.infer<typeof AssetSchema>;

export const AssetCreateSchema = z.object({
  symbol: z.string().min(1).max(32),
  market: MarketEnum,
  asset_type: AssetTypeEnum,
  currency: z.string().min(2).max(8),
  name: z.string().min(1).max(128),
  meta: z.record(z.any()).default({}),
});
export type AssetCreate = z.infer<typeof AssetCreateSchema>;

export const AssetCreateResponseSchema = z.object({
  asset: AssetSchema,
  backfill_enqueued: z.boolean(),
  note: z.string().nullable().optional(),
});
export type AssetCreateResponse = z.infer<typeof AssetCreateResponseSchema>;

export const PaginatedAssetsSchema = z.object({
  items: z.array(AssetSchema),
  total: z.number(),
  page: z.number(),
  page_size: z.number(),
});
export type PaginatedAssets = z.infer<typeof PaginatedAssetsSchema>;

// ─── Strategy registry ─────────────────────────────────────────────────

export const StrategyDescriptorSchema = z.object({
  name: z.string(),
  type: z.enum(["allocator", "filter"]),
  params_schema: z.record(z.any()),
  description: z.string().nullable().optional(),
});
export type StrategyDescriptor = z.infer<typeof StrategyDescriptorSchema>;

export const StrategyListResponseSchema = z.object({
  allocators: z.array(StrategyDescriptorSchema),
  filters: z.array(StrategyDescriptorSchema),
});
export type StrategyListResponse = z.infer<typeof StrategyListResponseSchema>;

// ─── Health ────────────────────────────────────────────────────────────

export const HealthResponseSchema = z.object({
  status: z.literal("ok"),
  version: z.string(),
});
export type HealthResponse = z.infer<typeof HealthResponseSchema>;

// ─── Error envelope ────────────────────────────────────────────────────

/**
 * Mirrors the backend's standard error envelope (architecture.md V3 §
 * 에러 모델). Every non-2xx response from our FastAPI surface should
 * decode to this shape; if not, the client falls back to a generic
 * HTTPError.
 */
export const ErrorResponseSchema = z.object({
  error: z.object({
    stage: z.string(),
    type: z.string(),
    message: z.string(),
    request_ctx: z.record(z.any()).default({}),
    trace_id: z.string(),
  }),
});
export type ErrorResponse = z.infer<typeof ErrorResponseSchema>;

// ─── Backtest ──────────────────────────────────────────────────────────
//
// Mirrors `backend/app/schemas/backtest.py` (TASK-062 산출물).
// 백테스트는 비동기 job 모델 — POST 가 즉시 pending 반환, GET 으로 progress
// 폴링, status='done' 일 때 /result 호출. 여기서는 생성·상태 응답까지만 정의.

export const BacktestStatusEnum = z.enum([
  "pending",
  "running",
  "done",
  "failed",
  "cancelled",
]);
export type BacktestStatus = z.infer<typeof BacktestStatusEnum>;

export const RebalanceScheduleEnum = z.enum([
  "daily",
  "weekly",
  "monthly",
  "quarterly",
  "yearly",
  "signal_event",
]);
export type RebalanceSchedule = z.infer<typeof RebalanceScheduleEnum>;

/**
 * Single filter entry inside a strategy config.
 *
 * Backend expects `[{name, params}, ...]` (list[dict]) — keep the
 * structure flat so the form layer can append/remove rows without a
 * mapping pass.
 */
export const FilterConfigSchema = z.object({
  name: z.string(),
  params: z.record(z.any()),
});
export type FilterConfig = z.infer<typeof FilterConfigSchema>;

/**
 * Strategy 3-요소 (allocator + filters AND + schedule).
 *
 * `allocator_params` / `filter_configs[].params` are loose dicts because
 * each allocator/filter has its own pydantic schema validated on the
 * server (StrategyDescriptor.params_schema → form). We keep them as
 * `z.record(z.any())` here so the runtime shape exactly mirrors what the
 * server accepts; per-strategy validation lives in the form widget.
 */
export const StrategyConfigSchema = z.object({
  allocator_name: z.string(),
  allocator_params: z.record(z.any()),
  filter_configs: z.array(FilterConfigSchema).default([]),
  rebalance_schedule: RebalanceScheduleEnum.default("monthly"),
});
export type StrategyConfig = z.infer<typeof StrategyConfigSchema>;

/**
 * POST /api/backtests payload.
 *
 * `period_start`/`period_end` are ISO date strings (YYYY-MM-DD); FastAPI
 * accepts both string and date for `datetime.date` fields. `initial_cash`
 * is a per-currency dict (e.g. {"KRW": 10_000_000}) — base_currency may
 * differ from the cash key (engine FX-converts).
 */
export const BacktestCreateSchema = z.object({
  name: z.string().nullable().optional(),
  strategy: StrategyConfigSchema,
  universe_asset_ids: z.array(z.number().int()).min(1),
  period_start: z.string(),
  period_end: z.string(),
  base_currency: z.string().min(2).max(8),
  initial_cash: z.record(z.number()),
});
export type BacktestCreate = z.infer<typeof BacktestCreateSchema>;

/**
 * Run meta returned by POST/GET /api/backtests/{run_id}.
 *
 * `error` is non-null only when status='failed' (mirrors the backend
 * standard error envelope shape — stage/type/message/request_ctx/
 * trace_id, see ErrorResponseSchema).
 */
export const BacktestRunSchema = z.object({
  run_id: z.number().int(),
  run_hash: z.string(),
  status: BacktestStatusEnum,
  progress: z.number().min(0).max(1),
  name: z.string().nullable().optional(),
  strategy_name: z.string(),
  period_start: z.string(),
  period_end: z.string(),
  base_currency: z.string(),
  created_at: z.string(),
  started_at: z.string().nullable().optional(),
  finished_at: z.string().nullable().optional(),
  error: z.record(z.any()).nullable().optional(),
});
export type BacktestRun = z.infer<typeof BacktestRunSchema>;

// ─── Backtest result (TASK-093) ────────────────────────────────────────
//
// Mirrors backend GET /api/backtests/{run_id}/result (TASK-062).
// Only fetched when the run's status='done'; before that, the result
// endpoint returns 404 / 409 and the UI keeps polling /api/backtests/
// {run_id} (TASK-094) instead.

/**
 * Single point on the equity curve. `time` is an ISO date string
 * ("YYYY-MM-DD"). `equity` is total NAV in `BacktestRun.base_currency`,
 * `cash` is the cash leg (also base-currency converted), and `drawdown`
 * is the running peak-to-trough ratio (negative or 0).
 */
export const EquityPointSchema = z.object({
  time: z.string(),
  equity: z.number(),
  cash: z.number(),
  drawdown: z.number(),
});
export type EquityPoint = z.infer<typeof EquityPointSchema>;

/**
 * Single executed trade. `commission` and `price` are in the asset's
 * native `currency` (not base_currency) — UI groups by currency to keep
 * comparisons honest (architecture.md V3 § UI/UX 원칙 4).
 */
export const TradeRecordSchema = z.object({
  time: z.string(),
  asset_id: z.number().int(),
  side: z.enum(["BUY", "SELL"]),
  qty: z.number(),
  price: z.number(),
  commission: z.number(),
  currency: z.string(),
});
export type TradeRecord = z.infer<typeof TradeRecordSchema>;

/**
 * Performance metrics envelope. CAGR/MDD/win_rate are ratios (0.12 ==
 * 12%). Sharpe/Sortino/Calmar are unit-less. Annual / monthly returns
 * are keyed by "YYYY" / "YYYY-MM" respectively (sparse — missing months
 * mean no data, not zero).
 *
 * Quant Lab CLAUDE.md §4: 결과 지표는 항상 CAGR/MDD/Sharpe/Sortino/
 * Calmar/승률 + 연·월 수익률 테이블을 계산.
 */
export const MetricsPayloadSchema = z.object({
  cagr: z.number(),
  mdd: z.number(),
  sharpe: z.number(),
  sortino: z.number(),
  calmar: z.number(),
  win_rate: z.number(),
  annual_returns: z.record(z.number()).default({}),
  monthly_returns: z.record(z.number()).default({}),
});
export type MetricsPayload = z.infer<typeof MetricsPayloadSchema>;

/**
 * Full backtest result envelope. `metrics` may be null for runs that
 * finished but produced no closed trades (e.g. zero-trade strategies);
 * the UI degrades gracefully and shows the equity / drawdown charts
 * only.
 */
export const BacktestResultSchema = z.object({
  run: BacktestRunSchema,
  equity_curve: z.array(EquityPointSchema),
  trades: z.array(TradeRecordSchema),
  metrics: MetricsPayloadSchema.nullable().optional(),
});
export type BacktestResult = z.infer<typeof BacktestResultSchema>;
