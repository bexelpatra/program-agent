"use client";

/**
 * useBacktestPolling — TASK-094 폴링 훅.
 *
 * 책임 1개: GET /api/backtests/{run_id} 를 1초 간격으로 폴링하다가
 * status 가 terminal (done/failed/cancelled) 이 되면 자동 정지.
 * 호출부는 `runId` 를 setState 로 흘려보내기만 하면 된다.
 *
 * 클린 아키텍처:
 *   - presentation 레이어 (ProgressPanel.tsx, /backtests/new) 가
 *     사용. domain/data 로 import 되지 않는다.
 *   - 폴링 cadence (1s) · terminal 분기 · cancel 트리거 같은 reactive
 *     상태 머신을 ProgressPanel 에서 떼어내, 패널은 순수 표현 컴포넌트로
 *     유지한다 (Single Responsibility).
 *
 * 정리 (cleanup) 보장:
 *   - effect 내 `cancelled` 플래그 + clearTimeout 으로 unmount /
 *     runId 변경 시 in-flight tick 을 안전하게 끊는다.
 *   - 컴포넌트가 사라진 뒤에도 setState 가 호출되지 않도록 모든
 *     setState 앞에 cancelled 가드를 둔다.
 */
import { useCallback, useEffect, useState } from "react";

import { api, ApiError } from "@/lib/api/client";
import type { BacktestRun, BacktestStatus } from "@/lib/api/schemas";

/** 한 번의 fetch 사이클 결과를 그대로 보존. */
export interface BacktestPollState {
  run: BacktestRun | null;
  loading: boolean;
  error: ApiError | null;
}

const POLL_INTERVAL_MS = 1000;
const TERMINAL_STATUSES: ReadonlySet<BacktestStatus> = new Set<BacktestStatus>([
  "done",
  "failed",
  "cancelled",
]);

export interface UseBacktestPollingResult extends BacktestPollState {
  /** UI 의 "취소" 버튼이 호출. 실패해도 throw 하지 않음 (다음 tick 이 상태 반영). */
  cancelRun: () => Promise<void>;
}

/**
 * @param runId  null 이면 폴링하지 않음 (폼 모드일 때).
 *               숫자가 들어오면 즉시 첫 tick + 이후 1s 간격.
 */
export function useBacktestPolling(
  runId: number | null,
): UseBacktestPollingResult {
  const [state, setState] = useState<BacktestPollState>({
    run: null,
    loading: false,
    error: null,
  });

  useEffect(() => {
    if (runId === null) {
      // runId 가 해제되면 (예: "다시 시도" 버튼) 패널 상태도 초기화.
      setState({ run: null, loading: false, error: null });
      return;
    }

    let cancelled = false;
    let timer: ReturnType<typeof setTimeout> | null = null;

    async function tick() {
      if (cancelled) return;
      // 첫 tick 이전엔 run==null 인 채로 loading 표시; 두 번째 tick 부터는
      // 기존 run 을 유지하면서 background refresh 만 표시.
      setState((prev) => ({ ...prev, loading: true }));
      try {
        const run = await api.getBacktest(runId as number);
        if (cancelled) return;
        setState({ run, loading: false, error: null });
        if (TERMINAL_STATUSES.has(run.status)) return;
        timer = setTimeout(tick, POLL_INTERVAL_MS);
      } catch (e) {
        if (cancelled) return;
        const apiErr = e instanceof ApiError ? e : null;
        setState({ run: null, loading: false, error: apiErr });
        // 폴링 실패 (네트워크 끊김 등) 도 1초 후 재시도. 사용자가 명시적
        // 으로 "다시 시도" 버튼을 누를 때까지 자동 회복 시도.
        timer = setTimeout(tick, POLL_INTERVAL_MS);
      }
    }

    void tick();

    return () => {
      cancelled = true;
      if (timer) {
        clearTimeout(timer);
        timer = null;
      }
    };
  }, [runId]);

  const cancelRun = useCallback(async () => {
    if (runId === null) return;
    try {
      await api.cancelBacktest(runId);
    } catch {
      // 사용자가 이미 종료한 백테스트를 또 취소한 경우 등은 무시.
      // 다음 polling tick 이 status='cancelled' / 404 로 상태를 정정함.
    }
  }, [runId]);

  return { ...state, cancelRun };
}
