"use client";

/**
 * /backtests/new — 백테스트 생성 화면 (TASK-092 → TASK-200/201 통합).
 *
 * 사용자 흐름:
 *   1. 전략(allocator) 드롭다운에서 선택 → params_schema 기반 자동 폼
 *      (StrategyParamsForm). dict 파라미터(weights 등)는 부모 카드의
 *      AssetWeightMap 위젯으로 표시.
 *   2. universe 검색·다중 선택 (UniverseSelector)
 *   3. universe 가 1개 이상이고 allocator 에 dict 파라미터(weights)가
 *      있으면 AssetWeightMap 카드 노출.
 *   4. signal filters[] 구성 (FilterConfigBuilder, AND 결합).
 *   5. 기간(시작/종료) + base_currency(드롭다운, 디폴트 없음) + 초기 자본
 *   6. 리밸런싱 주기 (monthly 디폴트)
 *   7. "백테스트 실행" → POST /api/backtests → run_id 반환 시 결과
 *      페이지(`/backtests/{run_id}`, TASK-093)로 라우팅
 *
 * UI/UX 원칙:
 *   - 1 (JSON 노출 금지): 모든 dict/array 파라미터는 전용 위젯
 *     (AssetWeightMap / FilterConfigBuilder). raw JSON-string 입력 영구 제거.
 *   - 2 (한국어 + trace_id): 에러 토스트에 trace_id 8자리 prefix 노출.
 *   - 5 (Zod 런타임 검증): BacktestCreate 페이로드는 client.ts 의
 *     fetchAndValidate 가 응답에 BacktestRunSchema 적용; 페이로드 자체는
 *     서버 pydantic 으로 검증되며 422 시 표준 에러 envelope.
 *   - 6 (점진적 노출): 화면 1개에서 카드 다단으로 단계 분할 — 별도 마법사
 *     화면 만들지 않음.
 */
import { useEffect, useMemo, useState } from "react";
import { useRouter } from "next/navigation";

