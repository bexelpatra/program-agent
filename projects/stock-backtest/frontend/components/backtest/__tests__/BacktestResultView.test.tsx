/**
 * BacktestResultView — 단위 테스트 (TASK-237 DoD).
 *
 * 검증 영역:
 *   1. layout='compact' / 'full' 두 케이스가 동일 결과 mock 으로 안정
 *      snapshot 을 생성한다 (회귀 detector).
 *   2. logScale 토글 prop 전달 — onLogScaleChange 가 현재값의 부정으로
 *      호출되는지.
 *
 * recharts (EquityChart / DrawdownChart 내부) 와 MonthlyHeatmap 의 SVG
 * 출력은 jsdom 의 layout 미지원으로 무의미한 0px 박스를 만들 뿐이라,
 * snapshot 안정성을 위해 시각화 자식 컴포넌트를 가벼운 stub 으로
 * 대체한다. 본 컴포넌트가 검증해야 하는 것은 "5개 시각화 슬롯 + 카드
 * 래퍼 + layout 별 grid 배치" 이지, 차트 라이브러리 출력 자체가 아님.
 */
import { describe, it, expect, vi, afterEach } from "vitest";
import { render, screen, fireEvent, cleanup } from "@testing-library/react";

// vitest config 의 globals=false 환경에서는 @testing-library/react 의
// 자동 afterEach cleanup 이 등록되지 않는다 (라이브러리가 globalThis.
// afterEach 를 찾지 못하면 skip). 누적된 DOM 으로 인해 동일 testid 가
// 다음 테스트에서 중복 매칭되므로 명시적으로 등록한다.
afterEach(() => {
  cleanup();
});

import type { BacktestResult } from "@/lib/api/types";

vi.mock("@/components/backtest/EquityChart", () => ({
  EquityChart: ({ logScale }: { logScale: boolean }) => (
    <div data-testid="equity-chart" data-logscale={String(logScale)} />
  ),
}));
vi.mock("@/components/backtest/DrawdownChart", () => ({
  DrawdownChart: () => <div data-testid="drawdown-chart" />,
}));
vi.mock("@/components/backtest/MetricsTable", () => ({
  MetricsTable: () => <div data-testid="metrics-table" />,
}));
vi.mock("@/components/backtest/MonthlyHeatmap", () => ({
  MonthlyHeatmap: () => <div data-testid="monthly-heatmap" />,
}));
vi.mock("@/components/backtest/TradesTable", () => ({
  TradesTable: () => <div data-testid="trades-table" />,
}));

import { BacktestResultView } from "@/components/backtest/BacktestResultView";

const fixture: BacktestResult = {
  run: {
    run_id: 42,
    run_hash: "abc123",
    status: "done",
    progress: 1,
    name: "테스트 런",
    strategy_name: "fixed_weight",
    period_start: "2020-01-01",
    period_end: "2024-12-31",
    base_currency: "KRW",
    created_at: "2024-01-01T00:00:00Z",
    started_at: "2024-01-01T00:00:00Z",
    finished_at: "2024-01-01T00:01:00Z",
    error: null,
  },
  equity_curve: [
    { time: "2020-01-01", equity: 1_000_000, cash: 1_000_000, drawdown: 0 },
    { time: "2024-12-31", equity: 1_500_000, cash: 0, drawdown: -0.05 },
  ],
  trades: [
    {
      time: "2020-01-02",
      asset_id: 1,
      side: "BUY",
      qty: 10,
      price: 100,
      commission: 0.5,
      currency: "KRW",
    },
  ],
  metrics: {
    cagr: 0.0845,
    mdd: -0.12,
    sharpe: 1.1,
    sortino: 1.4,
    calmar: 0.7,
    win_rate: 0.6,
    annual_returns: { "2020": 0.1, "2024": 0.08 },
    monthly_returns: { "2020-01": 0.02, "2024-12": -0.01 },
  },
};

describe("BacktestResultView", () => {
  it("layout='compact' 가 5개 시각화 슬롯 모두를 단일 컬럼 stack 으로 렌더한다", () => {
    const { container } = render(
      <BacktestResultView
        result={fixture}
        logScale={false}
        onLogScaleChange={() => {}}
        layout="compact"
      />,
    );

    expect(screen.getByTestId("equity-chart")).toBeTruthy();
    expect(screen.getByTestId("drawdown-chart")).toBeTruthy();
    expect(screen.getByTestId("metrics-table")).toBeTruthy();
    expect(screen.getByTestId("monthly-heatmap")).toBeTruthy();
    expect(screen.getByTestId("trades-table")).toBeTruthy();

    // compact 는 grid (md:grid-cols-2) 가 없어야 한다 — 자본곡선/낙폭이
    // 좌우 병치되지 않는 단일 컬럼 stack 임을 보장.
    expect(container.querySelector(".md\\:grid-cols-2")).toBeNull();
    expect(container.firstChild).toMatchSnapshot();
  });

  it("layout='full' 이 자본곡선/낙폭만 md:grid-cols-2 로 병치한다", () => {
    const { container } = render(
      <BacktestResultView
        result={fixture}
        logScale={false}
        onLogScaleChange={() => {}}
        layout="full"
      />,
    );

    expect(container.querySelector(".md\\:grid-cols-2")).not.toBeNull();
    expect(screen.getByTestId("equity-chart")).toBeTruthy();
    expect(screen.getByTestId("drawdown-chart")).toBeTruthy();
    expect(screen.getByTestId("metrics-table")).toBeTruthy();
    expect(screen.getByTestId("monthly-heatmap")).toBeTruthy();
    expect(screen.getByTestId("trades-table")).toBeTruthy();
    expect(container.firstChild).toMatchSnapshot();
  });

  it("logScale 토글 버튼 클릭 시 onLogScaleChange 가 부정값으로 호출된다", () => {
    const onLogScaleChange = vi.fn();
    render(
      <BacktestResultView
        result={fixture}
        logScale={false}
        onLogScaleChange={onLogScaleChange}
        layout="full"
      />,
    );

    fireEvent.click(screen.getByRole("button", { name: "로그" }));
    expect(onLogScaleChange).toHaveBeenCalledWith(true);
  });

  it("metrics 가 null 이어도 fallback 카드를 렌더하고 monthly heatmap 은 숨긴다", () => {
    const noMetrics: BacktestResult = { ...fixture, metrics: null };
    render(
      <BacktestResultView
        result={noMetrics}
        logScale={false}
        onLogScaleChange={() => {}}
        layout="full"
      />,
    );

    expect(screen.queryByTestId("metrics-table")).toBeNull();
    expect(screen.queryByTestId("monthly-heatmap")).toBeNull();
    expect(screen.getByText(/성과 지표를 계산하지 못했습니다/)).toBeTruthy();
  });
});
