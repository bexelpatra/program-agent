/**
 * AssetTable — read-only tabular view of registered assets.
 *
 * Pure presentational component. Receives the already-fetched asset
 * list from the parent page and renders the standard catalogue columns
 * (symbol / market / type / currency / name / start_date).
 *
 * Empty-state copy follows UI/UX 원칙 2 (한국어, 액션 가이드 형태):
 * tells the user how to add their first asset rather than rendering an
 * empty table.
 */
import { api } from "@/lib/api/client";
import { Badge } from "@/components/ui/badge";
import { ko } from "@/lib/i18n/ko";

// Derive the row type from the API client's actual return type rather
// than `z.infer<AssetSchema>`. Reason: `AssetSchema.meta` uses
// `.default({})`, which makes the Zod **input** type optional but the
// **output** type required. `z.array(AssetSchema).parse(...)` in this
// project's Zod version surfaces the input variance for nested
// elements, so widening to whatever `listAssets()` actually returns
// keeps state, props, and call-site types aligned.
export type AssetRow = Awaited<
  ReturnType<typeof api.listAssets>
>["items"][number];

const MARKET_VARIANT: Record<string, "default" | "secondary"> = {
  KR: "default",
  US: "secondary",
  CRYPTO: "default",
};

export function AssetTable({ items }: { items: AssetRow[] }) {
  if (items.length === 0) {
    return (
      <div className="p-8 text-center text-gray-500">
        등록된 자산이 없습니다. 우측 상단 &quot;{ko.asset.add}&quot; 버튼으로
        추가하세요.
      </div>
    );
  }
  return (
    <table className="w-full text-left">
      <thead className="border-b bg-gray-50">
        <tr>
          <th className="p-3 text-sm font-medium text-gray-600">심볼</th>
          <th className="p-3 text-sm font-medium text-gray-600">시장</th>
          <th className="p-3 text-sm font-medium text-gray-600">종류</th>
          <th className="p-3 text-sm font-medium text-gray-600">통화</th>
          <th className="p-3 text-sm font-medium text-gray-600">이름</th>
          <th className="p-3 text-sm font-medium text-gray-600">데이터 시작일</th>
        </tr>
      </thead>
      <tbody>
        {items.map((a) => (
          <tr
            key={a.asset_id}
            className="border-b last:border-0 hover:bg-gray-50"
          >
            <td className="p-3 font-mono text-sm">{a.symbol}</td>
            <td className="p-3">
              <Badge variant={MARKET_VARIANT[a.market]}>
                {ko.asset.market[a.market as keyof typeof ko.asset.market]}
              </Badge>
            </td>
            <td className="p-3 text-sm text-gray-600">{a.asset_type}</td>
            <td className="p-3 text-sm">{a.currency}</td>
            <td className="p-3">{a.name}</td>
            <td className="p-3 text-sm text-gray-500">{a.start_date || "-"}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
