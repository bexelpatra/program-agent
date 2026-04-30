"use client";

/**
 * /backtests/new — 백테스트 생성 화면 (TASK-092 → TASK-200/201 → TASK-218).
 *
 * TASK-218 (인플레이스 결과 표시):
 *   - URL 변경 없이 같은 페이지에서 폼 → 진행률 → 결과 까지 모두 표시한다.
 *     기존에는 status='done' 시 `/backtests/[run_id]` 로 router.push 했지만,
 *     사용자가 폼 입력값을 잃지 않도록 결과를 우측 패널에 in-place 렌더한다.
 *   - 폼 입력값은 useFormPersistence 로 localStorage 에 저장되며, 새로고침
 *     후에도 복원된다 (키: backtest:last_form_state:v1).
 *   - 레이아웃: lg breakpoint 이상 = 좌(폼 sticky) + 우(상태/결과). lg 미만
 *     = 단일 컬럼 stacked.
 *
 * 기존 동작 (회귀 0):
 *   - 이력에서 결과 다시 보기는 `/backtests/[run_id]` 페이지를 그대로 사용.
 *   - UI/UX 원칙 1 (JSON 노출 금지) — AssetWeightMap / FilterConfigBuilder 유지.
 *   - UI/UX 원칙 5 (Zod 런타임 검증) — fetchAndValidate 유지.
 *   - UI/UX 원칙 6 (점진적 노출) — 화면 수 그대로 (카탈로그 / new / 결과).
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

// `BacktestResult` 의 `z.infer` 결과와 client 메서드의 실제 반환 타입이
// nominal 으로 갈라지는 문제를 회피 (자세한 설명은 /backtests/[run_id]/
// page.tsx L41-45 동일 패턴).
type BacktestResult = Awaited<ReturnType<typeof api.getBacktestResult>>;
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
import { DrawdownChart } from "@/components/backtest/DrawdownChart";
import { EquityChart } from "@/components/backtest/EquityChart";
import { FilterConfigBuilder } from "@/components/backtest/FilterConfigBuilder";
import { MetricsTable } from "@/components/backtest/MetricsTable";
import { MonthlyHeatmap } from "@/components/backtest/MonthlyHeatmap";
import { ProgressPanel } from "@/components/backtest/ProgressPanel";
import { StrategyParamsForm } from "@/components/backtest/StrategyParamsForm";
import { TradesTable } from "@/components/backtest/TradesTable";
import {
  UniverseSelector,
  type UniverseAsset,
} from "@/components/backtest/UniverseSelector";
import { useBacktestPolling } from "@/hooks/useBacktestPolling";
import { useFormPersistence } from "@/hooks/useFormPersistence";

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
  { value: "semi_annual", label: "반기" },
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

// ─── 폼 상태 영속화 (TASK-218) ──────────────────────────────────────────
//
// universe_asset_ids 만 직렬화하고 Asset entity (symbol/name/market 등) 는
// 저장하지 않는다. 카탈로그가 변경되면 이름/시장 등은 stale 가능하므로
// 복원 시 asset_id 로 다시 조회한다 (UniverseSelector 가 hydrate 책임).

interface PersistedFormState {
  universe_asset_ids: number[];
  allocator_name: string;
  allocator_params: Record<string, unknown>;
  filter_configs: FilterConfig[];
  rebalance_schedule: RebalanceSchedule;
  period_start: string;
  period_end: string;
  base_currency: string;
  initial_cash: Record<string, number>;
}

const FORM_STORAGE_KEY = "backtest:last_form_state:v1";
const FORM_STATE_VERSION = 1;

function defaultFormState(): PersistedFormState {
  return {
    universe_asset_ids: [],
    allocator_name: "",
    allocator_params: {},
    filter_configs: [],
    rebalance_schedule: "monthly",
    period_start: "2020-01-01",
    period_end: todayIso(),
    base_currency: "",
    initial_cash: {},
  };
}

export default function NewBacktestPage() {
  const router = useRouter();
  const { toast } = useToast();

  // 폼 상태는 9 필드 묶음 단일 object 로 — useFormPersistence 가 한 번에
  // 직렬화. 개별 setter 헬퍼로 setForm((prev) => { ...prev, key: v }) 패턴.
  const [form, setForm, formHydrated] = useFormPersistence<PersistedFormState>({
    storageKey: FORM_STORAGE_KEY,
    initialValue: defaultFormState(),
    version: FORM_STATE_VERSION,
  });

  const setField = <K extends keyof PersistedFormState>(
    key: K,
    value: PersistedFormState[K],
  ) => {
    setForm((prev) => ({ ...prev, [key]: value }));
  };

  // universe 자산 entity 는 영속하지 않고, asset_id 배열만 유지 → 마운트 시
  // /api/assets/{id} 로 다시 조회해 entity 형태로 hydrate.
  const [universe, setUniverse] = useState<UniverseAsset[]>([]);
  useEffect(() => {
    if (!formHydrated) return;
    const ids = form.universe_asset_ids;
    if (ids.length === 0) {
      setUniverse((prev) => (prev.length === 0 ? prev : []));
      return;
    }
    // 이미 동일 set 이면 skip (sticky form 변경 시 무한루프 방지).
    const currentIds = universe.map((a) => a.asset_id).sort();
    const wantIds = [...ids].sort();
    if (
      currentIds.length === wantIds.length &&
      currentIds.every((v, i) => v === wantIds[i])
    ) {
      return;
    }
    let cancelled = false;
    void Promise.all(ids.map((id) => api.getAsset(id).catch(() => null))).then(
      (results) => {
        if (cancelled) return;
        const hydrated = results.filter(
          (a): a is UniverseAsset => a !== null,
        );
        setUniverse(hydrated);
      },
    );
    return () => {
      cancelled = true;
    };
    // form.universe_asset_ids 만 의존성. universe 는 비교용으로만 사용.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [form.universe_asset_ids, formHydrated]);

  // UniverseSelector 가 entity 단위 onChange — asset_id 를 form 에 동기화.
  const handleUniverseChange = (next: UniverseAsset[]) => {
    setUniverse(next);
    setField(
      "universe_asset_ids",
      next.map((a) => a.asset_id),
    );
  };

  const [strategies, setStrategies] = useState<StrategyListResponse>({
    allocators: [],
    filters: [],
  });
  const [strategiesLoading, setStrategiesLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);

  // 인플레이스 진행률 / 결과: submittedRunId 가 있으면 우측 패널에서
  // ProgressPanel 폴링 → done 시 BacktestResult fetch 후 결과 컴포넌트 렌더.
  const [submittedRunId, setSubmittedRunId] = useState<number | null>(null);
  const polling = useBacktestPolling(submittedRunId);
  const [result, setResult] = useState<BacktestResult | null>(null);
  const [resultLoading, setResultLoading] = useState(false);
  const [logScale, setLogScale] = useState(false);

  // status='done' 진입 시 /result 1회 fetch.
  useEffect(() => {
    if (polling.run?.status !== "done") {
      // 새 run 으로 전환되면 직전 결과 클리어.
      if (result !== null) setResult(null);
      return;
    }
    if (result?.run.run_id === polling.run.run_id) return; // 이미 fetch 됨
    let cancelled = false;
    setResultLoading(true);
    api
      .getBacktestResult(polling.run.run_id)
      .then((r) => {
        if (cancelled) return;
        setResult(r);
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
        if (!cancelled) setResultLoading(false);
      });
    return () => {
      cancelled = true;
    };
    // result 의존성 회피 — 새 run 진입 시 위 분기 (result !== null) 가 클리어.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [polling.run?.status, polling.run?.run_id, toast]);

  // TASK-204: universe 자산별 최근 close 가격(native currency) prefetch.
  // AssetWeightMap 의 매수 불가 경고 평가에 사용. 키는 asset_id.
  // universe 변경 시 새로 등장한 자산만 추가 fetch (이미 알고 있는 자산은
  // 그대로 유지 — 가격 변동 가능성은 있으나 사전 경고용 정확도로 충분).
  const [latestPrices, setLatestPrices] = useState<Record<number, number>>({});
  useEffect(() => {
    let cancelled = false;
    const missing = universe.filter(
      (a) => latestPrices[a.asset_id] === undefined,
    );
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
    () => strategies.allocators.find((a) => a.name === form.allocator_name),
    [strategies.allocators, form.allocator_name],
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
    const current = form.allocator_params[weightParamKey];
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
      setField("allocator_params", {
        ...form.allocator_params,
        [weightParamKey]: next,
      });
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [universe, weightParamKey]);

  const weightsTotal = useMemo(() => {
    if (!weightParamKey) return 0;
    const w = form.allocator_params[weightParamKey];
    if (!w || typeof w !== "object" || Array.isArray(w)) return 0;
    return Object.values(w as Record<string, number>).reduce(
      (s, v) => s + (typeof v === "number" ? v : 0),
      0,
    );
  }, [form.allocator_params, weightParamKey]);

  const canSubmit =
    !submitting &&
    form.allocator_name !== "" &&
    universe.length > 0 &&
    form.base_currency !== "" &&
    form.period_start !== "" &&
    form.period_end !== "" &&
    Number.isFinite(form.initial_cash[form.base_currency]) &&
    (form.initial_cash[form.base_currency] ?? 0) > 0 &&
    // weights 가 있는 allocator 면 합계 > 0 강제 (전부 0 이면 backend
    // FixedWeightParams._validate_weights 의 "weights total must be
    // positive" 에 걸린다 — 클라에서 미리 차단해 422 전에 안내).
    (!weightParamKey || weightsTotal > 0);

  async function handleSubmit() {
    if (!canSubmit) {
      const why =
        weightParamKey && weightsTotal === 0
          ? '자산별 비중이 모두 0 입니다. AssetWeightMap 의 "균등 분배" 버튼을 누르거나 슬라이더를 조정하세요.'
          : "전략, universe(1개 이상), 기축통화, 기간, 초기 자본을 모두 입력해야 합니다.";
      toast({
        title: "입력을 완성해주세요",
        description: why,
        variant: "destructive",
      });
      return;
    }

    const cashAmount = form.initial_cash[form.base_currency] ?? 0;
    const payload: BacktestCreate = {
      name: null,
      strategy: {
        allocator_name: form.allocator_name,
        allocator_params: form.allocator_params,
        filter_configs: form.filter_configs,
        rebalance_schedule: form.rebalance_schedule,
      },
      universe_asset_ids: universe.map((a) => a.asset_id),
      period_start: form.period_start,
      period_end: form.period_end,
      base_currency: form.base_currency,
      initial_cash: { [form.base_currency]: cashAmount },
    };

    setSubmitting(true);
    setResult(null);
    try {
      const run = await api.createBacktest(payload);
      toast({
        title: "백테스트가 시작되었습니다",
        description: `run_id=${run.run_id} · 진행률을 폴링합니다.`,
        variant: "success",
      });
      // TASK-218: router.push 하지 않는다. 같은 페이지 우측 패널에서
      // ProgressPanel → 결과 컴포넌트로 in-place 전환.
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

  const initialCashForBase = form.base_currency
    ? (form.initial_cash[form.base_currency] ?? 0)
    : 0;

  function setInitialCash(amount: number) {
    if (!form.base_currency) return;
    setField("initial_cash", { ...form.initial_cash, [form.base_currency]: amount });
  }

  return (
    <main className="min-h-screen bg-gray-50 p-4 md:p-8">
      <div className="mx-auto max-w-7xl space-y-6">
        <header className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">
              {ko.backtest.create}
            </h1>
            <p className="mt-1 text-sm text-gray-600">
              전략·universe·기간·기축통화를 선택해 백테스트를 실행합니다.
            </p>
          </div>
        </header>

        <div className="grid gap-6 lg:grid-cols-2">
          {/* 좌: 폼 (lg 이상에서 sticky) */}
          <div className="lg:sticky lg:top-4 lg:self-start lg:max-h-[calc(100vh-2rem)] lg:overflow-y-auto lg:pr-2">
            <div className="space-y-6">
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
                      value={form.allocator_name}
                      onChange={(e) => {
                        setForm((prev) => ({
                          ...prev,
                          allocator_name: e.target.value,
                          allocator_params: {},
                        }));
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
                        value={form.allocator_params}
                        onChange={(next) => setField("allocator_params", next)}
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
                  <UniverseSelector
                    value={universe}
                    onChange={handleUniverseChange}
                  />
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
                        (form.allocator_params[weightParamKey] as
                          | Record<number, number>
                          | undefined) ?? {}
                      }
                      onChange={(next) =>
                        setField("allocator_params", {
                          ...form.allocator_params,
                          [weightParamKey]: next,
                        })
                      }
                      latestPrices={latestPrices}
                      initialCash={initialCashForBase}
                      baseCurrency={form.base_currency || undefined}
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
                    value={form.filter_configs}
                    onChange={(next) => setField("filter_configs", next)}
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
                        value={form.period_start}
                        onChange={(e) => setField("period_start", e.target.value)}
                      />
                    </div>
                    <div>
                      <Label htmlFor="period_end">기간 종료</Label>
                      <Input
                        id="period_end"
                        type="date"
                        value={form.period_end}
                        onChange={(e) => setField("period_end", e.target.value)}
                      />
                    </div>
                    <div>
                      <Label htmlFor="base_ccy">{ko.backtest.baseCurrency}</Label>
                      <Select
                        id="base_ccy"
                        value={form.base_currency}
                        onChange={(e) => setField("base_currency", e.target.value)}
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
                        value={
                          Number.isFinite(initialCashForBase)
                            ? initialCashForBase
                            : ""
                        }
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
                        value={form.rebalance_schedule}
                        onChange={(e) =>
                          setField(
                            "rebalance_schedule",
                            e.target.value as RebalanceSchedule,
                          )
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
                <Button
                  onClick={() => void handleSubmit()}
                  disabled={!canSubmit}
                >
                  {submitting ? "실행 중..." : "백테스트 실행"}
                </Button>
              </div>
            </div>
          </div>

          {/* 우: 진행률 / 결과 (lg 이상). lg 미만에서는 폼 아래 stacked. */}
          <div className="space-y-6">
            {submittedRunId === null ? (
              <Card className="p-8 text-center text-sm text-gray-500">
                백테스트를 실행하면 결과가 이 영역에 표시됩니다.
              </Card>
            ) : (
              <>
                <ProgressPanel
                  run={polling.run}
                  loading={polling.loading}
                  error={polling.error}
                  onCancel={polling.cancelRun}
                  onReset={() => {
                    setSubmittedRunId(null);
                    setResult(null);
                  }}
                />

                {polling.run?.status === "done" && (
                  <BacktestResultPanel
                    result={result}
                    loading={resultLoading}
                    logScale={logScale}
                    onToggleLogScale={() => setLogScale((v) => !v)}
                  />
                )}
              </>
            )}
          </div>
        </div>
      </div>
    </main>
  );
}

// ─── 인플레이스 결과 패널 ──────────────────────────────────────────────
//
// `/backtests/[run_id]` 의 결과 화면과 동일한 시각화 컴포넌트들을 그대로
// 사용한다. 이력 화면 (별도 라우트) 은 회귀 0 — 이 패널은 신규 분리이며
// 기존 라우트에는 영향 없음.
function BacktestResultPanel({
  result,
  loading,
  logScale,
  onToggleLogScale,
}: {
  result: BacktestResult | null;
  loading: boolean;
  logScale: boolean;
  onToggleLogScale: () => void;
}) {
  if (loading || !result) {
    return (
      <Card className="p-6 text-center text-sm text-gray-500">
        {loading ? "결과 불러오는 중..." : "결과를 준비 중입니다."}
      </Card>
    );
  }
  const monthly = result.metrics?.monthly_returns ?? {};
  const hasMonthly = Object.keys(monthly).length > 0;

  return (
    <div className="space-y-6">
      <Card className="p-4">
        <div className="mb-3 flex items-center justify-between">
          <h2 className="text-lg font-semibold">자본 곡선</h2>
          <Button
            variant="ghost"
            size="sm"
            onClick={onToggleLogScale}
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
  );
}
