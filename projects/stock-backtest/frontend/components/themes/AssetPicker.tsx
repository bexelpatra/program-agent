"use client";

/**
 * AssetPicker — 자산 검색 + 다중 선택 위젯 (TASK-307).
 *
 * 기존 `UniverseSelector` (components/backtest/UniverseSelector.tsx) 의
 * 검색 UI 를 재사용 패턴으로 가져왔지만, 본 컴포넌트의 목적이 다르다:
 *   · UniverseSelector — 백테스트 universe (Asset 객체 누적, 비중 매핑)
 *   · AssetPicker — 테마 멤버 추가 시 자산 다중 선택 → asset_id 만 외부에
 *     넘기고, 추가된 자산은 부모 (ThemeEditor 또는 detail 화면) 가
 *     `api.addAssetToTheme` 를 반복 호출해 백엔드에 반영
 *
 * 차이점 때문에 신규 작성 (UniverseSelector 복사가 아닌). API 표면:
 *   · `excludeAssetIds` — 이미 테마 멤버인 자산을 검색 결과에서 disable
 *     처리 (중복 추가 방지 UI).
 *   · `selected` / `onSelectedChange` — 부모가 controlled state 로 관리.
 *     배열에는 Asset 객체 그대로 (parent 가 name/symbol 라벨링에 사용).
 *
 * UI/UX 원칙:
 *   · 1 (JSON 노출 0) — 폼만으로 자산 검색 + 선택.
 *   · 2 (한국어) — 모든 라벨/플레이스홀더/에러 한국어 + traceId.
 *   · 3 (진행 가시화) — loading "검색 중..." spinner.
 */
import { useState } from "react";

import { api, ApiError } from "@/lib/api/client";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select } from "@/components/ui/select";
import { useToast } from "@/components/ui/toast";
import { ko } from "@/lib/i18n/ko";
import type { Asset } from "@/lib/api/types";

interface Props {
  selected: Asset[];
  onSelectedChange: (next: Asset[]) => void;
  /** 이미 테마 멤버인 자산 — 검색 결과에서 disable 처리하기 위한 목록. */
  excludeAssetIds?: number[];
}

const MARKET_OPTIONS: { value: string; label: string }[] = [
  { value: "", label: "전체 시장" },
  { value: "KR", label: ko.asset.market.KR },
  { value: "US", label: ko.asset.market.US },
  { value: "CRYPTO", label: ko.asset.market.CRYPTO },
];

export function AssetPicker({
  selected,
  onSelectedChange,
  excludeAssetIds = [],
}: Props) {
  const { toast } = useToast();
  const [query, setQuery] = useState("");
  const [market, setMarket] = useState("");
  const [results, setResults] = useState<Asset[]>([]);
  const [loading, setLoading] = useState(false);
  const [searched, setSearched] = useState(false);

  async function runSearch() {
    setLoading(true);
    try {
      const res = await api.listAssets({
        q: query || undefined,
        market: market || undefined,
        limit: 25,
      });
      setResults(res.items);
      setSearched(true);
    } catch (e) {
      const err = e as ApiError;
      const traceSuffix = err.traceId
        ? ` (${err.traceId.slice(0, 8)})`
        : "";
      toast({
        title: ko.error.generic,
        description: `${err.message}${traceSuffix}`,
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  }

  function toggle(asset: Asset) {
    const already = selected.some((a) => a.asset_id === asset.asset_id);
    if (already) {
      onSelectedChange(
        selected.filter((a) => a.asset_id !== asset.asset_id),
      );
    } else {
      onSelectedChange([...selected, asset]);
    }
  }

  function isExcluded(assetId: number): boolean {
    return excludeAssetIds.includes(assetId);
  }

  return (
    <div className="space-y-3">
      <div className="flex flex-wrap items-end gap-2">
        <div className="flex-1 min-w-[200px]">
          <Label htmlFor="asset_picker_q">
            {ko.theme.assets.pickerSearchLabel}
          </Label>
          <Input
            id="asset_picker_q"
            placeholder={ko.theme.assets.pickerSearchPlaceholder}
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                e.preventDefault();
                void runSearch();
              }
            }}
          />
        </div>
        <div className="w-40">
          <Label htmlFor="asset_picker_market">시장</Label>
          <Select
            id="asset_picker_market"
            value={market}
            onChange={(e) => setMarket(e.target.value)}
          >
            {MARKET_OPTIONS.map((opt) => (
              <option key={opt.value} value={opt.value}>
                {opt.label}
              </option>
            ))}
          </Select>
        </div>
        <Button
          variant="secondary"
          onClick={() => void runSearch()}
          disabled={loading}
        >
          {loading ? "검색 중..." : "검색"}
        </Button>
      </div>

      {searched && (
        <div
          className="rounded border border-gray-200 bg-white p-2 max-h-56 overflow-y-auto"
          data-testid="asset-picker-results"
        >
          {results.length === 0 ? (
            <p className="p-2 text-sm text-gray-500">
              {ko.theme.assets.pickerEmpty}
            </p>
          ) : (
            <ul className="space-y-1">
              {results.map((asset) => {
                const isSelected = selected.some(
                  (a) => a.asset_id === asset.asset_id,
                );
                const excluded = isExcluded(asset.asset_id);
                return (
                  <li key={asset.asset_id}>
                    <button
                      type="button"
                      onClick={() => toggle(asset)}
                      disabled={excluded}
                      aria-pressed={isSelected}
                      data-testid={`asset-picker-row-${asset.asset_id}`}
                      className={
                        "w-full rounded p-2 text-left text-sm transition-colors " +
                        (isSelected
                          ? "bg-blue-50 ring-1 ring-blue-300"
                          : "hover:bg-gray-100") +
                        " disabled:cursor-not-allowed disabled:opacity-50"
                      }
                    >
                      <span className="font-mono">{asset.symbol}</span>
                      <span className="mx-2 text-gray-400">·</span>
                      <span>{asset.name}</span>
                      <span className="ml-2 text-xs text-gray-500">
                        ({ko.asset.market[asset.market]} / {asset.currency})
                      </span>
                      {isSelected && (
                        <span className="ml-2 text-xs text-blue-600">
                          ✓ {ko.theme.assets.selectedCount}
                        </span>
                      )}
                      {excluded && (
                        <span className="ml-2 text-xs text-amber-600">
                          ({ko.theme.assets.already})
                        </span>
                      )}
                    </button>
                  </li>
                );
              })}
            </ul>
          )}
        </div>
      )}

      <div>
        <p className="mb-2 text-sm font-medium">
          {ko.theme.assets.selectedCount}{" "}
          <span className="text-gray-500">({selected.length})</span>
        </p>
        {selected.length === 0 ? (
          <p className="text-sm text-gray-500">
            검색 후 자산을 선택하세요.
          </p>
        ) : (
          <div className="flex flex-wrap gap-2">
            {selected.map((asset) => (
              <button
                key={asset.asset_id}
                type="button"
                onClick={() => toggle(asset)}
                title="클릭해 선택 해제"
                className="cursor-pointer"
              >
                <Badge variant="secondary">
                  <span className="font-mono">{asset.symbol}</span>
                  <span className="mx-1 text-gray-500">·</span>
                  {asset.name}
                  <span className="ml-2 text-gray-400">×</span>
                </Badge>
              </button>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
