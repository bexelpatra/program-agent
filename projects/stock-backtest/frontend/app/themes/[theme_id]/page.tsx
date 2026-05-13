"use client";

/**
 * /themes/[theme_id] — Phase 2 테마 상세 + 정규화 차트 (TASK-308).
 *
 * 화면 구성:
 *   1. 테마 메타 카드 (이름/설명/멤버 표 + 자산 제거 인라인 버튼).
 *   2. 기간 선택 (start / end) + universe 교집합 통지 토스트.
 *   3. 멤버 정규화 (NormalizedPriceChart, rebase=100 다중 라인).
 *   4. 합산 시계열 (ThemeAggregateChart, equal weighting 단일 라인).
 *   5. "다른 테마와 비교" 영역 — 테마 다중 선택 → compareThemes →
 *      ThemeCompareChart 렌더.
 *
 * 절대 원칙 1·2·3·5 (JSON 비노출, 한국어, 진행 가시화, MVP 한정) 모두
 * 강제. 원칙 4 (시각화) — equity 차트가 아닌 정규화/합산/비교 3종 차트로
 * Phase 2 트랙 전용 시각화 (architecture.md V3 § "Frontend 화면 추가").
 *
 * ko.ts 의 `theme.*` namespace 는 TASK-307 가 별도로 추가하므로, 본
 * 화면은 inline 한국어 문자열을 사용한다 (Reviewer 권고 — 본 PR 의
 * `lib/i18n/ko.ts` 수정 라인 = 0).
 */
import Link from "next/link";
import { useCallback, useEffect, useMemo, useState } from "react";

import { api, ApiError } from "@/lib/api/client";

// `.default([])` 가 붙은 `active_members` / `affected_assets` 는 Zod 의
// input/output variance 로 인해 `z.infer` 결과와 실제 `api.X()` 반환 타입의
// 호환성이 깨질 수 있다 (frontend/lib/api/types.ts 모듈 주석 참조 —
// TASK-238 가 이미 backtest 결과에서 동일 이슈를 다룬다). 본 페이지의 state
// 는 실제 호출 반환 타입을 그대로 사용해 변종 (variance) 을 우회한다.
type ThemeDetailRow = Awaited<ReturnType<typeof api.getTheme>>;
type ThemeCompareData = Awaited<ReturnType<typeof api.compareThemes>>;
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useToast } from "@/components/ui/toast";

import { NormalizedPriceChart } from "@/components/themes/charts/NormalizedPriceChart";
import { ThemeAggregateChart } from "@/components/themes/charts/ThemeAggregateChart";
import { ThemeCompareChart } from "@/components/themes/charts/ThemeCompareChart";
import { useThemeChartData } from "@/hooks/useThemeChartData";

interface PageProps {
  params: { theme_id: string };
}

/** trace_id 앞 8자리 prefix — 길어진 추적 ID 의 시각적 잡음 축소. */
function tracePrefix(traceId: string): string {
  return traceId ? traceId.slice(0, 8) : "";
}

