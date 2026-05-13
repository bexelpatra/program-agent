"use client";

/**
 * ThemeCompareChart — 다중 테마 비교 차트 (TASK-308).
 *
 * `api.compareThemes(theme_ids, opts)` 응답을 입력. 각 테마의 aggregate
 * (equal weighting 합산) 라인을 동일 차트에 겹쳐 출력. NormalizedPriceChart
 * 와 동일한 색상 팔레트를 재사용해 시각 일관성 유지.
 *
 * universe_meta 통지는 본 컴포넌트가 직접 toast 를 띄우지 않고, 상위
 * 페이지가 useState 로 받아 토스트를 띄운다 (UI 분리 — 본 컴포넌트는
 * pure presentational).
 */
import {
  CartesianGrid,
  Legend,
  Line,
  LineChart,
  ReferenceLine,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import type { ThemeCompareItem } from "@/lib/api/types";

import { SERIES_COLORS } from "./NormalizedPriceChart";

interface MergedRow {
  time: string;
  [themeKey: string]: string | number;
}

export interface ThemeCompareChartProps {
  /** 백엔드 ThemeCompareResponse.themes — key 는 theme_id (string). */
  themes: Record<string, ThemeCompareItem>;
  height?: number;
}

/** 다중 테마 aggregate 시계열을 time 기준으로 union/merge. */
export function mergeThemes(
  themes: Record<string, ThemeCompareItem>,
): MergedRow[] {
  const timeMap = new Map<string, MergedRow>();
  for (const [tid, item] of Object.entries(themes)) {
    for (const p of item.aggregate) {
      const row = timeMap.get(p.time) ?? { time: p.time };
      row[tid] = p.value;
      timeMap.set(p.time, row);
    }
  }
  return Array.from(timeMap.values()).sort((a, b) =>
    a.time.localeCompare(b.time),
  );
}

export function ThemeCompareChart({
  themes,
  height = 320,
}: ThemeCompareChartProps) {
  const themeKeys = Object.keys(themes);
  if (themeKeys.length === 0) {
    return (
      <div className="p-4 text-sm text-gray-500">
        비교할 테마를 1개 이상 선택하세요.
      </div>
    );
  }
  const data = mergeThemes(themes);
  if (data.length === 0) {
    return (
      <div className="p-4 text-sm text-gray-500">
        선택한 테마들의 공통 데이터가 없습니다.
      </div>
    );
  }

  return (
    <ResponsiveContainer width="100%" height={height}>
      <LineChart
        data={data}
        margin={{ top: 8, right: 16, bottom: 0, left: 0 }}
      >
        <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
        <XAxis dataKey="time" tick={{ fontSize: 11 }} minTickGap={32} />
        <YAxis
          tick={{ fontSize: 11 }}
          domain={["auto", "auto"]}
          tickFormatter={(v: number) => v.toFixed(0)}
        />
        <ReferenceLine
          y={100}
          stroke="#9ca3af"
          strokeDasharray="4 4"
          label={{ value: "기준 100", fontSize: 10, fill: "#6b7280" }}
        />
        <Tooltip
          formatter={(v: number, name: string) => [
            v.toFixed(2),
            themes[name]?.name ?? `테마 ${name}`,
          ]}
          labelFormatter={(t: string) => `날짜: ${t}`}
          labelClassName="text-xs"
        />
        <Legend
          formatter={(value: string) =>
            themes[value]?.name ?? `테마 ${value}`
          }
          wrapperStyle={{ fontSize: 11 }}
        />
        {themeKeys.map((tid, idx) => (
          <Line
            key={tid}
            type="monotone"
            dataKey={tid}
            name={tid}
            stroke={SERIES_COLORS[idx % SERIES_COLORS.length]}
            dot={false}
            strokeWidth={2}
            isAnimationActive={false}
            connectNulls
          />
        ))}
      </LineChart>
    </ResponsiveContainer>
  );
}
