"use client";

/**
 * /backtests/[run_id] — 백테스트 결과 화면 (TASK-093).
 *
 * architecture.md V3 § "UI/UX 원칙 4" L685-688:
 *   "결과 화면 = 자본 곡선 + 낙폭 + 지표 테이블 + 연·월 수익률 히트맵
 *    + 거래 내역 테이블 (통화 그룹)."
 * Quant Lab CLAUDE.md §4: CAGR/MDD/Sharpe/Sortino/Calmar/승률 항상 노출.
 *
 * 진입 로직:
 *   1. GET /api/backtests/{run_id} → status 확인.
 *      - status='done' 일 때만 /result 호출 → 결과 렌더.
 *      - 'pending' / 'running' / 'cancelled' / 'failed' 면 안내 카드만
 *        보여 주고 (TASK-094 의 ProgressPanel 은 /backtests/new 전용)
 *        사용자에게 새로고침을 권한다.
 *   2. /result 호출이 ApiError 를 내면 toast(destructive) + trace_id
 *      8자리 prefix (UI/UX 원칙 2).
 *
 * 진행 중(`pending`/`running`) 인 run 은 일부러 폴링하지 않는다 — 결과
 * 화면은 "완료된 run 을 정독"하는 페이지다. 진행 모니터링은 새 백테스트
 * 페이지의 ProgressPanel(TASK-094) 책임이다.
 */
import { useEffect, useState } from "react";
import { useParams } from "next/navigation";

import { TradesTable } from "@/components/backtest/TradesTable";
import { MonthlyHeatmap } from "@/components/backtest/MonthlyHeatmap";
import { MetricsTable } from "@/components/backtest/MetricsTable";
import { EquityChart } from "@/components/backtest/EquityChart";
import { DrawdownChart } from "@/components/backtest/DrawdownChart";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { useToast } from "@/components/ui/toast";
import { ApiError, api } from "@/lib/api/client";
import { ko } from "@/lib/i18n/ko";
import type { BacktestRun, BacktestStatus } from "@/lib/api/schemas";
import type { BacktestResult } from "@/lib/api/types";

const STATUS_LABEL: Record<BacktestStatus, string> = {
  pending: ko.backtest.pending,
  running: ko.backtest.running,
  done: ko.backtest.done,
  failed: ko.backtest.failed,
  cancelled: ko.backtest.cancelled,
};

const STATUS_VARIANT: Record<
  BacktestStatus,
  "default" | "secondary" | "success" | "warning" | "destructive"
> = {
  pending: "secondary",
  running: "warning",
  done: "success",
  failed: "destructive",
  cancelled: "secondary",
};

function describeApiError(e: ApiError): string {
  if (!e.traceId) return e.message;
  return `${e.message} (${e.traceId.slice(0, 8)})`;
}

