"use client";

/**
 * AssetWeightMap — universe 의 자산별 목표 비중(0~100%) 입력 위젯.
 *
 * UI/UX 원칙 1 (JSON / 코드 노출 금지) 강제 — FixedWeight 의
 * `weights: dict[int, float]` 같은 dict 타입 파라미터를 사용자에게
 * raw JSON textarea 로 노출하던 임시 우회를 영구 제거하고 이 위젯이
 * 책임진다.
 *
 * 컨트롤드 컴포넌트:
 *   props.value          asset_id(number) → 비중(0~1) 의 dict
 *   props.onChange(next) 부모가 보유한 state 갱신
 *   props.universe       NewBacktestPage 가 UniverseSelector 로 모은
 *                        자산 배열을 그대로 전달 (asset_id, symbol,
 *                        name, market 만 사용)
 *   props.allowCashSlot  true 일 때 합계 < 100% 인 잔여를 _CASH_
 *                        슬리브로 안내 (architecture.md V3 § 현금/FX 모델
 *                        — base_currency 잔고로 자동 충족)
 *
 * 백엔드 계약: `weights` 의 키는 **asset_id 정수**. ticker 문자열을
 * 키로 보내면 422 ValidationError 가 난다 (FixedWeightParams.weights:
 * dict[int, float]). 이 위젯은 universe 자산의 asset_id 를 그대로
 * 키로 쓰므로 사용자가 ticker 를 직접 타이핑할 여지를 차단한다.
 */
import { useMemo } from "react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ko } from "@/lib/i18n/ko";

/**
 * universe 항목의 최소 인터페이스. UniverseSelector 가 노출하는
 * UniverseAsset 보다 좁게 잡아 외부 page 어디서 호출하든 어색하지
 * 않게 한다 (Asset / UniverseAsset 양쪽 호환).
 *
 * TASK-204: `currency` 추가 — amber 경고 배너에서 1주 가격을 native
 * currency 로 표시할 때 사용. 통화별 포맷터(`formatPrice`)가 분기.
 */
export interface AssetWeightMapAsset {
  asset_id: number;
  symbol: string;
  name: string;
  market: "KR" | "US" | "CRYPTO";
  currency: string;
}

interface Props {
  universe: AssetWeightMapAsset[];
  value: Record<number, number>;
  onChange: (next: Record<number, number>) => void;
  allowCashSlot?: boolean;
  /**
   * TASK-204: 자산별 최근 close 가격 (native currency 기준).
   * 키는 `asset_id`. 값이 없으면 (= prefetch 미완료 또는 백필 데이터
   * 없음) 해당 자산은 경고 평가 대상에서 제외 (silently 스킵).
   */
  latestPrices?: Record<number, number>;
  /**
   * TASK-204: 초기 자본 (base_currency 단위). 매수 가능 평가의
   * 분모로 사용. 0 이하이거나 미정의면 경고 평가 자체를 스킵
   * (initial_cash 미입력 단계에서 노이즈 회피).
   */
  initialCash?: number;
  /**
   * TASK-204: 초기 자본의 통화. 자산 native currency 와 다를 수 있으나
   * 1단계 단순화로 환산 없이 raw 비교 (FX 가 적용되면 사용자 보수적
   * 으로 자본을 늘리는 방향 안전). 표시 용도로만 사용.
   */
  baseCurrency?: string;
}

const MARKET_LABEL: Record<AssetWeightMapAsset["market"], string> = {
  KR: ko.asset.market.KR,
  US: ko.asset.market.US,
  CRYPTO: ko.asset.market.CRYPTO,
};

function clampPct(raw: number): number {
  if (!Number.isFinite(raw)) return 0;
  return Math.max(0, Math.min(100, raw));
}

/**
 * TASK-204: native currency 기준 1주 가격 포맷.
 * USD = `$1,234.56`, KRW = `₩12,345` (정수 — KRW 는 소수점 의미 없음),
 * 기타 = `123.45 XXX` fallback. 매수 불가 경고 메시지 안에서 사용.
 */
function formatPrice(value: number, currency: string): string {
  if (currency === "USD") {
    return `$${value.toLocaleString("en-US", {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    })}`;
  }
  if (currency === "KRW") {
    return `₩${Math.round(value).toLocaleString("ko-KR")}`;
  }
  return `${value.toLocaleString("en-US", {
    maximumFractionDigits: 2,
  })} ${currency}`;
}