export default function ThemeDetailPage({ params }: PageProps) {
  const themeId = Number.parseInt(params.theme_id, 10);
  const isValidId = Number.isFinite(themeId) && themeId > 0;
  const { toast } = useToast();

  // ── 1. 테마 메타 / 멤버 표 ─────────────────────────────────────────
  const [theme, setTheme] = useState<ThemeDetailRow | null>(null);
  const [themeLoading, setThemeLoading] = useState<boolean>(false);

  const loadTheme = useCallback(async () => {
    if (!isValidId) return;
    setThemeLoading(true);
    try {
      const t = await api.getTheme(themeId);
      setTheme(t);
    } catch (e) {
      const err = e instanceof ApiError ? e : null;
      toast({
        title: "테마 조회 실패",
        description: err
          ? `[${tracePrefix(err.traceId)}] ${err.message}`
          : "알 수 없는 오류",
        variant: "destructive",
      });
    } finally {
      setThemeLoading(false);
    }
  }, [themeId, isValidId, toast]);

  useEffect(() => {
    void loadTheme();
  }, [loadTheme]);

  // ── 2. 기간 선택 ──────────────────────────────────────────────────
  const [start, setStart] = useState<string>("");
  const [end, setEnd] = useState<string>("");

  const chartOpts = useMemo(
    () => ({
      normalize: "base100" as const,
      weighting: "equal" as const,
      start: start || undefined,
      end: end || undefined,
    }),
    [start, end],
  );

  // ── 3. 차트 데이터 ────────────────────────────────────────────────
  const {
    data: chartData,
    loading: chartLoading,
    error: chartError,
    refetch: refetchChart,
  } = useThemeChartData(isValidId ? themeId : 0, chartOpts);

  // universe 교집합 통지 — affected_assets 비어있지 않으면 토스트.
  // chartData 가 새로 들어올 때마다 한 번만 토스트 (해시로 가드).
  const [lastUniverseHash, setLastUniverseHash] = useState<string>("");
  useEffect(() => {
    if (!chartData?.universe_meta) return;
    const m = chartData.universe_meta;
    // Zod `.default([])` 변종 (variance) 으로 인해 optional 로 좁혀질 수
    // 있어 방어적 fallback.
    const affected = m.affected_assets ?? [];
    const hash = `${m.adjusted_start}|${m.adjusted_end}|${affected.join(",")}`;
    if (hash === lastUniverseHash) return;
    setLastUniverseHash(hash);
    if (affected.length > 0 && m.reason !== "ok") {
      toast({
        title: "기간이 자동 조정됐습니다",
        description: m.message,
      });
    }
  }, [chartData, lastUniverseHash, toast]);

  useEffect(() => {
    if (!chartError) return;
    toast({
      title: "차트 조회 실패",
      description: `[${tracePrefix(chartError.traceId)}] ${chartError.message}`,
      variant: "destructive",
    });
  }, [chartError, toast]);

  // ── 4. 자산 제거 (인라인) ─────────────────────────────────────────
  const handleRemoveAsset = useCallback(
    async (assetId: number) => {
      if (!isValidId) return;
      const ok = window.confirm("이 자산을 테마에서 제거하시겠습니까?");
      if (!ok) return;
      try {
        await api.removeAssetFromTheme(themeId, assetId);
        toast({
          title: "자산을 제거했습니다",
          variant: "success",
        });
        await loadTheme();
        refetchChart();
      } catch (e) {
        const err = e instanceof ApiError ? e : null;
        toast({
          title: "자산 제거 실패",
          description: err
            ? `[${tracePrefix(err.traceId)}] ${err.message}`
            : "알 수 없는 오류",
          variant: "destructive",
        });
      }
    },
    [themeId, isValidId, toast, loadTheme, refetchChart],
  );

  // ── 5. "다른 테마와 비교" ──────────────────────────────────────────
  const [compareOpen, setCompareOpen] = useState<boolean>(false);
  const [allThemes, setAllThemes] = useState<{ theme_id: number; name: string }[]>(
    [],
  );
  const [selectedCompareIds, setSelectedCompareIds] = useState<number[]>([]);
  const [compareData, setCompareData] = useState<ThemeCompareData | null>(
    null,
  );
  const [compareLoading, setCompareLoading] = useState<boolean>(false);
  const [lastCompareUniverseHash, setLastCompareUniverseHash] =
    useState<string>("");

  const openCompare = useCallback(async () => {
    setCompareOpen(true);
    try {
      const res = await api.listThemes(undefined, 200, 0);
      setAllThemes(res.items.map((t) => ({ theme_id: t.theme_id, name: t.name })));
      // 본 테마는 기본 포함.
      setSelectedCompareIds((prev) =>
        prev.length === 0 && isValidId ? [themeId] : prev,
      );
    } catch (e) {
      const err = e instanceof ApiError ? e : null;
      toast({
        title: "테마 목록 조회 실패",
        description: err
          ? `[${tracePrefix(err.traceId)}] ${err.message}`
          : "알 수 없는 오류",
        variant: "destructive",
      });
    }
  }, [themeId, isValidId, toast]);

  const toggleCompareTheme = useCallback((tid: number) => {
    setSelectedCompareIds((cur) =>
      cur.includes(tid) ? cur.filter((x) => x !== tid) : [...cur, tid],
    );
  }, []);

  const runCompare = useCallback(async () => {
    if (selectedCompareIds.length < 2) {
      toast({
        title: "테마 2개 이상을 선택하세요",
        variant: "destructive",
      });
      return;
    }
    setCompareLoading(true);
    try {
      const res = await api.compareThemes(selectedCompareIds, {
        normalize: "base100",
        weighting: "equal",
        start: start || undefined,
        end: end || undefined,
      });
      setCompareData(res);
      // Zod 출력 타입은 `affected_assets` 가 required (`.default([])`) 지만
      // 일부 추론 경로에서 optional 로 좁혀질 수 있어 방어적 fallback.
      const m = res.universe_meta;
      const affected = m.affected_assets ?? [];
      const hash = `${m.adjusted_start}|${m.adjusted_end}|${affected.join(",")}`;
      if (
        affected.length > 0 &&
        m.reason !== "ok" &&
        hash !== lastCompareUniverseHash
      ) {
        setLastCompareUniverseHash(hash);
        toast({
          title: "비교 기간이 자동 조정됐습니다",
          description: m.message,
        });
      }
    } catch (e) {
      const err = e instanceof ApiError ? e : null;
      toast({
        title: "테마 비교 실패",
        description: err
          ? `[${tracePrefix(err.traceId)}] ${err.message}`
          : "알 수 없는 오류",
        variant: "destructive",
      });
    } finally {
      setCompareLoading(false);
    }
  }, [selectedCompareIds, start, end, lastCompareUniverseHash, toast]);

  if (!isValidId) {
    return (
      <main className="min-h-screen bg-gray-50 p-8">
        <div className="mx-auto max-w-5xl">
          <Card className="p-6 text-sm text-red-700">
            잘못된 테마 ID 입니다.
            <div className="mt-3">
              <Link href="/themes">
                <Button variant="secondary">테마 목록으로</Button>
              </Link>
            </div>
          </Card>
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-gray-50 p-8">
      <div className="mx-auto max-w-7xl space-y-6">
        {/* 헤더 */}
        <header className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold">
              {theme?.name ?? (themeLoading ? "로딩 중..." : `테마 #${themeId}`)}
            </h1>
            {theme?.description ? (
              <p className="mt-1 text-sm text-gray-600">{theme.description}</p>
            ) : null}
          </div>
          <Link href="/themes">
            <Button variant="secondary">← 테마 목록</Button>
          </Link>
        </header>

        {/* 1. 멤버 표 */}
        <Card className="p-4">
          <div className="mb-3 flex items-center justify-between">
            <h2 className="text-lg font-semibold">멤버 자산</h2>
            <span className="text-sm text-gray-500">
              총 {theme?.active_members?.length ?? 0}개
            </span>
          </div>
          {theme && (theme.active_members?.length ?? 0) > 0 ? (
            <table className="w-full text-left">
              <thead className="border-b bg-gray-50">
                <tr>
                  <th className="p-3 text-sm font-medium text-gray-600">
                    자산 ID
                  </th>
                  <th className="p-3 text-sm font-medium text-gray-600">
                    추가일
                  </th>
                  <th className="p-3 text-sm font-medium text-gray-600">
                    메모
                  </th>
                  <th className="p-3 text-right text-sm font-medium text-gray-600">
                    동작
                  </th>
                </tr>
              </thead>
              <tbody>
                {(theme.active_members ?? []).map((m) => (
                  <tr
                    key={m.asset_id}
                    className="border-b last:border-0 hover:bg-gray-50"
                  >
                    <td className="p-3 font-mono text-sm">{m.asset_id}</td>
                    <td className="p-3 text-sm text-gray-600">
                      {m.added_at.slice(0, 10)}
                    </td>
                    <td className="p-3 text-sm text-gray-600">
                      {m.note ?? "-"}
                    </td>
                    <td className="p-3 text-right">
                      <Button
                        variant="destructive"
                        size="sm"
                        onClick={() => handleRemoveAsset(m.asset_id)}
                      >
                        제거
                      </Button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <div className="p-6 text-center text-sm text-gray-500">
              {themeLoading
                ? "멤버를 불러오는 중..."
                : "이 테마에 등록된 자산이 없습니다. 자산을 추가하면 정규화 차트가 표시됩니다."}
            </div>
          )}
          {/* AssetPicker 는 TASK-307 책임 — 본 화면에서는 자산 추가 UI 생략. */}
        </Card>

        {/* 2. 기간 선택 */}
        <Card className="p-4">
          <h2 className="mb-3 text-lg font-semibold">기간 선택</h2>
          <div className="flex flex-wrap items-end gap-3">
            <div className="flex flex-col gap-1">
              <Label htmlFor="period-start">시작일</Label>
              <Input
                id="period-start"
                type="date"
                value={start}
                onChange={(e) => setStart(e.target.value)}
                className="max-w-[180px]"
              />
            </div>
            <div className="flex flex-col gap-1">
              <Label htmlFor="period-end">종료일</Label>
              <Input
                id="period-end"
                type="date"
                value={end}
                onChange={(e) => setEnd(e.target.value)}
                className="max-w-[180px]"
              />
            </div>
            <Button onClick={refetchChart} disabled={chartLoading}>
              {chartLoading ? "조회 중..." : "차트 갱신"}
            </Button>
            {chartData?.universe_meta &&
            chartData.universe_meta.reason !== "ok" ? (
              <span className="ml-auto text-sm text-amber-700">
                {chartData.universe_meta.adjusted_start} ~{" "}
                {chartData.universe_meta.adjusted_end} 로 자동 조정됨
              </span>
            ) : null}
          </div>
        </Card>

        {/* 3. NormalizedPriceChart */}
        <Card className="p-4">
          <h2 className="mb-3 text-lg font-semibold">멤버 정규화 (기준 100)</h2>
          {chartLoading && !chartData ? (
            <div className="p-4 text-sm text-gray-500">차트를 불러오는 중...</div>
          ) : chartData ? (
            <NormalizedPriceChart members={chartData.members} />
          ) : (
            <div className="p-4 text-sm text-gray-500">데이터가 없습니다.</div>
          )}
        </Card>

        {/* 4. ThemeAggregateChart */}
        <Card className="p-4">
          <h2 className="mb-3 text-lg font-semibold">테마 합산 (등가중)</h2>
          {chartLoading && !chartData ? (
            <div className="p-4 text-sm text-gray-500">차트를 불러오는 중...</div>
          ) : chartData ? (
            <ThemeAggregateChart
              points={chartData.aggregate}
              label={theme?.name ?? `테마 ${themeId}`}
            />
          ) : (
            <div className="p-4 text-sm text-gray-500">데이터가 없습니다.</div>
          )}
        </Card>

        {/* 5. "다른 테마와 비교" */}
        <Card className="p-4">
          <div className="mb-3 flex items-center justify-between">
            <h2 className="text-lg font-semibold">다른 테마와 비교</h2>
            {!compareOpen ? (
              <Button onClick={openCompare}>비교 시작</Button>
            ) : (
              <Button variant="secondary" onClick={() => setCompareOpen(false)}>
                닫기
              </Button>
            )}
          </div>
          {compareOpen ? (
            <div className="space-y-3">
              <div className="flex flex-wrap gap-2">
                {allThemes.length === 0 ? (
                  <span className="text-sm text-gray-500">
                    테마 목록을 불러오는 중...
                  </span>
                ) : (
                  allThemes.map((t) => {
                    const checked = selectedCompareIds.includes(t.theme_id);
                    return (
                      <button
                        key={t.theme_id}
                        type="button"
                        onClick={() => toggleCompareTheme(t.theme_id)}
                        className={
                          checked
                            ? "rounded-full border border-blue-600 bg-blue-50 px-3 py-1 text-sm text-blue-700"
                            : "rounded-full border border-gray-300 bg-white px-3 py-1 text-sm text-gray-700 hover:bg-gray-50"
                        }
                      >
                        {checked ? "✓ " : ""}
                        {t.name}
                      </button>
                    );
                  })
                )}
              </div>
              <div className="flex items-center gap-3">
                <Button onClick={runCompare} disabled={compareLoading}>
                  {compareLoading ? "비교 중..." : "비교 차트 그리기"}
                </Button>
                <span className="text-xs text-gray-500">
                  {selectedCompareIds.length}개 선택됨 — 2개 이상 권장
                </span>
              </div>
              {compareData ? (
                <div className="pt-2">
                  <ThemeCompareChart themes={compareData.themes} />
                </div>
              ) : null}
            </div>
          ) : null}
        </Card>
      </div>
    </main>
  );
}
