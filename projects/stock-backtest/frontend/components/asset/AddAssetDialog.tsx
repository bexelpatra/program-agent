"use client";

/**
 * AddAssetDialog — inline modal for creating a new asset.
 *
 * Implementation notes:
 *  · Uses an inline overlay (not Radix Dialog) to keep the bundle lean
 *    and avoid pulling in another peer dependency. The interaction
 *    surface is deliberately minimal — submit / cancel only.
 *  · Errors surfaced via toast follow UI/UX 원칙 2 (한국어 +
 *    actionable hint). 422 → "찾을 수 없는 자산", 409 → "이미 등록된
 *    자산", others → generic + truncated trace_id for support.
 *  · Backfill state surfaces through the create response: the backend
 *    returns `backfill_enqueued` plus an optional `note` describing
 *    progress (e.g., "백필 대기열 가득. cron 다음 사이클에서 실행"),
 *    matching UI/UX 원칙 3 (진행 상태 가시화).
 */
import { useState } from "react";

import { api, ApiError } from "@/lib/api/client";
import { AssetCreateSchema } from "@/lib/api/schemas";
import type { AssetType, Market } from "@/lib/api/schemas";
import { ko } from "@/lib/i18n/ko";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Select } from "@/components/ui/select";
import { Label } from "@/components/ui/label";
import { useToast } from "@/components/ui/toast";

interface Props {
  open: boolean;
  onOpenChange: (v: boolean) => void;
  onCreated: () => void;
}

export function AddAssetDialog({ open, onOpenChange, onCreated }: Props) {
  const [symbol, setSymbol] = useState("");
  const [market, setMarket] = useState<Market>("US");
  const [assetType, setAssetType] = useState<AssetType>("ETF");
  const [currency, setCurrency] = useState("USD");
  const [name, setName] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const { toast } = useToast();

  if (!open) return null;

  function resetForm() {
    setSymbol("");
    setName("");
  }

  async function submit() {
    setSubmitting(true);
    try {
      const payload = AssetCreateSchema.parse({
        symbol: symbol.trim(),
        market,
        asset_type: assetType,
        currency,
        name: name.trim(),
        meta: {},
      });
      const res = await api.createAsset(payload);
      const backfillNote = res.backfill_enqueued
        ? "백필 진행 중"
        : "백필 예약 실패 — cron 대기";
      toast({
        title: "자산 등록 완료",
        description:
          res.note ??
          `${res.asset.symbol} (${res.asset.name}) 등록됨. ${backfillNote}`,
        variant: "success",
      });
      onCreated();
      onOpenChange(false);
      resetForm();
    } catch (e) {
      const err = e as ApiError;
      const title =
        err.status === 422
          ? ko.asset.notFound
          : err.status === 409
            ? ko.asset.duplicate
            : ko.error.generic;
      const traceSuffix = err.traceId
        ? ` (추적 ${err.traceId.slice(0, 8)})`
        : "";
      toast({
        title,
        description: `${err.message}${traceSuffix}`,
        variant: "destructive",
      });
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/50"
      role="dialog"
      aria-modal="true"
      aria-labelledby="add-asset-title"
    >
      <div className="w-full max-w-lg rounded-lg bg-white p-6 shadow-xl">
        <h2 id="add-asset-title" className="text-xl font-semibold">
          {ko.asset.add}
        </h2>
        <p className="mt-1 text-sm text-gray-600">
          ticker 와 기본 정보를 입력하면 즉시 검증 후 등록됩니다.
        </p>

        <div className="mt-4 space-y-3">
          <div className="space-y-1">
            <Label htmlFor="symbol">{ko.asset.addTickerLabel}</Label>
            <Input
              id="symbol"
              value={symbol}
              onChange={(e) => setSymbol(e.target.value)}
              placeholder="예: VTI, 069500, BTC-USD"
            />
          </div>
          <div className="space-y-1">
            <Label htmlFor="market">{ko.asset.addMarketLabel}</Label>
            <Select
              id="market"
              value={market}
              onChange={(e) => setMarket(e.target.value as Market)}
            >
              <option value="KR">{ko.asset.market.KR}</option>
              <option value="US">{ko.asset.market.US}</option>
              <option value="CRYPTO">{ko.asset.market.CRYPTO}</option>
            </Select>
          </div>
          <div className="space-y-1">
            <Label htmlFor="asset_type">자산 종류</Label>
            <Select
              id="asset_type"
              value={assetType}
              onChange={(e) => setAssetType(e.target.value as AssetType)}
            >
              <option value="ETF">ETF</option>
              <option value="EQUITY_INDEX">지수</option>
              <option value="BOND">채권</option>
              <option value="COMMODITY">원자재</option>
              <option value="CRYPTO">암호화폐</option>
            </Select>
          </div>
          <div className="space-y-1">
            <Label htmlFor="currency">통화</Label>
            <Input
              id="currency"
              value={currency}
              onChange={(e) => setCurrency(e.target.value)}
              placeholder="USD / KRW"
            />
          </div>
          <div className="space-y-1">
            <Label htmlFor="name">한글 이름</Label>
            <Input
              id="name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="예: Vanguard 토탈 마켓 ETF"
            />
          </div>
        </div>

        <div className="mt-6 flex justify-end gap-2">
          <Button
            variant="secondary"
            onClick={() => onOpenChange(false)}
            disabled={submitting}
          >
            취소
          </Button>
          <Button
            onClick={submit}
            disabled={submitting || !symbol.trim() || !name.trim()}
          >
            {submitting ? "검증 중..." : ko.asset.addSubmit}
          </Button>
        </div>
      </div>
    </div>
  );
}
