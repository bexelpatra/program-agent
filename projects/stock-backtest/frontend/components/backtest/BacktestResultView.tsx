"use client";

/**
 * BacktestResultView — 백테스트 결과 시각화 통합 컴포넌트 (TASK-237).
 *
 * 추출 배경:
 *   `/backtests/new/page.tsx` 의 `BacktestResultPanel` (인플레이스 결과
 *   패널) 과 `/backtests/[run_id]/page.tsx` 의 인라인 JSX 가 동일한 5개
 *   시각화 컴포넌트 (EquityChart / DrawdownChart / MetricsTable /
 *   MonthlyHeatmap / TradesTable) 를 거의 같은 방식으로 렌더하고 있었다.
 *   유일한 차이는 레이아웃:
 *     - new/page.tsx: 우측 패널이 lg breakpoint 에서 단일 컬럼으로
 *       sticky 폼과 병치되므로, 결과는 그 안에서 다시 세로 stack.
 *     - [run_id]/page.tsx: 페이지 전체 폭(max-w-7xl) 을 사용하므로
 *       자본곡선/낙폭을 `md:grid-cols-2` 로 좌우 병치.
 *
 * `layout` prop 으로 두 배치를 선택한다 — 결과 컴포넌트 5개 자체와
 * 모든 주변 카드/제목/로그스케일 토글은 동일.
 *
 * Quant Lab CLAUDE.md §4 / architecture.md V3 § "UI/UX 원칙 4":
 *   결과 화면 = 자본 곡선 + 낙폭 + 지표 테이블 + 연·월 수익률 히트맵 +
 *   거래 내역 테이블 (통화 그룹). 이 5개 블록은 어느 진입 경로에서도
 *   동일하게 노출돼야 한다 — 본 컴포넌트가 그 보장 지점이다.
 */
import type { BacktestResult } from "@/lib/api/types";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";

import { DrawdownChart } from "@/components/backtest/DrawdownChart";
import { EquityChart } from "@/components/backtest/EquityChart";
import { MetricsTable } from "@/components/backtest/MetricsTable";
import { MonthlyHeatmap } from "@/components/backtest/MonthlyHeatmap";
import { TradesTable } from "@/components/backtest/TradesTable";

export interface BacktestResultViewProps {
  result: BacktestResult;
  logScale: boolean;
  onLogScaleChange: (next: boolean) => void;
  /**
   * - `compact`: new/page.tsx 우측 패널 — 모든 카드를 세로로 stack.
   * - `full`: [run_id]/page.tsx 전용 페이지 — 자본곡선/낙폭을
   *   `md:grid-cols-2` 로 병치, 나머지(지표/월별/거래)는 단일 컬럼.
   *
   * default: `full` (전용 페이지 진입이 더 정형적인 사용 시나리오).
   */
  layout?: "compact" | "full";
}

export function BacktestResultView({
  result,
  logScale,
  onLogScaleChange,
  layout = "full",
}: BacktestResultViewProps) {
  const monthly = result.metrics?.monthly_returns ?? {};
  const hasMonthly = Object.keys(monthly).length > 0;

  const equityCard = (
    <Card className="p-4">
      <div className="mb-3 flex items-center justify-between">
        <h2 className="text-lg font-semibold">자본 곡선</h2>
        <Button
          variant="ghost"
          size="sm"
          onClick={() => onLogScaleChange(!logScale)}
          aria-pressed={logScale}
        >
          {logScale ? "선형" : "로그"}
        </Button>
      </div>
      <EquityChart points={result.equity_curve} logScale={logScale} />
    </Card>
  );

  const drawdownCard = (
    <Card className="p-4">
      <h2 className="mb-3 text-lg font-semibold">낙폭 (Drawdown)</h2>
      <DrawdownChart points={result.equity_curve} />
    </Card>
  );

  const metricsCard = result.metrics ? (
    <Card className="p-4">
      <h2 className="mb-3 text-lg font-semibold">성과 지표</h2>
      <MetricsTable metrics={result.metrics} />
    </Card>
  ) : (
    <Card className="p-4 text-sm text-gray-500">
      성과 지표를 계산하지 못했습니다 (체결된 거래가 없을 수 있음).
    </Card>
  );

  const monthlyCard = hasMonthly ? (
    <Card className="p-4">
      <h2 className="mb-3 text-lg font-semibold">월별 수익률</h2>
      <MonthlyHeatmap monthly={monthly} />
    </Card>
  ) : null;

  const tradesCard = (
    <Card className="p-0">
      <h2 className="border-b p-4 text-lg font-semibold">
        거래 내역 ({result.trades.length}건)
      </h2>
      <TradesTable trades={result.trades} />
    </Card>
  );

  if (layout === "compact") {
    return (
      <div className="space-y-6">
        {equityCard}
        {drawdownCard}
        {metricsCard}
        {monthlyCard}
        {tradesCard}
      </div>
    );
  }

  // layout === "full" — 자본곡선/낙폭만 좌우 병치, 나머지 단일 컬럼.
  return (
    <div className="space-y-6">
      <div className="grid gap-6 md:grid-cols-2">
        {equityCard}
        {drawdownCard}
      </div>
      {metricsCard}
      {monthlyCard}
      {tradesCard}
    </div>
  );
}
