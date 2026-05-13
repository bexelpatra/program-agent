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

// ─── JSON Schema descriptors (pydantic params_schema) ─────────────────
//
// Mirrors the structural shape `model_json_schema()` returns. Only the
// fields the UI consumes are validated; extra keys (e.g. `examples`,
// `format`, `pattern`) are stripped by Zod's default object behaviour
// but no runtime error. Backed by the TS interfaces in `./types.ts`.

const JsonSchemaPropertySchema = z.object({
  type: z.string().optional(),
  title: z.string().optional(),
  description: z.string().optional(),
  default: z.unknown().optional(),
  enum: z.array(z.unknown()).optional(),
});

const JsonSchemaObjectSchema = z.object({
  type: z.string().optional(),
  properties: z.record(JsonSchemaPropertySchema).optional(),
  required: z.array(z.string()).optional(),
});

// ─── Enums ─────────────────────────────────────────────────────────────

export const MarketEnum = z.enum(["KR", "US", "CRYPTO"]);
export type Market = z.infer<typeof MarketEnum>;

export const AssetTypeEnum = z.enum([
  "EQUITY_INDEX",
  "ETF",
  "BOND",
  "COMMODITY",
  "CRYPTO",
  // STOCK = Phase 2 테마주 트랙 (개별주) — backend AssetType literal 과 1:1 동기.
  "STOCK",
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
  // `optional()` (not `.default({})`) keeps Zod input/output variance
  // aligned for `z.array(AssetSchema)` consumers — see TASK-238.
  meta: z.record(z.unknown()).optional(),
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
  meta: z.record(z.unknown()).optional(),
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

// ─── OHLCV (TASK-204) ─────────────────────────────────────────────────
//
// Mirrors backend `OhlcvPoint` (backend/app/schemas/asset.py L63). `time`
// arrives as an ISO datetime string (FastAPI serialises `datetime.datetime`).
// `close` is required; OHLCV gaps may yield null open/high/low/adj_close/
// volume for partial back-fills. We use this on /backtests/new to fetch
// each universe asset's most recent close (≤ 14 day window) so we can
// preflight "1주 가격 > 비중 × 초기 자본" warnings before the user submits
// (TASK-204 — amber 경고 배너).

export const OhlcvPointSchema = z.object({
  time: z.string(),
  open: z.number().nullable().optional(),
  high: z.number().nullable().optional(),
  low: z.number().nullable().optional(),
  close: z.number(),
  adj_close: z.number().nullable().optional(),
  volume: z.number().nullable().optional(),
});
export type OhlcvPoint = z.infer<typeof OhlcvPointSchema>;

export const OhlcvListSchema = z.array(OhlcvPointSchema);
export type OhlcvList = z.infer<typeof OhlcvListSchema>;

// ─── Strategy registry ─────────────────────────────────────────────────

export const StrategyDescriptorSchema = z.object({
  name: z.string(),
  type: z.enum(["allocator", "filter"]),
  // Structural JSON Schema (object with `properties`/`required`) — the
  // UI consumes `properties[k].type/title/description/default/enum` to
  // render param fields. See `JsonSchemaObject` in `./types.ts`.
  params_schema: JsonSchemaObjectSchema,
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
    // `client.ts` ApiError requires a non-undefined Record; keep the
    // default to preserve that contract while dropping `any`.
    request_ctx: z.record(z.unknown()).default({}),
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
  "semi_annual",
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
  params: z.record(z.unknown()),
});
export type FilterConfig = z.infer<typeof FilterConfigSchema>;

/**
 * Strategy 3-요소 (allocator + filters AND + schedule).
 *
 * `allocator_params` / `filter_configs[].params` are loose dicts because
 * each allocator/filter has its own pydantic schema validated on the
 * server (StrategyDescriptor.params_schema → form). We keep them as
 * `z.record(z.unknown())` here so the runtime shape exactly mirrors what
 * the server accepts; per-strategy validation lives in the form widget.
 */
export const StrategyConfigSchema = z.object({
  allocator_name: z.string(),
  allocator_params: z.record(z.unknown()),
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
  error: z.record(z.unknown()).nullable().optional(),
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
  // `optional()` (no `.default({})`) — keeps Zod input/output variance
  // aligned for `BacktestResultSchema` consumers (see TASK-238). Call
  // sites already coalesce with `?? {}` (e.g. `result.metrics?.
  // monthly_returns ?? {}`) so dropping the default is safe.
  annual_returns: z.record(z.number()).optional(),
  monthly_returns: z.record(z.number()).optional(),
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

// ─── Pagination envelope (Phase 2 — TASK-306) ───────────────────────────
//
// 백엔드 `app/schemas/common.py` L52~ `PaginatedResponse[T]` 1:1 미러. 기존
// `PaginatedAssetsSchema` 는 자산 전용으로 굳어 있어, 테마 등 새 도메인에는
// `paginatedResponseSchema(...)` 로 제네릭 envelope 을 새로 생성한다.
export const paginatedResponseSchema = <T extends z.ZodTypeAny>(item: T) =>
  z.object({
    items: z.array(item),
    total: z.number(),
    page: z.number(),
    page_size: z.number(),
  });

// ─── Theme (Phase 2 — TASK-303 / TASK-305 / TASK-306) ───────────────────
//
// 백엔드 `app/schemas/theme.py` 의 11 스키마와 1:1 동기. 직렬화 주의:
//   - `created_at`, `added_at`, `occurred_at` 은 datetime → ISO string.
//   - `adjusted_start`, `adjusted_end` 는 date → "YYYY-MM-DD" string.
//   - `SeriesPoint.value` 는 백엔드 Decimal → JSON 직렬화 시 string 으로
//     올 수 있어, `z.coerce.number()` 로 number/string 양쪽 수용.

export const EventTypeEnum = z.enum(["ADDED", "REMOVED", "RECLASSIFIED"]);
export type EventType = z.infer<typeof EventTypeEnum>;

export const HistorySourceEnum = z.enum(["USER", "AUTO"]);
export type HistorySource = z.infer<typeof HistorySourceEnum>;

export const ChartAdjustmentReasonEnum = z.enum([
  "universe_start_later",
  "universe_end_earlier",
  "no_data",
  "ok",
]);
export type ChartAdjustmentReason = z.infer<typeof ChartAdjustmentReasonEnum>;

export const ThemeReadSchema = z.object({
  theme_id: z.number().int(),
  name: z.string(),
  slug: z.string(),
  description: z.string().nullable().optional(),
  user_id: z.string(),
  created_at: z.string(),
  // 목록 응답에서만 채워지는 옵션 필드 (backend Field default=None).
  member_count: z.number().int().nullable().optional(),
});

export const ThemeCreateSchema = z.object({
  name: z.string().min(1).max(120),
  slug: z.string().max(120).optional(),
  description: z.string().nullable().optional(),
  // backend default='local' — 미지정 시 클라이언트가 보내지 않으면 서버가 채움.
  user_id: z.string().min(1).max(64).optional(),
});

export const ThemeUpdateSchema = z.object({
  name: z.string().min(1).max(120).optional(),
  description: z.string().nullable().optional(),
});

export const ThemeAssetReadSchema = z.object({
  theme_id: z.number().int(),
  asset_id: z.number().int(),
  added_at: z.string(),
  removed_at: z.string().nullable().optional(),
  note: z.string().nullable().optional(),
});

export const ThemeDetailSchema = ThemeReadSchema.extend({
  active_members: z.array(ThemeAssetReadSchema).default([]),
});

export const ThemeAssetAddSchema = z.object({
  asset_id: z.number().int().min(1),
  note: z.string().nullable().optional(),
});

export const AssetThemeHistoryReadSchema = z.object({
  history_id: z.number().int(),
  asset_id: z.number().int(),
  theme_id: z.number().int(),
  event_type: EventTypeEnum,
  from_theme_id: z.number().int().nullable().optional(),
  occurred_at: z.string(),
  source: HistorySourceEnum,
  note: z.string().nullable().optional(),
});

/**
 * SeriesPoint — 정규화 차트 한 점 (백엔드 Decimal value).
 *
 * Pydantic 직렬화 시 Decimal 은 JSON string 으로 직렬화될 수 있어
 * (`"100.000000"`), `z.coerce.number()` 로 number / string 양쪽 수용.
 * frontend recharts 가 number 만 받으므로 여기서 number 로 강제 변환.
 */
export const SeriesPointSchema = z.object({
  time: z.string(),
  value: z.coerce.number(),
});

export const UniverseMetaSchema = z.object({
  adjusted_start: z.string(),
  adjusted_end: z.string(),
  affected_assets: z.array(z.number().int()).default([]),
  reason: ChartAdjustmentReasonEnum,
  message: z.string(),
});

/**
 * ThemeChartResponse — members 는 backend dict[int, ...] 직렬화 시 key 가
 * string 으로 변환되므로 `z.record(z.string(), ...)` 으로 받아야 한다.
 * 호출 사이트가 number key 가 필요하면 `Number(k)` 로 복원.
 */
export const ThemeChartResponseSchema = z.object({
  members: z.record(z.array(SeriesPointSchema)),
  aggregate: z.array(SeriesPointSchema),
  universe_meta: UniverseMetaSchema,
});

export const ThemeCompareItemSchema = z.object({
  name: z.string(),
  aggregate: z.array(SeriesPointSchema),
});

export const ThemeCompareResponseSchema = z.object({
  themes: z.record(ThemeCompareItemSchema),
  universe_meta: UniverseMetaSchema,
});

export const PaginatedThemesSchema = paginatedResponseSchema(ThemeReadSchema);

export const AssetThemeHistoryListSchema = z.array(AssetThemeHistoryReadSchema);
