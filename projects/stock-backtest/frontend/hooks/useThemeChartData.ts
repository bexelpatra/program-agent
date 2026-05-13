"use client";

/**
 * useThemeChartData — Phase 2 정규화 차트 데이터 훅 (TASK-308).
 *
 * 책임 1개: `api.getThemeChart(themeId, opts)` 호출 + 로딩/에러/데이터
 * 3상태 관리. opts 가 바뀌면 자동 refetch. 호출부는 (data, loading, error,
 * refetch) 만 소비하면 된다.
 *
 * 클린 아키텍처:
 *   - presentation 레이어 (`/themes/[theme_id]/page.tsx`) 가 사용.
 *     domain / data 로 import 되지 않는다.
 *   - api 호출 cadence (단발 + opts 변경 시 refetch) · 상태 머신을
 *     페이지에서 떼어내 페이지를 순수 표현 컴포넌트로 유지한다.
 *
 * 정리 (cleanup) 보장:
 *   - effect 내 `cancelled` 플래그로 unmount / opts 변경 시 in-flight
 *     fetch 의 setState 를 안전하게 끊는다.
 *   - useBacktestPolling (TASK-094) 의 패턴을 따른다.
 */
import { useCallback, useEffect, useRef, useState } from "react";

import { api, ApiError } from "@/lib/api/client";

// `.default([])` 가 붙은 `affected_assets` 로 인해 `z.infer<ThemeChartData
// Schema>` 의 변종 (variance) 이 발생할 수 있어 (frontend/lib/api/types.ts
// 모듈 주석 — TASK-238), state 타입은 실제 호출 반환을 그대로 사용한다.
type ThemeChartData = Awaited<ReturnType<typeof api.getThemeChart>>;

export interface ThemeChartOpts {
  normalize?: "base100";
  weighting?: "equal" | "market_cap";
  start?: string;
  end?: string;
  baseCurrency?: string;
}

export interface UseThemeChartDataResult {
  data: ThemeChartData | null;
  loading: boolean;
  error: ApiError | null;
  /** 동일 opts 로 다시 fetch (예: 사용자 "다시 시도" 버튼). */
  refetch: () => void;
}

export function useThemeChartData(
  themeId: number,
  opts: ThemeChartOpts,
): UseThemeChartDataResult {
  const [data, setData] = useState<ThemeChartData | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<ApiError | null>(null);
  // refetch 트리거 — 값 자체는 중요하지 않고 변화 자체가 effect 를 재시작.
  const [tick, setTick] = useState(0);
  // opts 의 primitive 필드만 effect deps 로 사용해 객체 identity 차이로
  // 인한 무한 refetch 를 방지.
  const { normalize, weighting, start, end, baseCurrency } = opts;
  // 첫 paint 시 loading=true 로 즉시 보여주기 위한 ref (effect 실행 전에
  // setState 호출하지 않도록 mount 여부 추적).
  const mountedRef = useRef(false);

  useEffect(() => {
    let cancelled = false;
    mountedRef.current = true;
    setLoading(true);
    setError(null);

    (async () => {
      try {
        const res = await api.getThemeChart(themeId, {
          normalize,
          weighting,
          start,
          end,
          baseCurrency,
        });
        if (cancelled) return;
        setData(res);
        setError(null);
      } catch (e) {
        if (cancelled) return;
        const apiErr = e instanceof ApiError ? e : null;
        setError(apiErr);
        setData(null);
      } finally {
        if (!cancelled) setLoading(false);
      }
    })();

    return () => {
      cancelled = true;
    };
  }, [themeId, normalize, weighting, start, end, baseCurrency, tick]);

  const refetch = useCallback(() => {
    setTick((n) => n + 1);
  }, []);

  return { data, loading, error, refetch };
}
