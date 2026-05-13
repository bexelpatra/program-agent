/**
 * Typed API client for the Quant Lab backend.
 *
 * Every request runs through `fetchAndValidate`, which:
 *   1. issues `fetch` with a JSON Content-Type
 *   2. on non-2xx responses, decodes the standard error envelope
 *      (`ErrorResponseSchema`) and throws an `ApiError` carrying the
 *      stage / type / trace_id (UI/UX 원칙 2: trace_id 노출 가능)
 *   3. on 2xx, runs Zod validation against the supplied schema and
 *      throws `ApiError(stage="client_validation")` on mismatch.
 *
 * Always import `api` from this module; do not call `fetch` directly
 * elsewhere in the frontend.
 */
import { z } from "zod";

import {
  AssetSchema,
  AssetCreateResponseSchema,
  AssetThemeHistoryListSchema,
  type AssetCreate,
  type BacktestCreate,
  BacktestResultSchema,
  BacktestRunSchema,
  ErrorResponseSchema,
  HealthResponseSchema,
  OhlcvListSchema,
  PaginatedAssetsSchema,
  PaginatedThemesSchema,
  StrategyListResponseSchema,
  ThemeAssetReadSchema,
  ThemeChartResponseSchema,
  ThemeCompareResponseSchema,
  ThemeDetailSchema,
  ThemeReadSchema,
} from "./schemas";
import type {
  ThemeAssetAdd,
  ThemeCreate,
  ThemeUpdate,
} from "./types";

const BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8001";

export class ApiError extends Error {
  constructor(
    public readonly status: number,
    public readonly stage: string,
    public readonly type: string,
    message: string,
    public readonly traceId: string,
    public readonly requestCtx: Record<string, unknown>,
  ) {
    super(message);
    this.name = "ApiError";
  }
}

async function fetchAndValidate<T>(
  path: string,
  schema: z.ZodSchema<T>,
  init?: RequestInit,
): Promise<T> {
  let res: Response;
  try {
    res = await fetch(`${BASE_URL}${path}`, {
      headers: { "Content-Type": "application/json", ...(init?.headers ?? {}) },
      ...init,
    });
  } catch (networkErr) {
    throw new ApiError(
      0,
      "network",
      "NetworkError",
      networkErr instanceof Error ? networkErr.message : String(networkErr),
      "",
      { path },
    );
  }

  if (!res.ok) {
    let errBody: unknown = null;
    try {
      errBody = await res.json();
    } catch {
      // body wasn't JSON; fall through to generic HTTPError
    }
    const parsed = ErrorResponseSchema.safeParse(errBody);
    if (parsed.success) {
      const e = parsed.data.error;
      throw new ApiError(
        res.status,
        e.stage,
        e.type,
        e.message,
        e.trace_id,
        e.request_ctx,
      );
    }
    throw new ApiError(
      res.status,
      "unknown",
      "HTTPError",
      `HTTP ${res.status}`,
      "",
      { path },
    );
  }

  const body: unknown = await res.json();
  const parsed = schema.safeParse(body);
  if (!parsed.success) {
    throw new ApiError(
      0,
      "client_validation",
      "ZodError",
      parsed.error.message,
      "",
      { path },
    );
  }
  return parsed.data;
}

/**
 * 204 No Content DELETE 헬퍼 (TASK-306).
 *
 * `fetchAndValidate` 는 항상 res.json() 을 시도하므로 204 응답에는 적용할 수
 * 없다. cancelBacktest 가 이미 동일 패턴을 inline 으로 보유하지만, theme
 * delete 두 곳에서 재사용하기 위해 작은 헬퍼로 추출. 비2xx 면 ApiError 를
 * 동일 contract 로 던지고, 2xx (204 포함) 면 그냥 반환.
 */
async function deleteNoContent(path: string): Promise<void> {
  let res: Response;
  try {
    res = await fetch(`${BASE_URL}${path}`, {
      method: "DELETE",
      headers: { "Content-Type": "application/json" },
    });
  } catch (networkErr) {
    throw new ApiError(
      0,
      "network",
      "NetworkError",
      networkErr instanceof Error ? networkErr.message : String(networkErr),
      "",
      { path, method: "DELETE" },
    );
  }
  if (!res.ok) {
    let errBody: unknown = null;
    try {
      errBody = await res.json();
    } catch {
      // body wasn't JSON; fall through to generic HTTPError
    }
    const parsed = ErrorResponseSchema.safeParse(errBody);
    if (parsed.success) {
      const e = parsed.data.error;
      throw new ApiError(
        res.status,
        e.stage,
        e.type,
        e.message,
        e.trace_id,
        e.request_ctx,
      );
    }
    throw new ApiError(
      res.status,
      "unknown",
      "HTTPError",
      `HTTP ${res.status}`,
      "",
      { path, method: "DELETE" },
    );
  }
}

