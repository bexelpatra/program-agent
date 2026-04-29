"use client";

/**
 * /assets — Asset Catalogue page.
 *
 * One of the three core screens (Quant Lab CLAUDE.md L26: "3 화면 한도").
 * Responsibilities:
 *   1. Search registered assets by symbol or 한글 이름 (server-side
 *      `q` filter on /api/assets).
 *   2. Filter by market (KR / US / CRYPTO).
 *   3. Add a new asset via <AddAssetDialog>; after success, refresh
 *      the list so the new row appears immediately.
 *
 * UI/UX 원칙 적용:
 *  · 1 (JSON 노출 금지) — form-only inputs, no JSON view.
 *  · 2 (한국어 우선) — every label / placeholder / error in Korean.
 *  · 3 (진행 상태 가시화) — "로딩 중...", "검증 중...", toast on
 *    success/failure incl. trace_id for support.
 */
import { useCallback, useEffect, useState } from "react";

import { api, ApiError } from "@/lib/api/client";
import { ko } from "@/lib/i18n/ko";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Select } from "@/components/ui/select";
import { Card } from "@/components/ui/card";
import { useToast } from "@/components/ui/toast";
import { AddAssetDialog } from "@/components/asset/AddAssetDialog";
import { AssetTable, type AssetRow } from "@/components/asset/AssetTable";

export default function AssetsPage() {
  const [items, setItems] = useState<AssetRow[]>([]);
  const [loading, setLoading] = useState(false);
  const [q, setQ] = useState("");
  const [market, setMarket] = useState<string>("");
  const [open, setOpen] = useState(false);
  const { toast } = useToast();

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const res = await api.listAssets({
        q: q || undefined,
        market: market || undefined,
        limit: 100,
      });
      setItems(res.items);
    } catch (e) {
      const err = e as ApiError;
      const traceSuffix = err.traceId
        ? ` (${ko.error.contactSupport} ${err.traceId})`
        : "";
      toast({
        title: ko.error.generic,
        description: `${err.message}${traceSuffix}`,
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  }, [q, market, toast]);

  useEffect(() => {
    load();
  }, [load]);

  return (
    <main className="min-h-screen bg-gray-50 p-8">
      <div className="mx-auto max-w-7xl space-y-6">
        <header className="flex items-center justify-between">
          <h1 className="text-3xl font-bold">자산 카탈로그</h1>
          <Button onClick={() => setOpen(true)}>{ko.asset.add}</Button>
        </header>

        <Card className="p-4">
          <div className="flex gap-3">
            <Input
              placeholder="심볼 또는 한글명 검색"
              value={q}
              onChange={(e) => setQ(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter") load();
              }}
            />
            <Select
              value={market}
              onChange={(e) => setMarket(e.target.value)}
              className="max-w-[180px]"
            >
              <option value="">전체 시장</option>
              <option value="KR">{ko.asset.market.KR}</option>
              <option value="US">{ko.asset.market.US}</option>
              <option value="CRYPTO">{ko.asset.market.CRYPTO}</option>
            </Select>
            <Button
              variant="secondary"
              onClick={load}
              disabled={loading}
              className="shrink-0"
            >
              {loading ? "로딩 중..." : "검색"}
            </Button>
          </div>
        </Card>

        <Card className="p-0">
          <AssetTable items={items} />
        </Card>
      </div>

      <AddAssetDialog
        open={open}
        onOpenChange={setOpen}
        onCreated={load}
      />
    </main>
  );
}
