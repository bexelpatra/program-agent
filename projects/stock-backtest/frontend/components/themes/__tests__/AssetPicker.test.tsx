/**
 * AssetPicker — 단위 테스트 (TASK-307 DoD #3).
 *
 * 검증 영역:
 *   1. 마운트 시점에는 결과 영역이 없다 (검색 전에는 빈 영역).
 *   2. 검색 버튼 → api.listAssets 호출, 결과 행 클릭 → onSelectedChange
 *      가 1개 자산 배열로 호출됨.
 *   3. excludeAssetIds 에 포함된 자산은 disabled (이미 추가됨 안내) +
 *      클릭해도 onSelectedChange 호출되지 않음.
 *
 * api.listAssets 는 vi.mock 으로 부분 대체. ToastProvider 래핑 필수
 * (AssetPicker 가 에러 토스트 발생 시 useToast 를 호출).
 */
import { describe, it, expect, vi, afterEach, beforeEach } from "vitest";
import {
  render,
  screen,
  fireEvent,
  cleanup,
  waitFor,
} from "@testing-library/react";

afterEach(() => {
  cleanup();
  vi.clearAllMocks();
});

vi.mock("@/lib/api/client", async () => {
  const actual = await vi.importActual<typeof import("@/lib/api/client")>(
    "@/lib/api/client",
  );
  return {
    ...actual,
    api: {
      listAssets: vi.fn(),
    },
  };
});

import { api } from "@/lib/api/client";
import { ToastProvider } from "@/components/ui/toast";
import { AssetPicker } from "@/components/themes/AssetPicker";
import type { Asset } from "@/lib/api/types";

const ASSETS: Asset[] = [
  {
    asset_id: 101,
    symbol: "VTI",
    market: "US",
    asset_type: "ETF",
    currency: "USD",
    name: "Vanguard 토탈 마켓",
    active: true,
  },
  {
    asset_id: 102,
    symbol: "069500",
    market: "KR",
    asset_type: "ETF",
    currency: "KRW",
    name: "KODEX 200",
    active: true,
  },
];

function renderPicker(props: {
  selected?: Asset[];
  excludeAssetIds?: number[];
}) {
  const onSelectedChange = vi.fn();
  const utils = render(
    <ToastProvider>
      <AssetPicker
        selected={props.selected ?? []}
        onSelectedChange={onSelectedChange}
        excludeAssetIds={props.excludeAssetIds ?? []}
      />
    </ToastProvider>,
  );
  return { ...utils, onSelectedChange };
}

describe("AssetPicker", () => {
  beforeEach(() => {
    (api.listAssets as ReturnType<typeof vi.fn>).mockResolvedValue({
      items: ASSETS,
      total: 2,
      page: 1,
      page_size: 25,
    });
  });

  it("마운트 시점에는 결과 영역 미렌더", () => {
    renderPicker({});
    expect(screen.queryByTestId("asset-picker-results")).toBeNull();
  });

  it("검색 후 행 클릭 → api.listAssets 호출 + onSelectedChange 1건", async () => {
    const { onSelectedChange } = renderPicker({});

    fireEvent.click(screen.getByRole("button", { name: /^검색$/ }));

    await waitFor(() => {
      expect(api.listAssets).toHaveBeenCalledTimes(1);
    });
    await waitFor(() => {
      expect(screen.getByTestId("asset-picker-results")).toBeTruthy();
    });

    fireEvent.click(screen.getByTestId("asset-picker-row-101"));
    expect(onSelectedChange).toHaveBeenCalledTimes(1);
    const arg = onSelectedChange.mock.calls[0][0];
    expect(arg).toHaveLength(1);
    expect(arg[0]).toMatchObject({ asset_id: 101, symbol: "VTI" });
  });

  it("excludeAssetIds 포함 자산 → disabled + onSelectedChange 미호출", async () => {
    const { onSelectedChange } = renderPicker({ excludeAssetIds: [102] });

    fireEvent.click(screen.getByRole("button", { name: /^검색$/ }));

    await waitFor(() => {
      expect(api.listAssets).toHaveBeenCalledTimes(1);
    });

    const row = (await screen.findByTestId(
      "asset-picker-row-102",
    )) as HTMLButtonElement;
    expect(row.disabled).toBe(true);

    fireEvent.click(row);
    expect(onSelectedChange).not.toHaveBeenCalled();
  });
});