/**
 * TASK-204: 매수 불가 경고 계산.
 *
 * 정수 주 단위 자산(KR/US market) 에 한해, 자산 1주 가격이
 * `initial_cash * weight` 보다 크면 0주 체결 → equity 평탄선 사고
 * (사용자 첫 시도 run_id=56 사례) 가 재현된다. 사전에 amber 경고로
 * 노출해 사용자가 자본을 늘리거나 비중을 줄이도록 유도한다.
 *
 * CRYPTO market 은 fractional 매매 가능(TASK-205) 이므로 평가 제외.
 *
 * 통화 환산은 1단계 단순화로 생략 — native price vs base_currency 자본
 * 의 raw 비교. fx 가 적용되면 일반적으로 자본 측이 늘어나므로 사용자가
 * 보수적으로 자본을 키우는 방향이 안전.
 */
export interface UnbuyableAlert {
  asset_id: number;
  symbol: string;
  currency: string;
  pricePerShare: number;
  weight: number;
  targetCash: number;
}

export function computeUnbuyableAlerts(
  universe: AssetWeightMapAsset[],
  value: Record<number, number>,
  latestPrices: Record<number, number> | undefined,
  initialCash: number | undefined,
): UnbuyableAlert[] {
  if (!latestPrices) return [];
  if (!initialCash || initialCash <= 0) return [];
  const alerts: UnbuyableAlert[] = [];
  for (const asset of universe) {
    if (asset.market === "CRYPTO") continue; // fractional 가능 — 평가 제외
    const weight = value[asset.asset_id] ?? 0;
    if (weight <= 0) continue;
    const price = latestPrices[asset.asset_id];
    if (price === undefined || price <= 0) continue; // 가격 미수집 → 평가 보류
    const targetCash = initialCash * weight;
    if (targetCash < price) {
      alerts.push({
        asset_id: asset.asset_id,
        symbol: asset.symbol,
        currency: asset.currency,
        pricePerShare: price,
        weight,
        targetCash,
      });
    }
  }
  return alerts;
}

