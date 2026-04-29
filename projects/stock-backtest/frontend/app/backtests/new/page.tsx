"use client";

/**
 * /backtests/new — 백테스트 생성 화면 (TASK-092).
 *
 * 사용자 흐름:
 *   1. 전략(allocator) 드롭다운에서 선택 → params_schema 기반 자동 폼
 *      (StrategyParamsForm)
 *   2. universe 검색·다중 선택 (UniverseSelector)
 *   3. 기간(시작/종료) + base_currency(드롭다운, 디폴트 없음) + 초기 자본
 *   4. 리밸런싱 주기 (monthly 디폴트)
 *   5. "백테스트 실행" → POST /api/backtests → run_id 반환 시 결과
 *      페이지(`/backtests/{run_id}`, TASK-093)로 라우팅
 *
 * UI/UX 원칙:
 *   - 1 (JSON 노출 금지): 모든 필드 폼 입력. dict 파라미터(FixedWeight
 *     weights)는 임시 JSON placeholder — coder-report observation.
 *   - 2 (한국어 + trace_id): 에러 토스트에 trace_id 8자리 prefix 노출.
 *   - 5 (Zod 런타임 검증): BacktestCreate 페이로드는 client.ts 의
 *     fetchAndValidate 가 응답에 BacktestRunSchema 적용; 페이로드 자체는
 *     서버 pydantic 으로 검증되며 422 시 표준 에러 envelope.
 *   - 6 (점진적 노출): 화면 1개에서 카드 4개로 단계 분할 (전략 / universe
 *     / 기간·자본 / 액션) — 별도 마법사 화면 만들지 않음.
 */
import { useEffect, useMemo, useState } from "react";
import { useRouter } from "next/navigation";

import { api, ApiError } from "@/lib/api/client";
import type {
  BacktestCreate,
  RebalanceSchedule,
  StrategyDescriptor,
  StrategyListResponse,
} from "@/lib/api/schemas";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select } from "@/components/ui/select";
import { useToast } from "@/components/ui/toast";
import { ko } from "@/lib/i18n/ko";

import { StrategyParamsForm } from "@/components/backtest/StrategyParamsForm";
import {
  UniverseSelector,
  type UniverseAsset,
} from "@/components/backtest/UniverseSelector";
// TASK-094: 폼 제출 후 in-place 진행률 패널.
// /backtests/new 가 폼 모드 ↔ 진행 모드를 토글 — 별도 라우트 만들지 않음
// (UI/UX 원칙 6: 화면 3개 한도 — 카탈로그 / new / 결과).
import { ProgressPanel } from "@/components/backtest/ProgressPanel";
import { useBacktestPolling } from "@/hooks/useBacktestPolling";

// 디폴트 없음 (architecture.md L568) — placeholder option 으로 강제 선택.
const BASE_CURRENCY_OPTIONS: { value: string; label: string }[] = [
  { value: "", label: "선택하세요" },
  { value: "KRW", label: "KRW (원)" },
  { value: "USD", label: "USD (달러)" },
];

const REBALANCE_OPTIONS: { value: RebalanceSchedule; label: string }[] = [
  { value: "daily", label: "매일" },
  { value: "weekly", label: "매주" },
  { value: "monthly", label: "매월" },
  { value: "quarterly", label: "분기" },
  { value: "yearly", label: "매년" },
];

function todayIso(): string {
  return new Date().toISOString().slice(0, 10);
}

