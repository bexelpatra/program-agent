/**
 * MonthlyHeatmap — 연 × 월 수익률 격자.
 *
 * `monthly` 키는 "YYYY-MM". 데이터가 없는 셀은 회색 dash; 데이터가
 * 있으면 부호 + 절대값 강도(|v| × 5, 최대 1)에 따라 녹/적 알파.
 *
 * architecture.md V3 § UI/UX 원칙 4 — "연·월 수익률 히트맵". 사용자가
 * 한 눈에 어느 해 / 어느 달이 강했고 약했는지 스캔하기 위한 패널.
 */
interface MonthlyHeatmapProps {
  monthly: Record<string, number>;
}

const MONTHS = Array.from({ length: 12 }, (_, i) => i + 1);

function colorFor(value: number): string {
  const intensity = Math.min(Math.abs(value) * 5, 1);
  if (value > 0) return `rgba(34, 197, 94, ${intensity})`;
  if (value < 0) return `rgba(239, 68, 68, ${intensity})`;
  return "transparent";
}

export function MonthlyHeatmap({ monthly }: MonthlyHeatmapProps) {
  const entries = Object.entries(monthly).sort(([a], [b]) => a.localeCompare(b));
  if (entries.length === 0) {
    return (
      <div className="p-2 text-sm text-gray-500">월별 데이터가 없습니다.</div>
    );
  }
  const years = Array.from(new Set(entries.map(([k]) => k.slice(0, 4))));

  return (
    <div className="overflow-x-auto">
      <table className="w-full text-xs border-collapse">
        <thead>
          <tr className="text-gray-600">
            <th className="p-1 text-left font-medium">연도</th>
            {MONTHS.map((m) => (
              <th key={m} className="p-1 text-center font-medium">
                {m}월
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {years.map((year) => (
            <tr key={year}>
              <td className="p-1 font-mono text-gray-700">{year}</td>
              {MONTHS.map((m) => {
                const key = `${year}-${String(m).padStart(2, "0")}`;
                const value = monthly[key];
                if (value === undefined) {
                  return (
                    <td
                      key={m}
                      className="p-1 text-center text-gray-300"
                    >
                      -
                    </td>
                  );
                }
                return (
                  <td
                    key={m}
                    className="p-1 text-center font-mono"
                    style={{ backgroundColor: colorFor(value) }}
                    title={`${key}: ${(value * 100).toFixed(2)}%`}
                  >
                    {(value * 100).toFixed(1)}%
                  </td>
                );
              })}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
