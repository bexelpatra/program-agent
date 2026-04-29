"use client";

/**
 * UniverseSelector — 자산 카탈로그 검색 + 다중 선택.
 *
 * 좌측 검색창(symbol/name prefix, 시장 필터) → 결과 리스트 → 클릭으로
 * 선택. 우측 영역(badge 그룹)에 선택 자산 누적, 클릭으로 제거.
 *
 * UI/UX 원칙 1 (JSON 노출 금지) — 사용자는 자산 메타(이름·시장·통화)로
 * 식별, asset_id 는 폼 제출 직전에만 변환되어 백엔드로 전송된다.
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

// AssetTable.tsx 와 동일한 트릭: AssetSchema.meta 의 .default({}) 가
// input/output variance 를 만들어 z.infer 와 listAssets() 의 실제 반환
// 타입이 어긋난다. listAssets() 의 actual return 을 element 타입으로
// 사용해 호출 사이트와 일치시킨다.
export type UniverseAsset = Awaited<
  ReturnType<typeof api.listAssets>
>["items"][number];

interface Props {
  value: UniverseAsset[];
  onChange: (next: UniverseAsset[]) => void;
}

const MARKET_OPTIONS: { value: string; label: string }[] = [
  { value: "", label: "전체 시장" },
  { value: "KR", label: ko.asset.market.KR },
  { value: "US", label: ko.asset.market.US },
  { value: "CRYPTO", label: ko.asset.market.CRYPTO },
];

export function UniverseSelector({ value, onChange }: Props) {
  const { toast } = useToast();
  const [query, setQuery] = useState("");
  const [market, setMarket] = useState("");
  const [results, setResults] = useState<UniverseAsset[]>([]);
  const [loading, setLoading] = useState(false);
  const [searched, setSearched] = useState(false);

  async function runSearch() {
    setLoading(true);
    try {
      const res = await api.listAssets({
        q: query || undefined,
        market: market || undefined,
        limit: 20,
      });
      setResults(res.items);
      setSearched(true);
    } catch (e) {
      const err = e as ApiError;
      toast({
        title: ko.error.generic,
        description:
          err.message + (err.traceId ? ` (${err.traceId.slice(0, 8)})` : ""),
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  }

  function add(asset: UniverseAsset) {
    if (value.some((a) => a.asset_id === asset.asset_id)) return;
    onChange([...value, asset]);
  }

  function remove(assetId: number) {
    onChange(value.filter((a) => a.asset_id !== assetId));
  }

  return (
    <div className="space-y-3">
      <div className="flex flex-wrap items-end gap-2">
        <div className="flex-1 min-w-[200px]">
          <Label htmlFor="universe_q">자산 검색 (심볼 또는 이름)</Label>
          <Input
            id="universe_q"
            placeholder="예: SPY, 삼성전자, BTC"
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
          <Label htmlFor="universe_market">시장</Label>
          <Select
            id="universe_market"
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
        <div className="rounded border border-gray-200 bg-white p-2 max-h-56 overflow-y-auto">
          {results.length === 0 ? (
            <p className="p-2 text-sm text-gray-500">
              검색 결과가 없습니다. 다른 키워드를 시도하거나 자산 카탈로그에서
              먼저 등록하세요.
            </p>
          ) : (
            <ul className="space-y-1">
              {results.map((asset) => {
                const alreadySelected = value.some(
                  (a) => a.asset_id === asset.asset_id,
                );
                return (
                  <li key={asset.asset_id}>
                    <button
                      type="button"
                      onClick={() => add(asset)}
                      disabled={alreadySelected}
                      className="w-full rounded p-2 text-left text-sm hover:bg-gray-100 disabled:cursor-not-allowed disabled:opacity-50"
                    >
                      <span className="font-mono">{asset.symbol}</span>
                      <span className="mx-2 text-gray-400">·</span>
                      <span>{asset.name}</span>
                      <span className="ml-2 text-xs text-gray-500">
                        ({ko.asset.market[asset.market]} / {asset.currency})
                      </span>
                      {alreadySelected && (
                        <span className="ml-2 text-xs text-blue-600">
                          (선택됨)
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
          선택된 자산 <span className="text-gray-500">({value.length})</span>
        </p>
        {value.length === 0 ? (
          <p className="text-sm text-gray-500">
            검색 후 자산을 선택해 universe 를 구성하세요.
          </p>
        ) : (
          <div className="flex flex-wrap gap-2">
            {value.map((asset) => (
              <button
                key={asset.asset_id}
                type="button"
                onClick={() => remove(asset.asset_id)}
                title="클릭해 제거"
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
