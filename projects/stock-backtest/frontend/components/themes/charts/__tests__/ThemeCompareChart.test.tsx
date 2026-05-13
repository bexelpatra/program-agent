/**
 * ThemeCompareChart — 단위 테스트 (TASK-308 DoD).
 *
 * 검증 영역:
 *   1. themes 가 비어있을 때 안내 메시지 (early return).
 *   2. themes 2개 → recharts `<Line>` 2개 + 범례 2개. tooltip 에 사용되는
 *      이름 매핑이 한국어로 표기되는지 본문에서 확인.
 *   3. `mergeThemes` 헬퍼: 시간 union/merge + 정렬 검증.
 *
 * NormalizedPriceChart.test.tsx 와 동일한 ResizeObserver polyfill +
 * ResponsiveContainer stub 패턴을 사용 (jsdom 의 layout 부재 우회).
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
  ThemeCompareChart,
  mergeThemes,
} from "@/components/themes/charts/ThemeCompareChart";

describe("mergeThemes", () => {
  it("두 테마의 aggregate 를 time 기준으로 union/merge + 정렬", () => {
    const merged = mergeThemes({
      "1": {
        name: "정치 A",
        aggregate: [
          { time: "2024-02-01", value: 102 },
          { time: "2024-01-02", value: 100 },
        ],
      },
      "2": {
        name: "정치 B",
        aggregate: [
          { time: "2024-01-02", value: 100 },
          { time: "2024-02-01", value: 98 },
        ],
      },
    });
    expect(merged).toHaveLength(2);
    expect(merged[0].time).toBe("2024-01-02");
    expect(merged[1].time).toBe("2024-02-01");
    expect(merged[0]["1"]).toBe(100);
    expect(merged[1]["2"]).toBe(98);
  });
});

describe("ThemeCompareChart", () => {
  it("themes 비어있으면 안내 메시지 렌더", () => {
    const { container } = render(<ThemeCompareChart themes={{}} />);
    expect(container.textContent).toContain("비교할 테마를 1개 이상");
  });

  it("themes 2개 → recharts Line 2개 + 범례 2개 (테마 이름 표시)", () => {
    const { container } = render(
      <ThemeCompareChart
        themes={{
          "1": {
            name: "정치 A",
            aggregate: [
              { time: "2024-01-02", value: 100 },
              { time: "2024-01-03", value: 102 },
            ],
          },
          "2": {
            name: "정치 B",
            aggregate: [
              { time: "2024-01-02", value: 100 },
              { time: "2024-01-03", value: 98 },
            ],
          },
        }}
      />,
    );

    const lines = container.querySelectorAll(".recharts-line");
    expect(lines.length).toBe(2);

    const legendItems = container.querySelectorAll(".recharts-legend-item");
    expect(legendItems.length).toBe(2);

    // 범례에 테마 한글 이름이 노출.
    expect(container.textContent).toContain("정치 A");
    expect(container.textContent).toContain("정치 B");
  });
});
