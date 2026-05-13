/**
 * NormalizedPriceChart — 단위 테스트 (TASK-308 DoD).
 *
 * 검증 영역:
 *   1. members 가 비어있을 때 안내 문구 렌더 (early return).
 *   2. members 가 2종이면 recharts `<Line>` 이 2개 (다중 라인).
 *   3. 정렬·병합 헬퍼 `mergeMembers` 가 시간순 union/merge 를 정확히 반환.
 *
 * recharts ResponsiveContainer 는 jsdom 에서 ResizeObserver 가 없어
 * crash 하므로 noop polyfill 을 주입. recharts 내부는 부모 width 가 0 이어도
 * `<Line>` `<Legend>` 같은 자식 component 를 정상적으로 mount 하므로
 * 라인/범례 개수는 안정적으로 셀 수 있다.
 */
import * as React from "react";
import { describe, it, expect, afterEach, beforeAll, vi } from "vitest";
import { render, cleanup } from "@testing-library/react";

beforeAll(() => {
  if (typeof globalThis.ResizeObserver === "undefined") {
    class RO {
      observe() {}
      unobserve() {}
      disconnect() {}
    }
    (globalThis as unknown as { ResizeObserver: typeof RO }).ResizeObserver = RO;
  }
});

// ResponsiveContainer 는 부모 width=0 일 때 자식 SVG 를 렌더하지 않는다.
// 고정 width/height 박스로 stub 하여 LineChart 의 path/legend 계산을 활성화.
vi.mock("recharts", async () => {
  const actual = await vi.importActual<typeof import("recharts")>("recharts");
  const Stub: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const child = React.Children.only(children) as React.ReactElement;
    return React.cloneElement(child, { width: 800, height: 320 });
  };
  return { ...actual, ResponsiveContainer: Stub };
});

afterEach(() => {
  cleanup();
});

import {
  NormalizedPriceChart,
  mergeMembers,
} from "@/components/themes/charts/NormalizedPriceChart";

describe("mergeMembers", () => {
  it("두 자산의 시계열을 time 기준으로 union/merge", () => {
    const merged = mergeMembers({
      "101": [
        { time: "2024-01-02", value: 100 },
        { time: "2024-01-03", value: 105 },
      ],
      "102": [
        { time: "2024-01-02", value: 100 },
        { time: "2024-01-03", value: 98 },
        { time: "2024-01-04", value: 99 },
      ],
    });

    expect(merged).toHaveLength(3);
    expect(merged[0]).toEqual({ time: "2024-01-02", "101": 100, "102": 100 });
    expect(merged[1]).toEqual({ time: "2024-01-03", "101": 105, "102": 98 });
    // 101 은 2024-01-04 에 없음 → 키 부재.
    expect(merged[2].time).toBe("2024-01-04");
    expect(merged[2]["101"]).toBeUndefined();
    expect(merged[2]["102"]).toBe(99);
  });

  it("빈 입력은 빈 배열", () => {
    expect(mergeMembers({})).toEqual([]);
  });
});

describe("NormalizedPriceChart", () => {
  it("members 가 비어있으면 안내 메시지 렌더", () => {
    const { container } = render(<NormalizedPriceChart members={{}} />);
    expect(container.textContent).toContain("표시할 멤버 데이터가 없습니다");
  });

  it("members 2 시리즈 → recharts Line 2개 + 범례 2개", () => {
    const { container } = render(
      <NormalizedPriceChart
        members={{
          "101": [
            { time: "2024-01-02", value: 100 },
            { time: "2024-01-03", value: 105 },
          ],
          "102": [
            { time: "2024-01-02", value: 100 },
            { time: "2024-01-03", value: 98 },
          ],
        }}
        labels={{ "101": "삼성전자", "102": "SK하이닉스" }}
      />,
    );

    // recharts <Line> 는 SVG `.recharts-line` 클래스를 발행한다.
    const lines = container.querySelectorAll(".recharts-line");
    expect(lines.length).toBe(2);

    // Legend 의 항목 (recharts-legend-item) 도 2개.
    const legendItems = container.querySelectorAll(".recharts-legend-item");
    expect(legendItems.length).toBe(2);

    // 라벨 mapping — 범례 텍스트에 한글 자산명이 등장.
    expect(container.textContent).toContain("삼성전자");
    expect(container.textContent).toContain("SK하이닉스");
  });
});