export default function BacktestResultPage() {
  const params = useParams<{ run_id: string }>();
  const runIdRaw = params?.run_id;
  const runId = Number(runIdRaw);

  const [run, setRun] = useState<BacktestRun | null>(null);
  const [result, setResult] = useState<BacktestResult | null>(null);
  const [logScale, setLogScale] = useState(false);
  const [loading, setLoading] = useState(true);
  const { toast } = useToast();

  useEffect(() => {
    if (!Number.isFinite(runId) || runId <= 0) {
      setLoading(false);
      return;
    }

    let cancelled = false;

    async function load() {
      try {
        // 1) status 확인 — 결과 endpoint 호출 전 게이트.
        const fetchedRun = await api.getBacktest(runId);
        if (cancelled) return;
        setRun(fetchedRun);

        if (fetchedRun.status === "failed") {
          // failed 일 때는 toast 로 사용자에게 즉시 알림.
          const errMsg =
            fetchedRun.error && typeof fetchedRun.error.message === "string"
              ? fetchedRun.error.message
              : "원인 불명";
          toast({
            title: ko.backtest.failed,
            description: errMsg,
            variant: "destructive",
          });
          return;
        }

        if (fetchedRun.status !== "done") {
          // pending / running / cancelled — 결과 없음.
          return;
        }

        // 2) done — 결과 fetch.
        const fetchedResult = await api.getBacktestResult(runId);
        if (cancelled) return;
        setResult(fetchedResult);
      } catch (e) {
        if (cancelled) return;
        if (e instanceof ApiError) {
          toast({
            title: ko.error.generic,
            description: describeApiError(e),
            variant: "destructive",
          });
        } else {
          toast({
            title: ko.error.generic,
            description: e instanceof Error ? e.message : String(e),
            variant: "destructive",
          });
        }
      } finally {
        if (!cancelled) setLoading(false);
      }
    }

    void load();

    return () => {
      cancelled = true;
    };
  }, [runId, toast]);

  if (!Number.isFinite(runId) || runId <= 0) {
    return (
      <main className="min-h-screen bg-gray-50 p-8">
        <div className="mx-auto max-w-2xl">
          <Card className="p-8 text-center text-sm text-gray-600">
            잘못된 백테스트 ID 입니다.
          </Card>
        </div>
      </main>
    );
  }

  if (loading) {
    return (
      <main className="min-h-screen bg-gray-50 p-8">
        <div className="mx-auto max-w-2xl">
          <Card className="p-8 text-center text-sm text-gray-500">
            로딩 중...
          </Card>
        </div>
      </main>
    );
  }

  if (!run) {
    return (
      <main className="min-h-screen bg-gray-50 p-8">
        <div className="mx-auto max-w-2xl">
          <Card className="p-8 text-center text-sm text-gray-600">
            백테스트 결과를 가져올 수 없습니다.
          </Card>
        </div>
      </main>
    );
  }

  const statusBadge = (
    <Badge variant={STATUS_VARIANT[run.status]}>
      {STATUS_LABEL[run.status]}
    </Badge>
  );

  // status !== 'done' 분기 — 안내 카드만 보여 준다.
  if (run.status !== "done" || !result) {
    return (
      <main className="min-h-screen bg-gray-50 p-8">
        <div className="mx-auto max-w-3xl space-y-6">
          <header className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold">
                백테스트 #{run.run_id}
              </h1>
              <p className="mt-1 text-sm text-gray-600">
                {run.strategy_name} · {run.period_start} ~ {run.period_end} ·{" "}
                {run.base_currency}
              </p>
            </div>
            {statusBadge}
          </header>
          <Card className="p-8 text-center text-sm text-gray-600">
            {run.status === "running" || run.status === "pending"
              ? "백테스트가 아직 실행 중입니다. 잠시 후 새로고침해 주세요."
              : run.status === "failed"
                ? "이 백테스트는 실패했습니다. 새로 실행해 주세요."
                : "이 백테스트는 취소되었습니다."}
          </Card>
        </div>
      </main>
    );
  }

  const monthly = result.metrics?.monthly_returns ?? {};
  const hasMonthly = Object.keys(monthly).length > 0;

  return (
    <main className="min-h-screen bg-gray-50 p-8">
      <div className="mx-auto max-w-7xl space-y-6">
        <header className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold">
              백테스트 #{result.run.run_id}
              {result.run.name ? (
                <span className="ml-2 text-base font-normal text-gray-600">
                  {result.run.name}
                </span>
              ) : null}
            </h1>
            <p className="mt-1 text-sm text-gray-600">
              {result.run.strategy_name} · {result.run.period_start} ~{" "}
              {result.run.period_end} · {result.run.base_currency}
            </p>
          </div>
          {statusBadge}
        </header>

        <div className="grid gap-6 md:grid-cols-2">
          <Card className="p-4">
            <div className="mb-3 flex items-center justify-between">
              <h2 className="text-lg font-semibold">자본 곡선</h2>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setLogScale((v) => !v)}
                aria-pressed={logScale}
              >
                {logScale ? "선형" : "로그"}
              </Button>
            </div>
            <EquityChart points={result.equity_curve} logScale={logScale} />
          </Card>
          <Card className="p-4">
            <h2 className="mb-3 text-lg font-semibold">낙폭 (Drawdown)</h2>
            <DrawdownChart points={result.equity_curve} />
          </Card>
        </div>

        {result.metrics ? (
          <Card className="p-4">
            <h2 className="mb-3 text-lg font-semibold">성과 지표</h2>
            <MetricsTable metrics={result.metrics} />
          </Card>
        ) : (
          <Card className="p-4 text-sm text-gray-500">
            성과 지표를 계산하지 못했습니다 (체결된 거래가 없을 수 있음).
          </Card>
        )}

        {hasMonthly ? (
          <Card className="p-4">
            <h2 className="mb-3 text-lg font-semibold">월별 수익률</h2>
            <MonthlyHeatmap monthly={monthly} />
          </Card>
        ) : null}

        <Card className="p-0">
          <h2 className="border-b p-4 text-lg font-semibold">
            거래 내역 ({result.trades.length}건)
          </h2>
          <TradesTable trades={result.trades} />
        </Card>
      </div>
    </main>
  );
}