import { api, ApiError } from "@/lib/api/client";
import type {
  BacktestCreate,
  FilterConfig,
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

import { AssetWeightMap } from "@/components/backtest/AssetWeightMap";
import { FilterConfigBuilder } from "@/components/backtest/FilterConfigBuilder";
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

/**
 * allocator params_schema 의 top-level properties 중 type 이 object 인
 * 키를 모두 반환. FixedWeight 의 `weights` 처럼 dict 파라미터를 식별해
 * AssetWeightMap 위젯을 노출할지 판단한다.
 */
function findObjectParamKeys(
  descriptor: StrategyDescriptor | undefined,
): string[] {
  if (!descriptor) return [];
  const props = (descriptor.params_schema?.properties ?? {}) as Record<
    string,
    { type?: string }
  >;
  return Object.entries(props)
    .filter(([, def]) => def?.type === "object")
    .map(([key]) => key);
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
  const [filterConfigs, setFilterConfigs] = useState<FilterConfig[]>([]);
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

  // TASK-204: universe 자산별 최근 close 가격(native currency) prefetch.
  // AssetWeightMap 의 매수 불가 경고 평가에 사용. 키는 asset_id.
  // universe 변경 시 새로 등장한 자산만 추가 fetch (이미 알고 있는 자산은
  // 그대로 유지 — 가격 변동 가능성은 있으나 사전 경고용 정확도로 충분).
  const [latestPrices, setLatestPrices] = useState<Record<number, number>>({});
  useEffect(() => {
    let cancelled = false;
    const missing = universe.filter((a) => latestPrices[a.asset_id] === undefined);
    if (missing.length === 0) return;
    void Promise.all(
      missing.map((a) =>
        api
          .getAssetLatestPrice(a.asset_id)
          .then((price) => ({ id: a.asset_id, price }))
          .catch(() => ({ id: a.asset_id, price: null as number | null })),
      ),
    ).then((results) => {
      if (cancelled) return;
      setLatestPrices((prev) => {
        const next = { ...prev };
        for (const { id, price } of results) {
          if (price !== null) next[id] = price;
        }
        return next;
      });
    });
    return () => {
      cancelled = true;
    };
    // latestPrices 가 의존성에 있으면 setState 후 재실행 → 무한루프.
    // missing 계산용으로만 사용하고 의존성에서 제외 (eslint disable).
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [universe]);

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

  const objectParamKeys = useMemo(
    () => findObjectParamKeys(selectedAllocator),
    [selectedAllocator],
  );

  const weightParamKey = objectParamKeys[0]; // MVP: FixedWeight.weights 1개

  // universe 변경 시 allocator weights 의 누락 asset_id 는 0 으로 추가,
  // 제거된 asset_id 는 삭제. 다른 dict 키는 그대로 유지.
  useEffect(() => {
    if (!weightParamKey) return;
    const current = allocatorParams[weightParamKey];
    const allowedIds = new Set(universe.map((a) => a.asset_id));
    const next: Record<number, number> = {};
    if (current && typeof current === "object" && !Array.isArray(current)) {
      for (const [k, v] of Object.entries(current as Record<string, unknown>)) {
        const id = Number(k);
        if (allowedIds.has(id) && typeof v === "number") {
          next[id] = v;
        }
      }
    }
    universe.forEach((a) => {
      if (next[a.asset_id] === undefined) next[a.asset_id] = 0;
    });
    // 변경 감지 — 동일하면 setState 호출하지 않아 무한루프 방지.
    const same =
      current &&
      typeof current === "object" &&
      !Array.isArray(current) &&
      Object.keys(current as object).length === Object.keys(next).length &&
      Object.entries(next).every(
        ([k, v]) => (current as Record<string, unknown>)[k] === v,
      );
    if (!same) {
      setAllocatorParams((prev) => ({ ...prev, [weightParamKey]: next }));
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [universe, weightParamKey]);

  const weightsTotal = useMemo(() => {
    if (!weightParamKey) return 0;
    const w = allocatorParams[weightParamKey];
    if (!w || typeof w !== "object" || Array.isArray(w)) return 0;
    return Object.values(w as Record<string, number>).reduce(
      (s, v) => s + (typeof v === "number" ? v : 0),
      0,
    );
  }, [allocatorParams, weightParamKey]);

  const canSubmit =
    !submitting &&
    allocatorName !== "" &&
    universe.length > 0 &&
    baseCurrency !== "" &&
    periodStart !== "" &&
    periodEnd !== "" &&
    Number.isFinite(initialCash) &&
    initialCash > 0 &&
    // weights 가 있는 allocator 면 합계 > 0 강제 (전부 0 이면 backend
    // FixedWeightParams._validate_weights 의 "weights total must be
    // positive" 에 걸린다 — 클라에서 미리 차단해 422 전에 안내).
    (!weightParamKey || weightsTotal > 0);

  async function handleSubmit() {
    if (!canSubmit) {
      const why = weightParamKey && weightsTotal === 0
        ? "자산별 비중이 모두 0 입니다. AssetWeightMap 의 \"균등 분배\" 버튼을 누르거나 슬라이더를 조정하세요."
        : "전략, universe(1개 이상), 기축통화, 기간, 초기 자본을 모두 입력해야 합니다.";
      toast({
        title: "입력을 완성해주세요",
        description: why,
        variant: "destructive",
      });
      return;
    }

    const payload: BacktestCreate = {
      name: null,
      strategy: {
        allocator_name: allocatorName,
        allocator_params: allocatorParams,
        filter_configs: filterConfigs,
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

        {weightParamKey && (
          <Card>
            <CardHeader>
              <CardTitle>자산별 비중</CardTitle>
              <CardDescription>
                선택된 universe 자산별로 목표 비중(%)을 슬라이더로 입력합니다.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <AssetWeightMap
                universe={universe}
                value={
                  (allocatorParams[weightParamKey] as
                    | Record<number, number>
                    | undefined) ?? {}
                }
                onChange={(next) =>
                  setAllocatorParams((prev) => ({
                    ...prev,
                    [weightParamKey]: next,
                  }))
                }
                latestPrices={latestPrices}
                initialCash={initialCash}
                baseCurrency={baseCurrency || undefined}
              />
            </CardContent>
          </Card>
        )}

        <Card>
          <CardHeader>
            <CardTitle>시그널 필터</CardTitle>
            <CardDescription>
              선택사항. 보유 자격 필터를 추가하면 모든 필터가 AND 로
              결합되어 적용됩니다.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <FilterConfigBuilder
              availableFilters={strategies.filters}
              value={filterConfigs}
              onChange={setFilterConfigs}
            />
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
