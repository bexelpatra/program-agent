"use client";

/**
 * TradesTable — paginated, currency-grouped trade log.
 *
 * architecture.md V3 § UI/UX 원칙 4 — "거래 내역 테이블 + 통화 그룹".
 * `price` / `commission` 은 native currency (KRW, USD, ...) 이므로
 * 통화별 필터를 제공해 잘못된 비교를 막는다.
 *
 * 페이지 사이즈는 20 — 백테스트 한 번에 수백 건 단위 거래가 흔하니
 * 한 화면에 다 띄우면 무겁다. 페이지네이션은 클라이언트 슬라이스
 * (서버 round-trip 없음).
 */
import { useMemo, useState } from "react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import type { TradeRecord } from "@/lib/api/schemas";

interface TradesTableProps {
  trades: TradeRecord[];
}

const PAGE_SIZE = 20;

export function TradesTable({ trades }: TradesTableProps) {
  const [page, setPage] = useState(0);
  const [currencyFilter, setCurrencyFilter] = useState<string>("all");

  const currencies = useMemo(
    () => Array.from(new Set(trades.map((t) => t.currency))).sort(),
    [trades],
  );

  const filtered = useMemo(
    () =>
      currencyFilter === "all"
        ? trades
        : trades.filter((t) => t.currency === currencyFilter),
    [trades, currencyFilter],
  );

  const pages = Math.max(1, Math.ceil(filtered.length / PAGE_SIZE));
  const safePage = Math.min(page, pages - 1);
  const slice = filtered.slice(safePage * PAGE_SIZE, (safePage + 1) * PAGE_SIZE);

  function selectCurrency(c: string) {
    setCurrencyFilter(c);
    setPage(0);
  }

  return (
    <div>
      <div className="flex flex-wrap items-center gap-2 border-b p-3">
        <span className="text-sm text-gray-600">통화:</span>
        <Button
          variant={currencyFilter === "all" ? "default" : "ghost"}
          size="sm"
          onClick={() => selectCurrency("all")}
        >
          전체
        </Button>
        {currencies.map((c) => (
          <Button
            key={c}
            variant={currencyFilter === c ? "default" : "ghost"}
            size="sm"
            onClick={() => selectCurrency(c)}
          >
            {c}
          </Button>
        ))}
      </div>
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead className="bg-gray-50">
            <tr className="text-gray-600">
              <th className="p-2 text-left font-medium">시각</th>
              <th className="p-2 text-left font-medium">자산</th>
              <th className="p-2 text-left font-medium">방향</th>
              <th className="p-2 text-right font-medium">수량</th>
              <th className="p-2 text-right font-medium">가격</th>
              <th className="p-2 text-right font-medium">수수료</th>
              <th className="p-2 text-left font-medium">통화</th>
            </tr>
          </thead>
          <tbody>
            {slice.map((t, i) => (
              <tr
                key={`${t.time}-${t.asset_id}-${i}`}
                className="border-b last:border-0"
              >
                <td className="p-2 font-mono text-xs">{t.time}</td>
                <td className="p-2 font-mono">#{t.asset_id}</td>
                <td className="p-2">
                  <Badge
                    variant={t.side === "BUY" ? "default" : "secondary"}
                  >
                    {t.side}
                  </Badge>
                </td>
                <td className="p-2 text-right font-mono">{t.qty}</td>
                <td className="p-2 text-right font-mono">
                  {t.price.toFixed(2)}
                </td>
                <td className="p-2 text-right font-mono text-gray-500">
                  {t.commission.toFixed(2)}
                </td>
                <td className="p-2">{t.currency}</td>
              </tr>
            ))}
            {slice.length === 0 && (
              <tr>
                <td
                  colSpan={7}
                  className="p-4 text-center text-sm text-gray-500"
                >
                  거래 내역이 없습니다.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
      {pages > 1 && (
        <div className="flex items-center justify-between border-t p-3 text-sm">
          <span className="text-gray-600">
            총 {filtered.length}건 — 페이지 {safePage + 1} / {pages}
          </span>
          <div className="flex gap-1">
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setPage(Math.max(0, safePage - 1))}
              disabled={safePage === 0}
            >
              이전
            </Button>
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setPage(Math.min(pages - 1, safePage + 1))}
              disabled={safePage >= pages - 1}
            >
              다음
            </Button>
          </div>
        </div>
      )}
    </div>
  );
}
