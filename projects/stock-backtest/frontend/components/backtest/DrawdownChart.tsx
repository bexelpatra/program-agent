"use client";

/**
 * DrawdownChart — running peak-to-trough drawdown.
 *
 * Filled area below zero (drawdowns are non-positive ratios; backend
 * computes `running_max - equity / running_max` and stores as a negative
 * number for display — see TASK-053/062). MDD is the most negative
 * value on this curve.
 *
 * architecture.md V3 § UI/UX 원칙 4 — separate panel from the equity
 * curve so the user can scan losses independently of the upward bias of
 * compounding NAV.
 */
import {
  Area,
  AreaChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import type { EquityPoint } from "@/lib/api/schemas";

interface DrawdownChartProps {
  points: EquityPoint[];
}

export function DrawdownChart({ points }: DrawdownChartProps) {
  if (points.length === 0) {
    return (
      <div className="p-4 text-sm text-gray-500">데이터가 없습니다.</div>
    );
  }

  return (
    <ResponsiveContainer width="100%" height={300}>
      <AreaChart data={points} margin={{ top: 8, right: 16, bottom: 0, left: 0 }}>
        <defs>
          <linearGradient id="ddGradient" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor="#ef4444" stopOpacity={0.4} />
            <stop offset="100%" stopColor="#ef4444" stopOpacity={0.05} />
          </linearGradient>
        </defs>
        <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
        <XAxis dataKey="time" tick={{ fontSize: 11 }} minTickGap={32} />
        <YAxis
          tickFormatter={(v: number) => `${(v * 100).toFixed(0)}%`}
          tick={{ fontSize: 11 }}
          domain={["auto", 0]}
        />
        <Tooltip
          formatter={(v: number) => `${(v * 100).toFixed(2)}%`}
          labelClassName="text-xs"
        />
        <Area
          type="monotone"
          dataKey="drawdown"
          stroke="#ef4444"
          strokeWidth={1.5}
          fill="url(#ddGradient)"
          isAnimationActive={false}
        />
      </AreaChart>
    </ResponsiveContainer>
  );
}
