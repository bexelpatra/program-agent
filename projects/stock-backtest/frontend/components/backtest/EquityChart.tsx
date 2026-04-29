"use client";

/**
 * EquityChart — equity curve over the backtest period.
 *
 * Single-line chart of total NAV (`equity` field) in the run's
 * base_currency. Toggle between linear and log Y-axis from the parent
 * page (long backtests with compounding benefit from log scale —
 * architecture.md V3 § UI/UX 원칙 4 implies "자본 곡선" should be
 * legible across multi-year horizons).
 *
 * Cash leg is intentionally not plotted here — it lives in the trades
 * table. Drawdown gets its own panel (DrawdownChart).
 */
import {
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import type { EquityPoint } from "@/lib/api/schemas";

interface EquityChartProps {
  points: EquityPoint[];
  logScale: boolean;
}

export function EquityChart({ points, logScale }: EquityChartProps) {
  if (points.length === 0) {
    return (
      <div className="p-4 text-sm text-gray-500">데이터가 없습니다.</div>
    );
  }

  return (
    <ResponsiveContainer width="100%" height={300}>
      <LineChart data={points} margin={{ top: 8, right: 16, bottom: 0, left: 0 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
        <XAxis dataKey="time" tick={{ fontSize: 11 }} minTickGap={32} />
        <YAxis
          scale={logScale ? "log" : "linear"}
          domain={["auto", "auto"]}
          tick={{ fontSize: 11 }}
          allowDataOverflow={logScale}
        />
        <Tooltip
          formatter={(v: number) => v.toLocaleString()}
          labelClassName="text-xs"
        />
        <Line
          type="monotone"
          dataKey="equity"
          stroke="#2563eb"
          dot={false}
          strokeWidth={2}
          isAnimationActive={false}
        />
      </LineChart>
    </ResponsiveContainer>
  );
}
