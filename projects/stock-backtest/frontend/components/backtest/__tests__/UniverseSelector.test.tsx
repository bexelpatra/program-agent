/**
 * UniverseSelector — TASK-311 단위 테스트.
 *
 * 검증 영역 (C5 후속, 생존편향 경고 토스트):
 *   1. STOCK 자산 (Phase 2 테마주 트랙) 을 universe 에 추가하면
 *      `warning.survivorshipBias` 토스트가 정확히 1회 호출된다.
 *   2. ETF / EQUITY_INDEX 등 비-STOCK 자산만 추가하면 토스트는
 *      호출되지 않는다 (0건).
 *
 * 구현 패턴 — `api.listAssets` 와 `useToast` 를 vi.mock 으로 대체.
 * AssetPicker 테스트 (`themes/__tests__/AssetPicker.test.tsx`) 패턴과
 * 동일. ToastProvider 래핑은 불필요 (useToast 자체를 mock).
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
    api: { listAssets: vi.fn() },
  };
});

const toastSpy = vi.fn();
vi.mock("@/components/ui/toast", () => ({
  // UniverseSelector 는 `useToast()` 의 `.toast` 만 사용한다.
  useToast: () => ({ toast: toastSpy, dismiss: vi.fn(), toasts: [] }),
}));

import { api } from "@/lib/api/client";
import { UniverseSelector } from "@/components/backtest/UniverseSelector";
import type { Asset } from "@/lib/api/types";

const STOCK_ASSET: Asset = {
  asset_id: 201,
  symbol: "005930",
  market: "KR",
  asset_type: "STOCK",
  currency: "KRW",
  name: "삼성전자",
  active: true,
};

const ETF_ASSET: Asset = {
  asset_id: 101,
  symbol: "069500",
  market: "KR",
  asset_type: "ETF",
  currency: "KRW",
  name: "KODEX 200",
  active: true,
};

const INDEX_ASSET: Asset = {
  asset_id: 102,
  symbol: "^GSPC",
  market: "US",
  asset_type: "EQUITY_INDEX",
  currency: "USD",
  name: "S&P 500",
  active: true,
};

function renderSelector(
  searchResults: Asset[],
  initial: Asset[] = [],
) {
  (api.listAssets as ReturnType<typeof vi.fn>).mockResolvedValue({
    items: searchResults,
    total: searchResults.length,
    page: 1,
    page_size: 20,
  });
  const onChange = vi.fn();
  const utils = render(
    <UniverseSelector value={initial} onChange={onChange} />,
  );
  return { ...utils, onChange };
}

describe("UniverseSelector — TASK-311 생존편향 경고", () => {
  beforeEach(() => {
    toastSpy.mockClear();
  });

  it("STOCK 자산을 선택하면 warning.survivorshipBias 토스트가 1회 호출된다", async () => {
    renderSelector([STOCK_ASSET]);

    fireEvent.click(screen.getByRole("button", { name: "검색" }));
    // 검색 결과 행 (button) 이 렌더될 때까지 대기.
    const row = await waitFor(() =>
      screen.getByRole("button", { name: /삼성전자/ }),
    );
    fireEvent.click(row);

    expect(toastSpy).toHaveBeenCalledTimes(1);
    expect(toastSpy).toHaveBeenCalledWith(
      expect.objectContaining({
        title: expect.stringContaining("생존편향"),
        variant: "destructive",
      }),
    );
  });

  it("ETF / EQUITY_INDEX 만 선택하면 토스트가 호출되지 않는다 (0건)", async () => {
    renderSelector([ETF_ASSET, INDEX_ASSET]);

    fireEvent.click(screen.getByRole("button", { name: "검색" }));
    const etfRow = await waitFor(() =>
      screen.getByRole("button", { name: /KODEX 200/ }),
    );
    fireEvent.click(etfRow);
    const indexRow = screen.getByRole("button", { name: /S&P 500/ });
    fireEvent.click(indexRow);

    expect(toastSpy).not.toHaveBeenCalled();
  });
});
