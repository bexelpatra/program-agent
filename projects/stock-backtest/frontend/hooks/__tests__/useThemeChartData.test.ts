/**
 * useThemeChartData — 단위 테스트 (TASK-308 DoD).
 *
 * 검증 영역:
 *   1. mount 시 loading=true → 응답 도착 시 data 채워지고 loading=false.
 *   2. api 실패 시 ApiError 가 error 상태로 노출 + data=null 유지.
 *   3. opts 변경 (start 날짜) → 재호출되어 새로운 data 로 갱신.
 *
 * api.getThemeChart 는 모듈 모킹 (vi.mock) 으로 deterministic 응답 주입.
 */
import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { renderHook, act, waitFor } from "@testing-library/react";

// vi.mock 은 사용 전에 hoist 되므로 import 순서 무관.
vi.mock("@/lib/api/client", () => {
  const ApiError = class extends Error {
    constructor(
      public status: number,
      public stage: string,
      public type: string,
      message: string,
      public traceId: string,
      public requestCtx: Record<string, unknown>,
    ) {
      super(message);
      this.name = "ApiError";
    }
  };
  return {
    api: {
      getThemeChart: vi.fn(),
    },
    ApiError,
  };
});

import { api, ApiError } from "@/lib/api/client";
import { useThemeChartData } from "@/hooks/useThemeChartData";

const mockGetThemeChart = api.getThemeChart as unknown as ReturnType<
  typeof vi.fn
>;

const sampleResponse = {
  members: {
    "101": [
      { time: "2024-01-02", value: 100 },
      { time: "2024-01-03", value: 105 },
    ],
  },
  aggregate: [
    { time: "2024-01-02", value: 100 },
    { time: "2024-01-03", value: 105 },
  ],
  universe_meta: {
    adjusted_start: "2024-01-02",
    adjusted_end: "2024-01-03",
    affected_assets: [],
    reason: "ok" as const,
    message: "",
  },
};

describe("useThemeChartData", () => {
  beforeEach(() => {
    mockGetThemeChart.mockReset();
  });

  afterEach(() => {
    vi.clearAllMocks();
  });

  it("mount 시 loading=true → data 도착 후 loading=false", async () => {
    let resolveFn: (v: typeof sampleResponse) => void = () => {};
    mockGetThemeChart.mockReturnValue(
      new Promise<typeof sampleResponse>((res) => {
        resolveFn = res;
      }),
    );

    const { result } = renderHook(() =>
      useThemeChartData(7, { normalize: "base100", weighting: "equal" }),
    );

    // 첫 effect 가 동기적으로 setState(loading=true) 호출 — React 가 commit
    // 한 뒤에 visible. async act 로 flush.
    await waitFor(() => expect(result.current.loading).toBe(true));
    expect(result.current.data).toBeNull();
    expect(result.current.error).toBeNull();

    await act(async () => {
      resolveFn(sampleResponse);
    });

    await waitFor(() => expect(result.current.loading).toBe(false));
    expect(result.current.data).toEqual(sampleResponse);
    expect(result.current.error).toBeNull();
    expect(mockGetThemeChart).toHaveBeenCalledTimes(1);
    expect(mockGetThemeChart).toHaveBeenCalledWith(7, {
      normalize: "base100",
      weighting: "equal",
      start: undefined,
      end: undefined,
      baseCurrency: undefined,
    });
  });

  it("api 실패 시 error 상태로 노출되고 data 는 null 유지", async () => {
    const apiErr = new ApiError(
      500,
      "data",
      "InternalError",
      "boom",
      "trace-xyz",
      {},
    );
    mockGetThemeChart.mockRejectedValueOnce(apiErr);

    const { result } = renderHook(() =>
      useThemeChartData(7, { normalize: "base100", weighting: "equal" }),
    );

    await waitFor(() => expect(result.current.loading).toBe(false));
    expect(result.current.error).toBe(apiErr);
    expect(result.current.data).toBeNull();
  });

  it("opts 변경 시 재호출되어 새로운 응답으로 갱신", async () => {
    mockGetThemeChart.mockResolvedValue(sampleResponse);

    const { result, rerender } = renderHook(
      ({ start }: { start?: string }) =>
        useThemeChartData(7, {
          normalize: "base100",
          weighting: "equal",
          start,
        }),
      { initialProps: { start: undefined as string | undefined } },
    );

    await waitFor(() => expect(result.current.loading).toBe(false));
    expect(mockGetThemeChart).toHaveBeenCalledTimes(1);

    const second = {
      ...sampleResponse,
      aggregate: [{ time: "2024-02-01", value: 110 }],
    };
    mockGetThemeChart.mockResolvedValue(second);

    rerender({ start: "2024-02-01" });

    await waitFor(() => expect(mockGetThemeChart).toHaveBeenCalledTimes(2));
    await waitFor(() =>
      expect(result.current.data?.aggregate[0].value).toBe(110),
    );
    expect(mockGetThemeChart).toHaveBeenLastCalledWith(7, {
      normalize: "base100",
      weighting: "equal",
      start: "2024-02-01",
      end: undefined,
      baseCurrency: undefined,
    });
  });
});
