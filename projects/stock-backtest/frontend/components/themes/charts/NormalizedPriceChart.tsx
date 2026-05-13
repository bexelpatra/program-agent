"use client";

/**
 * NormalizedPriceChart — 테마 멤버 자산별 정규화 (rebase=100) 라인 차트.
 *
 * Phase 2.1 (TASK-308). 각 멤버 자산의 시계열을 base100 으로 맞춰 한
 * `LineChart` 안에서 다중 라인으로 비교. recharts 의 한계 (배열 데이터에
 * 동일 시간 축이 필요) 를 만족시키기 위해 외부에서 받은 members 데이터를
 * `{ time, "<asset_id>": value, ... }` 형태로 union/merge 한다.
 *
 * 색상 팔레트는 EquityChart 의 #2563eb (blue-600) 를 시작으로 한
 * tailwind 계열에서 6 색을 순환한다 — 7번째 자산부터는 같은 색이 재사용
 * 되지만, MVP 의 테마는 보통 3~5 종목 묶음이라 충분 (architecture.md V3
 * § "정규화 차트 사양").
 */
import {
  CartesianGrid,
  Legend,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import type { SeriesPoint } from "@/lib/api/types";

/** EquityChart 팔레트 + 5색 추가 — tailwind 계열에서 시인성 우수. */
export const SERIES_COLORS = [
  "#2563eb", // blue-600 (EquityChart 기준 색)
  "#dc2626", // red-600
  "#16a34a", // green-600
  "#ea580c", // orange-600
  "#7c3aed", // violet-600
  "#0891b2", // cyan-600
];

export interface NormalizedPriceChartProps {
  /**
   * 백엔드 ThemeChartResponse.members 형태 — 키는 asset_id (string),
   * 값은 SeriesPoint[] (time + 정규화 value). 빈 객체면 안내 메시지.
   */
  members: Record<string, SeriesPoint[]>;
  /** asset_id → 표시 라벨 (심볼/이름). 미지정 키는 raw asset_id 사용. */
  labels?: Record<string, string>;
  height?: number;
}

interface MergedRow {
  time: string;
  [assetKey: string]: string | number;
}

/**
 * members 를 recharts 가 소비할 수 있는 `[{time, "<asset_id>": value}, ...]`
 * 단일 배열로 union/merge. 한 시점에 일부 자산이 비어 있어도 (universe
 * 교집합 outside) recharts 가 자동으로 그 라인의 segment 를 끊는다.
 */
export function mergeMembers(
  members: Record<string, SeriesPoint[]>,
): MergedRow[] {
  const timeMap = new Map<string, MergedRow>();
  for (const [aid, points] of Object.entries(members)) {
    for (const p of points) {
      const row = timeMap.get(p.time) ?? { time: p.time };
      row[aid] = p.value;
      timeMap.set(p.time, row);
    }
  }
  return Array.from(timeMap.values()).sort((a, b) =>
    a.time.localeCompare(b.time),
  );
}

export function NormalizedPriceChart({
  members,
  labels = {},
  height = 320,
}: NormalizedPriceChartProps) {
  const assetKeys = Object.keys(members);
  if (assetKeys.length === 0) {
    return (
      <div className="p-4 text-sm text-gray-500">
        표시할 멤버 데이터가 없습니다.
      </div>
    );
  }
  const data = mergeMembers(members);
  if (data.length === 0) {
    return (
      <div className="p-4 text-sm text-gray-500">
        선택한 기간에 공통 데이터가 없습니다.
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
        <Tooltip
          formatter={(v: number, name: string) => [
            // 한국어 라벨 + 소수점 2자리
            `${v.toFixed(2)} (정규화)`,
            labels[name] ?? `자산 ${name}`,
          ]}
          labelFormatter={(label: string) => `날짜: ${label}`}
          labelClassName="text-xs"
        />
        <Legend
          formatter={(value: string) => labels[value] ?? `자산 ${value}`}
          wrapperStyle={{ fontSize: 11 }}
        />
        {assetKeys.map((aid, idx) => (
          <Line
            key={aid}
            type="monotone"
            dataKey={aid}
            name={aid}
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