export default function NewBacktestPage() {
  const router = useRouter();
  const { toast } = useToast();

  const [strategies, setStrategies] = useState<StrategyListResponse>({
    allocators: [],
    filters: [],
  });
  const [strategiesLoading, setStrategiesLoading] = useState(true);

  const [allocatorName, setAllocatorName] = useState("");
  const [allocatorParams, setAllocatorParams] = useState<
    Record<string, unknown>
  >({});
  const [universe, setUniverse] = useState<UniverseAsset[]>([]);
  const [periodStart, setPeriodStart] = useState("2020-01-01");
  const [periodEnd, setPeriodEnd] = useState(todayIso());
  const [baseCurrency, setBaseCurrency] = useState("");
  const [initialCash, setInitialCash] = useState<number>(10_000_000);
  const [rebalanceSchedule, setRebalanceSchedule] =
    useState<RebalanceSchedule>("monthly");
  const [submitting, setSubmitting] = useState(false);

  // TASK-094: 폼 제출 직후 setSubmittedRunId(run.run_id) 로 in-place
  // 진행률 패널을 띄운다. null 이면 폼 모드 (기본).
  const [submittedRunId, setSubmittedRunId] = useState<number | null>(null);
  const polling = useBacktestPolling(submittedRunId);

  useEffect(() => {
    let cancelled = false;
    setStrategiesLoading(true);
    api
      .listStrategies()
      .then((res) => {
        if (cancelled) return;
        setStrategies(res);
      })
      .catch((e) => {
        if (cancelled) return;
        const err = e as ApiError;
        toast({
          title: ko.error.generic,
          description:
            err.message + (err.traceId ? ` (${err.traceId.slice(0, 8)})` : ""),
          variant: "destructive",
        });
      })
      .finally(() => {
        if (cancelled) return;
        setStrategiesLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, [toast]);

  const selectedAllocator: StrategyDescriptor | undefined = useMemo(
    () => strategies.allocators.find((a) => a.name === allocatorName),
    [strategies.allocators, allocatorName],
  );

  const canSubmit =
    !submitting &&
    allocatorName !== "" &&
    universe.length > 0 &&
    baseCurrency !== "" &&
    periodStart !== "" &&
    periodEnd !== "" &&
    Number.isFinite(initialCash) &&
    initialCash > 0;

  async function handleSubmit() {
    if (!canSubmit) {
      toast({
        title: "입력을 완성해주세요",
        description:
          "전략, universe(1개 이상), 기축통화, 기간, 초기 자본을 모두 입력해야 합니다.",
        variant: "destructive",
      });
      return;
    }

    const payload: BacktestCreate = {
      name: null,
      strategy: {
        allocator_name: allocatorName,
        allocator_params: allocatorParams,
        filter_configs: [],
        rebalance_schedule: rebalanceSchedule,
      },
      universe_asset_ids: universe.map((a) => a.asset_id),
      period_start: periodStart,
      period_end: periodEnd,
      base_currency: baseCurrency,
      initial_cash: { [baseCurrency]: initialCash },
    };

    setSubmitting(true);
    try {
      const run = await api.createBacktest(payload);
      toast({
        title: "백테스트가 시작되었습니다",
        description: `run_id=${run.run_id} · 진행률을 폴링합니다.`,
        variant: "success",
      });
      // TASK-094: 즉시 라우팅하지 않고 in-place 진행률 패널로 전환.
      // status='done' 시점에 ProgressPanel 이 자동으로 결과 화면으로
      // 라우팅한다.
      setSubmittedRunId(run.run_id);
    } catch (e) {
      const err = e as ApiError;
      toast({
        title: ko.error.generic,
        description:
          err.message + (err.traceId ? ` (${err.traceId.slice(0, 8)})` : ""),
        variant: "destructive",
      });
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <main className="min-h-screen bg-gray-50 p-8">
      <div className="mx-auto max-w-4xl space-y-6">
        <header>
          <h1 className="text-3xl font-bold text-gray-900">
            {ko.backtest.create}
          </h1>
          <p className="mt-1 text-sm text-gray-600">
            전략·universe·기간·기축통화를 선택해 백테스트를 실행합니다.
          </p>
        </header>

        {submittedRunId !== null ? (
          // TASK-094: 폼 제출 후 in-place 진행률 패널.
          // 결과 화면 (TASK-093) 으로의 라우팅은 ProgressPanel 내부에서
          // status='done' 시 수행한다.
          <ProgressPanel
            run={polling.run}
            loading={polling.loading}
            error={polling.error}
            onCancel={polling.cancelRun}
            onReset={() => setSubmittedRunId(null)}
          />
        ) : (
          <>
        <Card>
          <CardHeader>
            <CardTitle>{ko.backtest.selectStrategy}</CardTitle>
            <CardDescription>
              전략(allocator)을 고르고 파라미터를 입력하세요.
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <Label htmlFor="allocator">전략</Label>
              <Select
                id="allocator"
                value={allocatorName}
                onChange={(e) => {
                  setAllocatorName(e.target.value);
                  setAllocatorParams({});
                }}
                disabled={strategiesLoading}
              >
                <option value="">
                  {strategiesLoading
                    ? "전략 목록을 불러오는 중..."
                    : "선택하세요"}
                </option>
                {strategies.allocators.map((alloc) => (
                  <option key={alloc.name} value={alloc.name}>
                    {alloc.description ?? alloc.name}
                  </option>
                ))}
              </Select>
            </div>

            {selectedAllocator && (
              <div className="rounded border border-gray-200 bg-gray-50 p-4">
                <p className="mb-3 text-sm font-medium text-gray-700">
                  {selectedAllocator.name} 파라미터
                </p>
                <StrategyParamsForm
                  schema={selectedAllocator.params_schema}
                  value={allocatorParams}
                  onChange={setAllocatorParams}
                />
              </div>
            )}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>{ko.backtest.selectUniverse}</CardTitle>
            <CardDescription>
              자산 카탈로그에서 검색해 백테스트 universe 를 구성합니다.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <UniverseSelector value={universe} onChange={setUniverse} />
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>{ko.backtest.period} · 자본 · 리밸런싱</CardTitle>
            <CardDescription>
              기간과 기축통화, 초기 자본, 리밸런싱 주기를 지정합니다.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
              <div>
                <Label htmlFor="period_start">기간 시작</Label>
                <Input
                  id="period_start"
                  type="date"
                  value={periodStart}
                  onChange={(e) => setPeriodStart(e.target.value)}
                />
              </div>
              <div>
                <Label htmlFor="period_end">기간 종료</Label>
                <Input
                  id="period_end"
                  type="date"
                  value={periodEnd}
                  onChange={(e) => setPeriodEnd(e.target.value)}
                />
              </div>
              <div>
                <Label htmlFor="base_ccy">{ko.backtest.baseCurrency}</Label>
                <Select
                  id="base_ccy"
                  value={baseCurrency}
                  onChange={(e) => setBaseCurrency(e.target.value)}
                >
                  {BASE_CURRENCY_OPTIONS.map((opt) => (
                    <option key={opt.value} value={opt.value}>
                      {opt.label}
                    </option>
                  ))}
                </Select>
              </div>
              <div>
                <Label htmlFor="initial_cash">{ko.backtest.initialCash}</Label>
                <Input
                  id="initial_cash"
                  type="number"
                  min={0}
                  step={1}
                  value={Number.isFinite(initialCash) ? initialCash : ""}
                  onChange={(e) => {
                    const raw = e.target.value;
                    setInitialCash(raw === "" ? 0 : Number(raw));
                  }}
                />
                <p className="mt-1 text-xs text-gray-500">
                  기축통화 단위로 입력합니다.
                </p>
              </div>
              <div>
                <Label htmlFor="rebalance">리밸런싱 주기</Label>
                <Select
                  id="rebalance"
                  value={rebalanceSchedule}
                  onChange={(e) =>
                    setRebalanceSchedule(e.target.value as RebalanceSchedule)
                  }
                >
                  {REBALANCE_OPTIONS.map((opt) => (
                    <option key={opt.value} value={opt.value}>
                      {opt.label}
                    </option>
                  ))}
                </Select>
              </div>
            </div>
          </CardContent>
        </Card>

        <div className="flex justify-end gap-2">
          <Button variant="secondary" onClick={() => router.push("/")}>
            {ko.backtest.cancel}
          </Button>
          <Button onClick={() => void handleSubmit()} disabled={!canSubmit}>
            {submitting ? "실행 중..." : "백테스트 실행"}
          </Button>
        </div>
          </>
        )}
      </div>
    </main>
  );
}
