"use client";

/**
 * ThemeAggregateChart — 테마 멤버를 equal weighting (또는 market_cap)
 * 으로 합산한 단일 시계열 (TASK-308).
 *
 * NormalizedPriceChart 가 멤버별 라인을 보여주는 반면, 본 차트는 "테마
 * 전체" 의 흐름 한 줄로 압축. base100 으로 rebase 되어 있으므로 100 을
 * 기준으로 위/아래 등락을 한눈에 본다. (architecture.md V3 § "정규화
 * 차트 사양" — aggregate 라인은 단독 카드로 분리).
 */
import {
  CartesianGrid,
  Line,
  LineChart,
  ReferenceLine,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import type { SeriesPoint } from "@/lib/api/types";

export interface ThemeAggregateChartProps {
  points: SeriesPoint[];
  /** Tooltip / 범례에 사용할 테마 이름. 기본 "테마 합산". */
  label?: string;
  height?: number;
}

export function ThemeAggregateChart({
  points,
  label = "테마 합산",
  height = 280,
}: ThemeAggregateChartProps) {
  if (points.length === 0) {
    return (
      <div className="p-4 text-sm text-gray-500">합산 데이터가 없습니다.</div>
    );
  }

  return (
    <ResponsiveContainer width="100%" height={height}>
      <LineChart
        data={points}
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
          formatter={(v: number) => [v.toFixed(2), label]}
          labelFormatter={(t: string) => `날짜: ${t}`}
          labelClassName="text-xs"
        />
        <Line
          type="monotone"
          dataKey="value"
          name={label}
          stroke="#2563eb"
          dot={false}
          strokeWidth={2}
          isAnimationActive={false}
        />
      </LineChart>
    </ResponsiveContainer>
  );
}
