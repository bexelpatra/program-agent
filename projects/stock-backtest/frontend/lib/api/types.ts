/**
 * Shared API-layer types for the Quant Lab frontend.
 *
 * Why this file exists (TASK-238):
 *   `lib/api/schemas.ts` defines Zod schemas that mirror the backend
 *   pydantic contract. Earlier code derived call-site types via the
 *   `Awaited<ReturnType<typeof api.X>>` trick (see /backtests/new/page
 *   .tsx:36, /backtests/[run_id]/page.tsx:45, UniverseSelector.tsx:27)
 *   because `z.infer<...>` produced subtly different *nominal* types
 *   from independent imports — caused by `.default({})` on
 *   `z.record(z.any())` introducing input/output variance that TS
 *   surfaced as a distinct shape per import boundary.
 *
 *   `schemas.ts` was tightened in parallel to drop the `any` (and the
 *   default on array-nested record fields), so input/output types now
 *   align. This module then re-exports the canonical inferred types
 *   so call sites can write `import { BacktestResult } from "@/lib/
 *   api/types"` instead of the Awaited trick.
 *
 *   `JsonSchemaProperty` / `JsonSchemaObject` interfaces describe the
 *   pydantic-emitted JSON Schema shape that `StrategyDescriptor.params
 *   _schema` carries. They were previously redeclared inside
 *   `StrategyParamsForm.tsx`; centralising them here lets the form,
 *   the backtest pages, and any future param-rendering code share one
 *   structural contract.
 */
import type { z } from "zod";

import type {
  AssetSchema,
  AssetThemeHistoryReadSchema,
  BacktestResultSchema,
  PaginatedThemesSchema,
  SeriesPointSchema,
  StrategyDescriptorSchema,
  ThemeAssetAddSchema,
  ThemeAssetReadSchema,
  ThemeChartResponseSchema,
  ThemeCompareItemSchema,
  ThemeCompareResponseSchema,
  ThemeCreateSchema,
  ThemeDetailSchema,
  ThemeReadSchema,
  ThemeUpdateSchema,
  UniverseMetaSchema,
} from "./schemas";

// ─── JSON Schema descriptors (pydantic params_schema) ───────────────────

/**
 * One top-level property emitted by pydantic's `model_json_schema()`
 * for an allocator/filter param. We only model the fields the UI
 * actually uses; backend may attach more (e.g. `examples`, `format`,
 * `pattern`).
 */
export interface JsonSchemaProperty {
  type?: string;
  title?: string;
  description?: string;
  default?: unknown;
  enum?: unknown[];
}

/**
 * Object-typed JSON Schema (the shape pydantic produces for a model's
 * `model_json_schema()`). `properties` keys map to one
 * `JsonSchemaProperty` each.
 */
export interface JsonSchemaObject {
  type?: string;
  properties?: Record<string, JsonSchemaProperty>;
  required?: string[];
}

// ─── Re-exported inferred types ─────────────────────────────────────────
//
// Importing call sites should prefer these over `z.infer<...>` directly,
// so future schema-shape adjustments stay isolated to this module.

export type Asset = z.infer<typeof AssetSchema>;
export type BacktestResult = z.infer<typeof BacktestResultSchema>;
export type StrategyDescriptor = z.infer<typeof StrategyDescriptorSchema>;

// ─── Theme (Phase 2 — TASK-306) ─────────────────────────────────────────
//
// 백엔드 `app/schemas/theme.py` 미러 (schemas.ts). 모든 타입은 z.infer SoT
// 패턴 (TASK-238 결정) — `Awaited<ReturnType<...>>` 트릭 금지.

export type Theme = z.infer<typeof ThemeReadSchema>;
export type ThemeCreate = z.infer<typeof ThemeCreateSchema>;
export type ThemeUpdate = z.infer<typeof ThemeUpdateSchema>;
export type ThemeDetail = z.infer<typeof ThemeDetailSchema>;
export type ThemeAsset = z.infer<typeof ThemeAssetReadSchema>;
export type ThemeAssetAdd = z.infer<typeof ThemeAssetAddSchema>;
export type AssetThemeHistory = z.infer<typeof AssetThemeHistoryReadSchema>;
export type SeriesPoint = z.infer<typeof SeriesPointSchema>;
export type UniverseMeta = z.infer<typeof UniverseMetaSchema>;
export type ThemeChartResponse = z.infer<typeof ThemeChartResponseSchema>;
export type ThemeCompareItem = z.infer<typeof ThemeCompareItemSchema>;
export type ThemeCompareResponse = z.infer<typeof ThemeCompareResponseSchema>;
export type PaginatedThemes = z.infer<typeof PaginatedThemesSchema>;