export function AssetWeightMap({
  universe,
  value,
  onChange,
  allowCashSlot = true,
  latestPrices,
  initialCash,
  baseCurrency,
}: Props) {
  const total = useMemo(
    () =>
      universe.reduce((sum, a) => sum + (value[a.asset_id] ?? 0), 0),
    [universe, value],
  );
  const totalPct = total * 100;
  const cashRemainder = Math.max(0, 1 - total);

  // TASK-204: 매수 불가 자산 경고 — universe / weight / latestPrices /
  // initialCash 변동 시에만 재계산. 정수 주 자산만 평가 (CRYPTO 제외).
  const unbuyableAlerts = useMemo(
    () => computeUnbuyableAlerts(universe, value, latestPrices, initialCash),
    [universe, value, latestPrices, initialCash],
  );

  const hasCryptoInUniverse = useMemo(
    () => universe.some((a) => a.market === "CRYPTO"),
    [universe],
  );

  function setWeight(assetId: number, pct: number) {
    const clamped = clampPct(pct);
    const next = { ...value, [assetId]: clamped / 100 };
    onChange(next);
  }

  function distributeEvenly() {
    if (universe.length === 0) return;
    const each = 1 / universe.length;
    const next: Record<number, number> = {};
    universe.forEach((a) => {
      next[a.asset_id] = each;
    });
    onChange(next);
  }

  function clearAll() {
    onChange({});
  }

  function normalizeTo100() {
    if (total === 0) return;
    const factor = 1 / total;
    const next: Record<number, number> = {};
    universe.forEach((a) => {
      const current = value[a.asset_id] ?? 0;
      next[a.asset_id] = current * factor;
    });
    onChange(next);
  }

  if (universe.length === 0) {
    return (
      <div className="rounded border border-dashed border-gray-300 p-4 text-sm text-gray-500">
        먼저 위에서 자산(universe) 을 선택하세요. 선택된 자산별 비중을
        여기서 조정합니다.
      </div>
    );
  }

  const totalColor =
    Math.abs(totalPct - 100) < 0.5
      ? "text-green-700"
      : totalPct > 100
        ? "text-red-700"
        : "text-amber-700";

  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between border-b border-gray-200 pb-2">
        <span className="text-sm text-gray-600">자산별 목표 비중</span>
        <div className="flex flex-wrap gap-2">
          <Button
            type="button"
            size="sm"
            variant="ghost"
            onClick={distributeEvenly}
          >
            {ko.weight.distributeEvenly}
          </Button>
          <Button
            type="button"
            size="sm"
            variant="ghost"
            onClick={normalizeTo100}
            disabled={total === 0}
          >
            {ko.weight.normalize}
          </Button>
          <Button type="button" size="sm" variant="ghost" onClick={clearAll}>
            {ko.weight.reset}
          </Button>
        </div>
      </div>

      <div className="space-y-2">
        {universe.map((a) => {
          const w = value[a.asset_id] ?? 0;
          const pct = w * 100;
          const sliderId = `weight_slider_${a.asset_id}`;
          const numberId = `weight_number_${a.asset_id}`;
          return (
            <div key={a.asset_id} className="flex items-center gap-3">
              <div className="min-w-0 flex-1">
                <div className="flex items-center gap-2">
                  <span className="font-mono text-sm">{a.symbol}</span>
                  <Badge variant="secondary" className="text-xs">
                    {MARKET_LABEL[a.market]}
                  </Badge>
                  <span className="truncate text-sm text-gray-600">
                    {a.name}
                  </span>
                </div>
              </div>
              <input
                id={sliderId}
                type="range"
                min={0}
                max={100}
                step={1}
                value={pct}
                onChange={(e) => setWeight(a.asset_id, Number(e.target.value))}
                className="h-2 w-40 cursor-pointer appearance-none rounded bg-gray-200"
                aria-label={`${a.symbol} 비중 슬라이더`}
              />
              <div className="flex w-24 items-center gap-1">
                <Input
                  id={numberId}
                  type="number"
                  min={0}
                  max={100}
                  step={0.5}
                  value={pct.toFixed(1)}
                  onChange={(e) =>
                    setWeight(a.asset_id, Number(e.target.value))
                  }
                  className="text-right font-mono text-sm"
                  aria-label={`${a.symbol} 비중 (퍼센트)`}
                />
                <span className="text-xs text-gray-500">%</span>
              </div>
            </div>
          );
        })}
      </div>

      <div className="flex items-center justify-between border-t border-gray-200 pt-2">
        <span className="text-sm">{ko.weight.total}</span>
        <span className={`font-mono font-semibold ${totalColor}`}>
          {totalPct.toFixed(1)}%
        </span>
      </div>

      {allowCashSlot && totalPct < 99.5 && (
        <div className="rounded border border-amber-200 bg-amber-50 p-2 text-xs text-amber-800">
          {ko.weight.cashRemainder} {(cashRemainder * 100).toFixed(1)}% 는
          기축통화 현금(_CASH_) 슬리브로 자동 배분됩니다.
        </div>
      )}
      {totalPct > 100.5 && (
        <div className="rounded border border-red-200 bg-red-50 p-2 text-xs text-red-800">
          {ko.weight.exceeds100}. &quot;{ko.weight.normalize}&quot; 버튼으로
          자동 조정하세요.
        </div>
      )}

      {/* TASK-204: 매수 불가 자산 경고 (정수 주 자산 한정).
          사용자 첫 시도 사고(BTC 100% × $10k 초기 자본 → 0개 체결 →
          equity 평탄선) 재현 방지. 코인은 fractional 매매 가능 라벨로 별도 안내. */}
      {unbuyableAlerts.length > 0 && (
        <div className="rounded border border-amber-200 bg-amber-50 p-3 text-xs text-amber-800">
          <p className="mb-2 font-semibold">
            {ko.unbuyable.title}
          </p>
          <ul className="space-y-1">
            {unbuyableAlerts.map((alert) => (
              <li key={alert.asset_id}>
                <span className="font-mono">{alert.symbol}</span>
                {" 1주 ≈ "}
                <span className="font-mono">
                  {formatPrice(alert.pricePerShare, alert.currency)}
                </span>
                {" — 비중 "}
                <span className="font-mono">{(alert.weight * 100).toFixed(1)}%</span>
                {" × 초기 자본 "}
                <span className="font-mono">
                  {baseCurrency
                    ? formatPrice(initialCash ?? 0, baseCurrency)
                    : (initialCash ?? 0).toLocaleString("en-US")}
                </span>
                {" = "}
                <span className="font-mono">
                  {baseCurrency
                    ? formatPrice(alert.targetCash, baseCurrency)
                    : alert.targetCash.toLocaleString("en-US", {
                        maximumFractionDigits: 2,
                      })}
                </span>
                {" 로는 1주도 매수 불가."}
              </li>
            ))}
          </ul>
          <p className="mt-2">{ko.unbuyable.actionHint}</p>
        </div>
      )}

      {/* TASK-204: 코인이 universe 에 포함된 경우 fractional 가능 안내
          (경고가 아니라 정보성 — 사용자가 코인에 대해서도 경고를 기대했다가
          왜 안 뜨는지 의아해하는 상황 방지). */}
      {hasCryptoInUniverse && (
        <div className="rounded border border-blue-200 bg-blue-50 p-2 text-xs text-blue-800">
          {ko.unbuyable.cryptoOk}
        </div>
      )}
    </div>
  );
}