// ─── Public surface ─────────────────────────────────────────────────────

export interface ListAssetsParams {
  q?: string;
  market?: string;
  asset_type?: string;
  limit?: number;
  offset?: number;
}

export const api = {
  // health
  health: () => fetchAndValidate("/api/health", HealthResponseSchema),

  // assets
  listAssets: (params?: ListAssetsParams) => {
    const qs = new URLSearchParams();
    if (params?.q) qs.set("q", params.q);
    if (params?.market) qs.set("market", params.market);
    if (params?.asset_type) qs.set("asset_type", params.asset_type);
    if (params?.limit !== undefined) qs.set("limit", String(params.limit));
    if (params?.offset !== undefined) qs.set("offset", String(params.offset));
    const suffix = qs.toString() ? `?${qs.toString()}` : "";
    return fetchAndValidate(`/api/assets${suffix}`, PaginatedAssetsSchema);
  },

  getAsset: (assetId: number) =>
    fetchAndValidate(`/api/assets/${assetId}`, AssetSchema),

  // TASK-204: 자산 일봉 OHLCV. start/end 는 ISO date (YYYY-MM-DD).
  // /backtests/new 에서 최근 close 가격을 prefetch 해 매수 불가능
  // 자산을 사전에 amber 경고로 안내하는 데 사용.
  getAssetOhlcv: (assetId: number, start: string, end: string) =>
    fetchAndValidate(
      `/api/assets/${assetId}/ohlcv?start=${start}&end=${end}`,
      OhlcvListSchema,
    ),

  // TASK-204: 자산의 가장 최근 일봉 close 를 조회.
  // 직전 14일 윈도우(주말·공휴일·갭 흡수)로 OHLCV 호출 후 마지막 row 의
  // close 를 반환. 데이터가 1건도 없으면 null (백필 미완료 자산 또는
  // 신규 등록 직후). 호출 사이트에서 null 은 "경고 평가 보류" 처리.
  getAssetLatestPrice: async (assetId: number): Promise<number | null> => {
    const today = new Date();
    const end = today.toISOString().slice(0, 10);
    const startDate = new Date(today);
    startDate.setDate(startDate.getDate() - 14);
    const start = startDate.toISOString().slice(0, 10);
    const points = await fetchAndValidate(
      `/api/assets/${assetId}/ohlcv?start=${start}&end=${end}`,
      OhlcvListSchema,
    );
    if (points.length === 0) return null;
    return points[points.length - 1].close;
  },

  createAsset: (payload: AssetCreate) =>
    fetchAndValidate("/api/assets", AssetCreateResponseSchema, {
      method: "POST",
      body: JSON.stringify(payload),
    }),

  // strategies
  listStrategies: () =>
    fetchAndValidate("/api/strategies", StrategyListResponseSchema),

  // backtests (TASK-092 — async job model: POST returns pending, then poll
  // GET /api/backtests/{run_id} until status='done', then call /result).
  createBacktest: (payload: BacktestCreate) =>
    fetchAndValidate("/api/backtests", BacktestRunSchema, {
      method: "POST",
      body: JSON.stringify(payload),
    }),

  getBacktest: (runId: number) =>
    fetchAndValidate(`/api/backtests/${runId}`, BacktestRunSchema),

  // TASK-093 — full result (equity_curve + trades + metrics). Only call
  // when the run's status === 'done'; before then the backend returns
  // 404/409 and the UI continues polling getBacktest() instead.
  getBacktestResult: (runId: number) =>
    fetchAndValidate(`/api/backtests/${runId}/result`, BacktestResultSchema),

  // ─── Themes (Phase 2 — TASK-306) ──────────────────────────────────────
  //
  // 백엔드 `app/api/themes.py` (prefix=/api/themes) 와 1:1 매핑. compare/
  // chart 는 query string 빌더 분리. 모든 메서드는 `fetchAndValidate` 의
  // Zod 검증을 통과해야 데이터가 호출 사이트에 도달한다.

  listThemes: (userId?: string, limit?: number, offset?: number) => {
    const qs = new URLSearchParams();
    if (userId) qs.set("user_id", userId);
    if (limit !== undefined) qs.set("limit", String(limit));
    if (offset !== undefined) qs.set("offset", String(offset));
    const suffix = qs.toString() ? `?${qs.toString()}` : "";
    return fetchAndValidate(`/api/themes${suffix}`, PaginatedThemesSchema);
  },

  createTheme: (payload: ThemeCreate) =>
    fetchAndValidate("/api/themes", ThemeReadSchema, {
      method: "POST",
      body: JSON.stringify(payload),
    }),

  getTheme: (themeId: number) =>
    fetchAndValidate(`/api/themes/${themeId}`, ThemeDetailSchema),

  updateTheme: (themeId: number, payload: ThemeUpdate) =>
    fetchAndValidate(`/api/themes/${themeId}`, ThemeReadSchema, {
      method: "PATCH",
      body: JSON.stringify(payload),
    }),

  // 204 No Content — JSON 파싱 불가하므로 cancelBacktest 패턴으로 raw fetch.
  deleteTheme: async (themeId: number): Promise<void> => {
    await deleteNoContent(`/api/themes/${themeId}`);
  },

  addAssetToTheme: (themeId: number, payload: ThemeAssetAdd) =>
    fetchAndValidate(
      `/api/themes/${themeId}/assets`,
      ThemeAssetReadSchema,
      {
        method: "POST",
        body: JSON.stringify(payload),
      },
    ),

  removeAssetFromTheme: async (
    themeId: number,
    assetId: number,
  ): Promise<void> => {
    await deleteNoContent(`/api/themes/${themeId}/assets/${assetId}`);
  },

  /**
   * 정규화 차트 (rebase=100). normalize 디폴트 'base100', weighting 디폴트
   * 'equal' — Phase 2.1 MVP. start/end 미지정 시 universe 시작일 교집합 자동.
   */
  getThemeChart: (
    themeId: number,
    opts?: {
      normalize?: "base100";
      weighting?: "equal" | "market_cap";
      start?: string;
      end?: string;
      baseCurrency?: string;
    },
  ) => {
    const qs = new URLSearchParams();
    if (opts?.normalize) qs.set("normalize", opts.normalize);
    if (opts?.weighting) qs.set("weighting", opts.weighting);
    if (opts?.start) qs.set("start", opts.start);
    if (opts?.end) qs.set("end", opts.end);
    if (opts?.baseCurrency) qs.set("base_currency", opts.baseCurrency);
    const suffix = qs.toString() ? `?${qs.toString()}` : "";
    return fetchAndValidate(
      `/api/themes/${themeId}/chart${suffix}`,
      ThemeChartResponseSchema,
    );
  },

  /**
   * 다중 테마 비교. `theme_ids` 는 반복 (?theme_ids=1&theme_ids=2) 또는
   * 콤마 구분 둘 다 지원되지만 여기서는 반복 형식으로 고정.
   */
  compareThemes: (
    themeIds: number[],
    opts?: {
      normalize?: "base100";
      weighting?: "equal" | "market_cap";
      start?: string;
      end?: string;
      baseCurrency?: string;
    },
  ) => {
    const qs = new URLSearchParams();
    for (const id of themeIds) {
      qs.append("theme_ids", String(id));
    }
    if (opts?.normalize) qs.set("normalize", opts.normalize);
    if (opts?.weighting) qs.set("weighting", opts.weighting);
    if (opts?.start) qs.set("start", opts.start);
    if (opts?.end) qs.set("end", opts.end);
    if (opts?.baseCurrency) qs.set("base_currency", opts.baseCurrency);
    return fetchAndValidate(
      `/api/themes/compare?${qs.toString()}`,
      ThemeCompareResponseSchema,
    );
  },

  // 자산의 테마 변경 이력 (assets.py 라우터 — /api/assets/{id}/theme_history).
  getAssetThemeHistory: (assetId: number) =>
    fetchAndValidate(
      `/api/assets/${assetId}/theme_history`,
      AssetThemeHistoryListSchema,
    ),

  // TASK-094: pending/running 일 때는 cancel_requested 플래그 set,
  // 그 외 (done/failed/cancelled) 면 row 삭제. 백엔드는 양 경우 모두
  // 204 No Content 를 반환 (응답 body 없음 → fetchAndValidate 의
  // JSON 파싱 경로를 우회). 비2xx 일 때만 ApiError 를 던진다.
  cancelBacktest: async (runId: number): Promise<void> => {
    const path = `/api/backtests/${runId}`;
    let res: Response;
    try {
      res = await fetch(`${BASE_URL}${path}`, {
        method: "DELETE",
        headers: { "Content-Type": "application/json" },
      });
    } catch (networkErr) {
      throw new ApiError(
        0,
        "network",
        "NetworkError",
        networkErr instanceof Error ? networkErr.message : String(networkErr),
        "",
        { path, method: "DELETE" },
      );
    }
    if (!res.ok) {
      let errBody: unknown = null;
      try {
        errBody = await res.json();
      } catch {
        // body wasn't JSON; fall through to generic HTTPError
      }
      const parsed = ErrorResponseSchema.safeParse(errBody);
      if (parsed.success) {
        const e = parsed.data.error;
        throw new ApiError(
          res.status,
          e.stage,
          e.type,
          e.message,
          e.trace_id,
          e.request_ctx,
        );
      }
      throw new ApiError(
        res.status,
        "unknown",
        "HTTPError",
        `HTTP ${res.status}`,
        "",
        { path, method: "DELETE" },
      );
    }
  },
};
