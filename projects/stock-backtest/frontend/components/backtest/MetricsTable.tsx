/**
 * MetricsTable — six headline performance metrics.
 *
 * Quant Lab CLAUDE.md §4: 결과 지표는 항상 CAGR/MDD/Sharpe/Sortino/
 * Calmar/승률을 계산. Labels come from `lib/i18n/ko.ts` (한자 병기 포함:
 * "샤프지수 (Sharpe)" 등) so a future locale switch only touches the
 * catalogue.
 *
 * Formatting:
 *  · 비율류 (CAGR, MDD, 승률) → percent, 2 decimal places
 *  · 무차원 (Sharpe, Sortino, Calmar) → 2 decimal places
 *
 * 음수 / 양수 색상 강조 없음 — 의도적. Sharpe 등은 부호로 단순 좋음/
 * 나쁨을 가르기 어렵고 (e.g. -0.1 vs +0.05 둘 다 의미 없을 수 있음),
 * 사용자에게 숫자만 명확히 보여 주고 해석은 맡긴다.
 */
import { ko } from "@/lib/i18n/ko";

/**
 * Local prop shape — kept loose on `annual_returns` / `monthly_returns`
 * (optional Record) because the upstream `BacktestResult` type is
 * inferred via `z.ZodSchema<T>` which collapses input/output and treats
 * the `.default({})` fields as optional. The runtime always has them
 * (Zod fills defaults on parse), but TS sees them as possibly undefined
 * at the call site. Accept that here rather than casting at every call.
 */
interface MetricsTableProps {
  metrics: {
    cagr: number;
    mdd: number;
    sharpe: number;
    sortino: number;
    calmar: number;
    win_rate: number;
    annual_returns?: Record<string, number>;
    monthly_returns?: Record<string, number>;
  };
}

function fmtPct(value: number): string {
  return `${(value * 100).toFixed(2)}%`;
}

function fmtNum(value: number, digits = 2): string {
  return value.toFixed(digits);
}

export function MetricsTable({ metrics }: MetricsTableProps) {
  const rows: Array<[string, string]> = [
    [ko.metric.cagr, fmtPct(metrics.cagr)],
    [ko.metric.mdd, fmtPct(metrics.mdd)],
    [ko.metric.sharpe, fmtNum(metrics.sharpe)],
    [ko.metric.sortino, fmtNum(metrics.sortino)],
    [ko.metric.calmar, fmtNum(metrics.calmar)],
    [ko.metric.winRate, fmtPct(metrics.win_rate)],
  ];

  return (
    <div className="overflow-x-auto">
      <table className="w-full text-sm">
        <tbody>
          {rows.map(([label, value]) => (
            <tr key={label} className="border-b last:border-0">
              <td className="p-2 text-gray-600">{label}</td>
              <td className="p-2 text-right font-mono font-semibold">
                {value}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
